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
N -470 60 -470 90 {lab=VMEM}
N 290 -100 370 -100 {lab=VDD}
N 290 -120 370 -120 {lab=VSS}
N 290 -80 370 -80 {lab=spike}
N -80 40 -10 40 {lab=VT}
N -80 20 -10 20 {lab=Vamp_bias}
N -80 0 -10 -0 {lab=VKdn}
N -80 -20 -10 -20 {lab=VKup}
N -80 -40 -10 -40 {lab=VIp}
N -80 -60 -10 -60 {lab=VK}
N -80 -80 -10 -80 {lab=Vlk}
N -80 -100 -10 -100 {lab=VNA}
N -80 -120 -10 -120 {lab=VMEM}
N -600 -500 -600 -470 {lab=VK}
N -660 -500 -660 -470 {lab=Vlk}
N -660 -410 -660 -370 {lab=VSS}
N -600 -410 -600 -370 {lab=VSS}
N -740 -500 -740 -470 {lab=VNA}
N -740 -410 -740 -370 {lab=VSS}
N -600 -320 -600 -290 {lab=VKdn}
N -660 -320 -660 -290 {lab=VKup}
N -660 -230 -660 -190 {lab=VSS}
N -600 -230 -600 -190 {lab=VSS}
N -740 -320 -740 -290 {lab=VIp}
N -740 -230 -740 -190 {lab=VSS}
N -410 -320 -410 -290 {lab=VT}
N -410 -230 -410 -190 {lab=VSS}
N -490 -320 -490 -290 {lab=Vamp_bias}
N -490 -230 -490 -190 {lab=VSS}
C {vsource.sym} -660 -70 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {vsource.sym} -600 -70 0 0 {name=V2 value=0 savecurrent=false}
C {lab_wire.sym} -600 -130 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -660 -130 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {gnd.sym} -600 0 0 0 {name=l1 lab=0}
C {lab_wire.sym} -660 0 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {isource.sym} -470 -70 0 0 {name=Iin value=\{iin\} spice_ignore=false}
C {lab_wire.sym} -470 0 0 0 {name=p18 sig_type=std_logic lab=preIN}
C {lab_wire.sym} -470 -130 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {devices/code_shown.sym} -1310 -140 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -1320 230 0 0 {name=TRAN_SIM only_toplevel=false

value="
* Biases for 5 kHz at iin = 5 nA DC (typical corner, 27 C)
.param vdd=3.3 iin=5n
.param Vlk=0.420 Vamp_bias=0.535 VIp=0.573 VNA=2.0 VKup=2.277 VK=1.1 VKdn=0.573 VT=1.0
.ic v(VMEM)=0 v(spike)=0
.control
	save all
	tran 20n 2.4m 0 20n uic
	meas tran t3 when v(spike)=1.65 rise=3
	meas tran t11 when v(spike)=1.65 rise=11
	let f_spike = 8/(t11-t3)
	print f_spike
	write /foss/designs/engn2912e-project/analog/neuron/neuron_5khz_tb.raw
	plot v(VMEM) v(spike) title 'Membrane and spike' ylabel 'V'
.endc
"}
C {ammeter.sym} -470 30 0 0 {name=VMEM savecurrent=true spice_ignore=0}
C {lab_wire.sym} -470 90 0 0 {name=p9 sig_type=std_logic lab=VMEM}
C {analog/neuron/neuron_5khz.sym} 140 -40 0 0 {name=x1}
C {lab_wire.sym} 370 -120 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 370 -100 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 370 -80 0 0 {name=p3 sig_type=std_logic lab=spike}
C {lab_wire.sym} -80 -120 0 0 {name=p4 sig_type=std_logic lab=VMEM}
C {lab_wire.sym} -80 -100 0 0 {name=p5 sig_type=std_logic lab=VNA}
C {lab_wire.sym} -80 -80 0 0 {name=p6 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} -80 -60 0 0 {name=p11 sig_type=std_logic lab=VK}
C {lab_wire.sym} -80 -40 0 0 {name=p12 sig_type=std_logic lab=VIp}
C {lab_wire.sym} -80 -20 0 0 {name=p15 sig_type=std_logic lab=VKup}
C {lab_wire.sym} -80 0 0 0 {name=p16 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} -80 20 0 0 {name=p17 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} -80 40 0 0 {name=p20 sig_type=std_logic lab=VT}
C {vsource.sym} -660 -440 0 0 {name=Vlk value=\{Vlk\} savecurrent=false}
C {vsource.sym} -600 -440 0 0 {name=VK value=\{VK\} savecurrent=false}
C {lab_wire.sym} -600 -500 0 0 {name=p21 sig_type=std_logic lab=VK}
C {lab_wire.sym} -660 -500 0 0 {name=p22 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} -660 -370 0 0 {name=p23 sig_type=std_logic lab=VSS}
C {vsource.sym} -740 -440 0 0 {name=VNA value=\{VNA\} savecurrent=false}
C {lab_wire.sym} -740 -500 0 0 {name=p24 sig_type=std_logic lab=VNA}
C {lab_wire.sym} -740 -370 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {vsource.sym} -660 -260 0 0 {name=VKup value=\{VKup\} savecurrent=false}
C {vsource.sym} -600 -260 0 0 {name=VKdn value=\{VKdn\} savecurrent=false}
C {lab_wire.sym} -600 -320 0 0 {name=p26 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} -660 -320 0 0 {name=p27 sig_type=std_logic lab=VKup}
C {lab_wire.sym} -660 -190 0 0 {name=p28 sig_type=std_logic lab=VSS}
C {vsource.sym} -740 -260 0 0 {name=VIp value=\{VIp\} savecurrent=false}
C {lab_wire.sym} -740 -320 0 0 {name=p29 sig_type=std_logic lab=VIp}
C {lab_wire.sym} -740 -190 0 0 {name=p30 sig_type=std_logic lab=VSS}
C {vsource.sym} -410 -260 0 0 {name=VT value=\{VT\} savecurrent=false}
C {lab_wire.sym} -410 -320 0 0 {name=p32 sig_type=std_logic lab=VT}
C {lab_wire.sym} -410 -190 0 0 {name=p33 sig_type=std_logic lab=VSS}
C {vsource.sym} -490 -260 0 0 {name=Vamp_bias value=\{Vamp_bias\} savecurrent=false}
C {lab_wire.sym} -490 -320 0 0 {name=p34 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} -490 -190 0 0 {name=p35 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -600 -370 0 0 {name=p36 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -600 -190 0 0 {name=p37 sig_type=std_logic lab=VSS}
