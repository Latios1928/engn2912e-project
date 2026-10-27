# Digital Blocks

Summary of the synthesizable Verilog in this folder: what each module does,
how it's tested, current test status, and how it fits into the SNN.

Last updated: 2026-10-26

---

## Overview

| Module | File | Purpose | Testbench | Used in `snn_top.v`? |
|---|---|---|---|---|
| `rf` | `rf.v` | Weight register file: one write port, all words read in parallel | via `../tb_snn_top.v` | **Yes** (`u_rf`) |
| `serializer_tdm` | `serializer_tdm.v` | Time-division serializer: N parallel bits → K pins over N/K cycles | `tb_serializer_tdm.v` | No |
| `deserializer_tdm` | `deserializer_tdm.v` | Exact inverse of `serializer_tdm`: K pins → N-bit word | `tb_deserializer_tdm.v` | No |
| `sram_weight_loader` | `sram_weight_loader.v` | Reads NUM_WEIGHTS words from a 1-cycle-latency SRAM into a flat weight bus | `tb_sram_weight_loader.v` | No |

All modules use a single rising-edge clock and a **synchronous, active-high
reset** (`rf` has no reset, like an SRAM).

---

## Modules

### `rf` (weight register file)
- **Parameters:** `NUM_WORDS = 23`, `WIDTH = 3`, `AW = clog2(NUM_WORDS)`.
- **Ports:** `clk`, `wren`, `addr[AW-1:0]`, `data[WIDTH-1:0]` → `weights[NUM_WORDS*WIDTH-1:0]`.
- Writes `data` to word `addr` on the rising edge while `wren` is high. Writes to addresses ≥ NUM_WORDS are ignored.
- Word `w` is at `weights[w*WIDTH +: WIDTH]`; every word is visible at once.
- **No reset**: every word must be written before it is used.
- The defaults match the 3-5-1 SNN's 23 synapses, each with a 3-bit weight (map from `../analog/mock/snn.v`):
  - words 0–2: input pulse generator i → input neuron i
  - words 3–17: input i → hidden j (word 3 + 3j + i)
  - words 18–22: hidden j → output (word 18 + j)

### `serializer_tdm` (time-division serializer)
- **Parameters:** `N = 8` input bits, `K = 2` output pins (K must divide N); `T = N/K` cycles per frame.
- **Ports:** `clk`, `rst`, `in[N-1:0]` → `out[K-1:0]`, `frame_start`.
- On the edge where the counter wraps, captures `in` into K shift registers of T bits each. Each lane shifts out LSB first: `out[k]` carries `in[k*T]`, `in[k*T+1]`, …, `in[k*T+T-1]`.
- Frames follow each other with no idle cycle in between. `frame_start` is high on the first cycle of each frame.
- Spec: `../specifications/serializer_tdm.txt`.

### `deserializer_tdm` (time-division deserializer)
- **Parameters:** `N = 8`, `K = 2` (K must divide N); `T = N/K`.
- **Ports:** `clk`, `rst`, `in[K-1:0]` → `out[N-1:0]`, `frame_done`.
- Each lane shifts new bits in at the MSB side, so after T cycles lane k holds the first bit it received in bit 0 and the last in bit T-1. This exactly reverses `serializer_tdm`: chaining the two with the same N and K reproduces the original word.
- `out` always shows the live shift-register contents. It is only a complete word during the cycle `frame_done` is high.

### `sram_weight_loader` (SRAM → weight bus)
- **Parameters:** `NUM_WEIGHTS = 16`, `WEIGHT_WIDTH = 8`, `AW = clog2(NUM_WEIGHTS)`.
- **Ports:** `clk`, `rst`, `start` → `busy`, `done`, `sram_addr`, `sram_ren`; `sram_rdata` in; `weights[NUM_WEIGHTS*WEIGHT_WIDTH-1:0]` out.
- A `start` pulse (ignored while busy) issues addresses 0 … NUM_WEIGHTS-1, one per cycle. Each word is captured one cycle after its address is issued, to match the SRAM's read latency.
- `done` pulses for one cycle after the last word is captured. `busy` is high from `start` until then. A reset in the middle of a load aborts it.

---

## Test status

Run on 2026-10-26 with Icarus Verilog (`iverilog -g2012`):

| Testbench | Configurations | Result |
|---|---|---|
| `tb_serializer_tdm` | N/K = 8/2 (default), 12/4, 8/8, 8/1, 6/3 | **PASS** (200 checks each) |
| `tb_deserializer_tdm` | N/K = 8/2 (default), 12/4, 8/8, 8/1, 6/3 | **PASS** (200 checks each) |
| `tb_sram_weight_loader` | 16×8 (default), 23×3 (SNN size), 1×8 | **PASS** (5 checks each) |
| `../tb_snn_top` (covers `rf`) | default | **PASS** (5 checks) |

How the testbenches work:
- **serializer / deserializer:** `in` is randomized every cycle. A reference model is checked on every cycle (including partly filled frames), and a reset is applied once in the middle of a frame.
- **sram_weight_loader:** a behavioural SRAM is filled with new random data on each pass. The test runs 6 load passes; one is aborted by a mid-load reset, and the next pass checks that the loader recovered.

Commands (from this folder):

```bash
iverilog -g2012 -Wall -o sim.vvp serializer_tdm.v tb_serializer_tdm.v && vvp sim.vvp
```
```bash
iverilog -g2012 -Wall -o sim.vvp deserializer_tdm.v tb_deserializer_tdm.v && vvp sim.vvp
```
```bash
iverilog -g2012 -Wall -o sim.vvp sram_weight_loader.v tb_sram_weight_loader.v && vvp sim.vvp
```

Other sizes: add `-Ptb_<module>.N=12 -Ptb_<module>.K=4` (or `.NUM_WEIGHTS=`, `.WEIGHT_WIDTH=`).

`rf` / full system (from the repo root):

```bash
iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp digital/rf.v analog/mock/*.v snn_top.v tb_snn_top.v && vvp sim.vvp
```

---

## Lint (`verilator --lint-only -Wall`)

| File | Result |
|---|---|
| `rf.v` | Clean |
| `sram_weight_loader.v` | Clean |
| `serializer_tdm.v` | 1 width warning: `assign frame_start = !cnt;` (line 38) applies `!` to a multi-bit counter. Behaviour is correct (`!cnt` is `cnt == 0`); writing `cnt == 0` would silence it. |
| `deserializer_tdm.v` | 1 width warning: `in[k] << (T - 1)` (line 52) shifts a 1-bit value. Simulation is correct because the result widens to fit the OR, but `{in[k], {(T-1){1'b0}}}` would make the width explicit and is safer for synthesis. |

---

## Notes and open items

1. **Two ways of loading weights, only one connected.** `snn_top` loads
   weights through `rf` (data/addr/wren). `sram_weight_loader` and the TDM
   serializer and deserializer are standalone and not yet instantiated
   anywhere. Decide whether the chip's weight input path is:
   - pins → `deserializer_tdm` → `rf` writes,
   - SRAM → `sram_weight_loader` (replacing `rf`), or
   - `rf` driven directly, as now.
2. **Size mismatch.** `sram_weight_loader` defaults to 16 × 8-bit words.
   The SNN needs 23 × 3-bit words (`rf` defaults). The loader passes at
   23 × 3, so this is only a matter of parameters.
3. **`rf` has no dedicated testbench.** It is only covered by `tb_snn_top`.
   A small unit test would cover writes to out-of-range addresses and
   back-to-back writes.
4. **A test gap in `tb_sram_weight_loader`.** The comment says the aborted
   pass confirms there is no false `done`, but the testbench never checks
   that `done` stays low during that pass. It only checks that the next
   pass recovers.
5. **`deserializer_tdm` with T = 1 (K = N).** The counter is always at its
   last value, so `frame_done` is high all the time, even during reset.
   This is harmless, but worth knowing if `frame_done` gates anything.
