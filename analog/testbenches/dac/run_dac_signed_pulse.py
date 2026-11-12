"""DAC_signed switched by its enable (dac_signed_pulse_tb.sch): the charge each input spike delivers.

    python3 analog/testbenches/dac/run_dac_signed_pulse.py                # all suites, schematic
    python3 analog/testbenches/dac/run_dac_signed_pulse.py --pex          # post-layout (needs an extraction)
    python3 analog/testbenches/dac/run_dac_signed_pulse.py --only pulse,spike
    python3 analog/testbenches/dac/run_dac_signed_pulse.py --report-only  # rebuild the report from runs/

Run inside the container. In the network the DAC's enable is switched by every
input spike, so what reaches the synapse is a charge packet per spike, not a DC
current. Five spikes every 200 us per run (the network's 5 kHz input rate);
the outputs are held at 2.5 V (stand-ins for the DPI tails). Suites:

  pulse   ideal 10 us enable pulses with 10 ns edges (as from the digital pulse
          generator), codes 1, 2, 4, 7, 8, 15 x both signs. Charge per pulse vs
          on-current x width: the excess is charge injection and the charging of
          the DAC's internal node X at the edges                              (12 runs)
  spike   the same codes with the enable driven by a real neuron spike (shape from
          --spike-from, default neuron/results/neuron_nominal_tb.txt, spike 3,
          repeated): how much more a spike delivers than an ideal 10 us pulse,
          as for the hidden and output layers, whose DACs are enabled by the
          previous layer's spikes                                              (12 runs)
  width   enable pulses 2-50 us at codes 1 and 15: a straight-line fit
          q = I_on x width + q_fixed separates the per-pulse fixed charge     (10 runs)
  pvt_pulse   ideal 10 us pulses at codes 1 and 15 (s = 0), corners tt/ss/ff/sf/fs x
          0/27/85 C: charge per pulse, and the leakage while the enable is off,
          as charge per 200 us period                                         (30 runs)
  pvt_spike   the same codes with the enable driven by one full period of the
          neuron's own waveform at the same corner and temperature (from
          neuron/runs/robust_sch_pvt_<corner>_<T>C/, run_neuron_robust.py); corners
          where the neuron does not fire are skipped                          (up to 30 runs)

--pex swaps DAC_signed for its extraction (analog/neuron/layout/PEX/). Each run is in
runs/dac_signed_pulse_<sch|pex>_<suite>_<x>/. Writes, in results/ (post-layout: __pex):
  dac_signed_pulse_tb[__pex].md / .csv     report and one row per run
  dac_signed_pulse_tb.png                  excess charge per code; width fit
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

TB = "dac_signed_pulse_tb"
CELL = "DAC_signed"
RESULTS = HERE / "results"
RUNS = HERE / "runs"
SPIKE_DEFAULT = HERE.parent / "neuron" / "results" / "neuron_nominal_tb.txt"
NEURON_RUNS = HERE.parent / "neuron" / "runs"
TPER, T0, NPULSE = 200e-6, 50e-6, 5
CODES = [1, 2, 4, 7, 8, 15]
WIDTHS = [2e-6, 5e-6, 10e-6, 20e-6, 50e-6]
WEIGHT = {c: sum(wb * ((c >> b) & 1) for b, wb in enumerate((1, 2, 3, 4))) for c in range(16)}  # 1:2:3:4


# --- the spike-shaped enable -----------------------------------------------------------

def spike_pwl(path: Path, index=3, vfloor=0.02, full_period=False):
    """PWL points (t from 0, v) of spike number `index` in a wrdata file (time, ..., v(spike)).

    full_period=False: from where the spike rises above vfloor until it is back below it.
    full_period=True: one whole neuron period, from just before spike `index` rises to
    just before spike `index`+1 rises (for spikes that never fall back to 0 V or last
    longer than the input period). Returns (points, length)."""
    rows = [line.split() for line in path.read_text().splitlines()]
    names = [n.lower() for n in rows[0]]
    col = names.index("v(spike)")
    data = [(float(r[0]), float(r[col])) for r in rows[1:] if len(r) == len(names)]
    t = [d[0] for d in data]
    v = [d[1] for d in data]
    ups = [i for i in range(1, len(t)) if v[i - 1] < 1.65 <= v[i]]
    if len(ups) < index:
        raise SystemExit(f"{path}: fewer than {index} spikes")
    def start_of(k):
        st = k
        while st > 0 and v[st] > vfloor and v[st] > v[st - 1]:
            st -= 1
        return st
    i = ups[index - 1]
    st = start_of(i)
    if full_period:
        if len(ups) < index + 1:
            raise SystemExit(f"{path}: fewer than {index + 1} spikes")
        en = start_of(ups[index]) - 1
    else:
        en = i
        while en < len(t) - 1 and not (v[en] < vfloor and t[en] - t[i] > 5e-6):
            en += 1
    v0 = v[st] if full_period else 0.0
    pts, last = [(0.0, v0)], (0.0, v0)
    for j in range(st + 1, en):
        tt, vv = t[j] - t[st], v[j]
        if abs(vv - last[1]) > 0.01 or tt - last[0] > 0.5e-6:
            pts.append((tt, vv))
            last = (tt, vv)
    pts.append((t[en] - t[st], v[en] if full_period else 0.0))
    return pts, t[en] - t[st]


def spike_source_line(pts, tper=TPER):
    body = " ".join(f"{tt:.4e} {vv:.4f}" for tt, vv in pts)
    # pts starts at t = 0; time points must strictly increase, or ngspice aborts
    # where the waveform repeats. One period ends at tper with the start value.
    if tper > pts[-1][0] + 1e-9:
        body += f" {tper:.4e} {pts[0][1]:.4f}"
    return f"Ven en 0 PWL({body}) r=0 td={T0:.4e}"


def spike_netlist(text, pts, tper=TPER):
    lines = text.splitlines()
    idx = [i for i, line in enumerate(lines) if line.startswith("Ven ")]
    if len(idx) != 1:
        raise RuntimeError("expected one 'Ven' line in the netlist")
    lines[idx[0]] = spike_source_line(pts, tper)
    return "\n".join(lines) + "\n"


# --- conditions -------------------------------------------------------------------------

def case(v, suite, label, tbkey, params, tags, corner="tt", temp=27):
    p = {"p_tper": f"{TPER:g}", "p_t0": f"{T0:g}", "p_npulse": str(NPULSE)}
    p.update(params)
    t = dict(suite=suite, label=label, corner=corner, temp=temp, tper=float(p["p_tper"]))
    t.update(tags)
    return tb.Case(name=f"dac_signed_pulse_{v}_{suite}_{label}", tb=tbkey, params=p,
                   corner=corner, temp=temp, tags=t)


def suite_pulse(v, a):
    return [case(v, "pulse", f"c{c}_s{s}", TB, {"p_code": str(c), "p_s": str(s), "p_tpw": "10u"},
                 {"code": c, "s": s, "tpw": 10e-6}) for c in CODES for s in (0, 1)]


def suite_spike(v, a):
    return [case(v, "spike", f"c{c}_s{s}", TB + "_spike", {"p_code": str(c), "p_s": str(s), "p_tpw": "10u"},
                 {"code": c, "s": s, "tpw": None}) for c in CODES for s in (0, 1)]


def suite_width(v, a):
    return [case(v, "width", f"c{c}_w{w * 1e6:g}us", TB, {"p_code": str(c), "p_s": "0", "p_tpw": f"{w:g}"},
                 {"code": c, "s": 0, "tpw": w}) for c in (1, 15) for w in WIDTHS]


CORNERS = [(c, t) for c in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]
PVT_CODES = (1, 15)


def suite_pvt_pulse(v, a):
    return [case(v, "pvt_pulse", f"{cn}_{t}C_c{c}", TB, {"p_code": str(c), "p_s": "0", "p_tpw": "10u"},
                 {"code": c, "s": 0, "tpw": 10e-6}, corner=cn, temp=t)
            for cn, t in CORNERS for c in PVT_CODES]


def suite_pvt_spike(v, a):
    out = []
    for (cn, t), (pts, per) in sorted(a.corner_spikes.items()):
        tper = max(TPER, per)
        out += [case(v, "pvt_spike", f"{cn}_{t}C_c{c}", f"{TB}_spike_{cn}_{t}C",
                     {"p_code": str(c), "p_s": "0", "p_tpw": "10u", "p_tper": f"{tper:.6g}"},
                     {"code": c, "s": 0, "tpw": None, "neuron_period": per,
                      "spike_above_vsw": spike_above(pts)}, corner=cn, temp=t)
                for c in PVT_CODES]
    return out


def spike_above(pts, vsw=1.65):
    above = [tt for tt, vv in pts if vv >= vsw]
    return (max(above) - min(above)) if above else 0.0


SUITES = {"pulse": suite_pulse, "spike": suite_spike, "width": suite_width,
          "pvt_pulse": suite_pvt_pulse, "pvt_spike": suite_pvt_spike}


# --- analysis and report ------------------------------------------------------------------

def metrics(c):
    r = c.results
    n = int(r.get("npulse") or 0)
    qs = [r.get(f"q{k}") for k in range(1, n + 1)]
    qo = [r.get(f"qo{k}") for k in range(1, n + 1)]
    if n < 2 or any(q is None for q in qs):
        return None
    m = dict(c.tags)
    # runs saved before the corner suites existed have no corner/period tags: tt, 27 C, 200 us
    m.setdefault("corner", "tt")
    m.setdefault("temp", 27)
    m.setdefault("tper", TPER)
    m["q"] = statistics.mean(qs[1:])                 # pulses 2..N (pulse 1 starts from idle)
    m["q_spread"] = (max(qs[1:]) - min(qs[1:])) / m["q"] if m["q"] else 0
    m["q_other"] = max(abs(x) for x in qo)
    m["i_on"], m["t_settle"], m["i_peak"] = r.get("i_on"), r.get("t_settle"), r.get("i_peak")
    m["en_max"] = r.get("en_max")
    m["i_idle"] = r.get("i_idle")
    m["q_leak"] = (r.get("i_idle") or 0) * m["tper"]   # leakage while en is off, per period
    m["w"] = WEIGHT[m["code"]]
    if m["tpw"]:
        m["q_ideal"] = m["i_on"] * m["tpw"]
        m["excess"] = m["q"] - m["q_ideal"]
    return m


def fC(x):
    return "-" if x is None else f"{x * 1e15:.4g}"


def write_md(path, ms, variant, note, spike_note):
    pulse = {(m["code"], m["s"]): m for m in ms if m["suite"] == "pulse"}
    spike = {(m["code"], m["s"]): m for m in ms if m["suite"] == "spike"}
    width = [m for m in ms if m["suite"] == "width"]
    L = [f"# {TB}{'__pex' if variant == 'pex' else ''}: DAC_signed switched by its enable", "",
         f"Generated by `run_dac_signed_pulse.py{' --pex' if variant == 'pex' else ''}` on "
         f"{datetime.datetime.now():%Y-%m-%d %H:%M}. Cell: "
         + ("post-layout extraction (" + note + ")" if variant == "pex" else "schematic `analog/neuron/DAC_signed.sch`")
         + f". tt, 27 C, Iref 14.42 nA, outputs held at 2.5 V, {NPULSE} enables every {TPER * 1e6:g} us; "
         "charge per enable = mean of enables 2-5, leakage removed.", ""]
    if pulse:
        L += ["## Ideal 10 us enable pulses (10 ns edges)", "",
              "| code | weight | sign | on-current (nA) | charge (fC) | on-current x 10 us (fC) | excess (fC) | excess | "
              "settling to 1 % (ns) | to the other output (fC) |", "|" + "---|" * 10]
        for (c, s), m in sorted(pulse.items()):
            L.append(f"| {c} | {m['w']} | {'-' if s else '+'} | {m['i_on'] * 1e9:.4g} | {fC(m['q'])} | {fC(m['q_ideal'])} | "
                     f"{fC(m['excess'])} | {m['excess'] / m['q_ideal'] * 100:+.1f} % | {m['t_settle'] * 1e9:.3g} | "
                     f"{m['q_other'] * 1e15:.2g} |")
        L.append("")
    if spike:
        L += ["## Enable driven by a neuron spike", "", spike_note, "",
              "| code | weight | sign | charge (fC) | ideal 10 us pulse (fC) | spike / pulse | equivalent enable width (us) |",
              "|---|---|---|---|---|---|---|"]
        for (c, s), m in sorted(spike.items()):
            p = pulse.get((c, s))
            ratio = m["q"] / p["q"] if p else None
            eqw = m["q"] / p["i_on"] * 1e6 if p else None
            L.append(f"| {c} | {m['w']} | {'-' if s else '+'} | {fC(m['q'])} | {fC(p['q']) if p else '-'} | "
                     f"{ratio:.3f} | {eqw:.2f} |" if p else f"| {c} | {m['w']} | {'-' if s else '+'} | {fC(m['q'])} | - | - | - |")
        L.append("")
    if width:
        L += ["## Enable width (codes 1 and 15, s = 0)", "",
              "Straight-line fit q = I x width + q_fixed: I should match the on-current; q_fixed is the charge every "
              "enable adds on top (edges, node X).", "",
              "| code | I from the fit (nA) | on-current (nA) | q_fixed (fC) | q_fixed in units of 1 us of on-current |",
              "|---|---|---|---|---|"]
        for c in (1, 15):
            pts = sorted((m["tpw"], m["q"]) for m in width if m["code"] == c)
            if len(pts) >= 3:
                xs, ys = zip(*pts)
                mx, my = statistics.mean(xs), statistics.mean(ys)
                a = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x in xs)
                b = my - a * mx
                ion = statistics.mean(m["i_on"] for m in width if m["code"] == c)
                L.append(f"| {c} | {a * 1e9:.4g} | {ion * 1e9:.4g} | {b * 1e15:.3g} | {b / (ion * 1e-6):.2f} |")
        L += ["", "| code | width (us) | charge (fC) | on-current x width (fC) | excess |", "|---|---|---|---|---|"]
        for m in sorted(width, key=lambda m: (m["code"], m["tpw"])):
            L.append(f"| {m['code']} | {m['tpw'] * 1e6:g} | {fC(m['q'])} | {fC(m['q_ideal'])} | "
                     f"{m['excess'] / m['q_ideal'] * 100:+.1f} % |")
        L.append("")
    pp = {(m["corner"], m["temp"], m["code"]): m for m in ms if m["suite"] == "pvt_pulse"}
    ps = {(m["corner"], m["temp"], m["code"]): m for m in ms if m["suite"] == "pvt_spike"}
    if pp:
        L += ["## Corners and temperature: ideal 10 us pulses", "",
              "*Leakage per period*: the current that still flows while the enable is off, times one 200 us "
              "period, so it can be compared with the charge of one pulse. It flows whether a spike comes or not.", "",
              "| corner | T (C) | code | on-current (nA) | charge per pulse (fC) | excess | leakage, enable off (pA) | "
              "leakage per period (fC) | leakage / pulse charge |", "|" + "---|" * 9]
        for k in sorted(pp, key=lambda k: (["tt", "ss", "ff", "sf", "fs"].index(k[0]), k[1], k[2])):
            m = pp[k]
            L.append(f"| {k[0]} | {k[1]} | {k[2]} | {m['i_on'] * 1e9:.4g} | {fC(m['q'])} | "
                     f"{m['excess'] / m['q_ideal'] * 100:+.1f} % | {m['i_idle'] * 1e12:.3g} | {fC(m['q_leak'])} | "
                     f"{m['q_leak'] / m['q'] * 100:.2g} % |")
        L.append("")
    if ps:
        L += ["## Corners and temperature: enable driven by the neuron's spike at that corner", "",
              "| corner | T (C) | code | neuron period (us) | spike above 1.65 V (us) | charge per spike (fC) | "
              "ideal 10 us pulse, same corner (fC) | spike / pulse | equivalent enable width (us) |", "|" + "---|" * 9]
        for k in sorted(ps, key=lambda k: (["tt", "ss", "ff", "sf", "fs"].index(k[0]), k[1], k[2])):
            m, p = ps[k], pp.get(k)
            L.append(f"| {k[0]} | {k[1]} | {k[2]} | {m['neuron_period'] * 1e6:.4g} | {m['spike_above_vsw'] * 1e6:.3g} | "
                     f"{fC(m['q'])} | {fC(p['q']) if p else '-'} | {(m['q'] / p['q']) if p else float('nan'):.3g} | "
                     f"{(m['q'] / p['i_on'] * 1e6) if p else float('nan'):.3g} |")
        L.append("")
    L += [f"Every run: `{path.stem}.csv`. Netlists, logs and waveforms (isel, ioth, v(en)): "
          f"`runs/dac_signed_pulse_{variant}_*/`."]
    path.write_text("\n".join(L) + "\n")


def write_csv(path, ms):
    keys = ["suite", "corner", "temp", "code", "w", "s", "tpw", "tper", "i_on", "q", "q_ideal", "excess",
            "q_spread", "q_other", "i_idle", "q_leak", "t_settle", "i_peak", "en_max", "neuron_period",
            "spike_above_vsw"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for m in ms:
            w.writerow({k: ("" if m.get(k) is None else m.get(k)) for k in keys})


def plot(ms, stem):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: no plot")
        return
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(True, color=grid, lw=0.8)
        for sp in ax.spines.values():
            sp.set_color(grid)
        ax.tick_params(colors=ink2)
    pulse = {(m["code"], m["s"]): m for m in ms if m["suite"] == "pulse"}
    spike = {(m["code"], m["s"]): m for m in ms if m["suite"] == "spike"}
    a = axs[0]
    a.axhline(1, color=ink2, lw=1, ls="--")
    for data, label, color, marker in ((pulse, "ideal 10 us pulse", "#2a78d6", "o"),
                                       (spike, "neuron spike", "#eb6834", "s")):
        for s, ls in ((0, "-"), (1, ":")):
            pts = []
            for c in CODES:
                m, p = data.get((c, s)), pulse.get((c, s))
                if m and p:
                    pts.append((m["w"], m["q"] / (p["i_on"] * 10e-6)))
            if pts:
                a.plot(*zip(*sorted(pts)), color=color, lw=2, ls=ls, marker=marker, ms=6, mec=surf, mew=1.5,
                       label=f"{label}, {'Isum_i' if s else 'Isum_e'}")
    a.set_xlabel("Weight (units of the 1:2:3:4 DAC)", color=ink2)
    a.set_ylabel("Charge / (on-current x 10 us)", color=ink2)
    a.set_title("Charge per enable, relative to an ideal 10 us window", color=ink, loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8)
    a = axs[1]
    width = [m for m in ms if m["suite"] == "width"]
    for c, color, marker in ((1, "#2a78d6", "o"), (15, "#eb6834", "s")):
        pts = sorted((m["tpw"] * 1e6, m["q"] / m["i_on"] * 1e6) for m in width if m["code"] == c)
        if pts:
            a.plot(*zip(*pts), color=color, lw=2, marker=marker, ms=6, mec=surf, mew=1.5, label=f"code {c}")
    a.plot([0, 50], [0, 50], color=ink2, lw=1, ls="--", label="charge = on-current x width")
    a.set_xlabel("Enable width (us)", color=ink2)
    a.set_ylabel("Charge / on-current (us)", color=ink2)
    a.set_title("Charge vs enable width (the offset is the fixed charge per enable)", color=ink, loc="left", fontsize=10)
    a.legend(frameon=False, labelcolor=ink2, fontsize=8)
    fig.suptitle("DAC_signed switched by its enable (tt, 27 C)", color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{stem}.png", dpi=150, facecolor=surf)
    plt.close(fig)
    print(f"wrote {RESULTS / (stem + '.png')}")

    pp = {(m["corner"], m["temp"], m["code"]): m for m in ms if m["suite"] == "pvt_pulse"}
    ps = {(m["corner"], m["temp"], m["code"]): m for m in ms if m["suite"] == "pvt_spike"}
    if not pp:
        return
    corners = [("tt", "#2a78d6", "o"), ("ss", "#eb6834", "s"), ("ff", "#1baf7a", "^"),
               ("sf", "#eda100", "D"), ("fs", "#e87ba4", "v")]
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(True, color=grid, lw=0.8)
        for sp in ax.spines.values():
            sp.set_color(grid)
        ax.tick_params(colors=ink2)
    for cn, color, marker in corners:
        pts = [(t, pp[(cn, t, 1)]["q_leak"] / pp[(cn, t, 1)]["q"] * 100) for t in (0, 27, 85) if (cn, t, 1) in pp]
        pts = [(t, max(y, 1e-6)) for t, y in pts]
        if pts:
            axs[0].plot(*zip(*pts), color=color, lw=2, marker=marker, ms=7, mec=surf, mew=1.5, label=cn)
        pts = [(t, ps[(cn, t, 1)]["q"] / pp[(cn, t, 1)]["q"]) for t in (0, 27, 85)
               if (cn, t, 1) in ps and (cn, t, 1) in pp]
        if pts:
            axs[1].plot(*zip(*pts), color=color, lw=2, marker=marker, ms=7, mec=surf, mew=1.5, label=cn)
    axs[0].set_yscale("log")
    axs[0].set_xticks([0, 27, 85])
    axs[0].set_xlabel("Temperature (C)", color=ink2)
    axs[0].set_ylabel("Leakage per 200 us / charge of one pulse (%)", color=ink2)
    axs[0].set_title("Leakage while the enable is off, code 1", color=ink, loc="left", fontsize=10)
    axs[0].legend(frameon=False, labelcolor=ink2, fontsize=8, ncol=2)
    axs[1].axhline(1, color=ink2, lw=1, ls="--")
    axs[1].set_yscale("log")
    axs[1].set_xticks([0, 27, 85])
    axs[1].set_xlabel("Temperature (C)", color=ink2)
    axs[1].set_ylabel("Charge per neuron spike / per ideal 10 us pulse", color=ink2)
    axs[1].set_title("Spike-driven enable vs ideal pulse, code 1, same corner", color=ink, loc="left", fontsize=10)
    axs[1].legend(frameon=False, labelcolor=ink2, fontsize=8, ncol=2)
    fig.suptitle("DAC_signed switched by its enable: corners and temperature", color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{stem}_pvt.png", dpi=150, facecolor=surf)
    plt.close(fig)
    print(f"wrote {RESULTS / (stem + '_pvt.png')}")


def report(done, variant, note, spike_note):
    ms = [m for m in (metrics(c) for c in done if c.ok) if m]
    bad = [c.name for c in done if not c.ok or not metrics(c)]
    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}{'__pex' if variant == 'pex' else ''}"
    write_csv(RESULTS / f"{stem}.csv", ms)
    write_md(RESULTS / f"{stem}.md", ms, variant, note, spike_note)
    print(f"wrote {RESULTS / (stem + '.md')} and .csv ({len(ms)} runs analysed)")
    if bad:
        print("runs without results (see runs/<name>/ngspice.log):", ", ".join(bad))
    plot(ms, stem)


def save_tags(c, spike_note):
    d = RUNS / c.name
    if d.exists():
        (d / "case.json").write_text(json.dumps({"tags": c.tags, "tb": c.tb, "spike_note": spike_note}))


def load_runs(variant, suites):
    done, note = [], ""
    for j in sorted(RUNS.glob(f"dac_signed_pulse_{variant}_*/case.json")):
        info = json.loads(j.read_text())
        if info["tags"]["suite"] not in suites:
            continue
        c = tb.Case(name=j.parent.name, tb=info["tb"], tags=info["tags"])
        log = j.parent / "ngspice.log"
        c.log = log.read_text() if log.exists() else ""
        c.results = tb.parse_results(c.log)
        c.ok = bool(c.results) and "aborted" not in c.log
        note = info.get("spike_note") or note
        done.append(c)
    return done, note


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of DAC_signed")
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--spike-from", type=Path, default=SPIKE_DEFAULT,
                    help="wrdata file with a v(spike) column for the spike suite (default: %(default)s)")
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
        done, spike_note = load_runs(variant, suites)
        if not done:
            raise SystemExit(f"no runs in {RUNS}/dac_signed_pulse_{variant}_*")
        note = tbpex.pex_note((RUNS / done[0].name / f"{done[0].tb}.spice").read_text()) if a.pex else ""
        report(done, variant, note, spike_note)
        return

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / f"netlist_pulse_{variant}").read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    tb.check_connected(text, CELL)
    note = ""
    if a.pex:
        text = tbpex.use_pex(text, CELL)
        note = tbpex.pex_note(text)
    netlists = {TB: text}
    spike_note = ""
    if "spike" in suites:
        pts, _ = spike_pwl(a.spike_from)
        netlists[TB + "_spike"] = spike_netlist(text, pts)
        dur = pts[-1][0]
        above = [tt for tt, vv in pts if vv >= 1.65]
        spike_note = (f"Enable shape: spike 3 of `{a.spike_from.relative_to(tb.ROOT) if a.spike_from.is_relative_to(tb.ROOT) else a.spike_from}` "
                      f"(schematic neuron unless that file says otherwise), {len(pts)} PWL points, "
                      f"{dur * 1e6:.1f} us from start to below 20 mV, above 1.65 V for "
                      f"{(max(above) - min(above)) * 1e6:.1f} us, peak {max(v for _, v in pts):.2f} V; repeated every "
                      f"{TPER * 1e6:g} us. *Equivalent enable width*: the charge divided by the on-current.")

    a.corner_spikes = {}
    if "pvt_spike" in suites:
        skipped = []
        for cn, t in CORNERS:
            f = NEURON_RUNS / f"robust_sch_pvt_{cn}_{t}C" / "neuron_nominal_tb.txt"
            try:
                pts, per = spike_pwl(f, full_period=True)
            except (SystemExit, FileNotFoundError, ValueError) as e:
                skipped.append(f"{cn} {t} C ({'no waveform' if isinstance(e, FileNotFoundError) else 'too few spikes'})")
                continue
            a.corner_spikes[(cn, t)] = (pts, per)
            netlists[f"{TB}_spike_{cn}_{t}C"] = spike_netlist(text, pts, max(TPER, per))
        if skipped:
            print("pvt_spike: no neuron waveform for", ", ".join(skipped),
                  "(run run_neuron_robust.py --only pvt first, or the neuron does not fire there)")
        spike_note = (spike_note + " " if spike_note else "") + (
            "Corner suites: the enable is one full period of the neuron's waveform at the same corner and "
            "temperature (neuron/runs/robust_sch_pvt_*, schematic neuron, 9.5 nA DC), repeated every "
            "max(200 us, neuron period)."
            + (f" Skipped: {', '.join(skipped)}." if skipped else ""))

    cases = [c for s in suites for c in SUITES[s](variant, a)]
    print(f"{variant}: {len(cases)} runs ({', '.join(suites)}), {a.jobs} at a time")
    done = tb.run_cases(cases, netlists, RUNS, jobs=a.jobs)
    for c in done:
        save_tags(c, spike_note)
    # Report on every run of this variant in runs/, so a run with --only adds to the
    # report instead of replacing the other suites
    everything, _ = load_runs(variant, list(SUITES))
    report(everything, variant, note, spike_note)


if __name__ == "__main__":
    main()
