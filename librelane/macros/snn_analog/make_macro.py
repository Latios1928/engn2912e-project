#!/usr/bin/env python3
"""Hard-macro views of the analog SNN for LibreLane: snn_analog = SNN_signed + power rings.

    cd librelane/macros/snn_analog && python3 make_macro.py      # in the container (klayout.db)

Input (not modified): analog/layout_tools/top/SNN_signed/SNN_signed.gds and
SNN_signed_lvs_ref.spice, the signed-off 2-2-1 macro from top.py. Its 51 pins are 0.5 um
Metal2 pads on its bottom edge, VDD / VSS included, and it uses Metal1-Metal5 everywhere.

Why a wrapper: LibreLane's power grid (vertical Metal4 / horizontal Metal5 straps) connects to
a macro only where its straps cross the macro's power pins on those layers. SNN_signed has
only two 0.5 um Metal2 supply pads and blocks every metal layer, so the grid cannot reach it.
The wrapper cell snn_analog (named like the Verilog black box analog/snn/snn_analog.v that
snn_top.v instantiates) places SNN_signed unchanged and adds:
  - two Metal5 supply bands along the pin (bottom) edge, VSS outermost, VDD inside, both
    within the ~5.7 um the PDN's straps reach into the macro (see the comment in main())
  - each supply pad continued down on Metal2 to its band, with a Via2-Via3-Via4 stack
  - every signal pad continued down on Metal2 to the wrapper's bottom edge (the pin)
The power-grid connection depends on snn_top placing the macro flipped (FS) at the bottom
of the die, pins up, so the bands face the logic.

Writes (this folder):
  snn_analog.gds             wrapper + the SNN_signed hierarchy (self-contained)
  snn_analog.lef             abstract: size, pins, obstructions (SNN_signed body, all metals)
  snn_analog_lvs_ref.spice   SNN_signed's LVS reference + .subckt snn_analog wrapping it
"""
import re
from pathlib import Path

import klayout.db as db

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "analog/layout_tools/top/SNN_signed"
SRC_GDS, SRC_SPICE = SRC / "SNN_signed.gds", SRC / "SNN_signed_lvs_ref.spice"
CELL, INNER = "snn_analog", "SNN_signed"

# GF180MCU layers (GDS layer, datatype)
L = dict(M1=(34, 0), M2=(36, 0), M3=(42, 0), M4=(46, 0), M5=(81, 0),
         V2=(38, 0), V3=(40, 0), V4=(41, 0),
         M2_LBL=(36, 10), M4_LBL=(46, 10), M5_LBL=(81, 10),
         PR_BOUNDARY=(63, 0))   # Magic's PRBOUND (gf180mcuD.tech); LibreLane needs it in a macro GDS
LEF_LAYER = dict(M1="Metal1", M2="Metal2", M3="Metal3", M4="Metal4", M5="Metal5")

# Geometry (um), from the edge of the wrapper inwards
EDGE = 0.5          # wrapper edge -> ends of the supply bands (left / right)
BANDS = {"VSS": (0.5, 2.5), "VDD": (3.2, 5.2)}             # y (um) of the Metal5 supply bands
MARGIN = 16.0       # pin side: wrapper edge -> SNN_signed body (the PDN reaches about 5.7 um in)
SIDE_MARGIN = 2.0   # the other three sides: nothing there, so only a small clearance
VIA, VIA_PITCH, VIA_ENC = 0.26, 0.62, 0.12                 # 0.26 via, 0.36 space, >= 0.06 enclosure

POWER = ("VDD", "VSS")
ANALOG = ("Iref", "VT")


def um(v):
    return round(v / 0.005) * 0.005


def main():
    src = db.Layout()
    src.read(str(SRC_GDS))
    inner = src.cell(INNER)
    assert inner is not None, f"no cell {INNER} in {SRC_GDS}"
    dbu = src.dbu
    body = inner.dbbox()
    li = {k: src.layer(*v) for k, v in L.items()}

    # Pads: every Metal2 label of SNN_signed sits on a pad touching the body's bottom edge
    m2 = db.Region(inner.begin_shapes_rec(li["M2"])).merged()
    pads = {}
    for s in inner.shapes(li["M2_LBL"]).each():
        if not s.is_text():
            continue
        p = s.text_dpos
        hits = [poly.bbox() for poly in m2.each()
                if poly.bbox().contains(db.Point(round(p.x / dbu), round(p.y / dbu)))]
        assert len(hits) == 1, f"label {s.text_string}: {len(hits)} Metal2 pads"
        b = hits[0]
        box = db.DBox(b.left * dbu, b.bottom * dbu, b.right * dbu, b.top * dbu)
        assert abs(box.bottom - body.bottom) < 1e-3, f"{s.text_string} is not on the bottom edge"
        pads[s.text_string] = box
    assert len(pads) == 51, f"{len(pads)} pins, expected 51"

    # Wrapper: SNN_signed body moved to (SIDE_MARGIN, MARGIN): MARGIN below it (pin side, the
    # supply bands), SIDE_MARGIN on the left, right and top
    dx, dy = um(SIDE_MARGIN - body.left), um(MARGIN - body.bottom)
    W, H = um(body.width() + 2 * SIDE_MARGIN), um(body.height() + MARGIN + SIDE_MARGIN)
    top = src.create_cell(CELL)
    top.insert(db.DCellInstArray(inner.cell_index(), db.DTrans(dx, dy)))
    top.shapes(li["PR_BOUNDARY"]).insert(db.DBox(0, 0, W, H))

    shapes = []          # (layer key, DBox, net, is LEF pin shape) for the GDS and the LEF

    def rect(layer, x0, y0, x1, y1, net, pin=False):
        b = db.DBox(um(x0), um(y0), um(x1), um(y1))
        top.shapes(li[layer]).insert(b)
        shapes.append((layer, b, net, pin))

    def vias(layer, x0, y0, x1, y1):
        """Via array filling (x0, y0, x1, y1) with VIA_ENC enclosure."""
        nx = int((x1 - x0 - 2 * VIA_ENC - VIA) // VIA_PITCH) + 1
        ny = int((y1 - y0 - 2 * VIA_ENC - VIA) // VIA_PITCH) + 1
        ox = x0 + (x1 - x0 - (nx - 1) * VIA_PITCH - VIA) / 2
        oy = y0 + (y1 - y0 - (ny - 1) * VIA_PITCH - VIA) / 2
        for i in range(nx):
            for j in range(ny):
                x, y = ox + i * VIA_PITCH, oy + j * VIA_PITCH
                top.shapes(li[layer]).insert(db.DBox(um(x), um(y), um(x + VIA), um(y + VIA)))

    # Supply bands: two Metal5 bands along the pin (bottom) side, VSS outermost, VDD inside,
    # both within reach of the PDN. snn_top places this macro flipped (FS) at the bottom of
    # the die, pins up, so these bands face the logic, where the vertical Metal4 straps of
    # every supply come down; each strap crosses both bands and the PDN puts a via on its
    # own net's band. The straps stop FP_MACRO_*_HALO = 10 um short of the body obstruction
    # (MARGIN = 16 um in), i.e. about 5.7 um into the wrapper. Earlier tries (rings, side
    # bands) failed the grid check: concentric rings put VDD out of reach, and the straps on
    # the macro's sides are dangling pieces between the macro and the die edge.
    # Only the bands are LEF pin shapes: OpenROAD's grid check (PSM) cannot see vias inside
    # the macro, so a pin shape the grid does not touch counts as unconnected. Stubs and
    # landings are obstructions.
    for net, (y0, y1) in BANDS.items():
        rect("M5", EDGE, y0, W - EDGE, y1, net, pin=True)
        top.shapes(li["M5_LBL"]).insert(db.DText(net, db.DTrans(um(W / 2), um((y0 + y1) / 2))))

    # Pads -> stubs. Signal stubs end on the bottom edge (the pins). Each supply pad drops on
    # Metal2 to its band, with a Via2-Via3-Via4 stack (Metal3 / Metal4 landings) up to it.
    pins = {}
    for net, p in sorted(pads.items()):
        x0, x1, ytop = p.left + dx, p.right + dx, p.bottom + dy
        if net in BANDS:
            y0, y1 = BANDS[net]
            rect("M2", x0, y0, x1, ytop, net)
            v0, v1 = y0 + 0.2, y1 - 0.2
            rect("M3", x0, v0, x1, v1, net)
            rect("M4", x0, v0, x1, v1, net)
            for v in ("V2", "V3", "V4"):
                vias(v, x0, v0, x1, v1)
        else:
            rect("M2", x0, 0.0, x1, ytop, net)
            top.shapes(li["M2_LBL"]).insert(db.DText(net, db.DTrans(um((x0 + x1) / 2), um(0.5))))
            pins[net] = db.DBox(um(x0), 0.0, um(x1), um(ytop))

    # GDS: only the wrapper and what it uses, in 1 nm database units (SNN_signed.gds is in
    # 5 nm; KLayout DRC / LVS accept that, but LibreLane's Magic streamout requires 1 nm)
    out = db.Layout()
    out.dbu = 0.001
    out_top = out.create_cell(CELL)
    out_top.copy_tree(top)
    out.write(str(HERE / f"{CELL}.gds"))

    write_lef(W, H, shapes, pins, db.DBox(um(SIDE_MARGIN), um(MARGIN), um(SIDE_MARGIN + body.width()),
                                            um(MARGIN + body.height())))
    write_spice(sorted(pads))
    print(f"{CELL}: {W} x {H} um (SNN_signed {body.width():.2f} x {body.height():.2f} + {MARGIN} um pin-side / {SIDE_MARGIN} um other "
          f"margins), {len(pins)} signal pins on Metal2 (bottom edge), VSS / VDD bands on Metal5 "
          f"along the bottom edge")


def sort_key(n):
    m = re.match(r"(\w+)\[(\d+)\]$", n)
    return (m.group(1), -int(m.group(2))) if m else (n, 0)


def write_lef(W, H, shapes, pins, body):
    f = lambda v: f"{v:.3f}"   # noqa: E731
    o = ["VERSION 5.7 ;", 'BUSBITCHARS "[]" ;', 'DIVIDERCHAR "/" ;', "",
         f"MACRO {CELL}", "  CLASS BLOCK ;", f"  FOREIGN {CELL} 0 0 ;", "  ORIGIN 0 0 ;",
         f"  SIZE {f(W)} BY {f(H)} ;", "  SYMMETRY X Y ;"]
    for net in sorted(pins, key=sort_key):
        b = pins[net]
        d = "OUTPUT" if net.startswith("spike") else "INOUT" if net in ANALOG else "INPUT"
        o += [f"  PIN {net}", f"    DIRECTION {d} ;", "    USE SIGNAL ;", "    PORT",
              "      LAYER Metal2 ;", f"        RECT {f(b.left)} {f(b.bottom)} {f(b.right)} {f(b.top)} ;",
              "    END", f"  END {net}"]
    for net, use in (("VDD", "POWER"), ("VSS", "GROUND")):
        o += [f"  PIN {net}", "    DIRECTION INOUT ;", f"    USE {use} ;", "    PORT"]
        for layer in ("M2", "M3", "M4", "M5"):
            rs = [b for (ly, b, n, pin) in shapes if n == net and ly == layer and pin]
            if rs:
                o.append(f"      LAYER {LEF_LAYER[layer]} ;")
                o += [f"        RECT {f(b.left)} {f(b.bottom)} {f(b.right)} {f(b.top)} ;" for b in rs]
        o += ["    END", f"  END {net}"]
    # Obstructions: the SNN_signed body on every metal, plus the supply metal that is not a
    # pin shape (stubs, landings, lane), so the router keeps clear of it
    o.append("  OBS")
    for layer in ("M1", "M2", "M3", "M4", "M5"):
        rs = [body] + [b for (ly, b, n, pin) in shapes if ly == layer and n in POWER and not pin]
        o.append(f"    LAYER {LEF_LAYER[layer]} ;")
        o += [f"      RECT {f(b.left)} {f(b.bottom)} {f(b.right)} {f(b.top)} ;" for b in rs]
    o += ["  END", f"END {CELL}", "", "END LIBRARY", ""]
    (HERE / f"{CELL}.lef").write_text("\n".join(o))


def write_spice(nets):
    text = SRC_SPICE.read_text()
    m = re.search(rf"^\.subckt\s+{INNER}\s+(.*)$", text, re.M)
    inner_pins = m.group(1).split()
    assert sorted(inner_pins) == sorted(nets), "SPICE pins differ from the GDS pin labels"
    ports = ["VDD", "VSS", "Iref", "VT"] + sorted((n for n in nets if n not in POWER and n not in ANALOG),
                                                 key=sort_key)
    (HERE / f"{CELL}_lvs_ref.spice").write_text(
        f"* LVS reference of {CELL} (make_macro.py): {INNER} ({SRC_SPICE.relative_to(ROOT)}) inside\n"
        f"* VDD / VSS rings; the wrapper adds only metal, so its netlist is the one instance.\n"
        + text.rstrip() + "\n\n"
        f".subckt {CELL} {' '.join(ports)}\n"
        # gf180_xschem_klayout_spice_convert strips one leading X (top.py does the same)
        f"XX1 {' '.join(inner_pins)} {INNER}\n.ends\n")


if __name__ == "__main__":
    main()
