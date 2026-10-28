"""WellSling STEM check (WSL-STM-001, STANDARDS section 20).

Run from the repo root after the sizing note:
    python docs/04-calcs/sizing.py        (writes docs/04-calcs/results.csv)
    python docs/04-calcs/stem_check.py    (writes docs/04-calcs/stem_results.csv)

Every physical, chemical and biological claim the idea and its three concept options make, each with a
first-order check against a governing law, a limit or a cited source. Option A figures are read from the
calculation note's results (WSL-CAL-001) or recomputed here from the parametric model (cad/src/model.py);
options B and C are checked from first principles below. The kit 1.7 figures that failed (leg 1 with an initial
bow, three joints that could not be assembled) are recomputed here so the record shows what the fix changed.
First-order screening only; nothing here replaces a proof-load test (TRL 4).
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from stem_check import Check, limits, WITHIN, PLAUSIBLE, FIX, FAILS, G  # noqa: E402
import model as M  # noqa: E402

P, D = M.PARAMS, M.derived()
R = {r["tag"]: float(r["value"]) for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open()) if r["value"]}
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
CAL = "WSL-CAL-001"

# ------------------------------------------------------------------ option A: loads, rope, winch
W_kN = R["A2"]
c.balance("S1", f"Hook load {W_kN:.2f} kN for a 600 kg animal and its rigging", "Physics", "Mechanics and statics",
          inputs={"hook": W_kN}, outputs={"animal": 600 * G / 1000, "rigging and hanging rope": (R["A2"] * 1000 / G - 600) * G / 1000},
          unit="kN", law="Weight W = m g; the hook carries the animal, the rigging below it and the hanging rope", closed_by=f"{CAL} A1, A2")
c.claim("S2", f"Wire rope safety factor {R['B1']:.1f} on the bare rope and {0.9 * R['B1']:.1f} with its pressed ferrule eye", "Physics", "Strength of materials",
        law="Rope tension through a 97 % sheave against the 40 kN minimum breaking load of 8 mm 6 x 19 IWRC 1770 rope, times 0.9 for a ferrule-secured eye (catalogue class); 5 required (CAL assumption 5), above the 3.15 to 3.35 of ISO 4308-1 for mechanism groups M1 and M2",
        value=round(0.9 * R["B1"], 2), limit=5.0, unit="", rule="above", closed_by=f"{CAL} B1; independent review")
c.claim("S3", "Sheave pitch diameter to rope diameter ratio 25", "Engineering and technology", "Standards practice",
        law="Bending fatigue of wire rope grows as D/d falls; 18 used as the screening minimum (CAL assumption 5)",
        value=R["B2"], limit=18.0, unit="", rule="above", closed_by=f"{CAL} B2")
c.claim("S4", f"Winch pull on the third rope layer covers the rope tension ({R['B5']:.0%} used)", "Physics", "Mechanics and statics",
        law="Drum torque fixed by the gearbox: pull falls in proportion to the layer radius (rated 1,000 kg on layer 1)",
        value=R["B5"], limit=1.0, unit="(share of capacity)", rule="below", closed_by=f"{CAL} B5")
turns = 2.0 / (math.pi * (2 * P["drum_r"] + P["rope_d"]) / 1000)
c.claim("S5", f"At least three dead turns stay on the drum with the animal 15 m down ({turns:.1f} turns), as well as the drum's rope clamp", "Engineering and technology", "Standards practice",
        law="The rope end is held by the winch's own clamp; the dead turns take most of the tension off it by friction; three turns used as the screening minimum",
        value=round(turns, 1), limit=3.0, unit="turns", rule="above", closed_by=f"{CAL} B4")
c.cited("S6", f"Crank force at most 250 N through the lift ({R['B6']:.0f} N at the landing height)", "Biology", "Ergonomics",
        law="Handle force scales with rope tension and layer radius from a catalogue-class 230 N at the rated load (CAL assumption 9)",
        detail=f"{R['B6']:.0f} N against the 250 N target (PR-011); rests on the handle force of the winch bought, not yet confirmed. To close: winch datasheet and a force gauge at TRL 4 (WSL-DEC-001 item 1)",
        verdict=PLAUSIBLE, closed_by="")
E_lift = W_kN * 17.6
c.balance("S7", f"Crank work {R['B8'] * 0 + (E_lift / 0.8 / 0.97):.0f} kJ covers {E_lift:.0f} kJ of lift and the gear and sheave losses", "Physics", "Thermodynamics",
          inputs={"crank work": E_lift / (0.80 * 0.97)}, outputs={"lift m g h": E_lift, "winch losses (20 %)": E_lift / (0.80 * 0.97) * 0.20,
                                                                    "sheave loss (3 %)": E_lift / 0.97 * 0.03},
          unit="kJ", law="Conservation of energy, W = m g h plus friction losses", closed_by=f"{CAL} B8, B9")
crank_w = R["B6"] * 2 * math.pi * P["crank_arm"] / 1000 * 15 / 60
c.claim("S8", f"Whoever cranks works at about {crank_w:.0f} W near the top for a turn of 2 to 3 minutes; in a crew of three each averages {crank_w / 3:.0f} W", "Biology", "Human physiology and biomechanics",
        law="Short bouts up to about 300 W and about 75 W sustained (kit limits); the 94 W is above the sustained figure, so turns are short",
        value=round(crank_w, 1), limit=limits.HUMAN_PEAK_W, unit="W while cranking", rule="below", closed_by=f"{CAL} B8; independent review")
c.order_of_magnitude("S9", f"A 15 m lift takes about {R['B8']:.0f} min at 15 crank turns a minute", "Mathematics", "Orders of magnitude",
                     claimed=R["B8"], estimate=18.2 / (2 * math.pi * 0.058 / 9.6 * 15), unit="min",
                     law="Rope speed = drum circumference / gear ratio x crank speed (mean layer radius about 58 mm)", closed_by=f"{CAL} B8")

# ------------------------------------------------------------------ option A: tripod
c.claim("S10", f"Tripod does not tip with the hook line leaning 10 deg (tips at {R['C4']:.1f} deg)", "Physics", "Mechanics and statics",
        law="Static equilibrium of the three-leg frame with the rope pull on the head; a leg unloads when its compression reaches zero",
        value=R["C4"], limit=10.0, unit="deg", rule="above", closed_by=f"{CAL} C3, C4")
c.claim("S11", f"Leg buckling factor {R['C5']:.1f} at the safe working load", "Physics", "Strength of materials",
        law="Euler load of a pinned 4.5 m strut, pi^2 E I / L^2; factor 3 required", value=R["C5"], limit=3.0, unit="", rule="above", closed_by=f"{CAL} C5")
# leg 1 with an initial bow: the kit 1.7 tube and the tube fitted under the fix rule
def leg1(od, t, N=R["C3"], T=R["A3"], e=D["rope_offset"], L=P["leg_L"], fy=310.0):
    A = math.pi / 4 * (od ** 2 - (od - 2 * t) ** 2)
    I = math.pi / 64 * (od ** 4 - (od - 2 * t) ** 4)
    Z = I / (od / 2)
    Pcr = math.pi ** 2 * 210000 * I / L ** 2 / 1000
    amp = 1 / (1 - N / Pcr)
    amp_m = 1 / math.cos(math.pi / 2 * math.sqrt(N / Pcr))
    s = N * 1000 / A + (T * e * 1000 * amp_m + N * 1000 * L / 200 * amp) / Z
    return fy / s, s
old_f, old_s = leg1(76.1, 3.6, N=10.85, T=6.55)          # kit 1.7 tube at the kit 1.7 loads (WSL-CAL-001 v0.1 C3, A3)
new_f, new_s = leg1(*P["tube"])
c.claim("S12", f"Leg 1 (winch leg) stays below a third of yield in combined compression and bending with an initial bow of L/200 "
        f"(kit 1.7 tube 76.1 x 3.6 at its own loads: factor {old_f:.2f}; now 88.9 x 3.2: factor {new_f:.1f})", "Physics", "Strength of materials",
        law="Second-order elastic stress with an equivalent bow e0 = L/200 (EN 1993-1-1 Table 5.1, curve c, cold-formed hollow section); factor 3 required",
        value=round(new_s, 1), limit=round(310 / 3, 1), unit="MPa", rule="below", closed_by="WSL-DEC-001 D10 (was Fails, fix proposed); CAL C6")
c.claim("S13", f"Spread chains stop the feet sliding: thrust is 0.59 of the foot load, above timber-on-wet-soil friction; each chain crosses {R['C11'] * 0 + 1.77:.2f} m of a 3 m well mouth near its edge, taut", "Physics", "Mechanics and statics",
        law="Coulomb friction 0.4 (CAL assumption 12) against the leg thrust; the chains take the difference (factor 22 on their working load limit); catenary sag w L^2 / 8 T",
        value=0.59, limit=0.4, unit="(thrust / vertical)", rule="above", closed_by=f"{CAL} C7, C8")
c.cited("S14", f"Soft wet ground carries the pads at {R['C9']:.0f} kPa, {R['C10']:.0f} kPa with the hook line leaning 10 deg", "Physics", "Mechanics and statics",
        law="Bearing pressure = foot load / pad area, against 75 kPa assumed for soft wet ground (CAL assumption 12) and 40 kPa at the low end of soft clay",
        detail=f"{R['C9']:.0f} kPa at the safe working load with the hook line vertical; {R['C10']:.0f} kPa at SWL and {1.5 * R['C10']:.0f} kPa at proof with the 10 deg lean, below 40 kPa; a pad near the shaft has a smaller bearing wedge. To close: bearing check at the first trial site, TRL 4 (WSL-DEC-001 item 4)",
        verdict=PLAUSIBLE, closed_by="")
# rim surcharge, 2:1 load spread to the depth where the spread reaches the well wall
pad_x = P["foot_r"] - P["pad"][0] / 2 - P["well_d"] / 2
z_pad = 2 * pad_x / 1000
q_pad = R["C9"] * P["pad"][0] / 1000 * P["pad"][1] / 1000 / ((P["pad"][0] / 1000 + z_pad) * (P["pad"][1] / 1000 + z_pad))
bear_x = P["bearer_y"] - P["bearer"][1] / 2 - P["well_d"] / 2
z_b = 2 * bear_x / 1000
q_b = R["F4"] * P["bearer"][0] / 1000 * P["bearer"][1] / 1000 / ((P["bearer"][0] / 1000 + z_b) * (P["bearer"][1] / 1000 + z_b))
c.cited("S15", f"Pads and bearers add little to the earth pressure on the well wall ({q_pad:.1f} and {q_b:.1f} kPa where the load spread reaches it), and the rim and lining hold",
        "Physics", "Mechanics and statics",
        law="2:1 load spread under a footing, compared with the overburden of soil at that depth (about 18 kN/m3); the strength of an old brick or dry-stone lining is not known",
        detail=f"Added stress at most {max(q_pad / (18 * z_pad), q_b / (18 * z_b)):.2f} of the overburden; the lining that actually fails is the unknown, so the rim and lining are a go or no-go check at every well (WSL-BLD-001 safety stop S4). To close: site check at every well",
        verdict=PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------ option A: head, spreader, bands, bridge
c.claim("S16", "Leg pins in double shear far below grade 8.8 shear yield", "Physics", "Strength of materials",
        law="tau = F / (2 A); grade 8.8 shear yield about 0.6 x 640 MPa", value=R["D1"], limit=0.6 * 640 / 3, unit="MPa", rule="below", closed_by=f"{CAL} D1")
c.claim("S17", "Sheave axle bending within a third of S355 yield", "Physics", "Strength of materials",
        law="Simply supported pin, M = F L / 4, sigma = M / (pi d^3 / 32)", value=R["D3"], limit=355 / 3, unit="MPa", rule="below", closed_by=f"{CAL} D3")
c.claim("S18", f"Spreader beam bending factor {R['E1']:.1f}", "Physics", "Strength of materials",
        law="Cantilever moment from 60 % of the animal on one band; factor 3 on S355", value=R["E1"], limit=3.0, unit="", rule="above", closed_by=f"{CAL} E1")
c.claim("S19", f"Spreader cross bar bending factor {R['E2']:.1f}", "Physics", "Strength of materials",
        law="Cantilever from the bolts to the tip lug; factor 3 on S355", value=R["E2"], limit=3.0, unit="", rule="above", closed_by=f"{CAL} E2")
c.claim("S20", f"Band end yoke bars bending factor {R['E7']:.1f}", "Physics", "Strength of materials",
        law="Simply supported 25 mm bar, band leg at mid span; factor 3 on S355", value=R["E7"], limit=3.0, unit="", rule="above", closed_by=f"{CAL} E7")
c.claim("S21", f"Bridge runner bending factor {R['F2']:.1f} with the animal lying at mid span", "Physics", "Strength of materials",
        law="Simply supported RHS over 4.0 m, 1.25 x the animal on landing, 40 % on one runner", value=min(R["F1"], R["F2"]), limit=3.0, unit="", rule="above", closed_by=f"{CAL} F1, F2")
c.claim("S22", f"Plywood deck bending factor {R['F3']:.1f} under one hoof", "Physics", "Strength of materials",
        law="Plate strip of 300 mm over 500 mm runner centres; about 25 MPa characteristic bending strength of exterior plywood (CAL assumption 15)",
        value=R["F3"], limit=3.0, unit="", rule="above", closed_by=f"{CAL} F3")
c.claim("S23", f"Hooves clear the deck by {R['F5']:.0f} mm at the landing height, so the bridge slides under", "Mathematics", "Units and dimensional analysis",
        law="Stack of heights from the head sheave down to the hooves, from the model", value=R["F5"], limit=150.0, unit="mm", rule="above", closed_by=f"{CAL} F5")
# band pressure: the CAL's contact-length estimate and the hoop formula for a band wrapped at radius R
T_leg = R["E5"] * 1000
p_hoop = T_leg / (P["band"][0] / 1000 * P["band_r"] / 1000) / 1000
c.order_of_magnitude("S24", f"Average band pressure on the animal about {R['E6']:.0f} kPa", "Mathematics", "Orders of magnitude",
                     claimed=R["E6"], estimate=p_hoop, unit="kPa", law="Belt on a drum: p = T / (w R) for each leg tension T over band width w at wrap radius R",
                     closed_by=f"{CAL} E6")
c.cited("S25", f"Two plain bands at about {R['E6']:.0f} to {p_hoop:.0f} kPa for about {R['B8']:.0f} min do not injure a 600 kg cow or buffalo", "Biology", "Plant and animal biology",
        law="Large-animal rescue practice favours wide padded bands under chest and flank and short suspension; no tolerable pressure or time for cattle was found in a cited source",
        detail="No cited threshold; held as a question for the veterinary partner (sling width, pressure, chest and flank share, suspension time, risk of regurgitation). To close: veterinary review before any live lift, TRL 4 (WSL-DEC-001 item 5)",
        verdict=PLAUSIBLE, closed_by="")
pole_od, pole_t, _ = P["pole"]
Ip = math.pi / 64 * (pole_od ** 4 - (pole_od - 2 * pole_t) ** 4)
F_push = math.pi ** 2 * 69000 * Ip / 16000 ** 2
c.cited("S26", f"The passer pole, held from the rim, can push the J-head under a lying animal 15 m down (pole Euler load about {F_push:.0f} N)",
        "Physics", "Strength of materials",
        law="A 16 m, 40 x 2 mm aluminium pole buckles at pi^2 E I / L^2 if pushed end-on; the pole's own 17.6 kg hangs from the top hand, so the push at the head is its weight plus that",
        detail=f"Euler load {F_push:.0f} N pinned over 16 m, weight about 173 N; the force needed to slide the J under an animal in mud is not known. To close: dummy trial in a test pit, TRL 4 (WSL-BLD-001 first checks)",
        verdict=PLAUSIBLE, closed_by="")
c.claim("S27", f"Passer reaches {R['G3']:.1f} m below the rim", "Mathematics", "Units and dimensional analysis",
        law="Eight 2 m sections and the J-head below the top hand", value=R["G3"], limit=15.0, unit="m", rule="above", closed_by=f"{CAL} G3")

# ------------------------------------------------------------------ chemistry
c.cited("S28", "Hot-dip galvanising keeps the steel parts from rusting for decades beside a well", "Chemistry", "Environmental and atmospheric chemistry",
        law="Zinc corrosion rate 0.1 to 0.7 um/a (C2, rural), 0.7 to 2.1 um/a (C3) and 2.1 to 4.2 um/a (C4) (ISO 9223, via AGA); mean coating 70 um on 3 to 6 mm steel and 85 um over 6 mm (EN ISO 1461:2022)",
        detail="70 um at 2.1 to 4.2 um/a = 17 to 33 years beside a well with manure and splash (C3 to C4); longer in dry storage; worn surfaces (pin holes, sheave groove) lose their zinc and are inspected",
        verdict=WITHIN, closed_by="AGA (2026); Wedge Galvanizing (2024)")
c.cited("S29", "Plain polyester webbing bands suit wet, muddy wells", "Chemistry", "Materials and polymer chemistry",
        law="Polyester is resistant to most mineral acids but is damaged by alkalis (sling user instructions to EN 1492-1)",
        detail="Water and mud do not weaken polyester; lime, ash, cement slurry, manure slurry and strong alkaline cleaners can: wash in clean water, dry out of the sun, and inspect for abrasion, cuts and hoof damage before each use",
        verdict=WITHIN, closed_by="Certex Powertex user manual (checked 2026-10-25); WSL-BLD-001 care notes")

# ------------------------------------------------------------------ biology: the hazard the kit removes
c.cited("S30", "Air at the bottom of a well can be low in oxygen or hold toxic gas, so a person can collapse within seconds; working from the rim removes that exposure",
        "Biology", "Toxicology",
        law="Oxygen-deficient and toxic atmospheres in confined spaces (NIOSH FACE 85-02; CDC MMWR 1989)",
        detail="Several rescuers die in a row when each goes down after the last; the kit's method needs nobody below the rim at any stage",
        verdict=WITHIN, closed_by="WSL-PRB-001 sources")

# ------------------------------------------------------------------ engineering: joints that must assemble (found while detailing to D3)
c.cited("S31", "Every spread chain shackle has a hole of its own and pulls in line with its chain", "Engineering and technology", "Manufacturing tolerances",
        law="One pin per hole; a shackle loaded off its centre line loses working load (manufacturers' side-load rules)",
        detail="Kit 1.7: one 20 mm chain eye per foot for the shackles of two chains, drawn with a vertical pin through a horizontal hole: it could not be assembled. Now two fins per foot, each square to its chain, and chains with enlarged end links",
        verdict=WITHIN, closed_by="WSL-DEC-001 D11 (was Fails, fix proposed)")
c.cited("S32", "All four winch base bolts can be fitted with the bracket welded on leg 1", "Engineering and technology", "Manufacturing tolerances",
        law="A bolt and nut need clear space beside the tube under the bracket",
        detail="Kit 1.7: the bolt pattern was centred 70 mm off the leg's centre line, so one row of holes sat 10 mm from it, over the tube. Now the bracket is 300 x 300 mm and the pattern is centred 140 mm to the side: both rows clear the tube by 5 mm or more",
        verdict=WITHIN, closed_by="WSL-DEC-001 D12 (was Fails, fix proposed)")
c.cited("S33", "The 240 mm band eye bears on a straight bar across its full width", "Engineering and technology", "Standards practice",
        law="Webbing slings wider than 75 mm should bear on an essentially straight part of the lifting attachment; the eye angle should not exceed 20 deg (sling user instructions to EN 1492-1)",
        detail="Kit 1.7 shackled each 240 mm sewn eye straight onto a 1 t bow shackle with a 16 mm jaw: it could not be fitted and would have loaded the webbing at its edges. Now a band end yoke: a removable 25 mm bar 258 mm between side plates through the eye",
        verdict=WITHIN, closed_by="WSL-DEC-001 D13 (was Fails, fix proposed); CAL E7")
c.cited("S35", "The guide line eyes on the spreader beam clear the end sleeves and the cross bar bolts", "Engineering and technology", "Manufacturing tolerances",
        law="Two parts cannot occupy the same space; a bolt head and washer need a clear seat",
        detail="Kit 1.7: a 60 mm eye plate stood on the beam top 35 mm from each end, over the sleeve and M16 bolt at 500 mm. Now each eye is welded to an end cap and points along the beam",
        verdict=WITHIN, closed_by="WSL-DEC-001 D17 (was Fails, fix proposed)")
c.cited("S34", "Three people set up the kit in about 20 minutes", "Engineering and technology", "Standards practice",
        law="Task-by-task time estimate (CAL G4)", detail="20 min against 20 min: at the limit, and passing the bands is extra. To close: timed drill, TRL 4 (WSL-BLD-001 first checks)",
        verdict=PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------ added after the independent review (2026-10-25)
c.cited("S36", "A frightened animal kicking in the bands stays within the 1.5 times proof margin", "Physics", "Acoustics and vibration",
        law="Dynamic load on a hanging mass; the automatic brake allows no free fall, and the bands and rope stretch act as a spring",
        detail="At a dynamic factor of 1.5 the rope is at 4.0 on its break and the steel at its proof stresses (leg 1 136 MPa, factor 2.3 on yield). A slip or a sudden catch could give more; the dynamic factor of a kicking 600 kg animal is not known. To close: load cell on the hook during the dummy trial, TRL 4",
        verdict=PLAUSIBLE, closed_by="")
Dd = (2 * P["drum_r"] + P["rope_d"]) / P["rope_d"]
c.claim("S37", f"Winch drum pitch diameter to rope diameter ratio {Dd:.1f}", "Engineering and technology", "Standards practice",
        law="ISO 4308-1 Table 2: drum coefficient h1 at least 11.2 for mechanism group M1 and 12.5 for M2 (a rescue kit is used rarely)",
        value=round(Dd, 1), limit=12.5, unit="", rule="above", closed_by="ISO 4308-1; independent review")
torque_proof = 1.5 * R["A3"] * (P["drum_r"] + P["rope_d"] / 2 + 2 * 0.93 * P["rope_d"]) / 1000
torque_test = 1.5 * 9.81 * (P["drum_r"] + P["rope_d"] / 2) / 1000
c.claim("S38", f"The winch holds the kit's 1.5 times proof load on its third layer ({torque_proof:.2f} kN m at the drum)", "Engineering and technology", "Standards practice",
        law="Drum torque = rope tension x layer radius; the winch is bought statically tested by its maker to 1.5 times its rated load on the first layer",
        value=round(torque_proof, 3), limit=round(torque_test, 3), unit="kN m", rule="below", closed_by="WSL-DEC-001 D18 (was Fails, fix proposed: the proof exceeded the winch's working rating on layer 3)")
c.cited("S39", "The winch can break the animal free of mud at the bottom of the well", "Physics", "Fluid mechanics",
        law="Suction and adhesion of wet mud add to the weight when a body is pulled out; no figure for a 600 kg animal was found",
        detail="If the crank force rises past 250 N with no movement, the crew stops and does not force it (WSL-BLD-001 safety stop S5); the breakout force is not known. To close: dummy trial in a mud-bottomed test pit, TRL 4",
        verdict=PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------ option B: portable gantry and two chain hoists
Wa = 600 * G / 1000
span_B = 2 * P["B_frame_y"]
loads_B = (0.6 * Wa + 0.25, 0.4 * Wa + 0.25)          # kN at y = +450 and -450, rigging about 25 kg per band
RA = (loads_B[0] * (span_B / 2 + P["band_y"]) + loads_B[1] * (span_B / 2 - P["band_y"])) / span_B
M_B = RA * (span_B / 2 - P["band_y"]) / 1000            # kN m under the heavier load
h, b, t = P["B_beam"]
Ib = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12
s_B = M_B * 1e6 / (Ib / (h / 2))
c.claim("B1", f"Option B: gantry beam RHS 140 x 80 x 4 over {span_B / 1000:.1f} m, bending factor {355 / s_B:.1f}", "Physics", "Strength of materials",
        law="Simply supported beam, two hoist loads 900 mm apart (60 % and 40 % of the animal); factor 3 on S355", value=round(355 / s_B, 2), limit=3.0, unit="", rule="above")
Ls = math.hypot(P["B_foot_x"] - 70.0, 3200.0)
Is = (60 ** 4 - 54 ** 4) / 12
Pcr_B = math.pi ** 2 * 210000 * Is / Ls ** 2 / 1000
leg_B = RA / 2 / (3200.0 / Ls)
c.claim("B2", f"Option B: A-frame legs SHS 60 x 3, Euler factor {Pcr_B / leg_B:.0f}", "Physics", "Strength of materials",
        law="Euler load of a pinned strut; each leg carries half the end reaction along its axis", value=round(Pcr_B / leg_B, 1), limit=3.0, unit="", rule="above")
c.cited("B3", "Option B: hand chain pull stays within one person's reach (about 120 N per hoist at 0.4 of a 1 t rating)", "Biology", "Ergonomics",
        law="Hand chain pull scales with load from a catalogue-class 300 N at the rated load (assumed, not cited)",
        detail="Two operators must pull together to keep the animal level; the hand chains hang over the well mouth and are pulled from the rim at an angle. Not carried forward unless option chosen",
        verdict=PLAUSIBLE, closed_by="")
half_mass = (2 * (h + b) - 4 * t) * t * 7.85e-3 * (P["B_beam_L"] / 2 - P["B_splice_y"]) / 1000
half_old = (2 * (h + b) - 4 * t) * t * 7.85e-3 * P["B_beam_L"] / 2 / 1000
c.claim("B4", f"Option B: heaviest beam piece within a two-person carry of 35 kg (two halves: {half_old:.1f} kg; three sections: {half_mass:.1f} kg)", "Biology", "Ergonomics",
        law="Mass of steel = density x volume; 35 kg two-person carry limit (PR-013)", value=round(half_mass, 1), limit=35.0, unit="kg", rule="below",
        closed_by="WSL-DEC-001 D14, option B model (was Fails, fix proposed)")

# ------------------------------------------------------------------ option C: sheerlegs and draught haul
z_ap = 4100.0
yF = abs(P["C_foot_y"])
W_C = R["A2"]
M_tip = W_C * yF / 1000
apex, anchor = (0.0, z_ap), (P["C_anchor_y"], 160.0)
dy, dz = anchor[0] - apex[0], anchor[1] - apex[1]
Lg = math.hypot(dy, dz)
arm = abs((-yF - apex[0]) * dz - (0.0 - apex[1]) * dy) / Lg / 1000
G_C = M_tip / arm
c.cited("C1", f"Option C: the back guy ({G_C:.1f} kN) is held by a staked anchor plate in soft ground", "Physics", "Mechanics and statics",
        law="Moment of the hook load about the feet line taken by the guy's lever arm; anchor holding in soil depends on the soil and stake depth",
        detail=f"Guy tension {G_C:.1f} kN at {math.degrees(math.atan2(-dz, -dy)):.0f} deg; no holding capacity for a staked plate in wet soil was found in a cited source. A pull test would close it if option C were chosen",
        verdict=PLAUSIBLE, closed_by="")
trac = 2000 * G * 0.4 / 1000
c.order_of_magnitude("C2", f"Option C: a farm tractor can haul the {R['A3']:.1f} kN rope tension", "Physics", "Mechanics and statics",
                     claimed=R["A3"], estimate=trac, unit="kN", law="Drawbar pull about 0.4 x the weight of a 2 t tractor on soft ground (traction coefficient, order of magnitude)")
mu, turns_post = 0.15, 3
hold = R["A3"] * 1000 / math.exp(mu * 2 * math.pi * turns_post)
c.claim("C3", f"Option C: three turns on the snubbing post let one person hold the load with about {hold:.0f} N", "Physics", "Mechanics and statics",
        law="Capstan equation T1 / T2 = exp(mu theta), steel rope on a steel post mu about 0.15; 400 N taken as a short two-handed pull (assumed)", value=round(hold), limit=400.0, unit="N", rule="below")
c.cited("C4", "Option C: a tractor can lift the animal smoothly and stop on command", "Engineering and technology", "Control",
        law="A tractor at creep speed raises the animal 17.6 m in about a minute; a jerk or a missed stop loads the rope and the animal suddenly",
        detail="Control rests on the driver and a signaller; no brake holds the load except the post turns. Not carried forward unless option chosen",
        verdict=PLAUSIBLE, closed_by="")
Lc = math.sqrt((P["C_foot_x"] - 85.0) ** 2 + yF ** 2 + (z_ap - 120.0) ** 2)
od, wt = P["tube"]
Ic = math.pi / 64 * (od ** 4 - (od - 2 * wt) ** 4)
Pcr_C = math.pi ** 2 * 210000 * Ic / Lc ** 2 / 1000
legC = (W_C + R["A3"]) / 2 / ((z_ap - 120.0) / Lc) + G_C * 0.53 / 2
Ac = math.pi / 4 * (od ** 2 - (od - 2 * wt) ** 2)
sC = legC * 1000 / Ac + legC * 1000 * Lc / 200 / (1 - legC / Pcr_C) / (Ic / (od / 2))
c.claim("C5", f"Option C: sheerlegs CHS 88.9 x 3.2, {Lc / 1000:.2f} m, Euler factor {Pcr_C / legC:.1f}, factor {310 / sC:.1f} on yield with an initial bow of L/200", "Physics", "Strength of materials",
        law="Euler load of a pinned strut against the leg force from the hook load, the rope fall and the guy; second-order stress with a bow of L/200 (EN 1993-1-1)", value=round(min(Pcr_C / legC, 310 / sC), 2), limit=3.0, unit="", rule="above")

state = c.write()
print("stem_check:", state)
