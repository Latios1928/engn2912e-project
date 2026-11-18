"""Post-layout (PEX) option for the testbench runners.

use_pex(text, cell) takes a testbench netlist written by tbtools.netlist() and
makes every instance of the schematic subcircuit <cell> use its parasitic
extraction instead: the instance's subcircuit name becomes <cell>_pex, defined
in analog/neuron/layout/PEX/<cell>_pex_wrapper.spice (written by extract.sh in
that folder). The testbench schematic itself is not changed.

Before swapping, it checks that the extraction is current: the GDS copy in PEX/
must be identical to the block's <cell>.gds (analog/{neuron,DAC,DPI}/layout), otherwise the layout has
changed since the last extraction and this raises with the command to fix it.
"""

import filecmp
import re

from tbtools import ROOT

LAYOUT = ROOT / "analog" / "neuron" / "layout"
PEX = LAYOUT / "PEX"
# Hand-drawn block layouts (archived 2026-11-18 in <dir>/old/layout); PEX/ stays in analog/neuron/layout.
# The current block layouts are built by layout_tools/flow.py (flow/<cell>/<cell>.gds).
LAYOUT_DIRS = [ROOT / "analog" / d / "old" / "layout" for d in ("neuron", "DAC", "DPI")]


def layout_gds(cell: str):
    """The cell's current GDS (first block folder that has it)."""
    for d in LAYOUT_DIRS:
        if (d / f"{cell}.gds").exists():
            return d / f"{cell}.gds"
    raise RuntimeError(f"{cell}.gds not found in " + ", ".join(str(d) for d in LAYOUT_DIRS))
EXTRACT_CMD = ("docker exec gf180-work bash -l "
               "/foss/designs/engn2912e-project/analog/neuron/layout/PEX/extract.sh {cell}")


def check_current(cell: str):
    """Raise unless PEX/<cell>_pex_wrapper.spice exists and matches the current layout."""
    wrapper = PEX / f"{cell}_pex_wrapper.spice"
    gds_copy = PEX / f"{cell}.gds"
    fix = "Run the extraction again:\n  " + EXTRACT_CMD.format(cell=cell)
    if not wrapper.exists() or not gds_copy.exists():
        raise RuntimeError(f"no extraction of {cell} in {PEX}. {fix}")
    gds = layout_gds(cell)
    if not filecmp.cmp(gds, gds_copy, shallow=False):
        raise RuntimeError(f"{gds} has changed since it was extracted ({gds_copy} differs). {fix}")
    pex = PEX / f"{cell}_pex.spice"
    if wrapper.stat().st_mtime < pex.stat().st_mtime:
        raise RuntimeError(f"{wrapper.name} is older than {pex.name}. {fix}")
    return wrapper


def use_pex(text: str, cell: str) -> str:
    """Return the netlist with every <cell> instance replaced by its extraction."""
    wrapper = check_current(cell)
    lines, n = text.splitlines(), 0
    for i, line in enumerate(lines):
        t = line.split()
        if t and t[0][0] in "xX" and t[-1].lower() == cell.lower():
            lines[i] = line.rstrip()[: -len(t[-1])] + f"{cell}_pex"
            n += 1
    if n == 0:
        raise RuntimeError(f"no instance of {cell} in the netlist")
    # The wrapper goes after the model .lib lines, like tbtools.prepare's extra cards
    last_lib = max(i for i, line in enumerate(lines) if line.startswith(".lib"))
    lines.insert(last_lib + 1, f".include {wrapper}")
    return "\n".join(lines) + "\n"


def pex_note(text: str) -> str:
    """One line describing the extraction a netlist uses (for reports), or ''."""
    m = re.search(r"^\.include (\S+_pex_wrapper\.spice)", text, re.M)
    if not m:
        return ""
    head = open(m.group(1)).read().splitlines()[:3]
    return " ".join(h.lstrip("* ") for h in head[2:3])
