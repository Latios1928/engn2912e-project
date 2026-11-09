# Digital Blocks

Synthesizable Verilog in this folder and how it fits into the SNN.

Last updated: 2026-11-08

## `rf` (weight register file)

- **Used in:** `../snn_top.v` (`u_rf`) and `../mixed/snn_ms_tb.v`.
- **Parameters:** `NUM_WORDS = 23`, `WIDTH = 4`, `AW = clog2(NUM_WORDS)`.
- **Ports:** `clk`, `wren`, `addr[AW-1:0]`, `data[WIDTH-1:0]` → `weights[NUM_WORDS*WIDTH-1:0]`.
- Writes `data` to word `addr` on the rising edge while `wren` is high. Writes to addresses ≥ NUM_WORDS are ignored.
- Word `w` is at `weights[w*WIDTH +: WIDTH]`; every word is visible at once.
- **No reset**: every word must be written before it is used.
- The defaults match the 3-5-1 SNN's 23 synapses, each with a 4-bit binary weight (map from `../analog/mock/snn.v`):
  - words 0–2: input pulse generator i → input neuron i
  - words 3–17: input i → hidden j (word 3 + 3j + i)
  - words 18–22: hidden j → output (word 18 + j)

Weights are loaded directly through `data`/`addr`/`wren`. With 9 neurons and 23
weights, pin serialization or an SRAM isn't needed.

## Test and lint

`rf` has no dedicated testbench; `../tb_snn_top.v` covers it, including an
out-of-range write. From the repo root:

```bash
iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp digital/rf.v analog/mock/*.v snn_top.v tb_snn_top.v && vvp sim.vvp
```

The `analog/mock/*.v` glob also picks up the mock testbenches, but `-s tb_snn_top` selects the top.

Open item: a unit testbench for `rf` (back-to-back writes).
