## Coincidence scan, DPI scale k = 4 (`scan_coincidence.py`)

5 kHz train of 10 us pulses into the DPI alone. `R` = mean output current with 30 nA (two coincident weight-1 inputs) / with 15 nA (one). `window_mV_pred` = 37 mV x ln R, the AND window in Vlk this predicts. `tau_us_15n` = single-spike decay time constant. Idle current subtracted; no response is floored at 1 fA. Mismatch: 100 samples per point; `separable` = largest fraction of samples one common leak current could separate (15 nA below it, 30 nA above); `yield_<I>nA` = fraction with 15 nA below I/3 and 30 nA above 3I, for a leak-equivalent current I.

| vtau | vthr | iavg_15n_nA | iavg_30n_nA | R | window_mV_pred | tau_us_15n | n | sd_ln_i15 | sd_ln_i30 | separable | yield_1nA | yield_3nA | yield_10nA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.595 | 2.4 | 1e-06 | 173 | 7.909e+07 | 672.9 | 173.5 | 100 | 2.992 | 0.2379 | 0.99 | 0.97 | 0.97 | 0.98 |
| 0.595 | 2.5 | 1e-06 | 41.35 | 1.913e+07 | 620.4 | 173.6 | 100 | 2.894 | 0.2998 | 0.99 | 0.97 | 0.98 | 0.82 |
| 0.6 | 2.4 | 1e-06 | 140.2 | 1.274e+08 | 690.5 | 152.3 | 100 | 0 | 0.4928 | 0.99 | 0.99 | 0.99 | 0.99 |
| 0.6 | 2.5 | 1e-06 | 31.84 | 2.883e+07 | 635.5 | 152.4 | 100 | 0 | 0.4899 | 0.99 | 0.99 | 0.98 | 0.55 |
| 0.605 | 2.4 | 1e-06 | 106.3 | 7.104e+07 | 668.9 | 134 | 100 | 0 | 2.141 | 0.99 | 0.98 | 0.97 | 0.97 |
| 0.605 | 2.5 | 1e-06 | 22.33 | 1.547e+07 | 612.5 | 134.1 | 100 | 0 | 1.939 | 0.99 | 0.97 | 0.9 | 0.2 |
