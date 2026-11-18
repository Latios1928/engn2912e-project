#!/usr/bin/env python3
"""Make a simulation copy of the SNN_signed LVS reference netlist.

    python3 macro_sim.py <SNN_signed_lvs_ref.spice> <out.spice>

Two changes, both only in the copy:
- FETs longer than LMAX (bias MR_VK: 0.5/90.91 um) become equal series segments
  with the same W and total L, so ngspice finds a model bin (as
  analog/testbenches/snn/run_snn_signed.py does).
- The MIM cap is named after the LVS deck (cap_mim_2f0fF); use the simulation
  model the schematics use (cap_mim_2f0_m3m4_noshield).
"""

import re
import sys

LMAX = 50e-6  # longest L the GF180 nfet/pfet_03v3 model bins cover


def main(src, dst):
    out, n_split = [], 0
    for ln in open(src).read().splitlines():
        ln = ln.replace("cap_mim_2f0fF", "cap_mim_2f0_m3m4_noshield")
        m = re.match(r"^(X\S+) (\S+) (\S+) (\S+) (\S+) ([np]fet_03v3) (.*)$", ln)
        lm = m and re.search(r"(?<=\s)L=([0-9.]+)u", " " + m.group(7), re.I)
        if not lm or float(lm.group(1)) * 1e-6 <= LMAX:
            out.append(ln)
            continue
        name, d, g, s, b, mod, rest = m.groups()
        L = float(lm.group(1))
        n = int(L * 1e-6 // LMAX) + 1
        rest = re.sub(r"(?<=\s)L=[0-9.]+u", f"L={L / n:.4f}u", " " + rest, flags=re.I).strip()
        nodes = [d] + [f"{name}_s{i}" for i in range(1, n)] + [s]
        out += [f"{name}_{i} {nodes[i]} {g} {nodes[i + 1]} {b} {mod} {rest}" for i in range(n)]
        n_split += 1
    open(dst, "w").write("\n".join(out) + "\n")
    print(f"macro_sim: split {n_split} FET(s) longer than {LMAX * 1e6:.0f} um into series segments")


if __name__ == "__main__":
    main(*sys.argv[1:3])
