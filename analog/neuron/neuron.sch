v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -100 -0 -40 -0 {lab=VT}
N -100 20 -40 20 {lab=Vamp_bias}
N 0 -80 0 -50 {lab=VDD}
N -0 50 0 80 {lab=VSS}
N -180 -20 -40 -20 {lab=VMEM}
N 70 -0 160 -0 {lab=#net1}
N 160 -0 170 0 {lab=#net1}
N 170 0 170 70 {lab=#net1}
N 170 -70 170 -0 {lab=#net1}
N 210 -40 210 40 {lab=#net2}
N 210 0 210 40 {lab=#net2}
N 210 -0 340 -0 {lab=#net2}
N 340 -70 340 -0 {lab=#net2}
N 340 -70 340 -0 {lab=#net2}
N 340 -0 340 70 {lab=#net2}
N 380 -40 380 40 {lab=spike}
N 380 -40 380 -0 {lab=spike}
N 380 -0 440 -0 {lab=spike}
N 210 -70 240 -70 {lab=VDD}
N 380 -70 420 -70 {lab=VDD}
N 210 70 240 70 {lab=VSS}
N 380 70 410 70 {lab=VSS}
N 210 -120 210 -100 {lab=VDD}
N 380 -120 380 -100 {lab=#net3}
N 280 -180 280 -0 {lab=#net2}
N -180 -180 280 -180 {lab=#net2}
N -290 -180 -220 -180 {lab=VDD}
N -220 -150 -220 50 {lab=VMEM}
N -220 -20 -180 -20 {lab=VMEM}
N 440 -0 520 0 {lab=spike}
N -180 140 -140 140 {lab=spike}
N -220 50 -220 110 {lab=VMEM}
N -140 140 520 140 {lab=spike}
N 520 0 520 140 {lab=spike}
N -280 140 -220 140 {lab=VSS}
N 520 0 610 -0 {lab=spike}
N 610 60 610 110 {lab=VSS}
N 210 100 210 160 {lab=#net4}
N 380 100 380 160 {lab=#net5}
N -220 170 -220 200 {lab=#net6}
N 120 190 170 190 {lab=VIp}
N 290 190 340 190 {lab=VKdn}
N -180 -270 -140 -270 {lab=VNA}
N -220 -240 -220 -210 {lab=#net7}
N -290 -270 -220 -270 {lab=VDD}
N -220 -330 -220 -300 {lab=VDD}
N 210 190 260 190 {lab=VSS}
N 380 190 430 190 {lab=VSS}
N 210 220 210 250 {lab=VSS}
N 380 220 380 250 {lab=VSS}
N -280 230 -220 230 {lab=VSS}
N -220 260 -220 280 {lab=VSS}
N -180 230 -130 230 {lab=VK}
N -370 -20 -220 -20 {lab=VMEM}
N -370 -20 -370 -0 {lab=VMEM}
N -370 60 -370 90 {lab=VSS}
N -470 -20 -370 -20 {lab=VMEM}
N -540 -20 -470 -20 {lab=VMEM}
N -540 -20 -540 10 {lab=VMEM}
N -540 70 -540 110 {lab=VSS}
N -630 40 -580 40 {lab=Vlk}
N 380 -150 410 -150 {lab=VDD}
N 310 -150 340 -150 {lab=VKup}
N 380 -230 380 -180 {lab=VDD}
N -540 40 -490 40 {lab=VSS}
C {analog/neuron/spike_amplifier.sym} -20 0 0 0 {name=x1}
C {lab_wire.sym} -100 0 0 0 {name=p1 sig_type=std_logic lab=VT}
C {lab_wire.sym} -100 20 0 0 {name=p2 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} 0 80 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 0 -80 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 190 70 0 0 {name=M1
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
C {symbols/nfet_03v3.sym} 360 70 0 0 {name=M2
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
C {symbols/pfet_03v3.sym} 190 -70 0 0 {name=M3
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
C {symbols/pfet_03v3.sym} 360 -70 0 0 {name=M4
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
C {lab_wire.sym} 240 -70 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 420 -70 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 240 70 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 410 70 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 210 -120 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} -200 -180 0 1 {name=M5
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
C {lab_wire.sym} -290 -180 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} -200 140 0 1 {name=M6
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
C {lab_wire.sym} -280 140 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {symbols/cap_mim_analog.sym} 610 30 0 0 {name=C1
W=1e-6
L=1e-6
model=cap_mim_2f0_m3m4_noshield
spiceprefix=X
m=1}
C {lab_wire.sym} 610 110 0 0 {name=p13 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 590 0 0 0 {name=p14 sig_type=std_logic lab=spike}
C {symbols/nfet_03v3.sym} 360 190 0 0 {name=M7
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
C {symbols/nfet_03v3.sym} 190 190 0 0 {name=M8
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
C {symbols/pfet_03v3.sym} -200 -270 0 1 {name=M9
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
C {symbols/nfet_03v3.sym} -200 230 0 1 {name=M10
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
C {lab_wire.sym} -290 -270 0 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -220 -330 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 260 190 0 0 {name=p17 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 430 190 0 0 {name=p18 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 380 250 0 0 {name=p19 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 210 250 0 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -280 230 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -220 280 0 0 {name=p22 sig_type=std_logic lab=VSS}
C {symbols/cap_mim_analog.sym} -370 30 0 0 {name=C2
W=1e-6
L=1e-6
model=cap_mim_2f0_m3m4_noshield
spiceprefix=X
m=1}
C {lab_wire.sym} -370 90 0 0 {name=p23 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -290 -20 0 0 {name=p24 sig_type=std_logic lab=VMEM}
C {symbols/nfet_03v3.sym} -560 40 0 0 {name=M11
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
C {lab_wire.sym} -540 110 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -140 -270 0 0 {name=p26 sig_type=std_logic lab=VNA}
C {lab_wire.sym} -130 230 0 0 {name=p27 sig_type=std_logic lab=VK}
C {lab_wire.sym} 120 190 0 0 {name=p28 sig_type=std_logic lab=VIp}
C {lab_wire.sym} 290 190 0 0 {name=p29 sig_type=std_logic lab=VKdn}
C {symbols/pfet_03v3.sym} 360 -150 0 0 {name=M12
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
C {lab_wire.sym} 410 -150 0 0 {name=p10 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 310 -150 0 0 {name=p30 sig_type=std_logic lab=VKup}
C {lab_wire.sym} 380 -230 0 0 {name=p31 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -630 40 0 0 {name=p32 sig_type=std_logic lab=Vlk}
C {iopin.sym} -860 -150 0 0 {name=p33 lab=VSS}
C {iopin.sym} -860 -110 0 0 {name=p34 lab=VDD}
C {ipin.sym} -840 -60 0 0 {name=p35 lab=VMEM}
C {ipin.sym} -840 -20 0 0 {name=p36 lab=VNA}
C {ipin.sym} -840 30 0 0 {name=p37 lab=Vlk}
C {ipin.sym} -840 70 0 0 {name=p38 lab=VK}
C {ipin.sym} -840 110 0 0 {name=p39 lab=VIp}
C {ipin.sym} -840 150 0 0 {name=p40 lab=VKup}
C {ipin.sym} -840 190 0 0 {name=p41 lab=VKdn}
C {opin.sym} -860 300 0 0 {name=p42 lab=spike}
C {ipin.sym} -840 230 0 0 {name=p43 lab=Vamp_bias}
C {ipin.sym} -840 270 0 0 {name=p44 lab=VT}
C {lab_wire.sym} -490 40 0 0 {name=p45 sig_type=std_logic lab=VSS}
