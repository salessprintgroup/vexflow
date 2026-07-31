#!/bin/bash
# Build /Applications/Vexflow.app — a menu bar app (no Dock icon) that wraps the venv
# python.
#
# The bundle lives in /Applications but THE CODE STAYS in this folder; the launcher
# reaches back here by absolute path. Move this folder and you have to run this script
# again.
#
# macOS attributes the permissions to "Python" rather than to "Vexflow", because the
# launcher execs the interpreter. Getting a permission grant that names Vexflow would
# require freezing the app with PyInstaller, which is a deliberate non-goal: shipping
# readable source is the point of this project.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
APP="/Applications/Vexflow.app"

[ -x "$DIR/.venv/bin/python" ] || { echo "No .venv — run ./setup.sh first" >&2; exit 1; }

# From config.py, the one place a version number is written. It used to be typed here
# as well, which is how this bundle ended up claiming 1.0 after the app moved on.
VERSION="$("$DIR/.venv/bin/python" -c 'import config; print(config.VERSION)')"

# Icons are generated from code; assets/ is a build artefact and is not in git.
if [ ! -f "$DIR/assets/Vexflow.icns" ] || [ ! -f "$DIR/assets/menubar-idle@2x.png" ]; then
  "$DIR/.venv/bin/python" "$DIR/make_icon.py" >/dev/null
fi

# Guard against a typo in APP: only remove something that looks like our own bundle.
if [ -e "$APP" ] && [ ! -f "$APP/Contents/MacOS/vexflow" ]; then
  echo "$APP exists but is not a Vexflow bundle — refusing to touch it" >&2
  exit 1
fi
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$DIR/assets/Vexflow.icns" "$APP/Contents/Resources/Vexflow.icns"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>Vexflow</string>
  <key>CFBundleDisplayName</key><string>Vexflow</string>
  <key>CFBundleIdentifier</key><string>org.salessprintgroup.vexflow</string>
  <key>CFBundleExecutable</key><string>vexflow</string>
  <key>CFBundleIconFile</key><string>Vexflow</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleVersion</key><string>$VERSION</string>
  <key>CFBundleShortVersionString</key><string>$VERSION</string>
  <key>NSHumanReadableCopyright</key><string>© 2026 Sales Sprint Group LLC. MIT License. Provided as is, without warranty of any kind.</string>
  <key>NSMicrophoneUsageDescription</key><string>Vexflow sends your speech to Deepgram with your own API key so it can be typed as text.</string>
  <key>LSUIElement</key><true/>
  <key>LSMinimumSystemVersion</key><string>14.0</string>
</dict></plist>
PLIST

cat > "$APP/Contents/MacOS/vexflow" <<LAUNCH
#!/bin/bash
cd "$DIR"
SETTINGS="\$HOME/Library/Application Support/Vexflow/settings.json"
LOG="\$HOME/Library/Logs/vexflow.log"
# The app writes its own log and follows the setting live. This only catches output
# nothing else routes — tracebacks, stderr from the audio library.
if [ -f "\$SETTINGS" ] && grep -q '"logging_enabled"[[:space:]]*:[[:space:]]*true' "\$SETTINGS"; then
  mkdir -p "\$HOME/Library/Logs"
else
  rm -f "\$LOG"
  LOG=/dev/null
fi
exec "$DIR/.venv/bin/python" "$DIR/vexflow_app.py" >> "\$LOG" 2>&1
LAUNCH
chmod +x "$APP/Contents/MacOS/vexflow"

# Finder caches icons by bundle mtime; without this it shows a stale or blank icon.
touch "$APP"

echo "Built $APP"
