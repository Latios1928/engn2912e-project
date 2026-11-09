`timescale 1ns / 1ns

// Self-checking testbench for snn_top.
//
// First checks that words written through data/addr/wren land in the right
// place on the internal weights bus. Then, for each scenario, loads a weight
// set, waits SETTLE analog cycles with in = 0 (the network has no reset; the
// neuron leak drains what the previous scenario left), applies in for RUN
// analog cycles, and checks which neurons fired at least once against the
// expected set:
//   1. all weights max, in = 0             -> nothing fires
//   2. only pulse->input weights, in = 101 -> only input neurons 0 and 2
//   3. one path in1 -> hid2 -> out, in = 111 -> input 1, hidden 2, output
//   4. as 3 but hid2 -> out weight 0       -> input 1, hidden 2 only
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
  reg  [4:0] addr = 0;
  reg        wren = 1'b0;
  reg  [2:0] in = 0;
  wire [8:0] out;

  snn_top dut (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .wren(wren),
      .in(in),
      .out(out)
  );

  always #5 clk = ~clk;

  // Which neurons fired during the current scenario.
  reg [8:0] seen = 0;
  reg       counting = 1'b0;
  always @(out) if (counting) seen = seen | out;

  integer errors = 0;
  integer checks = 0;
  integer w;
  reg [91:0] ws;

  // Word indices (see snn_analog.v).
  function integer w_pulse(input integer i);
    w_pulse = i;
  endfunction
  function integer w_ih(input integer i, input integer j);
    w_ih = 3 + 3 * j + i;
  endfunction
  function integer w_ho(input integer j);
    w_ho = 18 + j;
  endfunction

  initial begin
    $dumpfile("tb_snn_top.vcd");
    $dumpvars(0, tb_snn_top);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // Register file: word w = w mod 16, plus an out-of-range write that must be ignored.
    for (w = 0; w < 23; w = w + 1) ws[w*4+:4] = w[3:0];
    load(ws);
    write_word(5'd31, 4'hF);
    checks = checks + 1;
    if (dut.w !== ws) begin
      errors = errors + 1;
      $display("rf: weights=%h, expected %h", dut.w, ws);
    end

    ws = {92{1'b1}};
    load(ws);
    run(3'b000, 9'b0_00000_000, "in = 0");

    ws = 0;
    for (w = 0; w < 3; w = w + 1) ws[w_pulse(w)*4+:4] = 4'hF;
    load(ws);
    run(3'b101, 9'b0_00000_101, "pulse weights only");

    ws = 0;
    ws[w_pulse(1)*4+:4] = 4'hF;
    ws[w_ih(1, 2)*4+:4] = 4'hF;
    ws[w_ho(2)*4+:4] = 4'hF;
    load(ws);
    run(3'b111, 9'b1_00100_010, "path in1->hid2->out");

    ws[w_ho(2)*4+:4] = 4'h0;
    load(ws);
    run(3'b111, 9'b0_00100_010, "hid2->out weight 0");

    if (errors == 0) $display("PASS: snn_top, %0d checks", checks);
    else $display("FAIL: snn_top, %0d errors in %0d checks", errors, checks);
    $finish;
  end

  task write_word(input [4:0] a, input [3:0] d);
    begin
      @(negedge clk);
      addr = a;
      data = d;
      wren = 1'b1;
      @(negedge clk);
      wren = 1'b0;
    end
  endtask

  task load(input [91:0] weights);
    integer i;
    begin
      for (i = 0; i < 23; i = i + 1) write_word(i[4:0], weights[i*4+:4]);
    end
  endtask

  task run(input [2:0] in_v, input [8:0] expected, input [8*24:1] name);
    begin
      in = 3'b000;
      #(SETTLE * CLK_PERIOD);
      in = in_v;
      seen = out;
      counting = 1'b1;
      #(RUN * CLK_PERIOD);
      counting = 1'b0;
      in = 3'b000;
      checks = checks + 1;
      if (seen !== expected) begin
        errors = errors + 1;
        $display("%0s: fired %b, expected %b ({out, hid[4:0], in[2:0]})", name, seen, expected);
      end
    end
  endtask

endmodule
