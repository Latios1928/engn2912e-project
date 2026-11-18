v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {snn_ms_tb_v2: SPICE side of the addr4_trim mixed-signal run. x1 is the 2-2-1 network
(analog/snn/snn_analog.sch, as in mixed/snn_ms_tb.sch). Its biases come from x2, the bias cell
(analog/neuron/bias_cell.sch, the one in SNN.gds), instead of fixed voltage sources. The bias
cell's reference current Iref comes from the Verilog-A model trim_iref.va, set by the trim bits
from Verilog (trim law of Luz's analog/bias/bias_gen.py).
Run with the Makefile, which compiles trim_iref.va first. VT (neuron threshold)
is an external pin of SNN.gds, a voltage source here. Verilog drives w, pulse and trim.} -700 -560 0 0 0.3 0.3 {}
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
C {lab_pin.sym} 150 0 0 1 {name=lsp sig_type=std_logic lab=spike[4:0]}
C {bias.sym} -600 400 0 0 {name=x2}
C {lab_pin.sym} -750 300 0 0 {name=l20 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -750 320 0 0 {name=l21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -750 340 0 0 {name=l22 sig_type=std_logic lab=Iref_n}
C {lab_pin.sym} -450 300 0 1 {name=l23 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -450 320 0 1 {name=l24 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -450 340 0 1 {name=l25 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -450 360 0 1 {name=l26 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -450 380 0 1 {name=l27 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -450 400 0 1 {name=l28 sig_type=std_logic lab=VK}
C {lab_pin.sym} -450 420 0 1 {name=l29 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -450 440 0 1 {name=l30 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -450 460 0 1 {name=l31 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -450 480 0 1 {name=l32 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -450 500 0 1 {name=l33 sig_type=std_logic lab=VT_inh}
C {devices/code_shown.sym} -700 -360 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {devices/code_shown.sym} -1300 -300 0 0 {name=HDL_INPUTS only_toplevel=true
value="
* Nets driven from Verilog: SpiceBind sets these external sources (snn_ms_tb_v2.v).
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
Vtrim[0] trim[0] 0 0 external
Vtrim[1] trim[1] 0 0 external
Vtrim[2] trim[2] 0 0 external
Vtrim[3] trim[3] 0 0 external
"}
C {devices/code_shown.sym} 300 -360 0 0 {name=SOURCES only_toplevel=true
value="
* Parameter names start with p_ (a .param named like a net can rename that net).
.param p_vdd=3.3 p_vt=1.66
Vdd VDD 0 \{p_vdd\}
Vss VSS 0 0
* Neuron threshold: an external pin of SNN.gds
VT VT VSS \{p_vt\}
* Reference current Iref: Verilog-A model trim_iref.va (compiled to trim_iref.osdi by the
* Makefile), set by the trim bits. Its defaults are the trim law of Luz's bias_gen.py:
* 71 / 100 / 136 nA at codes 0 / 9 / 15. It feeds the bias cell's Iref pin; ammeter VIref
* reads it. p_perr: process error of the current (1 = typical): set 0.82 (ss-like) or
* 1.28 (ff-like) for a 'bad chip' to trim.
.param p_perr=1
.model trim_iref_m trim_iref perr=\{p_perr\}
Ntrim VDD VSS Iref_m Imon trim[3] trim[2] trim[1] trim[0] trim_iref_m
VIref Iref_m Iref_n 0
* Trim monitor (bias_gen's Imon pad, held at 1.65 V): sinks a copy of Iref
VImon Imon VSS 1.65
.control
pre_osdi trim_iref.osdi
.endc
"}
C {devices/code_shown.sym} 300 250 0 0 {name=TRAN only_toplevel=true
value="
* Gear integration: trap makes the DPI output current ring after each reset (mixed/)
.options method=gear
.save v(spike[0]) v(spike[1]) v(spike[2]) v(spike[3]) v(spike[4]) v(pulse[0]) v(pulse[1])
+ v(x1.VMEM_0) v(x1.VMEM_1) v(x1.VMEM_2) v(x1.VMEM_3) v(x1.VMEM_4)
+ v(trim[0]) v(trim[1]) v(trim[2]) v(trim[3]) i(VIref) i(VImon)
+ v(Vb) v(Vlk) v(VKdn) v(VK) v(VNA) v(Vthr) v(VT_dpi)
* Runs until the Verilog testbench calls $finish. ngspice reserves memory for tstop/step
* points, so a huge bound crashes it: keep this just above the longest run.
.tran 0.1u 100m 0 0.1u
"}
