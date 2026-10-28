"""WellSling repo-specific CAD helpers (kit 1.9 parts library extensions).

These sit beside .kit/cad_parts.py and are used by cad/src/model.py for the detailed (D3) model of every
concept option. Candidates for a future kit release are listed in docs/REVIEW.md.

    frame()        a build123d Location from an origin, an x direction and a z direction
    stock()        any +Z-built stock (tube, RHS, bar) laid between two points
    plate_on()     cad_parts.sheet() placed on any plane, centred on a point
    fillet_on()    a cad_parts.weld_fillet bead along any direction with its legs along two given faces
    ring_weld()    a round fillet weld (tube to plate) about any axis
    chain()        link chain between two points (one link solid copied, alternate links turned 90 degrees)
    bow_shackle()  a bow shackle body and its screw pin, as two solids
    swivel_hook()  a latched swivel eye hook (one bought solid)

All sizes in millimetres. Directions are tuples and need not be unit length.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Box, Compound, Cylinder, Location, Plane, Polygon, Pos, Rot, Solid, Sphere,  # noqa: E402
                       Torus, extrude, Sketch, Circle, RectangleRounded)
import cad_parts as cp  # noqa: E402


# --------------------------------------------------------------------------------------------- vectors
def unit(a):
    n = math.sqrt(sum(x * x for x in a))
    return tuple(x / n for x in a)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, k):
    return tuple(x * k for x in a)


def perp(d):
    """A unit vector perpendicular to d."""
    d = unit(d)
    t = (0, 0, 1) if abs(d[2]) < 0.9 else (1, 0, 0)
    return unit(cross(d, t))


def frame(origin, x_dir, z_dir):
    x_dir = unit(x_dir)
    z_dir = unit(z_dir)
    x_dir = unit(sub(x_dir, mul(z_dir, dot(x_dir, z_dir))))
    return Location(Plane(origin=tuple(float(v) for v in origin), x_dir=x_dir, z_dir=z_dir))


# --------------------------------------------------------------------------------------------- placement
def stock(shape, p0, p1, x_dir=None):
    """A part built along +Z from z = 0 (cad_parts stock) placed so its z = 0 end is at p0 and it points at p1.
    x_dir fixes the turn of the section about its axis (the section's local X)."""
    d = unit(sub(p1, p0))
    xd = x_dir if x_dir is not None else perp(d)
    return frame(p0, xd, d) * shape


def plate_on(w, h, t, center, x_dir, z_dir, holes=(), r_corner=3.0, edge=0.8):
    """cad_parts.sheet(w along x_dir, h along y = z x x, t along z_dir), centred on center in all three axes.
    holes: [(x, y, d)] from the plate centre in the plate's own x and y."""
    s = cp.sheet(w, h, t, holes=holes, r_corner=r_corner, edge=edge)
    s = Pos(0, 0, -t / 2) * s
    return frame(center, x_dir, z_dir) * s


def fillet_on(origin, along, length, leg, d1, d2):
    """Fillet weld bead from origin along 'along' for 'length', its two legs along d1 and d2 (the two faces
    it joins, pointing away from the corner)."""
    bead = cp.weld_fillet(length, leg)              # along +X, legs along +Y and +Z
    a, z = unit(along), unit(d2)
    y = cross(z, a)
    if dot(y, unit(d1)) > 0:
        return Location(Plane(origin=tuple(origin), x_dir=a, z_dir=z)) * bead
    o2 = add(origin, mul(a, length))
    return Location(Plane(origin=tuple(o2), x_dir=mul(a, -1), z_dir=z)) * bead


def ring_weld(center, axis, r, leg, toward=1):
    """Round fillet weld of a tube of outside radius r onto a face whose normal is 'axis' at 'center';
    the bead sits on the side 'toward' (+1 along axis, -1 against it)."""
    cone = Solid.make_cone(r + leg, r, leg)
    ring = cone - Cylinder(r, 3 * leg)
    ring = ring - Pos(0, 0, -2 * leg) * Cylinder(r + 2 * leg, 2 * leg)
    ax = unit(axis) if toward > 0 else mul(unit(axis), -1)
    return frame(center, perp(ax), ax) * ring


# --------------------------------------------------------------------------------------------- rigging
def _link(wire_d, inner_len, inner_w):
    """One chain link, its long axis along X, lying in the XY plane, centred on the origin: two half tori and two
    straight sides, kept as a compound (no boolean), so it tessellates lightly."""
    rc = (inner_w + wire_d) / 2                        # centre-line radius of the ends
    straight = inner_len - inner_w
    end1 = Pos(straight / 2, 0, 0) * Rot(0, 0, -90) * Torus(rc, wire_d / 2, major_angle=180, align=None)
    end2 = Pos(-straight / 2, 0, 0) * Rot(0, 0, 90) * Torus(rc, wire_d / 2, major_angle=180, align=None)
    sides = [Pos(0, s * rc, 0) * Rot(0, 90, 0) * Cylinder(wire_d / 2, straight) for s in (-1, 1)]
    return Compound([end1, end2] + sides)


_LINKS = {}


def link_solid(wire_d=8.0, inner_len=24.0, inner_w=10.4):
    key = (wire_d, inner_len, inner_w)
    if key not in _LINKS:
        ln = _link(wire_d, inner_len, inner_w)
        premesh(ln)
        _LINKS[key] = ln
    return _LINKS[key]


def premesh(shape, deflection=0.4, angle=0.5):
    """Mesh a shape once with an absolute chord deflection, so every placed copy of it (chain links share one
    shape) reuses a light triangulation instead of the very fine one a relative mesh gives small tori."""
    try:
        from OCP.BRepMesh import BRepMesh_IncrementalMesh
        BRepMesh_IncrementalMesh(shape.wrapped, deflection, False, angle, True)
    except Exception:
        pass
    return shape


def chain(p0, p1, n0=None, n1=None, wire_d=8.0, pitch=24.0, inner_w=10.4, r0=0.0, r1=0.0, end_links=None):
    """Link chain hanging between two connecting wires (a shackle bow crown, a pin or a ring) whose centres are
    p0 and p1 and whose axes are n0 and n1 (the first and last link lie in the plane normal to n0 and n1, so the
    wire passes through them). r0, r1: radii of those wires. Grade 80 short link proportions by default.
    end_links: (wire, inner_len, inner_w) of an enlarged end link at both ends. Returns a Compound."""
    d = unit(sub(p1, p0))
    n0 = unit(n0) if n0 is not None else perp(d)
    n0 = unit(sub(n0, mul(d, dot(n0, d))))
    alt = cross(d, n0)
    L = math.dist(p0, p1)
    links = []
    a0, a1 = sub(p0, mul(d, r0)), add(p1, mul(d, r1))          # the wires sit inside the first and last link, against their inside ends
    if end_links:
        ew, el, ei = end_links
        e = link_solid(ew, el, ei)
        links.append(frame(add(a0, mul(d, el / 2)), d, n0) * e)
        links.append(frame(sub(a1, mul(d, el / 2)), d, n0 if n1 is None else n1) * e)
        a0 = add(a0, mul(d, el - ew))          # the next link's inside end wraps the end link's far wire
        a1 = sub(a1, mul(d, el - ew))
        r_first = ew / 2
        a0 = add(a0, mul(d, 0)); a1 = sub(a1, mul(d, 0))
        start_normal = alt
    else:
        start_normal = n0
    span = math.dist(a0, a1)
    n = max(1, int((span - pitch) // pitch) + 1)
    if n1 is not None and not end_links:
        want_same = abs(dot(unit(n1), n0)) > 0.7
        if (n % 2 == 1) != want_same:
            n -= 1
    n = max(1, n)
    step = (span - pitch) / max(n - 1, 1) if n > 1 else 0.0
    link = link_solid(wire_d, pitch, inner_w)
    other = cross(d, start_normal)
    for k in range(n):
        c = add(a0, mul(d, pitch / 2 + step * k))
        links.append(frame(c, d, start_normal if k % 2 == 0 else other) * link)
    return Compound(links)


def bow_shackle(pin_c, pin_axis, bow_dir, d_pin, gap, inside_len):
    """Bow shackle: body (two eyes on the pin, legs and a round bow) and screw pin with a collar.
    pin_c: middle of the pin between the eyes; pin_axis: pin direction (the collar end is at -pin_axis);
    bow_dir: from the pin toward the bow; gap: clear width between the eyes; inside_len: from the pin centre
    to the inside of the bow crown. The bow crown wire runs parallel to the pin, centred at
    pin_c + bow_dir * (inside_len + 0.45 d_pin). Returns (body, pin)."""
    a, b = unit(pin_axis), unit(bow_dir)
    c3 = cross(a, b)
    wire = d_pin * 0.9
    half = gap / 2 + wire / 2                        # eye centre from the middle, along the pin
    bow_r = half                                     # bow centre-line radius
    yc = inside_len + wire / 2 - bow_r               # bow centre, along bow_dir
    loc = Location(Plane(origin=tuple(pin_c), x_dir=a, z_dir=c3))   # local X = pin, local Y = toward bow
    pieces = []
    for s in (-1, 1):
        eye = Pos(s * half, 0, 0) * Rot(0, 90, 0) * (Cylinder(wire * 0.95, wire) - Cylinder(d_pin / 2 + 0.6, wire + 2))
        pieces.append(eye)
        ly0, ly1 = wire * 0.9, yc
        if ly1 > ly0 + 1:
            pieces.append(Pos(s * half, (ly0 + ly1) / 2, 0) * Rot(90, 0, 0) * Cylinder(wire / 2, ly1 - ly0))
    bowt = Torus(bow_r, wire / 2) & Pos(0, (bow_r + wire) / 2, 0) * Box(2 * (bow_r + wire) + 2, bow_r + wire, wire + 2)
    pieces.append(Pos(0, yc, 0) * bowt)
    x0 = -(half + wire / 2 + 0.6 * wire)
    x1 = half + wire / 2 + 0.35 * wire
    pin = Pos((x0 + x1) / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(d_pin / 2, x1 - x0)
    collar = Pos(x0 + 0.3 * wire, 0, 0) * Rot(0, 90, 0) * Cylinder(d_pin * 0.85, 0.6 * wire)
    return loc * Compound(pieces), loc * (pin + collar)


def swivel_hook(top, wll_scale=1.0):
    """Latched swivel eye hook hanging from 'top' (the inside top of its eye), bowl pointing +X. Grade 80,
    about 1 t; wll_scale scales it. Returns one solid (eye, swivel, shank, bowl, latch)."""
    k = wll_scale
    x, y, z = top
    eye = Pos(x, y, z - 22 * k) * Rot(90, 0, 0) * Torus(22 * k, 7 * k)
    swivel = Pos(x, y, z - 58 * k) * cp.break_edges(Cylinder(16 * k, 26 * k), 2.0)
    shank = Pos(x, y, z - 95 * k) * Cylinder(10 * k, 48 * k)
    bowl = Pos(x + 28 * k, y, z - 150 * k) * Rot(90, 0, 0) * Torus(28 * k, 10 * k)
    bowl = bowl & Pos(x + 28 * k, y, z - 150 * k - 10 * k) * Box(110 * k, 30 * k, 76 * k)
    tip = Pos(x + 56 * k, y, z - 136 * k) * Cylinder(8 * k, 30 * k)
    latch = Pos(x + 24 * k, y, z - 120 * k) * Rot(0, 60, 0) * Box(4 * k, 12 * k, 64 * k)
    return eye + swivel + shank + bowl + tip + latch


def disc(r, t, center, axis, hole=0.0, edge=1.0):
    """A round plate (end cap, washer, flange) of radius r and thickness t centred on center, normal axis."""
    s = Pos(0, 0, 0) * Cylinder(r, t)
    if hole:
        s = s - Cylinder(hole / 2, t + 2)
    s = cp.break_edges(s, min(edge, t / 3))
    return frame(center, perp(axis), axis) * s


def svg_tolerant():
    """build123d's SVG exporter hands svgpathtools an elliptical arc whose start equals its end for some tiny edges of
    a detailed model (svgpathtools asserts start != end and the whole drawing fails). Skip such a zero-length arc
    instead; nothing visible is lost. Repo-side workaround, called by the drawing scripts (see docs/REVIEW.md)."""
    import build123d.exporters as ex
    if getattr(ex.ExportSVG, "_wsl_tolerant", False):
        return
    orig = ex.ExportSVG._ellipse_segments

    def safe(self, edge, reverse):
        try:
            return orig(self, edge, reverse)
        except AssertionError:
            return []
    ex.ExportSVG._ellipse_segments = safe
    ex.ExportSVG._wsl_tolerant = True
