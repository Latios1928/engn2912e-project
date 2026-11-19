`timescale 1ns / 1ns

// Behavioral model of a signed synapse DAC (analog/DAC/DAC.sch); part of the
// behavioral snn_analog (snn_analog.v).
//
// weight is a 4-bit magnitude (0-15; binary branches 1:2:4:8 on the chip) and
// sign steers that current to the excitatory (0) or inhibitory (1) input.
//
// current = active ? +/- weight * GAIN : 0, as a 16-bit two's-complement
// value. Combinational.
module dac #(
    parameter GAIN = 16  // 15 * GAIN must fit in 15 bits, so GAIN <= 2184
) (
    input  wire        active,
    input  wire [ 3:0] weight,
    input  wire        sign,
    output wire [15:0] current
);
  localparam [15:0] G = GAIN[15:0];

  initial begin
    if (GAIN < 0 || GAIN * 15 > 32767) begin
      $error("dac: GAIN (%0d) must satisfy 0 <= 15*GAIN <= 32767", GAIN);
      $finish;
    end
  end

  wire [15:0] mag = {12'd0, weight} * G;

  assign current = !active ? 16'd0 : sign ? -mag : mag;

endmodule
