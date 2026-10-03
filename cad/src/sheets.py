"""WellSling general arrangement drawing WSL-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/WSL-DWG-001.svg, .pdf and .png from the parametric model: the tripod, winch,
spreader with both bands and the landing bridge, erected over a 3 m well at the landing height.
The concept sheet in media/ uses WSL-DWG-010. Figures in the notes come from WSL-CAL-001
(python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(Path(__file__).resolve().parent)]
from drawing import Sheet, project_views  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
D = M.derived(P)
C = M.build_components(P)
asm = M.assembly(P, C)

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
s = Sheet(project="WellSling", title="Rim-worked animal lifting kit for open wells: general arrangement",
          dwg_no="WSL-DWG-001", rev="P1", author="Amish Chadha", date="2026-10-03", concept=True, scale=None,
          material="S355 tube, RHS and plate, galvanised; hardwood; plywood; polyester webbing. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the constructable TRL 3 model (WSL-DDR-002)", "2026-10-03", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 57, 140, 62, label="Isometric view", sublabel="Seen from the front right, above; well not shown")
s.add_notes("Key dimensions (mm) and data", [
    f"Legs 76.1 x 3.6 tube, {P['leg_L']:.0f} pin to pin, {D['leg_angle']:.1f} deg from vertical",
    f"Feet on a {2 * P['foot_r']:.0f} circle; spans wells up to {P['well_d']:.0f} across",
    f"Head plate top {D['z_top']:.0f} above ground; sheave 200 pitch dia",
    f"Pads {P['pad'][0]:.0f} x {P['pad'][1]:.0f} x {P['pad'][2]:.0f}, two 25 stakes each",
    "Spread chains 8 mm grade 80 between the three feet",
    f"Winch 1,000 kg with load brake, drum {P['winch_s']:.0f} up leg 1",
    f"Spreader beam RHS 100 x 50 x 4, {P['beam'][0]:.0f} long; bands {2 * P['band_y']:.0f} apart",
    "Two plain webbing bands 240 wide, felt sleeves",
    f"Bridge: 3 runners RHS 100 x 50 x 3, {P['runner'][0]:.0f} long, on two bearers",
    f"Deck top {D['deck_top']:.0f}; hooves {D['hoof_clear']:.0f} above it at the landing height",
    "Safe working load 648 kg at the hook (600 kg animal)",
    "Kit about 550 kg; heaviest piece 32 kg",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=130, width=140)
s.save(ROOT / "cad/drawings/WSL-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/WSL-DWG-001.svg, .pdf, .png")
