"""What Claude is told about playing Kenshi through this interface.

INSTRUCTIONS is sent to every client as the MCP server's instructions. The longer
TOPICS are fetched on demand with the `manual` tool so they cost nothing until needed.

Both are orientation: how a turn works through these tools, what to look for on screen,
and the handful of game rules that hurt most when got wrong. Facts about the game beyond
that live in the reference (knowledge.py, the `lookup` tool), which this guide points to.

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
the pause state, not something read from the game, and Kenshi also pauses and un-pauses \
itself. The screenshot is the truth: a PAUSED panel shows while the game is paused. If they \
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
- On the title screen Escape quits the game, which cannot be started again from here.

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
- Left-click a character or their portrait to select them; Shift+left-click adds to the \
selection; left-drag a box around several. Right-click a portrait to jump the camera there. \
The hotkey tool selects squad members by number.

Giving orders (with characters selected)
- Right-click open ground: move there. With a character under the pointer, a click is never \
a move order.
- Right-click a thing or person: the default interaction. A standing enemy is attacked, \
someone with something to say is talked to, a downed stranger is looted, your own wounded \
character gets first aid, a bed is slept in, a machine or ore deposit is used. With SNEAK \
on, it tries to knock a person out instead, which is assault.
- Every other action is in the action menu, which exists only while the right button is \
held: menu_open(x, y), read the rows, then menu_choose(x, y) on one, or menu_cancel(). \
Entries act at once.
- Shift+right-click on work (an ore deposit, a machine, a storage box) makes it a standing \
job. press_key("r") stops what the selected characters are doing.
- Alt, the highlight key, is also the steal and lock-pick key. A plain right-click never \
steals (the character only walks over); with modifiers="alt" it takes the item or picks the \
lock, a crime if seen. A red item name means it has an owner.
- HUD order buttons: BLOCK, HOLD, PASSIVE, JOBS, RANGED, TAUNT and SNEAK switch on and off; \
MEDIC and RESCUE act once. Zoom in to see which are lit; lookup a button's name for what it does.

Camera and windows
- The camera tool pans, turns, zooms and tilts, also while the game is paused. The wheel \
zooms only with the pointer over the world, so close windows that cover the middle of the \
screen first.
- The hotkey tool opens the game's windows. hotkey("close", in_game=true) is Escape: it \
closes every open window at once. Never use it on the title screen, where Escape quits the game.
- quick_save and quick_load use one slot: quick_load throws away everything since the last \
quick save.

Time (set_speed and advance)
- Use these, never the pause key itself, which toggles. Kenshi also pauses itself when a \
conversation or the build window opens, in character creation and while an area loads, and \
un-pauses itself when a conversation closes or character creation is confirmed. After any \
of these, look for the PAUSED panel and correct the status line with sync_pause.
- Close the build window (hotkey("build_mode") again) before set_speed or advance: while it \
is open the pause key confirms the build instead.

Inside windows
- Drag an item to move it between slots or windows, or onto a portrait to hand it over. \
Right-clicking an item equips it, or with two inventories open moves one across (with \
Shift, the whole stack).
- In a shop, moving an item across buys or sells it at once; moving it back while the \
window is open undoes the deal.
- In a conversation, click one of the listed replies. Some cost money the moment you click, \
so read first.
""",
    "screen": """\
READING THE SCREEN

The layout shifts with resolution, UI scale and mods, and the sources disagree on where some \
panels sit. Treat this as what to look for, confirm it on your first screenshots, and record \
what you found in your notes.

- The 3D world fills the screen. Your characters and others are small figures; names and \
speech appear above them.
- The HUD is a band along the bottom edge. In it: a panel of details on whatever is selected \
(a character's health by body part and hunger, or a building's, bed's or container's details), \
which the wiki places bottom-left; the squad portraits; the order buttons; small window \
buttons; four time buttons (pause and three speeds); the money (c.1,234), day and clock.
- While the game is paused Kenshi shows a PAUSED panel and the pause button is lit. Learn what \
that looks like in this install, because it is the ground truth for the pause state.
- Messages about events appear for a few seconds as text near the HUD; zoom to read them.
- The cursor is not captured in screenshots. The magenta ring after a click is drawn by this \
tool, not by the game.

When a number matters (money, health, hunger, prices, stack sizes), zoom in and read it rather \
than estimating from the full screenshot. lookup("screen layout") says more about each panel.
""",
    "play": """\
PLAYING WELL THROUGH THIS INTERFACE

- Look before you run the clock. Before each advance, ask what could go wrong in that many \
seconds and shorten it if the answer is "a fight".
- New characters lose almost every fight. Early on, avoid combat. When chased, run to a \
guarded town gate, whose guards attack hostile pursuers. The Hub has no town guards: go into \
its bar, whose guards attack bandits that come near. Some gates are a danger to some squads, \
so lookup a town before you run to it.
- Being knocked down is not always death, but bleeding and hunger are, and in harsher regions \
the unconscious are eaten or enslaved. After a fight, bandage wounds: the healer needs a \
first aid kit in their own inventory; then right-click the wounded squad member or click \
MEDIC. Keep food on every character.
- A character who wakes with enemies near plays dead. Any order makes them stand up into the \
fight, so give none until the enemies have gone.
- Rest heals bruises and bandaged wounds only. A bed heals 8 times faster than standing \
around; towns rent them from about c.50 for 24 game hours, and right-clicking a rented bed \
pays at once.
- Money comes slowly at first. Mining ore near a town and selling it to a trader is the safe \
start (copper pays better than iron); so is hauling goods between towns once you know the roads.
- Crimes count when seen: taking an item with a red name, picking a lock, looting a body in \
town, entering a building that is not Public, locked or not. Told to leave, leave.
- Machines and research left alone only progress while a squad member or the camera is near.
- Save before anything risky and at natural checkpoints (hotkey("quick_save")).
- Long trips: lookup the regions on the way, zoom the camera out, right-click the ground in \
the direction you want, then advance at fast or fastest speed in chunks, checking the strip \
of frames each time for trouble.
""",
    "troubleshooting": """\
WHEN SOMETHING IS OFF

- A click did nothing: check the magenta ring. If it landed off-target, re-aim. If it landed \
right, a window may be in the way, nobody may be selected, a character may have been under \
the pointer, or the game may need a moment: advance briefly and look again.
- menu_open showed no list: nothing with a menu was under the pointer; menu_cancel and re-aim. \
Whether the menu opens while the game is paused is not confirmed: if it never does, try with \
the clock running.
- The status line says PAUSED but things are moving, or the reverse: trust the screenshot. \
With no PAUSED panel showing, call sync_pause(paused=false) and then set_speed("pause"); with \
the panel showing, sync_pause(paused=true).
- advance says nothing changed: unless the view was simply still, a conversation, the game \
menu or a loading screen is holding the game paused. Deal with it, then advance again.
- The view drifts by itself: the pointer is resting on the window's edge, which scrolls the \
camera even while paused. Any click moves it away. (Options, General, Edge scrolling turns \
this off.)
- The HUD is missing: press_key("f7") shows the UI again. The camera flies freely: \
press_key("semicolon") leaves the free camera.
- A hotkey opened the wrong thing or nothing: the operator may have rebound it. Use the \
on-screen button instead and tell the operator which key was wrong.
- You are lost in menus: hotkey("close", in_game=true) closes every open window; if the game \
menu opens instead, nothing was open, so press it again. On the title screen click its \
buttons instead: lookup("start a new game"). CONFIRM, the last of them, also starts the clock.
- The picture is black or shows another program: the game is probably in exclusive fullscreen \
or covered. Tell the operator; it must run windowed or borderless.
- "not the focused window": the operator clicked elsewhere. Try once more; if it still fails, \
ask the operator to click on the game.
- "Another window is covering the game": a notification or other window lies over the spot \
and the click was not sent. Notifications go away by themselves; otherwise aim beside it.
- "Kenshi is not responding": the game is loading or saving. Observe again after a moment, \
and keep trying for a minute or two before telling the operator.
- type_text refused a character, or says Caps Lock is on: the operator's keyboard layout \
cannot produce that character plainly. Use a simpler name.
""",
}


def manual(topic: str) -> str:
    key = topic.strip().lower()
    if key in ("", "index", "topics", "help"):
        return "Manual topics: " + ", ".join(TOPICS) + ". Call manual(topic) to read one."
    if key not in TOPICS:
        raise KeyError(f"No manual topic {topic!r}. Topics: {', '.join(TOPICS)}.")
    return TOPICS[key]
