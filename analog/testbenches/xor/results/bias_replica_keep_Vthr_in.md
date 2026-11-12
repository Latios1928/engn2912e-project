<!-- bias_replica_keep_Vthr_in: run_xor.py on 2026-11-12 -->
## XOR with current-referenced biases (bias_replica.py)

Every bias except VT is a diode replica fed by a current calibrated at tt (16 unit copies per subthreshold replica, 1 for VK, VKup, VNA, Vthr_in). Fixed voltages kept: ['Vthr_in']. Overrides none. `V_VT_*` = VDD - VT_* (source-gate voltage of the tau pFET) as generated.

| bias | nominal V | per unit copy | x Iref |
|---|---|---|---|
| Vthr | 2.7000 | 0.8307 nA | 0.05761 |
| VT_dpi | 2.7904 | 0.08429 nA | 0.005846 |
| VT_inh | 2.7904 | 0.08429 nA | 0.005846 |
| VT_in | 2.5850 | 11.53 nA | 0.7997 |
| Vthr_hid | 2.5000 | 59.33 nA | 4.114 |
| VT_hid | 2.6450 | 3.061 nA | 0.2123 |
| VNA | 1.9300 | 5049 nA | 350.1 |
| Vlk | 0.4800 | 2.34 nA | 0.1622 |
| VK | 1.2200 | 1.752e+04 nA | 1215 |
| VIp | 0.5730 | 24.02 nA | 1.666 |
| VKup | 2.3500 | 551.3 nA | 38.23 |
| VKdn | 0.5880 | 34.18 nA | 2.37 |
| Vamp_bias | 0.5350 | 96.54 nA | 6.695 |

**0 / 3 pass** (output is A XOR B); **0 / 3 strict** (also relays one spike per pulse, AND silent for one input).

| iref_scale | corner | temp | sample | out_00 | out_01 | out_10 | out_11 | in_01 | in_11 | OR_01 | OR_11 | AND_01 | AND_10 | AND_11 | t_out_01 | t_and_11 | t_out_11 | spurious | pass | strict | V_VT_in | V_Vthr_in | V_VT_hid | V_VT_dpi | V_Vthr | V_Vlk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ss | 27 | – | 0 | 0 | 0 | 2 | 0 | 3/3 | 0 | 9 | 0 | 0 | 0 | – | – | 2670 | 0 | False | False | 0.8389 | – | 0.7779 | 0.6299 | 2.578 | 0.5874 |
| 1 | ff | 27 | – | 0 | 0 | 0 | 0 | 42 | 42/42 | 84 | 105 | 33 | 32 | 63 | – | 33.3 | – | 0 | False | False | 0.591 | – | 0.5321 | 0.3893 | 2.822 | 0.3727 |
| 1 | fs | 27 | – | 0 | 4 | 4 | 16 | 7 | 10/10 | 14 | 30 | 0 | 0 | 0 | 2326 | – | 1041 | 0 | False | False | 0.8048 | – | 0.7442 | 0.5975 | 2.611 | 0.4014 |
