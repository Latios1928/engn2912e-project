"""Stack correction: current of S unit devices in series (gate on the master diode, output at the
typical pin voltage) times S, divided by one unit's current in the diode. Run in the container:
    python3 analog/bias/sim/stack_corr.py                  # for the unit sizes in bias_gen.py
    python3 analog/bias/sim/stack_corr.py --w 2 --l 4      # for another unit size
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bias_gen as bg  # noqa: E402

RUNS = HERE / "runs"
PDK = "/foss/pdks/gf180mcuD/libs.tech/ngspice"
SS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24]


def deck(typ, w, l):
    n = typ == "n"
    model, rail = ("nfet_03v3", "0") if n else ("pfet_03v3", "VDD")
    units = bg.P1 if n else bg.PM
    L = ["* stack corr", f".include {PDK}/design.ngspice", f".lib {PDK}/sm141064.ngspice typical",
         "Vdd VDD 0 3.3",
         # master diode as in bias_gen: nFET P1 units / pFET PM units at I0
         (f"I0 VDD g {bg.I0:g}" if n else f"I0 g 0 {bg.I0:g}"),
         f"XM g g {rail} {rail} {model} L={l}u W={w}u nf=1 m={units}"]
    for s in SS:
        nodes = [f"o{s}"] + [f"s{s}_{k}" for k in range(1, s)] + [rail]
        L += [f"X{s}_{k} {nodes[k]} g {nodes[k + 1]} {rail} {model} L={l}u W={w}u nf=1" for k in range(s)]
        L.append(f"Vo{s} o{s} 0 {2.5 if n else 0.7}")
    unit = bg.I0 / units
    L += [".control", "op"] + [f"let c{s}=abs(i(Vo{s}))*{s}/{unit:g}" for s in SS]
    L += ["echo RES " + " ".join(f"c{s}=$&c{s}" for s in SS), "quit", ".endc", ".end"]
    return "\n".join(L) + "\n"


def measure(typ, w, l, runs=None):
    """{S: factor} for unit devices W/L (um) of type 'n' or 'p'."""
    runs = Path(runs or RUNS)
    runs.mkdir(parents=True, exist_ok=True)
    f = runs / f"stack_{typ}.spice"
    f.write_text(deck(typ, w, l))
    log = subprocess.run(["ngspice", "-b", f.name], cwd=runs, capture_output=True, text=True).stdout
    m = re.search(r"^RES (.*)$", log, re.M)
    if not m:
        raise RuntimeError(f"stack_corr: no results, see {f}")
    return {int(s): float(v) for s, v in re.findall(r"c(\d+)=(\S+)", m.group(1))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", type=float)
    ap.add_argument("--l", type=float)
    a = ap.parse_args()
    for typ, (w, l) in (("n", bg.UNIT_N), ("p", bg.UNIT_P)):
        w, l = a.w or w, a.l or l
        vals = measure(typ, w, l)
        print(f'STACK_{typ.upper()} = {{' + ", ".join(f"{s}: {v:.4f}" for s, v in vals.items()) + "}")
