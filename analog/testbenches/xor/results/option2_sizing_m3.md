## DPI sizing for option 2 (threshold mode, `size_option2.py`)

DPI alone, 5 kHz train of 10 us pulses, vthr = 2.4 V; vtau at the centre of the nominal range where 15 nA gives no output and 30 nA more than 10 nA. 200 mismatch samples. `yield_<I>nA`: 15 nA below I/3 and 30 nA above 3I. `frac_15n_on`: one input gives more than 0.1 nA; `frac_30n_off`: two inputs give less than 3 nA.

| sizing | k_M1 | k_M2 | k_M3 | k_M4 | area_um2 | vtau_centre | vtau_window_mV | n | yield_1nA | yield_3nA | yield_10nA | frac_15n_on | frac_30n_off | i30_median_nA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| k = 1,1,2,1 | 1 | 1 | 2 | 1 | 0.431 | 0.591 | 22.5 | 200 | 0.83 | 0.82 | 0.815 | 0.095 | 0.085 | 642 |
| k = 1,1,3,1 | 1 | 1 | 3 | 1 | 0.739 | 0.603 | 25 | 200 | 0.95 | 0.945 | 0.945 | 0.005 | 0.045 | 647 |
| k = 1,1,4,1 | 1 | 1 | 4 | 1 | 1.17 | 0.603 | 25 | 200 | 1 | 1 | 1 | 0 | 0 | 708 |
| k = 1,1,6,1 | 1 | 1 | 6 | 1 | 2.4 | 0.607 | 25 | 200 | 1 | 1 | 1 | 0 | 0 | 736 |
