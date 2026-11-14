# Pin list: final top level

Chip top `snn_top.v` = digital `snn_digital` (LibreLane, `librelane/snn_top`) + analog macro `SNN`
(`analog/neuron/layout/SNN.gds`, schematic `analog/snn/snn_analog_inh.sch` + bias cell).
Status 2026-11-12. Sources: `snn_top.v`, `digital/snn_digital.v`, `analog/neuron/layout/SNN_pins.json`.

## 1. Chip pins (external)

| Pin | Dir | Domain | Width | Function | Connects to |
|---|---|---|---|---|---|
| `clk` | in | digital | 1 | system clock (config: 20 ns period) | digital: `rf`, `pulse_gen` |
| `rst` | in | digital | 1 | synchronous reset, active high (pulse generator only) | digital: `pulse_gen` |
| `data[3:0]` | in | digital | 4 | weight word to write | digital: register file |
| `addr[2:0]` | in | digital | 3 | weight word address (word k = synapse k, see §3) | digital: register file |
| `wren` | in | digital | 1 | write enable for `data` → word `addr` | digital: register file |
| `in[1:0]` | in | digital | 2 | enables input pulse channel i (PULSE_PERIOD 200, PULSE_WIDTH 10 clk cycles) | digital: `pulse_gen` |
| `out[4:0]` | out | analog → pin | 5 | spikes `{output, hidden[1:0], input[1:0]}`, full-swing 0 … VDD, ≈ 9–13 µs pulses | analog `spike[4:0]` |
| `Iref` | in (current) | analog | 1 | bias-cell reference current, **100 nA sourced into the pin** (scales every bias) | analog `Iref` |
| `VT` | in (voltage) | analog | 1 | neuron firing threshold, **1.66 V** (high-impedance gate input) | analog `VT` |
| `VDD` | supply | analog (+ digital, see §4) | 1 | 3.3 V | analog `VDD`; digital VDD |
| `VSS` | supply | ground | 1 | 0 V, substrate | analog `VSS`; digital VSS |

Total: 15 signal pins (`clk`, `rst`, 4 + 3 + 1 + 2 digital inputs, 5 outputs) + `Iref` + `VT` + supplies.
The 11 analog biases (Vb, Vthr, VT_dpi, VT_inh, VNA, Vlk, VK, VIp, VKup, VKdn, Vamp_bias) are internal:
the bias cell inside `SNN` makes them from `Iref`.

## 2. Internal top-level nets (digital ↔ analog macro)

| Net | Width | From → To | Notes |
|---|---|---|---|
| `w[31:0]` | 32 | `snn_digital.w` → `SNN.w[31:0]` | 8 weight words, word k = `w[4k+3:4k]`, static while running |
| `pulse[1:0]` | 2 | `snn_digital.pulse` → `SNN.pulse[1:0]` | input spike trains, gate the input-layer DAC enables |
| `spike[4:0]` | 5 | `SNN.spike[4:0]` → chip `out[4:0]` | no logic in between (`snn_top.v`) |
| `s[1:0]` | 2 | **not driven** → `SNN.s[1:0]` | sign of the two hidden → output synapses (1 = inhibitory); see §5 |

## 3. Analog macro `SNN` pins (285.14 × 547.04 µm, all on the bottom edge)

| Pin(s) | Layer | x on the bottom edge (µm) | Width (µm) |
|---|---|---|---|
| `Iref` | Metal3 | 1.20 | 0.4 |
| `VDD` | Metal3 | 3.10 | 1.0 |
| `VSS` | Metal3 | 4.50 | 1.0 |
| `w[0]` … `w[31]` | Metal3 | 123.78 + 0.80·k (`w[31]` at 148.58) | 0.4 |
| `pulse[0]`, `pulse[1]` | Metal3 | 149.38, 150.18 | 0.4 |
| `s[0]`, `s[1]` | Metal3 | 154.28, 155.08 | 0.4 |
| `VT` | Metal3 | 201.58 | 0.4 |
| `spike[0]` … `spike[4]` | M1, M5, M3, M1, M5 | 280.54, 281.39, 282.24, 283.04, 283.89 | 0.4 / 0.5 (M5) |

Word / synapse map (as in `mock/snn_analog.v`; the layout's DACs use the same bit positions):

| Word | Bits | Synapse | DAC in the layout |
|---|---|---|---|
| 0, 1 | `w[3:0]`, `w[7:4]` | `pulse[i]` → input neuron i | xdac0_0, xdac1_0 |
| 2 … 5 | `w[23:8]` | input i → hidden j (word 2 + 2j + i) | xdac2_0 … xdac3_1 |
| 6, 7 | `w[27:24]`, `w[31:28]` | hidden j → output (signed) | xdac4_0, xdac4_1 (DAC_signed, sign `s[j]`) |

## 4. Supplies and domains

- Analog macro: 3.3 V devices only (`nfet_03v3`, `pfet_03v3`); VDD = 3.3 V, VSS = 0 V = substrate.
  The bias cell draws ≈ 0.72 µA; the five neurons ≈ 0.3–0.5 µW each.
- Digital (`librelane/snn_top/config.json`): cell library `gf180mcu_fd_sc_mcu7t5v0`, signed off at the
  **5 V** corners (`nom_tt_025C_5v00`, `ss_125C_4v50`). See §5.

## 5. Open interface issues (to resolve before the final top level)

1. **Supply voltage.** The digital block is timed at 5 V, the analog macro is 3.3 V. Driving `w`, `pulse`
   from a 5 V domain would put 5 V on 3.3 V gates (DAC switches, Men), and the 3.3 V spikes would not
   reach a 5 V logic high. Either run the digital block at 3.3 V (the library has 3v00 / 3v30 / 3v60
   corners) on the same VDD, or add level shifters.
2. **Weight encoding.** `mock/snn_analog.v` / `mock/dac.v` (and so the digital weight convention) use
   sign-magnitude words: bit 3 = sign, bits 2:0 = magnitude on 1:2:4 branches (−7 … +7). The layout uses
   `DAC_binary`: all four bits are magnitude on 1:2:4:8 branches (0 … 15), and the sign of the two
   output synapses is a separate input `s[1:0]`. One side has to change (e.g. drive `s[j]` from
   `w[24+4j+3]` and use 1:2:4 magnitude, or redefine the digital words).
3. **`s[1:0]` has no driver** in `snn_top.v` / `snn_digital.v` (the black box `analog/snn/snn_analog.v`
   has only `w`, `pulse`, `spike`). Needs a source: two more register bits, the sign bits of words 6/7,
   or chip pins.
4. **`Iref`, `VT`, `VDD`, `VSS`** of the analog macro are not ports of `snn_top.v` or of the black box;
   they must be added as chip pins / pads (analog pads for `Iref` and `VT`).
5. **The committed digital layout is out of date.** `librelane/snn_top/results/snn_top.gds`
   (307.4 × 325.3 µm) still has the earlier 3-5-1 interface (`addr[4:0]`, `data[2:0]`, `in[2:0]`,
   `out[8:0]`, `clk_analog`); re-run `librelane/snn_top/run.sh` on the current RTL.
6. **Pin placement.** All analog macro pins are on its bottom edge (Metal3, spikes on M1/M3/M5);
   the digital macro's `w`/`pulse` outputs should face it, and `out[4:0]` must reach the pads on a
   layer the pads accept.
