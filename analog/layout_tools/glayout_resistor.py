"""
GF180 n-well resistor (`nwell`, 3 terminals: A, B, substrate) as a folded chain of bars.

    from glayout_resistor import nwell_res
    blk = nwell_res(pdk, top, "R0", w=2.0, l=150.0, a="Iref", b="Vgs", max_seg=40.0)
    blk.pads        # {"A": (x, y), "B": (x, y)}: met1 contact pads of the two end heads
    blk.spice       # LVS reference lines, one per bar (series chain, joint nets R0_j<k>)
    blk.bodies      # resistor bodies (NWELL and RES_MK) in `top` coordinates, for Magic PEX

Geometry is the PDK's own pcell (pymacros/cells/draw_res.py, draw_well_res), turned so the
length runs along y:
    RES_MK  (110/5)  w + 2 x 0.5 wide, l long: the resistor body; LVS L = its length
    NWELL            w wide, l + 2 x 0.48 long: the 0.48 um heads past RES_MK are the terminals
    COMP + NPLUS     in each head (NWELL enclosure 0.12, NPLUS 0.16 past COMP), contacts, met1
A resistor longer than `max_seg` becomes n bars side by side (NW.2b: 1.4 um apart), joined
alternately at the top and the bottom by met1 jumpers. LVS extracts one device per bar (the
GF180 deck does not combine series resistors by default), so the reference lists the same
chain: same total length, n - 1 extra heads in series (about 2 x 0.5 square of n-well each).

Rules (GF180, 3.3 V): NW.1b n-well resistor width >= 2 um, NW.2b spacing to other n-well
>= 1.4 um, NW.3 to DNWELL >= 3.1 um, DN.12 never inside DNWELL. The bulk is the substrate:
the cell's substrate rings tie it to VSS.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from gdsfactory.component import Component
from gdsfactory.components import rectangle

RES_MK = (110, 5)    # GF180 RES_MK marker (layers_definitions.lvs)
NW_RES_EXT = 0.48    # NWELL past RES_MK at each end (head), pcell
NW_RES_ENC = 0.5     # RES_MK past NWELL across the width, pcell
NW_ENC_CMP = 0.12    # NWELL enclosure of the head COMP
NP_ENC_CMP = 0.16    # NPLUS past COMP
BAR_SPACE = 1.4      # NW.2b: n-well to n-well, different potential
MIN_W = 2.0          # NW.1b
CO, CO_SP, CO_ENC = 0.22, 0.28, 0.07    # contact size, spacing, COMP enclosure
M1_ENC = 0.12        # met1 past contact (glayout's GF180 rule)
GRID = 0.01          # bar lengths: gdsfactory's rectangle rounds sizes to 10 nm (a 48.785 um bar
                     # came out 48.78, so LVS, which compares L exactly, did not match it)


@dataclass
class ResBlock:
    name: str
    ref: object                  # reference of the block in `top`
    pads: dict                   # "A" / "B" -> (x, y) of the end-head met1 pad centre
    spice: list                  # LVS reference lines
    bodies: list                 # [(x0, y0, x1, y1)] NWELL and RES_MK per bar, `top` coordinates
    met1: list = field(default_factory=list)   # [(x0, y0, x1, y1, net, tag)] for the router
    segments: list = field(default_factory=list)   # bar lengths (um)

    @property
    def xsize(self):
        return self.ref.xsize

    @property
    def ysize(self):
        return self.ref.ysize


def segment_lengths(l: float, max_seg: float) -> list:
    """Split l into the fewest bars of at most max_seg, equal to the 10 nm grid, summing to l."""
    total = round(l / GRID)
    n = max(1, math.ceil(l / max_seg - 1e-9))
    q, r = divmod(total, n)
    return [round((q + (1 if k < r else 0)) * GRID, 4) for k in range(n)]


def block_size(w: float, l: float, max_seg: float) -> tuple:
    """(width, height) of the block nwell_res would draw, without drawing it."""
    segs = segment_lengths(l, max_seg)
    return len(segs) * (w + BAR_SPACE) - BAR_SPACE + 2 * NW_RES_ENC, max(segs) + 2 * NW_RES_EXT


def _rect(comp, layer, x0, y0, x1, y1):
    r = comp << rectangle(size=(round(x1 - x0, 4), round(y1 - y0, 4)), layer=layer)
    r.move((x0, y0))
    return r


def _head(pdk, comp, x0, x1, y_out, y_in):
    """One terminal head between NWELL edge y_out and RES_MK edge y_in (either order); returns
    the met1 pad box."""
    lo, hi = sorted((y_out, y_in))
    out_lo = y_out < y_in                      # NWELL edge below the RES_MK edge (bottom head)
    c0, c1 = x0 + NW_ENC_CMP, x1 - NW_ENC_CMP
    d0, d1 = (lo + NW_ENC_CMP, hi) if out_lo else (lo, hi - NW_ENC_CMP)
    _rect(comp, pdk.get_glayer("active_tap"), c0, d0, c1, d1)
    _rect(comp, pdk.get_glayer("n+s/d"), c0 - NP_ENC_CMP, d0 - NP_ENC_CMP, c1 + NP_ENC_CMP, d1 + NP_ENC_CMP)
    n = max(1, int((c1 - c0 - 2 * CO_ENC + CO_SP) // (CO + CO_SP)))
    span = n * CO + (n - 1) * CO_SP
    cx0, cy = (c0 + c1) / 2 - span / 2, (d0 + d1) / 2
    for k in range(n):
        x = cx0 + k * (CO + CO_SP)
        _rect(comp, pdk.get_glayer("mcon"), x, cy - CO / 2, x + CO, cy + CO / 2)
    pad = (c0, cy - CO / 2 - M1_ENC, c1, cy + CO / 2 + M1_ENC)
    _rect(comp, pdk.get_glayer("met1"), *pad)
    return pad


def nwell_res(pdk, top, name: str, w: float, l: float, a: str, b: str, bulk: str = "VSS",
              max_seg: float = 40.0) -> ResBlock:
    """Draw the resistor into `top` with its lower-left RES_MK corner at (0, 0); place it with
    moved(), which shifts the reference and every coordinate the block reports."""
    if w < MIN_W - 1e-9:
        raise ValueError(f"{name}: n-well resistor width {w:g} um < {MIN_W:g} um (NW.1b)")
    segs = segment_lengths(l, max_seg)
    n = len(segs)
    c = Component(f"res_{name}")
    pitch = w + BAR_SPACE
    heads, bodies = [], []
    for k, sl in enumerate(segs):
        x0 = NW_RES_ENC + k * pitch                  # NWELL left edge
        x1 = x0 + w
        _rect(c, RES_MK, x0 - NW_RES_ENC, 0, x1 + NW_RES_ENC, sl)
        _rect(c, pdk.get_glayer("nwell"), x0, -NW_RES_EXT, x1, sl + NW_RES_EXT)
        bodies.append((x0, 0.0, x1, sl))
        heads.append(dict(bot=_head(pdk, c, x0, x1, -NW_RES_EXT, 0.0),
                          top=_head(pdk, c, x0, x1, sl + NW_RES_EXT, sl)))
    # chain: A at the bottom of bar 0, jumpers alternately at the top (0-1) and bottom (1-2)
    nets = [a] + [f"{name}_j{k}" for k in range(n - 1)] + [b]
    met1 = []
    for k, hd in enumerate(heads):
        for end in ("bot", "top"):
            # bar k runs from nets[k] to nets[k+1]; its bottom head is nets[k] for even k
            net = nets[k] if (end == "bot") == (k % 2 == 0) else nets[k + 1]
            met1.append((*hd[end], net, f"{name}.{k}.{end}"))
    for k in range(n - 1):
        end = "top" if k % 2 == 0 else "bot"
        p, q = heads[k][end], heads[k + 1][end]
        y0, y1 = min(p[1], q[1]), max(p[3], q[3])
        _rect(c, pdk.get_glayer("met1"), p[0], y0, q[2], y1)
        met1.append((p[0], y0, q[2], y1, nets[k + 1], f"{name}.jump{k}"))
    ref = top << c
    end_b = "top" if (n - 1) % 2 == 0 else "bot"
    pad_a, pad_b = heads[0]["bot"], heads[-1][end_b]
    rname = name if name.upper().startswith("R") else f"R{name}"
    # the PDK's spice->CDL converter strips one leading X; what is left must start with R
    spice = [f"X{rname}_s{k} {nets[k]} {nets[k + 1]} {bulk} nwell r_width={w:g}e-6 r_length={sl:g}e-6"
             for k, sl in enumerate(segs)] if n > 1 else \
            [f"X{rname} {a} {b} {bulk} nwell r_width={w:g}e-6 r_length={segs[0]:g}e-6"]
    centre = lambda p: ((p[0] + p[2]) / 2, (p[1] + p[3]) / 2)
    return ResBlock(name, ref, {"A": centre(pad_a), "B": centre(pad_b)}, spice, bodies, met1, segs)


def moved(blk: ResBlock, dx: float, dy: float) -> ResBlock:
    """Move the block's reference and every coordinate it reports by (dx, dy)."""
    blk.ref.move((dx, dy))
    sh = lambda bx: (bx[0] + dx, bx[1] + dy, bx[2] + dx, bx[3] + dy)
    blk.pads = {k: (x + dx, y + dy) for k, (x, y) in blk.pads.items()}
    blk.bodies = [sh(bx) for bx in blk.bodies]
    blk.met1 = [(*sh(m[:4]), *m[4:]) for m in blk.met1]
    return blk
