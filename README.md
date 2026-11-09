# ENGN 2912E Final Project

## Layout

| Folder | Contents |
|---|---|
| `analog/` | Analog modules: `neuron/` (DAC, DPI, neuron, testbenches), `snn/` (the 3-5-1 network), `testbenches/` |
| `digital/` | Digital modules that go into the chip (`rf.v`) |
| `mock/` | Behavioral mocks of the analog blocks, `snn_top.v`, and the pure-digital end-to-end test |
| `mixed/` | End-to-end test with as many analog modules as exist; the rest are Verilog |
| `librelane/` | Physical design of `snn_top` (digital mocks) |
| `specifications/` | Specs given to the AI, and how it is used |

## TODO

### Analog
- [ ] Neuron reset only pulls MEM down to ~0.74–1.01 V instead of `reset_bias` (0.2 V): the reset stops as soon as the comparator flips back. Hold the reset for a fixed time (one-shot or SR latch). See [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md).
- [ ] Number of input pulses per fire varies because the reset level varies; recheck once the reset is fixed.
- [ ] Finish [tools/analog_API_infrastructure/advisor.py](tools/analog_API_infrastructure/advisor.py): it does not run yet (`os.enrivon`, `tuple{`, missing commas in the JSON schema, wrong body in `meets_spec`).

### Mixed-signal ([mixed/README.md](mixed/README.md))
- [ ] The analog network has no reset: membranes keep 1.0–1.2 V after a 2 ms settle, so scenario latencies depend on the previous one. Add a reset (switch on VMEM) or lengthen `SETTLE`.
- [ ] Resize [analog/neuron/DAC.sch](analog/neuron/DAC.sch) to binary 1:2:4:8 (m = 4 and 8 on the last two branches) so it matches the mock.
- [ ] Add scenarios with intermediate weights once the DAC is binary; run corners.

### Digital
- [ ] Add a unit testbench for `rf` (back-to-back writes; out-of-range writes are already covered by `tb_snn_top`).

### Physical design
- [ ] Re-run LibreLane: the checked-in `snn_top` netlist and GDS in [librelane/snn_top/results/](librelane/snn_top/results/) predate the 4-bit weights (`data` is still 3 bits).
- [ ] Fix the 57 max-slew violations in the LibreLane run of `snn_top`. See [librelane/snn_top/](librelane/snn_top/).

### Docs
- [ ] Remove the stale housekeeping item (5) from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md): the move to `analog/neuron/` is already committed.
- [ ] Fill in the timeline and division of responsibilities above.
