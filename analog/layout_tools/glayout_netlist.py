"""
Schematic netlist -> flat device table for the gLayout floorplanner.

    from glayout_netlist import from_schematic
    cell = from_schematic("analog/neuron/neuron_sized.sch")
    print(cell.summary())          # devices, caps, pins, warnings
    cell.legalize()                # W < 0.5 um -> 0.5 um, L scaled to keep W/L
    cell.connect("x1_net2", "VT")  # explicit fix for a schematic wiring bug

    env -u PYTHONPATH .venv-glayout/bin/python glayout_netlist.py analog/neuron/neuron_sized.sch

What it does:
  * netlists the .sch with xschem (or reads a .spice you give it),
  * flattens subcircuit instances (x1.M3 -> device "x1_M3", internal net "x1_net1"),
  * keeps nfet_03v3 / pfet_03v3 / cap_mim_* devices with W, L, nf, m and c_width/c_length,
  * reads the top-level pin order from the "**.subckt <cell> pins" header line,
  * warns about nets that touch only gates (floating gates) and pins that connect to nothing,
    which is exactly how the VN-wire bug in spike_amplifier_sized.sch shows up.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

FET_MODELS = {"nfet_03v3": "n", "pfet_03v3": "p"}
MIN_W = 0.5          # glayout FET minimum width (um)
GRID = 0.01          # snap scaled L to this (um)


@dataclass
class Fet:
    name: str
    kind: str            # "n" / "p"
    w: float             # um, per finger (glayout convention)
    l: float
    d: str
    g: str
    s: str
    b: str
    nf: int = 1
    m: int = 1

    def row(self):
        """Tuple in the floorplanner's format."""
        return (self.name, self.kind, self.w, self.l, self.d, self.g, self.s)


@dataclass
class Cap:
    name: str
    top: str
    bot: str
    w: float             # um
    l: float


@dataclass
class Cell:
    name: str
    pins: list
    fets: list = field(default_factory=list)
    caps: list = field(default_factory=list)
    log: list = field(default_factory=list)          # legalize / connect actions

    # ------------------------------------------------------------------ queries
    @property
    def nmos(self):
        return [f for f in self.fets if f.kind == "n"]

    @property
    def pmos(self):
        return [f for f in self.fets if f.kind == "p"]

    def by_name(self, name):
        return next(f for f in self.fets if f.name == name)

    def warnings(self):
        """Floating gates and unconnected pins."""
        use = defaultdict(lambda: defaultdict(int))     # net -> terminal kind -> count
        for f in self.fets:
            for t, n in (("d", f.d), ("g", f.g), ("s", f.s), ("b", f.b)):
                use[n][t] += 1
        for c in self.caps:
            use[c.top]["c"] += 1; use[c.bot]["c"] += 1
        out = []
        for net, k in use.items():
            if net in self.pins:
                continue
            if set(k) == {"g"}:
                gates = [f.name for f in self.fets if f.g == net]
                out.append(f"floating gate: net '{net}' drives only gate(s) {gates}, "
                           f"nothing drives it")
            elif sum(k.values()) == 1:
                out.append(f"dangling net '{net}' (one connection)")
        for p in self.pins:
            if p not in use:
                out.append(f"pin '{p}' connects to nothing")
        return out

    def summary(self) -> str:
        lines = [f"{self.name}: {len(self.nmos)} NMOS, {len(self.pmos)} PMOS, "
                 f"{len(self.caps)} caps; pins: {' '.join(self.pins)}"]
        for f in self.fets:
            lines.append(f"  {f.name:8s} {f.kind} W={f.w:g} L={f.l:g} nf={f.nf} m={f.m}"
                         f"  D={f.d} G={f.g} S={f.s} B={f.b}")
        for c in self.caps:
            lines.append(f"  {c.name:8s} C {c.w:g}x{c.l:g} um  {c.top} - {c.bot}")
        lines += [f"  WARNING {w}" for w in self.warnings()]
        lines += [f"  CHANGED {x}" for x in self.log]
        return "\n".join(lines)

    # ------------------------------------------------------------------ edits
    def legalize(self, min_w: float = MIN_W):
        """Widen FETs below glayout's minimum width, scaling L to keep W/L (logged)."""
        for f in self.fets:
            if f.w < min_w:
                l_new = round(f.l * min_w / f.w / GRID) * GRID
                self.log.append(f"{f.name}: {f.w:g}/{f.l:g} -> {min_w:g}/{l_new:g} (W/L kept)")
                f.w, f.l = min_w, l_new
        return self

    def connect(self, net: str, to: str):
        """Merge `net` into `to` (fix a schematic wiring bug explicitly, logged)."""
        n = 0
        for f in self.fets:
            for t in ("d", "g", "s", "b"):
                if getattr(f, t) == net:
                    setattr(f, t, to); n += 1
        for c in self.caps:
            if c.top == net: c.top = to; n += 1
            if c.bot == net: c.bot = to; n += 1
        self.log.append(f"net {net} -> {to} ({n} terminals)")
        return self


# ----------------------------------------------------------------------------- parsing
def _num(v: str) -> float:
    """SPICE number -> float in base units ('0.28u' -> 2.8e-7, '10e-6' -> 1e-5)."""
    m = re.fullmatch(r"([-+\d.eE]+)([a-zA-Z]*)", v.strip("'\""))
    if not m:
        raise ValueError(v)
    mult = {"": 1, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3,
            "meg": 1e6}[m.group(2).lower()]
    return float(m.group(1)) * mult


def _lines(text: str):
    """Join '+' continuations, drop comments/blank lines (keep '**.subckt' header)."""
    out = []
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("+") and out:
            out[-1] += " " + s[1:]
        elif s and (not s.startswith("*") or s.lower().startswith("**.subckt")):
            out.append(s)
    return out


def _params(tokens):
    pos, kw = [], {}
    for t in tokens:
        if "=" in t:
            k, v = t.split("=", 1); kw[k.lower()] = v
        else:
            pos.append(t)
    return pos, kw


def parse_spice(text: str, top: str | None = None) -> Cell:
    lines = _lines(text)
    subckts, cur, top_lines, pins = {}, None, [], []
    globals_ = {"0", "gnd"} | {g.lower() for ln in lines if ln.lower().startswith(".global")
                               for g in ln.split()[1:]}
    for ln in lines:
        low = ln.lower()
        if low.startswith("**.subckt"):
            f = ln.split(); top = top or f[1]
            pins = [p for tok in f[2:] for p in tok.split(",")]     # xschem bus: a[1],a[0]
            continue
        if low.startswith(".subckt"):
            f = ln.split(); cur = f[1]; subckts[cur] = {"ports": f[2:], "body": []}
            continue
        if low.startswith(".ends"):
            cur = None; continue
        if low.startswith("."):
            continue
        (subckts[cur]["body"] if cur else top_lines).append(ln)

    cell = Cell(top or "top", pins)

    def walk(body, prefix, netmap):
        def net(n):
            if n.lower() in globals_:          # .GLOBAL nets (GND) are never prefixed
                return n
            return netmap.get(n, prefix + n if prefix else n)
        for ln in body:
            if not ln[0] in "Xx":
                continue
            pos, kw = _params(re.sub(r"'[^']*'", "''", ln).split())   # drop quoted exprs
            inst, model = pos[0], pos[-1]
            name = inst[1:]                       # XM1 -> M1 (devices)
            if model in FET_MODELS:
                d, g, s, b = (net(x) for x in pos[1:5])
                cell.fets.append(Fet(prefix + name, FET_MODELS[model],
                                     round(_num(kw["w"]) * 1e6 / int(_num(kw.get("nf", "1"))), 4),
                                     round(_num(kw["l"]) * 1e6, 4), d, g, s, b,
                                     int(_num(kw.get("nf", "1"))), int(_num(kw.get("m", "1")))))
            elif model.startswith("cap_mim"):
                cell.caps.append(Cap(prefix + name, net(pos[1]), net(pos[2]),
                                     round(_num(kw["c_width"]) * 1e6, 4),
                                     round(_num(kw["c_length"]) * 1e6, 4)))
            elif model in subckts:
                sub = subckts[model]
                actual = [net(x) for x in pos[1:-1]]
                walk(sub["body"], f"{prefix}{inst.lower()}_",   # x1 -> x1_M3, x1_net1
                     dict(zip(sub["ports"], actual)))
            else:
                raise ValueError(f"unknown model {model!r} in: {ln}")

    walk(top_lines, "", {})
    return cell


def netlist_schematic(sch: str | Path) -> str:
    """Run xschem's netlister on a .sch; returns the spice text."""
    sch = Path(sch).resolve()
    out = Path(tempfile.mkdtemp())
    rc = sch.parent / "xschemrc"
    cmd = ["xschem", "-q", "-x", "-n", "-s", "-o", str(out)] + \
          (["--rcfile", str(rc)] if rc.exists() else []) + [str(sch)]
    subprocess.run(cmd, cwd=sch.parent, capture_output=True, text=True, timeout=120)
    f = out / (sch.stem + ".spice")
    if not f.exists():
        raise RuntimeError(f"xschem wrote no netlist for {sch}")
    return f.read_text()


def from_schematic(path: str | Path) -> Cell:
    """.sch (netlisted with xschem) or .spice -> flat Cell."""
    p = Path(path)
    text = netlist_schematic(p) if p.suffix == ".sch" else p.read_text()
    return parse_spice(text)


if __name__ == "__main__":
    c = from_schematic(sys.argv[1])
    if "--legalize" in sys.argv:
        c.legalize()
    print(c.summary())
