#!/bin/sh
# Shared by repository and packaged installers. No user configuration is sourced.
layout_error() {
    echo "Error: $*" >&2
    exit 1
}
layout_name() {
    case "$1" in
        qwertz) echo Kazakh-QWERTZ ;;
        qwerty) echo Kazakh-QWERTY ;;
        *) layout_error "Unknown layout: $1" ;;
    esac
}
layout_parse_args() {
    layout_choice=qwertz
    if [ -f "$SCRIPT_DIR/.layout-variant" ]; then
        layout_choice="$(cat "$SCRIPT_DIR/.layout-variant")"
        layout_name "$layout_choice" >/dev/null
    fi
    LAYOUT_DEST_DIR="$HOME/Library/Keyboard Layouts"
    layout_choice_seen=no
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --dest-dir)
                [ "$#" -ge 2 ] && [ -n "$2" ] || layout_error "--dest-dir requires a path"
                LAYOUT_DEST_DIR="$2"
                shift 2
                ;;
            --help|-h)
                echo "Usage: $(basename "$0") [qwertz|qwerty|both] [--dest-dir PATH]"
                echo "Default layout: $layout_choice"
                exit 0
                ;;
            qwertz|qwerty|both)
                [ "$layout_choice_seen" = no ] || layout_error "Specify only one layout choice"
                layout_choice="$1"
                layout_choice_seen=yes
                shift
                ;;
            *) layout_error "Unknown argument: $1 (expected qwertz, qwerty, or both)" ;;
        esac
    done
    # Resolve relative paths safely, including paths beginning '-'.
    case "$LAYOUT_DEST_DIR" in /*) ;; *) LAYOUT_DEST_DIR="$PWD/$LAYOUT_DEST_DIR" ;; esac
    case "$layout_choice" in
        both) LAYOUT_VARIANTS="qwertz qwerty" ;;
        *) LAYOUT_VARIANTS="$layout_choice" ;;
    esac
}
layout_source_contents() {
    layout_source_name="$(layout_name "$2")"
    if [ -d "$1/$layout_source_name.bundle/Contents" ]; then
        echo "$1/$layout_source_name.bundle/Contents"
    elif [ "$2" = qwertz ]; then
        echo "$1/Contents"
    else
        echo "$1/variants/qwerty/Contents"
    fi
}
layout_validate_contents() {
    layout_check_name="$(layout_name "$2")"
    layout_check_info="$1/Info.plist"
    layout_check_xml="$1/Resources/$layout_check_name.keylayout"
    for layout_check_file in "$layout_check_info" "$1/version.plist" "$layout_check_xml" "$1/Resources/$layout_check_name.icns"; do
        [ -f "$layout_check_file" ] && [ -s "$layout_check_file" ] || layout_error "Missing or empty source file: $layout_check_file"
    done
    /usr/bin/plutil -lint "$layout_check_info" "$1/version.plist" >/dev/null || layout_error "Invalid source metadata: $1"
    [ "$(/usr/bin/plutil -extract CFBundleName raw -o - "$layout_check_info")" = "$layout_check_name" ] || layout_error "Source bundle name does not match $layout_check_name"
    [ "$(/usr/bin/plutil -extract CFBundleIdentifier raw -o - "$layout_check_info")" = "com.asqatqazet.keyboardlayout.kazakh-$2" ] || layout_error "Source bundle identifier does not match $layout_check_name"
    # xmllint supports XML 1.0; substitute legal XML 1.1 C0 references only for
    # this syntax check. The copied .keylayout is never rewritten.
    layout_check_valid="$(sed -e 's/version="1.1"/version="1.0"/' -e 's/\&\#x00[01][0-9A-Fa-f];/ /g' "$layout_check_xml" |
        /usr/bin/xmllint --nonet --xpath "string(boolean(/keyboard[@name='$layout_check_name']/layouts/layout and /keyboard/modifierMap and /keyboard/keyMapSet/keyMap/key))" - 2>/dev/null)" || layout_error "Invalid keyboard XML: $layout_check_xml"
    [ "$layout_check_valid" = true ] || layout_error "Source keyboard structure or name does not match $layout_check_name"
}
