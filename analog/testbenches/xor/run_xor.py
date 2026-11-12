"""XOR on the 2-2-1 snn_analog (xor_tb): the 4 input cases at corners, under mismatch, or over a grid.

    python3 analog/testbenches/xor/run_xor.py xor                          # tt, 27 C
    python3 analog/testbenches/xor/run_xor.py xor --corners all            # 5 corners and 0 / 85 C
    python3 analog/testbenches/xor/run_xor.py mc --mc 30                   # mismatch, 4 cases per sample
    python3 analog/testbenches/xor/run_xor.py grid --grid p_vtau=0.60,0.62 --grid c0+c1=5,7

Common options: --set NAME=VALUE (testbench .param, e.g. c7=-5 or p_vlk=0.47), --pulses N (input
pulses per case, default 20), --tag (result file suffix), --jobs. Writes results/<suite>[_tag].md/.csv.

Pass = the output neuron (spike[4]) fires at least once for (0,1) and (1,0) and never for (0,0) and
(1,1). Strict = pass, and also every relay fires exactly once per input pulse and the AND neuron is
silent for one input and fires for two (pass alone can come from an inhibition race). Neurons: n0, n1 inputs (relays), n2 hidden 0 (OR), n3 hidden 1 (AND), n4 output.
"""

import argparse
import bisect
import csv
import datetime
import itertools
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402

RESULTS = HERE / "results"
RUNS = HERE / "runs"
VTH = 1.65
T0, TSP = 100e-6, 200e-6
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
CORNERS = [("tt", 27), ("ss", 27), ("ff", 27), ("sf", 27), ("fs", 27), ("tt", 0), ("tt", 85)]


def edges(t, v, th=VTH):
    return [t[i] for i in range(1, len(v)) if v[i - 1] < th <= v[i]]


def spurious(t, vm, spikes, vmin=1.5, jump=0.3):
    """Spikes preceded (within 3 us) by a one-step membrane jump from below vmin: time-step artefacts."""
    n = 0
    for t1 in spikes:
        i1, i0 = bisect.bisect_left(t, t1), bisect.bisect_left(t, t1 - 3e-6)
        if any(vm[i] < vmin and vm[i + 1] - vm[i] > jump for i in range(max(i0, 0), max(i1 - 1, 0))):
            n += 1
    return n


def metrics(case):
    w = tb.read_wrdata(RUNS / case.name / "xor_tb.txt")
    t = w["time"]
    sp = {k: edges(t, w[f"v(sp{k})"]) for k in range(5)}
    r = {f"n{k}": len(sp[k]) for k in range(5)}
    r["n_spurious"] = sum(spurious(t, w[f"v(x1.vmem_{k})"], sp[k]) for k in range(5))
    r["t_out_us"] = round((sp[4][0] - T0) * 1e6, 1) if sp[4] else None
    r["t_and_us"] = round((sp[3][0] - T0) * 1e6, 1) if sp[3] else None
    r["vmax_out"] = max(w["v(x1.vmem_4)"])
    return r


def scale_dpi(text, k):
    """Netlist with the DPI_sized devices (all DPIs, inhibitory ones included) scaled by k in W and L."""
    m = re.search(r"^\.subckt DPI_sized .*?^\.ends", text, re.M | re.S)
    body = re.sub(r"L=1\.12u W=0\.88u", f"L={1.12 * k:.4g}u W={0.88 * k:.4g}u", m.group(0))
    assert body.count(f"W={0.88 * k:.4g}u") == 4, "DPI_sized devices not found"
    return text.replace(m.group(0), body)


def cases_for(label, params, corner="tt", temp=27, seed=None, pulses=20):
    p = dict(params)
    p["tstop"] = f"{T0 * 1e6 + pulses * TSP * 1e6 + 100:g}u"
    return [tb.Case(f"{label}_{a}{b}", "xor_tb", corner, temp, {**p, "ina": a, "inb": b}, seed=seed,
                    tags={"key": label, "ab": (a, b)}) for a, b in CASES]


def summarize(cases, extra_cols):
    """One row per key (4 cases): spike counts per case and pass."""
    rows = []
    for key in dict.fromkeys(c.tags["key"] for c in cases):
        grp = {c.tags["ab"]: c for c in cases if c.tags["key"] == key}
        row = dict(extra_cols[key])
        bad = [ab for ab, c in grp.items() if not c.ok or "singular matrix" in c.log]
        if bad:
            row["pass"] = f"sim failed {bad}"
            rows.append(row)
            continue
        m = {ab: metrics(c) for ab, c in grp.items()}
        for ab in CASES:
            row[f"out_{ab[0]}{ab[1]}"] = m[ab]["n4"]
        row.update({"in_01": m[(0, 1)]["n1"], "in_11": f"{m[(1, 1)]['n0']}/{m[(1, 1)]['n1']}",
                    "OR_01": m[(0, 1)]["n2"], "OR_11": m[(1, 1)]["n2"],
                    "AND_01": m[(0, 1)]["n3"], "AND_10": m[(1, 0)]["n3"], "AND_11": m[(1, 1)]["n3"],
                    "t_out_01": m[(0, 1)]["t_out_us"], "t_and_11": m[(1, 1)]["t_and_us"],
                    "t_out_11": m[(1, 1)]["t_out_us"],
                    "spurious": sum(x["n_spurious"] for x in m.values())})
        row["pass"] = (m[(0, 0)]["n4"] == 0 and m[(0, 1)]["n4"] > 0 and m[(1, 0)]["n4"] > 0 and m[(1, 1)]["n4"] == 0)
        # strict: also every hidden function right, not just the output (relays one spike per pulse,
        # AND silent for one input and firing for two)
        npulse = int((case_tstop(grp[(1, 1)]) - T0) // TSP) + 1   # pulse starts before tstop
        relays_ok = all(m[ab][f"n{i}"] == npulse * ab[i] for ab in CASES for i in (0, 1))
        and_ok = m[(0, 1)]["n3"] == 0 and m[(1, 0)]["n3"] == 0 and m[(1, 1)]["n3"] > 0
        row["strict"] = row["pass"] and relays_ok and and_ok
        rows.append(row)
    return rows


def case_tstop(case):
    v = str(case.params["tstop"])
    return float(v.rstrip("u")) * 1e-6


def write(rows, name, title, note):
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    fmt = lambda v: "–" if v is None else (f"{v:.4g}" if isinstance(v, float) else str(v))
    npass = sum(1 for r in rows if r.get("pass") is True)
    nstrict = sum(1 for r in rows if r.get("strict") is True)
    RESULTS.mkdir(exist_ok=True)
    with open(RESULTS / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(rows)
    md = [f"<!-- {name}: run_xor.py on {datetime.date.today()} -->", f"## {title}", "", note, "",
          f"**{npass} / {len(rows)} pass** (output is A XOR B); **{nstrict} / {len(rows)} strict** "
          "(also relays one spike per pulse, AND silent for one input).", "", "| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    md += ["| " + " | ".join(fmt(r.get(k)) for k in keys) + " |" for r in rows]
    (RESULTS / f"{name}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[5:]))
    return npass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("suite", choices=["xor", "mc", "grid"])
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--grid", action="append", default=[], metavar="NAME=V1,V2,...")
    ap.add_argument("--corners", default="tt", help="'tt' or 'all'")
    ap.add_argument("--mc", type=int, default=30)
    ap.add_argument("--seed0", type=int, default=7700)
    ap.add_argument("--pulses", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--tag", default="")
    ap.add_argument("--dpi-scale", type=float, default=1,
                    help="scale W and L of the four DPI_sized devices (W/L kept; 1 = 0.88u/1.12u)")
    ap.add_argument("--sch", default=str(HERE / "xor_tb.sch"), help="testbench (e.g. a bias-replica variant)")
    a = ap.parse_args()
    base = dict(s.split("=", 1) for s in a.set)
    text = tb.netlist(Path(a.sch), (RUNS / "_netlists").resolve()).read_text()
    assert "IS MISSING" not in text, "xschem: missing symbol in xor_tb"
    tb.check_connected(text, "snn_analog")
    if a.dpi_scale != 1:
        text = scale_dpi(text, a.dpi_scale)
    tag = a.suite + (f"_{a.tag}" if a.tag else "")
    cases, cols = [], {}
    if a.suite == "xor":
        for corner, temp in (CORNERS if a.corners == "all" else CORNERS[:1]):
            k = f"{tag}_{corner}_{temp}"
            cols[k] = {"corner": corner, "temp": temp}
            cases += cases_for(k, base, corner, temp, pulses=a.pulses)
    elif a.suite == "mc":
        for s in range(a.mc):
            k = f"{tag}_s{s}"
            cols[k] = {"sample": s}
            cases += cases_for(k, base, seed=a.seed0 + s, pulses=a.pulses)
    else:
        names = [g.split("=", 1)[0] for g in a.grid]
        for vals in itertools.product(*[g.split("=", 1)[1].split(",") for g in a.grid]):
            k = f"{tag}_" + "_".join(f"{n}{v}" for n, v in zip(names, vals))
            cols[k] = dict(zip(names, vals))
            # a grid name "c0+c1" sets several parameters to the same value
            pv = {p: v for n, v in zip(names, vals) for p in n.split("+")}
            cases += cases_for(k, {**base, **pv}, pulses=a.pulses)
    tb.run_cases(cases, {"xor_tb": text}, RUNS, a.jobs)
    rows = summarize(cases, cols)
    note = (f"`{Path(a.sch).name}`, overrides {base or 'none'}, {a.pulses} input pulses per case. `out_AB`: output "
            "spikes for inputs A, B; `in`, `OR`, `AND`: spikes of input 1, hidden 0, hidden 1; `t_*`: first spike "
            "after the first pulse (us).")
    write(rows, tag, f"XOR on the 2-2-1 network: {a.suite}", note)


if __name__ == "__main__":
    main()
