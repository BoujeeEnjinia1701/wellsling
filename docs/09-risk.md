---
doc_id: WSL-RSK-001
title: WellSling risk register and hazard analysis
project: WellSling
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.9.1 upgrade) with the project risks, the preliminary hazard analysis and a first-pass design FMEA of the chosen design (option A)
---

# WellSling risk register and hazard analysis

The top risks are a person going down the well despite the kit, a falling or swinging 600 kg load, and harm to the animal from the bands or the time it hangs. The design answers the first two with a method that needs nobody below the rim, an automatic load brake, factors of 3 or more and a proof-load gate; the third needs a veterinary partner. Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high); for detection, 5 means hard to detect.

> **Safety:** Nobody goes down the well at any stage; a person in a well is a call to the emergency services. The kit is an open engineering reference, not certified lifting or rescue equipment, and is not used on an animal before a proof-load test at 1.5 times the hook load.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner takes it up | Partners not yet approached; well rescues are sporadic | No trial wells, animals or veterinary review; stalls at TRL 3 | 3 | 4 | Amish | Approach the named candidates in WSL-PRB-001 with the build plan and renders |
| P2 | Veterinary review finds the bands or lift time harmful | No cited tolerance for cattle in slings | Band width, padding or lift speed must change | 3 | 3 | Veterinary partner | Review before any live lift; wider bands or a third band are options |
| P3 | Winch with a load-pressure brake not available locally | Spur-gear braked winches are less common than worm winches | Cost or lead time; a worm winch would make the lift too slow | 2 | 3 | Design lead | Check suppliers in the partner's region; keep the brake requirement (PR-007) |
| P4 | Cost stays about twice the value-engineering target | Own tripod, winch and bridge | Harder for a village to buy | 4 | 2 | Amish | Shared kits per cluster of villages; savings in WSL-DEC-001 value engineering |
| P5 | Passer cannot pass the bands under a lying animal | Long flexible pole, mud, a wedged animal | The method stalls at the first step | 3 | 4 | Design lead | Dummy trial in a test pit at TRL 4 (STEM S26); stiffer lower sections if needed |
| P6 | Users improvise without the proof-load test or the safety stops | Urgency of a real rescue | Collapse or a dropped animal | 3 | 5 | Safety lead | Proof-load gate and safety stops in WSL-BLD-001; training with the partner |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Bad air in the well | A person climbs down to help | Death of rescuers, often several | 5 | 2 | Method needs nobody below the rim (PR-001); safety notes in every document; call the emergency services for a person in a well | Low, depends on discipline at the well |
| H2 | Falling load | Rope, shackle, pin or band fails; brake slips | Animal killed or injured; people struck | 5 | 2 | Factors of 3 or more, rope 6.0; automatic load brake; proof load 1.5 times before use; nobody under the load | Low after the proof-load test |
| H3 | Tripod tips or a foot slides | Guide line pulled hard, swing, soft ground | Frame falls across the well and the crew | 5 | 2 | Tips only at 19.4 deg (PR-010); spread chains; staked pads; hook line kept within 10 deg | Low |
| H4 | Rim collapses | Crumbling or undercut rim loaded by people or pads | Person or frame falls into the well | 5 | 2 | Pads 700 mm and bearers 400 mm back; rim and lining checked at safety stop S4; harnesses within 1 m (PR-014) | Low to medium |
| H5 | Person falls into the well | Working at the rim, reaching for lines | Injury or death | 5 | 2 | Harness on a work-restraint lanyard tied to a foot | Low |
| H6 | Animal injured by the bands | Pressure and time in the bands; uneven share; regurgitation | Injury or death of the animal | 4 | 3 | Two 240 mm padded bands; level the animal with the chains; veterinary review before live lifts | Medium until the review |
| H7 | Kicking or thrashing animal | Fright as it is lifted | Struck crew; dynamic load on the rig | 4 | 3 | Hands clear of bands and legs; guide lines used gently; the 1.5 times proof covers a dynamic factor of 1.5 (STEM S36); vet or handler present | Medium |
| H11 | Animal stuck in mud | Suction and adhesion at the well bottom | Overload of the rig if the crank is forced | 4 | 3 | Stop if the crank gets much harder with no movement (safety stop S5); breakout force to be measured in the dummy trial (STEM S39) | Medium |
| H8 | Crank handle kickback | Handle released without the brake engaging | Hand or arm struck | 3 | 1 | Load-pressure brake holds whenever the handle is released; brake test at proof load | Low |
| H9 | Pinch points | Pins, shackles, chain links, bridge runners pushed under the load | Crushed fingers | 3 | 3 | Runners pushed from the side, never reached under the animal; gloves | Low |
| H10 | Struck by a falling part during setup | Walking the tripod up; head or sheave dropped | Head or foot injury | 4 | 2 | Head pinned on the ground; two foot ropes; nobody under the head; no climbing | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Leg 1 (winch leg) | Carry compression and the rope's bending | Buckles | Frame collapses | Bent leg, low-grade tube, overload | 5 | 1 | 3 | 15 | 88.9 x 3.2 mm structural tube, factor 3.7 with an initial bow (D10); straightness check in the plan; mill certificate |
| F2 | Leg pins and R-clips | Hold the legs to head and feet | Pin walks out | Leg drops free | R-clip missing or not on its lanyard | 5 | 2 | 2 | 20 | R-clips on lanyards; check at every hold point |
| F3 | Spread chains and fins | Stop the feet sliding out | Chain or shackle comes off | Feet slide; tripod collapses | Unmoused pin; slack chain | 5 | 2 | 2 | 20 | One fin and shackle per chain, in line (D11); mouse every pin; take up slack |
| F4 | Winch brake | Hold the load when the handle is released | Brake slips | Load runs back | Wrong winch type; worn brake; oil on the friction discs | 5 | 2 | 3 | 30 | Load-pressure brake specified; brake hold test at proof load; inspect before use |
| F5 | Winch bolts | Hold the winch on the bracket | Bolt loosens | Winch tilts; rope fleet changes | Nyloc not replaced | 4 | 2 | 2 | 16 | All four bolts clear the tube (D12); nyloc nuts; torque check |
| F6 | Wire rope | Carry the hook load | Breaks | Load falls | Kinks, broken wires, crushing on the drum | 5 | 1 | 2 | 10 | Factor 6.0; D/d 25; inspect before each use; replace on damage |
| F7 | Sheave and axle | Turn the rope over the head | Axle comes out | Rope drops off the head | Retaining ring missing | 5 | 1 | 3 | 15 | Head on the far side, DIN 471 ring on the leg side (D10); check at safety stop |
| F8 | Lift shackle | Join hook to spreader | Pin unscrews | Spreader drops | Unmoused screw pin | 5 | 2 | 2 | 20 | Mouse with wire; latched hook |
| F9 | Band end yokes | Carry the band eye on a straight bar | Removable bar slides out | Band end drops | R-clip missing | 5 | 2 | 2 | 20 | Two R-clips per bar; check before lifting (D13) |
| F10 | Webbing bands | Carry and cradle the animal | Band cut or torn | Animal slips or falls | Sharp edge, alkali damage, UV | 5 | 2 | 2 | 20 | Felt sleeves; inspect; store dry and dark; no lime or ash (STEM S29) |
| F11 | Bands on the animal | Spread the load | Uneven share; slips toward the belly | Injury; animal tips | Band spacing wrong for the animal | 4 | 3 | 3 | 36 | Choose sleeves 300 to 500 mm; adjust chains to level; veterinary guidance (S25) |
| F12 | Pads and stakes | Carry the feet on soft ground | Pad sinks or tilts | Tripod leans | Soft or saturated ground | 4 | 2 | 2 | 16 | 15 kPa design pressure; larger pads on soft ground; site check |
| F13 | Bridge runners | Carry the animal on landing | Runner slips off a bearer | Deck drops | Runner not over the bearer band | 4 | 2 | 2 | 16 | White bands mark the bearing length; cleats keep the deck on |
| F14 | Deck panels | Carry the hooves | Plywood breaks under a hoof | Leg through the deck | Rotten or delaminated ply | 4 | 1 | 2 | 8 | Factor 3.4; exterior ply; sealed edges; inspect |
| F15 | Passer pole joints | Keep the pole together | Section separates down the well | Pole lost; J-head down the well | Button lock not engaged | 2 | 3 | 2 | 12 | Button must show in every joint; tether line on the J-head |
