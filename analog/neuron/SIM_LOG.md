# Neuron / Schmitt-Trigger Comparator — Simulation Log

Running record of simulation setup, measured results, and open issues for the
analog integrate-and-fire neuron in this folder. Newest run entries are at the
bottom of the **Run log**; the **Current status** section is always kept in
sync with the latest results.

Last updated: 2026-10-26

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
   `DURATION` in `../mock/comparator.v`.
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
