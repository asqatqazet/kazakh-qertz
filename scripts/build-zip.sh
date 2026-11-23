#!/bin/sh
# Usage: scripts/build-zip.sh [VERSION] [qwertz|qwerty]
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
ZIP="$ROOT/dist/$PACKAGE_NAME-$PACKAGE_VERSION.zip"
# A fresh archive avoids retaining obsolete files when rebuilding a release.
(cd "$STAGE" && zip -qr "$WORK/package.zip" .)
mv "$WORK/package.zip" "$ZIP"
echo "Built: $ZIP"
ls -lh "$ZIP"
