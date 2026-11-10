"""Self-test for the Windows backend. Run it on Windows (or under Wine):

    python tests/windows_selftest.py

It opens a small stand-in window, drives it through the same controller the game
uses, and checks that what the window received matches what was sent: window
discovery, screen capture, pointer position, buttons, the wheel, scancodes, typed
characters and timing. It does not need Kenshi and does not touch any other window.
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

# Set-1 scancodes: the physical keys, whatever the keyboard layout prints on them.
SCAN = {"f2": 0x3C, "i": 0x17, "up": 0x48, "w": 0x11}
VK_SPACE, VK_F2, VK_F3, VK_UP, VK_SHIFT = 0x20, 0x71, 0x72, 0x26, 0x10
FIXTURE = HERE / "fixtures" / "win_window.py"


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


def note(text: str) -> None:
    """Something worth knowing that is not a failure of this program."""
    print(f"  note {text}")


def main() -> int:
    if sys.platform != "win32":
        print("This self-test is for Windows.")
        return 2
    import ctypes

    def layout_vk(scancode: int) -> int:
        """The virtual key this PC's keyboard layout gives a physical key."""
        return ctypes.windll.user32.MapVirtualKeyW(scancode, 1)  # MAPVK_VSC_TO_VK

    check("INPUT struct is 40 bytes", ctypes.sizeof(ws.INPUT) == 40, ctypes.sizeof(ws.INPUT))

    work = Path(tempfile.mkdtemp(prefix="kenshi-link-selftest-"))
    log = work / "events.jsonl"
    window = subprocess.Popen([sys.executable, str(FIXTURE), str(log)])
    overlay = None
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
        for line in game.backend.notes():
            note(line)

        print("pointer")
        game.click(321, 234)
        seen = wait_for(log, lambda ev: any(e["type"] == "button" and not e["down"] for e in ev),
                        "a left click")
        presses = [e for e in seen if e["type"] == "button"]
        check("left down then up", [(e["button"], e["down"]) for e in presses] == [("left", True), ("left", False)],
              presses)
        check("click landed on the requested pixel", (presses[0]["x"], presses[0]["y"]) == (321, 234),
              (presses[0]["x"], presses[0]["y"]))
        arrived = [e for e in seen if e["type"] == "motion" and e["time"] <= presses[0]["time"]][-1]
        check("pointer rested on the spot before the button went down",
              presses[0]["time"] - arrived["time"] >= config.pointer_dwell_seconds - 0.04,
              round(presses[0]["time"] - arrived["time"], 3))
        check("button stayed down for a slow frame",
              presses[1]["time"] - presses[0]["time"] >= config.click_hold_seconds - 0.04,
              round(presses[1]["time"] - presses[0]["time"], 3))

        before = len(events(log))
        started = time.time()
        game.click(600, 100, button="right", modifiers="shift", hold_seconds=0.5)
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 1,
                        "a shift+right click")[before:]
        right = [e for e in seen if e["type"] == "button"]
        shift = [e for e in seen if e["type"] == "key"]
        check("right button pressed at (600, 100)", (right[0]["button"], right[0]["x"], right[0]["y"]) == ("right", 600, 100),
              right)
        check("shift held during the click", right[0]["shift"], right[0])
        check("button was held for the requested time", time.time() - started >= 0.5)
        gaps = (right[0]["time"] - shift[0]["time"], shift[-1]["time"] - right[-1]["time"])
        check("shift went down well before the button and up well after",
              shift[0]["down"] and not shift[-1]["down"] and min(gaps) >= config.modifier_gap_seconds - 0.04,
              [round(gap, 3) for gap in gaps])

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

        # Windows does not document how it rounds pointer coordinates. The controller checks
        # every move and puts the pointer right if need be; this says whether it had to.
        info = game.backend.locate()
        missed = []
        for step in range(40):
            point = (info.left + 5 + step * 19, info.top + 5 + step * 14)
            game.backend.move(*point)
            time.sleep(0.02)
            if game.backend.cursor() != point:
                missed.append((point, game.backend.cursor()))
        if missed or game.backend.corrections:
            note(f"{len(missed)} of 40 pointer moves landed off the pixel asked for, e.g. {missed[:3]}; "
                 f"{game.backend.corrections} were put right during the checks above. Clicks are still "
                 "exact, but please report this with your screen resolution.")
        else:
            check("pointer moves land on the exact pixel without correction", True)

        print("another window on top")
        overlay_log = work / "overlay.jsonl"
        overlay = subprocess.Popen([sys.executable, str(FIXTURE), str(overlay_log), "overlay",
                                    str(info.left + 500), str(info.top + 400), "250", "120"])
        wait_for(overlay_log, lambda ev: any(e["type"] == "ready" for e in ev), "the covering window")
        time.sleep(0.5)
        before = len(events(log))
        try:
            game.click(600, 450)
            refused = False
        except ControlError as exc:
            refused = "covering the game" in str(exc)
        time.sleep(0.3)
        check("click on a covered spot refused", refused)
        check("... and it reached neither window",
              not [e for e in events(log)[before:] + events(overlay_log) if e["type"] == "button"])
        game.click(200, 200)
        seen = wait_for(log, lambda ev: any(e["type"] == "button" and not e["down"] for e in ev[before:]),
                        "a click beside the covering window")[before:]
        check("click beside it still lands", [(e["x"], e["y"]) for e in seen if e["type"] == "button"][:1] == [(200, 200)])
        overlay.terminate()
        overlay.wait(timeout=5)
        overlay = None

        print("keyboard")
        before = len(events(log))
        game.press_key("f2")
        game.hotkey("inventory")
        game.press_key("up")
        game.camera("forward", 1)
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 4,
                        "key presses")[before:]
        downs = [e for e in seen if e["type"] == "key" and e["down"]]
        check("scancodes f2, i, up, w", [e["scancode"] for e in downs] == [SCAN["f2"], SCAN["i"], SCAN["up"], SCAN["w"]],
              [hex(e["scancode"]) for e in downs])
        expected = [layout_vk(SCAN["f2"]), layout_vk(SCAN["i"]), VK_UP, layout_vk(SCAN["w"])]
        check("virtual keys are what this keyboard layout gives those keys", [e["vk"] for e in downs] == expected,
              ([hex(e["vk"]) for e in downs], [hex(vk) for vk in expected]))
        check("arrow key flagged extended", downs[2]["extended"] and not downs[0]["extended"], downs)
        ups = [e for e in seen if e["type"] == "key" and not e["down"]]
        check("key stayed down for a slow frame", ups[0]["time"] - downs[0]["time"] >= config.key_hold_seconds - 0.04,
              round(ups[0]["time"] - downs[0]["time"], 3))

        before = len(events(log))
        text = "Ab 1, ok?"
        game.type_text(text)
        seen = wait_for(log, lambda ev: sum(e["type"] == "char" for e in ev[before:]) >= len(text),
                        "typed text")[before:]
        typed = "".join(e["char"] for e in seen if e["type"] == "char")
        check(f"typing arrives as the characters {text!r}", typed == text, typed)
        check("capitals are typed with shift", [e["vk"] for e in seen if e["type"] == "key" and e["down"]][0] == VK_SHIFT)

        print("time control")
        before = len(events(log))
        game.advance(1.0, "fast", frames=1)
        seen = wait_for(log, lambda ev: sum(e["type"] == "key" and not e["down"] for e in ev[before:]) >= 3,
                        "advance keys")[before:]
        keys = [e["vk"] for e in seen if e["type"] == "key" and e["down"]]
        check("advance = fast speed, then normal speed and pause", keys == [VK_F3, VK_F2, VK_SPACE],
              [hex(v) for v in keys])
        print("safety")
        for combo in ("alt+f4", "ctrl+alt+f4", "alt+shift"):
            try:
                game.press_key(combo)
                check(f"{combo} refused", False)
            except ControlError:
                check(f"{combo} refused", True)
        before = len(events(log))
        config.stop_file.write_text("self-test\n", encoding="utf-8")
        try:
            game.click(300, 300)
            check("stop file halts input", False)
        except ControlError as exc:
            time.sleep(0.3)
            check("stop file halts input", "KENSHI_LINK_HALTED" in str(exc)
                  and not [e for e in events(log)[before:] if e["type"] in ("button", "key")], exc)
        config.stop_file.unlink()
        game.close()
    finally:
        for process in (overlay, window):
            if process is not None:
                process.terminate()
                process.wait(timeout=5)

    # No window of this name exists, whatever else is open on this PC.
    config = Config(backend="windows", data_dir=work / "home2", auto_focus=False,
                    process_regex=r"^kenshi-link-selftest-no-such-program\.exe$")
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
