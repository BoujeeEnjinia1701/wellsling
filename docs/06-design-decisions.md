---
doc_id: WSL-DEC-001
title: WellSling design decisions register
project: WellSling
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; all decisions made under Amish's 2026-10-03 pre-approval
---

# WellSling design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several entries below set safety limits (rating, proof load, set-back from the rim, harnesses, no swinging over the rim). Each takes the conservative option and names the evidence that would relax it. Nobody goes down a well with this kit, and it is not used on an animal before a proof-load test.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

These are facts that can only be settled with real parts, a real site or a veterinary partner. None changes a decision; each may change a size or a limit.

*Table 1. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Hand winch: rated 1,000 kg on the first layer with a load-pressure brake; handle force at rated load (230 N assumed); base bolt pattern; drum width and flange size | Crank force 196 N and 85 % utilisation on layer 3 rest on these; the bracket holes follow the base | WSL-CAL-001, section 3; WSL-DDR-002, A4 |
| 2 | Leg tube: mill certificate showing yield of 310 MPa or more and a 3.6 mm wall | Leg 1 bending factor 3.7 and buckling factor 5.1 | WSL-CAL-001, section 4 |
| 3 | Sheave: 200 mm pitch for 8 mm rope, 30 mm wide, 25 mm bore | Hanger spacing and the rope's line beside leg 1 | BOM line 3 |
| 4 | Ground bearing and friction at the first trial site (75 kPa and 0.4 assumed) | Pad size and the need for spread chains | WSL-DDR-002, A1 |
| 5 | Veterinary view on band width, pressure (about 17 kPa average), share between chest and flank bands (60 % assumed) and how long an animal may hang | Band width, felt thickness and the lift time of about 29 minutes | WSL-CAL-001, section 6; WSL-DDR-002, A5 |
| 6 | Webbing sling: 240 mm two-ply with flat sewn eyes and no insert, 8 t vertical working load limit | The plain-webbing design-around and the band factor | BOM line 18 |
| 7 | Deck panel mass with real plywood and battens (31.6 kg modelled) | The 35 kg carry limit, R13 | WSL-CAL-001, G1 |
| 8 | Typical well diameters, rim condition and depths in the first partner's area | The 3 m span and 15 m depth design case | WSL-REQ-001, R4 and R5 |

## Value engineering

Value-engineering target: USD 1,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 3,004 (USD 1,504 over the target). The target was set when the kit was to borrow the HatchSide tripod and winch; the kit now carries its own tripod, winch and landing bridge (WSL-DDR-001, D1 and D5). Main cost drivers and savings worth trying:

- The largest lines are the hand winch (USD 380), the sixteen passer pole sections (USD 288), the bridge runners and deck panels (USD 420 together), the two harnesses (USD 220), the three legs (USD 195), the spread chains (USD 153), the two bands (USD 150) and the head (USD 140).
- Savings worth trying: one passer pole of eight sections and a shorter retrieval pole for shallow wells (about USD 100); bamboo or timber runners for wells under 2 m (about USD 150, needs its own strength check); a cooperative buying winches and rigging for several villages at once; galvanising by weight in one batch with other kits.
- The tripod, winch and bridge are shared equipment: one kit per cluster of villages or per rescue van spreads the cost.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D9: own 600 kg tripod in place of HatchSide; wells up to 3 m in scope; two plain bands on an H-frame spreader; J-headed passer with a messenger line; animal landed on a slid-in bridge, never swung over the rim; spur-gear winch with load-pressure brake; 600 kg rating with proof at 1.5 times and a 10 deg lean limit; first co-design candidates (an animal rescue organisation in north India, a district dairy cooperative union in Haryana, a state veterinary university; none approached yet); harnesses for work near the rim; pitch, problem, design-arounds and budget unchanged | Amish, pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | WSL-DDR-001 |
| 2026-10-03 | Design for construction, changes C1 to C14: pinned legs with tongues, head weldment, offset sheave, winch bracket on leg 1, staked foot plates on pads, spread chains, H-frame spreader with sleeves and a five-hole lug, swivel hook and shackle, chain and shackle band ends, loose felt sleeves, sectioned passer, landing bridge, guide line eyes, galvanising | Amish, same pre-approval | WSL-DDR-002 |
| 2026-10-03 | Assumptions A1 to A5: 75 kPa ground and 0.4 friction (relaxed only by a site check); pads 650 mm and bearers 350 mm back from the rim (relaxed only by a survey of a sound lined rim); 10 deg lean limit; winch handle force 230 N to confirm; 60 % on one band to confirm with a veterinarian | Amish, same pre-approval | WSL-DDR-002 |
| 2026-10-03 | No use on an animal before a proof-load test at 1.5 times the hook load (conservative; this is a gate, not relaxed) | Amish, same pre-approval | WSL-BLD-001, section 6 |
| 2026-10-03 | Appearance model departures: a safe working load label on leg 1, ground, well ring, clay animal and mannequin drawn for the renders only | Amish, same pre-approval | docs/REVIEW.md, TRL 3 section |
