// Self-checking testbench for serializer_tdm.
//
// in is randomized every cycle (including mid-frame) so the check also
// verifies that out only reflects the value captured on the frame's capture
// edge. A reference model tracks the frame phase j and the captured snapshot;
// out[k] must equal snapshot[k*T + j] and frame_start must equal (j == 0).
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp serializer_tdm.v tb_serializer_tdm.v && vvp sim.vvp
//   iverilog -g2012 -Ptb_serializer_tdm.N=12 -Ptb_serializer_tdm.K=4 ...   (other sizes)

module tb_serializer_tdm #(
    parameter N = 8,
    parameter K = 2,
    parameter NCYCLES = 200
);
  localparam T = N / K;

  reg          clk = 1'b0;
  reg          rst = 1'b1;
  reg  [N-1:0] in = 0;
  wire [K-1:0] out;
  wire         frame_start;

  serializer_tdm #(
      .N(N),
      .K(K)
  ) dut (
      .clk(clk),
      .rst(rst),
      .in(in),
      .out(out),
      .frame_start(frame_start)
  );

  always #5 clk = ~clk;

  // Reference model, updated on the same edge as the DUT.
  reg     [N-1:0] snapshot;
  integer         j;
  integer         errors = 0;
  integer         checks = 0;
  integer         k;

  always @(posedge clk) begin
    if (rst || j == T - 1) begin
      snapshot <= in;
      j <= 0;
    end else begin
      j <= j + 1;
    end
  end

  // Drive and check on the falling edge, when everything has settled.
  integer cyc;
  initial begin
    $dumpfile("tb_serializer_tdm.vcd");
    $dumpvars(0, tb_serializer_tdm);

    j = 0;
    @(negedge clk);
    randomize_in();
    @(negedge clk);
    rst = 1'b0;

    for (cyc = 0; cyc < NCYCLES; cyc = cyc + 1) begin
      check();
      randomize_in();
      // Reset once mid-frame to check that it restarts the frame.
      rst = (cyc == NCYCLES / 2 + 1);
      @(negedge clk);
    end

    if (errors == 0) $display("PASS: N=%0d K=%0d, %0d checks", N, K, checks);
    else $display("FAIL: N=%0d K=%0d, %0d errors in %0d checks", N, K, errors, checks);
    $finish;
  end

  // Fill in with N random bits, 32 at a time.
  reg     [N+31:0] rnd;
  integer          i;
  task randomize_in;
    begin
      for (i = 0; i < N; i = i + 32) rnd[i+:32] = $urandom;
      in = rnd[N-1:0];
    end
  endtask

  task check;
    begin
      checks = checks + 1;
      if (frame_start !== (j == 0)) begin
        errors = errors + 1;
        $display("%0t: frame_start=%b, expected %b (j=%0d)", $time, frame_start, j == 0, j);
      end
      for (k = 0; k < K; k = k + 1) begin
        if (out[k] !== snapshot[k*T+j]) begin
          errors = errors + 1;
          $display("%0t: out[%0d]=%b, expected %b (j=%0d)", $time, k, out[k], snapshot[k*T+j], j);
        end
      end
    end
  endtask

endmodule
