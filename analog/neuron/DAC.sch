v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 100 -120 270 -120 {lab=Isum}
N 270 -120 450 -120 {lab=Isum}
N 450 -120 620 -120 {lab=Isum}
N 620 -60 620 -10 {lab=#net1}
N 450 80 620 80 {lab=GND}
N 270 80 450 80 {lab=GND}
N 100 80 270 80 {lab=GND}
N 360 80 360 130 {lab=GND}
N 30 20 60 20 {lab=Vb}
N 30 20 30 60 {lab=Vb}
N 0 60 560 60 {lab=Vb}
N 560 20 560 60 {lab=Vb}
N 560 20 580 20 {lab=Vb}
N 620 50 620 80 {lab=GND}
N 450 50 450 80 {lab=GND}
N 270 50 270 80 {lab=GND}
N 100 50 100 80 {lab=GND}
N 230 20 230 60 {lab=Vb}
N 410 20 410 60 {lab=Vb}
N 270 -60 270 -10 {lab=#net2}
N 450 -60 450 -10 {lab=#net3}
N 100 -60 100 -10 {lab=#net4}
N 20 -90 60 -90 {lab=w0}
N 190 -90 230 -90 {lab=w1}
N 370 -90 410 -90 {lab=w2}
N 530 -90 580 -90 {lab=w3}
N 100 -90 120 -90 {lab=#net4}
N 120 -90 120 -50 {lab=#net4}
N 100 -50 120 -50 {lab=#net4}
N 100 50 120 50 {lab=GND}
N 100 20 120 20 {lab=GND}
N 120 20 120 50 {lab=GND}
N 270 50 290 50 {lab=GND}
N 270 20 290 20 {lab=GND}
N 290 20 290 50 {lab=GND}
N 450 50 470 50 {lab=GND}
N 450 20 470 20 {lab=GND}
N 470 20 470 50 {lab=GND}
N 620 50 640 50 {lab=GND}
N 620 20 640 20 {lab=GND}
N 640 20 640 50 {lab=GND}
N 357.5 -172.5 357.5 -120 {lab=Isum}
N 270 -90 290 -90 {lab=#net2}
N 290 -90 290 -57.5 {lab=#net2}
N 270 -57.5 290 -57.5 {lab=#net2}
N 450 -90 472.5 -90 {lab=#net3}
N 472.5 -90 472.5 -55 {lab=#net3}
N 450 -55 472.5 -55 {lab=#net3}
N 620 -90 635 -90 {lab=#net1}
N 635 -90 635 -52.5 {lab=#net1}
N 620 -52.5 635 -52.5 {lab=#net1}
C {symbols/nfet_03v3.sym} 80 -90 0 0 {name=M1
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
C {symbols/nfet_03v3.sym} 80 20 0 0 {name=M2
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
C {symbols/nfet_03v3.sym} 250 -90 0 0 {name=M3
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
C {symbols/nfet_03v3.sym} 250 20 0 0 {name=M4
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
C {symbols/nfet_03v3.sym} 430 -90 0 0 {name=M5
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
C {symbols/nfet_03v3.sym} 430 20 0 0 {name=M6
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
C {symbols/nfet_03v3.sym} 600 -90 0 0 {name=M7
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
C {symbols/nfet_03v3.sym} 600 20 0 0 {name=M8
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
C {iopin.sym} -162.5 -117.5 0 0 {name=p1 lab=Vb}
C {ipin.sym} -122.5 -17.5 0 0 {name=p3 lab=w0}
C {ipin.sym} -122.5 22.5 0 0 {name=p4 lab=w1}
C {ipin.sym} -122.5 62.5 0 0 {name=p5 lab=w2}
C {ipin.sym} -122.5 102.5 0 0 {name=p6 lab=w3}
C {lab_wire.sym} 30 -90 0 0 {name=p7 sig_type=std_logic lab=w0}
C {lab_wire.sym} 200 -90 0 0 {name=p8 sig_type=std_logic lab=w1}
C {lab_wire.sym} 380 -90 0 0 {name=p9 sig_type=std_logic lab=w2}
C {lab_wire.sym} 540 -90 0 0 {name=p10 sig_type=std_logic lab=w3}
C {gnd.sym} 360 130 0 0 {name=l1 lab=GND}
C {lab_wire.sym} 7.5 60 0 0 {name=p11 sig_type=std_logic lab=Vb}
C {ipin.sym} 357.5 -172.5 0 0 {name=p2 lab=Isum}
