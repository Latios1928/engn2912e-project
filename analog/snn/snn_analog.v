`timescale 1ns / 1ns

// Verilog view of the analog macro SNN_signed
// (analog/layout_tools/top/SNN_signed): an empty black box with its digital
// ports. Synapse k has magnitude w[4k+3:4k] (0-15) and sign s[k]
// (1 = inhibitory). Supplies are not Verilog signals.
//
// - mixed/ compiles it, and SpiceBind connects this instance's ports to the
//   macro's SPICE netlist (which sources Iref and VT itself).
// - LibreLane uses it as the macro's black-box header, so Yosys does not
//   synthesize it. Its layout is librelane/macros/snn_analog (SNN_signed with
//   power rings). LibreLane defines ANALOG_PINS, which adds the analog pins
//   Iref and VT (see snn_top.v).
/* verilator lint_off UNUSEDSIGNAL */
/* verilator lint_off UNDRIVEN */
(* blackbox *)
module snn_analog (
`ifdef USE_POWER_PINS
    inout  wire        VDD,  // LibreLane's powered netlist (LVS): analog supply
    inout  wire        VSS,
`endif
`ifdef ANALOG_PINS
    inout  wire        Iref,
    inout  wire        VT,
`endif
    input  wire [31:0] w,
    input  wire [ 7:0] s,
    input  wire [ 1:0] pulse,
    output wire [ 4:0] spike
);
endmodule
/* verilator lint_on UNDRIVEN */
/* verilator lint_on UNUSEDSIGNAL */
