v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_network_tb: main's 2-2-1 network snn_analog with every bias from bias_gen. All 8 weights at 'wcode' (default 7 = +7), both inputs pulsing (10 us every 200 us). Optional coupling 'ccoup' from pulse[0] to every bias net (layout stand-in). RES pp_<net> / sh_<net>: peak-to-peak wobble and shift of the average from the DC value after 0.5 ms; spikes in network.txt (counted by run_bias.py).} -1100 -950 0 0 0.3 0.3 {}
C {analog/bias/bias_gen.sym} 0 0 0 0 {name=xbg}
C {vsource.sym} -940 200 0 0 {name=V1 value=\{vdd\} savecurrent=false}
C {gnd.sym} -940 230 0 0 {name=g1 lab=0}
N -940 170 -940 -160 {}
N -940 -160 -200 -160 {}
C {ammeter.sym} -200 -130 0 0 {name=VIdd savecurrent=true spice_ignore=0}
N -200 -100 -150 -100.0 {}
C {lab_wire.sym} -175.0 -100.0 0 0 {name=w2 sig_type=std_logic lab=VDD}
N -150 -80.0 -820 -80.0 {}
N -820 -80.0 -820 230 {}
C {gnd.sym} -820 230 0 0 {name=g3 lab=0}
C {vsource.sym} -700 200 0 0 {name=Vtr3 value='vdd*b3' savecurrent=false}
C {gnd.sym} -700 230 0 0 {name=g4 lab=0}
N -700 170 -700 -60.0 {}
N -700 -60.0 -150 -60.0 {}
C {vsource.sym} -590 200 0 0 {name=Vtr2 value='vdd*b2' savecurrent=false}
C {gnd.sym} -590 230 0 0 {name=g5 lab=0}
N -590 170 -590 -40.0 {}
N -590 -40.0 -150 -40.0 {}
C {vsource.sym} -480 200 0 0 {name=Vtr1 value='vdd*b1' savecurrent=false}
C {gnd.sym} -480 230 0 0 {name=g6 lab=0}
N -480 170 -480 -20.0 {}
N -480 -20.0 -150 -20.0 {}
C {vsource.sym} -370 200 0 0 {name=Vtr0 value='vdd*b0' savecurrent=false}
C {gnd.sym} -370 230 0 0 {name=g7 lab=0}
N -370 170 -370 0.0 {}
N -370 0.0 -150 0.0 {}
C {vsource.sym} -260 200 0 0 {name=Vmon value=\{vmon\} savecurrent=false}
C {gnd.sym} -260 230 0 0 {name=g8 lab=0}
N -260 170 -260 20.0 {}
N -260 20.0 -150 20.0 {}
N 150 -100.0 210 -100.0 {}
C {lab_wire.sym} 180.0 -100.0 0 0 {name=w9 sig_type=std_logic lab=Vb}
N 150 -80.0 210 -80.0 {}
C {lab_wire.sym} 180.0 -80.0 0 0 {name=w10 sig_type=std_logic lab=Vthr}
N 150 -60.0 210 -60.0 {}
C {lab_wire.sym} 180.0 -60.0 0 0 {name=w11 sig_type=std_logic lab=VT_dpi}
N 150 -40.0 210 -40.0 {}
C {lab_wire.sym} 180.0 -40.0 0 0 {name=w12 sig_type=std_logic lab=VNA}
N 150 -20.0 210 -20.0 {}
C {lab_wire.sym} 180.0 -20.0 0 0 {name=w13 sig_type=std_logic lab=Vlk}
N 150 0.0 210 0.0 {}
C {lab_wire.sym} 180.0 0.0 0 0 {name=w14 sig_type=std_logic lab=VK}
N 150 20.0 210 20.0 {}
C {lab_wire.sym} 180.0 20.0 0 0 {name=w15 sig_type=std_logic lab=VIp}
N 150 40.0 210 40.0 {}
C {lab_wire.sym} 180.0 40.0 0 0 {name=w16 sig_type=std_logic lab=VKup}
N 150 60.0 210 60.0 {}
C {lab_wire.sym} 180.0 60.0 0 0 {name=w17 sig_type=std_logic lab=VKdn}
N 150 80.0 210 80.0 {}
C {lab_wire.sym} 180.0 80.0 0 0 {name=w18 sig_type=std_logic lab=Vamp_bias}
N 150 100.0 210 100.0 {}
C {lab_wire.sym} 180.0 100.0 0 0 {name=w19 sig_type=std_logic lab=VT}
C {snn_analog.sym} 700 0 0 0 {name=x1}
C {lab_pin.sym} 550.0 -140.0 0 0 {name=l20 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 550.0 -120.0 0 0 {name=l21 sig_type=std_logic lab=0}
C {lab_pin.sym} 550.0 -100.0 0 0 {name=l22 sig_type=std_logic lab=w[31:0]}
C {lab_pin.sym} 550.0 -80.0 0 0 {name=l23 sig_type=std_logic lab=pulse[1:0]}
C {lab_pin.sym} 550.0 -60.0 0 0 {name=l24 sig_type=std_logic lab=Vb}
C {lab_pin.sym} 550.0 -40.0 0 0 {name=l25 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} 550.0 -20.0 0 0 {name=l26 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} 550.0 0.0 0 0 {name=l27 sig_type=std_logic lab=VNA}
C {lab_pin.sym} 550.0 20.0 0 0 {name=l28 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} 550.0 40.0 0 0 {name=l29 sig_type=std_logic lab=VK}
C {lab_pin.sym} 550.0 60.0 0 0 {name=l30 sig_type=std_logic lab=VIp}
C {lab_pin.sym} 550.0 80.0 0 0 {name=l31 sig_type=std_logic lab=VKup}
C {lab_pin.sym} 550.0 100.0 0 0 {name=l32 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} 550.0 120.0 0 0 {name=l33 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} 550.0 140.0 0 0 {name=l34 sig_type=std_logic lab=VT}
C {lab_pin.sym} 850.0 0.0 0 1 {name=l35 sig_type=std_logic lab=spike[4:0]}
C {devices/code_shown.sym} -400 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} -1900 -650 0 0 {name=SOURCES only_toplevel=true
value="
* weights: every 4-bit word = wcode (bit k = wk); inputs: 10 us pulses every 200 us
.param w3='floor(wcode/8)-2*floor(wcode/16)' w2='floor(wcode/4)-2*floor(wcode/8)'
.param w1='floor(wcode/2)-2*floor(wcode/4)' w0='wcode-2*floor(wcode/2)'
Vw0 w[0] 0 'vdd*w0'
Vw1 w[1] 0 'vdd*w1'
Vw2 w[2] 0 'vdd*w2'
Vw3 w[3] 0 'vdd*w3'
Vw4 w[4] 0 'vdd*w0'
Vw5 w[5] 0 'vdd*w1'
Vw6 w[6] 0 'vdd*w2'
Vw7 w[7] 0 'vdd*w3'
Vw8 w[8] 0 'vdd*w0'
Vw9 w[9] 0 'vdd*w1'
Vw10 w[10] 0 'vdd*w2'
Vw11 w[11] 0 'vdd*w3'
Vw12 w[12] 0 'vdd*w0'
Vw13 w[13] 0 'vdd*w1'
Vw14 w[14] 0 'vdd*w2'
Vw15 w[15] 0 'vdd*w3'
Vw16 w[16] 0 'vdd*w0'
Vw17 w[17] 0 'vdd*w1'
Vw18 w[18] 0 'vdd*w2'
Vw19 w[19] 0 'vdd*w3'
Vw20 w[20] 0 'vdd*w0'
Vw21 w[21] 0 'vdd*w1'
Vw22 w[22] 0 'vdd*w2'
Vw23 w[23] 0 'vdd*w3'
Vw24 w[24] 0 'vdd*w0'
Vw25 w[25] 0 'vdd*w1'
Vw26 w[26] 0 'vdd*w2'
Vw27 w[27] 0 'vdd*w3'
Vw28 w[28] 0 'vdd*w0'
Vw29 w[29] 0 'vdd*w1'
Vw30 w[30] 0 'vdd*w2'
Vw31 w[31] 0 'vdd*w3'
Vp0 pulse[0] 0 pulse(0 3.3 100u 10n 10n 10u 200u)
Vp1 pulse[1] 0 pulse(0 3.3 100u 10n 10n 10u 200u)
Cc_Vb pulse[0] Vb \{ccoup\}
Cc_Vthr pulse[0] Vthr \{ccoup\}
Cc_VT_dpi pulse[0] VT_dpi \{ccoup\}
Cc_VNA pulse[0] VNA \{ccoup\}
Cc_Vlk pulse[0] Vlk \{ccoup\}
Cc_VK pulse[0] VK \{ccoup\}
Cc_VIp pulse[0] VIp \{ccoup\}
Cc_VKup pulse[0] VKup \{ccoup\}
Cc_VKdn pulse[0] VKdn \{ccoup\}
Cc_Vamp_bias pulse[0] Vamp_bias \{ccoup\}
Cc_VT pulse[0] VT \{ccoup\}
Esp0 sp0 0 spike[0] 0 1
Esp1 sp1 0 spike[1] 0 1
Esp2 sp2 0 spike[2] 0 1
Esp3 sp3 0 spike[3] 0 1
Esp4 sp4 0 spike[4] 0 1
.ic v(x1.VMEM_0)=0 v(x1.VMEM_1)=0 v(x1.VMEM_2)=0 v(x1.VMEM_3)=0 v(x1.VMEM_4)=0 v(spike[0])=0 v(spike[1])=0 v(spike[2])=0 v(spike[3])=0 v(spike[4])=0
"}
C {devices/code_shown.sym} -1100 330 0 0 {name=CONTROL only_toplevel=true
value="
.param vdd=3.3 code=9 vmon=1.65
* trim bits of 'code' (b3 = MSB), driven by Vtr3..Vtr0
.param b3='floor(code/8)-2*floor(code/16)' b2='floor(code/4)-2*floor(code/8)'
.param b1='floor(code/2)-2*floor(code/4)' b0='code-2*floor(code/2)'
.csparam code_c=\{code\}
.csparam vdd_c=\{vdd\}
.param wcode=7 ccoup=0 tstop=3m
.csparam tstop_c=\{tstop\}
.options method=gear
.control
  save v(sp0) v(sp1) v(sp2) v(sp3) v(sp4) v(Vb) v(Vthr) v(VT_dpi) v(VNA) v(Vlk) v(VK) v(VIp) v(VKup) v(VKdn) v(Vamp_bias) v(VT)
  set wr_singlescale
  set wr_vecnames
  tran 0.1u $&tstop_c 0 0.1u
  meas tran hi_0 max v(Vb) from=0.5m
  meas tran lo_0 min v(Vb) from=0.5m
  meas tran av_0 avg v(Vb) from=0.5m
  let v0_0 = v(Vb)[0]
  let pp_0 = hi_0 - lo_0
  let sh_0 = av_0 - v0_0
  echo RES pp_Vb=$&pp_0
  echo RES sh_Vb=$&sh_0
  meas tran hi_1 max v(Vthr) from=0.5m
  meas tran lo_1 min v(Vthr) from=0.5m
  meas tran av_1 avg v(Vthr) from=0.5m
  let v0_1 = v(Vthr)[0]
  let pp_1 = hi_1 - lo_1
  let sh_1 = av_1 - v0_1
  echo RES pp_Vthr=$&pp_1
  echo RES sh_Vthr=$&sh_1
  meas tran hi_2 max v(VT_dpi) from=0.5m
  meas tran lo_2 min v(VT_dpi) from=0.5m
  meas tran av_2 avg v(VT_dpi) from=0.5m
  let v0_2 = v(VT_dpi)[0]
  let pp_2 = hi_2 - lo_2
  let sh_2 = av_2 - v0_2
  echo RES pp_VT_dpi=$&pp_2
  echo RES sh_VT_dpi=$&sh_2
  meas tran hi_3 max v(VNA) from=0.5m
  meas tran lo_3 min v(VNA) from=0.5m
  meas tran av_3 avg v(VNA) from=0.5m
  let v0_3 = v(VNA)[0]
  let pp_3 = hi_3 - lo_3
  let sh_3 = av_3 - v0_3
  echo RES pp_VNA=$&pp_3
  echo RES sh_VNA=$&sh_3
  meas tran hi_4 max v(Vlk) from=0.5m
  meas tran lo_4 min v(Vlk) from=0.5m
  meas tran av_4 avg v(Vlk) from=0.5m
  let v0_4 = v(Vlk)[0]
  let pp_4 = hi_4 - lo_4
  let sh_4 = av_4 - v0_4
  echo RES pp_Vlk=$&pp_4
  echo RES sh_Vlk=$&sh_4
  meas tran hi_5 max v(VK) from=0.5m
  meas tran lo_5 min v(VK) from=0.5m
  meas tran av_5 avg v(VK) from=0.5m
  let v0_5 = v(VK)[0]
  let pp_5 = hi_5 - lo_5
  let sh_5 = av_5 - v0_5
  echo RES pp_VK=$&pp_5
  echo RES sh_VK=$&sh_5
  meas tran hi_6 max v(VIp) from=0.5m
  meas tran lo_6 min v(VIp) from=0.5m
  meas tran av_6 avg v(VIp) from=0.5m
  let v0_6 = v(VIp)[0]
  let pp_6 = hi_6 - lo_6
  let sh_6 = av_6 - v0_6
  echo RES pp_VIp=$&pp_6
  echo RES sh_VIp=$&sh_6
  meas tran hi_7 max v(VKup) from=0.5m
  meas tran lo_7 min v(VKup) from=0.5m
  meas tran av_7 avg v(VKup) from=0.5m
  let v0_7 = v(VKup)[0]
  let pp_7 = hi_7 - lo_7
  let sh_7 = av_7 - v0_7
  echo RES pp_VKup=$&pp_7
  echo RES sh_VKup=$&sh_7
  meas tran hi_8 max v(VKdn) from=0.5m
  meas tran lo_8 min v(VKdn) from=0.5m
  meas tran av_8 avg v(VKdn) from=0.5m
  let v0_8 = v(VKdn)[0]
  let pp_8 = hi_8 - lo_8
  let sh_8 = av_8 - v0_8
  echo RES pp_VKdn=$&pp_8
  echo RES sh_VKdn=$&sh_8
  meas tran hi_9 max v(Vamp_bias) from=0.5m
  meas tran lo_9 min v(Vamp_bias) from=0.5m
  meas tran av_9 avg v(Vamp_bias) from=0.5m
  let v0_9 = v(Vamp_bias)[0]
  let pp_9 = hi_9 - lo_9
  let sh_9 = av_9 - v0_9
  echo RES pp_Vamp_bias=$&pp_9
  echo RES sh_Vamp_bias=$&sh_9
  meas tran hi_10 max v(VT) from=0.5m
  meas tran lo_10 min v(VT) from=0.5m
  meas tran av_10 avg v(VT) from=0.5m
  let v0_10 = v(VT)[0]
  let pp_10 = hi_10 - lo_10
  let sh_10 = av_10 - v0_10
  echo RES pp_VT=$&pp_10
  echo RES sh_VT=$&sh_10
  wrdata network.txt v(sp0) v(sp1) v(sp2) v(sp3) v(sp4)
  if $?batchmode = 0
    plot v(sp4)+4 v(sp3) v(Vthr) v(VT_dpi) title 'output, hid1 spikes; DPI biases'
  end
.endc
"}
