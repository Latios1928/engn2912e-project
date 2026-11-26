# analog/testbenches/

Characterization of the analog cells and of the network. Each block has a folder with xschem
testbenches (`*_tb.sch`) and runner scripts (`run_*.py`) that netlist the same schematics, run
them across sweeps, process corners, temperature, supply and mismatch, and write reports to the
folder's `results/` (`.md` / `.csv` / `.png`; post-layout runs end in `__pex`).

| Folder | Device under test | Runners |
|---|---|---|
| `dpi/` | `analog/DPI/DPI.sch`, with an ideal current sink in place of the DAC | `run_dpi.py` |
| `neuron/` | `analog/neuron/neuron.sch`, targets in `analog/neuron/sizing_context.txt` | `run_neuron_nominal.py`, `_rate.py`, `_pulse.py`, `_robust.py`, `_ibias.py` |
| `bias/` | `analog/neuron/bias.sch` | `bias_design.py` (sizing), `run_bias_cell.py` |
| `snn/` | the whole network, `analog/snn/snn_analog_signed.sch` + `bias` | `run_snn_signed.py` |

`tbtools.py` holds the shared parts: netlisting, corner / temperature / parameter substitution,
running ngspice and reading results. `tbpex.py` adds the post-layout option `--pex` (currently
broken for the cell runners: see TODO in the [main README](../../README.md#analog)).

## Running

Start xschem from the project root or from `analog/neuron`, `analog/DAC` or `analog/DPI`: their
`xschemrc` files source the root one, which puts every cell folder on the symbol path. In the GUI,
*Netlist* then *Simulate*; each testbench plots its waveforms and prints `RES name=value` lines.

Batch runs, from any directory, inside the container:

```sh
python3 analog/testbenches/dpi/run_dpi.py                    # all suites, about 10 s
python3 analog/testbenches/dpi/run_dpi.py --only nominal,pvt # selected suites
python3 analog/testbenches/dpi/run_dpi.py --mc 500 --jobs 8  # more mismatch samples

python3 analog/testbenches/neuron/run_neuron_nominal.py      # one run, specs PASS/FAIL, about 11 s
python3 analog/testbenches/neuron/run_neuron_nominal.py --param p_vkdn=0.56 --tag fail_vkdn0p56
python3 analog/testbenches/neuron/run_neuron_rate.py         # firing rate vs input current, about 3 min
python3 analog/testbenches/neuron/run_neuron_pulse.py        # pulses to fire, leak, refractory loss
python3 analog/testbenches/neuron/run_neuron_robust.py       # PVT, supply, bias drift, mismatch; about 20 min

python3 analog/testbenches/bias/run_bias_cell.py             # bias outputs over PVT, cell vs fixed voltages, about 2 min

python3 analog/testbenches/snn/run_snn_signed.py             # all 8 network scenarios, tt 27 C
python3 analog/testbenches/snn/run_snn_signed.py --pex       # post-layout macro (top_pex.sh extraction)
python3 analog/testbenches/snn/run_snn_signed.py --corner ss --temp 0
python3 analog/testbenches/snn/run_snn_signed.py --mc 50     # mismatch, 50 chips
```

Every runner takes `--help`. Common options: `--only <suites>`, `--quick`, `--mc N`, `--jobs N`,
`--report-only` (rebuild the report from the last runs without simulating). Scratch folders
(`runs/`) are git-ignored and rebuilt on every run.

Conventions that keep results traceable:

- Every output file starts with the name of the testbench that wrote it; runs with a deliberate
  change add `__<what changed>`, post-layout runs add `__pex`. The `.log` files start with a
  header naming the testbench, the extraction (if any), what was changed and the date.
- One testbench per measurement: `--pex` takes the same schematic and swaps the block for its
  extraction, so schematic and post-layout results come from identical sources and limits.
- Waveform `.txt` files are 4–5 MB each; commit them only when someone needs them.
- Corners map to the `sm141064.ngspice` sections `typical`, `ss`, `ff`, `sf`, `fs` (MIM caps only
  have typical / ss / ff, so `sf` and `fs` use typical caps). Each run gets a `.spiceinit` with
  `set num_threads=1`, so parallel runs don't compete for threads.

## Adding a block

1. Write `*_tb.sch` files whose `.param` line holds every value the runner may change and whose
   `.control` block prints `echo RES name=$&value` lines.
2. In a `run_<block>.py`, build `tbtools.Case` objects (testbench, corner, temperature, params,
   seed), run them with `tbtools.run_cases`, and format the results.
