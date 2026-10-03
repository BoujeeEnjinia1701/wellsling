"""WellSling concept media (TRL 3, constructable design of WSL-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the kit's components from cad/src/model.py and renders the media set with .kit/concept.py:
media/hero.png, media/exploded.png, media/flow.png, media/concept-blueprint.png and .pdf
(WSL-DWG-010), media/model.glb and media/viewer.html. Every coloured part carries the BOM line
number used in bom/bom.csv. Grey context (the well shaft and the 600 kg design animal in the
hero) has no BOM number. Figures on the sheet and in the flow diagram come from
docs/04-calcs/sizing.py (WSL-CAL-001). CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build_components, derived, well_context, animal_context  # noqa: E402

D = derived(P)
C = build_components(P)


def fuse(*keys):
    s = None
    for k in keys:
        s = C[k] if s is None else s + C[k]
    return s


a1 = math.radians(P["legs_phi"][0])
E1 = (math.cos(a1), math.sin(a1))
parts = [
    Part("Tripod legs (3)", fuse("leg_1", "leg_2", "leg_3"), "#64748B", 1, (0, 0, 0)),
    Part("Tripod head", fuse("head", "head_pins"), "#0F766E", 2, (0, 0, 1100)),
    Part("Head sheave", fuse("sheave", "axle"), "#B45309", 3, (500 * E1[0], 500 * E1[1], 700)),
    Part("Foot plates (3)", fuse("feet", "foot_pins"), "#1D4ED8", 5, (0, 0, 350)),
    Part("Ground pads (3)", C["pads"], "#A16207", 6, (0, 0, -250)),
    Part("Ground stakes (6)", C["stakes"], "#374151", 7, (0, 0, -1000)),
    Part("Spread chains (3)", C["spread_chains"], "#78716C", 8, (0, 0, -500)),
    Part("Hand winch with load brake", fuse("winch", "winch_bolts"), "#C2410C", 9, (900 * E1[0], 900 * E1[1], 0)),
    Part("Winch bracket", C["bracket"], "#7C3AED", 10, (450 * E1[0], 450 * E1[1], 0)),
    Part("Wire rope, 8 mm", C["rope"], "#111827", 11, (0, 0, 0)),
    Part("Swivel hook", C["hook"], "#DC2626", 12, (0, 0, 300)),
    Part("Spreader main beam", fuse("beam", "lift_shackle"), "#0E7490", 13, (0, 0, 150)),
    Part("Spreader cross bars (2)", fuse("cross_bars", "cross_bolts"), "#15803D", 14, (0, 0, 0)),
    Part("Adjusting chains (4)", fuse("adj_chains", "band_shackles"), "#57534E", 17, (0, 0, -150)),
    Part("Webbing bands (2)", C["bands"], "#EAB308", 18, (0, 0, -350)),
    Part("Felt sleeves (2)", C["felt"], "#F5F5F4", 19, (0, 0, -600)),
    Part("Rim bearers (2)", C["bearers"], "#92400E", 25, (0, 0, -300)),
    Part("Bridge runners (3)", C["runners"], "#475569", 26, (0, 0, 0)),
    Part("Deck panels (3)", fuse("deck", "cleats"), "#D6A461", 27, (0, 0, 300)),
]

context = [
    Part("Well shaft, 3 m across (site)", well_context(P, 1200), "#D1D5DB"),
    Part("Design animal, 600 kg (scale)", animal_context(P, D), "#9CA3AF"),
]

render_all(
    parts, project="WellSling", title="Rim-worked animal lifting kit for open wells", dwg_no="WSL-DWG-010",
    key_figures=[f"Tripod: three 76.1 x 3.6 mm legs, {P['leg_L'] / 1000:.1f} m pin to pin, feet on a {2 * P['foot_r'] / 1000:.0f} m circle",
                 f"Head {D['z_top'] / 1000:.2f} m up; spans wells up to {P['well_d'] / 1000:.0f} m across, pads 0.7 m back from the rim",
                 "Safe working load 648 kg at the hook (600 kg animal); rope factor 6.1",
                 "Hand winch 1,000 kg, automatic load brake; crank 196 N at most",
                 "Two plain webbing bands, 240 mm wide, on an H-frame spreader",
                 "Landing bridge: 3 runners, 3 deck panels; never swung over the rim",
                 "Kit about 550 kg; heaviest piece 32 kg; about USD 2,780 (estimate)"],
    cut=False, context=context,
    flow={"title": "energy to lift the design animal 17.6 m, from 15 m down to the landing height, kJ (WSL-CAL-001 estimates)",
          "unit": "kJ",
          "stages": [("Crank work, crew taking turns", 144), ("Winch drum output", 115), ("Rope at the hook", 112),
                     ("Animal and rigging raised", 112)],
          "losses": [(0, "Gears and load brake (20 %)", 29), (1, "Head sheave (3 %)", 3)]},
)
print("wrote media/hero.png, exploded.png, flow.png, concept-blueprint.png and .pdf, model.glb, viewer.html")
