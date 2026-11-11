v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {DPI_sized.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -20 0 0 {name=l1 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -150 0 0 0 {name=l2 sig_type=std_logic lab=VT}
C {lab_pin.sym} -150 20 0 0 {name=l3 sig_type=std_logic lab=Isum}
C {lab_pin.sym} 150 -20 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 0 0 1 {name=l5 sig_type=std_logic lab=Im}
C {symbols/nfet_03v3.sym} 300 160 0 0 {name=Mi1
L=8u
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
N 320 130 320 110 {lab=Im}
C {lab_pin.sym} 320 110 0 1 {name=l6 sig_type=std_logic lab=Im}
N 280 160 250 160 {lab=Im}
C {lab_pin.sym} 250 160 0 0 {name=l7 sig_type=std_logic lab=Im}
N 320 190 320 210 {lab=GND}
C {lab_pin.sym} 320 210 0 1 {name=l8 sig_type=std_logic lab=GND}
N 320 160 360 160 {lab=GND}
C {lab_pin.sym} 360 160 0 1 {name=l9 sig_type=std_logic lab=GND}
C {symbols/nfet_03v3.sym} 520 160 0 0 {name=Mi2
L=8u
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
N 540 130 540 110 {lab=Iout}
C {lab_pin.sym} 540 110 0 1 {name=l10 sig_type=std_logic lab=Iout}
N 500 160 470 160 {lab=Im}
C {lab_pin.sym} 470 160 0 0 {name=l11 sig_type=std_logic lab=Im}
N 540 190 540 210 {lab=GND}
C {lab_pin.sym} 540 210 0 1 {name=l12 sig_type=std_logic lab=GND}
N 540 160 580 160 {lab=GND}
C {lab_pin.sym} 580 160 0 1 {name=l13 sig_type=std_logic lab=GND}
C {iopin.sym} -400 -200 0 1 {name=p_VDD lab=VDD}
C {ipin.sym} -400 -170 0 0 {name=p_Vthr lab=Vthr}
C {ipin.sym} -400 -140 0 0 {name=p_VT lab=VT}
C {opin.sym} -400 -110 2 0 {name=p_Isum lab=Isum}
C {iopin.sym} -400 -80 0 1 {name=p_Iout lab=Iout}
T {DPI_inh: inhibitory synapse. DPI_sized.sym (same DPI as the excitatory synapses), but its output current Im goes into the
nFET mirror Mi1/Mi2 (2u/8u, 1:1), so Iout sinks it from the membrane instead of sourcing it.
Same Isum input as DPI.sym; drive it from the Isum_i outputs of DAC_signed.
Iout must stay above about 0.1 V for Mi2 to stay saturated, so inhibition cannot pull
the membrane below ground.} -400 300 0 0 0.3 0.3 {}
