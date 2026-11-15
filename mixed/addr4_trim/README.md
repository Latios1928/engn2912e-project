# addr4_trim: 4-bit address interface + trim, mixed-signal

An experiment beside `mixed/`, which is unchanged: no existing file in the repo is
modified, and every module here has a `_v2` name.

- **Digital:** `addr[3:0]` with no `wren` pin. `addr = 4'hF` is idle, and any other
  address writes `data` on every rising clock edge. Pulse timing and a trim code
  are now registers.
- **Analog:** the network's biases come from the real `bias_cell` (the cell in
  `SNN.gds`) instead of fixed voltage sources. Its reference current `Iref` comes
  from a Verilog-A model, `trim_iref.va`, set by the trim register. The trim law
  is that of Luz's `analog/bias/bias_gen.py`.

```
trim register ─ trim[3:0] ─► trim_iref.va ── Iref ──► bias_cell ──► biases ──► snn_analog
  (Verilog)                  (Verilog-A)                (transistors)            (transistors)
```

## Register map (`regs_v2.v`)

| addr | register | reset |
|---|---|---|
| 0–7 | weight words 0–7 (same `w` bus as `digital/rf.v`) | none |
| 8, 9 | pulse PERIOD [3:0], [7:4] | 200 |
| 10, 11 | pulse WIDTH [3:0], [7:4] | 10 |
| 12 | trim code | 9 |
| 13, 14 | debug 0, 1 (not used yet) | 0 |
| 15 | **idle**: no write | |

**Write protocol:** rest at `addr = 1111` (with pad pull-ups, an undriven bus is
idle). Set `data`, then set `addr` for one clock, then return to 1111. Change
`data` only while idle: data that changes while an address is held does get
written. Same pin count as `snn_top.v` (17): `wren` became `addr[3]`.

New PERIOD/WIDTH values take effect at the next period boundary, so a pulse is
never cut or stretched. `period = 0` means 256 cycles, and `width = 0` means no pulses.

## Files

| File | Replaces (unchanged) | Role |
|---|---|---|
| `regs_v2.v` | `digital/rf.v` | register map above |
| `pulse_gen_v2.v` | `digital/pulse_gen.v` | pulse generator with PERIOD/WIDTH inputs. Matches `pulse_gen.v` exactly at 200/10 (0 mismatches in 20,000 random cycles) |
| `snn_digital_v2.v`, `snn_top_v2.v` | `digital/snn_digital.v`, `snn_top.v` | wiring. `trim[3:0]` runs inside the chip to the analog block |
| `snn_analog_v2.v` | `analog/snn/snn_analog.v` | black box with a `trim[3:0]` port, for SpiceBind |
| `trim_iref.va` | — | trim bits → `Iref`: 71 / 100 / 136 nA at codes 0 / 9 / 15, `perr` = process error, `imon` = copy of `Iref` |
| `snn_ms_tb_v2.sch` | `mixed/snn_ms_tb.sch` | SPICE side: `trim_iref` → `bias_cell` → `snn_analog` (all schematics, no parasitics) |
| `snn_ms_tb_v2.v` | `mixed/snn_ms_tb.v` | Verilog side, scenarios 1–6 |
| `tb_regs_v2.v` | — | digital-only register test |
| `Makefile`, `sim.f` | `mixed/Makefile`, `mixed/sim.f` | build and run |

## Running (in the container, from this folder)

```bash
make regs                                                 # digital only, ~1 s
make run                                                  # scenarios 1-6, ~37 ms simulated
make run SCEN_FIRST=6 SCEN_LAST=6                         # trim scenario only
make run SCEN_FIRST=6 SCEN_LAST=6 PERR=0.82 TRIM="9 13"   # slow chip, then trimmed back
```

`TRIM`: up to 4 codes for scenario 6. `PERR`: process error of `Iref`
(`p_perr` in the schematic). Outputs: `snn_ms_tb_v2[__perr<PERR>].log/.raw`. The
first line of each log records the settings. The Makefile compiles `trim_iref.va`
with OpenVAF, and the netlist loads it with `pre_osdi`.

## Results (2026-11-14, tt, 27 °C)

**Digital (`make regs`):** all 9 checks pass. They cover reset values, every
register, idle writes nothing, the data-change rule, and the pulse timing changes.

**Trim → biases** (operating point, real `bias_cell`):

| trim | chip | Iref | Vb | Vlk | VKdn | Vthr |
|---|---|---|---|---|---|---|
| 0 | typical | 71.4 nA | 0.600 | 0.413 | 0.574 | 2.921 |
| 9 | typical | 100.0 nA | 0.616 | 0.425 | 0.588 | 2.909 |
| 15 | typical | 136.4 nA | 0.632 | 0.436 | 0.601 | 2.897 |
| 9 | slow (perr 0.82) | 82.0 nA | 0.606 | 0.418 | 0.580 | 2.916 |
| 13 | slow (perr 0.82) | 99.8 nA | 0.616 | 0.425 | 0.588 | 2.909 |

At trim 9 the biases equal the fixed voltages of `mixed/`. A slow chip trimmed to
code 13 is back within about 0.1 mV of nominal (an ff-like chip, perr 1.28, needs
code 3).

**`make run`** (about 20 min, sharing the CPU with another sweep):

| Scenario | Result | First spikes | Original `mixed/` |
|---|---|---|---|
| 1 all weights max, in = 00 | PASS | none | none |
| 2 pulse → input 0 | PASS | in0 797 µs | 826 µs |
| 3 in1 → hid1 → out | PASS | 734 → 1376 → 2088 µs | 774 → 1456 → 2223 µs |
| 4 as 3, hid1 → out = 0 | PASS | 500 → 961 µs, out silent | 566 → 1091 µs |
| 5 inhibition at hid1 | FAIL (expected) | in1 493, in0 682 → hid1 711 → out 1110 µs | same FAIL |
| 6 trim 9 vs 15, input 0 | PASS | 496 µs, 9 spikes / 3 ms vs 336 µs, 11 spikes | — |

Scenarios 1–4 fire the same neurons as `mixed/`. The first spikes come slightly
earlier, which is within the history and phase spread noted in `mixed/README.md`.
A higher trim makes the input neuron fire sooner and more often.

## Known issues / next

- **Scenario 5 can't pass with this schematic.** `snn_analog.sch` uses the unsigned
  `DAC`, so −7 (`1111`) excites. The layout is built from `snn_analog_inh.sch`:
  `DAC_signed` on the two hidden → output synapses (words 6, 7), a `DPI_inh` on the
  output, and separate sign pins `s[1:0]` (not bit 3), which nothing drives yet.
  So inhibition only exists at the output, not at hidden 1.
  **Plan:** use `snn_analog_inh.sym` here, add a sign register (address 13 →
  `s[1:0]`), and redefine scenario 5 as hid0 excitatory + hid1 inhibitory into the
  output: expect the output silent with s = 01 and firing with s = 00.
- **The 2 ms `SETTLE` doesn't empty the membranes.** The leak drains about 0.5 mV/µs,
  so it takes about 3.2 ms from threshold. In scenario 5, input 1 started at 0.72 V
  (left over from scenario 4) and input 0 at 0 V, so they fired one pulse (200 µs)
  apart for the whole run. Use `SETTLE` ≥ 4000.
- Everything is simulated from schematics (no parasitics), at tt, 27 °C only.
- OpenVAF has no `transition()`, so the trim bits use a smooth threshold
  (`tanh`) instead.
