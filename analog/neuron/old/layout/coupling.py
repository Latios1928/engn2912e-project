"""
Geometric coupling report for one net, from the LVS database (no parasitic extraction).

    klayout -b -r coupling.py -rd gds=<layout.gds> -rd net=VMEM -rd out=report.txt   (env LVSDB=<file.lvsdb>)

For every other net it reports:
  * overlap  : plan-view area where the other net crosses the target on a different
               conductor layer, split into adjacent layers (e.g. M1-M2) and farther ones;
  * side-run : length of target edges that face the other net on the same layer
               within 1.0 um.
Nets are named with the schematic names from the LVS cross-reference. VSS/VDD are
listed separately (they shield; they do not inject signal). GND counts as a supply.
These are geometry numbers, not capacitances.
"""
import os
import pya

TARGET = globals().get("net", "VMEM").upper()
OUT = globals().get("out", "")
GDS = globals().get("gds", "neuron_sized.gds")
NEAR = 1.0                                   # um, same-layer proximity window

lvs = pya.LayoutVsSchematic()
lvs.read(os.environ["LVSDB"])
ly = lvs.internal_layout()
dbu = ly.dbu
top = lvs.internal_top_cell()

# Identify the conductor layers of the extraction by comparing them with the drawn layers.
DRAWN = {"poly": (30, 0), "M1": (34, 0), "M2": (36, 0), "M3": (42, 0),
         "M4": (46, 0), "M5": (81, 0), "FuseTop": (75, 0)}
ORDER = ["poly", "M1", "M2", "M3", "M4", "FuseTop", "M5"]
src = pya.Layout()
src.read(GDS)
stop = src.top_cell()
assert abs(src.dbu - dbu) < 1e-9
drawn = {}
for name, (l, d) in DRAWN.items():
    li = src.find_layer(l, d)
    drawn[name] = pya.Region(stop.begin_shapes_rec(li)).merged() if li is not None else pya.Region()
circ = lvs.netlist().top_circuit()
all_nets = list(circ.each_net())

# Several extraction layers can be geometric copies of one drawn layer (raw input,
# "_con" layer, cap sub-layers). Keep the copy whose shapes are owned by nets.
cands = {name: [] for name in drawn}
for i in lvs.layer_indexes():
    r = lvs.layer_by_index(i).merged()
    if r.is_empty():
        continue
    for name, ref in drawn.items():
        if ref.is_empty():
            continue
        if (r ^ ref).area() <= 0.002 * ref.area():
            cands[name].append(i)
cond = {name: idxs for name, idxs in cands.items() if idxs}
missing = [n for n in ORDER if n not in cond and not drawn[n].is_empty()]
assert not missing, "could not identify layers: %s" % missing

# schematic names for layout nets
xref = lvs.xref()
names = {}
for cp in xref.each_circuit_pair():
    for np_ in xref.each_net_pair(cp):
        if np_.first() and np_.second():
            names[np_.first().cluster_id] = np_.second().name



def shapes(net):
    """Union over every extraction copy of each drawn layer."""
    out = {}
    for ln, idxs in cond.items():
        r = pya.Region()
        for i in idxs:
            r += lvs.shapes_of_net(net, lvs.layer_by_index(i), True)
        out[ln] = r.merged()
    return out


nets = {}
for n in circ.each_net():
    if n.terminal_count() + n.pin_count() == 0 and n.cluster_id not in names:
        continue                      # dangling copy-layer artefact: no devices, no pins
    nm = names.get(n.cluster_id, n.expanded_name()).upper()
    nets[nm] = shapes(n)
assert TARGET in nets, "net %s not found (%s)" % (TARGET, sorted(nets))
T = nets[TARGET]

rows = []
for nm, S in nets.items():
    if nm == TARGET:
        continue
    adj, far, side = 0.0, 0.0, 0.0
    detail = []
    for a in ORDER:
        if a not in T or T[a].is_empty():
            continue
        for b in ORDER:
            if b not in S or S[b].is_empty():
                continue
            if a == b:
                ep = T[a].separation_check(S[b], int(NEAR / dbu))
                ln = sum(e.first.length() for e in ep.each()) * dbu
                if ln > 0:
                    side += ln
                    detail.append("%s side %.2f um" % (a, ln))
            else:
                ar = (T[a] & S[b]).area() * dbu * dbu
                if ar > 0:
                    if abs(ORDER.index(a) - ORDER.index(b)) == 1:
                        adj += ar
                    else:
                        far += ar
                    detail.append("%s/%s %.3f um2" % (a, b, ar))
    if adj or far or side:
        rows.append((nm, adj, far, side, detail))

supplies = [r for r in rows if r[0] in ("VSS", "VDD", "GND")]
signals = sorted([r for r in rows if r[0] not in ("VSS", "VDD", "GND")], key=lambda r: -(r[1] + r[3]))

lines = ["Geometric coupling report for net %s  (window %.1f um; not a capacitance extraction)" % (TARGET, NEAR),
         "Target area per layer: " + ", ".join("%s %.1f um2" % (k, v.area() * dbu * dbu)
                                              for k, v in T.items() if not v.is_empty()),
         "",
         "%-10s %14s %14s %14s   %s" % ("net", "adj-overlap", "far-overlap", "side-run", "detail"),
         "%-10s %14s %14s %14s" % ("", "um2", "um2", "um"),
         "-- signals --"]
for (nm, a, f, s, d) in signals:
    lines.append("%-10s %14.3f %14.3f %14.2f   %s" % (nm, a, f, s, "; ".join(d)))
if not signals:
    lines.append("(none)")
lines.append("-- supplies (shields) --")
for (nm, a, f, s, d) in supplies:
    lines.append("%-10s %14.3f %14.3f %14.2f   %s" % (nm, a, f, s, "; ".join(d)))
txt = "\n".join(lines)
print(txt)
if OUT:
    with open(OUT, "w") as fh:
        fh.write(txt + "\n")
