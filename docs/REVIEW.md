# Review note: WellSling

## Session 2026-10-25: decisions

Amish Chadha (owner), 2026-10-25 12:43 CT, after a report listing each repo's proposed decisions and recommendations: "i approve of your recommendations". Both open decisions in WSL-DEC-001 carried a recommendation and are recorded as decided by Amish on 2026-10-25 with the option recommended (WSL-DEC-001 v0.3; WSL-DDR-003 v0.2, accepted). Brief: `/home/claude/fleet/DECISIONS.md`.

### Decisions now decided

- **D15, concept carried forward: option A**, tripod and hand winch (224 of 265; B 198, C 177). `project.yaml` `concept_chosen: A`; the model's `CHOSEN` was already A.
- **D16, graft of option B's idea: option (a)**, keep the adjusting chains, set before the lift. The lever hoist of option (b) is tried only if the TRL 4 dummy trial shows the animal hanging nose or tail down.

### What changed

No change to the design, model, drawings, calculations or BOM: both decisions keep the design as it stands. Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 3,093 (USD 1,593 over the target, PR-009 not met, as before); `budget_usd` unchanged. Text updated: `docs/06-design-decisions.md` (open decisions now none; two rows in Decisions made), `docs/decisions/0003-concept-selection.md`, `project.yaml`, `docs/02-concept.md` (WSL-PRC-001 v0.4), `docs/02a-concept-options.md` (WSL-OPT-001 v0.2), `docs/05-build-plan.md` (WSL-BLD-001 v0.3: check 8 records whether the dummy hangs level, for D16), `docs/11-plan.md` (WSL-PLN-001 v0.2), `README.md`.

### Still open (no recommendation, so not decided)

- Amish's review of the seven fixes made under the standing instruction (D10 to D14, D17, D18); each can be reversed.
- The reviewer's scope question: adult buffalo and Holstein cows can weigh 650 to 800 kg, above the 600 kg rating Amish set on 2026-10-03. Options were posed without a pick (keep 600 kg and state the limit on the kit, or re-rate for 750 kg).

### Safety

Unchanged: nobody goes down a well; the kit is not used on an animal before the proof-load test; the dynamic load of a kicking animal, mud breakout, the rim and the animal's tolerance of the bands remain TRL 4 checks.

### Recommended next step

Amish answers the two open questions above. Then the coordinator renders `media/options.png`. TRL 4 stays on hold under the portfolio cap.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (WSL-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (WSL-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (WSL-REQ-001 v0.1): 9 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## Session 2026-10-03: TRL 2 (populate)

Run as the first half of `/to-trl3` under Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Kit 1.7.0 installed.

### What was done

- `docs/01-problem.md` (WSL-PRB-001 v0.2): constraints restated (own tripod, value-engineering target), scope of wells up to 3 m, open questions settled, first co-design candidates, safety section.
- `docs/02-concept.md` (WSL-PRC-001 v0.2): how it works in five stages, components with BOM numbers, key design choices, first-order numbers, design-arounds kept, safety.
- `docs/03-requirements.md` (WSL-REQ-001 v0.2): 13 measurable requirements (R10 to R13 added) with TRL 3 status.
- Concept media from `cad/src/concept_media.py`: `media/hero.png` (with the 600 kg design animal and the well for scale), `media/concept-blueprint.png`, `.pdf` and `.svg` (WSL-DWG-010), `media/model.glb`, `media/viewer.html`, `media/exploded.png` with BOM callouts, `media/flow.png` (energy of a 15 m lift, estimates). No cutaway: nothing inside the parts matters to the concept.
- `bom/bom.csv`: 28 priced lines.

### Results

- The concept works on paper only with a tripod of its own: the shared HatchSide tripod is rated for people (191 kg class), and the design animal puts 648 kg on the hook.
- Swinging a 600 kg animal sideways over a rim was replaced by a slide-in landing bridge, keeping the load on the well axis.

### Requirements not met

- R9: over the value-engineering target (see TRL 3).
- R8 cannot be shown on paper.

### Decisions made under the pre-approval

WSL-DDR-001, items D1 to D9: own tripod; wells to 3 m; two bands on an H-frame; J-headed passer with messenger line; landing bridge, never swung; braked spur-gear winch; 600 kg rating with proof at 1.5 times and a 10 deg lean limit; first co-design candidates (not approached); harnesses near the rim.

### Safety concerns

- The kit lifts 600 kg over an open hole: falling or swinging load, tipping tripod, collapsing rim, kicking animal. All answered in the design and the safety stops, and none is cleared until a proof-load test.

## Session 2026-10-03: TRL 3 (advance and build plan)

Run as the second half of `/to-trl3` under the same pre-approval, which counts as the TRL 2 approval. An earlier run of this session stopped when the disk filled after the model, BOM and sizing were done; this run continued from those files and completed the rest.

### What was done

- `cad/src/model.py`: parametric build123d model of the constructable kit; 73 of 73 constructability checks pass (contact, clearance, rim set-back, landing clearance, rope fall and spreader swing). Exports `cad/step/wellsling-assembly.step` and four STL groups in `cad/stl/`.
- `docs/04-calcs/01-sizing.md` (WSL-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: loads, rope, sheave and winch, tripod statics and stability, pins and hangers, spreader and bands, landing bridge, mass, cost, reach and setup, and a results table against every requirement.
- `cad/src/sheets.py`: general arrangement `cad/drawings/WSL-DWG-001` (SVG, PDF, PNG) at Rev P1.
- `cad/src/build_plan_media.py`: `docs/05-build-plan/overview.png`, 15 making sketches `cad/drawings/WSL-DWG-101` to `115`, 11 joint close-ups and 14 step pictures.
- `docs/05-build-plan.md` (WSL-BLD-001 v0.1), `docs/06-design-decisions.md` (WSL-DEC-001 v0.1), `docs/decisions/0001-trl2-review-decisions.md` (WSL-DDR-001) and `docs/decisions/0002-design-for-construction.md` (WSL-DDR-002).
- `cad/src/product_model.py` (appearance model) and render scenes exported with `.kit/export_views.py` for hero, exploded and detail views; photoreal renders and cards are made on Amish's Mac.
- `project.yaml`: trl 3, trl_target 3, `design_state: constructable`, evidence listed; `budget_usd` unchanged. README leads with `media/render-hero.png` and has a "Building the prototype" section.

### Results

- Hook load 648 kg for a 600 kg animal; rope factor 6.1; sheave D/d 25; winch at 85 % of capacity on the third layer.
- Leg buckling factor 5.1 with a 10 deg lean (3.4 at proof); leg 1 bending factor 3.7; the tripod tips only at 19.3 deg.
- Spread chains needed (thrust 0.59 of vertical, above 0.4 friction); chain factor 23; ground pressure 15 kPa.
- Crank force at most 196 N; a 15 m lift takes about 29 minutes; 144 kJ at the crank.
- Bridge runner factor 3.4 or more; hooves 162 mm above the deck at the landing height.
- Kit about 550 kg; heaviest piece 31.6 kg; setup about 20 minutes.
- Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 3,004 (USD 1,504 over the target).

### Requirements not met

- R9: over the value-engineering target by USD 1,504. The target assumed a borrowed tripod; the overrun is accepted under the pre-approval and `budget_usd` is unchanged.
- R6 is met only at its limit (20 minutes, estimate).
- R8 (operation after a 15-minute briefing) cannot be shown on paper; it needs a user trial at TRL 4.

### Decisions made under the pre-approval

- WSL-DDR-002: design for construction, changes C1 to C14 and assumptions A1 to A5.
- No use on an animal before a proof-load test at 1.5 times the hook load.
- Appearance model departures (renders only): a safe working load label on leg 1, a ground slab and brick well ring, the clay 600 kg design animal hanging in the bands, and a 1.75 m mannequin standing at the winch for scale.
- A rim harness line (BOM line 28) was added under D9.

### Build plan findings

- Design changes for construction (2026-10-03), all in WSL-DDR-002: pinned legs with welded tongues; head weldment with lug pairs and sheave hangers; sheave offset beside leg 1 so the rope clears every leg; winch bracket welded on leg 1; staked foot plates on hardwood pads; three spread chains; H-frame spreader with sleeved bolt holes and a five-hole lift lug; swivel hook and lift shackle; chain-and-shackle band ends; loose felt sleeves; sectioned passer with J-head and hook head; landing bridge of bearers, runners and cleated deck panels; guide line eyes; galvanising with vent holes.
- The rope must be reeved over the sheave before the tripod is raised; the plan forbids climbing the tripod.
- The bridge is assembled only after the animal is above the rim, and runners are pushed from the side, never reached under the animal.
- Items to confirm with real parts (winch handle force and bolt pattern, tube certificate, sheave, ground, veterinary view on bands, deck mass, well survey) are in WSL-DEC-001.

### Safety concerns

- Lifting: the kit is not certified lifting or rescue equipment. Safety stops S1 to S7 in WSL-BLD-001 gate raising, loading, first use, lifting, bridging and lowering. Use on an animal waits for a proof-load test at 1.5 times the hook load with a competent lifting inspector.
- Bad air: the method never needs anyone below the rim; a person in a well is a call to the emergency services.
- Rim: pads 650 mm and bearers 350 mm back; harnesses within 1 m of the rim.
- Animal welfare: band pressure and lift time (about 29 minutes) need a veterinary view before any live lift.

### Recommended next step

The design looks ready for TRL 4 once Amish chooses to start it: build one kit, proof-load it with CalRig at 972 kg, and run the first checks in WSL-BLD-001 section 5 with a dummy in a test pit, with the first co-design candidate and a veterinarian involved.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.


## Session 2026-10-24: kit 1.9.1 upgrade

Run under Amish's instructions of 2026-10-24 ("I want detailed TRL3 CAD - and in fact want to ensure the CAD is detailed across all TRLs", "Detail every option", "Kit 1.9.1 rollout - proceed to rollout across the other repos") and his standing instruction of 2026-10-23 on STEM check failures. Work carried out on 2026-10-25; documents are dated that day. Kit 1.9.1 was installed by the coordinator (`.kit/`, `CLAUDE.md`, `.claude/commands/`). The design is unchanged in principle; seven details were fixed under the standing instruction.

### What was added

- `/upgrade-1.8` pipeline: `docs/01b-stem-check.md` (WSL-STM-001) with `docs/04-calcs/stem_check.py` and `stem_results.csv`; `docs/02a-concept-options.md` (WSL-OPT-001); `docs/decisions/0003-concept-selection.md` (WSL-DDR-003); users-and-needs and stakeholders tables in `docs/01-problem.md` (v0.3); `docs/03a-user-requirements.md` (WSL-URS-001, 17 URs); `docs/03-requirements.md` now WSL-PRS-001 (17 PRs, replacing WSL-REQ-001); `docs/03b-traceability.md` (WSL-RTM-001, generated, 0 gaps); `docs/07-regulatory.md` (REG), `08-feasibility.md` (FEA), `09-risk.md` (RSK with preliminary hazard analysis and a 15-row design FMEA), `10-market.md` (MKT), `11-plan.md` (PLN).
- `/upgrade-1.9`: `cad/src/model.py` rebuilt to the kit 1.9 interface (`PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN = "A"`, `OPTION_VIEWS`, `ALLOWED_CONTACTS`, `components(option)`), every option at D3 with `.kit/cad_parts.py` and the repo helpers in `cad/src/wsl_parts.py` (placed stock, fillet and ring weld beads, link-by-link chain, bow shackles). The legacy interface (`derived`, `build_components`, `mass_table`, `chain_eye_points`, `checks`) is kept and now built from the detailed parts, so `sizing.py`, the drawings and the build plan pictures use the D3 geometry. `cad/fidelity.json` passes at D3; STEP per made or bought part of option A in `cad/step/A/` and an assembly STEP per option.
- Regenerated from the model: `cad/drawings/WSL-DWG-001` (Rev P2), the 15 making sketches and a new one, `WSL-DWG-116` (band end yoke), the overview, 11 joint and 14 step pictures in `docs/05-build-plan/`, STL in `cad/stl/` (0.15 mm tolerance), and the concept media (`media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.*`, `model.glb`, `viewer.html`). `cad/src/product_model.py` rebuilt from `components(CHOSEN)` with a site scene.
- Updated: WSL-CAL-001 v0.2, WSL-PRC-001 v0.3, WSL-BLD-001 v0.2 (new section 3.15 for the yokes), WSL-DEC-001 v0.2, `bom/bom.csv` (new line 29, nine lines revised, converted to the kit's `item` format), README in the house structure, `project.yaml` (`stage: P3`, `stem_check: open`, `concept_options`, `concept_chosen: A (proposed)`, evidence).

### STEM verdicts and fixes

48 claims: 37 within known science, 11 plausible to confirm at TRL 4, none fails (`stem_check: open`). Fixed under the standing instruction and recorded in WSL-DEC-001 and WSL-DDR-004:

- D10: legs 88.9 x 3.2 mm (was 76.1 x 3.6): leg 1 reached a factor of only 2.98 (2.89 with secant amplification) once an initial bow of L/200 is counted; now 3.7. The sheave axle is held by a head and a retaining ring so it clears the larger leg.
- D11: two chain eye fins per foot (one 20 mm eye had to take two shackles); spread chains with enlarged end links.
- D12: winch bracket 300 x 300 mm, bolt pattern 140 mm off the leg's centre line (one bolt row sat over the tube).
- D13: band end yokes, a removable 25 mm bar through each 240 mm band eye (it was shackled onto a 1 t shackle with a 16 mm jaw); adjusting chain in use 200 mm.
- D14: option B beam in three sections (two halves were 38.6 kg each).
- D17: guide line eyes on the beam end caps (they sat on the end sleeves and bolts); lift lug 110 mm tall so the hook clears it.
- D18 (from the independent review): winch bought statically tested to 1.5 times its rating; proof load held on the brake (the 1.5 times proof exceeded the winch's working rating on its third layer).

Effect: hook load 648 to 662 kg, rope factor 6.1 to 6.0, winch 87 % on layer 3, crank 200 N, lift 18.2 m of rope in about 30 minutes, hooves 169 mm above the deck, heaviest piece 32.0 kg, estimated cost USD 3,093 (USD 89 more).

### Independent review

A headless second agent saw only the STEM check, the calculation note, the PRS and `sizing.py`. It upheld most arithmetic and raised 19 findings; responses are in WSL-STM-001, Table 3. Changes made: dynamic case added as an open item (S36), winch proof fix D18, rope termination and drum D/d checks (S2, S37), secant amplification on leg 1 (C6), lean-case pad pressure (C10), spread chain line across the well mouth (C11), winch bracket check (D4), pin bending (D1), lift taken as 18.2 m (B8), rim and lining made a go or no-go check (S15, safety stop S4), mud breakout added (S39, safety stop S5), PR-006 set to at risk.

### Option scores

| Option | Score (of 265) | Parts (D3) | Mass (kg, modelled) |
| --- | --- | --- | --- |
| A Tripod and hand winch | 224 | 351 (86 fasteners, 100 welds) | 522.0 |
| B Portable gantry and chain hoists | 198 | 427 (164 fasteners, 86 welds) | 654.4 |
| C Sheerlegs and draught haul | 177 | 312 (67 fasteners, 81 welds) | 552.8 |

Masses are from `cad/fidelity.json`: every modelled part at the kit's densities, with the winch and rope drawn in part. The calculation note's kit mass (555 kg) adds the lines, the passer and catalogue masses. B is 11.6 % behind A, outside the 10 % band.

### Requirements not met

- PR-009: over the value-engineering target by USD 1,593 (estimate USD 3,093 against USD 1,500).
- PR-006: at risk; the 20 minute setup estimate has no margin.
- PR-008: operation after a short briefing can only be shown in a user trial (TRL 4).
- PR-003 and PR-011 are met on paper for width and force; the animal's tolerance of the bands and the winch's real handle force are open (S25, S6).

### Decisions proposed and awaiting Amish

- D15: concept choice; option A recommended (224 of 265), WSL-DDR-003.
- D16: graft option B's best idea onto A, a lever hoist in place of one band's adjusting chains to level the animal under load; recommended only if the TRL 4 dummy trial shows the need.
- Review of the seven fixes D10 to D14, D17 and D18 made under the standing instruction (each can be reversed).
- Scope question raised by the reviewer: adult buffalo and Holstein cows can weigh 650 to 800 kg, above the 600 kg rating Amish set on 2026-10-03 (WSL-DDR-001, D7). Options: keep 600 kg and state the limit on the kit, or re-rate for 750 kg (heavier legs, winch and rigging). Not changed.

### Safety concerns

- The dynamic load of a kicking animal, breaking an animal free of mud, the rim and lining at each well and the animal's tolerance of the bands are not shown on paper; each is a TRL 4 check, and the safety stops now say what to do (stop, do not force; no-go on a doubtful rim).
- The spread chains cross the well mouth near its edge; stepping over them near the rim needs a harness.
- Nobody goes down a well; the kit is not used on an animal before the proof-load test.

### Kit bugs and notes met

- `.kit/cad_check.py` reads the BOM line number only from a column named `item` (leading digits). This repo's BOM kept the number in a `line` column and the name in `item`, so every BOM line looked missing. Worked around by converting `bom/bom.csv` to the kit format (`item` = "1 Tripod leg"); no repo script read `line`.
- `.kit/stem_check.py` treats any text in `closed_by` as closed, so a plausible row whose route to closure is written there reads as closed and the summary says "pass". Open rows keep `closed_by` empty and carry the route in the check text.
- The outdoor ground in `.kit/photoreal.py` is a solid plane, so a well mouth cannot show as a hole; the product model draws the dark of the shaft as a thin disc at ground level.
- `media/options.png` is not in the repo: it needs the Cycles render on Amish's Mac (`.kit/options.py` without `--export` was not run, as instructed). `python .kit/options.py --export` ran this 8 GB machine out of memory (it meshes every part of all three D3 options at 0.05 mm into Python vectors), so the scenes were exported by a scratch wrapper around the same kit code that reads each part's 0.4 mm premesh into numpy; the scenes and `wellsling__options_jobs.json` are in the session scratchpad (`wellsling-options-export/`) for the coordinator, who may prefer to rerun the kit export on the Mac. Until the coordinator renders it, `render.py --check` reports it missing.
- Meshing: build123d meshes with a relative deflection, so each small chain link torus came out at about 32,000 triangles and the D3 renders ran the 8 GB machine out of memory (exit 137). `cad/src/wsl_parts.py` now builds links without booleans and premeshes every part with an absolute deflection (0.4 mm, 0.5 rad); heavy steps run one per process.
- The kit's web export (`concept.export_web_model`, 0.2 mm chord error) gave a 60 MB `media/model.glb` for this 7 m model; `cad/src/concept_media.py` passes 3 mm and 0.9 rad to the same exporter instead (about 19 MB). The hero render ran out of memory in the kit's `_tris` (a Python vector per vertex); `concept_media.py` reads the same mesh into numpy instead (peak 1.1 GB).
- The build123d SVG exporter stops on an `AssertionError` (an ellipse segment whose start and end differ) on some hidden-line arcs of the D3 model; `wsl_parts.svg_tolerant()` skips those segments in the repo's drawing scripts. Joint 3 of the build plan draws the sheave hanger plates only, because the cut head lug would not mesh.
- Repo bug found late and fixed: build123d centres a half torus on its own bounding box, so the chain links built from two half tori in `wsl_parts._link` came out 27 mm long instead of 40 mm and overlapped the shackles (`cad_check` caught 28 overlaps). Fixed with `align=None`; `cad_check` then passed and every output that shows chain (STL, GA, build plan overview, joints and steps, hero, exploded view, web model) was regenerated.
- Process slip: `python .kit/options.py --help` was run once to read its usage; the kit has no help flag, so it started the full Cycles options run. It was stopped after about a minute, before it wrote anything (no `media/options.png`, no other file changed). Only the `--export` run was then used.
- The README DOI badge carried an error message in place of the badge URL (commit f1019ca); repaired from the concept DOI in `CITATION.cff`.
- BOM line 4 asked for a "70 mm grip" clevis pin for a 37 mm lug pair; corrected to the pin length the model uses.

### Recommended next step

Amish to choose the concept and review the fixes. Then the coordinator renders the options picture, the product renders (RENDER_VIEWS: hero, studio, exploded, detail) and the cards on Amish's Mac. TRL 4 (proof-load, brake and dummy trials with a veterinarian and a co-design partner) stays on hold under the portfolio cap.
