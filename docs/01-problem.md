---
doc_id: WSL-PRB-001
title: WellSling problem statement
project: WellSling
doc_type: Problem statement
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
  change: Populated to TRL 2 and 3; constraints restated for the kit's own tripod and the value-engineering target; open questions settled in WSL-DDR-001; first co-design candidates named; safety section added
---

# WellSling problem statement

Livestock fall into open wells in farming villages. People go down to get them out, and the bad air at the bottom kills them.

## The problem

Wells and pits can hold air that is low in oxygen or full of gases, and a person can collapse within seconds of entry, as survivors of a NIOSH-investigated tank incident reported ([NIOSH FACE 85-02](https://stacks.cdc.gov/view/cdc/164612)). Farm families face this in pits and wells, and deaths come in chains: one person collapses and others follow ([CDC MMWR, 1989](https://www.cdc.gov/mmwr/preview/mmwrhtml/00001448.htm); [The Hawk, 2026](https://www.thehawk.in/news/india/family-of-four-suffocate-to-death-in-bihars-vaishali)). An animal in a well adds urgency and value, which pushes people to act before help arrives.

Existing non-entry equipment is built for people, not large animals. Commercial confined-space tripods carry a rated load of about 191 kg (420 lb) ([3M](https://www.3m.com/3M/en_US/p/d/b00022925/)) and cost several thousand dollars with a winch ([PK Safety](https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010)), while a grown cow or buffalo can weigh 400 to 600 kg (estimate). There is no low-cost, open way to get a lifting band under a heavy animal from the rim of a well.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Farmers and livestock owners | Get a fallen animal out without anyone climbing down | Open wells on farms and village edges, minutes after the fall |
| Village volunteers and dairy cooperative staff | A kit they can fetch, set up and use with a short briefing | Kit kept at a shared point in the village |
| Animal rescue organisations | A lighter, cheaper large-animal lift for well rescues | Rescue vans covering many villages |
| Rural fire and disaster response crews | A non-entry option for animal-in-well call-outs | Long travel to villages |

## Operating environment

- Open, unlined or brick-lined wells assumed 1 to 3 m (3 to 10 ft) across and up to about 15 m (50 ft) deep for a first version (estimate).
- Rims may be crumbling, wet or unlined, with soft ground around them.
- Animal may be in water, standing, lying or wedged, and frightened.
- Hot, dusty or monsoon conditions; work often by day with no power on site.
- Air in the well may be low in oxygen or contain gases.

## Constraints

- Value-engineering target USD 1,500 for the kit (a hypothetical control target, not a spending limit). The target was set when the kit was to borrow the HatchSide tripod; HatchSide is rated for people (about 191 kg class), so WellSling now carries its own 600 kg tripod and winch (WSL-DDR-001).
- Everything worked from the rim; no step may need a person to go down.
- Plain webbing belly band with no stiffening insert, and the passer as a separate tool (IP design-around).
- Operable by three to four untrained villagers after a short briefing.
- Open design: hardware under CERN-OHL-S-2.0.

## Out of scope

- Rescue of people from wells.
- Veterinary care of the animal after lifting.
- Well covers, parapets and prevention, which are recommended but separate.
- Wells wider than 3 m, which need a different frame (for example an A-frame or a gantry over beams).

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| 3M DBI-SALA confined space tripod | Aluminium tripod of 2.13 or 2.74 m for confined-space entry and rescue, rated 191 kg (420 lb) | Rated for people, not 400 to 600 kg animals, and costly | [link](https://www.3m.com/3M/en_US/p/d/b00022925/) |
| 3M DBI-SALA tripod with Salalift II winch | Tripod and retrieval winch system with 18 m (60 ft) of cable, about USD 5,850 to 6,120 | No means of passing a band under an animal; price out of reach for villages | [link](https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010) |
| US5431248A confined space lowering and retrieving apparatus | Expired patent for a tripod or quadruped frame over manways | Personnel system; free prior art for a frame | [link](https://patents.google.com/patent/US5431248) |

## Co-design

A dairy cooperative or animal welfare organisation that already responds to animals in wells, ideally with a veterinarian, so the band, passer and lifting method are shaped around real animals, real wells and animal welfare during the lift. The first candidates to approach (none approached yet) are an animal rescue organisation that runs well rescues in north India, then a district dairy cooperative union in Haryana whose members lost people in the Jhajjar incident, with a state veterinary university for the band and handling advice (WSL-DDR-001, D8).

## Questions settled at TRL 2

The scaffold's open questions were settled in WSL-DDR-001 under Amish's 2026-10-03 pre-approval:

- The shared HatchSide tripod cannot carry a 600 kg animal, so WellSling has its own tripod, rated at a 648 kg hook load with the line leaning up to 10 deg (D1).
- Wells wider than 3 m are out of scope for this kit (D2).
- An animal lying down or wedged is reached with the J-headed passer pole and a messenger line: the J goes under the body and the nose brings the line up the far side, and the line then pulls the band through (D4).
- Two plain webbing bands 240 mm wide, chest and flank, with loose felt sleeves, share the load; the veterinary view on pressure and duration is an item to confirm (D3).
- The first co-design candidates are named above (D8).

## Safety

> **Safety:** The hazard that WellSling exists to remove is the bad air at the bottom of a well: nobody goes down at any stage, and if a person is already in the well, call the emergency services. The kit itself lifts a 600 kg animal over an open hole, so its own hazards are a falling or swinging load, a tipping tripod, a collapsing rim and a kicking animal. The design answers these with a load-brake winch, spread chains, pads set back from the rim, a landing bridge so the animal is never swung over the rim, and harnesses for anyone near the rim. It is an open engineering reference, not certified equipment.
