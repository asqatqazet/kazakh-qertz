#!/bin/sh
# Shared argument validation for the two archive formats.
package_init() {
    [ "$#" -le 2 ] || { echo "Usage: $0 [VERSION] [qwertz|qwerty]" >&2; exit 1; }
    PACKAGE_VERSION="${1:-dev}"
    PACKAGE_VARIANT="${2:-qwertz}"
    case "$PACKAGE_VERSION" in
        ''|[.-]*|*[!a-zA-Z0-9._-]*) echo "Error: Invalid version label: $PACKAGE_VERSION" >&2; exit 1 ;;
        [0-9]*) PACKAGE_VERSION="v$PACKAGE_VERSION" ;;
    esac
    . "$ROOT/scripts/layout-common.sh"
    PACKAGE_NAME="$(layout_name "$PACKAGE_VARIANT")"
}
