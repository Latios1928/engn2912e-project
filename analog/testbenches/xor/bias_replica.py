"""XOR on the 2-2-1 network with current-referenced biases: every fixed bias voltage of xor_tb replaced
by a diode-connected replica of the device it drives, fed by a current that scales with Iref.

    python3 analog/testbenches/xor/bias_replica.py                        # 7 corners/temperatures
    python3 analog/testbenches/xor/bias_replica.py --iref-scale 0.85,1.15  # master reference off by -/+15 %
    python3 analog/testbenches/xor/bias_replica.py --mc 30                 # mismatch at tt, replicas included
    python3 analog/testbenches/xor/bias_replica.py --mc 30 --replica-n 1   # single-device replicas

Ported from the 3-5-1 study (results/bias_replica*.md on branch xor-inhibition). A subthreshold bias
cannot be a precise voltage: a fixed VT_hid moves the current it sets by x0.05 to x14 over corners, so
each bias is instead the gate-source voltage of a copy of the transistor it drives (same type, W, L
and rail), carrying a current calibrated once at tt, 27 C and written as a ratio of Iref (the DAC
reference, 14.42 nA). All currents follow --iref-scale together, as they would follow one on-chip
master reference. The comparator threshold VT (about VDD/2) stays a voltage (a divider on chip).

Each replica is --replica-n unit copies in parallel (default 16), carrying n times the current: the
voltage is the same and the replica's own mismatch falls as 1/sqrt(n). One replica serves a whole
layer, so its mismatch would otherwise move every neuron of the layer at once. The strong-inversion
neuron biases (VK, VNA, VKup; 0.5-17 uA) use --strong-n copies (default 1) to save power.

Writes results/bias_replica[_tag].md/.csv.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import tbtools as tb  # noqa: E402
import run_xor as rx  # noqa: E402

IREF = 14.42e-9
VDD = 3.3
# bias net -> replica device (type, W um, L um): the transistor that the net drives
# (DPI entries: W and L of DPI_sized, filled in from the netlist by dpi_size())
DPI_NETS = ("VT_dpi", "VT_inh", "VT_in", "VT_hid",     # DPI tau: M3 of DPI_sized
            "Vthr", "Vthr_in", "Vthr_hid")             # DPI gain, set against the gate of the output pFET M4
REPLICA = {
    "Vlk": ("n", 1.0, 1.0), "VK": ("n", 1.0, 1.0), "VIp": ("n", 1.0, 1.0), "VKdn": ("n", 1.0, 1.0),
    "VNA": ("p", 1.0, 1.0), "VKup": ("p", 1.0, 1.0),               # neuron current sources
    "Vamp_bias": ("n", 0.22, 0.28),                                # comparator tail
}
# Single-copy replicas: the strong-inversion neuron biases (0.5-17 uA; 16 copies would cost ~1 mW)
STRONG = {"VK", "VNA", "VKup"}


def dpi_size(text):
    """W, L (um) of the tau pFET M3 of DPI_sized in the netlist, so the replicas follow the cell's size."""
    sub = re.search(r"^\.subckt DPI_sized .*?^\.ends", text, re.M | re.S).group(0)
    m = re.search(r"^XM3 .* pfet_03v3 L=([0-9.]+)u W=([0-9.]+)u", sub, re.M)
    return float(m.group(2)), float(m.group(1))


def copies(net, a):
    return a.strong_n if net in STRONG else a.replica_n


def dev(net, n):
    typ, w, l = REPLICA[net]
    rail, model = ("VDD", "pfet_03v3") if typ == "p" else ("VSS", "nfet_03v3")
    return "\n".join(f"XB{net}_{k} {net} {net} {rail} {rail} {model} L={l}u W={w}u nf=1" for k in range(n))


def bias_sources(text):
    """{net: (source line, param, referenced to VDD?)} for the bias sources of REPLICA."""
    out = {}
    for m in re.finditer(r"^(V\w+) (\S+) (\S+) \{(p_\w+)\}$", text, re.M):
        line, x, y, p = m.group(0), m.group(2), m.group(3), m.group(4)
        if x == "VDD" and y in REPLICA:
            out[y] = (line, p, True)
        elif x in REPLICA and y in ("0", "VSS"):
            out[x] = (line, p, False)
    return out


def params_of(text):
    vals = {}
    for line in re.findall(r"^\.param (.*)$", text, re.M):
        for k, v in re.findall(r"(\w+)=([-0-9.eE]+)", line):
            vals[k] = float(v)
    return vals


def calibrate(nominal, a):
    """Current per unit copy at the nominal voltage (tt, 27 C), from a one-device operating point."""
    d = rx.RUNS / "_bias_cal"
    d.mkdir(parents=True, exist_ok=True)
    (d / ".spiceinit").write_text("set ngbehavior=hsa\nset num_threads=1\n")
    lines = ["* replica calibration", ".include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice",
             ".lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical", f"Vdd VDD 0 {VDD}", "Vss VSS 0 0"]
    for net, v in nominal.items():
        lines += [f"Vf{net} {net} 0 {v}", dev(net, 1)]
    lines += [".control", "op"] + [f"print i(Vf{net})" for net in nominal] + ["quit", ".endc", ".end"]
    (d / "cal.spice").write_text("\n".join(lines) + "\n")
    log = subprocess.run(["ngspice", "-b", "cal.spice"], cwd=d, env=tb._env(), capture_output=True, text=True).stdout
    return {net: abs(float(re.search(rf"i\(vf{net.lower()}\) = (\S+)", log).group(1))) for net in nominal}


def build(text, overrides, a):
    w, l = dpi_size(text)
    REPLICA.update({n: ("p", w, l) for n in DPI_NETS})
    src = bias_sources(text)
    assert set(REPLICA) <= set(src), f"bias sources not found: {set(REPLICA) - set(src)}"
    pv = params_of(text)
    pv.update({k: float(v) for k, v in overrides.items() if k in pv})
    nominal = {net: (VDD - pv[p] if to_vdd else pv[p]) for net, (line, p, to_vdd) in src.items()
               if net not in a.keep}
    unit = calibrate(nominal, a)
    cur = {net: unit[net] * copies(net, a) for net in nominal}
    for net in nominal:
        line = src[net][0]
        isrc = (f"IB{net} {net} 0 {{p_ib_{net.lower()}}}" if REPLICA[net][0] == "p"
                else f"IB{net} VDD {net} {{p_ib_{net.lower()}}}")
        text = text.replace(line, f"* {net}: replica, {copies(net, a)} unit copies, {unit[net] / IREF:.4g} x Iref each\n"
                                  f"{isrc}\n{dev(net, copies(net, a))}")
    anchor = re.search(r"^\.param p_vlk=.*$", text, re.M).group(0)
    text = text.replace(anchor, anchor + "\n.param " + " ".join(f"p_ib_{n.lower()}={c:.6g}" for n, c in cur.items()))
    meas = "  meas tran vmax_out max v(x1.VMEM_4)"
    assert meas in text and "  save v(sp0)" in text
    text = text.replace("  save v(sp0)", "  save " + " ".join(f"v({n})" for n in nominal) + " v(sp0)", 1)
    text = text.replace(meas, meas + "".join(f"\n  meas tran b_{n.lower()} avg v({n})\n  echo RES b_{n.lower()}=$&b_{n.lower()}"
                                             for n in nominal))
    return text, nominal, unit, cur


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--iref-scale", default="1", help="comma-separated master current scales")
    ap.add_argument("--corners", default="all", help="'all', 'tt', or a comma list of corners at 27 C")
    ap.add_argument("--keep", default="", help="comma list of bias nets left as fixed voltages")
    ap.add_argument("--mc", type=int, default=0, help="mismatch samples at tt (4 cases each)")
    ap.add_argument("--seed0", type=int, default=7700)
    ap.add_argument("--replica-n", type=int, default=16, help="unit copies per subthreshold replica")
    ap.add_argument("--strong-n", type=int, default=1, help="unit copies per strong-inversion replica")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--pulses", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    a.keep = [k for k in a.keep.split(",") if k]
    extra = dict(s.split("=", 1) for s in a.set)
    base = tb.netlist(HERE / "xor_tb.sch", (rx.RUNS / "_netlists").resolve()).read_text()
    text, nominal, unit, cur = build(base, extra, a)
    print("DPI replicas: pFET W/L = %g/%g um" % REPLICA["VT_hid"][1:])
    tag = "br" + (f"_{a.tag}" if a.tag else "")
    cases, cols = [], {}
    for sc in [float(x) for x in a.iref_scale.split(",")]:
        p0 = {f"p_ib_{n.lower()}": c * sc for n, c in cur.items()}
        p0["iref"] = IREF * sc
        p0.update(extra)
        groups = ([("tt", 27, s) for s in range(a.mc)] if a.mc else
                  [(c, t, None) for c, t in (rx.CORNERS if a.corners == "all" else rx.CORNERS[:1] if a.corners == "tt"
                                             else [(c, 27) for c in a.corners.split(",")])])
        for corner, temp, s in groups:
            k = f"{tag}_{sc:g}_{corner}_{temp}" + ("" if s is None else f"_s{s}")
            cols[k] = {"iref_scale": sc, "corner": corner, "temp": temp, "sample": s}
            cases += rx.cases_for(k, p0, corner, temp, seed=None if s is None else a.seed0 + s, pulses=a.pulses)
    tb.run_cases(cases, {"xor_tb": text}, rx.RUNS, a.jobs)
    rows = rx.summarize(cases, cols)
    # generated bias voltages, from the (1,1) case of each key
    for row, key in zip(rows, cols):
        c = next(c for c in cases if c.tags["key"] == key and c.tags["ab"] == (1, 1))
        for n in ("VT_in", "Vthr_in", "VT_hid", "VT_dpi", "Vthr", "Vlk"):
            v = c.results.get(f"b_{n.lower()}")
            row[f"V_{n}"] = None if v is None else round(VDD - v if n.startswith("VT") else v, 4)
    note = (f"Every bias except VT is a diode replica fed by a current calibrated at tt "
            f"({a.replica_n} unit copies per subthreshold replica, {a.strong_n} for {', '.join(sorted(STRONG))}). "
            f"Fixed voltages kept: {a.keep or 'none'}. "
            f"Overrides {extra or 'none'}. `V_VT_*` = VDD - VT_* (source-gate voltage of the tau pFET) as generated.\n\n"
            "| bias | nominal V | per unit copy | x Iref |\n|---|---|---|---|\n" +
            "\n".join(f"| {n} | {nominal[n]:.4f} | {unit[n] * 1e9:.4g} nA | {unit[n] / IREF:.4g} |" for n in nominal))
    rx.write(rows, "bias_replica" + (f"_{a.tag}" if a.tag else ""), "XOR with current-referenced biases (bias_replica.py)", note)


if __name__ == "__main__":
    main()
