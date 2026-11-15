"""
Comparator layout for GF180MCU, built with gLayout.

Run (inside the container, from the repo root):
    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/neuron/layout/comparator_layout.py

Starter skeleton: an NMOS input diff pair plus an NMOS tail device, with the tail drain
routed to the pair's common source. Extend with the load/latch devices.
"""
from pathlib import Path

from gdsfactory.component import Component

from glayout import gf180 as pdk            # MappedPDK: layers, design rules, DRC/LVS hooks
from glayout import nmos, pmos              # transistor primitives
from glayout import c_route, L_route, straight_route, via_stack
from glayout import movex, movey, evaluate_bbox
from glayout.cells.elementary.diff_pair.diff_pair import diff_pair

OUT = Path(__file__).parent

def spike_amplifier(pdk,
                    w_in=4.0, l_in=2.0,
                    w_tail=0.5, l_tail=0.64,
                    w_pload=0.5, l_pload=8) -> Component:
    """
    Spike Amplifier Layout Function

    Parameters
    ----------
    pdk : MappedPDK
        The PDK object containing technology-specific information.
    w_in : float
        Width of the input NMOS transistors in micrometers.
    l_in : float    
        Length of the input NMOS transistors in micrometers.
    w_tail : float  
        Width of the tail NMOS transistor in micrometers.
    l_tail : float
        Length of the tail NMOS transistor in micrometers.
    w_pload : float
        Width of the load PMOS transistors in micrometers.
    l_pload : float
        Length of the load PMOS transistors in micrometers.
    Returns
    -------
    Component
        A gdsfactory Component representing the spike amplifier layout.
    """         
    spike_amplifier = Component("spike_amplifier")

    # --- input pair M1/M2 ---
    m1 = spike_amplifier << nmos(pdk, width=w_in, length=l_in, fingers=1, with_dnwell=True, with_substrate_tap=False, with_tie=False)
    m2 = spike_amplifier << nmos(pdk, width=w_in, length=l_in, fingers=1, with_dnwell=True, with_substrate_tap=False, with_tie=False)
    
    # --- tail device M3 ---
    m3 = spike_amplifier << nmos(pdk,width=w_tail, length=l_tail, fingers=1, with_dnwell=True, with_substrate_tap=False, with_tie=False)

    # --- PMOS current loads M4/M5 ---
    m4 = spike_amplifier << pmos(pdk, width=w_pload, length=l_pload, fingers=1, with_substrate_tap=False, with_tie=False)
    m5 = spike_amplifier << pmos(pdk, width=w_pload, length=l_pload, fingers=1, with_substrate_tap=False, with_tie=False)

    # DEVICE POSITIONING 
    gap = pdk.util_max_metal_seperation() + 0.5  #extra spacing to avoid DRC issues
    #middle row of transistors: M1, M2 
    m1.movex(-(evaluate_bbox(m1)[0] + gap) / 2)
    m2.movex((evaluate_bbox(m2)[0] + gap) / 2)

    #bottom tail device: M3
    m3.movey(-(evaluate_bbox(m3)[1] + evaluate_bbox(m1)[1])/2 - gap)

    #top PMOS loads: M4, M5
    dy = (evaluate_bbox(m4)[1] + evaluate_bbox(m1)[1])/2 + gap
    m4.movex(-(evaluate_bbox(m4)[0] + gap) / 2).movey(dy)
    m5.movex((evaluate_bbox(m5)[0] + gap) / 2).movey(dy)

    # ROUTING
    p = lambda dev, term, side: dev.ports[f"multiplier_0_{term}_{side}"]
    # Route the drains of M1 and M2 to the drains of M4 and M5
    spike_amplifier << c_route(pdk, p(m1, "source", "S"), p(m2, "source", "S"))

    return spike_amplifier



if __name__ == "__main__":
    c = spike_amplifier(pdk)
    c.show()
    c.write_gds(OUT / "spike_amplifier.gds")