`timescale 1ns / 1ns

// Self-checking testbench for pulse_gen.
//
// A reference model written from the spec runs beside the DUT: numbering the
// clock edges after reset 1, 2, 3, ..., after edge e the DUT must show, for
// each channel, a pulse exactly when that channel's en, as sampled at the
// last edge that was a multiple of PERIOD, was high and e mod PERIOD < WIDTH.
// en is changed at random times (mostly mid-period) and a reset is applied in
// the middle of the run. Two direct checks: a steady en gives pulses of
// exactly WIDTH cycles every PERIOD cycles, and the first pulse after en
// rises starts within PERIOD cycles and is not cut short.
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp pulse_gen.v tb_pulse_gen.v && vvp sim.vvp
//   iverilog -g2012 -Ptb_pulse_gen.PERIOD=1 -Ptb_pulse_gen.WIDTH=1 ...   (other shapes)
module tb_pulse_gen #(
    parameter PERIOD = 7,
    parameter WIDTH  = 3
);
  reg        clk = 1'b0;
  reg        rst = 1'b1;
  reg  [2:0] en = 3'b000;
  wire [2:0] pulse;

  pulse_gen #(
      .PERIOD(PERIOD),
      .WIDTH (WIDTH)
  ) dut (
      .clk(clk),
      .rst(rst),
      .en(en),
      .pulse(pulse)
  );

  always #5 clk = ~clk;

  integer errors = 0;
  integer checks = 0;

  // Reference model, updated on the same edge as the DUT.
  integer e = 0;  // edges since reset
  reg [2:0] en_s = 3'b000;  // en as sampled at the last multiple of PERIOD
  reg [2:0] exp_pulse = 3'b000;
  always @(posedge clk) begin
    if (rst) begin
      e = 0;
      en_s = 3'b000;
      exp_pulse = 3'b000;
    end else begin
      e = e + 1;
      if (e % PERIOD == 0) en_s = en;
      exp_pulse = (e % PERIOD < WIDTH) ? en_s : 3'b000;
    end
  end

  task check;
    begin
      checks = checks + 1;
      if (pulse !== exp_pulse) begin
        errors = errors + 1;
        $display("%0t: pulse=%b, expected %b (en=%b, e=%0d)", $time, pulse, exp_pulse, en, e);
      end
    end
  endtask

  // Check every cycle on the falling edge.
  always @(negedge clk) check;

  integer n;
  integer high;
  integer waited;

  initial begin
    $dumpfile("tb_pulse_gen.vcd");
    $dumpvars(0, tb_pulse_gen);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // Steady en on channel 0: after the first period boundary, every period
    // must contain exactly WIDTH high cycles.
    en = 3'b001;
    repeat (PERIOD) @(negedge clk);  // reach a period boundary
    repeat (3) begin
      high = 0;
      repeat (PERIOD) begin
        @(negedge clk);
        if (pulse[0]) high = high + 1;
      end
      checks = checks + 1;
      if (high !== WIDTH) begin
        errors = errors + 1;
        $display("steady en: %0d high cycles in a period, expected %0d", high, WIDTH);
      end
    end

    // First pulse after en rises: starts within PERIOD cycles, WIDTH long.
    en = 3'b000;
    repeat (2 * PERIOD) @(negedge clk);
    en[1] = 1'b1;
    waited = 0;
    while (!pulse[1] && waited <= PERIOD) begin
      @(negedge clk);
      waited = waited + 1;
    end
    checks = checks + 1;
    if (waited > PERIOD) begin
      errors = errors + 1;
      $display("first pulse did not start within PERIOD cycles of en rising");
    end
    high = 0;
    while (pulse[1]) begin
      high = high + 1;
      @(negedge clk);
      en[1] = 1'b0;  // dropped mid-pulse: the pulse must still be WIDTH long
    end
    // (With WIDTH == PERIOD the output is continuous while enabled, so it has
    // no fixed length to check.)
    if (WIDTH < PERIOD) begin
      checks = checks + 1;
      if (high !== WIDTH) begin
        errors = errors + 1;
        $display("first pulse: %0d cycles, expected %0d", high, WIDTH);
      end
    end

    // Random en changes against the model, with a reset in the middle.
    for (n = 0; n < 40 * PERIOD; n = n + 1) begin
      @(negedge clk);
      if ($urandom % 3 == 0) en = 3'($urandom);
      if (n == 20 * PERIOD + 3) rst = 1'b1;
      if (n == 20 * PERIOD + 5) rst = 1'b0;
    end

    if (errors == 0) $display("PASS: PERIOD=%0d WIDTH=%0d, %0d checks", PERIOD, WIDTH, checks);
    else $display("FAIL: PERIOD=%0d WIDTH=%0d, %0d errors in %0d checks", PERIOD, WIDTH, errors, checks);
    $finish;
  end

endmodule
