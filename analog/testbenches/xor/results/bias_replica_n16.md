<!-- bias_replica_n16: run_xor.py on 2026-11-12 -->
## XOR with current-referenced biases (bias_replica.py)

Every bias except VT is a diode replica fed by a current calibrated at tt (16 unit copies per subthreshold replica, 1 for VK, VKup, VNA). Fixed voltages kept: none. Overrides none. `V_VT_*` = VDD - VT_* (source-gate voltage of the tau pFET) as generated.

| bias | nominal V | per unit copy | x Iref |
|---|---|---|---|
| Vthr | 2.7000 | 0.8307 nA | 0.05761 |
| VT_dpi | 2.7904 | 0.08429 nA | 0.005846 |
| VT_inh | 2.7904 | 0.08429 nA | 0.005846 |
| Vthr_in | 2.4000 | 244.5 nA | 16.95 |
| VT_in | 2.6050 | 7.502 nA | 0.5202 |
| Vthr_hid | 2.5000 | 59.33 nA | 4.114 |
| VT_hid | 2.6450 | 3.061 nA | 0.2123 |
| VNA | 1.9300 | 5049 nA | 350.1 |
| Vlk | 0.4800 | 2.34 nA | 0.1622 |
| VK | 1.2200 | 1.752e+04 nA | 1215 |
| VIp | 0.5730 | 24.02 nA | 1.666 |
| VKup | 2.3500 | 551.3 nA | 38.23 |
| VKdn | 0.5880 | 34.18 nA | 2.37 |
| Vamp_bias | 0.5350 | 96.54 nA | 6.695 |

**7 / 7 pass** (output is A XOR B); **6 / 7 strict** (also relays one spike per pulse, AND silent for one input).

| iref_scale | corner | temp | sample | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass | strict | V_VT_in | V_Vthr_in | V_VT_hid | V_VT_dpi | V_Vthr | V_Vlk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | tt | 27 | – | 0 | 29 | 29 | 0 | 21 | 21/21 | 52 | 70 | 0 | 0 | 31 | 599.3 | 56.8 | – | 0 | True | True | 0.695 | 2.4 | 0.655 | 0.5096 | 2.7 | 0.48 |
| 1 | ss | 27 | – | 0 | 4 | 4 | 0 | 7 | 10/10 | 14 | 30 | 0 | 0 | 5 | 2117 | 650.9 | – | 0 | True | False | 0.8185 | 2.271 | 0.7779 | 0.6299 | 2.578 | 0.5874 |
| 1 | ff | 27 | – | 0 | 30 | 30 | 0 | 21 | 21/21 | 52 | 82 | 0 | 0 | 31 | 569.6 | 47 | – | 0 | True | True | 0.5714 | 2.529 | 0.5321 | 0.3893 | 2.822 | 0.3727 |
| 1 | sf | 27 | – | 0 | 31 | 31 | 0 | 21 | 21/21 | 52 | 73 | 0 | 0 | 31 | 546.3 | 42.8 | – | 0 | True | True | 0.6054 | 2.493 | 0.5658 | 0.4217 | 2.789 | 0.5587 |
| 1 | fs | 27 | – | 0 | 26 | 26 | 0 | 21 | 21/21 | 50 | 69 | 0 | 0 | 30 | 673 | 239.2 | – | 0 | True | True | 0.7846 | 2.307 | 0.7442 | 0.5975 | 2.611 | 0.4014 |
| 1 | tt | 0 | – | 0 | 24 | 24 | 0 | 21 | 21/21 | 44 | 64 | 0 | 0 | 27 | 672.1 | 231.1 | – | 0 | True | True | 0.7329 | 2.377 | 0.6962 | 0.5634 | 2.654 | 0.5255 |
| 1 | tt | 85 | – | 0 | 35 | 35 | 0 | 21 | 21/21 | 62 | 82 | 0 | 0 | 41 | 507.5 | 43.1 | – | 0 | True | True | 0.6127 | 2.45 | 0.5655 | 0.3932 | 2.8 | 0.3821 |
