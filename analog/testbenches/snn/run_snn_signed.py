"""Scenario runner for snn_signed_tb.sch: the 2-2-1 network with every synapse signed.

    python3 analog/testbenches/snn/run_snn_signed.py                 # all scenarios, tt 27 C
    python3 analog/testbenches/snn/run_snn_signed.py --only 3,5
    python3 analog/testbenches/snn/run_snn_signed.py --corner ss --temp 0
    python3 analog/testbenches/snn/run_snn_signed.py --pex           # post-layout macro
    python3 analog/testbenches/snn/run_snn_signed.py --mc 50         # mismatch, 50 chips
    python3 analog/testbenches/snn/run_snn_signed.py --mc 50 --mi2-w 2u   # same chips, old 1:1 mirror
    python3 analog/testbenches/snn/run_snn_signed.py --drawn --mc 50 # drawn sizes, no parasitics

Network: analog/snn/snn_analog_signed.sch. Every synapse is DAC (magnitude 0-15 on
1:2:4:8, sign s[k]: 0 = excitatory, 1 = inhibitory). Words (as mock/snn_analog.v):
  0, 1        pulse[i] -> input i        (inhibitory = current to VDD, no input)
  2 + 2j + i  input i  -> hidden j       (inhibitory -> DPI_inh xdpi6 / xdpi7)
  6 + j       hidden j -> output         (inhibitory -> DPI_inh xdpi5)
Biases come from bias (Iref 100 nA); VT = 1.66 V. Inputs: 10 us pulses every 200 us from
50 us, for 3 ms. Each scenario is its own simulation, so membranes start empty (the mixed/
testbench has no reset and carries history from one scenario to the next).

Scenarios 1-5 are those of mixed/README.md with +7 replaced by +15 (the 4-bit magnitude);
scenario 5 is the one that failed there for lack of a sign. 6-8 test the sign at the input and
output layers. A neuron "fires" if it spikes at least once in the run.

--pex replaces the network x1 and the bias cell xbias by the C-only extraction of the signed
macro (layout_tools/top_pex.sh -> layout_tools/top/SNN_signed/pex/SNN_signed_pex.spice, which
contains the bias cell). Its VMEM nets are the labels DPI_k.Isyn (VMEM_i = DPI_{4-i}.Isyn).

--mc N runs every selected scenario on N mismatch seeds (one seed = one chip, the PDK's
sw_stat_mismatch, bias cell included) and reports per-scenario and chip yield; run folders of
passing runs are deleted unless --keep. --mi2-w overrides the DPI_inh output-mirror width in the
schematic or --drawn netlist (2.4u = gain 1.2, the design; 2u = the old 1:1 mirror).

--drawn uses the macro's LVS reference instead (drawn device sizes, e.g. 0.5/0.64 um where the
schematic has 0.22/0.28 um, and dummies; no parasitics): mismatch scales with device area, so
this is the faster stand-in for --pex in Monte Carlo runs.

Writes results/snn_signed_tb[__pex|__drawn][__mi2w<W>][__<corner>_<temp>][__mc<N>].md
(corner/temp part only when not tt 27 C).
"""

import argparse
import filecmp
import re
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402

TB = "snn_signed_tb"
NEURONS = ["in0", "in1", "hid0", "hid1", "out"]
# name, weights {word: signed magnitude}, inputs (in0, in1), neurons that must fire
SCENARIOS = [
    ("1 all +15, no input", {k: 15 for k in range(8)}, (0, 0), set()),
    ("2 pulse0 -> in0 only", {0: 15}, (1, 0), {"in0"}),
    ("3 path in1 -> hid1 -> out", {1: 15, 5: 15, 7: 15}, (1, 1), {"in1", "hid1", "out"}),
    ("4 as 3, hid1 -> out = 0", {1: 15, 5: 15}, (1, 1), {"in1", "hid1"}),
    ("5 as 3, plus in0 -> hid1 = -15", {0: 15, 1: 15, 4: -15, 5: 15, 7: 15}, (1, 1), {"in0", "in1"}),
    ("6 pulse0 -> in0 = -15", {0: -15}, (1, 0), set()),
    ("7 hid0 -> out = -15 against hid1 -> out = +15", {0: 15, 1: 15, 2: 15, 5: 15, 6: -15, 7: 15}, (1, 1),
     {"in0", "in1", "hid0", "hid1"}),
    ("8 control for 7: hid0 -> out = 0", {0: 15, 1: 15, 2: 15, 5: 15, 7: 15}, (1, 1),
     {"in0", "in1", "hid0", "hid1", "out"}),
]


MACRO = tb.ROOT / "analog" / "layout_tools" / "top" / "SNN_signed"
PEX = MACRO / "pex" / "SNN_signed_pex.spice"


LMAX = 50e-6   # longest L the GF180 nfet/pfet_03v3 model bins cover
TRIM = 9       # trim code for a macro with the on-chip reference (bias_master + trim_steer); --trim


def split_long(pex):
    """FETs longer than LMAX (bias MR_VK: 0.5/90.91 um) -> n equal series segments, same W and
    total L, so ngspice finds a model bin. Simulation copy only; the extraction is unchanged."""
    out, n_split = [], 0
    for ln in pex.splitlines():
        m = re.match(r"^(X\S+) (\S+) (\S+) (\S+) (\S+) ([np]fet_03v3) (.*)$", ln)
        lm = m and re.search(r"(?<=\s)l=([0-9.]+)u", " " + m.group(7), re.I)
        if not lm or float(lm.group(1)) * 1e-6 <= LMAX:
            out.append(ln)
            continue
        name, d, g, src, b, mod, rest = m.groups()
        L = float(lm.group(1))
        n = int(L * 1e-6 // LMAX) + 1
        rest = re.sub(r"(?<=\s)(l)=[0-9.]+u", rf"\g<1>={L / n:.4f}u", " " + rest, flags=re.I).strip()
        nodes = [d] + [f"{name}_s{i}" for i in range(1, n)] + [src]
        for i in range(n):
            out.append(f"{name}_{i} {nodes[i]} {g} {nodes[i + 1]} {b} {mod} {rest}")
        n_split += 1
    print(f"split {n_split} FET(s) longer than {LMAX * 1e6:.0f} um into series segments")
    return "\n".join(out) + "\n"


def drop_tied_dummies(net):
    """Remove FETs with all four terminals on one net (layout dummies): no current, no
    capacitance (every junction sits between one node and itself). They are ~80 % of the macro's
    FETs, so dropping them makes the simulation copy several times faster; results are identical."""
    keep, n = [], 0
    for ln in net.replace("\n+", " ").splitlines():
        m = re.match(r"^X\S+ (\S+) (\S+) (\S+) (\S+) [np]fet_03v3 ", ln)
        if m and len(set(m.groups())) == 1:
            n += 1
            continue
        keep.append(ln)
    print(f"dropped {n} fully tied dummy FETs from the simulation copy")
    return "\n".join(keep) + "\n"


def swap_macro(text, sim, subckt):
    """Replace x1 (snn_analog_signed) + xbias (bias) by one instance of `subckt` from `sim`."""
    body = sim.read_text().replace("\n+", " ")
    pins = re.search(rf"^\.subckt {subckt} (.*?)$", body, re.M | re.I).group(1)
    lines, out, depth = text.replace("\n+", " ").splitlines(), [], 0
    for ln in lines:
        t = ln.split()
        depth += bool(t) and t[0].lower() == ".subckt"
        depth -= bool(t) and t[0].lower() == ".ends"
        if depth == 0 and t and t[0] == "x1":
            out.append(f"x1 {pins} {subckt}")   # tb nets carry the macro pin names
        elif depth == 0 and t and t[0] == "xbias":
            out.append("* xbias: inside the macro")
        else:
            out.append(ln)
    if "cal" in pins.split():
        # the macro makes its own reference (bias_master -> trim_steer -> bias): no Iref source;
        # drive the trim code (TRIM) and cal = 0, hold the Imon pad at 1.65 V (its trim target)
        out = [f"* {ln} (no Iref pin: on-chip reference)" if ln.split()[:1] == ["IREF"] else ln for ln in out]
        end = max(i for i, ln in enumerate(out) if ln.strip().lower() == ".end")
        out[end:end] = [f"Vtrim{b} trim[{b}] 0 {{p_vdd * {(TRIM >> b) & 1}}}" for b in (3, 2, 1, 0)] + [
            "Vcal cal 0 0", "Vimon Imon 0 1.65"]
    last_lib = max(i for i, ln in enumerate(out) if ln.startswith(".lib"))
    out.insert(last_lib + 1, f".include {sim}")
    if re.search(r"^X\S* .* nwell ", body, re.M):       # n-well resistors: their model section
        lib = out[last_lib].split()[1]                   # (tbtools.prepare sets its corner)
        out.insert(last_lib + 1, f".lib {lib} res_typical")
    return "\n".join(out) + "\n"


def use_pex(text):
    """Swap x1 (snn_analog_signed) + xbias (bias) for the extracted macro SNN_signed_flat."""
    if not PEX.exists() or not filecmp.cmp(MACRO / "SNN_signed.gds", MACRO / "pex" / "SNN_signed.gds",
                                           shallow=False):
        raise RuntimeError("extraction missing or older than SNN_signed.gds; run "
                           "bash analog/layout_tools/top_pex.sh SNN_signed")
    pex = PEX.read_text()
    # VMEM_i = DPI_{4-i}.Isyn; '.' in other label names -> '_' (ngspice uses '.' for hierarchy)
    for k in range(5):
        pex = re.sub(rf"(?<=\s)DPI_{k}\.Isyn(?=\s)", f"VMEM_{4 - k}", pex)
    pex = re.sub(r"(?<=\s)([A-Za-z]\w*)\.(\w+)(?=\s)", r"\1__\2", pex)
    pex = split_long(drop_tied_dummies(pex))
    sim = PEX.with_name("SNN_signed_pex_sim.spice")
    sim.write_text(pex)
    return swap_macro(text, sim, "SNN_signed_flat")


def use_drawn(text, mi2_w=None, dpi_size=None):
    """Swap x1 + xbias for the macro's LVS reference: drawn device sizes (e.g. 0.5/0.64 um for
    the schematic's 0.22/0.28 um), dummies, no parasitics. For mismatch at the real device areas
    at schematic speed."""
    ref = MACRO / "SNN_signed_lvs_ref.spice"
    if not ref.exists() or ref.stat().st_mtime < (MACRO / "SNN_signed.gds").stat().st_mtime - 60:
        raise RuntimeError(f"{ref} missing or older than SNN_signed.gds; run top.py route SNN_signed")
    net = ref.read_text().replace("cap_mim_2f0fF", "cap_mim_2f0_m4m5_noshield")   # LVS name -> model
    net = re.sub(r"^(X\S+ \S+ \S+ cap_mim\S* c_width=\S+ c_length=\S+) m=1$", r"\1", net, flags=re.M)
    net = split_long(drop_tied_dummies(net))
    if mi2_w:
        net = set_mi2_w(net, mi2_w)
    if dpi_size:
        net = set_dpi_size(net, dpi_size)
    sim = HERE / "runs" / "_netlist" / "SNN_signed_drawn_sim.spice"
    sim.parent.mkdir(parents=True, exist_ok=True)
    sim.write_text(net)
    return swap_macro(text, sim, "SNN_signed")


def params(weights, inputs):
    p = {"p_in0": inputs[0], "p_in1": inputs[1]}
    for k in range(8):
        v = weights.get(k, 0)
        p[f"p_w{k}"] = abs(v)
        p[f"p_s{k}"] = 1 if v < 0 else 0
    return p


def spikes(col, vsw=1.65):
    """Rising crossings of vsw."""
    n, above = 0, False
    for v in col:
        if not above and v > vsw:
            n, above = n + 1, True
        elif above and v < vsw:
            above = False
    return n


def first_spike(t, col, vsw=1.65):
    for ti, v in zip(t, col):
        if v > vsw:
            return ti
    return None


def wstr(w):
    return ", ".join(f"w{k}={v:+d}" for k, v in sorted(w.items())) or "all 0"


def evaluate(c):
    """Spike counts and first spikes of a finished case -> (counts, firsts, ok). counts None = sim failed."""
    if not c.ok:
        return None, None, False
    d = tb.read_wrdata(HERE / "runs" / c.name / f"{TB}.txt")
    t = d["time"]
    counts = [spikes(d[f"v(sp{i})"]) for i in range(len(NEURONS))]
    firsts = [first_spike(t, d[f"v(sp{i})"]) for i in range(len(NEURONS))]
    must = c.tags["scen"][3]
    ok = all((k > 0) == (nn in must) for nn, k in zip(NEURONS, counts))
    return counts, firsts, ok


def set_mi2_w(text, w):
    """Override the DPI_inh output-mirror width (Mi2) in a schematic netlist."""
    out, sub, hits = [], None, 0
    for ln in text.replace("\n+", " ").splitlines():
        t = ln.split()
        if t and t[0].lower() == ".subckt":
            sub = t[1]
        if sub == "DPI_inh" and t and t[0] == "XMi2":
            ln, n = re.subn(r"\bW=\S+", f"W={w}", ln, count=1)
            hits += n
        out.append(ln)
    if hits != 1:
        raise RuntimeError(f"--mi2-w: expected one XMi2 in subckt DPI_inh, found {hits}")
    return "\n".join(out) + "\n"


DPI_DEV = re.compile(r"^X(x1_)?M[1-4](_f\d+)?$")            # DPI M1-M4 (in DPI_inh: x1_M1-M4)
REPLICA = re.compile(r"^XMR_(Vthr|VT_dpi)(_f\d+)?$")       # their bias-cell replicas


def set_dpi_size(text, size):
    """Resize the DPI input pair / mirror M1-M4 (DPI and DPI_inh) and the bias replicas of
    Vthr / VT_dpi to W/L = size (e.g. "2u/2.56u"), keeping finger and m counts. Works on the
    schematic and the --drawn netlist."""
    w, l = size.split("/")
    out, sub, hits = [], None, {"DPI": 0, "DPI_inh": 0, "bias": 0}
    for ln in text.replace("\n+", " ").splitlines():
        t = ln.split()
        if t and t[0].lower() == ".subckt":
            sub = t[1]
        if t and ((sub in ("DPI", "DPI_inh") and DPI_DEV.match(t[0])) or (sub == "bias" and REPLICA.match(t[0]))):
            ln = re.sub(r"\bL=\S+", f"L={l}", re.sub(r"\bW=\S+", f"W={w}", ln, count=1), count=1)
            hits[sub] += 1
        out.append(ln)
    if hits["DPI"] != 4 or hits["bias"] < 2:
        raise RuntimeError(f"--dpi-size: unexpected device count {hits}")
    return "\n".join(out) + "\n"


def header(tag, a, extra=()):
    return [f"# {TB}{tag}: signed 2-2-1 network", "",
            f"Generated by `run_snn_signed.py` on {time.strftime('%Y-%m-%d %H:%M')}, {a.corner} {a.temp:g} C. "
            "Network `analog/snn/snn_analog_signed.sch` (all synapses `DAC`), biases from "
            "`bias` (Iref 100 nA), VT 1.66 V, 10 us pulses every 200 us from 50 us, 3 ms per scenario.",
            *(["", "**Post-layout:** network and bias cell replaced by the C-only Magic extraction of "
               "`layout_tools/top/SNN_signed/SNN_signed.gds` (`top_pex.sh`, C >= 0.01 fF, no wire R)."]
              if a.pex else []),
            *(["", "**Drawn sizes:** network and bias cell replaced by the macro's LVS reference "
               "(`layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice`: drawn device sizes and dummies, "
               "no parasitics)."] if a.drawn else []),
            *(["", f"**DPI M1-M4 and bias Vthr / VT_dpi replicas W/L = {a.dpi_size}** (patched netlist)."] if a.dpi_size else []),
            *(["", f"**DPI_inh Mi2 W = {a.mi2_w}** (schematic default 2.4u, mirror gain 1.2)."] if a.mi2_w else []),
            *extra]


def report_mc(cases, a, tag, t0):
    """Monte Carlo report: per-scenario yield, chip yield, failing chips, spike-count spread."""
    seeds = sorted({c.seed for c in cases})
    scen = []
    for c in cases:
        if c.tags["scen"] not in scen:
            scen.append(c.tags["scen"])
    res = {}
    for c in cases:
        counts, firsts, ok = evaluate(c)
        res[(c.seed, c.tags["scen"][0])] = (counts, firsts, ok)
        if ok and not a.keep:
            shutil.rmtree(HERE / "runs" / c.name, ignore_errors=True)
    L = header(tag, a, ["", f"**Mismatch Monte Carlo:** PDK `sw_stat_mismatch`, {len(seeds)} samples "
                            f"(seeds {seeds[0]}-{seeds[-1]}). One seed = one chip: every scenario of a seed sees "
                            "the same device mismatch, including the bias cell."])
    L += ["", "| scenario | must fire | pass | " + " | ".join(f"{n} mean (min-max)" for n in NEURONS) + " |",
          "|---|---|---|" + "---|" * len(NEURONS)]
    for s in scen:
        rows = [res[(sd, s[0])] for sd in seeds]
        good = [r for r in rows if r[0] is not None]
        n_ok = sum(r[2] for r in rows)
        stats = []
        for i in range(len(NEURONS)):
            v = [r[0][i] for r in good]
            stats.append(f"{sum(v) / len(v):.1f} ({min(v)}-{max(v)})" if v else "-")
        L.append(f"| {s[0]} | {', '.join(n for n in NEURONS if n in s[3]) or 'none'} | "
                 f"{n_ok} / {len(rows)} | " + " | ".join(stats) + " |")
    chip_ok = [sd for sd in seeds if all(res[(sd, s[0])][2] for s in scen)]
    L += ["", f"**Chip yield: {len(chip_ok)} / {len(seeds)}** (all {len(scen)} scenarios pass on the same seed)."]
    fails = [(sd, s) for sd in seeds for s in scen if not res[(sd, s[0])][2]]
    if fails:
        L += ["", "Failing runs (spike counts; first spike in us; bold = wrong):", "",
              "| seed | scenario | " + " | ".join(NEURONS) + " |", "|---|---|" + "---|" * len(NEURONS)]
        for sd, s in fails:
            counts, firsts, _ = res[(sd, s[0])]
            if counts is None:
                cells = ["sim failed"] * len(NEURONS)
            else:
                cells = []
                for nn, k, f in zip(NEURONS, counts, firsts):
                    x = f"{k}" + (f" ({f * 1e6:.0f})" if f is not None else "")
                    cells.append(f"**{x}**" if (k > 0) != (nn in s[3]) else x)
            L.append(f"| {sd} | {s[0]} | " + " | ".join(cells) + " |")
    L += ["", f"Run time {time.time() - t0:.0f} s."]
    out = HERE / "results" / f"{TB}{tag}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    print(f"chip yield {len(chip_ok)}/{len(seeds)}; " +
          ", ".join(f"s{s[0].split()[0]} {sum(res[(sd, s[0])][2] for sd in seeds)}/{len(seeds)}" for s in scen) +
          f"; wrote {out} ({time.time() - t0:.0f} s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated scenario numbers")
    ap.add_argument("--corner", default="tt", choices=sorted(tb.CORNERS))
    ap.add_argument("--temp", type=float, default=27)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pex", action="store_true", help="post-layout: the extracted SNN_signed macro")
    ap.add_argument("--drawn", action="store_true",
                    help="the macro's LVS reference: drawn device sizes, no parasitics")
    ap.add_argument("--mc", type=int, default=0, help="mismatch Monte Carlo: number of seeds (chips)")
    ap.add_argument("--seed0", type=int, default=1, help="first Monte Carlo seed")
    ap.add_argument("--keep", action="store_true", help="--mc: keep the run folders of passing runs too")
    ap.add_argument("--mi2-w", help="schematic or --drawn: override DPI_inh Mi2 W (2u = the old 1:1 mirror)")
    ap.add_argument("--trim", type=int, default=9, help="--pex / --drawn: trim code of the on-chip reference (0-15)")
    ap.add_argument("--dpi-size", help="schematic or --drawn: DPI M1-M4 and bias Vthr/VT_dpi replicas W/L, e.g. 2u/2.56u")
    a = ap.parse_args()
    if a.dpi_size and a.pex:
        ap.error("--dpi-size patches the schematic or --drawn netlist")
    if a.mi2_w and a.pex:
        ap.error("--mi2-w patches the schematic or --drawn netlist; the extraction has the drawn width")
    if a.pex and a.drawn:
        ap.error("--pex and --drawn are alternatives")
    global TRIM
    TRIM = a.trim
    pick = {int(x) for x in a.only.split(",")} if a.only else None
    scen = [s for s in SCENARIOS if pick is None or int(s[0].split()[0]) in pick]

    t0 = time.time()
    text = tb.netlist(HERE / f"{TB}.sch", HERE / "runs" / "_netlist").read_text()
    tb.check_connected(text, "snn_analog_signed")
    if a.pex:
        text = use_pex(text)
    if a.drawn:
        text = use_drawn(text, a.mi2_w, a.dpi_size)
    else:
        if a.mi2_w:
            text = set_mi2_w(text, a.mi2_w)
        if a.dpi_size:
            text = set_dpi_size(text, a.dpi_size)
    pfx = (f"trim{a.trim}_" if a.trim != 9 else "") + ("pex_" if a.pex else "drawn_" if a.drawn else "") + (f"mi2w{a.mi2_w}_" if a.mi2_w else "") + (f"dpi{a.dpi_size.replace('/', '-')}_" if a.dpi_size else "")
    seeds = list(range(a.seed0, a.seed0 + a.mc)) if a.mc else [None]
    cases = [tb.Case(name=f"{pfx}{'' if sd is None else f'mc{sd}_'}s{s[0].split()[0]}_{a.corner}{a.temp:g}",
                     tb=TB, corner=a.corner, temp=a.temp, seed=sd, params=params(s[1], s[2]), tags={"scen": s})
             for sd in seeds for s in scen]
    cases = tb.run_cases(cases, {TB: text}, HERE / "runs", jobs=a.jobs)

    tag = (("__pex" if a.pex else "__drawn" if a.drawn else "") + (f"__mi2w{a.mi2_w}" if a.mi2_w else "")
           + (f"__dpi{a.dpi_size.replace('/', '-')}" if a.dpi_size else "")
           + (f"__trim{a.trim}" if a.trim != 9 else "")
           + ("" if (a.corner, a.temp) == ("tt", 27) else f"__{a.corner}_{a.temp:g}")
           + (f"__mc{a.mc}" if a.mc else ""))
    if a.mc:
        report_mc(cases, a, tag, t0)
        return
    L = header(tag, a) + [
         "", "Spike counts per neuron (first spike in us). Bold = differs from the expected firing set.", "",
         "| scenario | weights | in | " + " | ".join(NEURONS) + " | result |",
         "|---|---|---|" + "---|" * len(NEURONS) + "---|"]
    n_pass = 0
    for c in cases:
        name, w, inp, must = c.tags["scen"]
        counts, firsts, ok = evaluate(c)
        if counts is None:
            cells = ["sim failed"] * len(NEURONS)
        else:
            cells = []
            for nn, k, fs in zip(NEURONS, counts, firsts):
                s = f"{k}" + (f" ({fs * 1e6:.0f})" if fs is not None else "")
                cells.append(f"**{s}**" if (k > 0) != (nn in must) else s)
        n_pass += ok
        L.append(f"| {name} | {wstr(w)} | {inp[0]}{inp[1]} | " + " | ".join(cells) +
                 f" | {'PASS' if ok else '**FAIL**'} |")
        print(f"{name}: {'PASS' if ok else 'FAIL'}  " + "  ".join(f"{nn}={x}" for nn, x in zip(NEURONS, cells)),
              flush=True)
    L += ["", f"**{n_pass} / {len(cases)} scenarios pass.** Run time {time.time() - t0:.0f} s."]
    (HERE / "results").mkdir(exist_ok=True)
    out = HERE / "results" / f"{TB}{tag}.md"
    out.write_text("\n".join(L) + "\n")
    print(f"{n_pass}/{len(cases)} pass; wrote {out} ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
