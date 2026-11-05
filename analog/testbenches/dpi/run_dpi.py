"""Run the DPI synapse testbenches and write a report.

    python3 analog/testbenches/dpi/run_dpi.py                 # all suites
    python3 analog/testbenches/dpi/run_dpi.py --quick         # fewer points, 20 MC samples
    python3 analog/testbenches/dpi/run_dpi.py --only nominal,pvt --mc 200 --jobs 8

Writes results/dpi_results.md, one CSV per suite and (if matplotlib is
installed) PNG plots into results/. Each simulation runs in runs/<case>/,
which keeps its netlist, ngspice log and wrdata files.
"""

import argparse
import csv
import datetime
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402

TBS = ["dpi_dc_tb", "dpi_step_tb", "dpi_spike_tb"]
RESULTS = HERE / "results"
RUNS = HERE / "runs"

# Reference operating point. These match the .param defaults in the schematics.
REF = {"vdd": 3.3, "vthr": 2.9, "vtau": 0.40, "iw": 5e-9, "tpw": 100e-6, "rate": 1e3}

# Provisional targets at the reference point. The AI chose these around the
# simulated typical behaviour; they are not project specs. Replace them once
# the synapse requirements are set. (lo, hi); None = no limit.
SPECS = {
    "gain_op": (0.5, 3.0),
    "slope_iw": (0.85, 1.10),
    "i_leak": (None, 20e-12),
    "tau_fall": (0.2e-3, 1e-3),
    "exp_ratio": (0.9, 1.1),
    "settle_err": (None, 0.01),
    "residual": (None, 0.01),
    "vsum_min": (0.5, None),
}

# metric: (description, unit, scale)
METRICS = {
    "isyn_op": ("Isyn at the reference point", "nA", 1e9),
    "gain_op": ("Gain Isyn/Iw, DC", "", 1),
    "ivdd_op": ("Supply current", "nA", 1e9),
    "vsum_op": ("V(Isum), tail node", "V", 1),
    "vsyn_op": ("Vsyn (gate of M4)", "V", 1),
    "slope_iw": ("Log-log slope of Isyn vs Iw, 0.5-50 nA", "", 1),
    "mvdec_vthr": ("Vthr change per decade of Isyn", "mV/dec", 1),
    "mvdec_vtau": ("Vtau change per decade of Isyn", "mV/dec", 1),
    "mvdec_vdd": ("VDD change per decade of Isyn, Vthr fixed", "mV/dec", 1),
    "i_leak": ("Isyn with Iw = 0", "pA", 1e12),
    "i_ss": ("Isyn, steady state", "nA", 1e9),
    "gain": ("Gain Isyn/Iw, step", "", 1),
    "settle_err": ("Change over the last 1 ms of the step (not settled if large)", "", 1),
    "tau_rise": ("Rise time constant (63 %)", "ms", 1e3),
    "t_rise": ("10-90 % rise time", "ms", 1e3),
    "tau_fall": ("Decay time constant (37 %)", "ms", 1e3),
    "exp_ratio": ("Decay shape: 13.5 % time / (2 tau), 1 = exponential", "", 1),
    "residual": ("Isyn 19 ms after release / Isyn at release", "", 1),
    "vsum_min": ("Lowest V(Isum) while Iw is on", "V", 1),
    "ivdd_on": ("Supply current while Iw is on", "nA", 1e9),
    "ipk1": ("Single-spike EPSC peak", "nA", 1e9),
    "q1": ("Charge per spike", "pC", 1e12),
    "dv_mem": ("Same charge as a step on 0.86 pF", "mV", 1e3),
    "tau_epsc": ("EPSC decay time constant", "ms", 1e3),
    "iavg2": ("Mean Isyn, spike train", "nA", 1e9),
    "ripple": ("Train ripple, peak-to-peak / mean", "", 1),
    "lin_rate": ("Train mean / (charge per spike x rate), 1 = linear", "", 1),
    "pk_ratio": ("Train peak / single-spike peak", "", 1),
}


def fmt(key, val):
    if val is None:
        return "n/a"
    scale = METRICS.get(key, ("", "", 1))[2]
    return f"{val * scale:.4g}"


def check(key, val):
    if key not in SPECS:
        return ""
    if val is None:
        return "FAIL"
    lo, hi = SPECS[key]
    ok = (lo is None or val >= lo) and (hi is None or val <= hi)
    return "PASS" if ok else "FAIL"


def spec_text(key):
    lo, hi = SPECS[key]
    unit, scale = METRICS[key][1], METRICS[key][2]
    if lo is None:
        return f"<= {hi * scale:.4g} {unit}".strip()
    if hi is None:
        return f">= {lo * scale:.4g} {unit}".strip()
    return f"{lo * scale:.4g} to {hi * scale:.4g} {unit}".strip()


# ----------------------------------------------------------------------------
# Suites. Each returns a list of cases; the report functions below format them.

def suite_nominal(a):
    return [tb.Case(f"nominal_{t.split('_')[1]}", t) for t in TBS]


def suite_tau(a):
    vals = [0.34, 0.38, 0.42, 0.46] if a.quick else [0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46]
    return [tb.Case(f"tau_{v:.2f}", "dpi_step_tb", params={"vtau": v}, tags={"vtau (V)": v})
            for v in vals]


def suite_vthr(a):
    vals = [2.80, 2.90, 3.00] if a.quick else [2.80, 2.85, 2.90, 2.95, 3.00]
    return [tb.Case(f"vthr_{v:.2f}", "dpi_step_tb", params={"vthr": v}, tags={"vthr (V)": v})
            for v in vals]


def suite_weight(a):
    # 3-bit weight w = 1..7, DAC current w x 1 nA, one reference-width spike
    ws = [1, 3, 5, 7] if a.quick else range(1, 8)
    return [tb.Case(f"weight_{w}", "dpi_spike_tb", params={"iw": f"{w}n"}, tags={"w": w})
            for w in ws]


def suite_width(a):
    widths = [10, 50, 100, 500] if a.quick else [10, 20, 50, 100, 200, 500]
    return [tb.Case(f"width_{w}u", "dpi_spike_tb", params={"tpw": f"{w}u"}, tags={"tpw (us)": w})
            for w in widths]


def suite_rate(a):
    rates = [0.5, 1, 2] if a.quick else [0.25, 0.5, 1, 2, 5]
    return [tb.Case(f"rate_{r}k", "dpi_spike_tb", params={"rate": f"{r}k"}, tags={"rate (kHz)": r})
            for r in rates]


def suite_pvt(a):
    corners = ["tt", "ss", "ff"] if a.quick else ["tt", "ss", "ff", "sf", "fs"]
    cases = []
    for c in corners:
        for t in (0, 27, 85):
            for name in TBS:
                cases.append(tb.Case(f"pvt_{c}_{t}_{name.split('_')[1]}", name, corner=c, temp=t,
                                     tags={"corner": c, "T (C)": t}))
    return cases


def suite_vdd(a):
    cases = []
    for v in (3.0, 3.3, 3.6):
        cases.append(tb.Case(f"vdd_{v}_fixed", "dpi_step_tb", params={"vdd": v},
                             tags={"VDD (V)": v, "Vthr": "2.9 V fixed"}))
        cases.append(tb.Case(f"vdd_{v}_track", "dpi_step_tb",
                             params={"vdd": v, "vthr": round(v - 0.4, 3)},
                             tags={"VDD (V)": v, "Vthr": "VDD - 0.4 V"}))
    return cases


def suite_mc(a):
    n = 20 if a.quick and a.mc is None else (a.mc or 100)
    return [tb.Case(f"mc_{s:03d}", "dpi_step_tb", seed=s, tags={"seed": s}) for s in range(1, n + 1)]


SUITES = {
    "nominal": suite_nominal,
    "tau": suite_tau,
    "vthr": suite_vthr,
    "weight": suite_weight,
    "width": suite_width,
    "rate": suite_rate,
    "pvt": suite_pvt,
    "vdd": suite_vdd,
    "mc": suite_mc,
}


# ----------------------------------------------------------------------------
# Report

def table(cases, keys):
    """Markdown table: tag columns, then the chosen metrics."""
    tags = list(cases[0].tags)
    head = tags + [f"{k} ({METRICS[k][1]})" if METRICS[k][1] else k for k in keys]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for c in cases:
        cells = [str(c.tags[t]) for t in tags]
        cells += [fmt(k, c.results.get(k)) if c.ok else "sim failed" for k in keys]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def write_csv(name, cases):
    keys = sorted({k for c in cases for k in c.results})
    with open(RESULTS / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case", "ok"] + list(cases[0].tags) + keys)
        for c in cases:
            w.writerow([c.name, c.ok] + [c.tags[t] for t in c.tags] +
                       [c.results.get(k, "") for k in keys])


def report_nominal(cases):
    lines = ["## Nominal (tt, 27 C, reference bias)", "",
             "| Metric | Value | Unit | Target | Check |", "|---|---|---|---|---|"]
    for c in cases:
        if not c.ok:
            lines.append(f"| {c.tb} | simulation failed, see runs/{c.name}/ngspice.log | | | |")
            continue
        for k, v in c.results.items():
            desc, unit, _ = METRICS.get(k, (k, "", 1))
            target = spec_text(k) if k in SPECS else ""
            lines.append(f"| {desc} (`{k}`) | {fmt(k, v)} | {unit} | {target} | {check(k, v)} |")
    return "\n".join(lines)


def report_weight(cases):
    q1 = {c.tags["w"]: c.results.get("q1") for c in cases if c.ok}
    base = q1.get(1) or None
    for c in cases:
        q = c.results.get("q1")
        c.tags["q / (w x q at w=1)"] = (f"{q / (c.tags['w'] * base):.3g}"
                                       if (q and base) else "n/a")
    return table(cases, ["ipk1", "q1", "dv_mem", "iavg2", "lin_rate"])


def report_width(cases):
    for c in cases:
        q = c.results.get("q1")
        qin = REF["iw"] * c.tags["tpw (us)"] * 1e-6
        c.tags["charge in (pC)"] = f"{qin * 1e12:.3g}"
        c.tags["charge out / in"] = f"{q / qin:.3g}" if q else "n/a"
    return table(cases, ["ipk1", "q1", "dv_mem", "tau_epsc"])


def report_pvt(cases):
    rows = {}
    for c in cases:
        key = (c.corner, c.temp)
        rows.setdefault(key, tb.Case(f"{c.corner}_{c.temp}", "", tags=dict(c.tags), ok=True))
        if c.ok:
            rows[key].results.update(c.results)
    merged = list(rows.values())
    for m in merged:
        err = m.results.get("settle_err")
        m.tags["settled"] = "yes" if err is not None and err < 0.01 else "NO"
    return table(merged, ["gain_op", "i_ss", "tau_fall", "tau_rise", "slope_iw",
                          "i_leak", "q1", "lin_rate"])


def report_mc(cases):
    lines = ["| Metric | Mean | Std dev | Std/mean | Min | Max | Unit |", "|---|---|---|---|---|---|---|"]
    good = [c for c in cases if c.ok]
    for k in ["i_ss", "gain", "tau_fall", "tau_rise"]:
        vals = [c.results[k] for c in good if c.results.get(k) is not None]
        if len(vals) < 2:
            continue
        mu, sd = statistics.mean(vals), statistics.stdev(vals)
        lines.append(f"| {METRICS[k][0]} | {fmt(k, mu)} | {fmt(k, sd)} | {sd / mu:.2f} | "
                     f"{fmt(k, min(vals))} | {fmt(k, max(vals))} | {METRICS[k][1]} |")
    lines.append("")
    lines.append(f"{len(good)} of {len(cases)} samples simulated (tt, 27 C, mismatch only).")
    return "\n".join(lines)


def plots(done):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return ["(matplotlib not installed: no plots)"]
    made = []

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(RESULTS / name, dpi=120)
        plt.close(fig)
        made.append(name)

    if "nominal" in done:
        d = RUNS / "nominal_dc"
        if (d / "dpi_dc_iw.txt").exists():
            fig, ax = plt.subplots(2, 2, figsize=(10, 7))
            iw = tb.read_wrdata(d / "dpi_dc_iw.txt")
            ax[0, 0].loglog(iw["iw"], iw["isyn"], label="Isyn")
            ax[0, 0].loglog(iw["iw"], iw["iw"], "--", color="gray", label="Isyn = Iw")
            ax[0, 0].set(xlabel="Iw (A)", ylabel="Isyn (A)", title="Isyn vs Iw")
            ax[0, 0].legend()
            for axis, f, xl in [(ax[0, 1], "vthr", "Vthr (V)"), (ax[1, 0], "vtau", "Vtau = Vsg(M3) (V)"),
                                (ax[1, 1], "vdd", "VDD (V), Vthr fixed")]:
                cols = tb.read_wrdata(d / f"dpi_dc_{f}.txt")
                x = cols[list(cols)[0]]
                axis.semilogy(x, cols["isyn"])
                axis.set(xlabel=xl, ylabel="Isyn (A)", title=f"Isyn vs {xl.split()[0]}")
            for a_ in ax.flat:
                a_.grid(True, which="both", alpha=0.3)
            save(fig, "dpi_dc.png")
        d = RUNS / "nominal_step"
        if (d / "dpi_step.txt").exists():
            s = tb.read_wrdata(d / "dpi_step.txt")
            fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
            t = [x * 1e3 for x in s["time"]]
            ax[0].plot(t, [x * 1e9 for x in s["isyn"]])
            ax[0].set(ylabel="Isyn (nA)", title=f"Step response, Iw = {REF['iw'] * 1e9:g} nA from 1 to 11 ms")
            ax[1].plot(t, s["v(isum)"], label="V(Isum)")
            ax[1].plot(t, s["v(x1.net1)"], label="Vsyn")
            ax[1].set(xlabel="t (ms)", ylabel="V")
            ax[1].legend()
            for a_ in ax:
                a_.grid(alpha=0.3)
            save(fig, "dpi_step.png")
        d = RUNS / "nominal_spike"
        if (d / "dpi_spike.txt").exists():
            s = tb.read_wrdata(d / "dpi_spike.txt")
            fig, ax = plt.subplots(figsize=(8, 4))
            t = [x * 1e3 for x in s["time"]]
            ax.plot(t, [x * 1e9 for x in s["isyn2"]], label=f"train, {REF['rate'] / 1e3:g} kHz")
            ax.plot(t, [x * 1e9 for x in s["isyn1"]], label="single spike at 1 ms")
            ax.set(xlabel="t (ms)", ylabel="Isyn (nA)",
                   title=f"Spikes: Iw = {REF['iw'] * 1e9:g} nA, width {REF['tpw'] * 1e6:g} us")
            ax.legend()
            ax.grid(alpha=0.3)
            save(fig, "dpi_spike.png")

    def xy(cases, tag, key):
        pts = [(c.tags[tag], c.results.get(key)) for c in cases if c.ok and c.results.get(key)]
        return [p[0] for p in pts], [p[1] for p in pts]

    if "tau" in done:
        x, y = xy(done["tau"], "vtau (V)", "tau_fall")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.semilogy(x, [v * 1e3 for v in y], "o-")
        ax.set(xlabel="Vtau = Vsg(M3) (V)", ylabel="tau decay (ms)", title="Decay time constant vs Vtau")
        ax.grid(True, which="both", alpha=0.3)
        save(fig, "dpi_tau_vs_vtau.png")
    if "weight" in done:
        x, y = xy(done["weight"], "w", "q1")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.semilogy(x, [v * 1e12 for v in y], "o-", label="simulated")
        if y:
            ax.semilogy(x, [w * y[0] * 1e12 / x[0] for w in x], "--", color="gray", label="linear in w")
        ax.set(xlabel="weight w (Iw = w x 1 nA)", ylabel="charge per spike (pC)",
               title=f"Charge per spike vs weight, width {REF['tpw'] * 1e6:g} us")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        save(fig, "dpi_weight.png")
    if "mc" in done:
        good = [c for c in done["mc"] if c.ok]
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        g = [c.results["gain"] for c in good if c.results.get("gain")]
        tf = [c.results["tau_fall"] * 1e3 for c in good if c.results.get("tau_fall")]
        ax[0].hist(g, bins=20)
        ax[0].set(xlabel="gain Isyn/Iw", ylabel="samples", title="Mismatch: gain")
        ax[1].hist(tf, bins=20)
        ax[1].set(xlabel="tau decay (ms)", title="Mismatch: tau decay")
        save(fig, "dpi_mc.png")
    return made


def tool_version(cmd):
    try:
        p = subprocess.run([f"{tb.TOOLS_BIN}/{cmd}", "--version"], capture_output=True, text=True)
        lines = [s.strip("* ") for s in (p.stdout + p.stderr).splitlines() if cmd in s.lower()]
        return lines[0] if lines else "unknown"
    except OSError:
        return "unknown"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--quick", action="store_true", help="fewer sweep points and 20 MC samples")
    ap.add_argument("--mc", type=int, help="number of mismatch samples (default 100)")
    ap.add_argument("--jobs", type=int, default=4, help="parallel ngspice runs")
    a = ap.parse_args()

    names = a.only.split(",") if a.only else list(SUITES)
    for n in names:
        if n not in SUITES:
            ap.error(f"unknown suite {n}")

    RESULTS.mkdir(exist_ok=True)
    print("Netlisting with xschem ...")
    netlists = {t: tb.netlist(HERE / f"{t}.sch", RUNS / "_netlists").read_text() for t in TBS}
    for text in netlists.values():
        tb.check_connected(text, "DPI")

    done = {}
    for n in names:
        cases = SUITES[n](a)
        print(f"Running {n}: {len(cases)} simulations")
        done[n] = tb.run_cases(cases, netlists, RUNS, a.jobs)
        bad = [c.name for c in done[n] if not c.ok]
        if bad:
            print(f"  failed: {', '.join(bad)}")
        write_csv(n, done[n])

    sections = {
        "nominal": lambda c: report_nominal(c),
        "tau": lambda c: "## Decay time constant vs Vtau (step test)\n\n" +
                         table(c, ["tau_fall", "tau_rise", "gain", "i_ss", "settle_err"]),
        "vthr": lambda c: "## Gain vs Vthr (step test)\n\n" +
                          table(c, ["gain", "i_ss", "tau_fall", "tau_rise", "vsum_min"]),
        "weight": lambda c: f"## Single spike vs weight (Iw = w x 1 nA, width {REF['tpw'] * 1e6:g} us)\n\n"
                            "The last tag column is 1 when the charge per spike is proportional to w.\n\n" +
                            report_weight(c),
        "width": lambda c: f"## Single spike vs pulse width (Iw = {REF['iw'] * 1e9:g} nA)\n\n" +
                           report_width(c),
        "rate": lambda c: f"## Spike train vs rate (Iw = {REF['iw'] * 1e9:g} nA, width {REF['tpw'] * 1e6:g} us)\n\n" +
                          table(c, ["iavg2", "ripple", "lin_rate", "pk_ratio"]),
        "pvt": lambda c: "## Process corners and temperature (reference bias)\n\n" + report_pvt(c),
        "vdd": lambda c: "## Supply (step test)\n\n" + table(c, ["i_ss", "gain", "tau_fall", "settle_err"]),
        "mc": lambda c: "## Device mismatch (step test)\n\n" + report_mc(c),
    }

    made = plots(done)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ref = ", ".join(f"{k} = {v:g}" for k, v in REF.items())
    md = [f"# DPI synapse testbench results",
          "",
          f"Generated by `run_dpi.py` on {now} ({tool_version('ngspice')}). "
          f"Suites: {', '.join(names)}{' (quick)' if a.quick else ''}.",
          "",
          f"Reference bias: {ref} (SI units). Targets marked *Check* are provisional; "
          "see `SPECS` in `run_dpi.py`.",
          ""]
    for n in names:
        md += [sections[n](done[n]), ""]
    if made:
        md += ["## Plots", ""] + [f"![{m}]({m})" for m in made] + [""]
    (RESULTS / "dpi_results.md").write_text("\n".join(md))
    print(f"Report: {RESULTS / 'dpi_results.md'}")

    fails = [k for c in done.get("nominal", []) for k, v in c.results.items() if check(k, v) == "FAIL"]
    if fails:
        print("Nominal checks failing: " + ", ".join(fails))


if __name__ == "__main__":
    main()
