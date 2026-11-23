#!/bin/sh
# Install one or both layouts without changing the other installed bundle.
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/scripts/layout-common.sh"
layout_parse_args "$@"

# Validate every requested source before changing any destination.
for variant in $LAYOUT_VARIANTS; do
    source_contents="$(layout_source_contents "$SCRIPT_DIR" "$variant")"
    layout_validate_contents "$source_contents" "$variant"
done
mkdir -p "$LAYOUT_DEST_DIR"
LAYOUT_DEST_DIR="$(CDPATH= cd -- "$LAYOUT_DEST_DIR" && pwd)"
WORK="$(mktemp -d "$LAYOUT_DEST_DIR/.kazakh-install.XXXXXX")"
PENDING_TARGET=""
PENDING_BACKUP=""
cleanup() {
    if [ -n "$PENDING_BACKUP" ] && [ -d "$PENDING_BACKUP" ] && [ ! -e "$PENDING_TARGET" ]; then
        mv "$PENDING_BACKUP" "$PENDING_TARGET" || {
            echo "Error: recovery copy retained at $PENDING_BACKUP" >&2
            return
        }
    fi
    rm -rf "$WORK"
}
trap cleanup EXIT
trap 'exit 1' HUP INT TERM

# Stage all copies first; an interrupted copy cannot damage an installed layout.
for variant in $LAYOUT_VARIANTS; do
    name="$(layout_name "$variant")"
    target="$LAYOUT_DEST_DIR/$name.bundle"
    if [ -L "$target" ] || { [ -e "$target" ] && [ ! -d "$target" ]; }; then
        layout_error "Refusing to replace a symlink or non-directory: $target"
    fi
    mkdir "$WORK/$name.bundle"
    cp -R "$(layout_source_contents "$SCRIPT_DIR" "$variant")" "$WORK/$name.bundle/Contents"
    layout_validate_contents "$WORK/$name.bundle/Contents" "$variant"
done
for variant in $LAYOUT_VARIANTS; do
    name="$(layout_name "$variant")"
    PENDING_TARGET="$LAYOUT_DEST_DIR/$name.bundle"
    PENDING_BACKUP="$WORK/previous-$name.bundle"
    if [ -d "$PENDING_TARGET" ]; then
        mv "$PENDING_TARGET" "$PENDING_BACKUP"
    fi
    mv "$WORK/$name.bundle" "$PENDING_TARGET"
    PENDING_BACKUP=""
    echo "Installed: $PENDING_TARGET"
done
echo ""
echo "Next steps:"
echo "  1. Log out and back in (or restart your Mac)."
echo "  2. Open System Settings -> Keyboard -> Input Sources -> Edit -> +"
echo "  3. Add the installed Kazakh layout(s) under Kazakh."
