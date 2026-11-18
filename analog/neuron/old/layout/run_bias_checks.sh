#!/bin/bash -l
# Regenerate the bias cell layout (bias_cell.sch: current-mode bias generator), run DRC + LVS, extract pins, coupling reports and images.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_dac_signed_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/bias_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/bias_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_bias.py -rd out=bias_cell.gds

echo "=== DRC (variant D)"
python3 $TECH/drc/run_drc.py --path=bias_cell.gds --variant=D --topcell=bias_cell \
    --run_dir=$RUN/drc --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS (substrate net VSS; --combine merges parallel fingers on both sides)"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py bias_cell_lvs_ref.spice -o bias_cell_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=bias_cell.gds --netlist=bias_cell_lvs_ref.cdl --variant=D \
    --topcell=bias_cell --run_dir=$RUN/lvs --lvs_sub=VSS --combine > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/bias_cell.lvsdb klayout -b -r lvs_xref.py

echo "=== pins, image"
klayout -b -r extract_pins.py -rd gds=bias_cell.gds -rd jout=bias_cell_pins.json -rd png=bias_cell.png > /dev/null
echo "wrote bias_cell_pins.json bias_cell.png"
