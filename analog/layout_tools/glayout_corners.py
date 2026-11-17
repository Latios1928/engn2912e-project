"""
Process-corner prediction: characterize corners once, predict them for every layout iteration.

    from glayout_corners import characterize, predict, load_table
    table = characterize(base_deck, par_deck, "neuron_corners.json")   # once (~5 min, parallel)
    print(predict(237.3e-6, table))     # all corners from ONE typical-corner number

Model, per corner c (FET corner x MIM corner):
    P0_c   = metric of the pre-layout netlist at corner c                (no parasitics)
    P1_c   = metric of the pre-layout netlist + predicted parasitics at c
    S_c    = (P1_c - P0_c) / (P1_tt - P0_tt)     how strongly corner c amplifies parasitics
    predict:  P_c(layout) = P0_c + S_c * (P_tt(layout) - P0_tt)
P_tt(layout) comes from the fast predicted-parasitics sim (or a real PEX typical run).
The table is valid while the circuit/sizing is unchanged; layout iterations only move
P_tt(layout). Re-characterize after a schematic or sizing change.

Also here: deck building from an xschem testbench, a parallel ngspice runner, a .raw reader,
and pex_wrapper() (pin-order wrapper for a Magic-extracted cell without a .sym).
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

FET_CORNERS = ["typical", "ff", "ss", "fs", "sf"]
MIM_CORNERS = ["mimcap_typical", "mimcap_ff", "mimcap_ss"]
SIM_CAP = "cap_mim_2f0_m4m5_noshield"      # simulation model of the LVS device cap_mim_2f0fF


# ----------------------------------------------------------------------------- decks
def for_sim(lvs_ref: str | Path, out: str | Path) -> Path:
    """LVS reference -> simulatable netlist (MIM cap LVS name -> simulation model)."""
    Path(out).write_text(Path(lvs_ref).read_text().replace("cap_mim_2f0fF", SIM_CAP))
    return Path(out)


def testbench_deck(tb_spice, cell: str, include, out, save=("v(spike)", "v(VMEM)")) -> Path:
    """xschem testbench netlist -> batch deck: DUT x1 swapped to `cell` from `include`,
    .control reduced to the tran line(s) + minimal save + write (no plots, no meas).
    The DUT is assumed to be the top-level instance x1 with the same pin order."""
    txt = Path(tb_spice).read_text().splitlines()
    out = Path(out)
    raw = out.with_suffix(".raw")
    res, in_ctl, depth = [], False, 0
    for ln in txt:
        s = ln.strip()
        low = s.lower()
        depth += low.startswith(".subckt") - low.startswith(".ends")
        if depth == 0 and re.match(r"^x1\s", ln):        # top-level DUT only
            ln = re.sub(r"\S+$", cell, ln)
        if s.lower() == ".control":
            in_ctl = True
            res += [f".include {include}", ".control", "\tsave " + " ".join(save)]
            continue
        if s.lower() == ".endc":
            in_ctl = False
            res += [f"\twrite {raw}", ".endc"]
            continue
        if in_ctl:
            if s.lower().startswith("tran"):
                res.append("\t" + s)
            continue
        res.append(ln)
    out.write_text("\n".join(res) + "\n")
    return out


def corner_deck(deck, fet: str, mim: str, out, temp: float | None = None) -> Path:
    """Copy a deck with its .lib corners switched (and optional .temp)."""
    txt = Path(deck).read_text()
    txt = re.sub(r"(sm141064\.ngspice\s+)typical\b", rf"\g<1>{fet}", txt)
    txt = re.sub(r"\bmimcap_typical\b", mim, txt)
    out = Path(out)
    txt = re.sub(r"write\s+\S+", f"write {out.with_suffix('.raw')}", txt)
    if temp is not None:
        txt = txt.replace(".control", f".temp {temp}\n.control", 1)
    out.write_text(txt)
    return out


# ----------------------------------------------------------------------------- running
def run(decks, jobs: int = 8, timeout: int = 3600) -> list:
    """Run ngspice -b on each deck in parallel. Returns [(deck, ok, seconds)]."""
    import time

    def one(d):
        t = time.time()
        p = subprocess.run(["ngspice", "-b", str(d)], capture_output=True, text=True,
                           timeout=timeout)
        Path(d).with_suffix(".log").write_text(p.stdout + p.stderr)
        return d, p.returncode == 0, time.time() - t
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(one, decks))


def read_raw(fn) -> dict:
    """ngspice binary .raw -> {vector name (lowercase): np.array}."""
    b = Path(fn).read_bytes()
    i = b.index(b"Binary:\n")
    h = b[:i].decode()
    nv = int(re.search(r"No\. Variables:\s*(\d+)", h).group(1))
    npt = int(re.search(r"No\. Points:\s*(\d+)", h).group(1))
    names = [l.split()[1].lower() for l in h.split("Variables:\n")[1].strip().splitlines()]
    d = np.frombuffer(b[i + 8:i + 8 + nv * npt * 8], dtype=np.float64).reshape(npt, nv)
    return dict(zip(names, d.T))


def period(raw, node="v(spike)", th=1.65, skip=1) -> float:
    """Mean period between rising crossings of `th`, skipping the first `skip` intervals."""
    d = read_raw(raw)
    t, v = d["time"], d[node.lower()]
    up = np.where((v[:-1] < th) & (v[1:] >= th))[0]
    # interpolate crossing times
    tc = t[up] + (th - v[up]) * (t[up + 1] - t[up]) / (v[up + 1] - v[up])
    per = np.diff(tc)[skip:]
    return float(per.mean()) if len(per) else float("nan")


# ----------------------------------------------------------------------------- model
def characterize(base_deck, par_deck, out_json, fets=FET_CORNERS, mims=MIM_CORNERS,
                 metric=period, jobs: int = 8) -> dict:
    """Run every corner on the pre-layout deck (base) and on base + predicted parasitics
    (par); store P0, P1, S per corner in out_json."""
    work = Path(tempfile.mkdtemp(prefix="corners_"))
    jobs_list = []
    for f in fets:
        for m in mims:
            for tag, deck in (("p0", base_deck), ("p1", par_deck)):
                jobs_list.append((f, m, tag, corner_deck(deck, f, m, work / f"{tag}_{f}_{m}.spice")))
    results = run([j[3] for j in jobs_list], jobs=jobs)
    vals = {}
    for (f, m, tag, deck), (_, ok, sec) in zip(jobs_list, results):
        vals[(f, m, tag)] = metric(deck.with_suffix(".raw")) if ok else float("nan")
    tt = ("typical", "mimcap_typical")
    d_tt = vals[tt + ("p1",)] - vals[tt + ("p0",)]
    table = {"_model": "P_c = P0_c + S_c * (P_tt(layout) - P0_tt)", "_work": str(work),
             "corners": {}}
    for f in fets:
        for m in mims:
            p0, p1 = vals[(f, m, "p0")], vals[(f, m, "p1")]
            table["corners"][f"{f}/{m}"] = {"P0": p0, "P1": p1,
                                            "S": (p1 - p0) / d_tt if d_tt else 1.0}
    Path(out_json).write_text(json.dumps(table, indent=1))
    return table


def load_table(path) -> dict:
    return json.loads(Path(path).read_text())


def predict(p_tt_layout: float, table: dict) -> dict:
    """All corners from one typical-corner metric of the layout."""
    c = table["corners"]
    p0_tt = c["typical/mimcap_typical"]["P0"]
    return {k: v["P0"] + v["S"] * (p_tt_layout - p0_tt) for k, v in c.items()}


def report(pred: dict, unit=1e-6, name="period", ref: dict | None = None) -> str:
    lines = [f"{'corner':28s} {name} (us)" + ("   actual    error" if ref else "")]
    for k, v in sorted(pred.items(), key=lambda kv: kv[1]):
        ln = f"{k:28s} {v / unit:8.1f}"
        if ref and k in ref:
            ln += f"  {ref[k] / unit:8.1f}  {(v - ref[k]) / ref[k] * 100:+5.1f} %"
        lines.append(ln)
    lo, hi = min(pred.values()), max(pred.values())
    lines.append(f"spread {lo / unit:.1f} .. {hi / unit:.1f} us ({(hi - lo) / ((hi + lo) / 2) * 100:.0f} %)")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- PEX helper
def pex_wrapper(pex_spice, sym, out, name: str) -> Path:
    """Wrapper subckt `name` with the pin order of `sym` around a Magic-extracted cell."""
    import hashlib
    import sys
    sys.path.insert(0, str(Path(pex_spice).parent))
    from make_pex_wrapper import symbol_pins
    want = symbol_pins(Path(sym))
    pex = Path(pex_spice)
    sub = next(l for l in pex.read_text().splitlines() if l.lower().startswith(".subckt")).split()
    if sorted(map(str.lower, want)) != sorted(map(str.lower, sub[2:])):
        raise ValueError(f"pin mismatch: symbol {want} vs extracted {sub[2:]}")
    md5 = hashlib.md5(pex.read_bytes()).hexdigest()
    Path(out).write_text(f"* {name}: {pex.name} (md5 {md5}) with the pin order of {Path(sym).name}\n"
                         f".include {pex.resolve()}\n.subckt {name} {' '.join(want)}\n"
                         f"Xpex {' '.join(sub[2:])} {sub[1]}\n.ends {name}\n")
    return Path(out)
