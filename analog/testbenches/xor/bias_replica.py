"""XOR with current-referenced biases: every fixed bias voltage replaced by a diode replica.

    python3 analog/testbenches/xor/bias_replica.py                       # 7 corners, master current x1
    python3 analog/testbenches/xor/bias_replica.py --iref-scale 0.7,1.3   # master current off by -30/+30 %
    python3 analog/testbenches/xor/bias_replica.py --mc 30                # mismatch at tt (replicas included)
    python3 analog/testbenches/xor/bias_replica.py --keep VK,VNA          # leave some biases as fixed voltages

On a chip a subthreshold bias cannot be a precise voltage (VT_hid = 0.6225 V moves the current it sets by
x0.05 to x14 over corners). Each bias here is made instead by a diode-connected copy of the transistor it
drives (same type, W and L, source on the same rail), fed by a fixed current. The currents are calibrated
once at tt, 27 C so that the replicas reproduce the nominal voltages, and are expressed as ratios of the DAC
reference current Iref (14.42 nA). All of them scale together with --iref-scale, the way they would follow
one on-chip master reference. The comparator threshold VT (1.66 V, about VDD/2) is a real voltage and stays
fixed (on a chip: a divider from VDD).

Writes results/bias_replica[_tag].csv/.md.
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import tbtools as tb  # noqa: E402
import run_xor as rx  # noqa: E402

LIBS = (".include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice\n"
        ".lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical\n")
IREF = 14.42e-9
VDD = 3.3
# bias net -> replica device (type, W um, L um): the transistor that the net drives
REPLICA = {
    "VT_dpi": ("p", 0.88, 1.12), "VT_inh": ("p", 0.88, 1.12),      # DPI tau, M3 of DPI_sized
    "VT_in": ("p", 0.88, 1.12), "VT_hid": ("p", 0.88, 1.12),
    "Vthr": ("p", 0.88, 1.12), "Vthr_in": ("p", 0.88, 1.12),       # DPI gain: compared with the gate of
    "Vthr_hid": ("p", 0.88, 1.12),                                 # the output pFET M4 by the nFET pair
    "Vlk": ("n", 1.0, 1.0), "VK": ("n", 1.0, 1.0), "VIp": ("n", 1.0, 1.0), "VKdn": ("n", 1.0, 1.0),
    "VNA": ("p", 1.0, 1.0), "VKup": ("p", 1.0, 1.0),               # neuron current sources
    "Vamp_bias": ("n", 0.22, 0.28),                                # comparator tail
}


def dev(net, typ, w, l):
    if typ == "p":
        return f"XB{net} {net} {net} VDD VDD pfet_03v3 L={l}u W={w}u nf=1"
    return f"XB{net} {net} {net} VSS VSS nfet_03v3 L={l}u W={w}u nf=1"


def bias_sources(text):
    """{net: (source line, param, referenced to VDD?)} for every bias source in REPLICA."""
    out = {}
    for m in re.finditer(r"^(V\w+) (\S+) (\S+) \{(p_\w+)\}$", text, re.M):
        line, a, b, p = m.group(0), m.group(2), m.group(3), m.group(4)
        if a == "VDD" and b in REPLICA:
            out[b] = (line, p, True)
        elif a in REPLICA and b in ("0", "VSS"):
            out[a] = (line, p, False)
    return out


def params_of(text):
    vals = {}
    for line in re.findall(r"^\.param (.*)$", text, re.M):
        for k, v in re.findall(r"(\w+)=(\S+)", line):
            try:
                vals[k] = float(v.rstrip("n")) * (1e-9 if v.endswith("n") else 1)
            except ValueError:
                pass
    return vals


def calibrate(nominal, workdir):
    """Current that each diode replica carries at its nominal voltage (tt, 27 C)."""
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / ".spiceinit").write_text("set ngbehavior=hsa\nset num_threads=1\n")
    lines = ["* replica calibration", LIBS, f"Vdd VDD 0 {VDD}", "Vss VSS 0 0"]
    for net, v in nominal.items():
        lines += [f"Vf{net} {net} 0 {v}", dev(net, *REPLICA[net])]
    lines += [".control", "op"] + [f"print i(Vf{net})" for net in nominal] + ["quit", ".endc", ".end"]
    (workdir / "cal.spice").write_text("\n".join(lines) + "\n")
    log = subprocess.run(["ngspice", "-b", "cal.spice"], cwd=workdir, env=tb._env(), capture_output=True, text=True).stdout
    cur = {}
    for net in nominal:
        m = re.search(rf"i\(vf{net.lower()}\) = (\S+)", log)
        cur[net] = abs(float(m.group(1)))   # pFET: current out of VDD into the node; nFET: into the diode
    return cur


def build(text, keep):
    src = bias_sources(text)
    missing = set(REPLICA) - set(src)
    assert not missing, f"bias sources not found: {missing}"
    pv = params_of(text)
    pv.update({k: float(v) for k, v in rx.XOR_BIAS.items()})
    nominal = {net: (VDD - pv[p] if to_vdd else pv[p]) for net, (line, p, to_vdd) in src.items() if net not in keep}
    cur = calibrate(nominal, rx.RUNS / "_bias_cal")
    for net in nominal:
        line = src[net][0]
        typ = REPLICA[net][0]
        isrc = f"IB{net} {net} 0 {{p_ib_{net.lower()}}}" if typ == "p" else f"IB{net} VDD {net} {{p_ib_{net.lower()}}}"
        text = text.replace(line, f"* {net}: diode replica fed by {cur[net] / IREF:.4g} x Iref\n{isrc}\n{dev(net, *REPLICA[net])}")
    anchor = re.search(r"^\.param p_vlk=.*$", text, re.M).group(0)
    text = text.replace(anchor, anchor + "\n.param " + " ".join(f"p_ib_{n.lower()}={c:.6g}" for n, c in cur.items()))
    # log the generated bias voltages
    save = "  save v(sp0)"
    assert text.count(save) == 1
    text = text.replace(save, "  save " + " ".join(f"v({n})" for n in nominal) + " v(sp0)")
    meas = "  meas tran vmax_out max v(x1.VMEM_8)"
    text = text.replace(meas, meas + "".join(f"\n  meas tran b_{n.lower()} avg v({n})\n  echo RES b_{n.lower()}=$&b_{n.lower()}"
                                             for n in nominal))
    return text, nominal, cur


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--iref-scale", default="1", help="comma-separated master current scales (default 1)")
    ap.add_argument("--keep", default="", help="comma-separated bias nets to leave as fixed voltages")
    ap.add_argument("--corners", default="all", help="'all' or 'tt' (tt, 27 C only)")
    ap.add_argument("--mc", type=int, default=0, help="mismatch samples at tt (all 4 cases per sample)")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    keep = [k for k in a.keep.split(",") if k]
    base = tb.netlist(HERE / "xor_tb.sch", (rx.RUNS / "_netlists").resolve()).read_text()
    text, nominal, cur = build(base, keep)
    print("replica currents (tt, 27 C):")
    for n, c in cur.items():
        print(f"  {n:10} {nominal[n]:.4f} V  {c * 1e9:10.4g} nA  = {c / IREF:8.4g} x Iref")
    extra = dict(s.split("=", 1) for s in a.set)
    corners = rx.CORNERS if a.corners == "all" else rx.CORNERS[:1]
    scales = [float(x) for x in a.iref_scale.split(",")]
    cases = []
    tag = "br" + (f"_{a.tag}" if a.tag else "")
    for sc in scales:
        p0 = {f"p_ib_{n.lower()}": c * sc for n, c in cur.items()}
        p0["iref"] = IREF * sc
        p0.update(extra)
        groups = [(c, t, None) for c, t in corners] if not a.mc else [("tt", 27, s) for s in range(a.mc)]
        for corner, temp, seed in groups:
            for ina, inb in rx.CASES:
                name = f"{tag}_{sc:g}_{corner}_{temp}_{'' if seed is None else f's{seed}_'}{ina}{inb}"
                cases.append(tb.Case(name, "xor_tb", corner, temp, rx.xor_params(ina, inb, p0),
                                     seed=None if seed is None else 7700 + seed,
                                     tags={"k": (sc, corner, temp, seed), "ab": (ina, inb)}))
    tb.run_cases(cases, {"xor_tb": text}, rx.RUNS, a.jobs)
    rows = []
    for key in dict.fromkeys(c.tags["k"] for c in cases):
        m, b = {}, {}
        for c in cases:
            if c.tags["k"] != key:
                continue
            m[c.tags["ab"]] = rx.xor_metrics(c) if c.ok and "singular matrix" not in c.log else None
            if c.tags["ab"] == (1, 1):
                b = c.results
        sc, corner, temp, seed = key
        row = {"iref_scale": sc, "corner": corner, "temp": temp, "sample": seed}
        if any(v is None for v in m.values()):
            row["pass"] = "sim failed"
            rows.append(row)
            continue
        for ab in rx.CASES:
            row[f"out_{ab[0]}{ab[1]}"] = m[ab]["n8"]
        row.update({"OR_10": m[(1, 0)]["n3"], "AND_10": m[(1, 0)]["n4"], "AND_01": m[(0, 1)]["n4"],
                    "AND_11": m[(1, 1)]["n4"], "relays_11": f"{m[(1, 1)]['n0']}/{m[(1, 1)]['n1']}",
                    "spurious": sum(x["n_spurious"] for x in m.values())})
        for n in ("VT_hid", "VT_in", "Vthr", "Vlk", "VK"):
            v = b.get(f"b_{n.lower()}")
            if v is not None:
                row[f"V_{n}"] = round(VDD - v if n.startswith("VT") else v, 4)
        row["pass"] = (m[(0, 0)]["n8"] == 0 and m[(0, 1)]["n8"] > 0 and m[(1, 0)]["n8"] > 0 and m[(1, 1)]["n8"] == 0)
        rows.append(row)
    keys = list(max(rows, key=len))
    fmt = lambda v: "–" if v is None else (f"{v:.4g}" if isinstance(v, float) else str(v))
    print(" | ".join(keys))
    for r in rows:
        print(" | ".join(fmt(r.get(k)) for k in keys))
    npass = sum(1 for r in rows if r["pass"] is True)
    print(f"{npass}/{len(rows)} pass")
    tb_name = "bias_replica" + (f"_{a.tag}" if a.tag else "")
    rx.RESULTS.mkdir(exist_ok=True)
    with open(rx.RESULTS / f"{tb_name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(rows)
    md = [f"## XOR with current-referenced biases (`bias_replica.py`)", "",
          f"Every bias except the comparator threshold VT is a diode replica of the device it drives, fed by a "
          f"current calibrated at tt (ratios of Iref below). Fixed voltages kept: {keep or 'none'}. Overrides: {extra or 'none'}. "
          f"`out_AB`: output spikes in 20 pulses; `V_VT_*` = VDD - VT (source-gate voltage of M3), generated by the replica. "
          f"**{npass} / {len(rows)} pass.**", "",
          "| bias | nominal V | current | x Iref |", "|---|---|---|---|"]
    md += [f"| {n} | {nominal[n]:.4f} | {c * 1e9:.4g} nA | {c / IREF:.4g} |" for n, c in cur.items()]
    md += ["", "| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    md += ["| " + " | ".join(fmt(r.get(k)) for k in keys) + " |" for r in rows]
    (rx.RESULTS / f"{tb_name}.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
