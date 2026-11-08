// Test sequencer and checker for the mixed-signal run (synthesizable style:
// clocked by clk, no # delays, so Verilator can build it into the d_cosim
// model). It replays the scenarios of ../tb_snn_top.v on the analog network:
//
//   0. rf readback: word w = w mod 16, plus an ignored write to address 31
//   1. all weights max, in = 000           -> nothing fires
//   2. only pulse->input weights, in = 101 -> only input neurons 0 and 2
//   3. one path in1 -> hid2 -> out, in = 111 -> input 1, hidden 2, output
//   4. as 3 but hid2 -> out weight 0       -> input 1, hidden 2 only
//
// For each scenario 1-4 it writes the 23 weight words through
// wren/addr/data, waits SETTLE cycles with in = 0 so the analog state decays
// (the analog network has no reset pin), then applies in for RUN cycles while
// ORing spike into seen, and compares seen with the expected set.
// "Max" weight is code 4'hF. Results are printed with $display, which shows
// up in the ngspice log. Scenarios SCEN_FIRST..SCEN_LAST are run.
module snn_sequencer #(
    parameter SCEN_FIRST = 0,
    parameter SCEN_LAST  = 4,
    parameter SETTLE     = 2000,  // clk cycles with in = 0 before each run
    parameter RUN        = 3000   // clk cycles with in applied
) (
    input  wire        clk,
    input  wire [ 8:0] spike,    // {output, hidden[4:0], input[2:0]}, from the analog network
    input  wire [91:0] weights,  // rf contents, for the readback check
    output reg         wren,
    output reg  [ 4:0] addr,
    output reg  [ 3:0] data,
    output reg  [ 2:0] in,
    output reg         rst,      // to the pulse generators
    output reg  [ 2:0] scen,     // scenario being run (for the waveform)
    output reg         running,  // high while in is applied and spikes are counted
    output reg         done
);
  localparam NWORDS = 23;
  localparam [3:0] MAX = 4'hF;

  // Word indices (see ../analog/mock/snn.v).
  localparam W_PULSE = 0;  // + i
  localparam W_IH = 3;  // + 3*j + i
  localparam W_HO = 18;  // + j

  localparam [2:0] S_LOAD = 3'd0, S_EXTRA = 3'd1, S_SETTLE = 3'd2, S_RUN = 3'd3, S_CHECK = 3'd4,
      S_NEXT = 3'd5, S_DONE = 3'd6;

  reg [2:0] state;
  reg [5:0] word;  // word being written; also the 2-cycle write phase in bit 0 of phase
  reg phase;
  reg [31:0] cnt;
  reg [8:0] seen;
  reg [91:0] ws;
  reg [2:0] in_v;
  reg [8:0] expected;
  reg [7:0] errors;
  reg [7:0] checks;

  // Weight set, input and expected firing set of each scenario.
  function [91:0] scen_weights(input [2:0] s);
    integer w;
    begin
      scen_weights = 0;
      case (s)
        3'd0: for (w = 0; w < NWORDS; w = w + 1) scen_weights[w*4+:4] = w[3:0];
        3'd1: scen_weights = {92{1'b1}};
        3'd2: for (w = 0; w < 3; w = w + 1) scen_weights[(W_PULSE+w)*4+:4] = MAX;
        3'd3, 3'd4: begin
          scen_weights[(W_PULSE+1)*4+:4] = MAX;
          scen_weights[(W_IH+3*2+1)*4+:4] = MAX;
          scen_weights[(W_HO+2)*4+:4] = (s == 3'd3) ? MAX : 4'h0;
        end
        default: scen_weights = 0;
      endcase
    end
  endfunction

  function [2:0] scen_in(input [2:0] s);
    case (s)
      3'd2: scen_in = 3'b101;
      3'd3, 3'd4: scen_in = 3'b111;
      default: scen_in = 3'b000;
    endcase
  endfunction

  function [8:0] scen_expected(input [2:0] s);
    case (s)
      3'd2: scen_expected = 9'b0_00000_101;
      3'd3: scen_expected = 9'b1_00100_010;
      3'd4: scen_expected = 9'b0_00100_010;
      default: scen_expected = 9'b0;
    endcase
  endfunction

  initial begin
    state = S_LOAD;
    scen = SCEN_FIRST[2:0];
    word = 0;
    phase = 0;
    cnt = 0;
    seen = 0;
    wren = 0;
    addr = 0;
    data = 0;
    in = 0;
    rst = 1;
    running = 0;
    done = 0;
    errors = 0;
    checks = 0;
    ws = scen_weights(SCEN_FIRST[2:0]);
    in_v = scen_in(SCEN_FIRST[2:0]);
    expected = scen_expected(SCEN_FIRST[2:0]);
  end

  always @(posedge clk) begin
    case (state)
      // One word every two cycles: wren high in phase 0, low in phase 1.
      S_LOAD: begin
        if (!phase) begin
          wren <= 1'b1;
          addr <= word[4:0];
          data <= ws[word*4+:4];
          phase <= 1'b1;
        end else begin
          wren <= 1'b0;
          phase <= 1'b0;
          if (word == NWORDS - 1) begin
            word <= 0;
            state <= (scen == 3'd0) ? S_EXTRA : S_SETTLE;
          end else word <= word + 1'b1;
        end
        cnt <= 0;
      end

      // Scenario 0 only: a write to an address past the last word must be ignored.
      S_EXTRA: begin
        if (!phase) begin
          wren <= 1'b1;
          addr <= 5'd31;
          data <= MAX;
          phase <= 1'b1;
        end else begin
          wren <= 1'b0;
          phase <= 1'b0;
          state <= S_CHECK;
        end
      end

      S_SETTLE: begin
        in <= 3'b000;
        rst <= 1'b1;
        if (cnt == SETTLE - 1) begin
          cnt <= 0;
          seen <= 0;
          rst <= 1'b0;
          in <= in_v;
          running <= 1'b1;
          state <= S_RUN;
          $display("snn_sequencer: scenario %0d running (in = %b)", scen, in_v);
        end else cnt <= cnt + 1;
      end

      S_RUN: begin
        seen <= seen | spike;
        if (cnt == RUN - 1) begin
          running <= 1'b0;
          in <= 3'b000;
          state <= S_CHECK;
        end else cnt <= cnt + 1;
      end

      S_CHECK: begin
        checks <= checks + 1'b1;
        if (scen == 3'd0) begin
          if (weights !== ws) begin
            errors <= errors + 1'b1;
            $display("snn_sequencer: FAIL scenario 0 (rf readback): weights=%h, expected %h",
                     weights, ws);
          end else $display("snn_sequencer: PASS scenario 0 (rf readback)");
        end else if (seen !== expected) begin
          errors <= errors + 1'b1;
          $display("snn_sequencer: FAIL scenario %0d: fired %b, expected %b ({out, hid[4:0], in[2:0]})",
                   scen, seen, expected);
        end else $display("snn_sequencer: PASS scenario %0d: fired %b", scen, seen);
        state <= S_NEXT;
      end

      S_NEXT: begin
        if (scen == SCEN_LAST[2:0]) begin
          state <= S_DONE;
          if (errors == 0) $display("snn_sequencer: PASS, %0d checks", checks);
          else $display("snn_sequencer: FAIL, %0d errors in %0d checks", errors, checks);
        end else begin
          scen <= scen + 1'b1;
          ws <= scen_weights(scen + 1'b1);
          in_v <= scen_in(scen + 1'b1);
          expected <= scen_expected(scen + 1'b1);
          state <= S_LOAD;
        end
      end

      default: begin
        done <= 1'b1;
        in <= 3'b000;
      end
    endcase
  end

endmodule
