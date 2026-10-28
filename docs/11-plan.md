---
doc_id: WSL-PLN-001
title: WellSling project plan
project: WellSling
doc_type: Project plan
version: "0.2"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.9.1 upgrade)
- version: "0.2"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Concept choice (D15, option A) and D16 (a) decided by Amish on 2026-10-25"
---

# WellSling project plan

WellSling is at TRL 3 and stage P3 (design outputs): model, drawings, priced BOM, build plan, decisions register, design FMEA and traceability are in place for option A, and every concept option is modelled at detail level D3. The next gate, P4 (verification), is on hold under the portfolio cap. The decisions requested of Amish are the concept choice (WSL-DDR-003, option A recommended) and review of the five fixes made under his standing instruction (WSL-DEC-001 D10 to D14). Method: STANDARDS sections 19 and 23.

> **Safety:** P4 work starts with a proof-load test of the built kit at 1.5 times the hook load by a competent person. Nothing is lifted over a well, and no animal is lifted, before that.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Amish | WSL-PRB-001 with users, needs and stakeholders | Done (v0.3) |
| STEM check | Design lead | WSL-STM-001, `stem_check.py`, independent review | Done; open items need TRL 4 |
| Concept options | Design lead | WSL-OPT-001, WSL-DDR-003, options models in `cad/src/model.py` | Done; option A chosen by Amish, 2026-10-25 |
| Requirements and traceability | Design lead | WSL-URS-001, WSL-PRS-001, WSL-RTM-001 | Done |
| Calculations | Design lead | WSL-CAL-001 v0.2 | Done |
| Detailed CAD | Design lead | `cad/src/model.py` at D3 for options A, B and C; `cad/fidelity.json`; STEP per part and per assembly | Done |
| Drawings, BOM and build plan | Design lead | WSL-DWG-001, 101 to 116; `bom/bom.csv`; WSL-BLD-001 | Done for option A |
| Regulatory, feasibility, risk, market | Design lead | WSL-REG-001, WSL-FEA-001, WSL-RSK-001, WSL-MKT-001 | Done (first pass) |
| Renders and storefront | Coordinator | Cycles renders on Amish's Mac: options picture, product renders, cards | Scenes exported; rendering pending |
| Co-design partner | Amish | Agreement with an animal rescue organisation or a dairy cooperative union, with a veterinarian | Not started |
| Verification (P4) | Partner and lifting inspector | Proof-load test, brake test, dummy trials | On hold (stage cap P3) |

## Resources needed

Table 2. Resources (P4 is planned work, on hold).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| District fabrication workshop | One kit built to WSL-BLD-001 | About 10 working days | 3,093 (BOM estimate) |
| Competent lifting inspector | Proof-load test at 1.5 times the hook load, brake test | 1 day | To assess |
| Veterinarian or veterinary university | Review of bands, pressure, lift time and handling | 2 days | To assess |
| Animal rescue organisation or cooperative | Test pit, dummy, crew for timed drills and first-operator trials | 3 days | To assess |
| Galvanising plant | Hot-dip galvanising of the made steel parts | Batch | Included in the BOM estimate |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | Problem, STEM check, concept options, first REG, FEA, PLN | Met |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Met |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM and feasibility closed | Met, except five STEM items that need TRL 4 evidence ; the concept choice was made on 2026-10-25 |
| P3 Design outputs | Model at D3, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability | Met (2026-10-25) |
| P4 Verification | Proof-load and brake tests, dummy trials, timed drill, user trial, RSK updated | On hold |
| P5 Validation | Field trial with a partner at real wells, veterinary validation | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish: confirm or reverse the fixes D10 to D14, D17 and D18, and answer the scope question on animals over 600 kg. The concept (option A) and the graft (keep the chains) were decided on 2026-10-25.
2. Amish: decide whether to graft option B's best idea, independent chest and flank adjustment, onto option A (WSL-DEC-001, open decision).
3. Coordinator: render the options picture and the product renders from the exported scenes, then the cards.
4. Amish: approach the first co-design candidates (WSL-PRB-001) when he chooses to start TRL 4.

## References

- American Galvanizers Association. "HDG Corrosion Rates for ISO Categories C1-C5/X." Accessed October 25, 2026. https://galvanizeit.org/knowledgebase/article/hdg-corrosion-rates-for-iso-categories-c1-c5-x.
- AFNOR. "NF EN 13157: Cranes, Safety, Hand Powered Lifting Equipment." Accessed October 25, 2026. https://www.boutique.afnor.org/en-gb/standard/nf-en-13157/cranes-safety-hand-powered-lifting-equipment/fa047756/62318.
- Aleph India. "BIS QCO for Chain Pulley Block, Ratchet Lever Hoist and Universal Gearless Pulling and Lifting Machine." Accessed October 25, 2026. https://alephindia.in/bis-qco-for-hand-operated-chain-pulley-block.php.
- 3M. "DBI-SALA Confined Space Tripod." Cited in WSL-PRB-001. https://www.3m.com/3M/en_US/p/d/b00022925/.
- Centers for Disease Control and Prevention. *Morbidity and Mortality Weekly Report*, 1989. Cited in WSL-PRB-001. https://www.cdc.gov/mmwr/preview/mmwrhtml/00001448.htm.
- Certex. *POWERTEX Round Slings / Webbing Slings, User Manual*. Accessed October 25, 2026. https://www.certex.dk/sites/Powertex/New%20manuals/Slings/Powertex-Slings-PRS-PWE-PWS-User-Manual-ML-20251201.pdf.
- European Committee for Standardization. EN 1993-1-1, *Eurocode 3: Design of Steel Structures, Part 1-1*.
- Google Patents. US5431248A, confined space lowering and retrieving apparatus. Cited in WSL-PRB-001. https://patents.google.com/patent/US5431248.
- Government of India. *The Prevention of Cruelty to Animals Act, 1960*. India Code. Accessed October 25, 2026. https://www.indiacode.nic.in/handle/123456789/1547.
- International Organization for Standardization. ISO 4308-1:2003, *Cranes and Lifting Appliances: Selection of Wire Ropes, Part 1: General*. Accessed October 25, 2026. https://dgcrane.com/wp-content/uploads/2023/09/ISO-04308-1-2003.pdf.
- IndiaMART. "Pulley Chain Block." Accessed October 25, 2026. https://m.indiamart.com/impcat/chain-blocks.html.
- National Institute for Occupational Safety and Health. *FACE 85-02*. Cited in WSL-PRB-001. https://stacks.cdc.gov/view/cdc/164612.
- OzFarmer. "Cow Lifter Liftease." Accessed October 25, 2026. https://ozfarmer.com/products/cow-lifter-liftease.
- PK Safety. "3M DBI-SALA Confined Space Aluminum Tripod with Winch." Cited in WSL-PRB-001. https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010.
- *The Hawk*. "Family of Four Suffocate to Death in Bihar's Vaishali." 2026. Cited in WSL-PRB-001. https://www.thehawk.in/news/india/family-of-four-suffocate-to-death-in-bihars-vaishali.
- University of Florida College of Veterinary Medicine, Veterinary Emergency Treatment Service. "ATR Equipment Resources." Accessed October 25, 2026. https://responseteam.vetmed.ufl.edu/animal-technical-rescue/atr-equipment-resources/.
- Wedge Galvanizing. "Hot Dip Galvanizing to EN ISO 1461:2022." 2024. Accessed October 25, 2026. https://www.wedge-galv.co.uk/wp-content/uploads/2024/10/4b-HDG-to-EN-1461-2024.pdf.
