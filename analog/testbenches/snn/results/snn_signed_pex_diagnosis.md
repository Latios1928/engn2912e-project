# Post-layout diagnosis of snn_signed (2026-11-18)

Hand-written notes on the post-layout runs of `run_snn_signed.py --pex` (generated table: [snn_signed_tb__pex.md](snn_signed_tb__pex.md), which each run overwrites).

## Scenarios 5 and 7: diagnosis and fix (2026-11-18)

Before the fix, the same macro with a 1:1 `DPI_inh` output mirror (Mi1 = Mi2 = 2u/8u) gave
**6 / 8**: scenario 5 hid1 2 spikes (1097 us), out 5; scenario 7 out 1 spike (1093 us).

- Both are a near-exact tie (-15 against +15 from neurons that fire alike). In the schematic the
  excitatory and inhibitory currents into the membrane cancel to 2.5-6 % (the mirror is slightly
  short at low VMEM); the leak absorbs the rest and VMEM levels off near 0.6 V.
- Post-layout the residual is about 4x: about 1.5x more total synaptic charge (DAC internal-node
  C kick, spikes 2.5-3x wider above 2.8 V), and hid0's DAC (word 6) delivers a few % less charge per
  spike than hid1's (word 7) plus one runt spike. VMEM then climbs about 0.3 V / 100 us and fires.
- Checks: with the weights mirrored (w6 = +15, w7 = -15) scenario 7 passes post-layout; the
  extracted `DPI_inh` and `DPI` cells give the same output for the same ideal input (inh/exc
  0.981 / 0.999 / 1.035 at 0.3 / 0.6 / 1.2 V, identical to the drawn-size netlists); moving the
  `Isum_i` coupling C to ground or removing the DAC switch-node C does not close the gap alone.
- Fix: Mi2 2.4u/8u (mirror gain 1.2), so equal-magnitude inhibition wins with margin. Tested
  first on the old extraction (gain 1.1 and 1.2 both pass 5 and 7 over 3 ms), then built:
  `DPI_inh` rebuilt (93.21 x 49.54 um), macro re-routed (same 616.4 x 806.5 um), DRC clean, LVS
  match, re-extracted: this table. The schematic suite also stays 8 / 8.
- Spike counts are not comparable one-to-one with the pre-fix extraction (in0 84 -> 83-84):
  the macro was re-routed and extracted with this container's Magic / PDK (open_pdks 1689ac3).
  The excess input-layer firing (schematic 22-23) is the DAC kick below and is still open.
- Extraction correction (later the same day): the first re-extraction used `ext2spice lvs`, which
  in Magic 8.3.684 drops every node-to-substrate capacitor (3.7 pF total instead of 9.6 pF).
  The figures first quoted for it (in0 67-71, failures at hot corners) came from that
  extraction and are void. `top_pex.sh` now uses `hierarchy off / scale off / subcircuit top on`
  (same devices and nets plus the substrate C); the tables in this folder are from that one.
  It is still lighter than the committed pre-fix extraction (Magic 8.3.636: 12.5 pF), mostly in
  coupling C.
- Corners and mismatch with the new gain: [snn_signed_verification.md](snn_signed_verification.md).
  All 15 corner / temperature points pass 8/8; under mismatch 45 / 100 chips pass all 8, the
  losses being scenarios 5 and 7 (an exact tie has no reliable winner from chip to chip).

## Why the post-layout macro fires more (diagnosis 2026-11-18, pre-fix extraction, scenario 2, in0 spike count)

| netlist | in0 spikes |
|---|---|
| schematic (`snn_analog_signed` + `bias`) | 22 |
| schematic network + resized bias cell from the LVS ref | 15 |
| LVS ref of the whole macro (drawn device sizes, no parasitics) | 23 (8/8 scenarios pass) |
| extraction, all parasitic C removed | 29 |
| extraction, coupling C to spike nets removed | 96 |
| extraction, every coupling C moved to ground | 103 |
| full extraction | 84 |

- Device resizing (0.22 -> 0.5 um "W/L kept") moves the bias outputs (Vthr, VT_dpi -100 mV,
  Vamp_bias +97 mV, VNA -55 mV, VK +41 mV) but on its own keeps 8/8 passing.
- The excess firing comes from parasitic C, not coupling. Bisection on 0.3 ms runs (VMEM_0 at
  280 us: no C 0.93 V, full 1.75 V): removing C on bias lines, Isum islands, the DPI Vsyn node or the
  neuron's internal nodes changes nothing; removing C on the 7 internal nets of the input DAC
  (word 0) restores it (0.84 V). Those nets are the DAC switch node X (65 fF), the four branch
  nodes net1..net4 with their isolated p-well bodies (40-103 fF each) and Y / sb: ~0.35 pF the
  schematic DAC does not have. With `en` low the current sources pull them to VSS; when `en` rises
  they are recharged from Isum, an extra charge kick into the exponential DPI.
- Same structure in every DAC. (The original note here, that the inhibitory paths of scenarios 5, 7
  lose against the 3-4x stronger excitatory ones, was not confirmed: adding these caps to the
  schematic DACs leaves 5 and 7 passing. See the section above for their actual cause.)
- Simulation notes: bias MR_VK (0.5/90.91 um) is beyond the 50 um model range and is simulated
  as 2 x 45.455 um in series; C-only extraction (no wire R), Magic well/junction caps approximate.
