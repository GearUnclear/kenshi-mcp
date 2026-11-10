"""A stand-in window for trying the interface and for tests. It is not Kenshi.

It draws an abstract test card (numbered dots on a grid) and reacts to the same
kinds of input the controller sends a real game: pause toggling, speed keys,
click-to-select, right-click-to-move, camera keys and the wheel.

Where Kenshi's handling of an input is what makes it awkward to automate, the stand-in
copies it: an action menu that exists only while the right button is held, speed keys
that set a speed outright while the pause key toggles, pauses the game makes by itself
(a conversation, the build window), a camera that scrolls while the pointer rests on
the window's edge, and a title screen that Escape quits.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from PIL import Image, ImageDraw, ImageFont

from ..config import Config
from ..keys import char_to_key
from .base import Backend, Clock, WindowInfo

_SPEED_KEYS = {"f2": 1.0, "f3": 2.0, "f4": 4.0}
_PAN_KEYS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
_UNIT_SPEED = 40.0  # world units per game second
_PAN_SPEED = 300.0  # world units per held second
_EDGE_SPEED = 300.0  # world units per second while the pointer rests on the window's edge
_EDGE_ZONE = 0.01  # the outer share of the window, each side, that scrolls the camera
_MENU_HOLD = 0.2  # the right button must stay down this long on a unit before its menu opens
_MENU_WIDTH, _MENU_TITLE, _MENU_ROW = 160, 24, 30
_MENU_ROWS = ("Option 1", "Option 2")
_SELECT_RADIUS = 26


@dataclass
class Unit:
    number: int
    x: float
    y: float
    target: tuple[float, float] | None = None
    selected: bool = False


@dataclass
class MockBackend(Backend):
    config: Config
    clock: Clock = field(default_factory=Clock)
    name: str = "mock"

    def __post_init__(self) -> None:
        self.left, self.top = 120, 60
        self.width, self.height = self.config.mock_width, self.config.mock_height
        self.focused = True
        self.present = True
        self.paused = True
        self.speed = 1.0
        self.game_time = 0.0
        self.camera = [0.0, 0.0]
        self.zoom = 1.0
        self.heading = 0.0
        self.units = [Unit(1, -120, -40), Unit(2, 60, 80), Unit(3, 200, -150)]
        self.menu: tuple[int, int] | None = None  # top-left corner of the open action menu
        self.menu_unit: int | None = None  # the unit it is for
        self.chosen: list[tuple[int, int]] = []  # (unit, row) for every menu entry chosen
        self.resume_speed = 1.0  # what the pause key goes back to
        self.conversation = False  # a conversation window is open, which holds the game paused
        self._before_conversation: bool | None = None
        self.build_mode = False  # the build window is open: Space places, it does not pause
        self.placed = 0  # buildings placed with Space in build mode
        self.title_screen = False  # no game is loaded: Escape quits
        self.quit = False
        self.speed_keys_resume = True  # False stands in for a state in which the speed keys are ignored
        self.typed = ""
        self.log: list[str] = []
        self.events: list[tuple] = []
        self._pointer = (self.left + self.width // 2, self.top + self.height // 2)
        self._held_keys: dict[str, float] = {}
        self._held_buttons: dict[str, tuple[float, tuple[int, int]]] = {}
        self._last_tick = self.clock.now()
        self.stamps: list[float] = []  # when each entry of `events` happened
        # Things a test can set to stand in for the operator and the desktop.
        self.panic = False  # the panic key is being held
        self.panic_callback = None  # called for a panic-key press, however short
        self.obstructed = False  # another window lies over the game at the pointer
        self.screen: tuple[int, int, int, int] | None = None  # desktop bounds, if they matter
        self.corner = (0, 0)  # the failsafe corner
        self.layout: dict[str, tuple[str, bool]] | None = None  # a non-US keyboard layout
        self.caps = False  # Caps Lock is on

    def _record(self, *event) -> None:
        self.events.append(event)
        self.stamps.append(self.clock.now())

    # ---- simulation -------------------------------------------------------------

    def _tick(self) -> None:
        now = self.clock.now()
        elapsed, self._last_tick = now - self._last_tick, now
        if elapsed <= 0:
            return
        for key, (dx, dy) in _PAN_KEYS.items():
            if key in self._held_keys:
                self.camera[0] += dx * _PAN_SPEED * elapsed
                self.camera[1] += dy * _PAN_SPEED * elapsed
        if "q" in self._held_keys:
            self.heading -= 90 * elapsed
        if "e" in self._held_keys:
            self.heading += 90 * elapsed
        self._edge_scroll(elapsed)
        self._open_menu_if_held()
        if self.paused:
            return
        game_elapsed = elapsed * self.speed
        self.game_time += game_elapsed
        for unit in self.units:
            if unit.target is None:
                continue
            dx, dy = unit.target[0] - unit.x, unit.target[1] - unit.y
            distance = math.hypot(dx, dy)
            step = _UNIT_SPEED * game_elapsed
            if distance <= step:
                unit.x, unit.y, unit.target = unit.target[0], unit.target[1], None
            else:
                unit.x += dx / distance * step
                unit.y += dy / distance * step

    def _edge_scroll(self, elapsed: float) -> None:
        """The camera pans while the pointer rests in the outer 1% of the window, paused or not."""
        position = self._pointer_in_window()
        if position is None or not self.focused:
            return
        for axis, size in ((0, self.width), (1, self.height)):
            share = position[axis] / size
            if share < _EDGE_ZONE:
                self.camera[axis] -= _EDGE_SPEED * elapsed
            elif share > 1 - _EDGE_ZONE:
                self.camera[axis] += _EDGE_SPEED * elapsed

    def _unit_at(self, position: tuple[int, int]) -> Unit | None:
        nearest, best = None, _SELECT_RADIUS
        for unit in self.units:
            ux, uy = self._to_window(unit.x, unit.y)
            distance = math.hypot(ux - position[0], uy - position[1])
            if distance <= best:
                nearest, best = unit, distance
        return nearest

    def _open_menu_if_held(self) -> None:
        """The action menu opens once the right button has rested on a unit long enough.

        Its top-left corner goes where the pointer is, pushed back inside the window if
        need be. Open ground has no menu, and neither does a press that moved off its unit
        before the time was up.
        """
        pressed = self._held_buttons.get("right")
        position = self._pointer_in_window()
        if pressed is None or self.menu is not None or position is None or position != pressed[1]:
            return
        if self.clock.now() - pressed[0] < _MENU_HOLD:
            return
        unit = self._unit_at(position)
        if unit is None:
            return
        height = _MENU_TITLE + _MENU_ROW * len(_MENU_ROWS)
        self.menu = (min(position[0], self.width - _MENU_WIDTH - 1), min(position[1], self.height - height - 1))
        self.menu_unit = unit.number
        self._note(f"menu opened at {position}")

    def _menu_row(self, position: tuple[int, int]) -> int | None:
        """Which row of the open menu a point is on, counting from 1; None for the title or outside."""
        if self.menu is None:
            return None
        dx, dy = position[0] - self.menu[0], position[1] - self.menu[1] - _MENU_TITLE
        if not (0 <= dx <= _MENU_WIDTH and 0 <= dy < _MENU_ROW * len(_MENU_ROWS)):
            return None
        return dy // _MENU_ROW + 1

    def _close_menu(self, position: tuple[int, int]) -> None:
        """A button was let go while the menu showed: over a row that is a choice. Either way it closes."""
        row = self._menu_row(position)
        if row is not None:
            self.chosen.append((self.menu_unit, row))
            self._note(f"menu option {row} chosen")
        self.menu = self.menu_unit = None

    # ---- what the game does to its own clock ------------------------------------

    def open_conversation(self) -> None:
        """A conversation window opens: the game pauses itself until it closes."""
        self.conversation, self._before_conversation = True, self.paused
        self.paused = True

    def close_conversation(self) -> None:
        """... and goes back to how it was, which un-pauses a game that had been running."""
        self.conversation = False
        if self._before_conversation is False:
            self.paused = False
        self._before_conversation = None

    def _to_window(self, wx: float, wy: float) -> tuple[float, float]:
        return (
            (wx - self.camera[0]) * self.zoom + self.width / 2,
            (wy - self.camera[1]) * self.zoom + self.height / 2,
        )

    def _to_world(self, px: float, py: float) -> tuple[float, float]:
        return (
            (px - self.width / 2) / self.zoom + self.camera[0],
            (py - self.height / 2) / self.zoom + self.camera[1],
        )

    def _pointer_in_window(self) -> tuple[int, int] | None:
        x, y = self._pointer[0] - self.left, self._pointer[1] - self.top
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        return None

    def _note(self, text: str) -> None:
        self.log.append(text)
        del self.log[:-4]

    # ---- Backend ----------------------------------------------------------------

    def locate(self) -> WindowInfo:
        from .base import WindowNotFound

        if not self.present:
            raise WindowNotFound("No Kenshi window found (mock window is closed).")
        return WindowInfo(
            "kenshi-link mock window", self.left, self.top, self.width, self.height, self.focused
        )

    def focus(self) -> None:
        self._record("focus")
        self.focused = True

    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        self._tick()
        frame = self._render()
        box = (left - self.left, top - self.top, left - self.left + width, top - self.top + height)
        return frame.crop(box)

    def move(self, x: int, y: int) -> None:
        self._tick()
        self._pointer = (x, y)
        self._record("move", x, y)

    def button(self, button: str, down: bool) -> None:
        self._tick()
        self._record("button", button, down, *self._pointer)
        if not self.focused:
            return
        position = self._pointer_in_window()
        if down:
            if position is not None:
                self._held_buttons[button] = (self.clock.now(), position)
            return
        pressed = self._held_buttons.pop(button, None)
        if pressed is None or position is None:
            if button == "right":
                self.menu = self.menu_unit = None
            return
        start = pressed[1]
        moved = math.hypot(position[0] - start[0], position[1] - start[1])
        if self.menu is not None:
            # While the menu shows, a release of any button over a row chooses it, and a
            # click anywhere else does nothing. Letting go of the right button closes it.
            if button == "right" or self._menu_row(position) is not None:
                self._close_menu(position)
        elif button == "left":
            if moved > 8:
                self._box_select(start, position)
            else:
                self._left_click(position)
        elif button == "right":
            self._right_click(position)

    def _left_click(self, position: tuple[int, int]) -> None:
        add = "shift" in self._held_keys
        nearest = self._unit_at(position)
        if not add:
            for unit in self.units:
                unit.selected = False
        if nearest is not None:
            nearest.selected = True
            self._note(f"selected unit {nearest.number}")

    def _box_select(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        x0, x1 = sorted((start[0], end[0]))
        y0, y1 = sorted((start[1], end[1]))
        for unit in self.units:
            ux, uy = self._to_window(unit.x, unit.y)
            unit.selected = x0 <= ux <= x1 and y0 <= uy <= y1
        self._note(f"box-selected {sum(u.selected for u in self.units)} unit(s)")

    def _right_click(self, position: tuple[int, int]) -> None:
        target = self._to_world(*position)
        moved = [u for u in self.units if u.selected]
        for unit in moved:
            unit.target = target
        if moved:
            self._note(f"move order for {len(moved)} unit(s)")

    def wheel(self, clicks: int) -> None:
        self._tick()
        self._record("wheel", clicks)
        if self.focused:
            self.zoom = max(0.25, min(4.0, self.zoom * (1.1**clicks)))

    def key(self, key: str, down: bool) -> None:
        self._tick()
        self._record("key", key, down)
        if not self.focused:
            return
        if not down:
            self._held_keys.pop(key, None)
            return
        self._held_keys[key] = self.clock.now()
        if key == "space":
            if self.build_mode:
                self.placed += 1  # in build mode this key confirms the placement
                self._note("building placed")
            elif self.paused:
                self.paused, self.speed = False, self.resume_speed
            else:
                self.paused, self.resume_speed = True, self.speed
        elif key in _SPEED_KEYS:
            if self.speed_keys_resume:
                # A speed key sets that speed outright, which ends a pause; it also closes
                # the build window.
                self.speed, self.paused, self.build_mode = _SPEED_KEYS[key], False, False
        elif key == "b":
            self.build_mode = not self.build_mode
            if self.build_mode and not self.paused:
                self.paused, self.resume_speed = True, self.speed  # opening it pauses the game
        elif key in "1234567890" and len(key) == 1:
            index = 10 if key == "0" else int(key)
            for unit in self.units:
                unit.selected = unit.number == index
        elif key == "grave":
            for unit in self.units:
                unit.selected = True
        elif key == "escape":
            if self.title_screen:
                self.quit, self.present = True, False  # no question asked
            self.build_mode = False
        if len(key) == 1 and key.isalnum():
            self.typed += key.upper() if "shift" in self._held_keys else key

    def cursor(self) -> tuple[int, int]:
        return self._pointer

    def panic_pressed(self) -> bool:
        return self.panic

    def watch_panic(self, callback) -> None:
        self.panic_callback = callback

    def pointer_on_window(self) -> bool:
        return not self.obstructed

    def screen_rect(self) -> tuple[int, int, int, int] | None:
        return self.screen

    def failsafe_corner(self) -> tuple[int, int]:
        return self.corner

    def typing_keys(self, text: str) -> list[tuple[str, bool]] | None:
        if self.layout is None:
            return None
        return [self.layout.get(char, char_to_key(char)) for char in text]

    def caps_lock(self) -> bool:
        return self.caps

    # ---- drawing ----------------------------------------------------------------

    def _render(self) -> Image.Image:
        image = Image.new("RGB", (self.width, self.height), (38, 42, 48))
        draw = ImageDraw.Draw(image)
        try:
            small, big = ImageFont.load_default(size=16), ImageFont.load_default(size=40)
        except TypeError:
            small = big = ImageFont.load_default()

        spacing = 100 * self.zoom
        if spacing >= 8:
            offset_x = (self.width / 2 - self.camera[0] * self.zoom) % spacing
            offset_y = (self.height / 2 - self.camera[1] * self.zoom) % spacing
            x = offset_x
            while x < self.width:
                draw.line([(x, 0), (x, self.height)], fill=(52, 57, 64))
                x += spacing
            y = offset_y
            while y < self.height:
                draw.line([(0, y), (self.width, y)], fill=(52, 57, 64))
                y += spacing

        for unit in self.units:
            ux, uy = self._to_window(unit.x, unit.y)
            if unit.target is not None:
                tx, ty = self._to_window(*unit.target)
                draw.line([(ux, uy), (tx, ty)], fill=(110, 110, 120))
                draw.line([(tx - 5, ty - 5), (tx + 5, ty + 5)], fill=(230, 230, 230), width=2)
                draw.line([(tx - 5, ty + 5), (tx + 5, ty - 5)], fill=(230, 230, 230), width=2)
            radius = 14
            colour = (240, 190, 60) if unit.selected else (90, 150, 220)
            draw.ellipse([ux - radius, uy - radius, ux + radius, uy + radius], fill=colour)
            if unit.selected:
                draw.ellipse(
                    [ux - radius - 5, uy - radius - 5, ux + radius + 5, uy + radius + 5],
                    outline=(255, 255, 255),
                    width=2,
                )
            draw.text((ux - 5, uy - 9), str(unit.number), fill=(0, 0, 0), font=small)

        if self.menu is not None:
            mx, my = self.menu
            height = _MENU_TITLE + _MENU_ROW * len(_MENU_ROWS)
            draw.rectangle([mx, my, mx + _MENU_WIDTH, my + height], fill=(20, 20, 24), outline=(220, 220, 220))
            draw.text((mx + 10, my + 3), f"Unit {self.menu_unit}", fill=(240, 190, 60), font=small)
            for i, label in enumerate(_MENU_ROWS):
                top = my + _MENU_TITLE + i * _MENU_ROW
                draw.line([(mx, top), (mx + _MENU_WIDTH, top)], fill=(90, 90, 90))
                draw.text((mx + 10, top + 6), label, fill=(240, 240, 240), font=small)

        for i, label in enumerate(
            text for text, shown in (("BUILD MODE", self.build_mode), ("CONVERSATION", self.conversation),
                                     ("TITLE SCREEN", self.title_screen)) if shown
        ):
            draw.text((self.width - 170, 34 + i * 22), label, fill=(240, 190, 60), font=small)

        status = f"kenshi-link mock   t={self.game_time:6.1f}s   speed x{self.speed:g}   zoom {self.zoom:.2f}"
        draw.rectangle([0, 0, self.width, 26], fill=(18, 20, 24))
        draw.text((10, 4), status, fill=(210, 210, 210), font=small)
        if self.paused:
            label = "PAUSED"
            box = draw.textbbox((0, 0), label, font=big)
            draw.text(((self.width - box[2]) / 2, 44), label, fill=(255, 90, 90), font=big)
        for i, line in enumerate(reversed(self.log)):
            draw.text((10, self.height - 24 - i * 20), line, fill=(170, 200, 170), font=small)
        return image
