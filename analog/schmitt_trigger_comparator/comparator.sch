v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -0 -30 -0 -0 {lab=VN}
N 0 -130 0 -90 {lab=VOUT}
N 0 -220 -0 -190 {lab=VP}
N 0 -310 -0 -280 {lab=VDD}
N -0 60 0 90 {lab=VSS}
N -40 -250 -40 30 {lab=VIN}
N -110 -120 -40 -120 {lab=VIN}
N -0 -210 110 -210 {lab=VP}
N -0 -20 110 -20 {lab=VN}
N 110 -20 150 -20 {lab=VN}
N 110 -210 150 -210 {lab=VP}
N 180 -170 180 -60 {lab=VOUT}
N -0 -120 180 -120 {lab=VOUT}
N 180 -120 320 -120 {lab=VOUT}
N 210 -20 240 -20 {lab=VDD}
N 210 -210 240 -210 {lab=VSS}
C {symbols/nfet_03v3.sym} -20 -250 0 0 {name=M2
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
C {symbols/nfet_03v3.sym} 180 -40 1 0 {name=M3
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
C {symbols/pfet_03v3.sym} -20 -60 0 0 {name=M6
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
C {symbols/pfet_03v3.sym} -20 30 0 0 {name=M8
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
C {lab_wire.sym} 0 90 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 0 -310 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -110 -120 0 0 {name=p3 sig_type=std_logic lab=VIN
}
C {lab_wire.sym} 110 -210 0 0 {name=p5 sig_type=std_logic lab=VP
}
C {lab_wire.sym} 110 -20 0 0 {name=p6 sig_type=std_logic lab=VN
}
C {symbols/nfet_03v3.sym} -20 -160 0 0 {name=M9
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
C {symbols/nfet_03v3.sym} 180 -190 1 1 {name=M1
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
C {lab_wire.sym} 320 -120 0 0 {name=p4 sig_type=std_logic lab=VOUT
}
C {lab_wire.sym} 240 -210 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 240 -20 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {ipin.sym} -390 -230 0 0 {name=p9 lab=VIN}
C {opin.sym} -410 -190 0 0 {name=p10 lab=VOUT
}
C {iopin.sym} -410 -90 0 0 {name=p11 lab=VDD}
C {iopin.sym} -410 -50 0 0 {name=p12 lab=VSS}
C {opin.sym} -410 -130 0 0 {name=p13 lab=VN
}
C {opin.sym} -410 -160 0 0 {name=p14 lab=VP
}
