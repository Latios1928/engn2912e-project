`timescale 1ns / 1ns

// The digital part of the chip for the addr4_trim experiment: register map
// (regs_v2) and programmable input pulse generator (pulse_gen_v2). Same role
// as digital/snn_digital.v (unchanged), with the 4-bit-address interface:
//
//   - data[3:0], addr[3:0]; no wren. addr = 4'hF is idle; any other address
//     writes data on every rising clk edge (see regs_v2.v for the map and the
//     write protocol).
//   - The pulse timing (period, width) comes from registers 8-11 instead of
//     parameters.
//   - trim[3:0] (register 12) goes to the analog side: Luz's bias generator
//     (analog/bias/bias_gen.sch), mocked in this experiment.
//   - dbg0/dbg1 (registers 13-14) are reserved for a debug mode; nothing uses
//     them yet.
//
// rst resets the pulse generator and the control registers (period 200,
// width 10, trim 9, debug 0); weights have no reset.
module snn_digital_v2 (
    input  wire        clk,
    input  wire        rst,    // synchronous, active high
    input  wire [ 3:0] data,
    input  wire [ 3:0] addr,
    input  wire [ 1:0] in,
    output wire [31:0] w,
    output wire [ 1:0] pulse,
    output wire [ 3:0] trim,
    output wire [ 3:0] dbg0,
    output wire [ 3:0] dbg1
);
  wire [7:0] period, width;

  regs_v2 u_regs (
      .clk(clk),
      .rst(rst),
      .addr(addr),
      .data(data),
      .weights(w),
      .period(period),
      .width(width),
      .trim(trim),
      .dbg0(dbg0),
      .dbg1(dbg1)
  );

  pulse_gen_v2 u_pulse (
      .clk(clk),
      .rst(rst),
      .period(period),
      .width(width),
      .en(in),
      .pulse(pulse)
  );

endmodule
