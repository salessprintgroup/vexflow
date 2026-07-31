"""Vexflow defaults.

Anything the Settings window can change is only a DEFAULT here — the live value
lives in settings.py (~/Library/Application Support/Vexflow/settings.json).
Everything else in this file is edit-and-restart.
"""
import os

APP_NAME = "Vexflow"
VERSION = "1.2.2"
# Interface languages, each written in itself: that is how somebody finds their own in
# a list they cannot yet read. English is the source language — its strings are the
# lookup keys in strings.py, so it is the one entry with no table of its own.
#
# Which of them is in use is a setting (settings.py, "ui_language"), not a property of
# the build. Empty means "whatever macOS is set to", which is what a fresh install gets.
# VEXFLOW_UI_LANG overrides both, for looking at one without changing anything:
#   VEXFLOW_UI_LANG=uk ./.venv/bin/python vexflow.py
UI_LANGUAGES = [
    ("English", "en"),
    ("Deutsch", "de"),
    ("Español", "es"),
    ("Français", "fr"),
    ("Italiano", "it"),
    ("Nederlands", "nl"),
    ("Polski", "pl"),
    ("Português", "pt"),
    ("Türkçe", "tr"),
    ("Русский", "ru"),
    ("Українська", "uk"),
]
# The line macOS shows in its own microphone dialog. It lives here, rather than only in
# the build script, so it is translated in i18n/ like every other sentence a user reads.
# macOS reads it out of Info.plist before Python starts, so it follows the SYSTEM
# language rather than the interface setting — the build writes one InfoPlist.strings
# per language and lets macOS pick.
MIC_USAGE = ("Vexflow sends your speech to Deepgram with your own API key so it can be "
             "typed as text.")
BUNDLE_ID = "org.salessprintgroup.vexflow"
HOMEPAGE = "https://github.com/salessprintgroup/vexflow"

# The trading name for prose, the registered entity for the copyright notice — a
# copyright line names the legal holder, and it has to match LICENSE.
VENDOR_NAME = "Sales Sprint Group"
VENDOR_LEGAL = "Sales Sprint Group LLC"
VENDOR_URL = "https://salessprintgroup.org"
COPYRIGHT_YEAR = "2026"
COPYRIGHT = f"© {COPYRIGHT_YEAR} {VENDOR_LEGAL}"
# The notice the app shows about itself. Short enough for the About panel, and it says
# the two things that matter: which licence, and that there is no warranty. Long form
# in LICENSE and NOTICE.
LICENSE_NAME = "MIT License"
LICENSE_URL = f"{HOMEPAGE}/blob/main/LICENSE"
# Kept as a plain string with placeholders rather than an f-string: it has to survive
# a dictionary lookup in strings.py, and an f-string would bake this build's values
# into the key.
LEGAL_NOTICE_BODY = (
    "Provided as is, without warranty of any kind, and used entirely at your own "
    "risk.\n\n"
    "{app} is a client for external services that you choose, hold accounts with and "
    "pay directly. Those services are not operated by or answerable to {vendor}; "
    "their terms, prices and handling of your data are a matter between you and them, "
    "and nothing here is said on their behalf. Charges incurred through your keys are "
    "yours, and no undertaking is given about the safety of any key you enter.\n\n"
    "Other names belong to their owners and appear only to identify what this "
    "connects to. No affiliation or endorsement is claimed.")
SUPPORT_DIR = os.path.expanduser("~/Library/Application Support/Vexflow")

# --- Deepgram ----------------------------------------------------------------
# Parameters verified against developers.deepgram.com.
# `dictation` and `filler_words` are deliberately off: they are English-only and
# corrupt non-English output under language=multi.
DEEPGRAM_HOST = "wss://api.deepgram.com/v1/listen"
DEEPGRAM_PARAMS = {
    "model": "nova-3",
    # `language` is chosen in Settings and injected per session.
    "smart_format": "true",
    "punctuate": "true",
    "interim_results": "true",
    "endpointing": "300",     # ms of silence before a segment is finalised
    "encoding": "linear16",   # raw PCM 16-bit LE signed (headerless -> encoding+rate required)
    "sample_rate": "16000",
    "channels": "1",
}

# Recognition language.
#
# Pick a single language when you mostly dictate in one: recall is measurably better
# than `multi`, which juggles ten languages and drops words. Foreign technical terms
# that come back transliterated get repaired by the cleanup pass. Use `multi` only if
# you genuinely code-switch mid-sentence.
# Full list: https://developers.deepgram.com/docs/models-languages-overview
LANGUAGES = [
    ("English", "en"),
    ("Multilingual (code-switching)", "multi"),
    ("Spanish", "es"),
    ("German", "de"),
    ("French", "fr"),
    ("Portuguese", "pt"),
    ("Italian", "it"),
    ("Dutch", "nl"),
    ("Russian", "ru"),
    ("Ukrainian", "uk"),
    ("Polish", "pl"),
    ("Turkish", "tr"),
    ("Hindi", "hi"),
    ("Japanese", "ja"),
]
LANGUAGE_DEFAULT = "multi"

# --- Deepgram keys -----------------------------------------------------------
# Keychain first, environment variable as a fallback. Never in the code, never in git.
KEYCHAIN_SERVICE = "vexflow-deepgram"
KEYCHAIN_ACCOUNT = "deepgram"
ENV_VAR = "DEEPGRAM_API_KEY"
DEEPGRAM_CONSOLE = "https://console.deepgram.com/signup"
# Seconds allowed for the key check (a websocket handshake, no audio).
KEY_CHECK_TIMEOUT = 8.0

# Optional SEPARATE narrow key with only the billing:read scope, used for the balance
# readout. Do not widen the transcription key for this. Without it the "Balance" menu
# entry simply does not appear.
KEYCHAIN_BILLING_SERVICE = "vexflow-deepgram-billing"
KEYCHAIN_BILLING_ACCOUNT = "deepgram"
DEEPGRAM_KEYS_CONSOLE = "https://console.deepgram.com/project/_/settings/api-keys"
BALANCE_REFRESH_SEC = 600   # how often to poll the balance, in seconds
# Below this the menu says the balance is running low. A nudge, not an alarm: dictation
# stops dead when the credit does, and the point is to notice a day before that.
BALANCE_LOW = 10.0          # in the account's own currency

# --- LLM transcript cleanup (optional) ---------------------------------------
# Speech-to-text gets words right but leaves run-on sentences, false starts and
# mangled proper nouns. A small, cheap model fixes that in under a second.
#
# Bring your own key from either vendor. No key -> cleanup is off and you still get
# the raw Deepgram transcript; dictation never depends on this.
#
# `api` is overridable per provider in Settings, so any OpenAI-compatible endpoint
# (a local model, a proxy, a gateway) works by pointing the OpenAI provider at it.
CLEAN_PROVIDERS = {
    "anthropic": {
        "label": "Claude",
        "api": "https://api.anthropic.com/v1/messages",
        "keychain": ("vexflow-anthropic", "anthropic"),
        "env": "ANTHROPIC_API_KEY",
        "console": "https://console.anthropic.com/settings/keys",
        "models": [
            ("Haiku 4.5 — fastest, cheapest", "claude-haiku-4-5"),
            ("Sonnet 5 — balanced", "claude-sonnet-5"),
            ("Opus 5 — most accurate", "claude-opus-5"),
        ],
        "default_model": "claude-haiku-4-5",
    },
    "openai": {
        "label": "OpenAI",
        "api": "https://api.openai.com/v1/chat/completions",
        "keychain": ("vexflow-openai", "openai"),
        "env": "OPENAI_API_KEY",
        "console": "https://platform.openai.com/api-keys",
        "models": [
            ("GPT-5.6 Luna — fastest, cheapest", "gpt-5.6-luna"),
            ("GPT-5.6 Terra — balanced", "gpt-5.6-terra"),
            ("GPT-5.6 Sol — most accurate", "gpt-5.6-sol"),
        ],
        "default_model": "gpt-5.6-luna",
    },
}
CLEAN_PROVIDER_DEFAULT = "anthropic"
ANTHROPIC_VERSION = "2023-06-01"
CLEAN_TIMEOUT = 8.0                # seconds per request; timeout or error -> raw text
CLEAN_MAX_TOKENS = 4096

# Your own vocabulary: names, product names, jargon, acronyms the recogniser keeps
# mangling. One term per line, or "wrong -> right" to force a correction.
# The file is gitignored — it is yours, and it only ever travels inside the cleanup
# prompt to the LLM vendor you chose.
VOCABULARY_FILE = os.path.join(SUPPORT_DIR, "vocabulary.txt")

# --- Diagnostics -------------------------------------------------------------
# The log is OFF by default and there is no file until you switch it on in Settings.
# A dictation tool that leaves a running account of when you spoke, for how long and
# how much you said is keeping a diary nobody asked for; you turn that on to chase a
# problem, and off again afterwards. Switching it off deletes the file.
#
# The cost is honest: with the log off, "it does not start" has to be reproduced with
# the log on before anyone can say why.
LOG_FILE = os.path.expanduser("~/Library/Logs/vexflow.log")
LOGGING_DEFAULT = False
LOG_MAX_BYTES = 5 * 1024 * 1024   # trimmed to the last of these when it is opened

# The ONLY switch that can put dictated text into the log file. It is an environment
# variable rather than a setting on purpose: a flag in a file can be turned on to chase
# one bug and then quietly stay on for months. This one lasts exactly as long as the
# process you launched with it, and the app logs a warning while it is active.
#
#   VEXFLOW_DEBUG_TRANSCRIPT=1 ./.venv/bin/python vexflow.py
#
# With it off — which is every normal run — no transcript ever reaches disk.
DEBUG_TRANSCRIPT = os.environ.get("VEXFLOW_DEBUG_TRANSCRIPT") == "1"

# --- Audio -------------------------------------------------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCKSIZE = 1600              # 100 ms frames (16000 * 0.1)

# --- Hotkeys -----------------------------------------------------------------
# Only modifier keys are supported: they are the only keys you can hold down without
# typing something into the app you are dictating into.
#
# A hotkey is one modifier, or a chord written with "+". Reach for a chord when every
# free single modifier is one you press while typing — holding Left Option alone would
# open the microphone on every option-click — or when another app already owns the
# obvious keys.
#
# Note that not every Mac keyboard has every key. Neither the built-in keyboard nor
# the Magic Keyboard has a RIGHT Control, so "ctrl_r" silently never fires on those.
# A None entry draws a separator in the menus and popups that show this list.
HOTKEY_CHOICES = [
    ("Right Command", "cmd_r"),
    ("Right Option", "alt_r"),
    ("Left Command", "cmd_l"),
    ("Left Option", "alt_l"),
    ("Left Control", "ctrl_l"),
    ("Right Control", "ctrl_r"),
    ("Left Shift", "shift_l"),
    ("Right Shift", "shift_r"),
    None,
    ("Control + Option", "ctrl_l+alt_l"),
    ("Control + Shift", "ctrl_l+shift_l"),
    ("Command + Option", "cmd_l+alt_l"),
    ("Option + Shift", "alt_l+shift_l"),
    ("Control + Option + Shift", "ctrl_l+alt_l+shift_l"),
]
# value -> display name, for anything that needs to render a stored hotkey.
HOTKEY_NAMES = {value: title for title, value in (c for c in HOTKEY_CHOICES if c)}

# Push-to-talk: hold, speak, release.
PTT_HOLD_KEY = "cmd_r"
# Toggle, for longer stretches: tap to start, tap again to stop. Empty string = off.
# Right Control is the default because it is the one modifier that is never part of
# ordinary typing — on keyboards that have it. Several Apple keyboards do not, in which
# case the toggle simply never fires and you pick another one in Settings.
TOGGLE_KEY = "ctrl_r"
# Toggle from a mouse button. Many mice report every extra button as "middle", so
# all of them end up toggling; that is why it ships off.
TOGGLE_MOUSE_BUTTON = False

# --- Pasting -----------------------------------------------------------------
PASTE_PRE_DELAY = 0.05       # let the physical Cmd lift before the synthetic Cmd-V
# Ceiling on the background wait before the clipboard is restored. A slow app
# (Electron under load) reads the clipboard after the paste, so the restore happens
# in the background, and only if nobody else wrote to the clipboard meanwhile
# (checked via changeCount).
PASTE_POST_DELAY = 1.0

# How long to wait for Deepgram's final results after the key is released.
FINALIZE_TIMEOUT = 5.0

# --- Deaf-microphone detection -----------------------------------------------
# Failure mode after sleep: the stream OPENS (the mic indicator lights up) but no
# callbacks arrive, or they carry digital silence. Resetting PortAudio inside the
# process does not clear it; only restarting the process does. Escalation ladder:
# rebuild the stream in place -> restart the process (execv).
DEAF_NO_FRAMES_SEC = 2.0      # recording this long without a single audio frame -> deaf
DEAF_STALL_SEC = 2.5          # frames were arriving and stopped (sleep, device unplugged)
DEAF_ALL_ZERO_SEC = 5.0       # this long of pure zeroes -> input muted or grabbed elsewhere
DEAF_MIN_SESSION_SEC = 0.8    # shorter than this proves nothing: the stream may not have started
SELF_RESTART_COOLDOWN_SEC = 300  # never self-restart more than once per 5 minutes
# Played when a recording fails (mic never opened or went deaf, Deepgram unreachable
# or dropped). Speech went nowhere, so say so immediately instead of failing silently.
ERROR_SOUND = "/System/Library/Sounds/Basso.aiff"
# Played on the start and stop of a recording, so you know the mic is live without
# looking at the menu bar. Turn off in Settings.
#
# Both edges use the same click, with the stop pitched down by playback rate: one
# short "tik" going in, a lower "tuk" coming out. Two different system sounds read as
# two unrelated events, and Pop in particular is a double knock that sounds like the
# recording stopped twice.
START_SOUND = "/System/Library/Sounds/Tink.aiff"
START_SOUND_RATE = 1.0
STOP_SOUND = "/System/Library/Sounds/Tink.aiff"
STOP_SOUND_RATE = 0.7

# --- Recording limits (zombie-session insurance) -----------------------------
# A lost push-to-talk release (the event tap died at the exact moment of release) or
# a forgotten toggle used to record forever: hot mic, growing queue, then one giant
# paste into whatever happened to be focused. On timeout the recording stops and the
# text goes to the CLIPBOARD instead of being pasted.
MAX_PTT_SEC = 300            # a PTT hold longer than 5 min is a lost release
MAX_TOGGLE_SEC = 1800        # a toggle longer than 30 min was forgotten

# Outbound audio queue, in frames (one frame = 100 ms), so roughly 60 s of buffer.
# When the websocket is dead the oldest frames are dropped rather than accumulating
# without limit (~115 MB/hour before this cap existed).
SEND_QUEUE_MAX = 600
