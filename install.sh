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

echo "Installed: $BUNDLE"
echo ""
echo "Next steps:"
echo "  1. Log out and back in (or restart your Mac)."
echo "  2. Open System Settings -> Keyboard -> Input Sources -> Edit -> +"
echo "  3. Find 'Kazakh-QWERTZ' under Kazakh and add it."
