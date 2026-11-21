# Pin list: final top level

Chip top `snn_top.v` = digital `snn_digital` (LibreLane, `librelane/snn_top`) + analog macro
`SNN_signed` (`analog/layout_tools/top/SNN_signed/SNN_signed.gds`: `bias` + `analog/snn/snn_analog_signed.sch`).
Status 2026-11-18. Sources: `snn_top.v`, `digital/regs.v`, `SNN_signed.gds` (pin labels),
`SNN_signed_lvs_ref.spice`.

## 1. Chip pins (external)

| Pin | Dir | Domain | Width | Function | Connects to |
|---|---|---|---|---|---|
| `clk` | in | digital | 1 | system clock, **1 MHz** (LibreLane `CLOCK_PERIOD` 1000 ns). With the reset pulse timing (period 200, width 10 clk) the inputs spike at the network's **5 kHz** operating rate, 10 µs wide | digital: `regs`, `pulse_gen` |
| `rst` | in | digital | 1 | synchronous reset, active high: pulse generator and pulse timing (not weights or signs) | digital: `regs`, `pulse_gen` |
| `data[3:0]` | in | digital | 4 | value to write | digital: `regs` |
| `addr[3:0]` | in | digital | 4 | register address, written every clock; `4'hF` = idle (no `wren` pin). 0–7 magnitudes (synapse k, see §3), 8–9 signs, 10–13 pulse period/width, 14 unused | digital: `regs` |
| `in[1:0]` | in | digital | 2 | enables input pulse channel i (period/width from registers, reset 200 / 10 clk cycles) | digital: `pulse_gen` |
| `out[4:0]` | out | analog → pin | 5 | spikes `{output, hidden[1:0], input[1:0]}`, full-swing 0 … VDD, ≈ 9–13 µs pulses | analog `spike[4:0]` |
| `Iref` | in (current) | analog | 1 | bias-cell reference current, **100 nA sourced into the pin** (scales every bias; adjusting it off chip replaces a trim) | analog `Iref` |
| `VT` | in (voltage) | analog | 1 | neuron firing threshold, **1.66 V** (high-impedance gate input) | analog `VT` |
| `VDDA` | supply | analog | 1 | 3.3 V | analog `VDD` |
| `VDDD` | supply | digital | 1 | 3.3 V, separate from `VDDA` so digital switching noise stays off the analog supply | digital VDD |
| `VSS` | supply | ground | 1 | 0 V, substrate (shared) | analog `VSS`; digital VSS |

Total: 17 digital signal pins (`clk`, `rst`, 4 + 4 + 2 inputs, 5 outputs) + `Iref` + `VT` + `VDDA` + `VDDD` + `VSS` = all 22 available.
The analog biases are internal: the bias cell inside `SNN_signed` makes them from `Iref`.

## 2. Internal top-level nets (digital ↔ analog macro)

| Net | Width | From → To | Notes |
|---|---|---|---|
| `w[31:0]` | 32 | `snn_digital.w` → `SNN_signed.w[31:0]` | magnitude of synapse k = `w[4k+3:4k]` (0–15), static while running |
| `s[7:0]` | 8 | `snn_digital.s` → `SNN_signed.s[7:0]` | sign of synapse k (1 = inhibitory), static while running |
| `pulse[1:0]` | 2 | `snn_digital.pulse` → `SNN_signed.pulse[1:0]` | input spike trains, gate the input-layer DAC enables |
| `spike[4:0]` | 5 | `SNN_signed.spike[4:0]` → chip `out[4:0]` | no logic in between (`snn_top.v`) |

## 3. Analog macro `SNN_signed` pins (596.5 × 798.5 µm, all on the bottom edge, Metal2 labels)

| Pin(s) | x on the bottom edge (µm) |
|---|---|
| `w[31]` … `w[0]` | 35.25 … 84.85 (1.6 µm pitch, `w[0]` rightmost) |
| `s[7]` … `s[0]` | 86.45 … 97.65 |
| `pulse[1]`, `pulse[0]` | 99.25, 100.85 |
| `VDD`, `VSS` | 378.51, 380.11 |
| `Iref` | 473.08 |
| `VT` | 486.29 |
| `spike[4]` … `spike[0]` | 605.63 … 612.03 |

Synapse map (as in `mock/snn_analog.v` and the macro's netlist):

| k | Magnitude | Sign | Synapse | DAC in the layout |
|---|---|---|---|---|
| 0, 1 | `w[3:0]`, `w[7:4]` | `s[0]`, `s[1]` | `pulse[i]` → input neuron i (inhibitory = off: the input neurons have no inhibitory DPI) | xdac0_0, xdac1_0 |
| 2 … 5 | `w[23:8]` | `s[5:2]` | input i → hidden j (k = 2 + 2j + i) | xdac2_0 … xdac3_1 |
| 6, 7 | `w[31:24]` | `s[7:6]` | hidden j → output (k = 6 + j) | xdac4_0, xdac4_1 |

## 4. Supplies and domains

- Analog macro: 3.3 V devices only (`nfet_03v3`, `pfet_03v3`); VDD = 3.3 V, VSS = 0 V = substrate.
  The bias cell draws ≈ 0.72 µA; the five neurons ≈ 0.3–0.5 µW each.
- Digital (`librelane/snn_top/config.json`): cell library `gf180mcu_fd_sc_mcu7t5v0`, signed off at the
  **5 V** corners (`nom_tt_025C_5v00`, `ss_125C_4v50`). See §5.
- Planned: separate supplies `VDDA` (analog) and `VDDD` (digital), both 3.3 V, shared `VSS`.

## 5. Open interface issues (to resolve before the final top level)

1. **Supply voltage.** The digital block is timed at 5 V, the analog macro is 3.3 V. Driving `w`, `s`,
   `pulse` from a 5 V domain would put 5 V on 3.3 V gates, and the 3.3 V spikes would not reach a 5 V
   logic high. Run the digital block at 3.3 V on `VDDD` (the library has 3v00 / 3v30 / 3v60 corners),
   or add level shifters.
2. **`Iref`, `VT`, `VDD` (→ `VDDA`), `VSS`** of the analog macro are not ports of `snn_top.v` or of the black box;
   they must be added as chip pins / pads (analog pads for `Iref` and `VT`).
3. **The committed digital layout is out of date.** `librelane/snn_top/results/snn_top.gds` still has
   the earlier 3-5-1 interface; re-run `librelane/snn_top/run.sh` on the current RTL.
4. **Pin placement.** All analog macro pins are on its bottom edge, with `w`, `s` and `pulse` together
   at the left end; the digital block's outputs should face them, and `out[4:0]` must reach the pads
   on a layer the pads accept.
