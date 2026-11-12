## Coincidence scan, DPI scale k = 1 (`scan_coincidence.py`)

5 kHz train of 10 us pulses into the DPI alone. `R` = mean output current with 30 nA (two coincident weight-1 inputs) / with 15 nA (one). `window_mV_pred` = 37 mV x ln R, the AND window in Vlk this predicts. `tau_us_15n` = single-spike decay time constant. Idle current subtracted; no response is floored at 1 fA. Mismatch: 100 samples per point; `separable` = largest fraction of samples one common leak current could separate (15 nA below it, 30 nA above); `yield_<I>nA` = fraction with 15 nA below I/3 and 30 nA above 3I, for a leak-equivalent current I.

| vtau | vthr | iavg_15n_nA | iavg_30n_nA | R | window_mV_pred | tau_us_15n | n | sd_ln_i15 | sd_ln_i30 | separable | yield_1nA | yield_3nA | yield_10nA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.485 | 2.5 | 0.006009 | 312.5 | 1110 | 259.4 | 52.58 | 100 | 6.987 | 4.065 | 0.48 | 0.42 | 0.43 | 0.43 |
| 0.485 | 2.6 | 0.006005 | 82.44 | 629 | 238.4 | 52.57 | 100 | 6.416 | 3.681 | 0.46 | 0.4 | 0.39 | 0.32 |
| 0.49 | 2.5 | 0.0002385 | 238.8 | 1962 | 280.5 | 47.67 | 100 | 6.771 | 4.567 | 0.52 | 0.45 | 0.44 | 0.4 |
| 0.49 | 2.6 | 0.0002385 | 65.89 | 1135 | 260.3 | 47.66 | 100 | 6.199 | 4.089 | 0.52 | 0.44 | 0.39 | 0.35 |
| 0.495 | 2.5 | 0.0001039 | 168 | 2133 | 283.6 | 43.32 | 100 | 6.559 | 5.179 | 0.63 | 0.41 | 0.4 | 0.39 |
| 0.495 | 2.6 | 0.0001039 | 43.47 | 1277 | 264.6 | 43.31 | 100 | 5.995 | 4.636 | 0.63 | 0.4 | 0.4 | 0.3 |
