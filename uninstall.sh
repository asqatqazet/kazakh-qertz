#!/bin/sh
set -e

BUNDLE="$HOME/Library/Keyboard Layouts/Kazakh-QWERTZ.bundle"

if [ -d "$BUNDLE" ]; then
    rm -rf "$BUNDLE"
    echo "Uninstalled: $BUNDLE"
    echo "Remove it from System Settings -> Keyboard -> Input Sources if it still appears."
else
    echo "Not installed at $BUNDLE - nothing to do."
fi
