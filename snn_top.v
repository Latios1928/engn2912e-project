`timescale 1ns / 1ns

// Chip top level: wires the digital part (digital/snn_digital.v) to the analog
// 3-5-1 network snn_analog. Wiring only.
//
// out is the spike (active) signal of all 9 neurons: {output, hidden[4:0],
// input[2:0]}. See digital/snn_digital.v for the other ports.
//
// snn_analog is not defined here: the build supplies it, either the
// behavioral model in mock/ or, in mixed/, an empty module that SpiceBind
// connects to the transistor-level network. On the chip it is the analog
// macro.
module snn_top #(
    parameter PULSE_PERIOD = 200,  // clk cycles
    parameter PULSE_WIDTH  = 10    // clk cycles
) (
    input  wire       clk,
    input  wire       rst,   // synchronous, active high
    input  wire [3:0] data,
    input  wire [4:0] addr,
    input  wire       wren,
    input  wire [2:0] in,
    output wire [8:0] out
);
  wire [91:0] w;
  wire [ 2:0] pulse;

  snn_digital #(
      .PULSE_PERIOD(PULSE_PERIOD),
      .PULSE_WIDTH (PULSE_WIDTH)
  ) u_digital (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .wren(wren),
      .in(in),
      .w(w),
      .pulse(pulse)
  );

  snn_analog u_snn_analog (
      .w(w),
      .pulse(pulse),
      .spike(out)
  );

endmodule
