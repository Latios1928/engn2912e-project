magic -rcfile /foss/pdks/gf180mcuD/libs.tech/magic/gf180mcuD.magicrc -noconsole -dnull << EOF
gds read /foss/designs/engn2912e-project/analog/layout_tools/flow/trim_steer/trim_steer.gds
load trim_steer
flatten trim_steer_flat -dotoplabels
load trim_steer_flat
box 253.49um -7.025um 255.49um 42.975um
paint rnw
box 256.89um -7.025um 258.89um 42.975um
paint rnw
box 260.29um -7.025um 262.29um 42.975um
paint rnw
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
ext2spice -o trim_steer_pex.spice
quit
EOF
