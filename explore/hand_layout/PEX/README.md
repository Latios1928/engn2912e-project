# Parasitic extraction (PEX) of the analog layouts

This folder turns a layout (`../<cell>.gds`) into a SPICE netlist that includes the
wiring's parasitic capacitance and resistance, so the testbenches can simulate the
block **as drawn** instead of as the schematic. There are no separate post-layout
testbenches: the runners in `analog/testbenches/<block>/` take `--pex` and run the same
testbench on the extraction. Post-layout results are the files ending in `__pex` in
`analog/testbenches/<block>/results/`.

## You changed a layout: do this

Everything runs inside the `gf180-work` container. From WSL / Windows:

1. **Regenerate and check the layout** as usual (DRC and LVS clean), e.g. for the neuron:
   ```sh
   docker exec gf180-work bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_neuron_checks.sh
   ```
2. **Extract it again.** One command per changed cell (`neuron_sized`, `DPI`, `DAC`, ...):
   ```sh
   docker exec gf180-work bash -l /foss/designs/engn2912e-project/analog/neuron/layout/PEX/extract.sh neuron_sized
   ```
3. **Read what it prints** (about 2 s). It must show:
   - warnings only of the kind `device missing 1 terminal; connecting remainder to node VSS/VDD`,
     one per dummy transistor (the neuron has 46: 26 to VSS, 20 to VDD). Any other warning: stop and look;
   - the same devices as the schematic plus the dummies (neuron: 36 `nfet_03v3`, 27 `pfet_03v3`,
     2 `cap_mim_2f0_m4m5_noshield`);
   - `wrote .../<cell>_pex_wrapper.spice`. If it says instead that the **pins differ**, a pin label is
     missing or renamed in the layout (or the symbol changed): fix the layout or the symbol, not the wrapper.
     The one allowed difference: a layout pin `GND` or `VSUBS` (Magic's name for an unlabelled substrate)
     that the symbol lacks, because the schematics use the global net `GND`. The wrapper ties it to ground.
4. **Re-run the block's runners with `--pex`**, e.g. for the neuron:
   ```sh
   docker exec gf180-work bash -lc "cd /foss/designs/engn2912e-project && python3 analog/testbenches/neuron/run_neuron_nominal.py --pex"
   docker exec gf180-work bash -lc "cd /foss/designs/engn2912e-project && python3 analog/testbenches/neuron/run_neuron_rate.py --pex"
   ```
   They write `results/*__pex.*` and refuse to run if step 2 was skipped (the GDS copy here
   differs from `../<cell>.gds`). Compare with the schematic results (same names without `__pex`).
5. **Commit** the layout, this folder's `<cell>.gds`, `<cell>_pex.spice`, `<cell>_pex_wrapper.spice`
   and `<cell>_extract_warnings.txt` together, plus the updated `__pex` results.

You changed only a **schematic** (sizes, not the layout)? The extraction is unchanged, but the
layout no longer matches: update the layout first (step 1), then continue from step 2.
You changed a **symbol's pin order**? Re-run step 2; the wrapper is regenerated from the symbol.

After re-extracting the same GDS, `git diff` shows `<cell>_pex.spice` as changed: Magic numbers
devices and nodes in a different order from run to run. The circuit is the same (checked
2026-11-12: same devices, same 423 resistors, same capacitance between every pair of nets).

## Files

| File | What it is | Edit? |
|---|---|---|
| `RC_extract.sh` | Magic extraction script, copied from `puf_sim/PEX/RC_extract.sh`: flattens the cell, extracts devices, R and C (keeps C > 0.5 fF and R > 5 Ω) | only to change the extraction settings, for every cell |
| `extract.sh` | Extracts one cell (what it does is listed below this table) | no |
| `make_pex_wrapper.py` | Writes `<cell>_pex_wrapper.spice` | no |
| `<cell>.gds` | Copy of `../<cell>.gds` that was extracted. The runners compare it with `../<cell>.gds` to detect a stale extraction | no, written by `extract.sh` |
| `<cell>_pex.spice` | **The extracted netlist**, subcircuit `<cell>_flat` | no, generated |
| `<cell>_pex_wrapper.spice` | Subcircuit `<cell>_pex`: includes `<cell>_pex.spice` and puts its pins in the order of `analog/neuron/<cell>.sym` | no, generated |
| `<cell>_extract_warnings.txt` | Magic's extraction warnings with their locations | no, generated |
| `RC_extract_<cell>.log` | Magic's log | no, generated |
| `<cell>_flat.ext`, `.res.ext`, `.nodes`, `.sim` | Magic's intermediate files | no, generated |

What `extract.sh` does: (1) copies `../<cell>.gds` here, (2) runs `RC_extract.sh`, (3) lists
the warnings and the devices, (4) runs `make_pex_wrapper.py`.

### Why a wrapper

Magic lists a subcircuit's pins in the order it finds them (neuron:
`VSS Vlk VK VT Vamp_bias VIp VKdn VNA VKup VMEM spike VDD`), but the testbenches connect pins by
position in the symbol's order (`VSS VDD VMEM VNA ...`). Without the wrapper, VDD would land
on Vlk. The wrapper maps the pins by name, so a testbench only changes the subcircuit name
from `<cell>` to `<cell>_pex`.

## Using the extraction in a testbench

- **Runner scripts:** `--pex` (see `analog/testbenches/tbpex.py`). The netlist of the normal
  testbench is used, with every `<cell>` instance switched to `<cell>_pex`. A new runner gets
  `--pex` by calling `tbpex.use_pex(text, cell)` on the netlist text.
- **One-off look in xschem** (e.g. to see post-layout waveforms live): in a scratch copy of the
  testbench, delete the block's symbol and add a code block with
  ```
  .include /foss/designs/engn2912e-project/analog/neuron/layout/PEX/<cell>_pex_wrapper.spice
  X1 <pins in symbol order, as net names> <cell>_pex
  ```
  Don't commit such copies; the runner's `--pex` is the reference.

## Status

| Cell | Extracted | Post-layout simulated |
|---|---|---|
| `neuron_sized` | 2026-11-12 | `run_neuron_nominal.py --pex`: fails t_refr (16.1 µs > 15 µs); see the neuron section of `analog/testbenches/README.md` |
| `DPI`, `DAC`, `DAC_binary` | not yet | - |
| `DAC_signed` | no layout yet | `run_dac_signed.py --pex` is ready: it runs as soon as `extract.sh DAC_signed` has |

`DPI` will stop at the wrapper step: its layout has a VSS pin that `DPI.sym` lacks (open
question in `analog/Analog_AI_Documentation.md` entry 58). Add the pin to the symbol first.
`DAC` and `DAC_binary` will stop too: their layouts have a VDD pin (deep N-well tie) that their
symbols lack. Add a VDD pin to the symbol (and to its instances), or tie it inside the wrapper by hand.

Notes: the extraction has no corners; run process corners by changing the models in the
testbench, as for the schematic. The MIM caps come out as `cap_mim_2f0_m4m5_noshield`
(the layout uses Metal4-Metal5) where the schematics use `cap_mim_2f0_m3m4_noshield`; the two
PDK models have the same parameters.
