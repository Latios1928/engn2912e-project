"""
DAC (current-steering weight DAC) layout generator for GF180MCU
(gf180mcuD, variant D: 5LM).

Run inside the iic-osic-tools container:
    klayout -b -r gen_dac.py -rd out=DAC.gds

Circuit (analog/neuron/DAC.sch): 1:2:3:4 weighted current sources (unit W/L = 1/8 um,
gate Vb), each switched by w[k] into the summing node X, which Men (gate en) passes to Isum.

    branch  source (m)   switch (m)    switch gate   branch node (= switch S = switch body)
    A       M2  x1       M1  x1        w[0]          net4
    B       M4  x2       M3  x2        w[1]          net2
    C       M6  x3       M5  x3        w[2]          net3
    D       M8  x4       M7  x4        w[3]          net1
    Men: D = Isum, G = en, S = X, B = GND

Layout (user requirements):
  * Deep N-well: every NMOS sits in an LVPWELL inside one DNWELL (tied to a new VDD pin).
    The switches have body = source in the schematic, so each branch's switches get their
    own LVPWELL island whose P+ guard ring is the body tap (tied to the branch node).
    The current-source array and Men sit in grounded LVPWELLs.
  * Dummy ring: the 10 unit current sources form a 2 x 5 common-centroid array
        upper row:  C D A D C
        lower row:  D B C B D
    surrounded by a full ring of identical dummies (4 x 7 positions, 18 dummies).
    Every centroid is exactly at the array centre horizontally (the long axis); A and B are
    off by half a row vertically, which an odd unit count cannot avoid in two rows.
    Each switch island and Men also have a dummy at both row ends.
  * Sensitive nodes: Vb stays inside the array (M2 lines on the gate contacts, GND straps
    around it). The four branch nodes run to the array with a GND shield track between
    each pair. The digital lines w[3:0] and en run in their own channel below the switch
    row (switch gates are contacted at the bottom), separated from it by a GND shield
    track. X and Isum run above the switch row between GND shield tracks. The branch nodes
    reach the array in their own channel.
  * Neighbouring horizontal tracks alternate between Metal1 and Metal3 in every channel:
    the signals X, Isum and the branch nodes are on Metal3 with the GND shields on Metal1
    between them; the digital tracks alternate M3/M1. (No MIM cap here, so Via2 is fine.)
  * Pins are labelled (Metal2 at the cell edge): left Isum, en, w[0]..w[3]; right Vb, VDD,
    GND; GND also on the Metal1 substrate ring.
"""
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet  # noqa: E402

cells.gf180mcu()
OUT = globals().get("out", "DAC.gds")

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
top = ly.create_cell("DAC")
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
    "C": ("M6", "M5", 3, "w[2]", "net3"),
    "D": ("M8", "M7", 4, "w[3]", "net1"),
}
UPPER = "CDADC"            # common-centroid array (columns 1..5; 0 and 6 are dummies)
LOWER = "DBCBD"
TRACK_ORDER = ["net2", "net1", "net3", "net4"]   # branch tracks bottom -> top (B < D < C < A)
DIG = ["en", "w[0]", "w[1]", "w[2]", "w[3]"]     # digital tracks, top -> bottom
# Horizontal tracks alternate between Metal1 and Metal3 in every channel, so that two
# neighbouring tracks are never on the same layer:
#   branch channel   net2 M3 | shield M1 | net1 M3 | shield M1 | net3 M3 | shield M1 | net4 M3
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
sl, sr, srel_lo, srel_hi = extent(SW, SL, "bottom")
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
A_LPW_X0 = SW_X1 + 2.2                     # array LVPWELL (GND) vs island D (net1): >= 1.4
A_RING_X0 = A_LPW_X0 + 0.4
A_DEV_X0 = A_RING_X0 + RW + 0.8
col_ox = [A_DEV_X0 - ul + i * UPITCH for i in range(7)]
VB_X = A_DEV_X0 + 7 * UPITCH - GAP + 0.6   # Vb riser, right of the dummy column
A_RING_X1 = VB_X + 0.2 + 0.8 + RW
A_LPW_X1 = A_RING_X1 + 0.4
DN_X1 = A_LPW_X1 + 2.5
CW = DN_X1 + 2.7 + OR_W + OR_O

# ------------------------------------------------------------------ y floorplan
# Everything is placed relative to T5, the lowest branch track, then shifted.


def layout_y(T5):
    y = {}
    y["T"] = {n: T5 + 2 * i * TP for i, n in enumerate(TRACK_ORDER)}   # GND shield between
    y["bsh"] = [T5 + (2 * i + 1) * TP for i in range(len(TRACK_ORDER) - 1)]
    # array: row 1 (gate bottom) below the channel, row 2 (gate top) above
    y["r1"] = T5 - TW / 2 - 0.6 - urel_hi_b
    y["rb"] = y["r1"] - (urel_hi_b - urel_lo_b) - ROWGAP          # bottom dummy row
    T8 = T5 + 2 * (len(TRACK_ORDER) - 1) * TP
    y["r2"] = T8 + TW / 2 + 0.6 - urel_lo_t
    y["rt"] = y["r2"] + (urel_hi_t - urel_lo_t) + ROWGAP          # top dummy row
    y["a_ring0"] = y["rb"] + urel_lo_b - 0.6 - RW                  # array ring outer bottom
    y["a_ring1"] = y["rt"] + urel_hi_t + 0.6 + RW                  # array ring outer top
    # switch side: analog channel t0..t4 (shield, X, shield, Isum, shield) below T5
    y["sh"] = [T5 - (5 - i) * TP for i in range(5)]               # t0..t4
    y["X"], y["Isum"] = y["sh"][1], y["sh"][3]
    y["s_ring1"] = y["sh"][0] - TW / 2 - 0.9                       # island ring outer top
    y["sw"] = y["s_ring1"] - RW - 0.6 - srel_hi                    # switch S/D centre line
    y["s_ring0"] = y["sw"] + srel_lo - 0.6 - RW                    # island ring outer bottom
    y["dsh"] = y["s_ring0"] - 0.4 - 0.9                            # digital GND shield
    y["dig"] = {n: y["dsh"] - (i + 1) * TP for i, n in enumerate(DIG)}
    return y


y0 = layout_y(0.0)
DN_Y0 = OR_O + OR_W + 2.7
T5 = DN_Y0 - min(y0["a_ring0"] - 0.4 - 2.5, y0["s_ring0"] - 0.4 - 2.5)
T5 = max(T5, OR_O + OR_W + 0.8 + TW / 2 - min(y0["dig"].values()))
Y = layout_y(T5)
A_LPW_Y1 = Y["a_ring1"] + 0.4
VDD_Y = A_LPW_Y1 + 1.25                     # N+ tap strip (DNWELL tie) centre
DN_Y1 = A_LPW_Y1 + 2.5
CH = DN_Y1 + 2.7 + OR_W + OR_O
assert max(Y["T"].values()) + 1.0 < VDD_Y - 0.25

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
for xs in (A_RING_X0 + 2.0, (A_RING_X0 + A_RING_X1) / 2, A_RING_X1 - 2.0):
    box("m1", xs - 0.5, OR_O + OR_W - 0.01, xs + 0.5, Y["a_ring0"] + 0.01)
men = islands[0]
ym = (Y["s_ring0"] + Y["s_ring1"]) / 2
box("m1", OR_O + OR_W - 0.01, ym - 0.5, men["ring"][0] + 0.01, ym + 0.5)

# ------------------------------------------------------------------ switch islands
S_TOP_IN = Y["s_ring1"] - RW           # inner edge of the island ring top side
S_BOT_IN = Y["s_ring0"] + RW
X_STUBS, GATE_STUBS = [], []           # (x, from_y, net)
devs = {}
for isl in islands:
    k, body = isl["key"], isl["body"]
    names = ["%s_DL" % k] + ([("Men" if k == "MEN" else "%s_%d" % (BR[k][1], i + 1))
                              for i in range(isl["m"])]) + ["%s_DR" % k]
    for i, (nm, ox) in enumerate(zip(names, isl["origins"])):
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
            for t in "SD":                                   # everything to the ring top
                vbar(tab(d, t), d[t].center().y, S_TOP_IN + 0.01)
            gate_tie(d, False)
            continue
        g = d["gates"][0]
        GATE_STUBS.append((g.center().x, g.center().y, nets[1]))
        if k == "MEN":
            X_STUBS.append((tab(d, "S"), d["S"].center().y, "X"))
            X_STUBS.append((tab(d, "D"), d["D"].center().y, "Isum"))
        else:
            vbar(tab(d, "S"), d["S"].center().y, S_TOP_IN + 0.01)   # S = body = ring
            X_STUBS.append((tab(d, "D"), d["D"].center().y, "X"))

# ------------------------------------------------------------------ current-source array
A_TOP_IN = Y["a_ring1"] - RW
A_BOT_IN = Y["a_ring0"] + RW
grid = {}
for c in range(7):
    for row, yrow, gpos in (("b", Y["rb"], "bottom"), ("1", Y["r1"], "bottom"),
                            ("2", Y["r2"], "top"), ("t", Y["rt"], "top")):
        letter = None
        if row == "1" and 1 <= c <= 5:
            letter = LOWER[c - 1]
        if row == "2" and 1 <= c <= 5:
            letter = UPPER[c - 1]
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

VB_LINES = []
for c in range(7):
    db, d1, d2, dt = grid[(c, "b")], grid[(c, "1")], grid[(c, "2")], grid[(c, "t")]
    # dummy rows: straps to the ring outside
    for t in "SD":
        vbar(tab(db, t), A_BOT_IN - 0.01, db[t].center().y)
        vbar(tab(dt, t), dt[t].center().y, A_TOP_IN + 0.01)
    g = db["gates"][0]
    box("m1", g.left, A_BOT_IN - 0.01, g.right, g.top)
    g = dt["gates"][-1]
    box("m1", g.left, g.bottom, g.right, A_TOP_IN + 0.01)
    # rows 1 / 2: GND terminals join the dummy beside them (outwards)
    for d, dout in ((d1, db), (d2, dt)):
        for t in "SD":
            if d["nets"][t] == "GND":
                vbar(tab(d, t), d[t].center().y, dout[t].center().y)
    if d1["letter"] is None:
        gate_tie(d1, False)
        gate_tie(d2, True)
    else:
        via12(d1["gates"][0].center().x, d1["gates"][0].center().y)   # Vb contacts
        via12(d2["gates"][-1].center().x, d2["gates"][-1].center().y)
# Vb: M2 lines along the gate contacts of row 1 and row 2, joined by a riser on the right
yv1 = grid[(3, "1")]["gates"][0].center().y
yv2 = grid[(3, "2")]["gates"][-1].center().y
x_first = grid[(1, "1")]["gates"][0].center().x
box("m2", x_first - 0.2, yv1 - 0.2, VB_X + 0.2, yv1 + 0.2)
box("m2", x_first - 0.2, yv2 - 0.2, VB_X + 0.2, yv2 + 0.2)
vbar(VB_X, yv1 - 0.2, yv2 + 0.2, "m2")
VB_PIN_Y = (Y["T"]["net2"] + Y["T"]["net4"]) / 2
box("m2", VB_X - 0.2, VB_PIN_Y - 0.2, CW, VB_PIN_Y + 0.2)

# ------------------------------------------------------------------ branch channel
ARR_STUBS = {n: [] for n in TRACK_ORDER}
for c in range(1, 6):
    for row in ("1", "2"):
        d = grid[(c, row)]
        net = d["nets"]["D"]
        ARR_STUBS[net].append((tab(d, "D"), d["D"].center().y))
# vertical-constraint check: lower-row track must be below upper-row track in each column
for c in range(1, 6):
    a, b = grid[(c, "1")]["nets"]["D"], grid[(c, "2")]["nets"]["D"]
    assert a == b or TRACK_ORDER.index(a) < TRACK_ORDER.index(b), (c, a, b)

for isl in islands[1:]:
    net = isl["body"]
    yt = Y["T"][net]
    # riser from the island ring top side to the branch track, at the ring's left end
    x_r = isl["ring"][0] + 0.25
    stub(x_r, Y["s_ring1"] - RW / 2, yt, SIG_LAYER)
    ys = ARR_STUBS[net]
    for (xx, yy) in ys:
        stub(xx, yy, yt, SIG_LAYER)
    x_hi = max(xx for xx, _ in ys)
    # M3 track: passes over the array ring (M1) without a jumper
    box(SIG_LAYER, x_r - 0.2, yt - TW / 2, x_hi + 0.2, yt + TW / 2)

# GND shields between the branch tracks: from the first island riser, across the array
# ring left side (merging with it), through the array channel to the ring right side
BSH_X0 = min(isl["ring"][0] for isl in islands[1:]) - 0.6
for y in Y["bsh"]:
    box("m1", BSH_X0, y - TW / 2, A_RING_X1, y + TW / 2)

# ------------------------------------------------------------------ X / Isum channel (shielded)
x_X = [x for (x, _, n) in X_STUBS if n == "X"]
x_I = [x for (x, _, n) in X_STUBS if n == "Isum"]
for (x, y, n) in X_STUBS:
    stub(x, y, Y[n], SIG_LAYER)
X_LO, X_HI = min(x_x - 0.5 for x_x in x_X), max(x_x + 0.5 for x_x in x_X)
box(SIG_LAYER, X_LO, Y["X"] - TW / 2, X_HI, Y["X"] + TW / 2)
box(SIG_LAYER, ESC_L - 0.2, Y["Isum"] - TW / 2, max(x_I) + 0.5, Y["Isum"] + TW / 2)
escape(Y["Isum"], SIG_LAYER)
# GND shields t0, t2, t4: from the left end of X / Isum to the array ring left side (GND)
for i in (0, 2, 4):
    y = Y["sh"][i]
    lo = ESC_L + 0.6 if i >= 2 else X_LO - 0.6
    box("m1", lo, y - TW / 2, A_RING_X0 + RW, y + TW / 2)
    assert Y["a_ring0"] < y - TW / 2 and y + TW / 2 < Y["a_ring1"], "shield misses the array ring"

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
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
