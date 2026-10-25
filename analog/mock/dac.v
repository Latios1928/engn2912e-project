// Behavioral mock of a synapse DAC (will become analog).
//
// current = active ? weight * GAIN : 0. Combinational.
module dac #(
    parameter GAIN = 16  // weight * GAIN must fit in 16 bits, so GAIN <= 9362
) (
    input  wire        active,
    input  wire [ 2:0] weight,
    output wire [15:0] current
);
  localparam [15:0] G = GAIN[15:0];

  initial begin
    if (GAIN < 0 || GAIN * 7 > 65535) begin
      $error("dac: GAIN (%0d) must satisfy 0 <= 7*GAIN <= 65535", GAIN);
      $finish;
    end
  end

  assign current = active ? {13'd0, weight} * G : 16'd0;

endmodule
