// Mixed-signal testbench: the chip top (snn_top.v, with digital/snn_digital.v: rf and pulse_gen)
// runs in Icarus; the 2-2-1 network snn_analog inside it is transistor-level in
// ngspice through SpiceBind (see ../analog/snn/snn_analog.v).
// Same scenarios as ../mock/tb_snn_top.v:
//   1. all weights max, in = 00             -> nothing fires
//   2. only pulse->input weights, in = 01   -> only input neuron 0
//   3. one path in1 -> hid1 -> out, in = 11 -> input 1, hidden 1, output
//   4. as 3 but hid1 -> out weight 0        -> input 1, hidden 1 only
//   5. as 3 plus in0 -> hid1 at -max, in = 11: the two inputs fire together
//      and cancel at hid1                   -> inputs 0 and 1 only
// The analog network has no reset pin, so each run is preceded by SETTLE us
// with in = 0. Prints PASS/FAIL and the time of each neuron's first spike.
`timescale 1ns / 1ns

module snn_ms_tb #(
    parameter SCEN_FIRST = 1,
    parameter SCEN_LAST  = 5,
    parameter SETTLE     = 2000,  // us
    parameter RUN        = 3000   // us
);
  // Weights are sign-magnitude: MAX is +7, NEG_MAX is -7.
  localparam [3:0] MAX = 4'h7;
  localparam [3:0] NEG_MAX = 4'hF;

  reg        clk = 1'b0;  // 1 us
  reg        rst = 1'b1;
  reg        wren = 1'b0;
  reg  [2:0] addr = 0;
  reg  [3:0] data = 0;
  reg  [1:0] in = 0;
  wire [4:0] spike;

  always #500 clk = ~clk;

  snn_top #(
      .PULSE_PERIOD(200),  // 200 us
      .PULSE_WIDTH (10)    // 10 us
  ) dut (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .wren(wren),
      .in(in),
      .out(spike)
  );

  wire [1:0] pulse = dut.pulse;  // for the waveform

  integer scen = 0;  // for the waveform
  reg [4:0] seen = 0;
  reg counting = 1'b0;
  time t_run = 0;
  integer k;
  always @(spike)
    if (counting)
      for (k = 0; k < 5; k = k + 1)
        if (spike[k] === 1'b1 && !seen[k]) begin
          seen[k] = 1'b1;
          $display("snn_ms_tb: scenario %0d: spike[%0d] first at %0d us", scen, k,
                   ($time - t_run) / 1000);
        end

  integer errors = 0;
  integer i;
  reg [31:0] ws;

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

  task load;
    for (i = 0; i < 8; i = i + 1) write_word(i[2:0], ws[i*4+:4]);
  endtask

  task check_run(input [1:0] in_v, input [4:0] expected);
    begin
      load;
      in = 2'b00;
      #(SETTLE * 1000);
      in = in_v;
      seen = 0;
      t_run = $time;
      counting = 1'b1;
      #(RUN * 1000);
      counting = 1'b0;
      in = 2'b00;
      if (seen === expected) $display("snn_ms_tb: PASS scenario %0d: fired %b", scen, seen);
      else begin
        errors = errors + 1;
        $display("snn_ms_tb: FAIL scenario %0d: fired %b, expected %b", scen, seen, expected);
      end
    end
  endtask

  initial begin
    $dumpfile("snn_ms_tb_digital.vcd");
    $dumpvars(0, snn_ms_tb);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    for (scen = SCEN_FIRST; scen <= SCEN_LAST; scen = scen + 1)
      case (scen)
        1: begin
          ws = {8{MAX}};
          check_run(2'b00, 5'b0_00_00);
        end
        2: begin
          ws = 0;
          for (i = 0; i < 2; i = i + 1) ws[i*4+:4] = MAX;
          check_run(2'b01, 5'b0_00_01);
        end
        3, 4: begin
          ws = 0;
          ws[1*4+:4] = MAX;  // pulse 1 -> input 1
          ws[(2+2*1+1)*4+:4] = MAX;  // input 1 -> hidden 1
          ws[(6+1)*4+:4] = (scen == 3) ? MAX : 4'h0;  // hidden 1 -> output
          check_run(2'b11, (scen == 3) ? 5'b1_10_10 : 5'b0_10_10);
        end
        5: begin
          ws = 0;
          ws[0*4+:4] = MAX;  // pulse 0 -> input 0
          ws[1*4+:4] = MAX;  // pulse 1 -> input 1
          ws[(2+2*1+0)*4+:4] = NEG_MAX;  // input 0 -> hidden 1, inhibitory
          ws[(2+2*1+1)*4+:4] = MAX;  // input 1 -> hidden 1
          ws[(6+1)*4+:4] = MAX;  // hidden 1 -> output
          check_run(2'b11, 5'b0_00_11);
        end
        default: ;
      endcase

    if (errors == 0) $display("snn_ms_tb: PASS, all scenarios");
    else $display("snn_ms_tb: FAIL, %0d scenarios failed", errors);
    $finish;
  end

endmodule
