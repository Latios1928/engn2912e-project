"""
Signed DAC (analog/neuron/DAC_signed.sch) layout generator for GF180MCU (gf180mcuD, variant D).

Run inside the iic-osic-tools container, after DAC_binary.gds exists (gen_dac_binary.py):
    klayout -b -r gen_dac_signed.py -rd out=DAC_signed.gds
    klayout -b -r gen_dac_signed.py -rd out=X.gds -rd dac=DAC     (the 1:2:3:4 DAC instead)

Circuit:
    x1   DAC_binary (DAC_binary.sch, weights 1:2:4:8), output Isum = Y  -> DAC_binary.gds,
         unchanged (option -rd dac=DAC: the 1:2:3:4 DAC of DAC_signed.sch, DAC.gds)
    Mse  nfet_03v3  D=Isum_e G=sb S=Y   B=GND  W=0.22 L=0.28
    Msi  nfet_03v3  D=Isum_i G=s  S=Y   B=GND  W=0.22 L=0.28
    Mni  nfet_03v3  D=sb     G=s  S=GND B=GND  W=0.22 L=0.28   } inverter: sb = not s
    Mpi  pfet_03v3  D=sb     G=s  S=VDD B=VDD  W=0.44 L=0.28   }

Floorplan (hierarchical: the DAC is an instance, not copied):
  * The block is drawn for a DAC whose w/en pins are below its Isum pin and whose DNWELL
    VDD tap strip is near its top (DAC.gds). DAC_binary.gds is the other way up, so it is
    placed mirrored in y, the block is drawn as usual and the finished cell is mirrored
    back: the DAC keeps its own orientation, the block is upside down.
  * The DAC on the right. A narrow steering block on its left, in the P substrate inside a
    P+ guard ring (GND) that closes onto the DAC's own left ring side.
  * Row A: Msi and Mse side by side, sharing their Y terminals in the middle. Y goes on
    Metal2 straight to the DAC's Isum pin stub.
  * Above them, the inverter: Mni, then Mpi in an N-well with an N+ tap (VDD). The
    VDD tap is tied on Metal2 to the left end of the DAC's own DNWELL tap strip (VDD).
  * Isum_e, Isum_i and s run to the left edge on Metal3 (over the Metal2 verticals).
  * The DAC's w[3:0] and en pins are extended on Metal2 under the block to the left edge.
  * Pins (Metal2 at the edge, labelled): left Isum_e, Isum_i, s, en, w[3:0];
    right Vb, VDD, GND (the DAC's own); GND also on the Metal1 guard ring.
"""
import json
import os
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet, draw_pfet  # noqa: E402

cells.gf180mcu()
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
OUT = globals().get("out", "DAC_signed.gds")
DAC_NAME = globals().get("dac", "DAC_binary")
DAC_GDS = os.path.join(HERE, DAC_NAME + ".gds")
DAC_PINS = os.path.join(HERE, DAC_NAME + "_pins.json")

L = {
    "nwell": (21, 0), "comp": (22, 0), "poly": (30, 0), "pplus": (31, 0), "nplus": (32, 0),
    "cont": (33, 0), "m1": (34, 0), "via1": (35, 0), "m2": (36, 0), "via2": (38, 0),
    "m3": (42, 0), "bnd": (0, 0), "m1_lbl": (34, 10), "m2_lbl": (36, 10),
}
ly = pya.Layout()
ly.dbu = 0.001
ly.read(DAC_GDS)
dac = ly.top_cell()
assert dac.name == DAC_NAME, dac.name
top = ly.create_cell("DAC_signed")
li = {k: ly.layer(*v) for k, v in L.items()}


def box(layer, x1, y1, x2, y2):
    top.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def sq(layer, cx, cy, s):
    box(layer, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)


def via12(cx, cy):
    sq("m1", cx, cy, 0.4)
    sq("m2", cx, cy, 0.4)
    sq("via1", cx, cy, 0.26)


def via23(cx, cy):
    sq("m2", cx, cy, 0.4)
    sq("m3", cx, cy, 0.4)
    sq("via2", cx, cy, 0.26)


def vbar(x, y1, y2, layer="m1", w=0.4):
    box(layer, x - w / 2, min(y1, y2), x + w / 2, max(y1, y2))


def hbar(y, x1, x2, layer, w=0.4):
    box(layer, min(x1, x2), y - w / 2, max(x1, x2), y + w / 2)


def contacts_x(x1, x2, cy, pitch=0.5):
    n = int((x2 - x1 - 0.22) / pitch) + 1
    x0 = (x1 + x2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        sq("cont", x0 + i * pitch, cy, 0.22)


def contacts_y(cx, y1, y2, pitch=0.5):
    n = int((y2 - y1 - 0.22) / pitch) + 1
    y0 = (y1 + y2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        sq("cont", cx, y0 + i * pitch, 0.22)


def tap(x1, y1, x2, y2, implant):
    box("comp", x1, y1, x2, y2)
    box("m1", x1, y1, x2, y2)
    box(implant, x1 - 0.16, y1 - 0.16, x2 + 0.16, y2 + 0.16)


# ------------------------------------------------------------------ devices
def make_fet(kind, w, l, gate_pos):
    fn = draw_nfet if kind == "n" else draw_pfet
    c = fn(ly, l_gate=l, w_gate=w, nf=1, con_bet_fin=0 if w < 0.36 else 1,
           gate_con_pos=gate_pos, bulk="None")
    c.flatten(True)
    for k in li:                                   # snap to the 5 nm grid
        r = pya.Region(c.shapes(li[k]))
        if not r.is_empty():
            c.shapes(li[k]).clear()
            c.shapes(li[k]).insert(r.snapped(5, 5))
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    sd = sorted([p for p in pads if p.bottom < w / 2 < p.top], key=lambda b: b.center().x)
    gp = [p for p in pads if not (p.bottom < w / 2 < p.top)]
    assert len(sd) == 2 and len(gp) == 1, (kind, w, pads)
    return c, sd[0], sd[1], gp[0]


DOFF = 0.35


def place(dev, x, y_sd):
    """Place a device with its S/D centre line at y_sd. Returns pads L (left), R, G."""
    c, pl, pr, g = dev
    t = pya.DTrans(x, y_sd - pl.center().y)
    top.insert(pya.DCellInstArray(c.cell_index(), t))
    return {"L": t * pl, "R": t * pr, "G": t * g, "y": y_sd, "bbox": t * c.dbbox()}


def tab(d, side):
    """M1 tab outward from the left or right S/D pad; returns its via x."""
    p = d[side]
    if side == "L":
        x = p.center().x - DOFF
        box("m1", x - 0.2, p.bottom, p.right, p.top)
    else:
        x = p.center().x + DOFF
        box("m1", p.left, p.bottom, x + 0.2, p.top)
    return x


N_TOP = make_fet("n", 0.22, 0.28, "top")
P_BOT = make_fet("p", 0.44, 0.28, "bottom")

# ------------------------------------------------------------------ floorplan
DAC_H = dac.dbbox().height()
PINS_RAW = json.load(open(DAC_PINS))["pins"]
_a = {p["name"]: p["access"][0] for p in PINS_RAW if p["access"] and p["layer"] == "Metal2"}
FLIP = _a["w[0]"]["y1"] > _a["Isum"]["y1"]   # w/en above Isum: build the block mirrored in y


def fy(a):
    """Pin access box in the (possibly mirrored) DAC frame used while drawing."""
    if not FLIP:
        return dict(a)
    return dict(a, y1=DAC_H - a["y2"], y2=DAC_H - a["y1"])


pins = {p["name"]: fy(p["access"][0]) for p in PINS_RAW if p["access"]}
pins.update({n: fy(a) for n, a in _a.items()})
RO, RW = 0.3, 0.5
RI = RO + RW
ESC = 1.6                                  # x of the left-edge escape vias
X1 = 4.0                                   # Msi / Mni / Mpi origin
X2 = X1 + 2.6                              # Mse origin
BW = 10.0                                  # block width; the DAC starts here
DAC_X = BW


def mid(p):
    return (p["y1"] + p["y2"]) / 2


Y_ISUM = mid(pins["Isum"])                 # DAC output (Y) stub
Y_VDD_TAP = mid(pins["VDD"])               # the DAC's DNWELL N+ tap strip (VDD), from x = 4.5
YA = Y_ISUM + 1.1                          # row A S/D line (Msi, Mse)
YC = Y_VDD_TAP - 2.3                       # Mpi, just below the VDD tap
YB = YC - 2.0                              # Mni
assert YB > YA + 5.0
Y_E, Y_I, Y_S = YA + 1.9, YA + 2.7, YA + 3.5   # M3 escape tracks: Isum_e, Isum_i, s

T_DAC = pya.DTrans(DAC_X, DAC_H) * pya.DTrans(pya.DTrans.M0) if FLIP else pya.DTrans(DAC_X, 0)
top.insert(pya.DCellInstArray(dac.cell_index(), T_DAC))
msi = place(N_TOP, X1, YA)
mse = place(N_TOP, X2, YA)
mni = place(N_TOP, X1, YB)
mpi = place(P_BOT, X1, YC)
assert mni["G"].top < mpi["G"].bottom

# ------------------------------------------------------------------ guard ring (GND)
# left, bottom and top sides; the bottom and top sides run onto the DAC's left ring side,
# so the ring closes there (no extra contacts on the overlap).
tap(RO, RO, DAC_X + RI, RI, "pplus")                       # bottom
tap(RO, DAC_H - RI, DAC_X + RI, DAC_H - RO, "pplus")       # top
tap(RO, RO, RI, DAC_H - RO, "pplus")                       # left
contacts_x(RI + 0.2, DAC_X - 0.2, RO + RW / 2)
contacts_x(RI + 0.2, DAC_X - 0.2, DAC_H - RO - RW / 2)
contacts_y(RO + RW / 2, RI + 0.2, DAC_H - RI - 0.2)

# ------------------------------------------------------------------ N-well, VDD tap
pb = mpi["bbox"]
NT = (X1 - 0.5, Y_VDD_TAP - 0.25, X1 + 2.0, Y_VDD_TAP + 0.25)   # N+ tap strip
tap(*NT, "nplus")
contacts_x(NT[0], NT[2], Y_VDD_TAP)
box("nwell", min(pb.left, NT[0] - 0.6), pb.bottom, max(pb.right, NT[2] + 0.6), NT[3] + 0.6)
s = mpi["L"]                                               # Mpi source up to the tap
box("m1", s.left, s.bottom, s.right, NT[1] + 0.01)
# VDD: tap -> M2 -> the DAC's own tap strip (via at DAC x = 5.0)
via12(NT[2] - 0.3, Y_VDD_TAP)
hbar(Y_VDD_TAP, NT[2] - 0.5, DAC_X + 5.2, "m2")
via12(DAC_X + 5.0, Y_VDD_TAP)

# ------------------------------------------------------------------ row A: Msi | Mse
# Msi: L = Isum_i, R = Y.  Mse: L = Y, R = Isum_e (MOS source/drain are interchangeable).
box("m1", msi["R"].left, msi["R"].bottom, mse["L"].right, msi["R"].top)   # Y bridge
xy = (msi["R"].right + mse["L"].left) / 2
via12(xy, YA)
vbar(xy, YA, Y_ISUM, "m2")
hbar(Y_ISUM, xy - 0.2, DAC_X + 0.6, "m2")                  # onto the DAC's Isum stub

x_e = tab(mse, "R")                                        # Isum_e
via12(x_e, YA)
vbar(x_e, YA, Y_E, "m2")
via23(x_e, Y_E)
x_i = tab(msi, "L")                                        # Isum_i
via12(x_i, YA)
vbar(x_i, YA, Y_I, "m2")
via23(x_i, Y_I)

# ------------------------------------------------------------------ inverter
gn, gp = mni["G"], mpi["G"]
box("m1", gn.left, gn.top - 0.01, gn.right, gp.bottom + 0.01)          # s: gate bridge
x_s = msi["G"].center().x
assert abs(x_s - gn.center().x) < 0.05
via12(x_s, msi["G"].center().y)                            # Msi gate (s)
via12(x_s, (gn.top + gp.bottom) / 2)
vbar(x_s, msi["G"].center().y, (gn.top + gp.bottom) / 2, "m2")
via23(x_s, Y_S)

x_sb = tab(mni, "R")                                       # sb: Mni D + Mpi D
tab(mpi, "R")
vbar(x_sb, YB, YC)
x_g2 = mse["G"].center().x                                 # Mse gate (sb)
via12(x_g2, mse["G"].center().y)
vbar(x_g2, mse["G"].center().y, YB, "m2")
hbar(YB, x_sb - 0.2, x_g2 + 0.2, "m2")
via12(x_sb, YB)

x_gnd = tab(mni, "L")                                      # Mni source -> ring (GND)
box("m1", RI - 0.01, YB - 0.2, x_gnd + 0.2, YB + 0.2)

# ------------------------------------------------------------------ left-edge escapes / pins
PIN = 0.6


def pin(name, layer, x1, y1, x2, y2):
    box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


for name, y, x_from in (("Isum_e", Y_E, x_e), ("Isum_i", Y_I, x_i), ("s", Y_S, x_s)):
    hbar(y, ESC - 0.2, x_from + 0.2, "m3")
    via23(ESC, y)
    hbar(y, 0.0, ESC, "m2")
    pin(name, "m2", 0.0, y - 0.2, PIN, y + 0.2)
# the DAC's digital pins, extended under the block to the left edge
for name in ("en", "w[0]", "w[1]", "w[2]", "w[3]"):
    p = pins[name]
    assert p["y2"] + 0.3 < YA - 0.5
    box("m2", 0.0, p["y1"], DAC_X + p["x2"], p["y2"])
    pin(name, "m2", 0.0, p["y1"], PIN, p["y2"])
# the DAC's right-edge pins, labelled at this level
for name in ("Vb", "VDD", "GND"):
    a = pins[name]
    pin(name, "m2", DAC_X + a["x1"], a["y1"], DAC_X + a["x2"], a["y2"])
pin("GND", "m1", BW / 2 - 1.0, RO, BW / 2 + 1.0, RI)

CW = DAC_X + dac.dbbox().width()
box("bnd", 0, 0, CW, DAC_H)
if FLIP:                                   # mirror back: the DAC returns to its own orientation
    top.transform(pya.DTrans(0, DAC_H) * pya.DTrans(pya.DTrans.M0))
for inst in list(top.each_inst()):
    if inst.cell_inst.cell_index != dac.cell_index():
        inst.flatten(-1)
for ci in [c.cell_index() for c in ly.top_cells() if c.cell_index() != top.cell_index()]:
    ly.delete_cell_rec(ci)                         # unused device cells left after flattening
assert [c.name for c in ly.top_cells()] == ["DAC_signed"]
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, DAC_H))
