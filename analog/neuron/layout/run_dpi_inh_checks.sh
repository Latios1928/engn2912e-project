#!/bin/bash -l
# Regenerate the inhibitory DPI layout (DPI_inh.sch: DPI_sized + nFET mirror), run DRC + LVS,
# extract pins and render an image. Regenerates DPI_sized.gds first (it is a subcell).
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_dpi_inh_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/dpi_inh_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/dpi_inh_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_dpi.py -rd out=DPI_sized.gds -rd name=DPI_sized -rd w=0.88 -rd l=1.12
klayout -b -r extract_pins.py -rd gds=DPI_sized.gds -rd jout=DPI_sized_pins.json > /dev/null
klayout -b -r gen_dpi_inh.py -rd out=DPI_inh.gds

echo "=== DRC (variant D: 5LM, MIM-B)"
python3 $TECH/drc/run_drc.py --path=DPI_inh.gds --variant=D --topcell=DPI_inh --run_dir=$RUN/drc \
    --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS (substrate net GND)"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py DPI_inh_lvs_ref.spice -o DPI_inh_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=DPI_inh.gds --netlist=DPI_inh_lvs_ref.cdl --variant=D \
    --topcell=DPI_inh --run_dir=$RUN/lvs --lvs_sub=GND > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/DPI_inh.lvsdb klayout -b -r lvs_xref.py

echo "=== pins, image"
klayout -b -r extract_pins.py -rd gds=DPI_inh.gds -rd jout=DPI_inh_pins.json -rd png=DPI_inh.png > /dev/null
klayout -b -r render_under.py -rd gds=DPI_inh.gds -rd png=DPI_inh_under_cap.png > /dev/null
echo "wrote DPI_inh_pins.json DPI_inh.png DPI_inh_under_cap.png"
