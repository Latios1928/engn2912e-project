# XOR on `snn_analog`

XOR needs inhibition. With excitatory weights only, the network's output is a
monotone function of its inputs, and XOR (= OR and not AND) is not monotone. This
folder holds the circuits, testbenches and simulations that add one inhibitory
synapse to the output neuron and size the hidden layer so that one hidden neuron is
an OR and one is an AND:

```
A ─┬─ relay 0 ─┬─► hid 0 (OR,  code 15 each) ──(+, code 1)──┐
   │           │                                            ├─► out = A XOR B
B ─┴─ relay 1 ─┴─► hid 1 (AND, code 1 each)  ──(−, code 15)─┘
```

The hard part is the AND: one input must not fire it, and two coincident inputs
must. All decisions below come from the simulations in `results/` (tt, 27 °C,
mismatch from the PDK's `sw_stat_mismatch`, same seed = same chip for the A, B and
A+B runs of a sample).

## Circuit changes

| Cell | What it is |
|---|---|
| `analog/neuron/DAC_signed.sch/.sym` | `DAC` plus two static steering switches: sign `s` = 0 sends the current to `Isum_e`, `s` = 1 to `Isum_i`. Internal inverter for `s̄`. |
| `analog/neuron/DPI_inh.sch/.sym` | `DPI_sized` plus a 1:1 nFET mirror (2 µm / 8 µm) that sinks its output current from VMEM. |
| `analog/neuron/DPI_sized.sch/.sym` | Copy of `DPI.sch` with all four transistors at W 0.88 µm, L 1.12 µm (×4 in W and L, see below). `DPI.sch` is unchanged. |
| `analog/snn/snn_analog.sch/.sym` | All DPIs are `DPI_sized`. The 5 hidden → output DACs are `DAC_signed` (pins `s[4:0]`); their inhibitory currents go to `DPI_inh` on the output membrane (bias `VT_inh`). Separate DPI biases per layer: `Vthr_in`/`VT_in` (inputs), `Vthr_hid`/`VT_hid` (hidden), `Vthr`/`VT_dpi` (output). |

`inh_cell_tb` (old DPI sizes): inhibitory/excitatory charge ratio 1.007, crosstalk
between the two paths below 2 fC.

## Decisions

### 1. How to make the AND: two options

- **Option 1, leak AND.** The neuron's leak (`Vlk`) beats the DPI current of one
  input and loses to two. The DPI is linear, so two inputs give only R ≈ 2× the
  current of one, and the leak transistor is subthreshold: the working window is
  about 37 mV × ln R ≈ 25 mV of `Vlk` (predicted 27 mV, measured 25 mV,
  `vlk*.md`).
- **Option 2, threshold AND.** The hidden DPI's τ current is set between the
  current of one input (15 nA) and two (30 nA), so one input gives no DPI output at
  all and two give a large one. The leak only has to remove leftovers.

### 2. Option 1 sizing (`dpi/size_dpi.py`, `and_mc_k*.md`)

DPI mismatch, 200 samples, each sizing retuned to the same gain and τ: the spread of
ln(gain) is about 1.0 at minimum size and falls as 0.82/k when W and L are scaled by
k. M4 gives 34 % of it, M1 and M2 26 % each, M3 14 % (and almost all of the τ
spread).

| DPI scale (all 4 devices) | AND yield, 100 samples |
|---|---|
| ×1 (Vlk 0.455) | 9 % |
| ×4 (Vlk 0.485) | 67 % |
| ×6 | 79 % |
| ×8 | 83 % |

The yield saturates: past ×4 the failures come from the neuron and the relays, not
the DPI. A 25 mV window is too small for mismatch. **Decision: option 2.**

### 3. Option 2 sizing (`size_option2.py`, `option2_sizing*.md`)

DPI alone, 100–200 samples, τ bias at the centre of each sizing's working range:

| Sizing | Area (µm²) | Yield |
|---|---|---|
| all ×1 | 0.25 | 36–38 % |
| all ×2 / ×3 / ×4 | 0.99 / 2.2 / 3.9 | ~80 % / 92–96 % / 100 % |
| M1, M2 or M4 ×8 alone | 4.1 | no better than ×1 |
| M3 ×2 / ×3 / ×4 alone | 0.43 / 0.74 / 1.2 | 82 % / 95 % / 100 % |

Here the threshold is set by M3 (the τ device) alone, so M3 ×4 looks enough at a
third of the area. At neuron level (`hidden_tb`, `and_mc_o2*.md`, 100 samples,
50 pulses):

| Sizing | AND yield | Relays: one spike per pulse |
|---|---|---|
| uniform ×4 | 96 % | 200 / 200 |
| M3 ×4 only | 93 % | 193 / 200 (25–67 spikes in 50 pulses) |

The relays (input neurons) use the same DPI in a different mode (short τ, one spike
per pulse) and need the M1/M2/M4 matching that M3 ×4 alone does not give. **Decision:
uniform ×4 (`DPI_sized`).**

Two findings changed the procedure:
- Real relay spikes deliver about 40 % more charge than the ideal 10 µs pulses of
  the DPI-only test (wider effective enable plus injection on the DAC's node X), so
  the hidden threshold has to be centred with real relays, not DPI-only.
- The relays have to fire exactly one spike per pulse, so they get their own biases
  (`Vthr_in` 2.4 V, `VT_in` 0.72 V, latency about 10 µs).

### 4. Network operating point (`xor_tb`)

| Bias | Value | From |
|---|---|---|
| `Vthr_in` / `VT_in` (relays) | 2.4 / 0.72 V | one spike per pulse, `hidden_tb` |
| `Vthr_hid` / `VT_hid` (hidden) | 2.5 / 0.6225 V | centre of the 0.610–0.635 V AND window |
| `Vlk` | 0.48 V | |
| `Vthr` / `VT_dpi` (output) | 2.785 / 0.5096 V | centre of the 2.770–2.80 V XOR window |
| `VT_inh` (output inhibitory) | 0.5096 V | no effect in a sweep: the inhibition is late, not weak |

Weights: relays code 15; OR (hid 0) code 15 from each input; AND (hid 1) code 1
from each input; hid 0 → out code 1 excitatory; hid 1 → out code 15 inhibitory
(`s1` = 1). With hid 0 → out at code 15 or 8, the output fires before the AND neuron
in the (1,1) case (7 spikes in 20 pulses, `xor_o2.md`); code 1 slows it enough.

## Results

**Nominal (tt, 27 °C, 20 pulses, `xor_final.md`):** pass. Output 0 / 6 / 6 / 0 spikes
for (0,0) / (0,1) / (1,0) / (1,1); the AND neuron fires 34 times in (1,1) and never
with one input.

**Mismatch (`xor_mc_final.md`, 30 samples, all 4 cases per sample):** 27 / 30 pass.

| Case | Output spikes, mean (min–max) | AND spikes, mean |
|---|---|---|
| (0,0) | 0 | 0 |
| (0,1) / (1,0) | 6.2 / 6.4 (1–13) | 0 / 0.1 |
| (1,1) | 0.1 (0–1) | 35 (14–55) |

All three failures are one output spike in (1,1), before the AND neuron's inhibition
arrives. A spike-count threshold cannot fix this, since the weakest single-input
samples also give 1 spike.

**Corners and temperature (`xor_final.md`):** pass at tt and sf only. ss and 0 °C:
the AND neuron fires on one input. fs: relays burst (108 spikes in 20 pulses). ff and
85 °C: the relays never fire. Every bias is a fixed voltage on a subthreshold device,
so the currents move by orders of magnitude across corners. The network needs
current-referenced biases (next section).

### Current-referenced biases (`bias_replica.py`)

A fixed 0.6225 V on the hidden DPI's τ transistor gives ×0.05 (ss) to ×14 (ff) of its
tt current, and holding the current would need ±120 mV against a 25 mV window. So the
real specification is a current: the AND window is 1.31–2.34 nA of τ current, about
0.09–0.16 × the DAC reference `Iref`. `bias_replica.py` replaces every bias source by a
diode-connected copy of the transistor it drives (same type, W, L and rail), fed by a
current calibrated at tt and written as a ratio of `Iref`. Only the comparator
threshold `VT` (1.66 V, about VDD/2) stays a voltage (a divider on chip).

| Master current | Corners passing (of 7) | Failures |
|---|---|---|
| fixed voltages (before) | 2 | AND on one input, relays silent or bursting |
| replicas, nominal | **7** | – |
| replicas, −15 % | **7** | – |
| replicas, +15 % | 4 | one output spike in (1,1) (ff, fs, 0 °C) |
| replicas, −30 % / +30 % | 5 / 1 | relays miss pulses (ss, fs) / one or two output spikes in (1,1) |

Spike counts across the 7 points at nominal current: output 6–9, OR 99–119, AND 29–39
in (1,1), relays one spike per pulse everywhere (`results/bias_replica.md`,
`bias_replica_iref.md`). The replicas cancel process and temperature, but not the
absolute reference: the input pulses (10 µs every 200 µs) come from the digital clock,
so a higher reference shortens the analog events against them, the AND neuron fires
later, and the (1,1) race is lost. The working range is about −15 % to +10 %, too tight
for a simple on-chip reference.

Ratios from the calibration (`results/bias_replica.md`): hidden τ 0.121, relay τ 1.02,
output τ 0.0073, hidden gain 4.49, relay gain 17.9, output gain 0.0084, `Vlk` 0.162,
`VK` 1215, `VNA` 350, `VKup` 38, `VKdn` 2.37, `VIp` 1.67, `Vamp_bias` 6.7 (× `Iref`).
The strong-inversion replicas (`VK` 17.5 µA, `VNA` 5 µA) would draw about 76 µW; a replica
with a smaller W/L at a proportionally smaller current should give nearly the same
voltage (to be checked). The output DPI currents are about 110 pA, so leakage at high
temperature needs a look.

## Running

```bash
python3 analog/testbenches/xor/run_xor.py --only xor            # 4 cases, tt and corners
python3 analog/testbenches/xor/run_xor.py --only xor_mc --mc-xor 30
python3 analog/testbenches/xor/run_xor.py --only and_mc --mc 100 --set p_vlk=0.48
python3 analog/testbenches/xor/size_option2.py --mc 100
python3 analog/testbenches/xor/scan_coincidence.py --k 4 --mc 200
python3 analog/testbenches/dpi/size_dpi.py sweep
```

`--set NAME=VALUE` overrides a testbench parameter, `--dpi-k k1,k2,k3,k4` patches the
plain-`DPI` testbenches (`hidden_tb`) to other sizes, `--tag` names the result files.
`run_xor.py` writes `results/<suite>[_tag].csv/.md` and collects them in
`results/xor_results.md`.

| File | Purpose |
|---|---|
| `inh_cell_tb.sch` | Excitatory (`DPI_sized`) vs inhibitory (`DPI_inh`) charge on a held membrane |
| `hidden_tb.sch` | Two relays (DAC → DPI → neuron) into one hidden neuron with 3 DACs; plain `DPI` so `--dpi-k` can patch it |
| `xor_tb.sch` | Full `snn_analog`: 92 weight bits from codes `c0`–`c22`, sign bits `s0`–`s4`, pulses from `ina`/`inb` |
| `run_xor.py` | Suites `cell`, `hidden`, `vlk`, `and_mc`, `xor`, `xor_mc` |
| `size_option2.py` | Option 2 DPI sizing (threshold centre + DPI-only Monte Carlo) |
| `bias_replica.py` | XOR with every bias made by a diode replica from one master current; corners, reference shift, mismatch |
| `scan_coincidence.py` | DPI-only response to 15 vs 30 nA over a bias grid (R, predicted window, yield) |

## Pitfalls

- Maximum step 0.1 µs. At 0.5 µs the neuron produced false spikes at relay edges
  (`run_xor.py` checks for single-step jumps from below 1.5 V; `DACs-DPI-neuron.sch`
  still uses 0.5 µs).
- A `.param` with the same name as a net (case-insensitive: `vthr_hid` and the net
  `Vthr_hid`) makes ngspice rename the net on long instance lines and leave it
  floating ("singular matrix: check node {vthr_hid}"). Parameters are `p_*`, and runs
  with "singular matrix" in the log are marked failed.
- `wrdata` does not accept `v(spike[0])`: copy the net with a unity VCVS
  (`Esp0 sp0 0 spike[0] 0 1`).
- Start the membranes and spike outputs at 0 V with `.ic`. Without it, the DC
  operating point of the sized network does not converge.

## Open

- The sign bits are tied in the testbenches. They are not in the digital register
  file yet (`snn_analog.v` is unchanged), and `mixed/` ties `s[4:0]` to 0.
- The (1,1) race: make the output's first spike later (lower output gain) or the
  inhibition earlier, and check on the same 30 samples.
- The (1,1) race now limits the mismatch yield and the tolerance to the reference current.
- Mismatch with the replicas included (`bias_replica.py --mc 30`): running at the time of writing.
- A bias-generator schematic with realizable mirror ratios; per-chip trim or an external
  reference pin for the master current.
- `Vlk` has not been re-swept since the switch to option 2 (0.48 V is from option 1's window,
  0.475–0.495 V).
