<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.74', 'vthr_in': '2.5', 'vtau_hid': '0.62', 'vthr_hid': '2.6', 'p_vlk': '0.48'}, DPI scales 1,1,4,1 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 93 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 7 samples [4, 38, 46, 56, 57, 76, 85]
- Two inputs did not fire it: 0 samples []
- Highest VMEM with one input (passing samples, V): mean 0.0007423, std 0.00298, min 6.583e-05, max 0.02421 (n = 93)
- Firing VMEM with two inputs (V): mean 1.569, std 0.0865, min 1.293, max 1.75 (n = 100)
- First spike with two inputs, pulse number: mean 3.15, std 1.94, min 2, max 13 (n = 100)
- Spikes in 50 pulses with two inputs: mean 134.2, std 69.8, min 6, max 338 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 49.84, std 2.78, min 25, max 67 (n = 200)
- False spikes (should be 0): 0

