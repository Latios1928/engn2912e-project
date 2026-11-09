# Mixed-signal simulation

`snn_top` with every block that has an analog version replaced by it. The
chip top (`../snn_top.v`, with `../digital/snn_digital.v`: weight register file
and input pulse generator) runs as Verilog in Icarus.
The 3-5-1 network is transistor-level in ngspice
(`analog/snn/snn_analog.sch`: 23 `DAC`, 9 `DPI`, 9 `neuron_sized`).
[SpiceBind](https://themperek.github.io/spicebind) couples the two through VPI:
an empty Verilog module, `snn_analog_stub.v`, stands in for the analog block.
The top instantiates `snn_analog` without defining it, so this build compiles the
stub where `../mock/` compiles its behavioral model.

| In `../mock/snn_analog.v` | In this simulation |
|---|---|
| `dac.v` | `analog/neuron/DAC.sch` (weights 1:2:3:4, 15 nA unit) |
| `neuron.v` + `comparator.v` | `analog/neuron/DPI.sch` → `analog/neuron/neuron_sized.sch` |

Everything else is Verilog and shared with `../mock/`: the top `../snn_top.v`
with `snn_digital`.

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
`clk` is 1 µs; `pulse_gen` makes one 10 µs pulse (10 cycles) every 200 µs
(200 cycles). It samples `in` at period boundaries, so the first pulse starts
up to 200 µs after `in` is applied, and the first-spike times below include that. Biases are copied from `analog/neuron/DACs-DPI-neuron.sch` (code
block SOURCES in `snn_ms_tb.sch`). Maximum time step is 0.1 µs.

## Results (2026-11-09, tt, 27 °C)

`make run` (all scenarios, about 20 ms simulated) took 224 s and all 4 passed.
First spike after `in` is applied (these include the wait for the next
`pulse_gen` period, up to 200 µs):

| Scenario | First spikes |
|---|---|
| 1 | none |
| 2 | in0, in2: 518 µs |
| 3 | in1: 479 µs → hid2: 788 µs → out: 1076 µs |
| 4 | in1: 219 µs → hid2: 367 µs; out silent |

Accuracy of the coupling, measured earlier with a pulse generator that started
its first pulse the moment `in` rose: scenario 3 run alone with a 2 ms settle
gave 415 / 727 / 1020 µs through SpiceBind against 412 / 722 / 996 µs in pure
ngspice with ideal sources (within 3 %).

Known limitations:

- **Timing depends on history and pulse phase.** Which neurons fire is
  reliable; first-spike times are less so. With the earlier pulse generator,
  two full runs differing only by a 50 µs time shift gave 393 / 699 / 986 µs
  and 416 / 729 / 1032 µs for scenario 3, and 287 µs and 153 µs for in1 in
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
| `snn_ms_tb.v` | Verilog testbench: instantiates `snn_top`, runs the scenarios and checks the spikes |
| `snn_analog_stub.v` | Empty `snn_analog` that SpiceBind connects to the SPICE network |
| `sim.f` | File list of this build (compare `../mock/sim.f`) |
| `snn_ms_tb.sch` | SPICE side: `snn_analog`, supplies, biases, models, `external` sources for Verilog-driven nets |
| `no_passwd_shim.c` | `LD_PRELOAD` shim for the `libngspice` crash below |
| `Makefile` | Ties it together |

## Pitfalls

- **ngspice crashes at start with a bus error and no output.** In this
  container uid 1000 has no `/etc/passwd` entry, and `ngSpice_Init` dereferences
  `getpwuid()` unchecked. The Makefile preloads `no_passwd_shim.so`.
- **Verilog-driven nets** must be `external` sources named `V<net>` in the
  netlist (`Vw[5] w[5] 0 0 external`). Outputs are plain nodes.
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
