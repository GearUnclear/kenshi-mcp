# kenshi-mcp

An MCP server that lets Claude play [Kenshi](https://lofigames.com/). Claude sees the game
through screenshots and operates it with the mouse and keyboard, the way a person would. It
works with Claude Code and Claude Desktop, and includes a runner for unattended play through
the Claude API.

The Python package and its command are called `kenshi-link`.

## Status

Early. It was built and tested on a machine without the game:

- The controller, the MCP server and the unattended runner are covered by tests against a
  stand-in window and a scripted API.
- The whole test suite and the Windows self-test pass on Windows Python under Wine, including
  the MCP server and the runner driving a real Win32 window. The Linux/X11 code is tested
  against a real X server.
- It has not yet been run against Kenshi itself, on native Windows, or against the live
  Claude API.

Key bindings and mouse conventions come from the game's published defaults. Expect the first
real session to turn up things that need tuning. Reports of what breaks are welcome.

## How it works

Kenshi is real-time with pause, and Claude needs several seconds per decision. So game time
is something Claude spends on purpose:

- The game stays paused while Claude looks and gives orders. Kenshi accepts orders while paused.
- `advance(seconds, speed)` runs the clock for a set time, pauses again, and returns a strip
  of in-between frames plus the final screenshot.
- Every action returns a screenshot taken afterwards, with a ring where a click landed, so
  Claude can check its own aim.

Claude works from screenshots only. It cannot read game memory or save files, so numbers come
from zooming in on the UI, and fast combat micro-management is out of reach.

## Setup (Windows)

You need Kenshi set to **windowed or borderless** (exclusive fullscreen gives black
screenshots), Python 3.11 or newer, and Claude Code, Claude Desktop or a Claude API key.

In PowerShell:

```powershell
git clone https://github.com/GearUnclear/kenshi-mcp
cd kenshi-mcp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[agent]"
```

Leave out `[agent]` if you only want the MCP server. If PowerShell refuses to run
`Activate.ps1`, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
once and try again.

Start Kenshi, load a save, and check that the window is found and captured:

```powershell
kenshi-link doctor --screenshot check.jpg
```

Open `check.jpg`. It should show the game. A black picture means exclusive fullscreen.

To check input injection and capture without the game, run the self-test. It opens a small
test window and verifies that every kind of input arrives intact; leave the mouse and
keyboard alone while it runs.

```powershell
python tests\windows_selftest.py
```

Run everything at the same privilege level as the game. If Kenshi runs as administrator and
this does not, Windows silently drops the input.

## Connect a Claude client

Claude Code, from the `kenshi-mcp` folder:

```powershell
claude mcp add --scope user kenshi -- "$PWD\.venv\Scripts\kenshi-link.exe" serve
```

Claude Desktop: add this to `%APPDATA%\Claude\claude_desktop_config.json` with your own path
(backslashes doubled), then restart the app.

```json
{
  "mcpServers": {
    "kenshi": {
      "command": "C:\\Users\\you\\kenshi-mcp\\.venv\\Scripts\\kenshi-link.exe",
      "args": ["serve"]
    }
  }
}
```

Then, with a save loaded, ask Claude to play. For example: "Use the kenshi tools. My character
is in the Hub with almost no money. Earn 1,000 cats by mining copper and selling it, and keep
them alive."

Claude uses your real mouse and keyboard, and brings Kenshi to the front whenever it acts, so
leave the PC to it while it plays.

## Unattended play

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
kenshi-link play --goal "Mine copper near the Hub and sell it until we have 1,000 cats." --max-steps 40
```

This runs Claude in a loop through the Claude API until the goal is reached or the budget
runs out (by default 300 game actions or 120 minutes, on `claude-opus-5-5`). Every turn sends
a screenshot, so long sessions cost real money. Start small.

- If a safety classifier declines a turn, the API retries it on a fallback model instead of
  ending the session. `--no-fallbacks` turns that off.
- Old screenshots are cleared from the context server-side. If a conversation still grows very
  large, Claude writes a handoff into its notes file and a fresh conversation continues from it.

See `kenshi-link play --help` for the other options. Transcripts are written to
`%USERPROFILE%\.kenshi-link\sessions\`.

## Stopping it

Any of these disables all input until you allow it again:

- Push the mouse into the top-left corner of the screen (the leftmost one, if you have several).
- Run `kenshi-link stop` from another PowerShell window.
- Tap Pause/Break, if your keyboard has it.

A stop takes effect within moments, including in the middle of typing, a drag or a held key.
`kenshi-link resume` allows input again.

Other guard rails:

- Input is only sent while the Kenshi window has focus, and pointer positions are confined to
  the window.
- A click is refused where another window, such as a notification, covers the game.
- Key combinations that leave the game (the Windows key, Alt+Tab, Alt+F4, Shift+Tab for the
  Steam overlay and similar) are refused, as are Kenshi's debug shortcuts.
- If Kenshi is running as administrator and this is not, it says so instead of failing silently.

## Tools

| Tool | What it does |
|---|---|
| `observe` | Screenshot, optionally with a coordinate grid |
| `zoom` | Enlarges a region at full resolution, for reading small text |
| `click`, `drag`, `scroll` | Pointer input in screenshot coordinates. A held right-click opens Kenshi's action menu |
| `press_key`, `type_text` | Keyboard input, limited to keys that stay inside the game |
| `hotkey` | Named actions through your key bindings: inventory, map, stats, research, build mode, squad selection, quick save and load |
| `camera` | Pan, rotate, zoom and tilt |
| `advance` | Run the game for N seconds at a chosen speed, then pause and report |
| `set_speed`, `sync_pause` | Pause or run the clock; correct the tracked pause state |
| `notes_read`, `notes_write` | A notes file that persists between conversations |
| `manual` | A guide to Kenshi's controls and screen layout, read on demand |

## Configuration

Optional, in `%USERPROFILE%\.kenshi-link\config.toml`. `config.example.toml` lists every
setting. The one most likely to matter is `[keymap]`: if you have rebound keys in Kenshi,
mirror the changes there.

To try the tools without the game, set `$env:KENSHI_LINK_BACKEND = "mock"`. That swaps Kenshi
for a built-in stand-in (numbered dots that can be selected, ordered around, paused and sped
up) and sends no real input.

## Linux

Kenshi under Proton or Wine works through X11 or XWayland. Install the same way, and use
`.venv/bin/kenshi-link` in place of the `.exe` path. The data directory is `~/.kenshi-link`.

## Development

```powershell
pip install -e ".[dev]"
pytest
```

On Linux, `xvfb-run -a pytest -m x11` also runs the X11 backend tests against a real X server.

## License

MIT. See [LICENSE](LICENSE).

This is an unofficial project and is not affiliated with Lo-Fi Games. It automates the mouse
and keyboard of a copy of Kenshi you own; it does not modify the game.
