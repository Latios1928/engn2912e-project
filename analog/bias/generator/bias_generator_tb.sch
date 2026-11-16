v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_generator testbench: bias_master -> trim_steer (Apple US 10,938,380 Fig. 2) -> bias_cell (analog/bias/generator/README.md)} -900 -520 0 0 0.45 0.45 {}
T {Set the trim code with b3..b0 and cal in the PARAMS block (code 9 = 1001 = nominal). Imon is held at 1.65 V, as on the tester.} -900 -480 0 0 0.3 0.3 {}
C {analog/bias/generator/bias_generator.sym} 0 0 0 0 {name=xgen}
C {vsource.sym} -820 300 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {gnd.sym} -820 330 0 0 {name=g1 lab=0}
N -820 270 -820 -260 {}
N -820 -260 -300 -260 {}
C {ammeter.sym} -300 -230 0 0 {name=VIdd savecurrent=true spice_ignore=0}
N -300 -200 -300 -100 {}
N -300 -100 -120 -100 {}
C {lab_wire.sym} -300.0 -150.0 0 0 {name=w2 sig_type=std_logic lab=VDD}
C {gnd.sym} -120 -80 1 0 {name=g3 lab=0}
C {vsource.sym} -720 300 0 0 {name=Vtr3 value='vdd*b3' savecurrent=false}
C {gnd.sym} -720 330 0 0 {name=g4 lab=0}
N -720 270 -720 -60 {}
N -720 -60 -120 -60 {}
C {vsource.sym} -630 300 0 0 {name=Vtr2 value='vdd*b2' savecurrent=false}
C {gnd.sym} -630 330 0 0 {name=g5 lab=0}
N -630 270 -630 -40 {}
N -630 -40 -120 -40 {}
C {vsource.sym} -540 300 0 0 {name=Vtr1 value='vdd*b1' savecurrent=false}
C {gnd.sym} -540 330 0 0 {name=g6 lab=0}
N -540 270 -540 -20 {}
N -540 -20 -120 -20 {}
C {vsource.sym} -450 300 0 0 {name=Vtr0 value='vdd*b0' savecurrent=false}
C {gnd.sym} -450 330 0 0 {name=g7 lab=0}
N -450 270 -450 0 {}
N -450 0 -120 0 {}
C {vsource.sym} -360 300 0 0 {name=Vcal value='vdd*cal' savecurrent=false}
C {gnd.sym} -360 330 0 0 {name=g8 lab=0}
N -360 270 -360 20 {}
N -360 20 -120 20 {}
C {vsource.sym} -270 300 0 0 {name=Vmon value=1.65 savecurrent=true}
C {gnd.sym} -270 330 0 0 {name=g9 lab=0}
N -270 270 -270 40 {}
N -270 40 -120 40 {}
N 120 -100 220 -100 {}
C {lab_wire.sym} 170.0 -100.0 0 0 {name=w10 sig_type=std_logic lab=Vb}
N 120 -80 220 -80 {}
C {lab_wire.sym} 170.0 -80.0 0 0 {name=w11 sig_type=std_logic lab=Vlk}
N 120 -60 220 -60 {}
C {lab_wire.sym} 170.0 -60.0 0 0 {name=w12 sig_type=std_logic lab=VKdn}
N 120 -40 220 -40 {}
C {lab_wire.sym} 170.0 -40.0 0 0 {name=w13 sig_type=std_logic lab=VIp}
N 120 -20 220 -20 {}
C {lab_wire.sym} 170.0 -20.0 0 0 {name=w14 sig_type=std_logic lab=Vamp_bias}
N 120 0 220 0 {}
C {lab_wire.sym} 170.0 0.0 0 0 {name=w15 sig_type=std_logic lab=VK}
N 120 20 220 20 {}
C {lab_wire.sym} 170.0 20.0 0 0 {name=w16 sig_type=std_logic lab=VNA}
N 120 40 220 40 {}
C {lab_wire.sym} 170.0 40.0 0 0 {name=w17 sig_type=std_logic lab=VKup}
N 120 60 220 60 {}
C {lab_wire.sym} 170.0 60.0 0 0 {name=w18 sig_type=std_logic lab=Vthr}
N 120 80 220 80 {}
C {lab_wire.sym} 170.0 80.0 0 0 {name=w19 sig_type=std_logic lab=VT_dpi}
N 120 100 220 100 {}
C {lab_wire.sym} 170.0 100.0 0 0 {name=w20 sig_type=std_logic lab=VT_inh}
C {devices/code_shown.sym} -900 -420 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {devices/code_shown.sym} 500 -420 0 0 {name=PARAMS only_toplevel=true
value="
* trim code 9 = 1001 (nominal); ss chips trim to about 14, ff to about 4
* cal = 1 while trimming (aux path on: glitch-free code changes), 0 afterwards
.param vdd=3.3 b3=1 b2=0 b1=0 b0=1 cal=0
.temp 27
"}
C {devices/code_shown.sym} 500 260 0 0 {name=SIM only_toplevel=true
value="
.control
save all
op
let imon_nA = -i(Vmon)*1e9
let supply_uA = i(VIdd)*1e6
print imon_nA supply_uA
print v(Vb) v(Vlk) v(VKdn) v(VIp) v(Vamp_bias) v(VK) v(VNA) v(VKup) v(Vthr) v(VT_dpi) v(VT_inh)
dc V1 2.97 3.63 0.03
plot v(Vb) v(Vlk) v(VKdn) v(VIp)
.endc
"}
