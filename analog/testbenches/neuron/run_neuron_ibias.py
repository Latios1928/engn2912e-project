"""Bias-current sweep for the current-biased neuron (analog/neuron/neuron.sch).

    python3 analog/testbenches/neuron/run_neuron_ibias.py              # all stages
    python3 analog/testbenches/neuron/run_neuron_ibias.py --stage start
    python3 analog/testbenches/neuron/run_neuron_ibias.py --jobs 8

neuron.sch has no bias transistors: it takes six bias currents and one voltage.
  into the neuron (fed from VDD):  INA (M5, Na feedback), IKup (M4, spike pull-up)
  out of the neuron (to VSS):      Ik (M6, reset), IIp (M1, inverter 1), IKdn (M2, spike
                                   pull-down), I_ampbias (spike amplifier tail)
  voltage:                         Vlk (gate of the leak M11)

An ideal current source cannot feed a switched pin (INA, IKup, Ik, IIp, IKdn are off most
of the cycle, so the source would drive its node to +-infinity). Each current is fed the
way an external bias generator would feed it: an ideal reference current into a
diode-connected device, mirrored 1:1 by an identical output device on the pin. The
devices are the type and size of the transistor that used to bias that pin inside
neuron (1/1 um; 0.22/0.28 um nFET for the amplifier tail), so the starting
currents reproduce the old voltage-biased operating point. The reference branches run
from a separate 3.3 V supply and are not in p_avg (the bias generator is shared by many
neurons); the mirror output devices are. The reference currents are held constant over
corners and temperature, which is what a trimmed bias generator provides
(analog/Bias/generator: +-2 % after trim). VT stays a fixed 1.66 V and Vlk a fixed voltage.

Measurements are those of neuron_nominal_tb.sch (spikes 3-7, VDD/2 crossings), specs from
analog/neuron/sizing_context.txt. Stages:
  start  the old operating point, tt 27 C
  sens   each bias x0.5 / x0.7 / x1.4 / x2 at tt 27 C
  opt    coordinate search over the 7 biases, objective = worst-case margin over the
         15 corner/temperature points (tt/ss/ff/sf/fs x 0/27/85 C)
  final  the best set over the 15 points, and the tt-centred set for comparison
Writes results/neuron_ibias_tb.md and .csv; runs in runs/ibias_<case>/.
"""

import argparse
import csv
import json
import math
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402

TB = "neuron_ibias_tb"
SCH = tb.ROOT / "analog/neuron/neuron.sch"
# neuron.sch is netlisted through the testbench that instantiates it (xschem writes the
# cell as a .subckt only when it is a child); only the subcircuits are kept.
HOST_TB = tb.ROOT / "analog/neuron/neuron_testbench.sch"
RESULTS = HERE / "results"
RUNS = HERE / "runs"

# name -> (start value, unit, lower bound, upper bound). Start = the current each
# old bias transistor carried at the passing tt 27 C point (Analog_AI_Documentation.md,
# bias study); Vlk = the old voltage.
BIAS = {
    "p_ina":  (5.05e-6, "uA", 0.2e-6, 50e-6),
    "p_ikup": (0.55e-6, "uA", 20e-9, 10e-6),
    "p_ik":   (17.5e-6, "uA", 0.5e-6, 100e-6),
    "p_iip":  (24.0e-9, "nA", 1e-9, 1e-6),
    "p_ikdn": (34.2e-9, "nA", 5e-9, 300e-9),
    "p_iamp": (96.5e-9, "nA", 5e-9, 2e-6),
    "p_vlk":  (0.425, "V", 0.25, 0.55),
}
LABEL = {"p_ina": "INA", "p_ikup": "IKup", "p_ik": "Ik", "p_iip": "IIp",
         "p_ikdn": "IKdn", "p_iamp": "I_ampbias", "p_vlk": "Vlk"}
SCALE = {"uA": 1e6, "nA": 1e9, "V": 1}

# sizing_context.txt; margin scale for one-sided specs in brackets
SPECS = {
    "period": (190e-6, 210e-6, None),
    "t_spike": (9e-6, 11e-6, None),
    "t_refr": (10e-6, 20e-6, None),
    "v_spike_max": (2.97, None, 0.33),
    "v_reset": (None, 0.05, 0.05),
    "p_avg": (None, 1e-6, 1e-6),
}
METRICS = list(SPECS)
PVT = [(c, t) for c in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]

DECK = """* {tb}: neuron.sch biased by mirrored ideal currents (written by run_neuron_ibias.py)
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice mimcap_typical
.param p_vdd=3.3 p_iin=9.5n p_vt=1.66 p_tstop={tstop}
.param {params}
.csparam vdd_c={{p_vdd}}
.csparam tstop_c={{p_tstop}}
V1 VDD VSS {{p_vdd}}
V2 VSS 0 0
VB VDDB VSS {{p_vdd}}
Iin VDD preIN {{p_iin}}
VMEM preIN VMEM 0
VT VT VSS {{p_vt}}
VLK Vlk VSS {{p_vlk}}
x1 VSS VDD VMEM INA Vlk Ik IIp IKup IKdn I_ampbias VT spike neuron
* pFET mirrors (current into the pin): reference from VDDB, output from VDD
IRNA gNA VSS {{p_ina}}
XMRNA gNA gNA VDDB VDDB pfet_03v3 L=1u W=1u
XMONA INA gNA VDD VDD pfet_03v3 L=1u W=1u
IRKUP gKUP VSS {{p_ikup}}
XMRKUP gKUP gKUP VDDB VDDB pfet_03v3 L=1u W=1u
XMOKUP IKup gKUP VDD VDD pfet_03v3 L=1u W=1u
* nFET mirrors (current out of the pin)
IRK VDDB gK {{p_ik}}
XMRK gK gK VSS VSS nfet_03v3 L=1u W=1u
XMOK Ik gK VSS VSS nfet_03v3 L=1u W=1u
IRIP VDDB gIP {{p_iip}}
XMRIP gIP gIP VSS VSS nfet_03v3 L=1u W=1u
XMOIP IIp gIP VSS VSS nfet_03v3 L=1u W=1u
IRKDN VDDB gKDN {{p_ikdn}}
XMRKDN gKDN gKDN VSS VSS nfet_03v3 L=1u W=1u
XMOKDN IKdn gKDN VSS VSS nfet_03v3 L=1u W=1u
IRAMP VDDB gAMP {{p_iamp}}
XMRAMP gAMP gAMP VSS VSS nfet_03v3 L=0.28u W=0.22u
XMOAMP I_ampbias gAMP VSS VSS nfet_03v3 L=0.28u W=0.22u
.ic v(VMEM)=0 v(spike)=0
.control
  save v(spike) v(VMEM) i(V1) i(VMEM)
  tran 20n $&tstop_c 0 20n uic
  let vsw = vdd_c/2
  let t3 = -1
  let t4 = -1
  let t7 = -1
  let tf3 = -1
  let trst = -1
  let trel = -1
  meas tran t3 when v(spike)=$&vsw rise=3
  meas tran t4 when v(spike)=$&vsw rise=4
  meas tran t7 when v(spike)=$&vsw rise=7
  meas tran tf3 when v(spike)=$&vsw fall=3
  if t7 < 0
    echo RES fired7=0
  else
    echo RES fired7=1
    let period = (t7 - t3)/4
    let t_spike = tf3 - t3
    meas tran v_spike_max max v(spike) from=$&t3 to=$&t4
    meas tran v_reset min v(VMEM) from=$&t3 to=$&t4
    let v10 = 0.1*vdd_c
    let vrel = v_reset + 0.01
    meas tran trst when v(VMEM)=$&v10 fall=1 td=$&t3
    meas tran trel when v(VMEM)=$&vrel rise=1 td=$&tf3
    let t_refr = trel - trst
    meas tran i_avg avg i(V1) from=$&t3 to=$&t7
    let p_avg = -i_avg*vdd_c
    echo RES period=$&period
    echo RES t_spike=$&t_spike
    echo RES t_refr=$&t_refr
    echo RES v_spike_max=$&v_spike_max
    echo RES v_reset=$&v_reset
    echo RES p_avg=$&p_avg
  end
.endc
"""


def neuron_subckts() -> str:
    """The neuron and spike_amplifier subcircuits, netlisted by xschem from neuron.sch."""
    text = tb.netlist(HOST_TB, RUNS / "_netlist").read_text()
    if "\n.subckt neuron " not in text:
        raise RuntimeError(f"no .subckt neuron in the netlist of {HOST_TB}")
    return text[text.index("\n.subckt neuron "):].replace("\n.end\n", "\n")


def deck_text(subckts: str, tstop: float) -> str:
    params = " ".join(f"{k}={v[0]:.6g}" for k, v in BIAS.items())
    text = DECK.format(tb=TB, tstop=tstop, params=params)
    return text + "\n" + subckts + "\n.end\n"


def margin(m, x):
    lo, hi, scale = SPECS[m]
    if x is None:
        return -10.0
    if lo is not None and hi is not None:
        half = (hi - lo) / 2
        return min(x - lo, hi - x) / half
    if lo is not None:
        return (x - lo) / scale
    return (hi - x) / scale


def score(case):
    r = case.results
    if not case.ok or not r.get("fired7"):
        return {m: -10.0 for m in METRICS}
    return {m: margin(m, r.get(m)) for m in METRICS}


def run(points, netlist_text, jobs, tag):
    """points: list of (name, corner, temp, params). Returns the filled cases."""
    cases = [tb.Case(name=f"ibias_{tag}_{n}", tb=TB, corner=c, temp=t, params=p,
                     tags={"label": n})
             for n, c, t, p in points]
    cases = tb.run_cases(cases, {TB: netlist_text}, RUNS, jobs=jobs)
    for c in cases:
        c.tags["margins"] = score(c)
        c.tags["worst"] = min(c.tags["margins"].values())
        c.tags["pass"] = c.tags["worst"] >= 0
    return cases


def fmt_params(p):
    return {LABEL[k]: round(v * SCALE[BIAS[k][1]], 4) for k, v in p.items()}


def pvt_eval(params, netlist_text, jobs, tag):
    pts = [(f"{c}{t}", c, t, params) for c, t in PVT]
    cases = run(pts, netlist_text, jobs, tag)
    n_pass = sum(c.tags["pass"] for c in cases)
    worst = min(c.tags["worst"] for c in cases)
    # Soft objective: mean of each condition's worst margin, clipped, so that moving a
    # failing corner towards the spec counts even before it passes.
    soft = sum(max(-2.0, min(1.0, c.tags["worst"])) for c in cases) / len(cases)
    return cases, (n_pass, worst, soft)


def objective(key):
    n_pass, worst, soft = key
    return n_pass + 0.5 * soft + 0.25 * max(-2.0, worst)


def coord_search(start, netlist_text, jobs, log, rounds=4):
    best = dict(start)
    cases, key = pvt_eval(best, netlist_text, jobs, "opt0")
    best_obj = objective(key)
    log.append(dict(step="start", params=fmt_params(best), key=key, obj=best_obj))
    print(f"  start: pass {key[0]}/15 worst {key[1]:+.3f} soft {key[2]:+.3f}", flush=True)
    steps = {k: (1.6 if k != "p_vlk" else 0.03) for k in BIAS}
    it = 0
    for rnd in range(rounds):
        improved = False
        for k in BIAS:
            for direction in (+1, -1):
                trial = dict(best)
                if k == "p_vlk":
                    trial[k] = best[k] + direction * steps[k]
                else:
                    trial[k] = best[k] * steps[k] ** direction
                lo, hi = BIAS[k][2], BIAS[k][3]
                if not lo <= trial[k] <= hi:
                    continue
                it += 1
                _, tkey = pvt_eval(trial, netlist_text, jobs, f"opt{it}")
                tobj = objective(tkey)
                log.append(dict(step=f"r{rnd} {LABEL[k]} {'+' if direction > 0 else '-'}",
                                params=fmt_params(trial), key=tkey, obj=tobj))
                print(f"  r{rnd} {LABEL[k]:>9} {'up' if direction > 0 else 'dn'}: "
                      f"pass {tkey[0]}/15 worst {tkey[1]:+.3f} soft {tkey[2]:+.3f}"
                      f"{'  *' if tobj > best_obj else ''}", flush=True)
                if tobj > best_obj:
                    best, best_obj, key = trial, tobj, tkey
                    improved = True
                    break
        for k in steps:     # refine
            steps[k] = math.sqrt(steps[k]) if k != "p_vlk" else steps[k] / 2
        if not improved and rnd >= 1:
            pass
    return best, key


def table(cases, first_cols):
    hdr = first_cols + ["fires"] + [m for m in METRICS] + ["all specs"]
    units = {"period": 1e6, "t_spike": 1e6, "t_refr": 1e6, "v_spike_max": 1,
             "v_reset": 1e3, "p_avg": 1e6}
    L = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for c in cases:
        r = c.results
        fired = bool(r.get("fired7")) and c.ok
        row = [c.corner, f"{c.temp:g}"] if first_cols == ["corner", "T (C)"] else [c.tags["label"]]
        row.append("yes" if fired else "**no**")
        for m in METRICS:
            v = r.get(m) if fired else None
            s = "-" if v is None else f"{v * units[m]:.4g}"
            if fired and c.tags["margins"][m] < 0:
                s = f"**{s}**"
            row.append(s)
        row.append("PASS" if c.tags["pass"] else "**FAIL**")
        L.append("| " + " | ".join(row) + " |")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", default="all", choices=["start", "sens", "opt", "all"])
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--tstop", type=float, default=2.0e-3)
    ap.add_argument("--rounds", type=int, default=3)
    a = ap.parse_args()

    RESULTS.mkdir(exist_ok=True)
    text = deck_text(neuron_subckts(), a.tstop)
    tb.check_connected(text, "neuron")
    (RUNS / "_netlist" / f"{TB}.spice").write_text(text)
    start = {k: v[0] for k, v in BIAS.items()}
    t0 = time.time()
    report = [f"# {TB}: bias currents for neuron.sch", "",
              f"Generated by `run_neuron_ibias.py` on {time.strftime('%Y-%m-%d %H:%M')}. "
              "Neuron `analog/neuron/neuron.sch`, Iin = 9.5 nA DC, VT = 1.66 V, VDD = 3.3 V. "
              "Each bias current is an ideal reference mirrored 1:1 onto its pin "
              "(see the script's docstring); Vlk is a voltage.", "",
              "Specs (`analog/neuron/sizing_context.txt`): period 190-210 us, t_spike 9-11 us, "
              "t_refr 10-20 us, v_spike_max >= 2.97 V, v_reset <= 50 mV, p_avg <= 1 uW. "
              "Units below: us, us, us, V, mV, uW. Bold = outside the spec.", ""]
    rows = []

    # start point at tt
    cs = run([("start", "tt", 27, start)], text, a.jobs, "start")
    report += ["## Start point (old operating point as currents), tt 27 C", "",
               "`" + json.dumps(fmt_params(start)) + "`", ""] + table(cs, ["set"]) + [""]
    rows += [dict(stage="start", case=c.tags["label"], corner=c.corner, temp=c.temp,
                  **fmt_params(start), **c.results) for c in cs]
    print(f"start: {cs[0].results}  ({time.time() - t0:.0f} s)", flush=True)

    if a.stage in ("sens", "all"):
        pts = []
        for k in BIAS:
            for f in ((0.5, 0.7, 1.4, 2.0) if k != "p_vlk" else (-0.05, -0.025, 0.025, 0.05)):
                p = dict(start)
                p[k] = start[k] * f if k != "p_vlk" else start[k] + f
                pts.append((f"{LABEL[k]} {'x' + str(f) if k != 'p_vlk' else f'{f:+.3f} V'}", "tt", 27, p))
        cs = run(pts, text, a.jobs, "sens")
        report += ["## Sensitivity at tt 27 C (one bias changed from the start point)", ""] \
            + table(cs, ["set"]) + [""]
        rows += [dict(stage="sens", case=c.tags["label"], corner=c.corner, temp=c.temp,
                      **fmt_params(c.params), **c.results) for c in cs]
        print(f"sens done ({time.time() - t0:.0f} s)", flush=True)

    if a.stage in ("opt", "all"):
        log = []
        print("coordinate search over 15 PVT points:", flush=True)
        best, key = coord_search(start, text, a.jobs, log, rounds=a.rounds)
        cs, key = pvt_eval(best, text, a.jobs, "final")
        report += ["## Best set over 15 PVT points", "",
                   f"Objective: number of passing points, then the mean and worst normalized "
                   f"spec margin (1 = spec centre, 0 = spec limit). Result: **{key[0]} / 15 pass**, "
                   f"worst margin {key[1]:+.2f}.", "",
                   "`" + json.dumps(fmt_params(best)) + "`", ""] + table(cs, ["corner", "T (C)"]) + [""]
        rows += [dict(stage="final", case=f"{c.corner}{c.temp:g}", corner=c.corner, temp=c.temp,
                      **fmt_params(best), **c.results) for c in cs]
        cs0, key0 = pvt_eval(start, text, a.jobs, "startpvt")
        report += ["## Start point over 15 PVT points (for comparison)", "",
                   f"**{key0[0]} / 15 pass**, worst margin {key0[1]:+.2f}.", ""] \
            + table(cs0, ["corner", "T (C)"]) + [""]
        rows += [dict(stage="startpvt", case=f"{c.corner}{c.temp:g}", corner=c.corner, temp=c.temp,
                      **fmt_params(start), **c.results) for c in cs0]
        report += ["## Search log", "", "| step | pass | worst | soft | biases |", "|---|---|---|---|---|"]
        report += [f"| {e['step']} | {e['key'][0]} | {e['key'][1]:+.2f} | {e['key'][2]:+.2f} | "
                   f"{e['params']} |" for e in log]
        (RESULTS / f"{TB}_best.json").write_text(json.dumps(
            dict(best=fmt_params(best), units={LABEL[k]: v[1] for k, v in BIAS.items()},
                 n_pass=key[0], worst_margin=key[1]), indent=1))

    report.append(f"\nRun time {time.time() - t0:.0f} s.")
    (RESULTS / f"{TB}.md").write_text("\n".join(report) + "\n")
    keys = sorted({k for r in rows for k in r})
    with open(RESULTS / f"{TB}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {RESULTS / (TB + '.md')} ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
