v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {dpi_load_tb: DC output current of the synapses vs the membrane voltage. x1: excitatory DPI (DPI_sized; run_dpi_load.py --cell DPI swaps in the min-size DPI), output Isyn sources current into Out_e. x2: inhibitory DPI_inh, output Iout sinks current from Out_i. A DC current (p_iw1..3) is sunk from each tail; each output voltage is swept 0 to VDD. Measures the current at the reference voltage, the voltage where it has dropped by 1 % and 10 % (excitatory: as VMEM rises; inhibitory: as VMEM falls), and the current at VMEM = 0, 1.66 (threshold) and 3.2 V (spike).} -900 -700 0 0 0.3 0.3 {}
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
.param p_iw1=15n p_iw2=45n p_iw3=150n p_vref_e=0.5 p_vref_i=1.0 p_vstep=10m
.csparam vdd_c=\{p_vdd\}
.csparam vstep_c=\{p_vstep\}
.csparam iw1_c=\{p_iw1\}
.csparam iw2_c=\{p_iw2\}
.csparam iw3_c=\{p_iw3\}
.csparam vre_c=\{p_vref_e\}
.csparam vri_c=\{p_vref_i\}
* DC input current sunk from each tail (stands in for the DAC)
Iwe Isum_e 0 \{p_iw1\}
Iwi Isum_i 0 \{p_iw1\}
* Output held at a swept voltage (stands in for VMEM)
Voe Out_e 0 \{p_vref_e\}
Voi Out_i 0 \{p_vref_i\}
"}
C {devices/code_shown.sym} 400 -380 0 0 {name=ANALYSIS only_toplevel=false
value="
.control
  save all

  * input level 1
  alter iwe dc = $&iw1_c
  alter iwi dc = $&iw1_c
  dc Voe 0 $&vdd_c $&vstep_c
  let ie1 = i(voe)
  meas dc e1_ref find ie1 at=$&vre_c
  let l99 = 0.99*e1_ref
  let l90 = 0.90*e1_ref
  let e1_v99 = -1
  let e1_v90 = -1
  meas dc e1_v99 when ie1=$&l99 fall=last
  meas dc e1_v90 when ie1=$&l90 fall=last
  meas dc e1_at0 find ie1 at=0
  meas dc e1_at166 find ie1 at=1.66
  meas dc e1_at32 find ie1 at=3.2
  meas dc vsum_e1 find v(Isum_e) at=$&vre_c
  echo RES e1_ref=$&e1_ref
  echo RES e1_v99=$&e1_v99
  echo RES e1_v90=$&e1_v90
  echo RES e1_at0=$&e1_at0
  echo RES e1_at166=$&e1_at166
  echo RES e1_at32=$&e1_at32
  echo RES vsum_e1=$&vsum_e1
  wrdata dpi_load_tb_e1.txt ie1
  dc Voi 0 $&vdd_c $&vstep_c
  let ii1 = -i(voi)
  meas dc i1_ref find ii1 at=$&vri_c
  let l99 = 0.99*i1_ref
  let l90 = 0.90*i1_ref
  let i1_v99 = -1
  let i1_v90 = -1
  meas dc i1_v99 when ii1=$&l99 rise=1
  meas dc i1_v90 when ii1=$&l90 rise=1
  meas dc i1_at01 find ii1 at=0.1
  meas dc i1_at05 find ii1 at=0.5
  meas dc i1_at166 find ii1 at=1.66
  meas dc i1_at32 find ii1 at=3.2
  meas dc vsum_i1 find v(Isum_i) at=$&vri_c
  echo RES i1_ref=$&i1_ref
  echo RES i1_v99=$&i1_v99
  echo RES i1_v90=$&i1_v90
  echo RES i1_at01=$&i1_at01
  echo RES i1_at05=$&i1_at05
  echo RES i1_at166=$&i1_at166
  echo RES i1_at32=$&i1_at32
  echo RES vsum_i1=$&vsum_i1
  wrdata dpi_load_tb_i1.txt ii1
  * input level 2
  alter iwe dc = $&iw2_c
  alter iwi dc = $&iw2_c
  dc Voe 0 $&vdd_c $&vstep_c
  let ie2 = i(voe)
  meas dc e2_ref find ie2 at=$&vre_c
  let l99 = 0.99*e2_ref
  let l90 = 0.90*e2_ref
  let e2_v99 = -1
  let e2_v90 = -1
  meas dc e2_v99 when ie2=$&l99 fall=last
  meas dc e2_v90 when ie2=$&l90 fall=last
  meas dc e2_at0 find ie2 at=0
  meas dc e2_at166 find ie2 at=1.66
  meas dc e2_at32 find ie2 at=3.2
  meas dc vsum_e2 find v(Isum_e) at=$&vre_c
  echo RES e2_ref=$&e2_ref
  echo RES e2_v99=$&e2_v99
  echo RES e2_v90=$&e2_v90
  echo RES e2_at0=$&e2_at0
  echo RES e2_at166=$&e2_at166
  echo RES e2_at32=$&e2_at32
  echo RES vsum_e2=$&vsum_e2
  wrdata dpi_load_tb_e2.txt ie2
  dc Voi 0 $&vdd_c $&vstep_c
  let ii2 = -i(voi)
  meas dc i2_ref find ii2 at=$&vri_c
  let l99 = 0.99*i2_ref
  let l90 = 0.90*i2_ref
  let i2_v99 = -1
  let i2_v90 = -1
  meas dc i2_v99 when ii2=$&l99 rise=1
  meas dc i2_v90 when ii2=$&l90 rise=1
  meas dc i2_at01 find ii2 at=0.1
  meas dc i2_at05 find ii2 at=0.5
  meas dc i2_at166 find ii2 at=1.66
  meas dc i2_at32 find ii2 at=3.2
  meas dc vsum_i2 find v(Isum_i) at=$&vri_c
  echo RES i2_ref=$&i2_ref
  echo RES i2_v99=$&i2_v99
  echo RES i2_v90=$&i2_v90
  echo RES i2_at01=$&i2_at01
  echo RES i2_at05=$&i2_at05
  echo RES i2_at166=$&i2_at166
  echo RES i2_at32=$&i2_at32
  echo RES vsum_i2=$&vsum_i2
  wrdata dpi_load_tb_i2.txt ii2
  * input level 3
  alter iwe dc = $&iw3_c
  alter iwi dc = $&iw3_c
  dc Voe 0 $&vdd_c $&vstep_c
  let ie3 = i(voe)
  meas dc e3_ref find ie3 at=$&vre_c
  let l99 = 0.99*e3_ref
  let l90 = 0.90*e3_ref
  let e3_v99 = -1
  let e3_v90 = -1
  meas dc e3_v99 when ie3=$&l99 fall=last
  meas dc e3_v90 when ie3=$&l90 fall=last
  meas dc e3_at0 find ie3 at=0
  meas dc e3_at166 find ie3 at=1.66
  meas dc e3_at32 find ie3 at=3.2
  meas dc vsum_e3 find v(Isum_e) at=$&vre_c
  echo RES e3_ref=$&e3_ref
  echo RES e3_v99=$&e3_v99
  echo RES e3_v90=$&e3_v90
  echo RES e3_at0=$&e3_at0
  echo RES e3_at166=$&e3_at166
  echo RES e3_at32=$&e3_at32
  echo RES vsum_e3=$&vsum_e3
  wrdata dpi_load_tb_e3.txt ie3
  dc Voi 0 $&vdd_c $&vstep_c
  let ii3 = -i(voi)
  meas dc i3_ref find ii3 at=$&vri_c
  let l99 = 0.99*i3_ref
  let l90 = 0.90*i3_ref
  let i3_v99 = -1
  let i3_v90 = -1
  meas dc i3_v99 when ii3=$&l99 rise=1
  meas dc i3_v90 when ii3=$&l90 rise=1
  meas dc i3_at01 find ii3 at=0.1
  meas dc i3_at05 find ii3 at=0.5
  meas dc i3_at166 find ii3 at=1.66
  meas dc i3_at32 find ii3 at=3.2
  meas dc vsum_i3 find v(Isum_i) at=$&vri_c
  echo RES i3_ref=$&i3_ref
  echo RES i3_v99=$&i3_v99
  echo RES i3_v90=$&i3_v90
  echo RES i3_at01=$&i3_at01
  echo RES i3_at05=$&i3_at05
  echo RES i3_at166=$&i3_at166
  echo RES i3_at32=$&i3_at32
  echo RES vsum_i3=$&vsum_i3
  wrdata dpi_load_tb_i3.txt ii3
  echo RES iw1=$&iw1_c
  echo RES iw2=$&iw2_c
  echo RES iw3=$&iw3_c
  echo dpi_load_tb: done
.endc
"}
