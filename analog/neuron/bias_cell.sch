v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {symbols/nfet_03v3.sym} 0 400 0 0 {name=MN0
L=8u
W=10u
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
C {lab_pin.sym} 20 370 0 1 {name=l1 sig_type=std_logic lab=Iref}
C {lab_pin.sym} -20 400 0 0 {name=l2 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 20 430 0 1 {name=l3 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 20 400 0 1 {name=l4 sig_type=std_logic lab=VSS}
C {symbols/nfet_03v3.sym} 200 400 0 0 {name=MNP
L=8u
W=10u
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
C {lab_pin.sym} 220 370 0 1 {name=l5 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 180 400 0 0 {name=l6 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 220 430 0 1 {name=l7 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 220 400 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 400 0 0 0 {name=MP0
L=8u
W=10u
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
C {lab_pin.sym} 420 30 0 1 {name=l9 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 380 0 0 0 {name=l10 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 420 -30 0 1 {name=l11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 420 0 0 1 {name=l12 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} 600 0 0 0 {name=MO_Vb
L=8u
W=1.435u
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
C {lab_pin.sym} 620 30 0 1 {name=l13 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 580 0 0 0 {name=l14 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 620 -30 0 1 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 620 0 0 1 {name=l16 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 600 400 0 0 {name=MR_Vb
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
C {lab_pin.sym} 620 370 0 1 {name=l17 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 580 400 0 0 {name=l18 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 620 430 0 1 {name=l19 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 620 400 0 1 {name=l20 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 800 0 0 0 {name=MO_Vlk
L=16u
W=0.84u
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
C {lab_pin.sym} 820 30 0 1 {name=l21 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 780 0 0 0 {name=l22 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 820 -30 0 1 {name=l23 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 820 0 0 1 {name=l24 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 800 400 0 0 {name=MR_Vlk
L=1u
W=1u
nf=1
m=8
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 820 370 0 1 {name=l25 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 780 400 0 0 {name=l26 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 820 430 0 1 {name=l27 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 820 400 0 1 {name=l28 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1000 0 0 0 {name=MO_VKdn
L=8u
W=12.94u
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
C {lab_pin.sym} 1020 30 0 1 {name=l29 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 980 0 0 0 {name=l30 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 1020 -30 0 1 {name=l31 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1020 0 0 1 {name=l32 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1000 400 0 0 {name=MR_VKdn
L=1u
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
C {lab_pin.sym} 1020 370 0 1 {name=l33 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 980 400 0 0 {name=l34 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 1020 430 0 1 {name=l35 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1020 400 0 1 {name=l36 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1200 0 0 0 {name=MO_VIp
L=8u
W=2.335u
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
C {lab_pin.sym} 1220 30 0 1 {name=l37 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 1180 0 0 0 {name=l38 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 1220 -30 0 1 {name=l39 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1220 0 0 1 {name=l40 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1200 400 0 0 {name=MR_VIp
L=1u
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
C {lab_pin.sym} 1220 370 0 1 {name=l41 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 1180 400 0 0 {name=l42 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 1220 430 0 1 {name=l43 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1220 400 0 1 {name=l44 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1400 0 0 0 {name=MO_Vamp_bias
L=8u
W=9.14u
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
C {lab_pin.sym} 1420 30 0 1 {name=l45 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 1380 0 0 0 {name=l46 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 1420 -30 0 1 {name=l47 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1420 0 0 1 {name=l48 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1400 400 0 0 {name=MR_Vamp_bias
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
C {lab_pin.sym} 1420 370 0 1 {name=l49 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 1380 400 0 0 {name=l50 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 1420 430 0 1 {name=l51 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1420 400 0 1 {name=l52 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1600 0 0 0 {name=MO_VK
L=8u
W=10.45u
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
C {lab_pin.sym} 1620 30 0 1 {name=l53 sig_type=std_logic lab=VK}
C {lab_pin.sym} 1580 0 0 0 {name=l54 sig_type=std_logic lab=vgp}
C {lab_pin.sym} 1620 -30 0 1 {name=l55 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1620 0 0 1 {name=l56 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1600 400 0 0 {name=MR_VK
L=40u
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
C {lab_pin.sym} 1620 370 0 1 {name=l57 sig_type=std_logic lab=VK}
C {lab_pin.sym} 1580 400 0 0 {name=l58 sig_type=std_logic lab=VK}
C {lab_pin.sym} 1620 430 0 1 {name=l59 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1620 400 0 1 {name=l60 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 1800 0 0 0 {name=MR_VNA
L=20u
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
C {lab_pin.sym} 1820 30 0 1 {name=l61 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 1780 0 0 0 {name=l62 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 1820 -30 0 1 {name=l63 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1820 0 0 1 {name=l64 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 1800 400 0 0 {name=MO_VNA
L=8u
W=5.755u
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
C {lab_pin.sym} 1820 370 0 1 {name=l65 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 1780 400 0 0 {name=l66 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 1820 430 0 1 {name=l67 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1820 400 0 1 {name=l68 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 2000 0 0 0 {name=MR_VKup
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
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2020 30 0 1 {name=l69 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 1980 0 0 0 {name=l70 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 2020 -30 0 1 {name=l71 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2020 0 0 1 {name=l72 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2000 400 0 0 {name=MO_VKup
L=8u
W=6.005u
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
C {lab_pin.sym} 2020 370 0 1 {name=l73 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 1980 400 0 0 {name=l74 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 2020 430 0 1 {name=l75 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2020 400 0 1 {name=l76 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 2200 0 0 0 {name=MR_Vthr
L=0.28u
W=0.22u
nf=1
m=32
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2220 30 0 1 {name=l77 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 2180 0 0 0 {name=l78 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 2220 -30 0 1 {name=l79 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2220 0 0 1 {name=l80 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2200 400 0 0 {name=MO_Vthr
L=32u
W=0.905u
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
C {lab_pin.sym} 2220 370 0 1 {name=l81 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 2180 400 0 0 {name=l82 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 2220 430 0 1 {name=l83 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2220 400 0 1 {name=l84 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 2400 0 0 0 {name=MR_VT_dpi
L=0.28u
W=0.22u
nf=1
m=32
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2420 30 0 1 {name=l85 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 2380 0 0 0 {name=l86 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 2420 -30 0 1 {name=l87 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2420 0 0 1 {name=l88 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2400 400 0 0 {name=MO_VT_dpi
L=32u
W=1.165u
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
C {lab_pin.sym} 2420 370 0 1 {name=l89 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 2380 400 0 0 {name=l90 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 2420 430 0 1 {name=l91 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2420 400 0 1 {name=l92 sig_type=std_logic lab=VSS}
C {symbols/pfet_03v3.sym} 2600 0 0 0 {name=MR_VT_inh
L=1.12u
W=0.88u
nf=1
m=16
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 2620 30 0 1 {name=l93 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} 2580 0 0 0 {name=l94 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} 2620 -30 0 1 {name=l95 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2620 0 0 1 {name=l96 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 2600 400 0 0 {name=MO_VT_inh
L=32u
W=0.625u
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
C {lab_pin.sym} 2620 370 0 1 {name=l97 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} 2580 400 0 0 {name=l98 sig_type=std_logic lab=Iref}
C {lab_pin.sym} 2620 430 0 1 {name=l99 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2620 400 0 1 {name=l100 sig_type=std_logic lab=VSS}
C {iopin.sym} -400 -300 0 1 {name=p_VDD lab=VDD}
C {iopin.sym} -400 -270 0 1 {name=p_VSS lab=VSS}
C {iopin.sym} -400 -240 0 1 {name=p_Iref lab=Iref}
C {opin.sym} -300 -210 0 0 {name=p_Vb lab=Vb}
C {opin.sym} -300 -180 0 0 {name=p_Vlk lab=Vlk}
C {opin.sym} -300 -150 0 0 {name=p_VKdn lab=VKdn}
C {opin.sym} -300 -120 0 0 {name=p_VIp lab=VIp}
C {opin.sym} -300 -90 0 0 {name=p_Vamp_bias lab=Vamp_bias}
C {opin.sym} -300 -60 0 0 {name=p_VK lab=VK}
C {opin.sym} -300 -30 0 0 {name=p_VNA lab=VNA}
C {opin.sym} -300 0 0 0 {name=p_VKup lab=VKup}
C {opin.sym} -300 30 0 0 {name=p_Vthr lab=Vthr}
C {opin.sym} -300 60 0 0 {name=p_VT_dpi lab=VT_dpi}
C {opin.sym} -300 90 0 0 {name=p_VT_inh lab=VT_inh}
T {bias_cell: current-mode bias generator for the SNN (one external reference current, fixed ratios).
Iref (100 nA, into the pin) sets the NMOS master MN0; MNP/MP0 make the PMOS master. Each bias is a mirror
output into a diode-connected replica of the transistor it drives, so the bias voltage follows the process
corner and temperature and the bias current stays fixed. Replicas: exact copies of the target device (m = parallel
copies), except VK / VNA / VKup (strong inversion), which use long narrow replicas to save current.
VT (neuron threshold) is not generated here: it is a comparison voltage, not a bias current.
Sized at tt 27 C to the tuned voltages (analog/testbenches/bias/bias_design.py); about 0.72 uA from VDD incl. Iref.} -400 -500 0 0 0.3 0.3 {}
