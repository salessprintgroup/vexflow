"""One narrow listen-only CGEventTap, instead of two pynput listeners.

Why not pynput (this replaced it after a profiling pass):

* pynput's masks routed EVERY system event through Python: the keyboard tap saw all
  keyDown/keyUp events (plus a CGEventKeyboardGetUnicodeString call on each), and the
  mouse tap saw every move, drag and scroll. On a small machine that is constant
  background CPU and GIL pressure — the whole system felt slower.
* pynput's stop() is a silent no-op if the listener has not reached run() yet, so a
  double restart (wake and watchdog back to back) leaked live taps permanently.
* pynput does not handle kCGEventTapDisabledByTimeout, so the tap went deaf until
  something recreated it.

Here the mask is only FlagsChanged (push-to-talk and toggle are modifiers) plus
OtherMouseDown. Typing and mouse movement are never delivered to this process at all;
WindowServer filters them. A timeout disable is repaired inside the callback, and the
watchdog only has to check CGEventTapIsEnabled — nothing is ever recreated.

A hotkey is one modifier ("cmd_r") or a chord ("ctrl_l+alt_l"). Chords matter when
another app already owns the obvious single keys, or when every free single modifier
is one you press while typing — holding Left Option alone would open the microphone on
every option-click.
"""
import sys

import Quartz

# Device-specific CGEventFlags bits (IOKit NX_DEVICE…KEYMASK). The device bit tells
# left from right, which the shared kCGEventFlagMaskCommand cannot: without it,
# "both Cmd held, right one released" would look like a release of neither.
_MOD_BITS = {
    "cmd_r":   0x0010,
    "cmd_l":   0x0008,
    "alt_r":   0x0040,
    "alt_l":   0x0020,
    "ctrl_r":  0x2000,
    "ctrl_l":  0x0001,
    "shift_r": 0x0004,
    "shift_l": 0x0002,
}

# Generic (side-agnostic) masks, used only for the "is the user still physically
# holding it" check, where being conservative is the safe direction.
_GENERIC_BITS = {
    "cmd": Quartz.kCGEventFlagMaskCommand,
    "alt": Quartz.kCGEventFlagMaskAlternate,
    "ctrl": Quartz.kCGEventFlagMaskControl,
    "shift": Quartz.kCGEventFlagMaskShift,
}


def parse(spec):
    """'ctrl_l+alt_l' -> (device mask, generic mask). Empty spec -> (0, 0).

    Raises ValueError on an unknown key so a typo in settings fails loudly at bind
    time rather than becoming a hotkey that silently never fires.
    """
    device = generic = 0
    for part in (spec or "").split("+"):
        part = part.strip()
        if not part:
            continue
        if part not in _MOD_BITS:
            raise ValueError(
                f"unknown modifier {part!r}; supported: {', '.join(sorted(_MOD_BITS))}")
        device |= _MOD_BITS[part]
        generic |= _GENERIC_BITS[part.rsplit("_", 1)[0]]
    return device, generic


class HotkeyTap:
    """Push-to-talk (hold) plus toggle (tap) plus a mouse toggle, through one tap.

    start() attaches the tap to the run loop of the CURRENT thread: in the menu bar app
    that is main before NSApp.run() (kCFRunLoopCommonModes, so it keeps working while a
    menu is open); in the CLI it is main with a manual CFRunLoopRunInMode spin.
    Callbacks fire on that thread and are marshalled into asyncio by the caller.

    Detection is purely by flag mask rather than by keycode. Holding the chord and then
    pressing an unrelated modifier leaves the mask satisfied, so no spurious start or
    stop — which is exactly what keycode matching got wrong.
    """

    def __init__(self, ptt_key, toggle_key, on_ptt_down, on_ptt_up, on_toggle,
                 mouse_toggle=False):
        self._ptt_mask, self._ptt_generic = parse(ptt_key)
        if not self._ptt_mask:
            raise ValueError("push-to-talk hotkey is empty")
        try:
            self._tog_mask, _ = parse(toggle_key)
        except ValueError as e:
            print(f"hotkeys: {e} — keyboard toggle disabled", file=sys.stderr, flush=True)
            self._tog_mask = 0
        self._on_ptt_down = on_ptt_down
        self._on_ptt_up = on_ptt_up
        self._on_toggle = on_toggle
        self._mouse_toggle = mouse_toggle
        self._tap = None
        self._source = None
        self._runloop = None
        self._cb = None          # keep the reference or pyobjc GCs the callback and crashes
        self._ptt_held = False
        self._tog_held = False

    def start(self):
        mask = Quartz.CGEventMaskBit(Quartz.kCGEventFlagsChanged)
        if self._mouse_toggle:
            mask |= Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseDown)

        def _callback(_proxy, etype, event, _refcon):
            # macOS disabled the tap (slow callback or user input) -> turn it back on.
            if etype in (Quartz.kCGEventTapDisabledByTimeout,
                         Quartz.kCGEventTapDisabledByUserInput):
                if self._tap is not None:
                    Quartz.CGEventTapEnable(self._tap, True)
                return event
            try:
                if etype == Quartz.kCGEventFlagsChanged:
                    flags = Quartz.CGEventGetFlags(event)
                    held = (flags & self._ptt_mask) == self._ptt_mask
                    if held and not self._ptt_held:
                        self._ptt_held = True
                        self._on_ptt_down()
                    elif not held and self._ptt_held:
                        self._ptt_held = False
                        self._on_ptt_up()
                    if self._tog_mask:
                        # Fire on the transition into "fully held", so a chord toggles
                        # once rather than once per key that completes it.
                        tog = (flags & self._tog_mask) == self._tog_mask
                        if tog and not self._tog_held:
                            self._on_toggle()
                        self._tog_held = tog
                elif etype == Quartz.kCGEventOtherMouseDown:
                    self._on_toggle()
            except Exception:
                pass  # an exception out of the callback must not kill the tap
            return event

        self._cb = _callback
        self._tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap, Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionListenOnly, mask, self._cb, None)
        if self._tap is None:
            return False   # no Accessibility permission
        self._source = Quartz.CFMachPortCreateRunLoopSource(None, self._tap, 0)
        self._runloop = Quartz.CFRunLoopGetCurrent()
        Quartz.CFRunLoopAddSource(self._runloop, self._source,
                                  Quartz.kCFRunLoopCommonModes)
        Quartz.CGEventTapEnable(self._tap, True)
        return True

    def ptt_physically_held(self):
        """Is the push-to-talk hotkey held right now, asked of the HID state rather
        than of our own bookkeeping.

        Used to spot a zombie recording after a dead tap swallowed the release. The
        check is side-agnostic on purpose: a false "still held" only delays cleanup by
        one watchdog tick, while a false "released" would cut a recording the user is
        in the middle of.
        """
        state = Quartz.CGEventSourceFlagsState(Quartz.kCGEventSourceStateHIDSystemState)
        return (state & self._ptt_generic) == self._ptt_generic

    def heal(self):
        """Watchdog and wake: if the system disabled the tap, enable it. True if repaired."""
        if self._tap is not None and not Quartz.CGEventTapIsEnabled(self._tap):
            Quartz.CGEventTapEnable(self._tap, True)
            return True
        return False

    def reset_ptt(self):
        """Clear a stuck push-to-talk state (release lost while the tap was dead)."""
        self._ptt_held = False

    def stop(self):
        if self._source is not None and self._runloop is not None:
            Quartz.CFRunLoopRemoveSource(self._runloop, self._source,
                                         Quartz.kCFRunLoopCommonModes)
            self._source = None
        if self._tap is not None:
            Quartz.CGEventTapEnable(self._tap, False)
            self._tap = None
        self._cb = None
