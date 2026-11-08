v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {snn_analog.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -150 -160 0 0 {name=l0 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -150 -140 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -150 -120 0 0 {name=l2 sig_type=std_logic lab=w[91:0]}
C {lab_pin.sym} -150 -100 0 0 {name=l3 sig_type=std_logic lab=pulse[2:0]}
C {lab_pin.sym} -150 -80 0 0 {name=l4 sig_type=std_logic lab=Vb}
C {lab_pin.sym} -150 -60 0 0 {name=l5 sig_type=std_logic lab=Vthr_in}
C {lab_pin.sym} -150 -40 0 0 {name=l6 sig_type=std_logic lab=Vthr_hid}
C {lab_pin.sym} -150 -20 0 0 {name=l7 sig_type=std_logic lab=Vthr_out}
C {lab_pin.sym} -150 0 0 0 {name=l8 sig_type=std_logic lab=VT_dpi}
C {lab_pin.sym} -150 20 0 0 {name=l9 sig_type=std_logic lab=VNA}
C {lab_pin.sym} -150 40 0 0 {name=l10 sig_type=std_logic lab=Vlk}
C {lab_pin.sym} -150 60 0 0 {name=l11 sig_type=std_logic lab=VK}
C {lab_pin.sym} -150 80 0 0 {name=l12 sig_type=std_logic lab=VIp}
C {lab_pin.sym} -150 100 0 0 {name=l13 sig_type=std_logic lab=VKup}
C {lab_pin.sym} -150 120 0 0 {name=l14 sig_type=std_logic lab=VKdn}
C {lab_pin.sym} -150 140 0 0 {name=l15 sig_type=std_logic lab=Vamp_bias}
C {lab_pin.sym} -150 160 0 0 {name=l16 sig_type=std_logic lab=VT}
C {lab_pin.sym} 150 0 0 1 {name=lsp sig_type=std_logic lab=spike[8:0]}
C {devices/code_shown.sym} -700 -300 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
C {devices/code_shown.sym} -700 -120 0 0 {name=DIGITAL only_toplevel=true
value="
* Digital side (rf, pulse generators, test sequencer): one d_cosim model.
* lib.spice and sim_params.spice are written by the Makefile; run ngspice from mixed/.
.include lib.spice
.include sim_params.spice
"}
C {devices/code_shown.sym} 300 -300 0 0 {name=SOURCES only_toplevel=true
value="
* Supplies and biases, as in analog/neuron/DACs-DPI-neuron.sch
* Parameter names start with p_: a .param with the same name as a net made ngspice
* rename that net to \{name\} on the long x1 line, leaving the biases unconnected.
.param p_vdd=3.3 p_vtau=0.40 p_iref=14.42n
.param p_vthr_in=2.909 p_vthr_hid=2.909 p_vthr_out=2.909
.param p_vlk=0.425 p_vamp_bias=0.535 p_vip=0.573 p_vna=1.93 p_vkup=2.35 p_vk=1.22 p_vkdn=0.588 p_vt=1.66
Vdd VDD 0 \{p_vdd\}
Vss VSS 0 0
* DAC unit current: Iref into a diode-connected unit current source (w[0] = 15 nA)
Iref VDD Vb \{p_iref\}
XMref Vb Vb 0 0 nfet_03v3 L=8u W=1u nf=1
Vthr_in Vthr_in 0 \{p_vthr_in\}
Vthr_hid Vthr_hid 0 \{p_vthr_hid\}
Vthr_out Vthr_out 0 \{p_vthr_out\}
Vtau VDD VT_dpi \{p_vtau\}
Vlk Vlk VSS \{p_vlk\}
VK VK VSS \{p_vk\}
VNA VNA VSS \{p_vna\}
VKup VKup VSS \{p_vkup\}
VKdn VKdn VSS \{p_vkdn\}
VIp VIp VSS \{p_vip\}
VT VT VSS \{p_vt\}
Vamp_bias Vamp_bias VSS \{p_vamp_bias\}
* Clocks: clk 1 us (rf, sequencer), clk_analog 10 us (pulse generators)
Vclk clk 0 pulse(0 \{p_vdd\} 0.5u 10n 10n 0.49u 1u)
Vclka clk_analog 0 pulse(0 \{p_vdd\} 5u 10n 10n 4.99u 10u)
"}
C {devices/code_shown.sym} 300 250 0 0 {name=TRAN only_toplevel=true
value="
* Gear integration: trap makes the DPI output current ring after each reset (entry 46)
.options method=gear
.csparam tstop_c=\{tstop\}
.control
* Weights are not saved: they are static during a run and 92 traces made the .raw ~0.5 GB.
  save spike[0] spike[1] spike[2] spike[3] spike[4] spike[5] spike[6] spike[7] spike[8] pulse[0] pulse[1] pulse[2] scen[0] scen[1] scen[2] running done x1.VMEM_0 x1.VMEM_1 x1.VMEM_2 x1.VMEM_3 x1.VMEM_4 x1.VMEM_5 x1.VMEM_6 x1.VMEM_7 x1.VMEM_8
  tran 0.5u $&tstop_c 0 0.5u
  write snn_ms_tb.raw
.endc
"}
T {Mixed-signal testbench: digital rf + pulse generators + test sequencer (Verilog, d_cosim)
driving the analog 3-5-1 network snn_analog. The sequencer prints PASS/FAIL per scenario.
Run with make -C mixed run (see mixed/README.md).} -700 -500 0 0 0.4 0.4 {}
