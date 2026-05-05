#!/bin/sh
# Build a macOS .dmg for the Kazakh-QWERTZ keyboard layout.
#
# Usage: scripts/build-dmg.sh [VERSION]
#   VERSION defaults to "dev" if not given (used in the output filename only).
#
# Output: dist/Kazakh-QWERTZ-<VERSION>.dmg
#
# The DMG contains:
#   - Kazakh-QWERTZ.bundle      (the keyboard layout itself)
#   - Install.command           (double-click in Finder to install)
#   - README.md, LICENSE
#
# Requires macOS (uses hdiutil). Run from any directory.

set -eu

VERSION="${1:-dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
WORK="$(mktemp -d)"
STAGE="$WORK/Kazakh-QWERTZ"
DMG="$DIST/Kazakh-QWERTZ-${VERSION}.dmg"

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

if [ ! -d "$ROOT/Contents" ]; then
    echo "Error: $ROOT/Contents not found (is this the repo root?)" >&2
    exit 1
fi

mkdir -p "$STAGE/Kazakh-QWERTZ.bundle"
cp -R "$ROOT/Contents" "$STAGE/Kazakh-QWERTZ.bundle/"

# Install.command — Finder treats .command files as double-clickable shell scripts.
cat > "$STAGE/Install.command" <<'CMD'
#!/bin/sh
set -e
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="$HOME/Library/Keyboard Layouts"
BUNDLE="$DEST_DIR/Kazakh-QWERTZ.bundle"

mkdir -p "$DEST_DIR"
rm -rf "$BUNDLE"
cp -R "$SRC_DIR/Kazakh-QWERTZ.bundle" "$BUNDLE"

osascript <<'OSA' || echo "Installed: $BUNDLE"
display dialog "Kazakh-QWERTZ installed.

Next:
1. Log out and log back in (or restart).
2. System Settings → Keyboard → Input Sources → Edit → +
3. Pick Kazakh → Kazakh-QWERTZ → Add." buttons {"OK"} default button "OK" with title "Kazakh-QWERTZ"
OSA
CMD
chmod +x "$STAGE/Install.command"

cp "$ROOT/README.md" "$STAGE/"
cp "$ROOT/LICENSE" "$STAGE/"

mkdir -p "$DIST"
rm -f "$DMG"
hdiutil create \
    -volname "Kazakh-QWERTZ" \
    -srcfolder "$STAGE" \
    -ov \
    -format UDZO \
    -fs HFS+ \
    "$DMG" >/dev/null

echo "Built: $DMG"
ls -lh "$DMG"
