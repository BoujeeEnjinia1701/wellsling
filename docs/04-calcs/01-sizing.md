---
doc_id: WSL-CAL-001
title: WellSling sizing calculations
project: WellSling
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue at TRL 3, on the constructable design of WSL-DDR-002
---

# WellSling sizing calculations

On paper, the constructable WellSling kit lifts a 600 kg animal 15 m up a 3 m well and lands it on the bridge deck with every main part at a safety factor of 3 or more, and the rope at 6.1. The two weak points are the effort and time of a long hand lift (about 29 minutes of cranking at up to 196 N) and the cost, which is USD 1,504 over the value-engineering target. Every figure below comes from `docs/04-calcs/sizing.py`, which imports the parametric model (`cad/src/model.py`), so the sizes here are the sizes in the STEP file, the drawings and the build plan. Tags in square brackets ([A1], [C5] ...) match the script output and `results.csv`.

These are first-principles screening estimates for a paper proof of concept. They do not replace a proof-load test of the real tripod, winch, rope and rigging, which is TRL 4 work.

> **Safety:** WellSling lifts a heavy, frightened animal over an open well. These numbers are for a design review only. The kit is not certified lifting or rescue equipment, nobody goes down the well at any stage, and nobody stands under the load or inside the tripod legs while it is raised.

## 1. Assumptions

*Table 1. Assumptions.*

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| 1 | Design animal | 600 kg (upper end of a grown cow or buffalo, 400 to 600 kg) | WSL-PRB-001 |
| 2 | Deepest lift | Animal 15 m below the rim | WSL-REQ-001, R4 |
| 3 | Widest well | 3.0 m across | WSL-REQ-001, R5 |
| 4 | Load factor for proof | 1.5 times the safe working load | WSL-REQ-001, R2 |
| 5 | Required factors | 3 on yield and buckling for steel parts, 5 on the rope's minimum breaking load, 18 for sheave D/d | Common lifting practice, used as screening targets |
| 6 | Hook line lean | Up to 10 deg from vertical from guide-line pull and swing | Judgement, conservative for a slow hand lift |
| 7 | Share of the animal on the more loaded band | 60 % (cattle carry their weight forward) | Judgement; to confirm with a veterinary partner |
| 8 | Sheave efficiency | 97 % (bronze bushed) | Catalogue class |
| 9 | Winch | Rated 1,000 kg on the first layer, 230 N at the handle at rated load, gear and brake efficiency 80 % | Catalogue class of a spur-gear hand winch with a load-pressure brake; confirm on the winch bought |
| 10 | Rope | 8 mm 6 x 19 IWRC, grade 1770, minimum breaking load 40 kN, 0.25 kg/m | Catalogue class |
| 11 | Leg steel | Yield 310 MPa (IS 4923 YSt 310 or EN 10219 S355J2H); plates S355 or S275 | BOM lines 1 and 2 |
| 12 | Ground | 75 kPa allowable bearing on soft wet ground; friction 0.4 between timber and wet soil | Conservative judgement; a firm site relaxes it |
| 13 | Landing | 1.25 times the animal weight on the deck as it settles | Judgement for a slow, braked lowering |
| 14 | Crank speed | 15 rpm sustained, crew taking turns | Judgement |
| 15 | Plywood | 25 MPa characteristic bending strength | Exterior plywood class |

## 2. Loads

- [A1] Design animal 600 kg; rigging below the hook (hook, shackles, spreader, chains, bands and sleeves) 42.8 kg; rope hanging below the sheave up to 4.7 kg.
- [A2] Design hook load 648 kg, which is 6.35 kN at the safe working load. Proof load 1.5 times that, 9.53 kN.
- [A3] Rope tension at the winch while lifting, through a 97 % sheave: 6.55 kN.

## 3. Rope, sheave and winch

The rope, sheave and drum all have room to spare; the winch is the limiting bought part and runs at 85 % of its capacity on the third rope layer.

- [B1] Rope safety factor 6.1 on its 40 kN minimum breaking load (need 5).
- [B2] Sheave pitch diameter 200 mm on 8 mm rope: D/d 25 (need 18).
- [B3] Drum 100 mm across and 168 mm wide, 20 turns per layer: it holds 54.7 m in 6 layers inside the 220 mm flanges (need 25 m).
- [B4] With the animal at 15 m, 23.0 m of rope is out and 2.0 m is on the drum (first layer). At the landing height 4.8 m is out and 20.2 m is on the drum (third layer).
- [B5] On the third layer the winch gives 7.69 kN against 6.55 kN needed: 85 % utilisation.
- [B6] Crank force, scaled from 230 N at rated load: 154 N as the lift starts and 196 N at the landing height (need at most 250 N).
- [B7] Gear ratio about 9.6 to 1; 35 mm of rope per crank turn on the first layer.
- [B8] Lifting 17.6 m (15 m deep to the landing height) at 15 rpm takes about 29 minutes. The crank does 144 kJ of work for 112 kJ of lift, about 92 W near the top, so the crew takes turns.
- [B9] Energy flow: crank 144 kJ; winch gears and brake lose 29 kJ; the sheave loses 3 kJ; 112 kJ goes into raising the animal and rigging (`media/flow.png`).

## 4. Tripod

The tripod is stable and strong at the safe working load and at proof. It would tip only if the hook line leaned 19.3 deg, almost twice the 10 deg allowed.

- [C1] Legs 4.50 m pin to pin at 32.1 deg from vertical, feet on a 5.0 m circle; head plate top 4.00 m above ground.
- [C2] Leg compressions at the safe working load with the hook line vertical: leg 1 (the winch leg) 9.34 kN, legs 2 and 3 2.79 kN each. Leg 1 carries more because the rope pulls its head toward the winch; below the winch it carries 2.79 kN.
- [C3] With the hook line leaning 10 deg in the worst direction, the largest leg compression is 10.85 kN; the smallest in any direction is 1.38 kN, so no foot lifts.
- [C4] A leg first unloads (the tripod would begin to tip) at a lean of 19.3 deg in the worst direction.
- [C5] Leg tube 76.1 x 3.6 mm: area 820 mm², second moment 54.0 cm⁴; Euler load pin to pin 55.3 kN. Buckling factor 5.1 at the safe working load with the 10 deg lean (need 3), 3.4 at proof.
- [C6] Leg 1 also bends, because the rope runs 121 mm outside its axis: 0.79 kN m, peak stress 83 MPa at the safe working load (factor 3.7 on 310 MPa, need 3) and 139 MPa at proof.
- [C7] Foot loads at the safe working load: 2.51 kN down and 1.48 kN outward at each foot.
- [C8] The outward thrust is 0.59 of the vertical load, more than the 0.4 friction of timber on wet soil, so the feet would slide without the spread chains. The chains carry 0.86 kN each at the safe working load and 1.28 kN at proof, against a 19.6 kN working load limit (factor 23).
- [C9] Ground pressure under the most loaded pad: 15 kPa at the safe working load and 22 kPa at proof, against 75 kPa assumed (factor 5.1). The pads sit 700 mm back from the rim of a 3 m well.

## 5. Head, pins and sheave hangers

- [D1] Leg pins 20 mm in double shear: 17 MPa at the largest leg load (factor 22 on grade 8.8 shear yield). Lug bearing 27 MPa and tongue bearing 34 MPa (factor 10 on S355).
- [D2] Sheave axle load 12.40 kN. The two 120 x 10 mm hanger plates see 16 MPa from tension and the 3.48 kN side load at 125 mm (factor 22.8).
- [D3] Sheave axle 25 mm over a 46 mm span: 93 MPa bending (factor 3.8 on S355; a grade 8.8 pin gives 6.9).

## 6. Spreader and bands

- [E1] Main beam RHS 100 x 50 x 4 mm: with 60 % of the animal on one band, 3.61 kN acts 450 mm from the lift lug, a moment of 1.62 kN m and a stress of 56 MPa (factor 6.3).
- [E2] Cross bar SHS 50 x 50 x 3 mm: 1.81 kN at each tip, 340 mm from the bolts, 74 MPa (factor 4.8).
- [E3] Lift lug 20 mm with a 22 mm hole 40 mm below its top edge: tear-out shear 5 MPa (factor 39); the 3.25 t shackle runs at 20 % of its working load limit.
- [E4] Each cross bar hangs on two M16 grade 8.8 bolts: 1.81 kN per bolt against a 113 kN proof load.
- [E5] Band leg tension 1.77 kN (180 kg) against an 8 t vertical working load limit for the sling; the 1 t shackles and 8 mm grade 80 chain run at 18 % and 9 % of theirs.
- [E6] Band pressure on the animal: 60 % of 600 kg over a 240 mm band in contact for 0.89 m is about 17 kPa on average (estimate). Two bands halve the pressure one band would give. The tolerable pressure and duration for cattle need a veterinary view (WSL-DEC-001).

## 7. Landing bridge

- [F1] Runner RHS 100 x 50 x 3 mm over a 4.0 m span between bearers, animal standing with hooves 1.2 m apart, 40 % of it on one runner, times 1.25 for landing: 92 MPa (factor 3.9) and 15 mm deflection.
- [F2] Animal lying, its weight over 1.6 m of body at mid-span: 105 MPa (factor 3.4).
- [F3] Deck 25 mm plywood over 500 mm runner centres, one hoof (1.84 kN) at mid-span on a 300 mm strip: 7.4 MPa against about 25 MPa (factor 3.4).
- [F4] Each rim bearer carries 4.60 kN: 16 kPa on the ground (factor 4.6), its near edge 400 mm back from the rim of a 3 m well.
- [F5] At the landing height the hooves are 162 mm above the deck (need 150), with 300 mm of adjusting chain; the deck top is 225 mm above the ground.

## 8. Mass, cost, reach and setup

- [G1] The heaviest single piece is a deck panel with its cleats, 31.6 kg (need at most 35 kg). The whole kit is about 550 kg including lines, harnesses and the passer, so it travels on a small trailer or pickup.
- [G2] Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 3,004 (USD 1,504 over the target). The target was set when the kit was to borrow the HatchSide tripod; the kit now carries its own 600 kg tripod, winch and landing bridge (WSL-DDR-001).
- [G3] Passer reach: eight 2 m sections and the J-head reach 16.5 m below the top hand (need 15 m). One made-up pole weighs 17.6 kg.
- [G4] Setup by three people, task by task (estimate): 20 minutes to the first lift, against 20 minutes. Passing the bands under the animal is extra and depends on how it lies.

## 9. Results against the requirements

*Table 2. Results against WSL-REQ-001.*

| ID | Requirement | Target | Result | Status |
| --- | --- | --- | --- | --- |
| R1 | No entry | Everything done from the rim | Bands passed by pole and messenger line, rigged, lifted and landed from the rim | Met by design |
| R2 | Lifting capacity | 600 kg animal with off-centre load; proof 1.5 times | Rope factor 6.1 [B1]; legs 5.1 buckling, 3.7 bending [C5, C6]; winch 85 % [B5]; all steel parts factor 3.4 or more at proof | Met on paper |
| R3 | Band spreads the load | At least 200 mm wide | Two bands 240 mm wide; about 17 kPa average [E6] | Met on paper; pressure to confirm with a veterinarian |
| R4 | Passer reach | 15 m | 16.5 m [G3] | Met on paper |
| R5 | Well span | 3 m | Pads 700 mm and bearers 400 mm back from the rim [C9, F4] | Met |
| R6 | Fast setup | 20 min | 20 min estimate [G4] | Met on paper, at the limit |
| R7 | Controlled lift | Hold at any point | Load-pressure brake holds the load when the handle is released | Met by selection |
| R8 | Simple operation | 15-minute briefing | Not shown on paper | To verify in a user trial (TRL 4) |
| R9 | Value-engineering target | USD 1,500 | USD 3,004 [G2] | Over the value-engineering target by USD 1,504 |
| R10 | Tripod stability | No foot lifts at a 10 deg lean | Tips only at 19.3 deg [C4] | Met on paper |
| R11 | Hand effort | Crank force at most 250 N | 196 N at most [B6] | Met on paper |
| R12 | Landing clearance | Hooves at least 150 mm above the deck | 162 mm [F5] | Met on paper |
| R13 | Carry weight | No piece over 35 kg | 31.6 kg [G1] | Met on paper |
