`timescale 1ns / 1ns

// Chip top level: wires the digital part (digital/snn_digital.v) to the analog
// 2-2-1 network snn_analog. Wiring only.
//
// Pins: clk, rst, data[3:0], addr[3:0] (addr = 4'hF is idle), in[1:0], and
// out[4:0] = spikes of all 5 neurons {output, hidden[1:0], input[1:0]}.
//
// Analog pins Iref (bias reference current, 100 nA into the pin) and VT
// (neuron threshold, 1.66 V) go straight to the analog macro. They exist only
// when ANALOG_PINS is defined: the layout build (LibreLane) defines it, so the
// chip top has them as ports and the router connects them to the macro. The
// simulations do not: mock/ has no analog pins, and in mixed/ the SPICE side
// sources Iref and VT itself. Supplies are not Verilog signals.
//
// snn_analog is not defined here: the build supplies it, either the
// behavioral model in mock/ or, in mixed/, the empty black box
// analog/snn/snn_analog.v that SpiceBind connects to the transistor-level
// network. On the chip it is the analog macro: librelane/macros/snn_analog
// (SNN_signed with power rings), same black box.
module snn_top (
`ifdef ANALOG_PINS
    inout  wire       Iref,  // analog: bias reference current
    inout  wire       VT,    // analog: neuron threshold voltage
`endif
    input  wire       clk,
    input  wire       rst,   // synchronous, active high
    input  wire [3:0] data,
    input  wire [3:0] addr,  // 4'hF = idle (no write)
    input  wire [1:0] in,
    output wire [4:0] out
);
  wire [31:0] w;
  wire [ 7:0] s;
  wire [ 1:0] pulse;

  snn_digital u_digital (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .in(in),
      .w(w),
      .s(s),
      .pulse(pulse)
  );

  snn_analog u_snn_analog (
`ifdef ANALOG_PINS
      .Iref(Iref),
      .VT(VT),
`endif
      .w(w),
      .s(s),
      .pulse(pulse),
      .spike(out)
  );

endmodule
