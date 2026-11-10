"""The small surface every platform implements: find the window, look at it, press things.

All coordinates here are physical screen pixels. The controller owns the mapping
between the image Claude sees, the window's client area and the screen.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from PIL import Image


class BackendError(Exception):
    """The platform layer could not do what was asked."""


class WindowNotFound(BackendError):
    """No Kenshi window is open (or it has no visible area)."""


class DesktopUnavailable(BackendError):
    """The desktop itself cannot be seen or sent input (locked screen, security prompt).

    Nothing a tool call does can change that, so the controller reports it as a halt.
    """


@dataclass(frozen=True)
class WindowInfo:
    title: str
    left: int  # screen position of the client area's top-left corner
    top: int
    width: int  # client area size
    height: int
    focused: bool


class Clock:
    """Real time. Tests swap in a fake so nothing actually sleeps."""

    def now(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        if seconds > 0:
            time.sleep(seconds)


BUTTONS = ("left", "right", "middle")


class Backend(ABC):
    name: str = "backend"

    @abstractmethod
    def locate(self) -> WindowInfo:
        """Find the game window. Raises WindowNotFound, or BackendError if it cannot be used."""

    @abstractmethod
    def focus(self) -> None:
        """Ask the desktop to bring the game window to the front."""

    def focus_error(self) -> str:
        """Why the last focus() did not work, if the platform said; shown to the operator."""
        return ""

    @abstractmethod
    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        """Grab a rectangle of the screen as an RGB image."""

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        """Move the pointer to a screen position."""

    def place(self, x: int, y: int) -> None:
        """Put the pointer exactly on a screen position, after move() left it elsewhere.

        Only platforms whose move() can land a pixel off need more than move() here.
        """
        self.move(x, y)

    @abstractmethod
    def button(self, button: str, down: bool) -> None:
        """Press or release 'left', 'right' or 'middle' at the pointer."""

    @abstractmethod
    def wheel(self, clicks: int) -> None:
        """Turn the wheel: positive is away from the user (zoom in / scroll up)."""

    @abstractmethod
    def key(self, key: str, down: bool) -> None:
        """Press or release a key by its canonical name from keys.KEYS."""

    @abstractmethod
    def cursor(self) -> tuple[int, int]:
        """Where the pointer is on screen."""

    def pointer_on_window(self) -> bool:
        """Whether the game is what a click at the pointer would reach.

        Focus says where keys go; a click goes to whatever is under the pointer, which can
        be a notification or an always-on-top window lying over the game.
        """
        return True

    def screen_rect(self) -> tuple[int, int, int, int] | None:
        """The desktop as (left, top, width, height), or None if the platform cannot say."""
        return None

    def failsafe_corner(self) -> tuple[int, int]:
        """The screen corner the operator pushes the mouse into to stop everything."""
        return (0, 0)

    def panic_pressed(self) -> bool:
        """Whether the operator is holding the panic key (Pause/Break)."""
        return False

    def watch_panic(self, callback: Callable[[], None]) -> None:
        """Have `callback` called, from any thread, whenever the panic key is pressed.

        For platforms that can be told about a key press. The others leave this alone and
        are polled through panic_pressed(), which only sees a key that is still down.
        """

    def typing_keys(self, text: str) -> list[tuple[str, bool]] | None:
        """The (key name, shift?) to press for each character on the game's keyboard layout.

        None means the platform cannot tell, and the US positions are used. Raises
        keys.BlockedInput for a character the layout cannot produce.
        """
        return None

    def caps_lock(self) -> bool:
        """Whether Caps Lock is on, which would invert the case of typed letters."""
        return False

    def notes(self) -> list[str]:
        """Extra lines for `kenshi-link doctor`."""
        return []

    def close(self) -> None:
        """Release platform resources."""
