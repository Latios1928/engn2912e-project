"""Write SNN_lvs_ref.spice: the hierarchical LVS reference of SNN.gds (gen_snn.py).

    python3 make_snn_lvs_ref.py [DAC_binary|DAC]

Subcircuits are copied from the blocks' own LVS references; the top level follows the xschem
netlist of analog/snn/snn_analog_inh.sch, with the plain DACs as the chosen DAC cell
(default DAC_binary) and every GND as VSS.
"""
import sys

DAC = sys.argv[1] if len(sys.argv) > 1 else "DAC_binary"


def subckts(f):
    out, cur = {}, None
    for line in open(f):
        if line.lower().startswith(".subckt"):
            cur = line.split()[1]
            out[cur] = [line]
        elif cur:
            out[cur].append(line)
            if line.lower().startswith(".ends"):
                cur = None
    return out


lib = {}
for f in ("neuron_sized", "DPI", DAC, "DAC_signed", "DPI_inh"):
    for k, v in subckts(f + "_lvs_ref.spice").items():
        assert k not in lib or lib[k] == v, k
        lib[k] = v
ports = {k: v[0].split()[2:] for k, v in lib.items()}


def inst(name, cell, conn):
    conn = {k: ("VSS" if v == "GND" else v) for k, v in conn.items()}
    assert set(conn) == set(ports[cell]), (name, set(ports[cell]) ^ set(conn))
    return "%s %s %s" % (name, " ".join(conn[q] for q in ports[cell]), cell)


def W(m):
    return {"w[%d]" % b: "w[%d]" % (4 * m + b) for b in range(4)}


L = []
for n, m, isum, en in (("xdac0_0", 0, "Isum_0", "pulse[0]"), ("xdac1_0", 1, "Isum_1", "pulse[1]"),
                       ("xdac2_0", 2, "Isum_2", "spike[0]"), ("xdac2_1", 3, "Isum_2", "spike[1]"),
                       ("xdac3_0", 4, "Isum_3", "spike[0]"), ("xdac3_1", 5, "Isum_3", "spike[1]")):
    L.append(inst(n, DAC, {"Isum": isum, "Vb": "Vb", "en": en, "VDD": "VDD", "GND": "VSS", **W(m)}))
for n, m, en, s in (("xdac4_0", 6, "spike[2]", "s[0]"), ("xdac4_1", 7, "spike[3]", "s[1]")):
    L.append(inst(n, "DAC_signed", {"Isum_e": "Isum_4", "Isum_i": "Isum_5", "s": s, "Vb": "Vb",
                                    "en": en, "VDD": "VDD", "GND": "VSS", **W(m)}))
for u in range(5):
    L.append(inst("xdpi%d" % u, "DPI", {"VDD": "VDD", "Vthr": "Vthr", "Isyn": "VMEM_%d" % u,
                                        "Isum": "Isum_%d" % u, "VT": "VT_dpi", "VSS": "VSS"}))
L.append(inst("xdpi5", "DPI_inh", {"VDD": "VDD", "Vthr": "Vthr", "VT": "VT_inh", "Isum": "Isum_5",
                                   "Iout": "VMEM_4", "GND": "VSS"}))
B = ["VNA", "Vlk", "VK", "VIp", "VKup", "VKdn", "Vamp_bias", "VT"]
for u in range(5):
    L.append(inst("xneu%d" % u, "neuron_sized", {"VSS": "VSS", "VDD": "VDD", "VMEM": "VMEM_%d" % u,
                                                  "spike": "spike[%d]" % u, **{b: b for b in B}}))
pins = (["VDD", "VSS", "Vb"] + ["w[%d]" % i for i in range(32)]
        + ["pulse[0]", "pulse[1]", "s[0]", "s[1]", "Vthr", "VT_dpi", "VT_inh"] + B
        + ["spike[%d]" % i for i in range(5)])
with open("SNN_lvs_ref.spice", "w") as f:
    f.write("* LVS reference for the SNN top-level layout (gen_snn.py), written by make_snn_lvs_ref.py.\n"
            "* Instances and nets as in analog/snn/snn_analog_inh.sch (xschem netlist), with these\n"
            "* layout-only changes:\n"
            "*   - the six plain DACs are %s%s; DAC_signed contains the binary DAC\n"
            "*   - every block is its layout cell; the subcircuits below are copied from the blocks'\n"
            "*     own LVS references (*_lvs_ref.spice: dummies, MIM caps, substrate / DNWELL ports)\n"
            "*   - the blocks' GND (DACs, DAC_signed, DPI_inh) and the substrate are the top-level VSS\n"
            % (DAC, " (weights 1:2:4:8, not the schematic's 1:2:3:4 DAC.sym)" if DAC == "DAC_binary" else ""))
    for k in ("neuron_sized", "DPI", DAC, "DAC_signed", "DPI_sized", "DPI_inh"):
        if k in lib:
            f.write("\n" + "".join(lib[k]))
    f.write("\n.subckt SNN " + " ".join(pins) + "\n" + "\n".join(L) + "\n.ends\n")
print("wrote SNN_lvs_ref.spice (plain DACs: %s)" % DAC)
