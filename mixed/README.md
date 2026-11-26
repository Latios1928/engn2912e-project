# mixed/

RTL mixed-signal simulation: `../snn_top.v` and `../digital/` run as Verilog in Icarus, and the
analog macro `SNN_signed` runs in ngspice. [SpiceBind](https://themperek.github.io/spicebind)
couples them through the black box `../analog/snn/snn_analog.v`.

The SPICE side is the macro in one of two forms:

- **pre-layout** (default): its LVS reference netlist
  (`analog/layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice`: drawn device sizes, no
  parasitics). `macro_sim.py` makes a simulation copy: the one FET longer than the models allow
  (bias `MR_VK`, 0.5/90.91 µm) is split into series segments, and the MIM cap gets its
  simulation model name;
- **post-layout** (`PEX=1`): its extraction from `SNN_signed.gds`
  (`top/SNN_signed/pex/SNN_signed_pex_sim.spice`, written by
  `analog/testbenches/snn/run_snn_signed.py --pex`). `pex_macro.py` gives it the LVS reference's
  pin order.

`snn_ms_tb.spice` sources `Iref` = 100 nA, `VT` = 1.66 V and VDD = 3.3 V.

## Running

From this folder, in the container:

```bash
make run                              # scenarios 1-8, pre-layout macro, about 30 min
make run PEX=1                        # scenarios 1-8, post-layout macro, about 8 min
make run SCEN_FIRST=3 SCEN_LAST=3     # one scenario
make run IREF=82n                     # another reference current (default 100n)
make run SETTLE=2000 RUN=1500         # shorter windows (us)
make regs                             # ../digital/tb_snn_digital.v
make vcd                              # .raw -> .vcd
make clean
```

`make run` prints the testbench's lines and fails unless the summary says PASS. Log:
`snn_ms_tb[_pex][__iref<IREF>].log` (the first line records the settings). Waveforms: analog in
the `.raw` (supply currents included; `.vcd` after `make vcd`), digital in
`snn_ms_tb[_pex]_digital.vcd`. The same options work in `../librelane/snn_top/gls_ms`, which runs
this testbench on the gate-level netlist.

The scenarios are listed at the top of `snn_ms_tb.v` (the same testbench runs on the gate-level
netlist in `../librelane/snn_top/gls_ms`; results in [signoff](../signoff/README.md)). Each one
loads the weights and signs through the register interface, waits `SETTLE` µs with the inputs off
(the network has no reset pin), then enables the inputs for `RUN` µs. First-spike times include
up to 200 µs of waiting for the next `pulse_gen` period, and shift by tens of µs with history and
pulse phase: which neurons fire is reliable, exact times are not.

## Results

tt, 27 °C, `Iref` 100 nA, `SETTLE` 4 ms, `RUN` 3 ms. All 8 scenarios pass with both macros.
First spike after the inputs are enabled, in µs (`{out, hid1, hid0, in1, in0}` = fired):

| # | Fired | Pre-layout macro | Post-layout macro |
|---|---|---|---|
| 1 | `00000` | none | none |
| 2 | `00001` | in0 449 | in0 410 |
| 3 | `11010` | in1 406 → hid1 647 → out 872 | in1 378 → hid1 566 → out 741 |
| 4 | `01010` | in1 358 → hid1 523 | in1 240 → hid1 341 |
| 5 | `00011` | in1 264, in0 292 | in1 197, in0 274 |
| 6 | `00000` | none | none |
| 7 | `01111` | in0, in1 407 → hid0, hid1 608 | in0, in1 404 → hid0 583, hid1 585 |
| 8 | `11111` | in0, in1 338 → hid0, hid1 558 → out 774 | in0, in1 327 → hid0 460, hid1 491 → out 512 |

The post-layout macro fires at the same time or earlier, as in the gate-level runs (signoff).

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
