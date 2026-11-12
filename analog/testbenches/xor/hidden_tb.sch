v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {hidden_tb: one hidden neuron of snn_analog with its two active inputs.
Relays: pulse train -> DAC (code_in) -> DPI -> neuron_sized, for input A (ina = 1) and B (inb = 1),
10 us pulses every tsp. The relay spikes drive the en pins of the hidden neuron's DACs
(codes ca, cb), as in the network; a third DAC (input 2, code 0, never enabled) is on the same tail.
Used for the OR neuron (one input fires it) and the AND neuron (one input must lose to the leak,
two must fire it). run_xor.py counts the spikes of all three neurons from the wrdata file.} -900 -1000 0 0 0.3 0.3 {}
C {DAC.sym} -300 -600 0 0 {name=xda}
C {lab_pin.sym} -450 -640 0 0 {name=l1 sig_type=std_logic lab=Isum_a}
C {lab_pin.sym} -450 -620 0 0 {name=l2 sig_type=std_logic lab=wr[3:0]}
C {lab_pin.sym} -450 -600 0 0 {name=l3 sig_type=std_logic lab=pa}
C {lab_pin.sym} -250 -640 0 1 {name=l4 sig_type=std_logic lab=Vb}
C {DPI.sym} 150 -600 0 0 {name=xpa}
C {lab_pin.sym} 0 -620 0 0 {name=l5 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} 0 -600 0 0 {name=l6 sig_type=std_logic lab=VT_in}
C {lab_pin.sym} 0 -580 0 0 {name=l7 sig_type=std_logic lab=Isum_a}
C {lab_pin.sym} 300 -620 0 1 {name=l8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 300 -600 0 1 {name=l9 sig_type=std_logic lab=VMEM_a}
C {neuron_sized.sym} 600 -500 0 0 {name=xna}
C {lab_pin.sym} 450 -580 0 0 {name=l10 sig_type=std_logic lab=VMEM_a}
C {lab_pin.sym} 750 -580 0 1 {name=l11 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 750 -560 0 1 {name=l12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 750 -540 0 1 {name=l13 sig_type=std_logic lab=spk_a}
C {lab_pin.sym} 450 -560 0 0 {name=l14 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 450 -540 0 0 {name=l15 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 450 -520 0 0 {name=l16 sig_type=std_logic lab=VK}
C {lab_pin.sym} 450 -500 0 0 {name=l17 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 450 -480 0 0 {name=l18 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 450 -460 0 0 {name=l19 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 450 -440 0 0 {name=l20 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 450 -420 0 0 {name=l21 sig_type=std_logic lab=VT}
C {DAC.sym} -300 -150 0 0 {name=xdb}
C {lab_pin.sym} -450 -190 0 0 {name=l22 sig_type=std_logic lab=Isum_b}
C {lab_pin.sym} -450 -170 0 0 {name=l23 sig_type=std_logic lab=wr[3:0]}
C {lab_pin.sym} -450 -150 0 0 {name=l24 sig_type=std_logic lab=pb}
C {lab_pin.sym} -250 -190 0 1 {name=l25 sig_type=std_logic lab=Vb}
C {DPI.sym} 150 -150 0 0 {name=xpb}
C {lab_pin.sym} 0 -170 0 0 {name=l26 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} 0 -150 0 0 {name=l27 sig_type=std_logic lab=VT_in}
C {lab_pin.sym} 0 -130 0 0 {name=l28 sig_type=std_logic lab=Isum_b}
C {lab_pin.sym} 300 -170 0 1 {name=l29 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 300 -150 0 1 {name=l30 sig_type=std_logic lab=VMEM_b}
C {neuron_sized.sym} 600 -50 0 0 {name=xnb}
C {lab_pin.sym} 450 -130 0 0 {name=l31 sig_type=std_logic lab=VMEM_b}
C {lab_pin.sym} 750 -130 0 1 {name=l32 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 750 -110 0 1 {name=l33 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 750 -90 0 1 {name=l34 sig_type=std_logic lab=spk_b}
C {lab_pin.sym} 450 -110 0 0 {name=l35 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 450 -90 0 0 {name=l36 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 450 -70 0 0 {name=l37 sig_type=std_logic lab=VK}
C {lab_pin.sym} 450 -50 0 0 {name=l38 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 450 -30 0 0 {name=l39 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 450 -10 0 0 {name=l40 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 450 10 0 0 {name=l41 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 450 30 0 0 {name=l42 sig_type=std_logic lab=VT}
C {DAC.sym} 1300 -600 0 0 {name=xha}
C {lab_pin.sym} 1150 -640 0 0 {name=l43 sig_type=std_logic lab=Isum_h}
C {lab_pin.sym} 1150 -620 0 0 {name=l44 sig_type=std_logic lab=wa[3:0]}
C {lab_pin.sym} 1150 -600 0 0 {name=l45 sig_type=std_logic lab=spk_a}
C {lab_pin.sym} 1350 -640 0 1 {name=l46 sig_type=std_logic lab=Vb}
C {DAC.sym} 1300 -480 0 0 {name=xhb}
C {lab_pin.sym} 1150 -520 0 0 {name=l47 sig_type=std_logic lab=Isum_h}
C {lab_pin.sym} 1150 -500 0 0 {name=l48 sig_type=std_logic lab=wb[3:0]}
C {lab_pin.sym} 1150 -480 0 0 {name=l49 sig_type=std_logic lab=spk_b}
C {lab_pin.sym} 1350 -520 0 1 {name=l50 sig_type=std_logic lab=Vb}
C {DAC.sym} 1300 -360 0 0 {name=xhc}
C {lab_pin.sym} 1150 -400 0 0 {name=l51 sig_type=std_logic lab=Isum_h}
C {lab_pin.sym} 1150 -380 0 0 {name=l52 sig_type=std_logic lab=w0[3:0]}
C {lab_pin.sym} 1150 -360 0 0 {name=l53 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1350 -400 0 1 {name=l54 sig_type=std_logic lab=Vb}
C {DPI.sym} 1750 -480 0 0 {name=xph}
C {lab_pin.sym} 1600 -500 0 0 {name=l55 sig_type=std_logic lab=Vthr_hid}
C {lab_pin.sym} 1600 -480 0 0 {name=l56 sig_type=std_logic lab=VT_hid}
C {lab_pin.sym} 1600 -460 0 0 {name=l57 sig_type=std_logic lab=Isum_h}
C {lab_pin.sym} 1900 -500 0 1 {name=l58 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1900 -480 0 1 {name=l59 sig_type=std_logic lab=VMEM_h}
C {neuron_sized.sym} 2200 -380 0 0 {name=xnh}
C {lab_pin.sym} 2050 -460 0 0 {name=l60 sig_type=std_logic lab=VMEM_h}
C {lab_pin.sym} 2350 -460 0 1 {name=l61 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2350 -440 0 1 {name=l62 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2350 -420 0 1 {name=l63 sig_type=std_logic lab=spk_h}
C {lab_pin.sym} 2050 -440 0 0 {name=l64 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 2050 -420 0 0 {name=l65 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 2050 -400 0 0 {name=l66 sig_type=std_logic lab=VK}
C {lab_pin.sym} 2050 -380 0 0 {name=l67 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 2050 -360 0 0 {name=l68 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 2050 -340 0 0 {name=l69 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 2050 -320 0 0 {name=l70 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 2050 -300 0 0 {name=l71 sig_type=std_logic lab=VT}
C {code_shown.sym} -900 150 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -900 270 0 0 {name=TRAN_SIM only_toplevel=false
value=".param vdd=3.3 vthr=2.909 vtau=0.40 vtau_i=0.40 iref=14.42n
.param p_vlk=0.425 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
.param code_in=15 ca=1 cb=1 ina=1 inb=1 tpw=10u tsp=200u t0=100u tstop=10.1m
* Separate DPI biases for the relays (_in) and the hidden neuron (_hid); default: the shared ones
.param vthr_in=\{vthr\} vtau_in=\{vtau\} vthr_hid=\{vthr\} vtau_hid=\{vtau\}
.param r0=\{floor(code_in/1)-2*floor(code_in/2)\} r1=\{floor(code_in/2)-2*floor(code_in/4)\} r2=\{floor(code_in/4)-2*floor(code_in/8)\} r3=\{floor(code_in/8)-2*floor(code_in/16)\}
.param a0=\{floor(ca/1)-2*floor(ca/2)\} a1=\{floor(ca/2)-2*floor(ca/4)\} a2=\{floor(ca/4)-2*floor(ca/8)\} a3=\{floor(ca/8)-2*floor(ca/16)\}
.param b0=\{floor(cb/1)-2*floor(cb/2)\} b1=\{floor(cb/2)-2*floor(cb/4)\} b2=\{floor(cb/4)-2*floor(cb/8)\} b3=\{floor(cb/8)-2*floor(cb/16)\}
.csparam tstop_c=\{tstop\}
Vdd VDD 0 \{vdd\}
Vss VSS 0 0
* DAC unit current: Iref into a diode-connected unit current source (w[0] = 15 nA)
Iref VDD Vb \{iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
Vthr Vthr 0 \{vthr\}
Vtau VDD VT_dpi \{vtau\}
Vtau_i VDD VT_inh \{vtau_i\}
VNA VNA VSS \{p_vna\}
Vlk Vlk VSS \{p_vlk\}
VK VK VSS \{p_vk\}
VIp VIp VSS \{p_vip\}
VKup VKup VSS \{p_vkup\}
VKdn VKdn VSS \{p_vkdn\}
Vamp_bias Vamp_bias VSS \{p_vamp_bias\}
VT VT VSS \{p_vt\}
Vthr_in Vthr_in 0 \{vthr_in\}
Vtau_in VDD VT_in \{vtau_in\}
Vthr_hid Vthr_hid 0 \{vthr_hid\}
Vtau_hid VDD VT_hid \{vtau_hid\}
Vwr0 wr[0] 0 \{vdd*r0\}
Vwr1 wr[1] 0 \{vdd*r1\}
Vwr2 wr[2] 0 \{vdd*r2\}
Vwr3 wr[3] 0 \{vdd*r3\}
Vwa0 wa[0] 0 \{vdd*a0\}
Vwa1 wa[1] 0 \{vdd*a1\}
Vwa2 wa[2] 0 \{vdd*a2\}
Vwa3 wa[3] 0 \{vdd*a3\}
Vwb0 wb[0] 0 \{vdd*b0\}
Vwb1 wb[1] 0 \{vdd*b1\}
Vwb2 wb[2] 0 \{vdd*b2\}
Vwb3 wb[3] 0 \{vdd*b3\}
Vw00 w0[0] 0 0
Vw01 w0[1] 0 0
Vw02 w0[2] 0 0
Vw03 w0[3] 0 0
VpA pa 0 pulse(0 \{vdd*ina\} \{t0\} 10n 10n \{tpw\} \{tsp\})
VpB pb 0 pulse(0 \{vdd*inb\} \{t0\} 10n 10n \{tpw\} \{tsp\})
.ic v(VMEM_a)=0 v(VMEM_b)=0 v(VMEM_h)=0 v(spk_a)=0 v(spk_b)=0 v(spk_h)=0
.options method=gear

.control
  save v(spk_a) v(spk_b) v(spk_h) v(VMEM_h) v(VMEM_a) v(pa)
  set wr_singlescale
  set wr_vecnames
  * Max step 0.1u: at 0.5u a relay spike edge sometimes kicked this neuron into a false spike
  tran 0.1u $&tstop_c 0 0.1u
  meas tran vmax_h max v(VMEM_h)
  meas tran spk_max max v(spk_h)
  echo RES vmax_h=$&vmax_h
  echo RES spk_max=$&spk_max
  wrdata hidden_tb.txt v(spk_a) v(spk_b) v(spk_h) v(VMEM_h)
  if $?batchmode = 0
    plot v(VMEM_h) v(spk_h) v(spk_a)*0.3+3.5 v(spk_b)*0.3+4.7 title 'Hidden membrane and spike; relay spikes A, B (offset)' ylabel 'V'
  end
.endc
"}
