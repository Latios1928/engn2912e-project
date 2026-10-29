v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -480 -60 -480 -40 {lab=vdd}
N -480 20 -480 40 {lab=GND}
N -380 -60 -380 -40 {lab=vbias}
N -380 20 -380 40 {lab=GND}
N -280 -60 -280 -40 {lab=spike_b}
N -280 20 -280 40 {lab=GND}
N -180 -60 -180 -40 {lab=iout}
N -180 20 -180 40 {lab=GND}
N 0 -60 0 -40 {lab=t1_b}
N 0 20 0 40 {lab=GND}
N 100 -60 100 -40 {lab=t2_b}
N 100 20 100 40 {lab=GND}
N 190 -60 190 -40 {lab=t3_b}
N 190 20 190 40 {lab=GND}
N 280 -60 280 -40 {lab=t4_b}
N 280 20 280 40 {lab=GND}
N 370 -60 370 -40 {lab=t5_b}
N 370 20 370 40 {lab=GND}
N 460 -60 460 -40 {lab=t6_b}
N 460 20 460 40 {lab=GND}
N 550 -60 550 -40 {lab=t7_b}
N 550 20 550 40 {lab=GND}
N 140 -380 180 -380 {lab=vbias}
N 140 -360 180 -360 {lab=spike_b}
N 140 -340 180 -340 {lab=t1_b}
N 140 -320 180 -320 {lab=t2_b}
N 140 -300 180 -300 {lab=t3_b}
N 140 -280 180 -280 {lab=t4_b}
N 140 -260 180 -260 {lab=t5_b}
N 140 -240 180 -240 {lab=t6_b}
N 140 -220 180 -220 {lab=t7_b}
N 420 -380 460 -380 {lab=vdd}
N 420 -360 460 -360 {lab=iout}
C {devices/code_shown.sym} -900 -500 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {vsource.sym} -480 -10 0 0 {name=Vdd value="3.3" savecurrent=false}
C {lab_pin.sym} -480 -60 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -480 40 0 1 {name=l2 sig_type=std_logic lab=GND}
C {vsource.sym} -380 -10 0 0 {name=Vb value="\{vbp\}" savecurrent=false}
C {lab_pin.sym} -380 -60 0 1 {name=l3 sig_type=std_logic lab=vbias}
C {lab_pin.sym} -380 40 0 1 {name=l4 sig_type=std_logic lab=GND}
C {vsource.sym} -280 -10 0 0 {name=Vspk value="\{vspk\}" savecurrent=false}
C {lab_pin.sym} -280 -60 0 1 {name=l5 sig_type=std_logic lab=spike_b}
C {lab_pin.sym} -280 40 0 1 {name=l6 sig_type=std_logic lab=GND}
C {vsource.sym} -180 -10 0 0 {name=Vmem value="\{vmem\}" savecurrent=false}
C {lab_pin.sym} -180 -60 0 1 {name=l7 sig_type=std_logic lab=iout}
C {lab_pin.sym} -180 40 0 1 {name=l8 sig_type=std_logic lab=GND}
C {vsource.sym} 0 -10 0 0 {name=Vt1 value="\{code>=1?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 0 -60 0 1 {name=l9 sig_type=std_logic lab=t1_b}
C {lab_pin.sym} 0 40 0 1 {name=l10 sig_type=std_logic lab=GND}
C {vsource.sym} 100 -10 0 0 {name=Vt2 value="\{code>=2?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 100 -60 0 1 {name=l11 sig_type=std_logic lab=t2_b}
C {lab_pin.sym} 100 40 0 1 {name=l12 sig_type=std_logic lab=GND}
C {vsource.sym} 190 -10 0 0 {name=Vt3 value="\{code>=3?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 190 -60 0 1 {name=l13 sig_type=std_logic lab=t3_b}
C {lab_pin.sym} 190 40 0 1 {name=l14 sig_type=std_logic lab=GND}
C {vsource.sym} 280 -10 0 0 {name=Vt4 value="\{code>=4?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 280 -60 0 1 {name=l15 sig_type=std_logic lab=t4_b}
C {lab_pin.sym} 280 40 0 1 {name=l16 sig_type=std_logic lab=GND}
C {vsource.sym} 370 -10 0 0 {name=Vt5 value="\{code>=5?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 370 -60 0 1 {name=l17 sig_type=std_logic lab=t5_b}
C {lab_pin.sym} 370 40 0 1 {name=l18 sig_type=std_logic lab=GND}
C {vsource.sym} 460 -10 0 0 {name=Vt6 value="\{code>=6?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 460 -60 0 1 {name=l19 sig_type=std_logic lab=t6_b}
C {lab_pin.sym} 460 40 0 1 {name=l20 sig_type=std_logic lab=GND}
C {vsource.sym} 550 -10 0 0 {name=Vt7 value="\{code>=7?0:3.3\}" savecurrent=false}
C {lab_pin.sym} 550 -60 0 1 {name=l21 sig_type=std_logic lab=t7_b}
C {lab_pin.sym} 550 40 0 1 {name=l22 sig_type=std_logic lab=GND}
C {unary_DAC.sym} 300 -300 0 0 {name=x1}
C {lab_pin.sym} 140 -380 0 0 {name=l23 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 140 -360 0 0 {name=l24 sig_type=std_logic lab=spike_b}
C {lab_pin.sym} 140 -340 0 0 {name=l25 sig_type=std_logic lab=t1_b}
C {lab_pin.sym} 140 -320 0 0 {name=l26 sig_type=std_logic lab=t2_b}
C {lab_pin.sym} 140 -300 0 0 {name=l27 sig_type=std_logic lab=t3_b}
C {lab_pin.sym} 140 -280 0 0 {name=l28 sig_type=std_logic lab=t4_b}
C {lab_pin.sym} 140 -260 0 0 {name=l29 sig_type=std_logic lab=t5_b}
C {lab_pin.sym} 140 -240 0 0 {name=l30 sig_type=std_logic lab=t6_b}
C {lab_pin.sym} 140 -220 0 0 {name=l31 sig_type=std_logic lab=t7_b}
C {lab_pin.sym} 460 -380 0 1 {name=l32 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 460 -360 0 1 {name=l33 sig_type=std_logic lab=iout}
C {code_shown.sym} -900 250 0 0 {name=SIM only_toplevel=false value="
.param vbp=2.6 vmem=1.0 code=0 vspk=0
.control
 echo code  Iout(spike on)  Iout(spike off)
 foreach c 0 1 2 3 4 5 6 7
  alterparam code=$c
  alterparam vspk=0
  reset
  op
  let on = -i(vmem)
  set ion = "$&on"
  alterparam vspk=3.3
  reset
  op
  let off = -i(vmem)
  echo $c $ion $&off
 end
.endc
"}
