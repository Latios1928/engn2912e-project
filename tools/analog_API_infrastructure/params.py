"""Load the three config files.

- params.yaml : what the optimizer may change  -> list[Param]
- spec.yaml   : targets a design must meet      -> Spec
- sim.yaml    : testbench, fixed values, analysis -> dict

All numbers are SI (m, V, A, s, F). YAML reads values like `20e-6` (no dot)
as strings, so every number goes through float().
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import yaml

Spec = dict[str, tuple[float, float]]


@dataclass(frozen=True)
class Param:
    """One tunable knob. Has the same name/lo/hi/step/fix as advisor.Param,
    so advisor.py's functions accept it unchanged."""

    name: str
    lo: float
    hi: float
    step: float
    init: float | None = None       # starting value (the current design)
    unit: str = ""
    devices: tuple[str, ...] = ()   # "subckt/INST:field" targets in the netlist

    def fix(self, x: float) -> float:
        """Clamp to [lo, hi] and snap to the step grid."""
        x = min(max(float(x), self.lo), self.hi)
        n = round((x - self.lo) / self.step)
        return float(f"{min(self.lo + n * self.step, self.hi):.12g}")


def _num(x, what: str) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{what}: expected a number, got {x!r}") from None


def _read(path: str | Path) -> dict:
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return data


def load_space(path: str | Path) -> list[Param]:
    space = []
    for name, d in _read(path).items():
        lo, hi, step = (_num(d.get(k), f"{name}.{k}") for k in ("lo", "hi", "step"))
        if not (lo < hi and step > 0):
            raise ValueError(f"{name}: need lo < hi and step > 0")
        init = d.get("init")
        devices = tuple(d.get("devices") or ())
        for dev in devices:
            if ":" not in dev:
                raise ValueError(f"{name}: device target {dev!r} must look like 'subckt/INST:field'")
        space.append(Param(
            name=name, lo=lo, hi=hi, step=step,
            init=None if init is None else _num(init, f"{name}.init"),
            unit=str(d.get("unit", "")), devices=devices,
        ))
    return space


def load_spec(path: str | Path) -> Spec:
    """{metric: (lo, hi)}; null bounds become -inf / +inf."""
    spec: Spec = {}
    for m, rng in _read(path).items():
        if m == "conditions":           # informational; fixed values live in sim.yaml
            continue
        if not (isinstance(rng, list) and len(rng) == 2):
            raise ValueError(f"spec {m}: expected [min, max]")
        lo = -math.inf if rng[0] is None else _num(rng[0], f"spec {m} min")
        hi = math.inf if rng[1] is None else _num(rng[1], f"spec {m} max")
        spec[m] = (lo, hi)
    return spec


def load_sim(path: str | Path) -> dict:
    sim = _read(path)
    if not (sim.get("testbench") or sim.get("base_netlist")):
        raise ValueError("sim.yaml: set 'testbench' (an .sch) or 'base_netlist' (a .spice)")
    sim["fixed"] = {k: _num(v, f"fixed.{k}") for k, v in (sim.get("fixed") or {}).items()}
    sim["timeout_s"] = _num(sim.get("timeout_s", 120), "timeout_s")
    sim["layout_factor"] = _num(sim.get("layout_factor", 1.0), "layout_factor")
    sim["analysis"] = sim.get("analysis") or ""
    sim["measures"] = [m.lower() for m in sim.get("measures") or []]
    sim["constraints"] = list(sim.get("constraints") or [])
    return sim
