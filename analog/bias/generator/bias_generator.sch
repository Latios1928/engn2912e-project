v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_generator: on-chip bias generator for the 2-2-1 SNN } -600 -560 0 0 0.5 0.5 {}
T {bias_master (reference) -> trim_steer (Apple US 10,938,380 Fig. 2 trim) -> bias_cell (11 biases). Imon = copy of Ibias for trimming: hold the pad at 1.65 V; trim target 102.7 nA.} -600 -520 0 0 0.3 0.3 {}
N -100 -110 40 -110 {}
N 40 -110 40 -30 {}
N 40 -30 90 -30 {}
N -320 -110 -300 -110 {}
N -320 -90 -300 -90 {}
N 70 -70 90 -70 {}
N 70 -50 90 -50 {}
N 70 -10 90 -10 {}
N 70 10 90 10 {}
N 70 30 90 30 {}
N 70 50 90 50 {}
N 70 70 90 70 {}
N 590 -100 610 -100 {}
N 590 -80 610 -80 {}
N 310 -70 480 -70 {}
N 480 -70 480 -60 {}
N 480 -60 610 -60 {}
N 910 -100 1020 -100 {}
N 910 -80 1020 -80 {}
N 910 -60 1020 -60 {}
N 910 -40 1020 -40 {}
N 910 -20 1020 -20 {}
N 910 0 1020 0 {}
N 910 20 1020 20 {}
N 910 40 1020 40 {}
N 910 60 1020 60 {}
N 910 80 1020 80 {}
N 910 100 1020 100 {}
C {iopin.sym} -560 -460 0 0 {name=p1 lab=VDD}
C {iopin.sym} -560 -420 0 0 {name=p2 lab=VSS}
C {ipin.sym} -560 -380 0 0 {name=p3 lab=trim[3]}
C {ipin.sym} -560 -340 0 0 {name=p4 lab=trim[2]}
C {ipin.sym} -560 -300 0 0 {name=p5 lab=trim[1]}
C {ipin.sym} -560 -260 0 0 {name=p6 lab=trim[0]}
C {ipin.sym} -560 -220 0 0 {name=p7 lab=cal}
C {iopin.sym} -560 -180 0 0 {name=p8 lab=Imon}
C {analog/bias/generator/bias_master.sym} -200 -100 0 0 {name=xmaster}
C {analog/bias/generator/trim_steer.sym} 200 0 0 0 {name=xtrim}
C {bias.sym} 760 0 0 0 {name=xcell}
C {lab_pin.sym} 40 -110 0 1 {name=l9 sig_type=std_logic lab=Iref}
C {lab_pin.sym} -320 -110 0 0 {name=l10 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -320 -90 0 0 {name=l11 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 70 -70 0 0 {name=l12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 70 -50 0 0 {name=l13 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 70 -10 0 0 {name=l14 sig_type=std_logic lab=trim[3]}
C {lab_pin.sym} 70 10 0 0 {name=l15 sig_type=std_logic lab=trim[2]}
C {lab_pin.sym} 70 30 0 0 {name=l16 sig_type=std_logic lab=trim[1]}
C {lab_pin.sym} 70 50 0 0 {name=l17 sig_type=std_logic lab=trim[0]}
C {lab_pin.sym} 70 70 0 0 {name=l18 sig_type=std_logic lab=cal}
C {lab_pin.sym} 590 -100 0 0 {name=l19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 590 -80 0 0 {name=l20 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 480 -70 0 1 {name=l21 sig_type=std_logic lab=Ibias}
C {opin.sym} 1020 -100 2 0 {name=p25 lab=Vb}
C {opin.sym} 1020 -80 2 0 {name=p26 lab=Vlk}
C {opin.sym} 1020 -60 2 0 {name=p27 lab=VKdn}
C {opin.sym} 1020 -40 2 0 {name=p28 lab=VIp}
C {opin.sym} 1020 -20 2 0 {name=p29 lab=Vamp_bias}
C {opin.sym} 1020 0 2 0 {name=p30 lab=VK}
C {opin.sym} 1020 20 2 0 {name=p31 lab=VNA}
C {opin.sym} 1020 40 2 0 {name=p32 lab=VKup}
C {opin.sym} 1020 60 2 0 {name=p33 lab=Vthr}
C {opin.sym} 1020 80 2 0 {name=p34 lab=VT_dpi}
C {opin.sym} 1020 100 2 0 {name=p35 lab=VT_inh}
N 590 -40 610 -40 {}
C {lab_pin.sym} 590 -40 0 0 {name=l50 sig_type=std_logic lab=Imon}
T {Imon: MMON, a copy of MN0, is inside the bias cell (2026-11-27)} 560 320 0 0 0.25 0.25 {}
