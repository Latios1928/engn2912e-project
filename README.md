# ENGN 2912E Final Project

## Layout

| Path | Contents |
|---|---|
| `analog/` | Analog modules: `neuron/` (DAC, DPI, neuron, testbenches), `snn/` (the 3-5-1 network), `testbenches/` |
| `digital/` | The digital part of the chip: `snn_digital.v` (`rf.v`, `pulse_gen.v`) |
| `snn_top.v` | Chip top: wires `digital/snn_digital.v` to `snn_analog`, which each build supplies |
| `mock/` | Behavioral `snn_analog` (and its DAC/neuron mocks) and the pure-digital end-to-end test of `snn_top` |
| `mixed/` | The same end-to-end test with the transistor-level `snn_analog` |
| `librelane/` | Physical design of the whole chip (`snn_top`, with `snn_analog` as a hard macro); reads `digital/` and `analog/` only |
| `specifications/` | Specs given to the AI, and how it is used |

## TODO

### Analog
- [ ] Neuron reset only pulls MEM down to ~0.74–1.01 V instead of `reset_bias` (0.2 V): the reset stops as soon as the comparator flips back. Hold the reset for a fixed time (one-shot or SR latch). See [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md).
- [ ] Number of input pulses per fire varies because the reset level varies; recheck once the reset is fixed.
- [ ] Finish [tools/analog_API_infrastructure/advisor.py](tools/analog_API_infrastructure/advisor.py): it does not run yet (`os.enrivon`, `tuple{`, missing commas in the JSON schema, wrong body in `meets_spec`).

### Mixed-signal ([mixed/README.md](mixed/README.md))
- [ ] Calibrate the behavioral `snn_analog` in `mock/` (clock period, `GAIN`, `DURATION`, `LEAK`) so first-spike timing is close to the analog results, if the mock should be quantitatively comparable.
- [ ] The analog network has no reset: membranes keep 1.0–1.2 V after a 2 ms settle, so scenario latencies depend on the previous one. Add a reset (switch on VMEM) or lengthen `SETTLE`.
- [ ] Resize [analog/neuron/DAC.sch](analog/neuron/DAC.sch) to binary 1:2:4:8 (m = 4 and 8 on the last two branches) so it matches the mock.
- [ ] Add scenarios with intermediate weights once the DAC is binary; run corners.

### Digital
- [ ] Pick the chip clock frequency. `pulse_gen`'s defaults (`PERIOD` 200, `WIDTH` 10) assume a 1 MHz `clk` for 10 µs pulses every 200 µs; a faster clock needs larger values and a wider counter.
- [ ] Add a unit testbench for `rf` (back-to-back writes; out-of-range writes are already covered by `tb_snn_top`).

### Physical design
- [ ] Build the whole chip with LibreLane, with `snn_analog` as a hardened macro: [librelane/snn_top/config.json](librelane/snn_top/config.json) lists the Verilog of `snn_top` and `digital/` but has no macro yet and cannot run. The macro needs, as in lab 3's `librelane/macros.yaml`: GDS and LEF from the analog layout, a Verilog black-box header, a liberty file (hand-written for an analog block), and a placement location; plus its supply and bias pins and a pad-ring top like lab 3's `chip_top`. The checked-in `results/` are from the old design (3-bit weights, mock network synthesized as gates); replace them, and recheck the 57 max-slew violations.

### Docs
- [ ] Remove the stale housekeeping item (5) from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md): the move to `analog/neuron/` is already committed.
- [ ] Fill in the timeline and division of responsibilities above.
