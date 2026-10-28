---
doc_id: WSL-CAL-001
title: WellSling sizing calculations
project: WellSling
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue at TRL 3, on the constructable design of WSL-DDR-002
- version: "0.2"
  date: '2026-10-25'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade. Leg 1 checked with an initial bow of L/200 and secant amplification (C6), legs now 88.9 x 3.2 mm (WSL-DEC-001 D10); band end yokes added below the chains (E7, D13); after the independent review, lift taken as the 18.2 m of rope wound in (B8, B9), foot pressure with the 10 deg lean (C10), spread chain line (C11), pin bending (D1) and the winch bracket (D4) added; rigging, hook load and every result rerun on the detailed D3 model; requirement tags now name the product requirements (PR) of WSL-PRS-001 with the old R numbers
---

# WellSling sizing calculations

On paper, the constructable WellSling kit lifts a 600 kg animal 15 m up a 3 m well and lands it on the bridge deck with every main part at a safety factor of 3 or more, and the rope at 6.0. The two weak points are the effort and time of a long hand lift (about 30 minutes of cranking at up to 200 N) and the cost, which is USD 1,593 over the value-engineering target. Every figure below comes from `docs/04-calcs/sizing.py`, which imports the parametric model (`cad/src/model.py`), so the sizes here are the sizes in the STEP file, the drawings and the build plan. Tags in square brackets ([A1], [C5] ...) match the script output and `results.csv`.

These are first-principles screening estimates for a paper proof of concept. They do not replace a proof-load test of the real tripod, winch, rope and rigging, which is TRL 4 work.

> **Safety:** WellSling lifts a heavy, frightened animal over an open well. These numbers are for a design review only. The kit is not certified lifting or rescue equipment, nobody goes down the well at any stage, and nobody stands under the load or inside the tripod legs while it is raised.

## 1. Assumptions

*Table 1. Assumptions.*

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| 1 | Design animal | 600 kg (upper end of a grown cow or buffalo, 400 to 600 kg) | WSL-PRB-001 |
| 2 | Deepest lift | Animal 15 m below the rim | WSL-PRS-001, PR-004 (was R4) |
| 3 | Widest well | 3.0 m across | WSL-PRS-001, PR-005 (was R5) |
| 4 | Load factor for proof | 1.5 times the safe working load | WSL-PRS-001, PR-002 (was R2) |
| 5 | Required factors | 3 on yield and buckling for steel parts, 5 on the rope's minimum breaking load, 18 for sheave D/d | Common lifting practice, used as screening targets |
| 5a | Initial bow of a strut | L/200 for a cold-formed hollow section (buckling curve c), elastic analysis | EN 1993-1-1, Table 5.1 (added in v0.2 after the STEM check, S12) |
| 6 | Hook line lean | Up to 10 deg from vertical from guide-line pull and swing | Judgement, conservative for a slow hand lift |
| 7 | Share of the animal on the more loaded band | 60 % (cattle carry their weight forward) | Judgement; to confirm with a veterinary partner |
| 8 | Sheave efficiency | 97 % (bronze bushed) | Catalogue class |
| 9 | Winch | Rated 1,000 kg on the first layer, 230 N at the handle at rated load, gear and brake efficiency 80 % | Catalogue class of a spur-gear hand winch with a load-pressure brake; confirm on the winch bought |
| 10 | Rope | 8 mm 6 x 19 IWRC, grade 1770, minimum breaking load 40 kN, 0.25 kg/m | Catalogue class |
| 11 | Leg steel | Tube 88.9 x 3.2 mm, yield 310 MPa (IS 4923 YSt 310 or EN 10219 S355J2H); plates S355 or S275 | BOM lines 1 and 2 |
| 12 | Ground | 75 kPa allowable bearing on soft wet ground; friction 0.4 between timber and wet soil | Conservative judgement; a firm site relaxes it |
| 13 | Landing | 1.25 times the animal weight on the deck as it settles | Judgement for a slow, braked lowering |
| 14 | Crank speed | 15 rpm sustained, crew taking turns | Judgement |
| 15 | Plywood | 25 MPa characteristic bending strength | Exterior plywood class |

## 2. Loads

- [A1] Design animal 600 kg; rigging below the hook (hook, shackles, spreader, cross bars, bolts, chains, band end yokes, bands and sleeves) 57.0 kg; rope hanging below the sheave up to 4.7 kg. The band end yokes (WSL-DEC-001 D13) add 13.3 kg and the full 1.0 m of each adjusting chain is now counted.
- [A2] Design hook load 662 kg, which is 6.49 kN at the safe working load. Proof load 1.5 times that, 9.74 kN.
- [A3] Rope tension at the winch while lifting, through a 97 % sheave: 6.69 kN.

## 3. Rope, sheave and winch

The rope, sheave and drum all have room to spare; the winch is the limiting bought part and runs at 87 % of its capacity on the third rope layer.

- [B1] Rope safety factor 6.0 on its 40 kN minimum breaking load (need 5).
- [B2] Sheave pitch diameter 200 mm on 8 mm rope: D/d 25 (need 18).
- [B3] Drum 100 mm across and 168 mm wide, 20 turns per layer: it holds 54.7 m in 6 layers inside the 220 mm flanges (need 25 m).
- [B4] With the animal at 15 m, 23.0 m of rope is out and 2.0 m is on the drum (first layer, about six turns). At the landing height 4.8 m is out and 20.2 m is on the drum (third layer).
- [B5] On the third layer the winch gives 7.69 kN against 6.69 kN needed: 87 % utilisation.
- [B6] Crank force, scaled from 230 N at rated load: 157 N as the lift starts and 200 N at the landing height (need at most 250 N).
- [B7] Gear ratio about 9.6 to 1; 35 mm of rope per crank turn on the first layer.
- [B8] Winding in 18.2 m of rope (the hook rises from 15 m down to the landing height; v0.1 used 17.6 m) at 15 rpm takes about 30 minutes. The crank does 152 kJ of work for 118 kJ of lift, about 94 W near the top: whoever cranks takes a turn of 2 to 3 minutes, and a crew of three averages about 31 W each.
- [B9] Energy flow: crank 152 kJ; winch gears and brake lose 30 kJ; the sheave loses 4 kJ; 118 kJ goes into raising the animal and rigging (`media/flow.png`).
- [B10] The drum's pitch diameter is 13.5 times the rope diameter, above the 12.5 that ISO 4308-1 gives for mechanism group M2 (a kit used rarely). The rope factor with a pressed ferrule eye at 90 % efficiency is 5.4 (need 5). The winch is bought statically tested by its maker to 1.5 times its rating: at the kit's proof load on the third layer the drum torque is 0.69 kN m, within that test's 0.80 kN m (WSL-DEC-001 D18).

## 4. Tripod

The tripod is stable and strong at the safe working load and at proof. It would tip only if the hook line leaned 19.4 deg, almost twice the 10 deg allowed. Version 0.1 checked the legs against the Euler load alone; version 0.2 adds the initial bow a real strut has (assumption 5a). With it the 76.1 x 3.6 mm tube of v0.1 reached a factor of only 2.98 on leg 1 (2.89 with the secant amplification of C6), so the legs are now 88.9 x 3.2 mm (WSL-DEC-001 D10).

- [C1] Legs 4.50 m pin to pin at 32.1 deg from vertical, feet on a 5.0 m circle; head plate top 4.00 m above ground.
- [C2] Leg compressions at the safe working load with the hook line vertical: leg 1 (the winch leg) 9.55 kN, legs 2 and 3 2.86 kN each. Leg 1 carries more because the rope pulls its head toward the winch; below the winch it carries 2.86 kN.
- [C3] With the hook line leaning 10 deg in the worst direction, the largest leg compression is 11.09 kN; the smallest in any direction is 1.42 kN, so no foot lifts.
- [C4] A leg first unloads (the tripod would begin to tip) at a lean of 19.4 deg in the worst direction.
- [C5] Leg tube 88.9 x 3.2 mm: area 862 mm², second moment 79.2 cm⁴; Euler load pin to pin 81.1 kN. Buckling factor 7.3 at the safe working load with the 10 deg lean (need 3), 4.9 at proof.
- [C6] Leg 1 also bends, because the rope runs 121 mm outside its axis: 0.81 kN m. With an initial bow of L/200 (22.5 mm), secant amplification of 1.20 on the rope's moment (taken as constant along the leg, which is conservative) and 1.16 on the bow, the peak stress is 83 MPa at the safe working load (factor 3.7 on 310 MPa, need 3) and 136 MPa at proof.
- [C7] Foot loads at the safe working load: 2.58 kN down and 1.52 kN outward at each foot.
- [C8] The outward thrust is 0.59 of the vertical load, more than the 0.4 friction of timber on wet soil, so the feet would slide without the spread chains. The chains carry 0.88 kN each at the safe working load and 1.31 kN at proof, against a 19.6 kN working load limit (factor 22). Each chain now shackles to a chain eye fin of its own, square to the chain (WSL-DEC-001 D11).
- [C9] Ground pressure under the most loaded pad: 15 kPa at the safe working load and 23 kPa at proof, against 75 kPa assumed (factor 5.0). The pads sit 700 mm back from the rim of a 3 m well.
- [C10] With the hook line leaning 10 deg in the worst direction the most loaded foot carries 3.79 kN down: 22 kPa under its pad at the safe working load and 33 kPa at proof, below the 40 kPa at the low end of soft clay (factor 1.8). A pad near the shaft has a smaller bearing wedge, so the site check stays a safety stop.
- [C11] Each spread chain runs 1.21 m from the well axis, so 1.77 m of it crosses the mouth of a 3 m well near its edge. Taut at the safe working load it sags about 34 mm; it stays clear of the animal, which hangs within about 0.7 m of the axis, and passes under the bridge runner ends. Anyone stepping over a chain near the rim wears a harness (WSL-BLD-001 safety stop S4).

## 5. Head, pins and sheave hangers

- [D1] Leg pins 20 mm in double shear: 18 MPa at the largest leg load (factor 22 on grade 8.8 shear yield) and 67 MPa in bending. Lug bearing 28 MPa and tongue bearing 35 MPa (factor 10 on S355). Each pin is held by an R-clip on a lanyard.
- [D2] Sheave axle load 12.67 kN. The two 120 x 10 mm hanger plates see 16 MPa from tension and the 3.55 kN side load at 125 mm (factor 22.3).
- [D3] Sheave axle 25 mm over a 46 mm span: 95 MPa bending (factor 3.7 on S355; a grade 8.8 pin gives 6.7). The axle is held by its head on the far side and a retaining ring on the leg 1 side, so its end clears the larger leg (WSL-DEC-001 D10).
- [D4] Winch bracket: the 6.69 kN rope pull acts 67 mm above the bracket face. Each M12 bolt sees 1.39 kN of tension and 1.67 kN of shear (grade 8.8 proof load about 48 kN), and the two 6 mm fillet welds 6 MPa. Every bolt and nut sits beside the tube, not over it (WSL-DEC-001 D12).

## 6. Spreader and bands

- [E1] Main beam RHS 100 x 50 x 4 mm: with 60 % of the animal on one band, 3.61 kN acts 450 mm from the lift lug, a moment of 1.62 kN m and a stress of 56 MPa (factor 6.3). Hung from the middle lug hole the beam would tilt until the hook line passes through the load's centre, 90 mm toward the chest; the shackle is moved to the hole 50 or 100 mm toward the heavier band to keep the animal level.
- [E2] Cross bar SHS 50 x 50 x 3 mm: 1.80 kN at each tip, 340 mm from the bolts, 74 MPa (factor 4.8).
- [E3] Lift lug 20 mm with a 22 mm hole 30 mm below its top edge (the lug is 110 mm tall so the hook clears it, WSL-DEC-001 D17): tear-out shear 8 MPa (factor 25); the 3.25 t shackle runs at 20 % of its working load limit.
- [E4] Each cross bar hangs on two M16 grade 8.8 bolts: 1.80 kN per bolt against a 113 kN proof load.
- [E5] Band leg tension 1.77 kN (180 kg) against an 8 t vertical working load limit for the sling; the 1 t shackles and 8 mm grade 80 chain run at 18 % and 9 % of theirs.
- [E6] Band pressure on the animal: 60 % of 600 kg over a 240 mm band in contact for 0.89 m is about 17 kPa on average (estimate); the belt formula, tension over band width times wrap radius, gives 21 kPa. Two bands halve the pressure one band would give. The tolerable pressure and duration for cattle need a veterinary view (WSL-DEC-001).
- [E7] Band end yokes (WSL-DEC-001 D13): each 240 mm sewn eye wraps a removable 25 mm bar 258 mm long between two side plates, so the webbing bears on a straight bar across its width, as the sling instructions to EN 1492-1 require for slings wider than 75 mm. The removable bar sees 43 MPa and the welded top bar under the lug 74 MPa (factor 4.8 on S355). The adjusting chain in use is now 200 mm, so the yoke does not lower the animal.

## 7. Landing bridge

- [F1] Runner RHS 100 x 50 x 3 mm over a 4.0 m span between bearers, animal standing with hooves 1.2 m apart, 40 % of it on one runner, times 1.25 for landing: 92 MPa (factor 3.9) and 15 mm deflection.
- [F2] Animal lying, its weight over 1.6 m of body at mid-span: 105 MPa (factor 3.4).
- [F3] Deck 25 mm plywood over 500 mm runner centres, one hoof (1.84 kN) at mid-span on a 300 mm strip: 7.4 MPa against about 25 MPa characteristic (factor 3.4). This ignores the hardwood cleat glued and screwed under the same line; with factors for wet service the bare plywood alone would be near a factor of 2, so the cleat is part of the deck's strength and must stay glued.
- [F4] Each rim bearer carries 4.59 kN: 16 kPa on the ground (factor 4.6), its near edge 400 mm back from the rim of a 3 m well.
- [F5] At the landing height the hooves are 169 mm above the deck (need 150), with 200 mm of adjusting chain; the deck top is 225 mm above the ground. The landing height is a winch position, not a fixed stop: 500 mm more rope can be wound in before the rope fall reaches its 300 mm minimum, which covers rope and band stretch.

## 8. Mass, cost, reach and setup

- [G1] The heaviest single piece is a deck panel with its cleats, 32.0 kg (need at most 35 kg); a tripod leg is 31.8 kg. The whole kit is about 555 kg including the lines and the passer, so it travels on a small trailer or pickup.
- [G2] Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 3,093 (USD 1,593 over the target). The target was set when the kit was to borrow the HatchSide tripod; the kit now carries its own 600 kg tripod, winch and landing bridge (WSL-DDR-001), and the kit 1.9.1 fixes add USD 89 (heavier legs, four band end yokes).
- [G3] Passer reach: eight 2 m sections and the J-head reach 16.5 m below the top hand (need 15 m). One made-up pole weighs 17.6 kg.
- [G4] Setup by three people, task by task (estimate): 20 minutes to the first lift, against 20 minutes. Passing the bands under the animal is extra and depends on how it lies.

## 9. Results against the requirements

*Table 2. Results against WSL-PRS-001 (old R numbers in brackets).*

| ID | Requirement | Target | Result | Status |
| --- | --- | --- | --- | --- |
| PR-001 (R1) | No entry | Everything done from the rim | Bands passed by pole and messenger line, rigged, lifted and landed from the rim | Met by design |
| PR-002 (R2) | Lifting capacity | 600 kg animal with off-centre load; proof 1.5 times | Rope factor 6.0, 5.4 with its eye [B1, B10]; legs 7.3 buckling, 3.7 bending with an initial bow [C5, C6]; winch 87 % [B5]; all steel parts factor 3.4 or more | Met on paper; dynamic load of a kicking animal to measure (STEM S36) |
| PR-003 (R3) | Band spreads the load | At least 200 mm wide | Two bands 240 mm wide; about 17 kPa average [E6], each eye on a straight 25 mm bar [E7] | Met on paper; pressure to confirm with a veterinarian |
| PR-004 (R4) | Passer reach | 15 m | 16.5 m [G3] | Met on paper |
| PR-005 (R5) | Well span | 3 m | Pads 700 mm and bearers 400 mm back from the rim [C9, F4] | Met |
| PR-006 (R6) | Fast setup | 20 min | 20 min estimate [G4], no margin | At risk |
| PR-007 (R7) | Controlled lift | Hold at any point | Load-pressure brake holds the load when the handle is released | Met by selection |
| PR-008 (R8) | Simple operation | 15-minute briefing | Not shown on paper | To verify in a user trial (TRL 4) |
| PR-009 (R9) | Value-engineering target | USD 1,500 | USD 3,093 [G2] | Over the value-engineering target by USD 1,593 |
| PR-010 (R10) | Tripod stability | No foot lifts at a 10 deg lean | Tips only at 19.4 deg [C4] | Met on paper |
| PR-011 (R11) | Hand effort | Crank force at most 250 N | 200 N at most [B6] | Met on paper (handle force of the winch bought to confirm) |
| PR-012 (R12) | Landing clearance | Hooves at least 150 mm above the deck | 169 mm [F5] | Met on paper |
| PR-013 (R13) | Carry weight | No piece over 35 kg | 32.0 kg [G1] | Met on paper |
| PR-014 | Rim restraint | Anyone within 1 m of the rim held back from the edge | Two harnesses on work-restraint lanyards tied to a foot (BOM line 28) | Met by design |
| PR-015 | Outdoor life | Steel parts galvanised; at least 70 um of zinc | Hot-dip galvanised to EN ISO 1461 (STEM S28) | Met by design |
| PR-016 | Local making | Made parts cut, drilled, bent and welded from stock | Every made part is plate, tube, box section, bar or timber (WSL-BLD-001) | Met by design |
| PR-017 | Design-arounds | Plain webbing bands with no insert; passer a separate tool | BOM lines 18 to 22 | Met by design |
