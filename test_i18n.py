"""Check the interface translations before a build ships them.

    ./.venv/bin/python test_i18n.py            every language
    ./.venv/bin/python test_i18n.py de fr      just these

Three things go wrong with a table of strings, and reading the file shows none of them:

  * a key nothing asks for any more — a rename left it behind, and the translation
    quietly stopped being used;
  * a key that exists in the source but not in the table — harmless, English shows
    through, but you want to know how much of the interface that is;
  * a translation too long for the control it goes into, which is how a button ends up
    reading "Neu star…".

The third one is the reason this file needs AppKit. It builds every window in every
language and asks each control whether the text it was handed fits the box it was
handed, which is a question only the text system can answer honestly — counting
characters gets it wrong, because glyph widths differ and so do fonts.
"""
import ast
import glob
import os
import sys

os.environ.setdefault("VEXFLOW_UI_LANG", "en")

import AppKit                                                # noqa: E402

import config                                                # noqa: E402
import strings                                               # noqa: E402
import widgets as w                                          # noqa: E402

# Reported, but not failed on: macOS truncates a pop-up row with an ellipsis and stays
# usable, where a clipped button label is simply unreadable.
SOFT = (AppKit.NSPopUpButton,)


# --- what the interface can ask for -----------------------------------------

def _calls_t(func):
    return ((isinstance(func, ast.Name) and func.id == "t")
            or (isinstance(func, ast.Attribute) and func.attr == "t"))


def source_strings():
    """Every English string the interface can hand to t().

    Plenty of translated text never appears as a literal argument to t(): tab titles
    and setup steps are looped over as variables, the menu-bar states come out of
    dictionaries, and the display halves of LANGUAGES and HOTKEY_CHOICES go through
    strings.entries(). So this takes every string constant in every source file, which
    is deliberately too generous — the set decides what counts as an orphan, and a set
    that is too wide misses one, while a set that is too narrow invents one.
    """
    found = set()
    for path in sorted(glob.glob("*.py")):
        if os.path.basename(path).startswith("test_"):
            continue
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                found.add(node.value)
    return found


def table(code):
    """One language's table, or {} for English, which is the keys themselves."""
    if code == "en":
        return {}
    path = os.path.join("i18n", "%s.py" % code)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), path)
    for node in tree.body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "TABLE":
            return ast.literal_eval(node.value)
    return None


# --- does the text fit the box ----------------------------------------------

def _overflow(view):
    """(description, overshoot in points) for a control whose text will not fit."""
    frame = view.frame()
    if isinstance(view, AppKit.NSTextField):
        text = str(view.stringValue())
        if not text:
            return None
        if not view.usesSingleLineMode():
            # A wrapping note is clipped vertically, not horizontally: the words go on
            # to the next line and the last line falls out of the bottom of the frame.
            size = view.font().pointSize() if view.font() else 11
            need = w._text_height(text, frame.size.width, size)
            over = need - frame.size.height
            return ("note %.0fx%.0f: %r" % (frame.size.width, frame.size.height, text),
                    over) if over > 1 else None
        need = view.attributedStringValue().size().width
    elif isinstance(view, (AppKit.NSButton, AppKit.NSPopUpButton)):
        text = str(view.title())
        if not text:
            return None
        need = view.fittingSize().width
    else:
        return None
    over = need - frame.size.width
    if over <= 1:
        return None
    kind = type(view).__name__.replace("NS", "").lower()
    return "%s %.0fpt: %r" % (kind, frame.size.width, text), over


def _walk(view, out):
    for child in view.subviews():
        hit = _overflow(child)
        if hit is not None:
            out.append((child, hit))
        _walk(child, out)
    # A tab view keeps its pages outside the subview tree until they are selected.
    if isinstance(view, AppKit.NSTabView):
        for item in view.tabViewItems():
            if item.view() is not None:
                _walk(item.view(), out)


def clipped(code):
    """Controls in either window whose text does not fit, for one language."""
    os.environ["VEXFLOW_UI_LANG"] = code
    import onboarding
    import ui
    out = []
    settings_window = ui.SettingsWindow.alloc().initWithEngine_(None)
    settings_window._build()
    _walk(settings_window.window.contentView(), out)
    welcome = onboarding.WelcomeWindow.alloc().initWithApp_(None)
    welcome._build()
    _walk(welcome.window.contentView(), out)
    return out


# --- report ------------------------------------------------------------------

def main(argv):
    app = AppKit.NSApplication.sharedApplication()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)

    source = source_strings()
    codes = argv[1:] or strings.available()

    # What counts as "the interface", for coverage: every key any table has an entry
    # for and the source still asks for. Self-calibrating — a new language is measured
    # against the languages that are already finished, not against a number I picked.
    expected = set()
    for code in strings.available():
        expected |= set(table(code) or {})
    expected &= source

    failures = 0
    for code in codes:
        rows = table(code)
        if rows is None:
            print("%s  NO TABLE (i18n/%s.py is missing)" % (code, code))
            failures += 1
            continue

        orphans = sorted(k for k in rows if k not in source)
        missing = sorted(expected - set(rows)) if code != "en" else []
        bad = clipped(code)
        hard = [b for b in bad if not isinstance(b[0], SOFT)]

        status = "ok" if not orphans and not hard else "FAIL"
        print("%-4s %-5s %3d/%d translated, %d orphaned, %d clipped"
              % (code, status, len(expected) - len(missing), len(expected),
                 len(orphans), len(bad)))
        for key in orphans:
            print("       orphan:  %r" % key)
        for key in missing:
            print("       missing: %r" % key)
        for view, (what, over) in bad:
            mark = "soft" if isinstance(view, SOFT) else "CLIP"
            print("       %s +%.0fpt  %s" % (mark, over, what))
        if status == "FAIL":
            failures += 1

    print()
    print("%d language(s) checked, %d with problems" % (len(codes), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
