"""DPI output vs membrane voltage (dpi_load_tb.sch): does the synapse still work as VMEM moves?

    python3 analog/testbenches/dpi/run_dpi_load.py                     # DPI_sized, all suites
    python3 analog/testbenches/dpi/run_dpi_load.py --cell DPI          # min-size DPI (on main)
    python3 analog/testbenches/dpi/run_dpi_load.py --bias chain --only pvt
    python3 analog/testbenches/dpi/run_dpi_load.py --pex               # post-layout (needs extractions)
    python3 analog/testbenches/dpi/run_dpi_load.py --report-only

Run inside the container. The excitatory output (x1, --cell) sources current into
VMEM; the inhibitory DPI_inh (x2) sinks current from it. In the network VMEM moves
from 0 to the 1.66 V threshold while integrating and to ~3.2 V during a spike, but
the old DPI testbenches held the output at 0 V. Here a DC input of 15, 45 and 150 nA
(DAC codes worth 1, 3 and 10 units) is sunk from each tail and the output voltage is
swept from 0 to VDD. Each run is one DC simulation (seconds). Suites:

  bias   the four bias presets (output, hidden, relay, chain) at tt 27 C        (4 runs)
  pvt    --bias at corners tt/ss/ff/sf/fs x 0/27/85 C                            (15 runs)
  mc     --bias with device mismatch, --mc samples (default 50)

Reported per input level: the output current at the reference VMEM (0.5 V
excitatory, 1.0 V inhibitory) and as a fraction of the input (DC gain); how much of
it is left at VMEM = 1.66 V and 3.2 V (excitatory) or 0.1 V (inhibitory); the VMEM at
which it has dropped by 1 % and 10 %; and the tail voltage V(Isum), which the DAC
needs to stay above 1.8-2.07 V (results of dac/run_dac_signed.py).
Writes results/dpi_load_tb[__<cell>][__<bias>][__pex].md / .csv / .png.
"""

import argparse
import csv
import datetime
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dpicommon as dc  # noqa: E402

TB = "dpi_load_tb"
LEVELS = (1, 2, 3)
DAC_STATIC = HERE.parent / "dac" / "results" / "dac_signed_static_tb.csv"


def suites(a, variant):
    pre = f"dpiload_{variant}_{a.cell}"
    out = {"bias": [], "pvt": [], "mc": []}
    for b in dc.BIASES:
        out["bias"].append(dc.tb.Case(name=f"{pre}_bias_{b}", tb=TB, params=dc.bias_params(b),
                                      tags={"suite": "bias", "bias": b}))
    for cn, t in dc.CORNERS:
        out["pvt"].append(dc.tb.Case(name=f"{pre}_pvt_{a.bias}_{cn}_{t}C", tb=TB, corner=cn, temp=t,
                                     params=dc.bias_params(a.bias), tags={"suite": "pvt", "bias": a.bias}))
    for s in range(1, a.mc + 1):
        out["mc"].append(dc.tb.Case(name=f"{pre}_mc_{a.bias}_seed{s}", tb=TB, seed=s,
                                    params=dc.bias_params(a.bias), tags={"suite": "mc", "bias": a.bias}))
    return out


def dac_vmin():
    """DAC_signed's minimum output voltage per (corner, temp), from its static results."""
    out = {}
    if DAC_STATIC.exists():
        for r in csv.DictReader(open(DAC_STATIC)):
            if r["suite"] in ("nominal", "pvt") and r["vmin_e"]:
                out[(r["corner"], int(float(r["temp"])))] = max(float(r["vmin_e"]), float(r["vmin_i"]))
    return out


def metrics(c):
    r = c.results
    if r.get("e1_ref") is None:
        return None
    m = {"case": c, "bias": c.tags["bias"], "corner": c.corner, "temp": c.temp}
    for j in LEVELS:
        iw = r[f"iw{j}"]
        e, i = r[f"e{j}_ref"], r[f"i{j}_ref"]
        m[j] = {"iw": iw, "e": e, "i": i, "gain_e": e / iw, "gain_i": i / iw,
                "e166": r[f"e{j}_at166"] / e, "e32": r[f"e{j}_at32"] / e, "e0": r[f"e{j}_at0"] / e,
                "i01": r[f"i{j}_at01"] / i, "i166": r[f"i{j}_at166"] / i,
                "e_v99": r[f"e{j}_v99"], "e_v90": r[f"e{j}_v90"], "i_v99": r[f"i{j}_v99"], "i_v90": r[f"i{j}_v90"],
                "vsum_e": r[f"vsum_e{j}"], "vsum_i": r[f"vsum_i{j}"]}
    return m


def v(x):
    return "none" if x is None or x < 0 else f"{x:.2f}"


def table(ms, first_cols, first_vals, vmins):
    L = ["| " + " | ".join(first_cols) + " | input (nA) | exc. out (nA) | exc. gain | left at 1.66 V | at 3.2 V | "
         "exc. -1 % / -10 % at VMEM (V) | inh. out (nA) | left at 0.1 V | inh. -1 % / -10 % at VMEM (V) | "
         "V(Isum) (V) | DAC needs (V) |", "|" + "---|" * (len(first_cols) + 12)]
    for m, fv in zip(ms, first_vals):
        need = vmins.get((m["corner"], int(m["temp"])))
        for j in LEVELS:
            d = m[j]
            vs = min(d["vsum_e"], d["vsum_i"])
            short = need is not None and vs < need
            L.append("| " + " | ".join(fv if j == 1 else [""] * len(fv)) +
                     f" | {d['iw'] * 1e9:.0f} | {d['e'] * 1e9:.4g} | {d['gain_e']:.3g} | {d['e166'] * 100:.0f} % | "
                     f"{d['e32'] * 100:.0f} % | {v(d['e_v99'])} / {v(d['e_v90'])} | {d['i'] * 1e9:.4g} | "
                     f"{d['i01'] * 100:.0f} % | {v(d['i_v99'])} / {v(d['i_v90'])} | "
                     f"{'**' if short else ''}{vs:.3f}{'**' if short else ''} | {'-' if need is None else f'{need:.2f}'} |")
    return L


def write_md(path, by, a, variant, note):
    vmins = dac_vmin()
    L = [f"# {path.stem}: synapse output vs membrane voltage", "",
         f"Generated by `run_dpi_load.py` on {datetime.datetime.now():%Y-%m-%d %H:%M}. Excitatory cell: "
         f"`{a.cell}`; inhibitory: `DPI_inh`" + (f"; post-layout ({note})" if variant == "pex" else "") +
         f". Bias presets: " + "; ".join(f"*{k}* Vthr {b[0]} V, vtau {b[1]} V ({b[3]})" for k, b in dc.BIASES.items()) + ".",
         "", "Reference VMEM: 0.5 V (excitatory), 1.0 V (inhibitory). *Left at*: output current at that VMEM as a "
         "fraction of the reference. *-1 % / -10 % at VMEM*: membrane voltage where the output has dropped by 1 % / "
         "10 % (excitatory: rising VMEM; inhibitory: falling VMEM; *none*: not within 0-3.3 V). *V(Isum)*: the tail "
         "voltage the DAC sees (lowest of the two DPIs at the reference VMEM); bold where it is below what "
         "`DAC_signed` needs at that corner (`dac/results/dac_signed_static_tb.csv`, 1 % compliance).", ""]
    if by.get("bias"):
        L += ["## Bias presets (tt, 27 C)", ""] + table(by["bias"], ["bias"], [[m["bias"]] for m in by["bias"]], vmins) + [""]
    if by.get("pvt"):
        L += [f"## Corners and temperature ({a.bias} biases)", ""] + table(
            by["pvt"], ["corner", "T (C)"], [[m["corner"], f"{m['temp']:g}"] for m in by["pvt"]], vmins) + [""]
    if by.get("mc"):
        ms = by["mc"]
        L += [f"## Device mismatch (tt, 27 C, {a.bias} biases, {len(ms)} samples)", "",
              "| input (nA) | quantity | mean | std dev | min | max |", "|---|---|---|---|---|---|"]
        for j in LEVELS:
            for key, name, k in (("gain_e", "excitatory gain", 1), ("gain_i", "inhibitory gain", 1),
                                 ("e166", "excitatory left at 1.66 V (%)", 100), ("i01", "inhibitory left at 0.1 V (%)", 100),
                                 ("vsum_e", "V(Isum) (V)", 1)):
                xs = [m[j][key] * k for m in ms]
                L.append(f"| {ms[0][j]['iw'] * 1e9:.0f} | {name} | {statistics.mean(xs):.4g} | {statistics.stdev(xs):.3g} | "
                         f"{min(xs):.4g} | {max(xs):.4g} |")
            ratio = [m[j]["i"] / m[j]["e"] for m in ms]
            L.append(f"| {ms[0][j]['iw'] * 1e9:.0f} | inhibitory / excitatory output | {statistics.mean(ratio):.4g} | "
                     f"{statistics.stdev(ratio):.3g} | {min(ratio):.4g} | {max(ratio):.4g} |")
        L.append("")
    L += [f"Every run: `{path.stem}.csv`. Logs and the swept curves: `runs/dpiload_{variant}_{a.cell}_*/`."]
    path.write_text("\n".join(L) + "\n")


def write_csv(path, by):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        keys = ["iw", "e", "i", "gain_e", "gain_i", "e0", "e166", "e32", "i01", "i166", "e_v99", "e_v90",
                "i_v99", "i_v90", "vsum_e", "vsum_i"]
        w.writerow(["suite", "bias", "corner", "temp", "seed", "level"] + keys)
        for s, ms in by.items():
            for m in ms:
                for j in LEVELS:
                    w.writerow([s, m["bias"], m["corner"], m["temp"], m["case"].seed or "", j] + [m[j][k] for k in keys])


def plot(path, by, a):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    nominal = [m for m in by.get("bias", []) if m["bias"] == a.bias] or by.get("bias", [])[:1]
    if not nominal:
        return
    run = dc.RUNS / nominal[0]["case"].name
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=dc.SURF)
    for ax, side, ref, title in ((axs[0], "e", 0.5, "Excitatory output (sources into VMEM)"),
                                 (axs[1], "i", 1.0, "Inhibitory output (sinks from VMEM)")):
        dc.style(ax)
        for j, color in zip(LEVELS, dc.SERIES):
            f = run / f"dpi_load_tb_{side}{j}.txt"
            if not f.exists():
                continue
            pts = [tuple(map(float, line.split()[:2])) for line in f.read_text().splitlines() if line.strip()]
            iref = nominal[0][j][side]
            ax.plot([p[0] for p in pts], [p[1] / iref * 100 for p in pts], color=color, lw=2,
                    label=f"input {nominal[0][j]['iw'] * 1e9:.0f} nA")
        for x, lab in ((1.66, "threshold"), (3.2, "spike")):
            ax.axvline(x, color=dc.INK2, lw=1, ls=":")
            ax.annotate(lab, (x, 0.03), xycoords=("data", "axes fraction"), rotation=90, fontsize=8,
                        color=dc.INK2, ha="right", va="bottom")
        ax.set_xlabel("Membrane voltage VMEM (V)", color=dc.INK2)
        ax.set_ylabel(f"Output current, % of its value at {ref} V", color=dc.INK2)
        ax.set_title(title, color=dc.INK, loc="left", fontsize=10)
        ax.legend(frameon=False, labelcolor=dc.INK2, fontsize=8)
    fig.suptitle(f"{a.cell} / DPI_inh output vs membrane voltage ({nominal[0]['bias']} biases, tt 27 C)",
                 color=dc.INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=dc.SURF)
    plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cell", choices=dc.CELLS, default="DPI_sized", help="excitatory DPI (default DPI_sized)")
    ap.add_argument("--bias", choices=list(dc.BIASES), default="output", help="bias preset for pvt and mc")
    ap.add_argument("--only", help="comma-separated suites: bias,pvt,mc")
    ap.add_argument("--mc", type=int, default=50, help="mismatch samples")
    ap.add_argument("--pex", action="store_true", help="post-layout extractions of the DPIs")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--report-only", action="store_true", help="no simulation: report from runs/")
    a = ap.parse_args()
    variant = "pex" if a.pex else "sch"
    all_cases = suites(a, variant)
    chosen = a.only.split(",") if a.only else list(all_cases)
    note = ""
    if not a.report_only:
        text, note = dc.prepare_netlist(HERE / f"{TB}.sch", dc.RUNS / f"netlist_load_{variant}_{a.cell}", a.cell, a.pex)
        cases = [c for s in chosen for c in all_cases[s]]
        print(f"{variant} {a.cell}: {len(cases)} runs ({', '.join(chosen)}), {a.jobs} at a time")
        dc.run_and_save(cases, {TB: text}, a.jobs)
    # report on every saved run of this cell/variant (all suites), so --only adds to it
    names = {c.name for s in all_cases.values() for c in s}
    done = [c for c in dc.load_runs(f"dpiload_{variant}_{a.cell}_") if c.name in names]
    by = {}
    for c in done:
        m = metrics(c) if c.ok else None
        if m:
            by.setdefault(c.tags["suite"], []).append(m)
    for s in by:
        by[s].sort(key=lambda m: (list(dc.BIASES).index(m["bias"]), ["tt", "ss", "ff", "sf", "fs"].index(m["corner"]),
                                  m["temp"], m["case"].seed or 0))
    dc.RESULTS.mkdir(exist_ok=True)
    stem = dc.stem(TB, a.cell, a.bias, a.pex)
    write_csv(dc.RESULTS / f"{stem}.csv", by)
    write_md(dc.RESULTS / f"{stem}.md", by, a, variant, note)
    plot(dc.RESULTS / f"{stem}.png", by, a)
    print(f"wrote {dc.RESULTS / (stem + '.md')} and .csv ({sum(len(v) for v in by.values())} runs)")


if __name__ == "__main__":
    main()
