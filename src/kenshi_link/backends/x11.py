"""Linux backend for Kenshi under Proton/Wine on X11 (or XWayland).

Input is injected with the XTEST extension, which Wine turns into ordinary
Windows keyboard and mouse input for the game.
"""

from __future__ import annotations

import re

from PIL import Image

from ..config import Config
from ..keys import KEYS
from .base import Backend, BackendError, WindowInfo, WindowNotFound

try:
    from Xlib import X, XK, display, error
    from Xlib.ext import xtest
    from Xlib.protocol import event as xevent
except ImportError as exc:  # pragma: no cover - dependency guard
    raise ImportError("the X11 backend needs python-xlib (pip install python-xlib)") from exc

_BUTTON_NUMBERS = {"left": 1, "middle": 2, "right": 3}


class X11Backend(Backend):
    name = "x11"

    def __init__(self, config: Config) -> None:
        self._config = config
        self._class_re = re.compile(config.x11_class_regex)
        self._title_re = re.compile(config.title_regex)
        try:
            self._display = display.Display()
        except Exception as exc:
            raise BackendError(
                f"Cannot open the X display ({exc}). Is DISPLAY set and is this an X11/XWayland session?"
            ) from exc
        if not self._display.query_extension("XTEST").present:
            raise BackendError("The X server has no XTEST extension, so input cannot be injected.")
        self._screen = self._display.screen()
        self._root = self._screen.root
        self._window = None
        self._sct = None
        self._keycodes: dict[str, int] = {}

    # ---- window -----------------------------------------------------------------

    def _atom(self, name: str) -> int:
        return self._display.intern_atom(name)

    def _property(self, window, name: str):
        try:
            return window.get_full_property(self._atom(name), X.AnyPropertyType)
        except error.XError:
            return None

    def _title(self, window) -> str:
        prop = self._property(window, "_NET_WM_NAME")
        if prop is not None and prop.value:
            value = prop.value
            return value.decode("utf-8", "replace") if isinstance(value, bytes) else str(value)
        try:
            return window.get_wm_name() or ""
        except error.XError:
            return ""

    def _all_windows(self) -> list:
        clients = self._property(self._root, "_NET_CLIENT_LIST")
        if clients is not None and len(clients.value):
            return [self._display.create_resource_object("window", wid) for wid in clients.value]
        found: list = []

        def walk(window, depth: int) -> None:
            try:
                children = window.query_tree().children
            except error.XError:
                return
            for child in children:
                found.append(child)
                if depth < 3:
                    walk(child, depth + 1)

        walk(self._root, 0)
        return found

    def _matches(self, window) -> bool:
        try:
            wm_class = window.get_wm_class()
            attributes = window.get_attributes()
        except error.XError:
            return False
        if not wm_class or attributes.map_state != X.IsViewable:
            return False
        return any(self._class_re.search(part or "") for part in wm_class)

    def _find(self):
        best = None
        best_score = (-1, -1)
        for window in self._all_windows():
            if not self._matches(window):
                continue
            try:
                geometry = window.get_geometry()
            except error.XError:
                continue
            titled = 1 if self._title_re.search(self._title(window)) else 0
            score = (titled, geometry.width * geometry.height)
            if score > best_score:
                best, best_score = window, score
        if best is None:
            raise WindowNotFound(
                "No Kenshi window found on this X display. Start the game (windowed or borderless) "
                "and load a save."
            )
        return best

    def _is_focused(self, window) -> bool:
        active = self._property(self._root, "_NET_ACTIVE_WINDOW")
        if active is not None and len(active.value) and active.value[0]:
            return int(active.value[0]) == window.id
        focus = self._display.get_input_focus().focus
        if isinstance(focus, int):
            if focus == X.PointerRoot:
                # No window manager: keys go to whatever is under the pointer.
                pointer = self._root.query_pointer()
                geometry = window.get_geometry()
                origin = self._root.translate_coords(window, 0, 0)
                return (
                    origin.x <= pointer.root_x < origin.x + geometry.width
                    and origin.y <= pointer.root_y < origin.y + geometry.height
                )
            return False
        current = focus
        for _ in range(16):  # the focus may be a child of the game's top-level window
            if current.id == window.id:
                return True
            try:
                parent = current.query_tree().parent
            except error.XError:
                return False
            if not parent or isinstance(parent, int) or parent.id == self._root.id:
                return False
            current = parent
        return False

    def locate(self) -> WindowInfo:
        try:
            if self._window is None or not self._matches(self._window):
                self._window = self._find()
            window = self._window
            geometry = window.get_geometry()
            origin = self._root.translate_coords(window, 0, 0)
            return WindowInfo(
                title=self._title(window),
                left=origin.x,
                top=origin.y,
                width=geometry.width,
                height=geometry.height,
                focused=self._is_focused(window),
            )
        except error.XError as exc:
            self._window = None
            raise WindowNotFound(f"The Kenshi window went away ({exc}).") from exc

    def focus(self) -> None:
        window = self._window or self._find()
        self._window = window
        try:
            if self._property(self._root, "_NET_SUPPORTING_WM_CHECK") is not None:
                message = xevent.ClientMessage(
                    window=window,
                    client_type=self._atom("_NET_ACTIVE_WINDOW"),
                    data=(32, [2, X.CurrentTime, 0, 0, 0]),  # 2 = request comes from a pager/tool
                )
                mask = X.SubstructureRedirectMask | X.SubstructureNotifyMask
                self._root.send_event(message, event_mask=mask)
            window.configure(stack_mode=X.Above)
            window.set_input_focus(X.RevertToParent, X.CurrentTime)
            self._display.sync()
        except error.XError as exc:
            raise BackendError(f"Could not focus the Kenshi window ({exc}).") from exc

    def screen_rect(self) -> tuple[int, int, int, int]:
        return (0, 0, self._screen.width_in_pixels, self._screen.height_in_pixels)

    # ---- capture ----------------------------------------------------------------

    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        screen_w, screen_h = self._screen.width_in_pixels, self._screen.height_in_pixels
        if left < 0 or top < 0 or left + width > screen_w or top + height > screen_h:
            raise BackendError(
                "The Kenshi window is partly off-screen, so it cannot be captured. "
                "Move it fully onto the screen."
            )
        try:
            if self._sct is None:
                import mss

                self._sct = (getattr(mss, "MSS", None) or mss.mss)()  # mss >= 10 renamed the class
            shot = self._sct.grab({"left": left, "top": top, "width": width, "height": height})
            return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        except Exception as exc:  # mss raises its own error type
            raise BackendError(f"The screen could not be captured ({exc}).") from exc

    # ---- input ------------------------------------------------------------------

    def _fake(self, event_type: int, detail: int = 0, **kwargs) -> None:
        xtest.fake_input(self._display, event_type, detail, **kwargs)
        self._display.sync()

    def move(self, x: int, y: int) -> None:
        self._fake(X.MotionNotify, x=x, y=y)

    def button(self, button: str, down: bool) -> None:
        self._fake(X.ButtonPress if down else X.ButtonRelease, _BUTTON_NUMBERS[button])

    def wheel(self, clicks: int) -> None:
        number = 4 if clicks > 0 else 5
        for _ in range(abs(clicks)):
            self._fake(X.ButtonPress, number)
            self._fake(X.ButtonRelease, number)

    def _keycode(self, key: str) -> int:
        if key not in self._keycodes:
            keysym = XK.string_to_keysym(KEYS[key].keysym)
            keycode = self._display.keysym_to_keycode(keysym) if keysym else 0
            if not keycode:
                raise BackendError(f"The '{key}' key is not on this X keyboard layout.")
            self._keycodes[key] = keycode
        return self._keycodes[key]

    def key(self, key: str, down: bool) -> None:
        self._fake(X.KeyPress if down else X.KeyRelease, self._keycode(key))

    def cursor(self) -> tuple[int, int]:
        pointer = self._root.query_pointer()
        return pointer.root_x, pointer.root_y

    def panic_pressed(self) -> bool:
        keycode = self._display.keysym_to_keycode(XK.string_to_keysym("Pause"))
        if not keycode:
            return False
        keymap = self._display.query_keymap()
        return bool(keymap[keycode // 8] & (1 << (keycode % 8)))

    def close(self) -> None:
        if self._sct is not None:
            self._sct.close()
            self._sct = None
        self._display.close()
