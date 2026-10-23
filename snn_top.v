// Top level: weight register file (digital, clk) driving the 3-5-1 SNN
// (analog mock, clk_analog).
//
// Weights are written one 3-bit word at a time through data/addr/wren; see
// analog/mock/snn.v for the address of each synapse. in[i] enables input
// pulse generator i, and out is the active signal of all 9 neurons:
// {output, hidden[4:0], input[2:0]}.
module snn_top #(
    parameter DURATION     = 4,
    parameter THRESHOLD    = 1000,
    parameter GAIN         = 16,
    parameter PULSE_PERIOD = 16,
    parameter PULSE_WIDTH  = 2
) (
    input  wire       clk,
    input  wire       clk_analog,
    input  wire       rst,         // synchronous to clk_analog, active high; clears the network state
    input  wire [2:0] data,
    input  wire [4:0] addr,
    input  wire       wren,
    input  wire [2:0] in,
    output wire [8:0] out
);
  wire [23*3-1:0] weights;

  rf #(
      .NUM_WORDS(23),
      .WIDTH(3),
      .AW(5)
  ) u_rf (
      .clk(clk),
      .wren(wren),
      .addr(addr),
      .data(data),
      .weights(weights)
  );

  snn #(
      .DURATION(DURATION),
      .THRESHOLD(THRESHOLD),
      .GAIN(GAIN),
      .PULSE_PERIOD(PULSE_PERIOD),
      .PULSE_WIDTH(PULSE_WIDTH)
  ) u_snn (
      .clk_analog(clk_analog),
      .rst(rst),
      .weights(weights),
      .in(in),
      .out(out)
  );

endmodule
