"""Vexflow CLI — run it from a terminal, no menu bar icon.

Useful for debugging: the log goes straight to the terminal instead of a file.
For everyday use run the menu bar app instead (./install.sh).
"""
import sys

import Quartz

import config
import logutil
import macos
import settings
from engine import Engine


def main():
    logutil.force_on()   # to the terminal, so the Settings switch does not apply
    if not macos.acquire_single_instance_lock():
        print("Vexflow is already running (the menu bar app?). Two copies means "
              "duplicated pastes.\nQuit it first: menu bar icon -> Quit Vexflow.")
        sys.exit(1)

    engine = Engine()
    engine.start()   # the event tap attaches to THIS thread's run loop

    if not engine.has_key:
        print("No Deepgram key found. Either run the menu bar app and use Settings,\n"
              "or store one now:\n"
              f'  security add-generic-password -s {config.KEYCHAIN_SERVICE} '
              f'-a {config.KEYCHAIN_ACCOUNT} -w "<DEEPGRAM_API_KEY>"\n'
              f"  or temporarily:  export {config.ENV_VAR}=<key>")
        sys.exit(1)

    ptt_key = settings.get("ptt_key")
    ptt = config.HOTKEY_NAMES.get(ptt_key, ptt_key)
    toggle = settings.get("toggle_key")
    hint = f"Hold [{ptt}] to dictate."
    if toggle:
        hint += f" Tap [{config.HOTKEY_NAMES.get(toggle, toggle)}] to toggle."
    if settings.get("mouse_toggle"):
        hint += " Middle mouse button also toggles."
    print(f"Vexflow ready (CLI). {hint} Ctrl-C to quit.")

    try:
        # Run the loop in slices: the tap is serviced here, and returning to Python
        # every 0.5 s keeps Ctrl-C responsive (an uninterrupted CFRunLoopRun()
        # swallows KeyboardInterrupt).
        while True:
            Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 0.5, False)
    except KeyboardInterrupt:
        print("\nStopping.")
        engine.stop(wait_session=2.0)


if __name__ == "__main__":
    main()
