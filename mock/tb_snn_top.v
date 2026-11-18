`timescale 1ns / 1ns

// Self-checking testbench for snn_top.
//
// First checks that weights and signs written through data/addr (regs.v
// protocol) land in the right place on w and s. Then, for each scenario, loads
// a weight set, waits SETTLE analog cycles with in = 0 (the network has no
// reset; the neuron leak drains what the previous scenario left), applies in
// for RUN analog cycles, and checks which neurons fired at least once against
// the expected set:
//   1. all weights max, in = 00             -> nothing fires
//   2. only pulse->input weights, in = 01   -> only input neuron 0
//   3. one path in1 -> hid1 -> out, in = 11 -> input 1, hidden 1, output
//   4. as 3 but hid1 -> out weight 0        -> input 1, hidden 1 only
//   5. as 3 plus in0 -> hid1 at -max, in = 11: the two inputs fire together
//      and cancel at hid1                   -> inputs 0 and 1 only
// clk (10 ns) and the network's own clock (14 ns) are unrelated.
// Synapse k has magnitude w[4k+3:4k] (max 15) and sign s[k] (1 = inhibitory).
// The same scenarios run on the transistor-level network in
// ../mixed/snn_ms_tb.v.
//
// Run (from this folder):
//   iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp -f sim.f && vvp sim.vvp
module tb_snn_top;
  // CLK_PERIOD: the default of snn_analog (mock/snn_analog.v), ns.
  // SETTLE: the leak drains at most THRESHOLD (1000) at 1 per cycle.
  localparam CLK_PERIOD = 14;  // ns
  localparam SETTLE = 1500;  // analog cycles
  localparam RUN = 1000;  // analog cycles

  reg        clk = 1'b0;
  reg        rst = 1'b1;
  reg  [3:0] data = 0;
  reg  [3:0] addr = 4'hF;  // idle
  reg  [1:0] in = 0;
  wire [4:0] out;

  snn_top dut (
      .clk (clk),
      .rst (rst),
      .data(data),
      .addr(addr),
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
  reg [7:0] ss;
  localparam [3:0] MAX = 4'hF;

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

    // Registers: word w = w, signs 10100101.
    for (w = 0; w < 8; w = w + 1) ws[w*4+:4] = w[3:0];
    ss = 8'b1010_0101;
    load(ws, ss);
    checks = checks + 1;
    if (dut.w !== ws || dut.s !== ss) begin
      errors = errors + 1;
      $display("regs: w=%h s=%b, expected %h %b", dut.w, dut.s, ws, ss);
    end

    ws = {8{MAX}};
    ss = 0;
    load(ws, ss);
    run(2'b00, 5'b0_00_00, "in = 0");

    ws = 0;
    for (w = 0; w < 2; w = w + 1) ws[w_pulse(w)*4+:4] = MAX;
    load(ws, ss);
    run(2'b01, 5'b0_00_01, "pulse weights only");

    ws = 0;
    ws[w_pulse(1)*4+:4] = MAX;
    ws[w_ih(1, 1)*4+:4] = MAX;
    ws[w_ho(1)*4+:4] = MAX;
    load(ws, ss);
    run(2'b11, 5'b1_10_10, "path in1->hid1->out");

    ws[w_ho(1)*4+:4] = 4'h0;
    load(ws, ss);
    run(2'b11, 5'b0_10_10, "hid1->out weight 0");

    ws[w_ho(1)*4+:4] = MAX;
    ws[w_pulse(0)*4+:4] = MAX;
    ws[w_ih(0, 1)*4+:4] = MAX;
    ss[w_ih(0, 1)] = 1'b1;  // inhibitory
    load(ws, ss);
    run(2'b11, 5'b0_00_11, "in0 inhibits hid1");

    if (errors == 0) $display("PASS: snn_top, %0d checks", checks);
    else $display("FAIL: snn_top, %0d errors in %0d checks", errors, checks);
    $finish;
  end

  // regs.v protocol: data while idle, address for one cycle, back to idle
  task write_word(input [3:0] a, input [3:0] d);
    begin
      @(negedge clk);
      data = d;
      @(negedge clk);
      addr = a;
      @(negedge clk);
      addr = 4'hF;
    end
  endtask

  task load(input [31:0] weights, input [7:0] signs);
    integer i;
    begin
      for (i = 0; i < 8; i = i + 1) write_word(i[3:0], weights[i*4+:4]);
      write_word(4'd8, signs[3:0]);
      write_word(4'd9, signs[7:4]);
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
