---
doc_id: WSL-DDR-002
title: WellSling design for construction
project: WellSling
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Concept made constructable; changes C1 to C14 and assumptions A1 to A5 decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Design-for-construction rule, Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible."

## Context

The TRL 2 concept (WSL-DDR-001) named the parts but not how each is made or joined: legs "anchored", a "spreader bar", "rim pads", a "passer pole". STANDARDS section 18 requires every part to be makeable by a stated process and to fit and fasten to its neighbours. The parametric model (`cad/src/model.py`) was rebuilt part by part, and its 73 constructability checks (contact, clearance, landing, rope fall, rim distance and spreader swing) all pass. None of the changes alters what the kit does, its pitch or its safety case; each is the simplest physically sound way to make a concept part.

## Changes

*Table 1. Changes from the concept to the constructable design.*

| # | Concept | Constructable design | Why |
| --- | --- | --- | --- |
| C1 | Tripod legs, joint not defined | 76.1 x 3.6 mm tube with welded 8 mm end caps and 16 mm tongues; 20 mm clevis pins at both ends | A pinned leg carries only compression, folds flat for transport and needs no threads under load |
| C2 | Tripod head | 440 x 12 mm disc with three pairs of 10 mm lugs, 17 mm apart, and two sheave hangers | One profile-cut weldment; lug pairs give double shear on every pin |
| C3 | Rope over the head | 200 mm sheave hung 80 mm to the side of leg 1 and 179 mm out, so the rope from the winch runs parallel to leg 1, 121 mm outside its axis, and drops 112 mm off the well axis | The rope clears the leg and the head, and the drop stays near the axis; the leg bending this causes is checked (CAL C6) |
| C4 | Winch "on the tripod" | 300 x 240 x 10 mm bracket welded on the outer face of leg 1, 900 mm up from the foot pin; winch on four M12 bolts | A crank height a standing person can turn; welded before galvanising |
| C5 | Leg anchors | Foot plate with a lug pair and a chain eye, on a 600 x 300 x 50 mm hardwood pad, held by two 25 mm stakes through both | Spreads 2.5 kN to 15 kPa on soft ground and stops the foot walking |
| C6 | None | Three 8 mm grade 80 spread chains between the feet | The leg thrust is 0.59 of the vertical load, above a 0.4 friction on wet soil; without the chains the feet slide out |
| C7 | Spreader bar | H-frame: RHS 100 x 50 x 4 mm beam with six sleeves and a five-hole lift lug; two SHS 50 x 50 x 3 mm cross bars on M16 bolts through the sleeves; tip lugs | Sleeves stop the bolts crushing the box section; the five holes let the crew balance the animal fore and aft; cross bar spacing can be moved for a calf |
| C8 | Hook to spreader | Latched swivel hook and a 3.25 t bow shackle through the lug | Lets the spreader turn without twisting the rope; the swing clears the legs by 100 mm or more |
| C9 | Band clipped to the bar | 1 t shackle in each tip lug, 1 m adjusting chain, 1 t shackle through the band's flat sewn eye | Band height set to the animal; no hardware sewn into the band (design-around kept) |
| C10 | Padding | Loose felt sleeve in a canvas cover that slides on the band | Padding with no stiffness (design-around kept) |
| C11 | Passer pole | 2 m aluminium sections with riveted spigots and button locks; steel J-head with a line eye; separate retrieval hook head; 8 mm messenger line | Carried in short lengths, made up to 16 m; the J goes under the animal without catching |
| C12 | Swing to firm ground | Landing bridge: two hardwood rim bearers, three RHS 100 x 50 x 3 mm runners 4.5 m long, three plywood deck panels with cleats | Every piece two people can carry (31.6 kg at most); the cleats keep the deck on the runners |
| C13 | Guide lines tied on | Two 60 x 60 x 10 mm eyes on the beam ends | A fixed point that cannot slip along the beam |
| C14 | Finish | Hot-dip galvanising with vent holes in every closed section | Kept outdoors by wells for years |

## Assumptions decided with the changes

- **A1.** Ground bearing 75 kPa under a pad, friction 0.4 on wet soil (conservative; relaxed by a plate-load or simple penetrometer check at a real site).
- **A2.** Pads at least 650 mm and bearers at least 350 mm back from the rim of a 3 m well (conservative; relaxed only by a survey of a lined well with a sound rim).
- **A3.** Hook line lean limited to 10 deg; guide lines are for steadying, not pulling.
- **A4.** Winch handle force 230 N at rated load (catalogue class); to confirm on the winch bought.
- **A5.** 60 % of the animal on the more loaded band; to confirm with the veterinary partner.

## Consequences

- Model, STEP and STL regenerated; general arrangement WSL-DWG-001 at Rev P1; making sketches WSL-DWG-101 to 115; build plan WSL-BLD-001.
- `design_state: constructable` set in `project.yaml`.
- The BOM has 28 priced lines; estimated cost USD 3,004 against the USD 1,500 value-engineering target.
