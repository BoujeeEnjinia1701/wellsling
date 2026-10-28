---
doc_id: WSL-DEC-001
title: WellSling design decisions register
project: WellSling
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; all decisions made under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-10-25'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade. Seven fixes decided under Amish's standing instruction of 2026-10-23 (D10 to D14, D17 and D18, WSL-DDR-004); concept selection and a graft from option B proposed, awaiting Amish (D15, D16, WSL-DDR-003); items to confirm and value engineering updated
- version: "0.3"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Amish's decisions of 2026-10-25 (\"i approve of your recommendations\"): D15 option A and D16 option (a) moved to Decisions made (WSL-DDR-003 accepted); no open decisions in the register"
---

# WellSling design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several entries below set safety limits (rating, proof load, set-back from the rim, harnesses, no swinging over the rim). Each takes the conservative option and names the evidence that would relax it. Nobody goes down a well with this kit, and it is not used on an animal before a proof-load test.

## Open decisions

None. D15 (concept, option A) and D16 (keep the adjusting chains, option (a)) were decided by Amish on 2026-10-25 and are under Decisions made. Two questions without a recommendation stay with Amish in `docs/REVIEW.md`: his review of the fixes D10 to D14, D17 and D18, and the reviewer's scope question on animals over 600 kg.

## To confirm when parts are bought

These are facts that can only be settled with real parts, a real site or a veterinary partner. None changes a decision; each may change a size or a limit.

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Hand winch: rated 1,000 kg on the first layer with a load-pressure brake; handle force at rated load (230 N assumed); base bolt pattern (160 mm square assumed); drum width and flange size | Crank force 200 N and 87 % utilisation on layer 3 rest on these; the bracket holes follow the base (D12) | WSL-CAL-001, section 3; WSL-STM-001 S6 |
| 2 | Leg tube: mill certificate showing yield of 310 MPa or more and a 3.2 mm wall on 88.9 mm | Leg 1 bending factor 3.7 with an initial bow and buckling factor 7.3 (D10) | WSL-CAL-001, section 4 |
| 3 | Sheave: 200 mm pitch for 8 mm rope, 30 mm wide, 25 mm bore | Hanger spacing and the rope's line beside leg 1 | BOM line 3 |
| 4 | Ground bearing and friction at the first trial site (75 kPa and 0.4 assumed) | Pad size and the need for spread chains | WSL-DDR-002, A1 |
| 5 | Veterinary view on band width, pressure (about 17 to 21 kPa average), share between chest and flank bands (60 % assumed) and how long an animal may hang | Band width, felt thickness and the lift time of about 30 minutes | WSL-CAL-001, section 6; WSL-STM-001 S25 |
| 6 | Webbing sling: 240 mm two-ply with flat sewn eyes long enough to pass over a 25 mm bar, no insert, 8 t vertical working load limit | The plain-webbing design-around, the band factor and the yoke fit (D13) | BOM lines 18 and 29 |
| 7 | Deck panel mass with real plywood and battens (32.0 kg modelled) | The 35 kg carry limit, PR-013 | WSL-CAL-001, G1 |
| 8 | Typical well diameters, rim condition and depths in the first partner's area | The 3 m span and 15 m depth design case | WSL-PRS-001, PR-004 and PR-005 |
| 9 | Force needed to slide the J-head under a lying animal in mud, and what the passer pole can push 15 m down | Whether the passer works as drawn or needs stiffer lower sections | WSL-STM-001 S26 |

## Value engineering

Value-engineering target: USD 1,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 3,093 (USD 1,593 over the target; the kit 1.9.1 fixes added USD 89). The target was set when the kit was to borrow the HatchSide tripod and winch; the kit now carries its own tripod, winch and landing bridge (WSL-DDR-001, D1 and D5). Main cost drivers and savings worth trying:

- The largest lines are the hand winch (USD 380), the sixteen passer pole sections (USD 288), the bridge runners and deck panels (USD 420 together), the two harnesses (USD 220), the three legs (USD 204), the spread chains (USD 153), the two bands (USD 150), the head (USD 140) and the four band end yokes (USD 80).
- Savings worth trying: one passer pole of eight sections and a shorter retrieval pole for shallow wells (about USD 100); bamboo or timber runners for wells under 2 m (about USD 150, needs its own strength check); a cooperative buying winches and rigging for several villages at once; galvanising by weight in one batch with other kits.
- The tripod, winch and bridge are shared equipment: one kit per cluster of villages or per rescue van spreads the cost.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D9: own 600 kg tripod in place of HatchSide; wells up to 3 m in scope; two plain bands on an H-frame spreader; J-headed passer with a messenger line; animal landed on a slid-in bridge, never swung over the rim; spur-gear winch with load-pressure brake; 600 kg rating with proof at 1.5 times and a 10 deg lean limit; first co-design candidates (an animal rescue organisation in north India, a district dairy cooperative union in Haryana, a state veterinary university; none approached yet); harnesses for work near the rim; pitch, problem, design-arounds and budget unchanged | Amish, pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | WSL-DDR-001 |
| 2026-10-03 | Design for construction, changes C1 to C14: pinned legs with tongues, head weldment, offset sheave, winch bracket on leg 1, staked foot plates on pads, spread chains, H-frame spreader with sleeves and a five-hole lug, swivel hook and shackle, chain and shackle band ends, loose felt sleeves, sectioned passer, landing bridge, guide line eyes, galvanising | Amish, same pre-approval | WSL-DDR-002 |
| 2026-10-03 | Assumptions A1 to A5: 75 kPa ground and 0.4 friction (relaxed only by a site check); pads 650 mm and bearers 350 mm back from the rim (relaxed only by a survey of a sound lined rim); 10 deg lean limit; winch handle force 230 N to confirm; 60 % on one band to confirm with a veterinarian | Amish, same pre-approval | WSL-DDR-002 |
| 2026-10-03 | No use on an animal before a proof-load test at 1.5 times the hook load (conservative; this is a gate, not relaxed) | Amish, same pre-approval | WSL-BLD-001, section 6 |
| 2026-10-03 | Appearance model departures: a safe working load label on leg 1, ground, well ring, clay animal and mannequin drawn for the renders only | Amish, same pre-approval | docs/REVIEW.md, TRL 3 section |
| 2026-10-25 | D10: tripod legs 88.9 x 3.2 mm in place of 76.1 x 3.6 mm, after leg 1 missed its factor of 3 with an initial bow; sheave axle held by a head and a retaining ring so its end clears the larger leg | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | WSL-DDR-004; WSL-STM-001 S12 |
| 2026-10-25 | D11: two chain eye fins per foot, each square to its spread chain; spread chains with enlarged end links | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 S31 |
| 2026-10-25 | D12: winch bracket 300 x 300 mm; winch bolt pattern centred 140 mm to the side of leg 1 so all four bolts clear the tube | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 S32 |
| 2026-10-25 | D13: band end yokes (removable 25 mm bar through each band eye); adjusting chain in use 200 mm | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 S33 |
| 2026-10-25 | D14: option B's gantry beam in three sections (option model only) | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 B4 |
| 2026-10-25 | D17: spreader guide line eyes moved from the beam top to the end caps, clear of the 500 mm sleeves and bolts; lift lug 110 mm tall (was 120) with its holes 30 mm below the top edge, so the swivel hook clears the lug with the catalogue 3.25 t shackle | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 S35 |
| 2026-10-25 | D18: the winch is bought statically tested by its maker to 1.5 times its rated load, and the kit's proof load is held on the brake, after the independent review found the 1.5 times proof exceeds the winch's working rating on the third layer | Decided under the same standing instruction | WSL-DDR-004; WSL-STM-001 S38 |
| 2026-10-25 | D15: concept carried forward, option A (tripod and hand winch, 224 of 265; B 198, C 177); `concept_chosen: A` | Amish, 2026-10-25 12:43 CT: "i approve of your recommendations" | WSL-DDR-003; WSL-OPT-001 |
| 2026-10-25 | D16: option (a), keep the adjusting chains, set before the lift; the TRL 4 dummy trials (build plan checks 7 and 8) record whether the animal hangs nose or tail down, and only then is option (b), a 0.75 t lever hoist in place of one band's two adjusting chains, tried. No change to the design or BOM | Amish, as above | WSL-DDR-003 |
