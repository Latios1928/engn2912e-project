v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 20 -180 40 -180 {lab=pre_b}
N 80 -230 80 -210 {lab=vref}
N 80 -180 100 -180 {lab=vdd}
N -100 40 -100 60 {lab=vss}
N 20 0 40 0 {lab=w0}
N 80 0 100 0 {lab=vss}
N 20 160 40 160 {lab=spike}
N 80 190 80 210 {lab=mem}
N 80 160 100 160 {lab=vss}
N 340 -180 360 -180 {lab=pre_b}
N 400 -230 400 -210 {lab=vref}
N 400 -180 420 -180 {lab=vdd}
N 260 40 260 60 {lab=vss}
N 340 0 360 0 {lab=w1}
N 400 0 420 0 {lab=vss}
N 340 160 360 160 {lab=spike}
N 400 190 400 210 {lab=mem}
N 400 160 420 160 {lab=vss}
N 660 -180 680 -180 {lab=pre_b}
N 720 -230 720 -210 {lab=vref}
N 720 -180 740 -180 {lab=vdd}
N 580 50 580 70 {lab=vss}
N 660 0 680 0 {lab=w2}
N 720 0 740 0 {lab=vss}
N 660 160 680 160 {lab=spike}
N 720 190 720 210 {lab=mem}
N 720 160 740 160 {lab=vss}
N 80 30 80 130 {lab=mid0}
N 400 30 400 130 {lab=mid1}
N 720 30 720 130 {lab=mid2}
N 80 -150 80 -30 {lab=top0}
N 400 -150 400 -30 {lab=top1}
N 720 -150 720 -30 {lab=top2}
N 580 -80 580 -10 {lab=top2}
N 580 -80 720 -80 {lab=top2}
N 260 -80 260 -20 {lab=top1}
N 260 -80 400 -80 {lab=top1}
N -100 -80 -100 -20 {lab=top0}
N -100 -80 80 -80 {lab=top0}
C {iopin.sym} -140 -320 0 0 {name=p1 lab=vdd}
C {ipin.sym} -140 -280 0 0 {name=p3 lab=vref}
C {ipin.sym} -140 -240 0 0 {name=p5 lab=spike}
C {ipin.sym} -140 -200 0 0 {name=p7 lab=w1}
C {iopin.sym} -140 -160 0 0 {name=p9 lab=mem}
C {symbols/pfet_03v3.sym} 60 -180 0 0 {name=M1
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
C {lab_pin.sym} 20 -180 0 0 {name=l10 sig_type=std_logic lab=pre_b}
C {lab_pin.sym} 80 -230 0 1 {name=l11 sig_type=std_logic lab=vref}
C {lab_pin.sym} 80 -130 0 1 {name=l12 sig_type=std_logic lab=top0}
C {lab_pin.sym} 100 -180 0 1 {name=l13 sig_type=std_logic lab=vdd}
C {capa.sym} -100 10 0 0 {name=C0
m=1
value=50f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} -100 60 0 1 {name=l15 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 60 0 0 0 {name=M4
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
C {lab_pin.sym} 20 0 0 0 {name=l16 sig_type=std_logic lab=w0}
C {lab_pin.sym} 80 80 0 1 {name=l18 sig_type=std_logic lab=mid0}
C {lab_pin.sym} 100 0 0 1 {name=l19 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 60 160 0 0 {name=M7
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
C {lab_pin.sym} 20 160 0 0 {name=l20 sig_type=std_logic lab=spike}
C {lab_pin.sym} 80 210 0 1 {name=l22 sig_type=std_logic lab=mem}
C {lab_pin.sym} 100 160 0 1 {name=l23 sig_type=std_logic lab=vss}
C {symbols/pfet_03v3.sym} 380 -180 0 0 {name=M2
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
C {lab_pin.sym} 340 -180 0 0 {name=l24 sig_type=std_logic lab=pre_b}
C {lab_pin.sym} 400 -230 0 1 {name=l25 sig_type=std_logic lab=vref}
C {lab_pin.sym} 400 -130 0 1 {name=l26 sig_type=std_logic lab=top1}
C {lab_pin.sym} 420 -180 0 1 {name=l27 sig_type=std_logic lab=vdd}
C {capa.sym} 260 10 0 0 {name=C1
m=2
value=50f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 260 60 0 1 {name=l29 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 380 0 0 0 {name=M5
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
C {lab_pin.sym} 340 0 0 0 {name=l30 sig_type=std_logic lab=w1}
C {lab_pin.sym} 400 80 0 1 {name=l32 sig_type=std_logic lab=mid1}
C {lab_pin.sym} 420 0 0 1 {name=l33 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 380 160 0 0 {name=M8
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
C {lab_pin.sym} 340 160 0 0 {name=l34 sig_type=std_logic lab=spike}
C {lab_pin.sym} 400 210 0 1 {name=l36 sig_type=std_logic lab=mem}
C {lab_pin.sym} 420 160 0 1 {name=l37 sig_type=std_logic lab=vss}
C {symbols/pfet_03v3.sym} 700 -180 0 0 {name=M3
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
C {lab_pin.sym} 660 -180 0 0 {name=l38 sig_type=std_logic lab=pre_b}
C {lab_pin.sym} 720 -230 0 1 {name=l39 sig_type=std_logic lab=vref}
C {lab_pin.sym} 720 -130 0 1 {name=l40 sig_type=std_logic lab=top2}
C {lab_pin.sym} 740 -180 0 1 {name=l41 sig_type=std_logic lab=vdd}
C {capa.sym} 580 20 0 0 {name=C2
m=4
value=50f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 580 70 0 1 {name=l43 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 700 0 0 0 {name=M6
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
C {lab_pin.sym} 660 0 0 0 {name=l44 sig_type=std_logic lab=w2}
C {lab_pin.sym} 720 80 0 1 {name=l46 sig_type=std_logic lab=mid2}
C {lab_pin.sym} 740 0 0 1 {name=l47 sig_type=std_logic lab=vss}
C {symbols/nfet_03v3.sym} 700 160 0 0 {name=M9
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
C {lab_pin.sym} 660 160 0 0 {name=l48 sig_type=std_logic lab=spike}
C {lab_pin.sym} 720 210 0 1 {name=l50 sig_type=std_logic lab=mem}
C {lab_pin.sym} 740 160 0 1 {name=l51 sig_type=std_logic lab=vss}
C {iopin.sym} -140 -300 0 0 {name=p2 lab=vss}
C {ipin.sym} -140 -260 0 0 {name=p10 lab=pre_b}
C {ipin.sym} -140 -220 0 0 {name=p4 lab=w0}
C {ipin.sym} -140 -180 0 0 {name=p8 lab=w2}
