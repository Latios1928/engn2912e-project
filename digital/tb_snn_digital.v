`timescale 1ns / 1ns

// Self-checking testbench for snn_digital (regs + pulse_gen). Run (from this
// folder):
//
//   iverilog -g2012 -Wall -o sim.vvp tb_snn_digital.v snn_digital.v regs.v \
//            pulse_gen.v && vvp -n sim.vvp
//
//   1. reset values
//   2. weights and signs are written to w and s
//   3. the unused address and idle (4'hF) write nothing
//   4. data changed while an address is held is written
//   5. pulse timing: 10 every 200 at reset; a new period/width takes effect
//      from the next period; width 0 = no pulses
// clk is 1 us, as in mixed/.
module tb_snn_digital;
  localparam [3:0] IDLE = 4'hF;

  reg        clk = 1'b0;
  reg        rst = 1'b1;
  reg  [3:0] data = 4'h0;
  reg  [3:0] addr = IDLE;
  reg  [1:0] in = 2'b00;
  wire [31:0] w;
  wire [1:0] pulse;
  wire [7:0] s;

  always #500 clk = ~clk;

  snn_digital dut (
      .clk(clk),
      .rst(rst),
      .data(data),
      .addr(addr),
      .in(in),
      .w(w),
      .pulse(pulse),
      .s(s)
  );

  wire [7:0] period = dut.period;
  wire [7:0] width = dut.width;

  integer errors = 0;

  task check(input [8*80-1:0] what, input pass);  // up to 80 characters
    begin
      if (pass) $display("tb_snn_digital: PASS %0s", what);
      else begin
        errors = errors + 1;
        $display("tb_snn_digital: FAIL %0s", what);
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
  integer n_pulses = 0, cur_start = -1;
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

  integer i, k, n_before;
  reg ok;
  reg [31:0] w_before;
  reg [7:0] s_before;
  reg [7:0] p_before, wd_before;

  initial begin
    $dumpfile("tb_snn_digital.vcd");
    $dumpvars(0, tb_snn_digital);

    // Weights and signs have no reset; clear them so waveforms start at 0, not x.
    dut.u_regs.weights = 32'd0;
    dut.u_regs.signs = 8'd0;

    repeat (3) @(negedge clk);
    rst = 1'b0;

    // 1. reset values
    check("1 reset values (period 200, width 10)", period == 8'd200 && width == 8'd10);

    // 2. write every register
    for (i = 0; i < 8; i = i + 1) write_reg(i[3:0], i[3:0] + 4'd3);
    ok = 1'b1;
    for (i = 0; i < 8; i = i + 1) if (w[i*4+:4] !== i[3:0] + 4'd3) ok = 1'b0;
    check("2a weights 0-7 written to w[4w+3:4w]", ok);
    write_reg(4'd8, 4'h5);
    write_reg(4'd9, 4'hA);
    check("2b signs (addr 8, 9) to s", s == 8'hA5);
    // period/width are checked in part 5

    // 3. idle writes nothing while data changes
    w_before = w;
    s_before = s;
    p_before = period;
    wd_before = width;
    write_reg(4'd14, 4'h3);  // unused address
    addr = IDLE;
    for (i = 0; i < 40; i = i + 1) begin
      @(negedge clk);
      data = 4'($urandom);
    end
    check("3 unused (14) and idle (15) addresses write nothing",
          w === w_before && s === s_before &&
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
    write_reg(4'd10, 4'h8);  // period 200 = 8'hC8
    write_reg(4'd11, 4'hC);
    write_reg(4'd12, 4'hA);  // width 10 = 8'h0A
    write_reg(4'd13, 4'h0);
    in = 2'b01;
    wait (n_pulses == 3);
    ok = 1'b1;
    for (k = 1; k < 3; k = k + 1)
      if (widths[k] != 10 || starts[k] - starts[k-1] != 200) ok = 1'b0;
    check("5a reset timing: 10-cycle pulses every 200 cycles", ok);

    // Write period 50, width 5 just after a pulse starts, i.e. mid-period
    wait (pulse[0]);
    n_before = n_pulses;
    write_reg(4'd10, 4'h2);  // period 50 = 8'h32
    write_reg(4'd11, 4'h3);
    write_reg(4'd12, 4'h5);  // width 5
    write_reg(4'd13, 4'h0);
    wait (n_pulses == n_before + 4);
    // pulse n_before is the one running during the change: old timing
    ok = (widths[n_before] == 10) && (starts[n_before+1] - starts[n_before] == 200);
    for (k = n_before + 2; k < n_before + 4; k = k + 1)
      if (widths[k] != 5 || starts[k] - starts[k-1] != 50) ok = 1'b0;
    check("5b new timing (50/5) only from the next period; current pulse untouched", ok);

    // width 0 = no pulses (from the next period)
    write_reg(4'd12, 4'h0);
    repeat (60) @(negedge clk);  // let the current period finish
    n_before = n_pulses;
    repeat (300) @(negedge clk);
    check("5c width 0 gives no pulses", n_pulses == n_before && pulse == 2'b00);

    in = 2'b00;
    if (errors == 0) $display("tb_snn_digital: PASS, all checks");
    else $display("tb_snn_digital: FAIL, %0d checks failed", errors);
    $finish;
  end

endmodule
