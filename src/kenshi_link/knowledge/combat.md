# Combat

How fights resolve in unmodded Kenshi 1.0.x: attack, block and dodge, weapon classes, armour, the behaviour buttons, crossbows and turrets, fighting groups, running away, and what happens after a defeat.

## How a melee exchange resolves
Also: combat mechanics, hit chance, who attacks, fight resolution
- Fighters take turns swinging. Who swings next is weighted by Melee Attack: each point of attack you have over the opponent's attack adds 2.5% to your odds of being the attacker.
- The defender then tries to block (if armed) or dodge (if unarmed).
- Base block chance is 70% when the defender's Melee Defence equals the attacker's Melee Attack.
- Each attack point above the defender's defence removes 1.5% block chance; each point below adds 1.2%.
- Block and dodge chance are limited to between 5% and 95%; 95% is reached at 21 levels above the attacker.
- A hit that gets through picks a body part by weighted chance, then armour and Toughness reduce the damage.
- Every unblocked hit staggers the victim briefly.

## Ordering an attack
Also: attack command, attack target, start a fight
- Right-click a hostile character with your characters selected: they move in and attack.
- Hold right-click on a character for the action menu, which includes "attack target".
- Characters fight back by themselves when attacked and join a nearby ally's fight (not on PASSIVE). They do not attack hostiles on sight unless HOLD is on.
- Attacking someone who is not hostile is assault: a crime if seen in a town, and it can turn their faction against you. Characters with a bounty on their head can be attacked freely.
- After you attack someone the cursor over them turns red (an aggression flag) for about 5 hours.
- While SNEAK is on, clicking a person may order a stealth knockout instead.
- Press R to stop the current action.
- With the game paused you can still give or change these orders.

## Blocking
Also: block chance, parry, weapon block, melee defence in a fight
- Only a character with a weapon equipped blocks. An armed character never dodges, except when hit while stumbling.
- Block chance comes from Melee Defence against the attacker's Melee Attack (see above).
- A blocked blow does no damage and does not stagger; a dodged blow does no damage either.
- Weapons add or subtract defence: for example Foreign Sabre +8, Jitte +8, Katana -4.
- With the BLOCK button on, the character gets +20 defence and never swings.
- A crawling character (leg down, or "Staying low") cannot block or dodge at all.
- Per kenshi.zone (not on the wiki): only the main target of a wide swing can block it; if they fail, others in the arc are hit too.
- If the right arm is unusable the character stops using weapons.

## Dodging (unarmed only)
Also: dodge chance, evade, martial arts defence
- An unarmed character dodges instead of blocking, using the Dodge skill against the attacker's Melee Attack (or Martial Arts).
- Maximum dodge chance is 95% at 21 levels above the attacker.
- Encumbrance cuts Dodge by 1% per 1%, up to -60%.
- Worn backpacks multiply Dodge: Small Backpack 0.85x, Medium 0.50x, Large 0.25x; thieves backpacks have no penalty.
- Dodge animations play at block speed, which for an unarmed character is driven by Martial Arts and Dexterity.
- Armed characters use Dodge only to escape a follow-up hit while stumbling.
- The BLOCK button adds 20 to Dodge as well.

## Stagger and stumble
Also: stun lock, knocked back, combo, stumbling
- Any hit that lands interrupts the target's own attack.
- If the hit's total damage is above a threshold of about 0.52 x the target's Toughness (52 at Toughness 100, under 1 at Toughness 1), the target stumbles: a long animation, up to about 4.5 seconds.
- A stumbling character cannot attack, and other enemies are allowed to strike at once, so hits chain ("stun lock").
- From about 1.2 seconds in, the victim rolls to break out with a dodge when the next swing comes.
- A blocked blow never staggers.
- Animals cannot be staggered or stumbled.
- Every crossbow bolt staggers a humanoid target that is not already staggered.
- A new character is stumbled by almost any hit, which is why new characters lose so fast.
- A shackled defender is knocked out outright by about a quarter of hits.

## Attack and block speed
Also: swing speed, slow attacks, combat speed formula
- Attack speed = (0.8 + 0.4 x (0.6 x Dexterity + 0.4 x Melee Attack) / 100) x 0.95 x Combat Speed, capped at 1.2.
- Base attack speed is 0.76; each Melee Attack level adds 0.00152 and each Dexterity level 0.00228. 100 in both gives 1.14.
- Block speed = (0.6 + 3.4 x (0.6 x Dexterity + 0.4 x Melee Defence) / 100) x 0.95 x Combat Speed, capped at 4.0.
- Unarmed, Martial Arts replaces both Melee Attack and Melee Defence in these formulas.
- Too little Strength for the weapon: about -2.6% per missing level, down to about -47.5%.
- Encumbrance slows attacks and blocks (to roughly 72.5% to 76.5% of normal at 100%).
- Fighting in deep water multiplies both speeds by 0.8.
- Injuries lower Dexterity and Strength, and so speed.

## Combat Speed multiplier (armour and backpacks)
Also: armour speed penalty, backpack combat speed
- Combat Speed is a separate multiplier on attack and block speed from worn gear. All worn multipliers multiply together.
- Raises it: Assassin's Rags 1.1x, Wooden Sandals 1.05x.
- Backpacks: small 0.95x, medium 0.9x, large 0.8x, Shopkeepers goods bag 0.5x. Thieves backpacks: none.
- Samurai Armour, Empire Samurai Armour, Ancient Samurai Armour 0.94x; Crab Armour 0.95x; Crab Trousers 0.96x; Holy Chest Plate and Unholy Chest Plate 0.96x.
- Chainmail and chain shirts (including Hive chain shirts) 0.97x.
- Samurai Legplates, Mercenary Plate, Armoured Rags 0.98x.
- Headgear never changes Combat Speed. Samurai Boots and Crab Shoes do not either.
- Do not confuse it with Combat Move Speed, which is fixed by race.

## How damage is calculated
Also: damage formula, toughness damage, armour damage reduction
- Blunt damage taken = raw blunt x (1 - blunt resistance) x (1 - damage resistance).
- Cut damage taken = raw cut x (1 - cut resistance) x (1 - damage resistance).
- Blunt and cut resistance come from an armour piece that covers the struck body part, and only if its coverage roll succeeds.
- Damage resistance comes from Toughness: -65% at Toughness 0, 0% at 50, +65% at 100. A new character takes about 1.6 times normal damage.
- A weapon's armour penetration lowers the armour's resistance by that percentage.
- Raw damage scales with the wielder: cut with Dexterity and weapon skill; blunt with Strength (75%) and weapon skill (25%); then the weapon's multipliers apply.
- Everything is scaled by the new-game setting "Global damage multiplier", which runs from 0.5x to 4x.
- Weapon damage has no random spread.

## Cut damage versus blunt (stun) damage
Also: stun damage, cutting damage, lethal damage, non-lethal
- Blunt weapons deal stun damage: it empties the body part's bar but causes no bleeding and heals by itself, conscious or not.
- Cutting weapons deal cut damage: it causes bleeding and never heals until bandaged with a first aid kit (or Skeleton Repair Kit).
- Unbandaged cut damage above 20% of a part's maximum health gets worse over time.
- A character knocked out by pure stun damage usually stands up within seconds unless driven into a recovery coma.
- So blunt-armed enemies (clubs, staffs) are far less deadly to lose to than sword- or animal-armed ones.
- Armour turns part of the cut damage it stops into stun damage.
- Unarmed hits never cause bleeding.

## Pierce damage (crossbows, turrets, animals)
Also: harpoon damage, harpoon resistance, bolt damage, animal bite
- Pierce is a kind of cut damage that ignores normal cut resistance. Crossbows, turrets and most animals deal it.
- Armour stops pierce only up to its Harpoon resistance, a flat number of points per piece, added up over all pieces covering the part (for example plate 35 + chainmail 20 = 55).
- The stopped points become stun damage through the armour's cut efficiency; the rest arrives as full cut damage.
- Example: a 50-damage bolt against 35 points of Harpoon resistance leaves 15 cut damage plus a little stun.
- Unarmoured characters take the whole amount as cut damage with heavy bleeding: crossbows always count as 2x blood loss.
- This is why animals shred unarmoured beginners and why armour is the answer to them.

## What weapon stats mean
Also: weapon tooltip, cut multiplier, blunt multiplier, blood loss, reach, indoors
- Cut and blunt damage figures: multipliers on the wielder's cut and blunt damage.
- Blood loss: multiplier on bleeding caused by the weapon's cut damage.
- Armour penetration: positive values weaken the target's armour; negative values strengthen it.
- Attack and Defence: added to the wielder's Melee Attack and Melee Defence while using it.
- Indoors: added to both attack and defence when fighting inside a building (usually negative for long weapons).
- Reach: longer weapons strike from further away and can hit several enemies in one swing.
- Damage vs race: bonus or penalty against animals, robots or humans.
- Weight and blunt damage set the Strength needed (greater of 40 x blunt figure and weight in kg).

## Weapon class: Katanas
Also: katana, wakizashi, nodachi, ninja blade, topper
- Pure cutting weapons, light, with low Strength requirements. Fast, offensive, high blood loss.
- Typical modifiers: attack bonus, defence penalty, armour penetration -15% to -30%, damage against robots -40%.
- Katana: cut 1x, blood loss 1.2x, penetration -30%, attack +4, defence -4, reach 21.
- Wakizashi: cut 0.9x, attack +2, defence -2, indoors +4, reach 16. Fits the secondary slot.
- Nodachi: cut 1.2x, attack +4, defence -4, indoors -4, reach 25, main slot only.
- Ninja Blade: cut 0.8x, attack +2, defence -4. Guardless Katana: attack +6, defence -6. Topper: cut 1.1x, blunt 0.1x, indoors -4.
- A two-hit combo makes them strong one-on-one and against animals, but exposed in a crowd.
- Best against unarmoured humans; poor against armour and Skeletons.

## Weapon class: Sabres
Also: sabre, foreign sabre, desert sabre, horse chopper, longsword
- Mostly cutting with some blunt. Defensive: most give a defence bonus and an attack penalty.
- Foreign Sabre: cut 1.2x, blunt 0.15x, attack -4, defence +8, reach 20.
- Holed Sabre: cut 1x, blunt 0.25x, attack -4, defence +6. Horse Chopper: attack -4, defence +4. Ringed Sabre: cut 1.2x, attack -2, defence +4.
- Desert Sabre: cut 1.1x, defence +2, large bonuses against spiders, Bonedogs and Skimmers.
- Longsword: attack -2, defence +2, penetration -15%; can go in the secondary slot.
- No indoor penalty. Armour penetration 0% (Longsword -15%).
- Fast attack animations leave few openings.
- A good first weapon for surviving: the defence bonus helps a low-skill character block.

## Weapon class: Hackers
Also: cleaver, combat cleaver, paladin's cross, long cleaver, moon cleaver
- An even mix of cut and blunt damage. Armour penetration +30% (Short-Cleaver +10%), bonus damage against robots, -10% against animals.
- Combat Cleaver: cut 0.75x, blunt 0.7x, robots +25%, reach 19.
- Flesh Cleaver: robots +15%, humans +20%, defence -2, reach 16.
- Long Cleaver: cut 0.8x, blunt 0.8x, robots +20%, defence -2, indoors -4, reach 25.
- Paladin's Cross: robots +50%, humans -10%, defence +2, indoors -2, reach 23.
- Short-Cleaver is the only one that fits the secondary slot.
- Blunt damage means high Strength requirements that grow with weapon quality.
- Best against armoured enemies and Skeletons.

## Weapon class: Heavy Weapons
Also: plank, fragment axe, falling sun, two-handed, big sword
- Two-handed, very heavy, highest damage per hit, long reach (25 to 32) and wide swings that hit groups.
- Plank: cut 0.8x, blunt 1.2x. Fragment Axe: cut 0.3x, blunt 1.8x. Falling Sun: cut 1.2x, blunt 1x, +50% against Beak Things, Gorillos and Leviathans.
- Indoor penalty -6 to attack and defence (Bull Horn Axe -4).
- Need both arms: with one arm disabled the character falls back to the secondary weapon or fists.
- Without the required Strength, attacks and blocks are up to 47.5% slower. A new character cannot use them effectively.
- Sold in Shek Kingdom weapon shops; common on Shek and Skeletons.
- Skeletons learn the skill 20% faster.

## Weapon class: Blunt weapons
Also: club, iron club, jitte, staff, spiked club, non-lethal weapon
- Almost pure blunt (stun) damage and very little bleeding.
- Iron Club: blunt 0.85x, cut 0.1x, indoors +2, secondary slot. Iron Stick: blunt 0.7x, attack -2, defence -2.
- Jitte: blunt 0.9x, no cut, defence +8, indoors +4. Heavy Jitte: blunt 1.3x, defence +8, penetration +10%.
- Mercenary Club: blunt 1x, penetration +30%, robots +20%.
- Victims wake quickly, so enemies beaten with clubs get back up.
- Strength requirements rise with quality because blunt damage does.
- Jitte and Heavy Jitte give no Dexterity XP.
- Many weak bandits carry clubs, which is why losing to them is survivable.

## Weapon class: Polearms
Also: polearm, heavy polearm, naginata, naginata katana, staff, spear
- Two-handed, light, long reach (23 to 28), attack bonus +4 to +8, indoor penalty -4 to -8.
- Polearm: cut 0.5x, blunt 0.5x, penetration +30%, animals +50%, attack +6, indoors -8.
- Heavy Polearm: cut 0.7x, blunt 0.4x, penetration +30%, animals +25%, attack +4, indoors -4.
- Naginata: cut 0.8x, blunt 0.2x, animals +50%, attack +6, indoors -8.
- Naginata Katana: cut 0.85x, animals +25%, humans +25%, robots -20%, penetration -15%.
- Staff: blunt 0.8x, almost no cut, attack +8, indoors -6; effectively a long blunt weapon.
- The wiki calls them an excellent choice for low-skilled characters: low Strength requirement, katana-like speed, long range.
- Rare in shops; Staffs are carried by farmers and nomads.

## Which weapon class to use against what
Also: best weapon against armour, best weapon against animals, best against robots
- Unarmoured or lightly armoured humans: Katanas (bleeding, speed) or Sabres.
- Heavy armour: Hackers, Polearm, Heavy Polearm, Mercenary Club (all +30% armour penetration). Katanas are worst.
- Skeletons and robots: Hackers (bonus damage). Katanas do 40% less.
- Animals: Polearms (+25% to +50%). Hackers do 10% less.
- Indoors: Sabres, Wakizashi, Jitte, Iron Club; avoid Heavy Weapons and Polearms.
- Crowds: long reach (Heavy Weapons, Polearms, Nodachi) hits several enemies per swing.
- Taking prisoners alive: Blunt weapons.
- Carry a sidearm of a different kind in the second slot; the character switches when the main weapon is penalised indoors.

## Weapon for a weak new character
Also: first weapon, starter weapon, beginner weapon, low strength weapon
- Check the Strength needed: greater of 40 x blunt figure and weight. A Strength 1 to 10 character can only swing light cutting weapons at normal speed.
- Katanas, Wakizashi and most sabres need only their weight in Strength.
- A sabre with a defence bonus (Foreign Sabre +8, Holed Sabre +6) helps a low-skill character block.
- Polearms give reach and an attack bonus at low Strength, but are rare and bad indoors.
- Low grades (Rusted Junk, Rusting Blade) are cheap and are actually better for training.
- Avoid Heavy Weapons, Hackers and high-grade clubs until Strength catches up.
- A weapon does not make a new character able to win; it lets them block, earn XP, and survive beside guards.

## Armour coverage
Also: coverage percent, armour hit chance, body part protection
- Each armour piece lists coverage per body part, for example Chest 100%, Stomach 85%, Arms 85%.
- Coverage is the chance that the piece applies at all to a hit on that part. With 80% coverage, one hit in five gets no protection from that piece.
- It is not a share of the damage blocked.
- Example coverage at Standard grade: Samurai Armour chest 100%, stomach 85%, arms 85%; Holy Chest Plate chest 100%, stomach 100%, arms 25%, legs 40%; Samurai Legplates stomach 50%, legs 100%.
- Many enemies wear armour with poor coverage, which is why some hits on them do full damage.
- Chest and stomach are hit most often, so cover them first.

## Cut resistance, cut efficiency and blunt resistance
Also: armour stats, stun conversion, cut resistance efficiency, resistances
- Blunt resistance: flat percentage off blunt damage.
- Cut resistance: percentage of cut damage stopped (maximum 90% on one piece).
- Blunt resistance on one piece is capped at 90% according to the wiki and 80% according to a code-based reference.
- Cut resistance efficiency: the share of the stopped cut damage that vanishes. The rest becomes stun damage that ignores further armour.
- Example: 75% cut resistance, 60% efficiency, 50 cut damage: 12.5 cut gets through and 15 stun is added.
- Low-efficiency armour therefore swaps bleeding wounds for bruises, which is still a good trade.
- Harpoon resistance: points of crossbow, turret and animal pierce damage absorbed.
- Shirts have their cut and blunt resistances multiplied by 0.8.
- Toughness is applied after all armour.

## Armour layering order
Also: overlapping armour, shirt under armour, stacking armour
- When several pieces cover the same body part, they are applied in slot order: Headgear, Body Armour, Legwear, Shirt, Footwear.
- Each later piece only works on the cut damage the earlier ones let through.
- Example: Samurai Armour (81.25% cut resistance, 90% efficiency) over a Leather Turtleneck (33.44%, 50%): 100 cut damage ends as 12.48 cut and 11.26 stun.
- Blunt resistance stacks the same way.
- Harpoon resistance simply adds up across pieces.
- Weather protections add up across all worn pieces.

## Armour penetration
Also: AP, armour piercing, negative armour penetration
- A weapon's armour penetration scales the target armour's resistances at the moment of the hit.
- +30% turns 66.5% blunt resistance into 46.55%.
- Negative penetration (katanas, -30%) raises the armour's cut resistance, but never above the 90% cap.
- Weapons with +30%: all Hackers except Short-Cleaver, Polearm, Heavy Polearm, Mercenary Club.
- Against unarmoured targets penetration does nothing; the weapon's raw damage and bleeding matter instead.

## Light, medium and heavy armour: class multipliers
Also: armour class penalties, stealth multiplier by class, athletics multiplier by class
- Clothing: no coverage. Some pieces give Martial Arts bonuses.
- Light armour: little protection, often bonuses to combat stats, stealth or speed. No Athletics, Combat Speed or Stealth penalty from its class.
- Medium armour: more coverage; class Stealth multiplier 0.9; Athletics as low as 0.85x on legwear and footwear.
- Heavy armour: most protection; Stealth multiplied by 0 to 0.4, Athletics down to 0.80x, Combat Speed down to 0.9x, plus penalties to skills and often Dexterity.
- Class multipliers for cut resistance: cloth 0.4, light 0.8, medium 0.9, heavy 1.0.
- Heavier pieces also weigh more, which raises Encumbrance on a low-Strength character.
- Headgear never penalises Athletics, Combat Speed or Stealth.
- What each class is for, in words: "Armour classes" in Items and equipment.

## Armour penalties to skills
Also: armour skill multiplier, 0.8x, armour debuff, negative stats
- Penalties show on the item either as a flat number (Melee Attack -8) or a multiplier (Stealth 0.50x).
- A multiplier scales the skill: 0.67x turns skill 50 into 33.5. Multipliers from several items multiply together.
- Flat examples: Tin Can -5 Melee Attack; Samurai Armour -8 Melee Attack and -10 Martial Arts; Crab Armour -10 Melee Attack; Armoured Rags -5 Melee Defence; Armoured Hood -2 Melee Defence; Samurai Legplates -10 Martial Arts; Samurai Boots -5 Martial Arts.
- Assassination multipliers: Samurai Armour 0.50x, Mercenary Plate 0.70x, Plate Jacket 0.80x, Crab Armour 0.20x.
- Some penalties shrink at higher armour quality.
- The bottom-left panel shows the resulting current skills; judge fights by those, not the stats page.

## Armour for a weak new character
Also: first armour, starter armour, beginner armour, cheap armour, what to wear
- Any armour is better than none: at Toughness near 0 every hit does about 1.6 times normal damage.
- Wear light or medium armour until stats improve: a low-Strength character can carry it and it may add combat bonuses. Which pieces to get, with prices: "Early armour picks" in Items and equipment.
- Most footwear other than Wooden Sandals slows running.
- Loot armour from bandits the town guards have beaten; taking from bandits is not a crime. Do not loot unconscious townspeople or guards.
- Watch the Encumbrance %: armour weight counts against a 16 to 25 kg carry limit.
- A helmet matters: head damage knocks out fastest and lengthens knockouts most.

## Behaviour buttons in a fight: which to set
Also: combat mode setup, stance for a fight, tank setup, squad orders in combat
- The seven toggles on the orders panel (BLOCK, HOLD, PASSIVE, JOBS, RANGED, TAUNT, SNEAK) are set per character. What each does is in the Interface file under "BLOCK button", "HOLD button" and so on.
- Your characters do not attack hostiles on sight by default: they fight when attacked, when ordered, or when a nearby ally is in a fight. HOLD and PASSIVE change this.
- Tank: TAUNT plus BLOCK on the best-armoured character. Players also toggle BLOCK by hand: on while enemies swing, off to counter-attack.
- Weak character: BLOCK to survive until help arrives, or while backing toward guards (the game's own tip).
- Crossbow users and medics: HOLD keeps them in place. RANGED off makes a crossbow carrier use the sidearm.
- Wounded: HOLD stops them rejoining the fight.
- Workers, traders and a hidden medic: PASSIVE.
- Whole squad down: PASSIVE and SNEAK, so characters who wake stay low instead of standing and being beaten again.

## Crossbows: how to use one
Also: using a crossbow, shoot crossbow, equip crossbow, ranged attack
- Equip the crossbow in Weapon 1, put matching bolts in the same character's inventory, and make sure RANGED is lit (it is on by default).
- Right-click an enemy to attack; the character aims, shoots and reloads.
- Carry a melee sidearm in the second slot. Crossbows need both arms.
- Kiting: with HOLD on, shoot, step back when the enemy closes, repeat.
- Larger targets are easier to hit: big animals are easy, spiders hard. Shooting from higher ground increases range.
- Every hit staggers a humanoid target, and bolts cause heavy bleeding. Armour with harpoon resistance absorbs a fixed amount per bolt.
- Skills: Crossbows (accuracy, reload), Perception (accuracy, range), Dexterity (reload), Precision Shooting (not hitting allies; see "Friendly fire"). A beginner misses often.
- Assassin's Rags, Drifter's Leather Jacket and Ninja Rags multiply the Crossbows skill by 1.10.
- Characters with Diplomat status cannot normally be targeted.
- Types, prices and bolts: "Crossbows compared" and "Crossbow ammunition" in Items and equipment.

## Friendly fire
Also: shooting allies, crossbow accident, turret hits friends
- Crossbows and turrets can hit and kill squad members.
- Avoidance comes from Precision Shooting (1.5% per level, full at about 67) for crossbows and from the Turrets skill (full at 50) for turrets.
- Low-skill shooters should use weak crossbows (Tooth Pick) or shoot only before melee is joined.
- Turn RANGED off once allies are between the shooter and the target.
- Dust storms, darkness and head injuries make it worse.

## Fighting several enemies
Also: outnumbered, surrounded, group fight, attack slots
- By default one attacker at a time holds the "attack slot" on a humanoid target, up to five can be engaged with it, and the rest circle. But a stumbling target may be struck by the others at once, so hits chain.
- Being outnumbered multiplies XP (+10% per extra enemy, up to x1.666) but is how weak characters die.
- Keep moving so enemies string out in a line, and fight the first to arrive.
- Use doorways and walls so only one or two can reach you.
- Put the armoured character in front with TAUNT and BLOCK; weaker ones attack from the sides.
- Long-reach weapons hit several enemies per swing.
- Lead the group to a guarded gate or into another hostile group instead of fighting it.

## Fighting retreat: Shift + move order
Also: withdraw while fighting, back away, careful retreat, combat mode move
- A loading-screen tip covers this: give a fighting character a move order with SHIFT held and they work their way to that spot carefully, still fighting and guarding themselves.
- A plain right-click move order instead makes the character turn and run, taking hits in the back from anyone in reach. (unverified)
- Use the Shift version to back a fighter toward guards, a doorway or the rest of the squad a few steps at a time.
- Use the plain run only when you are clearly faster than the enemy or not yet engaged.
- Holding SHIFT with other orders makes them permanent jobs, so use it here only with ground move orders during a fight.

## Hit and run (kiting)
Also: kite, skirmish, single fighter against group
- Needs a character faster than the enemies.
- Let the group approach, attack the nearest one once, then run a short distance whether or not the hit landed.
- If an enemy is about to swing first, step away a few paces and re-engage.
- Repeat; cutting weapons wear the group down through blood loss.
- Pause often to see who is about to swing.
- With crossbows: shoot, back up when someone closes, shoot again, using HOLD to stop the shooter charging.
- One mistake means being surrounded, so keep hunger above 200 and Encumbrance at 0%.

## Fighting next to town guards
Also: retreat to town, lure to gate, guards help
- All major towns except The Hub have town guards who attack hostile-faction groups.
- When chased, run to the nearest guarded town; once the guards are fighting your pursuers, join in for safe XP.
- Guards act against groups from factions hostile to their town.
- In Hive Villages the Hive soldiers only fight an animal that attacks a drone.
- Afterwards, loot the bandits (legal) and bandage the wounded.
- Do not swing at townspeople or guards by mistake; assault is a crime.
- The Hub is the exception: it has no town guards. Its bar belongs to the Trade Ninjas, whose guards attack Dust Bandits, Starving Bandits and Bonedogs that come near the bar, so run to the bar there.

## Luring enemies into each other
Also: smash groups, bandits fight bandits
- Hostile groups from different factions fight each other when they meet.
- Run toward one group, then circle toward the other; outrun both and they engage each other.
- Wait until one side is left and wounded, then finish or avoid it and loot the bodies.
- Works with bandits against bandits, bandits against animals, and bandits against patrols.
- Needs enough Athletics to stay ahead of both groups.

## When to run
Also: flee, retreat, escape decision, avoid fight
- A new character (skills 1 to 5, Toughness near 0) loses to almost any group.
- Run when: you are alone against two or more; the enemy has swords, crossbows or teeth rather than clubs; the enemy would enslave or eat you; chest, stomach or head is near 0; hunger is under 200; nobody is left to bandage you.
- Run before the fight starts. Once enemies surround a staggered character it is too late.
- Typical bandit combat stats: Hungry Bandits about 5, Dust Bandits about 15.
- Losing on purpose is acceptable only to club-armed bandits who just take food.

## How to run
Also: escape, outrun, run speed, chased
- Set movement to run and right-click the ground toward safety: a guarded gate, another hostile group, or deep water.
- Speed is what counts: Greenlander 15.7 mph at Athletics 0, so many enemies keep pace at first. Cannibals run 14 to 20 mph; Security Spiders about 11 mph.
- Drop weight first: each 1% Encumbrance costs 1% speed.
- Leg health below 55.6% slows running; a splint can restore it.
- Hunger below 200 slows running.
- Do not stop to pick things up; pursuers swing when they catch up.
- Swimming speed is low for beginners (about 1.3 mph), so water is a refuge only from enemies that swim worse.

## Shaking off pursuers
Also: lose pursuers, chase give up, break line of sight, enemies stop chasing
- From a code-based reference: an NPC chasing a fleeing target has no distance limit.
- It gives up only when it has neither seen nor heard the target for about 13 game minutes (roughly 24 real seconds at normal speed), or when it reaches the spot where it last sensed the target.
- It never gives up in the first 5 game minutes (about 9 real seconds) of the chase.
- With the target in view on open ground it keeps coming.
- So break line of sight: put buildings, walls or hills between you, or use SNEAK in darkness, then keep moving.
- An enemy also drops a target that is knocked out, carried, caged or dead.
- Guards or another hostile group drawing the pursuers into a fight ends the chase sooner.

## What happens when you lose a fight
Also: defeat, knocked out, after losing, consequences
- Losing usually means unconsciousness, not death. What follows depends on who won.
- Food-stealing bandits: take food and leave.
- Other bandits: beat you, may take belongings, and leave you bleeding.
- Slavers, Manhunters, United Cities and Holy Nation forces: bandage you and take you as a slave or prisoner.
- Town police: jail in a cage.
- Cannibals and Fogmen: carry you off to be eaten.
- Animals: some eat the unconscious, costing limbs or life.
- Nobody: you wake when the knockout timer ends, or bleed out first.
- In every case the real killers are untreated cut wounds and blood loss, so someone must bandage.
- The new-game option "Bandits loot the player" (on by default) decides whether NPCs loot your downed characters.

## Losing to slavers and the Holy Nation
Also: enslaved after a fight, captured by slavers, slave traders, shackles
- Slave Traders, Manhunters, Slave Hunters, United Cities and Holy Nation forces heal unconscious victims and carry them to a slave camp or town.
- Weapons are confiscated first; armour is replaced with Prisoner Shackles; the rest of the gear goes into storage at the camp.
- Slaves are kept alive: bandaged after beatings and fed to about hunger 100.
- Slave Traders do not attack unless their faction is hostile, but they do pick up anyone lying unconscious near them.
- Escape needs Lockpicking (shackles, cage), Stealth and patience; afterwards the character is an escaped slave, hunted until "Looks like a Slave" in the inventory window drops to 1%.
- Being imprisoned by the United Cities or Holy Nation can also end in slavery.

## Losing to cannibals and Fogmen
Also: eaten alive, prisoner pole, cannibal cage
- Cannibals (Cannibal Plains, Darkfinger and nearby) carry unconscious organic characters to their camps and cage them; when cages fill they beat prisoners to death and cook them. They use clubs so victims survive the trip.
- Fogmen (Fog Islands, Dreg) carry any non-Skeleton to a Fog Deathyard, tie them to a Prisoner Pole, and Fog Princes or Fog Heavies eat them alive, limbs first.
- Being eaten applies cut damage that must be bandaged afterwards.
- On a pole a character can still bandage themselves once able, and can pick the lock to escape.
- Rescue is possible but new Fogmen keep arriving.
- Never lose a fight in these regions.

## Losing to town guards or police: jail
Also: arrested after a fight, prison cage, jailed
- Guards who defeat a character with a bounty put them in a Prisoner Cage.
- Weapons are taken on entering the cell.
- A bounty expires after 4 hours per c.100; a jail sentence is half that time.
- Bounties above c.10,000 never expire on their own.
- A prisoner can escape with the "escape" option in the right-click-hold menu (lockpicking), but leaving early is itself a crime.
- In United Cities or Holy Nation towns a jailed character may be enslaved if a slaver patrol comes by.

## Losing to animals
Also: eaten by animals, animal attack aftermath
- Many animals deal pierce damage with heavy bleeding, so an unarmoured character can bleed out fast.
- Some animals eat unconscious bodies, alive or dead, which removes limbs and can kill.
- A character knocked out only by blood loss gets back up instantly if an animal starts eating them; most animals then flee. Sneak and bandage at once.
- Bonedogs carry off severed limbs.
- Animals cannot be staggered, so a weak character cannot interrupt their attacks.
- Polearms and armour with Harpoon resistance are the tools against them.

## Secret medic: keep one character out of the fight
Also: backup medic, hidden healer, survive a wipe
- With two or more characters, keep one well back before any risky fight.
- Set that character to PASSIVE (and SNEAK if their Stealth is decent) with a first aid kit in the inventory.
- When the others are down, wait until the enemy has left, then move in and bandage: blood first, then head, chest and stomach.
- Carry the worst-hurt to a bed.
- The wiki's point: with a second character around, a lost fight tends to end in bad wounds rather than death.
- A lone character has no such safety net: avoid fights rather than rely on waking up.

## Sources
- https://kenshi.fandom.com/wiki/Melee_Attack : attack odds, block chance per point, base 70%, attack speed per level.
- https://kenshi.fandom.com/wiki/Melee_Defense , /Dodge : armed characters block, unarmed dodge, 95% at 21 levels.
- https://kenshi.fandom.com/wiki/Global_Game_Settings : 5% and 95% limits, stumble threshold, attack slots note.
- https://kenshi.fandom.com/wiki/Combat_Speed : speed formulas, gear multipliers, strength and encumbrance effects, combat move speed.
- https://kenshi.fandom.com/wiki/Damage : damage formulas, stun and cut, pierce and Harpoon resistance, blood loss, KO rules.
- https://kenshi.fandom.com/wiki/Resistances , /Armor_Stats , /Guide_to_Equipment : coverage, layering, efficiency, penetration, class multipliers, grades, weapon slots.
- https://kenshi.fandom.com/wiki/Weapons , /Weapons/Classes , /Katanas , /Sabres , /Hackers , /Heavy_Weapons , /Blunt_Weapons , /Polearms : class traits and per-weapon modifiers, manufacturers.
- https://kenshi.fandom.com/wiki/Unknown_(manufacturer) : Rusted Junk modifiers.
- https://kenshi.fandom.com/wiki/Heavy_Armour , /Light_Armour , /Armour : coverage examples, armour classes, sell value.
- https://kenshi.fandom.com/wiki/Getting_Started : the seven buttons and what each does, defaults, starter armour advice, crime notes.
- https://kenshi.fandom.com/wiki/Combat_Strategies : tank, secret medic, retreat to guards (not The Hub), hit and run, smashing groups, hiring.
- https://kenshi.fandom.com/wiki/The_Hub , /Trade_Ninjas : the Hub bar's Trade Ninja guards and whom they attack.
- https://kenshi.fandom.com/wiki/Crossbows , /Mounted_Crossbow , /Harpoon_Turret , /Turrets , /Precision_Shooting , /Adventurer_Bar : ranged weapons, bolts, friendly fire.
- https://kenshi.fandom.com/wiki/Stronger_Opponent_Logic , /Guide_to_Training_Statistics : outnumbered bonus, BLOCK and Dodge XP, gear maluses.
- https://kenshi.fandom.com/wiki/Hungry_Bandit , /Starving_Bandits , /Dust_Bandit , /Dust_Bandits : early enemy stats, gear, behaviour.
- https://kenshi.fandom.com/wiki/Slavery , /Cannibals , /Fogmen , /Prisoner_Pole , /Bounty , /Prisoner_Cage , /Hive_Village : outcomes of defeat.
- https://kenshi.fandom.com/wiki/Guide_to_Health : blood-loss knockout and animals, Medic button.
- https://kenshi.fandom.com/wiki/Loading_Screen , /Jobs , /Controls : in-game tips (BLOCK, Shift + move in combat, bounties, sidearm switching), job rules, R key.
- https://github.com/VlcekM/meitouclient (local clone, third-party reference worked out from the game's code and data; only its statements about the original game were used): docs/game/combat.md (blocked and dodged blows, stumble threshold and length, attack slots, target scoring for TAUNT and PASSIVE, attack on sight only on HOLD, chase give-up, armour caps, no damage spread); docs/game/perception.md (HOLD ranges); docs/game/ui-screens.md (orders panel buttons and tooltip wording); docs/game/ragdolls.md (Staying low, crawling); docs/game/carry-loot.md (RESCUE off on HOLD, looting option); docs/game/character-stats.md (constants: attack slots 1, block chance 70/12/15).
- https://steamcommunity.com/app/233860/discussions/0/133257636770657665/ (via web search): RESCUE button behaviour, player report.
- https://kenshi.zone/en/combat and https://kenshi.zone/en/prison-escape (via web search summaries only; site not reachable): area attacks and blocking, outcomes by captor.
- https://steamcommunity.com/app/233860/discussions/0/1633040337756799731/ (via web search): HOLD still engages enemies in reach.
- Crossbow skill and armour-bonus notes merged in from Items and equipment rest on the sources listed there.
