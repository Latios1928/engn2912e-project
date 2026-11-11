`timescale 1ns / 1ns

// Behavioral model of a synapse DAC (analog/neuron/DAC.sch); part of the
// behavioral snn_analog (snn_analog.v).
//
// weight is sign-magnitude: weight[3] is the sign (1 = negative, inhibitory)
// and weight[2:0] the magnitude, so the range is -7..+7 (1000 is -0, the same
// as 0000). On the chip the magnitude bits drive binary branches (1:2:4) and
// the sign only steers their current to the excitatory or inhibitory input,
// so no branches oppose each other.
//
// current = active ? +/- weight[2:0] * GAIN : 0, as a 16-bit two's-complement
// value. Combinational.
//
// analog/neuron/DAC.sch is still unsigned, with four branches sized 1:2:3:4.
module dac #(
    parameter GAIN = 16  // 7 * GAIN must fit in 15 bits, so GAIN <= 4681
) (
    input  wire        active,
    input  wire [ 3:0] weight,
    output wire [15:0] current
);
  localparam [15:0] G = GAIN[15:0];

  initial begin
    if (GAIN < 0 || GAIN * 7 > 32767) begin
      $error("dac: GAIN (%0d) must satisfy 0 <= 7*GAIN <= 32767", GAIN);
      $finish;
    end
  end

  wire [15:0] mag = {13'd0, weight[2:0]} * G;

  assign current = !active ? 16'd0 : weight[3] ? -mag : mag;

endmodule
