# mixed/

RTL mixed-signal simulation: `../snn_top.v` and `../digital/` run as Verilog in Icarus, and the
analog macro `SNN_signed` runs in ngspice. [SpiceBind](https://themperek.github.io/spicebind)
couples them through the black box `../analog/snn/snn_analog.v`.

The SPICE side is the macro's LVS reference netlist
(`analog/layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice`, drawn device sizes, no
parasitics). `macro_sim.py` makes a simulation copy of it: the one FET longer than the models allow
(bias `MR_VK`, 0.5/90.91 µm) is split into series segments, and the MIM cap gets its simulation
model name. `snn_ms_tb.spice` sources `Iref` = 100 nA, `VT` = 1.66 V and VDD = 3.3 V.

## Running

From this folder, in the container:

```bash
make run                              # scenarios 1-8, about 58 ms simulated
make run SCEN_FIRST=3 SCEN_LAST=3     # one scenario
make run IREF=82n                     # another reference current (default 100n)
make run SETTLE=2000 RUN=1500         # shorter windows (us)
make regs                             # ../digital/tb_snn_digital.v
make vcd                              # .raw -> .vcd
make clean
```

`make run` prints the testbench's lines and fails unless the summary says PASS. Log:
`snn_ms_tb[__iref<IREF>].log` (the first line records the settings). Waveforms: analog in the
`.raw` (`.vcd` after `make vcd`), digital in `snn_ms_tb_digital.vcd`.

The scenarios are listed at the top of `snn_ms_tb.v` (the same testbench runs on the gate-level
netlist in `../librelane/snn_top/gls_ms`; results in [signoff](../signoff/README.md)). Each one
loads the weights and signs through the register interface, waits `SETTLE` µs with the inputs off
(the network has no reset pin), then enables the inputs for `RUN` µs. First-spike times include
up to 200 µs of waiting for the next `pulse_gen` period, and shift by tens of µs with history and
pulse phase: which neurons fire is reliable, exact times are not.

## Pitfalls

- **ngspice crashes at start with a bus error and no output.** In this container uid 1000 has no
  `/etc/passwd` entry, and `ngSpice_Init` dereferences `getpwuid()` unchecked. The Makefile
  preloads `no_passwd_shim.so`.
- **Verilog-driven nets** must be `external` sources named `V<net>` in the netlist
  (`Vw[5] w[5] 0 0 external`). Outputs are plain nodes.
- **Parameter names.** A `.param` named like a net (e.g. `VT`) makes ngspice rename that net.
  Testbench parameters start with `p_`.
- **`.tran` stop time.** The Verilog `$finish` ends the run, but ngspice reserves memory for
  tstop/step points, so a huge bound segfaults in `OUTpData` at random times. It is set to 65 ms
  (the eight scenarios need about 58 ms); raise it only for longer runs.
- **Time step.** Keep 0.1–0.5 µs. At 0.02 µs SpiceBind came out 4–5 % early while pure ngspice
  did not move.
