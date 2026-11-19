#!/usr/bin/env python3
"""Post-layout macro for the gate-level mixed-signal run (make run PEX=1).

    python3 pex_macro.py <SNN_signed_pex_sim.spice> <SNN_signed_lvs_ref.spice> <out.spice>

The extraction (analog/layout_tools/top/SNN_signed/pex/SNN_signed_pex_sim.spice, written by
analog/testbenches/snn/run_snn_signed.py: C-only Magic extraction, nets renamed for ngspice,
long FETs split) defines .subckt SNN_signed_flat with its own pin order. The testbench
(mixed/snn_ms_tb.spice) instantiates SNN_signed in the LVS reference's pin order, so this
writes the extraction with its .subckt line renamed to SNN_signed in that order.
"""
import re
import sys


def pins(text, name):
    m = re.search(rf"^\.subckt {name} (.*?)$", text.replace("\n+", " "), re.M | re.I)
    if not m:
        sys.exit(f"pex_macro.py: no .subckt {name}")
    return m.group(1).split()


def main(pex_path, lvs_path, out_path):
    pex = open(pex_path).read()
    flat = pins(pex, "SNN_signed_flat")
    lvs = pins(open(lvs_path).read(), "SNN_signed")
    if sorted(flat) != sorted(lvs):
        sys.exit(f"pex_macro.py: pin sets differ: {sorted(set(flat) ^ set(lvs))}")
    # Rename the extracted subcircuit to SNN_signed with the LVS pin order (only the header
    # changes: the pins are the same nets). No wrapper level, so the testbench's
    # .save v(x1.VMEM_k) finds the membranes as in the parasitic-free run.
    head = re.search(r"^\.subckt SNN_signed_flat .*?\n(?!\+)", pex, re.M | re.S)
    pex = (pex[:head.start()] + "* pins reordered to the LVS reference (pex_macro.py)\n"
           + f".subckt SNN_signed {' '.join(lvs)}\n" + pex[head.end():])
    open(out_path, "w").write(pex)
    print(f"pex_macro.py: {out_path} (SNN_signed_flat, {pex.count(chr(10) + 'C')} parasitic C)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
