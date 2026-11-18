# snn_signed verification: process corners and mismatch (2026-11-18)

Verification of the signed 2-2-1 macro after the `DPI_inh` mirror-gain fix (Mi2 2u/8u -> 2.4u/8u,
gain 1.2; see [snn_signed_pex_diagnosis.md](snn_signed_pex_diagnosis.md)). All runs use
`run_snn_signed.py` with the 8 scenarios of [snn_signed_tb.md](snn_signed_tb.md) (3 ms each, 10 us
pulses every 200 us). The per-run reports are the `snn_signed_tb__*.md` files in this folder.

Three netlists:

| name | what it is | option |
|---|---|---|
| schematic | `snn_analog_signed` + `bias` from xschem (DPI / neuron devices drawn 0.22 / 0.28 um) | (none) |
| drawn | the macro's LVS reference: drawn device sizes (0.5 / 0.64 um, W/L kept), no parasitics | `--drawn` |
| post-layout | C-only Magic extraction of `SNN_signed.gds` (`top_pex.sh`), 9.6 pF total | `--pex` |

## Summary

| check | result |
|---|---|
| nominal (tt, 27 C): schematic / drawn / post-layout | 8/8 / 8/8 / 8/8 |
| process corners tt, ss, ff, sf, fs x 0, 27, 70 C (schematic) | 15 / 15 points 8/8 |
| process corners tt, ss, ff, sf, fs x 0, 27, 70 C (post-layout) | 15 / 15 points 8/8 |
| mismatch MC, 100 chips, post-layout, all 8 scenarios | **45 / 100 chips** pass all 8 |
| mismatch MC, 100 chips, drawn, scenarios 5 and 7, gain 1.0 / 1.2 | **41 / 100** -> **51 / 100** |

The fix makes the macro pass at nominal and across all process / temperature corners. Under
random device mismatch, the two -15 against +15 tie tests (scenarios 5 and 7) fail on about a third
of the chips each. A higher mirror gain helps but does not close it (76 / 100 at gain 2.0, below).

## Process corners

Post-layout and schematic: every point passes 8/8.

| corner | 0 C | 27 C | 70 C |
|---|---|---|---|
| tt | 8/8 | 8/8 | 8/8 |
| ss | 8/8 | 8/8 | 8/8 |
| ff | 8/8 | 8/8 | 8/8 |
| sf | 8/8 | 8/8 | 8/8 |
| fs | 8/8 | 8/8 | 8/8 |

Spike-count range over the 15 points (min-max):

| scenario | netlist | in0 | in1 | hid0 | hid1 | out |
|---|---|---|---|---|---|---|
| 2 pulse0 -> in0 | post-layout | 62-103 | 0 | 0 | 0 | 0 |
| | schematic | 16-28 | 0 | 0 | 0 | 0 |
| 3 in1 -> hid1 -> out | post-layout | 0 | 61-101 | 0 | 39-59 | 34-54 |
| | schematic | 0 | 16-29 | 0 | 21-49 | 23-58 |
| 5 in0 -15 vs in1 +15 into hid1 | post-layout | 63-104 | 62-102 | 0 | **0** | 0 |
| | schematic | 17-31 | 17-31 | 0 | **0** | 0 |
| 7 hid0 -15 vs hid1 +15 into out | post-layout | 63-104 | 62-102 | 40-60 | 40-60 | **0** |
| | schematic | 17-30 | 17-30 | 22-48 | 22-48 | **0** |
| 8 control for 7 (hid0 -> out = 0) | post-layout | 63-104 | 62-102 | 40-60 | 40-60 | 34-55 |
| | schematic | 17-31 | 17-31 | 22-51 | 22-51 | 24-60 |

Scenarios 1, 4 and 6 stay silent where required at every point. The input layer fires about 3.5x
more post-layout than in the schematic (the open DAC charge-kick issue, see the diagnosis note).

## Mismatch Monte Carlo

PDK `sw_stat_mismatch`, `--mc 100` (seeds 1-100), tt 27 C. One seed is one chip: every scenario of
a seed sees the same mismatch, bias cell included. Chip yield = all scenarios pass on that seed.

### Post-layout, all 8 scenarios ([snn_signed_tb__pex__mc100.md](snn_signed_tb__pex__mc100.md))

| scenario | pass | in0 mean (min-max) | in1 | hid0 | hid1 | out |
|---|---|---|---|---|---|---|
| 1 all +15, no input | 100 / 100 | 0 | 0 | 0 | 0 | 0 |
| 2 pulse0 -> in0 | 100 / 100 | 81.3 (61-103) | 0 | 0 | 0 | 0 |
| 3 in1 -> hid1 -> out | 100 / 100 | 0 | 80.4 (56-110) | 0 | 48.2 (34-65) | 41.9 (16-61) |
| 4 as 3, hid1 -> out = 0 | 99 / 100 | 0.0 (0-1) | 80.5 (56-111) | 0 | 48.2 (34-65) | 0 |
| 5 in0 -15 vs in1 +15 into hid1 | **66 / 100** | 82.8 (62-105) | 81.8 (57-112) | 0 | 6.3 (0-41) | 7.6 (0-48) |
| 6 pulse0 -> in0 = -15 | 100 / 100 | 0 | 0 | 0 | 0 | 0 |
| 7 hid0 -15 vs hid1 +15 into out | **67 / 100** | 82.8 (62-105) | 81.8 (57-112) | 48.3 (30-72) | 48.7 (34-66) | 5.0 (0-51) |
| 8 control for 7 | 100 / 100 | 82.8 (62-105) | 81.8 (57-112) | 48.3 (30-72) | 48.7 (34-66) | 42.3 (16-62) |

**Chip yield 45 / 100.**

- Every functional path works on every chip (scenarios 2, 3, 6, 8 and the silent scenario 1).
- The losses are the two tie tests. On a failing chip the neuron that should stay silent fires
  1-50 times: excitation wins by the chip's mismatch.
- The failures follow the synapse weights, not the presynaptic rates: in 20 of the 34 failing
  scenario-5 runs the inhibitory input in0 fired *more* than in1 (median in1 / in0 0.94,
  range 0.72-1.37). The per-synapse weight spread (DAC branch currents, DPI gain, mirror)
  is larger than the 20 % margin the gain gives.
- One scenario-4 failure (seed 50): in0 (weight 0) fired once at 4 us, before the first pulse
  at 50 us: a power-up spike on that chip, not a synaptic one. Some drawn-netlist chips show the
  same (seed 10: in0 and in1 first spike at 5 us). The network has no reset (README TODO), so the
  start-up state decides it.

### Mirror gain under mismatch (drawn sizes, scenarios 5 and 7, same 100 chips)

`--drawn --mc 100 --only 5,7 --mi2-w <W>`. Only Mi2's width changes, so a seed is the same chip in
every row. Drawn sizes are used here because the extraction cannot be re-sized (a sweep point is
15 min against 90 min post-layout); the drawn netlist at gain 1.2 gives the same scenario 5 / 7
yields as post-layout (65 / 66 against 66 / 67).

| Mi2 W | gain | s5 pass | s7 pass | chip yield (both) | report |
|---|---|---|---|---|---|
| 2u | 1.0 (before the fix) | 54 | 57 | 41 / 100 | [mi2w2u](snn_signed_tb__drawn__mi2w2u__mc100.md) |
| **2.4u** | **1.2 (built)** | **65** | **66** | **51 / 100** | [drawn](snn_signed_tb__drawn__mc100.md) |
| 2.8u | 1.4 | 75 | 74 | 60 / 100 | [mi2w2.8u](snn_signed_tb__drawn__mi2w2.8u__mc100.md) |
| 3.2u | 1.6 | 83 | 77 | 68 / 100 | [mi2w3.2u](snn_signed_tb__drawn__mi2w3.2u__mc100.md) |
| 4u | 2.0 | 87 | 81 | 76 / 100 | [mi2w4u](snn_signed_tb__drawn__mi2w4u__mc100.md) |

- Yield rises steadily with gain but slowly: even at 2x inhibition a quarter of the chips fail.
  In the drawn netlist the input rates also spread widely (in0 9-63 spikes on the same pulses),
  so on some chips the excitatory input fires 2-4x the inhibitory one.
- A higher gain cannot break the other scenarios: none of them needs excitation to beat
  inhibition. It does make every -w weight act as about gain x w.
- Conclusion: an exact +w against -w tie has no reliable winner from chip to chip. Either the
  network's weights need a margin (for example -15 against +12), or the synapse weights need
  trimming or much larger devices. Raising the gain alone trades a symmetric weight scale for
  a partial yield gain.

## Caveats

- **Extraction tool version.** This container's Magic (8.3.684, open_pdks 1689ac3) gives
  9.6 pF total; the committed pre-fix extraction (Magic 8.3.636) had 12.5 pF, mostly from higher
  coupling C. With 8.3.684, `ext2spice lvs` drops all node-to-substrate C (3.7 pF total);
  `top_pex.sh` no longer uses it. An earlier corner campaign on that broken extraction showed
  failures at hot corners; those results were discarded.
- **Schematic device sizes.** The schematic's DPI / neuron devices are 0.22 / 0.28 um, the
  layout's 0.5 / 0.64 um (same W/L). Schematic MC therefore overstates mismatch about 2.3x; use
  the drawn or post-layout MC.
- **Seeds across netlists.** `sw_stat_mismatch` draws per device in netlist order, so seed N is
  the same chip across the drawn gain sweep, but not between the drawn and post-layout netlists.
- **Speed.** Fully tied dummy FETs (D = G = S = B) are removed from the drawn and post-layout
  simulation copies (`drop_tied_dummies`), same results, about 9x faster.
- 100 samples: a yield of 50 % has a 95 % interval of about +/- 10 points.
