"""Characterise DAC_signed (the weight DAC with a sign switch) with dac_signed_static_tb.sch.

    python3 analog/testbenches/dac/run_dac_signed.py                 # all suites, schematic
    python3 analog/testbenches/dac/run_dac_signed.py --pex           # post-layout (needs an extraction)
    python3 analog/testbenches/dac/run_dac_signed.py --only nominal,pvt
    python3 analog/testbenches/dac/run_dac_signed.py --mc 200 --jobs 8
    python3 analog/testbenches/dac/run_dac_signed.py --report-only   # rebuild the report from runs/

Run inside the container. Every run is one DC simulation (all 16 codes x both
signs, then a compliance sweep of each output), a few seconds. Suites:

  nominal  tt, 27 C. Also gives the sign-magnitude table: what each digital weight
           -7..+7 delivers when bits 2:0 are the magnitude and bit 3 drives s, as
           in the digital register file and mock (mock/dac.v)
  pvt      corners tt/ss/ff/sf/fs x 0/27/85 C                                 (15 runs)
  mc       device mismatch, tt 27 C, --mc samples (default 100), including the
           reference diode that sets Vb

Measured per run: Vb, unit current (least-squares slope of current vs ideal
weight), branch ratios, full scale, INL, monotonicity, excitatory/inhibitory
current ratio per code, current to the unselected output (crosstalk), code-0
leakage, and the lowest output voltage that still gives full scale within 1 %.

--pex swaps DAC_signed for its extraction (analog/neuron/layout/PEX/); it stops with
the command to run if there is no extraction or the layout changed since.
Each run is in runs/dac_signed_<sch|pex>_<suite>_<x>/. Writes, in results/
(post-layout runs add __pex):
  dac_signed_static_tb[__pex].md / .csv     report and one row per run
  dac_signed_static_tb[__pex]_codes.csv     nominal current for every code and sign
  dac_signed_static_tb.png                  sign-magnitude transfer (schematic and
                                            post-layout overlaid) and mismatch spread
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

TB = "dac_signed_static_tb"
CELL = "DAC_signed"
RESULTS = HERE / "results"
RUNS = HERE / "runs"
VE_NOM = 2.5  # output voltage the currents are measured at (p_ve, p_vi)


# --- conditions ------------------------------------------------------------------

def case(variant, suite, label, corner="tt", temp=27, seed=None):
    return tb.Case(name=f"dac_signed_{variant}_{suite}_{label}", tb=TB, corner=corner, temp=temp,
                   seed=seed, tags={"suite": suite, "label": label})


def suite_nominal(v, a):
    return [case(v, "nominal", "tt_27C")]


def suite_pvt(v, a):
    return [case(v, "pvt", f"{c}_{t}C", corner=c, temp=t)
            for c in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]


def suite_mc(v, a):
    return [case(v, "mc", f"seed{s}", seed=s) for s in range(1, (a.mc or 100) + 1)]


SUITES = {"nominal": suite_nominal, "pvt": suite_pvt, "mc": suite_mc}


# --- analysis ----------------------------------------------------------------------

def bits(code):
    return [(code >> b) & 1 for b in range(4)]


def analyze(r):
    """Metrics of one run from its RES values; None if the run is incomplete."""
    if int(r.get("npts") or 0) != 32:
        return None
    sel = {(c, s): r[f"{'ie' if s == 0 else 'ii'}{16 * s + c}"] for c in range(16) for s in (0, 1)}
    off = {(c, s): r[f"{'ii' if s == 0 else 'ie'}{16 * s + c}"] for c in range(16) for s in (0, 1)}
    i0, i1 = sel[(0, 0)], sel[(1, 0)]
    ratios = [(sel[(1 << b, 0)] - i0) / (i1 - i0) for b in range(4)]
    weights = [round(x) for x in ratios]
    w = {c: sum(wb * bb for wb, bb in zip(weights, bits(c))) for c in range(16)}
    m = {"vb": r.get("vb"), "ratios": ratios, "weights": weights, "sel": sel, "off": off, "w": w}
    for s in (0, 1):
        xs = [w[c] for c in range(16)]
        ys = [sel[(c, s)] for c in range(16)]
        mx, my = statistics.mean(xs), statistics.mean(ys)
        unit = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        offs = my - unit * mx
        m[f"unit{s}"] = unit
        m[f"inl{s}"] = max(abs(sel[(c, s)] - (offs + unit * w[c])) / unit for c in range(16))
        levels = sorted(set(w.values()))
        mean_at = [statistics.mean(sel[(c, s)] for c in range(16) if w[c] == lv) for lv in levels]
        m[f"mono{s}"] = all(b > a for a, b in zip(mean_at, mean_at[1:]))
        m[f"fs{s}"] = sel[(15, s)]
        m[f"leak0_{s}"] = sel[(0, s)]
    m["unit"] = m["unit0"]
    m["inl"] = max(m["inl0"], m["inl1"])
    m["mono"] = m["mono0"] and m["mono1"]
    ei = [sel[(c, 1)] / sel[(c, 0)] for c in range(1, 16)]
    m["ei_min"], m["ei_max"] = min(ei), max(ei)
    m["xtalk"] = max(off[(c, s)] / sel[(c, s)] for c in range(1, 16) for s in (0, 1))
    m["xtalk_abs"] = max(off[(c, s)] for c in range(16) for s in (0, 1))
    m["vmin_e"], m["vmin_i"] = r.get("vmin_e"), r.get("vmin_i")
    # Sign-magnitude: digital weight d in -7..7 -> bits 2:0 = |d|, s = (d < 0)
    m["smag"] = {d: (sel[(abs(d), 1 if d < 0 else 0)] * (-1 if d < 0 else 1)) for d in range(-7, 8)}
    return m


# --- reporting -----------------------------------------------------------------------

def nA(x):
    return "-" if x is None else f"{x * 1e9:.4g}"


def pA(x):
    return "-" if x is None else f"{x * 1e12:.3g}"


def fmt_v(x):
    return "-" if x is None or x < 0 else f"{x:.3g}"


def write_md(path, by, variant, note):
    L = [f"# {TB}{'__pex' if variant == 'pex' else ''}: DAC_signed, DC", "",
         f"Generated by `run_dac_signed.py{' --pex' if variant == 'pex' else ''}` on "
         f"{datetime.datetime.now():%Y-%m-%d %H:%M}. Cell: "
         + ("post-layout extraction (" + note + ")" if variant == "pex" else "schematic `analog/neuron/DAC_signed.sch`")
         + f". Iref 14.42 nA into a 1 um / 8 um diode for Vb, en high, outputs held at {VE_NOM} V, gmin 1e-16 S.", ""]
    nom = next((m for c, m in by.get("nominal", []) if m), None)
    if nom:
        u = nom["unit"]
        L += ["## Nominal (tt, 27 C)", "",
              f"- Vb {nom['vb']:.4g} V; unit current {nA(u)} nA (s = 0), {nA(nom['unit1'])} nA (s = 1)",
              f"- Branch ratios w[0..3]: {', '.join(f'{x:.3f}' for x in nom['ratios'])} "
              f"(taken as {':'.join(map(str, nom['weights']))}); full scale {nA(nom['fs0'])} nA = "
              f"{nom['fs0'] / u:.2f} units",
              f"- INL {nom['inl']:.3g} units; monotonic: {'yes' if nom['mono'] else '**no**'}",
              f"- Inhibitory / excitatory current, codes 1-15: {nom['ei_min']:.5f} to {nom['ei_max']:.5f}",
              f"- Current to the unselected output: at most {pA(nom['xtalk_abs'])} pA "
              f"({nom['xtalk'] * 100:.2g} % of the selected current)",
              f"- Code 0 (en on, all bits off): {pA(nom['leak0_0'])} pA",
              f"- Full scale within 1 % down to an output voltage of {fmt_v(nom['vmin_e'])} V (Isum_e), "
              f"{fmt_v(nom['vmin_i'])} V (Isum_i)", "",
              "### Every code", "",
              "| code | w[3:0] | ideal weight | Isum_e, s = 0 (nA) | Isum_i, s = 1 (nA) | i / e | to the other output (pA) |",
              "|---|---|---|---|---|---|---|"]
        for c in range(16):
            e, i = nom["sel"][(c, 0)], nom["sel"][(c, 1)]
            L.append(f"| {c} | {c:04b} | {nom['w'][c]} | {nA(e)} | {nA(i)} | "
                     f"{(i / e if c else float('nan')):.5f} | {pA(max(nom['off'][(c, 0)], nom['off'][(c, 1)]))} |")
        L += ["", "### Digital sign-magnitude weights", "",
              "The digital side (`rf`, `mock/dac.v`) stores weights as sign-magnitude: bit 3 is the sign, "
              "bits 2:0 the magnitude (0-7, binary). Wired straight to `DAC_signed` (bits 2:0 to w[2:0], "
              "w[3] = 0, bit 3 to s), each digital weight delivers:", "",
              "| digital weight | to | units delivered | ideal | error (units) |", "|---|---|---|---|---|"]
        for d in range(-7, 8):
            got = nom["smag"][d] / u
            L.append(f"| {d:+d} | {'Isum_i' if d < 0 else 'Isum_e'} | {got:+.2f} | {d:+d} | {got - d:+.2f} |")
        L += ["", "With branches 1:2:3:4, bits 2:0 weigh 1:2:3, so magnitudes 4-7 come out as 3-6 units: "
              "the digital weights and the analog branches disagree (see the end of this report).", ""]
    if by.get("pvt"):
        L += ["## Process corners and temperature", "",
              "| corner | T (C) | Vb (V) | unit (nA) | full scale (nA) | INL (units) | monotonic | i / e | "
              "to the other output (pA) | code 0 (pA) | vmin e / i (V) |", "|" + "---|" * 11]
        for c, m in by["pvt"]:
            if not m:
                L.append(f"| {c.corner} | {c.temp:g} | run failed | | | | | | | | |")
                continue
            L.append(f"| {c.corner} | {c.temp:g} | {m['vb']:.3f} | {nA(m['unit'])} | {nA(m['fs0'])} | "
                     f"{m['inl']:.3g} | {'yes' if m['mono'] else '**no**'} | {m['ei_min']:.4f}-{m['ei_max']:.4f} | "
                     f"{pA(m['xtalk_abs'])} | {pA(m['leak0_0'])} | {fmt_v(m['vmin_e'])} / {fmt_v(m['vmin_i'])} |")
        L.append("")
    if by.get("mc"):
        ms = [m for c, m in by["mc"] if m]
        n = len(by["mc"])
        L += ["## Device mismatch (tt, 27 C)", "",
              f"{len(ms)} of {n} samples simulated; monotonic in {sum(m['mono'] for m in ms)} of {len(ms)}. "
              "The reference diode mismatches too, so the unit spread includes the reference.", "",
              "| quantity | mean | std dev | min | max |", "|---|---|---|---|---|"]
        rows = [("unit current (nA)", [m["unit"] * 1e9 for m in ms]),
                ("full scale (nA)", [m["fs0"] * 1e9 for m in ms]),
                ("INL (units)", [m["inl"] for m in ms]),
                ("i / e, lowest code", [m["ei_min"] for m in ms]),
                ("i / e, highest code", [m["ei_max"] for m in ms])]
        rows += [(f"branch w[{b}] ratio (ideal {ms[0]['weights'][b]})", [m["ratios"][b] for m in ms]) for b in range(4)]
        for name, xs in rows:
            if len(xs) >= 2:
                L.append(f"| {name} | {statistics.mean(xs):.4g} | {statistics.stdev(xs):.3g} | {min(xs):.4g} | {max(xs):.4g} |")
        L.append("")
    L += ["## Open points", "",
          "- Weight format: the digital side is sign-magnitude with a 3-bit binary magnitude; `DAC_signed` "
          "wraps the 1:2:3:4 `DAC` with a separate sign pin. A matching cell would steer `DAC_binary`'s "
          "x1/x2/x4 branches with s = bit 3.",
          "- Dynamic behaviour (charge per input spike when `en` switches, injection, real spike shapes) "
          "needs a pulse testbench.", "",
          f"Every run: `{path.stem}.csv`; nominal currents per code: `{path.stem}_codes.csv`. "
          f"Netlists and logs: `runs/dac_signed_{variant}_*/`."]
    path.write_text("\n".join(L) + "\n")


def write_csvs(stem, by):
    keys = ["vb", "unit", "unit1", "fs0", "fs1", "inl", "mono", "ei_min", "ei_max", "xtalk", "xtalk_abs",
            "leak0_0", "leak0_1", "vmin_e", "vmin_i"]
    with open(RESULTS / f"{stem}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["suite", "label", "corner", "temp", "seed"] + keys + [f"ratio_w{b}" for b in range(4)])
        for suite, cms in by.items():
            for c, m in cms:
                w.writerow([suite, c.tags["label"], c.corner, c.temp, c.seed or ""]
                           + ([m[k] for k in keys] + m["ratios"] if m else [""] * (len(keys) + 4)))
    nom = next((m for c, m in by.get("nominal", []) if m), None)
    if nom:
        with open(RESULTS / f"{stem}_codes.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["code", "ideal_weight", "i_e_s0", "i_i_s1", "other_output_s0", "other_output_s1"])
            for c in range(16):
                w.writerow([c, nom["w"][c], nom["sel"][(c, 0)], nom["sel"][(c, 1)], nom["off"][(c, 0)], nom["off"][(c, 1)]])


def plot(by_variant):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: no plot")
        return
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    series = [("sch", "Schematic", "#2a78d6", "o"), ("pex", "Post-layout (PEX)", "#eb6834", "s")]
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(True, color=grid, lw=0.8)
        for sp in ax.spines.values():
            sp.set_color(grid)
        ax.tick_params(colors=ink2)
    a = axs[0]
    a.plot([-7, 7], [-7, 7], color=ink2, lw=1, ls="--", label="ideal (digital weight)")
    for v, label, color, marker in series:
        nom = by_variant.get(v)
        if nom:
            ds = list(range(-7, 8))
            a.plot(ds, [nom["smag"][d] / nom["unit"] for d in ds], color=color, lw=2, marker=marker,
                   ms=6, mec=surf, mew=1.5, label=label)
    a.set_xlabel("Digital weight (sign-magnitude, bit 3 = sign)", color=ink2)
    a.set_ylabel("Delivered current (units of 15 nA; < 0: Isum_i)", color=ink2)
    a.set_title("What each digital weight delivers", color=ink, loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8)
    a = axs[1]
    mc = by_variant.get("mc_units")
    if mc:
        a.hist([x * 1e9 for x in mc], bins=20, color="#2a78d6", edgecolor=surf, linewidth=2)
        a.set_xlabel("Unit current (nA), mismatch incl. reference", color=ink2)
        a.set_ylabel("samples", color=ink2)
        a.set_title(f"Unit current over {len(mc)} mismatch samples (tt, 27 C)", color=ink, loc="left", fontsize=10)
    else:
        a.set_axis_off()
    fig.suptitle("DAC_signed, DC", color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{TB}.png", dpi=150, facecolor=surf)
    plt.close(fig)
    print(f"wrote {RESULTS / (TB + '.png')}")


def report(done, variant, note, suites):
    by = {s: [(c, analyze(c.results) if c.ok else None) for c in done if c.tags["suite"] == s] for s in suites}
    by = {s: v for s, v in by.items() if v}
    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}{'__pex' if variant == 'pex' else ''}"
    write_csvs(stem, by)
    write_md(RESULTS / f"{stem}.md", by, variant, note)
    print(f"wrote {RESULTS / (stem + '.md')} and .csv")
    for s, cms in by.items():
        ok = [m for c, m in cms if m]
        print(f"  {s:8}: {len(ok)} of {len(cms)} runs analysed"
              + (f", unit {statistics.mean(m['unit'] for m in ok) * 1e9:.4g} nA" if ok else ""))
    # Plot: nominal of both variants (from their latest runs) and this variant's mismatch
    pv = {}
    for v in ("sch", "pex"):
        j = RUNS / f"dac_signed_{v}_nominal_tt_27C" / "ngspice.log"
        if j.exists():
            pv[v] = analyze(tb.parse_results(j.read_text()))
    ms = [m for c, m in by.get("mc", []) if m]
    if ms:
        pv["mc_units"] = [m["unit"] for m in ms]
    plot(pv)


def save_tags(c):
    d = RUNS / c.name
    if d.exists():
        (d / "case.json").write_text(json.dumps({"tags": c.tags, "corner": c.corner, "temp": c.temp, "seed": c.seed}))


def load_runs(variant, suites):
    done = []
    for j in sorted(RUNS.glob(f"dac_signed_{variant}_*/case.json")):
        info = json.loads(j.read_text())
        if info["tags"]["suite"] not in suites:
            continue
        c = tb.Case(name=j.parent.name, tb=TB, corner=info["corner"], temp=info["temp"],
                    seed=info["seed"], tags=info["tags"])
        log = j.parent / "ngspice.log"
        c.log = log.read_text() if log.exists() else ""
        c.results = tb.parse_results(c.log)
        c.ok = bool(c.results) and "aborted" not in c.log
        done.append(c)
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of DAC_signed")
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--mc", type=int, help="number of mismatch samples (default 100)")
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
            raise SystemExit(f"no runs in {RUNS}/dac_signed_{variant}_*")
        note = tbpex.pex_note((RUNS / done[0].name / f"{TB}.spice").read_text()) if a.pex else ""
        report(done, variant, note, suites)
        return

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / f"netlist_{variant}").read_text()
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
