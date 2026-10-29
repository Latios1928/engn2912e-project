v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -100 0 -60 0 {lab=VSS}
N 50 0 120 0 {lab=VSS}
N -100 30 -100 50 {lab=#net1}
N -100 50 120 50 {lab=#net1}
N 120 30 120 50 {lab=#net1}
N -0 50 -0 90 {lab=#net1}
N -0 150 0 190 {lab=VSS}
N -210 -0 -140 -0 {lab=VP}
N 160 -0 240 0 {lab=VN}
N -100 -130 -100 -30 {lab=#net2}
N 120 -130 120 -30 {lab=spike_out}
N -170 -160 -140 -160 {lab=#net2}
N -170 -220 -170 -160 {lab=#net2}
N -170 -220 160 -220 {lab=#net2}
N 160 -220 160 -160 {lab=#net2}
N -170 -160 -170 -120 {lab=#net2}
N -170 -120 -100 -120 {lab=#net2}
N -100 -250 -100 -190 {lab=VDD}
N 120 -250 120 -190 {lab=VDD}
N -100 -160 -60 -160 {lab=VDD}
N 70 -160 120 -160 {lab=VDD}
N -110 120 -40 120 {lab=VB}
N -0 120 40 120 {lab=VSS}
N 120 -90 200 -90 {lab=spike_out}
C {symbols/nfet_03v3.sym} -120 0 0 0 {name=M1
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
C {symbols/nfet_03v3.sym} 140 0 0 1 {name=M2
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
C {lab_wire.sym} -60 0 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 50 0 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {symbols/nfet_03v3.sym} -20 120 0 0 {name=M3
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
C {lab_wire.sym} 0 190 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -210 0 0 0 {name=p4 sig_type=std_logic lab=VP}
C {lab_wire.sym} 240 0 0 0 {name=p5 sig_type=std_logic lab=VN}
C {symbols/pfet_03v3.sym} -120 -160 0 0 {name=M4
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
C {symbols/pfet_03v3.sym} 140 -160 0 1 {name=M5
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
C {lab_wire.sym} -100 -250 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 120 -250 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -60 -160 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 70 -160 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -110 120 0 0 {name=p10 sig_type=std_logic lab=VB}
C {lab_wire.sym} 40 120 0 0 {name=p11 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 200 -90 0 0 {name=p12 sig_type=std_logic lab=spike_out}
C {iopin.sym} -320 -150 0 0 {name=p13 lab=VDD}
C {iopin.sym} -320 -110 0 0 {name=p14 lab=VSS}
C {ipin.sym} -300 -70 0 0 {name=p15 lab=VP}
C {ipin.sym} -300 -30 0 0 {name=p16 lab=VN}
C {ipin.sym} -300 10 0 0 {name=p17 lab=VB}
C {opin.sym} -320 50 0 0 {name=p18 lab=spike_out}
