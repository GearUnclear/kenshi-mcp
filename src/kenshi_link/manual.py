"""What Claude is told about playing Kenshi through this interface.

INSTRUCTIONS is sent to every client as the MCP server's instructions. The longer
TOPICS are fetched on demand with the `manual` tool so they cost nothing until needed.

Key names below are Kenshi's defaults. Players can rebind them, and the operator
mirrors any changes in the [keymap] section of the kenshi-link config, so the tools
that go through the keymap (set_speed, advance, camera, hotkey) stay correct even
when a key listed here is not.
"""

from __future__ import annotations

INSTRUCTIONS = """\
kenshi-link lets you play the game Kenshi on the operator's computer: you see the game \
through screenshots and act with its mouse and keyboard.

How a turn works
- Kenshi is real-time with pause, and you take far longer to decide than the game takes to \
kill someone. So keep the game paused while you look and think. Kenshi accepts orders while \
paused: select characters, give orders, open windows, move the camera, all without time passing.
- When your orders are in, call advance(seconds, speed). It runs the game for that long, pauses \
it again and shows you what happened. Use short advances (2-10 s at normal speed) when anything \
could go wrong nearby, and long, fast ones for travel or waiting.
- Every tool that acts returns a screenshot taken afterwards. Read it before acting again; an \
order that was not confirmed on screen did not necessarily happen.

Seeing and pointing
- Coordinates are pixels in the latest full screenshot, (0, 0) at the top-left. After a click \
the screenshot shows a magenta ring where it landed; if the ring missed, correct and retry.
- Kenshi's text is small. Use zoom on a region before relying on any number or label you \
cannot read cleanly, and observe(grid=true) when you need help judging positions.
- The status line in square brackets at the end of each result is this tool's belief about \
pause and speed, not something read from the game. The screenshot is the truth: if they \
disagree, fix the belief with sync_pause.

Knowing the game
- lookup(query) searches a built-in reference on Kenshi: places, factions, creatures, items \
and prices, health, crime, building, the interface, step-by-step how-tos. Use it before you \
guess: to plan a trip, on meeting a faction or creature, to learn what a button does, or when \
an order did not do what you expected. lookup_topics lists what it covers.
- The screen outranks the reference, a fact it marks (unverified) is only a lead, and on how \
to send an input the tool descriptions outrank it.

Limits
- Input is sent only while the Kenshi window has focus, and only keys that stay inside the game.
- If a result contains KENSHI_LINK_HALTED, the operator has stopped the session or their PC is \
locked. Stop calling game tools and tell them what you were doing.
- Loading a save discards progress since the last save; make sure that is what you want.

Memory
- notes_read and notes_write keep a notes file that outlives this conversation. Read it when \
you start. Write to it whenever you learn something you would not want to rediscover: the goal \
and plan, who is in the squad and their condition, where things are, what killed you last time.

Start by calling notes_read, manual("controls") and observe.
"""

TOPICS: dict[str, str] = {
    "controls": """\
KENSHI CONTROLS (default bindings)

Selecting
- Left-click a character, or their portrait, to select them. Shift+left-click adds to the \
selection. Left-drag a box around several characters to select them together.
- hotkey("select_1") ... hotkey("select_10") select squad members by number; repeat=2 also \
centres the camera on them. hotkey("select_all") selects the whole squad; hotkey("next_squad") \
switches squad.

Giving orders (with characters selected)
- Right-click the ground: move there.
- Right-click a thing or person: the default interaction (attack an enemy, talk, loot, open, \
pick up, use a machine, enter a door).
- Hold right-click on a target (click with button="right", hold_seconds=0.7): opens a menu of \
every action available on it. Then left-click the option you want.
- Shift+right-click on a job such as a mine, a machine or a storage box adds it to the \
character's standing job list, so they keep doing it.
- The buttons in the lower part of the screen switch behaviours on and off for the selected \
characters (for example sneaking, holding position, passive, blocking, taunting, ranged, \
doing jobs, medic and rescue) and set walking, jogging or running. Click them like any button; \
zoom in first to read which is which and which are currently lit.

Camera (the camera tool)
- forward/back/left/right pan, rotate_left/rotate_right turn, zoom_in/zoom_out use the wheel, \
tilt_up/tilt_down drag with the middle button. The camera moves while the game is paused.
- Wheel actions go to whatever is under the pointer, so close windows that cover the middle \
of the screen before zooming.

Windows (the hotkey tool)
- inventory, map, stats, research, crafting, build_mode open and close the matching window. \
close presses Escape, which closes the top window, or opens the main menu if none is open.
- highlight_items holds the highlight key and takes the screenshot while item labels are showing.
- quick_save and quick_load save and load the quick-save slot.

Time (set_speed and advance)
- The pause key toggles, so always go through set_speed/advance rather than pressing it yourself; \
they track which state the game is in.

Inside windows
- Inventories are grids: drag an item to move it between slots or windows. Trading, looting \
and containers show two inventories side by side.
- Dialogue shows a list of reply lines; click the one you want.
- Text boxes (naming a character or squad): click the box, then type_text.
""",
    "screen": """\
READING THE SCREEN

The layout shifts with resolution, UI scale and mods, so treat this as what to look for and \
confirm it on your first screenshots (then record what you found in your notes).

- The 3D world fills the screen. Your characters and others are small figures; names and \
speech appear above them.
- Squad portraits sit along the bottom-left. A portrait shows a character's condition at a \
glance and can be clicked to select them.
- The selected character's details (health by body part, hunger, encumbrance, current goal) \
appear in a panel near the portraits.
- The order and behaviour buttons, the row of window buttons, the time controls \
(pause and the speed arrows), the clock and the money counter (cats, written c.) are grouped \
toward the bottom-right.
- When the game is paused, Kenshi says so on screen and the pause control is lit. Learn what \
that looks like in this install, because it is the ground truth for the pause state.
- Messages about events (combat, hunger, crimes, arrivals) appear as text over the world or \
in a log; zoom to read them.
- The cursor is not captured in screenshots. The magenta ring after a click is drawn by this \
tool, not by the game.

When a number matters (money, health, hunger, prices, stack sizes), zoom in and read it rather \
than estimating from the full screenshot.
""",
    "play": """\
PLAYING WELL THROUGH THIS INTERFACE

- Look before you run the clock. Before each advance, ask what could go wrong in that many \
seconds and shorten it if the answer is "a fight".
- New characters lose almost every fight. Early on, avoid combat, stay near town guards, and \
run toward a town gate when chased: guards engage hostile pursuers.
- Being knocked down is not always death, but bleeding and hunger are. After any fight check \
each character's condition, bandage wounds (first aid kits, or the medic behaviour), and keep \
food in someone's inventory.
- Rest heals. Beds heal much faster than standing around; bars rent them.
- Money comes slowly at first. Mining ore near a town and selling it to a trader is the safe \
start; so is hauling goods between towns once you know the roads.
- Taking things that are not yours, or entering locked buildings, is a crime with witnesses \
around. Check an item's ownership before picking it up in town.
- Save before anything risky and at natural checkpoints (hotkey("quick_save")).
- Long trips: zoom the camera out, right-click the ground in the direction you want, then \
advance at fast or fastest speed in chunks, checking the strip of frames each time for trouble.
- Keep notes current. Your view of the world is one screen at a time; the notes are how you \
remember where towns, ore, enemies and your own people are.
""",
    "troubleshooting": """\
WHEN SOMETHING IS OFF

- A click did nothing: check the magenta ring. If it landed off-target, re-aim. If it landed \
right, a window may be in the way, nobody may be selected, or the game may need a moment: \
advance briefly and look again.
- The right-click menu vanished when the button was released: open it and choose in one \
motion instead, with drag(button="right") from the target to where the option appears.
- A hotkey opened the wrong thing or nothing: the operator may have rebound it. Use the \
on-screen button instead and tell the operator which key was wrong.
- The status line says PAUSED but things are moving (or the reverse): trust the screenshot, \
call sync_pause with the real state, then set_speed("pause") if the game is running.
- The picture is black or shows another program: the game is probably in exclusive fullscreen \
or covered. Tell the operator; it must run windowed or borderless.
- "not the focused window": the operator clicked elsewhere. Try once more (the tool tries to \
refocus the game); if it still fails, ask the operator to click on the game.
- "Another window is covering the game": a notification or some other window lies over the \
spot you aimed at, and the click was not sent. Observe to see it; notifications go away by \
themselves, otherwise aim beside it or tell the operator.
- "Kenshi is not responding": the game is busy loading or saving and nothing was sent. Observe \
again after a moment, and keep trying for a minute or two before telling the operator.
- A loading screen that does respond: use advance, or wait a few seconds and observe again. \
After a load the game may come back paused; observe re-checks this.
- type_text refused a character, or says Caps Lock is on: the operator's keyboard layout \
cannot produce that character plainly. Use a simpler name.
- You are lost in menus: hotkey("close") backs out one window at a time. If the main menu \
opens, press it again to close it.
""",
}


def manual(topic: str) -> str:
    key = topic.strip().lower()
    if key in ("", "index", "topics", "help"):
        return "Manual topics: " + ", ".join(TOPICS) + ". Call manual(topic) to read one."
    if key not in TOPICS:
        raise KeyError(f"No manual topic {topic!r}. Topics: {', '.join(TOPICS)}.")
    return TOPICS[key]
