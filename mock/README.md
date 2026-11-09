# Mock modules and pure-digital end-to-end test

Behavioral Verilog stand-ins for the analog blocks, plus a full digital model of
the chip. The same scenarios run on the transistor-level network in
[../mixed/](../mixed/README.md).

| File | What it is |
|---|---|
| `dac.v`, `neuron.v`, `comparator.v`, `pulse_gen.v` | Mocks of the synapse DAC, neuron (with its comparator) and input pulse generator. `dac.v` is binary 1:2:4:8 (`analog/neuron/DAC.sch` is still 1:2:3:4). |
| `snn_mock.v` | The 3-5-1 network from those mocks. Weight word map: words 0–2 pulse → input, 3–17 input i → hidden j (3 + 3j + i), 18–22 hidden j → output (18 + j). |
| `snn_top.v` | `../digital/rf.v` (weights, loaded through `data`/`addr`/`wren`) driving `snn_mock`. LibreLane synthesizes this. |
| `tb_snn_top.v` | End-to-end test: rf readback, then 3 firing scenarios. |
| `tb_neuron.v`, `tb_pulse_gen.v` | Unit tests of the neuron + DAC and of `pulse_gen`. |

Run from this folder:

```bash
iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp ../digital/rf.v *.v && vvp sim.vvp
iverilog -g2012 -Wall -o sim.vvp comparator.v dac.v neuron.v tb_neuron.v && vvp sim.vvp
iverilog -g2012 -Wall -o sim.vvp pulse_gen.v tb_pulse_gen.v && vvp sim.vvp
```

The first command compiles every `.v` here, including the unit testbenches;
`-s tb_snn_top` selects the top.

When a mock gets an analog version, it stays here so the pure-digital test
keeps working.
