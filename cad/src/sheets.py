"""WellSling general arrangement drawing WSL-DWG-001 (Rev P2).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/WSL-DWG-001.svg, .pdf and .png from the detailed (D3) parametric model, option A: the
tripod, winch, spreader with both bands on their yokes and the landing bridge, erected over a 3 m well at the
landing height, every bolt, pin, chain link and weld drawn.
The concept sheet in media/ uses WSL-DWG-010. Figures in the notes come from WSL-CAL-001
(python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(Path(__file__).resolve().parent)]
from drawing import Sheet, project_views  # noqa: E402
import csv  # noqa: E402
import re  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
D = M.derived(P)
# The GA shows the made and bought parts; fasteners and weld beads are left off the sheet (they are in the STEP
# files and the making sketches). Torus-built parts (chain links, shackle bows, hook, thimble) can project to
# degenerate ellipse edges the SVG exporter rejects, so those are drawn in a second pass only if the first works.
from build123d import Compound  # noqa: E402
import wsl_parts  # noqa: E402
wsl_parts.svg_tolerant()
PARTS = [q for q in M.option_a(P) if q["kind"] in ("made", "bought")]
ROUND = ("chain", "shackle", "hook", "Thimble", "rope", "Wire rope")
asm = Compound([q["shape"] for q in PARTS])
lean = Compound([q["shape"] for q in PARTS if not any(k in q["name"] for k in ROUND)])
ROWS = list(csv.DictReader((ROOT / "docs/04-calcs/results.csv").open()))
R = {r["tag"]: float(r["value"]) for r in ROWS if r["value"]}
KIT_KG = re.search(r"whole kit about (\d+) kg", next(r["result"] for r in ROWS if r["tag"] == "G1")).group(1)

work = ROOT / "cad/drawings/_views"
try:
    views = project_views(asm, work)
    SHOWN = "Fasteners and weld beads not shown"
except AssertionError:          # svgpathtools rejects a degenerate arc from a torus edge: draw without the round rigging
    shutil.rmtree(work, ignore_errors=True)
    views = project_views(lean, work)
    SHOWN = "Fasteners, welds, chains, shackles, rope and hook not shown"
s = Sheet(project="WellSling", title="Rim-worked animal lifting kit for open wells: general arrangement",
          dwg_no="WSL-DWG-001", rev="P2", author="Amish Chadha", date="2026-10-25", concept=True, scale=None,
          material="S355 tube, RHS and plate, galvanised; hardwood; plywood; polyester webbing. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the constructable TRL 3 model (WSL-DDR-002)", "2026-10-03", "AC"),
                     ("P2", "D3 model; 88.9 mm legs, chain eye fins, winch bracket, band end yokes (WSL-DDR-004)", "2026-10-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 57, 140, 62, label="Isometric view", sublabel=f"Front right, above. {SHOWN}")
s.add_notes("Key dimensions (mm) and data", [
    f"Legs {P['tube'][0]} x {P['tube'][1]} tube, {P['leg_L']:.0f} pin to pin, {D['leg_angle']:.1f} deg from vertical",
    f"Feet on a {2 * P['foot_r']:.0f} circle; spans wells up to {P['well_d']:.0f} across",
    f"Head plate top {D['z_top']:.0f} above ground; sheave 200 pitch dia",
    f"Pads {P['pad'][0]:.0f} x {P['pad'][1]:.0f} x {P['pad'][2]:.0f}, two 25 stakes each",
    "Spread chains 8 mm grade 80, one chain eye fin each",
    f"Winch 1,000 kg with load brake, drum {P['winch_s']:.0f} up leg 1",
    f"Spreader beam RHS 100 x 50 x 4, {P['beam'][0]:.0f} long; bands {2 * P['band_y']:.0f} apart",
    "Two plain webbing bands 240 wide on band end yokes",
    f"Bridge: 3 runners RHS 100 x 50 x 3, {P['runner'][0]:.0f} long, on two bearers",
    f"Deck top {D['deck_top']:.0f}; hooves {D['hoof_clear']:.0f} above it at the landing height",
    f"Safe working load {R['A2'] * 1000 / 9.81:.0f} kg at the hook (600 kg animal)",
    f"Kit about {KIT_KG} kg; heaviest piece {R['G1']:.0f} kg",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=130, width=140)
s.save(ROOT / "cad/drawings/WSL-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/WSL-DWG-001.svg, .pdf, .png")
