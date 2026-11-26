#!/usr/bin/env python3
"""Make a simulation copy of the SNN_signed LVS reference netlist.

    python3 macro_sim.py <SNN_signed_lvs_ref.spice> <out.spice>

Three changes, all only in the copy:
- FETs with all four terminals on one net (the layout's dummies, ~80 % of the macro's
  FETs) are dropped: they carry no current and add no capacitance, so results do not
  change and the simulation runs several times faster (as
  analog/testbenches/snn/run_snn_signed.py does for its copies).
- FETs longer than LMAX (bias MR_VK: 0.5/90.91 um) become equal series segments
  with the same W and total L, so ngspice finds a model bin.
- The MIM cap is named after the LVS deck (cap_mim_2f0fF); use the simulation
  model the schematics use (cap_mim_2f0_m3m4_noshield).
"""

import re
import sys

LMAX = 50e-6  # longest L the GF180 nfet/pfet_03v3 model bins cover
FET = re.compile(r"^(X\S+) (\S+) (\S+) (\S+) (\S+) ([np]fet_03v3) (.*)$")


def main(src, dst):
    out, n_split, n_dummy = [], 0, 0
    for ln in open(src).read().replace("\n+", " ").splitlines():
        ln = ln.replace("cap_mim_2f0fF", "cap_mim_2f0_m3m4_noshield")
        m = FET.match(ln)
        if m and len(set(m.group(2, 3, 4, 5))) == 1:
            n_dummy += 1
            continue
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
    print(f"macro_sim: dropped {n_dummy} fully tied dummy FETs, split {n_split} FET(s) longer "
          f"than {LMAX * 1e6:.0f} um into series segments")


if __name__ == "__main__":
    main(*sys.argv[1:3])
