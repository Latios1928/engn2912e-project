#!/usr/bin/env python3
"""Simulation copies for the gate-level mixed-signal run (the originals are not changed).

    python3 prep.py <netlist.nl.v> <mixed/snn_ms_tb.v> <out netlist> <out tb>

Netlist (LibreLane final/nl): drop the .Iref / .VT connections of u_snn_analog. In this
run the SPICE side (mixed/snn_ms_tb.spice) sources Iref and VT itself, so the black box
analog/snn/snn_analog.v is compiled without ANALOG_PINS and SpiceBind sees the same
ports as in mixed/.

Testbench (mixed/snn_ms_tb.v): it peeks at two RTL-internal signals that a flat
gate-level netlist does not have:
  - dut.pulse (waveform only)           -> dut.u_snn_analog.pulse (same nets)
  - dut.u_digital.period / .width check -> skipped (the reset values are checked by the
    RTL runs and by the digital GLS, ../gls)
"""
import re
import sys


def sub_once(text, old, new, what):
    n = text.count(old)
    if n < 1:
        sys.exit(f"prep.py: {what}: pattern not found: {old!r}")
    return text.replace(old, new)


def main(nl_in, tb_in, nl_out, tb_out):
    nl = open(nl_in).read()
    nl, n = re.subn(r"(snn_analog u_snn_analog \()\.Iref\(Iref\),\s*\.VT\(VT\),\s*", r"\1", nl)
    if n != 1:
        sys.exit(f"prep.py: expected one u_snn_analog with .Iref/.VT first, found {n}")
    open(nl_out, "w").write(nl)

    tb = open(tb_in).read()
    tb = sub_once(tb, "dut.pulse;", "dut.u_snn_analog.pulse;", "pulse")
    tb = sub_once(tb, "if (dut.u_digital.period !== 8'd200 || dut.u_digital.width !== 8'd10) begin",
                  "if (1'b0) begin  // GLS: reset values not visible in the flat netlist", "check")
    tb = sub_once(tb, "dut.u_digital.period,", "8'd0,", "display")
    tb = sub_once(tb, "dut.u_digital.width);", "8'd0);", "display")
    assert "u_digital" not in tb, "prep.py: u_digital still referenced"
    open(tb_out, "w").write(tb)
    print(f"prep.py: {nl_out}, {tb_out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
