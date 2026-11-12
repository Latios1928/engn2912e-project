v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {neuron_pulse_tb: neuron_sized.sch driven by square current pulses into VMEM: amplitude p_ipk, width p_tpw,
one every p_tper from p_t0 (charge per pulse q = p_ipk * p_tpw). Counts output spikes and reports the input pulse
that first fires the neuron, input pulses per output spike, the VMEM step and leak droop of pulse 1, and the
effective membrane capacitance q / step. Run over many pulse settings by run_neuron_pulse.py (--pex: post-layout).} -1320 -720 0 0 0.3 0.3 {}
T {Bias voltages (absolute, to VSS)} -760 -560 0 0 0.25 0.25 {}
T {Input current pulses into VMEM
(ammeter VMEM reads them)} -560 -180 0 0 0.25 0.25 {}
N -600 -130 -600 -100 {lab=VSS}
N -660 -130 -660 -100 {lab=VDD}
N -660 -40 -660 0 {lab=VSS}
N -600 -40 -600 0 {lab=0}
N -470 -40 -470 0 {lab=preIN}
N -470 -130 -470 -100 {lab=VDD}
N -470 60 -470 90 {lab=VMEM}
N 290 -100 370 -100 {lab=VDD}
N 290 -120 370 -120 {lab=VSS}
N 290 -80 370 -80 {lab=spike}
N -80 40 -10 40 {lab=VT}
N -80 20 -10 20 {lab=Vamp_bias}
N -80 0 -10 0 {lab=VKdn}
N -80 -20 -10 -20 {lab=VKup}
N -80 -40 -10 -40 {lab=VIp}
N -80 -60 -10 -60 {lab=VK}
N -80 -80 -10 -80 {lab=Vlk}
N -80 -100 -10 -100 {lab=VNA}
N -80 -120 -10 -120 {lab=VMEM}
N -600 -500 -600 -470 {lab=VK}
N -660 -500 -660 -470 {lab=Vlk}
N -660 -410 -660 -370 {lab=VSS}
N -600 -410 -600 -370 {lab=VSS}
N -740 -500 -740 -470 {lab=VNA}
N -740 -410 -740 -370 {lab=VSS}
N -600 -320 -600 -290 {lab=VKdn}
N -660 -320 -660 -290 {lab=VKup}
N -660 -230 -660 -190 {lab=VSS}
N -600 -230 -600 -190 {lab=VSS}
N -740 -320 -740 -290 {lab=VIp}
N -740 -230 -740 -190 {lab=VSS}
N -410 -320 -410 -290 {lab=VT}
N -410 -230 -410 -190 {lab=VSS}
N -490 -320 -490 -290 {lab=Vamp_bias}
N -490 -230 -490 -190 {lab=VSS}
C {vsource.sym} -660 -70 0 0 {name=V1 value=\{p_vdd\} savecurrent=false}
C {vsource.sym} -600 -70 0 0 {name=V2 value=0 savecurrent=false}
C {lab_wire.sym} -600 -130 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -660 -130 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {gnd.sym} -600 0 0 0 {name=l1 lab=0}
C {lab_wire.sym} -660 0 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {isource.sym} -470 -70 0 0 {name=Iin value="pulse(0 \{p_ipk\} \{p_t0\} 10n 10n \{p_tpw\} \{p_tper\})" spice_ignore=false}
C {lab_wire.sym} -470 0 0 0 {name=p18 sig_type=std_logic lab=preIN}
C {lab_wire.sym} -470 -130 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {ammeter.sym} -470 30 0 0 {name=VMEM savecurrent=true spice_ignore=0}
C {lab_wire.sym} -470 90 0 0 {name=p9 sig_type=std_logic lab=VMEM}
C {neuron_sized.sym} 140 -40 0 0 {name=x1}
C {lab_wire.sym} 370 -120 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 370 -100 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 370 -80 0 0 {name=p3 sig_type=std_logic lab=spike}
C {lab_wire.sym} -80 -120 0 0 {name=p4 sig_type=std_logic lab=VMEM}
C {lab_wire.sym} -80 -100 0 0 {name=p5 sig_type=std_logic lab=VNA}
C {lab_wire.sym} -80 -80 0 0 {name=p6 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} -80 -60 0 0 {name=p11 sig_type=std_logic lab=VK}
C {lab_wire.sym} -80 -40 0 0 {name=p12 sig_type=std_logic lab=VIp}
C {lab_wire.sym} -80 -20 0 0 {name=p15 sig_type=std_logic lab=VKup}
C {lab_wire.sym} -80 0 0 0 {name=p16 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} -80 20 0 0 {name=p17 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} -80 40 0 0 {name=p20 sig_type=std_logic lab=VT}
C {vsource.sym} -660 -440 0 0 {name=Vlk value=\{p_vlk\} savecurrent=false}
C {vsource.sym} -600 -440 0 0 {name=VK value=\{p_vk\} savecurrent=false}
C {lab_wire.sym} -600 -500 0 0 {name=p21 sig_type=std_logic lab=VK}
C {lab_wire.sym} -660 -500 0 0 {name=p22 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} -660 -370 0 0 {name=p23 sig_type=std_logic lab=VSS}
C {vsource.sym} -740 -440 0 0 {name=VNA value=\{p_vna\} savecurrent=false}
C {lab_wire.sym} -740 -500 0 0 {name=p24 sig_type=std_logic lab=VNA}
C {lab_wire.sym} -740 -370 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {vsource.sym} -660 -260 0 0 {name=VKup value=\{p_vkup\} savecurrent=false}
C {vsource.sym} -600 -260 0 0 {name=VKdn value=\{p_vkdn\} savecurrent=false}
C {lab_wire.sym} -600 -320 0 0 {name=p26 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} -660 -320 0 0 {name=p27 sig_type=std_logic lab=VKup}
C {lab_wire.sym} -660 -190 0 0 {name=p28 sig_type=std_logic lab=VSS}
C {vsource.sym} -740 -260 0 0 {name=VIp value=\{p_vip\} savecurrent=false}
C {lab_wire.sym} -740 -320 0 0 {name=p29 sig_type=std_logic lab=VIp}
C {lab_wire.sym} -740 -190 0 0 {name=p30 sig_type=std_logic lab=VSS}
C {vsource.sym} -410 -260 0 0 {name=VT value=\{p_vt\} savecurrent=false}
C {lab_wire.sym} -410 -320 0 0 {name=p32 sig_type=std_logic lab=VT}
C {lab_wire.sym} -410 -190 0 0 {name=p33 sig_type=std_logic lab=VSS}
C {vsource.sym} -490 -260 0 0 {name=Vamp_bias value=\{p_vamp\} savecurrent=false}
C {lab_wire.sym} -490 -320 0 0 {name=p34 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} -490 -190 0 0 {name=p35 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -600 -370 0 0 {name=p36 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -600 -190 0 0 {name=p37 sig_type=std_logic lab=VSS}
C {devices/code_shown.sym} -1320 -560 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -1320 160 0 0 {name=TRAN_SIM only_toplevel=false
value="
* Biases of neuron_sized (as in neuron_nominal_tb). The pulse settings, p_tstop and
* p_tmax (maximum time step) are set per point by run_neuron_pulse.py.
.param p_vdd=3.3 p_ipk=20n p_tpw=10u p_tper=200u p_t0=50u p_tstop=5m p_tmax=100n
.param p_vlk=0.425 p_vamp=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
.csparam vdd_c=\{p_vdd\}
.csparam tstop_c=\{p_tstop\}
.csparam tmax_c=\{p_tmax\}
.csparam ipk_c=\{p_ipk\}
.csparam tpw_c=\{p_tpw\}
.csparam tper_c=\{p_tper\}
.csparam t0_c=\{p_t0\}
.ic v(VMEM)=0 v(spike)=0
.control
  save v(spike) v(VMEM) i(VMEM)
  tran 20n $&tstop_c 0 $&tmax_c uic
  let vsw = vdd_c/2

  * Output spikes: rising edges of spike through VDD/2 (a failed meas keeps -1)
  let n = 0
  let k = 1
  let t1 = -1
  let tlast = -1
  while k <= 2000
    let tk = -1
    meas tran tk when v(spike)=$&vsw rise=$&k
    if tk < 0
      break
    end
    if k = 1
      let t1 = tk
    end
    let tlast = tk
    let n = k
    let k = k + 1
  end

  * Input pulses that started at least 30 us before the end of the run (a later
  * one may not have had time to fire the neuron)
  let n_in = floor((tstop_c - 30u - t0_c)/tper_c) + 1
  * Input pulse during which (or after which) the first output spike came
  let n_first = 0
  if n >= 1
    let n_first = floor((t1 - t0_c)/tper_c) + 1
  end
  * Input pulses per output spike after the first one
  let n_per = 0
  if n >= 2
    let n_per = (tlast - t1)/((n - 1)*tper_c)
  end

  * Pulse 1: charge delivered, VMEM step, leak droop until just before pulse 2
  let q = ipk_c*tpw_c
  let ta = t0_c - 1u
  let tb = t0_c + tpw_c + 0.5u
  let tc = t0_c + tper_c - 0.5u
  meas tran v_a find v(VMEM) at=$&ta
  meas tran v_b find v(VMEM) at=$&tb
  meas tran v_c find v(VMEM) at=$&tc
  meas tran q1 integ i(VMEM) from=$&ta to=$&tb
  let dv1 = v_b - v_a
  let droop1 = v_b - v_c
  let c_eff = 0
  if dv1 > 1m
    let c_eff = q1/dv1
  end

  echo RES ipk=$&ipk_c
  echo RES tpw=$&tpw_c
  echo RES tper=$&tper_c
  echo RES q=$&q
  echo RES q1=$&q1
  echo RES n_in=$&n_in
  echo RES nspikes=$&n
  echo RES n_first=$&n_first
  echo RES n_per=$&n_per
  echo RES t_first=$&t1
  echo RES dv1=$&dv1
  echo RES droop1=$&droop1
  echo RES c_eff=$&c_eff
  echo neuron_pulse_tb: q $&q C per pulse, $&n output spikes for $&n_in input pulses, first after pulse $&n_first, then one per $&n_per pulses

  set wr_singlescale
  set wr_vecnames
  if $?batchmode = 0
    wrdata /foss/designs/engn2912e-project/analog/testbenches/neuron/results/neuron_pulse_tb.txt v(VMEM) v(spike) i(VMEM)
    plot v(VMEM) v(spike) title 'neuron_pulse_tb: membrane and spike' xlabel 't (s)' ylabel 'V'
    plot i(VMEM) title 'neuron_pulse_tb: input current' xlabel 't (s)' ylabel 'A'
  else
    wrdata neuron_pulse_tb.txt v(VMEM) v(spike) i(VMEM)
  end
.endc
"}
