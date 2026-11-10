"""The game controller: every way Claude can look at or act on Kenshi goes through here.

Three ideas shape it:

* Kenshi is real-time-with-pause and Claude needs seconds to decide, so game time
  only passes inside `advance()` (or after an explicit `set_speed`), and the
  controller keeps track of whether the game is paused.
* Claude works in the pixel space of the screenshot it was given; the controller
  maps that to the window and the screen.
* Input is only ever sent while the Kenshi window has focus, is limited to keys
  that stay inside the game, and stops for good when the operator says so.

Nothing can be read from the game, so the pause state kept here is a belief. Kenshi
pauses and un-pauses itself (a conversation, the build window, character creation, an
area loading), which no key press of ours explains. Two rules keep a wrong belief from
doing harm: the keys pressed never depend on it in a way that could invert (a speed key
sets a speed outright, and the pause key, which toggles, is only pressed straight after
one), and whenever the picture contradicts the belief the result says so.

One thing is held across calls: the right mouse button, while Kenshi's action menu is
open (menu_open). Everything that could leave it stuck lets go of it: any failed call,
any other call that sends input, an operator stop, lost focus, a time limit (tend) and
shutdown.
"""

from __future__ import annotations

import functools
import json
import locale
import math
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from . import imaging
from .backends import Backend, BackendError, Clock, WindowInfo, WindowNotFound, create_backend
from .backends.base import BUTTONS, DesktopUnavailable
from .config import SPEEDS, Config
from .keys import BlockedInput, char_to_key, check_allowed, check_modifiers, parse_combo, parse_modifiers

HALT_MARKER = "KENSHI_LINK_HALTED"
_ESCAPE_REFUSED = (
    "Escape was not sent. On Kenshi's title screen (CONTINUE, NEW GAME, LOAD GAME ...) it quits the "
    "game without asking, and kenshi-link cannot start it again. If the latest screenshot shows a "
    "loaded game (the world, or a window over it), use hotkey('close', in_game=true). On the title "
    "screen, click the open window's own close or cancel button instead."
)

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
# The operator stops everything by pushing the mouse into the corner of the screen: a
# pointer within this many pixels of it, each way, counts. The pointer must never be put
# there by this program, or the next check would take its own move for the operator's.
_CORNER_ZONE = 3
# Pointer targets keep this far from the window's edges. More than the corner zone, so
# that a click in the corner of a borderless window at the corner of the screen stays
# clear of it even if it lands a pixel off.
_EDGE_MARGIN = _CORNER_ZONE + 2
# Kenshi scrolls its camera for as long as the pointer rests in the outer 1% of its view,
# over the HUD too and while paused. A click there is allowed, but the pointer is not left
# there: it is parked this share of the window in from the edge, half as much again.
_SCROLL_ZONE = 0.015
# Kenshi opens its action menu once the right button has been held 0.2 s on a target
# (0.25 s on a portrait). A held right click of this length or more has opened it.
_MENU_OPENS_AFTER = 0.2
_MENU_DROPPED = "The action menu that was being held was closed without a choice."


class ControlError(Exception):
    """Something Claude should read and react to (bad arguments, no window, lost focus)."""


class Halted(ControlError):
    """The operator stopped the session, or the desktop is out of reach. No more input will be sent."""


class Interrupted(ControlError):
    """A sequence was cut short because the program is shutting down."""


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


@dataclass
class _HeldMenu:
    """The right button is down on a target, with Kenshi's action menu (if any) showing."""

    x: float  # where it was pressed, in screenshot pixels
    y: float
    point: tuple[int, int]  # the same place in window pixels
    since: float  # clock time of the press


def _action(method=None, *, keeps_menu: bool = False):
    """Mark a method as one of the things Claude can do, and make it safe around a held menu.

    A held action menu is closed before anything else is sent, unless the action is part
    of using it (`keeps_menu`). And whatever goes wrong, nothing stays held afterwards.
    """

    def decorate(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                if not keeps_menu:
                    self._close_menu("the button was released first, because another action was asked for")
                return function(self, *args, **kwargs)
            except ControlError as exc:
                note = _MENU_DROPPED if self._menu is not None else self._menu_ended
                self._release_all()
                self._menu_ended = ""
                if note:
                    raise type(exc)(f"{exc} {note}") from exc
                raise
            except BaseException:
                self._release_all()
                raise

        return wrapper

    return decorate(method) if method is not None else decorate


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
        self._menu: _HeldMenu | None = None  # the right button, held across calls (see menu_open)
        self._menu_ended = ""  # why the last held menu was closed without a choice, until reported
        self._session = time.strftime("%Y%m%d-%H%M%S")
        self._frame_number = 0
        # Set from other threads (see request_pause and shutdown); read on the one that acts.
        self._pause_requested = threading.Event()
        self._closing = threading.Event()
        if config.panic_key:
            self.backend.watch_panic(self._panic_seen)

    # ---- operator stop ----------------------------------------------------------

    def _halt_message(self, reason: str) -> str:
        return (
            f"{HALT_MARKER}: {reason}. All game input is disabled until the operator deletes "
            f"{self.config.stop_file} (or runs `kenshi-link resume`). Do not retry; stop and tell "
            "the operator."
        )

    def _write_stop(self, reason: str) -> None:
        try:
            self.config.data_dir.mkdir(parents=True, exist_ok=True)
            self.config.stop_file.write_text(
                f"{reason}\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n", encoding="utf-8"
            )
        except OSError:
            pass

    def _panic_seen(self) -> None:
        """The backend noticed a press of the panic key. This can run on any thread, at any
        time, so it only leaves the stop file for the next check to find."""
        self._write_stop("the operator pressed Pause/Break")

    def _forget_pause(self) -> None:
        self.paused = None
        self.pause_source = "unknown"

    def _in_corner(self, x: int, y: int) -> bool:
        corner_x, corner_y = self.backend.failsafe_corner()
        return 0 <= x - corner_x < _CORNER_ZONE and 0 <= y - corner_y < _CORNER_ZONE

    def _clear_of_corner(self, x: int, y: int) -> tuple[int, int]:
        """The nearest screen point to (x, y) that the operator's corner check cannot mistake."""
        if not self.config.failsafe_corner:
            return x, y
        corner_x, corner_y = self.backend.failsafe_corner()
        reach = _CORNER_ZONE + 1  # one spare pixel
        dx, dy = x - corner_x, y - corner_y
        if not (0 <= dx < reach and 0 <= dy < reach):
            return x, y
        return (corner_x + reach, y) if dx >= dy else (x, corner_y + reach)

    def _control_error(self, exc: BackendError) -> ControlError:
        """A backend failure in the form Claude should see it."""
        if isinstance(exc, DesktopUnavailable):
            # Nothing Claude can do will help, and each retry costs a turn: say so the way
            # an operator stop is said. No stop file: it ends when the desktop is back.
            return Halted(f"{HALT_MARKER}: {exc}. Do not retry; stop and tell the operator.")
        return ControlError(str(exc))

    def _check_halt(self) -> None:
        if self.config.stop_file.exists():
            self._forget_pause()  # the operator has had the controls since
            raise Halted(self._halt_message(_stop_reason(self.config.stop_file)))
        reason = None
        try:
            if self.config.panic_key and self.backend.panic_pressed():
                reason = "the operator pressed Pause/Break"
            elif self.config.failsafe_corner and self._in_corner(*self.backend.cursor()):
                reason = "the operator moved the mouse to the top-left corner of the screen"
        except BackendError as exc:
            raise self._control_error(exc) from exc
        if reason:
            self._write_stop(reason)
            self._forget_pause()
            raise Halted(self._halt_message(reason))

    def _poll(self) -> None:
        """The check made between the steps of a sequence: an operator stop, or shutdown."""
        self._check_halt()
        if self._closing.is_set():
            raise Interrupted("kenshi-link is shutting down, so the rest was not sent.")

    def request_pause(self) -> None:
        """Ask a running advance() to stop early and pause now. Safe to call from any thread."""
        self._pause_requested.set()

    def shutdown(self) -> None:
        """Wind up from another thread: whatever is in progress stops at its next check, an
        advance pauses the game first, and no new action starts. close() must still be called."""
        self._closing.set()

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
                    why = self.backend.focus_error()
                    raise ControlError(
                        "Kenshi could not be brought to the front, so nothing was sent or captured "
                        f"(keys must never reach another program). {why + ' ' if why else ''}"
                        "Ask the operator to click on the game window."
                    )
            bounds = self.backend.screen_rect()
        except BackendError as exc:
            raise self._control_error(exc) from exc
        if info.width < 64 or info.height < 64:
            raise ControlError("The Kenshi window is minimised or too small to use.")
        if bounds is not None and not (
            bounds[0] <= info.left
            and bounds[1] <= info.top
            and info.left + info.width <= bounds[0] + bounds[2]
            and info.top + info.height <= bounds[1] + bounds[3]
        ):
            # The part off the screen cannot be captured, and a click aimed there lands on
            # whatever is at the screen's edge instead.
            raise ControlError(
                "The Kenshi window is partly off the screen, so nothing was sent or captured. Ask "
                "the operator to move it fully onto the screen, or to switch the game to borderless."
            )
        return info

    def _fit(self, info: WindowInfo) -> imaging.Fit:
        return imaging.fit(info.width, info.height, self.config.max_long_edge)

    def _grab(self, info: WindowInfo) -> Image.Image:
        try:
            return self.backend.capture(info.left, info.top, info.width, info.height)
        except BackendError as exc:
            raise self._control_error(exc) from exc

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

    def _scroll_margin(self, info: WindowInfo) -> tuple[int, int]:
        """How far in from the window's edges, each way, the pointer must rest so as not to
        scroll Kenshi's camera."""
        return (
            max(_EDGE_MARGIN, math.ceil(info.width * _SCROLL_ZONE)),
            max(_EDGE_MARGIN, math.ceil(info.height * _SCROLL_ZONE)),
        )

    def _off_the_edge(self, info: WindowInfo, wx: int, wy: int) -> tuple[int, int]:
        """The nearest window point to (wx, wy) that is clear of the edge-scroll zone."""
        margin_x, margin_y = self._scroll_margin(info)
        return (
            max(margin_x, min(info.width - 1 - margin_x, wx)),
            max(margin_y, min(info.height - 1 - margin_y, wy)),
        )

    def _leave_edge(self, info: WindowInfo) -> bool:
        """Move a pointer that is resting on the game window's edge a little way in.

        Left there, it scrolls the camera for as long as it stays, paused or not: the view
        slides away and the picture keeps changing, which looks like a running game. The
        ring on the screenshot still marks where the click landed.
        """
        try:
            x, y = self.backend.cursor()
            wx, wy = x - info.left, y - info.top
            inside = self._off_the_edge(info, wx, wy)
            if not (0 <= wx < info.width and 0 <= wy < info.height) or (wx, wy) == inside:
                return False
            self._poll()  # the screen's corner is inside this zone: the operator may have put it there
            self.backend.move(*self._clear_of_corner(info.left + inside[0], info.top + inside[1]))
        except BackendError as exc:
            raise self._control_error(exc) from exc
        self.clock.sleep(self.config.pointer_dwell_seconds)
        return True

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

    def _require_pointer_on_game(self) -> None:
        """Focus decides where keys go, but a click or the wheel goes to whatever is under
        the pointer: refuse if that is not the game."""
        if not self.backend.pointer_on_window():
            raise ControlError(
                "Another window is covering the game where the pointer is (a notification, the "
                "taskbar or something set to stay on top), so the click was not sent: it would have "
                "gone to that window. Use observe to see what is in the way; wait for it to go, "
                "or pick a spot it does not cover."
            )

    def _button_down(self, button: str) -> None:
        self._require_pointer_on_game()
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
        self._menu = None

    def _wheel(self, clicks: int) -> None:
        self._require_pointer_on_game()
        self.backend.wheel(clicks)

    def _hold(self, seconds: float) -> None:
        """Wait with something held down, looking out for an operator stop meanwhile.

        A stop raises from here; _input then releases whatever is held.
        """
        end = self.clock.now() + seconds
        while (remaining := end - self.clock.now()) > 1e-9:
            self.clock.sleep(min(self.config.halt_poll_seconds, remaining))
            if end - self.clock.now() > 1e-9:
                self._poll()

    def _tap(self, combo: str, hold: float = 0.0, *, checked: bool = True) -> None:
        """Press and release a key or combo.

        `checked=False` is for the keys that control game time: they are sent whatever
        else is going on, because they are how a run is brought to a stop.
        """
        mods, key = parse_combo(combo)
        if checked:
            self._poll()
        for mod in mods:
            self._key_down(mod)
        self._key_down(key)
        if checked:
            self._hold(max(self.config.key_hold_seconds, hold))
        else:
            self.clock.sleep(max(self.config.key_hold_seconds, hold))
        self._key_up(key)
        for mod in reversed(mods):
            self._key_up(mod)
        self.clock.sleep(0.04)

    def _modifiers_down(self, mods: list[str]) -> None:
        for mod in mods:
            self._key_down(mod)
        if mods:
            # The game reads keyboard and mouse separately, once a frame each: without a
            # pause the click can be handled before the modifier is seen to be down.
            self.clock.sleep(self.config.modifier_gap_seconds)

    def _modifiers_up(self, mods: list[str]) -> None:
        if mods:
            self.clock.sleep(self.config.modifier_gap_seconds)  # ... or after it is seen to be up
        for mod in reversed(mods):
            self._key_up(mod)

    def _glide(self, info: WindowInfo, wx: int, wy: int, seconds: float | None = None) -> None:
        """Move the pointer in a few steps so the game sees motion, ending exactly on target.

        The operator's stop is checked before every step: once the pointer has been pulled
        away from the corner they parked it in, nothing could tell it had been there.
        """
        target = self._clear_of_corner(info.left + wx, info.top + wy)
        start = self.backend.cursor()
        steps = max(1, self.config.mouse_move_steps)
        duration = self.config.mouse_move_seconds if seconds is None else seconds
        for i in range(1, steps):
            t = i / steps
            self._poll()
            self.backend.move(
                *self._clear_of_corner(
                    round(start[0] + (target[0] - start[0]) * t), round(start[1] + (target[1] - start[1]) * t)
                )
            )
            self.clock.sleep(duration / steps)
        self._poll()
        self.backend.move(*target)
        # The game takes the pointer's position once per frame, and handles a button before
        # the movement that arrived in the same frame: rest here until it has caught up.
        self.clock.sleep(self.config.pointer_dwell_seconds)
        self._poll()  # before the pointer is touched again: the operator may have taken it
        if self.backend.cursor() != target:
            # The platform's coordinate rounding (or a nudge of the mouse) left it elsewhere.
            self.backend.place(*target)
            self.clock.sleep(self.config.pointer_dwell_seconds)
        self._pointer = (target[0] - info.left, target[1] - info.top)

    def _require_focus(self, doing: str) -> None:
        """Mid-sequence check: stop, rather than refocus, if the game lost focus."""
        try:
            focused = self.backend.locate().focused
        except WindowNotFound:
            focused = False
        except BackendError as exc:
            error = self._control_error(exc)
            if isinstance(error, Halted):
                raise error from exc
            raise ControlError(f"{exc} That was noticed while {doing}, so the rest was not sent.") from exc
        if not focused:
            raise ControlError(
                f"Kenshi lost focus while {doing}, so the rest was not sent. Look at the screen "
                "before continuing."
            )

    def _begin(self) -> WindowInfo:
        if self._closing.is_set():
            raise Interrupted("kenshi-link is shutting down; nothing was sent.")
        self._check_halt()
        if self._menu is not None:
            self._review_menu()
        info = self._window()
        if self._menu is None:
            self._leave_edge(info)  # wherever it was left, by us or by the operator
        self.actions += 1
        return info

    def _input(self, function, *args, **kwargs):
        """Run an input sequence, releasing everything if it fails part-way."""
        try:
            return function(*args, **kwargs)
        except BackendError as exc:
            self._release_all()
            raise self._control_error(exc) from exc
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
            f"The pause state was not known, so it was inferred as {state} from whether the picture "
            "is changing. Kenshi shows a PAUSED panel while it is paused: if the screenshot says "
            "otherwise, call sync_pause."
        )

    def _reconcile(self, motion: float) -> list[str]:
        """What to tell Claude when the picture and the pause belief disagree."""
        if self.paused is None:
            return [self._infer_pause(motion)]
        if self.paused and self._moving(motion):
            return [
                f"Note: {motion:.2%} of the picture is changing although the game should be paused. A "
                "moving camera or animated UI can do that. So can the game: Kenshi un-pauses itself "
                "when a conversation closes and when character creation is confirmed. If the PAUSED "
                "panel is not showing, call sync_pause(paused=false) and then set_speed('pause')."
            ]
        if not self.paused and not self._moving(motion):
            return [
                "Note: the picture is not changing although the game should be running. Kenshi "
                "pauses itself for a conversation, the build window, character creation and while an "
                "area loads. If the PAUSED panel is showing, call sync_pause(paused=true)."
            ]
        return []

    def _state_line(self, info: WindowInfo, motion: float | None = None) -> str:
        fit = self._fit(info)
        if self.paused is None:
            state = "pause state unknown"
        elif self.paused:
            state = f"game PAUSED ({self.pause_source})"
        else:
            state = f"game RUNNING at {self.speed or 'unknown'} speed ({self.pause_source})"
        parts = [state, f"screenshot {fit.width}x{fit.height}"]
        if motion is not None:
            parts.append(f"picture changing {motion:.2%}")
        if self._menu is not None:
            parts.append("RIGHT BUTTON HELD for the action menu")
        return "[" + " · ".join(parts) + "]"

    def _resume(self, speed: str) -> None:
        """Set the clock running at `speed`.

        Only the speed key is pressed. It sets that speed outright and ends a pause, so the
        result is the same whatever state the game was in. The pause key is not used here:
        it toggles, and would pause a game that was running after all.
        """
        self._tap(self.config.keymap[f"speed_{speed}"], checked=False)
        self.paused = False
        self.pause_source = "tracked"
        self.speed = speed

    def _pause(self) -> None:
        """Pause the game, whatever state it is in.

        The pause key toggles, and the game also pauses by itself, so pressing it on the
        strength of a belief can start the clock instead of stopping it. Normal speed is
        asked for first: that leaves the game running whatever it was doing before, and the
        toggle then has only one way to go. If the game had paused itself, it runs for the
        moment between the two keys. Normal speed rather than the one last asked for, because
        the pause key remembers the speed it interrupted, and that is the speed the game goes
        back to if it later un-pauses by itself.
        """
        self._tap(self.config.keymap["speed_normal"], checked=False)
        self._tap(self.config.keymap["pause"], checked=False)
        self.paused = True
        self.pause_source = "tracked"
        self.speed = "normal"

    def _confirm_pause(self, motion: float) -> list[str]:
        """After the pause keys: does the picture agree that the game has stopped?"""
        if not self._moving(motion):
            return []
        self._forget_pause()
        return [
            f"THE GAME MAY STILL BE RUNNING: {motion:.2%} of the picture is changing after the pause "
            "keys were pressed, so the pause state is now unknown. Look for the PAUSED panel. If it "
            "is showing, call sync_pause(paused=true); if it is not, call set_speed('pause') again."
        ]

    def _finish(
        self, action: str, arguments: dict, lines: list[str], info: WindowInfo, images: list[Shot],
        motion: float | None = None,
    ) -> Result:
        if self._menu_ended:
            lines, self._menu_ended = [self._menu_ended, *lines], ""
        text = "\n".join([*lines, self._state_line(info, motion)])
        self._log(action, arguments, text)
        return Result(text, images)

    def _after_input(
        self, action: str, arguments: dict, lines: list[str], *, mark: bool = False, probe: bool = True
    ) -> Result:
        """The screenshot and status that end an input action.

        `probe` also measures whether the picture is changing and says so when that
        contradicts the pause belief: it is how a game that un-paused itself (a conversation
        closed, character creation was confirmed) is noticed before the next advance. It is
        left out where the action itself moves the view.
        """
        info = self._window()
        if self._menu is None and self._leave_edge(info):
            lines.append(
                "The pointer was then moved in from the edge of the window, where it would have "
                "kept scrolling the camera."
            )
        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        if not probe:
            return self._finish(action, arguments, lines, info, [self._shot(info, mark=mark)])
        frame, motion = self._probe(info)
        lines += self._reconcile(motion)
        return self._finish(action, arguments, lines, info, [self._shot(info, frame, mark=mark)], motion)

    # ---- looking ----------------------------------------------------------------

    @_action(keeps_menu=True)
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
        if self._menu is not None:
            lines.append(self._menu_reminder())
        return self._finish(
            "observe", {"grid": grid}, lines, info, [self._shot(info, frame, grid=grid, mark=self._menu is not None)],
            motion,
        )

    @_action(keeps_menu=True)
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

    @_action
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
            self._modifiers_down(mods)
            for i in range(count):
                self._button_down(button)
                self._hold(max(self.config.click_hold_seconds, hold_seconds))
                self._button_up(button)
                if i < count - 1:
                    self.clock.sleep(0.09)
            self._modifiers_up(mods)

        self._input(run)
        kind = {1: "", 2: "double-", 3: "triple-"}[count]
        held = f", holding for {hold_seconds:g}s" if hold_seconds else ""
        prefix = f"{'+'.join(mods)}+" if mods else ""
        action = f"{prefix}{button} {kind}click".capitalize()
        lines = [f"{action} at ({x:g}, {y:g}){held}. The magenta ring marks where it landed."]
        if button == "right" and hold_seconds >= _MENU_OPENS_AFTER:
            lines.append(
                "A right button held that long opens Kenshi's action menu, which closed again when the "
                "button was released here. To see the menu and choose from it, use menu_open."
            )
        lines += self._steal_warning(mods)
        arguments = {"x": x, "y": y, "button": button, "modifiers": modifiers, "count": count,
                     "hold_seconds": hold_seconds}
        return self._after_input("click", arguments, lines, mark=True)

    @_action
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
            self._modifiers_down(mods)
            self._button_down(button)
            self.clock.sleep(0.08)
            self._glide(info, *end, seconds=self.config.drag_seconds)
            self.clock.sleep(0.08)
            self._button_up(button)
            self._modifiers_up(mods)

        self._input(run)
        lines = [f"Dragged the {button} button from ({x0:g}, {y0:g}) to ({x1:g}, {y1:g})."]
        lines += self._steal_warning(mods)
        arguments = {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "button": button, "modifiers": modifiers}
        return self._after_input("drag", arguments, lines, mark=True)

    @_action
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
                self._wheel(1 if direction == "up" else -1)
                self.clock.sleep(0.03)

        self._input(run)
        lines = [f"Scrolled {direction} {amount} notch(es) at ({x:g}, {y:g})."]
        return self._after_input(
            "scroll", {"x": x, "y": y, "direction": direction, "amount": amount}, lines, mark=True, probe=False
        )

    def _steal_warning(self, mods: list[str]) -> list[str]:
        """Kenshi's highlight key is also what turns a click into stealing or lock-picking."""
        _, key = parse_combo(self.config.keymap.get("highlight_items", "alt"))
        if key not in mods:
            return []
        return [
            f"{key.capitalize()} was held for this. In Kenshi that key is the steal and lock-pick "
            "modifier as well as the highlight key: on an item, container or lock that belongs to "
            "someone else, this was theft or lock-picking, a crime if anyone saw it."
        ]

    # ---- the action menu ---------------------------------------------------------
    #
    # Kenshi's menu of every action on a target opens while the right button is held on it
    # and exists only for as long as the button stays down; an entry is chosen by letting go
    # over it. So the button has to stay down from one call (menu_open, which returns the
    # screenshot that shows the list) to the next (menu_choose or menu_cancel).

    @property
    def menu_held(self) -> bool:
        """Whether the right button is being held for the action menu. Safe to read from any thread."""
        return self._menu is not None

    def _menu_reminder(self) -> str:
        left = max(0.0, self.config.menu_timeout_seconds - (self.clock.now() - self._menu.since))
        return (
            f"The right button is still held at ({self._menu.x:g}, {self._menu.y:g}), where the ring is. "
            "Call menu_choose(x, y) with a point on the row you want, or menu_cancel(). observe and "
            "zoom keep it held; anything else that touches the game, an operator stop, or another "
            f"{left:.0f}s without a choice releases it without choosing."
        )

    def _close_menu(self, why: str) -> None:
        """Let go of the held right button where it is, and remember why for the next result."""
        if self._menu is None:
            return
        try:
            self.backend.button("right", False)
        except Exception:
            pass
        if ("button", "right") in self._held:
            self._held.remove(("button", "right"))
        self._menu = None
        self._menu_ended = f"The action menu was closed without a choice: {why}."
        self._log("menu_release", {}, self._menu_ended)

    def _menu_lapsed(self) -> str | None:
        """Why a held menu has to be let go now, if it has."""
        if self._closing.is_set():
            return "kenshi-link is shutting down"
        limit = self.config.menu_timeout_seconds
        if self.clock.now() - self._menu.since >= limit:
            return f"the button had been held for {limit:g}s"
        try:
            focused = self.backend.locate().focused
        except BackendError:
            focused = False
        return None if focused else "Kenshi lost focus"

    def _review_menu(self) -> None:
        why = self._menu_lapsed()
        if why:
            self._close_menu(why)

    def tend(self) -> None:
        """Look after a held menu between calls: let go of it if the operator has stopped
        the session, the game has lost focus, the time limit has passed or the program is
        shutting down.

        Nothing else notices these while no call is in progress. Whoever owns this controller
        calls it regularly, on the thread that makes the other calls.
        """
        if self._menu is None:
            return
        try:
            self._check_halt()
        except Halted:
            stopped = self.config.stop_file.exists()
            self._close_menu("the operator stopped the session" if stopped else "the desktop is out of reach")
            return
        except ControlError:
            pass  # the stop checks are failing; the time limit still applies
        try:
            self._review_menu()
        except Exception:
            self._release_all()

    @_action
    def menu_open(self, x: float, y: float) -> Result:
        info = self._begin()
        wx, wy = self._window_point(info, x, y)
        # A pointer resting on the window's edge scrolls the camera, and this one rests until
        # a choice is made: keep the press clear of it.
        target = self._off_the_edge(info, wx, wy)
        hold = self.config.menu_hold_seconds
        arguments = {"x": x, "y": y}

        def run() -> Result:
            self._glide(info, *target)
            before = self._grab(info)
            self._button_down("right")
            self._menu = _HeldMenu(x, y, target, self.clock.now())
            self._hold(hold)
            self.clock.sleep(self.config.settle_seconds)
            self._require_focus("holding the right button")
            frame = self._grab(info)
            lines = [
                f"Pressed the right button at ({x:g}, {y:g}) and held it for {hold:g}s. IT IS STILL DOWN. "
                "This screenshot was taken with it held, and the magenta ring marks the pointer."
            ]
            if target != (wx, wy):
                lines.append(
                    "The press was moved a little way in from the edge of the window, because a pointer "
                    "resting on the edge scrolls the camera."
                )
            if self._moving(imaging.motion_fraction(before, frame)) or (self.paused is False):
                lines.append(
                    "Kenshi's action menu lists the target's name, then one row per action, with its "
                    "top-left corner at the pointer unless the screen's edge pushed it aside. If no "
                    "list is showing, nothing here has a menu: letting go then acts as an ordinary "
                    "right-click on this spot."
                )
            else:
                lines.append(
                    "NOTHING CHANGED ON SCREEN when the button went down, so no menu seems to have "
                    "opened: open ground has none, and a target that has one may need the game clock "
                    "running. Letting go now acts as an ordinary right-click on this spot (on open "
                    "ground, a move order)."
                )
            lines.append(self._menu_reminder())
            return self._finish("menu_open", arguments, lines, info, [self._shot(info, frame, mark=True)])

        return self._input(run)

    @_action(keeps_menu=True)
    def menu_choose(self, x: float, y: float) -> Result:
        info = self._begin()  # a stop is reported as a stop; a hold that has lapsed is let go
        if self._menu is None:
            why, self._menu_ended = self._menu_ended, ""
            raise ControlError(
                f"No action menu is being held, so nothing was chosen. {why + ' ' if why else ''}"
                "Call menu_open on the target first."
            )
        wx, wy = self._window_point(info, x, y)

        def run() -> None:
            self._glide(info, wx, wy, seconds=self.config.drag_seconds)
            self._require_pointer_on_game()
            self.clock.sleep(0.08)
            self._button_up("right")
            self._menu = None

        self._input(run)
        lines = [
            f"Moved to ({x:g}, {y:g}) with the right button held and released it there; the magenta "
            "ring marks the spot. If that was a row of the action menu, its order has been given: "
            "check what the character is now doing."
        ]
        return self._after_input("menu_choose", {"x": x, "y": y}, lines, mark=True)

    @_action(keeps_menu=True)
    def menu_cancel(self) -> Result:
        info = self._begin() if self._menu is not None else None
        if self._menu is None:  # never held, or let go already (the reason is then on record)
            why, self._menu_ended = self._menu_ended, ""
            text = why or "No action menu was being held; nothing was sent."
            self._log("menu_cancel", {}, text)
            return Result(text)
        pressed = self._menu.point

        def run() -> None:
            if self.backend.cursor() != (info.left + pressed[0], info.top + pressed[1]):
                self._glide(info, *pressed)  # something moved it: back to where the menu's title is
            self._button_up("right")
            self._menu = None

        self._input(run)
        lines = [
            "Released the right button where it was pressed. With the action menu open that is its "
            "title, which chooses nothing. If no menu had opened, or the screen's edge had pushed "
            "the list under the pointer, this was a right-click on what lies there: check the screenshot."
        ]
        return self._after_input("menu_cancel", {}, lines, mark=True)

    # ---- keyboard ---------------------------------------------------------------

    def _modifiers(self, modifiers: str) -> list[str]:
        try:
            mods = parse_modifiers(modifiers)
            check_modifiers(mods)
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc
        return mods

    def _checked_combo(self, combo: str) -> tuple[list[str], str]:
        try:
            mods, key = parse_combo(combo)
            check_allowed(
                mods, key, allow_debug_keys=self.config.allow_debug_keys,
                allow_shift_tab=self.config.allow_shift_tab,
            )
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc
        return mods, key

    def _same_combo(self, mods: list[str], key: str, action: str) -> bool:
        other_mods, other_key = parse_combo(self.config.keymap[action])
        return key == other_key and set(mods) == set(other_mods)

    @_action
    def press_key(self, key: str, repeat: int = 1, hold_seconds: float = 0.0) -> Result:
        if not 1 <= repeat <= 20:
            raise ControlError("repeat must be between 1 and 20.")
        if not 0 <= hold_seconds <= self.config.max_hold_seconds:
            raise ControlError(f"hold_seconds must be between 0 and {self.config.max_hold_seconds:g}.")
        mods, name = self._checked_combo(key)
        if name == "escape":
            raise ControlError(_ESCAPE_REFUSED)
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
            lines.append(
                "That is the pause key. It toggles, so this tool's record was flipped; whether the "
                "game followed depends on what state it was really in. Prefer set_speed for this."
            )
        for speed in SPEEDS[1:]:
            if self._same_combo(mods, name, f"speed_{speed}"):
                self.speed, self.paused, self.pause_source = speed, False, "tracked"
                lines.append(f"That is the key for {speed} speed, which also ends a pause: the game is running.")
        if self._same_combo(mods, name, "build_mode") and repeat % 2 == 1:
            lines += self._build_mode_pressed()
        return self._after_input(
            "press_key", {"key": key, "repeat": repeat, "hold_seconds": hold_seconds}, lines
        )

    def _build_mode_pressed(self) -> list[str]:
        """The build window makes the pause belief worthless, in both directions."""
        self._forget_pause()
        return [
            "Kenshi pauses itself when the build window opens. While it is open the pause key confirms "
            "the build instead of pausing, and the speed keys close the window: so close it (this key "
            "again) before set_speed or advance."
        ]

    @_action
    def type_text(self, text: str) -> Result:
        if not text:
            raise ControlError("text is empty.")
        if len(text) > 200:
            raise ControlError("text is limited to 200 characters per call.")
        try:
            strokes = [char_to_key(char) for char in text]
            self._begin()
            if self.backend.caps_lock() and any(char.isalpha() for char in text):
                raise ControlError(
                    "Caps Lock is on, so the letters would come out in the wrong case. Nothing was "
                    "typed. Ask the operator to turn Caps Lock off."
                )
            # Key names are positions on a US keyboard; the game turns key presses into
            # characters with the operator's layout, which may put them elsewhere.
            strokes = self.backend.typing_keys(text) or strokes
        except BlockedInput as exc:
            raise ControlError(str(exc)) from exc
        except BackendError as exc:
            raise self._control_error(exc) from exc

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

    @_action
    def hotkey(self, action: str, repeat: int = 1, in_game: bool = False) -> Result:
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
        if name == "escape":
            # With no window open, Escape on Kenshi's title screen quits the game at once.
            # Nothing here can tell the title screen from a game, so Claude has to say.
            if not in_game:
                raise ControlError(_ESCAPE_REFUSED)
            if repeat != 1:
                raise ControlError(
                    "Escape is pressed once per call: a second press opens the game menu, or quits "
                    "Kenshi if this is the title screen after all. Look at the screenshot in between."
                )
        self._begin()
        arguments = {"action": action, "repeat": repeat}

        if action == "highlight_items":
            # The labels only show while the key is down, so the screenshot is taken mid-hold.
            # The same key is Kenshi's steal and lock-pick modifier: it is down for this one
            # screenshot and nothing is clicked meanwhile.
            def hold_and_look() -> Result:
                for key in [*mods, name]:
                    self._key_down(key)
                self._hold(max(0.5, self.config.settle_seconds))
                self._require_focus("holding the highlight key")
                info = self.backend.locate()
                shot = self._shot(info)
                for key in reversed([*mods, name]):
                    self._key_up(key)
                lines = [
                    f"Held {combo} (highlight items) for this screenshot only, then released it; nothing "
                    "was clicked while it was down. That key is also Kenshi's steal and lock-pick "
                    "modifier: a click with it held takes an item that belongs to someone else or "
                    "starts picking a lock."
                ]
                return self._finish("hotkey", arguments, lines, info, [shot])

            return self._input(hold_and_look)

        def run() -> None:
            for _ in range(repeat):
                self._tap(combo)
                self.clock.sleep(0.05)

        self._input(run)
        lines = [f"Pressed {combo} ({action})" + (f" x{repeat}" if repeat > 1 else "") + "."]
        if action == "quick_load":
            self._forget_pause()
            self.clock.sleep(1.0)
            lines.append("A load was requested; wait for it to finish, then observe to re-check the pause state.")
            return self._after_input("hotkey", arguments, lines, probe=False)
        if action == "build_mode" and repeat % 2 == 1:
            lines += self._build_mode_pressed()
        return self._after_input("hotkey", arguments, lines)

    # ---- camera -----------------------------------------------------------------

    @_action
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
                    self._wheel(1 if action == "zoom_in" else -1)
                    self.clock.sleep(0.03)
            elif action in ("tilt_up", "tilt_down"):
                # Stop short of the window's edge, where the pointer would also scroll the view.
                travel = min(steps * _TILT_STEP_PIXELS, info.height // 2 - self._scroll_margin(info)[1] - 1)
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
        return self._after_input("camera", {"action": action, "steps": steps}, lines, probe=False)

    # ---- time -------------------------------------------------------------------

    @_action
    def set_speed(self, speed: str) -> Result:
        if speed not in SPEEDS:
            raise ControlError(f"speed must be one of: {', '.join(SPEEDS)}.")
        try:
            return self._set_speed(speed)
        finally:
            if speed == "pause":
                self._pause_requested.clear()  # this call was the request (see request_pause)

    def _set_speed(self, speed: str) -> Result:
        info = self._begin()
        lines: list[str] = []
        pressed = False

        def run() -> None:
            nonlocal pressed
            if speed != "pause":
                self._resume(speed)
                lines.append(
                    f"The game is now RUNNING at {speed} speed and will keep running while you think. "
                    "Pause again as soon as you need to decide something."
                )
                return
            if self.paused is None:
                _, motion = self._probe(info)
                lines.append(self._infer_pause(motion))
            if self.paused:
                lines.append(
                    "This tool's record says the game is already paused, so nothing was pressed. If "
                    "the PAUSED panel is not showing, call sync_pause(paused=false) and then this again."
                )
            else:
                self._pause()
                pressed = True
                lines.append("Paused the game.")

        self._input(run)
        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        frame, motion = self._probe(info)
        lines += self._confirm_pause(motion) if pressed else self._reconcile(motion)
        return self._finish("set_speed", {"speed": speed}, lines, info, [self._shot(info, frame)], motion)

    @_action
    def advance(self, seconds: float, speed: str = "normal", frames: int = 2) -> Result:
        if speed not in SPEEDS[1:]:
            raise ControlError(f"speed must be one of: {', '.join(SPEEDS[1:])}.")
        limit = self.config.max_advance_seconds
        if not 0.2 <= seconds <= limit:
            raise ControlError(f"seconds must be between 0.2 and {limit:g}.")
        if not 0 <= frames <= 4:
            raise ControlError("frames must be between 0 and 4.")
        info = self._begin()
        arguments = {"seconds": seconds, "speed": speed, "frames": frames}
        lines: list[str] = []
        samples: list[Image.Image] = []
        first = self._grab(info)  # what the screen showed before the clock was started

        self._input(self._resume, speed)
        began = self.clock.now()
        sample_times = [began + seconds * (i + 1) / (frames + 1) for i in range(frames)]
        left_running = f"The game was not paused: it was left running at {speed} speed."
        interrupted: Halted | None = None
        cut_short = ""  # why the run ended before its time, if it did
        while True:
            now = self.clock.now()
            if now >= began + seconds:
                break
            self.clock.sleep(min(self.config.halt_poll_seconds, began + seconds - now))
            if self._closing.is_set() or self._pause_requested.is_set():
                self._pause_requested.clear()
                cut_short = "a pause was asked for"
                break
            try:
                self._check_halt()
            except Halted as exc:
                interrupted = exc
                break
            except Exception as exc:
                # The stop checks themselves are failing. Do not sit out the rest of the
                # run blind: pause now, and report what went wrong with the result.
                cut_short = f"the operator's stop could not be checked ({exc})"
                break
            if sample_times and self.clock.now() >= sample_times[0]:
                sample_times.pop(0)
                try:
                    current = self.backend.locate()
                    if current.focused:  # never capture whatever else is on top
                        samples.append(
                            self.backend.capture(current.left, current.top, current.width, current.height)
                        )
                except Exception:
                    pass  # a missed frame is not worth the run; a real problem shows at the pause
        ran_for = self.clock.now() - began
        if interrupted is not None:
            # The operator has taken over; send nothing more, not even the pause key.
            self._forget_pause()
            raise Halted(f"{interrupted} {left_running}") from interrupted

        last: Image.Image | None = None
        try:
            info = self._window()
            if not self._closing.is_set():
                try:
                    last = self.backend.capture(info.left, info.top, info.width, info.height)
                except Exception:
                    pass  # only used to tell whether anything happened
            self._input(self._pause)
        except Halted as exc:  # the desktop went away (locked screen): the key cannot get there
            self.paused = False
            raise Halted(f"{exc} {left_running}") from exc
        except ControlError as exc:
            self.paused = False
            raise ControlError(
                f"THE GAME IS STILL RUNNING at {speed} speed: it could not be paused after "
                f"{ran_for:.1f}s because: {exc}"
            ) from exc
        if self._closing.is_set():
            text = f"Shutting down: the run was stopped after {ran_for:.1f}s and the game was paused."
            self._log("advance", arguments, text)
            raise Interrupted(text)

        self.clock.sleep(self.config.settle_seconds)
        info = self._window()
        frame, motion = self._probe(info)
        lines.append(f"Ran the game for {ran_for:.1f}s of real time at {speed} speed, then paused it.")
        if cut_short:
            lines.append(f"That is less than the {seconds:g}s asked for, because {cut_short}.")
        if last is not None:
            lines += self._what_the_run_showed([first, *samples, last])
        images: list[Shot] = []
        strip = imaging.filmstrip(samples)
        if strip is not None:
            images.append(self._encode(strip))
            lines.append(
                f"Image 1 is a strip of {len(samples)} frame(s) captured along the way (oldest on the left); "
                "image 2 is the screen now."
            )
        images.append(self._shot(info, frame))
        lines += self._confirm_pause(motion)
        return self._finish("advance", arguments, lines, info, images, motion)

    def _what_the_run_showed(self, frames: list[Image.Image]) -> list[str]:
        """Whether the picture kept changing through a run, from the frames taken along it.

        A game that pauses itself part-way (a conversation opens, an area loads) cannot be
        told from the keys pressed, only from a picture that stops changing.
        """
        changed = [self._moving(imaging.motion_fraction(a, b)) for a, b in zip(frames, frames[1:])]
        if not any(changed):
            return [
                "NOTHING ON SCREEN CHANGED during the run. Either nothing in view was moving, or the "
                "clock never ran: a conversation, the game menu or a loading screen can hold Kenshi "
                "paused whatever key is pressed. Check the screenshot before advancing again."
            ]
        if len(changed) > 1 and not changed[-1]:
            return [
                "The picture stopped changing before the end of the run. Either everything in view "
                "came to rest, or Kenshi paused itself part-way, as it does when a conversation opens "
                "or an area loads: look at the strip and the screenshot."
            ]
        return []

    def sync_pause(self, paused: bool) -> Result:
        self.paused = bool(paused)
        self.pause_source = "told"
        text = f"Recorded that the game is {'PAUSED' if paused else 'RUNNING'}. No key was pressed."
        if not paused:
            text += " Call set_speed('pause') to pause it."
        self._log("sync_pause", {"paused": paused}, text)
        return Result(text)

    # ---- housekeeping -----------------------------------------------------------

    def describe(self) -> str:
        """Plain-text health report used by `kenshi-link doctor`."""
        lines = [f"backend: {self.backend.name}"]
        try:
            info = self.backend.locate()
        except WindowNotFound as exc:
            return "\n".join([*lines, f"window: NOT FOUND - {exc}"])
        except BackendError as exc:
            return "\n".join([*lines, f"window: UNUSABLE - {exc}"])
        fit = self._fit(info) if info.width and info.height else None
        lines.append(f"window: {info.title!r}")
        lines.append(f"client area: {info.width}x{info.height} at ({info.left}, {info.top}) on screen")
        lines.append(f"focused: {info.focused}")
        if fit:
            lines.append(f"screenshot size sent to Claude: {fit.width}x{fit.height} (scale {fit.scale:.3f})")
        lines.append(f"stop file: {'PRESENT - input disabled' if self.config.stop_file.exists() else 'absent'}")
        lines += self.backend.notes()
        return "\n".join(lines)

    def release_held(self) -> None:
        """Let go of every key and button this controller is holding down."""
        self._release_all()

    def close(self) -> None:
        self._close_menu("kenshi-link is shutting down")
        self._release_all()
        self.backend.close()


def _decode(data: bytes) -> str:
    """Text from a file the operator may have written with any tool; it never fails.

    These files are UTF-8 when kenshi-link writes them. Windows editors and PowerShell may
    add a byte-order mark, PowerShell's `>` writes UTF-16, and older editors save in the
    system code page.
    """
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = data.decode("utf-16", errors="replace")
    else:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode(locale.getencoding(), errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _stop_reason(path: Path) -> str:
    """The first line of the stop file. Its existence is what stops input; the text is
    only shown as the reason, so an unreadable or empty file still stops everything."""
    try:
        text = _decode(path.read_bytes())
    except OSError:
        return "stop file present"
    lines = text.replace("\x00", "").strip().splitlines()
    return lines[0].strip() if lines else "stop file present"


def read_notes(path: Path) -> str:
    try:
        return _decode(path.read_bytes())
    except FileNotFoundError:
        return ""


def write_notes(path: Path, text: str, mode: str = "append") -> int:
    """Save notes and return the file's new length in characters."""
    if mode not in ("append", "replace"):
        raise ControlError("mode must be 'append' or 'replace'.")
    # Text mode writes each "\n" as the platform's line ending; a "\r\n" passed through
    # would land on disk as "\r\r\n" on Windows and read back as a blank line.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "replace":
        content = text.rstrip() + "\n"
    else:
        existing = read_notes(path)
        separator = "" if not existing or existing.endswith("\n") else "\n"
        content = existing + separator + text.rstrip() + "\n"
    path.write_text(content, encoding="utf-8")
    return len(content)
