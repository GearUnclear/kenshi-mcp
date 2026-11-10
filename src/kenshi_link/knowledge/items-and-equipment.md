# Items and equipment

What matters about Kenshi's items: slots, inventory space and weight, food and hunger, medical kits, backpacks, tools, weapons, armour, crossbows, blueprints, materials, typical prices and which shops sell what.

## Equipment slots
Also: gear slots, what can I wear, weapon slots, armour slots, belt slot, Weapon 1, Weapon 2
- A character has nine equipment slots, one item each, beside the grid in the inventory window: Weapon 1, Weapon 2, Belt, Head, Chest (shirt), Armour (body armour), Legs, Feet, Backpack.
- Weapon 1, the upper slot, takes any weapon (one large or two small) and is the one used. Weapon 2 only takes weapons no larger than 1 high by 7 wide in the grid.
- Belt takes Lanterns only.
- Limb slots appear only after a natural limb is lost; they take Robot Limbs.
- Slots a race cannot use are drawn red (code analysis); see "Race limits on equipment".
- Equip by dragging an item from the grid onto its slot, or right-click it; right-clicking a worn item takes it off.
- Worn equipment still counts toward carry weight (installed Robot Limbs do not). A worn backpack has its own extra grid.
- Armour pieces of different classes can be mixed freely.

## Race limits on equipment
Also: hive armour, skeleton armour, shek helmets, cannot wear
- Humans (Greenlander, Scorchlander): all slots, normal shirts only.
- Shek: all slots; cannot wear Wool Hat, Cap, Hachigane, Side-Angle Hachigane.
- Skeletons: Body Armour and Legwear only (no headgear, shirt or footwear slot).
- Hive Soldier Drones: Body Armour, Legwear and hive shirts only; no headgear, no footwear.
- Hive Workers and Princes: headgear (Workers with many helmet restrictions), Body Armour, Legwear and hive shirts; no footwear.
- Hive shirts (Leather Hive Vest, Hiver Chain Shirt, Rusted Hive Shirt) are the only shirts hivers can wear and only hivers can wear them.
- Footwear disappears as a slot if both natural legs are lost.

## Inventory grid and item sizes
Also: inventory size, grid, slots, how much fits, item dimensions
- Every item occupies a rectangle of grid squares.
- The body inventory appears to be 8 wide by 10 tall: the wiki says four Beak Thing Eggs (4x5 each) fill it, and the meitouclient project uses 8 by 10 in its own client; not confirmed for the original (unverified)
- Sizes on the Fandom wiki (wide x tall): Dried Meat 2x2, Book 2x2, Basic First Aid Kit 2x1, Copper 3x2, Raw Iron 3x2, Iron Plates 4x3, Building Materials 6x3, Steel Bars 6x1, Water 5x5, Sleeping Bag 5x3.
- kenshi.wiki lists Copper as 2x3, so check an item's shape in the grid before planning a load.
- Weapons are long and thin: an Iron Club is 7 squares long, a Nodachi 10. The Nodachi does not fit the body grid and must sit in a weapon slot or a backpack.
- A worn backpack adds a second grid (8x8 up to 12x20; animals 20x20).

## Item weight and encumbrance
Also: carry weight, overloaded, too heavy, slow walking
- Carry weight = Strength + 15 (kg) per the wiki; meitouclient's in-game test (1.0.65) found 1.2 x Strength + 15. Worn gear, inventory and backpack contents all count.
- Carrying a person adds 30 kg.
- A worn backpack reduces the weight of what is inside it (30% to 60%; animal packs 90%).
- Encumbrance penalties per 1% over: movement speed -1% (down to a crawl at 100%), dodge -1% (max -60%), martial arts -0.8%, combat speed -0.235%, hunger rate +0.7% (up to +70%).
- Moving while encumbered is the standard way to train Strength.
- The inventory window shows the weight figures beneath the grid.
- Hunger below 200 also cuts Strength: -0.9% per point, down to -90% at 100 hunger.

## Prices: value, sell value, mark-up
Also: item price, tooltip price, how much is it worth, average price
- Tooltips on equipment show Value (shop price) and Sell value (what you get).
- Weapons, armour, crossbows and blueprints: Sell value is 25% of Value, including gear you crafted.
- Backpacks, food, maps and robot limbs: sell for 50%.
- Trade goods and materials: buy and sell at the same local price, which each town sets within 30% of base.
- Stolen items sell at half; Shinobi traders deal at half both ways.
- Faction uniform pieces sell at 30% of the plain item's price, and a trader can refuse one.
- "Average price" figures in this file are wiki base values; price randomisation means your game differs slightly.
- Wiki trick: sell an item, close the trade window, reopen it and buy the item back. Armour comes back undyed and a first aid kit comes back with full charges (you pay the difference). A buy-back inside the same open window is reported to just reverse the sale.

## Food items and nutrition
Also: food list, nutrition values, how much hunger does food restore, food prices
| Food | Nutrition | Buy c. | Size squares |
|---|---|---|---|
| Dried Meat | 15 | 78 | 4 |
| Thinfish | 10 | 360 | 3 |
| Grand Fish | 15 | 360 | 6 |
| Dried Fish | 20 | 360 | 3 |
| Chewsticks | 20 | 152 | 6 |
| Rice Bowl | 25 | 186 | 9 |
| Cooked Vegetables | 25 | 318 | 9 |
| Bread | 30 | 488 | 6 |
| Meatwrap | 50 | 658 | 6 |
| Dustwich | 70 | 730 | 6 |
| Gohan | 75 | 444 | 9 |
| Foodcube | 75 | 874 | 6 |
| Ration Pack | 125 | 1,143 | 4 |
- All weigh 1 kg except Chewsticks and Bread (0.5 kg).
- Sell value is half the buy value.
- Ancient Nutri-Rations match the Ration Pack (125, c.1,143).
- Raw Meat: 15 nutrition, c.60, only for hivers, Scorchlanders and animals.
- Foul Raw Meat: 10 nutrition, c.1, only animals, Hive Soldiers and Hive Workers.

## Which food to buy
Also: cheapest food, best food, travel food, food per cat
- Cheapest per nutrition point: Dried Meat (about c.5.2 per point) and Gohan (c.5.9). Then Rice Bowl (c.7.4), Chewsticks (c.7.6), Ration Pack (c.9.1).
- Worst value: Thinfish (c.36 per point), Grand Fish, Dried Fish, Bread.
- Most nutrition per inventory square: Ration Pack (31 per square), then Foodcube (12.5), Dustwich (11.7).
- For a poor new character: Dried Meat. For long trips: Ration Packs or Foodcubes.
- Bars sell prepared food. The Hub's bar lists Dried Meat, Bread, Cooked Vegetables, Dried Fish, Meatwrap, Foodcube and Ration Pack.
- Gohan is not stocked in United Cities, Shek or Tech Hunter shops; the Smugglers Bar sells it 25% off (about c.324).
- Shek-run shops do not stock Bread, Foodcube, Gohan or Cooked Vegetables.
- How hunger and automatic eating work: "Hunger: the scale and thresholds" and "Eating: how characters eat automatically" in Health and medical.

## Cooking raw meat on the road
Also: campfire, dried meat recipe, cook meat, raw meat
- A Campfire can be placed anywhere from the build menu, costs no materials and does not create an outpost.
- At a Campfire (or a Cooking Stove) 1 Raw Meat becomes 1 Dried Meat.
- Raw Meat comes from animal corpses: Swamp Turtle 14, Garru 10, Wild Bull 10, Goat 7, Crab 6, Beak Thing 5, Bonedog 3, Landbat 2, Skimmer 2.
- Dried Meat can also be found by looting campfires in the world.
- Scorchlanders and hivers can simply eat the Raw Meat.
- Loading-screen tip: without a backpack, feed your animals by dropping food on the floor near them.

## Where to buy medical supplies
Also: buy first aid kit, medic shop, bandage shop
- Bars: the Black Market Bar (The Hub) and Adventurer Bars (Waystations, Black Scratch, Spring, World's End) list Basic First Aid Kits as common stock; Adventurer Bars also list Standard kits and both splint kits.
- General Shops (Squin, Admag, Bark and others) and Holy General Shops: Basic First Aid Kit.
- Travel Gear (Squin, Admag, Heft, Sho-Battai): Basic, Standard and Advanced First Aid Kits, both splint kits, both skeleton repair kits.
- Hive Traders: Standard First Aid Kit.
- Advanced kits and Advanced Splint Kits are never stocked in Holy Nation or Shek trade-culture shops (Travel Gear is run by Tech Hunters, so it is the exception inside Shek towns).
- Kit charges, quality and recipes: "First aid kits: types and stats", "Splint kits" and "Skeleton repair: kits" in Health and medical.

## Sleeping Bag (item)
Also: sleeping bag, bedroll, portable bed, camp bed item
- Sleeping Bag: c.605, 5 kg, 5x3 squares. Sold by travel shops and Adventurer Bars, or crafted from 8 Fabrics at a Medical Workbench.
- In build mode it becomes a Camp Bed anywhere outside town borders or inside your own building; dismantling the Camp Bed returns the Sleeping Bag. Steps: "Make a camp bed from a sleeping bag" in How-to.
- A Camp Bed does not create an outpost.
- The wiki calls it often-neglected and potentially life-saving: carry one on any trip away from towns.
- Healing rates of Beds and Camp Beds: "Beds: healing rates" in Health and medical. Renting: "Bed rental: prices and free beds" there.

## Backpacks compared
Also: backpack list, backpack capacity, backpack penalties, bag sizes
| Backpack | Grid | Price | Combat skills, speed |
|---|---|---|---|
| Scavenger's Basket | 10x14 | c.250 | -5, 0.90x |
| Trader's Wooden Backpack | 8x8 | c.800 | -5, 0.90x |
| Wooden Backpack | 8x8 | c.800 | -5, 0.90x |
| Small Backpack | 8x8 | c.1,000 | -2, 0.95x |
| Medium Backpack | 10x14 | c.1,500 | -5, 0.90x |
| Large Backpack | 12x20 | c.3,000 | -10, 0.80x |
| Small Thieves Backpack | 8x8 | c.3,000 | 0, 1.00x |
| Thieves Backpack | 10x14 | c.5,000 | -2, 1.00x |
| Bull Backpack | 20x20 | c.2,000 | animal only |
| Garru Backpack | 20x20 | c.2,000 | animal only |
- Weight reduction for contents: Scavenger's Basket 30%; Thieves packs 60%; animal packs 90%; all others 50%.
- Stealth and dodge multipliers: Small 0.85x; Medium, Wooden, Basket 0.50x; Trader's Wooden 0.40x; Large 0.25x; Thieves packs 1.00x.
- Own weight: Small, Basket, Small Thieves 1 kg; Thieves 2 kg; Medium, Wooden 4 kg; Large 8 kg.
- Backpacks sell for half their price.

## Which backpack to buy first
Also: best backpack, cheap backpack, mining backpack, trading backpack
- Cheapest space: Scavenger's Basket (c.250, 140 squares) but only 30% weight reduction and no stacking.
- Best for ore and trade goods: Wooden Backpack or Trader's Wooden Backpack (c.800): only 64 squares, but each slot stacks up to 9 of a normally unstackable good.
- Best for a fighter: Small Thieves Backpack (no penalty at all) or Thieves Backpack; half price from the Shinobi Trader after joining the Shinobi Thieves.
- The "combat skills" penalty lowers Melee Attack and Melee Defence only. Martial Arts and Dodge skill are not reduced by it.
- Before a fight, drag a penalised pack from the Backpack slot into the body inventory, or drop it.
- Travel Gear (Squin, Admag, Heft, Sho-Battai) stocks most types; Flats Lagoon, Mourn and Squin have the widest choice.

## Backpack stacking rules
Also: stack items, stacking bonus, stack multiplier, carry more ore
- Most items do not stack, or stack only a little, in the body inventory (Tools stack in fours; Books to 4).
- Wooden Backpack: stack minimum 3, multiplier 3. Non-stacking goods stack to 9; goods that already stack hold three times as many (Books to 12).
- Trader's Wooden Backpack: listed with the same minimum 3 and multiplier 3 as the Wooden Backpack.
- Bull Backpack: multiplier 5. Garru Backpack: multiplier 6. Applied directly, no minimum.
- Small, Medium, Large, Thieves packs and the Scavenger's Basket: no stacking bonus.
- Stacking multiplies weight too: a Garru Backpack holding 96 Water weighs 966 kg before reduction.
- Stolen items do not stack properly with clean ones until the stolen flag is removed.

## Animal backpacks and pack animals
Also: pack bull, pack garru, pack beast, bull backpack, garru backpack
- Bull Backpack and Garru Backpack: 20x20 grid (400 squares), 90% weight reduction, c.2,000, 6 kg.
- Each fits only its own kind of animal (unverified)
- Animals are sold by Farm Shops (Garru, Bonedog; in Bark, Heft, Heng, Stoat, Brink, Black Scratch and farming villages) and by roaming Nomad Animal Traders; animal backpacks by Travel Gear and Farm Shops.
- Animals eat from squad backpacks like everyone else.
- Animal speed depends mostly on age, not Athletics. Game-code notes price an animal at 14,000 x (age + 0.1), so pups are far cheaper than adults.
- Weak bandit factions butcher an unconscious animal for meat, so a lost fight can cost the animal.
- The Wandering Trader start includes a teen Pack Bull with a Bull Backpack.

## Backpack tricks and pitfalls
Also: hide items, smuggle in backpack, dropped backpack bug, loot backpack
- A backpack placed in the body inventory (not worn) still holds its contents; gate searches do not look inside it.
- An unworn backpack's contents weigh their full weight.
- To pick up or open a dropped backpack, hold right-click on it and choose loot.
- Bug: after dropping a backpack, items inside can become flagged "Stolen from (your name)" and sell for a quarter. Drop those items on the ground and pick them up again to clear it, away from shops and witnesses.
- Dropping a stolen backpack inside a store and picking it up again can count as a new crime.
- Shopkeepers' own packs (Traders Backpack Large, Shopkeepers goods bag) are not sold anywhere.

## Tools and Hacksaw
Also: break locks, cut shackles, open chest without lockpicking, bolt cutters
- Tools (c.240, 3 kg, 3x2, stacks of 4) and Hacksaw (c.72, 1 kg, 2x4) do the same job: cut open locks and remove slave shackles without any Lockpicking skill.
- The Hacksaw is lighter and cheaper, so prefer it.
- Cutting is slower and noisier than picking and usually consumes the tool. Higher Strength makes it faster; several characters can cut at once.
- The tool must be in the body inventory, not inside a backpack.
- Lockpicking itself needs no item: hold Alt and right-click a locked door or container, or hold right-click and choose "Lockpick".
- A padlock cursor marks a locked object.
- General Shops stock Hacksaws; the Hub bar and Adventurer Bars sometimes stock Tools.

## Lanterns
Also: light, night, belt item, lantern of radiance, darkness
- Lanterns go in the Belt slot and light the area around the character.
- Darkness penalises crafting, labouring, crossbow use and robotics work; a lantern reduces that.
- Lantern of Radiance (average c.90) is the shop version, sold mainly by Hive Traders and Hive Caravans.
- The plain Lantern (c.76, quality 25) is not sold; it is found as loot in places such as the Old Village and Hive Villages.
- Hive merchants push lanterns on travellers heading for the Fog Islands.

## Maps as items
Also: map item, reveal towns, find locations, buy map
- Map items reveal locations on the world map when used, then disappear.
- A map cannot be used if you already know everything it shows.
- Sold at Travel Gear and similar travel shops and some bars.
- Map of the Border Zone: The Hub, a Waystation, a Tiny Settlement.
- Map of the Shek Kingdom: Admag, The Great Fortress, Last Stand, Squin.
- Glorious Holy Map: Bad Teeth, Blister Hill, Stack, Holy Farms, Holy Mines, military bases.
- Map of the United Cities (Central Territories): Heft, Heng, Sho-Battai, Stoat, Bark, Brink, Drin, Bast, Black Scratch and more.
- Map of the Swamps: Shark, Mud Town, swamp villages. Map of Vain: the Hive Villages.
- Map to Mongrel and Map to World's End show one town each.

## Weapon slots and how weapons are used
Also: sidearm, secondary weapon, backup weapon, two weapons, Weapon I, Weapon II, which weapon is used
- Weapon 1 is used by default. If several weapons sit in Weapon 1, the topmost is used.
- The character switches to Weapon 2 when Weapon 1 is penalised: indoors with a weapon that has an Indoors penalty, or when the left arm is unusable with a two-handed weapon.
- Heavy Weapons, Polearms and crossbows need both arms working (or splinted above 0).
- Every weapon needs the right arm; with it disabled the character fights unarmed or not at all.
- Only the weapon in use applies its bonuses and penalties.
- Weapon skill, Dexterity and Strength scale damage: cut damage follows Dexterity, blunt follows Strength.
- With no weapon the character uses Martial Arts.
- Any shop will buy weapons, not just weapon shops.

## Weapon classes
Also: katana, sabre, hacker, heavy weapon, blunt, polearm, weapon types
- Katanas (Katana, Wakizashi, Ninja Blade, Nodachi, Guardless Katana, Topper): pure cut, high bleeding, usually +10% against humans, weak against armour (-15% to -30%) and robots (-40%). Mostly very light (1 to 2 kg), except Nodachi and Topper.
- Sabres (Horse Chopper, Ringed Sabre, Desert Sabre, Foreign Sabre, Holed Sabre, Longsword): mostly cut with some blunt; many give a Defence bonus and an Attack penalty.
- Hackers (cleavers, Paladin's Cross): cut and blunt mixed, +30% armour penetration, bonus against robots, -10% against animals.
- Heavy Weapons (Plank, Fragment Axe, Falling Sun): huge damage in a wide arc, very heavy, -6 indoors.
- Blunt (Iron Club, Iron Stick, Jitte, Spiked Club, Mercenary Club): stun damage that knocks out without bleeding; good for taking bounties alive.
- Polearms (Polearm, Naginata, Staff): long reach, light, bonus against animals, -4 to -8 indoors.

## Weapon grades and manufacturers
Also: weapon quality, rusted junk, catun, edge type, meitou, mk
- Lowest to highest: Rusted Junk, Rusting Blade (maker: Unknown); Mid-Grade Salvage, Old Refitted Blade, Refitted Blade (Ancient); Catun No.1, No.2, No.3 (Catun Scrapmaster); Mk I, Mk II, Mk III (Skeleton Smiths); Edge Type 1, 2, 3 (Edgewalkers); Meitou (Cross).
- The tooltip shows the grade as "[Model # ...]" and "Manufactured by ...". Higher grades do more damage and, for blunt-heavy weapons, need more Strength.
- Unknown: price x0.3; Rusted Junk also has -1 attack and defence. Common on Starving Bandits and Dust Bandits.
- Ancient: price x0.8, weight x0.7, cut x0.9. The standard issue of most armies.
- Catun: price x1.2, weight x1.2, blunt x1.2.
- Edgewalkers: price x1.4, cut x1.1. Edge Type 2 and 3 are only bought or stolen at the Scraphouse.
- Meitou weapons are unique and held by named characters.
- "Homemade" is what your own smith produces.
- Crossbows use the armour grades (Prototype to Masterwork) instead.

## Light and heavy weapons for a low-Strength character
Also: weapon too heavy, weapon weight, which weapon can I carry, Required Strength Level
- The tooltip lists "Required Strength Level": the greater of the weapon's weight in kg and 40 times its blunt damage value. Below it combat speed drops by up to 47.5% (details: "Weapon strength requirement" in Stats and training).
- Grade changes the requirement: an Iron Stick needs Strength 2.8 as Rusted Junk but 14 as a Refitted Blade and about 20 as Catun No.1.
- Light weapons for a Strength-1 character: Wakizashi, Ninja Blade and Guardless Katana (about 1 kg), Katana (2 kg).
- Too heavy at the start: Nodachi and Topper (8 kg), Horse Chopper (6 kg), any Heavy Weapon (20 kg and up).
- Using a too-heavy weapon is slow but trains Strength faster.

## Weapon price examples
Also: how much does a sword cost, weapon cost, katana price
| Weapon and grade | Value | Sell value |
|---|---|---|
| Iron Stick, Rusted Junk | c.90 | c.22 |
| Iron Club, Rusted Junk | c.180 | c.45 |
| Horse Chopper, Rusted Junk | c.452 | c.113 |
| Wakizashi, Rusted Junk | c.565 | c.141 |
| Katana, Rusted Junk | c.1,131 | c.282 |
| Wakizashi, Mid-Grade Salvage | c.1,864 | c.466 |
| Katana, Mid-Grade Salvage | c.3,729 | c.932 |
| Wakizashi, Catun No.1 | c.4,722 | c.1,180 |
| Katana, Catun No.1 | c.9,445 | c.2,361 |
| Nodachi, Edge Type 1 | c.45,575 | c.11,393 |
- Weapon shops: Shek Weapon Shop (Squin, Admag: Plank, Fragment Axe, Long Cleaver), Empire Weapon Shop (Heng, Stoat: wide range), Holy Weapon Shop, Mongrel Weapon Shop, Shark Smithy, Catun Scrapmasters, Scraphouse.
- The Hub's bar occasionally stocks weapons and Tooth Pick crossbows.
- Looting is far cheaper than buying.

## Armour classes
Also: clothing, light armour, medium armour, heavy armour, armour types
- Clothing: no real protection; some pieces help Martial Arts, Stealth or Athletics. Typical starting wear.
- Light Armour: modest protection, low weight, often bonuses to combat skills, dodge or stealth. The wiki's advice for early characters.
- Medium Armour: more coverage and resistance with moderate penalties (stealth, dodge, dexterity, crossbows).
- Heavy Armour: best resistances, heavy, strong penalties to stealth, dodge, athletics, combat speed and often dexterity.
- Fighting under armour penalties trains combat skills faster.
- Stealth multipliers listed on medium and heavy pieces are harsh: a Chain Shirt is 0.35x stealth, Samurai Boots 0.06x.
- Armour is made at a Clothing Bench, Leather Armour Crafting Bench, Chain Armour Crafting Bench or Heavy Armour Smithy.

## Armour grades
Also: armour quality, shoddy, standard, high, specialist, masterwork, prototype
- Lowest to highest: Prototype, Shoddy, Standard, High, Specialist, Masterwork. The tooltip shows "[Standard Grade]".
- Internal quality levels: Prototype 5, Shoddy 20, Standard 40, High 60, Specialist 80, Masterwork 95.
- Grade raises resistances and price steeply, and softens some penalties on heavy pieces. Heart Protector: Prototype cut 11%, value c.426; Shoddy 20%, c.1,425; Standard 32%, c.4,621; High 44%, c.9,949.
- Bandana value by grade: c.24, c.186, c.703, c.1,564, c.2,769, c.3,900.
- Weight does not change with grade.
- Shop stock grade depends on the owning faction; Shinobi Thieves shops are mostly Standard, some Shoddy and High.
- Starting gear is typically Shoddy with a 5% chance of Standard.
- Crossbows use these same six grades.
- Home-made armour grade depends only on the crafter's Armour Smith skill.

## Reading an armour tooltip
Also: blunt resistance, cut resistance, cut efficiency, harpoon resistance, coverage
- Blunt resistance: percentage removed from blunt damage.
- Cut resistance: percentage of cut damage "resisted".
- Cut resistance efficiency: the share of resisted cut damage that vanishes; the rest becomes stun damage.
- Harpoon resistance (points): pierce damage absorbed before bolts and animal piercing attacks start cutting.
- Coverage: per body part, the chance the piece applies when that part is hit. A Bandana covers 40% of the head; a Heart Protector 50% of the chest.
- Skills: flat bonuses or multipliers the piece applies (Melee defence +2, Stealth 0.54x, Athletics 1.10x).
- Weather protection: Duststorm, Acid, Burning, Gas percentages.
- Layers are checked in order: head, body armour, legwear, shirt, boots; damage already resisted is not reduced again.

## Early armour picks
Also: first armour, cheap armour, what to wear early, beginner gear
- Any armour beats none, but shop armour is poor value: you lose 75% on resale. Loot it instead.
- Wiki advice: buy the lowest grade (Prototype or Shoddy) Light Armour if you must buy, and wear Wooden Sandals.
- Wooden Sandals: c.50, Athletics 1.10x, combat speed 1.05x, no protection. They help you outrun trouble.
- Useful light pieces (Standard values): Drifter's Leather Jacket c.1,788 (Melee defence +5), Leather Shirt c.4,470, Samurai Clothpants (legs 100%), Drifters Leather Pants, Bandana c.703, Heart Protector c.4,621 (chest 50%).
- Dust Bandits drop Heart Protectors, Spiked Helmets, Armoured Rag Skirts and Samurai Boots.
- Samurai Boots cut Athletics to 0.75x: leave them off a runner.
- Dustcoat and Longcoat add acid-rain protection (80% and 70%).

## Footwear
Also: boots, sandals, shoes, run faster
| Footwear | Class | Athletics | Stealth |
|---|---|---|---|
| Wooden Sandals | Cloth | 1.10x | 1.0x |
| Drifter's Boots | Light | 1.0x | 0.90x |
| Plated Longboots | Medium | 0.90x | 0.45x |
| Samurai Boots | Heavy | 0.75x | 0.06x |
| Prisoner Shackles | Cloth | 0.8x | 0.6x |
- Standard-grade cost: Wooden Sandals c.50, Drifter's Boots c.596, Plated Longboots c.1,128, Samurai Boots c.1,212.
- Boots give 40% leg protection; sandals none.
- Only humans and Shek have a footwear slot.
- Sold at Boot Shops (Mongrel; Holy Boot Shop in Holy Nation towns), Clothing Shops and by looting.
- Prisoner Shackles count as footwear and must be picked or cut off.

## Crossbows compared
Also: crossbow types, crossbow list, crossbow stats, ranged weapons, bow, junkbow, tooth pick, ranger, spring bat, oldworld bow, eagle's cross
| Crossbow | Damage | Range | Reload |
|---|---|---|---|
| Junkbow | 12-30 | 30-40 m | 2.0-4.0 s |
| Tooth Pick | 11-32 | 38-50 m | 1.3-3.0 s |
| Ranger | 23-57 | 61-79 m | 2.0-4.5 s |
| Spring Bat | 35-101 | 41-54 m | 3.5-8.0 s |
| Oldworld Bow MkI | 23-64 | 82-109 m | 2.5-4.5 s |
| Oldworld Bow MkII | 40-77 | 82-118 m | 2.3-7.9 s |
| Eagle's Cross | 56-127 | 152-188 m | 4.1-10 s |
- Ranges run from worst to best grade; bolts are under "Crossbow ammunition".
- Weights: Junkbow and Tooth Pick 2 kg, Ranger 3.5 kg, Spring Bat 6 kg, Oldworld MkI 6.5 kg, MkII 7.5 kg, Eagle's Cross 9 kg.
- Standard-grade value: Junkbow c.1,379, Tooth Pick c.3,239, Spring Bat c.3,239, Ranger c.4,460, Oldworld MkI c.5,519, MkII c.6,579, Eagle's Cross c.7,539. Sell value is a quarter.
- The "required skill" shown on a crossbow has no effect, and all crossbows have 2x blood loss whatever the tooltip says.
- For a beginner or low-skill support shooter the wiki suggests a Tooth Pick or Ranger: short reloads, cheap, light.

## Crossbow ammunition
Also: bolts, arrows, ammo, toothpicks, regulars, heavies, longs
| Ammunition | Shots | Value | Used by |
|---|---|---|---|
| Bolts [Toothpicks] | 40 | c.243 | Junkbow, Tooth Pick |
| Bolts [Regulars] | 30 | c.243 | Ranger, Oldworld Bow MkI and MkII |
| Bolts [Heavies] | 20 | c.272 | Spring Bat |
| Bolts [Longs] | 10 | c.389 | Eagle's Cross |
- Toothpicks and Regulars weigh 1 kg per bundle; Heavies and Longs 2 kg. Bolts sell for half.
- The matching bolts must be in the shooter's inventory; the wrong type will not load.
- Sold at Ranger Shops (Bark, Catun, Heft, Sho-Battai; Black Scratch, Flats Lagoon, Mongrel, World's End), the Hub's bar, Adventurer Bars and Travel Gear. There are no Ranger Shops in Shek or Holy Nation towns.
- Longs are the rarest: bulk only at World's End and Mongrel.
- Bolts are made at an Arrow Making Bench after the Crossbow Bolts research.

## Blueprints
Also: blueprint, learn recipe, unlock weapon, unlock armour, research blueprint
- A blueprint is an item that unlocks a recipe or research instantly when used: right-click it in your inventory to learn it (code analysis). Most weapon and armour types can only be learned this way.
- Weapon blueprints are sold by weapon traders and differ by faction; armour, clothing and hat blueprints by armour, clothing and hat traders.
- After learning one you can craft that item at whatever grades your research and smith allow. The "Research Level" printed on weapon blueprints can be ignored.
- Each blueprint appears at most once per vendor list.
- The Bookshop in Black Scratch sells many weapon blueprints in one place.
- Tent blueprints (Camp Shelter c.200, Scrap Tent c.200, Mercenary Tent c.300) are at travel shops.
- Blueprints are among the best things to steal.

## Weapon blueprint prices
Also: blueprint cost, katana blueprint, sabre blueprint
- Sabres (Horse Chopper) c.1,500; Ninja Blades c.2,500; Polearms c.3,000; Longswords c.3,000; Holed Sabres c.3,500.
- The Plank c.4,000; Wakizashis, Combat Cleaver, Long Cleavers, Short-Cleaver, Paladin's Cross c.5,000 each; Cleavers c.2,000.
- Ringed Sabres, Jittes, Toppers c.6,000; Fragment Axe, Naginatas c.8,000.
- Katanas c.10,000; Desert Sabres c.12,000; Foreign Sabres c.14,000; Nodachi c.15,000 (needs Katanas); Exotic Weapons (Falling Sun) c.20,000.
- Bolts: Regulars c.400; Heavies c.1,000; Longs c.1,000.
- Iron Club and Staff need no blueprint: they come with the Basic Weapon Smithing research.
- A Bandana blueprint costs c.1,757, far more than the 2 Books of research that unlock the same thing.
- Shek Weapon Shops sell Plank, Fragment Axe and Long Cleaver blueprints.

## Research artifacts
Also: book, ancient science book, engineering research, AI core, research items
- Book: c.300, 1 kg, 2x2. The common research input. Sold by general shops, Mechanical Shops, Travel Gear, Hive Traders and caravans; often found in houses and ruins.
- Ancient Science Book: c.5,000, 2x2. Found in Ancient Labs, Lost Libraries and similar ruins; sold only at the Scraphouse and the Travel and Repairs Shops in World's End and Flats Lagoon, and those do not restock. Illegal in the Holy Nation.
- Engineering Research: c.8,000, weightless, 2x2. Near-guaranteed at Post-Ancient Workshop, Workshop Complex and Deadland Workshop; sometimes sold at the Scraphouse and Travel and Repairs Shops.
- AI Core: c.25,000, 1 kg, 4x4. Late-game ruins; three for sale at the Scraphouse. Illegal in the Holy Nation.
- Full tech tree totals: about 306 to 317 Books, 154 to 164 Ancient Science Books, 19 Engineering Research, 29 to 32 AI Cores (sources differ).

## Building and crafting materials
Also: materials list, building materials price, iron plates, fabrics, steel bars
| Item | Avg price | Weight |
|---|---|---|
| Raw Stone | c.36 | 4 kg |
| Raw Iron | c.90 | 9 kg |
| Building Materials | c.108 | 2 kg |
| Iron Plates | c.135 | 2 kg |
| Copper | c.180 | 4 kg |
| Fabrics | c.63 | 1 kg |
| Leather | c.156 | 1 kg |
| Electrical Components | c.216 | 1 kg |
| Armour Plating | c.504 | 5 kg |
| Steel Bars | c.648 | 4 kg |
| Robotics Components | c.2,838 | 2 kg |
| Water | c.25 | 10 kg |
- Building Materials and Iron Plates are stocked by General Shops, Mechanical Shops, Hive Traders and the Hub's bar.
- Slaver towns sell Building Materials, Iron Plates, Raw Iron, Raw Stone and Copper at half price.
- Crops: Wheatstraw c.40, Greenfruit c.30, Cactus c.15, Riceweed c.13, Hemp c.19, Cotton c.75, Strawflour c.400.

## Shop types and what they sell
Also: where to buy, which shop, vendor types, store list
- Bar: food, drink, sometimes first aid; recruits and mercenaries stand inside. Open at night.
- General Shop / Empire General Shop / Holy General Shop: trade goods, materials, Books, Basic First Aid Kits, Hacksaws, crops.
- Mechanical Shop / Adventurer Mechanical Shop: Building Materials, Iron Plates, Steel Bars, Copper, Books, crops, construction blueprints.
- Travel Gear / Travel and Repairs Shop: backpacks, first aid and splint kits, repair kits, Sleeping Bags, Ration Packs, maps, Books (and Robot Limbs at Travel and Repairs).
- Weapon Shop, Armour Shop, Clothing Shop, Headgear Shop, Boot Shop: that equipment plus its blueprints.
- Ranger Shop: crossbows and bolts.
- Hive Trader: mixed goods, hive shirts, Hashish; restocks every 6 hours.
- Thieves Guild: ninja gear and Thieves Backpacks at half price, members only.
- Scraphouse (Deadlands): top-grade weapons, artifacts, AI Cores.

## Shops in the early towns
Also: early shops, starting area shops, what is sold where
- The Hub: one bar (food, Basic First Aid Kits, Building Materials, Iron Plates, bolts, some weapons, blueprints) and the Thieves Guild tower. No backpack, armour or general shop.
- Squin (Shek): Armour Shop, two bars, General Shop, Police Station, Travel Gear, Weapon Shop.
- Stack (Holy Nation, humans only in practice): Armour Shop, bakery, three bars, Boot Shop, Clothes Shop, General Shop, Headgear Shop, Mechanical Shop.
- Bad Teeth (Holy Nation): Armour Shop, Weapon Shop, bakery, three bars.
- Sho-Battai (United Cities): two bars, bakery, General Shop, Headgear Shop, Mechanical Shop, Ranger Shop, Travel Gear, Slave Shop, Police Station, Thieves Guild.
- Border Zone Waystation: Adventurer Bar, Adventurer Mechanical Shop, Robotics Workshop.
- Hive Villages: Hive Trader and Hive Robotics Shop (closed to hive player characters).

## Sources
- https://kenshi.fandom.com/wiki/Items : equipment slots, item categories.
- https://kenshi.fandom.com/wiki/Guide_to_Equipment : weapon use rules, strength rule, armour stats explained, race restrictions table, crossbow tiers.
- https://kenshi.fandom.com/wiki/Weapons , https://kenshi.fandom.com/wiki/Weapons/Classes , https://kenshi.fandom.com/wiki/Weapons/Damage , https://kenshi.fandom.com/wiki/Weapons/Modifiers : slots, classes, weights, modifiers, grade names.
- https://kenshi.fandom.com/wiki/Unknown_(manufacturer) , https://kenshi.fandom.com/wiki/Ancient_(Manufacturer) , https://kenshi.fandom.com/wiki/Catun_Scrapmaster_(Manufacturer) , https://kenshi.fandom.com/wiki/Skeleton_Smiths_(Manufacturer) , https://kenshi.fandom.com/wiki/Edgewalkers , https://kenshi.fandom.com/wiki/Cross , https://kenshi.fandom.com/wiki/Homemade , https://kenshi.fandom.com/wiki/Meitou : manufacturer modifiers.
- https://kenshi.fandom.com/wiki/Katana , https://kenshi.fandom.com/wiki/Wakizashi , https://kenshi.fandom.com/wiki/Nodachi , https://kenshi.fandom.com/wiki/Iron_Club , https://kenshi.fandom.com/wiki/Iron_Stick , https://kenshi.fandom.com/wiki/Horse_Chopper : values, sell values, weights and strength by grade.
- https://kenshi.fandom.com/wiki/Strength , https://kenshi.fandom.com/wiki/Encumbrance : carry weight, penalties, hunger effect on Strength.
- https://kenshi.fandom.com/wiki/Food , https://kenshi.fandom.com/wiki/Guide_to_Health , https://kenshi.fandom.com/wiki/Dried_Meat , https://kenshi.fandom.com/wiki/Raw_Meat , https://kenshi.fandom.com/wiki/Campfire : food table, hunger rules, race hunger rates, cooking.
- https://kenshi.fandom.com/wiki/Medical_Items , https://kenshi.fandom.com/wiki/Basic_First_Aid_Kit , https://kenshi.fandom.com/wiki/Standard_First_Aid_Kit , https://kenshi.fandom.com/wiki/Splint_Kit , https://kenshi.fandom.com/wiki/Skeleton_Repair_Kit , https://kenshi.fandom.com/wiki/Skeleton_Repair_Bed : kits, charges, quality, recipes, repair bed rentals.
- https://kenshi.fandom.com/wiki/Bed , https://kenshi.fandom.com/wiki/Camp_Bed , https://kenshi.fandom.com/wiki/Sleeping_Bag , https://kenshi.fandom.com/wiki/Camping : healing rates, bed rental, camp beds.
- https://kenshi.fandom.com/wiki/Backpacks , https://kenshi.fandom.com/wiki/Wooden_Backpack , https://kenshi.fandom.com/wiki/Small_Backpack , https://kenshi.fandom.com/wiki/Scavenger%27s_Basket : backpack table, stacking, tricks and bugs.
- https://kenshi.fandom.com/wiki/Tools , https://kenshi.fandom.com/wiki/Hacksaw , https://kenshi.fandom.com/wiki/Lockpicking , https://kenshi.fandom.com/wiki/Lanterns , https://kenshi.fandom.com/wiki/Lantern , https://kenshi.fandom.com/wiki/Maps : tools, lanterns, map items.
- https://kenshi.fandom.com/wiki/Armour , https://kenshi.fandom.com/wiki/Light_Armour , https://kenshi.fandom.com/wiki/Medium_Armour , https://kenshi.fandom.com/wiki/Heavy_Armour , https://kenshi.fandom.com/wiki/Clothing , https://kenshi.fandom.com/wiki/Body_Armour , https://kenshi.fandom.com/wiki/Legwear , https://kenshi.fandom.com/wiki/Footwear , https://kenshi.fandom.com/wiki/Wooden_Sandals , https://kenshi.fandom.com/wiki/Bandana , https://kenshi.fandom.com/wiki/Heart_Protector , https://kenshi.fandom.com/wiki/Faction_Uniform : armour classes, grades, stats, uniforms.
- https://kenshi.fandom.com/wiki/Crossbows and the pages for each crossbow and bolt type: damage, range, weights, values, ammunition, skills.
- https://kenshi.fandom.com/wiki/Blueprints , https://kenshi.fandom.com/wiki/Research_Artifacts , https://kenshi.fandom.com/wiki/Book , https://kenshi.fandom.com/wiki/Ancient_Science_Book , https://kenshi.fandom.com/wiki/Engineering_Research , https://kenshi.fandom.com/wiki/AI_Core , https://kenshi.fandom.com/wiki/Tech_tree : blueprint prices and sources, artifacts.
- https://kenshi.fandom.com/wiki/Robot_Limbs : limb loss, limb prices, Holy Nation reaction.
- https://kenshi.fandom.com/wiki/General_Shop , https://kenshi.fandom.com/wiki/Empire_General_Shop , https://kenshi.fandom.com/wiki/Holy_General_Shop , https://kenshi.fandom.com/wiki/Travel_Gear , https://kenshi.fandom.com/wiki/Travel_and_Repairs_Shop , https://kenshi.fandom.com/wiki/Adventurer_Bar , https://kenshi.fandom.com/wiki/Adventurer_Mechanical_Shop , https://kenshi.fandom.com/wiki/Black_Market_Bar , https://kenshi.fandom.com/wiki/Hive_Trader , https://kenshi.fandom.com/wiki/Equipment_Shops , https://kenshi.fandom.com/wiki/Ranger_Shop , https://kenshi.fandom.com/wiki/Boot_Shop , https://kenshi.fandom.com/wiki/Shek_Weapon_Shop , https://kenshi.fandom.com/wiki/Empire_Weapon_Shop , https://kenshi.fandom.com/wiki/Thieves_Guild , https://kenshi.fandom.com/wiki/Smugglers_Bar : stock lists, prices, locations.
- https://kenshi.fandom.com/wiki/The_Hub , https://kenshi.fandom.com/wiki/Squin , https://kenshi.fandom.com/wiki/Stack , https://kenshi.fandom.com/wiki/Bad_Teeth , https://kenshi.fandom.com/wiki/Sho-Battai , https://kenshi.fandom.com/wiki/Waystation_(Border_Zone) : shops per town.
- Trade-culture pages (Empire, Slavers, Shek Kingdom, The Holy Nation, Swamper, Empire Lawless) on kenshi.fandom.com : illegal and never-stocked items.
- docs/game/economy.md, docs/game/character-stats.md and docs/game/ui-screens.md in https://github.com/VlcekM/meitouclient (notes on the original game's data and code): sell fractions by item kind, buy-back behaviour, animal price, carry capacity test, inventory pocket size used by that project.
- https://kenshi.fandom.com/wiki/Money_Making_Strategies : four Beak Thing Eggs fill an inventory (basis for the 8x10 grid inference).
- https://kenshi.wiki/Copper : differing size notation for the same item.
- https://kenshi.fandom.com/wiki/Guide_to_Equipment and https://github.com/VlcekM/meitouclient docs/game/ui-screens.md : weapon slots, red slots, right-click to equip (merged in from Interface).
- Weapon grade, armour quality level and crossbow reload facts merged in from Combat rest on the sources listed there.
