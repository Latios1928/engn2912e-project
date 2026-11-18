#!/bin/bash -l
# Regenerate the analog SNN top level (analog/snn/snn_analog_inh.sch, with binary DACs and the bias cell) from the existing block
# layouts, run DRC + LVS, extract pins and render an image. The blocks are read as they are:
# rerun their own check scripts first if a block changed.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_snn_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/snn_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/snn_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_snn.py -rd out=SNN.gds
python3 make_snn_lvs_ref.py DAC_binary

echo "=== DRC (variant D)"
python3 $TECH/drc/run_drc.py --path=SNN.gds --variant=D --topcell=SNN --run_dir=$RUN/drc \
    --mp=8 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-300
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS (substrate net VSS; --combine merges parallel fingers on both sides)"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py SNN_lvs_ref.spice -o SNN_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=SNN.gds --netlist=SNN_lvs_ref.cdl --variant=D \
    --topcell=SNN --run_dir=$RUN/lvs --lvs_sub=VSS --combine > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/SNN.lvsdb klayout -b -r lvs_xref.py

echo "=== well bias (isolated P-wells, DNWELL, NWELL, substrate taps)"
LVSDB=$RUN/lvs/SNN.lvsdb klayout -b -r well_bias_check.py -rd gds=SNN.gds -rd out=SNN_well_bias.md | sed -n '/^## Issues found/,$p'

echo "=== pins, image"
klayout -b -r extract_pins.py -rd gds=SNN.gds -rd jout=SNN_pins.json -rd png=SNN.png > /dev/null
echo "wrote SNN_pins.json SNN.png"
