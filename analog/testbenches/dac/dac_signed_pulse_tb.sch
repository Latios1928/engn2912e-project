v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dac_signed_pulse_tb: DAC_signed.sch switched by its enable, as in the network.
Vb from Iref (p_iref) into a diode-connected unit current source; weight code p_code and sign p_s held static;
both outputs held by voltage sources (Isum_e at p_ve, Isum_i at p_vi). en: p_npulse pulses of width p_tpw every p_tper
from p_t0, edges p_tr / p_tf (run_dac_signed_pulse.py can replace this source by a real neuron spike shape).
Measures the charge each pulse delivers to the selected output and to the other one, the on-current and the
settling time. Prints RES lines; run_dac_signed_pulse.py runs it over codes, widths and spike shapes (--pex).} -820 -560 0 0 0.3 0.3 {}
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
.param p_vdd=3.3 p_iref=14.42n p_ve=2.5 p_vi=2.5 p_code=15 p_s=0
.param p_tpw=10u p_tper=200u p_t0=50u p_tr=10n p_tf=10n p_npulse=5 p_tmax=20n
* See dac_signed_static_tb: the default gmin (1e-12 S) adds 2.5 pA per node.
.options gmin=1e-16
.csparam vdd_c=\{p_vdd\}
.csparam s_c=\{p_s\}
.csparam tpw_c=\{p_tpw\}
.csparam tper_c=\{p_tper\}
.csparam t0_c=\{p_t0\}
.csparam np_c=\{p_npulse\}
.csparam tmax_c=\{p_tmax\}
.csparam code_c=\{p_code\}
Vdd VDD 0 \{p_vdd\}
* DAC unit current: Iref into a diode-connected copy of the unit current source (1 um / 8 um)
Iref VDD Vb \{p_iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
* Enable: ideal pulses (run_dac_signed_pulse.py --suite spike replaces this line)
Ven en 0 pulse(0 \{p_vdd\} \{p_t0\} \{p_tr\} \{p_tf\} \{p_tpw\} \{p_tper\})
* Static weight code (0..15) and sign (0/1), decoded into logic levels
Vcode code 0 \{p_code\}
Bw0 w[0] 0 V = \{p_vdd\}*(floor(v(code)+0.5) - 2*floor(floor(v(code)+0.5)/2))
Bw1 w[1] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/2) - 2*floor(floor(v(code)+0.5)/4))
Bw2 w[2] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/4) - 2*floor(floor(v(code)+0.5)/8))
Bw3 w[3] 0 V = \{p_vdd\}*(floor(floor(v(code)+0.5)/8) - 2*floor(floor(v(code)+0.5)/16))
Vs s 0 \{p_vdd*p_s\}
* Outputs held at fixed voltages (stand-ins for the DPI tails); current in = -i(V...)
Vhe Ie 0 \{p_ve\}
Vhi Ii 0 \{p_vi\}
"}
C {code_shown.sym} -820 40 0 0 {name=ANALYSIS only_toplevel=false
value="
.control
  save i(vhe) i(vhi) v(en)
  let tstop = t0_c + np_c*tper_c
  tran 10n $&tstop 0 $&tmax_c
  let ie = -i(vhe)
  let ii = -i(vhi)
  * selected output (s = 0: Isum_e, s = 1: Isum_i) and the other one
  let isel = ie*(1 - s_c) + ii*s_c
  let ioth = ii*(1 - s_c) + ie*s_c

  * Idle currents before the first pulse (leakage), removed from each window
  let ta = t0_c - 20u
  let tb = t0_c - 1u
  meas tran i_idle avg isel from=$&ta to=$&tb
  meas tran o_idle avg ioth from=$&ta to=$&tb

  * Charge of each pulse: window from 1 us before it to 1 us before the next
  let k = 1
  while k <= np_c
    let ta = t0_c + (k - 1)*tper_c - 1u
    let tb = ta + tper_c
    meas tran qs integ isel from=$&ta to=$&tb
    meas tran qo integ ioth from=$&ta to=$&tb
    let q = qs - i_idle*tper_c
    let qx = qo - o_idle*tper_c
    echo RES q$&k=$&q
    echo RES qo$&k=$&qx
    let k = k + 1
  end

  * On-current in the middle of the first pulse (ideal pulses), and settling:
  * time from the enable edge until the current is within 1 % of it
  let ta = t0_c + 0.6*tpw_c
  let tb = t0_c + 0.9*tpw_c
  meas tran i_on avg isel from=$&ta to=$&tb
  let lvl = 0.99*i_on
  let t99 = -1
  meas tran t99 when isel=$&lvl rise=1 td=$&t0_c
  let t_settle = t99 - t0_c
  meas tran i_peak max isel from=$&t0_c to=$&tstop
  meas tran en_max max v(en)
  echo RES npulse=$&np_c
  echo RES code=$&code_c
  echo RES s=$&s_c
  echo RES tpw=$&tpw_c
  echo RES i_idle=$&i_idle
  echo RES i_on=$&i_on
  echo RES i_peak=$&i_peak
  echo RES t_settle=$&t_settle
  echo RES en_max=$&en_max
  echo dac_signed_pulse_tb: done

  set wr_singlescale
  set wr_vecnames
  if $?batchmode = 0
    wrdata /foss/designs/engn2912e-project/analog/testbenches/dac/results/dac_signed_pulse_tb.txt isel ioth v(en)
    plot isel ioth title 'dac_signed_pulse_tb: current into the selected and the other output' ylabel 'A'
    plot v(en) title 'enable' ylabel 'V'
  else
    wrdata dac_signed_pulse_tb.txt isel ioth v(en)
  end
.endc
"}

