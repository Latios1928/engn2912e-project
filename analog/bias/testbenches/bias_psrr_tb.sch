v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_psrr_tb: 1 V AC on VDD (both supplies). For each bias, the part of the ripple that reaches the gate drive of the device it biases: VDD - V(pin) for pFET-type biases, V(pin) for nFET-type ones and VT. RES psrr_<pin>_<f> in dB at 1 kHz, 100 kHz, 1 MHz (0 dB = the whole ripple).} -1100 -950 0 0 0.3 0.3 {}
C {vsource.sym} -1100 -300 0 0 {name=V1 value=\{vdd\} ac 1 savecurrent=false}
C {lab_pin.sym} -1100 -330 0 0 {name=l1 sig_type=std_logic lab=VDDS}
C {lab_pin.sym} -1100 -270 0 0 {name=l2 sig_type=std_logic lab=0}
C {ammeter.sym} -1000 -300 0 0 {name=VIdd savecurrent=true spice_ignore=0}
C {lab_pin.sym} -1000 -330 0 0 {name=l3 sig_type=std_logic lab=VDDS}
C {lab_pin.sym} -1000 -270 0 0 {name=l4 sig_type=std_logic lab=VDD}
C {vsource.sym} -800 -300 0 0 {name=Vtr3 value='vdd*(floor(code/8)-2*floor(code/16))' savecurrent=false}
C {lab_pin.sym} -800 -330 0 0 {name=l5 sig_type=std_logic lab=tr3}
C {lab_pin.sym} -800 -270 0 0 {name=l6 sig_type=std_logic lab=0}
C {vsource.sym} -720 -300 0 0 {name=Vtr2 value='vdd*(floor(code/4)-2*floor(code/8))' savecurrent=false}
C {lab_pin.sym} -720 -330 0 0 {name=l7 sig_type=std_logic lab=tr2}
C {lab_pin.sym} -720 -270 0 0 {name=l8 sig_type=std_logic lab=0}
C {vsource.sym} -640 -300 0 0 {name=Vtr1 value='vdd*(floor(code/2)-2*floor(code/4))' savecurrent=false}
C {lab_pin.sym} -640 -330 0 0 {name=l9 sig_type=std_logic lab=tr1}
C {lab_pin.sym} -640 -270 0 0 {name=l10 sig_type=std_logic lab=0}
C {vsource.sym} -560 -300 0 0 {name=Vtr0 value='vdd*(floor(code/1)-2*floor(code/2))' savecurrent=false}
C {lab_pin.sym} -560 -330 0 0 {name=l11 sig_type=std_logic lab=tr0}
C {lab_pin.sym} -560 -270 0 0 {name=l12 sig_type=std_logic lab=0}
C {vsource.sym} -450 -300 0 0 {name=Vmon value=\{vmon\} savecurrent=false}
C {lab_pin.sym} -450 -330 0 0 {name=l13 sig_type=std_logic lab=Imon}
C {lab_pin.sym} -450 -270 0 0 {name=l14 sig_type=std_logic lab=0}
C {analog/bias/bias_gen.sym} -200 -300 0 0 {name=xbg}
C {lab_pin.sym} -350 -400.0 0 0 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -350 -380.0 0 0 {name=l16 sig_type=std_logic lab=0}
C {lab_pin.sym} -350 -360.0 0 0 {name=l17 sig_type=std_logic lab=tr3}
C {lab_pin.sym} -350 -340.0 0 0 {name=l18 sig_type=std_logic lab=tr2}
C {lab_pin.sym} -350 -320.0 0 0 {name=l19 sig_type=std_logic lab=tr1}
C {lab_pin.sym} -350 -300.0 0 0 {name=l20 sig_type=std_logic lab=tr0}
C {lab_pin.sym} -350 -280.0 0 0 {name=l21 sig_type=std_logic lab=Imon}
C {lab_pin.sym} -50 -400.0 0 1 {name=l22 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -50 -380.0 0 1 {name=l23 sig_type=std_logic lab=Vthr}
C {lab_pin.sym} -50 -360.0 0 1 {name=l24 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -50 -340.0 0 1 {name=l25 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -50 -320.0 0 1 {name=l26 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -50 -300.0 0 1 {name=l27 sig_type=std_logic lab=VK}
C {lab_pin.sym} -50 -280.0 0 1 {name=l28 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -50 -260.0 0 1 {name=l29 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -50 -240.0 0 1 {name=l30 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -50 -220.0 0 1 {name=l31 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -50 -200.0 0 1 {name=l32 sig_type=std_logic lab=VT}
C {devices/code_shown.sym} -1100 -700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} -1100 -150 0 0 {name=CONTROL only_toplevel=true
value="
.param vdd=3.3 code=9 vmon=1.65
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
