"""First-run window: the macOS permissions Vexflow cannot work without.

The three steps here are the ones with no alternative: without the microphone there is
no audio, without accessibility there is no hotkey and no paste, and without a restart
macOS does not apply the accessibility grant to the running process.

The window does not ask for the API key — a secret does not belong in a wizard — but
it does not pretend the job is finished without one either. With the permissions done
and no key stored, the last button hands over to Settings instead of closing.

The window polls, so granting something in System Settings ticks a step off here
without anyone having to press a refresh button.
"""
import os

import AppKit
import objc
from Foundation import NSObject, NSMakeRect

import config
import macos
import settings
import strings
import widgets as w
from strings import t

WIDTH, HEIGHT = 680, 456
PAD = 24
ROW_H = 72
STEP_X = PAD + 30            # text column, right of the step marker
STEP_BTN_W = 150             # wide enough for "Universellen Zugriff erlauben"-length verbs

# (key, title, explanation) in the order they have to be done.
STEPS = [
    ("mic", "Allow microphone access",
     "So Vexflow can hear you."),
    ("ax", "Allow accessibility access",
     "So Vexflow can see the hotkey and paste the text."),
    ("restart", "Restart Vexflow",
     "macOS applies the accessibility grant only at launch."),
]


class WelcomeWindow(NSObject):
    """Owns the window. Created once, reused if reopened from the menu."""

    def initWithApp_(self, delegate):
        self = objc.super(WelcomeWindow, self).init()
        if self is None:
            return None
        self.app_delegate = delegate
        self.engine = getattr(delegate, "engine", None)
        self.window = None
        self.timer = None
        return self

    # --- lifecycle ----------------------------------------------------------

    @objc.python_method
    def show(self):
        if self.window is None:
            self._build()
        self.refresh()
        macos.become_foreground()
        self.window.center()
        self.window.makeKeyAndOrderFront_(None)
        if self.timer is None:
            self.timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1.5, self, b"tick:", None, True)

    def windowWillClose_(self, _notification):
        if self.timer is not None:
            self.timer.invalidate()
            self.timer = None
        macos.become_background()

    def tick_(self, _timer):
        self.refresh()

    @objc.python_method
    def _build(self):
        style = AppKit.NSWindowStyleMaskTitled | AppKit.NSWindowStyleMaskClosable
        self.window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(0, 0, WIDTH, HEIGHT), style, AppKit.NSBackingStoreBuffered, False)
        self.window.setTitle_(t("Welcome to ") + config.APP_NAME)
        self.window.setReleasedWhenClosed_(False)
        self.window.setDelegate_(self)
        v = self.window.contentView()

        y = HEIGHT - 82
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "assets", "Vexflow.icns")
        image = AppKit.NSImage.alloc().initWithContentsOfFile_(icon_path)
        if image is not None:
            iv = AppKit.NSImageView.alloc().initWithFrame_(NSMakeRect(PAD, y - 6, 56, 56))
            iv.setImage_(image)
            iv.setImageScaling_(AppKit.NSImageScaleProportionallyUpOrDown)
            v.addSubview_(iv)

        v.addSubview_(w.label(t("Set up ") + config.APP_NAME, PAD + 70, y + 32, 400,
                              bold=True, size=17))
        v.addSubview_(w.note(
            t("macOS needs to grant two permissions before dictation can work. "
              "This takes about a minute."),
            PAD + 70, y - 4, WIDTH - PAD - 90, 34, size=12))
        y -= 42

        # First thing on the way in, before the permissions: somebody who cannot read
        # this window should not have to finish it before finding the way out. The
        # language names stay in their own language for the same reason.
        ui_lang_entries, _ = w.titled_entries(config.UI_LANGUAGES)
        v.addSubview_(w.label(t("Interface language"), PAD, y + 3, 150))
        self.ui_lang_popup = w.popup(ui_lang_entries, PAD + 160, y - 2, 170, self,
                                     b"changeUILanguage:")
        v.addSubview_(self.ui_lang_popup)
        y -= 34

        self.progress = w.progress_bar(PAD, y, WIDTH - PAD * 2)
        self.progress.setMaxValue_(float(len(STEPS)))
        v.addSubview_(self.progress)
        self.progress_label = w.label("", PAD, y - 20, WIDTH - PAD * 2, size=11,
                                      color=w.SECONDARY)
        v.addSubview_(self.progress_label)
        y -= 44

        self.rows = {}
        for number, (ident, title, subtitle) in enumerate(STEPS, start=1):
            y = self._step(v, y, number, ident, title, subtitle)

        v.addSubview_(w.separator(0, 50, WIDTH))
        v.addSubview_(w.linked_note(
            f"© {config.COPYRIGHT_YEAR} ", config.VENDOR_LEGAL, config.VENDOR_URL, "",
            PAD, 20, WIDTH - PAD - 140))
        self.close_button = w.button(t("Close"), WIDTH - PAD - 110, 16, 110, self,
                                     b"closeWindow:", default=True, small=False)
        v.addSubview_(self.close_button)

    @objc.python_method
    def _step(self, view, y, number, ident, title, subtitle):
        marker = w.label(f"{number}", PAD, y + 2, 20, bold=True, color=w.SECONDARY)
        view.addSubview_(marker)
        view.addSubview_(w.label(t(title), STEP_X, y + 2, 320, bold=True, size=12))
        view.addSubview_(w.note(t(subtitle), STEP_X, y - 16, 340, 16))
        status = w.label("", STEP_X, y - 34, 320, size=11, color=w.SECONDARY)
        view.addSubview_(status)

        action = {"mic": b"allowMic:", "ax": b"allowAx:"}.get(ident, b"restartApp:")
        title_for = t({"mic": "Allow", "ax": "Allow"}.get(ident, "Restart"))
        button = w.button(title_for, WIDTH - PAD - STEP_BTN_W, y, STEP_BTN_W,
                          self, action)
        view.addSubview_(button)

        self.rows[ident] = {"marker": marker, "status": status, "button": button,
                            "number": str(number)}
        return y - ROW_H

    # --- state --------------------------------------------------------------

    @objc.python_method
    def _states(self):
        mic = macos.microphone_status()
        # "unknown" means the AVFoundation bindings are absent, not that access was
        # refused; macOS asks on first use, so do not block the user on it.
        ax_ok = macos.has_accessibility()
        return {
            "mic": mic in ("granted", "unknown"),
            "ax": ax_ok,
            # Only meaningful once accessibility is granted, and already satisfied if
            # the running process picked the grant up when it launched.
            "restart": ax_ok and (self.engine is None or self.engine.hotkeys_live),
        }

    @objc.python_method
    def refresh(self):
        if self.window is None:
            return
        w.select_value(self.ui_lang_popup, config.UI_LANGUAGES, strings.language())
        state = self._states()
        done = sum(state.values())
        self.progress.setDoubleValue_(float(done))

        # Point at the first thing still to do, not at how many are finished — with
        # step 1 outstanding and 2 and 3 already true, "Step 3 of 3" is a lie.
        pending = [i for i, (ident, _, _) in enumerate(STEPS, start=1)
                   if not state[ident]]
        self.progress_label.setStringValue_(
            t("Step {} of {}").format(pending[0], len(STEPS)) if pending
            else t("Permissions are set."))

        mic_text = t({"granted": "Granted", "unknown": "Requested on first use",
                      "denied": "Denied — turn it on in System Settings",
                      "undetermined": "Not requested yet"}[macos.microphone_status()])
        self._row("mic", state["mic"], mic_text)
        self._row("ax", state["ax"], t("Granted") if state["ax"] else t("Not granted"))
        self._row("restart", state["restart"],
                  t("Hotkeys are live") if state["restart"]
                  else t("Restart to activate the hotkey") if state["ax"]
                  else t("Finish step 2 first"))
        self.rows["restart"]["button"].setEnabled_(state["ax"])

        if pending:
            return
        # Permissions are done. Dictation still needs a Deepgram key, so send the user
        # to the one place it can be entered rather than closing on a half-set-up app.
        # Through the engine where there is one: this runs on a timer, and asking the
        # Keychain means spawning `security` every time round.
        if (self.engine.has_key if self.engine is not None
                else bool(macos.get_api_key())):
            self._set_final_button(t("Done"), b"closeWindow:")
        else:
            self._set_final_button(t("Add your API key"), b"openSettings:")

    @objc.python_method
    def _set_final_button(self, title, action):
        if self.close_button.title() == title:
            return
        self.close_button.setTitle_(title)
        self.close_button.setAction_(action)
        # The frame was sized for "Close", which clipped "Add your API key" to
        # "Add your". Fit the title and keep the right edge where it was.
        self.close_button.sizeToFit()
        width = max(110, self.close_button.frame().size.width + 20)
        self.close_button.setFrame_(NSMakeRect(WIDTH - PAD - width, 16, width, 32))

    @objc.python_method
    def _row(self, ident, ok, text):
        row = self.rows[ident]
        row["status"].setStringValue_(text)
        row["status"].setTextColor_(w.SECONDARY if ok else w.ALERT)
        row["marker"].setStringValue_("✓" if ok else row["number"])
        row["button"].setHidden_(ok)

    # --- actions ------------------------------------------------------------

    def allowMic_(self, _sender):
        if macos.microphone_status() == "undetermined":
            macos.request_microphone()
        else:
            macos.open_settings_pane("microphone")

    def allowAx_(self, _sender):
        macos.prompt_accessibility()
        macos.open_settings_pane("accessibility")

    def restartApp_(self, _sender):
        macos.restart_app()

    def changeUILanguage_(self, sender):
        value = w.selected_value(sender, config.UI_LANGUAGES)
        if not value or value == strings.language():
            return
        strings.set_language(value)
        # Redraws immediately rather than waiting for the restart in step 3: somebody
        # who cannot read this window needs it to change while they are looking at it.

    def openSettings_(self, _sender):
        self.window.performClose_(None)
        if self.app_delegate is not None:
            self.app_delegate.show_settings()

    def closeWindow_(self, _sender):
        self.window.performClose_(None)

    @objc.python_method
    def rebuild(self):
        """Draw the window again in the current language. See ui.SettingsWindow."""
        if self.window is None:
            return
        visible = self.window.isVisible()
        origin = self.window.frame().origin
        self.window.setDelegate_(None)
        self.window.orderOut_(None)
        self.window = None
        self.rows = {}
        self._build()
        self.refresh()
        if visible:
            self.window.setFrameOrigin_(origin)
            self.window.makeKeyAndOrderFront_(None)


def needs_setup():
    """Open by itself when Vexflow cannot dictate yet — no accessibility, or no key.

    The key belongs here because of what a fresh install actually looks like: the
    permissions can already be granted (macOS attributes them to the interpreter, which
    another build may have registered), and then the guide never appeared at all and
    the only sign of a missing key was an orange icon in the menu bar.
    """
    return not macos.has_accessibility() or not macos.get_api_key()
