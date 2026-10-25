// Self-checking testbench for pulse_gen.
//
// With en high, pulse must be high exactly when (cycles since en rose) mod
// PERIOD < WIDTH. en is dropped mid-period and raised again to check that
// the pattern restarts from the start of a pulse, and pulse must stay low
// while en is low.
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp pulse_gen.v tb_pulse_gen.v && vvp sim.vvp
//   iverilog -g2012 -Ptb_pulse_gen.PERIOD=1 -Ptb_pulse_gen.WIDTH=1 ...   (other shapes)
module tb_pulse_gen #(
    parameter PERIOD = 5,
    parameter WIDTH  = 2
);
  reg  clk = 1'b0;
  reg  rst = 1'b1;
  reg  en = 1'b0;
  wire pulse;

  pulse_gen #(
      .PERIOD(PERIOD),
      .WIDTH (WIDTH)
  ) dut (
      .clk_analog(clk),
      .rst(rst),
      .en(en),
      .pulse(pulse)
  );

  always #5 clk = ~clk;

  integer errors = 0;
  integer checks = 0;
  integer n;

  initial begin
    $dumpfile("tb_pulse_gen.vcd");
    $dumpvars(0, tb_pulse_gen);

    @(negedge clk);
    rst = 1'b0;
    run_enabled(3 * PERIOD + 1);  // ends mid-period
    run_disabled(4);
    run_enabled(2 * PERIOD);

    if (errors == 0) $display("PASS: PERIOD=%0d WIDTH=%0d, %0d checks", PERIOD, WIDTH, checks);
    else $display("FAIL: PERIOD=%0d WIDTH=%0d, %0d errors in %0d checks", PERIOD, WIDTH, errors,
                  checks);
    $finish;
  end

  // Raise en on a falling edge and check ncycles cycles of pulse pattern.
  task run_enabled(input integer ncycles);
    begin
      en = 1'b1;
      for (n = 0; n < ncycles; n = n + 1) begin
        #1 check(n % PERIOD < WIDTH);
        @(negedge clk);
      end
    end
  endtask

  task run_disabled(input integer ncycles);
    begin
      en = 1'b0;
      for (n = 0; n < ncycles; n = n + 1) begin
        #1 check(1'b0);
        @(negedge clk);
      end
    end
  endtask

  task check(input expected);
    begin
      checks = checks + 1;
      if (pulse !== expected) begin
        errors = errors + 1;
        $display("%0t: pulse=%b, expected %b (en=%b)", $time, pulse, expected, en);
      end
    end
  endtask

endmodule
