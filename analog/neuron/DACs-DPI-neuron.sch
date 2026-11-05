v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {vdd*b32}
S {}
F {}
E {}
T {Vb reference: Iref into a diode-connected
DAC unit current source (same W/L)} 360 100 0 0 0.25 0.25 {}
T {DACs-DPI-neuron: three DACs (weights 1:2:3:4, unit 15 nA) -> DPI synapse -> neuron_sized.
Input spikes every tsp (10 us wide) drive each DAC's enable; the weight bits are held at code1/code2/code3.
Prints the membrane voltage after each input spike, the input spike on which the neuron first fires,
and the number of input spikes per output spike after that. Start xschem from the project root.} -730 -620 0 0 0.3 0.3 {}
T {neuron_sized: VMEM is driven by the DPI output Isyn (VIsyn in TRAN_SIM).
Bias sources and values as in neuron_sized_testbench.sch.} 1300 -620 0 0 0.3 0.3 {}
N -80 190 -40 190 {lab=Isum}
N -80 50 -80 190 {lab=Isum}
N -80 -100 -40 -100 {lab=Isum}
N -170 10 -130 10 {lab=VDD}
N -170 30 -130 30 {lab=Isyn}
N -500 10 -470 10 {lab=Vthr}
N -500 30 -470 30 {lab=VT_dpi}
N -500 50 -470 50 {lab=Isum_dpi}
N -70 -80 -40 -80 {lab=w0[3:0] bus=true}
N -70 70 -40 70 {lab=w1[3:0] bus=true}
N -170 50 -80 50 {lab=Isum}
N -80 50 -40 50 {lab=Isum}
N -70 210 -40 210 {lab=w2[3:0] bus=true}
N 160 -100 160 80 {lab=Vb}
N 160 80 160 190 {lab=Vb}
N 160 80 210 80 {lab=Vb}
N -520 -270 -520 -240 {lab=VDD}
N -520 -180 -520 -140 {lab=0}
N -130 30 -130 80 {lab=Isyn}
N -420 -270 -420 -240 {lab=VDD}
N -420 -180 -420 -140 {lab=VT_dpi}
N -80 -100 -80 50 {lab=Isum}
N 320 -20 320 10 {lab=VDD}
N 320 70 320 120 {lab=Vb}
N 280 120 320 120 {lab=Vb}
N 280 120 280 150 {lab=Vb}
N 320 180 320 210 {lab=0}
N 320 150 340 150 {lab=0}
N 340 150 340 180 {lab=0}
N 320 180 340 180 {lab=0}
N 900 -130 900 -100 {lab=VSS}
N 900 -40 900 0 {lab=0}
N 1790 -100 1870 -100 {lab=VDD}
N 1790 -120 1870 -120 {lab=VSS}
N 1790 -80 1870 -80 {lab=spike}
N 1420 40 1490 40 {lab=VT}
N 1420 20 1490 20 {lab=Vamp_bias}
N 1420 0 1490 0 {lab=VKdn}
N 1420 -20 1490 -20 {lab=VKup}
N 1420 -40 1490 -40 {lab=VIp}
N 1420 -60 1490 -60 {lab=VK}
N 1420 -80 1490 -80 {lab=Vlk}
N 1420 -100 1490 -100 {lab=VNA}
N 1420 -120 1490 -120 {lab=VMEM}
N 900 -500 900 -470 {lab=VK}
N 840 -500 840 -470 {lab=Vlk}
N 840 -410 840 -370 {lab=VSS}
N 900 -410 900 -370 {lab=VSS}
N 760 -500 760 -470 {lab=VNA}
N 760 -410 760 -370 {lab=VSS}
N 900 -320 900 -290 {lab=VKdn}
N 840 -320 840 -290 {lab=VKup}
N 840 -230 840 -190 {lab=VSS}
N 900 -230 900 -190 {lab=VSS}
N 760 -320 760 -290 {lab=VIp}
N 760 -230 760 -190 {lab=VSS}
N 1090 -320 1090 -290 {lab=VT}
N 1090 -230 1090 -190 {lab=VSS}
N 1010 -320 1010 -290 {lab=Vamp_bias}
N 1010 -230 1010 -190 {lab=VSS}
N -70 -60 -40 -60 {lab=en0}
N -70 90 -40 90 {lab=en1}
N -70 230 -40 230 {lab=en2}
C {DAC.sym} 110 -60 0 0 {name=x1}
C {DAC.sym} 110 90 0 0 {name=x2}
C {DAC.sym} 110 230 0 0 {name=x3}
C {DPI.sym} -320 30 0 0 {name=x4}
C {lab_wire.sym} -130 10 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -130 30 0 0 {name=p2 sig_type=std_logic lab=Isyn}
C {lab_wire.sym} -480 10 0 0 {name=p3 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -480 30 0 0 {name=p4 sig_type=std_logic lab=VT_dpi}
C {lab_wire.sym} -480 50 0 0 {name=p21 sig_type=std_logic lab=Isum_dpi}
C {lab_wire.sym} -170 50 0 0 {name=p22 sig_type=std_logic lab=Isum}
C {lab_wire.sym} -60 -80 0 0 {name=p5 sig_type=std_logic lab=w0[3:0] bus=true}
C {lab_wire.sym} -60 70 0 0 {name=p9 sig_type=std_logic lab=w1[3:0] bus=true}
C {lab_wire.sym} -60 210 0 0 {name=p13 sig_type=std_logic lab=w2[3:0] bus=true}
C {devices/code_shown.sym} -730 160 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {lab_wire.sym} 210 80 0 0 {name=p17 sig_type=std_logic lab=Vb}
C {isource.sym} 320 40 0 0 {name=Iref value=\{iref\}}
C {lab_wire.sym} 320 -20 0 0 {name=p23 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 280 120 0 0 {name=p24 sig_type=std_logic lab=Vb}
C {symbols/nfet_03v3.sym} 300 150 0 0 {name=Mref
L=8u
W=1u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {gnd.sym} 320 210 0 0 {name=l2 lab=0}
C {vsource.sym} -520 -210 0 0 {name=V1 value=3.3 savecurrent=false}
C {lab_wire.sym} -520 -270 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {gnd.sym} -520 -140 0 0 {name=l1 lab=0}
C {vsource.sym} -420 -210 0 0 {name=V2 value=\{vtau\} savecurrent=false}
C {lab_wire.sym} -420 -270 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -420 -140 0 0 {name=p20 sig_type=std_logic lab=VT_dpi}
C {vsource.sym} 900 -70 0 0 {name=Vss value=0 savecurrent=false}
C {lab_wire.sym} 900 -130 0 0 {name=pn7 sig_type=std_logic lab=VSS}
C {gnd.sym} 900 0 0 0 {name=ln1 lab=0}
C {neuron_sized.sym} 1640 -40 0 0 {name=xn}
C {lab_wire.sym} 1870 -120 0 0 {name=pn1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 1870 -100 0 0 {name=pn2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1870 -80 0 0 {name=pn3 sig_type=std_logic lab=spike}
C {lab_wire.sym} 1420 -120 0 0 {name=pn4 sig_type=std_logic lab=VMEM}
C {lab_wire.sym} 1420 -100 0 0 {name=pn5 sig_type=std_logic lab=VNA}
C {lab_wire.sym} 1420 -80 0 0 {name=pn6 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} 1420 -60 0 0 {name=pn11 sig_type=std_logic lab=VK}
C {lab_wire.sym} 1420 -40 0 0 {name=pn12 sig_type=std_logic lab=VIp}
C {lab_wire.sym} 1420 -20 0 0 {name=pn15 sig_type=std_logic lab=VKup}
C {lab_wire.sym} 1420 0 0 0 {name=pn16 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} 1420 20 0 0 {name=pn17 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} 1420 40 0 0 {name=pn20 sig_type=std_logic lab=VT}
C {vsource.sym} 840 -440 0 0 {name=Vlk value=\{Vlk\} savecurrent=false}
C {vsource.sym} 900 -440 0 0 {name=VK value=\{VK\} savecurrent=false}
C {lab_wire.sym} 900 -500 0 0 {name=pn21 sig_type=std_logic lab=VK}
C {lab_wire.sym} 840 -500 0 0 {name=pn22 sig_type=std_logic lab=Vlk}
C {lab_wire.sym} 840 -370 0 0 {name=pn23 sig_type=std_logic lab=VSS}
C {vsource.sym} 760 -440 0 0 {name=VNA value=\{VNA\} savecurrent=false}
C {lab_wire.sym} 760 -500 0 0 {name=pn24 sig_type=std_logic lab=VNA}
C {lab_wire.sym} 760 -370 0 0 {name=pn25 sig_type=std_logic lab=VSS}
C {vsource.sym} 840 -260 0 0 {name=VKup value=\{VKup\} savecurrent=false}
C {vsource.sym} 900 -260 0 0 {name=VKdn value=\{VKdn\} savecurrent=false}
C {lab_wire.sym} 900 -320 0 0 {name=pn26 sig_type=std_logic lab=VKdn}
C {lab_wire.sym} 840 -320 0 0 {name=pn27 sig_type=std_logic lab=VKup}
C {lab_wire.sym} 840 -190 0 0 {name=pn28 sig_type=std_logic lab=VSS}
C {vsource.sym} 760 -260 0 0 {name=VIp value=\{VIp\} savecurrent=false}
C {lab_wire.sym} 760 -320 0 0 {name=pn29 sig_type=std_logic lab=VIp}
C {lab_wire.sym} 760 -190 0 0 {name=pn30 sig_type=std_logic lab=VSS}
C {vsource.sym} 1090 -260 0 0 {name=VT value=\{VT\} savecurrent=false}
C {lab_wire.sym} 1090 -320 0 0 {name=pn32 sig_type=std_logic lab=VT}
C {lab_wire.sym} 1090 -190 0 0 {name=pn33 sig_type=std_logic lab=VSS}
C {vsource.sym} 1010 -260 0 0 {name=Vamp_bias value=\{Vamp_bias\} savecurrent=false}
C {lab_wire.sym} 1010 -320 0 0 {name=pn34 sig_type=std_logic lab=Vamp_bias}
C {lab_wire.sym} 1010 -190 0 0 {name=pn35 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 900 -370 0 0 {name=pn36 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 900 -190 0 0 {name=pn37 sig_type=std_logic lab=VSS}
C {code_shown.sym} -730 380 0 0 {name=TRAN_SIM only_toplevel=false

value="
* How many input spikes of a given weight fire neuron_sized.
* One input spike of width tpw every tsp, from t0, on the enable (en) of each DAC.
* The weight bits of DACs x1 / x2 / x3 are held at code1 / code2 / code3 (0..15). DAC branch weights w[0]..w[3] = 1:2:3:4 with a 15 nA unit,
* so code 2 = weight 2 = 30 nA while the spike is high.
* vthr is tuned so that code 2 at 5 kHz (tsp = 200 us) first fires the neuron on input
* spike 10 (tt, 27 C). The count is steep in vthr: about one input spike per 1-2 mV.
.param vdd=3.3 vthr=2.909 vtau=0.40 iref=14.42n tpw=10u tsp=200u t0=100u
.param code1=2 code2=0 code3=0
* neuron_sized biases, as in neuron_sized_testbench.sch
.param Vlk=0.425 Vamp_bias=0.535 VIp=0.573 VNA=1.93 VKup=2.35 VK=1.22 VKdn=0.588 VT=1.66
* Bit b of each code
.param x1b0=\{code1-2*floor(code1/2)\} x1b1=\{floor(code1/2)-2*floor(code1/4)\}
.param x1b2=\{floor(code1/4)-2*floor(code1/8)\} x1b3=\{floor(code1/8)-2*floor(code1/16)\}
.param x2b0=\{code2-2*floor(code2/2)\} x2b1=\{floor(code2/2)-2*floor(code2/4)\}
.param x2b2=\{floor(code2/4)-2*floor(code2/8)\} x2b3=\{floor(code2/8)-2*floor(code2/16)\}
.param x3b0=\{code3-2*floor(code3/2)\} x3b1=\{floor(code3/2)-2*floor(code3/4)\}
.param x3b2=\{floor(code3/4)-2*floor(code3/8)\} x3b3=\{floor(code3/8)-2*floor(code3/16)\}
.csparam tsp_c=\{tsp\}
.csparam t0_c=\{t0\}
.csparam wsum_c=\{x1b0+2*x1b1+3*x1b2+4*x1b3 + x2b0+2*x2b1+3*x2b2+4*x2b3 + x3b0+2*x3b1+3*x3b2+4*x3b3\}
.ic v(VMEM)=0 v(spike)=0
* Gear integration: the default (trap) makes i(VIsyn) ring step to step after each reset
.options method=gear

Vthr  Vthr 0 \{vthr\}
VIdac Isum_dpi Isum 0
* DPI output into the neuron membrane
VIsyn Isyn VMEM 0

* Weights are static levels, as from the weight register file: Vw<b><d> holds
* bit <b> of code<d+1> on DAC x<d+1> (net w<d>[<b>])
Vw00 w0[0] 0 \{vdd*x1b0\}
Vw10 w0[1] 0 \{vdd*x1b1\}
Vw20 w0[2] 0 \{vdd*x1b2\}
Vw30 w0[3] 0 \{vdd*x1b3\}
Vw01 w1[0] 0 \{vdd*x2b0\}
Vw11 w1[1] 0 \{vdd*x2b1\}
Vw21 w1[2] 0 \{vdd*x2b2\}
Vw31 w1[3] 0 \{vdd*x2b3\}
Vw02 w2[0] 0 \{vdd*x3b0\}
Vw12 w2[1] 0 \{vdd*x3b1\}
Vw22 w2[2] 0 \{vdd*x3b2\}
Vw32 w2[3] 0 \{vdd*x3b3\}

* Input spike train on each DAC's enable (the previous section's output)
Ven0 en0 0 pulse(0 \{vdd\} \{t0\} 10n 10n \{tpw\} \{tsp\})
Ven1 en1 0 pulse(0 \{vdd\} \{t0\} 10n 10n \{tpw\} \{tsp\})
Ven2 en2 0 pulse(0 \{vdd\} \{t0\} 10n 10n \{tpw\} \{tsp\})

.control
  save all
  set wr_singlescale
  set wr_vecnames
  tran 0.1u 6.1m 0 0.5u
  let isyn = i(VIsyn)
  let nin = floor((6.1m - t0_c)/tsp_c)
  let rate_khz = 1e-3/tsp_c
  echo
  echo Total weight per input spike: $&wsum_c, input rate $&rate_khz kHz, $&nin input spikes

  meas tran vsp max v(spike)
  let n_first = 0
  if vsp < 1.65
    echo The neuron did not fire.
    let nshow = nin
  else
    meas tran t1 when v(spike)=1.65 rise=1
    let n_first = floor((t1 - t0_c)/tsp_c) + 1
    let lat_us = (t1 - t0_c - (n_first - 1)*tsp_c)*1e6
    let nshow = n_first
    echo First output spike after input spike $&n_first ($&lat_us us after it).
  end

  * Membrane just before each next input spike, and the DPI peak in each interval
  echo
  echo input  VMEM_before_next(V)  Isyn_peak(nA)
  let k = 1
  while k <= nshow
    let ta = t0_c + (k - 1)*tsp_c
    let tb = t0_c + k*tsp_c - 1u
    meas tran m_v find v(VMEM) at=$&tb
    let tc = ta + 0.5*tsp_c
    meas tran m_i max isyn from=$&ta to=$&tc
    let i_na = m_i*1e9
    if k = n_first
      echo $&k  fired  $&i_na
    else
      echo $&k  $&m_v  $&i_na
    end
    let k = k + 1
  end

  * Input spikes per output spike once firing has started
  let t3 = 0
  if n_first > 0
    meas tran t3 when v(spike)=1.65 rise=3
  end
  let n_per = 0
  if t3 > 0
    let n_per = (t3 - t1)/(2*tsp_c)
    echo
    echo After the first output: one output spike every $&n_per input spikes.
  end

  * DAC charge per input spike (spike 2), with the DAC leakage between spikes removed
  let ta = t0_c + tsp_c
  let tm = ta + 0.5*tsp_c
  let te = ta + tsp_c - 1u
  meas tran m_q integ i(VIdac) from=$&ta to=$&tm
  meas tran m_lk avg i(VIdac) from=$&tm to=$&te
  let q_spike = m_q - m_lk*(tm - ta)
  let q_fc = q_spike*1e15
  let lk_pa = m_lk*1e12
  echo DAC charge per input spike: $&q_fc fC (DAC leakage between spikes $&lk_pa pA)
  echo RES q_spike=$&q_spike
  echo RES i_leak=$&m_lk

  echo RES n_first=$&n_first
  echo RES n_per=$&n_per

  wrdata dacs_dpi_neuron.txt v(VMEM) v(spike) isyn v(en0)
  if $?batchmode = 0
    plot v(VMEM) v(spike) v(en0)*0.15 title 'Membrane, output spike, input spikes on en0 (x0.15)' ylabel 'V'
    plot isyn title 'DPI output current into the membrane' ylabel 'A'
  end
.endc
"}
C {lab_wire.sym} -70 -60 0 0 {name=p30 sig_type=std_logic lab=en0}
C {lab_wire.sym} -70 90 0 0 {name=p31 sig_type=std_logic lab=en1}
C {lab_wire.sym} -70 230 0 0 {name=p32 sig_type=std_logic lab=en2}
