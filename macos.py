"""macOS glue: Keychain, clipboard, synthetic Cmd-V, permissions, single-instance lock.

Every call into the system (subprocess or pyobjc) is isolated here so it can be
audited separately from the logic. Nothing is written to disk except the lock file
and the restart marker, neither of which contains transcript text.
"""
import fcntl
import os
import shutil
import subprocess
import sys
import time

import AppKit
from AppKit import (NSPasteboard, NSPasteboardItem, NSPasteboardTypeString,
                    NSWorkspace)
from Foundation import NSBundle, NSURL
import Quartz

import config
import logutil
from strings import t


# --- Keychain ----------------------------------------------------------------

def _keychain_read(service, account):
    try:
        # timeout 30: right after login, `security` can sit on a Keychain prompt.
        # 5 s was not enough and the app started up "with no key" on a valid Keychain.
        out = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return None


def keychain_write(service, account, secret):
    """Store or replace a secret in the login Keychain. True on success.

    The secret is passed via -w as an argument; it is visible to `ps` for the
    lifetime of this call, which is the same trade-off the documented
    `security add-generic-password` recipe makes.
    """
    try:
        out = subprocess.run(
            ["security", "add-generic-password", "-U", "-s", service,
             "-a", account, "-w", secret],
            capture_output=True, text=True, timeout=30,
        )
        return out.returncode == 0
    except Exception:
        return False


def keychain_delete(service, account):
    try:
        subprocess.run(
            ["security", "delete-generic-password", "-s", service, "-a", account],
            capture_output=True, text=True, timeout=30,
        )
        return True
    except Exception:
        return False


def get_api_key():
    """Deepgram transcription key from the Keychain or the environment."""
    return (_keychain_read(config.KEYCHAIN_SERVICE, config.KEYCHAIN_ACCOUNT)
            or os.environ.get(config.ENV_VAR) or None)


def set_api_key(key):
    return keychain_write(config.KEYCHAIN_SERVICE, config.KEYCHAIN_ACCOUNT, key)


def get_billing_key():
    """Narrow billing:read key, used only for the balance readout."""
    return _keychain_read(config.KEYCHAIN_BILLING_SERVICE, config.KEYCHAIN_BILLING_ACCOUNT)


def set_billing_key(key):
    return keychain_write(config.KEYCHAIN_BILLING_SERVICE,
                          config.KEYCHAIN_BILLING_ACCOUNT, key)


def get_llm_key(provider):
    """Cleanup key for one LLM provider: Keychain first, then that vendor's env var."""
    spec = config.CLEAN_PROVIDERS[provider]
    service, account = spec["keychain"]
    return _keychain_read(service, account) or os.environ.get(spec["env"]) or None


def set_llm_key(provider, key):
    service, account = config.CLEAN_PROVIDERS[provider]["keychain"]
    return keychain_write(service, account, key)


def clear_llm_key(provider):
    service, account = config.CLEAN_PROVIDERS[provider]["keychain"]
    return keychain_delete(service, account)


# --- Clipboard (NSPasteboard) ------------------------------------------------

# nspasteboard.org convention: Transient means "do not keep in history" (Maccy,
# Paste and Copied honour it) — without it every transcript ended up on the disk of
# whatever clipboard manager was running. Concealed marks sensitive content such as
# passwords from a password manager; we never resurrect that with a restore.
_TRANSIENT_TYPE = "org.nspasteboard.TransientType"
_CONCEALED_TYPE = "org.nspasteboard.ConcealedType"


def _pasteboard():
    return NSPasteboard.generalPasteboard()


def save_clipboard():
    """Snapshot every flavour of every item. Best effort — lazy data cannot be caught."""
    snapshot = []
    items = _pasteboard().pasteboardItems()
    if not items:
        return snapshot
    for item in items:
        data = {}
        for flavour in item.types():
            d = item.dataForType_(flavour)
            if d is not None:
                data[flavour] = d
        if data:
            snapshot.append(data)
    return snapshot


def set_text(text):
    pb = _pasteboard()
    pb.clearContents()
    pb.setString_forType_(text, NSPasteboardTypeString)
    pb.setString_forType_("", _TRANSIENT_TYPE)   # transcripts stay out of clipboard history


def restore_clipboard(snapshot):
    pb = _pasteboard()
    pb.clearContents()
    if not snapshot:
        return
    items = []
    for data in snapshot:
        if _CONCEALED_TYPE in data:
            continue   # never put back a password the manager may already have cleared
        item = NSPasteboardItem.alloc().init()
        for flavour, d in data.items():
            item.setData_forType_(d, flavour)
        items.append(item)
    if items:
        pb.writeObjects_(items)


def change_count():
    """Clipboard write counter. It increments on every write by any app, which lets
    us avoid clobbering a clipboard somebody else has since claimed."""
    return _pasteboard().changeCount()


# --- Single-instance lock (shared by the CLI and the menu bar app) -----------
# Two copies means two event taps and duplicated pastes. Application Support rather
# than Caches: the system may purge Caches, which would void the guarantee.

_LOCK_FD = None   # keep the handle open so the flock lives as long as the process


def acquire_single_instance_lock():
    """True if we are the only instance; False if another process holds the lock."""
    global _LOCK_FD
    try:
        os.makedirs(config.SUPPORT_DIR, exist_ok=True)
        _LOCK_FD = open(os.path.join(config.SUPPORT_DIR, "vexflow.lock"), "w")
    except OSError:
        return True  # could not open the lock file — do not block startup over it
    try:
        fcntl.flock(_LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


# --- Self-restart marker (recovery from a wedged CoreAudio client) -----------
# The file is empty; only its mtime matters. It is the cooldown guard against a
# restart loop when audio is dead system-wide and restarting cannot help. Survives execv.

_RESTART_MARKER = os.path.join(config.SUPPORT_DIR, "last-self-restart")


def touch_restart_marker():
    try:
        os.makedirs(config.SUPPORT_DIR, exist_ok=True)
        with open(_RESTART_MARKER, "w"):
            pass
    except OSError:
        pass


def restart_marker_age():
    """Seconds since the last self-restart, or None if there has never been one."""
    try:
        return max(0.0, time.time() - os.path.getmtime(_RESTART_MARKER))
    except OSError:
        return None


# --- Sounds ------------------------------------------------------------------

def play_sound(path, rate=1.0):
    """Fire-and-forget system sound, optionally pitch-shifted.

    afplay's --rate resamples, so a rate below 1 plays the same click lower and
    slightly slower. That is how the stop tone is derived from the start tone instead
    of picking a second, unrelated system sound.

    Runs as a separate process, so it survives even the execv self-restart.
    """
    if not path:
        return
    try:
        cmd = ["afplay", path] if rate == 1.0 else ["afplay", "-r", str(rate), path]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def play_error_sound():
    play_sound(config.ERROR_SOUND)


# --- Permissions -------------------------------------------------------------

def has_accessibility():
    """Accessibility (kTCCServicePostEvent) — required to type the text into other apps."""
    try:
        from ApplicationServices import AXIsProcessTrusted
        return bool(AXIsProcessTrusted())
    except Exception:
        return False


def prompt_accessibility():
    """Show the system prompt and register the process in the Accessibility list."""
    try:
        from ApplicationServices import AXIsProcessTrustedWithOptions
        try:
            from ApplicationServices import kAXTrustedCheckOptionPrompt as KEY
        except Exception:
            KEY = "AXTrustedCheckOptionPrompt"
        AXIsProcessTrustedWithOptions({KEY: True})
    except Exception:
        pass


def microphone_status():
    """'granted' | 'denied' | 'undetermined' | 'unknown'.

    'unknown' just means the AVFoundation bindings are not installed; recording still
    works, macOS will ask on the first attempt.
    """
    try:
        from AVFoundation import (AVCaptureDevice, AVMediaTypeAudio,
                                  AVAuthorizationStatusAuthorized,
                                  AVAuthorizationStatusDenied,
                                  AVAuthorizationStatusNotDetermined)
        status = AVCaptureDevice.authorizationStatusForMediaType_(AVMediaTypeAudio)
        return {
            AVAuthorizationStatusAuthorized: "granted",
            AVAuthorizationStatusDenied: "denied",
            AVAuthorizationStatusNotDetermined: "undetermined",
        }.get(status, "denied")
    except Exception:
        return "unknown"


def request_microphone(callback=None):
    """Trigger the system microphone prompt. No-op if the bindings are missing."""
    try:
        from AVFoundation import AVCaptureDevice, AVMediaTypeAudio
        AVCaptureDevice.requestAccessForMediaType_completionHandler_(
            AVMediaTypeAudio, callback or (lambda granted: None))
        return True
    except Exception:
        return False


# Deep links into the relevant System Settings panes, so the Settings window can send
# the user exactly where the switch is instead of describing the path in prose.
SETTINGS_PANES = {
    "accessibility": "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility",
    "microphone": "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone",
    "input-monitoring": "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent",
}


def open_settings_pane(which):
    open_url(SETTINGS_PANES.get(which, SETTINGS_PANES["accessibility"]))


def open_url(url):
    try:
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
        return True
    except Exception:
        return False


def open_path(path):
    """Open a file with its default app, creating it first if it does not exist."""
    try:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8"):
                pass
        NSWorkspace.sharedWorkspace().openFile_(path)
        return True
    except Exception:
        return False


# --- App identity in the Dock ------------------------------------------------
# We run as the interpreter, so the bundle macOS sees is Python's own app bundle:
# without the two calls below the Dock announces a rocket called "Python" the moment a
# window opens. Freezing the app with PyInstaller would fix it at the cost of shipping
# a blob instead of readable source, which is the one trade this project will not make.

def set_app_identity():
    """Make the process call itself Vexflow and look like Vexflow.

    Two separate things, because macOS asks two different questions:

    * The NAME comes from the main bundle's info dictionary, patched here in memory.
      Setting the title of our own NSMenu does NOT do this — the name is CFBundleName
      or nothing.
    * The ICON is asked for by name. Everything that draws an application icon
      without being told which one — NSAlert, the About panel — calls
      `imageNamed:NSApplicationIcon` and gets the interpreter's rocket. Registering
      ours under that name redirects all of them at once. The Dock tile is the
      exception and is handled in become_foreground().

    Call it before the first NSApplication is created.
    """
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    if info is not None:
        info["CFBundleName"] = config.APP_NAME
        info["CFBundleDisplayName"] = config.APP_NAME
        # The version and the copyright line come from the same dictionary, and the
        # About panel reads them. Left alone, it credited the Python Software
        # Foundation, in 2001, for version 3.14.5 — a wrong copyright notice inside a
        # product published by someone else.
        info["CFBundleShortVersionString"] = config.VERSION
        info["CFBundleVersion"] = config.VERSION
        info["NSHumanReadableCopyright"] = f"{config.COPYRIGHT}. {config.LICENSE_NAME}."

    icon = app_icon()
    if icon is not None:
        previous = AppKit.NSImage.imageNamed_("NSApplicationIcon")
        if previous is not None:
            previous.setName_(None)   # a name belongs to one image at a time
        icon.setName_("NSApplicationIcon")


_APP_ICON = None


def app_icon():
    """Our icon as an NSImage, loaded once. None if the assets are missing."""
    global _APP_ICON
    if _APP_ICON is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "Vexflow.icns")
        _APP_ICON = AppKit.NSImage.alloc().initWithContentsOfFile_(path)
    return _APP_ICON


def become_foreground():
    """Take a Dock icon and the keyboard focus, for as long as a window is open.

    The icon is applied HERE rather than once at startup: an accessory app has no Dock
    tile, and the tile created by the policy change below does not inherit an image
    that was set while there was nothing to set it on — it falls back to the bundle's,
    i.e. the Python rocket.
    """
    app = AppKit.NSApp()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
    icon = app_icon()
    if icon is not None:
        app.setApplicationIconImage_(icon)
    app.activateIgnoringOtherApps_(True)


def become_background():
    """Back to menu-bar-only, so no Dock icon lingers for a background app."""
    AppKit.NSApp().setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)


# --- Synthetic Cmd-V (Quartz CGEvent) ----------------------------------------

_KVK_ANSI_V = 0x09  # virtual keycode for the V key (ANSI)

# The system ORs physical Shift/Option/Ctrl into synthetic events (documented Quartz
# default: state combining), which turned Cmd-V into Cmd-Opt-V or Cmd-Shift-V and
# silently broke the paste. Cmd itself is deliberately NOT waited for: it ORs into
# Cmd-V harmlessly (it is the flag we want), and waiting would break the paste on the
# next push-to-talk hold.
_WAIT_MODS = (Quartz.kCGEventFlagMaskShift
              | Quartz.kCGEventFlagMaskAlternate
              | Quartz.kCGEventFlagMaskControl)


def _wait_modifiers_clear(timeout=1.0, step=0.02):
    """Wait for Shift/Option/Ctrl to be released; post anyway on timeout, otherwise
    the transcript would vanish from the clipboard on restore."""
    deadline = time.monotonic() + timeout
    while Quartz.CGEventSourceFlagsState(
            Quartz.kCGEventSourceStateHIDSystemState) & _WAIT_MODS:
        if time.monotonic() >= deadline:
            break
        time.sleep(step)


def restart_app():
    """Replace this process with a fresh copy of itself.

    macOS reads the Accessibility permission only at launch, so granting it mid-session
    does nothing until a restart. Offering the restart in the UI is friendlier than
    telling somebody to hunt down a menu bar icon and quit it.
    """
    argv = [sys.executable, os.path.abspath(sys.argv[0])]
    try:
        os.execv(argv[0], argv)
    except Exception:
        return False
    return True


def paste():
    """Emulate Cmd-V into the frontmost app. Requires Accessibility."""
    _wait_modifiers_clear()
    src = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    down = Quartz.CGEventCreateKeyboardEvent(src, _KVK_ANSI_V, True)
    Quartz.CGEventSetFlags(down, Quartz.kCGEventFlagMaskCommand)
    up = Quartz.CGEventCreateKeyboardEvent(src, _KVK_ANSI_V, False)
    Quartz.CGEventSetFlags(up, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)


# --- Uninstall ----------------------------------------------------------------

def uninstall(purge=False):
    """Drop the login item, delete the app. Returns (ok, message).

    A packaged app has no Finder-drag uninstall to fall back on, so it has to be able
    to remove itself. Deleting the bundle we are running from is safe on macOS: the
    process keeps going from the unlinked inode until it exits.

    There is deliberately no `launchctl bootout` here, and that is the whole story of
    why removal used to take two goes. Vexflow IS the launchd job, so booting it out
    killed this process on the spot — the app vanished, the bundle stayed, and only a
    second attempt (started by hand, so not a job any more) ever reached the delete.
    Deleting the plist is enough: nothing brings the job back at the next login, and
    quitting cleanly does not trip KeepAlive, which only fires on a crash.
    """
    plist = os.path.expanduser(f"~/Library/LaunchAgents/{config.BUNDLE_ID}.plist")
    try:
        os.remove(plist)
    except OSError:
        pass
    logutil.remove_log()   # diagnostics for an app that is going away are just litter

    if purge:
        try:
            shutil.rmtree(config.SUPPORT_DIR, ignore_errors=True)
        except Exception:
            pass
        keychain_delete(config.KEYCHAIN_SERVICE, config.KEYCHAIN_ACCOUNT)
        keychain_delete(config.KEYCHAIN_BILLING_SERVICE, config.KEYCHAIN_BILLING_ACCOUNT)
        for spec in config.CLEAN_PROVIDERS.values():
            keychain_delete(*spec["keychain"])

    return _delete_bundle("/Applications/Vexflow.app")


def _delete_bundle(path):
    """Delete the app bundle and CONFIRM it is gone. Returns (ok, message).

    Confirming is the point. This used to report "Vexflow has been removed" on the
    strength of an exit code, which left the app sitting in /Applications under a
    dialog saying it was not.

    The installer hands the bundle to the person who installed it, so the ordinary
    case is a plain delete with no password. A bundle from an older install is still
    root-owned, and that is what the fallback is for; macOS titles that dialog after
    osascript whatever prompt we pass it, which is why it is a fallback and not the
    normal path.
    """
    if not os.path.exists(path):
        return True, t("Vexflow has been removed.")

    shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        return True, t("Vexflow has been removed.")

    script = (f'do shell script "rm -rf {path!s}" '
              f'with prompt "Vexflow needs your password to remove itself '
              f'from the Applications folder." '
              f'with administrator privileges')
    try:
        out = subprocess.run(["osascript", "-e", script],
                             capture_output=True, text=True, timeout=120)
    except Exception as e:
        return False, t("Login item removed; deleting the app failed: ") + str(e)
    if os.path.exists(path):
        return False, (t("Login item removed, but deleting the app was cancelled.")
                       if out.returncode != 0 else
                       t("Login item removed, but the app could not be deleted."))
    return True, t("Vexflow has been removed.")
