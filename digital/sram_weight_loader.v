// SRAM-backed weight configuration loader.
//
// On a `start` pulse, sequentially reads NUM_WEIGHTS words out of a
// single-port synchronous SRAM (1-cycle read latency: address presented
// at cycle i is read back at cycle i+1) and captures each word into the
// flattened `weights` register file. `done` pulses for one cycle once the
// last word has been captured; `weights` holds the fully loaded set from
// that point until the next `start`.
//
// Address sequencing and data capture are offset by exactly one cycle to
// match the SRAM's latency: sram_addr/sram_ren for weight i are driven
// during cycle i of the load, and sram_rdata for weight i is captured
// during cycle i+1 (one cycle after that address was issued).

module sram_weight_loader #(
    parameter NUM_WEIGHTS  = 16,
    parameter WEIGHT_WIDTH = 8,
    parameter AW = (NUM_WEIGHTS > 1) ? $clog2(NUM_WEIGHTS) : 1
) (
    input  wire                                clk,
    input  wire                                rst,    // synchronous, active high
    input  wire                                start,  
    output wire                                busy,   // high from start until done pulses
    output wire                                done,   // one-cycle pulse: weights fully loaded
    output wire [                     AW-1:0]  sram_addr,
    output wire                                sram_ren,
    input  wire [           WEIGHT_WIDTH-1:0]  sram_rdata,
    output reg  [NUM_WEIGHTS*WEIGHT_WIDTH-1:0] weights
);
  initial begin
    if (NUM_WEIGHTS < 1) begin
      $error("sram_weight_loader: NUM_WEIGHTS (%0d) must be >= 1", NUM_WEIGHTS);
      $finish;
    end
  end

  localparam CW = (NUM_WEIGHTS > 1) ? $clog2(NUM_WEIGHTS + 1) : 1;
  reg  [CW-1:0] cnt;
  reg           busy_r;
  reg           done_r;

  assign busy      = busy_r;
  assign sram_addr = cnt[AW-1:0];
  assign sram_ren  = busy_r && (cnt < NUM_WEIGHTS);
  assign done      = done_r;

  always @(posedge clk) begin
    if (rst) begin
      busy_r <= 1'b0;
      cnt    <= 0;
    end else if (start && !busy_r) begin
      busy_r <= 1'b1;
      cnt    <= 0;
    end else if (busy_r) begin
      if (cnt == NUM_WEIGHTS) busy_r <= 1'b0;
      else cnt <= cnt + 1'b1;
    end
  end

  always @(posedge clk) begin
    if (rst) done_r <= 1'b0;
    else done_r <= busy_r && (cnt == NUM_WEIGHTS);
  end

  always @(posedge clk) begin
    if (!rst && busy_r && cnt >= 1 && cnt <= NUM_WEIGHTS)
      weights[(cnt-1)*WEIGHT_WIDTH+:WEIGHT_WIDTH] <= sram_rdata;
  end

endmodule
