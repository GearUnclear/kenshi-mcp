"""A bare Win32 window that stands in for Kenshi and logs the input it receives.

Usage: python win_window.py EVENT_LOG.jsonl
Borderless 800x600 window at (100, 50): blue, with a red 100x100 square top-left.
"""

import ctypes
import json
import sys
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

LRESULT = ctypes.c_ssize_t
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

WS_POPUP, WS_VISIBLE = 0x80000000, 0x10000000
WM_DESTROY, WM_PAINT = 0x0002, 0x000F
WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP = 0x0100, 0x0101, 0x0104, 0x0105
WM_MOUSEMOVE, WM_MOUSEWHEEL = 0x0200, 0x020A
BUTTON_MESSAGES = {
    0x0201: ("left", True), 0x0202: ("left", False),
    0x0204: ("right", True), 0x0205: ("right", False),
    0x0207: ("middle", True), 0x0208: ("middle", False),
}
MK_LBUTTON, MK_SHIFT = 0x0001, 0x0004
WIDTH, HEIGHT, LEFT, TOP = 800, 600, 100, 50


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int), ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR), ("lpszClassName", wintypes.LPCWSTR),
    ]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC), ("fErase", wintypes.BOOL), ("rcPaint", wintypes.RECT),
        ("fRestore", wintypes.BOOL), ("fIncUpdate", wintypes.BOOL), ("rgbReserved", ctypes.c_byte * 32),
    ]


user32.DefWindowProcW.argtypes = (wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
user32.DefWindowProcW.restype = LRESULT
user32.CreateWindowExW.argtypes = (
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HANDLE, wintypes.HINSTANCE, wintypes.LPVOID,
)
user32.CreateWindowExW.restype = wintypes.HWND
user32.RegisterClassW.argtypes = (ctypes.POINTER(WNDCLASSW),)
user32.BeginPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PAINTSTRUCT))
user32.BeginPaint.restype = wintypes.HDC
user32.EndPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PAINTSTRUCT))
user32.FillRect.argtypes = (wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.HANDLE)
user32.GetMessageW.argtypes = (ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT)
user32.TranslateMessage.argtypes = (ctypes.POINTER(wintypes.MSG),)
user32.DispatchMessageW.argtypes = (ctypes.POINTER(wintypes.MSG),)
user32.SetForegroundWindow.argtypes = (wintypes.HWND,)
user32.UpdateWindow.argtypes = (wintypes.HWND,)
gdi32.CreateSolidBrush.argtypes = (wintypes.DWORD,)
gdi32.CreateSolidBrush.restype = wintypes.HANDLE
kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE


def _signed16(value: int) -> int:
    value &= 0xFFFF
    return value - 0x10000 if value & 0x8000 else value


def main() -> None:
    log = open(sys.argv[1], "a", buffering=1)

    def record(**fields) -> None:
        log.write(json.dumps(fields) + "\n")

    blue = gdi32.CreateSolidBrush(0x00804020)  # COLORREF is 0x00BBGGRR
    red = gdi32.CreateSolidBrush(0x000000FF)

    def window_proc(hwnd, message, wparam, lparam):
        if message == WM_PAINT:
            paint = PAINTSTRUCT()
            hdc = user32.BeginPaint(hwnd, ctypes.byref(paint))
            user32.FillRect(hdc, ctypes.byref(wintypes.RECT(0, 0, WIDTH, HEIGHT)), blue)
            user32.FillRect(hdc, ctypes.byref(wintypes.RECT(0, 0, 100, 100)), red)
            user32.EndPaint(hwnd, ctypes.byref(paint))
            return 0
        if message in (WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP):
            record(
                type="key", down=message in (WM_KEYDOWN, WM_SYSKEYDOWN), vk=int(wparam),
                scancode=(lparam >> 16) & 0xFF, extended=bool((lparam >> 24) & 1),
            )
            return 0
        if message in BUTTON_MESSAGES:
            button, down = BUTTON_MESSAGES[message]
            record(
                type="button", button=button, down=down, x=_signed16(lparam), y=_signed16(lparam >> 16),
                shift=bool(wparam & MK_SHIFT),
            )
            return 0
        if message == WM_MOUSEMOVE:
            record(type="motion", x=_signed16(lparam), y=_signed16(lparam >> 16),
                   left_down=bool(wparam & MK_LBUTTON))
            return 0
        if message == WM_MOUSEWHEEL:
            record(type="wheel", delta=_signed16(wparam >> 16))
            return 0
        if message == WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, message, wparam, lparam)

    proc = WNDPROC(window_proc)
    instance = kernel32.GetModuleHandleW(None)
    window_class = WNDCLASSW()
    window_class.lpfnWndProc = proc
    window_class.hInstance = instance
    window_class.lpszClassName = "KenshiLinkTestWindow"
    if not user32.RegisterClassW(ctypes.byref(window_class)):
        raise ctypes.WinError(ctypes.get_last_error())
    hwnd = user32.CreateWindowExW(
        0, "KenshiLinkTestWindow", "Kenshi 1.0.64 - x64 (test window)", WS_POPUP | WS_VISIBLE,
        LEFT, TOP, WIDTH, HEIGHT, None, None, instance, None,
    )
    if not hwnd:
        raise ctypes.WinError(ctypes.get_last_error())
    user32.UpdateWindow(hwnd)
    user32.SetForegroundWindow(hwnd)
    record(type="ready")

    message = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
        user32.TranslateMessage(ctypes.byref(message))
        user32.DispatchMessageW(ctypes.byref(message))


if __name__ == "__main__":
    main()
