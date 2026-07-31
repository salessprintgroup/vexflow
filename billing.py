"""Deepgram balance readout.

Uses a SEPARATE key with only the billing:read scope, so the transcription key never
needs widening. A key that can spend your account and a key that can read it are worth
keeping apart. Bare urllib, no extra dependency. The /balances response shape is
{"balances": [{"amount": <num>, "units": "USD", ...}]}, verified against
developers.deepgram.com.

The polling lives here rather than in the menu bar app so that the Settings window can
ask for a fresh reading the moment a key is saved, without either module importing the
other.
"""
import json
import threading
import urllib.error
import urllib.request

import config
import macos
from logutil import log

API = "https://api.deepgram.com/v1"

# (state, text, amount). state is one of:
#   "missing"     — no billing key stored
#   "checking"    — a reading is on its way
#   "ok"          — text and amount are good
#   "denied"      — Deepgram refused the key, or it has no billing:read scope
#   "unreachable" — network or server problem, says nothing about the key
_LOCK = threading.Lock()
_STATE = ("missing", None, None)
_WAKE = threading.Event()
_THREAD = None


def current():
    """The last reading, as (state, text, amount)."""
    with _LOCK:
        return _STATE


def is_low(state, amount):
    return state == "ok" and amount is not None and amount < config.BALANCE_LOW


def refresh_soon():
    """Read the balance again now instead of at the next interval.

    Called when a key is saved: ten minutes of a stale "Not set" next to a key you just
    pasted reads as the key not working.
    """
    _set(("checking", None, None))
    _WAKE.set()


def start_polling():
    """Begin refreshing in the background. Safe to call once; later calls do nothing."""
    global _THREAD
    if _THREAD is None:
        _THREAD = threading.Thread(target=_loop, daemon=True)
        _THREAD.start()


def _set(state):
    global _STATE
    with _LOCK:
        previous = _STATE
        _STATE = state
    if state[0] != previous[0] or state[1] != previous[1]:
        log(f"  + Deepgram balance: {state[0]}{' ' + state[1] if state[1] else ''}")


def _loop():
    while True:
        # The key is re-read every round rather than captured once: one saved in
        # Settings has to start working without a restart.
        _set(fetch_balance(macos.get_billing_key()))
        _WAKE.wait(config.BALANCE_REFRESH_SEC)
        _WAKE.clear()


def _get(path, key):
    req = urllib.request.Request(f"{API}{path}", headers={"Authorization": f"Token {key}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def fetch_balance(key):
    """One reading, as (state, text, amount). Blocking; called from the poll thread.

    A wrong key and a key without the billing:read scope both answer 401/403, and there
    is nothing to tell them apart with — the message says so rather than guessing.
    """
    if not key:
        return "missing", None, None
    try:
        projects = _get("/projects", key).get("projects", [])
        if not projects:
            return "denied", None, None
        pid = projects[0]["project_id"]
        balances = _get(f"/projects/{pid}/balances", key).get("balances", [])
        total = sum(b.get("amount", 0) for b in balances)
        units = str((balances[0].get("units") if balances else "USD")).upper()
        text = f"${total:,.2f}" if units == "USD" else f"{total:,.2f} {units}"
        return "ok", text, float(total)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return "denied", None, None
        return "unreachable", None, None
    except Exception:
        return "unreachable", None, None
