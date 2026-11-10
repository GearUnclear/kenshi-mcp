"""A bare X11 window that looks like Kenshi-under-Wine to the backend and logs its input.

Usage: python x11_window.py EVENT_LOG.jsonl
Draws a red 100x100 square in the top-left corner of a blue 800x600 window.
"""

import json
import sys

from Xlib import X, display

WIDTH, HEIGHT, LEFT, TOP = 800, 600, 100, 50


def main() -> None:
    d = display.Display()
    screen = d.screen()
    window = screen.root.create_window(
        LEFT, TOP, WIDTH, HEIGHT, 0, screen.root_depth, X.InputOutput, X.CopyFromParent,
        background_pixel=0x204080,
        event_mask=(
            X.ExposureMask | X.KeyPressMask | X.KeyReleaseMask | X.ButtonPressMask
            | X.ButtonReleaseMask | X.PointerMotionMask | X.StructureNotifyMask
        ),
    )
    window.set_wm_name("Kenshi 1.0.64 - x64 (test window)")
    window.set_wm_class("kenshi_x64.exe", "kenshi_x64.exe")
    window.map()
    d.sync()
    gc = window.create_gc(foreground=0xFF0000)

    with open(sys.argv[1], "a", buffering=1) as log:

        def record(**fields) -> None:
            log.write(json.dumps(fields) + "\n")

        record(type="ready")
        while True:
            event = d.next_event()
            if event.type == X.Expose:
                window.fill_rectangle(gc, 0, 0, 100, 100)
                d.flush()
            elif event.type in (X.KeyPress, X.KeyRelease):
                record(
                    type="key", down=event.type == X.KeyPress,
                    keysym=d.keycode_to_keysym(event.detail, 0), state=event.state,
                )
            elif event.type in (X.ButtonPress, X.ButtonRelease):
                record(
                    type="button", down=event.type == X.ButtonPress, button=event.detail,
                    x=event.event_x, y=event.event_y, state=event.state,
                )
            elif event.type == X.MotionNotify:
                record(type="motion", x=event.event_x, y=event.event_y, state=event.state)


if __name__ == "__main__":
    main()
