#!/bin/bash
# Fetch the current Vexflow release and hand it to the installer.
#
#   curl -fsSL https://raw.githubusercontent.com/salessprintgroup/vexflow/main/get.sh | bash
#
# There is one package and it carries every language; the interface follows the system
# on a fresh install and is a setting after that. --lang is still accepted, because the
# two-package command above was handed out in chat windows that are still open, but it
# no longer selects anything.
#
# Or, if piping a downloaded script into a shell is not something you do — and it is a
# fair thing not to do — read it first and then run it:
#
#   curl -fsSLO https://raw.githubusercontent.com/salessprintgroup/vexflow/main/get.sh
#   less get.sh && bash get.sh
#
# Why this exists rather than "download the .pkg from Releases": the package is not
# signed with a paid Apple Developer certificate. A file that arrives through a browser,
# Messages or a chat client carries macOS's quarantine flag, and Gatekeeper then refuses
# to open an unsigned package at all — one dialog, one OK button, no way forward that is
# obvious from inside it. curl does not set that flag. A package fetched here therefore
# opens normally, and nobody has to be talked through System Settings on the phone.
#
# What it does not do is install anything by itself. It downloads, then opens Apple's
# own installer, which shows the licence and asks for your password the usual way.
set -euo pipefail

REPO="salessprintgroup/vexflow"
while [ $# -gt 0 ]; do
  case "$1" in
    --lang) shift; if [ $# -gt 0 ]; then shift; fi ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
PATTERN='Vexflow-[0-9.]*\.pkg'

[ "$(uname)" = Darwin ] || { echo "Vexflow is a macOS application." >&2; exit 1; }

say() { printf '\033[1m%s\033[0m\n' "$*"; }

# The asset URL comes out of the release metadata rather than being built from a version
# number, so a change in how the files are named cannot silently break this script. The
# English pattern ends at ".pkg" straight after the digits, which is what keeps it from
# matching the Russian build.
say "Looking up the current release"
URL="$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
       | grep -o "https://[^\"]*$PATTERN" | head -1)" || true
[ -n "$URL" ] || {
  echo "Could not find a $LANG_CODE package in the latest release of $REPO." >&2
  echo "Look at https://github.com/$REPO/releases and download it by hand." >&2
  exit 1
}

WORK="$(mktemp -d "${TMPDIR:-/tmp}/vexflow-get.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PKG="$WORK/$(basename "$URL")"

say "Downloading $(basename "$URL")"
curl -fL --progress-bar "$URL" -o "$PKG"

# A truncated or redirected-to-HTML download would otherwise fail later, inside the
# installer, where the message says nothing useful.
xar -tf "$PKG" >/dev/null 2>&1 || {
  echo "The downloaded file is not a valid installer package." >&2
  exit 1
}

say "Opening the installer"
open -W "$PKG"
echo "Done. Vexflow lives in Applications and starts at login."
