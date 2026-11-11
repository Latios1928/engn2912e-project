<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168', 'p_vlk': '0.485'}, DPI scales 8,8,8,8 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 83 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 9 samples [0, 22, 26, 27, 33, 36, 61, 64, 67]
- Two inputs did not fire it: 8 samples [5, 15, 17, 23, 32, 34, 54, 59]
- Highest VMEM with one input (passing samples, V): mean 0.1451, std 0.28, min 0.01695, max 1.384 (n = 91)
- Firing VMEM with two inputs (V): mean 1.663, std 0.0395, min 1.57, max 1.764 (n = 92)
- First spike with two inputs, pulse number: mean 16.45, std 5.84, min 9, max 37 (n = 92)
- Spikes in 50 pulses with two inputs: mean 5.73, std 3.6, min 0, max 19 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 58.08, std 7.7, min 40, max 85 (n = 200)
- False spikes (should be 0): 0

