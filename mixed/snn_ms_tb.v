// Mixed-signal testbench: rf and the pulse generators run here in Icarus; the
// 3-5-1 network (snn_analog) is transistor-level in ngspice through SpiceBind.
// Same scenarios as ../tb_snn_top.v:
//   1. all weights max, in = 000             -> nothing fires
//   2. only pulse->input weights, in = 101   -> only input neurons 0 and 2
//   3. one path in1 -> hid2 -> out, in = 111 -> input 1, hidden 2, output
//   4. as 3 but hid2 -> out weight 0         -> input 1, hidden 2 only
// The analog network has no reset pin, so each run is preceded by SETTLE us
// with in = 0. Prints PASS/FAIL and the time of each neuron's first spike.
`timescale 1ns / 1ns

// Implemented in SPICE (analog/snn/snn_analog.sch); SpiceBind drives its ports.
module snn_analog (
    input  wire [91:0] w,
    input  wire [ 2:0] pulse,
    output wire [ 8:0] spike
);
endmodule

module snn_ms_tb #(
    parameter SCEN_FIRST = 1,
    parameter SCEN_LAST  = 4,
    parameter SETTLE     = 2000,  // us
    parameter RUN        = 3000   // us
);
  localparam [3:0] MAX = 4'hF;

  reg        clk = 1'b0;         // 1 us, rf
  reg        clk_analog = 1'b0;  // 10 us, pulse generators
  reg        rst = 1'b1;
  reg        wren = 1'b0;
  reg  [4:0] addr = 0;
  reg  [3:0] data = 0;
  reg  [2:0] in = 0;
  wire [91:0] w;
  wire [ 2:0] pulse;
  wire [ 8:0] spike;

  always #500 clk = ~clk;
  always #5000 clk_analog = ~clk_analog;

  rf #(
      .NUM_WORDS(23),
      .WIDTH(4),
      .AW(5)
  ) u_rf (
      .clk(clk),
      .wren(wren),
      .addr(addr),
      .data(data),
      .weights(w)
  );

  genvar g;
  generate
    for (g = 0; g < 3; g = g + 1) begin : g_pulse
      pulse_gen #(
          .PERIOD(20),  // 200 us
          .WIDTH (1)    // 10 us
      ) u_pulse (
          .clk_analog(clk_analog),
          .rst(rst),
          .en(in[g]),
          .pulse(pulse[g])
      );
    end
  endgenerate

  snn_analog ana (
      .w(w),
      .pulse(pulse),
      .spike(spike)
  );

  integer scen = 0;  // for the waveform
  reg [8:0] seen = 0;
  reg counting = 1'b0;
  time t_run = 0;
  integer k;
  always @(spike)
    if (counting)
      for (k = 0; k < 9; k = k + 1)
        if (spike[k] === 1'b1 && !seen[k]) begin
          seen[k] = 1'b1;
          $display("snn_ms_tb: scenario %0d: spike[%0d] first at %0d us", scen, k,
                   ($time - t_run) / 1000);
        end

  integer errors = 0;
  integer i;
  reg [91:0] ws;

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

  task load;
    for (i = 0; i < 23; i = i + 1) write_word(i[4:0], ws[i*4+:4]);
  endtask

  task check_run(input [2:0] in_v, input [8:0] expected);
    begin
      load;
      in = 3'b000;
      rst = 1'b1;
      #(SETTLE * 1000);
      // Just after a rising edge: pulse_gen's output is combinational in en,
      // so raising en mid-cycle would make the first pulse too short.
      @(posedge clk_analog);
      #1;
      rst = 1'b0;
      in = in_v;
      seen = 0;
      t_run = $time;
      counting = 1'b1;
      #(RUN * 1000);
      counting = 1'b0;
      in = 3'b000;
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

    for (scen = SCEN_FIRST; scen <= SCEN_LAST; scen = scen + 1)
      case (scen)
        1: begin
          ws = {92{1'b1}};
          check_run(3'b000, 9'b0_00000_000);
        end
        2: begin
          ws = 0;
          for (i = 0; i < 3; i = i + 1) ws[i*4+:4] = MAX;
          check_run(3'b101, 9'b0_00000_101);
        end
        3, 4: begin
          ws = 0;
          ws[1*4+:4] = MAX;  // pulse 1 -> input 1
          ws[(3+3*2+1)*4+:4] = MAX;  // input 1 -> hidden 2
          ws[(18+2)*4+:4] = (scen == 3) ? MAX : 4'h0;  // hidden 2 -> output
          check_run(3'b111, (scen == 3) ? 9'b1_00100_010 : 9'b0_00100_010);
        end
        default: ;
      endcase

    if (errors == 0) $display("snn_ms_tb: PASS, all scenarios");
    else $display("snn_ms_tb: FAIL, %0d scenarios failed", errors);
    $finish;
  end

endmodule
