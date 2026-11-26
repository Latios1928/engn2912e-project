# Plan: Verilog model of a 3-5-1 spiking neural network

## Context
We need a simulatable Verilog model of a 3-5-1 spiking neural network (SNN). The original sketch is in the untracked file `specifications/mock.txt`.
- **Keep:** the digital parts (top level and weight storage) may end up in the final chip.
- **Placeholders:** the analog-mock modules (comparator, DAC, neuron, pulse generator, SNN) stand in for circuits that will later be analog. They are behavioral and clocked on `clk_analog`.

Decisions made while planning:
- **One weight per synapse.** That's 23 weights of 3 bits each: 3 pulse→input, 15 input→hidden and 5 hidden→output. Weights are unsigned, so every synapse is excitatory.
- **Inputs go through a pulse generator.** While `in[i]` is high, a new analog mock emits periodic pulses (PERIOD, WIDTH). Each pulse reaches input neuron i through a weighted DAC, so all 9 neurons are real.
- **Outputs:** `out[9]` is the `active` signal of all 9 neurons.
- **Weight storage is a register file named `rf`,** not an SRAM plus loader. The teammate's `digital/sram_weight_loader.v` would store every weight twice (SRAM plus 69 flip-flops), so it stays unused for now.
- **No pin multiplexing yet.** `serializer_tdm`/`deserializer_tdm` are left alone.

## Pin and parameter changes from the sketch
- `addr` grows from 4 to 5 bits (23 words). Writes to addresses 23–31 are ignored.
- `weights[3][9]` becomes a flat `weights[23*3-1:0]`, which matches how `sram_weight_loader.weights` is packed, in case we switch later.
- `voltage`/`current` are flattened buses (`[15:0]`, `currents[INDEGREE*16-1:0]`), because Verilog-2001 ports can't be 2-D.
- Add an `rst` input to top. It is synchronous to `clk_analog` and clears neuron voltages, comparator countdowns and pulse phases; without it the simulation starts at X. `rf` has no reset, like an SRAM, so the testbench writes every weight first.

## Weight address map (shared by `rf` and `snn`)
| addr | synapse |
|---|---|
| 0–2 | pulse[i] → input neuron i (addr = i) |
| 3–17 | input i → hidden j (addr = 3 + 3*j + i) |
| 18–22 | hidden j → output (addr = 18 + j) |

Grouping by postsynaptic neuron keeps each neuron's incoming weights contiguous. I'll document the map in a header comment in `snn.v` and `rf.v`.

## Files

### Digital (`digital/`)
- **`rf.v`, the weight register file.** Params `NUM_WORDS=23`, `WIDTH=3`, `AW=5`. Ports: `clk`, `wren`, `addr[AW-1:0]`, `data[WIDTH-1:0]`, `weights[NUM_WORDS*WIDTH-1:0]`. Writes are synchronous on `clk`, and all words are read out continuously in parallel.
- **`snn_top.v`, the top level.** Ports: `clk`, `clk_analog`, `rst`, `data[2:0]`, `addr[4:0]`, `wren`, `in[2:0]`, `out[8:0]`. It instantiates `rf` (on `clk`) and `snn` (on `clk_analog`), and passes `DURATION`, `THRESHOLD`, `GAIN`, `PULSE_PERIOD` and `PULSE_WIDTH` down. A header comment will note that `weights` and `in` cross from the `clk` domain to `clk_analog` with no synchronizer. That's acceptable in the model because weights are written before the network runs, but it's a known gap for silicon.

### Analog mocks (`analog/mock/`)
This new subfolder keeps behavioral Verilog apart from the xschem schematic folders.
- **`comparator.v`.** Params `DURATION`, `THRESHOLD`. If `voltage > THRESHOLD`, set `countdown <= DURATION`; otherwise decrement it, stopping at 0. `active = (countdown != 0)`. The countdown width is `$clog2(DURATION+1)`.
- **`dac.v`.** Param `GAIN`. `current = active ? weight * GAIN : 0`, computed at 16 bits through a `localparam [15:0]` gain so it lints cleanly.
- **`neuron.v`.** Params `INDEGREE`, `DURATION`, `THRESHOLD`. Each cycle: if `active`, set `voltage <= 0`; otherwise `voltage <= voltage + sum(currents)`, saturating at 16'hFFFF (a mock supply rail). The sum uses a wider accumulator so it can't overflow. It contains a `comparator`, and `active` is forwarded from it.
  - The comparator output is registered. So a neuron fires the cycle after its voltage crosses threshold, then stays active (and held at 0 V, which acts as a refractory period) for DURATION cycles.
- **`pulse_gen.v`.** Params `PERIOD`, `WIDTH`. A phase counter runs 0..PERIOD-1 while `en` is high and is held at 0 while `en` is low. `pulse = en && (phase < WIDTH)`, so a pulse starts immediately when `en` rises.
- **`snn.v`.** Params `DURATION`, `THRESHOLD`, `GAIN`, `PULSE_PERIOD`, `PULSE_WIDTH`. Ports: `clk_analog`, `rst`, `weights[68:0]`, `in[2:0]`, `out[8:0]`. Generate loops build:
  - **Input layer:** 3 `pulse_gen`s, 3 DACs, and 3 input neurons with `INDEGREE=1`.
  - **Hidden layer:** 15 DACs and 5 hidden neurons with `INDEGREE=3`.
  - **Output layer:** 5 DACs and 1 output neuron with `INDEGREE=5`.
  - `out = {output, hidden[4:0], input[2:0]}`.

Coding style follows `digital/serializer_tdm.v`: a header comment explaining behavior and timing, `parameter` checks in an `initial $error` block, `localparam` widths, `+:` part-selects, and synchronous active-high reset.

Starting defaults, tuned in the testbench so the full path actually fires: `GAIN=16`, `THRESHOLD=255`, `DURATION=4`, `PULSE_PERIOD=16`, `PULSE_WIDTH=2`.

### Testbenches
They follow the `digital/tb_serializer_tdm.v` style: drive on negedge, check outputs against expected values, and print PASS/FAIL.
- **`analog/mock/tb_neuron.v`.** Feed a constant current and check the exact cycle the neuron fires, the DURATION-long active window, the voltage reset, and saturation. This covers the comparator and DAC as well.
- **`analog/mock/tb_pulse_gen.v`.** Check the pulse spacing (PERIOD) and width (WIDTH), and the restart when `en` rises.
- **`digital/tb_snn_top.v`.** Write all 23 weights through `rf` and check the `weights` bus hierarchically. Then run these scenarios:
  1. `in = 0`: no neuron fires.
  2. Only the pulse→input weights are nonzero: only `out[2:0]` toggles, and only for inputs that are on.
  3. A full path (one input → one hidden → output) has max weights: that hidden neuron and `out[8]` fire, and the other hidden neurons stay quiet.
  4. Zeroing one hidden→output weight stops its contribution to the output.

## Verification
```sh
cd /foss/designs/engn2912e-project
F="digital/rf.v digital/snn_top.v analog/mock/{comparator,dac,neuron,pulse_gen,snn}.v"
iverilog -g2012 -Wall -o sim.vvp $F digital/tb_snn_top.v && vvp sim.vvp   # plus each unit TB
slang -Wconversion --top snn_top $F                                       # matches the editor's slang server
verilator --lint-only -Wall --top-module snn_top $F                       # stricter width checks
```
The goal is no warnings from slang `-Wconversion` and Verilator `-Wall` on the RTL, and PASS from all three testbenches.
