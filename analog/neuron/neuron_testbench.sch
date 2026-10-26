v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -600 -130 -600 -100 {lab=VSS}
N -660 -130 -660 -100 {lab=VDD}
N -660 -40 -660 0 {lab=VSS}
N -600 -40 -600 0 {lab=0}
N -470 -40 -470 0 {lab=preIN}
N -470 -130 -470 -100 {lab=VDD}
N 140 30 230 30 {lab=MEM}
N 140 50 230 50 {lab=reset_bias}
N 140 10 230 10 {lab=VOUT}
N 140 -10 230 -10 {lab=VN}
N 140 -30 220 -30 {lab=VP}
N 220 -30 230 -30 {lab=VP}
N 140 -50 230 -50 {lab=VSS}
N 140 -70 230 -70 {lab=VDD}
N -740 -130 -740 -100 {lab=reset_bias}
N -740 -40 -740 0 {lab=VSS}
N -470 60 -470 90 {lab=MEM}
C {neuron.sym} -10 -10 0 0 {name=x1}
C {vsource.sym} -660 -70 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {vsource.sym} -600 -70 0 0 {name=V2 value=0 savecurrent=false}
C {lab_wire.sym} -600 -130 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -660 -130 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {gnd.sym} -600 0 0 0 {name=l1 lab=0}
C {lab_wire.sym} -660 0 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {isource.sym} -470 -70 0 0 {name=Iin value="pulse(0 \{ipk\} \{delay\} \{trise\} \{tfall\} \{pulse_width\} \{per\})" spice_ignore=false}
C {lab_wire.sym} -470 0 0 0 {name=p18 sig_type=std_logic lab=preIN}
C {lab_wire.sym} -470 -130 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 230 -70 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 230 -50 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 230 -30 0 0 {name=p3 sig_type=std_logic lab=VP}
C {lab_wire.sym} 230 -10 0 0 {name=p4 sig_type=std_logic lab=VN}
C {lab_wire.sym} 230 10 0 0 {name=p5 sig_type=std_logic lab=VOUT}
C {lab_wire.sym} 230 30 0 0 {name=p6 sig_type=std_logic lab=MEM}
C {lab_wire.sym} 230 50 0 0 {name=p12 sig_type=std_logic lab=reset_bias}
C {vsource.sym} -740 -70 0 0 {name=Vbias value=\{reset_bias\} savecurrent=false}
C {lab_wire.sym} -740 -130 0 0 {name=p13 sig_type=std_logic lab=reset_bias}
C {lab_wire.sym} -740 0 0 0 {name=p14 sig_type=std_logic lab=VSS}
C {devices/code_shown.sym} -1310 -140 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {code_shown.sym} -1310 60 0 0 {name=TRAN_SIM only_toplevel=false 

value="
.param vdd=3.3 reset_bias=0.2 ipk=20n delay=100u trise=1u tfall=1u pulse_width=50u per=1m
.control
	save all 
	tran 1u 10m 
	write /foss/designs/engn2912e-project/analog/neuron/neuron_tb.raw
	wrdata /foss/designs/engn2912e-project/analog/neuron/neuron_tb.txt v(mem) v(vout) i(vmem)

	plot v(mem) v(vout) title 'Membrane and spike' ylabel 'V'
	plot i(VMEM)
.endc
"}
C {ammeter.sym} -470 30 0 0 {name=VMEM savecurrent=true spice_ignore=0}
C {lab_wire.sym} -470 90 0 0 {name=p9 sig_type=std_logic lab=MEM}
