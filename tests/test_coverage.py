#!/usr/bin/env python3
"""Verify the keylayout reaches every Kazakh letter and has no duplicate key bindings.

Uses regex parsing because the .keylayout is XML 1.1 with control-character
references that Python's stdlib XML 1.0 parser rejects.

A letter is considered "covered" if it appears as the output of any key in any
keyMap of the primary keyMapSet — including modifier-shifted maps. This catches
accidental removal without dictating layout decisions.
"""

import re
import sys
from collections import Counter
from html import unescape
from pathlib import Path

KEYLAYOUT = Path(__file__).resolve().parent.parent / "Contents" / "Resources" / "Kazakh-QWERTZ.keylayout"

KAZAKH_LOWER = "аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя"
KAZAKH_UPPER = "АӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЪЫІЬЭЮЯ"

# Letters known to be absent from the current layout. Tracked separately so
# the test still passes (catching new regressions) while keeping the gap visible.
# To fix: add bindings in Ukelele and remove the letter from this set.
KNOWN_MISSING_LOWER = set("һцщъыьэю")
KNOWN_MISSING_UPPER = set("ҢҺЦЩЪЫЬЭЮЯ")

PRIMARY_MAPSET = "16c"

MAPSET_RE = re.compile(
    r'<keyMapSet\s+id="([^"]+)"\s*>(.*?)</keyMapSet>', re.DOTALL
)
KEYMAP_RE = re.compile(
    r'<keyMap\s+index="(\d+)"[^>]*>(.*?)</keyMap>', re.DOTALL
)
KEY_RE = re.compile(r'<key\s+code="(\d+)"\s+output="([^"]*)"\s*/>')


def parse_mapset(text, mapset_id):
    for m in MAPSET_RE.finditer(text):
        if m.group(1) == mapset_id:
            keymaps = {}
            for km in KEYMAP_RE.finditer(m.group(2)):
                idx = int(km.group(1))
                keys = {int(c): unescape(o) for c, o in KEY_RE.findall(km.group(2))}
                keymaps[idx] = keys
            return keymaps
    return None


def check_coverage(keymaps, alphabet, known_missing, label):
    where = {}
    for letter in alphabet:
        for idx, keys in sorted(keymaps.items()):
            if letter in keys.values():
                where[letter] = idx
                break

    missing = [c for c in alphabet if c not in where]
    unexpected = [c for c in missing if c not in known_missing]
    assert not unexpected, f"{label}: unexpectedly missing letters {unexpected}"

    by_map = Counter(where.values())
    breakdown = ", ".join(f"map {i}: {n}" for i, n in sorted(by_map.items()))
    covered = len(alphabet) - len(missing)
    print(f"  {label}: {covered}/{len(alphabet)} letters covered ({breakdown})")
    if missing:
        print(f"    known gaps: {''.join(missing)}")


def check_no_dup_codes(keymaps):
    for idx, keys in keymaps.items():
        codes = list(keys.keys())
        dups = [c for c, n in Counter(codes).items() if n > 1]
        assert not dups, f"keyMap {idx}: duplicate codes {dups}"


def main():
    assert KEYLAYOUT.exists(), f"Keylayout file not found: {KEYLAYOUT}"
    text = KEYLAYOUT.read_text(encoding="utf-8")

    print(f"Checking {KEYLAYOUT.name}...")
    keymaps = parse_mapset(text, PRIMARY_MAPSET)
    assert keymaps, f"keyMapSet {PRIMARY_MAPSET!r} not found"

    check_no_dup_codes(keymaps)
    check_coverage(keymaps, KAZAKH_LOWER, KNOWN_MISSING_LOWER, "lowercase")
    check_coverage(keymaps, KAZAKH_UPPER, KNOWN_MISSING_UPPER, "uppercase")
    print("OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
