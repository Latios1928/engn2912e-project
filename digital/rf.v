// Weight register file: NUM_WORDS words of WIDTH bits, one write port, all
// words read out in parallel on weights (word w at weights[w*WIDTH +: WIDTH]).
//
// Writes happen on the rising clk edge while wren is high. Writes to
// addresses >= NUM_WORDS are ignored. There is no reset (like an SRAM), so
// every word must be written before it is used.
//
// For the SNN, word w is synapse w in the map documented in analog/mock/snn.v.
module rf #(
    parameter NUM_WORDS = 23,
    parameter WIDTH     = 3,
    parameter AW        = (NUM_WORDS > 1) ? $clog2(NUM_WORDS) : 1
) (
    input  wire                       clk,
    input  wire                       wren,
    input  wire [             AW-1:0] addr,
    input  wire [          WIDTH-1:0] data,
    output reg  [NUM_WORDS*WIDTH-1:0] weights
);
  genvar w;
  generate
    for (w = 0; w < NUM_WORDS; w = w + 1) begin : g_word
      localparam [AW-1:0] ADDR = w;
      always @(posedge clk) begin
        if (wren && addr == ADDR) weights[w*WIDTH+:WIDTH] <= data;
      end
    end
  endgenerate

endmodule
