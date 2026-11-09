# Mixed-signal simulation

`snn_top` with every block that has an analog version replaced by it. The
weight register file and the input pulse generators run as Verilog in Icarus.
The 3-5-1 network is transistor-level in ngspice
(`analog/snn/snn_analog.sch`: 23 `DAC`, 9 `DPI`, 9 `neuron_sized`).
[SpiceBind](https://themperek.github.io/spicebind) couples the two through VPI:
an empty Verilog module stands in for the analog block.

| Mock block (`../mock/`) | In this simulation |
|---|---|
| `dac.v` | `analog/neuron/DAC.sch` (weights 1:2:3:4, 15 nA unit) |
| `neuron.v` + `comparator.v` | `analog/neuron/DPI.sch` → `analog/neuron/neuron_sized.sch` |
| `pulse_gen.v` | still Verilog (no analog version yet) |
| `../digital/rf.v` | Verilog |

## Running

From this folder:

```bash
make run                              # scenarios 1-4, about 20 ms simulated
make run SCEN_FIRST=3 SCEN_LAST=3     # one scenario
make run SETTLE=500 RUN=1500          # shorter windows (us)
make vcd                              # snn_ms_tb.raw -> snn_ms_tb.vcd
make clean
```

`make run` prints the testbench's lines and fails unless the summary says
PASS. The full log is `snn_ms_tb.log`. Waveforms: analog in `snn_ms_tb.raw`
(`.vcd` after `make vcd`, using xschem's `rawtovcd`; every trace is analog,
so `spike[0..8]` are separate traces), digital in `snn_ms_tb_digital.vcd`.

| # | Weights | `in` | Must fire (`{out, hid[4:0], in[2:0]}`) |
|---|---|---|---|
| 1 | all max (code 15) | 000 | nothing |
| 2 | pulse → input only, max | 101 | `0_00000_101` |
| 3 | path in1 → hid2 → out, max | 111 | `1_00100_010` |
| 4 | as 3, hid2 → out = 0 | 111 | `0_00100_010` |

Each scenario loads its 23 words (46 µs), waits `SETTLE` µs with `in = 0`
(the analog network has no reset pin), then applies `in` for `RUN` µs.
`clk` is 1 µs; `clk_analog` is 10 µs, and `pulse_gen` makes one 10 µs pulse
every 200 µs. Biases are copied from `analog/neuron/DACs-DPI-neuron.sch` (code
block SOURCES in `snn_ms_tb.sch`). Maximum time step is 0.1 µs.

## Results (2026-11-08, tt, 27 °C)

`make run` (all scenarios, about 20 ms simulated) took 221 s and all 4 passed.
First spike after `in` is applied:

| Scenario | First spikes |
|---|---|
| 1 | none |
| 2 | in0, in2: 383 µs |
| 3 | in1: 416 µs → hid2: 729 µs → out: 1032 µs |
| 4 | in1: 153 µs → hid2: 298 µs; out silent |

Accuracy, scenario 3 run alone with a 2 ms settle, against pure ngspice with
ideal sources: SpiceBind 415 / 727 / 1020 µs, pure ngspice 412 / 722 / 996 µs
(within 3 %).

Known limitations:

- **Timing depends on history.** Which neurons fire is reliable; first-spike
  times are less so. Two full runs differing only by a 50 µs time shift (an
  extra digital-only scenario at the start) gave 393 / 699 / 986 µs and
  416 / 729 / 1032 µs for scenario 3, and 287 µs and 153 µs for in1 in
  scenario 4. Do not quote first-spike times from one sequence as exact.
- **Time step.** Keep 0.1–0.5 µs. At 0.02 µs SpiceBind came out 4–5 % early
  while pure ngspice did not move; the cause is unknown.
- **No reset.** A 2 ms settle does not empty the membranes, so scenario 4
  starts from what scenario 3 left. A longer `SETTLE` or a reset switch on
  VMEM would make scenarios independent.
- **Start-up.** Unused membranes start far from 0 at the operating point and
  take a few ms to leak away.
- **Mock vs analog DAC.** The mock DAC is binary (1:2:4:8) but `DAC.sch` is
  still 1:2:3:4. The scenarios only use codes 0 and 15.
- Only typical corner, 27 °C, nominal biases. SpiceBind itself is early-stage.

## Files

| File | Purpose |
|---|---|
| `snn_ms_tb.v` | Verilog top: `rf`, 3× `pulse_gen`, empty `snn_analog`, scenarios and checks |
| `snn_ms_tb.sch` | SPICE side: `snn_analog`, supplies, biases, models, `external` sources for Verilog-driven nets |
| `no_passwd_shim.c` | `LD_PRELOAD` shim for the `libngspice` crash below |
| `Makefile` | Ties it together |

## Pitfalls

- **ngspice crashes at start with a bus error and no output.** In this
  container uid 1000 has no `/etc/passwd` entry, and `ngSpice_Init` dereferences
  `getpwuid()` unchecked. The Makefile preloads `no_passwd_shim.so`.
- **Verilog-driven nets** must be `external` sources named `V<net>` in the
  netlist (`Vw[5] w[5] 0 0 external`). Outputs are plain nodes.
- **Raising `en` of `pulse_gen` mid-cycle** shortens the first pulse, because
  its output is combinational in `en`. The testbench changes `in` just after a
  rising `clk_analog` edge.
- **Parameter names.** A `.param` named like a net (e.g. `VT`) made ngspice
  rename that net to `{vt}` on the long `x1` line, leaving the neuron biases
  floating ("singular matrix: check node {vamp_bias}"). Testbench parameters
  start with `p_`.
- **`.tran` stop time.** The Verilog `$finish` ends the run, but ngspice
  reserves memory for tstop/step points, so a huge bound segfaults in
  `OUTpData` depending on free memory (1 s did). It is set to 100 ms; raise
  it only if a run gets longer.
- **xschem.** Netlist from the project root with `--rcfile xschemrc`, and check
  the result rather than the exit code (xschem returns 10 after a good
  netlist). The Makefile also stops on `IS MISSING` and on duplicate `.subckt`
  names (CAD7: same-named subcircuits silently collapse).
