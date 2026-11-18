import pya, os
db = pya.LayoutVsSchematic()
db.read(os.environ["LVSDB"])
xref = db.xref()
for cp in xref.each_circuit_pair():
    print("circuit", cp.first().name if cp.first() else None, cp.second().name if cp.second() else None, cp.status())
    for n in xref.each_net_pair(cp):
        if str(n.status()) != "Match":
            print("  net", n.first().expanded_name() if n.first() else None, "|", n.second().expanded_name() if n.second() else None, n.status())
    for d in xref.each_device_pair(cp):
        if str(d.status()) != "Match":
            print("  dev", d.first().expanded_name() if d.first() else None, d.first().device_class().name if d.first() else "", "|", d.second().expanded_name() if d.second() else None, d.second().device_class().name if d.second() else "", d.status())
    for p in xref.each_pin_pair(cp):
        if str(p.status()) != "Match":
            print("  pin", p.first().expanded_name() if p.first() else None, "|", p.second().expanded_name() if p.second() else None, p.status())
