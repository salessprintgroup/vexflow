#!/bin/bash
# Create the Python environment Vexflow runs in.
#
# Called twice in a normal life: by the installer's postinstall script, and by the app
# launcher if the environment is ever missing (someone copied the .app by hand, or
# deleted Application Support). It must therefore be safe to run repeatedly.
#
# The environment lives in the user's Application Support, not inside the .app:
# /Applications is root-owned, and a user-writable directory inside a bundle there is
# a bad idea. It also means the app bundle stays a read-only artefact you can replace
# wholesale on update.
#
#   bootstrap.sh <app-resources-dir>
set -euo pipefail

RESOURCES="${1:?usage: bootstrap.sh <app-resources-dir>}"
SRC="$RESOURCES/app"
SUPPORT="$HOME/Library/Application Support/Vexflow"
VENV="$SUPPORT/venv"

log() { printf '%s %s\n' "$(date '+%m-%d %H:%M:%S')" "$*"; }

# --- find a usable Python -----------------------------------------------------
# Newest first. /usr/bin/python3 comes last but is genuinely usable: it ships with the
# Xcode Command Line Tools, and nothing in this codebase needs newer syntax. It is a
# stub until those tools are installed, so `--version` is the real test, not existence.
find_python() {
  local candidates=(
    "${VEXFLOW_PYTHON:-}"
    /opt/homebrew/bin/python3.14 /opt/homebrew/bin/python3.13
    /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.11
    /opt/homebrew/bin/python3
    /usr/local/bin/python3.14 /usr/local/bin/python3.13
    /usr/local/bin/python3.12 /usr/local/bin/python3.11
    /usr/local/bin/python3
    "$(command -v python3 2>/dev/null || true)"
    /usr/bin/python3
  )
  for py in "${candidates[@]}"; do
    [ -n "$py" ] && [ -x "$py" ] || continue
    if "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
      echo "$py"; return 0
    fi
  done
  return 1
}

PYTHON="$(find_python)" || {
  log "no usable Python 3.9+ found"
  exit 2
}
log "using $PYTHON ($("$PYTHON" -c 'import platform; print(platform.python_version())'))"

# --- build the environment ----------------------------------------------------
mkdir -p "$SUPPORT"

# A venv built by a Python that has since been upgraded or uninstalled is broken in a
# way that is confusing to debug, so verify rather than assume and rebuild if needed.
if [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c 'import sys' 2>/dev/null; then
  log "reusing the existing environment"
else
  rm -rf "$VENV"
  log "creating the environment"
  "$PYTHON" -m venv "$VENV"
fi

log "installing dependencies"
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet -r "$SRC/requirements.txt"

# Fail here rather than at first launch, where the only symptom is a menu bar icon
# that never appears.
"$VENV/bin/python" -c "import AppKit, Quartz, sounddevice, websockets" || {
  log "dependency check failed"
  exit 3
}
log "environment ready"
