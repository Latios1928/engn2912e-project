"""Turn an xschem netlist into a reusable template, and write params.spice.

The template is the xschem netlist with:
- the interactive .control ... .endc block and any old analyses removed;
- every tuned/fixed name removed from the netlist's own .param lines;
- device fields named in params.yaml replaced by {PARAM} (e.g. c_width={W_C2});
- `.include params.spice` at the top and the analysis block from sim.yaml
  at the end.

Between runs only params.spice changes, so xschem runs once per loop.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from params import Param

_SUFFIX = {"t": 1e12, "g": 1e9, "meg": 1e6, "k": 1e3, "m": 1e-3,
           "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15, "a": 1e-18}
_NUM_RE = re.compile(r"^([-+]?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?)(meg|[tgkmunpfa])?[a-z]*$", re.I)
_ASSIGN_RE = re.compile(r"([A-Za-z_]\w*)\s*=\s*('[^']*'|\{[^}]*\}|\S+)")
_ANALYSES = (".tran", ".meas", ".measure", ".op", ".dc", ".ac", ".noise", ".print", ".plot")


def spice_num(s: str) -> float:
    """'0.22u' -> 2.2e-07, '5meg' -> 5e6, '20.52e-6' -> 2.052e-05."""
    m = _NUM_RE.match(s.strip())
    if not m:
        raise ValueError(f"not a SPICE number: {s!r}")
    return float(m.group(1)) * _SUFFIX.get((m.group(2) or "").lower(), 1.0)


def logical_lines(text: str) -> list[str]:
    """Join '+' continuation lines onto the line they continue."""
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("+") and out:
            out[-1] += " " + line[1:].strip()
        else:
            out.append(line)
    return out


def generate_base_netlist(testbench: Path, out_dir: Path, repo_root: Path) -> Path:
    """Netlist an .sch with xschem in batch mode (run from the repo root so
    relative symbol paths like analog/neuron/x.sym resolve)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["xschem", "-n", "-s", "-q", "-x", "-o", str(out_dir), str(testbench)]
    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, timeout=120)
    path = out_dir / (Path(testbench).stem + ".spice")
    if not path.exists():
        raise RuntimeError(f"xschem did not write {path}\n{proc.stdout}\n{proc.stderr}")
    return path


def _parse_target(t: str) -> tuple[str, str, str]:
    """'neuron_5khz/XC2:c_width' -> ('neuron_5khz', 'xc2', 'c_width'); no '/' = top level."""
    where, field = t.rsplit(":", 1)
    subckt, _, inst = where.rpartition("/")
    return subckt.lower(), inst.lower(), field


def make_template(base_text: str, space: list[Param], fixed_names: list[str], analysis: str) -> str:
    override = {n.lower() for n in fixed_names} | {p.name.lower() for p in space}

    targets: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for p in space:
        for t in p.devices:
            sub, inst, field = _parse_target(t)
            targets.setdefault((sub, inst), []).append((field, p.name))
    applied: set[tuple[str, str, str]] = set()

    lines = logical_lines(base_text)
    out = lines[:1] + [".include params.spice"]   # line 1 is the SPICE title line
    in_control, subckt = False, ""
    for ln in lines[1:]:
        s = ln.strip()
        low = s.lower()
        if low.startswith(".control"):
            in_control = True
            continue
        if in_control:
            in_control = not low.startswith(".endc")
            continue
        if low == ".end" or (low.startswith(_ANALYSES) and not subckt):
            continue
        if low.startswith(".subckt"):
            subckt = s.split()[1].lower()
        elif low.startswith(".ends"):
            subckt = ""
        elif low.startswith(".param"):
            kept = [f"{k}={v}" for k, v in _ASSIGN_RE.findall(s[6:]) if k.lower() not in override]
            if not kept:
                continue
            ln = ".param " + " ".join(kept)
        elif s and s[0] not in "*.":
            inst = s.split()[0].lower()
            for field, pname in targets.get((subckt, inst), []):
                ln, n = re.subn(rf"(?<![\w/*]){re.escape(field)}\s*=\s*('[^']*'|\{{[^}}]*\}}|\S+)",
                                f"{field}={{{pname}}}", ln, flags=re.I)
                if n:
                    applied.add((subckt, inst, field))
        out.append(ln)

    missing = [f"{s or '(top)'}/{i}:{f}" for (s, i), fl in targets.items()
               for f, _ in fl if (s, i, f) not in applied]
    if missing:
        raise ValueError(f"device targets not found in netlist: {missing}")
    out += ["", "* ---- analysis (from sim.yaml) ----", analysis.strip(), ".end", ""]
    return "\n".join(out)


def write_params(values: dict[str, float], path: Path) -> None:
    lines = ["* written by netlist.write_params; do not edit"]
    lines += [f".param {k}={v:.10g}" for k, v in values.items()]
    Path(path).write_text("\n".join(lines) + "\n")
