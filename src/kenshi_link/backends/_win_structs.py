"""Win32 input structures, declared with fixed-width types.

Kept apart from windows.py so the layout can be checked on any platform: on 64-bit
Windows INPUT must be exactly 40 bytes or SendInput silently rejects it.
"""

from __future__ import annotations

import ctypes

LONG = ctypes.c_int32
DWORD = ctypes.c_uint32
WORD = ctypes.c_uint16
ULONG_PTR = ctypes.c_size_t

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_ABSOLUTE = 0x8000
WHEEL_DELTA = 120

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

BUTTON_FLAGS = {
    ("left", True): MOUSEEVENTF_LEFTDOWN,
    ("left", False): MOUSEEVENTF_LEFTUP,
    ("right", True): MOUSEEVENTF_RIGHTDOWN,
    ("right", False): MOUSEEVENTF_RIGHTUP,
    ("middle", True): MOUSEEVENTF_MIDDLEDOWN,
    ("middle", False): MOUSEEVENTF_MIDDLEUP,
}


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", DWORD), ("wParamL", WORD), ("wParamH", WORD)]


class _INPUTUNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", DWORD), ("u", _INPUTUNION)]


def mouse_input(dx: int, dy: int, data: int, flags: int) -> INPUT:
    event = INPUT()
    event.type = INPUT_MOUSE
    event.mi = MOUSEINPUT(dx, dy, data & 0xFFFFFFFF, flags, 0, 0)
    return event


def key_input(scancode: int, extended: bool, down: bool, vk: int = 0) -> INPUT:
    """A key event identified by scancode.

    With KEYEVENTF_SCANCODE Windows ignores wVk and derives the virtual key from the
    scancode itself. Wine (9.0 at least) does not: there a scancode-only event never
    updates the key state, so modifiers would not register. Filling wVk as well is
    harmless on Windows and makes the same event work on both.
    """
    flags = KEYEVENTF_SCANCODE
    if extended:
        flags |= KEYEVENTF_EXTENDEDKEY
    if not down:
        flags |= KEYEVENTF_KEYUP
    event = INPUT()
    event.type = INPUT_KEYBOARD
    event.ki = KEYBDINPUT(vk, scancode, flags, 0, 0)
    return event


def absolute_coords(x: int, y: int, virtual: tuple[int, int, int, int]) -> tuple[int, int]:
    """Map a screen pixel to SendInput's 0..65535 space across the whole virtual desktop.

    Microsoft does not document how Windows rounds on the way back. AutoHotkey's source
    records it as pixel = value * size // 65536 (Wine does the same), under which the
    obvious pixel * 65535 / (size - 1) lands one pixel short near the top-left of the
    screen. Aiming just past the start of the pixel's own interval lands on it exactly.
    """
    vx, vy, vw, vh = virtual
    nx = (x - vx) * 65536 // max(1, vw) + 1
    ny = (y - vy) * 65536 // max(1, vh) + 1
    return max(0, min(65535, nx)), max(0, min(65535, ny))


def top_left_corner(monitors: list[tuple[int, int, int, int]]) -> tuple[int, int]:
    """The corner of the desktop that a mouse pushed up and to the left ends up in.

    `monitors` are (left, top, right, bottom) rectangles. With one monitor that is (0, 0).
    With another monitor to the left of or above the primary one, (0, 0) is in the middle
    of the desktop and the pointer slides straight past it, so the corner used is that of
    the leftmost monitor (the upper one if two are level).
    """
    if not monitors:
        return (0, 0)
    left, top, _, _ = min(monitors, key=lambda rect: (rect[0], rect[1]))
    return (left, top)


def elevation_problem(ours: bool | None, theirs: bool | None) -> str | None:
    """Why input cannot reach the game, given who runs as administrator, or None if it can.

    Each argument is True (elevated), False (not) or None (Windows refused to say). Windows
    silently drops input sent to a more privileged program, and SendInput reports success
    all the same, so this has to be worked out beforehand. A game we are refused a look
    at, when we are not elevated ourselves, is taken to be elevated: that refusal is how
    Windows treats questions about a more privileged program.
    """
    if ours is not False or theirs is False:
        return None
    seems = "is" if theirs else "appears to be"
    return (
        f"Kenshi {seems} running as administrator and kenshi-link is not, so Windows silently "
        "discards every key and click sent to the game. Nothing was sent. Ask the operator to "
        "start both at the same level: either restart Kenshi (and Steam) normally, or start the "
        "program that launches kenshi-link (PowerShell, Claude Code or Claude Desktop) as administrator."
    )
