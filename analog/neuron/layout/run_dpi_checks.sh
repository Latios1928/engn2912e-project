#!/bin/bash -l
# Regenerate the DPI layout, run DRC + LVS, extract pins and render images.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_dpi_checks.sh
# Outputs in this folder: DPI.gds, DPI_lvs_ref.cdl, DPI_pins.json, DPI.png, DPI_under_cap.png
# Run directories (DRC/LVS reports) go to /tmp/dpi_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/dpi_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_dpi.py -rd out=DPI.gds

echo "=== DRC (variant D: 5LM, MIM-B)"
python3 $TECH/drc/run_drc.py --path=DPI.gds --variant=D --topcell=DPI --run_dir=$RUN/drc \
    --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py DPI_lvs_ref.spice -o DPI_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=DPI.gds --netlist=DPI_lvs_ref.cdl --variant=D --topcell=DPI \
    --run_dir=$RUN/lvs > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/DPI.lvsdb klayout -b -r lvs_xref.py

echo "=== pins"
klayout -b -r extract_pins.py -rd gds=DPI.gds -rd jout=DPI_pins.json -rd png=DPI.png > /dev/null
klayout -b -r render_under.py -rd gds=DPI.gds -rd png=DPI_under_cap.png > /dev/null
echo "wrote DPI_pins.json DPI.png DPI_under_cap.png"
