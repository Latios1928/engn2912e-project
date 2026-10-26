v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -0 -40 0 -10 {lab=VN}
N -0 -30 170 -30 {lab=VN}
N -0 50 0 80 {lab=VSS}
N 230 -30 290 -30 {lab=VDD}
N 0 -220 -0 -190 {lab=#net1}
N 0 -210 170 -210 {lab=#net1}
N 200 -170 200 -70 {lab=#net2}
N 0 -130 -0 -100 {lab=#net2}
N 0 -120 200 -120 {lab=#net2}
N -90 -250 -40 -250 {lab=VIN}
N -90 -250 -90 20 {lab=VIN}
N -90 20 -40 20 {lab=VIN}
N -90 -70 -40 -70 {lab=VIN}
N -90 -160 -40 -160 {lab=VIN}
N -170 -110 -90 -110 {lab=VIN}
N -0 -310 -0 -280 {lab=VDD}
C {ipin.sym} -390 -230 0 0 {name=p9 lab=VIN}
C {opin.sym} -410 -190 0 0 {name=p10 lab=VOUT
}
C {iopin.sym} -410 -90 0 0 {name=p11 lab=VDD}
C {iopin.sym} -410 -50 0 0 {name=p12 lab=VSS}
C {opin.sym} -410 -130 0 0 {name=p13 lab=VN
}
C {opin.sym} -410 -160 0 0 {name=p14 lab=VP
}
C {symbols/nfet_03v3.sym} -20 -70 0 0 {name=M1
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
C {symbols/nfet_03v3.sym} -20 20 0 0 {name=M2
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
C {symbols/nfet_03v3.sym} 200 -50 1 0 {name=M3
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
C {lab_wire.sym} 290 -30 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 0 80 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 120 -30 0 0 {name=p3 sig_type=std_logic lab=VN}
C {symbols/pfet_03v3.sym} -20 -160 0 0 {name=M4
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
C {symbols/pfet_03v3.sym} -20 -250 0 0 {name=M5
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
C {symbols/pfet_03v3.sym} 200 -190 3 0 {name=M6
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
C {lab_wire.sym} -170 -110 0 0 {name=p4 sig_type=std_logic lab=VIN}
C {lab_wire.sym} 0 -310 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 120 -120 0 0 {name=p6 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 120 -210 0 0 {name=p7 sig_type=std_logic lab=VP}
