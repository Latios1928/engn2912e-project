# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


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


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 1, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory), {'p_vthr': 2.785}. 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 6 | 1070 | 3.245 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 105 | 0 | 6 | 1068 | 3.245 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 0 | – | 0.5308 | True |
| ss | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.007745 | True |
| ss | 27 | 0 | 1 | 1 | 0 | 20 | 27 | 23 | 0 | – | 0.01467 | False |
| ss | 27 | 1 | 0 | 1 | 20 | 0 | 27 | 23 | 0 | – | 0.01466 | False |
| ss | 27 | 1 | 1 | 0 | 20 | 20 | 29 | 25 | 0 | – | 0.00922 | True |
| ff | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | True |
| ff | 27 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | False |
| ff | 27 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | False |
| ff | 27 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | True |
| sf | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.0006106 | True |
| sf | 27 | 0 | 1 | 1 | 0 | 3 | 6 | 0 | 2 | 2319 | 2.353 | True |
| sf | 27 | 1 | 0 | 1 | 3 | 0 | 6 | 0 | 2 | 2319 | 2.365 | True |
| sf | 27 | 1 | 1 | 0 | 5 | 5 | 10 | 5 | 0 | – | 0.0366 | True |
| fs | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 8.024e-05 | True |
| fs | 27 | 0 | 1 | 1 | 0 | 108 | 332 | 65 | 0 | – | 0.003446 | False |
| fs | 27 | 1 | 0 | 1 | 108 | 0 | 332 | 65 | 0 | – | 0.003445 | False |
| fs | 27 | 1 | 1 | 0 | 113 | 113 | 440 | 137 | 0 | – | 0.003563 | True |
| tt | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.001098 | True |
| tt | 0 | 0 | 1 | 1 | 0 | 20 | 106 | 68 | 0 | – | 0.1858 | False |
| tt | 0 | 1 | 0 | 1 | 20 | 0 | 106 | 67 | 0 | – | 0.1857 | False |
| tt | 0 | 1 | 1 | 0 | 20 | 20 | 114 | 85 | 0 | – | 0.009429 | True |
| tt | 85 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | True |
| tt | 85 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | False |
| tt | 85 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | False |
| tt | 85 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | True |


<!-- xor_mc: run_xor.py on 2026-11-11 -->
## XOR with mismatch (`xor_tb`)

27 / 30 samples give the right output in all 4 cases.

- A=0 B=0: output spikes mean 0, std 0, min 0, max 0 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=0 B=1: output spikes mean 6.167, std 2.63, min 1, max 13 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=1 B=0: output spikes mean 6.433, std 2.69, min 1, max 13 (n = 30); AND spikes mean 0.1333, std 0.73, min 0, max 4 (n = 30); wrong in samples []
- A=1 B=1: output spikes mean 0.1, std 0.305, min 0, max 1 (n = 30); AND spikes mean 35, std 9.15, min 14, max 55 (n = 30); wrong in samples [8, 20, 22]


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 8, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory). 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 43 | 255.8 | 3.241 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 106 | 0 | 43 | 255.8 | 3.248 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 7 | 219.3 | 3.247 | False |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


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


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 1, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory), {'p_vthr': 2.785}. 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 6 | 1070 | 3.245 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 105 | 0 | 6 | 1068 | 3.245 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 0 | – | 0.5308 | True |
| ss | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.007745 | True |
| ss | 27 | 0 | 1 | 1 | 0 | 20 | 27 | 23 | 0 | – | 0.01467 | False |
| ss | 27 | 1 | 0 | 1 | 20 | 0 | 27 | 23 | 0 | – | 0.01466 | False |
| ss | 27 | 1 | 1 | 0 | 20 | 20 | 29 | 25 | 0 | – | 0.00922 | True |
| ff | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | True |
| ff | 27 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | False |
| ff | 27 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | False |
| ff | 27 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | – | 5.911e-06 | True |
| sf | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.0006106 | True |
| sf | 27 | 0 | 1 | 1 | 0 | 3 | 6 | 0 | 2 | 2319 | 2.353 | True |
| sf | 27 | 1 | 0 | 1 | 3 | 0 | 6 | 0 | 2 | 2319 | 2.365 | True |
| sf | 27 | 1 | 1 | 0 | 5 | 5 | 10 | 5 | 0 | – | 0.0366 | True |
| fs | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 8.024e-05 | True |
| fs | 27 | 0 | 1 | 1 | 0 | 108 | 332 | 65 | 0 | – | 0.003446 | False |
| fs | 27 | 1 | 0 | 1 | 108 | 0 | 332 | 65 | 0 | – | 0.003445 | False |
| fs | 27 | 1 | 1 | 0 | 113 | 113 | 440 | 137 | 0 | – | 0.003563 | True |
| tt | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.001098 | True |
| tt | 0 | 0 | 1 | 1 | 0 | 20 | 106 | 68 | 0 | – | 0.1858 | False |
| tt | 0 | 1 | 0 | 1 | 20 | 0 | 106 | 67 | 0 | – | 0.1857 | False |
| tt | 0 | 1 | 1 | 0 | 20 | 20 | 114 | 85 | 0 | – | 0.009429 | True |
| tt | 85 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | True |
| tt | 85 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | False |
| tt | 85 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | False |
| tt | 85 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | – | 1.273e-05 | True |


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 8, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory). 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 43 | 255.8 | 3.241 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 106 | 0 | 43 | 255.8 | 3.248 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 7 | 219.3 | 3.247 | False |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


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


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 8, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory). 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 7.573e-05 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 20 | 106 | 0 | 43 | 255.8 | 3.241 | True |
| tt | 27 | 1 | 0 | 1 | 20 | 0 | 106 | 0 | 43 | 255.8 | 3.248 | True |
| tt | 27 | 1 | 1 | 0 | 20 | 20 | 139 | 34 | 7 | 219.3 | 3.247 | False |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


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


<!-- xor: run_xor.py on 2026-11-11 -->
## XOR on the full network (`xor_tb`)

Weights: {'c0': 15, 'c1': 15, 'c3': 15, 'c4': 15, 'c6': 1, 'c7': 1, 'c18': 8, 'c19': 15}, signs {'s0': 0, 's1': 1} (s1 = 1: hidden 1 -> output inhibitory). 4 ms (20 pulses) per case, membranes start at 0 V. `n0`, `n1`: input relays; `n3` = hidden 0 (OR); `n4` = hidden 1 (AND); `n8` = output. Pass = output fires if and only if A XOR B.

| corner | temp | A | B | XOR | n0 | n1 | n3 | n4 | n8 | t_out_us | vmax_out | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tt | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – | 0.001474 | True |
| tt | 27 | 0 | 1 | 1 | 0 | 47 | 95 | 103 | 10 | 747.1 | 3.238 | True |
| tt | 27 | 1 | 0 | 1 | 47 | 0 | 95 | 102 | 10 | 745.9 | 3.243 | True |
| tt | 27 | 1 | 1 | 0 | 57 | 57 | 109 | 142 | 0 | – | 0.06888 | True |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


<!-- and_mc: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_in': '0.72', 'vthr_in': '2.4', 'vtau_hid': '0.6225', 'vthr_hid': '2.5', 'p_vlk': '0.48'}, DPI scales 4,4,4,4 -->
## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 96 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 3 samples [46, 76, 85]
- Two inputs did not fire it: 1 samples [59]
- Highest VMEM with one input (passing samples, V): mean 0.001461, std 0.00972, min 5.851e-05, max 0.07922 (n = 97)
- Firing VMEM with two inputs (V): mean 1.6, std 0.0545, min 1.467, max 1.718 (n = 99)
- First spike with two inputs, pulse number: mean 4.444, std 2.36, min 2, max 23 (n = 99)
- Spikes in 50 pulses with two inputs: mean 80.17, std 28.1, min 0, max 143 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 50, std 0, min 50, max 50 (n = 200)
- False spikes (should be 0): 0


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.62', 'vthr_hid': '2.4', 'vtau_in': '0.62', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 571 | – | 614 | 1 | – | 415 | 0 |  |
| 0.48 | 1 | 569 | – | 614 | 1 | – | 411 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.61', 'vthr_hid': '2.4', 'vtau_in': '0.61', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 599 | – | 634 | 1 | – | 498 | 1 |  |
| 0.48 | 1 | 598 | – | 634 | 1 | – | 498 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4', 'vtau_in': '0.60', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 619 | – | 648 | 1 | – | 548 | 1 |  |
| 0.48 | 1 | 620 | – | 648 | 1 | – | 548 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.59', 'vthr_hid': '2.4', 'vtau_in': '0.59', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 629 | – | 659 | 1 | – | 586 | 0 |  |
| 0.48 | 1 | 628 | – | 659 | 1 | – | 585 | 2 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.58', 'vthr_hid': '2.4', 'vtau_in': '0.58', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 637 | – | 668 | 1 | – | 611 | 1 |  |
| 0.48 | 1 | 636 | – | 668 | 1 | – | 611 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.57', 'vthr_hid': '2.4', 'vtau_in': '0.57', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 649 | – | 675 | 1 | – | 631 | 0 |  |
| 0.48 | 1 | 649 | – | 675 | 1 | – | 630 | 1 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.56', 'vthr_hid': '2.4', 'vtau_in': '0.56', 'vthr_in': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.44 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |
| 0.48 | 1 | 657 | – | 686 | 1 | – | 646 | 1343 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096', 'vtau_hid': '0.60', 'vthr_hid': '2.4'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 363 | – | 487 | 3 | – | 71 | 779 |  |
| 0.4 | 10 | 605 | – | 647 | 2 | – | 71 | 1252 |  |
| 0.42 | 1 | 359 | – | 485 | 3 | – | 70 | 771 |  |
| 0.42 | 10 | 603 | – | 647 | 2 | – | 70 | 1250 |  |
| 0.44 | 1 | 353 | – | 478 | 3 | – | 68 | 756 |  |
| 0.44 | 10 | 601 | – | 643 | 2 | – | 68 | 1244 |  |
| 0.46 | 1 | 337 | – | 470 | 4 | – | 65 | 722 |  |
| 0.46 | 10 | 595 | – | 639 | 2 | – | 65 | 1234 |  |
| 0.48 | 1 | 304 | – | 453 | 5 | – | 60 | 640 |  |
| 0.48 | 10 | 584 | – | 630 | 3 | – | 60 | 1214 |  |
| 0.5 | 1 | 235 | – | 419 | 5 | – | 52 | 509 |  |
| 0.5 | 10 | 564 | – | 613 | 3 | – | 52 | 1176 |  |
| 0.52 | 1 | 0 | 0.04983 | 333 | 7 | – | 39 | 254 | yes |
| 0.52 | 10 | 499 | – | 568 | 4 | – | 39 | 1054 |  |
| 0.54 | 1 | 0 | 1.754e-05 | 0 | – | 0.003951 | 15 | 0 |  |
| 0.54 | 10 | 205 | – | 300 | 7 | – | 15 | 443 |  |
| 0.56 | 1 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |
| 0.56 | 10 | 0 | 1.081e-05 | 0 | – | 1.081e-05 | 0 | 0 |  |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


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


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.06792 | 9 | 12 | – | 58 | 0 | yes |
| 0.48 | 2 | 8 | – | 31 | 7 | – | 58 | 0 |  |
| 0.48 | 3 | 19 | – | 50 | 5 | – | 58 | 0 |  |
| 0.48 | 4 | 29 | – | 71 | 5 | – | 58 | 0 |  |
| 0.485 | 1 | 0 | 0.04075 | 7 | 14 | – | 57 | 0 | yes |
| 0.485 | 2 | 6 | – | 28 | 7 | – | 57 | 0 |  |
| 0.485 | 3 | 16 | – | 48 | 6 | – | 57 | 0 |  |
| 0.485 | 4 | 27 | – | 68 | 5 | – | 57 | 0 |  |
| 0.49 | 1 | 0 | 0.02987 | 4 | 18 | – | 55 | 0 | yes |
| 0.49 | 2 | 3 | – | 25 | 8 | – | 55 | 0 |  |
| 0.49 | 3 | 13 | – | 43 | 6 | – | 55 | 0 |  |
| 0.49 | 4 | 24 | – | 63 | 5 | – | 55 | 0 |  |
| 0.495 | 1 | 0 | 0.02372 | 1 | 38 | – | 53 | 0 | yes |
| 0.495 | 2 | 0 | 1.352 | 22 | 8 | – | 53 | 0 | yes |
| 0.495 | 3 | 10 | – | 41 | 6 | – | 53 | 0 |  |
| 0.495 | 4 | 20 | – | 59 | 5 | – | 53 | 0 |  |
| 0.5 | 1 | 0 | 0.01911 | 0 | – | 0.3084 | 50 | 0 |  |
| 0.5 | 2 | 0 | 0.141 | 18 | 9 | – | 50 | 0 | yes |
| 0.5 | 3 | 6 | – | 36 | 7 | – | 50 | 0 |  |
| 0.5 | 4 | 16 | – | 55 | 6 | – | 50 | 0 |  |
| 0.505 | 1 | 0 | 0.0152 | 0 | – | 0.05753 | 47 | 0 |  |
| 0.505 | 2 | 0 | 0.04886 | 13 | 11 | – | 47 | 0 | yes |
| 0.505 | 3 | 2 | – | 31 | 7 | – | 47 | 0 |  |
| 0.505 | 4 | 11 | – | 49 | 6 | – | 47 | 0 |  |
| 0.51 | 1 | 0 | 0.01249 | 0 | – | 0.03632 | 44 | 0 |  |
| 0.51 | 2 | 0 | 0.0339 | 8 | 13 | – | 44 | 0 | yes |
| 0.51 | 3 | 0 | 0.3399 | 26 | 8 | – | 44 | 0 | yes |
| 0.51 | 4 | 6 | – | 44 | 7 | – | 44 | 0 |  |
| 0.515 | 1 | 0 | 0.01006 | 0 | – | 0.02705 | 41 | 0 |  |
| 0.515 | 2 | 0 | 0.0251 | 0 | – | 1.619 | 41 | 0 |  |
| 0.515 | 3 | 0 | 0.06359 | 17 | 10 | – | 41 | 0 | yes |
| 0.515 | 4 | 0 | 1.311 | 36 | 8 | – | 41 | 0 | yes |
| 0.52 | 1 | 0 | 0.00815 | 0 | – | 0.02061 | 37 | 0 |  |
| 0.52 | 2 | 0 | 0.01925 | 0 | – | 0.1432 | 37 | 0 |  |
| 0.52 | 3 | 0 | 0.03697 | 11 | 13 | – | 37 | 0 | yes |
| 0.52 | 4 | 0 | 0.1118 | 27 | 9 | – | 37 | 0 | yes |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.1156 | 10 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 9 | – | 32 | 7 | – | 60 | 0 |  |
| 0.48 | 3 | 20 | – | 53 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 5 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.04673 | 8 | 13 | – | 58 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 58 | 0 |  |
| 0.485 | 3 | 18 | – | 48 | 5 | – | 58 | 0 |  |
| 0.485 | 4 | 28 | – | 69 | 5 | – | 58 | 0 |  |
| 0.49 | 1 | 0 | 0.03336 | 5 | 16 | – | 56 | 0 | yes |
| 0.49 | 2 | 4 | – | 26 | 7 | – | 56 | 0 |  |
| 0.49 | 3 | 15 | – | 45 | 6 | – | 56 | 0 |  |
| 0.49 | 4 | 25 | – | 66 | 5 | – | 56 | 0 |  |
| 0.495 | 1 | 0 | 0.02573 | 2 | 26 | – | 54 | 0 | yes |
| 0.495 | 2 | 1 | – | 22 | 8 | – | 54 | 0 |  |
| 0.495 | 3 | 11 | – | 43 | 6 | – | 54 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 54 | 0 |  |
| 0.5 | 1 | 0 | 0.02067 | 0 | – | 0.7334 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.326 | 19 | 9 | – | 52 | 0 | yes |
| 0.5 | 3 | 8 | – | 38 | 7 | – | 52 | 0 |  |
| 0.5 | 4 | 17 | – | 55 | 6 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01652 | 0 | – | 0.07076 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06027 | 14 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 3 | – | 33 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 51 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01364 | 0 | – | 0.03907 | 46 | 0 |  |
| 0.51 | 2 | 0 | 0.0382 | 9 | 13 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 0.8594 | 27 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 8 | – | 45 | 7 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01078 | 0 | – | 0.0299 | 42 | 0 |  |
| 0.515 | 2 | 0 | 0.02727 | 3 | 20 | – | 42 | 0 | yes |
| 0.515 | 3 | 0 | 0.07901 | 20 | 9 | – | 42 | 0 | yes |
| 0.515 | 4 | 0 | 1.632 | 37 | 7 | – | 42 | 0 | yes |
| 0.52 | 1 | 0 | 0.008744 | 0 | – | 0.02211 | 38 | 0 |  |
| 0.52 | 2 | 0 | 0.02072 | 0 | – | 0.3449 | 38 | 0 |  |
| 0.52 | 3 | 0 | 0.04239 | 12 | 12 | – | 38 | 0 | yes |
| 0.52 | 4 | 0 | 0.1409 | 29 | 8 | – | 38 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 1 | 0 | 0.2833 | 11 | 11 | – | 60 | 0 | yes |
| 0.48 | 2 | 10 | – | 33 | 6 | – | 60 | 0 |  |
| 0.48 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.48 | 4 | 31 | – | 73 | 4 | – | 60 | 0 |  |
| 0.485 | 1 | 0 | 0.05238 | 8 | 12 | – | 59 | 0 | yes |
| 0.485 | 2 | 7 | – | 29 | 7 | – | 59 | 0 |  |
| 0.485 | 3 | 18 | – | 49 | 5 | – | 59 | 0 |  |
| 0.485 | 4 | 29 | – | 69 | 5 | – | 59 | 0 |  |
| 0.49 | 1 | 0 | 0.03625 | 6 | 15 | – | 57 | 0 | yes |
| 0.49 | 2 | 5 | – | 27 | 7 | – | 57 | 0 |  |
| 0.49 | 3 | 15 | – | 48 | 6 | – | 57 | 0 |  |
| 0.49 | 4 | 26 | – | 66 | 5 | – | 57 | 0 |  |
| 0.495 | 1 | 0 | 0.02718 | 3 | 23 | – | 55 | 0 | yes |
| 0.495 | 2 | 2 | – | 24 | 8 | – | 55 | 0 |  |
| 0.495 | 3 | 12 | – | 43 | 6 | – | 55 | 0 |  |
| 0.495 | 4 | 22 | – | 62 | 5 | – | 55 | 0 |  |
| 0.5 | 1 | 0 | 0.02191 | 0 | – | 0.9417 | 52 | 0 |  |
| 0.5 | 2 | 0 | 0.591 | 20 | 8 | – | 52 | 0 | yes |
| 0.5 | 3 | 9 | – | 39 | 6 | – | 52 | 0 |  |
| 0.5 | 4 | 18 | – | 57 | 5 | – | 52 | 0 |  |
| 0.505 | 1 | 0 | 0.01743 | 0 | – | 0.08476 | 49 | 0 |  |
| 0.505 | 2 | 0 | 0.06977 | 15 | 10 | – | 49 | 0 | yes |
| 0.505 | 3 | 4 | – | 34 | 7 | – | 49 | 0 |  |
| 0.505 | 4 | 13 | – | 52 | 6 | – | 49 | 0 |  |
| 0.51 | 1 | 0 | 0.01403 | 0 | – | 0.04462 | 47 | 0 |  |
| 0.51 | 2 | 0 | 0.04105 | 10 | 12 | – | 47 | 0 | yes |
| 0.51 | 3 | 0 | 1.055 | 28 | 8 | – | 47 | 0 | yes |
| 0.51 | 4 | 9 | – | 45 | 6 | – | 47 | 0 |  |
| 0.515 | 1 | 0 | 0.01135 | 0 | – | 0.03193 | 43 | 0 |  |
| 0.515 | 2 | 0 | 0.02885 | 4 | 18 | – | 43 | 0 | yes |
| 0.515 | 3 | 0 | 0.08916 | 22 | 9 | – | 43 | 0 | yes |
| 0.515 | 4 | 2 | – | 39 | 7 | – | 43 | 0 |  |
| 0.52 | 1 | 0 | 0.009163 | 0 | – | 0.02325 | 39 | 0 |  |
| 0.52 | 2 | 0 | 0.02165 | 0 | – | 0.4826 | 39 | 0 |  |
| 0.52 | 3 | 0 | 0.04597 | 14 | 11 | – | 39 | 0 | yes |
| 0.52 | 4 | 0 | 0.2004 | 30 | 8 | – | 39 | 0 | yes |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7656', 'vtau': '0.5168', 'vtau_i': '0.5168'}, DPI scales 8,8,8,8 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 21 | 7 | – | 67 | 0 |  |
| 0.435 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.435 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.435 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.44 | 1 | 7 | – | 20 | 7 | – | 66 | 0 |  |
| 0.44 | 2 | 19 | – | 43 | 5 | – | 66 | 0 |  |
| 0.44 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.44 | 4 | 42 | – | 85 | 4 | – | 66 | 0 |  |
| 0.445 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.445 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.445 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.445 | 4 | 41 | – | 84 | 4 | – | 66 | 0 |  |
| 0.45 | 1 | 5 | – | 18 | 8 | – | 65 | 0 |  |
| 0.45 | 2 | 17 | – | 41 | 5 | – | 65 | 0 |  |
| 0.45 | 3 | 28 | – | 61 | 5 | – | 65 | 0 |  |
| 0.45 | 4 | 40 | – | 83 | 4 | – | 65 | 0 |  |
| 0.455 | 1 | 4 | – | 17 | 8 | – | 64 | 0 |  |
| 0.455 | 2 | 16 | – | 40 | 6 | – | 64 | 0 |  |
| 0.455 | 3 | 27 | – | 62 | 5 | – | 64 | 0 |  |
| 0.455 | 4 | 38 | – | 82 | 4 | – | 64 | 0 |  |
| 0.46 | 1 | 3 | – | 16 | 9 | – | 63 | 0 |  |
| 0.46 | 2 | 15 | – | 38 | 6 | – | 63 | 0 |  |
| 0.46 | 3 | 26 | – | 58 | 5 | – | 63 | 0 |  |
| 0.46 | 4 | 37 | – | 79 | 4 | – | 63 | 0 |  |
| 0.465 | 1 | 2 | – | 14 | 9 | – | 62 | 0 |  |
| 0.465 | 2 | 14 | – | 36 | 6 | – | 62 | 0 |  |
| 0.465 | 3 | 24 | – | 58 | 5 | – | 62 | 0 |  |
| 0.465 | 4 | 35 | – | 77 | 4 | – | 62 | 0 |  |
| 0.47 | 1 | 1 | – | 13 | 10 | – | 61 | 0 |  |
| 0.47 | 2 | 12 | – | 35 | 6 | – | 61 | 0 |  |
| 0.47 | 3 | 23 | – | 56 | 5 | – | 61 | 0 |  |
| 0.47 | 4 | 34 | – | 75 | 5 | – | 61 | 0 |  |
| 0.475 | 1 | 0 | 0.6299 | 11 | 11 | – | 60 | 0 | yes |
| 0.475 | 2 | 10 | – | 33 | 7 | – | 60 | 0 |  |
| 0.475 | 3 | 21 | – | 54 | 5 | – | 60 | 0 |  |
| 0.475 | 4 | 32 | – | 74 | 5 | – | 60 | 0 |  |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7666', 'vtau': '0.5147', 'vtau_i': '0.5147'}, DPI scales 6,6,6,6 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.435 | 3 | 32 | – | 67 | 4 | – | 68 | 0 |  |
| 0.435 | 4 | 44 | – | 88 | 4 | – | 68 | 0 |  |
| 0.44 | 1 | 8 | – | 21 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 20 | – | 44 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 31 | – | 65 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 43 | – | 84 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 20 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 19 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 42 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.45 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.45 | 3 | 30 | – | 63 | 4 | – | 66 | 0 |  |
| 0.45 | 4 | 41 | – | 85 | 4 | – | 66 | 0 |  |
| 0.455 | 1 | 5 | – | 18 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 17 | – | 41 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 62 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 40 | – | 83 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 16 | – | 40 | 6 | – | 65 | 0 |  |
| 0.46 | 3 | 27 | – | 59 | 5 | – | 65 | 0 |  |
| 0.46 | 4 | 38 | – | 80 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 15 | 9 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 38 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 26 | – | 59 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 37 | – | 78 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 1 | – | 14 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 13 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 24 | – | 58 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 35 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.065 | 12 | 10 | – | 61 | 0 | yes |
| 0.475 | 2 | 11 | – | 34 | 6 | – | 61 | 0 |  |
| 0.475 | 3 | 22 | – | 55 | 5 | – | 61 | 0 |  |
| 0.475 | 4 | 33 | – | 74 | 4 | – | 61 | 0 |  |


# XOR on snn_analog: simulation results

Written by `run_xor.py`; each section notes the date and any parameter overrides it ran with.

<!-- vlk: run_xor.py on 2026-11-11, overrides {'vthr': '2.7703', 'vtau': '0.5096', 'vtau_i': '0.5096'}, DPI scales 4,4,4,4 -->
## Leak bias vs one and two inputs (`hidden_tb`, tt, 27 °C)

10 ms (50 pulses). `AND` = no spike with one input, at least one with two. `VMEM max` is given only when the neuron did not fire (firing threshold about 1.65 V).

| Vlk (V) | weight | A: spikes | A: VMEM max (V) | A+B: spikes | A+B: first at pulse | A+B: VMEM max (V) | relay spikes | false spikes | AND |
|---|---|---|---|---|---|---|---|---|---|
| 0.435 | 1 | 9 | – | 22 | 7 | – | 69 | 0 |  |
| 0.435 | 2 | 21 | – | 45 | 5 | – | 69 | 0 |  |
| 0.435 | 3 | 33 | – | 67 | 4 | – | 69 | 0 |  |
| 0.435 | 4 | 44 | – | 87 | 4 | – | 69 | 0 |  |
| 0.44 | 1 | 8 | – | 22 | 7 | – | 68 | 0 |  |
| 0.44 | 2 | 21 | – | 45 | 5 | – | 68 | 0 |  |
| 0.44 | 3 | 32 | – | 66 | 4 | – | 68 | 0 |  |
| 0.44 | 4 | 44 | – | 87 | 4 | – | 68 | 0 |  |
| 0.445 | 1 | 7 | – | 21 | 7 | – | 67 | 0 |  |
| 0.445 | 2 | 20 | – | 44 | 5 | – | 67 | 0 |  |
| 0.445 | 3 | 32 | – | 66 | 4 | – | 67 | 0 |  |
| 0.445 | 4 | 43 | – | 86 | 4 | – | 67 | 0 |  |
| 0.45 | 1 | 6 | – | 20 | 7 | – | 67 | 0 |  |
| 0.45 | 2 | 19 | – | 43 | 5 | – | 67 | 0 |  |
| 0.45 | 3 | 31 | – | 64 | 4 | – | 67 | 0 |  |
| 0.45 | 4 | 42 | – | 85 | 4 | – | 67 | 0 |  |
| 0.455 | 1 | 6 | – | 19 | 8 | – | 66 | 0 |  |
| 0.455 | 2 | 18 | – | 42 | 5 | – | 66 | 0 |  |
| 0.455 | 3 | 29 | – | 63 | 4 | – | 66 | 0 |  |
| 0.455 | 4 | 41 | – | 82 | 4 | – | 66 | 0 |  |
| 0.46 | 1 | 4 | – | 17 | 8 | – | 65 | 0 |  |
| 0.46 | 2 | 17 | – | 40 | 5 | – | 65 | 0 |  |
| 0.46 | 3 | 28 | – | 62 | 4 | – | 65 | 0 |  |
| 0.46 | 4 | 39 | – | 82 | 4 | – | 65 | 0 |  |
| 0.465 | 1 | 3 | – | 16 | 8 | – | 64 | 0 |  |
| 0.465 | 2 | 15 | – | 39 | 6 | – | 64 | 0 |  |
| 0.465 | 3 | 27 | – | 60 | 5 | – | 64 | 0 |  |
| 0.465 | 4 | 38 | – | 80 | 4 | – | 64 | 0 |  |
| 0.47 | 1 | 2 | – | 15 | 9 | – | 63 | 0 |  |
| 0.47 | 2 | 14 | – | 37 | 6 | – | 63 | 0 |  |
| 0.47 | 3 | 25 | – | 59 | 5 | – | 63 | 0 |  |
| 0.47 | 4 | 36 | – | 78 | 4 | – | 63 | 0 |  |
| 0.475 | 1 | 0 | 1.319 | 13 | 10 | – | 62 | 0 | yes |
| 0.475 | 2 | 12 | – | 35 | 6 | – | 62 | 0 |  |
| 0.475 | 3 | 23 | – | 56 | 5 | – | 62 | 0 |  |
| 0.475 | 4 | 34 | – | 75 | 4 | – | 62 | 0 |  |


# XOR on snn_analog: simulation results

Generated by `run_xor.py` on 2026-11-11. Suites: and_mc. Parameter overrides: {'p_vlk': '0.455'}.

## AND and OR neurons with mismatch (`hidden_tb`)

Each sample is one mismatch draw (one seed), simulated with A alone, B alone and A+B, so all three see the same devices. 10 ms (50 pulses).

**AND (code 1, weight 1):** 9 / 100 samples pass (no spike with one input, spike with two).
- One input fired it: 52 samples [0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 16, 18, 19, 21, 22, 24, 26, 27, 28]
- Two inputs did not fire it: 39 samples [1, 5, 9, 15, 17, 20, 23, 32, 33, 34, 35, 39, 40, 41, 43, 44, 47, 49, 51, 52]
- Highest VMEM with one input (passing samples, V): mean 0.4107, std 0.504, min 0.002491, max 1.454 (n = 48)
- Firing VMEM with two inputs (V): mean 1.663, std 0.0379, min 1.582, max 1.762 (n = 61)
- First spike with two inputs, pulse number: mean 10.21, std 6.62, min 2, max 31 (n = 61)
- Spikes in 50 pulses with two inputs: mean 18.32, std 33.2, min 0, max 209 (n = 100)
- Relay spikes in 50 pulses (nominal 49): mean 69.92, std 71.2, min 0, max 385 (n = 200)
- False spikes (should be 0): 0



<!-- xor_mc: run_xor.py on 2026-11-11 -->
## XOR with mismatch (`xor_tb`)

27 / 30 samples give the right output in all 4 cases.

- A=0 B=0: output spikes mean 0, std 0, min 0, max 0 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=0 B=1: output spikes mean 6.167, std 2.63, min 1, max 13 (n = 30); AND spikes mean 0, std 0, min 0, max 0 (n = 30); wrong in samples []
- A=1 B=0: output spikes mean 6.433, std 2.69, min 1, max 13 (n = 30); AND spikes mean 0.1333, std 0.73, min 0, max 4 (n = 30); wrong in samples []
- A=1 B=1: output spikes mean 0.1, std 0.305, min 0, max 1 (n = 30); AND spikes mean 35, std 9.15, min 14, max 55 (n = 30); wrong in samples [8, 20, 22]

