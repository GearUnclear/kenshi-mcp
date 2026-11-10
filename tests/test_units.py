"""Keys, imaging, config and the Win32 structures (checked on any platform)."""

from __future__ import annotations

import ctypes
import re
from pathlib import Path

import pytest
from PIL import Image

from kenshi_link import imaging
from kenshi_link.backends import _win_structs as ws
from kenshi_link.config import DEFAULT_KEYMAP, Config, load_config
from kenshi_link.controller import ControlError, read_notes, write_notes
from kenshi_link.keys import (
    KEYS,
    BlockedInput,
    char_to_key,
    check_allowed,
    check_modifiers,
    layout_strokes,
    parse_combo,
    parse_modifiers,
)

# ---- keys ----------------------------------------------------------------------


def test_combo_parsing_and_aliases():
    assert parse_combo("Ctrl+Shift+S") == (["ctrl", "shift"], "s")
    assert parse_combo("esc") == ([], "escape")
    assert parse_combo("`") == ([], "grave")
    assert parse_combo("alt") == ([], "alt")
    assert parse_modifiers("") == [] and parse_modifiers("shift+ctrl") == ["shift", "ctrl"]


@pytest.mark.parametrize("combo", ["win", "super+d", "cmd+q", "a+b", "shift+shift+a", "", "nosuchkey", "ctrl+"])
def test_bad_combos_are_rejected(combo):
    with pytest.raises(BlockedInput):
        parse_combo(combo)


def test_os_level_and_debug_combos_are_blocked():
    for combo in ("alt+tab", "alt+f4", "ctrl+escape", "ctrl+alt+delete", "alt+enter"):
        with pytest.raises(BlockedInput):
            check_allowed(*parse_combo(combo))
    with pytest.raises(BlockedInput, match="debug"):
        check_allowed(*parse_combo("shift+f12"))
    check_allowed(*parse_combo("shift+f12"), allow_debug_keys=True)
    check_allowed(*parse_combo("f5"))


@pytest.mark.parametrize(
    "combo",
    ["ctrl+alt+f4", "shift+alt+f4", "ctrl+shift+alt+f4", "alt+shift+escape", "ctrl+alt+shift+tab",
     "ctrl+alt+tab", "shift+alt+space", "ctrl+alt+enter", "ctrl+shift+escape", "ctrl+alt+escape",
     "ctrl+shift+alt+delete"],
)
def test_an_extra_modifier_does_not_get_a_system_combo_through(combo):
    with pytest.raises(BlockedInput, match="operating system"):
        check_allowed(*parse_combo(combo), allow_debug_keys=True, allow_shift_tab=True)


def test_modifier_chords_that_switch_the_keyboard_layout_are_blocked():
    for combo in ("alt+shift", "shift+alt", "ctrl+shift", "shift+ctrl", "ctrl+alt+shift"):
        with pytest.raises(BlockedInput, match="keyboard layout"):
            check_allowed(*parse_combo(combo))
    for modifiers in (["alt", "shift"], ["shift", "ctrl"], ["ctrl", "alt", "shift"]):
        with pytest.raises(BlockedInput, match="keyboard layout"):
            check_modifiers(modifiers)  # held during a click
    for harmless in (["shift"], ["ctrl"], ["alt"], ["ctrl", "alt"], []):
        check_modifiers(harmless)
    for combo in ("shift", "alt", "ctrl+alt", "ctrl+shift+s", "alt+shift+a"):  # a real key in the combo is fine
        check_allowed(*parse_combo(combo))


def test_the_steam_overlay_key_and_debug_keys_need_the_operator_to_opt_in():
    for combo in ("shift+tab", "ctrl+shift+tab"):
        with pytest.raises(BlockedInput, match="Steam overlay"):
            check_allowed(*parse_combo(combo))
        check_allowed(*parse_combo(combo), allow_shift_tab=True)
    check_allowed(*parse_combo("tab"))
    for combo in ("shift+f11", "ctrl+shift+f11", "shift+f12", "ctrl+shift+f12", "alt+shift+f12"):
        with pytest.raises(BlockedInput, match="debug"):
            check_allowed(*parse_combo(combo))
        check_allowed(*parse_combo(combo), allow_debug_keys=True)
    check_allowed(*parse_combo("f11"))
    check_allowed(*parse_combo("ctrl+f12"))


def test_key_table_is_consistent():
    assert KEYS["space"].scancode == 0x39 and KEYS["space"].vk == 0x20
    assert KEYS["f2"].scancode == 0x3C and KEYS["f2"].vk == 0x71 and KEYS["f2"].keysym == "F2"
    assert KEYS["f12"].scancode == 0x58 and KEYS["f12"].vk == 0x7B
    assert KEYS["w"].scancode == 0x11 and KEYS["w"].vk == ord("W")
    assert KEYS["up"].extended and not KEYS["w"].extended
    assert len({k.scancode for k in KEYS.values() if not k.extended}) == sum(not k.extended for k in KEYS.values())
    for combo in DEFAULT_KEYMAP.values():
        parse_combo(combo)


def test_typing_map():
    assert char_to_key("a") == ("a", False) and char_to_key("A") == ("a", True)
    assert char_to_key("!") == ("1", True) and char_to_key(" ") == ("space", False)
    with pytest.raises(BlockedInput):
        char_to_key("ß")


SHIFT, CTRL_ALT = 1, 6  # modifier bits as VkKeyScanEx reports them; Ctrl+Alt is AltGr


def us_layout(char: str):
    name, shift = char_to_key(char)
    return KEYS[name].scancode, SHIFT if shift else 0, False


def french_layout(char: str):
    """A few keys of the French AZERTY layout, as Windows describes it."""
    table = {
        "a": (0x10, 0), "q": (0x1E, 0), "z": (0x11, 0), "w": (0x2C, 0), "m": (0x27, 0),
        "A": (0x10, SHIFT), "M": (0x27, SHIFT), "1": (0x02, SHIFT), "&": (0x02, 0),
        ",": (0x32, 0), "?": (0x32, SHIFT), ".": (0x33, SHIFT), "!": (0x35, 0),
        "@": (0x0B, CTRL_ALT), "[": (0x06, CTRL_ALT), "<": (0x56, 0),
    }
    if char == "^":
        return 0x1A, 0, True  # a dead key: nothing appears until the next key
    if char in table:
        return (*table[char], False)
    return us_layout(char) if char.isalpha() else None


def test_typing_follows_the_keyboard_layout():
    text = "Camp-1 [x]\n\t!"
    assert layout_strokes(text, us_layout) == [char_to_key(char) for char in text]
    # On AZERTY "a" is where a US keyboard has Q, "m" where it has the semicolon, and the
    # digits need Shift. Space, Enter and Tab are the same keys everywhere.
    assert layout_strokes("Cam 1\n", french_layout) == [
        ("c", True), ("q", False), ("semicolon", False), ("space", False), ("1", True), ("enter", False),
    ]
    assert layout_strokes("zw,?.!", french_layout) == [
        ("w", False), ("z", False), ("m", False), ("m", True), ("comma", True), ("slash", False),
    ]


@pytest.mark.parametrize(
    ("char", "why"),
    [("@", "AltGr"), ("[", "AltGr"), ("^", "dead key"), ("<", "no name here"), ("#", "no key for it")],
    ids=["altgr", "altgr-bracket", "dead-key", "a-key-with-no-us-name", "not-on-the-layout"],
)
def test_characters_the_layout_cannot_give_plainly_are_refused(char, why):
    with pytest.raises(BlockedInput, match=why):
        layout_strokes(f"a{char}", french_layout)
    with pytest.raises(BlockedInput, match="US-keyboard"):
        layout_strokes("\u00e9", french_layout)  # the tool types ASCII only, whatever the layout has


# ---- imaging -------------------------------------------------------------------


def test_fit_scales_down_only_and_round_trips_coordinates():
    fit = imaging.fit(1920, 1080, 1280)
    assert (fit.width, fit.height) == (1280, 720)
    assert fit.to_window(640, 360) == (960, 540)
    assert fit.to_image(960, 540) == (640, 360)
    small = imaging.fit(800, 600, 1280)
    assert (small.width, small.height, small.scale) == (800, 600, 1.0)


def test_fit_respects_the_api_image_limits():
    fit = imaging.fit(5120, 1440, 2576)
    assert max(fit.width, fit.height) <= imaging.API_MAX_LONG_EDGE
    assert imaging.visual_tokens(fit.width, fit.height) <= imaging.API_MAX_VISUAL_TOKENS
    square = imaging.fit(2500, 2500, 2576)
    assert imaging.visual_tokens(square.width, square.height) <= imaging.API_MAX_VISUAL_TOKENS


def test_motion_fraction_detects_small_changes_and_ignores_none():
    base = Image.new("RGB", (1920, 1080), (40, 40, 40))
    assert imaging.motion_fraction(base, base.copy()) == 0.0
    changed = base.copy()
    changed.paste((200, 200, 200), (900, 500, 930, 540))  # one small figure moved
    assert imaging.motion_fraction(base, changed) > 0.0001
    assert imaging.motion_fraction(base, Image.new("RGB", (10, 10))) == 1.0


def test_encoding_and_filmstrip():
    image = Image.new("RGB", (320, 180), (10, 20, 30))
    data, fmt = imaging.encode(image, "jpeg", 80)
    assert fmt == "jpeg" and data[:2] == b"\xff\xd8"
    data, fmt = imaging.encode(image, "png")
    assert fmt == "png" and data[:4] == b"\x89PNG"
    strip = imaging.filmstrip([image, image, image], height=90)
    assert strip.size == (160 * 3 + 8, 90)
    assert imaging.filmstrip([]) is None


# ---- Win32 structures ----------------------------------------------------------


@pytest.mark.skipif(ctypes.sizeof(ctypes.c_void_p) != 8, reason="64-bit layout")
def test_input_struct_matches_the_win64_layout():
    assert ctypes.sizeof(ws.MOUSEINPUT) == 32
    assert ctypes.sizeof(ws.KEYBDINPUT) == 24
    assert ctypes.sizeof(ws.INPUT) == 40
    assert ws.INPUT.mi.offset == 8


def test_key_and_mouse_events_are_built_correctly():
    down = ws.key_input(0x48, True, True, 0x26)
    assert down.type == ws.INPUT_KEYBOARD and down.ki.wScan == 0x48 and down.ki.wVk == 0x26
    assert down.ki.dwFlags == ws.KEYEVENTF_SCANCODE | ws.KEYEVENTF_EXTENDEDKEY
    up = ws.key_input(0x39, False, False, 0x20)
    assert up.ki.dwFlags == ws.KEYEVENTF_SCANCODE | ws.KEYEVENTF_KEYUP
    wheel = ws.mouse_input(0, 0, -120, ws.MOUSEEVENTF_WHEEL)
    assert wheel.mi.mouseData == 0xFFFFFF88


def windows_pixel(value: int, size: int) -> int:
    """How Windows (per AutoHotkey's source) and Wine turn 0..65535 back into a pixel."""
    return value * size >> 16


@pytest.mark.parametrize(
    "virtual",
    [(0, 0, 1920, 1080), (0, 0, 3840, 2160), (0, 0, 2560, 1440), (0, 0, 1366, 768), (0, 0, 1280, 800),
     (-1920, 0, 3840, 1080), (-2560, -1440, 6400, 2520)],  # the last two: monitors left of and above the primary
)
def test_absolute_coordinates_land_on_every_pixel_of_the_virtual_desktop(virtual):
    left, top, width, height = virtual
    for x in range(left, left + width):
        value = ws.absolute_coords(x, top, virtual)[0]
        assert 0 <= value <= 65535 and left + windows_pixel(value, width) == x
    for y in range(top, top + height):
        value = ws.absolute_coords(left, y, virtual)[1]
        assert 0 <= value <= 65535 and top + windows_pixel(value, height) == y


def test_absolute_coordinates_near_the_corner_do_not_fall_short():
    # The formula this replaced, round(x * 65535 / (width - 1)), put pixel 3 of a 1920-wide
    # desktop at pixel 2: inside the corner the operator uses to stop everything.
    assert windows_pixel(round(3 * 65535 / 1919), 1920) == 2
    assert windows_pixel(ws.absolute_coords(3, 3, (0, 0, 1920, 1080))[0], 1920) == 3


def test_the_failsafe_corner_is_where_a_mouse_pushed_up_and_left_ends_up():
    assert ws.top_left_corner([(0, 0, 1920, 1080)]) == (0, 0)
    assert ws.top_left_corner([(0, 0, 1920, 1080), (1920, 0, 3840, 1080)]) == (0, 0)
    # A monitor to the left: (0, 0) is now mid-desktop and the pointer slides past it.
    assert ws.top_left_corner([(0, 0, 1920, 1080), (-1920, 0, 0, 1080)]) == (-1920, 0)
    assert ws.top_left_corner([(0, 0, 1920, 1080), (-1280, 300, 0, 1324)]) == (-1280, 300)
    assert ws.top_left_corner([(0, 0, 1920, 1080), (0, -1080, 1920, 0)]) == (0, -1080)  # one above
    assert ws.top_left_corner([]) == (0, 0)


def test_elevation_mismatch_is_reported_only_when_the_game_outranks_us():
    assert ws.elevation_problem(False, False) is None
    assert ws.elevation_problem(True, True) is None and ws.elevation_problem(True, False) is None
    assert "is running as administrator" in ws.elevation_problem(False, True)
    # Windows refusing to say, to a program that is not elevated, is itself the sign.
    assert "appears to be running as administrator" in ws.elevation_problem(False, None)
    assert ws.elevation_problem(True, None) is None and ws.elevation_problem(None, None) is None
    assert ws.elevation_problem(None, True) is None  # our own level unknown: claim nothing


# ---- config and notes ----------------------------------------------------------


def test_config_file_and_environment_overrides(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text('max_long_edge = 1600\nauto_focus = false\n[keymap]\ninventory = "k"\n')
    config = load_config(path, env={"KENSHI_LINK_BACKEND": "mock", "KENSHI_LINK_HOME": str(tmp_path / "h")})
    assert config.max_long_edge == 1600 and config.auto_focus is False
    assert config.keymap["inventory"] == "k" and config.keymap["map"] == "m"
    assert config.backend == "mock" and config.data_dir == tmp_path / "h"


def test_config_rejects_unknown_settings_and_unsafe_keymaps(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("no_such_setting = 1\n")
    with pytest.raises(ValueError, match="unknown setting"):
        load_config(path, env={})
    path.write_text('[keymap]\nquick_save = "alt+f4"\n')
    with pytest.raises(ValueError, match="not usable"):
        load_config(path, env={})
    with pytest.raises(ValueError):
        Config(backend="playstation").validate()


def test_the_example_config_names_real_settings_and_shows_their_defaults(tmp_path):
    example = Path(__file__).resolve().parent.parent / "config.example.toml"
    # Every setting in it is commented out as "# name = value": switch them all on.
    text = re.sub(r"(?m)^# (\w+ = .*)$", r"\1", example.read_text(encoding="utf-8"))
    assert text.count("\n[keymap]\n") == 1
    path = tmp_path / "config.toml"
    path.write_text(text, encoding="utf-8")
    config, defaults = load_config(path, env={}), Config()
    shown = set(re.findall(r"(?m)^(\w+) = ", text.split("[keymap]")[0]))
    assert {"pointer_dwell_seconds", "modifier_gap_seconds", "click_hold_seconds", "key_hold_seconds",
            "halt_poll_seconds", "allow_shift_tab"} <= shown
    for name in shown:
        assert getattr(config, name) == getattr(defaults, name), name
    assert config.keymap == DEFAULT_KEYMAP


def test_new_timing_and_safety_settings_have_defaults_and_can_be_set(tmp_path):
    defaults = Config()
    assert (defaults.click_hold_seconds, defaults.key_hold_seconds) == (0.1, 0.1)
    assert (defaults.pointer_dwell_seconds, defaults.modifier_gap_seconds) == (0.12, 0.12)
    assert defaults.halt_poll_seconds == 0.1 and defaults.allow_shift_tab is False
    path = tmp_path / "config.toml"
    path.write_text("pointer_dwell_seconds = 0.2\nmodifier_gap_seconds = 0\nallow_shift_tab = true\n"
                    '[keymap]\nprevious_squad = "shift+tab"\n')
    config = load_config(path, env={"KENSHI_LINK_HALT_POLL_SECONDS": "0.05", "KENSHI_LINK_CLICK_HOLD_SECONDS": "0.25"})
    assert (config.pointer_dwell_seconds, config.modifier_gap_seconds) == (0.2, 0.0)
    assert (config.halt_poll_seconds, config.click_hold_seconds) == (0.05, 0.25)
    assert config.keymap["previous_squad"] == "shift+tab"
    path.write_text('[keymap]\nprevious_squad = "shift+tab"\n')  # without the opt-in
    with pytest.raises(ValueError, match="Steam overlay"):
        load_config(path, env={})
    for bad in ({"halt_poll_seconds": 0}, {"halt_poll_seconds": 5}, {"modifier_gap_seconds": -1},
                {"pointer_dwell_seconds": -0.1}):
        with pytest.raises(ValueError):
            Config(**bad).validate()


def test_config_file_as_windows_editors_save_it(tmp_path):
    path = tmp_path / "config.toml"
    # Notepad's "UTF-8 with BOM" and PowerShell's `Set-Content -Encoding UTF8` both add a
    # byte-order mark, and both write CRLF line endings.
    path.write_bytes(b"\xef\xbb\xbfmax_long_edge = 1600\r\n[keymap]\r\ninventory = \"k\"\r\n")
    config = load_config(path, env={})
    assert config.max_long_edge == 1600 and config.keymap["inventory"] == "k"
    # A Windows path belongs in single quotes; in double quotes TOML rejects the backslashes.
    path.write_bytes(b"data_dir = 'C:\\Users\\you\\kenshi'\r\n")
    assert str(load_config(path, env={}).data_dir) == r"C:\Users\you\kenshi"
    path.write_bytes(b'data_dir = "C:\\Users\\you\\kenshi"\r\n')
    with pytest.raises(ValueError, match="config.toml"):  # the message names the file at fault
        load_config(path, env={})
    path.write_bytes("max_long_edge = 1600\r\n".encode("utf-16"))  # PowerShell's `>` redirection
    with pytest.raises(ValueError, match="not UTF-8"):
        load_config(path, env={})


def test_notes_edited_by_hand_on_windows_still_read(tmp_path, monkeypatch):
    notes = tmp_path / "notes.md"
    notes.write_bytes(b"\xef\xbb\xbf# Goal\r\nReach the Hub\r\n")  # UTF-8 with a byte-order mark, CRLF
    assert read_notes(notes) == "# Goal\nReach the Hub\n"
    notes.write_bytes("# Goal\r\nReach the Hub\r\n".encode("utf-16"))  # PowerShell: "..." > notes.md
    assert read_notes(notes) == "# Goal\nReach the Hub\n"
    # Saved in the system code page rather than UTF-8 (an older Notepad's "ANSI").
    monkeypatch.setattr("locale.getencoding", lambda: "cp1252")
    notes.write_bytes(b"caf\xe9 in the Hub\r\n")
    assert read_notes(notes) == "caf\u00e9 in the Hub\n"
    write_notes(notes, "more")  # ... and the next save makes the file UTF-8
    assert notes.read_bytes().decode("utf-8").replace("\r\n", "\n") == "caf\u00e9 in the Hub\nmore\n"
    monkeypatch.setattr("locale.getencoding", lambda: "utf-8")  # not text in any encoding we know
    notes.write_bytes(b"caf\xe9 in the Hub\r\n")
    assert read_notes(notes) == "caf\ufffd in the Hub\n"


def test_notes_do_not_grow_blank_lines_from_crlf_text(tmp_path):
    notes = tmp_path / "notes.md"
    assert write_notes(notes, "one\r\ntwo\rthree") == len("one\ntwo\nthree\n")
    assert read_notes(notes) == "one\ntwo\nthree\n"
    assert b"\r\r" not in notes.read_bytes()
    write_notes(notes, "caf\u00e9 \u2192 \u65e5\u672c\u8a9e")
    assert notes.read_bytes().replace(b"\r\n", b"\n").endswith("caf\u00e9 \u2192 \u65e5\u672c\u8a9e\n".encode("utf-8"))


def test_notes_append_and_replace(tmp_path):
    notes = tmp_path / "deep" / "notes.md"
    assert read_notes(notes) == ""
    write_notes(notes, "first")
    write_notes(notes, "second")
    assert read_notes(notes) == "first\nsecond\n"
    write_notes(notes, "fresh", mode="replace")
    assert read_notes(notes) == "fresh\n"
    with pytest.raises(ControlError):
        write_notes(notes, "x", mode="prepend")
