"""Platform backends and the factory that picks one."""

from __future__ import annotations

import sys

from ..config import Config
from .base import Backend, BackendError, Clock, WindowInfo, WindowNotFound

__all__ = ["Backend", "BackendError", "Clock", "WindowInfo", "WindowNotFound", "create_backend"]


def create_backend(config: Config, clock: Clock | None = None) -> Backend:
    choice = config.backend
    if choice == "auto":
        choice = "windows" if sys.platform == "win32" else "x11"
    if choice == "mock":
        from .mock import MockBackend

        return MockBackend(config, clock or Clock())
    if choice == "windows":
        if sys.platform != "win32":
            raise BackendError("The windows backend only runs on Windows.")
        from .windows import WindowsBackend

        return WindowsBackend(config)
    if choice == "x11":
        if sys.platform == "win32":
            raise BackendError("The x11 backend does not run on Windows.")
        try:
            from .x11 import X11Backend
        except ImportError as exc:
            raise BackendError(str(exc)) from exc
        return X11Backend(config)
    raise BackendError(f"Unknown backend {choice!r}.")
