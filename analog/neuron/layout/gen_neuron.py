"""
neuron_sized layout generator for GF180MCU (gf180mcuD, variant D: 5LM, MIM-B M4-M5).

Run inside the iic-osic-tools container:
    klayout -b -r gen_neuron.py -rd out=neuron_sized.gds

Circuit: analog/neuron/neuron_sized.sch (+ spike_amplifier.sch, flattened as A1..A5).

Revision 2 (user feedback on revision 1):
  * Dummy rings: the subthreshold / matching-critical devices (NMOS A1 A2 A3 M7 M8 M10 M11,
    PMOS A4 A5 M9 M12) sit in a row that has an identical dummy directly above and below
    every device, plus end dummies, so each critical device is surrounded on all sides.
    The diff pair and the mirror also have flank dummies inside the row. The switching
    devices (M1..M6) sit outside the rings.
  * No long parallel M1 runs next to switching nets: spike, net1 and net2 each get their own
    channel track with a grounded M1 shield track on both sides (VSS below, VDD above).
    The spike-gated reset device M6 now sits next to M1/M2, so spike stays short.
    The DC bias lines (Vlk, VK, VT, Vamp_bias, VIp, VKdn, VNA, VKup) stay packed together.

Kept from revision 1:
  * VMEM never uses the shared channel: an M2 bus inside the NMOS guard ring (below the
    bottom dummy row) and one inside the PMOS guard ring (above the top dummy row), joined
    through the left margin on Metal5 (the C2 top plate).
  * One DNWELL (VDD); NMOS in an LVPWELL (VSS), PMOS in an NWELL (VDD).
  * Guard rings: P+ around the NMOS (VSS), N+ around the PMOS (VDD), P+ substrate ring (VSS).
  * C2 (VMEM) and C1 (spike) over the transistors on one shared VSS bottom plate.
  * Under the caps only M1, M2 and Via1 (the PDK LVS deck ignores Via2/Via3 under FuseTop).
"""
import sys
import pya

sys.path.insert(0, "/foss/pdks/gf180mcuD/libs.tech/klayout/tech/pymacros")
import cells  # noqa: E402
from cells.draw_fet import draw_nfet, draw_pfet  # noqa: E402

cells.gf180mcu()
OUT = globals().get("out", "neuron_sized.gds")

# ------------------------------------------------------------------ layers
L = {
    "dnwell": (12, 0), "nwell": (21, 0), "comp": (22, 0), "poly": (30, 0),
    "pplus": (31, 0), "nplus": (32, 0), "cont": (33, 0), "m1": (34, 0),
    "via1": (35, 0), "m2": (36, 0), "via2": (38, 0), "m3": (42, 0),
    "via3": (40, 0), "m4": (46, 0), "via4": (41, 0), "m5": (81, 0),
    "lvpwell": (204, 0), "bnd": (0, 0),
    "m1_lbl": (34, 10), "m2_lbl": (36, 10),
}
ly = pya.Layout()
ly.dbu = 0.001
top = ly.create_cell("neuron_sized")
li = {k: ly.layer(*v) for k, v in L.items()}


def box(layer, x1, y1, x2, y2):
    top.shapes(li[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def sq(layer, cx, cy, s):
    box(layer, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)


VIA = 0.26
PAD = {"m1": 0.40, "m2": 0.40, "m3": 0.40, "m4": 0.40, "m5": 0.46}


_vias = {}


def via_stack(cx, cy, lo, hi):
    """Stacked vias; a via that would land on (almost) the same spot as an existing one of
    the same layer is merged into it (same-net stubs ending in one place)."""
    for m in range(lo, hi + 1):
        sq("m%d" % m, cx, cy, PAD["m%d" % m])
    for v in range(lo, hi):
        lst = _vias.setdefault(v, [])
        if any(abs(cx - x) < 0.52 and abs(cy - y) < 0.52 for (x, y) in lst):
            continue
        lst.append((cx, cy))
        sq("via%d" % v, cx, cy, VIA)


def contacts(x1, y1, x2, y2, pitch=0.5):
    if (x2 - x1) >= (y2 - y1):
        n = int((x2 - x1 - 0.22) / pitch) + 1
        x0 = (x1 + x2) / 2 - (n - 1) * pitch / 2
        for i in range(n):
            sq("cont", x0 + i * pitch, (y1 + y2) / 2, 0.22)
    else:
        n = int((y2 - y1 - 0.22) / pitch) + 1
        y0 = (y1 + y2) / 2 - (n - 1) * pitch / 2
        for i in range(n):
            sq("cont", (x1 + x2) / 2, y0 + i * pitch, 0.22)


def ring(x1, y1, x2, y2, w, implant):
    """Guard ring: COMP + implant + M1 + contacts; (x1,y1,x2,y2) is the outer edge."""
    sides = [(x1, y1, x2, y1 + w), (x1, y2 - w, x2, y2),
             (x1, y1 + w, x1 + w, y2 - w), (x2 - w, y1 + w, x2, y2 - w)]
    for s in sides:
        box("comp", *s)
        box("m1", *s)
        box(implant, s[0] - 0.16, s[1] - 0.16, s[2] + 0.16, s[3] + 0.16)
    contacts(*sides[0])
    contacts(*sides[1])
    for s in sides[2:]:                          # keep side contacts clear of the corners
        contacts(s[0], s[1] + 0.3, s[2], s[3] - 0.3)
    return sides


# ------------------------------------------------------------------ devices
def make_fet(kind, w, l, gate_pos):
    fn = draw_nfet if kind == "n" else draw_pfet
    c = fn(ly, l_gate=l, w_gate=w, nf=1, con_bet_fin=0 if w < 0.36 else 1,
           gate_con_pos=gate_pos, bulk="None")
    c.flatten(True)
    if kind == "p":
        c.shapes(li["nwell"]).clear()
    for k in li:                                  # snap to the 5 nm grid
        r = pya.Region(c.shapes(li[k]))
        if not r.is_empty():
            c.shapes(li[k]).clear()
            c.shapes(li[k]).insert(r.snapped(5, 5))
    pads = [s.dbbox() for s in c.shapes(li["m1"]).each()]
    mid = w / 2
    sd = sorted([p for p in pads if p.bottom < mid < p.top], key=lambda b: b.center().x)
    gp = sorted([p for p in pads if not (p.bottom < mid < p.top)], key=lambda b: b.center().y)
    assert len(sd) == 2 and gp, (kind, w, l, pads)
    core = pya.Region()
    for k in ("comp", "poly", "m1"):
        core += pya.Region(c.shapes(li[k]))
    return c, sd, gp, core.bbox().to_dtype(ly.dbu)


_cache = {}


def fet(kind, w, l, gate_pos):
    key = (kind, w, l, gate_pos)
    if key not in _cache:
        _cache[key] = make_fet(*key)
    return _cache[key]


DOFF = 0.35          # S/D tab offset, keeps S/D M2 stubs clear of the gate M2 pad
DOFF_WIDE = 1.0      # wider tab on switching / amplifier S-D stubs: their vertical M2 stub
                     # then runs 1.14 um (edge to edge) from the gate stub instead of 0.35 um
WIDE = {"M1", "M2", "M3", "M4", "M5", "M6", "A1", "A2", "A5"}
RAILS = ("VSS", "VDD")


def doff(name, net):
    return DOFF_WIDE if name in WIDE and net not in RAILS else DOFF
GAP = 0.7            # horizontal gap between device extents
ROWGAP = 0.5         # vertical gap between the features of stacked rows


def extent(spec):
    """Left/right extent of a device (incl. tabs) relative to its origin, and its y range."""
    (name, kind, w, l, gpos, flip, s, g, d) = spec
    c, sd, gp, core = fet(kind, w, l, gpos)
    if flip:
        t = pya.DTrans(pya.DTrans.M90)
        sd = [p.transformed(t) for p in sd][::-1]
        core = core.transformed(t)
    net_l, net_r = (d, s) if flip else (s, d)
    left = min(core.left, sd[0].center().x - doff(name, net_l) - 0.2)
    right = max(core.right, sd[1].center().x + doff(name, net_r) + 0.2)
    return left, right, core.bottom - w / 2, core.top - w / 2   # y relative to S/D centre


def place_dev(spec, ox, row_y):
    """Place a device with its origin x at ox and its S/D centre line at row_y."""
    (name, kind, w, l, gpos, flip, s, g, d) = spec
    c, sd, gp, core = fet(kind, w, l, gpos)
    oy = row_y - w / 2
    trans = pya.DTrans(pya.DTrans.M90 if flip else pya.DTrans.R0, ox, oy)
    top.insert(pya.DCellInstArray(c.cell_index(), trans))
    sd_t = sorted([p.transformed(trans) for p in sd], key=lambda b: b.center().x)
    gp_t = sorted([p.transformed(trans) for p in gp], key=lambda b: b.center().y)
    return {"name": name, "kind": kind, "W": w, "L": l, "flip": flip,
            "S": sd_t[1] if flip else sd_t[0], "D": sd_t[0] if flip else sd_t[1],
            "S_side": "R" if flip else "L", "D_side": "L" if flip else "R",
            "gates": gp_t, "nets": {"S": s, "G": g, "D": d}, "ox": ox, "y": row_y,
            "core": core.transformed(trans)}


GAP_SW = 1.6         # wider gap between switch devices: keeps the vertical M2 stubs of
                     # neighbouring switches (e.g. net2 of M1 and spike of M2) > 1 um apart


def row_origins(specs, x0, gap=GAP):
    """Origin x of each device for a left-to-right row starting at x0."""
    xs, x = [], x0
    for spec in specs:
        left, right, _, _ = extent(spec)
        xs.append(x - left)
        x = x + (right - left) + gap
    return xs, x - gap


# name, kind, W, L, gate contact, flip (S on the right), S, G, D
# Critical rows: every entry gets an identical dummy directly above and below.
CRIT_N = [
    ("EN1", "n", 1.0, 1.0, "top", False, "VSS", "VSS", "VSS"),
    ("M11", "n", 1.0, 1.0, "top", False, "VSS", "Vlk", "VMEM"),
    ("M10", "n", 1.0, 1.0, "top", False, "VSS", "VK", "net6"),
    ("FN1", "n", 0.22, 0.28, "alternating", False, "VSS", "VSS", "VSS"),
    ("A1", "n", 0.22, 0.28, "alternating", True, "tail", "VMEM", "amp_n2"),
    ("A2", "n", 0.22, 0.28, "alternating", False, "tail", "VT", "net1"),
    ("FN2", "n", 0.22, 0.28, "alternating", False, "VSS", "VSS", "VSS"),
    ("A3", "n", 0.22, 0.28, "top", False, "VSS", "Vamp_bias", "tail"),
    ("M8", "n", 1.0, 1.0, "top", False, "VSS", "VIp", "net4"),
    ("M7", "n", 1.0, 1.0, "top", False, "VSS", "VKdn", "net5"),
    ("EN2", "n", 1.0, 1.0, "top", False, "VSS", "VSS", "VSS"),
]
NONC_N = [
    ("M1", "n", 0.22, 0.28, "top", False, "net4", "net1", "net2"),
    ("M2", "n", 0.22, 0.28, "top", True, "net5", "net2", "spike"),
    ("M6", "n", 0.22, 5.0, "top", False, "net6", "spike", "VMEM"),
]
CRIT_P = [
    ("EP1", "p", 1.0, 1.0, "bottom", False, "VDD", "VDD", "VDD"),
    ("M9", "p", 1.0, 1.0, "bottom", False, "VDD", "VNA", "net7"),
    ("FP1", "p", 0.22, 0.28, "alternating", False, "VDD", "VDD", "VDD"),
    ("A4", "p", 0.22, 0.28, "alternating", True, "VDD", "amp_n2", "amp_n2"),
    ("A5", "p", 0.22, 0.28, "alternating", False, "VDD", "amp_n2", "net1"),
    ("FP2", "p", 0.22, 0.28, "alternating", False, "VDD", "VDD", "VDD"),
    ("M12", "p", 1.0, 1.0, "bottom", False, "VDD", "VKup", "net3"),
    ("EP2", "p", 1.0, 1.0, "bottom", False, "VDD", "VDD", "VDD"),
]
NONC_P = [
    ("M3", "p", 0.22, 0.28, "bottom", False, "VDD", "net1", "net2"),
    ("M4", "p", 0.22, 0.28, "bottom", True, "net3", "net2", "spike"),
    ("M5", "p", 0.22, 0.28, "bottom", False, "net7", "net2", "VMEM"),
]
LINKS = [("A1", "S", "A2", "S"), ("A4", "S", "A5", "S")]
LEFT_PINS = ["Vlk", "VK", "VT", "Vamp_bias", "VIp", "VKdn", "VNA", "VKup"]
RIGHT_PINS = ["spike"]
AGGRESSORS = ["spike", "net1", "net2"]       # switching nets: shielded on both sides
RAIL = {"n": "VSS", "p": "VDD"}
VMEM_DOWN = [("M11", "D"), ("A1", "G"), ("M6", "D")]   # NMOS VMEM terminals -> lower bus
VMEM_UP = [("M5", "D")]                               # PMOS VMEM terminal  -> upper bus


def dummy_row(specs, tag, gate_pos):
    """Identical dummies (same kind/W/L/flip) for every entry of a critical row."""
    rail = RAIL[specs[0][1]]
    return [("%s_%s" % (tag, s[0]), s[1], s[2], s[3], gate_pos, s[5], rail, rail, rail)
            for s in specs]


def rel_y(specs):
    lo = min(extent(s)[2] for s in specs)
    hi = max(extent(s)[3] for s in specs)
    return lo, hi


def stack_pitch(lower, upper):
    """Centre-to-centre pitch so that the two rows (aligned entry by entry) clear by ROWGAP."""
    return max(extent(a)[3] - extent(b)[2] for a, b in zip(lower, upper)) + ROWGAP


# ------------------------------------------------------------------ x floorplan
OR_O, OR_W = 0.3, 0.5                       # outer substrate ring offset / width
STK_L = 2.2                                 # x of the VMEM via stacks (left margin)
ESC_L = 1.4                                 # left escape vias (M1 track -> M2 pin)
DN_X0 = 3.6                                 # DNWELL left edge
WELL_X0 = DN_X0 + 2.5                       # LVPWELL / NWELL left edge
RING_W = 0.5
RING_X0 = WELL_X0 + 0.4                     # row guard rings, outer edge
DEV_X0 = RING_X0 + RING_W + 1.0             # first device extent
RINGGAP = 1.6                               # gap between the dummy ring and the switch devices

xs_cn, x_cn_end = row_origins(CRIT_N, DEV_X0)
xs_nn, x_nn_end = row_origins(NONC_N, x_cn_end + RINGGAP, GAP_SW)
xs_cp, x_cp_end = row_origins(CRIT_P, DEV_X0)
xs_np, x_np_end = row_origins(NONC_P, max(x_cp_end, x_cn_end) + RINGGAP, GAP_SW)
X_END = max(x_nn_end, x_np_end)
RING_X1 = X_END + 1.0 + RING_W
WELL_X1 = RING_X1 + 0.4
DN_X1 = WELL_X1 + 2.5
CW = DN_X1 + 2.7 + OR_W + OR_O
ESC_R = CW - 1.4

# ------------------------------------------------------------------ NMOS block (y)
DN_Y0 = 3.6
NW_Y0 = DN_Y0 + 2.5                          # LVPWELL bottom
NR_Y0 = NW_Y0 + 0.4                          # NMOS ring outer bottom
NB_IN = NR_Y0 + RING_W                       # NMOS ring bottom side, inner edge
BUS_N = NB_IN + 0.7                          # VMEM bus (M2), under the bottom dummy row
BOT_N = dummy_row(CRIT_N, "DB", "bottom")
TOP_N = dummy_row(CRIT_N, "DT", "top")
y_nb = BUS_N + 0.6 - rel_y(BOT_N)[0]         # bottom dummy row
y_nc = y_nb + stack_pitch(BOT_N, CRIT_N)     # critical + switch row
y_nt = y_nc + stack_pitch(CRIT_N, TOP_N)     # top dummy row
NT_IN = max(y_nt + rel_y(TOP_N)[1], y_nc + rel_y(NONC_N)[1]) + 0.6   # ring top side, inner edge
CH_Y0 = NT_IN + RING_W + 0.9                 # first channel track

ndev = {}
for spec, ox in zip(BOT_N, xs_cn):
    ndev[spec[0]] = place_dev(spec, ox, y_nb)
for spec, ox in zip(CRIT_N, xs_cn):
    ndev[spec[0]] = place_dev(spec, ox, y_nc)
for spec, ox in zip(TOP_N, xs_cn):
    ndev[spec[0]] = place_dev(spec, ox, y_nt)
for spec, ox in zip(NONC_N, xs_nn):
    ndev[spec[0]] = place_dev(spec, ox, y_nc)

# PMOS devices are placed after the channel is sized; their x is known already.
BOT_P = dummy_row(CRIT_P, "PB", "bottom")
TOP_P = dummy_row(CRIT_P, "PT", "top")


# ------------------------------------------------------------------ channel terminals
def tab_x(dev, t):
    p = dev[t]
    o = doff(dev["name"], dev["nets"][t])
    return p.center().x + (-o if dev[t + "_side"] == "L" else o)


def ghost(spec, ox):
    """Device dict at y = 0, used only for x positions."""
    global top
    keep = top
    top = ly.create_cell("_ghost")
    d = place_dev(spec, ox, 0.0)
    ly.delete_cell(top.cell_index())
    top = keep
    return d


pghost = {s[0]: ghost(s, ox) for s, ox in list(zip(CRIT_P, xs_cp)) + list(zip(NONC_P, xs_np))}

term = {}          # net -> list of (x, side, source)


def add_term(net, x, side, src):
    term.setdefault(net, []).append((x, side, src))


linked = set()
for (a, ta, b, tb) in LINKS:
    linked.add((a, ta))
    linked.add((b, tb))


def collect(devs, names, side):
    for nm in names:
        d = devs[nm]
        for t in ("S", "D", "G"):
            net = d["nets"][t]
            if net == RAIL[d["kind"]] or net == "VMEM":
                continue
            if (nm, t) in linked:
                continue
            if t == "G":
                g = d["gates"][-1] if side == "N" else d["gates"][0]
                add_term(net, g.center().x, side, ("G", nm))
            else:
                add_term(net, tab_x(d, t), side, (t, nm))


collect(ndev, [s[0] for s in CRIT_N + NONC_N], "N")
collect(pghost, [s[0] for s in CRIT_P + NONC_P], "P")
for (a, ta, b, tb) in LINKS:                       # link midpoint stub if the net goes elsewhere
    devs, side = (ndev, "N") if a in ndev else (pghost, "P")
    net = devs[a]["nets"][ta]
    if net != RAIL[devs[a]["kind"]]:
        pa, pb = devs[a][ta], devs[b][tb]
        add_term(net, (pa.right + pb.left) / 2, side, ("L", a, b))

# ------------------------------------------------------------------ channel assignment
TW, TP = 0.40, 0.80      # track width, pitch
COLW = 0.75              # two vertical M2 stubs closer than this conflict


def net_span(net):
    xs = [t[0] for t in term[net]]
    lo, hi = min(xs), max(xs)
    if net in LEFT_PINS:
        lo = ESC_L
    if net in RIGHT_PINS:
        hi = ESC_R
    return lo - 0.3, hi + 0.3


n_stub_x = [x for ts in term.values() for (x, s, _) in ts if s == "N"]
p_stub_x = [x for ts in term.values() for (x, s, _) in ts if s == "P"]
CH_XMIN, CH_XMAX = DEV_X0, X_END


def free_column(x_pref, avoid, direction):
    """Nearest x (stepping away from x_pref) at least COLW from every x in avoid."""
    x = x_pref
    for _ in range(400):
        if all(abs(x - a) >= COLW for a in avoid) and CH_XMIN <= x <= CH_XMAX:
            return x
        x += 0.05 * direction
    raise AssertionError("no free column near %.2f" % x_pref)


# items: list of dicts {name, nets: [(net, track offset)], height, span, stubs: [(x, side, offset)]}
items = []
for net in term:
    lo, hi = net_span(net)
    if net in AGGRESSORS:
        # lower shield drops to the NMOS ring (VSS), upper shield rises to the PMOS ring (VDD)
        # drop columns avoid every stub (N and P side): a drop that shares a column with
        # another net's stub would add a track-order constraint and can create a cycle
        all_x = n_stub_x + p_stub_x + [x for it_ in items for x in it_.get("drops", ())]
        xd_lo = free_column(lo - 0.6, all_x, -1) if lo - 0.6 >= CH_XMIN else free_column(lo, all_x, +1)
        xd_hi = free_column(min(hi + 0.6, CH_XMAX), all_x + [xd_lo], +1) if hi + 0.6 <= CH_XMAX \
            else free_column(CH_XMAX, all_x + [xd_lo], -1)
        lo2 = min(lo, xd_lo - 0.3)
        hi2 = max(hi, xd_hi + 0.3)
        stubs = [(x, s, 1) for (x, s, _) in term[net]] + [(xd_lo, "N", 0), (xd_hi, "P", 2)]
        items.append({"name": net, "height": 3, "span": (lo2 - 0.5, hi2 + 0.5),
                      "net_span": (lo, hi), "stubs": stubs, "drops": (xd_lo, xd_hi),
                      "shield_span": (lo2, hi2)})
    else:
        items.append({"name": net, "height": 1, "span": (lo, hi), "net_span": (lo, hi),
                      "stubs": [(x, s, 0) for (x, s, _) in term[net]]})

# constraints: an N stub (item a, offset oa) and a P stub (item b, offset ob) in the same
# column need track(a)+oa < track(b)+ob
cons = {it["name"]: [] for it in items}
for a in items:
    for b in items:
        if a is b:
            continue
        for (xa, sa, oa) in a["stubs"]:
            for (xb, sb, ob) in b["stubs"]:
                if sa == "N" and sb == "P" and abs(xa - xb) < COLW:
                    cons[b["name"]].append((a["name"], oa, ob))

occ = {}           # track -> list of (lo, hi)


def free(t, lo, hi):
    return all(hi + 0.6 <= a or lo >= b + 0.6 for (a, b) in occ.get(t, []))


base = {}
pending = sorted(items, key=lambda it: it["span"][0])
t = 0
while pending and t < 200:
    progressed = True
    while progressed:
        progressed = False
        for it in list(pending):
            req = 0
            ok = True
            for (pa, oa, ob) in cons[it["name"]]:
                if pa not in base:
                    ok = False
                    break
                req = max(req, base[pa] + oa - ob + 1)
            if not ok or t < req:
                continue
            lo, hi = it["span"]
            if all(free(t + k, lo, hi) for k in range(it["height"])):
                for k in range(it["height"]):
                    occ.setdefault(t + k, []).append((lo, hi))
                base[it["name"]] = t
                pending.remove(it)
                progressed = True
    t += 1
if pending:
    names = {it["name"] for it in pending}
    for it in pending:
        print("  ", it["name"], "waits on", sorted({(a, oa, ob, base.get(a)) for (a, oa, ob) in cons[it["name"]]
                                                 if a in names or a not in base}))
assert not pending, "channel assignment failed: %s" % [it["name"] for it in pending]
NTRK = max(base[it["name"]] + it["height"] for it in items)
TRK = {}
for it in items:
    TRK[it["name"]] = CH_Y0 + (base[it["name"]] + (1 if it["height"] == 3 else 0)) * TP
CH_Y1 = CH_Y0 + (NTRK - 1) * TP
print("channel: %d tracks" % NTRK)
for k in range(NTRK):
    print("  %5.2f" % (CH_Y0 + k * TP),
          [it["name"] + ("" if it["height"] == 1 else ("~shield" if base[it["name"]] != k - 1 else ""))
           for it in items if base[it["name"]] <= k < base[it["name"]] + it["height"]])

# ------------------------------------------------------------------ PMOS block (y)
PR_BOT = CH_Y1 + 0.9                         # PMOS ring bottom side, outer edge
PB_IN = PR_BOT + RING_W
y_pb = PB_IN + 0.6 - rel_y(BOT_P)[0]
y_pc = y_pb + stack_pitch(BOT_P, CRIT_P)
y_pc = max(y_pc, PB_IN + 0.6 - rel_y(NONC_P)[0])
y_pt = y_pc + stack_pitch(CRIT_P, TOP_P)
BUS_P = max(y_pt + rel_y(TOP_P)[1], y_pc + rel_y(NONC_P)[1]) + 0.7
PT_IN = BUS_P + 0.7                          # PMOS ring top side, inner edge
NWL_Y1 = PT_IN + RING_W + 0.4
DN_Y1 = NWL_Y1 + 2.5
CH = DN_Y1 + 2.7 + OR_W + OR_O

pdev = {}
for spec, ox in zip(BOT_P, xs_cp):
    pdev[spec[0]] = place_dev(spec, ox, y_pb)
for spec, ox in zip(CRIT_P, xs_cp):
    pdev[spec[0]] = place_dev(spec, ox, y_pc)
for spec, ox in zip(TOP_P, xs_cp):
    pdev[spec[0]] = place_dev(spec, ox, y_pt)
for spec, ox in zip(NONC_P, xs_np):
    pdev[spec[0]] = place_dev(spec, ox, y_pc)

# ------------------------------------------------------------------ wells + rings
box("dnwell", DN_X0, DN_Y0, DN_X1, DN_Y1)
box("lvpwell", WELL_X0, NW_Y0, WELL_X1, NT_IN + RING_W + 0.4)
ring(RING_X0, NR_Y0, RING_X1, NT_IN + RING_W, RING_W, "pplus")
box("nwell", WELL_X0, PR_BOT - 0.4, WELL_X1, NWL_Y1)
ring(RING_X0, PR_BOT, RING_X1, PT_IN + RING_W, RING_W, "nplus")
ring(OR_O, OR_O, CW - OR_O, CH - OR_O, OR_W, "pplus")
for xs in (RING_X0 + 2.0, (RING_X0 + RING_X1) / 2, RING_X1 - 2.0):   # NMOS ring -> substrate ring
    box("m1", xs - 0.5, OR_O + OR_W - 0.01, xs + 0.5, NR_Y0 + 0.01)
NT_C = NT_IN + RING_W / 2                    # centre line of the NMOS ring top side
PB_C = PR_BOT + RING_W / 2                   # centre line of the PMOS ring bottom side


# ------------------------------------------------------------------ device wiring
def tab(dev, t):
    """M1 tab outward from a S/D pad; returns the tab x."""
    p = dev[t]
    x = tab_x(dev, t)
    if dev[t + "_side"] == "L":
        box("m1", x - 0.2, p.bottom, p.right, p.top)
    else:
        box("m1", p.left, p.bottom, x + 0.2, p.top)
    return x


def vbar(x, y1, y2):
    box("m1", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def stub(x, y0, y1):
    via_stack(x, y0, 1, 2)
    box("m2", x - 0.2, min(y0, y1) - 0.2, x + 0.2, max(y0, y1) + 0.2)
    via_stack(x, y1, 1, 2)


def gate_tie(d, side_up):
    """Tie a dummy's gate pad to its S tab: a solid block over the S pad column up to the
    gate pad height, then a strip at gate-pad height across to the gate pad. The S pad
    column keeps the PDK pad outline towards the second (unused) gate contact."""
    g = d["gates"][-1] if side_up else d["gates"][0]
    s = d["S"]
    xt = tab_x(d, "S")
    gx = g.center().x
    if d["S_side"] == "L":
        cx1, cx2, sx1, sx2 = xt - 0.2, s.right, s.right - 0.01, gx
    else:
        cx1, cx2, sx1, sx2 = s.left, xt + 0.2, gx, s.left + 0.01
    if side_up:
        box("m1", cx1, s.bottom, cx2, g.top)
    else:
        box("m1", cx1, g.bottom, cx2, s.top)
    box("m1", sx1, g.bottom, sx2, g.top)


def wire_block(devs, crit, bot, topr, nonc, kind):
    rail = RAIL[kind]
    up_in = NT_IN if kind == "n" else PT_IN          # ring side above the block (inner edge)
    lo_in = NB_IN if kind == "n" else PB_IN          # ring side below the block (inner edge)
    # top dummy row: everything up to the ring above
    for s in topr:
        d = devs[s[0]]
        for t in ("S", "D"):
            vbar(tab(d, t), d[t].center().y, up_in + 0.01)
        g = d["gates"][-1]
        box("m1", g.left, g.bottom, g.right, up_in + 0.01)
    # bottom dummy row: everything down to the ring below
    for s in bot:
        d = devs[s[0]]
        for t in ("S", "D"):
            vbar(tab(d, t), lo_in - 0.01, d[t].center().y)
        g = d["gates"][0]
        box("m1", g.left, lo_in - 0.01, g.right, g.top)
    # critical row: rail terminals join the dummy directly above (same x, same tab)
    for s, sa in zip(crit, topr):
        d, da = devs[s[0]], devs[sa[0]]
        for t in ("S", "D"):
            if d["nets"][t] == rail:
                vbar(tab(d, t), d[t].center().y, da[t].center().y)
        if d["nets"]["G"] == rail:                   # dummies inside the critical row
            gate_tie(d, kind == "n")
    # switch devices: rail terminals strap straight to the ring away from the channel
    for s in nonc:
        d = devs[s[0]]
        for t in ("S", "D"):
            if d["nets"][t] == rail:
                if kind == "n":
                    vbar(tab(d, t), lo_in - 0.01, d[t].center().y)
                else:
                    vbar(tab(d, t), d[t].center().y, up_in + 0.01)


wire_block(ndev, CRIT_N, BOT_N, TOP_N, NONC_N, "n")
wire_block(pdev, CRIT_P, BOT_P, TOP_P, NONC_P, "p")

LINK_X = {}
for (a, ta, b, tb) in LINKS:
    devs = ndev if a in ndev else pdev
    pa, pb = devs[a][ta], devs[b][tb]
    box("m1", pa.right - 0.01, min(pa.bottom, pb.bottom), pb.left + 0.01, max(pa.top, pb.top))
    LINK_X[(a, b)] = ((pa.right + pb.left) / 2, (pa.center().y + pb.center().y) / 2)

# channel stubs + tracks
for it in items:
    net = it["name"]
    y = TRK[net]
    for (x, side, src) in term[net]:
        devs = ndev if side == "N" else pdev
        if src[0] == "G":
            d = devs[src[1]]
            g = d["gates"][-1] if side == "N" else d["gates"][0]
            stub(g.center().x, g.center().y, y)
        elif src[0] in ("S", "D"):
            d = devs[src[1]]
            stub(tab(d, src[0]), d[src[0]].center().y, y)
        else:
            xm, ym = LINK_X[(src[1], src[2])]
            stub(xm, ym, y)
    # same-net stubs that land close together on the track: bridge them on M2
    xs_net = sorted(x for (x, _, _) in term[net])
    for xa, xb in zip(xs_net, xs_net[1:]):
        if 0 < xb - xa < 0.9:
            box("m2", xa - 0.2, y - 0.2, xb + 0.2, y + 0.2)
    lo, hi = it["net_span"]
    box("m1", lo, y - TW / 2, hi, y + TW / 2)
    if it["height"] == 3:                            # shields
        s_lo, s_hi = it["shield_span"]
        box("m1", s_lo, y - TP - TW / 2, s_hi, y - TP + TW / 2)      # VSS shield below
        box("m1", s_lo, y + TP - TW / 2, s_hi, y + TP + TW / 2)      # VDD shield above
        xd_lo, xd_hi = it["drops"]
        stub(xd_lo, NT_C, y - TP)
        stub(xd_hi, PB_C, y + TP)
    if net in LEFT_PINS:
        via_stack(ESC_L, y, 1, 2)
        box("m2", 0.0, y - 0.2, ESC_L, y + 0.2)
    if net in RIGHT_PINS:
        via_stack(ESC_R, y, 1, 2)
        box("m2", ESC_R, y - 0.2, CW, y + 0.2)

# ------------------------------------------------------------------ VMEM buses
for (nm, t) in VMEM_DOWN:
    d = ndev[nm]
    if t == "G":
        g = d["gates"][0]
        x, y = g.center().x, g.center().y
    else:
        x, y = tab(d, t), d[t].center().y
    via_stack(x, y, 1, 2)
    box("m2", x - 0.2, BUS_N - 0.2, x + 0.2, y + 0.2)
x_bus_n = max(tab_x(ndev[nm], t) if t != "G" else ndev[nm]["gates"][0].center().x for nm, t in VMEM_DOWN)
box("m2", STK_L - 0.2, BUS_N - 0.2, x_bus_n + 0.2, BUS_N + 0.2)
via_stack(STK_L, BUS_N, 2, 5)
for (nm, t) in VMEM_UP:
    d = pdev[nm]
    x, y = tab(d, t), d[t].center().y
    via_stack(x, y, 1, 2)
    box("m2", x - 0.2, y - 0.2, x + 0.2, BUS_P + 0.2)
    box("m2", STK_L - 0.2, BUS_P - 0.2, x + 0.2, BUS_P + 0.2)
via_stack(STK_L, BUS_P, 2, 5)
box("m5", STK_L - 0.25, BUS_N - 0.25, STK_L + 0.25, BUS_P + 0.25)      # Metal5 spine
box("m2", 0.0, BUS_N - 0.25, STK_L, BUS_N + 0.25)                    # VMEM pin

# ------------------------------------------------------------------ MIM caps
C2W, C1W = 22.18, 10.0
CAPGAP = 2.0
BP_X0 = STK_L + 0.25 + 1.25
FT2_X0 = BP_X0 + 0.6
FT1_X0 = FT2_X0 + C2W + CAPGAP
BP_X1 = FT1_X0 + C1W + 0.6
YC = (CH_Y0 + CH_Y1) / 2
FT2_Y0 = max(OR_O + OR_W + 1.0, YC - C2W / 2)
FT1_Y0 = min(max(OR_O + OR_W + 1.0, TRK["spike"] - C1W / 2), CH - OR_O - OR_W - 3.0 - C1W)
BP_Y0 = min(FT2_Y0, FT1_Y0) - 0.6
BP_Y1 = max(FT2_Y0 + C2W, FT1_Y0 + C1W) + 0.6
assert BP_Y1 < CH - OR_O - OR_W - 0.5, "cap too tall for the cell"


def mim(x0, y0, size):
    c = ly.create_cell("cap_mim", "gf180mcu",
                       {"mim_option": "MIM-B", "metal_level": "M5", "wc": size, "lc": size})
    top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans(x0, y0)))


mim(FT2_X0, FT2_Y0, C2W)
mim(FT1_X0, FT1_Y0, C1W)
box("m4", BP_X0, BP_Y0, BP_X1, BP_Y1)

VSX = FT2_X0 + C2W + CAPGAP / 2                    # VSS via4 strip between the caps
box("m5", VSX - 0.25, BP_Y0 + 0.6, VSX + 0.25, BP_Y1 - 0.1)
yv = BP_Y0 + 1.0
while yv < BP_Y1 - 0.6:
    sq("via4", VSX, yv, VIA)
    yv += 1.0
VSY = FT1_Y0 + C1W + 0.6 + 0.25 + 0.05
assert VSY + 0.25 < BP_Y1 - 0.1
STK_VSS_X = CW - OR_O - OR_W / 2
box("m5", VSX - 0.25, VSY - 0.25, STK_VSS_X + 0.25, VSY + 0.25)
via_stack(STK_VSS_X, VSY, 1, 5)
box("m5", STK_L - 0.25, YC - 0.25, FT2_X0 + 1.0, YC + 0.25)   # C2 top plate -> VMEM spine

# C1 top plate (spike) -> stack on the spike track, right of the bottom plate
ys = TRK["spike"]
assert FT1_Y0 + 0.5 < ys < FT1_Y0 + C1W - 0.5, "spike track not beside C1"
crossing = [x for it in items for (x, s, o) in it["stubs"]]   # incl. spike's own stubs
lo_sp, hi_sp = [it for it in items if it["name"] == "spike"][0]["net_span"]
STK_SP = max(BP_X1 + 1.5, lo_sp + 0.5)            # outside the plate, on the spike track
while any(abs(STK_SP - x) < COLW for x in crossing):
    STK_SP += 0.05
assert lo_sp < STK_SP < hi_sp
via_stack(STK_SP, ys, 1, 5)
box("m5", FT1_X0 + C1W - 1.0, ys - 0.25, STK_SP + 0.25, ys + 0.25)

# ------------------------------------------------------------------ pins
PIN = 0.6


def pin(name, layer, x1, y1, x2, y2):
    box(layer, x1, y1, x2, y2)
    top.shapes(li[layer + "_lbl"]).insert(pya.DText(name, pya.DTrans((x1 + x2) / 2, (y1 + y2) / 2)))


for n in LEFT_PINS:
    pin(n, "m2", 0.0, TRK[n] - 0.2, PIN, TRK[n] + 0.2)
pin("VMEM", "m2", 0.0, BUS_N - 0.25, PIN, BUS_N + 0.25)
pin("spike", "m2", CW - PIN, TRK["spike"] - 0.2, CW, TRK["spike"] + 0.2)
yvdd = (PR_BOT + PT_IN + RING_W) / 2
via_stack(RING_X1 - RING_W / 2, yvdd, 1, 2)
box("m2", RING_X1 - RING_W / 2, yvdd - 0.25, CW, yvdd + 0.25)
pin("VDD", "m2", CW - PIN, yvdd - 0.25, CW, yvdd + 0.25)
yvss = (NR_Y0 + NT_IN + RING_W) / 2
via_stack(CW - OR_O - OR_W / 2, yvss, 1, 2)
pin("VSS", "m2", CW - PIN, yvss - 0.25, CW, yvss + 0.25)
top.shapes(li["m1_lbl"]).insert(pya.DText("VSS", pya.DTrans(CW / 2, OR_O + OR_W / 2)))

box("bnd", 0, 0, CW, CH)
top.flatten(-1, True)
ly.write(OUT)
print("wrote %s  %.2f x %.2f um" % (OUT, CW, CH))
