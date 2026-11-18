"""
gLayout neuron: analog/neuron/neuron_sized.sch -> neuron_glayout.gds (+ LVS ref, predictions).

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/neuron/layout/gen_neuron_glayout.py

Everything cell-specific is below; the floorplan, routing, rings and predictions live in
glayout_floorplan.py (two_row). The hand-drawn neuron_sized.gds (gen_neuron.py) is untouched.

Schematic issues handled here (printed on every run, also written into the LVS reference):
  * legalize(): M1..M5 0.22/0.28 -> 0.5/0.64, M6 0.22/5 -> 0.5/11.36 (glayout min W, W/L kept)
  * connect("x1_net2", "VT"): spike_amplifier_sized.sch's VN wire stops short of its label,
    so the amp's M2 gate floats. Remove this line once the schematic is fixed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "layout_tools"))   # glayout_* library

from glayout_netlist import from_schematic
from glayout_floorplan import two_row, write_cell

SCH = HERE.parent / "neuron_sized.sch"
# left -> right. Amp diff pair (x1_M1/x1_M2) adjacent with its tail; mirror x1_M4/x1_M5 adjacent.
ORDER_N = ["x1_M3", "x1_M1", "x1_M2", "M1", "M8", "M2", "M7", "M6", "M10", "M11"]
ORDER_P = ["x1_M4", "x1_M5", "M3", "M4", "M12", "M5", "M9"]


def build():
    cell = from_schematic(SCH).legalize()
    cell.connect("x1_net2", "VT")
    for w in cell.warnings():
        print("WARNING", w)
    return two_row(cell, "neuron_glayout", ORDER_N, ORDER_P, dummy_l=1.0)


if __name__ == "__main__":
    res = build()
    print(write_cell(res, HERE, report_nets=["VMEM", "spike", "net1", "net2", "x1_net3"]))
    if "--show" in sys.argv:
        res.top.flatten().show()
