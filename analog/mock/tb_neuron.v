// Self-checking testbench for neuron (and the comparator inside it) and dac.
//
// A reference model of the neuron spec runs alongside the DUT; voltage and
// active must match it every cycle. The stimulus covers a normal fire, the
// DURATION+1-cycle active window with voltage held at 0, zero input, and
// saturation at 16'hFFFF. The first fire is also checked against a
// hand-computed cycle and window length. The dac is checked exhaustively.
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp comparator.v dac.v neuron.v tb_neuron.v && vvp sim.vvp
module tb_neuron;
  localparam INDEGREE = 2;
  localparam DURATION = 3;
  localparam THRESHOLD = 100;
  localparam GAIN = 16;
  localparam [15:0] G = GAIN;

  reg                    clk = 1'b0;
  reg                    rst = 1'b1;
  reg  [INDEGREE*16-1:0] currents = 0;
  wire                   active;

  neuron #(
      .INDEGREE (INDEGREE),
      .DURATION (DURATION),
      .THRESHOLD(THRESHOLD)
  ) dut (
      .clk_analog(clk),
      .rst(rst),
      .currents(currents),
      .active(active)
  );

  reg         dac_active;
  reg  [ 2:0] dac_weight;
  wire [15:0] dac_current;

  dac #(
      .GAIN(GAIN)
  ) u_dac (
      .active (dac_active),
      .weight (dac_weight),
      .current(dac_current)
  );

  always #5 clk = ~clk;

  // Reference model, updated on the same edge as the DUT.
  integer mv;  // voltage
  integer mc;  // comparator countdown
  integer sum;
  integer k;

  always @(posedge clk) begin
    sum = mv;
    for (k = 0; k < INDEGREE; k = k + 1) sum = sum + $signed({16'd0, currents[k*16+:16]});
    if (rst || mc > 0) mv <= 0;
    else mv <= (sum > 65535) ? 65535 : sum;
    if (rst) mc <= 0;
    else if (mv > THRESHOLD) mc <= DURATION;
    else if (mc > 0) mc <= mc - 1;
  end

  integer errors = 0;
  integer checks = 0;
  integer cyc;
  integer first_fire = -1;
  integer first_len = 0;
  integer saturated = 0;
  integer d;  // dac loop; k belongs to the model

  initial begin
    $dumpfile("tb_neuron.vcd");
    $dumpvars(0, tb_neuron);

    mv = 0;
    mc = 0;
    @(negedge clk);
    rst = 1'b0;

    // 40 per cycle: voltage 40, 80, 120 > 100 after edges 1-3, so active rises
    // on edge 4, i.e. at check cycle 4 (cycle 0 is sampled before edge 1).
    currents = {16'd30, 16'd10};
    for (cyc = 0; cyc < 30; cyc = cyc + 1) begin
      check();
      if (active && first_fire < 0) first_fire = cyc;
      if (first_fire >= 0 && first_len == cyc - first_fire && active) first_len = first_len + 1;
      @(negedge clk);
    end
    expect_int("first fire cycle", first_fire, 4);
    expect_int("active window", first_len, DURATION + 1);

    currents = 0;
    repeat (10) begin
      check();
      @(negedge clk);
    end

    // Sum of voltage and two max currents overflows 16 bits: must saturate.
    currents = {16'hFFFF, 16'hFFFF};
    repeat (10) begin
      check();
      if (dut.voltage == 16'hFFFF) saturated = 1;
      @(negedge clk);
    end
    expect_int("saturated", saturated, 1);

    for (d = 0; d < 16; d = d + 1) begin
      {dac_active, dac_weight} = d[3:0];
      #1;
      checks = checks + 1;
      if (dac_current !== (dac_active ? {13'd0, dac_weight} * G : 16'd0)) begin
        errors = errors + 1;
        $display("dac: active=%b weight=%0d current=%0d", dac_active, dac_weight, dac_current);
      end
    end

    if (errors == 0) $display("PASS: neuron + dac, %0d checks", checks);
    else $display("FAIL: neuron + dac, %0d errors in %0d checks", errors, checks);
    $finish;
  end

  task check;
    begin
      checks = checks + 1;
      if (dut.voltage !== mv[15:0] || active !== (mc > 0)) begin
        errors = errors + 1;
        $display("%0t: voltage=%0d active=%b, expected voltage=%0d active=%b", $time, dut.voltage,
                 active, mv, mc > 0);
      end
    end
  endtask

  task expect_int(input [8*20:1] name, input integer got, input integer want);
    begin
      checks = checks + 1;
      if (got != want) begin
        errors = errors + 1;
        $display("%0s: got %0d, expected %0d", name, got, want);
      end
    end
  endtask

endmodule
