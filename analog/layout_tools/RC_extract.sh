#!/bin/bash
# args:
# first arg = gds file to read
# second arg = name of top cell in gds file to read
magic -rcfile /foss/pdks/gf180mcuD/libs.tech/magic//gf180mcuD.magicrc -noconsole -dnull << EOF
gds read $1
load $2
flatten $2_flat -dotoplabels
load $2_flat
select top cell
extract do local
extract halo 0.5um
extract all
ext2sim labels on
ext2sim
extresist tolerance 25
extresist
ext2spice lvs
ext2spice cthresh 0.5f
ext2spice rthresh 5
ext2spice extresist on
ext2spice -o $2_pex.spice
quit
EOF

