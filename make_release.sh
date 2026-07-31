#!/bin/bash
# Build the redistributable installer: dist/Vexflow-<version>.pkg
#
# The bundle this produces is SELF-CONTAINED in the sense that matters: it carries its
# own copy of the source, so it does not depend on this checkout still existing. What
# it does not carry is a Python interpreter — the installer builds an environment from
# whatever Python the target Mac already has (Homebrew, or the one that ships with the
# Xcode Command Line Tools).
#
# That trade is deliberate. Freezing the app with PyInstaller would remove the
# dependency and, in the same move, turn a program you can read into a binary blob —
# for a tool whose entire pitch is "audit the network path yourself", the blob is the
# worse failure.
#
#   ./make_release.sh              build the pkg
#   ./make_release.sh --install    build it, then install it on this Mac
#
# One package, every language. Until 1.2 the interface language was frozen into the
# build and there were two packages to keep in step; now it is a setting the user can
# change at any time, so there is one. The tables ride along in i18n/ and the app picks
# one at startup — the system language on a fresh install, whatever was chosen after
# that.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

INSTALL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --install) INSTALL="yes"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

VERSION="$(./.venv/bin/python -c 'import config; print(config.VERSION)' 2>/dev/null \
           || grep -E '^VERSION' config.py | cut -d'"' -f2)"
IDENTIFIER="org.salessprintgroup.vexflow.app"
DIST="$DIR/dist"

# Everything except the finished package is built OUTSIDE the repository, in a temp
# directory removed on exit. The repo ends up holding one artefact — dist/*.pkg.
#
# This is not tidiness. macOS installers relocate bundles: given a payload containing
# Vexflow.app, the installer asks Spotlight where that bundle identifier already lives
# and installs over THAT copy instead of the declared location. A staging copy inside
# the repo gets indexed like any other app, so an install wrote the payload back into
# build/root/ — leaving /Applications empty, a root-owned app tree inside the working
# copy, and a very confused user. Keeping the staging area out of the indexed tree
# removes the target; BundleIsRelocatable=false below removes the behaviour itself.
WORK="$(mktemp -d "${TMPDIR:-/tmp}/vexflow-build.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
ROOT="$WORK/root"
APP="$ROOT/Vexflow.app"
SCRIPTS="$WORK/scripts"
RES="$WORK/resources"

say() { printf '\033[1m%s\033[0m\n' "$*"; }
ok() { printf '  \033[32m✓\033[0m %s\n' "$*"; }

say "Building Vexflow $VERSION"
mkdir -p "$ROOT" "$SCRIPTS" "$RES" "$DIST"

# Releases before this one staged inside the repo. If such a directory is still around
# — possibly root-owned, if an installer relocated onto it — it is dead weight now.
if [ -e "$DIR/build" ]; then
  rm -rf "$DIR/build" 2>/dev/null \
    || echo "  note: leftover build/ is root-owned; clear it with: sudo rm -rf \"$DIR/build\""
fi

# --- icons ---------------------------------------------------------------------
# Generated rather than committed, so they can never drift from make_icon.py.
[ -x .venv/bin/python ] || { echo "run ./setup.sh first (need .venv to draw icons)" >&2; exit 1; }
./.venv/bin/python make_icon.py >/dev/null
ok "icons"

# --- app bundle ----------------------------------------------------------------
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources/app/assets"

# Source, readable, inside the bundle. Tests and dev-only scripts are left out; the
# repo is one click away for those.
for f in *.py requirements.txt; do
  case "$f" in
    test_*.py|make_icon.py|make_release.sh) continue ;;
  esac
  cp "$f" "$APP/Contents/Resources/app/"
done
# The translation tables. A subdirectory, so the loop above does not pick them up.
mkdir -p "$APP/Contents/Resources/app/i18n"
cp i18n/*.py "$APP/Contents/Resources/app/i18n/"
LANGS="$(./.venv/bin/python -c 'import config; print(" ".join(c for _, c in config.UI_LANGUAGES))')"
ok "interface languages: $LANGS"
cp assets/menubar-*.png "$APP/Contents/Resources/app/assets/"
cp assets/Vexflow.icns "$APP/Contents/Resources/app/assets/"
cp assets/Vexflow.icns "$APP/Contents/Resources/Vexflow.icns"
cp packaging/bootstrap.sh "$APP/Contents/Resources/bootstrap.sh"
cp packaging/launcher.sh "$APP/Contents/MacOS/vexflow"
# The licence and the notice travel inside the installed app, not only in the repo:
# whoever ends up with the bundle has the terms it came under, without going to look.
cp LICENSE NOTICE "$APP/Contents/Resources/"
chmod +x "$APP/Contents/MacOS/vexflow" "$APP/Contents/Resources/bootstrap.sh"

# The microphone dialog belongs to macOS, not to us: it is drawn from Info.plist before
# a line of Python runs, so it cannot follow the interface setting. What it can follow
# is the system language, and the way to do that is one InfoPlist.strings per .lproj.
# The English sentence stays in Info.plist as the fallback for languages with no table.
MIC_USAGE="$(./.venv/bin/python -c 'import config; print(config.MIC_USAGE)')"
for code in $LANGS; do
  mkdir -p "$APP/Contents/Resources/$code.lproj"
  VEXFLOW_UI_LANG="$code" ./.venv/bin/python - "$code" <<'PY' \
    > "$APP/Contents/Resources/$code.lproj/InfoPlist.strings"
import sys, config, strings
# Escaped and written as UTF-8: .strings files are read as UTF-8 by modern macOS, and
# a stray quote in a translation would otherwise truncate the sentence at that point.
text = strings.t(config.MIC_USAGE).replace("\\", "\\\\").replace('"', '\\"')
print('"NSMicrophoneUsageDescription" = "%s";' % text)
PY
done
ok "microphone dialog in $(echo "$LANGS" | wc -w | tr -d ' ') languages"

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
  <key>CFBundleDevelopmentRegion</key><string>en</string>
  <key>CFBundleVersion</key><string>$VERSION</string>
  <key>CFBundleShortVersionString</key><string>$VERSION</string>
  <key>NSHumanReadableCopyright</key><string>© 2026 Sales Sprint Group LLC. MIT License. Provided as is, without warranty of any kind.</string>
  <key>NSMicrophoneUsageDescription</key><string>$MIC_USAGE</string>
  <key>LSUIElement</key><true/>
  <key>LSMinimumSystemVersion</key><string>14.0</string>
</dict></plist>
PLIST
ok "Vexflow.app ($(du -sh "$APP" | cut -f1))"

# --- installer scripts and resources -------------------------------------------
cp packaging/postinstall "$SCRIPTS/postinstall"
cp packaging/bootstrap.sh "$SCRIPTS/bootstrap.sh"
chmod +x "$SCRIPTS/postinstall" "$SCRIPTS/bootstrap.sh"

# The installer picks its own panes by SYSTEM language, out of the .lproj directories
# below, and falls back to the ones sitting loose in Resources when there is no match.
# So the base copies are English and every translated pane is a bonus, never a
# requirement — a language can ship its interface without its installer text.
cp packaging/welcome.html packaging/conclusion.html "$RES/"
for code in $LANGS; do
  [ -f "packaging/welcome.$code.html" ] || continue
  mkdir -p "$RES/$code.lproj"
  cp "packaging/welcome.$code.html" "$RES/$code.lproj/welcome.html"
  cp "packaging/conclusion.$code.html" "$RES/$code.lproj/conclusion.html"
done
ok "installer panes: en$(for c in $LANGS; do [ -f "packaging/welcome.$c.html" ] && printf ' %s' "$c"; done)"
# The installer's licence pane. LICENSE plus NOTICE, because the trademark reservation
# and the third-party attributions belong in front of the person installing it, not
# only in a repository they may never open.
{ cat LICENSE; printf '\n\n%s\n\n' "$(printf '=%.0s' $(seq 1 78))"; cat NOTICE; } \
  > "$RES/LICENSE.txt"
sed "s/VERSION_PLACEHOLDER/$VERSION/" packaging/distribution.xml > "$WORK/distribution.xml"

# --- package -------------------------------------------------------------------
# Belt and braces against relocation: say so explicitly in the component plist, so the
# installer puts the app where --install-location says even if an older copy is found
# somewhere else on the disk.
pkgbuild --analyze --root "$ROOT" "$WORK/component.plist" >/dev/null
plutil -replace 0.BundleIsRelocatable -bool NO "$WORK/component.plist"

pkgbuild --root "$ROOT" \
         --component-plist "$WORK/component.plist" \
         --identifier "$IDENTIFIER" \
         --version "$VERSION" \
         --install-location /Applications \
         --scripts "$SCRIPTS" \
         "$WORK/vexflow-app.pkg" >/dev/null
ok "component package (relocation disabled)"

PKG="$DIST/Vexflow-$VERSION.pkg"
productbuild --distribution "$WORK/distribution.xml" \
             --package-path "$WORK" \
             --resources "$RES" \
             "$PKG" >/dev/null
ok "$PKG ($(du -h "$PKG" | cut -f1))"

# The package is unsigned, so macOS blocks the first open and the person on the other
# end is stuck at a dialog with one OK button. The route through the interface differs
# by macOS version — Sequoia dropped the right-click override — so the instruction that
# holds everywhere is the Terminal one, printed here ready to paste into a chat window.
say "Built: $PKG"
printf '\nSend one of these along with the package:\n\n'
cat <<'EOF'
  ┌─ English ──────────────────────────────────────────────────────────────┐
  macOS will not open this installer the usual way: it is not signed with a
  paid Apple certificate. Clearing that takes a minute, once.

  1. Save the file to your Downloads folder.
  2. Press Cmd+Space, type "Terminal", press Return.
  3. Paste this line into the Terminal window and press Return:

     xattr -c ~/Downloads/Vexflow-*.pkg && open ~/Downloads/Vexflow-*.pkg

  4. The installer opens: Continue, your Mac password, Done.

  If Terminal says "no matches found", the file is not in Downloads.
  └────────────────────────────────────────────────────────────────────────┘

  ┌─ Русский ──────────────────────────────────────────────────────────────┐
  Мак не даст открыть установщик обычным способом: он не подписан платным
  сертификатом Apple. Обходится один раз, за минуту.

  1. Сохрани файл в «Загрузки».
  2. Нажми ⌘+пробел, набери «Терминал», Enter.
  3. Вставь в окно Терминала эту строку и нажми Enter:

     xattr -c ~/Downloads/Vexflow-*.pkg && open ~/Downloads/Vexflow-*.pkg

  4. Откроется установщик: «Продолжить», пароль от мака, «Готово».

  Если Терминал ответил «no matches found» — файл лежит не в «Загрузках».
  └────────────────────────────────────────────────────────────────────────┘
EOF
printf '\n'

if [ -n "$INSTALL" ]; then
  say "Installing on this Mac (needs your password)"
  sudo installer -pkg "$PKG" -target /
fi
