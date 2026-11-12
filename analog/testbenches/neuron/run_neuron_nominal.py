"""Run neuron_nominal_tb.sch once and keep its waveforms and log in results/.

    python3 analog/testbenches/neuron/run_neuron_nominal.py                 # schematic neuron
    python3 analog/testbenches/neuron/run_neuron_nominal.py --pex           # post-layout neuron
    python3 analog/testbenches/neuron/run_neuron_nominal.py --param p_vkdn=0.56 --tag fail_vkdn0p56

Run inside the container. The testbench checks the six simulated specs of
analog/neuron/sizing_context.txt and prints CHECK ... PASS/FAIL lines. The run
itself happens in runs/nominal_<tag>/; these files are then written to results/:

  neuron_nominal_tb[__pex][__<tag>].txt   waveforms: time, VMEM, spike
  neuron_nominal_tb[__pex][__<tag>].log   ngspice output, with a header naming the
                                          testbench, the extraction and what was changed

--param overrides a .param of the testbench (repeatable); give such runs a --tag
saying what changed, so the files say it too.
"""

import argparse
import datetime
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tbtools as tb  # noqa: E402
import tbpex  # noqa: E402

TB = "neuron_nominal_tb"
CELL = "neuron_sized"
RESULTS = HERE / "results"
RUNS = HERE / "runs"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pex", action="store_true", help="use the post-layout extraction of the neuron")
    ap.add_argument("--param", action="append", default=[], metavar="NAME=VALUE",
                    help="override a .param of the testbench, e.g. p_vkdn=0.56")
    ap.add_argument("--tag", help="name for a run with --param, e.g. fail_vkdn0p56")
    ap.add_argument("--corner", default="tt", choices=sorted(tb.CORNERS))
    ap.add_argument("--temp", type=float, default=27)
    a = ap.parse_args()
    params = dict(p.split("=", 1) for p in a.param)
    if (params or a.corner != "tt" or a.temp != 27) and not a.tag:
        raise SystemExit("give a --tag that says what was changed (it goes into the file names)")

    text = tb.netlist(HERE / f"{TB}.sch", RUNS / "netlist_nominal").read_text()
    if "IS MISSING" in text:
        raise SystemExit("netlist has a missing symbol (see the 'IS MISSING' line): check the symbol paths")
    tb.check_connected(text, CELL)
    if a.pex:
        text = tbpex.use_pex(text, CELL)

    suffix = ("__pex" if a.pex else "") + (f"__{a.tag}" if a.tag else "")
    name = f"nominal{suffix or '__sch'}"
    case = tb.Case(name=name, tb=TB, corner=a.corner, temp=a.temp, params=params)
    tb.run_case(case, {TB: text}, RUNS)

    log = case.log.replace("\r", "\n")
    for line in log.splitlines():
        if line.startswith(("CHECK", f"{TB}:")):
            print(line)
    if not case.ok:
        print(f"simulation failed, see {RUNS / name / 'ngspice.log'}")

    RESULTS.mkdir(exist_ok=True)
    stem = f"{TB}{suffix}"
    wave = RUNS / name / f"{TB}.txt"
    if wave.exists():
        shutil.copyfile(wave, RESULTS / f"{stem}.txt")
    changed = ", ".join(f"{k} = {v}" for k, v in params.items()) or "nothing"
    header = [
        f"* Source testbench: analog/testbenches/neuron/{TB}.sch, run by run_neuron_nominal.py"
        + (" --pex" if a.pex else ""),
        "* Neuron: " + ("post-layout, " + tbpex.pex_note(text) if a.pex else "schematic neuron_sized.sch"),
        f"* Changed from the testbench: {changed}",
        f"* Simulated {datetime.datetime.now():%Y-%m-%d %H:%M}, {a.corner}, {a.temp:g} C, "
        "ngspice batch mode, num_threads=1",
        f"* Waveforms (time, VMEM, spike): {stem}.txt",
        "* " + "-" * 66,
    ]
    (RESULTS / f"{stem}.log").write_text("\n".join(header) + "\n" + log)
    print(f"wrote {RESULTS / (stem + '.log')} and .txt")


if __name__ == "__main__":
    main()
