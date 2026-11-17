"""
Token-efficient helpers for driving gLayout (GF180) from an AI assistant.

Every helper returns a short, plain-text-friendly result instead of raw gdsfactory
objects or long tracebacks, so the assistant reads tens of tokens instead of thousands.

    from glayout_helpers import fet, pin, route, place, ports_brief, describe, rules, drc

Run scripts with:
    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python <script>.py
"""
from __future__ import annotations

import os
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from glayout import nmos, pmos, c_route, L_route, straight_route
from glayout import evaluate_bbox

# glayout's FET primitive cannot fit a source/drain contact row below this width (µm).
MIN_FET_WIDTH = 0.5

# Project defaults: no per-device DNW, tie ring or substrate ring (added later, shared).
_FET_DEFAULTS = dict(with_tie=False, with_substrate_tap=False)

_SIDES = {90.0: "N", 0.0: "E", 270.0: "S", 180.0: "W"}
_TERM_ALIASES = {"d": "drain", "s": "source", "g": "gate"}


# --------------------------------------------------------------------------- devices
def fet(pdk, kind: str, w: float, l: float, fingers: int = 1, **kw):
    """Build an NMOS/PMOS with project defaults and an early, one-line width check.

    kind: "n" or "p". w is the width PER FINGER (glayout convention): total W = w * fingers,
    and LVS extracts one device of width w per finger.
    Extra kwargs go to glayout's nmos()/pmos() and override defaults.
    NMOS default: no deep n-well (use one shared DNW around the group instead).
    """
    if w < MIN_FET_WIDTH:
        raise ValueError(
            f"fet: W/finger={w:g}um < {MIN_FET_WIDTH}um (glayout minimum). "
            f"Use W>={MIN_FET_WIDTH:g}; scale L to keep W/L."
        )
    opts = {**_FET_DEFAULTS, **kw}
    if kind.lower().startswith("n"):
        opts.setdefault("with_dnwell", False)
        return nmos(pdk, width=w, length=l, fingers=fingers, **opts)
    if kind.lower().startswith("p"):
        return pmos(pdk, width=w, length=l, fingers=fingers, **opts)
    raise ValueError(f"fet: kind must be 'n' or 'p', got {kind!r}")


# --------------------------------------------------------------------------- ports
def pin(dev, term: str, side: str, mult: int = 0):
    """Port of a FET terminal: pin(m1, "d", "N") -> multiplier_0_drain_N."""
    term = _TERM_ALIASES.get(term.lower(), term.lower())
    name = f"multiplier_{mult}_{term}_{side.upper()}"
    try:
        return dev.ports[name]
    except KeyError:
        raise KeyError(f"pin: no port {name!r}. Try ports_brief(dev, {term!r}).") from None


def ports_brief(comp, pattern: str | None = None, limit: int = 40) -> str:
    """Group port names by stem and list their sides on one line each.

    A glayout FET has ~800 ports; this collapses them to a few lines, e.g.
        multiplier_0_drain: N E S W  (met2, w=3.06)
    pattern: optional regex filter on the stem (e.g. "drain|gate").
    """
    groups: dict[str, list] = defaultdict(list)
    for name, p in comp.ports.items():
        stem, _, side = name.rpartition("_")
        if side not in "NESW" or not stem:
            stem, side = name, "?"
        if pattern and not re.search(pattern, stem):
            continue
        groups[stem].append((side, p))
    lines = []
    for stem in sorted(groups):
        sides = "".join(sorted({s for s, _ in groups[stem]}, key="NESW?".index))
        p = groups[stem][0][1]
        widths = "/".join(f"{w:g}" for w in sorted({round(q.width, 3) for _, q in groups[stem]}))
        lines.append(f"{stem}: {' '.join(sides)}  ({_glayer(p)}, w={widths})")
    extra = len(lines) - limit
    out = "\n".join(lines[:limit])
    return out + (f"\n... {extra} more stems (pass pattern=)" if extra > 0 else "")


def _glayer(port) -> str:
    try:
        from glayout import gf180
        return gf180.layer_to_glayer(port.layer)
    except Exception:
        return str(port.layer)


def _side(port) -> str:
    return _SIDES.get(round(port.orientation % 360, 1), f"{port.orientation:g}deg")


# --------------------------------------------------------------------------- routing
def route(pdk, top, a, b, width: float | None = 0.5, layer: str | None = None, **kw):
    """Connect two ports, choosing straight/L/C route from their orientations.

    same direction       -> c_route   (U-shape)
    facing, aligned      -> straight_route
    perpendicular        -> L_route
    width: metal width for every segment (None = glayout default = port width).
    layer: metal for the connecting segment (cglayer / glayer2 / hglayer).
    Returns the route reference, already added to `top`.
    """
    sa, sb = _side(a), _side(b)
    horiz = {"E", "W"}
    if sa == sb:
        args = dict(width1=width, width2=width, cwidth=width, cglayer=layer)
        fn = c_route
    elif {sa, sb} in ({"N", "S"}, {"E", "W"}):
        dx, dy = abs(a.center[0] - b.center[0]), abs(a.center[1] - b.center[1])
        aligned = dx < 1e-3 if sa in ("N", "S") else dy < 1e-3
        if not aligned:
            raise ValueError(
                f"route: {sa}/{sb} ports face each other but are offset by "
                f"{dx if sa in ('N', 'S') else dy:.3f}um. Align them (movex/movey) or "
                f"use the same side on both (-> c_route)."
            )
        args = dict(width=width, glayer2=layer)
        fn = straight_route
    else:
        # L_route: edge1 vertical, edge2 horizontal is handled internally by glayout
        args = dict(vwidth=width, hwidth=width, hglayer=layer)
        fn = L_route
    args = {k: v for k, v in args.items() if v is not None}
    args.update(kw)
    try:
        return top << fn(pdk, a, b, **args)
    except Exception as e:
        raise RuntimeError(f"route[{fn.__name__} {sa}->{sb}]: {e}") from None


# --------------------------------------------------------------------------- placement
def place(dev, ref=None, side: str = "E", gap: float = 0.3, align: str = "center"):
    """Place `dev` next to `ref` with an edge-to-edge gap (not center-to-center).

    side: N/E/S/W of ref. align: "center", or "min"/"max" to line up edges along
    the other axis (left/bottom or right/top). With ref=None, centers dev at origin.
    """
    if ref is None:
        dev.move((-dev.center[0], -dev.center[1]))
        return dev
    side = side.upper()
    if side == "E":
        dx, dy = ref.xmax + gap - dev.xmin, 0
    elif side == "W":
        dx, dy = ref.xmin - gap - dev.xmax, 0
    elif side == "N":
        dx, dy = 0, ref.ymax + gap - dev.ymin
    elif side == "S":
        dx, dy = 0, ref.ymin - gap - dev.ymax
    else:
        raise ValueError(f"place: side must be N/E/S/W, got {side!r}")
    if side in ("E", "W"):
        dy = {"center": ref.center[1] - dev.center[1],
              "min": ref.ymin - dev.ymin, "max": ref.ymax - dev.ymax}[align]
    else:
        dx = {"center": ref.center[0] - dev.center[0],
              "min": ref.xmin - dev.xmin, "max": ref.xmax - dev.xmax}[align]
    dev.move((dx, dy))
    return dev


# --------------------------------------------------------------------------- inspection
def describe(top, names: dict | None = None) -> str:
    """One line per reference: name, center, size. Plus the cell bbox.

    names: optional {"M1": m1, ...} so lines use your device names, not cell hashes.
    """
    label = {id(r): n for n, r in (names or {}).items()}
    w, h = evaluate_bbox(top)
    lines = [f"{top.name}: {w:.2f} x {h:.2f} um, {len(top.references)} refs"]
    for r in top.references:
        n = label.get(id(r))
        if n is None and names:
            continue  # skip routes when the caller named the devices
        rw, rh = evaluate_bbox(r)
        lines.append(f"  {n or r.parent.name[:24]}: c=({r.center[0]:.2f},{r.center[1]:.2f})"
                     f" size={rw:.2f}x{rh:.2f}")
    return "\n".join(lines)


def rules(pdk, *layers: str) -> str:
    """Compact design-rule lookup. rules(pdk, "met2", "nwell", ("dnwell","nwell"))."""
    out = []
    for item in layers:
        pair = item if isinstance(item, tuple) else (item,)
        try:
            r = pdk.get_grule(*pair)
            txt = ", ".join(f"{k.replace('min_', '')}={v:g}" for k, v in r.items()) or "none"
        except Exception:
            txt = "no rule in glayout table (check KLayout DRC)"
        out.append(f"{'/'.join(pair)}: {txt}")
    return "\n".join(out)


# --------------------------------------------------------------------------- DRC
def drc(gds: str | Path, topcell: str, run_dir: str | Path = "/tmp/glayout_drc",
        variant: str = "D", max_rules: int = 15, timeout: int = 900) -> str:
    """Run the GF180 KLayout DRC deck and return a short per-rule violation summary.

    Uses the same deck/flags as the run_*_checks.sh scripts. Slow (minutes).
    """
    tech = Path(os.environ.get("PDK_ROOT", "/foss/pdks")) / os.environ.get("PDK", "gf180mcuD") \
        / "libs.tech/klayout/tech/drc/run_drc.py"
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["python3", str(tech), f"--path={gds}", f"--variant={variant}",
           f"--topcell={topcell}", f"--run_dir={run_dir}", "--mp=4"]
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return f"drc: timed out after {timeout}s"
    counts: dict[str, int] = defaultdict(int)
    for f in run_dir.glob("*.lyrdb"):
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            continue
        for item in root.iter("item"):
            cat = (item.findtext("category") or "?").strip("'\"")
            counts[cat] += 1
    if not counts:
        return "drc: clean (no violations found)"
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    lines = [f"drc: {sum(counts.values())} violations in {len(counts)} rules"]
    lines += [f"  {rule}: {n}" for rule, n in ranked[:max_rules]]
    if len(ranked) > max_rules:
        lines.append(f"  ... {len(ranked) - max_rules} more rules")
    return "\n".join(lines)
