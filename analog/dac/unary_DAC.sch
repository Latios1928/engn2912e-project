v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -60 -150 -40 -150 {lab=vbias}
N 0 -200 0 -180 {lab=vdd}
N 0 -120 0 -100 {lab=n1}
N 0 -150 20 -150 {lab=vdd}
N -60 0 -40 0 {lab=t1_b}
N 0 -50 0 -30 {lab=n1}
N 0 30 0 50 {lab=sum}
N 0 0 20 0 {lab=vdd}
N 120 -150 140 -150 {lab=vbias}
N 180 -200 180 -180 {lab=vdd}
N 180 -120 180 -100 {lab=n2}
N 180 -150 200 -150 {lab=vdd}
N 120 0 140 0 {lab=t2_b}
N 180 -50 180 -30 {lab=n2}
N 180 30 180 50 {lab=sum}
N 180 0 200 0 {lab=vdd}
N 300 -150 320 -150 {lab=vbias}
N 360 -200 360 -180 {lab=vdd}
N 360 -120 360 -100 {lab=n3}
N 360 -150 380 -150 {lab=vdd}
N 300 0 320 0 {lab=t3_b}
N 360 -50 360 -30 {lab=n3}
N 360 30 360 50 {lab=sum}
N 360 0 380 0 {lab=vdd}
N 480 -150 500 -150 {lab=vbias}
N 540 -200 540 -180 {lab=vdd}
N 540 -120 540 -100 {lab=n4}
N 540 -150 560 -150 {lab=vdd}
N 480 0 500 0 {lab=t4_b}
N 540 -50 540 -30 {lab=n4}
N 540 30 540 50 {lab=sum}
N 540 0 560 0 {lab=vdd}
N 660 -150 680 -150 {lab=vbias}
N 720 -200 720 -180 {lab=vdd}
N 720 -120 720 -100 {lab=n5}
N 720 -150 740 -150 {lab=vdd}
N 660 0 680 0 {lab=t5_b}
N 720 -50 720 -30 {lab=n5}
N 720 30 720 50 {lab=sum}
N 720 0 740 0 {lab=vdd}
N 840 -150 860 -150 {lab=vbias}
N 900 -200 900 -180 {lab=vdd}
N 900 -120 900 -100 {lab=n6}
N 900 -150 920 -150 {lab=vdd}
N 840 0 860 0 {lab=t6_b}
N 900 -50 900 -30 {lab=n6}
N 900 30 900 50 {lab=sum}
N 900 0 920 0 {lab=vdd}
N 1020 -150 1040 -150 {lab=vbias}
N 1080 -200 1080 -180 {lab=vdd}
N 1080 -120 1080 -100 {lab=n7}
N 1080 -150 1100 -150 {lab=vdd}
N 1020 0 1040 0 {lab=t7_b}
N 1080 -50 1080 -30 {lab=n7}
N 1080 30 1080 50 {lab=sum}
N 1080 0 1100 0 {lab=vdd}
N 600 180 620 180 {lab=spike_b}
N 660 130 660 150 {lab=sum}
N 660 210 660 230 {lab=iout}
N 660 180 680 180 {lab=vdd}
C {iopin.sym} -140 -480 0 0 {name=p1 lab=vdd}
C {ipin.sym} -140 -455 0 0 {name=p2 lab=vbias}
C {ipin.sym} -140 -430 0 0 {name=p3 lab=spike_b}
C {ipin.sym} -140 -405 0 0 {name=p4 lab=t1_b}
C {ipin.sym} -140 -380 0 0 {name=p5 lab=t2_b}
C {ipin.sym} -140 -355 0 0 {name=p6 lab=t3_b}
C {ipin.sym} -140 -330 0 0 {name=p7 lab=t4_b}
C {ipin.sym} -140 -305 0 0 {name=p8 lab=t5_b}
C {ipin.sym} -140 -280 0 0 {name=p9 lab=t6_b}
C {ipin.sym} -140 -255 0 0 {name=p10 lab=t7_b}
C {opin.sym} -140 -230 0 0 {name=p11 lab=iout}
C {symbols/pfet_03v3.sym} -20 -150 0 0 {name=M1
L=2u
W=0.5u
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
C {lab_pin.sym} -60 -150 0 0 {name=l12 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 0 -200 0 1 {name=l13 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 0 -100 0 1 {name=l14 sig_type=std_logic lab=n1}
C {lab_pin.sym} 20 -150 0 1 {name=l15 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} -20 0 0 0 {name=M8
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
C {lab_pin.sym} -60 0 0 0 {name=l16 sig_type=std_logic lab=t1_b}
C {lab_pin.sym} 0 -50 0 1 {name=l17 sig_type=std_logic lab=n1}
C {lab_pin.sym} 0 50 0 1 {name=l18 sig_type=std_logic lab=sum}
C {lab_pin.sym} 20 0 0 1 {name=l19 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 160 -150 0 0 {name=M2
L=2u
W=0.5u
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
C {lab_pin.sym} 120 -150 0 0 {name=l20 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 180 -200 0 1 {name=l21 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 180 -100 0 1 {name=l22 sig_type=std_logic lab=n2}
C {lab_pin.sym} 200 -150 0 1 {name=l23 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 160 0 0 0 {name=M9
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
C {lab_pin.sym} 120 0 0 0 {name=l24 sig_type=std_logic lab=t2_b}
C {lab_pin.sym} 180 -50 0 1 {name=l25 sig_type=std_logic lab=n2}
C {lab_pin.sym} 180 50 0 1 {name=l26 sig_type=std_logic lab=sum}
C {lab_pin.sym} 200 0 0 1 {name=l27 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 340 -150 0 0 {name=M3
L=2u
W=0.5u
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
C {lab_pin.sym} 300 -150 0 0 {name=l28 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 360 -200 0 1 {name=l29 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 360 -100 0 1 {name=l30 sig_type=std_logic lab=n3}
C {lab_pin.sym} 380 -150 0 1 {name=l31 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 340 0 0 0 {name=M10
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
C {lab_pin.sym} 300 0 0 0 {name=l32 sig_type=std_logic lab=t3_b}
C {lab_pin.sym} 360 -50 0 1 {name=l33 sig_type=std_logic lab=n3}
C {lab_pin.sym} 360 50 0 1 {name=l34 sig_type=std_logic lab=sum}
C {lab_pin.sym} 380 0 0 1 {name=l35 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 520 -150 0 0 {name=M4
L=2u
W=0.5u
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
C {lab_pin.sym} 480 -150 0 0 {name=l36 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 540 -200 0 1 {name=l37 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 540 -100 0 1 {name=l38 sig_type=std_logic lab=n4}
C {lab_pin.sym} 560 -150 0 1 {name=l39 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 520 0 0 0 {name=M11
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
C {lab_pin.sym} 480 0 0 0 {name=l40 sig_type=std_logic lab=t4_b}
C {lab_pin.sym} 540 -50 0 1 {name=l41 sig_type=std_logic lab=n4}
C {lab_pin.sym} 540 50 0 1 {name=l42 sig_type=std_logic lab=sum}
C {lab_pin.sym} 560 0 0 1 {name=l43 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 700 -150 0 0 {name=M5
L=2u
W=0.5u
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
C {lab_pin.sym} 660 -150 0 0 {name=l44 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 720 -200 0 1 {name=l45 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 720 -100 0 1 {name=l46 sig_type=std_logic lab=n5}
C {lab_pin.sym} 740 -150 0 1 {name=l47 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 700 0 0 0 {name=M12
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
C {lab_pin.sym} 660 0 0 0 {name=l48 sig_type=std_logic lab=t5_b}
C {lab_pin.sym} 720 -50 0 1 {name=l49 sig_type=std_logic lab=n5}
C {lab_pin.sym} 720 50 0 1 {name=l50 sig_type=std_logic lab=sum}
C {lab_pin.sym} 740 0 0 1 {name=l51 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 880 -150 0 0 {name=M6
L=2u
W=0.5u
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
C {lab_pin.sym} 840 -150 0 0 {name=l52 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 900 -200 0 1 {name=l53 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 900 -100 0 1 {name=l54 sig_type=std_logic lab=n6}
C {lab_pin.sym} 920 -150 0 1 {name=l55 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 880 0 0 0 {name=M13
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
C {lab_pin.sym} 840 0 0 0 {name=l56 sig_type=std_logic lab=t6_b}
C {lab_pin.sym} 900 -50 0 1 {name=l57 sig_type=std_logic lab=n6}
C {lab_pin.sym} 900 50 0 1 {name=l58 sig_type=std_logic lab=sum}
C {lab_pin.sym} 920 0 0 1 {name=l59 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 1060 -150 0 0 {name=M7
L=2u
W=0.5u
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
C {lab_pin.sym} 1020 -150 0 0 {name=l60 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 1080 -200 0 1 {name=l61 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1080 -100 0 1 {name=l62 sig_type=std_logic lab=n7}
C {lab_pin.sym} 1100 -150 0 1 {name=l63 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 1060 0 0 0 {name=M14
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
C {lab_pin.sym} 1020 0 0 0 {name=l64 sig_type=std_logic lab=t7_b}
C {lab_pin.sym} 1080 -50 0 1 {name=l65 sig_type=std_logic lab=n7}
C {lab_pin.sym} 1080 50 0 1 {name=l66 sig_type=std_logic lab=sum}
C {lab_pin.sym} 1100 0 0 1 {name=l67 sig_type=std_logic lab=vdd}
C {symbols/pfet_03v3.sym} 640 180 0 0 {name=M15
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
C {lab_pin.sym} 600 180 0 0 {name=l68 sig_type=std_logic lab=spike_b}
C {lab_pin.sym} 660 130 0 1 {name=l69 sig_type=std_logic lab=sum}
C {lab_pin.sym} 660 230 0 1 {name=l70 sig_type=std_logic lab=iout}
C {lab_pin.sym} 680 180 0 1 {name=l71 sig_type=std_logic lab=vdd}
