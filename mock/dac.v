`timescale 1ns / 1ns

// Behavioral mock of a synapse DAC (will become analog).
//
// current = active ? weight * GAIN : 0. Combinational.
//
// weight is a 4-bit binary code (branch weights 1:2:4:8). Note that
// analog/neuron/DAC.sch is still sized 1:2:3:4; codes that use w[2] or w[3]
// give less current there until it is resized.
module dac #(
    parameter GAIN = 16  // weight * GAIN must fit in 16 bits, so GAIN <= 4369
) (
    input  wire        active,
    input  wire [ 3:0] weight,
    output wire [15:0] current
);
  localparam [15:0] G = GAIN[15:0];

  initial begin
    if (GAIN < 0 || GAIN * 15 > 65535) begin
      $error("dac: GAIN (%0d) must satisfy 0 <= 15*GAIN <= 65535", GAIN);
      $finish;
    end
  end

  assign current = active ? {12'd0, weight} * G : 16'd0;

endmodule
