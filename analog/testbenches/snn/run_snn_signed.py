"""Scenario runner for snn_signed_tb.sch: the 2-2-1 network with every synapse signed.

    python3 analog/testbenches/snn/run_snn_signed.py                 # all scenarios, tt 27 C
    python3 analog/testbenches/snn/run_snn_signed.py --only 3,5
    python3 analog/testbenches/snn/run_snn_signed.py --corner ss --temp 0
    python3 analog/testbenches/snn/run_snn_signed.py --pex           # post-layout macro

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

Writes results/snn_signed_tb[__pex].md (+ __<corner>_<temp> when not tt 27 C).
"""

import argparse
import filecmp
import re
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


def split_long(pex):
    """FETs longer than LMAX (bias MR_VK: 0.5/90.91 um) -> n equal series segments, same W and
    total L, so ngspice finds a model bin. Simulation copy only; the extraction is unchanged."""
    out, n_split = [], 0
    for ln in pex.splitlines():
        m = re.match(r"^(X\S+) (\S+) (\S+) (\S+) (\S+) ([np]fet_03v3) (.*)$", ln)
        lm = m and re.search(r"(?<=\s)l=([0-9.]+)u", " " + m.group(7))
        if not lm or float(lm.group(1)) * 1e-6 <= LMAX:
            out.append(ln)
            continue
        name, d, g, src, b, mod, rest = m.groups()
        L = float(lm.group(1))
        n = int(L * 1e-6 // LMAX) + 1
        rest = re.sub(r"(?<=\s)l=[0-9.]+u", f"l={L / n:.4f}u", " " + rest).strip()
        nodes = [d] + [f"{name}_s{i}" for i in range(1, n)] + [src]
        for i in range(n):
            out.append(f"{name}_{i} {nodes[i]} {g} {nodes[i + 1]} {b} {mod} {rest}")
        n_split += 1
    print(f"pex: split {n_split} FET(s) longer than {LMAX * 1e6:.0f} um into series segments")
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
    pex = split_long(pex)
    sim = PEX.with_name("SNN_signed_pex_sim.spice")
    sim.write_text(pex)
    pins = re.search(r"^\.subckt SNN_signed_flat (.*?)\n(?!\+)", pex.replace("\n+", " "), re.M | re.S).group(1)
    lines, out, depth = text.replace("\n+", " ").splitlines(), [], 0
    for ln in lines:
        t = ln.split()
        depth += bool(t) and t[0].lower() == ".subckt"
        depth -= bool(t) and t[0].lower() == ".ends"
        if depth == 0 and t and t[0] == "x1":
            out.append("x1 " + pins + " SNN_signed_flat")   # tb nets carry the macro pin names
        elif depth == 0 and t and t[0] == "xbias":
            out.append("* xbias: inside the extracted macro")
        else:
            out.append(ln)
    last_lib = max(i for i, ln in enumerate(out) if ln.startswith(".lib"))
    out.insert(last_lib + 1, f".include {sim}")
    return "\n".join(out) + "\n"


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated scenario numbers")
    ap.add_argument("--corner", default="tt", choices=sorted(tb.CORNERS))
    ap.add_argument("--temp", type=float, default=27)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pex", action="store_true", help="post-layout: the extracted SNN_signed macro")
    a = ap.parse_args()
    pick = {int(x) for x in a.only.split(",")} if a.only else None
    scen = [s for s in SCENARIOS if pick is None or int(s[0].split()[0]) in pick]

    t0 = time.time()
    text = tb.netlist(HERE / f"{TB}.sch", HERE / "runs" / "_netlist").read_text()
    tb.check_connected(text, "snn_analog_signed")
    if a.pex:
        text = use_pex(text)
    pfx = "pex_" if a.pex else ""
    cases = [tb.Case(name=f"{pfx}s{s[0].split()[0]}_{a.corner}{a.temp:g}", tb=TB, corner=a.corner, temp=a.temp,
                     params=params(s[1], s[2]), tags={"scen": s}) for s in scen]
    cases = tb.run_cases(cases, {TB: text}, HERE / "runs", jobs=a.jobs)

    tag = ("__pex" if a.pex else "") + ("" if (a.corner, a.temp) == ("tt", 27) else f"__{a.corner}_{a.temp:g}")
    L = [f"# {TB}{tag}: signed 2-2-1 network", "",
         f"Generated by `run_snn_signed.py` on {time.strftime('%Y-%m-%d %H:%M')}, {a.corner} {a.temp:g} C. "
         "Network `analog/snn/snn_analog_signed.sch` (all synapses `DAC`), biases from "
         "`bias` (Iref 100 nA), VT 1.66 V, 10 us pulses every 200 us from 50 us, 3 ms per scenario.",
         *(["", "**Post-layout:** network and bias cell replaced by the C-only Magic extraction of "
            "`layout_tools/top/SNN_signed/SNN_signed.gds` (`top_pex.sh`, C >= 0.01 fF, no wire R)."] if a.pex else []),
         "", "Spike counts per neuron (first spike in us). Bold = differs from the expected firing set.", "",
         "| scenario | weights | in | " + " | ".join(NEURONS) + " | result |",
         "|---|---|---|" + "---|" * len(NEURONS) + "---|"]
    n_pass = 0
    for c in cases:
        name, w, inp, must = c.tags["scen"]
        cells, ok = [], c.ok
        if c.ok:
            d = tb.read_wrdata(HERE / "runs" / c.name / f"{TB}.txt")
            t = d["time"]
            for i, nn in enumerate(NEURONS):
                col = d[f"v(sp{i})"]
                k = spikes(col)
                fs = first_spike(t, col)
                s = f"{k}" + (f" ({fs * 1e6:.0f})" if fs is not None else "")
                if (k > 0) != (nn in must):
                    s, ok = f"**{s}**", False
                cells.append(s)
        else:
            cells = ["sim failed"] * len(NEURONS)
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
