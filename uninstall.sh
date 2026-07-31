#!/bin/bash
# Remove Vexflow: stop it, drop the login item, delete the app bundle.
#
# Your source folder, virtualenv and settings are left alone. Pass --purge to also
# delete your settings, vocabulary and API keys.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="org.salessprintgroup.vexflow"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SUPPORT="$HOME/Library/Application Support/Vexflow"

launchctl unload "$PLIST" 2>/dev/null || true
rm -f "$PLIST"
pkill -f "$DIR/vexflow_app.py" 2>/dev/null || true
rm -rf /Applications/Vexflow.app
rm -f "$SUPPORT/vexflow.lock"
rm -f "$HOME/Library/Logs/vexflow.log" "$HOME/Library/Logs/vexflow-install.log"

echo "Vexflow stopped, login item removed, app bundle deleted."

if [ "${1:-}" = "--purge" ]; then
  rm -rf "$SUPPORT"
  for entry in "vexflow-deepgram deepgram" "vexflow-deepgram-billing deepgram" \
               "vexflow-anthropic anthropic" "vexflow-openai openai"; do
    set -- $entry
    security delete-generic-password -s "$1" -a "$2" >/dev/null 2>&1 || true
  done
  echo "Settings, vocabulary and Keychain entries removed."
else
  echo "Settings and API keys kept. Run './uninstall.sh --purge' to remove those too."
fi

echo "Permissions in System Settings (Microphone, Accessibility) can be revoked by hand."
