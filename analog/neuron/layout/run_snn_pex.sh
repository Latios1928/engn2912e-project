#!/bin/bash -l
# Parasitic extraction of SNN.gds with Magic (gf180mcuD). Writes into PEX/:
#   SNN_pex_c.spice   flat netlist, all devices + every coupling / ground capacitance (cthresh 0),
#                     hierarchical net names (e.g. DPI_1/Isyn); from a hierarchical extraction
#   SNN_pex.spice     .subckt SNN_flat (ports = the SNN pins): devices + all parasitic C >= 0.01 fF,
#                     from a flattened copy. For post-layout simulation (X1 <pins> SNN_flat).
# No wire resistance: Magic's extresist merges the isolated LVPWELL body nodes (Isum of every DPI
# and DAC_signed output) into the substrate, which shorts Isum to VSS (the extracted SNN then draws
# ~0.88 mA and latches). Wire R in this layout is < ~100 ohm (RC delays of ps), so C-only is used.
# Magic instance names: DPI_j / neuron_sized_j are row 4-j (DPI_0 = output row u4, DPI_4 = input row u0).
# Run inside the iic-osic-tools container.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RC=$PDK_ROOT/$PDK/libs.tech/magic/gf180mcuD.magicrc
RUN=/tmp/snn_pex_run
rm -rf $RUN && mkdir -p $RUN/c $RUN/rc "$HERE/PEX"
cd $RUN/c
magic -dnull -noconsole -rcfile $RC > magic.log 2>&1 <<EOT
gds readonly true
gds read $HERE/SNN.gds
load SNN
extract style ngspice(si)
extract all
ext2spice lvs
ext2spice cthresh 0
ext2spice hierarchy off
ext2spice format ngspice
ext2spice -o $HERE/PEX/SNN_pex_c.spice
quit -noprompt
EOT
cd $RUN/rc
magic -dnull -noconsole -rcfile $RC > magic.log 2>&1 <<EOT
gds readonly true
gds read $HERE/SNN.gds
load SNN
flatten SNN_flat
load SNN_flat
extract style ngspice(si)
extract all
ext2spice lvs
ext2spice cthresh 0.01
ext2spice format ngspice
ext2spice -o $HERE/PEX/SNN_pex.spice
quit -noprompt
EOT
# Magic leaves the substrate as its own node VSUBS (only capacitors touch it). In this design the
# substrate is VSS (P+ guard rings), so map it onto VSS; otherwise the node floats in ngspice.
sed -i -E 's/(^|[ ])VSUBS([ ]|$)/\1VSS\2/g; s/(^|[ ])VSUBS([ ]|$)/\1VSS\2/g' "$HERE/PEX/SNN_pex_c.spice" "$HERE/PEX/SNN_pex.spice"
for f in SNN_pex_c SNN_pex; do
    printf "%-12s devices %5d  R %5d  C %5d\n" $f $(grep -c '^X' $HERE/PEX/$f.spice) $(grep -c '^R' $HERE/PEX/$f.spice) $(grep -c '^C' $HERE/PEX/$f.spice)
done
