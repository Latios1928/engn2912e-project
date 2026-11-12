"""
Inhibitory DPI synapse (analog/neuron/DPI_inh.sch) layout generator for GF180MCU
(gf180mcuD, variant D: 5LM, MIM-B M4-M5).

Run inside the iic-osic-tools container, after DPI_sized.gds exists:
    klayout -b -r gen_dpi.py -rd out=DPI_sized.gds -rd name=DPI_sized -rd w=0.88 -rd l=1.12
    klayout -b -r gen_dpi_inh.py -rd out=DPI_inh.gds

Circuit:
    x1   DPI_sized  (VDD, Vthr, VT, Isum; output Isyn = Im)       -> DPI_sized.gds, unchanged
    Mi1  nfet_03v3  D=Im   G=Im S=GND B=GND   W=2 L=8   (diode)
    Mi2  nfet_03v3  D=Iout G=Im S=GND B=GND   W=2 L=8   (1:1 mirror output)

Floorplan (hierarchical: DPI_sized is an instance, not copied):
  * DPI_sized on top. Below it, the mirror in the P substrate, inside a P+ guard ring (GND)
    whose top side is the DPI's own bottom guard-ring side (VSS = GND).
  * The mirror is one row of four identical W = 2 / L = 8 devices, rotated so that the
    gate length runs vertically: dummy, Mi2, Mi1, dummy. Sources are at the top (strapped
    to the ring), drains at the bottom; the Mi2 and Mi1 gate contacts face each other and
    are bridged on Metal1. The dummies have every terminal on GND.
  * Im: Mi1 drain -> Metal2 to the right, up a Metal2 riser just right of the DPI cell to
    its Isyn pin. Iout: Mi2 drain -> Metal2 to the left edge.
  * Pins (Metal2 at the edge, labelled): left Vthr, VT, Isum (the DPI's own pin stubs),
    Iout; right VDD; GND on the Metal1 guard ring.
"""
import json
import os
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet  # noqa: E402

cells.gf180mcu()
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
OUT = globals().get("out", "DPI_inh.gds")
DPI_GDS = globals().get("dpi", os.path.join(HERE, "DPI_sized.gds"))
DPI_PINS = globals().get("dpi_pins", os.path.join(HERE, "DPI_sized_pins.json"))

L = {
    "comp": (22, 0), "poly": (30, 0), "pplus": (31, 0), "nplus": (32, 0), "cont": (33, 0),
    "m1": (34, 0), "via1": (35, 0), "m2": (36, 0), "bnd": (0, 0),
    "m1_lbl": (34, 10), "m2_lbl": (36, 10),
}
ly = pya.Layout()
ly.dbu = 0.001
ly.read(DPI_GDS)
dpi = ly.top_cell()
assert dpi.name == "DPI_sized", dpi.name
top = ly.create_cell("DPI_inh")
li = {k: ly.layer(*v) for k, v in L.items()}


def box(layer, x1, y1, x2, y2):
    top.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def sq(layer, cx, cy, s):
    box(layer, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)


def via12(cx, cy):
    sq("m1", cx, cy, 0.4)
    sq("m2", cx, cy, 0.4)
    sq("via1", cx, cy, 0.26)


def vbar(x, y1, y2, layer="m1", w=0.4):
    box(layer, x - w / 2, min(y1, y2), x + w / 2, max(y1, y2))


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


def ptap(x1, y1, x2, y2):
    """P+ substrate strip: COMP + P+ implant + M1 (contacts added separately)."""
    box("comp", x1, y1, x2, y2)
    box("m1", x1, y1, x2, y2)
    box("pplus", x1 - 0.16, y1 - 0.16, x2 + 0.16, y2 + 0.16)


# ------------------------------------------------------------------ the DPI and its pins
pins = {p["name"]: p["access"][0] for p in json.load(open(DPI_PINS))["pins"]}
DPI_W = dpi.dbbox().width()
RO, RW = 0.3, 0.5                      # guard ring outer offset / width (same as gen_dpi.py)
RI = RO + RW

# ------------------------------------------------------------------ mirror devices
UW, UL = 2.0, 8.0
GAP = 0.8


def make_fet(gate_pos):
    c = draw_nfet(ly, l_gate=UL, w_gate=UW, nf=1, con_bet_fin=1, gate_con_pos=gate_pos,
                  bulk="None")
    c.flatten(True)
    for k in li:                                   # snap to the 5 nm grid
        r = pya.Region(c.shapes(li[k]))
        if not r.is_empty():
            c.shapes(li[k]).clear()
            c.shapes(li[k]).insert(r.snapped(5, 5))
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    sd = sorted([p for p in pads if p.bottom < UW / 2 < p.top], key=lambda b: b.center().x)
    gp = [p for p in pads if not (p.bottom < UW / 2 < p.top)]
    assert len(sd) == 2 and len(gp) == 1, pads
    return c, sd[0], sd[1], gp[0]


ROT = pya.DTrans(pya.DTrans.R270)              # (x, y) -> (y, -x): source on top, drain below
FET = {g: make_fet(g) for g in ("top", "bottom")}   # "top" gate -> right side, "bottom" -> left


def rot_extent(gpos):
    c = FET[gpos][0]
    return ROT * c.dbbox()


ROW = [("D_L", "bottom"), ("Mi2", "top"), ("Mi1", "bottom"), ("D_R", "top")]
H_DEV = max(rot_extent(g).height() for _, g in ROW)
ROW_W = sum(rot_extent(g).width() for _, g in ROW) + GAP * (len(ROW) - 1)

# y floorplan: ring bottom side, 0.8 clearance, devices, 0.8 clearance, ring top side = the
# DPI's bottom ring side
DEV_BOT = RI + 0.8
DEV_TOP = DEV_BOT + H_DEV
YD = DEV_TOP + 0.8 - RO                    # DPI origin: its ring bottom side starts at YD + RO
CH = YD + dpi.dbbox().height()

# x floorplan: Im riser in a column right of the DPI cell
RISER_X = DPI_W + 0.7
CW = RISER_X + 0.2 + 0.4 + RI             # block ring right side clears the riser
x = (CW - ROW_W) / 2
devs = {}
for name, gpos in ROW:
    c, s, d, g = FET[gpos]
    ext = rot_extent(gpos)
    t = pya.DTrans(x - ext.left, DEV_TOP - ext.top) * ROT
    top.insert(pya.DCellInstArray(c.cell_index(), t))
    devs[name] = {"S": t * s, "D": t * d, "G": t * g}
    x += ext.width() + GAP

top.insert(pya.DCellInstArray(dpi.cell_index(), pya.DTrans(0, YD)))
RING_TOP_IN = YD + RO                      # inner edge of the shared top ring side

# ------------------------------------------------------------------ guard ring (GND)
# left, bottom and right sides, plus the top side right of the DPI. Where the ring overlaps
# the DPI's own ring (corners) only COMP/M1/implant are drawn, no extra contacts.
ptap(RO, RO, CW - RO, RI)                                  # bottom
ptap(RO, RO, RI, YD + RI)                                  # left, up into the DPI ring corner
ptap(CW - RI, RO, CW - RO, YD + RI)                        # right
ptap(DPI_W - RI, YD + RO, CW - RO, YD + RI)                # top, right of the DPI
contacts_x(RI + 0.2, CW - RI - 0.2, RO + RW / 2)
contacts_y(RO + RW / 2, RI + 0.2, YD - 0.2)
contacts_y(CW - RO - RW / 2, RI + 0.2, YD + RO - 0.1)
contacts_x(DPI_W + 0.2, CW - RI - 0.2, YD + RO + RW / 2)

# ------------------------------------------------------------------ mirror wiring
for name in ("D_L", "Mi2", "Mi1", "D_R"):
    s = devs[name]["S"]                                    # sources up to the ring (GND)
    box("m1", s.left, s.bottom, s.right, RING_TOP_IN + 0.01)
for name in ("D_L", "D_R"):
    d, g = devs[name]["D"], devs[name]["G"]
    box("m1", d.left, RI - 0.01, d.right, d.top)           # dummy drain down to the ring
    box("m1", g.left, g.bottom, g.right, RING_TOP_IN + 0.01)   # dummy gate up to the ring
# gate bridge Mi2 (gate on its right) <-> Mi1 (gate on its left)
g2, g1 = devs["Mi2"]["G"], devs["Mi1"]["G"]
assert g2.right < g1.left
ym = (g1.bottom + g1.top) / 2
box("m1", g2.left, ym - 0.5, g1.right, ym + 0.5)
# Mi1 diode: its drain pad to its own gate contact (both Im)
d1 = devs["Mi1"]["D"]
box("m1", g1.left, d1.bottom, d1.left + 0.01, g1.bottom + 0.4)
box("m1", g1.left, d1.bottom, d1.right, d1.top)

# Im: Mi1 drain -> M2 right -> riser up to the DPI's Isyn pin
yi = d1.center().y
via12(d1.center().x, yi)
box("m2", d1.center().x - 0.2, yi - 0.2, RISER_X + 0.2, yi + 0.2)
isyn = pins["Isyn"]
y_isyn = YD + (isyn["y1"] + isyn["y2"]) / 2
vbar(RISER_X, yi - 0.2, y_isyn + 0.2, "m2")
box("m2", isyn["x1"] + 0.0, y_isyn - 0.2, RISER_X + 0.2, y_isyn + 0.2)

# Iout: Mi2 drain -> M2 left to the edge
d2 = devs["Mi2"]["D"]
yo = d2.center().y
via12(d2.center().x, yo)
box("m2", 0.0, yo - 0.2, d2.center().x + 0.2, yo + 0.2)

# VDD: the DPI's right-edge stub out to the new edge (above the riser's top end)
vdd = pins["VDD"]
assert YD + vdd["y1"] > y_isyn + 0.2 + 0.3
box("m2", vdd["x1"], YD + vdd["y1"], CW, YD + vdd["y2"])

# ------------------------------------------------------------------ pins
PIN = 0.6


def pin(name, layer, x1, y1, x2, y2):
    box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


for n in ("Vthr", "VT", "Isum"):                           # the DPI's own left-edge stubs
    p = pins[n]
    pin(n, "m2", p["x1"], YD + p["y1"], p["x2"], YD + p["y2"])
pin("Iout", "m2", 0.0, yo - 0.2, PIN, yo + 0.2)
pin("VDD", "m2", CW - PIN, YD + vdd["y1"], CW, YD + vdd["y2"])
pin("GND", "m1", CW / 2 - 1.0, RO, CW / 2 + 1.0, RI)

box("bnd", 0, 0, CW, CH)
# keep DPI_sized as a subcell (same cell as DPI_sized.gds); flatten only the mirror devices
for inst in list(top.each_inst()):
    if inst.cell_inst.cell_index != dpi.cell_index():
        inst.flatten(-1)
for ci in [c.cell_index() for c in ly.top_cells() if c.cell_index() != top.cell_index()]:
    ly.delete_cell_rec(ci)                         # unused device cells left after flattening
assert [c.name for c in ly.top_cells()] == ["DPI_inh"]
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
