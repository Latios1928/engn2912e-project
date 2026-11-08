# Mixed-signal simulation

`snn_top` with every block that has an analog version replaced by it. The
digital parts (weight register file, input pulse generators, and a test
sequencer) run as Verilog inside ngspice through one XSPICE `d_cosim` model.
The 3-5-1 network is transistor-level: `analog/snn/snn_analog.sch`, which has
23 `DAC`, 9 `DPI` and 9 `neuron_sized` instances.

| Mock block (`analog/mock/`) | In this simulation |
|---|---|
| `dac.v` | `analog/neuron/DAC.sch` (weights 1:2:3:4, 15 nA unit) |
| `neuron.v` + `comparator.v` | `analog/neuron/DPI.sch` → `analog/neuron/neuron_sized.sch` |
| `pulse_gen.v` | still Verilog (no analog version yet) |
| `../digital/rf.v` | Verilog |

The flow is adapted from CAD7 of ENGN 1600 ([mgyee/engn1600-team1](https://github.com/mgyee/engn1600-team1)),
whose bugs are written up in `../feedback.typ`.

## Running

From this folder:

```bash
make run                              # scenarios 0-4, about 20 ms simulated
make run SCEN_FIRST=3 SCEN_LAST=3     # one scenario
make run SETTLE=500 RUN=1500          # shorter windows (clk cycles of 1 us)
make vcd                              # snn_ms_tb.raw -> snn_ms_tb.vcd (gtkwave / Surfer)
make clean
```

The sequencer prints one line per scenario and a summary to the ngspice log
(`snn_ms_tb.log`); `make run` shows those lines and fails unless the summary
says PASS. The scenarios are those of `../tb_snn_top.v`:

| # | Weights | `in` | Must fire (`{out, hid[4:0], in[2:0]}`) |
|---|---|---|---|
| 0 | word w = w mod 16, then a write to address 31 | – | rf readback only (digital) |
| 1 | all max (code 15) | 000 | nothing |
| 2 | pulse → input only, max | 101 | `0_00000_101` |
| 3 | path in1 → hid2 → out, max | 111 | `1_00100_010` |
| 4 | as 3, hid2 → out = 0 | 111 | `0_00100_010` |

Each scenario loads its 23 words (46 µs), waits `SETTLE` µs with `in = 0`
(the analog network has no reset pin, so the DPIs and membranes have to
decay), then applies `in` for `RUN` µs and records which spikes went high.

Timing: `clk` = 1 µs (rf and sequencer); `clk_analog` = 10 µs, and
`pulse_gen` makes one 10 µs pulse every 20 cycles (5 kHz), as in
`analog/neuron/DACs-DPI-neuron.sch`. Biases are copied from that testbench
(code block SOURCES in `snn_ms_tb.sch`; DPI `Vthr` can be set per layer).

## Results (2026-11-08, tt, 27 °C)

`make run` (all scenarios, 20.4 ms simulated) took 583 s and passed all 5
checks. First spike and number of spikes in each 3 ms run window:

| Scenario | First spike after `in` is applied (spike count) |
|---|---|
| 1 | none |
| 2 | in0, in2: 409 µs (14 each) |
| 3 | in1: 416 µs (14) → hid2: 724 µs (16) → out: 1013 µs (16) |
| 4 | in1: 205 µs (15) → hid2: 352 µs (18); out silent |

The input neurons fire on the 3rd pulse (pulses at 0, 200, 400 µs), close to
the "weight 10 fires on input 2" of `DACs-DPI-neuron` (entry 46), which
counts from the first pulse after a 100 µs delay.

Known limitations:

- **No reset.** The analog network has no reset pin, so a 2 ms settle with
  `in = 0` stands in for one, and it does not empty the membranes. Scenario 4
  starts with in1, hid2 and out at 1.0–1.2 V (threshold 1.66 V), left over
  from scenario 3, so its latencies are shorter. The firing sets still match;
  a longer `SETTLE` or a reset switch on VMEM would make scenarios independent.
- **Start-up.** Hidden 4's membrane starts at ≈ 1.6 V from the operating
  point and leaks to 0 within ≈ 5 ms (scenario 1 starts at 2.1 ms with it at
  0.46 V). Other membranes jump to ≈ 3 V for the first few µs.
- **Mock vs analog DAC.** The mock DAC is binary (1:2:4:8) but `DAC.sch` is
  still 1:2:3:4. The scenarios only use codes 0 and 15, which mean "off" and
  "max" in both.
- Only typical corner, 27 °C, nominal biases.

## Files

| File | Purpose |
|---|---|
| `snn_ms_tb.sch` | Testbench: `snn_analog` + supplies, biases, clocks, models, run control |
| `snn_digital.v` | The one `d_cosim` top: `rf`, 3× `pulse_gen`, `snn_sequencer` |
| `snn_sequencer.v` | Writes the weights, applies `in`, checks the spikes, prints PASS/FAIL |
| `vlnggen.sh` | Builds `snn_digital.so` (replaces ngspice's `vlnggen`, see below) |
| `instantiate.py` | Writes `lib.spice`: the `d_cosim` line in header port order, bridges, net links |
| `raw2vcd.py` | `.raw` → `.vcd`: `name[i]` traces as buses, membrane voltages as analog |
| `Makefile` | Ties it together |

Generated (not in git): `snn_digital.so`, `snn_digital_obj_dir/`,
`lib.spice`, `sim_params.spice` (`tstop`), `build.cfg`, `snn_ms_tb.spice`,
`.raw`, `.vcd`, `.log`.

```
snn_ms_tb.spice          (xschem, netlisted from the project root)
├── snn_ms_tb.sch
│   └── analog/snn/snn_analog.sym/.sch
│       └── analog/neuron/{DAC, DPI, neuron_sized → spike_amplifier}.sch
├── lib.spice            (instantiate.py)
│   ├── snn_digital.so   (vlnggen.sh)
│   │   └── snn_digital.v, snn_sequencer.v, ../digital/rf.v, ../analog/mock/pulse_gen.v
│   └── snn_digital_obj_dir/{inputs,outputs}.h
└── sim_params.spice     (Makefile: tstop from SCEN_*, SETTLE, RUN)
```

## Pitfalls handled here

Found in CAD7 (`../feedback.typ`) or while building this flow:

- **Pin order.** The `.so`'s ports are in the order of
  `snn_digital_obj_dir/inputs.h` / `outputs.h`, not the Verilog order.
  `instantiate.py` reads those headers; never write the `d_cosim` line by hand.
- **One `d_cosim` model.** Several in one netlist were unstable in CAD7, so
  every digital block lives in `snn_digital.v`.
- **`ngspice vlnggen` is broken in ngspice-46**: it lowercases the Verilator
  command line (`--mdir`, `--cflags`, prefix `vlng`) and Verilator rejects it.
  `vlnggen.sh` does the same steps in bash (Verilator → port headers →
  build with ngspice's shim → `g++ --shared`), and also stops on ports over
  64 bits, which `vlnggen` drops without a warning. CAD7's
  `ngspice -b vlnggen` worked with an older ngspice; if a later version fixes
  the lowercasing, the Makefile's `vlnggen.sh` call can go back to it.
- **Ports of at most 31 bits.** The shim reads port bits with `(1 << i)`, and
  ports over 64 bits are skipped silently. The 92-bit weight bus is split into
  `w_at0`, `w_at23`, `w_at46`, `w_at69`; `instantiate.py` maps bit *i* of
  `w_atN` to the analog net `w[N+i]`. (Not `w__N`: Verilator mangles `__`.)
- **Brackets.** XSPICE vectors are written `[ a b ]`, so `w[5]` cannot appear
  in one. The bridges use flat nodes (`a_w_5`) and a 0 V source links each to
  the bracketed net.
- **Parameter names.** A `.param` named like a net (e.g. `VT`) made ngspice
  rename that net to `{vt}` on the long `x1` line, leaving the neuron biases
  floating ("singular matrix: check node {vamp_bias}"). Testbench parameters
  start with `p_`.
- **xschem.** Netlist from the project root with `--rcfile xschemrc` (symbol
  paths), and check the result rather than the exit code (xschem returns 10
  after a good netlist). The Makefile also stops on `IS MISSING` and on
  duplicate `.subckt` names (CAD7: same-named subcircuits silently collapse).
