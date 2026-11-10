# Mixed-signal simulation of the SNN: rf and pulse generators in Icarus Verilog,
# the analog 2-2-1 network (analog/snn/snn_analog.sch) in ngspice, coupled by
# SpiceBind. See README.md.
#
#   make run                             all scenarios (1-4, about 20 ms simulated)
#   make run SCEN_FIRST=3 SCEN_LAST=3    one scenario
#   make run SETTLE=500 RUN=1500         shorter windows (us)
#   make vcd                             snn_ms_tb.raw -> snn_ms_tb.vcd
#   make clean

MIXED := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
ROOT  := $(abspath $(MIXED)/..)
export PATH := /foss/tools/bin:$(PATH)

SCEN_FIRST ?= 1
SCEN_LAST  ?= 4
SETTLE     ?= 2000
RUN        ?= 3000

SPICEBIND := /foss/tools/spicebind
VSRC := sim.f snn_ms_tb.v $(ROOT)/analog/snn/snn_analog.v $(ROOT)/snn_top.v $(wildcard $(ROOT)/digital/*.v)
PFX  := -Psnn_ms_tb
SCHEMATICS := snn_ms_tb.sch $(ROOT)/analog/snn/snn_analog.sch $(ROOT)/analog/snn/snn_analog.sym \
              $(wildcard $(ROOT)/analog/neuron/DAC.s* $(ROOT)/analog/neuron/DPI.s* \
                         $(ROOT)/analog/neuron/neuron_sized.s* $(ROOT)/analog/neuron/spike_amplifier.s*)

.DEFAULT_GOAL := run
.PHONY: run vcd clean

# xschem resolves symbols from the current folder, so netlist from the project
# root with the project xschemrc. It exits with status 10 even after a good
# netlist, so check the file instead.
snn_ms_tb.spice: $(SCHEMATICS)
	rm -f $@
	cd $(ROOT) && xschem --rcfile xschemrc -n -q -x -o $(MIXED) -N $@ mixed/snn_ms_tb.sch || true
	@grep -q 'snn_analog$$' $@ || { echo "netlisting failed"; exit 1; }
	@! grep -n 'IS MISSING' $@ || { echo "netlist has missing symbols"; exit 1; }
	@d=$$(grep -i '^\.subckt' $@ | awk '{print tolower($$2)}' | sort | uniq -d); \
	  [ -z "$$d" ] || { echo "duplicate subckt names: $$d"; exit 1; }

no_passwd_shim.so: no_passwd_shim.c
	gcc -shared -fPIC -o $@ $<

run: snn_ms_tb.spice no_passwd_shim.so $(VSRC)
	iverilog -g2012 -Wall -s snn_ms_tb -o snn_ms_tb.vvp \
	  $(PFX).SCEN_FIRST=$(SCEN_FIRST) $(PFX).SCEN_LAST=$(SCEN_LAST) \
	  $(PFX).SETTLE=$(SETTLE) $(PFX).RUN=$(RUN) -f sim.f
	@rm -f dump.raw
	@start=$$(date +%s); \
	  SPICE_NETLIST=$(MIXED)/snn_ms_tb.spice HDL_INSTANCE=snn_ms_tb.dut.u_snn_analog VCC=3.3 \
	  LOGIC_THRESHOLD_LOW=1.64 LOGIC_THRESHOLD_HIGH=1.66 \
	  LD_PRELOAD=$(MIXED)/no_passwd_shim.so \
	  vvp -M $(SPICEBIND) -m spicebind_vpi snn_ms_tb.vvp > snn_ms_tb.log 2>&1; \
	  echo "simulation took $$(( $$(date +%s) - start )) s"
	@mv -f dump.raw snn_ms_tb.raw
	@# ngspice's progress output uses \r, so split on it to find the testbench lines.
	@tr '\r' '\n' < snn_ms_tb.log | grep -E 'snn_ms_tb: |\*\* Error|singular' | awk '!seen[$$0]++'
	@tr '\r' '\n' < snn_ms_tb.log | grep -q 'snn_ms_tb: PASS,'

vcd: snn_ms_tb.vcd
snn_ms_tb.vcd: snn_ms_tb.raw
	rawtovcd $< > $@

clean:
	rm -f no_passwd_shim.so snn_ms_tb.vvp snn_ms_tb.spice snn_ms_tb.raw snn_ms_tb.log \
	      snn_ms_tb.vcd snn_ms_tb_digital.vcd dump.raw
