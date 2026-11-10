"""Keys, imaging, config and the Win32 structures (checked on any platform)."""

from __future__ import annotations

import ctypes

import pytest
from PIL import Image

from kenshi_link import imaging
from kenshi_link.backends import _win_structs as ws
from kenshi_link.config import DEFAULT_KEYMAP, Config, load_config
from kenshi_link.controller import ControlError, read_notes, write_notes
from kenshi_link.keys import KEYS, BlockedInput, char_to_key, check_allowed, parse_combo, parse_modifiers

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


def test_absolute_coordinates_span_the_virtual_desktop():
    single = (0, 0, 1920, 1080)
    assert ws.absolute_coords(0, 0, single) == (0, 0)
    assert ws.absolute_coords(1919, 1079, single) == (65535, 65535)
    left_monitor = (-1920, 0, 3840, 1080)  # a second monitor to the left of the primary
    assert ws.absolute_coords(-1920, 0, left_monitor) == (0, 0)
    assert ws.absolute_coords(0, 0, left_monitor)[0] == round(1920 * 65535 / 3839)


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
