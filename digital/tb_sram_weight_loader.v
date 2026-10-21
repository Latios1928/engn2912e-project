// Self-checking testbench for sram_weight_loader.
//
// Models a single-port synchronous SRAM with 1-cycle read latency,
// pre-loaded with random reference weight values. Drives `start`, waits
// for `done`, and checks that every slice of `weights` matches the
// reference SRAM content. Repeats across several load passes (including
// a reset issued mid-load) to confirm the loader restarts cleanly.
//
// Run:
//   iverilog -g2012 -Wall -o sim.vvp sram_weight_loader.v tb_sram_weight_loader.v && vvp sim.vvp
//   iverilog -g2012 -Ptb_sram_weight_loader.NUM_WEIGHTS=24 ...   (other sizes)

module tb_sram_weight_loader #(
    parameter NUM_WEIGHTS  = 16,
    parameter WEIGHT_WIDTH = 8,
    parameter NPASSES      = 6
);
  localparam AW = (NUM_WEIGHTS > 1) ? $clog2(NUM_WEIGHTS) : 1;

  reg                     clk = 1'b0;
  reg                     rst = 1'b1;
  reg                     start = 1'b0;
  wire                    busy;
  wire                    done;
  wire [          AW-1:0] sram_addr;
  wire                    sram_ren;
  reg  [WEIGHT_WIDTH-1:0] sram_rdata;

  wire [NUM_WEIGHTS*WEIGHT_WIDTH-1:0] weights;

  sram_weight_loader #(
      .NUM_WEIGHTS (NUM_WEIGHTS),
      .WEIGHT_WIDTH(WEIGHT_WIDTH)
  ) dut (
      .clk(clk),
      .rst(rst),
      .start(start),
      .busy(busy),
      .done(done),
      .sram_addr(sram_addr),
      .sram_ren(sram_ren),
      .sram_rdata(sram_rdata),
      .weights(weights)
  );

  always #5 clk = ~clk;

  // Behavioral SRAM: synchronous read, 1-cycle latency, reference content
  // reloaded with fresh random values before each pass.
  reg [WEIGHT_WIDTH-1:0] mem[0:NUM_WEIGHTS-1];
  always @(posedge clk) begin
    if (sram_ren) sram_rdata <= mem[sram_addr];
  end

  integer errors = 0;
  integer checks = 0;
  integer i;

  task fill_mem;
    begin
      for (i = 0; i < NUM_WEIGHTS; i = i + 1) mem[i] = $urandom;
    end
  endtask

  task check_weights;
    begin
      checks = checks + 1;
      for (i = 0; i < NUM_WEIGHTS; i = i + 1) begin
        if (weights[i*WEIGHT_WIDTH+:WEIGHT_WIDTH] !== mem[i]) begin
          errors = errors + 1;
          $display("%0t: weights[%0d]=%h, expected %h", $time, i,
                    weights[i*WEIGHT_WIDTH+:WEIGHT_WIDTH], mem[i]);
        end
      end
    end
  endtask

  integer pass;
  initial begin
    $dumpfile("tb_sram_weight_loader.vcd");
    $dumpvars(0, tb_sram_weight_loader);

    sram_rdata = 0;
    @(negedge clk);
    rst = 1'b0;

    for (pass = 0; pass < NPASSES; pass = pass + 1) begin
      fill_mem();
      @(negedge clk);
      start = 1'b1;
      @(negedge clk);
      start = 1'b0;

      // Mid-load reset on one pass, to confirm the loader aborts cleanly
      // rather than producing a partially-loaded false "done". The NEXT
      // pass (a normal start/wait/check) then verifies the loader actually
      // recovered into a working state afterward.
      if (pass == NPASSES / 2) begin
        repeat (2) @(negedge clk);
        rst = 1'b1;
        @(negedge clk);
        rst = 1'b0;
      end else begin
        wait (done);
        @(negedge clk);
        check_weights();
      end
    end

    if (errors == 0) $display("PASS: NUM_WEIGHTS=%0d WEIGHT_WIDTH=%0d, %0d checks", NUM_WEIGHTS,
                               WEIGHT_WIDTH, checks);
    else
      $display("FAIL: NUM_WEIGHTS=%0d WEIGHT_WIDTH=%0d, %0d errors in %0d checks", NUM_WEIGHTS,
                WEIGHT_WIDTH, errors, checks);
    $finish;
  end

endmodule
