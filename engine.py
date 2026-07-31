"""Vexflow engine — capture, Deepgram, paste, plus the hotkey and mouse dispatcher.

One engine drives both front ends: the CLI (vexflow.py) and the menu bar app
(vexflow_app.py). An asyncio loop runs on a background thread; hotkeys come from a
single narrow CGEventTap (hotkeys.py) attached to the run loop of the calling thread
(in the app that is main, which NSApplication spins).

Two hard-won behaviours are encoded here and should not be "simplified" away:

* Zombie sessions. A lost push-to-talk release or a forgotten toggle used to record
  forever, ending in one huge paste into whatever had focus. Sessions now have a
  maximum age and the text goes to the clipboard instead of being pasted.
* Deaf microphone after sleep. The stream opens, the mic indicator lights up, and no
  audio arrives. Resetting PortAudio inside the process does not fix it; only
  restarting the process does. The ladder is: rebuild the stream, then execv.
"""
import asyncio
import os
import sys
import threading
import time

import sounddevice as sd

import config
import llm
import macos
import settings
from strings import t
import deepgram_live
from deepgram_live import Transcriber
from hotkeys import HotkeyTap
from logutil import log


def _reset_portaudio():
    """Reset PortAudio. Fixes error -9986 after sleep or an audio device change
    (a stale AudioObjectID cache). The terminate/initialize pair keeps PortAudio's
    atexit counter balanced."""
    try:
        sd._terminate()
    except Exception:
        pass
    finally:
        try:
            sd._initialize()
        except Exception as e:
            log(f"  x PortAudio failed to reinitialise: {e}", err=True)


def _input_device_name():
    """Name of the default input, so the log shows WHERE a session actually recorded
    (built-in mic, headset, a phone over Continuity)."""
    try:
        return sd.query_devices(kind="input")["name"]
    except Exception:
        return "unknown input"


class Session:
    """One recording: open the mic, wait for stop, finalise, paste."""

    def __init__(self, api_key, loop, label="", engine=None, max_age=None):
        self._loop = loop
        self._label = label
        self._engine = engine
        self._max_age = max_age
        self._transcriber = Transcriber(api_key, settings.get("language"))
        self._stream = None
        self._stop_event = asyncio.Event()
        # Audio health, written by the audio callback and read by the watchdog:
        self._frames = 0                        # frames delivered by the callback
        self._nonzero = False                   # has any non-silent sample arrived
        self._last_frame_t = time.monotonic()   # when the last frame arrived
        self._started_t = 0.0
        self._deaf_terminal = False             # still deaf after rebuilding the stream
        self._chars = 0                         # characters produced, for the usage line

    def request_stop(self):
        self._loop.call_soon_threadsafe(self._stop_event.set)

    def log_usage(self):
        """One line per recording, so Deepgram spend can be measured after the fact.

        Audio seconds are counted from delivered frames rather than from the wall
        clock: that is what actually went up the websocket, and it is what Deepgram
        meters. The character count is the other half — how much text came back for
        that audio.

        Nothing here is content, by construction. A duration and a count cannot be read
        back into words, and the text itself never leaves the process. Grep the log for
        "= usage" to add it all up.
        """
        audio = self._frames * config.BLOCKSIZE / config.SAMPLE_RATE
        cleanup = ("off" if not settings.get("clean_enabled")
                   else f"{settings.provider()}/{settings.model()}")
        log(f"  = usage audio={audio:.1f}s chars={self._chars} "
            f"language={settings.get('language')} cleanup={cleanup}")

    def _open_stream(self):
        """Open and start the mic; on failure close the half-open stream, or it leaks."""
        stream = sd.RawInputStream(
            samplerate=config.SAMPLE_RATE, channels=config.CHANNELS,
            dtype="int16", blocksize=config.BLOCKSIZE, callback=self._audio_cb)
        try:
            stream.start()
        except Exception:
            try:
                stream.close()
            except Exception:
                pass
            raise
        return stream

    def _audio_cb(self, indata, frames, time_info, status):
        if status:
            log(f"  ! audio: {status}", err=True)  # input overflow means dropped frames
        chunk = bytes(indata)
        self._frames += 1
        self._last_frame_t = time.monotonic()
        if not self._nonzero and chunk.count(0) != len(chunk):
            self._nonzero = True   # a live mic has a noise floor; all zeroes means dead input
        try:
            self._loop.call_soon_threadsafe(self._transcriber.send, chunk)
        except RuntimeError:
            pass  # loop died (the watchdog handles it) — never crash the PortAudio callback

    async def run(self):
        self._started_t = time.monotonic()
        # Open the mic first and buffer PCM while the websocket connects, so the first
        # word is not lost.
        try:
            self._stream = self._open_stream()
        except Exception as e:
            # One PortAudio reset and retry: after sleep or a device change the first
            # open fails with -9986 permanently until PortAudio is reinitialised.
            log(f"  ! microphone: {e} — resetting PortAudio and retrying", err=True)
            _reset_portaudio()
            await asyncio.sleep(0.3)
            try:
                self._stream = self._open_stream()
            except Exception as e2:
                log(f"  x microphone: {e2}", err=True)
                macos.play_error_sound()
                if self._engine is not None:
                    self._engine.notice = "Microphone did not open — check input and permissions"
                    # "Failed to open twice" is the same family as "opened deaf": in
                    # practice only a process restart clears it.
                    self._engine.report_audio_health(True)
                return
        log(f"  * recording{self._label} [{_input_device_name()}]")
        if settings.get("play_sounds"):
            macos.play_sound(config.START_SOUND, config.START_SOUND_RATE)

        try:
            await self._transcriber.start()
        except Exception as e:
            # After wake the network may still be down (observed: timed out during
            # opening handshake). One retry a second later; the mic is already open and
            # the queue is buffering, so a successful retry loses no speech.
            log(f"  ! Deepgram connect: {type(e).__name__} — retrying in 1s", err=True)
            await asyncio.sleep(1.0)
            try:
                await self._transcriber.start()
            except Exception as e2:
                self._close_stream()
                status = deepgram_live._status_of(e2)
                log(f"  x Deepgram connect: {e2}", err=True)
                macos.play_error_sound()
                if self._engine is not None:
                    if status in (401, 403):
                        # Not a network problem. Say which one it is, and flip the
                        # menu bar to the not-ready glyph so it is visible without
                        # opening any menu.
                        self._engine.key_state = "invalid"
                        self._engine.key_detail = f"Deepgram rejected this key (HTTP {status})"
                        self._engine.notice = "Deepgram rejected your key — open Settings"
                    else:
                        self._engine.notice = "Deepgram unreachable — check your connection"
                return

        # Wait for: the user stopping, the websocket dying, or the duration ceiling.
        # In parallel, watch for a deaf stream (mic open but no frames, or pure silence).
        watcher = asyncio.ensure_future(self._watch_audio())
        stop_w = asyncio.ensure_future(self._stop_event.wait())
        dead_w = asyncio.ensure_future(self._transcriber.wait_closed())
        done, pending = await asyncio.wait(
            {stop_w, dead_w}, timeout=self._max_age,
            return_when=asyncio.FIRST_COMPLETED)
        for pending_task in pending:
            pending_task.cancel()
        watcher.cancel()
        timed_out = not done
        ws_died = dead_w in done and stop_w not in done
        recorded = time.monotonic() - self._started_t
        self._close_stream()
        if settings.get("play_sounds"):
            macos.play_sound(config.STOP_SOUND, config.STOP_SOUND_RATE)

        text = await self._transcriber.finish()
        # Evidence of a deaf session: no frames at all despite a real duration, or
        # every sample a digital zero. A live mic cannot do that, so fix it rather
        # than waiting for the user to notice.
        deaf = (self._deaf_terminal
                or (self._frames == 0 and recorded >= config.DEAF_MIN_SESSION_SEC)
                or (not self._nonzero and recorded >= config.DEAF_ALL_ZERO_SEC))
        if not text:
            if self._deaf_terminal:
                log("  x microphone deaf even after rebuilding the stream — speech lost",
                    err=True)
            else:
                log(f"  . empty ({recorded:.1f}s, {self._frames} frames, "
                    f"audio: {'yes' if self._nonzero else 'no'})")
            if self._engine is not None:
                if ws_died:
                    self._engine.notice = "Deepgram connection dropped — text lost"
                elif self._deaf_terminal:
                    self._engine.notice = "Microphone is dead — restarting"
            if deaf or ws_died:
                macos.play_error_sound()   # speech went nowhere, say so immediately
            if self._engine is not None:
                self._engine.report_audio_health(deaf, terminal=self._deaf_terminal)
            return
        if self._engine is not None:
            self._engine.report_audio_health(False)
        if config.DEBUG_TRANSCRIPT:
            log(f"  [raw] {text}")

        eng = self._engine
        if eng is not None and settings.get("clean_enabled"):
            provider = settings.provider()
            key = eng.llm_key(provider)
            if key:
                cleaned = await self._loop.run_in_executor(
                    None, llm.clean, text, provider, key,
                    settings.model(provider), settings.api_base(provider))
                if cleaned:
                    if config.DEBUG_TRANSCRIPT and cleaned != text:
                        log(f"  [clean] {cleaned}")
                    text = cleaned

        self._chars = len(text)   # the final count, whichever way the text is delivered

        if timed_out or ws_died:
            # Pasting minutes later, or after a dropped connection, is dangerous: wrong
            # place, wrong time. Put it on the clipboard and tell the user.
            macos.set_text(text)
            why = t("duration limit") if timed_out else t("Deepgram connection dropped")
            log(f"  ! recording stopped ({why}) — text is on the clipboard ({len(text)} chars)")
            macos.play_error_sound()   # without a signal the user keeps talking into nothing
            if eng is not None:
                eng.notice = t("Stopped ({}) — text is on the clipboard, "
                               "press Cmd-V").format(why)
            return

        if settings.get("paste_automatically"):
            await self._insert(text)
            log(f"  + pasted ({len(text)} chars)")   # never log the content itself
        else:
            macos.set_text(text)
            log(f"  + copied ({len(text)} chars)")
            if eng is not None:
                eng.notice = "Copied — press Cmd-V to paste"

    async def _watch_audio(self):
        """Watch for a deaf stream: mic indicator on, but no frames, or pure zeroes,
        or frames that stopped. First verdict rebuilds the stream in place (PortAudio
        reset plus a fresh device; the session and websocket survive, only the
        un-recorded part is lost). Second verdict stops the session and escalates to
        the engine, because that wedge only clears on a process restart."""
        healed = False
        base = time.monotonic()
        try:
            while True:
                await asyncio.sleep(0.5)
                now = time.monotonic()
                frames = self._frames
                dead = (
                    (frames == 0 and now - base >= config.DEAF_NO_FRAMES_SEC)
                    or (frames > 0 and now - self._last_frame_t >= config.DEAF_STALL_SEC)
                    or (frames > 0 and not self._nonzero
                        and now - base >= config.DEAF_ALL_ZERO_SEC))
                if not dead:
                    continue
                dev = _input_device_name()
                if healed:
                    log(f"  x stream still deaf after a rebuild ({dev}) — stopping",
                        err=True)
                    self._deaf_terminal = True
                    self._stop_event.set()
                    return
                log(f"  ! microphone silent ({dev}: {frames} frames, audio "
                    f"{'seen' if self._nonzero else 'never arrived'}) — rebuilding stream",
                    err=True)
                self._close_stream()
                _reset_portaudio()
                try:
                    self._stream = self._open_stream()
                except Exception as e:
                    log(f"  x rebuilding the stream failed: {e}", err=True)
                    self._deaf_terminal = True
                    self._stop_event.set()
                    return
                healed = True
                self._frames = 0
                self._nonzero = False
                base = time.monotonic()
                self._last_frame_t = base
                if self._engine is not None:
                    self._engine.notice = "Microphone rebuilt mid-recording — the start may be lost"
        except asyncio.CancelledError:
            raise
        except Exception as e:   # the watchdog must not die quietly, it is the detector
            log(f"  ! audio watchdog crashed: {type(e).__name__}: {e}", err=True)

    def _close_stream(self):
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None

    async def _insert(self, text):
        snapshot = macos.save_clipboard()
        macos.set_text(text)
        owned = macos.change_count()   # our write, as of right now
        await asyncio.sleep(config.PASTE_PRE_DELAY)
        macos.paste()                  # waits internally for Shift/Opt/Ctrl to lift
        # Restore in the background: the session ends immediately so push-to-talk is
        # free again, and the clipboard comes back after PASTE_POST_DELAY if nobody
        # else has written to it meanwhile.
        if self._engine is not None:
            self._engine.schedule_restore(snapshot, owned)


class Engine:
    """Hotkeys and mouse (one CGEventTap) plus orchestration. One recording at a time.

    .state   — "idle" | "recording", read by the UI.
    .paused  — blocks new recordings from starting.
    .notice  — one-line message for the menu (mic or network error, timeout); cleared
               when the next recording starts.
    """

    def __init__(self):
        self._api_key = None
        self._llm_keys = {}
        self._loop = None
        self._session = None
        self._mode = None        # "ptt" | "toggle" | None
        self.state = "idle"
        self.paused = False
        self.notice = None
        self.hotkeys_live = False
        # "missing" | "checking" | "valid" | "invalid" | "unreachable".
        # A key that exists is not a key that works, and the difference used to be
        # invisible: a wrong key produced a normal-looking app that silently returned
        # no text. The state is checked at startup and whenever a key is saved.
        self.key_state = "missing"
        self.key_detail = ""
        # The same, per cleanup provider. A wrong key here is quieter still: dictation
        # keeps working and only the cleanup is silently skipped.
        self.llm_key_state = {p: "missing" for p in config.CLEAN_PROVIDERS}
        self.llm_key_detail = {p: "" for p in config.CLEAN_PROVIDERS}
        self._tap = None
        self._thread = None
        self._bg = set()             # background tasks (clipboard restore) — keep refs
        self._last_toggle = 0.0      # debounce for a bouncy middle mouse button
        self._deaf_streak = 0        # consecutive deaf sessions
        self._audio_reset_pending = False   # wake during a recording defers the reset
        self._argv = None            # how to restart ourselves (execv) on dead audio

    # --- keys ---------------------------------------------------------------

    def reload_keys(self):
        """Re-read every key from the Keychain, so a key saved in Settings works
        without a restart.

        Verification is the caller's call, not this method's: only the caller knows
        WHICH key changed. Re-checking all of them on every save put the menu bar icon
        back into "checking" and made a working Deepgram key look briefly broken
        because an unrelated cleanup key had been pasted.
        """
        self._api_key = macos.get_api_key()
        self._llm_keys = {p: macos.get_llm_key(p) for p in config.CLEAN_PROVIDERS}
        self.notice = None

    def verify_key(self, done=None):
        """Check the Deepgram key against Deepgram, off the calling thread.

        `done` is invoked with (state, detail) on the loop thread when finished, so the
        Settings window can report the result next to the field the user just used.
        """
        if self._loop is None:
            return
        if not self._api_key:
            self.key_state, self.key_detail = "missing", ""
            if done is not None:
                done("missing", "")
            return

        async def _run():
            self.key_state, self.key_detail = "checking", ""
            state, detail = await deepgram_live.check_key(
                self._api_key, settings.get("language"))
            self.key_state, self.key_detail = state, detail
            log(f"  + Deepgram key: {state}{' — ' + detail if detail else ''}")
            if done is not None:
                done(state, detail)

        asyncio.run_coroutine_threadsafe(_run(), self._loop)

    def verify_llm_key(self, provider):
        """Check one cleanup key against its vendor, on a throwaway thread.

        A plain thread rather than the asyncio loop: the vendor calls are blocking
        urllib, and the loop belongs to the recording path.
        """
        key = self._llm_keys.get(provider)
        if not key:
            self.llm_key_state[provider] = "missing"
            self.llm_key_detail[provider] = ""
            return

        def _run():
            self.llm_key_state[provider] = "checking"
            state, detail = llm.check_key(provider, key, settings.model(provider),
                                          settings.api_base(provider))
            self.llm_key_state[provider] = state
            self.llm_key_detail[provider] = detail
            label = config.CLEAN_PROVIDERS[provider]["label"]
            log(f"  + {label} key: {state}{' — ' + detail if detail else ''}")

        threading.Thread(target=_run, daemon=True).start()

    def verify_llm_keys(self):
        """Check every cleanup key that exists. Ones that do not are left as missing."""
        for provider in config.CLEAN_PROVIDERS:
            self.verify_llm_key(provider)

    def llm_key(self, provider):
        return self._llm_keys.get(provider)

    @property
    def has_key(self):
        return bool(self._api_key)

    @property
    def has_any_llm_key(self):
        return any(self._llm_keys.values())

    # --- lifecycle ----------------------------------------------------------

    def start(self):
        """Bring up the background loop and the event tap (on the caller's run loop)."""
        macos.prompt_accessibility()
        self._api_key = macos.get_api_key()
        self._llm_keys = {p: macos.get_llm_key(p) for p in config.CLEAN_PROVIDERS}
        # For self-healing dead CoreAudio: restart with the same interpreter and script
        # (vexflow_app.py or vexflow.py). Works under launchd and from the CLI.
        self._argv = [sys.executable, os.path.abspath(sys.argv[0])]
        age = macos.restart_marker_age()
        if age is not None and age < 60:
            self.notice = "Restarted after a dead microphone — please dictate again"
        if config.DEBUG_TRANSCRIPT:
            log("  ! VEXFLOW_DEBUG_TRANSCRIPT is set — dictated text WILL be written "
                "to the log for this run", err=True)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self.verify_key()
        self.verify_llm_keys()
        self._bind_tap()

    def _bind_tap(self):
        ptt = settings.get("ptt_key")
        toggle = settings.get("toggle_key") or ""
        try:
            self._tap = self._make_tap(ptt, toggle)
        except ValueError as e:
            # A bad hotkey in settings must not leave the app with no tap at all —
            # that would look exactly like "dictation is broken" with nothing in the
            # log to explain it. Fall back to the shipped default and say so.
            log(f"  x hotkey {ptt!r} rejected: {e} — falling back to "
                f"{config.PTT_HOLD_KEY!r}", err=True)
            self.notice = f"Hotkey {ptt!r} is not valid — using {config.PTT_HOLD_KEY}"
            self._tap = self._make_tap(config.PTT_HOLD_KEY, "")
        self.hotkeys_live = self._tap.start()
        if not self.hotkeys_live:
            self.notice = "No Accessibility permission — hotkeys are dead"
            log("  x event tap not created (missing Accessibility?)", err=True)
        else:
            log(f"  + hotkeys bound: ptt={ptt!r} toggle={toggle!r} "
                f"mouse={bool(settings.get('mouse_toggle'))}")

    def _make_tap(self, ptt, toggle):
        return HotkeyTap(
            ptt, toggle,
            on_ptt_down=lambda: self._loop.call_soon_threadsafe(self._ptt_down),
            on_ptt_up=lambda: self._loop.call_soon_threadsafe(self._ptt_up),
            on_toggle=lambda: self._loop.call_soon_threadsafe(self._toggle),
            mouse_toggle=bool(settings.get("mouse_toggle")))

    def rebind_hotkeys(self):
        """Rebuild the tap after the Settings window changed a key. Must run on the
        thread that owns the run loop, which is where the Settings actions fire."""
        if self._tap is not None:
            self._tap.stop()
        self._bind_tap()   # logs what it actually bound, including any fallback

    def stop(self, wait_session=0.0):
        """Stop the tap and optionally wait up to wait_session for an active recording."""
        if self._tap:
            self._tap.stop()
        if self._session is not None:
            self._session.request_stop()
            deadline = time.monotonic() + wait_session
            while self._session is not None and time.monotonic() < deadline:
                time.sleep(0.1)
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)

    def ensure_loop(self):
        """Bring the background loop thread back if it died (watchdog insurance)."""
        if self._thread is None or not self._thread.is_alive():
            if self._session is not None:
                # The session lived on a dead loop, so its finally block will never
                # run. Without this reset, new recordings would be blocked forever.
                log("  ! loop died with an active session — state reset", err=True)
                self._session = None
                self._mode = None
                self.state = "idle"
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
            self._thread.start()

    def heal(self):
        """Watchdog and wake: cheaply repair anything that may have died. Nothing is
        recreated — the tap is simply re-enabled, which does not interrupt a recording."""
        self.ensure_loop()
        revived = self._tap.heal() if self._tap else False
        if revived:
            log("  ! event tap had been disabled by the system — re-enabled", err=True)
        # Zombie push-to-talk: the release was lost while the tap was dead (the hotkey
        # is not physically held, yet a recording is running) — close it cleanly.
        # Toggle is left alone; it is supposed to live a long time.
        if (self._mode == "ptt" and self._session is not None
                and self._tap is not None and not self._tap.ptt_physically_held()):
            if self._tap:
                self._tap.reset_ptt()
            self._loop.call_soon_threadsafe(self._force_ptt_stop)

    def reset_audio(self):
        """Reset PortAudio after wake (marshalled onto the loop, so it is serialised
        with session start)."""
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._reset_audio_on_loop)

    def _reset_audio_on_loop(self):
        if self._session is not None:
            # An active recording holds the stream; PortAudio must not be touched
            # underneath it. This reset used to be dropped SILENTLY here, so the first
            # session after sleep recorded into a deaf stream.
            self._audio_reset_pending = True
            log("  ! recording in progress — PortAudio reset deferred", err=True)
            return
        _reset_portaudio()

    def report_audio_health(self, deaf, terminal=False):
        """Track deaf sessions. One triggers a precautionary PortAudio reset; two in a
        row, or "deaf even after a stream rebuild", restarts the process — the logs say
        that wedge clears no other way."""
        if not deaf:
            self._deaf_streak = 0
            return
        self._deaf_streak += 1
        if terminal or self._deaf_streak >= 2:
            self._deaf_streak = 0
            self._self_restart_for_audio()   # execv: normally does not return
        else:
            _reset_portaudio()
            log("  ! deaf session — PortAudio reset as a precaution", err=True)

    def _self_restart_for_audio(self):
        """Restart in place (execv: same PID, fresh process, new coreaudiod client).
        This automates exactly what used to be done by hand with launchctl kickstart.
        The cooldown marker prevents a loop when audio is dead system-wide."""
        age = macos.restart_marker_age()
        if age is not None and age < config.SELF_RESTART_COOLDOWN_SEC:
            self.notice = "Microphone still dead after a restart — check System Settings > Sound"
            log(f"  x audio dead, but the last self-restart was {age:.0f}s ago — not looping",
                err=True)
            return
        macos.touch_restart_marker()
        log("  ~ audio is dead in this process — restarting Vexflow (execv)")
        try:
            os.execv(self._argv[0], self._argv)
        except Exception as e:
            log(f"  x execv failed: {e}", err=True)
            self.notice = "Microphone is dead — restart Vexflow manually"

    def schedule_restore(self, snapshot, owned):
        """Put the clipboard back in the background: wait up to PASTE_POST_DELAY and
        restore only if the clipboard is still ours (changeCount unmoved — otherwise
        somebody else's content is there now)."""
        async def _restore_later():
            waited = 0.0
            while waited < config.PASTE_POST_DELAY:
                await asyncio.sleep(0.1)
                waited += 0.1
                if macos.change_count() != owned:
                    return
            if macos.change_count() == owned:
                macos.restore_clipboard(snapshot)
        task = self._loop.create_task(_restore_later())
        self._bg.add(task)
        task.add_done_callback(self._bg.discard)

    def request_stop_active(self):
        """Emergency stop from the menu — works even if the hotkey tap has died."""
        session = self._session
        if session is not None:
            session.request_stop()

    # --- orchestration (all on the loop thread) -----------------------------

    def _ptt_down(self):
        if self._session is None and not self.paused:
            self._begin("ptt", "")

    def _ptt_up(self):
        if self._session is not None and self._mode == "ptt":
            self._session.request_stop()

    def _force_ptt_stop(self):
        """Close a zombie push-to-talk from heal() (release lost to a dead tap)."""
        if self._session is not None and self._mode == "ptt":
            log("  ! push-to-talk release was lost (tap was dead) — closing", err=True)
            self._session.request_stop()

    def _toggle(self):
        now = time.monotonic()
        if now - self._last_toggle < 0.15:   # middle mouse button bounce
            return
        self._last_toggle = now
        if self._session is None:
            if not self.paused:
                self._begin("toggle", " (toggle — tap again to stop)")
        elif self._mode == "toggle":
            self._session.request_stop()
        # a push-to-talk session is running -> ignore the toggle

    def _begin(self, mode, label):
        if not self._api_key:
            self.notice = "No Deepgram key — open Settings"
            macos.play_error_sound()
            return
        if self.key_state == "invalid":
            # Refusing here beats opening the microphone, recording, and discarding it.
            self.notice = "Deepgram rejected your key — open Settings"
            macos.play_error_sound()
            return
        self.notice = None
        max_age = config.MAX_PTT_SEC if mode == "ptt" else config.MAX_TOGGLE_SEC
        session = Session(self._api_key, self._loop, label, self, max_age=max_age)
        self._session = session
        self._mode = mode
        self.state = "recording"
        asyncio.create_task(self._run(session))

    async def _run(self, session):
        try:
            await session.run()
        finally:
            # Here rather than inside run(), which returns from five different places.
            session.log_usage()
            self._session = None
            self._mode = None
            self.state = "idle"
            if self._audio_reset_pending:   # wake landed during a recording
                self._audio_reset_pending = False
                _reset_portaudio()
                log("  + deferred PortAudio reset done")
