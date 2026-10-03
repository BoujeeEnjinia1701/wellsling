"""WellSling parametric model (build123d), constructable design (TRL 3, WSL-DDR-002).

Run from the repo root:
    python cad/src/model.py            export STEP and STL, run the constructability checks
    python cad/src/model.py --check    run the constructability checks only

WellSling is a rim-worked kit for lifting a fallen cow, buffalo or calf out of an open well
without anyone going down. It has a steel tripod of its own (three 76.1 mm legs pinned to a
head plate, a 200 mm head sheave and a hand winch with an automatic load brake on one leg),
staked feet on timber pads tied by spread chains, an H-frame spreader with two plain webbing
bands (chest and flank), and a landing bridge of three steel runners and plywood deck panels
that is slid across the well mouth under the lifted animal so it is lowered onto a floor and
never swung.

Coordinates in mm. Z up, ground at Z = 0, the well axis on the Z axis. Leg 1 (the winch leg)
points at -60 deg, legs 2 and 3 at +60 and 180 deg. Each leg-related part is built in a
leg-local frame (X radial, outward; Y tangential, counter-clockwise; Z up) and turned about Z.
PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from build123d import (Box, Cylinder, Location, Plane, Pos, Rot, Solid, Torus, Compound,
                       export_step, export_stl)

ROOT = Path(__file__).resolve().parents[2]

PARAMS = {
    # site and tripod geometry
    "well_d": 3000.0,          # largest well the design case covers (R5)
    "foot_r": 2500.0,          # radius of the foot pin circle about the well axis
    "leg_L": 4500.0,           # leg, head pin to foot pin
    "legs_phi": (-60.0, 60.0, 180.0),
    "head_pin_r": 110.0,       # radius of the head pins about the axis
    "head_pin_drop": 55.0,     # head pin centre below the head plate underside
    "foot_pin_z": 120.0,       # foot pin centre above the ground
    # leg
    "tube": (76.1, 3.6),       # OD x wall, galvanised steel (65 NB medium class)
    "cap_t": 8.0,              # end cap disc welded on each tube end
    "tongue": (60.0, 16.0, 90.0),   # width x thickness x length (cap face to tongue end)
    "pin_from_cap": 60.0,      # pin centre from the cap face
    "pin_d": 20.0, "hole_d": 21.0,
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
    # winch on leg 1
    "winch_s": 900.0,          # winch drum centre along leg 1 from the foot pin
    "bracket": (300.0, 240.0, 10.0),   # along leg x tangential x thickness
    "drum_axis": 175.0,        # drum axis outward of leg 1's axis
    "drum_r": 50.0, "drum_flange_r": 110.0,
    "crank_arm": 300.0,
    # foot
    "foot_plate": (260.0, 260.0, 10.0),
    "foot_lug": (100.0, 90.0),     # radial length x height above the foot plate
    "pad": (600.0, 300.0, 50.0),   # timber ground pad, radial x tangential x thickness
    "stake": (25.0, 760.0), "stake_s": 85.0, "stake_hole": 28.0,
    "eye": (60.0, 12.0, 40.0),     # chain eye plate, radial x thickness x height
    "chain_d": 20.0,               # envelope diameter used to draw an 8 mm chain
    # spreader
    "beam": (1100.0, 100.0, 50.0, 4.0),   # length (Y) x height x width x wall, RHS
    "sleeve": (26.9, 3.2), "sleeve_y": (300.0, 400.0, 500.0),
    "cross": (760.0, 50.0, 3.0),   # length (X) x size x wall, SHS
    "cross_plate": (100.0, 160.0, 10.0),  # X x Y x thickness, welded on the cross bar top
    "band_y": 450.0,               # half the band spacing (cross bars on sleeves 400 and 500)
    "lift_lug": (300.0, 120.0, 20.0),     # Y x height x thickness
    "lift_holes": (-100.0, -50.0, 0.0, 50.0, 100.0), "lift_hole_d": 22.0, "lift_hole_z": 80.0,
    "tip_lug": (60.0, 70.0, 10.0),  # X x height x thickness, under each cross bar tip
    "band": (240.0, 6.0, 2000.0),   # width x thickness x effective length
    "band_r": 354.0,                # band wrap radius under the animal
    "chain_len": 300.0,             # adjusting chain in use, shackle to shackle (300 to 1,000)
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
}

DENSITY = {"steel": 7.85e-6, "aluminium": 2.70e-6, "hardwood": 0.75e-6, "plywood": 0.60e-6,
           "polyester": 1.38e-6, "felt": 0.30e-6}

# ----------------------------------------------------------------- vector helpers
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


def obox(center, x_dir, z_dir, dx, dy, dz):
    """Box of size dx, dy, dz centred at center, its X along x_dir and Z along z_dir."""
    return Location(Plane(origin=center, x_dir=x_dir, z_dir=z_dir)) * Box(dx, dy, dz)


def ybore(center, d, length=400.0):
    """Cylinder along Y through center (for pin holes in leg-local plates)."""
    return rod(_add(center, (0, -length / 2, 0)), _add(center, (0, length / 2, 0)), d / 2)


def turn(shape, phi):
    return Rot(0, 0, phi) * shape


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
    # sheave centre: the rope from the winch runs parallel to leg 1, rope_offset outward of its axis
    n, u = D["n"], D["u"]
    zc = D["z_u"] + P["sheave_zc"]
    axis_c = _dot(D["Hp"], n)                  # leg axis: p . n = const
    D["rope_offset"] = P["drum_axis"] - P["drum_r"] - P["rope_d"] / 2   # rope leaves the bare drum on the leg side
    target = axis_c + D["rope_offset"] - P["sheave_pitch_r"]
    xc = (target - n[2] * zc) / n[0]
    D["sheave_c"] = (xc, P["sheave_s"], zc)    # leg 1 local
    D["drop_local"] = (xc - P["sheave_pitch_r"], P["sheave_s"])
    phi = math.radians(P["legs_phi"][0])
    x, s = D["drop_local"]
    D["drop"] = (x * math.cos(phi) - s * math.sin(phi), x * math.sin(phi) + s * math.cos(phi))
    D["drop_off"] = math.hypot(*D["drop"])
    # rope tangent point toward the winch (outer side of the sheave)
    D["tan_out"] = _add(D["sheave_c"], _mul(n, P["sheave_pitch_r"]))
    # winch: drum centre along leg 1
    W = _add(D["F"], _mul(u, -P["winch_s"]))
    D["winch_axis_pt"] = _add(W, _mul(n, P["drum_axis"]))
    D["drum_tan"] = _add(D["winch_axis_pt"], _mul(n, -P["drum_r"] - P["rope_d"] / 2 - 0.0))
    D["rope_up_len"] = math.dist(D["tan_out"], (D["drum_tan"][0], P["sheave_s"], D["drum_tan"][2]))
    # hanging rigging stack (global Z), from the sheave down
    D["fall_top_z"] = zc
    D["thimble_top"] = zc - P["fall_top"]
    D["ring_c"] = D["thimble_top"] - 320.0             # hook ring centre: thimble and ferrule 120, swivel 200
    D["bow_z"] = D["ring_c"] - 13.45                   # shackle bow bar resting in the hook
    D["shackle_pin_z"] = D["bow_z"] - 80.0
    D["lift_hole_z"] = D["shackle_pin_z"] - 1.5         # the pin bears on the top of the 22 mm hole
    D["beam_top"] = D["lift_hole_z"] - P["lift_hole_z"]
    D["beam_bot"] = D["beam_top"] - P["beam"][1]
    D["cross_top"] = D["beam_bot"] - P["cross_plate"][2]
    D["cross_bot"] = D["cross_top"] - P["cross"][1]
    D["tip_hole_z"] = D["cross_bot"] - P["tip_lug"][1] + 25.0
    D["tip_pin_z"] = D["tip_hole_z"] - 1.5               # the pin bears on the bottom of the 14 mm hole
    D["band_eye_z"] = D["tip_pin_z"] - 60.0 - P["chain_len"] - 60.0
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


# ----------------------------------------------------------------- tripod (leg-local)
def _leg_local(P, D, winch=False):
    """One leg in its local frame: tube, two end caps, two tongues with pin holes."""
    od, wall = P["tube"]
    u, n = D["u"], D["n"]
    F, Hp = D["F"], D["Hp"]
    tw, tt, tl = P["tongue"]
    pc, ct = P["pin_from_cap"], P["cap_t"]
    a = _add(Hp, _mul(u, pc + ct))            # tube end at the head
    b = _add(F, _mul(u, -(pc + ct)))          # tube end at the foot
    tube = rod(a, b, od / 2, od / 2 - wall)
    caps = rod(_add(Hp, _mul(u, pc)), a, od / 2) + rod(b, _add(F, _mul(u, -pc)), od / 2)
    t_head = obox(_add(Hp, _mul(u, pc - tl / 2)), n, u, tw, tt, tl) - ybore(Hp, P["hole_d"])
    t_foot = obox(_add(F, _mul(u, -(pc - tl / 2))), n, u, tw, tt, tl) - ybore(F, P["hole_d"])
    return {"tube": tube, "caps": caps, "tongues": t_head + t_foot}


def _winch_local(P, D):
    """Winch bracket welded to leg 1 and the bought winch (simplified), leg-local."""
    u, n = D["u"], D["n"]
    od = P["tube"][0]
    W = _add(D["F"], _mul(u, -P["winch_s"]))
    bl, bw, bt = P["bracket"]
    s0 = 70.0                                                 # bracket centre, tangential
    br_c = _add(_add(W, _mul(n, od / 2 + bt / 2)), (0, s0, 0))
    bracket = obox(br_c, u, n, bl, bw, bt)
    # winch: base plate, two side frames, drum with flanges, gear and brake housing, crank
    base_c = _add(_add(W, _mul(n, od / 2 + bt + 5)), (0, s0, 0))
    base = obox(base_c, u, n, 220, 220, 10)
    ax = D["winch_axis_pt"]
    frames = None
    for s in (-24.0, 164.0):
        fc = _add(_add(W, _mul(n, (od / 2 + bt + 10 + P["drum_axis"] + 125) / 2)), (0, s, 0))
        h = P["drum_axis"] + 125 - (od / 2 + bt + 10)
        f = obox(fc, u, n, 250, 8, h) - ybore(_add(ax, (0, s, 0)), 30, 20)
        frames = f if frames is None else frames + f
    drum = rod(_add(ax, (0, -20, 0)), _add(ax, (0, 160, 0)), P["drum_r"])
    flanges = (rod(_add(ax, (0, -20, 0)), _add(ax, (0, -14, 0)), P["drum_flange_r"])
               + rod(_add(ax, (0, 154, 0)), _add(ax, (0, 160, 0)), P["drum_flange_r"]))
    shaft = rod(_add(ax, (0, -28, 0)), _add(ax, (0, 168, 0)), 12.5)
    gear_c = _add(_add(ax, _mul(u, -40)), (0, 205, 0))
    gearbox = obox(_add(gear_c, _mul(n, -20)), u, n, 230, 74, 230)
    crank_ax = _add(gear_c, _mul(u, -60))
    crank_shaft = rod(_add(crank_ax, (0, 37, 0)), _add(crank_ax, (0, 95, 0)), 10)
    arm_dir = _norm(_add(_mul(n, 0.5), (0, 0, 0.8)))
    arm_end = _add(_add(crank_ax, _mul(arm_dir, P["crank_arm"])), (0, 95, 0))
    arm = obox(_mul(_add(_add(crank_ax, (0, 95, 0)), arm_end), 0.5), _norm((arm_dir[2], 0, -arm_dir[0])),
               arm_dir, 30, 12, P["crank_arm"] + 30)
    grip = rod(_add(arm_end, (0, 6, 0)), _add(arm_end, (0, 136, 0)), 16)
    winch = base + frames + drum + flanges + shaft + gearbox + crank_shaft + arm + grip
    bolts = None
    for du in (-80.0, 80.0):
        for ds in (-80.0, 80.0):
            c = _add(_add(W, (0, s0 + ds, 0)), _mul(u, du))
            b = rod(_add(c, _mul(n, od / 2 - 2)), _add(c, _mul(n, od / 2 + bt + 22)), 6)
            bolts = b if bolts is None else bolts + b
    return {"bracket": bracket, "winch": winch, "winch_bolts": bolts}


def _head(P, D):
    """Head plate with three lug pairs and the sheave hanger plates (global, one weldment)."""
    zu = D["z_u"]
    plate = Pos(0, 0, zu + P["head_t"] / 2) * Cylinder(P["head_d"] / 2, P["head_t"])
    L, drop = P["head_lug"]
    lugs = None
    off = P["lug_gap"] / 2 + P["lug_t"] / 2
    for phi in P["legs_phi"]:
        for s in (-off, off):
            lug = Pos(P["head_pin_r"], s, zu - drop / 2) * Box(L, P["lug_t"], drop)
            lug = lug - ybore(D["Hp"], P["hole_d"])
            lug = turn(lug, phi)
            lugs = lug if lugs is None else lugs + lug
    hw, ht = P["hanger"]
    xc, sc, zc = D["sheave_c"]
    hangers = None
    for s in (sc - P["sheave_w"] / 2 - 3 - ht / 2, sc + P["sheave_w"] / 2 + 3 + ht / 2):
        h = zu - (zc - 65)
        hp = Pos(xc, s, zu - h / 2) * Box(hw, ht, h)
        hp = hp - ybore((xc, s, zc), P["axle_d"] + 1, 30)
        hp = turn(hp, P["legs_phi"][0])
        hangers = hp if hangers is None else hangers + hp
    return {"head_plate": plate, "head_lugs": lugs, "hangers": hangers}


def _sheave(P, D):
    xc, sc, zc = D["sheave_c"]
    w = P["sheave_w"]
    c = (xc, sc, zc)
    hub = rod(_add(c, (0, -w / 2 + 4, 0)), _add(c, (0, w / 2 - 4, 0)), P["sheave_hub_r"])
    fl = (rod(_add(c, (0, -w / 2, 0)), _add(c, (0, -w / 2 + 4, 0)), P["sheave_flange_r"])
          + rod(_add(c, (0, w / 2 - 4, 0)), _add(c, (0, w / 2, 0)), P["sheave_flange_r"]))
    sheave = hub + fl
    gap = 3.0
    axle = rod(_add(c, (0, -w / 2 - gap - P["hanger"][1] - 12, 0)), _add(c, (0, w / 2 + gap + P["hanger"][1] + 18, 0)), P["axle_d"] / 2)
    spacers = (rod(_add(c, (0, -w / 2 - gap, 0)), _add(c, (0, -w / 2, 0)), 20)
               + rod(_add(c, (0, w / 2, 0)), _add(c, (0, w / 2 + gap, 0)), 20))
    phi = P["legs_phi"][0]
    return {"sheave": turn(sheave + spacers, phi), "axle": turn(axle, phi)}


def _rope(P, D):
    """Rope from the drum to the sheave, a short arc over the sheave, and the fall to the thimble."""
    r = P["rope_d"] / 2
    s = P["sheave_s"]
    u, n = D["u"], D["n"]
    t_out = (D["tan_out"][0], s, D["tan_out"][2])
    # the rope line runs parallel to the leg from the tangent point down to the drum
    ax = D["winch_axis_pt"]
    along = _dot(_sub(ax, t_out), u)
    t_drum = _add(t_out, _mul(u, along))
    up = rod(t_drum, t_out, r)
    xc, _, zc = D["sheave_c"]
    pr = P["sheave_pitch_r"]
    arc = None
    a0 = math.degrees(math.atan2(n[2], n[0]))
    for k in range(10):     # rope over the top of the sheave, from the outer tangent to the fall
        a1 = a0 + (180 - a0) * k / 10
        a2 = a0 + (180 - a0) * (k + 1) / 10
        p1 = (xc + pr * math.cos(math.radians(a1)), s, zc + pr * math.sin(math.radians(a1)))
        p2 = (xc + pr * math.cos(math.radians(a2)), s, zc + pr * math.sin(math.radians(a2)))
        seg = rod(p1, p2, r)
        arc = seg if arc is None else arc + seg
    fall = rod((xc - pr, s, zc), (xc - pr, s, D["thimble_top"]), r)
    phi = P["legs_phi"][0]
    return {"rope": turn(up + arc + fall, phi)}


def _hook(P, D):
    """Thimble eye, swivel hook and the bow shackle in the lift lug (global, at the drop point)."""
    x, y = D["drop"]
    tt = D["thimble_top"]
    eye = Pos(x, y, tt - 60) * Rot(90, 0, 0) * Torus(35, 8)
    ferrule = Pos(x, y, tt + 20) * Cylinder(10, 40)
    rc = D["ring_c"]
    swivel = Pos(x, y, tt - 133) * Cylinder(18, 60)
    shank = rod((x, y, tt - 163), (x, y, rc + 32), 12)
    bowl = Pos(x, y, rc) * Rot(0, 90, 0) * Torus(32, 10)
    return {"hook": eye + ferrule + swivel + shank + bowl}


def _shackle(center, axis, bow_dir, pin_d, gap, bow_len):
    """Bow shackle as a pin and a U of round bar. axis: pin direction; bow_dir: toward the bow."""
    c = center
    half = gap / 2 + pin_d / 2
    a = _norm(axis)
    b = _norm(bow_dir)
    pin = rod(_add(c, _mul(a, -half - 8)), _add(c, _mul(a, half + 8)), pin_d / 2)
    l1 = _add(c, _mul(a, -half)); l2 = _add(c, _mul(a, half))
    side1 = rod(l1, _add(l1, _mul(b, bow_len)), pin_d / 2 * 0.9)
    side2 = rod(l2, _add(l2, _mul(b, bow_len)), pin_d / 2 * 0.9)
    top = rod(_add(l1, _mul(b, bow_len)), _add(l2, _mul(b, bow_len)), pin_d / 2 * 0.9)
    return pin + side1 + side2 + top


def _spreader(P, D):
    """H-frame spreader: main beam with sleeves and lift lug, two bolted cross bars with tip lugs."""
    x0, y0 = D["drop"]
    bl, bh, bw, bt = P["beam"]
    zb = (D["beam_top"] + D["beam_bot"]) / 2
    beam = Pos(x0, y0, zb) * (Box(bw, bl, bh) - Box(bw - 2 * bt, bl - 2 * 0.0 + 10, bh - 2 * bt))
    ends = (Pos(x0, y0 + bl / 2 + 3, zb) * Box(bw, 6, bh) + Pos(x0, y0 - bl / 2 - 3, zb) * Box(bw, 6, bh))
    eyes = None
    for sgn in (1, -1):    # guide line eye plates on the beam end caps
        ye = y0 + sgn * (bl / 2 - 35)
        e = Pos(x0, ye, D["beam_top"] + 30) * Box(10, 60, 60)
        e = e - rod((x0 - 20, ye, D["beam_top"] + 35), (x0 + 20, ye, D["beam_top"] + 35), 9)
        eyes = e if eyes is None else eyes + e
    sleeves = None
    so, si = P["sleeve"][0] / 2, P["sleeve"][0] / 2 - P["sleeve"][1]
    bore_cut = None
    for ys in P["sleeve_y"]:
        for sgn in (1, -1):
            p0 = (x0, y0 + sgn * ys, D["beam_bot"]); p1 = (x0, y0 + sgn * ys, D["beam_top"])
            sl = rod(p0, p1, so, si)
            sleeves = sl if sleeves is None else sleeves + sl
            c = rod(_add(p0, (0, 0, -1)), _add(p1, (0, 0, 1)), so)
            bore_cut = c if bore_cut is None else bore_cut + c
    beam = beam - bore_cut
    lugL, lugH, lugT = P["lift_lug"]
    lug = Pos(x0, y0, D["beam_top"] + lugH / 2) * Box(lugT, lugL, lugH)
    for yh in P["lift_holes"]:
        lug = lug - rod((x0 - 20, y0 + yh, D["lift_hole_z"]), (x0 + 20, y0 + yh, D["lift_hole_z"]), P["lift_hole_d"] / 2)
    # cross bars
    cl, cs, ct = P["cross"]
    px, py, pt = P["cross_plate"]
    zc = (D["cross_top"] + D["cross_bot"]) / 2
    crosses, plates, tips, bolts = None, None, None, None
    for sgn in (1, -1):
        yc = y0 + sgn * P["band_y"]
        cb = Pos(x0, yc, zc) * (Box(cl, cs, cs) - Box(cl + 10, cs - 2 * ct, cs - 2 * ct))
        cb = cb + Pos(x0 + cl / 2 + 3, yc, zc) * Box(6, cs, cs) + Pos(x0 - cl / 2 - 3, yc, zc) * Box(6, cs, cs)
        pl = Pos(x0, yc, D["cross_top"] + pt / 2) * Box(px, py, pt)
        for dy in (-50.0, 50.0):
            pl = pl - rod((x0, yc + dy, D["cross_top"] - 1), (x0, yc + dy, D["cross_top"] + pt + 1), 9)
            b = rod((x0, yc + dy, D["cross_top"] - 18), (x0, yc + dy, D["beam_top"] + 12), 8)
            nut = Pos(x0, yc + dy, D["cross_top"] - 7) * Cylinder(13, 14)
            hd = Pos(x0, yc + dy, D["beam_top"] + 5) * Cylinder(13, 10)
            bb = b + nut + hd
            bolts = bb if bolts is None else bolts + bb
        tl = None
        for sx in (1, -1):
            tx = x0 + sx * (cl / 2 - 40)
            t = Pos(tx, yc, D["cross_bot"] - P["tip_lug"][1] / 2) * Box(P["tip_lug"][0], P["tip_lug"][2], P["tip_lug"][1])
            t = t - rod((tx, yc - 20, D["tip_hole_z"]), (tx, yc + 20, D["tip_hole_z"]), 7)
            tl = t if tl is None else tl + t
        crosses = cb if crosses is None else crosses + cb
        plates = pl if plates is None else plates + pl
        tips = tl if tips is None else tips + tl
    shackle = _shackle((x0, y0, D["shackle_pin_z"]), (1, 0, 0), (0, 0, 1), 19, P["lift_lug"][2] + 4, 80)
    return {"beam": beam + ends + eyes + sleeves + lug, "cross_bars": crosses + plates + tips,
            "cross_bolts": bolts, "lift_shackle": shackle}


def _bands(P, D):
    """Two plain webbing bands, chest and flank, with felt sleeves, adjusting chains and shackles."""
    x0, y0 = D["drop"]
    bw, bt, _ = P["band"]
    R = P["band_r"]
    cl = P["cross"][0]
    bands, sleeves, chains, shackles = None, None, None, None
    for sgn in (1, -1):
        yc = y0 + sgn * P["band_y"]
        zc = D["band_c"]
        # straight legs
        legs = (Pos(x0 - R, yc, zc + D["band_straight"] / 2) * Box(bt, bw, D["band_straight"])
                + Pos(x0 + R, yc, zc + D["band_straight"] / 2) * Box(bt, bw, D["band_straight"]))
        # wrap: a half ring under the animal
        ring = (Pos(x0, yc, zc) * Rot(90, 0, 0) * (Cylinder(R + bt / 2, bw) - Cylinder(R - bt / 2, bw + 2)))
        ring = ring & (Pos(x0, yc, zc - R) * Box(2 * R + 40, bw + 10, 2 * R))
        band = legs + ring
        sl = (Pos(x0, yc, zc) * Rot(90, 0, 0) * (Cylinder(R + bt / 2 + 10, bw + 20) - Cylinder(R + bt / 2, bw + 22)))
        sl = sl & (Pos(x0, yc, zc - R) * Box(2 * R * 0.85, bw + 30, 2 * R))
        bands = band if bands is None else bands + band
        sleeves = sl if sleeves is None else sleeves + sl
        for sx in (1, -1):
            tx = x0 + sx * (cl / 2 - 40)
            bx = x0 + sx * R
            top_sh = _shackle((tx, yc, D["tip_pin_z"]), (0, 1, 0), (0, 0, -1), 11, P["tip_lug"][2] + 3, 60)
            ch = rod((tx, yc, D["tip_pin_z"] - 60), (bx, yc, D["band_eye_z"] + 60), P["chain_d"] / 2)
            low_sh = _shackle((bx, yc, D["band_eye_z"]), (0, 1, 0), (0, 0, 1), 11, bw + 6, 60)
            chains = ch if chains is None else chains + ch
            s2 = top_sh + low_sh
            shackles = s2 if shackles is None else shackles + s2
    return {"bands": bands, "felt": sleeves, "adj_chains": chains, "band_shackles": shackles}


def _feet(P, D):
    out = {"pads": None, "foot_plates": None, "stakes": None, "foot_pins": None, "head_pins": None}
    fpL, fpW, fpT = P["foot_plate"]
    pr, ps, pt = P["pad"]
    off = P["lug_gap"] / 2 + P["lug_t"] / 2
    for phi in P["legs_phi"]:
        R = P["foot_r"]
        pad = Pos(R, 0, pt / 2) * Box(pr, ps, pt)
        plate = Pos(R, 0, pt + fpT / 2) * Box(fpL, fpW, fpT)
        lugL, lugH = P["foot_lug"]
        for s in (-off, off):
            lug = Pos(R, s, pt + fpT + lugH / 2) * Box(lugL, P["lug_t"], lugH)
            plate = plate + (lug - ybore(D["F"], P["hole_d"]))
        er, et, eh = P["eye"]
        ex = R - fpL / 2 + 10 + er / 2
        eye = Pos(ex, 0, pt + fpT + eh / 2) * Box(er, et, eh)
        eye = eye - ybore((ex, 0, pt + fpT + 20), 20)
        plate = plate + eye
        stakes = None
        for s in (-P["stake_s"], P["stake_s"]):
            hole = Pos(R, s, pt / 2) * Cylinder(P["stake_hole"] / 2, 2 * pt + 2 * fpT)
            pad = pad - hole
            plate = plate - hole
            st = rod((R, s, -(P["stake"][1] - pt - fpT - 15)), (R, s, pt + fpT), P["stake"][0] / 2)
            st = st + Pos(R, s, pt + fpT + 7.5) * Cylinder(24, 15)
            stakes = st if stakes is None else stakes + st
        fpin = ybore(D["F"], P["pin_d"], 2 * off + P["lug_t"] + 14) + Pos(R, -off - P["lug_t"] / 2 - 12, P["foot_pin_z"]) * Rot(90, 0, 0) * Cylinder(16, 10)
        hpin = ybore(D["Hp"], P["pin_d"], 2 * off + P["lug_t"] + 14) + Pos(P["head_pin_r"], -off - P["lug_t"] / 2 - 12, D["z_hp"]) * Rot(90, 0, 0) * Cylinder(16, 10)
        for k, shp in (("pads", pad), ("foot_plates", plate), ("stakes", stakes), ("foot_pins", fpin), ("head_pins", hpin)):
            shp = turn(shp, phi)
            out[k] = shp if out[k] is None else out[k] + shp
    return out


def chain_eye_points(P=PARAMS, D=None):
    D = D or derived(P)
    pts = []
    ex = P["foot_r"] - P["foot_plate"][0] / 2 + 10 + P["eye"][0] / 2
    z = P["pad"][2] + P["foot_plate"][2] + 20
    for phi in P["legs_phi"]:
        a = math.radians(phi)
        pts.append((ex * math.cos(a), ex * math.sin(a), z))
    return pts


def _spread_chains(P, D):
    pts = chain_eye_points(P, D)
    shp = None
    for i in range(3):
        a, b = pts[i], pts[(i + 1) % 3]
        d = _norm(_sub(b, a))
        p0 = _add(a, _mul(d, 45)); p1 = _add(b, _mul(d, -45))
        c = rod(p0, p1, P["chain_d"] / 2)
        sh = (_shackle(a, (0, 0, 1), d, 13, P["eye"][1] + 3, 40) + _shackle(b, (0, 0, 1), _mul(d, -1), 13, P["eye"][1] + 3, 40))
        shp = (c + sh) if shp is None else shp + c + sh
    return {"spread_chains": shp}


def _bridge(P, D):
    L, h, w, t = P["runner"]
    bx, by, bt = P["bearer"]
    bearers = (Pos(0, P["bearer_y"], bt / 2) * Box(bx, by, bt) + Pos(0, -P["bearer_y"], bt / 2) * Box(bx, by, bt))
    runners = None
    for x in P["runner_x"]:
        r = Pos(x, 0, bt + h / 2) * (Box(w, L, h) - Box(w - 2 * t, L + 2, h - 2 * t))
        r = r + Pos(x, L / 2 - 2, bt + h / 2) * Box(w, 4, h) + Pos(x, -L / 2 + 2, bt + h / 2) * Box(w, 4, h)
        runners = r if runners is None else runners + r
    dx, dy, dt = P["deck"]
    z0 = bt + h
    decks, cleats = None, None
    for k in (-1, 0, 1):
        yc = k * dy
        d = Pos(0, yc, z0 + dt / 2) * Box(dx, dy - 4, dt)
        decks = d if decks is None else decks + d
        for cx in P["cleat_x"]:
            c = Pos(cx, yc, z0 - P["cleat"][1] / 2) * Box(P["cleat"][0], P["cleat"][2], P["cleat"][1])
            cleats = c if cleats is None else cleats + c
    return {"bearers": bearers, "runners": runners, "deck": decks, "cleats": cleats}


def passer_parts(P=PARAMS, origin=(0.0, -3400.0, 20.0), sections=2):
    """Passer pole (sections joined) with the J-head, laid on the ground along +X from origin."""
    od, wall, L = P["pole"]
    so, sl = P["spigot"]
    x0, y0, z0 = origin
    poles, spig = None, None
    x = x0
    for k in range(sections):
        p = rod((x, y0, z0 + od / 2), (x + L, y0, z0 + od / 2), od / 2, od / 2 - wall)
        poles = p if poles is None else poles + p
        s = rod((x + L - 100, y0, z0 + od / 2), (x + L + 150, y0, z0 + od / 2), so / 2, so / 2 - 3)
        spig = s if spig is None else spig + s
        x += L + 2
    # J-head: 26.9 x 3.2 steel tube, straight shank 500, a 180 deg bend of radius jhead_r, nose 250
    r = P["jhead_tube"] / 2
    ri = r - 3.2
    R = P["jhead_r"]
    zc = z0 + od / 2
    shank_end = (x + 500, y0, zc)
    jh = rod((x - 150 + 150, y0, zc), shank_end, r, ri)
    jh = jh + rod((x - 150, y0, zc), (x + 2, y0, zc), so / 2)          # spigot of the head
    prev = shank_end
    for k in range(1, 13):
        a = math.radians(-90 + 180 * k / 12)
        p = (x + 500 + R * math.cos(a), y0 + R + R * math.sin(a), zc)
        jh = jh + rod(prev, p, r, ri)
        prev = p
    nose_end = (prev[0] - 250, prev[1], zc)
    jh = jh + rod(prev, nose_end, r) + Pos(*nose_end) * Cylinder(r, 2 * r)
    eye = Pos(nose_end[0] - 10, nose_end[1] + 25, zc) * (Cylinder(22, 8) - Cylinder(12, 10))
    # retrieval hook head: spigot, 400 mm of 16 mm round bar and an open hook of 60 mm radius
    yh = y0 + 2 * R + 300
    hk = rod((x0 - 150, yh, zc), (x0 + 2, yh, zc), so / 2) + rod((x0, yh, zc), (x0 + 400, yh, zc), 8)
    prev = (x0 + 400, yh, zc)
    for k in range(1, 9):
        a = math.radians(-90 + 200 * k / 8)
        p = (x0 + 400 + 60 * math.cos(a), yh + 60 + 60 * math.sin(a), zc)
        hk = hk + rod(prev, p, 8)
        prev = p
    return {"poles": poles, "spigots": spig, "jhead": jh + eye, "hookhead": hk}


# ----------------------------------------------------------------- assembly
BOM = {   # component key: (BOM line, name)
    "legs": (1, "Tripod legs (3)"),
    "head": (2, "Tripod head"),
    "sheave": (3, "Head sheave, 200 mm, with axle"),
    "pins": (4, "Leg pins (6)"),
    "feet": (5, "Foot plates (3)"),
    "pads": (6, "Ground pads (3)"),
    "stakes": (7, "Ground stakes (6)"),
    "spread_chains": (8, "Spread chains (3) and shackles"),
    "winch": (9, "Hand winch, 1,000 kg, load brake"),
    "bracket": (10, "Winch bracket and bolts"),
    "rope": (11, "Wire rope, 8 mm, 25 m"),
    "hook": (12, "Swivel hook and thimble eye"),
    "beam": (13, "Spreader main beam"),
    "cross_bars": (14, "Spreader cross bars (2)"),
    "cross_bolts": (15, "Cross bar bolts (4)"),
    "shackles": (16, "Shackles (9)"),
    "adj_chains": (17, "Adjusting chains (4)"),
    "bands": (18, "Webbing bands (2)"),
    "felt": (19, "Felt sleeves (2)"),
    "bearers": (25, "Rim bearers (2)"),
    "runners": (26, "Bridge runners (3)"),
    "deck": (27, "Deck panels (3)"),
}


def build_components(P=PARAMS):
    """Every component of the erected kit as named shapes (global coordinates)."""
    D = derived(P)
    C = {}
    legs = [_leg_local(P, D) for _ in P["legs_phi"]]
    for i, (phi, lg) in enumerate(zip(P["legs_phi"], legs), start=1):
        C[f"leg_{i}"] = turn(lg["tube"] + lg["caps"] + lg["tongues"], phi)
    w = _winch_local(P, D)
    phi1 = P["legs_phi"][0]
    C["bracket"] = turn(w["bracket"], phi1)
    C["winch"] = turn(w["winch"], phi1)
    C["winch_bolts"] = turn(w["winch_bolts"], phi1)
    h = _head(P, D)
    C["head"] = h["head_plate"] + h["head_lugs"] + h["hangers"]
    C.update(_sheave(P, D))
    C.update(_rope(P, D))
    C.update(_hook(P, D))
    f = _feet(P, D)
    C["pads"], C["feet"], C["stakes"] = f["pads"], f["foot_plates"], f["stakes"]
    C["foot_pins"], C["head_pins"] = f["foot_pins"], f["head_pins"]
    C.update(_spread_chains(P, D))
    C.update(_spreader(P, D))
    C.update(_bands(P, D))
    C.update(_bridge(P, D))
    return C


def assembly(P=PARAMS, C=None):
    C = C or build_components(P)
    return Compound(children=list(C.values()))


def well_context(P=PARAMS, depth=2500.0):
    r = P["well_d"] / 2
    return Pos(0, 0, -depth / 2) * (Cylinder(r + 230, depth) - Cylinder(r, depth + 2))


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
    """Mass in kg of each component group (steel unless named)."""
    C = C or build_components(P)
    mat = {"pads": "hardwood", "bearers": "hardwood", "deck": "plywood", "cleats": "hardwood",
           "bands": "polyester", "felt": "felt"}
    out = {}
    for k, s in C.items():
        if k in ("rope",):
            out[k] = 0.25 * 25.0   # 25 m of 8 mm rope at 0.25 kg/m, all of it on the kit
            continue
        if k in ("adj_chains", "spread_chains"):
            continue
        out[k] = s.volume * DENSITY[mat.get(k, "steel")]
    out["winch"] = 24.0            # catalogue mass class of a 1,000 kg hand winch with load brake
    out["spread_chains"] = 3 * 4.3 * 1.4 + 6 * 0.5   # 8 mm grade 80 chain 1.4 kg/m, shackles
    out["adj_chains"] = 4 * 0.6 * 1.4 + 0.0
    out["bands"] = 2 * 2.6         # 240 mm two-ply polyester flat sling, 2 m, about 2.6 kg
    pp = passer_parts(P, sections=1)
    out["passer_poles"] = 16 * pp["poles"].volume * DENSITY["aluminium"] + 16 * pp["spigots"].volume * DENSITY["aluminium"]
    out["jhead"] = pp["jhead"].volume * DENSITY["steel"]
    return out


# ----------------------------------------------------------------- constructability checks
def checks(P=PARAMS, C=None, verbose=True):
    """Parts that must touch do touch (gap <= 0.6 mm); parts that must not touch are apart
    (no shared volume and at least the stated clearance)."""
    C = C or build_components(P)
    D = derived(P)
    touch = [
        ("leg_1", "head_pins"), ("leg_2", "head_pins"), ("leg_3", "head_pins"),
        ("leg_1", "foot_pins"), ("head", "head_pins"), ("feet", "foot_pins"),
        ("feet", "pads"), ("feet", "stakes"), ("leg_1", "bracket"), ("bracket", "winch"),
        ("head", "axle"), ("sheave", "axle"), ("head", "sheave"), ("rope", "sheave"), ("rope", "winch"),
        ("rope", "hook"), ("hook", "lift_shackle"), ("lift_shackle", "beam"),
        ("beam", "cross_bars"), ("cross_bolts", "beam"), ("cross_bolts", "cross_bars"),
        ("band_shackles", "cross_bars"), ("band_shackles", "adj_chains"), ("band_shackles", "bands"),
        ("bands", "felt"), ("spread_chains", "feet"), ("bearers", "runners"), ("runners", "deck"),
        ("deck", "cleats"),
    ]
    apart = [   # (a, b, clearance mm)
        ("leg_1", "head", 0.4), ("leg_2", "head", 0.4), ("leg_3", "head", 0.4),
        ("leg_1", "feet", 0.4), ("leg_2", "feet", 0.4), ("leg_3", "feet", 0.4),
        ("leg_1", "sheave", 10), ("leg_2", "sheave", 10), ("leg_3", "sheave", 10),
        ("leg_1", "rope", 15), ("leg_1", "winch", 1),
        ("rope", "head", 5), ("rope", "bracket", 10),
        ("leg_1", "spread_chains", 30), ("leg_2", "spread_chains", 30), ("leg_3", "spread_chains", 30),
        ("spread_chains", "runners", 5), ("spread_chains", "bearers", 5), ("spread_chains", "deck", 5),
        ("pads", "bearers", 100), ("feet", "runners", 100), ("pads", "runners", 100),
        ("leg_1", "deck", 100), ("leg_2", "deck", 100), ("leg_3", "deck", 100),
        ("bands", "cross_bars", 50), ("bands", "deck", 100), ("felt", "deck", 100),
        ("adj_chains", "beam", 20), ("hook", "beam", 5), ("rope", "beam", 100),
        ("leg_1", "beam", 150), ("leg_2", "beam", 150), ("leg_3", "beam", 150),
        ("leg_1", "bands", 300), ("leg_2", "bands", 300), ("leg_3", "bands", 300),
        ("runners", "cleats", 2), ("winch", "spread_chains", 100),
    ]
    results = []
    for a, b in touch:
        d = C[a].distance_to(C[b])
        ok = d <= 0.6
        results.append((ok, f"touch  {a:14s} {b:14s} gap {d:7.2f} mm"))
    for a, b, clr in apart:
        try:
            ov = (C[a] & C[b]).volume
        except Exception:
            ov = 0.0
        d = C[a].distance_to(C[b])
        ok = ov < 1.0 and d >= clr
        results.append((ok, f"apart  {a:14s} {b:14s} gap {d:7.1f} mm (need {clr:g}), shared {ov:.1f} mm3"))
    extra = [
        (D["hoof_clear"] >= 150, f"hooves {D['hoof_clear']:.0f} mm above the deck at the nominal lift (need 150)"),
        (D["fall_len"] >= 300, f"rope fall {D['fall_len']:.0f} mm below the sheave centre (need 300)"),
        (P["foot_r"] - P["pad"][0] / 2 - P["well_d"] / 2 >= 650, f"pad edge {P['foot_r'] - P['pad'][0] / 2 - P['well_d'] / 2:.0f} mm back from a {P['well_d']:.0f} mm well rim (need 650)"),
        (P["bearer_y"] - P["bearer"][1] / 2 - P["well_d"] / 2 >= 350, f"bearer edge {P['bearer_y'] - P['bearer'][1] / 2 - P['well_d'] / 2:.0f} mm back from the rim (need 350)"),
    ]
    # the spreader may turn on the swivel hook: its farthest point must clear every leg at that height
    x0, y0 = D["drop"]
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
        n_ok = sum(1 for ok, _ in results if ok)
        print(f"{n_ok} of {len(results)} constructability checks pass")
    return results


def export(P=PARAMS, C=None):
    C = C or build_components(P)
    step_dir, stl_dir = ROOT / "cad" / "step", ROOT / "cad" / "stl"
    step_dir.mkdir(parents=True, exist_ok=True); stl_dir.mkdir(parents=True, exist_ok=True)
    asm = assembly(P, C)
    export_step(asm, str(step_dir / "wellsling-assembly.step"))
    groups = {"tripod": ["leg_1", "leg_2", "leg_3", "head", "head_pins", "foot_pins", "feet", "sheave", "axle"],
              "spreader": ["beam", "cross_bars", "cross_bolts", "lift_shackle"],
              "bridge": ["bearers", "runners", "deck", "cleats"]}
    for g, keys in groups.items():
        export_stl(Compound(children=[C[k] for k in keys]), str(stl_dir / f"wellsling-{g}.stl"), tolerance=0.5, angular_tolerance=0.3)
    pp = passer_parts(P, origin=(0, 0, 0), sections=1)
    export_stl(pp["jhead"], str(stl_dir / "wellsling-passer-jhead.stl"), tolerance=0.5, angular_tolerance=0.3)
    print("wrote cad/step/wellsling-assembly.step and cad/stl/*.stl")


if __name__ == "__main__":
    D = derived()
    print(f"leg angle {D['leg_angle']:.1f} deg from vertical; head plate top {D['z_top']:.0f} mm; "
          f"drop {D['drop_off']:.0f} mm off the axis; hooves {D['hoof_clear']:.0f} mm above the deck")
    C = build_components()
    res = checks(C=C)
    if "--check" not in sys.argv:
        export(C=C)
    if not all(ok for ok, _ in res):
        sys.exit(1)
