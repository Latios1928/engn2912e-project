#!/bin/bash -l
# Regenerate the signed DAC layout (DAC_signed.sch with the binary DAC + sign steering); DAC_binary.gds must exist (run_dac_binary_checks.sh), run DRC + LVS, extract pins, coupling reports and images.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_dac_signed_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/dac_signed_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/dac_signed_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_dac_signed.py -rd out=DAC_signed.gds

echo "=== DRC (variant D)"
python3 $TECH/drc/run_drc.py --path=DAC_signed.gds --variant=D --topcell=DAC_signed \
    --run_dir=$RUN/drc --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS (substrate net GND; --combine merges parallel fingers on both sides)"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py DAC_signed_lvs_ref.spice -o DAC_signed_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=DAC_signed.gds --netlist=DAC_signed_lvs_ref.cdl --variant=D \
    --topcell=DAC_signed --run_dir=$RUN/lvs --lvs_sub=GND --combine > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/DAC_signed.lvsdb klayout -b -r lvs_xref.py

echo "=== pins, coupling, image"
klayout -b -r extract_pins.py -rd gds=DAC_signed.gds -rd jout=DAC_signed_pins.json -rd png=DAC_signed.png > /dev/null
for n in Y Isum_e Isum_i s sb; do
    LVSDB=$RUN/lvs/DAC_signed.lvsdb klayout -b -r coupling.py -rd gds=DAC_signed.gds -rd net=$n \
        -rd out="DAC_signed_coupling_$(echo $n | tr -d '[]')".txt > /dev/null
done
echo "wrote DAC_signed_pins.json DAC_signed.png DAC_signed_coupling_{Y,Isum_e,Isum_i,s,sb}.txt"
