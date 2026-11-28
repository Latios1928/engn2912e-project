v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {trim_steer: steered-mirror bias current trim, after Apple patent US 10,938,380 B1 Fig.2} -380 -480 0 0 0.5 0.5 {}
T {Ibias = (14 + code) x Iref / 23: 61 / 100 / 126 % at code 0 / 9 / 15. Every source stays on: trim[k] steers it to the bias node (S_k) or the aux node (S_kX).} -380 -440 0 0 0.3 0.3 {}
T {cal = 1 (trimming): M_Aux is a diode, the aux node sits at the bias node's voltage, so a code change does not disturb Vgs. cal = 0: vaux discharges slowly through MDIS, I_aux -> 0.} -380 -410 0 0 0.3 0.3 {}
T {M0 + R0 (noise filter)} -60 -270 0 0 0.35 0.35 {}
T {R0: 75 sq} 60 -110 0 0 0.25 0.25 {}
T {gate cap} 230 -120 0 0 0.25 0.25 {}
T {Current sources (all on) and steering switches S_k / S_kX} 360 -270 0 0 0.35 0.35 {}
T {14 units} 480 -245 0 0 0.25 0.25 {}
T {1 unit} 880 -245 0 0 0.25 0.25 {}
T {2 units} 1280 -245 0 0 0.25 0.25 {}
T {4 units} 1680 -245 0 0 0.25 0.25 {}
T {8 units} 2080 -245 0 0 0.25 0.25 {}
T {bias node -> bias_cell} 2160 -25 0 0 0.25 0.25 {}
T {aux node} 2160 70 0 0 0.25 0.25 {}
T {trim[k] -> tb_k (gates of S_kX)} 360 220 0 0 0.3 0.3 {}
T {M_Aux + analog control} 2420 -40 0 0 0.35 0.35 {}
T {MDIS: 0.5/45.45 pull-down (W/L of the earlier 0.22/20)} 2760 350 0 0 0.25 0.25 {}
T {MCAUX: gate cap} 2660 470 0 0 0.25 0.25 {}
N -120 -300 20 -300 {}
N 20 -300 260 -300 {}
N 260 -300 460 -300 {}
N 460 -300 860 -300 {}
N 860 -300 1260 -300 {}
N 1260 -300 1660 -300 {}
N 1660 -300 2060 -300 {}
N 2060 -300 2480 -300 {}
N -120 640 2400 640 {}
N 2400 640 2480 640 {}
N 2480 640 2700 640 {}
N 2700 640 2800 640 {}
N -140 -300 -120 -300 {}
N -140 640 -120 640 {}
N 20 -200 40 -200 {}
N 20 -300 20 -230 {}
N 20 -170 20 -140 {}
N 20 -140 20 -100 {}
N -40 -140 20 -140 {}
N -40 -200 -40 -140 {}
N -40 -200 -20 -200 {}
N 20 -140 120 -140 {}
N 80 -170 100 -170 {}
N 120 -250 120 -200 {}
N 120 -250 180 -250 {}
N 260 -200 280 -200 {}
N 260 -300 260 -230 {}
N 260 -170 260 -140 {}
N 200 -200 220 -200 {}
N 460 -200 480 -200 {}
N 460 -300 460 -230 {}
N 400 -200 420 -200 {}
N 460 -170 460 -120 {}
N 460 -90 480 -90 {}
N 400 -90 420 -90 {}
N 460 -60 460 0 {}
N 860 -200 880 -200 {}
N 860 -300 860 -230 {}
N 800 -200 820 -200 {}
N 860 -170 860 -120 {}
N 860 -90 880 -90 {}
N 800 -90 820 -90 {}
N 860 -60 860 0 {}
N 860 -120 1060 -120 {}
N 1060 -90 1080 -90 {}
N 1000 -90 1020 -90 {}
N 1060 -60 1060 60 {}
N 1260 -200 1280 -200 {}
N 1260 -300 1260 -230 {}
N 1200 -200 1220 -200 {}
N 1260 -170 1260 -120 {}
N 1260 -90 1280 -90 {}
N 1200 -90 1220 -90 {}
N 1260 -60 1260 0 {}
N 1260 -120 1460 -120 {}
N 1460 -90 1480 -90 {}
N 1400 -90 1420 -90 {}
N 1460 -60 1460 60 {}
N 1660 -200 1680 -200 {}
N 1660 -300 1660 -230 {}
N 1600 -200 1620 -200 {}
N 1660 -170 1660 -120 {}
N 1660 -90 1680 -90 {}
N 1600 -90 1620 -90 {}
N 1660 -60 1660 0 {}
N 1660 -120 1860 -120 {}
N 1860 -90 1880 -90 {}
N 1800 -90 1820 -90 {}
N 1860 -60 1860 60 {}
N 2060 -200 2080 -200 {}
N 2060 -300 2060 -230 {}
N 2000 -200 2020 -200 {}
N 2060 -170 2060 -120 {}
N 2060 -90 2080 -90 {}
N 2000 -90 2020 -90 {}
N 2060 -60 2060 0 {}
N 2060 -120 2260 -120 {}
N 2260 -90 2280 -90 {}
N 2200 -90 2220 -90 {}
N 2260 -60 2260 60 {}
N 460 0 860 0 {}
N 860 0 1260 0 {}
N 1260 0 1660 0 {}
N 1660 0 2060 0 {}
N 2060 0 2360 0 {}
N 1060 60 1460 60 {}
N 1460 60 1860 60 {}
N 1860 60 2260 60 {}
N 2260 60 2480 60 {}
N 860 300 880 300 {}
N 860 420 880 420 {}
N 860 250 860 270 {}
N 860 330 860 360 {}
N 860 360 860 390 {}
N 800 300 820 300 {}
N 800 300 800 360 {}
N 800 360 800 420 {}
N 800 420 820 420 {}
N 780 360 800 360 {}
N 860 450 860 480 {}
N 1260 300 1280 300 {}
N 1260 420 1280 420 {}
N 1260 250 1260 270 {}
N 1260 330 1260 360 {}
N 1260 360 1260 390 {}
N 1200 300 1220 300 {}
N 1200 300 1200 360 {}
N 1200 360 1200 420 {}
N 1200 420 1220 420 {}
N 1180 360 1200 360 {}
N 1260 450 1260 480 {}
N 1660 300 1680 300 {}
N 1660 420 1680 420 {}
N 1660 250 1660 270 {}
N 1660 330 1660 360 {}
N 1660 360 1660 390 {}
N 1600 300 1620 300 {}
N 1600 300 1600 360 {}
N 1600 360 1600 420 {}
N 1600 420 1620 420 {}
N 1580 360 1600 360 {}
N 1660 450 1660 480 {}
N 2060 300 2080 300 {}
N 2060 420 2080 420 {}
N 2060 250 2060 270 {}
N 2060 330 2060 360 {}
N 2060 360 2060 390 {}
N 2000 300 2020 300 {}
N 2000 300 2000 360 {}
N 2000 360 2000 420 {}
N 2000 420 2020 420 {}
N 1980 360 2000 360 {}
N 2060 450 2060 480 {}
N 2480 60 2480 90 {}
N 2480 90 2480 120 {}
N 2480 150 2500 150 {}
N 2480 180 2480 640 {}
N 2420 150 2440 150 {}
N 2480 90 2700 90 {}
N 2700 90 2700 120 {}
N 2700 150 2720 150 {}
N 2640 150 2660 150 {}
N 2700 180 2700 210 {}
N 2800 300 2820 300 {}
N 2800 250 2800 270 {}
N 2740 300 2760 300 {}
N 2800 330 2800 640 {}
N 2700 420 2720 420 {}
N 2640 420 2660 420 {}
N 2700 390 2700 450 {}
N 2700 450 2700 640 {}
N 2400 300 2420 300 {}
N 2400 420 2420 420 {}
N 2400 250 2400 270 {}
N 2400 330 2400 360 {}
N 2400 360 2400 390 {}
N 2340 300 2360 300 {}
N 2340 300 2340 360 {}
N 2340 360 2340 420 {}
N 2340 420 2360 420 {}
N 2320 360 2340 360 {}
N 2400 450 2400 640 {}
C {iopin.sym} -340 -260 0 0 {name=p1 lab=VDD}
C {iopin.sym} -340 -220 0 0 {name=p2 lab=VSS}
C {iopin.sym} -340 -180 0 0 {name=p3 lab=Iref}
C {ipin.sym} -340 -140 0 0 {name=p4 lab=trim[3]}
C {ipin.sym} -340 -100 0 0 {name=p5 lab=trim[2]}
C {ipin.sym} -340 -60 0 0 {name=p6 lab=trim[1]}
C {ipin.sym} -340 -20 0 0 {name=p7 lab=trim[0]}
C {ipin.sym} -340 20 0 0 {name=p8 lab=cal}
C {lab_pin.sym} -140 -300 0 0 {name=l9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -140 640 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 0 -200 0 0 {name=M0
L=6.0u
W=1.0u
nf=1
m=23
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 40 -200 0 1 {name=l11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 20 -100 0 0 {name=l12 sig_type=std_logic lab=Iref}
C {symbols/nwell.sym} 120 -170 0 0 {name=R0
W=2.0e-6
L=150.000e-6
model=nwell
spiceprefix=X
m=1
}
C {lab_pin.sym} 80 -170 0 0 {name=l13 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 180 -250 0 1 {name=l14 sig_type=std_logic lab=Vgs}
C {symbols/pfet_03v3.sym} 240 -200 0 0 {name=MCG
L=10.0u
W=10.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 280 -200 0 1 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 260 -140 0 0 {name=l16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 200 -200 0 0 {name=l17 sig_type=std_logic lab=Vgs}
C {symbols/pfet_03v3.sym} 440 -200 0 0 {name=MB
L=6.0u
W=1.0u
nf=1
m=14
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 480 -200 0 1 {name=l18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 400 -200 0 0 {name=l19 sig_type=std_logic lab=Vgs}
C {symbols/nfet_03v3.sym} 440 -90 0 0 {name=SB
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 480 -90 0 1 {name=l20 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 400 -90 0 0 {name=l21 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} 840 -200 0 0 {name=M1
L=6.0u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 880 -200 0 1 {name=l22 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 800 -200 0 0 {name=l23 sig_type=std_logic lab=Vgs}
C {symbols/nfet_03v3.sym} 840 -90 0 0 {name=S0
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 880 -90 0 1 {name=l24 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 800 -90 0 0 {name=l25 sig_type=std_logic lab=trim[0]}
C {symbols/nfet_03v3.sym} 1040 -90 0 0 {name=S0X
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1080 -90 0 1 {name=l26 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1000 -90 0 0 {name=l27 sig_type=std_logic lab=tb0}
C {symbols/pfet_03v3.sym} 1240 -200 0 0 {name=M2
L=6.0u
W=1.0u
nf=1
m=2
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1280 -200 0 1 {name=l28 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1200 -200 0 0 {name=l29 sig_type=std_logic lab=Vgs}
C {symbols/nfet_03v3.sym} 1240 -90 0 0 {name=S1
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1280 -90 0 1 {name=l30 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1200 -90 0 0 {name=l31 sig_type=std_logic lab=trim[1]}
C {symbols/nfet_03v3.sym} 1440 -90 0 0 {name=S1X
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1480 -90 0 1 {name=l32 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1400 -90 0 0 {name=l33 sig_type=std_logic lab=tb1}
C {symbols/pfet_03v3.sym} 1640 -200 0 0 {name=M3
L=6.0u
W=1.0u
nf=1
m=4
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1680 -200 0 1 {name=l34 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1600 -200 0 0 {name=l35 sig_type=std_logic lab=Vgs}
C {symbols/nfet_03v3.sym} 1640 -90 0 0 {name=S2
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1680 -90 0 1 {name=l36 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1600 -90 0 0 {name=l37 sig_type=std_logic lab=trim[2]}
C {symbols/nfet_03v3.sym} 1840 -90 0 0 {name=S2X
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1880 -90 0 1 {name=l38 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1800 -90 0 0 {name=l39 sig_type=std_logic lab=tb2}
C {symbols/pfet_03v3.sym} 2040 -200 0 0 {name=M4
L=6.0u
W=1.0u
nf=1
m=8
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2080 -200 0 1 {name=l40 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2000 -200 0 0 {name=l41 sig_type=std_logic lab=Vgs}
C {symbols/nfet_03v3.sym} 2040 -90 0 0 {name=S3
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2080 -90 0 1 {name=l42 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2000 -90 0 0 {name=l43 sig_type=std_logic lab=trim[3]}
C {symbols/nfet_03v3.sym} 2240 -90 0 0 {name=S3X
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2280 -90 0 1 {name=l44 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2200 -90 0 0 {name=l45 sig_type=std_logic lab=tb3}
C {opin.sym} 2360 0 2 0 {name=p46 lab=Ibias}
C {symbols/pfet_03v3.sym} 840 300 0 0 {name=MIP0
L=0.28u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 880 300 0 1 {name=l47 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 840 420 0 0 {name=MIN0
L=0.28u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 880 420 0 1 {name=l48 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 860 250 0 1 {name=l49 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 860 360 0 1 {name=l50 sig_type=std_logic lab=tb0}
C {lab_pin.sym} 780 360 0 0 {name=l51 sig_type=std_logic lab=trim[0]}
C {lab_pin.sym} 860 480 0 1 {name=l52 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1240 300 0 0 {name=MIP1
L=0.28u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1280 300 0 1 {name=l53 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1240 420 0 0 {name=MIN1
L=0.28u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1280 420 0 1 {name=l54 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1260 250 0 1 {name=l55 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1260 360 0 1 {name=l56 sig_type=std_logic lab=tb1}
C {lab_pin.sym} 1180 360 0 0 {name=l57 sig_type=std_logic lab=trim[1]}
C {lab_pin.sym} 1260 480 0 1 {name=l58 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1640 300 0 0 {name=MIP2
L=0.28u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1680 300 0 1 {name=l59 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1640 420 0 0 {name=MIN2
L=0.28u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 1680 420 0 1 {name=l60 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1660 250 0 1 {name=l61 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1660 360 0 1 {name=l62 sig_type=std_logic lab=tb2}
C {lab_pin.sym} 1580 360 0 0 {name=l63 sig_type=std_logic lab=trim[2]}
C {lab_pin.sym} 1660 480 0 1 {name=l64 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 2040 300 0 0 {name=MIP3
L=0.28u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2080 300 0 1 {name=l65 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2040 420 0 0 {name=MIN3
L=0.28u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2080 420 0 1 {name=l66 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2060 250 0 1 {name=l67 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2060 360 0 1 {name=l68 sig_type=std_logic lab=tb3}
C {lab_pin.sym} 1980 360 0 0 {name=l69 sig_type=std_logic lab=trim[3]}
C {lab_pin.sym} 2060 480 0 1 {name=l70 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2480 90 0 0 {name=l71 sig_type=std_logic lab=aux}
C {symbols/nfet_03v3.sym} 2460 150 0 0 {name=MAUX
L=8.0u
W=10.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2500 150 0 1 {name=l72 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2420 150 0 0 {name=l73 sig_type=std_logic lab=vaux}
C {symbols/nfet_03v3.sym} 2680 150 0 0 {name=MCAL
L=0.5u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2720 150 0 1 {name=l74 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2640 150 0 0 {name=l75 sig_type=std_logic lab=cal}
C {lab_pin.sym} 2700 210 0 1 {name=l76 sig_type=std_logic lab=vaux}
C {symbols/nfet_03v3.sym} 2780 300 0 0 {name=MDIS
L=45.45u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2820 300 0 1 {name=l77 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2800 250 0 1 {name=l78 sig_type=std_logic lab=vaux}
C {lab_pin.sym} 2740 300 0 0 {name=l79 sig_type=std_logic lab=calb}
C {symbols/nfet_03v3.sym} 2680 420 0 0 {name=MCAUX
L=5.0u
W=5.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2720 420 0 1 {name=l80 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2640 420 0 0 {name=l81 sig_type=std_logic lab=vaux}
C {symbols/pfet_03v3.sym} 2380 300 0 0 {name=MIPC
L=0.28u
W=1.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2420 300 0 1 {name=l82 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2380 420 0 0 {name=MINC
L=0.28u
W=0.5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2420 420 0 1 {name=l83 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2400 250 0 1 {name=l84 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2400 360 0 1 {name=l85 sig_type=std_logic lab=calb}
C {lab_pin.sym} 2320 360 0 0 {name=l86 sig_type=std_logic lab=cal}
