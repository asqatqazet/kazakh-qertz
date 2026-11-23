#!/bin/sh
# Usage: scripts/stage-package.sh qwertz|qwerty NEW_DIRECTORY
# Both release formats use this same complete, directly installable payload.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
. "$ROOT/scripts/layout-common.sh"
[ "$#" -eq 2 ] || layout_error "Usage: $0 qwertz|qwerty NEW_DIRECTORY"
variant="$1"
name="$(layout_name "$variant")"
stage="$2"
case "$stage" in /*) ;; *) stage="$PWD/$stage" ;; esac
[ ! -e "$stage" ] && [ ! -L "$stage" ] || layout_error "Package staging directory already exists: $stage"
source_contents="$(layout_source_contents "$ROOT" "$variant")"
layout_validate_contents "$source_contents" "$variant"
mkdir -p "$stage/$name.bundle" "$stage/scripts"
cp -R "$source_contents" "$stage/$name.bundle/Contents"
cp "$ROOT/install.sh" "$ROOT/uninstall.sh" "$stage/"
cp "$ROOT/scripts/layout-common.sh" "$stage/scripts/"
printf '%s\n' "$variant" > "$stage/.layout-variant"
cat > "$stage/Install.command" <<CMD
#!/bin/sh
set -eu
SCRIPT_DIR="\$(CDPATH= cd -- "\$(dirname -- "\$0")" && pwd)"
exec "\$SCRIPT_DIR/install.sh" "$variant" "\$@"
CMD
chmod +x "$stage/Install.command" "$stage/install.sh" "$stage/uninstall.sh"
cp "$ROOT/README.md" "$ROOT/README.kk.md" "$ROOT/README.zh.md" "$ROOT/RELEASE_NOTES.md" "$ROOT/LICENSE" "$stage/"
