#!/bin/bash -l
# Parasitic extraction of one analog layout, ready for the post-layout testbenches.
#
#   docker exec gf180-work bash -l /foss/designs/engn2912e-project/analog/neuron/layout/PEX/extract.sh neuron_sized
#
# 1. copies <cell>.gds from analog/neuron/layout (or analog/DAC/layout,
#    analog/DPI/layout) into this folder (the extraction always
#    uses the current layout),
# 2. runs RC_extract.sh (Magic: flatten, extract devices + R + C, cthresh 0.5f,
#    rthresh 5) -> <cell>_pex.spice, log in RC_extract_<cell>.log,
# 3. lists Magic's extraction warnings and the devices it found, so they can be
#    checked against the schematic,
# 4. writes <cell>_pex_wrapper.spice (make_pex_wrapper.py), which gives the
#    extracted cell the pin order of <cell>.sym (analog/neuron, DAC or DPI).
# See README.md in this folder.
set -e
cell=${1:?usage: extract.sh <cell>   (e.g. neuron_sized, DAC_signed, DPI_sized)}
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"
# The GDS lives with its block: analog/neuron/layout, analog/DAC/layout or analog/DPI/layout.
gds=""
for d in .. ../../../DAC/layout ../../../DPI/layout; do
    [ -f "$d/$cell.gds" ] && { gds="$d/$cell.gds"; break; }
done
[ -n "$gds" ] || { echo "error: $cell.gds not found in analog/{neuron,DAC,DPI}/layout"; exit 1; }

cp "$gds" .
rm -f "${cell}_pex.spice"
bash RC_extract.sh "$cell.gds" "$cell" > "RC_extract_$cell.log" 2>&1
[ -s "${cell}_pex.spice" ] || { echo "error: Magic wrote no ${cell}_pex.spice, see RC_extract_$cell.log"; exit 1; }

# Magic only counts its warnings in the log. Extract again in a scratch folder
# (so this folder's output is untouched) and save the warning texts.
tmp=$(mktemp -d)
cp "$cell.gds" "$tmp/"
(cd "$tmp" && magic -rcfile "$PDK_ROOT/$PDK/libs.tech/magic/$PDK.magicrc" -noconsole -dnull > /dev/null 2>&1 << EOF
gds read $cell.gds
load $cell
flatten ${cell}_flat -dotoplabels
load ${cell}_flat
extract all
feedback save warnings.txt
quit
EOF
)
cp "$tmp/warnings.txt" "${cell}_extract_warnings.txt" 2> /dev/null || : > "${cell}_extract_warnings.txt"
rm -rf "$tmp"

echo "== $cell: extraction warnings (dummy transistors give 'device missing 1 terminal')"
if [ -s "${cell}_extract_warnings.txt" ]; then
    grep -A1 "^feedback add" "${cell}_extract_warnings.txt" | grep -v -E "^(--|box)" \
        | sed 's/^feedback add //' | tr -d '"' | paste -d' ' - - | sed 's/ pale$//' | sort | uniq -c
else
    echo "   none"
fi
echo "== devices in ${cell}_pex.spice"
grep -E "^X" "${cell}_pex.spice" | grep -oE "(nfet|pfet)_[0-9a-z]+|cap_mim[a-z0-9_]*|ppolyf[a-z0-9_]*" | sort | uniq -c
echo "   parasitic C: $(grep -cE '^C' "${cell}_pex.spice"), R: $(grep -cE '^R' "${cell}_pex.spice")"

python3 make_pex_wrapper.py "$cell"
