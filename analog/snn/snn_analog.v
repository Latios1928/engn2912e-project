`timescale 1ns / 1ns

// Verilog view of analog/snn/snn_analog.sch: an empty black box with the digital
// ports of the analog network. Biases and supplies are not Verilog signals.
//
// - mixed/ compiles it, and SpiceBind connects this instance's ports to the
//   SPICE netlist of the transistor-level network.
// - LibreLane will use it as the macro's black-box header, so Yosys does not
//   synthesize it.
// - mock/ compiles a behavioral module of the same name instead.
(* blackbox *)
module snn_analog (
    input  wire [31:0] w,
    input  wire [ 1:0] pulse,
    output wire [ 4:0] spike
);
endmodule
