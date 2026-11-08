# Mixed-signal simulation of snn_top (digital rf + analog 3-5-1 network)

## Context
`snn_top.v` today is fully behavioural: `rf` (digital) drives `analog/mock/snn.v`
(Verilog stand-ins for DAC, neuron, comparator, pulse_gen). Real analog blocks now
exist in `analog/neuron/`: `DAC.sym` (w[3:0], branch weights 1:2:3:4, `en` pin,
15 nA unit), `DPI.sym` (synapse, Isum → Isyn) and `neuron_sized.sym`, already proven
as a chain in `DACs-DPI-neuron.sch` (entries 46–48 of `analog/Analog_AI_Documentation.md`).
Goal: an ngspice mixed-signal run where every mock block that has an analog version
is replaced by it (DAC, DPI+neuron replace mock dac/neuron/comparator), while `rf`
and `pulse_gen` stay digital (Verilator `d_cosim`). User decisions:
- Step 1: change the digital mock to mimic the analog DAC (4-bit, 1:2:3:4) and update tbs.
- `pulse_gen` stays Verilog inside the co-sim block.
- The analog network is an xschem schematic; digital is pulled in via a code block (CAD7 style).

Lessons from `feedback.typ` / CAD7 ([mgyee/engn1600-team1](https://github.com/mgyee/engn1600-team1)) to design around:
- vlnggen reorders pins → always build the `d_cosim` line from `<mod>_obj_dir/inputs.h|outputs.h` (reuse CAD7 `instantiate.py`).
- Several `.model d_cosim` were unstable → exactly ONE Verilog wrapper / one `.so`.
- Duplicate subckt names silently collapse → check netlist for duplicate `.subckt` names.
- xschem CLI netlisting is cwd-sensitive → always run from project root with project `xschemrc`; grep netlist for `IS MISSING` and unnamed `net\d+` on block pins (entries 43/44/47).
- XSPICE vector syntax uses `[ ]` → digital port nodes must not contain brackets.

## Step 1 — Mock follows the analog weight format (4-bit, 1:2:3:4)
- `analog/mock/dac.v`: `weight[3:0]`; branch weights are parameters `BW0..BW3` (default 1, 2, 3, 4 to match `DAC.sch`); `current = active ? (BW0·w0 + BW1·w1 + BW2·w2 + BW3·w3) * GAIN : 0`; param check `(BW0+BW1+BW2+BW3)*GAIN <= 65535`. Comment that with 1:2:3:4 the 16 codes give 11 distinct weights, and that 1:2:4:8 (planned) gives 16.
- Pass `BW0..BW3` up through `snn.v` and `snn_top.v` (defaults 1,2,3,4) so a testbench can pick either scheme with `-P`. The analog `DAC.sch` stays 1:2:3:4 for now (its `m=` values are numeric; parameter expressions would break LVS, per `feedback.typ`); the mixed-signal flow uses the default.
- `analog/mock/snn.v`: `W = 4`, `weights[23*4-1:0]`; update word-map comment.
- `digital/rf.v`: default `WIDTH = 4`.
- `snn_top.v`: `data[3:0]`, `weights[23*4-1:0]`, `rf #(.WIDTH(4))`.
- `tb_snn_top.v`: 4-bit `data`, `ws[91:0]`, word w = w mod 16 pattern, max weight = `4'hF`; same 4 scenarios/expectations. Re-check timing assumptions still hold (max per-cycle current 160 vs 112 before).
- `analog/mock/tb_neuron.v`: exhaustive dac check over `{active, weight[3:0]}` against the parameterized formula.
- Docs: `digital/README.md` (rf defaults, 23 × 4), `tb_snn_top.json` untouched.
- Verify: iverilog `tb_neuron`, `tb_pulse_gen`, `tb_snn_top` all PASS with the default 1:2:3:4 and again with `-P…BW2=4 -P…BW3=8`; `verilator --lint-only -Wall` on changed RTL.

## Step 2 — Digital co-sim block (`mixed/`)
New folder `mixed/` at the repo root.
- `mixed/snn_digital.v` — the single co-sim top (one `.so`). Contains `rf` (`../digital/rf.v`), 3× `pulse_gen` (`../analog/mock/pulse_gen.v`) and `snn_sequencer.v`.
  - Inputs: `clk`, `clk_analog`, `spike[8:0]` (analog neuron outputs, via ADC bridges).
  - Outputs: `w0..w91` (rf weight bits, flat names), `pulse0..2`, debug `scen`, `running`.
- `mixed/snn_sequencer.v` — test sequencer and checker; clocked (no `#` delays) replay of `tb_snn_top`'s 4 scenarios: write the 23 words through `data/addr/wren`, idle gap with weights 0 so DPI/VMEM decay (no analog reset pin exists), enable `in` for RUN `clk_analog` cycles, OR `spike` into `seen`, compare with expected set, `$display` per-scenario PASS/FAIL and a final summary.
- Timing: `clk_analog` period 10 µs with `PULSE_WIDTH=1`, `PULSE_PERIOD=20` → 10 µs pulses every 200 µs, matching `DACs-DPI-neuron.sch`. `clk` ≈ 1 µs (23-word load ≈ 46 µs). RUN ≈ 3 ms per scenario + ≈ 2 ms gap (estimate from entry 46: weight 10 fires on input 2, ~1.1 inputs/output) → ≈ 20 ms total. A `SCEN` parameter allows running a single scenario.
- `mixed/instantiate.py` — adapted from `../archive/engn1600-team1/CAD7/instantiate.py`: parse headers, emit the one `a… d_cosim` line with digital node names `d_<port><bit>`, `.model … simulation="<abs path>.so"` (path from Makefile, not hardcoded), explicit `adc_bridge`/`dac_bridge` models (0/3.3 V, ~10 ns edges, ADC thresholds ≈ 1.0/2.3 V) and bridge instances mapping `d_w5` ↔ analog net `w[5]` etc. (if bracketed analog names break the bridge vector syntax, link through 0 V sources from flat-named nodes).
- `mixed/Makefile` — adapted CAD7 targets: `snn_digital.so` (deps: all `.v`), `lib.spice`, netlist (`cd <root> && xschem -n -q -o mixed/ …`), `run` (`ngspice -b`, then `raw2vcd.py`), `clean`. Tools via `/foss/tools/bin`.
- `mixed/raw2vcd.py` — copy from CAD7 (check `vcd` Python module is installed).
- Smoke test first: tiny netlist with the `.so`, a few bridged pins and a resistor load → confirm pin order, 3.3 V levels, spike readback, `$display` output.

## Step 3 — Analog network schematic
- `analog/snn/snn_analog.sch` / `.sym` (new folder: it is a purely analog block, but a network, not a neuron part; the testbench stays in `mixed/`). Symbols referenced as `analog/neuron/DAC.sym` etc., which resolve via the root `xschemrc` when xschem starts from the project root; add `analog/snn` to `XSCHEM_LIBRARY_PATH` in `xschemrc` so bare references work too. Name distinct from Verilog `snn`.
  - 3 input sections: DAC (`en` = `pulse[i]`, `w` = word i) → DPI → `neuron_sized`.
  - 5 hidden: 3 DACs each (`en` = input spike i, word 3+3j+i) on one DPI `Isum` → neuron.
  - 1 output: 5 DACs (`en` = hidden spike j, word 18+j) → DPI → neuron.
  - Ports: `VDD VSS w[91:0] pulse[2:0] spike[8:0]` + shared biases `Vb Vthr VT_dpi VNA Vlk VK VIp VKup VKdn Vamp_bias VT`.
  - Use xschem instance arrays + bus labels where they netlist cleanly; DPI `Isyn` → neuron `VMEM` directly.
- Written as plain-text `.sch`, verified by headless netlisting from the project root: no `IS MISSING`, no unnamed nets on DAC/DPI/neuron pins, no duplicate `.subckt` names, expected instance counts (23 DAC, 9 DPI, 9 neuron_sized).

## Step 4 — Top testbench
- `mixed/snn_ms_tb.sch`: `snn_analog.sym`; VDD/VSS; bias sources and `Iref`/`Mref` Vb reference copied from `DACs-DPI-neuron.sch` (vthr 2.909, vtau 0.40, iref 14.42n, neuron biases); clock PULSE sources; MODELS block incl. `mimcap_typical`; code block `.include lib.spice`; control: `.options method=gear`, op-point start (no `uic`, per entry 46), `tran` with ≤0.5 µs max step, `save` only spikes/VMEMs/Isyn/pulses/weights, `write snn_ms_tb.raw`.
- If scenario 3 (in1→hid2→out at max weight) fails to propagate, tune per-layer DPI `Vthr` (allowed as separate pins) and record values; neuron spikes have slower edges than the ideal en pulses (entry 48 limitation).

## Step 5 — Docs
- `mixed/README.md`: flow, Makefile targets, file tree (like the CAD7 tables), known pitfalls.
- Root `README.md` TODO updates; new entry in `analog/Analog_AI_Documentation.md` (team logs AI work there); note in `digital/README.md`.

## Verification
1. Step 1: `iverilog -g2012 -Wall …` for `tb_neuron`, `tb_pulse_gen`, `tb_snn_top` → PASS.
2. Smoke test of `d_cosim` + bridges (pin order, levels).
3. Headless netlist checks of `snn_analog` / `snn_ms_tb` (missing symbols, unnamed nets, duplicate subckts).
4. `make -C mixed run` (background; may take tens of minutes): Verilog checker prints PASS for all 4 scenarios; `snn_ms_tb.vcd` opens in gtkwave showing weights, pulses, VMEMs, spikes.
5. Report runtime, first-fire times per layer, and any tuning done.

## Changes during implementation (2026-11-08)
- Step 1: weights are binary 1:2:4:8 in the mock (user request), not parameterized `BW0..BW3`; `DAC.sch` is still 1:2:3:4.
- `snn_stim.v` became `snn_sequencer.v`; the network is in `analog/snn/`, not `analog/neuron/`.
- `ngspice vlnggen` replaced by `mixed/vlnggen.sh` (ngspice-46 lowercases its Verilator command).
- The 92-bit weight port is split into `w_at0/23/46/69` (the d_cosim shim handles at most 31 bits per port).
- Testbench `.param`s are prefixed `p_` (a param named like a net disconnected the biases).
- The `d_cosim` flow (Steps 2 and 4) was later replaced by SpiceBind: `mixed/snn_ms_tb.v` replaces `snn_digital.v`, `snn_sequencer.v`, `vlnggen.sh` and `instantiate.py`.
- `mixed/raw2vcd.py` was replaced by xschem's `rawtovcd`.
- See `mixed/README.md` for results and limitations.
