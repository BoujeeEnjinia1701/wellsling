---
doc_id: WSL-DDR-004
title: WellSling STEM check and D3 detailing fixes
project: WellSling
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Seven failed details fixed under Amish's standing instruction of 2026-10-23 during the kit 1.9.1 upgrade (WSL-DEC-001 D10 to D14, D17 and D18)
---

# 0004: STEM check and D3 detailing fixes

- **Date:** 2026-10-25
- **Status:** decided under Amish's standing instruction of 2026-10-23: "when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction; a fix that changes the working principle, pitch or scope goes to Amish instead." None of these fixes changes the working principle, the pitch or the scope. Amish can reverse any of them.

## Context

The kit 1.9.1 upgrade ran the first STEM check on WellSling (WSL-STM-001) and rebuilt the model to detail level D3, with every bolt, pin, shackle, chain link and weld bead modelled and checked for interference (`.kit/cad_check.py`). Seven details failed: one strength check that the kit 1.7 calculation had made too leniently, four joints that could not be assembled as drawn, an option B piece over the carry limit, and (found by the independent review) a proof load above the winch's working rating. Each fix below was weighed against its alternatives for the design and its constructability, implemented in the model, calculations, BOM, build plan and requirements, and the check was rerun so the row closed.

## Decisions

*Table 1. Fixes, options weighed and cost.*

| # | Failed detail (STEM row) | Options weighed | Decision | Cost and effect |
| --- | --- | --- | --- | --- |
| D10 | Leg 1 bends under the rope pull 121 mm off its axis. With the initial bow of L/200 that EN 1993-1-1 Table 5.1 gives for a cold-formed hollow section, the 76.1 x 3.6 mm tube reaches a factor of 2.98 against the 3 required (2.89 with the secant amplification adopted after the independent review) (S12). The larger leg then put the sheave axle's nut and split pin 10 mm inside it | (a) 76.1 x 4.5 mm tube: factor about 3.4, but the leg grows to about 36.6 kg, over the 35 kg carry limit; (b) a mid-length brace on leg 1: more parts and a joint in the strut; (c) bring the drum closer to the leg to cut the rope offset: the winch frame does not allow it; (d) 88.9 x 3.2 mm tube on all three legs | (d) All three legs 88.9 x 3.2 mm, end caps 100 mm across; the sheave axle is held by a head on the far side and a DIN 471 retaining ring on the leg side | Leg 1 factor 3.7; buckling factor 7.3 (was 5.1); each leg 31.8 kg (+1.9 kg); about USD 9 for three legs |
| D11 | One 20 mm chain eye per foot had to take the shackles of two spread chains, drawn with a vertical pin through a horizontal hole: it could not be assembled (S31) | (a) one shackle per foot holding both chain end links in its bow: the bow is loaded from two directions; (b) a master link on the eye: a 2 t master link's wire does not pass an 8 mm chain link; (c) two chain eye fins per foot, each square to its own chain, and chains with an enlarged end link at each end | (c) Two 60 x 45 x 12 mm fins per foot, hole 25 mm above the base; spread chains with enlarged end links | Each shackle pulls in line with its chain; one more small plate per foot; no cost change |
| D12 | The winch bolt pattern was centred 70 mm off leg 1's centre line, so one row of holes sat 10 mm from it, over the tube, where no nut can go (S32) | (a) weld studs to the bracket: no nut access under it either; (b) centre the winch on the tube: the rope would run off-centre on the drum; (c) widen the bracket and move the pattern to 140 mm off the centre line | (c) Bracket 300 x 300 x 10 mm centred 110 mm to the side; bolt pattern 160 mm square centred 140 mm to the side; frames and gearbox set clear of the bracket | Both bolt rows clear the tube by 5 mm or more; 1.6 kg more plate; no cost change |
| D13 | Each 240 mm band eye was shackled straight onto a 1 t bow shackle with a 16 mm jaw: it cannot be fitted, and a webbing sling wider than 75 mm should bear on an essentially straight part (S33) | (a) slings with folded (reduced) eyes: still far too wide for a 1 t jaw; (b) a wide-body sling shackle: heavy and costly; (c) a band end yoke: a removable 25 mm bar through the eye, two side plates and a welded top bar with a lug for the shackle | (c) Four band end yokes (BOM line 29), each eye on a 25 mm bar 258 mm between the plates; adjusting chain in use 200 mm instead of 300 mm so the hooves still clear the deck | Bars at a factor of 4.8; 13.3 kg added below the hook (hook load 662 kg, rope factor 6.0, winch 87 %); USD 80 |
| D17 | The spreader's guide line eyes stood on the beam top 35 mm from each end, over the sleeve and M16 bolt at 500 mm (S35) | (a) move the eyes inboard: they would clash with the 400 mm bolts or the lift lug; (b) weld each eye to an end cap, pointing along the beam | (b) A 60 x 60 x 10 mm eye on each end cap. Detailing the hook and shackle to catalogue sizes also showed the hook bowl 1.5 mm above the lift lug, so the lug is now 110 mm tall with its holes 30 mm below the top edge (tear-out factor still above 20) | No cost change; the guide lines pull along the beam as before |
| D18 | The kit's proof load of 1.5 times the hook load puts 10.0 kN on the rope; on the third layer that is 130 % of the winch's working rating (independent review; S38) | (a) a 1,500 kg winch: cost and mass up, price to assess; (b) proof-test the frame with a separate pulling device and leave the winch at its rating; (c) buy a winch statically tested by its maker to 1.5 times its rated load and hold the proof load on the brake: the drum torque at proof on layer 3 (0.69 kN m) is within the maker's static test torque (0.80 kN m) | (c) Winch specification and first check 4 updated | No cost change assumed (static testing to its standard is normal practice for a rated winch; confirm when bought) |
| D14 | Option B's 5.8 m gantry beam in two halves weighed 38.6 kg a piece, over the 35 kg two-person carry (B4) | (a) a lighter RHS: the beam factor drops below 3; (b) aluminium: cost and joints; (c) three sections with two bolted splices | (c) Three sections of about 1.93 m (25.7 kg), splices with 10 mm side plates and eight M16 bolts each | Option B model only; option B is not the recommended concept |

## Consequences

- WSL-CAL-001 v0.2: C5, C6, E7, F5 and every load result rerun; WSL-PRS-001 statuses from v0.2.
- `cad/src/model.py`, `bom/bom.csv` (lines 1, 3, 4, 5, 8, 10, 13, 17, 18 and the new line 29), the drawings and the build plan pictures regenerated; WSL-BLD-001 updated where these parts are made and fitted.
- Estimated cost of the constructable design: USD 3,093 (was 3,004).
