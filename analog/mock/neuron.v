// Behavioral mock of an integrate-and-fire neuron (will become analog).
//
// Every clk_analog cycle, voltage increases by the sum of the INDEGREE input
// currents, saturating at 16'hFFFF (the mock supply rail). While active,
// voltage is held at 0 instead. There is no leak.
//
// active comes from the internal comparator. Timing: if voltage exceeds
// THRESHOLD after edge e, active rises at e+1 and voltage is cleared at e+2
// (it still integrates at e+1), so the comparator reloads once more and
// active stays high for DURATION+1 cycles.
module neuron #(
    parameter INDEGREE  = 1,
    parameter DURATION  = 4,
    parameter THRESHOLD = 1000
) (
    input  wire                   clk_analog,
    input  wire                   rst,         // synchronous, active high
    input  wire [INDEGREE*16-1:0] currents,    // INDEGREE 16-bit currents, packed
    output wire                   active
);
  // voltage plus INDEGREE currents: INDEGREE+1 16-bit terms
  localparam SW = 16 + $clog2(INDEGREE + 1);

  initial begin
    if (INDEGREE < 1) begin
      $error("neuron: INDEGREE (%0d) must be >= 1", INDEGREE);
      $finish;
    end
  end

  reg     [  15:0] voltage;
  reg     [SW-1:0] sum;
  integer          i;

  always @(*) begin
    sum = {{(SW - 16) {1'b0}}, voltage};
    for (i = 0; i < INDEGREE; i = i + 1) sum = sum + {{(SW - 16) {1'b0}}, currents[i*16+:16]};
  end

  always @(posedge clk_analog) begin
    if (rst || active) voltage <= 16'd0;
    else if (|sum[SW-1:16]) voltage <= 16'hFFFF;
    else voltage <= sum[15:0];
  end

  comparator #(
      .DURATION (DURATION),
      .THRESHOLD(THRESHOLD)
  ) u_cmp (
      .clk_analog(clk_analog),
      .rst(rst),
      .voltage(voltage),
      .active(active)
  );

endmodule
