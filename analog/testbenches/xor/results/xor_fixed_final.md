<!-- xor_fixed_final: run_xor.py on 2026-11-12 -->
## XOR on the 2-2-1 network: xor

`xor_tb.sch`, overrides none, 20 input pulses per case. `out_AB`: output spikes for inputs A, B; `in`, `OR`, `AND`: spikes of input 1, hidden 0, hidden 1; `t_*`: first spike after the first pulse (us).

**1 / 7 pass** (output is A XOR B); **1 / 7 strict** (also relays one spike per pulse, AND silent for one input).

| corner | temp | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass | strict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 29 | 28 | 0 | 21 | 21/21 | 52 | 72 | 0 | 0 | 31 | 597.7 | 58.2 | – | 0 | True | True |
| ss | 27 | 0 | 0 | 0 | 0 | 24 | 24/24 | 26 | 28 | 24 | 24 | 26 | – | 83.5 | – | 0 | False | False |
| ff | 27 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False | False |
| sf | 27 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False | False |
| fs | 27 | 0 | 0 | 0 | 0 | 208 | 213/213 | 283 | 393 | 132 | 132 | 219 | – | 250.2 | – | 0 | False | False |
| tt | 0 | 0 | 0 | 0 | 0 | 41 | 41/41 | 102 | 110 | 80 | 80 | 93 | – | 42.6 | – | 0 | False | False |
| tt | 85 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False | False |
