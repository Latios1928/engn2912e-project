v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_dc_tb: operating point of bias_gen at trim code 'code' (per output: pin voltage, probe current / target g, g/m with m = Imon / its target), supply current, VT; VDD swept 2.97-3.63 V; the Imon pad voltage below which Imon drops by more than 1 %. Results print as RES lines.} -1100 -950 0 0 0.3 0.3 {}
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
C {analog/bias/testbenches/bias_probes.sym} 450 -30.0 0 0 {name=xp}
N 150 -100.0 300 -100.0 {}
C {lab_wire.sym} 225.0 -100.0 0 0 {name=w9 sig_type=std_logic lab=Vb}
N 150 -80.0 300 -80.0 {}
C {lab_wire.sym} 225.0 -80.0 0 0 {name=w10 sig_type=std_logic lab=Vthr}
N 150 -60.0 300 -60.0 {}
C {lab_wire.sym} 225.0 -60.0 0 0 {name=w11 sig_type=std_logic lab=VT_dpi}
N 150 -40.0 300 -40.0 {}
C {lab_wire.sym} 225.0 -40.0 0 0 {name=w12 sig_type=std_logic lab=VNA}
N 150 -20.0 300 -20.0 {}
C {lab_wire.sym} 225.0 -20.0 0 0 {name=w13 sig_type=std_logic lab=Vlk}
N 150 0.0 300 0.0 {}
C {lab_wire.sym} 225.0 0.0 0 0 {name=w14 sig_type=std_logic lab=VK}
N 150 20.0 300 20.0 {}
C {lab_wire.sym} 225.0 20.0 0 0 {name=w15 sig_type=std_logic lab=VIp}
N 150 40.0 300 40.0 {}
C {lab_wire.sym} 225.0 40.0 0 0 {name=w16 sig_type=std_logic lab=VKup}
N 150 60.0 300 60.0 {}
C {lab_wire.sym} 225.0 60.0 0 0 {name=w17 sig_type=std_logic lab=VKdn}
N 150 80.0 300 80.0 {}
C {lab_wire.sym} 225.0 80.0 0 0 {name=w18 sig_type=std_logic lab=Vamp_bias}
N -200 -160 280 -160 {}
N 280 -160 280 -140.0 {}
N 280 -140.0 300 -140.0 {}
C {gnd.sym} 300 -120.0 1 0 {name=g19 lab=0}
N 150 100.0 210 100.0 {}
C {lab_wire.sym} 180.0 100.0 0 0 {name=w20 sig_type=std_logic lab=VT}
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
* Reference: tt, 27 C, trim code 9 (see analog/testbenches/README.md)
.param vdd=3.3 code=9 vmon=1.65
* trim bits of 'code' (b3 = MSB), driven by Vtr3..Vtr0
.param b3='floor(code/8)-2*floor(code/16)' b2='floor(code/4)-2*floor(code/8)'
.param b1='floor(code/2)-2*floor(code/4)' b0='code-2*floor(code/2)'
.csparam code_c=\{code\}
.csparam vdd_c=\{vdd\}
.control
  save all
  op
  let tr = 1/(0.743 + (15 - code_c)*0.045133)
  let m = abs(i(Vmon))/(2.3072e-07*tr)
  let g_Vb = abs(i(v.xp.vp_vb))/1.442e-08
  let g_Vthr = abs(i(v.xp.vp_vthr))/7.367e-11
  let g_VT_dpi = abs(i(v.xp.vp_vt_dpi))/9.37e-11
  let g_VNA = abs(i(v.xp.vp_vna))/5.049e-06
  let g_Vlk = abs(i(v.xp.vp_vlk))/5.415e-10
  let g_VK = abs(i(v.xp.vp_vk))/1.752e-05
  let g_VIp = abs(i(v.xp.vp_vip))/2.402e-08
  let g_VKup = abs(i(v.xp.vp_vkup))/5.513e-07
  let g_VKdn = abs(i(v.xp.vp_vkdn))/3.418e-08
  let g_Vamp_bias = abs(i(v.xp.vp_vamp_bias))/9.654e-08
  let itot = abs(i(VIdd))
  echo RES m=$&m
  echo RES itot=$&itot
  echo RES vt=$&v(VT)
  echo RES v_Vb=$&v(Vb)
  let gm_Vb = g_Vb/m
  echo RES gm_Vb=$&gm_Vb
  set gm0_Vb = $&gm_Vb
  echo RES v_Vthr=$&v(Vthr)
  let gm_Vthr = g_Vthr/m
  echo RES gm_Vthr=$&gm_Vthr
  set gm0_Vthr = $&gm_Vthr
  echo RES v_VT_dpi=$&v(VT_dpi)
  let gm_VT_dpi = g_VT_dpi/m
  echo RES gm_VT_dpi=$&gm_VT_dpi
  set gm0_VT_dpi = $&gm_VT_dpi
  echo RES v_VNA=$&v(VNA)
  let gm_VNA = g_VNA/m
  echo RES gm_VNA=$&gm_VNA
  set gm0_VNA = $&gm_VNA
  echo RES v_Vlk=$&v(Vlk)
  let gm_Vlk = g_Vlk/m
  echo RES gm_Vlk=$&gm_Vlk
  set gm0_Vlk = $&gm_Vlk
  echo RES v_VK=$&v(VK)
  let gm_VK = g_VK/m
  echo RES gm_VK=$&gm_VK
  set gm0_VK = $&gm_VK
  echo RES v_VIp=$&v(VIp)
  let gm_VIp = g_VIp/m
  echo RES gm_VIp=$&gm_VIp
  set gm0_VIp = $&gm_VIp
  echo RES v_VKup=$&v(VKup)
  let gm_VKup = g_VKup/m
  echo RES gm_VKup=$&gm_VKup
  set gm0_VKup = $&gm_VKup
  echo RES v_VKdn=$&v(VKdn)
  let gm_VKdn = g_VKdn/m
  echo RES gm_VKdn=$&gm_VKdn
  set gm0_VKdn = $&gm_VKdn
  echo RES v_Vamp_bias=$&v(Vamp_bias)
  let gm_Vamp_bias = g_Vamp_bias/m
  echo RES gm_Vamp_bias=$&gm_Vamp_bias
  set gm0_Vamp_bias = $&gm_Vamp_bias

  * supply 2.97-3.63 V (+-10 %): worst |(g/m)(VDD) / (g/m)(3.3 V) - 1| per output
  dc V1 2.97 3.63 0.11
  let tr = 1/(0.743 + (15 - code_c)*0.045133)
  let m = abs(i(Vmon))/(2.3072e-07*tr)
  let g_Vb = abs(i(v.xp.vp_vb))/1.442e-08
  let g_Vthr = abs(i(v.xp.vp_vthr))/7.367e-11
  let g_VT_dpi = abs(i(v.xp.vp_vt_dpi))/9.37e-11
  let g_VNA = abs(i(v.xp.vp_vna))/5.049e-06
  let g_Vlk = abs(i(v.xp.vp_vlk))/5.415e-10
  let g_VK = abs(i(v.xp.vp_vk))/1.752e-05
  let g_VIp = abs(i(v.xp.vp_vip))/2.402e-08
  let g_VKup = abs(i(v.xp.vp_vkup))/5.513e-07
  let g_VKdn = abs(i(v.xp.vp_vkdn))/3.418e-08
  let g_Vamp_bias = abs(i(v.xp.vp_vamp_bias))/9.654e-08
  let e_Vb = abs(g_Vb/m/$gm0_Vb - 1)
  meas dc ev_Vb max e_Vb
  echo RES ev_Vb=$&ev_Vb
  let e_Vthr = abs(g_Vthr/m/$gm0_Vthr - 1)
  meas dc ev_Vthr max e_Vthr
  echo RES ev_Vthr=$&ev_Vthr
  let e_VT_dpi = abs(g_VT_dpi/m/$gm0_VT_dpi - 1)
  meas dc ev_VT_dpi max e_VT_dpi
  echo RES ev_VT_dpi=$&ev_VT_dpi
  let e_VNA = abs(g_VNA/m/$gm0_VNA - 1)
  meas dc ev_VNA max e_VNA
  echo RES ev_VNA=$&ev_VNA
  let e_Vlk = abs(g_Vlk/m/$gm0_Vlk - 1)
  meas dc ev_Vlk max e_Vlk
  echo RES ev_Vlk=$&ev_Vlk
  let e_VK = abs(g_VK/m/$gm0_VK - 1)
  meas dc ev_VK max e_VK
  echo RES ev_VK=$&ev_VK
  let e_VIp = abs(g_VIp/m/$gm0_VIp - 1)
  meas dc ev_VIp max e_VIp
  echo RES ev_VIp=$&ev_VIp
  let e_VKup = abs(g_VKup/m/$gm0_VKup - 1)
  meas dc ev_VKup max e_VKup
  echo RES ev_VKup=$&ev_VKup
  let e_VKdn = abs(g_VKdn/m/$gm0_VKdn - 1)
  meas dc ev_VKdn max e_VKdn
  echo RES ev_VKdn=$&ev_VKdn
  let e_Vamp_bias = abs(g_Vamp_bias/m/$gm0_Vamp_bias - 1)
  meas dc ev_Vamp_bias max e_Vamp_bias
  echo RES ev_Vamp_bias=$&ev_Vamp_bias

  * Imon pad: lowest pad voltage with Imon within 1 % of its 1.65 V value
  dc Vmon 0 3.3 0.01
  let imon = abs(i(Vmon))
  meas dc i165 find imon at=1.65
  let r = imon/i165
  meas dc imon_vmin when r=0.99 cross=1
  echo RES imon_vmin=$&imon_vmin
  if $?batchmode = 0
    plot r title 'Imon / Imon(1.65 V) vs pad voltage'
  end
.endc
"}
