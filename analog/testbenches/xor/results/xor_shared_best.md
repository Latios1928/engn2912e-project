<!-- xor_shared_best: run_xor.py on 2026-11-12 -->
## XOR on the 2-2-1 network: xor

`xor_tb.sch`, overrides {'p_vthr': '2.45', 'p_vtau': '0.65', 'c0': '5', 'c1': '5', 'c4': '2', 'c5': '2'}, 20 input pulses per case. `out_AB`: output spikes for inputs A, B; `in`, `OR`, `AND`: spikes of input 1, hidden 0, hidden 1; `t_*`: first spike after the first pulse (us).

**1 / 7 pass.**

| corner | temp | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 10 | 10 | 0 | 29 | 29/29 | 86 | 108 | 22 | 22 | 67 | 683.4 | 252.9 | – | 0 | True |
| ss | 27 | 0 | 0 | 0 | 0 | 23 | 23/23 | 27 | 28 | 25 | 25 | 26 | – | 256.3 | – | 0 | False |
| ff | 27 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False |
| sf | 27 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False |
| fs | 27 | 0 | 0 | 0 | 0 | 198 | 200/200 | 406 | 496 | 248 | 248 | 343 | – | 300.2 | – | 0 | False |
| tt | 0 | 0 | 0 | 0 | 0 | 65 | 67/67 | 114 | 118 | 104 | 103 | 109 | – | 232.4 | – | 0 | False |
| tt | 85 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False |
