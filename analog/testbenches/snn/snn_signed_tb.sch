v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {snn_analog_signed.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -140 0 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -150 -120 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -150 -100 0 0 {name=l3 sig_type=std_logic lab=w[31:0]}
C {lab_pin.sym} -150 -80 0 0 {name=l4 sig_type=std_logic lab=pulse[1:0]}
C {lab_pin.sym} -150 -60 0 0 {name=l5 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -150 -40 0 0 {name=l6 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -150 -20 0 0 {name=l7 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -150 0 0 0 {name=l8 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -150 20 0 0 {name=l9 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -150 40 0 0 {name=l10 sig_type=std_logic lab=VK}
C {lab_pin.sym} -150 60 0 0 {name=l11 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -150 80 0 0 {name=l12 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -150 100 0 0 {name=l13 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -150 120 0 0 {name=l14 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -150 140 0 0 {name=l15 sig_type=std_logic lab=VT}
C {lab_pin.sym} -150 160 0 0 {name=l16 sig_type=std_logic lab=s[7:0]}
C {lab_pin.sym} 150 0 0 1 {name=l18 sig_type=std_logic lab=spike[4:0]}
C {bias_cell.sym} -600 0 0 0 {name=xbias}
C {lab_pin.sym} -750 -100 0 0 {name=l19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -750 -80 0 0 {name=l20 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -750 -60 0 0 {name=l21 sig_type=std_logic lab=Iref}
C {lab_pin.sym} -450 -100 0 1 {name=l22 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -450 -80 0 1 {name=l23 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -450 -60 0 1 {name=l24 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -450 -40 0 1 {name=l25 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -450 -20 0 1 {name=l26 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -450 0 0 1 {name=l27 sig_type=std_logic lab=VK}
C {lab_pin.sym} -450 20 0 1 {name=l28 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -450 40 0 1 {name=l29 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -450 60 0 1 {name=l30 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -450 80 0 1 {name=l31 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -450 100 0 1 {name=l32 sig_type=std_logic lab=VT_inh}
C {devices/code_shown.sym} -1300 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -1300 -500 0 0 {name=TRAN_SIM only_toplevel=false
value="
* Stimulus and settings. Parameters start with p_ (a .param named like a net can rename it).
* p_wk = magnitude of weight word k (0-15, 1:2:4:8), p_sk = its sign (0 = excitatory, 1 = inhibitory),
* p_in0/p_in1 = 1 enables the 10 us / 200 us pulse train on pulse[0] / pulse[1].
.param p_vdd=3.3 p_iref=100n p_vt=1.66 p_tstop=3m p_tdel=50u p_in0=0 p_in1=0
.param p_w0=0 p_w1=0 p_w2=0 p_w3=0 p_w4=0 p_w5=0 p_w6=0 p_w7=0
.param p_s0=0 p_s1=0 p_s2=0 p_s3=0 p_s4=0 p_s5=0 p_s6=0 p_s7=0
.csparam tstop_c=\{p_tstop\}
V1 VDD VSS \{p_vdd\}
V2 VSS 0 0
IREF VDD Iref \{p_iref\}
VVT VT VSS \{p_vt\}
VP0 pulse[0] VSS PULSE(0 \{p_vdd*p_in0\} \{p_tdel\} 10n 10n 10u 200u)
VP1 pulse[1] VSS PULSE(0 \{p_vdd*p_in1\} \{p_tdel\} 10n 10n 10u 200u)
VW0_0 w[0] VSS \{p_vdd*(floor(p_w0/1)-2*floor(p_w0/2))\}
VW0_1 w[1] VSS \{p_vdd*(floor(p_w0/2)-2*floor(p_w0/4))\}
VW0_2 w[2] VSS \{p_vdd*(floor(p_w0/4)-2*floor(p_w0/8))\}
VW0_3 w[3] VSS \{p_vdd*(floor(p_w0/8)-2*floor(p_w0/16))\}
VS0 s[0] VSS \{p_vdd*p_s0\}
VW1_0 w[4] VSS \{p_vdd*(floor(p_w1/1)-2*floor(p_w1/2))\}
VW1_1 w[5] VSS \{p_vdd*(floor(p_w1/2)-2*floor(p_w1/4))\}
VW1_2 w[6] VSS \{p_vdd*(floor(p_w1/4)-2*floor(p_w1/8))\}
VW1_3 w[7] VSS \{p_vdd*(floor(p_w1/8)-2*floor(p_w1/16))\}
VS1 s[1] VSS \{p_vdd*p_s1\}
VW2_0 w[8] VSS \{p_vdd*(floor(p_w2/1)-2*floor(p_w2/2))\}
VW2_1 w[9] VSS \{p_vdd*(floor(p_w2/2)-2*floor(p_w2/4))\}
VW2_2 w[10] VSS \{p_vdd*(floor(p_w2/4)-2*floor(p_w2/8))\}
VW2_3 w[11] VSS \{p_vdd*(floor(p_w2/8)-2*floor(p_w2/16))\}
VS2 s[2] VSS \{p_vdd*p_s2\}
VW3_0 w[12] VSS \{p_vdd*(floor(p_w3/1)-2*floor(p_w3/2))\}
VW3_1 w[13] VSS \{p_vdd*(floor(p_w3/2)-2*floor(p_w3/4))\}
VW3_2 w[14] VSS \{p_vdd*(floor(p_w3/4)-2*floor(p_w3/8))\}
VW3_3 w[15] VSS \{p_vdd*(floor(p_w3/8)-2*floor(p_w3/16))\}
VS3 s[3] VSS \{p_vdd*p_s3\}
VW4_0 w[16] VSS \{p_vdd*(floor(p_w4/1)-2*floor(p_w4/2))\}
VW4_1 w[17] VSS \{p_vdd*(floor(p_w4/2)-2*floor(p_w4/4))\}
VW4_2 w[18] VSS \{p_vdd*(floor(p_w4/4)-2*floor(p_w4/8))\}
VW4_3 w[19] VSS \{p_vdd*(floor(p_w4/8)-2*floor(p_w4/16))\}
VS4 s[4] VSS \{p_vdd*p_s4\}
VW5_0 w[20] VSS \{p_vdd*(floor(p_w5/1)-2*floor(p_w5/2))\}
VW5_1 w[21] VSS \{p_vdd*(floor(p_w5/2)-2*floor(p_w5/4))\}
VW5_2 w[22] VSS \{p_vdd*(floor(p_w5/4)-2*floor(p_w5/8))\}
VW5_3 w[23] VSS \{p_vdd*(floor(p_w5/8)-2*floor(p_w5/16))\}
VS5 s[5] VSS \{p_vdd*p_s5\}
VW6_0 w[24] VSS \{p_vdd*(floor(p_w6/1)-2*floor(p_w6/2))\}
VW6_1 w[25] VSS \{p_vdd*(floor(p_w6/2)-2*floor(p_w6/4))\}
VW6_2 w[26] VSS \{p_vdd*(floor(p_w6/4)-2*floor(p_w6/8))\}
VW6_3 w[27] VSS \{p_vdd*(floor(p_w6/8)-2*floor(p_w6/16))\}
VS6 s[6] VSS \{p_vdd*p_s6\}
VW7_0 w[28] VSS \{p_vdd*(floor(p_w7/1)-2*floor(p_w7/2))\}
VW7_1 w[29] VSS \{p_vdd*(floor(p_w7/2)-2*floor(p_w7/4))\}
VW7_2 w[30] VSS \{p_vdd*(floor(p_w7/4)-2*floor(p_w7/8))\}
VW7_3 w[31] VSS \{p_vdd*(floor(p_w7/8)-2*floor(p_w7/16))\}
VS7 s[7] VSS \{p_vdd*p_s7\}
VSP0 spike[0] sp0 0
VSP1 spike[1] sp1 0
VSP2 spike[2] sp2 0
VSP3 spike[3] sp3 0
VSP4 spike[4] sp4 0
.control
  save v(sp0) v(sp1) v(sp2) v(sp3) v(sp4) v(x1.vmem_0) v(x1.vmem_1) v(x1.vmem_2) v(x1.vmem_3) v(x1.vmem_4)
  tran 0.1u $&tstop_c 0 0.1u
  set wr_singlescale
  set wr_vecnames
  wrdata snn_signed_tb.txt v(sp0) v(sp1) v(sp2) v(sp3) v(sp4) v(x1.vmem_0) v(x1.vmem_1) v(x1.vmem_2) v(x1.vmem_3) v(x1.vmem_4)
  echo RES done=1
  if $?batchmode = 0
    plot v(sp0) v(sp1)+4 v(sp2)+8 v(sp3)+12 v(sp4)+16 title 'snn_signed_tb: spikes in0, in1, hid0, hid1, out (offset 4 V)'
  end
.endc
"}
T {snn_signed_tb: the 2-2-1 network snn_analog_signed (all synapses DAC_signed_binary: signed, 1:2:4:8 magnitude 0-15)
with its biases from the real bias_cell (Iref = 100 nA; its VT_inh output is unused) and VT = 1.66 V. Weight words, signs and inputs are .params
(p_wk, p_sk, p_in0, p_in1); run_snn_signed.py runs the scenarios and counts spikes.} -1300 -900 0 0 0.4 0.4 {}
