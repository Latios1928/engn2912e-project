"""neuron_sized driven by square current pulses (neuron_pulse_tb.sch).

    python3 analog/testbenches/neuron/run_neuron_pulse.py               # schematic neuron
    python3 analog/testbenches/neuron/run_neuron_pulse.py --pex         # post-layout neuron
    python3 analog/testbenches/neuron/run_neuron_pulse.py --only charge,refractory
    python3 analog/testbenches/neuron/run_neuron_pulse.py --report-only # rebuild report from runs/

Run inside the container. Three suites, each point in runs/pulse_<sch|pex>_<suite>_<x>/:

  charge      10 us pulses every 200 us (the network's 5 kHz input rate), amplitude
              5 nA-400 nA, so the charge per pulse q spans 0.05-4 pC. How many pulses
              fire the neuron, against the ideal ceil(Q/q), Q = C VT ~ 1.66 pC.
  interval    20 nA x 10 us pulses (q = 0.2 pC, ideal 9 pulses per spike), one every
              15 us to 5 ms. How the leak between pulses raises the count, and the
              longest interval that still fires.
  refractory  200 nA x 10 us pulses (q = 2 pC, more than Q: every pulse should fire), one
              every 12 to 60 us (200 nA: below the current that overdrives the reset). Pulses that land in the refractory period after a spike
              are lost: output spikes per input pulse drops below 1.

Writes results/neuron_pulse_tb[__pex].md / .csv and results/neuron_pulse_tb.png
(schematic and post-layout overlaid when both exist).
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

TB = "neuron_pulse_tb"
CELL = "neuron_sized"
RESULTS = HERE / "results"
RUNS = HERE / "runs"

C_MEM, V_T = 1e-12, 1.66
Q_IDEAL = C_MEM * V_T          # charge to reach threshold from 0 V, no leak
I_LEAK_GUESS = 0.5e-9          # for the run-length estimate only
T0 = 50e-6

SUITES = {
    # suite: (fixed settings, swept key, values)
    "charge": ({"tpw": 10e-6, "tper": 200e-6}, "ipk",
               [5e-9, 10e-9, 15e-9, 20e-9, 30e-9, 50e-9, 80e-9, 120e-9, 166e-9, 250e-9, 400e-9]),
    "interval": ({"ipk": 20e-9, "tpw": 10e-6}, "tper",
                 [15e-6, 25e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3]),
    # 200 nA stays below the ~500 nA at which the input overdrives the reset
    # (run_neuron_rate.py); a stronger pulse would fire through the refractory period.
    "refractory": ({"ipk": 200e-9, "tpw": 10e-6}, "tper",
                   [12e-6, 16e-6, 20e-6, 24e-6, 28e-6, 32e-6, 40e-6, 60e-6]),
}
# Nominal schematic timing (neuron_nominal_tb): spike width + refractory time
T_DEAD_NOMINAL = 9.20e-6 + 14.61e-6


def tstop_for(suite, ipk, tpw, tper):
    if suite == "refractory":
        return max(1e-3, T0 + 60 * tper)
    qnet = ipk * tpw - I_LEAK_GUESS * tper
    if qnet <= 0.05 * ipk * tpw:
        return 40e-3
    n_est = math.ceil(Q_IDEAL / qnet)
    return min(max(T0 + tper * (4 * n_est + 3), 2e-3), 40e-3)


def label(x):
    return f"{x:.4g}".replace(".", "p").replace("-", "m").replace("+", "")


def cases_for(suite, variant, tmax):
    fixed, key, values = SUITES[suite]
    out = []
    for v in values:
        s = dict(fixed, **{key: v})
        out.append(tb.Case(
            name=f"pulse_{variant}_{suite}_{label(v)}", tb=TB,
            params={"p_ipk": f"{s['ipk']:.6g}", "p_tpw": f"{s['tpw']:.6g}", "p_tper": f"{s['tper']:.6g}",
                    "p_t0": f"{T0:.6g}", "p_tstop": f"{tstop_for(suite, **s):.4g}", "p_tmax": f"{tmax:.3g}"},
            tags={"suite": suite}))
    return out


def ideal_n(q):
    return math.ceil(Q_IDEAL / q - 1e-9)


def row(c):
    r = c.results
    q = r.get("q") or 0
    n = int(r.get("nspikes") or 0)
    n_in = int(r.get("n_in") or 0)
    return {
        "suite": c.tags["suite"], "ipk": r.get("ipk"), "tpw": r.get("tpw"), "tper": r.get("tper"),
        "q": q, "ideal_n": ideal_n(q) if q > 0 else None, "n_in": n_in, "nspikes": n,
        "n_first": int(r.get("n_first") or 0) if n else None,
        "n_per": r.get("n_per") if n >= 2 else None,
        "spikes_per_pulse": n / n_in if n_in else None,
        "dv1": r.get("dv1"), "droop1": r.get("droop1"), "c_eff": r.get("c_eff") or None,
        "ok": c.ok,
    }


def eng(x, unit, digits=4):
    if x is None:
        return "-"
    for f, p in ((1e-15, "f"), (1e-12, "p"), (1e-9, "n"), (1e-6, "u"), (1e-3, "m"), (1, "")):
        if abs(x) < f * 1000:
            return f"{x / f:.{digits}g} {p}{unit}"
    return f"{x:.{digits}g} {unit}"


def num(x, fmt="{:.3g}"):
    return "-" if x is None else fmt.format(x)


def write_csv(path, rows):
    keys = ["suite", "ipk", "tpw", "tper", "q", "ideal_n", "n_in", "nspikes", "n_first", "n_per",
            "spikes_per_pulse", "dv1", "droop1", "c_eff", "ok"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r[k] is None else r[k]) for k in keys})


def write_md(path, rows, variant, note, tmax):
    by = {s: [r for r in rows if r["suite"] == s] for s in SUITES}
    L = [f"# {TB}{'__pex' if variant == 'pex' else ''}: neuron driven by current pulses", "",
         f"Generated by `run_neuron_pulse.py{' --pex' if variant == 'pex' else ''}` on "
         f"{datetime.datetime.now():%Y-%m-%d %H:%M}. Neuron: "
         + ("post-layout extraction (" + note + ")" if variant == "pex" else "schematic `neuron_sized.sch`")
         + f". tt, 27 C, VDD 3.3 V, biases as in `neuron_nominal_tb`, first pulse at {eng(T0, 's')}, "
         f"maximum time step {eng(tmax, 's')}.", "",
         f"Ideal reference: an integrate-and-fire neuron with no leak, reset to 0, needs "
         f"ceil(Q/q) pulses per spike, Q = C VT = 1 pF x 1.66 V = {eng(Q_IDEAL, 'C')}.", ""]
    ceff = [r["c_eff"] for r in rows if r["c_eff"] and r["suite"] == "charge" and r["n_first"] != 1]
    if ceff:
        L += [f"Effective membrane capacitance from the VMEM step of pulse 1 (q / step): "
              f"{eng(min(ceff), 'F')} to {eng(max(ceff), 'F')} (1 pF MIM plus device and wiring "
              f"capacitance on VMEM).", ""]
    if by["charge"]:
        fire = [r for r in by["charge"] if r["nspikes"]]
        L += ["## Charge per pulse (10 us pulses every 200 us)", ""]
        if fire:
            L += [f"Smallest charge per pulse that fires: {eng(fire[0]['q'], 'C')} "
                  f"({eng(fire[0]['ipk'], 'A')} pulses). ", ""]
        L += ["| Pulse | q | ideal pulses/spike | first spike after pulse | pulses/spike after | VMEM step, pulse 1 | droop to pulse 2 |",
              "|---|---|---|---|---|---|---|"]
        for r in by["charge"]:
            L.append(f"| {eng(r['ipk'], 'A')} | {eng(r['q'], 'C')} | {num(r['ideal_n'], '{}')} | "
                     f"{num(r['n_first'], '{}') if r['nspikes'] else 'never'} | {num(r['n_per'], '{:.2f}')} | "
                     f"{eng(r['dv1'], 'V', 3)} | {eng(r['droop1'], 'V', 3)} |")
        L.append("")
    if by["interval"]:
        fire = [r for r in by["interval"] if r["nspikes"]]
        L += ["## Interval between pulses (20 nA x 10 us, q = 0.2 pC, ideal 9 pulses)", ""]
        if fire:
            L += [f"Longest interval that still fires: {eng(max(r['tper'] for r in fire), 's')}.", ""]
        L += ["| Interval | average current | first spike after pulse | pulses/spike after | droop to pulse 2 |",
              "|---|---|---|---|---|"]
        for r in by["interval"]:
            L.append(f"| {eng(r['tper'], 's')} | {eng(r['q'] / r['tper'], 'A', 3)} | "
                     f"{num(r['n_first'], '{}') if r['nspikes'] else 'never'} | {num(r['n_per'], '{:.2f}')} | "
                     f"{eng(r['droop1'], 'V', 3)} |")
        L.append("")
    if by["refractory"]:
        full = [r for r in by["refractory"] if (r["spikes_per_pulse"] or 0) >= 0.95]
        L += ["## Pulses inside the refractory period (200 nA x 10 us, q = 2 pC > Q)", ""]
        if full:
            L += [f"Shortest interval at which every pulse fires: {eng(min(r['tper'] for r in full), 's')} "
                  f"(nominal spike width + refractory time: {eng(T_DEAD_NOMINAL, 's')}).", ""]
        L += ["| Interval | input pulses | output spikes | spikes per pulse |", "|---|---|---|---|"]
        for r in by["refractory"]:
            L.append(f"| {eng(r['tper'], 's')} | {r['n_in']} | {r['nspikes']} | {num(r['spikes_per_pulse'], '{:.2f}')} |")
        L.append("")
    bad = [r for r in rows if not r["ok"]]
    if bad:
        L += [f"Failed simulations: {len(bad)} (see `runs/`)."]
    L += [f"Plot: `{TB}.png`. Per-point netlists, logs and waveforms: `runs/pulse_{variant}_*/`."]
    path.write_text("\n".join(L) + "\n")


def plot():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: no plot")
        return
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    series = [("sch", "Schematic", "#2a78d6", "o"), ("pex", "Post-layout (PEX)", "#eb6834", "s")]
    data = {}
    for variant, *_ in series:
        p = RESULTS / f"{TB}{'__pex' if variant == 'pex' else ''}.csv"
        if p.exists():
            with open(p) as f:
                data[variant] = [{k: (float(v) if v not in ("", "True", "False") and k != "suite" else v)
                                  for k, v in r.items()} for r in csv.DictReader(f)]
    if not data:
        return
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.6), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(True, color=grid, lw=0.8)
        for sp in ax.spines.values():
            sp.set_color(grid)
        ax.tick_params(colors=ink2)

    a = axs[0]
    qs = [x * 1e-13 for x in range(4, 450)]
    a.plot([q * 1e12 for q in qs], [ideal_n(q) for q in qs], color=ink2, lw=1, ls="--",
           drawstyle="steps-post", label="ideal ceil(Q/q)")
    for variant, label_, color, marker in series:
        rs = [r for r in data.get(variant, []) if r["suite"] == "charge" and r["n_per"] != ""]
        if rs:
            a.plot([r["q"] * 1e12 for r in rs], [r["n_per"] for r in rs], color=color, lw=2,
                   marker=marker, ms=6, mec=surf, mew=1.5, label=label_)
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlabel("Charge per pulse q (pC)", color=ink2)
    a.set_ylabel("Input pulses per output spike", color=ink2)
    a.set_title("Pulses to fire vs charge\n10 us pulses every 200 us", color=ink, loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8)

    a = axs[1]
    a.axhline(ideal_n(0.2e-12), color=ink2, lw=1, ls="--", label="ideal (no leak)")
    for variant, label_, color, marker in series:
        rs = [r for r in data.get(variant, []) if r["suite"] == "interval" and r["n_first"] != ""]
        if rs:
            a.plot([r["tper"] * 1e6 for r in rs], [r["n_first"] for r in rs], color=color, lw=2,
                   marker=marker, ms=6, mec=surf, mew=1.5, label=label_)
    a.set_xscale("log")
    a.set_xlabel("Time between pulses (us)", color=ink2)
    a.set_ylabel("Pulse that first fires the neuron", color=ink2)
    a.set_title("Leak between pulses\n20 nA x 10 us pulses (q = 0.2 pC)", color=ink, loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8)

    a = axs[2]
    a.axvline(T_DEAD_NOMINAL * 1e6, color=ink2, lw=1, ls=":")
    a.annotate("spike width + refractory\n(nominal, schematic)", (T_DEAD_NOMINAL * 1e6, 0.05),
               xytext=(4, 0), textcoords="offset points", fontsize=8, color=ink2)
    for variant, label_, color, marker in series:
        rs = [r for r in data.get(variant, []) if r["suite"] == "refractory" and r["spikes_per_pulse"] != ""]
        if rs:
            a.plot([r["tper"] * 1e6 for r in rs], [r["spikes_per_pulse"] for r in rs], color=color, lw=2,
                   marker=marker, ms=6, mec=surf, mew=1.5, label=label_)
    a.set_ylim(0, 1.1)
    a.set_xlabel("Time between pulses (us)", color=ink2)
    a.set_ylabel("Output spikes per input pulse", color=ink2)
    a.set_title("Pulses lost in the refractory period\n200 nA x 10 us pulses (q = 2 pC > Q)", color=ink,
                loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8, loc="lower right")

    fig.suptitle("neuron_sized driven by current pulses (tt, 27 C)", color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{TB}.png", dpi=150, facecolor=surf)
    plt.close(fig)
    print(f"wrote {RESULTS / (TB + '.png')}")


def report(done, variant, note, tmax):
    order = list(SUITES)
    done = sorted(done, key=lambda c: (order.index(c.tags["suite"]),
                                        c.results.get("ipk") or 0, c.results.get("tper") or 0))
    rows = [row(c) for c in done]
    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}{'__pex' if variant == 'pex' else ''}"
    write_csv(RESULTS / f"{stem}.csv", rows)
    write_md(RESULTS / f"{stem}.md", rows, variant, note, tmax)
    print(f"wrote {RESULTS / (stem + '.md')} and .csv")
    for r in rows:
        print(f"  {r['suite']:10} q {eng(r['q'], 'C'):>9}  tper {eng(r['tper'], 's'):>9}  "
              f"{r['nspikes']:4d}/{r['n_in']:<4d} spikes/pulses  first after {num(r['n_first'], '{}'):>5}  "
              f"per spike {num(r['n_per'], '{:.2f}'):>6}  (ideal {num(r['ideal_n'], '{}')})")
    plot()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of the neuron")
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--jobs", type=int, default=4, help="parallel ngspice runs (one thread each)")
    ap.add_argument("--tmax", type=float, default=100e-9, help="maximum time step (s)")
    ap.add_argument("--report-only", action="store_true",
                    help="no simulation: rebuild the report from the runs already in runs/")
    a = ap.parse_args()
    variant = "pex" if a.pex else "sch"
    suites = a.only.split(",") if a.only else list(SUITES)
    for s in suites:
        if s not in SUITES:
            raise SystemExit(f"unknown suite {s}; choose from {','.join(SUITES)}")

    if a.report_only:
        done = []
        for log in sorted(RUNS.glob(f"pulse_{variant}_*/ngspice.log")):
            suite = log.parent.name.split("_")[2]
            if suite not in suites:
                continue
            c = tb.Case(name=log.parent.name, tb=TB, tags={"suite": suite})
            c.log = log.read_text()
            c.results = tb.parse_results(c.log)
            c.ok = bool(c.results) and "aborted" not in c.log
            if c.results.get("q"):
                done.append(c)
        if not done:
            raise SystemExit(f"no runs in {RUNS}/pulse_{variant}_*")
        report(done, variant, tbpex.pex_note((RUNS / done[0].name / f"{TB}.spice").read_text()) if a.pex else "", a.tmax)
        return

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / f"netlist_pulse_{variant}").read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    tb.check_connected(text, CELL)
    note = ""
    if a.pex:
        text = tbpex.use_pex(text, CELL)
        note = tbpex.pex_note(text)

    cases = [c for s in suites for c in cases_for(s, variant, a.tmax)]
    print(f"{variant}: {len(cases)} points ({', '.join(suites)}), {a.jobs} at a time")
    done = tb.run_cases(cases, {TB: text}, RUNS, jobs=a.jobs)
    bad = [c.name for c in done if not c.ok]
    if bad:
        print("simulations that failed (see runs/<name>/ngspice.log):", ", ".join(bad))
    report(done, variant, note, a.tmax)


if __name__ == "__main__":
    main()
