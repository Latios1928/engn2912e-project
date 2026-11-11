"""XOR on snn_analog: inhibitory synapse, AND/OR hidden neurons, full network.

    python3 analog/testbenches/xor/run_xor.py                      # all suites
    python3 analog/testbenches/xor/run_xor.py --only hidden        # one suite
    python3 analog/testbenches/xor/run_xor.py --only and_mc --mc 200 --jobs 10

Suites:
  cell     inh_cell_tb: inhibitory vs excitatory charge for a 10-spike train, by code,
           membrane voltage, corner/temperature and mismatch
  hidden   hidden_tb at tt: every hidden weight code with one input (A) and with two (A+B)
  vlk      hidden_tb at tt: weights 1-4, one and two inputs, against the leak bias Vlk
  and_mc   hidden_tb with mismatch: AND and OR codes, inputs A, B and A+B on the same
           sample (same seed), so "leak beats one input, loses to two" is checked per chip
  xor      xor_tb: the 4 input cases on the full network, tt and corners
  xor_mc   xor_tb with mismatch: the 4 cases per sample

Writes results/xor_results.md and one CSV per suite. Each simulation runs in
runs/<case>/ (netlist, ngspice log, wrdata file).
"""

import argparse
import csv
import datetime
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402
sys.path.insert(0, str(HERE.parent / "dpi"))
from size_dpi import patch as patch_dpi  # noqa: E402

TBS = ["inh_cell_tb", "hidden_tb", "xor_tb"]
RESULTS = HERE / "results"
RUNS = HERE / "runs"
VTH = 1.65          # spike threshold for counting (half of VDD)
T0, TSP = 100e-6, 200e-6

# DAC branch weights 1:2:3:4: weight of each code
WEIGHT = [0, 1, 2, 3, 3, 4, 5, 6, 4, 5, 6, 7, 7, 8, 9, 10]
# One code per weight 1..10
CODE_OF_WEIGHT = {1: 1, 2: 2, 3: 3, 4: 8, 5: 9, 6: 10, 7: 11, 8: 13, 9: 14, 10: 15}

# XOR weights (xor_tb word codes) and output gain, chosen by the weight searches on xor_tb (tt):
# AND = weight 1 per input (threshold-mode hidden DPI), OR = code 15 (far above the threshold, close
# to saturation, so one and two inputs excite the output alike), hidden 1 -> output inhibitory at
# code 15, hidden 0 -> output excitatory at code 1, and p_vthr (output DPI gain) at the centre of its
# working range 2.77-2.80 V.
AND_CODE = 1
OR_CODE = 15
XOR_CODES = {"c0": 15, "c1": 15, "c3": OR_CODE, "c4": OR_CODE, "c6": AND_CODE, "c7": AND_CODE,
             "c18": 1, "c19": 15}
XOR_SIGNS = {"s0": 0, "s1": 1}
XOR_BIAS = {"p_vthr": 2.785}
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
VLK_SWEEP = [0.425, 0.44, 0.445, 0.45, 0.455, 0.46, 0.465, 0.47, 0.475, 0.48, 0.485, 0.49, 0.50]
CORNERS = [("tt", 27), ("ss", 27), ("ff", 27), ("sf", 27), ("fs", 27), ("tt", 0), ("tt", 85)]


# ------------------------------------------------------------------ waveform analysis
def edges(t, v, th=VTH):
    """Times of the rising crossings of th."""
    return [t[i] for i in range(1, len(v)) if v[i - 1] < th <= v[i]]


def v_before(t, v, t1, dt=2e-6):
    """v at the last sample before t1 - dt."""
    return v[max(i for i, tt in enumerate(t) if tt <= t1 - dt)]


def spurious(t, vm, spikes, vmin=1.5, jump=0.3):
    """False spikes: the membrane jumps by more than `jump` in one time step from below `vmin`
    within 3 us before the spike (what a too-large time step produced at relay spike edges,
    0.98 -> 1.77 V in one 0.2 us step). A membrane charged quickly by a large DPI current rises
    steeply but smoothly and is not counted. Should be 0; reported so it cannot go unnoticed."""
    import bisect
    n = 0
    for t1 in spikes:
        i1 = bisect.bisect_left(t, t1)
        i0 = bisect.bisect_left(t, t1 - 3e-6)
        if any(vm[i] < vmin and vm[i + 1] - vm[i] > jump for i in range(max(i0, 0), max(i1 - 1, 0))):
            n += 1
    return n


def hidden_metrics(case):
    w = tb.read_wrdata(RUNS / case.name / "hidden_tb.txt")
    t, vm = w["time"], w["v(vmem_h)"]
    sa, sb, sh = (edges(t, w[k]) for k in ("v(spk_a)", "v(spk_b)", "v(spk_h)"))
    r = {"n_a": len(sa), "n_b": len(sb), "n_h": len(sh), "n_spurious": spurious(t, vm, sh)}
    if sh:
        t1 = sh[0]
        r["t_first_us"] = (t1 - T0) * 1e6
        r["pulse_first"] = int((t1 - T0) // TSP) + 1
        # The membrane rises smoothly to the threshold, then jumps within ~1 us
        r["v_fire"] = v_before(t, vm, t1)
    else:
        r["vmax_pre"] = max(vm)
        # Still rising at the end? Compare the last quarter with the third quarter.
        n = len(t)
        r["vmax_q3"] = max(vm[n // 2:3 * n // 4])
        r["vmax_q4"] = max(vm[3 * n // 4:])
    return r


def xor_metrics(case):
    w = tb.read_wrdata(RUNS / case.name / "xor_tb.txt")
    t = w["time"]
    r = {f"n{k}": len(edges(t, w[f"v(sp{k})"])) for k in (0, 1, 3, 4, 8)}
    s8 = edges(t, w["v(sp8)"])
    r["n_spurious"] = sum(spurious(t, w[f"v(x1.vmem_{k})"], edges(t, w[f"v(sp{k})"])) for k in (3, 4, 8))
    r["t_out_us"] = (s8[0] - T0) * 1e6 if s8 else None
    r["vmax_out"] = max(w["v(x1.vmem_8)"])
    return r


# ------------------------------------------------------------------ suites
def suite_cell(a):
    cases = []
    for code in (1, 2, 8, 15):
        for vmem in (0.2, 0.8, 1.4):
            cases.append(tb.Case(f"cell_c{code}_v{vmem}", "inh_cell_tb", params={"code": code, "vmem": vmem},
                                 tags={"code": code, "vmem": vmem}))
    for corner, temp in CORNERS:
        cases.append(tb.Case(f"cell_{corner}_{temp}", "inh_cell_tb", corner, temp, {"code": 2},
                             tags={"code": 2, "vmem": 0.5}))
    for i in range(a.mc):
        cases.append(tb.Case(f"cell_mc{i}", "inh_cell_tb", params={"code": 2}, seed=1000 + i,
                             tags={"code": 2, "vmem": 0.5}))
    return cases


def suite_hidden(a):
    cases = []
    for wt, code in CODE_OF_WEIGHT.items():
        for name, ina, inb in (("A", 1, 0), ("AB", 1, 1)):
            cases.append(tb.Case(f"hid_w{wt}_{name}", "hidden_tb",
                                 params={"ca": code, "cb": code, "ina": ina, "inb": inb},
                                 tags={"weight": wt, "code": code, "inputs": name}))
    return cases


def suite_vlk(a):
    cases = []
    for vlk in ([float(x) for x in a.vlk.split(",")] if a.vlk else VLK_SWEEP):
        for wt in ([int(x) for x in a.weights.split(",")] if a.weights else (1, 2, 3, 4)):
            for name, ina, inb in (("A", 1, 0), ("AB", 1, 1)):
                cases.append(tb.Case(f"vlk{a.tag or ''}{vlk}_w{wt}_{name}", "hidden_tb",
                                     params={"p_vlk": vlk, "ca": CODE_OF_WEIGHT[wt], "cb": CODE_OF_WEIGHT[wt],
                                             "ina": ina, "inb": inb},
                                     tags={"vlk": vlk, "weight": wt, "inputs": name}))
    return cases


def suite_and_mc(a):
    cases = []
    for role, code in (("AND", a.and_code), ("OR", a.or_code)):
        if role not in a.roles.split(","):
            continue
        for i in range(a.mc):
            for name, ina, inb in (("A", 1, 0), ("B", 0, 1), ("AB", 1, 1)):
                cases.append(tb.Case(f"mc{a.tag or ''}_{role}_{i}_{name}", "hidden_tb",
                                     params={"ca": code, "cb": code, "ina": ina, "inb": inb}, seed=2000 + i,
                                     tags={"role": role, "code": code, "sample": i, "inputs": name}))
    return cases


def xor_params(ina, inb, extra=None):
    p = dict(XOR_CODES, **XOR_SIGNS, **XOR_BIAS, ina=ina, inb=inb)
    p.update(extra or {})
    return p


def suite_xor(a):
    cases = []
    for corner, temp in CORNERS if not a.quick else CORNERS[:1]:
        for ina, inb in CASES:
            cases.append(tb.Case(f"xor_{corner}_{temp}_{ina}{inb}", "xor_tb", corner, temp, xor_params(ina, inb),
                                 tags={"corner": corner, "temp": temp, "A": ina, "B": inb}))
    return cases


def suite_xor_mc(a):
    cases = []
    for i in range(a.mc_xor):
        for ina, inb in CASES:
            cases.append(tb.Case(f"xmc_{i}_{ina}{inb}", "xor_tb", params=xor_params(ina, inb), seed=3000 + i,
                                 tags={"sample": i, "A": ina, "B": inb}))
    return cases


SUITES = {"cell": suite_cell, "hidden": suite_hidden, "vlk": suite_vlk, "and_mc": suite_and_mc, "xor": suite_xor,
          "xor_mc": suite_xor_mc}
METRICS = {"hidden_tb": hidden_metrics, "xor_tb": xor_metrics}


# ------------------------------------------------------------------ report
def fmt(v):
    if v is None:
        return "–"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def md_table(rows, keys):
    out = ["| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    out += ["| " + " | ".join(fmt(r.get(k)) for k in keys) + " |" for r in rows]
    return "\n".join(out)


def rows_of(cases):
    rows = []
    for c in cases:
        r = dict(c.tags, ok=c.ok, corner=c.corner, temp=c.temp)
        r.update(c.results)
        rows.append(r)
    return rows


def write_csv(name, rows):
    keys = sorted({k for r in rows for k in r})
    with open(RESULTS / f"{name}.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, keys)
        wr.writeheader()
        wr.writerows(rows)


def summarize(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return "–"
    return f"mean {statistics.mean(vals):.4g}, std {statistics.stdev(vals):.3g}, " \
           f"min {min(vals):.4g}, max {max(vals):.4g} (n = {len(vals)})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated suites: " + ",".join(SUITES))
    ap.add_argument("--mc", type=int, default=100, help="mismatch samples for cell and and_mc (default 100)")
    ap.add_argument("--mc-xor", type=int, default=30, help="mismatch samples for xor_mc (default 30)")
    ap.add_argument("--and-code", type=int, default=AND_CODE, help=f"AND neuron weight code (default {AND_CODE})")
    ap.add_argument("--or-code", type=int, default=OR_CODE, help=f"OR neuron weight code (default {OR_CODE})")
    ap.add_argument("--roles", default="AND,OR", help="and_mc: which neurons to run (default AND,OR)")
    ap.add_argument("--quick", action="store_true", help="xor at tt only")
    ap.add_argument("--jobs", type=int, default=10, help="parallel ngspice runs")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                    help="override a .param in every simulation (e.g. --set p_vlk=0.5); repeatable")
    ap.add_argument("--dpi-k", help="DPI device scales k1,k2,k3,k4 (W = 0.22u*k, L = 0.28u*k; see "
                    "dpi/size_dpi.py); pair with --set vthr=.. --set vtau=.. --set vtau_i=.. from its retune")
    ap.add_argument("--tag", help="suffix for the result files (results/<suite>_<tag>.csv/.md), "
                    "so runs with different settings are kept side by side")
    ap.add_argument("--weights", help="vlk suite: comma-separated hidden weights (default 1,2,3,4)")
    ap.add_argument("--vlk", help="vlk suite: comma-separated Vlk values (default VLK_SWEEP)")
    ap.add_argument("--report", action="store_true",
                    help="no simulation: rebuild the report sections from the CSVs in results/")
    a = ap.parse_args()
    overrides = dict(kv.split("=", 1) for kv in a.set)
    if a.report:
        for name in SUITES:
            for f in _files(name, ".csv"):
                with open(f) as fh:
                    rows = [{k: _value(v) for k, v in r.items()} for r in csv.DictReader(fh)]
                f.with_suffix(".md").write_text(f"<!-- {name}: rebuilt from {f.name} -->\n"
                                                + REPORTERS[name](rows) + "\n")
        write_report()
        return

    suites = a.only.split(",") if a.only else list(SUITES)
    RESULTS.mkdir(exist_ok=True)
    netdir = RUNS / "_netlists"
    netlists = {}
    for name in TBS:
        text = tb.netlist(HERE / f"{name}.sch", netdir).read_text()
        if "IS MISSING" in text:
            sys.exit(f"{name}: netlist has missing symbols")
        for sub in ("DAC", "DAC_signed", "DPI", "DPI_inh", "neuron_sized", "snn_analog"):
            tb.check_connected(text, sub)
        if a.dpi_k:
            text = patch_dpi(text, [float(x) for x in a.dpi_k.split(",")])
        netlists[name] = text

    for name in suites:
        cases = SUITES[name](a)
        for c in cases:
            c.params = {**c.params, **overrides}
            c.tags.update({k: v for k, v in overrides.items()})
        print(f"{name}: {len(cases)} simulations", flush=True)
        tb.run_cases(cases, netlists, RUNS, a.jobs)
        for c in cases:
            # A floating node (e.g. a bias net renamed by a .param of the same name) shows up only
            # as this warning, and the run still "succeeds": treat it as a failure
            if "singular matrix" in c.log:
                c.ok = False
                c.results["error"] = "singular matrix"
            if c.ok and c.tb in METRICS:
                c.results.update(METRICS[c.tb](c))
        bad = [c.name for c in cases if not c.ok]
        if bad:
            print(f"  {len(bad)} failed: {bad[:5]}")
        rows = rows_of(cases)
        for r, c in zip(rows, cases):
            r["name"] = c.name
            r["mc"] = c.seed is not None
        fname = f"{name}_{a.tag}" if a.tag else name
        write_csv(fname, rows)
        head = f"<!-- {name}: run_xor.py on {datetime.date.today()}" \
               + (f", overrides {overrides}" if overrides else "") \
               + (f", DPI scales {a.dpi_k}" if a.dpi_k else "") + " -->\n"
        (RESULTS / f"{fname}.md").write_text(head + REPORTERS[name](rows) + "\n")
    write_report()


def _value(v):
    """A CSV cell back to int / float / bool / None."""
    if v in ("", "None"):
        return None
    if v in ("True", "False"):
        return v == "True"
    for conv in (int, float):
        try:
            return conv(v)
        except ValueError:
            pass
    return v


def _files(suite, ext):
    """results/<suite><ext> and results/<suite>_<tag><ext>, untagged first."""
    plain = RESULTS / f"{suite}{ext}"
    return ([plain] if plain.exists() else []) + sorted(RESULTS.glob(f"{suite}_*{ext}"))


def write_report():
    """The report is every suite section written so far, in suite order."""
    parts = ["# XOR on snn_analog: simulation results", "",
             "Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.", ""]
    parts += [f.read_text() for n in SUITES for f in _files(n, ".md")]
    (RESULTS / "xor_results.md").write_text("\n".join(parts))
    print(f"report: {RESULTS / 'xor_results.md'}")


# ------------------------------------------------------------------ per-suite report sections
def rep_cell(rows):
    for r in rows:
        for k in ("q_exc", "q_inh", "x_exc", "x_inh"):
            if r.get(k) is not None:
                r[k + "_fc"] = r[k] * 1e15
    sweep = [r for r in rows if not r["mc"] and r["name"].startswith("cell_c")]
    pvt = [r for r in rows if not r["mc"] and not r["name"].startswith("cell_c")]
    mc = [r for r in rows if r["mc"] and r["ok"]]
    return "\n".join([
        "## Inhibitory vs excitatory synapse (`inh_cell_tb`)", "",
        "Charge for a train of 10 spikes at 5 kHz; both outputs held at `vmem`. "
        "`ratio` = q_inh / q_exc (1 = matched). `x_exc_fc`, `x_inh_fc`: charge that reaches the wrong DPI "
        "through the off steering switch.", "",
        md_table(sweep, ["code", "vmem", "q_exc_fc", "q_inh_fc", "ratio", "x_exc_fc", "x_inh_fc"]), "",
        "Code 2, vmem = 0.5 V, corners and temperature:", "",
        md_table(pvt, ["corner", "temp", "q_exc_fc", "q_inh_fc", "ratio"]), "",
        f"Mismatch, code 2: ratio {summarize([r.get('ratio') for r in mc])}; "
        f"q_exc (fC) {summarize([r.get('q_exc_fc') for r in mc])}.", ""])


def rep_hidden(rows):
    by = {}
    for r in rows:
        by.setdefault(r["weight"], {})[r["inputs"]] = r
    out = []
    for wt in sorted(by):
        A, AB = by[wt].get("A", {}), by[wt].get("AB", {})
        out.append({"weight": wt, "code": A.get("code"),
                    "A: spikes": A.get("n_h"), "A: first at pulse": A.get("pulse_first"),
                    "A: VMEM max (V)": A.get("vmax_pre"),
                    "A+B: spikes": AB.get("n_h"), "A+B: first at pulse": AB.get("pulse_first"),
                    "relay spikes": A.get("n_a")})
    return "\n".join([
        "## Hidden neuron vs weight (`hidden_tb`, tt, 27 °C)", "",
        "Two relay neurons (code 15, 5 kHz pulses) drive the hidden neuron's DACs; both hidden weights "
        "equal. 10 ms (50 pulses). AND needs **no** spike with A alone and a spike with A+B; OR needs "
        "a spike with A alone. `VMEM max` with no spike is how close one input gets to firing.", "",
        md_table(out, list(out[0].keys())), ""])


def rep_and_mc(rows):
    out = ["## AND and OR neurons with mismatch (`hidden_tb`)", "",
           "Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, "
           "so all three see the same devices. 10 ms (50 pulses).", ""]
    for role in ("AND", "OR"):
        if not any(r["role"] == role for r in rows):
            continue
        samples = {}
        for r in rows:
            if r["role"] == role and r["ok"]:
                samples.setdefault(r["sample"], {})[r["inputs"]] = r
        full = {i: s for i, s in samples.items() if len(s) == 3}
        code = next(iter(rows))["code"] if rows else None
        code = next((r["code"] for r in rows if r["role"] == role), code)
        if role == "AND":
            good = [i for i, s in full.items()
                    if s["A"]["n_h"] == 0 and s["B"]["n_h"] == 0 and s["AB"]["n_h"] > 0]
            fail_single = [i for i, s in full.items() if s["A"]["n_h"] > 0 or s["B"]["n_h"] > 0]
            fail_double = [i for i, s in full.items() if s["AB"]["n_h"] == 0]
            single_max = [max(s["A"]["vmax_pre"], s["B"]["vmax_pre"]) for s in full.values()
                          if s["A"]["n_h"] == 0 and s["B"]["n_h"] == 0]
            out += [f"**AND (code {code}, weight {WEIGHT[code]}):** {len(good)} / {len(full)} samples pass "
                    f"(no spike with one input, spike with two).",
                    f"- One input fired it: {len(fail_single)} samples {sorted(fail_single)[:20]}",
                    f"- Two inputs did not fire it: {len(fail_double)} samples {sorted(fail_double)[:20]}",
                    f"- Highest VMEM with one input (passing samples, V): {summarize(single_max)}",
                    f"- Firing VMEM with two inputs (V): {summarize([s['AB'].get('v_fire') for s in full.values()])}",
                    f"- First spike with two inputs, pulse number: "
                    f"{summarize([s['AB'].get('pulse_first') for s in full.values()])}",
                    f"- Spikes in 50 pulses with two inputs: {summarize([s['AB']['n_h'] for s in full.values()])}",
                    f"- Relay spikes in 50 pulses (nominal 49): "
                    f"{summarize([s[k]['n_a'] for s in full.values() for k in ('A', 'AB')])}",
                    f"- False spikes (should be 0): {sum(s[k].get('n_spurious', 0) for s in full.values() for k in s)}",
                    ""]
        else:
            good = [i for i, s in full.items() if min(s[k]["n_h"] for k in ("A", "B", "AB")) > 0]
            out += [f"**OR (code {code}, weight {WEIGHT[code]}):** {len(good)} / {len(full)} samples fire "
                    f"with A, with B and with A+B.",
                    f"- First spike with one input, pulse number: "
                    f"{summarize([s[k].get('pulse_first') for s in full.values() for k in ('A', 'B')])}",
                    f"- First spike with two inputs, pulse number: "
                    f"{summarize([s['AB'].get('pulse_first') for s in full.values()])}", ""]
    return "\n".join(out)


def xor_ok(r):
    want = r["A"] ^ r["B"]
    return (r.get("n8", 0) > 0) == bool(want)


def rep_xor(rows):
    for r in rows:
        r["XOR"] = r["A"] ^ r["B"]
        r["pass"] = xor_ok(r) if r["ok"] else False
    keys = ["corner", "temp", "A", "B", "XOR", "n0", "n1", "n3", "n4", "n8", "t_out_us", "vmax_out", "pass"]
    return "\n".join([
        "## XOR on the full network (`xor_tb`)", "",
        f"Weights: {XOR_CODES}, signs {XOR_SIGNS} (s1 = 1: hidden 1 -> output inhibitory), {XOR_BIAS}. "
        "4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); "
        "`n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.", "",
        md_table(rows, keys), ""])


def rep_xor_mc(rows):
    samples = {}
    for r in rows:
        if r["ok"]:
            samples.setdefault(r["sample"], []).append(r)
    full = {i: s for i, s in samples.items() if len(s) == 4}
    good = [i for i, s in full.items() if all(xor_ok(r) for r in s)]
    lines = ["## XOR with mismatch (`xor_tb`)", "",
             f"{len(good)} / {len(full)} samples give the right output in all 4 cases.", ""]
    for ab in CASES:
        rs = [r for s in full.values() for r in s if (r["A"], r["B"]) == ab]
        bad = sorted(r["sample"] for r in rs if not xor_ok(r))
        lines.append(f"- A={ab[0]} B={ab[1]}: output spikes {summarize([r.get('n8') for r in rs])}; "
                     f"AND spikes {summarize([r.get('n4') for r in rs])}; wrong in samples {bad[:20]}")
    return "\n".join(lines) + "\n"


def rep_vlk(rows):
    by = {}
    for r in rows:
        by.setdefault((r["vlk"], r["weight"]), {})[r["inputs"]] = r
    out = []
    for (vlk, wt), d in sorted(by.items()):
        A, AB = d.get("A", {}), d.get("AB", {})
        out.append({"Vlk (V)": vlk, "weight": wt, "A: spikes": A.get("n_h"),
                    "A: VMEM max (V)": A.get("vmax_pre") if not A.get("n_h") else None,
                    "A+B: spikes": AB.get("n_h"), "A+B: first at pulse": AB.get("pulse_first"),
                    "A+B: VMEM max (V)": AB.get("vmax_pre") if not AB.get("n_h") else None,
                    "relay spikes": A.get("n_a"), "false spikes": A.get("n_spurious", 0) + AB.get("n_spurious", 0),
                    "AND": "yes" if A.get("n_h") == 0 and (AB.get("n_h") or 0) > 0 else ""})
    return "\n".join([
        "## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)", "",
        "10 ms (50 pulses). `AND` = no spike with one input, at least one with two. "
        "`VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).", "",
        md_table(out, list(out[0].keys())), ""])


REPORTERS = {"cell": rep_cell, "hidden": rep_hidden, "vlk": rep_vlk, "and_mc": rep_and_mc, "xor": rep_xor, "xor_mc": rep_xor_mc}

if __name__ == "__main__":
    main()
