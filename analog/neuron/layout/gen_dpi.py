"""
DPI synapse layout generator for GF180MCU (gf180mcuD, variant D: 5LM, MIM-B M4-M5).

Run inside the iic-osic-tools container:
    klayout -b -r gen_dpi.py -rd out=DPI.gds

Circuit (analog/neuron/DPI.sch):
    M1 nfet_03v3 D=VDD  G=Vthr S=Isum B=Isum   W=0.22 L=0.28
    M2 nfet_03v3 D=net1 G=net1 S=Isum B=Isum   W=0.22 L=0.28
    M3 pfet_03v3 D=net1 G=VT   S=VDD  B=VDD    W=0.22 L=0.28
    M4 pfet_03v3 D=Isyn G=net1 S=VDD  B=VDD    W=0.22 L=0.28
    C4 VDD-net1 1 pF  -> MIM cap 22.36 x 22.36 um (2 fF/um^2), bottom plate VDD, top plate net1

Floorplan:
  * One deep N-well (DNWELL, tied to VDD) holds everything. The NFETs sit in an
    LVPWELL island tied to Isum (the schematic ties their bodies to their sources).
    The PFETs sit directly in DNWELL (body = VDD).
  * A P+ guard ring (VSS / substrate) surrounds the DNWELL (rule DN.3).
  * The MIM cap covers the transistors. Its plates are reached only from Metal5
    (rule MIMTM.10), via two via stacks on the right side of the cell.
  * Routing under the cap uses only M1 (rails, tracks) and M2 (stubs, pins): the LVS
    deck ignores Via2/Via3 under FuseTop. Via2..Via4 appear only in two stacks outside it.
  * Pins: Metal2 at the cell edges, VSS on the Metal1 guard ring.
"""
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet, draw_pfet  # noqa: E402

cells.gf180mcu()  # registers the PCell library "gf180mcu"

OUT = globals().get("out", "DPI.gds")

# ---------------------------------------------------------------- layers
L = {
    "dnwell": (12, 0), "nwell": (21, 0), "comp": (22, 0), "poly": (30, 0),
    "pplus": (31, 0), "nplus": (32, 0), "cont": (33, 0), "m1": (34, 0),
    "via1": (35, 0), "m2": (36, 0), "via2": (38, 0), "m3": (42, 0),
    "via3": (40, 0), "m4": (46, 0), "via4": (41, 0), "m5": (81, 0),
    "lvpwell": (204, 0), "bnd": (0, 0),
    "m1_lbl": (34, 10), "m2_lbl": (36, 10), "m3_lbl": (42, 10), "m5_lbl": (81, 10),
}

ly = pya.Layout()
ly.dbu = 0.001
top = ly.create_cell("DPI")
li = {k: ly.layer(*v) for k, v in L.items()}


def box(layer, x1, y1, x2, y2):
    top.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def sq(layer, cx, cy, size):
    h = size / 2
    box(layer, cx - h, cy - h, cx + h, cy + h)


# --------------------------------------------------------------- via helpers
VIA = 0.26
PAD = {"m1": 0.40, "m2": 0.40, "m3": 0.40, "m4": 0.40, "m5": 0.46}


def via_stack(cx, cy, lo, hi):
    """Stacked vias from metal `lo` to metal `hi` (1..5) centred at (cx, cy)."""
    for m in range(lo, hi + 1):
        sq("m%d" % m, cx, cy, PAD["m%d" % m])
    for v in range(lo, hi):
        sq("via%d" % v, cx, cy, VIA)


def contacts_row(x1, x2, cy, pitch=0.5):
    """Row of 0.22 um contacts between x1 and x2 at height cy."""
    n = int((x2 - x1 - 0.22) / pitch) + 1
    x0 = (x1 + x2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        sq("cont", x0 + i * pitch, cy, 0.22)


def contacts_col(x, y1, y2, pitch=0.5):
    n = int((y2 - y1 - 0.22) / pitch) + 1
    y0 = (y1 + y2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        sq("cont", x, y0 + i * pitch, 0.22)


# ----------------------------------------------------------- device helpers
W, LG, LD = 0.22, 0.28, 0.80   # LD: S/D diffusion length (spreads the pads apart)


def make_fet(kind, gate_pos):
    fn = draw_nfet if kind == "n" else draw_pfet
    c = fn(ly, l_gate=LG, w_gate=W, inter_sd_l=LD, nf=1, con_bet_fin=0,
           gate_con_pos=gate_pos, bulk="None")
    c.flatten(True)
    if kind == "p":                       # PFETs live in DNWELL: no NWELL of their own
        c.shapes(li["nwell"]).clear()
    # the PDK generator draws some M1 pad edges off the 5 nm grid (e.g. -0.081, 0.301):
    # snap every layer of the device to 5 nm
    for k in li:
        r = pya.Region(c.shapes(li[k]))
        if r.is_empty():
            continue
        c.shapes(li[k]).clear()
        c.shapes(li[k]).insert(r.snapped(5, 5))
    # find the terminal pads on M1: S/D share a y, the gate pad sits above/below
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    sd = sorted([p for p in pads if p.bottom < 0.1 < p.top], key=lambda b: b.center().x)
    g = [p for p in pads if not (p.bottom < 0.1 < p.top)]
    assert len(sd) == 2 and len(g) == 1, (kind, pads)
    return c, {"S": sd[0], "D": sd[1], "G": g[0]}


def place(cell_pads, x, y):
    c, pads = cell_pads
    top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans(x, y)))
    return {k: v.moved(x, y) for k, v in pads.items()}


nfet_cell = make_fet("n", "top")
pfet_cell = make_fet("p", "bottom")

# ------------------------------------------------------------- floorplan
CW, CH = 28.0, 26.0                        # cell size
RING_O, RING_W = 0.3, 0.5                  # guard ring outer offset and COMP width
RI = RING_O + RING_W                       # ring inner offset (0.8)
DN = (RI + 2.7, RI + 2.7, 24.6, CH - RI - 2.7)   # DNWELL box

# --- guard ring (P+ to substrate, VSS)
for (x1, y1, x2, y2) in [
    (RING_O, RING_O, CW - RING_O, RI),                 # bottom
    (RING_O, CH - RI, CW - RING_O, CH - RING_O),       # top
    (RING_O, RING_O, RI, CH - RING_O),                 # left
    (CW - RI, RING_O, CW - RING_O, CH - RING_O),       # right
]:
    box("comp", x1, y1, x2, y2)
    box("m1", x1, y1, x2, y2)
box("pplus", RING_O - 0.16, RING_O - 0.16, CW - RING_O + 0.16, CH - RING_O + 0.16)
# pplus is a frame: cut the inside back out by drawing it as 4 strips instead
top.shapes(li["pplus"]).clear()
for (x1, y1, x2, y2) in [
    (RING_O - 0.16, RING_O - 0.16, CW - RING_O + 0.16, RI + 0.16),
    (RING_O - 0.16, CH - RI - 0.16, CW - RING_O + 0.16, CH - RING_O + 0.16),
    (RING_O - 0.16, RING_O - 0.16, RI + 0.16, CH - RING_O + 0.16),
    (CW - RI - 0.16, RING_O - 0.16, CW - RING_O + 0.16, CH - RING_O + 0.16),
]:
    box("pplus", x1, y1, x2, y2)
rc = RING_O + RING_W / 2
contacts_row(RI + 0.2, CW - RI - 0.2, rc)
contacts_row(RI + 0.2, CW - RI - 0.2, CH - rc)
contacts_col(rc, RING_O, CH - RING_O)
contacts_col(CW - rc, RING_O, CH - RING_O)

# --- deep N-well
box("dnwell", *DN)

# --- LVPWELL island (NFET body = Isum) with its P+ tap
LPW = (DN[0] + 2.5, DN[1] + 2.5, DN[0] + 9.0, DN[1] + 7.0)
box("lvpwell", *LPW)
ptap = (LPW[0] + 0.8, LPW[1] + 0.6, LPW[2] - 0.8, LPW[1] + 1.1)
box("comp", *ptap)
box("pplus", ptap[0] - 0.16, ptap[1] - 0.16, ptap[2] + 0.16, ptap[3] + 0.16)
box("m1", *ptap)
contacts_row(ptap[0], ptap[2], (ptap[1] + ptap[3]) / 2)
ISUM_Y = (ptap[1] + ptap[3]) / 2

# --- N+ tap for DNWELL (VDD rail)
ntap = (DN[0] + 2.0, DN[3] - 2.2, DN[2] - 2.0, DN[3] - 1.7)
box("comp", *ntap)
box("nplus", ntap[0] - 0.16, ntap[1] - 0.16, ntap[2] + 0.16, ntap[3] + 0.16)
box("m1", *ntap)
contacts_row(ntap[0], ntap[2], (ntap[1] + ntap[3]) / 2)
VDD_Y = (ntap[1] + ntap[3]) / 2

# --- transistors
NY = ptap[3] + 1.4                         # NMOS row origin y
x_n1 = LPW[0] + 1.6
p_M1 = place(nfet_cell, x_n1, NY)
p_M2 = place(nfet_cell, x_n1 + 3.2, NY)
PY = ntap[1] - 1.6                         # PMOS row origin y
p_M3 = place(pfet_cell, LPW[2] + 2.6, PY)
p_M4 = place(pfet_cell, LPW[2] + 5.8, PY)
# NWELL (inside DNWELL) around the PFETs and the VDD tap: the DRC deck only
# counts an N-tap inside NWELL for the tap-distance rule DF.13
box("nwell", ntap[0] - 0.6, PY - 1.4, ntap[2] + 0.6, ntap[3] + 0.6)


def ctr(b):
    return b.center().x, b.center().y


# sources: M1 straps to the rails
for p in (p_M1, p_M2):                     # NMOS S down to Isum tap
    s = p["S"]
    box("m1", s.left, ptap[1], s.right, s.top)
for p in (p_M3, p_M4):                     # PMOS S up to VDD tap
    s = p["S"]
    box("m1", s.left, s.bottom, s.right, ntap[3])

# --- routing channel: M1 horizontal tracks between the rows, M2 vertical stubs.
# Under the MIM cap only M1, M2 and Via1 are used: the LVS deck drops any
# Via2/Via3 under FuseTop (via2_n_cap = via2.not(fusetop)), so Via2+ appear only
# in the two stacks outside the cap.
TRK = {"Vthr": NY + 1.9, "net1": NY + 2.7, "VT": NY + 3.5, "Isyn": NY + 4.3}
assert TRK["Isyn"] + 0.6 < PY - 0.7, "channel too small"
TW = 0.40                                   # track width
STACK_X = CW - 1.9                          # x of the two Via2..Via4 stacks
ESC_L, ESC_R = 1.8, CW - 1.3                # M1 -> M2 escape vias inside the guard ring


DOFF = 0.35   # drain via offset: keeps the drain M2 stub clear of the gate M2 pad


def drain_tap(pad):
    """M1 tab to the right of a drain pad; returns the via position on it."""
    cx, cy = ctr(pad)
    box("m1", pad.left, pad.bottom, cx + DOFF + 0.2, pad.top)
    return cx + DOFF, cy


def stub(pad, y_track, net, drain=False):
    """Via1 on the pad, M2 vertical to the track, Via1 down to the M1 track."""
    cx, cy = drain_tap(pad) if drain else ctr(pad)
    via_stack(cx, cy, 1, 2)
    box("m2", cx - 0.2, min(cy, y_track) - 0.2, cx + 0.2, max(cy, y_track) + 0.2)
    via_stack(cx, y_track, 1, 2)
    return cx


def track(net, x1, x2):
    y = TRK[net]
    box("m1", x1, y - TW / 2, x2, y + TW / 2)


def escape(y, x_via, x_edge):
    """Via1 from an M1 track to an M2 pin stub running out to the cell edge."""
    via_stack(x_via, y, 1, 2)
    box("m2", min(x_via, x_edge), y - 0.2, max(x_via, x_edge), y + 0.2)


# Vthr: M1 gate -> left edge
x = stub(p_M1["G"], TRK["Vthr"], "Vthr")
track("Vthr", ESC_L - 0.2, x + 0.2)
escape(TRK["Vthr"], ESC_L, 0.0)

# VT: M3 gate -> left edge
x = stub(p_M3["G"], TRK["VT"], "VT")
track("VT", ESC_L - 0.2, x + 0.2)
escape(TRK["VT"], ESC_L, 0.0)

# net1: M2 drain + gate, M3 drain, M4 gate -> stack up to the cap top plate
xs = [stub(p_M2["D"], TRK["net1"], "net1", drain=True), stub(p_M2["G"], TRK["net1"], "net1"),
      stub(p_M3["D"], TRK["net1"], "net1", drain=True), stub(p_M4["G"], TRK["net1"], "net1")]
track("net1", min(xs) - 0.2, STACK_X + 0.2)

# Isyn: M4 drain -> right edge
x = stub(p_M4["D"], TRK["Isyn"], "Isyn", drain=True)
track("Isyn", x - 0.2, ESC_R + 0.2)
escape(TRK["Isyn"], ESC_R, CW)

# VDD from M1 drain: M2 straight up to the VDD rail
cx, cy = drain_tap(p_M1["D"])
via_stack(cx, cy, 1, 2)
box("m2", cx - 0.2, cy - 0.2, cx + 0.2, VDD_Y + 0.2)
via_stack(cx, VDD_Y, 1, 2)

# VDD rail -> M2 -> right edge pin and the VDD stack
via_stack(ntap[2] - 0.3, VDD_Y, 1, 2)
box("m2", ntap[2] - 0.5, VDD_Y - 0.25, CW, VDD_Y + 0.25)

# Isum: tap -> M2 -> left edge
via_stack(ptap[0] + 0.3, ISUM_Y, 1, 2)
box("m2", 0.0, ISUM_Y - 0.25, ptap[0] + 0.5, ISUM_Y + 0.25)

# ------------------------------------------------------------- MIM capacitor
CAP = 22.36                                  # 22.36^2 * 2 fF/um^2 = 1.000 pF
CX0, CY0 = 1.4, 1.2                          # FuseTop lower-left
cap = ly.create_cell("cap_mim", "gf180mcu",
                     {"mim_option": "MIM-B", "metal_level": "M5", "wc": CAP, "lc": CAP})
top.insert(pya.DCellInstArray(cap.cell_index(), pya.DTrans(CX0, CY0)))
FT = (CX0, CY0, CX0 + CAP, CY0 + CAP)        # FuseTop / top plate (M5)
BP = (CX0 - 0.6, CY0 - 0.6, CX0 + CAP + 0.6, CY0 + CAP + 0.6)   # PCell bottom plate (M4)

# bottom plate (VDD): extend M4 above the top plate, via4 row up to an M5 VDD strip
V4Y = FT[3] + 0.6 + 0.25 + 0.05             # M5 strip >=0.6 from the wide top plate (MT.2b)
box("m4", BP[0], BP[1], BP[2], V4Y + 0.13 + 0.45)  # >=0.4 enclosure (MIMTM.2)
xv = FT[0] + 0.5
while xv < FT[2] - 0.5:
    sq("via4", xv, V4Y, VIA)
    xv += 1.0
box("m5", FT[0], V4Y - 0.25, STACK_X + 0.25, V4Y + 0.25)
# VDD stack: M2 rail -> M3 -> M4 island -> M5, outside the bottom plate (MIMTM.1: 1.2 um)
assert STACK_X - 0.25 - BP[2] >= 1.2
assert STACK_X - 0.25 > FT[2]               # stacks must sit outside FuseTop (LVS)
via_stack(STACK_X, VDD_Y, 2, 5)
box("m5", STACK_X - 0.25, VDD_Y - 0.25, STACK_X + 0.25, V4Y + 0.25)

# top plate (net1): extend M5 to the right, stack down to the net1 track
via_stack(STACK_X, TRK["net1"], 1, 5)
box("m5", FT[2] - 1.0, TRK["net1"] - 0.25, STACK_X + 0.25, TRK["net1"] + 0.25)

# ------------------------------------------------------------- pins / labels
PIN = 0.6   # pin box length at the edge


def pin(name, layer, x1, y1, x2, y2):
    box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(
        pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


pin("Vthr", "m2", 0.0, TRK["Vthr"] - 0.2, PIN, TRK["Vthr"] + 0.2)
pin("VT", "m2", 0.0, TRK["VT"] - 0.2, PIN, TRK["VT"] + 0.2)
pin("Isum", "m2", 0.0, ISUM_Y - 0.25, PIN, ISUM_Y + 0.25)
pin("Isyn", "m2", CW - PIN, TRK["Isyn"] - 0.2, CW, TRK["Isyn"] + 0.2)
pin("VDD", "m2", CW - PIN, VDD_Y - 0.25, CW, VDD_Y + 0.25)
pin("VSS", "m1", CW / 2 - 1.0, RING_O, CW / 2 + 1.0, RI)

box("bnd", 0, 0, CW, CH)                     # PR boundary

top.flatten(-1, True)
ly.write(OUT)
print("wrote", OUT, "bbox", top.dbbox())
