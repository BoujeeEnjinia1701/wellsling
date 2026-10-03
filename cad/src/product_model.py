"""WellSling product appearance model (build123d), TRL 3, constructable design (WSL-DDR-002).

Finished-product look for photoreal renders, built from the constructable model: every component of
cad/src/model.py build_components() is used as it is (pads, stakes, foot plates and pins, the three
legs, head, sheave, winch on its bracket, spread chains, rope and hook, the H-frame spreader with its
bolts and shackles, adjusting chains, both webbing bands with felt sleeves, rim bearers, runners and
deck panels). Only the look is added, as recorded in docs/REVIEW.md: a safe working load label on
leg 1, a ground slab and brick well ring around a 3 m well, the 600 kg design animal hanging in the
bands at the landing height (clay massing from model.animal_context) and a 1.75 m mannequin standing
at the winch handle for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: Z up from the ground, the well axis on Z, leg 1 (winch leg) toward -60 deg.
Groups: "shell" (tripod, winch, rope and bridge), "internal" (spreader, bands and rigging),
"context" (ground, well, animal, mannequin).

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

TITLE = "WellSling: rim-worked animal lifting kit for open wells"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -35,
     "note": "Product render from the front right and above (about 22 deg elevation): the tripod over a 3 m well, "
             "the 600 kg design animal held in two webbing bands at the landing height over the slid-in bridge deck, "
             "1.75 m person standing at the winch handle for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 22, "az": -35,
     "note": "Exploded view from the front right and above (about 22 deg elevation): pads, stakes and foot plates, "
             "legs, head and sheave, winch and bracket, spread chains, rope and hook, spreader, chains and bands, "
             "rim bearers, runners and deck panels; well and animal not shown"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 15, "az": -50,
     "note": "Detail of the lifting rig from the front right, about 15 deg elevation: swivel hook, lift shackle, "
             "H-frame spreader, adjusting chains and the two plain webbing bands with felt sleeves"},
]

C_GALV = "#A9B0B8"       # hot-dip galvanised steel
C_ACCENT = "#0F766E"     # teal head and spreader paint
C_WINCH = "#C2410C"
C_CHAIN = "#5B6168"
C_ROPE = "#3B3F45"
C_BAND = "#E2A90F"       # yellow polyester webbing
C_FELT = "#8C8478"
C_WOOD = "#8A5A2B"
C_PLY = "#C49A5E"
C_HOOK = "#B91C1C"
C_LABEL = "#F4F4F2"
C_GROUND = "#9A8B74"
C_BRICK = "#9C5B3E"
C_CLAY = "#B9B4AC"

# model key: (display name, colour, material, group, BOM line, explode offset)
a1 = math.radians(M.PARAMS["legs_phi"][0])
E1 = (math.cos(a1), math.sin(a1))
LOOK = {
    "pads": ("Ground pads, hardwood", C_WOOD, "wood", "shell", 6, (0, 0, -300)),
    "stakes": ("Ground stakes", C_GALV, "metal", "shell", 7, (0, 0, -900)),
    "feet": ("Foot plates, galvanised", C_GALV, "metal", "shell", 5, (0, 0, 200)),
    "foot_pins": ("Foot pins", C_GALV, "metal", "shell", 4, (0, 0, 200)),
    "leg_1": ("Tripod leg 1 (winch leg), galvanised tube", C_GALV, "metal", "shell", 1, (0, 0, 600)),
    "leg_2": ("Tripod leg 2, galvanised tube", C_GALV, "metal", "shell", 1, (0, 0, 600)),
    "leg_3": ("Tripod leg 3, galvanised tube", C_GALV, "metal", "shell", 1, (0, 0, 600)),
    "bracket": ("Winch bracket", C_GALV, "metal", "shell", 10, (0, 0, 600)),
    "winch": ("Hand winch with load brake", C_WINCH, "painted", "shell", 9, (900 * E1[0], 900 * E1[1], 600)),
    "winch_bolts": ("Winch bolts M12", C_GALV, "metal", "shell", 10, (900 * E1[0], 900 * E1[1], 600)),
    "head": ("Tripod head, painted", C_ACCENT, "painted", "shell", 2, (0, 0, 1700)),
    "head_pins": ("Head pins", C_GALV, "metal", "shell", 4, (0, 0, 1700)),
    "sheave": ("Head sheave, 200 mm", C_WINCH, "painted", "shell", 3, (600 * E1[0], 600 * E1[1], 1400)),
    "axle": ("Sheave axle pin", C_GALV, "metal", "shell", 3, (600 * E1[0], 600 * E1[1], 1400)),
    "spread_chains": ("Spread chains, grade 80", C_CHAIN, "metal", "shell", 8, (0, 0, -500)),
    "rope": ("Wire rope, 8 mm", C_ROPE, "metal", "shell", 11, (0, 0, 600)),
    "hook": ("Swivel hook with latch", C_HOOK, "painted", "internal", 12, (0, 0, 800)),
    "lift_shackle": ("Lift shackle, 3.25 t", C_GALV, "metal", "internal", 16, (0, 0, 650)),
    "beam": ("Spreader main beam, painted", C_ACCENT, "painted", "internal", 13, (0, 0, 500)),
    "cross_bolts": ("Cross bar bolts M16", C_GALV, "metal", "internal", 15, (0, 0, 900)),
    "cross_bars": ("Spreader cross bars, painted", C_ACCENT, "painted", "internal", 14, (0, 0, 250)),
    "band_shackles": ("Band shackles, 1 t", C_GALV, "metal", "internal", 16, (0, 0, 0)),
    "adj_chains": ("Adjusting chains, grade 80", C_CHAIN, "metal", "internal", 17, (0, 0, 0)),
    "bands": ("Plain webbing bands, 240 mm", C_BAND, "fabric", "internal", 18, (0, 0, -250)),
    "felt": ("Felt sleeves, canvas cover", C_FELT, "fabric", "internal", 19, (0, 0, -500)),
    "bearers": ("Rim bearers, hardwood", C_WOOD, "wood", "shell", 25, (0, 0, -900)),
    "runners": ("Bridge runners, galvanised RHS", C_GALV, "metal", "shell", 26, (0, 0, -700)),
    "deck": ("Deck panels, grit-painted plywood", C_PLY, "wood", "shell", 27, (0, 0, -500)),
    "cleats": ("Deck cleats, hardwood", C_WOOD, "wood", "shell", 27, (0, 0, -500)),
}


def _label(p=M.PARAMS):
    """Safe working load label wrapped on leg 1, 1.6 m up from the foot pin."""
    D = M.derived(p)
    lg = M._leg_local(p, D)
    u = D["u"]
    c = M._add(D["F"], M._mul(u, -1600.0))
    c2 = M._add(D["F"], M._mul(u, -1800.0))
    band = M.rod(c, c2, p["tube"][0] / 2 + 1.0, p["tube"][0] / 2 - 0.5)
    return M.turn(band, p["legs_phi"][0])


def _site(p=M.PARAMS):
    r = p["well_d"] / 2
    ground = Pos(0, 0, -40) * (Cylinder(4300, 80) - Cylinder(r + 230, 90))
    ring = M.well_context(p, 1500)
    return ground, ring


def product_parts(p=M.PARAMS):
    comps = M.build_components(p)
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(explode)})

    for key, (name, color, mat, group, bom, ex) in LOOK.items():
        add(name, comps[key], color, mat, bom, group, ex)
    add("Safe working load label, 600 kg animal", _label(p), C_LABEL, "paper", None, "shell", (0, 0, 600))
    ground, ring = _site(p)
    add("Ground around the well", ground, C_GROUND, "clay", None, "context")
    add("Brick well ring, 3 m across", ring, C_BRICK, "clay", None, "context")
    add("Design animal, 600 kg (clay massing)", M.animal_context(p), C_CLAY, "clay", None, "context")
    from context_parts import mannequin
    # stand outboard of leg 1, beside the winch handle, facing the well
    D = M.derived(p)
    r, s = 2750.0, 480.0
    x = r * E1[0] - s * E1[1]
    y = r * E1[1] + s * E1[0]
    face = math.degrees(math.atan2(-y, -x)) + 90.0      # the mannequin faces -Y; turn it to face the well axis
    person = Pos(x, y, 0) * Rot(0, 0, face) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale), standing at the winch", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:50s} {q['group']:9s} {q['material']:8s} vol={s.volume / 1000:10.1f} cm3")
