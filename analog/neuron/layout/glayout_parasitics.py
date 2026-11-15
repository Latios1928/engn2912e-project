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


def predict_caps(shapes: dict, coeffs: dict | None = None, calibrated: bool = True) -> dict:
    """Per-net capacitance (farads). shapes: Router.shapes."""
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

    calib = json.loads(CALIB.read_text()) if (calibrated and CALIB.exists()) else {}
    out = {}
    for net in set(gnd) | set(cpl):
        f = calib.get(net, calib.get("*", 1.0))
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


def calibrate(shapes: dict, pex_spice: str | Path, nets) -> str:
    """Fit factor = extracted / predicted for each named net; store in parasitic_calib.json.
    Nets Magic leaves unnamed (internal a_123# names) get the mean factor via '*'."""
    raw = predict_caps(shapes, calibrated=False)
    ext = magic_net_caps(pex_spice)
    calib, lines = {}, []
    for n in nets:
        p, e = raw.get(n, {}).get("total", 0), ext.get(n, 0)
        if p > 0 and e > 0:
            calib[n] = e / p
            lines.append(f"{n:>10s}: predicted {p * 1e15:6.1f} fF, extracted {e * 1e15:6.1f} fF"
                         f" -> factor {e / p:.2f}")
    if calib:
        calib["*"] = sum(calib.values()) / len(calib)
    CALIB.write_text(json.dumps(calib, indent=1))
    return "\n".join(lines + [f"stored {CALIB.name} (default factor {calib.get('*', 1):.2f})"])


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
