<!-- xor_mc: run_xor.py on 2026-11-11 -->
## XOR with mismatch (`xor_tb`)

27 / 30 samples give the right output in all 4 cases.

- A=0 B=0: output spikes mean 0, std 0, min 0, max 0 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=0 B=1: output spikes mean 6.167, std 2.63, min 1, max 13 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=1 B=0: output spikes mean 6.433, std 2.69, min 1, max 13 (n = 30); AND spikes mean 0.1333, std 0.73, min 0, max 4 (n = 30); wrong in samples []
- A=1 B=1: output spikes mean 0.1, std 0.305, min 0, max 1 (n = 30); AND spikes mean 35, std 9.15, min 14, max 55 (n = 30); wrong in samples [8, 20, 22]

