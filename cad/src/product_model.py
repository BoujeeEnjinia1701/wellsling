"""WellSling product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is, at detail level D3: the three 88.9 mm
legs with their caps, tongues and welds, the head weldment, the sheave and its axle, the leg pins and R-clips,
the staked foot plates with their chain eye fins on hardwood pads, the spread chains link by link with their
shackles, the winch on its bracket with its bolts, the rope and its coil, the swivel hook, the H-frame spreader
with sleeves, lug, bolts and shackles, the adjusting chains, band end yokes, webbing bands and felt sleeves, the
landing bridge (bearers, runners, deck panels, cleats and screws) and the passer laid on the ground. Only the
context is added: an old brick well lining round a 3 m open well, flush with the ground, with the dark of the shaft at ground level, the
600 kg design animal hanging in the bands at the landing height (clay massing from model.animal_context), and a
1.75 m mannequin standing at the winch handle for scale. Ground level is model z = 0 (photoreal --ground-z=0);
every site part reaches below it.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (every product part), "rig" (the spreader, chains, yokes, bands and sleeves, for the detail
view), "context" (site, animal and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "WellSling: rim-worked animal lifting kit for open wells"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=42,-55", "--lens=35"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 20, "az": -35, "args": _SITE,
     "note": "Site render from the front right and a little above (about 20 deg elevation): the tripod over a 3 m open well "
             "with an old brick lining, the 600 kg design animal held in two webbing bands at the landing height over the slid-in "
             "bridge deck, the passer laid on the ground, and a 1.75 m person standing at the winch handle for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render from the front right and above (about 24 deg elevation): tripod, winch on leg 1, staked feet with "
             "spread chains, rope and hook, H-frame spreader with chains, band end yokes and bands, landing bridge and passer"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 22, "az": -35,
     "note": "Exploded view from the front right and above (about 22 deg elevation): pads, stakes and foot plates, legs, head "
             "and sheave, winch and bracket, spread chains, rope and hook, spreader, chains, yokes and bands, rim bearers, "
             "runners and deck panels"},
    {"name": "detail", "groups": ["rig"], "explode": False, "el": 15, "az": -50,
     "note": "Detail of the lifting rig from the front right, about 15 deg elevation: swivel hook, lift shackle, H-frame "
             "spreader, adjusting chains, band end yokes and the two plain webbing bands with felt sleeves"},
]

a1 = math.radians(M.PARAMS["legs_phi"][0])
E1 = (math.cos(a1), math.sin(a1))
EXPLODE = {   # component group: explode offset (mm)
    "pads": (0, 0, -300), "stakes": (0, 0, -900), "feet": (0, 0, 200), "foot_pins": (0, 0, 200),
    "leg_1": (0, 0, 600), "leg_2": (0, 0, 600), "leg_3": (0, 0, 600), "bracket": (0, 0, 600),
    "winch": (900 * E1[0], 900 * E1[1], 600), "winch_bolts": (900 * E1[0], 900 * E1[1], 600),
    "head": (0, 0, 1700), "head_pins": (0, 0, 1700), "sheave": (600 * E1[0], 600 * E1[1], 1400),
    "axle": (600 * E1[0], 600 * E1[1], 1400), "spread_chains": (0, 0, -500), "rope": (0, 0, 600),
    "hook": (0, 0, 800), "lift_shackle": (0, 0, 650), "beam": (0, 0, 500), "cross_bolts": (0, 0, 900),
    "cross_bars": (0, 0, 250), "band_shackles": (0, 0, 0), "adj_chains": (0, 0, 0), "yokes": (0, 0, -100),
    "bands": (0, 0, -250), "felt": (0, 0, -500), "bearers": (0, 0, -900), "runners": (0, 0, -700),
    "deck": (0, 0, -500), "cleats": (0, 0, -500), "passer": (0, -600, 0),
}
RIG = ("hook", "lift_shackle", "beam", "cross_bars", "cross_bolts", "band_shackles", "adj_chains", "yokes", "bands", "felt")


def site(P=M.PARAMS):
    """Old brick lining round the well, flush with the ground (10 mm proud) and reaching 1.5 m down, the dark of the shaft at ground
    level (the procedural ground has no hole), the design animal and a mannequin at the winch."""
    r = P["well_d"] / 2
    out = []
    kerb = Pos(0, 0, (10 - 1500) / 2) * (Cylinder(r + 230, 1510) - Cylinder(r, 1512))
    out.append(part("Brick well lining, 3 m well (site)", kerb, "concrete", kind="context", group="context", color="#9C5B3E"))
    shaft = Pos(0, 0, -40) * Cylinder(r - 2, 90)
    out.append(part("Dark of the well shaft (site)", shaft, "matte_black", kind="context", group="context"))
    out.append(part("Design animal 600 kg, clay massing (scale)", M.animal_context(P), "skin", kind="context", group="context"))
    try:
        from context_parts import mannequin
        rr, s = 2750.0, 520.0
        x = rr * E1[0] - s * E1[1]
        y = rr * E1[1] + s * E1[0]
        face = math.degrees(math.atan2(-y, -x)) + 90.0      # the mannequin faces -Y; turn it to face the well axis
        man = Pos(x, y, 0) * Rot(0, 0, face) * mannequin(1750, "stand")
        out.append(part("Person 1.75 m, standing at the winch (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts(P=M.PARAMS):
    out = []
    for q in M.components(M.CHOSEN):
        if q["kind"] == "context":
            continue
        r = dict(q)
        r["group"] = "shell"
        r["explode"] = EXPLODE.get(q.get("key"), (0, 0, 0))
        out.append(r)
        if q.get("key") in RIG:
            g = dict(r); g["group"] = "rig"; g["name"] = q["name"] + " (rig view)"
            out.append(g)
    return out + site(P)


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "rig" for p in ps), "rig,",
          sum(p["group"] == "context" for p in ps), "context")
