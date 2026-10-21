// Time-division serializer: reads N parallel inputs through K output pins.
//
// Every T = N/K cycles the N inputs are captured into K shift registers of
// T bits each. Shift register k holds in[k*T +: T] and shifts out LSB first,
// so over one frame out[k] carries in[k*T], in[k*T+1], ..., in[k*T+T-1].
//
// Timing: the capture happens on the clock edge that wraps the counter to 0,
// so out is valid for T consecutive cycles (counter = 0..T-1) with no dead
// cycle between frames. frame_start is high during the first cycle of each
// frame (counter = 0), aligned with out. out[k] at counter value j is
// in[k*T + j] as sampled on the capture edge that started this frame.

module serializer_tdm #(
    parameter N = 8,
    parameter K = 2   // must divide N
) (
    input  wire         clk,
    input  wire         rst,         // synchronous, active high
    input  wire [N-1:0] in,
    output wire [K-1:0] out,
    output wire         frame_start  // high while out carries bit 0 of each group
);
  localparam T = N / K;
  localparam CW = (T > 1) ? $clog2(T) : 1;
  localparam [CW-1:0] CNT_LAST = T[CW-1:0] - 1'b1;

  initial begin
    if (K < 1 || N % K != 0) begin
      $error("serializer_tdm: K (%0d) must divide N (%0d)", K, N);
      $finish;
    end
  end

  reg [CW-1:0] cnt;
  reg [N-1:0] sr;  // K shift registers of T bits, packed
  wire last = (cnt == CNT_LAST);

  assign frame_start = !cnt;

  always @(posedge clk) cnt <= rst || last ? 0 : cnt + 1'b1;

  genvar k;
  generate
    for (k = 0; k < K; k = k + 1) begin : g_sr
      always @(posedge clk) begin
        if (rst || last) sr[k*T+:T] <= in[k*T+:T];
        else sr[k*T+:T] <= sr[k*T+:T] >> 1;
      end
      assign out[k] = sr[k*T];
    end
  endgenerate

endmodule
