`timescale 1ns / 1ns

// Empty stand-in for analog/snn/snn_analog.sch. This build compiles it instead
// of mock/snn_analog.v; SpiceBind connects the ports of this instance to the
// SPICE netlist (HDL_INSTANCE in the Makefile).
module snn_analog (
    input  wire [91:0] w,
    input  wire [ 2:0] pulse,
    output wire [ 8:0] spike
);
endmodule
