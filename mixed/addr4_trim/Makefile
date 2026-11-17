# Mixed-signal simulation of the addr4_trim interface: snn_top_v2 (regs_v2,
# pulse_gen_v2) in Icarus Verilog; the 2-2-1 network, its bias cell and the
# trimmed reference current (trim_iref.va) in ngspice; coupled by SpiceBind.
# Same flow as ../Makefile (unchanged). Run from this folder in the container.
#
#   make run                               all scenarios (1-6, about 35 ms simulated)
#   make run SCEN_FIRST=6 SCEN_LAST=6      only the trim scenario
#   make run SCEN_FIRST=6 SCEN_LAST=6 PERR=0.82 TRIM="9 13"
#                                          slow chip, then trimmed back
#   make run SETTLE=500 RUN=1500           shorter windows (us)
#   make regs                              digital-only register test (tb_regs_v2.v, 1 s)
#   make vcd                               .raw -> .vcd
#   make clean
#
# TRIM: up to 4 trim codes for scenario 6, run in order.
# PERR: process error of the reference current (p_perr in snn_ms_tb_v2.sch).
# Outputs: snn_ms_tb_v2[__perr<PERR>].log/.raw; PERR = 1 gives no suffix.

HERE := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
ROOT := $(abspath $(HERE)/../..)
export PATH := /foss/tools/bin:$(PATH)

SCEN_FIRST ?= 1
SCEN_LAST  ?= 6
SETTLE     ?= 2000
RUN        ?= 3000
TRIM       ?= 9 15
PERR       ?= 1

ifneq ($(words $(TRIM)),$(filter 1 2 3 4,$(words $(TRIM))))
$(error TRIM takes 1 to 4 codes, got "$(TRIM)")
endif
# TRIM "9 15" -> 16'h00F9 (first code in the low nibble)
TRIM_HEX := $(shell v=0; i=0; for c in $(TRIM); do v=$$((v | (c & 15) << (4 * i))); i=$$((i + 1)); done; printf "16'h%04X" $$v)
N_TRIM   := $(words $(TRIM))

TAG  := $(if $(filter 1 1.0,$(PERR)),,__perr$(PERR))
OUT  := snn_ms_tb_v2$(TAG)

SPICEBIND := /foss/tools/spicebind
VSRC := sim.f $(shell grep -v '^//' sim.f)
PFX  := -Psnn_ms_tb_v2
SCHEMATICS := snn_ms_tb_v2.sch $(ROOT)/analog/snn/snn_analog.sch $(ROOT)/analog/snn/snn_analog.sym \
              $(wildcard $(ROOT)/analog/DAC/DAC.s* $(ROOT)/analog/DPI/DPI.s* \
                         $(ROOT)/analog/neuron/neuron_sized.s* $(ROOT)/analog/neuron/spike_amplifier.s* \
                         $(ROOT)/analog/neuron/bias_cell.s*)

.DEFAULT_GOAL := run
.PHONY: run regs vcd clean

# Verilog-A model of the trimmed reference current, loaded by pre_osdi in the netlist
trim_iref.osdi: trim_iref.va
	openvaf $< -o $@

# xschem resolves symbols from the current folder, so netlist from the project
# root with the project xschemrc. It exits with status 10 even after a good
# netlist, so check the file instead.
snn_ms_tb_v2.spice: $(SCHEMATICS)
	rm -f $@
	cd $(ROOT) && xschem --rcfile xschemrc -n -q -x -o $(HERE) -N $@ mixed/addr4_trim/snn_ms_tb_v2.sch || true
	@grep -q 'snn_analog$$' $@ || { echo "netlisting failed"; exit 1; }
	@grep -q 'bias_cell$$' $@ || { echo "netlist has no bias_cell"; exit 1; }
	@grep -q '^\.param p_perr=1$$' $@ || { echo "netlist has no '.param p_perr=1' line"; exit 1; }
	@! grep -n 'IS MISSING' $@ || { echo "netlist has missing symbols"; exit 1; }
	@d=$$(grep -i '^\.subckt' $@ | awk '{print tolower($$2)}' | sort | uniq -d); \
	  [ -z "$$d" ] || { echo "duplicate subckt names: $$d"; exit 1; }

# The netlist used for this run: PERR substituted
$(OUT)_run.spice: snn_ms_tb_v2.spice FORCE
	sed 's/^\.param p_perr=1$$/.param p_perr=$(PERR)/' $< > $@

no_passwd_shim.so: ../no_passwd_shim.c
	gcc -shared -fPIC -o $@ $<

run: $(OUT)_run.spice trim_iref.osdi no_passwd_shim.so $(VSRC)
	iverilog -g2012 -Wall -s snn_ms_tb_v2 -o $(OUT).vvp \
	  $(PFX).SCEN_FIRST=$(SCEN_FIRST) $(PFX).SCEN_LAST=$(SCEN_LAST) \
	  $(PFX).SETTLE=$(SETTLE) $(PFX).RUN=$(RUN) \
	  $(PFX).TRIM_CODES="$(TRIM_HEX)" $(PFX).N_TRIM=$(N_TRIM) -f sim.f
	@rm -f dump.raw
	@echo "PERR=$(PERR) TRIM=\"$(TRIM)\" scenarios $(SCEN_FIRST)-$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN) -> $(OUT).log"
	@start=$$(date +%s); \
	  { echo "# make run PERR=$(PERR) TRIM=\"$(TRIM)\" SCEN_FIRST=$(SCEN_FIRST) SCEN_LAST=$(SCEN_LAST) SETTLE=$(SETTLE) RUN=$(RUN)"; \
	    SPICE_NETLIST=$(HERE)/$(OUT)_run.spice HDL_INSTANCE=snn_ms_tb_v2.dut.u_snn_analog VCC=3.3 \
	    LOGIC_THRESHOLD_LOW=1.64 LOGIC_THRESHOLD_HIGH=1.66 \
	    LD_PRELOAD=$(HERE)/no_passwd_shim.so \
	    vvp -M $(SPICEBIND) -m spicebind_vpi $(OUT).vvp; } > $(OUT).log 2>&1; \
	  echo "simulation took $$(( $$(date +%s) - start )) s"
	@mv -f dump.raw $(OUT).raw
	@# ngspice's progress output uses \r, so split on it to find the testbench lines.
	@tr '\r' '\n' < $(OUT).log | grep -E 'snn_ms_tb_v2: |\*\* Error|singular|osdi' | awk '!seen[$$0]++'
	@tr '\r' '\n' < $(OUT).log | grep -q 'snn_ms_tb_v2: PASS,'

regs:
	iverilog -g2012 -Wall -s tb_regs_v2 -o tb_regs_v2.vvp tb_regs_v2.v snn_digital_v2.v regs_v2.v pulse_gen_v2.v
	vvp -n tb_regs_v2.vvp | grep 'tb_regs_v2:'

vcd: $(OUT).vcd
$(OUT).vcd: $(OUT).raw
	rawtovcd $< > $@

FORCE:

clean:
	rm -f no_passwd_shim.so trim_iref.osdi snn_ms_tb_v2.spice snn_ms_tb_v2*_run.spice \
	      snn_ms_tb_v2*.vvp snn_ms_tb_v2*.raw snn_ms_tb_v2*.log snn_ms_tb_v2*.vcd \
	      snn_ms_tb_v2_digital.vcd dump.raw tb_regs_v2.vvp tb_regs_v2.vcd
