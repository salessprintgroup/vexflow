#!/bin/bash
# Vexflow.app/Contents/MacOS/vexflow — what macOS actually starts.
#
# The app bundle carries readable source in Contents/Resources/app; the Python
# environment lives in the user's Application Support. This script joins the two.
CONTENTS="$(cd "$(dirname "$0")/.." && pwd)"
RESOURCES="$CONTENTS/Resources"
SRC="$RESOURCES/app"
SUPPORT="$HOME/Library/Application Support/Vexflow"
VENV="$SUPPORT/venv"
LOG="$HOME/Library/Logs/vexflow.log"

# The app writes its own log, and decides that live from the setting — this script is
# only choosing where the noise NOBODY routes goes: a Python traceback, a PortAudio
# complaint on stderr, the environment build below. With logging off there is no file
# for that either, and a stale one from a previous run is removed.
#
# settings.json is written by json.dump(indent=2), which puts the flag on its own line.
if [ -f "$SUPPORT/settings.json" ] &&
   grep -q '"logging_enabled"[[:space:]]*:[[:space:]]*true' "$SUPPORT/settings.json"; then
  mkdir -p "$HOME/Library/Logs"
else
  rm -f "$LOG"
  LOG=/dev/null
fi

# Self-heal: the installer normally builds this, but the .app may have been copied by
# hand, or Application Support cleaned out. Rebuilding takes a minute and beats a menu
# bar icon that never appears.
if [ ! -x "$VENV/bin/python" ]; then
  echo "launcher: no Python environment yet, building one" >> "$LOG"
  osascript -e 'display notification "Setting up. This takes about a minute." with title "Vexflow"' 2>/dev/null || true
  # Captured rather than streamed, so the failure can explain itself in the dialog. It
  # has to: with logging off there is no file to send anyone to, and this is the one
  # failure that happens before the app exists to switch logging on in.
  OUT="$("$RESOURCES/bootstrap.sh" "$RESOURCES" 2>&1)"; STATUS=$?
  printf '%s\n' "$OUT" >> "$LOG"
  if [ $STATUS -ne 0 ]; then
    DETAIL="$(printf '%s' "$OUT" | tail -3 | tr '\n"' '  ')"
    osascript -e "display alert \"Vexflow could not start\" message \"Setting up its Python environment failed. Installing the Xcode Command Line Tools usually fixes it: xcode-select --install\n\n$DETAIL\" as critical" 2>/dev/null || true
    exit 1
  fi
fi

exec "$VENV/bin/python" "$SRC/vexflow_app.py" >> "$LOG" 2>&1
