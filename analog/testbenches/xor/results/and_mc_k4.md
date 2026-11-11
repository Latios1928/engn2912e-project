<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'p_vlk': '0.485'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 67 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 19 samples [0, 6, 10, 11, 18, 21, 22, 26, 27, 30, 31, 36, 58, 60, 61, 64, 67, 75, 89]
- Two inputs did not fire it: 14 samples [1, 5, 15, 17, 20, 23, 32, 34, 35, 54, 59, 66, 69, 91]
- Highest VMEM with one input (passing samples, V): mean 0.3289, std 0.445, min 0.01204, max 1.556 (n = 81)
- Firing VMEM with two inputs (V): mean 1.664, std 0.0403, min 1.57, max 1.764 (n = 86)
- First spike with two inputs, pulse number: mean 14.21, std 6.22, min 6, max 43 (n = 86)
- Spikes in 50 pulses with two inputs: mean 7.57, std 6.11, min 0, max 35 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 60.74, std 14.6, min 29, max 112 (n = 200)
- False spikes (should be 0): 0

