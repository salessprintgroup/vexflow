#!/bin/bash
# Vexflow — one-command setup.
#
#   ./setup.sh              install, build the app, start it, keep it running at login
#   ./setup.sh --no-startup install and start it, but do not add it to login items
#
# Safe to run again after pulling an update: it reuses the virtualenv and rebuilds
# the app bundle.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

AUTOSTART=1
[ "${1:-}" = "--no-startup" ] && AUTOSTART=0

say() { printf '\033[1m%s\033[0m\n' "$*"; }
ok()  { printf '  \033[32m✓\033[0m %s\n' "$*"; }
die() { printf '  \033[31m✗\033[0m %s\n' "$*" >&2; exit 1; }

say "Vexflow setup"

# 1. macOS version -------------------------------------------------------------
MACOS_MAJOR=$(sw_vers -productVersion | cut -d. -f1)
[ "$MACOS_MAJOR" -ge 14 ] || die "macOS 14 (Sonoma) or newer is required; found $(sw_vers -productVersion)"
ok "macOS $(sw_vers -productVersion)"

# 2. Python --------------------------------------------------------------------
# The system python3 in /usr/bin is a stub that only works once the Command Line
# Tools are installed, so check that it actually runs before trusting it.
PY=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$candidate"; break
  fi
done
[ -n "$PY" ] || die "Python 3.10+ not found. Install it with: xcode-select --install   (or: brew install python)"
ok "Python $($PY -c 'import platform; print(platform.python_version())') ($PY)"

# 3. Virtualenv and dependencies ----------------------------------------------
if [ ! -x ".venv/bin/python" ]; then
  say "Creating the virtualenv"
  "$PY" -m venv .venv || die "could not create .venv"
fi
say "Installing dependencies"
./.venv/bin/python -m pip install --quiet --upgrade pip
./.venv/bin/python -m pip install --quiet -r requirements.txt || die "dependency install failed"
ok "dependencies ready"

# 4. Icons and app bundle ------------------------------------------------------
say "Building the app"
./.venv/bin/python make_icon.py >/dev/null || die "icon generation failed"
./make_app.sh >/dev/null || die "app bundle build failed"
ok "/Applications/Vexflow.app"

# 5. Autostart -----------------------------------------------------------------
if [ "$AUTOSTART" -eq 1 ]; then
  ./install.sh >/dev/null
  ok "starts automatically at login"
else
  open -a /Applications/Vexflow.app
  ok "started (no login item; run ./install.sh later to add one)"
fi

cat <<'EOF'

Vexflow is running. Look for the bolt icon in your menu bar.

Next, in the Settings window that just opened:
  1. Paste a Deepgram API key      (Keys tab — "Get key" opens the signup page)
  2. Grant Microphone and Accessibility  (Permissions tab)
  3. Quit and start Vexflow once more — macOS only reads the Accessibility
     permission at launch

Then hold the right Command key, say something, and let go.

  Settings again:  menu bar icon -> Settings…
  Log:             off by default; Settings -> Permissions turns it on
  Remove:          ./uninstall.sh

EOF
