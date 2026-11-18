"""
gLayout generator for the sized spike amplifier (analog/neuron/spike_amplifier_sized.sch).

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/neuron/layout/gen_spike_amp.py

Writes spike_amp.gds and spike_amp_lvs_ref.spice next to this file.

Circuit (5T OTA used as comparator):
    M1 nfet  D=net2      G=VP  S=net1  B=VSS   W=4    L=2
    M2 nfet  D=spike_out G=VN  S=net1  B=VSS   W=4    L=2
    M3 nfet  D=net1      G=VB  S=VSS   B=VSS   W=0.5  L=0.64  (schematic 0.22/0.28, see below)
    M4 pfet  D=net2      G=net2 S=VDD  B=VDD   W=0.5  L=8     (diode)
    M5 pfet  D=spike_out G=net2 S=VDD  B=VDD   W=0.5  L=8

Layout-only change: glayout cannot draw W < 0.5 um, so M3 is 0.5/0.64 (same W/L ~0.78 as
0.22/0.28). Update the schematic to match before relying on simulations.

Style: every NMOS in one shared deep n-well (body = VSS), dummy-transistor rings around the
NMOS and PMOS groups. Routing: met2 = device buses, met3 = local nets, met4 = NMOS->PMOS.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "layout_tools"))   # glayout_* library

from gdsfactory.component import Component
from glayout import gf180 as pdk, straight_route, via_stack

from glayout_helpers import fet, place, describe
from glayout_rings import dummy_ring, dnw_guard, nwell_guard, strap, label, _rect

W_IN, L_IN = 4.0, 2.0
W_TAIL, L_TAIL = 0.5, 0.64
W_LOAD, L_LOAD = 0.5, 8.0
GAP = 0.6          # device-to-device gap inside a group (> Nplus/Pplus spacing 0.4)
WIRE = 0.5         # local wire width


# ----------------------------------------------------------------------------- wiring
def bus(dev, term):
    """(x0, x1, y) of a FET's met2 bus for gate/source/drain."""
    w, e = dev.ports[f"multiplier_0_{term}_W"], dev.ports[f"multiplier_0_{term}_E"]
    return w.center[0], e.center[0], e.center[1]


def via(top, x, y, lo, hi):
    v = top << via_stack(pdk, lo, hi)
    v.move((x - v.center[0], y - v.center[1]))
    return v


def wire(top, pts, layer, w=WIRE):
    """Manhattan wire through pts on one metal layer (each segment a rectangle)."""
    lay = pdk.get_glayer(layer)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        _rect(top, lay, min(x0, x1) - w / 2, min(y0, y1) - w / 2,
              max(x0, x1) + w / 2, max(y0, y1) + w / 2)


def spike_amp():
    top = Component("spike_amp_build")

    # ------------------------------------------------------------- NMOS group (in DNW)
    m1 = top << fet(pdk, "n", W_IN, L_IN, with_dummy=False)
    m2 = top << fet(pdk, "n", W_IN, L_IN, with_dummy=False)
    place(m2, m1, "E", GAP)
    m3 = top << fet(pdk, "n", W_TAIL, L_TAIL, with_dummy=False)
    m3.move(((m1.center[0] + m2.center[0]) / 2 - m3.center[0], 0))
    place(m3, m1, "S", GAP)
    m3.move(((m1.center[0] + m2.center[0]) / 2 - m3.center[0], 0))  # re-center under pair

    dn = dummy_ring(pdk, top, [m1, m2, m3], "n", length=L_IN, rail="VSS", name="DN")
    g = dnw_guard(pdk, top, [m1, m2, m3, dn.ref], body="VSS", dnw="VDD", sub="VSS")
    top << straight_route(pdk, dn.ports["rail_N"], g.ports["body_N_top_met_S"])

    # ------------------------------------------------------------- PMOS group (above)
    pg = Component("pmos_grp")
    m4 = pg << fet(pdk, "p", W_LOAD, L_LOAD, with_dummy=False)
    m5 = pg << fet(pdk, "p", W_LOAD, L_LOAD, with_dummy=False)
    place(m5, m4, "E", GAP)
    dp = dummy_ring(pdk, pg, [m4, m5], "p", length=L_LOAD, rail="VDD", name="DP")
    ng = nwell_guard(pdk, pg, [m4, m5, dp.ref], body="VDD")
    pg << straight_route(pdk, dp.ports["rail_N"], ng.ports["body_N_top_met_S"])
    pg.add_ports(m4.get_ports_list(), prefix="M4_")
    pg.add_ports(m5.get_ports_list(), prefix="M5_")
    pg.add_ports(ng.ref.get_ports_list(), prefix="ng_")
    pr = top << pg
    # centre over the pair; 1 um above the substrate ring (NW.3 Nwell-DNW 3.1 is met
    # because the substrate ring already sits 2.5 um outside the DNWELL)
    cx = (m1.center[0] + m2.center[0]) / 2
    pr.move((cx - pr.center[0], g.ref.ymax + 1.0 - pr.ymin))

    class P:  # PMOS device ports in top coordinates
        def __init__(self, prefix): self.prefix = prefix
        @property
        def ports(self):
            return {k[len(self.prefix):]: v for k, v in pr.ports.items() if k.startswith(self.prefix)}
    p4, p5 = P("M4_"), P("M5_")

    # ------------------------------------------------------------- net1: M1.S, M2.S, M3.D (met3)
    _, _, ys = bus(m1, "source")
    via(top, m1.center[0], ys, "met2", "met3")
    via(top, m2.center[0], ys, "met2", "met3")
    wire(top, [(m1.center[0], ys), (m2.center[0], ys)], "met3")
    _, _, yd3 = bus(m3, "drain")
    via(top, cx, yd3, "met2", "met3")
    wire(top, [(cx, yd3), (cx, ys)], "met3")

    # ------------------------------------------------------------- VSS: M3.S -> body ring (met3)
    _, _, ys3 = bus(m3, "source")
    yb = g.ports["body_S_top_met_N"].center[1] - 0.25   # on the ring metal
    via(top, cx, ys3, "met2", "met3")
    via(top, cx, yb, "met2", "met3")
    wire(top, [(cx, ys3), (cx, yb)], "met3")

    # ------------------------------------------------------------- PMOS gates: M4.G - M5.G (met3)
    _, _, yg = bus(p4, "gate")
    xg4, xg5 = pr.ports["M4_multiplier_0_gate_E"].center[0] - 0.5, pr.ports["M5_multiplier_0_gate_W"].center[0] + 0.5
    x_n2 = m1.center[0] - 0.8      # net2 riser, off the net1 via column
    x_out = m2.center[0] + 0.8     # spike_out riser
    xg4 = min(xg4, x_n2)           # gate bar must reach the net2 riser
    via(top, xg4, yg, "met2", "met3")
    via(top, xg5, yg, "met2", "met3")
    wire(top, [(xg4, yg), (xg5, yg)], "met3")

    # ------------------------------------------------------------- net2 / spike_out (met4)
    _, _, yd = bus(m1, "drain")
    _, _, yd4 = bus(p4, "drain")
    for x in (x_n2, x_out):
        via(top, x, yd, "met2", "met4")
        via(top, x, yd4, "met2", "met4")
        wire(top, [(x, yd), (x, yd4)], "met4")
    via(top, x_n2, yg, "met3", "met4")   # net2 picks up the PMOS gate bar (diode M4)

    # ------------------------------------------------------------- VDD: M4.S, M5.S -> n-tap ring (met3)
    _, _, ysp = bus(p4, "source")
    ytop = pr.ports["ng_body_N_top_met_S"].center[1] + 0.25
    for dev, dx in ((p4, -2.5), (p5, +2.5)):
        x = (dev.ports["multiplier_0_source_W"].center[0] + dev.ports["multiplier_0_source_E"].center[0]) / 2 + dx
        via(top, x, ysp, "met2", "met3")
        via(top, x, ytop, "met2", "met3")
        wire(top, [(x, ysp), (x, ytop)], "met3")

    # ------------------------------------------------------------- ring straps
    strap(pdk, top, g.ports["body_N_top_met_N"], g.ports["sub_N_top_met_S"], shift=-6.0)   # body -> VSS
    strap(pdk, top, g.ports["dnw_N_top_met_N"], pr.ports["ng_body_S_top_met_S"], shift=6.0)  # DNW -> VDD

    # ------------------------------------------------------------- pins
    for dev, name in ((m1, "VP"), (m2, "VN"), (m3, "VB")):
        x0, x1, y = bus(dev, "gate")
        top.add_label(text=name, position=((x0 + x1) / 2, y), layer=pdk.get_glayer("met2_label"))
    top.add_label(text="spike_out", position=(x_out, (yd + yd4) / 2), layer=pdk.get_glayer("met4_label"))
    label(pdk, top, g.ports["sub_S_top_met_S"], "VSS")
    label(pdk, top, pr.ports["ng_body_N_top_met_N"], "VDD")

    ref_lines = [
        "XM1 net2 VP net1 VSS nfet_03v3 L=2u W=4u nf=1",
        "XM2 spike_out VN net1 VSS nfet_03v3 L=2u W=4u nf=1",
        f"XM3 net1 VB VSS VSS nfet_03v3 L={L_TAIL:g}u W={W_TAIL:g}u nf=1",
        "XM4 net2 net2 VDD VDD pfet_03v3 L=8u W=0.5u nf=1",
        "XM5 spike_out net2 VDD VDD pfet_03v3 L=8u W=0.5u nf=1",
    ] + dn.spice + dp.spice
    return top, ref_lines


if __name__ == "__main__":
    top, ref_lines = spike_amp()
    print(describe(top))
    flat = top.flatten()
    flat.name = "spike_amp"
    flat.write_gds(str(HERE / "spike_amp.gds"))
    with open(HERE / "spike_amp_lvs_ref.spice", "w") as f:
        f.write("* LVS reference for spike_amp.gds (generated by gen_spike_amp.py)\n"
                "* = spike_amplifier_sized.sch with M3 0.5/0.64 (glayout min W) + dummy rings\n"
                ".subckt spike_amp VDD VSS VP VN VB spike_out\n")
        f.write("\n".join(ref_lines) + "\n.ends\n")
    if "--show" in sys.argv:
        flat.show()
