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

def spike_amplifier(pdk, w_in)
