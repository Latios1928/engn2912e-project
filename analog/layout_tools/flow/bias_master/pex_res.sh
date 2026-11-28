magic -rcfile /foss/pdks/gf180mcuD/libs.tech/magic/gf180mcuD.magicrc -noconsole -dnull << EOF
gds read /foss/designs/engn2912e-project/analog/layout_tools/flow/bias_master/bias_master.gds
load bias_master
flatten bias_master_flat -dotoplabels
load bias_master_flat
box 679.28um -14.12um 681.28um 34.67um
paint rnw
box 682.68um -14.12um 684.68um 34.67um
paint rnw
box 686.08um -14.12um 688.08um 34.66um
paint rnw
box 689.48um -14.12um 691.48um 34.66um
paint rnw
box 692.88um -14.12um 694.88um 34.66um
paint rnw
box 696.28um -14.12um 698.28um 34.66um
paint rnw
box 699.68um -14.12um 701.68um 34.66um
paint rnw
box 703.08um -14.12um 705.08um 34.66um
paint rnw
box 706.48um -14.12um 708.48um 34.66um
paint rnw
box 709.88um -14.12um 711.88um 34.66um
paint rnw
box 713.28um -14.12um 715.28um 34.66um
paint rnw
box 716.68um -14.12um 718.68um 34.66um
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
ext2spice -o bias_master_pex.spice
quit
EOF
