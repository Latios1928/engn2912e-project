`timescale 1ns / 1ns

// Self-checking testbench for snn_top.
//
// First checks that words written through data/addr/wren land in the right
// place on the internal weights bus. Then, for each scenario, loads a weight
// set, waits SETTLE analog cycles with in = 0 (the network has no reset; the
// neuron leak drains what the previous scenario left), applies in for RUN
// analog cycles, and checks which neurons fired at least once against the
// expected set:
//   1. all weights max, in = 00             -> nothing fires
//   2. only pulse->input weights, in = 01   -> only input neuron 0
//   3. one path in1 -> hid1 -> out, in = 11 -> input 1, hidden 1, output
//   4. as 3 but hid1 -> out weight 0        -> input 1, hidden 1 only
// clk (10 ns) and the network's own clock (14 ns) are unrelated.
// "Max" weight is 4'hF. The same scenarios run on the transistor-level
// network in ../mixed/snn_ms_tb.v.
//
// Run (from this folder):
//   iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp -f sim.f && vvp sim.vvp
module tb_snn_top;
  localparam CLK_PERIOD = 14;  // ns; the CLK_PERIOD default of snn_analog (mock/snn_analog.v)
  localparam SETTLE = 1500;  // analog cycles; the leak drains at most THRESHOLD (1000) at 1 per cycle
  localparam RUN = 1000;  // analog cycles

  reg        clk = 1'b0;
  reg        rst = 1'b1;
  reg  [3:0] data = 0;
  reg  [2:0] addr = 0;
  reg        wren = 1'b0;
  reg  [1:0] in = 0;
  wire [4:0] out;

  snn_top dut (
      .clk (clk),
      .rst (rst),
      .data(data),
      .addr(addr),
      .wren(wren),
      .in  (in),
      .out (out)
  );

  always #5 clk = ~clk;

  // Which neurons fired during the current scenario.
  reg [4:0] seen = 0;
  reg       counting = 1'b0;
  always @(out) if (counting) seen = seen | out;

  integer errors = 0;
  integer checks = 0;
  integer w;
  reg [31:0] ws;

  // Word indices (see snn_analog.v).
  function integer w_pulse(input integer i);
    w_pulse = i;
  endfunction
  function integer w_ih(input integer i, input integer j);
    w_ih = 2 + 2 * j + i;
  endfunction
  function integer w_ho(input integer j);
    w_ho = 6 + j;
  endfunction

  initial begin
    $dumpfile("tb_snn_top.vcd");
    $dumpvars(0, tb_snn_top);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // Register file: word w = w.
    for (w = 0; w < 8; w = w + 1) ws[w*4+:4] = w[3:0];
    load(ws);
    checks = checks + 1;
    if (dut.w !== ws) begin
      errors = errors + 1;
      $display("rf: weights=%h, expected %h", dut.w, ws);
    end

    ws = {32{1'b1}};
    load(ws);
    run(2'b00, 5'b0_00_00, "in = 0");

    ws = 0;
    for (w = 0; w < 2; w = w + 1) ws[w_pulse(w)*4+:4] = 4'hF;
    load(ws);
    run(2'b01, 5'b0_00_01, "pulse weights only");

    ws = 0;
    ws[w_pulse(1)*4+:4] = 4'hF;
    ws[w_ih(1, 1)*4+:4] = 4'hF;
    ws[w_ho(1)*4+:4] = 4'hF;
    load(ws);
    run(2'b11, 5'b1_10_10, "path in1->hid1->out");

    ws[w_ho(1)*4+:4] = 4'h0;
    load(ws);
    run(2'b11, 5'b0_10_10, "hid1->out weight 0");

    if (errors == 0) $display("PASS: snn_top, %0d checks", checks);
    else $display("FAIL: snn_top, %0d errors in %0d checks", errors, checks);
    $finish;
  end

  task write_word(input [2:0] a, input [3:0] d);
    begin
      @(negedge clk);
      addr = a;
      data = d;
      wren = 1'b1;
      @(negedge clk);
      wren = 1'b0;
    end
  endtask

  task load(input [31:0] weights);
    integer i;
    begin
      for (i = 0; i < 8; i = i + 1) write_word(i[2:0], weights[i*4+:4]);
    end
  endtask

  task run(input [1:0] in_v, input [4:0] expected, input [8*24:1] name);
    begin
      in = 2'b00;
      #(SETTLE * CLK_PERIOD);
      in = in_v;
      seen = out;
      counting = 1'b1;
      #(RUN * CLK_PERIOD);
      counting = 1'b0;
      in = 2'b00;
      checks = checks + 1;
      if (seen !== expected) begin
        errors = errors + 1;
        $display("%0s: fired %b, expected %b ({out, hid[1:0], in[1:0]})", name, seen, expected);
      end
    end
  endtask

endmodule
