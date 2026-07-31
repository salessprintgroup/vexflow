"""Timestamped logging, and the log file itself.

The timestamp is not decoration: without it there was no way to line up an empty
recording with a sleep/wake event, which is exactly where the deaf-microphone bug hid.
Transcript text is never logged unless config.DEBUG_TRANSCRIPT is on.

This module OWNS the file. It used to be the launcher script that owned it, pointing
the process's stdout either at the log or at /dev/null according to the setting — a
decision taken before Python started and therefore impossible to revisit. Ticking the
box in Settings changed nothing until the app was restarted, and an execv self-restart
(which does not go through the launcher) inherited whichever answer was true hours
earlier. Writing the file from here makes the setting mean what it says: on starts
writing now, off stops now and deletes it.
"""
import os
import sys
import threading
import time

import config
import settings

_LOCK = threading.Lock()
_FILE = None        # open handle while logging is on
_FORCED = False     # CLI: log to the terminal regardless of the setting


def force_on():
    """Log for this process whatever the setting says.

    For the CLI, whose output goes to the terminal you started it from. The setting is
    about writing a file, and there is no file here.
    """
    global _FORCED
    _FORCED = True


def log(msg, err=False):
    line = f"[{time.strftime('%m-%d %H:%M:%S')}] {msg}"
    if _FORCED:
        print(line, file=sys.stderr if err else sys.stdout, flush=True)
        return
    if not settings.get("logging_enabled"):
        close()      # switched off mid-run: stop on this line, not at the next start
        return
    with _LOCK:
        handle = _handle()
        if handle is None:
            return
        try:
            handle.write(line + "\n")
            handle.flush()   # a crash must not take the last few lines with it
        except OSError:
            _drop()


def close():
    """Let go of the file. Safe to call when it was never open."""
    with _LOCK:
        _drop()


def remove_log():
    """Delete the log, closing it first so the bytes actually go.

    Off has to mean the file is gone, not that it stopped growing — and an unlinked
    file that a handle is still writing to keeps its disk space and comes back to life
    at the next write.
    """
    with _LOCK:
        _drop()
        try:
            os.remove(config.LOG_FILE)
        except OSError:
            pass


def _drop():
    """Close and forget the handle. Caller holds _LOCK."""
    global _FILE
    if _FILE is not None:
        try:
            _FILE.close()
        except OSError:
            pass
        _FILE = None


def _handle():
    """The log file, opened on first use. None if it cannot be opened at all."""
    global _FILE
    if _FILE is None:
        try:
            os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
            _trim()
            _FILE = open(config.LOG_FILE, "a", encoding="utf-8")
        except OSError:
            return None
    return _FILE


def _trim():
    """Keep the last LOG_MAX_BYTES. Checked when the file is opened, which is once a
    run: a crash loop appends tracebacks forever, and this used to reach gigabytes."""
    try:
        if os.path.getsize(config.LOG_FILE) <= config.LOG_MAX_BYTES:
            return
        with open(config.LOG_FILE, "rb") as f:
            f.seek(-config.LOG_MAX_BYTES, os.SEEK_END)
            tail = f.read()
        with open(config.LOG_FILE, "wb") as f:
            f.write(tail)
    except OSError:
        pass
