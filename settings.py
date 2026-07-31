"""User settings — a small JSON overlay on top of the defaults in config.py.

Everything the Settings window can change lives here, so config.py stays a file you
only touch for advanced tuning. Values are written to

    ~/Library/Application Support/Vexflow/settings.json

Reads are cached; the file is only re-read when it changes on disk, so the engine can
call get() on a hot path without hitting the filesystem every time.
"""
import json
import os
import threading

import config

PATH = os.path.join(config.SUPPORT_DIR, "settings.json")

_LOCK = threading.Lock()
_CACHE = None
_MTIME = None


def defaults():
    provider = config.CLEAN_PROVIDER_DEFAULT
    return {
        # Two different languages live next to each other here. "ui_language" is the
        # one the app talks to you in; "language" is the one it expects to hear.
        # Empty means "follow macOS", and it stays empty until somebody picks one, so
        # a Mac that switches its system language takes Vexflow along with it.
        "ui_language": "",
        "language": config.LANGUAGE_DEFAULT,
        "ptt_key": config.PTT_HOLD_KEY,
        "toggle_key": config.TOGGLE_KEY,
        "mouse_toggle": config.TOGGLE_MOUSE_BUTTON,
        "clean_enabled": True,
        "clean_provider": provider,
        # One remembered model per provider, so switching vendor and back keeps your pick.
        "clean_model": {k: v["default_model"] for k, v in config.CLEAN_PROVIDERS.items()},
        # Per-provider endpoint override, for OpenAI-compatible gateways and local models.
        "api_base": {},
        "play_sounds": True,
        "paste_automatically": True,
        # Read by the launcher script too (it decides where stdout goes before Python
        # starts), so this key has to stay a plain boolean at the top level.
        "logging_enabled": config.LOGGING_DEFAULT,
    }


def _load():
    """Return the settings dict, re-reading the file only when its mtime moved."""
    global _CACHE, _MTIME
    try:
        mtime = os.path.getmtime(PATH)
    except OSError:
        mtime = None
    if _CACHE is not None and mtime == _MTIME:
        return _CACHE
    data = defaults()
    if mtime is not None:
        try:
            with open(PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
            if isinstance(stored, dict):
                for key, value in stored.items():
                    # Merge one level down so a new provider added in a later release
                    # still gets its default model instead of disappearing.
                    if isinstance(data.get(key), dict) and isinstance(value, dict):
                        data[key] = {**data[key], **value}
                    elif key in data:
                        data[key] = value
        except (OSError, ValueError):
            pass   # corrupt or unreadable file must not stop dictation
    _CACHE, _MTIME = data, mtime
    return data


def get(key):
    with _LOCK:
        return _load().get(key)


def set(key, value):
    """Persist one setting. Returns True when it reached disk."""
    global _CACHE, _MTIME
    with _LOCK:
        data = dict(_load())
        data[key] = value
        try:
            os.makedirs(config.SUPPORT_DIR, exist_ok=True)
            tmp = PATH + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, PATH)   # atomic: never leave a half-written settings file
        except OSError:
            return False
        _CACHE = data
        try:
            _MTIME = os.path.getmtime(PATH)
        except OSError:
            _MTIME = None
        return True


# --- Convenience accessors used across the app -------------------------------

def provider():
    """Current cleanup provider id, guarded against a stale value in the file."""
    p = get("clean_provider")
    return p if p in config.CLEAN_PROVIDERS else config.CLEAN_PROVIDER_DEFAULT


def provider_config(name=None):
    return config.CLEAN_PROVIDERS[name or provider()]


def model(name=None):
    """Chosen model id for a provider, falling back to that provider's default."""
    name = name or provider()
    chosen = (get("clean_model") or {}).get(name)
    valid = [m for _, m in config.CLEAN_PROVIDERS[name]["models"]]
    return chosen if chosen in valid else config.CLEAN_PROVIDERS[name]["default_model"]


def set_model(name, model_id):
    models = dict(get("clean_model") or {})
    models[name] = model_id
    return set("clean_model", models)


def api_base(name=None):
    """Endpoint for a provider — the override if set, otherwise the shipped default."""
    name = name or provider()
    override = (get("api_base") or {}).get(name)
    return override or config.CLEAN_PROVIDERS[name]["api"]


def set_api_base(name, url):
    bases = dict(get("api_base") or {})
    if url:
        bases[name] = url
    else:
        bases.pop(name, None)
    return set("api_base", bases)
