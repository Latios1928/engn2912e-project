v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -240 -40 -160 -40 {lab=VIN}
N 140 -40 240 -40 {lab=VOUT}
N 140 -20 240 -20 {lab=VP}
N 140 -0 240 -0 {lab=VN}
N 140 20 240 20 {lab=VDD}
N 140 40 240 40 {lab=VSS}
N -410 0 -410 30 {lab=VSS}
N -470 0 -470 30 {lab=VDD}
N -350 0 -350 30 {lab=VIN}
N -470 90 -470 130 {lab=VSS}
N -410 90 -410 130 {lab=0}
N -350 90 -350 130 {lab=VSS}
N -120 90 -120 120 {lab=VP}
N -60 90 -60 120 {lab=VN}
N 0 90 0 120 {lab=VOUT}
N -120 180 -120 210 {lab=VSS}
N -60 180 -60 210 {lab=VSS}
N -0 180 -0 210 {lab=VSS}
C {analog/schmitt_trigger_comparator/comparator.sym} -10 0 0 0 {name=x1}
C {vsource.sym} -470 60 0 0 {name=V1 value=3.3 savecurrent=false}
C {vsource.sym} -410 60 0 0 {name=V2 value=0 savecurrent=false}
C {vsource.sym} -350 60 0 0 {name=V3 value=3 savecurrent=false}
C {lab_wire.sym} -240 -40 0 0 {name=p1 sig_type=std_logic lab=VIN}
C {lab_wire.sym} 240 -40 0 0 {name=p2 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 240 -20 0 0 {name=p3 sig_type=std_logic lab=VP}
C {lab_wire.sym} 240 0 0 0 {name=p4 sig_type=std_logic lab=VN}
C {lab_wire.sym} 240 20 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 240 40 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -410 0 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -470 0 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -350 0 0 0 {name=p9 sig_type=std_logic lab=VIN}
C {gnd.sym} -410 130 0 0 {name=l1 lab=0}
C {lab_wire.sym} -470 130 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -350 130 0 0 {name=p11 sig_type=std_logic lab=VSS}
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
C {code_shown.sym} 420 -20 0 0 {name=s1 only_toplevel=false value="
** DELAY 0x0001 << [0xE -> 0xF -> 0xE]

.control
save all 

.endc
"}
