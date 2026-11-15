`timescale 1ns / 1ns

// Digital-only test of the addr4_trim interface: snn_digital_v2 (regs_v2 +
// pulse_gen_v2). No analog side, runs in a second:
//
//   iverilog -g2012 -Wall -s tb_regs_v2 -o tb_regs_v2.vvp tb_regs_v2.v \
//            snn_digital_v2.v regs_v2.v pulse_gen_v2.v && vvp -n tb_regs_v2.vvp
//
// Checks, each printed as PASS/FAIL:
//   1. reset values: period 200, width 10, trim 9, debug 0
//   2. every register can be written and read back on its output
//   3. addr = 4'hF (idle) writes nothing, whatever data does
//   4. holding an address while data changes writes the new data (why the
//      protocol says: change data only while idle)
//   5. pulses: 10 cycles every 200 at reset; a new period/width written
//      mid-period takes effect only from the next period; width 0 = no pulses
// clk is 1 MHz (1 us), as in mixed/snn_ms_tb.v.
module tb_regs_v2;
  localparam [3:0] IDLE = 4'hF;

  reg        clk = 1'b0;
  reg        rst = 1'b1;
  reg  [3:0] data = 4'h0;
  reg  [3:0] addr = IDLE;
  reg  [1:0] in = 2'b00;
  wire [31:0] w;
  wire [1:0] pulse;
  wire [3:0] trim, dbg0, dbg1;

  always #500 clk = ~clk;

  snn_digital_v2 dut (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .in(in),
      .w(w),
      .pulse(pulse),
      .trim(trim),
      .dbg0(dbg0),
      .dbg1(dbg1)
  );

  wire [7:0] period = dut.period;
  wire [7:0] width = dut.width;

  integer errors = 0;

  task check(input [8*80-1:0] what, input ok);  // up to 80 characters
    begin
      if (ok) $display("tb_regs_v2: PASS %0s", what);
      else begin
        errors = errors + 1;
        $display("tb_regs_v2: FAIL %0s", what);
      end
    end
  endtask

  // The write protocol: data while idle, address for one cycle, back to idle
  task write_reg(input [3:0] a, input [3:0] d);
    begin
      @(negedge clk);
      data = d;
      @(negedge clk);
      addr = a;
      @(negedge clk);
      addr = IDLE;
    end
  endtask

  // Pulse measurement on channel 0: start cycle and width of each pulse
  integer cyc = 0;
  always @(posedge clk) cyc <= cyc + 1;
  integer n_pulses = 0, last_start = -1, cur_start = -1;
  integer starts[0:63];
  integer widths[0:63];
  reg p0_q = 1'b0;
  always @(posedge clk) begin
    p0_q <= pulse[0];
    if (pulse[0] && !p0_q) cur_start <= cyc;
    if (!pulse[0] && p0_q && n_pulses < 64) begin
      starts[n_pulses] <= cur_start;
      widths[n_pulses] <= cyc - cur_start;
      n_pulses <= n_pulses + 1;
    end
  end

  integer i, k, ok, t_change, n_before;
  reg [31:0] w_before;
  reg [3:0] trim_before, d0_before, d1_before;
  reg [7:0] p_before, wd_before;

  initial begin
    $dumpfile("tb_regs_v2.vcd");
    $dumpvars(0, tb_regs_v2);

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // 1. reset values
    check("1 reset values (period 200, width 10, trim 9, debug 0)",
          period == 8'd200 && width == 8'd10 && trim == 4'd9 && dbg0 == 4'd0 && dbg1 == 4'd0);

    // 2. write every register
    for (i = 0; i < 8; i = i + 1) write_reg(i[3:0], 4'(i + 3));
    ok = 1;
    for (i = 0; i < 8; i = i + 1) if (w[i*4+:4] !== 4'(i + 3)) ok = 0;
    check("2a weights 0-7 written to w[4w+3:4w]", ok);
    write_reg(4'd12, 4'd5);
    check("2b trim (addr 12)", trim == 4'd5);
    write_reg(4'd13, 4'hA);
    write_reg(4'd14, 4'h6);
    check("2c debug registers (addr 13, 14)", dbg0 == 4'hA && dbg1 == 4'h6);
    // period/width are checked in part 5

    // 3. idle writes nothing while data changes
    w_before = w;
    trim_before = trim;
    d0_before = dbg0;
    d1_before = dbg1;
    p_before = period;
    wd_before = width;
    addr = IDLE;
    for (i = 0; i < 40; i = i + 1) begin
      @(negedge clk);
      data = $urandom;
    end
    check("3 idle (addr 15) writes nothing",
          w === w_before && trim === trim_before && dbg0 === d0_before && dbg1 === d1_before &&
          period === p_before && width === wd_before);

    // 4. holding an address while data changes writes the new data
    @(negedge clk);
    data = 4'h1;
    addr = 4'd3;
    @(negedge clk);
    data = 4'hE;  // changed while addr still points at weight 3
    @(negedge clk);
    addr = IDLE;
    check("4 data changed while addr held is written (protocol rule)", w[15:12] === 4'hE);

    // 5. pulse timing. Restore reset timing, then run channel 0.
    write_reg(4'd8, 4'h8);  // period 200 = 8'hC8
    write_reg(4'd9, 4'hC);
    write_reg(4'd10, 4'hA);  // width 10 = 8'h0A
    write_reg(4'd11, 4'h0);
    in = 2'b01;
    wait (n_pulses == 3);
    ok = 1;
    for (k = 1; k < 3; k = k + 1)
      if (widths[k] != 10 || starts[k] - starts[k-1] != 200) ok = 0;
    check("5a reset timing: 10-cycle pulses every 200 cycles", ok);

    // Write period 50, width 5 just after a pulse starts, i.e. mid-period
    wait (pulse[0]);
    t_change = cyc;
    n_before = n_pulses;
    write_reg(4'd8, 4'h2);  // period 50 = 8'h32
    write_reg(4'd9, 4'h3);
    write_reg(4'd10, 4'h5);  // width 5
    write_reg(4'd11, 4'h0);
    wait (n_pulses == n_before + 4);
    // pulse n_before is the one running during the change: old timing
    ok = (widths[n_before] == 10) && (starts[n_before+1] - starts[n_before] == 200);
    for (k = n_before + 2; k < n_before + 4; k = k + 1)
      if (widths[k] != 5 || starts[k] - starts[k-1] != 50) ok = 0;
    check("5b new timing (50/5) only from the next period; current pulse untouched", ok);

    // width 0 = no pulses (from the next period)
    write_reg(4'd10, 4'h0);
    repeat (60) @(negedge clk);  // let the current period finish
    n_before = n_pulses;
    repeat (300) @(negedge clk);
    check("5c width 0 gives no pulses", n_pulses == n_before && pulse == 2'b00);

    in = 2'b00;
    if (errors == 0) $display("tb_regs_v2: PASS, all checks");
    else $display("tb_regs_v2: FAIL, %0d checks failed", errors);
    $finish;
  end

endmodule
