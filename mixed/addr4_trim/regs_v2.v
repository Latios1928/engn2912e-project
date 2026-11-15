`timescale 1ns / 1ns

// Register map of the 4-bit-address interface (no wren pin), for the
// addr4_trim experiment. Replaces digital/rf.v here only; rf.v is unchanged.
//
// One write per clock: on every rising clk edge, data is stored in the
// register selected by addr, unless addr is IDLE (4'hF), which writes nothing.
// So the address doubles as the write strobe. Protocol for the driver:
//   1. rest at addr = 4'hF (enable the pad pull-ups so an undriven bus is idle)
//   2. put the value on data
//   3. set addr to the target for at least one clk cycle
//   4. return addr to 4'hF before changing data or going to another register
// Holding an address for several cycles just rewrites the same value.
//
//   addr     register                          reset value
//   0 - 7    weight word 0 - 7 (as rf.v)       none (write before use, like rf.v)
//   8        pulse PERIOD [3:0]                200 = 8'hC8 -> 4'h8
//   9        pulse PERIOD [7:4]                            -> 4'hC
//   10       pulse WIDTH  [3:0]                10  = 8'h0A -> 4'hA
//   11       pulse WIDTH  [7:4]                            -> 4'h0
//   12       trim code                         9 (Luz's bias_gen, nominal code)
//   13       debug register 0                  0
//   14       debug register 1                  0
//   15       IDLE: no write
//
// Weight word w is at weights[4w+3:4w], as in rf.v, so snn_analog sees the
// same w bus. rst (synchronous, active high) resets only the non-weight
// registers, so the chip runs with the default pulse timing and trim before
// anything is written.
module regs_v2 (
    input  wire        clk,
    input  wire        rst,
    input  wire [ 3:0] addr,
    input  wire [ 3:0] data,
    output reg  [31:0] weights,
    output wire [ 7:0] period,
    output wire [ 7:0] width,
    output reg  [ 3:0] trim,
    output reg  [ 3:0] dbg0,
    output reg  [ 3:0] dbg1
);
  localparam [3:0] IDLE = 4'hF;
  localparam [7:0] PERIOD_RST = 8'd200;
  localparam [7:0] WIDTH_RST = 8'd10;
  localparam [3:0] TRIM_RST = 4'd9;

  reg [3:0] period_lo, period_hi, width_lo, width_hi;
  assign period = {period_hi, period_lo};
  assign width  = {width_hi, width_lo};

  // Weights: no reset, like rf.v
  genvar w;
  generate
    for (w = 0; w < 8; w = w + 1) begin : g_word
      localparam [3:0] ADDR = w;
      always @(posedge clk) begin
        if (addr == ADDR) weights[w*4+:4] <= data;
      end
    end
  endgenerate

  // Control registers: reset to working defaults
  always @(posedge clk) begin
    if (rst) begin
      period_lo <= PERIOD_RST[3:0];
      period_hi <= PERIOD_RST[7:4];
      width_lo  <= WIDTH_RST[3:0];
      width_hi  <= WIDTH_RST[7:4];
      trim      <= TRIM_RST;
      dbg0      <= 4'd0;
      dbg1      <= 4'd0;
    end else begin
      case (addr)
        4'd8:    period_lo <= data;
        4'd9:    period_hi <= data;
        4'd10:   width_lo <= data;
        4'd11:   width_hi <= data;
        4'd12:   trim <= data;
        4'd13:   dbg0 <= data;
        4'd14:   dbg1 <= data;
        IDLE:    ;  // no write
        default: ;  // 0-7: weights (written above)
      endcase
    end
  end

endmodule
