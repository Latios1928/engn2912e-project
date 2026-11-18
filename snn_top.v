`timescale 1ns / 1ns

// Chip top level: wires the digital part (digital/snn_digital.v) to the analog
// 2-2-1 network snn_analog. Wiring only.
//
// Pins: clk, rst, data[3:0], addr[3:0] (addr = 4'hF is idle), in[1:0], and
// out[4:0] = spikes of all 5 neurons {output, hidden[1:0], input[1:0]}.
// The analog macro also has Iref, VT and supplies (not Verilog signals).
//
// snn_analog is not defined here: the build supplies it, either the
// behavioral model in mock/ or, in mixed/, the empty black box
// analog/snn/snn_analog.v that SpiceBind connects to the transistor-level
// network. On the chip it is the analog macro SNN_signed (same black box).
module snn_top (
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
      .w(w),
      .s(s),
      .pulse(pulse),
      .spike(out)
  );

endmodule
