v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {pre_b tied to spike (simplest drive)} -150 -400 0 0 0.25 0.25 {}
N -500 -50 -500 -30 {lab=vdd}
N -500 30 -500 50 {lab=#net1}
N -420 -50 -420 -30 {lab=vss}
N -420 30 -420 50 {lab=#net2}
N -340 -50 -340 -30 {lab=vref}
N -340 30 -340 50 {lab=#net3}
N -260 -50 -260 -30 {lab=spike}
N -260 30 -260 50 {lab=#net4}
N -180 -50 -180 -30 {lab=w0}
N -180 30 -180 50 {lab=#net5}
N -100 -50 -100 -30 {lab=w1}
N -100 30 -100 50 {lab=#net6}
N -20 -50 -20 -30 {lab=w2}
N -20 30 -20 50 {lab=#net7}
N 80 -50 80 -30 {lab=mem}
N 80 30 80 50 {lab=#net8}
N 140 -350 180 -350 {lab=vref}
N 140 -330 180 -330 {lab=spike}
N 140 -310 180 -310 {lab=spike}
N 140 -290 180 -290 {lab=w0}
N 140 -270 180 -270 {lab=w1}
N 140 -250 180 -250 {lab=w2}
N 420 -350 460 -350 {lab=vdd}
N 420 -330 460 -330 {lab=vss}
N 420 -310 460 -310 {lab=mem}
N -520 100 -520 140 {lab=GND}
C {devices/code_shown.sym} -900 -500 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {vsource.sym} -500 0 0 0 {name=Vdd value="3.3" savecurrent=false}
C {lab_pin.sym} -500 -50 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {vsource.sym} -420 0 0 0 {name=Vss value="0" savecurrent=false}
C {lab_pin.sym} -420 -50 0 1 {name=l3 sig_type=std_logic lab=vss}
C {vsource.sym} -340 0 0 0 {name=Vref value="\{vref\}" savecurrent=false}
C {lab_pin.sym} -340 -50 0 1 {name=l5 sig_type=std_logic lab=vref}
C {vsource.sym} -260 0 0 0 {name=Vspk value="pulse(0 3.3 5u 1n 1n 1u 10u)" savecurrent=false}
C {lab_pin.sym} -260 -50 0 1 {name=l7 sig_type=std_logic lab=spike}
C {vsource.sym} -180 0 0 0 {name=Vw0 value="\{w0\}" savecurrent=false}
C {lab_pin.sym} -180 -50 0 1 {name=l9 sig_type=std_logic lab=w0}
C {vsource.sym} -100 0 0 0 {name=Vw1 value="\{w1\}" savecurrent=false}
C {lab_pin.sym} -100 -50 0 1 {name=l11 sig_type=std_logic lab=w1}
C {vsource.sym} -20 0 0 0 {name=Vw2 value="\{w2\}" savecurrent=false}
C {lab_pin.sym} -20 -50 0 1 {name=l13 sig_type=std_logic lab=w2}
C {capa.sym} 80 0 0 0 {name=Cmem m=1 value=1p footprint=1206 device="ceramic capacitor"}
C {lab_pin.sym} 80 -50 0 1 {name=l15 sig_type=std_logic lab=mem}
C {charge_injection_DAC.sym} 300 -300 0 0 {name=x1}
C {lab_pin.sym} 140 -350 0 0 {name=l17 sig_type=std_logic lab=vref}
C {lab_pin.sym} 140 -330 0 0 {name=l18 sig_type=std_logic lab=spike}
C {lab_pin.sym} 140 -310 0 0 {name=l19 sig_type=std_logic lab=spike}
C {lab_pin.sym} 140 -290 0 0 {name=l20 sig_type=std_logic lab=w0}
C {lab_pin.sym} 140 -270 0 0 {name=l21 sig_type=std_logic lab=w1}
C {lab_pin.sym} 140 -250 0 0 {name=l22 sig_type=std_logic lab=w2}
C {lab_pin.sym} 460 -350 0 1 {name=l23 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 460 -330 0 1 {name=l24 sig_type=std_logic lab=vss}
C {lab_pin.sym} 460 -310 0 1 {name=l25 sig_type=std_logic lab=mem}
C {code_shown.sym} -900 250 0 0 {name=SIM only_toplevel=false value="
.param vref=3.3 w0=0 w1=0 w2=0
.ic v(mem)=0.2
.control
 echo weight  MEM after spikes 1..6 (start 0.2 V)
 foreach w 1 2 3 4 5 6 7
  let b0 = $w % 2
  let b1 = floor($w/2) % 2
  let b2 = floor($w/4) % 2
  let v0 = b0*3.3
  let v1 = b1*3.3
  let v2 = b2*3.3
  alterparam w0=$&v0
  alterparam w1=$&v1
  alterparam w2=$&v2
  reset
  tran 10n 60u uic
  meas tran m1 find v(mem) at=9.9u
  meas tran m2 find v(mem) at=19.9u
  meas tran m3 find v(mem) at=29.9u
  meas tran m4 find v(mem) at=39.9u
  meas tran m5 find v(mem) at=49.9u
  meas tran m6 find v(mem) at=59.9u
  echo $w $&m1 $&m2 $&m3 $&m4 $&m5 $&m6
  if $w = 7
   plot v(mem) v(spike)
  end
 end
.endc
"}
C {gnd.sym} -520 140 0 0 {name=l26 lab=GND}
C {lab_wire.sym} -520 120 0 0 {name=p1 sig_type=std_logic lab=GND}
C {lab_wire.sym} -500 50 0 0 {name=p2 sig_type=std_logic lab=GND}
C {lab_wire.sym} -420 50 0 0 {name=p3 sig_type=std_logic lab=GND}
C {lab_wire.sym} -340 50 0 0 {name=p4 sig_type=std_logic lab=GND}
C {lab_wire.sym} -260 50 0 0 {name=p5 sig_type=std_logic lab=GND}
C {lab_wire.sym} -180 50 0 0 {name=p6 sig_type=std_logic lab=GND}
C {lab_wire.sym} -100 50 0 0 {name=p7 sig_type=std_logic lab=GND}
C {lab_wire.sym} -20 50 0 0 {name=p8 sig_type=std_logic lab=GND}
C {lab_wire.sym} 80 50 0 0 {name=p9 sig_type=std_logic lab=GND}
