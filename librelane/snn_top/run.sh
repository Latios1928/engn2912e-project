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
   "$run"final/render/*.png results/ 2>/dev/null
echo "Copied outputs of $run to results/"
