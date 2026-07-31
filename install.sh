#!/bin/bash
# Keep Vexflow running: build the app bundle and register a LaunchAgent
# (RunAtLoad plus KeepAlive).
#
# KeepAlive only fires on a crash (SuccessfulExit=false), so choosing Quit from the
# menu really quits — it does not come straight back.
#
# Most people should run ./setup.sh instead; this is the autostart half of it.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="org.salessprintgroup.vexflow"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

"$DIR/make_app.sh"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/Applications/Vexflow.app/Contents/MacOS/vexflow</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><dict><key>SuccessfulExit</key><false/></dict>
</dict></plist>
PL

# Kill a manually started copy first: otherwise the launchd child loses the flock,
# exits 0, and KeepAlive{SuccessfulExit=false} treats that as a clean finish — which
# disarms the automatic restart.
pkill -f "$DIR/vexflow_app.py" 2>/dev/null || true
sleep 0.5

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "Autostart enabled ($LABEL). The icon will appear in your menu bar."
echo "  Log:     off — switch it on in Settings -> Permissions if you need one"
echo "  Remove:  ./uninstall.sh"
