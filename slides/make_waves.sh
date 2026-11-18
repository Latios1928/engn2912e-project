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
python3 tools/vcd2png.py digital/tb_snn_digital.vcd --start 780000 --end 1100000 \
    --sig tb_snn_digital.period::dec \
    --sig tb_snn_digital.width::dec --sig 'tb_snn_digital.pulse[0]:pulse[0]' \
    --vline 1001500 \
    --title "pulse_gen: new period/width take effect at the next period" \
    -o slides/pulse_gen_wave.png
