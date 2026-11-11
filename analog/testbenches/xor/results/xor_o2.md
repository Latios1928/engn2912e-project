<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 8, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory). 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 43 | 255.8 | 3.241 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 106 | 0 | 43 | 255.8 | 3.248 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 7 | 219.3 | 3.247 | False |

