---
doc_id: WSL-REG-001
title: WellSling regulatory and standards register
project: WellSling
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.9.1 upgrade)
---

# WellSling regulatory and standards register

Which standards and regulations bear on WellSling, where, and what is needed. WellSling is published as an open engineering reference, not as certified lifting or rescue equipment, and nothing here is a product claim. The bought lifting parts (winch, wire rope, shackles, chain, webbing slings and harnesses) should each be bought declared to its standard; the made parts are designed with steel-design practice and must be proof-loaded before use (TRL 4). Not legal advice; anything marked "to assess" needs a qualified reviewer, such as a competent lifting inspector, before any use on an animal. Method: STANDARDS section 23.

> **Safety:** Lifting equipment is regulated because its failure kills. Until a proof-load test at 1.5 times the hook load has been passed and recorded by a competent person, the kit is not used on an animal or near people.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | EN 13157:2004+A1:2009, Cranes, safety, hand powered lifting equipment | EU (reference practice elsewhere) | Hand powered lifting equipment, including drum winches, manual chain hoists, lever hoists and pulley blocks | The hand winch (BOM line 9) in option A; the chain hoists of option B. Buy a winch declared to it or to an equivalent national standard | Design lead | To assess |
| G2 | IS 3832:2005, Hand operated chain pulley blocks, and the draft Chain Pulley Block, Ratchet Lever Hoist and Universal Gearless Pulling and Lifting Machine (Quality Control) Order, 2025 | India | Design and testing of hand chain blocks; draft order to require BIS certification | Option B only; option A has no chain block | Design lead | Does not apply to option A; applies if option B is chosen |
| G3 | EN 1492-1, Textile slings, flat woven webbing slings made of man-made fibres | EU (reference practice elsewhere) | Webbing slings: working load limits, eyes, marking and use, including the rule that a sling wider than 75 mm bears on an essentially straight part | The two 240 mm bands (BOM line 18) and their yoke bars (line 29, STEM S33) | Design lead | Applies (buy to it); met by design for the yoke bar |
| G4 | EN 818-2, Short link chain for lifting purposes, grade 8 | EU (reference practice elsewhere) | Grade 8 lifting chain | Spread chains and adjusting chains (BOM lines 8 and 17) | Design lead | Applies (buy to it) |
| G5 | EN 13889, Forged steel shackles for general lifting purposes | EU (reference practice elsewhere) | Dee and bow shackles | Every shackle (BOM lines 8 and 16) | Design lead | Applies (buy to it) |
| G6 | EN 12385-4, Steel wire ropes, stranded ropes for general lifting; IS 2266, Steel wire ropes for general engineering purposes | EU; India | Wire rope construction and minimum breaking load | The 8 mm wire rope (BOM line 11) | Design lead | Applies (buy to one of them) |
| G7 | EN 361, Full body harnesses; EN 358, Belts and lanyards for work positioning and restraint | EU (reference practice elsewhere) | Personal fall protection | Rim harnesses and lanyards (BOM line 28, PR-014) | Safety lead | Applies (buy to it) |
| G8 | EN ISO 1461:2022, Hot dip galvanized coatings on fabricated iron and steel articles | International | Coating thickness and finish | Every made steel part (PR-015, STEM S28) | Fabricator | Met by design |
| G9 | EN 1993-1-1, Eurocode 3, design of steel structures | EU (reference practice elsewhere) | Member resistance, buckling, imperfections | Used for the leg check with an initial bow (WSL-CAL-001 C6) | Design lead | Used as the design reference |
| G10 | The Prevention of Cruelty to Animals Act, 1960 | India | Duty not to cause unnecessary pain or suffering to animals | How an animal is handled and lifted; band pressure and time in the bands (STEM S25) | Veterinary partner | To assess |
| G11 | The Factories Act, 1948, section 29 (lifting machines, chains, ropes and lifting tackles) | India | Examination of lifting tackle in factories | A farm or village is not a factory, so it does not apply directly; its periodic examination is adopted as practice (inspect before each use, proof-load after any repair) | Safety lead | Does not apply (adopted as practice) |
| G12 | Regulation (EU) 2023/1230 on machinery | EU | Placing machinery and lifting accessories on the EU market | Only if a kit were ever sold or supplied in the EU; the open design itself is not placed on the market | Amish (decision) | To assess (only before any supply) |
| G13 | State and district rules on covering open wells | India (local) | Prevention: covers and parapets on open wells | Prevention is out of the kit's scope (WSL-PRB-001) but is the first answer; the partner would know the local rules | Co-design partner | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- AFNOR. "NF EN 13157: Cranes, Safety, Hand Powered Lifting Equipment." Accessed October 25, 2026. https://www.boutique.afnor.org/en-gb/standard/nf-en-13157/cranes-safety-hand-powered-lifting-equipment/fa047756/62318.
- Aleph India. "BIS QCO for Chain Pulley Block, Ratchet Lever Hoist and Universal Gearless Pulling and Lifting Machine." Accessed October 25, 2026. https://alephindia.in/bis-qco-for-hand-operated-chain-pulley-block.php.
- Certex. *POWERTEX Round Slings / Webbing Slings, User Manual* (instructions to EN 1492-1). Accessed October 25, 2026. https://www.certex.dk/sites/Powertex/New%20manuals/Slings/Powertex-Slings-PRS-PWE-PWS-User-Manual-ML-20251201.pdf.
- Government of India. *The Prevention of Cruelty to Animals Act, 1960*. India Code. Accessed October 25, 2026. https://www.indiacode.nic.in/handle/123456789/1547.
- Wedge Galvanizing. "Hot Dip Galvanizing to EN ISO 1461:2022." 2024. Accessed October 25, 2026. https://www.wedge-galv.co.uk/wp-content/uploads/2024/10/4b-HDG-to-EN-1461-2024.pdf.
- The other standards are cited by number and title; their texts were not consulted for this register, and each is to be checked against the edition in force when parts are bought.
