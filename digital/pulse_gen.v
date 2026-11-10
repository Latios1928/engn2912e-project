`timescale 1ns / 1ns

// Input pulse generator: two channels sharing one counter.
//
// Every PERIOD clk cycles, each channel whose en bit was high at the end of
// the previous period outputs a pulse of exactly WIDTH cycles; the others stay
// low. en is sampled only at period boundaries, so a pulse is never cut short
// when en rises or falls mid-period; the cost is up to PERIOD cycles between
// en rising and the first pulse. Outputs come straight from flip-flops
// (they drive the analog DAC enables).
//
// With clk = 1 MHz, PERIOD = 200 and WIDTH = 10 give the 10 us pulses every
// 200 us (5 kHz) that analog/neuron/DACs-DPI-neuron.sch is tuned for.
module pulse_gen #(
    parameter PERIOD = 200,  // clk cycles per period
    parameter WIDTH  = 10    // clk cycles per pulse, 1 <= WIDTH <= PERIOD
) (
    input  wire       clk,
    input  wire       rst,    // synchronous, active high
    input  wire [1:0] en,
    output reg  [1:0] pulse
);
  localparam CW = (PERIOD > 1) ? $clog2(PERIOD) : 1;
  localparam [CW-1:0] LAST = PERIOD - 1;
  localparam [CW:0] W = WIDTH;  // one extra bit: WIDTH may equal PERIOD

  initial begin
    if (WIDTH < 1 || WIDTH > PERIOD) begin
      $error("pulse_gen: need 1 <= WIDTH (%0d) <= PERIOD (%0d)", WIDTH, PERIOD);
      $finish;
    end
  end

  reg  [CW-1:0] cnt;  // position in the period
  reg  [   1:0] en_q;  // en as sampled at the start of this period

  wire [CW-1:0] cnt_n = (cnt == LAST) ? {CW{1'b0}} : cnt + 1'b1;
  wire [   1:0] en_n = (cnt == LAST) ? en : en_q;

  always @(posedge clk) begin
    if (rst) begin
      cnt   <= {CW{1'b0}};
      en_q  <= 2'b00;
      pulse <= 2'b00;
    end else begin
      cnt   <= cnt_n;
      en_q  <= en_n;
      pulse <= en_n & {2{{1'b0, cnt_n} < W}};
    end
  end

endmodule
