"""Run ngspice in batch mode in a per-point folder."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

NGSPICE = os.environ.get("NGSPICE", "ngspice")


class SimTimeout(RuntimeError):
    pass


def run_ngspice(netlist: Path, workdir: Path, timeout: float = 120) -> str:
    """Run `ngspice -b netlist` with cwd=workdir; return stdout+stderr.

    A .spiceinit with num_threads=1 is written first: the loop runs several
    simulations in parallel, and ngspice's own threads would oversubscribe
    the CPU. The log is also saved as workdir/sim.log.
    """
    workdir = Path(workdir)
    init = workdir / ".spiceinit"
    if not init.exists():
        init.write_text("set num_threads=1\n")
    try:
        proc = subprocess.run([NGSPICE, "-b", str(netlist)], cwd=workdir,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or b"") if isinstance(e.stdout, bytes) else (e.stdout or "")
        (workdir / "sim.log").write_text(str(partial) + f"\n*** timeout after {timeout} s\n")
        raise SimTimeout(f"ngspice timed out after {timeout} s") from None
    log = proc.stdout + proc.stderr
    (workdir / "sim.log").write_text(log)
    return log
