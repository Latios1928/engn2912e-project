#!/bin/bash -l
# Regenerate the binary DAC layout (DAC_binary.sch), run DRC + LVS, extract pins, coupling reports and images.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_dac_binary_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/dac_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/dac_binary_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_dac_binary.py -rd out=DAC_binary.gds

echo "=== DRC (variant D)"
python3 $TECH/drc/run_drc.py --path=DAC_binary.gds --variant=D --topcell=DAC_binary \
    --run_dir=$RUN/drc --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS (substrate net GND; --combine merges parallel fingers on both sides)"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py DAC_binary_lvs_ref.spice -o DAC_binary_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=DAC_binary.gds --netlist=DAC_binary_lvs_ref.cdl --variant=D \
    --topcell=DAC_binary --run_dir=$RUN/lvs --lvs_sub=GND --combine > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/DAC_binary.lvsdb klayout -b -r lvs_xref.py

echo "=== pins, coupling, image"
klayout -b -r extract_pins.py -rd gds=DAC_binary.gds -rd jout=DAC_binary_pins.json -rd png=DAC_binary.png > /dev/null
for n in Vb X Isum net1 net2 net3 net4 en 'w[0]' 'w[1]' 'w[2]' 'w[3]'; do
    LVSDB=$RUN/lvs/DAC_binary.lvsdb klayout -b -r coupling.py -rd gds=DAC_binary.gds -rd net=$n \
        -rd out="DAC_binary_coupling_$(echo $n | tr -d '[]')".txt > /dev/null
done
echo "wrote DAC_binary_pins.json DAC_binary.png DAC_binary_coupling_{Vb,X,Isum,net1..net4,en,w0..w3}.txt"
