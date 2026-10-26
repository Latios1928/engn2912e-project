v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -240 -40 -160 -40 {lab=IN}
N 140 -40 240 -40 {lab=VOUT}
N 140 -20 240 -20 {lab=VP}
N 140 -0 240 -0 {lab=VN}
N 140 20 240 20 {lab=VDD}
N 140 40 240 40 {lab=VSS}
N -860 0 -860 30 {lab=VSS}
N -920 0 -920 30 {lab=VDD}
N -800 0 -800 30 {lab=preIN}
N -920 90 -920 130 {lab=VSS}
N -860 90 -860 130 {lab=0}
N -800 90 -800 130 {lab=VSS}
N -120 90 -120 120 {lab=VP}
N -60 90 -60 120 {lab=VN}
N 0 90 0 120 {lab=VOUT}
N -120 180 -120 210 {lab=VSS}
N -60 180 -60 210 {lab=VSS}
N -0 180 -0 210 {lab=VSS}
N -730 90 -730 130 {lab=preIN}
N -730 0 -730 30 {lab=VDD}
N -190 90 -190 120 {lab=IN}
N -190 180 -190 210 {lab=VSS}
N -280 -40 -240 -40 {lab=IN}
N -420 -40 -340 -40 {lab=preIN}
C {analog/schmitt_trigger_comparator/comparator.sym} -10 0 0 0 {name=x1}
C {vsource.sym} -920 60 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {vsource.sym} -860 60 0 0 {name=V2 value=0 savecurrent=false}
C {vsource.sym} -800 60 0 0 {name=Vin value=3 savecurrent=false spice_ignore=true}
C {lab_wire.sym} -240 -40 0 0 {name=p1 sig_type=std_logic lab=IN}
C {lab_wire.sym} 240 -40 0 0 {name=p2 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 240 -20 0 0 {name=p3 sig_type=std_logic lab=VP}
C {lab_wire.sym} 240 0 0 0 {name=p4 sig_type=std_logic lab=VN}
C {lab_wire.sym} 240 20 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 240 40 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -860 0 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -920 0 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -800 0 0 0 {name=p9 sig_type=std_logic lab=preIN}
C {gnd.sym} -860 130 0 0 {name=l1 lab=0}
C {lab_wire.sym} -920 130 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -800 130 0 0 {name=p11 sig_type=std_logic lab=VSS}
C {capa.sym} -120 150 0 0 {name=C1
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {capa.sym} -60 150 0 0 {name=C2
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {capa.sym} 0 150 0 0 {name=C3
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} -120 210 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -60 210 0 0 {name=p13 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 0 210 0 0 {name=p14 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -120 90 0 0 {name=p15 sig_type=std_logic lab=VP}
C {lab_wire.sym} -60 90 0 0 {name=p16 sig_type=std_logic lab=VN}
C {lab_wire.sym} 0 90 0 0 {name=p17 sig_type=std_logic lab=VOUT}
C {devices/code_shown.sym} 410 -240 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {code_shown.sym} 420 -20 0 0 {name=DC only_toplevel=false 

spice_ignore=true 
value="

.param vdd=3.3
.control
save all 

dc Vin 0 3.3 0.01
write schmitt_trigger_comparator_tb.raw

.endc
"}
C {code_shown.sym} 420 240 0 0 {name=TRAN only_toplevel=false 


spice_ignore=false
value="

.param vdd=3.3 ipk=15p trise=100u tfall=100u per=200u
.control
save all 

tran 10n 2m
write tb_tran.raw

.endc
"}
C {isource.sym} -730 60 0 0 {name=Iin value="pulse(0 \{ipk\} 0 \{trise\} \{tfall\} 0 \{per\})" spice_ignore=false}
C {lab_wire.sym} -730 130 0 0 {name=p18 sig_type=std_logic lab=preIN}
C {lab_wire.sym} -730 0 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {capa.sym} -190 150 0 0 {name=C4
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} -190 210 0 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -190 90 0 0 {name=p21 sig_type=std_logic lab=IN}
C {ammeter.sym} -310 -40 3 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {lab_wire.sym} -420 -40 0 0 {name=p22 sig_type=std_logic lab=preIN}
