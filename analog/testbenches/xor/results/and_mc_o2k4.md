<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0

