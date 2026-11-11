<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |

