# Mixed-signal simulation

The chip at transistor level: `../snn_top.v` (with `../digital/`) runs as
Verilog in Icarus, and the analog macro `SNN_signed` (bias cell + 2-2-1
network) runs in ngspice. [SpiceBind](https://themperek.github.io/spicebind)
couples them: the empty black box `../analog/snn/snn_analog.v` stands in for
the macro, and SpiceBind connects its ports (`w`, `s`, `pulse`, `spike`) to the
SPICE netlist.

The SPICE side is the macro's LVS reference netlist
(`analog/layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice`), so it has the
drawn device sizes. `macro_sim.py` makes a simulation copy of it: the one FET
longer than the models allow (bias `MR_VK`, 0.5/90.91 µm) is split into series
segments, and the MIM cap gets its simulation model name. The macro's other
pins are sources in `snn_ms_tb.spice`: `Iref` = 100 nA, `VT` = 1.66 V, VDD 3.3 V.

## Running

From this folder:

```bash
make run                              # scenarios 1-8, about 58 ms simulated
make run SCEN_FIRST=3 SCEN_LAST=3     # one scenario
make run IREF=82n                     # another reference current (default 100n)
make run SETTLE=2000 RUN=1500         # shorter windows (us)
make regs                             # ../digital/tb_snn_digital.v
make vcd                              # .raw -> .vcd
make clean
```

`make run` prints the testbench's lines and fails unless the summary says
PASS. Log: `snn_ms_tb[__iref<IREF>].log` (the first line records the
settings). Waveforms: analog in the `.raw` (`.vcd` after `make vcd`), digital
in `snn_ms_tb_digital.vcd`.

| # | Synapses (magnitude 15) | `in` | Must fire (`{out, hid[1:0], in[1:0]}`) |
|---|---|---|---|
| 1 | all, excitatory | 00 | nothing |
| 2 | pulse → input only | 01 | `0_00_01` |
| 3 | path in1 → hid1 → out | 11 | `1_10_10` |
| 4 | as 3, hid1 → out = 0 | 11 | `0_10_10` |
| 5 | as 3, plus pulse 0 → in0 and in0 → hid1 inhibitory | 11 | `0_00_11` |

The testbench writes the pulse timing (200 / 10) through the interface, then
for each scenario loads the 8 magnitudes and 2 sign registers, waits `SETTLE`
µs with `in = 0` (the network has no reset pin), and applies `in` for `RUN`
µs. `clk` is 1 µs; `pulse_gen` makes one 10 µs pulse every 200 µs and samples
`in` at period boundaries, so first-spike times include up to 200 µs of
waiting. Maximum time step 0.1 µs.

## Results

2026-11-18, tt, 27 °C, `Iref` 100 nA, `SETTLE` 4000, `RUN` 3000. All five
scenarios pass (36 ms simulated, 17 min). First spike after `in` is applied
(includes the wait for the next `pulse_gen` period, up to 200 µs):

| # | Result | First spikes |
|---|---|---|
| 1 | PASS | none |
| 2 | PASS | in0 463 µs |
| 3 | PASS | in1 436 µs → hid1 683 µs → out 904 µs |
| 4 | PASS | in1 343 µs → hid1 578 µs; out silent |
| 5 | PASS | in1 334 µs, in0 359 µs; hid1 and out silent (inhibition works) |

Scenario 5 could not pass on the earlier unsigned network.

## Limitations

- **Timing depends on history and pulse phase.** Which neurons fire is
  reliable; first-spike times shift by tens of µs between runs. Do not quote
  them as exact.
- **No reset: 4 ms of settle does not empty the membranes.** The leak drains
  about 0.2 mV/µs, so a membrane left near threshold needs about 8 ms. At the
  end of the settle most are at 0.3 mV, but scenario 4 starts with in1 at
  324 mV and the output at 206 mV, scenario 5 with hid1 at 194 mV (threshold
  is about 1.6 V). All scenarios still pass.
- **Time step.** Keep 0.1–0.5 µs. At 0.02 µs SpiceBind came out 4–5 % early
  while pure ngspice did not move; the cause is unknown.
- tt, 27 °C, no parasitics (Latios's `analog/testbenches/snn/` has post-layout
  runs of the macro on its own).

## Pitfalls

- **ngspice crashes at start with a bus error and no output.** In this
  container uid 1000 has no `/etc/passwd` entry, and `ngSpice_Init` dereferences
  `getpwuid()` unchecked. The Makefile preloads `no_passwd_shim.so`.
- **Verilog-driven nets** must be `external` sources named `V<net>` in the
  netlist (`Vw[5] w[5] 0 0 external`). Outputs are plain nodes.
- **Parameter names.** A `.param` named like a net (e.g. `VT`) makes ngspice
  rename that net. Testbench parameters start with `p_`.
- **`.tran` stop time.** The Verilog `$finish` ends the run, but ngspice
  reserves memory for tstop/step points, so a huge bound segfaults in
  `OUTpData`, at random times (1 s did; so did 100 ms on this macro). It is set
  to 65 ms: the eight scenarios need about 58 ms, so raise it only for longer runs.
