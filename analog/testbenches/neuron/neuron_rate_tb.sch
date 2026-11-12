v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {neuron_rate_tb: firing rate of neuron_sized.sch versus a constant input current p_iin into VMEM.
Counts the spikes in p_tstop and reports the rate (spike 2 to the last spike; spike 1 starts from the
initial condition), the time to the first spike, and whether the neuron latched (spike stuck high).
Run over many currents by run_neuron_rate.py (add --pex for the post-layout neuron).} -1320 -720 0 0 0.3 0.3 {}
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
* Biases of neuron_sized (as in neuron_nominal_tb). p_iin, p_tstop and p_tmax
* (maximum time step) are set per point by run_neuron_rate.py.
.param p_vdd=3.3 p_iin=9.5n p_tstop=2m p_tmax=100n
.param p_vlk=0.425 p_vamp=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
.csparam vdd_c=\{p_vdd\}
.csparam tstop_c=\{p_tstop\}
.csparam tmax_c=\{p_tmax\}
.csparam iin_c=\{p_iin\}
.ic v(VMEM)=0 v(spike)=0
.control
  save v(spike) v(VMEM)
  tran 20n $&tstop_c 0 $&tmax_c uic
  let vsw = vdd_c/2

  * Count rising edges of spike through VDD/2 (a failed meas keeps -1)
  let n = 0
  let k = 1
  let t1 = -1
  let t2 = -1
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
    if k = 2
      let t2 = tk
    end
    let tlast = tk
    let n = k
    let k = k + 1
  end

  * rate: from spike 2 to the last spike (spike 1 starts from VMEM = 0)
  let rate = 0
  if n >= 3
    let rate = (n - 2)/(tlast - t2)
  end
  * Latch check over the last 20 % of the run: spike stuck high, VMEM range
  let tw = 0.8*tstop_c
  meas tran spike_min_end min v(spike) from=$&tw to=$&tstop_c
  meas tran spike_max_end max v(spike) from=$&tw to=$&tstop_c
  meas tran vmem_max_end max v(VMEM) from=$&tw to=$&tstop_c
  meas tran vmem_min_end min v(VMEM) from=$&tw to=$&tstop_c
  meas tran spike_max max v(spike)

  echo RES iin=$&iin_c
  echo RES nspikes=$&n
  echo RES rate=$&rate
  echo RES t_first=$&t1
  echo RES t_last=$&tlast
  echo RES spike_max=$&spike_max
  echo RES spike_min_end=$&spike_min_end
  echo RES spike_max_end=$&spike_max_end
  echo RES vmem_max_end=$&vmem_max_end
  echo RES vmem_min_end=$&vmem_min_end
  echo neuron_rate_tb: iin $&iin_c A, $&n spikes in $&tstop_c s, rate $&rate Hz

  set wr_singlescale
  set wr_vecnames
  if $?batchmode = 0
    wrdata /foss/designs/engn2912e-project/analog/testbenches/neuron/results/neuron_rate_tb.txt v(VMEM) v(spike)
    plot v(VMEM) v(spike) title 'neuron_rate_tb: membrane and spike' xlabel 't (s)' ylabel 'V'
  else
    wrdata neuron_rate_tb.txt v(VMEM) v(spike)
  end
.endc
"}
