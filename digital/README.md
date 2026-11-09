# Digital Blocks

Digital modules that go into the final chip. Today that is the weight register
file; the real chip top will be added here once the analog network exists.
The pure-digital end-to-end design (`snn_top.v`, with the behavioral mocks) is
in [../mock/](../mock/README.md).

## `rf` (weight register file)

- **Used in:** `../mock/snn_top.v` (`u_rf`) and `../mixed/snn_ms_tb.v`.
- **Parameters:** `NUM_WORDS = 23`, `WIDTH = 4`, `AW = clog2(NUM_WORDS)`.
- **Ports:** `clk`, `wren`, `addr[AW-1:0]`, `data[WIDTH-1:0]` → `weights[NUM_WORDS*WIDTH-1:0]`.
- Writes `data` to word `addr` on the rising edge while `wren` is high. Writes to addresses ≥ NUM_WORDS are ignored.
- Word `w` is at `weights[w*WIDTH +: WIDTH]`; every word is visible at once.
- **No reset**: every word must be written before it is used.
- The defaults match the 3-5-1 SNN's 23 synapses, each with a 4-bit binary weight (map from `../mock/snn_mock.v`):
  - words 0–2: input pulse generator i → input neuron i
  - words 3–17: input i → hidden j (word 3 + 3j + i)
  - words 18–22: hidden j → output (word 18 + j)

Weights are loaded directly through `data`/`addr`/`wren`. With 9 neurons and 23
weights, pin serialization or an SRAM isn't needed.

## Test

`rf` has no dedicated testbench; `../mock/tb_snn_top.v` covers it, including an
out-of-range write (see [../mock/README.md](../mock/README.md)).

Open item: a unit testbench for `rf` (back-to-back writes).
