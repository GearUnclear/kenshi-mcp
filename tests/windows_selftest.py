"""Self-test for the Windows backend. Run it on Windows (or under Wine):

    python tests/windows_selftest.py

It opens a small stand-in window, drives it through the same controller the game
uses, and checks that what the window received matches what was sent: window
discovery, screen capture, pointer position, buttons, the wheel, scancodes.
It does not need Kenshi and does not touch any other window.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from PIL import Image  # noqa: E402

from kenshi_link.backends import _win_structs as ws  # noqa: E402
from kenshi_link.config import Config  # noqa: E402
from kenshi_link.controller import ControlError, Controller  # noqa: E402

VK = {"f2": 0x71, "i": 0x49, "space": 0x20, "shift": 0x10, "a": 0x41, "b": 0x42, "1": 0x31,
      "up": 0x26, "w": 0x57}
SCAN = {"f2": 0x3C, "i": 0x17, "space": 0x39, "up": 0x48, "w": 0x11}


def events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def wait_for(path: Path, predicate, what: str, timeout: float = 8.0) -> list[dict]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        seen = events(path)
        if predicate(seen):
            return seen
        time.sleep(0.05)
    raise AssertionError(f"timed out waiting for {what}; saw {events(path)[-12:]}")


def near(pixel, expected, tolerance=40) -> bool:
    return all(abs(a - b) <= tolerance for a, b in zip(pixel, expected))


def check(name: str, condition: bool, detail: object = "") -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {name}" + (f"  {detail}" if not condition else ""))
    if not condition:
        raise AssertionError(name)


def main() -> int:
    if sys.platform != "win32":
        print("This self-test is for Windows.")
        return 2
    import ctypes

    check("INPUT struct is 40 bytes", ctypes.sizeof(ws.INPUT) == 40, ctypes.sizeof(ws.INPUT))

    work = Path(tempfile.mkdtemp(prefix="kenshi-link-selftest-"))
    log = work / "events.jsonl"
    window = subprocess.Popen([sys.executable, str(HERE / "fixtures" / "win_window.py"), str(log)])
    try:
        wait_for(log, lambda ev: any(e["type"] == "ready" for e in ev), "the test window")
        time.sleep(0.5)

        # The stand-in window belongs to python.exe rather than kenshi_x64.exe.
        config = Config(backend="windows", data_dir=work / "home", settle_seconds=0.15,
                        process_regex=r"(?i)^python.*\.exe$", failsafe_corner=False)
        config.validate()
        game = Controller(config)

        print("window and capture")
        result = game.observe()
        image = Image.open(io.BytesIO(result.images[-1].data)).convert("RGB")
        check("client area found as 800x600", image.size == (800, 600), image.size)
        check("red square captured at top-left", near(image.getpixel((50, 50)), (255, 0, 0)),
              image.getpixel((50, 50)))
        check("blue background captured", near(image.getpixel((400, 300)), (0x20, 0x40, 0x80)),
              image.getpixel((400, 300)))

        print("pointer")
        game.click(321, 234)
        seen = wait_for(log, lambda ev: any(e["type"] == "button" and not e["down"] for e in ev),
                        "a left click")
        presses = [e for e in seen if e["type"] == "button"]
        check("left down then up", [(e["button"], e["down"]) for e in presses] == [("left", True), ("left", False)],
              presses)
        check("click landed on the requested pixel", (presses[0]["x"], presses[0]["y"]) == (321, 234),
              (presses[0]["x"], presses[0]["y"]))

        before = len(events(log))
        started = time.time()
        game.click(600, 100, button="right", modifiers="shift", hold_seconds=0.5)
        seen = wait_for(log, lambda ev: any(e["type"] == "button" and e["button"] == "right" and not e["down"]
                                            for e in ev[before:]), "a right click")[before:]
        right = [e for e in seen if e["type"] == "button"]
        check("right button pressed at (600, 100)", (right[0]["button"], right[0]["x"], right[0]["y"]) == ("right", 600, 100),
              right)
        check("shift held during the click", right[0]["shift"], right[0])
        check("button was held for the requested time", time.time() - started >= 0.5)

        before = len(events(log))
        game.scroll(400, 300, "up", 2)
        game.scroll(400, 300, "down", 1)
        seen = wait_for(log, lambda ev: sum(e["type"] == "wheel" for e in ev[before:]) >= 3, "wheel events")[before:]
        check("wheel deltas", [e["delta"] for e in seen if e["type"] == "wheel"] == [120, 120, -120],
              [e["delta"] for e in seen if e["type"] == "wheel"])

        before = len(events(log))
        game.drag(200, 200, 500, 400)
        seen = wait_for(log, lambda ev: any(e["type"] == "button" and not e["down"] for e in ev[before:]),
                        "a drag")[before:]
        left = [e for e in seen if e["type"] == "button"]
        check("drag starts at (200, 200)", (left[0]["x"], left[0]["y"], left[0]["down"]) == (200, 200, True), left[0])
        check("drag ends at (500, 400)", (left[-1]["x"], left[-1]["y"], left[-1]["down"]) == (500, 400, False), left[-1])
        check("motion seen with the button down", any(e["type"] == "motion" and e["left_down"] for e in seen))

        print("keyboard")
        before = len(events(log))
        game.press_key("f2")
        game.hotkey("inventory")
        game.press_key("up")
        game.camera("forward", 1)
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 4,
                        "key presses")[before:]
        downs = [e for e in seen if e["type"] == "key" and e["down"]]
        check("virtual keys f2, i, up, w", [e["vk"] for e in downs] == [VK["f2"], VK["i"], VK["up"], VK["w"]],
              [hex(e["vk"]) for e in downs])
        check("scancodes match", [e["scancode"] for e in downs] == [SCAN["f2"], SCAN["i"], SCAN["up"], SCAN["w"]],
              [hex(e["scancode"]) for e in downs])
        check("arrow key flagged extended", downs[2]["extended"] and not downs[0]["extended"], downs)

        before = len(events(log))
        game.type_text("Ab 1")
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 5,
                        "typed text")[before:]
        typed = [e["vk"] for e in seen if e["type"] == "key" and e["down"]]
        check("typing sends shift, a, b, space, 1",
              typed == [VK["shift"], VK["a"], VK["b"], VK["space"], VK["1"]], [hex(v) for v in typed])

        print("time control")
        before = len(events(log))
        game.advance(1.0, "fast", frames=1)
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 3,
                        "advance keys")[before:]
        keys = [e["vk"] for e in seen if e["type"] == "key" and e["down"]]
        check("advance = unpause, fast speed, pause", keys == [VK["space"], 0x72, VK["space"]], [hex(v) for v in keys])

        print("safety")
        try:
            game.press_key("alt+f4")
            check("alt+f4 refused", False)
        except ControlError:
            check("alt+f4 refused", True)
        game.close()
    finally:
        window.terminate()
        window.wait(timeout=5)

    config = Config(backend="windows", data_dir=work / "home2", process_regex=r"(?i)^python.*\.exe$",
                    auto_focus=False)
    game = Controller(config)
    try:
        game.observe()
        check("missing window reported", False)
    except ControlError as exc:
        check("missing window reported", "No Kenshi window" in str(exc), exc)
    game.close()

    print("All Windows backend checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
