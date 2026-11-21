#!/bin/bash
# Run LibreLane on snn_top for GF180MCU (7-track 5V cells).
# Usage (inside the gf180-work container): ./run.sh
# The key outputs of the newest run are copied to results/ (tracked in git);
# the full runs/ folder is ignored.
cd "$(dirname "$0")"
librelane --manual-pdk --pdk-root /foss/pdks --pdk gf180mcuD \
    --scl gf180mcu_fd_sc_mcu7t5v0 config.json "$@" || exit $?

run=$(ls -d runs/*/ | tail -1)
mkdir -p results
cp "$run"final/gds/snn_top.gds \
   "$run"final/metrics.json "$run"final/metrics.csv \
   "$run"final/nl/snn_top.nl.v \
   "$run"final/pnl/snn_top.pnl.v \
   "$run"final/render/*.png results/ 2>/dev/null
mkdir -p results/sdf
for c in nom_ss_125C_3v00 nom_tt_025C_3v30 nom_ff_n40C_3v60; do
    cp "$run"final/sdf/$c/snn_top__$c.sdf results/sdf/   # for gls/ (make timing)
done
echo "Copied outputs of $run to results/"

# Submission files (lvs_config.json): the chip GDS, and the powered netlist,
# which chip-level LVS needs (final/nl has no power pins).
cp "$run"final/gds/snn_top.gds ../../gds/snn_top.gds
cp "$run"final/pnl/snn_top.pnl.v ../../verilog/gl/snn_top.v
echo "Copied snn_top.gds to gds/ and snn_top.pnl.v to verilog/gl/snn_top.v"
echo "Next: python3 chip_lvs.py (full-chip LVS; LibreLane's own LVS black-boxes the macro)"
