// Digital side of the mixed-signal run: the one module built into the
// d_cosim model (snn_digital.so). Contains everything of snn_top that has no
// analog version yet:
//   - rf (weight register file), written by the test sequencer
//   - 3 pulse generators (input spikes for the input-layer DACs)
//   - snn_sequencer (stimulus and checker)
// The analog network (analog/snn/snn_analog.sch) takes w and pulse and
// returns spike.
//
// Keep everything in this one module: several d_cosim models in one netlist
// were unstable in CAD7 (see feedback.typ;
// https://github.com/mgyee/engn1600-team1).
module snn_digital #(
    parameter PULSE_PERIOD = 20,  // clk_analog cycles; 20 x 10 us = 200 us
    parameter PULSE_WIDTH  = 1,   // 10 us
    parameter SCEN_FIRST   = 0,
    parameter SCEN_LAST    = 4,
    parameter SETTLE       = 2000,  // clk cycles
    parameter RUN          = 3000   // clk cycles
) (
    input  wire        clk,         // sequencer and rf clock
    input  wire        clk_analog,  // pulse generator clock
    input  wire [ 8:0] spike,       // {output, hidden[4:0], input[2:0]}
    // rf contents (23 words x 4 bits) to the DAC weight pins, split in four
    // because ngspice's d_cosim shim reads port bits with (1 << i) and so only
    // handles ports up to 31 bits. Bit i of w_atN is w[N + i] (instantiate.py
    // names the analog nets that way).
    output wire [22:0] w_at0,
    output wire [22:0] w_at23,
    output wire [22:0] w_at46,
    output wire [22:0] w_at69,
    output wire [ 2:0] pulse,       // to the input-layer DAC enables
    output wire [ 2:0] scen,
    output wire        running,
    output wire        done
);
  wire       wren;
  wire [4:0] addr;
  wire [3:0] data;
  wire [2:0] in;
  wire       rst;
  wire [91:0] w;

  assign {w_at69, w_at46, w_at23, w_at0} = w;

  snn_sequencer #(
      .SCEN_FIRST(SCEN_FIRST),
      .SCEN_LAST (SCEN_LAST),
      .SETTLE    (SETTLE),
      .RUN       (RUN)
  ) u_seq (
      .clk(clk),
      .spike(spike),
      .weights(w),
      .wren(wren),
      .addr(addr),
      .data(data),
      .in(in),
      .rst(rst),
      .scen(scen),
      .running(running),
      .done(done)
  );

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

  // in and rst come from the clk domain; register them on clk_analog so
  // every pulse is a full PULSE_WIDTH cycles wide.
  reg [2:0] in_a;
  reg       rst_a;
  initial begin
    in_a  = 3'b000;
    rst_a = 1'b1;
  end
  always @(posedge clk_analog) begin
    in_a  <= in;
    rst_a <= rst;
  end

  genvar i;
  generate
    for (i = 0; i < 3; i = i + 1) begin : g_pulse
      pulse_gen #(
          .PERIOD(PULSE_PERIOD),
          .WIDTH (PULSE_WIDTH)
      ) u_pulse (
          .clk_analog(clk_analog),
          .rst(rst_a),
          .en(in_a[i]),
          .pulse(pulse[i])
      );
    end
  endgenerate

endmodule
