"""WellSling prototype build plan pictures (WSL-BLD-001, STANDARDS section 18).

Run from the repo root:
    python cad/src/build_plan_media.py                       everything (heavy: better one group per process)
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py, so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/WSL-DWG-101 to 115        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P  # noqa: E402
from build123d import Box, Pos, Rot, Compound  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = m.derived(P)
X0, Y0 = D["drop"]
_C = None

COL = {"legs": "#64748B", "head": "#0F766E", "sheave": "#B45309", "pins": "#111827", "feet": "#1D4ED8",
       "pads": "#A16207", "stakes": "#374151", "spread_chains": "#78716C", "winch": "#C2410C", "bracket": "#7C3AED",
       "rope": "#111827", "hook": "#DC2626", "beam": "#0E7490", "cross_bars": "#15803D", "cross_bolts": "#111827",
       "shackles": "#57534E", "adj_chains": "#57534E", "bands": "#EAB308", "felt": "#A8A29E", "bearers": "#92400E",
       "runners": "#475569", "deck": "#D6A461", "cleats": "#92400E", "passer": "#94A3B8", "jhead": "#B91C1C"}


def comps():
    global _C
    if _C is None:
        _C = m.build_components(P)
    return _C


def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box (for close-ups)."""
    w = bx(x0, x1, y0, y1, z0, z1)
    try:
        sols = list(shape.solids()) or [shape]
    except Exception:
        sols = [shape]
    kept = []
    for s_ in sols:
        bb = s_.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        try:
            r = s_ & w
            if r is not None and r.volume > 1e-3:
                kept.append(r)
        except Exception:
            pass
    return Compound(children=kept) if kept else None


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def K(key, name, explode=(0, 0, 0), color=None, col=None):
    return part(name, comps()[key], color or COL.get(col or key, "#64748B"), explode)


def W(key, name, box, explode=(0, 0, 0), color=None, col=None):
    s = win(comps()[key], *box)
    return None if s is None else part(name, s, color or COL.get(col or key, "#64748B"), explode)


def fuse(*keys):
    s = None
    for k in keys:
        s = comps()[k] if s is None else s + comps()[k]
    return s


def legs():
    return fuse("leg_1", "leg_2", "leg_3")


def keep(ps):
    return [p for p in ps if p is not None]


# single components in their own frame (one of several)
P1 = dict(P, legs_phi=(0.0,))


def one_foot():
    f = m._feet(P1, D)
    return f


def leg_flat():
    """One leg laid along X for the three views."""
    lg = m._leg_local(P, D)
    s = lg["tube"] + lg["caps"] + lg["tongues"]
    best = None
    for ang in (D["leg_angle"] - 90, 90 - D["leg_angle"], D["leg_angle"] + 90, -D["leg_angle"] - 90):
        r = Rot(0, ang, 0) * s
        bb = r.bounding_box()
        if best is None or bb.size.Z < best[0]:
            best = (bb.size.Z, r)
    return best[1]


def bracket_flat():
    w = m._winch_local(P, D)
    s = w["bracket"]
    best = None
    for ang in (D["leg_angle"] - 90, 90 - D["leg_angle"], D["leg_angle"] + 90, -D["leg_angle"] - 90, D["leg_angle"], -D["leg_angle"]):
        r = Rot(0, ang, 0) * s
        bb = r.bounding_box()
        if best is None or bb.size.Z < best[0]:
            best = (bb.size.Z, r)
    return best[1]


def passer(sections=1, origin=(0.0, 0.0, 0.0)):
    return m.passer_parts(P, origin=origin, sections=sections)


# ----------------------------------------------------------------- overview
def overview():
    c = comps()
    a1 = math.radians(P["legs_phi"][0])
    e1 = (math.cos(a1), math.sin(a1))
    pp = passer(1, origin=(-2000.0, -3600.0, 0.0))
    parts = [
        part("Ground pads (3)", c["pads"], COL["pads"], (0, 0, -300)),
        part("Ground stakes (6)", c["stakes"], COL["stakes"], (0, 0, -1100)),
        part("Foot plates (3)", c["feet"], COL["feet"], (0, 0, 250)),
        part("Winch bracket, welded to leg 1", c["bracket"], COL["bracket"], (900 * e1[0], 900 * e1[1], 300)),
        part("Tripod legs (3)", legs(), COL["legs"], (0, 0, 700)),
        part("Tripod head", c["head"], COL["head"], (0, 0, 2000)),
        part("Head sheave and axle", c["sheave"] + c["axle"], COL["sheave"], (700 * e1[0], 700 * e1[1], 1600)),
        part("Leg pins (6)", c["head_pins"] + c["foot_pins"], COL["pins"], (0, 0, 1200)),
        part("Hand winch with load brake", c["winch"] + c["winch_bolts"], COL["winch"], (1500 * e1[0], 1500 * e1[1], 300)),
        part("Spread chains (3)", c["spread_chains"], COL["spread_chains"], (0, 0, -600)),
        part("Wire rope, 8 mm", c["rope"], COL["rope"], (0, 0, 700)),
        part("Swivel hook", c["hook"], COL["hook"], (0, 0, 900)),
        part("Spreader main beam", c["beam"], COL["beam"], (0, 0, 700)),
        part("Spreader cross bars (2)", c["cross_bars"], COL["cross_bars"], (0, 0, 450)),
        part("Cross bar bolts (4)", c["cross_bolts"], COL["cross_bolts"], (0, 0, 1050)),
        part("Lift shackle", c["lift_shackle"], COL["shackles"], (0, 0, 850)),
        part("Adjusting chains and shackles (4)", c["adj_chains"] + c["band_shackles"], COL["adj_chains"], (0, 0, 150)),
        part("Webbing bands (2)", c["bands"], COL["bands"], (0, 0, -150)),
        part("Felt sleeves (2)", c["felt"], COL["felt"], (0, 0, -450)),
        part("Rim bearers (2)", c["bearers"], COL["bearers"], (-5200, 0, -900)),
        part("Bridge runners (3)", c["runners"], COL["runners"], (-5200, 0, -500)),
        part("Deck panels (3)", c["deck"] + c["cleats"], COL["deck"], (-5200, 0, -100)),
        part("Passer pole sections (16)", pp["poles"] + pp["spigots"], COL["passer"], (0, 0, 0)),
        part("Passer J-head", pp["jhead"], COL["jhead"], (0, 0, 0)),
        part("Retrieval hook head", pp["hookhead"], COL["jhead"], (0, -400, 0)),
    ]
    return bv.overview(parts, OUT / "overview.png", "WellSling: the kit pulled apart, in build order",
                       "Numbered in build order; the bought lines and rope are drawn as fitted", elev=20, azim=-50,
                       size=(11, 8), key=True)


# ----------------------------------------------------------------- making sketches
def sheet(n, shape, name, color, neighbours, title, material, notes, view_shape=None, inset=(24, -58)):
    p = part(name, shape, color)
    return bv.component_sheet(p, keep(neighbours), "WellSling", f"WSL-DWG-{n}", f"WellSling: {title}", material,
                              notes, DATE, out_dir=str(DWG), view_shape=view_shape, inset_view=inset)


def sheets(which=None):
    c = comps()
    S = {}
    foot = one_foot()
    near3 = (-3000, -1900, -500, 500, -800, 900)        # around the foot of leg 3 (at 180 deg)
    S[101] = lambda: sheet(101, foot["pads"], "Ground pad", COL["pads"],
        [part("foot plate", foot["foot_plates"], "#D1D5DB"), part("stakes", foot["stakes"], "#D1D5DB")],
        "ground pad (make 3)", "Hardwood board 600 x 300 x 50 mm; 25 x 2 mm steel strap",
        ["Make three. Hardwood board 600 x 300 x 50 mm, sawn square,",
         "  the grain along the 600 mm length.",
         "Holes: two 28 mm holes straight through, on the cross centre line,",
         "  85 mm each side of the middle (170 mm apart).",
         "Band each end with 25 x 2 mm steel strap, 40 mm in from the end,",
         "  nailed, so the board cannot split along the grain.",
         "It lies with the 600 mm length pointing at the well, its near",
         "  end at least 650 mm back from the rim.",
         "The foot plate sits on top, its two holes over these holes.",
         "Check: the board lies flat on a floor without rocking."])
    S[102] = lambda: sheet(102, win(foot["stakes"], -10000, 10000, 0, 10000, -10000, 10000), "Ground stake", COL["stakes"],
        [part("pad", foot["pads"], "#D1D5DB"), part("foot plate", foot["foot_plates"], "#D1D5DB")],
        "ground stake (make 6)", "25 mm round bar, S275; 48 mm round, 15 mm thick, for the head",
        ["Make six. Cut 25 mm round bar 760 mm long.",
         "Point one end: a 60 mm long taper, forged or ground.",
         "Head: a 48 mm disc, 15 mm thick, centred on the other end,",
         "  welded all round so a sledge cannot knock it off.",
         "Two stakes go through each foot plate and pad and about",
         "  630 mm into the ground; the head rests on the foot plate.",
         "Galvanise after welding.",
         "Check: the stake slides through a 28 mm hole without force."])
    S[103] = lambda: sheet(103, foot["foot_plates"], "Foot plate", COL["feet"],
        [part("pad", foot["pads"], "#D1D5DB"), part("stakes", foot["stakes"], "#D1D5DB"),
         part("leg", win(m._leg_local(P, D)["tube"] + m._leg_local(P, D)["tongues"], 2200, 2800, -200, 200, 0, 500), "#D1D5DB")],
        "foot plate (make 3)", "10 mm and 12 mm S275 plate, hot-dip galvanised",
        ["Make three. Base: 260 x 260 x 10 mm plate.",
         "Two 28 mm stake holes on the cross centre line, 85 mm each side",
         "  of the middle, to match the pad.",
         "Leg lugs: two 100 x 90 x 10 mm plates standing on the base,",
         "  centred, 17 mm apart (inside faces), running toward the well.",
         "  21 mm pin hole through both, 60 mm above the base top.",
         "  Drill the two lugs together after welding so the holes line up.",
         "Chain eye: 60 x 40 x 12 mm plate standing on the inner edge,",
         "  10 mm in from it, in line with the lugs; 20 mm hole",
         "  20 mm above the base. The two spread chains shackle to it.",
         "Fillet weld 6 mm all round; galvanise after welding.",
         "Check: the leg tongue (16 mm) slides between the lugs and a",
         "  20 mm pin goes through all three holes by hand."])
    S[104] = lambda: sheet(104, m._winch_local(P, D)["bracket"], "Winch bracket", COL["bracket"],
        [part("leg 1", win(m._leg_local(P, D)["tube"], 1500, 2600, -400, 400, 400, 1700), "#D1D5DB")],
        "winch bracket on leg 1 (make 1)", "10 mm S275 plate; four M12 x 40 grade 8.8 bolts",
        ["Make one. Plate 300 x 240 x 10 mm.",
         "Four 13 mm holes on a 160 mm square, centred on the plate,",
         "  to suit the winch base (check against the winch bought).",
         "It is welded flat on the outer face of leg 1 (the face away",
         "  from the well), its 300 mm length along the leg, its middle",
         "  900 mm up the leg from the foot pin centre.",
         "It sits 70 mm off the leg centre line, toward the side the",
         "  winch handle will be on, so the drum lines up under the sheave.",
         "Two 6 mm fillet welds along the leg, both sides, full length.",
         "Weld before the leg is galvanised.",
         "Check: the plate is flat and square to the leg within 1 mm."], view_shape=bracket_flat())
    S[105] = lambda: sheet(105, c["leg_3"], "Tripod leg", COL["legs"],
        [part("head", c["head"], "#D1D5DB"), part("other legs", c["leg_1"] + c["leg_2"], "#D1D5DB"),
         part("feet", c["feet"], "#D1D5DB")],
        "tripod leg (make 3; leg 1 carries the winch bracket)", "Tube 76.1 x 3.6 mm, yield 310 MPa or more; 8 and 16 mm plate",
        ["Make three. Structural tube 76.1 x 3.6 mm, yield at least",
         "  310 MPa, cut 4,364 mm long, ends square. Not water pipe.",
         "End caps: 8 mm discs, 76 mm across, welded on both ends.",
         "Tongues: 60 x 90 x 16 mm plate, one welded to the middle of",
         "  each cap, in line with the tube; the two tongues lie in the",
         "  same plane. 21 mm pin hole 60 mm from the cap face.",
         "Pin hole to pin hole: 4,500 mm. Set it in a jig.",
         "Leg 1: weld the winch bracket (WSL-DWG-104) before galvanising.",
         "Drill a 10 mm vent hole near each end; galvanise.",
         "Check: pin centres 4,500 mm apart within 3 mm; leg straight",
         "  within 5 mm; all three legs the same length within 2 mm."], view_shape=leg_flat())
    S[106] = lambda: sheet(106, c["head"], "Tripod head", COL["head"],
        [part("legs", win(legs(), -600, 600, -600, 600, 3500, 4100), "#D1D5DB"), part("sheave", c["sheave"] + c["axle"], "#D1D5DB")],
        "tripod head weldment (make 1)", "12 mm and 10 mm S355 plate, hot-dip galvanised",
        ["Make one. Disc 440 mm across, 12 mm S355 plate.",
         "Leg lugs: six 110 x 85 x 10 mm plates under the disc, in three",
         "  pairs at 120 deg, each pair 17 mm apart (inside faces) and",
         "  centred 110 mm out from the middle, running outward.",
         "  21 mm hole in each, 55 mm below the disc, 110 mm out.",
         "Sheave hangers: two 120 x 10 mm plates, 190 mm deep, hanging",
         "  under the leg 1 pair, 36 mm apart (inside faces), 80 mm to one",
         "  side of that pair and 179 mm out from the middle.",
         "  26 mm axle hole in each, 125 mm below the disc.",
         "Profile cut; drill each pair together; 8 mm fillet welds.",
         "Check: a 20 mm pin passes through each pair; the 25 mm axle",
         "  passes both hangers; holes square to the plates."], inset=(-15, -40))
    sp = (X0 - 700, X0 + 700, Y0 - 700, Y0 + 700, 2380, 2800)
    S[107] = lambda: sheet(107, c["beam"], "Spreader main beam", COL["beam"],
        [part("cross bars", c["cross_bars"], "#D1D5DB"), part("bolts", c["cross_bolts"], "#D1D5DB"),
         part("lift shackle", c["lift_shackle"], "#D1D5DB")],
        "spreader main beam (make 1)", "RHS 100 x 50 x 4 mm S355; tube 26.9 x 3.2 mm; 20, 10 and 6 mm plate",
        ["Make one. RHS 100 x 50 x 4 mm, 1,100 mm long, 100 mm side upright.",
         "Sleeves: six 26.9 x 3.2 mm tubes, 100 mm long, through 27 mm",
         "  holes in the top and bottom walls, 300, 400 and 500 mm each",
         "  side of the middle; welded flush top and bottom.",
         "Lift lug: 300 x 120 x 20 mm plate standing on top, centred,",
         "  along the beam. Five 22 mm holes 50 mm apart, 40 mm below",
         "  its top edge, so the hook point can move to balance the animal.",
         "End caps 6 mm. Guide line eyes: 60 x 60 x 10 mm plates on top,",
         "  35 mm from each end, 18 mm hole.",
         "Full-penetration weld on the lug; 6 mm fillets elsewhere.",
         "Check: an M16 bolt passes each sleeve; lug square to the beam."], inset=(20, -40))
    S[108] = lambda: sheet(108, win(c["cross_bars"], -5000, 5000, Y0, 5000, 0, 5000), "Spreader cross bar", COL["cross_bars"],
        [part("main beam", c["beam"], "#D1D5DB"), part("bolts", c["cross_bolts"], "#D1D5DB"), part("bands", c["bands"], "#D1D5DB")],
        "spreader cross bar (make 2)", "SHS 50 x 50 x 3 mm S355; 10 and 6 mm plate",
        ["Make two. SHS 50 x 50 x 3 mm, 760 mm long, 6 mm end caps.",
         "Top plate: 100 x 160 x 10 mm, centred on top, its 160 mm",
         "  across the bar. Two 18 mm holes on the plate's long centre",
         "  line, 50 mm each side of the bar centre line (100 mm apart).",
         "Tip lugs: 60 x 70 x 10 mm plates hanging under each end,",
         "  centred 40 mm in from the end, in line with the bar.",
         "  14 mm hole 25 mm above the lug's bottom edge.",
         "6 mm fillet welds all round; galvanise.",
         "It hangs under the main beam on two M16 bolts through the",
         "  sleeves at 400 and 500 mm (or 300 and 400 for a calf).",
         "Check: bolts pass plate and sleeves together by hand."], inset=(20, -40))
    S[109] = lambda: sheet(109, win(c["felt"], -5000, 5000, Y0, 5000, -5000, 5000), "Felt sleeve", COL["felt"],
        [part("band", win(c["bands"], -5000, 5000, Y0, 5000, -5000, 5000), "#D1D5DB")],
        "felt sleeve on the webbing band (make 2)", "10 mm wool felt; heavy cotton canvas",
        ["Make two. Wool felt 10 mm thick, cut 1,000 x 260 mm.",
         "Cover: heavy canvas sewn as a flat tube around the felt,",
         "  with a 300 mm wide pocket open at both ends so the band",
         "  slides through it.",
         "It is padding only. It must not stiffen the band: no boards,",
         "  rods or plates of any kind inside it.",
         "It sits under the animal's chest or flank, centred on the band.",
         "Check: the band slides through by hand; the sleeve folds flat."], inset=(15, -40))
    pp = passer(2)
    S[110] = lambda: sheet(110, passer(1)["poles"] + passer(1)["spigots"], "Passer pole section", COL["passer"],
        [part("next section", win(pp["poles"], 2000, 2600, -100, 100, -100, 100), "#D1D5DB")],
        "passer pole section (make 16)", "Aluminium tube 6063-T6, 40 x 2 mm; spigot tube 35.5 x 3 mm",
        ["Make sixteen (two poles of eight). Tube 40 x 2 mm, 2,000 mm.",
         "Spigot: 35.5 mm tube, 250 mm long, pushed 100 mm into one end",
         "  and fixed with two 5 mm rivets at right angles.",
         "Lock: a spring button in the spigot, 75 mm out from the tube",
         "  end, clicks into a 10 mm hole 75 mm in from the plain end",
         "  of the next section.",
         "Deburr every end; mark each section with a depth band.",
         "Check: two sections join and lock by hand with no wobble."], inset=(25, -60),
        view_shape=Rot(0, 90, 0) * (passer(1)["poles"] + passer(1)["spigots"]))
    S[111] = lambda: sheet(111, passer(1, origin=(0, 0, 0))["jhead"], "Passer J-head", COL["jhead"], [],
        "passer J-head (make 1)", "Steel tube 26.9 x 3.2 mm; 35.5 mm spigot; 6 mm plate eye",
        ["Make one. Tube 26.9 x 3.2 mm: a 500 mm straight shank, then a",
         "  half-turn bend of 400 mm radius, then a 250 mm nose.",
         "Bend cold on a former; no kinks. Round the nose end smooth.",
         "Line eye: 44 mm washer plate, 24 mm hole, welded at the nose.",
         "Spigot: 35.5 mm tube, 150 mm long, welded into the shank end",
         "  with the button lock, to fit any pole section.",
         "It is a separate tool. It never fixes to the band.",
         "Check: the J slides under a 400 mm body without snagging."], inset=(60, -60))
    S[112] = lambda: sheet(112, passer(1)["hookhead"], "Retrieval hook head", COL["jhead"], [],
        "retrieval hook head (make 1)", "16 mm round bar; 35.5 mm spigot",
        ["Make one. 16 mm round bar, 400 mm straight, then an open",
         "  hook of 60 mm radius, bent cold through about 200 deg.",
         "Round the hook tip; it catches the messenger line, not the animal.",
         "Spigot: 35.5 mm tube, 150 mm long, welded on the straight end,",
         "  with the button lock, to fit any pole section.",
         "Check: the hook picks an 8 mm line off the floor easily."], inset=(60, -60))
    S[113] = lambda: sheet(113, win(c["bearers"], -5000, 5000, 0, 5000, -10, 500), "Rim bearer", COL["bearers"],
        [part("runners", win(c["runners"], -5000, 5000, 1500, 2400, -10, 500), "#D1D5DB")],
        "rim bearer (make 2)", "Hardwood 1,400 x 200 x 100 mm",
        ["Make two. Hardwood 1,400 x 200 x 100 mm, sawn square.",
         "Mark the three runner positions on top: 500 mm apart,",
         "  the middle one at the centre of the length.",
         "Seal the ends; chamfer the top edges 10 mm.",
         "It lies flat on firm ground, square to the runners, its",
         "  near edge at least 350 mm back from the rim.",
         "Check: it lies flat without rocking; the marks are square."])
    S[114] = lambda: sheet(114, win(c["runners"], -1000, -400, -5000, 5000, -10, 500), "Bridge runner", COL["runners"],
        [part("bearers", c["bearers"], "#D1D5DB"), part("deck", c["deck"], "#D1D5DB")],
        "bridge runner (make 3)", "RHS 100 x 50 x 3 mm S355, hot-dip galvanised",
        ["Make three. RHS 100 x 50 x 3 mm, 4,500 mm long, 100 mm upright.",
         "End caps: 4 mm plate, welded all round, with a 10 mm vent hole",
         "  near each end before galvanising.",
         "Paint a white band 1,250 mm in from each end: the bearer goes",
         "  between the band and the end, so 4.0 m spans the well.",
         "It is pushed across the well mouth from one side, resting on",
         "  both rim bearers, 500 mm from the next runner.",
         "Check: straight within 5 mm; no dents in the top face."], inset=(30, -40))
    S[115] = lambda: sheet(115, win(c["deck"] + c["cleats"], -5000, 5000, -760, 760, -100, 500), "Deck panel", COL["deck"],
        [part("runners", win(c["runners"], -5000, 5000, -900, 900, -10, 500), "#D1D5DB")],
        "deck panel (make 3)", "Exterior plywood 25 mm; hardwood 45 x 45 mm cleats",
        ["Make three. Exterior plywood 25 mm, 1,500 x 1,220 mm.",
         "Cleats: two hardwood 45 x 45 x 1,400 mm battens glued and",
         "  screwed underneath, 250 mm each side of the middle, running",
         "  along the 1,500 mm length, 50 mm in from each end.",
         "  The cleats drop between the runners so the panel cannot",
         "  slide sideways off the bridge.",
         "Seal all edges; grit paint on top.",
         "Check: the panel drops onto three runners 500 mm apart and",
         "  sits flat; it weighs no more than 35 kg."], inset=(35, -40))
    for n in sorted(S):
        if which and n not in which:
            continue
        print(n, "->", S[n]())


# ----------------------------------------------------------------- joints
def joints(which=None):
    c = comps()
    J = {}

    def jt(n, parts, title, sub, **kw):
        return bv.joint(keep(parts), OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", sub, **kw)

    fb = (-2850, -2150, -300, 300, -150, 420)
    J[1] = lambda: jt(1, [W("pads", "Ground pad", fb), W("feet", "Foot plate and lugs", fb), W("stakes", "Ground stakes", fb),
                         W("foot_pins", "Foot pin, 20 mm", fb), W("leg_3", "Leg 3, its tongue between the lugs", fb, col="legs"),
                         W("spread_chains", "Spread chain shackles", fb)],
                      "leg foot on its pad", "The 16 mm leg tongue sits between two lugs 17 mm apart; one 20 mm pin; stakes through plate and pad",
                      elev=22, azim=-120)
    hb = (-400, 400, -400, 400, 3650, 4020)
    J[2] = lambda: jt(2, [W("head", "Head plate, lugs and hangers", hb), W("head_pins", "Head pins, 20 mm", hb, col="pins"),
                         W("leg_1", "Leg 1 (winch leg)", hb, col="legs"), W("leg_2", "Leg 2", hb, col="legs"),
                         W("leg_3", "Leg 3", hb, col="legs")],
                      "legs pinned to the head", "Seen from below: each tongue between a pair of lugs, one pin with an R-clip on a lanyard",
                      elev=-30, azim=-60)
    sc = (-120, 420, -420, 180, 3640, 4000)
    J[3] = lambda: jt(3, [W("head", "Hanger plates", sc), W("sheave", "Sheave, 200 mm, with spacers", sc),
                         W("axle", "Axle pin, 25 mm", sc, col="pins"), W("rope", "Wire rope", sc)],
                      "head sheave in its hangers", "Cut through the axle: 3 mm spacer each side, axle through both hangers, nut and split pin",
                      cut="+Y", elev=15, azim=-30)
    wb = (500, 1700, -2500, -1300, 450, 1500)
    J[4] = lambda: jt(4, [W("leg_1", "Leg 1", wb, col="legs"), W("bracket", "Winch bracket", wb), W("winch", "Hand winch", wb),
                         W("winch_bolts", "Four M12 bolts", wb, col="pins"), W("rope", "Rope to the sheave", wb)],
                      "winch on leg 1", "Bracket welded to the outer face of the leg; winch base on four M12 bolts; rope leaves the drum on the leg side",
                      elev=20, azim=-150)
    hk = (X0 - 200, X0 + 200, Y0 - 250, Y0 + 250, 2540, 3150)
    J[5] = lambda: jt(5, [W("rope", "Rope, thimble eye", hk), W("hook", "Swivel hook with latch", hk),
                         W("lift_shackle", "Bow shackle, 3.25 t", hk, col="shackles"), W("beam", "Lift lug on the beam", hk)],
                      "hook to the spreader", "The shackle pin goes through one of five lug holes; the bow sits in the hook under its latch",
                      elev=15, azim=-60)
    cb = (X0 - 90, X0 + 90, Y0 + 300, Y0 + 620, 2390, 2600)
    J[6] = lambda: jt(6, [W("beam", "Main beam and sleeves", cb), W("cross_bars", "Cross bar and top plate", cb),
                         W("cross_bolts", "M16 bolts and nuts", cb)],
                      "cross bar under the main beam", "Cut along the beam: each M16 bolt through a sleeve and the top plate, nut under the plate",
                      cut="+X", elev=15, azim=-60)
    tx = X0 + P["cross"][0] / 2 - 40
    tb = (tx - 150, X0 + P["band_r"] + 150, Y0 + 300, Y0 + 600, 1820, 2420)
    J[7] = lambda: jt(7, [W("cross_bars", "Cross bar tip lug", tb), W("band_shackles", "1 t shackles", tb, col="shackles"),
                         W("adj_chains", "Adjusting chain", tb), W("bands", "Band sewn eye", tb)],
                      "band to the cross bar", "Shackle in the tip lug, chain to set the band height, shackle through the band's sewn eye",
                      elev=15, azim=-60)
    bb = (X0 - 500, X0 + 500, Y0 + 250, Y0 + 650, D["band_c"] - 420, D["band_c"] + 200)
    J[8] = lambda: jt(8, [W("bands", "Webbing band, 240 mm", bb), W("felt", "Felt sleeve", bb)],
                      "band and felt sleeve", "Cut across the band: the felt sleeve rides loose on the band; nothing stiffens it",
                      cut="+Y", elev=10, azim=-70)
    pj = passer(2)
    pw = (1700, 2400, -100, 100, -100, 100)
    J[9] = lambda: jt(9, [part("Pole section", win(pj["poles"], *pw), COL["passer"]),
                         part("Spigot with button lock", win(pj["spigots"], *pw), "#0E7490")],
                      "passer pole sections", "Cut along the pole: spigot riveted 100 mm into one section, 150 mm into the next",
                      cut="+Y", elev=20, azim=-60)
    J[10] = lambda: jt(10, [part("Last pole section", win(pj["poles"], 3300, 4100, -100, 1000, -100, 100), COL["passer"]),
                           part("Spigot", win(pj["spigots"], 3300, 4200, -100, 1000, -100, 100), "#0E7490"),
                           part("J-head with line eye", pj["jhead"], COL["jhead"])],
                       "J-head on the passer pole", "The J goes under the animal and the nose comes up the far side carrying the messenger line",
                       elev=55, azim=-70)
    rb = (-800, 150, 1750, 2300, -1, 300)
    J[11] = lambda: jt(11, [W("bearers", "Rim bearer", rb), W("runners", "Bridge runners", rb), W("deck", "Deck panel", rb),
                           W("cleats", "Cleats under the deck", rb)],
                       "bridge on its bearer", "Runners rest on the bearer; the deck's cleats drop between the runners",
                       elev=20, azim=-30)
    for n in sorted(J):
        if which and n not in which:
            continue
        print(n, "->", J[n]())


# ----------------------------------------------------------------- steps
def steps(which=None):
    c = comps()
    E = {}

    def st(n, done, new, title, sub, **kw):
        return bv.step(keep(done), keep(new), OUT / f"step-{n:02d}.png", f"Step {n}: {title}", sub, **kw)

    pads = K("pads", "Ground pads")
    feet = K("feet", "Foot plates")
    stakes = K("stakes", "Stakes")
    base = [pads, feet, stakes]
    E[1] = lambda: st(1, [], [K("pads", "Ground pads (3)", (0, 0, 400))], "ground pads",
                      "On the setting-out marks: 5.0 m circle centred on the well, 120 deg apart, near ends 700 mm back from a 3 m rim",
                      elev=35, azim=-50)
    E[2] = lambda: st(2, [pads], [K("feet", "Foot plates (3)", (0, 0, 400)), K("stakes", "Stakes, two per foot", (0, 0, 900))],
                      "foot plates and stakes", "Lugs pointing at the well centre; drive both stakes through plate and pad until the heads seat",
                      elev=35, azim=-50)
    hb = (-450, 450, -450, 450, 3550, 4050)
    E[3] = lambda: st(3, [W("head", "Tripod head", hb)], [K("sheave", "Sheave and spacers", (0, 0, -300)),
                                                         K("axle", "Axle pin", (0, -250, 0), col="pins")],
                      "sheave into the head", "On the ground before raising: sheave between the hangers, spacers either side, axle, nut, split pin",
                      elev=-20, azim=-40)
    wb = (300, 1900, -2700, -1100, 300, 1600)
    E[4] = lambda: st(4, [W("leg_1", "Leg 1", wb, col="legs"), W("bracket", "Bracket", wb)],
                      [W("winch", "Hand winch", wb, explode=(450, -780, 300)), W("winch_bolts", "M12 bolts", wb, explode=(450, -780, 300), col="pins")],
                      "winch onto leg 1", "On the ground: four M12 bolts with nyloc nuts, torqued; handle on the side away from the leg",
                      elev=20, azim=-150)
    trip = [K("leg_1", "Leg 1 (winch)", col="legs"), K("leg_2", "Leg 2", col="legs"), K("leg_3", "Leg 3", col="legs"),
            K("head", "Head"), K("sheave", "Sheave"), K("bracket", "Bracket"), K("winch", "Winch"),
            K("head_pins", "Head pins", col="pins")]
    E[5] = lambda: st(5, base, [part("Tripod: legs pinned to the head, sheave and winch on", fuse("leg_1", "leg_2", "leg_3", "head", "sheave", "head_pins"), COL["legs"], (0, 0, 900)),
                                part("Winch on leg 1", fuse("bracket", "winch"), COL["winch"], (0, 0, 900)),
                                K("foot_pins", "Foot pins (3)", (0, 0, 900), col="pins")],
                      "legs pinned to the head, tripod raised",
                      "Pin all three legs to the head on the ground, walk the tripod up over the well with two foot ropes, pin each foot",
                      elev=20, azim=-50, label_done=False)
    erected = base + [part(q.name, q.shape, "#D1D5DB") for q in trip] + [K("foot_pins", "Foot pins", col="pins")]
    E[6] = lambda: st(6, erected, [K("spread_chains", "Spread chains (3)", (0, 0, 500))], "spread chains",
                      "Shackle a chain between each pair of chain eyes; take up the slack so all three are hand tight",
                      elev=35, azim=-50, label_done=False)
    E[7] = lambda: st(7, erected + [K("spread_chains", "Spread chains")],
                      [K("rope", "Wire rope", (0, 0, 0)), K("hook", "Swivel hook", (0, 0, 600))],
                      "rope reeved and hook on", "Rope from the drum up the leg, over the sheave and down the middle; hook on the thimble eye",
                      elev=20, azim=-50, label_done=False)
    sp = [K("beam", "Spreader main beam")]
    E[8] = lambda: st(8, sp, [K("cross_bars", "Cross bars (2)", (0, 0, -250)), K("cross_bolts", "M16 bolts (4)", (0, 0, 300))],
                      "spreader assembled", "On the ground: cross bars under the beam at the 400 and 500 mm sleeves, bolts down, nuts under",
                      elev=25, azim=-55)
    hung = erected + [K("spread_chains", "Spread chains"), K("rope", "Rope"), K("hook", "Hook")]
    spr = [K("beam", "Spreader"), K("cross_bars", "Cross bars"), K("cross_bolts", "Bolts")]
    E[9] = lambda: st(9, hung, [part(q.name, q.shape, q.color, (0, 0, -500)) for q in spr] +
                      [K("lift_shackle", "Lift shackle", (0, 0, -500), col="shackles")],
                      "spreader on the hook", "Shackle through the middle lug hole, bow into the hook, latch closed; guide lines on both end eyes",
                      elev=20, azim=-50, label_done=False)
    near = (X0 - 1000, X0 + 1000, Y0 - 1000, Y0 + 1000, 1000, 2700)
    hung2 = [W("beam", "Spreader", near), W("cross_bars", "Cross bars", near), W("cross_bolts", "Bolts", near),
             W("lift_shackle", "Lift shackle", near, col="shackles"), W("hook", "Hook", near), W("rope", "Rope", near)]
    E[10] = lambda: st(10, hung2, [K("adj_chains", "Adjusting chains (4)", (0, 0, -300)), K("band_shackles", "1 t shackles (8)", (0, 0, -300), col="shackles"),
                                   K("bands", "Webbing bands (2)", (0, 0, -600)), K("felt", "Felt sleeves (2)", (0, 0, -600))],
                       "bands, chains and sleeves", "At the well: each band is passed under the animal first (see the passer), then shackled to the chains",
                       elev=20, azim=-55, label_done=False)
    rig = erected + [K("spread_chains", "Spread chains"), K("rope", "Rope"), K("hook", "Hook")] + \
        [part(q.name, q.shape, "#D1D5DB") for q in spr] + [K("lift_shackle", "Lift shackle", col="shackles"),
                                                         K("adj_chains", "Chains"), K("bands", "Bands"), K("felt", "Felt")]
    E[11] = lambda: st(11, rig, [K("bearers", "Rim bearers (2)", (0, 0, 400))], "rim bearers",
                       "Once the animal is above the rim: a bearer each side of the well, 2.0 m from its centre, square to the runners",
                       elev=35, azim=-30, label_done=False)
    E[12] = lambda: st(12, rig + [K("bearers", "Bearers")], [K("runners", "Bridge runners (3)", (0, -2500, 0))], "runners slid across",
                       "Push each runner across from one side, under the animal, 500 mm apart; the white bands sit over the bearers",
                       elev=35, azim=-30, label_done=False)
    E[13] = lambda: st(13, rig + [K("bearers", "Bearers"), K("runners", "Runners")],
                       [K("deck", "Deck panels (3)", (0, -2000, 300)), K("cleats", "Cleats", (0, -2000, 300))], "deck panels",
                       "Slide the three panels in along the runners, cleats down between them; then lower the animal onto the deck",
                       elev=35, azim=-30, label_done=False)
    pj = passer(2, origin=(0, 0, 0))
    E[14] = lambda: st(14, [part("Pole section", win(pj["poles"], -10, 2010, -100, 100, -100, 100), COL["passer"])],
                       [part("Next section", win(pj["poles"], 2010, 4100, -100, 100, -100, 100), COL["passer"], (600, 0, 0)),
                        part("Spigots", pj["spigots"], "#0E7490", (0, 0, 0)), part("J-head", pj["jhead"], COL["jhead"], (1200, 0, 0))],
                       "passer pole made up", "Click sections together until the J reaches the animal; the button lock must show in every joint",
                       elev=50, azim=-70)
    for n in sorted(E):
        if which and n not in which:
            continue
        print(n, "->", E[n]())


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    what, nums = args[0], [int(a) for a in args[1:]]
    if what == "overview":
        print("overview ->", overview())
    elif what == "sheets":
        sheets(nums or None)
    elif what == "joints":
        joints(nums or None)
    elif what == "steps":
        steps(nums or None)
    else:
        for w in args:
            {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}[w]()
