#!/usr/bin/env python3
"""Power estimate of snn_top from a gate-level mixed-signal run (librelane/snn_top/gls_ms), and
one VCD with the digital and the analog signals together.

    python3 tools/snn_power.py librelane/snn_top/gls_ms/gls_ms_pex.raw \\
        librelane/snn_top/gls_ms/gls_ms_pex_digital.vcd -o slides/power_pex

Analog (the SNN_signed macro, VDDA): from SPICE. The run saves the supply current i(Vdd)
(gls_ms/Makefile adds the .save), so P = VDD * average(-i(Vdd)), per scenario window.
This includes the 100 nA Iref current source, which in the testbench draws from VDD; on the
chip Iref comes from a pin (the bench), so it is listed separately.

Digital (standard cells, VDDD): OpenSTA report_power on the routed layout (LibreLane
final/odb, nominal SPEF, typical 3.3 V library) with the switching activity of the
gate-level simulation (read_vcd). The analog macro has no power model, so it is not in
this number. The VCD covers the whole run, so this is the average over all scenarios.

Writes <out>_power.txt (the summary below) and <out>_merged.vcd: the digital VCD plus a
scope "analog" with the membranes, the supply current and the analog power as real
signals (each written when it changes by more than a small deadband).
Needs numpy (container); runs openroad for the digital part.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snn_waves import NEURONS, SCENARIOS, read_raw, windows, pair_vmem  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIB = "/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/lib/gf180mcu_fd_sc_mcu7t5v0__tt_025C_3v30.lib"


def avg(t, y, t0, t1):
    """Time average of y over [t0, t1] (trapezoids, non-uniform steps)."""
    i0, i1 = np.searchsorted(t, t0), np.searchsorted(t, t1)
    if i1 - i0 < 2:
        return float("nan")
    return float(np.trapezoid(y[i0:i1], t[i0:i1]) / (t[i1 - 1] - t[i0]))


def digital_power(vcd, run_dir, scope):
    tcl = f"""
read_db {run_dir}/final/odb/snn_top.odb
read_liberty {LIB}
read_sdc {run_dir}/final/sdc/snn_top.sdc
read_spef {run_dir}/final/spef/nom/snn_top.nom.spef
read_vcd -scope {scope} {vcd}
report_activity_annotation
report_power -digits 4
exit
"""
    with tempfile.NamedTemporaryFile("w", suffix=".tcl", delete=False) as f:
        f.write(tcl)
    out = subprocess.run(["openroad", "-no_init", "-exit", f.name], capture_output=True, text=True).stdout
    os.unlink(f.name)
    m = re.search(r"^Total\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", out, re.M)
    if not m:
        sys.exit("snn_power.py: no 'Total' line from report_power:\n" + out[-2000:])
    internal, switching, leakage, total = (float(x) for x in m.groups())
    va, un = re.search(r"^vcd\s+(\d+)", out, re.M), re.search(r"^unannotated\s+(\d+)", out, re.M)
    return dict(internal=internal, switching=switching, leakage=leakage, total=total,
                report=out[out.find("Group"):] if "Group" in out else out[-1500:],
                annotated=f"activity from the VCD on {va.group(1)} pins, {un.group(1) if un else 0} without"
                if va else None)


def merge_vcd(dig_path, out_path, t, analog, unit_s):
    """Digital VCD + analog real signals (scope 'analog') -> one VCD."""
    text = open(dig_path).read()
    head, body = text.split("$enddefinitions", 1)
    body = body.split("$end", 1)[1]
    ids = {}
    decl = ["$scope module analog $end"]
    for k, (name, _, _) in enumerate(analog):
        ids[name] = f"~a{k}"
        decl.append(f"$var real 64 {ids[name]} {name} $end")
    decl.append("$upscope $end")
    # analog events: (time in VCD units, line), only when the value moved past the deadband
    ev = []
    for name, y, dead in analog:
        last = None
        for ti, v in zip(t, y):
            if last is None or abs(v - last) > dead:
                ev.append((int(round(ti / unit_s)), f"r{v:.6g} {ids[name]}"))
                last = v
    ev.sort(key=lambda e: e[0])
    out, j = [head.rstrip(), *decl, "$enddefinitions $end"], 0
    cur = None
    for ln in body.splitlines():
        if ln.startswith("#"):
            tnow = int(ln[1:])
            while j < len(ev) and ev[j][0] < tnow:
                if ev[j][0] != cur:
                    out.append(f"#{ev[j][0]}")
                    cur = ev[j][0]
                out.append(ev[j][1])
                j += 1
            out.append(ln)
            cur = tnow
            while j < len(ev) and ev[j][0] == tnow:
                out.append(ev[j][1])
                j += 1
        elif ln.strip():
            out.append(ln)
    while j < len(ev):
        if ev[j][0] != cur:
            out.append(f"#{ev[j][0]}")
            cur = ev[j][0]
        out.append(ev[j][1])
        j += 1
    open(out_path, "w").write("\n".join(out) + "\n")
    return len(ev)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("vcd", help="digital VCD of the same run (gls_ms*_digital.vcd)")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--run-dir", default=os.path.join(ROOT, "librelane/snn_top/runs/full_2"))
    ap.add_argument("--scope", default="snn_ms_tb/dut")
    ap.add_argument("--vdd", type=float, default=3.3)
    ap.add_argument("--iref", type=float, default=100e-9)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--settle", type=float, default=4000)
    ap.add_argument("--run", type=float, default=3000)
    a = ap.parse_args()

    sig = read_raw(a.raw)
    t = sig["time"]
    if "i(vdd)" not in sig:
        sys.exit("snn_power.py: the .raw has no i(vdd); rerun gls_ms (its Makefile saves it now)")
    p = -a.vdd * sig["i(vdd)"]                         # power delivered by the supply (W)
    n = sum(1 for k in range(a.first, 6) if windows(k - a.first + 1, a.first, a.settle, a.run)[-1][3]
            <= t[-1] + 100e-6)
    win = windows(n, a.first, a.settle, a.run)

    lines = [f"Power estimate: {a.raw}", "", "Analog macro (VDDA = %.2f V, from SPICE i(Vdd)):" % a.vdd]
    lines.append(f"  {'scenario':40s} {'settle (uW)':>12s} {'run (uW)':>10s}")
    for k, t_load, t0, t1 in win:
        name = SCENARIOS.get(k, (f"scenario {k}",))[0]
        lines.append(f"  {k}. {name:37s} {avg(t, p, t_load + 30e-6, t0) * 1e6:12.2f} {avg(t, p, t0, t1) * 1e6:10.2f}")
    p_all = avg(t, p, t[0], t[-1])
    p_iref = a.vdd * a.iref
    lines += [f"  average over the whole run: {p_all * 1e6:.2f} uW, peak {p.max() * 1e6:.1f} uW",
              f"  of which the Iref source: {p_iref * 1e6:.2f} uW (external on the chip: macro alone "
              f"{(p_all - p_iref) * 1e6:.2f} uW)"]
    if "i(vt)" in sig:
        lines.append(f"  VT pin: {avg(t, a.vdd * 0 + sig['i(vt)'], t[0], t[-1]) * 1e9:.3f} nA average (negligible)")

    d = digital_power(os.path.abspath(a.vcd), a.run_dir, a.scope)
    lines += ["", "Digital (VDDD, OpenSTA with the simulation's activity, typical 3.3 V, nominal SPEF):",
              f"  internal {d['internal'] * 1e6:.2f} uW, switching {d['switching'] * 1e6:.2f} uW, "
              f"leakage {d['leakage'] * 1e9:.2f} nW, total {d['total'] * 1e6:.2f} uW",
              f"  (average over the run; {d['annotated'] or 'activity annotation: see report'})",
              "", f"Total (macro + digital): {(p_all + d['total']) * 1e6:.2f} uW "
              f"(without the external Iref: {(p_all - p_iref + d['total']) * 1e6:.2f} uW)"]
    report = "\n".join(lines)
    print(report)
    open(f"{a.out}_power.txt", "w").write(report + "\n\nOpenSTA report_power:\n" + d["report"])

    # merged VCD (timescale of the digital VCD)
    ts = re.search(r"\$timescale\s+(\d+)\s*(\w+)\s+\$end", open(a.vcd).read(4000))
    unit = int(ts.group(1)) * {"s": 1, "ms": 1e-3, "us": 1e-6, "ns": 1e-9, "ps": 1e-12, "fs": 1e-15}[ts.group(2)]
    pairs = pair_vmem(sig, t)
    short = ["in0", "in1", "hid0", "hid1", "out"]
    analog = [(f"vmem_{short[k]}", sig[v], 2e-3) for k, v in sorted(pairs.items())]
    analog += [("i_vdd_A", -sig["i(vdd)"], 1e-9), ("p_analog_W", p, 3e-9)]
    nev = merge_vcd(a.vcd, f"{a.out}_merged.vcd", t, analog, unit)
    print(f"\nwrote {a.out}_power.txt and {a.out}_merged.vcd ({nev} analog value changes added)")


if __name__ == "__main__":
    main()
