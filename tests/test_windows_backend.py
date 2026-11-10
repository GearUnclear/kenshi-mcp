"""Drives the real Windows backend against a real Win32 window. Runs on Windows (or under
Wine) only; everywhere else the module is skipped. Real input is sent while it runs.

Conditions that cannot be produced on a test machine (a locked desktop, a game running
as administrator, Windows refusing input) are imitated by replacing the one Win32 call
that reports them."""

from __future__ import annotations

import ctypes
import io
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest
from PIL import Image

if sys.platform != "win32":
    pytest.skip("needs Windows", allow_module_level=True)

from kenshi_link.backends import _win_structs as ws  # noqa: E402
from kenshi_link.backends import windows  # noqa: E402
from kenshi_link.backends.base import BackendError, DesktopUnavailable, WindowNotFound  # noqa: E402
from kenshi_link.config import Config  # noqa: E402
from kenshi_link.controller import HALT_MARKER, ControlError, Controller, Halted  # noqa: E402
from kenshi_link.keys import char_to_key  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "win_window.py"
LEFT, TOP, WIDTH, HEIGHT = 100, 50, 800, 600  # where the fixture puts its window
WM_APP = 0x8000
VK_CONTROL, VK_CANCEL, VK_PAUSE, VK_CAPITAL = 0x11, 0x03, 0x13, 0x14

user32 = windows.user32
user32.PostMessageW.argtypes = (ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t)


def events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def wait_for(path: Path, predicate, timeout: float = 8.0) -> list[dict]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        seen = events(path)
        if predicate(seen):
            return seen
        time.sleep(0.05)
    raise AssertionError(f"timed out; last events: {events(path)[-10:]}")


def start_window(log: Path, *arguments: str) -> subprocess.Popen:
    process = subprocess.Popen([sys.executable, str(FIXTURE), str(log), *arguments])
    try:
        wait_for(log, lambda seen: any(e["type"] == "ready" for e in seen), timeout=20)
    except BaseException:
        process.kill()
        raise
    time.sleep(0.3)  # the first paint
    return process


def stop_window(process: subprocess.Popen) -> None:
    process.terminate()
    process.wait(timeout=10)


@pytest.fixture
def window_log(tmp_path):
    log = tmp_path / "events.jsonl"
    process = start_window(log)
    try:
        yield log
    finally:
        stop_window(process)


@pytest.fixture
def config(tmp_path) -> Config:
    # The stand-in window belongs to python.exe rather than kenshi_x64.exe.
    cfg = Config(backend="windows", data_dir=tmp_path / "home", settle_seconds=0.1,
                 process_regex=r"(?i)^python.*\.exe$", failsafe_corner=False, panic_key=False)
    cfg.validate()
    return cfg


@pytest.fixture
def backend(config, window_log):
    backend = windows.WindowsBackend(config)
    backend.locate()
    yield backend
    backend.close()


@pytest.fixture
def game(config, window_log):
    controller = Controller(config)
    yield controller
    controller.close()


def tap(vk: int, *, held: int = 0) -> None:
    """Press a key the way a keyboard driver reports it: by virtual key, not through KEYS."""
    sequence = ([(held, True)] if held else []) + [(vk, True), (vk, False)] + ([(held, False)] if held else [])
    for key, down in sequence:
        event = ws.INPUT()
        event.type = ws.INPUT_KEYBOARD
        event.ki = ws.KEYBDINPUT(key, 0, 0 if down else ws.KEYEVENTF_KEYUP, 0, 0)
        assert user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(ws.INPUT)) == 1
        time.sleep(0.03)


# ---- the pointer -----------------------------------------------------------------------


SETTLE = 0.02  # Wine hears of pointer moves back from the X server, a moment after making them


def test_every_move_lands_on_the_pixel_asked_for(backend):
    left, top, width, height = backend.screen_rect()
    points = [(x, top + 7 + x % 400) for x in range(left, left + width, 29)]
    points += [(left + 11 + y % 500, y) for y in range(top, top + height, 17)]
    points += [(left + 3, top + 3), (left + width - 1, top + height - 1), (left + 1, top + 5), (left + 5, top + 1)]
    missed = []
    for point in points:
        backend.move(*point)
        time.sleep(SETTLE)
        if backend.cursor() != point:
            missed.append((point, backend.cursor()))
    assert not missed, "the 0..65535 mapping must be exact: (asked for, got)"


def test_a_pointer_left_off_target_is_put_right_with_motion_a_game_can_see(backend, window_log, monkeypatch):
    backend.move(LEFT + 418, TOP + 240)  # as if aiming at (420, 240) had landed two pixels short
    time.sleep(0.15)
    sent, send = [], backend._send
    monkeypatch.setattr(backend, "_send", lambda event: (sent.append((event.mi.dx, event.mi.dy, event.mi.dwFlags)),
                                                          send(event))[1])
    before = len(events(window_log))
    backend.place(LEFT + 420, TOP + 240)
    # One pixel aside and back, as relative movement. A mouse read through DirectInput
    # reports that; it reports nothing for SetCursorPos, or for a move of zero pixels.
    assert sent == [(1, 0, ws.MOUSEEVENTF_MOVE), (-1, 0, ws.MOUSEEVENTF_MOVE)]
    assert backend.corrections == 1

    def motion(seen: list[dict]) -> list[tuple[int, int]]:
        return [(e["x"], e["y"]) for e in seen[before:] if e["type"] == "motion"]

    visited = motion(wait_for(window_log, lambda seen: motion(seen)[-1:] == [(420, 240)]))
    assert (419, 240) in visited, "the step aside was real movement"
    time.sleep(0.15)
    assert backend.cursor() == (LEFT + 420, TOP + 240)


def test_the_controller_puts_right_a_move_that_fell_short_before_it_clicks(game, window_log, monkeypatch):
    exact = ws.absolute_coords
    # Every move lands two pixels left of where it was aimed: rounding Windows might do.
    monkeypatch.setattr(ws, "absolute_coords", lambda x, y, virtual: exact(x - 2, y, virtual))
    game.click(321, 234)
    seen = wait_for(window_log, lambda seen: any(e["type"] == "button" and not e["down"] for e in seen))
    assert [(e["x"], e["y"], e["down"]) for e in seen if e["type"] == "button"] == [(321, 234, True), (321, 234, False)]
    assert game.backend.corrections == 1


def test_the_failsafe_corner_and_the_desktop_bounds_come_from_the_monitors(backend):
    left, top, width, height = backend.screen_rect()
    assert width >= 800 and height >= 600
    corner = backend.failsafe_corner()
    assert corner[0] == left and top <= corner[1] < top + height
    assert backend.failsafe_corner() == corner  # the second answer comes from the cache


def test_the_pointer_is_known_to_be_over_the_game_or_not(backend, tmp_path):
    backend.move(LEFT + 400, TOP + 300)
    assert backend.pointer_on_window()
    backend.move(LEFT + WIDTH + 60, TOP + HEIGHT + 60)  # bare desktop beside the window
    assert not backend.pointer_on_window()
    overlay_log = tmp_path / "overlay.jsonl"
    overlay = start_window(overlay_log, "overlay", str(LEFT + 500), str(TOP + 400), "250", "120")
    try:
        backend.move(LEFT + 600, TOP + 450)  # over the notification that lies on the game
        assert not backend.pointer_on_window()
        backend.move(LEFT + 200, TOP + 200)
        assert backend.pointer_on_window()
    finally:
        stop_window(overlay)


def test_a_click_where_another_window_covers_the_game_is_not_sent(game, window_log, tmp_path):
    overlay_log = tmp_path / "overlay.jsonl"
    overlay = start_window(overlay_log, "overlay", str(LEFT + 500), str(TOP + 400), "250", "120")
    try:
        with pytest.raises(ControlError, match="covering the game"):
            game.click(600, 450, modifiers="shift")
        with pytest.raises(ControlError, match="covering the game"):
            game.scroll(600, 450, "up", 2)
        game.click(200, 200)  # beside it, the game is still clickable
        seen = wait_for(window_log, lambda seen: any(e["type"] == "button" and not e["down"] for e in seen))
        assert [(e["x"], e["y"]) for e in seen if e["type"] == "button"] == [(200, 200), (200, 200)]
        assert not [e for e in seen if e["type"] == "wheel"]
        keys = [(e["vk"], e["down"]) for e in seen if e["type"] == "key"]
        assert keys == [(0x10, True), (0x10, False)], "shift went down and came back up"
        assert not [e for e in events(overlay_log) if e["type"] in ("button", "wheel")]
    finally:
        stop_window(overlay)


def test_a_window_hanging_off_the_desktop_is_refused(game, monkeypatch):
    left, top, width, height = game.backend.screen_rect()
    monkeypatch.setattr(game.backend, "screen_rect", lambda: (left, top, LEFT + WIDTH - 10, height))
    with pytest.raises(ControlError, match="partly off the screen"):
        game.click(200, 200)


# ---- finding the window ------------------------------------------------------------------


def test_the_window_is_found_captured_and_focused_again(game, backend, tmp_path):
    result = game.observe()
    image = Image.open(io.BytesIO(result.images[-1].data)).convert("RGB")
    assert image.size == (WIDTH, HEIGHT)
    assert all(abs(a - b) <= 40 for a, b in zip(image.getpixel((50, 50)), (255, 0, 0)))
    # Another program's window takes the foreground, as when the operator clicks elsewhere.
    other_log = tmp_path / "other.jsonl"
    other = start_window(other_log, "overlay", "950", "100", "200", "200")
    try:
        user32.SetForegroundWindow(events(other_log)[0]["hwnd"])
        time.sleep(0.3)
        assert not backend.locate().focused
        backend.focus()
        time.sleep(0.3)
        assert backend.locate().focused and backend.focus_error() == ""
    finally:
        stop_window(other)


def test_the_runner_brings_the_game_forward_before_it_starts_the_server(config, window_log, tmp_path):
    from kenshi_link import agent

    other_log = tmp_path / "other.jsonl"
    other = start_window(other_log, "overlay", "950", "100", "200", "200")
    probe = windows.WindowsBackend(config)
    try:
        user32.SetForegroundWindow(events(other_log)[0]["hwnd"])
        time.sleep(0.3)
        assert not probe.locate().focused
        agent._let_the_server_take_focus()  # must be harmless whatever this process is allowed
        agent._bring_game_forward(config)
        time.sleep(0.3)
        assert probe.locate().focused
        user32.SetForegroundWindow(events(other_log)[0]["hwnd"])
        time.sleep(0.3)
        config.auto_focus = False  # the operator's choice is respected here too
        agent._bring_game_forward(config)
        time.sleep(0.3)
        assert not probe.locate().focused
    finally:
        probe.close()
        stop_window(other)


def test_a_handle_that_now_belongs_to_another_program_is_looked_up_again(backend, monkeypatch):
    hwnd, pid = backend._hwnd, backend._pid
    assert hwnd and pid
    backend._pid = pid + 4  # as if the game had closed and Windows had reused its window handle
    monkeypatch.setattr(backend, "_find", lambda: (_ for _ in ()).throw(WindowNotFound("No Kenshi window found.")))
    with pytest.raises(WindowNotFound):
        backend.locate()
    monkeypatch.undo()
    assert backend.locate().width == WIDTH and (backend._hwnd, backend._pid) == (hwnd, pid)


def test_a_game_that_has_stopped_answering_is_reported_and_left_alone(game, window_log):
    game.observe()
    hwnd = game.backend._hwnd
    assert not user32.IsHungAppWindow(hwnd)
    user32.PostMessageW(hwnd, WM_APP, 8000, 0)  # the window stops reading its messages for 8 s
    wait_for(window_log, lambda seen: any(e["type"] == "busy" for e in seen))
    deadline = time.time() + 7.5
    while time.time() < deadline and not user32.IsHungAppWindow(hwnd):
        time.sleep(0.25)
    before = len(events(window_log))
    with pytest.raises(ControlError, match="not responding") as error:
        game.press_key("i")
    assert not isinstance(error.value, Halted)
    assert "window: UNUSABLE - Kenshi is not responding" in game.describe()
    wait_for(window_log, lambda seen: any(e["type"] == "answering" for e in seen), timeout=12)
    time.sleep(0.5)
    assert not [e for e in events(window_log)[before:] if e["type"] == "key"], "no key was queued up for it"
    game.press_key("i")  # and it is usable again without anything being reset
    wait_for(window_log, lambda seen: any(e["type"] == "key" and e["vk"] == 0x49 for e in seen[before:]))


def test_the_same_report_when_windows_says_the_window_is_hung(backend, monkeypatch):
    monkeypatch.setattr(user32, "IsHungAppWindow", lambda hwnd: 1)
    with pytest.raises(BackendError, match="not responding"):
        backend.locate()
    with pytest.raises(BackendError, match="not responding"):
        backend.focus()


# ---- privilege and the desktop -----------------------------------------------------------


def test_elevation_is_read_for_this_process_and_for_the_game(backend):
    ours = windows._elevated(windows.kernel32.GetCurrentProcess())
    assert ours in (True, False)
    assert windows._process_elevated(backend._pid) == ours  # the test window is our own child
    assert windows._process_elevated(0xFFFFFFF0) is not True  # no such process: no claim either way


@pytest.mark.parametrize(("theirs", "wording"), [(True, "Kenshi is running as administrator"),
                                                 (None, "Kenshi appears to be running as administrator")])
def test_a_game_running_as_administrator_is_refused_before_any_input(config, window_log, monkeypatch, theirs, wording):
    monkeypatch.setattr(windows, "_elevated", lambda process: False)
    monkeypatch.setattr(windows, "_process_elevated", lambda pid: theirs)
    game = Controller(config)
    try:
        with pytest.raises(ControlError, match=wording):
            game.click(200, 200)
        report = game.describe()
        assert "window: UNUSABLE - " in report and "silently discards" in report
    finally:
        game.close()
    time.sleep(0.3)
    assert not [e for e in events(window_log) if e["type"] in ("button", "key", "wheel")]


def test_a_locked_desktop_is_told_apart_from_other_failures(backend, monkeypatch):
    assert windows._desktop_available()
    backend.capture(LEFT, TOP, 50, 50)

    monkeypatch.setattr(user32, "GetCursorPos", lambda point: 0)
    with pytest.raises(BackendError, match=r"pointer position \(error \d+\)") as error:
        backend.cursor()
    assert not isinstance(error.value, DesktopUnavailable)
    monkeypatch.undo()

    monkeypatch.setattr(user32, "SendInput", lambda count, event, size: 0)
    refusal = r"did not accept the input \(SendInput inserted nothing, error \d+\)"
    with pytest.raises(BackendError, match=refusal) as error:
        backend.key("i", True)
    assert not isinstance(error.value, DesktopUnavailable) and "administrator" not in str(error.value)
    monkeypatch.undo()

    def broken_grab(_area):
        raise OSError("BitBlt failed")

    monkeypatch.setattr(backend._sct, "grab", broken_grab)
    with pytest.raises(BackendError, match=r"could not be captured \(BitBlt failed\)") as error:
        backend.capture(LEFT, TOP, 50, 50)
    assert not isinstance(error.value, DesktopUnavailable)
    assert backend.capture(LEFT, TOP, 50, 50).size == (50, 50), "capture starts afresh after a failure"

    # The lock screen, a UAC prompt and the screen saver each take input to another desktop,
    # which this program cannot open (the first two) or which has another name (the third).
    names = iter(["Screen-saver", "Default"])
    for imitate in (lambda: monkeypatch.setattr(user32, "OpenInputDesktop", lambda *args: None),
                    lambda: monkeypatch.setattr(windows, "_object_name", lambda handle: next(names))):
        imitate()
        assert not windows._desktop_available()
        monkeypatch.undo()
    monkeypatch.setattr(windows, "_desktop_available", lambda: False)
    monkeypatch.setattr(user32, "GetCursorPos", lambda point: 0)
    monkeypatch.setattr(user32, "SendInput", lambda count, event, size: 0)
    monkeypatch.setattr(backend._sct, "grab", broken_grab)
    for blocked in (backend.locate, backend.cursor, lambda: backend.key("i", True), lambda: backend.move(300, 300),
                    lambda: backend.capture(LEFT, TOP, 50, 50)):
        with pytest.raises(DesktopUnavailable, match="desktop is not available"):
            blocked()


def test_a_locked_desktop_halts_the_controller_without_a_stop_file(game, config, monkeypatch):
    game.observe()
    monkeypatch.setattr(windows, "_desktop_available", lambda: False)
    game.observe()  # one sign alone (here: another desktop has the input) is not believed
    monkeypatch.setattr(user32, "GetCursorPos", lambda point: 0)
    with pytest.raises(Halted, match=HALT_MARKER):
        game.click(200, 200)
    assert not config.stop_file.exists()
    monkeypatch.undo()
    game.observe()


# ---- the operator's stop key -------------------------------------------------------------


def test_a_tap_of_pause_is_caught_however_short(config, window_log):
    presses: list[float] = []
    backend = windows.WindowsBackend(config)
    try:
        backend.watch_panic(lambda: presses.append(time.time()))
        assert any("registered as a hotkey" in line for line in backend.notes())
        tap(VK_PAUSE)
        deadline = time.time() + 3
        while not presses and time.time() < deadline:
            time.sleep(0.02)
        assert len(presses) == 1
        assert not backend.panic_pressed(), "the key is up again: polling would have missed it"
        tap(VK_CANCEL, held=VK_CONTROL)  # Ctrl+Pause arrives as Break
        deadline = time.time() + 3
        while len(presses) < 2 and time.time() < deadline:
            time.sleep(0.02)
        assert len(presses) == 2

        second = windows.WindowsBackend(config)  # another kenshi-link while the first is running
        try:
            second.watch_panic(lambda: None)
            assert any("could not be registered as a hotkey (error 1409" in line for line in second.notes())
        finally:
            second.close()
    finally:
        backend.close()
    again = windows.WindowsBackend(config)  # closing gave the key back
    try:
        again.watch_panic(lambda: None)
        assert any("registered as a hotkey" in line for line in again.notes())
    finally:
        again.close()


def test_a_tap_of_pause_between_actions_halts_the_next_one(config, window_log):
    config.panic_key = True
    game = Controller(config)
    try:
        game.observe()
        tap(VK_PAUSE)
        deadline = time.time() + 3
        while not config.stop_file.exists() and time.time() < deadline:
            time.sleep(0.02)
        assert config.stop_file.read_text(encoding="utf-8").startswith("the operator pressed Pause/Break")
        before = len(events(window_log))
        with pytest.raises(Halted, match="the operator pressed Pause/Break"):
            game.click(200, 200)
        time.sleep(0.3)
        assert not [e for e in events(window_log)[before:] if e["type"] == "button"]
    finally:
        game.close()


# ---- the keyboard ------------------------------------------------------------------------


def us_layout(backend) -> bool:
    sample = "abcdefghijklmnopqrstuvwxyz0123456789"
    return backend.typing_keys(sample) == [char_to_key(char) for char in sample]


def test_typing_is_planned_from_the_layout_and_arrives_as_the_characters_asked_for(game, window_log):
    text = "Camp-1 [x] ok!"
    if us_layout(game.backend):
        assert game.backend.typing_keys(text) == [char_to_key(char) for char in text]
        assert not [line for line in game.backend.notes() if line.startswith("keyboard layout")]
    game.type_text(text)
    seen = wait_for(window_log, lambda seen: sum(e["type"] == "char" for e in seen) >= len(text))
    assert "".join(e["char"] for e in seen if e["type"] == "char") == text


def test_caps_lock_is_seen(game, window_log):
    if game.backend.caps_lock():
        pytest.skip("Caps Lock is on")
    game.observe()
    tap(VK_CAPITAL)
    try:
        time.sleep(0.2)
        assert game.backend.caps_lock()
        with pytest.raises(ControlError, match="Caps Lock is on"):
            game.type_text("Hub")
    finally:
        tap(VK_CAPITAL)
    time.sleep(0.2)
    assert not game.backend.caps_lock()
    time.sleep(0.3)
    assert not [e for e in events(window_log) if e["type"] == "char"]
