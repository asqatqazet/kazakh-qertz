#!/usr/bin/env python3
"""Check modifier-selected output for every declared hardware layout.

Uses only Python's standard library. These are static XML checks, not a
substitute for typing in macOS applications. Run: python3 tests/test_coverage.py
"""

from __future__ import annotations

import copy
import itertools
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

KEYLAYOUT = Path(__file__).resolve().parent.parent / "Contents" / "Resources" / "Kazakh-QWERTZ.keylayout"
KAZAKH_LOWER = "аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя"
KAZAKH_UPPER = KAZAKH_LOWER.upper()

# Physical US labels identify positions independently of the XML map indices.
KEY_CODES = {
    "A": 0, "S": 1, "D": 2, "F": 3, "H": 4, "G": 5,
    "Z": 6, "X": 7, "C": 8, "V": 9, "B": 11,
    "Q": 12, "W": 13, "E": 14, "R": 15, "Y": 16, "T": 17,
    "1": 18, "2": 19, "3": 20, "4": 21, "6": 22, "5": 23,
    "=": 24, "9": 25, "7": 26, "-": 27, "8": 28, "0": 29,
    "]": 30, "O": 31, "U": 32, "[": 33, "I": 34, "P": 35,
    "L": 37, "J": 38, "'": 39, "K": 40, ";": 41, "\\": 42,
    ",": 43, "/": 44, "N": 45, "M": 46, ".": 47, "`": 50,
}
BASE_LETTERS = dict(zip(
    "QWERTYUIOP[]ASDFGHJKL;'\\ZXCVBNM`",
    "ғуертзұіопүяасдыгқжклөәхишңвбнмй",
))
BASE = {key: BASE_LETTERS.get(key, key) for key in KEY_CODES}
SHIFT_PUNCTUATION = dict(zip("1234567890-=,./", '!@#$%^&*()_+":?'))
OPTION = {
    **BASE, **dict(zip("FHCXEOWJBV", "фһцщэёючьъ")),
    "`": "`", "[": "[", "]": "]", ";": ";", "'": "'", "\\": "\\",
    ",": "«", ".": "…", "-": "–", "=": "≠", "3": "№", "4": "₸",
}
OPTION_SHIFT_PUNCTUATION = {
    "`": "~", "[": "{", "]": "}", ";": ":", "'": '"', "\\": "|",
    ",": "»", "-": "—", "=": "±", "/": "?",
}
MODIFIER_BITS = ("shift", "rightShift", "caps", "option", "rightOption", "command", "control", "rightControl")
MODIFIER_GROUPS = {
    **{key: (key,) for key in MODIFIER_BITS},
    "anyShift": ("shift", "rightShift"),
    "anyOption": ("option", "rightOption"),
    "anyControl": ("control", "rightControl"),
}
ALL_MODIFIERS = tuple(
    frozenset(key for key, pressed in zip(MODIFIER_BITS, bits) if pressed)
    for bits in itertools.product((False, True), repeat=len(MODIFIER_BITS))
)
JIS_TYPES = {18, 21, 22, 23, 30, 194, 197, 200, 201, 206, 207}


class LayoutError(ValueError):
    """Invalid/unsupported keylayout or failed output contract."""


def require(condition, message):
    if not condition:
        raise LayoutError(message)


def attributes(element, required, optional=()):
    require(set(required) <= element.attrib.keys(), f"<{element.tag}> missing required attributes {required}")
    unknown = element.attrib.keys() - set(required) - set(optional)
    require(not unknown, f"Unsupported <{element.tag}> attributes: {sorted(unknown)}")


def parse_xml(text):
    """Protect XML 1.1 control references from XML 1.0 parsing, then restore.

    HTML unescape is unsuitable because it can delete control characters.
    ElementTree does not fetch the external keyboard DTD.
    """
    replacements = {}
    next_marker = 0xF0000

    def protect(match):
        nonlocal next_marker
        value = match.group(1)
        code = int(value[1:], 16) if value.startswith("x") else int(value)
        require(0 < code <= 0x10FFFF and not 0xD800 <= code <= 0xDFFF,
                f"Invalid XML character reference: {match.group(0)}")
        if code in (9, 10, 13) or code >= 32:
            return match.group(0)
        while chr(next_marker) in text or chr(next_marker) in replacements:
            next_marker += 1
        marker = chr(next_marker)
        replacements[marker] = chr(code)
        return marker

    sanitized = re.sub(r"&#(x[0-9A-Fa-f]+|[0-9]+);", protect, text)
    try:
        root = ET.fromstring(sanitized)
    except ET.ParseError as error:
        raise LayoutError(f"Invalid XML: {error}") from error
    translation = str.maketrans(replacements)
    for element in root.iter():
        element.attrib.update({key: value.translate(translation) for key, value in element.attrib.items()})
    return root


def modifier_masks(specification):
    """Expand Apple's required/optional and any-left-or-right grammar."""
    masks = {frozenset()}
    used = set()
    for token in specification.split():
        optional = token.endswith("?")
        name = token[:-1] if optional else token
        require(name in MODIFIER_GROUPS, f"Unsupported modifier token: {token}")
        group = MODIFIER_GROUPS[name]
        require(not used.intersection(group), f"Overlapping modifier tokens: {specification}")
        used.update(group)
        choices = [frozenset(key for key, on in zip(group, bits) if on)
                   for bits in itertools.product((False, True), repeat=len(group))
                   if optional or any(bits)]
        masks = {before | choice for before in masks for choice in choices}
    return masks


@dataclass(frozen=True)
class HardwareLayout:
    first: int
    last: int
    map_set: str
    modifier_map: str

    @property
    def label(self):
        return f"hardware {self.first}–{self.last} ({self.map_set})"

    @property
    def is_jis(self):
        return bool(JIS_TYPES.intersection(range(self.first, self.last + 1)))


class Keyboard:
    def __init__(self, root):
        self.root, self.layouts, self.modifiers, self.maps, self._resolved = root, [], {}, {}, {}
        require(root.tag == "keyboard", "Expected <keyboard> root")
        attributes(root, ("group", "id", "name", "maxout"))
        allowed = {"layouts", "modifierMap", "keyMapSet", "actions"}
        require(all(element.tag in allowed for element in root), "Unsupported keyboard construct (for example, dead-key terminators)")
        require(len(root.findall("layouts")) == 1, "Expected exactly one <layouts>")
        actions = self._actions(root)
        for element in root.find("layouts"):
            require(element.tag == "layout", "Unsupported <layouts> child")
            attributes(element, ("first", "last", "mapSet", "modifiers"))
            layout = HardwareLayout(int(element.get("first")), int(element.get("last")), element.get("mapSet"), element.get("modifiers"))
            require(0 <= layout.first <= layout.last, f"Invalid hardware range: {layout.label}")
            require(all(layout.last < other.first or other.last < layout.first for other in self.layouts), "Overlapping hardware ranges")
            self.layouts.append(layout)
        require(self.layouts, "No declared hardware layouts")
        for element in root.findall("modifierMap"):
            attributes(element, ("id", "defaultIndex"))
            name = element.get("id")
            require(name not in self.modifiers, f"Duplicate modifierMap {name}")
            rules = []
            for selection in element:
                require(selection.tag == "keyMapSelect", "Unsupported modifierMap child")
                attributes(selection, ("mapIndex",))
                for rule in selection:
                    require(rule.tag == "modifier", "Unsupported keyMapSelect child")
                    attributes(rule, ("keys",))
                    rules.append((modifier_masks(rule.get("keys")), int(selection.get("mapIndex"))))
            self.modifiers[name] = (int(element.get("defaultIndex")), rules)
        seen_sets = set()
        for element in root.findall("keyMapSet"):
            attributes(element, ("id",))
            name = element.get("id")
            require(name not in seen_sets, f"Duplicate keyMapSet {name}")
            seen_sets.add(name)
            for key_map in element:
                require(key_map.tag == "keyMap", "Unsupported keyMapSet child")
                attributes(key_map, ("index",), ("baseMapSet", "baseIndex"))
                identity = (name, int(key_map.get("index")))
                require(identity not in self.maps, f"Duplicate keyMap {identity}")
                base = key_map.get("baseMapSet")
                require((base is None) == (key_map.get("baseIndex") is None), f"Incomplete inheritance in {identity}")
                parent = None if base is None else (base, int(key_map.get("baseIndex")))
                keys = {}
                for key in key_map:
                    require(key.tag == "key", f"Unsupported keyMap child in {identity}")
                    attributes(key, ("code",), ("output", "action"))
                    code = int(key.get("code"))
                    require(code not in keys, f"Duplicate key code {code} in {identity}")
                    require(("output" in key.attrib) != ("action" in key.attrib), f"Key {code} needs exactly one output/action")
                    require(not list(key), f"Unsupported inline key action at {identity}/{code}")
                    if "action" in key.attrib:
                        action = key.get("action")
                        require(action in actions, f"Undefined action {action}")
                        keys[code] = actions[action]
                    else:
                        keys[code] = key.get("output")
                self.maps[identity] = (parent, keys)
        for identity in self.maps:
            self.effective_map(identity)
        for layout in self.layouts:
            require(layout.modifier_map in self.modifiers, f"Undefined modifierMap in {layout.label}")
            default, rules = self.modifiers[layout.modifier_map]
            for index in {default, *(index for _, index in rules)}:
                require((layout.map_set, index) in self.maps, f"Undefined selected map {layout.map_set}/{index}")

    @classmethod
    def from_text(cls, text):
        return cls(parse_xml(text))

    @staticmethod
    def _actions(root):
        result = {}
        require(len(root.findall("actions")) <= 1, "Duplicate <actions>")
        for container in root.findall("actions"):
            for action in container:
                require(action.tag == "action", "Unsupported actions child")
                attributes(action, ("id",))
                name = action.get("id")
                require(name not in result, f"Duplicate action {name}")
                conditions = list(action)
                require(len(conditions) == 1 and conditions[0].tag == "when", f"Unsupported contextual action {name}")
                condition = conditions[0]
                attributes(condition, ("state", "output"))
                require(condition.get("state") == "none", f"Unsupported dead-key state in action {name}")
                result[name] = condition.get("output")
        return result

    def effective_map(self, identity, visiting=frozenset()):
        if identity in self._resolved:
            return self._resolved[identity]
        require(identity not in visiting, f"Inheritance cycle at {identity}")
        require(identity in self.maps, f"Undefined inherited map {identity}")
        parent, local = self.maps[identity]
        inherited = {} if parent is None else self.effective_map(parent, visiting | {identity})
        self._resolved[identity] = {**inherited, **local}
        return self._resolved[identity]

    def select(self, layout, modifiers):
        selected, rules = self.modifiers[layout.modifier_map]
        # Apple TN2056: a later matching keyMapSelect takes precedence.
        for masks, index in rules:
            if modifiers in masks:
                selected = index
        return selected

    def outputs(self, layout, modifiers=frozenset()):
        return self.effective_map((layout.map_set, self.select(layout, modifiers)))


def expected_text(modifiers):
    shifted = bool(modifiers.intersection(("shift", "rightShift")))
    option = bool(modifiers.intersection(("option", "rightOption")))
    expected = dict(OPTION if option else BASE)
    if shifted or "caps" in modifiers:
        expected = {key: value.upper() if value in KAZAKH_LOWER else value for key, value in expected.items()}
    if shifted:
        expected.update(OPTION_SHIFT_PUNCTUATION if option else SHIFT_PUNCTUATION)
    return expected


def check_layout(keyboard):
    require(len(KEY_CODES) == 47 and len(BASE_LETTERS) == 32, "Invalid test key-position fixture")
    for layout in keyboard.layouts:
        for modifiers in ALL_MODIFIERS:
            actual = keyboard.outputs(layout, modifiers)
            label = f"{layout.label}, modifiers={','.join(sorted(modifiers)) or 'none'}"
            if modifiers.intersection(("control", "rightControl")):
                expected = {key: chr(ord(key.lower()) - 96) for key in KEY_CODES if key.isalpha()}
            elif "command" in modifiers:
                expected = {key: key.lower() for key in KEY_CODES if key.isalpha()}
            else:
                expected = expected_text(modifiers)
            for key, value in expected.items():
                require(actual.get(KEY_CODES[key]) == value,
                        f"{label}, physical {key}: expected {value!r}, got {actual.get(KEY_CODES[key])!r}")
            if not modifiers.intersection(("control", "rightControl", "command")):
                for code, value in {36: "\r", 48: "\t", 49: " ", 51: "\b", 53: "\x1b"}.items():
                    require(actual.get(code) == value, f"{label}: control/space key {code} changed")
                if layout.is_jis:
                    option = bool(modifiers.intersection(("option", "rightOption")))
                    shift = bool(modifiers.intersection(("shift", "rightShift")))
                    upper = shift or "caps" in modifiers
                    extras = {93: ("|" if shift else "\\") if option else ("Й" if upper else "й"),
                              94: ("~" if shift else "`") if option else "_", 95: ",", 102: " ", 104: " "}
                    for code, value in extras.items():
                        require(actual.get(code) == value, f"{label}: JIS extra key {code} expected {value!r}, got {actual.get(code)!r}")
        for name, modifiers, alphabet in (
            ("lowercase", frozenset(), KAZAKH_LOWER),
            ("Shift uppercase", frozenset({"shift"}), KAZAKH_UPPER),
            ("Caps uppercase", frozenset({"caps"}), KAZAKH_UPPER),
            ("Shift+Caps uppercase", frozenset({"shift", "caps"}), KAZAKH_UPPER),
        ):
            available = set()
            for layer in (modifiers, modifiers | {"option"}):
                outputs = keyboard.outputs(layout, layer)
                available.update(outputs.get(code) for code in KEY_CODES.values())
            missing = set(alphabet) - available
            require(not missing, f"{layout.label}: missing {name} letters {''.join(sorted(missing))}")
        check_words(keyboard, layout)


def check_words(keyboard, layout):
    # Fixed strokes cover all ten Option letters and returning to the base layer.
    recipes = (
        ("Қазақстан", "^H A Y A H S T A N"), ("қазақтың", "H A Y A H T F C"),
        ("жұмыс", "J U M F S"), ("әке", "' K E"), ("өрік", "; R I K"),
        ("үлгі", "[ L G I"), ("қаһарман", "H A @H A R M A N"),
        ("фильм", "@F Z L @B M"), ("объект", "O B @V E K T"),
        ("щётка", "@X @O T K A"), ("цирк", "@C Z R K"),
        ("юань", "@W A N @B"), ("экран", "@E K R A N"),
        ("аяқ", "A ] H"), ("чех", "@J E \\"),
    )
    for word, recipe in recipes:
        typed = []
        for stroke in recipe.split():
            modifiers = frozenset({"option"}) if stroke.startswith("@") else frozenset({"shift"}) if stroke.startswith("^") else frozenset()
            typed.append(keyboard.outputs(layout, modifiers).get(KEY_CODES[stroke.lstrip("@^")], ""))
        require("".join(typed) == word, f"{layout.label}: sample {word!r} produced {''.join(typed)!r}")


def check_validator_regressions(keyboard):
    """Prove that previously hidden defects fail, without modifying any files."""
    main_layout = keyboard.layouts[0]
    jis_layout = next(layout for layout in keyboard.layouts if layout.is_jis)

    def selected_element(root, layout, modifiers=frozenset()):
        index = keyboard.select(layout, modifiers)
        return root.find(f"./keyMapSet[@id='{layout.map_set}']/keyMap[@index='{index}']")

    def must_fail(root, expected):
        try:
            check_layout(Keyboard(root))
        except LayoutError as error:
            require(expected in str(error), f"Regression failed for the wrong reason: {error}")
        else:
            raise LayoutError(f"Validator missed regression: {expected}")

    duplicate = copy.deepcopy(keyboard.root)
    normal_map = selected_element(duplicate, main_layout)
    normal_map.append(copy.deepcopy(normal_map.find("key")))
    must_fail(duplicate, "Duplicate key code")

    hardware_override = copy.deepcopy(keyboard.root)
    hardware_map = selected_element(hardware_override, jis_layout)
    old = hardware_map.find("key[@code='39']")
    if old is not None:
        hardware_map.remove(old)
    ET.SubElement(hardware_map, "key", code="39", output=":")
    must_fail(hardware_override, "physical '")

    wrong_caps = copy.deepcopy(keyboard.root)
    caps_map = selected_element(wrong_caps, main_layout, frozenset({"caps"}))
    old = caps_map.find("key[@code='0']")
    if old is not None:
        caps_map.remove(old)
    ET.SubElement(caps_map, "key", code="0", output="A")
    must_fail(wrong_caps, "physical A")


def main():
    keyboard = Keyboard.from_text(KEYLAYOUT.read_text(encoding="utf-8"))
    check_layout(keyboard)
    check_validator_regressions(keyboard)
    profiles = {(layout.map_set, layout.modifier_map) for layout in keyboard.layouts}
    print(f"OK: 42/42 lowercase and uppercase letters across {len(keyboard.layouts)} hardware routes ({len(profiles)} effective profiles).")
    print(f"Checked {len(ALL_MODIFIERS)} modifier combinations per route, punctuation, JIS extras, shortcuts, and sample words.")
    print("Regression checks rejected duplicate keys, a hardware override, and incorrect Caps Lock output.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
