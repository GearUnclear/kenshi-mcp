# Health and medical

Body-part health, blood, knockouts, playing dead, first aid, splints, beds, carrying the wounded, limb loss and robot limbs, Skeleton repair, hunger and food, and what kills a character permanently in unmodded Kenshi 1.0.x.

## Reading the health panel
Also: health bars, condition, blood bar, arrows, wound icons, bar colours
- The selected character's health pane lists Blood (Oil for Skeletons) on the top line, then Head, Chest, Stomach, Left Arm, Right Arm, Left Leg, Right Leg.
- Each part has its own bar and number. Bars stop at 0 but the number can go negative.
- Arrows "<" over Blood mean bleeding: one arrow per 0.05 blood lost per second; one to three is usual.
- "<" beside a body part means 20 or more unbandaged cut damage there: the wound is getting worse. "<<" means the cut damage exceeds the part's whole maximum and it is worsening about 4 times faster.
- Bar colours, per a wiki guide: green is health; yellow is bandaged health regenerating; red is damage needing a kit; black is health only rest restores.
- The bottom-left panel can be expanded to show the KO point.

## Body parts and what each controls
Also: head, chest, stomach, arms, legs, vital parts, limb function
- Vital parts: Head, Chest, Stomach. Any one of them below 0 from a hit knocks the character out; any one below minus its maximum kills.
- Head damage lowers Field Medic, Robotics, Science, Cooking, Turrets, Perception and Crossbows, and (with arms) Melee Defence.
- Chest and stomach damage (the worse of the two) lowers Strength, Dexterity, Melee Attack, Martial Arts, labour and craft skills, and Stealth.
- Arms: an arm below 0 costs 34% Strength and Dexterity. With the right arm unusable the character cannot use weapons; two-handed weapons and crossbows need both arms.
- Legs: run speed drops once leg health falls below 55.6% of maximum; a character whose legs are disabled can only crawl.
- Arms and legs can be severed; vital parts cannot.

## Which wounds need a bandage: cut damage, not stun
Also: blunt damage healing, cut healing, does it heal by itself, yellow and red bars
- Stun damage (from blunt weapons, fists, acid rain, and the part of a cut that armour converts) heals by itself over time, awake or unconscious. No kit is needed.
- Cut damage (blades, bites, bolts) never heals until it is bandaged with a first aid kit, however long you wait.
- Once bandaged, the damage becomes "bandaged health" that regenerates over time, faster in a bed.
- Unbandaged cut damage of 20% or more of a part's maximum gets worse on its own.
- Robot parts and Skeletons need a Skeleton Repair Kit instead of a first aid kit.
- So after any fight with cutting weapons, bandaging comes before resting.

## Knockout: when a character goes down
Also: unconscious, KO, knocked out, rebooting
- A hit that takes Head, Chest or Stomach below 0 health knocks the character out.
- Blood falling to 0 also knocks them out.
- Hunger below 100 + KO point (90 at Toughness 0) causes repeated fainting.
- A successful stealth knockout (Assassination) does the same.
- Arm damage alone does not knock out. A leg going "down" while standing causes a 3-second knockout, after which the character crawls.
- A knocked-out character shows "Unconscious" ("Rebooting" for a Skeleton), drops out of the fight, and can be looted, carried, enslaved or eaten.
- They wake when the knockout timer runs out, provided they are not in a recovery coma and blood is above 0.

## KO point and recovery coma
Also: coma, critical, cannot get up, will not wake
- KO point = -10 - 0.75 x Toughness: -10 at Toughness 0, -47.5 at 50, -85 at 100.
- If a vital part (Head, Chest, Stomach) falls below the KO point, the character enters a Recovery coma.
- In a coma they stay down, whatever the knockout timer says, until every vital part is back above 0.
- A cut wound below 0 keeps degenerating unless bandaged, so an untreated coma ends in death.
- A new character's KO point is about -11: almost any knockout from cuts becomes a coma that needs someone else's bandage.
- A character above the KO point can get up again with a vital part still negative; one more hit there drops them at once.

## How long a knockout lasts
Also: KO time, knockout timer, wake up time, recovery timer
- From a code-based reference: seconds = 20 + k x (25 x the cut-minus-stun damage fraction of each of head, chest and stomach + an extra for every part below 0 + 50 x the fraction of blood missing).
- k depends on Toughness: 3 at Toughness 0, about 1.9 at 50, 0.75 at 100.
- Extra for a part n% below 0: head 2.25 x n, chest or stomach 1.25 x n, arm or leg 0.5 x n.
- Cut damage lengthens it and stun shortens it: club knockouts are short, deep cuts long.
- Example: Toughness 0, chest cut to -10 of 100, nothing else: 20 + 3 x (27.5 + 12.5) = 140 seconds.
- The timer restarts on every hit that leaves a vital part below 0.
- For player characters it runs down 1 to 2 times faster than game seconds.

## Wound degeneration (wounds getting worse)
Also: wound worsening, deteriorating, festering, untreated cut
- Starts when unbandaged cut damage on a part reaches 20% of its maximum health.
- Speed is 1x at 30% unbandaged cut damage and rises by 1x per extra 10%, to 7x at 90%.
- At 100% or more (the "<<" state) it runs about 4 times faster again and can outpace bandaging.
- Multiplied by Toughness: 1.7x at Toughness 0, falling to 0.03x at 100.
- It stops completely while the character lies in any bed, Camp Bed or Skeleton Repair Bed.
- Bandaging the part stops it.
- The new-game option "Chance of death" (0.5 to 4) multiplies both degeneration and bleeding.
- A degenerating vital part will reach minus its maximum and kill; a degenerating limb can be lost.
- Robot limbs and Skeleton arms and legs never degenerate; a Skeleton's head, chest and stomach do.

## Bleeding: how blood loss works
Also: blood loss, bleed rate, clotting, bleeding arrows
- Each cut or pierce hit opens a wound with bleed = damage after armour and Toughness x weapon blood loss / 1000.
- Blood lost per second = sum of open wounds x 1.2 x racial bleed rate.
- Each hit also removes blood at once: 20% of its cut and pierce damage x weapon blood loss x racial bleed rate.
- Wounds clot steadily by themselves; you bleed at the full rate only for a few seconds.
- Total blood lost by one untreated wound grows with the square of its size: one big hit is far worse than several small ones.
- Racial bleed rate: Greenlander 1, Scorchlander 0.9, Shek 0.9, Hive 0.3, Skeleton 0.1.
- Crossbows count as 2x blood loss; Katanas 1.1x to 1.3x; unarmed hits cause none.
- Bandaging stops the bleeding first, newest wound first.

## How to stop bleeding
Also: bleeding out, stop blood loss, blood arrows, bandage a bleed
- Arrows "<" over the Blood line mean the character is bleeding.
- Small bleeds clot and stop by themselves; heavy ones can empty the blood meter first.
- To stop it: a conscious character holding a first aid kit right-clicks the bleeding character (or themselves). First aid closes bleeding wounds first.
- An unconscious bleeder needs another character to do it.
- A stump from a lost limb bleeds steadily and does not clot: bandage it or fit a robot limb.
- Skeletons lose Oil the same way; use a Skeleton Repair Kit.
- Without a kit you can only wait for clotting.
- Blood starts to recover only when all bleeding has stopped; lying in a bed doubles the recovery.
- Always carry a Basic First Aid Kit (about c.76).

## Blood loss knockout and bleeding out
Also: blood zero, bled out, death from blood loss, negative blood
- Blood at 0: the character is knocked out.
- After waking from a blood-loss knockout, they are not knocked out by blood again until it falls to -25, unless it has recovered above 25 in between.
- Death comes when blood falls below minus the character's maximum blood: below -50 for a Hive character, -100 for a Skeleton, and -76 to -150 for a human or Shek depending on Strength.
- Maximum blood: Hive 50; Skeleton 100 (Oil); Greenlander, Scorchlander and Shek 75 + 0.75 x Strength.
- Life-threatening bleeds come mostly from very low Toughness, from losing a limb, and from pierce damage (turrets, animals).
- An unconscious character cannot bandage themselves, so someone else must.

## Blood recovery
Also: blood regeneration, regain blood, blood refill
- Blood does not regenerate at all while the character is still bleeding.
- After bleeding stops, a Greenlander regains about 3.2 blood per 22 game minutes according to the wiki (about 8.7 per game hour); a code-based reference gives 0.04 per second of medical time, which is 4.4 to 8.7 per game hour. It scales with racial heal rate.
- Resting in any bed, Camp Bed or Skeleton Repair Bed doubles blood recovery.
- Shek (heal rate 0.8) recover blood more slowly than Greenlanders; Scorchlanders (1.1) slightly faster; Skeletons (2) twice as fast.
- There is no item that restores blood directly. (unverified)
- A character woken from a blood-loss knockout is fragile until blood is back above 25.

## What kills a character for good
Also: death, permanent death, dying, how characters die
- Head, Chest or Stomach falling below minus its maximum health (below -100 for a Greenlander, -125 for a Shek, -75 for a Hive Worker's chest).
- Blood falling below minus maximum blood.
- Starvation: hunger reaching 0.
- Being eaten by cannibals, Fogmen or animals, or peeled in a Peeler Machine, once the damage reaches the vital parts.
- Friendly fire from crossbows or turrets.
- Death is permanent: there is no revival. Only loading an earlier save undoes it.
- Not fatal by themselves: knockouts, lost limbs (once the stump is bandaged), slavery, jail. The game's own tip: defeat is not always the end, since a squad member may recover in time to save the others.
- The usual chain is knockout, untreated cuts, degeneration, death. Bandaging breaks it.

## Playing dead
Also: play dead, staying down, pretending, fake death
- When a knockout ends, the character checks whether it is safe to get up. Safe means no conscious enemy is sensed nearby, or a conscious ally is. Downed enemies do not count.
- If it is not safe, they stay on the ground and the health panel reads "Playing dead...". It is automatic and lasts until it becomes safe.
- Any player order makes a character who is playing dead get up at once.
- A character with the Medic job set leaves playing dead to treat allies. A lone character may bandage themselves while down.
- The wiki says high-Toughness characters stand and fight on by themselves; a code-based reference shows only the safety check.
- Player reports: a looter may notice the character is alive and attack.
- Skeletons, through a bug, usually do not repair themselves while playing dead.

## Staying low (crawling after a knockout)
Also: staying low, crawl, wake up sneaking, crawl away
- If a character wakes from a knockout with SNEAK on and it is safe to get up, they do not stand: the health panel reads "Staying low" and they crawl.
- An order given to a character who is playing dead with SNEAK on also puts them into Staying low instead of standing.
- Crawl speed is about 1.6 mph (1.1 mph with a leg down). Stealth is doubled; blocking and dodging are impossible.
- To stand up: turn SNEAK off or pick a movement speed (walk, jog, run).
- Being attacked in melee also ends it.
- Use it to crawl a beaten character away from enemies that have lost interest, toward cover or a medic.

## Keeping a beaten squad down safely
Also: stay down, do not get up, let the enemy leave
- When everyone is down, select the squad and turn on PASSIVE and SNEAK.
- PASSIVE stops woken characters from attacking; with SNEAK on, a woken character crawls ("Staying low") instead of standing.
- Turn on HOLD or remove the Medic job so nobody stands up to bandage while enemies watch.
- Do not issue move or attack orders: any order makes a character who is playing dead get up.
- A character who wakes with a conscious ally nearby gets up by themselves, so one fighter still standing pulls the others back into the fight.
- Wait until the enemy group has walked away before bandaging, unless someone is about to die.
- A second character hidden at a distance on PASSIVE is the reliable way to recover the squad.

## Ordering a downed character to get up: when it is worth it
Also: force get up, stand up and fight, get up risk
- Ordering a character who is "Playing dead..." to stand while enemies are near gives a large Toughness gain, paid only if no conscious ally is nearby. The amounts are in "Toughness bonus for getting up while playing dead" in Stats and training.
- It also restarts the beating: with a vital part still negative, the next hit there knocks them out again.
- Sensible only against enemies that use clubs and do not enslave or eat, such as Hungry Bandits, and only with someone available to bandage afterwards.
- Knockouts from stun damage are short, so several rounds can be done in one fight.
- Never do it when a vital part is near the KO point or bleeding is heavy.

## First aid kits: types and stats
Also: bandages, medkit, basic first aid kit, standard first aid kit, advanced first aid kit, kit charges
- First aid kits treat cut damage on organic body parts of any non-Skeleton race.

| Kit | Charges | Quality | Average price |
|---|---|---|---|
| Basic First Aid Kit | 150 | 5 | c.76 |
| Standard First Aid Kit | 400 | 40 | c.147 |
| Advanced First Aid Kit | 1000 | 100 | c.265 |

- Weight: Basic 1 kg; Standard and Advanced 2 kg. Inventory size: 2x1, 2x2, 2x3.
- Quality limits the medic: a kit only lets Field Medic skill up to its quality count for speed.
- Charges are used as wounds are treated; higher Field Medic uses fewer per wound. A Basic kit goes fast: about 2 charges per second of bandaging at Field Medic 0.
- Kits found or bought may be partly used (random charges).
- Recipes at a Medical Workbench: Basic = 1 Fabrics (research Basic First Aid Kits); Standard = 1 Fabrics + 1 Hemp.
- "Medical Supplies" (c.120) is a trade good with no healing use.

## Bandaging rules: kits, patients and limits
Also: bandage rules, first aid rules, who can be healed, heal myself, heal ally, treat wounded, I don't have a medkit
- The kit must be in the medic's own inventory or worn backpack; kits held by the patient or other squad members are not used. With no kit the order is refused: "I don't have a medkit."
- Bandaging takes time and the game must be running. Another order interrupts it.
- Self-treatment works at 80% of Field Medic skill. It is impossible while unconscious or in a coma; a lone character who is playing dead may do it without standing.
- A patient can be conscious, unconscious, in a coma, or lying in a bed.
- Anyone can be treated: squad members, guards, townspeople, animals, and unconscious or playing-dead enemies. Conscious hostiles normally cannot be.
- Several medics can work at once, which is faster than one specialist.
- Treating a character gives a small relations gain with their faction and Field Medic XP.
- Which clicks: "First aid on yourself" and "First aid on someone else" in How-to.

## Order in which wounds are treated
Also: triage order, bandage priority
- First aid always works from the top of the health pane down: Blood (bleeding), Head, Chest and Stomach (either order), Left Arm, Right Arm, Left Leg, Right Leg.
- Bleeding wounds are closed newest first; nothing is bandaged until all are closed.
- Then parts are bandaged one at a time, so a patient with many injured parts takes proportionally longer and more charges.
- Kits in the character's own inventory are used before kits in a worn backpack.
- Among several kits, the one with the fewest charges left is used first.
- If kits are short, treat the character with the most negative vital part or the most blood arrows first.

## Field Medic skill and kit quality
Also: healing speed, medic speed, slow bandaging
- Medic speed = 3 + 0.42 x Field Medic.
- The kit's quality caps the skill that counts: Basic 5, Standard 40, Advanced 100.
- Higher skill also uses fewer charges per wound.
- A character with very low or negative Field Medic can even apply negative bandaged health.
- Head injuries reduce the medic's skill by 0.45% per 1% of head health lost.
- Skill does not change how fast bandaged health then regenerates; only beds do.
- Train it by bandaging everyone after every fight, including beaten bandits.

## First aid kits from loot: who carries them
Also: loot first aid kit, find medkit, free bandages
- Many NPCs carry a Basic First Aid Kit: common soldiers of the United Cities and Holy Nation, all Shek Kingdom and Hive military, and some bandit groups.
- Standard kits are carried by United Cities police and Bounty Hunters; Advanced kits by nobles and Holy Nation doctors.
- Loot kits from bandits beaten by town guards; that is legal. Take the kit before bandaging them.
- Carry at least one kit on every character; an unconscious medic's kit helps nobody unless another character has one too.
- Shops that stock kits: "Where to buy medical supplies" in Items and equipment.

## Triage after a lost fight (checklist)
Also: after combat, recovery steps, what to do when everyone is down
- Pause. Check each portrait and health pane: blood arrows, negative vital parts, "<" and "<<" marks.
- If enemies are still near, keep everyone down (PASSIVE, SNEAK) and wait.
- Bring in the hidden medic, or the first character able to stand.
- Bandage the worst first: most blood arrows, then most negative head, chest or stomach.
- Bandage any stump at once or fit a robot limb.
- Check food was not taken; hunger below 200 slows everything.
- Carry coma patients to a bed (8x healing, no degeneration); set a Camp Bed if no town is near.
- Splint legs below half health if you must walk.
- Save once everyone is stable.

## Splint kits
Also: splint, splints, rig limb, rigged health, advanced splint kit, broken leg
- A splint adds "rigged" health to a badly damaged organic arm or leg so it works again. It does not wear off and hits do not remove it.
- Splint Kit: 100 charges, quality 25, 2 kg, 2x2, average c.212. Rigs up to 26 health, if Field Medic is at least 25.
- Advanced Splint Kit: 100 charges, quality 50, 3 kg, 3x3, average c.311. Rigs up to 51 health.
- The amount rigged follows the medic's Field Medic skill, capped at kit quality + 1.
- Only for a limb below about 47.5 health; it cannot be raised above 50 effective health.
- The wiki says only bandaged cut damage can be splinted; a code-based reference says stun plus bandaged damage. Either way, bandage first.
- Rigged health counts against amputation. No use on vital parts.
- Recipe: 2.5 Fabrics + 1 Hemp at a Medical Workbench.
- NPCs never apply splints themselves, even when they carry one.

## How to splint a limb
Also: use splint kit, apply splint, Splint Injuries
- Put the kit in the medic's own inventory or worn backpack. Without one the order is refused: "I don't have a splint kit."
- Bandage the limb first.
- Hold right-click on the injured character (or their portrait) and choose "Splint Injuries".
- The standing job version is called "Splint Rigging"; it applies splints automatically.
- A white section on the limb's bar shows the rigged health; it may not be visible if the limb is deeply negative.
- Running at full speed needs leg health of 55.6% of maximum. With the 50 cap, only Hive Worker Drones (75 maximum) and Hive Princes (80) get back to full speed; others just limp faster.
- Splinting gives Field Medic XP.
- Player reports say the order sometimes fails; check the bar afterwards.

## Beds: healing rates
Also: bed heal speed, sleep, rest, 8x, recover faster
- Bed: organic health (stun and bandaged) heals at 8 times the normal rate. Camp Bed: 4 times.
- A code-based reference lists "Old Bed" at 1 (no bonus) and "Fish Bed" at 2, so read the bed's name.
- Skeleton Repair Bed: robot parts heal at 8 times; organic parts are not sped up, but the bed slowly bandages them.
- In any bed, blood (or oil) recovers twice as fast, hunger drains at one third the rate, and wounds do not degenerate.
- Unbandaged cut damage still does not heal in a bed: bandage first, then sleep.
- One character per bed.
- To use: select the character and right-click the bed; any other order gets them up ("Sleep in a bed" in How-to).
- Being held in a cage doubles the normal healing rate.

## Bed rental: prices and free beds
Also: bar bed price, inn, rent bed cost, free bed, sleep in town
- Beds and Camp Beds can be rented in bars and some other buildings in friendly towns and outposts, from as little as c.50.
- A rental lasts 24 hours. During that time a healed character can get up and a wounded squad member can take the same bed.
- United Cities bars (Small Empire Bar, Empire Bar, Empire Big Bar) charge c.150.
- Free beds: the upstairs of the Smugglers Bar in Shem; Camp Beds in wild camps (bandit camps and similar); some other locations too.
- Beds in barracks and private buildings are forbidden unless you are allied with the owning faction; using them is trespassing.
- Skeleton Repair Beds are rented the same way but cost c.200 to c.3,000.
- A rentable bed shows its price when clicked. Players describe a prompt to pay first; the code analysis in How-to finds the money is simply taken (unverified)
- Which clicks: "Rent a bed" in How-to.

## Natural healing without a bed
Also: heal over time, waiting to heal, regeneration
- Stun damage and bandaged health regenerate slowly by themselves while standing, walking or working.
- Only a bed speeds it: Bed x8, Camp Bed x4. Skills and food do not.
- The rate scales with the part's maximum health and the racial heal rate: Greenlander 1, Scorchlander 1.1, Shek 0.8 (with 125 health), Hive 1, Skeleton 2.
- Cut damage without a bandage never heals this way and may worsen.
- Hunger keeps draining while you wait, at one third the rate in a bed.

## How long healing takes
Also: healing speed, heal rate numbers, hours to heal, recovery time
- From a code-based reference: each body part regains 0.0125 health per second x (maximum health / 100) x racial heal rate, on a medical clock that runs 1 to 2 times game time for player characters.
- One game hour is about 109 real seconds at normal speed.
- Greenlander, up and about: roughly 1.4 to 2.7 health per game hour per part.
- Greenlander in a Bed: roughly 11 to 22 per game hour. Camp Bed: half that.
- So 100 points of bandaged or stun damage take about 5 to 9 game hours in a Bed, 9 to 18 in a Camp Bed, and 1.5 to 3 game days with no bed.
- All parts heal at once, so total time follows the worst part.
- Skeleton parts, once repaired, heal 250 times faster.

## Carrying: weight, risks and setting down
Also: carry wounded rules, carried body weight, put down, drag to safety
- The body adds 30 kg to the carrier, whatever it wears or holds; check the carrier's Encumbrance.
- The carrier needs a working left arm. A carrier who is attacked fights with the body still on the shoulder.
- Bandage before carrying when possible, so the patient does not bleed out on the way.
- Carrying also works on strangers, enemies and animals. Holy Nation characters generally ignore whoever is carried.
- A body that is not friendly to the carrier is knocked out again when set down, for longer with higher Assassination; friends are set down awake.
- Player reports: putting a body down can snap it back to where it was picked up; a bed avoids this.
- Which clicks: "Carry a downed character" and "Put a carried character in a bed" in How-to.

## Crippled limbs: effects
Also: broken arm, broken leg, limping, cannot fight, disabled arm
- Leg health below 55.6% of maximum: run speed falls. A leg that is negative but still above the KO point merely limps; below the KO point the character crawls (next section).
- An arm below 0: -34% Strength and Dexterity.
- Right arm below 0 or missing: no weapon use.
- Left arm unusable: no two-handed weapons, polearms or crossbows (the character switches to the sidearm or fists) and no carrying of bodies.
- Martial Arts techniques need their limbs: a disabled arm removes punches, legs remove kicks.
- Each disabled arm cuts swim speed to 0.6 times.
- Splints restore function temporarily; healing in a bed restores it properly.

## Leg down: when a character can only crawl
Also: crawling, crippled, cannot walk, leg collapse
- From a code-based reference: a leg is "down" when it is lost, crushed, or its health (bandages included) is below the KO point: -10 at Toughness 0, -47.5 at 50, -85 at 100.
- One leg down is enough.
- A standing character whose leg goes down is knocked out for 3 seconds and then can only crawl, at about 1.1 mph.
- A crawler cannot block or dodge and has only weak ground attacks; their orders and current fight are cancelled when they collapse.
- So a new character (KO point about -11) is crippled by a leg at -11, while a tough one keeps limping far below 0.
- Bandaging raises the leg's counted health; once it is back above the KO point the character stands again.
- A lost leg needs a robot leg.

## Limb loss (amputation)
Also: severed limb, lost arm, lost leg, dismemberment
- An arm or leg is severed when its health (any splint included) is below minus its maximum (below -100 for a Greenlander limb, -75 for a Hive Worker Drone, -125 for a Shek) and, on the default setting, it then takes a hit.
- The loss costs 5 to 30 blood on the spot, and the stump then bleeds as a 200-damage cut would.
- The stump has only 5 maximum health.
- The loss is permanent. Only a robot limb replaces it; a robot limb itself is never cut off.
- Uncommon in ordinary fights: the character is usually knocked out first.
- It is common when being eaten (Fogmen, cannibals, animals) or put in a Peeler Machine.
- Hive Worker Drones and Hive Princes, with low limb health, lose limbs most easily.
- Losing a limb gives a large one-off Toughness gain.

## Dismemberment setting
Also: limb loss option, never, rare, frequent
- A game option called "Dismemberment" sets how limbs are lost.
- Never: limbs are never severed.
- Rare (default): a limb below -100% of its maximum is severed only when it is then damaged by an attack.
- Frequent: a limb is severed the moment it falls below -100%, from any cause, including stun damage and wound degeneration.
- On Rare, an untreated limb can sit far below -100% and stay attached.
- Being eaten or peeled can take limbs on Rare and Frequent.

## After losing a limb: treat the stump
Also: stump, amputee first aid, bleeding stump, severed limb care
- A fresh stump bleeds heavily and steadily until bandaged; the steady part does not clot.
- Bandage the stump at once with a first aid kit.
- Alternatively fit any robot limb into the empty slot: this stops most of the bleeding immediately, and the limb can even be removed again afterwards.
- Hive characters (50 blood) can be knocked out by the instant blood loss alone.
- With one leg gone the character can barely move; with an arm gone they may be unable to use their weapon. Carry them.
- Severed limbs lie on the ground as items; Bonedogs take them. They cannot be reattached.

## Robot limbs: installing
Also: prosthetic, attach robot arm, limbs button, replace limb
- A character must already have lost the natural limb; healthy limbs cannot be swapped.
- Open the amputee's inventory window. The "Limbs" button becomes usable when a limb is missing.
- Click "Limbs", then drag the robot limb into the matching slot, or right-click the limb in the character's inventory.
- Left and right limbs are different items with similar icons; read the name before buying.
- An installed limb no longer counts toward Encumbrance.
- Robot limbs are repaired with Skeleton Repair Kits (Robotics skill), not first aid kits, and suffer wear that only a Skeleton Repair Bed removes.
- Cut damage to a robot limb on an organic character still causes bleeding.
- Wearing one makes the Holy Nation treat the character as a Skeleton.

## Robot limbs: arm types
Also: economy arm, skeleton arm, KLR arm, industrial lifter arm, steady arm, thief's arm
- Figures are for Masterwork grade; lower grades are worse, and bonuses only appear at High grade or above.
- Economy Arm: c.3,207, 95 health; Dexterity -20.7%, Lockpicking and Thievery -52.5%, Crossbows -11.5%.
- Skeleton Arm: about c.16,600 to c.18,400, 170 health; Dexterity +25%.
- KLR Series Arm: c.32,075, 245 health; Strength +10%, Dexterity +10%.
- Industrial Lifter Arm: c.25,660, 195 health; Strength +23.75%.
- Steady Arm (left only): c.25,660, 145 health; Crossbows +25%, Dexterity +20%. Cannot be crafted.
- Thief's Arm (right only): c.25,660, 145 health; Lockpicking and Thievery +25%, Dexterity +20%. Cannot be crafted.
- All arms reduce swim speed (mostly -25%). The listed "unarmed damage bonus" does nothing.
- Limbs use the armour grade names; shops mostly stock Shoddy to High, and the prices here are Masterwork values. A Thief's Arm helps Thievery only at High grade or better.

## Robot limbs: leg types
Also: economy leg, skeleton leg, KLR leg, stealth leg, scout leg
- Figures are for Masterwork grade.
- Economy Leg: c.4,561, 95 health; Athletics -14%, Stealth -14%, Swimming -50%.
- Skeleton Leg: c.18,293, 170 health; Athletics +10%, Stealth -42%.
- KLR Series Leg: c.27,367, 290 health; Stealth -52%, Swimming -50%.
- Stealth Leg: c.18,440, 170 health; Stealth +25%, Athletics +4%.
- Scout Leg: c.18,440, 145 health; Athletics +38%, Stealth -8%.
- One robot leg with one organic leg gives a limp at walking pace.
- Economy limbs have less health than a human limb (95 against 100), so they are disabled easily.

## Robot limbs: where to buy
Also: robotics shop, prosthetics shop, limb vendor
- Vendor types: Hive Robotics Shop, Robotics Shop, Robotics Workshop, Mongrel Robotics Workshop, Travel and Repairs Shop.
- Hive Robotics Shops (in Hive Villages) sell cheap Economy limbs. Hive player characters cannot trade there.
- The Robotics Shop in Black Desert City has the largest high-quality selection.
- Robotics Workshops stand in Heft, Heng, Black Scratch and the Waystation in the Border Zone; Mongrel has its own; World's End has Travel and Repairs.
- These places usually also rent Skeleton Repair Beds.
- Limbs also turn up as loot in ruins.
- They are equipment: they sell back for only half their value.
- Players can craft them at a Skeleton Limb Bench after late research.

## Skeleton repair: kits
Also: skeleton repair kit, authentic skeleton repair kit, repair robot, fix skeleton
- Skeletons and robot limbs are repaired with repair kits and the Robotics skill, never with first aid kits.
- Skeleton Repair Kit: 500 charges, quality 50, 2 kg, 3x2, average c.4,341. Recipe: 0.5 Robotics Components + 1 Steel Bars at a Robotics Bench.
- Authentic Skeleton Repair Kit: 100 charges, quality 20, 3 kg, average c.1,865. Despite the name it is the worse one.
- To repair: select a character holding a kit and right-click the damaged Skeleton, or hold right-click and choose "Repairs". A conscious Skeleton can repair itself.
- Repaired damage then heals at 250 times the base heal rate.
- Kits are sold in Adventurer shops and robotics vendors, found in ancient ruins, and carried by some Skeletons and United Cities Police Chiefs.
- Two always lie in the undefended Armoury Ruin in the south-east Deadlands.
- Stun damage on Skeletons heals by itself. Wear and repair beds: "Skeleton wear and tear" and "Skeleton Repair Bed locations and prices".

## Skeleton wear and tear
Also: wear damage, max health reduced, maintenance
- Every weapon hit on a Skeleton or robot limb lowers that part's maximum health by 4% of the cut, pierce and blunt damage taken.
- Example: a 200-damage hit leaves the part able to heal only to 192 until serviced.
- Wound degeneration, acid, fire and Peeler Machines do not add wear.
- Hover the part's bar to see wear (shown once above 5 points). Above 40 the tooltip recommends finding a Skeleton Bed.
- Only sleeping in a Skeleton Repair Bed removes wear; it takes seconds to minutes.
- A Skeleton Repair Bed also repairs cut damage without a kit, at roughly 1 health per 0.345 game minutes.

## Skeleton Repair Bed locations and prices
Also: repair bed rent, where to fix skeleton, free repair bed
- Free: Burn's Tower (Floodlands, 1 bed); Tower of Abuse (Venge, 2, hostiles present); Iron HQ (The Crags); Skinhouse (Sonorous Dark, dangerous for non-Skeletons).
- Black Desert City (Deadlands): Skeleton Bar, 5 beds at c.200; Robotics Shop, 1 at c.2,000.
- Shark (The Swamp): The Dancing Skeleton bar, c.400.
- World's End: Travel and Repairs, 2 beds at c.800. Flats Lagoon: 2 at c.800.
- Western Hive Villages: c.800.
- Mongrel (Fog Islands): c.1,600 and c.3,000.
- Robotics Workshops in Heft, Heng, Black Scratch and the Border Zone Waystation: c.2,000.
- The bed can also be researched (Skeleton Repair Beds) and built.

## Hunger: the scale and thresholds
Also: hunger meter, starving, malnourished, hungry, hunger numbers, fed, starve to death, hunger death
- Hunger runs from 0 to 300; a new character normally starts at 300. (One third-party guide says 400; the game's code caps it at 300.)
- 200 or more: no penalty.
- Below 250 with an empty stomach: the character eats automatically if food is in reach.
- 100 to 200: stat penalties, and movement slowed by up to half. The status word is "Hungry", or "Malnourished" once fed and recovering.
- Below 100: "Starving". The character passes out below a point set by Toughness: 100 + KO point, so 90 at Toughness 0 and 50 at a KO point of -50.
- At 0 the character dies.
- A character who has passed out still eats if food is in reach.
- Slaves are held at about 100. Skeletons have no hunger.
- Some game starts begin hungry: feed the character first.

## Hunger: how fast it drains
Also: hunger rate, food per day, how long without food
- Base: 100 hunger per 60 game hours at rate 1, about 40 per day (about 109 real minutes per 100 at normal speed).
- Race multiplier: Hive Prince and Worker Drone 0.5, Hive Soldier Drone 0.6, Scorchlander 0.9, Greenlander 1, Shek 1.25.
- Activity multiplier, from a code-based reference: standing idle 0.8; moving or fighting 1.0 plus 0.7 x Encumbrance (1.7 at 100%); mining 1.2; sitting 0.66 to 0.75; in a bed or knocked out 0.33.
- Hunger does not drain while food is being digested.
- From a full 300, a Greenlander has roughly 2.5 days before penalties (200) and about 5 before starving (100).
- The new-game option "Hunger time" (0.25 to 8, default 1) scales how long hunger lasts.

## Eating: how characters eat automatically
Also: how to eat, feed character, auto eat, food in inventory
- There is no eat command, and right-clicking food does nothing: a character eats by themselves when hunger is below 250, the stomach is empty and food is in reach.
- Their own inventory is used first, then their worn backpack.
- Squad food: the wiki says any squad member's inventory or backpack; a code-based reference says only the worn backpacks of squad members within about 20 m, once hunger is below 225, with the squad's Share Food option on.
- The lowest-nutrition food is eaten first. One bite is at most 50 nutrition; each point restores 1 hunger as it is digested.
- Edible ingredients alone (Raw Meat, Bread) are not touched until hunger is below 200.
- Food does not spoil, and water is not needed. Nutrition and prices: "Food items and nutrition" in Items and equipment.
- To feed someone, drag food into their inventory; for an animal with no backpack available, drop food on the ground near it.

## Sharing food through a backpack
Also: squad food, shared food, feed whole squad, feeding a squad from one backpack, food backpack
- Food in a worn backpack is shared: every squad member standing near the wearer eats from it when hungry.
- Only members of the same squad share; a second squad needs its own carrier.
- Animals in the squad eat from it too, or from a pack animal's backpack.
- To avoid backpack combat penalties, keep the pack in the inventory and put it on briefly at meal times, or use a Small Thieves Backpack (no penalties).
- Bandits who loot food take it from worn backpacks and inventories, not from a backpack stored inside an inventory or from the ground.
- Non-stolen stacks of the same food merge when moved into one inventory.

## Starvation: what to do
Also: no food, starving character, emergency food
- Below 200 hunger the character is already weaker and slower; do not travel far or fight.
- Buy the cheapest filling food at a bar or trader: Dried Meat, Rice Bowl, Gohan.
- No money: mine ore by a town and sell it, or loot food from bandits the guards have beaten.
- Scorchlanders and Hive characters can eat Raw Meat from dead animals as it is.
- Resting in a bed cuts hunger drain to one third while waiting.
- A fainting character must be fed by a squad member putting food in their inventory, or carried to food.
- Timing: eating stops hunger drain, so eat during heavy work or heavy carrying rather than before.

## New-game options that change survival
Also: difficulty options, chance of death, hunger time, global damage multiplier, bandits loot
- These sliders are set when a game is created (advanced options) and are saved with the world.
- "Chance of death" (0.5 to 4): multiplies bleeding and wound degeneration. It does not change starvation.
- "Hunger time" (0.25 to 8): multiplies how long hunger lasts.
- "Global damage multiplier" (0.5 to 4): multiplies damage dealt and combat XP.
- "Bandits loot the player" (on by default): lets NPCs loot your downed characters.
- "Dismemberment" (Never, Rare, Frequent): how limbs are lost.
- All default to 1 (or Rare), which is what the numbers in this file assume.

## Acid, burning and gas damage
Also: weather damage, acid damage, burn damage, gas damage
- Acid Rain (Deadlands, Iron Valleys, Darkfinger, seasonally the Burning Forest): slowly deals stun damage to unprotected organic body parts. 80% protection is enough to out-heal it; buildings and tents give shelter.
- Acidic ground (Deadlands, Iron Valleys, Black Desert): burns unprotected legs, so footwear is needed.
- Acidic water (Deadlands, Vain): damages swimmers; armour does not help.
- Burning: beams in Venge. Gas: poison clouds in the Black Desert and Ashlands. Dust storms cut Perception and combat skills.
- Skeletons are immune to all of it; Hive races to acid only.
- With limb loss set to Frequent, weather damage alone can sever a limb below -100%.

## Being eaten alive
Also: eaten, eaten alive, prisoner pole, cannibal cage
- Fogmen and cannibals carry unconscious organic characters to their camps; Fogmen tie them to Prisoner Poles and eat them alive, cannibals cage and later cook them.
- Eating applies cut damage and negative bandaged health, limbs first, and can sever limbs.
- It can take seconds to minutes, so escape or rescue is possible.
- A character on a pole can bandage themselves once able (with the Medic job set) and can pick the lock.
- The damage must be bandaged afterwards even if a robot limb is fitted.
- A character knocked out only by blood loss stands up at once if an animal starts eating them; sneak away and bandage.
- Skeletons are not eaten.

## Healing strangers, enemies and animals
Also: heal NPC, heal bandit, medic XP farming, relations from healing
- Any hurt character or animal that is unconscious, playing dead or friendly can be bandaged.
- It gives Field Medic XP, which depends on time spent treating; animals have big health pools and train it well.
- It gives a small relations gain with the patient's faction.
- Loot a beaten bandit's Basic First Aid Kit first, then use it on them.
- Putting an incapacitated NPC in a bed may also raise relations.
- Conscious hostile characters cannot normally be treated.
- A prisoner you want alive must be bandaged before being carried, or they bleed out on the way.

## Sources
- https://kenshi.fandom.com/wiki/Guide_to_Health : beds, hunger thresholds, bleeding and triage, bandaging methods and order, Medic button, repairs, splints, limb replacement.
- https://kenshi.fandom.com/wiki/Damage : knockout and coma rules, stun and cut, degeneration rates, blood-loss formulas, limb loss, wear, KO times, skill penalties.
- https://kenshi.fandom.com/wiki/Toughness : KO point and degeneration formulas, hunger fainting, playing dead tip.
- https://kenshi.fandom.com/wiki/Update:0.61 : developer description of knockout, coma and playing-dead rules.
- https://kenshi.fandom.com/wiki/Medical_Items , /Basic_First_Aid_Kit , /Standard_First_Aid_Kit , /Advanced_First_Aid_Kit , /Splint_Kit , /Advanced_Splint_Kit , /Skeleton_Repair_Kit , /Authentic_Skeleton_Repair_Kit : kit stats, prices, who carries them, crafting.
- https://kenshi.fandom.com/wiki/Bed , /Camp_Bed , /Sleeping_Bag , /Skeleton_Repair_Bed : healing multipliers, rental, repair bed locations and prices.
- https://kenshi.fandom.com/wiki/Small_Empire_Bar , /Empire_Bar , /Empire_Big_Bar , /Smugglers_Bar : bed prices.
- https://kenshi.fandom.com/wiki/Loading_Screen , /Jobs : in-game tips (MEDIC button, playing dead, defeat), first aid jobs ignore the JOBS toggle.
- https://kenshi.fandom.com/wiki/Getting_Started : playing dead with PASSIVE and SNEAK, bed multipliers, starting hungry.
- https://kenshi.fandom.com/wiki/Global_Game_Settings : blood recovery rate.
- https://kenshi.fandom.com/wiki/Robot_Limbs : installing, stats, prices, vendors, stump bleeding.
- https://kenshi.fandom.com/wiki/Skeleton , /Skeleton_(Race) : repair speed, wear, kit locations, playing-dead bug.
- https://kenshi.fandom.com/wiki/Food , /Wheatstraw_60%25_or_Cactus_100%25%3F , /Backpacks , /Hungry_Bandit , /Starving_Bandits : nutrition, prices, hunger drain, food sharing, food theft.
- https://kenshi.fandom.com/wiki/Strength , /Dexterity : hunger and injury penalties, blood formula.
- https://kenshi.fandom.com/wiki/Weapons , /Guide_to_Equipment , /Martial_Arts , /GlitchMaker%27s_General_Guide : effects of disabled limbs, bar colours.
- https://kenshi.fandom.com/wiki/Weather_Effects , /Prisoner_Pole , /Fogmen , /Cannibals , /Peeler_Machine , /Severed_Limbs : environmental damage and being eaten.
- https://kenshi.fandom.com/wiki/Field_Medic , /Guide_to_Training_Statistics , /Assassination , /Adventurer_Bar , /Prisoner_Cage , /AI_Goals , /Controls : medic skill, healing others, drop knockout, kit vendors, carry commands, rescue goals, build key.
- https://github.com/VlcekM/meitouclient (local clone, third-party reference worked out from the game's code and data; only its statements about the original game were used): docs/game/character-stats.md (hunger scale and death at 0, status words, knockout time formula and constants, coma rule, blood rules, healing and bed rates, first aid order, self-treatment at 80%, kit search and drain, "I don't have a medkit.", splint rules and wording, leg-down rule, limb severing, eating rules, activity hunger rates, new-game options); docs/game/ragdolls.md (playing dead safety test, "Playing dead...", "Staying low", crawl speeds); docs/game/carry-loot.md (left arm needed to carry, put-down knockout, rescue conditions); docs/game/pathfinding.md and docs/game/game-loop.md (crawl speed, length of a game hour).
- https://steamcommunity.com/app/233860/discussions/0/613956964595378556/ and /133257636770657665/ (via web search): putting a carried character in a bed, RESCUE button, put-down bug.
- https://steamcommunity.com/app/233860/discussions/0/2656452469271825571/ (via web search): splint menu option.
- https://steamcommunity.com/app/233860/discussions/0/3051633726585328459/ and /1519260397789324022/ (via web search): playing dead being noticed by looters.
- https://steamcommunity.com/app/233860/discussions/0/594820656462030250/ (via web search): right-click a bed to sleep.
- https://kenshi.zone/en/hunger-food and https://kenshi.zone/en/item-basic-first-aid-kit (via web search summaries only; site not reachable): hunger option, kit quality cap.
- https://gamesfuze.com/guides/kenshi-how-to-eat-food/ (via web search): the conflicting 400 hunger maximum.
- Kit sizes and recipes and robot limb grades merged in from Items and equipment rest on the sources listed there.
