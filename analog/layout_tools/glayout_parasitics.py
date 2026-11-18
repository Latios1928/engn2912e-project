"""
Parasitic-capacitance prediction for gLayout cells, before extraction.

    from glayout_parasitics import predict_caps, report, inject_caps
    caps = predict_caps(router.shapes)            # {net: {"total": F, "gnd": F, "couple": {net: F}}}
    print(report(caps, nets=["VMEM", "spike"]))
    inject_caps("pre.spice", "pre_plus_par.spice", caps, after="x1 ")   # lumped C for a fast sim

Model (same coefficients Magic uses for PEX, read from the PDK's gf180mcuD.tech):
  * area + fringe to substrate        C = A*areacap + P*perimeter        (per metal)
  * same-layer sidewall coupling      C = L_par * sidewall / (d + offset) for d < 2 um
  * cross-layer overlap coupling      C = A_overlap * overlap(upper, lower)
Units in the tech file: aF/um^2 and aF/um. Shapes come from glayout_router.Router.shapes
(every shape tagged with its net), so the prediction is available as soon as routing is
planned, before any GDS, DRC or Magic run.

Known simplifications (why `calibrate()` exists): shielding by lower metals is ignored
(substrate C slightly high), device-internal metal not registered with the router is
missing, MIM plates are skipped (they are the device). `calibrate()` fits one factor per
net against a Magic extraction and stores it, so later predictions are corrected.
"""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from pathlib import Path

TECH = Path(os.environ.get("PDK_ROOT", "/foss/pdks")) / os.environ.get("PDK", "gf180mcuD") \
    / "libs.tech/magic/gf180mcuD.tech"
CALIB = Path(__file__).with_name("parasitic_calib.json")
METALS = ["met1", "met2", "met3", "met4", "met5"]
_MAGIC = {f"allm{i}": f"met{i}" for i in range(1, 6)}
COUPLE_RANGE = 2.0          # um: ignore same-layer coupling beyond this
SKIP_TAGS = {"C1", "C2"}    # MIM plates recorded for the short checker, not wires


def load_coeffs(tech: Path = TECH) -> dict:
    """{'area': {met: aF/um2}, 'perim': {...}, 'side': {met: (aF/um, offset)},
        'overlap': {(upper, lower): aF/um2}} from Magic's tech file."""
    c = {"area": {}, "perim": {}, "side": {}, "overlap": {}}
    for line in tech.read_text().splitlines():
        f = line.split()
        if len(f) < 4 or f[1] not in _MAGIC:
            continue
        m = _MAGIC[f[1]]
        if f[0] == "defaultareacap" and len(f) == 4:
            c["area"][m] = float(f[3])
        elif f[0] == "defaultperimeter" and len(f) == 4:
            c["perim"][m] = float(f[3])
        elif f[0] == "defaultsidewall":
            c["side"][m] = (float(f[3]), float(f[4]) if len(f) > 4 else 0.0)
        elif f[0] == "defaultoverlap" and len(f) == 6 and f[3] in _MAGIC:
            c["overlap"][(m, _MAGIC[f[3]])] = float(f[5])
    return c


def _rects(shapes):
    out = defaultdict(list)
    for layer, lst in shapes.items():
        if layer in METALS:
            out[layer] = [s for s in lst if s[5] not in SKIP_TAGS]
    return out


def predict_caps(shapes: dict, coeffs: dict | None = None, calibrated: bool = True,
                 cell: str | None = None) -> dict:
    """Per-net capacitance (farads). shapes: Router.shapes (or load_shapes()).
    calibrated: apply factors from the extraction feedback store (per cell, then global)."""
    k = coeffs or load_coeffs()
    rects = _rects(shapes)
    gnd = defaultdict(float)
    cpl = defaultdict(lambda: defaultdict(float))

    for layer, lst in rects.items():
        ca, cp = k["area"].get(layer, 0), k["perim"].get(layer, 0)
        side, off = k["side"].get(layer, (0, 0))
        for x0, y0, x1, y1, net, _t in lst:
            w, h = x1 - x0, y1 - y0
            gnd[net] += (w * h * ca + 2 * (w + h) * cp) * 1e-18
        # same-layer sidewall coupling between different nets
        for i, a in enumerate(lst):
            for b in lst[i + 1:]:
                if a[4] == b[4]:
                    continue
                ox = min(a[2], b[2]) - max(a[0], b[0])      # x overlap (>0: stacked in y)
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 0 and oy < 0:
                    d, lp = -oy, ox
                elif oy > 0 and ox < 0:
                    d, lp = -ox, oy
                else:
                    continue
                if d < COUPLE_RANGE:
                    c = lp * side / (d + off) * 1e-18
                    cpl[a[4]][b[4]] += c; cpl[b[4]][a[4]] += c

    # cross-layer overlap (upper over lower, any pair of metals)
    for (up, lo), cov in k["overlap"].items():
        for a in rects.get(up, []):
            for b in rects.get(lo, []):
                if a[4] == b[4]:
                    continue
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 0 and oy > 0:
                    c = ox * oy * cov * 1e-18
                    cpl[a[4]][b[4]] += c; cpl[b[4]][a[4]] += c

    out = {}
    for net in set(gnd) | set(cpl):
        f = factor(net, cell) if calibrated else 1.0
        g = gnd[net] * f
        cp = {n: v * f for n, v in cpl[net].items()}
        out[net] = {"gnd": g, "couple": cp, "total": g + sum(cp.values()), "factor": f}
    return out


def report(caps: dict, nets=None, top: int = 3) -> str:
    """One line per net: total, to-substrate, largest couplings."""
    nets = nets or sorted(caps, key=lambda n: -caps[n]["total"])
    lines = []
    for n in nets:
        if n not in caps:
            lines.append(f"{n:>10s}: no shapes"); continue
        c = caps[n]
        big = sorted(c["couple"].items(), key=lambda kv: -kv[1])[:top]
        cp = ", ".join(f"{m} {v * 1e15:.1f}" for m, v in big)
        lines.append(f"{n:>10s}: {c['total'] * 1e15:6.1f} fF  (sub {c['gnd'] * 1e15:5.1f}; {cp})")
    return "\n".join(lines)


def magic_net_caps(pex_spice: str | Path) -> dict:
    """Total parasitic C per named net from a Magic PEX netlist (sum of every C on it)."""
    units = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "a": 1e-18, "": 1.0}
    tot = defaultdict(float)
    for line in Path(pex_spice).read_text().splitlines():
        if line[:1] not in "Cc" or len(line.split()) < 4:
            continue
        f = line.split()
        m = re.match(r"([\d.eE+-]+)([afpnu]?)", f[3])
        c = float(m.group(1)) * units[m.group(2)]
        for node in f[1:3]:
            tot[node.split(".")[0]] += c
    return dict(tot)


# ----------------------------------------------------------------------------- feedback store
# parasitic_calib.json (version 2):
#   {"version": 2, "global": <median of cell defaults>,
#    "cells": {cell: {"factors": {net: extracted/predicted}, "default": mean,
#                     "history": [{date, gds_md5, nets, mean, err_before, err_after}, ...]}}}
# Lookup order for a net: this cell's factor -> this cell's default -> global -> 1.0.
# A new cell therefore starts from what every earlier extraction taught the predictor.

def load_store() -> dict:
    if not CALIB.exists():
        return {"version": 2, "global": 1.0, "cells": {}}
    d = json.loads(CALIB.read_text())
    if d.get("version") != 2:            # v1: one flat {net: factor} dict from the neuron
        d = {"version": 2, "global": d.get("*", 1.0),
             "cells": {"neuron": {"factors": {k: v for k, v in d.items() if k != "*"},
                                          "default": d.get("*", 1.0), "history": []}}}
    return d


def factor(net: str, cell: str | None = None, store: dict | None = None) -> float:
    st = store or _STORE_CACHE.setdefault("s", load_store())
    c = st["cells"].get(cell or "", {})
    return c.get("factors", {}).get(net, c.get("default", st.get("global", 1.0)))


_STORE_CACHE: dict = {}


def calibrate(shapes: dict, pex_spice: str | Path, cell: str, nets=None,
              gds: str | Path | None = None) -> dict:
    """Extraction -> predictor feedback. Compares the raw prediction with Magic's per-net C
    for every net named in both (Magic names only labelled nets; internal a_123# nodes get
    the cell default), stores per-net factors + history for `cell`, updates the global
    default. Returns a summary dict (also what the flow writes to signoff.json)."""
    import datetime
    import hashlib
    import statistics
    raw = predict_caps(shapes, calibrated=False)
    ext = magic_net_caps(pex_spice)
    store = load_store()
    skip = {"VSS", "VDD", "GND", "0", "VSUBS"}
    nets = nets or sorted(n for n in set(raw) & set(ext) if n not in skip and not n.startswith("a_"))
    before_f = factor  # prediction the flow used before this extraction (old store)
    rows = []
    for n in nets:
        p, e = raw.get(n, {}).get("total", 0), ext.get(n, 0)
        if p > 0 and e > 0:
            old = p * before_f(n, cell, store)
            rows.append(dict(net=n, predicted_raw_fF=p * 1e15, extracted_fF=e * 1e15,
                             factor=e / p, err_before=(old - e) / e))
    if not rows:
        return {"cell": cell, "nets": 0, "note": "no common named nets; store unchanged"}
    facs = {r["net"]: r["factor"] for r in rows}
    mean = sum(facs.values()) / len(facs)
    entry = store["cells"].setdefault(cell, {"factors": {}, "default": mean, "history": []})
    entry["factors"].update(facs)
    entry["default"] = mean
    err_before = max(abs(r["err_before"]) for r in rows)
    entry["history"].append(dict(
        date=datetime.date.today().isoformat(),
        gds_md5=hashlib.md5(Path(gds).read_bytes()).hexdigest() if gds else None,
        nets=len(rows), mean=round(mean, 4), err_before=round(err_before, 4), err_after=0.0))
    store["global"] = statistics.median(c["default"] for c in store["cells"].values())
    CALIB.write_text(json.dumps(store, indent=1))
    _STORE_CACHE.clear()
    return {"cell": cell, "nets": len(rows), "mean_factor": round(mean, 3),
            "spread": [round(min(facs.values()), 3), round(max(facs.values()), 3)],
            "max_err_before": round(err_before, 3), "global_factor": round(store["global"], 3),
            "rows": rows}


def calibration_report(summary: dict) -> str:
    if not summary.get("nets"):
        return f"calibration {summary['cell']}: {summary.get('note')}"
    lines = [f"calibration {summary['cell']}: {summary['nets']} nets, factor "
             f"{summary['mean_factor']} (range {summary['spread'][0]}..{summary['spread'][1]}), "
             f"worst error before {summary['max_err_before'] * 100:+.0f} %, global "
             f"{summary['global_factor']}"]
    for r in sorted(summary["rows"], key=lambda r: -abs(r["err_before"]))[:5]:
        lines.append(f"  {r['net']:>10s}: pred(raw) {r['predicted_raw_fF']:6.1f} fF  "
                     f"extracted {r['extracted_fF']:6.1f} fF  was {r['err_before'] * 100:+.0f} %")
    return "\n".join(lines)


def save_shapes(shapes: dict, path: str | Path):
    """Router shapes -> JSON, so signoff can calibrate without rebuilding the layout."""
    Path(path).write_text(json.dumps({k: [list(s) for s in v] for k, v in shapes.items()}))


def load_shapes(path: str | Path) -> dict:
    return {k: [tuple(s) for s in v] for k, v in json.loads(Path(path).read_text()).items()}


def inject_caps(deck_in, deck_out, caps: dict, subckt: str | None = None, after: str = "x1 ",
                ref: str = "VSS", min_f: float = 1e-16, skip=("VSS", "VDD")) -> int:
    """Copy a SPICE file, adding one lumped C (net -> ref) per predicted net.

    subckt: insert just before that subcircuit's .ends (use this for internal nets: a net
            like net1 only exists inside the cell's subckt; at top level it would be a new,
            unconnected node). Otherwise insert after the first line starting with `after`.
    Returns the number of caps added (0 = insertion point not found)."""
    lines = Path(deck_in).read_text().splitlines()
    add = [f"Cpred_{n} {n} {ref} {c['total']:.4g}" for n, c in sorted(caps.items())
           if n not in skip and c["total"] >= min_f]
    out, done, inside = [], False, False
    for line in lines:
        low = line.lower().split()
        if subckt and low[:2] == [".subckt", subckt.lower()]:
            inside = True
        if subckt and inside and not done and low[:1] == [".ends"]:
            out += add; done = True; inside = False
        out.append(line)
        if not subckt and not done and line.startswith(after):
            out += add; done = True
    Path(deck_out).write_text("\n".join(out) + "\n")
    return len(add) if done else 0
