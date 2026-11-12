"""The synapses driven by DAC-like current pulses (dpi_pulse_tb.sch): charge out per charge in.

    python3 analog/testbenches/dpi/run_dpi_pulse.py                   # DPI_sized, output biases, all suites
    python3 analog/testbenches/dpi/run_dpi_pulse.py --cell DPI --bias chain
    python3 analog/testbenches/dpi/run_dpi_pulse.py --only code,pair
    python3 analog/testbenches/dpi/run_dpi_pulse.py --pex             # post-layout (needs extractions)
    python3 analog/testbenches/dpi/run_dpi_pulse.py --report-only

Run inside the container. The input is what the DAC delivers: pulses of code x 15 nA,
10 us wide, every 200 us (5 kHz), sunk from the tail of the excitatory DPI (x1,
--cell) and of the inhibitory DPI_inh (x2). Both outputs are held at a membrane
voltage (default 0.5 V). The charge each output delivers to (or removes from) the
membrane is compared with the input charge. Suites:

  code     one pulse of codes 1, 2, 4, 7, 10, 15 (0.15-2.25 pC in): gain and linearity  (6 runs)
  train    10 pulses at 5 kHz, codes 1, 4, 15: charge of each pulse vs the first      (3 runs)
  pair     two code-4 pulses 20 us-2 ms apart vs one: does a second input add more
           (coincidence, as the XOR's AND relies on) or less                       (8 runs)
  width    one code-4 pulse 10 us vs 16.5 us (the enable time of a real neuron spike,
           dac/run_dac_signed_pulse.py)                                             (2 runs)
  vmem     one code-15 pulse with VMEM held at 0.1-2.5 V                              (5 runs)
  pvt      one code-4 pulse, corners tt/ss/ff/sf/fs x 0/27/85 C                     (15 runs)
  mc       one code-4 pulse with device mismatch, --mc samples (default 50)

Writes results/dpi_pulse_tb[__<cell>][__<bias>][__pex].md / .csv / .png.
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

TB = "dpi_pulse_tb"
CODES = [1, 2, 4, 7, 10, 15]
WEIGHT = {c: sum(wb * ((c >> b) & 1) for b, wb in enumerate((1, 2, 3, 4))) for c in range(16)}  # DAC 1:2:3:4
PAIR_GAPS = [20e-6, 50e-6, 100e-6, 200e-6, 400e-6, 700e-6, 1e-3, 2e-3]
VMEMS = [0.1, 0.5, 1.0, 1.66, 2.5]


def mk(a, variant, suite, label, units, extra=None, corner="tt", temp=27, seed=None):
    """One run; `units` is the input current in DAC units (code weight), not the code."""
    p = dc.bias_params(a.bias)
    p.update({"p_code": f"{units:g}", "p_npulse": "1", "p_tper": "200u", "p_tpw": "10u", "p_vmem": "0.5"})
    p.update(extra or {})
    return dc.tb.Case(name=f"dpipulse_{variant}_{a.cell}_{a.bias}_{suite}_{label}", tb=TB, params=p,
                      corner=corner, temp=temp, seed=seed,
                      tags={"suite": suite, "bias": a.bias, "units": units, "code": None})


def suites(a, v):
    s = {"code": [], "train": [], "pair": [], "width": [], "vmem": [], "pvt": [], "mc": []}
    for c in CODES:
        x = mk(a, v, "code", f"c{c}", WEIGHT[c])
        x.tags["code"] = c
        s["code"].append(x)
    for c in (1, 4, 15):
        x = mk(a, v, "train", f"c{c}", WEIGHT[c], {"p_npulse": "10"})
        x.tags["code"] = c
        s["train"].append(x)
    for g in PAIR_GAPS:
        x = mk(a, v, "pair", f"gap{g * 1e6:g}us", WEIGHT[4], {"p_npulse": "2", "p_tper": f"{g:g}"})
        x.tags.update(code=4, gap=g)
        s["pair"].append(x)
    for w in (10e-6, 16.5e-6):
        x = mk(a, v, "width", f"w{w * 1e6:g}us", WEIGHT[4], {"p_tpw": f"{w:g}"})
        x.tags.update(code=4, tpw=w)
        s["width"].append(x)
    for vm in VMEMS:
        x = mk(a, v, "vmem", f"v{vm:g}".replace(".", "p"), WEIGHT[15], {"p_vmem": f"{vm:g}"})
        x.tags.update(code=15, vmem=vm)
        s["vmem"].append(x)
    for cn, t in dc.CORNERS:
        x = mk(a, v, "pvt", f"{cn}_{t}C", WEIGHT[4], corner=cn, temp=t)
        x.tags["code"] = 4
        s["pvt"].append(x)
    for sd in range(1, a.mc + 1):
        x = mk(a, v, "mc", f"seed{sd}", WEIGHT[4], seed=sd)
        x.tags["code"] = 4
        s["mc"].append(x)
    return s


def metrics(c):
    r = c.results
    if r.get("qe_tot") is None or not r.get("qin"):
        return None
    n = int(r["npulse"])
    m = dict(c.tags)
    m.update(case=c, corner=c.corner, temp=c.temp, qin=r["qin"], qe=r["qe_tot"], qi=r["qi_tot"],
             ge=r["qe_tot"] / (n * r["qin"]), gi=r["qi_tot"] / (n * r["qin"]),
             qek=[r.get(f"qe{k}") for k in range(1, n + 1)], qik=[r.get(f"qi{k}") for k in range(1, n + 1)],
             tau_e=r.get("tau_e"), tau_i=r.get("tau_i"), pe=r.get("pe"), pi=r.get("pi"),
             vsum=min(r.get("vsum_e_min") or 9, r.get("vsum_i_min") or 9), n=n)
    m["ratio"] = m["qi"] / m["qe"] if m["qe"] else None
    return m


def fC(x):
    return "-" if x is None else f"{x * 1e15:.4g}"


def ms_(x):
    return "-" if x is None or x < 0 else f"{x * 1e3:.3g}"


def write_md(path, by, a, variant, note):
    L = [f"# {path.stem}: synapses driven by DAC-like current pulses", "",
         f"Generated by `run_dpi_pulse.py` on {datetime.datetime.now():%Y-%m-%d %H:%M}. Excitatory `{a.cell}`, "
         f"inhibitory `DPI_inh`, *{a.bias}* biases (Vthr {dc.BIASES[a.bias][0]} V, vtau {dc.BIASES[a.bias][1]} V; "
         f"{dc.BIASES[a.bias][3]})" + (f", post-layout ({note})" if variant == "pex" else "") +
         ". Input: code x 15 nA (DAC branches 1:2:3:4) for 10 us; outputs held at 0.5 V unless stated. "
         "*Gain*: charge delivered to the membrane / input charge, over the whole response (3 ms after the "
         "last pulse). *i / e*: inhibitory charge removed / excitatory charge delivered.", ""]
    if by.get("code"):
        L += ["## Gain vs weight (one pulse, tt 27 C)", "",
              "| code | units | charge in (fC) | excitatory out (fC) | gain | inhibitory out (fC) | gain | i / e | "
              "decay time (ms) | peak out (nA) | lowest V(Isum) (V) |", "|" + "---|" * 11]
        for m in by["code"]:
            L.append(f"| {m['code']} | {m['units']} | {fC(m['qin'])} | {fC(m['qe'])} | {m['ge']:.3g} | {fC(m['qi'])} | "
                     f"{m['gi']:.3g} | {m['ratio']:.3f} | {ms_(m['tau_e'])} | {m['pe'] * 1e9:.3g} | {m['vsum']:.3f} |")
        dead = [m["code"] for m in by["code"] if m["ge"] < 0.01]
        live = [m for m in by["code"] if m["ge"] >= 0.01]
        L += [""]
        if dead:
            L += [f"Codes {', '.join(map(str, dead))}: less than 1 % of the input charge reaches the membrane "
                  "(a single pulse that small does not get through the DPI)."]
        if len(live) >= 2:
            L += [f"Codes {live[0]['code']}-{live[-1]['code']}: gain {live[0]['ge']:.3g} to {live[-1]['ge']:.3g} "
                  f"({live[-1]['ge'] / live[0]['ge']:.2f}x; 1 = charge out proportional to charge in)."]
        L += [""]
    if by.get("train"):
        L += ["## Trains: 10 pulses at 5 kHz", "",
              "| code | charge per pulse, pulses 1 / 2 / 5 / 10 (fC) | pulse 10 / pulse 1 | total gain | i / e |",
              "|---|---|---|---|---|"]
        for m in by["train"]:
            q = m["qek"]
            L.append(f"| {m['code']} | {fC(q[0])} / {fC(q[1])} / {fC(q[4])} / {fC(q[9])} | {q[9] / q[0]:.2f} | "
                     f"{m['ge']:.3g} | {m['ratio']:.3f} |")
        L += ["", "Pulse 10's window includes the decay after the train, so compare pulses 1-9 for build-up.", ""]
    single = next((m for m in by.get("code", []) if m["code"] == 4), None)
    if by.get("pair") and single:
        L += ["## Two pulses vs one (code 4)", "",
              "| gap | excitatory: two / (2 x one) | inhibitory: two / (2 x one) |", "|---|---|---|"]
        for m in sorted(by["pair"], key=lambda m: m["gap"]):
            L.append(f"| {m['gap'] * 1e6:g} us | {m['qe'] / (2 * single['qe']):.3f} | {m['qi'] / (2 * single['qi']):.3f} |")
        L += ["", "Above 1: the second input adds more than the first (the synapse rewards coincidence); "
              "1: linear; below 1: the second adds less.", ""]
    if by.get("width"):
        w = sorted(by["width"], key=lambda m: m["tpw"])
        if len(w) == 2:
            L += ["## Input width (code 4)", "",
                  f"16.5 us instead of 10 us (1.65x the input charge, as a real neuron spike delivers through the DAC) "
                  f"gives {w[1]['qe'] / w[0]['qe']:.2f}x the excitatory and {w[1]['qi'] / w[0]['qi']:.2f}x the "
                  f"inhibitory output charge.", ""]
    if by.get("vmem"):
        L += ["## Membrane voltage (one code-15 pulse)", "", "| VMEM (V) | excitatory out (fC) | inhibitory out (fC) | i / e |",
              "|---|---|---|---|"]
        for m in sorted(by["vmem"], key=lambda m: m["vmem"]):
            L.append(f"| {m['vmem']:g} | {fC(m['qe'])} | {fC(m['qi'])} | {m['ratio']:.3f} |")
        L.append("")
    if by.get("pvt"):
        L += ["## Corners and temperature (one code-4 pulse)", "",
              "| corner | T (C) | excitatory gain | inhibitory gain | i / e | decay time (ms) | lowest V(Isum) (V) |",
              "|---|---|---|---|---|---|---|"]
        for m in by["pvt"]:
            L.append(f"| {m['corner']} | {m['temp']:g} | {m['ge']:.3g} | {m['gi']:.3g} | {m['ratio']:.3f} | "
                     f"{ms_(m['tau_e'])} | {m['vsum']:.3f} |")
        ge = [m["ge"] for m in by["pvt"]]
        L += ["", f"Excitatory gain across corners: {min(ge):.3g} to {max(ge):.3g} ({max(ge) / min(ge):.3g}x).", ""]
    if by.get("mc"):
        ms = by["mc"]
        L += [f"## Device mismatch (one code-4 pulse, {len(ms)} samples)", "",
              "| quantity | mean | std dev | std / mean | min | max |", "|---|---|---|---|---|---|"]
        for key, name in (("ge", "excitatory gain"), ("gi", "inhibitory gain"), ("ratio", "i / e")):
            xs = [m[key] for m in ms]
            L.append(f"| {name} | {statistics.mean(xs):.4g} | {statistics.stdev(xs):.3g} | "
                     f"{statistics.stdev(xs) / statistics.mean(xs):.2f} | {min(xs):.4g} | {max(xs):.4g} |")
        L.append("")
    L += [f"Every run: `{path.stem}.csv`. Logs and waveforms: `runs/dpipulse_{variant}_{a.cell}_{a.bias}_*/`."]
    path.write_text("\n".join(L) + "\n")


def write_csv(path, by):
    keys = ["suite", "corner", "temp", "code", "units", "qin", "qe", "qi", "ge", "gi", "ratio", "tau_e", "tau_i",
            "pe", "pi", "vsum", "n"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(keys + ["gap", "tpw", "vmem", "seed"])
        for s, ms in by.items():
            for m in ms:
                w.writerow([m.get(k, "") if m.get(k) is not None else "" for k in keys] +
                           [m.get("gap", ""), m.get("tpw", ""), m.get("vmem", ""), m["case"].seed or ""])


def plot(path, by, a):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), facecolor=dc.SURF)
    for ax in axs:
        dc.style(ax)
    a0 = axs[0]
    if by.get("code"):
        ms = by["code"]
        a0.plot([m["qin"] * 1e15 for m in ms], [m["ge"] for m in ms], color=dc.SERIES[0], lw=2, marker="o",
                ms=6, mec=dc.SURF, mew=1.5, label="excitatory")
        a0.plot([m["qin"] * 1e15 for m in ms], [m["gi"] for m in ms], color=dc.SERIES[1], lw=2, ls=":",
                marker="s", ms=6, mec=dc.SURF, mew=1.5, label="inhibitory")
        a0.set_xscale("log")
        a0.set_xlabel("Input charge per pulse (fC)", color=dc.INK2)
        a0.set_ylabel("Gain: charge out / charge in", color=dc.INK2)
        a0.set_title("Gain vs weight (one pulse)", color=dc.INK, loc="left", fontsize=10)
        a0.legend(frameon=False, labelcolor=dc.INK2, fontsize=8)
    a1 = axs[1]
    for m, color in zip(by.get("train", []), dc.SERIES):
        q = m["qek"][:9]
        a1.plot(range(1, 10), [x / q[0] for x in q], color=color, lw=2, marker="o", ms=5, mec=dc.SURF,
                label=f"code {m['code']}")
    a1.axhline(1, color=dc.INK2, lw=1, ls="--")
    a1.set_xlabel("Pulse number (5 kHz train)", color=dc.INK2)
    a1.set_ylabel("Excitatory charge / charge of pulse 1", color=dc.INK2)
    a1.set_title("Build-up during a train", color=dc.INK, loc="left", fontsize=10)
    if by.get("train"):
        a1.legend(frameon=False, labelcolor=dc.INK2, fontsize=8)
    a2 = axs[2]
    single = next((m for m in by.get("code", []) if m["code"] == 4), None)
    if by.get("pair") and single:
        ms = sorted(by["pair"], key=lambda m: m["gap"])
        a2.plot([m["gap"] * 1e6 for m in ms], [m["qe"] / (2 * single["qe"]) for m in ms], color=dc.SERIES[0], lw=2,
                marker="o", ms=6, mec=dc.SURF, label="excitatory")
        a2.axhline(1, color=dc.INK2, lw=1, ls="--")
        a2.set_xscale("log")
        a2.set_xlabel("Time between the two pulses (us)", color=dc.INK2)
        a2.set_ylabel("Charge of two / (2 x charge of one)", color=dc.INK2)
        a2.set_title("Two inputs vs one (code 4)", color=dc.INK, loc="left", fontsize=10)
    fig.suptitle(f"{a.cell} / DPI_inh driven by DAC-like pulses ({a.bias} biases, tt 27 C)", color=dc.INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=dc.SURF)
    plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cell", choices=dc.CELLS, default="DPI_sized")
    ap.add_argument("--bias", choices=list(dc.BIASES), default="output")
    ap.add_argument("--only", help="comma-separated suites: code,train,pair,width,vmem,pvt,mc")
    ap.add_argument("--mc", type=int, default=50)
    ap.add_argument("--pex", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    variant = "pex" if a.pex else "sch"
    all_cases = suites(a, variant)
    chosen = a.only.split(",") if a.only else list(all_cases)
    note = ""
    if not a.report_only:
        text, note = dc.prepare_netlist(HERE / f"{TB}.sch", dc.RUNS / f"netlist_pulse_{variant}_{a.cell}", a.cell, a.pex)
        cases = [c for s in chosen for c in all_cases[s]]
        print(f"{variant} {a.cell} {a.bias}: {len(cases)} runs ({', '.join(chosen)}), {a.jobs} at a time")
        dc.run_and_save(cases, {TB: text}, a.jobs)
    names = {c.name for s in all_cases.values() for c in s}
    by = {}
    for c in dc.load_runs(f"dpipulse_{variant}_{a.cell}_{a.bias}_"):
        if c.name in names and c.ok:
            m = metrics(c)
            if m:
                by.setdefault(c.tags["suite"], []).append(m)
    order = ["tt", "ss", "ff", "sf", "fs"]
    for s in by:
        by[s].sort(key=lambda m: (m.get("code") or 0, order.index(m["corner"]), m["temp"], m["case"].seed or 0))
    dc.RESULTS.mkdir(exist_ok=True)
    stem = dc.stem(TB, a.cell, a.bias, a.pex)
    write_csv(dc.RESULTS / f"{stem}.csv", by)
    write_md(dc.RESULTS / f"{stem}.md", by, a, variant, note)
    plot(dc.RESULTS / f"{stem}.png", by, a)
    print(f"wrote {dc.RESULTS / (stem + '.md')} and .csv ({sum(len(v) for v in by.values())} runs)")


if __name__ == "__main__":
    main()
