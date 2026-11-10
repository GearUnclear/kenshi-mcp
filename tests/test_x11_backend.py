"""Drives the real X11 backend against a real X window. Run under: xvfb-run -a pytest -m x11"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from PIL import Image

pytestmark = pytest.mark.x11

if sys.platform != "linux" or not os.environ.get("DISPLAY"):
    pytest.skip("needs an X display", allow_module_level=True)

from kenshi_link.config import Config  # noqa: E402
from kenshi_link.controller import ControlError, Controller  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "x11_window.py"
# The fixture window: 800x600 client area at (100, 50), which fits within 1280 so scale is 1.
WIDTH, HEIGHT = 800, 600


def _events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _wait_for(path: Path, predicate, timeout: float = 5.0) -> list[dict]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        events = _events(path) if path.exists() else []
        if predicate(events):
            return events
        time.sleep(0.05)
    raise AssertionError(f"timed out; events so far: {_events(path) if path.exists() else []}")


@pytest.fixture
def window_log(tmp_path):
    log = tmp_path / "events.jsonl"
    process = subprocess.Popen([sys.executable, str(FIXTURE), str(log)])
    try:
        _wait_for(log, lambda events: any(e["type"] == "ready" for e in events))
        time.sleep(0.3)  # let the first Expose paint
        yield log
    finally:
        process.terminate()
        process.wait(timeout=5)


@pytest.fixture
def game(tmp_path, window_log):
    config = Config(backend="x11", data_dir=tmp_path / "home", settle_seconds=0.1)
    config.validate()
    controller = Controller(config)
    yield controller
    controller.close()


def _image(result) -> Image.Image:
    return Image.open(io.BytesIO(result.images[-1].data)).convert("RGB")


def _near(pixel, expected, tolerance=40) -> bool:
    return all(abs(a - b) <= tolerance for a, b in zip(pixel, expected))


def test_finds_window_and_captures_its_pixels(game):
    result = game.observe()
    image = _image(result)
    assert image.size == (WIDTH, HEIGHT)
    assert _near(image.getpixel((50, 50)), (255, 0, 0)), "red square in the corner"
    assert _near(image.getpixel((400, 300)), (0x20, 0x40, 0x80)), "blue background"
    assert "800x600" in result.text


def test_left_click_arrives_at_the_same_window_pixel(game, window_log):
    game.click(321, 234)
    events = _wait_for(
        window_log, lambda ev: sum(e["type"] == "button" and not e["down"] for e in ev) >= 1
    )
    presses = [e for e in events if e["type"] == "button"]
    assert [(e["button"], e["down"]) for e in presses] == [(1, True), (1, False)]
    assert (presses[0]["x"], presses[0]["y"]) == (321, 234)


def test_right_click_hold_and_shift_modifier(game, window_log):
    started = time.time()
    game.click(600, 100, button="right", modifiers="shift", hold_seconds=0.5)
    events = _wait_for(
        window_log, lambda ev: sum(e["type"] == "button" and not e["down"] for e in ev) >= 1
    )
    presses = [e for e in events if e["type"] == "button"]
    assert presses[0]["button"] == 3 and presses[0]["down"]
    assert presses[0]["state"] & 0x1, "shift was held when the button went down"
    assert time.time() - started >= 0.5
    keys = [(e["keysym"], e["down"]) for e in events if e["type"] == "key"]
    assert keys[0] == (0xFFE1, True) and keys[-1] == (0xFFE1, False)  # Shift_L down ... up


def test_keys_reach_the_window_with_the_right_symbols(game, window_log):
    game.press_key("f2")
    game.hotkey("inventory")
    game.set_speed("fast")  # the speed key alone: it sets that speed whatever the game was doing
    game.set_speed("pause")  # normal speed, then the pause key
    events = _wait_for(
        window_log, lambda ev: sum(e["type"] == "key" and e["down"] for e in ev) >= 5
    )
    downs = [e["keysym"] for e in events if e["type"] == "key" and e["down"]]
    assert downs == [0xFFBF, ord("i"), 0xFFC0, 0xFFBF, ord(" ")]  # F2, i, F3, F2, space


def test_typing_uses_shift_for_capitals(game, window_log):
    game.type_text("Ab 1")
    events = _wait_for(
        window_log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev) >= 5
    )
    downs = [e["keysym"] for e in events if e["type"] == "key" and e["down"]]
    assert downs == [0xFFE1, ord("a"), ord("b"), ord(" "), ord("1")]


def test_scroll_and_drag(game, window_log):
    game.scroll(400, 300, "up", 2)
    game.drag(200, 200, 500, 400)
    events = _wait_for(
        window_log,
        lambda ev: sum(e["type"] == "button" and e["button"] == 1 and not e["down"] for e in ev) >= 1,
    )
    wheel = [e for e in events if e["type"] == "button" and e["button"] == 4 and e["down"]]
    assert len(wheel) == 2 and (wheel[0]["x"], wheel[0]["y"]) == (400, 300)
    left = [e for e in events if e["type"] == "button" and e["button"] == 1]
    assert (left[0]["x"], left[0]["y"], left[0]["down"]) == (200, 200, True)
    assert (left[-1]["x"], left[-1]["y"], left[-1]["down"]) == (500, 400, False)
    dragged = [e for e in events if e["type"] == "motion" and e["state"] & 0x100]
    assert dragged, "pointer motion was seen while the left button was down"


def _right_button(events: list[dict]) -> list[tuple]:
    return [(e["down"], e["x"], e["y"]) for e in events if e["type"] == "button" and e["button"] == 3]


def test_the_right_button_stays_down_from_menu_open_until_a_row_is_chosen(game, window_log):
    opened = game.menu_open(300, 250)
    events = _wait_for(window_log, lambda ev: any(e["type"] == "button" for e in ev))
    assert _right_button(events) == [(True, 300, 250)] and game.menu_held
    assert "IT IS STILL DOWN" in opened.text
    game.zoom(250, 200, 450, 400)  # looking leaves it down
    time.sleep(0.3)
    assert _right_button(_events(window_log)) == [(True, 300, 250)]
    game.menu_choose(340, 320)
    events = _wait_for(window_log, lambda ev: len(_right_button(ev)) == 2)
    assert _right_button(events) == [(True, 300, 250), (False, 340, 320)] and not game.menu_held
    dragged = [e for e in events if e["type"] == "motion" and e["state"] & 0x400]
    assert dragged, "the pointer moved to the row with the right button down"


def test_a_held_menu_is_let_go_by_another_action_and_by_closing(game, window_log, tmp_path):
    game.menu_open(300, 250)
    pressed = game.press_key("i")
    events = _wait_for(window_log, lambda ev: any(e["type"] == "key" for e in ev))
    assert "closed without a choice" in pressed.text
    released = [e for e in events if e["type"] in ("button", "key")]
    assert (released[1]["type"], released[1]["down"]) == ("button", False), "the button came up before the key went down"
    leaving = Controller(Config(backend="x11", data_dir=tmp_path / "home2", settle_seconds=0.1))
    leaving.menu_open(500, 400)
    leaving.close()  # as at shutdown
    events = _wait_for(window_log, lambda ev: len(_right_button(ev)) == 4)
    assert _right_button(events)[-2:] == [(True, 500, 400), (False, 500, 400)]


def test_a_click_on_the_edge_of_the_window_does_not_leave_the_pointer_there(game, window_log):
    game.click(400, 599)
    events = _wait_for(window_log, lambda ev: sum(e["type"] == "button" and not e["down"] for e in ev) >= 1)
    clicked = [e for e in events if e["type"] == "button"]
    assert (clicked[0]["x"], clicked[0]["y"]) == (400, 594), "as near the edge as a click goes"
    time.sleep(0.2)
    resting = [e for e in _events(window_log) if e["type"] == "motion"][-1]
    assert (resting["x"], resting["y"]) == (400, 590), "then 1.5% of the height in from it"


def test_no_window_is_reported_clearly(tmp_path):
    config = Config(backend="x11", data_dir=tmp_path / "home", x11_class_regex="no-such-game")
    controller = Controller(config)
    try:
        with pytest.raises(ControlError, match="No Kenshi window"):
            controller.observe()
    finally:
        controller.close()
