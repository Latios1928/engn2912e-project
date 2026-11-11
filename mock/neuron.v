`timescale 1ns / 1ns

// Behavioral model of an integrate-and-fire neuron (analog/neuron/DPI.sch and
// neuron_sized.sch); part of the behavioral snn_analog (snn_analog.v).
//
// Every clk_analog cycle, voltage changes by the sum of the INDEGREE input
// currents (signed; negative ones are inhibitory), clamped to 0..16'hFFFF
// (the mock ground and supply rail), and then drops by LEAK (not below 0). While active, voltage is held at 0 instead.
//
// active comes from the internal comparator. Timing: if voltage exceeds
// THRESHOLD after edge e, active rises at e+1 and voltage is cleared at e+2
// (it still integrates at e+1), so the comparator reloads once more and
// active stays high for DURATION+1 cycles.
module neuron #(
    parameter INDEGREE  = 1,
    parameter LEAK      = 1,  // charge lost per clk_analog cycle
    parameter DURATION  = 4,
    parameter THRESHOLD = 1000
) (
    input  wire                   clk_analog,
    input  wire                   rst,         // synchronous, active high
    input  wire [INDEGREE*16-1:0] currents,    // INDEGREE signed 16-bit currents, packed
    output wire                   active
);
  // voltage (0..65535) plus INDEGREE signed 16-bit currents, as a signed sum
  localparam SW = 18 + $clog2(INDEGREE + 1);

  localparam [15:0] LEAK_V = LEAK[15:0];
  localparam signed [SW-1:0] LEAK_S = LEAK;
  localparam signed [SW-1:0] MAX_V = 65535;

  initial begin
    if (INDEGREE < 1 || LEAK < 0 || LEAK > 65535) begin
      $error("neuron: need INDEGREE >= 1 (%0d) and 0 <= LEAK <= 65535 (%0d)", INDEGREE, LEAK);
      $finish;
    end
  end

  reg     [  15:0] voltage;
  reg signed [SW-1:0] sum;
  integer          i;

  always @(*) begin
    sum = $signed({{(SW - 16) {1'b0}}, voltage});
    for (i = 0; i < INDEGREE; i = i + 1)
      sum = sum + $signed({{(SW - 16) {currents[i*16+15]}}, currents[i*16+:16]});
  end

  always @(posedge clk_analog) begin
    if (rst || active) voltage <= 16'd0;
    else if (sum > MAX_V) voltage <= 16'hFFFF;
    else if (sum > LEAK_S) voltage <= sum[15:0] - LEAK_V;
    else voltage <= 16'd0;
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
