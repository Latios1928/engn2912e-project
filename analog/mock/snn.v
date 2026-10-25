// Behavioral mock of the 3-5-1 spiking neural network (will become analog).
//
// in[i] enables pulse generator i, whose pulses reach input neuron i through
// a DAC. Adjacent layers are fully connected through DACs. Every synapse has
// its own 3-bit weight, packed in weights as 23 words of 3 bits:
//
//   word 0..2    pulse[i]  -> input i      (word i)
//   word 3..17   input i   -> hidden j     (word 3 + 3*j + i)
//   word 18..22  hidden j  -> output       (word 18 + j)
//
// out = {output, hidden[4:0], input[2:0]} (active of every neuron).
module snn #(
    parameter DURATION     = 4,
    parameter THRESHOLD    = 1000,
    parameter GAIN         = 16,
    parameter PULSE_PERIOD = 16,
    parameter PULSE_WIDTH  = 2
) (
    input  wire            clk_analog,
    input  wire            rst,         // synchronous, active high
    input  wire [23*3-1:0] weights,
    input  wire [     2:0] in,
    output wire [     8:0] out
);
  localparam NI = 3;  // input neurons
  localparam NH = 5;  // hidden neurons
  localparam W = 3;  // weight width
  localparam W_IN = 0;  // word offsets into weights
  localparam W_IH = NI;
  localparam W_HO = NI + NI * NH;

  wire [NI-1:0] pulse;
  wire [NI-1:0] act_in;
  wire [NH-1:0] act_hid;
  wire          act_out;

  assign out = {act_out, act_hid, act_in};

  genvar i, j;
  generate
    for (i = 0; i < NI; i = i + 1) begin : g_in
      wire [15:0] cur;
      pulse_gen #(
          .PERIOD(PULSE_PERIOD),
          .WIDTH (PULSE_WIDTH)
      ) u_pulse (
          .clk_analog(clk_analog),
          .rst(rst),
          .en(in[i]),
          .pulse(pulse[i])
      );
      dac #(
          .GAIN(GAIN)
      ) u_dac (
          .active (pulse[i]),
          .weight (weights[(W_IN+i)*W+:W]),
          .current(cur)
      );
      neuron #(
          .INDEGREE (1),
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
            .weight (weights[(W_IH+NI*j+i)*W+:W]),
            .current(cur[i*16+:16])
        );
      end
      neuron #(
          .INDEGREE (NI),
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
            .weight (weights[(W_HO+j)*W+:W]),
            .current(cur[j*16+:16])
        );
      end
      neuron #(
          .INDEGREE (NH),
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
