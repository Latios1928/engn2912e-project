v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {snn_analog.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -140 0 0 {name=l0 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -150 -120 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -150 -100 0 0 {name=l2 sig_type=std_logic lab=w[31:0]}
C {lab_pin.sym} -150 -80 0 0 {name=l3 sig_type=std_logic lab=pulse[1:0]}
C {lab_pin.sym} -150 -60 0 0 {name=l4 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -150 -40 0 0 {name=l5 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -150 -20 0 0 {name=l6 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -150 0 0 0 {name=l7 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -150 20 0 0 {name=l8 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -150 40 0 0 {name=l9 sig_type=std_logic lab=VK}
C {lab_pin.sym} -150 60 0 0 {name=l10 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -150 80 0 0 {name=l11 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -150 100 0 0 {name=l12 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -150 120 0 0 {name=l13 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -150 140 0 0 {name=l14 sig_type=std_logic lab=VT}
C {lab_pin.sym} -150 160 0 0 {name=l15 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} -150 180 0 0 {name=l16 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} -150 200 0 0 {name=l17 sig_type=std_logic lab=VT_in}
C {lab_pin.sym} -150 220 0 0 {name=l18 sig_type=std_logic lab=Vthr_hid}
C {lab_pin.sym} -150 240 0 0 {name=l19 sig_type=std_logic lab=VT_hid}
C {lab_pin.sym} 150 0 0 1 {name=lsp sig_type=std_logic lab=spike[4:0]}
C {devices/code_shown.sym} -700 -300 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {devices/code_shown.sym} -700 -120 0 0 {name=HDL_INPUTS only_toplevel=true
value="
* Nets driven from Verilog: SpiceBind sets these external sources (snn_ms_tb.v).
Vw[0] w[0] 0 0 external
Vw[1] w[1] 0 0 external
Vw[2] w[2] 0 0 external
Vw[3] w[3] 0 0 external
Vw[4] w[4] 0 0 external
Vw[5] w[5] 0 0 external
Vw[6] w[6] 0 0 external
Vw[7] w[7] 0 0 external
Vw[8] w[8] 0 0 external
Vw[9] w[9] 0 0 external
Vw[10] w[10] 0 0 external
Vw[11] w[11] 0 0 external
Vw[12] w[12] 0 0 external
Vw[13] w[13] 0 0 external
Vw[14] w[14] 0 0 external
Vw[15] w[15] 0 0 external
Vw[16] w[16] 0 0 external
Vw[17] w[17] 0 0 external
Vw[18] w[18] 0 0 external
Vw[19] w[19] 0 0 external
Vw[20] w[20] 0 0 external
Vw[21] w[21] 0 0 external
Vw[22] w[22] 0 0 external
Vw[23] w[23] 0 0 external
Vw[24] w[24] 0 0 external
Vw[25] w[25] 0 0 external
Vw[26] w[26] 0 0 external
Vw[27] w[27] 0 0 external
Vw[28] w[28] 0 0 external
Vw[29] w[29] 0 0 external
Vw[30] w[30] 0 0 external
Vw[31] w[31] 0 0 external
Vpulse[0] pulse[0] 0 0 external
Vpulse[1] pulse[1] 0 0 external
"}
C {devices/code_shown.sym} 300 -300 0 0 {name=SOURCES only_toplevel=true
value="
* Supplies and biases: the XOR operating point of analog/testbenches/xor/xor_tb.sch
* (fixed voltages, tt; see analog/testbenches/xor/README.md). Per-layer DPI biases:
* inputs Vthr_in / VT_in, hidden Vthr_hid / VT_hid, output Vthr / VT_dpi (VT_inh: output inhibition).
* Parameter names start with p_: a .param with the same name as a net made ngspice
* rename that net to \{name\} on the long x1 line, leaving the biases unconnected.
.param p_vdd=3.3 p_iref=14.42n
.param p_vthr=2.70 p_vtau=0.5096 p_vtau_i=0.5096
.param p_vthr_in=2.4 p_vtau_in=0.695 p_vthr_hid=2.5 p_vtau_hid=0.655
.param p_vlk=0.48 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
Vdd VDD 0 \{p_vdd\}
Vss VSS 0 0
* DAC unit current: Iref into a diode-connected unit current source (w[0] = 15 nA)
Iref VDD Vb \{p_iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
* VT_* are source-gate voltages of the DPI tau pFET (VT = VDD - p_vtau)
Vthr Vthr 0 \{p_vthr\}
Vtau VDD VT_dpi \{p_vtau\}
Vtau_i VDD VT_inh \{p_vtau_i\}
Vthr_in Vthr_in 0 \{p_vthr_in\}
Vtau_in VDD VT_in \{p_vtau_in\}
Vthr_hid Vthr_hid 0 \{p_vthr_hid\}
Vtau_hid VDD VT_hid \{p_vtau_hid\}
Vlk Vlk VSS \{p_vlk\}
VK VK VSS \{p_vk\}
VNA VNA VSS \{p_vna\}
VKup VKup VSS \{p_vkup\}
VKdn VKdn VSS \{p_vkdn\}
VIp VIp VSS \{p_vip\}
VT VT VSS \{p_vt\}
Vamp_bias Vamp_bias VSS \{p_vamp_bias\}
* Without this the DC operating point of the sized network does not converge
.ic v(x1.VMEM_0)=0 v(x1.VMEM_1)=0 v(x1.VMEM_2)=0 v(x1.VMEM_3)=0 v(x1.VMEM_4)=0 v(spike[0])=0 v(spike[1])=0 v(spike[2])=0 v(spike[3])=0 v(spike[4])=0
"}
C {devices/code_shown.sym} 300 250 0 0 {name=TRAN only_toplevel=true
value="
* Gear integration: trap makes the DPI output current ring after each reset (entry 46)
.options method=gear
.save v(spike[0]) v(spike[1]) v(spike[2]) v(spike[3]) v(spike[4]) v(pulse[0]) v(pulse[1]) v(x1.VMEM_0) v(x1.VMEM_1) v(x1.VMEM_2) v(x1.VMEM_3) v(x1.VMEM_4)
* Runs until the Verilog testbench calls $finish. ngspice reserves memory for tstop/step
* points, so a huge bound crashes it (1 s did): keep this just above the longest run.
.tran 0.1u 100m 0 0.1u
"}
T {Mixed-signal testbench: rf and pulse generators (Verilog, snn_ms_tb.v) drive the analog
2-2-1 network snn_analog through SpiceBind. The Verilog testbench prints PASS/FAIL.
Run with make -C mixed run (see mixed/README.md).} -700 -500 0 0 0.4 0.4 {}
