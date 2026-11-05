v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {vdd*b32}
S {}
F {}
E {}
N -80 190 -40 190 {lab=Isum}
N -80 50 -80 190 {lab=Isum}
N -80 -100 -40 -100 {lab=Isum}
N -170 10 -130 10 {lab=VDD}
N -170 30 -130 30 {lab=Isyn}
N -500 10 -470 10 {lab=Vthr}
N -500 30 -470 30 {lab=VT}
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
N -420 -180 -420 -140 {lab=VT}
N -80 -100 -80 50 {lab=Isum}
C {DAC.sym} 110 -60 0 0 {name=x1}
C {DAC.sym} 110 90 0 0 {name=x2}
C {DAC.sym} 110 230 0 0 {name=x3}
C {DPI.sym} -320 30 0 0 {name=x4}
C {lab_wire.sym} -130 10 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -130 30 0 0 {name=p2 sig_type=std_logic lab=Isyn}
C {lab_wire.sym} -480 10 0 0 {name=p3 sig_type=std_logic lab=Vthr}
C {lab_wire.sym} -480 30 0 0 {name=p4 sig_type=std_logic lab=VT}
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
"}
C {lab_wire.sym} 210 80 0 0 {name=p17 sig_type=std_logic lab=Vb}
N 320 -20 320 10 {lab=VDD}
N 320 70 320 120 {lab=Vb}
N 280 120 320 120 {lab=Vb}
N 280 120 280 150 {lab=Vb}
N 320 180 320 210 {lab=0}
N 320 150 340 150 {lab=0}
N 340 150 340 180 {lab=0}
N 340 180 320 180 {lab=0}
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
T {Vb reference: Iref into a diode-connected
DAC unit current source (same W/L)} 360 100 0 0 0.25 0.25 {}
C {vsource.sym} -520 -210 0 0 {name=V1 value=3.3 savecurrent=false}
C {lab_wire.sym} -520 -270 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {gnd.sym} -520 -140 0 0 {name=l1 lab=0}
C {vsource.sym} -420 -210 0 0 {name=V2 value=\{vtau\} savecurrent=false}
C {lab_wire.sym} -420 -270 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -420 -140 0 0 {name=p20 sig_type=std_logic lab=VT}
C {code_shown.sym} -660 270 0 0 {name=TRAN_SIM only_toplevel=false 

value="
* DAC + DPI weight-code test.
* One input spike of width tpw every tsp, starting at t0. Spike k (k = 0..15)
* carries code k: bit b of k drives w<d>[b] of DAC x<d+1> while the spike is high.
* d1, d2, d3 = 1 send the codes to x1, x2, x3 (default: x1 only).
* DAC branch weights w[0]..w[3] = 1:2:3:4; iref sets the unit (w[0]) current,
* trimmed so that w[0] gives 15 nA here (the mirror reads about 4 % high, because
* V(Isum) ~ 2.5 V while the diode sits at ~0.6 V).
* DPI biases from analog/testbenches/README.md (before: Vthr = 3 V, VDD - VT = 0.5 V).
.param vdd=3.3 vthr=2.9 vtau=0.40 iref=14.42n tpw=10u tsp=2m t0=1m d1=1 d2=0 d3=0
.csparam tpw_c=\{tpw\}
.csparam tsp_c=\{tsp\}
.csparam t0_c=\{t0\}

Vthr  Vthr 0 \{vthr\}
VIdac Isum_dpi Isum 0
VIsyn Isyn 0 0

* Spike train, and one gate per code bit: gate b is high around the spikes k
* whose bit b is set (delay (2^b - 0.5) tsp, width 2^b tsp, period 2^(b+1) tsp)
Vspk spk 0 pulse(0 1 \{t0\} 10n 10n \{tpw\} \{tsp\})
Vg0 g0 0 pulse(0 1 \{t0+0.5*tsp\} 10n 10n \{tsp\} \{2*tsp\})
Vg1 g1 0 pulse(0 1 \{t0+1.5*tsp\} 10n 10n \{2*tsp\} \{4*tsp\})
Vg2 g2 0 pulse(0 1 \{t0+3.5*tsp\} 10n 10n \{4*tsp\} \{8*tsp\})
Vg3 g3 0 pulse(0 1 \{t0+7.5*tsp\} 10n 10n \{8*tsp\} \{16*tsp\})

* Bw<b><d> drives bit <b> of DAC x<d+1>, net w<d>[<b>]
Bw00 w0[0] 0 V = vdd*d1*v(spk)*v(g0)
Bw10 w0[1] 0 V = vdd*d1*v(spk)*v(g1)
Bw20 w0[2] 0 V = vdd*d1*v(spk)*v(g2)
Bw30 w0[3] 0 V = vdd*d1*v(spk)*v(g3)
Bw01 w1[0] 0 V = vdd*d2*v(spk)*v(g0)
Bw11 w1[1] 0 V = vdd*d2*v(spk)*v(g1)
Bw21 w1[2] 0 V = vdd*d2*v(spk)*v(g2)
Bw31 w1[3] 0 V = vdd*d2*v(spk)*v(g3)
Bw02 w2[0] 0 V = vdd*d3*v(spk)*v(g0)
Bw12 w2[1] 0 V = vdd*d3*v(spk)*v(g1)
Bw22 w2[2] 0 V = vdd*d3*v(spk)*v(g2)
Bw32 w2[3] 0 V = vdd*d3*v(spk)*v(g3)

.control
  save all
  set wr_singlescale
  set wr_vecnames
  tran 0.1u 33.5m 0 1u
  let idac = i(VIdac)
  let isyn = i(VIsyn)
  * Ideal weight of each code with branch weights 1:2:3:4
  compose wsum values 0 1 2 3 3 4 5 6 4 5 6 7 7 8 9 10

  * Per spike window k: DAC current while the spike is high (second half of the
  * spike), DAC leakage between spikes, charge per spike with the leakage
  * removed, and the DPI output peak. Unit = code 1 (w[0] only).
  let ion = vector(16)
  let leak = vector(16)
  let qnet = vector(16)
  let ipk = vector(16)
  let k = 0
  while k < 16
    let ts = t0_c + k*tsp_c
    let ta = ts + 0.5*tpw_c
    let tb = ts + 0.95*tpw_c
    let tl = ts + 0.5*tsp_c
    let te = ts + tsp_c - 1u
    meas tran m_on avg idac from=$&ta to=$&tb
    meas tran m_leak avg idac from=$&tl to=$&te
    meas tran m_q integ idac from=$&ts to=$&te
    meas tran m_pk max isyn from=$&ts to=$&te
    let ion[k] = m_on - m_leak
    let leak[k] = m_leak
    let qnet[k] = m_q - m_leak*(te - ts)
    let ipk[k] = m_pk
    let k = k + 1
  end

  let iunit = ion[1]
  echo
  echo code  weight  Idac(nA)  Idac/unit  error  Qnet(pC)  Isyn_peak(nA)
  let errmax = 0
  let k = 0
  while k < 16
    let wk = wsum[k]
    let ratio = ion[k]/iunit
    let err = 0
    if k > 0
      let err = ratio/wk - 1
      if abs(err) > errmax
        let errmax = abs(err)
      end
    end
    let ion_na = ion[k]*1e9
    let q_pc = qnet[k]*1e12
    let ipk_na = ipk[k]*1e9
    echo $&k  $&wk  $&ion_na  $&ratio  $&err  $&q_pc  $&ipk_na
    let k = k + 1
  end
  let k = 0
  while k < 16
    let v1 = ion[k]
    let v2 = qnet[k]
    let v3 = ipk[k]
    echo RES idac_$&k=$&v1
    echo RES q_$&k=$&v2
    echo RES isyn_pk_$&k=$&v3
    let k = k + 1
  end
  let v1 = leak[0]
  echo RES iunit=$&iunit
  echo RES idac_leak=$&v1
  echo RES dac_err_max=$&errmax

  wrdata dacs_dpi_codes.txt idac isyn
  if $?batchmode = 0
    plot idac title 'DAC output current (code k on spike k)' ylabel 'A'
    plot isyn title 'DPI output current' ylabel 'A'
    plot v(w0[0]) v(w0[1])+4 v(w0[2])+8 v(w0[3])+12 title 'x1 weight bits'
  end
.endc
"}
