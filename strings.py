"""User-facing text, in whichever language the interface is set to.

The English source string is also the lookup key, so a missing translation falls back
to English instead of showing a bare identifier, and the call sites stay readable:
t("Open log") says what it will draw.

Only text a user can see belongs here. Log lines stay English on purpose — they are
grep targets, they are quoted in the documentation, and they are read by whoever is
debugging rather than by whoever is dictating.

The tables live one per language in i18n/, loaded on demand. A session touches exactly
one of them, and somebody fixing Polish opens a file nobody else is editing.
"""
import importlib
import os

import config
import settings

_TABLES = {}      # language code -> table, filled on first use
_SYSTEM = None    # what macOS is set to, worked out once


def available():
    """Language codes there is an interface for, English included."""
    return [code for _, code in config.UI_LANGUAGES]


def _system_language():
    """The first of the user's macOS languages that Vexflow has an interface for."""
    global _SYSTEM
    if _SYSTEM is None:
        _SYSTEM = "en"
        try:
            from Foundation import NSLocale
            known = available()
            for tag in NSLocale.preferredLanguages() or []:
                # Tags arrive as "uk-UA", "pt-BR", "zh-Hans-CN". What sits in front of
                # the first dash is the language, which is what we translate at.
                code = str(tag).split("-")[0]
                if code in known:
                    _SYSTEM = code
                    break
        except Exception:
            pass    # no AppKit around (tests, build tooling): English is a fine answer
    return _SYSTEM


def language():
    """The language in force: the override, then the setting, then whatever macOS is."""
    forced = os.environ.get("VEXFLOW_UI_LANG")
    code = forced or settings.get("ui_language") or _system_language()
    return code if code in available() else "en"


_LISTENERS = []


def on_language_change(callback):
    """Register something that has to redraw itself when the language changes.

    A registry rather than a direct call into the app module, because the app runs as
    vexflow_app.py and is therefore called __main__ inside its own process. A window
    doing `import vexflow_app` gets a SECOND, freshly executed copy of that module,
    whose delegate is None — so the redraw was silently skipped and the language only
    appeared to change on the next restart. That was the 1.2 bug. Nothing here depends
    on what the app module happens to be called.
    """
    if callback not in _LISTENERS:
        _LISTENERS.append(callback)


def set_language(code):
    """Store the choice, then tell everything already on screen to draw itself again."""
    settings.set("ui_language", code)
    for callback in list(_LISTENERS):
        try:
            callback()
        except Exception:
            pass    # a failed redraw must not take dictation down with it


def _table(code):
    if code not in _TABLES:
        try:
            _TABLES[code] = importlib.import_module("i18n.%s" % code).TABLE
        except Exception:
            # A table with a syntax error in it would otherwise take the whole app down
            # at the first label it draws. English keeps dictation working.
            _TABLES[code] = {}
    return _TABLES[code]


def t(text):
    """The current language's version of an English source string."""
    code = language()
    if code == "en":
        return text
    return _table(code).get(text, text)


def entries(choices):
    """Translate the display half of a (title, value) list, separators intact."""
    return [None if c is None else (t(c[0]), c[1]) for c in choices]


def names(mapping):
    """Translate the values of a value -> display-name map."""
    return {value: t(title) for value, title in mapping.items()}
