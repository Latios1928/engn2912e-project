// Self-checking testbench for deserializer_tdm.
//
// in is randomized every cycle. A reference model applies the exact same
// shift-in-from-MSB update rule as the DUT, so out must match the
// reference model's shift register on every cycle, not just at frame
// completion -- this also verifies the live (mid-frame, partially-filled)
// value of out, not just the final assembled word.
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp deserializer_tdm.v tb_deserializer_tdm.v && vvp sim.vvp
//   iverilog -g2012 -Ptb_deserializer_tdm.N=12 -Ptb_deserializer_tdm.K=4 ...   (other sizes)

module tb_deserializer_tdm #(
    parameter N = 8,
    parameter K = 2,
    parameter NCYCLES = 200
);
  localparam T = N / K;

  reg          clk = 1'b0;
  reg          rst = 1'b1;
  reg  [K-1:0] in = 0;
  wire [N-1:0] out;
  wire         frame_done;

  deserializer_tdm #(
      .N(N),
      .K(K)
  ) dut (
      .clk(clk),
      .rst(rst),
      .in(in),
      .out(out),
      .frame_done(frame_done)
  );

  always #5 clk = ~clk;

  // Reference model: same shift-in-from-MSB rule as the DUT, plus a frame phase counter.
  reg     [N-1:0] ref_sr;
  integer         j;
  integer         errors = 0;
  integer         checks = 0;
  integer         k;

  always @(posedge clk) begin
    if (rst) begin
      ref_sr <= 0;
      j <= 0;
    end else begin
      for (k = 0; k < K; k = k + 1)
        ref_sr[k*T+:T] <= (ref_sr[k*T+:T] >> 1) | (in[k] << (T - 1));
      j <= (j == T - 1) ? 0 : j + 1;
    end
  end

  // Drive and check on the falling edge, when everything has settled.
  integer cyc;
  initial begin
    $dumpfile("tb_deserializer_tdm.vcd");
    $dumpvars(0, tb_deserializer_tdm);

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

  // Fill in with K random bits, 32 at a time.
  reg     [K+31:0] rnd;
  integer          i;
  task randomize_in;
    begin
      for (i = 0; i < K; i = i + 32) rnd[i+:32] = $urandom;
      in = rnd[K-1:0];
    end
  endtask

  task check;
    begin
      checks = checks + 1;
      if (frame_done !== (j == T - 1)) begin
        errors = errors + 1;
        $display("%0t: frame_done=%b, expected %b (j=%0d)", $time, frame_done, j == T - 1, j);
      end
      if (out !== ref_sr) begin
        errors = errors + 1;
        $display("%0t: out=%b, expected %b (j=%0d)", $time, out, ref_sr, j);
      end
    end
  endtask

endmodule
