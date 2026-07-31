"""Vexflow menu bar app — the normal way to run it.

The status item is created immediately in main(), before app.run(), rather than from
applicationDidFinishLaunching: under launchd that callback is not guaranteed to
arrive. The activation policy is set explicitly to Accessory so the icon does not
depend on Info.plist either.
"""
import os
import traceback

import AppKit
import objc

import billing
import config
import macos
import settings
import strings
from engine import Engine
from strings import t
from logutil import log

# Text fallbacks survive a missing assets folder: no icons means a text badge rather
# than a crash. The no-key state is always text, because it is a problem that should
# be loud.
IDLE, REC, PAUSED, NOKEY = "VF", "VF ●", "VF ||", "VF (!)"

# What the menu says while the key is anything other than proven good.
KEY_STATUS = {
    "missing": "No Deepgram key — open Settings",
    "checking": "Checking your Deepgram key…",
    "invalid": "Deepgram rejected your key — open Settings",
    "unreachable": "Can't reach Deepgram — check your connection",
}   # translated where they are shown, so the keys stay greppable
# The same for a cleanup vendor, appended to its heading in the Cleanup submenu.
# A valid key adds nothing: the working case should be silent.
KEY_NOTE = {
    "missing": " — no key",
    "checking": " — checking the key…",
    "invalid": " — key rejected",
    "unreachable": " — could not check the key",
}
MB_POINTS = 18.0          # menu bar glyph height, in points


def _load_menubar_icons():
    """{'idle': NSImage, 'rec': NSImage}, or None if the assets are missing.

    Both densities go into one NSImage as explicit representations: an NSImage loaded
    from a file does not pick up its @2x sibling (only imageNamed: inside a bundle
    does that), and without @2x the glyph is blurry on a Retina display.
    """
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    icons = {}
    # idle is a template so macOS tints it for the menu bar theme; rec and nokey carry
    # their own red and must not be recoloured.
    for kind, template in (("idle", True), ("rec", False), ("warn", False)):
        img = AppKit.NSImage.alloc().initWithSize_((MB_POINTS, MB_POINTS))
        for suffix in ("", "@2x"):
            path = os.path.join(base, f"menubar-{kind}{suffix}.png")
            rep = AppKit.NSImageRep.imageRepWithContentsOfFile_(path)
            if rep is None:
                return None
            rep.setSize_((MB_POINTS, MB_POINTS))   # points, not pixels — this is what makes @2x work
            img.addRepresentation_(rep)
        img.setTemplate_(template)   # idle is recoloured by macOS; rec stays red
        icons[kind] = img
    return icons


_ICONS = None
_ENGINE = None
_DELEGATE = None      # keep a reference so the delegate is not garbage collected


def _balance_line():
    """What the Balance entry says, or None when it should not be shown at all."""
    state, text, amount = billing.current()
    if state == "missing":
        return None          # no billing key: not a problem, just not a feature in use
    if state == "ok":
        return t("Balance: {} — running low" if billing.is_low(state, amount)
                 else "Balance: {}").format(text)
    return t({
        "checking": "Balance: checking…",
        "denied": "Balance key rejected — open Settings",
        "unreachable": "Balance: can't reach Deepgram",
    }[state])


def _hotkey_summary():
    names = strings.names(config.HOTKEY_NAMES)
    ptt = settings.get("ptt_key")
    parts = [t("Hold ") + names.get(ptt, ptt)]
    toggle = settings.get("toggle_key")
    if toggle:
        parts.append(t("tap ") + names.get(toggle, toggle))
    if settings.get("mouse_toggle"):
        parts.append(t("middle mouse button"))
    return "  ·  ".join(parts)


def _install_main_menu():
    """Give the process an application menu and an Edit menu.

    A menu bar app has no visible menu bar, so it is tempting to skip this. But key
    equivalents are dispatched THROUGH the main menu: with no Edit menu there is
    nothing that claims Cmd-V, and paste silently does nothing in every text field we
    own — right-click still works, which makes it look like a field bug rather than a
    missing menu. The items also give the standard editing shortcuts to the Settings
    and Welcome windows for free.

    The menu's own title is not what names the app — that comes from the bundle, and
    is handled by macos.set_app_identity().
    """
    main = AppKit.NSMenu.alloc().init()

    app_item = AppKit.NSMenuItem.alloc().init()
    main.addItem_(app_item)
    app_menu = AppKit.NSMenu.alloc().initWithTitle_(config.APP_NAME)
    # No target: the action travels the responder chain to the app delegate, which is
    # set after this menu is built. The standard panel is not used directly because it
    # would carry no licence line.
    app_menu.addItemWithTitle_action_keyEquivalent_(
        t("About ") + config.APP_NAME, b"showAbout:", "")
    app_menu.addItem_(AppKit.NSMenuItem.separatorItem())
    app_menu.addItemWithTitle_action_keyEquivalent_(
        t("Hide ") + config.APP_NAME, b"hide:", "h")
    app_menu.addItem_(AppKit.NSMenuItem.separatorItem())
    app_menu.addItemWithTitle_action_keyEquivalent_(
        t("Quit ") + config.APP_NAME, b"terminate:", "q")
    app_item.setSubmenu_(app_menu)

    edit_item = AppKit.NSMenuItem.alloc().init()
    main.addItem_(edit_item)
    edit_menu = AppKit.NSMenu.alloc().initWithTitle_(t("Edit"))
    for title, selector, key in (
        ("Undo", b"undo:", "z"),
        ("Redo", b"redo:", "Z"),
        (None, None, None),
        ("Cut", b"cut:", "x"),
        ("Copy", b"copy:", "c"),
        ("Paste", b"paste:", "v"),
        ("Select All", b"selectAll:", "a"),
    ):
        if title is None:
            edit_menu.addItem_(AppKit.NSMenuItem.separatorItem())
        else:
            edit_menu.addItemWithTitle_action_keyEquivalent_(t(title), selector, key)
    edit_item.setSubmenu_(edit_menu)

    AppKit.NSApp().setMainMenu_(main)


class Delegate(AppKit.NSObject):
    """Menu bar controller.

    Every helper that takes arguments is marked @objc.python_method: pyobjc turns
    plain methods into Objective-C selectors, and a selector's arity is derived from
    its name, so an unmarked helper fails at class-creation time.
    """

    @objc.python_method
    def setup(self):
        bar = AppKit.NSStatusBar.systemStatusBar()
        self.item = bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength)
        self.item.setAutosaveName_("Vexflow")   # remember the position after a Cmd-drag
        self._set_button(self.item.button(), "idle")
        self.settings_window = None
        self.welcome_window = None
        self.engine = _ENGINE
        self._build_menu()

        self.timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.3, self, b"refresh:", None, True)
        # Self-heal: cheap (CGEventTapIsEnabled plus a re-enable when needed), nothing
        # is ever recreated.
        self.watchdog = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            120.0, self, b"watchdog:", None, True)
        AppKit.NSWorkspace.sharedWorkspace().notificationCenter().addObserver_selector_name_object_(
            self, b"onWake:", AppKit.NSWorkspaceDidWakeNotification, None)
        log(f"app: status item={self.item is not None}, "
            f"button={self.item.button() is not None}, visible={self.item.isVisible()}")

    # --- menu ---------------------------------------------------------------

    @objc.python_method
    def _mi(self, title, sel, key=""):
        it = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, sel, key)
        if sel is not None:
            it.setTarget_(self)
        return it

    @objc.python_method
    def _build_menu(self):
        menu = AppKit.NSMenu.alloc().init()

        self.status_mi = self._mi(t("Ready"), None)
        menu.addItem_(self.status_mi)

        # Always built, hidden until there is a billing key — so pasting one into
        # Settings makes the entry appear without a restart.
        self.balance_mi = self._mi(t("Balance: …"), None)
        menu.addItem_(self.balance_mi)

        self.hint_mi = self._mi(_hotkey_summary(), None)
        menu.addItem_(self.hint_mi)

        menu.addItem_(AppKit.NSMenuItem.separatorItem())

        # Emergency stop, works even if the hotkey tap has died.
        self.stop_mi = self._mi(t("Stop recording"), b"stopRecording:")
        self.stop_mi.setHidden_(True)
        menu.addItem_(self.stop_mi)
        self.pause_mi = self._mi(t("Pause"), b"togglePause:")
        menu.addItem_(self.pause_mi)

        menu.addItem_(AppKit.NSMenuItem.separatorItem())

        # Language submenu.
        self.lang_items = []
        lang_parent = self._mi(t("Language"), None)
        lang_menu = AppKit.NSMenu.alloc().init()
        for label, code in strings.entries(config.LANGUAGES):
            it = self._mi(label, b"setLanguage:")
            it.setRepresentedObject_(code)
            lang_menu.addItem_(it)
            self.lang_items.append((it, code))
        lang_parent.setSubmenu_(lang_menu)
        menu.addItem_(lang_parent)

        # Cleanup submenu: on/off plus every provider and model in one place.
        self.model_items = []
        self.provider_headers = []
        self.clean_mi = self._mi(t("Clean up transcripts"), b"toggleClean:")
        clean_parent = self._mi(t("LLM Cleanup"), None)
        clean_menu = AppKit.NSMenu.alloc().init()
        # Manual enabling. AppKit's automatic menu validation re-enables every item
        # with a working target each time the menu opens, so setEnabled_(False) on a
        # model whose vendor has no key never survived — it stayed selectable, and
        # picking it left cleanup quietly doing nothing.
        clean_menu.setAutoenablesItems_(False)
        clean_menu.addItem_(self.clean_mi)
        for provider, spec in config.CLEAN_PROVIDERS.items():
            clean_menu.addItem_(AppKit.NSMenuItem.separatorItem())
            header = self._mi(spec["label"], None)
            header.setEnabled_(False)   # a caption, not a command
            clean_menu.addItem_(header)
            self.provider_headers.append((header, provider, spec["label"]))
            for label, model_id in spec["models"]:
                it = self._mi("   " + t(label), b"setModel:")
                it.setRepresentedObject_(f"{provider}/{model_id}")
                clean_menu.addItem_(it)
                self.model_items.append((it, provider, model_id))
        clean_parent.setSubmenu_(clean_menu)
        menu.addItem_(clean_parent)

        menu.addItem_(AppKit.NSMenuItem.separatorItem())
        menu.addItem_(self._mi(t("Setup Guide…"), b"openWelcome:"))
        menu.addItem_(self._mi(t("Settings…"), b"openSettings:", ","))
        # Hidden while logging is off, which is the default: there is no file, and an
        # entry that would create an empty one is worse than no entry.
        self.log_mi = self._mi(t("Open log"), b"openLog:")
        menu.addItem_(self.log_mi)

        menu.addItem_(AppKit.NSMenuItem.separatorItem())
        menu.addItem_(self._mi(t("Vexflow on GitHub"), b"openHomepage:"))
        menu.addItem_(self._mi(t("Built by ") + config.VENDOR_NAME, b"openVendor:"))

        menu.addItem_(AppKit.NSMenuItem.separatorItem())
        menu.addItem_(self._mi(t("Quit Vexflow"), b"quit:", "q"))
        self.item.setMenu_(menu)

    # --- rendering ----------------------------------------------------------

    @objc.python_method
    def _set_title(self, obj, text, cache_attr):
        """setTitle_ only when it changed — do not hammer AppKit every 0.3s."""
        if getattr(self, cache_attr, None) != text:
            setattr(self, cache_attr, text)
            obj.setTitle_(text)

    @objc.python_method
    def _set_button(self, btn, kind):
        """Menu bar glyph: idle / rec / paused / nokey. Also only on change."""
        if getattr(self, "_c_btn", None) == kind:
            return
        self._c_btn = kind
        # paused reuses the idle glyph at reduced opacity; every other state has its own.
        asset = {"idle": "idle", "paused": "idle", "rec": "rec", "warn": "warn"}[kind]
        img = _ICONS.get(asset) if _ICONS else None
        if img is None:
            # Only when the assets are missing entirely — a text badge beats no icon.
            btn.setImage_(None)
            btn.setAlphaValue_(1.0)
            btn.setTitle_({"idle": IDLE, "rec": REC,
                           "paused": PAUSED, "warn": NOKEY}[kind])
            return
        btn.setTitle_("")
        btn.setImage_(img)
        btn.setAlphaValue_(0.45 if kind == "paused" else 1.0)

    def refresh_(self, _timer):
        btn = self.item.button()
        balance = _balance_line()
        if getattr(self, "_c_bal_vis", None) != (balance is None):
            self._c_bal_vis = balance is None
            self.balance_mi.setHidden_(balance is None)
        if balance is not None:
            self._set_title(self.balance_mi, balance, "_c_bal")
        self._set_title(self.hint_mi, _hotkey_summary(), "_c_hint")

        if _ENGINE.state == "recording":
            self._set_button(btn, "rec")
            self._set_title(self.status_mi, t("Recording…"), "_c_st")
        elif _ENGINE.paused:
            self._set_button(btn, "paused")
            self._set_title(self.status_mi, t("Paused"), "_c_st")
        elif _ENGINE.key_state != "valid":
            # Orange sail until the key has actually been accepted by Deepgram. A key
            # that merely exists is not a key that works, and the difference used to
            # be invisible from the menu bar.
            self._set_button(btn, "warn")
            self._set_title(self.status_mi, t(KEY_STATUS[_ENGINE.key_state]), "_c_st")
        else:
            self._set_button(btn, "idle")
            self._set_title(self.status_mi, t(_ENGINE.notice) if _ENGINE.notice else t("Ready"),
                            "_c_st")

        self._set_title(self.pause_mi,
                        t("Resume") if _ENGINE.paused else t("Pause"), "_c_pause")

        enabled = bool(settings.get("clean_enabled"))
        self.clean_mi.setState_(1 if enabled else 0)
        provider, model = settings.provider(), settings.model()
        for header, p, label in self.provider_headers:
            # Say what is wrong with the key right above the models it disables.
            self._set_title(header,
                            label + t(KEY_NOTE.get(_ENGINE.llm_key_state.get(p), "")),
                            f"_c_hdr_{p}")
        for it, p, m in self.model_items:
            it.setState_(1 if (enabled and p == provider and m == model) else 0)
            # Selectable only when the key could actually be used. "unreachable" stays
            # selectable: that is a network the app happened to miss, not a bad key.
            it.setEnabled_(_ENGINE.llm_key_state.get(p) not in ("missing", "invalid"))
        for it, code in self.lang_items:
            it.setState_(1 if settings.get("language") == code else 0)

        recording = _ENGINE.state == "recording"
        if getattr(self, "_c_stop_vis", None) != recording:
            self._c_stop_vis = recording
            self.stop_mi.setHidden_(not recording)

        logging_on = bool(settings.get("logging_enabled"))
        if getattr(self, "_c_log_vis", None) != logging_on:
            self._c_log_vis = logging_on
            self.log_mi.setHidden_(not logging_on)

    # --- actions ------------------------------------------------------------

    def stopRecording_(self, _sender):
        _ENGINE.request_stop_active()

    def togglePause_(self, _sender):
        _ENGINE.paused = not _ENGINE.paused

    def toggleClean_(self, _sender):
        settings.set("clean_enabled", not settings.get("clean_enabled"))

    def setModel_(self, sender):
        provider, model_id = str(sender.representedObject()).split("/", 1)
        settings.set("clean_provider", provider)
        settings.set_model(provider, model_id)
        settings.set("clean_enabled", True)

    def setLanguage_(self, sender):
        settings.set("language", str(sender.representedObject()))

    def openSettings_(self, _sender):
        self.show_settings()

    def openWelcome_(self, _sender):
        self.show_welcome()

    @objc.python_method
    def show_welcome(self):
        try:
            if self.welcome_window is None:
                from onboarding import WelcomeWindow
                self.welcome_window = WelcomeWindow.alloc().initWithApp_(self)
            self.welcome_window.show()
        except Exception:
            # Through log(), not print_exc(): stderr goes wherever the launcher
            # pointed it, which with logging off is /dev/null.
            log(f"app: welcome window failed to open\n{traceback.format_exc()}", err=True)

    @objc.python_method
    def show_settings(self):
        try:
            if self.settings_window is None:
                from ui import SettingsWindow
                self.settings_window = SettingsWindow.alloc().initWithEngine_(_ENGINE)
            self.settings_window.show()
        except Exception:
            # A broken settings window must never take the dictation path down with it.
            log(f"app: settings window failed to open\n{traceback.format_exc()}", err=True)

    def openLog_(self, _sender):
        macos.open_path(config.LOG_FILE)

    def showAbout_(self, _sender):
        """The standard About panel, carrying the licence and the disclaimer.

        Name, version and copyright come from the bundle info dictionary, which
        macos.set_app_identity() has already corrected — without that they are the
        interpreter's.
        """
        notice = (f"{config.COPYRIGHT}. {config.LICENSE_NAME}. "
                  + t(config.LEGAL_NOTICE_BODY).format(app=config.APP_NAME,
                                                       vendor=config.VENDOR_LEGAL))
        credits = AppKit.NSAttributedString.alloc().initWithString_attributes_(
            notice, {AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(10)})
        AppKit.NSApp().orderFrontStandardAboutPanelWithOptions_(
            {AppKit.NSAboutPanelOptionCredits: credits})

    def openHomepage_(self, _sender):
        macos.open_url(config.HOMEPAGE)

    def openVendor_(self, _sender):
        macos.open_url(config.VENDOR_URL)

    def watchdog_(self, _timer):
        _ENGINE.heal()

    def onWake_(self, _notification):
        _ENGINE.heal()
        _ENGINE.reset_audio()   # a stale audio device cache causes -9986, seen in practice
        # The reset is marshalled onto the loop; if a recording is running it is
        # deferred (the engine logs that).
        log("app: wake — tap checked, PortAudio reset requested")

    def quit_(self, _sender):
        _ENGINE.stop(wait_session=2.0)   # let an active recording finish cleanly
        AppKit.NSApp().terminate_(None)


def main():
    global _ENGINE, _DELEGATE, _ICONS
    macos.set_app_identity()   # before AppKit reads the bundle and calls us "Python"
    if not macos.acquire_single_instance_lock():
        log("app: already running — exiting")
        return
    try:
        log("app: starting")
        try:
            _ICONS = _load_menubar_icons()
        except Exception:
            _ICONS = None       # a missing glyph is no reason not to start
        log(f"app: badge={'icon' if _ICONS else 'text (no assets)'}")

        _ENGINE = Engine()
        _ENGINE.start()
        log(f"app: deepgram key={'present' if _ENGINE.has_key else 'missing'}, "
            f"cleanup key={'present' if _ENGINE.has_any_llm_key else 'missing'}")

        billing.start_polling()

        app = AppKit.NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
        _install_main_menu()
        _DELEGATE = Delegate.alloc().init()
        _DELEGATE.setup()
        app.setDelegate_(_DELEGATE)

        # First run, or anything still missing: show the four setup steps rather than
        # leaving a mute icon in the menu bar with no explanation.
        import onboarding
        if onboarding.needs_setup():
            AppKit.NSTimer.scheduledTimerWithTimeInterval_repeats_block_(
                0.4, False, lambda _t: _DELEGATE.show_welcome())

        log("app: running")
        app.run()
    except Exception:
        log(f"app: failed to start\n{traceback.format_exc()}", err=True)
        raise


if __name__ == "__main__":
    main()
