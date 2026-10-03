---
doc_id: WSL-DDR-001
title: WellSling TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The scaffold (WSL-PRB-001, WSL-PRC-001 and WSL-REQ-001, all v0.1) described a plain webbing belly band, a separate passer pole and the shared HatchSide tripod and winch, with the animal "swung to firm ground" at the top. It left five open questions: whether HatchSide can carry 400 to 600 kg off-centre, wells wider than a tripod can span, passing the band under a lying or wedged animal, band width and padding, and the first trial partner. Populating the concept to TRL 2 meant settling these. Amish pre-approved every recommendation in this batch, so each item below is decided, not proposed. Items that touch safety take the conservative option and say what evidence would relax it. Partners are the first candidates to approach, not agreements.

## Options considered

*Table 1. Options.*

| # | Item | Options |
| --- | --- | --- |
| D1 | Lifting frame | (a) the shared HatchSide tripod; (b) a heavy HatchSide variant shared by both projects; (c) a WellSling tripod of its own, sized for a 600 kg animal |
| D2 | Well width | (a) up to 3 m with a tripod; (b) wider wells with an A-frame or beams over the well |
| D3 | Band arrangement | (a) one belly band on a spreader bar; (b) two bands, chest and flank, on an H-frame spreader |
| D4 | Passing the band | (a) push the band itself with the pole; (b) pass a light messenger line with a J-headed pole, then pull the band through on the line |
| D5 | Getting the animal out of the well mouth | (a) swing it sideways onto firm ground; (b) lift it just clear of the rim and slide a bridge under it, then lower it onto the bridge |
| D6 | Winch | (a) worm-gear winch; (b) spur-gear winch with an automatic load-pressure brake |
| D7 | Rating | (a) 400 kg animal; (b) 600 kg animal (648 kg at the hook), proof 1.5 times, hook line lean up to 10 deg |
| D8 | Co-design partner | Animal rescue organisations, dairy cooperatives, veterinary universities, rural fire services |
| D9 | Work near the rim | (a) stay back by instruction only; (b) harness and work-restraint lanyard tied to a tripod foot for anyone within 1 m of the rim |

## Decision

- **D1 (c).** WellSling has its own tripod. HatchSide is rated in the 191 kg class for people; a 600 kg animal needs about three times that at the hook, and sharing one heavier tripod would make HatchSide too heavy for its own users.
- **D2 (a).** Wells up to 3 m across are in scope; wider wells are out of scope for this kit.
- **D3 (b).** Two plain 240 mm bands on an H-frame spreader. Two bands halve the pressure of one, keep the animal level, and keep the plain-webbing design-around.
- **D4 (b).** A J-headed passer pole and a messenger line, with a separate retrieval hook head. The passer stays a separate tool (design-around).
- **D5 (b).** The animal is landed on a bridge slid across the well mouth and is never swung over the rim. This is the conservative choice: it keeps the load on the well axis and keeps people away from the rim edge. It would be relaxed only by a separate study of a swing-out frame with its own stability case.
- **D6 (b).** A spur-gear winch with an automatic load-pressure brake, mounted on one leg.
- **D7 (b).** A 600 kg design animal, proof 1.5 times, lean up to 10 deg. A heavier animal is outside the rating; the rating rises only after a proof-load test (TRL 4).
- **D8.** First candidates to approach, in order (none approached yet): an animal rescue organisation that runs well rescues in north India; a district dairy cooperative union in Haryana; a state veterinary university for band pressure and handling advice.
- **D9 (b).** Harnesses and work-restraint lanyards (BOM line 28) for anyone within 1 m of the rim. Conservative; it would be relaxed only for a well with a sound parapet at least 1 m high.
- **Unchanged:** the pitch, the problem, the plain-webbing and separate-passer design-arounds, and `budget_usd` (USD 1,500), now read as a value-engineering target.

## Consequences

- The kit is heavier (about 550 kg) and dearer (USD 3,004 estimated, USD 1,504 over the value-engineering target) than a kit that borrows HatchSide; Amish's pre-approval accepts the overrun.
- New requirements R10 to R13 (stability, hand effort, landing clearance, carry weight) in WSL-REQ-001 v0.2.
- The bridge adds a landing step to the method and three pieces of 31.6 kg or less to carry.
- The HatchSide shared block is no longer used; CalRig proof-loading remains the TRL 4 route.
