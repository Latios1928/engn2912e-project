// Self-checking testbench for snn_top.
//
// First checks that words written through data/addr/wren land in the right
// place on the internal weights bus. Then loads a weight set per scenario,
// resets the network, applies in for RUN clk_analog cycles, and checks which
// neurons fired at least once against the expected set:
//   1. all weights max, in = 0          -> nothing fires
//   2. only pulse->input weights, in = 101 -> only input neurons 0 and 2
//   3. one path in1 -> hid2 -> out, in = 111 -> input 1, hidden 2, output
//   4. as 3 but hid2 -> out weight 0     -> input 1, hidden 2 only
// clk and clk_analog run at unrelated periods.
//
// Run (from the repo root):
//   iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp digital/rf.v analog/mock/*.v snn_top.v tb_snn_top.v && vvp sim.vvp
module tb_snn_top;
  localparam RUN = 1000;

  reg        clk = 1'b0;
  reg        clk_analog = 1'b0;
  reg        rst = 1'b1;
  reg  [2:0] data = 0;
  reg  [4:0] addr = 0;
  reg        wren = 1'b0;
  reg  [2:0] in = 0;
  wire [8:0] out;

  snn_top dut (
      .clk(clk),
      .clk_analog(clk_analog),
      .rst(rst),
      .data(data),
      .addr(addr),
      .wren(wren),
      .in(in),
      .out(out)
  );

  always #5 clk = ~clk;
  always #7 clk_analog = ~clk_analog;

  // Which neurons fired during the current scenario.
  reg [8:0] seen = 0;
  reg       counting = 1'b0;
  always @(posedge clk_analog) if (counting) seen <= seen | out;

  integer errors = 0;
  integer checks = 0;
  integer w;
  reg [68:0] ws;

  // Word indices (see analog/mock/snn.v).
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

    // Register file: word w = w mod 8, plus an out-of-range write that must be ignored.
    for (w = 0; w < 23; w = w + 1) ws[w*3+:3] = w[2:0];
    load(ws);
    write_word(5'd31, 3'd7);
    checks = checks + 1;
    if (dut.weights !== ws) begin
      errors = errors + 1;
      $display("rf: weights=%h, expected %h", dut.weights, ws);
    end

    ws = {69{1'b1}};
    load(ws);
    run(3'b000, 9'b0_00000_000, "in = 0");

    ws = 0;
    for (w = 0; w < 3; w = w + 1) ws[w_pulse(w)*3+:3] = 3'd7;
    load(ws);
    run(3'b101, 9'b0_00000_101, "pulse weights only");

    ws = 0;
    ws[w_pulse(1)*3+:3] = 3'd7;
    ws[w_ih(1, 2)*3+:3] = 3'd7;
    ws[w_ho(2)*3+:3] = 3'd7;
    load(ws);
    run(3'b111, 9'b1_00100_010, "path in1->hid2->out");

    ws[w_ho(2)*3+:3] = 3'd0;
    load(ws);
    run(3'b111, 9'b0_00100_010, "hid2->out weight 0");

    if (errors == 0) $display("PASS: snn_top, %0d checks", checks);
    else $display("FAIL: snn_top, %0d errors in %0d checks", errors, checks);
    $finish;
  end

  task write_word(input [4:0] a, input [2:0] d);
    begin
      @(negedge clk);
      addr = a;
      data = d;
      wren = 1'b1;
      @(negedge clk);
      wren = 1'b0;
    end
  endtask

  task load(input [68:0] weights);
    integer i;
    begin
      for (i = 0; i < 23; i = i + 1) write_word(i[4:0], weights[i*3+:3]);
    end
  endtask

  task run(input [2:0] in_v, input [8:0] expected, input [8*24:1] name);
    begin
      @(negedge clk_analog);
      rst = 1'b1;
      in  = 3'b000;
      @(negedge clk_analog);
      rst = 1'b0;
      in = in_v;
      seen = 0;
      counting = 1'b1;
      repeat (RUN) @(negedge clk_analog);
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
