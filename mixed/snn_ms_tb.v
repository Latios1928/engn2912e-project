// Mixed-signal testbench: snn_top runs in Icarus, and its snn_analog is the
// analog macro SNN_signed in ngspice (snn_ms_tb.spice) through SpiceBind.
//
// Scenarios 1-5 match ../mock/tb_snn_top.v; 1-8 match the analog-only runner
// analog/testbenches/snn/run_snn_signed.py:
//   1. all weights max, in = 00             -> nothing fires
//   2. only pulse->input weights, in = 01   -> only input neuron 0
//   3. one path in1 -> hid1 -> out, in = 11 -> input 1, hidden 1, output
//   4. as 3 but hid1 -> out weight 0        -> input 1, hidden 1 only
//   5. as 3 plus in0 -> hid1 at max, inhibitory, in = 11: the two inputs fire
//      together and cancel at hid1          -> inputs 0 and 1 only
//   6. pulse 0 -> input 0 at max, inhibitory, in = 01: the input neurons have
//      no inhibitory synapse, so an inhibitory weight is off -> nothing fires
//   7. both inputs drive both hidden neurons' paths (in0 -> hid0, in1 -> hid1),
//      hid0 -> out at max inhibitory against hid1 -> out at max, in = 11
//                                           -> inputs and hidden, not output
//   8. control for 7: hid0 -> out = 0      -> all five fire
// Scenario 7 is a tie (+15 against -15); post-layout Monte Carlo passes 94 / 100
// chips on it (analog/testbenches/snn/results/snn_signed_tb__pex__mc100.md).
// Synapse k has magnitude w[4k+3:4k] (max 15) and sign s[k] (1 = inhibitory).
// The pulse timing (200, 10) is written through regs at the start. The
// network has no reset pin, so each run is preceded by SETTLE us with in = 0.
`timescale 1ns / 1ns

module snn_ms_tb #(
    parameter SCEN_FIRST = 1,
    parameter SCEN_LAST = 8,
    parameter SETTLE = 4000,  // us
    parameter RUN = 3000  // us
);
  localparam [3:0] IDLE = 4'hF;
  localparam [3:0] A_SIGN_LO = 4'd8, A_SIGN_HI = 4'd9;
  localparam [3:0] A_PER_LO = 4'd10, A_PER_HI = 4'd11;
  localparam [3:0] A_WID_LO = 4'd12, A_WID_HI = 4'd13;
  localparam [3:0] MAX = 4'hF;

  reg        clk = 1'b0;  // 1 us
  reg        rst = 1'b1;
  reg  [3:0] addr = IDLE;
  reg  [3:0] data = 0;
  reg  [1:0] in = 0;
  wire [4:0] spike;

  always #500 clk = ~clk;

  snn_top dut (
      .clk (clk),
      .rst (rst),
      .data(data),
      .addr(addr),
      .in  (in),
      .out (spike)
  );

  wire [1:0] pulse = dut.pulse;  // for the waveform

  integer scen = 0;  // for the waveform
  reg [4:0] seen = 0;
  reg counting = 1'b0;
  time t_run = 0;
  integer k;
  always @(posedge spike[0] or posedge spike[1] or posedge spike[2] or posedge spike[3]
           or posedge spike[4])
    if (counting)
      for (k = 0; k < 5; k = k + 1)
        if (spike[k] === 1'b1 && !seen[k]) begin
          seen[k] = 1'b1;
          $display("snn_ms_tb: scenario %0d: spike[%0d] first at %0d us", scen, k,
                   integer'(($time - t_run) / 1000));
        end

  integer errors = 0;
  integer i;
  reg [31:0] ws;
  reg [7:0] ss;

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

  task load;
    begin
      for (i = 0; i < 8; i = i + 1) write_reg(i[3:0], ws[i*4+:4]);
      write_reg(A_SIGN_LO, ss[3:0]);
      write_reg(A_SIGN_HI, ss[7:4]);
    end
  endtask

  // One run: load weights and signs, settle with in = 0, then in_v for RUN us
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

    // Pulse timing: write the reset values through the interface
    write_reg(A_PER_LO, 4'h8);  // period 200 = 8'hC8
    write_reg(A_PER_HI, 4'hC);
    write_reg(A_WID_LO, 4'hA);  // width 10 = 8'h0A
    write_reg(A_WID_HI, 4'h0);
    if (dut.u_digital.period !== 8'd200 || dut.u_digital.width !== 8'd10) begin
      errors = errors + 1;
      $display("snn_ms_tb: FAIL setup: period %0d width %0d", dut.u_digital.period,
               dut.u_digital.width);
    end

    for (scen = SCEN_FIRST; scen <= SCEN_LAST; scen = scen + 1) begin
      ss = 0;
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
          ws[(2+2*1+0)*4+:4] = MAX;  // input 0 -> hidden 1, inhibitory:
          ss[2+2*1+0] = 1'b1;
          ws[(2+2*1+1)*4+:4] = MAX;  // input 1 -> hidden 1
          ws[(6+1)*4+:4] = MAX;  // hidden 1 -> output
          check_run(2'b11, 5'b0_00_11);
        end
        6: begin
          ws = 0;
          ws[0*4+:4] = MAX;  // pulse 0 -> input 0, inhibitory
          ss[0] = 1'b1;
          check_run(2'b01, 5'b0_00_00);
        end
        7, 8: begin
          ws = 0;
          ws[0*4+:4] = MAX;  // pulse 0 -> input 0
          ws[1*4+:4] = MAX;  // pulse 1 -> input 1
          ws[(2+2*0+0)*4+:4] = MAX;  // input 0 -> hidden 0
          ws[(2+2*1+1)*4+:4] = MAX;  // input 1 -> hidden 1
          ws[(6+0)*4+:4] = (scen == 7) ? MAX : 4'h0;  // hidden 0 -> output,
          ss[6+0] = (scen == 7);  // inhibitory in 7
          ws[(6+1)*4+:4] = MAX;  // hidden 1 -> output
          check_run(2'b11, (scen == 7) ? 5'b0_11_11 : 5'b1_11_11);
        end
        default: ;
      endcase
    end

    if (errors == 0) $display("snn_ms_tb: PASS, all scenarios");
    else $display("snn_ms_tb: FAIL, %0d scenarios failed", errors);
    $finish;
  end

endmodule
