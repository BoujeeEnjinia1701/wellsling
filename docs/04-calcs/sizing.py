"""WellSling sizing calculations (WSL-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Imports the parametric model (cad/src/model.py) so every size used here is the one in the STEP
file and the drawings, reads bom/bom.csv and project.yaml, prints every result with a tag
([A1], [B2] ...) that the calculation note quotes, and writes docs/04-calcs/results.csv.
First-principles screening estimates for a paper proof of concept; nothing here replaces a
proof-load test of the real tripod, winch, rope and rigging (TRL 4).
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src")]
import model as M  # noqa: E402

P, D = M.PARAMS, M.derived()
g = 9.81
OUT = []


def out(tag, text, value=None, unit=""):
    print(f"[{tag}] {text}")
    OUT.append((tag, text, "" if value is None else f"{value:.4g}", unit))


# ------------------------------------------------------------------ A. loads
C = M.build_components()
mass = M.mass_table(C=C)
animal = 600.0                                     # design animal, upper end of 400 to 600 kg
rig_keys = ["hook", "lift_shackle", "beam", "cross_bars", "cross_bolts", "band_shackles", "adj_chains", "bands", "felt"]
rigging = sum(mass[k] for k in rig_keys)
rope_kg_m = 0.25
fall_max = 15.0 + D["z_u"] / 1000                   # rope hanging below the sheave with the animal at 15 m
hook_kg = animal + rigging + rope_kg_m * fall_max
Wh = hook_kg * g / 1000                            # kN
out("A1", f"Design animal {animal:.0f} kg; rigging below the hook {rigging:.1f} kg; hanging rope up to {rope_kg_m * fall_max:.1f} kg", animal, "kg")
out("A2", f"Design hook load {hook_kg:.0f} kg = {Wh:.2f} kN (SWL case); proof load 1.5 x = {1.5 * Wh:.2f} kN", Wh, "kN")
eta_sheave = 0.97
Tw = Wh / eta_sheave
out("A3", f"Rope tension at the winch while lifting (bronze-bushed sheave 97 %): {Tw:.2f} kN", Tw, "kN")

# ------------------------------------------------------------------ B. rope, sheave, winch
MBL = 40.0
out("B1", f"Rope 8 mm 6 x 19 IWRC 1770, MBL {MBL:.0f} kN: safety factor {MBL / Tw:.1f} (need 5)", MBL / Tw, "")
out("B2", f"Sheave pitch diameter {2 * P['sheave_pitch_r']:.0f} mm on 8 mm rope: D/d = {2 * P['sheave_pitch_r'] / P['rope_d']:.0f} (need 18)", 2 * P["sheave_pitch_r"] / P["rope_d"], "")
# drum layers
width = 168.0
turns = width / (P["rope_d"] * 1.05)
radii = [P["drum_r"] + P["rope_d"] / 2 + 0.93 * P["rope_d"] * k for k in range(8)]
cap = np.cumsum([2 * math.pi * r / 1000 * turns for r in radii])
rope_total = 25.0
paid_top = D["rope_up_len"] / 1000 + D["fall_len"] / 1000 + 0.5
on_drum_top = rope_total - paid_top
paid_deep = D["rope_up_len"] / 1000 + fall_max + 0.5
on_drum_deep = rope_total - paid_deep
lay_top = int(np.searchsorted(cap, on_drum_top)) + 1
lay_deep = int(np.searchsorted(cap, on_drum_deep)) + 1
n_layers_fit = int((P["drum_flange_r"] - P["drum_r"] - 10) // (0.93 * P["rope_d"]))
out("B3", f"Drum {2 * P['drum_r']:.0f} mm, {width:.0f} mm wide, {turns:.0f} turns per layer; holds {cap[n_layers_fit - 1]:.1f} m in {n_layers_fit} layers within the {2 * P['drum_flange_r']:.0f} mm flanges (need {rope_total:.0f} m)", cap[n_layers_fit - 1], "m")
out("B4", f"Rope paid out with the animal at 15 m: {paid_deep:.1f} m ({on_drum_deep:.1f} m on the drum, layer {lay_deep}); at the landing height {paid_top:.1f} m ({on_drum_top:.1f} m on the drum, layer {lay_top})", on_drum_top, "m")
r_top = radii[lay_top - 1] / 1000
r1 = radii[0] / 1000
rated = 1000 * g / 1000
cap_top = rated * r1 / r_top
out("B5", f"Winch rated {rated:.2f} kN on the first layer; on layer {lay_top} it gives {cap_top:.2f} kN against {Tw:.2f} kN needed: utilisation {Tw / cap_top:.0%}", Tw / cap_top, "")
F_rated = 230.0                                   # N at the handle at the rated load, first layer (catalogue class; confirm)
arm = P["crank_arm"] / 1000
F_top = F_rated * Tw / rated * r_top / r1
F_deep = F_rated * Tw / rated * radii[lay_deep - 1] / 1000 / r1
out("B6", f"Crank force (230 N at rated load, first layer, assumed): {F_deep:.0f} N as the lift starts at 15 m, {F_top:.0f} N at the landing height (need at most 250 N)", F_top, "N")
eta_w = 0.80
ratio = rated * 1000 * r1 / (F_rated * arm * eta_w)
v_turn = 2 * math.pi * r1 / ratio
lift_m = 15.0 + 2.6
rpm = 15.0
avg_r = (radii[lay_deep - 1] + r_top * 1000) / 2 / 1000
t_lift = lift_m / (v_turn * avg_r / r1 * rpm)
E_lift = Wh * lift_m
E_crank = E_lift / (eta_w * eta_sheave)
P_crank = F_top * 2 * math.pi * arm * rpm / 60
out("B7", f"Gear ratio about {ratio:.1f}:1 (from the handle force); {v_turn * 1000:.0f} mm of rope per crank turn on the first layer", ratio, "")
out("B8", f"Lifting {lift_m:.1f} m (15 m deep to the landing height) at {rpm:.0f} rpm: about {t_lift:.0f} min; work at the crank {E_crank:.0f} kJ for {E_lift:.0f} kJ of lift; about {P_crank:.0f} W at the crank near the top, so the crew takes turns", t_lift, "min")
out("B9", f"Lift energy flow: crank {E_crank:.0f} kJ, winch gears and brake {E_crank * (1 - eta_w):.0f} kJ lost, sheave {E_crank * eta_w * (1 - eta_sheave):.0f} kJ lost, {E_lift:.0f} kJ into raising the animal and rigging", E_lift, "kJ")

# ------------------------------------------------------------------ C. tripod statics
def leg_vectors():
    feet, heads = [], []
    for phi in P["legs_phi"]:
        a = math.radians(phi)
        e = np.array([math.cos(a), math.sin(a), 0.0])
        feet.append(e * P["foot_r"] + np.array([0, 0, P["foot_pin_z"]]))
        heads.append(e * P["head_pin_r"] + np.array([0, 0, D["z_hp"]]))
    return feet, heads


feet, heads = leg_vectors()
head_node = np.mean(heads, axis=0)
c = [(heads[i] - feet[i]) / np.linalg.norm(heads[i] - feet[i]) for i in range(3)]      # foot to head
phi1 = math.radians(P["legs_phi"][0])
u_l = np.array(D["u"])
u_g = np.array([u_l[0] * math.cos(phi1), u_l[0] * math.sin(phi1), u_l[2]])                # head toward foot, leg 1
head_kg = mass["head"] + mass["sheave"] + mass["axle"] + mass["head_pins"]
leg_kg = mass["leg_1"]


def solve(W, alpha_deg=0.0, psi_deg=0.0, rope=True):
    """Leg compressions (kN) at the head for a hook load W (kN) whose line leans alpha from vertical toward psi."""
    a, ps = math.radians(alpha_deg), math.radians(psi_deg)
    hook = np.array([math.sin(a) * math.cos(ps), math.sin(a) * math.sin(ps), -math.cos(a)]) * W / math.cos(a)
    T = W / math.cos(a) / eta_sheave if rope else 0.0
    rope_f = u_g * T                                   # the rope pulls the head toward the winch
    own = np.array([0, 0, -(head_kg + 1.5 * leg_kg) * g / 1000])
    A = hook + rope_f + own
    F = np.linalg.solve(np.array(c).T, -A)
    return F, T


F0, T0 = solve(Wh)
out("C1", f"Legs {P['leg_L'] / 1000:.2f} m pin to pin at {D['leg_angle']:.1f} deg from vertical, feet on a {2 * P['foot_r'] / 1000:.1f} m circle; head plate top {D['z_top'] / 1000:.2f} m above ground", D["leg_angle"], "deg")
out("C2", f"Leg compressions at SWL, hook line vertical: leg 1 (winch) {F0[0]:.2f} kN, leg 2 {F0[1]:.2f} kN, leg 3 {F0[2]:.2f} kN; leg 1 below the winch carries {F0[0] - T0:.2f} kN", F0[0], "kN")
worst = (None, -1e9, None)
minleg = (None, 1e9)
for psi in range(0, 360, 5):
    F, _ = solve(Wh, 10.0, psi)
    if F.max() > worst[1]:
        worst = (psi, F.max(), F)
    if F.min() < minleg[1]:
        minleg = (psi, F.min())
out("C3", f"Hook line leaning 10 deg in the worst direction (psi {worst[0]} deg): largest leg compression {worst[1]:.2f} kN; smallest leg compression in any direction {minleg[1]:.2f} kN (stays in compression, no foot lifts)", worst[1], "kN")
amax = None
for a10 in range(0, 900):
    a = a10 / 10
    if min(solve(Wh, a, psi)[0].min() for psi in range(0, 360, 10)) <= 0:
        amax = a
        break
out("C4", f"A leg first unloads (the tripod would tip) when the hook line leans {amax:.1f} deg from vertical in the worst direction, against 10 deg allowed for guide-line pull and swing", amax, "deg")
# leg 1 strength: axial plus bending from the rope's offset from the leg axis
od, wall = P["tube"]
A_t = math.pi / 4 * (od ** 2 - (od - 2 * wall) ** 2)
I_t = math.pi / 64 * (od ** 4 - (od - 2 * wall) ** 4)
Z_t = I_t / (od / 2)
E_s, fy_leg = 210000.0, 310.0
Lb = P["leg_L"]
Pcr = math.pi ** 2 * E_s * I_t / Lb ** 2 / 1000
Fmax = worst[1]
e = D["rope_offset"]
Mb = T0 * e / 1000                                    # kN m, the rope pull is offset e from leg 1's axis
amp = 1 / (1 - Fmax / Pcr)
sig = Fmax * 1000 / A_t + Mb * 1e6 / Z_t * amp
sig_p = 1.5 * Fmax * 1000 / A_t + 1.5 * Mb * 1e6 / Z_t / (1 - 1.5 * Fmax / Pcr)
out("C5", f"Leg tube {od} x {wall} mm: A {A_t:.0f} mm2, I {I_t / 1e4:.1f} cm4; Euler load pin to pin {Pcr:.1f} kN; buckling factor {Pcr / Fmax:.1f} at SWL with the 10 deg lean (need 3), {Pcr / (1.5 * Fmax):.1f} at proof", Pcr / Fmax, "")
out("C6", f"Leg 1: rope pull {T0:.2f} kN offset {e:.0f} mm from the leg axis bends it by {Mb:.2f} kN m; peak stress {sig:.0f} MPa at SWL, factor {fy_leg / sig:.1f} on a 310 MPa yield (need 3); {sig_p:.0f} MPa at proof", fy_leg / sig, "")
# feet: vertical, thrust, chains, pads
lw = leg_kg * g / 1000 / 2
V = np.array([F0[i] * c[i][2] + lw for i in range(3)])
V[0] -= T0 * (-u_g[2])                                 # the rope pulls leg 1 up at the winch
Fl = [F0[0] - T0, F0[1], F0[2]]                       # leg 1 below the winch carries less: the rope pulls it up
H = [Fl[i] * np.array([c[i][0], c[i][1]]) for i in range(3)]
pts = [np.array(p[:2]) for p in M.chain_eye_points()]
Tch = np.zeros(3)
# feet push outward with -H (leg compression pushes the foot away from the head)
Aeq, beq = [], []
for i in range(3):
    j, k = (i + 1) % 3, (i - 1) % 3
    dj = (pts[j] - pts[i]) / np.linalg.norm(pts[j] - pts[i])
    dk = (pts[k] - pts[i]) / np.linalg.norm(pts[k] - pts[i])
    row_x = np.zeros(3); row_y = np.zeros(3)
    row_x[i] += dj[0]; row_y[i] += dj[1]        # chain i joins foot i and foot i+1
    row_x[k] += dk[0]; row_y[k] += dk[1]        # chain k joins foot i-1 and foot i
    Aeq += [row_x, row_y]; beq += [H[i][0], H[i][1]]
Tch, res, *_ = np.linalg.lstsq(np.array(Aeq), np.array(beq), rcond=None)
out("C7", f"Foot loads at SWL: vertical {V[0]:.2f}, {V[1]:.2f}, {V[2]:.2f} kN; outward thrust {np.linalg.norm(H[0]):.2f}, {np.linalg.norm(H[1]):.2f}, {np.linalg.norm(H[2]):.2f} kN", max(np.linalg.norm(h) for h in H), "kN")
mu = 0.4
out("C8", f"Thrust to vertical ratio {max(np.linalg.norm(H[i]) / V[i] for i in range(3)):.2f} at the feet, above a friction of {mu} on wet timber and soil, so the spread chains are needed; chain tensions {Tch[0]:.2f}, {Tch[1]:.2f}, {Tch[2]:.2f} kN at SWL, {1.5 * Tch.max():.2f} kN at proof, against a 19.6 kN WLL (factor {19.6 / Tch.max():.0f})", Tch.max(), "kN")
pad_A = P["pad"][0] * P["pad"][1] / 1e6
q_allow = 75.0
q = (V.max() + (mass["pads"] / 3 + mass["feet"] / 3) * g / 1000) / pad_A
out("C9", f"Ground pressure under the most loaded pad {q:.0f} kPa at SWL, {1.5 * q:.0f} kPa at proof, against {q_allow:.0f} kPa assumed for soft wet ground (factor {q_allow / q:.1f}); pads 700 mm back from a 3 m rim", q, "kPa")

# ------------------------------------------------------------------ D. head, pins, sheave hangers
Fpin = worst[1] * 1.0
A_pin = math.pi / 4 * P["pin_d"] ** 2
tau = Fpin * 1000 / (2 * A_pin)
out("D1", f"Leg pins 20 mm in double shear: {tau:.0f} MPa at the largest leg load (factor {0.6 * 640 / tau:.0f} on grade 8.8 shear yield); lug bearing {Fpin * 1000 / (2 * P['lug_t'] * P['pin_d']):.0f} MPa, tongue bearing {Fpin * 1000 / (P['tongue'][1] * P['pin_d']):.0f} MPa (S355, factor {355 / (Fpin * 1000 / (P['tongue'][1] * P['pin_d'])):.0f})", tau, "MPa")
R_sh = np.linalg.norm(np.array([0, 0, -Wh]) + u_g * T0)
lat = math.sqrt(R_sh ** 2 - (Wh + T0 * (-u_g[2])) ** 2)
lever = -P["sheave_zc"]
hw, ht = P["hanger"]
Zh = 2 * ht * hw ** 2 / 6
s_h = lat * lever * 1000 / Zh + R_sh * 1000 / (2 * ht * (hw - P["axle_d"]))
out("D2", f"Sheave axle load {R_sh:.2f} kN; hanger plates (two, 120 x 10 mm) {s_h:.0f} MPa from tension and the {lat:.2f} kN side load at {lever:.0f} mm (factor {355 / s_h:.1f} on S355)", s_h, "MPa")
ax_span = P["sheave_w"] + 6 + P["hanger"][1]
Max = R_sh * ax_span / 4
s_ax = Max * 1e3 / (math.pi * P["axle_d"] ** 3 / 32)
out("D3", f"Sheave axle 25 mm, span {ax_span:.0f} mm between hanger centres: bending {s_ax:.0f} MPa (factor {355 / s_ax:.1f} on S355; a grade 8.8 pin gives {640 / s_ax:.1f})", s_ax, "MPa")

# ------------------------------------------------------------------ E. spreader and bands
front = 0.6                                            # share of the animal on the more loaded band (cattle carry weight forward)
Wa = animal * g / 1000
lug_load = Wh - rope_kg_m * fall_max * g / 1000
Rb = front * Wa + (mass["cross_bars"] / 2 + mass["bands"] / 2) * g / 1000
Mbeam = Rb * P["band_y"] / 1000
bl, bh, bw, bt = P["beam"]
Ib = (bw * bh ** 3 - (bw - 2 * bt) * (bh - 2 * bt) ** 3) / 12
Zb = Ib / (bh / 2)
s_b = Mbeam * 1e6 / Zb
out("E1", f"Main beam RHS {bh:.0f} x {bw:.0f} x {bt:.0f}: {front:.0%} of the animal on one band gives {Rb:.2f} kN at {P['band_y']:.0f} mm, moment {Mbeam:.2f} kN m, stress {s_b:.0f} MPa (factor {355 / s_b:.1f} on S355, need 3)", 355 / s_b, "")
cl, cs, ct = P["cross"]
Pt = Rb / 2
arm_t = cl / 2 - 40
Ic = (cs ** 4 - (cs - 2 * ct) ** 4) / 12
s_c = Pt * arm_t * 1000 / (Ic / (cs / 2))
out("E2", f"Cross bar SHS {cs:.0f} x {ct:.0f}: {Pt:.2f} kN at each tip, {arm_t:.0f} mm from the bolts, stress {s_c:.0f} MPa (factor {355 / s_c:.1f})", 355 / s_c, "")
t_lug = P["lift_lug"][2]
s_lug = lug_load * 1000 / (2 * (P["lift_hole_z"] - 0) * 0 + 2 * (40 - P["lift_hole_d"] / 2) * t_lug)
out("E3", f"Lift lug 20 mm, 22 mm hole 40 mm below its top edge: tear-out shear {s_lug:.0f} MPa at SWL (factor {0.6 * 355 / s_lug:.1f} on shear yield); 3.25 t shackle at {lug_load / 31.9:.0%} of WLL", 0.6 * 355 / s_lug, "")
bolt_t = Rb / 2
out("E4", f"Each cross bar hangs on two M16 grade 8.8 bolts: {bolt_t:.2f} kN per bolt against 113 kN proof load", bolt_t, "kN")
leg_T = front * Wa / 2
out("E5", f"Band leg tension {leg_T:.2f} kN ({leg_T / g * 1000:.0f} kg) against the sling's 8 t vertical WLL; 1 t shackles and 8 mm grade 80 chain at {leg_T / 9.81:.0%} and {leg_T / 19.6:.0%} of WLL", leg_T, "kN")
contact = math.pi * P["band_r"] / 1000 * 0.8
p_band = front * Wa / (P["band"][0] / 1000 * contact)
out("E6", f"Band pressure on the animal: {front:.0%} of {animal:.0f} kg over a 240 mm band in contact for {contact:.2f} m: {p_band:.0f} kPa average (estimate; two bands instead of one halve it)", p_band, "kPa")

# ------------------------------------------------------------------ F. landing bridge
span = 2 * P["bearer_y"]
L_r, h_r, w_r, t_r = P["runner"]
Ir = (w_r * h_r ** 3 - (w_r - 2 * t_r) * (h_r - 2 * t_r) ** 3) / 12
Zr = Ir / (h_r / 2)
share, dyn, hoof_gap = 0.4, 1.25, 1.2
Pr = share * Wa * dyn
Mr = Pr / 2 * (span / 2000 - hoof_gap / 2)
s_r = Mr * 1e6 / Zr
d_r = (Pr / 2 * 1000) * (span / 2 - hoof_gap * 500) * (3 * span ** 2 - 4 * (span / 2 - hoof_gap * 500) ** 2) / (24 * E_s * Ir)
out("F1", f"Runner RHS {h_r:.0f} x {w_r:.0f} x {t_r:.0f}, span {span / 1000:.1f} m between bearers: animal standing (hooves 1.2 m apart), {share:.0%} on one runner, x {dyn} for landing: {s_r:.0f} MPa (factor {355 / s_r:.1f}, need 3), deflection {d_r:.0f} mm", 355 / s_r, "")
Pc = Wa * share * dyn
body = 1.6
Mc = Pc * (span / 4000 - body / 8)
out("F2", f"Animal lying, its weight spread over {body} m of body at mid-span, {share:.0%} on one runner: {Mc * 1e6 / Zr:.0f} MPa (factor {355 / (Mc * 1e6 / Zr):.1f})", 355 / (Mc * 1e6 / Zr), "")
hoof = Wa / 4 * dyn
Mp = hoof * 0.5 / 4
s_p = Mp * 1e6 / (300 * P["deck"][2] ** 2 / 6)
out("F3", f"Deck 25 mm plywood over 500 mm runner centres, one hoof ({hoof:.2f} kN) at mid-span on a 300 mm strip: {s_p:.1f} MPa against about 25 MPa characteristic (factor {25 / s_p:.1f})", 25 / s_p, "")
bridge_kg = mass["runners"] + mass["deck"] + mass["cleats"]
Rbear = (Wa * dyn + bridge_kg * g / 1000) / 2
qb = Rbear / (P["bearer"][0] * P["bearer"][1] / 1e6)
out("F4", f"Each rim bearer carries {Rbear:.2f} kN: {qb:.0f} kPa on the ground (factor {q_allow / qb:.1f} on {q_allow:.0f} kPa), its near edge {P['bearer_y'] - P['bearer'][1] / 2 - P['well_d'] / 2:.0f} mm back from a 3 m rim", qb, "kPa")
out("F5", f"Hooves {D['hoof_clear']:.0f} mm above the deck at the landing height with 300 mm of adjusting chain; deck top {D['deck_top']:.0f} mm above ground", D["hoof_clear"], "mm")

# ------------------------------------------------------------------ G. mass, cost, reach, setup
pieces = {"Tripod leg": mass["leg_1"], "Tripod head": mass["head"], "Hand winch": mass["winch"],
          "Bridge runner": mass["runners"] / 3, "Deck panel with cleats": (mass["deck"] + mass["cleats"]) / 3,
          "Rim bearer": mass["bearers"] / 2, "Spreader main beam": mass["beam"], "Foot plate": mass["feet"] / 3}
heavy = max(pieces, key=pieces.get)
total = sum(v for k, v in mass.items() if k not in ("head_pins", "foot_pins")) + mass["head_pins"] + mass["foot_pins"] + 6.0 + 4.0
out("G1", f"Heaviest single piece: {heavy}, {pieces[heavy]:.1f} kg (need at most 35 kg); whole kit about {total:.0f} kg including lines and passer", pieces[heavy], "kg")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
target = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
out("G2", f"Value-engineering target: USD {target:,.0f}. Estimated cost of the constructable design: USD {cost:,.2f} (USD {cost - target:,.2f} over the target)", cost, "USD")
reach = 8 * P["pole"][2] / 1000 + 0.5
out("G3", f"Passer reach: eight 2 m sections and the J-head give {reach:.1f} m below the top hand (need 15 m); one pole weighs {mass['passer_poles'] / 2 + mass['jhead']:.1f} kg with its head", reach, "m")
tasks = [("Unload and lay out the kit at the well", 3), ("Set out the three pads with the marked setting-out line, drive six stakes", 4),
         ("Pin the legs to the head on the ground, fit the winch, reeve the rope", 4), ("Walk the tripod up and pin the feet", 3),
         ("Fit the three spread chains and tension them", 2), ("Assemble the spreader and hang it on the hook", 2), ("Briefing and checks at the safety stop", 2)]
t_set = sum(t for _, t in tasks)
out("G4", f"Set-up by three people, task by task (estimate): {t_set} min to the first lift against 20 min (passing the bands is extra and depends on the animal)", t_set, "min")

with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tag", "result", "value", "unit"])
    w.writerows(OUT)
