v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {DAC_signed: DAC.sym with a static sign bit s. The DAC output (Y) is steered by
Mse (gate sb = not s) to Isum_e, the tail of the excitatory DPI, or by Msi (gate s)
to Isum_i, the tail of the inhibitory DPI (DPI_inh). s is a static weight bit, so the
steering adds no charge per spike; with the gate at VDD each switch is a cascode in
series with Men, like Men itself. Mpi/Mni make sb from s.} -400 300 0 0 0.3 0.3 {}
N 310 -270 310 -250 {lab=Isum_e}
N 240 -220 270 -220 {lab=sb}
N 310 -190 310 -170 {lab=Y}
N 310 -220 350 -220 {lab=GND}
N -110 -280 -110 -260 {lab=Isum_i}
N -180 -230 -150 -230 {lab=s}
N -110 -200 -110 -180 {lab=Y}
N -110 -230 -70 -230 {lab=GND}
N 100 -260 100 -240 {lab=sb}
N 30 -290 60 -290 {lab=s}
N 100 -340 100 -320 {lab=VDD}
N 100 -290 140 -290 {lab=VDD}
N 100 -200 100 -180 {lab=sb}
N 30 -150 60 -150 {lab=s}
N 100 -120 100 -100 {lab=GND}
N 100 -150 140 -150 {lab=GND}
C {DAC.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -40 0 0 {name=l1 sig_type=std_logic lab=Y}
C {lab_pin.sym} -150 -20 0 0 {name=l2 sig_type=std_logic lab=w[3:0]}
C {lab_pin.sym} -150 0 0 0 {name=l3 sig_type=std_logic lab=en}
C {lab_pin.sym} 50 -40 0 1 {name=l4 sig_type=std_logic lab=Vb}
C {symbols/nfet_03v3.sym} 290 -220 0 0 {name=Mse
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
C {lab_pin.sym} 310 -270 0 1 {name=l5 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} 240 -220 0 0 {name=l6 sig_type=std_logic lab=sb}
C {lab_pin.sym} 310 -170 0 1 {name=l7 sig_type=std_logic lab=Y}
C {lab_pin.sym} 350 -220 0 1 {name=l8 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} -130 -230 0 0 {name=Msi
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
C {lab_pin.sym} -110 -280 0 1 {name=l9 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} -180 -230 0 0 {name=l10 sig_type=std_logic lab=s}
C {lab_pin.sym} -110 -180 0 1 {name=l11 sig_type=std_logic lab=Y}
C {lab_pin.sym} -70 -230 0 1 {name=l12 sig_type=std_logic lab=GND}
C {symbols/pfet_03v3.sym} 80 -290 0 0 {name=Mpi
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
C {lab_pin.sym} 100 -240 0 1 {name=l13 sig_type=std_logic lab=sb}
C {lab_pin.sym} 30 -290 0 0 {name=l14 sig_type=std_logic lab=s}
C {lab_pin.sym} 100 -340 0 1 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 140 -290 0 1 {name=l16 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 80 -150 0 0 {name=Mni
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
C {lab_pin.sym} 100 -200 0 1 {name=l17 sig_type=std_logic lab=sb}
C {lab_pin.sym} 30 -150 0 0 {name=l18 sig_type=std_logic lab=s}
C {lab_pin.sym} 100 -100 0 1 {name=l19 sig_type=std_logic lab=GND}
C {lab_pin.sym} 140 -150 0 1 {name=l20 sig_type=std_logic lab=GND}
C {ipin.sym} -400 -200 0 0 {name=p_w lab=w[3:0]}
C {ipin.sym} -400 -170 0 0 {name=p_en lab=en}
C {ipin.sym} -400 -140 0 0 {name=p_s lab=s}
C {iopin.sym} -400 -110 0 1 {name=p_Vb lab=Vb}
C {iopin.sym} -400 -80 0 1 {name=p_VDD lab=VDD}
C {iopin.sym} -400 -50 0 1 {name=p_Isum_e lab=Isum_e}
C {iopin.sym} -400 -20 0 1 {name=p_Isum_i lab=Isum_i}
