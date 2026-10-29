v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 0 -80 0 -40 {lab=#net1}
N 160 -80 160 -40 {lab=#net2}
N 320 -80 320 -40 {lab=#net3}
N 0 -180 0 -140 {lab=vdd}
N 0 70 320 70 {lab=Iout}
N 320 -180 320 -140 {lab=vdd}
N 160 -180 160 -140 {lab=vdd}
N -60 -10 -40 -10 {lab=Vw0_b}
N 100 -10 120 -10 {lab=Vw1_b}
N 260 -10 280 -10 {lab=Vw2}
N -60 -110 -40 -110 {lab=Vbias}
N 100 -110 120 -110 {lab=Vbias}
N 260 -110 280 -110 {lab=Vbias}
N 0 -110 20 -110 {lab=vdd}
N 160 -110 190 -110 {lab=vdd}
N 320 -110 360 -110 {lab=vdd}
N 0 -10 20 -10 {lab=vdd}
N 160 -10 190 -10 {lab=vdd}
N 320 -10 350 -10 {lab=vdd}
N -0 20 -0 70 {lab=Iout}
N 160 20 160 70 {lab=Iout}
N 320 20 320 70 {lab=Iout}
C {ipin.sym} -280 -300 0 0 {name=p1 lab=Vw0}
C {iopin.sym} -280 -200 0 0 {name=p2 lab=vdd}
C {opin.sym} -280 -140 0 0 {name=p13 lab=Iout
}
C {ipin.sym} -280 -280 0 0 {name=p5 lab=Vw1}
C {ipin.sym} -280 -260 0 0 {name=p6 lab=Vw2}
C {ipin.sym} -280 -220 0 0 {name=p8 lab=Vbias}
C {lab_wire.sym} -60 -110 0 0 {name=p11 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} 110 -110 0 0 {name=p12 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} 270 -110 0 0 {name=p14 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} -60 -10 0 0 {name=p15 sig_type=std_logic lab=Vw0_b}
C {lab_wire.sym} 100 -10 0 0 {name=p16 sig_type=std_logic lab=Vw1_b}
C {lab_wire.sym} 270 -10 0 0 {name=p17 sig_type=std_logic lab=Vw2_b}
C {lab_wire.sym} 360 -110 0 1 {name=p18 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 190 -110 0 1 {name=p19 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 20 -110 0 1 {name=p20 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 350 -10 0 1 {name=p21 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 190 -10 0 1 {name=p22 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 20 -10 0 1 {name=p23 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 110 70 0 0 {name=p24 sig_type=std_logic lab=Iout}
C {symbols/pfet_03v3.sym} -20 -110 0 0 {name=M1
L=0.28u
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
C {symbols/pfet_03v3.sym} 140 -110 0 0 {name=M2
L=0.28u
W=0.22u
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
C {symbols/pfet_03v3.sym} 300 -110 0 0 {name=M3
L=0.28u
W=0.22u
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
C {symbols/pfet_03v3.sym} 300 -10 0 0 {name=M4
L=0.28u
W=0.22u
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
C {symbols/pfet_03v3.sym} 140 -10 0 0 {name=M5
L=0.28u
W=0.22u
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
C {symbols/pfet_03v3.sym} -20 -10 0 0 {name=M6
L=0.28u
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
C {lab_wire.sym} 0 -170 0 0 {name=p4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 160 -170 0 0 {name=p7 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 320 -170 0 0 {name=p9 sig_type=std_logic lab=vdd}
