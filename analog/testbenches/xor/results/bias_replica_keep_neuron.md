<!-- bias_replica_keep_VK,VNA,: run_xor.py on 2026-11-12 -->
## XOR with current-referenced biases (bias_replica.py)

Every bias except VT is a diode replica fed by a current calibrated at tt (16 unit copies per subthreshold replica, 1 for VK, VKup, VNA, Vthr_in). Fixed voltages kept: ['VK', 'VNA', 'VKup', 'VKdn', 'VIp', 'Vamp_bias', 'Vlk']. Overrides none. `V_VT_*` = VDD - VT_* (source-gate voltage of the tau pFET) as generated.

| bias | nominal V | per unit copy | x Iref |
|---|---|---|---|
| Vthr | 2.7000 | 0.8307 nA | 0.05761 |
| VT_dpi | 2.7904 | 0.08429 nA | 0.005846 |
| VT_inh | 2.7904 | 0.08429 nA | 0.005846 |
| Vthr_in | 2.2000 | 1214 nA | 84.17 |
| VT_in | 2.5850 | 11.53 nA | 0.7997 |
| Vthr_hid | 2.5000 | 59.33 nA | 4.114 |
| VT_hid | 2.6450 | 3.061 nA | 0.2123 |

**0 / 3 pass** (output is A XOR B); **0 / 3 strict** (also relays one spike per pulse, AND silent for one input).

| iref_scale | corner | temp | sample | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass | strict | V_VT_in | V_Vthr_in | V_VT_hid | V_VT_dpi | V_Vthr | V_Vlk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ss | 27 | – | 0 | 0 | 0 | 0 | 5 | 7/7 | 10 | 13 | 7 | 7 | 13 | – | 446.1 | – | 0 | False | False | 0.8389 | 2.062 | 0.7779 | 0.6299 | 2.578 | – |
| 1 | ff | 27 | – | 0 | 0 | 0 | 0 | 84 | 84/84 | 20 | 104 | 0 | 0 | 0 | – | – | – | 0 | False | False | 0.591 | 2.338 | 0.5321 | 0.3893 | 2.822 | – |
| 1 | fs | 27 | – | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | – | – | – | 0 | False | False | 0.8048 | 2.102 | 0.7442 | 0.5975 | 2.611 | – |
