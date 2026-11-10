# Law and crime

What counts as a crime in Kenshi and where, how witnesses, guards, bounties, jail and slavery work, and how to check ownership and deal with stolen or illegal goods.

## How crime works: you must be seen
Also: witnesses, getting caught, caught stealing, seen by guards, committing crime, alarm
- A crime only counts if someone from the owning faction or its allies sees it.
- When seen, an alarm is raised and guards rush to arrest you; a bounty is added to the character who did it.
- Each illegal act has a cool-down timer during which you still count as "committing crime"; stop before anyone looks and wait it out.
- After you stop picking a lock you remain a criminal for 3 seconds.
- After stealing from a container a timer shows at the bottom left above the character's name; wait for it to finish unseen.
- Resisting arrest adds an assault charge.
- While your "committing crime" flag is up, factions hostile to you may attack you freely inside the town.
- Factions whose characters are classed as bandits can be seen committing crimes but never get bounties; attacking them gives you no bounty.

## Crime list: bounty, expiry and jail time
Also: crime table, how much bounty, sentence length, fines

| Crime | Bounty | Expires | Jail |
|---|---|---|---|
| Trespassing | c.100 | 4 hours | 2 hours |
| Looting | c.500 | 20 hours | 10 hours |
| Assault | c.500 | 20 hours | 10 hours |
| Burglary (lockpicking) | c.1,000 | 40 hours | 20 hours |
| Theft | c.2,500 | 100 hours | 50 hours |
| Escaping Prison | c.2,500 | 100 hours | 50 hours |
| Refusing Bag Check | c.4,000 | 160 hours | 80 hours |
| Terrorism | c.5,000 | 200 hours | 100 hours |
| Kidnapping | c.5,000 | 200 hours | 100 hours |
| Uniform Theft | c.5,000 | 200 hours | 100 hours |

- Rule: 4 hours to expire per c.100 of bounty; the jail sentence is half the expiry time.
- Refusing Bag Check is listed for the United Cities.
- Bounties stack: each crime adds its amount to the character's total.

## Theft: owned items show a red name
Also: stealing, red text, picking up things in town, is this item owned
- Items owned by an NPC have their name coloured red; taking one is theft (c.2,500 bounty if seen).
- Picking an owned item off the ground requires holding Alt while clicking, so a plain right-click will not steal it by accident.
- Taking a red item lying out in the world always succeeds mechanically; the risk is only being seen.
- Being caught costs a little standing with the owning faction.
- Stealing junk from residential buildings does not affect your access to the town's shops.
- Use Stealth mode (the sneak button) whenever you steal.
- Loot from bandits and other enemies of the town is not stolen property.

## Stealing from containers and shops
Also: shoplifting, steal chance, shopkeeper, Thievery
- Stealing from a container shows a success chance based on the Thievery skill and on how close the nearest NPC is.
- Even after a successful, unseen steal, stay hidden until the timer above the character's name runs out.
- If a shop catches you stealing, that shop will never trade with your faction again; sending a different character does not help.
- No Thievery experience is gained when the chance is 98% or higher.
- Wiki method: sneak in, hide behind furniture until night, wait for the shopkeeper and guards to go to bed, then take shelf items before trying containers.
- Unlock the door beforehand for a quick exit but leave it closed: town guards investigate doors left open at night.
- Locked containers always hold at least one item; clicking a container shows [EMPTY] when it has nothing.

## Looting bodies: when it is a crime
Also: looting unconscious people, taking gear from the fallen, corpses in town
- Taking items from an unconscious townsperson, guard or other non-bandit in view of the town is the Looting crime (c.500).
- The wiki's crime table also lists "Looting bodies" under Theft (c.2,500), so expect either charge.
- Looting bandits and other attackers that the guards knocked down is not a crime.
- Looting an unconscious character does not need Alt.
- Out in the wilderness nobody reports it, but allies of the victim nearby will still react.
- Do not wear looted faction uniforms in that faction's towns.

## Trespassing: private and public buildings
Also: entering houses, "get out", private property, closed shop
- Entering a building set to private is trespassing (c.100 bounty, expires in 4 hours).
- Residential houses are usually private, notably in Mongrel and in Holy Nation towns.
- Some military bases, such as Narko's Trap, also count.
- During the day occupants usually ask you to leave several times before the charge is applied; leave at once.
- A Noble House is never public; staying inside gets you attacked, and fighting back adds an Assault bounty.
- Shops and Police Stations are public by day and closed at night; bars and Thieves Guild towers stay open at night.
- Thieves Guild towers object to non-members who linger or use their equipment.

## Shops after closing time
Also: locked in a shop at night, shopkeeper tells me to leave
- At night the shopkeeper locks the shop door.
- If you are still inside, the shopkeeper asks you to go, repeatedly; only after many warnings does a trespassing charge follow and the guards move in.
- Walk out when told and nothing happens.
- Shopkeepers and shop guards go to sleep if the building has beds for all of them.
- Slave Shops stay open all night.

## Checking whether a building is public, private or for sale
Also: can I enter this building, building owner, For Sale
- Left-click the building and read its details in the bottom-left corner of the screen.
- The panel shows the building's name (for example a Police Station) and whether it is "Public".
- If it does not say Public, treat it as private and stay out.
- Buildings you can buy show a "For Sale" button in the same panel.
- Signs by the door also mark shops and Police Stations.
- A door or container is locked when the cursor changes to a padlock over it.

## Checking whether an item or container is owned
Also: who owns this, safe to take, stolen warning
- An item whose name is shown in red belongs to someone; a normal-coloured name is free to take.
- The highlight-items key shows item labels, which should let you check the colour before clicking (unverified)
- Everything inside a shop or occupied house, including its containers, belongs to that building's faction.
- Taking from someone else's container is stealing and shows a chance percentage.
- Merely opening an unlocked container to look appears to be safe (unverified)
- Picking a lock on a container or door you do not own is Burglary even if you take nothing.
- Beds and Training Dummies in faction buildings are private equipment too.
- Whether the tooltip names the owner before you take the item is not stated on the wiki (unverified)

## Lockpicking and the Burglary charge
Also: pick a lock, locked door, locked chest, padlock cursor
- Start by holding Alt and right-clicking the lock, or hold right-click and choose "Lockpick".
- A bar fills; at the end of each cycle the character has the shown percent chance to succeed.
- Chance = 90 / 2^((lock level - Lockpicking skill) / 10), capped at 90%.
- If the chance is under 5% the character says the skill is too low and cannot try.
- Being seen picking a lock you do not own is Burglary: c.1,000 bounty.
- Lock levels, before random variation: Holy Nation cages 35, containers 30, doors 25 (plus or minus 10); United Cities cages 40, containers 40, doors 30 (plus or minus 10); Shek Kingdom 40 for all (plus or minus 20).
- A skill-0 character has about 16% per cycle on a level 25 door and cannot attempt anything above level 41.
- Successful picks give 5 times the experience of failed ones.

## Assault and self-defence
Also: attacking townspeople, fighting back, who started it
- Attacking an NPC of a lawful faction in view of that faction is Assault (c.500).
- Fighting back against that faction's members after they attack you is also charged as Assault, even on block or passive.
- A failed Assassination (stealth knockout) attempt usually counts as Assault.
- Anyone who already has a bounty can be attacked freely without trouble from the police.
- Characters classed as bandits, including City Heroes of the United Heroes League, can be attacked inside towns and the guards side with you.
- Bandits chasing you into a guarded town are attacked by the gate guards.

## Kidnapping and carrying people
Also: pick up a body, carry unconscious character, abduction
- Being seen carrying off an NPC who is not your ally is Kidnapping: c.5,000 bounty.
- The charge is applied again each time you are caught stealing clothing or weapons the kidnapped NPC is wearing.
- Carrying a character with a bounty to the police is allowed.
- Carrying your own squad members is always fine.
- Dropping an unconscious stranger beside a slaver, instead of selling them yourself, leaves them unaware that you caused their capture.
- A character you ever kidnapped will not later thank you or offer to join.

## Terrorism: freeing slaves and prisoners
Also: unlock cages, free a slave, attack a noble
- Terrorism (c.5,000 bounty, 200 hours) covers freeing slaves or other criminals from cages, including being seen unlocking your own shackles.
- It also covers kidnapping slaves and attacking people with Diplomatic Status.
- Freed slaves usually sprint for the gate and are beaten down and recaptured by town guards.
- A slave escorted safely well outside the walls may join you.
- Lockpicking a police cage is seen as Burglary; carrying the freed prisoner away is not treated as a prison break.

## Using other people's beds and training dummies
Also: private equipment, police station dummies, free training
- Training Dummies and beds inside faction buildings are private.
- Residents first yell at you; if you keep using the equipment after several warnings they attack.
- Police Station dummies can be used without complaint only when allied with that faction.
- Shinobi Thieves members may use the tower's beds, Assassination Dummies and Locksmith Training Boxes.
- Nomad camps and their Camp Beds are free to use.

## Wearing faction uniforms (Uniform Theft)
Also: faction uniform, uniform armour, looted uniform, samurai armour, holy chest plate, uniform price
- Armour tagged as a faction uniform says so at the top of its item description, with the faction's name.
- Wearing even one piece puts the character "in Disguise". Near that faction it risks being spotted; guards then attack, and the faction's enemies may attack you as one of them.
- In the United Cities being seen through adds a Uniform Theft bounty of c.5,000.
- You may wear a faction's uniform freely once allied with it.
- Uniform wearers include Samurai, Samurai Police, Holy Sentinels, Paladins, Inquisitors, Hundred Guardians, Slavers, Manhunters, Ninja Guards, Sand Ninja leaders and Dust-style gangs such as Reavers and Crab Raiders.
- Faction uniform pieces sell at 30% of the plain item's price, and a trader can refuse one ("What is that a uniform? I don't want that!"). Safe rule early: never wear looted uniforms in or near towns; sell them to a trader of a different faction.
- Passing as a member with a full set: "Disguises".

## Disguises
Also: sneak past guards, looks like, disguise percentage
- A full uniform (helmet, chest piece, leggings) usually gives 100% or near 100% disguise.
- The inventory screen shows, top right, who you are disguised as and how effective it is.
- Using a faction's own uniform against that faction carries about a 40% penalty; an ally's uniform (Traders Guild, Slave Traders, United Cities share) has none.
- Against the faction that enslaved you the penalty is 50%.
- If discovered, the disguise is "blown" for about 250 seconds and works worse afterwards because your face is known.
- Stealth skill makes a disguise hold up better at close range.
- Do not wear a uniform into the land of that faction's enemies: a Holy Nation uniform gets you attacked by the Shek.

## Who recognises a bounty
Also: wanted, walking into town with a bounty
- It takes time for someone to recognise a wanted character; get in, avoid attention and get out fast.
- The bigger the bounty, the more people know your face.
- The keenest eyes belong to Police and Bounty Hunters; civilians recognise only the most infamous criminals.
- A bounty belongs to the faction that issued it; other factions' guards do not act on it.
- Allied factions ignore existing bounties on your characters.
- Avoid towns with a police presence while wanted there; Stealth and a disguise both reduce the chance of being recognised.

## What guards do when they catch you
Also: arrest, arrested, caught by guards, guards attack after stealing, guards attacking me, police, samurai police, surrender
- Guards attack to knock the wanted character down, then carry them to a Prisoner Cage in the Police Station.
- Weapons are confiscated and stored in a container near the cells.
- A United Cities Samurai making an arrest may offer to let you off for a fine.
- In a faction that practises slavery (The Holy Nation, United Cities), a passing slaver patrol can enslave a caged prisoner and take them to a mine or camp.
- Shek Kingdom jails do not lead to slavery.
- Running before anyone sees a minor crime avoids the bounty entirely.

## Bounties: how they expire
Also: how long does a bounty last, bounty duration, bounty timer, waiting out a bounty, clear my name, wanted
- A bounty fades by itself: 4 hours per c.100.
- Examples: trespassing 4 hours, assault 20 hours, lockpicking 40 hours, theft 100 hours.
- A bounty from briefly evading arrest for a minor crime should be gone within hours.
- Bounties are per character, not per squad; other squad members are not wanted.
- Select the character: the bounty is shown at the top of the bottom-left panel, and hovering over it shows which faction issued it.
- Wait outside town, or in a faction that does not care, until it is gone.

## Notorious bounties (over c.10,000)
Also: permanent bounty, never expires
- A total over c.10,000 makes the character notorious: the bounty no longer expires by itself.
- In jail, a bounty of c.25,000 or less can still be served off.
- Above c.25,000 it can only be removed by bail.
- Being enslaved by a faction clears the bounty you had with that faction.
- Wiki bug note: bounties over c.10,000 sometimes disappear over time anyway.

## Turning yourself in and serving time
Also: get in the cage, serve the sentence, jail time
- Select the wanted character, hold right-click on a Prisoner Cage in the Police Station and choose "get in".
- The sentence is half the bounty's expiry time: 2 hours per c.100.
- Serve it out and the bounty is cleared; simple lockpicking costs less than a day.
- You lose your weapons while inside; look for them in the containers near the cells afterwards.
- Risk: in Holy Nation and United Cities towns a caged prisoner may be taken as a slave.
- Leaving before the sentence ends is Escaping Prison: a new c.2,500 bounty.

## Jailbreak: lock chance and the Escaping Prison bounty
Also: jailbreak, break out of jail, prison escape, escape bounty
- "Escape" in the caged character's menu picks the lock and walks out as soon as it opens (clicks: "Escape from a cage or shackles" in How-to). Alternatively pick the lock and stay inside, then leave at a chosen moment.
- Lockpicking has a -10 penalty when opening your own cage.
- You may still attempt it if your unpenalised chance would be 5% or more: skill 0 can try a level 40 cage, at about 2.8% per cycle.
- Leaving early adds the Escaping Prison bounty of c.2,500 (100 hours).
- A character with no sentence who gets into a town cage is simply let out by the guards; for practice use abandoned cages (Bast, Fort Simion).
- Stealth, darkness and a disguise decide whether you get out of the building and the gate.

## Bail: paying off a bounty
Also: pay bounty, pay off bounty, free a jailed squad member, get out of jail, Police Chief
- Another of your characters talks to the Police Chief (United Cities), Inquisitor (Holy Nation) or Hundred Guardian (Shek Kingdom) in the Police Station and pays bail.
- Bail costs double the prisoner's bounty and clears it.
- If the chief walks close enough to talk to, a prisoner can pay off their own bounty from inside the cage.
- Bail is the only way to remove a bounty above c.25,000.
- The same officers resell confiscated equipment.
- Holy Nation officers will only deal with a human male.

## The wilderness has no law
Also: crimes outside towns, no witnesses
- Away from towns of major factions nobody reports crimes, so no bounty is given.
- Your actions still anger the individual NPCs or factions you attack.
- The Hub has no police; its bar guards (Trade Ninjas) and the Shinobi Thieves defend only their own property and allies.
- Hostile factions cannot freely attack you inside another faction's city unless your "committing crime" flag is up or they are allied with that city.

## Which faction's law applies where
Also: jurisdiction, who gives the bounty
- United Cities law covers its towns and also Empire Peasants, Free Traders, Tech Hunters and Machinists: crimes against any of them give a United Cities bounty.
- United Cities and the Traders Guild share bounties; a bounty with both is doubled.
- The Holy Nation's police are Inquisitors, in the Police Stations of Blister Hill and Stack.
- Shek Kingdom police are Hundred Guardians, with stations in Admag, Squin, Last Stand and The Great Fortress.
- United Cities Police Stations: Brink, Catun, Clownsteady, Heft, Heng, Sho-Battai, Stoat.
- Half the police patrol the town while the other half rest in the station.

## Illegal goods by faction
Also: illegal items, contraband, banned items, what not to carry

| Where | Illegal items |
|---|---|
| The Holy Nation | Hashish, Ancient Science Book, AI Core, Forbidden Sympathy, Cultural Groupings And Evolution Series, Moll's Speech, Letter To Moll |
| United Cities, Traders Guild, Empire Peasants | Hashish, Bloodrum, Hemp |
| Slave Traders, Free Traders | Hashish, Bloodrum, Hemp |
| Shek Kingdom | Hashish |
| Tech Hunters, Anti-Slavers, The Swamp, Crab Town | nothing |

- Keep illegal items away from gate guards of the faction concerned.
- The Border Zone Waystation follows the United Cities list.
- The Holy Flame (c.90) is the opposite case: carrying it helps in The Holy Nation and is required for Prayer Day.

## Gate bag checks
Also: contraband search, "I need to check your inventory", Samurai Gate Sergeant
- United Cities gates always have 1 Samurai Gate Sergeant; he sometimes stops travellers to check for contraband.
- With nothing illegal, simply allowing the search is the quickest way through.
- Refusing or attacking is Refusing Bag Check: c.4,000 bounty.
- He can usually be bribed, unless he has an Honorable personality; a Dumb one accepts a smaller bribe.
- An Honorable sergeant can instead be talked past with the right dialogue choice.
- A Traitorous sergeant frames you if you carry nothing illegal; at bad United Cities relations, any sergeant who is not Honorable or Dumb frames you.
- Holy Nation Holy Sentinels and Shek gate guards also search; in The Holy Nation a human male carrying The Holy Flame is searched least. Do not try to bribe Holy Nation guards.
- Allied factions do not search you.

## Hashish smuggling
Also: drugs, sell hash, smuggler, markup
- Hashish (base value c.150, weight 1) is bought in The Swamp and in Hive Villages.
- Sell markups: United Cities north-east 1200%, Slave Traders 600%, United Cities south 500%, The Holy Nation 400%, Tech Hunters 400%, Shek Kingdom 350%.
- Where it is illegal, ordinary shops will not buy it; the buyer is the Shinobi Trader inside a Thieves Guild tower, at half price (so 600% in Heft, Heng and other northern towns).
- A Thief Fence in a bar does not buy Hashish.
- Flats Lagoon, Mourn and Manhunter Base buy it openly at 400% with no fence cut; Flats Lagoon is next to The Swamp.
- The Traders Guild will not touch it.
- Being caught at a gate gets you arrested; the wiki does not give a separate smuggling bounty figure.

## Illegal buildings and the Drug Bust
Also: hemp farm, hashish production, base raid
- In United Cities territory these player buildings are illegal: Biofuel Distillery (Hemp), Hemp Farm, Hemp Processor, Hydroponic Hemp.
- A Smart, Honorable or Fearful Samurai who sees one gives a c.2,000 bounty and arrests at once if you are inside an NPC town or your squad has fewer than 9 characters; otherwise he reports it.
- Corrupt Samurai (Traitorous, Dumb, Brave or Maniacal) extort instead: pay c.2,000, then they ask c.1,000 more; with too little money they accept the c.2,000.
- Once reported, a Drug Bust assault of 1 to 3 samurai squads reaches your base 12 to 72 hours later.
- This stops if Emperor Tengu is killed or captured.
- The Holy Nation lists ancient-tech benches as illegal buildings but has no dialogue that enforces it.

## United Cities law in brief
Also: Empire rules, United Cities crimes, poverty law, samurai fine
- Slavery is legal; anti-slavery activity is treated as terrorism.
- Starving characters are arrested for poverty: a gate sergeant demands that you hold at least c.500; a patrol wants a c.2,000 bribe unless it takes pity.
- Hashish, Bloodrum and Hemp are contraband and bags are checked at gates.
- Stealing inside a Noble House brings a Noble's Wrath attack on your outpost.
- A jailed character can be enslaved by Slave Traders and taken to a slave camp.
- Unconscious characters in or near town may be picked up and enslaved rather than left alone.
- Outposts on United Cities land are taxed c.3,000 weekly unless you are allied.

## Holy Nation law in brief
Also: Okran rules, heresy, Holy Nation crimes
- Skeletons and anyone with a robotic limb are attacked on sight unless you are allied.
- Shek and Hive characters must stay beside a human of the same squad or be arrested and sent to Rebirth.
- Only human males may hand in bounties, bail prisoners or deal with officials.
- Residential houses are private.
- Illegal items: Hashish, Ancient Science Book, AI Core and several banned texts.
- Carry The Holy Flame; swear loyalty when questioned; never praise Narko.
- Prisoners and trespassers go to Rebirth or the Holy Mines as slaves; the Holy Nation never sells slaves.
- An outpost in their land needs at least one male and a copy of The Holy Flame for Prayer Day.

## Shek Kingdom law in brief
Also: Shek rules, Hundred Guardian police
- Hashish is the only contraband; gate guards search for it.
- Hemp and hemp buildings are legal.
- Hundred Guardians act as police and run the Police Stations.
- The Shek do not practise slavery, so jail here does not end in a slave camp.
- Shek Warriors may pick fights with Humans and Hivers regardless of law.
- Using the station's training dummies gets you berated unless allied.

## Stolen goods: the stolen flag
Also: marked as stolen, stolen tag, hot items
- Anything you steal is flagged as stolen when you look at it in your inventory.
- For a while it also lists who it was stolen from; that part eventually falls off.
- The flag only matters when selling back to the faction it was stolen from.
- Most stolen items, trade goods included, sell for half their normal value.
- Shopkeepers do not care about loot taken from their enemies.

## Selling stolen goods
Also: fence chance, sell hot items, get caught selling
- Selling to a different faction than the victim: 100% safe.
- Selling to the Hive or to the Shinobi Thieves: 100% safe.
- Selling back to the faction you stole from: success chance is 20% + 0.42% per point of Thievery, shown when you try.
- What exactly happens when the sale fails is not spelled out on the wiki; expect to be treated as a thief (unverified)
- Most towns contain shops of more than one faction, so walk the item to another faction's shop.
- Carry stolen goods to another faction's town when in doubt.

## Fences: Thief Fence, Shinobi Trader, Black Market Bar
Also: fence, where to sell stolen items, stolen goods buyer
- Thief Fence: a Shinobi Thieves member found in some town bars; trades with anyone, member or not; buys and sells everything at 50%.
- Shinobi Trader: inside a Thieves Guild tower (Admag, Catun, Clownsteady, Heft, Heng, Mongrel, Sho-Battai, The Hub); also 50% prices; the only buyer of Hashish where it is illegal.
- Black Market Bar (The Hub and Rebel Base, run by Trade Ninjas): an ordinary bar and shop that accepts stolen goods from any faction except goods stolen from the bar itself.
- Joining the Shinobi Thieves costs c.10,000, paid to the Thief Boss outside a tower.

## Removing the stolen flag
Also: launder stolen goods, clean items
- Sell the item to a Shinobi Trader and buy it back: it is no longer considered stolen and can be sold to local shops at full price.
- Putting a lifted item into a specialised storage container can also clear the tag.
- A Crossbow locker or an Item Furnace is named by the wiki for the same purpose.
- The owner's name on the tag wears off with time; the wiki does not say the stolen flag itself ever expires.

## How you become a slave
Also: enslaved, captured by slavers, taken to the mines
- Slavers (Slave Traders, Manhunters, Slave Hunters, Reavers, and Holy Nation soldiers) pick up unconscious non-allied characters, heal them and carry them to a slave site.
- Being jailed in The Holy Nation or United Cities can end the same way when a slaver patrol passes.
- Getting into a Prisoner Cage in a Slave Shop also does it.
- Weapons go first; some armour is replaced by Prisoner Shackles (Hive Prisoner Shackles for characters who cannot wear boots); the rest is confiscated on reaching a camp.
- Confiscated gear is usually stored in a chest at the site and can be stolen back.
- Destinations: Rebirth and Holy Mines (Holy Nation); Stone Camp, South Stone Camp, Slave Farm, Slave Farm South, Eyesocket, Slave Markets (Slave Traders); Ark (Reavers).
- Your bounty with the enslaving faction is cleared.

## Life as a slave
Also: Obedient Slave job, shackles, slave camp routine
- The character's job list is replaced by a single "Obedient Slave" job: follow orders to farm, labour or fight.
- Removing that job marks the character as an escaped slave, though not always at once.
- Prisoner Shackles weigh 20 kg and sharply cut movement speed and Stealth.
- Slaves are fed to a minimum of 100 hunger: malnourished but never starving.
- Slavers patch you up whenever you are knocked out, which makes it a safe place to train Toughness, Lockpicking, Stealth and Thievery.
- At night you are locked in a cage; other slaves' cages may be within lockpicking reach.
- Slaver caravans sometimes buy or rent slaves and march them elsewhere.
- Holy Nation guards carry no repair kits, so an enslaved Skeleton must avoid damage.

## Escaping slavery
Also: break shackles, slave camp escape, run from the mine
- Shackles: lock level 20, or break with Strength 20, or cut with Tools or a saw. Lockpicking 0 gives about 22% per cycle by the formula, about 11% if the -10 imprisonment penalty applies.
- Unlock the shackles early but keep them on while guards watch; guards attack a slave seen without them.
- Take them off only when you sneak, fight or run.
- Night is best; knock out a lone guard with Assassination, drop his weapon and strip his armour.
- A full set of guard armour works as a disguise (keep the shackles on until you move).
- At the gate there are usually two rows of guards; slip out along the side.
- Bandit attacks pull most guards away; small sites such as Holy Mines have gaps.
- If allied with the slaver faction you may simply unlock your shackles and leave.
- Another squad member can buy you back at a Slave Shop.

## Escaped slave and ex-slave status
Also: "Looks like a Slave", runner, hunted after escaping
- A slave who runs is called a runner, marked as an escaped slave and attacked by everyone from pro-slavery factions.
- After a clean escape you are branded an ex-slave for several game-days.
- The inventory window shows a "Looks like a Slave" percentage: the chance of being identified.
- Change clothes and hair and stay away from towns until it reads 1%.
- A slaver may shave your head; a Plastic Surgeon restores hair.
- Grey of the Anti-Slavers, at Spring, clears the status at once when spoken to.
- Putting on unlocked shackles again gives the escaped-slave status.
- Getting into an NPC-owned cage while marked ex-slave or escaped slave enslaves you instantly.

## Buying and freeing slaves
Also: slave shop, purchase a slave, slave recruits
- Talk to the Slaver Boss in a Slave Shop, or the slavemonger of a slaver caravan, to buy a slave.
- Price scales with the slave's skills: about c.1,000 for an unskilled one, several thousand for most others.
- Each purchase gives +1 with Slave Traders and +4 with the slave's own faction.
- You cannot own slaves: a bought slave becomes an ally (green dot on the map) who follows you and may later join, or runs away.
- A slave whose Strength, Dexterity and Toughness add up to more than 75 usually will not join.
- Breaking a slave out instead is Terrorism if seen.
- A character you sold into slavery yourself will not be grateful when bought back.

## Bribes
Also: pay off guards, corruption, extortion
- Samurai Gate Sergeant bag check: usually bribable; not if Honorable; cheaper if Dumb.
- Samurai patrol arresting a starving character: c.2,000.
- Samurai who found an illegal hemp building: c.2,000, then a further c.1,000 if you have it.
- Dust Boss toll: c.500, without a backpack equipped.
- Starving Bandits begging: c.500 gives +2 relations, c.1,500 gives +5.
- Hounds: c.2,000 to Ears in Shark buys an introduction to Big Grim.
- Holy Nation guards: do not attempt a bribe.
- Exact gate-bribe amounts are not given on the wiki (unverified)

## Sources
- https://kenshi.fandom.com/wiki/Bounty : crime table, expiry rule, notorious bounties, bail, turning in bounties, shared United Cities and Traders Guild bounties. Fetched as wikitext through api.php.
- https://kenshi.fandom.com/wiki/Getting_Started : being seen, cool-down timer, shop theft bans, closing time, looting bandits, wilderness, checking buildings.
- https://kenshi.fandom.com/wiki/Thievery : red item names, Alt to steal, container chance, stolen flag, selling formula, clearing the tag.
- https://kenshi.fandom.com/wiki/Lockpicking : how to pick, formula, 5% floor, cage penalty. Percentages for skill 0 are computed here from that formula.
- https://kenshi.fandom.com/wiki/Stealth , https://kenshi.fandom.com/wiki/Disguise , https://kenshi.fandom.com/wiki/Faction_Uniform : stealth, disguises, uniform theft.
- https://kenshi.fandom.com/wiki/Loading_Screen : in-game tips on bounties, recognition, stolen goods, open doors at night, shackles.
- https://kenshi.fandom.com/wiki/Prisoner_Cage , https://kenshi.fandom.com/wiki/Police_Station , https://kenshi.fandom.com/wiki/Police_Chief , https://kenshi.fandom.com/wiki/Shek_Police_Station , https://kenshi.fandom.com/wiki/Inquisitor , https://kenshi.fandom.com/wiki/Samurai : jail, cages, police, bail, arrests.
- https://kenshi.fandom.com/wiki/Slavery , https://kenshi.fandom.com/wiki/Prisoner_Shackles , https://kenshi.fandom.com/wiki/Slave_Shop , https://kenshi.fandom.com/wiki/Rebirth , https://kenshi.fandom.com/wiki/Grey , https://kenshi.fandom.com/wiki/Guide_to_Faction_Relations : enslavement, escape, slave status, buying and selling slaves.
- https://kenshi.fandom.com/wiki/The_Holy_Nation_Trade_Culture , https://kenshi.fandom.com/wiki/Empire_Trade_Culture , https://kenshi.fandom.com/wiki/Slavers_Trade_Culture , https://kenshi.fandom.com/wiki/Free_Traders_Trade_Culture , https://kenshi.fandom.com/wiki/Shek_Kingdom_Trade_Culture , https://kenshi.fandom.com/wiki/Empire_Lawless_Trade_Culture , https://kenshi.fandom.com/wiki/Swamper_Trade_Culture , https://kenshi.fandom.com/wiki/Southeast_Trade_Culture : illegal goods and buildings by faction.
- https://kenshi.fandom.com/wiki/Samurai_Gate_Sergeant , https://kenshi.fandom.com/wiki/Hashish , https://kenshi.fandom.com/wiki/Drug_Bust : bag checks, bribes, smuggling prices, illegal buildings.
- https://kenshi.fandom.com/wiki/Thief_Fence , https://kenshi.fandom.com/wiki/Shinobi_Trader , https://kenshi.fandom.com/wiki/Shinobi_Thieves , https://kenshi.fandom.com/wiki/Thieves_Guild , https://kenshi.fandom.com/wiki/Black_Market_Bar , https://kenshi.fandom.com/wiki/Rebel_Base : fences and laundering.
- https://kenshi.fandom.com/wiki/The_Holy_Nation , https://kenshi.fandom.com/wiki/United_Cities , https://kenshi.fandom.com/wiki/Shek_Kingdom , https://kenshi.fandom.com/wiki/Noble_House , https://kenshi.fandom.com/wiki/Tech_Hunters , https://kenshi.fandom.com/wiki/Game_Starts : faction laws, lock levels, legal systems.
- https://kenshi.fandom.com/wiki/Dust_Bandits , https://kenshi.fandom.com/wiki/Starving_Bandits , https://kenshi.fandom.com/wiki/Hounds : payments to bandits and gangs.
- https://kenshi.wiki/bounty , https://kenshi.wiki/slavery , https://kenshi.wiki/thievery : read as HTML; adapted from the Fandom wiki and identical on the facts used here.
- https://kenshi.fandom.com/wiki/Faction_Uniform and https://github.com/VlcekM/meitouclient docs/game/economy.md : uniforms sell at 30% of the plain item; a trader can refuse one.
- Uniform and contraband notes merged in from Items and equipment rest on the sources listed there.
