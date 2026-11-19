# ENGN 2912E Final Project

## Layout

| Path | Contents |
|---|---|
| `analog/` | Analog cells (`DAC/`, `DPI/`, `neuron/`, `bias/`), the network (`snn/`: schematic, Verilog black box), the macro layout (`layout_tools/top/SNN_signed/`), `testbenches/` |
| `digital/` | The digital part of the chip: `snn_digital.v` (`regs.v`, `pulse_gen.v`) |
| `snn_top.v` | Chip top: wires `digital/snn_digital.v` to `snn_analog`, which each build supplies |
| `mock/` | Behavioral `snn_analog` (and its DAC/neuron mocks) and the pure-digital end-to-end test of `snn_top` |
| `mixed/` | The same end-to-end test with the analog macro `SNN_signed` in ngspice |
| `librelane/` | Physical design of the whole chip (`snn_top`, with `snn_analog` as a hard macro); reads `digital/` and `analog/` only |
| `specifications/` | Specs given to the AI, and how it is used |

## TODO

### Analog
- [ ] Post-layout, the DACs over-excite: in0 fires 83–84 times per scenario against 22 in the schematic. The DAC's internal nodes (X and the isolated branch p-wells, ~0.33 pF) drain to 0 V while `en` is low and are refilled from `Isum` at each enable. Candidate fix: steer the current to VDD while `en` is low. See [analog/testbenches/snn/results/snn_signed_pex_diagnosis.md](analog/testbenches/snn/results/snn_signed_pex_diagnosis.md).
- [ ] Scenarios 5 and 7 (−15 against +15) fail under mismatch: with the `DPI_inh` mirror gain of 1.2 they pass all process corners, but only 45 / 100 post-layout Monte Carlo chips pass all 8 scenarios (gain 2.0 reaches 76 / 100 on 5 and 7). Decide between weight margin in the network (e.g. −15 against +12), a higher gain, or trimmed / larger synapse devices. See [analog/testbenches/snn/results/snn_signed_verification.md](analog/testbenches/snn/results/snn_signed_verification.md).
- [ ] Neuron reset only pulls MEM down to ~0.74–1.01 V instead of `reset_bias` (0.2 V): the reset stops as soon as the comparator flips back. Hold the reset for a fixed time (one-shot or SR latch). See [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md).
- [ ] Number of input pulses per fire varies because the reset level varies; recheck once the reset is fixed.
- [ ] Finish [tools/analog_API_infrastructure/advisor.py](tools/analog_API_infrastructure/advisor.py): it does not run yet (`os.enrivon`, `tuple{`, missing commas in the JSON schema, wrong body in `meets_spec`).

### Mixed-signal ([mixed/README.md](mixed/README.md))
- [ ] Calibrate the behavioral `snn_analog` in `mock/` (clock period, `GAIN`, `DURATION`, `LEAK`) so first-spike timing is close to the analog results, if the mock should be quantitatively comparable.
- [ ] The analog network has no reset: after the 4 ms `SETTLE` some membranes still hold up to ~0.3 V (threshold ~1.6 V, leak ~0.2 mV/µs), so a scenario starts from what the previous one left. Add a reset (switch on VMEM) or lengthen `SETTLE` (about 8 ms empties any membrane).
- [ ] Decide whether weights and signs should reset to 0 (about 40 flip-flops with reset) so the chip powers up silent; today they are undefined until written.
- [ ] Add scenarios with intermediate weights; run corners.

### Digital
- [ ] Pick the chip clock frequency. The pulse timing reset values (period 200, width 10) assume a 1 MHz `clk` for 10 µs pulses every 200 µs; the 8-bit period register allows at most about 1.3 MHz for that timing.

### Physical design
- [ ] Every flow/glayout GDS uses a 0.005 µm database unit; the PDK's newer DRC deck (`gf180mcu.drc`, rule `DBU`) requires 0.001 µm. `flow.drc()` waives it for now (see [analog/layout_tools/TOPLEVEL_FLOW.md](analog/layout_tools/TOPLEVEL_FLOW.md)). Fix before tape-out, and run the antenna and density checks at chip level. (The LibreLane macro wrapper `librelane/macros/snn_analog` already writes its GDS in 0.001 µm, which Magic requires.)
- [ ] LibreLane top level (`top-level` branch): [librelane/snn_top/config.json](librelane/snn_top/config.json) hardens `snn_top` with the analog macro `snn_analog` ([librelane/macros/snn_analog](librelane/macros/snn_analog): `SNN_signed` plus pin stubs and VDDA/VSSA bands for the power grid; rerun `make_macro.py` after any `SNN_signed` change). 640 × 910 µm, DRC / LVS / antenna / timing clean; gate-level simulations in `librelane/snn_top/gls` and `gls_ms`. Still to do: replace the old `results/` with the final run, copy its GDS / netlist to `gds/` and `verilog/gl/` (`lvs_config.json`), the max-slew warnings at the slow corner, an optional hand-written liberty for the macro, and the pad-ring integration.

### Docs
- [ ] Delete the `old/` folders (unused cells archived by the cell cleanup) once nothing references them.
- [ ] Remove the stale housekeeping item (5) from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md): the move to `analog/neuron/` is already committed.
- [ ] Fill in the timeline and division of responsibilities above.
