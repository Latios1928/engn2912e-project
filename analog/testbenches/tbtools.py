"""Shared helpers for the analog testbenches.

Each testbench is an xschem schematic whose .control block prints its results as
lines of the form "RES name=value". These helpers:

  1. netlist a testbench with xschem (run from the project root, so symbols such
     as analog/neuron/DPI.sym resolve the same way as in the GUI),
  2. make a copy of the netlist for one condition: process corner, temperature,
     .param overrides, and optionally device mismatch with a given seed,
  3. run ngspice in batch mode in its own folder and collect the RES values.

The device-specific runner scripts (for example dpi/run_dpi.py) decide which
conditions to run and how to report them.
"""

import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # project root
TOOLS_BIN = "/foss/tools/bin"

# Process corner -> section names in sm141064.ngspice (MOS devices, MIM caps).
# The MIM caps only have typical/ss/ff, so the skewed MOS corners use typical caps.
CORNERS = {
    "tt": ("typical", "mimcap_typical"),
    "ss": ("ss", "mimcap_ss"),
    "ff": ("ff", "mimcap_ff"),
    "sf": ("sf", "mimcap_typical"),
    "fs": ("fs", "mimcap_typical"),
}


@dataclass
class Case:
    """One simulation: a testbench under one set of conditions."""
    name: str                 # unique; also the name of the run folder
    tb: str                   # testbench name, e.g. "dpi_step_tb"
    corner: str = "tt"
    temp: float = 27
    params: dict = field(default_factory=dict)
    seed: int | None = None   # None = no mismatch; an int turns mismatch on
    tags: dict = field(default_factory=dict)  # extra columns for the report
    results: dict = field(default_factory=dict)
    ok: bool = False
    log: str = ""


def _env():
    env = dict(os.environ)
    env["PATH"] = TOOLS_BIN + os.pathsep + env.get("PATH", "")
    return env


def netlist(sch: Path, outdir: Path) -> Path:
    """Netlist an xschem schematic and return the path of the .spice file."""
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / (sch.stem + ".spice")
    cmd = ["xschem", "-q", "-x", "-r", "-n", "-s", "-o", str(outdir), "-N", out.name, str(sch)]
    subprocess.run(cmd, cwd=ROOT, env=_env(), capture_output=True, text=True, timeout=120)
    if not out.exists():
        raise RuntimeError(f"xschem did not write {out}")
    return out


def check_connected(text: str, subckt: str):
    """Raise if any instance of subckt has a pin on an unnamed net (netN).

    This happens when a symbol's pins are moved and the testbench wires no
    longer reach them; the simulation would still run, with the pin floating.
    """
    for line in text.splitlines():
        tokens = line.split()
        if tokens and tokens[0].lower().startswith("x") and tokens[-1] == subckt:
            loose = [t for t in tokens[1:-1] if re.fullmatch(r"net\d+", t)]
            if loose:
                raise RuntimeError(f"{tokens[0]} ({subckt}) has unconnected pins: {line.strip()}\n"
                                   "Check the wires to the symbol in the testbench schematic.")


def prepare(text: str, case: Case) -> str:
    """Return a copy of the netlist text set up for the case's conditions."""
    mos, mim = CORNERS[case.corner]
    text = re.sub(r"(sm141064\.ngspice\s+)typical\b", r"\g<1>" + mos, text)
    text = re.sub(r"(sm141064\.ngspice\s+)mimcap_typical\b", r"\g<1>" + mim, text)

    lines = text.splitlines()
    for name, value in case.params.items():
        pat = re.compile(rf"(\s){re.escape(name)}=\S+")
        hits = 0
        for i, line in enumerate(lines):
            if line.lower().startswith(".param"):
                lines[i], n = pat.subn(rf"\g<1>{name}={value}", line)
                hits += n
        if hits == 0:
            raise KeyError(f"{case.tb}: no .param named {name}")

    # Extra cards go after the last .lib line so they override design.ngspice
    extra = [f".temp {case.temp}"]
    if case.seed is not None:
        extra += [".param sw_stat_mismatch=1", f".options seed={case.seed}"]
    last_lib = max(i for i, line in enumerate(lines) if line.startswith(".lib"))
    lines[last_lib + 1:last_lib + 1] = extra
    return "\n".join(lines) + "\n"


def parse_results(log: str) -> dict:
    """Collect 'RES name=value' lines. Values that failed to measure become None."""
    results = {}
    for m in re.finditer(r"^RES (\w+)=(\S*)", log, re.M):
        try:
            results[m.group(1)] = float(m.group(2))
        except ValueError:
            results[m.group(1)] = None
    return results


def run_case(case: Case, netlists: dict, rundir: Path) -> Case:
    """Simulate one case in rundir/<case.name> and fill in its results."""
    d = rundir / case.name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    spice = d / (case.tb + ".spice")
    spice.write_text(prepare(netlists[case.tb], case))
    # ngspice reads ./.spiceinit instead of ~/.spiceinit: keep the user's
    # settings (ngbehavior etc.) but use one thread, since runs go in parallel
    home_init = Path.home() / ".spiceinit"
    init = home_init.read_text() if home_init.exists() else ""
    (d / ".spiceinit").write_text(init + "\nset num_threads=1\n")
    p = subprocess.run(["ngspice", "-b", spice.name], cwd=d, env=_env(),
                       capture_output=True, text=True, timeout=1800)
    case.log = p.stdout + p.stderr
    (d / "ngspice.log").write_text(case.log)
    case.results = parse_results(case.log)
    case.ok = p.returncode == 0 and bool(case.results) and "aborted" not in case.log
    return case


def run_cases(cases, netlists: dict, rundir: Path, jobs: int = 4):
    """Run many cases in parallel. Returns the same cases, filled in."""
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        return list(pool.map(lambda c: run_case(c, netlists, rundir), cases))


def read_wrdata(path: Path):
    """Read an ngspice wrdata file written with wr_singlescale and wr_vecnames.

    Returns a dict of lower-case column name -> list of floats.
    """
    rows = path.read_text().split("\n")
    names = rows[0].lower().split()
    cols = {n: [] for n in names}
    for row in rows[1:]:
        vals = row.split()
        if len(vals) == len(names):
            for n, v in zip(names, vals):
                cols[n].append(float(v))
    return cols
