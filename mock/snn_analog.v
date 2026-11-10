`timescale 1ns / 1ns

// Behavioral stand-in for the analog 2-2-1 spiking neural network
// (analog/snn/snn_analog.sch): the same module name and ports, so
// snn_top.v works with either. The pure-digital build (mock/) compiles
// this file; the mixed-signal build (mixed/) compiles an empty module of the
// same name instead, which SpiceBind fills with the transistor-level network.
//
// Like the analog network, it has no clock or reset input. It generates its
// own clock (CLK_PERIOD ns) and releases an internal power-on reset after 2
// cycles; the neurons leak (LEAK per cycle) so that charge dies away on its
// own.
//
// pulse[i] reaches input neuron i through a DAC. Adjacent layers are fully
// connected through DACs. Every synapse has its own 4-bit weight, packed in w
// as 8 words of 4 bits:
//
//   word 0..1    pulse[i]  -> input i      (word i)
//   word 2..5    input i   -> hidden j     (word 2 + 2*j + i)
//   word 6..7    hidden j  -> output       (word 6 + j)
//
// spike = {output, hidden[1:0], input[1:0]} (active of every neuron).
module snn_analog #(
    parameter DURATION     = 4,
    parameter THRESHOLD    = 1000,
    parameter GAIN         = 16,
    parameter LEAK         = 1,
    parameter CLK_PERIOD   = 14   // ns, even; arbitrary, and unrelated to the digital clock on purpose
) (
    input  wire [8*4-1:0] w,
    input  wire [    1:0] pulse,
    output wire [    4:0] spike
);
  localparam NI = 2;  // input neurons
  localparam NH = 2;  // hidden neurons
  localparam WW = 4;  // weight width
  localparam W_IN = 0;  // word offsets into w
  localparam W_IH = NI;
  localparam W_HO = NI + NI * NH;

  // Own clock and power-on reset (the analog network has neither as a port).
  reg clk_analog;
  reg [1:0] por;
  initial begin
    clk_analog = 1'b0;
    por = 2'd0;
  end
  always #(CLK_PERIOD / 2) clk_analog = ~clk_analog;
  always @(posedge clk_analog) if (por != 2'd2) por <= por + 2'd1;
  wire rst = (por != 2'd2);  // high for the first 2 cycles

  wire [NI-1:0] act_in;
  wire [NH-1:0] act_hid;
  wire          act_out;

  assign spike = {act_out, act_hid, act_in};

  genvar i, j;
  generate
    for (i = 0; i < NI; i = i + 1) begin : g_in
      wire [15:0] cur;
      dac #(
          .GAIN(GAIN)
      ) u_dac (
          .active (pulse[i]),
          .weight (w[(W_IN+i)*WW+:WW]),
          .current(cur)
      );
      neuron #(
          .INDEGREE (1),
          .LEAK     (LEAK),
          .DURATION (DURATION),
          .THRESHOLD(THRESHOLD)
      ) u_neuron (
          .clk_analog(clk_analog),
          .rst(rst),
          .currents(cur),
          .active(act_in[i])
      );
    end

    for (j = 0; j < NH; j = j + 1) begin : g_hid
      wire [NI*16-1:0] cur;
      for (i = 0; i < NI; i = i + 1) begin : g_syn
        dac #(
            .GAIN(GAIN)
        ) u_dac (
            .active (act_in[i]),
            .weight (w[(W_IH+NI*j+i)*WW+:WW]),
            .current(cur[i*16+:16])
        );
      end
      neuron #(
          .INDEGREE (NI),
          .LEAK     (LEAK),
          .DURATION (DURATION),
          .THRESHOLD(THRESHOLD)
      ) u_neuron (
          .clk_analog(clk_analog),
          .rst(rst),
          .currents(cur),
          .active(act_hid[j])
      );
    end

    if (1) begin : g_out
      wire [NH*16-1:0] cur;
      for (j = 0; j < NH; j = j + 1) begin : g_syn
        dac #(
            .GAIN(GAIN)
        ) u_dac (
            .active (act_hid[j]),
            .weight (w[(W_HO+j)*WW+:WW]),
            .current(cur[j*16+:16])
        );
      end
      neuron #(
          .INDEGREE (NH),
          .LEAK     (LEAK),
          .DURATION (DURATION),
          .THRESHOLD(THRESHOLD)
      ) u_neuron (
          .clk_analog(clk_analog),
          .rst(rst),
          .currents(cur),
          .active(act_out)
      );
    end
  endgenerate

endmodule
