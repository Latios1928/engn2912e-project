"""Measured and computed metrics, and how a point is judged against the spec."""
from __future__ import annotations

import math
import re

from netlist import logical_lines, spice_num
from params import Spec

_MEAS_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")


def parse_meas(log: str, names: list[str]) -> dict[str, float | None]:
    """Pull `name = value` lines for the wanted .meas names from an ngspice log.
    A .meas that failed (e.g. no spikes) is None, not an error."""
    want = {n.lower() for n in names}
    found: dict[str, float | None] = {n: None for n in want}
    for line in log.splitlines():
        m = _MEAS_RE.match(line)
        if m and m.group(1).lower() in want and found[m.group(1).lower()] is None:
            found[m.group(1).lower()] = float(m.group(2))
    return found


def _value(tok: str, values: dict[str, float]) -> float:
    tok = tok.strip().strip("'")
    if tok.startswith("{") and tok.endswith("}"):
        ns = {k.lower(): v for k, v in values.items()}
        return float(eval(tok[1:-1].lower(), {"__builtins__": {}}, ns))
    return spice_num(tok)


def _field(line: str, names: tuple[str, ...], values: dict[str, float], default: float | None = None):
    for n in names:
        m = re.search(rf"(?<![\w/*]){n}\s*=\s*('[^']*'|\{{[^}}]*\}}|\S+)", line, re.I)
        if m:
            return _value(m.group(1), values)
    if default is None:
        raise ValueError(f"no {names} in: {line[:80]}")
    return default


def area(template_text: str, values: dict[str, float], layout_factor: float = 1.0) -> dict[str, float]:
    """a_active = Σ W·L of all transistors × layout_factor; a_cap = Σ W·L of MIM caps.
    Walks the subcircuit hierarchy from the top level, so every instance counts."""
    subckts: dict[str, list[str]] = {"": []}
    cur = ""
    for ln in logical_lines(template_text):
        s = ln.strip()
        low = s.lower()
        if low.startswith(".subckt"):
            cur = s.split()[1].lower()
            subckts[cur] = []
        elif low.startswith(".ends"):
            cur = ""
        elif s[:1] in ("x", "X"):
            subckts[cur].append(s)

    def tally(name: str, depth: int = 0) -> tuple[float, float]:
        if depth > 20:
            raise RecursionError("subcircuit nesting too deep")
        act = cap = 0.0
        for line in subckts[name]:
            toks = line.split()
            i = next((k for k, t in enumerate(toks) if "=" in t), len(toks))
            model = toks[i - 1].lower()
            mult = _field(line, ("m",), values, 1.0)
            if model in subckts:
                a, c = tally(model, depth + 1)
                act, cap = act + a * mult, cap + c * mult
            elif "fet" in model:
                act += _field(line, ("W",), values) * _field(line, ("L",), values) * mult
            elif "cap_mim" in model:
                cap += (_field(line, ("c_width", "w"), values)
                        * _field(line, ("c_length", "l"), values) * mult)
        return act, cap

    act, cap = tally("")
    return {"a_active": act * layout_factor, "a_cap": cap}


def _bad(x) -> bool:
    return x is None or (isinstance(x, float) and math.isnan(x))


def meets_spec(metrics: dict, spec: Spec) -> bool:
    return all(not _bad(metrics.get(m)) and lo <= metrics[m] <= hi for m, (lo, hi) in spec.items())


def score(metrics: dict, spec: Spec, missing_penalty: float = 10.0) -> float:
    """Distance from spec, summed over metrics: 0 = meets spec.
    Each miss is relative to the violated bound; a missing metric costs missing_penalty."""
    s = 0.0
    for m, (lo, hi) in spec.items():
        x = metrics.get(m)
        if _bad(x):
            s += missing_penalty
        elif x < lo:
            s += (lo - x) / max(abs(lo), 1e-30)
        elif x > hi:
            s += (x - hi) / max(abs(hi), 1e-30)
    return s
