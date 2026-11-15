`timescale 1ns / 1ns

// Input pulse generator with programmable timing, for the addr4_trim
// experiment. Same behaviour as digital/pulse_gen.v (which is unchanged), but
// PERIOD and WIDTH are 8-bit inputs (from regs_v2) instead of parameters.
//
// Two channels share one counter. Every period, each channel whose en bit was
// high at the end of the previous period outputs a pulse of width clk cycles;
// the others stay low. en, period and width are all sampled only at period
// boundaries, so a pulse is never cut short or stretched when en or a register
// changes mid-period: a new period/width takes effect from the next period.
// Outputs come straight from flip-flops (they drive the analog DAC enables).
//
// period: clk cycles per period, 1-255; 0 means 256.
// width:  clk cycles per pulse. 0 = no pulses; width >= period = en held high
//         for the whole period.
// With clk = 1 MHz, period = 200 and width = 10 (the reset values in regs_v2)
// give the 10 us pulses every 200 us of digital/pulse_gen.v's defaults.
module pulse_gen_v2 (
    input  wire       clk,
    input  wire       rst,     // synchronous, active high
    input  wire [7:0] period,
    input  wire [7:0] width,
    input  wire [1:0] en,
    output reg  [1:0] pulse
);
  reg  [7:0] cnt;  // position in the period
  reg  [1:0] en_q;  // en as sampled at the start of this period
  reg  [7:0] period_q;  // timing of this period
  reg  [7:0] width_q;

  // Last count of this period; with 8-bit wraparound, period_q = 0 gives 255
  // (a 256-cycle period).
  wire [7:0] last = period_q - 8'd1;
  wire       wrap = (cnt == last);

  wire [7:0] cnt_n = wrap ? 8'd0 : cnt + 8'd1;
  wire [1:0] en_n = wrap ? en : en_q;
  wire [7:0] width_n = wrap ? width : width_q;

  always @(posedge clk) begin
    if (rst) begin
      cnt      <= 8'd0;
      en_q     <= 2'b00;
      period_q <= period;
      width_q  <= width;
      pulse    <= 2'b00;
    end else begin
      cnt   <= cnt_n;
      en_q  <= en_n;
      pulse <= en_n & {2{cnt_n < width_n}};
      if (wrap) begin
        period_q <= period;
        width_q  <= width;
      end
    end
  end

endmodule
