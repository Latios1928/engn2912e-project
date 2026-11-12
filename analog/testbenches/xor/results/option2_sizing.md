## DPI sizing for option 2 (threshold mode, `size_option2.py`)

DPI alone, 5 kHz train of 10 us pulses, vthr = 2.4 V; vtau at the centre of the nominal range where 15 nA gives no output and 30 nA more than 10 nA. 100 mismatch samples. `yield_<I>nA`: 15 nA below I/3 and 30 nA above 3I. `frac_15n_on`: one input gives more than 0.1 nA; `frac_30n_off`: two inputs give less than 3 nA.

| sizing | k_M1 | k_M2 | k_M3 | k_M4 | area_um2 | vtau_centre | vtau_window_mV | n | yield_1nA | yield_3nA | yield_10nA | frac_15n_on | frac_30n_off | i30_median_nA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all x1 | 1 | 1 | 1 | 1 | 0.246 | 0.497 | 20 | 100 | 0.38 | 0.37 | 0.36 | 0.29 | 0.34 | 404 |
| all x2 | 2 | 2 | 2 | 2 | 0.986 | 0.59 | 25 | 100 | 0.8 | 0.82 | 0.79 | 0.11 | 0.09 | 172 |
| all x3 | 3 | 3 | 3 | 3 | 2.22 | 0.6 | 25 | 100 | 0.96 | 0.96 | 0.92 | 0.01 | 0.03 | 140 |
| all x4 | 4 | 4 | 4 | 4 | 3.94 | 0.601 | 27.5 | 100 | 1 | 1 | 1 | 0 | 0 | 129 |
| all x6 | 6 | 6 | 6 | 6 | 8.87 | 0.607 | 25 | 100 | 1 | 1 | 1 | 0 | 0 | 118 |
| M1 x8 only | 8 | 1 | 1 | 1 | 4.13 | 0.497 | 20 | 100 | 0.38 | 0.37 | 0.36 | 0.29 | 0.34 | 873 |
| M2 x8 only | 1 | 8 | 1 | 1 | 4.13 | 0.496 | 17.5 | 100 | 0.38 | 0.37 | 0.36 | 0.31 | 0.32 | 150 |
| M3 x8 only | 1 | 1 | 8 | 1 | 4.13 | 0.61 | 25 | 100 | 1 | 1 | 1 | 0 | 0 | 730 |
| M4 x8 only | 1 | 1 | 1 | 8 | 4.13 | 0.494 | 17.5 | 100 | 0.37 | 0.36 | 0.27 | 0.3 | 0.34 | 41.3 |
