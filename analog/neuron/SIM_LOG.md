# Neuron / Schmitt-Trigger Comparator — Simulation Log

Running record of simulation setup, measured results, and open issues for the
analog integrate-and-fire neuron in this folder. Newest run entries are at the
bottom of the **Run log**; the **Current status** section is always kept in
sync with the latest results.

Last updated: 2026-11-11

> **Note (2026-11-03):** the sections below up to the run log describe the
> earlier Schmitt-trigger neuron (`neuron_old.sch`). The current `neuron.sch`
> is the Indiveri et al. 2011 Fig. 4 neuron; its 5 kHz copy is logged in the
> last run-log entry.

---

## Current status

| Item | Status |
|---|---|
| Comparator thresholds | Measured: **VTH+ = 1.954 V, VTH− = 1.298 V**, hysteresis 0.656 V |
| Neuron integrates input | Yes: MEM steps up with each input pulse |
| Neuron fires | Yes: fires when MEM reaches ≈ 1.955 V (matches VTH+) |
| Reset to `reset_bias` (0.2 V) | **No**: MEM only drops to ≈ 0.74–1.01 V per reset |
| Reset speed | Fast: ≈ 6.5–7 ns from peak to bottom |

**Main open issue:** the reset ends itself. M1 turns off as soon as the
comparator flips back (MEM < VTH−), so MEM never reaches 0.2 V. C2 (100 fF on
the reset gate) extends the hold a little (bottom went from ≈ 1.2 V to
≈ 0.74–1.01 V) but is not enough. See *Open issues*.

---

## Files

| File | Purpose |
|---|---|
| `comparator.sch` / `.sym` | Schmitt-trigger comparator (inverting: VOUT falls when VIN rises past VTH+) |
| `neuron.sch` / `.sym` | Neuron: membrane cap C1, comparator, inverter (M2/M3), reset switch M1 to `reset_bias`, hold cap C2 |
| `neuron_testbench.sch` | Pulsed current input → MEM; writes `neuron_tb.raw` / `neuron_tb.txt` |
| `schmitt_trigger_comparator_testbench.sch` | Triangle-wave input on the comparator alone; measures VTH+ / VTH−; writes `comparator_tb.txt` |
| `neuron_tb.txt`, `comparator_tb.txt` | `wrdata` output: column pairs of (time, value) |
| `neuron_5khz.sch` / `.sym`, `neuron_5khz_testbench.sch` | Fig. 4 neuron copy sized for 5 kHz at 5 nA DC input (2026-11-03) |
| `neuron_sized.sch` / `.sym`, `neuron_sized_testbench.sch` | Fig. 4 neuron copy sized by sweep to `sizing_context.txt` at 9.5 nA DC (2026-11-05) |

---

## Current circuit parameters

### Comparator (`comparator.sch`)
- Stack: 2× PMOS (M5, M4) from VDD, 2× NMOS (M1, M2) to VSS; feedback NMOS M3 (VN → VDD) and PMOS M6 (VP → VSS), all gated by VOUT.
- All devices: W = 0.22 µm, L = 0.28 µm (minimum size).

### Neuron (`neuron.sch`)
| Device | Value |
|---|---|
| C1 (membrane) | 1 pF |
| M1 (reset NMOS, MEM → reset_bias) | W = 2 µm, L = 0.28 µm |
| M2 / M3 (reset inverter) | W = 0.22 µm, L = 0.28 µm |
| C2 (reset-gate hold cap) | 100 fF |

### Testbenches
| Testbench | Stimulus | Analysis |
|---|---|---|
| Neuron | `Iin = pulse(0 ipk delay trise tfall pulse_width per)`, ipk = 20 nA, delay = 100 µs, trise = tfall = 1 µs, pulse_width = 50 µs, per = 1 ms; vdd = 3.3 V, reset_bias = 0.2 V | `tran 1u 10m` |
| Comparator | `Vin = pwl(0 0 5m vdd 10m 0)` (5 ms up, 5 ms down) | `tran 1u 10m`, `meas` for VTH+ / VTH− |

---

## Measured results

### Comparator (from `comparator_tb.txt`)
| Quantity | Value | How measured |
|---|---|---|
| VTH+ | **1.954 V** | VIN when VOUT falls through 1.65 V (t ≈ 2.96 ms) |
| VTH− | **1.298 V** | VIN when VOUT rises through 1.65 V (t ≈ 8.03 ms) |
| Hysteresis | **0.656 V** | VTH+ − VTH− |
| VOUT swing | −0.002 to 3.307 V | full rail-to-rail |

### Neuron (from `neuron_tb.txt`, ipk = 20 nA)
| Quantity | Value |
|---|---|
| MEM step per input pulse | ≈ 1.0 V (20 nA × ~51 µs / 1 pF) |
| Firing level (MEM peak) | ≈ 1.955 V (agrees with VTH+) |
| MEM after reset | ≈ 0.74–1.01 V (target 0.2 V) |
| Reset fall time | ≈ 6.5–7.1 ns |
| Fires in 10 ms | 8 (VOUT has 16 edges) |
| VOUT overshoot | down to −0.17 V (capacitive kickback from fast MEM edges) |

---

## Open issues / next steps

1. **Reset doesn't reach 0.2 V.** It ends when MEM drops below VTH−
   (≈ 1.3 V; MEM falls a bit further because of the comparator + inverter
   delay). Hold the reset on for a fixed time that doesn't depend on VTH−:
   a one-shot pulse (delay chain + gate, or `pulse_gen`) or an SR latch
   that is cleared after a delay. That also sets the spike width, like
   `DURATION` in `../../mock/comparator.v`.
2. **Number of input pulses per fire depends on the starting point.**
   Because the reset level varies (0.74–1.01 V), the number of pulses
   needed to fire again varies too. Fixing (1) should make this regular.
3. **Time resolution around resets.** `tran 1u 10m` gives few points per
   reset. To study a single reset, run a short window with a max step,
   e.g. `tran 1n <window> 0 1n`.
4. **`.ic` / `uic` not applied.** MEM starts at ≈ 30 mV, not 0. Add
   `.ic v(mem)=0` and `tran … uic` if an exact starting point matters.
5. **Housekeeping.** The `analog/schmitt_trigger_comparator/` files are
   deleted in git and `analog/neuron/` is untracked; commit the move.
   Consider adding `*.raw` and `*_tb.txt` to `.gitignore`.

---

## Run log

### 2026-10-25: First neuron testbench runs
- **"unknown subckt … neuron"**: the plot title in TRAN_SIM opened with `'` and closed with `"`, which ended the code block's `value="…"` early. The `.control` block lost its `.endc` and swallowed the `.subckt neuron` definition. Fixed by matching the quotes.
- **"tran simulation(s) aborted" / singular matrix at `vbias#branch`**: label p13 on Vbias's + terminal said `VDD`, putting the 0.2 V Vbias in parallel with the 3.3 V V1 and leaving `reset_bias` floating. Fixed by relabeling it `reset_bias`.
- Ammeter renamed `iMEM` → `VMEM` so SPICE treats it as a 0 V source (an `I…` name would be a 0 A current source).
- Results written to the shared folder with absolute `write` / `wrdata` paths.

### 2026-10-26: ipk = 1 nA
- MEM rose ≈ 51 mV per pulse to only ≈ 0.53 V in 10 ms. It never reached VTH+, so the neuron never fired.

### 2026-10-26: ipk = 1 µA
- Fired ≈ 67 times during one 50 µs input pulse (every ≈ 0.75 µs).
- Reset was fast (≈ 9 ns) but only dropped MEM from ≈ 1.96 V to ≈ 1.21 V, i.e. to VTH−.
- Changes made afterwards: M1 widened to W = 2 µm, C2 = 100 fF added on the reset gate.

### 2026-10-26: Comparator characterization (triangle input)
- `pwl(0 0 5m vdd 10m 0)`, `tran 1u 10m`.
- VTH+ = 1.954 V, VTH− = 1.298 V, hysteresis = 0.656 V.

### 2026-10-26: ipk = 20 nA, delay = 100 µs, M1 W = 2 µm, C2 = 100 fF
- Fires on the 2nd input pulse and again roughly every 1–2 pulses after that (8 fires in 10 ms).
- Fires at ≈ 1.955 V. MEM resets to ≈ 0.74–1.01 V in ≈ 7 ns, still well above the 0.2 V target.

### 2026-11-03: `neuron_5khz` (Fig. 4 neuron sized for 5 kHz), run by the AI
- Files: `neuron_5khz.sch` / `.sym`, `neuron_5khz_testbench.sch`. Same topology as `neuron.sch`; sizes and biases in `../Analog_AI_Documentation.md` entry 28.
- Stimulus: Iin = 5 nA DC, VDD = 3.3 V, typical corner, 27 °C; `tran 20n 2.4m 0 20n uic` with `.ic v(VMEM)=0 v(spike)=0`.
- **f = 4.999 kHz** (8 periods, from the xschem-generated netlist). Spike 0 → 3.30 V, ≈ 6.4 µs wide at 1.65 V. VMEM peaks ≈ 1.66 V and resets to < 1 mV. Average power ≈ 0.21 µW.
- f vs Iin: 2 nA 1.75 kHz · 3 nA 2.86 kHz · 5 nA 5.00 kHz · 7.5 nA 7.54 kHz · 10 nA 9.95 kHz · 20 nA 18.4 kHz.
- Corners (Iin = 5 nA): tt 0 °C 4.92 kHz; ss 0/27/85 °C 1.79/2.96/4.35 kHz; ff 0 °C 3.27 kHz; tt 85 °C and ff 27/85 °C do not fire (leak > input).
- The testbench now loads `sm141064.ngspice mimcap_typical`. Without it the MIM caps are unknown subcircuits; the original `neuron_testbench.sch` still lacks this line and the bias `.param`s.

### 2026-11-05: `neuron_sized` (sweep to `sizing_context.txt`), run by the AI
- Files: `neuron_sized.sch` / `.sym`, `neuron_sized_testbench.sch`. Configs: `tools/analog_API_infrastructure/configs_sized/`. Details: `../Analog_AI_Documentation.md` entry 42.
- Changes vs `neuron_5khz`:
  - C2 is 22.18 × 22.18 µm (1.00 pF) and C1 is 10 × 10 µm (≈ 0.21 pF).
  - Biases: Vlk 0.425, VNA 1.93, VKup 2.35, VK 1.22, VKdn 0.588, VT 1.66 V (Vamp_bias 0.535 and VIp 0.573 unchanged).
- Stimulus: Iin = 9.5 nA DC, VDD = 3.3 V, tt, 27 °C. Analysis: `tran 40n 1.6m 0 40n uic`, measured over spikes 3–7.
- Results:

| Metric | Target | Result |
|---|---|---|
| period | 190–210 µs | 201.4 µs |
| t_spike (above 1.65 V) | 9–11 µs | 9.29 µs |
| t_refr (VMEM < 0.33 V → VMEM rises 10 mV above v_reset) | 12–15 µs | 14.69 µs |
| v_spike_max | ≥ 2.97 V | 3.23 V |
| v_reset | ≤ 50 mV | 0.9 mV |
| p_avg | ≤ 1 µW | 0.38 µW |
| a_cap | ≤ 700 µm² | 592 µm² |

- t_spike and t_refr come from the same C1 discharge, so they move together (t_refr ≈ t_spike + 5.4 µs). This leaves ≈ 0.3 µs of margin on each.
- Corners and temperature were not run.

### 2026-11-11: `DAC_binary` (1:2:4:8, multi-finger) vs `DAC` (1:2:3:4), run by the AI
Static characterisation in the container (script and decks outside the repo, `/tmp/dacbin_sim3`). Conditions as in `DACs-DPI.sch`: Iref = 14.42 nA into a diode-connected 1u/8u NMOS for Vb, V(Isum) held at 2.5 V, en = 3.3 V, all 16 codes. The old DAC's m = k devices were expanded into k unit instances, because the PDK mismatch model scales with W·L but ignores m.

| Result (tt, 27 °C) | `DAC_binary` | `DAC` (1:2:3:4) |
|---|---|---|
| LSB (least-squares) | 15.02 nA | 15.03 nA |
| Full scale (code 15) | 225.2 nA (15 LSB) | 150.2 nA (10 LSB) |
| Code 0 (off leakage) | 20.8 pA | 33.9 pA |
| INL / DNL max | 0.005 / 0.002 LSB | 0.005 / 0.002 LSB |
| Branch error vs ideal | +0.31 / +0.20 / +0.12 / +0.04 % | +0.32 / +0.18 / +0.11 / +0.07 % |
| Full scale within 1 % for V(Isum) ≥ | 2.04 V | 2.06 V |
| MC mismatch, 200 runs: branch σ | ×1 3.3 %, ×2 2.5 %, ×4 1.5 %, ×8 0.77 % | ×1 3.3 %, ×2 2.2 %, ×3 1.8 %, ×4 1.3 % |
| MC: DNL max (mean / p95), INL max p95 | 0.14 / 0.27 LSB, 0.17 LSB | 0.13 / 0.26 LSB, 0.15 LSB |
| MC: monotonic | 200 / 200 | 200 / 200 |
| MC: full scale σ (incl. reference mismatch) | 7.8 nA (3.4 %) | — |

- Corners (tt/ss/ff/sf/fs × 0/27/85 °C): LSB 14.89–15.14 nA, DNL ≤ 0.015 LSB everywhere. At ff/85 °C and fs/85 °C the off switches leak (code 0: 2.34 nA and 1.26 nA; 2.3 nA is 0.16 LSB), so code 1 reads 17.2 nA at ff/85 °C. This is an offset while en is high, not a linearity error. The binary DAC leaks more than the old one (15 vs 10 switch fingers).
- **Simulator setting:** multi-finger devices need `set ngbehavior=hsa` (the container's default `~/.spiceinit`). A run-directory `.spiceinit` without it makes nf devices bin by total width, and the ×2/×4/×8 branches then read about 3.7 % low (code 15 = 217.7 nA instead of 225.2 nA).

