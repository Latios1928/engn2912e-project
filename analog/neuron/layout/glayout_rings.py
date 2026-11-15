"""
Ring helpers for GF180 gLayout cells: shared deep-n-well guard for NMOS, n-tap guard
for PMOS, dummy-transistor rings, and metal straps/labels for LVS.

    from glayout_rings import dummy_ring, dnw_guard, nwell_guard, strap, label

Typical order for one cell:
    1. place the real devices (fet(..., with_dummy=False))
    2. dummy_ring(pdk, top, nmos_refs, "n") / dummy_ring(pdk, top, pmos_refs, "p")
    3. dnw_guard(pdk, top, nmos_refs + [nmos_dummies])   -> body / DNW-tie / substrate rings
       nwell_guard(pdk, top, pmos_refs + [pmos_dummies]) -> PMOS body (n-tap) ring
    4. strap()/route() the rings to their rails, label() the pins

Every spacing below comes from the GF180 DRC deck (3.3 V "_LV" rules); the rule name is
noted next to each number so it can be checked or tuned.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from gdsfactory.component import Component
from gdsfactory.components import rectangle
from glayout import nmos, pmos, via_stack
from glayout.primitives.guardring import tapring

from glayout_helpers import MIN_FET_WIDTH

# --- geometry of glayout's tapring (measured): COMP ring width, implant overhang ----------
RING_COMP = 0.36       # COMP width of a tapring side
RING_IMP = 0.16        # p+/n+ implant extends this far past the COMP on both sides

# --- GF180 rules used (µm) -------------------------------------------------------------------
LPW_3 = 2.5            # DNWELL enclosure of LVPWELL
DF_4B = 0.62           # DNWELL overlap of NCOMP (DNW tie)
DF_18 = 2.5            # DNWELL space to substrate PCOMP (outside NWELL/DNWELL)
NP_2 = 0.4             # Nplus / Pplus space (also the dummy-to-device gap)
DF_4C = 0.43           # NWELL overlap of PCOMP (PMOS active) outside DNWELL


@dataclass
class Ring:
    """Result of a ring helper: the reference added to `top` plus a short summary."""
    ref: object
    size: tuple
    nets: dict = field(default_factory=dict)       # ring name -> net it must be tied to
    spice: list = field(default_factory=list)      # extra reference-netlist lines (dummies)

    @property
    def ports(self):
        return self.ref.ports

    def __repr__(self):
        nets = ", ".join(f"{k}->{v}" for k, v in self.nets.items())
        return f"Ring({self.size[0]:.2f} x {self.size[1]:.2f} um; {nets})"


# ----------------------------------------------------------------------------- utilities
def _bbox(refs):
    xs0 = min(r.xmin for r in refs); ys0 = min(r.ymin for r in refs)
    xs1 = max(r.xmax for r in refs); ys1 = max(r.ymax for r in refs)
    return xs0, ys0, xs1, ys1


def _rect(comp, layer, x0, y0, x1, y1):
    r = comp << rectangle(size=(x1 - x0, y1 - y0), layer=layer)
    r.move((x0, y0))
    return r


def _tap(pdk, comp, kind, inner_w, inner_h, prefix, keep_nwell=True):
    """Tap ring whose COMP inner edge encloses an inner_w x inner_h rectangle at (0,0)."""
    ring = tapring(pdk, enclosed_rectangle=(inner_w, inner_h),
                   sdlayer="p+s/d" if kind == "p" else "n+s/d")
    if not keep_nwell:
        # glayout fills the whole interior of an n+ tapring with NWELL. Inside a DNWELL
        # that would cover the LVPWELL (LPW.12), so draw it without that layer.
        ring = ring.flatten()
        ring.remove_layers(layers=[pdk.get_glayer("nwell")])
    ref = comp << ring
    comp.add_ports(ref.get_ports_list(), prefix=prefix)
    return ref


# ----------------------------------------------------------------------------- dummy ring
def dummy_ring(pdk, top, refs, kind: str, length: float | None = None,
               width: float = MIN_FET_WIDTH, gap: float = NP_2, rail: str | None = None,
               bulk: str | None = None, name: str = "DUM") -> Ring:
    """Surround a group of same-type FETs with dummy transistors on all four sides.

    Each dummy is a real nfet/pfet whose gate, source and drain are shorted on a met2 slab;
    the four slabs touch, forming one met2 frame (ports rail_N/E/S/W) that you tie to the
    rail (`rail`, default VSS for n / VDD for p). The bulk is whatever well the guard puts
    under it (dnw_guard / nwell_guard).

    LVS: dummies are real devices, so they must be in the reference netlist. The returned
    Ring.spice holds one line per extracted dummy; paste them into the .subckt.
    length: dummy gate length; match the real devices (default 1.0).
    bulk: net of the well under the dummies, for the netlist lines (default = rail).
    """
    kind = kind.lower()[0]
    rail = rail or ("VSS" if kind == "n" else "VDD")
    bulk = bulk or rail
    fet_fn = nmos if kind == "n" else pmos
    length = length or 1.0
    common = dict(length=length, with_tie=False, with_dummy=False, with_substrate_tap=False)
    if kind == "n":
        common["with_dnwell"] = False

    def make(w, fingers):
        return fet_fn(pdk, width=w, fingers=fingers, **common)

    x0, y0, x1, y1 = _bbox(refs)
    gw, gh = x1 - x0, y1 - y0

    # side columns: one finger, as tall as the group
    probe = make(width, 1)
    over_h = probe.ysize - width
    w_side = max(width, round((gh - over_h) / 0.02) * 0.02)  # snap to 2x grid
    side = make(w_side, 1)

    # top/bottom rows: as many fingers as fit over the group + both columns
    span = gw + 2 * (gap + side.xsize)
    pitch = make(width, 2).xsize - probe.xsize
    n_f = max(1, int((span - probe.xsize) // pitch) + 1)
    row = make(width, n_f)

    ring = Component(f"{name}_ring_{kind}")
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    slab = pdk.get_glayer("met2")
    places = {
        "W": (side, cx - gw / 2 - gap - side.xsize / 2, cy),
        "E": (side, cx + gw / 2 + gap + side.xsize / 2, cy),
        "S": (row, cx, cy - gh / 2 - gap - row.ysize / 2),
        "N": (row, cx, cy + gh / 2 + gap + row.ysize / 2),
    }
    frame = {}
    for s, (comp, px, py) in places.items():
        r = ring << comp
        r.move((px - r.center[0], py - r.center[1]))
        frame[s] = r
    # met2 frame: rows span full width, columns span between the rows -> one connected net
    for s in ("N", "S"):
        r = frame[s]
        _rect(ring, slab, r.xmin, r.ymin, r.xmax, r.ymax)
    for s in ("W", "E"):
        r = frame[s]
        _rect(ring, slab, r.xmin, frame["S"].ymax - 0.5, r.xmax, frame["N"].ymin + 0.5)
    for s, r in frame.items():
        ring.add_port(f"rail_{s}", center=(r.center[0], r.ymax if s != "S" else r.ymin) if s in "NS"
                      else (r.xmax if s == "E" else r.xmin, r.center[1]),
                      width=(r.xsize if s in "NS" else r.ysize), layer=slab,
                      orientation={"N": 90, "S": 270, "E": 0, "W": 180}[s])

    ref = top << ring
    model = "nfet_03v3" if kind == "n" else "pfet_03v3"
    spice = []
    for s, w, nf in (("N", width, n_f), ("S", width, n_f), ("W", w_side, 1), ("E", w_side, 1)):
        for k in range(nf):
            spice.append(f"X{name}{s}{k} {rail} {rail} {rail} {bulk} {model} "
                         f"L={length:g}u W={w:g}u nf=1")
    return Ring(ref, (ring.xsize, ring.ysize), {"rail": rail}, spice)


# ----------------------------------------------------------------------------- NMOS guard
def dnw_guard(pdk, top, refs, body: str = "VSS", dnw: str = "VDD", sub: str = "VSS",
              body_gap: float = 0.36, tie_gap: float = 0.43) -> Ring:
    """Smallest DRC-legal deep-n-well enclosure around a group of NMOS (and their dummies).

    Inside -> out:
      merged LVPWELL over every device
      p+ body ring (LVPWELL tie)           -> `body`   ports body_*
      n+ ring inside DNWELL (DNW tie)      -> `dnw`    ports dnw_*
      DNWELL                                (LPW.3: 2.5 um past LVPWELL)
      p+ substrate ring (rule DN.3)        -> `sub`    ports sub_*
    body_gap: device bbox to body-ring COMP. 0.36 = M2.2a (0.28) + the 0.07 um the ring
              metal reaches inside its COMP, so the ring clears dummy/device met2.
    tie_gap:  LVPWELL edge to DNW-tie COMP (>= 0.43 puts it in the relaxed NP/PP regime).
    """
    x0, y0, x1, y1 = _bbox(refs)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
    g = Component("dnw_guard")

    d_body = body_gap                                  # body ring COMP inner edge
    d_lpw = d_body + RING_COMP + RING_IMP              # LVPWELL edge = Pplus outer edge
    d_tie = d_lpw + tie_gap                            # DNW tie COMP inner edge
    d_dnw = max(d_lpw + LPW_3, d_tie + RING_COMP + DF_4B)
    d_sub = d_dnw + DF_18                              # substrate ring COMP inner edge

    _tap(pdk, g, "p", 2 * (hw + d_body), 2 * (hh + d_body), "body_")
    _rect(g, pdk.get_glayer("pwell"), -hw - d_lpw, -hh - d_lpw, hw + d_lpw, hh + d_lpw)
    _tap(pdk, g, "n", 2 * (hw + d_tie), 2 * (hh + d_tie), "dnw_", keep_nwell=False)
    _rect(g, pdk.get_glayer("dnwell"), -hw - d_dnw, -hh - d_dnw, hw + d_dnw, hh + d_dnw)
    _tap(pdk, g, "p", 2 * (hw + d_sub), 2 * (hh + d_sub), "sub_")

    ref = top << g
    ref.move((cx, cy))
    return Ring(ref, (g.xsize, g.ysize), {"body": body, "dnw": dnw, "sub": sub})


# ----------------------------------------------------------------------------- PMOS guard
def nwell_guard(pdk, top, refs, body: str = "VDD", gap: float = 0.36) -> Ring:
    """n+ tap ring with one merged NWELL around a group of PMOS (and their dummies)."""
    x0, y0, x1, y1 = _bbox(refs)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
    g = Component("nwell_guard")
    _tap(pdk, g, "n", 2 * (hw + gap), 2 * (hh + gap), "body_", keep_nwell=True)
    ref = top << g
    ref.move((cx, cy))
    return Ring(ref, (g.xsize, g.ysize), {"body": body})


# ----------------------------------------------------------------------------- wiring
def strap(pdk, top, a, b, layer: str = "met3", width: float | None = None,
          shift: float = 0.0):
    """Join two ports with a straight bar on `layer`, via-stacked down at each end.

    Use it to cross other rings (e.g. body ring -> substrate ring over the DNW tie ring).
    The bar runs along the axis where the two ports differ most.
    shift: slide the bar sideways along the ports (um). Two straps on the same layer
    must not overlap, so give each one its own shift.
    """
    la, lb = pdk.layer_to_glayer(a.layer), pdk.layer_to_glayer(b.layer)
    lay = pdk.get_glayer(layer)
    (ax, ay), (bx, by) = a.center, b.center
    vertical = abs(ax - bx) < abs(ay - by)
    if vertical:
        ax, bx = ax + shift, bx + shift
    else:
        ay, by = ay + shift, by + shift
    vias = []
    for (px, py), gl, p in (((ax, ay), la, a), ((bx, by), lb, b)):
        v = top << via_stack(pdk, gl, layer)
        # ports sit on the metal's outer edge: pull the pad back so it stays on the metal
        dx, dy = {0: (-1, 0), 90: (0, -1), 180: (1, 0), 270: (0, 1)}[round(p.orientation) % 360]
        px, py = px + dx * v.xsize / 2, py + dy * v.ysize / 2
        v.move((px - v.center[0], py - v.center[1]))
        vias.append(v)
    (ax, ay), (bx, by) = vias[0].center, vias[1].center
    w = width or max(vias[0].xsize, vias[0].ysize)
    if not vertical:                   # horizontal bar at a's y
        _rect(top, lay, min(ax, bx) - w / 2, ay - w / 2, max(ax, bx) + w / 2, ay + w / 2)
    else:                              # vertical bar at a's x
        _rect(top, lay, ax - w / 2, min(ay, by) - w / 2, ax + w / 2, max(ay, by) + w / 2)
    return vias


def label(pdk, top, port, text: str):
    """Put an LVS pin label on the metal of `port` (GF180 label datatype 10)."""
    gl = pdk.layer_to_glayer(port.layer)
    top.add_label(text=text, position=tuple(port.center), layer=pdk.get_glayer(f"{gl}_label"))
