## Coincidence scan, DPI scale k = 4 (`scan_coincidence.py`)

5 kHz train of 10 us pulses into the DPI alone. `R` = mean output current with 30 nA (two coincident weight-1 inputs) / with 15 nA (one). `window_mV_pred` = 37 mV x ln R, the AND window in Vlk this predicts. `tau_us_15n` = single-spike decay time constant. Idle current subtracted; no response is floored at 1 fA. Mismatch: 100 samples per point; `separable` = largest fraction of samples one common leak current could separate (15 nA below it, 30 nA above).

| vtau | vthr | iavg_15n_nA | iavg_30n_nA | R | window_mV_pred | tau_us_15n | n | sd_ln_i15 | sd_ln_i30 | separable |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.59 | 2.5 | 1e-06 | 50.97 | 6.399e+05 | 494.7 | 197.2 | 100 | 6.779 | 0.2517 | 0.99 |
| 0.595 | 2.5 | 1e-06 | 41.35 | 1.913e+07 | 620.4 | 173.6 | 100 | 2.894 | 0.2998 | 0.99 |
| 0.6 | 2.5 | 1e-06 | 31.84 | 2.883e+07 | 635.5 | 152.4 | 100 | 0 | 0.4899 | 0.99 |
| 0.605 | 2.5 | 1e-06 | 22.33 | 1.547e+07 | 612.5 | 134.1 | 100 | 0 | 1.939 | 0.99 |
| 0.61 | 2.5 | 1e-06 | 13.06 | 3.262e+06 | 554.9 | 117.9 | 100 | 0 | 3.842 | 0.99 |
