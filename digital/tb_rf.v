`timescale 1ns / 1ns

// Self-checking testbench for rf, kept short so the waveform fits on a slide.
//
//   1. write words 0-3 on four back-to-back cycles (wren held high)
//   2. one cycle with wren low: addr/data change but nothing is written
//   3. write word 7, then overwrite word 1
//
// weights is shown in hex, so each hex digit is one 4-bit word (word 7 on the
// left, word 0 on the right): 00000000 -> 00004321 -> A0004321 -> A0004371.
// A reference copy of the words is updated on the same clock edge, and weights
// must match it on every falling edge.
//
// Run (from this folder):
//   iverilog -g2012 -Wall -o sim.vvp rf.v tb_rf.v && vvp sim.vvp
module tb_rf;
  reg         clk = 1'b0;
  reg         wren = 1'b0;
  reg  [ 2:0] addr = 0;
  reg  [ 3:0] data = 0;
  wire [31:0] weights;

  rf #(
      .NUM_WORDS(8),
      .WIDTH(4),
      .AW(3)
  ) dut (
      .clk(clk),
      .wren(wren),
      .addr(addr),
      .data(data),
      .weights(weights)
  );

  always #5 clk = ~clk;

  // Reference model and check.
  reg     [31:0] expected = 0;
  integer        errors = 0;
  integer        checks = 0;
  always @(posedge clk) if (wren) expected[addr*4+:4] <= data;
  always @(negedge clk) begin
    checks = checks + 1;
    if (weights !== expected) begin
      errors = errors + 1;
      $display("%0t: weights=%h, expected %h", $time, weights, expected);
    end
  end

  // Set the inputs for one clock cycle (they change on the falling edge).
  task drive(input w, input [2:0] a, input [3:0] d);
    begin
      wren = w;
      addr = a;
      data = d;
      @(negedge clk);
    end
  endtask

  integer i;

  initial begin
    $dumpfile("tb_rf.vcd");
    $dumpvars(0, tb_rf);

    // rf has no reset; clear it so the waveform starts at 00000000.
    for (i = 0; i < 8; i = i + 1) dut.weights[i*4+:4] = 4'h0;

    @(negedge clk);
    drive(1'b0, 3'd0, 4'h0);
    drive(1'b1, 3'd0, 4'h1);  // 1. back-to-back writes
    drive(1'b1, 3'd1, 4'h2);
    drive(1'b1, 3'd2, 4'h3);
    drive(1'b1, 3'd3, 4'h4);
    drive(1'b0, 3'd5, 4'hF);  // 2. wren low: ignored
    drive(1'b1, 3'd7, 4'hA);  // 3. write word 7
    drive(1'b1, 3'd1, 4'h7);  //    overwrite word 1
    drive(1'b0, 3'd0, 4'h0);
    drive(1'b0, 3'd0, 4'h0);

    if (errors == 0) $display("PASS: rf, %0d checks", checks);
    else $display("FAIL: rf, %0d errors in %0d checks", errors, checks);
    $finish;
  end

endmodule
