---
doc_id: WSL-DDR-003
title: WellSling concept selection
project: WellSling
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection proposed (kit 1.9.1 upgrade); awaiting Amish
- version: "0.2"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Accepted: Amish chose option A and graft option (a) on 2026-10-25 (\"i approve of your recommendations\")"
---

# 0003: Concept selection

- **Date:** 2026-10-25
- **Status:** Accepted. Amish Chadha (owner), 2026-10-25 12:43 CT: "i approve of your recommendations". Option A is carried forward (WSL-DEC-001 D15) and the adjusting chains stay (D16, option (a)); `concept_chosen: A`.

## Context

Kit 1.8 requires at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21). WellSling was designed before kit 1.8, so its design is option A and is not redesigned without Amish's go. Two further options were developed, modelled at detail level D3 and checked in the STEM check (WSL-STM-001): a portable gantry with two hand chain hoists (B) and sheerlegs with a draught haul (C). The scoring is in WSL-OPT-001, Table 2.

## Options considered

*Table 1. Options.*

| Option | Working principle | Weighted score (of 265) | Strengths | Weaknesses |
| --- | --- | --- | --- | --- |
| A Tripod and hand winch | Own tripod and sheave; braked hand winch on one leg; two bands on an H-frame; slid-in bridge | 224 | Automatic brake; human power only; most margin; heaviest piece 32.0 kg | Setup time at its limit; one lift line, so the animal is levelled only by setting the chains before the lift |
| B Portable gantry and chain hoists | Box beam on two A-frames; one hand chain hoist per band | 198 | Chest and flank lifted separately; automatic hoist brakes | Beam assembled and lifted to 3.3 m; two operators pulling over the well mouth; 15 m of load chain per hoist; highest cost |
| C Sheerlegs and draught haul | Two leaning legs on a back guy; tractor hauls through blocks, with brake turns on a post | 177 | Fast lift; rope length cheap | No automatic brake; tractor jerk risk; guy anchor holding unknown; three anchors to set |

## Recommendation

Decided by Amish on 2026-10-25, as recommended: carry option A forward. B is 11.6 % behind, outside the 10 % band, so a single option is recommended rather than two. Graft B's best idea, separate adjustment of the chest and flank bands, by replacing one band's adjusting chains with a 0.75 t lever hoist if the TRL 4 dummy trial shows the animal hanging nose or tail down (WSL-DEC-001 D16, decided 2026-10-25: option (a), the adjusting chains stay and the dummy trial decides whether to try the lever hoist).

## Consequences

- A is confirmed: no change to the design; `concept_chosen` in `project.yaml` is A.
- If B or C is chosen: the chosen option's model in `cad/src/model.py` becomes `CHOSEN`, and the drawings, priced BOM, build plan, calculation note and requirements statuses are redone for it.
