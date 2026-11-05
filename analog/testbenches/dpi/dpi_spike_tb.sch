v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dpi_spike_tb: response to input spikes. x1 gets one Iw pulse (width tpw) at 1 ms; x2 gets a
pulse train at rate from 1 ms on. Measures the single-spike EPSC (peak, charge, equivalent step on a
cmem membrane, decay constant) and, for the train, the mean Isyn, ripple, and the ratio of the mean
to (single-spike charge x rate), which is 1 for a linear synapse.} -1100 -900 0 0 0.3 0.3 {}
T {x1: single spike} -330 -360 0 0 0.25 0.25 {}
T {x2: spike train at rate} -330 -160 0 0 0.25 0.25 {}
N -1100 -360 -1100 -330 {lab=VDD}
N -1100 -270 -1100 -240 {lab=0}
N -980 -360 -980 -330 {lab=Vthr}
N -980 -270 -980 -240 {lab=0}
N -860 -360 -860 -330 {lab=VDD}
N -860 -270 -860 -240 {lab=VT}
N -740 -360 -740 -330 {lab=Isum1}
N -740 -270 -740 -240 {lab=0}
N -620 -360 -620 -330 {lab=Isyn1}
N -620 -270 -620 -240 {lab=0}
N -740 -160 -740 -130 {lab=Isum2}
N -740 -70 -740 -40 {lab=0}
N -620 -160 -620 -130 {lab=Isyn2}
N -620 -70 -620 -40 {lab=0}
N -50 -320 -10 -320 {lab=VDD}
N -390 -320 -350 -320 {lab=Vthr}
N -50 -300 -10 -300 {lab=Isyn1}
N -390 -280 -350 -280 {lab=Isum1}
N -390 -300 -350 -300 {lab=VT}
N -50 -120 -10 -120 {lab=VDD}
N -390 -120 -350 -120 {lab=Vthr}
N -50 -100 -10 -100 {lab=Isyn2}
N -390 -80 -350 -80 {lab=Isum2}
N -390 -100 -350 -100 {lab=VT}
C {vsource.sym} -1100 -300 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {lab_wire.sym} -1100 -360 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} -1100 -240 0 0 {name=lp2 lab=0}
C {vsource.sym} -980 -300 0 0 {name=Vthr value=\{vthr\} savecurrent=false}
C {lab_wire.sym} -980 -360 0 0 {name=p3 sig_type=std_logic lab=Vthr}
C {gnd.sym} -980 -240 0 0 {name=lp4 lab=0}
C {vsource.sym} -860 -300 0 0 {name=Vtau value=\{vtau\} savecurrent=false}
C {lab_wire.sym} -860 -360 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -860 -240 0 0 {name=p6 sig_type=std_logic lab=VT}
C {isource.sym} -740 -300 0 0 {name=Iw1 value="pulse(0 \{iw\} 1m 10n 10n \{tpw\} 1)"}
C {lab_wire.sym} -740 -360 0 0 {name=p7 sig_type=std_logic lab=Isum1}
C {gnd.sym} -740 -240 0 0 {name=lp8 lab=0}
C {ammeter.sym} -620 -300 0 0 {name=VIsyn1 savecurrent=true spice_ignore=0}
C {lab_wire.sym} -620 -360 0 0 {name=p9 sig_type=std_logic lab=Isyn1}
C {gnd.sym} -620 -240 0 0 {name=lp10 lab=0}
C {isource.sym} -740 -100 0 0 {name=Iw2 value="pulse(0 \{iw\} 1m 10n 10n \{tpw\} \{1/rate\})"}
C {lab_wire.sym} -740 -160 0 0 {name=p11 sig_type=std_logic lab=Isum2}
C {gnd.sym} -740 -40 0 0 {name=lp12 lab=0}
C {ammeter.sym} -620 -100 0 0 {name=VIsyn2 savecurrent=true spice_ignore=0}
C {lab_wire.sym} -620 -160 0 0 {name=p13 sig_type=std_logic lab=Isyn2}
C {gnd.sym} -620 -40 0 0 {name=lp14 lab=0}
C {DPI.sym} -200 -300 0 0 {name=x1}
C {lab_wire.sym} -10 -320 0 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -390 -320 0 0 {name=p16 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -10 -300 0 0 {name=p17 sig_type=std_logic lab=Isyn1}
C {lab_wire.sym} -390 -280 0 0 {name=p18 sig_type=std_logic lab=Isum1}
C {lab_wire.sym} -390 -300 0 0 {name=p19 sig_type=std_logic lab=VT}
C {DPI.sym} -200 -100 0 0 {name=x2}
C {lab_wire.sym} -10 -120 0 0 {name=p20 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -390 -120 0 0 {name=p21 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -10 -100 0 0 {name=p22 sig_type=std_logic lab=Isyn2}
C {lab_wire.sym} -390 -80 0 0 {name=p23 sig_type=std_logic lab=Isum2}
C {lab_wire.sym} -390 -100 0 0 {name=p24 sig_type=std_logic lab=VT}
C {code_shown.sym} -1100 80 0 0 {name=TRAN_SIM only_toplevel=false
value="
* Reference operating point (see analog/testbenches/README.md)
* cmem is only used to convert charge per spike into a membrane step (neuron_5khz Cmem)
.param vdd=3.3 vthr=2.9 vtau=0.40 iw=5n tpw=100u rate=1k cmem=0.86p
.csparam iw_c=\{iw\}
.csparam tpw_c=\{tpw\}
.csparam rate_c=\{rate\}
.csparam cmem_c=\{cmem\}
.control
  save all
  set wr_singlescale
  set wr_vecnames
  tran 0.5u 21m 0 1u
  let isyn1 = i(VIsyn1)
  let isyn2 = i(VIsyn2)

  * Single spike (x1)
  meas tran i_base find isyn1 at=0.9m
  meas tran ipk1 max isyn1 from=1m to=11m
  meas tran q1 integ isyn1 from=1m to=11m
  let q1 = q1 - i_base*10m
  let dv_mem = q1/cmem_c
  let t_end = 1m + tpw_c
  let l37 = i_base + 0.3679*(ipk1 - i_base)
  meas tran t37 when isyn1=$&l37 fall=1 td=$&t_end
  let tau_epsc = t37 - t_end

  * Spike train (x2), measured once settled
  meas tran iavg2 avg isyn2 from=11m to=21m
  meas tran imax2 max isyn2 from=11m to=21m
  meas tran imin2 min isyn2 from=11m to=21m
  let ripple = (imax2 - imin2)/iavg2
  let lin_rate = (iavg2 - i_base)/(q1*rate_c)
  let pk_ratio = imax2/ipk1

  echo RES ipk1=$&ipk1
  echo RES q1=$&q1
  echo RES dv_mem=$&dv_mem
  echo RES tau_epsc=$&tau_epsc
  echo RES iavg2=$&iavg2
  echo RES ripple=$&ripple
  echo RES lin_rate=$&lin_rate
  echo RES pk_ratio=$&pk_ratio

  wrdata dpi_spike.txt isyn1 isyn2
  if $?batchmode = 0
    plot isyn1 isyn2 title 'Single spike (isyn1) and spike train (isyn2)' ylabel 'Isyn (A)'
    plot Isum1 Isum2 title 'Inputs for both'
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
