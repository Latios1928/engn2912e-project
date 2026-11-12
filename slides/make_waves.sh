#!/bin/bash
# Regenerate the waveform PNGs for the slides. Run from anywhere:
#   slides/make_waves.sh
# The same views can be opened in Vaporview: digital/tb_rf.json and
# digital/tb_pulse_gen.json (open the matching .vcd after running this).
set -e
cd "$(dirname "$0")/.."
export PATH=/foss/tools/bin:$PATH

# rf: back-to-back writes, an ignored cycle (wren low), then an overwrite.
(cd digital && iverilog -g2012 -Wall -o sim.vvp rf.v tb_rf.v && vvp -n sim.vvp | grep -E 'PASS|FAIL')
python3 tools/vcd2png.py digital/tb_rf.vcd --start 0 --end 110 \
    --sig tb_rf.clk --sig tb_rf.wren --sig tb_rf.addr::dec --sig tb_rf.data \
    --sig tb_rf.weights \
    --title "rf: one word per write, all 8 words visible on weights (one hex digit each)" \
    -o slides/rf_wave.png

# pulse_gen (PERIOD 7, WIDTH 3, clk 10 ns): en is sampled at period boundaries
# (dashed lines, cnt = 0), so pulses always have the full width.
(cd digital && iverilog -g2012 -Wall -o sim.vvp pulse_gen.v tb_pulse_gen.v && vvp -n sim.vvp | grep -E 'PASS|FAIL')
python3 tools/vcd2png.py digital/tb_pulse_gen.vcd --start 20 --end 560 \
    --sig tb_pulse_gen.clk --sig tb_pulse_gen.dut.cnt::dec \
    --sig 'tb_pulse_gen.en[0]' --sig 'tb_pulse_gen.pulse[0]' \
    --sig 'tb_pulse_gen.en[1]' --sig 'tb_pulse_gen.pulse[1]' \
    --vline 95 --vline 165 --vline 235 --vline 305 --vline 375 --vline 445 --vline 515 \
    --title "pulse_gen: en sampled at period boundaries, pulses always full width" \
    -o slides/pulse_gen_wave.png

# Vaporview views of the same windows: digital/tb_rf.json and digital/tb_pulse_gen.json.
# zoomRatio there is pixels per ns for a 1000-pixel-wide waveform area
# (zoomRatio = width / window length, scrollLeft = window start * zoomRatio);
# adjust both if your pane is a different width.
