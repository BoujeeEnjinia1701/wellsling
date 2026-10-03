---
doc_id: WSL-REQ-001
title: WellSling requirements
project: WellSling
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status for every requirement from WSL-CAL-001; R2 restated for the kit's own tripod; R9 restated as a value-engineering target; R10 to R13 added (WSL-DDR-001)
---

# WellSling requirements

Twelve of the thirteen requirements are met on paper or by design. R9 is reported against the value-engineering target, which the constructable design exceeds by USD 1,504, and R8 (operation after a short briefing) can only be shown in a user trial. Results come from WSL-CAL-001; tags in square brackets point to its sections.

> **Safety:** WellSling lifts a heavy, frightened animal over an open well. Nobody goes down the well at any stage. The kit is an open engineering reference, not certified lifting or rescue equipment, and it must be proof-loaded before any use (TRL 4).

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | No entry | Bands passed, rigged, lifted and landed entirely from the rim | Trial with a weighted dummy in a test pit | Met by design |
| R2 | Lifting capacity | Design animal 600 kg (648 kg at the hook with rigging), with the hook line leaning up to 10 deg; proof-loaded to 1.5 times | Proof-load test of tripod, winch, rope and rigging | Met on paper [B1, B5, C5, C6] |
| R3 | Band spreads the load | Each band at least 200 mm (8 in) wide; average pressure on the animal stated | Design review with a veterinary partner | Met on paper: two 240 mm bands, about 17 kPa [E6] |
| R4 | Passer reach | Passes the band under an animal up to 15 m (50 ft) below the rim | Trial in a test pit with a dummy | Met on paper: 16.5 m [G3] |
| R5 | Well span | Straddles wells up to 3 m (10 ft) across, every pad and bearer at least 350 mm back from the rim | Fit check on sample wells | Met: pads 700 mm, bearers 400 mm back [C9, F4] |
| R6 | Fast setup | Three people ready to lift within 20 minutes of arrival | Timed drill | Met on paper, at the limit: 20 min estimate [G4] |
| R7 | Controlled lift | Load held by the winch brake at any point when the handle is released | Brake hold test at proof load | Met by selection of a load-pressure brake |
| R8 | Simple operation | Villagers complete a lift after a 15-minute briefing | User trial with first-time operators | Not shown on paper; to verify at TRL 4 |
| R9 | Value-engineering target | USD 1,500 for the whole kit (a hypothetical control target, not a limit) | Costed bill of materials | Estimated USD 3,004: over the value-engineering target by USD 1,504 [G2] |
| R10 | Tripod stability | No foot lifts with the hook line leaning 10 deg in any direction | Lean test at proof load | Met on paper: tips only at 19.3 deg [C4] |
| R11 | Hand effort | Crank force at most 250 N throughout the lift | Force gauge on the handle | Met on paper: 196 N at most [B6] |
| R12 | Landing clearance | Hooves at least 150 mm above the deck at the landing height, so the bridge slides under | Fit check with a dummy | Met on paper: 162 mm [F5] |
| R13 | Carry weight | No single piece heavier than 35 kg, so two people carry any piece | Weigh the parts | Met on paper: 31.6 kg [G1] |

## Assumptions

- The design animal is 600 kg, the upper end of a grown cow or buffalo; a heavier animal is outside the rating.
- The ground around the well bears at least 75 kPa under a timber pad; a softer site needs larger pads.
- A plain webbing band with a loose felt sleeve can lift a large animal for the length of a lift without injury when two bands share the load. This is to be confirmed with a veterinary partner.
- Most open wells where animals fall are 3 m across or less.
- A village or cooperative keeps the kit in one known place and practises with it.
