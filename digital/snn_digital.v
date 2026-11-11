`timescale 1ns / 1ns

// The digital part of the chip: weight register file and input pulse
// generator. Takes the chip's digital pins and produces what the analog
// network needs (w, pulse); it does not depend on the analog side at all, so
// it can be implemented (LibreLane) on its own.
//
// Weights are written one 4-bit word at a time through data/addr/wren; see
// mock/snn_analog.v for the address of each synapse and the layout of w
// (23 words of 4 bits, word k at w[4k+3:4k]). in[i] enables input pulse
// channel i. rst resets the pulse generator only.
module snn_digital #(
    parameter PULSE_PERIOD = 200,  // clk cycles
    parameter PULSE_WIDTH  = 10    // clk cycles
) (
    input  wire        clk,
    input  wire        rst,   // synchronous, active high
    input  wire [ 3:0] data,
    input  wire [ 4:0] addr,
    input  wire        wren,
    input  wire [ 2:0] in,
    output wire [91:0] w,
    output wire [ 2:0] pulse
);

  rf #(
      .NUM_WORDS(23),
      .WIDTH(4),
      .AW(5)
  ) u_rf (
      .clk(clk),
      .wren(wren),
      .addr(addr),
      .data(data),
      .weights(w)
  );

  pulse_gen #(
      .PERIOD(PULSE_PERIOD),
      .WIDTH (PULSE_WIDTH)
  ) u_pulse (
      .clk(clk),
      .rst(rst),
      .en(in),
      .pulse(pulse)
  );

endmodule
