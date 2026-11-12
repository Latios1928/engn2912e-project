v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_startup_tb: VDD ramps from 0 to vdd in 'tramp' with every node at 0 V (uic), i.e. starting in the zero-current state of the beta multiplier. RES m_end (Imon / target at the end), t_settle (time from the end of the ramp until Imon is within 1 % of its final value).} -1100 -950 0 0 0.3 0.3 {}
C {vsource.sym} -1100 -300 0 0 {name=V1 value="pwl(0 0 \{tramp\} \{vdd\})" savecurrent=false}
C {lab_pin.sym} -1100 -330 0 0 {name=l1 sig_type=std_logic lab=VDDS}
C {lab_pin.sym} -1100 -270 0 0 {name=l2 sig_type=std_logic lab=0}
C {ammeter.sym} -1000 -300 0 0 {name=VIdd savecurrent=true spice_ignore=0}
C {lab_pin.sym} -1000 -330 0 0 {name=l3 sig_type=std_logic lab=VDDS}
C {lab_pin.sym} -1000 -270 0 0 {name=l4 sig_type=std_logic lab=VDD}
C {vsource.sym} -800 -300 0 0 {name=Vtr3 value='vdd*(floor(code/8)-2*floor(code/16))' savecurrent=false}
C {lab_pin.sym} -800 -330 0 0 {name=l5 sig_type=std_logic lab=tr3}
C {lab_pin.sym} -800 -270 0 0 {name=l6 sig_type=std_logic lab=0}
C {vsource.sym} -720 -300 0 0 {name=Vtr2 value='vdd*(floor(code/4)-2*floor(code/8))' savecurrent=false}
C {lab_pin.sym} -720 -330 0 0 {name=l7 sig_type=std_logic lab=tr2}
C {lab_pin.sym} -720 -270 0 0 {name=l8 sig_type=std_logic lab=0}
C {vsource.sym} -640 -300 0 0 {name=Vtr1 value='vdd*(floor(code/2)-2*floor(code/4))' savecurrent=false}
C {lab_pin.sym} -640 -330 0 0 {name=l9 sig_type=std_logic lab=tr1}
C {lab_pin.sym} -640 -270 0 0 {name=l10 sig_type=std_logic lab=0}
C {vsource.sym} -560 -300 0 0 {name=Vtr0 value='vdd*(floor(code/1)-2*floor(code/2))' savecurrent=false}
C {lab_pin.sym} -560 -330 0 0 {name=l11 sig_type=std_logic lab=tr0}
C {lab_pin.sym} -560 -270 0 0 {name=l12 sig_type=std_logic lab=0}
C {vsource.sym} -450 -300 0 0 {name=Vmon value=\{vmon\} savecurrent=false}
C {lab_pin.sym} -450 -330 0 0 {name=l13 sig_type=std_logic lab=Imon}
C {lab_pin.sym} -450 -270 0 0 {name=l14 sig_type=std_logic lab=0}
C {analog/bias/bias_gen.sym} -200 -300 0 0 {name=xbg}
C {lab_pin.sym} -350 -400.0 0 0 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -350 -380.0 0 0 {name=l16 sig_type=std_logic lab=0}
C {lab_pin.sym} -350 -360.0 0 0 {name=l17 sig_type=std_logic lab=tr3}
C {lab_pin.sym} -350 -340.0 0 0 {name=l18 sig_type=std_logic lab=tr2}
C {lab_pin.sym} -350 -320.0 0 0 {name=l19 sig_type=std_logic lab=tr1}
C {lab_pin.sym} -350 -300.0 0 0 {name=l20 sig_type=std_logic lab=tr0}
C {lab_pin.sym} -350 -280.0 0 0 {name=l21 sig_type=std_logic lab=Imon}
C {lab_pin.sym} -50 -400.0 0 1 {name=l22 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -50 -380.0 0 1 {name=l23 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -50 -360.0 0 1 {name=l24 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -50 -340.0 0 1 {name=l25 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -50 -320.0 0 1 {name=l26 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -50 -300.0 0 1 {name=l27 sig_type=std_logic lab=VK}
C {lab_pin.sym} -50 -280.0 0 1 {name=l28 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -50 -260.0 0 1 {name=l29 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -50 -240.0 0 1 {name=l30 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -50 -220.0 0 1 {name=l31 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -50 -200.0 0 1 {name=l32 sig_type=std_logic lab=VT}
C {devices/code_shown.sym} -1100 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} -1100 -150 0 0 {name=CONTROL only_toplevel=true
value="
.param vdd=3.3 code=9 vmon=1.65
.csparam code_c=\{code\}
.csparam vdd_c=\{vdd\}
.param tramp=100u
.csparam tramp_c=\{tramp\}
.control
  save i(Vmon) v(xbg.Vgn) v(VT) v(Vb) v(VDD)
  let tstop = tramp_c + 3m
  tran 1u $&tstop 0 10u uic
  * Imon averaged over the last 1 ms: the instantaneous current through a voltage source is
  * noisy in a variable-step transient. Settling is judged on the master gate Vgn (quiet).
  let tend0 = tstop - 1m
  meas tran ifin avg i(Vmon) from=$&tend0 to=$&tstop
  let tr = 1/(0.743 + (15 - code_c)*0.045133)
  let m_end = abs(ifin)/(2.3072e-07*tr)
  echo RES m_end=$&m_end
  let vgn = v(xbg.Vgn)
  meas tran vgnfin avg vgn from=$&tend0 to=$&tstop
  let lo = vgnfin - 1m
  meas tran tlo when vgn=$&lo cross=last
  let t_settle = tlo - tramp_c
  echo RES t_settle=$&t_settle
  let imon = abs(i(Vmon))
  if $?batchmode = 0
    plot imon title 'Imon during start-up'
  end
.endc
"}
