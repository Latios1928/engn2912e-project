===== ENGN 2912E Final Project =====
Timeline/Division of Responsibilities 

## TODO

### Analog
- [ ] Neuron reset only pulls MEM down to ~0.74–1.01 V instead of `reset_bias` (0.2 V): the reset stops as soon as the comparator flips back. Hold the reset for a fixed time (one-shot or SR latch). See [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md).
- [ ] Number of input pulses per fire varies because the reset level varies; recheck once the reset is fixed.
- [ ] Finish [tools/analog_API_infrastructure/advisor.py](tools/analog_API_infrastructure/advisor.py): it does not run yet (`os.enrivon`, `tuple{`, missing commas in the JSON schema, wrong body in `meets_spec`).

### Digital
- [ ] Decide the weight-loading path: pins → `deserializer_tdm` → `rf`, SRAM → `sram_weight_loader`, or `rf` driven directly (current). `serializer_tdm`, `deserializer_tdm` and `sram_weight_loader` are not connected to `snn_top` yet.
- [ ] Add a unit testbench for `rf` (out-of-range addresses, back-to-back writes).
- [ ] `tb_sram_weight_loader`: check that `done` stays low during the aborted pass.
- [ ] Fix the two Verilator width warnings in `serializer_tdm.v` and `deserializer_tdm.v`. See [digital/README.md](digital/README.md).

### Physical design
- [ ] Fix the 57 max-slew violations in the LibreLane run of `snn_top`. See [librelane/snn_top/](librelane/snn_top/).

### Docs
- [ ] Remove the stale housekeeping item (5) from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md): the move to `analog/neuron/` is already committed.
- [ ] Fill in the timeline and division of responsibilities above.
