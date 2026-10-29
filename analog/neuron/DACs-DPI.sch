v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {vdd*b32}
S {}
F {}
E {}
N -80 190 -40 190 {lab=#net1}
N -80 50 -80 190 {lab=#net1}
N -80 -100 -40 -100 {lab=#net1}
N -170 10 -130 10 {lab=VDD}
N -170 30 -130 30 {lab=Isyn}
N -500 10 -470 10 {lab=Vthr}
N -500 30 -470 30 {lab=VT}
N -70 -80 -40 -80 {lab=w00}
N -70 -60 -40 -60 {lab=w10}
N -70 -40 -40 -40 {lab=w20}
N -70 -20 -40 -20 {lab=w30}
N -70 70 -40 70 {lab=w01}
N -70 90 -40 90 {lab=w11}
N -70 110 -40 110 {lab=w21}
N -70 130 -40 130 {lab=w31}
N -170 50 -80 50 {lab=#net1}
N -80 50 -40 50 {lab=#net1}
N -70 210 -40 210 {lab=w02}
N -70 230 -40 230 {lab=w12}
N -70 250 -40 250 {lab=w22}
N -70 270 -40 270 {lab=w32}
N 260 -100 260 80 {lab=Vb}
N 260 80 260 190 {lab=Vb}
N 260 80 310 80 {lab=Vb}
N -520 -270 -520 -240 {lab=VDD}
N -520 -180 -520 -140 {lab=0}
N -130 30 -130 80 {lab=Isyn}
N -420 -270 -420 -240 {lab=VDD}
N -420 -180 -420 -140 {lab=VT}
N -80 -100 -80 50 {lab=#net1}
C {DAC.sym} 110 -60 0 0 {name=x1}
C {DAC.sym} 110 90 0 0 {name=x2}
C {DAC.sym} 110 230 0 0 {name=x3}
C {DPI.sym} -320 30 0 0 {name=x4}
C {lab_wire.sym} -130 10 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -130 30 0 0 {name=p2 sig_type=std_logic lab=Isyn}
C {lab_wire.sym} -480 10 0 0 {name=p3 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -480 30 0 0 {name=p4 sig_type=std_logic lab=VT}
C {lab_wire.sym} -50 -80 0 0 {name=p5 sig_type=std_logic lab=w00}
C {lab_wire.sym} -50 -60 0 0 {name=p6 sig_type=std_logic lab=w10}
C {lab_wire.sym} -50 -40 0 0 {name=p7 sig_type=std_logic lab=w20}
C {lab_wire.sym} -50 -20 0 0 {name=p8 sig_type=std_logic lab=w30}
C {lab_wire.sym} -50 70 0 0 {name=p9 sig_type=std_logic lab=w01}
C {lab_wire.sym} -50 90 0 0 {name=p10 sig_type=std_logic lab=w11}
C {lab_wire.sym} -50 110 0 0 {name=p11 sig_type=std_logic lab=w21}
C {lab_wire.sym} -50 130 0 0 {name=p12 sig_type=std_logic lab=w31}
C {lab_wire.sym} -50 210 0 0 {name=p13 sig_type=std_logic lab=w02}
C {lab_wire.sym} -50 230 0 0 {name=p14 sig_type=std_logic lab=w12}
C {lab_wire.sym} -50 250 0 0 {name=p15 sig_type=std_logic lab=w22}
C {lab_wire.sym} -50 270 0 0 {name=p16 sig_type=std_logic lab=w32}
C {devices/code_shown.sym} -730 160 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {lab_wire.sym} 310 80 0 0 {name=p17 sig_type=std_logic lab=Vb}
C {vsource.sym} -520 -210 0 0 {name=V1 value=3.3 savecurrent=false}
C {lab_wire.sym} -520 -270 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {gnd.sym} -520 -140 0 0 {name=l1 lab=0}
C {vsource.sym} -420 -210 0 0 {name=V2 value=0.5 savecurrent=false}
C {lab_wire.sym} -420 -270 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -420 -140 0 0 {name=p20 sig_type=std_logic lab=VT}
C {code_shown.sym} -660 270 0 0 {name=TRAN_SIM only_toplevel=false 

value="
.param vdd=3.3
.param b10=1 b20=1 b30=1
.param b01=0 b11=0 b21=0 b31=1
.param b02=0 b12=0 b22=0 b32=0

* w00 pulsed so you can see the DPI charge and decay
Vw00 w00 0 pulse(0 \{vdd\} 1m 10n 10n 2m 10m)
Vw10 w10 0 \{vdd*b10\}
Vw20 w20 0 \{vdd*b20\}
Vw30 w30 0 \{vdd*b30\}
Vw01 w01 0 \{vdd*b01\}
Vw11 w11 0 \{vdd*b11\}
Vw21 w21 0 \{vdd*b21\}
Vw31 w31 0 \{vdd*b31\}
Vw02 w02 0 \{vdd*b02\}
Vw12 w12 0 \{vdd*b12\}
Vw22 w22 0 \{vdd*b22\}
Vw32 w32 0 \{vdd*b32\}

Vthr  Vthr 0 3
Vb    Vb   0 0.5
VIsyn Isyn 0 0

.control
  save all
  tran 1u 10m
  plot i(VIsyn)
  plot v(x4.net1)
.endc

"}
