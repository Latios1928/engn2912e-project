`timescale 1ns / 1ns

// Verilog view of the analog macro SNN_signed
// (analog/layout_tools/top/SNN_signed): an empty black box with its digital
// ports. Synapse k has magnitude w[4k+3:4k] (0-15) and sign s[k]
// (1 = inhibitory). Iref, VT and the supplies are not Verilog signals.
//
// - mixed/ compiles it, and SpiceBind connects this instance's ports to the
//   macro's SPICE netlist.
// - LibreLane will use it as the macro's black-box header, so Yosys does not
//   synthesize it.
// - mock/ compiles a behavioral module of the same name instead.
/* verilator lint_off UNUSEDSIGNAL */
/* verilator lint_off UNDRIVEN */
(* blackbox *)
module snn_analog (
    input  wire [31:0] w,
    input  wire [ 7:0] s,
    input  wire [ 1:0] pulse,
    output wire [ 4:0] spike
);
endmodule
/* verilator lint_on UNDRIVEN */
/* verilator lint_on UNUSEDSIGNAL */
