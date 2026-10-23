// Behavioral mock of the input pulse generator (will become analog).
//
// While en is high, pulse is high for the first WIDTH cycles of every PERIOD
// clk_analog cycles. The phase counter is held at 0 while en is low, so a
// pulse starts in the same cycle en rises.
module pulse_gen #(
    parameter PERIOD = 16,
    parameter WIDTH  = 2    // 1 <= WIDTH <= PERIOD
) (
    input  wire clk_analog,
    input  wire rst,         // synchronous, active high
    input  wire en,
    output wire pulse
);
  localparam CW = (PERIOD > 1) ? $clog2(PERIOD) : 1;
  localparam [CW-1:0] PHASE_LAST = PERIOD[CW-1:0] - 1'b1;
  localparam [CW:0] W = WIDTH[CW:0];  // one extra bit: WIDTH may equal PERIOD

  initial begin
    if (WIDTH < 1 || WIDTH > PERIOD) begin
      $error("pulse_gen: need 1 <= WIDTH (%0d) <= PERIOD (%0d)", WIDTH, PERIOD);
      $finish;
    end
  end

  reg [CW-1:0] phase;

  assign pulse = en && ({1'b0, phase} < W);

  always @(posedge clk_analog) begin
    if (rst || !en || phase == PHASE_LAST) phase <= 0;
    else phase <= phase + 1'b1;
  end

endmodule
