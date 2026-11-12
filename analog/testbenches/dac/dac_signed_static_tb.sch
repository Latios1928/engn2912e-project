v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dac_signed_static_tb: DC characterisation of DAC_signed.sch (the DAC with a sign switch).
Vb from Iref (p_iref) into a diode-connected unit current source, as in DACs-DPI.sch. Both outputs are held
by voltage sources (Isum_e at p_ve, Isum_i at p_vi), en is held high. One nested DC sweep covers all 16 weight
codes x both signs (s = 0: current to Isum_e, s = 1: to Isum_i); then full scale while sweeping each output's
voltage (compliance). Prints RES lines; run_dac_signed.py runs it over corners and mismatch (--pex: post-layout).} -820 -560 0 0 0.3 0.3 {}
T {Device under test} -170 -130 0 0 0.25 0.25 {}
C {DAC_signed.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -40 0 0 {name=l1 sig_type=std_logic lab=Ie}
C {lab_pin.sym} -150 -20 0 0 {name=l2 sig_type=std_logic lab=w[3:0]}
C {lab_pin.sym} -150 0 0 0 {name=l3 sig_type=std_logic lab=en}
C {lab_pin.sym} -150 20 0 0 {name=l4 sig_type=std_logic lab=s}
C {lab_pin.sym} 50 -40 0 1 {name=l5 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 50 -20 0 1 {name=l6 sig_type=std_logic lab=Ii}
C {lab_pin.sym} 50 0 0 1 {name=l7 sig_type=std_logic lab=VDD}
C {devices/code_shown.sym} -820 -380 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {code_shown.sym} -820 -240 0 0 {name=SOURCES only_toplevel=false
value="
* Parameters start with p_ (a .param named like a net can rename that net).
.param p_vdd=3.3 p_iref=14.42n p_ve=2.5 p_vi=2.5 p_code=15 p_s=0 p_vstep=10m
* gmin (a conductance ngspice puts across every junction) is 1e-12 S by default:
* at 2.5 V that alone is 2.5 pA per node, which swamps the off-state leakage this
* testbench measures (true leakage at tt 27 C: ~4 pA at code 0, < 1 fA to the
* unselected output). 1e-16 S converges fine here.
.options gmin=1e-16
.csparam vdd_c=\{p_vdd\}
.csparam ve_c=\{p_ve\}
.csparam vi_c=\{p_vi\}
.csparam vstep_c=\{p_vstep\}
Vdd VDD 0 \{p_vdd\}
* DAC unit current: Iref into a diode-connected copy of the unit current source (1 um / 8 um)
Iref VDD Vb \{p_iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
Ven en 0 \{p_vdd\}
* Weight code (0..15) and sign (0/1) as swept voltages, decoded into logic levels
Vcode code 0 \{p_code\}
Vsgn sgn 0 \{p_s\}
Bw0 w[0] 0 V = \{p_vdd\}*(floor(v(code)+0.5) - 2*floor(floor(v(code)+0.5)/2))
Bw1 w[1] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/2) - 2*floor(floor(v(code)+0.5)/4))
Bw2 w[2] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/4) - 2*floor(floor(v(code)+0.5)/8))
Bw3 w[3] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/8) - 2*floor(floor(v(code)+0.5)/16))
Bs s 0 V = \{p_vdd\}*floor(v(sgn)+0.5)
* Outputs held at fixed voltages (stand-ins for the DPI tails). The DAC sinks
* current, so the current into each output node is -i(V...).
Vhe Ie 0 \{p_ve\}
Vhi Ii 0 \{p_vi\}
"}
C {code_shown.sym} -820 40 0 0 {name=ANALYSIS only_toplevel=false
value="
.control
  save i(vhe) i(vhi) v(vb) v(w[0]) v(w[1]) v(w[2]) v(w[3]) v(s)

  * 1. All codes x both signs: index k = 16*s + code
  dc Vcode 0 15 1 Vsgn 0 1 1
  let ie = -i(vhe)
  let ii = -i(vhi)
  let nk = length(ie)
  echo RES npts=$&nk
  let k = 0
  while k < nk
    let a = ie[k]
    let b = ii[k]
    echo RES ie$&k=$&a
    echo RES ii$&k=$&b
    let k = k + 1
  end
  let vb0 = v(vb)[0]
  echo RES vb=$&vb0

  * 2. Compliance: full scale (code 15) while sweeping each output's voltage.
  * vmin_*: lowest output voltage at which the current is within 1 % of its
  * value at the nominal output voltage.
  alter vcode dc = 15
  alter vsgn dc = 0
  dc Vhe 0 $&vdd_c $&vstep_c
  let ie_v = -i(vhe)
  meas dc ie_nom find ie_v at=$&ve_c
  let lvl = 0.99*ie_nom
  let vmin_e = -1
  meas dc vmin_e when ie_v=$&lvl rise=1
  echo RES ie_fs_nom=$&ie_nom
  echo RES vmin_e=$&vmin_e
  wrdata dac_signed_static_tb_compliance_e.txt ie_v

  alter vsgn dc = 1
  dc Vhi 0 $&vdd_c $&vstep_c
  let ii_v = -i(vhi)
  meas dc ii_nom find ii_v at=$&vi_c
  let lvl = 0.99*ii_nom
  let vmin_i = -1
  meas dc vmin_i when ii_v=$&lvl rise=1
  echo RES ii_fs_nom=$&ii_nom
  echo RES vmin_i=$&vmin_i
  wrdata dac_signed_static_tb_compliance_i.txt ii_v
  echo dac_signed_static_tb: done

  if $?batchmode = 0
    plot ie_v ii_v title 'dac_signed_static_tb: full-scale current vs output voltage' ylabel 'A'
  end
.endc
"}
