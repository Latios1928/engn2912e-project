"""Shared parts of the DPI runners (run_dpi_load.py, run_dpi_pulse.py).

- BIASES: the DPI bias presets used in the project (--bias)
- prepare_netlist(): netlist a testbench, check it, swap the excitatory cell (--cell)
  and the post-layout extraction (--pex)
- sch(): writes the small xschem testbenches of this folder

The testbenches hold an excitatory synapse (instance x1, DPI_sized by default) and an
inhibitory one (x2, DPI_inh, which contains a DPI_sized). Biases: Vthr is an absolute
gate voltage; vtau is the source-gate voltage of the pFET tau device, so VT = VDD - vtau.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402
import tbpex  # noqa: E402

# name: (Vthr, vtau excitatory, vtau inhibitory, where it comes from)
BIASES = {
    "output": (2.785, 0.5096, 0.5096, "XOR output layer (testbenches/xor/README.md)"),
    "hidden": (2.5, 0.6225, 0.6225, "XOR hidden layer (testbenches/xor/README.md)"),
    "relay": (2.4, 0.72, 0.72, "XOR input relays (testbenches/xor/README.md)"),
    "chain": (2.909, 0.40, 0.40, "neuron/DACs-DPI-neuron.sch (one DPI bias set for the 2-2-1 network on main)"),
}
CELLS = ("DPI_sized", "DPI")
IUNIT = 15e-9  # DAC unit current


def bias_params(name):
    vthr, vtau, vtau_i, _ = BIASES[name]
    return {"p_vthr": f"{vthr:g}", "p_vtau": f"{vtau:g}", "p_vtau_i": f"{vtau_i:g}"}


def _subckt(text, name):
    m = re.search(rf"^\.subckt {re.escape(name)} .*?^\.ends\b.*?$", text, re.M | re.S | re.I)
    return m.group(0) if m else None


def use_cell(text, cell, rundir):
    """Make the excitatory instance x1 use `cell` (DPI_sized or DPI; same pins)."""
    if cell == "DPI_sized":
        return text
    if _subckt(text, cell) is None:
        # Take the cell's subcircuit from a testbench that uses it (dpi_step_tb uses DPI)
        donor = tb.netlist(HERE / "dpi_step_tb.sch", rundir / "donor").read_text()
        body = _subckt(donor, cell)
        if body is None:
            raise RuntimeError(f"no .subckt {cell} in the dpi_step_tb netlist")
        text = text.replace("\n.end\n", f"\n{body}\n.end\n") if "\n.end\n" in text else text + "\n" + body + "\n"
    lines, n, inside = text.splitlines(), 0, False
    for i, line in enumerate(lines):
        t = line.split()
        if t and t[0].lower() == ".subckt":
            inside = True
        elif t and t[0].lower() == ".ends":
            inside = False
        # only the testbench's own x1, not the x1 inside DPI_inh's subcircuit
        if not inside and t and t[0].lower() == "x1" and t[-1] == "DPI_sized":
            lines[i] = line.rstrip()[: -len("DPI_sized")] + cell
            n += 1
    if n != 1:
        raise RuntimeError("expected one top-level x1 DPI_sized instance")
    return "\n".join(lines) + "\n"


def prepare_netlist(sch, rundir, cell, pex, check=("DPI_sized", "DPI_inh")):
    """Netlist, check the pins, swap the cell, optionally use the extractions.

    Returns (netlist text, note on the extraction for the report)."""
    text = tb.netlist(sch, rundir).read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    for c in check:
        tb.check_connected(text, c)
    text = use_cell(text, cell, rundir)
    note = ""
    if pex:
        # Every cell of the synapse that has a symbol of its own: the excitatory DPI,
        # the inhibitory DPI and any DAC_signed in the testbench. tbpex stops with the command
        # to run when a cell has no (current) extraction.
        cells = [cell, "DPI_inh"] + (["DAC_signed"] if re.search(r"^x\S* .* DAC_signed$", text, re.M) else [])
        notes = []
        for c in cells:
            text = tbpex.use_pex(text, c)
            notes.append(f"{c}: {tbpex.pex_note(text) or 'extracted'}")
        note = "; ".join(notes)
    return text, note


# --- schematic writer -------------------------------------------------------------

def sch(title, instances, blocks):
    """xschem schematic text: a title, symbol instances with a label on every pin, code blocks.

    instances: (symbol, x, y, [(pin_x, pin_y, side, label), ...]); side 'l' or 'r'.
    blocks: (name, x, y, text, tcleval)."""
    out = ["v {xschem version=3.4.8RC file_version=1.3}", "G {}", "K {}", "V {}", "S {}", "F {}", "E {}",
           "T {" + title.replace("{", "(").replace("}", ")") + "} -900 -700 0 0 0.3 0.3 {}"]
    k = 0
    for sym, x, y, pins in instances:
        name = f"x{len([1 for o in out if o.startswith('C {') and 'name=x' in o]) + 1}"
        out.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")
        for px, py, side, lab in pins:
            k += 1
            flip = "0 1" if side == "r" else "0 0"
            out.append(f"C {{lab_pin.sym}} {x + px} {y + py} {flip} {{name=l{k} sig_type=std_logic lab={lab}}}")
    for name, x, y, text, tcl in blocks:
        esc = text.replace("{", "\\{").replace("}", "\\}")
        fmt = 'format="tcleval( @value )"\n' if tcl else ""
        top = "true" if tcl else "false"
        out.append(f"C {{devices/code_shown.sym}} {x} {y} 0 0 {{name={name} only_toplevel={top}\n{fmt}value=\"\n{esc}\n\"}}")
    return "\n".join(out) + "\n"


MODELS = """.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical"""

# Pin positions (symbol coordinates) of DPI_sized / DPI and DPI_inh
DPI_PINS = lambda vt, isum, out: [(-150, -20, "l", "Vthr"), (-150, 0, "l", vt), (-150, 20, "l", isum),
                                  (150, -20, "r", "VDD"), (150, 0, "r", out)]


# --- running and reloading ----------------------------------------------------------

import json  # noqa: E402

RUNS = HERE / "runs"
RESULTS = HERE / "results"
CORNERS = [(c, t) for c in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]


def run_and_save(cases, netlists, jobs):
    """Run the cases (runs/<name>/) and save their conditions next to the logs."""
    done = tb.run_cases(cases, netlists, RUNS, jobs=jobs)
    for c in done:
        d = RUNS / c.name
        if d.exists():
            (d / "case.json").write_text(json.dumps({"tb": c.tb, "tags": c.tags, "corner": c.corner,
                                                     "temp": c.temp, "seed": c.seed, "params": c.params}))
    return done


def load_runs(prefix):
    """Every saved run whose folder name starts with prefix (for reports and --report-only)."""
    done = []
    for j in sorted(RUNS.glob(f"{prefix}*/case.json")):
        info = json.loads(j.read_text())
        c = tb.Case(name=j.parent.name, tb=info["tb"], corner=info["corner"], temp=info["temp"],
                    seed=info["seed"], params=info["params"], tags=info["tags"])
        log = j.parent / "ngspice.log"
        c.log = log.read_text() if log.exists() else ""
        c.results = tb.parse_results(c.log)
        c.ok = bool(c.results) and "aborted" not in c.log and "singular" not in c.log.lower()
        done.append(c)
    return done


def stem(tbname, cell, bias, pex, default_bias="output"):
    """Result file name: <tb>[__<cell>][__<bias>][__pex] (defaults DPI_sized, output left out)."""
    return (tbname + ("" if cell == "DPI_sized" else f"__{cell}") + ("" if bias == default_bias else f"__{bias}")
            + ("__pex" if pex else ""))


def style(ax, ink2="#52514e", grid="#e4e3df", surf="#fcfcfb"):
    ax.set_facecolor(surf)
    ax.grid(True, color=grid, lw=0.8)
    for sp in ax.spines.values():
        sp.set_color(grid)
    ax.tick_params(colors=ink2)


INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
