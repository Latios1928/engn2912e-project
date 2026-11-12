v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_startup_tb: VDD ramps from 0 to vdd in 'tramp' with every node at 0 V (uic), i.e. starting in the zero-current state of the beta multiplier. RES m_end (Imon / target at the end), t_settle (time from the end of the ramp until Imon is within 1 % of its final value).} -1100 -950 0 0 0.3 0.3 {}
C {analog/bias/bias_gen.sym} 0 0 0 0 {name=xbg}
C {vsource.sym} -940 200 0 0 {name=V1 value="pwl(0 0 \{tramp\} \{vdd\})" savecurrent=false}
C {gnd.sym} -940 230 0 0 {name=g1 lab=0}
N -940 170 -940 -160 {}
N -940 -160 -200 -160 {}
C {ammeter.sym} -200 -130 0 0 {name=VIdd savecurrent=true spice_ignore=0}
N -200 -100 -150 -100.0 {}
C {lab_wire.sym} -175.0 -100.0 0 0 {name=w2 sig_type=std_logic lab=VDD}
N -150 -80.0 -820 -80.0 {}
N -820 -80.0 -820 230 {}
C {gnd.sym} -820 230 0 0 {name=g3 lab=0}
C {vsource.sym} -700 200 0 0 {name=Vtr3 value='vdd*b3' savecurrent=false}
C {gnd.sym} -700 230 0 0 {name=g4 lab=0}
N -700 170 -700 -60.0 {}
N -700 -60.0 -150 -60.0 {}
C {vsource.sym} -590 200 0 0 {name=Vtr2 value='vdd*b2' savecurrent=false}
C {gnd.sym} -590 230 0 0 {name=g5 lab=0}
N -590 170 -590 -40.0 {}
N -590 -40.0 -150 -40.0 {}
C {vsource.sym} -480 200 0 0 {name=Vtr1 value='vdd*b1' savecurrent=false}
C {gnd.sym} -480 230 0 0 {name=g6 lab=0}
N -480 170 -480 -20.0 {}
N -480 -20.0 -150 -20.0 {}
C {vsource.sym} -370 200 0 0 {name=Vtr0 value='vdd*b0' savecurrent=false}
C {gnd.sym} -370 230 0 0 {name=g7 lab=0}
N -370 170 -370 0.0 {}
N -370 0.0 -150 0.0 {}
C {vsource.sym} -260 200 0 0 {name=Vmon value=\{vmon\} savecurrent=false}
C {gnd.sym} -260 230 0 0 {name=g8 lab=0}
N -260 170 -260 20.0 {}
N -260 20.0 -150 20.0 {}
N 150 -100.0 210 -100.0 {}
C {lab_wire.sym} 180.0 -100.0 0 0 {name=w9 sig_type=std_logic lab=Vb}
N 150 -80.0 210 -80.0 {}
C {lab_wire.sym} 180.0 -80.0 0 0 {name=w10 sig_type=std_logic lab=Vthr}
N 150 -60.0 210 -60.0 {}
C {lab_wire.sym} 180.0 -60.0 0 0 {name=w11 sig_type=std_logic lab=VT_dpi}
N 150 -40.0 210 -40.0 {}
C {lab_wire.sym} 180.0 -40.0 0 0 {name=w12 sig_type=std_logic lab=VNA}
N 150 -20.0 210 -20.0 {}
C {lab_wire.sym} 180.0 -20.0 0 0 {name=w13 sig_type=std_logic lab=Vlk}
N 150 0.0 210 0.0 {}
C {lab_wire.sym} 180.0 0.0 0 0 {name=w14 sig_type=std_logic lab=VK}
N 150 20.0 210 20.0 {}
C {lab_wire.sym} 180.0 20.0 0 0 {name=w15 sig_type=std_logic lab=VIp}
N 150 40.0 210 40.0 {}
C {lab_wire.sym} 180.0 40.0 0 0 {name=w16 sig_type=std_logic lab=VKup}
N 150 60.0 210 60.0 {}
C {lab_wire.sym} 180.0 60.0 0 0 {name=w17 sig_type=std_logic lab=VKdn}
N 150 80.0 210 80.0 {}
C {lab_wire.sym} 180.0 80.0 0 0 {name=w18 sig_type=std_logic lab=Vamp_bias}
N 150 100.0 210 100.0 {}
C {lab_wire.sym} 180.0 100.0 0 0 {name=w19 sig_type=std_logic lab=VT}
C {devices/code_shown.sym} -400 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} -1100 330 0 0 {name=CONTROL only_toplevel=true
value="
.param vdd=3.3 code=9 vmon=1.65
* trim bits of 'code' (b3 = MSB), driven by Vtr3..Vtr0
.param b3='floor(code/8)-2*floor(code/16)' b2='floor(code/4)-2*floor(code/8)'
.param b1='floor(code/2)-2*floor(code/4)' b0='code-2*floor(code/2)'
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
