// Mixed-signal testbench for the addr4_trim interface: the chip top
// (snn_top_v2.v, with snn_digital_v2: regs_v2 and pulse_gen_v2) runs in Icarus;
// inside it, snn_analog_v2 is the transistor-level SPICE side in ngspice through
// SpiceBind (snn_ms_tb_v2.sch): trim_iref.va -> bias_cell -> 2-2-1 network.
// Same role as ../snn_ms_tb.v (unchanged).
//
// Scenarios 1-5 are those of ../snn_ms_tb.v, at the nominal trim code 9:
//   1. all weights max, in = 00             -> nothing fires
//   2. only pulse->input weights, in = 01   -> only input neuron 0
//   3. one path in1 -> hid1 -> out, in = 11 -> input 1, hidden 1, output
//   4. as 3 but hid1 -> out weight 0        -> input 1, hidden 1 only
//   5. as 3 plus in0 -> hid1 at -max, in = 11: the two inputs fire together
//      and cancel at hid1                   -> inputs 0 and 1 only
// Scenario 6 checks that the trim register reaches the analog side: the setup of
// scenario 2 (input neuron 0 driven by its pulses) is run once per code in
// TRIM_CODES. For each code it prints the time of the first spike and the number
// of spikes of input neuron 0 in the run. PASS if the neuron fires at every code
// and the spike count or first-spike time differs between the first two codes.
// The trim register is restored to 9 afterwards.
//
// Every write follows the protocol of regs_v2.v: data changes only while addr is
// IDLE (4'hF), then addr selects the register for one clk cycle and returns to
// IDLE. The pulse timing registers (8-11) are written once at the start with the
// reset values (200, 10), so their write path to the analog side is exercised.
//
// The analog network has no reset pin, so each run is preceded by SETTLE us
// with in = 0 (this also lets the biases settle after a trim change).
//
// A 'bad chip' is a SPICE parameter (p_perr in snn_ms_tb_v2.sch, the Makefile's
// PERR): run scenario 6 with PERR=0.82 and TRIM_CODES including 9 and 13 to see
// the trim bring it back to the typical chip at code 9.
`timescale 1ns / 1ns

module snn_ms_tb_v2 #(
    parameter SCEN_FIRST = 1,
    parameter SCEN_LAST = 6,
    parameter SETTLE = 2000,  // us
    parameter RUN = 3000,  // us
    // Scenario 6: up to 4 trim codes, run in order TRIM_CODES[3:0],
    // TRIM_CODES[7:4], ...; N_TRIM of them are used.
    parameter [15:0] TRIM_CODES = {4'd0, 4'd0, 4'd15, 4'd9},
    parameter N_TRIM = 2
);
  localparam [3:0] IDLE = 4'hF;
  localparam [3:0] A_PER_LO = 4'd8, A_PER_HI = 4'd9;
  localparam [3:0] A_WID_LO = 4'd10, A_WID_HI = 4'd11;
  localparam [3:0] A_TRIM = 4'd12;
  localparam [3:0] TRIM_NOM = 4'd9;
  // Weights are sign-magnitude: MAX is +7, NEG_MAX is -7.
  localparam [3:0] MAX = 4'h7;
  localparam [3:0] NEG_MAX = 4'hF;

  reg        clk = 1'b0;  // 1 us
  reg        rst = 1'b1;
  reg  [3:0] addr = IDLE;
  reg  [3:0] data = 0;
  reg  [1:0] in = 0;
  wire [4:0] spike;

  always #500 clk = ~clk;

  snn_top_v2 dut (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .in(in),
      .out(spike)
  );

  wire [1:0] pulse = dut.pulse;  // for the waveform
  wire [3:0] trim = dut.trim;

  integer scen = 0;  // for the waveform
  reg [4:0] seen = 0;
  reg counting = 1'b0;
  time t_run = 0;
  integer t_first[0:4];  // us after the run start, -1 = no spike
  integer n_spk[0:4];
  integer k;
  always @(posedge spike[0] or posedge spike[1] or posedge spike[2] or posedge spike[3]
           or posedge spike[4])
    if (counting)
      for (k = 0; k < 5; k = k + 1)
        if (spike[k] === 1'b1 && !seen[k]) begin
          seen[k] = 1'b1;
          t_first[k] = ($time - t_run) / 1000;
          $display("snn_ms_tb_v2: scenario %0d: spike[%0d] first at %0d us", scen, k, t_first[k]);
        end
  // Spike counts: rising edges of each neuron's spike during the run
  genvar g;
  generate
    for (g = 0; g < 5; g = g + 1) begin : g_cnt
      always @(posedge spike[g]) if (counting) n_spk[g] = n_spk[g] + 1;
    end
  endgenerate

  integer errors = 0;
  integer i;
  reg [31:0] ws;

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
    for (i = 0; i < 8; i = i + 1) write_reg(i[3:0], ws[i*4+:4]);
  endtask

  // One run: load weights, settle with in = 0, then RUN us with in = in_v
  task run(input [1:0] in_v);
    begin
      load;
      in = 2'b00;
      #(SETTLE * 1000);
      in = in_v;
      seen = 0;
      for (i = 0; i < 5; i = i + 1) begin
        t_first[i] = -1;
        n_spk[i] = 0;
      end
      t_run = $time;
      counting = 1'b1;
      #(RUN * 1000);
      counting = 1'b0;
      in = 2'b00;
    end
  endtask

  task check_run(input [1:0] in_v, input [4:0] expected);
    begin
      run(in_v);
      if (seen === expected) $display("snn_ms_tb_v2: PASS scenario %0d: fired %b", scen, seen);
      else begin
        errors = errors + 1;
        $display("snn_ms_tb_v2: FAIL scenario %0d: fired %b, expected %b", scen, seen, expected);
      end
    end
  endtask

  // Scenario 6
  integer j, ok6;
  reg [3:0] code;
  integer first0[0:3];
  integer count0[0:3];

  initial begin
    $dumpfile("snn_ms_tb_v2_digital.vcd");
    $dumpvars(0, snn_ms_tb_v2);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // Pulse timing: write the reset values through the interface
    write_reg(A_PER_LO, 4'h8);  // period 200 = 8'hC8
    write_reg(A_PER_HI, 4'hC);
    write_reg(A_WID_LO, 4'hA);  // width 10 = 8'h0A
    write_reg(A_WID_HI, 4'h0);
    write_reg(A_TRIM, TRIM_NOM);
    if (dut.u_digital.period !== 8'd200 || dut.u_digital.width !== 8'd10 || trim !== TRIM_NOM) begin
      errors = errors + 1;
      $display("snn_ms_tb_v2: FAIL setup: period %0d width %0d trim %0d", dut.u_digital.period,
               dut.u_digital.width, trim);
    end

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
        6: begin
          ws = 0;
          ws[0*4+:4] = MAX;  // pulse 0 -> input 0
          ok6 = 1;
          for (j = 0; j < N_TRIM; j = j + 1) begin
            code = TRIM_CODES[j*4+:4];
            write_reg(A_TRIM, code);
            run(2'b01);
            first0[j] = t_first[0];
            count0[j] = n_spk[0];
            $display("snn_ms_tb_v2: scenario 6: trim %0d: input 0 first spike %0d us, %0d spikes in %0d us",
                     code, first0[j], count0[j], RUN);
            if (count0[j] == 0) ok6 = 0;
          end
          if (N_TRIM >= 2 && count0[0] == count0[1] && first0[0] == first0[1]) ok6 = 0;
          write_reg(A_TRIM, TRIM_NOM);
          if (ok6) $display("snn_ms_tb_v2: PASS scenario 6: trim changes the neuron's response");
          else begin
            errors = errors + 1;
            $display("snn_ms_tb_v2: FAIL scenario 6: no firing at some code, or no effect of trim");
          end
        end
        default: ;
      endcase

    if (errors == 0) $display("snn_ms_tb_v2: PASS, all scenarios");
    else $display("snn_ms_tb_v2: FAIL, %0d scenarios failed", errors);
    $finish;
  end

endmodule
