`timescale 1ns / 1ns

// Register map. On every rising clk edge, data is written to the register at
// addr, unless addr is IDLE (4'hF). To write: rest at IDLE, set data, set addr
// for one cycle, return to IDLE. Change data only while idle.
//
//   addr     register             reset
//   0 - 7    weight word 0 - 7    none
//   8, 9     signs [3:0], [7:4]   none
//   10, 11   PERIOD [3:0], [7:4]  200
//   12, 13   WIDTH  [3:0], [7:4]  10
//   14       INPUT EN [1:0]       00   (data[3:2] ignored)
//   15       IDLE: no write
//
// Synapse k has magnitude weights[4k+3:4k] (0-15) and sign signs[k]
// (1 = inhibitory); see mock/snn_analog.v for the synapse of each k.
// INPUT EN bit i enables input pulse channel i (pulse_gen samples it at each
// period boundary).
// rst (synchronous, active high) resets the pulse timing and INPUT EN only, so
// after a reset no input pulses run and the timing is the default.
module regs (
    input  wire        clk,
    input  wire        rst,
    input  wire [ 3:0] addr,
    input  wire [ 3:0] data,
    output reg  [31:0] weights,
    output reg  [ 7:0] signs,
    output wire [ 7:0] period,
    output wire [ 7:0] width,
    output reg  [ 1:0] in_en
);
  localparam [7:0] PERIOD_RST = 8'd200;
  localparam [7:0] WIDTH_RST = 8'd10;

  reg [3:0] period_lo, period_hi, width_lo, width_hi;
  assign period = {period_hi, period_lo};
  assign width  = {width_hi, width_lo};

  // Weights and signs: no reset
  genvar w;
  generate
    for (w = 0; w < 8; w = w + 1) begin : g_word
      localparam [3:0] ADDR = w;
      always @(posedge clk) begin
        if (addr == ADDR) weights[w*4+:4] <= data;
      end
    end
  endgenerate

  always @(posedge clk) begin
    if (addr == 4'd8) signs[3:0] <= data;
    if (addr == 4'd9) signs[7:4] <= data;
  end

  // Pulse timing and input enables: reset to working defaults (inputs off)
  always @(posedge clk) begin
    if (rst) begin
      period_lo <= PERIOD_RST[3:0];
      period_hi <= PERIOD_RST[7:4];
      width_lo  <= WIDTH_RST[3:0];
      width_hi  <= WIDTH_RST[7:4];
      in_en     <= 2'b00;
    end else begin
      case (addr)
        4'd10:   period_lo <= data;
        4'd11:   period_hi <= data;
        4'd12:   width_lo <= data;
        4'd13:   width_hi <= data;
        4'd14:   in_en <= data[1:0];
        default: ;  // weights, signs, IDLE
      endcase
    end
  end

endmodule
