"""
Top-level layout of the analog SNN (analog/snn/snn_analog_inh.sch, the 2-2-1 network with signed
hidden -> output synapses) for GF180MCU (gf180mcuD, variant D).

Run inside the iic-osic-tools container, after the block layouts exist:
    klayout -b -r gen_snn.py -rd out=SNN.gds

Blocks (instances of the existing cells, not copies):
    neuron_sized.gds  xneu0..4        DPI.gds      xdpi0..4 (excitatory, minimum size, as DPI.sym)
    DAC_binary.gds    xdac0_0 .. xdac3_1 (6)       DAC_signed.gds  xdac4_0, xdac4_1
    (the schematic's DAC.sym is the 1:2:3:4 DAC; the layout uses the binary 1:2:4:8 DAC, also
    inside DAC_signed. -rd dac=DAC selects the 1:2:3:4 DAC.gds for the six plain DACs.)
    DPI_inh.gds       xdpi5 (inhibitory synapse of the output neuron)
    bias_cell.gds     xbias (current-mode bias generator, analog/neuron/bias_cell.sch): makes Vb, Vthr,
                      VT_dpi, VT_inh and the seven neuron biases from one reference current Iref

Floorplan: one row per neuron, bottom to top u0 (input 0), u1 (input 1), u2, u3 (hidden),
u4 (output). Each row, left to right:

    col L | DAC(s), mirrored | channel A | DPI(s) | channel B | neuron | channel C
    Vb    | pins Isum/en/w   | w, en, s, | Isum,  | VDD, VSS, | biases | VDD, VSS,
    VDD   | face channel A   | Isum (row | Vthr,  | VMEM,     | left,  | spike
    VSS   |                  | local),   | VT     | neuron    | supply |
          |                  | Vthr, VT  | left   | biases    | right  |

  * Routing uses Metal2 (horizontal stubs from a block pin to its track) and Metal3
    (vertical tracks in the channels); nothing is routed over a block. The spike lines are
    the exception: their vertical tracks rotate through Metal1, Metal5 and Metal3 and their
    bottom-channel taps alternate Metal4 / Metal2, so that no two spike lines run side by
    side on the same layer. Tracks are ordered
    so that no two Metal2 stubs of different nets overlap; the generator checks the spacing
    of every top-level Metal2/Metal3 shape it draws.
  * A bottom channel holds the VDD and VSS Metal2 buses that join the supply tracks of all
    three columns, and the four spike taps: spike[0..3] run down channel C and back up
    channel A to the DAC enables of the next layer.
  * The output neuron's DPI_inh output (Iout) joins VMEM_4 through the gap between DPI4 and
    DPI_inh.
  * The bias cell sits above the top row. Its bottom-edge outputs drop into a routing channel
    between the cell and the top row; its top-edge outputs go over it and down a corridor on its
    right. In that channel each bias joins the top end of its existing track (column L, channel A
    or channel B), so the biases are distributed from the top; the tracks no longer reach the
    bottom edge. The cell's VDD / VSS come from the channel C supply tracks, Iref from a column L
    track that runs up from the Iref pin.
  * Pins: all on the bottom edge, labelled, Metal3 except spike[i] (on its track's layer:
    spike[0], spike[3] Metal1, spike[1], spike[4] Metal5, spike[2] Metal3): VDD, VSS, Vb, w[31:0], pulse[1:0], s[1:0],
    Iref (bias cell reference current, 100 nA into the pin), VT (neuron threshold voltage), spike[4:0].
    The blocks' GND (DAC, DAC_signed, DPI_inh) and VSS are the same net, VSS.
"""
import json
import os
import pya

DAC = globals().get("dac", "DAC_binary")    # cell used for the six plain DACs
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
OUT = globals().get("out", os.path.join(HERE, "SNN.gds"))

ly = pya.Layout()
ly.dbu = 0.001
top = ly.create_cell("SNN")
L = {"m1": (34, 0), "via1": (35, 0), "m2": (36, 0), "via2": (38, 0), "m3": (42, 0),
     "via3": (40, 0), "m4": (46, 0), "via4": (41, 0), "m5": (81, 0),
     "bnd": (0, 0), "m1_lbl": (34, 10), "m3_lbl": (42, 10), "m5_lbl": (81, 10)}
li = {k: ly.layer(*v) for k, v in L.items()}


# ------------------------------------------------------------------ blocks
# All block GDS files are read into this one layout. A cell that already exists under the
# same name is reused (SkipNewCell), so DAC_signed's DAC subcell is the same cell as the six
# plain DACs, and LVS sees one DAC circuit.
OPT = pya.LoadLayoutOptions()
OPT.cell_conflict_resolution = pya.LoadLayoutOptions.SkipNewCell
for n in (DAC, "DPI_sized", "DPI", "neuron_sized", "DAC_signed", "DPI_inh", "bias_cell"):
    ly.read(os.path.join(HERE, n + ".gds"), OPT)


def load(name):
    """A block cell already in the layout; returns (cell, size, pins {name: [access...]})."""
    c = ly.cell(name)
    assert c is not None, name
    pins = {}
    for p in json.load(open(os.path.join(HERE, name + "_pins.json")))["pins"]:
        if p["layer"] == "Metal2":
            pins.setdefault(p["name"], []).extend(p["access"])
    return c, c.dbbox(), pins


BLK = {n: load(n) for n in ("neuron_sized", "DPI", DAC, "DAC_signed", "DPI_inh")}


class Inst:
    """A placed block. mirror=True mirrors it about its left edge (x -> x0 - x)."""

    def __init__(self, name, kind, x, y, mirror=False):
        self.name, self.kind, self.x, self.y, self.mirror = name, kind, x, y, mirror
        c, bb, self.pins = BLK[kind]
        self.w, self.h = bb.width(), bb.height()
        t = pya.DTrans(x, y) * (pya.DTrans(pya.DTrans.M90) if mirror else pya.DTrans())
        top.insert(pya.DCellInstArray(c.cell_index(), t))

    def pin(self, name):
        """(x at the cell edge, y centre) of a Metal2 edge pin."""
        acc = [a for a in self.pins[name] if a["side"] in ("left", "right")]
        assert len(acc) == 1, (self.name, name, acc)
        a = acc[0]
        xe = a["x1"] if a["side"] == "left" else a["x2"]
        x = self.x - xe if self.mirror else self.x + xe
        return x, self.y + (a["y1"] + a["y2"]) / 2

    def ring_x(self):
        """x of the centre of the block's right guard-ring side (unmirrored blocks only)."""
        assert not self.mirror
        return self.x + self.w - 0.55


# ------------------------------------------------------------------ drawing with checks
SHAPES = {"m1": [], "m2": [], "m3": [], "m4": [], "m5": []}   # (DBox, net)
SPACE = {"m1": 0.23, "m2": 0.3, "m3": 0.3, "m4": 0.3, "m5": 0.46}
PAD = {"m1": 0.4, "m2": 0.4, "m3": 0.4, "m4": 0.4, "m5": 0.46}
VIA = {1: "via1", 2: "via2", 3: "via3", 4: "via4"}


def draw(layer, b, net):
    if layer in SHAPES:
        for (o, n) in SHAPES[layer]:
            if n != net and o.enlarged(SPACE[layer] - 0.001, SPACE[layer] - 0.001).overlaps(b):
                raise AssertionError("%s short/spacing: %s %s vs %s %s" % (layer, net, b, n, o))
        SHAPES[layer].append((b, net))
    top.shapes(li[layer]).insert(b)


def rect(layer, x1, y1, x2, y2, net):
    draw(layer, pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)), net)


def via23(x, y, net):
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2, net)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2, net)
    top.shapes(li["via2"]).insert(pya.DBox(x - 0.13, y - 0.13, x + 0.13, y + 0.13))


def via12(x, y, net):
    stack(x, y, "m1", "m2", net)


def stack(x, y, la, lb, net):
    """Stacked vias between metal layers la and lb (e.g. "m1", "m5"), pads on every metal."""
    a, b = sorted((int(la[1]), int(lb[1])))
    for m in range(a, b + 1):
        h = PAD["m%d" % m] / 2
        rect("m%d" % m, x - h, y - h, x + h, y + h, net)
    for v in range(a, b):
        top.shapes(li[VIA[v]]).insert(pya.DBox(x - 0.13, y - 0.13, x + 0.13, y + 0.13))


# ------------------------------------------------------------------ tracks
class Track:
    def __init__(self, net, x, w=0.4, y_lo=None, layer="m3"):
        self.net, self.x, self.w, self.layer = net, x, w, layer
        self.y_lo, self.y_hi = y_lo, None      # y_lo None -> reaches the bottom edge (pin)
        self.y_min = None

    def need(self, y):
        self.y_hi = y if self.y_hi is None else max(self.y_hi, y)
        self.y_min = y if self.y_min is None else min(self.y_min, y)
        if self.y_lo is not None and self.y_lo is not True:
            self.y_lo = min(self.y_lo, y)


TRACKS = []


def column(x0, specs):
    """Lay tracks left to right from x0; specs = [(net, width[, layer])]. Returns ({net: Track}, x_end)."""
    out = {}
    x = x0
    prev_w = None
    for spec in specs:
        net, w = spec[:2]
        layer = spec[2] if len(spec) > 2 else "m3"
        if prev_w is not None:
            x += prev_w / 2 + max(0.4, SPACE["m3"] + 0.1) + w / 2
        else:
            x += w / 2
        t = Track(net, x, w, layer=layer)
        out[net] = t
        TRACKS.append(t)
        prev_w = w
    return out, x + prev_w / 2


def stub(x_from, x_to, y, net):
    """Metal2 stub from a block pin edge (x_from) to x_to, 0.3 um into the pin."""
    x_in = x_from - 0.3 if x_to > x_from else x_from + 0.3
    rect("m2", x_in, y - 0.2, x_to, y + 0.2, net)


def tap(track, y, x_from):
    """Metal2 stub at y from x_from (a block pin edge) to the track, via(s) onto the track."""
    stub(x_from, track.x, y, track.net)
    stack(track.x, y, "m2", track.layer, track.net)
    track.need(y)


LOCAL = {}                                  # (track x, net) -> [y]: row-local track segments


def ltap(track, y, x_from, net):
    """tap() on a row-local track (LA, LB, LC, LV): its segment is drawn per net later."""
    stub(x_from, track.x, y, net)
    via23(track.x, y, net)
    LOCAL.setdefault((track.x, net), []).append(y)


SUP = 1.0                                   # supply track width
EDGE = 1.0                                  # clearance between a block edge and a channel
# Spike lines: neighbouring spike tracks never share a layer. The vertical tracks rotate
# through Metal1 -> Metal5 -> Metal3 (the rotation starts on Metal1 so that the spike tracks
# next to the Metal3 tracks around them are not on Metal3 either); the bottom-channel taps
# that join channels C and A alternate Metal4 / Metal2 (they cross the Metal1/3/5 verticals).
SPIKE_W = {"m1": 0.4, "m3": 0.4, "m5": 0.5}
SPIKE_LAYER = ["m1", "m5", "m3", "m1", "m5"]     # spike[0..4], channel C (and A for 0..3)
SPIKE_TAP_LAYER = ["m4", "m2", "m4", "m2"]       # spike[0..3] taps, bottom to top

# ------------------------------------------------------------------ x floorplan
colL, x = column(EDGE, [("Iref", 0.4), ("Vb", 0.4), ("VDD", SUP), ("VSS", SUP)])
XD0 = x + EDGE
XD1 = XD0 + BLK["DAC_signed"][1].width()    # DAC column: original left edges (pins) at XD1

CH_A = ([("w[%d]" % i, 0.4) for i in range(32)] + [("pulse[0]", 0.4), ("pulse[1]", 0.4)]
        + [("spike[%d]" % i, SPIKE_W[SPIKE_LAYER[i]], SPIKE_LAYER[i]) for i in range(4)]
        + [("s[0]", 0.4), ("s[1]", 0.4)]
        + [("LA", 0.4), ("LB", 0.4), ("LC", 0.4)]
        + [("Vthr", 0.4), ("VT_dpi", 0.4), ("VT_inh", 0.4)])
chA, x = column(XD1 + EDGE, CH_A)
XP0 = x + EDGE                              # DPI column
XP1 = XP0 + max(BLK["DPI"][1].width(), BLK["DPI_inh"][1].width())
BIAS = ["VNA", "Vlk", "VK", "VIp", "VKup", "VKdn", "Vamp_bias", "VT"]
chB, x = column(XP1 + EDGE, [("VDD", SUP), ("VSS", SUP), ("LV", 0.4)] + [(b, 0.4) for b in BIAS])
XN0 = x + EDGE                              # neuron column
XN1 = XN0 + BLK["neuron_sized"][1].width()
chC, x = column(XN1 + EDGE, [("VDD", SUP), ("VSS", SUP)]
                + [("spike[%d]" % i, SPIKE_W[SPIKE_LAYER[i]], SPIKE_LAYER[i]) for i in range(5)])
CW = x + EDGE

# local tracks only exist inside a row: they start where they are first needed
for t in (chA["LA"], chA["LB"], chA["LC"], chB["LV"]):
    t.y_lo = True
for i in range(4):
    chA["spike[%d]" % i].y_lo = True             # starts at its bottom-channel tap

# ------------------------------------------------------------------ y floorplan
Y_VSS = (1.0, 2.6)                          # bottom channel Metal2 buses
Y_VDD = (3.2, 4.8)
Y_SPK = [5.6 + 0.8 * i for i in range(4)]   # spike[0..3] taps
ROW_GAP = 2.0
DAC_H = max(BLK[DAC][1].height(), BLK["DAC_signed"][1].height())
NEU_H = BLK["neuron_sized"][1].height()
DPI_H, INH_H = BLK["DPI"][1].height(), BLK["DPI_inh"][1].height()
INH_GAP = 2.0                               # DPI4 -> DPI_inh gap (Iout route)
DAC_GAP = 0.2                               # between stacked DACs: their P+ rings' implant (PP.2)

rows = []
y = Y_SPK[-1] + 0.2 + ROW_GAP
for u, ndac in enumerate([1, 1, 2, 2, 2]):
    h = max(NEU_H, ndac * DAC_H + (ndac - 1) * DAC_GAP, DPI_H + (INH_GAP + INH_H if u == 4 else 0))
    rows.append((y, h))
    y += h + ROW_GAP
CH = y - ROW_GAP + EDGE

# ------------------------------------------------------------------ place blocks
W_OF = {"xdac0_0": 0, "xdac1_0": 1, "xdac2_0": 2, "xdac2_1": 3, "xdac3_0": 4, "xdac3_1": 5,
        "xdac4_0": 6, "xdac4_1": 7}
EN_OF = {"xdac0_0": "pulse[0]", "xdac1_0": "pulse[1]", "xdac2_0": "spike[0]",
         "xdac2_1": "spike[1]", "xdac3_0": "spike[0]", "xdac3_1": "spike[1]",
         "xdac4_0": "spike[2]", "xdac4_1": "spike[3]"}
DACS_OF = {0: ["xdac0_0"], 1: ["xdac1_0"], 2: ["xdac2_0", "xdac2_1"],
           3: ["xdac3_0", "xdac3_1"], 4: ["xdac4_0", "xdac4_1"]}
inst = {}
for u, (y0, h) in enumerate(rows):
    for k, dn in enumerate(DACS_OF[u]):
        inst[dn] = Inst(dn, "DAC_signed" if u == 4 else DAC, XD1, y0 + k * (DAC_H + DAC_GAP),
                        mirror=True)
    inst["xdpi%d" % u] = Inst("xdpi%d" % u, "DPI", XP0, y0)
    inst["xneu%d" % u] = Inst("xneu%d" % u, "neuron_sized", XN0, y0)
inst["xdpi5"] = Inst("xdpi5", "DPI_inh", XP0, rows[4][0] + DPI_H + INH_GAP)

# ------------------------------------------------------------------ wiring
# DACs: digital and Isum pins (right, facing channel A), supplies / Vb (left, column L)
for dn, d in ((n, inst[n]) for n in W_OF):
    m = W_OF[dn]
    for b in range(4):
        x0, yy = d.pin("w[%d]" % b)
        tap(chA["w[%d]" % (4 * m + b)], yy, x0)
    x0, yy = d.pin("en")
    tap(chA[EN_OF[dn]], yy, x0)
    if d.kind == DAC:
        x0, yy = d.pin("Isum")
        ltap(chA["LA"], yy, x0, "Isum_%d" % int(dn[4]))
    else:
        x0, yy = d.pin("Isum_e")
        ltap(chA["LA"], yy, x0, "Isum_4")
        x0, yy = d.pin("Isum_i")
        ltap(chA["LB"], yy, x0, "Isum_5")
        x0, yy = d.pin("s")
        tap(chA["s[%d]" % int(dn[-1])], yy, x0)
    for pn, tn in (("Vb", "Vb"), ("VDD", "VDD"), ("GND", "VSS")):
        x0, yy = d.pin(pn)
        tap(colL[tn], yy, x0)

# DPIs: Isum (local), Vthr / VT (global) on the left; Isyn (VMEM, local) / VDD / VSS on the right
for u in range(5):
    p = inst["xdpi%d" % u]
    x0, yy = p.pin("Isum")
    ltap(chA["LA"], yy, x0, "Isum_%d" % u)
    x0, yy = p.pin("Vthr")
    tap(chA["Vthr"], yy, x0)
    x0, yy = p.pin("VT")
    tap(chA["VT_dpi"], yy, x0)
    x0, yy = p.pin("Isyn")
    ltap(chB["LV"], yy, x0, "VMEM_%d" % u)
    x0, yy = p.pin("VDD")
    tap(chB["VDD"], yy, x0)
    yv = p.y + 3.0                                  # VSS: via1 on the right ring side
    via12(p.ring_x(), yv, "VSS")
    rect("m2", p.ring_x(), yv - 0.2, chB["VSS"].x, yv + 0.2, "VSS")
    via23(chB["VSS"].x, yv, "VSS")
    chB["VSS"].need(yv)
inh = inst["xdpi5"]
x0, yy = inh.pin("Isum")
ltap(chA["LB"], yy, x0, "Isum_5")
x0, yy = inh.pin("Vthr")
tap(chA["Vthr"], yy, x0)
x0, yy = inh.pin("VT")
tap(chA["VT_inh"], yy, x0)
x0, yy = inh.pin("VDD")
tap(chB["VDD"], yy, x0)
yv = inh.y + 10.0
via12(inh.ring_x(), yv, "VSS")
rect("m2", inh.ring_x(), yv - 0.2, chB["VSS"].x, yv + 0.2, "VSS")
via23(chB["VSS"].x, yv, "VSS")
chB["VSS"].need(yv)
# Iout -> LC -> down to the DPI4 / DPI_inh gap -> across to LV (VMEM_4)
x0, yy = inh.pin("Iout")
ltap(chA["LC"], yy, x0, "VMEM_4")
yg = inh.y - INH_GAP / 2
via23(chA["LC"].x, yg, "VMEM_4")
LOCAL[(chA["LC"].x, "VMEM_4")].append(yg)
rect("m2", chA["LC"].x, yg - 0.2, chB["LV"].x, yg + 0.2, "VMEM_4")
via23(chB["LV"].x, yg, "VMEM_4")
LOCAL[(chB["LV"].x, "VMEM_4")].append(yg)

# neurons: biases / VMEM on the left (channel B), VDD / VSS / spike on the right (channel C)
for u in range(5):
    n = inst["xneu%d" % u]
    for b in BIAS:
        x0, yy = n.pin(b)
        tap(chB[b], yy, x0)
    x0, yy = n.pin("VMEM")
    ltap(chB["LV"], yy, x0, "VMEM_%d" % u)
    x0, yy = n.pin("VDD")
    tap(chC["VDD"], yy, x0)
    x0, yy = n.pin("VSS")
    tap(chC["VSS"], yy, x0)
    x0, yy = n.pin("spike")
    tap(chC["spike[%d]" % u], yy, x0)

# local track segments
for (tx, net), ys in LOCAL.items():
    rect("m3", tx - 0.2, min(ys) - 0.2, tx + 0.2, max(ys) + 0.2, net)

# spike[0..3]: channel C -> bottom channel tap -> channel A spike_en track (the DAC enables)
for i in range(4):
    ys = Y_SPK[i]
    tc, ta = chC["spike[%d]" % i], chA["spike[%d]" % i]
    hl = SPIKE_TAP_LAYER[i]
    stack(tc.x, ys, tc.layer, hl, tc.net)
    rect(hl, ta.x, ys - 0.2, tc.x, ys + 0.2, tc.net)
    stack(ta.x, ys, ta.layer, hl, tc.net)
    ta.y_lo = ys

# bottom channel supply buses (Metal2) joining columns L, B and C
X_BUS0, X_BUS1 = colL["VDD"].x - SUP / 2, chC["VSS"].x + SUP / 2
rect("m2", X_BUS0, Y_VSS[0], X_BUS1, Y_VSS[1], "VSS")
rect("m2", X_BUS0, Y_VDD[0], X_BUS1, Y_VDD[1], "VDD")


def via23_row(x, y1, y2, w, net):
    """Via2 array where a wide supply track lands on a bus."""
    n = max(1, int((w - 0.26) / 0.52) + 1)
    for i in range(n):
        cx = x - (n - 1) * 0.26 + i * 0.52
        for cy in (y1 + 0.4, y2 - 0.4):
            top.shapes(li["via2"]).insert(pya.DBox(cx - 0.13, cy - 0.13, cx + 0.13, cy + 0.13))


for net, ybus in (("VSS", Y_VSS), ("VDD", Y_VDD)):
    for col in (colL, chB, chC):
        t = col[net]
        via23_row(t.x, ybus[0], ybus[1], t.w, net)
        if col is not colL:
            t.y_lo = ybus[0]                        # B / C supply tracks stop on their bus

# ------------------------------------------------------------------ bias cell above the top row
TP = 0.8                                            # routing track pitch
BIAS_TRACK = {"Vb": colL["Vb"], "Vthr": chA["Vthr"], "VT_dpi": chA["VT_dpi"], "VT_inh": chA["VT_inh"],
              **{b: chB[b] for b in ("VNA", "Vlk", "VK", "VIp", "VKup", "VKdn", "Vamp_bias")}}
BP = {}
for p_ in json.load(open(os.path.join(HERE, "bias_cell_pins.json")))["pins"]:
    for a in p_["access"]:
        BP.setdefault(p_["name"], []).append(a)
bcell = ly.cell("bias_cell")
BW, BH = bcell.dbbox().width(), bcell.dbbox().height()
Y_TOP = CH - EDGE                                   # top of the top row
n_bot = [b for b in BIAS_TRACK if BP[b][0]["side"] == "bottom"]
n_top = [b for b in BIAS_TRACK if BP[b][0]["side"] == "top"]
Y_C1 = Y_TOP + EDGE + 0.8                           # first routing track above the top row
Y_H = {}
XC0 = XD0                                           # bias cell lower-left
YC0 = Y_C1 + len(BIAS_TRACK) * TP + 1.2
X_COR = XC0 + BW + EDGE + 0.6                       # corridor (M3 verticals) right of the cell
Y_C2 = YC0 + BH + EDGE                              # routing tracks above the cell
top.insert(pya.DCellInstArray(bcell.cell_index(), pya.DTrans(XC0, YC0)))


def bpin(name, i=0):
    a = BP[name][i]
    return XC0 + (a["x1"] + a["x2"]) / 2, YC0 + (a["y1"] + a["y2"]) / 2, a


# channel assignment: biases leaving the cell's bottom edge on the lower tracks (sorted by their
# target x, so the cell-pin drops and the track extensions do not meet), then those that come
# round the corridor
order = sorted(n_bot, key=lambda b: BIAS_TRACK[b].x) + sorted(n_top, key=lambda b: BIAS_TRACK[b].x)
for i, b in enumerate(order):
    Y_H[b] = Y_C1 + i * TP
for j, b in enumerate(sorted(n_top, key=lambda b: bpin(b)[0])):
    x0, y0, a = bpin(b)
    yc2 = Y_C2 + j * TP
    xcor = X_COR + j * TP
    rect("m3", x0 - 0.2, YC0 + a["y1"], x0 + 0.2, yc2 + 0.2, b)        # up from the cell's top edge
    via23(x0, yc2, b)
    rect("m2", x0 - 0.2, yc2 - 0.2, xcor + 0.2, yc2 + 0.2, b)        # over the cell to the corridor
    via23(xcor, yc2, b)
    rect("m3", xcor - 0.2, Y_H[b] - 0.2, xcor + 0.2, yc2 + 0.2, b)   # down the corridor
    via23(xcor, Y_H[b], b)
    BP[b + "_src"] = xcor
for b in n_bot:
    x0, y0, a = bpin(b)
    rect("m3", x0 - 0.2, Y_H[b] - 0.2, x0 + 0.2, YC0 + a["y2"], b)  # down from the cell's bottom edge
    via23(x0, Y_H[b], b)
    BP[b + "_src"] = x0
for b in BIAS_TRACK:
    t = BIAS_TRACK[b]
    xs = BP[b + "_src"]
    rect("m2", min(xs, t.x) - 0.2, Y_H[b] - 0.2, max(xs, t.x) + 0.2, Y_H[b] + 0.2, b)
    via23(t.x, Y_H[b], b)
    t.y_lo = t.y_min                                # no bottom pin any more: from the lowest tap ...
    t.y_hi = Y_H[b]                                 # ... up to the channel
# supplies of the cell: VDD (two pins) and VSS on its right edge -> channel C supply tracks
for name, t in (("VDD", chC["VDD"]), ("VSS", chC["VSS"])):
    for i in range(len(BP[name])):
        if BP[name][i]["side"] != "right":
            continue
        x0, y0, a = bpin(name, i)
        rect("m2", XC0 + a["x1"], y0 - 0.2, t.x + t.w / 2, y0 + 0.2, name)
        via23(t.x, y0, name)
        t.y_hi = max(t.y_hi, y0)
# Iref: column L track from the bottom pin up to the cell's Iref pin (left edge)
x0, y0, a = bpin("Iref")
t = colL["Iref"]
rect("m2", t.x - 0.2, y0 - 0.2, XC0 + a["x2"], y0 + 0.2, "Iref")
via23(t.x, y0, "Iref")
t.need(y0)
CH = Y_C2 + len(n_top) * TP + EDGE

# draw the global tracks
for t in TRACKS:
    if t.net is None or t.y_hi is None:
        continue
    lo = 0.0 if t.y_lo is None else t.y_lo
    if lo is True:
        continue
    rect(t.layer, t.x - t.w / 2, lo - 0.25 if lo > 0 else 0.0, t.x + t.w / 2, t.y_hi + 0.25, t.net)

# ------------------------------------------------------------------ pins (bottom edge; spike on its track's layer)
PINS = (["VDD", "VSS", "Iref"] + ["w[%d]" % i for i in range(32)] + ["pulse[0]", "pulse[1]", "s[0]", "s[1]"]
        + ["VT"] + ["spike[%d]" % i for i in range(5)])
for pn in PINS:
    t = (colL[pn] if pn in ("VDD", "VSS", "Iref") else chC[pn] if pn.startswith("spike")
         else chA.get(pn) or chB.get(pn))
    assert t.y_lo is None and t.y_hi is not None, pn
    top.shapes(li[t.layer + "_lbl"]).insert(pya.DText(pn, pya.DTrans(t.x, 0.3)))

top.shapes(li["bnd"]).insert(pya.DBox(0, 0, CW, CH))
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
