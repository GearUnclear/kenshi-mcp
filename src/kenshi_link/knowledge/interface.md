# Interface

What is on Kenshi's screen in the unmodded 1.0.x game (HUD, windows, menus), what each element shows and does, and the default keyboard and mouse bindings, from the wikis, the patch notes and a third-party analysis of the game's code and GUI files, noting where sources disagree or a position is not confirmed.

## How sure these layout facts are
Also: confidence, verified, unverified, code analysis, resolution, UI scale, font size
- Keys, mouse behaviour and what buttons do come from the two Kenshi wikis and the official patch notes mirrored there. Treat those as reliable.
- "(code analysis)" marks facts from the MeitouClient project's notes: a third party's reading of the 1.0.68 executable, its controls.cfg and its GUI layout files. Exact on labels, defaults and input rules, but not from the developers and mostly unchecked in the running game.
- Percentages are shares of the screen's width and height from the top-left corner, from those layout files. The GUI stretches with the window, so they hold at any resolution; sizes quoted "at 1080p" scale with the height.
- The Font Size option changes text size and can shift what a panel shows.
- A bullet ending in (unverified) rests on memory, one forum post or an old guide.
- Find elements by label first, then record pixel positions in your notes.

## Screen layout at a glance
Also: HUD, GUI, main panel, bottom bar, where is everything
- The 3D world fills the screen. The HUD is a band of panels along the bottom edge: selection info, health, portraits, orders, window buttons, speed buttons, time and money (code analysis; it gives no left-to-right order).
- Bottom-left: the information panel for whatever is selected (wiki: "the bottom left UI").
- Bottom-right: order buttons, movement-speed icon, Build, Prospect and the jobs list (wiki, patch notes); also the outpost panel while the camera is over your own outpost.
- Squad portraits: in the band; community guides say the middle (unverified)
- Speed buttons, clock and money: in the band; expected toward the right (unverified)
- Just above the band, centre: event messages and button tooltips, about 32% to 68% across and 71% to 78% down (code analysis).
- Top-left: tutorial lines. Top-right: a thin bar while data loads.
- The PAUSED panel is part of the HUD; where it sits is (unverified)
- Names and speech appear above characters.

## Selected character panel (bottom-left)
Also: character info panel, State line, Goal line, expand stats, lower left panel
- Left-click a character (yours or anyone) and their details fill the panel. A stranger is only inspected: your own selection stays and still takes orders (code analysis).
- Top line: name on the left, faction on the right. Your faction is "Nameless" until renamed.
- Then "State:" (Normal, Defensive, Sleeping, Unconscious, Dead), "Goal:" (what they are doing; "Aimless" if nothing) and "Encumbrance:" as a percentage (code analysis).
- Stat lines: Attack and Defense (Martial Arts when fighting unarmed), Strength, Dexterity, Toughness, Dodge.
- While working, a line names the skill in use, for example "Labouring 1".
- A small ^ button expands the panel: Athletics XP, Strength XP, Toughness XP, KO point, Run speed, Hunger Rate.
- A "Bounty:" line, at the top of the panel (wiki), shows only for a character with a bounty or a status such as Slave or "Committing Crime!" with its countdown.
- Effects of worn items such as shackles show here, not in the item text (wiki).

## Health readout: blood and body parts
Also: health pane, medical panel, limbs, bleeding arrows, bar colours
- The health pane is in the bottom-left area (wiki). Rows from the top: Blood (Oil on Skeletons), then the body parts, with Hunger last (code analysis). The wiki's order: Head, Chest, Stomach, Left Arm, Right Arm, Left Leg, Right Leg.
- Each row has a name, a number and a layered bar: green is health now; yellow is bandaged and will heal; red is untreated damage; the grey end is damage only rest restores (one wiki guide calls it black).
- Arrows at the right of a row (code analysis): "<" needs bandaging; "<<" below zero and getting worse; "<<!!" a vital part below the knockout point; "!!!" destroyed. The wiki reads "<" as a degenerating wound and "<<" as about 4 times faster.
- On the Blood row, more "<" means faster bleeding.
- Head, Chest or Stomach below 0 means knocked out; a part at minus its maximum means death or limb loss.

## Health status word
Also: condition, Normal, Wounded, Unconscious, Playing dead, Recovery coma, Dying, Rebooting
- The health pane carries one word for the character's overall state (code analysis).
- Healthy to hurt: Normal, Slightly Injured, Wounded.
- Food: Hungry or Malnourished (hunger below 200), Starving (below 100).
- Bleeding: losing blood. Blood loss KO and Bleeding out: unconscious from blood loss.
- "Unconscious (N)": knocked out, N counting down. Skeletons show "Rebooting".
- Recovery coma: stays down until every vital part is back above 0.
- "Playing dead...": awake but staying down until enemies leave.
- Crippled: the legs cannot carry them. Crippled arm: the weapon arm is out.
- Critical, Limb trauma, Dying: wounds getting worse; treat them now.

## Hunger display
Also: food meter, hunger row, hunger number, hunger arrows
- Hunger is the last row of the health pane; the number has a normal maximum of 300 (code analysis). Skeletons have no hunger row and do not eat.
- Arrows on the row: ">" food is being digested; "<" falling; "<!" below 200 (code analysis).
- Status words: "Hungry" between 100 and 200 with an empty stomach, "Malnourished" in the same band once fed and recovering, "Starving" below 100.
- Stat and speed penalties start below 200; fainting starts at 100 + KO point (90 at Toughness 0, lower with more Toughness); death is at 0. See "Hunger: the scale and thresholds" in Health and medical.
- Game starts flagged malnourished begin at 170 of 300.
- Below 250 a character eats automatically from food in reach.
- The portrait gets a hunger mark below 125 (code analysis).

## Squad portraits and squad tabs
Also: character icons, portrait bar, party list, squad list
- Each squad with members has a tab carrying its name (a new game's squad may read "Nameless_0"). Click a tab, or press Tab, to show that squad (code analysis).
- Portraits are square cells, 60 to 128 px, up to 10 in a row; further rows scroll.
- Left-click: select. Shift+left-click: add, or take out one already selected.
- Double-left-click or a quick right-click: select and jump the camera to them, however far away; it then follows them until you pan.
- Right button held 0.25 s: that character's action menu.
- Look (code analysis): highlighted border = selected; faded = dead, unconscious, carried or in bed; flashing red = in danger off screen; small marks for combat, hunger, shackles, prison.
- Dragging an item onto a portrait gives it to that character (patch notes).
- Portraits and tabs flash when something needs attention (patch notes).
- ` (backtick) selects the whole squad; a "select all" button also exists.

## Order and behaviour buttons (the seven toggles)
Also: behaviour buttons, combat mode, stance buttons, AI toggles, orders panel, right side buttons, numpad keys
- Seven toggle buttons sit on the right side of the HUD, labelled in capitals: BLOCK, HOLD, PASSIVE, JOBS, RANGED, TAUNT, SNEAK. Each has its own section ("BLOCK button" and so on).
- Each is an on/off toggle for the selected characters, set per character until changed. Left-click to switch.
- Default for a new character: JOBS and RANGED on, the other five off.
- The same panel holds the movement-speed icon, MEDIC, RESCUE, Prospect and the jobs list (code analysis). MEDIC and RESCUE are commands, not toggles.
- A lit (highlighted) button is on; zoom in to tell lit from unlit (unverified)
- Default keys (code analysis): numpad 0 BLOCK, 1 HOLD, 2 PASSIVE, 3 RANGED, 4 SNEAK, 5 TAUNT, 6 next movement speed, 7 MEDIC, 8 RESCUE; JOBS and Prospect have none. The wiki's key list shows none of these.

## BLOCK button
Also: block mode, defensive mode, defensive stance, block only, never attack
- On: the character never swings, only defends, and still squares up to enemies. The selection panel then reads "State: Defensive".
- Bonus while on: +20 Melee Defence; the button's own text promises 20 melee defence and no attempts to attack. The wiki also lists +20 Dodge; the code analysis counts that only for a character fighting unarmed.
- It applies only while standing, not while crawling (code analysis).
- A crippled character still tries to punch attackers even with BLOCK on.
- BLOCK does not stop crossbow fire if RANGED is also on.
- It lowers the Dodge XP gained; Melee Defence XP is unaffected.
- Use it to buy time when outmatched, or to train defence.
- If an attack order seems to do nothing, check that BLOCK is not lit.

## HOLD button
Also: hold position, stay put, stand ground, do not chase, guard a spot
- On: the character holds the spot where the button was pressed (or where a later move order ends) and does not run off to join combat elsewhere.
- On HOLD a character attacks hostiles on sight, which it otherwise does not, but only close ones: roughly within 8 m of the held spot, 14 m for an enemy already fighting and heading their way (code analysis). Crossbow users with RANGED on are exempt from that range.
- A medic on HOLD treats only themselves and does not walk to others (wiki); HOLD also switches RESCUE off for that character.
- HOLD counts as off while the character is sneaking (code analysis); patch notes say only that it does not break stealth.
- Uses: keeping crossbow users, a medic or workers in place, stopping the wounded from rejoining a fight, guarding a doorway.
- HOLD replaced the old PASSIVE button in one patch; PASSIVE was later added back, so both exist in 1.0.

## PASSIVE button
Also: passive mode, non-combat mode, do not attack, self-defence only, pacifist
- On: the character does not attack on sight and does not join allies' fights. The button's text calls it non-combat mode: no fighting unless attacked first.
- Attacked, the character still defends and fights back, so PASSIVE does not end a fight already started.
- Enemies choosing a target rate a PASSIVE character a little lower (code analysis).
- Use it to keep a character out of trouble in town, where joining a fight can become a crime, and for a hidden medic, workers, or traders passing hostile-looking groups.
- When the whole squad is down, PASSIVE plus SNEAK keeps characters who wake from standing up and restarting the fight (wiki).
- PASSIVE does not stop a character you directly order to attack (unverified)

## JOBS button
Also: jobs toggle, disable jobs, stop working, automation toggle
- On (the default): the character works through their jobs list (mining, hauling, crafting) from the top.
- Off: no automated work, and the rows in the jobs list are dimmed. Use it away from base so characters do not try to run home to their jobs, or when a worker must stay put or follow closely.
- First-aid jobs (Medic, Robotics) keep running with JOBS off.
- Follow and bodyguard jobs also keep running with JOBS off (patch notes).
- JOBS replaced an older "chase" button; 1.0 has no chase toggle.
- Turning JOBS off does not delete the jobs list; turning it on resumes it.

## RANGED button
Also: ranged mode, crossbow toggle, use ranged weapons, shoot
- On (the default): the character uses a crossbow if one is equipped and the right bolts are in the inventory, and fires turrets.
- Off: crossbows, Mounted Crossbows and Harpoon Turrets are not used; the character fights in melee with the other weapon.
- Characters have two weapon slots; the crossbow is only drawn while RANGED is on.
- Turn it off to stop friendly fire into a melee.

## TAUNT button
Also: taunt mode, draw aggro, threat, tank
- On: enemies choosing a target rate this character higher (+2 in their target score) and count the attackers it already has far less (x0.35), so they pile onto it (code analysis).
- Not a guaranteed taunt: the enemy's current target and distance still count, and the wiki adds damage dealt, so enemies may still pick someone else.
- Use it on the best-armoured, highest-defence character, usually with BLOCK, to protect weaker ones.
- Never leave it on for a weak character.

## SNEAK button
Also: stealth mode, stealth button, crouch, hide
- On: the character tries to move in stealth.
- While on, two icons join the name tag above the character: an eye and a light meter (see "Stealth indicators").
- Success depends on light, skill, equipment weight, movement, wounds and line of sight. Switching it on does not hide a character from an enemy who is already alerted.
- A sneaking character who is not in a fight does not attack on sight or join allies' fights (code analysis).
- A character who wakes from a knockout with SNEAK on, or gets an order while playing dead with it on, crawls instead of standing; the health panel reads "Staying low" (see "Staying low" in Health and medical).
- Stealth state is saved with the game.
- Right-clicking a standing person while sneaking orders a stealth knockout, which counts as assault in towns.

## MEDIC button
Also: medic order, heal squad, first aid button, medic job, robotics job, auto heal
- Left-click: the selected characters at once look for wounded squad members nearby to treat.
- Shift+left-click: adds the permanent Medic job; it adds Robotics too when the squad has a Skeleton or someone carries a repair kit (code analysis).
- The healer needs a first aid kit in their inventory or worn backpack (a Skeleton Repair Kit for Skeletons and robot limbs).
- For the Robotics job on an organic character, keep the repair kit in the main inventory, not a bag, while assigning (wiki).
- Medic and Robotics jobs take priority over other jobs until removed from the jobs list.
- A medic job makes a character leave the "playing dead" pose to heal allies, where they can be attacked again.

## RESCUE button
Also: rescue order, rescue job, carry wounded to bed, auto carry to bed
- RESCUE is a command beside MEDIC on the orders panel (added in update 0.28).
- Left-click: the selected characters pick up wounded squad members and put them in a bed if one is available; players report they bandage first when carrying a kit.
- Shift+left-click adds Rescue to the jobs list as a permanent job (code analysis; a forum reply agrees).
- It does nothing while the rescuer is on HOLD or already carrying someone, and the carrier needs a working left arm (code analysis).
- One form of the behaviour acts only when it finds a usable bed (code analysis), so it fails with no free bed you may use nearby.
- It skips the dead, characters already in a bed or cage, and animals.
- Players report it works only when rescuer, patient and bed are fairly close (unverified); otherwise carry by hand.

## Movement speed buttons
Also: walk, jog, run, group speed, match slowest, movement icon
- An icon in the orders panel shows the mode, Walk, Jog, Run or Group, with an arrow on each side (code analysis). The wiki calls it "your character's movement icon at the bottom right".
- Each arrow steps one mode and wraps round; the change goes to every selected character. The icon shows the mode of one of them.
- Group makes the selected characters keep to the pace of the slowest (patch notes: "match the speed of your slowest character").
- Athletics trains at any speed, but moving faster than 80% of top run speed adds 50% (tooltip line "Full speed bonus: +50%"); encumbrance lowers the rate.
- The setting is saved per character (patch notes).
- Being hit can knock characters out of Group (unverified)
- R does not change speed: it is the stop key (wiki and code analysis), whatever one Steam guide says.

## Time controls and game speed
Also: pause button, speed buttons, fast forward, >>, >>>, F2, F3, F4
- Four buttons in the HUD band: pause, 1x, 2x and 5x (code analysis; a patch raised the >>> button from 3x to 5x).
- Keys: Space pauses and unpauses; F2 normal; F3 2x; F4 5x.
- A speed button or F2 to F4 sets that speed directly, also from a pause. Clicking the pause button while paused does nothing (code analysis).
- Space resumes at the speed that was running when Space last paused the game. After a pause made with the button, Space may do nothing: use F2.
- The active speed button is highlighted (patch notes).
- The game pauses itself while a conversation window is open, when the build menu opens, during character creation and while the area under the camera loads (code analysis).
- In build mode Space confirms the build instead of pausing.
- One game hour takes about 109 real seconds at 1x.

## How the game shows it is paused
Also: PAUSED text, pause indicator, is the game paused
- A panel reading PAUSED shows on the HUD while the game is stopped. The code analysis lists it among the main HUD's panels, and a well-known mod exists only to remove this "gigantic PAUSED panel".
- Where it sits: a forum helper says "at the top of the screen", so look top-centre first (unverified)
- The pause button in the time controls is highlighted while paused (patch notes say speed buttons are highlighted).
- Nothing in the world moves: characters, weather and the clock stop.
- You can still select, give orders, open windows and move the camera, which runs on real time.
- The game may have paused itself: see "Time controls and game speed".
- Opening the Escape menu also stops the game (unverified)
- An autosave can still happen once while paused.
- F7 hides the whole UI, including this panel.

## Clock and money
Also: time of day, day counter, Day, money total, cash
- The time and money panel in the HUD band reads "Money" with the total as c.1,234, "Day: N" and the time as HH:MM (code analysis).
- A new game starts on Day 1 at 10:00 (code analysis).
- Money is Cats, written with a "c." prefix.
- There is one shared total for your whole faction; it is not an item in anyone's inventory.
- Cats found as items (Cats, String of Cats) join the total when looted, or when right-clicked in your inventory.
- Expected place: toward the bottom-right, by the speed buttons (unverified)
- Zoom in before trusting the number.

## Window buttons on the HUD
Also: INV, STA, MAP, TCH, TEC, SQD, HLP, Build button, Floor, menu buttons
- Six small buttons open the main windows. Their labels in the game's layout file are INV, STA, MAP, TCH, SQD, HLP (code analysis); a 2018 guide writes the fourth as TEC.
- INV: inventory (key I). STA: character stats (C). MAP: world map (M). TCH: research (T). SQD: squad management (no key). HLP: the Tutorials window (F1).
- An old patch note puts the Help button "just below the map button"; a forum post puts SQD "down near the bottom right". Their place within the band is (unverified)
- "Build" button: a loading tip says "in the upper right of the GUI"; the wiki says "on the bottom right". Key: B.
- A "Floor N" readout with up and down arrows sets which building floor is shown (Page Up, Page Down).
- "Prospect" is in the orders panel, "in lower-right part of the screen" (wiki). No default key.
- If a hotkey fails, use these buttons.

## Jobs list and AI panel
Also: orders panel, job queue, AI options, goals, No jobs assigned
- The selected character's jobs are listed in the orders panel "in the bottom right" (patch notes).
- Rows are numbered, for example "1: Operating machine". An empty list reads "[No jobs assigned]" with the hint "To add jobs, hold shift key when giving an order" (code analysis).
- Jobs run from the top down; drag a row to reorder it.
- A red X at the right end of a row removes that job (code analysis).
- With JOBS off the list is kept and its rows are dimmed.
- Far from the outpost a job was given at, its text is shortened and the job is ignored.
- Faction-wide AI switches are on the AI tab of the Overview window: nine tick boxes (Heal Allies, Rescue Allies, Feed Animals, Share Food, Shoot first and others) and "Follow Formation": Random, Military or Caravan (code analysis).

## Overview window and its tabs
Also: management screen, tabbed window, MAP FACTION RESEARCH CRAFTING SQUADS DIALOGUE AI
- One large window holds seven tabs, in this order: MAP, FACTION, RESEARCH, CRAFTING, SQUADS, DIALOGUE, AI (code analysis).
- M opens it on MAP, T on RESEARCH, Y on CRAFTING. The MAP and TCH buttons do the same; SQD opens SQUADS.
- FACTION, DIALOGUE and AI have no default key: open the window with M and click the tab.
- DIALOGUE is the message log: speech bubbles, conversation lines, your replies and system messages.
- Escape closes it.

## Mouse cursor shapes and colours
Also: red cursor, green plus, padlock cursor, pointer, chance percent
- The pointer changes with what a right-click would do (code analysis): attack, talk, first aid, loot, lift a body, pick up or steal, use, mine, build, repair, door, lock, lockpick, knockout, "cannot walk there".
- Wiki cues: red over a hostile character; a green plus over a wounded one; a padlock over a locked door or container.
- No colour change over a person means neutral or friendly: a right-click talks if they have something to say and otherwise does nothing; attacking needs the hold menu.
- Over a lock, or over a person while sneaking, a percentage beside the pointer gives the chance, red when poor, green when good (code analysis).
- kenshi-link screenshots do not include the cursor, so you rarely see these cues. Rely on labels and on what happens after the click.
- A green marker shows where a move order landed, another while the camera rotates; both are on by default and can be turned off in the options.

## The right-click-hold action menu
Also: context menu, radial menu, hold right click, action list, options on target
- Hold the right mouse button on a character, body, building, door, bed, container or portrait. After 0.2 s (0.25 s on a portrait) a list opens with its top-left corner at the pointer: the target's name as a title, then one row per action (code analysis).
- The list exists only while the button is down. Releasing over a row gives that order; releasing anywhere else just closes it. A left-click on a row while the right button is still held also works. Escape does not close it.
- Player reports conflict ("hold right click and then click" against holding while you drag to the option); the code analysis supports holding.
- Rows that need a roll show the chance at the right: Pick Lock, Stealth KO, Kidnap.
- Shift held while choosing turns the order into a job.
- On cages, and on doors locked by someone else, it opens the moment the button goes down.

## Action menu entries
Also: context menu options, verbs, Attack Unprovoked, Talk To, Loot, Pick Up, Put in Bed
- Exact row labels, in the game's fixed (not alphabetical) order (code analysis).
- Hostile: Attack Target (that one only), Talk To, Attack All, Stealth KO.
- Neutral or friendly person: Talk To, Follow, Bodyguard, Attack Unprovoked, Pick Up, Stealth KO.
- Downed stranger: First Aid, Loot, Pick Up or Kidnap, Splint Injuries.
- Your own character: First Aid (Repairs for robots), Trade (opens both inventories), Stand Up, Follow, Bodyguard, Put Down, Pick Up.
- Bed: Sleep, or Put in Bed while carrying someone.
- Container: Loot, or Inventory on your own; locked: Pick Lock, Use Tools, Use Strength.
- Door: Open, Close, Lock, Unlock; someone else's locked door: Pick Lock, Smash, Use Tools, Use Strength.
- Buildings and machines: Build, Use, Repair, Dismantle, Training, Auto-Haul, Man Turret.
- Cage: Get in, Put in, Set Free. Prisoner: Escape. Shackles: Unlock Shackles.
- Entries depend on who is selected and the target's state. With everyone selected down it only says "Your selected character is unconscious".

## Item labels in the world
Also: Alt key, highlight items, item names, red item name, shop signs
- Hold Left Alt: every loose item nearby gets a name label, and building signs light up yellow (code analysis, from a player's report). Labels vanish when Alt is released.
- A red label means the item belongs to someone: taking it is theft. Others are white or tinted by item grade; the one under the pointer turns green.
- Wiki: picking a loose item up requires Alt held while clicking it.
- Code analysis: a plain right-click picks up an unowned item; on an owned one the character only walks over and the game says "Hold down the ALT key to steal items". With Alt held, a left-click on a label also picks it up.
- Shop counters and other people's locked doors give the same hint, or "...to pick the lock."
- Bodies and dropped backpacks are looted without Alt, and Alt does not highlight them (forum).
- Item tooltips say if an item is stolen and who from.

## Stealth indicators (eye and sun)
Also: sneak icons, blue eye, yellow eye, red eye, detection, arrows, light level
- With SNEAK on, two icons join the name tag above the character: a stealth icon (the eye) left of the name and a light-level icon (the sun) at its right end (code analysis).
- Blue eye: nobody nearby sees you.
- Yellow eye: someone is starting to notice you. Move to cover or stand still.
- Red eye: you have been spotted.
- Arrows by the character point toward each watcher: yellow for one who is noticing, red for one who has seen you. An arrow lingers about 4 s (code analysis).
- The light icon has seven steps from full light to dark. Darkness makes sneaking much easier.
- While sneaking, the knockout chance shows beside the pointer over a person.
- Stealth knockouts only work while unseen (players say the red eye blocks them) (unverified)

## Inventory window
Also: character inventory, I key, backpack grid, ARRANGE, OPEN BAG, Total Weight
- I opens and closes it, as does INV; one of your own living characters must be selected (code analysis).
- It opens near the top-left corner, titled with the character's name.
- Main grid: 8 columns by 10 rows; each item covers a block of cells (Copper 3x2, Sleeping Bag 5x3). Equipment slots sit beside it.
- Lines (code analysis): "Total Weight" as carried/capacity, a burden word (Weightless, Lightweight, Moderate, Heavy, Overloaded), "Disguise:", "Slave of:", "Looks like slave:". Capacity is Strength + 15 kg per the wiki and tooltip, 1.2 x Strength + 15 kg per the code analysis.
- Buttons: ARRANGE repacks the grid; OPEN BAG shows the worn backpack's grid in a window to the left; LIMBS opens the robot-limb slots (amputees only).
- A stack shows its count in the item's lower-right corner; items with charges (food, kits) carry a thin bar along their bottom edge.
- The pin button in the title bar keeps this window open while you select someone else.

## Moving items with the mouse
Also: drag item, shift click, transfer stack, drop item, right-click item, pick up item in inventory
- Left press on an item picks it up onto the pointer; release after dragging, or press again, to put it down. From a stack this takes one unit; hold Shift or Ctrl for the whole stack (code analysis).
- Put down on another item, the two swap. Released over a character or a squad portrait, it is given to them; over open ground it is dropped.
- Right-click: equips an item or takes it off; with another inventory open, moves one unit across (in a shop this buys or sells). Shift+right-click moves the whole stack.
- Right-click also reads a map item, learns a blueprint and turns Cats into money; it does not eat food.
- Double-click does nothing special (code analysis; one forum post says it trades).
- Stacks only form in containers and backpacks that allow stacking; identical food items merge unless stolen.
- Refusals show as messages: "No room for that item.", "Out of trading range." With no room, try ARRANGE.

## Loot and container windows
Also: looting window, chest, storage, body inventory, Lock state
- Looting a body or opening a container shows two windows side by side: your character's inventory and the target's. They open once your character arrives.
- Open it with a plain right-click on a downed stranger or a container, or with Loot in the action menu. On your own characters the entry is Trade (code analysis; the wiki says Loot); on your own storage, Inventory.
- Left-clicking a container shows "Lock state:", "Lock complexity:" and "Empty" in the info panel (code analysis; the wiki writes [EMPTY]). Locked containers always hold something.
- Left-clicking your own storage, bench or machine opens its window alone, at the lower left.
- Taking from a container that belongs to someone is theft, rolled against Thievery and how near the owner is; a failure reads "Got caught stealing."
- An ore deposit has its own small inventory, looted the same way.
- Close with Escape.

## Trade window
Also: shop window, buying, selling, vendor, barter, Money, Buyback, Fencing Item
- Opens from a shopkeeper's dialogue, at once, wherever the two are standing (code analysis).
- Your character's window is near the top-left; the trader's stock is directly to its right, titled with the trader's name: a square grid 18 cells wide with a scroll bar and a "Money:" line for the trader's cats.
- Right-click an item to buy or sell one unit (Shift for the stack), or drag it across.
- Money changes hands with each item; there is no basket or confirm step.
- Refusals: "You can't afford that.", "The shopkeeper can't afford that."
- Anything traded can be traded back at the same price until the window closes; its tooltip reads "Buyback".
- Selling stolen goods first asks "Fence it anyway?" under the title "Fencing Item", with the chance of being caught.
- Switching the selected character keeps the window open. If your inventory is not showing, press I (forum).
- Animals are bought in a separate window with tick boxes and CONFIRM.

## Price lines in item tooltips
Also: price tooltip, Value, Sell value, Avg. Price, Price mark-up, FENCING CHANCE, Stolen from
- Hovering an item opens its tooltip beside the inventory window, not at the pointer: name, "Value" (the trader's mark-up or discount in brackets), "Sell value", weight and details (code analysis).
- Trade goods add "Avg. Price" and, while trading, "Price mark-up N%": red when dear, green when cheap.
- Stolen items show "Stolen from:" and "FENCING CHANCE:", the chance of selling them back to the faction they came from: 20% + 0.42% per Thievery level.
- A trader's money is limited: read the "Money:" line in their window.
- Shopkeepers do not mind loot taken from their enemies.
- What sells for how much (25% for gear, half for stolen goods, 30% for faction uniforms) is in "Money basics: what sells for how much" in Making money.

## Dialogue window
Also: conversation, talk, reply options, speech bubble, dialogue log
- Two panels in the lower middle of the screen (code analysis): the other person's, about 25% to 73% across and 60% to 74% down, with portrait, name and line; under it yours, about 35% to 64% across and from 75% down to the bottom, with portrait, name, the replies and your money as "c. N".
- Left-click a reply. A lone "[...]" reply just continues their speech.
- The game is paused while the window is open and returns to its earlier speed when it closes (code analysis).
- Only replies whose conditions are met are listed. A reply's effects (payment, hiring) happen the moment it is clicked.
- A line that needs no answer opens no window: it is only a bubble over the speaker.
- Guards, tax collectors and bandits can start a conversation themselves.
- Past lines are kept on the DIALOGUE tab of the Overview window.
- Number keys also pick replies, per a forum post (unverified)

## Character stats window
Also: statistics, skills, C key, STA, attributes, XP
- C opens and closes it for the selected character, as does STA (code analysis).
- About 980 by 650 px at 1080p, titled with the character's name.
- Attributes at the top: Strength, Toughness, Dexterity, Perception.
- Four skill columns (code analysis, from a screenshot of the game): Weapons (Katanas, Sabres, Hackers, Heavy weapons, Blunt, Polearms); Combat (Melee attack, Melee defence, Dodge, Martial arts) over Ranged (Turrets, Crossbows, Precision shooting); Thievery (Stealth, Lockpicking, Thievery, Assassination) over Athletics (Athletics, Swimming); Sciences (Field medic, Engineer, Robotics, Science) over Trades (Weapon smith, Armour smith, Crossbow smith, Labouring, Farming, Cooking).
- Hover or click a skill: the bottom area shows "Stats Affected", "Ways To Train", a "Next Level" bar and a description.
- It shows derived values such as the KO point and marks stats changed by equipment; it updates while open.
- Close with Escape or C.

## Map window
Also: world map, M key, map markers, town colours, travel, zoom map
- M opens the map, the MAP tab of the Overview window. It starts zoomed right out, centred on where the camera is (code analysis; a community guide says on the selected character).
- Wheel: zoom toward the pointer. Left or middle drag: pan.
- Right-click a point: the selected characters walk to that exact point, and a green marker stands there for 3 s (code analysis; a forum post agrees).
- Zoomed right out, your characters' markers and all town names are hidden: zoom in a few notches.
- Colours (code analysis): your characters light blue, brighter when selected; allies, freed prisoners included, green; neutral pale grey; enemies red. An arrow marks the camera and its facing.
- Only discovered places are shown. Map items reveal more and are used up.
- Hovering an explored town shows its name, "Faction:", "Relations:" and residents.
- Your own outposts appear in your colour under their name.

## Build menu and build mode
Also: construction, B key, build button, placing buildings, ghost, Commands
- B or the Build button toggles build mode. Opening it pauses the game and closes inventory windows; the build window replaces the HUD panels along the bottom edge (code analysis). Patch notes speak of a confirm/cancel window at the top of the screen.
- Build window: categories, the buildings in one with a picture, "Materials cost:", "Estimated build time:", a Commands box, Confirm and Undo buttons, floor arrows.
- Categories: Buildings, Camping, Crafting, Defence, Farming, Food, Interior, Lights, Mining, Power, Storage, Tech, Training, Walls.
- The Commands box (code analysis): Place Building: Left-Click; Clear Building: Right-Click; Undo: Backspace; Cancel All: Esc; "Press [Confirm] when finished".
- Ghost colours: green allowed, red blocked, blue too close to a town or an interior item outside a building. A blocked placement says why.
- Placed buildings start as wireframes that need Building Materials and a builder.
- Without research only a Small Shack and camping items are offered. Interior items need a building you own.

## Research window
Also: technology page, tech tree, T key, TCH, research queue
- T opens the RESEARCH tab of the Overview window. Its caption reads "RESEARCH - LEVEL N (CURRENT RATE: x)": bench level and research speed (code analysis).
- With no bench it tells you to build a research bench and assign someone to it. Benches, tech levels and costs are in Research, crafting and building.
- A list of categories (Core, Crafting, Defence, Electrics, Farming, Industry, Smithing, Training), then one line per available technology with its time; dark red means it cannot start yet.
- Hover or click a line for details: "Cost:" items (green when the bench holds them, "[Paid]" once paid), "Requirements:", "Needs research bench level N", and what it unlocks.
- Paying puts it in the queue; a character must then work at the bench (forum for the paying step).
- Queue entries can be deleted from the list.

## Crafting queue window
Also: Y key, crafting list, production queue, QUEUE button, bench window
- Y opens the CRAFTING tab of the Overview window.
- It lists what your benches have queued. Hovering an entry shows "State:" ("In production...", "Out of resources", "Output full"), "ETA:", "-Current Smith:" and, for gear, "-Predicted Result:" and "-Critical Success Chance:" (code analysis).
- Left-clicking your own bench opens the bench's window: a "QUEUE..." button, Input slots and an Output slot with progress bars. An input reads "Empty!", "OK" or "Invalid item!"; an idle bench says "Nothing Queued" (code analysis).
- A character assigned to the bench works through the queue.
- The queue has a repeat option that is remembered (patch notes).
- Selecting a working character shows which skill is used and its effect on output.

## Factions window
Also: FACTION tab, relations list, reputation screen, contracts, rename faction
- It is the FACTION tab of the Overview window: press M, then click FACTION. It has no default key (code analysis; a forum post agrees).
- "Faction name" box: your faction's name. Click it, type and press Enter to rename; a name already in use is refused. Typing here disables hotkeys.
- One line per faction you have met: name, a number from -100 to 100 and a bar growing left below 0 or right above 0. The number is red below -30 and green above 60 (code analysis).
- 0 is neutral; allied factions let you use their private beds.
- "Information", on the right (wiki), lists Upcoming Events and contracts, such as "Bodyguard Contract" with "-Protecting:" and "-Expires in:".
- Only one bodyguard job is shown at a time (wiki).
- Becoming allied or losing an ally produces an on-screen notification.

## Squad management window
Also: SQD, squads, ADD SQUAD, dismiss character, move between squads, rename squad
- The SQUADS tab of the Overview window; the SQD button opens it (code analysis).
- One box per squad: an editable name (up to 32 characters), its size as "N/20", a DELETE button and its members' portraits.
- ADD SQUAD makes an empty squad. DELETE works only on an empty squad and never on the last one.
- Drag a portrait into another squad's box to move that character; a squad's first member is its leader. Boxes and portraits can be dragged to reorder.
- Drag a portrait onto the DISMISS area to dismiss; the game asks "Dismiss character 'X'?".
- Limits: 10 squads, 20 characters per squad, 30 characters in total.
- A new recruit joins the squad on show, or a new squad if that one is full.
- Squad membership matters: food in a worn backpack is shared within the squad, and MEDIC heals the character's own squad.

## Prospecting window
Also: prospect, Prospect button, Prospecting Results, resource survey
- The Prospect button makes the selected character survey the area; a higher Science skill covers a larger area.
- The results window opens mid-screen, titled "Prospecting Results" (code analysis).
- It shows: Zone, Altitude, Prospector Skill, Area Size, Wind Speed, Environment (soil types), and Resources.
- Resource rows: Water, Fertility, Stone, Iron, Copper. Click a row to show that resource on the small map.
- The map marks iron and copper outcrops you can mine by hand.
- Use it to find the nearest ore deposit to a town.
- At 1080p the numbers can be hidden behind the map image; Alt+Enter twice is the wiki's workaround, but kenshi-link blocks Alt+Enter, so ask the operator.

## Info panel for buildings, beds and containers
Also: BUY button, For sale, building info, rental price, Cost to use, selected object
- Left-click an object to see its details where a character's would be: name on the left, owning faction on the right, then "Type:" and "Town:" (code analysis).
- A house is selected through its door: "Open/Close:" and "Security:" (Locked or Unlocked, with lock level); on your own doors both are buttons.
- Building for sale: a "For sale:" line whose button shows the price, c.N; clicking it asks "Do you want to buy this building for c.N?" (code analysis). A loading tip calls it a BUY button "in the bottom left of the screen".
- Bed: "Cost to use:" reads "Pay c.N" or "Private"; "Healing bonus:" gives its rate.
- Container: "Lock state:", "Lock complexity:" and "Empty".
- Ore and machines: "Iron Quality:" or "Copper Quality:", "Workers: N/M", "Efficiency:".
- The health area shows "Building Condition" and materials delivered against needed (an older wiki page places this bottom right).
- Your own buildings add buttons: power on/off, [UPGRADE], [DOWNGRADE], Dismantle (asks first), PAUSE CONSTRUCTION.

## Main menu
Also: title screen, Continue, New Game, Load Game, Exit
- Buttons, in capitals: CONTINUE, NEW GAME, LOAD GAME, IMPORT GAME, OPTIONS, CREDITS, EXIT (code analysis; the wiki gives the same order). The version text reads "Kenshi 1.0.68 - x64 (Newland)".
- CONTINUE loads the last save written, quicksaves and autosaves included; it is absent when that save is gone.
- NEW GAME opens "Choose your beginning". It never deletes existing saves.
- LOAD GAME and IMPORT GAME open their windows beside the buttons, which stay clickable.
- EXIT asks "Are you sure you want to exit?" with YES and CANCEL. kenshi-link cannot restart the game.
- Do not press Escape here: with no window open it quits the game without asking (code analysis).
- In message boxes Enter presses the first button and Escape the last.
- Position and look of the buttons: (unverified)

## In-game menu (Escape)
Also: pause menu, Esc, save game, quit, RESUME
- The first Escape press closes all open windows; pressing it again with none open brings up the menu (patch notes).
- Buttons (code analysis): NEW GAME, SAVE GAME, LOAD GAME, OPTIONS, EXIT GAME, RESUME.
- RESUME or Escape closes it.
- While it is open, game hotkeys are ignored (code analysis).
- There is no "return to main menu" without leaving the game, by player report (unverified)
- The game is paused while the menu is open (unverified)
- If windows keep disappearing when you only meant to close one, that is expected: Escape closes them all at once.

## Save and load windows
Also: save game, load game, quicksave, autosave, save slot, delete save
- Titled "Save game" and "Load game"; in play they open in the middle of the screen (code analysis).
- A list of saves with "Name" and "Date" columns, newest first.
- Click a save to select it; an info box then shows Date, File version, Faction name, Funds, Members size, Location and Day.
- Save window: a name box and SAVE; an existing name asks "Overwrite save X?". CANCEL closes.
- Load window: LOAD and CANCEL, plus a "Reset squad positions" tick.
- To delete a save, select it and press Delete or Backspace, then confirm; there is no delete button. The save in use cannot be deleted.
- F5 writes the slot named "quicksave"; F9 loads it. Autosaves are autosave0 to autosave2; the options set their interval or switch them off.
- Loading shows the loading screen and discards unsaved progress.
- An option stores saves in the user folder instead of the install folder.

## Import game
Also: import save, reset squad positions, refresh world
- IMPORT GAME, on the main menu, loads a save into a rebuilt world. Use it after updates or when NPCs or shops have gone missing.
- Ticks: Import Buildings, Import Research, Import Dead NPCs and Import Relations (the wiki puts them in an "Advanced" area), on by default, and "Reset squad positions", off by default (code analysis).
- Unchecking Import Dead NPCs brings dead unique characters back; unchecking Import Relations resets faction relations to their defaults.
- "Reset squad positions" recovers characters lost "in the void" (patch notes).
- Emptied bars only get new recruits after an import.
- Importing keeps the clock, money, faction name, discovered towns and your squads.

## New game: Choose Your Beginning
Also: start a new game, game start list, advanced options, BEGIN
- NEW GAME opens the window "Choose your beginning" in the right half of the screen.
- It shows one start at a time: its name, "Difficulty:", "Cash:", "Play Style:" and a description. Arrows step through the starts and wrap round; the first shown is Wanderer (code analysis). The wiki counts 13 starts.
- "Wanderer" is the intended default: one character in The Hub with c.1,000.
- Buttons: ADVANCED OPTIONS, BEGIN, CANCEL.
- ADVANCED OPTIONS opens a panel of difficulty sliders; hovering one explains it at the bottom. Defaults are fine.
- BEGIN leads to character creation.
- Starts marked with an asterisk on the wiki restrict the race you may pick.
- Details of each start are in the game-starts reference.

## Character creation screen
Also: character customization, character editor, race, appearance, name, CONFIRM, RANDOMISE
- Appears after BEGIN, after hiring some recruits, and for c.200 at a Plastic Surgeon in a bar. The game is paused while it is open.
- Controls, in capitals (code analysis): RACE, SUBRACE and GENDER with arrows; tabs BODY, FACE and HAIR, each a list of sliders; RANDOMISE (the open tab), RANDOMISE ALL, RESET; CLOTHES; IMPORT, EXPORT; CHANGE CHARACTER with arrows and a count such as "1/1"; CONFIRM.
- Name: click the name box and type, 30 characters at most. It is the only place a character can be renamed.
- One screen serves all starting characters: step through them with CHANGE CHARACTER, then press CONFIRM once.
- CONFIRM closes the screen, possibly through a loading screen, and sets the game running at normal speed, so pause straight away (code analysis).
- There is no cancel or back button; Escape opens the game menu over the screen.
- For recruits and surgery the race, subrace and gender arrows are hidden.

## Loading screen
Also: loading, tips, stuck loading, loading bar
- Shown after creating a game, loading or importing: a picture, the word LOADING with up to three dots, and a gameplay tip.
- A thin progress bar in the top-right corner shows background loading; it can also appear during play (code analysis).
- Loading can take a long time; wait and observe again.
- When the camera or squad moves far, the game holds itself paused until the area under the camera has loaded (code analysis; players report the same).
- Check the PAUSED panel after every load: a loaded game may or may not start paused (unverified)

## Options menu
Also: settings, font size, graphics, audio, mods tab
- Tabs (code analysis): General, Gameplay, Graphics, Audio, Controls, and a list of active mods. Changes apply as you make them; Close or Escape shuts the window.
- General: Tutorials, User Save Location, Auto save, Show character names, Show movement marker, Show rotation marker, Edge scrolling, Language censorship, Show damage floaters, Font Size, Fast zone hopping.
- Gameplay: Squad size multiplier, Difficulty settings, Town attacks frequency, Dismemberment. Patch notes name limb loss (default "rare"), hunger time, raid size and squad sizes as difficulty options.
- Controls: Invert mouse X and Y, Swap mouse buttons, Hardware Mouse, camera speeds, then the key bindings.
- Font Size is a slider from -10 to 32. Default 3 per the code analysis; the wiki says patch 1.0.62 changed it from 0 to 4.
- Most graphics changes need a restart; resolution, anti-aliasing and fullscreen mode are also in the launcher.
- Options have tooltips.

## Rebinding keys (Options, Controls)
Also: key bindings, keybinds, reset keys, unbound actions, hotkey setup, controls.cfg
- The Controls tab lists every action and its key. Click a line, then press the new key or mouse button; Escape cancels. A key already in use swaps with the other action (code analysis).
- The Defaults button puts every binding back and changes nothing else.
- Bindings are stored in controls.cfg in the game folder; an action missing from that file keeps its default (code analysis).
- No default key: the JOBS toggle, Prospect, the FACTION tab.
- Patch 1.0.60 added default keybinds for controller setups that apply only after pressing reset.
- If "select" is unbound from the left mouse button, dialogue replies cannot be clicked (forum).
- The operator mirrors any changed keys in kenshi-link's keymap; a named hotkey that opens the wrong thing means the two disagree.

## Options that affect display and control
Also: borderless, windowed, fullscreen, invert mouse, swap mouse buttons, markers, edge scrolling
- Display mode: fullscreen, windowed or borderless, set in the launcher or with "Full Screen" and "Border" in the options. kenshi-link needs windowed or borderless.
- At low resolutions some windows have gone partly off screen (patch notes).
- Edge scrolling (General, on by default): the camera pans whenever the pointer is within 1% of a screen edge, even over the HUD (code analysis). Switching it off stops that drift.
- Font Size: larger text reads better in screenshots but enlarges panels; some windows misbehave at large sizes.
- Swap mouse buttons, for left-handed play. If right-click selects instead of ordering, this is on.
- Invert mouse Y is on by default (code analysis).
- Show movement marker, Show rotation marker and Show character names are on by default.
- Alt+Enter toggles fullscreen but is blocked by kenshi-link.

## Default keys: general
Also: hotkeys, keyboard shortcuts, key bindings, controls list
- 1 to 9 and 0: select the 1st to 10th member of the squad on show. Pressed twice within half a second, the camera centres on them. With Shift the member is added to, or taken out of, the selection (code analysis).
- ] and [: select the next or previous member of the squad (code analysis).
- ` (backtick): select everyone in the squad on show. The wiki also lists - and +.
- Tab: show the next squad.
- Space: pause and unpause. F2: normal speed. F3: 2x. F4: 5x.
- F5: quick save. F9: quick load.
- F1: Tutorials window. F7: hide or show the whole UI. F8 or Print Screen: screenshot.
- R: stop the selected characters.
- Left Alt (held): show item labels; needed to steal.
- Escape: close all windows, then open the menu.
- Hotkeys do nothing while a text box has the keyboard.

## Default keys: windows
Also: menu shortcuts, inventory key, map key, stats key
- I: Character Inventory. C: Character Stats. Each opens and closes its window (code analysis).
- M: Map. T: Technology (research). Y: Crafting Queue. These open the Overview window on that tab.
- B: toggle build mode.
- A second press of M, T or Y is expected to close the window: the game names these actions toggle_map, toggle_research and toggle_crafting (unverified)
- No default key: squad management, factions, prospect, JOBS.
- These match kenshi-link's default keymap (inventory i, map m, stats c, research t, crafting y, build_mode b).

## Default keys: camera
Also: camera controls, pan, rotate, zoom, tilt, edge scroll
- W A S D or the arrow keys: move the camera. Q and E: rotate.
- , (comma) and . (period): tilt (code analysis; not in the wiki's list).
- Home: zoom in. End: zoom out.
- Mouse wheel: zoom (code analysis). It does nothing while the pointer is over a HUD panel or window.
- Hold the middle mouse button, or Left Ctrl, and move the mouse: rotate and tilt.
- F: "rotate camera down" on the wiki; the code analysis says it jumps the camera to the first selected character.
- Pointer within 1% of a screen edge: the camera pans that way (Edge scrolling option). A pointer left on the outermost pixels after a click keeps the camera drifting.
- ; (semicolon): toggles the free camera added in 1.0.67. Avoid it; press ; again if the camera behaves oddly.
- The camera moves while the game is paused.

## Default keys: build mode
Also: rotate building, place building, undo building, floors
- B: toggle build mode.
- Left-click: place the building. Right-click: clear the building in hand.
- Space: confirm. It does not pause while build mode is open.
- Escape: cancel everything placed and leave build mode (code analysis).
- Backspace: undo the last building placed.
- Page Up / Page Down: move up or down one floor.
- , (comma): rotate the building left. . (period): rotate right.
- = : move the building up. - : move it down.
- ] : increase slope. [ : decrease slope.
- The wiki lists "-" for both moving down and decreasing slope; treat the slope keys as [ and ].
- Pressing a speed button leaves build mode (patch notes).

## Default keys: tools and debug
Also: editor, navmesh, stuck characters
- Shift+F12: toggle the in-game editor. Do not use it; kenshi-link blocks it unless the operator allows debug keys.
- Ctrl+Shift+F11: rebuild the navmesh. The developers recommend it when characters are stuck inside structures or furniture has vanished after loading. It is a debug shortcut and is blocked by default.
- Ctrl+F6: reload biome data, a developer tool (code analysis). Leave it alone.
- Alt+Enter: toggle fullscreen; blocked.

## Mouse controls
Also: left click, right click, hold right click, box select, edge scroll
- Left-click a character or portrait: select. Left-click an object or a stranger: show its info without losing your selection.
- Shift+left-click: add to the selection, or take out one already in it.
- Left-drag on the world: selection box.
- Right-click the ground: selected characters move there.
- Right-click a target: its default action. With a character under the pointer the click never becomes a move order (code analysis).
- Right button held 0.2 s on a target, 0.25 s on a portrait: the action menu, open only while held.
- Shift with an order: make it a permanent job.
- Quick right-click or double-left-click on a portrait: centre the camera on them.
- Middle button held: rotate the camera. Wheel: zoom.
- On the map, right-click sends characters. In build mode, left-click places (the game's Commands text; an old patch note has the buttons swapped).
- Mouse buttons 4 and 5 are not used (patch notes).

## Keys where sources disagree
Also: conflicting bindings, R key, F key, speed multipliers
- R: the wiki ("Stop Character Action", "cancel your action (R)") and the code analysis (a stop action bound to R) agree; DefKey's "Rotate camera up" and a Steam guide's "cycles movement speed" look wrong.
- F: the wiki and DefKey say the camera rotates down; the code analysis says F centres the camera on the first selected character, with tilt on comma and period. Test once.
- F3 and F4: 2x and 5x (wiki, patch notes, code analysis); DefKey only says "faster" and "fastest".
- Select all: the wiki gives "`/~ or -/+", the code analysis only `. kenshi-link sends backtick.
- Jobs: most sources say Shift+right-click; one wiki page says "shift-left-clicking the deposit".
- Also disputed, each in its own section: the research button's label, the Font Size default, whether Alt is needed for unowned items.
- Tab: "cycle squads" (wiki), "toggle squads" (one guide); same key.

## Messages, tutorial and logs
Also: notifications, event messages, tutorial bubbles, help window, region name
- Event messages such as "Discovered X" or "Building purchased!" show one at a time on a strip just above the HUD, about 32% to 68% across and 71% to 78% down, for 4 s each (code analysis). They are also kept on the DIALOGUE tab.
- Characters announce things in speech above their heads ("This isn't mine").
- Entering a new region shows its name in large text about a third of the way down the screen for some 5 s.
- Tutorial lines pile up at the top-left; clicking one opens the tutorial window there, with DISMISS and FINISH. F1 or HLP lists all tutorials.
- Faction changes and raid announcements appear as on-screen notices; a raid announcement can snap the camera to the location once.
- Floating damage numbers, an option, are red when your character is hit, green when yours lands a blow, grey otherwise (code analysis).
- "Committing Crime!" and "Escaped Prisoner" show in the selection panel's status line.

## Progress bars: lockpicking and stealing
Also: lockpick bar, steal chance, theft timer, percentage
- Lockpicking shows a bar filling left to right. At the end of each cycle the character has the percentage shown in the bar as their chance to succeed; then it repeats.
- The same chance shows beside the pointer over the lock and next to Pick Lock in the action menu (code analysis).
- Maximum chance 90%. Below 5% the character refuses and says their skill is too low.
- Stealing from a container has a success chance based on Thievery and how close the owner is.
- After a successful theft, a countdown shows at the bottom left above the character's name; being seen before it ends still gets you caught.
- You remain a criminal for 3 seconds after stopping a lockpick attempt.

## Hiding and restoring the UI
Also: F7, cinematic mode, HUD disappeared, no interface
- F7 hides the entire UI for screenshots; F7 again shows it (code analysis: one switch for the whole GUI).
- If the HUD is missing from a screenshot (no portraits, no buttons), F7 was probably pressed.
- With the UI hidden, the PAUSED panel, the expand-stats button and every other panel are hidden too.
- Hotkeys still work while the UI is hidden (unverified)
- kenshi-link has no named hotkey for F7; use press_key.

## Sources
- https://kenshi.fandom.com/wiki/Controls and https://kenshi.wiki/controls : every default key and mouse action.
- https://kenshi.fandom.com/wiki/Getting_Started : order buttons and their defaults, weapon slots, red cursor, ore deposits.
- https://kenshi.fandom.com/wiki/Changelog : official patch notes; Escape, speed buttons, HOLD/PASSIVE/JOBS history, RESCUE, item right-clicks, buy-back, map, build-mode window, saves, options, portraits.
- https://kenshi.fandom.com/wiki/Loading_Screen : in-game tips (MEDIC, Build and BUY buttons, Shift for jobs).
- https://kenshi.fandom.com/wiki/Guide_to_Health : health pane, bleeding arrows, hunger thresholds, first aid methods, Limbs button.
- https://kenshi.fandom.com/wiki/GlitchMaker%27s_General_Guide : health bar colours.
- https://kenshi.fandom.com/wiki/Jobs : jobs list rules.
- https://kenshi.fandom.com/wiki/Stealth , /Thievery , /Lockpicking : eye and sun icons, Alt to pick up, red names, theft timer, lockpick bar and formula.
- https://kenshi.fandom.com/wiki/Items , /Guide_to_Equipment , /Encumbrance , /Disguise , /Slavery : equipment slots, weapon slot rules, capacity, inventory indicators.
- https://kenshi.fandom.com/wiki/Main_Menu , /Options_Menu , /Character_Customization , /Game_Starts , /Guide_to_UI_and_Controls : menus, import options, creation screen, C for stats.
- https://kenshi.fandom.com/wiki/Construction , /Guide_to_Building_an_Outpost , /Technology , /Small_Research_Bench , /Prospecting , /Events , /Statistics , /Athletics , /Bounty , /Maps , /Playable_Characters , /Trade_Goods , /Dialogue_Structure_Overlook : their windows.
- https://github.com/VlcekM/meitouclient (MeitouClient, GPLv3: a third-party reimplementation whose research notes on the original 1.0.68 executable, controls.cfg and GUI layout files are the "code analysis" above; only its statements about the original game were used): docs/game/ui-screens.md (HUD panels, portraits, health rows, windows, menus, tooltips); docs/game/ui-input.md (default bindings, action menu, quick right-click, pointers, item labels); docs/game/game-loop.md (speeds, pause, clock); docs/game/dialogue.md (conversation window); docs/game/locks.md, economy.md, perception.md, buildings-production.md, ai-tasks.md (beds, trade, stealth icons, build menu, AI tab); docs/formats/camera.md, docs/formats/settings.md (camera, options); docs/characters.md (character editor).
- Web search summaries of Steam community guides and discussions (steamcommunity.com, steamsolo.com): TEC label, double-click trading, number keys in dialogue, position guesses. Not read directly; treated as unverified.
- https://www.nexusmods.com/kenshi/mods/1272 (via search summary): existence of the large PAUSED panel in the base game's main panel layout.
- https://defkey.com/kenshi-pc-shortcuts (via search summary): alternative reading of R, F3 and F4.
- https://github.com/VlcekM/meitouclient docs/game (combat.md, perception.md, carry-loot.md, ragdolls.md): HOLD, TAUNT, PASSIVE, BLOCK and RESCUE behaviour, Staying low.
