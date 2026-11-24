# Pin list: final top level

Chip top `snn_top.v` = digital `snn_digital` (LibreLane, `librelane/snn_top`) + analog macro
`SNN_signed` (`analog/layout_tools/top/SNN_signed/SNN_signed.gds`: `bias` + `analog/snn/snn_analog_signed.sch`).
Status 2026-11-24. Sources: `snn_top.v`, `digital/regs.v`, `SNN_signed.gds` (pin labels),
`SNN_signed_lvs_ref.spice`.

## 1. Chip pins (external)

| Pin | Dir | Domain | Width | Function | Connects to |
|---|---|---|---|---|---|
| `clk` | in | digital | 1 | system clock, **1 MHz** (LibreLane `CLOCK_PERIOD` 1000 ns). With the reset pulse timing (period 200, width 10 clk) the inputs spike at the network's **5 kHz** operating rate, 10 µs wide | digital: `regs`, `pulse_gen` |
| `rst` | in | digital | 1 | synchronous reset, active high: pulse generator and pulse timing (not weights or signs) | digital: `regs`, `pulse_gen` |
| `data[3:0]` | in | digital | 4 | value to write | digital: `regs` |
| `addr[3:0]` | in | digital | 4 | register address, written every clock; `4'hF` = idle (no `wren` pin). 0–7 magnitudes (synapse k, see §3), 8–9 signs, 10–13 pulse period/width, 14 input enables (below) | digital: `regs` |
| `out[4:0]` | out | analog → pin | 5 | spikes `{output, hidden[1:0], input[1:0]}`, full-swing 0 … VDD, ≈ 9–13 µs pulses | analog `spike[4:0]` |
| `Iref` | in (current) | analog | 1 | bias-cell reference current, **100 nA sourced into the pin** (scales every bias; adjusting it off chip replaces a trim) | analog `Iref` |
| `VT` | in (voltage) | analog | 1 | neuron firing threshold, **1.66 V** (high-impedance gate input) | analog `VT` |
| `VDDA` | supply | analog | 1 | 3.3 V | analog `VDD` |
| `VSSA` | ground | analog | 1 | 0 V, analog ground | analog `VSS` |
| `VDDD` | supply | digital | 1 | 3.3 V, separate from `VDDA` so digital switching noise stays off the analog supply | digital VDD |
| `VSSD` | ground | digital | 1 | 0 V, digital ground, separate from `VSSA` for the same reason | digital VSS |

Total: 15 digital signal pins (`clk`, `rst`, 4 + 4 inputs, 5 outputs) + `Iref` + `VT` + 4 supplies (`VDDA`, `VSSA`, `VDDD`, `VSSD`) = **21 pads**. Open: confirm the pad limit with the organisers.

**Input enables (register 14).** The two input pulse channels are switched on and off by register 14
(`INPUT EN`), not by pins: write `data = 4'b00 b1 b0` to `addr = 14`, where bit i enables channel i
(`0011` both, `0001` input 0 only, `0000` off; `data[3:2]` are ignored). `rst` clears it to `00`.
`pulse_gen` samples the enables only at period boundaries (every 200 µs by default), so a 3 µs register
write behaves like the former `in[1:0]` pins, which this register replaced (23 → 21 pads, 2026-11-24).
Below, "`in`" means this register.
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

- Analog macro: 3.3 V devices only (`nfet_03v3`, `pfet_03v3`) on `VDDA` / `VSSA`.
  The bias cell draws ≈ 0.72 µA; the five neurons ≈ 0.3–0.5 µW each.
- Digital (`librelane/snn_top/config.json`): cell library `gf180mcu_fd_sc_mcu7t5v0` on `VDDD` / `VSSD`,
  signed off at the 3.3 V corners (`tt_025C_3v30`, `ss_125C_3v00`, `ff_n40C_3v60`), so the digital
  outputs `w`, `s`, `pulse` swing 0–3.3 V like the macro's inputs, and no level shifters are needed.
- The two grounds are separate nets and pads, so digital switching current does not flow in the
  analog ground. They share the p-substrate; the macro's `ISOSUB` marker (GDS 23/5, extraction / LVS
  only) keeps them separate nets in chip-level LVS (README, Physical design).

## 5. Power-up and operating procedure

The weight and sign registers (addresses 0–9) have **no reset**: they power up in an arbitrary
state, and `rst` does not change them. `rst` resets only the pulse timing (200 / 10), the input
enables (`in = 00`) and the pulse generator. An arbitrary weight set is harmless while `in = 00`: no input pulses means no DAC is ever
enabled, so nothing fires (scenario 1, all weights at maximum with `in = 00`, passes in every
simulation, RTL to post-layout). Procedure:

1. Power up with `addr = 4'hF`. The register file writes on every clock edge while `addr` is not
   `4'hF` (there is no write-enable pin), so the board must hold `addr` at `4'hF` from power-on
   (pull-ups), or registers are overwritten continuously.
2. Run `clk` at 1 MHz and pulse `rst` for at least one clock: pulse timing 200 / 10 (10 µs pulses at
   5 kHz), inputs off (`in = 00`), no pulses pending. Until this reset the input enable register is
   in an arbitrary state, so apply it right after power-up.
3. Write all 10 weight / sign registers (addresses 0–9).
4. Then write the input enables (register 14).

Between test cases, write `in = 00` (register 14) and wait at least 8 ms: the neurons have no
membrane reset, and the leak needs about 8 ms to empty any membrane. A mid-run `rst` keeps the
weights (no reload needed) and also stops the input pulses (it clears `in`), but it does not empty
the membranes: the 8 ms wait still applies.

## 6. Interface issues resolved (kept for reference)

The four open issues listed here up to 2026-11-18 are resolved: the digital block is timed at 3.3 V
(no level shifters); `Iref` and `VT` are chip ports (`ANALOG_PINS`) routed to the macro; the committed
layout is the current RTL (`results/`, run `RUN_2026-11-21_22-31-59`); and the macro sits flipped (FS)
at the bottom of the die with its pins facing the logic.
