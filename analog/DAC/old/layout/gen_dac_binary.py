"""
Binary DAC (DAC_binary.sch, weights 1:2:4:8 with multi-finger devices) layout generator
for GF180MCU (gf180mcuD, variant D: 5LM).

Run inside the iic-osic-tools container:
    klayout -b -r gen_dac_binary.py -rd out=DAC_binary.gds

Circuit: each branch k (= 1, 2, 4, 8) is a current source W = k x 1 um, L = 8 um, nf = k
(gate Vb) switched by W = k x 0.22 um, L = 0.28 um, nf = k (gate w[b]) into X; Men (gate en)
passes X to Isum. Switch bodies sit on their branch nodes (as in the schematic).

    branch  source   switch   gate   branch node
    A x1    M2       M1       w[0]   net4
    B x2    M4       M3       w[1]   net2
    C x4    M6       M5       w[2]   net3
    D x8    M8       M7       w[3]   net1

The fingers are laid out as separate unit devices so that they can be interleaved; LVS
combines parallel fingers, so it compares them with the schematic's W/nf devices.

Layout (same rules as gen_dac.py for the 1:2:3:4 DAC):
  * Deep N-well (VDD pin), each branch's switches in their own LVPWELL whose P+ ring is
    the body tap (branch node); Men and the array in grounded LVPWELLs; P+ substrate ring.
  * The 15 unit sources form a 3 x 5 common-centroid array, point-symmetric about the
    centre unit, so every branch centroid is exactly at the array centre:
        top     D C D C D
        middle  B D A D B
        bottom  D C D C D
    No two units of the same branch touch. A full ring of identical dummies surrounds it
    (5 x 7 positions, 20 dummies). Each switch row (and Men) also sits in a full dummy
    ring: identical dummies above and below every switch plus one at each row end, all on
    the well's body net (3 x (k+2) positions per branch).
  * Floorplan: the switch islands (Men, A..D) form one row along the top; the current-source
    array sits directly below them, right-aligned with island D. (The generator builds the
    islands below the array and mirrors the finished cell in y.)
  * Routing: channel A (bottom/middle rows) carries all four branch nodes; branches C and D
    also use channel B (middle/top rows). Channel C, between the X/Isum channel and the
    array, carries the four branch nodes from the island rings to one M2 riser per node in
    the free space left of the array, which joins channels C, A (and B). Signals are on
    Metal3 with GND shields on Metal1 between them (alternating layers); the middle row's
    GND sources strap onto the top shield of channel A. The X/Isum and channel C shields
    are tied to the array ring by an M1 GND spine at the right end; the array ring goes to
    the substrate ring on the right. Vb stays inside the array. The digital lines run above
    the switches, X and Isum between the switches and the array, both shielded.
  * Pins (Metal2 at the edge, labelled): left Isum, en, w[0]..w[3]; right Vb, VDD, GND;
    GND also on the Metal1 substrate ring.
"""
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet  # noqa: E402

cells.gf180mcu()
OUT = globals().get("out", "DAC_binary.gds")

# ------------------------------------------------------------------ layers / helpers
L = {
    "dnwell": (12, 0), "comp": (22, 0), "poly": (30, 0),
    "pplus": (31, 0), "nplus": (32, 0), "cont": (33, 0), "m1": (34, 0),
    "via1": (35, 0), "m2": (36, 0), "via2": (38, 0), "m3": (42, 0),
    "lvpwell": (204, 0), "bnd": (0, 0),
    "m1_lbl": (34, 10), "m2_lbl": (36, 10),
}
ly = pya.Layout()
ly.dbu = 0.001
top = ly.create_cell("DAC_binary")
li = {k: ly.layer(*v) for k, v in L.items()}


def box(layer, x1, y1, x2, y2):
    top.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def sq(layer, cx, cy, s):
    box(layer, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)


VIA = 0.26
_vias = []


def via12(cx, cy):
    """Via1 with 0.4 um M1 and M2 pads; merges with an existing via at the same spot."""
    sq("m1", cx, cy, 0.4)
    sq("m2", cx, cy, 0.4)
    if any(abs(cx - x) < 0.52 and abs(cy - y) < 0.52 for (x, y) in _vias):
        return
    _vias.append((cx, cy))
    sq("via1", cx, cy, VIA)


_vias2 = []


def via23(cx, cy):
    """Via2 with 0.4 um M2 and M3 pads; merges with an existing via at the same spot."""
    sq("m2", cx, cy, 0.4)
    sq("m3", cx, cy, 0.4)
    if any(abs(cx - x) < 0.52 and abs(cy - y) < 0.52 for (x, y) in _vias2):
        return
    _vias2.append((cx, cy))
    sq("via2", cx, cy, VIA)


def contacts(x1, y1, x2, y2, pitch=0.5):
    """Contacts along the long axis, kept >= 0.1 um from the strip ends (CO.4)."""
    if (x2 - x1) >= (y2 - y1):
        n = int((x2 - x1 - 0.22 - 0.2) / pitch) + 1
        x0 = (x1 + x2) / 2 - (n - 1) * pitch / 2
        for i in range(n):
            sq("cont", x0 + i * pitch, (y1 + y2) / 2, 0.22)
    else:
        n = int((y2 - y1 - 0.22 - 0.2) / pitch) + 1
        y0 = (y1 + y2) / 2 - (n - 1) * pitch / 2
        for i in range(n):
            sq("cont", (x1 + x2) / 2, y0 + i * pitch, 0.22)


RW = 0.5   # ring width


def ring(x1, y1, x2, y2, implant, w=RW):
    """Guard ring (COMP + implant + M1 + contacts), outer edge (x1,y1,x2,y2)."""
    sides = [(x1, y1, x2, y1 + w), (x1, y2 - w, x2, y2),
             (x1, y1 + w, x1 + w, y2 - w), (x2 - w, y1 + w, x2, y2 - w)]
    for s in sides:
        box("comp", *s)
        box("m1", *s)
        box(implant, s[0] - 0.16, s[1] - 0.16, s[2] + 0.16, s[3] + 0.16)
    contacts(*sides[0])
    contacts(*sides[1])
    for s in sides[2:]:
        contacts(s[0], s[1] + 0.3, s[2], s[3] - 0.3)
    return sides


def strip(x1, y1, x2, y2, implant):
    box("comp", x1, y1, x2, y2)
    box("m1", x1, y1, x2, y2)
    box(implant, x1 - 0.16, y1 - 0.16, x2 + 0.16, y2 + 0.16)
    contacts(x1, y1, x2, y2)


# ------------------------------------------------------------------ devices
def make_fet(w, l, gate_pos):
    c = draw_nfet(ly, l_gate=l, w_gate=w, nf=1, con_bet_fin=0 if w < 0.36 else 1,
                  gate_con_pos=gate_pos, bulk="None")
    c.flatten(True)
    for k in li:                                   # snap to the 5 nm grid
        r = pya.Region(c.shapes(li[k]))
        if not r.is_empty():
            c.shapes(li[k]).clear()
            c.shapes(li[k]).insert(r.snapped(5, 5))
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    mid = w / 2
    sd = sorted([p for p in pads if p.bottom < mid < p.top], key=lambda b: b.center().x)
    gp = sorted([p for p in pads if not (p.bottom < mid < p.top)], key=lambda b: b.center().y)
    assert len(sd) == 2 and gp, (w, l, pads)
    core = pya.Region()
    for k in ("comp", "poly", "m1"):
        core += pya.Region(c.shapes(li[k]))
    return c, sd, gp, core.bbox().to_dtype(ly.dbu)


_cache = {}


def fet(w, l, gate_pos):
    key = (w, l, gate_pos)
    if key not in _cache:
        _cache[key] = make_fet(*key)
    return _cache[key]


DOFF = 0.35      # S/D tab offset
GAP = 0.7        # horizontal gap between device extents
ROWGAP = 0.5     # vertical clearance between stacked rows


def extent(w, l, gpos):
    c, sd, gp, core = fet(w, l, gpos)
    left = min(core.left, sd[0].center().x - DOFF - 0.2)
    right = max(core.right, sd[1].center().x + DOFF + 0.2)
    return left, right, core.bottom - w / 2, core.top - w / 2


def place(name, w, l, gpos, ox, y, nets):
    """Place an (unflipped) NMOS: origin x ox, S/D centre line y. nets = (S, G, D)."""
    c, sd, gp, core = fet(w, l, gpos)
    t = pya.DTrans(ox, y - w / 2)
    top.insert(pya.DCellInstArray(c.cell_index(), t))
    return {"name": name, "S": sd[0].moved(ox, y - w / 2), "D": sd[1].moved(ox, y - w / 2),
            "gates": sorted([g.moved(ox, y - w / 2) for g in gp], key=lambda b: b.center().y),
            "nets": dict(zip("SGD", nets)), "y": y}


def tab(d, t):
    """M1 tab outward from the S (left) or D (right) pad; returns the tab x."""
    p = d[t]
    if t == "S":
        x = p.center().x - DOFF
        box("m1", x - 0.2, p.bottom, p.right, p.top)
    else:
        x = p.center().x + DOFF
        box("m1", p.left, p.bottom, x + 0.2, p.top)
    return x


def vbar(x, y1, y2, layer="m1"):
    box(layer, x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def gate_tie(d, up):
    """Tie a dummy's gate pad (top if up else bottom) to its S tab with solid M1."""
    g = d["gates"][-1] if up else d["gates"][0]
    s = d["S"]
    xt = s.center().x - DOFF
    if up:
        box("m1", xt - 0.2, s.bottom, s.right, g.top)
    else:
        box("m1", xt - 0.2, g.bottom, s.right, s.top)
    box("m1", s.right - 0.01, g.bottom, g.center().x, g.top)


def stub(x, y0, y1, top="m1"):
    """M2 vertical from an M1 pad at y0 to a track at y1 on M1 (via1) or M3 (via2)."""
    via12(x, y0)
    vbar(x, y0, y1, "m2")
    if top == "m1":
        via12(x, y1)
    else:
        via23(x, y1)


def escape(y, layer):
    """Pin escape at ESC_L: from an M1 or M3 track down/up to the M2 pin stub."""
    if layer == "m1":
        via12(ESC_L, y)
    else:
        via23(ESC_L, y)
    box("m2", 0.0, y - 0.2, ESC_L, y + 0.2)


# ------------------------------------------------------------------ circuit data
UW, UL = 1.0, 8.0          # unit current source
SW, SL = 0.22, 0.28        # unit switch / Men
BR = {  # branch: (source name, switch name, units, switch gate, branch node)
    "A": ("M2", "M1", 1, "w[0]", "net4"),
    "B": ("M4", "M3", 2, "w[1]", "net2"),
    "C": ("M6", "M5", 4, "w[2]", "net3"),
    "D": ("M8", "M7", 8, "w[3]", "net1"),
}
ROWS = {"1": "DCDCD", "2": "BDADB", "3": "DCDCD"}   # bottom, middle, top (columns 1..5)
TRACK_ORDER = ["net3", "net1", "net4", "net2"]     # channel A, bottom -> top (C < D < A < B)
CHB_ORDER = ["net1", "net3"]                       # channel B (top-row branches D, C)
DIG = ["en", "w[0]", "w[1]", "w[2]", "w[3]"]     # digital tracks, top -> bottom
# Horizontal tracks alternate between Metal1 and Metal3 in every channel, so that two
# neighbouring tracks are never on the same layer:
#   channel A        net3 M3 | sh M1 | net1 M3 | sh M1 | net4 M3 | sh M1 | net2 M3 | sh M1
#   channel B        sh M1 | net1 M3 | sh M1 | net3 M3 | sh M1
#   switch channel   shield M1 | X M3 | shield M1 | Isum M3 | shield M1
#   digital channel  shield M1 | en M3 | w[0] M1 | w[1] M3 | w[2] M1 | w[3] M3
SIG_LAYER = "m3"                                 # X, Isum and the branch nodes
DIG_LAYER = {"en": "m3", "w[0]": "m1", "w[1]": "m3", "w[2]": "m1", "w[3]": "m3"}
TP, TW = 0.8, 0.4                                # track pitch / width

# ------------------------------------------------------------------ x floorplan
OR_O, OR_W = 0.3, 0.5
DN_X0 = OR_O + OR_W + 2.7                  # DNWELL left edge (3.5)
ESC_L = DN_X0 + 1.0                        # pin escape vias (inside DNWELL, left of the wells)
WELL_GAP = 1.8                             # LVPWELL spacing between islands (LPW.2a: 1.4)

# switch islands: Men island first (next to the Isum / en pins), then A..D
ISL = [("MEN", "GND", 1, "en")] + [(k, BR[k][4], BR[k][2], BR[k][3]) for k in "ABCD"]
sl, sr, srel_lo, srel_hi = extent(SW, SL, "bottom")    # switch row / bottom dummy row
_, _, trel_lo, trel_hi = extent(SW, SL, "top")          # top dummy row (gate contact on top)
SPITCH = (sr - sl) + GAP
islands = []
x = DN_X0 + 2.5                            # first LVPWELL edge
for (key, body, m, gate) in ISL:
    n_dev = m + 2                          # + one dummy at each end
    lpw_x0 = x
    ring_x0 = lpw_x0 + 0.4
    dev_x0 = ring_x0 + RW + 0.7
    origins = [dev_x0 - sl + i * SPITCH for i in range(n_dev)]
    ring_x1 = dev_x0 + n_dev * SPITCH - GAP + 0.7 + RW
    lpw_x1 = ring_x1 + 0.4
    islands.append({"key": key, "body": body, "m": m, "gate": gate, "origins": origins,
                    "lpw": (lpw_x0, lpw_x1), "ring": (ring_x0, ring_x1)})
    x = lpw_x1 + WELL_GAP
SW_X1 = islands[-1]["lpw"][1]

# current-source array
ul, ur, urel_lo_t, urel_hi_t = extent(UW, UL, "top")
_, _, urel_lo_b, urel_hi_b = extent(UW, UL, "bottom")
UPITCH = (ur - ul) + GAP
# The array sits directly above the switch row (below it after the final mirror), right-
# aligned with it, so that its LVPWELL ends where island D's does.
A_W = 0.4 + RW + 0.8 + 7 * UPITCH - GAP + 0.6 + 0.2 + 0.8 + RW + 0.4
A_LPW_X0 = SW_X1 - A_W
A_RING_X0 = A_LPW_X0 + 0.4
A_DEV_X0 = A_RING_X0 + RW + 0.8
col_ox = [A_DEV_X0 - ul + i * UPITCH for i in range(7)]
VB_X = A_DEV_X0 + 7 * UPITCH - GAP + 0.6   # Vb riser, right of the dummy column
A_RING_X1 = VB_X + 0.2 + 0.8 + RW
A_LPW_X1 = A_RING_X1 + 0.4
assert abs(A_LPW_X1 - SW_X1) < 1e-6
# one M2 riser per branch node, channel C <-> A (<-> B). The array is narrower than the
# switch row, so the risers go in the free space left of the array, just left of island A's
# ring riser (nothing else runs vertically there in channel C).
X_RISER_A = islands[1]["ring"][0] + 0.25
JOIN_X = {n: X_RISER_A - 0.9 - i * 0.8 for i, n in enumerate(TRACK_ORDER)}
assert max(JOIN_X.values()) + 0.2 < A_RING_X0 and min(JOIN_X.values()) - 0.8 > ESC_L
GSPINE_X = SW_X1 - 1.0                     # M1 GND spine: channel shields -> array ring
DN_X1 = A_LPW_X1 + 2.5
CW = DN_X1 + 2.7 + OR_W + OR_O

# ------------------------------------------------------------------ y floorplan
# Built bottom -> top as: digital channel, switch islands, X/Isum channel, branch channel C,
# array (with channels A and B inside). The finished cell is mirrored in y at the end, so
# the array ends up below the switches.
C_ORDER = TRACK_ORDER                      # channel C (switch side of the array), bottom -> top


def layout_y(base):
    y = {}
    # switch islands: bottom dummy row / switch row / top dummy row in a dummy ring
    y["s_ring0"] = base                                            # island ring outer bottom
    y["sb"] = y["s_ring0"] + RW + 0.6 - srel_lo                    # bottom dummy row
    y["sw"] = y["sb"] + (srel_hi - srel_lo + ROWGAP)               # switch S/D centre line
    y["st"] = y["sw"] + (srel_hi - trel_lo + ROWGAP)               # top dummy row
    y["s_ring1"] = y["st"] + RW + 0.6 + trel_hi                    # island ring outer top
    # analog channel t0..t4 (shield, X, shield, Isum, shield) above the islands
    y["sh"] = [y["s_ring1"] + TW / 2 + 0.9 + i * TP for i in range(5)]
    y["X"], y["Isum"] = y["sh"][1], y["sh"][3]
    # channel C: the four branch nodes, each with a GND shield above it
    y["C"] = {n: y["sh"][4] + (2 * i + 1) * TP for i, n in enumerate(C_ORDER)}
    y["csh"] = [y["sh"][4] + (2 * i + 2) * TP for i in range(len(C_ORDER))]
    # array: ring, bottom dummy row, row 1 (gate bottom), channel A, row 2, channel B, row 3
    y["a_ring0"] = y["csh"][-1] + TW / 2 + 0.9                     # array ring outer bottom
    y["rb"] = y["a_ring0"] + RW + 0.6 - urel_lo_b                  # bottom dummy row
    y["r1"] = y["rb"] + (urel_hi_b - urel_lo_b) + ROWGAP
    T5 = y["r1"] + urel_hi_b + 0.6 + TW / 2                        # lowest channel A track
    y["T"] = {n: T5 + 2 * i * TP for i, n in enumerate(TRACK_ORDER)}
    y["bsh"] = [T5 + (2 * i + 1) * TP for i in range(len(TRACK_ORDER))]
    y["r2"] = y["bsh"][-1] + TW / 2 + 0.6 - urel_lo_t
    B0 = y["r2"] + urel_hi_t + 0.6 + TW / 2
    y["TB"] = {n: B0 + (2 * i + 1) * TP for i, n in enumerate(CHB_ORDER)}
    y["bshB"] = [B0 + 2 * i * TP for i in range(len(CHB_ORDER) + 1)]
    y["r3"] = y["bshB"][-1] + TW / 2 + 0.6 - urel_lo_t
    y["rt"] = y["r3"] + (urel_hi_t - urel_lo_t) + ROWGAP          # top dummy row
    y["a_ring1"] = y["rt"] + urel_hi_t + 0.6 + RW                  # array ring outer top
    # digital channel below the islands
    y["dsh"] = y["s_ring0"] - 0.4 - 0.9                            # digital GND shield
    y["dig"] = {n: y["dsh"] - (i + 1) * TP for i, n in enumerate(DIG)}
    return y


y0 = layout_y(0.0)
DN_Y0 = OR_O + OR_W + 2.7
BASE = max(DN_Y0 + 0.4 + 2.5,                                       # LVPWELL 2.5 inside DNWELL
           OR_O + OR_W + 0.8 + TW / 2 - min(y0["dig"].values()))   # digital tracks above ring
Y = layout_y(BASE)
A_LPW_Y1 = Y["a_ring1"] + 0.4
VDD_Y = A_LPW_Y1 + 1.25                     # N+ tap strip (DNWELL tie) centre
DN_Y1 = A_LPW_Y1 + 2.5
CH = DN_Y1 + 2.7 + OR_W + OR_O
assert Y["a_ring1"] + 0.4 < VDD_Y - 0.25
assert Y["a_ring0"] - 0.4 - (Y["s_ring1"] + 0.4) >= 1.4          # LVPWELL spacing (LPW.2a)

# ------------------------------------------------------------------ wells, rings, taps
box("dnwell", DN_X0, DN_Y0, DN_X1, DN_Y1)
ring(OR_O, OR_O, CW - OR_O, CH - OR_O, "pplus")                                  # GND substrate
strip(DN_X0 + 1.0, VDD_Y - 0.25, DN_X1 - 1.0, VDD_Y + 0.25, "nplus")             # VDD DNWELL tie
box("lvpwell", A_LPW_X0, Y["a_ring0"] - 0.4, A_LPW_X1, A_LPW_Y1)
aring = ring(A_RING_X0, Y["a_ring0"], A_RING_X1, Y["a_ring1"], "pplus")         # array (GND)
for isl in islands:
    box("lvpwell", isl["lpw"][0], Y["s_ring0"] - 0.4, isl["lpw"][1], Y["s_ring1"] + 0.4)
    isl["sides"] = ring(isl["ring"][0], Y["s_ring0"], isl["ring"][1], Y["s_ring1"], "pplus")

# GND connections: array ring -> substrate ring; Men ring -> substrate ring (left)
for ys in (Y["a_ring0"] + 3.0, (Y["a_ring0"] + Y["a_ring1"]) / 2, Y["a_ring1"] - 3.0):
    box("m1", A_RING_X1 - 0.01, ys - 0.5, CW - OR_O - OR_W + 0.01, ys + 0.5)
men = islands[0]
ym = (Y["s_ring0"] + Y["s_ring1"]) / 2
box("m1", OR_O + OR_W - 0.01, ym - 0.5, men["ring"][0] + 0.01, ym + 0.5)

# ------------------------------------------------------------------ switch islands
# Each island is a dummy ring around its switch row: an identical dummy directly above and
# below every device of the row, plus a dummy at each row end. All dummies are tied to the
# island's body net (the P+ ring): the branch node, or GND for Men.
S_TOP_IN = Y["s_ring1"] - RW           # inner edge of the island ring top side
S_BOT_IN = Y["s_ring0"] + RW
X_STUBS, GATE_STUBS = [], []           # (x, from_y, net)
devs = {}
for isl in islands:
    k, body = isl["key"], isl["body"]
    names = ["%s_DL" % k] + ([("Men" if k == "MEN" else "%s_%d" % (BR[k][1], i + 1))
                              for i in range(isl["m"])]) + ["%s_DR" % k]
    for i, (nm, ox) in enumerate(zip(names, isl["origins"])):
        # dummy rows: everything to the ring outside
        dt = place("%s_T%d" % (k, i), SW, SL, "top", ox, Y["st"], (body,) * 3)
        db = place("%s_B%d" % (k, i), SW, SL, "bottom", ox, Y["sb"], (body,) * 3)
        for t in "SD":
            vbar(tab(dt, t), dt[t].center().y, S_TOP_IN + 0.01)
            vbar(tab(db, t), S_BOT_IN - 0.01, db[t].center().y)
        g = dt["gates"][-1]
        box("m1", g.left, g.bottom, g.right, S_TOP_IN + 0.01)
        g = db["gates"][0]
        box("m1", g.left, S_BOT_IN - 0.01, g.right, g.top)
        # switch row
        dummy = i in (0, len(names) - 1)
        if dummy:
            nets = (body, body, body)
        elif k == "MEN":
            nets = ("X", "en", "Isum")
        else:
            nets = (body, isl["gate"], "X")
        d = place(nm, SW, SL, "bottom", ox, Y["sw"], nets)
        devs[nm] = d
        if dummy:
            for t in "SD":                                   # join the dummy above
                vbar(tab(d, t), d[t].center().y, dt[t].center().y)
            gate_tie(d, False)
            continue
        g = d["gates"][0]
        GATE_STUBS.append((g.center().x, g.center().y, nets[1]))   # down, over the dummy row
        if k == "MEN":
            X_STUBS.append((tab(d, "S"), d["S"].center().y, "X"))
            X_STUBS.append((tab(d, "D"), d["D"].center().y, "Isum"))
        else:
            vbar(tab(d, "S"), d["S"].center().y, dt["S"].center().y)  # S = body: join dummy above
            X_STUBS.append((tab(d, "D"), d["D"].center().y, "X"))      # up, over the dummy row

# ------------------------------------------------------------------ current-source array
A_TOP_IN = Y["a_ring1"] - RW
A_BOT_IN = Y["a_ring0"] + RW
grid = {}
for c in range(7):
    for row, yrow, gpos in (("b", Y["rb"], "bottom"), ("1", Y["r1"], "bottom"),
                            ("2", Y["r2"], "top"), ("3", Y["r3"], "top"),
                            ("t", Y["rt"], "top")):
        letter = ROWS[row][c - 1] if row in ROWS and 1 <= c <= 5 else None
        if letter:
            src = BR[letter][0]
            idx = sum(1 for (cc, rr), v in grid.items() if v["letter"] == letter) + 1
            nm = "%s_%d" % (src, idx)
            nets = ("GND", "Vb", BR[letter][4])
        else:
            nm = "DA_%s%d" % (row, c)
            nets = ("GND", "GND", "GND")
        d = place(nm, UW, UL, gpos, col_ox[c], yrow, nets)
        d["letter"] = letter
        grid[(c, row)] = d

Y_SH_TOP = Y["bsh"][-1]                     # channel A top shield (GND)
for c in range(7):
    db, d1, d2, d3, dt = (grid[(c, r)] for r in ("b", "1", "2", "3", "t"))
    # dummy rows: straps to the ring outside
    for t in "SD":
        vbar(tab(db, t), A_BOT_IN - 0.01, db[t].center().y)
        vbar(tab(dt, t), dt[t].center().y, A_TOP_IN + 0.01)
    g = db["gates"][0]
    box("m1", g.left, A_BOT_IN - 0.01, g.right, g.top)
    g = dt["gates"][-1]
    box("m1", g.left, g.bottom, g.right, A_TOP_IN + 0.01)
    # GND terminals: row 1 -> dummy below, row 3 -> dummy above, row 2 -> channel A top shield
    for d, ytarget in ((d1, db), (d3, dt), (d2, None)):
        for t in "SD":
            if d["nets"][t] == "GND":
                y_to = Y_SH_TOP if ytarget is None else ytarget[t].center().y
                vbar(tab(d, t), d[t].center().y, y_to)
    if d1["letter"] is None:
        gate_tie(d1, False)
        gate_tie(d2, True)
        gate_tie(d3, True)
    else:
        via12(d1["gates"][0].center().x, d1["gates"][0].center().y)   # Vb contacts
        via12(d2["gates"][-1].center().x, d2["gates"][-1].center().y)
        via12(d3["gates"][-1].center().x, d3["gates"][-1].center().y)
# Vb: M2 lines along the gate contacts of rows 1-3, joined by a riser on the right
yv = [grid[(3, "1")]["gates"][0].center().y, grid[(3, "2")]["gates"][-1].center().y,
      grid[(3, "3")]["gates"][-1].center().y]
x_first = grid[(1, "1")]["gates"][0].center().x
for y in yv:
    box("m2", x_first - 0.2, y - 0.2, VB_X + 0.2, y + 0.2)
vbar(VB_X, yv[0] - 0.2, yv[2] + 0.2, "m2")
VB_PIN_Y = Y["r2"]
box("m2", VB_X - 0.2, VB_PIN_Y - 0.2, CW, VB_PIN_Y + 0.2)

# ------------------------------------------------------------------ branch channel
ARR_A = {n: [] for n in TRACK_ORDER}     # rows 1 and 2 -> channel A
ARR_B = {n: [] for n in CHB_ORDER}       # row 3 -> channel B
for c in range(1, 6):
    for row in ("1", "2", "3"):
        d = grid[(c, row)]
        net = d["nets"]["D"]
        (ARR_B if row == "3" else ARR_A)[net].append((tab(d, "D"), d["D"].center().y))
assert all(ARR_A[n] for n in TRACK_ORDER) and all(ARR_B[n] for n in CHB_ORDER)
assert set(n for n, v in ARR_B.items() if v) == set(CHB_ORDER)
# channel A: lower-row track must be below the middle-row track in each column
for c in range(1, 6):
    a_, b_ = grid[(c, "1")]["nets"]["D"], grid[(c, "2")]["nets"]["D"]
    assert a_ == b_ or TRACK_ORDER.index(a_) < TRACK_ORDER.index(b_), (c, a_, b_)


# Each branch node: island ring -> channel C (M2 riser through the X/Isum channel), along
# channel C to its join riser left of the array, up to channel A (and channel B for the
# top-row branches C and D), and along those channels to the source drains.
for isl in islands[1:]:
    net = isl["body"]
    yc = Y["C"][net]
    x_r = isl["ring"][0] + 0.25                       # riser from the island ring top side
    isl["x_r"] = x_r
    stub(x_r, Y["s_ring1"] - RW / 2, yc, SIG_LAYER)
    xj = JOIN_X[net]
    box(SIG_LAYER, min(x_r, xj) - 0.2, yc - TW / 2, max(x_r, xj) + 0.2, yc + TW / 2)
    ys = [yc, Y["T"][net]] + ([Y["TB"][net]] if net in CHB_ORDER else [])
    for yy in ys:
        via23(xj, yy)
    vbar(xj, ys[0], ys[-1], "m2")
    yt = Y["T"][net]
    for (xx, yy) in ARR_A[net]:
        stub(xx, yy, yt, SIG_LAYER)
    x_hi = max(xx for xx, _ in ARR_A[net])
    box(SIG_LAYER, xj - 0.2, yt - TW / 2, x_hi + 0.2, yt + TW / 2)    # M3 over the ring
    if net in CHB_ORDER:
        yb = Y["TB"][net]
        for (xx, yy) in ARR_B[net]:
            stub(xx, yy, yb, SIG_LAYER)
        x_hiB = max(xx for xx, _ in ARR_B[net])
        box(SIG_LAYER, xj - 0.2, yb - TW / 2, x_hiB + 0.2, yb + TW / 2)

# join risers must not run into an island riser (both M2) inside channel C
for isl in islands[1:]:
    for n, xj in JOIN_X.items():
        if Y["C"][isl["body"]] > Y["C"][n] - 0.5:
            assert abs(isl["x_r"] - xj) >= 0.8, (isl["key"], n, isl["x_r"], xj)

# channel B shields: inside the array, from ring side to ring side
for y in Y["bshB"]:
    box("m1", A_RING_X0, y - TW / 2, A_RING_X1, y + TW / 2)

# channel A GND shields: from left of the join risers, across the array ring left side
# (merging with it), through the array to the ring right side
BSH_X0 = min(JOIN_X.values()) - 0.6
for y in Y["bsh"]:
    box("m1", BSH_X0, y - TW / 2, A_RING_X1, y + TW / 2)

# channel C GND shields: from left of the leftmost riser to the GND spine
CSH_X0 = min([isl["x_r"] for isl in islands[1:]] + list(JOIN_X.values())) - 0.6
for y in Y["csh"]:
    box("m1", CSH_X0, y - TW / 2, GSPINE_X + 0.2, y + TW / 2)

# ------------------------------------------------------------------ X / Isum channel (shielded)
x_X = [x for (x, _, n) in X_STUBS if n == "X"]
x_I = [x for (x, _, n) in X_STUBS if n == "Isum"]
for (x, y, n) in X_STUBS:
    stub(x, y, Y[n], SIG_LAYER)
X_LO, X_HI = min(x_x - 0.5 for x_x in x_X), max(x_x + 0.5 for x_x in x_X)
box(SIG_LAYER, X_LO, Y["X"] - TW / 2, X_HI, Y["X"] + TW / 2)
box(SIG_LAYER, ESC_L - 0.2, Y["Isum"] - TW / 2, max(x_I) + 0.5, Y["Isum"] + TW / 2)
escape(Y["Isum"], SIG_LAYER)
# GND shields t0, t2, t4: from the left end of X / Isum to the GND spine
for i in (0, 2, 4):
    y = Y["sh"][i]
    lo = ESC_L + 0.6 if i >= 2 else X_LO - 0.6
    box("m1", lo, y - TW / 2, GSPINE_X + 0.2, y + TW / 2)
# GND spine (M1): ties the t0/t2/t4 and channel C shields to the array ring bottom side
assert X_HI + 0.2 < GSPINE_X - 0.2 and A_RING_X0 + RW < GSPINE_X < A_RING_X1 - RW
vbar(GSPINE_X, Y["sh"][0] - TW / 2, Y["a_ring0"] + RW)

# ------------------------------------------------------------------ digital channel
# GND shield between the switch islands and the digital tracks, tied to the substrate ring
box("m1", OR_O + OR_W - 0.01, Y["dsh"] - TW / 2, SW_X1, Y["dsh"] + TW / 2)
for (x, y, n) in GATE_STUBS:
    stub(x, y, Y["dig"][n], DIG_LAYER[n])
for n in DIG:
    xs = [x for (x, _, nn) in GATE_STUBS if nn == n]
    yd = Y["dig"][n]
    box(DIG_LAYER[n], ESC_L - 0.2, yd - TW / 2, max(xs) + 0.5, yd + TW / 2)
    escape(yd, DIG_LAYER[n])

# ------------------------------------------------------------------ pins
PIN = 0.6


def pin(name, layer, x1, y1, x2, y2):
    box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


pin("Isum", "m2", 0.0, Y["Isum"] - 0.2, PIN, Y["Isum"] + 0.2)
for n in DIG:
    pin(n, "m2", 0.0, Y["dig"][n] - 0.2, PIN, Y["dig"][n] + 0.2)
pin("Vb", "m2", CW - PIN, VB_PIN_Y - 0.2, CW, VB_PIN_Y + 0.2)
via12(DN_X1 - 1.3, VDD_Y)
box("m2", DN_X1 - 1.3, VDD_Y - 0.25, CW, VDD_Y + 0.25)
pin("VDD", "m2", CW - PIN, VDD_Y - 0.25, CW, VDD_Y + 0.25)
yg = (Y["a_ring0"] + Y["rb"]) / 2
via12(CW - OR_O - OR_W / 2, yg)
pin("GND", "m2", CW - PIN, yg - 0.25, CW, yg + 0.25)
top.shapes(li["m1_lbl"]).insert(pya.DText("GND", pya.DTrans(CW / 2, OR_O + OR_W / 2)))

box("bnd", 0, 0, CW, CH)
top.flatten(-1, True)
# mirror in y so that the current-source array (gate Vb) sits below the switches (gates w[3:0])
top.transform(pya.DTrans(pya.DTrans.M0))
top.transform(pya.DTrans(0, CH))
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
