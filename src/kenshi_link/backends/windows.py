"""Windows backend.

Input goes through SendInput: keys as hardware scancodes (Kenshi polls the keyboard
through DirectInput and ignores virtual-key-only events), the pointer as absolute
moves on the virtual desktop. Capture reads the screen where the window sits, so
Kenshi must run windowed or borderless, not exclusive fullscreen.
"""

from __future__ import annotations

import ctypes
import os
import re
from ctypes import wintypes

from PIL import Image

from ..config import Config
from ..keys import KEYS
from . import _win_structs as ws
from .base import Backend, BackendError, WindowInfo, WindowNotFound

if not hasattr(ctypes, "WinDLL"):  # pragma: no cover - import guard for other platforms
    raise ImportError("the Windows backend can only be loaded on Windows")

SM_XVIRTUALSCREEN, SM_YVIRTUALSCREEN, SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN = 76, 77, 78, 79
SW_RESTORE = 9
VK_PAUSE = 0x13
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def _declare() -> None:
    user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(ws.INPUT), ctypes.c_int)
    user32.SendInput.restype = wintypes.UINT
    user32.GetSystemMetrics.argtypes = (ctypes.c_int,)
    user32.GetSystemMetrics.restype = ctypes.c_int
    user32.GetCursorPos.argtypes = (ctypes.POINTER(wintypes.POINT),)
    user32.GetCursorPos.restype = wintypes.BOOL
    user32.SetCursorPos.argtypes = (ctypes.c_int, ctypes.c_int)
    user32.SetCursorPos.restype = wintypes.BOOL
    user32.EnumWindows.argtypes = (WNDENUMPROC, wintypes.LPARAM)
    user32.EnumWindows.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = (wintypes.HWND,)
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.IsWindow.argtypes = (wintypes.HWND,)
    user32.IsWindow.restype = wintypes.BOOL
    user32.IsIconic.argtypes = (wintypes.HWND,)
    user32.IsIconic.restype = wintypes.BOOL
    user32.GetWindowTextLengthW.argtypes = (wintypes.HWND,)
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
    user32.GetWindowTextW.restype = ctypes.c_int
    user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetClientRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
    user32.GetClientRect.restype = wintypes.BOOL
    user32.ClientToScreen.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.POINT))
    user32.ClientToScreen.restype = wintypes.BOOL
    user32.GetForegroundWindow.argtypes = ()
    user32.GetForegroundWindow.restype = wintypes.HWND
    user32.SetForegroundWindow.argtypes = (wintypes.HWND,)
    user32.SetForegroundWindow.restype = wintypes.BOOL
    user32.BringWindowToTop.argtypes = (wintypes.HWND,)
    user32.BringWindowToTop.restype = wintypes.BOOL
    user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
    user32.ShowWindow.restype = wintypes.BOOL
    user32.AttachThreadInput.argtypes = (wintypes.DWORD, wintypes.DWORD, wintypes.BOOL)
    user32.AttachThreadInput.restype = wintypes.BOOL
    user32.GetAsyncKeyState.argtypes = (ctypes.c_int,)
    user32.GetAsyncKeyState.restype = ctypes.c_short
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.QueryFullProcessImageNameW.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.GetCurrentThreadId.argtypes = ()
    kernel32.GetCurrentThreadId.restype = wintypes.DWORD


_declare()


def _enable_dpi_awareness() -> None:
    """Make window coordinates physical pixels, matching what screen capture returns."""
    try:
        ctypes.WinDLL("shcore").SetProcessDpiAwareness(2)  # per-monitor
        return
    except (OSError, AttributeError):
        pass
    try:
        user32.SetProcessDPIAware()
    except AttributeError:
        pass


def _handle(hwnd: object) -> int:
    return int(hwnd or 0)


class WindowsBackend(Backend):
    name = "windows"

    def __init__(self, config: Config) -> None:
        _enable_dpi_awareness()
        self._config = config
        self._process_re = re.compile(config.process_regex)
        self._title_re = re.compile(config.title_regex)
        self._hwnd = 0
        self._sct = None

    # ---- window -----------------------------------------------------------------

    def _title(self, hwnd: int) -> str:
        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value

    def _exe_name(self, hwnd: int) -> str:
        pid = wintypes.DWORD(0)
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if not pid.value:
            return ""
        process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if not process:
            return ""
        try:
            size = wintypes.DWORD(1024)
            buffer = ctypes.create_unicode_buffer(size.value)
            if not kernel32.QueryFullProcessImageNameW(process, 0, buffer, ctypes.byref(size)):
                return ""
            return os.path.basename(buffer.value.replace("\\", "/"))
        finally:
            kernel32.CloseHandle(process)

    def _client_rect(self, hwnd: int) -> tuple[int, int, int, int]:
        rect = wintypes.RECT()
        if not user32.GetClientRect(hwnd, ctypes.byref(rect)):
            return 0, 0, 0, 0
        origin = wintypes.POINT(0, 0)
        user32.ClientToScreen(hwnd, ctypes.byref(origin))
        return origin.x, origin.y, rect.right - rect.left, rect.bottom - rect.top

    def _find(self) -> int:
        matches: list[tuple[int, int, int]] = []

        def visit(hwnd: object, _lparam: object) -> bool:
            handle = _handle(hwnd)
            if not user32.IsWindowVisible(handle):
                return True
            if not self._process_re.search(self._exe_name(handle)):
                return True
            # The owning program decides; the title only breaks ties between its windows.
            titled = 1 if self._title_re.search(self._title(handle)) else 0
            _, _, width, height = self._client_rect(handle)
            matches.append((titled, width * height, handle))
            return True

        callback = WNDENUMPROC(visit)
        user32.EnumWindows(callback, 0)
        if not matches:
            raise WindowNotFound(
                "No Kenshi window found. Start the game (windowed or borderless) and load a save."
            )
        return max(matches)[2]

    def locate(self) -> WindowInfo:
        hwnd = self._hwnd
        if not hwnd or not user32.IsWindow(hwnd) or not user32.IsWindowVisible(hwnd):
            hwnd = self._hwnd = self._find()
        left, top, width, height = self._client_rect(hwnd)
        if user32.IsIconic(hwnd):
            width = height = 0
        focused = _handle(user32.GetForegroundWindow()) == hwnd
        return WindowInfo(self._title(hwnd), left, top, width, height, focused)

    def focus(self) -> None:
        hwnd = self._hwnd or self._find()
        self._hwnd = hwnd
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, SW_RESTORE)
        if _handle(user32.GetForegroundWindow()) == hwnd:
            return
        user32.SetForegroundWindow(hwnd)
        foreground = _handle(user32.GetForegroundWindow())
        if foreground == hwnd:
            return
        # Windows refuses focus changes from background processes; borrowing the
        # foreground thread's input queue is the sanctioned way around that.
        this_thread = kernel32.GetCurrentThreadId()
        other_thread = user32.GetWindowThreadProcessId(foreground, None) if foreground else 0
        attached = bool(
            other_thread
            and other_thread != this_thread
            and user32.AttachThreadInput(this_thread, other_thread, True)
        )
        try:
            user32.BringWindowToTop(hwnd)
            user32.SetForegroundWindow(hwnd)
        finally:
            if attached:
                user32.AttachThreadInput(this_thread, other_thread, False)

    # ---- capture ----------------------------------------------------------------

    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        if self._sct is None:
            import mss

            self._sct = (getattr(mss, "MSS", None) or mss.mss)()  # mss >= 10 renamed the class
        shot = self._sct.grab({"left": left, "top": top, "width": width, "height": height})
        return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")

    # ---- input ------------------------------------------------------------------

    def _send(self, event: ws.INPUT) -> None:
        sent = user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(ws.INPUT))
        if sent != 1:
            raise BackendError(
                "Windows rejected the input (SendInput returned 0). This usually means Kenshi is "
                "running as administrator and this program is not: start both at the same level."
            )

    def _virtual_screen(self) -> tuple[int, int, int, int]:
        return (
            user32.GetSystemMetrics(SM_XVIRTUALSCREEN),
            user32.GetSystemMetrics(SM_YVIRTUALSCREEN),
            user32.GetSystemMetrics(SM_CXVIRTUALSCREEN),
            user32.GetSystemMetrics(SM_CYVIRTUALSCREEN),
        )

    def move(self, x: int, y: int) -> None:
        nx, ny = ws.absolute_coords(x, y, self._virtual_screen())
        flags = ws.MOUSEEVENTF_MOVE | ws.MOUSEEVENTF_ABSOLUTE | ws.MOUSEEVENTF_VIRTUALDESK
        self._send(ws.mouse_input(nx, ny, 0, flags))
        cx, cy = self.cursor()
        if abs(cx - x) > 1 or abs(cy - y) > 1:
            # Rounding in the 0..65535 mapping can land a pixel or two off on big desktops.
            user32.SetCursorPos(x, y)
            self._send(ws.mouse_input(0, 0, 0, ws.MOUSEEVENTF_MOVE))

    def button(self, button: str, down: bool) -> None:
        self._send(ws.mouse_input(0, 0, 0, ws.BUTTON_FLAGS[(button, down)]))

    def wheel(self, clicks: int) -> None:
        self._send(ws.mouse_input(0, 0, clicks * ws.WHEEL_DELTA, ws.MOUSEEVENTF_WHEEL))

    def key(self, key: str, down: bool) -> None:
        definition = KEYS[key]
        self._send(ws.key_input(definition.scancode, definition.extended, down, definition.vk))

    def cursor(self) -> tuple[int, int]:
        point = wintypes.POINT()
        if not user32.GetCursorPos(ctypes.byref(point)):
            raise BackendError("could not read the pointer position")
        return point.x, point.y

    def panic_pressed(self) -> bool:
        return bool(user32.GetAsyncKeyState(VK_PAUSE) & 0x8000)

    def close(self) -> None:
        if self._sct is not None:
            self._sct.close()
            self._sct = None
