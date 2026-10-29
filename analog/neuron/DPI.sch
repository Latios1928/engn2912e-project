v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 10 -2.5 30 -2.5 {lab=Isum}
N 30 -2.5 30 37.5 {lab=Isum}
N 10 37.5 30 37.5 {lab=Isum}
N 10 60 160 60 {lab=Isum}
N 160 60 240 60 {lab=Isum}
N 240 40 240 60 {lab=Isum}
N 220 10 240 10 {lab=Isum}
N 220 10 220 40 {lab=Isum}
N 220 40 240 40 {lab=Isum}
N 240 -100 240 -20 {lab=#net1}
N 152.5 -130 200 -130 {lab=VT}
N 240 -130 262.5 -130 {lab=VDD}
N 240 -160 262.5 -160 {lab=VDD}
N 262.5 -160 262.5 -130 {lab=VDD}
N 240 -180 240 -160 {lab=VDD}
N 240 -60 355 -60 {lab=#net1}
N 280 10 355 10 {lab=#net1}
N 355 -60 355 10 {lab=#net1}
N 355 -75 355 -60 {lab=#net1}
N 355 -60 447.5 -60 {lab=#net1}
N 487.5 -60 510 -60 {lab=VDD}
N 487.5 -90 510 -90 {lab=VDD}
N 510 -90 510 -60 {lab=VDD}
N 487.5 -110 487.5 -90 {lab=VDD}
N 487.5 -180 487.5 -110 {lab=VDD}
N 487.5 -30 487.5 5 {lab=Isyn}
N 122.5 60 122.5 105 {lab=Isum}
N 240 -180 487.5 -180 {lab=VDD}
N 10 -180 10 -32.5 {lab=VDD}
N 10 -180 242.5 -180 {lab=VDD}
N -52.5 -2.5 -30 -2.5 {lab=Vthr}
N 487.5 5 487.5 10 {lab=Isyn}
N 355 -180 355 -140 {lab=VDD}
N 355 -80 355 -75 {lab=#net1}
N 10 27.5 10 37.5 {lab=Isum}
N 10 37.5 10 60 {lab=Isum}
C {symbols/nfet_03v3.sym} -10 -2.5 0 0 {name=M1
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
C {symbols/nfet_03v3.sym} 260 10 0 1 {name=M2
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
C {symbols/pfet_03v3.sym} 220 -130 0 0 {name=M3
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
C {symbols/pfet_03v3.sym} 467.5 -60 0 0 {name=M4
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
C {ipin.sym} -165 -132.5 0 0 {name=p1 lab=Vthr}
C {iopin.sym} -167.5 -170 0 1 {name=p9 lab=VDD}
C {lab_wire.sym} -52.5 -2.5 0 0 {name=p2 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} 10 -180 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {opin.sym} -167.5 -92.5 2 0 {name=p4 lab=Isyn}
C {lab_wire.sym} 487.5 10 0 0 {name=p5 sig_type=std_logic lab=Isyn}
C {opin.sym} -167.5 -52.5 2 0 {name=p6 lab=Isum}
C {lab_wire.sym} 122.5 102.5 0 0 {name=p7 sig_type=std_logic lab=Isum}
C {ipin.sym} -170 -17.5 0 0 {name=p8 lab=VT}
C {lab_wire.sym} 155 -130 0 0 {name=p10 sig_type=std_logic lab=VT}
C {capa.sym} 355 -110 0 0 {name=C4
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
