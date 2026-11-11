#!/bin/bash -l
# Regenerate the neuron_sized layout, run DRC + LVS, extract pins, VMEM coupling report and images.
# Run inside the iic-osic-tools container:
#   docker exec <container> bash -l /foss/designs/engn2912e-project/analog/neuron/layout/run_neuron_checks.sh
# Run directories (DRC/LVS reports) go to /tmp/neuron_checks (outside the repo).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RUN=/tmp/neuron_checks
TECH=$PDK_ROOT/$PDK/libs.tech/klayout/tech
mkdir -p $RUN/drc $RUN/lvs
cd "$HERE"

klayout -b -r gen_neuron.py -rd out=neuron_sized.gds

echo "=== DRC (variant D: 5LM, MIM-B)"
python3 $TECH/drc/run_drc.py --path=neuron_sized.gds --variant=D --topcell=neuron_sized \
    --run_dir=$RUN/drc --mp=4 > $RUN/drc/log.txt 2>&1 || true
grep -E "Violated|is clean" $RUN/drc/log.txt | cut -c1-200
grep -q "mslot generated an exception" $RUN/drc/log.txt && \
    echo "note: mslot table crashed (PDK deck bug, nil via_below for Metal1); MSLOT.1 needs metal > 30 um wide, not present here"
RDBDIR=$RUN/drc klayout -b -r drc_summary.py

echo "=== LVS"
python3 $TECH/lvs/gf180_xschem_klayout_spice_convert.py neuron_sized_lvs_ref.spice -o neuron_sized_lvs_ref.cdl
python3 $TECH/lvs/run_lvs.py --layout=neuron_sized.gds --netlist=neuron_sized_lvs_ref.cdl --variant=D \
    --topcell=neuron_sized --run_dir=$RUN/lvs > $RUN/lvs/log.txt 2>&1 || true
grep -E "Netlists (don.t )?match|Congratulations" $RUN/lvs/log.txt | cut -c1-200
LVSDB=$RUN/lvs/neuron_sized.lvsdb klayout -b -r lvs_xref.py

echo "=== pins, VMEM coupling, images"
klayout -b -r extract_pins.py -rd gds=neuron_sized.gds -rd jout=neuron_sized_pins.json -rd png=neuron_sized.png > /dev/null
klayout -b -r render_under.py -rd gds=neuron_sized.gds -rd png=neuron_sized_under_cap.png > /dev/null
for n in VMEM spike net1 net2; do
    LVSDB=$RUN/lvs/neuron_sized.lvsdb klayout -b -r coupling.py -rd gds=neuron_sized.gds -rd net=$n \
        -rd out=coupling_$n.txt > /dev/null
done
echo "wrote neuron_sized_pins.json neuron_sized.png neuron_sized_under_cap.png coupling_{VMEM,spike,net1,net2}.txt"
