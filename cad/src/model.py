"""WellSling parametric model (build123d), kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check of every option, STEP per part (chosen option) and per assembly
    python cad/src/model.py               constructability checks of option A, part list with masses, STL of option A
    python cad/src/model.py --check       constructability checks only

WellSling is a rim-worked kit for lifting a fallen cow, buffalo or calf out of an open well without anyone going
down. Concept options (WSL-OPT-001; option A is the design carried since kit 1.7, the choice awaits Amish):
    A  tripod and hand winch: a steel tripod of its own (three 88.9 mm legs pinned to a head plate, a 200 mm head
       sheave and a spur-gear hand winch with an automatic load brake on leg 1), staked feet on timber pads tied by
       spread chains, an H-frame spreader with two plain webbing bands (chest and flank) on chains and band end yokes,
       and a landing bridge of three steel runners and plywood deck panels slid across the well mouth
    B  portable gantry and two chain hoists: a sectioned box beam on two pinned A-frames straddles the well; one hand
       chain hoist per band lifts the chest and the flank on separate lines; same bands, yokes and landing bridge
    C  sheerlegs and draught haul: two pinned legs lean over the well, held by a back guy to a staked ground anchor;
       the rope runs from a block at the apex through a snatch block at the feet to a tractor, with two turns on a
       staked snubbing post as the brake; same spreader, bands and landing bridge

Coordinates in mm. Z up, ground at Z = 0, the well axis on the Z axis. Option A: leg 1 (the winch leg) points at
-60 deg, legs 2 and 3 at +60 and 180 deg; each leg-related part is built in a leg-local frame (X radial, outward;
Y tangential, counter-clockwise; Z up) and turned about Z. The landing bridge runners run along Y.

Every part is a cad_parts.part() dict with a "key" naming its component group (the groups the calculation note,
the drawings and the build plan pictures use: build_components() returns them as compounds). BOM line numbers are
given for the chosen option. Design changes made in the kit 1.9.1 upgrade are recorded in WSL-DEC-001 (D10 to D14, D17 and D18; WSL-DDR-004).
PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for _p in (str(HERE), str(ROOT / ".kit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from build123d import (Box, Cylinder, Location, Plane, Pos, Rot, Solid, Torus, Compound,  # noqa: E402
                       export_step, export_stl)
import cad_parts as cp  # noqa: E402
import wsl_parts as W  # noqa: E402

TITLE = "WellSling"

PARAMS = {
    # site and tripod geometry
    "well_d": 3000.0,          # largest well the design case covers (PR-005)
    "foot_r": 2500.0,          # radius of the foot pin circle about the well axis
    "leg_L": 4500.0,           # leg, head pin to foot pin
    "legs_phi": (-60.0, 60.0, 180.0),
    "head_pin_r": 110.0,       # radius of the head pins about the axis
    "head_pin_drop": 55.0,     # head pin centre below the head plate underside
    "foot_pin_z": 120.0,       # foot pin centre above the ground
    # leg (WSL-DEC-001 D10, 2026-10-25: 88.9 x 3.2 in place of 76.1 x 3.6 after the STEM check, S12)
    "tube": (88.9, 3.2),       # OD x wall, galvanised structural steel
    "cap_t": 8.0,              # end cap disc welded on each tube end
    "cap_d": 100.0,            # end cap diameter: 5.5 mm proud of the tube all round for the fillet weld
    "tongue": (60.0, 16.0, 90.0),   # width x thickness x length (cap face to tongue end)
    "pin_from_cap": 60.0,      # pin centre from the cap face
    "pin_d": 20.0, "hole_d": 21.0,
    "pin_grip": 24.0,          # clevis pin: head to split pin hole less one diameter (cad_parts.clevis_pin)
    # head
    "head_d": 440.0, "head_t": 12.0,
    "lug_t": 10.0, "lug_gap": 17.0,
    "head_lug": (110.0, 85.0),      # radial length x drop below the head plate
    # sheave and rope
    "rope_d": 8.0,
    "sheave_pitch_r": 100.0, "sheave_hub_r": 96.0, "sheave_flange_r": 115.0, "sheave_w": 30.0,
    "sheave_s": 80.0,          # tangential offset of the sheave plane from leg 1's plane
    "sheave_zc": -125.0,       # sheave centre below the head plate underside
    "hanger": (120.0, 10.0),   # hanger plate width x thickness
    "axle_d": 25.0,
    "fall_top": 800.0,         # rope fall from the sheave centre to the thimble top, nominal lift
    # winch on leg 1 (WSL-DEC-001 D12: bracket 300 x 300 and the winch 140 mm to the side, so every bolt clears the tube)
    "winch_s": 900.0,          # winch drum centre along leg 1 from the foot pin
    "bracket": (300.0, 300.0, 10.0),   # along leg x tangential x thickness
    "bracket_s": 110.0,        # bracket centre, tangential offset from leg 1's plane
    "winch_s0": 140.0,         # winch base and bolt pattern centre, tangential offset
    "winch_bolts": (160.0, 160.0),     # bolt pattern, along leg x tangential
    "drum_axis": 175.0,        # drum axis outward of leg 1's axis
    "drum_r": 50.0, "drum_flange_r": 110.0,
    "crank_arm": 300.0,
    # foot (WSL-DEC-001 D11: two chain eye fins, one per spread chain)
    "foot_plate": (260.0, 260.0, 10.0),
    "foot_lug": (100.0, 90.0),     # radial length x height above the foot plate
    "pad": (600.0, 300.0, 50.0),   # timber ground pad, radial x tangential x thickness
    "stake": (25.0, 760.0), "stake_s": 85.0, "stake_hole": 28.0,
    "eye": (60.0, 12.0, 45.0),     # chain eye fin: length along its chain x thickness x height
    "fin_x": 80.0, "fin_s": 60.0,  # fin centre in from the foot pin circle, and to the side
    "eye_hole_z": 24.0,            # fin hole centre above the foot plate top
    "chain_d": 20.0,               # envelope diameter of 8 mm chain (legacy drawings)
    # spreader
    "beam": (1100.0, 100.0, 50.0, 4.0),   # length (Y) x height x width x wall, RHS
    "sleeve": (26.9, 3.2), "sleeve_y": (300.0, 400.0, 500.0),
    "cross": (760.0, 50.0, 3.0),   # length (X) x size x wall, SHS
    "cross_plate": (100.0, 160.0, 10.0),  # X x Y x thickness, welded on the cross bar top
    "band_y": 450.0,               # half the band spacing (cross bars on sleeves 400 and 500)
    "lift_lug": (300.0, 110.0, 20.0),     # Y x height x thickness (110 tall: the hook clears its top edge, WSL-DEC-001 D17)
    "lift_holes": (-100.0, -50.0, 0.0, 50.0, 100.0), "lift_hole_d": 22.0, "lift_hole_z": 80.0,
    "tip_lug": (60.0, 70.0, 10.0),  # X x height x thickness, under each cross bar tip
    "band": (240.0, 6.0, 2000.0),   # width x thickness x effective length
    "band_r": 354.0,                # band wrap radius under the animal
    "chain_len": 200.0,             # adjusting chain in use, shackle bow to shackle bow (200 to 1,000)
    # bow shackles (catalogue class): pin diameter, jaw width, inside length
    "shackle_1t": (11.0, 16.0, 37.0), "shackle_2t": (16.0, 20.6, 48.0), "shackle_325t": (19.0, 27.0, 60.0),
    # band end yoke (WSL-DEC-001 D13): removable 25 mm bar through the band's sewn eye, side plates, welded top bar, lug
    "yoke_bar_d": 25.0, "yoke_gap": 100.0, "yoke_plate": (40.0, 10.0, 150.0), "yoke_inside": 258.0,
    # landing bridge
    "runner": (4500.0, 100.0, 50.0, 3.0),   # length (Y) x height x width x wall, RHS
    "runner_x": (-500.0, 0.0, 500.0),
    "bearer": (1400.0, 200.0, 100.0),       # X x Y x thickness, hardwood
    "bearer_y": 2000.0,
    "deck": (1220.0, 1500.0, 25.0),         # X x Y x thickness, exterior plywood
    "cleat": (45.0, 45.0, 1400.0), "cleat_x": (-250.0, 250.0),
    # passer
    "pole": (40.0, 2.0, 2000.0),            # aluminium tube OD x wall x section length
    "spigot": (35.5, 250.0),                # spigot OD x length (100 inside, 150 out)
    "jhead_r": 400.0, "jhead_tube": 26.9,
    # option B: portable gantry with two chain hoists
    "B_frame_y": 2700.0,          # A-frame planes either side of the well
    "B_foot_x": 1100.0,           # A-frame feet either side of the beam line
    "B_beam": (140.0, 80.0, 4.0), # RHS height x width x wall
    "B_beam_L": 5800.0,           # three sections spliced at +/- B_splice_y
    "B_splice_y": 967.0,
    "B_leg": (60.0, 3.0),         # SHS A-frame legs
    "B_brace": (40.0, 3.0),       # SHS knee braces
    "B_tie_z": 1500.0,            # A-frame mid tie height
    # option C: sheerlegs, back guy, draught haul
    "C_foot_x": 1000.0, "C_foot_y": -2400.0,   # sheerleg feet
    "C_apex": (0.0, 0.0),         # apex pin over the well axis (x, y)
    "C_anchor_y": -7000.0,        # back guy ground anchor
    "C_post_y": -4800.0,          # snubbing post
}
P = PARAMS

OPTIONS = {"A": "Tripod and hand winch", "B": "Portable gantry and chain hoists", "C": "Sheerlegs and draught haul"}
PRINCIPLES = {
    "A": "A steel tripod of its own carries a sheave over the well; a braked hand winch on one leg raises two webbing "
         "bands on an H-frame spreader, and a bridge is slid under the animal to land it.",
    "B": "A sectioned box beam on two pinned A-frames spans the well; one hand chain hoist per band lifts the chest and "
         "the flank on separate lines, and the same bridge is slid under to land it.",
    "C": "Two pinned legs lean over the well on a back guy; a tractor hauls the rope through a block at the apex and a "
         "snatch block at the feet, with turns on a snubbing post as the brake.",
}
CHOSEN = "A"
OPTION_VIEWS = {"A": {"el": 20, "az": -50, "scale": "person", "ground_z": 0},
                "B": {"el": 20, "az": -50, "scale": "person", "ground_z": 0},
                "C": {"el": 18, "az": -60, "scale": "person", "ground_z": 0}}
# Contacts that are meant: weld beads fuse into the parent metal; a split pin or R-clip sits in its cross hole; the
# wire rope runs onto its own coil on the drum; a bush sits on its axle; a band's sewn eye wraps the yoke bar.
ALLOWED_CONTACTS = [("Weld", ""), ("R-clip", ""), ("Split pin", ""), ("Wire rope", "Wire rope"),
                    ("bush", "axle"), ("Webbing band", "band end bar"), ("Felt sleeve", "Webbing band")]

DENSITY = {"steel": 7.85e-6, "aluminium": 2.70e-6, "hardwood": 0.75e-6, "plywood": 0.60e-6,
           "polyester": 1.38e-6, "felt": 0.30e-6}
GALV, STEEL, CHAIN, WOOD, PLY, BAND, ALU = "galvanised", "mild_steel", "mild_steel", "hardwood", "plywood", "canvas", "aluminium"
C_BAND, C_FELT, C_WINCH, C_HOOK, C_CHAIN = "#E2A90F", "#8C8478", "#C2410C", "#B91C1C", "#4B5056"


# ----------------------------------------------------------------- vector helpers (legacy names kept)
def _v(*a):
    return tuple(float(x) for x in a)


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _mul(a, k):
    return tuple(x * k for x in a)


def _norm(a):
    n = math.sqrt(sum(x * x for x in a))
    return tuple(x / n for x in a)


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rod(p0, p1, r, r_in=0.0):
    """Solid cylinder (or tube) between two points."""
    d = _sub(p1, p0)
    L = math.sqrt(_dot(d, d))
    pl = Plane(origin=p0, z_dir=_norm(d))
    s = Solid.make_cylinder(r, L, pl)
    if r_in > 0:
        s = s - Solid.make_cylinder(r_in, L, pl)
    return s


def turn(shape, phi):
    return Rot(0, 0, phi) * shape


def _rotz(v, phi):
    a = math.radians(phi)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a), v[2])


def ybore(center, d, length=400.0):
    return rod(_add(center, (0, -length / 2, 0)), _add(center, (0, length / 2, 0)), d / 2)


# ----------------------------------------------------------------- derived geometry
def derived(P=PARAMS):
    D = {}
    run = P["foot_r"] - P["head_pin_r"]
    rise = math.sqrt(P["leg_L"] ** 2 - run ** 2)
    D["run"], D["rise"] = run, rise
    D["leg_angle"] = math.degrees(math.asin(run / P["leg_L"]))       # from vertical
    D["z_hp"] = P["foot_pin_z"] + rise
    D["z_u"] = D["z_hp"] + P["head_pin_drop"]                         # head plate underside
    D["z_top"] = D["z_u"] + P["head_t"]
    D["u"] = _norm((run, 0.0, -rise))          # leg-local, head pin toward foot pin
    D["n"] = (-D["u"][2], 0.0, D["u"][0])      # leg-local outward normal in the leg plane
    D["F"] = (P["foot_r"], 0.0, P["foot_pin_z"])
    D["Hp"] = (P["head_pin_r"], 0.0, D["z_hp"])
    n, u = D["n"], D["u"]
    zc = D["z_u"] + P["sheave_zc"]
    axis_c = _dot(D["Hp"], n)
    D["rope_offset"] = P["drum_axis"] - P["drum_r"] - P["rope_d"] / 2   # rope leaves the bare drum on the leg side
    target = axis_c + D["rope_offset"] - P["sheave_pitch_r"]
    xc = (target - n[2] * zc) / n[0]
    D["sheave_c"] = (xc, P["sheave_s"], zc)    # leg 1 local
    D["drop_local"] = (xc - P["sheave_pitch_r"], P["sheave_s"])
    phi = math.radians(P["legs_phi"][0])
    x, s = D["drop_local"]
    D["drop"] = (x * math.cos(phi) - s * math.sin(phi), x * math.sin(phi) + s * math.cos(phi))
    D["drop_off"] = math.hypot(*D["drop"])
    D["tan_out"] = _add(D["sheave_c"], _mul(n, P["sheave_pitch_r"]))
    Wp = _add(D["F"], _mul(u, -P["winch_s"]))
    D["W"] = Wp
    D["winch_axis_pt"] = _add(Wp, _mul(n, P["drum_axis"]))
    D["drum_tan"] = _add(D["winch_axis_pt"], _mul(n, -P["drum_r"] - P["rope_d"] / 2))
    D["rope_up_len"] = math.dist(D["tan_out"], (D["drum_tan"][0], P["sheave_s"], D["drum_tan"][2]))
    # hanging rigging stack (global Z), from the sheave down
    D["fall_top_z"] = zc
    D["thimble_top"] = zc - P["fall_top"]
    D["ring_c"] = D["thimble_top"] - 320.0             # hook bowl centre
    D["bow_z"] = D["ring_c"] - 13.45                   # lift shackle bow crown resting in the hook
    d325, _, in325 = P["shackle_325t"]
    D["shackle_pin_z"] = D["bow_z"] - (in325 + 0.45 * d325)
    D["lift_hole_z"] = D["shackle_pin_z"] - 1.5        # the pin bears on the top of the 22 mm hole
    D["beam_top"] = D["lift_hole_z"] - P["lift_hole_z"]
    D["beam_bot"] = D["beam_top"] - P["beam"][1]
    D["cross_top"] = D["beam_bot"] - P["cross_plate"][2]
    D["cross_bot"] = D["cross_top"] - P["cross"][1]
    D.update(band_stack(P, D["cross_bot"]))
    straight = (P["band"][2] - math.pi * P["band_r"]) / 2
    D["band_straight"] = straight
    D["band_c"] = D["band_eye_z"] - straight              # centre of the band wrap
    D["animal_c"] = D["band_c"] + 25.0                    # body centre of the 600 kg design animal
    D["belly"] = D["animal_c"] - 375.0
    D["hooves"] = D["belly"] - 760.0
    D["deck_top"] = P["bearer"][2] + P["runner"][1] + P["deck"][2]
    D["hoof_clear"] = D["hooves"] - D["deck_top"]
    D["fall_len"] = D["fall_top_z"] - D["thimble_top"]
    return D


def band_stack(P, cross_bot):
    """Heights from a cross bar's underside down to the band's sewn eye (tip lug, shackle, chain, shackle, yoke)."""
    d1, _, in1 = P["shackle_1t"]
    o = {}
    o["tip_hole_z"] = cross_bot - P["tip_lug"][1] + 25.0
    o["tip_pin_z"] = o["tip_hole_z"] - 1.5               # the pin bears on the bottom of the 14 mm hole
    o["top_crown_z"] = o["tip_pin_z"] - (in1 + 0.45 * d1)
    o["low_crown_z"] = o["top_crown_z"] - P["chain_len"]
    o["low_pin_z"] = o["low_crown_z"] - (in1 + 0.45 * d1)
    o["yoke_hole_z"] = o["low_pin_z"] - 1.5              # the shackle pin lifts on the top of the yoke lug hole
    o["yoke_top_z"] = o["yoke_hole_z"] - 40.0
    o["band_eye_z"] = o["yoke_top_z"] - P["yoke_gap"]    # the removable bar the band's eye wraps
    return o


# ----------------------------------------------------------------- part helpers
def _p(name, shape, mat, kind, bom, key, group="shell", explode=(0, 0, 0), color=None):
    q = cp.part(name, W.premesh(shape), mat, kind=kind, bom=bom, group=group, explode=explode, color=color)
    q["key"] = key
    return q


def _moved(q, loc, name=None):
    r = dict(q)
    r["shape"] = loc * q["shape"]
    if name:
        r["name"] = name
    return r


def _bolt_set(d, grip, origin, x_dir, z_dir, bom, key, label="", extra=None, mat="zinc_plated", explode=(0, 0, 0)):
    loc = W.frame(origin, x_dir, z_dir)
    return [_p(f"{nm}{label}", loc * shp, mat, "fastener", bom, key, explode=explode)
            for nm, shp in cp.hex_bolt_set(int(d), grip, extra=extra)]


def _clevis(origin, axis, x_dir, grip, d, bom, key, label):
    """Clevis pin whose head bears at origin and whose shank runs along axis, with its R-clip."""
    loc = W.frame(origin, x_dir, W.mul(axis, -1))
    return [_p(f"Leg pin, 20 mm clevis pin, {label}", loc * cp.clevis_pin(d, grip), GALV, "bought", bom, key),
            _p(f"R-clip, {label}", loc * Pos(0, 0, -grip - d) * cp.split_pin(d), GALV, "fastener", bom, key)]


def _shackle(name, pin_c, axis, bow, size, gap_fill, bom, key, explode=(0, 0, 0)):
    d, jaw, inside = size
    body, pin = W.bow_shackle(pin_c, axis, bow, d, jaw, inside)
    return [_p(f"{name} body", body, GALV, "bought", bom, key, explode=explode),
            _p(f"{name} screw pin", pin, GALV, "fastener", bom, key, explode=explode)]


def crown(pin_c, bow, size):
    d, _, inside = size
    return W.add(pin_c, W.mul(W.unit(bow), inside + 0.45 * d))


# ----------------------------------------------------------------- option A: tripod
def leg_parts(P, D, i, phi, winch=False):
    """One tripod leg with its caps, tongues and welds; leg 1 also carries the winch bracket, the winch and its bolts."""
    od, t = P["tube"]
    u, n, F, Hp = D["u"], D["n"], D["F"], D["Hp"]
    tw, tt, tl = P["tongue"]
    pc, ct = P["pin_from_cap"], P["cap_t"]
    key = f"leg_{i}"
    a = _add(Hp, _mul(u, pc + ct))
    b = _add(F, _mul(u, -(pc + ct)))
    Lt = math.dist(a, b)
    tube = cp.round_tube(od, t, Lt)
    for zz in (40.0, Lt - 40.0):                      # galvanising vent holes
        tube = tube - Pos(0, 0, zz) * Rot(0, 90, 0) * Cylinder(5.0, od + 4)
    out = [_p(f"Tripod leg {i} tube, CHS {od} x {t}", W.stock(tube, a, b, x_dir=n), GALV, "made", 1, key)]
    ends = (("head", Hp, -1), ("foot", F, 1))
    for nm, pin, sgn in ends:
        cap_c = _add(pin, _mul(u, -sgn * (pc + ct / 2)))
        out.append(_p(f"Tripod leg {i} {nm} end cap, 8 mm", W.disc(P["cap_d"] / 2, ct, cap_c, u, edge=1.0), GALV, "made", 1, key))
        face = _add(pin, _mul(u, -sgn * (pc + ct)))
        out.append(_p(f"Weld, leg {i} tube to {nm} cap", W.ring_weld(face, u, od / 2, 5.0, toward=sgn), GALV, "weld", 1, key))
        tc = _add(pin, _mul(u, -sgn * (pc - tl / 2)))
        tongue = W.plate_on(tw, tl, tt, tc, n, (0, 1, 0), holes=[(0.0, sgn * (pc - tl / 2), P["hole_d"])], r_corner=8.0, edge=1.0)
        out.append(_p(f"Tripod leg {i} {nm} tongue, 16 mm", tongue, GALV, "made", 1, key))
        cface = _add(pin, _mul(u, -sgn * pc))
        for sy in (-1, 1):
            o = _add(_add(cface, (0, sy * tt / 2, 0)), _mul(n, -tw / 2))
            out.append(_p(f"Weld, leg {i} {nm} tongue to cap {'+' if sy > 0 else '-'}",
                          W.fillet_on(o, n, tw, 6.0, _mul(u, sgn), (0, sy, 0)), GALV, "weld", 1, key))
    if winch:
        out += winch_parts(P, D)
    return [_moved(q, Rot(0, 0, phi)) for q in out]


def winch_parts(P, D):
    """Winch bracket welded on leg 1, the bought winch (leg-local) and its four M12 bolts."""
    od = P["tube"][0]
    u, n = D["u"], D["n"]
    Wp = D["W"]
    bl, bw, bt = P["bracket"]
    s0, sb = P["winch_s0"], P["bracket_s"]
    du, ds = P["winch_bolts"][0] / 2, P["winch_bolts"][1] / 2
    holes = [(x, y + s0 - sb, 13.0) for x in (-du, du) for y in (-ds, ds)]
    br_c = _add(_add(Wp, _mul(n, od / 2 + bt / 2)), (0, sb, 0))
    out = [_p("Winch bracket, 300 x 300 x 10 mm plate", W.plate_on(bl, bw, bt, br_c, u, n, holes=holes, r_corner=6.0), GALV, "made", 10, "bracket")]
    yw = math.sqrt((od / 2) ** 2 - (od / 2 - 6.0) ** 2)
    for sy in (-1, 1):
        o = _add(_add(_add(Wp, _mul(u, -bl / 2)), _mul(n, od / 2)), (0, sy * yw, 0))
        out.append(_p(f"Weld, winch bracket to leg 1 {'+' if sy > 0 else '-'}", W.fillet_on(o, u, bl, 6.0, (0, sy, 0), _mul(n, -1)), GALV, "weld", 10, "bracket"))
    # the bought winch: base, side frames, drum and flanges, shaft, gear and brake housing, crank and grip
    ax = D["winch_axis_pt"]
    base_c = _add(_add(Wp, _mul(n, od / 2 + bt + 5)), (0, s0, 0))
    pieces = [W.plate_on(220, 220, 10, base_c, u, n, holes=[(x, y, 13.0) for x in (-du, du) for y in (-ds, ds)], r_corner=8.0)]
    h = P["drum_axis"] + 125 - (od / 2 + bt + 10)
    for s in (s0 - 104.0, s0 + 104.0):
        fc = _add(_add(Wp, _mul(n, (od / 2 + bt + 10 + P["drum_axis"] + 125) / 2)), (0, s, 0))
        fr = W.plate_on(250, h, 8, fc, u, (0, 1, 0), r_corner=20.0)
        pieces.append(fr)
    a0, a1 = _add(ax, (0, s0 - 90, 0)), _add(ax, (0, s0 + 90, 0))
    pieces.append(rod(a0, a1, P["drum_r"], P["drum_r"] - 8.0))
    for s in (s0 - 90.0, s0 + 84.0):
        pieces.append(cp.break_edges(rod(_add(ax, (0, s, 0)), _add(ax, (0, s + 6, 0)), P["drum_flange_r"]), 1.5))
    pieces.append(rod(_add(ax, (0, s0 - 112, 0)), _add(ax, (0, s0 - 90, 0)), 12.5))
    gear_c = _add(_add(ax, _mul(u, -40)), (0, s0 + 135, 0))
    gb = W.frame(_add(gear_c, _mul(n, 12)), u, n) * (cp.break_edges(Box(230, 74, 230), 8.0) - Box(218, 62, 218))
    pieces.append(gb)
    brake = rod(_add(gear_c, (0, 37, 0)), _add(gear_c, (0, 52, 0)), 70.0)
    pieces.append(cp.break_edges(_moved_shape(brake, _mul(u, 50)), 2.0))
    crank_ax = _add(gear_c, _mul(u, -60))
    pieces.append(rod(_add(crank_ax, (0, 52, 0)), _add(crank_ax, (0, 110, 0)), 10))
    arm_dir = _norm(_add(_mul(n, 0.5), (0, 0, 0.8)))
    arm_mid = _add(_add(crank_ax, (0, 110, 0)), _mul(arm_dir, P["crank_arm"] / 2))
    arm_end = _add(_add(crank_ax, (0, 110, 0)), _mul(arm_dir, P["crank_arm"]))
    pieces.append(W.frame(arm_mid, (0, 1, 0), arm_dir) * cp.break_edges(Box(12, 30, P["crank_arm"] + 30), 3.0))
    pieces.append(cp.break_edges(rod(_add(arm_end, (0, 6, 0)), _add(arm_end, (0, 136, 0)), 16), 3.0))
    out.append(_p("Hand winch, 1,000 kg, spur gear, automatic load brake", Compound(pieces), "painted_steel", "bought", 9, "winch", color=C_WINCH))
    coil_r = P["drum_r"] + 3 * 0.93 * P["rope_d"] + P["rope_d"] * 0.07
    coil = rod(_add(ax, (0, s0 - 84, 0)), _add(ax, (0, s0 + 84, 0)), coil_r, P["drum_r"])
    out.append(_p("Wire rope on the winch drum, 20 m in 3 layers", coil, "rope", "bought", 11, "rope", color="#7D838A"))
    for x in (-du, du):
        for y in (-ds, ds):
            c = _add(_add(Wp, _mul(u, x)), (0, s0 + y, 0))
            top = _add(c, _mul(n, od / 2 + bt + 10))
            out += _bolt_set(12, bt + 10, top, u, n, 10, "winch_bolts", label=", winch to bracket", extra=4.0)
    return out


def _moved_shape(s, v):
    return Pos(*v) * s


def head_parts(P, D):
    """Head weldment: plate, three lug pairs, two sheave hangers and their welds (global)."""
    zu = D["z_u"]
    out = [_p("Tripod head plate, 440 x 12 mm", W.disc(P["head_d"] / 2, P["head_t"], (0, 0, zu + P["head_t"] / 2), (0, 0, 1), edge=1.5),
              GALV, "made", 2, "head")]
    L, drop = P["head_lug"]
    off = P["lug_gap"] / 2 + P["lug_t"] / 2
    hz = D["z_hp"] - (zu - drop / 2)
    for k, phi in enumerate(P["legs_phi"], start=1):
        for s in (-off, off):
            sg = 1 if s > 0 else -1
            lug = W.plate_on(L, drop, P["lug_t"], (P["head_pin_r"], s, zu - drop / 2), (1, 0, 0), (0, 1, 0),
                             holes=[(0.0, -hz, P["hole_d"])], r_corner=10.0, edge=0.8)
            out.append(_p(f"Tripod head lug, leg {k} {'+' if sg > 0 else '-'}", turn(lug, phi), GALV, "made", 2, "head"))
            for face in (1, -1):
                y = s + face * P["lug_t"] / 2
                bead = W.fillet_on((P["head_pin_r"] - L / 2, y, zu), (1, 0, 0), L, 5.0, (0, face, 0), (0, 0, -1))
                out.append(_p(f"Weld, head lug leg {k} {'+' if sg > 0 else '-'} face {face:+d}", turn(bead, phi), GALV, "weld", 2, "head"))
    hw, ht = P["hanger"]
    xc, sc, zc = D["sheave_c"]
    h = zu - (zc - 65)
    for s in (sc - P["sheave_w"] / 2 - 3 - ht / 2, sc + P["sheave_w"] / 2 + 3 + ht / 2):
        sg = 1 if s > sc else -1
        hp = W.plate_on(hw, h, ht, (xc, s, zu - h / 2), (1, 0, 0), (0, 1, 0), holes=[(0.0, -(zc - (zu - h / 2)), P["axle_d"] + 1)], r_corner=10.0)
        out.append(_p(f"Tripod head sheave hanger {'+' if sg > 0 else '-'}", turn(hp, P["legs_phi"][0]), GALV, "made", 2, "head"))
        for face in (1, -1):
            y = s + face * ht / 2
            bead = W.fillet_on((xc - hw / 2, y, zu), (1, 0, 0), hw, 6.0, (0, face, 0), (0, 0, -1))
            out.append(_p(f"Weld, sheave hanger {'+' if sg > 0 else '-'} face {face:+d}", turn(bead, P["legs_phi"][0]), GALV, "weld", 2, "head"))
    return out


def sheave_parts(P, D):
    xc, sc, zc = D["sheave_c"]
    w = P["sheave_w"]
    c = (xc, sc, zc)
    phi = P["legs_phi"][0]
    yl = lambda y0, y1, r: rod(_add(c, (0, y0, 0)), _add(c, (0, y1, 0)), r)
    sheave = yl(-w / 2 + 4, w / 2 - 4, P["sheave_hub_r"]) + yl(-w / 2, -w / 2 + 4, P["sheave_flange_r"]) + yl(w / 2 - 4, w / 2, P["sheave_flange_r"])
    sheave = cp.break_edges(sheave - yl(-w, w, 17.5), 0.8)
    bush = yl(-w / 2, w / 2, 17.5) - yl(-w, w, P["axle_d"] / 2)
    ht = P["hanger"][1]
    y_ring = -w / 2 - 3 - ht                      # outer face of the hanger nearer leg 1
    y_far = w / 2 + 3 + ht                        # outer face of the far hanger
    axle = yl(y_ring - 3.0, y_far, P["axle_d"] / 2) + cp.break_edges(yl(y_far, y_far + 8, 20.0), 1.0)
    axle = axle - (yl(y_ring - 1.7, y_ring - 0.1, 13.0) - yl(y_ring - 2, y_ring, 12.0))   # ring groove
    ring = yl(y_ring - 1.6, y_ring - 0.2, 16.75) - yl(y_ring - 2, y_ring, 12.0)
    out = [_p("Head sheave, 200 mm pitch, 230 mm over the flanges", sheave, GALV, "bought", 3, "sheave"),
           _p("Sheave bronze bush, 35 x 25 x 30", bush, "brass", "bought", 3, "sheave"),
           _p("Sheave axle pin, 25 mm, with head", axle, GALV, "bought", 3, "axle"),
           _p("Retaining ring for the sheave axle, 25 mm (DIN 471)", ring, "stainless", "fastener", 3, "axle")]
    for sg in (-1, 1):
        sp = yl(sg * w / 2, sg * (w / 2 + 3), 20.0) - yl(-w, w, P["axle_d"] / 2 + 0.5) if sg > 0 else yl(-(w / 2 + 3), -w / 2, 20.0) - yl(-w, w, P["axle_d"] / 2 + 0.5)
        out.append(_p(f"Sheave spacer washer, 3 mm {'+' if sg > 0 else '-'}", sp, GALV, "bought", 3, "sheave"))
    return [_moved(q, Rot(0, 0, phi)) for q in out]


def pin_parts(P, D):
    """Six leg pins with R-clips: three at the head, three at the feet."""
    off = P["lug_gap"] / 2 + P["lug_t"]
    out = []
    for k, phi in enumerate(P["legs_phi"], start=1):
        for nm, (x, z), key in (("head", (P["head_pin_r"], D["z_hp"]), "head_pins"), ("foot", (P["foot_r"], P["foot_pin_z"]), "foot_pins")):
            o = (x, -off - 0.5, z)
            for q in _clevis(o, (0, 1, 0), (1, 0, 0), P["pin_grip"], P["pin_d"], 4, key, f"leg {k} {nm}"):
                out.append(_moved(q, Rot(0, 0, phi)))
    return out


def fin_dirs(P=PARAMS):
    """Unit direction (foot-local) of the + side chain eye fin of each foot: toward the matching fin of the next foot."""
    R = P["foot_r"]
    f0 = (R - P["fin_x"], P["fin_s"], 0)                          # the same for every foot: the next foot is 120 deg on
    f1 = _rotz((R - P["fin_x"], -P["fin_s"], 0), 120.0)
    return _norm(_sub(f1, f0))


def foot_parts(P, D, k, phi, fins=True, bom=(5, 6, 7), key_prefix=""):
    """One foot: hardwood pad with steel straps, foot plate weldment (base, lug pair, chain eye fins), welds, two stakes."""
    R = P["foot_r"]
    fpL, fpW, fpT = P["foot_plate"]
    pr, ps, pt = P["pad"]
    sh = [(0.0, -P["stake_s"], P["stake_hole"]), (0.0, P["stake_s"], P["stake_hole"])]
    kp = key_prefix
    out = [_p(f"Ground pad {k}, hardwood 600 x 300 x 50", W.plate_on(pr, ps, pt, (R, 0, pt / 2), (1, 0, 0), (0, 0, 1), holes=sh, r_corner=6.0, edge=3.0),
              WOOD, "made", bom[1], kp + "pads")]
    for sx in (-1, 1):
        strap = Pos(R + sx * (pr / 2 - 40), 0, pt / 2) * (Box(25, ps + 4, pt + 4) - Box(27, ps, pt))
        out.append(_p(f"Ground pad {k} end strap {'+' if sx > 0 else '-'}", strap, GALV, "made", bom[1], kp + "pads"))
    out.append(_p(f"Foot plate {k} base, 260 x 260 x 10", W.plate_on(fpL, fpW, fpT, (R, 0, pt + fpT / 2), (1, 0, 0), (0, 0, 1), holes=sh, r_corner=6.0),
                  GALV, "made", bom[0], kp + "feet"))
    lugL, lugH = P["foot_lug"]
    off = P["lug_gap"] / 2 + P["lug_t"] / 2
    ztop = pt + fpT
    for s in (-off, off):
        sg = 1 if s > 0 else -1
        hz = P["foot_pin_z"] - (ztop + lugH / 2)
        lug = W.plate_on(lugL, lugH, P["lug_t"], (R, s, ztop + lugH / 2), (1, 0, 0), (0, 1, 0), holes=[(0.0, -hz, P["hole_d"])], r_corner=10.0)
        out.append(_p(f"Foot plate {k} lug {'+' if sg > 0 else '-'}", lug, GALV, "made", bom[0], kp + "feet"))
        for face in (1, -1):
            y = s + face * P["lug_t"] / 2
            out.append(_p(f"Weld, foot {k} lug {'+' if sg > 0 else '-'} face {face:+d}",
                          W.fillet_on((R - lugL / 2, y, ztop), (1, 0, 0), lugL, 5.0, (0, face, 0), (0, 0, 1)), GALV, "weld", bom[0], kp + "feet"))
    if fins:
        er, et, eh = P["eye"]
        if fins is True:
            cpos = fin_dirs(P)
            fl = [((cpos[0], sg * cpos[1], 0.0), sg) for sg in (1, -1)]
        else:
            fl = fins
        for c, sg in fl:
            nh = (-c[1], c[0], 0.0)
            fc = (R - P["fin_x"], sg * P["fin_s"], ztop + eh / 2)
            fin = W.plate_on(er, eh, et, fc, c, nh, holes=[(0.0, -(P["eye_hole_z"] - eh / 2), 20.0)], r_corner=10.0)
            out.append(_p(f"Foot plate {k} chain eye fin {'+' if sg > 0 else '-'}", fin, GALV, "made", bom[0], kp + "feet"))
            for face in (1, -1):
                o = _add(_add(fc, _mul(c, -er / 2)), _add(_mul(nh, face * et / 2), (0, 0, -eh / 2)))
                out.append(_p(f"Weld, foot {k} fin {'+' if sg > 0 else '-'} face {face:+d}",
                              W.fillet_on(o, c, er, 5.0, _mul(nh, face), (0, 0, 1)), GALV, "weld", bom[0], kp + "feet"))
    sd, sl = P["stake"]
    z_bot = -(sl - pt - fpT - 15)
    for s in (-P["stake_s"], P["stake_s"]):
        shaft = Pos(R, s, (z_bot + 60 + ztop) / 2) * Cylinder(sd / 2, ztop - z_bot - 60)
        point = Pos(R, s, z_bot) * Solid.make_cone(1.5, sd / 2, 60)
        head = Pos(R, s, ztop + 7.5) * cp.break_edges(Cylinder(24, 15), 1.5)
        out.append(_p(f"Ground stake {k} {'+' if s > 0 else '-'}, 25 mm bar", shaft + point + head, GALV, "made", bom[2], kp + "stakes"))
    return [_moved(q, Rot(0, 0, phi)) for q in out]


def fin_frame(P, k):
    """Global centre of foot k's + and - fin holes, their hole axes and the direction each fin points (toward its chain)."""
    R = P["foot_r"]
    cpos = fin_dirs(P)
    phi = P["legs_phi"][k]
    res = {}
    for sg in (1, -1):
        c = (cpos[0], sg * cpos[1], 0.0)
        nh = (-c[1], c[0], 0.0)
        hole = (R - P["fin_x"], sg * P["fin_s"], P["pad"][2] + P["foot_plate"][2] + P["eye_hole_z"])
        res[sg] = (_rotz(hole, phi), _rotz(nh, phi), _rotz(c, phi))
    return res


def spread_chain_parts(P, D):
    out = []
    s2 = P["shackle_2t"]
    for i in range(3):
        j = (i + 1) % 3
        hi, ni, ci = fin_frame(P, i)[1]
        hj, nj, cj = fin_frame(P, j)[-1]
        bear = (20.0 - s2[0]) / 2                     # the chain pulls each pin against the side of its hole
        hi, hj = W.add(hi, W.mul(ci, bear)), W.add(hj, W.mul(cj, bear))
        out += _shackle(f"Spread chain {i + 1} shackle at foot {i + 1}, 2 t bow", hi, ni, ci, s2, 0, 8, "spread_chains")
        out += _shackle(f"Spread chain {i + 1} shackle at foot {j + 1}, 2 t bow", hj, nj, cj, s2, 0, 8, "spread_chains")
        a, b = crown(hi, ci, s2), crown(hj, cj, s2)
        ch = W.chain(a, b, n0=ni, n1=nj, r0=0.45 * s2[0], r1=0.45 * s2[0], end_links=(10.0, 50.0, 26.0))
        out.append(_p(f"Spread chain {i + 1}, 8 mm grade 80 with enlarged end links", ch, CHAIN, "bought", 8, "spread_chains", color=C_CHAIN))
    return out


def rope_and_hook_parts(P, D, drop=None):
    """Wire rope from the drum up leg 1, over the sheave and down the middle; thimble eye; swivel hook."""
    r = P["rope_d"] / 2
    s = P["sheave_s"]
    u, n = D["u"], D["n"]
    t_out = (D["tan_out"][0], s, D["tan_out"][2])
    ax = D["winch_axis_pt"]
    along = _dot(_sub(ax, t_out), u)
    t_drum = _add(t_out, _mul(u, along))
    xc, _, zc = D["sheave_c"]
    pr = P["sheave_pitch_r"]
    a0 = math.degrees(math.atan2(n[2], n[0]))
    pts = [t_drum, t_out]
    prr = pr + 0.8                                   # chord allowance so the drawn rope stays on the groove
    for k in range(1, 13):
        a = math.radians(a0 + (180 - a0) * k / 12)
        pts.append((xc + prr * math.cos(a), s, zc + prr * math.sin(a)))
    pts.append((xc - prr, s, D["thimble_top"] + 4.0))
    phi = P["legs_phi"][0]
    out = [_p("Wire rope, 8 mm 6 x 19 IWRC, drum to sheave to hook", turn(cp.rope(pts, P["rope_d"]), phi), GALV, "bought", 11, "rope")]
    out += hook_stack(P, D, D["drop"])
    return out


def hook_stack(P, D, xy, bom_eye=11, bom_hook=12):
    x, y = xy
    tt = D["thimble_top"]
    ferrule = Pos(x, y, tt - 20) * cp.break_edges(Cylinder(10, 40), 1.5)
    thimble = Pos(x, y, tt - 83) * Rot(90, 0, 0) * Torus(35, 8)
    out = [_p("Thimble eye with pressed ferrule", Compound([ferrule, thimble]), GALV, "bought", bom_eye, "hook")]
    ze = tt - 121
    eye = Pos(x, y, ze) * Rot(0, 90, 0) * Torus(18, 7)
    swivel = Pos(x, y, ze - 40) * cp.break_edges(Cylinder(18, 30), 2.0)
    rc = D["ring_c"]
    shank = rod((x, y, ze - 55), (x, y, rc + 40), 12)
    bowl = Pos(x, y, rc) * Rot(0, 90, 0) * Torus(32, 10)
    latch = Pos(x, y + 26, rc + 30) * Rot(-35, 0, 0) * cp.break_edges(Box(14, 4, 52), 1.0)
    out.append(_p("Swivel eye hook, grade 80, with safety latch", Compound([eye, swivel, shank, bowl, latch]), "safety_red", "bought", bom_hook, "hook", color=C_HOOK))
    return out


# ----------------------------------------------------------------- spreader, bands and band ends (options A and C)
def cross_bar_parts(P, x0, yc, cross_top, label, bom=14, key="cross_bars", top="plate"):
    """SHS cross bar along X with end caps, tip lugs and either the bolted top plate (A, C) or a top lift lug (B)."""
    cl, cs, ct = P["cross"]
    zc = cross_top - cs / 2
    out = [_p(f"Spreader cross bar {label}, SHS 50 x 50 x 3", W.stock(cp.shs(cs, ct, cl - 12), (x0 - cl / 2 + 6, yc, zc), (x0 + cl / 2 - 6, yc, zc), x_dir=(0, 1, 0)),
              GALV, "made", bom, key)]
    for sx in (-1, 1):
        cap = W.plate_on(cs, cs, 6, (x0 + sx * (cl / 2 - 3), yc, zc), (0, 1, 0), (1, 0, 0), holes=[(0.0, 0.0, 8.0)], r_corner=4.0)
        out.append(_p(f"Spreader cross bar {label} end cap {'+' if sx > 0 else '-'}", cap, GALV, "made", bom, key))
    px, py, pt = P["cross_plate"]
    if top == "plate":
        pl = W.plate_on(px, py, pt, (x0, yc, cross_top + pt / 2), (1, 0, 0), (0, 0, 1), holes=[(0.0, -50.0, 18.0), (0.0, 50.0, 18.0)], r_corner=6.0)
        out.append(_p(f"Spreader cross bar {label} top plate", pl, GALV, "made", bom, key))
        for sy in (-1, 1):
            out.append(_p(f"Weld, cross bar {label} top plate {'+' if sy > 0 else '-'}",
                          W.fillet_on((x0 - px / 2, yc + sy * cs / 2, cross_top), (1, 0, 0), px, 5.0, (0, 0, -1), (0, sy, 0)), GALV, "weld", bom, key))
    else:
        lugL, lugH, lugT = 120.0, 100.0, 16.0
        lg = W.plate_on(lugL, lugH, lugT, (x0, yc, cross_top + lugH / 2), (1, 0, 0), (0, 1, 0), holes=[(0.0, -(lugH / 2 - 35.0), 22.0)], r_corner=12.0)
        out.append(_p(f"Band bar {label} lift lug, 16 mm", lg, GALV, "made", bom, key))
        for sy in (-1, 1):
            out.append(_p(f"Weld, band bar {label} lift lug {'+' if sy > 0 else '-'}",
                          W.fillet_on((x0 - lugL / 2, yc + sy * lugT / 2, cross_top), (1, 0, 0), lugL, 5.0, (0, sy, 0), (0, 0, 1)), GALV, "weld", bom, key))
    tlx, tlh, tlt = P["tip_lug"]
    cb = cross_top - cs
    for sx in (-1, 1):
        tx = x0 + sx * (cl / 2 - 40)
        tl = W.plate_on(tlx, tlh, tlt, (tx, yc, cb - tlh / 2), (1, 0, 0), (0, 1, 0), holes=[(0.0, -(-tlh / 2 + 25.0), 14.0)], r_corner=8.0)
        out.append(_p(f"Spreader cross bar {label} tip lug {'+' if sx > 0 else '-'}", tl, GALV, "made", bom, key))
        for face in (1, -1):
            out.append(_p(f"Weld, cross bar {label} tip lug {'+' if sx > 0 else '-'} face {face:+d}",
                          W.fillet_on((tx - tlx / 2, yc + face * tlt / 2, cb), (1, 0, 0), tlx, 5.0, (0, face, 0), (0, 0, -1)), GALV, "weld", bom, key))
    return out


def band_end_parts(P, S, tx, x_bar, yc, label, boms=(16, 17, 29)):
    """Band end: shackle in the tip lug, adjusting chain, shackle in the yoke lug, and the band end yoke."""
    s1 = P["shackle_1t"]
    out = []
    top_pin = (tx, yc, S["tip_pin_z"])
    out += _shackle(f"Band shackle {label} at the tip lug, 1 t bow", top_pin, (0, 1, 0), (0, 0, -1), s1, 0, boms[0], "band_shackles")
    low_pin = (x_bar, yc, S["low_pin_z"])
    out += _shackle(f"Band shackle {label} at the yoke, 1 t bow", low_pin, (0, 1, 0), (0, 0, 1), s1, 0, boms[0], "band_shackles")
    a, b = crown(top_pin, (0, 0, -1), s1), crown(low_pin, (0, 0, 1), s1)
    out.append(_p(f"Adjusting chain {label}, 8 mm grade 80, 1.0 m", W.chain(a, b, n0=(0, 1, 0), n1=(0, 1, 0), r0=0.45 * s1[0], r1=0.45 * s1[0]),
                  CHAIN, "bought", boms[1], "adj_chains", color=C_CHAIN))
    # yoke
    bd = P["yoke_bar_d"]
    pw, ptk, ph = P["yoke_plate"]
    yin = P["yoke_inside"] / 2
    zb, zt = S["band_eye_z"], S["yoke_top_z"]
    bar_half = yin + ptk + 22
    bar = cp.round_bar(bd, 2 * bar_half, chamfer_ends=1.0)
    for zz in (10.0, 2 * bar_half - 10.0):
        bar = bar - Pos(0, 0, zz) * Rot(0, 90, 0) * Cylinder(3.3, bd + 4)
    out.append(_p(f"Yoke {label} band end bar, 25 mm, removable", W.stock(bar, (x_bar, yc - bar_half, zb), (x_bar, yc + bar_half, zb), x_dir=(1, 0, 0)),
                  GALV, "made", boms[2], "yokes"))
    for sy in (-1, 1):
        rc = (x_bar, yc + sy * (bar_half - 10.0), zb)
        out.append(_p(f"R-clip {label} yoke bar {'+' if sy > 0 else '-'}", Pos(*rc) * cp.split_pin(20.0), GALV, "fastener", boms[2], "yokes"))
    pz = (zb - 25.0 + zt + 25.0) / 2
    phh = (zt + 25.0) - (zb - 25.0)
    for sy in (-1, 1):
        plc = (x_bar, yc + sy * (yin + ptk / 2), pz)
        pl = W.plate_on(pw, phh, ptk, plc, (1, 0, 0), (0, 1, 0), holes=[(0.0, -(zb - pz), bd + 1)], r_corner=12.0)
        out.append(_p(f"Yoke {label} side plate {'+' if sy > 0 else '-'}", pl, GALV, "made", boms[2], "yokes"))
        out.append(_p(f"Weld, yoke {label} top bar to side plate {'+' if sy > 0 else '-'}",
                      W.ring_weld((x_bar, yc + sy * yin, zt), (0, 1, 0), bd / 2, 4.0, toward=-sy), GALV, "weld", boms[2], "yokes"))
    tb = cp.round_bar(bd, 2 * yin, chamfer_ends=1.0)
    out.append(_p(f"Yoke {label} top bar, 25 mm", W.stock(tb, (x_bar, yc - yin, zt), (x_bar, yc + yin, zt), x_dir=(1, 0, 0)), GALV, "made", boms[2], "yokes"))
    lz0 = zt + bd / 2
    lug = W.plate_on(60.0, 50.0, 10.0, (x_bar, yc, lz0 + 25.0), (1, 0, 0), (0, 1, 0), holes=[(0.0, -(S["yoke_hole_z"] - (lz0 + 25.0)), 14.0)], r_corner=10.0)
    out.append(_p(f"Yoke {label} lug, 10 mm", lug, GALV, "made", boms[2], "yokes"))
    for face in (1, -1):
        out.append(_p(f"Weld, yoke {label} lug face {face:+d}", W.fillet_on((x_bar - 30.0, yc + face * 5.0, lz0), (1, 0, 0), 60.0, 4.0, (0, face, 0), (0, 0, 1)),
                      GALV, "weld", boms[2], "yokes"))
    return out


def band_parts(P, S, x0, yc, label, band_c, boms=(18, 19)):
    """Plain webbing band (both legs, the wrap under the animal and the two sewn eyes round the yoke bars) and its felt sleeve."""
    bw, bt, _ = P["band"]
    R = P["band_r"]
    zeye = S["band_eye_z"]
    rb = P["yoke_bar_d"] / 2
    straight = zeye - band_c
    pieces = []
    for sx in (-1, 1):
        pieces.append(Pos(x0 + sx * R, yc, band_c + straight / 2) * Box(bt, bw, straight))
        xb = x0 + sx * (R + rb + bt / 2)
        loop = Pos(xb, yc, zeye) * Rot(90, 0, 0) * (Cylinder(rb + bt, bw) - Cylinder(rb, bw + 2))
        loop = loop & Pos(xb, yc, zeye + rb + bt) * Box(2 * (rb + bt) + 2, bw + 4, 2 * (rb + bt))
        pieces.append(loop)
        pieces.append(Pos(x0 + sx * (R + 2 * rb + bt), yc, zeye - 75.0) * Box(bt, bw, 150.0))
    ring = Pos(x0, yc, band_c) * Rot(90, 0, 0) * (Cylinder(R + bt / 2, bw) - Cylinder(R - bt / 2, bw + 2))
    ring = ring & (Pos(x0, yc, band_c - R) * Box(2 * R + 40, bw + 10, 2 * R))
    pieces.append(ring)
    out = [_p(f"Webbing band {label}, plain polyester 240 mm, two-ply", Compound(pieces), BAND, "bought", boms[0], "bands", color=C_BAND)]
    sl = Pos(x0, yc, band_c) * Rot(90, 0, 0) * (Cylinder(R + bt / 2 + 10, bw + 20) - Cylinder(R + bt / 2, bw + 22))
    sl = sl & (Pos(x0, yc, band_c - R) * Box(2 * R * 0.85, bw + 30, 2 * R))
    out.append(_p(f"Felt sleeve {label}, 10 mm felt in canvas", sl, BAND, "made", boms[1], "felt", color=C_FELT))
    return out


def spreader_parts(P, D, xy):
    """H-frame spreader under the hook: lift shackle, main beam with sleeves, lug and eyes, two cross bars on four
    M16 bolts, and both bands on their chains and yokes."""
    x0, y0 = xy
    bl, bh, bw, bt = P["beam"]
    zb = D["beam_bot"]
    out = []
    out += _shackle("Lift shackle, 3.25 t bow", (x0, y0, D["shackle_pin_z"]), (1, 0, 0), (0, 0, 1), P["shackle_325t"], 0, 16, "lift_shackle")
    beam = cp.rhs(bw, bh, bt, bl - 12)
    beam = W.stock(beam, (x0, y0 - bl / 2 + 6, zb + bh / 2), (x0, y0 + bl / 2 - 6, zb + bh / 2), x_dir=(1, 0, 0))
    so, sw = P["sleeve"]
    for ys in P["sleeve_y"]:
        for sg in (1, -1):
            beam = beam - Pos(x0, y0 + sg * ys, zb + bh / 2) * Cylinder(so / 2 + 0.5, bh + 10)
    out.append(_p("Spreader main beam, RHS 100 x 50 x 4", beam, GALV, "made", 13, "beam"))
    for sg in (1, -1):
        cap = W.plate_on(bw, bh, 6, (x0, y0 + sg * (bl / 2 - 3), zb + bh / 2), (1, 0, 0), (0, 1, 0), holes=[(0.0, 0.0, 8.0)], r_corner=6.0)
        out.append(_p(f"Spreader main beam end cap {'+' if sg > 0 else '-'}", cap, GALV, "made", 13, "beam"))
    for ys in P["sleeve_y"]:
        for sg in (1, -1):
            sl = Pos(x0, y0 + sg * ys, zb + (bh + 3) / 2) * (Cylinder(so / 2, bh + 3) - Cylinder(so / 2 - sw, bh + 5))
            out.append(_p(f"Spreader sleeve at {sg * ys:+.0f} mm, 26.9 x 3.2", cp.break_edges(sl, 0.4), GALV, "made", 13, "beam"))
            out.append(_p(f"Weld, sleeve at {sg * ys:+.0f} mm", W.ring_weld((x0, y0 + sg * ys, zb + bh), (0, 0, 1), so / 2, 3.0), GALV, "weld", 13, "beam"))
    lugL, lugH, lugT = P["lift_lug"]
    holes = [(yh, -(D["lift_hole_z"] - (D["beam_top"] + lugH / 2)), P["lift_hole_d"]) for yh in P["lift_holes"]]
    lug = W.plate_on(lugL, lugH, lugT, (x0, y0, D["beam_top"] + lugH / 2), (0, 1, 0), (1, 0, 0), holes=[(h[0], -h[1], h[2]) for h in holes], r_corner=15.0, edge=1.0)
    out.append(_p("Spreader lift lug, 20 mm, five holes", lug, GALV, "made", 13, "beam"))
    for sx in (-1, 1):
        out.append(_p(f"Weld, lift lug to beam {'+' if sx > 0 else '-'}",
                      W.fillet_on((x0 + sx * lugT / 2, y0 - lugL / 2, D["beam_top"]), (0, 1, 0), lugL, 6.0, (sx, 0, 0), (0, 0, 1)), GALV, "weld", 13, "beam"))
    for sg in (1, -1):
        ye = y0 + sg * (bl / 2 + 30.0)
        eye = W.plate_on(60.0, 60.0, 10.0, (x0, ye, zb + bh / 2), (0, 1, 0), (1, 0, 0), holes=[(sg * 5.0, 0.0, 18.0)], r_corner=12.0)
        out.append(_p(f"Spreader guide line eye {'+' if sg > 0 else '-'}", eye, GALV, "made", 13, "beam"))
        for sx in (-1, 1):
            out.append(_p(f"Weld, guide line eye {'+' if sg > 0 else '-'} face {sx:+d}",
                          W.fillet_on((x0 + sx * 5.0, y0 + sg * bl / 2, zb + bh / 2 - 30.0), (0, 0, 1), 60.0, 4.0, (sx, 0, 0), (0, sg, 0)), GALV, "weld", 13, "beam"))
    S = band_stack(P, D["cross_bot"])
    for sg, lab in ((1, "chest"), (-1, "flank")):
        yc = y0 + sg * P["band_y"]
        out += cross_bar_parts(P, x0, yc, D["cross_top"], lab)
        for dy in (-50.0, 50.0):
            out += _bolt_set(16, 3.0 + bh + P["cross_plate"][2], (x0, yc + dy, D["beam_top"] + 3.0), (1, 0, 0), (0, 0, 1), 15, "cross_bolts",
                             label=f", cross bar {lab}", extra=160 - (3.0 + bh + 10) - 6 - 14.8, mat=GALV)
        out += band_rig(P, S, x0, yc, lab, D["band_c"])
    return out


def band_rig(P, S, x0, yc, lab, band_c):
    out = []
    cl = P["cross"][0]
    R = P["band_r"]
    rb = P["yoke_bar_d"] / 2
    for sx in (-1, 1):
        tx = x0 + sx * (cl / 2 - 40)
        x_bar = x0 + sx * (R + rb + P["band"][1] / 2)
        out += band_end_parts(P, S, tx, x_bar, yc, f"{lab} {'+' if sx > 0 else '-'}")
    out += band_parts(P, S, x0, yc, lab, band_c)
    return out


# ----------------------------------------------------------------- landing bridge (all options)
def bridge_parts(P, boms=(25, 26, 27)):
    L, h, w, t = P["runner"]
    bx, by, bt = P["bearer"]
    out = []
    for sg in (1, -1):
        b = W.plate_on(bx, by, bt, (0, sg * P["bearer_y"], bt / 2), (1, 0, 0), (0, 0, 1), r_corner=4.0, edge=5.0)
        out.append(_p(f"Rim bearer {'+' if sg > 0 else '-'}, hardwood 1,400 x 200 x 100", b, WOOD, "made", boms[0], "bearers"))
    zc = bt + h / 2
    for x in P["runner_x"]:
        out.append(_p(f"Bridge runner at x {x:+.0f}, RHS 100 x 50 x 3", W.stock(cp.rhs(w, h, t, L - 8), (x, -L / 2 + 4, zc), (x, L / 2 - 4, zc), x_dir=(1, 0, 0)),
                      GALV, "made", boms[1], "runners"))
        for sg in (1, -1):
            cap = W.plate_on(w, h, 4, (x, sg * (L / 2 - 2), zc), (1, 0, 0), (0, 1, 0), holes=[(0.0, 0.0, 10.0)], r_corner=6.0)
            out.append(_p(f"Bridge runner at x {x:+.0f} end cap {'+' if sg > 0 else '-'}", cap, GALV, "made", boms[1], "runners"))
    dx, dy, dt = P["deck"]
    z0 = bt + h
    cw, ch_, cl = P["cleat"]
    for k in (-1, 0, 1):
        yc = k * dy
        screws = [(cx, yc + sy) for cx in P["cleat_x"] for sy in (-525.0, -175.0, 175.0, 525.0)]
        deck = W.plate_on(dx, dy - 4, dt, (0, yc, z0 + dt / 2), (1, 0, 0), (0, 0, 1), r_corner=10.0, edge=3.0)
        for sx, sy in screws:
            deck = deck - Pos(sx, sy, z0 + 7.5) * Cylinder(3.0, 15.0)
        out.append(_p(f"Deck panel {k + 2}, plywood 25 mm", deck, PLY, "made", boms[2], "deck"))
        for cx in P["cleat_x"]:
            cleat = cp.break_edges(Pos(cx, yc, z0 - ch_ / 2) * Box(cw, cl, ch_), 2.0)
            for sx, sy in screws:
                if sx == cx:
                    cleat = cleat - Pos(sx, sy, z0 - ch_ / 2) * Cylinder(3.0, ch_ + 2)
            out.append(_p(f"Deck panel {k + 2} cleat at x {cx:+.0f}, hardwood 45 x 45", cleat, WOOD, "made", boms[2], "cleats"))
        for sx, sy in screws:
            scr = Pos(sx, sy, z0 - ch_) * Rot(180, 0, 0) * cp.coach_screw(6, 60)
            out.append(_p(f"Deck screw 6 x 60, panel {k + 2}", scr, "zinc_plated", "fastener", boms[2], "cleats"))
    return out


def passer_parts(P=PARAMS, origin=(0.0, -3400.0, 20.0), sections=2, last_spigot=True):
    """Passer pole (sections joined) with the J-head, laid on the ground along +X from origin."""
    od, wall, L = P["pole"]
    so, sl = P["spigot"]
    x0, y0, z0 = origin
    poles, spig = None, None
    x = x0
    for k in range(sections):
        p = rod((x, y0, z0 + od / 2), (x + L, y0, z0 + od / 2), od / 2, od / 2 - wall)
        poles = p if poles is None else poles + p
        if last_spigot or k < sections - 1:
            s = rod((x + L - 100, y0, z0 + od / 2), (x + L + 150, y0, z0 + od / 2), so / 2, so / 2 - 3)
            spig = s if spig is None else spig + s
        x += L + 2
    r = P["jhead_tube"] / 2
    ri = r - 3.2
    R = P["jhead_r"]
    zc = z0 + od / 2
    shank_end = (x + 500, y0, zc)
    jh = rod((x, y0, zc), shank_end, r, ri)
    jh = jh + rod((x - 150, y0, zc), (x + 2, y0, zc), so / 2)
    prev = shank_end
    for k in range(1, 13):
        a = math.radians(-90 + 180 * k / 12)
        p = (x + 500 + R * math.cos(a), y0 + R + R * math.sin(a), zc)
        jh = jh + rod(prev, p, r, ri)
        prev = p
    nose_end = (prev[0] - 250, prev[1], zc)
    jh = jh + rod(prev, nose_end, r) + Pos(*nose_end) * Cylinder(r, 2 * r)
    eye = Pos(nose_end[0] - 10, nose_end[1] + 25, zc) * (Cylinder(22, 8) - Cylinder(12, 10))
    yh = y0 + 2 * R + 300
    hk = rod((x0 - 150, yh, zc), (x0 + 2, yh, zc), so / 2) + rod((x0, yh, zc), (x0 + 400, yh, zc), 8)
    prev = (x0 + 400, yh, zc)
    for k in range(1, 9):
        a = math.radians(-90 + 200 * k / 8)
        p = (x0 + 400 + 60 * math.cos(a), yh + 60 + 60 * math.sin(a), zc)
        hk = hk + rod(prev, p, 8)
        prev = p
    return {"poles": poles, "spigots": spig, "jhead": jh + eye, "hookhead": hk}


def passer_model_parts(P):
    pp = passer_parts(P, origin=(-500.0, -3700.0, 0.0), sections=2, last_spigot=False)
    return [_p("Passer pole sections (2 of 16), aluminium 40 x 2", pp["poles"], ALU, "made", 20, "passer"),
            _p("Passer pole spigots, aluminium 35.5 x 3", pp["spigots"], ALU, "made", 20, "passer"),
            _p("Passer J-head, steel tube 26.9 x 3.2", pp["jhead"], GALV, "made", 21, "passer"),
            _p("Retrieval hook head, 16 mm bar", pp["hookhead"], GALV, "made", 22, "passer")]


def option_a(P=PARAMS):
    D = derived(P)
    out = []
    for i, phi in enumerate(P["legs_phi"], start=1):
        out += leg_parts(P, D, i, phi, winch=(i == 1))
        out += foot_parts(P, D, i, phi)
    out += head_parts(P, D)
    out += sheave_parts(P, D)
    out += pin_parts(P, D)
    out += spread_chain_parts(P, D)
    out += rope_and_hook_parts(P, D)
    out += spreader_parts(P, D, D["drop"])
    out += bridge_parts(P)
    out += passer_model_parts(P)
    return out


# ----------------------------------------------------------------- shared builders for options B and C
def pinned_leg(P, top, foot, label, key, section=("chs", 88.9, 3.2), holes=()):
    """A leg pinned at both ends: tube (CHS) or SHS between two pin centres, end caps, tongues and welds. Both pins
    are horizontal and square to the leg's own vertical plane. holes: global (point, axis, d) cut through the leg."""
    pc, ct = P["pin_from_cap"], P["cap_t"]
    tw, tt, tl = P["tongue"]
    d = W.unit(W.sub(foot, top))
    h = W.unit((d[0], d[1], 0.0)) if math.hypot(d[0], d[1]) > 1e-6 else (1.0, 0.0, 0.0)
    a = W.unit(W.cross((0, 0, 1), h))
    nrm = W.unit(W.cross(a, d))
    p0, p1 = W.add(top, W.mul(d, pc + ct)), W.sub(foot, W.mul(d, pc + ct))
    kind, size, wall = section
    stock = cp.round_tube(size, wall, math.dist(p0, p1)) if kind == "chs" else cp.shs(size, wall, math.dist(p0, p1))
    shape = W.stock(stock, p0, p1, x_dir=nrm)
    for pt, ax, dia in holes:
        shape = shape - W.frame(pt, W.perp(ax), ax) * Cylinder(dia / 2, 400.0)
    out = [_p(f"{label} {'tube, CHS' if kind == 'chs' else 'SHS'} {size} x {wall}", shape, GALV, "made", None, key)]
    for nm, pin, sg in (("top", top, 1), ("foot", foot, -1)):
        cc = W.add(pin, W.mul(d, sg * (pc + ct / 2)))
        if kind == "chs":
            cap = W.disc(size / 2 + 5.5, ct, cc, d, edge=1.0)
        else:
            cap = W.plate_on(size + 10, size + 10, ct, cc, nrm, d, r_corner=4.0)
        out.append(_p(f"{label} {nm} end cap", cap, GALV, "made", None, key))
        face = W.add(pin, W.mul(d, sg * (pc + ct)))
        if kind == "chs":
            out.append(_p(f"Weld, {label} {nm} cap", W.ring_weld(face, d, size / 2, 5.0, toward=sg), GALV, "weld", None, key))
        tc = W.add(pin, W.mul(d, sg * (pc - tl / 2)))
        out.append(_p(f"{label} {nm} tongue", W.plate_on(tw, tl, tt, tc, nrm, a, holes=[(0.0, sg * (pc - tl / 2), P["hole_d"])], r_corner=8.0), GALV, "made", None, key))
        cf = W.add(pin, W.mul(d, sg * pc))
        for sy in (-1, 1):
            o = W.add(W.add(cf, W.mul(a, sy * tt / 2)), W.mul(nrm, -tw / 2))
            out.append(_p(f"Weld, {label} {nm} tongue {'+' if sy > 0 else '-'}", W.fillet_on(o, nrm, tw, 6.0, W.mul(d, -sg), W.mul(a, sy)), GALV, "weld", None, key))
    return out, a, h


def lug_pair(P, pin, a, h, z_plate, label, key, L=90.0):
    """Two lug plates hanging under a plate (underside at z_plate), either side of a 16 mm tongue, holed for the pin."""
    off = P["lug_gap"] / 2 + P["lug_t"] / 2
    H = z_plate - pin[2] + 45.0
    out = []
    for sg in (-1, 1):
        c = W.add(pin, W.mul(a, sg * off))
        c = (c[0], c[1], z_plate - H / 2)
        lug = W.plate_on(L, H, P["lug_t"], c, h, a, holes=[(0.0, -(pin[2] - c[2]), P["hole_d"])], r_corner=10.0)
        out.append(_p(f"{label} lug {'+' if sg > 0 else '-'}", lug, GALV, "made", None, key))
        for face in (-1, 1):
            o = W.add((c[0], c[1], z_plate), W.add(W.mul(a, face * P["lug_t"] / 2), W.mul(h, -L / 2)))
            out.append(_p(f"Weld, {label} lug {'+' if sg > 0 else '-'} face {face:+d}", W.fillet_on(o, h, L, 5.0, W.mul(a, face), (0, 0, -1)), GALV, "weld", None, key))
    return out


def pin_at(P, pin, a, h, label, key):
    off = P["lug_gap"] / 2 + P["lug_t"]
    o = W.add(pin, W.mul(a, -(off + 0.5)))
    out = _clevis(o, a, h, P["pin_grip"], P["pin_d"], None, key, label)
    for q in out:
        q["name"] = q["name"].replace("Leg pin", "Pin")
    return out


def placed_foot(P, D, xy, h, label, key_prefix, fin_dir=None):
    """Option A's foot (pad, straps, plate, lug pair, stakes) turned so its lugs run along h and set at xy (z = 0).
    fin_dir: global horizontal direction of one chain eye fin (for a tie chain), or None."""
    R = P["foot_r"]
    psi = math.degrees(math.atan2(h[1], h[0]))
    Pf = dict(P, legs_phi=(0.0,))
    fins = None
    if fin_dir is not None:
        loc = _rotz(fin_dir, -psi)
        fins = [((loc[0], loc[1], 0.0), 1 if loc[1] > 0 else -1)]
    parts = foot_parts(Pf, D, 1, 0.0, fins=fins, bom=(None, None, None), key_prefix=key_prefix)
    loc = Pos(xy[0], xy[1], 0) * Rot(0, 0, psi) * Pos(-R, 0, 0)
    out = []
    for q in parts:
        r = _moved(q, loc)
        r["name"] = r["name"].replace("Ground pad 1", f"{label} pad").replace("Foot plate 1", f"{label} plate").replace(
            "Ground stake 1", f"{label} stake").replace("foot 1", label)
        out.append(r)
    return out, (lambda v: _add(_rotz(_sub(v, (R, 0, 0)), psi), (xy[0], xy[1], 0)))


def stake_plate(P, center, w, l, stakes, label, key, lug=None):
    """A staked steel ground anchor plate (12 mm) with 25 mm stakes; lug: (offset y, hole height) for a vertical eye lug."""
    x, y, _ = center
    out = [_p(f"{label} plate, 12 mm", W.plate_on(w, l, 12.0, (x, y, 6.0), (1, 0, 0), (0, 0, 1), holes=[(sx, sy, 28.0) for sx, sy in stakes], r_corner=10.0), GALV, "made", None, key)]
    for sx, sy in stakes:
        st = Pos(x + sx, y + sy, -350.0) * Cylinder(12.5, 724.0) + Pos(x + sx, y + sy, -712.0) * Solid.make_cone(1.5, 12.5, 50.0) + Pos(x + sx, y + sy, 12.0 + 7.5) * cp.break_edges(Cylinder(24, 15), 1.5)
        out.append(_p(f"{label} stake {sx:+.0f} {sy:+.0f}, 25 mm bar", st, GALV, "made", None, key))
    if lug:
        ly, lh = lug
        lc = (x, y + ly, 12.0 + 45.0)
        out.append(_p(f"{label} eye lug, 12 mm", W.plate_on(100.0, 90.0, 12.0, lc, (0, 1, 0), (1, 0, 0), holes=[(0.0, 12.0 + lh - lc[2], 22.0)], r_corner=12.0), GALV, "made", None, key))
        for face in (-1, 1):
            out.append(_p(f"Weld, {label} eye lug face {face:+d}", W.fillet_on((x + face * 6.0, y + ly - 50.0, 12.0), (0, 1, 0), 100.0, 6.0, (face, 0, 0), (0, 0, 1)), GALV, "weld", None, key))
    return out


def tangent_internal(c1, c2, r, side1):
    """Internal tangent between two equal circles (2D): the point on circle 1 on side1 (+1 or -1 of the c1->c2 line)
    and the matching point on circle 2."""
    m = ((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2)
    dm = math.dist(c1, m)
    base = math.atan2(m[1] - c1[1], m[0] - c1[0])
    al = math.acos(r / dm)
    t1 = (c1[0] + r * math.cos(base + side1 * al), c1[1] + r * math.sin(base + side1 * al))
    t2 = (2 * m[0] - t1[0], 2 * m[1] - t1[1])
    return t1, t2


# ----------------------------------------------------------------- option B: portable gantry and two chain hoists
def chain_hoist(top, bowl_c, label, side=1):
    """Hand chain hoist, 1 t class (bought). top: inside top of the top hook (it hangs on a shackle crown along X);
    bowl_c: centre of the bottom hook bowl (a shackle crown along X rests in it). Returns body, load chain, bottom
    hook and hand chain loop."""
    x, y, z = top
    body = [Pos(x, y, z - 16) * Rot(0, 90, 0) * Torus(24, 8),
            Pos(x, y, z - 55) * cp.break_edges(Cylinder(14, 30), 2.0),
            Pos(x, y, z - 150) * Rot(90, 0, 0) * cp.break_edges(Cylinder(85, 140), 6.0),
            Pos(x, y + side * 95, z - 160) * Rot(90, 0, 0) * cp.break_edges(Cylinder(115, 50), 6.0)]
    zb = bowl_c[2]
    lc = W.chain((x, y, z - 242), (x, y, zb + 128), n0=(1, 0, 0), wire_d=6.3, pitch=19.0, inner_w=8.5)
    hook = Compound([Pos(x, y, zb + 85) * cp.break_edges(Cylinder(16, 40), 2.0), rod((x, y, zb + 65), (x, y, zb + 32), 10),
                     Pos(x, y, zb) * Rot(90, 0, 0) * Torus(32, 10)])
    # the hand chain loop is pulled out to the operator at the rim (harnessed), clear of the bands and the animal
    hand = Compound([W.chain((x + sx * 105, y + side * 95, z - 280), (x + sx * 105, side * 1750.0, 1100.0), n0=(0, 1, 0), wire_d=5.0, pitch=15.0, inner_w=7.0)
                     for sx in (-1, 1)])
    return Compound(body), lc, hook, hand


def option_b(P=PARAMS):
    D = derived(P)
    out = []
    yF, xF = P["B_frame_y"], P["B_foot_x"]
    bh, bw_, bt = P["B_beam"]
    s325 = P["shackle_325t"]
    cross_top = D["cross_top"]                     # the band bars sit where option A's cross bars sit: same landing height
    bar_hole = cross_top + 65.0
    bar_pin = (0.0, 0.0, bar_hole + 1.5)
    bowl = crown(bar_pin, (0, 0, 1), s325)[2] + 13.45
    hook_top = bowl + 450.0                        # bowl to top hook, 1 t hoist near its closed height (catalogue class)
    crown_top = hook_top - 0.45 * s325[0]         # the top hook hangs on the crown: crown top = hook inside top
    lug_pin = crown_top + s325[2] + 0.45 * s325[0]
    lug_hole = lug_pin + 1.5
    beam_bot = lug_hole + 50.0                    # hole 30 mm above the lug bottom, clear of the hoist hook
    zc = beam_bot + bh / 2
    L = P["B_beam_L"]
    half = L / 2
    js = P["B_splice_y"]                           # two splices: three sections of about 1.93 m (WSL-DEC-001 D14)
    sad = [(sy, 60.0) for sy in (-50.0, 50.0)]
    bolts = lambda yj: [(yj + yy, zz) for yy in (-250.0, -150.0, 150.0, 250.0) for zz in (-30.0, 30.0)]
    secs = [(-half, -js, "1"), (-js, js, "2"), (js, half, "3")]
    allb = bolts(-js) + bolts(js)
    for y0, y1, nm in secs:
        beam = W.stock(cp.rhs(bw_, bh, bt, (y1 - y0) - 5.0), (0.0, y0 + 2.5, zc), (0.0, y1 - 2.5, zc), x_dir=(1, 0, 0))
        for yy, zz in allb:
            if y0 < yy < y1:
                beam = beam - Pos(0.0, yy, zc + zz) * Rot(0, 90, 0) * Cylinder(9.0, bw_ + 20)
        for sg in (-1, 1):
            for sy, zz in sad:
                if y0 < sg * yF + sy < y1:
                    beam = beam - Pos(0.0, sg * yF + sy, beam_bot + zz) * Rot(0, 90, 0) * Cylinder(9.0, bw_ + 20)
        out.append(_p(f"Gantry beam section {nm}, RHS 140 x 80 x 4", beam, GALV, "made", None, "B_beam"))
    for sg in (-1, 1):
        cap = W.plate_on(bw_, bh, 6, (0.0, sg * (half + 3), zc), (1, 0, 0), (0, 1, 0), holes=[(0.0, 0.0, 10.0)], r_corner=6.0)
        out.append(_p(f"Gantry beam end cap {'+' if sg > 0 else '-'}", cap, GALV, "made", None, "B_beam"))
    for yj in (-js, js):
        for sx in (-1, 1):
            sp = Pos(sx * (bw_ / 2 + 5), yj, zc) * cp.break_edges(Box(10.0, 600.0, 120.0), 1.0)
            for yy, zz in bolts(yj):
                sp = sp - Pos(sx * (bw_ / 2 + 5), yy, zc + zz) * Rot(0, 90, 0) * Cylinder(9.0, 40.0)
            out.append(_p(f"Gantry beam splice plate at {yj:+.0f} {'+' if sx > 0 else '-'}, 10 mm", sp, GALV, "made", None, "B_beam"))
        for yy, zz in bolts(yj):
            out += _bolt_set(16, bw_ + 20, (bw_ / 2 + 10, yy, zc + zz), (0, 1, 0), (1, 0, 0), None, "B_beam", label=", beam splice", mat=GALV)
    for sg, lab in ((1, "chest"), (-1, "flank")):
        yh = sg * P["band_y"]
        lg = W.plate_on(100.0, 80.0, 16.0, (0.0, yh, beam_bot - 40.0), (0, 1, 0), (1, 0, 0), holes=[(0.0, -10.0, 22.0)], r_corner=12.0)
        out.append(_p(f"Hoist lug {lab}, 16 mm", lg, GALV, "made", None, "B_beam"))
        for sx in (-1, 1):
            out.append(_p(f"Weld, hoist lug {lab} face {sx:+d}", W.fillet_on((sx * 8.0, yh - 50.0, beam_bot), (0, 1, 0), 100.0, 6.0, (sx, 0, 0), (0, 0, -1)), GALV, "weld", None, "B_beam"))
        out += _shackle(f"Hoist shackle {lab}, 3.25 t bow", (0.0, yh, lug_pin), (1, 0, 0), (0, 0, -1), s325, 0, None, "B_hoists")
        body, lc, hook, hand = chain_hoist((0.0, yh, hook_top), (0.0, yh, bowl), lab, side=sg)
        out.append(_p(f"Chain hoist {lab}, 1 t, hand chain, 15 m lift", body, "safety_yellow", "bought", None, "B_hoists"))
        out.append(_p(f"Chain hoist {lab} load chain, 6.3 mm", lc, CHAIN, "bought", None, "B_hoists", color=C_CHAIN))
        out.append(_p(f"Chain hoist {lab} bottom hook", hook, "safety_red", "bought", None, "B_hoists", color=C_HOOK))
        out.append(_p(f"Chain hoist {lab} hand chain loop", hand, CHAIN, "bought", None, "B_hoists", color=C_CHAIN))
        out += _shackle(f"Band bar shackle {lab}, 3.25 t bow", (0.0, yh, bar_pin[2]), (0, 1, 0), (0, 0, 1), s325, 0, None, "B_hoists")
        out += cross_bar_parts(P, 0.0, yh, cross_top, lab, bom=None, key="B_bars", top="lug")
        S = band_stack(P, cross_top - P["cross"][1])
        out += band_rig(P, S, 0.0, yh, lab, D["band_c"])
    # A-frames: saddle with cheeks on the beam, two pinned SHS legs on lug pairs, a welded mid tie, knee brace, feet
    sad_t = 12.0
    z_sp = beam_bot - sad_t                       # saddle underside
    for sg in (-1, 1):
        y = sg * yF
        tag = "+" if sg > 0 else "-"
        out.append(_p(f"A-frame {tag} saddle plate, 12 mm", W.plate_on(300.0, 220.0, sad_t, (0.0, y, z_sp + sad_t / 2), (1, 0, 0), (0, 0, 1), r_corner=8.0), GALV, "made", None, "B_frames"))
        for sx in (-1, 1):
            ch = W.plate_on(220.0, 120.0, 10.0, (sx * (bw_ / 2 + 5), y, beam_bot + 60.0), (0, 1, 0), (sx, 0, 0),
                            holes=[(sy * (1 if sx > 0 else -1), 0.0, 18.0) for sy, _ in sad], r_corner=8.0)
            out.append(_p(f"A-frame {tag} saddle cheek {'+' if sx > 0 else '-'}", ch, GALV, "made", None, "B_frames"))
            out.append(_p(f"Weld, A-frame {tag} cheek {'+' if sx > 0 else '-'}",
                          W.fillet_on((sx * (bw_ / 2 + 10), y - 110.0, beam_bot), (0, 1, 0), 220.0, 5.0, (sx, 0, 0), (0, 0, 1)), GALV, "weld", None, "B_frames"))
        for sy, zz in sad:
            out += _bolt_set(16, bw_ + 20, (bw_ / 2 + 10, y + sy, beam_bot + zz), (0, 1, 0), (1, 0, 0), None, "B_frames", label=", beam to saddle", mat=GALV)
        z_pin = z_sp - P["head_pin_drop"]
        zt = P["B_tie_z"]
        for sx in (-1, 1):
            top = (sx * 70.0, y, z_pin)
            foot = (sx * xF, y, P["foot_pin_z"])
            dl = W.unit(W.sub(foot, top))
            tpt = W.add(top, W.mul(dl, (z_pin - (zt + 25.0)) / -dl[2]))
            legp, a, h = pinned_leg(P, top, foot, f"A-frame {tag} leg {'+' if sx > 0 else '-'}", "B_frames", section=("shs", P["B_leg"][0], P["B_leg"][1]),
                                    holes=[(W.add(tpt, (0, 0, 0)), (0, 1, 0), 13.0)])
            out += legp
            out += lug_pair(P, top, a, h, z_sp, f"A-frame {tag} top {'+' if sx > 0 else '-'}", "B_frames")
            out += pin_at(P, top, a, h, f"A-frame {tag} top {'+' if sx > 0 else '-'}", "B_frames")
            fp, _ = placed_foot(P, D, (foot[0], foot[1]), h, f"A-frame {tag} foot {'+' if sx > 0 else '-'}", "B_")
            out += [q for q in fp if True]
            out += pin_at(P, foot, a, h, f"A-frame {tag} foot {'+' if sx > 0 else '-'}", "B_frames")
            out += _bolt_set(12, P["B_leg"][0] + 6.0, (tpt[0], y - P["B_leg"][0] / 2 - 6.0, tpt[2]), (1, 0, 0), (0, -1, 0), None, "B_frames", label=f", mid tie {tag}{'+' if sx > 0 else '-'}", mat=GALV)
        # mid tie: flat bar across the legs' -Y faces (toward the well), bolted with M12
        xt = abs(70.0 + (xF - 70.0) * (z_pin - (zt + 25.0)) / (z_pin - P["foot_pin_z"]))
        tie = Pos(0.0, y - sg * 0 - P["B_leg"][0] / 2 - 3.0, zt + 25.0) * cp.break_edges(Box(2 * xt + 80.0, 6.0, 50.0), 1.0)
        for sx in (-1, 1):
            tie = tie - Pos(sx * xt, y - P["B_leg"][0] / 2 - 3.0, zt + 25.0) * Rot(90, 0, 0) * Cylinder(6.5, 20.0)
        lug_y = y - P["B_leg"][0] / 2 - 6.0
        out.append(_p(f"A-frame {tag} mid tie, flat 50 x 6", tie, GALV, "made", None, "B_frames"))
        bl_ = W.plate_on(80.0, 70.0, 10.0, (0.0, lug_y - 35.0, zt + 25.0 + 30.0), (0, 1, 0), (1, 0, 0), holes=[(0.0, -10.0, 18.0)], r_corner=10.0)
        bl_ = Pos(0.0, lug_y - 40.0 * 0, zt + 25.0 + 25.0 + 35.0) * cp.break_edges(Box(10.0, 70.0, 70.0), 1.0) - Pos(0.0, lug_y - 0.0, zt + 25.0 + 70.0) * Rot(0, 90, 0) * Cylinder(9.0, 20.0)
        out.append(_p(f"A-frame {tag} brace lug on the tie", bl_, GALV, "made", None, "B_frames"))
        kb0 = (10.0, lug_y, zt + 25.0 + 70.0)
        kb1 = (10.0, sg * (yF - 900.0), beam_bot - 40.0)
        kd = W.unit(W.sub(kb1, kb0))
        brace = cp.shs(P["B_brace"][0], P["B_brace"][1], math.dist(kb0, kb1) - 181.0)
        out.append(_p(f"A-frame {tag} knee brace, SHS 40 x 3", W.stock(brace, W.add(kb0, W.mul(kd, 90.5)), W.sub(kb1, W.mul(kd, 90.5)), x_dir=(1, 0, 0)), GALV, "made", None, "B_frames"))
        for nm, pt, sgn in (("tie end", kb0, 1), ("beam end", kb1, -1)):
            tg = W.plate_on(50.0, 100.0, 10.0, W.add(pt, W.mul(kd, sgn * 40.0)), (0, 0, 1) if False else W.unit(W.cross((1, 0, 0), kd)), (1, 0, 0), holes=[(0.0, -sgn * 40.0 * 0 + (-40.0 if sgn > 0 else 40.0) * -1 * -1, 18.0)], r_corner=8.0)
            tg = W.frame(W.add(pt, W.mul(kd, sgn * 40.0)), W.unit(W.cross((1, 0, 0), kd)), (1, 0, 0)) * Pos(0, 0, -5.0) * cp.sheet(50.0, 100.0, 10.0, holes=[(0.0, 0.0, 0.0001)], r_corner=8.0)
            tg = tg - Pos(*pt) * Rot(0, 90, 0) * Cylinder(9.0, 40.0)
            out.append(_p(f"A-frame {tag} knee brace {nm} tongue", tg, GALV, "made", None, "B_frames"))
            out += _bolt_set(16, 20.0, (pt[0] + 5.0, pt[1], pt[2]), (0, 1, 0), (1, 0, 0), None, "B_frames", label=f", knee brace {tag} {nm}", mat=GALV)
        ul = Pos(0.0, kb1[1], beam_bot - 40.0) * cp.break_edges(Box(10.0, 100.0, 80.0), 1.0) - Pos(*kb1) * Rot(0, 90, 0) * Cylinder(9.0, 40.0)
        out.append(_p(f"A-frame {tag} brace lug under the beam", ul, GALV, "made", None, "B_frames"))
        out.append(_p(f"Weld, brace lug under the beam {tag}", W.fillet_on((-5.0, kb1[1] - 50.0, beam_bot), (0, 1, 0), 100.0, 5.0, (-1, 0, 0), (0, 0, -1)), GALV, "weld", None, "B_frames"))
    out += bridge_parts(P, boms=(None, None, None))
    for q in out:
        q["bom"] = None
    return out


# ----------------------------------------------------------------- option C: sheerlegs and draught haul
def option_c(P=PARAMS):
    D = derived(P)
    out = []
    xF, yF = P["C_foot_x"], P["C_foot_y"]
    s325 = P["shackle_325t"]
    rr = P["sheave_pitch_r"]
    z_s = D["sheave_c"][2]                        # top block sheave at option A's sheave height: same hook stack
    eye_c = z_s + 190.0
    crown_c = eye_c + 25.0 - 8.0 - 0.45 * s325[0]
    pin_z = crown_c + s325[2] + 0.45 * s325[0]
    hole_z = pin_z + 1.5
    z_hu = hole_z + 30.0                          # head plate underside
    z_pin = z_hu - P["head_pin_drop"]
    # head: plate, guy eye, block lug, two lug pairs
    out.append(_p("Sheer head plate, 14 mm", W.plate_on(320.0, 220.0, 14.0, (0.0, 0.0, z_hu + 7.0), (1, 0, 0), (0, 0, 1), r_corner=10.0), GALV, "made", None, "C_head"))
    ge = W.plate_on(90.0, 110.0, 16.0, (0.0, -40.0, z_hu + 14.0 + 55.0), (0, 1, 0), (1, 0, 0), holes=[(0.0, 25.0, 22.0)], r_corner=14.0)
    out.append(_p("Sheer head guy eye, 16 mm", ge, GALV, "made", None, "C_head"))
    bl = W.plate_on(90.0, 70.0, 16.0, (0.0, 0.0, z_hu - 35.0), (0, 1, 0), (1, 0, 0), holes=[(0.0, hole_z - (z_hu - 35.0), 22.0)], r_corner=14.0)
    out.append(_p("Sheer head block lug, 16 mm", bl, GALV, "made", None, "C_head"))
    for face in (-1, 1):
        out.append(_p(f"Weld, guy eye face {face:+d}", W.fillet_on((face * 8.0, -85.0, z_hu + 14.0), (0, 1, 0), 90.0, 6.0, (face, 0, 0), (0, 0, 1)), GALV, "weld", None, "C_head"))
        out.append(_p(f"Weld, block lug face {face:+d}", W.fillet_on((face * 8.0, -45.0, z_hu), (0, 1, 0), 90.0, 6.0, (face, 0, 0), (0, 0, -1)), GALV, "weld", None, "C_head"))
    for sx in (-1, 1):
        top = (sx * 85.0, 0.0, z_pin)
        foot = (sx * xF, yF, P["foot_pin_z"])
        tag = "+" if sx > 0 else "-"
        legp, a, h = pinned_leg(P, top, foot, f"Sheerleg {tag}", "C_legs")
        out += legp
        out += lug_pair(P, top, a, h, z_hu, f"Sheer head {tag}", "C_head", L=80.0)
        out += pin_at(P, top, a, h, f"sheer head {tag}", "C_head")
        fp, _ = placed_foot(P, D, (foot[0], foot[1]), h, f"Sheerleg foot {tag}", "C_", fin_dir=(-sx, 0.0, 0.0))
        out += fp
        out += pin_at(P, foot, a, h, f"sheerleg foot {tag}", "C_feet")
    # feet tie chain between the two fins
    fins = {}
    for q in out:
        pass
    for sx in (-1, 1):
        h = W.unit((sx * xF - sx * 85.0, yF, 0.0))
        psi = math.degrees(math.atan2(h[1], h[0]))
        loc = _rotz((-sx, 0.0, 0.0), -psi)
        sgn = 1 if loc[1] > 0 else -1
        R = P["foot_r"]
        hole_l = (R - P["fin_x"], sgn * P["fin_s"], P["pad"][2] + P["foot_plate"][2] + P["eye_hole_z"])
        hole = _add(_rotz(_sub(hole_l, (R, 0, 0)), psi), (sx * xF, yF, 0))
        c = _rotz((loc[0], loc[1], 0.0), psi)
        nh = (-c[1], c[0], 0.0)
        fins[sx] = (hole, nh, c)
    s2 = P["shackle_2t"]
    for sx in (-1, 1):
        hole, nh, c = fins[sx]
        out += _shackle(f"Feet tie shackle {'+' if sx > 0 else '-'}, 2 t bow", hole, nh, c, s2, 0, None, "C_feet")
    aa = crown(fins[1][0], fins[1][2], s2)
    bb = crown(fins[-1][0], fins[-1][2], s2)
    out.append(_p("Feet tie chain, 8 mm grade 80", W.chain(aa, bb, n0=fins[1][1], n1=fins[-1][1], r0=0.45 * s2[0], r1=0.45 * s2[0], end_links=(10.0, 50.0, 26.0)),
                  CHAIN, "bought", None, "C_feet", color=C_CHAIN))
    # top block on a shackle under the head
    out += _shackle("Top block shackle, 3.25 t bow", (0.0, 0.0, pin_z), (1, 0, 0), (0, 0, -1), s325, 0, None, "C_rope")
    blk = [Pos(0.0, 0.0, eye_c) * Rot(0, 90, 0) * Torus(25, 8), Pos(0.0, 0.0, eye_c - 30.0) * cp.break_edges(Cylinder(14, 26), 2.0)]
    for sx in (-1, 1):
        blk.append(W.plate_on(250.0, 230.0, 8.0, (sx * 23.0, 0.0, z_s + 45.0), (0, 1, 0), (sx, 0, 0), holes=[(0.0, -45.0 * sx, 26.0)], r_corner=50.0))
    blk.append(Pos(0.0, 0.0, z_s + 155.0) * cp.break_edges(Box(54.0, 60.0, 20.0), 2.0))
    blk.append(Pos(0.0, 0.0, z_s) * Rot(0, 90, 0) * Cylinder(12.5, 70.0))
    out.append(_p("Top block, 200 mm sheave, 2 t, swivel eye", Compound(blk), "safety_yellow", "bought", None, "C_rope"))
    shv = Pos(0.0, 0.0, z_s) * Rot(0, 90, 0) * (Cylinder(96.0, 22.0) + Pos(0, 0, 13.0) * Cylinder(115.0, 4.0) + Pos(0, 0, -13.0) * Cylinder(115.0, 4.0) - Cylinder(12.6, 40.0))
    out.append(_p("Top block sheave, 200 mm pitch", cp.break_edges(shv, 0.8), GALV, "bought", None, "C_rope"))
    # snatch block on a staked anchor plate between the feet
    y_sb = yF - 250.0                             # behind the feet line, clear of the bridge
    out += stake_plate(P, (0.0, y_sb, 0.0), 400.0, 300.0, [(sx * 150.0, sy * 100.0) for sx in (-1, 1) for sy in (-1, 1)], "Snatch block anchor", "C_anchor", lug=(0.0, 60.0))
    sb_pin = (0.0, y_sb, 12.0 + 60.0 + 1.5)
    out += _shackle("Snatch block shackle, 3.25 t bow", sb_pin, (1, 0, 0), (0, 0, 1), s325, 0, None, "C_rope")
    sb_eye = crown(sb_pin, (0, 0, 1), s325)[2] - 0.45 * s325[0] + 17.0   # the block pulls up: eye inside bottom on the crown
    z_sb = sb_eye + 33.0 + 26.0 + 115.0 + 4.0
    sbk = [Pos(0.0, y_sb, sb_eye) * Rot(0, 90, 0) * Torus(25, 8), Pos(0.0, y_sb, sb_eye + 46.0) * cp.break_edges(Cylinder(14, 26), 2.0)]
    for sx in (-1, 1):
        sbk.append(W.plate_on(240.0, 260.0, 8.0, (sx * 23.0, y_sb, z_sb - 30.0), (0, 1, 0), (sx, 0, 0), holes=[(0.0, 30.0 * sx, 26.0)], r_corner=60.0))
    sbk.append(Pos(0.0, y_sb, z_sb) * Rot(0, 90, 0) * Cylinder(12.5, 70.0))
    out.append(_p("Snatch block, 200 mm sheave, 2 t, opening side plate", Compound(sbk), "safety_yellow", "bought", None, "C_rope"))
    shv2 = Pos(0.0, y_sb, z_sb) * Rot(0, 90, 0) * (Cylinder(96.0, 22.0) + Pos(0, 0, 13.0) * Cylinder(115.0, 4.0) + Pos(0, 0, -13.0) * Cylinder(115.0, 4.0) - Cylinder(12.6, 40.0))
    out.append(_p("Snatch block sheave, 200 mm pitch", cp.break_edges(shv2, 0.8), GALV, "bought", None, "C_rope"))
    # the rope: hook fall on the +Y side of the top block, over it, internal tangent to the snatch block, under it, to the post
    prr = rr + 0.8
    t1, t2 = tangent_internal((0.0, z_s), (y_sb, z_sb), prr, -1)
    pts = [(0.0, prr, D["thimble_top"] + 4.0)]
    a_end = math.degrees(math.atan2(t1[1] - z_s, t1[0]))
    if a_end < 0:
        a_end += 360.0
    for k in range(0, 17):
        ang = math.radians(0.0 + (a_end - 0.0) * k / 16)
        pts.append((0.0, prr * math.cos(ang), z_s + prr * math.sin(ang)))
    a2 = math.degrees(math.atan2(t2[1] - z_sb, t2[0] - y_sb))
    for k in range(0, 9):
        ang = math.radians(a2 + (-90.0 - a2) * k / 8)
        pts.append((0.0, y_sb + prr * math.cos(ang), z_sb + prr * math.sin(ang)))
    py_ = P["C_post_y"]
    pr_ = 57.15 + 4.6
    z0w = 330.0
    pts.append((-pr_, py_, z0w))                   # arrives tangent to the post and leaves tangent after three turns
    for k in range(1, 73):
        ang = math.radians(180.0 + 1080.0 * k / 72)
        pts.append((pr_ * math.cos(ang), py_ + pr_ * math.sin(ang), z0w + 14.0 * 3 * k / 72))
    pts.append((-pr_, py_ - 2600.0, z0w + 42.0))
    out.append(_p("Wire rope, 8 mm, hook to top block to snatch block to the snubbing post and the tractor", cp.rope(pts, P["rope_d"]), GALV, "bought", None, "C_rope"))
    xy = (0.0, prr)
    out += hook_stack(P, D, xy, bom_eye=None, bom_hook=None)
    out += spreader_parts(P, D, xy)
    # back guy with a turnbuckle to a staked anchor plate
    ge_c = (0.0, -40.0, z_hu + 14.0 + 55.0 + 25.0)
    anc = (0.0, P["C_anchor_y"], 0.0)
    out += stake_plate(P, anc, 600.0, 300.0, [(x, y) for x in (-240.0, -120.0, 120.0, 240.0) for y in (-90.0, 90.0)], "Guy anchor", "C_anchor", lug=(90.0, 50.0))
    al = (0.0, P["C_anchor_y"] + 90.0, 12.0 + 50.0)
    dg = W.unit(W.sub(al, ge_c))
    out += _shackle("Back guy shackle at the head, 3.25 t bow", ge_c, (1, 0, 0), dg, s325, 0, None, "C_guy")
    out += _shackle("Back guy shackle at the anchor, 3.25 t bow", al, (1, 0, 0), W.mul(dg, -1), s325, 0, None, "C_guy")
    g0 = W.add(crown(ge_c, dg, s325), W.mul(dg, 0.45 * s325[0] + 6.0))
    g1 = W.sub(crown(al, W.mul(dg, -1), s325), W.mul(dg, 0.45 * s325[0] + 6.0))
    t0 = W.sub(g1, W.mul(dg, 1300.0))
    out.append(_p("Back guy, 10 mm wire rope, head to turnbuckle", cp.rope([g0, W.sub(t0, W.mul(dg, 6.0))], 10.0), GALV, "bought", None, "C_guy"))
    tbk = W.stock(cp.break_edges(Box(34.0, 34.0, 360.0), 3.0).moved(Location((0, 0, 180.0))) - Pos(0, 0, 180.0) * Box(36.0, 16.0, 220.0), t0, W.add(t0, W.mul(dg, 360.0)))
    out.append(_p("Back guy turnbuckle, M20, jaw and jaw", tbk, GALV, "bought", None, "C_guy"))
    out.append(_p("Back guy, 10 mm wire rope, turnbuckle to anchor", cp.rope([W.add(t0, W.mul(dg, 366.0)), g1], 10.0), GALV, "bought", None, "C_guy"))
    # snubbing post: CHS on a staked base plate with gussets
    out += stake_plate(P, (0.0, py_, 0.0), 400.0, 400.0, [(sx * 150.0, sy * 150.0) for sx in (-1, 1) for sy in (-1, 1)], "Snubbing post base", "C_post")
    post = Pos(0.0, py_, 12.0 + 350.0) * (Cylinder(57.15, 700.0) - Cylinder(51.15, 702.0))
    out.append(_p("Snubbing post, CHS 114.3 x 6, 700 mm", cp.break_edges(post, 1.0), GALV, "made", None, "C_post"))
    out.append(_p("Snubbing post cap", W.disc(64.0, 8.0, (0.0, py_, 12.0 + 700.0 + 4.0), (0, 0, 1)), GALV, "made", None, "C_post"))
    out.append(_p("Weld, post to base", W.ring_weld((0.0, py_, 12.0), (0, 0, 1), 57.15, 6.0), GALV, "weld", None, "C_post"))
    for k in range(4):
        ang = 45.0 + 90.0 * k
        g = cp.break_edges(Pos(50.0, 0, 50.0) * Box(100.0, 10.0, 100.0) - Pos(100.0, 0, 100.0) * Rot(0, 45, 0) * Box(141.4, 12.0, 141.4), 0.8)
        out.append(_p(f"Snubbing post gusset {k + 1}", Pos(0.0, py_, 12.0) * Rot(0, 0, ang) * Pos(57.15, 0, 0) * g, GALV, "made", None, "C_post"))
    out += bridge_parts(P, boms=(None, None, None))
    for q in out:
        q["bom"] = None
    return out


# ----------------------------------------------------------------- site context
def well_context(P=PARAMS, depth=2500.0):
    r = P["well_d"] / 2
    return Pos(0, 0, -depth / 2) * (Cylinder(r + 230, depth) - Cylinder(r, depth + 2))


def site_parts(P=PARAMS):
    return [_p("Brick well ring, 3 m across (site)", well_context(P, 1500.0), "concrete", "context", None, "site", group="context")]


def components(option=CHOSEN):
    parts = {"A": option_a, "B": option_b, "C": option_c}[option](PARAMS)
    return parts + site_parts(PARAMS)


# ----------------------------------------------------------------- legacy interface (calculations, drawings, build plan)
_CACHE = {}


def _option_a_cached(P=PARAMS):
    k = id(P)
    if k not in _CACHE:
        _CACHE[k] = option_a(P)
    return _CACHE[k]


def build_components(P=PARAMS):
    """Every component group of option A as one compound per key (global coordinates), from the detailed parts."""
    groups = {}
    for q in _option_a_cached(P):
        groups.setdefault(q["key"], []).append(q["shape"])
    return {k: Compound(v) for k, v in groups.items()}


def assembly(P=PARAMS, C=None):
    C = C or build_components(P)
    return Compound(children=list(C.values()))


def _leg_local(P, D):
    """One leg in its own frame (no winch), grouped as tube, caps (with welds) and tongues, for the build plan."""
    parts = leg_parts(P, D, 1, 0.0, winch=False)
    g = {"tube": [], "caps": [], "tongues": []}
    for q in parts:
        nm = q["name"]
        g["tube" if "tube" in nm and "Weld" not in nm else ("tongues" if "tongue" in nm and "Weld" not in nm else "caps")].append(q["shape"])
    return {k: Compound(v) for k, v in g.items()}


def _winch_local(P, D):
    g = {"bracket": [], "winch": [], "winch_bolts": []}
    for q in winch_parts(P, D):
        if q["key"] in g:
            g[q["key"]].append(q["shape"])
    return {k: Compound(v) for k, v in g.items()}


def _feet(P, D):
    out = {"pads": [], "foot_plates": [], "stakes": [], "foot_pins": [], "head_pins": []}
    for k, phi in enumerate(P["legs_phi"], start=1):
        for q in foot_parts(P, D, k, phi):
            out[{"pads": "pads", "feet": "foot_plates", "stakes": "stakes"}[q["key"]]].append(q["shape"])
    for q in pin_parts(P, D):
        out[q["key"]].append(q["shape"])
    return {k: Compound(v) for k, v in out.items() if v}


def chain_eye_points(P=PARAMS, D=None):
    """One point per foot for the spread chain statics: the middle of its two chain eye fin holes."""
    pts = []
    for k in range(3):
        f = fin_frame(P, k)
        pts.append(tuple((a + b) / 2 for a, b in zip(f[1][0], f[-1][0])))
    return pts


def animal_context(P=PARAMS, D=None):
    """Clay massing of the 600 kg design animal hanging in the bands (scale context, not a part)."""
    from build123d import Sphere, scale
    D = D or derived(P)
    x0, y0 = D["drop"]
    zc = D["animal_c"]
    body = Pos(x0, y0, zc) * scale(Sphere(1.0), (325, 850, 375))
    legs = None
    for sx in (-1, 1):
        for sy, yy in ((1, 560), (-1, -620)):
            top = (x0 + sx * 170, y0 + yy, zc - 150)
            bot = (x0 + sx * 170, y0 + yy + sy * 60, D["hooves"])
            lg = rod(top, bot, 60) + Pos(*bot) * Cylinder(55, 40)
            legs = lg if legs is None else legs + lg
    neck = rod((x0, y0 + 700, zc + 100), (x0, y0 + 1050, zc + 300), 170)
    head = Pos(x0, y0 + 1180, zc + 250) * scale(Sphere(1.0), (130, 260, 150))
    return body + legs + neck + head


def mass_table(P=PARAMS, C=None):
    """Mass in kg of each component group of option A, from the detailed parts (cad_parts densities), with the bought
    and soft parts the model draws only in part set to their catalogue masses."""
    out = {}
    for q in _option_a_cached(P):
        out[q["key"]] = out.get(q["key"], 0.0) + cp.mass_kg(q)
    out["rope"] = 0.25 * 25.0          # 25 m of 8 mm rope at 0.25 kg/m, all of it on the kit
    out["winch"] = 24.0                # catalogue mass class of a 1,000 kg hand winch with load brake
    out["adj_chains"] = 4 * 1.0 * 1.4  # the whole 1.0 m of each chain hangs on the rig
    out["bands"] = 2 * 2.6             # 240 mm two-ply polyester flat sling, 2 m, about 2.6 kg
    felt = [q for q in _option_a_cached(P) if q["key"] == "felt"]
    out["felt"] = sum(q["shape"].volume for q in felt) * DENSITY["felt"]
    out.pop("passer", None)
    pp = passer_parts(P, sections=1)
    out["passer_poles"] = 16 * pp["poles"].volume * DENSITY["aluminium"] + 16 * pp["spigots"].volume * DENSITY["aluminium"]
    out["jhead"] = pp["jhead"].volume * DENSITY["steel"]
    return out


# ----------------------------------------------------------------- constructability checks (option A)
def checks(P=PARAMS, C=None, verbose=True):
    """Parts that must touch do touch (gap <= 0.6 mm); parts that must not touch keep the stated clearance; set-backs,
    landing clearance, rope fall and spreader swing. Interference between every pair of parts is checked by
    .kit/cad_check.py."""
    C = C or build_components(P)
    D = derived(P)
    touch = [
        ("leg_1", "head_pins"), ("leg_2", "head_pins"), ("leg_3", "head_pins"), ("leg_1", "foot_pins"),
        ("head", "head_pins"), ("feet", "foot_pins"), ("feet", "pads"), ("feet", "stakes"), ("leg_1", "bracket"),
        ("bracket", "winch"), ("head", "axle"), ("sheave", "axle"), ("rope", "sheave"), ("rope", "hook"),
        ("hook", "lift_shackle"), ("lift_shackle", "beam"), ("beam", "cross_bars"), ("cross_bolts", "beam"),
        ("cross_bolts", "cross_bars"), ("band_shackles", "cross_bars"), ("band_shackles", "adj_chains"),
        ("band_shackles", "yokes"), ("bands", "yokes"), ("bands", "felt"), ("spread_chains", "feet"),
        ("bearers", "runners"), ("runners", "deck"), ("deck", "cleats"), ("winch_bolts", "bracket"),
    ]
    apart = [
        ("leg_1", "head", 0.4), ("leg_2", "head", 0.4), ("leg_3", "head", 0.4),
        ("leg_1", "feet", 0.4), ("leg_2", "feet", 0.4), ("leg_3", "feet", 0.4),
        ("leg_1", "sheave", 10), ("leg_2", "sheave", 10), ("leg_3", "sheave", 10),
        ("leg_1", "winch_bolts", 2), ("rope", "head", 5), ("rope", "bracket", 10),
        ("leg_1", "spread_chains", 30), ("leg_2", "spread_chains", 30), ("leg_3", "spread_chains", 30),
        ("spread_chains", "runners", 2), ("spread_chains", "bearers", 5), ("spread_chains", "deck", 5),
        ("pads", "bearers", 100), ("feet", "runners", 100), ("pads", "runners", 100),
        ("leg_1", "deck", 100), ("leg_2", "deck", 100), ("leg_3", "deck", 100),
        ("bands", "cross_bars", 50), ("bands", "deck", 100), ("felt", "deck", 100),
        ("adj_chains", "beam", 20), ("hook", "beam", 5), ("rope", "beam", 100),
        ("leg_1", "beam", 150), ("leg_2", "beam", 150), ("leg_3", "beam", 150),
        ("leg_1", "bands", 300), ("leg_2", "bands", 300), ("leg_3", "bands", 300),
        ("runners", "cleats", 2), ("winch", "spread_chains", 100), ("yokes", "cross_bars", 50),
    ]
    results = []
    for a, b in touch:
        d = C[a].distance_to(C[b])
        results.append((d <= 0.6, f"touch  {a:14s} {b:14s} gap {d:7.2f} mm"))
    for a, b, clr in apart:
        d = C[a].distance_to(C[b])
        results.append((d >= clr, f"apart  {a:14s} {b:14s} gap {d:7.1f} mm (need {clr:g})"))
    extra = [
        (D["hoof_clear"] >= 150, f"hooves {D['hoof_clear']:.0f} mm above the deck at the nominal lift (need 150)"),
        (D["fall_len"] >= 300, f"rope fall {D['fall_len']:.0f} mm below the sheave centre (need 300)"),
        (P["foot_r"] - P["pad"][0] / 2 - P["well_d"] / 2 >= 650, f"pad edge {P['foot_r'] - P['pad'][0] / 2 - P['well_d'] / 2:.0f} mm back from a {P['well_d']:.0f} mm well rim (need 650)"),
        (P["bearer_y"] - P["bearer"][1] / 2 - P["well_d"] / 2 >= 350, f"bearer edge {P['bearer_y'] - P['bearer'][1] / 2 - P['well_d'] / 2:.0f} mm back from the rim (need 350)"),
    ]
    reach = math.hypot(P["beam"][0] / 2 + 6, P["beam"][2] / 2)
    reach = max(reach, math.hypot(P["band_y"] + P["cross"][1] / 2, P["cross"][0] / 2 + 6))
    z = D["beam_top"]
    leg_r = P["head_pin_r"] + (D["z_hp"] - z) * math.tan(math.radians(D["leg_angle"]))
    inner = leg_r - P["tube"][0] / 2 / math.cos(math.radians(D["leg_angle"]))
    clear = inner - reach - D["drop_off"]
    D["turn_clear"] = clear
    extra.append((clear >= 100, f"spreader turned to any angle clears the legs by {clear:.0f} mm at the nominal lift (need 100)"))
    results += extra
    if verbose:
        for ok, txt in results:
            print(("pass " if ok else "FAIL ") + txt)
        print(f"{sum(1 for ok, _ in results if ok)} of {len(results)} constructability checks pass")
    return results


def export_stl_files(P=PARAMS):
    """STL of option A by group (cad/stl/), chord tolerance 0.15 mm. STEP files come from .kit/cad_check.py --export."""
    import copy
    parts = [q for q in _option_a_cached(P) if q["kind"] != "context"]
    stl_dir = ROOT / "cad" / "stl"
    stl_dir.mkdir(parents=True, exist_ok=True)
    groups = {"tripod": ["leg_1", "leg_2", "leg_3", "head", "head_pins", "foot_pins", "feet", "sheave", "axle", "bracket"],
              "spreader": ["beam", "cross_bars", "cross_bolts", "lift_shackle", "yokes"],
              "bridge": ["bearers", "runners", "deck", "cleats"]}
    for g, keys in groups.items():
        export_stl(Compound([copy.copy(q["shape"]) for q in parts if q["key"] in keys]), str(stl_dir / f"wellsling-{g}.stl"),
                   tolerance=0.15, angular_tolerance=0.3)
    pp = passer_parts(P, origin=(0, 0, 0), sections=1)
    export_stl(pp["jhead"], str(stl_dir / "wellsling-passer-jhead.stl"), tolerance=0.15, angular_tolerance=0.3)
    print("wrote cad/stl/*.stl")


if __name__ == "__main__":
    D = derived()
    print(f"leg angle {D['leg_angle']:.1f} deg from vertical; head plate top {D['z_top']:.0f} mm; "
          f"drop {D['drop_off']:.0f} mm off the axis; hooves {D['hoof_clear']:.0f} mm above the deck")
    res = checks()
    if "--check" not in sys.argv:
        for opt in OPTIONS:
            ps = [q for q in components(opt) if q["kind"] != "context"]
            print(f"option {opt}: {len(ps)} parts, {sum(cp.mass_kg(q) for q in ps):.1f} kg")
        export_stl_files()
    if not all(ok for ok, _ in res):
        sys.exit(1)
