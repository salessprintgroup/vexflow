"""Settings window.

Everything needed to run Vexflow lives here: API keys, language, hotkeys, the cleanup
model, and the two macOS permissions. Nobody should have to type
`security add-generic-password` to use a dictation app.

Changes apply the moment you make them, the way System Settings behaves, so there is
no Apply and nothing to lose by closing the window. Done just closes it.

The window is built lazily on first open and reused. While it is open the app switches
to a regular activation policy so the window can take keyboard focus, then drops back
to accessory (menu bar only) on close.
"""
import os

import AppKit
import objc
from Foundation import NSObject, NSMakeRect

import billing
import config
import logutil
import macos
import settings
import strings
import widgets as w
from strings import t

# What the ? next to each key row says. Long enough to answer "what is this and where
# do I get one" without sending anyone to the README, short enough to read standing up.
#
# Nothing here describes a service's pricing, plans or terms. Those belong to the
# service, they change without notice, and repeating them inside an app turns them into
# something the app appears to be promising. The button goes to the source instead.
HELP = {
    "deepgram": (
        "Deepgram key",
        "The one key Vexflow cannot work without. Your microphone audio goes from this "
        "Mac to the speech-to-text service under this key and comes back as text, with "
        "no server of ours in between. Create a key in your own account there and paste "
        "the whole string. It is kept in your login Keychain, never in a file — and, "
        "like any credential on any machine, it is yours to look after.",
        "Open the console", config.DEEPGRAM_CONSOLE),
    "billing": (
        "Balance key",
        "Optional, and a second key on purpose. Reading your account balance needs the "
        "billing:read scope, which the key above has no business holding — one key that "
        "spends and one that reads are worth keeping apart. Create a key with "
        "billing:read only and the menu bar shows the balance the service reports.",
        "Open the console", config.DEEPGRAM_KEYS_CONSOLE),
    "anthropic": (
        "Anthropic key",
        "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
        "mangled names. Only the transcript is sent, never the audio, and what the "
        "service does with it is between you and them. The key is checked the moment "
        "you save it, so a wrong one says so here instead of quietly doing nothing.",
        "Open the console", config.CLEAN_PROVIDERS["anthropic"]["console"]),
    "openai": (
        "OpenAI key",
        "Optional, and an alternative to the key above rather than an addition — "
        "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
        "also point this key at any OpenAI-compatible endpoint, including a model "
        "running on your own machine.",
        "Open the console", config.CLEAN_PROVIDERS["openai"]["console"]),
}

# The window is wider than the English interface needs, and that is the point: it has
# to hold eleven languages without a single label going under an ellipsis. German and
# Russian labels run about half again as long as their English source, and buttons are
# the tightest thing here — "Restart Vexflow" is 82 points, "Перезапустить Vexflow" is
# 127. test_i18n.py measures every control in every language against these numbers.
WIDTH, HEIGHT = 680, 556
PAD = 20
FOOTER_H = 46
# The interface language sits in a band of its own above the tabs. It changes every
# label in the window, the tab names included, so it is not a setting that belongs
# inside any one tab. The window grew by exactly this much; the tabs are unchanged.
HEADER_H = 34
# Tab views are inset from the window, so every tab lays out against ITS width.
CONTENT_W = WIDTH - 40
RIGHT = CONTENT_W - PAD          # right edge available inside a tab
LABEL_W = 170
COL = PAD + LABEL_W              # left edge of the second column
NOTE_W = RIGHT - COL
# Widths for the controls a translation is most likely to burst: the two buttons on
# every key row, and the buttons on the permissions tab.
SAVE_W, GETKEY_W = 90, 100
KEYS_CLUSTER = SAVE_W + GETKEY_W + 34    # + the help button and the gaps
ACTION_W = 170


class SettingsWindow(NSObject):
    """Owns the window. One instance, created on first open."""

    def initWithEngine_(self, engine):
        self = objc.super(SettingsWindow, self).init()
        if self is None:
            return None
        self.engine = engine
        self.window = None
        self.timer = None
        self._key_fields = {}
        self._key_status = {}
        self._help_idents = []   # index by button tag, since a tag is all AppKit carries
        self._popover = None     # AppKit does not retain it; without this it flickers out
        return self

    # --- window -------------------------------------------------------------

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
                1.0, self, b"tick:", None, True)

    def tick_(self, _timer):
        self.refresh()

    def windowWillClose_(self, _notification):
        if self.timer is not None:
            self.timer.invalidate()
            self.timer = None
        macos.become_background()

    def done_(self, _sender):
        self.window.performClose_(None)

    @objc.python_method
    def _build(self):
        style = (AppKit.NSWindowStyleMaskTitled
                 | AppKit.NSWindowStyleMaskClosable
                 | AppKit.NSWindowStyleMaskMiniaturizable)
        self.window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(0, 0, WIDTH, HEIGHT), style, AppKit.NSBackingStoreBuffered, False)
        self.window.setTitle_(t("{} Settings").format(config.APP_NAME))
        self.window.setReleasedWhenClosed_(False)
        self.window.setDelegate_(self)

        content = self.window.contentView()

        # The language names are deliberately NOT run through t(): somebody who has
        # landed in a language they cannot read finds their own by looking for a word
        # they recognise, and "Deutsch" only helps if it stays "Deutsch".
        top = HEIGHT - HEADER_H
        ui_lang_entries, _ = w.titled_entries(config.UI_LANGUAGES)
        content.addSubview_(w.label(t("Interface language"), PAD, top + 3, LABEL_W))
        self.ui_lang_popup = w.popup(ui_lang_entries, COL, top - 2, 170, self,
                                     b"changeUILanguage:")
        content.addSubview_(self.ui_lang_popup)
        # Title set when it is needed, so the prompt arrives in the language just
        # chosen — which is also the clearest possible confirmation it was understood.
        self.ui_restart_button = w.button("", COL + 180, top - 2, 160, self,
                                          b"restartApp:")
        self.ui_restart_button.setHidden_(True)
        content.addSubview_(self.ui_restart_button)

        tabs = AppKit.NSTabView.alloc().initWithFrame_(
            NSMakeRect(10, FOOTER_H, WIDTH - 20, HEIGHT - FOOTER_H - 10 - HEADER_H))
        for title, builder in (("Keys", self._tab_keys),
                               ("Dictation", self._tab_dictation),
                               ("Cleanup", self._tab_cleanup),
                               ("Permissions", self._tab_permissions)):
            # The identifier stays English; only the tab label is translated.
            item = AppKit.NSTabViewItem.alloc().initWithIdentifier_(title)
            item.setLabel_(t(title))
            view = AppKit.NSView.alloc().initWithFrame_(
                NSMakeRect(0, 0, CONTENT_W, HEIGHT - FOOTER_H - 50 - HEADER_H))
            builder(view)
            item.setView_(view)
            tabs.addTabViewItem_(item)
        content.addSubview_(tabs)

        # Footer: quiet credit on the left, the only button that closes on the right.
        content.addSubview_(w.separator(0, FOOTER_H - 4, WIDTH))
        content.addSubview_(w.linked_note(
            f"{config.APP_NAME} {config.VERSION} · © {config.COPYRIGHT_YEAR} ",
            config.VENDOR_LEGAL, config.VENDOR_URL, "",
            PAD, 16, WIDTH - PAD - 120))
        content.addSubview_(w.button(t("Done"), WIDTH - PAD - 90, 12, 90, self,
                                     b"done:", default=True, small=False))

    # --- tab: keys ----------------------------------------------------------

    @objc.python_method
    def _tab_keys(self, view):
        y = view.frame().size.height - 30
        view.addSubview_(w.label(t("Speech to text"), PAD, y, 300, bold=True))
        y -= 22
        view.addSubview_(w.note(
            t("Audio goes from this Mac straight to Deepgram using your own key. "
              "Fields marked * are required."),
            PAD, y - 18, RIGHT - PAD, 30))
        y -= 44

        y = self._key_row(view, y, "deepgram", t("Deepgram key"),
                          b"saveDeepgram:", b"openDeepgramConsole:", required=True)
        y = self._key_row(view, y, "billing", t("Balance key"),
                          b"saveBilling:", b"openDeepgramKeys:")

        y -= 8
        view.addSubview_(w.separator(PAD, y + 14, RIGHT - PAD))
        view.addSubview_(w.label(t("Transcript cleanup"), PAD, y - 8, 320, bold=True))
        y -= 30
        view.addSubview_(w.note(
            t("Optional. A small model fixes punctuation, false starts and mangled "
              "names. Without a key you still get the raw transcript."),
            PAD, y - 18, RIGHT - PAD, 30))
        y -= 44

        y = self._key_row(view, y, "anthropic", t("Anthropic key"),
                          b"saveAnthropic:", b"openAnthropicConsole:")
        y = self._key_row(view, y, "openai", t("OpenAI key"),
                          b"saveOpenAI:", b"openOpenAIConsole:")

    @objc.python_method
    def _key_row(self, view, y, ident, title, save_sel, console_sel, required=False):
        view.addSubview_((w.required_label if required else w.label)(
            title, PAD, y + 3, LABEL_W))
        f = w.field(COL, y, RIGHT - COL - KEYS_CLUSTER, secure=True,
                    placeholder=t("paste key"),
                    target=self, action=save_sel)   # Return commits
        f.setDelegate_(self)                        # for the character count as you paste
        view.addSubview_(f)
        self._key_fields[ident] = f
        # The ? carries what used to be a paragraph above the row: what the key is for,
        # and where to get one.
        self._help_idents.append(ident)
        view.addSubview_(w.help_button(RIGHT - KEYS_CLUSTER + 3, y - 1, self,
                                       b"showHelp:", tag=len(self._help_idents)))
        view.addSubview_(w.button(t("Save"), RIGHT - SAVE_W - GETKEY_W - 10, y - 1,
                                  SAVE_W, self, save_sel))
        view.addSubview_(w.button(t("Get key"), RIGHT - GETKEY_W, y - 1, GETKEY_W,
                                  self, console_sel))
        status = w.label("", COL, y - 17, NOTE_W, size=11, color=w.SECONDARY)
        view.addSubview_(status)
        self._key_status[ident] = status
        return y - 46

    # --- tab: dictation -----------------------------------------------------

    @objc.python_method
    def _tab_dictation(self, view):
        y = view.frame().size.height - 36
        lang_entries, _ = w.titled_entries(strings.entries(config.LANGUAGES))
        # "Recognition language" rather than plain "Language" only here: this row now
        # sits under the interface-language one, and two rows called Language would be
        # a puzzle. The menu bar keeps the short form, where there is nothing to mix up.
        view.addSubview_(w.label(t("Recognition language"), PAD, y + 3, LABEL_W))
        self.lang_popup = w.popup(lang_entries, COL, y - 2, 300, self, b"changeLanguage:")
        view.addSubview_(self.lang_popup)
        y -= 20
        view.addSubview_(w.note(
            t("A single language recognises better than Multilingual. Choose "
              "Multilingual only if you switch languages inside one sentence."),
            COL, y - 18, NOTE_W, 34))
        y -= 50

        hotkey_entries, _ = w.titled_entries(strings.entries(config.HOTKEY_CHOICES))

        view.addSubview_(w.label(t("Push to talk"), PAD, y + 3, LABEL_W))
        self.ptt_popup = w.popup(hotkey_entries, COL, y - 2, 300, self, b"changePTT:")
        view.addSubview_(self.ptt_popup)
        y -= 20
        view.addSubview_(w.note(t("Hold, speak, release."), COL, y - 4, NOTE_W, 16))
        y -= 36

        view.addSubview_(w.label(t("Hands-free toggle"), PAD, y + 3, LABEL_W))
        self.toggle_popup = w.popup([t("Off"), None] + hotkey_entries, COL, y - 2, 300,
                                    self, b"changeToggle:")
        view.addSubview_(self.toggle_popup)
        y -= 20
        view.addSubview_(w.note(t("Tap once to start, tap again to stop."),
                                COL, y - 4, NOTE_W, 16))
        y -= 34

        view.addSubview_(w.note(
            t("Combined entries fire only while both keys are held — safer when the "
              "free single keys are ones you type with."),
            COL, y - 18, NOTE_W, 34))
        y -= 44

        self.mouse_cb = w.checkbox(t("Also toggle with the middle mouse button"),
                                   PAD, y, RIGHT - PAD, self, b"changeMouse:")
        view.addSubview_(self.mouse_cb)
        y -= 26
        self.sounds_cb = w.checkbox(t("Play a sound when recording starts and stops"),
                                    PAD, y, RIGHT - PAD, self, b"changeSounds:")
        view.addSubview_(self.sounds_cb)
        y -= 26
        self.paste_cb = w.checkbox(t("Paste automatically (off: copy to clipboard only)"),
                                   PAD, y, RIGHT - PAD, self, b"changePaste:")
        view.addSubview_(self.paste_cb)

    # --- tab: cleanup -------------------------------------------------------

    @objc.python_method
    def _tab_cleanup(self, view):
        y = view.frame().size.height - 32
        self.clean_cb = w.checkbox(t("Clean up transcripts with an LLM"), PAD, y,
                                   RIGHT - PAD, self, b"changeCleanEnabled:")
        view.addSubview_(self.clean_cb)
        y -= 40

        self._provider_values = list(config.CLEAN_PROVIDERS.keys())
        view.addSubview_(w.label(t("Provider"), PAD, y + 3, LABEL_W))
        self.provider_popup = w.popup(
            [config.CLEAN_PROVIDERS[p]["label"] for p in self._provider_values],
            COL, y - 2, 200, self, b"changeProvider:")
        view.addSubview_(self.provider_popup)
        y -= 36

        view.addSubview_(w.label(t("Model"), PAD, y + 3, LABEL_W))
        self.model_popup = w.popup([], COL, y - 2, 300, self, b"changeModel:")
        view.addSubview_(self.model_popup)
        y -= 20
        self.model_note = w.note("", COL, y - 4, NOTE_W, 16)
        view.addSubview_(self.model_note)
        y -= 42

        view.addSubview_(w.label(t("Your vocabulary"), PAD, y + 3, LABEL_W))
        view.addSubview_(w.button(t("Edit vocabulary…"), COL, y - 1, 150,
                                  self, b"editVocabulary:"))
        y -= 20
        view.addSubview_(w.note(
            t("Names and jargon the recogniser keeps getting wrong. One per line, "
              "kept on this Mac."),
            COL, y - 20, NOTE_W, 36))
        y -= 56

        view.addSubview_(w.separator(PAD, y + 16, RIGHT - PAD))
        view.addSubview_(w.label(t("Advanced"), PAD, y - 4, 120, bold=True, size=11))
        y -= 28
        view.addSubview_(w.label(t("Endpoint"), PAD, y + 3, LABEL_W, size=12))
        self.api_field = w.field(COL, y, RIGHT - COL - 75, target=self,
                                 action=b"saveEndpoint:")
        view.addSubview_(self.api_field)
        view.addSubview_(w.button(t("Save"), RIGHT - SAVE_W, y - 1, SAVE_W, self,
                                  b"saveEndpoint:"))
        y -= 20
        view.addSubview_(w.note(
            t("Leave as-is for the vendor's own API, or point it at any "
              "OpenAI-compatible endpoint."),
            COL, y - 18, NOTE_W, 32))

    # --- tab: permissions ---------------------------------------------------

    @objc.python_method
    def _tab_permissions(self, view):
        y = view.frame().size.height - 34
        view.addSubview_(w.note(
            t("macOS asks for these once. Vexflow cannot record or type without them."),
            PAD, y, RIGHT - PAD, 18, size=12))
        y -= 48

        view.addSubview_(w.label(t("Microphone"), PAD, y + 3, LABEL_W))
        self.mic_status = w.label("", COL, y + 3, RIGHT - COL - ACTION_W - 10, size=12)
        view.addSubview_(self.mic_status)
        self.mic_button = w.button(t("Open Settings"), RIGHT - ACTION_W, y - 1, ACTION_W, self,
                                   b"openMicPane:")
        view.addSubview_(self.mic_button)
        y -= 22
        view.addSubview_(w.note(t("Lets Vexflow hear you."), COL, y - 2, NOTE_W, 16))
        y -= 48

        view.addSubview_(w.label(t("Accessibility"), PAD, y + 3, LABEL_W))
        self.ax_status = w.label("", COL, y + 3, RIGHT - COL - ACTION_W - 10, size=12)
        view.addSubview_(self.ax_status)
        self.ax_button = w.button(t("Open Settings"), RIGHT - ACTION_W, y - 1, ACTION_W, self,
                                  b"openAxPane:")
        view.addSubview_(self.ax_button)
        y -= 22
        view.addSubview_(w.note(
            t("Lets Vexflow see the hotkey and paste into the app you are using. "
              "Granting it takes effect only after Vexflow restarts."),
            COL, y - 34, NOTE_W, 50))
        y -= 70

        view.addSubview_(w.separator(PAD, y + 18, RIGHT - PAD))
        view.addSubview_(w.button(t("Re-check"), PAD, y - 4, ACTION_W, self, b"refreshNow:"))
        self.restart_button = w.button(t("Restart Vexflow"), PAD + ACTION_W + 10, y - 4, ACTION_W, self,
                                       b"restartApp:")
        view.addSubview_(self.restart_button)
        self.log_button = w.button(t("Open log"), RIGHT - ACTION_W, y - 4, ACTION_W, self, b"openLog:")
        view.addSubview_(self.log_button)
        y -= 32

        self.log_cb = w.checkbox(t("Keep a diagnostic log"), PAD, y, RIGHT - PAD,
                                 self, b"changeLogging:")
        view.addSubview_(self.log_cb)
        y -= 18
        view.addSubview_(w.note(
            t("Off, so nothing about your dictation reaches the disk. Turn it on to "
              "chase a problem and off again afterwards — switching it off deletes the "
              "file. It records timings and errors, never what you said."),
            PAD + 18, y - 30, RIGHT - PAD - 18, 46))
        y -= 54
        self.debug_note = w.note("", PAD, y - 16, RIGHT - PAD, 32)
        view.addSubview_(self.debug_note)
        y -= 36
        view.addSubview_(w.link(t("Remove Vexflow from this Mac…"), PAD, y, 320,
                                self, b"uninstall:"))

    # --- state --------------------------------------------------------------

    @objc.python_method
    def refresh(self):
        """Pull every control back in line with what is actually stored."""
        if self.window is None:
            return
        for ident in ("deepgram", "billing", "anthropic", "openai"):
            present = self._stored_key(ident)
            f = self._key_fields.get(ident)
            status = self._key_status.get(ident)
            # Leave a field being typed into alone: its status line is showing the
            # character count, and overwriting that once a second would erase the one
            # piece of feedback a field full of dots can give.
            if status is not None and not (f is not None and f.stringValue()):
                if ident == "deepgram":
                    text, bad = self._deepgram_status(present)
                elif ident == "billing":
                    text, bad = self._billing_status()
                else:
                    text, bad = self._llm_status(ident, present)
                status.setStringValue_(text)
                status.setTextColor_(w.ALERT if bad else w.SECONDARY)
            if f is not None:
                f.setPlaceholderString_(t("paste a new key to replace") if present
                                        else t("paste key"))

        w.select_value(self.ui_lang_popup, config.UI_LANGUAGES, strings.language())
        w.select_value(self.lang_popup, config.LANGUAGES, settings.get("language"))
        w.select_value(self.ptt_popup, config.HOTKEY_CHOICES, settings.get("ptt_key"))
        toggle = settings.get("toggle_key")
        if not toggle or not w.select_value(self.toggle_popup,
                                            [None, None] + config.HOTKEY_CHOICES,
                                            toggle):
            self.toggle_popup.selectItemAtIndex_(0)
        self.mouse_cb.setState_(1 if settings.get("mouse_toggle") else 0)
        self.sounds_cb.setState_(1 if settings.get("play_sounds") else 0)
        self.paste_cb.setState_(1 if settings.get("paste_automatically") else 0)

        self.clean_cb.setState_(1 if settings.get("clean_enabled") else 0)
        provider = settings.provider()
        if provider in self._provider_values:
            self.provider_popup.selectItemAtIndex_(self._provider_values.index(provider))
        self._reload_models(provider)
        self.api_field.setStringValue_(settings.api_base(provider))

        self._permission_row(self.mic_status, self.mic_button,
                             macos.microphone_status())
        self._permission_row(self.ax_status, self.ax_button,
                             "granted" if macos.has_accessibility() else "denied")
        logging_on = bool(settings.get("logging_enabled"))
        self.log_cb.setState_(1 if logging_on else 0)
        self.log_button.setHidden_(not logging_on)   # with no file there is nothing to open
        self.debug_note.setStringValue_(
            "" if not config.DEBUG_TRANSCRIPT else
            t("Transcript debug logging is ON for this run — dictated text is being "
              "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.")
            if logging_on else
            t("VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
              "write what you dictate into it."))
        self.debug_note.setTextColor_(w.ALERT)

    @objc.python_method
    def _stored_key(self, ident):
        """Whether a key is stored, asked of the engine rather than the Keychain.

        `security` is a subprocess, this window refreshes once a second, and there are
        four keys — that was four process spawns per second on the main thread.
        """
        if ident == "billing":
            return billing.current()[0] != "missing"
        if self.engine is not None:
            return (self.engine.has_key if ident == "deepgram"
                    else bool(self.engine.llm_key(ident)))
        return bool(macos.get_api_key() if ident == "deepgram"
                    else macos.get_llm_key(ident))

    @objc.python_method
    def _billing_status(self):
        """(text, is_problem) for the balance key row. The reading IS the check: a key
        that cannot read a balance has nothing else to prove."""
        state, text, amount = billing.current()
        low = billing.is_low(state, amount)
        return {
            "missing": (t("Not set"), False),
            "checking": (t("Checking with Deepgram…"), False),
            "ok": (t("Balance: {} — running low" if low else "Balance: {}").format(text),
                   low),
            "denied": (t("Deepgram rejected this key, or it has no billing:read scope"),
                       True),
            "unreachable": (t("Saved, but Deepgram could not be reached to check it"),
                            True),
        }[state]

    @objc.python_method
    def _llm_status(self, ident, present):
        """(text, is_problem) for a cleanup key row, checked the way Deepgram is.

        A wrong cleanup key is the quietest failure in the app: dictation carries on,
        the transcript simply never gets corrected.
        """
        label = config.CLEAN_PROVIDERS[ident]["label"]
        if not present:
            return t("Not set"), False
        if self.engine is None:
            return t("Saved in Keychain"), False
        detail = (self.engine.llm_key_detail.get(ident) or "")[:70]
        return {
            "checking": (t("Checking with {}…").format(label), False),
            "valid": (t("Verified — {} accepted this key").format(label), False),
            "invalid": (t("{} rejected this key: {}").format(label, detail) if detail
                        else t("{} rejected this key").format(label), True),
            "unreachable": (t("Saved, but {} could not be reached to check it")
                            .format(label), True),
            "missing": (t("Not set"), False),
        }.get(self.engine.llm_key_state.get(ident, "missing"),
              (t("Saved in Keychain"), False))

    @objc.python_method
    def _deepgram_status(self, present):
        """(text, is_problem) for the Deepgram row.

        "Saved in Keychain" was actively misleading: a mistyped key is saved just as
        happily as a real one, and the only later symptom was dictation quietly
        producing nothing. Report what Deepgram itself said.
        """
        if not present:
            # Red, because this is the one row where "not set" means nothing works.
            return t("Required — dictation does not work without it"), True
        if self.engine is None:
            return t("Saved in Keychain"), False
        return {
            "checking": (t("Checking with Deepgram…"), False),
            "valid": (t("Verified — Deepgram accepted this key"), False),
            "invalid": (t("Deepgram rejected this key. Check you copied all of it."),
                        True),
            "unreachable": (t("Saved, but Deepgram could not be reached to check it"),
                            True),
            "missing": (t("Not set"), False),
        }.get(self.engine.key_state, (t("Saved in Keychain"), False))

    @objc.python_method
    def _permission_row(self, status_label, action_button, state):
        """Grey when fine, red only when it is blocking and the button next to it
        is the fix."""
        text, blocking = {
            "granted": (t("Granted"), False),
            "denied": (t("Not granted"), True),
            "undetermined": (t("Not requested yet"), True),
            "unknown": (t("Asked on first use"), False),
        }[state]
        status_label.setStringValue_(text)
        status_label.setTextColor_(w.ALERT if blocking else w.SECONDARY)
        action_button.setHidden_(not blocking)

    @objc.python_method
    def _reload_models(self, provider):
        spec = config.CLEAN_PROVIDERS[provider]
        self.model_popup.removeAllItems()
        self._model_values = [m for _, m in spec["models"]]
        for model_label, _ in spec["models"]:
            self.model_popup.addItemWithTitle_(t(model_label))
        chosen = settings.model(provider)
        if chosen in self._model_values:
            self.model_popup.selectItemAtIndex_(self._model_values.index(chosen))
        # Say why cleanup will not run, here where the model is chosen — a rejected key
        # stops it just as completely as a missing one.
        state = (self.engine.llm_key_state.get(provider) if self.engine is not None
                 else ("valid" if macos.get_llm_key(provider) else "missing"))
        note = {
            "missing": t("No {} key yet — add one on the Keys tab.").format(spec["label"]),
            "invalid": t("{} rejected the key — check it on the Keys tab.")
                       .format(spec["label"]),
        }.get(state, "")
        self.model_note.setStringValue_(note)
        self.model_note.setTextColor_(w.ALERT if note else w.SECONDARY)

    # --- actions ------------------------------------------------------------

    @objc.python_method
    def _save_key(self, ident, setter):
        f = self._key_fields[ident]
        value = f.stringValue().strip()
        if not value:
            return
        if setter(value):
            f.setStringValue_("")
            # Check the one that changed, and only that one.
            if ident == "billing":
                billing.refresh_soon()
            elif self.engine is not None:
                self.engine.reload_keys()
                if ident == "deepgram":
                    self.engine.verify_key()
                else:
                    self.engine.verify_llm_key(ident)
            self.refresh()

    def controlTextDidChange_(self, notification):
        """Report how many characters actually landed in a key field.

        A secure field is dots, so a paste that dropped most of the key looks exactly
        like one that did not. Short of showing the secret, the count is the only
        feedback available — and "4 characters" next to a 108-character key is
        instantly readable as a bad paste.
        """
        field = notification.object()
        for ident, f in self._key_fields.items():
            if f is field:
                count = len(f.stringValue().strip())
                status = self._key_status[ident]
                status.setStringValue_(
                    t("{} characters — press Save").format(count) if count else "")
                status.setTextColor_(w.SECONDARY)
                return

    def showHelp_(self, sender):
        # Tags are not our namespace — AppKit hands plain buttons -1 — so range-check
        # rather than index blind.
        index = sender.tag() - 1
        if not 0 <= index < len(self._help_idents):
            return
        title, body, link_text, url = HELP[self._help_idents[index]]
        self._popover = w.show_help(sender, t(title), t(body), t(link_text), url)

    def saveDeepgram_(self, _s):
        self._save_key("deepgram", macos.set_api_key)

    def saveBilling_(self, _s):
        self._save_key("billing", macos.set_billing_key)

    def saveAnthropic_(self, _s):
        self._save_key("anthropic", lambda v: macos.set_llm_key("anthropic", v))

    def saveOpenAI_(self, _s):
        self._save_key("openai", lambda v: macos.set_llm_key("openai", v))

    def openDeepgramConsole_(self, _s):
        macos.open_url(config.DEEPGRAM_CONSOLE)

    def openDeepgramKeys_(self, _s):
        macos.open_url(config.DEEPGRAM_KEYS_CONSOLE)

    def openAnthropicConsole_(self, _s):
        macos.open_url(config.CLEAN_PROVIDERS["anthropic"]["console"])

    def openOpenAIConsole_(self, _s):
        macos.open_url(config.CLEAN_PROVIDERS["openai"]["console"])

    def changeUILanguage_(self, sender):
        value = w.selected_value(sender, config.UI_LANGUAGES)
        if not value or value == strings.language():
            return
        settings.set("ui_language", value)
        # Every label already on screen — this window, the menu bar, the setup guide —
        # was drawn in the old language. Redrawing all of it in place is a wide change
        # for something done once; a restart takes a second and cannot leave half the
        # interface behind. t() answers in the new language from here on.
        self.ui_restart_button.setTitle_(t("Restart to apply"))
        self.ui_restart_button.setHidden_(False)

    def changeLanguage_(self, sender):
        value = w.selected_value(sender, config.LANGUAGES)
        if value:
            settings.set("language", value)

    def changePTT_(self, sender):
        value = w.selected_value(sender, config.HOTKEY_CHOICES)
        if value:
            settings.set("ptt_key", value)
            self._rebind()

    def changeToggle_(self, sender):
        if sender.indexOfSelectedItem() == 0:
            settings.set("toggle_key", "")
        else:
            value = w.selected_value(sender, [None, None] + config.HOTKEY_CHOICES)
            if value is None:
                return
            settings.set("toggle_key", value)
        self._rebind()

    def changeMouse_(self, sender):
        settings.set("mouse_toggle", bool(sender.state()))
        self._rebind()

    def changeSounds_(self, sender):
        settings.set("play_sounds", bool(sender.state()))

    def changePaste_(self, sender):
        settings.set("paste_automatically", bool(sender.state()))

    def changeLogging_(self, sender):
        """Takes effect on this line, not at the next start: the app writes the file
        itself. Off deletes it."""
        enabled = bool(sender.state())
        settings.set("logging_enabled", enabled)
        if not enabled:
            logutil.remove_log()
        self.refresh()

    def changeCleanEnabled_(self, sender):
        settings.set("clean_enabled", bool(sender.state()))

    def changeProvider_(self, sender):
        provider = self._provider_values[sender.indexOfSelectedItem()]
        settings.set("clean_provider", provider)
        self._reload_models(provider)
        self.api_field.setStringValue_(settings.api_base(provider))

    def changeModel_(self, sender):
        index = sender.indexOfSelectedItem()
        if 0 <= index < len(self._model_values):
            settings.set_model(settings.provider(), self._model_values[index])

    def saveEndpoint_(self, _s):
        url = self.api_field.stringValue().strip()
        provider = settings.provider()
        default = config.CLEAN_PROVIDERS[provider]["api"]
        settings.set_api_base(provider, "" if url in ("", default) else url)
        self.api_field.setStringValue_(settings.api_base(provider))

    def editVocabulary_(self, _s):
        path = config.VOCABULARY_FILE
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(VOCABULARY_TEMPLATE)
            except OSError:
                pass
        macos.open_path(path)

    def openMicPane_(self, _s):
        if macos.microphone_status() == "undetermined":
            macos.request_microphone()
        else:
            macos.open_settings_pane("microphone")

    def openAxPane_(self, _s):
        macos.prompt_accessibility()
        macos.open_settings_pane("accessibility")

    def openLog_(self, _s):
        macos.open_path(config.LOG_FILE)

    def refreshNow_(self, _s):
        self.refresh()

    def restartApp_(self, _s):
        macos.restart_app()

    def uninstall_(self, _s):
        """Two questions, because one of the answers is irreversible."""
        alert = AppKit.NSAlert.alloc().init()
        alert.setMessageText_(t("Remove Vexflow from this Mac?"))
        alert.setInformativeText_(t(
            "This quits Vexflow, removes it from your login items and deletes the "
            "app. Your API keys and settings are kept unless you choose otherwise."))
        alert.addButtonWithTitle_(t("Remove"))
        alert.addButtonWithTitle_(t("Cancel"))
        alert.addButtonWithTitle_(t("Remove and Delete My Keys"))
        response = alert.runModal()
        if response == AppKit.NSAlertSecondButtonReturn:
            return
        purge = response == AppKit.NSAlertThirdButtonReturn

        ok, message = macos.uninstall(purge=purge)
        done = AppKit.NSAlert.alloc().init()
        done.setMessageText_(message)
        if ok:
            done.setInformativeText_(t(
                "Microphone and Accessibility entries stay in System Settings until "
                "you remove them by hand."))
        done.runModal()
        if ok:
            AppKit.NSApp().terminate_(None)

    @objc.python_method
    def _rebind(self):
        if self.engine is not None:
            self.engine.rebind_hotkeys()


VOCABULARY_TEMPLATE = """# Vexflow vocabulary
#
# Terms the recogniser keeps getting wrong: names, products, jargon, acronyms.
# One per line. Lines starting with # are ignored.
#
# Two forms work:
#   Kubernetes                   <- just the correct spelling
#   cuber netties -> Kubernetes  <- force a specific mishearing to a specific term
#
# This file stays on your Mac. It is sent only as part of the cleanup prompt, to
# whichever LLM vendor you configured, and only while cleanup is switched on.

"""
