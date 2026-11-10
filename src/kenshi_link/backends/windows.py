"""Windows backend.

Input goes through SendInput: keys as hardware scancodes (Kenshi polls the keyboard
through DirectInput and ignores virtual-key-only events), the pointer as absolute
moves on the virtual desktop. Capture reads the screen where the window sits, so
Kenshi must run windowed or borderless, not exclusive fullscreen.
"""

from __future__ import annotations

import ctypes
import logging
import os
import re
import threading
from collections.abc import Callable
from ctypes import wintypes

from PIL import Image

from ..config import Config
from ..keys import KEYS, BlockedInput, char_to_key, layout_strokes
from . import _win_structs as ws
from .base import Backend, BackendError, DesktopUnavailable, WindowInfo, WindowNotFound

if not hasattr(ctypes, "WinDLL"):  # pragma: no cover - import guard for other platforms
    raise ImportError("the Windows backend can only be loaded on Windows")

log = logging.getLogger("kenshi_link")

SM_XVIRTUALSCREEN, SM_YVIRTUALSCREEN, SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN = 76, 77, 78, 79
SW_RESTORE = 9
GA_ROOT = 2
VK_CANCEL, VK_PAUSE, VK_CAPITAL = 0x03, 0x13, 0x14
MOD_CONTROL, MOD_NOREPEAT = 0x0002, 0x4000
WM_QUIT, WM_HOTKEY = 0x0012, 0x0312
MAPVK_VK_TO_VSC, MAPVK_VK_TO_CHAR = 0, 2
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
TOKEN_QUERY = 0x0008
TOKEN_ELEVATION = 20  # the TokenElevation information class
DESKTOP_READOBJECTS = 0x0001
UOI_NAME = 2
ERROR_ACCESS_DENIED = 5

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
MONITORENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL, wintypes.HANDLE, wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM
)
HKL = ctypes.c_void_p

NOT_RESPONDING = (
    "Kenshi is not responding right now: it is probably loading or saving. Nothing was sent. "
    "Wait a few seconds and observe again."
)
DESKTOP_GONE = (
    "The Windows desktop is not available: the screen is locked, or a security prompt (UAC, "
    "Ctrl+Alt+Del), the screen saver or a disconnected remote session is in front. The game "
    "cannot be seen and no input can reach it until the operator is back at the desktop"
)


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
    user32.IsHungAppWindow.argtypes = (wintypes.HWND,)
    user32.IsHungAppWindow.restype = wintypes.BOOL
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
    user32.ShowWindowAsync.argtypes = (wintypes.HWND, ctypes.c_int)
    user32.ShowWindowAsync.restype = wintypes.BOOL
    user32.AttachThreadInput.argtypes = (wintypes.DWORD, wintypes.DWORD, wintypes.BOOL)
    user32.AttachThreadInput.restype = wintypes.BOOL
    user32.WindowFromPoint.argtypes = (wintypes.POINT,)
    user32.WindowFromPoint.restype = wintypes.HWND
    user32.GetAncestor.argtypes = (wintypes.HWND, wintypes.UINT)
    user32.GetAncestor.restype = wintypes.HWND
    user32.EnumDisplayMonitors.argtypes = (wintypes.HDC, ctypes.c_void_p, MONITORENUMPROC, wintypes.LPARAM)
    user32.EnumDisplayMonitors.restype = wintypes.BOOL
    user32.GetAsyncKeyState.argtypes = (ctypes.c_int,)
    user32.GetAsyncKeyState.restype = ctypes.c_short
    user32.GetKeyState.argtypes = (ctypes.c_int,)
    user32.GetKeyState.restype = ctypes.c_short
    user32.GetKeyboardLayout.argtypes = (wintypes.DWORD,)
    user32.GetKeyboardLayout.restype = HKL
    user32.VkKeyScanExW.argtypes = (wintypes.WCHAR, HKL)
    user32.VkKeyScanExW.restype = ctypes.c_short
    user32.MapVirtualKeyExW.argtypes = (wintypes.UINT, wintypes.UINT, HKL)
    user32.MapVirtualKeyExW.restype = wintypes.UINT
    user32.RegisterHotKey.argtypes = (wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT)
    user32.RegisterHotKey.restype = wintypes.BOOL
    user32.UnregisterHotKey.argtypes = (wintypes.HWND, ctypes.c_int)
    user32.UnregisterHotKey.restype = wintypes.BOOL
    user32.GetMessageW.argtypes = (ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT)
    user32.GetMessageW.restype = ctypes.c_int
    user32.PeekMessageW.argtypes = (
        ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT,
    )
    user32.PeekMessageW.restype = wintypes.BOOL
    user32.PostThreadMessageW.argtypes = (wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
    user32.PostThreadMessageW.restype = wintypes.BOOL
    user32.OpenInputDesktop.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    user32.OpenInputDesktop.restype = wintypes.HANDLE
    user32.GetThreadDesktop.argtypes = (wintypes.DWORD,)
    user32.GetThreadDesktop.restype = wintypes.HANDLE
    user32.CloseDesktop.argtypes = (wintypes.HANDLE,)
    user32.CloseDesktop.restype = wintypes.BOOL
    user32.GetUserObjectInformationW.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    user32.GetUserObjectInformationW.restype = wintypes.BOOL
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.GetCurrentProcess.argtypes = ()
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
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
    advapi32.OpenProcessToken.argtypes = (wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE))
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.GetTokenInformation.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    advapi32.GetTokenInformation.restype = wintypes.BOOL


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


def _elevated(process: object) -> bool | None:
    """Whether a process runs as administrator.

    None means Windows refused to let us look, which is what it does to a program asking
    about a more privileged one. Any other failure (the process has just exited, say) is
    no evidence either way and counts as "no".
    """
    token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(process, TOKEN_QUERY, ctypes.byref(token)):
        return None if ctypes.get_last_error() == ERROR_ACCESS_DENIED else False
    try:
        elevated, size = wintypes.DWORD(0), wintypes.DWORD(0)
        if not advapi32.GetTokenInformation(
            token, TOKEN_ELEVATION, ctypes.byref(elevated), ctypes.sizeof(elevated), ctypes.byref(size)
        ):
            return False
        return bool(elevated.value)
    finally:
        kernel32.CloseHandle(token)


def _process_elevated(pid: int) -> bool | None:
    """As _elevated, for another process by id."""
    process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not process:
        return None if ctypes.get_last_error() == ERROR_ACCESS_DENIED else False
    try:
        return _elevated(process)
    finally:
        kernel32.CloseHandle(process)


def _object_name(handle: object) -> str | None:
    buffer = ctypes.create_unicode_buffer(256)
    needed = wintypes.DWORD(0)
    if not handle or not user32.GetUserObjectInformationW(
        handle, UOI_NAME, buffer, ctypes.sizeof(buffer), ctypes.byref(needed)
    ):
        return None
    return buffer.value


def _desktop_available() -> bool:
    """Whether the desktop receiving input is the one this program lives on.

    While the screen is locked, or a UAC prompt or the screen saver is up, input goes to
    another desktop: GetCursorPos fails, SendInput inserts nothing and screen capture
    fails or shows nothing useful.
    """
    desktop = user32.OpenInputDesktop(0, False, DESKTOP_READOBJECTS)
    if not desktop:
        return False
    try:
        active = _object_name(desktop)
        ours = _object_name(user32.GetThreadDesktop(kernel32.GetCurrentThreadId()))
    finally:
        user32.CloseDesktop(desktop)
    return active is None or ours is None or active.lower() == ours.lower()


class _PanicHotkey(threading.Thread):
    """Registers Pause/Break (and Ctrl+Break) as system hotkeys and reports each press.

    GetAsyncKeyState only says whether the key is down at the instant it is asked, so a
    tap between two checks is lost. A hotkey is delivered as a message however briefly the
    key was pressed, whichever program has focus. Hotkeys belong to the thread that
    registered them, hence a thread of its own with a message loop.
    """

    def __init__(self, callback: Callable[[], None]) -> None:
        super().__init__(name="kenshi-link-panic-key", daemon=True)
        self._callback = callback
        self._thread_id = 0
        self.ready = threading.Event()
        self.registered = False
        self.error = 0

    def run(self) -> None:
        self._thread_id = kernel32.GetCurrentThreadId()
        message = wintypes.MSG()
        # Asking for a message first makes sure this thread has its message queue, which is
        # where the hotkey is delivered, before anything is registered against it.
        user32.PeekMessageW(ctypes.byref(message), None, 0, 0, 0)
        self.registered = bool(user32.RegisterHotKey(None, 1, MOD_NOREPEAT, VK_PAUSE))
        self.error = 0 if self.registered else ctypes.get_last_error()
        # With Ctrl held, the Pause key produces Break instead, which is a different key code.
        also = bool(user32.RegisterHotKey(None, 2, MOD_NOREPEAT | MOD_CONTROL, VK_CANCEL))
        self.ready.set()
        if not (self.registered or also):
            return
        while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
            if message.message == WM_HOTKEY:
                try:
                    self._callback()
                except Exception:  # the loop must survive: it is the operator's stop button
                    log.exception("could not record the Pause/Break press")
        user32.UnregisterHotKey(None, 1)
        user32.UnregisterHotKey(None, 2)

    def stop(self) -> None:
        if self.is_alive() and self._thread_id:
            user32.PostThreadMessageW(self._thread_id, WM_QUIT, 0, 0)
            self.join(timeout=0.5)  # it is a daemon thread: not worth holding up an exit for


class WindowsBackend(Backend):
    name = "windows"

    def __init__(self, config: Config) -> None:
        _enable_dpi_awareness()
        self._config = config
        self._process_re = re.compile(config.process_regex)
        self._title_re = re.compile(config.title_regex)
        self._hwnd = 0
        self._pid = 0  # the process that owned _hwnd when it was found
        self._sct = None
        self._hotkey: _PanicHotkey | None = None
        self._focus_error = ""
        self._monitors: tuple[tuple[int, int, int, int], tuple[int, int]] | None = None
        self.corrections = 0  # times the pointer had to be put right after a move (see place)

    # ---- window -----------------------------------------------------------------

    def _title(self, hwnd: int) -> str:
        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value

    def _owner(self, hwnd: int) -> tuple[int, int]:
        """(thread id, process id) of a window."""
        pid = wintypes.DWORD(0)
        thread = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return thread, pid.value

    def _exe_name(self, hwnd: int) -> str:
        pid = self._owner(hwnd)[1]
        if not pid:
            return ""
        process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
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

    def _adopt(self, hwnd: int) -> int:
        """Take a newly found window as the game, unless input could never reach it."""
        pid = self._owner(hwnd)[1]
        problem = ws.elevation_problem(_elevated(kernel32.GetCurrentProcess()), _process_elevated(pid))
        if problem:
            raise BackendError(problem)
        self._hwnd, self._pid = hwnd, pid
        return hwnd

    def _game_window(self) -> int:
        """The game window's handle, looked up again if the one we had is no longer it."""
        hwnd = self._hwnd
        # Windows reuses handle values, so a handle that is still a window is not enough:
        # it must also still belong to the process it was found in.
        if hwnd and not (user32.IsWindow(hwnd) and self._owner(hwnd)[1] == self._pid):
            hwnd = self._hwnd = 0
        if hwnd and user32.IsHungAppWindow(hwnd):
            # Checked before visibility: Windows may put a stand-in "ghost" window in
            # front of one that has stopped answering.
            raise BackendError(NOT_RESPONDING)
        if not hwnd or not user32.IsWindowVisible(hwnd):
            self._hwnd = 0
            hwnd = self._adopt(self._find())
            if user32.IsHungAppWindow(hwnd):
                raise BackendError(NOT_RESPONDING)
        return hwnd

    def _require_desktop(self) -> None:
        if not _desktop_available():
            raise DesktopUnavailable(DESKTOP_GONE)

    def locate(self) -> WindowInfo:
        # Checked before anything is tried, so that a locked PC is reported as that. Being
        # wrong here would stop everything, so two signs must agree: input is going to
        # another desktop, and Windows will not say where the pointer is.
        if not _desktop_available() and not user32.GetCursorPos(ctypes.byref(wintypes.POINT())):
            raise DesktopUnavailable(DESKTOP_GONE)
        hwnd = self._game_window()
        left, top, width, height = self._client_rect(hwnd)
        if user32.IsIconic(hwnd):
            width = height = 0
        focused = _handle(user32.GetForegroundWindow()) == hwnd
        return WindowInfo(self._title(hwnd), left, top, width, height, focused)

    def focus(self) -> None:
        self._focus_error = ""
        hwnd = self._game_window()
        if user32.IsIconic(hwnd):
            # The Async form only posts the request, so a busy game cannot hold us up.
            user32.ShowWindowAsync(hwnd, SW_RESTORE)
        if _handle(user32.GetForegroundWindow()) == hwnd:
            return
        user32.SetForegroundWindow(hwnd)
        foreground = _handle(user32.GetForegroundWindow())
        if foreground == hwnd:
            return
        # Windows refuses focus changes from background processes. Sharing an input queue
        # with the thread that has the foreground is the sanctioned way around that. A
        # classic console window reports a thread with no message queue, which cannot be
        # shared with, so the game's own thread is tried as well.
        this_thread = kernel32.GetCurrentThreadId()
        foreground_thread = self._owner(foreground)[0] if foreground else 0
        for other in dict.fromkeys((foreground_thread, self._owner(hwnd)[0])):
            if not other or other == this_thread:
                continue
            if not user32.AttachThreadInput(this_thread, other, True):
                continue
            try:
                user32.BringWindowToTop(hwnd)
                user32.SetForegroundWindow(hwnd)
            finally:
                user32.AttachThreadInput(this_thread, other, False)
            if _handle(user32.GetForegroundWindow()) == hwnd:
                return
        self._focus_error = (
            f"Windows refused to change the front window (error {ctypes.get_last_error()}): it only "
            "lets the program the user last worked in do that."
        )

    def focus_error(self) -> str:
        return self._focus_error

    def pointer_on_window(self) -> bool:
        under = _handle(user32.WindowFromPoint(wintypes.POINT(*self.cursor())))
        if not under or not self._hwnd:
            return False
        if _handle(user32.GetAncestor(under, GA_ROOT)) == self._hwnd:
            return True
        return self._owner(under)[1] == self._pid  # another window of the game's own

    def screen_rect(self) -> tuple[int, int, int, int]:
        return self._virtual_screen()

    def failsafe_corner(self) -> tuple[int, int]:
        virtual = self._virtual_screen()
        if self._monitors is None or self._monitors[0] != virtual:
            rects: list[tuple[int, int, int, int]] = []

            def visit(_monitor: object, _dc: object, rect: object, _lparam: object) -> bool:
                found = rect.contents
                rects.append((found.left, found.top, found.right, found.bottom))
                return True

            user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(visit), 0)
            self._monitors = (virtual, ws.top_left_corner(rects))
        return self._monitors[1]

    # ---- capture ----------------------------------------------------------------

    def capture(self, left: int, top: int, width: int, height: int) -> Image.Image:
        try:
            if self._sct is None:
                import mss

                self._sct = (getattr(mss, "MSS", None) or mss.mss)()  # mss >= 10 renamed the class
            shot = self._sct.grab({"left": left, "top": top, "width": width, "height": height})
            return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        except Exception as exc:  # mss raises its own error type for any failed GDI call
            self._drop_capture()  # its device contexts may be stale: start afresh next time
            self._require_desktop()
            raise BackendError(f"The screen could not be captured ({exc}).") from exc

    def _drop_capture(self) -> None:
        sct, self._sct = self._sct, None
        if sct is not None:
            try:
                sct.close()
            except Exception:
                pass

    # ---- input ------------------------------------------------------------------

    def _send(self, event: ws.INPUT) -> None:
        if user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(ws.INPUT)) == 1:
            return
        code = ctypes.get_last_error()
        self._require_desktop()
        # Not the administrator mismatch: Windows reports success for input it then drops
        # for that reason, which is why locate() checks for it beforehand.
        raise BackendError(
            f"Windows did not accept the input (SendInput inserted nothing, error {code}). Another "
            "program is blocking input for the moment, for example security or remote-control "
            "software. Nothing more was sent."
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

    def place(self, x: int, y: int) -> None:
        # SetCursorPos puts the pointer on an exact pixel, but reports no movement to
        # DirectInput, so a game that reads the mouse that way would go on using the
        # position it had. One pixel aside and back is movement it does report; when it
        # then asks where the pointer is, it finds the position set here.
        self.corrections += 1
        virtual = self._virtual_screen()
        step = 1 if self.cursor()[0] + 1 < virtual[0] + virtual[2] else -1
        self._send(ws.mouse_input(step, 0, 0, ws.MOUSEEVENTF_MOVE))
        self._send(ws.mouse_input(-step, 0, 0, ws.MOUSEEVENTF_MOVE))
        user32.SetCursorPos(x, y)

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
            code = ctypes.get_last_error()
            self._require_desktop()
            raise BackendError(f"Windows would not report the pointer position (error {code}).")
        return point.x, point.y

    # ---- keyboard layout --------------------------------------------------------

    def _layout_lookup(self) -> Callable[[str], tuple[int, int, bool] | None]:
        """Where the game's keyboard layout puts a character (see keys.layout_strokes)."""
        game_thread = self._owner(self._hwnd)[0] if self._hwnd else 0
        layout = user32.GetKeyboardLayout(game_thread) or user32.GetKeyboardLayout(0)

        def lookup(char: str) -> tuple[int, int, bool] | None:
            found = user32.VkKeyScanExW(char, layout)
            if found == -1:
                return None
            vk, modifiers = found & 0xFF, (found >> 8) & 0xFF
            scancode = user32.MapVirtualKeyExW(vk, MAPVK_VK_TO_VSC, layout)
            dead = bool(user32.MapVirtualKeyExW(vk, MAPVK_VK_TO_CHAR, layout) & 0x80000000)
            return scancode, modifiers, dead

        return lookup

    def typing_keys(self, text: str) -> list[tuple[str, bool]]:
        return layout_strokes(text, self._layout_lookup())

    def caps_lock(self) -> bool:
        # A thread's view of the toggle keys is brought up to date when it looks at its
        # message queue, which this thread otherwise never does.
        user32.PeekMessageW(ctypes.byref(wintypes.MSG()), None, 0, 0, 0)
        return bool(user32.GetKeyState(VK_CAPITAL) & 1)

    # ---- operator stop ----------------------------------------------------------

    def panic_pressed(self) -> bool:
        return bool(user32.GetAsyncKeyState(VK_PAUSE) & 0x8000)

    def watch_panic(self, callback: Callable[[], None]) -> None:
        if self._hotkey is None:
            self._hotkey = _PanicHotkey(callback)
            self._hotkey.start()
            self._hotkey.ready.wait(timeout=2)

    def notes(self) -> list[str]:
        lines = []
        if self._hotkey is not None:
            if self._hotkey.registered:
                lines.append("stop key: Pause/Break is registered as a hotkey, so a tap is enough")
            else:
                lines.append(
                    f"stop key: Pause/Break could not be registered as a hotkey (error {self._hotkey.error}; "
                    "another program, or another kenshi-link, has it). In this program it only works "
                    "while held down."
                )
        sample = "abcdefghijklmnopqrstuvwxyz0123456789"
        try:
            us_layout = self.typing_keys(sample) == [char_to_key(char) for char in sample]
        except BlockedInput:
            us_layout = False
        if not us_layout:
            lines.append(
                "keyboard layout: not a US layout. Key names in [keymap] stand for the keys in the US "
                "positions, whatever is printed on them; type_text follows your layout."
            )
        return lines

    def close(self) -> None:
        if self._hotkey is not None:
            self._hotkey.stop()
            self._hotkey = None
        self._drop_capture()
