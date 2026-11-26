# digital/

RTL of the chip's digital part, `snn_digital` (`regs.v`, `pulse_gen.v`). What it does: the
[main README](../README.md#digital-snn_digital-digital).

## Test

From this folder:

```bash
iverilog -g2012 -Wall -o sim.vvp tb_snn_digital.v snn_digital.v regs.v pulse_gen.v && vvp sim.vvp
```

`tb_snn_digital.v` (12 checks): reset values, weights and signs, the ignored bits of register 14
and the idle address write nothing, the data-change rule, pulse timing changes (taking effect only
from the next period, `width = 0` = no pulses), the input enables sampled only at period boundaries,
and `rst` clearing the enables while keeping weights and signs.

The gate-level netlist of this logic is tested in `../librelane/snn_top/gls`, and the whole chip in
`../mixed/` and `../librelane/snn_top/gls_ms`.
