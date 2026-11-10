"""Controller behaviour against the stand-in window, on virtual time."""

from __future__ import annotations

import io

import pytest
from PIL import Image

from kenshi_link.backends.base import BackendError, DesktopUnavailable, WindowNotFound
from kenshi_link.controller import HALT_MARKER, ControlError, Controller, Halted, Interrupted
from kenshi_link.keys import BlockedInput

# The mock window is 1600x900 and screenshots are 1280x720, so image = window * 0.8.
# Unit 2 starts at world (60, 80) = window (860, 530) = image (688, 424).
UNIT_2 = (688, 424)


def keys_pressed(backend) -> list[str]:
    return [event[1] for event in backend.events if event[0] == "key" and event[2]]


def image_of(result) -> Image.Image:
    return Image.open(io.BytesIO(result.images[-1].data))


def when(backend, *event, last: bool = False) -> float:
    """The (virtual) time of the first, or last, event that starts with these fields."""
    times = [t for e, t in zip(backend.events, backend.stamps) if e[: len(event)] == event]
    assert times, f"no {event} event in {backend.events}"
    return times[-1] if last else times[0]


def after(clock, monkeypatch, seconds: float, action) -> None:
    """Run `action` once, the first time the clock passes `seconds` during a sleep."""
    real_sleep, done = clock.sleep, []

    def sleep(duration):
        real_sleep(duration)
        if clock.time > seconds and not done:
            done.append(True)
            action()

    monkeypatch.setattr(clock, "sleep", sleep)


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
        controller.click(*UNIT_2, modifiers="ctrl+alt")
    assert ("key", "alt", False) in backend.events and ("key", "ctrl", False) in backend.events


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


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        ("stop\r\n".encode("utf-16"), "stop"),  # PowerShell: "stop" > STOP
        ("\u0441\u0442\u043e\u043f\r\n".encode("utf-8"), "\u0441\u0442\u043e\u043f"),  # Notepad, UTF-8
        (b"\xef\xbb\xbfstop now\r\n", "stop now"),  # UTF-8 with a byte-order mark
        (b"arr\xeat\r\n", "arr\u00eat"),  # the system code page (cp1252 in this test)
        (b"\x81\x8d\x8f\x90\x9d", "\ufffd" * 5),  # bytes that are neither UTF-8 nor cp1252
        (b"", "stop file present"),
        (b"\r\n\r\n", "stop file present"),
    ],
    ids=["utf-16", "utf-8", "utf-8-bom", "cp1252", "undecodable", "empty", "blank-lines"],
)
def test_a_stop_file_halts_whatever_wrote_it(controller, config, backend, monkeypatch, content, reason):
    monkeypatch.setattr("locale.getencoding", lambda: "cp1252")
    config.data_dir.mkdir(parents=True)
    config.stop_file.write_bytes(content)
    with pytest.raises(Halted) as halted:
        controller.advance(1.0)
    assert str(halted.value).startswith(f"{HALT_MARKER}: {reason}. ")
    assert backend.events == []


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


# ---- timing: what a game that reads its input once per frame needs -------------------


def test_the_pointer_rests_on_the_target_before_the_button_goes_down(config, backend, clock):
    Controller(config, backend, clock).click(*UNIT_2)
    arrived, pressed = when(backend, "move", 980, 590), when(backend, "button", "left", True)
    assert pressed - arrived == pytest.approx(config.pointer_dwell_seconds) and config.pointer_dwell_seconds >= 0.1
    backend.events.clear(), backend.stamps.clear()
    config.pointer_dwell_seconds = 0.4
    Controller(config, backend, clock).scroll(688, 424, "up", 1)
    assert when(backend, "wheel") - when(backend, "move", 980, 590, last=True) == pytest.approx(0.4)


def test_a_drag_is_released_only_after_the_pointer_has_rested_at_the_end(controller, config, backend):
    controller.drag(400, 200, 900, 600)
    arrived, released = when(backend, "move", last=True), when(backend, "button", "left", False)
    assert released - arrived >= config.pointer_dwell_seconds


def test_buttons_and_keys_stay_down_longer_than_a_slow_frame(config, backend, clock):
    controller = Controller(config, backend, clock)
    controller.click(*UNIT_2)
    controller.press_key("i")
    assert when(backend, "button", "left", False) - when(backend, "button", "left", True) == pytest.approx(0.1)
    assert when(backend, "key", "i", False) - when(backend, "key", "i", True) == pytest.approx(0.1)
    backend.events.clear(), backend.stamps.clear()
    config.click_hold_seconds, config.key_hold_seconds = 0.25, 0.3
    controller.click(*UNIT_2)
    controller.press_key("i")
    assert when(backend, "button", "left", False) - when(backend, "button", "left", True) == pytest.approx(0.25)
    assert when(backend, "key", "i", False) - when(backend, "key", "i", True) == pytest.approx(0.3)


@pytest.mark.parametrize("gap", [None, 0.5])
def test_a_modifier_is_down_well_before_the_click_and_up_well_after(config, backend, clock, gap):
    if gap is not None:
        config.modifier_gap_seconds = gap
    controller = Controller(config, backend, clock)
    controller.click(1000, 200, button="right", modifiers="shift")
    expected = config.modifier_gap_seconds
    assert expected >= 0.1
    assert when(backend, "button", "right", True) - when(backend, "key", "shift", True) == pytest.approx(expected)
    assert when(backend, "key", "shift", False) - when(backend, "button", "right", False) == pytest.approx(expected)
    backend.events.clear(), backend.stamps.clear()
    controller.drag(400, 200, 900, 600, modifiers="ctrl")
    assert when(backend, "button", "left", True) - when(backend, "key", "ctrl", True) == pytest.approx(expected)
    assert when(backend, "key", "ctrl", False) - when(backend, "button", "left", False) == pytest.approx(expected)


def test_a_pointer_that_is_not_on_target_after_the_move_is_placed_there_before_the_click(
    controller, config, backend, monkeypatch
):
    move, placed = backend.move, []

    def falls_short(x, y):
        move(x - 1, y)  # what a platform's coordinate rounding can do

    def place(x, y):
        placed.append((x, y))
        move(x, y)

    monkeypatch.setattr(backend, "move", falls_short)
    monkeypatch.setattr(backend, "place", place)
    controller.click(*UNIT_2)
    assert placed == [(980, 590)]
    downs = [e for e in backend.events if e[0] == "button" and e[2]]
    assert downs == [("button", "left", True, 980, 590)]
    rested = when(backend, "button", "left", True) - when(backend, "move", 980, 590)
    assert rested == pytest.approx(config.pointer_dwell_seconds), "it rests again after being put right"


def test_a_pointer_the_operator_knocked_aside_is_put_back_but_the_corner_still_stops(
    controller, backend, clock, monkeypatch
):
    placed = []
    monkeypatch.setattr(backend, "place", lambda x, y: (placed.append((x, y)), setattr(backend, "_pointer", (x, y))))
    after(clock, monkeypatch, 0.15, lambda: setattr(backend, "_pointer", (700, 300)))  # during the rest
    controller.click(*UNIT_2)
    assert placed == [(980, 590)] and [u.number for u in backend.units if u.selected] == [2]
    placed.clear()
    monkeypatch.undo()
    monkeypatch.setattr(backend, "place", lambda x, y: placed.append((x, y)))
    after(clock, monkeypatch, clock.time + 0.15, lambda: setattr(backend, "_pointer", (1, 1)))
    with pytest.raises(Halted, match="top-left corner"):
        controller.click(*UNIT_2)
    assert placed == [] and backend.cursor() == (1, 1)


def test_a_plain_click_does_not_pay_for_the_modifier_gap(config, backend, clock):
    config.modifier_gap_seconds = 5.0
    Controller(config, backend, clock).click(*UNIT_2)
    assert when(backend, "button", "left", False) - when(backend, "move") < 1.0


# ---- operator stops in the middle of a sequence --------------------------------------


def test_a_stop_while_typing_ends_it_there_with_nothing_held(controller, config, backend, monkeypatch):
    original = backend.key

    def key(name, down):
        original(name, down)
        if len(backend.typed) >= 3:
            backend.panic = True  # the operator presses Pause/Break

    monkeypatch.setattr(backend, "key", key)
    with pytest.raises(Halted, match="Pause/Break"):
        controller.type_text("abcdefghij")
    assert backend.typed == "abc" and backend._held_keys == {}
    assert config.stop_file.exists()


def test_a_stop_during_repeated_presses_ends_them(controller, config, backend, clock, monkeypatch):
    config.data_dir.mkdir(parents=True)
    after(clock, monkeypatch, 1.0, lambda: config.stop_file.write_text("stop\n"))
    with pytest.raises(Halted):
        controller.press_key("r", repeat=20)
    assert 1 <= len(keys_pressed(backend)) < 20 and backend._held_keys == {}


def test_a_stop_during_a_long_hold_releases_the_key_at_once(controller, config, backend, clock, monkeypatch):
    config.data_dir.mkdir(parents=True)
    after(clock, monkeypatch, 1.0, lambda: config.stop_file.write_text("stop\n"))
    with pytest.raises(Halted, match=HALT_MARKER):
        controller.press_key("w", hold_seconds=8)
    assert clock.time < 1.0 + 2 * config.halt_poll_seconds, "noticed within one check interval"
    assert ("key", "w", False) in backend.events and backend._held_keys == {}


def test_a_stop_during_a_long_click_hold_releases_the_button(controller, backend, clock, monkeypatch):
    after(clock, monkeypatch, 1.0, lambda: setattr(backend, "panic", True))
    with pytest.raises(Halted):
        controller.click(300, 300, button="right", hold_seconds=5)
    assert clock.time < 1.5 and backend._held_buttons == {}
    assert ("button", "right", False, *backend.cursor()) in backend.events


def test_the_mouse_shoved_into_the_corner_stops_a_drag_in_progress(controller, backend, clock, monkeypatch):
    def shove() -> None:
        assert "left" in backend._held_buttons, "the drag is under way"
        backend._pointer = (1, 1)

    after(clock, monkeypatch, 0.45, shove)
    with pytest.raises(Halted, match="top-left corner"):
        controller.drag(400, 200, 900, 600)
    assert backend._held_buttons == {}
    moves_after = [e for e, t in zip(backend.events, backend.stamps) if e[0] == "move" and t > 0.6]
    assert moves_after == [], "the pointer was not pulled back out of the corner"


def test_a_tap_of_the_panic_key_between_actions_is_not_lost(controller, config, backend):
    controller.observe()
    backend.panic_callback()  # the platform reports the key press; nothing is being held now
    with pytest.raises(Halted, match="the operator pressed Pause/Break"):
        controller.click(*UNIT_2)
    assert config.stop_file.exists() and not [e for e in backend.events if e[0] == "button"]


def test_the_panic_key_is_not_watched_when_it_is_switched_off(config, backend, clock):
    config.panic_key = False
    Controller(config, backend, clock)
    assert backend.panic_callback is None


def test_a_stop_forgets_the_pause_state(controller, config):
    controller.sync_pause(True)
    config.stop_file.write_text("stop\n")
    with pytest.raises(Halted):
        controller.observe()
    config.stop_file.unlink()  # the operator may have done anything in between
    assert controller.paused is None
    assert "inferred" in controller.observe().text


def test_a_stop_during_advance_says_the_game_was_left_running(controller, backend, clock, monkeypatch):
    after(clock, monkeypatch, 2.0, lambda: setattr(backend, "panic", True))
    with pytest.raises(Halted) as halted:
        controller.advance(10, "fast")
    assert str(halted.value).startswith(HALT_MARKER) and "left running at fast speed" in str(halted.value)


# ---- the failsafe corner and this program's own pointer moves ------------------------


def test_a_click_in_the_corner_of_a_window_at_the_screen_corner_does_not_trip_the_failsafe(controller, backend):
    backend.left = backend.top = 0  # borderless, at the origin of the desktop
    backend._pointer = (800, 450)
    controller.click(0, 0)
    assert backend.cursor() == (5, 5)
    controller.click(1, 2)  # the next action is not halted
    assert not controller.config.stop_file.exists()


def test_the_pointer_is_never_parked_in_or_dragged_through_the_corner(controller, backend):
    backend.left = backend.top = -10  # the window hangs off the top-left of the screen
    backend._pointer = (-3, 5)
    controller.click(12, 6)  # window (15, 7) is screen (5, -3): the straight path crosses (1, 1)
    moves = [(e[1], e[2]) for e in backend.events if e[0] == "move"]
    assert moves and not [m for m in moves if 0 <= m[0] <= 3 and 0 <= m[1] <= 3]
    backend._pointer = (800, 450)
    controller.click(8, 8)  # window (10, 10) is the corner pixel itself
    assert backend.cursor() == (4, 0)
    downs = [e for e in backend.events if e[0] == "button" and e[2]]
    assert downs[-1][3:] == (4, 0), "it clicked where it stopped, and the ring is drawn there"
    assert controller._pointer == (14, 10)


def test_the_failsafe_corner_follows_the_backend(controller, config, backend):
    backend.corner = (-1920, 0)  # a second monitor to the left of the primary one
    backend._pointer = (0, 0)
    controller.observe()  # mid-desktop now: not a corner
    backend._pointer = (-1919, 2)
    with pytest.raises(Halted, match="top-left corner"):
        controller.observe()


def test_without_the_failsafe_corner_the_pointer_may_go_anywhere(config, backend, clock):
    config.failsafe_corner = False
    backend.left = backend.top = -10
    controller = Controller(config, backend, clock)
    controller.click(8, 8)
    assert backend.cursor() == (0, 0)
    controller.observe()


# ---- what is under the pointer, and where the window is ------------------------------


def test_nothing_is_clicked_when_another_window_covers_the_spot(controller, backend):
    backend.obstructed = True
    with pytest.raises(ControlError, match="covering the game"):
        controller.click(*UNIT_2, modifiers="shift")
    assert not [e for e in backend.events if e[0] == "button"]
    assert ("key", "shift", False) in backend.events and backend._held_keys == {}
    with pytest.raises(ControlError, match="covering the game"):
        controller.drag(400, 200, 900, 600)
    for wheel in (lambda: controller.scroll(640, 360, "up", 3), lambda: controller.camera("zoom_in", 2)):
        with pytest.raises(ControlError, match="covering the game"):
            wheel()
    assert not [e for e in backend.events if e[0] in ("button", "wheel")]
    controller.press_key("i")  # keys go to the focused window whatever the pointer is over
    backend.obstructed = False
    controller.click(*UNIT_2)


def test_a_window_partly_off_the_screen_is_refused_before_any_input(controller, backend):
    backend.screen = (0, 0, 1600, 900)  # the 1600x900 window at (120, 60) hangs off this
    for action in (controller.observe, lambda: controller.click(*UNIT_2), lambda: controller.press_key("i")):
        with pytest.raises(ControlError, match="partly off the screen"):
            action()
    assert backend.events == []
    backend.screen = (-1920, 0, 3840, 1080)
    controller.click(*UNIT_2)
    backend.left = -400  # onto the monitor on the left: still on the desktop
    controller.observe()


def test_a_failed_refocus_passes_on_what_the_platform_said(controller, backend, monkeypatch):
    backend.focused = False
    monkeypatch.setattr(backend, "focus", lambda: None)
    monkeypatch.setattr(backend, "focus_error", lambda: "Windows refused to change the front window (error 5).")
    with pytest.raises(ControlError, match=r"brought to the front.*\(error 5\)\. Ask the operator to click"):
        controller.press_key("i")
    assert backend.events == []


# ---- a desktop or a game that is out of reach ----------------------------------------


def unavailable(*_args):
    raise DesktopUnavailable("The Windows desktop is not available: the screen is locked")


def test_a_locked_desktop_is_reported_as_a_halt_without_a_stop_file(controller, config, backend, monkeypatch):
    monkeypatch.setattr(backend, "cursor", unavailable)
    with pytest.raises(Halted) as halted:
        controller.click(*UNIT_2)
    assert str(halted.value).startswith(f"{HALT_MARKER}: The Windows desktop is not available")
    assert "Do not retry" in str(halted.value)
    monkeypatch.undo()
    monkeypatch.setattr(backend, "locate", unavailable)
    config.failsafe_corner = False
    for action in (controller.observe, lambda: controller.press_key("i"), lambda: controller.advance(1)):
        with pytest.raises(Halted, match=HALT_MARKER):
            action()
    assert backend.events == [] and not config.stop_file.exists()
    monkeypatch.undo()
    controller.observe()  # back at the desktop: nothing to resume


def test_a_desktop_locked_during_advance_is_a_halt_that_says_the_game_runs_on(
    controller, config, backend, clock, monkeypatch
):
    def lock() -> None:
        monkeypatch.setattr(backend, "cursor", unavailable)
        monkeypatch.setattr(backend, "locate", unavailable)
        monkeypatch.setattr(backend, "capture", unavailable)

    after(clock, monkeypatch, 2.0, lock)
    with pytest.raises(Halted) as halted:
        controller.advance(10, "normal")
    text = str(halted.value)
    assert text.startswith(HALT_MARKER) and "left running at normal speed" in text
    assert keys_pressed(backend) == ["space", "f2"] and controller.paused is None
    assert not config.stop_file.exists()


def test_the_same_with_the_stop_checks_switched_off(config, backend, clock, monkeypatch):
    config.failsafe_corner = config.panic_key = False
    controller = Controller(config, backend, clock)
    after(clock, monkeypatch, 2.0, lambda: monkeypatch.setattr(backend, "locate", unavailable))
    with pytest.raises(Halted, match="left running at normal speed"):
        controller.advance(5, "normal", frames=0)
    assert controller.paused is False


def test_a_pointer_that_cannot_be_read_is_an_error_claude_can_read(controller, backend, monkeypatch):
    def broken():
        raise BackendError("Windows would not report the pointer position (error 5).")

    monkeypatch.setattr(backend, "cursor", broken)
    with pytest.raises(ControlError, match="pointer position") as error:
        controller.press_key("i")
    assert not isinstance(error.value, Halted) and backend.events == []


def test_stop_checks_failing_during_advance_end_the_run_with_the_game_paused(
    controller, backend, clock, monkeypatch
):
    def broken():
        raise BackendError("Windows would not report the pointer position (error 5).")

    after(clock, monkeypatch, 2.0, lambda: monkeypatch.setattr(backend, "cursor", broken))
    result = controller.advance(60, "normal")
    assert keys_pressed(backend) == ["space", "f2", "space"] and backend.paused is True
    assert clock.time < 5 and controller.paused is True
    assert "less than the 60s asked for" in result.text and "pointer position" in result.text


def test_a_capture_failure_is_reported_and_a_missed_frame_does_not_end_an_advance(
    controller, backend, clock, monkeypatch
):
    original = backend.capture

    def failing(*args):
        if 1.0 < clock.time < 4.6:
            raise BackendError("The screen could not be captured (BitBlt failed).")
        return original(*args)

    monkeypatch.setattr(backend, "capture", failing)
    result = controller.advance(5, "normal", frames=2)  # both in-between frames fall in the bad stretch
    assert backend.paused is True and len(result.images) == 1 and "strip" not in result.text

    def broken(*args):
        raise BackendError("The screen could not be captured (BitBlt failed).")

    monkeypatch.setattr(backend, "capture", broken)
    with pytest.raises(ControlError, match="could not be captured"):
        controller.observe()


def test_a_game_that_is_not_responding_is_reported_as_such(controller, backend, monkeypatch):
    def hung():
        raise BackendError("Kenshi is not responding right now: it is probably loading or saving.")

    monkeypatch.setattr(backend, "locate", hung)
    with pytest.raises(ControlError, match="not responding") as error:
        controller.click(*UNIT_2)
    assert not isinstance(error.value, Halted) and backend.events == []
    assert "window: UNUSABLE - Kenshi is not responding" in controller.describe()


def test_a_game_that_stops_responding_while_typing_is_not_sent_the_rest(controller, backend, monkeypatch):
    original = backend.locate

    def locate():
        if len(backend.typed) >= 8:
            raise BackendError("Kenshi is not responding right now: it is probably loading or saving.")
        return original()

    monkeypatch.setattr(backend, "locate", locate)
    with pytest.raises(ControlError, match="not responding.*while typing, so the rest was not sent"):
        controller.type_text("abcdefghijklmnopqrst")
    assert backend.typed == "abcdefgh" and backend._held_keys == {}


def test_describe_tells_a_missing_window_from_an_unusable_one(controller, backend, monkeypatch):
    backend.present = False
    assert "window: NOT FOUND - " in controller.describe()
    backend.present = True
    monkeypatch.setattr(backend, "notes", lambda: ["stop key: Pause/Break is registered as a hotkey"])
    report = controller.describe().splitlines()
    assert report[-2].startswith("stop file:") and report[-1].startswith("stop key:")

    def gone():
        raise WindowNotFound("No Kenshi window found.")

    monkeypatch.setattr(backend, "locate", gone)
    assert "window: NOT FOUND - No Kenshi window found." in controller.describe()


# ---- pausing on request, and shutting down -------------------------------------------


def test_a_pause_request_cuts_an_advance_short_and_pauses(controller, backend, clock, monkeypatch):
    after(clock, monkeypatch, 2.0, controller.request_pause)
    result = controller.advance(60, "fast")
    assert keys_pressed(backend) == ["space", "f3", "space"] and backend.paused is True
    assert clock.time < 5 and "less than the 60s asked for, because a pause was asked for" in result.text
    monkeypatch.undo()
    backend.events.clear()
    assert "Ran the game for 3.0s" in controller.advance(3, "normal").text, "the request does not linger"


def test_set_speed_pause_consumes_its_own_request(controller, backend):
    controller.request_pause()  # what the server does when set_speed("pause") arrives
    controller.set_speed("pause")
    result = controller.advance(3, "normal")
    assert "less than" not in result.text and backend.game_time == pytest.approx(3, abs=0.5)
    controller.request_pause()
    with pytest.raises(ControlError):
        controller.set_speed("warp")  # not a pause: the request stands
    assert "less than the 3s asked for" in controller.advance(3, "normal").text


def test_shutdown_during_advance_pauses_the_game_and_skips_the_screenshot(
    controller, config, backend, clock, monkeypatch
):
    after(clock, monkeypatch, 2.0, controller.shutdown)
    with pytest.raises(Interrupted, match="the game was paused"):
        controller.advance(60, "normal")
    assert keys_pressed(backend) == ["space", "f2", "space"] and backend.paused is True
    assert clock.time < 2.5, "no settling or screenshots on the way out"
    log = next(config.sessions_dir.glob("*.jsonl")).read_text(encoding="utf-8")
    assert "Shutting down: the run was stopped after 1." in log and "the game was paused" in log
    with pytest.raises(Interrupted, match="shutting down"):
        controller.observe()


def test_shutdown_during_a_long_hold_lets_go_of_the_key(controller, backend, clock, monkeypatch):
    after(clock, monkeypatch, 1.0, controller.shutdown)
    with pytest.raises(Interrupted, match="shutting down"):
        controller.camera("forward", 20)  # a five-second hold of W
    assert clock.time < 1.5 and ("key", "w", False) in backend.events and backend._held_keys == {}


def test_close_releases_anything_still_held(controller, backend):
    controller._key_down("shift")
    controller._button_down("left")
    controller.close()
    assert backend._held_keys == {} and backend._held_buttons == {}
    assert backend.events[-2:] == [("button", "left", False, *backend.cursor()), ("key", "shift", False)]


# ---- keys: rules, the keyboard layout and Caps Lock ----------------------------------


def test_system_combos_stay_blocked_with_extra_modifiers(controller, config, backend):
    for combo in ("ctrl+alt+f4", "shift+alt+f4", "alt+shift+escape", "ctrl+alt+shift+tab", "alt+shift",
                  "ctrl+shift", "shift+tab", "ctrl+shift+f12"):
        with pytest.raises(ControlError, match="blocked|disabled"):
            controller.press_key(combo)
    for modifiers in ("alt+shift", "ctrl+shift"):
        with pytest.raises(ControlError, match="keyboard layout"):
            controller.click(*UNIT_2, modifiers=modifiers)
        with pytest.raises(ControlError, match="keyboard layout"):
            controller.drag(400, 200, 900, 600, modifiers=modifiers)
    assert backend.events == []
    config.allow_shift_tab = True
    controller.press_key("shift+tab")
    assert keys_pressed(backend) == ["shift", "tab"]


def test_typing_presses_the_keys_the_keyboard_layout_puts_the_characters_on(controller, backend):
    # French AZERTY: "a" is on the key a US keyboard calls Q, and digits need Shift.
    backend.layout = {"a": ("q", False), "A": ("q", True), "1": ("1", True), "m": ("semicolon", False)}
    controller.type_text("Aam 1")
    assert keys_pressed(backend) == ["shift", "q", "q", "semicolon", "space", "shift", "1"]


def test_text_the_layout_cannot_produce_is_refused_before_anything_is_typed(controller, backend, monkeypatch):
    def typing_keys(text):
        raise BlockedInput("Cannot type '@': on the keyboard layout Kenshi is using it needs AltGr.")

    monkeypatch.setattr(backend, "typing_keys", typing_keys)
    with pytest.raises(ControlError, match="needs AltGr"):
        controller.type_text("me@home")
    assert backend.events == []


def test_caps_lock_stops_letters_being_typed_in_the_wrong_case(controller, backend):
    backend.caps = True
    with pytest.raises(ControlError, match="Caps Lock is on"):
        controller.type_text("Hub")
    assert backend.events == []
    controller.type_text("12 34")  # Caps Lock does not change these
    assert backend.typed == "1234"
