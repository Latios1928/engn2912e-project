`timescale 1ns / 1ns

// Chip top level for the addr4_trim experiment: wires snn_digital_v2 to the
// analog block snn_analog_v2. Wiring only. Same role as snn_top.v (unchanged).
//
// Pins: clk, rst, data[3:0], addr[3:0] (no wren: addr = 4'hF is idle), in[1:0],
// out[4:0] = spikes of all 5 neurons {output, hidden[1:0], input[1:0]}.
//   snn_top.v:    clk rst data[3:0] addr[2:0] wren in[1:0] out[4:0] = 17 pins
//   snn_top_v2.v: clk rst data[3:0] addr[3:0]      in[1:0] out[4:0] = 17 pins
// The same pin count: wren became addr[3], and the address space grew from 8
// to 15 registers (+ idle).
//
// trim[3:0] runs inside the chip from the register to the analog block.
// The debug registers dbg0/dbg1 are not connected to anything yet.
module snn_top_v2 (
    input  wire       clk,
    input  wire       rst,   // synchronous, active high
    input  wire [3:0] data,
    input  wire [3:0] addr,  // 4'hF = idle (no write)
    input  wire [1:0] in,
    output wire [4:0] out
);
  wire [31:0] w;
  wire [ 1:0] pulse;
  wire [ 3:0] trim;
  /* verilator lint_off UNUSEDSIGNAL */
  wire [ 3:0] dbg0, dbg1;  // reserved for the debug mode
  /* verilator lint_on UNUSEDSIGNAL */

  snn_digital_v2 u_digital (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .in(in),
      .w(w),
      .pulse(pulse),
      .trim(trim),
      .dbg0(dbg0),
      .dbg1(dbg1)
  );

  snn_analog_v2 u_snn_analog (
      .w(w),
      .pulse(pulse),
      .trim(trim),
      .spike(out)
  );

endmodule
