# Research, crafting and building

How a squad researches technology, crafts goods, buys or builds property, powers and feeds a base, automates work with jobs, and what an outpost attracts and how to prepare for it.

## Research: how it works
Also: research bench, technology, tech tree, unlock buildings, science
- Research needs a research bench you own, inside a building, and a character working at it.
- Put the cost items (Books and so on) into a research bench's inventory: per game-code notes the cost is taken from your bench inventories near the camera when a research is queued, and is never charged twice.
- Open the research window (the bench's research button or the research hotkey) and pick a technology; it joins the queue.
- If something is missing the game says "Cannot research '(name)'. Requirements not met." or names the bench level needed.
- Progress accrues only while someone operates the bench and its area is loaded (near the camera or one of your characters).
- When done: "Research complete: (name)".
- Window header: "RESEARCH - LEVEL n (CURRENT RATE: x)".
- Some technologies come only from Blueprints, not the bench.

## Small Research Bench
Also: first bench, starting research, research in a shack
- Cost: 3 Building Materials. Type: interior, so it must stand inside a building you own.
- It fits in a Small Shack, the smallest building.
- It researches everything at Tech Level 1.
- It cannot be upgraded into Research Bench II; that one is built separately.
- It needs no power.
- Efficiency ("output rate") 0.85, the lowest of the benches.
- Cheapest way to start: a collapsed Small Shack in The Hub or Stack (c.1,500), Building Materials to repair it and 3 more for the bench (c.108 each), and a few Books (c.300 each).
- Several benches can work at once, each additional one adding less.

## Research Bench II to VI
Also: bench upgrade, bigger research bench, bench power
| Bench | Cost (Iron Plates) | Power | Efficiency |
|---|---|---|---|
| Research Bench II | 10 | 0 | 90% |
| Research Bench III | 20 | 10 | 95% |
| Research Bench IV | 25 | 15 | 100% |
| Research Bench V | 30 | 25 | 105% |
| Research Bench VI | 35 | 30 | 110% |
- Each becomes buildable when the matching Tech Level research is finished.
- From level II up, select the bench and press its upgrade button instead of rebuilding.
- Research Bench II does not fit in a Small Shack; a Storm House or bigger is needed.
- Benches III and above draw power, so they need a generator or a powered town.
- Research Bench IV, V and VI are illegal buildings in the Holy Nation's rules, though its patrols have no dialogue that reacts to them.

## Tech levels: cost and time
Also: tech level 2, tech level 3, how many books, ancient science books needed
| Research | Cost | Listed time |
|---|---|---|
| Tech Level 2 | 6 Books | 4 hours |
| Tech Level 3 | 10 Books | 10 hours |
| Tech Level 4 | 4 Ancient Science Books | 16 hours |
| Tech Level 5 | 8 Ancient Science Books | 24 hours |
| Tech Level 6 | 2 AI Cores | 32 hours |
- Tech Level 2 lists Small House (2 Books) as its requirement, so reaching level 2 costs 8 Books (about c.2,400).
- Each level must be finished before the next appears.
- Tech level never drops, even if the best bench is lost.
- Advice from the wiki: research the next Tech Level before spending artifacts on side technologies.
- Everything in the tree needs roughly 306 to 317 Books, 154 to 164 Ancient Science Books, 19 Engineering Research and 29 to 32 AI Cores (sources differ), plus 2 each of Cactus, Cotton, Hemp, Riceweed and Wheatstraw.

## Research speed and the Science skill
Also: how long does research take, research rate, science skill
- Wiki: research rate = 0.5 + 0.009 x Science, so 0.5x at Science 0 and 1.4x at 100.
- Game-code notes (meitouclient): real hours = listed time x 0.3 x 1.3^(research level - 1), divided by bench efficiency and the Science factor. Tech Level 2's "4 hours" is 1.2 game hours at rate 1.0.
- With a Small Research Bench (0.85) and Science 1 (about 0.51) the rate is about 0.43, so Tech Level 2 takes roughly 2.8 game hours.
- A second bench working at the same time contributes 0.6x, a third 0.36x.
- Research trains Science; so do the Electrical Workbench and Hemp Processor.
- Greenlanders and Hive Princes learn Science 20% faster; Shek, Hive Workers and Hive Soldiers 20% slower.
- Low power slows a powered bench in proportion.

## First research order for a new squad
Also: what to research first, early tech, research priorities
- No item cost, only bench time: Storage Boxes: Ore, Storage Boxes, Storage Boxes: Farming (under 1 hour each), Item Storage, Gear Storage, Public Sales (4 hours listed each).
- Then, with Books: Small House (2) and Tech Level 2 (6).
- For income: Clothing Manufacture (1) and Hats and Headgear (2) to craft Bandanas.
- For safety and training: Simple Training Dummies (2), Lockpick Training (3).
- For food: Cooking (1), Wheatstraw Farming (2 Books + 2 Wheatstraw), Baking (2).
- For materials: Iron Plates (1).
- At Tech Level 2: Beds (2), Basic First Aid Kits (2), Sleeping Bags (1), Leather Armour Crafting (4), Mounted Crossbows (4), Light Wind Generator Theory (4).
- A shack-only squad can do every Tech Level 1 item; Tech Level 2 needs a bigger house for Research Bench II.

## Tech Level 1 research list
Also: level 1 technologies, small bench research list
- Core: Small House 2 Books (Storm House); Tech Level 2 6 Books; Item Storage, Gear Storage, Public Sales free.
- Industry: Iron Plates 1 Book (Manual Iron Refinery); Improved Stone Mining 3 Books; Storage Boxes, Storage Boxes: Ore, Storage Boxes: Farming free.
- Electrics: Wind Generator Theory 2 Books; Fuel Generator Theory 4 Books; Indoor Lighting 1 Book.
- Farming: Cooking 1 Book; Baking 2 Books; Wheatstraw, Cotton, Riceweed, Cactus Farming 2 Books + 2 of the crop each (Cactus needs Wheatstraw Farming first).
- Smithing: Basic Weapon Smithing 2 Books; Basic Weapon Grades 2 Books; Clothing Manufacture 1 Book; Hats and Headgear 2 Books; Simple Clothing Types 1 Book.
- Crafting: Fabric Manufacture 1 Book.
- Defence: Makeshift Walls 2 Books.
- Training: Simple Training Dummies 2 Books; Lockpick Training 3 Books.
- The wiki's Science page files Storage Boxes: Ore under Research Bench II; its own page says Tech Level 1.

## Tech Level 2 research: buildings, industry, power, food
Also: level 2 technologies, research bench II list, beds research, small wind generator research
- Core: Beds 2 Books; Medium Building Shells 6 Books (L-House, Longhouse, Bughouse); Tech Level 3 10 Books.
- Industry: Iron Plates II 2 Books (powered Iron Refinery); Improved Stone Mining 2 4 Books; Powered Stone Refinery 3 Books; Wells II 2 Books; Storage Boxes: Crafting free.
- Electrics: Light Wind Generator Theory 4 Books (Small Wind Generator); Biofuel 2 Books; Basic Exterior Lighting 1 Book; Light Post 1 Book.
- Farming: Advanced Cooking 2 Books (Foodcube, Gohan, Meatwrap); Desert Cooking 3 Books (Chewsticks, Dustwich); Hemp Farming 2 Books + 2 Hemp; Grog Distillation, Rum Brewing, Sake Distillation 6 Books each.
- All of these need Research Bench II, which costs 10 Iron Plates and a Storm House or larger to stand in.

## Tech Level 2 research: gear, medical, defence, training
Also: level 2 smithing, leather armour research, first aid research, mounted crossbow research
- Smithing: Leather Armour Crafting 4 Books; Basic Weapon Grades 2 to 4 (3, 4 and 5 Books); Heavy Weapons 6 Books; Crossbow Bolts 6 Books; Weapon Melting 1 Book (Item Furnace).
- Crafting: Basic First Aid Kits 2 Books; Sleeping Bags 1 Book; Hemp-Based Fabric 2 Books.
- Defence: Mounted Crossbows 4 Books; Defensive Walls 6 Books; Crossbow Turret Strings 2 Books; Corpse Disposal free.
- Training: Better Training Dummies 4 Books; Lockpick Training II 4 Books; Thievery Training, Assassin Training and Turret Training 2 Books each.
- Cheapest useful set for a small squad: Beds, Basic First Aid Kits and Sleeping Bags, 5 Books in all.

## Tech Level 3 research highlights
Also: level 3 technologies, engineering research uses
- Core: Tech Level 4 (4 Ancient Science Books); Heavy Building Foundations and Large Building Shells (1 Engineering Research each); Outpost Type III (2 Engineering Research).
- Industry: Steel Bars (1 Ancient Science Book); Ore Drill (2 Ancient Science Books); Iron Plates III 3 Books; Rain Collector 3 Books; Wells III (1 Ancient Science Book); Automated Mining Tech (1 AI Core).
- Electrics: Electrical Crafting 4 Books; Batteries 4 Books; Skeleton Repair Beds (2 Engineering Research).
- Smithing: Plate Armour Crafting (1 Engineering Research: Heart Protector, Armoured Rags); Medicine 6 Books (Standard First Aid Kit); Splints 4 Books; Crossbow Crafting (1 Engineering Research); Advanced Weapon Smithing (1 Ancient Science Book).
- Crafting: Robotics (1 Ancient Science Book; needs Electrical Crafting and Steel Bars).
- Farming: Hashish Production (1 Engineering Research).
- Defence: Imprisonment 1 Book (Prisoner Cage); Prototype Harpoon Turrets and Mounted Crossbows II (1 Ancient Science Book each).

## Tech Level 4 to 6 in brief
Also: late research, hydroponics research, ai core research
- Level 4: Chain Armour Crafting (3 Ancient Science Books), Advanced Medicine and Advanced Splints (1 each), Copper Alloys (1 Engineering Research), Semi-Automatic Ore Drill (4), Advanced Wind Generator Theory (2), Automatic looms, Tech Level 5 (8).
- Level 5: Hydroponics (1 AI Core) then each crop (2 to 4 Ancient Science Books), Fully Automatic Ore Drill (2 AI Cores + 2 books), Hybrid Stone Mine, Skeleton Arms and Legs (2 AI Cores each), Large Defensive Walls (3 Engineering Research).
- Level 6: Edgewalkers weapon grade (4 AI Cores), robot limb upgrades (2 AI Cores each), Strong Defensive Walls (4 Engineering Research), Steel Bars 3.
- Ancient Science Books and AI Cores come almost only from guarded ruins; plan expeditions, not shopping.

## Crafting stations at a glance
Also: workbench list, crafting bench cost, which bench makes what
| Station | Build cost | Makes |
|---|---|---|
| Clothing Bench | 3 Iron Plates | cloth clothing, Bandanas |
| Weapon Smith | 6 Iron Plates | melee weapons |
| Leather Tanning Bench | 3 Iron Plates | Leather |
| Leather Armour Crafting Bench | 8 Iron Plates | leather armour |
| Plate Beating Station | 4 Iron Plates | Armour Plating |
| Heavy Armour Smithy | 5 Building Materials + 10 Iron Plates | plate armour |
| Basic Medical Workbench | 3 Iron Plates | Basic First Aid Kit, Sleeping Bag |
| Medical Workbench | 6 Iron Plates | all kits and splints |
| Arrow Making Bench | 4 Iron Plates | bolts, Hinge, Spring Steel |
| Crossbow Crafting Bench | 8 Iron Plates | crossbows |
| Electrical Workbench | 10 Iron Plates | Electrical Components |
| Cooking Stove | 2 Iron Plates | all cooked food |
- Most are interior or interior/exterior, so they fit in a town house. Benches draw 2 to 10 power each (Plate Beating Station none); a bench without supply shows "No power".

## Using a crafting bench
Also: craft queue, queue button, repeat queue, critical success
- Select the bench; its panel has a "QUEUE..." button that opens the list of things it can make. Add items to the queue; "Repeat Queue" keeps it cycling.
- A character must be told to work the bench (right-click it, or Shift + right-click to make it a job).
- Ingredients must be in the bench's input slots; workers with hauling jobs fetch them from storage.
- Hovering a queue entry shows State, ETA, Predicted Result, Material Costs and Critical Success Chance.
- Critical success makes the item one grade higher; chance is about (skill - grade threshold) / 50.
- Injuries and darkness lower the crafter's effective skill: craft healed and under lights.
- Status words on a machine: "Working", "Output full", "Out of resource", "Production queue empty", "No power", "No workers".

## Clothing Bench and the Bandana start
Also: tailor, make clothes, armour smith training, bandana crafting
- Research Clothing Manufacture (1 Book), then build a Clothing Bench (3 Iron Plates, interior, 1 worker, 4 power).
- Starting recipes: Rag Loincloth, Rag Shirt, Martial Artist Bindings. Hats and Headgear (2 Books) adds Bandana, Turban, Tagelmust, Cap and more. Simple Clothing Types (1 Book) adds Wooden Sandals, Cloth Shirt, Cargopants, Gi.
- Input: Fabrics (about c.63 each). A Bandana uses 0.4 Fabrics.
- It trains Armour Smith; item grade follows that skill.
- Bandana sell value by grade: c.6, c.46, c.175, c.391, c.692, c.975.
- The wiki calls the Clothing Bench the best way to raise Armour Smith at first.

## Armour grade by Armour Smith skill
Also: armour quality crafted, armour smith levels
- Predicted grade by skill: Prototype from 0, Shoddy from 20, Standard from 40, High from 60, Specialist from 80. Masterwork only comes from a critical success.
- No research gates armour grades; only skill, light and injuries matter.
- Crafting time (hours) = 1.3 x materials x slot factor x material factor / speed, where speed = 0.5 + 0.009 x Armour Smith.
- Slot factors: head 0.6, body armour 1, shirt 3, legs 0.45, boots 0.5. Chainmail items take double.
- Materials needed scale with body coverage; non-fabric armour also uses Fabrics equal to 20% of its main material.
- Scorchlanders learn Armour Smith and Weapon Smith 20% faster; Hive Soldiers slower.
- Making Leather, Armour Plating or Chainmail Sheets also trains the skill.

## Weapon Smith bench and weapon grades
Also: weapon smithing bench, forge weapons, weapon quality crafted
- Named "Weapon Smith" in game. Level I: 6 Iron Plates, 8 power, uses Iron Plates, makes Rusted Junk to Refitted Blade. Level II: 20 Iron Plates, 12 power, uses Iron Plates + Fabrics, up to Catun No.3 (Tech Level 3). Level III: 35 Iron Plates, 30 power, uses Steel Bars + Fabrics (Tech Level 5).
- Skill needed per grade: Rusting Blade 10, Mid-Grade Salvage 15, Old Refitted Blade 20, Refitted Blade 25, Catun No.1 30, No.2 35, No.3 40, Mk I 50, Mk II 55, Mk III 60, Edge Type 1 70.
- Grades also need research: Basic Weapon Grades (to Catun No.1), Advanced Weapon Grades (to Mk III), Edgewalkers.
- Basic Weapon Smithing (2 Books) unlocks only Iron Club and Staff; other weapons need blueprints.
- Material per weapon: Iron Club 2, Wakizashi 4, Desert Sabre 5, Katana 7, Nodachi 10, Plank 12.

## Leather and plate armour chain
Also: leather armour bench, tanning, armour plating, heavy armour smithy
- Leather Armour Crafting (Tech Level 2, 4 Books) unlocks the Leather Tanning Bench and Leather Armour Crafting Bench, and the Trader's Leathers recipe.
- Leather Tanning Bench: 0.5 Animal Skin makes 1 Leather. 4 power.
- Leather Armour Crafting Bench: uses Leather and Fabrics; 5 power. Most leather armour needs a blueprint.
- Plate Armour Crafting (Tech Level 3, 1 Engineering Research) unlocks the Plate Beating Station and Heavy Armour Smithy, with Heart Protector, Armoured Rags and Armoured Rag Skirt.
- Plate Beating Station: 4 Raw Iron make 1 Armour Plating; no power, manual.
- Heavy Armour Smithy: uses Armour Plating and Fabrics; 10 power.
- Chain Armour Crafting (Tech Level 4, 3 Ancient Science Books): 3 Steel Bars make 1 Chainmail Sheets.

## Medical Workbench recipes
Also: make first aid kits, craft bandages, craft sleeping bag
- Basic Medical Workbench (3 Iron Plates, 5 power): Basic First Aid Kit = 1 Fabrics; Sleeping Bag = 8 Fabrics.
- Medical Workbench (6 Iron Plates, 10 power): Standard First Aid Kit = 1 Fabrics + 1 Hemp; Advanced First Aid Kit = 1.5 Fabrics + 2 Hemp; Splint Kit = 2.5 Fabrics + 1 Hemp; Advanced Splint Kit = 3.5 Fabrics + 2 Hemp.
- Research: Basic First Aid Kits (Tech Level 2, 2 Books), Sleeping Bags (1 Book), Medicine (Tech Level 3, 6 Books), Splints (4 Books), Advanced Medicine and Advanced Splints (Tech Level 4, 1 Ancient Science Book each).
- Working it trains Field Medic.
- Kits store in a Medicrate (2 Building Materials).

## Fabrics, looms and hemp
Also: fabric loom, cotton, make fabrics
- Fabric Loom (cotton): 6 Cotton make 1 Fabrics. Research Fabric Manufacture (1 Book).
- Fabric Loom (hemp): 3 Hemp make 1 Fabrics. Research Hemp-Based Fabric (Tech Level 2, 2 Books).
- Buying inputs, a Fabrics costs about c.450 from Cotton but c.57 from Hemp; shop Fabrics cost about c.63. Buy Fabrics or grow Hemp.
- Hemp Farms and hemp biofuel are illegal buildings in United Cities and Free Trader territory.
- Looms train Labouring. Automatic looms arrive at Tech Level 4.
- Fabrics also go into beds (4), kits, tents and weapon recipes at Weapon Smith II and III.

## Stone and Building Materials
Also: stone mine, stone processor, make building materials
- Stone Mine: 3 Building Materials, exterior, no research, 3 workers, no power, at most 80% efficiency. Output is Raw Stone; rate depends on the site's stone value (prospect first).
- Manual Stone Processor: 6 Iron Plates, 3 workers, no power, 40% efficiency. 2 Raw Stone make 1 Building Materials.
- Upgrades: Stone Mine II to VI (fewer workers, up to 110%); Stone Processor II (15 Iron Plates, 10 power, 60%) up to V (120%).
- Hybrid Stone Mine (Tech Level 5) makes Building Materials directly; Hybrid Stone Mine II needs no workers.
- Storage: "Storage: Stones" and "Storage: Building Materials" (free research Storage Boxes).
- Building Materials cost c.108 in shops, so early on buying is simpler than a manual stone line.

## Iron Plates and Steel Bars
Also: iron refinery, steel refinery, smelt iron, refine ore
- Manual Iron Refinery: research Iron Plates (1 Book); 6 Iron Plates to build; 1 to 3 workers; no power. 1 Raw Iron makes 1 Iron Plates.
- Iron Refinery (Iron Plates II): 10 Iron Plates, 2 workers, 10 power, 90%. Refinery II: 1 worker, 20 power. III and IV need no operator but still need loading.
- Steel Refinery (Tech Level 3, 1 Ancient Science Book): 20 Iron Plates, 2 workers, 10 power, 50%. 4 Iron Plates make 1 Steel Bars.
- Values: Raw Iron c.90, Iron Plates c.135, Steel Bars c.648.
- These are exterior machines: they need an outpost, not a town house.
- Ore Drill (Tech Level 3, 2 Ancient Science Books): 25 Building Materials, 2 workers, 20 power, makes Raw Iron anywhere iron prospecting is good. Drill III is unmanned.

## Hand mining rates
Also: ore node output, copper per day, iron per day, mining formula
- Game-data notes (meitouclient) give ore rocks these figures: Copper node 2 workers, Iron node 3 workers, each holding at most 5 pieces.
- Per worker per in-game day at a 100% node: Copper about 36 x skill factor; Raw Iron about 25.6 x skill factor.
- Skill factor = 0.5 + 0.9 x Labouring / 100: 0.5 at skill 0, 1.0 near 56, 1.4 at 100.
- So Copper per worker per day: about 18 at Labouring 0, 36 at 56, 50 at 100. Raw Iron: about 13, 26, 36.
- Output scales with the node's quality percentage.
- kenshi.zone's figures (36 a day at a standard copper node) agree.
- A node only produces while someone is working it.

## Other production machines
Also: electrical workbench, robotics bench, arrow bench, brewing, item furnace
- Electrical Workbench (Tech Level 3): 1 Copper makes 1 Electrical Components; 10 power; trains Science.
- Arrow Making Bench (Crossbow Bolts, 6 Books): Bolts [Toothpicks] or [Regulars] = 1.5 Iron Plates; [Heavies] = 0.35 Steel Bars; [Longs] = 0.5 Steel Bars; Hinge = 0.5 Iron Plates; Spring Steel = 2 Raw Iron + 0.2 Copper.
- Crossbow Crafting Bench: Junkbow = 1 Hinge + 4 Steel Bars; other crossbows need blueprints and Crossbow Parts.
- Robotics Bench (Robotics research): Skeleton Repair Kit = 0.5 Robotics Components + 1 Steel Bars.
- Grog Machine: 20 Wheatstraw + 1 Water. Rum Still: 20 Cactus + 1 Water. Sake Still: 20 Riceweed + 1 Water. Hemp Processor: 5 Hemp + 1 Water (20 power, illegal in several territories).
- Item Furnace (Weapon Melting, 1 Book; 4 Iron Plates; ground only): melts weapons into Raw Iron (weight / 5, between 0.5 and 5 each) and clears stolen flags.

## Owning a town building: rules and limits
Also: town house rules, bought building, public or private building, collapsed house
- Buildings are sold only by factions that are not hostile to you. The clicks: "Buy a building in town" in How-to.
- A bought building cannot be sold back or dismantled.
- Before purchase most of these houses are private homes: walking in gets you warned, then attacked.
- Buying replaces the old interior with an empty one.
- Ruined ("Collapsed") buildings are cheaper but have almost no usable floor until repaired.
- Set the building Public or Private from its panel: Public lets citizens in (needed for a Shop Counter); Private keeps them out.
- Buy one before founding an outpost: town guards deal with threats while you research and craft.

## House prices
Also: how much is a house, shack price, storm house price, longhouse price
- Game-data notes: price = building materials in the shell x 400 x the owner faction's cost multiplier, times 0.375 if ruined.
- Small Shack (5 materials): c.1,500 collapsed in The Hub and Stack; c.4,000 intact in Stack, Bad Teeth, Sho-Battai.
- Storm House (16): c.4,800 collapsed in The Hub. Old Storm House: c.6,000 collapsed.
- Longhouse (24): c.7,200 collapsed (The Hub, Squin, Bad Teeth); c.19,200 intact (Squin, Sho-Battai).
- Bughouse and L-House (35): c.10,500 collapsed in The Hub; a Bughouse in Trader's Edge is c.28,000.
- Snailhouse, Stationhouse: c.12,000 collapsed in The Hub.
- Towns safe from being overwritten by world events (which deletes everything inside your building): The Hub, Black Scratch, Mongrel, Mourn, Mud Town, Flats Lagoon and Waystations.

## Repairing a ruined building
Also: repair house, collapsed building, fix shack
- Hold right-click on the ruined building and choose "Repair"; every selected character starts working.
- Click the building to see how many Building Materials it still needs.
- Materials are taken from the workers' inventories and backpacks, one unit per delivery action, so the workers must carry them.
- Repair cost is in Building Materials only (c.108 each; the Hub's bar and general or mechanical shops sell them).
- You do not need all materials at once: work resumes when more are delivered.
- Repairing trains the Engineer skill.
- Even a bought-but-unrepaired shack can hold a little; repair it to fit benches and storage.

## What fits inside a town building
Also: build in town, interior buildings, rooftop
- Allowed: every "Interior" item (benches, beds, storage, Research Bench, Cooking Stove, Bread Oven, training dummies, Prisoner Cage) and items marked Interior/exterior.
- On an accessible roof: some exterior items, notably the Small Wind Generator and Rain Collector.
- Not possible in town: farms (except rooftop Hydroponics), wells, mines, refineries, the Grain Silo, the Item Furnace and large Wind Generators. So no Bread in town.
- Your building shares the town's power grid: a town short on power drains what you generate.
- Whether a town's own generators will run your benches, in The Hub for example, is not confirmed: check the bench panel for "No power" (unverified)
- Small Shack: room for a Small Research Bench and little else. Storm House: 4 to 5 times the floor space plus an open roof.
- NPCs can enter a Public building; set storage rooms Private.

## Town house or outpost first
Also: where to build base, base or house, when to build outpost
- A town house has no raids, no tax visits, guards nearby, shops next door, and enough room for research, clothing, weapon and medical benches and storage.
- An outpost is needed for farms, wells, mines, refineries, big generators and walls: anything "Exterior".
- An outpost draws scheduled faction visits and wandering raiders; the wiki's advice is to wait until the squad has cats and combat stats.
- Sensible path: shack and Small Research Bench in town, storage-box mining from the town, Tech Level 2 in a Storm House, crafting for cats, recruits and training, then an outpost.
- Raw materials can still be gathered outside and processed inside the town house.
- Only Building Materials and Iron Plates are needed for most early interior items.

## Build mode: placing things
Also: build menu, construct, place building, ghost colour
- Open build mode (the Build button, bottom right, or the build hotkey). Opening it pauses the game.
- Categories include Buildings, Camping, Crafting, Defence, Farming, Food, Interior, Lights, Mining, Power, Storage, Tech, Training, Walls.
- Only researched items are listed. Each shows "Materials cost:" and "Estimated build time:".
- Pick an item, move the ghost, click to place, then confirm.
- Ghost colours: green can be placed; red cannot (obstruction); blue is too close to a town, or an interior item that must go inside your own building.
- Messages: "Can't build too close to another town.", "Too close to another building.", "Can't place in a building you don't own.", "Can only be placed on certain locations (marked by blue nodes)."
- A placed item is a wireframe site until built.

## Constructing a placed building
Also: construction, deliver materials, build time, engineer
- Characters must carry the listed materials to the site; each delivery action moves one unit of each missing material from their inventory or backpack.
- Any squad member can add materials and labour; progress stops when delivered materials run out and resumes later.
- With a build job set, a builder fetches materials from your own storage nearby.
- Build speed scales with the Engineer skill, from 0.3x at 0 to 2.0x at 100; the menu's "Estimated build time" assumes about skill 41.
- Extra builders help with diminishing returns.
- Completion message: "Building '(name)' construction complete".
- Dismantling returns part of the materials.
- Select a finished building to see its condition, contents and upgrade button.

## Building shells and their cost
Also: shack cost, house cost, building materials needed
| Shell | Building Materials | Research |
|---|---|---|
| Small Shack | 5 | none |
| Storm House | 16 | Small House |
| Longhouse | 24 | Medium Building Shells |
| Bughouse | 35 | Medium Building Shells |
| L-House | 35 | Medium Building Shells |
| Watchtower | 60 + 10 Iron Plates | Large Building Shells |
- Small Shack door lock is level 15; so is the Storm House's.
- Storm House, Longhouse, Bughouse and L-House have usable roofs.
- Outhouse (1 Building Material) is decorative.
- Bigger shells (Y-House, Snailhouse, Stationhouse, Stephouse, Outpost s-III and s-IV) need Engineering Research.
- Any shell placed outside a town founds or extends an outpost.

## Camping structures that are not an outpost
Also: campfire, camp bed, tent, temporary camp
- Campfire: free, placed anywhere, cooks Raw Meat into Dried Meat.
- Camp Bed: uses 1 Sleeping Bag (returned when dismantled); 4x healing.
- Scrap Tent (1 Animal Skin), Mercenary Tent and Flat Shelter (1 Fabrics each) give rain cover and need blueprints (c.200 to c.300).
- None of these creates a player town, so they attract no faction events.
- Use them for mining trips and travel instead of founding an outpost by accident with a Small Shack.

## Founding an outpost
Also: start a base, player town, settlement, your outpost
- Placing a building shell (or other town-creating structure) outside every town creates a player town, first named "Your Outpost", marked on the map. It can be renamed.
- Shells cannot be placed within a town's block radius: about 2.5 times the town's radius for cities, less for ruins.
- Later buildings near it join the same outpost.
- From that moment faction events can be rolled against it whenever one of your characters is there.
- The wiki's Events page says wandering "base attack" squads only target a base that has a gate.
- Prospect first (Prospect button, lower right): the window lists Water, Fertility, Stone, Iron, Copper, wind speed and the Arid/Green/Swamp mix.
- Check which faction's towns are in range: see the tax and raid sections.

## Outpost level and map icon
Also: town level, base size, outpost icon
- Level 0 "Small place": any building.
- Level 1 "Village": any one of a gate, Research Bench II or better, 2 buildings with interiors, or 4 turrets.
- Level 2 "Outpost": a gate plus one of Research Bench IV or better, 5 buildings, or 5 turrets.
- Level 3 "Town": a gate, Research Bench IV or better, 5 buildings and 7 turrets.
- Walls, farms, storage, power and population do not count.
- The level is only recalculated when you leave the build menu near the base.
- Level matters for some dialogue: United Cities tax collectors insult a base under level 2; the Shek Tribute Round needs level 1 and 5 characters; a level 3 base with more than 15 characters turns a Slave Raid away.

## Good areas for a first outpost
Also: base location, where to settle, best base spot
- Border Zone (around The Hub): many high-quality iron and copper veins, but Dust Bandits and Starving Bandits roam and Dust Bandits extort bases near their camps.
- Okran's Pride (Holy Nation, south of Blister Hill): fertile, good stone and iron, patrols kill bandits and animals. Cost: Prayer Day, and trouble for female-only or non-human squads.
- Shem: 100% iron and 80% copper deposits, flat land, few bandits, no tax visits; arid, and far from towns.
- Gut, Howler Maze, High Bonefields, Northern Coast, Leviathan Coast, Fishman Island: rich but for stronger squads (Beak Things, cannibals, crabs).
- United Cities land brings a c.3,000 weekly tax within range of its towns.
- The Swamp needs no farm watering.

## Power basics
Also: electricity, generator, no power, battery
- Each machine lists Power Consumption; generators list Power Output. A base's panel shows power generated against power required and battery charge.
- If supply is short, machines are not switched off: production, crafting, research and powered farms slow in proportion to the share of demand met.
- Each powered machine has "Power" (on/off) and "Battery" toggles on its panel.
- Typical demand: Research Bench III 10, IV 15, V 25, VI 30; Weapon Smith 8; Clothing Bench 4; Electrical Workbench 10; Iron Refinery 10 to 40; Stone Processor II 10; Well II 8; Hemp Processor 20; Hydroponics 10.
- No power needed: Small Research Bench, Research Bench II, Stone Mine, Manual Iron Refinery, Manual Stone Processor, basic Well, Plate Beating Station, Mounted Crossbow, storage.
- Battery Bank (Batteries research, Tech Level 3): 4 Electrical Components + 2 Iron Plates, stores power for calm spells.

## Wind generators
Also: wind power, small wind generator, wind turbine
| Generator | Max output | Wind range (mph) |
|---|---|---|
| Small Wind Generator | 25 | 0.89 to 5.59 |
| Wind Generator | 50 | 2.24 to 11.18 |
| Wind Generator II | 100 | 2.24 to 11.18 |
- Wind Generator: research Wind Generator Theory (2 Books); 8 Iron Plates + 5 Copper; exterior only.
- Small Wind Generator: Light Wind Generator Theory (Tech Level 2, 4 Books); 7 Iron Plates + 4 Electrical Components; works in light wind almost all the time and may be built on a town house roof.
- Wind Generator II: Advanced Wind Generator Theory (Tech Level 4); upgrade costs 8 Electrical Components.
- Output follows current wind, which changes with weather; some zones have no wind at all. Prospecting shows wind speed.
- A generator shows "No Wind" when it cannot turn.

## Fuel generators and biofuel
Also: small generator, generator II, fuel, biofuel distillery
- Small Generator: Fuel Generator Theory (4 Books); 4 Copper + 4 Iron Plates; interior or exterior; output 40, up to 70 with the two Upgraded Small Generators researches.
- Generator II: Heavy Generator Theory (Tech Level 3, 2 Ancient Science Books); 10 Electrical Components + 6 Iron Plates; output 100 (130 with upgrades); burns about 6.5 Fuel per day at full load.
- Fuel: c.192 from construction traders, or made in a Biofuel Distillery (6 Iron Plates, Biofuel research 2 Books): 4 Greenfruit or 4 Wheatstraw make 1 Fuel; the Hemp version is twice as effective.
- A generator without fuel shows "Out of fuel".
- Fuel use scales with the load actually drawn.
- Use fuel where wind is unreliable; otherwise wind plus a Battery Bank is free.

## Farming basics
Also: grow food, crops, fertility, environment, farm efficiency
- Each crop has an environment match per zone type:
- Arid: Cactus 100%, Wheatstraw 50% (the Wheat Farm page says 60%), Hemp 40%.
- Green: Cotton, Greenfruit, Hemp, Wheatstraw 100%.
- Swamp: Hemp and Riceweed 100%.
- Zones can mix environments and the percentages add up. Prospecting shows the mix and the local Fertility, which scales growth and yield.
- Farms need Water delivered into them; rain tops them up when it rains.
- Harvest chance per plant depends on the Farming skill: about 50% at skill 0, 89% at 25, 100% from about 33, multiplied by environment and fertility.
- Unskilled farmers waste crops: train first on the public farms in Swamp towns, where taking crops is not treated as a crime.
- Raptors eat crops in some regions.

## Crop table
Also: crops, Wheatstraw, wheat, Greenfruit, Riceweed, Cactus, Hemp, Cotton, crop growth time, water per day, farm yield
| Crop | Water per day | Growth (hours) | Small farm yield |
|---|---|---|---|
| Cactus | 2 | 24 | 16 |
| Wheatstraw | 5 | 22 | 25 |
| Hemp | 6 | 21.6 | 25 |
| Greenfruit | 10 | 23.3 | 40 |
| Riceweed | 10 | 15 | 30 |
| Cotton | 10 | 30 | 30 |
- Figures are from the wiki's Farming table; individual farm pages differ slightly (Cotton 6 water, Wheatstraw 24 hours).
- Water use is multiplied by the biome: desert biomes use far more than the listed figure (game-data notes give 8x in "Desert", 0.1x in the Floodlands).
- A ripe crop must be harvested within a limited time (Greenfruit about 18 hours, Cotton 20, Riceweed 24, Wheatstraw 48, Cactus 67) or it dies.
- Wheatstraw does not die when out of water; it just stops growing.

## Building farms
Also: farm cost, farm sizes, seeds needed, vegetable farm
- A farm costs crop items, not Building Materials: Small 10; Medium 25 (Cactus and Hemp 20, Riceweed 30); Large 40 (Cactus and Hemp 30, Riceweed 50); Extra Large 60 (Cactus 40; only Cactus, Cotton, Wheatstraw).
- All sizes occupy the same ground; upgrade later and harvested crops still in the farm count toward the upgrade.
- Vegetable Farm (Greenfruit) needs no research. Wheat, Cotton, Riceweed, Cactus farms: 2 Books + 2 of the crop each at Tech Level 1. Hemp Farm: Tech Level 2.
- Buy seed crops at Farm Shops, Mechanical Shops or Hive Traders (Wheatstraw c.40, Greenfruit c.30, Cactus c.15, Riceweed c.13, Hemp c.19, Cotton c.75).
- Each farm takes 1 to 4 workers at harvest.
- Each crop has its own storage box (Storage: Wheatstraw and so on).

## Water: wells, rain collectors, tanks
Also: well, water supply, rain collector, water tank
- Well: 5 Building Materials, exterior, no research, 1 worker, 75% efficiency. Output depends on the site's Water value; low ground near water is best. Game-data notes give about 36 Water a day at 100%, holding 10.
- Well II (Wells II, 2 Books): unmanned, 8 power, 100%. Well III: 10 power, 125%.
- Rain Collector (Tech Level 3, 3 Books; 4 Iron Plates): unmanned, no power, holds 10 Water, works only in non-acid rain; can go on a town roof.
- Water Tank (free Storage Boxes: Farming; 3 Iron Plates): stores 100 Water.
- Water weighs 10 kg and is 5x5 in the grid, so keep wells beside farms.
- Shops sell only a few Water per day (c.25).
- To automate: Shift + right-click the Well and the farm to create water jobs, then check their order in the job list.

## Cooking recipes
Also: cooking stove, make food, recipes, food ingredients
- Cooking Stove: research Cooking (1 Book); 2 Iron Plates; interior; 1 worker; 2 power; trains Cooking.
- Dried Meat = 1 Raw Meat.
- Cooked Vegetables (25) = 8 Greenfruit + 1 Water.
- Rice Bowl (25) = 10 Riceweed + 1 Water.
- Chewsticks (20) = 8 Cactus + 0.25 Water (Desert Cooking).
- Dustwich (70) = 1 Bread + 8 Cactus (Desert Cooking).
- Gohan (75) = 8 Greenfruit + 10 Riceweed (Advanced Cooking).
- Foodcube (75) = 1 Bread + 8 Greenfruit (Advanced Cooking).
- Meatwrap (50) = 1 Bread + 1 Raw Meat (Advanced Cooking).
- Numbers in brackets are nutrition. Cooking skill only changes speed.
- A Campfire handles Raw Meat without any research.

## Bread: Grain Silo and Bread Oven
Also: flour, strawflour, baking, bread chain, wheat to bread
- Research Baking (2 Books): Grain Silo, Bread Oven, Flour Storage, Bread Basket.
- Grain Silo (4 Iron Plates, exterior, 1 worker, 4 power): 10 Wheatstraw make 1 Strawflour. Trains Farming.
- Bread Oven (4 Building Materials, interior): 1 Strawflour + 0.25 Water make 1 Bread (30 nutrition). It runs by itself; it only needs hauling.
- So 10 Wheatstraw become 30 nutrition as Bread, or 75 as a Foodcube with 8 Greenfruit.
- The Grain Silo is exterior-only: no Bread production inside towns.
- Strawflour can be bought (c.400) to bake in town.
- Bread Basket holds 50 Bread and hungry characters eat from it.

## Feeding a base automatically
Also: food store, bread basket, animal feeder, base food
- Food Store (Item Storage research; 1 Building Material; 18x18, stacks x4): holds every food except Bread. Hungry squad members walk to it and eat.
- Bread Basket: same for Bread.
- Animal Feeder (1 Building Material on its own page, 2 in the storage table): a food box animals and people eat from; does not stack.
- General Storage Boxes are not used for eating.
- Give the cook jobs in this order: operate Cooking Stove, then haul to Food Store.
- Characters sometimes snack from the store even when full, so production must outpace it.
- Shek tribute collectors and raiders that "loot food" take from these containers.
- Skeletons need no food at all.

## Hydroponics
Also: indoor farming, grow food in town
- Research Hydroponics at Tech Level 5 (1 AI Core), then each crop: Wheatstraw 2 Ancient Science Books; Greenfruit, Hemp, Riceweed 4 each.
- Each unit: 10 of the crop + 4 Iron Plates + 2 Electrical Components; 10 power; needs Water.
- Ignores environment and fertility; grows faster (10 to 15 hours) and can be placed indoors or on roofs, where even acid rain waters it.
- Far too expensive for an early squad; listed so it is not mistaken for an early option.

## Storage containers
Also: storage box, chest, where to store items, stack size in storage
- General Storage Chest and General Storage Boxes (Item Storage research, free; 1 Building Material; 18x18 grid; stacks x5) hold anything.
- Metal Chest: 1 Iron Plates, 12x12, no stacking.
- Armour Storage (22x18), Weapon Cabinet, Weapon Stand, Crossbow Locker, Boltbox: Gear Storage research, free.
- Single-item stores hold one material in bulk: Storage: Copper 100, Storage: Ore 100, Storage: Iron Plates 50, Storage: Building Materials 100, Storage: Stones 100, Storage: Steel Bars 25, Fabric Chest 50, crop stores 100 to 250, Water Tank 100.
- Workers haul only into the matching specialised store, and benches draw inputs from them.
- Putting stolen goods into specialised storage clears the stolen flag; the Crossbow Locker does this for any item.

## Jobs: automating work
Also: job list, permanent job, shift right click, auto haul, labour
- Hold Shift and right-click a task target (ore node, machine, farm, storage, bench) to add it to the selected character's job list.
- The character runs the first job in the list that can be done, moving down when one is blocked (output full, inputs empty) and returning when it frees up.
- Jobs only run while the character's Jobs button is on.
- Reorder by dragging entries in the Jobs window; remove unwanted ones there.
- Job kinds: operating a machine, hauling to a storage, first aid (medic, robotics), engineering (building and repair), collecting corpses, looting dead animals.
- Mining with a matching storage built adds hauling by itself.
- Jobs are dropped if the character goes too far from the base they were set at.
- Becoming a slave wipes the job list.

## Job lists that work
Also: job order, miner jobs, farmer jobs, cook jobs
- Miner: mine Copper node, then haul to Storage: Copper.
- Refiner: operate Iron Refinery, then haul to Storage: Iron Plates. Put hauling after machine work, or the worker shuttles between the two.
- Farmer: haul Water from Well to farm, harvest farm, haul to the crop storage.
- Cook: operate Cooking Stove, haul to Food Store.
- Researcher: operate Research Bench only.
- Builder: an engineering job makes the character fetch materials from storage and build queued sites.
- Medic: switch on the medic behaviour so wounded squad members get bandaged without orders.
- Keep one fighter free of jobs near the gate.
- Check the list after each Shift + right-click: one click can add several entries.

## Lighting
Also: lights, dark penalty, night work
- Work in darkness is penalised: mining, crafting, fighting and robotics all lose effectiveness.
- Indoor Lighting (1 Book): Ceiling Lamp, Ceiling Fan Lamp, Electrical Torch Post. Basic Exterior Lighting (Tech Level 2): Spotlight. Light Post (Tech Level 2).
- Electric lights need power; outdoor lamps draw nothing by day.
- A crafter's predicted grade drops at night without light, so light every bench.
- A Lantern in the Belt slot helps a single worker.
- The wiki is unsure whether torch posts and campfires remove the penalty.

## What an outpost attracts
Also: base events, raids, visits, why am I attacked
- Every 6 game hours each faction rolls for a new event; it runs only one at a time.
- The base must be within the event's range of that faction's town or camp; closer means likelier.
- A player character must be at the base: events do not target empty bases.
- Scheduled visits appear with a countdown in the Events list on the Factions window.
- Three families: tax or tribute visits (major factions and some gangs), unprovoked raids (bandits, cannibals, slavers), and trade caravans.
- Refusing or beating a visit schedules a bigger follow-up.
- Many first visits happen once per game; later ones are follow-ups.
- A campaign beaten by third parties on its way often never returns.
- Separate from events, wandering raider squads attack bases they pass.

## Tax and tribute visits by faction
Also: tax collector, tribute, protection money, faction visits
| Faction | Event | Range | Demand |
|---|---|---|---|
| United Cities | Tax Man Visit | 3,500 | c.3,000 a week |
| The Holy Nation | Prayer Day | 2,000 | pray with the priest |
| Shek Kingdom | Tribute Round | 1,500 | food from your stores |
| Dust Bandits | Bandit Demands | 4,500 | c.2,000 every 2 days |
| Traders Guild | Traders Guild Visit | 5,000 of Trader's Edge | c.4,000 a week |
| Hounds | Hound's Welcome | 2,500 of Rot | join them |
| Stone Rats | Stone Rat Visit | 3,800 | payment (amount not confirmed) |
- Ranges are the wiki's figures in metres from that faction's locations.
- Allies of a faction are not taxed by it; enemies get assaults instead.
- In every case the leader shouts for you to come and talk: select a character and speak to them.

## United Cities tax in detail
Also: tax man, tax evasion, samurai tax
- Triggers for a base within 3,500 of a United Cities location; 50% a day inside 2,200.
- 3 to 6 Samurai and a Samurai Sergeant arrive. Talk to the sergeant.
- Pay c.3,000: they leave; a Tax Collector returns every 140 to 160 hours for c.3,000 (sometimes c.4,500).
- "Can't afford it": they return in 60 to 72 hours wanting c.4,500.
- Ignore or refuse: Tax Evasion Enforcement in 12 to 72 hours, two or more squads of 10 to 20 Samurai Conscripts plus Samurai. Interrupt its leader to pay a c.6,000 fine instead.
- Beating the enforcement brings a United Cities Assault in 72 to 144 hours.
- Never happens if you are allied with the United Cities or Anti-Slavers, or hostile to the United Cities.
- Hemp Farms and Hemp Processors seen by Samurai trigger a Drug Bust.

## Holy Nation Prayer Day
Also: prayer day, Holy Priest visit, outpost in Holy Nation land
- Triggers within 2,000 of a Holy Nation location; 50% a day inside 1,500.
- A Holy Priest with 5 High Paladins and 4 Holy Servants arrives and asks to pray.
- To pass: the character who talks must be Human, the squad must include at least one male, and The Holy Flame must be in inventory. The first time, the priest hands out a free copy.
- Repeats every 100 to 160 hours.
- Failing schedules a Holy Nation Assault (Minor): non-human speaker 10 to 20 hours, attacking the priest 12 to 24, all-female squad 12 to 36, ignoring them 36 to 48.
- Non-humans seen at the base cause demands to hand them over; a Human carrying The Holy Flame can claim them as servants.
- Stops if you become their enemy, ally the Shek Kingdom or Flotsam Ninjas, or the Phoenix is gone.

## Shek Tribute Round
Also: shek tribute, food tribute, return for blood
- Triggers within 1,500 of a Shek Kingdom settlement (15% a day inside 1,000) for a base of level 1 or more with 5 or more characters.
- 6 to 9 Shek Warriors arrive.
- Accept: each takes about 10 food items from your food containers; they return every 120 to 250 hours.
- Negotiate or challenge: they leave and Return For Blood comes in 24 to 30 hours (challenging gives +1 Shek relations).
- Ignore: Return For Blood in 12 to 24 hours.
- The wiki rates this the costliest tax if the stores are full; food lying on the ground is not taken.
- Not triggered for allies or enemies of the Shek Kingdom.
- A base near Squin or Admag must plan for this.

## Dust Bandit demands
Also: Bandit Demands event, bandit extortion at an outpost, Dust Bandits at my base
- Triggers within 4,500 of a Dust Bandit location or camp; 20% a day inside 2,000. This covers much of the Border Zone.
- One or two squads of 6 to 10 Dust Bandits and 1 to 4 Dust Bandit Bowmen under a Dust Boss arrive and demand a talk.
- Pay c.2,000: they return every 42 to 56 hours.
- Refuse or ignore: they attack, breaking gates.
- Stabbing the boss in dialogue makes them flee, then Bandit Rage arrives in 20 to 50 hours: 3 to 6 squads.
- Beating them only delays the next demand (50% chance in 50 to 80 hours).
- Ends for good when the Dust King is dead (bounty c.35,000).
- For a small squad paying c.2,000 is far cheaper than losing a fight.

## Unprovoked raids by region
Also: raids list, cannibal raid, slave raid, ninja raid
- Black Dragon Ninjas (Bandit Raid): within 4,500 of the Tower Of Ninjas in the Border Zone; two squads of about 9 to 11.
- Band of Bones (Raid): within 5,000 of the Exile Camp.
- Kral's Chosen (Shek Proving): within 4,000 of New Kralia.
- Cannibals (Cannibal Raid, Scrawny Raid): within 4,000 of their villages or camps, bases with 5 or more characters; dozens of Scrawny Cannibals who carry off the fallen to be eaten.
- Slave Traders (Slave Raid): within 4,000 of their locations, 5 or more characters; captives become slaves.
- Reavers (Blooded Raid): within 8,000 of their locations.
- Sand Ninjas (Ninja Raid): within 5,000 of the Cactus Den.
- Red Sabres (Red Sabre Raid): within 4,200 of their hideout in the Swamp.
- Most stop when the faction's leader is killed or captured.

## Wandering base attacks
Also: base attack, random raid, wandering attackers
- Roaming squads of certain factions attack player bases they come near; this is separate from scheduled events.
- Factions that do it include Dust Bandits, Starving Bandits, Vagrants, Black Dragon Ninjas, Band of Bones, Red Sabres, Swamp Ninjas, Rebel Farmers, Skeleton Bandits, Crab Raiders, spiders and wolves.
- Per the wiki's event notes they start only if the base has a gate, one of your characters is within 2,500 units, and the faction's cooldown has passed.
- Cooldown by the "Town attacks frequency" option: Normal 32 to 96 hours, Fewer 72 to 144, Rare 130 to 188, Never none.
- Raiders break gates, fight whoever they meet, and some loot food or free prisoners.
- Game-code notes: raids do not damage machines or building shells; only walls, gates and doors lose health.

## Trade caravans that visit
Also: caravan, traders visiting base, hive caravan, beast trader
- Caravan Visit (Traders Guild): bases within 11,000 of Trader's Edge. Sells kits, Foodcubes, Gohan, Ration Packs, some Books. Has no cats until you buy something.
- Materials Trader and Farm Trader (Western Hive): bases within 11,000 of a hive location; 8 to 10 Caravan Drones and Pack Beasts with materials or crops.
- Beast Trader (Nomads): sells Goats, Pack Bulls, Bonedogs and Pack Beasts at the gate; several thousand cats each. Game-code notes price an animal at 14,000 x (age + 0.1).
- The leader shouts an offer; talk to them to trade.
- Hive traders are common visitors in the Border Zone.
- Caravans ignore the raid frequency option.

## Walls and gates
Also: defensive wall, makeshift wall, gate, fortify
- Makeshift Walls (2 Books): Makeshift Wall, 1 Building Material per segment; Makeshift Gate, 5 Building Materials, 12 hours.
- Defensive Walls (Tech Level 2, 6 Books): Defensive Wall II (turrets can be mounted on top) and Defensive Gate II (10 Building Materials). Levels III and IV need Engineering Research.
- Placing: click to start, drag, click to pin corners, right-click to finish. The blue arrows must point outward.
- Test the ring: close the gate and order a character outside; if they cannot path out, it is sealed.
- Enemies can still slip in where walls meet rocks or cliffs.
- A gate raises the outpost level and, by the wiki's notes, is what makes wandering base attacks possible; by that rule a gateless cluster of buildings is not targeted by them (scheduled events still come).
- Raiders break gates; repair them after each attack.

## Turrets
Also: mounted crossbow, harpoon turret, base defence, turret stats
- Mounted Crossbow (Tech Level 2, 4 Books): 6 Iron Plates, no power, pierce damage 55, range 65 m, reload 2 to 8 s, 180 degree arc; weak against heavy armour. Can stand on the ground, on walls or on a Storm House roof.
- Harpoon Turret (Tech Level 3, 1 Ancient Science Book): 3 Copper + 7 Iron Plates + 3 Steel Bars, 3 power, damage 75, range 120 m, reload 2 to 4 s.
- Turrets need no ammunition. A character must man each one (Shift + right-click it to make that a job), with RANGED on.
- Turrets skill: accuracy and reload from 25% at skill 0, helped by Perception and Dexterity; friendly fire avoidance 0% at skill 0, 100% at 50. Untrained gunners shoot your own fighters.
- Firing from above improves range, accuracy and damage; from below worsens them.
- Training Turret (Turret Training, 2 Books) trains gunners safely.
- Each turret counts toward the outpost level.

## Preparing an outpost for trouble
Also: defend base, base checklist, survive raid
- Before building, check ranges to United Cities, Holy Nation, Shek, Dust Bandit and cannibal locations and keep the cats, book or food each will demand.
- Keep beds (8x healing), first aid kits and a spare medic inside a building.
- Keep food in containers; keep a reserve of c.5,000 for tax or tribute.
- Standard defence: a wall ring with one gate, and Mounted Crossbows on walls or Storm House roofs manned by characters with some Turrets skill.
- Without walls: keep weak workers indoors with the door shut; Beak Things, for one, cannot follow into buildings.
- Hire Mercenaries from a bar to guard the outpost: about c.2,000 per two days, up to eight days.
- Being allied with a nearby faction brings reinforcements against some raids.
- Lower the "Town raid events" frequency and size options if needed.

## Training equipment: research and build cost
Also: build training dummy, build lockpick box, training buildings, train skills at base
- Training Dummy MkI: research Simple Training Dummies (2 Books); 4 Iron Plates.
- Locksmith Training Box: research Lockpick Training (3 Books); 2 Iron Plates.
- Thief Training Boxes, Assassination Dummies and the Training Turret are researched the same way.
- All are interior items: fine for a town house.
- Police stations and Thieves Guild towers have the same equipment; using it uninvited annoys the owners.
- How far each one trains a skill: "Training equipment caps (dummies, lock boxes, turrets)" in Stats and training.

## Prisoner Cage
Also: cage, imprison, hold captive
- Research Imprisonment (Tech Level 3, 1 Book); 5 Iron Plates; interior or exterior; lock level 15.
- To cage someone: hold right-click on the body and choose "pick up", carry them to the cage, then right-click the cage or choose "put in".
- A selected character can "get in" by the same menu; a caged player character picks the lock with "escape".
- Talking to a prisoner lowers relations with their faction by 1.
- Raiders "liberate captives", so cages draw attention.
- A cage owned by a law faction pays out a prisoner's bounty when you put them in.

## Sources
- https://kenshi.fandom.com/wiki/Technology , https://kenshi.fandom.com/wiki/Tech_Level_(Tech) , https://kenshi.fandom.com/wiki/Research_Bench , https://kenshi.fandom.com/wiki/Small_Research_Bench , https://kenshi.fandom.com/wiki/Science , https://kenshi.fandom.com/wiki/Tech_tree : benches, tech level costs, Science formula, tree totals.
- The individual "(Tech)" pages of https://kenshi.fandom.com/wiki/Category:Technology (134 pages read): cost, tech level, requirements and unlocks of each research; also https://kenshi.fandom.com/wiki/Core_Tech , /Industry_Tech , /Electrics_Tech , /Farming_Tech , /Smithing_Tech , /Crafting_Tech , /Defense_Tech , /Training_Tech .
- https://kenshi.fandom.com/wiki/Crafting , https://kenshi.fandom.com/wiki/Clothing_Bench , https://kenshi.fandom.com/wiki/Weapon_Smithing_Bench , https://kenshi.fandom.com/wiki/Weapon_Smith , https://kenshi.fandom.com/wiki/Armour_Smith , https://kenshi.fandom.com/wiki/Leather_Armour_Crafting_Bench , https://kenshi.fandom.com/wiki/Leather_Tanning_Bench , https://kenshi.fandom.com/wiki/Plate_Beating_Station , https://kenshi.fandom.com/wiki/Heavy_Armour_Smithy , https://kenshi.fandom.com/wiki/Medical_Workbench , https://kenshi.fandom.com/wiki/Arrow_Making_Bench , https://kenshi.fandom.com/wiki/Crossbow_Crafting_Bench , https://kenshi.fandom.com/wiki/Electrical_Workbench , https://kenshi.fandom.com/wiki/Fabrics , https://kenshi.fandom.com/wiki/Bandana , https://kenshi.fandom.com/wiki/Item_Furnace : stations, recipes, grades by skill.
- https://kenshi.fandom.com/wiki/Stone_Mine , https://kenshi.fandom.com/wiki/Stone_Processor , https://kenshi.fandom.com/wiki/Iron_Refinery , https://kenshi.fandom.com/wiki/Manual_Iron_Refinery , https://kenshi.fandom.com/wiki/Steel_Refinery , https://kenshi.fandom.com/wiki/Ore_Drill , https://kenshi.fandom.com/wiki/Industry_Buildings : industry machines.
- https://kenshi.fandom.com/wiki/Player-Owned_Buildings_in_Town , https://kenshi.fandom.com/wiki/Construction , https://kenshi.fandom.com/wiki/Guide_to_Building_an_Outpost , https://kenshi.fandom.com/wiki/Getting_Started , https://kenshi.fandom.com/wiki/The_Hub , https://kenshi.fandom.com/wiki/Small_Shack , https://kenshi.fandom.com/wiki/Storm_House , https://kenshi.fandom.com/wiki/Longhouse , https://kenshi.fandom.com/wiki/Bughouse , https://kenshi.fandom.com/wiki/Watchtower , https://kenshi.fandom.com/wiki/Buildings_List , https://kenshi.fandom.com/wiki/Camping , https://kenshi.fandom.com/wiki/Prospecting , https://kenshi.fandom.com/wiki/Town_size_vs_map_icon_-_Town_Level_Icons , https://kenshi.fandom.com/wiki/Engineer : buying, repairing, build mode, shells, outposts, levels, sites.
- https://kenshi.fandom.com/wiki/Power , https://kenshi.fandom.com/wiki/Wind_Generator , https://kenshi.fandom.com/wiki/Small_Wind_Generator , https://kenshi.fandom.com/wiki/Small_Generator , https://kenshi.fandom.com/wiki/Generator_II , https://kenshi.fandom.com/wiki/Battery_Bank , https://kenshi.fandom.com/wiki/Fuel , https://kenshi.fandom.com/wiki/Biofuel_Distillery , https://kenshi.fandom.com/wiki/Lighting : power and light.
- https://kenshi.fandom.com/wiki/Farming and the farm pages (Wheat, Vegetable, Cactus, Riceweed, Hemp, Cotton), https://kenshi.fandom.com/wiki/Hydroponics , https://kenshi.fandom.com/wiki/Well , https://kenshi.fandom.com/wiki/Rain_Collector , https://kenshi.fandom.com/wiki/Water_Tank , https://kenshi.fandom.com/wiki/Cooking_Stove , https://kenshi.fandom.com/wiki/Cooking , https://kenshi.fandom.com/wiki/Bread_Oven , https://kenshi.fandom.com/wiki/Grain_Silo , https://kenshi.fandom.com/wiki/Food_Store , https://kenshi.fandom.com/wiki/Bread_Basket , https://kenshi.fandom.com/wiki/Animal_Feeder : farming, water, cooking, feeding.
- https://kenshi.fandom.com/wiki/Storage , https://kenshi.fandom.com/wiki/Jobs , https://kenshi.fandom.com/wiki/Storage:_Copper : storage and jobs.
- https://kenshi.fandom.com/wiki/Events and the event pages (Tax Man Visit, Tax Collector, Tax Evasion Enforcement, Prayer Day, Tribute Round, Bandit Demands, Bandit Rage, Traders Guild Visit, Hound's Welcome, Stone Rat Visit, Bandit Raid, Raid, Shek Proving, Cannibal Raid, Scrawny Raid, Slave Raid, Blooded Raid, Ninja Raid, Red Sabre Raid, Caravan Visit, Materials Trader, Farm Trader, Beast Trader, Drug Bust): triggers, ranges, squads, demands, base attacks, mercenary prices.
- https://kenshi.fandom.com/wiki/Defensive_Walls , https://kenshi.fandom.com/wiki/Defensive_Gates , https://kenshi.fandom.com/wiki/Turrets , https://kenshi.fandom.com/wiki/Mounted_Crossbow , https://kenshi.fandom.com/wiki/Harpoon_Turret , https://kenshi.fandom.com/wiki/Training_Dummy , https://kenshi.fandom.com/wiki/Locksmith_Training_Box , https://kenshi.fandom.com/wiki/Thief_Training_Boxes , https://kenshi.fandom.com/wiki/Prisoner_Cage : defence, training, cages.
- docs/game/buildings-production.md in https://github.com/VlcekM/meitouclient (notes on the original game's data and code): research time formula and bench rates, cost items read from bench inventories, production and mining rate formula, ore rock data, power figures, build-speed formula, placement messages, house price formula, farm water and harvest formula, zones needing to be loaded, on-screen status strings.
- docs/game/economy.md in https://github.com/VlcekM/meitouclient : animal purchase price, bounty payout on caging.
- docs/game/ui-screens.md in https://github.com/VlcekM/meitouclient : "For sale:" button and purchase confirmation text.
- https://kenshi.zone/en/item-copper (seen only as a web-search summary): copper mining rate cross-check.
- Turret reload times merged in from Combat and the Prayer Day end condition from Factions rest on the sources listed in those files.
