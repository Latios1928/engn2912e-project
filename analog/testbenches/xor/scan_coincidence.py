"""Option 2 bias scan: how strongly does the DPI favour two coincident inputs over one?

    python3 analog/testbenches/xor/scan_coincidence.py --k 4 --vtau 0.5,0.52 --vthr 2.5,2.6 [--mc 200]

Uses dpi/dpi_spike_tb (DPI alone, ideal tail current): the mean output current of a
5 kHz train of 10 us pulses (iavg2) at iw = 15 nA (one weight-1 input) and 30 nA (two
coincident weight-1 inputs), and the single-spike decay time constant, over a grid of
vtau and vthr. k scales all four DPI transistors (dpi/size_dpi.py; 1 = current sizes).

The DPI's idle current (iw = 0) is subtracted from both.
R = iavg2(30 nA) / iavg2(15 nA) is what the AND neuron's leak has to sit between: the
leak transistor is subthreshold, so the AND window in Vlk should be about
(UT/kappa) * ln(R), roughly 37 mV * ln(R). hidden_tb measures the real window.
With --mc N, each grid point is instead simulated with N mismatch samples (same seeds at
15 and 30 nA, so each sample is one DPI) and the report gives the spread of ln(iavg) and the
fraction of samples a single leak current can separate (the best common threshold).
Writes results/coincidence_k<k>[_mc].csv and .md.
"""

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "dpi"))
import tbtools as tb  # noqa: E402
from size_dpi import patch  # noqa: E402

RUNS = HERE / "runs" / "coincidence"
RESULTS = HERE / "results"
VTAU = [0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64]
VTHR = [2.60, 2.65, 2.70, 2.75, 2.80, 2.85, 2.909, 2.95]
I1, I2 = 15e-9, 30e-9


def separable(l1, l2):
    """Largest fraction of samples with ln i15 < T < ln i30 for one common threshold T."""
    best = 0
    for t in sorted(l1 + l2):
        best = max(best, sum(1 for a, b in zip(l1, l2) if a < t < b))
    return best / len(l1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--k", type=float, default=1, help="DPI device scale (default 1)")
    ap.add_argument("--vtau", help="comma-separated vtau values")
    ap.add_argument("--vthr", help="comma-separated vthr values")
    ap.add_argument("--mc", type=int, default=0, help="mismatch samples per point (0 = nominal)")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--tag", help="suffix for the result file names")
    a = ap.parse_args()
    k = a.k
    vtaus = [float(x) for x in a.vtau.split(",")] if a.vtau else VTAU
    vthrs = [float(x) for x in a.vthr.split(",")] if a.vthr else VTHR
    text = tb.netlist(HERE.parent / "dpi" / "dpi_spike_tb.sch", RUNS / "_netlists").read_text()
    tb.check_connected(text, "DPI")
    text = patch(text, [k] * 4)
    seeds = list(range(7000, 7000 + a.mc)) if a.mc else [None]
    cases = []
    for vtau in vtaus:
        for vthr in vthrs:
            for iw in (0.0, I1, I2):
                for sd in seeds:
                    cases.append(tb.Case(f"k{k:g}_{vtau}_{vthr}_{iw * 1e9:.0f}_{sd}", "dpi_spike_tb",
                                         params={"vtau": vtau, "vthr": vthr, "iw": iw, "tpw": "10u", "rate": "5k"},
                                         seed=sd, tags={"vtau": vtau, "vthr": vthr, "iw": iw, "seed": sd}))
    tb.run_cases(cases, {"dpi_spike_tb": text}, RUNS, a.jobs)
    for c in cases:
        import shutil
        shutil.rmtree(RUNS / c.name, ignore_errors=True)
    res = {(c.tags["vtau"], c.tags["vthr"], c.tags["iw"], c.tags["seed"]): c.results for c in cases if c.ok}
    rows, samples = [], []
    for vtau in vtaus:
        for vthr in vthrs:
            l1, l2, i1s, i2s, taus = [], [], [], [], []
            for sd in seeds:
                z, a1, a2 = (res.get((vtau, vthr, iw, sd), {}) for iw in (0.0, I1, I2))
                if not (z.get("iavg2") is not None and a1.get("iavg2") is not None and a2.get("iavg2") is not None):
                    continue
                # No response at all (at or below the idle current) is floored at 1 fA, not dropped:
                # for 15 nA that is the best case for an AND
                i1, i2 = (max(x["iavg2"] - z["iavg2"], 1e-15) for x in (a1, a2))
                i1s.append(i1)
                i2s.append(i2)
                l1.append(math.log(i1))
                l2.append(math.log(i2))
                if a1.get("tau_epsc"):
                    taus.append(a1["tau_epsc"])
            if not l1:
                rows.append({"vtau": vtau, "vthr": vthr})
                continue
            r = math.exp(statistics.mean(l2) - statistics.mean(l1))
            row = {"vtau": vtau, "vthr": vthr,
                   "iavg_15n_nA": statistics.median(i1s) * 1e9, "iavg_30n_nA": statistics.median(i2s) * 1e9,
                   "R": r, "window_mV_pred": 37 * math.log(r) if r > 1 else 0,
                   "tau_us_15n": statistics.median(taus) * 1e6 if taus else None}
            if a.mc:
                row.update({"n": len(l1), "sd_ln_i15": statistics.stdev(l1), "sd_ln_i30": statistics.stdev(l2),
                            "separable": separable(l1, l2)})
                # The leak sits at a fixed, nA-scale current set by Vlk. Yield at leak-equivalent current IL:
                # one input below IL/3 and two inputs above 3*IL (a factor 3 of margin on each side)
                for il in (1e-9, 3e-9, 10e-9):
                    row[f"yield_{il * 1e9:g}nA"] = sum(1 for x, y in zip(i1s, i2s)
                                                       if x < il / 3 and y > 3 * il) / len(i1s)
                samples.extend({"vtau": vtau, "vthr": vthr, "sample": i, "i15": x, "i30": y}
                               for i, (x, y) in enumerate(zip(i1s, i2s)))
            rows.append(row)
    RESULTS.mkdir(exist_ok=True)
    name = f"coincidence_k{k:g}" + ("_mc" if a.mc else "") + (f"_{a.tag}" if a.tag else "")
    with open(RESULTS / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(max(rows, key=len)))
        w.writeheader()
        w.writerows(rows)
    if samples:
        with open(RESULTS / f"{name}_samples.csv", "w", newline="") as f:
            w = csv.DictWriter(f, list(samples[0]))
            w.writeheader()
            w.writerows(samples)
    keys = list(max(rows, key=len))
    fmt = lambda v: "–" if v is None else (f"{v:.4g}" if isinstance(v, float) else str(v))
    md = [f"## Coincidence scan, DPI scale k = {k:g} (`scan_coincidence.py`)", "",
          "5 kHz train of 10 us pulses into the DPI alone. `R` = mean output current with 30 nA (two "
          "coincident weight-1 inputs) / with 15 nA (one). `window_mV_pred` = 37 mV x ln R, the AND window "
          "in Vlk this predicts. `tau_us_15n` = single-spike decay time constant. Idle current subtracted; no response is floored at 1 fA."
          + (f" Mismatch: {a.mc} samples per point; `separable` = largest fraction of samples one common "
             "leak current could separate (15 nA below it, 30 nA above); `yield_<I>nA` = fraction with 15 nA "
             "below I/3 and 30 nA above 3I, for a leak-equivalent current I." if a.mc else ""), "",
          "| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    md += ["| " + " | ".join(fmt(r.get(x)) for x in keys) + " |" for r in rows]
    (RESULTS / f"{name}.md").write_text("\n".join(md) + "\n")
    for r in rows:
        print(" ".join(f"{x}={fmt(r.get(x))}" for x in keys))


if __name__ == "__main__":
    main()
