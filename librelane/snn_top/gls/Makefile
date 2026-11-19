# Gate-level simulation (GLS) of snn_top: the LibreLane netlist instead of the RTL, with
# the GF180 standard-cell models, the behavioral analog model (mock/snn_analog.v) in place
# of the analog macro, and the RTL testbench mock/tb_snn_top.v unchanged (self-checking).
#
#   make                         functional GLS (cells without delays)
#   make NETLIST=path/to/x.nl.v  another netlist (default: the latest full run)
#   make clean
#
# Run in the container, from this folder.

ROOT    := $(abspath ../../..)
NETLIST ?= $(ROOT)/librelane/snn_top/runs/full_1/final/nl/snn_top.nl.v
CELLS   := /foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog
MOCK    := $(ROOT)/mock

SRC := $(CELLS)/primitives.v $(CELLS)/gf180mcu_fd_sc_mcu7t5v0.v $(NETLIST) \
       $(MOCK)/snn_analog.v $(MOCK)/neuron.v $(MOCK)/comparator.v $(MOCK)/dac.v \
       $(MOCK)/tb_snn_top.v

.PHONY: run clean
run: gls.vvp
	vvp -n gls.vvp | tee gls.log | grep -E "PASS|FAIL|ERROR|error"
	@grep -q "PASS: snn_top" gls.log

# FUNCTIONAL: cell models without specify blocks (zero-delay); ANALOG_PINS: the netlist
# connects Iref / VT on the analog instance
gls.vvp: $(SRC)
	iverilog -g2012 -DFUNCTIONAL -DANALOG_PINS -s tb_snn_top -o $@ $(SRC)

clean:
	rm -f gls.vvp gls.log *.vcd
