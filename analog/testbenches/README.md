# Analog testbenches

Characterization testbenches for the analog blocks. Each block has a folder with:

- **xschem testbenches** (`*_tb.sch`). Open them in xschem and press *Netlist* then *Simulate*. Each one plots its waveforms and prints its measurements as `RES name=value` lines.
- **a runner script** (`run_<block>.py`) that netlists the same schematics, runs them across sweeps, process corners, temperature, supply and device mismatch, and writes a report to `results/`.

`tbtools.py` holds the parts shared by all runners: netlisting, corner/temperature/parameter substitution, running ngspice and reading results.

Blocks covered so far: **DPI synapse** (`dpi/`).

## Running

Start xschem from the project root (`/foss/designs/engn2912e-project`), the same way as for `analog/neuron/neuron_5khz_testbench.sch`. The testbenches refer to the device as `analog/neuron/DPI.sym`, which xschem looks up relative to the directory it was started in.

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

## Adding another block

Copy the layout of `dpi/`:

1. Write one or more `*_tb.sch` files whose `.param` line holds every value the runner may change, and whose `.control` block prints `echo RES name=$&value` lines.
2. In a `run_<block>.py`, build `tbtools.Case` objects (testbench, corner, temperature, params, seed), run them with `tbtools.run_cases`, and format the results.
