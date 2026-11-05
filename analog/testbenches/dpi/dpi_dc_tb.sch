v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dpi_dc_tb: DC characterization of DPI.sch with an ideal tail current Iw = 10^V(lg).
Measures Isyn at the reference point, Isyn vs Iw (100 pA to 100 nA, log-log slope),
Isyn vs Vthr, Isyn vs Vtau (Vsg of M3), Isyn vs VDD with Vthr fixed, and the leakage floor at Iw = 0.
Results print as RES lines and curves go to dpi_dc_*.txt in the simulation directory.} -1100 -800 0 0 0.3 0.3 {}
T {Iw = 10^V(lg), sunk from Isum} -700 -200 0 0 0.25 0.25 {}
N -1100 -360 -1100 -330 {lab=VDD}
N -1100 -270 -1100 -240 {lab=0}
N -980 -360 -980 -330 {lab=Vthr}
N -980 -270 -980 -240 {lab=0}
N -860 -360 -860 -330 {lab=VDD}
N -860 -270 -860 -240 {lab=VT}
N -740 -360 -740 -330 {lab=lg}
N -740 -270 -740 -240 {lab=0}
N -620 -360 -620 -330 {lab=Isum}
N -620 -270 -620 -240 {lab=0}
N -500 -360 -500 -330 {lab=Isyn}
N -500 -270 -500 -240 {lab=0}
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
C {vsource.sym} -740 -300 0 0 {name=Vlg value=\{log10(iw)\} savecurrent=false}
C {lab_wire.sym} -740 -360 0 0 {name=p7 sig_type=std_logic lab=lg}
C {gnd.sym} -740 -240 0 0 {name=lp8 lab=0}
C {bsource.sym} -620 -300 0 0 {name=Biw VAR=I FUNC="pow(10,V(lg))" m=1}
C {lab_wire.sym} -620 -360 0 0 {name=p9 sig_type=std_logic lab=Isum}
C {gnd.sym} -620 -240 0 0 {name=lp10 lab=0}
C {ammeter.sym} -500 -300 0 0 {name=VIsyn savecurrent=true spice_ignore=0}
C {lab_wire.sym} -500 -360 0 0 {name=p11 sig_type=std_logic lab=Isyn}
C {gnd.sym} -500 -240 0 0 {name=lp12 lab=0}
C {DPI.sym} -200 -300 0 0 {name=x1}
C {lab_wire.sym} -10 -320 0 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -390 -320 0 0 {name=p14 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -10 -300 0 0 {name=p15 sig_type=std_logic lab=Isyn}
C {lab_wire.sym} -390 -280 0 0 {name=p16 sig_type=std_logic lab=Isum}
C {lab_wire.sym} -390 -300 0 0 {name=p17 sig_type=std_logic lab=VT}
C {code_shown.sym} -1100 -120 0 0 {name=TRAN_SIM only_toplevel=false
value="
* Reference operating point (see analog/testbenches/README.md)
.param vdd=3.3 vthr=2.9 vtau=0.40 iw=5n
.csparam iw_c=\{iw\}
.csparam vthr_c=\{vthr\}
.csparam vtau_c=\{vtau\}
.csparam vdd_c=\{vdd\}
.control
  save all
  set wr_singlescale
  set wr_vecnames
  let lg_nom = log10(iw_c)
  let lg_lo = lg_nom - 1
  let lg_hi = lg_nom + 1

  * 0) Operating point at the reference bias
  op
  let isyn_op = i(VIsyn)
  let gain_op = isyn_op/iw_c
  let ivdd_op = -i(V1)
  let vsum_op = v(Isum)
  let vsyn_op = v(x1.net1)
  echo RES isyn_op=$&isyn_op
  echo RES gain_op=$&gain_op
  echo RES ivdd_op=$&ivdd_op
  echo RES vsum_op=$&vsum_op
  echo RES vsyn_op=$&vsyn_op

  * 1) Isyn vs Iw, 100 pA to 100 nA
  dc Vlg -10 -7 0.02
  let iw = 10^v(lg)
  let isyn = i(VIsyn)
  meas dc isyn_lo find isyn at=$&lg_lo
  meas dc isyn_hi find isyn at=$&lg_hi
  let slope_iw = log10(isyn_hi/isyn_lo)/2
  echo RES slope_iw=$&slope_iw
  wrdata dpi_dc_iw.txt iw isyn v(Isum) v(x1.net1)
  if $?batchmode = 0
    plot isyn vs iw loglog title 'Isyn vs Iw' xlabel 'Iw (A)' ylabel 'Isyn (A)'
  end

  * 2) Isyn vs Vthr
  dc Vthr 2.6 3.2 2m
  let isyn = i(VIsyn)
  let va = vthr_c - 0.05
  let vb = vthr_c + 0.05
  meas dc i_a find isyn at=$&va
  meas dc i_b find isyn at=$&vb
  let mvdec_vthr = 100/log10(i_a/i_b)
  echo RES mvdec_vthr=$&mvdec_vthr
  wrdata dpi_dc_vthr.txt isyn
  if $?batchmode = 0
    plot ylog isyn title 'Isyn vs Vthr' xlabel 'Vthr (V)' ylabel 'Isyn (A)'
  end

  * 3) Isyn vs Vtau (Vsg of the tau pFET M3)
  dc Vtau 0.30 0.50 1m
  let isyn = i(VIsyn)
  let va = vtau_c - 0.05
  let vb = vtau_c + 0.05
  meas dc i_a find isyn at=$&va
  meas dc i_b find isyn at=$&vb
  let mvdec_vtau = 100/log10(i_a/i_b)
  echo RES mvdec_vtau=$&mvdec_vtau
  wrdata dpi_dc_vtau.txt isyn
  if $?batchmode = 0
    plot ylog isyn title 'Isyn vs Vtau' xlabel 'Vtau = Vsg(M3) (V)' ylabel 'Isyn (A)'
  end

  * 4) Isyn vs VDD with Vthr fixed (Vtau follows VDD)
  dc V1 3.0 3.6 5m
  let isyn = i(VIsyn)
  let va = vdd_c - 0.1
  let vb = vdd_c + 0.1
  meas dc i_a find isyn at=$&va
  meas dc i_b find isyn at=$&vb
  let mvdec_vdd = 200/log10(i_b/i_a)
  echo RES mvdec_vdd=$&mvdec_vdd
  wrdata dpi_dc_vdd.txt isyn
  if $?batchmode = 0
    plot ylog isyn title 'Isyn vs VDD (Vthr fixed)' xlabel 'VDD (V)' ylabel 'Isyn (A)'
  end

  * 5) Leakage floor with no input current
  alter Vlg dc=-20
  op
  let i_leak = i(VIsyn)
  echo RES i_leak=$&i_leak
.endc
"}
C {devices/code_shown.sym} -1100 -560 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
