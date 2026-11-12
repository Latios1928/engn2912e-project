"""DPI sizing for option 2 (hidden DPI in threshold mode), by DPI-only Monte Carlo.

    python3 analog/testbenches/xor/size_option2.py [--mc 100] [--jobs 3] [--only uniform,single]

In threshold mode one weight-1 input (15 nA) must give no DPI output and two coincident
inputs (30 nA) must give a large one. Where the DPI turns on is set by its tau current
(M3) and the differential pair, so the sizing that matters differs from the gain-spread
sizing of dpi/size_dpi.py. For each candidate sizing this script
  1. scans vtau at vthr = VTHR (nominal) and takes the middle of the range where 15 nA gives
     no output (< 1 pA above idle) and 30 nA gives more than 10 nA;
  2. runs --mc mismatch samples there and reports the yield: the fraction of samples with
     15 nA below IL/3 and 30 nA above 3*IL, for leak-equivalent currents IL = 1, 3, 10 nA.
Candidates: uniform scale k on all four devices, and one device at x8 with the rest x1.
Writes results/option2_sizing.csv and .md.
"""

import argparse
import csv
import shutil
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "dpi"))
import tbtools as tb  # noqa: E402
from size_dpi import patch, DEVICES, UNIT_AREA  # noqa: E402

RUNS = HERE / "runs" / "option2"
RESULTS = HERE / "results"
VTHR = 2.4
I1, I2 = 15e-9, 30e-9
IL = (1e-9, 3e-9, 10e-9)
UNIFORM = [1, 2, 3, 4, 6]


class Sim:
    def __init__(self, jobs):
        self.base = tb.netlist((HERE.parent / "dpi" / "dpi_spike_tb.sch").resolve(),
                               (RUNS / "_netlists").resolve()).read_text()
        tb.check_connected(self.base, "DPI")
        self.jobs, self.n = jobs, 0

    def iavg(self, k, points, seeds=(None,)):
        """{(vtau, iw, seed): iavg2 - idle} for each vtau in points and iw in (15n, 30n)."""
        text = patch(self.base, k)
        cases = []
        for vtau in points:
            for iw in (0.0, I1, I2):
                for sd in seeds:
                    self.n += 1
                    cases.append(tb.Case(f"o{self.n}", "dpi_spike_tb", seed=sd,
                                         params={"vtau": vtau, "vthr": VTHR, "iw": iw, "tpw": "10u", "rate": "5k"},
                                         tags={"vtau": vtau, "iw": iw, "seed": sd}))
        tb.run_cases(cases, {"dpi_spike_tb": text}, RUNS, self.jobs)
        raw = {(c.tags["vtau"], c.tags["iw"], c.tags["seed"]): c.results.get("iavg2") for c in cases}
        for c in cases:
            shutil.rmtree(RUNS / c.name, ignore_errors=True)
        out = {}
        for (vtau, iw, sd), v in raw.items():
            idle = raw.get((vtau, 0.0, sd))
            if iw and v is not None and idle is not None:
                out[(vtau, iw, sd)] = v - idle
        return out

    def centre(self, k):
        """Middle of the vtau range where 15 nA is off and 30 nA is on (nominal), or None."""
        grid = [round(0.40 + 0.01 * i, 3) for i in range(36)]
        r = self.iavg(k, grid)
        ok = [v for v in grid if r.get((v, I1, None), 1) < 1e-12 and r.get((v, I2, None), 0) > 10e-9]
        if not ok:
            return None, None
        lo, hi = min(ok), max(ok)
        fine = [round(lo - 0.01 + 0.0025 * i, 4) for i in range(int((hi - lo + 0.02) / 0.0025) + 1)]
        r = self.iavg(k, fine)
        ok = [v for v in fine if r.get((v, I1, None), 1) < 1e-12 and r.get((v, I2, None), 0) > 10e-9]
        return (min(ok) + max(ok)) / 2, max(ok) - min(ok)

    def mc(self, k, vtau, n):
        r = self.iavg(k, [vtau], seeds=range(9000, 9000 + n))
        pairs = [(r[(vtau, I1, s)], r[(vtau, I2, s)]) for s in range(9000, 9000 + n)
                 if (vtau, I1, s) in r and (vtau, I2, s) in r]
        y = {f"yield_{il * 1e9:g}nA": sum(1 for a, b in pairs if a < il / 3 and b > 3 * il) / len(pairs)
             for il in IL}
        on15 = sum(1 for a, _ in pairs if a > 0.1e-9) / len(pairs)
        off30 = sum(1 for _, b in pairs if b < 3e-9) / len(pairs)
        return {"n": len(pairs), **y, "frac_15n_on": on15, "frac_30n_off": off30,
                "i30_median_nA": statistics.median(b for _, b in pairs) * 1e9}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mc", type=int, default=100)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--only", default="uniform,single")
    ap.add_argument("--cands", help="explicit sizings k1,k2,k3,k4 separated by ';' (replaces --only)")
    ap.add_argument("--tag", help="suffix for the result files")
    a = ap.parse_args()
    S = Sim(a.jobs)
    cands = []
    if a.cands:
        a.only = ""
        for c in a.cands.split(";"):
            k = [float(x) for x in c.split(",")]
            cands.append(("k = " + ",".join(f"{x:g}" for x in k), k))
    if "uniform" in a.only:
        cands += [(f"all x{s}", [s] * 4) for s in UNIFORM]
    if "single" in a.only:
        for i, d in enumerate(DEVICES):
            k = [1, 1, 1, 1]
            k[i] = 8
            cands.append((f"{d} x8 only", k))
    rows = []
    for label, k in cands:
        c, width = S.centre(k)
        row = {"sizing": label, **{f"k_{d}": s for d, s in zip(DEVICES, k)},
               "area_um2": sum(s * s for s in k) * UNIT_AREA, "vtau_centre": c,
               "vtau_window_mV": width * 1e3 if width is not None else None}
        if c is not None:
            row.update(S.mc(k, c, a.mc))
        rows.append(row)
        print("  ".join(f"{x}={v:.4g}" if isinstance(v, float) else f"{x}={v}" for x, v in row.items()), flush=True)
    RESULTS.mkdir(exist_ok=True)
    keys = list(max(rows, key=len))
    name = "option2_sizing" + (f"_{a.tag}" if a.tag else "")
    with open(RESULTS / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(rows)
    fmt = lambda v: "–" if v is None else (f"{v:.3g}" if isinstance(v, float) else str(v))
    md = ["## DPI sizing for option 2 (threshold mode, `size_option2.py`)", "",
          f"DPI alone, 5 kHz train of 10 us pulses, vthr = {VTHR} V; vtau at the centre of the nominal range "
          "where 15 nA gives no output and 30 nA more than 10 nA. "
          f"{a.mc} mismatch samples. `yield_<I>nA`: 15 nA below I/3 and 30 nA above 3I. "
          "`frac_15n_on`: one input gives more than 0.1 nA; `frac_30n_off`: two inputs give less than 3 nA.", "",
          "| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    md += ["| " + " | ".join(fmt(r.get(x)) for x in keys) + " |" for r in rows]
    (RESULTS / f"{name}.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
