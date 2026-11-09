# Mock modules and pure-digital end-to-end test

A behavioral stand-in for the analog network, and the end-to-end test that runs
it with the real chip top from `../digital/`. The same scenarios run on the
transistor-level network in [../mixed/](../mixed/README.md).

`../snn_top.v` instantiates a module named `snn_analog` and does not define
it. Each flow decides which one to compile: this folder's behavioral
`snn_analog.v` (file list `sim.f`), or the empty module in `../mixed/` that
SpiceBind connects to the SPICE network.

| File | What it is |
|---|---|
| `snn_analog.v` | Behavioral `snn_analog`, with the same ports as the analog network (`w[91:0]`, `pulse[2:0]`, `spike[8:0]`). It has no clock or reset input: it generates its own clock (`CLK_PERIOD` ns) and a power-on reset. Built from the three mocks below. Weight word map: words 0–2 pulse → input, 3–17 input i → hidden j (3 + 3j + i), 18–22 hidden j → output (18 + j). |
| `dac.v`, `neuron.v`, `comparator.v` | Mocks of the synapse DAC and neuron (with its comparator, and a leak of `LEAK` per cycle). `dac.v` is binary 1:2:4:8 (`analog/neuron/DAC.sch` is still 1:2:3:4). |
| `tb_snn_top.v` | End-to-end test of `../snn_top.v`: rf readback, then 3 firing scenarios. There is no reset, so each scenario is preceded by a settle time with `in = 0`, as in `../mixed/`. |
| `tb_neuron.v` | Unit test of the neuron (leak included) and the DAC. |
| `sim.f` | File list of this build. |

Run from this folder:

```bash
iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp -f sim.f && vvp sim.vvp
iverilog -g2012 -Wall -o sim.vvp comparator.v dac.v neuron.v tb_neuron.v && vvp sim.vvp
```

Limits of the mock: its timing is not calibrated to the analog network (the
clock, `GAIN`, `DURATION` and `LEAK` are arbitrary), so only which neurons fire
is comparable with `../mixed/`, not when. The scenarios leave no sub-threshold
charge, so they don't exercise the leak end to end; `tb_neuron.v` does.

When a mock gets an analog version, it stays here so the pure-digital test
keeps working.
