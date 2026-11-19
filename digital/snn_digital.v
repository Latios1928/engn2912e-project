`timescale 1ns / 1ns

// The digital part of the chip: register map (regs) and programmable input
// pulse generator (pulse_gen). Takes the chip's digital pins and produces what
// the analog macro needs (w, s, pulse); it does not depend on the analog side,
// so it can be implemented (LibreLane) on its own.
//
// data[3:0], addr[3:0]; no wren. addr = 4'hF is idle; any other address writes
// data on every rising clk edge (see regs.v for the map and the write
// protocol). in[i] enables input pulse channel i.
//
// rst resets the pulse generator and the pulse timing (period 200, width 10);
// weights and signs have no reset.
module snn_digital (
    input  wire        clk,
    input  wire        rst,    // synchronous, active high
    input  wire [ 3:0] data,
    input  wire [ 3:0] addr,
    input  wire [ 1:0] in,
    output wire [31:0] w,
    output wire [ 7:0] s,
    output wire [ 1:0] pulse
);
  wire [7:0] period, width;

  regs u_regs (
      .clk(clk),
      .rst(rst),
      .addr(addr),
      .data(data),
      .weights(w),
      .signs(s),
      .period(period),
      .width(width)
  );

  pulse_gen u_pulse (
      .clk(clk),
      .rst(rst),
      .period(period),
      .width(width),
      .en(in),
      .pulse(pulse)
  );

endmodule
