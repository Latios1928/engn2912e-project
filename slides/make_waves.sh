#!/bin/bash
# Regenerate the waveform PNGs for the slides from digital/tb_snn_digital.v.
# Run from anywhere:
#   slides/make_waves.sh
set -e
cd "$(dirname "$0")/.."
export PATH=/foss/tools/bin:$PATH

(cd digital && iverilog -g2012 -Wall -o sim.vvp tb_snn_digital.v snn_digital.v regs.v pulse_gen.v &&
    vvp -n sim.vvp | grep -E 'all checks')

# regs: data set while idle (addr F), then addr for one cycle. Magnitudes 0-7
# (each hex digit of w is one synapse, 7 on the left), then the two sign
# registers.
python3 tools/vcd2png.py digital/tb_snn_digital.vcd --start 1000 --end 37000 \
    --sig tb_snn_digital.clk --sig tb_snn_digital.addr --sig tb_snn_digital.data \
    --sig tb_snn_digital.w --sig tb_snn_digital.s::bin \
    --title "regs: write data to the register at addr; addr = F is idle" \
    -o slides/regs_wave.png

# pulse_gen: period 200 -> 50 and width 10 -> 5 written mid-period (after the
# pulse at 802 us); the new timing starts at the next period boundary (dashed).
# Same window, en (INPUT EN, register 14): en[1] raised mid-period waits for the
# boundary (pulse[1] starts with pulse[0]); dropped just after the 1052 us
# boundary it still finishes that pulse and gives none after (tb check 5b).
python3 tools/vcd2png.py digital/tb_snn_digital.vcd --start 780000 --end 1160000 \
    --sig tb_snn_digital.period::dec \
    --sig tb_snn_digital.width::dec \
    --sig 'tb_snn_digital.in_en[0]:en[0]' --sig 'tb_snn_digital.in_en[1]:en[1]' \
    --sig 'tb_snn_digital.pulse[0]:pulse[0]' --sig 'tb_snn_digital.pulse[1]:pulse[1]' \
    --vline 1002500 --vline 1052500 --vline 1102500 \
    --title "pulse_gen: new period/width and en take effect at the next period" \
    -o slides/pulse_gen_wave.png
