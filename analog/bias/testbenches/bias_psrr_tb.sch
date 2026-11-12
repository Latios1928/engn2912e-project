v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_psrr_tb: 1 V AC on VDD (both supplies). For each bias, the part of the ripple that reaches the gate drive of the device it biases: VDD - V(pin) for pFET-type biases, V(pin) for nFET-type ones and VT. RES psrr_<pin>_<f> in dB at 1 kHz, 100 kHz, 1 MHz (0 dB = the whole ripple).} -1100 -950 0 0 0.3 0.3 {}
C {analog/bias/bias_gen.sym} 0 0 0 0 {name=xbg}
C {vsource.sym} -940 200 0 0 {name=V1 value="\{vdd\} ac 1" savecurrent=false}
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
C {devices/code_shown.sym} -400 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} -1100 330 0 0 {name=CONTROL only_toplevel=true
value="
.param vdd=3.3 code=9 vmon=1.65
* trim bits of 'code' (b3 = MSB), driven by Vtr3..Vtr0
.param b3='floor(code/8)-2*floor(code/16)' b2='floor(code/4)-2*floor(code/8)'
.param b1='floor(code/2)-2*floor(code/4)' b0='code-2*floor(code/2)'
.csparam code_c=\{code\}
.csparam vdd_c=\{vdd\}
.control
  save all
  ac dec 10 1 100meg
  let ps_Vb = db(v(Vb))
  meas ac psrr_Vb_1k find ps_Vb at=1k
  echo RES psrr_Vb_1k=$&psrr_Vb_1k
  meas ac psrr_Vb_100k find ps_Vb at=100k
  echo RES psrr_Vb_100k=$&psrr_Vb_100k
  meas ac psrr_Vb_1M find ps_Vb at=1meg
  echo RES psrr_Vb_1M=$&psrr_Vb_1M
  let ps_Vthr = db(1 - v(Vthr))
  meas ac psrr_Vthr_1k find ps_Vthr at=1k
  echo RES psrr_Vthr_1k=$&psrr_Vthr_1k
  meas ac psrr_Vthr_100k find ps_Vthr at=100k
  echo RES psrr_Vthr_100k=$&psrr_Vthr_100k
  meas ac psrr_Vthr_1M find ps_Vthr at=1meg
  echo RES psrr_Vthr_1M=$&psrr_Vthr_1M
  let ps_VT_dpi = db(1 - v(VT_dpi))
  meas ac psrr_VT_dpi_1k find ps_VT_dpi at=1k
  echo RES psrr_VT_dpi_1k=$&psrr_VT_dpi_1k
  meas ac psrr_VT_dpi_100k find ps_VT_dpi at=100k
  echo RES psrr_VT_dpi_100k=$&psrr_VT_dpi_100k
  meas ac psrr_VT_dpi_1M find ps_VT_dpi at=1meg
  echo RES psrr_VT_dpi_1M=$&psrr_VT_dpi_1M
  let ps_VNA = db(1 - v(VNA))
  meas ac psrr_VNA_1k find ps_VNA at=1k
  echo RES psrr_VNA_1k=$&psrr_VNA_1k
  meas ac psrr_VNA_100k find ps_VNA at=100k
  echo RES psrr_VNA_100k=$&psrr_VNA_100k
  meas ac psrr_VNA_1M find ps_VNA at=1meg
  echo RES psrr_VNA_1M=$&psrr_VNA_1M
  let ps_Vlk = db(v(Vlk))
  meas ac psrr_Vlk_1k find ps_Vlk at=1k
  echo RES psrr_Vlk_1k=$&psrr_Vlk_1k
  meas ac psrr_Vlk_100k find ps_Vlk at=100k
  echo RES psrr_Vlk_100k=$&psrr_Vlk_100k
  meas ac psrr_Vlk_1M find ps_Vlk at=1meg
  echo RES psrr_Vlk_1M=$&psrr_Vlk_1M
  let ps_VK = db(v(VK))
  meas ac psrr_VK_1k find ps_VK at=1k
  echo RES psrr_VK_1k=$&psrr_VK_1k
  meas ac psrr_VK_100k find ps_VK at=100k
  echo RES psrr_VK_100k=$&psrr_VK_100k
  meas ac psrr_VK_1M find ps_VK at=1meg
  echo RES psrr_VK_1M=$&psrr_VK_1M
  let ps_VIp = db(v(VIp))
  meas ac psrr_VIp_1k find ps_VIp at=1k
  echo RES psrr_VIp_1k=$&psrr_VIp_1k
  meas ac psrr_VIp_100k find ps_VIp at=100k
  echo RES psrr_VIp_100k=$&psrr_VIp_100k
  meas ac psrr_VIp_1M find ps_VIp at=1meg
  echo RES psrr_VIp_1M=$&psrr_VIp_1M
  let ps_VKup = db(1 - v(VKup))
  meas ac psrr_VKup_1k find ps_VKup at=1k
  echo RES psrr_VKup_1k=$&psrr_VKup_1k
  meas ac psrr_VKup_100k find ps_VKup at=100k
  echo RES psrr_VKup_100k=$&psrr_VKup_100k
  meas ac psrr_VKup_1M find ps_VKup at=1meg
  echo RES psrr_VKup_1M=$&psrr_VKup_1M
  let ps_VKdn = db(v(VKdn))
  meas ac psrr_VKdn_1k find ps_VKdn at=1k
  echo RES psrr_VKdn_1k=$&psrr_VKdn_1k
  meas ac psrr_VKdn_100k find ps_VKdn at=100k
  echo RES psrr_VKdn_100k=$&psrr_VKdn_100k
  meas ac psrr_VKdn_1M find ps_VKdn at=1meg
  echo RES psrr_VKdn_1M=$&psrr_VKdn_1M
  let ps_Vamp_bias = db(v(Vamp_bias))
  meas ac psrr_Vamp_bias_1k find ps_Vamp_bias at=1k
  echo RES psrr_Vamp_bias_1k=$&psrr_Vamp_bias_1k
  meas ac psrr_Vamp_bias_100k find ps_Vamp_bias at=100k
  echo RES psrr_Vamp_bias_100k=$&psrr_Vamp_bias_100k
  meas ac psrr_Vamp_bias_1M find ps_Vamp_bias at=1meg
  echo RES psrr_Vamp_bias_1M=$&psrr_Vamp_bias_1M
  let ps_VT = db(v(VT))
  meas ac psrr_VT_1k find ps_VT at=1k
  echo RES psrr_VT_1k=$&psrr_VT_1k
  meas ac psrr_VT_100k find ps_VT at=100k
  echo RES psrr_VT_100k=$&psrr_VT_100k
  meas ac psrr_VT_1M find ps_VT at=1meg
  echo RES psrr_VT_1M=$&psrr_VT_1M
  if $?batchmode = 0
    plot ps_Vthr ps_VT_dpi ps_Vlk ps_VK ps_VNA ps_VT xlog title 'Supply ripple at the gate drive (dB)'
  end
.endc
"}
