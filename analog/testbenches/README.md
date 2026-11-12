# Analog testbenches

Characterization testbenches for the analog blocks. Each block has a folder with:

- **xschem testbenches** (`*_tb.sch`). Open them in xschem and press *Netlist* then *Simulate*. Each one plots its waveforms and prints its measurements as `RES name=value` lines.
- **a runner script** (`run_<block>.py`) that netlists the same schematics, runs them across sweeps, process corners, temperature, supply and device mismatch, and writes a report to `results/`.

`tbtools.py` holds the parts shared by all runners: netlisting, corner/temperature/parameter substitution, running ngspice and reading results. `tbpex.py` adds the post-layout option (`--pex`), see *Post-layout (PEX)* below.

Blocks covered so far: **DPI synapse** (`dpi/`), **neuron** (`neuron/`), **signed weight DAC** (`dac/`).

## Folder layout

```
analog/
├── neuron/                      schematics and symbols of the blocks (DAC, DPI, neuron_sized, ...)
│   └── layout/                  layouts (<cell>.gds), their generators and DRC/LVS scripts
│       └── PEX/                 parasitic extraction: extract.sh <cell> -> <cell>_pex.spice + wrapper
│                                (README.md there: what to do after a layout change)
└── testbenches/
    ├── README.md                this file
    ├── tbtools.py, tbpex.py     shared runner code
    └── <block>/                 one folder per block (dac/, dpi/, neuron/)
        ├── <name>_tb.sch        xschem testbenches (schematic block)
        ├── run_<block>*.py      runner scripts: single runs, sweeps, corners, mismatch;
        │                        --pex runs the same testbench on the post-layout block
        ├── results/             everything the testbenches produce: waveforms (.txt), logs (.log),
        │                        runner reports (.md / .csv / .png); post-layout ones end in __pex
        └── runs/                scratch, one folder per simulation (git-ignored, rebuilt every run)
```

Rules that keep this traceable:

- Every output file starts with the name of the testbench that wrote it (`results/neuron_nominal_tb.txt`, `results/neuron_rate_tb.csv`). Runs with a change on purpose add `__<what changed>` (`neuron_nominal_tb__fail_vkdn0p56.log`), post-layout runs add `__pex`.
- Testbench folders hold only testbenches and runners; their outputs go to `results/` (from the xschem GUI too). The `.log` files there start with a header naming the source testbench, the extraction (if any), what was changed and the date.
- One testbench per measurement. There are no separate post-layout testbenches: a runner's `--pex` takes the same schematic and swaps the block for its extraction, so schematic and post-layout results always come from identical sources, measurements and limits. The extraction lives with the layouts (`analog/neuron/layout/PEX/`).
- Waveform `.txt` files are 4-5 MB each. Commit them only when someone needs them; otherwise keep `.log` and `results/`.

## Running

Start xschem from the project root or from `analog/neuron`. The `xschemrc` files in those two folders put both on the symbol search path, so `analog/neuron/DPI.sym` and bare `DPI.sym` references both resolve. Restart xschem after pulling them, because it reads `xschemrc` only at startup.

Batch runs (from any directory):

```sh
python3 analog/testbenches/dpi/run_dpi.py                    # all suites, about 10 s
python3 analog/testbenches/dpi/run_dpi.py --quick            # fewer points, 20 mismatch samples
python3 analog/testbenches/dpi/run_dpi.py --only nominal,pvt # selected suites
python3 analog/testbenches/dpi/run_dpi.py --mc 500 --jobs 8  # more mismatch samples
```

The runner writes:

- `dpi/results/dpi_results.md`: the report, with tables for every suite and the plots;
- `dpi/results/<suite>.csv`: every measured value for every case;
- `dpi/runs/<case>/`: the netlist, ngspice log and waveform files of each simulation. This folder is git-ignored and is rebuilt on every run.

Notes on the runner:

- It stops with an error if any pin of the DPI instance lands on an unnamed net (`netN`). That happens when the pins of `DPI.sym` move and the testbench wires no longer reach them. (It happened once while these testbenches were being written: the `Isum` pin moved to the left side of the symbol.)
- Each run gets a `.spiceinit` copied from `~/.spiceinit` with `set num_threads=1` added, so parallel runs don't compete for threads. Without that, 8 parallel runs were about 10× slower.
- Corners map to the `sm141064.ngspice` sections `typical`, `ss`, `ff`, `sf`, `fs`. MIM caps only have typical/ss/ff, so `sf` and `fs` use typical caps. Mismatch runs set `sw_stat_mismatch=1` and a different `.options seed` for each sample.

## DPI synapse (`dpi/`)

Device under test: `analog/neuron/DPI.sch`.

- M1 (gate `Vthr`) and the diode-connected M2 form a differential pair on the tail node `Isum`.
- M3 (gate `VT`) is the τ leak into `Vsyn` (internal node `net1`).
- C4 (1 pF, ideal `capa`) sits between VDD and `Vsyn`.
- M4 is the output pFET that drives `Isyn`.

The DAC is replaced by an ideal current sink `Iw` on `Isum`, so the synapse is characterized on its own.

### Reference operating point

| Parameter | Value | Meaning |
|---|---|---|
| `vdd` | 3.3 V | supply |
| `vthr` | 2.9 V | gate of M1 (absolute, as in `DACs-DPI.sch`) |
| `vtau` | 0.40 V | Vsg of M3: the testbench sets `VT = VDD − vtau`, as `V2` does in `DACs-DPI.sch` |
| `iw` | 5 nA | tail current while an input is active |
| `tpw` | 100 µs | input spike width (spike test) |
| `rate` | 1 kHz | spike-train rate (spike test) |

The AI chose these so that the gain Isyn/Iw is about 1.4 and τ ≈ 0.4 ms. That gives Isyn ≈ 7 nA, the same order as the 5 nA that drives `neuron_5khz` at 5 kHz. `DACs-DPI.sch` used `Vsg(M3) = 0.5 V` and `Vthr = 3 V` until 2026-11-05, which give a gain of 0.012 and τ_decay = 33 µs (simulated with the step test). It now uses the reference values above. Change the `.param` line in each testbench, and `REF` in `run_dpi.py`, to move the reference point.

### Testbenches

| File | Stimulus | Measures |
|---|---|---|
| `dpi_dc_tb.sch` | `Iw = 10^V(lg)` from a B-source, so one `dc` sweep covers 100 pA to 100 nA | Operating point; Isyn vs Iw and its log-log slope over 0.5–50 nA; Isyn vs Vthr, Vtau and VDD (mV per decade); leakage with Iw = 0 |
| `dpi_step_tb.sch` | Iw on from 1 to 11 ms | Steady-state gain; rise τ (63 %) and 10–90 % time; decay τ (37 %); decay shape (13.5 % point / 2τ, 1 = exponential); residual current; lowest V(Isum), i.e. headroom left for the DAC |
| `dpi_spike_tb.sch` | x1: one pulse of width `tpw`; x2: pulse train at `rate` | Single-spike EPSC peak, charge and decay τ; the same charge expressed as a step on 0.86 pF (`neuron_5khz` Cmem); train mean, ripple, and mean / (charge per spike × rate), which is 1 for a linear synapse |

### Runner suites

| Suite | What it varies | Testbench |
|---|---|---|
| `nominal` | nothing (tt, 27 °C) | all three |
| `tau` | `vtau` 0.34–0.46 V | step |
| `vthr` | `vthr` 2.80–3.00 V | step |
| `weight` | `iw` = w × 1 nA, w = 1…7 (3-bit weight) | spike |
| `width` | `tpw` 10–500 µs | spike |
| `rate` | `rate` 0.25–5 kHz | spike |
| `pvt` | tt/ss/ff/sf/fs × 0/27/85 °C | all three |
| `vdd` | VDD 3.0/3.3/3.6 V, with Vthr fixed and with Vthr = VDD − 0.4 V | step |
| `mc` | device mismatch, 100 samples by default | step |

The pass/fail targets in `SPECS` (`run_dpi.py`) are **provisional**. The AI chose them around the simulated typical behaviour so that a change in behaviour shows up; they are not project requirements. Replace them once the synapse specs are set.

### What the first run shows (2026-11-05)

See `dpi/results/dpi_results.md` for the full tables. In short:

1. **Typical works as a DPI.** Gain 1.40, τ_rise 0.40 ms, τ_decay 0.43 ms, exponential decay (shape 0.99), leakage 3.3 pA. The log-log slope is 0.88 (slightly sub-linear in Iw).
2. **The response to a single spike is strongly non-linear in the charge per spike.** Vsyn idles at VDD and has to be pulled down about 0.5 V before Isyn becomes significant, so small inputs do almost nothing.
   - At 100 µs width, the charge per spike for weights 1…7 spans 3.7×10⁻⁵ to 0.54 pC: a factor of about 15,000 where a linear synapse would give 7.
   - 10 µs pulses at 5 nA give no measurable EPSC.
   - Spike trains facilitate: the train mean is about 4× (charge per spike × rate).
3. **Device mismatch is large.** With every transistor at 0.22/0.28 µm, gain has std/mean ≈ 1.1 (0.11 to 14.5 over 200 samples), and τ_decay ≈ 0.7.
4. **Fixed bias voltages make the synapse corner- and temperature-dependent**, as with the neuron. τ_decay ranges from 2.9 µs (ff, 85 °C) to 15 ms (fs, 0 °C). At ff and sf at 85 °C, the gain falls below 0.004.
5. **An absolute Vthr makes the gain follow VDD exponentially.** With Vthr fixed at 2.9 V, the gain is 0.0015 at 3.0 V and 159 at 3.6 V. With Vthr = VDD − 0.4 V, it stays between 1.25 and 1.57.

Other things to check in the schematic (not changed here):

- C4 is an ideal `capa`. It should become a MIM cap like those in `neuron_5khz.sch`; the testbenches already load `mimcap_typical`.
- The bulks of M1 and M2 are tied to `Isum`. On silicon this needs NMOS in an isolated p-well; otherwise the bulks go to VSS and the pair sees body effect. Check what the PDK offers.

### DPI at the network's operating point (`dpi/`, 2026-11-12)

The testbenches above use 5 nA inputs, 100 µs pulses and an output held at 0 V. These two use the network's conditions: inputs of code × 15 nA for 10 µs (what `DAC_signed` delivers), the output held at a membrane voltage, the sized excitatory cell **and** the inhibitory `DPI_inh` side by side. Shared code: `dpi/dpicommon.py`.

| File | What it does |
|---|---|
| `dpi_load_tb.sch` + `run_dpi_load.py` | DC input 15 / 45 / 150 nA, output voltage swept 0–3.3 V: how much output is left as VMEM rises (excitatory) or falls (inhibitory), and the tail voltage V(Isum) the DAC sees. Suites `bias` (the four presets), `pvt`, `mc` |
| `dpi_pulse_tb.sch` + `run_dpi_pulse.py` | DAC-like current pulses: charge on the membrane per charge in. Suites `code`, `train` (10 pulses at 5 kHz), `pair` (two pulses 20 µs–2 ms apart), `width` (10 vs 16.5 µs), `vmem`, `pvt`, `mc` |

Options on both: `--cell DPI_sized|DPI` (excitatory cell; default `DPI_sized`), `--bias output|hidden|relay|chain` (presets from the XOR README and `DACs-DPI-neuron.sch`; default `output`), `--only`, `--mc N`, `--pex`, `--report-only`. Results: `dpi/results/<tb>[__<cell>][__<bias>][__pex].md/.csv/.png`. The `chain` preset is meant for the min-size `DPI`; the inhibitory `DPI_inh` (a sized cell) is not matched to it.

```sh
python3 analog/testbenches/dpi/run_dpi_load.py                          # DPI_sized, output biases, ~20 s
python3 analog/testbenches/dpi/run_dpi_pulse.py --cell DPI --bias chain # min-size DPI as on main
```

## Neuron (`neuron/`)

Device under test: `analog/neuron/neuron_sized.sch`, targets from `analog/neuron/sizing_context.txt`.

| File | What it does |
|---|---|
| `neuron_nominal_tb.sch` | Constant 9.5 nA into VMEM, tt, 27 °C. Measures period, spike width, refractory time, spike peak, reset level and power on spikes 3-7 (same definitions as the sizing sweep) and prints `CHECK ... PASS/FAIL` per spec. In the GUI it simulates the schematic neuron and writes `results/neuron_nominal_tb.txt` |
| `run_neuron_nominal.py` | Runs `neuron_nominal_tb` once and writes `results/neuron_nominal_tb[__pex][__<tag>].txt/.log`; `--pex` for the post-layout neuron, `--param NAME=VALUE --tag <what>` for a deliberate change, `--corner`/`--temp` |
| `results/neuron_nominal_tb.txt/.log` | Last schematic run (all 6 specs pass) |
| `results/neuron_nominal_tb__pex.txt/.log` | Last post-layout run (t_refr fails, see below) |
| `results/neuron_nominal_tb__fail_*.txt/.log` | Two deliberately broken runs that show the checks catch failures (Vlk 0.55 V: no firing; VKdn 0.56 V: 3 specs fail) |
| `neuron_rate_tb.sch` | Counts spikes for one input current: rate, time to first spike, latch check |
| `run_neuron_rate.py` | Sweeps the input current 0.3 nA-10 µA with `neuron_rate_tb` and refines the firing, overdrive and latch onsets; `--pex` for the post-layout neuron, `--report-only` to rebuild the report from `runs/` without simulating. Writes `results/neuron_rate_tb[__pex].md/.csv` and `results/neuron_rate_tb.png` (both curves when both exist) |
| `neuron_pulse_tb.sch` | Square current pulses into VMEM (amplitude, width, interval): input pulse that first fires, input pulses per output spike, VMEM step and leak droop of pulse 1, effective membrane capacitance |
| `run_neuron_pulse.py` | Three suites with `neuron_pulse_tb`: *charge* (pulses to fire vs charge per pulse, against the ideal ceil(Q/q)), *interval* (leak loss between pulses), *refractory* (pulses lost after a spike); `--pex`, `--only`, `--report-only`. Writes `results/neuron_pulse_tb[__pex].md/.csv` and `results/neuron_pulse_tb.png` |
| `run_neuron_robust.py` | Robustness with `neuron_nominal_tb` (runs of 5 ms): *pvt* (5 corners x 0/27/85 °C), *vdd* (3.0/3.3/3.6 V, PMOS biases fixed or tracking VDD), *bias* (each bias ±10 mV: sensitivity and tolerated drift per spec), *mc* (mismatch, `--mc N`, default 100: spread and yield); `--pex`, `--only`, `--quick`, `--report-only`. Checks the six specs itself (spike peak ≥ 0.9 VDD). Writes `results/neuron_nominal_tb__robust[__pex].md/.csv` and `_pvt.png`, `_mc.png` |

```sh
python3 analog/testbenches/neuron/run_neuron_nominal.py        # schematic, about 11 s
python3 analog/testbenches/neuron/run_neuron_nominal.py --pex  # post-layout, about 45 s
python3 analog/testbenches/neuron/run_neuron_nominal.py --param p_vkdn=0.56 --tag fail_vkdn0p56
python3 analog/testbenches/neuron/run_neuron_rate.py           # schematic, about 3 min
python3 analog/testbenches/neuron/run_neuron_rate.py --pex     # post-layout
python3 analog/testbenches/neuron/run_neuron_rate.py --quick   # 10 currents, no refinement
python3 analog/testbenches/neuron/run_neuron_pulse.py          # 29 pulse runs
python3 analog/testbenches/neuron/run_neuron_robust.py         # 137 runs, about 20 min with 4 jobs
python3 analog/testbenches/neuron/run_neuron_robust.py --only pvt,bias --pex
```

### Neuron: schematic vs post-layout (tt, 27 °C, 9.5 nA DC, `neuron_nominal_tb`)

| Spec | Target | Schematic | Post-layout (`__pex`) | Change |
|---|---|---|---|---|
| period | 190–210 µs | 201.4 µs | 208.8 µs | +3.7 % |
| t_spike | 9–11 µs | 9.20 µs | 10.23 µs | +11 % |
| t_refr | 12–15 µs | 14.61 µs | **16.11 µs FAIL** | +10 % |
| v_spike_max | ≥ 2.97 V | 3.224 V | 3.274 V | |
| v_reset | ≤ 50 mV | 0.90 mV | 0.90 mV | |
| p_avg | ≤ 1 µW | 0.381 µW | 0.392 µW | +3 % |

The extraction (2026-11-12) has the 17 transistors of `neuron_sized.sch` with matching sizes and connections, 46 dummies and both MIM caps at their drawn sizes. It adds 27.5 fF on VMEM (+2.7 % on C2 = 1 pF), 17.1 fF on `spike` (+8 % on C1 ≈ 0.21 pF), 11.1 fF on net1 and 7.7 fF on net2; coupling into VMEM from switching nets is at most 0.8 fF.

Post-layout fails `t_refr`. Spike width and refractory time both come from the discharge of C1 (the spike node) through the VKdn current, so the 8 % extra capacitance there lengthens both by about 10 %. The period keeps only 1.2 µs of margin, from the 27 fF on VMEM. Ways to recover (not yet tried): raise VKdn by a few mV (sensitive: −28 mV lengthened t_spike and t_refr by 7.9 and 13 µs, `results/neuron_nominal_tb__fail_vkdn0p56.log`), or shrink C1 in schematic and layout by the 17 fF of wiring; pull the period back with Vlk or the input current. Re-run both `run_neuron_nominal.py` and `--pex` after any change.

## Signed weight DAC (`dac/`)

Device under test: `analog/neuron/DAC_signed.sch`, the 1:2:3:4 `DAC` with a sign switch (`s` = 0: current to `Isum_e`, `s` = 1: to `Isum_i`).

| File | What it does |
|---|---|
| `dac_signed_static_tb.sch` | Iref 14.42 nA into a 1 µm / 8 µm diode for Vb, `en` high, both outputs held at 2.5 V. One nested DC sweep: all 16 codes × both signs; then full scale while sweeping each output's voltage (compliance). `gmin` is 1e-16 S: the default 1e-12 S adds 2.5 pA per node, which hides the real leakage |
| `run_dac_signed.py` | Suites *nominal* (incl. what each digital sign-magnitude weight −7…+7 delivers), *pvt* (5 corners × 0/27/85 °C), *mc* (`--mc N`, default 100, incl. the reference diode). Unit current, branch ratios, INL, monotonicity, inhibitory/excitatory ratio, current to the unselected output, code-0 leakage, compliance. `--pex` (ready for a future layout), `--only`, `--report-only`. Writes `results/dac_signed_static_tb[__pex].md/.csv`, `_codes.csv`, `.png` |

```sh
python3 analog/testbenches/dac/run_dac_signed.py                # nominal, pvt, 100 mismatch samples, ~2 min
python3 analog/testbenches/dac/run_dac_signed.py --only nominal
python3 analog/testbenches/dac/run_dac_signed.py --pex          # once DAC_signed has a layout
```

Not covered yet: the charge per input spike when `en` switches (a pulse testbench), and `DAC` / `DAC_binary` on their own.

## Post-layout (PEX)

Extraction: `analog/neuron/layout/PEX/` and its README (**read it after any layout change**).
In short: `extract.sh <cell>` copies the layout, runs Magic and writes `<cell>_pex_wrapper.spice`,
a subcircuit `<cell>_pex` with the same pins as the symbol.

There are no separate post-layout schematics. Runners with `--pex` netlist the normal testbench and call `tbpex.use_pex(text, cell)`, which
switches every instance of `<cell>` to `<cell>_pex`. It refuses to run if the layout changed
since the last extraction (the GDS copy in `PEX/` differs from `analog/neuron/layout/<cell>.gds`).
To add `--pex` to another runner, call `tbpex.use_pex()` on the netlist text before running the cases.

## Adding another block

Copy the layout of `dpi/`:

1. Write one or more `*_tb.sch` files whose `.param` line holds every value the runner may change, and whose `.control` block prints `echo RES name=$&value` lines.
2. In a `run_<block>.py`, build `tbtools.Case` objects (testbench, corner, temperature, params, seed), run them with `tbtools.run_cases`, and format the results.
