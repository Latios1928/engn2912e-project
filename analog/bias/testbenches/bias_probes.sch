v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_probes: one copy of the device each bias pin drives in snn_analog (main), drain held at its gate voltage by a unity VCVS (no load on the pin), par=1e6 so it has no mismatch of its own. The current through Vp_<pin> is what that pin would set in the network.} -1100 -950 0 0 0.3 0.3 {}
C {iopin.sym} -900 -800 0 0 {name=p0 lab=VDD}
C {iopin.sym} -900 -770 0 0 {name=p1 lab=VSS}
C {iopin.sym} -900 -740 0 0 {name=p2 lab=Vb}
C {iopin.sym} -900 -710 0 0 {name=p3 lab=Vthr}
C {iopin.sym} -900 -680 0 0 {name=p4 lab=VT_dpi}
C {iopin.sym} -900 -650 0 0 {name=p5 lab=VNA}
C {iopin.sym} -900 -620 0 0 {name=p6 lab=Vlk}
C {iopin.sym} -900 -590 0 0 {name=p7 lab=VK}
C {iopin.sym} -900 -560 0 0 {name=p8 lab=VIp}
C {iopin.sym} -900 -530 0 0 {name=p9 lab=VKup}
C {iopin.sym} -900 -500 0 0 {name=p10 lab=VKdn}
C {iopin.sym} -900 -470 0 0 {name=p11 lab=Vamp_bias}
C {devices/code_shown.sym} -600 -800 0 0 {name=PROBES only_toplevel=false
value="
* probe per bias pin: E holds the drain at the gate voltage, Vp measures the current
E_Vb pd_Vb VSS Vb VSS 1
X_Vb pd_Vb Vb ps_Vb VSS nfet_03v3 L=8.0u W=1.0u nf=1 par=1e6
Vp_Vb ps_Vb VSS 0
E_Vthr pd_Vthr VSS Vthr VSS 1
X_Vthr pd_Vthr Vthr ps_Vthr VDD pfet_03v3 L=0.28u W=0.22u nf=1 par=1e6
Vp_Vthr VDD ps_Vthr 0
E_VT_dpi pd_VT_dpi VSS VT_dpi VSS 1
X_VT_dpi pd_VT_dpi VT_dpi ps_VT_dpi VDD pfet_03v3 L=0.28u W=0.22u nf=1 par=1e6
Vp_VT_dpi VDD ps_VT_dpi 0
E_VNA pd_VNA VSS VNA VSS 1
X_VNA pd_VNA VNA ps_VNA VDD pfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_VNA VDD ps_VNA 0
E_Vlk pd_Vlk VSS Vlk VSS 1
X_Vlk pd_Vlk Vlk ps_Vlk VSS nfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_Vlk ps_Vlk VSS 0
E_VK pd_VK VSS VK VSS 1
X_VK pd_VK VK ps_VK VSS nfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_VK ps_VK VSS 0
E_VIp pd_VIp VSS VIp VSS 1
X_VIp pd_VIp VIp ps_VIp VSS nfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_VIp ps_VIp VSS 0
E_VKup pd_VKup VSS VKup VSS 1
X_VKup pd_VKup VKup ps_VKup VDD pfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_VKup VDD ps_VKup 0
E_VKdn pd_VKdn VSS VKdn VSS 1
X_VKdn pd_VKdn VKdn ps_VKdn VSS nfet_03v3 L=1.0u W=1.0u nf=1 par=1e6
Vp_VKdn ps_VKdn VSS 0
E_Vamp_bias pd_Vamp_bias VSS Vamp_bias VSS 1
X_Vamp_bias pd_Vamp_bias Vamp_bias ps_Vamp_bias VSS nfet_03v3 L=0.28u W=0.22u nf=1 par=1e6
Vp_Vamp_bias ps_Vamp_bias VSS 0
"}
