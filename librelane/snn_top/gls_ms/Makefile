# Gate-level mixed-signal simulation of snn_top: the LibreLane netlist (GF180 standard
# cells) in Icarus Verilog, the analog macro SNN_signed (its LVS reference netlist) in
# ngspice, coupled by SpiceBind. Same testbench, SPICE side and options as ../../../mixed
# (which runs the RTL); only the digital side differs. Run in the container, from here.
#
#   make run                               scenarios 1-8 (about 58 ms simulated)
#   make run SCEN_FIRST=2 SCEN_LAST=2      one scenario
#   make run SETTLE=2000 RUN=1500          shorter windows (us)
#   make run NETLIST=path/to/x.nl.v        another netlist (default: results/, the published run)
#   make run PEX=1                         macro with its extracted parasitics (C-only Magic
#                                          extraction of SNN_signed.gds) instead of its LVS netlist
#   make clean
#
# Outputs: gls_ms.log / .raw (analog, incl. supply current i(Vdd)) / _digital.vcd (gate-level
# netlist activity), gls_ms_pex.* with PEX=1. Power: tools/snn_power.py. Nothing in mixed/ is modified: prep.py writes
# simulation copies of the netlist and the testbench here.

HERE := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
ROOT := $(abspath $(HERE)/../../..)
MIXED := $(ROOT)/mixed
export PATH := /foss/tools/bin:$(PATH)

SCEN_FIRST ?= 1
SCEN_LAST  ?= 8
SETTLE     ?= 4000
RUN        ?= 3000
IREF       ?= 100n
NETLIST    ?= $(ROOT)/librelane/snn_top/results/snn_top.nl.v
PEX        ?= 0

PDK_ROOT ?= /foss/pdks
PDK      ?= gf180mcuD
MODELS   := $(PDK_ROOT)/$(PDK)/libs.tech/ngspice
CELLS    := $(PDK_ROOT)/$(PDK)/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog
MACRO    := $(ROOT)/analog/layout_tools/top/SNN_signed/SNN_signed_lvs_ref.spice
MACRO_PEX := $(ROOT)/analog/layout_tools/top/SNN_signed/pex/SNN_signed_pex_sim.spice
OUT      := $(if $(filter 1,$(PEX)),gls_ms_pex,gls_ms)
MACRO_SIM := $(if $(filter 1,$(PEX)),macro_pex.spice,macro_sim.spice)
SPICEBIND := /foss/tools/spicebind
PFX := -Psnn_ms_tb

VSRC := $(CELLS)/primitives.v $(CELLS)/gf180mcu_fd_sc_mcu7t5v0.v snn_top_gls.nl.v \
        $(ROOT)/analog/snn/snn_analog.v snn_ms_tb_gls.v

.DEFAULT_GOAL := run
.PHONY: run clean

snn_top_gls.nl.v snn_ms_tb_gls.v: $(NETLIST) $(MIXED)/snn_ms_tb.v prep.py
	python3 prep.py $(NETLIST) $(MIXED)/snn_ms_tb.v snn_top_gls.nl.v snn_ms_tb_gls.v

macro_sim.spice: $(MACRO) $(MIXED)/macro_sim.py
	python3 $(MIXED)/macro_sim.py $< $@

macro_pex.spice: $(MACRO_PEX) $(MACRO) $(MIXED)/pex_macro.py
	python3 $(MIXED)/pex_macro.py $(MACRO_PEX) $(MACRO) $@

$(OUT)_run.spice: $(MIXED)/snn_ms_tb.spice $(MACRO_SIM) FORCE
	sed -e 's|@PDK@|$(MODELS)|' -e 's|@MACRO@|$(HERE)/$(MACRO_SIM)|' -e 's/p_iref=100n/p_iref=$(IREF)/' \
	    -e '/^\.save v(spike\[0\])/i .save i(Vdd) i(VT)' $< > $@
	@grep -q '^\.save i(Vdd)' $@ || { echo "could not add the supply-current .save"; exit 1; }

no_passwd_shim.so: $(MIXED)/no_passwd_shim.c
	gcc -shared -fPIC -o $@ $<

# FUNCTIONAL: cell models without delays
run: $(OUT)_run.spice no_passwd_shim.so $(VSRC)
	iverilog -g2012 -DFUNCTIONAL -s snn_ms_tb -o $(OUT).vvp \
	  $(PFX).SCEN_FIRST=$(SCEN_FIRST) $(PFX).SCEN_LAST=$(SCEN_LAST) \
	  $(PFX).SETTLE=$(SETTLE) $(PFX).RUN=$(RUN) $(VSRC)
	@rm -f dump.raw
	@echo "GLS + SPICE (PEX=$(PEX)): IREF=$(IREF) scenarios $(SCEN_FIRST)-$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN) -> $(OUT).log"
	@start=$$(date +%s); \
	  { echo "# make run PEX=$(PEX) IREF=$(IREF) SCEN_FIRST=$(SCEN_FIRST) SCEN_LAST=$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN) NETLIST=$(NETLIST)"; \
	    SPICE_DUMP_RAW=1 SPICE_NETLIST=$(HERE)/$(OUT)_run.spice HDL_INSTANCE=snn_ms_tb.dut.u_snn_analog VCC=3.3 \
	    LOGIC_THRESHOLD_LOW=1.64 LOGIC_THRESHOLD_HIGH=1.66 \
	    LD_PRELOAD=$(HERE)/no_passwd_shim.so \
	    vvp -M $(SPICEBIND) -m spicebind_vpi $(OUT).vvp; } > $(OUT).log 2>&1; \
	  echo "simulation took $$(( $$(date +%s) - start )) s"
	@mv -f dump.raw $(OUT).raw
	@mv -f snn_ms_tb_digital.vcd $(OUT)_digital.vcd
	@tr '\r' '\n' < $(OUT).log | grep -E 'snn_ms_tb: |\*\* Error|singular' | awk '!seen[$$0]++'
	@tr '\r' '\n' < $(OUT).log | grep -q 'snn_ms_tb: PASS,'

FORCE:

clean:
	rm -f no_passwd_shim.so gls_ms*_run.spice macro_sim.spice macro_pex.spice snn_top_gls.nl.v \
	      snn_ms_tb_gls.v gls_ms*.vvp gls_ms*.raw gls_ms*.log dump.raw *.vcd
