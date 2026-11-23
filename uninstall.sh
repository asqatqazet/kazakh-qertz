#!/bin/sh
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/scripts/layout-common.sh"
layout_parse_args "$@"
for variant in $LAYOUT_VARIANTS; do
    bundle="$LAYOUT_DEST_DIR/$(layout_name "$variant").bundle"
    if [ -L "$bundle" ] || { [ -e "$bundle" ] && [ ! -d "$bundle" ]; }; then
        layout_error "Refusing to remove a symlink or non-directory: $bundle"
    fi
done
for variant in $LAYOUT_VARIANTS; do
    bundle="$LAYOUT_DEST_DIR/$(layout_name "$variant").bundle"
    if [ -d "$bundle" ]; then
        rm -rf "$bundle"
        echo "Uninstalled: $bundle"
    else
        echo "Not installed at $bundle - nothing to do."
    fi
done
echo "Remove the uninstalled layout(s) from System Settings -> Keyboard -> Input Sources if still listed."
