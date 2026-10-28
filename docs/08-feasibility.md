---
doc_id: WSL-FEA-001
title: WellSling feasibility assessment
project: WellSling
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.9.1 upgrade), closed for the chosen design at P3
---

# WellSling feasibility assessment

WellSling is feasible on paper: the frame, winch, rigging and bridge work with every steel part at a factor of 3 or more and every made part can be cut, drilled and welded in a village workshop. Its feasibility now rests on four things paper cannot settle: whether a 600 kg animal tolerates the bands for about half an hour, whether the passer can be steered under a lying animal 15 m down, the soil and rim at real wells, and the handle force of the winch actually bought. Method: STANDARDS section 23.

> **Safety:** Feasibility on paper is not fitness for use. The kit is not used on an animal before a proof-load test at 1.5 times the hook load.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Statics, strength, stability and clearances all close on paper; four details that failed in kit 1.7 are fixed (leg tube, chain eyes, winch bolts, band eyes) | High | Margins are screening factors, not a certified rating; the passer and band questions remain | WSL-STM-001; WSL-CAL-001 v0.2 |
| Materials | Common structural tube, box section, plate, hardwood and exterior plywood; galvanised | High | Tube must be structural (310 MPa), not water pipe; the mill certificate is checked | WSL-CAL-001 assumption 11; BOM lines 1, 2 |
| Manufacturing and assembly | Every made part is cut, drilled, bent or welded from stock; every bolted and pinned joint is modelled with its holes and fasteners and checked for interference at D3 | High | Galvanising needs a plant within reach; drilling lug pairs together keeps the pins true | WSL-BLD-001; `cad/fidelity.json` |
| Power and controls | Human power only: a crank at up to 200 N, about 94 W near the top, crew taking turns; an automatic load-pressure brake | Medium | The crank force rests on a catalogue-class handle force of 230 N at the rated load; confirm on the winch bought | WSL-CAL-001 B6; STEM S6 |
| Supply of parts | Winch, rope, shackles, chain, slings and harnesses are catalogue items | Medium | A spur-gear winch with a load-pressure brake and a 240 mm two-ply sling with eyes for a 25 mm bar must be found locally; one cooperative buying for several villages helps | BOM lines 9, 18; MKT |
| Animal handling | Two plain 240 mm bands under chest and flank, about 17 to 21 kPa, about 30 minutes in the bands | Low | No cited tolerance for cattle; needs a veterinary partner before any live lift | WSL-STM-001 S25; WSL-DEC-001 item 5 |
| Site conditions | Pads 700 mm and bearers 400 mm back from a 3 m rim; 75 kPa ground assumed | Medium | Soft, wet or undercut rims; a site check is a safety stop | WSL-STM-001 S14, S15; WSL-BLD-001 |
| Passing the bands | A 16 m sectioned pole with a J-head and a messenger line | Low | The push the pole can give 15 m down and the force to slide under an animal in mud are not known | WSL-STM-001 S26 |

Ratings: High, Medium, Low.
