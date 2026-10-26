v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 30 150 110 150 {lab=reset_bias}
N -0 120 0 150 {lab=VSS}
N -120 150 -30 150 {lab=MEM}
N -120 210 -120 250 {lab=VSS}
N 130 20 260 20 {lab=VSS}
N 130 -0 260 -0 {lab=VDD}
N 130 -20 250 -20 {lab=VN}
N 250 -20 260 -20 {lab=VN}
N 130 -40 260 -40 {lab=VP}
N 130 -60 260 -60 {lab=VOUT}
N -250 -60 -170 -60 {lab=MEM}
N 270 100 270 210 {lab=VOUT}
N 270 150 300 150 {lab=VOUT}
N 230 50 230 70 {lab=VDD}
N 230 240 230 260 {lab=VSS}
N 200 210 230 210 {lab=VSS}
N 200 100 230 100 {lab=VDD}
N 230 130 230 180 {lab=#net1}
N -0 190 140 190 {lab=#net1}
N 140 150 140 190 {lab=#net1}
N 140 150 230 150 {lab=#net1}
N 40 250 40 280 {lab=VSS}
C {symbols/nfet_03v3.sym} 0 170 3 0 {name=M1
L=0.28u
W=2u
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
C {lab_wire.sym} 0 120 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {capa.sym} -120 180 0 0 {name=C1
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} -120 250 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -250 -60 0 0 {name=p4 sig_type=std_logic lab=MEM}
C {lab_wire.sym} -120 150 0 0 {name=p5 sig_type=std_logic lab=MEM}
C {lab_wire.sym} 260 -60 0 0 {name=p6 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 260 -40 0 0 {name=p7 sig_type=std_logic lab=VP}
C {lab_wire.sym} 260 -20 0 0 {name=p8 sig_type=std_logic lab=VN}
C {lab_wire.sym} 260 0 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 260 20 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 110 150 0 0 {name=p11 sig_type=std_logic lab=reset_bias}
C {iopin.sym} -560 -60 0 0 {name=p12 lab=VDD}
C {iopin.sym} -560 -30 0 0 {name=p13 lab=VSS}
C {opin.sym} -560 0 0 0 {name=p14 lab=VP}
C {opin.sym} -560 30 0 0 {name=p15 lab=VN}
C {opin.sym} -560 60 0 0 {name=p16 lab=VOUT}
C {iopin.sym} -560 90 0 0 {name=p17 lab=MEM}
C {iopin.sym} -560 120 0 0 {name=p18 lab=reset_bias}
C {comparator.sym} -20 -20 0 0 {name=x1}
C {symbols/nfet_03v3.sym} 250 210 0 1 {name=M2
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
C {symbols/pfet_03v3.sym} 250 100 0 1 {name=M3
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
C {lab_wire.sym} 300 150 0 0 {name=p19 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 230 50 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 100 0 0 {name=p20 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 210 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 230 260 0 0 {name=p22 sig_type=std_logic lab=VSS}
C {capa.sym} 40 220 0 0 {name=C2
m=1
value=100f
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} 40 280 0 0 {name=p23 sig_type=std_logic lab=VSS}
