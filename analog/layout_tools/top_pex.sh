#!/bin/bash
# C-only Magic PEX of a top.py macro: top/<top>/<top>.gds -> top/<top>/pex/<top>_pex.spice
#   .subckt <top>_flat <macro pins>: all devices + parasitic C >= 0.01 fF, from a flattened copy.
# No wire R: Magic extresist merges isolated LVPWELL bodies (Isum islands) into the substrate.
# Usage: top_pex.sh [SNN_signed]
# Not "ext2spice lvs": with Magic 8.3.684 (open_pdks 1689ac3) it drops every node-to-substrate
# capacitor (6.7 of 9.6 pF on SNN_signed), while Magic 8.3.636 kept them. The settings below give
# the same devices and nets, plus those capacitors.
set -e
TOP=${1:-SNN_signed}
HERE=$(cd "$(dirname "$0")" && pwd)
D=$HERE/top/$TOP
RC=$PDK_ROOT/$PDK/libs.tech/magic/gf180mcuD.magicrc
RUN=/tmp/${TOP}_pex_run
rm -rf $RUN && mkdir -p $RUN $D/pex
cd $RUN
magic -dnull -noconsole -rcfile $RC > $D/pex/magic.log 2>&1 <<EOT
gds read $D/$TOP.gds
load $TOP
flatten ${TOP}_flat
load ${TOP}_flat
extract style ngspice()
extract all
ext2spice hierarchy off
ext2spice scale off
ext2spice subcircuit top on
ext2spice cthresh 0.01
ext2spice format ngspice
ext2spice -o $D/pex/${TOP}_pex.spice
quit -noprompt
EOT
# substrate = VSS (P+ guard rings); Magic leaves it as VSUBS
sed -i -E 's/(^|[ ])VSUBS([ ]|$)/\1VSS\2/g; s/(^|[ ])VSUBS([ ]|$)/\1VSS\2/g' $D/pex/${TOP}_pex.spice
cp $D/$TOP.gds $D/pex/$TOP.gds
printf "devices %d  C %d  R %d\n" $(grep -c '^X' $D/pex/${TOP}_pex.spice) $(grep -c '^C' $D/pex/${TOP}_pex.spice) $(grep -c '^R' $D/pex/${TOP}_pex.spice)
