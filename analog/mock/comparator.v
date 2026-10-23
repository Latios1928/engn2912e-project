// Behavioral mock of the neuron's threshold comparator (will become analog).
//
// While voltage > THRESHOLD, countdown is reloaded with DURATION; otherwise
// it counts down to 0. active = (countdown != 0), so active rises on the
// clk_analog edge after voltage first exceeds THRESHOLD and stays high until
// DURATION edges after voltage last exceeded it.
module comparator #(
    parameter DURATION  = 4,
    parameter THRESHOLD = 1000
) (
    input  wire        clk_analog,
    input  wire        rst,         // synchronous, active high
    input  wire [15:0] voltage,
    output wire        active
);
  localparam CW = $clog2(DURATION + 1);
  localparam [CW-1:0] DUR = DURATION[CW-1:0];
  localparam [15:0] THR = THRESHOLD[15:0];

  initial begin
    if (DURATION < 1 || THRESHOLD < 0 || THRESHOLD > 65534) begin
      $error("comparator: need DURATION >= 1 (%0d) and 0 <= THRESHOLD <= 65534 (%0d)", DURATION,
             THRESHOLD);
      $finish;
    end
  end

  reg [CW-1:0] countdown;

  assign active = |countdown;

  always @(posedge clk_analog) begin
    if (rst) countdown <= 0;
    else if (voltage > THR) countdown <= DUR;
    else if (active) countdown <= countdown - 1'b1;
  end

endmodule
