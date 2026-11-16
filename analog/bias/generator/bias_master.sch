v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
E {}
T {bias_master: beta-multiplier reference} -380 -420 0 0 0.5 0.5 {}
T {I0 = n UT ln(K) / R = 200 nA; the Iref pin sinks 4/8 x I0 = 100 nA (the patent's reference current source, into trim_steer's M0)} -380 -380 0 0 0.3 0.3 {}
C {iopin.sym} -340 -280 0 0 {name=p1 lab=VDD}
C {iopin.sym} -340 -240 0 0 {name=p2 lab=VSS}
N -120 -260 20 -260 {}
N 20 -260 460 -260 {}
N 460 -260 720 -260 {}
N 720 -260 1160 -260 {}
N 1160 -260 1300 -260 {}
N -120 300 20 300 {}
N 20 300 460 300 {}
N 460 300 720 300 {}
N 720 300 900 300 {}
N 900 300 1160 300 {}
N 1160 300 1300 300 {}
N -120 -260 -140 -260 {}
C {lab_pin.sym} -140 -260 0 0 {name=l3 sig_type=std_logic lab=VDD}
N -120 300 -140 300 {}
C {lab_pin.sym} -140 300 0 0 {name=l4 sig_type=std_logic lab=VSS}
T {Master reference (beta multiplier)} -60 -230 0 0 0.4 0.4 {}
C {symbols/pfet_03v3.sym} 0 -150 0 0 {name=M3
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
N 20 -150 40 -150 {}
C {lab_pin.sym} 40 -150 0 1 {name=l5 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} 440 -150 0 0 {name=M4
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
N 460 -150 480 -150 {}
C {lab_pin.sym} 480 -150 0 1 {name=l6 sig_type=std_logic lab=VDD}
N 20 -260 20 -180 {}
N 460 -260 460 -180 {}
N 20 -120 20 -80 {}
N 20 -80 20 -30 {}
N 20 -80 -40 -80 {}
N -40 -80 -40 -150 {}
N -40 -150 -20 -150 {}
N 20 -80 380 -80 {}
N 380 -80 380 -150 {}
N 380 -150 420 -150 {}
C {lab_pin.sym} -40 -80 0 0 {name=l7 sig_type=std_logic lab=Vgp}
C {symbols/nfet_03v3.sym} 0 0 0 0 {name=M2
L=6.0u
W=1.0u
nf=1
m=64
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
N 20 0 40 0 {}
C {lab_pin.sym} 40 0 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {symbols/nfet_03v3.sym} 440 0 0 0 {name=M1
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
model=nfet_03v3
spiceprefix=X
}
N 460 0 480 0 {}
C {lab_pin.sym} 480 0 0 1 {name=l9 sig_type=std_logic lab=VSS}
T {M2 = 8 x M1} -150 40 0 0 0.25 0.25 {}
N 460 -120 460 -60 {}
N 460 -60 460 -30 {}
N 460 -60 400 -60 {}
N 400 -60 400 0 {}
N 400 0 420 0 {}
C {lab_pin.sym} 400 -60 0 1 {name=l10 sig_type=std_logic lab=Vgn}
N -20 0 -40 0 {}
C {lab_pin.sym} -40 0 0 0 {name=l11 sig_type=std_logic lab=Vgn}
N 460 30 460 300 {}
N 20 30 20 50 {}
N 20 50 20 70 {}
C {lab_pin.sym} 20 50 0 1 {name=l12 sig_type=std_logic lab=Vr}
C {symbols/nwell.sym} 20 100 0 0 {name=R
W=2.0e-6
L=585.380e-6
model=nwell
spiceprefix=X
m=1
}
N 0 100 -20 100 {}
C {lab_pin.sym} -20 100 0 0 {name=l13 sig_type=std_logic lab=VSS}
T {n-well 2 um wide, 292.7 squares (+2900 ppm/K: cancels UT's +3300 ppm/K)} -360 140 0 0 0.25 0.25 {}
N 20 130 20 300 {}
T {Start-up} 670 -230 0 0 0.4 0.4 {}
T {MS1: 4 x 0.22/50 in series, always on} 760 -200 0 0 0.2 0.2 {}
C {symbols/pfet_03v3.sym} 700 -150 0 0 {name=MS1_0
L=50u
W=0.22u
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
N 720 -150 740 -150 {}
C {lab_pin.sym} 740 -150 0 1 {name=l14 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} 700 -90 0 0 {name=MS1_1
L=50u
W=0.22u
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
N 720 -90 740 -90 {}
C {lab_pin.sym} 740 -90 0 1 {name=l15 sig_type=std_logic lab=VDD}
N 680 -150 680 -90 {}
C {symbols/pfet_03v3.sym} 700 -30 0 0 {name=MS1_2
L=50u
W=0.22u
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
N 720 -30 740 -30 {}
C {lab_pin.sym} 740 -30 0 1 {name=l16 sig_type=std_logic lab=VDD}
N 680 -90 680 -30 {}
C {symbols/pfet_03v3.sym} 700 30 0 0 {name=MS1_3
L=50u
W=0.22u
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
N 720 30 740 30 {}
C {lab_pin.sym} 740 30 0 1 {name=l17 sig_type=std_logic lab=VDD}
N 680 -30 680 30 {}
N 720 -260 720 -180 {}
N 680 -150 660 -150 {}
C {lab_pin.sym} 660 -150 0 0 {name=l18 sig_type=std_logic lab=VSS}
N 720 60 720 90 {}
N 720 90 720 120 {}
C {symbols/nfet_03v3.sym} 700 150 0 0 {name=MS2
L=6.0u
W=1.0u
nf=1
m=16
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
N 720 150 740 150 {}
C {lab_pin.sym} 740 150 0 1 {name=l19 sig_type=std_logic lab=VSS}
N 680 150 660 150 {}
C {lab_pin.sym} 660 150 0 0 {name=l20 sig_type=std_logic lab=Vgn}
N 720 180 720 300 {}
N 720 90 840 90 {}
N 840 90 840 150 {}
N 840 150 860 150 {}
C {lab_pin.sym} 840 90 0 1 {name=l21 sig_type=std_logic lab=X}
C {symbols/nfet_03v3.sym} 880 150 0 0 {name=MS3
L=4u
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
N 900 150 920 150 {}
C {lab_pin.sym} 920 150 0 1 {name=l22 sig_type=std_logic lab=VSS}
N 900 120 920 120 {}
C {lab_pin.sym} 920 120 0 1 {name=l23 sig_type=std_logic lab=Vgp}
N 900 180 900 300 {}
T {off (X = 0) once the reference runs} 760 220 0 0 0.2 0.2 {}
T {Output} 1130 -230 0 0 0.4 0.4 {}
C {symbols/nfet_03v3.sym} 1140 150 0 0 {name=MREF
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
model=nfet_03v3
spiceprefix=X
}
N 1160 150 1180 150 {}
C {lab_pin.sym} 1180 150 0 1 {name=l24 sig_type=std_logic lab=VSS}
N 1120 150 1100 150 {}
C {lab_pin.sym} 1100 150 0 0 {name=l25 sig_type=std_logic lab=Vgn}
N 1160 180 1160 300 {}
N 1160 120 1160 40 {}
N 1160 40 1260 40 {}
C {iopin.sym} 1260 40 0 0 {name=p26 lab=Iref}
T {Iref = 4/8 of M1 = 100 nA (sink)} 1180 60 0 0 0.25 0.25 {}
