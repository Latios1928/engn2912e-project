# ENGN 2912E Final Project

**Chip signoff summary — layout, verification results and how to re-run them: [signoff/](signoff/README.md).**

## Layout

| Path | Contents |
|---|---|
| `analog/` | Analog cells (`DAC/`, `DPI/`, `neuron/`, `bias/`), the network (`snn/`: schematic, Verilog black box), the macro layout (`layout_tools/top/SNN_signed/`), `testbenches/` |
| `digital/` | The digital part of the chip: `snn_digital.v` (`regs.v`, `pulse_gen.v`) |
| `snn_top.v` | Chip top: wires `digital/snn_digital.v` to `snn_analog`, which each build supplies |
| `mock/` | Behavioral `snn_analog` (and its DAC/neuron mocks) and the pure-digital end-to-end test of `snn_top` |
| `mixed/` | The same end-to-end test with the analog macro `SNN_signed` in ngspice |
| `librelane/` | Physical design of the whole chip (`snn_top`, with `snn_analog` as a hard macro); reads `digital/` and `analog/` only |
| `signoff/` | Chip signoff summary for reviewers: floorplan, results of every check, `run_checks.sh` to re-run them |
| `specifications/` | Specs given to the AI, and how it is used |

## TODO

### Analog
- [ ] Post-layout, the input neurons fire about 2.7× as often as in the schematic: 49–56 spikes per scenario against 16–21 ([snn_signed_tb__pex.md](analog/testbenches/snn/results/snn_signed_tb__pex.md) vs [snn_signed_tb.md](analog/testbenches/snn/results/snn_signed_tb.md)). The DAC's internal nodes drain while `en` is low and are refilled from `Isum` at each enable; tying the switch bodies to GND (2026-11-18) reduced it. Candidate fix: steer the current to VDD while `en` is low. All 8 scenarios still pass post-layout. See [snn_signed_pex_diagnosis.md](analog/testbenches/snn/results/snn_signed_pex_diagnosis.md).
- [ ] Scenarios 5 and 7 (−15 against +15) are a near tie: with the `DPI_inh` mirror gain of 1.2 and the larger DPI input pair they pass all process corners, and 93 / 100 post-layout Monte Carlo chips pass both (5: 99, 7: 94; failures are 1–3 stray spikes, [snn_signed_tb__pex__mc100.md](analog/testbenches/snn/results/snn_signed_tb__pex__mc100.md)). Accept, or add margin (weight margin in the test, e.g. −15 against +12, or a higher gain).
- [x] Neuron reset: the old items (reset stopping at 0.74–1.01 V, varying pulses per fire) were about the earlier Schmitt-trigger neuron. The current neuron resets to < 1 mV ([analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md)).
- [x] [tools/analog_API_infrastructure/advisor.py](tools/analog_API_infrastructure/advisor.py) is the completed advisor; `advisor_draft.py` is the original draft, kept with its fixes listed in that folder's README.

### Mixed-signal ([mixed/README.md](mixed/README.md))
- [ ] Calibrate the behavioral `snn_analog` in `mock/` (clock period, `GAIN`, `DURATION`, `LEAK`) so first-spike timing is close to the analog results, if the mock should be quantitatively comparable.
- [ ] The analog network has no membrane reset: after the 4 ms `SETTLE` some membranes still hold up to ~0.3 V (threshold ~1.6 V), so a scenario starts from what the previous one left. On the chip, wait at least 8 ms with `in = 00` between test cases ([PINLIST.md](PINLIST.md) §5), or add a reset (switch on VMEM; analog change, full rebuild).
- [x] Weights at power-up: no reset; the documented power-up procedure handles it (2026-11-22). Arbitrary weights are harmless while `in = 00` (scenario 1 passes in every simulation); the power-up procedure is in [PINLIST.md](PINLIST.md) §5, including holding `addr` at `4'hF` from power-on.
- [x] Scenarios 6–8 (sign at the input, the tie at the output, its control) added to `mixed/snn_ms_tb.v` and run at gate level. Still open: rerun the RTL run in `mixed/` with them, intermediate-weight scenarios, and mixed-signal corners (the analog-only runner covers corners and mismatch).

### Digital
- [x] Clock frequency (confirmed 2026-11-21): the network runs at 5 kHz (10 µs spikes every 200 µs, the rate the neuron and DPI are sized for), with a 1 MHz `clk` and the reset pulse timing (period 200, width 10). LibreLane (`CLOCK_PERIOD` 1000), `digital/tb_snn_digital.v` and `mixed/snn_ms_tb.v` all use 1 MHz. The 8-bit period register allows at most about 1.3 MHz for 5 kHz pulses.

### Physical design
- [x] Database unit: the flow / glayout cell GDS and `SNN_signed.gds` use 0.005 µm (`flow.drc()` waives the `DBU` rule there), but the macro GDS LibreLane uses (`librelane/macros/snn_analog`) and the chip GDS (`gds/snn_top.gds`) are 0.001 µm, and the chip's KLayout DRC (741 rules, density included) reports only the 27 fill errors below.
- [ ] LibreLane top level (`chip-signoff` branch; summary in [signoff/](signoff/README.md)): [librelane/snn_top/config.json](librelane/snn_top/config.json) hardens `snn_top` with the analog macro `snn_analog` ([librelane/macros/snn_analog](librelane/macros/snn_analog): `SNN_signed` plus pin stubs and VDDA/VSSA bands for the power grid; rerun `make_macro.py` after any `SNN_signed` change). 640 × 910 µm; gate-level simulations in `librelane/snn_top/gls` and `gls_ms`. Run `RUN_2026-11-21_22-31-59` (in `results/`, `gds/snn_top.gds`, `verilog/gl/snn_top.v`): Magic DRC, antenna, power grid, timing and max slew/cap/fanout clean at all 9 corners. VDDA / VSSA and VDDD / VSSD are separate nets and pads, for switching-noise isolation. They share the p-substrate, so the macro wrapper carries an `ISOSUB` marker (GDS 23/5, written by `make_macro.py`) over its footprint, kept 2 µm away from the deep n-well; without it, extraction merges VSSA and VSSD through the substrate and chip LVS fails. The marker is for extraction / LVS only: GDS layer 23 is in neither the drawn-layer table nor the mask-layer numbering of the GF180MCU design manual (sections 4.1 and 4.3, where datatype 5 is the marking-layer convention), so no mask is made from it; only the PDK's Magic and KLayout LVS decks read it. Also: the project SDC [snn_top.sdc](librelane/snn_top/snn_top.sdc) (Iref / VT untimed), and no delay cells (the resizer had used `dlyb_1` as fanout buffers, which caused the old slow-corner slew violations). Full-chip LVS down to transistors (Magic extraction of `gds/snn_top.gds` against `verilog/gl/snn_top.v` + `snn_analog_lvs_ref.spice`, the `lvs_config.json` sources) matches uniquely with VSSA and VSSD separate. LibreLane's own LVS black-boxes the macro, so run [chip_lvs.py](librelane/snn_top/chip_lvs.py) after any design change (see *After a design change* below). Gate-level simulations on this netlist (2026-11-21), all PASS: `gls/` `make` (behavioral analog, 6 checks); `gls/` `make timing` ([tb_gls_timing.v](librelane/snn_top/gls/tb_gls_timing.v), 1 MHz clock, pulse timing and register writes into the macro, 13 checks, zero-delay and with the ss / tt / ff SDF); `gls_ms/` `make run` (macro schematic netlist in ngspice, scenarios 1-8, 34 min) and `make run PEX=1` (post-layout macro, scenarios 1-8, 11 min). Scenarios 6-8 (sign at the input, the +15 / -15 tie at the output, its control) are new in `mixed/snn_ms_tb.v`; the RTL run in `mixed/` has not been repeated with them. Still to do: the 27 KLayout `DCF.1a` errors (COMP density, needs fill; LibreLane exits non-zero on them, so `run.sh` skips its copy step: copy by hand), confirm with the organisers that their precheck accepts the 23/5 marker in the submitted GDS (the manual's analog-layer section could not be checked), an optional hand-written liberty for the macro, and the pad-ring integration.

### After a design change
Rerun the chain from the step that changed, then all checks (each step's output is the next one's input):

1. Analog cell: `analog/layout_tools/flow.py` (cell DRC / LVS / PEX), then `top.py` (`SNN_signed` signoff) and `top_pex.sh`.
2. `librelane/macros/snn_analog/make_macro.py` (macro GDS with the `ISOSUB` marker, LEF, LVS reference).
3. Digital RTL or anything above: `librelane/snn_top/run.sh` (publishes `results/`, `gds/snn_top.gds`, `verilog/gl/snn_top.v`, `results/sdf/`). Until fill is added, LibreLane exits non-zero on the 27 `DCF.1a` errors and `run.sh` skips its copy step: copy the run's `final/` files by hand.
4. `python3 librelane/snn_top/chip_lvs.py`: full-chip LVS down to transistors plus the checks that each link of the chain is current (macro signoff, macro reference and layout = `SNN_signed`, chip macro = `snn_analog.gds`, published files = `results/`, VSSA / VSSD separate). It names the step to rerun when one fails. `--layout <gds>` checks a candidate GDS before publishing.
5. Gate-level: `librelane/snn_top/gls`: `make` and `make timing`; `librelane/snn_top/gls_ms`: `make run PEX=1` (scenarios 1–8, about 11 min; `make run` for the schematic macro, about 34 min).

### Docs
- [x] The `old/` folders (cells, hand layouts and testbenches archived by the cell cleanup) are deleted (2026-11-22); restore anything from git commit 2dd89b5.
- [x] Stale housekeeping item removed from [analog/neuron/SIM_LOG.md](analog/neuron/SIM_LOG.md).
- [ ] Fill in the timeline and division of responsibilities above.
