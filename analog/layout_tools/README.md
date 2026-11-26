# analog/layout_tools/

Layout of the analog cells (gLayout, `flow.py`) and of the analog macro `SNN_signed` assembled
from them (`top.py`). Every stage reads and writes files, prints a short status and refuses to
run if the stage before it has not passed, so any cell or the macro can be resumed from scratch.

| Path | Contents |
|---|---|
| `flow/<cell>/` | one cell (`DAC`, `DPI`, `DPI_inh`, `neuron`, `bias`): `<cell>.gds`, LVS reference, pins, PEX netlist, `signoff.json` |
| `top/SNN_signed/` | the macro: `SNN_signed.gds`, `SNN_signed_lvs_ref.spice`, `signoff.json`, `pex/` |
| `flow_cells.yaml`, `layout_policy.yaml` | cell registry (schematic, symbol, testbench) and designer defaults |
| `top_flow.yaml` | macro settings: blocks, floorplan, routing, macro pins, signoff |

`drc/` and `lvs/` folders and Magic `*_flat.*` intermediates are rewritten by every signoff and
are not tracked.

## Running

The flow runs in the gLayout environment `.venv-glayout` at the repo root (git-ignored; Python 3.11
with gLayout, set up with `uv`, see entry 75 of [`ai/Analog_AI_Documentation.md`](../../ai/Analog_AI_Documentation.md)).
From the repo root, inside the container:

```sh
F="env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/layout_tools/flow.py"
$F status  neuron          # what exists, what passed, what blocks the next stage
$F run     neuron          # table -> decide -> build -> signoff (decisions automatic)
$F run     neuron --manual # stop at every open decide question instead
$F answer  neuron Q-dummy_l "cap 2"    # answer a decide question
$F sim     neuron          # predicted-parasitic sim vs PEX sim

T="env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/layout_tools/top.py"
$T status   SNN_signed
$T run      SNN_signed     # netlist -> abstract -> plan -> place -> route -> signoff

bash analog/layout_tools/top_pex.sh SNN_signed   # C-only Magic PEX -> top/SNN_signed/pex/
```

Single stages: `flow.py table|decide|build|signoff <cell>`, `top.py
netlist|abstract|plan|place|route|signoff SNN_signed`.

After a macro change, continue with `librelane/macros/snn_analog/make_macro.py` and the rest of
the chain in the [main README](../../README.md#after-a-design-change).

`api_driver.py` drives the cell flow with one Claude API call (`AGENT_BRIEF.md` is its system
prompt): `python3 analog/layout_tools/api_driver.py neuron "build and sign off this cell"`.
