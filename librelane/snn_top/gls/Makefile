# Gate-level simulation (GLS) of snn_top: the LibreLane netlist instead of the RTL, with the
# GF180 standard-cell models. Run in the container, from this folder.
#
#   make                         tb_gls_timing.v at the chip's 1 MHz clock: zero-delay, then
#                                with the SDF of each corner in $(CORNERS) (pulse timing,
#                                weights / signs into the macro)
#   make NETLIST=path/to/x.nl.v  another netlist (default: results/, the published run)
#   make clean
#
# The default netlist and SDFs are the ones librelane/snn_top/run.sh publishes to results/,
# so they always come from the same run.

ROOT    := $(abspath ../../..)
RESULTS := $(ROOT)/librelane/snn_top/results
NETLIST ?= $(RESULTS)/snn_top.nl.v
SDF_DIR ?= $(RESULTS)/sdf
CORNERS ?= nom_ss_125C_3v00 nom_tt_025C_3v30 nom_ff_n40C_3v60
CELLS   := /foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog
export PATH := /foss/tools/bin:$(PATH)

# timescale.v first: the cell library and the netlist have no `timescale of their own, and
# without one Icarus reads the SDF delays in the wrong unit
TSRC := timescale.v $(CELLS)/primitives.v $(CELLS)/gf180mcu_fd_sc_mcu7t5v0.v $(NETLIST) \
        $(ROOT)/analog/snn/snn_analog.v tb_gls_timing.v

.PHONY: timing clean
.DEFAULT_GOAL := timing
# Icarus applies the SDF path and interconnect delays, but not the cells' setup / hold
# checks (OpenSTA signs those off). It cannot match a few conditional IOPATHs of some
# AOI / OAI / mux cells ("SDF ERROR: Unable to match ModPath"); those arcs keep the models'
# default delays. The logs keep the messages; only the testbench's PASS / FAIL is checked.
# FUNCTIONAL: cell models without specify blocks (zero-delay); ANALOG_PINS: the netlist
# connects Iref / VT on the analog instance
timing: $(TSRC)
	iverilog -g2012 -DFUNCTIONAL -DANALOG_PINS -s tb_gls_timing -o timing_zero.vvp $(TSRC)
	vvp -n timing_zero.vvp > timing_zero.log 2>&1
	@grep '^tb_gls_timing: \(PASS\|FAIL\)' timing_zero.log | sed 's/^/zero-delay: /'
	@for c in $(CORNERS); do \
	  sdf=$(SDF_DIR)/snn_top__$$c.sdf; \
	  iverilog -g2012 -gspecify -DANALOG_PINS "-DSDF_FILE=\"$$sdf\"" -s tb_gls_timing \
	    -o timing_$$c.vvp $(TSRC) 2> timing_$$c.compile.log || exit 1; \
	  vvp -n timing_$$c.vvp > timing_$$c.log 2>&1; \
	  grep '^tb_gls_timing: \(PASS\|FAIL\)' timing_$$c.log | sed "s/^/$$c: /"; \
	done
	@! grep -l '^tb_gls_timing: FAIL' timing_*.log
	@test $$(grep -l '^tb_gls_timing: PASS' timing_*.log | wc -l) -eq $$(( $(words $(CORNERS)) + 1 ))

timescale.v:
	echo '`timescale 1ns / 1ps' > $@

clean:
	rm -f *.vcd timing_*.vvp timing_*.log timescale.v
