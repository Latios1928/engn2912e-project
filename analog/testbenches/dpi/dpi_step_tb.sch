v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dpi_step_tb: step response of DPI.sch. Iw = iw from 1 ms to 11 ms, then 0 until 31 ms.
Measures the steady-state gain Isyn/Iw, rise time constant (63 %), 10-90 % rise time,
decay time constant (37 %), whether the decay is exponential (2-tau point / tau),
the residual current 19 ms after release, and the lowest V(Isum) seen by the tail current.} -1100 -800 0 0 0.3 0.3 {}
T {Iw sunk from Isum (stands in for the DAC)} -800 -200 0 0 0.25 0.25 {}
N -1100 -360 -1100 -330 {lab=VDD}
N -1100 -270 -1100 -240 {lab=0}
N -980 -360 -980 -330 {lab=Vthr}
N -980 -270 -980 -240 {lab=0}
N -860 -360 -860 -330 {lab=VDD}
N -860 -270 -860 -240 {lab=VT}
N -740 -360 -740 -330 {lab=Isum}
N -740 -270 -740 -240 {lab=0}
N -620 -360 -620 -330 {lab=Isyn}
N -620 -270 -620 -240 {lab=0}
N -50 -320 -10 -320 {lab=VDD}
N -390 -320 -350 -320 {lab=Vthr}
N -50 -300 -10 -300 {lab=Isyn}
N -390 -280 -350 -280 {lab=Isum}
N -390 -300 -350 -300 {lab=VT}
C {vsource.sym} -1100 -300 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {lab_wire.sym} -1100 -360 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} -1100 -240 0 0 {name=lp2 lab=0}
C {vsource.sym} -980 -300 0 0 {name=Vthr value=\{vthr\} savecurrent=false}
C {lab_wire.sym} -980 -360 0 0 {name=p3 sig_type=std_logic lab=Vthr}
C {gnd.sym} -980 -240 0 0 {name=lp4 lab=0}
C {vsource.sym} -860 -300 0 0 {name=Vtau value=\{vtau\} savecurrent=false}
C {lab_wire.sym} -860 -360 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -860 -240 0 0 {name=p6 sig_type=std_logic lab=VT}
C {isource.sym} -740 -300 0 0 {name=Iw value="pulse(0 \{iw\} 1m 100n 100n 10m 100)"}
C {lab_wire.sym} -740 -360 0 0 {name=p7 sig_type=std_logic lab=Isum}
C {gnd.sym} -740 -240 0 0 {name=lp8 lab=0}
C {ammeter.sym} -620 -300 0 0 {name=VIsyn savecurrent=true spice_ignore=0}
C {lab_wire.sym} -620 -360 0 0 {name=p9 sig_type=std_logic lab=Isyn}
C {gnd.sym} -620 -240 0 0 {name=lp10 lab=0}
C {DPI.sym} -200 -300 0 0 {name=x1}
C {lab_wire.sym} -10 -320 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -390 -320 0 0 {name=p12 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -10 -300 0 0 {name=p13 sig_type=std_logic lab=Isyn}
C {lab_wire.sym} -390 -280 0 0 {name=p14 sig_type=std_logic lab=Isum}
C {lab_wire.sym} -390 -300 0 0 {name=p15 sig_type=std_logic lab=VT}
C {code_shown.sym} -1100 -120 0 0 {name=TRAN_SIM only_toplevel=false
value="
* Reference operating point (see analog/testbenches/README.md)
.param vdd=3.3 vthr=2.9 vtau=0.40 iw=5n
.csparam iw_c=\{iw\}
.control
  save all
  set wr_singlescale
  set wr_vecnames
  tran 2u 31m 0 10u
  let isyn = i(VIsyn)

  meas tran i_base find isyn at=0.9m
  meas tran i_ss avg isyn from=10.5m to=11m
  meas tran i_ss_prev avg isyn from=10m to=10.5m
  let settle_err = abs(i_ss - i_ss_prev)/i_ss
  let gain = i_ss/iw_c

  * Rise
  let l10 = i_base + 0.1*(i_ss - i_base)
  let l63 = i_base + 0.6321*(i_ss - i_base)
  let l90 = i_base + 0.9*(i_ss - i_base)
  meas tran t10 when isyn=$&l10 rise=1 td=1m
  meas tran t63 when isyn=$&l63 rise=1 td=1m
  meas tran t90 when isyn=$&l90 rise=1 td=1m
  let tau_rise = t63 - 1m
  let t_rise = t90 - t10

  * Decay after Iw turns off at 11 ms
  meas tran i_off find isyn at=11.0001m
  let l37 = i_base + 0.3679*(i_off - i_base)
  let l14 = i_base + 0.1353*(i_off - i_base)
  meas tran t37 when isyn=$&l37 fall=1 td=11.0001m
  meas tran t14 when isyn=$&l14 fall=1 td=11.0001m
  let tau_fall = t37 - 11.0001m
  let exp_ratio = (t14 - 11.0001m)/(2*tau_fall)
  meas tran i_end find isyn at=30m
  let residual = i_end/i_off

  * Headroom left for the DAC tail current, and supply current while on
  meas tran vsum_min min v(Isum) from=1.1m to=11m
  meas tran ivdd_on avg i(V1) from=10.5m to=11m
  let ivdd_on = -ivdd_on

  echo RES i_ss=$&i_ss
  echo RES gain=$&gain
  echo RES settle_err=$&settle_err
  echo RES tau_rise=$&tau_rise
  echo RES t_rise=$&t_rise
  echo RES tau_fall=$&tau_fall
  echo RES exp_ratio=$&exp_ratio
  echo RES residual=$&residual
  echo RES vsum_min=$&vsum_min
  echo RES ivdd_on=$&ivdd_on

  wrdata dpi_step.txt isyn v(Isum) v(x1.net1)
  if $?batchmode = 0
    plot isyn title 'DPI step response' xlabel 't (s)' ylabel 'Isyn (A)'
    plot v(Isum) v(x1.net1) title 'Tail node and Vsyn' ylabel 'V'

  end
.endc
"}
C {devices/code_shown.sym} -1100 -560 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
