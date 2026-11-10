# Stats and training

What every attribute and skill does, exactly how each gains experience, and the safest efficient ways to raise them early, including encumbrance and carried weight.

## Opening the stats window and reading XP
Also: character stats page, C key, skill list, XP percentage, level progress
- Press C (default) with a character selected to open the Character Stats page.
- Hover a skill to read its description and the progress toward the next level.
- Skills are grouped: Attributes, Weapon Skills, Combat Skills, Thievery, Athletics, Science, Trade, Ranged.
- The numbers that apply in a fight are the current ones in the bottom-left character panel, not the raw ones on the stats page: armour, backpack, injuries, hunger and weather change them.
- The bottom-left panel also shows live training rates such as the Athletics XP % and Strength XP %, and the Encumbrance %.
- A value in brackets next to a skill, such as (-10), is a modifier from gear.

## How experience and levels work
Also: XP formula, level multiplier, skill cap, level 100, diminishing returns
- XP given = base experience x exp gain multiplier (3 by default) x racial multiplier x level multiplier x opponent multiplier.
- Level multiplier = (1 - level/101) squared: 1.00 at level 0, about 0.81 at level 10, 0.49 at 30, 0.25 at 50, 0.04 at 80.
- So the first 20 to 30 levels of anything come quickly and the last 20 are very slow.
- If the XP from one action is too small it rounds to 0 and nothing is gained.
- No skill can reach level 101 by training, and many cannot reach 100. Field Medic and Robotics are time-based and are the exception.
- Lowering your effective level with gear does not make you level as if you were that level; it only changes the opponent multiplier for combat skills.

## Stronger Opponent Logic (XP for fighting better enemies)
Also: SOL, skill difference, XP bonus, fighting stronger enemies, XP penalty
- Combat XP is multiplied by comparing one of your skills with the opposing skill of the enemy.
- +10% XP for every level you are below the opponent, up to x6.0 at 50 levels below.
- -4% XP for every level you are above, down to x0.1 at 22.5 levels above.
- Affected: Melee Attack, Melee Defence, Martial Arts, Dodge, Dexterity and the six weapon skills.
- Melee Attack and weapon skills are compared with the enemy's Melee Defence (or Martial Arts if the enemy is unarmed).
- Melee Defence and Dodge are compared with the enemy's Melee Attack (or Martial Arts if unarmed).
- Your modified level is used, so gear that lowers a skill raises the multiplier.
- Fighting animals: hitting them uses their defence as if fully grown.

## Outnumbered XP bonus
Also: fighting many enemies XP, 1v8
- Combat XP is multiplied by +10% for each enemy by which a single character is outnumbered.
- 1 against 4 gives x1.3.
- The bonus caps at 1 against 8 or more, x1.666.
- Combined with the x6 opponent multiplier the theoretical maximum is x10.

## Recommended training order for a new character
Also: what to train first, early game training plan, beginner build
- The wiki's order: Athletics and Stealth first, so you can outrun or hide from anything in the wilderness and choose your fights.
- Then Toughness, which lowers all damage taken.
- Then Melee Defence, by being hit by enemies with high attack.
- Then Melee Attack and Dexterity, using Rusted Junk weapons with high cut and low blunt damage.
- Strength can be trained in parallel from the first minute by carrying weight while walking anywhere.
- Labouring (mining) trains while earning money and is safe next to a town.

## A safe first-days routine near a town
Also: beginner routine, early game loop, what to do first, train while earning
- Feed the character first if hunger is below 250; a hungry start cuts speed and Strength.
- Mine a Copper or Iron deposit just outside a town gate (Labouring XP and ore to sell).
- Carry the ore in an unworn backpack or the plain inventory until Encumbrance is near 70%, then walk it to a trader (Strength XP).
- Leave SNEAK on while working and walking near NPCs (slow Stealth XP).
- Make the return trips empty and in run mode (Athletics XP at the full rate).
- Buy a Basic First Aid Kit, food, any light armour and a cheap light weapon with the first money.
- When bandits attack the town, stay behind the guards, hit stragglers, then bandage the fallen (combat and Field Medic XP) and loot the bandits.
- Sleep in a rented bed when hurt.

## Strength: what it does
Also: STR, strength stat, what strength affects
- Sets carry capacity (see the encumbrance sections).
- Sets whether a weapon can be swung at normal speed (see weapon strength requirement).
- Raises blunt damage with weapons: Strength supplies 75% of blunt scaling, the weapon skill 25%.
- Raises Martial Arts damage more than any other stat.
- Raises the chance to break free of or resist kidnapping.
- For Greenlanders, Scorchlanders and Shek, blood = 75 + 0.75 x base Strength.
- Hunger hits Strength hardest: -0.9% per hunger point below 200, to -90% at 100.
- Injured arms, chest or stomach lower it by up to 22.5%; an arm below 0 health costs a further 34%.

## Strength: training by walking with weight
Also: strength XP walking, encumbrance training, 70% encumbrance, carry training
- Strength XP is earned while moving on land with Encumbrance above 0%. The current rate shows as Strength XP % in the bottom-left panel.
- Rate = (Encumbrance as a fraction) squared x 50%, capped at 25%: about 4.5% at 30% Encumbrance, 12.5% at 50%, and the 25% cap from about 71% up.
- More weight than that only slows you and cuts Athletics XP.
- Carrying a person or animal (alive, unconscious or dead) doubles it to 50%, the maximum from walking; the tooltip line is "Carrying somebody: 200%".
- Items held by the carried character do not count toward your weight.
- Swimming gives no Strength XP.
- Safe but slow: very high Strength this way takes hundreds of game days. Most useful for the first 20 to 40 levels.

## Strength: safe step-by-step routine in town
Also: backpack of iron, follow a guard, strength grind
- Buy a backpack (a Wooden Backpack or Trader's Wooden Backpack stacks ore) and fill it with heavy items such as Raw Iron or ore.
- Put the filled backpack into the character's inventory grid, not the backpack slot. Worn backpacks reduce the weight of their contents; an unworn one counts in full.
- Check the bottom-left panel: aim for Encumbrance of 70% or a little more (about 3 times carry capacity).
- With a second character: hold right-click on them and choose pick up, so the first carries them (50% rate).
- Order the loaded character to walk: hold right-click on a patrolling guard and choose follow, or right-click back and forth inside the walls.
- Set "follow" as a job so the character resumes if interrupted.
- Remove the weight before any fight or escape: at 100% Encumbrance speed is about 2 mph.

## Strength: training in combat
Also: heavy weapon strength XP, strength per hit, martial arts strength
- Fastest method. Each strike you make gives Strength XP, even if blocked.
- Blocking a hit gives 40% of a strike's XP; being hit unblocked gives 10%.
- With a weapon, XP per swing depends on how far your Strength is below the weapon's required Strength, peaking at 110% when you are 20 or more levels short.
- A weapon giving 110% Strength XP gives 11 times the XP per swing of one giving 10%.
- Unarmed (Martial Arts), XP per hit equals your Encumbrance %: 100% Encumbrance gives 100%. Being hit gives 10% of your Encumbrance %.
- Both methods make you slow and easy to hit, so do them only where losing is survivable, such as beside town guards.

## Weapon strength requirement
Also: required strength, too heavy weapon, slow swing, 40x blunt
- Required Strength = the greater of 40 x the weapon's blunt damage figure and the weapon's weight in kg.
- Examples: Paladin's Cross (blunt 1.46, 29 kg) needs 58.4; Staff (blunt 1.00, 5 kg) needs 40; Jitte (blunt 1.20, 16 kg) needs 48; Nodachi (blunt 0, 8 kg) needs 8.
- Katanas and most sabres have little blunt damage, so their requirement is just their weight.
- Below the requirement, attack and block speed fall about 2.6% per missing level, to about -47.5% at 18 to 20 levels short.
- Strength above the requirement gives no speed bonus, but injuries lower Strength, so keep a margin of about 10%.
- Martial Arts: the Strength and Martial Arts pages say it needs Strength equal to 80% of the Martial Arts level; the Combat Speed page says it has no requirement.

## Encumbrance: carry weight and the percentage
Also: overweight, weight limit, encumbered, inventory weight, kg, carry capacity
- Every item has a weight; worn equipment counts too. A carried body adds 30 kg.
- Carry capacity C = 1.2 x effective Strength + 15 kg, according to a reference built from the game's code and checked in game.
- The Strength tooltip ("Max carry weight") and the wiki give Strength + 15 kg instead.
- Up to C the character is at 0% Encumbrance.
- Effective Strength includes hunger and injury penalties, so a starving or wounded character is encumbered sooner.
- Items inside a worn backpack weigh less by that backpack's reduction; installed robot limbs weigh nothing.
- Encumbrance cannot exceed 100%.
- The wiki also lists state labels: Weightless, Lightweight, Moderate, Heavy, Overloaded (90% or more).

## Encumbrance percentage: how much weight gives what
Also: encumbrance formula, how much to carry, weight for 70%, training weight
- From a code-based reference: Encumbrance % = 100 x (1 - (C - 0.05 x W) / (0.95 x W)), kept between 0 and 100. C is carry capacity (1.2 x Strength + 15 kg), W the total weight carried.
- 0% while W is at most C.
- 50% at about 1.9 x C.
- 70% (the Strength-training target) at about 3 x C.
- 90% at about 6.9 x C; 100% only at 20 x C.
- Strength 1: C is about 16 kg, so 70% needs about 48 kg.
- Strength 10: C = 27 kg, 70% at about 81 kg.
- Strength 20: C = 39 kg, 70% at about 116 kg.
- Raw Iron and ore in a backpack that is in the inventory but not worn are the usual training weights.

## Encumbrance penalties
Also: slow movement, overloaded effects, weight and speed, weight and combat
- Movement speed: -1% per 1% Encumbrance, down to a floor of about 2.5 mph (11 game units) at 100%.
- Dodge: -1% per 1% Encumbrance, capped at -60% (reached at 60%). Dodge XP is cut by the same percentage as Encumbrance.
- Martial Arts skill: -0.8% per 1% Encumbrance, -80% at 100%.
- Hunger rate while moving or fighting: +0.007 per 1% Encumbrance, 1.7x at 100%.
- Attack and block speed: the Encumbrance page says -0.235% per 1% from the start (-23.5% at 100%); the Combat Speed page says no effect up to 50%, then a linear drop to 72.5% of normal at 100%.
- Athletics XP falls as Encumbrance rises; Strength XP from walking rises until 70%.
- Weight also makes sneaking easier to detect.

## Backpacks and carried weight
Also: backpack encumbrance reduction, backpack penalties, backpack types
- A worn backpack lowers the weight of what is inside it: Small Backpack, Medium Backpack, Large Backpack, Wooden Backpack and Trader's Wooden Backpack 50%; Thieves Backpack and Small Thieves Backpack 60%; Scavenger's Basket 30%.
- Worn backpacks cost combat stats. Melee Attack and Melee Defence: Small -2, Medium -5, Large -10, Wooden -5, Thieves -2, Small Thieves 0.
- Combat speed: Small 0.95x, Medium 0.90x, Large 0.80x; thieves backpacks 1.00x.
- Stealth and Dodge: Small 0.85x, Medium 0.50x, Large 0.25x; thieves backpacks 1.00x.
- Backpack penalties do not reduce Martial Arts.
- A backpack placed in the inventory grid (not worn) gives no penalty and no weight reduction.
- Food in a worn backpack is shared with nearby squad members.

## Carrying a person: weight and training effect
Also: pick up, carry body, carry squad member, lift person
- Hold right-click on a character (squad member, unconscious body, corpse or animal) and choose the pick up option.
- A carried body adds 30 kg regardless of what it is wearing or holding. The carrier needs a working left arm.
- Walking while carrying doubles walking Strength XP (maximum 50%).
- Swimming while carrying doubles Swimming XP.
- Holy Nation characters generally ignore whoever is being carried.
- A classic group routine: one character at 70% Encumbrance carries another; everyone else walks unencumbered alongside at the same slow pace and still earns Athletics XP at the full rate.

## Toughness: what it does
Also: toughness stat, damage resistance from toughness, what toughness affects
- Damage resistance % = -65 + 1.3 x Toughness. At Toughness 0 a character takes 65% extra damage; break-even is level 50; at 100 damage is cut by 65%.
- KO point = -10 - 0.75 x Toughness. This is how far below 0 a vital part can go before the character falls into a recovery coma (-10 at level 0, -85 at 100).
- Wound degeneration speed = 1.7 - 0.0167 x Toughness (1.7x at 0, 0.03x at 100).
- Shortens knockout time from cuts and blood loss.
- Raises the damage needed to make the character stumble.
- Adds to Martial Arts damage.
- Sets when hunger makes you faint: at hunger 100 + KO point or lower (a KO point of -50 means fainting at 50 hunger and below).

## Toughness: how it is trained
Also: toughness XP, getting beaten up, taking damage
- XP comes from taking damage. Damage that armour or Toughness then cancels still counts.
- It is scaled by the damage received against your Toughness level: x0.1 when the damage is 25 or more below your level, x2 at 10 above, up to x6 at 50 above.
- Being knocked out by a blow to the head, chest or stomach pays a bonus; leg and blood-loss knockouts do not.
- Ordering a character who is playing dead to get up pays a large bonus (next section).
- Losing a limb gives a large one-off gain.
- Some dialogue choices that pick a fight also give Toughness.
- Good armour helps training: more hits survived per knockout and shorter knockouts.

## Toughness bonus for getting up while playing dead
Also: get up bonus, Toughness XP multiplier, force get up XP
- Give any order to a character whose health panel reads "Playing dead...": they stand, and Toughness gains a large amount.
- The gain is proportional to (number of enemies sensed + 10) x the Toughness XP multiplier.
- It is paid only when the player gave the order, enemies are sensed, and no conscious ally is near. With an ally still up, nothing is paid.
- The multiplier is shown as "Toughness XP" in the expanded bottom-left panel: 3x for a character in good shape; "Crippled left arm" adds 1x, "Crippled right arm" 2x, "Blood loss trauma" 2x.
- Among the ways to train it, the game's own tooltip for Toughness names "Get up and fight instead of playing dead".
- The character then faces the same enemies again, usually with a vital part still below 0.

## Toughness: safest ways to train early
Also: lose fights safely, starving bandits toughness, who to lose to
- Lose to enemies that do not enslave or eat the unconscious. The wiki recommends Starving Bandits: Iron Clubs (mostly stun damage), take only food, then leave.
- Before the fight, put food in a backpack held in the inventory (not worn) or drop it, so it is not taken.
- Keep a second character far out of sight on PASSIVE to bandage afterwards: if the downed character senses a conscious ally, they just get up and no bonus is paid.
- When the downed character wakes and is playing dead, give any order to make them stand: this is the big XP gain. Expect to be knocked down again.
- Fight near a town gate with guards so that someone finishes the enemy.
- Avoid doing this near slavers, cannibals, Fogmen or hungry animals.
- Always carry a first aid kit: cuts do not heal without one.

## Dexterity: what it does
Also: DEX, dexterity stat, what dexterity affects
- Raises attack speed for all attacks (+0.00228 per level) and block speed.
- Supplies 60% of attack and block speed scaling; Melee Attack (for attacking) or Melee Defence (for blocking) supply the other 40%.
- Raises cut damage with weapons: half the cut scaling comes from Dexterity, half from the weapon skill.
- Speeds up reloading crossbows and turrets.
- Has no effect on Martial Arts damage, only on its attack speed.
- Attack speed caps at 1.2x and block speed at 4.0x.
- Lowered by injuries: -0.6% per 1% of chest or stomach health lost and per 1% of arm health lost; -34% for an arm below 0.
- Hunger: -0.2% per hunger point below 200, up to -20%.
- Wearing no armour and no backpack at all gives Dexterity x1.1 (also Dodge x1.1 and Stealth x1.2).

## Dexterity: how it is trained
Also: dexterity XP, train dexterity, dexterity grind
- XP is given per hit landed in melee, not per damage.
- XP = the Melee Attack (or Martial Arts) XP for that hit x cut damage / (cut + blunt damage) of the weapon.
- Katanas have no blunt damage, so they give the full ratio. Jitte and Heavy Jitte have no cut damage and give none.
- Martial Arts always counts as pure cut, so unarmed fighting gives the full ratio.
- Lower-quality weapons have more cut relative to blunt and do less damage, so fights last longer: use Rusted Junk (also -1 attack and defence).
- Sabres train it faster than katanas, because sabres lower your attack (raising the opponent multiplier) while katanas raise it.
- Reloading crossbows trains it only very slowly.
- Training Melee Attack on dummies first lowers later Dexterity gains.

## Perception
Also: ranged accuracy, perception training
- Governs accuracy with crossbows and turrets, especially against far or moving targets, and affects range.
- Trained by aiming and shooting crossbows and by operating turrets.
- Reduces crossbow accuracy deviation together with the Crossbows skill.
- Dust storms lower it by up to 20%.
- Headgear bonuses: Sandogasa +6, Straw Hat +6, Ashland Hat +4, Ashlander Stormgoggles +4, Iron Hat +4, Rattan Hat +4, Square Goggles +2.
- Head injuries lower it.
- Races: Hive Prince 1.2x, Hive Soldier Drone 0.8x.

## Athletics: what it does and how it is trained
Also: run speed, running XP, movement mode, jog, walk
- Athletics sets maximum run speed; each level adds the same step between the race's level 0 and level 100 speeds.
- XP is gained whenever the character moves on land (walking counts), except while manoeuvring in a fight.
- Athletics XP % (bottom-left panel) = 100% minus Encumbrance %, times 1.5 while moving faster than 80% of maximum run speed. Tooltip lines: "Encumbrance penalty", "Full speed bonus: +50%".
- So run mode at 0% Encumbrance gives 150%; walk or jog mode, a bad leg or a heavy load loses the bonus.
- Injured legs, hunger and Encumbrance reduce speed directly, not the skill.
- Upright run speed never falls below about 2.5 mph; a crawling character moves at about 1.1 mph.
- Only legwear and footwear can carry Athletics penalties: medium armour as low as 0.85x, heavy as low as 0.80x.

## Athletics: fastest safe training
Also: train running, athletics grind, outrun enemies
- Empty the inventory until Encumbrance reads 0%, set run mode, and send the character on long trips or back and forth inside town walls.
- Every journey trains it, so travel light when the goal is speed rather than Strength.
- Early levels come fast: the wiki advises training it as much as possible at the start, because without a few levels running from danger is hard.
- Swap goals by need: carry weight on safe ground for Strength, drop it for Athletics.
- A Greenlander gains about 0.11 mph per level (15.7 mph at 0, 26.8 mph at 100).

## Swimming
Also: swim speed, water, drowning, swim training
- Swimming sets speed in deep water: units = 6 + level x race multiplier x 0.38; about 1.3 mph at level 0 and 9.8 mph at level 100 for humans and Hive.
- Trained only by swimming. Carrying another character doubles the XP.
- Characters cannot drown and can swim indefinitely.
- No Strength XP is earned while swimming.
- Animals can still attack in shallow water; in deep water attack and block speed are cut to 0.8x.
- Water in the Deadlands and Vain is acidic and hurts everyone except Hive races and Skeletons; armour protection does not help.
- Safe water for training: off most coasts. Floodlands, Wend, South Wetlands and The Swamp have water but also dangerous animals.
- Robot limbs reduce swim speed.

## Stealth: what it does
Also: sneak skill, sneaking, detection, being seen
- Turn on the SNEAK button; an eye and a sun appear above the character.
- The eye is blue while unseen, yellow while inside someone's line of sight but not yet noticed, red once spotted; the full reading is under "Stealth indicators (eye and sun)" in Interface.
- Sun: how much light is on the character. It is half-dimmed in dim light and fully shaded in darkness.
- A character in darkness cannot be seen by NPCs standing in light; a character in light is seen from far away.
- Detection depends on cover, distance, light, carried weight and armour, and wounds.
- Stealth also governs how well disguises work and avoiding recognition with a bounty.
- At effective Stealth above 30 the character sneaks at a run, with a different animation.

## Stealth: how it is trained
Also: stealth XP, sneak training, sneaking in town
- XP is earned only while SNEAK is on and someone is sensed nearby (enemy or neutral).
- Relative rates in the game's code: 0.2 with only neutrals around; 0.9 with enemies about but none noticing you; 1.5 while an enemy is noticing or detecting you.
- Standing still cuts the rate to one tenth. Nothing is gained while knocked out, carried, in a bed or in a cage.
- Being spotted does not stop the XP.
- Safe and slow: sneak around a town, or leave SNEAK on while mining outside a gate.
- Fast and risky: sneak near hostile animals, retreating when the eye turns red (wiki example: blood spiders at the Lost Library north-east of Rebirth).
- While sneaking, right-clicking a person can order a stealth knockout: assault in a town.
- Remove armour with a Stealth penalty. Carrying a body multiplies Stealth by 0.75.

## Stealth: equipment bonuses and penalties
Also: ninja rags, assassin's rags, stealth armour, naked bonus
- Wearing nothing: +20% Stealth.
- Ninja Rags: +30%.
- +10% each: Assassin's Rags, Basket Hat, Black Rag Shirt, Dark Leather Shirt, Dustcoat, Ninja Gi, Ninja Pants, Swamp Ninja Mask.
- Stealth Leg (left) and Stealth Leg (right) robot limbs: +25% each at Masterwork.
- Medium armour class multiplies Stealth by 0.9; heavy armour by between 0 and 0.4; chain and plate materials reduce it further.
- Backpacks: Small 0.85x, Medium 0.50x, Large 0.25x, thieves backpacks 1.00x.
- Black Plate Jacket is a medium body armour with no Stealth penalty.
- Leg and torso injuries reduce Stealth.

## Lockpicking: how it works
Also: pick lock, locked door, locked chest, padlock cursor, lock level
- A locked door or container shows a padlock cursor.
- To pick it: hold right-click and choose "Lockpick", or hold ALT and right-click. No tools are needed.
- A bar fills; at the end of each cycle there is a % chance of success, shown in the bar.
- Chance = 90 / 2^((lock level - Lockpicking) / 10), capped at 90%.
- Below 5% the character cannot even try; that happens when the lock is about 41.7 levels above the skill. A level 100 lock needs Lockpicking 58.3.
- With Lockpicking 0, a level 40 lock is possible (5.6%); a level 50 lock is not.
- Picking a lock on someone else's property is a crime if seen; you stay "criminal" for about 3 seconds after stopping.
- Imprisoned characters get -10 Lockpicking.

## Lockpicking: training
Also: lockpicking XP, cage training, Locksmith Training Box
- A successful pick gives 5 times the XP of a failed one. Lock difficulty does not change the XP, so pick easy locks repeatedly.
- Best early method: get into an empty Prisoner Cage (hold right-click, "get in"), pick your way out, get in again. The cage re-locks each time.
- Use cages away from guards, such as in the ruins of Bast; in a populated town the guards just let you out. Police stations in towns also have cages.
- Locked gates in ruins re-lock when closed, so they can be picked repeatedly.
- Locksmith Training Box caps: 11 (basic), 21 (II), 30 (III). Slow. They stand in Shinobi Thieves towers; use them while sneaking unless you have joined the Thieves, and stop if seen.
- Hive Prince is the only race with a Lockpicking bonus (1.2x).

## Thievery: how it works and XP
Also: stealing skill, steal chance, thievery XP
- Items with a red name belong to someone. Taking one from the world requires holding ALT and counts as stealing; success is 100% if unseen.
- Stealing from a container uses the Thievery skill; NPCs standing close lower the chance.
- After a theft a short timer (bottom left) must run out before you are in the clear.
- XP is gained only when the success chance is below 98%.
- XP at level 0 (100% is one level): caught stealing from a container but not attacked 240%; failing to steal from a sleeping or playing-dead character 240%; stealing from a container unseen 60%; caught selling stolen goods 60%; taking an item off the floor 30%.
- Selling stolen goods to another faction always works; to the owner's faction the chance is 20% + 0.42 x Thievery. They sell for half value.

## Thievery: safe training
Also: thief training, steal junk, drop and re-steal
- Start with red-named items lying on shelves and floors in ordinary houses: small XP, no failure roll, and being caught there does not ban you from shops.
- Sneak, work at night, and keep line of sight blocked.
- Drop the stolen items and pick them up again, repeatedly.
- Being caught stealing from a shop bans your whole faction from that shop for good, so do not practise there.
- Check a container before trying: click it; "[EMPTY]" means nothing inside. Locked containers always hold at least one item.
- Unconscious characters give no Thievery XP; sleeping ones do.
- Stolen junk can be sold to any vendor of a different faction.

## Assassination
Also: stealth knockout, knock out from behind, KO attempt
- Used for stealth knockouts: while sneaking, order a knockout on a humanoid target (not animals).
- Sets the chance of success and how long the victim stays out.
- The target's Toughness, Assassination, Thievery or Melee Defence reduces the chance, whichever counts most; Toughness and Assassination count double.
- Both success and failure give XP; a failed attempt gives 3 times as much.
- A failed, noticed attempt is assault: in towns it brings a bounty and possibly jail.
- Assassination Dummy caps: 10, 20 (II), 29 (III). They stand on the first floor of Shinobi Thieves towers (for example in The Hub) for members.
- Armour multipliers: Assassin's Rags 1.30x, Ninja Rags 1.10x; Plate Jacket 0.80x, Mercenary Plate 0.70x, Samurai Armour 0.50x, Crab Armour 0.20x.

## Melee Attack
Also: attack skill, hit chance, attack XP
- Decides how often you are the one attacking, how likely the enemy is to block, and adds a little attack speed (+0.00152 per level).
- Each point of your attack above the enemy's defence removes 1.5% from their block chance (base 70%); each point below adds 1.2%.
- Each point of attack above the enemy's attack adds 2.5% to your odds of taking the next attack; a 40-point lead means you attack twice for each of theirs.
- Trained by attacking with any weapon. A blocked attack gives about half the XP of a hit.
- XP follows Stronger Opponent Logic against the enemy's Melee Defence.
- Training dummies raise it only to 5, 10 or 15.
- Races: Shek 1.2x, Hive Soldier Drone 1.2x.

## Melee Defence
Also: defence skill, block chance, block XP, defense
- Used only when a weapon is equipped: an armed character blocks; an unarmed one dodges instead.
- Sets block chance and adds block speed.
- Block chance tops out at 95% when your defence is at least 21 levels above the attacker's attack; it never falls below 5%.
- Trained by being attacked while armed. Failing to block gives 8 times the XP of a successful block.
- XP follows Stronger Opponent Logic against the attacker's Melee Attack.
- The BLOCK button adds 20 to defence while it is on.
- Arm and head injuries reduce it.
- No race has a modifier.

## Training Melee Attack and Defence safely
Also: combat training early, fight with guards, train fighting
- Fight beside town guards: lure a bandit group to a guarded gate, wait until the guards are engaged, then join in. The guards win; you collect XP.
- The Hub has no town guards; only the Trade Ninja guards at its bar attack Dust Bandits, Starving Bandits and Bonedogs that come near.
- Keep one character out of the fight on PASSIVE with a first aid kit.
- Use a Rusted Junk weapon: less damage means longer fights and more hits, plus -1 attack and defence for a better opponent multiplier.
- Wear the best armour you have; XP does not depend on damage taken.
- Bandage the losers afterwards for Field Medic XP.
- Advanced: gear that lowers attack or defence (see the gear section) multiplies XP but makes you lose more.
- Hit and run with a fast character: strike once, back off, repeat.

## Training Dummy (Mk I, II, III)
Also: training dummies, dummy cap, police station dummy
- Trains Melee Attack only. No weapon skill, Dexterity or Strength.
- Caps: Training Dummy MkI level 5, MkII level 10, MkIII level 15. Past the cap the character keeps swinging but gains nothing.
- MkI dummies stand in police stations in towns. Using a faction's dummy may draw warnings; if you keep going after several warnings they attack.
- Building your own needs the Simple Training Dummies research and 4 Iron Plates.
- Raising attack on dummies first reduces later Dexterity XP, since Dexterity XP is scaled by your attack against the enemy's defence.

## Dodge
Also: evade, dodging, unarmed defence, dodge XP
- Used when unarmed, and by anyone who is attacked while stumbling.
- A character holding a weapon blocks instead of dodging.
- Chance is worked out like block chance: maximum 95% at 21 levels above the attacker's attack.
- Trained when attacked while unarmed, while busy (sleeping, lockpicking, bandaging) or while staggered.
- Being hit gives at least twice the XP of a successful dodge.
- Dodge XP is reduced by your Encumbrance %: 40% Encumbrance means 60% XP.
- Encumbrance also cuts the skill itself by up to 60%, and backpacks and heavy armour multiply it down.
- The BLOCK button adds 20 to Dodge (only when unarmed) but reduces Dodge XP.
- Leg injuries cut Dodge by up to half.
- Races: Scorchlander 1.2x; Shek 0.8x; Skeleton 0.8x.

## Martial Arts: what it does
Also: unarmed, fists, punching, kicks, martial arts damage
- The skill for fighting with no weapon equipped. It replaces Melee Attack, Melee Defence and the weapon skill.
- Damage of a 100-power attack = (2.5 + 0.075 x Martial Arts) x (1 + 0.1 x Strength + 0.08 x Toughness).
- At level 0 in all three the damage is 2.5: a new character's punches are nearly useless.
- Dexterity adds attack speed only.
- New techniques unlock with level: Kicklow at 5, Shotei at 15, Double Strike at 25, Jump Kick at 30, Double Punch Mid at 35, Mega Kick at 45, Jump Knee Strike at 55. The starting "Bad Punch" is dropped at 20.
- Fighting indoors gives +8 Martial Arts.
- Unarmed hits never cause bleeding.
- Organic fists deal only 60% damage to Skeletons and robots.
- A technique needs its limbs above 0 health.

## Martial Arts: training and recoil damage
Also: unarmed training, hurting own hands, recoil
- XP follows Stronger Opponent Logic against the enemy's Melee Defence (or Martial Arts). A blocked attack gives half.
- Organic characters hurt themselves when they hit: against no armour, cloth or leather they take stun damage of 1 - (Martial Arts + Toughness) x 0.005 per hit; against chain the same in cut and stun; against metal plate or a Skeleton, 2 - (Martial Arts + Toughness) x 0.01 in each.
- Recoil stops once Martial Arts + Toughness reaches 200, or with robot limbs. Skeletons take none.
- So train first on unarmoured or lightly armoured enemies.
- Encumbrance lowers the effective skill (-0.8% per 1%), raising the XP multiplier and training Strength too.
- Backpacks do not lower Martial Arts.
- Bonuses: Martial Artist Bindings +4, Assassin's Rags +6, Armoured Rag Skirt +4. Penalties: Samurai Armour -10, Samurai Legplates -10, Samurai Boots -5.

## Weapon skills (Katanas, Sabres, Hackers, Heavy Weapons, Blunt, Polearms)
Also: weapon class skill, katana skill, sabre skill, weapon XP
- Each weapon class has its own skill, raised only by fighting with a weapon of that class.
- The skill raises damage with that class: it supplies half of cut-damage scaling (Dexterity the other half) and a quarter of blunt-damage scaling (Strength the rest).
- XP follows Stronger Opponent Logic: your weapon skill against the enemy's Melee Defence (or Martial Arts if they are unarmed).
- A blocked attack gives 40% of the XP of a landed one. Blocking gives a much smaller amount.
- Training dummies do not raise weapon skills.
- Injuries do not lower weapon skills directly, but they lower Strength and Dexterity.
- Race modifiers: Skeleton Heavy Weapons 1.2x; P4 Unit Katanas 0.8x; none otherwise.

## Crossbows skill
Also: ranged skill, crossbow accuracy, crossbow training, aiming
- Affects accuracy, aiming and reload speed with hand-held crossbows.
- Accuracy deviation shrinks by a percentage equal to Perception + Crossbows; reload time depends on Crossbows + Dexterity (each counted up to 100).
- XP is gained while aiming and reloading, not per shot, so rate of fire does not matter.
- A character gains XP aiming at a target even without line of sight, so "attack" orders on an unreachable enemy train the skill without shots.
- Gear: Assassin's Rags, Ninja Rags and Drifter's Leather Jacket each 1.10x; Steady Arm (left) up to +25%.
- Head injuries lower it.
- A weak crossbow such as the Tooth Pick is the suggested training weapon because friendly fire with it does little harm.

## Turrets skill
Also: mounted crossbow skill, harpoon turret skill, Training Turret
- Affects accuracy and reload speed on turrets (each runs from 25% at level 0 to 125% at the top) and friendly-fire avoidance (0% at level 0, 100% at level 50).
- Trained only by operating turrets: Mounted Crossbow, Harpoon Turret and their upgrades, or the Training Turret.
- Training Turret caps: the upgrade table lists 11 (MkI), 21 (MkII), 31 (MkIII); the building's own description says it trains "up to level 5".
- Operating a turret also trains Perception; reloading trains Dexterity.
- Turrets need no ammunition. Mounted Crossbows need no power.
- Races: Hive Worker Drone 1.2x, Skeleton 1.2x.

## Precision Shooting
Also: friendly fire skill, friendly fire avoidance, avoid hitting friends
- The ability to avoid hitting allies with crossbows and turrets.
- Each level adds 1.5% friendly-fire avoidance, reaching 100% at about level 67.
- It is trained only by accidentally shooting your own allies. Shots that miss them give nothing.
- Armour that modifies the Crossbows stat also modifies it.
- Reduced in dust storms, in the dark and with head injuries.
- Until it is high, keep crossbow users at an angle where squad members are not between them and the target.

## Field Medic
Also: medic skill, bandaging speed, first aid skill, medic XP
- Sets bandaging speed: about 3 + 0.42 x skill health points per second, with the skill capped by the kit's quality (Basic First Aid Kit 5, Standard 40, Advanced 100).
- Treating yourself uses only 80% of the skill.
- Sets how fast kits are used up: about 2 charges per second of bandaging at skill 0, falling to 0.1 at skill 100. A beginner empties a 150-charge Basic kit in a little over a minute of bandaging.
- Also sets how much a Splint Kit can restore.
- XP is based on time spent treating, so slow basic kits give more XP per wound.
- Trained by bandaging anyone, animals included; crafting at a Medical Workbench trains it slowly.
- Head injuries lower the displayed skill by 0.45% per 1% of head health lost.
- Races: Hive Prince 1.2x, Hive Soldier Drone 0.8x.

## Robotics
Also: repair skill, robotics skill, repairing robots
- The medic skill for Skeletons and robot limbs: repair speed = 3 + 0.42 x Robotics, using Skeleton Repair Kits.
- Also sets crafting speed and quality at a Robotics Bench and Skeleton Limb Bench.
- Trained by repairing Skeletons or robot limbs and by crafting robotic parts.
- Darkness and head injuries lower it.
- Races: Skeleton 1.2x; Shek 0.8x; Hive Soldier Drone 0.8x.

## Science
Also: research speed, prospecting
- Sets research speed and the range and accuracy of Prospecting.
- Trained by working at a Research Bench or an Electrical Workbench.
- Head injuries lower it.
- Races: Greenlander 1.2x, Hive Prince 1.2x; Shek, Hive Soldier Drone, Hive Worker Drone 0.8x.
- Not useful to a wandering character until there is a building to research in.

## Engineer
Also: engineering, building speed, construction skill
- Sets how fast a character builds and repairs structures.
- Trained by building, repairing, dismantling, and producing Copper Alloy Plates.
- Several characters working on the same construction all gain XP.
- A known grind: partly dismantle (right-click option) and rebuild your own finished object repeatedly; both actions give XP and no extra materials are used unless it is fully dismantled.
- Races: Hive Worker Drone 1.2x; Hive Soldier Drone 0.8x.

## Labouring
Also: mining skill, labour, ore mining speed
- Sets the speed of mining and of running simple machines.
- Trained by doing the work: mining a Copper or Iron deposit trains it anywhere, with no research or base needed.
- Shift+right-click a deposit to make mining a standing job.
- Mining next to a town is the safe early money-maker and trains Labouring at the same time; putting the ore in an unworn backpack in the inventory then trains Strength on the walk back.
- Leaving SNEAK on while mining near a gate adds a trickle of Stealth XP.
- Arm and torso injuries lower it.
- Races: Hive Worker Drone 1.2x; Scorchlander, Shek, Hive Prince 0.8x.

## Farming
Also: harvest skill, crops
- Sets farming speed and the chance of a successful harvest.
- Trained by working farms. Some towns have farms a visitor can work: Holy Farms, Drifter's Last and towns in The Swamp.
- Races: Greenlander 1.2x, Hive Worker Drone 1.2x; Scorchlander, Shek, Hive Soldier Drone 0.8x.

## Cooking
Also: cooking skill, brewing
- Sets how fast food is cooked and drinks are brewed. It does not change food quality or unlock recipes.
- Trained by cooking at a Cooking Stove or campfire, or brewing.
- Races: Greenlander 1.2x; Scorchlander, Hive Soldier Drone, Hive Worker Drone 0.8x.

## Weapon Smith, Armour Smith, Crossbow Smith
Also: crafting skills, smithing, weapon quality, armour quality
- Weapon Smith: crafting speed and quality of weapons at a Weapon Smithing Bench.
- Armour Smith: speed and quality of armour; also trained while making the materials for armour.
- Crossbow Smith: speed and quality of crossbows, and speed of making bolts.
- All are trained only by crafting at the matching bench.
- Working in darkness slows production but does not change XP per time.
- Races: Scorchlander 1.2x and Hive Soldier Drone 0.8x for Weapon Smith and Armour Smith.

## Skill penalties from injuries
Also: wounded stats, injury debuff, damaged arm, damaged head
- Arms and torso (best arm x worst of chest and stomach): Strength (down to -22.5%), Dexterity (to -60%), Melee Attack and Martial Arts (to -30%), Labouring, Engineer, smithing and Farming (to -75%), Swimming.
- Head: Science, Robotics, Cooking, Field Medic, Turrets, Perception, Crossbows (to about -45%).
- Arms and head: Melee Defence (to -20%).
- Arms: Thievery and Lockpicking (to about -45%).
- Legs: run speed, not the Athletics skill (no penalty above 55.6% leg health), and Dodge (to -50%).
- Legs and torso: Stealth.
- Toughness and the weapon skills are not reduced directly.
- An arm below 0 health (or missing): a further -34% Strength and Dexterity. With both arms disabled, labour, craft and thieving skills fall to almost nothing.
- In poor light, crafting, Science, Perception and Crossbows are reduced as well.

## Skill penalties from hunger
Also: starving stats, malnourished, hungry debuff
- Penalties start when hunger falls below 200 and grow until 100. The status word is "Hungry" (or "Malnourished" once fed and recovering), then "Starving" below 100.
- At 100 or less, from a code-based reference: Strength -90%; Swimming about -50%; Labouring, Engineer, smithing and Farming about -37%; Science, Robotics, Cooking, Field Medic, Turrets and Crossbows about -30%; Perception about -27%; Thievery and Lockpicking about -19%; Dexterity -18% (the wiki says -20%); Athletics -15%; Melee Attack and Martial Arts -7.5%; Melee Defence -5%.
- Toughness, Dodge, Assassination and the weapon skills are not affected.
- Movement speed falls to as little as half.
- Slaves are kept at about 100 hunger, which is why they fight and run so badly.
- Keep hunger above 200 before any fight or escape.

## Training equipment caps (dummies, lock boxes, turrets)
Also: training building caps, max level from training
- Training Dummy MkI / MkII / MkIII: Melee Attack to 5 / 10 / 15.
- Assassination Dummy / II / III: Assassination to 10 / 20 / 29.
- Locksmith Training Box / II / III: Lockpicking to 11 / 21 / 30. Thief Training Boxes: Thievery to 11 / 21 / 30.
- Training Turret MkI / MkII / MkIII: Turrets to 11 / 21 / 31 (the item description says 5 for the first).
- Past the cap the character keeps "training" with no gain: move them off.
- Assassination Dummies and Locksmith Training Boxes are found in Shinobi Thieves towers; Training Dummy MkI in police stations.

## Gear that lowers your stats to speed up training
Also: training weights, stat malus gear, tin can, large backpack
- Lower effective skill means a higher opponent multiplier (up to x6) but real danger.
- Melee Attack: Tin Can -5; Hive Prisoner Shackles -15; Crab Armour -10; Samurai Armour -8; Large Backpack or Traders Backpack Large -10; Rusted Junk Holed Sabre or Foreign Sabre about -5; heavy weapons indoors -6.
- Melee Defence: Armoured Hood -2; Hive Prisoner Shackles -15; Armoured Rags -5; Large Backpack -10.
- Martial Arts: Samurai Armour -10, Samurai Legplates -10, Samurai Boots -5, plus Encumbrance.
- Penalties from several items add up.
- Base XP still follows your real level; only the opponent multiplier changes.

## Training while enslaved
Also: slave training, slavery stats
- Slavers bandage slaves after beating them and keep them fed to about hunger 100, so failed escapes are survivable.
- Stealth: leave SNEAK on the whole time.
- Lockpicking: pick your own shackles and cage, and neighbouring cages.
- Thievery and Toughness: escape attempts train both.
- Strength and Martial Arts gain from the constant hunger penalty lowering effective stats.
- Costs: all gear is confiscated, healing in a cage is slow, and after escaping the character is hunted as an escaped slave for several game days.

## Sources
- https://kenshi.fandom.com/wiki/Statistics : list of stats, what each does, medic and robotics speed formula, racial multipliers.
- https://kenshi.fandom.com/wiki/Guide_to_Training_Statistics : XP formula, level multiplier, training order, methods for every skill, malus gear lists.
- https://kenshi.fandom.com/wiki/Stronger_Opponent_Logic : opponent multiplier rules, which skills are compared, outnumbered bonus, block XP ratios.
- https://kenshi.fandom.com/wiki/Strength : carry formula, walking XP (25% at 70%, 50% carrying), combat XP, requirement, blood formula, hunger penalty.
- https://kenshi.fandom.com/wiki/Encumbrance : carry weight, labels, penalties.
- https://kenshi.fandom.com/wiki/Combat_Speed : speed formulas, strength shortfall, encumbrance threshold, examples.
- https://kenshi.fandom.com/wiki/Backpacks : backpack reductions and penalties.
- https://kenshi.fandom.com/wiki/Toughness : formulas, XP scaling, playing dead tip.
- https://kenshi.fandom.com/wiki/Update:0.61 : Toughness bonus for getting up, multiplied by enemies.
- https://kenshi.fandom.com/wiki/Dexterity , /Perception , /Athletics , /Swimming , /Stealth , /Lockpicking , /Thievery , /Assassination : effects, formulas, training notes, equipment.
- https://kenshi.fandom.com/wiki/Melee_Attack , /Melee_Defense , /Dodge , /Martial_Arts : combat skill numbers, techniques, recoil, damage formula.
- https://kenshi.fandom.com/wiki/Training_Dummy , /Assassination_Dummy , /Locksmith_Training_Box , /Training_Turret : caps.
- https://kenshi.fandom.com/wiki/Crossbows , /Turrets , /Precision_Shooting , /Harpoon_Turret : ranged skills.
- https://kenshi.fandom.com/wiki/Field_Medic , /Robotics , /Engineer , /Labouring , /Cooking , /Medical_Items : science and trade skills, head-injury penalty.
- https://kenshi.fandom.com/wiki/Getting_Started : early training advice, dummies in towns, farms, guards.
- https://kenshi.fandom.com/wiki/Combat_Strategies , /The_Hub , /Trade_Ninjas : The Hub has no town guards but its bar has Trade Ninja guards; hit and run.
- https://kenshi.fandom.com/wiki/Damage : skill penalties by body part.
- https://kenshi.fandom.com/wiki/Hungry_Bandit , /Starving_Bandits : enemies that only take food.
- https://kenshi.fandom.com/wiki/Slavery , /Prisoner_Cage : training while enslaved, cage commands.
- https://kenshi.fandom.com/wiki/Armor_Stats : class multipliers for athletics and stealth.
- https://github.com/VlcekM/meitouclient (local clone, third-party reference worked out from the game's code and data; only its statements about the original game were used): docs/game/character-stats.md (carry capacity and encumbrance formula, XP events, walking Strength rate, Athletics and Stealth rates, Toughness get-up bonus, stat multipliers for hunger and injury, first aid rate and kit drain, constants); docs/game/ui-screens.md (tooltip lines for Athletics XP, Strength XP, Toughness XP, Dodge); docs/game/pathfinding.md (speed floor and crawl speed); docs/game/locks.md (lockpick chance, confirming the wiki).
- Thief Training Box caps merged in from Research, crafting and building rest on the sources listed there.
