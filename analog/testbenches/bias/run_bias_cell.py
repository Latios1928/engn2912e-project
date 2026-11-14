#!/usr/bin/env python3
"""Verify the current-mode bias cell (analog/neuron/bias_cell.sch).

    python3 analog/testbenches/bias/run_bias_cell.py            # all suites, ~2 min
    python3 analog/testbenches/bias/run_bias_cell.py --only neuron,dpi

Suites (all with Iref = 100 nA):
  biases  the cell's 11 output voltages at 5 corners x 0/27/85 C (schematic netlist)
  neuron  neuron_sized at 9.5 nA DC, 15 PVT points: biases as fixed voltages (as before) vs from
          the cell (VT stays a voltage). Same measurements as the sizing sweep (spikes 3-7).
  dpi     DPI (DPI.sch, minimum size) DC gain Isyn/Iw at Iw = 15 nA, VMEM = 1 V, 15 PVT points:
          Vthr / VT fixed vs from the cell
  mc      100 mismatch samples of the cell at tt 27 C (parallel copies written out, since the
          PDK mismatch model ignores m)
Writes results/bias_cell.md. Netlists come from the repo schematics through xschem.
"""
import argparse
import json
import re
import statistics as st
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import bias_design as bd  # noqa: E402

W = json.load(open(HERE / "bias_cell_sizes.json"))
RUN = Path(tempfile.mkdtemp(prefix="bias_cell_"))
(RUN / ".spiceinit").write_text("set num_threads=1\nset ngbehavior=hsa\n")
LIB = {"tt": "typical", "ss": "ss", "ff": "ff", "sf": "sf", "fs": "fs"}
CAP = {"tt": "typical", "ss": "ss", "ff": "ff", "sf": "typical", "fs": "typical"}
PVT = [(c, t) for c in LIB for t in (0, 27, 85)]
NB = ["Vlk", "VK", "VNA", "VKup", "VKdn", "VIp", "Vamp_bias"]
SPEC = {"period": (190e-6, 210e-6), "t_spike": (9e-6, 11e-6), "t_refr": (12e-6, 15e-6), "v_spike_max": (2.97, 9)}
ANALYSIS = """.control
save v(spike) v(vmem) i(V1)
tran 40n 6m 0 40n uic
meas tran t3 when v(spike)=1.65 rise=3
meas tran t4 when v(spike)=1.65 rise=4
meas tran t7 when v(spike)=1.65 rise=7
meas tran tf3 when v(spike)=1.65 fall=3
let period = (t7 - t3)/4
print period
let t_spike = tf3 - t3
print t_spike
meas tran v_spike_max max v(spike) from=$&t3 to=$&t4
meas tran v_reset min v(vmem) from=$&t3 to=$&t4
let vrel = v_reset + 0.01
meas tran trel when v(vmem)=$&vrel rise=1 td=$&tf3
meas tran trst when v(vmem)=0.33 fall=1 td=$&t3
let t_refr = trel - trst
print t_refr
.endc
"""


def netlist(sch):
    out = RUN / ("net_" + Path(sch).stem)
    out.mkdir(exist_ok=True)
    subprocess.run(["xschem", "-n", "-s", "-q", "-x", "-o", str(out), str(sch)], cwd=REPO,
                   capture_output=True, text=True, timeout=120)
    f = out / (Path(sch).stem + ".spice")
    assert f.exists(), sch
    return f.read_text()


def joined(text):
    lines = []
    for ln in text.splitlines():
        if ln.startswith("+") and lines:
            lines[-1] += " " + ln[1:]
        else:
            lines.append(ln)
    return lines


def spice(f, text):
    p = RUN / f
    p.write_text(text)
    return subprocess.run(["ngspice", "-b", p.name], cwd=RUN, capture_output=True, text=True, timeout=1200).stdout


def cell_subckt():
    """bias_cell as netlisted from analog/neuron/bias_cell.sch."""
    t = netlist(REPO / "analog/neuron/bias_cell.sch").replace("**.subckt", ".subckt").replace("**.ends", ".ends")
    return "\n".join(ln for ln in joined(t) if ln.startswith((".subckt", "XM", ".ends"))) + "\n"


def corner_lib(text, c, t):
    text = text.replace("sm141064.ngspice typical", "sm141064.ngspice " + LIB[c])
    text = text.replace("mimcap_typical", "mimcap_" + CAP[c])
    return text + "\n.temp %d\n" % t


def num(out, names):
    return {k: float(v) for k, v in re.findall(r"^(?:\w+\.)?(%s)\s*=\s*([-+0-9.eE]+)" % "|".join(names), out, re.M)}


# ------------------------------------------------------------------ suites
def suite_biases(sub):
    def run(ct):
        c, t = ct
        txt = "\n".join(["* biases", bd.LIBH.format(c=LIB[c]), ".temp %d" % t, "VSUP VDD 0 3.3",
                         "Iref VDD Iref_n %g" % bd.IREF, sub,
                         "X1 VDD 0 Iref_n " + " ".join(bd.B) + " bias_cell", ".control", "op",
                         "print " + " ".join("v(%s)" % b for b in bd.B), "print i(vsup)", ".endc", ".end"])
        out = spice("b_%s_%d.spice" % ct, txt)
        v = {k.lower(): float(x) for k, x in re.findall(r"^v\((\w+)\) = ([-+0-9.eE]+)", out, re.M)}
        i = re.search(r"^i\(vsup\) = ([-+0-9.eE]+)", out, re.M)
        return ct, v, abs(float(i.group(1))) if i else None
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(run, PVT))


def suite_neuron(sub):
    tb = netlist(REPO / "analog/neuron/neuron_sized_testbench.sch")
    lines = [ln for ln in joined(tb) if not (ln.lower().startswith(".save") or ln.strip().lower() == ".end")]
    base, ctl = [], False
    for ln in lines:
        if ln.lower().startswith(".control"):
            ctl = True
        if not ctl:
            base.append(ln)
        if ln.lower().startswith(".endc"):
            ctl = False
    base = "\n".join(base).replace("iin=5n", "iin=9.5n")
    # biases from the sizing run (neuron_sized_testbench.sch already holds them)

    def run(k):
        c, t, mode = k
        txt = base
        if mode == "cell":
            for b in NB:
                txt = re.sub(r"^%s %s VSS \{%s\}\s*$" % (b, b, b), "", txt, flags=re.M | re.I)
            outs = " ".join(b if b in NB else "nc_" + b for b in bd.B)
            txt += "\nIref_b VDD Iref_n %g\nXbias VDD VSS Iref_n %s bias_cell\n%s" % (bd.IREF, outs, sub)
        txt = corner_lib(txt, c, t) + ANALYSIS + ".end\n"
        return k, num(spice("n_%s_%d_%s.spice" % k, txt), ["period", "t_spike", "t_refr", "v_spike_max"])
    with ThreadPoolExecutor(8) as ex:
        return dict(ex.map(run, [(c, t, m) for m in ("voltage", "cell") for c, t in PVT]))


def suite_dpi(sub):
    t = netlist(REPO / "analog/neuron/DPI.sch").replace("**.subckt", ".subckt").replace("**.ends", ".ends")
    dpi = "\n".join(ln for ln in joined(t) if ln.startswith((".subckt", "XM", "C", ".ends")) and not ln.startswith("C {"))

    def run(k):
        c, tt, mode = k
        L = ["* dpi", bd.LIBH.format(c=LIB[c]), ".lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice mimcap_" + CAP[c],
             ".temp %d" % tt, dpi, "VSUP VDD 0 3.3", "Vmem VMEM 0 1.0", "Iw Isum 0 15n", "X1 VDD Vthr VMEM Isum VT DPI"]
        if mode == "voltage":
            L += ["Vthr Vthr 0 2.909", "Vtau VDD VT 0.40"]
        else:
            outs = " ".join({"Vthr": "Vthr", "VT_dpi": "VT"}.get(b, "nc_" + b) for b in bd.B)
            L += ["Iref VDD Iref_n %g" % bd.IREF, sub, "Xb VDD 0 Iref_n %s bias_cell" % outs]
        L += [".control", "op", "let g = -i(Vmem)/15n", "print g", ".endc", ".end"]
        return k, num(spice("d_%s_%d_%s.spice" % k, "\n".join(L) + "\n"), ["g"]).get("g")
    with ThreadPoolExecutor(8) as ex:
        return dict(ex.map(run, [(c, tt, m) for m in ("voltage", "cell") for c, tt in PVT]))


def suite_mc(sub):
    # write the m parallel copies out (the PDK mismatch model ignores m)
    exp = []
    for ln in sub.splitlines():
        m = re.search(r"\bm=(\d+)", ln)
        if ln.startswith("XM") and m and int(m.group(1)) > 1:
            n = int(m.group(1))
            name = ln.split()[0]
            for j in range(n):
                exp.append(ln.replace(name, "%s_%d" % (name, j), 1).replace("m=%d" % n, "m=1"))
        else:
            exp.append(ln)
    sube = "\n".join(exp) + "\n"

    def run(seed):
        txt = "\n".join(["* mc", bd.LIBH.format(c="typical"), ".param sw_stat_mismatch=1", ".options seed=%d" % seed,
                         "VSUP VDD 0 3.3", "Iref VDD Iref_n %g" % bd.IREF, sube,
                         "X1 VDD 0 Iref_n " + " ".join(bd.B) + " bias_cell", ".control", "op",
                         "print " + " ".join("v(%s)" % b for b in bd.B), ".endc", ".end"])
        out = spice("mc_%d.spice" % seed, txt)
        return {k.lower(): float(x) for k, x in re.findall(r"^v\((\w+)\) = ([-+0-9.eE]+)", out, re.M)}
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(run, range(1, 101)))


# ------------------------------------------------------------------ report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="biases,neuron,dpi,mc")
    a = ap.parse_args()
    only = a.only.split(",")
    sub = cell_subckt()
    md = ["# bias_cell: current-mode bias generator", "",
          "Generated by `run_bias_cell.py`. Cell `analog/neuron/bias_cell.sch`, Iref = %.0f nA, VDD = 3.3 V. "
          "Sizing: `bias_design.py` (`bias_cell_sizes.json`)." % (bd.IREF * 1e9), ""]
    if "biases" in only:
        R = suite_biases(sub)
        md += ["## Bias voltages across corners and temperature", "",
               "| corner | T (C) | " + " | ".join(bd.B) + " | supply (nA) |", "|---" * (len(bd.B) + 3) + "|"]
        for (c, t), v, i in R:
            md.append("| %s | %d | " % (c, t) + " | ".join("%.3f" % v[b.lower()] for b in bd.B) + " | %.0f |" % (i * 1e9))
        md.append("")
    if "neuron" in only:
        R = suite_neuron(sub)
        md += ["## neuron_sized, 9.5 nA DC: biases as fixed voltages vs from the cell", "",
               "| corner | T (C) | period fixed / cell (us) | t_spike fixed / cell (us) | t_refr fixed / cell (us) | v_spike_max fixed / cell (V) | all specs fixed / cell |",
               "|---|---|---|---|---|---|---|"]
        npass = {"voltage": 0, "cell": 0}

        def fmt(m, k, s=1e6):
            return "-" if k not in m else ("%.4g" % (m[k] * s))
        for c, t in PVT:
            row = []
            ok = {}
            for mode in ("voltage", "cell"):
                m = R[(c, t, mode)]
                ok[mode] = "period" in m and all(k in m and lo <= m[k] <= hi for k, (lo, hi) in SPEC.items())
                npass[mode] += ok[mode]
            vm, cm = R[(c, t, "voltage")], R[(c, t, "cell")]
            md.append("| %s | %d | %s / %s | %s / %s | %s / %s | %s / %s | %s / %s |" % (
                c, t, fmt(vm, "period"), fmt(cm, "period"), fmt(vm, "t_spike"), fmt(cm, "t_spike"),
                fmt(vm, "t_refr"), fmt(cm, "t_refr"), fmt(vm, "v_spike_max", 1), fmt(cm, "v_spike_max", 1),
                "PASS" if ok["voltage"] else "fail", "PASS" if ok["cell"] else "fail"))
        md += ["", "Pass (specs of `neuron/sizing_context.txt`): fixed voltages %d/15, bias cell %d/15. "
               "'-' = fewer than 7 spikes in 6 ms (does not fire)." % (npass["voltage"], npass["cell"]), ""]
    if "dpi" in only:
        R = suite_dpi(sub)
        md += ["## DPI (minimum size) DC gain Isyn/Iw at Iw = 15 nA, VMEM = 1 V", "",
               "| corner | T (C) | Vthr 2.909 V, VT = VDD - 0.40 V | from the cell |", "|---|---|---|---|"]
        for c, t in PVT:
            md.append("| %s | %d | %.3g | %.3g |" % (c, t, abs(R[(c, t, "voltage")]), abs(R[(c, t, "cell")])))
        for mode in ("voltage", "cell"):
            g = [abs(R[(c, t, mode)]) for c, t in PVT]
            md.append("\n%s: gain %.3g to %.3g (%.1fx)" % ("Fixed voltages" if mode == "voltage" else "Bias cell", min(g), max(g), max(g) / min(g)))
        md.append("")
    if "mc" in only:
        R = suite_mc(sub)
        md += ["## Mismatch, 100 samples, tt 27 C", "", "| bias | sigma (mV) |", "|---|---|"]
        for b in bd.B:
            xs = [r[b.lower()] for r in R if b.lower() in r]
            md.append("| %s | %.2f |" % (b, st.pstdev(xs) * 1e3))
        md.append("")
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "bias_cell.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
