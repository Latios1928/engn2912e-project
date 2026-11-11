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
C {lab_pin.sym} -150 -100 0 0 {name=l2 sig_type=std_logic lab=w[91:0]}
C {lab_pin.sym} -150 -80 0 0 {name=l3 sig_type=std_logic lab=pulse[2:0]}
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
C {lab_pin.sym} -150 160 0 0 {name=l15 sig_type=std_logic lab=s[4:0]}
C {lab_pin.sym} -150 180 0 0 {name=l16 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} -150 200 0 0 {name=l17 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} -150 220 0 0 {name=l18 sig_type=std_logic lab=VT_in}
C {lab_pin.sym} -150 240 0 0 {name=l19 sig_type=std_logic lab=Vthr_hid}
C {lab_pin.sym} -150 260 0 0 {name=l20 sig_type=std_logic lab=VT_hid}
C {lab_pin.sym} 150 0 0 1 {name=lsp sig_type=std_logic lab=spike[8:0]}
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
Vw[32] w[32] 0 0 external
Vw[33] w[33] 0 0 external
Vw[34] w[34] 0 0 external
Vw[35] w[35] 0 0 external
Vw[36] w[36] 0 0 external
Vw[37] w[37] 0 0 external
Vw[38] w[38] 0 0 external
Vw[39] w[39] 0 0 external
Vw[40] w[40] 0 0 external
Vw[41] w[41] 0 0 external
Vw[42] w[42] 0 0 external
Vw[43] w[43] 0 0 external
Vw[44] w[44] 0 0 external
Vw[45] w[45] 0 0 external
Vw[46] w[46] 0 0 external
Vw[47] w[47] 0 0 external
Vw[48] w[48] 0 0 external
Vw[49] w[49] 0 0 external
Vw[50] w[50] 0 0 external
Vw[51] w[51] 0 0 external
Vw[52] w[52] 0 0 external
Vw[53] w[53] 0 0 external
Vw[54] w[54] 0 0 external
Vw[55] w[55] 0 0 external
Vw[56] w[56] 0 0 external
Vw[57] w[57] 0 0 external
Vw[58] w[58] 0 0 external
Vw[59] w[59] 0 0 external
Vw[60] w[60] 0 0 external
Vw[61] w[61] 0 0 external
Vw[62] w[62] 0 0 external
Vw[63] w[63] 0 0 external
Vw[64] w[64] 0 0 external
Vw[65] w[65] 0 0 external
Vw[66] w[66] 0 0 external
Vw[67] w[67] 0 0 external
Vw[68] w[68] 0 0 external
Vw[69] w[69] 0 0 external
Vw[70] w[70] 0 0 external
Vw[71] w[71] 0 0 external
Vw[72] w[72] 0 0 external
Vw[73] w[73] 0 0 external
Vw[74] w[74] 0 0 external
Vw[75] w[75] 0 0 external
Vw[76] w[76] 0 0 external
Vw[77] w[77] 0 0 external
Vw[78] w[78] 0 0 external
Vw[79] w[79] 0 0 external
Vw[80] w[80] 0 0 external
Vw[81] w[81] 0 0 external
Vw[82] w[82] 0 0 external
Vw[83] w[83] 0 0 external
Vw[84] w[84] 0 0 external
Vw[85] w[85] 0 0 external
Vw[86] w[86] 0 0 external
Vw[87] w[87] 0 0 external
Vw[88] w[88] 0 0 external
Vw[89] w[89] 0 0 external
Vw[90] w[90] 0 0 external
Vw[91] w[91] 0 0 external
Vpulse[0] pulse[0] 0 0 external
Vpulse[1] pulse[1] 0 0 external
Vpulse[2] pulse[2] 0 0 external
"}
C {devices/code_shown.sym} 300 -300 0 0 {name=SOURCES only_toplevel=true
value="
* Supplies and biases, as in analog/neuron/DACs-DPI-neuron.sch
* Parameter names start with p_: a .param with the same name as a net made ngspice
* rename that net to \{name\} on the long x1 line, leaving the biases unconnected.
* DPIs are DPI_sized (W 0.88u, L 1.12u); biases per layer from the Monte Carlo runs in
* analog/testbenches/xor (README.md): output keeps the old gain and tau, input relays fire one
* spike per pulse, hidden layer in threshold mode, Vlk 0.48
.param p_vdd=3.3 p_vtau=0.5096 p_iref=14.42n
.param p_vthr=2.7703
.param p_vthr_in=2.4 p_vtau_in=0.72 p_vthr_hid=2.5 p_vtau_hid=0.6225
.param p_vlk=0.48 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
Vdd VDD 0 \{p_vdd\}
Vss VSS 0 0
* DAC unit current: Iref into a diode-connected unit current source (w[0] = 15 nA)
Iref VDD Vb \{p_iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
Vthr Vthr 0 \{p_vthr\}
Vtau VDD VT_dpi \{p_vtau\}
* Output inhibitory synapse (DPI_inh): same tau. The scenarios use no inhibition, so the
* sign bits s[4:0] of the hidden -> output synapses are 0 (not driven from Verilog yet).
Vtau_i VDD VT_inh \{p_vtau\}
Vthr_in Vthr_in 0 \{p_vthr_in\}
Vtau_in VDD VT_in \{p_vtau_in\}
Vthr_hid Vthr_hid 0 \{p_vthr_hid\}
Vtau_hid VDD VT_hid \{p_vtau_hid\}
Vs0 s[0] 0 0
Vs1 s[1] 0 0
Vs2 s[2] 0 0
Vs3 s[3] 0 0
Vs4 s[4] 0 0
Vlk Vlk VSS \{p_vlk\}
VK VK VSS \{p_vk\}
VNA VNA VSS \{p_vna\}
VKup VKup VSS \{p_vkup\}
VKdn VKdn VSS \{p_vkdn\}
VIp VIp VSS \{p_vip\}
VT VT VSS \{p_vt\}
Vamp_bias Vamp_bias VSS \{p_vamp_bias\}
"}
C {devices/code_shown.sym} 300 250 0 0 {name=TRAN only_toplevel=true
value="
* Start every membrane and spike output at 0 V: without this the DC operating point of the
* sized network does not converge (gmin and source stepping both fail) and the run hangs
.ic v(x1.VMEM_0)=0 v(x1.VMEM_1)=0 v(x1.VMEM_2)=0 v(x1.VMEM_3)=0 v(x1.VMEM_4)=0 v(x1.VMEM_5)=0 v(x1.VMEM_6)=0 v(x1.VMEM_7)=0 v(x1.VMEM_8)=0 v(spike[0])=0 v(spike[1])=0 v(spike[2])=0 v(spike[3])=0 v(spike[4])=0 v(spike[5])=0 v(spike[6])=0 v(spike[7])=0 v(spike[8])=0
* Gear integration: trap makes the DPI output current ring after each reset (entry 46)
.options method=gear
.save v(spike[0]) v(spike[1]) v(spike[2]) v(spike[3]) v(spike[4]) v(spike[5]) v(spike[6]) v(spike[7]) v(spike[8]) v(pulse[0]) v(pulse[1]) v(pulse[2]) v(scen[0]) v(scen[1]) v(scen[2]) v(running) v(done) v(x1.VMEM_0) v(x1.VMEM_1) v(x1.VMEM_2) v(x1.VMEM_3) v(x1.VMEM_4) v(x1.VMEM_5) v(x1.VMEM_6) v(x1.VMEM_7) v(x1.VMEM_8)
* Runs until the Verilog testbench calls $finish. ngspice reserves memory for tstop/step
* points, so a huge bound crashes it (1 s did): keep this just above the longest run.
.tran 0.1u 100m 0 0.1u
"}
T {Mixed-signal testbench: rf and pulse generators (Verilog, snn_ms_tb.v) drive the analog
3-5-1 network snn_analog through SpiceBind. The Verilog testbench prints PASS/FAIL.
Run with make -C mixed run (see mixed/README.md).} -700 -500 0 0 0.4 0.4 {}
