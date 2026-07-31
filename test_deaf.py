"""Regression test for the deaf-microphone watchdog — no real mic, socket or sound.

A fake stream drives Session._audio_cb the way PortAudio would (modes: deaf, all
zeroes, live, frames that stall), a fake transcriber swallows the frames, and execv is
mocked. The detection thresholds are monkeypatched down to fractions of a second, so
the whole run takes about seven seconds.

It covers the full ladder: rebuild the stream in place -> terminal stop ->
report_audio_health -> execv, including the restart cooldown.

    .venv/bin/python test_deaf.py      # 12 assertions, exit 1 on failure
"""
import asyncio
import sys
import threading
import time

import config

# Speed the thresholds up for the test (production values are 2.0 / 2.5 / 5.0 / 0.8).
config.DEAF_NO_FRAMES_SEC = 0.6
config.DEAF_STALL_SEC = 0.8
config.DEAF_ALL_ZERO_SEC = 1.2
config.DEAF_MIN_SESSION_SEC = 0.3
config.ERROR_SOUND = None   # stay quiet during the run

import engine    # noqa: E402  (imported after the thresholds are patched)
import macos     # noqa: E402

FRAME = b"\x00" * 3200          # 100 ms of silence
NOISY = b"\x01\x00" * 1600      # 100 ms of "noise"

SOUNDS = []
macos.play_error_sound = lambda: SOUNDS.append(1)
macos.play_sound = lambda path: None


class FakeSettings:
    """Just enough of the settings module for Session and Engine."""
    _values = {
        "language": "en",
        "play_sounds": False,
        "clean_enabled": False,
        "paste_automatically": True,
        "ptt_key": "cmd_r",
        "toggle_key": "",
        "mouse_toggle": False,
    }

    @staticmethod
    def get(key):
        return FakeSettings._values.get(key)

    @staticmethod
    def provider():
        return "anthropic"

    @staticmethod
    def model(name=None):
        return "test-model"

    @staticmethod
    def api_base(name=None):
        return "http://localhost/unused"


class FakeStream:
    """Mimics a PortAudio stream: a thread calls the callback every 100 ms."""
    mode = "noisy"          # noisy | zeros | deaf | stall_after_5

    def __init__(self, callback):
        self._cb = callback
        self._run = False
        self._thread = None

    def start(self):
        self._run = True
        self._thread = threading.Thread(target=self._pump, daemon=True)
        self._thread.start()

    def _pump(self):
        n = 0
        while self._run:
            time.sleep(0.1)
            if not self._run:
                break
            if FakeStream.mode == "deaf":
                continue
            if FakeStream.mode == "stall_after_5" and n >= 5:
                continue
            n += 1
            self._cb(NOISY if FakeStream.mode in ("noisy", "stall_after_5") else FRAME,
                     1600, None, None)

    def stop(self):
        self._run = False

    def close(self):
        self._run = False


class FakeSD:
    @staticmethod
    def RawInputStream(samplerate=None, channels=None, dtype=None, blocksize=None,
                       callback=None):
        return FakeStream(callback)

    @staticmethod
    def query_devices(kind=None):
        return {"name": "Fake Mic"}

    @staticmethod
    def _terminate():
        pass

    @staticmethod
    def _initialize():
        pass


class FakeTranscriber:
    def __init__(self, *a, **k):
        self._closed = asyncio.Event()

    def send(self, pcm):
        pass

    async def start(self):
        pass

    async def wait_closed(self):
        await self._closed.wait()

    async def finish(self):
        return ""


class FakeEngine:
    def __init__(self):
        self.notice = None
        self.reports = []

    def report_audio_health(self, deaf, terminal=False):
        self.reports.append((deaf, terminal))

    def schedule_restore(self, *a):
        pass

    def llm_key(self, provider):
        return None


engine.sd = FakeSD
engine.Transcriber = FakeTranscriber
engine.settings = FakeSettings


async def run_session(mode, stop_after=None, max_age=None):
    FakeStream.mode = mode
    eng = FakeEngine()
    s = engine.Session("key", asyncio.get_running_loop(), engine=eng, max_age=max_age)
    if stop_after is not None:
        asyncio.get_running_loop().call_later(stop_after, s._stop_event.set)
    t0 = time.monotonic()
    await s.run()
    return eng, s, time.monotonic() - t0


def check(name, cond):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}")
    if not cond:
        sys.exit(1)


async def main():
    # 1. Deaf stream: heal at ~0.6s, terminal at ~1.2-1.7s, closes without the user.
    eng, s, dt = await run_session("deaf")
    check(f"deaf: terminal after {dt:.1f}s with no user action",
          dt < 4 and s._deaf_terminal)
    check("deaf: report(deaf=True, terminal=True)", eng.reports == [(True, True)])
    check("deaf: notice mentions the restart", "restarting" in (eng.notice or "").lower())

    # 2. Live stream, user stopped: empty result, but NOT deaf.
    eng, s, dt = await run_session("noisy", stop_after=0.7)
    check("live: not terminal", not s._deaf_terminal)
    check("live: report(deaf=False)", eng.reports == [(False, False)])

    # 3. All zeroes: deaf at ~1.2s, heal, still zeroes, terminal.
    eng, s, dt = await run_session("zeros")
    check(f"zeroes: terminal after {dt:.1f}s",
          s._deaf_terminal and eng.reports == [(True, True)])

    # 4. Frames arrived and stalled (sleep, device unplugged): heal brings them back.
    eng, s, dt = await run_session("stall_after_5", stop_after=2.5)
    check("stall: heal restored frames, not terminal", not s._deaf_terminal)
    check("stall: notice mentions the rebuild", "rebuilt" in (eng.notice or "").lower())
    check("stall: report(deaf=False)", eng.reports == [(False, False)])

    # 5. A short deaf tap (below DEAF_MIN_SESSION_SEC) proves nothing.
    eng, s, dt = await run_session("deaf", stop_after=0.15)
    check("short tap: not treated as evidence", eng.reports == [(False, False)])

    print("SESSION TESTS OK")


asyncio.run(main())

# 6. Engine.report_audio_health: escalation and cooldown, without a real execv.
EXECS = []
engine.os.execv = lambda p, a: EXECS.append((p, a))
macos.restart_marker_age = lambda: None          # no cooldown in force
macos.touch_restart_marker = lambda: None


def _engine():
    e = engine.Engine()
    e._argv = ["/usr/bin/true", "/usr/bin/true"]
    return e


e = _engine()
e.report_audio_health(True)                       # streak 1 -> PortAudio reset only
check("streak 1: no restart", not EXECS)
e.report_audio_health(True)                       # streak 2 -> execv
check("streak 2: execv", len(EXECS) == 1)
e2 = _engine()
e2.report_audio_health(True, terminal=True)       # terminal -> execv immediately
check("terminal: execv immediately", len(EXECS) == 2)
macos.restart_marker_age = lambda: 10.0           # fresh marker -> cooldown applies
e3 = _engine()
e3.report_audio_health(True, terminal=True)
check("cooldown: no execv, notice instead",
      len(EXECS) == 2 and "System Settings" in (e3.notice or ""))
print("ENGINE TESTS OK")
