# Digital Blocks

The digital part of the chip, as one module, `snn_digital`: the register map
and the input pulse generator. It takes the chip's digital pins and produces
what the analog macro needs (`w`, `s`, `pulse`). It has no dependency on
the analog side: the neuron spikes go straight to the chip's output pins, so
the digital logic can be simulated, linted and synthesized without it.

The chip top, `../snn_top.v`, only wires `snn_digital` to `snn_analog`.

## `regs` (register map)

- **Ports:** `clk`, `rst`, `addr[3:0]`, `data[3:0]` → `weights[31:0]`,
  `signs[7:0]`, `period[7:0]`, `width[7:0]`.
- There is no `wren` pin: `addr = 4'hF` is idle, and any other address writes
  `data` on every rising clock edge.

| addr | register | reset |
|---|---|---|
| 0–7 | weight magnitudes, synapses 0–7 | none |
| 8, 9 | signs of synapses 3–0, 7–4 | none |
| 10, 11 | pulse PERIOD [3:0], [7:4] | 200 |
| 12, 13 | pulse WIDTH [3:0], [7:4] | 10 |
| 14 | unused | |
| 15 | **idle**: no write | |

- **Write protocol:** rest at `addr = 1111` (with pad pull-ups, an undriven bus
  is idle). Set `data`, then set `addr` for one clock, then return to 1111.
  Change `data` only while idle: data that changes while an address is held
  does get written.
- Synapse k has magnitude `weights[4k+3:4k]` (0–15) and sign `signs[k]`
  (1 = inhibitory), as the `SNN_signed` macro takes them (map from
  `../mock/snn_analog.v`):
  - k = 0–1: input pulse generator i → input neuron i (inhibitory = off)
  - k = 2–5: input i → hidden j (k = 2 + 2j + i)
  - k = 6–7: hidden j → output (k = 6 + j)
- `rst` resets only the pulse timing, so the chip runs with the default timing
  before anything is written. Weights and signs must be written before use.

## `pulse_gen` (input pulse generator)

- **Ports:** `clk`, `rst` (synchronous, active high), `period[7:0]`,
  `width[7:0]`, `en[1:0]` → `pulse[1:0]`.
- Two channels share one counter. Each period, a channel whose `en` bit was
  high at the end of the previous period outputs a pulse of `width` cycles.
  `en`, `period` and `width` are sampled only at period boundaries, so a pulse
  is never cut or stretched; the first pulse can start up to one period after
  `en` rises.
- `period = 0` means 256 cycles; `width = 0` means no pulses.
- Outputs come straight from flip-flops, since they drive the analog DAC enables.
- At a 1 MHz `clk` the reset values give the 10 µs pulses every 200 µs (5 kHz)
  that `../analog/neuron/old/DACs-DPI-neuron.sch` is tuned for.
- The chip's package exposes `in[1:0]` (these `en` bits), not `pulse[1:0]`.

## `snn_digital`

- **Ports:** `clk`, `rst`, `data[3:0]`, `addr[3:0]`, `in[1:0]` → `w[31:0]`,
  `s[7:0]`, `pulse[1:0]`.
- The chip's pins are `clk`, `rst`, `data`, `addr`, `in` and `out` (17), plus
  the analog references and supplies (which are not Verilog signals).

## Test

From this folder:

```bash
iverilog -g2012 -Wall -o sim.vvp tb_snn_digital.v snn_digital.v regs.v pulse_gen.v && vvp sim.vvp
```

`tb_snn_digital.v` (9 checks): reset values, weights and signs, the unused
and idle addresses write nothing, the data-change rule, pulse timing changes
(taking effect only from the next period, `width = 0` = no pulses), and `en`
(`in`) sampled only at period boundaries (a late `en` waits for the next one; a
dropped `en` lets the current pulse finish). The whole chip is covered by
`../mock/tb_snn_top.v` and `../mixed/`.
