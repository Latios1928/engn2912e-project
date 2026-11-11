// Pure-digital build: the chip top with the behavioral snn_analog in this
// folder. Run from this folder:
//   iverilog -g2012 -Wall -s tb_snn_top -o sim.vvp -f sim.f && vvp sim.vvp
../snn_top.v
../digital/snn_digital.v
../digital/rf.v
../digital/pulse_gen.v
snn_analog.v
neuron.v
comparator.v
dac.v
tb_snn_top.v
