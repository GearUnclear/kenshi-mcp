"""Key names, combo parsing, and the safety rules for what may be pressed.

One table maps each key name to its Windows set-1 scancode (Kenshi reads the
keyboard through DirectInput, which only sees scancodes), its Windows virtual-key
code and its X11 keysym.
"""

from __future__ import annotations

from dataclasses import dataclass


class BlockedInput(Exception):
    """The requested key or combo is not allowed to be sent."""


@dataclass(frozen=True)
class KeyDef:
    name: str
    scancode: int
    extended: bool
    keysym: str
    vk: int


_NAMED_VK = {
    "escape": 0x1B, "backspace": 0x08, "tab": 0x09, "enter": 0x0D, "ctrl": 0x11, "shift": 0x10,
    "alt": 0x12, "space": 0x20, "pageup": 0x21, "pagedown": 0x22, "end": 0x23, "home": 0x24,
    "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28, "insert": 0x2D, "delete": 0x2E,
    "minus": 0xBD, "equals": 0xBB, "lbracket": 0xDB, "rbracket": 0xDD, "semicolon": 0xBA,
    "apostrophe": 0xDE, "grave": 0xC0, "backslash": 0xDC, "comma": 0xBC, "period": 0xBE,
    "slash": 0xBF,
}


def _vk(name: str) -> int:
    if name in _NAMED_VK:
        return _NAMED_VK[name]
    if len(name) == 1:  # letters and digits use their upper-case ASCII code
        return ord(name.upper())
    return 0x70 + int(name[1:]) - 1  # f1..f12


def _build_table() -> dict[str, KeyDef]:
    table: dict[str, KeyDef] = {}

    def add(name: str, scancode: int, keysym: str, extended: bool = False) -> None:
        table[name] = KeyDef(name, scancode, extended, keysym, _vk(name))

    add("escape", 0x01, "Escape")
    for i, digit in enumerate("1234567890"):
        add(digit, 0x02 + i, digit)
    add("minus", 0x0C, "minus")
    add("equals", 0x0D, "equal")
    add("backspace", 0x0E, "BackSpace")
    add("tab", 0x0F, "Tab")
    for i, letter in enumerate("qwertyuiop"):
        add(letter, 0x10 + i, letter)
    add("lbracket", 0x1A, "bracketleft")
    add("rbracket", 0x1B, "bracketright")
    add("enter", 0x1C, "Return")
    add("ctrl", 0x1D, "Control_L")
    for i, letter in enumerate("asdfghjkl"):
        add(letter, 0x1E + i, letter)
    add("semicolon", 0x27, "semicolon")
    add("apostrophe", 0x28, "apostrophe")
    add("grave", 0x29, "grave")
    add("shift", 0x2A, "Shift_L")
    add("backslash", 0x2B, "backslash")
    for i, letter in enumerate("zxcvbnm"):
        add(letter, 0x2C + i, letter)
    add("comma", 0x33, "comma")
    add("period", 0x34, "period")
    add("slash", 0x35, "slash")
    add("alt", 0x38, "Alt_L")
    add("space", 0x39, "space")
    for i in range(10):
        add(f"f{i + 1}", 0x3B + i, f"F{i + 1}")
    add("f11", 0x57, "F11")
    add("f12", 0x58, "F12")
    add("home", 0x47, "Home", extended=True)
    add("up", 0x48, "Up", extended=True)
    add("pageup", 0x49, "Prior", extended=True)
    add("left", 0x4B, "Left", extended=True)
    add("right", 0x4D, "Right", extended=True)
    add("end", 0x4F, "End", extended=True)
    add("down", 0x50, "Down", extended=True)
    add("pagedown", 0x51, "Next", extended=True)
    add("insert", 0x52, "Insert", extended=True)
    add("delete", 0x53, "Delete", extended=True)
    return table


KEYS: dict[str, KeyDef] = _build_table()

MODIFIERS = ("ctrl", "shift", "alt")

_ALIASES = {
    "esc": "escape",
    "return": "enter",
    "control": "ctrl",
    "ctl": "ctrl",
    "option": "alt",
    "spacebar": "space",
    " ": "space",
    "`": "grave",
    "~": "grave",
    "tilde": "grave",
    "backtick": "grave",
    "-": "minus",
    "=": "equals",
    "equal": "equals",
    "[": "lbracket",
    "]": "rbracket",
    ";": "semicolon",
    "'": "apostrophe",
    ",": "comma",
    ".": "period",
    "/": "slash",
    "\\": "backslash",
    "pgup": "pageup",
    "page_up": "pageup",
    "pgdn": "pagedown",
    "pgdown": "pagedown",
    "page_down": "pagedown",
    "del": "delete",
    "ins": "insert",
    "bksp": "backspace",
    "arrowup": "up",
    "arrowdown": "down",
    "arrowleft": "left",
    "arrowright": "right",
}

# Keys that reach outside the game no matter what they are combined with.
_NEVER = {"super", "win", "windows", "meta", "cmd", "command"}

# Combos the operating system or window manager acts on instead of the game.
_BLOCKED_COMBOS = {
    (frozenset({"alt"}), "tab"),
    (frozenset({"alt"}), "f4"),
    (frozenset({"alt"}), "escape"),
    (frozenset({"alt"}), "space"),
    (frozenset({"alt"}), "enter"),
    (frozenset({"alt", "shift"}), "tab"),
    (frozenset({"ctrl"}), "escape"),
    (frozenset({"ctrl", "shift"}), "escape"),
    (frozenset({"ctrl", "alt"}), "delete"),
    (frozenset({"ctrl", "alt"}), "tab"),
}

# Kenshi's developer/debug shortcuts. Off unless the operator opts in.
_DEBUG_COMBOS = {
    (frozenset({"shift"}), "f12"),  # in-game world editor
    (frozenset({"ctrl", "shift"}), "f11"),  # rebuild navmesh
    (frozenset({"shift"}), "f11"),  # reload/fix stuck characters
}


def normalize_key(name: str) -> str:
    """Return the canonical name for a single key, or raise BlockedInput."""
    key = name if name == " " else name.strip().lower()
    key = _ALIASES.get(key, key)
    if key in _NEVER:
        raise BlockedInput(f"The '{name}' key is never sent: it acts on the desktop, not the game.")
    if key not in KEYS:
        raise BlockedInput(
            f"Unknown key '{name}'. Use letters, digits, f1-f12, space, enter, escape, tab, "
            "backspace, delete, insert, home, end, pageup, pagedown, arrow keys (up/down/left/right), "
            "grave, minus, equals, comma, period, slash, semicolon, apostrophe, lbracket, rbracket, "
            "backslash, or the modifiers shift/ctrl/alt."
        )
    return key


def parse_combo(combo: str) -> tuple[list[str], str]:
    """Split 'ctrl+shift+s' into (['ctrl', 'shift'], 's').

    A lone modifier ('alt') is returned as the key with no modifiers, so it can be held.
    """
    raw = combo.strip()
    if not raw:
        raise BlockedInput("Empty key.")
    parts = ["+"] if raw == "+" else [p for p in raw.split("+")]
    if any(p == "" for p in parts):
        # A trailing '+' such as 'shift++' means the plus key itself, which is shift+equals.
        raise BlockedInput(f"Could not parse key combo '{combo}'. Write combos like 'shift+f5'.")
    names = [normalize_key(p) for p in parts]
    *mods, key = names
    for mod in mods:
        if mod not in MODIFIERS:
            raise BlockedInput(
                f"In '{combo}', '{mod}' is not a modifier. Only shift, ctrl and alt can prefix a key."
            )
    if len(set(mods)) != len(mods):
        raise BlockedInput(f"Modifier repeated in '{combo}'.")
    return mods, key


def parse_modifiers(text: str | None) -> list[str]:
    """Parse a modifiers-only string such as 'shift' or 'ctrl+shift' ('' or None means none)."""
    if not text or not text.strip():
        return []
    mods = [normalize_key(p) for p in text.split("+")]
    for mod in mods:
        if mod not in MODIFIERS:
            raise BlockedInput(f"'{mod}' is not a modifier. Use shift, ctrl, alt or a '+'-joined mix.")
    if len(set(mods)) != len(mods):
        raise BlockedInput(f"Modifier repeated in '{text}'.")
    return mods


def check_allowed(mods: list[str], key: str, *, allow_debug_keys: bool = False) -> None:
    """Raise BlockedInput when a combo would act outside the game or trip a debug tool."""
    signature = (frozenset(mods), key)
    if signature in _BLOCKED_COMBOS:
        raise BlockedInput(
            f"'{'+'.join([*mods, key])}' is blocked: the operating system handles it, not Kenshi."
        )
    if signature in _DEBUG_COMBOS and not allow_debug_keys:
        raise BlockedInput(
            f"'{'+'.join([*mods, key])}' is one of Kenshi's debug shortcuts and is disabled. "
            "The operator can enable it with allow_debug_keys in the config."
        )


# Characters that can be typed on a US layout: char -> (key name, needs shift).
_SHIFTED = {
    "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "*": "8",
    "(": "9", ")": "0", "_": "minus", "+": "equals", "{": "lbracket", "}": "rbracket",
    ":": "semicolon", '"': "apostrophe", "<": "comma", ">": "period", "?": "slash",
    "|": "backslash", "~": "grave",
}
_PLAIN = {
    " ": "space", "-": "minus", "=": "equals", "[": "lbracket", "]": "rbracket",
    ";": "semicolon", "'": "apostrophe", ",": "comma", ".": "period", "/": "slash",
    "\\": "backslash", "`": "grave", "\n": "enter", "\t": "tab",
}


def char_to_key(char: str) -> tuple[str, bool]:
    """Map one typed character to (key name, shift?) on a US keyboard layout."""
    if len(char) != 1:
        raise ValueError("char_to_key takes exactly one character")
    if char in _PLAIN:
        return _PLAIN[char], False
    if char in _SHIFTED:
        return _SHIFTED[char], True
    if char.isascii() and char.isalpha():
        return char.lower(), char.isupper()
    if char.isascii() and char.isdigit():
        return char, False
    raise BlockedInput(
        f"Cannot type {char!r}: only US-keyboard ASCII characters can be typed into the game."
    )
