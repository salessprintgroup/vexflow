"""Deepgram live streaming over a bare websocket — the smallest auditable surface."""
import asyncio
import json
from urllib.parse import urlencode

from websockets.asyncio.client import connect

import config
from logutil import log


def _status_of(exc):
    """HTTP status behind a failed handshake, across websockets versions."""
    for attr in ("response", "status_code"):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value
        code = getattr(value, "status_code", None)
        if isinstance(code, int):
            return code
    return None


async def check_key(api_key, language=None):
    """Validate a Deepgram key: open the exact websocket dictation uses, then close it
    without sending audio. Returns (state, detail) where state is
    "missing" | "valid" | "invalid" | "unreachable".

    There is no cheaper honest check. Deepgram's management endpoints (/v1/projects,
    /v1/auth/token) answer 401 for a transcription-scoped key just as they do for a
    wrong one, so they cannot tell a bad key from a correctly narrow key. The handshake
    can, it costs nothing, and it exercises the same URL, headers and parameters the
    real session uses — including a typo in DEEPGRAM_PARAMS.
    """
    if not api_key:
        return "missing", ""
    try:
        ws = await asyncio.wait_for(
            connect(_build_url(language),
                    additional_headers={"Authorization": f"Token {api_key}"},
                    max_size=None),
            timeout=config.KEY_CHECK_TIMEOUT)
    except Exception as e:
        status = _status_of(e)
        if status in (401, 403):
            return "invalid", f"Deepgram rejected this key (HTTP {status})"
        if status is not None:
            return "unreachable", f"Deepgram answered HTTP {status}"
        return "unreachable", type(e).__name__
    try:
        await ws.close()
    except Exception:
        pass
    return "valid", ""


def _build_url(language=None):
    params = {**config.DEEPGRAM_PARAMS, "language": language or config.LANGUAGE_DEFAULT}
    return f"{config.DEEPGRAM_HOST}?{urlencode(params)}"


class Transcriber:
    """One recording: open the socket, stream PCM, collect finals, close.

        t = Transcriber(api_key)
        t.send(pcm)              # safe to call BEFORE start(); frames are buffered
        await t.start()          # connect plus background sender and receiver
        text = await t.finish()  # flush, CloseStream, await finals, return the text
    """

    def __init__(self, api_key, language=None):
        self._api_key = api_key
        self._language = language or config.LANGUAGE_DEFAULT
        self._ws = None
        # Bounded: when the socket is dead the oldest frames are dropped rather than
        # accumulating gigabytes.
        self._send_q = asyncio.Queue(maxsize=config.SEND_QUEUE_MAX)
        self._segments = []              # final transcripts, in order
        self._send_task = None
        self._recv_task = None
        self._closed = asyncio.Event()
        self._dropped = 0                # frames discarded to queue overflow

    def send(self, pcm: bytes):
        """Queue one PCM frame (called from the audio callback via call_soon_threadsafe)."""
        try:
            self._send_q.put_nowait(pcm)
        except asyncio.QueueFull:
            try:
                self._send_q.get_nowait()   # drop the oldest frame
                self._send_q.task_done()
            except asyncio.QueueEmpty:
                pass
            self._send_q.put_nowait(pcm)
            self._dropped += 1
            if self._dropped == 1 or self._dropped % 300 == 0:  # log ~ every 30s of loss
                log(f"  ! audio queue full: dropped {self._dropped} frames "
                    f"(upload to Deepgram is behind or broken)", err=True)

    async def wait_closed(self):
        """Wait for the receiver to die (socket closed or failed) — drop detection."""
        await self._closed.wait()

    async def start(self):
        self._ws = await connect(
            _build_url(self._language),
            additional_headers={"Authorization": f"Token {self._api_key}"},
            max_size=None,
        )
        self._send_task = asyncio.create_task(self._sender())
        self._recv_task = asyncio.create_task(self._receiver())

    async def _sender(self):
        while True:
            chunk = await self._send_q.get()
            try:
                if chunk is None:        # shutdown sentinel
                    break
                await self._ws.send(chunk)
            except Exception as e:
                log(f"  ! upload to Deepgram broke: {type(e).__name__}", err=True)
                break
            finally:
                self._send_q.task_done()

    async def _receiver(self):
        try:
            async for msg in self._ws:
                try:
                    if isinstance(msg, bytes):
                        continue
                    data = json.loads(msg)
                    if data.get("type") == "Results" and data.get("is_final"):
                        alts = data.get("channel", {}).get("alternatives") or []
                        if alts:
                            t = alts[0].get("transcript", "").strip()
                            if t:
                                self._segments.append(t)
                except Exception:
                    continue  # one malformed message must not kill the receiver
        except Exception:
            pass
        finally:
            self._closed.set()

    async def finish(self):
        """Stop sending, flush the queue, CloseStream, await finals, return the text."""
        # Let already-scheduled send() callbacks from the audio thread run (last frame).
        await asyncio.sleep(0.05)
        # Finish the sender once the queue has drained.
        try:
            self._send_q.put_nowait(None)
        except asyncio.QueueFull:      # queue jammed with a dead tail — make room
            self._send_q.get_nowait()
            self._send_q.task_done()
            self._send_q.put_nowait(None)
        try:
            await asyncio.wait_for(self._send_q.join(), timeout=2.0)
        except asyncio.TimeoutError:
            left = self._send_q.qsize()
            log(f"  ! audio tail did not upload in time (~{left} frames "
                f"= {left / 10:.0f}s)", err=True)
        # Tell Deepgram to finish its buffer and close.
        try:
            await self._ws.send(json.dumps({"type": "CloseStream"}))
        except Exception:
            pass
        # Wait for the receiver to consume the finals and the socket to close.
        try:
            await asyncio.wait_for(self._closed.wait(), timeout=config.FINALIZE_TIMEOUT)
        except asyncio.TimeoutError:
            pass
        for task in (self._send_task, self._recv_task):
            if task and not task.done():
                task.cancel()
        try:
            await self._ws.close()
        except Exception:
            pass
        return " ".join(self._segments).strip()
