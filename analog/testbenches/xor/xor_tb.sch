v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {xor_tb: the full snn_analog network (pure ngspice, no Verilog) with weight codes c0..c22
(word k = synapse k, see snn_analog.sch) and sign bits s0..s4 of the hidden -> output synapses.
pulse[0] = A (ina), pulse[1] = B (inb): 10 us pulses every tsp from t0, pulse[2] off.
All membranes start at 0 V. run_xor.py counts the spikes of every neuron in the wrdata file.
Default weights: XOR with hidden 0 = OR (excitatory to the output) and hidden 1 = AND (inhibitory).} -900 -700 0 0 0.3 0.3 {}
C {snn_analog.sym} 300 -200 0 0 {name=x1}
C {lab_pin.sym} 150 -340 0 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 -320 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 150 -300 0 0 {name=l3 sig_type=std_logic lab=w[91:0]}
C {lab_pin.sym} 150 -280 0 0 {name=l4 sig_type=std_logic lab=pulse[2:0]}
C {lab_pin.sym} 150 -260 0 0 {name=l5 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 150 -240 0 0 {name=l6 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 150 -220 0 0 {name=l7 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 150 -200 0 0 {name=l8 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 150 -180 0 0 {name=l9 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 150 -160 0 0 {name=l10 sig_type=std_logic lab=VK}
C {lab_pin.sym} 150 -140 0 0 {name=l11 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 150 -120 0 0 {name=l12 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 150 -100 0 0 {name=l13 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 150 -80 0 0 {name=l14 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 150 -60 0 0 {name=l15 sig_type=std_logic lab=VT}
C {lab_pin.sym} 150 -40 0 0 {name=l16 sig_type=std_logic lab=s[4:0]}
C {lab_pin.sym} 150 -20 0 0 {name=l17 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} 150 0 0 0 {name=l18 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} 150 20 0 0 {name=l19 sig_type=std_logic lab=VT_in}
C {lab_pin.sym} 150 40 0 0 {name=l20 sig_type=std_logic lab=Vthr_hid}
C {lab_pin.sym} 150 60 0 0 {name=l21 sig_type=std_logic lab=VT_hid}
C {lab_pin.sym} 450 -200 0 1 {name=lsp sig_type=std_logic lab=spike[8:0]}
C {code_shown.sym} -900 -350 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -900 -230 0 0 {name=TRAN_SIM only_toplevel=false
value=".param vdd=3.3 p_vthr=2.785 p_vtau=0.5096 p_vtau_i=0.5096 iref=14.42n
.param p_vthr_in=2.4 p_vtau_in=0.72 p_vthr_hid=2.5 p_vtau_hid=0.6225
.param p_vlk=0.48 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
* Weight codes (DAC branch weights 1:2:3:4: code 15 = weight 10, code 8 = 4, code 1 = 1)
* in -> input relay: words 0, 1; input i -> hidden j: word 3 + 3j + i; hidden j -> output: 18 + j
.param c0=15 c1=15 c2=0 c3=15 c4=15 c5=0 c6=1 c7=1 c8=0 c9=0 c10=0 c11=0 c12=0 c13=0 c14=0 c15=0 c16=0 c17=0 c18=1 c19=15 c20=0 c21=0 c22=0
.param s0=0 s1=1 s2=0 s3=0 s4=0
.param ina=1 inb=1 tpw=10u tsp=200u t0=100u tstop=4.1m
.csparam tstop_c=\{tstop\}
Vdd VDD 0 \{vdd\}
Vss VSS 0 0
* DAC unit current: Iref into a diode-connected unit current source (w[0] = 15 nA)
Iref VDD Vb \{iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
Vthr Vthr 0 \{p_vthr\}
Vtau VDD VT_dpi \{p_vtau\}
Vtau_i VDD VT_inh \{p_vtau_i\}
VNA VNA VSS \{p_vna\}
Vlk Vlk VSS \{p_vlk\}
VK VK VSS \{p_vk\}
VIp VIp VSS \{p_vip\}
VKup VKup VSS \{p_vkup\}
VKdn VKdn VSS \{p_vkdn\}
Vamp_bias Vamp_bias VSS \{p_vamp_bias\}
VT VT VSS \{p_vt\}
Vthr_in Vthr_in 0 \{p_vthr_in\}
Vtau_in VDD VT_in \{p_vtau_in\}
Vthr_hid Vthr_hid 0 \{p_vthr_hid\}
Vtau_hid VDD VT_hid \{p_vtau_hid\}
Vw0 w[0] 0 \{vdd*(floor(c0/1)-2*floor(c0/2))\}
Vw1 w[1] 0 \{vdd*(floor(c0/2)-2*floor(c0/4))\}
Vw2 w[2] 0 \{vdd*(floor(c0/4)-2*floor(c0/8))\}
Vw3 w[3] 0 \{vdd*(floor(c0/8)-2*floor(c0/16))\}
Vw4 w[4] 0 \{vdd*(floor(c1/1)-2*floor(c1/2))\}
Vw5 w[5] 0 \{vdd*(floor(c1/2)-2*floor(c1/4))\}
Vw6 w[6] 0 \{vdd*(floor(c1/4)-2*floor(c1/8))\}
Vw7 w[7] 0 \{vdd*(floor(c1/8)-2*floor(c1/16))\}
Vw8 w[8] 0 \{vdd*(floor(c2/1)-2*floor(c2/2))\}
Vw9 w[9] 0 \{vdd*(floor(c2/2)-2*floor(c2/4))\}
Vw10 w[10] 0 \{vdd*(floor(c2/4)-2*floor(c2/8))\}
Vw11 w[11] 0 \{vdd*(floor(c2/8)-2*floor(c2/16))\}
Vw12 w[12] 0 \{vdd*(floor(c3/1)-2*floor(c3/2))\}
Vw13 w[13] 0 \{vdd*(floor(c3/2)-2*floor(c3/4))\}
Vw14 w[14] 0 \{vdd*(floor(c3/4)-2*floor(c3/8))\}
Vw15 w[15] 0 \{vdd*(floor(c3/8)-2*floor(c3/16))\}
Vw16 w[16] 0 \{vdd*(floor(c4/1)-2*floor(c4/2))\}
Vw17 w[17] 0 \{vdd*(floor(c4/2)-2*floor(c4/4))\}
Vw18 w[18] 0 \{vdd*(floor(c4/4)-2*floor(c4/8))\}
Vw19 w[19] 0 \{vdd*(floor(c4/8)-2*floor(c4/16))\}
Vw20 w[20] 0 \{vdd*(floor(c5/1)-2*floor(c5/2))\}
Vw21 w[21] 0 \{vdd*(floor(c5/2)-2*floor(c5/4))\}
Vw22 w[22] 0 \{vdd*(floor(c5/4)-2*floor(c5/8))\}
Vw23 w[23] 0 \{vdd*(floor(c5/8)-2*floor(c5/16))\}
Vw24 w[24] 0 \{vdd*(floor(c6/1)-2*floor(c6/2))\}
Vw25 w[25] 0 \{vdd*(floor(c6/2)-2*floor(c6/4))\}
Vw26 w[26] 0 \{vdd*(floor(c6/4)-2*floor(c6/8))\}
Vw27 w[27] 0 \{vdd*(floor(c6/8)-2*floor(c6/16))\}
Vw28 w[28] 0 \{vdd*(floor(c7/1)-2*floor(c7/2))\}
Vw29 w[29] 0 \{vdd*(floor(c7/2)-2*floor(c7/4))\}
Vw30 w[30] 0 \{vdd*(floor(c7/4)-2*floor(c7/8))\}
Vw31 w[31] 0 \{vdd*(floor(c7/8)-2*floor(c7/16))\}
Vw32 w[32] 0 \{vdd*(floor(c8/1)-2*floor(c8/2))\}
Vw33 w[33] 0 \{vdd*(floor(c8/2)-2*floor(c8/4))\}
Vw34 w[34] 0 \{vdd*(floor(c8/4)-2*floor(c8/8))\}
Vw35 w[35] 0 \{vdd*(floor(c8/8)-2*floor(c8/16))\}
Vw36 w[36] 0 \{vdd*(floor(c9/1)-2*floor(c9/2))\}
Vw37 w[37] 0 \{vdd*(floor(c9/2)-2*floor(c9/4))\}
Vw38 w[38] 0 \{vdd*(floor(c9/4)-2*floor(c9/8))\}
Vw39 w[39] 0 \{vdd*(floor(c9/8)-2*floor(c9/16))\}
Vw40 w[40] 0 \{vdd*(floor(c10/1)-2*floor(c10/2))\}
Vw41 w[41] 0 \{vdd*(floor(c10/2)-2*floor(c10/4))\}
Vw42 w[42] 0 \{vdd*(floor(c10/4)-2*floor(c10/8))\}
Vw43 w[43] 0 \{vdd*(floor(c10/8)-2*floor(c10/16))\}
Vw44 w[44] 0 \{vdd*(floor(c11/1)-2*floor(c11/2))\}
Vw45 w[45] 0 \{vdd*(floor(c11/2)-2*floor(c11/4))\}
Vw46 w[46] 0 \{vdd*(floor(c11/4)-2*floor(c11/8))\}
Vw47 w[47] 0 \{vdd*(floor(c11/8)-2*floor(c11/16))\}
Vw48 w[48] 0 \{vdd*(floor(c12/1)-2*floor(c12/2))\}
Vw49 w[49] 0 \{vdd*(floor(c12/2)-2*floor(c12/4))\}
Vw50 w[50] 0 \{vdd*(floor(c12/4)-2*floor(c12/8))\}
Vw51 w[51] 0 \{vdd*(floor(c12/8)-2*floor(c12/16))\}
Vw52 w[52] 0 \{vdd*(floor(c13/1)-2*floor(c13/2))\}
Vw53 w[53] 0 \{vdd*(floor(c13/2)-2*floor(c13/4))\}
Vw54 w[54] 0 \{vdd*(floor(c13/4)-2*floor(c13/8))\}
Vw55 w[55] 0 \{vdd*(floor(c13/8)-2*floor(c13/16))\}
Vw56 w[56] 0 \{vdd*(floor(c14/1)-2*floor(c14/2))\}
Vw57 w[57] 0 \{vdd*(floor(c14/2)-2*floor(c14/4))\}
Vw58 w[58] 0 \{vdd*(floor(c14/4)-2*floor(c14/8))\}
Vw59 w[59] 0 \{vdd*(floor(c14/8)-2*floor(c14/16))\}
Vw60 w[60] 0 \{vdd*(floor(c15/1)-2*floor(c15/2))\}
Vw61 w[61] 0 \{vdd*(floor(c15/2)-2*floor(c15/4))\}
Vw62 w[62] 0 \{vdd*(floor(c15/4)-2*floor(c15/8))\}
Vw63 w[63] 0 \{vdd*(floor(c15/8)-2*floor(c15/16))\}
Vw64 w[64] 0 \{vdd*(floor(c16/1)-2*floor(c16/2))\}
Vw65 w[65] 0 \{vdd*(floor(c16/2)-2*floor(c16/4))\}
Vw66 w[66] 0 \{vdd*(floor(c16/4)-2*floor(c16/8))\}
Vw67 w[67] 0 \{vdd*(floor(c16/8)-2*floor(c16/16))\}
Vw68 w[68] 0 \{vdd*(floor(c17/1)-2*floor(c17/2))\}
Vw69 w[69] 0 \{vdd*(floor(c17/2)-2*floor(c17/4))\}
Vw70 w[70] 0 \{vdd*(floor(c17/4)-2*floor(c17/8))\}
Vw71 w[71] 0 \{vdd*(floor(c17/8)-2*floor(c17/16))\}
Vw72 w[72] 0 \{vdd*(floor(c18/1)-2*floor(c18/2))\}
Vw73 w[73] 0 \{vdd*(floor(c18/2)-2*floor(c18/4))\}
Vw74 w[74] 0 \{vdd*(floor(c18/4)-2*floor(c18/8))\}
Vw75 w[75] 0 \{vdd*(floor(c18/8)-2*floor(c18/16))\}
Vw76 w[76] 0 \{vdd*(floor(c19/1)-2*floor(c19/2))\}
Vw77 w[77] 0 \{vdd*(floor(c19/2)-2*floor(c19/4))\}
Vw78 w[78] 0 \{vdd*(floor(c19/4)-2*floor(c19/8))\}
Vw79 w[79] 0 \{vdd*(floor(c19/8)-2*floor(c19/16))\}
Vw80 w[80] 0 \{vdd*(floor(c20/1)-2*floor(c20/2))\}
Vw81 w[81] 0 \{vdd*(floor(c20/2)-2*floor(c20/4))\}
Vw82 w[82] 0 \{vdd*(floor(c20/4)-2*floor(c20/8))\}
Vw83 w[83] 0 \{vdd*(floor(c20/8)-2*floor(c20/16))\}
Vw84 w[84] 0 \{vdd*(floor(c21/1)-2*floor(c21/2))\}
Vw85 w[85] 0 \{vdd*(floor(c21/2)-2*floor(c21/4))\}
Vw86 w[86] 0 \{vdd*(floor(c21/4)-2*floor(c21/8))\}
Vw87 w[87] 0 \{vdd*(floor(c21/8)-2*floor(c21/16))\}
Vw88 w[88] 0 \{vdd*(floor(c22/1)-2*floor(c22/2))\}
Vw89 w[89] 0 \{vdd*(floor(c22/2)-2*floor(c22/4))\}
Vw90 w[90] 0 \{vdd*(floor(c22/4)-2*floor(c22/8))\}
Vw91 w[91] 0 \{vdd*(floor(c22/8)-2*floor(c22/16))\}
Vs0 s[0] 0 \{vdd*s0\}
Vs1 s[1] 0 \{vdd*s1\}
Vs2 s[2] 0 \{vdd*s2\}
Vs3 s[3] 0 \{vdd*s3\}
Vs4 s[4] 0 \{vdd*s4\}
Vp0 pulse[0] 0 pulse(0 \{vdd*ina\} \{t0\} 10n 10n \{tpw\} \{tsp\})
Vp1 pulse[1] 0 pulse(0 \{vdd*inb\} \{t0\} 10n 10n \{tpw\} \{tsp\})
Vp2 pulse[2] 0 0
* spike[n] copied to sp<n> (no load) for wrdata
Esp0 sp0 0 spike[0] 0 1
Esp1 sp1 0 spike[1] 0 1
Esp2 sp2 0 spike[2] 0 1
Esp3 sp3 0 spike[3] 0 1
Esp4 sp4 0 spike[4] 0 1
Esp5 sp5 0 spike[5] 0 1
Esp6 sp6 0 spike[6] 0 1
Esp7 sp7 0 spike[7] 0 1
Esp8 sp8 0 spike[8] 0 1
.ic v(x1.VMEM_0)=0 v(x1.VMEM_1)=0 v(x1.VMEM_2)=0 v(x1.VMEM_3)=0 v(x1.VMEM_4)=0 v(x1.VMEM_5)=0 v(x1.VMEM_6)=0 v(x1.VMEM_7)=0 v(x1.VMEM_8)=0 v(spike[0])=0 v(spike[1])=0 v(spike[2])=0 v(spike[3])=0 v(spike[4])=0 v(spike[5])=0 v(spike[6])=0 v(spike[7])=0 v(spike[8])=0
.options method=gear

.control
  save v(sp0) v(sp1) v(sp2) v(sp3) v(sp4) v(sp5) v(sp6) v(sp7) v(sp8) v(x1.VMEM_8) v(x1.VMEM_3) v(x1.VMEM_4)
  set wr_singlescale
  set wr_vecnames
  * Max step 0.1u: at 0.5u a relay spike edge sometimes kicked this neuron into a false spike
  tran 0.1u $&tstop_c 0 0.1u
  meas tran vmax_out max v(x1.VMEM_8)
  echo RES vmax_out=$&vmax_out
  wrdata xor_tb.txt v(sp0) v(sp1) v(sp2) v(sp3) v(sp4) v(sp5) v(sp6) v(sp7) v(sp8) v(x1.VMEM_8) v(x1.VMEM_3) v(x1.VMEM_4)
  if $?batchmode = 0
    plot v(x1.VMEM_8) v(sp8)+4 v(sp3)*0.3+8 v(sp4)*0.3+9.5 v(sp0)*0.3+11 v(sp1)*0.3+12.5 title 'Output membrane, output spike; hidden OR, AND; inputs A, B (offset)' ylabel 'V'
  end
.endc
"}
