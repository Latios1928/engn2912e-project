# Top-level layout flow: design draft (2026-11-17)

Goal: build the analog SNN macro (first target `analog/snn/snn_analog_signed.sch`) from its
schematic and its block layouts with the same file-based, stage-by-stage style as the cell
flow (`flow.py`): every stage reads and writes files under `top/<top>/`, prints one short
status, can be rerun alone, and is checked by fast predictors before the real tools.
`gen_snn.py` (hand-coded, `snn_analog_inh` only) stays as the reference to match.

## 1. What exists and what is missing

| | have | missing for a top level |
|---|---|---|
| blocks | 4 flow cells signed off (neuron_glayout, bias_cell, DPI, DAC_signed_binary); hand GDS for DPI, DPI_inh, DAC_binary, DAC_signed, neuron_sized, bias_cell | edge pins on flow cells (now M4 labels at the left end of internal tracks, M2 rail labels inside); one abstract format for both kinds |
| netlist | xschem netlists the top schematic | a block map (symbol -> layout) and pin mapping by name |
| placement | gen_snn.py's fixed row plan | placement derived from the network, editable decisions |
| routing | cell router (tracks, pack_tracks, short check); gen_snn.py hand tracks | a channel router over blocks |
| checks | real DRC / LVS / Magic PEX; predrc, parasitic predictor, coupling.py | hierarchical LVS ref from the schematic; top-level short check, predrc, coupling prediction |

## 2. Stages (`top.py <stage> <top>`, outputs in `top/<top>/`)

| stage | does | writes | passes when |
|---|---|---|---|
| netlist | xschem netlist of the top schematic -> instances {name, symbol, pin -> net}, top pins; map each symbol to a block via `top_blocks.yaml` | netlist.json | every instance has a block, every block pin is in the symbol |
| abstract | for every block used: bbox, pins (name, layer, side, access box), blockages per metal layer, LVS ref file, PEX file | abstracts/<block>.json | every pin has an edge access box |
| plan | floorplan decisions (like `decide`): rows / columns, orientation, channel order, supply style, sensitive nets, bias position; asks questions, auto-answers from `top_policy.yaml` | floorplan.yaml, plan.json | no open questions, no blockers |
| place | coordinates from the plan; channel widths from routing demand (iterates with route's estimate) | placement.json | no overlaps, channels wide enough |
| route | global (net -> channel sequence) + detailed (track assignment) + supply | <top>.gds, shapes.json, route.json | every net routed, short check clean, predrc 0 |
| signoff | DRC, hierarchical LVS, Magic PEX (C-only first), island-short check | drc/ lvs/ pex/ signoff.json | DRC clean, LVS match |
| sim | top testbench (`snn_signed_tb`) with the macro swapped for its extraction; compare spike counts with the schematic run | sim.json | every scenario as in schematic |
| status / run | as in the cell flow | | |

## 3. Key pieces

### 3.1 Block abstract (one format for flow cells and hand blocks)
`abstracts/<block>.json`, same fields as today's `<block>_pins.json` (bbox, per pin: layer,
side, access box) plus `blockage` per metal layer (rectangles the top router must avoid),
`lvs_ref`, `pex`, `source: flow | hand`, and the block's own signoff status. Hand blocks: from
`extract_pins.py` (already edge pins). Flow cells: two changes in `two_row`:
1. **edge pins**: every pin net gets a stub to the cell boundary on a pin layer. Default
   Metal3 on the left or right edge (vertical top-level tracks in the channels reach them
   with a Metal2/Metal3 stub, as in gen_snn.py); VDD / VSS on Metal2 straps to the left and
   right edges. Pin side per pin from the plan (`pin_sides` in the block's layout.yaml), so a
   block can face its channel.
2. write `<cell>_pins.json` in the abstract format during `build`.

### 3.2 Block map `top_blocks.yaml`
```yaml
DAC_signed_binary: {source: flow, cell: DAC_signed_binary}      # or {source: hand, gds: ../DAC/layout/DAC_signed.gds}
DPI:               {source: flow, cell: DPI}
DPI_inh_min:       {source: flow, cell: DPI_inh_min}            # not built yet
neuron_sized:      {source: flow, cell: neuron_glayout}
bias_cell:         {source: flow, cell: bias_cell}
pin_alias: {GND: VSS}                                           # schematic ground name -> layout
```
The bias cell is not in `snn_analog_signed.sch` (biases are pins there): the map can add
`extra_instances: {xbias: bias_cell}` whose outputs replace the bias pins, as gen_snn.py does.

### 3.3 Floorplan (`plan`)
Default template = gen_snn.py's, derived from the netlist instead of hard-coded: one **row per
neuron**, in layer order (inputs, hidden, output); in each row the blocks that drive that
neuron's VMEM, left to right: `DAC column (all DACs into this neuron) | ch A | DPI + DPI_inh | ch B | neuron | ch C`.
Rows found from the graph: a neuron's row holds every DPI whose output is its VMEM and every
DAC whose Isum feeds those DPIs. Bias cell above the top row (or left column, policy).
Decisions in `floorplan.yaml` (designer edits survive reruns, like layout.yaml):
row order, mirror per block, which side each block's pins face, channel layer use, sensitive
nets and their rules (VMEM, Isum*: no parallel run with spike/en over N um, or a shield),
supply style (edge buses + per-row straps, or M5 grid).

### 3.4 Router (`route`)
Channel router, nothing over blocks except declared layers (M5 if no block uses it):
- **layer plan**: M2 short horizontal stubs pin -> track; M3 vertical tracks in channels;
  M4 horizontal inter-row buses in the gaps between rows; M5 supply grid / long spikes.
- **global**: each net = pins in rows/channels -> the channel and inter-row gaps it uses
  (a net local to one row stays in that row's channel).
- **detailed**: left-edge track packing per channel and per inter-row gap
  (`pack_tracks` generalised to vertical channels), stub order chosen so no two M2 stubs of
  different nets overlap (the rule gen_snn.py checks by hand).
- **sensitive nets**: cost on adjacency; spike lines separated or rotated across layers as
  in gen_snn.py.
- every shape net-tagged in a `Router` (same class as cells) -> `check()` short finder,
  predrc on the GDS, coupling prediction from the shapes (coupling.py logic on the predictor).
- channel width demand -> fed back to `place` (one or two iterations).

### 3.5 LVS and PEX
- **LVS ref** from the top schematic netlist: each instance line kept, each block subckt
  replaced by that block's own LVS ref (`*_lvs_ref.spice`, with its added VSS/VDD pins and
  dummies), extra instances (bias cell) inserted, pins mapped by name, `pin_alias` applied.
  Replaces make_snn_lvs_ref.py.
- **PEX**: C-only first (run_snn_pex.sh's finding: Magic extresist merged isolated LVPWELL
  bodies into substrate). With the new islands in DPI / DAC cells, `signoff` checks the
  extraction for any Isum*/island net shorted to VSS before it is used.

## 4. Milestones (each ends with real DRC + LVS)

1. **Edge pins + abstracts.** two_row edge pins, `<cell>_pins.json`; abstracts for all
   blocks. Rerun the 4 flow cells (DRC/LVS must stay clean). Build `DPI_inh_min`.
2. **Reproduce the known top.** netlist + plan + place + route on `snn_analog_inh` with the
   hand blocks; acceptance: DRC clean, LVS match, area within ~10 % of SNN.gds (285 x 547 um).
   This validates the flow against a layout that is known to work.
3. **Signed network.** `snn_analog_signed` with flow blocks (8 DAC_signed_binary, 5 DPI,
   3 DPI_inh_min, 5 neurons, bias cell); DRC / LVS.
4. **Post-layout check.** C-only PEX, island-short check, `snn_signed_tb` scenarios on the
   extraction vs schematic; coupling report on VMEM / Isum.
5. **Speed.** predictors on the top level (short check, predrc, coupling) so a plan change
   costs seconds before the ~minutes of real DRC/LVS; `top.py run` for the whole chain.

## 5. Open decisions (designer)
1. **Block sources.** Flow DAC is 305 x 54 um vs hand DAC_signed 182 x 33 um (x8 in the
   signed network: ~0.13 vs ~0.05 mm2); flow DPI 55 x 54 vs hand 28 x 26. Area budget?
   Tie the DAC switch bodies to VSS (no islands, costs nothing electrically) before building?
2. **Bias cell position** (above the top row as now, or a left column) and whether VT stays
   a pin.
3. **Supply style**: edge buses + row straps (as gen_snn.py) or an M5 grid.
4. **Sensitive-net rules**: which nets (VMEM_*, Isum*, Vb) and how far from spike / en / w.
5. **Pin side of the macro** (all on the bottom edge today) — set by the digital block / pads.
6. Digital side of `s[7:0]` (not a layout question, but the macro pin list depends on it).
