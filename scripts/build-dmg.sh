#!/bin/sh
# Usage: scripts/build-dmg.sh [VERSION] [qwertz|qwerty]
# Numeric versions gain a v prefix; default output is Kazakh-QWERTZ-dev.dmg.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
. "$ROOT/scripts/package-common.sh"
package_init "$@"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
trap 'exit 1' HUP INT TERM
STAGE="$WORK/$PACKAGE_NAME"
"$ROOT/scripts/stage-package.sh" "$PACKAGE_VARIANT" "$STAGE"
mkdir -p "$ROOT/dist"
DMG="$ROOT/dist/$PACKAGE_NAME-$PACKAGE_VERSION.dmg"
hdiutil create -volname "$PACKAGE_NAME" -srcfolder "$STAGE" -ov -format UDZO -fs HFS+ "$DMG" >/dev/null
echo "Built: $DMG"
ls -lh "$DMG"
