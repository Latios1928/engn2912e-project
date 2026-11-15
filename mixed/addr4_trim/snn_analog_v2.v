`timescale 1ns / 1ns

// Verilog view of the analog block for the addr4_trim experiment: an empty
// black box, as analog/snn/snn_analog.v (unchanged), plus the trim[3:0] input.
//
// In this folder's mixed-signal run, SpiceBind connects this instance's ports
// to the SPICE netlist: the 2-2-1 network (analog/snn/snn_analog.sch), its
// bias cell (analog/neuron/bias_cell.sch), and a behavioral reference current
// set by trim (a mock of Luz's trimmed bias generator, analog/bias/bias_gen.sch,
// which has no layout yet). Biases and supplies are not Verilog signals.
// The ports are deliberately not used or driven in Verilog.
/* verilator lint_off UNUSEDSIGNAL */
/* verilator lint_off UNDRIVEN */
(* blackbox *)
module snn_analog_v2 (
    input  wire [31:0] w,
    input  wire [ 1:0] pulse,
    input  wire [ 3:0] trim,
    output wire [ 4:0] spike
);
endmodule
/* verilator lint_on UNDRIVEN */
/* verilator lint_on UNUSEDSIGNAL */
