"""WellSling concept media (TRL 3, constructable design of WSL-DDR-002 with the kit 1.9.1 fixes of WSL-DDR-004),
generated from the detailed (D3) parametric model.

Run from the repo root:
    python cad/src/concept_media.py [hero|exploded|flow|blueprint|web ...]   (default: all of them; one per process
                                             keeps memory down on a large D3 model)
Takes the kit's component groups from cad/src/model.py (build_components(), every bolt, pin, link and weld of
option A) and renders the media set with .kit/concept.py. Every coloured part carries the BOM line number used in
bom/bom.csv. Grey context (the well shaft and the 600 kg design animal in the hero) has no BOM number. Figures on
the sheet and in the flow diagram come from docs/04-calcs/sizing.py (WSL-CAL-001). CONCEPT, NOT FOR FABRICATION.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import concept as K  # noqa: E402
from concept import Part, render_all  # noqa: E402
from build123d import Pos  # noqa: E402
from model import PARAMS as P, build_components, derived, well_context, animal_context  # noqa: E402

PROJECT, TITLE = "WellSling", "Rim-worked animal lifting kit for open wells"
D = derived(P)
C = build_components(P)
ROWS = list(csv.DictReader((ROOT / "docs/04-calcs/results.csv").open()))
R = {r["tag"]: float(r["value"]) for r in ROWS if r["value"]}
KIT_KG = re.search(r"whole kit about (\d+) kg", next(r["result"] for r in ROWS if r["tag"] == "G1")).group(1)


def fuse(*keys):
    from build123d import Compound
    return Compound([C[k] for k in keys])


a1 = math.radians(P["legs_phi"][0])
E1 = (math.cos(a1), math.sin(a1))


def parts():
    return [
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
        Part("Band end yokes (4)", C["yokes"], "#9333EA", 29, (0, 0, -250)),
        Part("Webbing bands (2)", C["bands"], "#EAB308", 18, (0, 0, -350)),
        Part("Felt sleeves (2)", C["felt"], "#F5F5F4", 19, (0, 0, -600)),
        Part("Rim bearers (2)", C["bearers"], "#92400E", 25, (0, 0, -300)),
        Part("Bridge runners (3)", C["runners"], "#475569", 26, (0, 0, 0)),
        Part("Deck panels (3)", fuse("deck", "cleats"), "#D6A461", 27, (0, 0, 300)),
    ]


def _ground():
    """Ground round the well mouth, 30 mm thick with its top at z = 0, so the pads and the person stand on it."""
    from build123d import Cylinder, Pos
    return Pos(0, 0, -15) * (Cylinder(4800, 30) - Cylinder(P["well_d"] / 2, 32))


def _person():
    """1.75 m person standing on the ground at the winch handle, as in the product model."""
    rr, s = 2750.0, 520.0
    return K.human_figure(1750, x=rr * E1[0] - s * E1[1], y=rr * E1[1] + s * E1[0], z=0.0)


context = [
    Part("Ground round the well (site)", _ground(), "#E7E5E4"),
    Part("Well shaft, 3 m across (site)", Pos(0, 0, -5) * well_context(P, 700), "#D1D5DB"),
    Part("Design animal, 600 kg (scale)", animal_context(P, D), "#9CA3AF"),
]

MD = ROOT / "media"
ROUND = ("chain", "shackle", "hook", "Thimble", "rope", "Wire rope")


def key_figures():
    return [f"Tripod: three 88.9 x 3.2 mm legs, {P['leg_L'] / 1000:.1f} m pin to pin, feet on a {2 * P['foot_r'] / 1000:.0f} m circle",
            f"Head {D['z_top'] / 1000:.2f} m up; spans wells up to {P['well_d'] / 1000:.0f} m across, pads 0.7 m back from the rim",
            f"Safe working load {R['A2'] * 1000 / 9.81:.0f} kg at the hook (600 kg animal); rope factor {R['B1']:.1f}",
            f"Hand winch 1,000 kg, automatic load brake; crank {R['B6']:.0f} N at most",
            "Two plain webbing bands, 240 mm wide, on band end yokes and an H-frame spreader",
            "Landing bridge: 3 runners, 3 deck panels; never swung over the rim",
            f"Kit about {KIT_KG} kg; heaviest piece {R['G1']:.0f} kg; about USD {R['G2']:,.0f} (estimate)"]


def _np_tris(shape, tol=1.0):
    """Triangles of a shape as numpy arrays, read straight from its mesh (every model part is premeshed by
    wsl_parts.premesh). The kit's _tris builds a Python Vector per vertex, which on this D3 model (every chain link
    meshed) ran the hero render out of memory; this reads the same mesh with a fraction of the memory."""
    import numpy as np
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopoDS import TopoDS
    w = shape.wrapped
    BRepMesh_IncrementalMesh(w, tol, False, 0.5, True)   # meshes only faces that have no mesh yet
    vs, ts, n0 = [], [], 0
    ex = TopExp_Explorer(w, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()) if hasattr(TopoDS, "Face") else TopoDS.Face_s(ex.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(f, loc)
        if tri is not None:
            trsf = loc.Transformation()
            nn = tri.NbNodes()
            v = np.empty((nn, 3))
            for i in range(nn):
                p = tri.Node(i + 1).Transformed(trsf)
                v[i] = (p.X(), p.Y(), p.Z())
            t = np.empty((tri.NbTriangles(), 3), dtype=np.int64)
            rev = f.Orientation() == TopAbs_REVERSED
            for i in range(tri.NbTriangles()):
                a, b, c = tri.Triangle(i + 1).Get()
                t[i] = (a, c, b) if rev else (a, b, c)
            vs.append(v); ts.append(t - 1 + n0); n0 += nn
        ex.Next()
    if not vs:
        return np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int64)
    return np.vstack(vs), np.vstack(ts)


K._tris = _np_tris


def web_model():
    """Web model (media/model.glb and viewer.html) through the kit exporter. The kit's 0.2 mm chord error gives about
    60 MB on this 7 m D3 model (every chain link is meshed), so the export here uses 3 mm and 0.9 rad, which keeps the
    file under 20 MB (about 19 MB) while the links, pins and welds stay visible."""
    import build123d
    real = build123d.export_gltf

    def coarse(shape, path, unit=None, binary=False, linear_deflection=0.001, angular_deflection=0.1):
        kw = {} if unit is None else {"unit": unit}
        return real(shape, path, binary=binary, linear_deflection=3.0, angular_deflection=0.9, **kw)

    build123d.export_gltf = coarse
    try:
        return K.export_web_model(parts(), "media", title=f"{PROJECT}: {TITLE}")
    finally:
        build123d.export_gltf = real


def flow_spec():
    E_lift = round(R["B9"])                       # kJ into raising the animal and rigging
    E_crank = round(R["B9"] / (0.80 * 0.97))
    drum = round(R["B9"] / 0.97)
    return {"title": "energy to lift the design animal 18.2 m, from 15 m down to the landing height, kJ (WSL-CAL-001 estimates)",
            "unit": "kJ",
            "stages": [("Crank work, crew taking turns", E_crank), ("Winch drum output", drum), ("Rope at the hook", E_lift),
                       ("Animal and rigging raised", E_lift)],
            "losses": [(0, "Gears and load brake (20 %)", E_crank - drum), (1, "Head sheave (3 %)", drum - E_lift)]}


def blueprint():
    """Blueprint concept sheet WSL-DWG-010. Hidden-line views of every chain link and fastener exhaust memory, so the
    sheet draws the made and bought parts without the round rigging, fasteners and welds."""
    import datetime
    from build123d import Compound
    from drawing import Sheet, project_views
    import wsl_parts
    wsl_parts.svg_tolerant()
    import model as M
    lean = [q["shape"] for q in M.option_a(P) if q["kind"] in ("made", "bought") and not any(k in q["name"] for k in ROUND)]
    views = project_views(Compound(lean), MD / "_views")
    date = datetime.date.today().isoformat()
    s = Sheet(project=PROJECT, title=TITLE, dwg_no="WSL-DWG-010", rev="P2", author="Amish Chadha", date=date, theme="blueprint",
              material="Concept model; chains, rope, shackles, fasteners and welds not drawn",
              revisions=[("P2", "Concept sheet from the D3 model", date, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Key figures", key_figures(), x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    import shutil
    shutil.rmtree(MD / "_views", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": lambda: K._render(parts() + context + [_person()], MD / "hero.png", title=PROJECT,
                                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person at the winch, for scale"),
           "exploded": lambda: K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                                         note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv"),
           "flow": lambda: K.flow_diagram(flow_spec()["stages"], MD / "flow.png", f"{PROJECT}: {flow_spec()['title']}", "kJ", flow_spec()["losses"]),
           "web": web_model,
           "blueprint": blueprint}
    for w in sys.argv[1:] or ["hero", "exploded", "flow", "blueprint", "web"]:
        print(w, "->", fns[w]())
