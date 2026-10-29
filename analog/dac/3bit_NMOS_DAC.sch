v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -80 -80 -80 -40 {lab=#net1}
N 80 -80 80 -40 {lab=#net2}
N 240 -80 240 -40 {lab=#net3}
N -80 -180 -80 -140 {lab=Iout}
N -80 -180 240 -180 {lab=Iout}
N 240 -180 240 -140 {lab=Iout}
N 80 -180 80 -140 {lab=Iout}
N 80 20 80 40 {lab=vss}
N 240 20 240 40 {lab=vss}
N -80 20 -80 40 {lab=vss}
N -140 -10 -120 -10 {lab=Vbias}
N 20 -10 40 -10 {lab=Vbias}
N 180 -10 200 -10 {lab=Vbias}
N -140 -110 -120 -110 {lab=Vw0}
N 20 -110 40 -110 {lab=Vw1}
N 180 -110 200 -110 {lab=Vw2}
N -80 -110 -60 -110 {lab=vss}
N 80 -110 110 -110 {lab=vss}
N 240 -110 280 -110 {lab=vss}
N -80 -10 -60 -10 {lab=vss}
N 80 -10 110 -10 {lab=vss}
N 240 -10 270 -10 {lab=vss}
C {symbols/nfet_03v3.sym} -100 -110 0 0 {name=M1
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
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} -100 -10 0 0 {name=M2
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
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 60 -110 0 0 {name=M3
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
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 60 -10 0 0 {name=M4
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
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 220 -110 0 0 {name=M5
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
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 220 -10 0 0 {name=M6
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
model=nfet_03v3
spiceprefix=X
}
C {ipin.sym} -360 -300 0 0 {name=p1 lab=Vw0}
C {iopin.sym} -360 -200 0 0 {name=p2 lab=vdd}
C {iopin.sym} -360 -180 0 0 {name=p3 lab=vss}
C {opin.sym} -360 -140 0 0 {name=p13 lab=Iout
}
C {ipin.sym} -360 -280 0 0 {name=p5 lab=Vw1}
C {ipin.sym} -360 -260 0 0 {name=p6 lab=Vw2}
C {ipin.sym} -360 -220 0 0 {name=p8 lab=Vbias}
C {lab_wire.sym} -80 40 0 0 {name=p7 sig_type=std_logic lab=vss}
C {lab_wire.sym} 80 40 0 0 {name=p9 sig_type=std_logic lab=vss}
C {lab_wire.sym} 240 40 0 0 {name=p10 sig_type=std_logic lab=vss}
C {lab_wire.sym} -130 -10 0 0 {name=p11 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} 30 -10 0 0 {name=p12 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} 190 -10 0 0 {name=p14 sig_type=std_logic lab=Vbias}
C {lab_wire.sym} -140 -110 0 0 {name=p15 sig_type=std_logic lab=Vw0}
C {lab_wire.sym} 30 -110 0 0 {name=p16 sig_type=std_logic lab=Vw1}
C {lab_wire.sym} 190 -110 0 0 {name=p17 sig_type=std_logic lab=Vw2}
C {lab_wire.sym} 280 -110 0 1 {name=p18 sig_type=std_logic lab=vss}
C {lab_wire.sym} 110 -110 0 1 {name=p19 sig_type=std_logic lab=vss}
C {lab_wire.sym} -60 -110 0 1 {name=p20 sig_type=std_logic lab=vss}
C {lab_wire.sym} 270 -10 0 1 {name=p21 sig_type=std_logic lab=vss}
C {lab_wire.sym} 110 -10 0 1 {name=p22 sig_type=std_logic lab=vss}
C {lab_wire.sym} -60 -10 0 1 {name=p23 sig_type=std_logic lab=vss}
C {lab_wire.sym} 40 -180 0 0 {name=p24 sig_type=std_logic lab=Iout}
