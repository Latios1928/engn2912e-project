v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dpi_pulse_tb: the synapses driven by DAC-like current pulses at the network's operating point. p_npulse pulses of p_code x 15 nA, p_tpw wide, every p_tper, are sunk from the tails of x1 (excitatory DPI_sized; --cell DPI: min-size DPI) and x2 (inhibitory DPI_inh); both outputs are held at p_vmem. Measures the charge each output delivers (excitatory) or removes (inhibitory) per input pulse and in total, its peak current and decay time, and the lowest tail voltage. Run by run_dpi_pulse.py.} -900 -700 0 0 0.3 0.3 {}
C {DPI_sized.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -20 0 0 {name=l1 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -150 0 0 0 {name=l2 sig_type=std_logic lab=VT_e}
C {lab_pin.sym} -150 20 0 0 {name=l3 sig_type=std_logic lab=Isum_e}
C {lab_pin.sym} 150 -20 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 0 0 1 {name=l5 sig_type=std_logic lab=Out_e}
C {DPI_inh.sym} 0 200 0 0 {name=x2}
C {lab_pin.sym} -150 180 0 0 {name=l6 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -150 200 0 0 {name=l7 sig_type=std_logic lab=VT_i}
C {lab_pin.sym} -150 220 0 0 {name=l8 sig_type=std_logic lab=Isum_i}
C {lab_pin.sym} 150 180 0 1 {name=l9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 200 0 1 {name=l10 sig_type=std_logic lab=Out_i}
C {devices/code_shown.sym} -900 -520 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {devices/code_shown.sym} -900 -380 0 0 {name=SOURCES only_toplevel=false
value="
.param p_vdd=3.3 p_vthr=2.785 p_vtau=0.5096 p_vtau_i=0.5096
* gmin 1e-16 S: the default (1e-12 S) adds pA-level currents to every node, as large as
* the smallest DPI currents measured here
.options gmin=1e-16
Vdd VDD 0 \{p_vdd\}
Vthr Vthr 0 \{p_vthr\}
* tau biases: VT = VDD - vtau (vtau is the pFET's source-gate voltage)
Vtau VDD VT_e \{p_vtau\}
Vtaui VDD VT_i \{p_vtau_i\}
.param p_code=1 p_iunit=15n p_tpw=10u p_tper=200u p_t0=100u p_npulse=5 p_vmem=0.5 p_tdecay=3m p_tmax=0.5u
.csparam t0_c=\{p_t0\}
.csparam tper_c=\{p_tper\}
.csparam tpw_c=\{p_tpw\}
.csparam np_c=\{p_npulse\}
.csparam tdecay_c=\{p_tdecay\}
.csparam tmax_c=\{p_tmax\}
.csparam qin_c=\{p_code*p_iunit*p_tpw\}
* Input: p_npulse current pulses of code x 15 nA, p_tpw wide, every p_tper, sunk from each tail
Iwe Isum_e 0 pulse(0 \{p_code*p_iunit\} \{p_t0\} 10n 10n \{p_tpw\} \{p_tper\} \{p_npulse\})
Iwi Isum_i 0 pulse(0 \{p_code*p_iunit\} \{p_t0\} 10n 10n \{p_tpw\} \{p_tper\} \{p_npulse\})
* Outputs held at the membrane voltage p_vmem
Voe Out_e 0 \{p_vmem\}
Voi Out_i 0 \{p_vmem\}
"}
C {devices/code_shown.sym} 400 -380 0 0 {name=ANALYSIS only_toplevel=false
value="
.control
  save i(voe) i(voi) v(Isum_e) v(Isum_i)
  let tlast = t0_c + np_c*tper_c
  let tstop = tlast + tdecay_c
  tran 10n $&tstop 0 $&tmax_c
  let ie = i(voe)
  let ii = -i(voi)
  * idle (before the first pulse), removed from every charge
  let ta = t0_c - 50u
  let tb = t0_c - 1u
  meas tran ie0 avg ie from=$&ta to=$&tb
  meas tran ii0 avg ii from=$&ta to=$&tb
  * charge in each window: pulse k until pulse k+1 (the last one until the end of the run)
  let k = 1
  while k <= np_c
    let ta = t0_c + (k - 1)*tper_c
    let tb = ta + tper_c
    if k = np_c
      let tb = tstop
    end
    meas tran qe integ ie from=$&ta to=$&tb
    meas tran qi integ ii from=$&ta to=$&tb
    let qe = qe - ie0*(tb - ta)
    let qi = qi - ii0*(tb - ta)
    echo RES qe$&k=$&qe
    echo RES qi$&k=$&qi
    let k = k + 1
  end
  meas tran qe_tot integ ie from=$&t0_c to=$&tstop
  meas tran qi_tot integ ii from=$&t0_c to=$&tstop
  let qe_tot = qe_tot - ie0*(tstop - t0_c)
  let qi_tot = qi_tot - ii0*(tstop - t0_c)
  meas tran pe max ie from=$&t0_c to=$&tstop
  meas tran pi max ii from=$&t0_c to=$&tstop
  * decay after the last input: time to fall to 37 % of the current at the end of the last pulse
  let tl = t0_c + (np_c - 1)*tper_c + tpw_c
  meas tran ie_l find ie at=$&tl
  meas tran ii_l find ii at=$&tl
  let le = 0.3679*ie_l
  let li = 0.3679*ii_l
  let te37 = -1
  let ti37 = -1
  meas tran te37 when ie=$&le fall=last
  meas tran ti37 when ii=$&li fall=last
  let tau_e = te37 - tl
  let tau_i = ti37 - tl
  meas tran vsum_e_min min v(Isum_e) from=$&t0_c to=$&tstop
  meas tran vsum_i_min min v(Isum_i) from=$&t0_c to=$&tstop
  echo RES npulse=$&np_c
  echo RES qin=$&qin_c
  echo RES qe_tot=$&qe_tot
  echo RES qi_tot=$&qi_tot
  echo RES ie_idle=$&ie0
  echo RES ii_idle=$&ii0
  echo RES pe=$&pe
  echo RES pi=$&pi
  echo RES tau_e=$&tau_e
  echo RES tau_i=$&tau_i
  echo RES vsum_e_min=$&vsum_e_min
  echo RES vsum_i_min=$&vsum_i_min
  echo dpi_pulse_tb: done
  set wr_singlescale
  set wr_vecnames
  if $?batchmode = 0
    wrdata /foss/designs/engn2912e-project/analog/testbenches/dpi/results/dpi_pulse_tb.txt ie ii
    plot ie ii title 'dpi_pulse_tb: excitatory output, inhibitory output (A)'
  else
    wrdata dpi_pulse_tb.txt ie ii
  end
.endc
"}
