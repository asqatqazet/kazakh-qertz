#!/bin/sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="$HOME/Library/Keyboard Layouts"
BUNDLE="$DEST_DIR/Kazakh-QWERTZ.bundle"

if [ ! -d "$SCRIPT_DIR/Contents" ]; then
    echo "Error: Contents/ not found next to install.sh" >&2
    exit 1
fi

mkdir -p "$DEST_DIR"
rm -rf "$BUNDLE"
mkdir -p "$BUNDLE"
cp -R "$SCRIPT_DIR/Contents" "$BUNDLE/"

# Force the user's preferences daemon to rescan keyboard layouts so the new
# bundle shows up immediately in System Settings -> Input Sources, with no
# logout required. cfprefsd is per-user, auto-respawns, no sudo needed.
killall cfprefsd 2>/dev/null || true

echo "Installed: $BUNDLE"
echo ""
echo "Next steps:"
echo "  1. Open System Settings -> Keyboard -> Input Sources -> Edit -> +"
echo "  2. Find 'Kazakh-QWERTZ' under Kazakh and add it."
echo ""
echo "If it doesn't appear, log out and back in once - that always works."
