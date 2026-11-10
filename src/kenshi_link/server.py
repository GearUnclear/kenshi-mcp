"""The MCP server: the tools a Claude client uses to play Kenshi.

Run it with `kenshi-link serve` (or `python -m kenshi_link.server`). It speaks MCP
over stdio, so any MCP client (Claude Code, Claude Desktop, the bundled autonomous
runner) can attach to it.
"""

from __future__ import annotations

import asyncio
import functools
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Any, Literal

from pydantic import Field

from .config import Config, load_config
from .controller import ControlError, Controller, Result, read_notes, write_notes
from .manual import INSTRUCTIONS, TOPICS
from .manual import manual as read_manual

try:  # mcp 2.x
    from mcp.server.mcpserver import Image, MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
except ImportError:  # mcp 1.x, where the same class is called FastMCP
    from mcp.server.fastmcp import FastMCP as MCPServer
    from mcp.server.fastmcp import Image
    from mcp.server.fastmcp.exceptions import ToolError

log = logging.getLogger("kenshi_link")

Speed = Literal["pause", "normal", "fast", "fastest"]
RunSpeed = Literal["normal", "fast", "fastest"]
Button = Literal["left", "right", "middle"]
CameraAction = Literal[
    "forward", "back", "left", "right", "rotate_left", "rotate_right",
    "zoom_in", "zoom_out", "tilt_up", "tilt_down",
]


class _Session:
    """Owns the controller and runs every call on one dedicated thread.

    The platform handles underneath (X display, GDI contexts, the attached input
    queue) belong to the thread that made them, and input sequences must never
    interleave, so a single worker gives both guarantees.
    """

    def __init__(self, config: Config, controller: Controller | None = None) -> None:
        self.config = config
        self._controller = controller
        self._pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="kenshi-link")

    def _get(self) -> Controller:
        if self._controller is None:
            try:
                self._controller = Controller(self.config)
            except Exception as exc:
                raise ControlError(f"Could not start the game interface: {exc}") from exc
        return self._controller

    def _call(self, method: str, args: tuple, kwargs: dict) -> Result:
        return getattr(self._get(), method)(*args, **kwargs)

    async def _on_worker(self, function, *args: Any) -> Any:
        """Run on the worker thread, turning failures into errors the model can read.

        The MCP SDK only passes a message through to the client for ToolError; anything
        else is reported as an anonymous crash, which would leave Claude guessing.
        """
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(self._pool, functools.partial(function, *args))
        except ControlError as exc:
            raise ToolError(str(exc)) from exc
        except Exception as exc:
            log.exception("unexpected failure in the game interface")
            raise ToolError(f"Internal error in kenshi-link ({type(exc).__name__}: {exc}).") from exc

    async def run(self, method: str, *args: Any, **kwargs: Any) -> list[Any]:
        result = await self._on_worker(self._call, method, args, kwargs)
        return [result.text, *(Image(data=shot.data, format=shot.format) for shot in result.images)]

    async def run_plain(self, function, *args: Any) -> Any:
        return await self._on_worker(function, *args)


def build_server(config: Config | None = None, controller: Controller | None = None) -> MCPServer:
    config = config or load_config()
    session = _Session(config, controller)
    server = MCPServer("kenshi-link", instructions=INSTRUCTIONS)
    tool = functools.partial(server.tool, structured_output=False)

    # ---- looking ----------------------------------------------------------------

    @tool()
    async def observe(
        grid: Annotated[
            bool, Field(description="Draw a labelled coordinate grid over the screenshot.")
        ] = False,
    ) -> list:
        """Take a screenshot of the Kenshi window without touching the game.

        Call this at the start, after waiting for something, and any time you are unsure
        what is on screen. It also re-checks whether the game looks paused. Other tools
        already return a screenshot, so you do not need to call this after each of them.
        """
        return await session.run("observe", grid)

    @tool()
    async def zoom(
        x0: Annotated[float, Field(description="Left edge of the region, in screenshot pixels.")],
        y0: Annotated[float, Field(description="Top edge of the region, in screenshot pixels.")],
        x1: Annotated[float, Field(description="Right edge of the region, in screenshot pixels.")],
        y1: Annotated[float, Field(description="Bottom edge of the region, in screenshot pixels.")],
    ) -> list:
        """Show one region of the screen enlarged, at the game's full resolution.

        Use it to read small text and numbers (stats, prices, health, item names, button
        labels, messages) before relying on them. It does not change the game or the
        coordinate system: keep using full-screenshot coordinates for clicks.
        """
        return await session.run("zoom", x0, y0, x1, y1)

    # ---- pointer ----------------------------------------------------------------

    @tool()
    async def click(
        x: Annotated[float, Field(description="X in screenshot pixels.")],
        y: Annotated[float, Field(description="Y in screenshot pixels.")],
        button: Annotated[Button, Field(description="Mouse button.")] = "left",
        modifiers: Annotated[
            str, Field(description="Keys held during the click: '', 'shift', 'ctrl', 'alt' or e.g. 'ctrl+shift'.")
        ] = "",
        count: Annotated[int, Field(description="1 for a click, 2 for a double-click.", ge=1, le=3)] = 1,
        hold_seconds: Annotated[
            float, Field(description="Keep the button down this long before releasing.", ge=0)
        ] = 0.0,
    ) -> list:
        """Click in the game.

        Left-click selects characters and presses buttons. Right-click gives the selected
        characters their default order for whatever is under the pointer (move, attack,
        talk, loot, use). A right-click with hold_seconds=0.7 opens Kenshi's menu of all
        actions for that target. Shift+right-click on a job adds it as a standing job.
        Returns a screenshot with a magenta ring where the click landed.
        """
        return await session.run("click", x, y, button, modifiers, count, hold_seconds)

    @tool()
    async def drag(
        x0: Annotated[float, Field(description="Start X in screenshot pixels.")],
        y0: Annotated[float, Field(description="Start Y in screenshot pixels.")],
        x1: Annotated[float, Field(description="End X in screenshot pixels.")],
        y1: Annotated[float, Field(description="End Y in screenshot pixels.")],
        button: Annotated[Button, Field(description="Mouse button held during the drag.")] = "left",
        modifiers: Annotated[str, Field(description="Keys held during the drag, as for click.")] = "",
    ) -> list:
        """Press a mouse button at one point, move to another, and release.

        Use it to box-select several characters (left-drag across the world), to move
        items between inventory slots or windows, and to drag sliders and scrollbars.
        """
        return await session.run("drag", x0, y0, x1, y1, button, modifiers)

    @tool()
    async def scroll(
        x: Annotated[float, Field(description="X in screenshot pixels to scroll at.")],
        y: Annotated[float, Field(description="Y in screenshot pixels to scroll at.")],
        direction: Annotated[Literal["up", "down"], Field(description="Wheel direction.")],
        amount: Annotated[int, Field(description="Number of wheel notches.", ge=1, le=30)] = 3,
    ) -> list:
        """Turn the mouse wheel with the pointer at a position.

        Over a list or window it scrolls the contents. Over the 3D world, up zooms the
        camera in and down zooms out (the camera tool does the same from the centre).
        """
        return await session.run("scroll", x, y, direction, amount)

    # ---- keyboard ---------------------------------------------------------------

    @tool()
    async def press_key(
        key: Annotated[
            str,
            Field(description="A key or combo such as 'escape', 'enter', 'r', 'f7', 'shift+a', 'delete'."),
        ],
        repeat: Annotated[int, Field(description="How many times to press it.", ge=1, le=20)] = 1,
        hold_seconds: Annotated[float, Field(description="Hold each press this long.", ge=0)] = 0.0,
    ) -> list:
        """Press a key that the other tools do not cover.

        Prefer the dedicated tools: set_speed and advance for time, camera for the camera,
        hotkey for game windows, squad selection and saving. Keys that would leave the game
        (the Windows key, alt+tab, alt+f4 and similar) are refused.
        """
        return await session.run("press_key", key, repeat, hold_seconds)

    @tool()
    async def type_text(
        text: Annotated[str, Field(description="Text to type (US-keyboard characters, up to 200).")],
    ) -> list:
        """Type text into the text box that currently has focus in the game.

        Only use it when a text box is active (naming a character, squad, save or
        building): click the box first. Typed into the world instead, the letters act as
        hotkeys and a space toggles pause.
        """
        return await session.run("type_text", text)

    hotkey_actions = sorted(
        action
        for action in config.keymap
        if action not in ("pause", "speed_normal", "speed_fast", "speed_fastest")
        and not action.startswith("camera_")
    )

    @tool(
        description=(
            "Press one of Kenshi's hotkeys by what it does, using the operator's key bindings.\n\n"
            "Actions: " + ", ".join(hotkey_actions) + ".\n"
            "inventory, map, stats, research, crafting and build_mode open or close that window. "
            "select_1 to select_10 pick a squad member (repeat=2 also centres the camera on them); "
            "select_all picks the whole squad; next_squad switches squad. close presses Escape. "
            "highlight_items shows item labels in the returned screenshot. quick_save saves; "
            "quick_load loads the last quick save and discards everything since."
        )
    )
    async def hotkey(
        action: Annotated[str, Field(description="One of the listed action names.")],
        repeat: Annotated[int, Field(description="How many times to press it.", ge=1, le=5)] = 1,
    ) -> list:
        return await session.run("hotkey", action, repeat)

    # ---- camera -----------------------------------------------------------------

    @tool()
    async def camera(
        action: Annotated[CameraAction, Field(description="How to move the camera.")],
        steps: Annotated[
            int, Field(description="How far: each step is a short pan/turn, one zoom notch or a small tilt.", ge=1, le=20)
        ] = 2,
    ) -> list:
        """Move the game camera. Works while the game is paused.

        forward/back/left/right pan across the ground, rotate_left/rotate_right turn the
        view, zoom_in/zoom_out change height, tilt_up/tilt_down change the viewing angle.
        To jump to a squad member instead, use hotkey('select_N', repeat=2).
        """
        return await session.run("camera", action, steps)

    # ---- time -------------------------------------------------------------------

    @tool()
    async def advance(
        seconds: Annotated[
            float, Field(description="Real seconds to let the game run before pausing again.", gt=0)
        ],
        speed: Annotated[RunSpeed, Field(description="Game speed while it runs.")] = "normal",
        frames: Annotated[
            int, Field(description="How many in-between frames to capture and return as a strip.", ge=0, le=4)
        ] = 2,
    ) -> list:
        """Let game time pass, then pause again and show the result.

        This is the normal way to make anything happen: give orders while paused, then
        advance. It unpauses at the chosen speed, waits, re-pauses, and returns a strip of
        frames from along the way plus a screenshot of the paused game. Keep it short
        (2-10 s, normal speed) when enemies or other risks are near; use longer runs at
        fast or fastest for travel, mining, healing and waiting.
        """
        return await session.run("advance", seconds, speed, frames)

    @tool()
    async def set_speed(
        speed: Annotated[Speed, Field(description="'pause', or a running speed.")],
    ) -> list:
        """Pause the game, or set it running and leave it running.

        Use set_speed('pause') to make sure the game is paused. Setting a running speed
        leaves the clock running while you think, which is rarely what you want: use
        advance instead unless you intend to watch something unfold with repeated observe calls.
        """
        return await session.run("set_speed", speed)

    @tool()
    async def sync_pause(
        paused: Annotated[bool, Field(description="True if the game is actually paused right now.")],
    ) -> list:
        """Correct this tool's record of whether the game is paused. Presses nothing.

        Call it when the screenshot contradicts the status line (for example the game's
        pause indicator is showing but the status says RUNNING), so that the next
        set_speed or advance presses the pause key the right number of times.
        """
        return await session.run("sync_pause", paused)

    # ---- memory and reference ---------------------------------------------------

    @tool()
    async def notes_read() -> str:
        """Read your persistent notes file.

        The notes survive between conversations and context resets. Read them when you
        start playing and whenever you need something you may have recorded earlier.
        """
        text = await session.run_plain(read_notes, config.notes_file)
        return text if text.strip() else "(The notes file is empty.)"

    @tool()
    async def notes_write(
        text: Annotated[str, Field(description="Markdown text to save.")],
        mode: Annotated[
            Literal["append", "replace"],
            Field(description="'append' adds to the end; 'replace' rewrites the whole file."),
        ] = "append",
    ) -> str:
        """Save to your persistent notes file.

        Record what a future you would need: the current goal and plan, squad members
        and their state, money, locations of towns and resources, what the UI looks like
        in this install, and lessons from mistakes. Use replace to tidy the file when it
        grows long or goes stale.
        """
        size = await session.run_plain(write_notes, config.notes_file, text, mode)
        return f"Notes saved ({size} characters in the file)."

    @tool(
        description=(
            "Read a section of the guide to playing Kenshi through this interface. Topics: "
            + ", ".join(TOPICS)
            + ". Read 'controls' before your first action, and 'troubleshooting' when a tool "
            "result surprises you."
        )
    )
    async def manual(
        topic: Annotated[str, Field(description="Topic name.")] = "controls",
    ) -> str:
        try:
            return read_manual(topic)
        except KeyError as exc:
            raise ToolError(str(exc.args[0])) from exc

    return server


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="kenshi-link: %(message)s")
    server = build_server()
    server.run()


if __name__ == "__main__":
    main()
