"""Mismatch-driven sizing of the DPI synapse (analog/neuron/DPI.sch).

    python3 analog/testbenches/dpi/size_dpi.py sens            # contribution of each device
    python3 analog/testbenches/dpi/size_dpi.py sweep           # uniform scale vs spread
    python3 analog/testbenches/dpi/size_dpi.py check k1,k2,k3,k4   # one sizing: retune + MC

Every transistor of DPI.sch is 0.22u/0.28u. Here device i gets W = 0.22u*k_i and
L = 0.28u*k_i: W/L stays the same (so the nominal currents stay close), the gate
area grows by k_i^2, and mismatch (Pelgrom) should fall as 1/k_i. The sizes are
patched into the netlist of dpi_step_tb; DPI.sch itself is not changed.

Each sizing is first retuned (vthr, vtau) so that its nominal step gain and decay
time constant match the current DPI at the network's operating point (vthr 2.909 V,
vtau 0.40 V, 15 nA = weight 1), so the spreads compare like with like.
Writes results/dpi_sizing.md and results/dpi_sizing_<mode>.csv.
"""

import csv
import math
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402

RUNS = HERE / "runs" / "sizing"
RESULTS = HERE / "results"
DEVICES = ["M1", "M2", "M3", "M4"]
ROLE = {"M1": "nFET, gate Vthr (differential pair)", "M2": "nFET, diode on Vsyn (differential pair)",
        "M3": "pFET, gate VT (tau leak)", "M4": "pFET, output (Isyn)"}
OP = {"vthr": 2.909, "vtau": 0.40, "iw": 15e-9}     # network operating point
UNIT_AREA = 0.22 * 0.28                             # um^2


def patch(text, k):
    """Give DPI device Mi the scale k[i] (W = 0.22u*k, L = 0.28u*k)."""
    out, inside = [], False
    for line in text.splitlines():
        if line.lower().startswith(".subckt dpi "):
            inside = True
        elif line.lower().startswith(".ends"):
            inside = False
        m = re.match(r"(XM(\d))\s", line)
        if inside and m and m.group(1)[1:] in DEVICES:
            s = k[DEVICES.index(m.group(1)[1:])]
            line, n = re.subn(r"L=0\.28u W=0\.22u", f"L={0.28 * s:.4g}u W={0.22 * s:.4g}u", line)
            assert n == 1, line
        out.append(line)
    return "\n".join(out) + "\n"


class Runner:
    def __init__(self):
        self.base = tb.netlist(HERE / "dpi_step_tb.sch", RUNS / "_netlists").read_text()
        tb.check_connected(self.base, "DPI")
        self.n = 0

    def run(self, k, params_list, seeds=None, jobs=10):
        """Simulate one sizing for each (params, seed); returns the result dicts."""
        text = patch(self.base, k)
        cases = []
        for i, p in enumerate(params_list):
            self.n += 1
            cases.append(tb.Case(f"s{self.n}", "dpi_step_tb", params=p,
                                 seed=None if seeds is None else seeds[i]))
        tb.run_cases(cases, {"dpi_step_tb": text}, RUNS, jobs)
        for c in cases:
            shutil_rm(RUNS / c.name)
        return [c.results if c.ok else {} for c in cases]

    def nominal(self, k, vthr, vtau):
        r = self.run(k, [dict(OP, vthr=vthr, vtau=vtau)])[0]
        return r.get("gain"), r.get("tau_fall")

    def retune(self, k, target):
        """vthr, vtau that give the target (gain, tau_fall) for sizing k (Newton on the logs)."""
        g0, t0 = target
        vthr, vtau = OP["vthr"], OP["vtau"]
        for _ in range(6):
            pts = self.run(k, [dict(OP, vthr=vthr, vtau=vtau), dict(OP, vthr=vthr + 0.005, vtau=vtau),
                               dict(OP, vthr=vthr, vtau=vtau + 0.005)])
            (g, t), (gx, tx), (gy, ty) = [(p["gain"], p["tau_fall"]) for p in pts]
            e = [math.log(g / g0), math.log(t / t0)]
            if max(abs(x) for x in e) < 0.01:
                break
            J = [[math.log(gx / g) / 0.005, math.log(gy / g) / 0.005],
                 [math.log(tx / t) / 0.005, math.log(ty / t) / 0.005]]
            det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
            vthr -= (J[1][1] * e[0] - J[0][1] * e[1]) / det
            vtau -= (-J[1][0] * e[0] + J[0][0] * e[1]) / det
        return vthr, vtau, g, t

    def mc(self, k, vthr, vtau, n, seed0=5000):
        res = self.run(k, [dict(OP, vthr=vthr, vtau=vtau)] * n, seeds=[seed0 + i for i in range(n)])
        gains = [r["gain"] for r in res if r.get("gain", 0) > 0]
        taus = [r["tau_fall"] for r in res if r.get("tau_fall", 0) > 0]
        return {"n": len(gains), "sd_ln_gain": statistics.stdev(math.log(x) for x in gains),
                "sd_ln_tau": statistics.stdev(math.log(x) for x in taus),
                "gain_med": statistics.median(gains), "gain_min": min(gains), "gain_max": max(gains),
                "gains": gains}


def shutil_rm(d):
    import shutil
    shutil.rmtree(d, ignore_errors=True)


def area(k):
    return sum(s * s for s in k) * UNIT_AREA


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sens"
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    R = Runner()
    RESULTS.mkdir(exist_ok=True)
    target = R.nominal([1, 1, 1, 1], OP["vthr"], OP["vtau"])
    print(f"reference (all 0.22/0.28): gain {target[0]:.4g}, tau_fall {target[1] * 1e3:.4g} ms", flush=True)
    rows = []

    def do(label, k, retune=True):
        vthr, vtau = OP["vthr"], OP["vtau"]
        if retune and k != [1, 1, 1, 1]:
            vthr, vtau, g, t = R.retune(k, target)
        m = R.mc(k, vthr, vtau, n)
        row = {"sizing": label, **{f"k_{d}": s for d, s in zip(DEVICES, k)}, "area_um2": area(k),
               "vthr": vthr, "vtau": vtau, **{x: m[x] for x in m if x != "gains"}}
        rows.append(row)
        print(f"{label:28} area {row['area_um2']:7.3f} um2  vthr {vthr:.4f} vtau {vtau:.4f}  "
              f"sd_ln_gain {m['sd_ln_gain']:.3f}  sd_ln_tau {m['sd_ln_tau']:.3f}  (n={m['n']})", flush=True)
        return row

    if mode == "sens":
        base = do("all minimum (current)", [1, 1, 1, 1])
        for i, d in enumerate(DEVICES):
            k = [1, 1, 1, 1]
            k[i] = 8
            do(f"{d} x8 only", k)
        do("all x8", [8, 8, 8, 8])
    elif mode == "sweep":
        for s in [1, 2, 3, 4, 6, 8]:
            do(f"all x{s}", [s] * 4)
    elif mode == "check":
        k = [float(x) for x in sys.argv[2].split(",")]
        do("k = " + ",".join(f"{x:g}" for x in k), k)
    path = RESULTS / f"dpi_sizing_{mode}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote", path)


if __name__ == "__main__":
    main()
