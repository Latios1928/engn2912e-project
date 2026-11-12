"""Firing rate of neuron_sized versus constant input current (neuron_rate_tb.sch).

    python3 analog/testbenches/neuron/run_neuron_rate.py            # schematic neuron
    python3 analog/testbenches/neuron/run_neuron_rate.py --pex      # post-layout neuron
    python3 analog/testbenches/neuron/run_neuron_rate.py --quick    # 10 currents, no refinement

Run inside the container (it calls xschem and ngspice). Sweeps the input current
log-spaced from 0.3 nA to 10 uA, then adds points where the neuron starts to
fire and where it latches. Each point runs in runs/rate_<sch|pex>_<current>/
(netlist, ngspice log, waveforms) with one ngspice thread, --jobs at a time.

Writes, in results/ (names start with the testbench name; post-layout runs add __pex):
  neuron_rate_tb.csv / neuron_rate_tb__pex.csv   every point
  neuron_rate_tb.md  / neuron_rate_tb__pex.md    summary
  neuron_rate_tb.png                              rate vs current, schematic and
                                                  post-layout overlaid when both exist
"""

import argparse
import csv
import datetime
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402
import tbpex  # noqa: E402

TB = "neuron_rate_tb"
CELL = "neuron_sized"
RESULTS = HERE / "results"
RUNS = HERE / "runs"

GRID_NA = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1, 1.5, 2, 3, 5, 7, 9.5, 15, 20, 30, 50, 100,
           200, 500, 1000, 2000, 5000, 10000]
QUICK_NA = [0.5, 1, 2, 5, 9.5, 20, 50, 200, 1000, 5000]

VSW = 1.65                 # VDD/2: spike threshold, as in the testbench
SPIKE_LOW = 0.33           # 10 % VDD: a spike must fall back below this between spikes
C_MEM, V_T = 1e-12, 1.66   # for the run-length estimate only
I_LEAK_GUESS = 0.5e-9
NOMINAL_PERIOD = 201.409e-6  # neuron_nominal_tb, schematic, 9.5 nA, 20 ns step
SPEC_PERIOD = (190e-6, 210e-6)  # sizing_context.txt, at 9.5 nA


def tstop_for(i):
    """Long enough for about 12 periods, between 1 ms and 30 ms."""
    period = C_MEM * V_T / max(i - I_LEAK_GUESS, 0.02e-9) + 30e-6
    return min(max(12 * period, 1e-3), 30e-3)


def case_for(i, variant, tmax):
    label = f"{i * 1e9:.4g}".replace(".", "p")
    return tb.Case(name=f"rate_{variant}_{label}nA", tb=TB,
                   params={"p_iin": f"{i:.6g}", "p_tstop": f"{tstop_for(i):.4g}",
                           "p_tmax": f"{tmax:.3g}"},
                   tags={"iin": i})


def classify(c):
    r = c.results
    if not c.ok or r.get("nspikes") is None:
        return "error"
    if (r.get("spike_min_end") or 0) > VSW:
        return "latched"       # spike stuck high: the input beats the reset
    n = int(r["nspikes"])
    if n == 0:
        return "silent"
    if n < 3:
        return "few"
    # The input beats the reset: the spike no longer falls back to ~0 V between
    # spikes and VMEM is not held at 0, so the refractory period is lost. The
    # count is then of incomplete spikes, not a usable firing rate.
    if (r.get("spike_min_end") or 0) > SPIKE_LOW:
        return "overdriven"
    return "fires"


def refine(done, variant, tmax):
    """Extra points at the firing onset and at the overdrive / latch onsets."""
    pts = sorted(done, key=lambda c: c.tags["iin"])
    cls = [(c.tags["iin"], classify(c)) for c in pts]
    extra = []
    fires = [i for i, k in cls if k == "fires"]
    if fires:
        below = [i for i, k in cls if k in ("silent", "few") and i < fires[0]]
        if below and fires[0] / below[-1] > 1.05:
            lo, hi = below[-1], fires[0]
            extra += [lo + (hi - lo) * j / 7 for j in range(1, 7)]
        bad = [i for i, k in cls if k in ("overdriven", "latched") and i > fires[-1]]
        if bad and bad[0] / fires[-1] > 1.05:
            lo, hi = fires[-1], bad[0]
            extra += [lo * (hi / lo) ** (j / 5) for j in range(1, 5)]
    return [case_for(i, variant, tmax) for i in extra]


def summarize(cases):
    pts = sorted(cases, key=lambda c: c.tags["iin"])
    rows = [(c.tags["iin"], classify(c), c.results) for c in pts]
    s = {"rows": rows}
    fires = [(i, r["rate"]) for i, k, r in rows if k == "fires"]
    silent = [i for i, k, _ in rows if k in ("silent", "few")]
    latched = [i for i, k, _ in rows if k == "latched"]
    over = [i for i, k, _ in rows if k == "overdriven"]
    s["i_fire"] = fires[0][0] if fires else None
    s["i_silent"] = max((i for i in silent if not fires or i < fires[0][0]), default=None)
    s["i_ok_max"] = fires[-1][0] if fires else None
    s["i_over"] = min((i for i in over if not fires or i > fires[-1][0]), default=None)
    s["i_latch"] = min((i for i in latched if not fires or i > fires[-1][0]), default=None)
    s["rate_max"] = max(fires, key=lambda p: p[1]) if fires else None
    # Slope of f vs I over 1-20 nA (about 1/(C VT) for an ideal integrate-and-fire
    # neuron). Its intercept is not the firing threshold: the curve bends near it.
    fit = [(i, f) for i, f in fires if 1e-9 <= i <= 20e-9]
    if len(fit) >= 3:
        mx = sum(i for i, _ in fit) / len(fit)
        my = sum(f for _, f in fit) / len(fit)
        s["gain"] = sum((i - mx) * (f - my) for i, f in fit) / sum((i - mx) ** 2 for i, _ in fit)
    at95 = [r["rate"] for i, k, r in rows if abs(i - 9.5e-9) < 1e-12 and k == "fires"]
    s["period_95"] = 1 / at95[0] if at95 else None
    return s


def eng(x, unit):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    for f, p in ((1e-12, "p"), (1e-9, "n"), (1e-6, "u"), (1e-3, "m"), (1, ""), (1e3, "k")):
        if abs(x) < f * 1000:
            return f"{x / f:.4g} {p}{unit}"
    return f"{x / 1e6:.4g} M{unit}"


def write_csv(path, s):
    keys = ["nspikes", "rate", "t_first", "t_last", "spike_max", "spike_min_end",
            "spike_max_end", "vmem_min_end", "vmem_max_end"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iin_A", "class"] + keys)
        for i, k, r in s["rows"]:
            w.writerow([f"{i:.6g}", k] + [r.get(x, "") for x in keys])


def write_md(path, s, variant, note, tmax):
    L = [f"# {TB}{'__pex' if variant == 'pex' else ''}: firing rate vs input current",
         "",
         f"Generated by `run_neuron_rate.py{' --pex' if variant == 'pex' else ''}` on "
         f"{datetime.datetime.now():%Y-%m-%d %H:%M}. Neuron: "
         + ("post-layout extraction (" + note + ")" if variant == "pex" else "schematic `neuron_sized.sch`")
         + f". tt, 27 C, VDD 3.3 V, biases as in `neuron_nominal_tb`, maximum time step {eng(tmax, 's')}.",
         "",
         "| Result | Value |",
         "|---|---|",
         f"| Lowest current tested that does not fire repeatedly | {eng(s['i_silent'], 'A')} |",
         f"| Lowest current tested that fires (>= 3 spikes) | {eng(s['i_fire'], 'A')} |"]
    if "gain" in s:
        L += [f"| Slope of the rate, 1-20 nA (ideal 1/(C VT) = {1 / (C_MEM * V_T) * 1e-9:.0f} Hz/nA) | "
              f"{s['gain'] * 1e-9:.1f} Hz/nA |"]
    if s["rate_max"]:
        L += [f"| Highest current with clean spikes, and its rate | {eng(s['i_ok_max'], 'A')}: "
              f"{eng(s['rate_max'][1], 'Hz')} |"]
    L += [f"| Lowest current tested that overdrives (spike no longer falls below "
          f"{SPIKE_LOW} V) | {eng(s['i_over'], 'A')} |",
          f"| Lowest current tested that latches (spike stuck high) | {eng(s['i_latch'], 'A')} |"]
    if s["period_95"]:
        ok = SPEC_PERIOD[0] <= s["period_95"] <= SPEC_PERIOD[1]
        L += [f"| Period at 9.5 nA (spec 190-210 us) | {eng(s['period_95'], 's')} "
              f"{'PASS' if ok else 'FAIL'} |"]
    L += ["", "Classes: *fires* >= 3 clean spikes; *few* 1-2 spikes (too slow to measure a rate "
          "in the run); *silent* no spike; *overdriven* the input beats the reset, so the spike no "
          f"longer falls below {SPIKE_LOW} V between spikes and VMEM is not held at 0 (the count is "
          "of incomplete spikes, shown in brackets); *latched* spike stuck high at the end of the run.",
          "",
          "| Iin | class | spikes | rate | first spike | spike min at end | VMEM at end (min-max) |",
          "|---|---|---|---|---|---|---|"]
    for i, k, r in s["rows"]:
        rate = (eng(r.get('rate'), 'Hz') if k == 'fires'
                else f"({eng(r.get('rate'), 'Hz')})" if k == 'overdriven' else '-')
        L.append(f"| {eng(i, 'A')} | {k} | {int(r.get('nspikes') or 0)} | {rate} | "
                 f"{eng(r.get('t_first'), 's') if (r.get('t_first') or -1) > 0 else '-'} | "
                 f"{r.get('spike_min_end', float('nan')):.3f} V | "
                 f"{r.get('vmem_min_end', float('nan')):.3f}-{r.get('vmem_max_end', float('nan')):.3f} V |")
    L += ["", f"Plot: `{TB}.png`. Per-point netlists, logs and waveforms: `runs/rate_{variant}_*/`."]
    path.write_text("\n".join(L) + "\n")


def read_csv(path):
    with open(path) as f:
        return [(float(r["iin_A"]), r["class"], float(r["rate"] or 0)) for r in csv.DictReader(f)]


def plot():
    """Rate vs current; overlays schematic and post-layout when both CSVs exist."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: no plot")
        return
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    series = [("sch", "Schematic", "#2a78d6", "o"), ("pex", "Post-layout (PEX)", "#eb6834", "s")]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=surf)
    ax.set_facecolor(surf)
    shown = 0
    onsets = {}  # (kind, current) -> [(series label, color)]
    for variant, label, color, marker in series:
        path = RESULTS / f"{TB}{'__pex' if variant == 'pex' else ''}.csv"
        if not path.exists():
            continue
        rows = read_csv(path)
        pts = [(i * 1e9, f) for i, k, f in rows if k == "fires"]
        if not pts:
            continue
        x, y = zip(*pts)
        ax.plot(x, y, color=color, lw=2, marker=marker, ms=6, mec=surf, mew=1.5, label=label)
        # Overdriven points: hollow, dashed, not a usable rate
        od = [(i * 1e9, f) for i, k, f in rows if k == "overdriven"]
        if od:
            ox, oy = zip(*([pts[-1]] + od))
            ax.plot(ox, oy, color=color, lw=1, ls="--", marker=marker, ms=6, mfc=surf,
                    mec=color, mew=1.5, markevery=list(range(1, len(ox))))
        fire = [i for i, k, _ in rows if k == "fires"]
        for kind in ("overdriven", "latched"):
            at = [i for i, k, _ in rows if k == kind and fire and i > max(fire)]
            if at:
                onsets.setdefault((kind, min(at)), []).append((label, color))
        shown += 1
    if not shown:
        plt.close(fig)
        return
    # One line per onset; shared by both series when they coincide
    for (kind, i), who in sorted(onsets.items(), key=lambda kv: kv[0][1]):
        color = who[0][1] if len(who) == 1 else ink2
        name = who[0][0] if len(who) == 1 else "both"
        ax.axvline(i * 1e9, color=color, lw=1, ls="--" if kind == "overdriven" else ":")
        ax.annotate(f"{kind} from {i * 1e9:.4g} nA ({name})", (i * 1e9, 0.02),
                    xycoords=("data", "axes fraction"), rotation=90, fontsize=8,
                    color=ink2, ha="right", va="bottom")
    # Spec window at the design point: 9.5 nA, period 190-210 us
    ax.plot([9.5, 9.5], [1 / SPEC_PERIOD[1], 1 / SPEC_PERIOD[0]], color=ink, lw=3,
            solid_capstyle="butt")
    ax.annotate("spec: 9.5 nA,\n4.76-5.26 kHz", (9.5, 1 / SPEC_PERIOD[0]), xytext=(-8, 8),
                textcoords="offset points", ha="right", fontsize=8, color=ink2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Input current into VMEM (nA)", color=ink2)
    ax.set_ylabel("Firing rate (Hz)", color=ink2)
    ax.set_title("neuron_sized: firing rate vs input current (tt, 27 C)\n"
                 "hollow, dashed: overdriven (spike no longer resets; not a usable rate)",
                 color=ink, loc="left", fontsize=10)
    ax.grid(True, which="major", color=grid, lw=0.8)
    for sp in ax.spines.values():
        sp.set_color(grid)
    ax.tick_params(colors=ink2)
    ax.legend(frameon=False, labelcolor=ink2, loc="upper left")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{TB}.png", dpi=150, facecolor=surf)
    plt.close(fig)
    print(f"wrote {RESULTS / (TB + '.png')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of the neuron")
    ap.add_argument("--quick", action="store_true", help="10 currents, no refinement")
    ap.add_argument("--jobs", type=int, default=4, help="parallel ngspice runs (one thread each)")
    ap.add_argument("--tmax", type=float, default=100e-9, help="maximum time step (s)")
    ap.add_argument("--report-only", action="store_true",
                    help="no simulation: rebuild the report from the runs already in runs/")
    a = ap.parse_args()
    variant = "pex" if a.pex else "sch"

    if a.report_only:
        done = []
        for log in sorted(RUNS.glob(f"rate_{variant}_*/ngspice.log")):
            c = tb.Case(name=log.parent.name, tb=TB)
            c.log = log.read_text()
            c.results = tb.parse_results(c.log)
            c.ok = bool(c.results) and "aborted" not in c.log
            if c.results.get("iin"):
                c.tags["iin"] = c.results["iin"]
                done.append(c)
        if not done:
            raise SystemExit(f"no runs in {RUNS}/rate_{variant}_*")
        print(f"{variant}: report from {len(done)} existing runs (no simulation)")
        report(done, variant, a, note=tbpex.pex_note((RUNS / done[0].name / f"{TB}.spice").read_text()) if a.pex else "")
        return

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / f"netlist_{variant}").read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    tb.check_connected(text, CELL)
    note = ""
    if a.pex:
        text = tbpex.use_pex(text, CELL)
        note = tbpex.pex_note(text)
    netlists = {TB: text}

    cases = [case_for(i * 1e-9, variant, a.tmax) for i in (QUICK_NA if a.quick else GRID_NA)]
    print(f"{variant}: {len(cases)} currents, {a.jobs} at a time")
    done = tb.run_cases(cases, netlists, RUNS, jobs=a.jobs)
    if not a.quick:
        more = refine(done, variant, a.tmax)
        if more:
            print(f"{variant}: {len(more)} more points at the firing / latch onsets")
            done += tb.run_cases(more, netlists, RUNS, jobs=a.jobs)
    bad = [c.name for c in done if not c.ok]
    if bad:
        print("simulations that failed (see runs/<name>/ngspice.log):", ", ".join(bad))
    report(done, variant, a, note)


def report(done, variant, a, note):
    s = summarize(done)
    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}{'__pex' if a.pex else ''}"
    write_csv(RESULTS / f"{stem}.csv", s)
    write_md(RESULTS / f"{stem}.md", s, variant, note, a.tmax)
    print(f"wrote {RESULTS / (stem + '.csv')} and .md")
    if s["period_95"] and not a.pex:
        dev = s["period_95"] / NOMINAL_PERIOD - 1
        print(f"check: period at 9.5 nA {s['period_95'] * 1e6:.2f} us vs {NOMINAL_PERIOD * 1e6:.2f} us "
              f"from neuron_nominal_tb (20 ns step): {dev * 100:+.2f} %")
    for i, k, r in s["rows"]:
        print(f"  {eng(i, 'A'):>9}  {k:8}  {int(r.get('nspikes') or 0):4d} spikes  "
              f"{eng(r.get('rate'), 'Hz') if k == 'fires' else '':>10}")
    plot()


if __name__ == "__main__":
    main()
