// FPGA-style weight deserializer: inverse of serializer_tdm -- accumulates
// an N-bit word from K parallel input pins over T = N/K cycles.
//
// Every T cycles, K independent shift registers each receive one new bit
// per cycle on in[k], shifting it in at the MSB side and pushing older
// bits toward the LSB, so that after T cycles shift register k holds the
// bit received at cycle 0 in its LSB (bit 0) and the bit received at
// cycle T-1 in its MSB (bit T-1) of that lane's T-bit slice. This is the
// exact inverse of serializer_tdm's shift-out order: feeding
// serializer_tdm's out stream (same N, K) into this module's in
// reconstructs the original N-bit word in out[N-1:0].
//
// out continuously reflects the live shift-register contents, so it is
// only guaranteed fully valid once a frame completes. frame_done is high
// during the cycle a frame completes (counter wraps), signalling out
// holds a freshly-assembled word for the remainder of that cycle.

module deserializer_tdm #(
    parameter N = 8,
    parameter K = 2   // must divide N
) (
    input  wire         clk,
    input  wire         rst,         // synchronous, active high
    input  wire [K-1:0] in,
    output wire [N-1:0] out,
    output wire         frame_done   // high during the cycle `out` completes a word
);
  localparam T = N / K;
  localparam CW = (T > 1) ? $clog2(T) : 1;
  localparam [CW-1:0] CNT_LAST = T[CW-1:0] - 1'b1;

  initial begin
    if (K < 1 || N % K != 0) begin
      $error("deserializer_tdm: K (%0d) must divide N (%0d)", K, N);
      $finish;
    end
  end

  reg [CW-1:0] cnt;
  reg [N-1:0] sr;  // K shift registers of T bits, packed
  wire last = (cnt == CNT_LAST);

  assign frame_done = last;

  always @(posedge clk) cnt <= rst || last ? 0 : cnt + 1'b1;

  genvar k;
  generate
    for (k = 0; k < K; k = k + 1) begin : g_sr
      always @(posedge clk) begin
        if (rst) sr[k*T+:T] <= 0;
        else sr[k*T+:T] <= (sr[k*T+:T] >> 1) | (in[k] << (T - 1));
      end
      assign out[k*T+:T] = sr[k*T+:T];
    end
  endgenerate

endmodule
