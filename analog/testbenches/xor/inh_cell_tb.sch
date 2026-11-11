v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {inh_cell_tb: excitatory vs inhibitory synapse at the same weight code.
xa (sign sa = 0) and xb (sign sb = 1) are DAC_signed cells sharing both DPI tails, as the five
output DACs of snn_analog do. xa gets nsp input spikes every tsp from t0, xb the same from t0 + tgap.
Both outputs are held at vmem (Vhe, Vhi), so the charge does not depend on a membrane.
Measures the charge the excitatory DPI delivers (q_exc), the charge the inhibitory DPI_inh
removes (q_inh), their ratio, and the charge that leaks to the wrong side (crosstalk).
Both synapses are DPI_sized (DPI_inh contains one), at the output-layer biases.} -900 -700 0 0 0.3 0.3 {}
C {DAC_signed.sym} -300 -300 0 0 {name=xa}
C {lab_pin.sym} -450 -340 0 0 {name=l1 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} -450 -320 0 0 {name=l2 sig_type=std_logic lab=w[3:0]}
C {lab_pin.sym} -450 -300 0 0 {name=l3 sig_type=std_logic lab=ena}
C {lab_pin.sym} -450 -280 0 0 {name=l4 sig_type=std_logic lab=sa}
C {lab_pin.sym} -250 -340 0 1 {name=l5 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -250 -320 0 1 {name=l6 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} -250 -300 0 1 {name=l7 sig_type=std_logic lab=VDD}
C {DAC_signed.sym} -300 -150 0 0 {name=xb}
C {lab_pin.sym} -450 -190 0 0 {name=l8 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} -450 -170 0 0 {name=l9 sig_type=std_logic lab=w[3:0]}
C {lab_pin.sym} -450 -150 0 0 {name=l10 sig_type=std_logic lab=enb}
C {lab_pin.sym} -450 -130 0 0 {name=l11 sig_type=std_logic lab=sbit}
C {lab_pin.sym} -250 -190 0 1 {name=l12 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -250 -170 0 1 {name=l13 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} -250 -150 0 1 {name=l14 sig_type=std_logic lab=VDD}
C {DPI_sized.sym} 200 -300 0 0 {name=xe}
C {lab_pin.sym} 50 -320 0 0 {name=l15 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 50 -300 0 0 {name=l16 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 50 -280 0 0 {name=l17 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} 350 -320 0 1 {name=l18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 350 -300 0 1 {name=l19 sig_type=std_logic lab=Ve}
C {DPI_inh.sym} 200 -150 0 0 {name=xi}
C {lab_pin.sym} 50 -170 0 0 {name=l20 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 50 -150 0 0 {name=l21 sig_type=std_logic lab=VT_inh}
C {lab_pin.sym} 50 -130 0 0 {name=l22 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} 350 -170 0 1 {name=l23 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 350 -150 0 1 {name=l24 sig_type=std_logic lab=Vi}
C {code_shown.sym} -900 -40 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -900 80 0 0 {name=TRAN_SIM only_toplevel=false
value=".param vdd=3.3 p_vthr=2.7703 p_vtau=0.5096 p_vtau_i=0.5096 iref=14.42n
.param p_vthr_in=2.4 p_vtau_in=0.72 p_vthr_hid=2.5 p_vtau_hid=0.6225
.param p_vlk=0.48 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
.param code=2 vmem=0.5 tpw=10u tsp=200u nsp=10 t0=0.2m tgap=5m
.param b0=\{floor(code/1)-2*floor(code/2)\} b1=\{floor(code/2)-2*floor(code/4)\} b2=\{floor(code/4)-2*floor(code/8)\} b3=\{floor(code/8)-2*floor(code/16)\}
.csparam t0_c=\{t0\}
.csparam tgap_c=\{tgap\}
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
Vw0 w[0] 0 \{vdd*b0\}
Vw1 w[1] 0 \{vdd*b1\}
Vw2 w[2] 0 \{vdd*b2\}
Vw3 w[3] 0 \{vdd*b3\}
Vsa sa 0 0
Vsb sbit 0 \{vdd\}
Vena ena 0 pulse(0 \{vdd\} \{t0\} 10n 10n \{tpw\} \{tsp\} \{nsp\})
Venb enb 0 pulse(0 \{vdd\} \{t0+tgap\} 10n 10n \{tpw\} \{tsp\} \{nsp\})
* Synapse outputs held at vmem: i(Vhe) > 0 is charge delivered, i(Vhi) < 0 charge removed
Vhe Ve 0 \{vmem\}
Vhi Vi 0 \{vmem\}
.options method=gear

.control
  save all
  tran 0.1u 10.2m 0 0.5u
  let ie = i(Vhe)
  let ii = -i(Vhi)
  let tb0 = t0_c - 100u
  let tb1 = t0_c - 1u
  let ta = t0_c
  let tae = t0_c + tgap_c - 1u
  let tbb = t0_c + tgap_c
  let tbe = t0_c + 2*tgap_c - 1u
  * Idle (leakage) currents before the first spike, removed from each window
  meas tran ie0 avg ie from=$&tb0 to=$&tb1
  meas tran ii0 avg ii from=$&tb0 to=$&tb1
  meas tran qe_a integ ie from=$&ta to=$&tae
  meas tran qi_a integ ii from=$&ta to=$&tae
  meas tran qe_b integ ie from=$&tbb to=$&tbe
  meas tran qi_b integ ii from=$&tbb to=$&tbe
  meas tran pk_e max ie from=$&ta to=$&tae
  meas tran pk_i max ii from=$&tbb to=$&tbe
  let tw = tae - ta
  let q_exc = qe_a - ie0*tw
  let q_inh = qi_b - ii0*tw
  let x_exc = qi_a - ii0*tw
  let x_inh = qe_b - ie0*tw
  let ratio = q_inh/q_exc
  let q_exc_fc = q_exc*1e15
  let q_inh_fc = q_inh*1e15
  let x_exc_fc = x_exc*1e15
  let x_inh_fc = x_inh*1e15
  echo
  echo Excitatory train (xa s=0): $&q_exc_fc fC delivered / $&x_exc_fc fC on the inhibitory side
  echo Inhibitory train (xb s=1): $&q_inh_fc fC removed / $&x_inh_fc fC on the excitatory side
  echo Inhibitory / excitatory charge: $&ratio
  echo RES q_exc=$&q_exc
  echo RES q_inh=$&q_inh
  echo RES ratio=$&ratio
  echo RES x_exc=$&x_exc
  echo RES x_inh=$&x_inh
  echo RES pk_exc=$&pk_e
  echo RES pk_inh=$&pk_i
  echo RES i_idle_exc=$&ie0
  echo RES i_idle_inh=$&ii0
  if $?batchmode = 0
    plot ie ii title 'Excitatory output current (xa spike) and inhibitory sink current (xb spike)' ylabel 'A'
  end
.endc
"}
