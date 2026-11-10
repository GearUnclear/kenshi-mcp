"""Controller behaviour against the stand-in window, on virtual time."""

from __future__ import annotations

import io

import pytest
from PIL import Image

from kenshi_link.backends.base import BackendError
from kenshi_link.controller import HALT_MARKER, ControlError, Controller, Halted

# The mock window is 1600x900 and screenshots are 1280x720, so image = window * 0.8.
# Unit 2 starts at world (60, 80) = window (860, 530) = image (688, 424).
UNIT_2 = (688, 424)


def keys_pressed(backend) -> list[str]:
    return [event[1] for event in backend.events if event[0] == "key" and event[2]]


def image_of(result) -> Image.Image:
    return Image.open(io.BytesIO(result.images[-1].data))


# ---- looking -------------------------------------------------------------------


def test_observe_returns_a_scaled_screenshot_and_infers_pause(controller):
    result = controller.observe()
    assert image_of(result).size == (1280, 720)
    assert "inferred as PAUSED" in result.text
    assert controller.paused is True and controller.pause_source == "inferred"


def test_observe_infers_running_when_the_picture_moves(controller, backend):
    backend.paused = False
    backend.units[0].selected = True
    backend.units[0].target = (400.0, 300.0)
    result = controller.observe()
    assert "inferred as RUNNING" in result.text
    assert controller.paused is False


def test_observe_flags_a_pause_belief_that_the_picture_contradicts(controller, backend):
    controller.sync_pause(True)
    backend.paused = False
    backend.units[0].target = (400.0, 300.0)
    assert "still changing" in controller.observe().text


def test_grid_overlay_changes_the_picture(controller):
    plain, gridded = controller.observe(), controller.observe(grid=True)
    assert plain.images[0].data != gridded.images[0].data
    assert "grid" in gridded.text


def test_zoom_magnifies_a_region_and_validates_it(controller):
    result = controller.zoom(0, 0, 400, 100)
    assert image_of(result).size == (1280, 320)
    with pytest.raises(ControlError, match="x0 < x1"):
        controller.zoom(400, 0, 100, 100)
    with pytest.raises(ControlError, match="too small"):
        controller.zoom(0, 0, 10, 10)
    with pytest.raises(ControlError, match="inside"):
        controller.zoom(0, 0, 5000, 100)


# ---- pointer -------------------------------------------------------------------


def test_click_maps_screenshot_pixels_to_the_screen(controller, backend):
    controller.click(*UNIT_2)
    assert [u.number for u in backend.units if u.selected] == [2]
    downs = [e for e in backend.events if e[0] == "button" and e[2]]
    # window (860, 530) plus the mock window's screen offset (120, 60)
    assert downs == [("button", "left", True, 980, 590)]


def test_right_click_orders_and_advance_moves_the_unit(controller, backend):
    controller.click(*UNIT_2)
    controller.click(1000, 200, button="right")
    assert backend.units[1].target is not None
    before = (backend.units[1].x, backend.units[1].y)
    controller.advance(3, "normal")
    assert (backend.units[1].x, backend.units[1].y) != before


def test_right_click_hold_opens_the_context_menu(controller, backend):
    controller.click(300, 300, button="right", hold_seconds=0.7)
    assert backend.menu is not None


def test_drag_box_selects(controller, backend):
    controller.drag(400, 200, 900, 600)
    assert sum(u.selected for u in backend.units) >= 2


def test_shift_click_adds_to_selection_and_releases_shift(controller, backend):
    controller.click(*UNIT_2)
    unit_1 = (round((-120 + 800) * 0.8), round((-40 + 450) * 0.8))
    controller.click(*unit_1, modifiers="shift")
    assert sorted(u.number for u in backend.units if u.selected) == [1, 2]
    assert ("key", "shift", False) in backend.events


def test_points_outside_the_screenshot_are_rejected_without_input(controller, backend):
    with pytest.raises(ControlError, match="outside the 1280x720"):
        controller.click(1280, 10)
    assert not [e for e in backend.events if e[0] in ("button", "key")]


def test_scroll_zooms_the_mock_camera(controller, backend):
    controller.scroll(640, 360, "up", 3)
    assert backend.zoom > 1.0
    with pytest.raises(ControlError):
        controller.scroll(640, 360, "sideways", 1)


def test_a_failure_mid_click_releases_held_modifiers(controller, backend, monkeypatch):
    def broken(button, down):
        raise BackendError("device lost")

    monkeypatch.setattr(backend, "button", broken)
    with pytest.raises(ControlError, match="device lost"):
        controller.click(*UNIT_2, modifiers="ctrl+shift")
    assert ("key", "shift", False) in backend.events and ("key", "ctrl", False) in backend.events


# ---- keyboard ------------------------------------------------------------------


def test_keys_that_leave_the_game_are_refused(controller, backend):
    for combo in ("alt+f4", "alt+tab", "win", "ctrl+escape", "super+d", "shift+f12"):
        with pytest.raises(ControlError):
            controller.press_key(combo)
    assert keys_pressed(backend) == []


def test_pressing_the_pause_key_directly_keeps_the_belief_in_step(controller, backend):
    controller.sync_pause(True)
    result = controller.press_key("space")
    assert backend.paused is False and controller.paused is False
    assert "pause key" in result.text


def test_type_text_types_into_the_game(controller, backend):
    controller.type_text("Ab1")
    assert backend.typed == "Ab1"
    with pytest.raises(ControlError, match="US-keyboard"):
        controller.type_text("é")


def test_hotkey_uses_the_keymap(controller, backend):
    controller.hotkey("inventory")
    controller.hotkey("select_3", repeat=2)
    assert keys_pressed(backend) == ["i", "3", "3"]
    assert [u.number for u in backend.units if u.selected] == [3]
    with pytest.raises(ControlError, match="Unknown action"):
        controller.hotkey("teleport")
    with pytest.raises(ControlError, match="set_speed"):
        controller.hotkey("pause")


def test_rebound_keys_are_respected(config, backend, clock):
    config.keymap["inventory"] = "k"
    Controller(config, backend, clock).hotkey("inventory")
    assert keys_pressed(backend) == ["k"]


def test_highlight_items_screenshots_while_the_key_is_held(controller, backend, monkeypatch):
    held_during_capture = []
    original = backend.capture

    def capture(*args):
        held_during_capture.append("alt" in backend._held_keys)
        return original(*args)

    monkeypatch.setattr(backend, "capture", capture)
    controller.hotkey("highlight_items")
    assert held_during_capture == [True]
    assert ("key", "alt", False) in backend.events


# ---- camera --------------------------------------------------------------------


def test_camera_actions(controller, backend):
    controller.camera("right", 2)
    assert backend.camera[0] > 0
    controller.camera("zoom_out", 3)
    assert backend.zoom < 1.0
    controller.camera("tilt_up", 2)
    middle = [e for e in backend.events if e[0] == "button" and e[1] == "middle"]
    assert [e[2] for e in middle] == [True, False]
    assert middle[1][4] < middle[0][4], "dragged upward"
    with pytest.raises(ControlError):
        controller.camera("barrel_roll")


# ---- time ----------------------------------------------------------------------


def test_advance_unpauses_runs_and_repauses(controller, backend):
    result = controller.advance(5, "fast", frames=2)
    assert keys_pressed(backend) == ["space", "f3", "space"]
    assert backend.paused is True and controller.paused is True
    assert controller.pause_source == "tracked" and controller.speed == "fast"
    assert 9.5 <= backend.game_time <= 11.5, "about 5 s at double speed"
    assert len(result.images) == 2 and "strip of 2" in result.text


def test_advance_from_a_running_game_does_not_toggle_it_off(controller, backend):
    backend.paused = False
    controller.sync_pause(False)
    controller.advance(1, "normal", frames=0)
    assert keys_pressed(backend) == ["f2", "space"]
    assert backend.paused is True


def test_set_speed_pause_is_idempotent(controller, backend):
    controller.sync_pause(True)
    result = controller.set_speed("pause")
    assert keys_pressed(backend) == [] and "already paused" in result.text


def test_set_speed_pauses_a_game_found_running(controller, backend):
    backend.paused = False
    backend.units[0].target = (500.0, 300.0)
    controller.set_speed("pause")
    assert backend.paused is True and keys_pressed(backend) == ["space"]


def test_set_speed_running_then_pause(controller, backend):
    controller.set_speed("fastest")
    assert backend.paused is False and backend.speed == 4.0
    controller.set_speed("pause")
    assert backend.paused is True


def test_advance_validates_arguments(controller):
    for kwargs in ({"seconds": 0}, {"seconds": 9999}, {"seconds": 1, "speed": "pause"}, {"seconds": 1, "frames": 9}):
        with pytest.raises(ControlError):
            controller.advance(**kwargs)


def test_quick_load_forgets_the_pause_state(controller):
    controller.sync_pause(True)
    controller.hotkey("quick_load")
    assert controller.paused is None


# ---- safety --------------------------------------------------------------------


def test_stop_file_blocks_everything(controller, config, backend):
    config.data_dir.mkdir(parents=True)
    config.stop_file.write_text("operator said stop\n")
    with pytest.raises(Halted, match=HALT_MARKER):
        controller.click(*UNIT_2)
    with pytest.raises(Halted):
        controller.observe()
    assert backend.events == []
    config.stop_file.unlink()
    controller.observe()


def test_mouse_in_the_corner_trips_the_failsafe(controller, config, backend):
    backend._pointer = (0, 0)
    with pytest.raises(Halted, match="top-left corner"):
        controller.press_key("i")
    assert config.stop_file.exists() and keys_pressed(backend) == []
    backend._pointer = (500, 500)
    with pytest.raises(Halted):
        controller.press_key("i")


def test_panic_key_trips_the_failsafe(controller, config, backend):
    backend.panic = True
    with pytest.raises(Halted, match="Pause/Break"):
        controller.observe()
    assert config.stop_file.exists()


def test_panic_during_advance_sends_nothing_more(controller, backend, clock, monkeypatch):
    real_sleep = clock.sleep

    def sleep(seconds):
        real_sleep(seconds)
        if clock.time > 2.0:
            backend.panic = True

    monkeypatch.setattr(clock, "sleep", sleep)
    with pytest.raises(Halted):
        controller.advance(10, "normal")
    assert keys_pressed(backend) == ["space", "f2"], "no pause key after the operator took over"
    assert controller.paused is None


def test_unfocused_window_is_refocused_before_input(controller, backend):
    backend.focused = False
    controller.click(*UNIT_2)
    assert backend.events[0] == ("focus",)


def test_without_auto_focus_nothing_is_sent_to_an_unfocused_window(config, backend, clock):
    config.auto_focus = False
    backend.focused = False
    with pytest.raises(ControlError, match="not the focused window"):
        Controller(config, backend, clock).press_key("i")
    assert backend.events == []


def test_losing_focus_during_advance_reports_a_running_game(config, backend, clock, monkeypatch):
    config.auto_focus = False
    controller = Controller(config, backend, clock)
    real_sleep = clock.sleep

    def sleep(seconds):
        real_sleep(seconds)
        if clock.time > 2.0:
            backend.focused = False

    monkeypatch.setattr(clock, "sleep", sleep)
    with pytest.raises(ControlError, match="STILL RUNNING"):
        controller.advance(5, "normal")
    assert controller.paused is False


def test_missing_window_is_an_error_claude_can_read(controller, backend):
    backend.present = False
    with pytest.raises(ControlError, match="No Kenshi window"):
        controller.observe()


def test_actions_are_logged(controller, config):
    controller.click(*UNIT_2)
    logs = list(config.sessions_dir.glob("*.jsonl"))
    assert len(logs) == 1 and '"action": "click"' in logs[0].read_text()


def test_typing_stops_if_the_game_loses_focus(config, backend, clock, monkeypatch):
    config.auto_focus = False
    controller = Controller(config, backend, clock)
    original = backend.key

    def key(name, down):
        original(name, down)
        if len(backend.typed) >= 5:
            backend.focused = False

    monkeypatch.setattr(backend, "key", key)
    with pytest.raises(ControlError, match="lost focus while typing"):
        controller.type_text("abcdefghijklmnopqrst")
    assert len(backend.typed) < 20
