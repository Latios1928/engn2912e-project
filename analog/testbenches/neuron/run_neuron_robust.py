"""Robustness of neuron_sized: neuron_nominal_tb.sch under PVT, supply, bias and mismatch.

    python3 analog/testbenches/neuron/run_neuron_robust.py                  # all suites, schematic
    python3 analog/testbenches/neuron/run_neuron_robust.py --pex            # post-layout neuron
    python3 analog/testbenches/neuron/run_neuron_robust.py --only pvt,bias
    python3 analog/testbenches/neuron/run_neuron_robust.py --mc 200 --jobs 8
    python3 analog/testbenches/neuron/run_neuron_robust.py --quick          # 20 mismatch samples
    python3 analog/testbenches/neuron/run_neuron_robust.py --report-only    # rebuild from runs/

Run inside the container. Uses the nominal testbench (9.5 nA DC into VMEM; period,
spike width, refractory time, spike peak, reset level and power on spikes 3-7) and
checks the six specs of analog/neuron/sizing_context.txt here, with the spike peak
limit at 0.9 VDD. Each run lasts 5 ms instead of 1.8 ms so that slow corners still
give the 7 spikes the measurements need. Suites:

  pvt   corners tt/ss/ff/sf/fs x 0/27/85 C                                 (15 runs)
  vdd   VDD 3.0/3.3/3.6 V, the PMOS biases (VNA, VKup) either fixed or moved
        with VDD (a bias generator referenced to VDD would do the latter)    (6 runs)
  bias  each bias voltage +-10 mV: sensitivity of every spec, and how many mV
        of drift each bias tolerates before a spec fails                    (16 runs)
  mc    device mismatch, tt 27 C, --mc samples (default 100): spread and yield

The specs are defined at tt, 27 C; the other conditions show how far the design
moves, with fixed bias voltages. Each run is in runs/robust_<sch|pex>_<suite>_<x>/.
Writes, in results/ (post-layout runs add __pex):
  neuron_nominal_tb__robust[__pex].md / .csv    report and every run
  neuron_nominal_tb__robust[__pex]_pvt.png      period, spike width, refractory vs T per corner
  neuron_nominal_tb__robust[__pex]_mc.png       mismatch histograms with the spec limits
"""

import argparse
import csv
import datetime
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402
import tbpex  # noqa: E402

TB = "neuron_nominal_tb"
CELL = "neuron_sized"
RESULTS = HERE / "results"
RUNS = HERE / "runs"
TSTOP = 5e-3

# .param defaults of neuron_nominal_tb.sch
NOM = {"p_vdd": 3.3, "p_iin": 9.5e-9, "p_vlk": 0.425, "p_vamp": 0.535, "p_vip": 0.573,
       "p_vna": 1.93, "p_vkup": 2.35, "p_vk": 1.22, "p_vkdn": 0.588, "p_vt": 1.66}
BIASES = ["p_vlk", "p_vamp", "p_vip", "p_vna", "p_vkup", "p_vk", "p_vkdn", "p_vt"]
BIAS_STEP = 0.010

# sizing_context.txt; v_spike_max's limit is 0.9 VDD (2.97 V at 3.3 V)
METRICS = ["period", "t_spike", "t_refr", "v_spike_max", "v_reset", "p_avg"]
UNITS = {"period": ("us", 1e6), "t_spike": ("us", 1e6), "t_refr": ("us", 1e6),
         "v_spike_max": ("V", 1), "v_reset": ("mV", 1e3), "p_avg": ("uW", 1e6)}


def limits(m, vdd):
    return {"period": (190e-6, 210e-6), "t_spike": (9e-6, 11e-6), "t_refr": (12e-6, 15e-6),
            "v_spike_max": (0.9 * vdd, None), "v_reset": (None, 0.05), "p_avg": (None, 1e-6)}[m]


def passes(m, v, vdd):
    if v is None:
        return False
    lo, hi = limits(m, vdd)
    return (lo is None or v >= lo) and (hi is None or v <= hi)


def fmt(m, v):
    if v is None:
        return "-"
    unit, k = UNITS[m]
    return f"{v * k:.4g}"


def case(variant, suite, label, corner="tt", temp=27, params=None, seed=None, tags=None):
    p = {"p_tstop": f"{TSTOP:g}"}
    p.update({k: f"{v:.6g}" for k, v in (params or {}).items()})
    t = {"suite": suite, "label": label, "corner": corner, "temp": temp, "seed": seed,
         "vdd": float(p.get("p_vdd", NOM["p_vdd"]))}
    t.update(tags or {})
    return tb.Case(name=f"robust_{variant}_{suite}_{label}", tb=TB, corner=corner, temp=temp,
                   params=p, seed=seed, tags=t)


def suite_pvt(v, a):
    return [case(v, "pvt", f"{c}_{t}C", corner=c, temp=t)
            for c in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]


def suite_vdd(v, a):
    out = []
    for vdd in (3.0, 3.3, 3.6):
        d = vdd - NOM["p_vdd"]
        out.append(case(v, "vdd", f"{vdd:g}V_fixed".replace(".", "p"), params={"p_vdd": vdd},
                        tags={"pmos_bias": "fixed"}))
        out.append(case(v, "vdd", f"{vdd:g}V_track".replace(".", "p"),
                        params={"p_vdd": vdd, "p_vna": NOM["p_vna"] + d, "p_vkup": NOM["p_vkup"] + d},
                        tags={"pmos_bias": "tracks VDD"}))
    return out


def suite_bias(v, a):
    out = [case(v, "bias", "nominal", tags={"bias": "", "delta": 0.0})]
    for b in BIASES:
        for sgn in (+1, -1):
            d = sgn * BIAS_STEP
            out.append(case(v, "bias", f"{b}_{'p' if sgn > 0 else 'm'}{abs(d) * 1e3:g}mV",
                            params={b: NOM[b] + d}, tags={"bias": b, "delta": d}))
    return out


def suite_mc(v, a):
    n = 20 if a.quick and not a.mc else (a.mc or 100)
    return [case(v, "mc", f"seed{s}", seed=s) for s in range(1, n + 1)]


SUITES = {"pvt": suite_pvt, "vdd": suite_vdd, "bias": suite_bias, "mc": suite_mc}


def save_tags(c):
    d = RUNS / c.name
    if d.exists():
        (d / "case.json").write_text(json.dumps({"tags": c.tags, "corner": c.corner, "temp": c.temp,
                                                 "seed": c.seed, "params": c.params}))


def load_runs(variant, suites):
    done = []
    for j in sorted(RUNS.glob(f"robust_{variant}_*/case.json")):
        info = json.loads(j.read_text())
        if info["tags"]["suite"] not in suites:
            continue
        c = tb.Case(name=j.parent.name, tb=TB, corner=info["corner"], temp=info["temp"],
                    params=info["params"], seed=info["seed"], tags=info["tags"])
        log = j.parent / "ngspice.log"
        c.log = log.read_text() if log.exists() else ""
        c.results = tb.parse_results(c.log)
        c.ok = bool(c.results) and "aborted" not in c.log
        done.append(c)
    return done


def row(c):
    r = c.results
    vdd = c.tags["vdd"]
    fired = bool(r.get("fired7"))
    vals = {m: (r.get(m) if fired else None) for m in METRICS}
    ok = {m: passes(m, vals[m], vdd) for m in METRICS}
    return {"case": c, "fired": fired, "vals": vals, "ok": ok, "all_ok": fired and all(ok.values()),
            "sim_ok": c.ok}


def table(rows, first_cols, first_vals):
    hdr = first_cols + ["fires"] + [f"{m} ({UNITS[m][0]})" for m in METRICS] + ["all specs"]
    L = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for r, fv in zip(rows, first_vals):
        cells = fv + ["yes" if r["fired"] else "**no**"]
        for m in METRICS:
            s = fmt(m, r["vals"][m])
            cells.append(s if r["ok"][m] or r["vals"][m] is None else f"**{s}**")
        cells.append("PASS" if r["all_ok"] else "**FAIL**")
        L.append("| " + " | ".join(cells) + " |")
    return L


def write_md(path, by, variant, note):
    L = [f"# {TB}__robust{'__pex' if variant == 'pex' else ''}: neuron robustness", "",
         f"Generated by `run_neuron_robust.py{' --pex' if variant == 'pex' else ''}` on "
         f"{datetime.datetime.now():%Y-%m-%d %H:%M}. Neuron: "
         + ("post-layout extraction (" + note + ")" if variant == "pex" else "schematic `neuron_sized.sch`")
         + f". Testbench `{TB}` (9.5 nA DC), runs of {TSTOP * 1e3:g} ms, bias voltages fixed unless stated.",
         "",
         "Specs (`analog/neuron/sizing_context.txt`, defined at tt 27 C): period 190-210 us, "
         "t_spike 9-11 us, t_refr 12-15 us, v_spike_max >= 0.9 VDD, v_reset <= 50 mV, p_avg <= 1 uW. "
         "Bold: outside the spec. *fires* = at least 7 spikes in the run (needed for the measurements).", ""]
    if by.get("pvt"):
        rs = by["pvt"]
        n_ok = sum(r["all_ok"] for r in rs)
        dead = [f"{r['case'].corner} {r['case'].temp:g} C" for r in rs if not r["fired"]]
        L += ["## Process corners and temperature", "",
              f"{n_ok} of {len(rs)} conditions meet all specs. "
              + (f"Does not fire: {', '.join(dead)}." if dead else "Fires everywhere."), ""]
        L += table(rs, ["corner", "T (C)"], [[r["case"].corner, f"{r['case'].temp:g}"] for r in rs]) + [""]
    if by.get("vdd"):
        rs = by["vdd"]
        L += ["## Supply voltage", "",
              "*fixed*: all biases at their nominal voltage. *tracks VDD*: VNA and VKup (PMOS, "
              "source at VDD) move with VDD, so their gate-source voltage stays the same.", ""]
        L += table(rs, ["VDD (V)", "PMOS biases"],
                   [[f"{r['case'].tags['vdd']:g}", r["case"].tags["pmos_bias"]] for r in rs]) + [""]
    if by.get("bias"):
        rs = by["bias"]
        nom = next((r for r in rs if r["case"].tags["bias"] == ""), None)
        L += ["## Bias sensitivity (each bias +-10 mV)", ""]
        if nom and nom["fired"]:
            L += ["Change of each spec per 10 mV increase of the bias (half the difference between "
                  "+10 mV and -10 mV). *Tolerance*: drift (mV, linear estimate) before the first spec "
                  "leaves its range, and which spec that is. Bias voltages on subthreshold devices "
                  "change their current by about 10x per 60-100 mV, so a few mV matter.", "",
                  "| bias | " + " | ".join(f"{m} ({UNITS[m][0]}/10 mV)" for m in METRICS)
                  + " | tolerance (mV) |", "|" + "---|" * (len(METRICS) + 2)]
            for b in BIASES:
                up = next((r for r in rs if r["case"].tags["bias"] == b and r["case"].tags["delta"] > 0), None)
                dn = next((r for r in rs if r["case"].tags["bias"] == b and r["case"].tags["delta"] < 0), None)
                cells, tol = [], []
                for m in METRICS:
                    if up and dn and up["vals"][m] is not None and dn["vals"][m] is not None:
                        sens = (up["vals"][m] - dn["vals"][m]) / 2          # per 10 mV
                        cells.append(f"{sens * UNITS[m][1]:+.3g}")
                        lo, hi = limits(m, NOM["p_vdd"])
                        x = nom["vals"][m]
                        if not nom["ok"][m]:
                            continue   # already out of spec at nominal: no drift tolerance
                        if sens > 0 and hi is not None:
                            tol.append(((hi - x) / sens * 10, f"+{m}"))
                        if sens < 0 and lo is not None:
                            tol.append(((x - lo) / -sens * 10, f"+{m}"))
                        if sens > 0 and lo is not None:
                            tol.append(((x - lo) / sens * 10, f"-{m}"))
                        if sens < 0 and hi is not None:
                            tol.append(((hi - x) / -sens * 10, f"-{m}"))
                    else:
                        cells.append("no firing" if (up or dn) else "-")
                t = min(tol) if tol else None
                ts = f"{t[0]:.1f} ({t[1][0]}, {t[1][1:]})" if t else "-"
                L.append(f"| {b[2:]} ({NOM[b]:g} V) | " + " | ".join(cells) + f" | {ts} |")
            already = [m for m in METRICS if not nom["ok"][m]]
            L += ["", "Tolerance sign: (+, x) means raising the bias makes spec x fail first; (-, x) lowering it."
                  + (f" Specs already out of range at nominal, so left out of the tolerance: {', '.join(already)}."
                     if already else ""), ""]
        L += table(rs, ["bias", "change"],
                   [[r["case"].tags["bias"][2:] or "nominal", f"{r['case'].tags['delta'] * 1e3:+g} mV"] for r in rs]) + [""]
    if by.get("mc"):
        rs = by["mc"]
        fired = [r for r in rs if r["fired"]]
        n = len(rs)
        L += ["## Device mismatch (tt, 27 C)", "",
              f"{len(fired)} of {n} samples fire; **{sum(r['all_ok'] for r in rs)} of {n} meet all specs "
              f"({100 * sum(r['all_ok'] for r in rs) / n:.0f} % yield)**.", "",
              "| spec | mean | std dev | min | max | in spec |", "|---|---|---|---|---|---|"]
        for m in METRICS:
            xs = [r["vals"][m] * UNITS[m][1] for r in fired if r["vals"][m] is not None]
            if len(xs) >= 2:
                L.append(f"| {m} ({UNITS[m][0]}) | {statistics.mean(xs):.4g} | {statistics.stdev(xs):.3g} | "
                         f"{min(xs):.4g} | {max(xs):.4g} | {sum(r['ok'][m] for r in rs)} / {n} |")
        L.append("")
    bad = [r["case"].name for rs in by.values() for r in rs if not r["sim_ok"]]
    if bad:
        L += [f"Simulations that failed to run: {', '.join(bad)} (see `runs/<name>/ngspice.log`).", ""]
    L += [f"Every run: `{path.stem}.csv`. Netlists, logs and waveforms: `runs/robust_{variant}_*/`."]
    path.write_text("\n".join(L) + "\n")


def write_csv(path, by):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["suite", "label", "corner", "temp", "vdd", "seed", "changed", "fired"] + METRICS
                   + ["all_specs"])
        for suite, rs in by.items():
            for r in rs:
                c = r["case"]
                changed = ";".join(f"{k}={v}" for k, v in c.params.items() if k != "p_tstop")
                w.writerow([suite, c.tags["label"], c.corner, c.temp, c.tags["vdd"], c.seed or "", changed,
                            int(r["fired"])] + ["" if r["vals"][m] is None else r["vals"][m] for m in METRICS]
                           + [int(r["all_ok"])])


def plots(by, stem):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: no plots")
        return
    ink, ink2, grid, surf, band = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#e9f1fb"
    corners = [("tt", "#2a78d6", "o"), ("ss", "#eb6834", "s"), ("ff", "#1baf7a", "^"),
               ("sf", "#eda100", "D"), ("fs", "#e87ba4", "v")]
    shown = ["period", "t_spike", "t_refr"]

    def style(ax):
        ax.set_facecolor(surf)
        ax.grid(True, color=grid, lw=0.8)
        for sp in ax.spines.values():
            sp.set_color(grid)
        ax.tick_params(colors=ink2)

    if by.get("pvt"):
        fig, axs = plt.subplots(1, 3, figsize=(14, 4.4), facecolor=surf)
        for ax, m in zip(axs, shown):
            style(ax)
            lo, hi = limits(m, 3.3)
            ax.axhspan(lo * 1e6, hi * 1e6, color=band, zorder=0, label="spec")
            for cn, color, marker in corners:
                rs = sorted([r for r in by["pvt"] if r["case"].corner == cn], key=lambda r: r["case"].temp)
                pts = [(r["case"].temp, r["vals"][m] * 1e6) for r in rs if r["vals"][m] is not None]
                if pts:
                    ax.plot(*zip(*pts), color=color, lw=2, marker=marker, ms=7, mec=surf, mew=1.5, label=cn)
            ax.set_xlabel("Temperature (C)", color=ink2)
            ax.set_ylabel(f"{m} (us)", color=ink2)
            ax.set_xticks([0, 27, 85])
        axs[0].legend(frameon=False, labelcolor=ink2, fontsize=8, ncol=2)
        dead = [f"{r['case'].corner} {r['case'].temp:g} C" for r in by["pvt"] if not r["fired"]]
        fig.suptitle("neuron_sized across corners and temperature, 9.5 nA DC"
                     + (f"  (no firing: {', '.join(dead)})" if dead else ""),
                     color=ink, x=0.01, ha="left")
        fig.tight_layout()
        fig.savefig(RESULTS / f"{stem}_pvt.png", dpi=150, facecolor=surf)
        plt.close(fig)
        print(f"wrote {RESULTS / (stem + '_pvt.png')}")

    if by.get("mc"):
        fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), facecolor=surf)
        fired = [r for r in by["mc"] if r["fired"]]
        for ax, m in zip(axs, shown):
            style(ax)
            xs = [r["vals"][m] * 1e6 for r in fired if r["vals"][m] is not None]
            if xs:
                ax.hist(xs, bins=20, color="#2a78d6", edgecolor=surf, linewidth=2)
            for lim in limits(m, 3.3):
                if lim is not None:
                    ax.axvline(lim * 1e6, color=ink, lw=1.5, ls="--")
            ax.set_xlabel(f"{m} (us); dashed: spec limits", color=ink2)
            ax.set_ylabel("samples", color=ink2)
        n = len(by["mc"])
        fig.suptitle(f"neuron_sized device mismatch, tt 27 C: {len(fired)} of {n} samples fire, "
                     f"{sum(r['all_ok'] for r in by['mc'])} meet all specs", color=ink, x=0.01, ha="left")
        fig.tight_layout()
        fig.savefig(RESULTS / f"{stem}_mc.png", dpi=150, facecolor=surf)
        plt.close(fig)
        print(f"wrote {RESULTS / (stem + '_mc.png')}")


def report(done, variant, note, suites):
    by = {s: [row(c) for c in done if c.tags["suite"] == s] for s in suites}
    by = {s: rs for s, rs in by.items() if rs}
    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}__robust{'__pex' if variant == 'pex' else ''}"
    write_csv(RESULTS / f"{stem}.csv", by)
    write_md(RESULTS / f"{stem}.md", by, variant, note)
    print(f"wrote {RESULTS / (stem + '.md')} and .csv")
    for s, rs in by.items():
        print(f"  {s:5}: {sum(r['all_ok'] for r in rs)} of {len(rs)} meet all specs, "
              f"{sum(not r['fired'] for r in rs)} do not fire")
    plots(by, stem)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of the neuron")
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--mc", type=int, help="number of mismatch samples (default 100)")
    ap.add_argument("--quick", action="store_true", help="20 mismatch samples")
    ap.add_argument("--jobs", type=int, default=4, help="parallel ngspice runs (one thread each)")
    ap.add_argument("--report-only", action="store_true",
                    help="no simulation: rebuild the report from the runs already in runs/")
    a = ap.parse_args()
    variant = "pex" if a.pex else "sch"
    suites = a.only.split(",") if a.only else list(SUITES)
    for s in suites:
        if s not in SUITES:
            raise SystemExit(f"unknown suite {s}; choose from {','.join(SUITES)}")

    if a.report_only:
        done = load_runs(variant, suites)
        if not done:
            raise SystemExit(f"no runs in {RUNS}/robust_{variant}_*")
        report(done, variant, tbpex.pex_note((RUNS / done[0].name / f"{TB}.spice").read_text()) if a.pex else "", suites)
        return

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / f"netlist_robust_{variant}").read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    tb.check_connected(text, CELL)
    note = ""
    if a.pex:
        text = tbpex.use_pex(text, CELL)
        note = tbpex.pex_note(text)

    cases = [c for s in suites for c in SUITES[s](variant, a)]
    print(f"{variant}: {len(cases)} runs ({', '.join(suites)}), {a.jobs} at a time")
    done = tb.run_cases(cases, {TB: text}, RUNS, jobs=a.jobs)
    for c in done:
        save_tags(c)
    report(done, variant, note, suites)


if __name__ == "__main__":
    main()
