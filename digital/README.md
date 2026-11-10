# Digital Blocks

The digital part of the chip, as one module, `snn_digital`: the weight register
file and the input pulse generator. It takes the chip's digital pins and
produces what the analog network needs (`w`, `pulse`). It has no dependency on
the analog side: the neuron spikes go straight to the chip's output pins, so
the digital logic can be simulated, linted and synthesized without it.

The chip top, `../snn_top.v`, only wires `snn_digital` to `snn_analog`.

## `rf` (weight register file)

- **Used in:** `snn_digital.v` (`u_rf`).
- **Parameters:** `NUM_WORDS = 23`, `WIDTH = 4`, `AW = clog2(NUM_WORDS)`.
- **Ports:** `clk`, `wren`, `addr[AW-1:0]`, `data[WIDTH-1:0]` → `weights[NUM_WORDS*WIDTH-1:0]`.
- Writes `data` to word `addr` on the rising edge while `wren` is high. Writes to addresses ≥ NUM_WORDS are ignored.
- Word `w` is at `weights[w*WIDTH +: WIDTH]`; every word is visible at once.
- **No reset**: every word must be written before it is used.
- The defaults match the 2-2-1 SNN's 8 synapses, each with a 4-bit binary weight (map from `../mock/snn_analog.v`):
  - words 0–1: input pulse generator i → input neuron i
  - words 2–5: input i → hidden j (word 2 + 2j + i)
  - words 6–7: hidden j → output (word 6 + j)

Weights are loaded directly through `data`/`addr`/`wren`. With 5 neurons and 8
weights, pin serialization or an SRAM isn't needed.

## `snn_digital`

- **Parameters:** `PULSE_PERIOD = 200`, `PULSE_WIDTH = 10` (passed to `pulse_gen`).
- **Ports:** `clk`, `rst`, `data[3:0]`, `addr[2:0]`, `wren`, `in[1:0]` →
  `w[31:0]`, `pulse[1:0]`.
- `rf` holds the weights (`w` is its `weights` bus) and `pulse_gen` turns `in`
  into `pulse`. `w` and `pulse` are the inputs of `snn_analog`; its `spike[4:0]`
  output goes straight to the chip's `out` pins in `../snn_top.v`.
- The chip's pins are `clk`, `rst`, `data`, `addr`, `wren`, `in` and `out`, plus
  the analog biases and supplies (which are not Verilog signals).

## `pulse_gen` (input pulse generator)

- **Parameters:** `PERIOD = 200`, `WIDTH = 10` (in `clk` cycles).
- **Ports:** `clk`, `rst` (synchronous, active high), `en[1:0]` → `pulse[1:0]`.
- Two channels share one counter. Each period, a channel whose `en` bit was
  high at the end of the previous period outputs a pulse of exactly `WIDTH`
  cycles. `en` is sampled only at period boundaries, so a pulse is never cut
  short; the first pulse can start up to `PERIOD` cycles after `en` rises.
- Outputs come straight from flip-flops, since they drive the analog DAC enables.
- At a 1 MHz `clk` the defaults give the 10 µs pulses every 200 µs (5 kHz) that
  `../analog/neuron/DACs-DPI-neuron.sch` is tuned for. For another clock, set
  `PERIOD` and `WIDTH` to the same times in cycles.
- It needs a reset, so the chip has a `rst` pin; `rf` and the analog network
  have none.
- The chip's package exposes `in[1:0]` (these `en` bits), not `pulse[1:0]`: the
  pulse timing is fixed on chip, and `pulse` is an internal net between this
  block and `snn_analog`.

## Test

`tb_pulse_gen.v` checks `pulse_gen` against a reference model written from the
spec, with random `en` changes and a mid-run reset. `rf` and `snn_digital` are
covered by `../mock/tb_snn_top.v` (including a readback of every `rf` word) and
by `../mixed/`. From this folder:

```bash
iverilog -g2012 -Wall -o sim.vvp pulse_gen.v tb_pulse_gen.v && vvp sim.vvp
```

Other shapes: add `-Ptb_pulse_gen.PERIOD=1 -Ptb_pulse_gen.WIDTH=1` and the like.

Open item: a unit testbench for `rf` (back-to-back writes).
