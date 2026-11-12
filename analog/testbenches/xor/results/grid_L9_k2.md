<!-- grid_L9_k2: run_xor.py on 2026-11-12 -->
## XOR on the 2-2-1 network: grid

`xor_tb.sch`, overrides {'p_vthr_in': '2.2', 'p_vtau_hid': '0.62'}, 10 input pulses per case. `out_AB`: output spikes for inputs A, B; `in`, `OR`, `AND`: spikes of input 1, hidden 0, hidden 1; `t_*`: first spike after the first pulse (us).

**3 / 7 pass.**

| p_vtau_in | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.70 | 0 | 3 | 3 | 0 | 11 | 11/11 | 62 | 79 | 0 | 0 | 24 | 1088 | 440.1 | – | 0 | True |
| 0.71 | 0 | 3 | 3 | 0 | 11 | 11/11 | 62 | 79 | 0 | 0 | 24 | 1086 | 442.4 | – | 0 | True |
| 0.72 | 0 | 3 | 3 | 0 | 11 | 11/11 | 61 | 78 | 0 | 0 | 23 | 1083 | 445.8 | – | 0 | True |
| 0.73 | 0 | 0 | 0 | 0 | 5 | 11/11 | 25 | 78 | 0 | 0 | 25 | – | 444.6 | – | 0 | False |
| 0.74 | 0 | 0 | 0 | 1 | 2 | 5/5 | 9 | 36 | 0 | 0 | 0 | – | – | 2000 | 0 | False |
| 0.75 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False |
| 0.76 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False |
