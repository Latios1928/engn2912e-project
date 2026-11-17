# Agent brief: GF180 gLayout analog layout flow

You drive a file-based layout flow for analog cells in a GF180MCU (gf180mcuD, 5 metals,
MIM-B) project. Everything you need is on disk; this brief replaces any earlier chat.

## The flow (one command per stage, `flow.py <stage> <cell>`)
| stage | does | writes (flow/<cell>/) | passes when |
|---|---|---|---|
| table | schematic -> flat device table, warnings, legalization | table.json | always (read warnings!) |
| decide | wells / DNW / dummies / guard rings / placement + reasons; auto-answers questions unless `--manual` | layout.yaml, decide.json | no open questions, no blockers |
| answer | answers one decide question (`answer <cell> <Q-id> "<option>"`) | layout.yaml | — |
| build | devices -> dummies -> wells/rings -> plan -> routing -> caps/pins -> LVS ref; short check, DRC prediction, parasitic prediction | <cell>.gds, _lvs_ref.spice, _pred.spice, .shapes.json, build.json | router clean, 0 predicted DRC errors |
| signoff | real KLayout DRC + LVS, Magic RC extraction, **feeds extraction back into the parasitic predictor** | drc/, lvs/, _pex.spice, signoff.json, parasitic_calib.json | DRC clean, LVS match, PEX ok |
| sim | testbench: predicted-parasitic sim vs PEX sim (typical) | sim/, sim.json | both ran |
| status | one screen of what exists / passed / blocks | — | — |
| run | table..signoff, stops where a human is needed | — | — |

Cells are registered in `flow_cells.yaml` (schematic, `connect` fixes, symbol, testbench,
metric). Designer defaults: `layout_policy.yaml`.

## Rules
- Start every task with `status`. Read `*.json` artifacts, not raw tool logs.
- Decisions are **auto** by default: `decide`/`run` answer every question with its policy
  default (`answered_by: auto`, listed in decide.json `auto_answers`) and continue. Always
  report the auto answers. `--manual` (or `decisions: manual` in flow_cells.yaml, or
  `decisions.mode` in layout_policy.yaml) makes the flow stop at open questions instead.
- Designer answers (`flow.py answer ...` or a hand edit) always beat auto answers. **Never
  answer a question yourself** unless the user's request states the answer.
- Auto mode cannot remove capability blockers (single row, extra DNW islands,
  common-centroid); those still stop the flow — report them.
- `connect` entries are schematic-bug workarounds; report them, never add one silently.
- Device resizing (W < 0.5 um -> 0.5 um, W/L kept) is automatic and logged in table.json;
  report it — the schematic must be updated to match before trusting simulations.
- A stage that fails: read its json, explain the cause in one or two lines, propose the fix.
  Do not loop more than twice on the same failure.
- Do not edit: the schematics (`*.sch`), `analog/neuron/layout/comparator_layout.py` (the designer's own file).
- Signoff (DRC ~1 min, LVS ~5 s, PEX ~1 s) is cheap; `sim` takes ~8 min — run it only when
  asked or when a parasitic-sensitive change was made.

## What the floorplanner (two_row) can build today
NMOS row in one shared DNW (body = ground), PMOS row in one n-well (body = VDD), dummy ring
per row, <= 2 MIM caps with the bottom plate on ground. `decide` reports anything else as a
blocker (single-row cells, extra DNW islands, common-centroid, extra guard rings).

## Known gLayout / GF180 facts (already handled in code; useful when diagnosing)
- FET `width` is per finger; min 0.5 um. LVS extracts one device per finger.
- n+ tap rings fill NWELL inside; stripped inside DNW (LPW.12).
- MIM cap extension tab lifts the bottom plate to met5; tab disabled. MIMTM.1: other met4
  >= 1.2 um from a MIM bottom plate.
- DNW stack ~6.4 um per side (LPW.3 2.5, DF.18 2.5, DN.3 substrate ring).
- Internal nets live inside the cell subckt: inject predicted caps there, not at top level.

## Reporting
Short: what ran, pass/fail, numbers (area, DRC/LVS, calibration factor, sim error),
open questions, next step. No raw logs.
