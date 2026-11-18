"""
Bias cell (analog/neuron/bias_cell.sch) layout generator for GF180MCU (gf180mcuD, variant D).

Run inside the iic-osic-tools container:
    klayout -b -r gen_bias.py -rd out=bias_cell.gds

Circuit: one external reference current Iref (pin) into the NMOS master MN0; MNP/MP0 form the
PMOS master. Every bias is a mirror output into a diode-connected replica of the transistor it
drives (sizes in analog/testbenches/bias/bias_cell_sizes.json, from bias_design.py):
    PMOS output -> NMOS replica: Vb, Vlk, VKdn, VIp, Vamp_bias, VK
    NMOS output -> PMOS replica: VNA, VKup, Vthr, VT_dpi, VT_inh

Floorplan: two tiers, each = NMOS row, gate-bus channel (Iref bus, vgp bus on Metal2), PMOS
row in an N-well with its N+ tap rail (VDD). Tier A (bottom) is tier B mirrored in y, so the two
NMOS rows share the central P+ tap rail (VSS). Each bias is one column: its mirror output and
its replica stacked; a Metal3 vertical joins their drains and runs to the pin, at the top edge
(tier B) or the bottom edge (tier A). Devices are multi-finger PCells (contacts between
fingers); sources strap to the rails on Metal1, drains to a Metal2 strap, gates to one Metal1
strap per device. The Iref and vgp buses of the two tiers are joined by Metal3 links at the
left end.

Pins: bias outputs on Metal3 (top / bottom edge, labelled); Iref, VDD, VSS on Metal2 at the
left edge; VSS / VDD also labelled on the Metal1 rails.
"""
import json
import os
import sys
import math
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet, draw_pfet  # noqa: E402

cells.gf180mcu()
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
OUT = globals().get("out", "bias_cell.gds")
SIZES = os.path.join(HERE, "..", "..", "testbenches", "bias", "bias_cell_sizes.json")

L = {"nwell": (21, 0), "comp": (22, 0), "poly": (30, 0), "pplus": (31, 0), "nplus": (32, 0),
     "cont": (33, 0), "m1": (34, 0), "via1": (35, 0), "m2": (36, 0), "via2": (38, 0), "m3": (42, 0),
     "bnd": (0, 0), "m1_lbl": (34, 10), "m2_lbl": (36, 10), "m3_lbl": (42, 10)}
ly = pya.Layout()
ly.dbu = 0.001
li = {k: ly.layer(*v) for k, v in L.items()}
W = json.load(open(SIZES))

# ------------------------------------------------------------------ circuit (as bias_design.py)
W0, LM = 10.0, 8.0
REPL = {  # bias: (replica type, W, L, m, mirror side, output L)
    "Vb": ("n", 1.0, 8.0, 1, "P", 8.0), "Vlk": ("n", 1.0, 1.0, 8, "P", 16.0),
    "VKdn": ("n", 1.0, 1.0, 4, "P", 8.0), "VIp": ("n", 1.0, 1.0, 1, "P", 8.0),
    "Vamp_bias": ("n", 0.22, 0.28, 1, "P", 8.0), "VK": ("n", 0.22, 40.0, 1, "P", 8.0),
    "VNA": ("p", 0.22, 20.0, 1, "N", 8.0), "VKup": ("p", 1.0, 8.0, 1, "N", 8.0),
    "Vthr": ("p", 0.22, 0.28, 32, "N", 32.0), "VT_dpi": ("p", 0.22, 0.28, 32, "N", 32.0),
    "VT_inh": ("p", 0.88, 1.12, 16, "N", 32.0),
}
WF_MAX = 5.0   # max finger width


def dev(name, kind, w_total, l, nets, m=1):
    """Device spec. Fingers: m copies (replicas), or the width split into <= WF_MAX fingers."""
    if m > 1:
        nf = m
    else:                       # smallest finger count >= W/WF_MAX that splits W exactly on the 5 nm grid
        units = round(w_total / 0.005)
        n0 = max(1, math.ceil(w_total / WF_MAX - 1e-9))
        nf = next((n for n in range(n0, n0 + 8) if units % n == 0), 1)
    wf = round((w_total / nf) / 0.005) * 0.005
    assert abs(wf * nf - w_total) < 1e-6 or m > 1, (name, w_total, nf)
    return {"name": name, "kind": kind, "wf": wf, "l": l, "nf": nf, "nets": nets}


# columns: (column net, NMOS device, PMOS device)
COLS_A, COLS_B = [], []
COLS_B.append(("Iref", dev("MN0", "n", W0, LM, {"G": "Iref", "D": "Iref"}), None))
COLS_B.append(("vgp", dev("MNP", "n", W["MNP"], LM, {"G": "Iref", "D": "vgp"}),
               dev("MP0", "p", W0, LM, {"G": "vgp", "D": "vgp"})))
for b, (k, w, l, m, side, lo) in REPL.items():
    if side == "P":
        col = (b, dev("MR_" + b, "n", w * m, l, {"G": b, "D": b}, m),
               dev("MO_" + b, "p", W[b], lo, {"G": "vgp", "D": b}))
    else:
        col = (b, dev("MO_" + b, "n", W[b], lo, {"G": "Iref", "D": b}),
               dev("MR_" + b, "p", w * m, l, {"G": b, "D": b}, m))
    (COLS_B if b in ("Vb", "Vlk", "VKdn", "VIp", "VK") else COLS_A).append(col)

# ------------------------------------------------------------------ PCell cache
_cache = {}


def fet_cell(kind, wf, l, nf, gate_pos):
    key = (kind, wf, l, nf, gate_pos)
    if key in _cache:
        return _cache[key]
    fn = draw_nfet if kind == "n" else draw_pfet
    sdl = 0.7                                 # internal S/D length: contact room (CO.7) and S/D-to-gate-pad M1 spacing (M1.2a)
    c = fn(ly, l_gate=l, w_gate=wf, nf=nf, inter_sd_l=sdl, con_bet_fin=1,
           gate_con_pos=gate_pos, bulk="None")
    c.flatten(True)
    if kind == "p":                           # the tier's N-well covers all PMOS
        c.shapes(li["nwell"]).clear()
    for k in li:
        r = pya.Region(c.shapes(li[k]))
        if not r.is_empty():
            c.shapes(li[k]).clear()
            c.shapes(li[k]).insert(r.snapped(5, 5))
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    sd = sorted([p for p in pads if p.bottom < wf / 2 < p.top], key=lambda b: b.center().x)
    if wf < 0.38 and nf > 1:
        # narrow fingers: the PCell widens the active area (dogbone) only at the two end contacts;
        # do the same at the internal ones (CO.4: COMP enclosure of contact >= 0.07 um)
        imp = "nplus" if kind == "n" else "pplus"
        for p in sd[1:-1]:
            cx, cy = p.center().x, p.center().y
            c.shapes(li["comp"]).insert(pya.DBox(cx - 0.19, cy - 0.19, cx + 0.19, cy + 0.19))
            c.shapes(li[imp]).insert(pya.DBox(cx - 0.35, cy - 0.35, cx + 0.35, cy + 0.35))
    gp = [p for p in pads if not (p.bottom < wf / 2 < p.top)]
    assert len(sd) == nf + 1 and len(gp) == nf, (key, len(sd), len(gp))
    core = pya.Region()
    for k in ("comp", "poly", "m1", "pplus", "nplus"):
        core += pya.Region(c.shapes(li[k]))
    _cache[key] = (c, sd, gp, core.bbox().to_dtype(ly.dbu))
    return _cache[key]


# ------------------------------------------------------------------ drawing helpers
class Drawer:
    def __init__(self, cell):
        self.cell = cell

    def box(self, layer, x1, y1, x2, y2):
        self.cell.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    def sq(self, layer, cx, cy, s):
        self.box(layer, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)

    def via(self, cx, cy, lo, hi, m1_pad=True):
        """stacked vias from metal lo to hi (1..3); m1_pad=False: land Via1 on an existing M1 pad"""
        cx, cy = snap(cx), snap(cy)
        for m in range(lo, hi + 1):
            if m == 1 and not m1_pad:
                continue
            self.sq("m%d" % m, cx, cy, 0.4)
        for v in range(lo, hi):
            self.sq("via%d" % v, cx, cy, 0.26)

    def contacts(self, x1, y1, x2, y2, pitch=0.5):
        if (x2 - x1) >= (y2 - y1):
            n = int((x2 - x1 - 0.22 - 0.2) / pitch) + 1
            x0 = (x1 + x2) / 2 - (n - 1) * pitch / 2
            for i in range(n):
                self.sq("cont", x0 + i * pitch, (y1 + y2) / 2, 0.22)
        else:
            n = int((y2 - y1 - 0.22 - 0.2) / pitch) + 1
            y0 = (y1 + y2) / 2 - (n - 1) * pitch / 2
            for i in range(n):
                self.sq("cont", (x1 + x2) / 2, y0 + i * pitch, 0.22)

    def tap(self, x1, y1, x2, y2, implant):
        self.box("comp", x1, y1, x2, y2)
        self.box("m1", x1, y1, x2, y2)
        self.box(implant, x1 - 0.16, y1 - 0.16, x2 + 0.16, y2 + 0.16)
        self.contacts(x1, y1, x2, y2)


GAP = 1.2        # between devices / columns


def snap(v):
    return round(v / 0.005) * 0.005
RAIL_W = 0.5     # tap rail width
TW = 0.4         # metal track width


# ------------------------------------------------------------------ one tier
def build_tier(name, cols, w_force=None):
    """Tier in local coordinates: VSS rail at y = 0..RAIL_W, NMOS row, channel, PMOS row, VDD rail.
    Returns the cell and geometry (bias pin x at the top edge, bus y, heights)."""
    cell = ly.create_cell(name)
    d = Drawer(cell)
    # row heights from the devices
    def ext(dv, gate_pos):
        c, sd, gp, core = fet_cell(dv["kind"], dv["wf"], dv["l"], dv["nf"], gate_pos)
        return c, sd, gp, core
    n_h = max(ext(c[1], "top")[3].height() for c in cols if c[1])
    p_h = max(ext(c[2], "bottom")[3].height() for c in cols if c[2])
    Y_DN = RAIL_W + 0.6 + 0.4 + 0.6                   # NMOS D strap (M2) centre
    Y_NB = Y_DN + 0.2 + 0.9                           # NMOS core bottom
    Y_NT = Y_NB + n_h                                 # NMOS core top (gate pads)
    Y_IREF = Y_NT + 0.8 + 0.9 + 0.2                   # Iref bus (M2), clear of the gate straps
    Y_VGP = Y_IREF + 1.2                              # vgp bus (M2)
    Y_PB = Y_VGP + 0.2 + 0.9 + 0.8 + 1.4              # PMOS core bottom (gate pads); NWELL starts below
    Y_PT = Y_PB + p_h
    Y_DP = Y_PT + 0.9 + 0.2                           # PMOS D strap
    Y_VDD0 = Y_DP + 0.2 + 0.6 + 0.4 + 0.6             # VDD N+ tap rail bottom
    H = Y_VDD0 + RAIL_W
    x = 2 * TW + 3.0                                  # left margin: bus links (top level)
    geo = {"pins": {}, "Y_IREF": Y_IREF, "Y_VGP": Y_VGP, "H": H, "x0": x}
    bus_x = {"Iref": [], "vgp": []}
    for (net, nd, pd) in cols:
        devs = []
        for dv, gate_pos in ((nd, "top"), (pd, "bottom")):
            if dv:
                devs.append((dv, gate_pos) + ext(dv, gate_pos))
        w_col = max(core.width() for (_, _, _, _, _, core) in devs)
        placed = []
        for (dv, gate_pos, c, sd, gp, core) in devs:
            ox = snap(x + (w_col - core.width()) / 2 - core.left)
            oy = (Y_NB - core.bottom) if dv["kind"] == "n" else (Y_PB - core.bottom)
            t = pya.DTrans(ox, oy)
            cell.insert(pya.DCellInstArray(c.cell_index(), t))
            sdp = [t * p for p in sd]
            gpp = [t * p for p in gp]
            placed.append((dv, sdp, gpp))
        # column vertical x: centre of the column
        xc = snap(x + w_col / 2)
        verts = []
        for (dv, sdp, gpp) in placed:
            nmos = dv["kind"] == "n"
            rail_y = (0.0, RAIL_W) if nmos else (Y_VDD0, H)
            ystrap = Y_DN if nmos else Y_DP
            # sources (even pads) -> rail on M1
            for p in sdp[0::2]:
                if nmos:
                    d.box("m1", p.left, rail_y[1] - 0.01, p.right, p.top)
                else:
                    d.box("m1", p.left, p.bottom, p.right, rail_y[0] + 0.01)
            # drains (odd pads) -> via1 -> M2 down/up to the drain strap
            xs = []
            for p in sdp[1::2]:
                cx = p.center().x
                d.via(cx, p.center().y, 1, 2, m1_pad=False)     # the PCell pad (0.38 um) encloses Via1
                cx = snap(cx)
                d.box("m2", cx - 0.2, min(snap(p.center().y), ystrap), cx + 0.2, max(snap(p.center().y), ystrap))
                xs.append(cx)
            x_lo, x_hi = min(xs + [xc]) - 0.2, max(xs + [xc]) + 0.2
            d.box("m2", x_lo, ystrap - 0.2, x_hi, ystrap + 0.2)
            if dv["nets"]["D"] == net:
                d.via(xc, ystrap, 2, 3)
                verts.append(ystrap)
            # gate pads -> one M1 bar along the outer pad row (or just outside a single row);
            # the inner pads join it with a vertical inside their own x range. A bar at the inner
            # row would run 0.22 um from the S/D pads (M1.2a).
            outward = 1 if nmos else -1                  # NMOS gate pads face up, PMOS down
            rows = sorted({round(g.center().y, 3) for g in gpp}, key=lambda yy: outward * yy)
            gx0, gx1 = min(g.left for g in gpp), max(g.right for g in gpp)
            gx1 = max(gx1, xc + 0.3)
            gx0 = min(gx0, xc - 0.3)
            if len(rows) > 1:
                outer = [g for g in gpp if round(g.center().y, 3) == rows[-1]][0]
                bb, bt = outer.bottom, outer.top
            else:
                g0 = gpp[0]
                bb, bt = (g0.top + 0.3, g0.top + 0.7) if nmos else (g0.bottom - 0.7, g0.bottom - 0.3)
            d.box("m1", gx0, bb, gx1, bt)
            for g in gpp:
                if not (abs(g.bottom - bb) < 1e-6 and abs(g.top - bt) < 1e-6):
                    d.box("m1", g.left, min(g.bottom, bb), g.right, max(g.top, bt))
            gy = (bb + bt) / 2
            g = dv["nets"]["G"]
            if g == net:                                 # diode: gate strap to the column vertical
                d.via(xc, gy, 1, 3)
                verts.append(gy)
            else:                                        # gate on a bus: M2 stub
                bus_y = Y_IREF if g == "Iref" else Y_VGP
                xs_ = gx0 + 0.3
                d.via(xs_, gy, 1, 2)
                d.box("m2", xs_ - 0.2, min(gy, bus_y), xs_ + 0.2, max(gy, bus_y))
                bus_x[g].append(xs_)
        # column net onto its bus (master columns)
        if net in ("Iref", "vgp"):
            by = Y_IREF if net == "Iref" else Y_VGP
            d.via(xc, by, 2, 3)
            verts.append(by)
            bus_x[net].append(xc)
            d.box("m3", xc - TW / 2, min(verts) - 0.2, xc + TW / 2, max(verts) + 0.2)
        else:                                            # bias column: vertical to the top edge (pin)
            d.box("m3", xc - TW / 2, min(verts) - 0.2, xc + TW / 2, H + 1.5)
            geo["pins"][net] = xc
        x += w_col + GAP
    W_T = max(x - GAP + 1.5, w_force or 0)
    geo["W"] = W_T
    # buses (M2) from the left margin to the last user
    geo["buses"] = [net for net in ("Iref", "vgp") if bus_x[net]]
    for net, by in (("Iref", Y_IREF), ("vgp", Y_VGP)):
        if bus_x[net]:                                 # a tier may have no user of a bus
            d.box("m2", geo["x0"] - 2.0, by - TW / 2, max(bus_x[net]) + 0.2, by + TW / 2)
    # rails: VSS P+ tap at the bottom, VDD N+ tap at the top, N-well over the PMOS row
    d.tap(0.0, Y_VDD0, W_T, H, "nplus")              # (the shared VSS rail is drawn at the top level)
    d.box("nwell", -0.6, Y_PB - 1.0, W_T + 0.6, H + 0.6)
    return cell, geo


_, g1 = build_tier("tmpB", COLS_B)
_, g2 = build_tier("tmpA", COLS_A)
WW = max(g1["W"], g2["W"])
for c in ("tmpA", "tmpB"):
    ly.delete_cell(ly.cell(c).cell_index())
cellB, gB = build_tier("bias_tierB", COLS_B, WW)
cellA, gA = build_tier("bias_tierA", COLS_A, WW)

# ------------------------------------------------------------------ top: A mirrored below B
top = ly.create_cell("bias_cell")
D = Drawer(top)
PAD_EDGE = 1.5                                       # pins: M3 verticals run 1.5 um past the rails
Y_MID = gA["H"] + PAD_EDGE                           # shared VSS rail at y = Y_MID .. +RAIL_W
top.insert(pya.DCellInstArray(cellB.cell_index(), pya.DTrans(0, Y_MID)))
top.insert(pya.DCellInstArray(cellA.cell_index(), pya.DTrans(0, Y_MID + RAIL_W) * pya.DTrans(pya.DTrans.M0)))
CH = Y_MID + gB["H"] + PAD_EDGE
CW = WW
D.tap(0.0, Y_MID, CW, Y_MID + RAIL_W, "pplus")      # shared VSS rail (P+ substrate tap)
# VDD: join the two N+ tap rails with a Metal3 link at the right edge
xv = CW - 0.6
yt_r = Y_MID + gB["H"] - RAIL_W / 2
yb_r = Y_MID + RAIL_W - (gA["H"] - RAIL_W / 2)
D.via(xv, yt_r, 1, 3)
D.via(xv, yb_r, 1, 3)
D.box("m3", xv - TW / 2, yb_r - 0.2, xv + TW / 2, yt_r + 0.2)
# bus links between the tiers (M3) at the left margin
for i, (net, yb, ya) in enumerate((("Iref", gB["Y_IREF"], gA["Y_IREF"]), ("vgp", gB["Y_VGP"], gA["Y_VGP"]))):
    if not (net in gB["buses"] and net in gA["buses"]):
        assert net != "Iref"                           # the Iref link also carries the Iref pin
        continue
    xl = 1.0 + 1.0 * i
    y_b, y_a = Y_MID + yb, Y_MID + RAIL_W - ya
    D.via(xl, y_b, 2, 3)
    D.via(xl, y_a, 2, 3)
    D.box("m3", xl - TW / 2, y_a - 0.2, xl + TW / 2, y_b + 0.2)
    D.box("m2", xl - 0.2, y_b - TW / 2, gB["x0"] - 1.9, y_b + TW / 2)
    D.box("m2", xl - 0.2, y_a - TW / 2, gA["x0"] - 1.9, y_a + TW / 2)


def pin(name, layer, x1, y1, x2, y2):
    D.box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


for net, xc in gB["pins"].items():
    pin(net, "m3", xc - TW / 2, CH - 0.6, xc + TW / 2, CH)
for net, xc in gA["pins"].items():
    pin(net, "m3", xc - TW / 2, 0.0, xc + TW / 2, 0.6)
# Iref pin: from the Iref link, on M2 at the shared rail height ... use the link itself on M3
yI = Y_MID + RAIL_W / 2
D.via(1.0, yI, 2, 3)
pin("Iref", "m2", -0.6, yI - 0.2, 1.2, yI + 0.2)
# VSS / VDD: labels on the rails and M2 stubs at the right edge
pin("VSS", "m1", CW - 2.0, Y_MID, CW - 1.0, Y_MID + RAIL_W)
yt = Y_MID + gB["H"] - RAIL_W / 2
yb = Y_MID + RAIL_W - (gA["H"] - RAIL_W / 2)
pin("VDD", "m1", CW - 2.0, yt - 0.25, CW - 1.0, yt + 0.25)
top.shapes(li["m1_lbl"]).insert(pya.DText("VDD", pya.DTrans(CW - 1.5, yb)))
# Metal2 edge pins for the supplies (right edge): VDD at both N+ rails (from the VDD link),
# VSS from the shared P+ rail
for yy in (yt_r, yb_r):
    pin("VDD", "m2", xv - 0.2, yy - 0.2, CW + 0.6, yy + 0.2)
ys = Y_MID + RAIL_W / 2
D.via(CW - 1.6, ys, 1, 2)
pin("VSS", "m2", CW - 1.8, ys - 0.2, CW + 0.6, ys + 0.2)
# the tiers' N-wells reach 0.6 um past x = 0 and x = CW: shift everything inside the boundary
top.flatten(-1, True)
top.transform(pya.DTrans(0.6, 0))
CW += 1.2
top.shapes(li["bnd"]).insert(pya.DBox(0, 0, CW, CH))
for ci in [c.cell_index() for c in ly.top_cells() if c.cell_index() != top.cell_index()]:
    ly.delete_cell_rec(ci)
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
print("tier B:", [c[0] for c in COLS_B], "\ntier A:", [c[0] for c in COLS_A])
