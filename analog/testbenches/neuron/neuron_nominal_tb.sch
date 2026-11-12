v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {neuron_nominal_tb: nominal check of neuron_sized.sch against analog/neuron/sizing_context.txt.
Constant input current p_iin (9.5 nA) into VMEM, VDD 3.3 V, tt, 27 C, VMEM and spike start at 0 V.
Measures period, spike width, refractory time, spike peak, reset level and average power on spikes 3-7
(definitions as in tools/analog_API_infrastructure/configs_sized/sim.yaml) and prints PASS/FAIL per spec.} -1320 -720 0 0 0.3 0.3 {}
T {Bias voltages (absolute, to VSS)} -760 -560 0 0 0.25 0.25 {}
T {Input current into VMEM
(ammeter VMEM reads it)} -560 -180 0 0 0.25 0.25 {}
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
C {isource.sym} -470 -70 0 0 {name=Iin value=\{p_iin\} spice_ignore=false}
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
* Operating point of neuron_sized (analog/Analog_AI_Documentation.md entry 42).
* Parameters start with p_ because a .param named like a net (VT, Vlk, ...) can
* rename that net on the instance line (see mixed/README.md, Pitfalls).
.param p_vdd=3.3 p_iin=9.5n p_tstop=1.8m
.param p_vlk=0.425 p_vamp=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
.csparam vdd_c=\{p_vdd\}
.csparam tstop_c=\{p_tstop\}
.ic v(VMEM)=0 v(spike)=0
.control
  save v(spike) v(VMEM) i(V1) i(VMEM)
  tran 20n $&tstop_c 0 20n uic

  * Spike edges at VDD/2. Spikes 1-2 start from the initial condition, so
  * everything is measured from spike 3 on. A failed measurement keeps -1.
  let vsw = vdd_c/2
  let t3 = -1
  let t4 = -1
  let t7 = -1
  let tf3 = -1
  let trst = -1
  let trel = -1
  meas tran t3 when v(spike)=$&vsw rise=3
  meas tran t4 when v(spike)=$&vsw rise=4
  meas tran t7 when v(spike)=$&vsw rise=7
  meas tran tf3 when v(spike)=$&vsw fall=3

  let nfail = 0
  if t7 < 0
    echo
    echo neuron_nominal_tb: FAIL, fewer than 7 spikes in $&tstop_c s, nothing measured
    echo RES fired7=0
  else
    echo RES fired7=1

    * period: mean spike-to-spike time over spikes 3-7
    let period = (t7 - t3)/4
    * t_spike: time v(spike) stays above VDD/2, spike 3
    let t_spike = tf3 - t3
    * v_spike_max / v_reset: highest spike and lowest VMEM from spike 3 to spike 4
    meas tran v_spike_max max v(spike) from=$&t3 to=$&t4
    meas tran v_reset min v(VMEM) from=$&t3 to=$&t4
    * t_refr: end of reset (VMEM falls below 10 % VDD) until VMEM is free again
    * (rises 10 mV above v_reset). t_refr_post counts from the spike's falling edge.
    let v10 = 0.1*vdd_c
    let vrel = v_reset + 0.01
    meas tran trst when v(VMEM)=$&v10 fall=1 td=$&t3
    meas tran trel when v(VMEM)=$&vrel rise=1 td=$&tf3
    let t_refr = trel - trst
    let t_refr_post = trel - tf3
    * p_avg: supply power over spikes 3-7, including the input current (fed from VDD)
    meas tran i_avg avg i(V1) from=$&t3 to=$&t7
    let p_avg = -i_avg*vdd_c
    meas tran i_in avg i(VMEM) from=$&t3 to=$&t7

    echo RES period=$&period
    echo RES t_spike=$&t_spike
    echo RES t_refr=$&t_refr
    echo RES t_refr_post=$&t_refr_post
    echo RES v_spike_max=$&v_spike_max
    echo RES v_reset=$&v_reset
    echo RES p_avg=$&p_avg
    echo RES i_in=$&i_in

    * Targets from analog/neuron/sizing_context.txt
    let x = period*1e6
    if (period >= 190e-6) & (period <= 210e-6)
      echo CHECK period       $&x us     target 190 to 210 us   PASS
    else
      echo CHECK period       $&x us     target 190 to 210 us   FAIL
      let nfail = nfail + 1
    end
    let x = t_spike*1e6
    if (t_spike >= 9e-6) & (t_spike <= 11e-6)
      echo CHECK t_spike      $&x us     target 9 to 11 us      PASS
    else
      echo CHECK t_spike      $&x us     target 9 to 11 us      FAIL
      let nfail = nfail + 1
    end
    let x = t_refr*1e6
    if (t_refr >= 12e-6) & (t_refr <= 15e-6)
      echo CHECK t_refr       $&x us     target 12 to 15 us     PASS
    else
      echo CHECK t_refr       $&x us     target 12 to 15 us     FAIL
      let nfail = nfail + 1
    end
    if v_spike_max >= 2.97
      echo CHECK v_spike_max  $&v_spike_max V      target >= 2.97 V       PASS
    else
      echo CHECK v_spike_max  $&v_spike_max V      target >= 2.97 V       FAIL
      let nfail = nfail + 1
    end
    let x = v_reset*1e3
    if v_reset <= 0.05
      echo CHECK v_reset      $&x mV     target <= 50 mV        PASS
    else
      echo CHECK v_reset      $&x mV     target <= 50 mV        FAIL
      let nfail = nfail + 1
    end
    let x = p_avg*1e6
    if p_avg <= 1e-6
      echo CHECK p_avg        $&x uW     target <= 1 uW         PASS
    else
      echo CHECK p_avg        $&x uW     target <= 1 uW         FAIL
      let nfail = nfail + 1
    end
    echo RES n_fail=$&nfail
    if nfail = 0
      echo neuron_nominal_tb: PASS, all 6 simulated specs met
    else
      echo neuron_nominal_tb: FAIL, $&nfail specs not met
    end
  end

  * Waveforms (time, VMEM, spike). From the GUI they go to this testbench's
  * folder; in batch mode (runner scripts) to the run's own folder, so that
  * parallel runs don't overwrite each other.
  set wr_singlescale
  set wr_vecnames
  if $?batchmode = 0
    wrdata /foss/designs/engn2912e-project/analog/testbenches/neuron/results/neuron_nominal_tb.txt v(VMEM) v(spike)
  else
    wrdata neuron_nominal_tb.txt v(VMEM) v(spike)
  end
  if $?batchmode = 0
    plot v(VMEM) v(spike) title 'neuron_nominal_tb: membrane and spike' xlabel 't (s)' ylabel 'V'
  end
.endc
"}
