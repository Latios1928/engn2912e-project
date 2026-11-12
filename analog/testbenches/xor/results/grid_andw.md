<!-- grid_andw: run_xor.py on 2026-11-12 -->
## XOR on the 2-2-1 network: grid

`xor_tb.sch`, overrides none, 20 input pulses per case. `out_AB`: output spikes for inputs A, B; `in`, `OR`, `AND`: spikes of input 1, hidden 0, hidden 1; `t_*`: first spike after the first pulse (us).

**4 / 10 pass** (output is A XOR B); **3 / 10 strict** (also relays one spike per pulse, AND silent for one input).

| c4+c5 | p_vtau_hid | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass | strict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 0.63 | 0 | 0 | 0 | 0 | 21 | 21/21 | 96 | 124 | 34 | 35 | 70 | – | 45.9 | – | 0 | False | False |
| 2 | 0.64 | 0 | 1 | 1 | 0 | 21 | 21/21 | 75 | 103 | 15 | 15 | 53 | 1221 | 48 | – | 0 | True | False |
| 2 | 0.65 | 0 | 4 | 4 | 0 | 21 | 21/21 | 62 | 83 | 0 | 0 | 41 | 1518 | 52.5 | – | 0 | True | True |
| 2 | 0.66 | 0 | 1 | 1 | 0 | 21 | 21/21 | 42 | 63 | 0 | 0 | 21 | 2777 | 73.6 | – | 0 | True | True |
| 2 | 0.67 | 0 | 1 | 1 | 0 | 21 | 21/21 | 39 | 52 | 0 | 0 | 20 | 3387 | 235 | – | 0 | True | True |
| 3 | 0.63 | 0 | 0 | 0 | 0 | 21 | 21/21 | 96 | 124 | 58 | 58 | 87 | – | 31.8 | – | 0 | False | False |
| 3 | 0.64 | 0 | 0 | 0 | 0 | 21 | 21/21 | 76 | 103 | 39 | 39 | 68 | – | 31.9 | – | 0 | False | False |
| 3 | 0.65 | 0 | 0 | 0 | 0 | 21 | 21/21 | 62 | 84 | 21 | 21 | 52 | – | 32.1 | – | 0 | False | False |
| 3 | 0.66 | 0 | 0 | 0 | 0 | 21 | 21/21 | 42 | 63 | 9 | 9 | 42 | – | 32.4 | – | 0 | False | False |
| 3 | 0.67 | 0 | 0 | 0 | 0 | 21 | 21/21 | 35 | 52 | 0 | 0 | 31 | – | 32.8 | – | 0 | False | False |
