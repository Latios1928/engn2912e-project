# Mixed-signal simulation of the SNN: digital rf + pulse generators + test
# sequencer (Verilog, built into one d_cosim model) driving the analog 3-5-1
# network (analog/snn/snn_analog.sch). See README.md.
# Adapted from the CAD7 Makefile of engn1600-team1:
#   https://github.com/mgyee/engn1600-team1
#
#   make run                      all scenarios (0-4, about 20 ms simulated)
#   make run SCEN_FIRST=3 SCEN_LAST=3   one scenario
#   make vcd                      snn_ms_tb.raw -> snn_ms_tb.vcd
#   make clean

MIXED := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
ROOT  := $(abspath $(MIXED)/..)
TOOLS := /foss/tools/bin
export PATH := $(TOOLS):$(PATH)

SCEN_FIRST ?= 0
SCEN_LAST  ?= 4
SETTLE     ?= 2000   # clk cycles (1 us) with in = 0 before each scenario
RUN        ?= 3000   # clk cycles with in applied

TOP  := snn_digital
VSRC := snn_digital.v snn_sequencer.v $(ROOT)/digital/rf.v $(ROOT)/analog/mock/pulse_gen.v
GEN  := -GSCEN_FIRST=$(SCEN_FIRST) -GSCEN_LAST=$(SCEN_LAST) -GSETTLE=$(SETTLE) -GRUN=$(RUN)

# Simulated time: 46 us to load each scenario's weights + SETTLE + RUN, plus margin.
NSCEN := $(shell f=$(SCEN_FIRST); [ $$f -lt 1 ] && f=1; echo $$(( $(SCEN_LAST) - f + 1 )))
TSTOP := $(shell echo "$(NSCEN) * ($(SETTLE) + $(RUN) + 50) + 200" | bc)u

SCHEMATICS := snn_ms_tb.sch $(ROOT)/analog/snn/snn_analog.sch $(ROOT)/analog/snn/snn_analog.sym \
              $(wildcard $(ROOT)/analog/neuron/DAC.s* $(ROOT)/analog/neuron/DPI.s* \
                         $(ROOT)/analog/neuron/neuron_sized.s* $(ROOT)/analog/neuron/spike_amplifier.s*)

.PHONY: all run vcd netlist lib clean

all: run

# The .so depends on the scenario parameters, so record them and rebuild on change.
build.cfg: FORCE
	@echo "$(GEN)" | cmp -s - $@ || echo "$(GEN)" > $@

$(TOP).so: $(VSRC) build.cfg vlnggen.sh
	rm -rf $(TOP)_obj_dir
	./vlnggen.sh -Wno-fatal $(GEN) --top-module $(TOP) $(VSRC)

lib.spice: $(TOP).so instantiate.py
	python3 instantiate.py --obj-dir $(TOP)_obj_dir --module $(TOP) --so $(MIXED)/$(TOP).so > $@

sim_params.spice: build.cfg
	echo ".param tstop=$(TSTOP)" > $@

lib: lib.spice

# xschem resolves symbols from the current folder, so netlist from the project
# root with the project xschemrc (feedback.typ, entry 47).
#   xschem exits with status 10 even after a good netlist, so check the file instead.
snn_ms_tb.spice: $(SCHEMATICS)
	rm -f $@
	cd $(ROOT) && xschem --rcfile xschemrc -n -q -x -o $(MIXED) -N $@ mixed/snn_ms_tb.sch || true
	@grep -q '^x1 .* snn_analog' $@ || grep -q 'snn_analog$$' $@ || { echo "netlisting failed"; exit 1; }
	@! grep -n 'IS MISSING' $@ || { echo "netlist has missing symbols"; exit 1; }
	@d=$$(grep -i '^\.subckt' $@ | awk '{print tolower($$2)}' | sort | uniq -d); \
	  [ -z "$$d" ] || { echo "duplicate subckt names: $$d"; exit 1; }

netlist: snn_ms_tb.spice

run: snn_ms_tb.spice lib.spice sim_params.spice
	@echo "Simulating $(TSTOP) (scenarios $(SCEN_FIRST)-$(SCEN_LAST))"
	@# ngspice's progress output uses \r, so $$display lines land mid-line: split on \r.
	@start=$$(date +%s); ngspice -b snn_ms_tb.spice > snn_ms_tb.log 2>&1; \
	  echo "ngspice took $$(( $$(date +%s) - start )) s"
	@tr '\r' '\n' < snn_ms_tb.log | grep -oE 'snn_sequencer: .*|.*(rror|abort|singular).*' | awk '!seen[$$0]++'
	@tr '\r' '\n' < snn_ms_tb.log | grep -q 'snn_sequencer: PASS,'

vcd: snn_ms_tb.vcd
snn_ms_tb.vcd: snn_ms_tb.raw raw2vcd.py
	python3 raw2vcd.py $< $@

clean:
	rm -rf $(TOP)_obj_dir $(TOP).so lib.spice sim_params.spice build.cfg snn_ms_tb.spice \
	       snn_ms_tb.raw snn_ms_tb.vcd snn_ms_tb.log

FORCE:
