# Mixed-signal simulation: snn_top (regs, pulse_gen) in Icarus Verilog; the
# analog macro SNN_signed (its LVS reference netlist) in ngspice; coupled by
# SpiceBind. Run from this folder in the container.
#
#   make run                               scenarios 1-8 (about 58 ms simulated)
#   make run SCEN_FIRST=5 SCEN_LAST=5      one scenario
#   make run IREF=82n                      other Iref (default 100n)
#   make run SETTLE=2000 RUN=1500          shorter windows (us)
#   make regs                              ../digital/tb_snn_digital.v
#   make vcd                               .raw -> .vcd
#   make clean
#
# Outputs: snn_ms_tb[__iref<IREF>].log/.raw.

HERE := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
ROOT := $(abspath $(HERE)/..)
export PATH := /foss/tools/bin:$(PATH)

SCEN_FIRST ?= 1
SCEN_LAST  ?= 8
SETTLE     ?= 4000
RUN        ?= 3000
IREF       ?= 100n

PDK_ROOT ?= /foss/pdks
PDK      ?= gf180mcuD
MODELS   := $(PDK_ROOT)/$(PDK)/libs.tech/ngspice
MACRO    := $(ROOT)/analog/layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice

TAG  := $(if $(filter 100n,$(IREF)),,__iref$(IREF))
OUT  := snn_ms_tb$(TAG)

SPICEBIND := /foss/tools/spicebind
VSRC := sim.f $(shell grep -v '^//' sim.f)
PFX  := -Psnn_ms_tb

.DEFAULT_GOAL := run
.PHONY: run regs vcd clean

# Simulation copy of the macro netlist: long FETs split, MIM cap model renamed
macro_sim.spice: $(MACRO) macro_sim.py
	python3 macro_sim.py $< $@

# The netlist used for this run: paths and IREF filled in
$(OUT)_run.spice: snn_ms_tb.spice macro_sim.spice FORCE
	sed -e 's|@PDK@|$(MODELS)|' -e 's|@MACRO@|$(HERE)/macro_sim.spice|' -e 's/p_iref=100n/p_iref=$(IREF)/' $< > $@

no_passwd_shim.so: no_passwd_shim.c
	gcc -shared -fPIC -o $@ $<

run: $(OUT)_run.spice no_passwd_shim.so $(VSRC)
	iverilog -g2012 -Wall -s snn_ms_tb -o $(OUT).vvp \
	  $(PFX).SCEN_FIRST=$(SCEN_FIRST) $(PFX).SCEN_LAST=$(SCEN_LAST) \
	  $(PFX).SETTLE=$(SETTLE) $(PFX).RUN=$(RUN) -f sim.f
	@rm -f dump.raw
	@echo "IREF=$(IREF) scenarios $(SCEN_FIRST)-$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN) -> $(OUT).log"
	@start=$$(date +%s); \
	  { echo "# make run IREF=$(IREF) SCEN_FIRST=$(SCEN_FIRST) SCEN_LAST=$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN)"; \
	    SPICE_DUMP_RAW=1 SPICE_NETLIST=$(HERE)/$(OUT)_run.spice HDL_INSTANCE=snn_ms_tb.dut.u_snn_analog VCC=3.3 \
	    LOGIC_THRESHOLD_LOW=1.64 LOGIC_THRESHOLD_HIGH=1.66 \
	    LD_PRELOAD=$(HERE)/no_passwd_shim.so \
	    vvp -M $(SPICEBIND) -m spicebind_vpi $(OUT).vvp; } > $(OUT).log 2>&1; \
	  echo "simulation took $$(( $$(date +%s) - start )) s"
	@mv -f dump.raw $(OUT).raw
	@# ngspice's progress output uses \r, so split on it to find the testbench lines.
	@tr '\r' '\n' < $(OUT).log | grep -E 'snn_ms_tb: |\*\* Error|singular' | awk '!seen[$$0]++'
	@tr '\r' '\n' < $(OUT).log | grep -q 'snn_ms_tb: PASS,'

regs:
	cd $(ROOT)/digital && iverilog -g2012 -Wall -o sim.vvp tb_snn_digital.v snn_digital.v regs.v pulse_gen.v
	cd $(ROOT)/digital && vvp -n sim.vvp | grep 'tb_snn_digital:'

vcd: $(OUT).vcd
$(OUT).vcd: $(OUT).raw
	rawtovcd $< > $@

FORCE:

clean:
	rm -f no_passwd_shim.so snn_ms_tb*_run.spice snn_ms_tb*.vvp snn_ms_tb*.raw \
	      snn_ms_tb*.log snn_ms_tb*.vcd snn_ms_tb_digital.vcd dump.raw macro_sim.spice
