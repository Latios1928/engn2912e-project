# Timing constraints for snn_top (PNR_SDC_FILE and SIGNOFF_SDC_FILE in config.json).
#
# Based on LibreLane's generic base.sdc, with one difference: the analog pins
# Iref (100 nA bias reference current) and VT (1.66 V neuron threshold) are DC
# inputs to the analog macro, not digital signals. base.sdc puts a driving cell,
# an input delay, an output delay and a pad load on every port, these included
# (inout ports count as inputs and as outputs). With a minimum-size inverter
# modelled as driving the long route to the macro, STA reported max-slew
# violations on Iref and VT that do not exist. Here they get no timing
# constraints and an ideal (zero) input transition. RSZ_DONT_TOUCH_RX in
# config.json also keeps the resizer from buffering them.
#
# Clock: 1 MHz (CLOCK_PERIOD 1000 ns). The default pulse timing (period 200,
# width 10 clk) makes the 10 us input spikes every 200 us, the 5 kHz rate the
# network is designed for.

set clock_port [lindex $::env(CLOCK_PORT) 0]
create_clock [get_ports $clock_port] -name $clock_port -period $::env(CLOCK_PERIOD)
set clocks [get_clocks $clock_port]

# Digital ports only. The analog pins are left out on purpose.
set dig_inputs  [get_ports {rst data[*] addr[*] in[*]}]
set dig_outputs [get_ports {out[*]}]
set analog_pins [get_ports {Iref VT}]

set io_delay [expr $::env(CLOCK_PERIOD) * $::env(IO_DELAY_CONSTRAINT) / 100]
puts "\[INFO] Setting input and output delay to: $io_delay"
set_input_delay  $io_delay -clock $clocks $dig_inputs
set_output_delay $io_delay -clock $clocks $dig_outputs

set_max_fanout $::env(MAX_FANOUT_CONSTRAINT) [current_design]
set_max_transition $::env(MAX_TRANSITION_CONSTRAINT) [current_design]
set_max_capacitance $::env(MAX_CAPACITANCE_CONSTRAINT) [current_design]

set_driving_cell \
    -lib_cell [lindex [split $::env(SYNTH_DRIVING_CELL) "/"] 0] \
    -pin [lindex [split $::env(SYNTH_DRIVING_CELL) "/"] 1] \
    $dig_inputs
set_driving_cell \
    -lib_cell [lindex [split $::env(SYNTH_CLK_DRIVING_CELL) "/"] 0] \
    -pin [lindex [split $::env(SYNTH_CLK_DRIVING_CELL) "/"] 1] \
    [get_ports $clock_port]

# Analog pins: ideal source, no load, not timed.
set_input_transition 0 $analog_pins

set cap_load [expr $::env(OUTPUT_CAP_LOAD) / 1000.0]
puts "\[INFO] Setting load to: $cap_load"
set_load $cap_load $dig_outputs

set_clock_uncertainty $::env(CLOCK_UNCERTAINTY_CONSTRAINT) $clocks
set_clock_transition $::env(CLOCK_TRANSITION_CONSTRAINT) $clocks
set_timing_derate -early [expr 1 - $::env(TIME_DERATING_CONSTRAINT) / 100.0]
set_timing_derate -late  [expr 1 + $::env(TIME_DERATING_CONSTRAINT) / 100.0]

if { [info exists ::env(OPENLANE_SDC_IDEAL_CLOCKS)] && $::env(OPENLANE_SDC_IDEAL_CLOCKS) } {
    unset_propagated_clock [all_clocks]
} else {
    set_propagated_clock [all_clocks]
}
