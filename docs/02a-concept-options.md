---
doc_id: WSL-OPT-001
title: WellSling concept options
project: WellSling
doc_type: Concept options
version: "0.2"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.9.1 upgrade). The design carried since kit 1.7 is option A; options B and C added with different working principles; all three modelled at D3 and scored against WSL-URS-001
- version: "0.2"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Amish chose option A and graft option (a) on 2026-10-25 (WSL-DEC-001 D15, D16)"
---

# WellSling concept options

Recommendation: option A, the tripod and hand winch carried since kit 1.7, scores 224 of 265 against 198 for option B (portable gantry and two chain hoists) and 177 for option C (sheerlegs and draught haul). B is 11.6 % behind A, just outside the 10 % band, so one option was recommended, and Amish chose it on 2026-10-25 (WSL-DEC-001 D15, WSL-DDR-003). Method: STANDARDS section 21.

![Concept options side by side at one scale](../media/options.png)

*Figure 1. The three options at one scale, rendered from the D3 models in `cad/src/model.py` (the Cycles picture is made by the coordinator with `.kit/options.py`).*

> **Safety:** Every option lifts a 600 kg animal over an open well and is worked from the rim; none is used before a proof-load test at 1.5 times the hook load. Option C puts a tractor on the rope and relies on a person holding the brake turns, which is its main safety weakness.

## The options

### Option A: Tripod and hand winch

A steel tripod of its own carries a sheave over the well; a braked hand winch on one leg raises two webbing bands on an H-frame spreader, and a bridge is slid under the animal to land it. Three 88.9 mm legs pinned to a head plate stand on staked foot plates and timber pads, tied by spread chains; the 8 mm rope runs from a 1,000 kg spur-gear winch with an automatic load-pressure brake up leg 1 and over a 200 mm sheave. Each band's two eyes hang on band end yokes, adjusting chains and shackles from the cross bars of the spreader. First-order numbers: hook load 662 kg, rope factor 6.0, winch at 87 % on its third layer, crank at most 200 N, about 30 minutes for a 15 m lift, tips only at 19.4 deg, heaviest piece 32.0 kg (WSL-CAL-001). Key risks: animal tolerance of the bands, passer push force, setup time at its limit. From a co-design partner it needs real wells, a test pit and a veterinarian.

### Option B: Portable gantry and chain hoists

A sectioned box beam on two pinned A-frames spans the well; one hand chain hoist per band lifts the chest and the flank on separate lines, and the same bridge is slid under to land it. The 5.8 m beam (RHS 140 x 80 x 4, three bolted sections) sits in saddles on A-frames of SHS 60 x 3 legs 2.7 m either side of the well, with knee braces to the beam. Each 1 t hoist hangs on a shackle under the beam and lifts a band bar (a cross bar with a top lug) carrying the same chains, yokes and bands as A. First-order numbers: beam factor 3.1, legs 39 on Euler, hand chain pull about 120 N per hoist (assumed), heaviest beam section 25.7 kg (after the fix D14), about 20 to 30 minutes with two operators. Its best feature: chest and flank are lifted separately, so the animal can be kept level. Key risks: thin beam margin, the beam lifted onto saddles at 3.3 m, two operators pulling hand chains over the well mouth, 15 m of load chain per hoist.

### Option C: Sheerlegs and draught haul

Two pinned legs lean over the well on a back guy; a tractor hauls the rope through a block at the apex and a snatch block at the feet, with turns on a snubbing post as the brake. The legs (CHS 88.9 x 3.2, 4.74 m) stand on staked feet 2.4 m from the well axis, tied by a chain; a 10 mm guy with a turnbuckle runs to a staked anchor plate 7 m back. The rope runs from the hook over the top block, down to a snatch block on its own staked anchor, three turns round a staked post and on to the tractor; the spreader, bands and bridge are A's. First-order numbers: guy tension 6.5 kN, leg factor 7.6 on Euler, about 400 N to hold the load on three turns, the lift itself about a minute at a tractor's creep speed. Key risks: the guy anchor's holding in soft ground, a jerk or missed stop from the tractor, no automatic brake, three anchors to set.

## First-order numbers

Table 1. Options compared. Parts and mass from `cad/fidelity.json` (every modelled part, including fasteners and welds; catalogue items such as the winch and rope drawn in part); costs are first-order estimates from the option A BOM rates, with the chain hoist price cited in WSL-MKT-001.

| Quantity | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Estimated parts cost (USD) | 3,093 (priced BOM) | About 3,400 (estimate, plus or minus 30 %) | About 3,000 (estimate, plus or minus 30 %) plus a tractor |
| Mass of the modelled kit (kg) | 522.0 | 654.4 | 552.8 |
| Parts in the D3 model | 351 (86 fasteners, 100 welds) | 427 (164 fasteners, 86 welds) | 312 (67 fasteners, 81 welds) |
| Output or throughput | 15 m lift in about 30 min | About 20 to 30 min (estimate) | About 1 min of haul once rigged |
| Energy or effort | 152 kJ at the crank, up to 200 N, crew of three in turns | About 160 kJ at two hand chains (estimate), about 120 N each | Tractor; about 400 N on the brake turns |
| Crew | 3 to 4 | 4 (two at the hand chains) | 4 and a tractor driver |
| STEM check | Within known science; 8 rows open for TRL 4 | Within known science; B3 plausible | Within known science; C1 and C4 plausible |

## Scoring

Table 2. Weighted scoring (weights: High UR 3, Medium 2, Low 1; scores 1 to 5).

| Criterion | Source | Weight | A | B | C | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Nobody goes down the well | UR-001 | 3 | 5 | 5 | 5 | All three are worked from the rim; the bands are passed by the passer in every option |
| Lifts a 600 kg animal | UR-002 | 3 | 5 | 4 | 4 | A: every part at a factor of 3 or more; B: beam at 3.1, the least margin; C: frame fine, guy anchor holding unknown (C1) |
| Wells 15 m deep | UR-003 | 3 | 5 | 4 | 5 | A and C: rope length is cheap; B: two hoists each need 15 m of load chain and a long hand chain loop |
| Wells 3 m across, weak rims | UR-004 | 3 | 4 | 4 | 4 | All keep pads 0.7 m or more back from a 3 m rim |
| Ready in 20 minutes | UR-005 | 3 | 3 | 2 | 2 | A: 20 min estimate, at the limit; B: two A-frames, three beam sections and 24 bolts lifted to 3.3 m; C: three staked anchors, a guy and a tractor to bring up |
| Short briefing | UR-006 | 3 | 4 | 3 | 2 | A: one crank, one brake; B: two hoists must be pulled together to keep the animal level; C: driver, signaller and brake hand must work as one |
| Stops and holds | UR-007 | 3 | 5 | 5 | 2 | A and B: automatic load brakes; C: only the turns on the post, held by a person |
| Gentle on the animal | UR-008 | 3 | 4 | 5 | 3 | B can lift chest and flank separately to keep the animal level; C lifts fast and can jerk |
| Lands without swinging | UR-009 | 3 | 5 | 5 | 4 | Same slid-in bridge in all three; C's hook is off the leg plane and swings more if the tractor surges |
| Human power only | UR-010 | 3 | 4 | 4 | 2 | A: 200 N at the crank; B: hand chain about 120 N per hoist (assumed); C needs a tractor |
| Frame does not tip | UR-011 | 3 | 5 | 4 | 3 | A: tips only at 19.4 deg; B: knee braces hold the beam line; C: stands on its guy and one anchor |
| Nobody falls in | UR-012 | 3 | 4 | 3 | 4 | B's hand chains hang over the well mouth and are pulled from the rim edge |
| Two-person pieces | UR-013 | 2 | 5 | 3 | 4 | A: 32.0 kg at most; B: 25.7 kg beam sections, but the beam is assembled and lifted to 3.3 m; C: legs about 31 kg |
| Affordable to share | UR-014 | 2 | 3 | 2 | 3 | First-order cost A USD 3,093, B about USD 3,400, C about USD 3,000 plus a tractor |
| Lives outdoors | UR-015 | 2 | 4 | 4 | 4 | All steel galvanised; timber pads and deck |
| Local repair | UR-016 | 2 | 4 | 3 | 4 | A: one bought winch; B: two bought chain hoists; C: blocks and a post a workshop can service |
| Free to copy | UR-017 | 1 | 5 | 5 | 5 | No insert in the bands and a separate passer in every option |
| Cost against the value-engineering target | STANDARDS s21 | 2 | 2 | 1 | 2 | All over the USD 1,500 target; B the most |
| Buildable with local skills | STANDARDS s21 | 2 | 4 | 4 | 4 | Plate, tube, box section and timber in all three |
| Safety | STANDARDS s21 | 3 | 4 | 4 | 2 | C: a tractor on the line, a person holding the brake turns and an anchor of unknown holding |
| Maintenance | STANDARDS s21 | 1 | 4 | 3 | 4 | Hoist chains need care in mud; A's winch and C's blocks are simple |
| **Weighted total** (of 265) | | | **224** | **198** | **177** | |

## Recommendation

Option A is recommended: it meets every high-priority user need on paper, holds the load on an automatic brake, needs nothing but people at the well, and has the most margin on the frame. Option B is the runner-up at 198 (11.6 % behind, outside the 10 % band) and its best idea, lifting the chest and the flank separately to keep the animal level, can be grafted onto A without changing its working principle: replace one band's two adjusting chains with a 0.75 t lever hoist so its height can be changed under load (WSL-DEC-001 D16; on 2026-10-25 Amish chose to keep the chains for now and let the TRL 4 dummy trial show whether the hoist is needed). Option C is the fastest lift but scores lowest on control and safety. Amish decided on 2026-10-25 ("i approve of your recommendations"): option A, recorded in the decisions register and WSL-DDR-003; option A stays `CHOSEN` in the model.
