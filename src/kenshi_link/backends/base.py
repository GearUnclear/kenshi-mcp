"""The small surface every platform implements: find the window, look at it, press things.

All coordinates here are physical screen pixels. The controller owns the mapping
between the image Claude sees, the window's client area and the screen.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image


class BackendError(Exception):
    """The platform layer could not do what was asked."""


class WindowNotFound(BackendError):
    """No Kenshi window is open (or it has no visible area)."""


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
        """Find the game window. Raises WindowNotFound."""

    @abstractmethod
    def focus(self) -> None:
        """Ask the desktop to bring the game window to the front."""

    @abstractmethod
    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        """Grab a rectangle of the screen as an RGB image."""

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        """Move the pointer to a screen position."""

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

    def panic_pressed(self) -> bool:
        """Whether the operator is holding the panic key (Pause/Break)."""
        return False

    def close(self) -> None:
        """Release platform resources."""
