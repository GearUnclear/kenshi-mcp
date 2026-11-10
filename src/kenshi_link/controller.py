"""The game controller: every way Claude can look at or act on Kenshi goes through here.

Three ideas shape it:

* Kenshi is real-time-with-pause and Claude needs seconds to decide, so game time
  only passes inside `advance()` (or after an explicit `set_speed`), and the
  controller keeps track of whether the game is paused.
* Claude works in the pixel space of the screenshot it was given; the controller
  maps that to the window and the screen.
* Input is only ever sent while the Kenshi window has focus, is limited to keys
  that stay inside the game, and stops for good when the operator says so.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from . import imaging
from .backends import Backend, BackendError, Clock, WindowInfo, create_backend
from .backends.base import BUTTONS
from .config import SPEEDS, Config
from .keys import BlockedInput, char_to_key, check_allowed, parse_combo, parse_modifiers

HALT_MARKER = "KENSHI_LINK_HALTED"

CAMERA_ACTIONS = (
    "forward",
    "back",
    "left",
    "right",
    "rotate_left",
    "rotate_right",
    "zoom_in",
    "zoom_out",
    "tilt_up",
    "tilt_down",
)
_TIME_ACTIONS = ("pause", "speed_normal", "speed_fast", "speed_fastest")
_CAMERA_STEP_SECONDS = 0.25
_TILT_STEP_PIXELS = 40
_EDGE_MARGIN = 3


class ControlError(Exception):
    """Something Claude should read and react to (bad arguments, no window, lost focus)."""


class Halted(ControlError):
    """The operator stopped the session. No more input will be sent."""


@dataclass
class Shot:
    data: bytes
    format: str  # "jpeg" or "png"
    width: int
    height: int

    @property
    def mime(self) -> str:
        return f"image/{self.format}"


@dataclass
class Result:
    text: str
    images: list[Shot] = field(default_factory=list)


class Controller:
    def __init__(
        self, config: Config, backend: Backend | None = None, clock: Clock | None = None
    ) -> None:
        self.config = config
        self.clock = clock or Clock()
        self.backend = backend or create_backend(config, self.clock)
        self.paused: bool | None = None
        self.pause_source = "unknown"  # unknown | inferred | tracked | told
        self.speed: str | None = None
        self.actions = 0
        self._pointer: tuple[int, int] | None = None  # last pointer target, window pixels
        self._held: list[tuple[str, str]] = []
        self._session = time.strftime("%Y%m%d-%H%M%S")
        self._frame_number = 0

    # ---- operator stop ----------------------------------------------------------

    def _halt_message(self, reason: str) -> str:
        return (
            f"{HALT_MARKER}: {reason}. All game input is disabled until the operator deletes "
            f"{self.config.stop_file} (or runs `kenshi-link resume`). Do not retry; stop and tell "
            "the operator."
        )

    def _trip(self, reason: str) -> None:
        try:
            self.config.data_dir.mkdir(parents=True, exist_ok=True)
            self.config.stop_file.write_text(f"{reason}\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except OSError:
            pass
        self.paused = None
        self.pause_source = "unknown"

    def _check_halt(self) -> None:
        if self.config.stop_file.exists():
            try:
                reason = self.config.stop_file.read_text().strip().splitlines()[0]
            except (OSError, IndexError):
                reason = "stop file present"
            raise Halted(self._halt_message(reason or "stop file present"))
        reason = None
        if self.config.panic_key and self.backend.panic_pressed():
            reason = "the operator pressed Pause/Break"
        elif self.config.failsafe_corner:
            x, y = self.backend.cursor()
            if 0 <= x <= 2 and 0 <= y <= 2:
                reason = "the operator moved the mouse to the top-left corner of the screen"
        if reason:
            self._trip(reason)
            raise Halted(self._halt_message(reason))

    # ---- window and pixels ------------------------------------------------------

    def _window(self) -> WindowInfo:
        """Find the game window and make sure it has focus, or explain why not."""
        try:
            info = self.backend.locate()
            if not info.focused or info.width == 0:
                if not self.config.auto_focus:
                    raise ControlError(
                        "Kenshi is not the focused window, so nothing was sent or captured. "
                        "Ask the operator to click on the game window."
                    )
                self.backend.focus()
                self.clock.sleep(0.25)
                info = self.backend.locate()
                if not info.focused:
                    raise ControlError(
                        "Kenshi could not be brought to the front, so nothing was sent or captured "
                        "(keys must never reach another program). Ask the operator to click on the "
                        "game window."
                    )
        except BackendError as exc:
            raise ControlError(str(exc)) from exc
        if info.width < 64 or info.height < 64:
            raise ControlError("The Kenshi window is minimised or too small to use.")
        return info

    def _fit(self, info: WindowInfo) -> imaging.Fit:
        return imaging.fit(info.width, info.height, self.config.max_long_edge)

    def _grab(self, info: WindowInfo) -> Image.Image:
        try:
            return self.backend.capture(info.left, info.top, info.width, info.height)
        except BackendError as exc:
            raise ControlError(str(exc)) from exc

    def _window_point(self, info: WindowInfo, x: float, y: float, what: str = "Point") -> tuple[int, int]:
        """Screenshot pixels -> window pixels, rejecting anything outside the picture."""
        fit = self._fit(info)
        if not (0 <= x < fit.width and 0 <= y < fit.height):
            raise ControlError(
                f"{what} ({x:g}, {y:g}) is outside the {fit.width}x{fit.height} screenshot. "
                "Coordinates are screenshot pixels with (0, 0) at the top-left."
            )
        wx, wy = fit.to_window(x, y)
        wx = max(_EDGE_MARGIN, min(info.width - 1 - _EDGE_MARGIN, wx))
        wy = max(_EDGE_MARGIN, min(info.height - 1 - _EDGE_MARGIN, wy))
        return wx, wy

    def _shot(
        self, info: WindowInfo, frame: Image.Image | None = None, *, grid: bool = False, mark: bool = False
    ) -> Shot:
        frame = frame if frame is not None else self._grab(info)
        fit = self._fit(info)
        image = imaging.resize(frame, (fit.width, fit.height))
        if mark and self.config.mark_pointer and self._pointer is not None:
            image = imaging.draw_marker(image, *fit.to_image(*self._pointer))
        if grid:
            image = imaging.draw_grid(image)
        return self._encode(image)

    def _encode(self, image: Image.Image) -> Shot:
        data, fmt = imaging.encode(image, self.config.image_format, self.config.jpeg_quality)
        if self.config.save_frames:
            try:
                folder = self.config.sessions_dir / self._session
                folder.mkdir(parents=True, exist_ok=True)
                self._frame_number += 1
                extension = "jpg" if fmt == "jpeg" else fmt
                (folder / f"{self._frame_number:05d}.{extension}").write_bytes(data)
            except OSError:
                pass
        return Shot(data, fmt, image.width, image.height)

    def _log(self, action: str, arguments: dict, text: str) -> None:
        try:
            self.config.sessions_dir.mkdir(parents=True, exist_ok=True)
            record = {"time": time.time(), "action": action, "arguments": arguments, "result": text}
            with (self.config.sessions_dir / f"{self._session}.jsonl").open("a", encoding="utf-8") as out:
                out.write(json.dumps(record) + "\n")
        except OSError:
            pass

    # ---- low-level input --------------------------------------------------------

    def _key_down(self, key: str) -> None:
        self.backend.key(key, True)
        self._held.append(("key", key))

    def _key_up(self, key: str) -> None:
        self.backend.key(key, False)
        if ("key", key) in self._held:
            self._held.remove(("key", key))

    def _button_down(self, button: str) -> None:
        self.backend.button(button, True)
        self._held.append(("button", button))

    def _button_up(self, button: str) -> None:
        self.backend.button(button, False)
        if ("button", button) in self._held:
            self._held.remove(("button", button))

    def _release_all(self) -> None:
        """Never leave a key or button stuck down, whatever went wrong."""
        for kind, name in reversed(self._held):
            try:
                if kind == "key":
                    self.backend.key(name, False)
                else:
                    self.backend.button(name, False)
            except Exception:
                pass
        self._held.clear()

    def _tap(self, combo: str, hold: float = 0.0) -> None:
        mods, key = parse_combo(combo)
        for mod in mods:
            self._key_down(mod)
        self._key_down(key)
        self.clock.sleep(max(self.config.key_hold_seconds, hold))
        self._key_up(key)
        for mod in reversed(mods):
            self._key_up(mod)
        self.clock.sleep(0.04)

    def _glide(self, info: WindowInfo, wx: int, wy: int, seconds: float | None = None) -> None:
        """Move the pointer in a few steps so the game sees motion, ending exactly on target."""
        target = (info.left + wx, info.top + wy)
        start = self.backend.cursor()
        steps = max(1, self.config.mouse_move_steps)
        duration = self.config.mouse_move_seconds if seconds is None else seconds
        for i in range(1, steps):
            t = i / steps
            self.backend.move(
                round(start[0] + (target[0] - start[0]) * t), round(start[1] + (target[1] - start[1]) * t)
            )
            self.clock.sleep(duration / steps)
        self.backend.move(*target)
        self.clock.sleep(0.03)
        self._pointer = (wx, wy)

    def _require_focus(self, doing: str) -> None:
        """Mid-sequence check: stop, rather than refocus, if the game lost focus."""
        try:
            focused = self.backend.locate().focused
        except BackendError:
            focused = False
        if not focused:
            raise ControlError(
                f"Kenshi lost focus while {doing}, so the rest was not sent. Look at the screen "
                "before continuing."
            )

    def _begin(self) -> WindowInfo:
        self._check_halt()
        info = self._window()
        self.actions += 1
        return info

    def _input(self, function, *args):
        """Run an input sequence, releasing everything if it fails part-way."""
        try:
            return function(*args)
        except BackendError as exc:
            self._release_all()
            raise ControlError(str(exc)) from exc
        except BaseException:
            self._release_all()
            raise

    # ---- pause tracking ---------------------------------------------------------

    def _probe(self, info: WindowInfo) -> tuple[Image.Image, float]:
        """Two frames a moment apart: the later frame and how much of the picture changed."""
        first = self._grab(info)
        self.clock.sleep(self.config.motion_probe_seconds)
        second = self._grab(info)
        return second, imaging.motion_fraction(first, second)

    def _moving(self, motion: float) -> bool:
        return motion > self.config.motion_threshold

    def _infer_pause(self, motion: float) -> str:
        self.paused = not self._moving(motion)
        self.pause_source = "inferred"
        state = "PAUSED" if self.paused else "RUNNING"
        return (
            f"The pause state was unknown, so it was inferred as {state} from whether the picture "
            "is changing. Check the screenshot for the game's own pause indicator and call "
            "sync_pause if this is wrong."
        )

    def _reconcile(self, motion: float) -> list[str]:
        if self.paused is None:
            return [self._infer_pause(motion)]
        if self.paused and self._moving(motion):
            return [
                f"Note: {motion:.2%} of the picture is still changing although the game should be "
                "paused. Animated UI or weather can cause this, but if the game's pause indicator "
                "is missing, call sync_pause(paused=false) and then set_speed('pause')."
            ]
        if not self.paused and not self._moving(motion):
            return [
                "Note: the picture is not changing although the game should be running. If the "
                "game's pause indicator is showing, call sync_pause(paused=true)."
            ]
        return []

    def _state_line(self, info: WindowInfo, motion: float | None = None) -> str:
        fit = self._fit(info)
        if self.paused is None:
            state = "pause state unknown"
        else:
            state = f"game {'PAUSED' if self.paused else 'RUNNING'} ({self.pause_source})"
        parts = [state, f"speed {self.speed or 'unknown'}", f"screenshot {fit.width}x{fit.height}"]
        if motion is not None:
            parts.append(f"picture changing {motion:.2%}")
        return "[" + " · ".join(parts) + "]"

    def _resume(self, info: WindowInfo, speed: str) -> list[str]:
        notes: list[str] = []
        if self.paused is None:
            _, motion = self._probe(info)
            notes.append(self._infer_pause(motion))
        if self.paused:
            self._tap(self.config.keymap["pause"])
            self.clock.sleep(0.08)
        self._tap(self.config.keymap[f"speed_{speed}"])
        self.paused = False
        self.pause_source = "tracked"
        self.speed = speed
        return notes

    def _finish(
        self, action: str, arguments: dict, lines: list[str], info: WindowInfo, images: list[Shot],
        motion: float | None = None,
    ) -> Result:
        text = "\n".join([*lines, self._state_line(info, motion)])
        self._log(action, arguments, text)
        return Result(text, images)

    def _after_input(self, action: str, arguments: dict, lines: list[str], *, mark: bool = False) -> Result:
        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        return self._finish(action, arguments, lines, info, [self._shot(info, mark=mark)])

    # ---- looking ----------------------------------------------------------------

    def observe(self, grid: bool = False) -> Result:
        info = self._begin()
        frame, motion = self._probe(info)
        fit = self._fit(info)
        lines = [
            f"Screenshot of the Kenshi window, {fit.width}x{fit.height} "
            f"(the window itself is {info.width}x{info.height}). Give coordinates in screenshot pixels."
        ]
        if grid:
            lines.append("A yellow coordinate grid is drawn on top; it is not part of the game.")
        lines += self._reconcile(motion)
        return self._finish(
            "observe", {"grid": grid}, lines, info, [self._shot(info, frame, grid=grid)], motion
        )

    def zoom(self, x0: float, y0: float, x1: float, y1: float) -> Result:
        info = self._begin()
        fit = self._fit(info)
        if not (0 <= x0 < x1 <= fit.width and 0 <= y0 < y1 <= fit.height):
            raise ControlError(
                f"Region ({x0:g}, {y0:g})-({x1:g}, {y1:g}) must satisfy x0 < x1, y0 < y1 and lie inside "
                f"the {fit.width}x{fit.height} screenshot."
            )
        if x1 - x0 < 16 or y1 - y0 < 16:
            raise ControlError("Zoom region is too small; make it at least 16x16 screenshot pixels.")
        frame = self._grab(info)
        box = (
            max(0, round(x0 / fit.scale)),
            max(0, round(y0 / fit.scale)),
            min(info.width, round(x1 / fit.scale)),
            min(info.height, round(y1 / fit.scale)),
        )
        crop = frame.crop(box)
        limit = self.config.max_long_edge
        factor = min(3.0, limit / max(crop.width, crop.height))
        target = imaging.fit(round(crop.width * factor), round(crop.height * factor), limit)
        image = imaging.resize(crop, (target.width, target.height))
        magnification = target.width / max(1.0, x1 - x0)
        lines = [
            f"Zoomed view of screenshot region ({x0:g}, {y0:g})-({x1:g}, {y1:g}), shown {magnification:.1f}x "
            "larger. This is for reading only: coordinates for other tools still refer to the full screenshot."
        ]
        return self._finish(
            "zoom", {"x0": x0, "y0": y0, "x1": x1, "y1": y1}, lines, info, [self._encode(image)]
        )

    # ---- pointer ----------------------------------------------------------------

    def click(
        self, x: float, y: float, button: str = "left", modifiers: str = "", count: int = 1,
        hold_seconds: float = 0.0,
    ) -> Result:
        if button not in BUTTONS:
            raise ControlError(f"button must be one of {', '.join(BUTTONS)} (got {button!r}).")
        if not 1 <= count <= 3:
            raise ControlError("count must be 1, 2 or 3.")
        if not 0 <= hold_seconds <= self.config.max_hold_seconds:
            raise ControlError(f"hold_seconds must be between 0 and {self.config.max_hold_seconds:g}.")
        mods = self._modifiers(modifiers)
        info = self._begin()
        wx, wy = self._window_point(info, x, y)

        def run() -> None:
            self._glide(info, wx, wy)
            for mod in mods:
                self._key_down(mod)
            for i in range(count):
                self._button_down(button)
                self.clock.sleep(max(self.config.click_hold_seconds, hold_seconds))
                self._button_up(button)
                if i < count - 1:
                    self.clock.sleep(0.09)
            for mod in reversed(mods):
                self._key_up(mod)

        self._input(run)
        kind = {1: "", 2: "double-", 3: "triple-"}[count]
        held = f", holding for {hold_seconds:g}s" if hold_seconds else ""
        prefix = f"{'+'.join(mods)}+" if mods else ""
        action = f"{prefix}{button} {kind}click".capitalize()
        lines = [f"{action} at ({x:g}, {y:g}){held}. The magenta ring marks where it landed."]
        arguments = {"x": x, "y": y, "button": button, "modifiers": modifiers, "count": count,
                     "hold_seconds": hold_seconds}
        return self._after_input("click", arguments, lines, mark=True)

    def drag(
        self, x0: float, y0: float, x1: float, y1: float, button: str = "left", modifiers: str = ""
    ) -> Result:
        if button not in BUTTONS:
            raise ControlError(f"button must be one of {', '.join(BUTTONS)} (got {button!r}).")
        mods = self._modifiers(modifiers)
        info = self._begin()
        start = self._window_point(info, x0, y0, "Start point")
        end = self._window_point(info, x1, y1, "End point")

        def run() -> None:
            self._glide(info, *start)
            for mod in mods:
                self._key_down(mod)
            self._button_down(button)
            self.clock.sleep(0.08)
            self._glide(info, *end, seconds=self.config.drag_seconds)
            self.clock.sleep(0.08)
            self._button_up(button)
            for mod in reversed(mods):
                self._key_up(mod)

        self._input(run)
        lines = [f"Dragged the {button} button from ({x0:g}, {y0:g}) to ({x1:g}, {y1:g})."]
        arguments = {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "button": button, "modifiers": modifiers}
        return self._after_input("drag", arguments, lines, mark=True)

    def scroll(self, x: float, y: float, direction: str, amount: int = 3) -> Result:
        if direction not in ("up", "down"):
            raise ControlError("direction must be 'up' or 'down'.")
        if not 1 <= amount <= 30:
            raise ControlError("amount must be between 1 and 30 wheel notches.")
        info = self._begin()
        wx, wy = self._window_point(info, x, y)

        def run() -> None:
            self._glide(info, wx, wy)
            for _ in range(amount):
                self.backend.wheel(1 if direction == "up" else -1)
                self.clock.sleep(0.03)

        self._input(run)
        lines = [f"Scrolled {direction} {amount} notch(es) at ({x:g}, {y:g})."]
        return self._after_input(
            "scroll", {"x": x, "y": y, "direction": direction, "amount": amount}, lines, mark=True
        )

    # ---- keyboard ---------------------------------------------------------------

    def _modifiers(self, modifiers: str) -> list[str]:
        try:
            return parse_modifiers(modifiers)
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc

    def _checked_combo(self, combo: str) -> tuple[list[str], str]:
        try:
            mods, key = parse_combo(combo)
            check_allowed(mods, key, allow_debug_keys=self.config.allow_debug_keys)
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc
        return mods, key

    def _same_combo(self, mods: list[str], key: str, action: str) -> bool:
        other_mods, other_key = parse_combo(self.config.keymap[action])
        return key == other_key and set(mods) == set(other_mods)

    def press_key(self, key: str, repeat: int = 1, hold_seconds: float = 0.0) -> Result:
        if not 1 <= repeat <= 20:
            raise ControlError("repeat must be between 1 and 20.")
        if not 0 <= hold_seconds <= self.config.max_hold_seconds:
            raise ControlError(f"hold_seconds must be between 0 and {self.config.max_hold_seconds:g}.")
        mods, name = self._checked_combo(key)
        combo = "+".join([*mods, name])
        self._begin()

        def run() -> None:
            for i in range(repeat):
                if i:
                    self._require_focus("pressing keys")
                self._tap(combo, hold_seconds)

        self._input(run)
        lines = [f"Pressed {combo}" + (f" x{repeat}" if repeat > 1 else "") + "."]
        if self._same_combo(mods, name, "pause"):
            if self.paused is not None and repeat % 2 == 1:
                self.paused = not self.paused
                self.pause_source = "tracked"
            lines.append("That is the pause key, so pause was toggled. Prefer set_speed for this.")
        for speed in SPEEDS[1:]:
            if self._same_combo(mods, name, f"speed_{speed}"):
                self.speed = speed
        return self._after_input(
            "press_key", {"key": key, "repeat": repeat, "hold_seconds": hold_seconds}, lines
        )

    def type_text(self, text: str) -> Result:
        if not text:
            raise ControlError("text is empty.")
        if len(text) > 200:
            raise ControlError("text is limited to 200 characters per call.")
        try:
            strokes = [char_to_key(char) for char in text]
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc
        self._begin()

        def run() -> None:
            for i, (name, shift) in enumerate(strokes):
                if i and i % 8 == 0:
                    self._require_focus("typing")
                self._tap(f"shift+{name}" if shift else name)

        self._input(run)
        lines = [f"Typed {len(text)} character(s)."]
        _, pause_key = parse_combo(self.config.keymap["pause"])
        if any(name == pause_key for name, _ in strokes):
            lines.append(
                "The text included the pause key. If no text box had focus, pause was toggled: "
                "check the screenshot and use sync_pause if needed."
            )
        return self._after_input("type_text", {"text": text}, lines)

    def hotkey(self, action: str, repeat: int = 1) -> Result:
        keymap = self.config.keymap
        usable = sorted(a for a in keymap if a not in _TIME_ACTIONS and not a.startswith("camera_"))
        if action in _TIME_ACTIONS:
            raise ControlError("Use set_speed or advance to control game time.")
        if action.startswith("camera_"):
            raise ControlError("Use the camera tool to move the camera.")
        if action not in keymap:
            raise ControlError(f"Unknown action {action!r}. Available: {', '.join(usable)}.")
        if not 1 <= repeat <= 5:
            raise ControlError("repeat must be between 1 and 5.")
        combo = keymap[action]
        mods, name = self._checked_combo(combo)
        self._begin()
        arguments = {"action": action, "repeat": repeat}

        if action == "highlight_items":
            # The labels only show while the key is down, so the screenshot is taken mid-hold.
            def hold_and_look() -> Result:
                for key in [*mods, name]:
                    self._key_down(key)
                self.clock.sleep(max(0.5, self.config.settle_seconds))
                info = self._window()
                shot = self._shot(info)
                for key in reversed([*mods, name]):
                    self._key_up(key)
                lines = [f"Held {combo} (highlight items) while taking this screenshot, then released it."]
                return self._finish("hotkey", arguments, lines, info, [shot])

            return self._input(hold_and_look)

        def run() -> None:
            for _ in range(repeat):
                self._tap(combo)
                self.clock.sleep(0.05)

        self._input(run)
        lines = [f"Pressed {combo} ({action})" + (f" x{repeat}" if repeat > 1 else "") + "."]
        if action == "quick_load":
            self.paused = None
            self.pause_source = "unknown"
            self.clock.sleep(1.0)
            lines.append("A load was requested; wait for it to finish, then observe to re-check the pause state.")
        return self._after_input("hotkey", arguments, lines)

    # ---- camera -----------------------------------------------------------------

    def camera(self, action: str, steps: int = 2) -> Result:
        if action not in CAMERA_ACTIONS:
            raise ControlError(f"action must be one of: {', '.join(CAMERA_ACTIONS)}.")
        if not 1 <= steps <= 20:
            raise ControlError("steps must be between 1 and 20.")
        info = self._begin()
        centre = (info.width // 2, info.height // 2)

        def run() -> None:
            if action in ("zoom_in", "zoom_out"):
                self._glide(info, *centre)
                for _ in range(steps):
                    self.backend.wheel(1 if action == "zoom_in" else -1)
                    self.clock.sleep(0.03)
            elif action in ("tilt_up", "tilt_down"):
                travel = min(steps * _TILT_STEP_PIXELS, info.height // 2 - 2 * _EDGE_MARGIN - 1)
                offset = -travel if action == "tilt_up" else travel
                self._glide(info, *centre)
                self._button_down("middle")
                self.clock.sleep(0.08)
                self._glide(info, centre[0], centre[1] + offset, seconds=self.config.drag_seconds)
                self.clock.sleep(0.08)
                self._button_up("middle")
            else:
                self._tap(self.config.keymap[f"camera_{action}"], steps * _CAMERA_STEP_SECONDS)

        self._input(run)
        self._pointer = None
        lines = [f"Camera {action.replace('_', ' ')}, {steps} step(s)."]
        return self._after_input("camera", {"action": action, "steps": steps}, lines)

    # ---- time -------------------------------------------------------------------

    def set_speed(self, speed: str) -> Result:
        if speed not in SPEEDS:
            raise ControlError(f"speed must be one of: {', '.join(SPEEDS)}.")
        info = self._begin()
        lines: list[str] = []

        def run() -> None:
            if speed == "pause":
                if self.paused is None:
                    _, motion = self._probe(info)
                    lines.append(self._infer_pause(motion))
                if self.paused:
                    lines.append("The game is already paused; nothing was pressed.")
                else:
                    self._tap(self.config.keymap["pause"])
                    self.paused = True
                    self.pause_source = "tracked"
                    lines.append("Paused the game.")
            else:
                lines.extend(self._resume(info, speed))
                lines.append(
                    f"The game is now RUNNING at {speed} speed and will keep running while you think. "
                    "Pause again as soon as you need to decide something."
                )

        self._input(run)
        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        frame, motion = self._probe(info)
        lines += self._reconcile(motion)
        return self._finish("set_speed", {"speed": speed}, lines, info, [self._shot(info, frame)], motion)

    def advance(self, seconds: float, speed: str = "normal", frames: int = 2) -> Result:
        if speed not in SPEEDS[1:]:
            raise ControlError(f"speed must be one of: {', '.join(SPEEDS[1:])}.")
        limit = self.config.max_advance_seconds
        if not 0.2 <= seconds <= limit:
            raise ControlError(f"seconds must be between 0.2 and {limit:g}.")
        if not 0 <= frames <= 4:
            raise ControlError("frames must be between 0 and 4.")
        info = self._begin()
        lines: list[str] = []
        samples: list[Image.Image] = []

        def start() -> None:
            lines.extend(self._resume(info, speed))

        self._input(start)
        began = self.clock.now()
        sample_times = [began + seconds * (i + 1) / (frames + 1) for i in range(frames)]
        interrupted: Halted | None = None
        while True:
            now = self.clock.now()
            if now >= began + seconds:
                break
            self.clock.sleep(min(0.1, began + seconds - now))
            try:
                self._check_halt()
            except Halted as exc:
                interrupted = exc
                break
            if sample_times and self.clock.now() >= sample_times[0]:
                sample_times.pop(0)
                try:
                    current = self.backend.locate()
                    if current.focused:  # never capture whatever else is on top
                        samples.append(self._grab(current))
                except (BackendError, ControlError):
                    pass
        if interrupted is not None:
            # The operator has taken over; send nothing more, not even the pause key.
            self.paused = None
            self.pause_source = "unknown"
            raise interrupted
        ran_for = self.clock.now() - began

        try:
            info = self._window()
            self._input(self._tap, self.config.keymap["pause"])
        except ControlError as exc:
            self.paused = False
            raise ControlError(
                f"THE GAME IS STILL RUNNING at {speed} speed: it could not be paused after "
                f"{ran_for:.1f}s because: {exc}"
            ) from exc
        self.paused = True
        self.pause_source = "tracked"

        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        frame, motion = self._probe(info)
        lines.append(f"Ran the game for {ran_for:.1f}s of real time at {speed} speed, then paused it.")
        images: list[Shot] = []
        strip = imaging.filmstrip(samples)
        if strip is not None:
            images.append(self._encode(strip))
            lines.append(
                f"Image 1 is a strip of {len(samples)} frame(s) captured along the way (oldest on the left); "
                "image 2 is the screen now."
            )
        images.append(self._shot(info, frame))
        lines += self._reconcile(motion)
        arguments = {"seconds": seconds, "speed": speed, "frames": frames}
        return self._finish("advance", arguments, lines, info, images, motion)

    def sync_pause(self, paused: bool) -> Result:
        self.paused = bool(paused)
        self.pause_source = "told"
        text = f"Recorded that the game is {'PAUSED' if paused else 'RUNNING'}. No key was pressed."
        self._log("sync_pause", {"paused": paused}, text)
        return Result(text)

    # ---- housekeeping -----------------------------------------------------------

    def describe(self) -> str:
        """Plain-text health report used by `kenshi-link doctor`."""
        lines = [f"backend: {self.backend.name}"]
        try:
            info = self.backend.locate()
        except BackendError as exc:
            return "\n".join([*lines, f"window: NOT FOUND - {exc}"])
        fit = self._fit(info) if info.width and info.height else None
        lines.append(f"window: {info.title!r}")
        lines.append(f"client area: {info.width}x{info.height} at ({info.left}, {info.top}) on screen")
        lines.append(f"focused: {info.focused}")
        if fit:
            lines.append(f"screenshot size sent to Claude: {fit.width}x{fit.height} (scale {fit.scale:.3f})")
        lines.append(f"stop file: {'PRESENT - input disabled' if self.config.stop_file.exists() else 'absent'}")
        return "\n".join(lines)

    def close(self) -> None:
        self._release_all()
        self.backend.close()


def read_notes(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def write_notes(path: Path, text: str, mode: str = "append") -> int:
    """Save notes and return the file's new length in characters."""
    if mode not in ("append", "replace"):
        raise ControlError("mode must be 'append' or 'replace'.")
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "replace":
        content = text.rstrip() + "\n"
    else:
        existing = read_notes(path)
        separator = "" if not existing or existing.endswith("\n") else "\n"
        content = existing + separator + text.rstrip() + "\n"
    path.write_text(content, encoding="utf-8")
    return len(content)
