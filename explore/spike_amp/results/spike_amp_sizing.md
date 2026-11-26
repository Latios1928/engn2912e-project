# Spike amplifier sizing

Sweep by `run_sweep.py` (`amp_char.py`): 5T OTA of `analog/neuron/spike_amplifier.sch` used as the neuron's comparator (VP = VMEM, VN = VT = 1.66 V), tail M3 kept at 0.22/0.28 um with Vamp_bias = 0.535 V (the bias cell's replica stays valid), load = the neuron's inverter 1 (M1/M3 + M8 at VIp) + 2 fF; tt 27 C. 320 points: pair W 0.5-8 um x L 0.5-4 um, mirror W 0.5-4 um x L 1-8 um.

Metric definitions: systematic offset = VP at which the output crosses VDD/2 minus VN (DC sweep); offset sigma = 40 mismatch samples of that trip point (`sw_stat_mismatch`); A0 / fu = open-loop gain and unity-gain frequency at the trip point; PM = 180 deg + phase at fu, i.e. the phase margin the amplifier would have in unity-gain feedback (it is used open-loop); trip delay = output crossing VDD/2 after VP passes the trip point on the real VMEM ramp (9.5 mV/us); noise = input-referred.

## Minimum size (current) and the chosen size

| pair W/L (um) | mirror W/L (um) | systematic offset (mV) | offset sigma (mV) | A0 (dB) | fu (MHz) | PM (deg) | trip delay (us) | noise 1 Hz-100 kHz (uVrms) | noise @1 kHz (uV/rtHz) | area (um2) | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.22/0.28 | 0.22/0.28 | -55.9 | 40.54 | 24.6 | 97.1 | 81 | 0.03 | 336 | 3.11 | 0.3 | current spike_amplifier.sch |
| 4/2 | 0.5/8 | -1.2 | 2.56 | 53.8 | 19.2 | 64 | 0.66 | 60 | 0.29 | 24.1 | **spike_amplifier_sized.sch** |

## Pareto front: mismatch offset vs area

| pair W/L (um) | mirror W/L (um) | systematic offset (mV) | offset sigma (mV) | A0 (dB) | fu (MHz) | PM (deg) | trip delay (us) | noise 1 Hz-100 kHz (uVrms) | noise @1 kHz (uV/rtHz) | area (um2) | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5/0.5 | 0.5/1 | -6.2 | 15.41 | 42.1 | 53.9 | 64 | 0.25 | 159 | 1.41 | 1.6 |  |
| 0.5/1 | 0.5/1 | -3.3 | 11.14 | 48.0 | 49.2 | 63 | 0.41 | 128 | 1.06 | 2.1 |  |
| 0.5/1 | 0.5/2 | -2.6 | 9.81 | 49.2 | 39.1 | 62 | 0.43 | 122 | 1.01 | 3.1 |  |
| 1/1 | 0.5/1 | -3.2 | 9.03 | 48.0 | 48.6 | 61 | 0.42 | 101 | 0.76 | 3.1 |  |
| 0.5/2 | 0.5/2 | -1.8 | 7.41 | 52.6 | 34.7 | 58 | 0.56 | 107 | 0.78 | 4.1 |  |
| 0.5/2 | 0.5/4 | -1.4 | 6.60 | 53.6 | 27.0 | 64 | 0.57 | 102 | 0.75 | 6.1 |  |
| 1/2 | 0.5/2 | -1.8 | 5.89 | 52.5 | 35.6 | 56 | 0.54 | 87 | 0.57 | 6.1 |  |
| 2/1 | 0.5/2 | -2.5 | 5.78 | 49.4 | 36.2 | 59 | 0.47 | 77 | 0.52 | 6.1 |  |
| 0.5/4 | 0.5/4 | -1.1 | 5.03 | 56.6 | 23.2 | 55 | 0.69 | 97 | 0.59 | 8.1 |  |
| 2/2 | 0.5/2 | -1.8 | 4.80 | 52.5 | 33.8 | 52 | 0.56 | 75 | 0.43 | 10.1 |  |
| 4/1 | 0.5/2 | -2.4 | 4.61 | 49.7 | 30.4 | 56 | 0.54 | 66 | 0.39 | 10.1 |  |
| 0.5/4 | 0.5/8 | -0.8 | 4.54 | 57.4 | 19.1 | 66 | 0.71 | 92 | 0.57 | 12.1 |  |
| 1/4 | 0.5/4 | -1.1 | 3.91 | 56.5 | 25.0 | 51 | 0.66 | 81 | 0.43 | 12.1 |  |
| 2/2 | 0.5/4 | -1.5 | 3.79 | 53.4 | 26.7 | 58 | 0.58 | 70 | 0.40 | 12.1 |  |
| 1/4 | 0.5/8 | -0.9 | 3.41 | 57.2 | 20.8 | 63 | 0.68 | 77 | 0.41 | 16.1 |  |
| 2/4 | 0.5/4 | -1.1 | 3.09 | 56.4 | 25.0 | 44 | 0.67 | 72 | 0.34 | 20.1 |  |
| 4/2 | 0.5/4 | -1.5 | 2.94 | 53.4 | 22.9 | 54 | 0.64 | 63 | 0.31 | 20.1 |  |
| 2/4 | 0.5/8 | -0.9 | 2.54 | 57.0 | 20.7 | 56 | 0.69 | 68 | 0.32 | 24.1 |  |
| 8/2 | 0.5/4 | -1.5 | 2.39 | 53.5 | 17.5 | 50 | 0.77 | 58 | 0.25 | 36.1 |  |
| 4/4 | 0.5/8 | -0.9 | 1.93 | 56.8 | 18.2 | 49 | 0.75 | 63 | 0.26 | 40.1 |  |
| 4/4 | 2/8 | -1.1 | 1.87 | 56.6 | 15.2 | 57 | 0.83 | 68 | 0.27 | 64.1 |  |
| 8/4 | 0.5/8 | -0.9 | 1.51 | 56.7 | 14.0 | 42 | 0.88 | 60 | 0.22 | 72.1 |  |
| 8/4 | 2/8 | -1.1 | 1.44 | 56.5 | 11.9 | 51 | 0.95 | 64 | 0.23 | 96.1 |  |
| 8/4 | 4/8 | -1.2 | 1.37 | 56.4 | 10.5 | 57 | 1.03 | 68 | 0.24 | 128.1 |  |

## In the neuron (neuron_sized, biases from the bias cell, 9.5 nA DC)

| | minimum-size amplifier | sized amplifier |
|---|---|---|
| tt 27 C: period / t_spike / t_refr (us) | 201.5 / 9.32 / 14.71 | 204.2 / 9.62 / 14.99 |
| PVT points passing all specs (15) | 4 | 5 |
| mismatch, 40 samples of the whole neuron + bias cell: period sigma | 5.79 us (2.88 %) | 3.45 us (1.68 %) |
| mismatch: t_spike sigma | 1.50 us | 1.58 us |

The sized amplifier adds gate capacitance on VMEM and trips about 0.6 us later, so the period grows by 1.3 % and t_refr by 0.3 us (now at its 15 us limit). Not yet applied to `neuron_sized.sch` or its layout.
