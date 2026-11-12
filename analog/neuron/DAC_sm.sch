v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {symbols/nfet_03v3.sym} 100 -90 0 0 {name=M1
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
C {lab_pin.sym} 120 -120 0 1 {name=l1 sig_type=std_logic lab=X}
C {lab_pin.sym} 80 -90 0 0 {name=l2 sig_type=std_logic lab=w[0]}
C {lab_pin.sym} 120 -60 0 1 {name=l3 sig_type=std_logic lab=n0}
C {lab_pin.sym} 120 -90 0 1 {name=l4 sig_type=std_logic lab=n0}
C {symbols/nfet_03v3.sym} 100 30 0 0 {name=M2
L=8u
W=1u
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
C {lab_pin.sym} 120 0 0 1 {name=l5 sig_type=std_logic lab=n0}
C {lab_pin.sym} 80 30 0 0 {name=l6 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 120 60 0 1 {name=l7 sig_type=std_logic lab=GND}
C {lab_pin.sym} 120 30 0 1 {name=l8 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 320 -90 0 0 {name=M3
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
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 340 -120 0 1 {name=l9 sig_type=std_logic lab=X}
C {lab_pin.sym} 300 -90 0 0 {name=l10 sig_type=std_logic lab=w[1]}
C {lab_pin.sym} 340 -60 0 1 {name=l11 sig_type=std_logic lab=n1}
C {lab_pin.sym} 340 -90 0 1 {name=l12 sig_type=std_logic lab=n1}
C {symbols/nfet_03v3.sym} 320 30 0 0 {name=M4
L=8u
W=1u
nf=1
m=2
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 340 0 0 1 {name=l13 sig_type=std_logic lab=n1}
C {lab_pin.sym} 300 30 0 0 {name=l14 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 340 60 0 1 {name=l15 sig_type=std_logic lab=GND}
C {lab_pin.sym} 340 30 0 1 {name=l16 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 540 -90 0 0 {name=M5
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
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 560 -120 0 1 {name=l17 sig_type=std_logic lab=X}
C {lab_pin.sym} 520 -90 0 0 {name=l18 sig_type=std_logic lab=w[2]}
C {lab_pin.sym} 560 -60 0 1 {name=l19 sig_type=std_logic lab=n2}
C {lab_pin.sym} 560 -90 0 1 {name=l20 sig_type=std_logic lab=n2}
C {symbols/nfet_03v3.sym} 540 30 0 0 {name=M6
L=8u
W=1u
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
C {lab_pin.sym} 560 0 0 1 {name=l21 sig_type=std_logic lab=n2}
C {lab_pin.sym} 520 30 0 0 {name=l22 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 560 60 0 1 {name=l23 sig_type=std_logic lab=GND}
C {lab_pin.sym} 560 30 0 1 {name=l24 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 100 -260 0 0 {name=Men
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
C {lab_pin.sym} 120 -290 0 1 {name=l25 sig_type=std_logic lab=Y}
C {lab_pin.sym} 80 -260 0 0 {name=l26 sig_type=std_logic lab=en}
C {lab_pin.sym} 120 -230 0 1 {name=l27 sig_type=std_logic lab=X}
C {lab_pin.sym} 120 -260 0 1 {name=l28 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 320 -260 0 0 {name=Mse
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
C {lab_pin.sym} 340 -290 0 1 {name=l29 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} 300 -260 0 0 {name=l30 sig_type=std_logic lab=sb}
C {lab_pin.sym} 340 -230 0 1 {name=l31 sig_type=std_logic lab=Y}
C {lab_pin.sym} 340 -260 0 1 {name=l32 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 540 -260 0 0 {name=Msi
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
C {lab_pin.sym} 560 -290 0 1 {name=l33 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} 520 -260 0 0 {name=l34 sig_type=std_logic lab=w[3]}
C {lab_pin.sym} 560 -230 0 1 {name=l35 sig_type=std_logic lab=Y}
C {lab_pin.sym} 560 -260 0 1 {name=l36 sig_type=std_logic lab=GND}
C {symbols/pfet_03v3.sym} 760 -300 0 0 {name=Mpi
L=0.28u
W=0.44u
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
C {lab_pin.sym} 780 -330 0 1 {name=l37 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 740 -300 0 0 {name=l38 sig_type=std_logic lab=w[3]}
C {lab_pin.sym} 780 -270 0 1 {name=l39 sig_type=std_logic lab=sb}
C {lab_pin.sym} 780 -300 0 1 {name=l40 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 760 -170 0 0 {name=Mni
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
C {lab_pin.sym} 780 -200 0 1 {name=l41 sig_type=std_logic lab=sb}
C {lab_pin.sym} 740 -170 0 0 {name=l42 sig_type=std_logic lab=w[3]}
C {lab_pin.sym} 780 -140 0 1 {name=l43 sig_type=std_logic lab=GND}
C {lab_pin.sym} 780 -170 0 1 {name=l44 sig_type=std_logic lab=GND}
C {ipin.sym} -250 -300 0 0 {name=p0 lab=w[3:0]}
C {ipin.sym} -250 -270 0 0 {name=p1 lab=en}
C {iopin.sym} -250 -240 0 1 {name=p2 lab=Vb}
C {iopin.sym} -250 -210 0 1 {name=p3 lab=VDD}
C {iopin.sym} -250 -180 0 1 {name=p4 lab=Isum_e}
C {iopin.sym} -250 -150 0 1 {name=p5 lab=Isum_i}
T {DAC_sm: sign-magnitude synapse DAC (weight word w[3:0], -7..+7, as mock/dac.v).
w[2:0]: binary magnitude, branches 1:2:4 (m = 1, 2, 4 unit cells; unit: switch 0.22u/0.28u,
source 1u/8u, as DAC.sch). Men (gate en, the presynaptic spike or input pulse) passes the
branch current to Y. w[3]: sign, steers Y through Mse to Isum_e (excitatory DPI tail, w[3] = 0)
or through Msi to Isum_i (inhibitory DPI_inh tail, w[3] = 1); Mpi/Mni make sb = not w[3].
The weight is static between register writes, so the steering adds no charge per spike.} -250 120 0 0 0.3 0.3 {}
