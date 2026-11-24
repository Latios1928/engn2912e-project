`timescale 1ns / 1ps

// Gate-level timing testbench for the digital part of snn_top, at the chip's real 1 MHz
// clock. It runs with zero-delay cells or with an SDF from LibreLane (`make timing`).
//
// Why a separate testbench: tb_snn_top.v (the `make` target) drives a behavioral analog
// model and clocks at 10 ns to suit that model. With slow-corner delays, a 10 ns clock
// would report setup failures that cannot happen on the chip. This one leaves the analog
// macro an empty black box and checks only what the digital part delivers to it:
//   0. after reset the inputs are off (INPUT EN, register 14, resets to 00): no pulses
//   1. the reset pulse timing (period 200, width 10 clk = 10 us every 200 us, the 5 kHz
//      operating rate), measured on the pulse nets into the macro
//   2. weights and signs written through data/addr reach w[31:0] / s[7:0], for several
//      patterns, with no X
//   3. new pulse timing written through the registers (period 20, width 3)
//   4. one channel enabled: the other stays low; width 0: no pulses
//   5. rst mid-run clears INPUT EN (no pulses after it) and keeps weights and signs
// The pulse period is measured rising edge to rising edge and the width rising to falling
// edge, each to 5 ns: both edges come from the same flip-flop, so a period is exact and a
// width is off only by the rise/fall delay difference.
// Icarus applies the SDF delays but does not run the cells' setup/hold checks; OpenSTA
// signs those off (all corners clean).
module tb_gls_timing;
  localparam [3:0] IDLE = 4'hF;
  localparam [3:0] A_SIGN_LO = 4'd8, A_SIGN_HI = 4'd9;
  localparam [3:0] A_PER_LO = 4'd10, A_PER_HI = 4'd11;
  localparam [3:0] A_WID_LO = 4'd12, A_WID_HI = 4'd13;
  localparam [3:0] A_IN_EN = 4'd14;
  localparam real TCLK = 1000.0;  // ns, 1 MHz
  localparam real TOL = 5.0;  // ns

  reg clk = 1'b0;
  reg rst = 1'b1;
  reg [3:0] addr = IDLE;
  reg [3:0] data = 4'h0;
  wire [4:0] out;
  wire Iref, VT;

  always #500 clk = ~clk;

  snn_top dut (
      .Iref(Iref),
      .VT  (VT),
      .clk (clk),
      .rst (rst),
      .data(data),
      .addr(addr),
      .out (out)
  );

`ifdef SDF_FILE
  initial $sdf_annotate(`SDF_FILE, dut);
`endif

  // The macro's inputs (ports of the black-box instance, present in the flat netlist)
  wire [31:0] w = dut.u_snn_analog.w;
  wire [7:0] s = dut.u_snn_analog.s;
  wire [1:0] p = dut.u_snn_analog.pulse;

  integer errors = 0;
  integer checks = 0;

  task fail(input [8*80-1:0] msg);
    begin
      errors = errors + 1;
      $display("tb_gls_timing: FAIL %0s (t = %0t)", msg, $time);
    end
  endtask

  task write_reg(input [3:0] a, input [3:0] d);
    begin
      @(negedge clk);
      data = d;
      @(negedge clk);
      addr = a;
      @(negedge clk);
      addr = IDLE;
    end
  endtask

  // Input enables: register 14 (INPUT EN), bits [1:0]
  task set_in(input [1:0] en);
    write_reg(A_IN_EN, {2'b00, en});
  endtask

  task load(input [31:0] ws, input [7:0] ss);
    integer i;
    begin
      for (i = 0; i < 8; i = i + 1) write_reg(i[3:0], ws[i*4+:4]);
      write_reg(A_SIGN_LO, ss[3:0]);
      write_reg(A_SIGN_HI, ss[7:4]);
      @(negedge clk);
      checks = checks + 1;
      if (w !== ws || s !== ss) begin
        fail("weights / signs");
        $display("  w = %h s = %b, expected %h %b", w, s, ws, ss);
      end
    end
  endtask

  task timing(input [7:0] per, input [7:0] wid);
    begin
      write_reg(A_PER_LO, per[3:0]);
      write_reg(A_PER_HI, per[7:4]);
      write_reg(A_WID_LO, wid[3:0]);
      write_reg(A_WID_HI, wid[7:4]);
    end
  endtask

  // Period and width of channel ch, from the second pulse on (the first one after a
  // change may still use the old timing, which is sampled at period boundaries)
  task automatic measure(input integer ch, input real per_exp, input real wid_exp);
    realtime r1, f1, r2;
    begin
      wait (p[ch] === 1'b1);
      wait (p[ch] === 1'b0);
      wait (p[ch] === 1'b1);
      r1 = $realtime;
      wait (p[ch] === 1'b0);
      f1 = $realtime;
      wait (p[ch] === 1'b1);
      r2 = $realtime;
      checks = checks + 1;
      if ((r2 - r1) < per_exp * TCLK - TOL || (r2 - r1) > per_exp * TCLK + TOL ||
          (f1 - r1) < wid_exp * TCLK - TOL || (f1 - r1) > wid_exp * TCLK + TOL) begin
        fail("pulse timing");
        $display("  channel %0d: period %0.3f ns width %0.3f ns, expected %0.0f / %0.0f clk",
                 ch, r2 - r1, f1 - r1, per_exp, wid_exp);
      end else
        $display("tb_gls_timing: channel %0d: period %0.3f us, width %0.3f us", ch,
                 (r2 - r1) / 1000.0, (f1 - r1) / 1000.0);
    end
  endtask

  // No pulse on channel ch for n clock cycles
  task automatic quiet(input integer ch, input integer n);
    integer i;
    begin
      checks = checks + 1;
      for (i = 0; i < n; i = i + 1) begin
        @(posedge clk);
        if (p[ch] !== 1'b0) begin
          fail("expected no pulses");
          $display("  channel %0d = %b", ch, p[ch]);
          i = n;
        end
      end
    end
  endtask

  initial begin
    #20_000_000;  // 20 ms
    $display("tb_gls_timing: FAIL timeout");
    $finish;
  end

  initial begin
`ifdef SDF_FILE
    $display("tb_gls_timing: SDF %0s", `SDF_FILE);
`else
    $display("tb_gls_timing: zero-delay cells");
`endif
    repeat (3) @(negedge clk);
    rst = 1'b0;
    @(negedge clk);
    checks = checks + 1;
    if (p !== 2'b00) fail("pulse not 0 after reset");

    // 0. Inputs off after reset: two default periods without pulses
    fork
      quiet(0, 400);
      quiet(1, 400);
    join

    // 1. Reset timing, both channels
    set_in(2'b11);
    fork
      measure(0, 200, 10);
      measure(1, 200, 10);
    join

    // 2. Weights and signs
    load(32'h7654_3210, 8'b1010_0101);
    load(32'hFFFF_FFFF, 8'hFF);
    load(32'h0000_0000, 8'h00);
    load(32'hA5C3_96E1, 8'b0110_1001);
    load(32'h1234_ABCD, 8'b1100_0011);

    // 3. New timing through the registers
    timing(8'd20, 8'd3);
    fork
      measure(0, 20, 3);
      measure(1, 20, 3);
    join

    // 4. One channel only; then width 0
    set_in(2'b01);
    repeat (60) @(negedge clk);  // two periods: en is sampled at period boundaries
    fork
      measure(0, 20, 3);
      quiet(1, 60);
    join
    timing(8'd20, 8'd0);
    repeat (60) @(negedge clk);
    quiet(0, 60);

    // 5. rst mid-run: both channels running, then a reset clears INPUT EN (and restores
    // timing 200 / 10); weights and signs are kept
    timing(8'd20, 8'd3);
    set_in(2'b11);
    fork
      measure(0, 20, 3);
      measure(1, 20, 3);
    join
    @(negedge clk);
    rst = 1'b1;
    @(negedge clk);
    rst = 1'b0;
    fork
      quiet(0, 400);
      quiet(1, 400);
    join
    checks = checks + 1;
    if (w !== 32'h1234_ABCD || s !== 8'b1100_0011) fail("weights / signs changed by rst");

    if (errors == 0) $display("tb_gls_timing: PASS, %0d checks", checks);
    else $display("tb_gls_timing: FAIL, %0d of %0d checks", errors, checks);
    $finish;
  end
endmodule
