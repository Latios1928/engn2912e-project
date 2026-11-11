<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147', 'p_vlk': '0.485'}, DPI scales 6,6,6,6 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 79 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 15 samples [0, 6, 10, 22, 26, 27, 31, 33, 36, 60, 61, 64, 67, 75, 89]
- Two inputs did not fire it: 6 samples [15, 17, 23, 32, 54, 59]
- Highest VMEM with one input (passing samples, V): mean 0.1658, std 0.23, min 0.0154, max 1.144 (n = 85)
- Firing VMEM with two inputs (V): mean 1.665, std 0.0404, min 1.569, max 1.764 (n = 94)
- First spike with two inputs, pulse number: mean 15.78, std 6.92, min 8, max 48 (n = 94)
- Spikes in 50 pulses with two inputs: mean 6.75, std 4.35, min 0, max 24 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 59.83, std 9.87, min 37, max 93 (n = 200)
- False spikes (should be 0): 0

