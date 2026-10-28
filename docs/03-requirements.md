---
doc_id: WSL-PRS-001
title: WellSling product requirements and specifications
project: WellSling
doc_type: Product requirements and specifications
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Replaces WSL-REQ-001 v0.2 (kit 1.9.1 upgrade). R1 to R13 migrated to PR-001 to PR-013 with the same targets and verification, tolerance, units and traced user requirements added; PR-014 to PR-017 added from the constraints and settled questions; status from WSL-CAL-001 v0.2
---

# WellSling product requirements and specifications

What the design must do, each traced to a user need in WSL-URS-001. Fourteen of the seventeen requirements are met on paper or by design. PR-006 (setup in 20 minutes) is at risk: the estimate meets the target with no margin. PR-009 is reported against the value-engineering target, which the constructable design exceeds by USD 1,593. PR-008 (operation after a short briefing) can only be shown in a user trial. Results come from WSL-CAL-001 v0.2; tags in square brackets point to its sections. Targets are proposals for review with a co-design partner. Method: STANDARDS section 22.

> **Safety:** WellSling lifts a heavy, frightened animal over an open well. Nobody goes down the well at any stage. The kit is an open engineering reference, not certified lifting or rescue equipment, and it must be proof-loaded before any use (TRL 4).

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Safety | No entry | Bands shall be passed, rigged, lifted and landed entirely from the rim | 0 | max | people below the rim | Inspection of the method (BLD-001), TRL 3; trial with a weighted dummy in a test pit, TRL 4 | Met by design | R1 |
| PR-002 | UR-002, UR-011 | Performance | Lifting capacity | The kit shall lift the design animal with the hook line leaning up to 10 deg, every steel part at a factor of 3 on yield and buckling and the rope at 5, and shall be proof-loaded to 1.5 times | 600 (662 at the hook) | min | kg | Analysis [A2, B1, B10, C5, C6], TRL 3; proof-load test, TRL 4 | Met on paper (static; the dynamic load of a kicking animal to measure at TRL 4) | R2 |
| PR-003 | UR-008 | Performance | Band spreads the load | Each band shall be at least 200 mm wide, bear on a straight bar at its eyes, and the average pressure on the animal shall be stated | 200 | min | mm width | Analysis [E6, E7], TRL 3; design review with a veterinary partner, TRL 4 | Met on paper for width: two 240 mm bands, about 17 to 21 kPa; tolerance to verify at TRL 4 | R3 |
| PR-004 | UR-003 | Performance | Passer reach | The passer shall reach an animal 15 m below the rim | 15 | min | m | Analysis [G3], TRL 3; trial in a test pit, TRL 4 | Met on paper: 16.5 m | R4 |
| PR-005 | UR-004 | Physical architecture | Well span | The kit shall straddle wells up to 3 m across with every pad at least 650 mm and every bearer at least 350 mm back from the rim | 3.0 | min | m | Analysis [C9, F4], TRL 3; fit check on sample wells, TRL 4 | Met: pads 700 mm, bearers 400 mm back | R5 |
| PR-006 | UR-005 | Usability | Fast setup | Three people shall have the kit ready to lift within 20 minutes of arrival | 20 | max | min | Analysis [G4], TRL 3; timed drill, TRL 4 | At risk: 20 min estimate with no margin | R6 |
| PR-007 | UR-007 | Safety | Controlled lift | The winch brake shall hold the load at any point when the handle is released | 100 | min | % of hook load held | Inspection of the winch specified, TRL 3; brake hold test at proof load, TRL 4 | Met by selection of a load-pressure brake | R7 |
| PR-008 | UR-006 | Usability | Simple operation | First-time operators shall complete a lift after a briefing | 15 | max | min of briefing | User trial with first-time operators, TRL 4 | To verify at TRL 4 | R8 |
| PR-009 | UR-014 | Cost | Value-engineering target | The whole kit shall be costed against the value-engineering target, a hypothetical control target and not a limit | 1,500 | target | USD | Costed BOM [G2], TRL 3 | Over target: USD 3,093, USD 1,593 over | R9 |
| PR-010 | UR-011 | Safety | Tripod stability | No foot shall lift with the hook line leaning 10 deg in any direction | 10 | min | deg | Analysis [C3, C4], TRL 3; lean test at proof load, TRL 4 | Met on paper: tips only at 19.4 deg | R10 |
| PR-011 | UR-010 | Usability | Hand effort | Crank force shall stay at or below the target throughout the lift | 250 | max | N | Analysis [B6], TRL 3; force gauge on the handle, TRL 4 | Met on paper: 200 N at most, on an assumed handle force | R11 |
| PR-012 | UR-009 | Physical architecture | Landing clearance | Hooves shall be at least 150 mm above the deck at the landing height so the bridge slides under | 150 | min | mm | Analysis [F5], TRL 3; fit check with a dummy, TRL 4 | Met on paper: 169 mm | R12 |
| PR-013 | UR-013 | Packaging and transport | Carry weight | No single piece shall be heavier than two people can carry | 35 | max | kg | Analysis [G1], TRL 3; weigh the parts, TRL 4 | Met on paper: 32.0 kg | R13 |
| PR-014 | UR-012 | Safety | Rim restraint | Anyone within 1 m of the rim shall wear a harness on a work-restraint lanyard tied to a foot and set so the wearer cannot reach the edge | 1.0 | min | m from the rim | Inspection of the kit and method (BOM line 28, BLD-001), TRL 3; drill, TRL 4 | Met by design | |
| PR-015 | UR-015 | Materials | Outdoor life | Every steel part shall be hot-dip galvanised after welding, with vent holes in closed sections | 70 | min | um mean zinc on 3 to 6 mm steel | Inspection of the BOM and analysis (STEM S28), TRL 3; coating gauge, TRL 4 | Met by design | |
| PR-016 | UR-016 | Materials | Local making | Every made part shall be cut, drilled, bent or welded from plate, tube, box section, bar or timber with workshop tools | 100 | min | % of made parts | Inspection of the drawings and build plan (BLD-001), TRL 3 | Met by design | |
| PR-017 | UR-017 | Physical architecture | Design-arounds | The bands shall be plain webbing with no stiffening insert, and the passer a separate tool never fixed to a band | 0 | max | stiffening inserts | Inspection of the BOM (lines 18 to 22), TRL 3 | Met by design | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The design animal is 600 kg, the upper end of a grown cow or buffalo; a heavier animal is outside the rating.
- The ground around the well bears at least 75 kPa under a timber pad; a softer site needs larger pads.
- A plain webbing band with a loose felt sleeve can lift a large animal for the length of a lift without injury when two bands share the load. This is to be confirmed with a veterinary partner.
- Most open wells where animals fall are 3 m across or less.
- A village or cooperative keeps the kit in one known place and practises with it.
