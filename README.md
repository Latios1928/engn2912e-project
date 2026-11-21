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
- [x] Clock frequency (confirmed 2026-11-21): the network runs at 5 kHz (10 µs spikes every 200 µs, the rate the neuron and DPI are sized for), with a 1 MHz `clk` and the reset pulse timing (period 200, width 10). LibreLane (`CLOCK_PERIOD` 1000), `digital/tb_snn_digital.v` and `mixed/snn_ms_tb.v` all use 1 MHz. The 8-bit period register allows at most about 1.3 MHz for 5 kHz pulses.

### Physical design
- [ ] Every flow/glayout GDS uses a 0.005 µm database unit; the PDK's newer DRC deck (`gf180mcu.drc`, rule `DBU`) requires 0.001 µm. `flow.drc()` waives it for now (see [analog/layout_tools/TOPLEVEL_FLOW.md](analog/layout_tools/TOPLEVEL_FLOW.md)). Fix before tape-out, and run the antenna and density checks at chip level. (The LibreLane macro wrapper `librelane/macros/snn_analog` already writes its GDS in 0.001 µm, which Magic requires.)
- [ ] LibreLane top level (`top-level` branch): [librelane/snn_top/config.json](librelane/snn_top/config.json) hardens `snn_top` with the analog macro `snn_analog` ([librelane/macros/snn_analog](librelane/macros/snn_analog): `SNN_signed` plus pin stubs and VDDA/VSSA bands for the power grid; rerun `make_macro.py` after any `SNN_signed` change). 640 × 910 µm; gate-level simulations in `librelane/snn_top/gls` and `gls_ms`. Run `RUN_2026-11-21_22-31-59` (in `results/`, `gds/snn_top.gds`, `verilog/gl/snn_top.v`): Magic DRC, antenna, power grid, timing and max slew/cap/fanout clean at all 9 corners. VDDA / VSSA and VDDD / VSSD are separate nets and pads, for switching-noise isolation. They share the p-substrate, so the macro wrapper carries an `ISOSUB` marker (GDS 23/5, written by `make_macro.py`) over its footprint, kept 2 µm away from the deep n-well; without it, extraction merges VSSA and VSSD through the substrate and chip LVS fails. The marker is for extraction / LVS only: GDS layer 23 is in neither the drawn-layer table nor the mask-layer numbering of the GF180MCU design manual (sections 4.1 and 4.3, where datatype 5 is the marking-layer convention), so no mask is made from it; only the PDK's Magic and KLayout LVS decks read it. Also: the project SDC [snn_top.sdc](librelane/snn_top/snn_top.sdc) (Iref / VT untimed), and no delay cells (the resizer had used `dlyb_1` as fanout buffers, which caused the old slow-corner slew violations). Full-chip LVS down to transistors (Magic extraction of `gds/snn_top.gds` against `verilog/gl/snn_top.v` + `snn_analog_lvs_ref.spice`, the `lvs_config.json` sources) matches uniquely with VSSA and VSSD separate. LibreLane's own LVS black-boxes the macro, so rerun the full-chip check after any macro change. Gate-level simulations on this netlist (2026-11-21), all PASS: `gls/` `make` (behavioral analog, 6 checks); `gls/` `make timing` ([tb_gls_timing.v](librelane/snn_top/gls/tb_gls_timing.v), 1 MHz clock, pulse timing and register writes into the macro, 13 checks, zero-delay and with the ss / tt / ff SDF); `gls_ms/` `make run` (macro schematic netlist in ngspice, scenarios 1-8, 34 min) and `make run PEX=1` (post-layout macro, scenarios 1-8, 11 min). Scenarios 6-8 (sign at the input, the +15 / -15 tie at the output, its control) are new in `mixed/snn_ms_tb.v`; the RTL run in `mixed/` has not been repeated with them. Still to do: the 27 KLayout `DCF.1a` errors (COMP density, needs fill; LibreLane exits non-zero on them, so `run.sh` skips its copy step: copy by hand), confirm with the organisers that their precheck accepts the 23/5 marker in the submitted GDS (the manual's analog-layer section could not be checked), an optional hand-written liberty for the macro, and the pad-ring integration.

### Docs
- [ ] Delete the `old/` folders (unused cells archived by the cell cleanup) once nothing references them.
- [ ] Remove the stale housekeeping item (5) from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md): the move to `analog/neuron/` is already committed.
- [ ] Fill in the timeline and division of responsibilities above.
