# Review note: WellSling

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
