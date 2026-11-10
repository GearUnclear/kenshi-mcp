# How-to

Numbered mouse-and-keyboard procedures for the unmodded 1.0.x game (selecting, ordering, talking, trading, looting, healing, sleeping, carrying, mining, recruiting, stealth, travel, saving, building, research, new game), each step followed by what should appear on screen; "(code analysis)" marks facts from a third party's reading of the game's code and GUI files.

## Sending these inputs through kenshi-link
Also: tool calls, hold right click, modifiers, shift click, alt click, double click
- Plain right-click: click with button "right". Its press is too short to open the action menu, which needs 0.2 s.
- Action menu: the list is open only while the right button is down (code analysis), so click with hold_seconds opens it and closes it again with nothing chosen. Use menu_open on the target, read the list in the returned screenshot, then menu_choose on the wanted row or menu_cancel; see "Open the action menu on a target".
- Shift+right-click (job): click with button "right" and modifiers "shift".
- Alt+right-click (steal, lockpick): click with button "right" and modifiers "alt".
- Double-click: click with count 2.
- Box selection or moving an item: drag with button "left".
- Keys below are Kenshi's defaults; hotkey("inventory") and the other named hotkeys send whatever the operator has bound.
- Orders are accepted while paused, but walking, talking and picking things up only happen once time runs. After giving an order, advance a few seconds and look again.
- A window that should have opened but did not usually means the character has not arrived yet.

## Select one character
Also: choose character, pick squad member, click portrait
1. Left-click the character in the world, or left-click their portrait on the HUD. Expect: the bottom-left panel shows that character's name and health, and the portrait's border is highlighted.
2. Or press the number key for their portrait position in the squad on show: 1 for the first, up to 0 for the tenth.
3. Press the same number key again within half a second to centre the camera on them.
4. Or press ] or [ to step to the next or previous squad member (code analysis).
- Selection works while paused.
- Left-clicking an NPC or a building shows it in the bottom-left panel, but your own characters stay selected and still take orders (code analysis).
- A dead character of yours cannot be selected; clicking the body only inspects it.
- No source describes how a selected character is marked in the world; note it once you see it (unverified)

## Select several characters
Also: box select, multi-select, shift click, drag selection, select all
1. Left-click the first character or portrait.
2. Shift+left-click each further character or portrait. Expect: each is added; Shift+clicking one already selected takes it out (code analysis).
3. Or left-drag a box on the world around the characters and release. Expect: every one of your characters inside the box is selected.
4. Or press ` (backtick) to select everyone in the squad on show.
- Start a box drag on open ground, not on a HUD panel or on a character.
- HUD buttons are not triggered by the mouse-up that ends a box drag (patch notes).
- With several selected, an order goes to all of them; where only one can act (talk, loot, pick up), the nearest one goes (code analysis).
- The order buttons then show one character's state, not a summary, per a forum post (unverified)

## Switch squad or find a far-away character
Also: next squad, cycle squads, centre camera, jump to character, follow camera
1. Press Tab, or click a squad's tab by the portraits. Expect: the portrait area shows the next squad that has members; the selection does not change (code analysis).
2. Left-click a portrait to select that character.
3. Quick right-click or double-left-click the portrait, or press its number key twice. Expect: the camera jumps to that character, however far away.
4. After that jump the camera keeps following the character; panning ends the follow (code analysis).
- Number keys and ` act on the squad on show (code analysis).
- F jumps the camera to the first selected character, per the code analysis; the wiki lists F as a camera tilt key.
- Shift+Tab steps backwards through squads, per a forum post (unverified)

## Move characters
Also: walk to, move order, go there, right-click ground
1. Select the character or characters.
2. Right-click the ground where they should go. Expect: a green marker at that spot that fades in a second or two (option "Show movement marker", on by default).
3. Let time run. Expect: they travel there at the speed set by the movement icon (Walk, Jog, Run or Group).
- With several selected, the rest spread around the point (code analysis).
- With a character under the pointer the right-click is never a move: you get that character's default action or nothing (code analysis). Click clear ground.
- Right-clicking an object gives its default action instead of a move.
- A character lying down or playing dead gets up when given a move order.
- A new order replaces the current one. No source describes a way to queue several destinations.
- If nothing happens: nobody of yours is selected, a window is under the pointer, or the mouse buttons are swapped in the options.
- For long distances see "Travel using the map".

## Move carefully during a fight
Also: shift move, combat manoeuvre, reposition while fighting
1. Select a character who is in combat.
2. Shift+right-click the ground. Expect: they work their way to that position while still fighting and defending themselves (loading-screen tip).
- A plain right-click is an ordinary move order; the tip implies the character then stops defending while moving.
- To hold a line or doorway, move them there and switch HOLD on.
- To run away, plain right-click far off, set the movement icon to Run, and head for town guards.

## Default action of a plain right-click
Also: right click, default order, what does right-click do, quick click
- Ground: move there. A plain building: walk to it.
- Hostile character who is up: attack; your characters then fight that whole group (patch notes).
- Any downed character who is not yours, and your own dead: loot, which opens their inventory (code analysis).
- Friendly or neutral person with something to say: talk. With nothing to say: no action.
- Your own wounded character: first aid (green plus cursor; the wiki says any wounded character). Your own downed, unhurt character: pick up. The body your character carries: put down (code analysis).
- While sneaking, a standing stranger: a stealth knockout attempt.
- Bed: sleep. Machine, bench or ore deposit: operate. Unfinished building: build.
- Door: open or close. Container: open it.
- Cage while carrying someone: put them in (wiki).
- Loose item: pick up; owned items need Left Alt (the wiki says every loose item does).
- Someone else's locked door or shop counter: the character only walks there and the game says "Hold down the ALT key..."; use Alt+right-click.

## Getting things done without the action menu
Also: avoid hold menu, quick click alternatives, default order, buttons instead of menu
- These routes need no action menu and are quicker than menu_open and menu_choose (code analysis unless marked).
- Loot a body: plain right-click a downed stranger.
- Pick up your own downed character: plain right-click them once nothing is left to bandage. Put down: plain right-click the carried body.
- First aid: plain right-click a wounded squad member, or click MEDIC (wiki).
- Sleep: plain right-click the bed.
- Lockpick or steal: Alt+right-click the door, chest or shop counter.
- Escape a cage: Alt+right-click the cage your character is in.
- Share items within the squad: drag an item onto the other character's portrait (patch notes).
- Your own door, a building for sale, dismantling: left-click it and use the buttons in the info panel.
- Your own storage or bench: left-click it to open its window.
- Still menu-only: Attack Unprovoked, Attack Target, Follow, Bodyguard, Pick Up or Kidnap on strangers, Put in Bed, Repair of a ruin.

## Open the action menu on a target
Also: hold right click, context menu, more actions, radial menu
1. Select the character who should act.
2. Call menu_open on the target (character, portrait, body, building, door, bed, container). Expect: a screenshot with the list showing and the right button still held.
3. Call menu_choose on the wanted row, or menu_cancel to close the list without choosing. Expect: the order is given if the release lands on a row.
4. Check the character's "Goal:" line or jobs list to see which order was taken.
- The list's top-left corner is at the pointer: a title with the target's name, then the rows downward, ordered as in "Action menu entries" in the interface reference (code analysis).
- The button must rest on the target for 0.2 s (0.25 s on a portrait) before the list opens (code analysis); menu_open waits longer than that.
- If the screenshot shows no list, nothing opened: menu_cancel, then try a plain right-click or a different target.

## Does the action menu stay open after release
Also: menu vanished, menu disappears, release right button, drag to option
- No, according to the code analysis: the list is shown only while the right button is held, and letting go closes it wherever the pointer is. Letting go over a row is how you choose.
- A left-click on a row also works, but only while the right button is still down.
- One Steam answer agrees: "You have to hold the right-click as you drag the cursor to the menu option you want."
- Other player answers say "hold right click and then click" the entry, and patch notes say the menu on a locked door opens instantly on a right-click. Neither shows that it survives the release.
- So through kenshi-link a click with hold_seconds can never choose an entry; menu_open and menu_choose hold the button for you between calls.
- If a screenshot ever shows the list still open after a release, this install behaves differently: left-click the entry and record that in your notes.

## Give a standing job with Shift
Also: permanent job, assign work, shift right click, automate, job list
1. Select the worker.
2. Shift+right-click the work target: ore deposit, machine, crafting or research bench, farm, unfinished building, storage container, animal corpse, training dummy. Expect: a new numbered line in the jobs list at the bottom right.
3. Check that JOBS is lit for that character.
4. Let time run. Expect: they start the job and return to it after any one-off order.
- For an action that is not the default, hold Shift while choosing it in the action menu (community guide, code analysis).
- Shift+left-click MEDIC adds the Medic job; Shift+left-click RESCUE adds Rescue.
- Attack, bodyguard and follow can be made jobs the same way (patch notes). Bodyguard from the menu is always a job (code analysis).
- Shift on a storage container gives a hauling job; on an animal corpse, a gather-meat-and-skins job.
- One wiki page says shift-left-click for deposits; if Shift+right-click adds nothing, try that.

## Remove, reorder or pause jobs
Also: delete job, job priority, stop working, clear jobs
1. Select the character. Expect: their jobs are listed in the orders panel at the bottom right, numbered from 1; an empty list reads "[No jobs assigned]".
2. To change priority, drag a job up or down the list. The job dropped onto and everything below it move down.
3. To delete one, click the red X at the right end of its row (code analysis; a forum post agrees).
4. To pause all jobs without deleting them, click JOBS so it is unlit. Expect: the rows are dimmed.
- Jobs are tried from the top; if one cannot be done the next is tried, and a higher one is resumed when possible.
- Medic and turret jobs act whenever a target exists, wherever they sit in the list, and only stop when deleted.
- Becoming a slave wipes the list.
- Far from the outpost where they were given, work jobs are ignored.

## Stop what a character is doing
Also: cancel order, halt, stand still, R key
1. Select the character.
2. Press R. Expect: they stop (wiki: "Stop Character Action"; the code analysis finds a stop action bound to R).
3. Or right-click the ground next to them. Expect: the current action is dropped and they step there.
4. If they go back to work straight away, switch JOBS off.
5. If they keep running to fights, switch HOLD or PASSIVE on.
- A shortcut site and one Steam guide give R other meanings; two wiki pages and the code analysis outweigh them.
- A character in a bed stays there until another order replaces the sleep order (code analysis).

## Talk to someone and choose replies
Also: dialogue, conversation, speak to NPC, reply options
1. Select one character.
2. Right-click the person. Expect: your character walks over; then two panels in the lower middle of the screen, theirs with their line and yours below it with the replies.
3. Left-click a reply. Expect: the next line, or the panels close. A lone "[...]" just continues their speech.
4. Repeat until they close.
- The game pauses itself while the panels are open and returns to its earlier speed afterwards (code analysis): check the pause state after a conversation.
- If no panels appear, the person has nothing that needs an answer, or your character has not arrived. "Talk To" is also in the hold menu.
- Number keys also choose replies, per a forum post (unverified)
- Replies that are not available to you are simply not listed.
- A reply can cost money at once (hiring, bribes, services). Read it before clicking.
- Right-clicking a hostile attacks; right-clicking someone who is down loots them instead (code analysis).
- Speech bubbles over heads need no answer.

## Buy from a shop
Also: purchase, trader, shopkeeper, vendor, buy food, buy first aid kit
1. Select the character who will carry the goods.
2. Right-click the shopkeeper, usually standing behind or near the shop counter. Expect: the dialogue panels.
3. Choose the reply that asks to trade. Expect: the trade window opens at once: your inventory near the top-left, the trader's stock to its right.
4. If your inventory is not showing, press I.
5. Hover an item for its "Value", then right-click it or drag it into your grid. Shift+right-click takes the whole stack. Expect: the item moves and your cats drop.
6. Press Escape to close.
- Trading always goes through that reply: only the shopkeeper's own dialogue offers it (code analysis). Its wording differs by shop.
- Only the original shopkeeper trades; a guard standing in for one has no trade dialogue.
- Refusals: "No room for that item." (no free block of its size), "You can't afford that.", "Out of trading range." (too far away).
- A shopkeeper who has caught you stealing never trades with your faction again.

## Sell to a shop
Also: sell loot, sell ore, sell copper, selling items, get money
1. Open the trade window as for buying.
2. Hover your item to see its "Sell value".
3. Right-click the item in your own grid, or drag it into the trader's grid. Shift+right-click sells the whole stack. Expect: the item moves across and your cats rise.
4. Press Escape to close.
- Trade goods (ore, materials and most things that are not weapons or gear) sell at the full local value, within 30% of base. Copper base c.180, Raw Iron c.90.
- Weapons, armour and other gear sell for far less than they cost. Food sells at 50%.
- Stolen items sell at half, can be refused by the faction they came from, and first bring up a "Fencing Item" prompt asking "Fence it anyway?".
- Faction uniform pieces sell at 30% of the plain item's price and can be refused; use a trader of another faction.
- "The shopkeeper can't afford that." means the trader is out of money; the "Money:" line in their window shows what they have left (code analysis).

## Undo a purchase or sale
Also: buy back, refund, wrong item, mistake while trading
1. Keep the trade window open.
2. Move the item back the way it came: right-click it or drag it across. Expect: the same amount of cats is returned or taken; nothing is lost.
- Per the patch notes, anything just bought or sold can be traded back at the price it went for.
- The item's tooltip reads "Buyback" while this applies.
- Undo before closing: the refund ends when the trade window closes (code analysis, from a player's report).

## Loot a body
Also: looting, take items from corpse, search unconscious, scavenge
1. Select one of your characters.
2. Right-click the body of a downed stranger, or hold right-click on it and choose "Loot". Expect: after your character has walked over, your inventory and the body's side by side.
3. Right-click an item to take it, or drag it across. Shift+right-click takes a stack.
4. Press Escape to close.
- Equipped gear on the body can be taken too.
- Cats are added to your total automatically.
- Looting bandits, criminals and slaves is legal. Looting townspeople or guards is a crime if seen, and only counts once you actually take something.
- On your own squad a plain right-click differs: first aid if wounded, pick up if down and unhurt, loot only if dead (code analysis).
- You can loot while crawling.
- Too many corpses left around attract predators.

## Open a container or storage
Also: chest, barrel, storage box, take from container, put items in storage
1. Left-click the container. Expect: "Lock state:" and "Lock complexity:" in the info panel, and "Empty" (the wiki writes "[EMPTY]") if there is nothing inside.
2. With a character selected, right-click the container, or hold right-click and choose "Loot" ("Inventory" on your own). Expect: both inventories side by side once the character arrives.
3. Move items with right-click or by dragging.
4. Press Escape to close.
- Your own storage: a left-click alone opens its window, at the lower left (code analysis).
- A padlock cursor or "Lock state: Locked" means it is locked: see "Pick a lock".
- You may look inside unlocked containers freely; taking items that belong to someone is theft with a success chance.
- Shop counters: a plain right-click only brings "Hold down the ALT key to steal items"; Alt+right-click opens them (patch notes, code analysis).
- Your own storage boxes only accept the item type they are built for.

## Pick up an item from the ground
Also: take item, grab item, alt click, loose item, dropped item
1. Select a character.
2. Hold Left Alt. Expect: a name label on every loose item nearby. Red label: owned, so taking it is theft.
3. With Alt still held, right-click the item or its label. Expect: the character walks to it and it goes into their inventory.
- Alt+left-click on the label also works (forum, code analysis).
- The wiki says loose items cannot be picked up without Alt. The code analysis says a plain right-click takes unowned items and Alt is needed only for owned ones, where the game says "Hold down the ALT key to steal items". Holding Alt is safe either way.
- A dropped backpack: hold right-click on it without Alt and choose "Loot".
- An item will not be picked up if the inventory has no free block for it.
- Stealing loose items always succeeds, but being seen still makes it a crime.

## Equip a weapon, armour or backpack
Also: wear, wield, put on, equipment, change weapon
1. Select the character and press I. Expect: the inventory window near the top-left, with the grid and equipment slots.
2. Right-click the item in the grid. Expect: it jumps to its slot.
3. Or drag the item onto the slot: Weapon 1 (upper, the one used), Weapon 2, Belt, Head, Chest, Armour, Legs, Feet, Backpack.
4. To take something off, right-click it in its slot or drag it into the grid.
- Weapon 2 only fits weapons 1 cell high and up to 7 wide.
- A worn backpack has a second grid, shown with OPEN BAG, and lowers the weight of what is in it, usually with a combat penalty.
- Stolen faction uniforms worn in that faction's towns get you attacked.
- Robot limbs: click LIMBS first; amputees only.

## Give an item to another character or drop it
Also: transfer item, share items, drop on ground, trade between squad
1. Select the giver and press I.
2. Drag the item onto the receiver's portrait, or onto the receiver in the world. Expect: it moves to their inventory if they have room and are close by.
3. Or: hold right-click on the other character and choose "Trade" (code analysis; the wiki calls the entry "Loot"). Expect: both inventories open; move items with right-click or drag.
4. To drop an item, drag it out of the inventory window and release it over open ground (code analysis).
- A drag takes one unit from a stack; hold Shift or Ctrl while picking it up to take the whole stack (code analysis).
- Characters must be near each other to exchange items.
- Food kept in a worn backpack is shared with the squad automatically, so it need not be handed out.
- Dropped items stay in the world and are saved with the game.

## First aid on yourself
Also: bandage self, bandage yourself, heal myself, use first aid kit
1. Make sure the character has a first aid kit in their inventory or worn backpack.
2. Select the wounded character.
3. Right-click the character themselves (the cursor shows a green plus), or hold right-click on them or their portrait and choose "First Aid". Expect: a bandaging animation, then red bars turning yellow.
4. Let time run until it finishes.
- Alternative: click MEDIC with only that character selected.
- An unconscious character cannot treat themselves.
- Wounds are treated in the order Blood, Head, Chest, Stomach, Left Arm, Right Arm, Left Leg, Right Leg.
- The kit with the fewest charges left is used first; inventory before backpack.
- Skeletons and robot limbs need a Skeleton Repair Kit and the entry is "Repairs".
- Bandaging stops degeneration; real healing then needs time, ideally a bed.

## First aid on someone else
Also: heal ally, bandage friend, treat wounded, medic another character
1. Select the healer, who must carry a first aid kit.
2. Right-click the wounded squad member in the world (green plus cursor), or hold right-click on them or on their portrait and choose "First Aid"; a plain right-click on a portrait only centres the camera (wiki). For anyone else, use the hold menu. Expect: the healer walks over and bandages.
3. Let time run until the patient's red bars have turned yellow.
- A plain right-click on a downed stranger loots instead of healing (code analysis).
- Any downed character can be healed, friend or enemy; conscious enemies usually cannot.
- Healing someone gives a small relations gain with their faction and trains Field Medic.
- Low Field Medic is slow and burns through kits.
- With HOLD on, the first-aid job does not walk to patients; switch HOLD off if the healer does not move.
- Splints for limbs below 0 are a separate kit; the menu entry is "Splint Injuries".

## Keep the squad healed automatically
Also: medic job, auto heal, permanent medic, standing medic order
1. Select the character or characters who carry kits.
2. Left-click MEDIC. Expect: they treat every wounded squad member nearby now.
3. For a standing order, Shift+left-click MEDIC. Expect: a Medic job appears in their jobs list.
- The Medic job works even with JOBS switched off.
- It takes priority over other jobs whenever someone is hurt.
- Risk: a medic who is playing dead will stand up to heal allies and may be attacked again. When the whole squad is down and enemies are near, do not give medic orders; use PASSIVE and SNEAK and wait.
- A lone downed character with the job bandages themselves while still playing dead.

## Sleep in a bed
Also: rest, heal in bed, use bed, sleeping, get out of bed
1. Select the character.
2. Right-click the bed. Expect: the character walks over and lies down; "State:" reads Sleeping and their portrait fades.
3. Let time run, at high speed if the area is safe.
4. To get up, give any other order, such as a right-click on the ground: the sleep order lasts until another replaces it (code analysis).
- The hold menu's entry on a bed is "Sleep".
- A bed heals at 8 times the normal rate, a camp bed at 4 times; the bed's "Healing bonus:" line shows its rate. Blood returns twice as fast in either.
- Wounds do not worsen while in bed, but unbandaged cut damage does not heal either: bandage first.
- Hunger falls at one third of the normal rate.
- One sleeper per bed.
- "This isn't mine" means the bed is private: barracks, houses. Allies of the owning faction may use those.
- Beds in ruins and bandit hideouts can be used.

## Rent a bed
Also: bar bed, inn, pay for bed, rest in town, bed rental
1. Find beds for rent, normally in a bar; some bars show a bed on their sign (forum).
2. Left-click a bed. Expect: "Cost to use:" in the info panel, reading "Pay c.N" for a bed to rent or "Private" (code analysis).
3. Select your character and right-click the bed. Expect: no prompt; the money is taken with the message "Paid c.N for bed rental." and the character lies down (code analysis).
4. There is no need to talk to the barman (forum).
- "Can't afford c.N for bed rental." means too few cats; the character does not lie down.
- Paying covers that bed for 24 game hours, so a healed character can get up and let a wounded one use it.
- Prices start around c.50 (wiki); the code analysis shows c.100 in bars. Skeleton repair beds cost c.200 to c.3,000. Allied factions' beds are free.
- A carrier laying someone in a rented bed pays (code analysis); players report no charge for an incapacitated character.
- Many minor outposts have no beds for rent.

## Make a camp bed from a sleeping bag
Also: sleeping bag, camping, rest in the wild
1. Have a Sleeping Bag in the character's inventory (5x3 cells, 5 kg; sold in travel shops).
2. Press B. Expect: the build menu; the game pauses itself.
3. Choose Camp Bed in the camping category. Expect: a ghost of the bed at the pointer.
4. Left-click to place it on green ground outside town borders, or inside a building you own, and confirm.
5. Select the character and right-click the camp bed to sleep. If it shows as an unfinished wireframe, right-click it once first so the character builds it (unverified)
6. When done, dismantle it to get the Sleeping Bag back.
- Heals at 4 times the normal rate.
- Placing a camp bed does not found an outpost.
- Remember Space confirms build mode; leave build mode before pausing with Space.

## Carry a downed character
Also: pick up body, carry wounded, rescue ally, carry unconscious
1. Select a healthy humanoid character. Animals cannot carry.
2. Your own downed character with nothing left to bandage: plain right-click them (code analysis). Anyone else: hold right-click on them and choose "Pick Up". Expect: your character walks over and lifts them.
3. Right-click the ground to walk; the carried character comes along.
4. To set them down, plain right-click the carried body, or choose "Put Down" in the menu on the carrier or on the carried character's portrait.
- Carrying adds 30 kg to encumbrance, so the carrier slows; it trains Strength.
- The carrier needs a working left arm (code analysis).
- If "Pick Up" is missing, check that the right character is selected and is not already carrying someone; if they wrongly count as carrying, use "Put Down" first.
- Picking up townspeople is kidnapping, a serious crime; the entry then reads "Kidnap". Carrying your own people or bandits is not.
- A carrier can still be attacked; put the body down before fighting.

## Put a carried character in a bed
Also: lay in bed, place in bed, rescue to bed, put in bed, heal unconscious ally
1. Carry the character as above.
2. With the carrier selected, hold right-click on a free bed and choose "Put in Bed". Expect: the carrier walks over and lays them down.
3. Check the patient's health pane; bandage any red bars.
- Players describe a plain right-click on the bed doing the same; the code analysis finds a plain right-click gives the sleep order even while carrying. The menu entry works either way.
- The bed must be one you may use: rented, free, or your own.
- In a bed, wounds stop getting worse at once and healing runs at the bed's rate. An unconscious patient stays until they wake; a conscious one gets up when ordered.
- Putting an incapacitated NPC in a bed can raise relations with their faction.
- With a cage, a plain right-click while carrying puts the captive in; the menu entry is "Put in".
- To automate it, select helpers and click RESCUE (see "RESCUE button" in Interface).

## Mine ore
Also: mining, mine copper, mine iron, ore deposit, resource node
1. Find a deposit. The Prospect button's result map marks iron and copper outcrops near the character.
2. Left-click the deposit to check it: the info panel shows "Iron Quality:" or "Copper Quality:" and "Workers: N/M" (code analysis).
3. Select the miner and right-click the deposit. Expect: they walk to it and start working; a progress meter fills (community guide).
4. For continuous mining, Shift+right-click the deposit instead. Expect: a mining job in the jobs list.
5. Let time run. Expect: ore accumulates inside the deposit, not in the miner's inventory (wiki, forum).
- A deposit holds 5 pieces; then work stops until it is emptied.
- One to three miners fit a deposit, depending on its size.
- Mining trains Labouring, and a higher skill mines faster.
- Copper is worth twice as much as Raw Iron and weighs less than half (4 kg against 9 kg).
- Deposits are out in the open; watch for animals and bandits.

## Collect ore from the deposit
Also: take ore, empty deposit, ore not in inventory
1. Select the miner standing at the deposit.
2. Hold right-click on the deposit and choose "Loot". Or left-click the deposit and press I. Expect: the deposit's small inventory beside the miner's.
3. Shift+right-click the ore, or drag each piece across. Expect: it moves into the inventory or worn backpack.
4. Close with Escape. A miner with the job goes back to work now that the deposit has room.
- Each piece is 3x2 cells. Ordinary backpacks do not stack ore; Trader backpacks stack 6 and Wooden backpacks 9 per pile, and animal packs stack too.
- Watch "Total Weight" in the inventory window: base carry weight is Strength + 15 kg per the wiki and the Strength tooltip, 1.2 x Strength + 15 kg per a code-based reference checked in game.
- A heavy load trains Strength but slows the walk home.
- If attacked while loaded, drop the backpack or move it into the main inventory to shed its combat penalty.

## Haul ore to town and sell it
Also: sell copper, make money mining, first money, hauling
1. Fill the inventory and backpack as above.
2. Right-click the ground toward town, or use the map, and let time run in chunks.
3. In town, find a trader; the wiki says raw materials sell "at any store". Trade goods shops are the surest.
4. Open the trade window and Shift+right-click the ore. Expect: cats rise by the local price for each piece.
- Copper's local price is between about c.126 and c.234 (base c.180, ±30%); Raw Iron between about c.63 and c.117.
- Markup differs by town and changes little between neighbouring towns.
- The wiki rates mining below most other ways of making money, but it is safe and trains Labouring and Strength.
- Buy food and a first aid kit before going back.

## Recruit at a bar
Also: hire, new squad member, recruit, join, companion
1. Have the hiring fee: generic recruits ask between c.3,000 and c.7,500; the plain "Recruit" asks c.3,000. Some unique characters join free.
2. Go into a bar. Recruits are usually inside; some patrol the town.
3. Select your character and right-click a likely person. Expect: a dialogue in which they offer to join for a price.
4. Choose the reply that pays. Expect: cats drop and they become your character at once.
5. If the character creation screen opens, adjust name and looks, then click CONFIRM. Expect: the screen closes and the game runs at normal speed (code analysis), so pause again.
6. Check that their portrait has appeared.
- There is no marker showing who is recruitable; you find out by talking.
- The recruit joins the squad on show, or a new squad if that one has 20 (code analysis). At 30 characters hiring is refused.
- New recruits are weak, poorly equipped and often hungry.
- An emptied bar does not get new recruits unless the save is imported.

## Hire mercenary bodyguards
Also: mercenaries, guards for hire, protection, bodyguard contract
1. Find a mercenary squad leader in a bar: a Mercenary Captain, or a Tech Hunter squad leader. Cannibal Hunter leaders also hire out.
2. Select your character and right-click the leader.
3. Choose the reply that hires them to guard you or your outpost. Expect: cats drop and the squad follows you.
- The wiki disagrees on price: its Mercenary Guild page says c.2,000 per day as bodyguards and c.1,000 per day as outpost guards; its Events page says c.1,000 per day (up to two days) as bodyguards and c.2,000 per two days (up to eight) for an outpost. Cannibal Hunters: c.3,000 per day.
- Time left shows on the FACTION tab of the Overview window (press M, click FACTION) as "Bodyguard Contract" with "-Expires in:".
- They are not under your control and leave when the contract ends.

## Pick a lock
Also: lockpicking, locked door, locked chest, unlock, padlock
1. Confirm it is locked: a padlock cursor, or "Lock state: Locked" or "Security: Locked" in the info panel.
2. Select the character.
3. Hold Left Alt and right-click the door or container. Or hold right-click on it and choose "Pick Lock" (the wiki writes "Lockpick"), which shows the chance beside it. Expect: the character walks over and a bar fills left to right.
4. Let time run. At the end of each fill there is a roll at the percentage shown in the bar; on failure it starts again.
5. When it succeeds, open the door or container as usual.
- Without Alt a right-click only walks there and shows "Hold down the ALT key to pick the lock."
- If the character says their skill is not high enough, the chance is below 5% and they will not try.
- Picking someone else's lock is a crime if seen, and for 3 seconds after you stop. Stop when someone looks.
- The wiki names no lockpick item; the skill alone is used.

## Lockpicking chance and alternatives
Also: lock level, lockpick formula, Tools, hacksaw, break lock
- Chance per cycle is 90 / 2^((lock level − Lockpicking) / 10) percent, capped at 90%.
- A level 100 lock needs Lockpicking 58 or more.
- −10 Lockpicking when picking your own cage.
- A success gives 5 times the experience of a failure, so easier locks train faster.
- Locks re-lock about once a day, per forum posts (unverified)
- Tools (an item, 3 kg, 3x2 cells, sold by trade goods traders) cut through a lock without the skill: slower, noisier, faster with more Strength, and the Tools must be in the main inventory, not a bag. A hacksaw works the same. The menu entries are "Use Tools" and "Use Strength" (code analysis).
- Opening a gate you unlocked and closing it again re-locks it, which is the usual way to practise.

## Sneak
Also: stealth, hide, crouch, avoid detection, sneak past
1. Select the character and click SNEAK so it is lit. Expect: an eye icon and a sun (light level) icon join the name tag above their head.
2. Move with right-click as usual. Sneaking is slow below Stealth 30.
3. Watch the eye. Blue: unseen. Yellow: someone is starting to notice; get behind cover or stand still. Red: spotted.
4. Watch for arrows by the character: each points at a watcher, yellow for noticing, red for seen (code analysis).
5. Watch the sun icon: dimmer means darker and safer.
6. Click SNEAK again to stand up.
- Easier at night, in dust storms and rain, when lightly loaded and unwounded.
- Closed doors muffle noise; sleeping people hear more.
- Careful where you right-click: on a standing person it orders a knockout attempt, which is assault.
- Stealth only trains near other characters, much faster near hostile ones.

## Steal an item
Also: theft, thievery, shoplifting, take owned item
1. Switch SNEAK on and wait for a blue eye.
2. Loose item with a red label: hold Left Alt and right-click it. It always succeeds, but being seen is still a crime.
3. Container: open it (Alt+right-click for a shop counter) and move the item to your inventory. Expect: a roll against a chance based on Thievery and how close the owner is; a failure reads "Got caught stealing."
4. Afterwards stay unseen until the timer at the bottom left, above the character's name, runs out.
- Stolen items are flagged in their tooltip and sell at half value; do not sell them to the faction they came from.
- Getting caught in a shop bans your whole faction from that shopkeeper for good.
- Shops lock up at night; staying inside after closing becomes trespassing.
- Practise on junk in houses before shops.

## Knock someone out from stealth
Also: stealth KO, stealth knockout, assassinate, knock out
1. Switch SNEAK on and get behind the target unseen.
2. Right-click the target, or hold right-click and choose "Stealth KO", which shows the chance beside it (code analysis). Expect: a strike; on success they drop unconscious.
- The chance also shows beside the pointer while it is over the target.
- Chance falls with the target's Toughness, Assassination, Thievery or Melee Defence, whichever counts most.
- Failed attempts give 3 times the experience but usually start a fight and count as assault.
- It does not work on animals. It works on sleeping people.
- A knocked-out person can be looted like a sleeper.
- The wiki advises against knocking out shopkeepers: a bug can empty the shop for good.
- Players say it fails while the eye is red (unverified)

## Travel using the map
Also: long distance, go to town, map travel, route
1. Select the travellers and set the movement icon to Run, or to Group to keep them together.
2. Press M. Expect: the world map, zoomed right out.
3. Scroll the wheel up over the area you want until your markers (light blue) and town names appear; left-drag to pan (code analysis).
4. Right-click the destination on the map. Expect: a green marker there for 3 s; after closing the map, the characters are heading that way.
5. Press M or Escape to close, then run time in chunks, checking for trouble.
- They go to the exact point clicked, even inside a private house, so click just outside the town gate (forum).
- The right button is the one that orders; the left only pans (code analysis).
- There is no fast travel in the unmodded game.
- Without the map: zoom the camera out and right-click the ground in the right direction, repeatedly.

## Pause, unpause and change speed
Also: stop time, speed up, fast forward, slow down
1. Press Space to pause. Expect: the PAUSED panel and a lit pause button.
2. Press Space again to resume, at the speed that was running when Space paused (code analysis).
3. Press F2 for normal, F3 for 2x, F4 for 5x, or click the matching button. Expect: that button lit; these also end a pause.
- Through kenshi-link use set_speed and advance instead of pressing these yourself, so its record of the pause state stays right.
- The game pauses itself when a conversation opens, when the build menu opens, in character creation and while a new area loads (code analysis). A Space press then un-pauses instead of pausing.
- Clicking the pause button while paused does nothing; after a pause made with that button, Space may do nothing either (code analysis). Use F2.
- In build mode Space confirms the build instead of pausing, and speed buttons close build mode.
- If the picture and the tool's belief disagree, the PAUSED panel decides.

## Quick save and quick load
Also: F5, F9, save now, reload
1. Press F5. Expect: the game saves to the slot named "quicksave", replacing the previous quicksave.
2. Press F9 to load that slot. Expect: the loading screen, then the game as it was at the last F5.
- F9 throws away everything since the save, without asking as far as sources say (unverified)
- Save before fights, thefts, lockpicking and long trips.
- After loading, check whether the game is paused before doing anything else.
- Autosaves are separate (autosave0 to autosave2) and run on the interval set in the options.
- CONTINUE on the main menu loads whichever save was written last, quicksave or autosave included (code analysis).

## Save to a named slot or load a save
Also: save game, load game, save window, new save, delete save
1. Press Escape until no windows are open, then once more. Expect: the game menu: NEW GAME, SAVE GAME, LOAD GAME, OPTIONS, EXIT GAME, RESUME.
2. Click SAVE GAME. Expect: the "Save game" window in the middle of the screen, with a list of saves ("Name", "Date") and a name box.
3. Click the name box, type a name and click SAVE. Expect: for a name that already exists, "Overwrite save X?" (code analysis).
4. To load, click LOAD GAME in the same menu or on the main menu, click a save in the list, then LOAD.
- Selecting a save shows its Date, Faction name, Funds, Location and Day.
- To delete a save, select it and press Delete or Backspace, then confirm; the one being played cannot be deleted.
- Typing only belongs in a focused text box; typed into the world, letters act as hotkeys and Space pauses.
- IMPORT GAME, on the main menu only, is for repairing a save, not for normal loading.

## Start a new game
Also: new game, main menu, choose your beginning, begin
1. On the main menu click NEW GAME. Expect: the window "Choose your beginning" in the right half of the screen.
2. It shows one start at a time, Wanderer first, with "Difficulty:", "Cash:", "Play Style:" and a description. Click its arrows to step through the starts (code analysis).
3. Leave ADVANCED OPTIONS at their defaults unless told otherwise.
4. Click BEGIN. Expect: the character creation screen.
5. Create each starting character and click CONFIRM. Expect: the world, on Day 1 at 10:00, running at normal speed (code analysis).
6. Pause at once, then observe and find your character.
- New Game never overwrites existing saves.
- There is no way back from character creation to the start list (forum).
- Never press Escape on the main menu itself: with no window open it quits the game (code analysis).
- Save once the game has started.

## Create your character
Also: character creation, customise, race choice, name character, CONFIRM
1. Choose RACE and SUBRACE with their arrows if the start allows it. Greenlander has no experience penalties and is the neutral pick.
2. Choose GENDER; use the BODY, FACE and HAIR tabs and their sliders, or RANDOMISE ALL, or leave the defaults.
3. Click the name box and type a name (30 characters at most).
4. With several starting characters, click the CHANGE CHARACTER arrows and repeat for each; the count reads like "1/2".
5. Click CONFIRM once for all of them. Expect: a question first if some characters were never shown; then the game runs at normal speed (code analysis).
- Race matters: only humans are safe in Holy Nation lands; Skeletons need no food but need repair kits; Hive cannot wear boots; Shek eat more.
- The game is paused while the screen is open.
- The same screen appears after hiring some recruits, without the race arrows; CONFIRM to continue.
- A character's name can only be changed on this screen.

## Build something
Also: build mode, place building, construction, shack, furniture
1. Put Building Materials (or the item the building needs) in a character's inventory.
2. Press B, or click Build. Expect: the build window along the bottom of the screen; the game pauses itself (code analysis).
3. Click a category, then the building. Expect: a ghost at the pointer.
4. Move it where it turns green. Red: blocked. Blue: too near a town, or an interior item outside a building.
5. Rotate with comma and period and left-click to place (the game's own text: "Place Building: Left-Click"). Right-click clears the building in hand.
6. Click Confirm or press Space, then B if the build window is still open. Expect: a wireframe where the building will be. Escape instead cancels everything placed.
7. Select builders and right-click the wireframe; Shift+right-click makes it a job. Expect: the condition bar fills as materials go in.
- Backspace undoes the last placement. A refused spot says why ("Too close to another building.").
- Materials can be brought in several trips.
- Outside towns only; interior items need a building you own.

## Buy a building in town
Also: purchase house, own building, BUY button, For sale, property
1. Left-click the building's door. Expect: its details in the bottom-left panel; if it is for sale, a "For sale:" line with a button showing the price, c.N (code analysis; a loading tip calls it a BUY button).
2. Click that button. Expect: "Do you want to buy this building for c.N?" with Yes and No.
3. Click Yes. Expect: cats drop and the message "Building purchased!"; without the money, "Can't afford to buy this building."
4. Ruined buildings need repair: hold right-click on the building and choose "Repair" with builders selected who carry Building Materials.
- A ruined building costs much less (code analysis).
- Purchases cannot be sold back.
- Owning a building lets you place interior items in town: bed, storage, research bench.
- You can lock your own doors with the "Security:" button in the door's info panel or from its action menu.

## Research a technology
Also: research bench, tech, technology, unlock buildings
1. Own a building: buy one in town or build a Small Shack outside.
2. In build mode place a Small Research Bench (interior, 3 Building Materials) and have it built.
3. Press T. Expect: the RESEARCH tab of the Overview window, captioned "RESEARCH - LEVEL N (CURRENT RATE: x)"; with no bench it tells you to build one.
4. Click a category, then a technology, to read its "Cost:" (usually Books) and "Requirements:". Have the items in the bench or the researcher's inventory, then start it. Expect: it joins the research queue (payment step from a forum post).
5. Select the researcher and Shift+right-click the bench. Expect: a research job; progress advances while they work.
- A technology shown in dark red cannot be started yet (code analysis).
- Science skill sets the speed; working in the dark is less efficient.
- First goals: Small House, then Tech Level 2, 8 Books in total, which unlocks the next bench.
- The small bench cannot be upgraded; later benches have an upgrade button.

## Attack someone
Also: fight, attack order, attack unprovoked, target enemy
1. Select your fighters and check that BLOCK and PASSIVE are not lit.
2. Hostile target: right-click it. Expect: they attack that enemy group.
3. To focus one particular enemy, hold right-click on it and choose "Attack Target".
4. Neutral or friendly target: hold right-click and choose "Attack Unprovoked".
- Menu labels are from the code analysis; "Attack All" is the whole-group order.
- Attacking in town is assault if seen and brings the guards.
- Anyone with a bounty can be attacked without legal trouble.
- New characters lose most fights; fight beside town guards when possible.
- Shift-clicking attack makes it a standing "attack enemies on sight" job.
- Crossbows are only used with RANGED lit and ammunition carried.

## After a knockout: stay down or get up
Also: knocked down, squad wiped, get up, stand up, wake up, play dead
- "Unconscious (N)": wait; no order wakes a character. A knockout ends when its timer runs out, unless a vital part is below the KO point ("Recovery coma": all vital parts must first be back above 0) or blood is at or below 0.
- "Playing dead...": the knockout is over, but a conscious enemy is sensed and no conscious ally is. A conscious ally nearby makes the character get up unasked.
- To stay down safely: switch PASSIVE and SNEAK on and give no medic or move orders.
- To get up: give any order, or choose "Stand Up" in the menu on the character. With SNEAK on they crawl ("Staying low") instead.
- An ordered get-up near enemies restarts the fight; it trains Toughness only when no conscious ally is near.
- A character with one leg below the KO point can only crawl; they can still loot.
- The rules: "Playing dead", "KO point and recovery coma" and "Leg down" in Health and medical.

## Escape from a cage or shackles
Also: break out of prison, jailbreak steps, unlock shackles, captured
1. Select the imprisoned character. Expect: "State:" reads "Locked (lvl: N)", or "(Unlocked...)" if the cage is open (code analysis).
2. Hold Left Alt and right-click the cage, or hold right-click on the character or their portrait and choose "Escape". Expect: lockpicking starts; they leave the cage when it succeeds.
3. Keep SNEAK on and wait for guards to look away or sleep.
- Lockpicking has a −10 penalty on your own cage.
- Shackles are removed by picking their lock ("Unlock Shackles") or with a saw.
- Getting into a cage yourself in a populated town does not hold you: the guards let you out.
- After escaping a slave camp, "Looks like slave:" in the inventory window shows how recognisable you are; change clothes and wait for it to fall to 1%.
- Escaped slaves should avoid towns for several game days.

## Close windows and get back to the world
Also: stuck in menu, close window, Escape, lost in windows
1. Press Escape once. Expect: every open window closes.
2. If the game menu appears instead, no window was open; press Escape again or click RESUME.
3. If you are in build mode, press B to leave it; Escape also leaves it but discards what was placed (code analysis).
4. If the HUD is missing entirely, press F7 to bring the UI back.
5. If the camera moves strangely, free camera mode may be on: press ; (semicolon).
- I and C close their own window when pressed again (code analysis). Whether M, T and Y do is (unverified)
- On the main menu, do not press Escape: with no window open it quits the game (code analysis).
- The wheel acts on whatever is under the pointer, so close windows before zooming the camera.
- After a load, a conversation or a visit to the build menu, check the PAUSED panel before giving orders.

## Sources
- https://kenshi.fandom.com/wiki/Controls and https://kenshi.wiki/controls : selection, box select, Shift, right-click, hold right-click menu, portraits, all keys.
- https://kenshi.fandom.com/wiki/Loading_Screen : in-game tips on Shift jobs, Shift move in combat, MEDIC, playing dead, BUY button, Build button, job reordering.
- https://kenshi.fandom.com/wiki/Changelog : patch notes on attack-group default, Pick up / Put down, Put in bed, buy-back, right-click and Shift+right-click on items, lockpicking via the menu, quicksave slot, Escape, build-mode confirm, RESCUE, markers, jobs.
- https://kenshi.fandom.com/wiki/Guide_to_Health , /Field_Medic , /Bed , /Camp_Bed , /Sleeping_Bag , /Skeleton_Repair_Bed : first aid methods and order, kits, bed rates, rental, camp beds.
- https://kenshi.fandom.com/wiki/Getting_Started : order buttons, collecting ore, looting law, shops, recruits, mercenaries, stealth and thievery practice.
- https://kenshi.fandom.com/wiki/Jobs : job list behaviour.
- https://kenshi.fandom.com/wiki/Money_Making_Strategies , /Copper , /Raw_Iron , /Trade_Goods , /Prospecting , /Labouring , /Encumbrance , /Strength : mining, deposit capacity, prices, weights, carrying weight.
- https://kenshi.fandom.com/wiki/Lockpicking , /Stealth , /Thievery , /Assassination , /Prisoner_Cage , /Slavery , /Backpacks : lockpicking steps and formula, eye and sun, Alt to steal, timer, knockouts, cages, escape, dropped backpacks.
- https://kenshi.fandom.com/wiki/Playable_Characters , /Generic_Recruits , /Recruit , /Bars , /Events , /Character_Customization : recruiting, fees, limits, mercenary prices, creation screen.
- https://kenshi.fandom.com/wiki/Construction , /Guide_to_Building_an_Outpost , /Player-Owned_Buildings_in_Town , /Small_Research_Bench , /Research_Bench , /Technology : building, buying, repairing, research.
- https://kenshi.fandom.com/wiki/Main_Menu , /Game_Starts : new game, Continue, Load, Import.
- https://kenshi.fandom.com/wiki/Dialogue_Structure_Overlook and /Dialogue_Conditions_%26_Effects : dialogue pop-up, replies, trade window opened from dialogue.
- https://github.com/VlcekM/meitouclient (MeitouClient, GPLv3: a third-party reimplementation whose research notes on the original 1.0.68 executable and GUI files are the "code analysis" above; only its statements about the original game were used): docs/game/ui-input.md (quick right-click defaults, action menu rules and labels, selection, Alt hints, portraits, build commands); docs/game/ui-screens.md (windows, panels, save and new-game screens, map, trade, building purchase); docs/game/game-loop.md (pause and speed); docs/game/dialogue.md (conversation panels and pause, recruiting); docs/game/locks.md (bed orders, rent, cages); docs/game/carry-loot.md (carrying, loot window); docs/game/economy.md (trade opening, range, buy-back); docs/game/perception.md (stealth icons, arrows); docs/game/buildings-production.md (build menu); docs/formats/camera.md (camera keys); docs/characters.md (character editor).
- Web search summaries of Steam community discussions and guides (not read directly; unverified): holding and dragging to a menu entry, "hold then click", pressing I in the trade window, shopkeeper stand-ins, bed rental by clicking the bed, Alt+click pick-up, map clicks, number keys in dialogue, research payment step.
- https://kenshi.fandom.com/wiki/Damage , /Toughness , /Faction_Uniform and https://github.com/VlcekM/meitouclient docs/game (ragdolls.md, character-stats.md, economy.md): when a knockout ends, playing dead, crawling, carry capacity, uniform prices and the trader's refusal line.
- https://kenshi.fandom.com/wiki/Mercenary_Guild , /Events : the two mercenary price lists.
