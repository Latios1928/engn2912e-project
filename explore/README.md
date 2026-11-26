# explore/

Design work that is **not on the final chip**, kept for reference. Files are as they were when
moved here, so paths inside them may still name their old locations.

| Folder | What it is | Run |
|---|---|---|
| `bias/` | On-chip bias generator (Luz): a beta-multiplier reference with a 4-bit steered-mirror trim feeding the bias cell. Not used: the macro takes `Iref` from a pin. | [`bias/generator/README.md`](bias/generator/README.md); `python3 explore/bias/sim/bias_tb.py` |
| `unsigned/` | The earlier unsigned 2-2-1 network (`snn_analog.sch`, built from `DAC_unsigned`). `bias/testbenches/bias_network_tb.sch` uses it, so `xschemrc` keeps this folder on the symbol path. | open in xschem |
| `hand_layout/` | Hand-era layout work: the hand-coded `neuron_sized.gds` and the first gLayout `neuron_glayout.gds` with their extractions, the old macro's extraction (`SNN_pex*.spice`), its well-bias audit (`SNN_well_bias.md`), `comparator_layout.py`, and the extraction scripts (`PEX/extract.sh`, `make_pex_wrapper.py`). The current layouts come from `analog/layout_tools/`. | `PEX/README.md` (old paths) |
| `spike_amp/` | Sizing sweep of the neuron's spike amplifier (5T OTA); its result set the sizes in `analog/neuron/spike_amplifier.sch`. | `python3 explore/spike_amp/run_sweep.py` |
| `analog_API_infrastructure/` | LLM-assisted sizing loop used for the neuron (`configs_sized/`). | [its README](analog_API_infrastructure/README.md) |

## Earlier designs no longer in the tree

All of these are in `main`'s history; check out or `git show` the commit listed.

| What | Replaced by | Last on `main` at |
|---|---|---|
| Behavioral analog model `mock/` (Verilog DAC / neuron / comparator) and its end-to-end testbench | gate-level timing testbench and mixed-signal runs | `fd146c6` |
| XOR study on the unsigned network (`analog/testbenches/xor/`) | the signed network's scenarios 5–8 | `fd146c6` |
| Hand-drawn cell layouts (`DAC_signed`, `DAC_binary`, `DPI`, `DPI_inh`, `bias_cell`, spike amplifier, comparator) and the hand-assembled macro `SNN.gds`, in the `old/` folders | `analog/layout_tools/` (gLayout flow and `top.py`) | `2647ca2` |
| Archived cells and their testbenches (`old/` folders), including the Schmitt-trigger neuron `neuron_old.sch` and the partly signed network `snn_analog_inh.sch` | the current cells in `analog/` | `2647ca2` |
| Register file with a `wren` pin (`digital/rf.v`), the trim register and its Verilog-A reference (`mixed/addr4_trim/`) | `digital/regs.v` (4-bit address, no `wren`); `Iref` as a chip pin | `eb84041` |
| `in[1:0]` chip pins for the input enables | register 14 | `f94bf54` |

The hand layouts were 2–8× smaller than the gLayout cells (bounding boxes, µm²): DAC 6 700 vs
14 400, DPI 730 vs 3 100, DPI_inh 1 100 vs 5 600, bias 9 000 vs 68 000, neuron 3 300 vs 8 000.
The cells have been re-sized since (binary DAC, larger DPI input pair, `DPI_inh` mirror gain), so
this is a rough comparison only.
