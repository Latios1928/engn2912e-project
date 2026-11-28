"""
Top-level layout flow: assemble the analog SNN macro from signed-off blocks, stage by stage
(design: TOPLEVEL_FLOW.md, settings: top_flow.yaml). Same style as flow.py: every stage reads
and writes files under top/<top>/, prints one short status, writes <stage>.json, and refuses to
run if the stage before it has not passed.

    T="env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/layout_tools/top.py"
    $T status   SNN_signed      # what exists, what passed
    $T netlist  SNN_signed      # xschem netlist -> instances, pins -> nets, macro pins
    $T abstract SNN_signed      # per block: bbox, edge pins, LVS ref, signoff state
    $T plan     SNN_signed      # rows (one per neuron) found from the netlist graph
    $T place    SNN_signed      # coordinates, channel widths from routing demand
    $T route    SNN_signed      # route (channels grow on failure) -> GDS, LVS ref
    $T signoff  SNN_signed      # real KLayout DRC + LVS
    $T run      SNN_signed      # all of the above

Stages and their files (top/<top>/):
    netlist   netlist.json
    abstract  abstracts/<cell>.json, abstracts/<cell>_nolabels.gds
    plan      plan.json
    place     placement.json
    route     <top>.gds, <top>_lvs_ref.spice, route.json (+ sensitive-net report)
    signoff   drc/ lvs/ signoff.json
Not implemented yet (TOPLEVEL_FLOW.md): sim, PEX, supply styles other than "routed".
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CONF = HERE / "top_flow.yaml"
TOPDIR = HERE / "top"
REPO = HERE.parents[1]

import flow                                                         # noqa: E402  (FLOW, TECH, login)

ROW_KINDS = ("dac", "dpi", "neuron")


# ----------------------------------------------------------------------------- helpers
def conf() -> dict:
    import yaml
    return yaml.safe_load(CONF.read_text())


def tdir(top: str) -> Path:
    d = TOPDIR / top
    d.mkdir(parents=True, exist_ok=True)
    return d


def save(top: str, stage: str, data: dict) -> dict:
    data = {"stage": stage, "top": top, "time": time.strftime("%Y-%m-%d %H:%M:%S"), **data}
    (tdir(top) / f"{stage}.json").write_text(json.dumps(data, indent=1, default=str))
    return data


def load(top: str, stage: str) -> dict | None:
    f = TOPDIR / top / f"{stage}.json"
    return json.loads(f.read_text()) if f.exists() else None


def need(top: str, stage: str) -> dict:
    d = load(top, stage)
    if not d or not d.get("ok"):
        raise SystemExit(f"blocked: stage '{stage}' has not passed for {top} "
                         f"(run: top.py {stage} {top}; status: top.py status {top})")
    return d


def check_top(top: str) -> dict:
    c = conf()
    if c["top"]["name"] != top:
        raise SystemExit(f"error: top_flow.yaml describes {c['top']['name']}, not {top}")
    return c


def expand(name: str) -> list[str]:
    """'w[31:0]' -> ['w[31]', ..., 'w[0]']; anything else -> [name]."""
    m = re.fullmatch(r"(.+)\[(\d+):(\d+)\]", name)
    if not m:
        return [name]
    b, hi, lo = m.group(1), int(m.group(2)), int(m.group(3))
    step = -1 if hi >= lo else 1
    return [f"{b}[{i}]" for i in range(hi, lo + step, step)]


def glob_re(pat: str) -> re.Pattern:
    """Net-name pattern where only '*' is a wildcard (brackets are literal: spike[*])."""
    return re.compile("^" + re.escape(pat).replace(r"\*", ".*") + "$")


def kind_of(cell: str) -> str:
    c = cell.lower()
    if c.startswith("dac"):
        return "dac"
    if c.startswith("dpi_inh"):
        return "dpi_inh"
    if c.startswith("dpi"):
        return "dpi"
    if c.startswith("neuron"):
        return "neuron"
    if c.startswith("bias") or c.startswith("trim"):     # bias cell and the generator above it
        return "bias"
    return "other"


# ----------------------------------------------------------------------------- netlist
def _spice_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        if raw.startswith("+") and out:
            out[-1] += " " + raw[1:].strip()
        else:
            out.append(raw.rstrip())
    return out


def _netlist_sch(sch: Path) -> str:
    out = Path(tempfile.mkdtemp())
    rc = REPO / "xschemrc"
    flow.login(f"xschem -q -x -n -s -o {out} --rcfile {rc} {sch.name} > /dev/null 2>&1", sch.parent, timeout=300)
    f = out / (sch.stem + ".spice")
    if not f.exists():
        raise SystemExit(f"error: xschem wrote no netlist for {sch}")
    return f.read_text()


def st_netlist(top):
    c = check_top(top)
    sch = (HERE / c["top"]["schematic"]).resolve()
    text = _netlist_sch(sch)
    if "IS MISSING" in text:
        miss = sorted(set(re.findall(r"\*\s+(\S+) -\s+(\S+)\s+IS MISSING", text)))
        raise SystemExit(f"error: xschem could not find symbols {miss} (xschemrc library path?)")
    alias = {str(k): v for k, v in (c.get("net_alias") or {}).items()}
    a = lambda n: alias.get(n, n)                                   # noqa: E731
    # top pins: "**.subckt <name> pins" + "*+ ..." comment lines (buses comma-separated)
    head, top_pins = False, []
    for line in text.splitlines():
        if line.startswith("**.subckt"):
            head = True
            top_pins += re.split(r"[ ,]+", line.split(None, 2)[2]) if len(line.split()) > 2 else []
        elif head and line.startswith("*+"):
            top_pins += re.split(r"[ ,]+", line[2:].strip())
        elif head:
            break
    top_pins = [a(p) for p in top_pins if p]
    lines = _spice_lines(text)
    subckt = {}
    for ln in lines:
        t = ln.split()
        if t and t[0].lower() == ".subckt":
            subckt[t[1]] = t[2:]
    first_sub = next(i for i, ln in enumerate(lines) if ln.lower().startswith(".subckt"))
    raw_inst = [ln.split() for ln in lines[:first_sub] if ln[:1].lower() == "x"]
    blocks = c["blocks"]
    problems, insts = [], {}
    for t in raw_inst:
        name, nets, sym = t[0], t[1:-1], t[-1]
        if sym not in blocks:
            problems.append(f"{name}: symbol {sym} has no entry in top_flow.yaml blocks:")
            continue
        pins = subckt.get(sym)
        if pins is None or len(pins) != len(nets):
            problems.append(f"{name}: subckt {sym} pins {pins} vs {len(nets)} nets")
            continue
        m = {p: a(n) for p, n in zip(pins, nets)}
        for rail in ("VSS", "VDD"):              # layout supply pins the symbol may not have
            m.setdefault(rail, rail)
        insts[name] = dict(symbol=sym, cell=blocks[sym].get("cell", sym), source=blocks[sym]["source"], nets=m)
    # extra instances (bias cell): its outputs replace top pins with internal nets
    ports = list(top_pins)
    for name, e in (c.get("extra_instances") or {}).items():
        blk = e["block"]
        if blk not in blocks:
            problems.append(f"{name}: block {blk} not in blocks:")
            continue
        m = {}
        for o in e.get("outputs", []):
            if o not in ports:
                problems.append(f"{name}: output {o} is not a top pin of the schematic")
            ports = [p for p in ports if p != o]
            m[o] = o
        for i in e.get("inputs", []):
            m[i] = i
            if i not in ports:
                ports.append(i)
        for u in e.get("unused_outputs", []):
            m[u] = f"{name}_{u}_nc"
        for p, net in (e.get("nets") or {}).items():      # internal nets between extra instances
            if net in ports:
                problems.append(f"{name}: internal net {net} is also a macro pin")
            m[p] = net
        for rail in ("VSS", "VDD"):
            m.setdefault(rail, rail)
        insts[name] = dict(symbol=blk, cell=blocks[blk].get("cell", blk), source=blocks[blk]["source"],
                           nets=m, extra=True)
    # macro pin order
    order = []
    for p in (c.get("macro_pins") or {}).get("order", []):
        order += expand(p)
    unknown = [p for p in order if p not in ports]
    if unknown:
        problems.append(f"macro_pins.order names nets that are not macro pins: {unknown}")
    ports = [p for p in order if p in ports] + [p for p in ports if p not in order]
    nets = {}
    for n, i in insts.items():
        for p, net in i["nets"].items():
            nets.setdefault(net, []).append(f"{n}.{p}")
    for net, users in nets.items():
        if len(users) < 2 and net not in ports and not net.endswith("_nc"):
            problems.append(f"net {net} has one connection only ({users[0]})")
    data = dict(ok=not problems, problems=problems, schematic=str(sch), instances=insts, ports=ports,
                nets={k: v for k, v in sorted(nets.items())})
    save(top, "netlist", data)
    kinds = {}
    for i in insts.values():
        kinds[i["cell"]] = kinds.get(i["cell"], 0) + 1
    return (f"netlist {top}: {len(insts)} instances ({', '.join(f'{v} {k}' for k, v in kinds.items())}), "
            f"{len(nets)} nets, {len(ports)} macro pins" + "".join(f"\n  PROBLEM {p}" for p in problems))


# ----------------------------------------------------------------------------- abstract
def _block_files(c: dict, symbol: str) -> dict:
    b = c["blocks"][symbol]
    if b["source"] == "flow":
        cell = b.get("cell", symbol)
        d = flow.FLOW / cell
        return dict(cell=cell, gds=d / f"{cell}.gds", lvs_ref=d / f"{cell}_lvs_ref.spice",
                    pins=d / f"{cell}_pins.json", signoff=d / "signoff.json")
    cell = b.get("cell", symbol)
    return dict(cell=cell, gds=(HERE / b["gds"]).resolve(), lvs_ref=(HERE / b["lvs_ref"]).resolve(),
                pins=(HERE / b["pins"]).resolve(), signoff=None)


def _unlabelled(src: Path, out: Path) -> None:
    """Copy of a block GDS without text: the flat top must carry only top-level labels."""
    import klayout.db as kdb
    ly = kdb.Layout()
    ly.read(str(src))
    for cl in ly.each_cell():
        for li in ly.layer_indexes():
            for s in list(cl.shapes(li).each(kdb.Shapes.STexts)):
                cl.shapes(li).erase(s)
    ly.write(str(out))


def st_abstract(top):
    c = check_top(top)
    nl = need(top, "netlist")
    ad = tdir(top) / "abstracts"
    ad.mkdir(exist_ok=True)
    problems, done = [], {}
    for inst in nl["instances"].values():
        sym = inst["symbol"]
        if sym in done:
            continue
        f = _block_files(c, sym)
        cell = f["cell"]
        miss = [k for k in ("gds", "lvs_ref", "pins") if not Path(f[k]).exists()]
        if miss:
            problems.append(f"{cell}: missing {miss} (build it: flow.py run {cell})")
            done[sym] = None
            continue
        so = json.loads(Path(f["signoff"]).read_text()) if f["signoff"] and Path(f["signoff"]).exists() else None
        state = "hand block (not checked)"
        if f["signoff"]:
            if not so or not so.get("ok"):
                problems.append(f"{cell}: has not passed signoff (flow.py signoff {cell})")
                state = "not signed off"
            else:
                t_so = time.mktime(time.strptime(so["time"], "%Y-%m-%d %H:%M:%S"))
                if Path(f["gds"]).stat().st_mtime > t_so + 1:
                    problems.append(f"{cell}: GDS is newer than its signoff (rerun flow.py signoff {cell})")
                    state = "stale signoff"
                else:
                    state = f"DRC {so['drc']}, LVS {so['lvs']} ({so['time']})"
        pins = json.loads(Path(f["pins"]).read_text())
        x0, y0, x1, y1 = pins["bbox"]
        ref_txt = Path(f["lvs_ref"]).read_text()
        hdr = next(ln for ln in ref_txt.splitlines() if ln.lower().startswith(".subckt"))
        ref_pins = hdr.split()[2:]
        port_nets = {p["net"] for p in pins["ports"]}
        for p in pins["ports"]:
            side = {0: "E", 180: "W", 90: "N", 270: "S"}[round(p["orientation"]) % 360]
            edge = {"E": abs(p["x"] - x1), "W": abs(p["x"] - x0), "N": abs(p["y"] - y1), "S": abs(p["y"] - y0)}[side]
            p["side"] = side
            if edge > 1e-3:
                problems.append(f"{cell}: pin {p['net']} ({side}) is {edge:.3f} um inside the cell edge")
        no_pin = [p for p in ref_pins if p not in port_nets]
        if no_pin:
            problems.append(f"{cell}: LVS pins without an edge pin: {no_pin}")
        sym_pins = set(inst["nets"])
        extra = [p for p in ref_pins if p not in sym_pins and p not in ("VSS", "VDD")]
        if extra:
            problems.append(f"{cell}: block pins {extra} not in symbol {sym}")
        gds = ad / f"{cell}_nolabels.gds"
        _unlabelled(Path(f["gds"]), gds)
        ab = dict(cell=cell, symbol=sym, kind=kind_of(cell), source=c["blocks"][sym]["source"],
                  gds=str(gds), gds_src=str(f["gds"]), lvs_ref=str(f["lvs_ref"]), lvs_pins=ref_pins,
                  bbox=[x0, y0, x1, y1], size=[round(x1 - x0, 4), round(y1 - y0, 4)], ports=pins["ports"],
                  signoff=state)
        (ad / f"{cell}.json").write_text(json.dumps(ab, indent=1))
        done[sym] = ab
    save(top, "abstract", dict(ok=not problems, problems=problems,
                               blocks={k: v["cell"] for k, v in done.items() if v}))
    lines = [f"abstract {top}: {sum(1 for v in done.values() if v)} blocks"]
    for v in done.values():
        if v:
            sides = {}
            for p in v["ports"]:
                sides[p["side"]] = sides.get(p["side"], 0) + 1
            lines.append(f"  {v['cell']:18s} {v['size'][0]:7.2f} x {v['size'][1]:6.2f} um  pins "
                         + " ".join(f"{s}{n}" for s, n in sorted(sides.items())) + f"  [{v['signoff']}]")
    return "\n".join(lines + [f"  PROBLEM {p}" for p in problems])


def abstracts(top: str) -> dict:
    """symbol -> abstract dict."""
    out = {}
    for f in (tdir(top) / "abstracts").glob("*.json"):
        a = json.loads(f.read_text())
        out[a["symbol"]] = a
    return out


# ----------------------------------------------------------------------------- plan
def st_plan(top):
    c = check_top(top)
    nl = need(top, "netlist")
    need(top, "abstract")
    fp = c["floorplan"]
    if fp.get("template", "neuron_rows") != "neuron_rows":
        raise SystemExit(f"error: floorplan template {fp['template']!r} not implemented (neuron_rows only)")
    abs_ = abstracts(top)
    inst = nl["instances"]
    kind = {n: abs_[i["symbol"]]["kind"] for n, i in inst.items()}
    problems, rows, used = [], [], set()
    roles = fp.get("roles") or {}
    order = fp.get("row_order") or list(roles)
    for role in order:
        neu = roles.get(role)
        if neu not in inst or kind[neu] != "neuron":
            problems.append(f"row {role}: {neu} is not a neuron instance")
            continue
        vmem = inst[neu]["nets"]["VMEM"]
        exc = sorted(n for n in inst if kind[n] == "dpi" and inst[n]["nets"].get("Isyn") == vmem)
        inh = sorted(n for n in inst if kind[n] == "dpi_inh" and inst[n]["nets"].get("Iout") == vmem)
        isums = {inst[n]["nets"]["Isum"] for n in exc + inh}
        dacs = sorted(n for n in inst if kind[n] == "dac"
                      and ({inst[n]["nets"].get("Isum_e"), inst[n]["nets"].get("Isum_i")} & isums))
        rows.append(dict(role=role, neuron=neu, vmem=vmem, dpi=exc, dpi_inh=inh, dac=dacs))
        used |= {neu, *exc, *inh, *dacs}
    bias = [n for n in inst if kind[n] == "bias"]
    left = sorted(set(inst) - used - set(bias))
    if left:
        problems.append(f"instances in no row: {left}")
    stack = (fp.get("bias") or {}).get("stack") or bias       # bottom -> top above the rows
    if len(bias) > 1 and sorted(stack) != sorted(bias):
        problems.append(f"floorplan.bias.stack {stack} must list every bias block {bias}")
    bias = [n for n in stack if n in bias]
    pos = fp.get("bias", {}).get("position", "above_top_row")
    if bias and pos != "above_top_row":
        problems.append(f"bias.position {pos!r} not implemented (above_top_row only)")
    sup = c["routing"]["supply"]["style"]
    if sup != "routed":
        problems.append(f"routing.supply.style {sup!r} not implemented (routed only)")
    edge = c["macro_pins"].get("edge", "bottom")
    if edge != "bottom":
        problems.append(f"macro_pins.edge {edge!r} not implemented (bottom only)")
    data = dict(ok=not problems, problems=problems, rows=rows, bias=bias,
                mirror=fp.get("mirror") or {}, bias_position=pos, supply=sup, pin_edge=edge)
    save(top, "plan", data)
    lines = [f"plan {top}: {len(rows)} rows (bottom -> top), bias {' < '.join(bias) or '-'} {pos}"]
    for r in rows:
        lines.append(f"  {r['role']:5s} {r['neuron']:6s} DACs {','.join(r['dac']) or '-':16s} "
                     f"DPI {','.join(r['dpi']) or '-':6s} DPI_inh {','.join(r['dpi_inh']) or '-'}")
    return "\n".join(lines + [f"  PROBLEM {p}" for p in problems])


# ----------------------------------------------------------------------------- place
CHANNELS = ("left", "A", "B", "C")          # vertical channels: | left | DAC | A | DPI | B | neuron | C |


def _facing(kind: str, side: str) -> str | None:
    """Vertical channel a block pin faces (None: faces a row gap / the top gap)."""
    if side in "NS":
        return None
    return {("dac", "W"): "left", ("dac", "E"): "A", ("dpi", "W"): "A", ("dpi", "E"): "B",
            ("dpi_inh", "W"): "A", ("dpi_inh", "E"): "B", ("neuron", "W"): "B",
            ("neuron", "E"): "C", ("bias", "W"): "left", ("bias", "E"): "C"}.get((kind, side))


def demand(top: str) -> dict:
    """Tracks each vertical channel needs: nets that leave their row (or reach a macro pin)
    count once per channel, row-local nets count for the busiest row only."""
    nl, plan, abs_ = load(top, "netlist"), load(top, "plan"), abstracts(top)
    inst = nl["instances"]
    row_of = {}
    for k, r in enumerate(plan["rows"]):
        for n in [r["neuron"], *r["dpi"], *r["dpi_inh"], *r["dac"]]:
            row_of[n] = k
    net_rows = {}
    for n, i in inst.items():
        for p, net in i["nets"].items():
            net_rows.setdefault(net, set()).add(row_of.get(n, -1))
    ports = set(nl["ports"])
    glob, local = {ch: set() for ch in CHANNELS}, {ch: {} for ch in CHANNELS}
    for n, i in inst.items():
        a = abs_[i["symbol"]]
        for p in a["ports"]:
            ch = _facing(a["kind"], p["side"])
            if ch is None:
                continue
            net = i["nets"][p["net"]]
            if len(net_rows[net]) > 1 or net in ports:
                glob[ch].add(net)
            else:
                local[ch].setdefault(row_of.get(n, -1), set()).add(net)
    return {ch: len(glob[ch]) + max((len(s) for s in local[ch].values()), default=0) for ch in CHANNELS}


def _growth(top: str) -> dict:
    g = load(top, "growth")
    return (g or {}).get("factors", {})


def layout_geometry(top: str, growth: dict | None = None) -> dict:
    """Coordinates of every block, pad and channel from the plan, the abstracts and the
    channel demand (times the growth factors the route stage learned)."""
    c = conf()
    nl, plan, abs_ = load(top, "netlist"), load(top, "plan"), abstracts(top)
    fp, rt = c["floorplan"], c["routing"]
    growth = growth if growth is not None else _growth(top)
    pitch = 0.8                                     # router track pitch on met3 / met4 (RouterTech)
    util = float(rt.get("track_utilisation", 0.7))
    edge = float(rt.get("channel_margin_um", 3.0))
    inst = nl["instances"]

    def size(n):
        return abs_[inst[n]["symbol"]]["size"]

    def chan_w(name, tracks):
        return round((tracks * pitch / util + 2 * edge) * growth.get(name, 1.0), 2)

    dem = demand(top)
    cw = {ch: chan_w(ch, dem[ch]) for ch in CHANNELS}
    fixed = fp.get("channels_um") or {}
    for k, v in fixed.items():
        if v != "auto":
            cw[k] = float(v) * growth.get(k, 1.0)
    rows = plan["rows"]
    dacs = [n for r in rows for n in r["dac"]]
    dpis = [n for r in rows for n in r["dpi"] + r["dpi_inh"]]
    neus = [r["neuron"] for r in rows]
    w_dac = max(size(n)[0] for n in dacs)
    w_dpi = max(size(n)[0] for n in dpis)
    w_neu = max(size(n)[0] for n in neus)
    margin = float(fp.get("margin_um", 4.0))
    x_left = margin
    x_dac = x_left + cw["left"]
    x_dpi = x_dac + w_dac + cw["A"]
    x_neu = x_dpi + w_dpi + cw["B"]
    width = x_neu + w_neu + cw["C"] + margin
    stack_gap = float(fp.get("stack_gap_um", 6.0))
    row_gap = chan_w("rowgap", int(fp.get("row_gap_tracks", 8)))
    # macro pins (pads) and the gap above them
    pads = nl["ports"]
    pad_pitch = float(c["macro_pins"].get("spacing_um", 1.6))
    pad_w, pad_h = 0.5, 1.0
    bottom_gap = round((max(8, int(0.5 * len(pads))) * pitch / util + 2 * edge) * growth.get("bottom", 1.0), 2)
    y = margin + pad_h + bottom_gap
    placed, row_box = {}, []
    for k, r in enumerate(rows):
        y0 = y
        yy = y0
        for n in r["dac"]:                       # DACs stacked, first at the bottom
            placed[n] = dict(x=x_dac + (w_dac - size(n)[0]), y=yy)
            yy += size(n)[1] + stack_gap
        h_dac = yy - stack_gap - y0
        yy = y0
        for n in r["dpi"] + r["dpi_inh"]:        # excitatory DPI at the bottom, inhibitory above
            placed[n] = dict(x=x_dpi, y=yy)
            yy += size(n)[1] + stack_gap
        h_dpi = yy - stack_gap - y0
        placed[r["neuron"]] = dict(x=x_neu, y=y0)
        h = max(h_dac, h_dpi, size(r["neuron"])[1])
        row_box.append((y0, y0 + h))
        y = y0 + h + (row_gap if k < len(rows) - 1 else 0)
    # bias blocks, stacked above the top row (plan order, bottom -> top): each one above its own
    # routing gap. With more than one (the generator over the bias cell), all of them sit right of
    # a side column that carries their W pins down to the rows' left channel.
    top_gap = 0.0
    stack = plan["bias"] or []
    stack = [stack] if isinstance(stack, str) else stack
    side = 0.0
    if len(stack) > 1:
        w_pins = max(sum(1 for p in abs_[inst[b]["symbol"]]["ports"] if p["side"] == "W") for b in stack)
        side = chan_w("top", w_pins + 4)
    for k, b in enumerate(stack):
        a = abs_[inst[b]["symbol"]]
        s_pins = [p for p in a["ports"] if p["side"] == "S"]
        gap = chan_w("top", max(8, len(s_pins) + 4))
        if k == 0:
            cx = sum(p["x"] - a["bbox"][0] for p in s_pins) / len(s_pins) if s_pins else a["size"][0] / 2
            target = x_neu - cw["B"] / 2           # bias pins drop into channel B (neuron biases)
            bx = min(max(margin, target - cx), max(margin, width - margin - a["size"][0]))
            bx = max(bx, margin + side)
        else:
            bx = margin + side
        placed[b] = dict(x=bx, y=y + gap)
        width = max(width, bx + a["size"][0] + margin)
        y = y + gap + a["size"][1]
        top_gap += gap
    height = y + margin
    snap = lambda v: round(round(v / 0.01) * 0.01, 2)               # noqa: E731  (2x grid, 10 nm)
    for n, p in placed.items():
        p["x"], p["y"] = snap(p["x"]), snap(p["y"])
        p["w"], p["h"] = size(n)
        p["mirrored"] = bool((plan.get("mirror") or {}).get(abs_[inst[n]["symbol"]]["kind"], False))
    # pad x: under the net's lowest pin, sorted, pushed apart to the pad pitch
    lowest = {}
    for n, i in inst.items():
        a = abs_[i["symbol"]]
        p0 = placed[n]
        for pp in a["ports"]:
            net = i["nets"][pp["net"]]
            if net not in pads:
                continue
            px = p0["x"] + (pp["x"] - a["bbox"][0])
            py = p0["y"] + (pp["y"] - a["bbox"][1])
            ch = _facing(a["kind"], pp["side"])
            if ch == "left":
                px = x_left + cw["left"] / 2
            elif ch == "A":
                px = x_dac + w_dac + cw["A"] / 2
            elif ch == "B":
                px = x_dpi + w_dpi + cw["B"] / 2
            elif ch == "C":
                px = x_neu + w_neu + cw["C"] / 2
            if net not in lowest or py < lowest[net][1]:
                lowest[net] = (px, py)
    tx = sorted(((lowest.get(n, (width / 2, 0))[0], k, n) for k, n in enumerate(pads)))
    xs, prev = [], margin - pad_pitch
    for t, _k, n in tx:
        x = max(t, prev + pad_pitch)
        xs.append([n, x])
        prev = x
    if xs and xs[-1][1] + pad_w + margin > width:  # shift left (keeping the pitch) to fit the die
        for k in range(len(xs) - 1, -1, -1):
            lim = (xs[k + 1][1] - pad_pitch) if k + 1 < len(xs) else width - margin - pad_w
            xs[k][1] = min(xs[k][1], lim)
        if xs[0][1] < margin:                      # still too many: widen the die
            dx = margin - xs[0][1]
            for e in xs:
                e[1] += dx
            width += dx
    pad_pos = {n: dict(x=snap(x), y=snap(margin), w=pad_w, h=pad_h) for n, x in xs}
    regions = dict(
        left=(x_left, x_dac), A=(x_dac + w_dac, x_dpi), B=(x_dpi + w_dpi, x_neu), C=(x_neu + w_neu, width),
        bottom=(0.0, row_box[0][0]) if row_box else (0, 0),
        top=(row_box[-1][1], height) if row_box else (0, 0),     # the whole bias stack
        rowgaps=[(row_box[k][1], row_box[k + 1][0]) for k in range(len(row_box) - 1)])
    return dict(width=snap(width), height=snap(height), blocks=placed, pads=pad_pos, channels_um=cw,
                demand_tracks=dem, row_gap_um=row_gap, bottom_gap_um=bottom_gap, top_gap_um=top_gap,
                rows=row_box, regions=regions, growth=growth)


def st_place(top):
    check_top(top)
    need(top, "plan")
    g = layout_geometry(top)
    boxes = [(n, b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]) for n, b in g["blocks"].items()]
    boxes += [(f"pad:{n}", p["x"], p["y"], p["x"] + p["w"], p["y"] + p["h"]) for n, p in g["pads"].items()]
    problems = []
    min_gap = float(conf()["floorplan"].get("min_block_gap_um", 4.0))
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            gx = max(b[1] - a[3], a[1] - b[3])
            gy = max(b[2] - a[4], a[2] - b[4])
            gap = max(gx, gy)
            limit = 0.8 if a[0].startswith("pad:") or b[0].startswith("pad:") else min_gap
            if gap < limit - 1e-6:
                problems.append(f"{a[0]} / {b[0]}: gap {gap:.2f} um < {limit} um")
        if a[1] < 0 or a[2] < 0 or a[3] > g["width"] or a[4] > g["height"]:
            problems.append(f"{a[0]} outside the die")
    save(top, "place", dict(ok=not problems, problems=problems[:20], **{k: v for k, v in g.items()}))
    (tdir(top) / "placement.json").write_text(json.dumps(g, indent=1))
    ch = ", ".join(f"{k} {v:.1f}" for k, v in g["channels_um"].items())
    return (f"place {top}: {g['width']:.1f} x {g['height']:.1f} um ({g['width'] * g['height'] / 1e6:.3f} mm2), "
            f"{len(g['blocks'])} blocks, {len(g['pads'])} pads\n  channels (um): {ch}; row gap "
            f"{g['row_gap_um']:.1f}, bottom {g['bottom_gap_um']:.1f}, top {g['top_gap_um']:.1f}\n"
            f"  demand (tracks): {g['demand_tracks']}"
            + "".join(f"\n  PROBLEM {p}" for p in problems[:20]))


# ----------------------------------------------------------------------------- route
def _router_env():
    from glayout import gf180 as pdk
    import glayout.floorplan.route_flow as rf
    rf.floorplan_netlist = lambda circuit, result, name: None      # imported GDS: own LVS ref
    pdk.activate()
    return pdk, rf


def _make_block(pdk, a: dict, cache: dict):
    import gdsfactory as gf
    from glayout.floorplan.block import Block, Variant, extract_pins
    if a["cell"] in cache:
        return cache[a["cell"]]
    comp = gf.import_gds(a["gds"], cellname=a["cell"])
    comp = comp.copy() if getattr(comp, "_locked", False) else comp
    if hasattr(comp, "unlock"):
        comp.unlock()
    net_ports = {}
    for k, p in enumerate(a["ports"]):
        name = f"{p['net']}_{p['side']}{k}"
        comp.add_port(name=name, center=(p["x"], p["y"]), width=p["width"],
                      orientation=p["orientation"], layer=pdk.get_glayer(p["layer"]))
        net_ports.setdefault(p["net"], []).append(name)
    v = Variant({}, float(comp.xsize), float(comp.ysize), extract_pins(comp, net_ports, pdk), comp)
    cache[a["cell"]] = Block(a["cell"], a["kind"], [v])
    return cache[a["cell"]]


def _pad_block(pdk, net: str, w: float, h: float):
    """Macro pin: a met2 rectangle with one port facing up (into the die)."""
    from glayout.backend import Component
    from glayout.floorplan.block import Block, Variant, extract_pins
    safe = re.sub(r"[^A-Za-z0-9_]", "_", net)
    comp = Component(f"pad_{safe}")
    comp.add_polygon([(0, 0), (w, 0), (w, h), (0, h)], layer=pdk.get_glayer("met2"))
    comp.add_port(name="P_N", center=(w / 2, h), width=w, orientation=90, layer=pdk.get_glayer("met2"))
    v = Variant({}, w, h, extract_pins(comp, {net: ["P_N"]}, pdk), comp)
    return Block(f"pad_{safe}", "pad", [v])


def _tech(pdk):
    from glayout.floorplan.router import RouterTech, H, V
    from glayout.primitives.via_gen import via_stack
    from glayout.util.comp_utils import evaluate_bbox
    c = conf()["routing"]
    t = RouterTech.from_pdk(pdk, detour_ratio=float(c.get("detour_ratio", 0.0)),
                            max_iterations=int(c.get("max_iterations", 35)))
    # met3 pins (N/S risers): land on met3 itself (H layer), or via up to met4
    v = via_stack(pdk, "met3", "met4")
    pads = {}
    for lay in v.get_layers():
        g = pdk.layer_to_glayer(tuple(lay))
        if g.startswith("met"):
            pads[g] = max(evaluate_bbox(v.extract(layers=[tuple(lay)])))
    t.access_pads[("met3", H)] = {"met3": t.wire[H]}
    t.access_pads[("met3", V)] = pads
    return t


def _circuit(top, pdk, g):
    from glayout.floorplan.anneal import FloorplanResult, FloorplanWeights, Placed
    from glayout.floorplan.circuit import Circuit, Instance
    nl, abs_ = load(top, "netlist"), abstracts(top)
    cache, insts, placed = {}, [], {}
    for n, i in nl["instances"].items():
        blk = _make_block(pdk, abs_[i["symbol"]], cache)
        insts.append(Instance(n, blk, {p: i["nets"][p] for p in blk.nets}))
        b = g["blocks"][n]
        v = blk.variants[0]
        placed[n] = Placed(n, b["x"], b["y"], v.width, v.height, 0, b["mirrored"])
    for net, p in g["pads"].items():
        name = "pad_" + re.sub(r"[^A-Za-z0-9_]", "_", net)
        blk = _pad_block(pdk, net, p["w"], p["h"])
        insts.append(Instance(name, blk, {net: net}))
        placed[name] = Placed(name, p["x"], p["y"], p["w"], p["h"], 0, False)
    circ = Circuit(top, insts, ports=list(nl["ports"]))
    fp = FloorplanResult(circ, placed, dict(width=g["width"], height=g["height"]), FloorplanWeights())
    return circ, fp


def _region_of(g: dict, x: float, y: float) -> str:
    r = g["regions"]
    for name in ("bottom", "top"):
        lo, hi = r[name]
        if lo <= y <= hi:
            return name
    for k, (lo, hi) in enumerate(r["rowgaps"]):
        if lo <= y <= hi:
            return "rowgap"
    for name in CHANNELS:
        lo, hi = r[name]
        if lo <= x <= hi:
            return name
    # inside a block column: the nearest vertical channel
    return min(CHANNELS, key=lambda n: min(abs(x - r[n][0]), abs(x - r[n][1])))


def write_hierarchical(top: str, pdk, rr, g: dict, gds: Path) -> dict:
    """<top>.gds as a hierarchy: one instance per block of its own signed-off cell (with its own
    labels), and the top cell holding only the routing, the pads and the macro pin labels.
    route_floorplan's result is flat (blocks merged into one cell); this writes the same shapes."""
    import klayout.db as kdb
    from glayout.backend import Component
    from glayout.floorplan.route_flow import draw_routes
    nl, abs_ = load(top, "netlist"), abstracts(top)
    tmp = Path(tempfile.mkdtemp())
    # routing + pads + macro pin labels, flattened into one cell
    wires = Component(f"{top}_routing")
    draw_routes(pdk, wires, rr)
    for net, p in g["pads"].items():
        x0, y0 = p["x"], p["y"]
        wires.add_polygon([(x0, y0), (x0 + p["w"], y0), (x0 + p["w"], y0 + p["h"]), (x0, y0 + p["h"])],
                          layer=pdk.get_glayer("met2"))
        x, y = x0 + p["w"] / 2, y0 + p["h"] / 2
        wires.add_polygon([(x - 0.135, y - 0.135), (x + 0.135, y - 0.135), (x + 0.135, y + 0.135),
                           (x - 0.135, y + 0.135)], layer=pdk.get_glayer("met2_pin"))
        wires.add_label(text=net, position=(x, y), layer=pdk.get_glayer("met2_label"))
    flat = wires.flatten()
    flat.name = f"{top}_routing"
    flat.write_gds(str(tmp / "routing.gds"))
    ly = kdb.Layout()
    ly.dbu = 0.001
    ly.read(str(tmp / "routing.gds"))
    rcell = ly.top_cell()                          # gdsfactory may rename the cell on write
    tc = ly.create_cell(top)
    tc.copy_tree(rcell)                            # flat already: shapes only
    rcell.delete()
    cells, check = {}, []
    for n, i in nl["instances"].items():
        a = abs_[i["symbol"]]
        if a["cell"] not in cells:                 # the signed-off GDS, labels kept
            before = {c.cell_index() for c in ly.each_cell()}
            ly.read(a["gds_src"])
            new = [c for c in ly.each_cell() if c.cell_index() not in before]
            cell = ly.cell(a["cell"])
            if cell is None:
                raise SystemExit(f"error: {a['gds_src']} has no cell {a['cell']} (got {[c.name for c in new]})")
            cells[a["cell"]] = cell
        cell = cells[a["cell"]]
        b = g["blocks"][n]
        x0, y0, x1, y1 = a["bbox"]
        if b["mirrored"]:                          # mirror about the y axis, then align the bbox
            t = kdb.DTrans(kdb.DTrans.M90, kdb.DVector(b["x"] + x1, b["y"] - y0))
        else:
            t = kdb.DTrans(kdb.DVector(b["x"] - x0, b["y"] - y0))
        tc.insert(kdb.DCellInstArray(cell.cell_index(), t))
        bb = cell.dbbox().transformed(t)
        check.append(max(abs(bb.left - b["x"]), abs(bb.bottom - b["y"])))
    ly.write(str(gds))
    shutil.rmtree(tmp, ignore_errors=True)
    return dict(cells=sorted(cells), instances=len(nl["instances"]), max_bbox_offset_um=round(max(check), 4))


def res_bodies(top: str, g: dict) -> list:
    """n-well resistor bodies of every flow block, in macro coordinates: Magic's GDS import has no
    rule for them, so top_pex.sh paints rnw over each before extracting (as flow.py signoff)."""
    nl, abs_ = load(top, "netlist"), abstracts(top)
    out = []
    for n, i in nl["instances"].items():
        a = abs_[i["symbol"]]
        bj = flow.FLOW / a["cell"] / f"{a['cell']}.build.json"
        if a["source"] != "flow" or not bj.exists():
            continue
        b, (x0, y0, x1, _y1) = g["blocks"][n], a["bbox"]
        for bx0, by0, bx1, by1 in json.loads(bj.read_text()).get("res_bodies") or []:
            if b["mirrored"]:                   # as write_hierarchical: x -> b.x + x1 - x
                bx0, bx1 = b["x"] + x1 - bx1, b["x"] + x1 - bx0
            else:
                bx0, bx1 = bx0 - x0 + b["x"], bx1 - x0 + b["x"]
            out.append([round(v, 4) for v in (bx0, by0 - y0 + b["y"], bx1, by1 - y0 + b["y"])])
    return out


def lvs_ref(top: str, path: Path) -> None:
    """Top subckt over each block's own LVS reference (pins by name); macro pins in order."""
    nl, abs_ = load(top, "netlist"), abstracts(top)
    parts, seen, lines = [], set(), []
    for n, i in nl["instances"].items():
        a = abs_[i["symbol"]]
        if a["cell"] not in seen:
            seen.add(a["cell"])
            parts.append(Path(a["lvs_ref"]).read_text())
        nets = [i["nets"].get(p, p) for p in a["lvs_pins"]]
        # gf180_xschem_klayout_spice_convert strips one leading X (XDAC.. -> a diode)
        lines.append(f"XX{n} " + " ".join(nets) + f" {a['cell']}")
    path.write_text("\n".join(parts) + f"\n.subckt {top} {' '.join(nl['ports'])}\n" + "\n".join(lines)
                    + "\n.ends\n")


def _segments(rr):
    g, out = rr.grid, {}
    for net, plist in rr.paths.items():
        for path in plist:
            for a, b in zip(path, path[1:]):
                if g.layer(a) == g.layer(b):
                    (ax, ay), (bx, by) = g.xy(a), g.xy(b)
                    out.setdefault(net, []).append((g.layer(a), ax, ay, bx, by))
    return out


def _parallel(sa, sb, near):
    tot = 0.0
    for za, ax0, ay0, ax1, ay1 in sa:
        for zb, bx0, by0, bx1, by1 in sb:
            if za != zb:
                continue
            if ay0 == ay1 and by0 == by1 and 0 < abs(ay0 - by0) <= near:
                tot += max(0.0, min(max(ax0, ax1), max(bx0, bx1)) - max(min(ax0, ax1), min(bx0, bx1)))
            elif ax0 == ax1 and bx0 == bx1 and 0 < abs(ax0 - bx0) <= near:
                tot += max(0.0, min(max(ay0, ay1), max(by0, by1)) - max(min(ay0, ay1), min(by0, by1)))
    return tot


def sensitive_report(rr, rules) -> list[dict]:
    """Parallel run of each sensitive net next to its aggressors (same layer, within min_spacing)."""
    seg = _segments(rr)
    out = []
    for rule in rules or []:
        sens = [n for n in seg if any(glob_re(p).match(n) for p in rule["nets"])]
        agg = [n for n in seg if any(glob_re(p).match(n) for p in rule["aggressors"])]
        for s in sorted(sens):
            run = {a: round(_parallel(seg[s], seg[a], rule["min_spacing_um"]), 1) for a in agg if a != s}
            run = {a: v for a, v in run.items() if v > 0}
            worst = max(run.values(), default=0.0)
            out.append(dict(net=s, parallel_um=run, worst_um=worst, limit_um=rule["max_parallel_um"],
                            ok=worst <= rule["max_parallel_um"]))
    return out


def st_route(top):
    c = check_top(top)
    need(top, "place")
    pdk, rf = _router_env()
    tech = _tech(pdk)
    d = tdir(top)
    attempts = int(c["routing"].get("grow_attempts", 3))
    growth = dict(_growth(top))
    log, t0 = [], time.time()
    for k in range(attempts + 1):
        g = layout_geometry(top, growth)
        circ, fp = _circuit(top, pdk, g)
        ta = time.time()
        comp, rr = rf.route_floorplan(pdk, circ, fp, tech, name=top, labels=False)
        spots = {}
        for x, y in rr.hotspots:
            r = _region_of(g, x, y)
            spots[r] = spots.get(r, 0) + 1
        log.append(dict(attempt=k, size_um=[g["width"], g["height"]], routed=rr.success,
                        failed=list(rr.failed_nets), unreachable=list(rr.unreachable),
                        hotspots=spots, growth=dict(growth), seconds=round(time.time() - ta)))
        print(f"route attempt {k}: {g['width']:.0f} x {g['height']:.0f} um, routed={rr.success}, "
              f"failed {len(rr.failed_nets)}, unreachable {len(rr.unreachable)}, hotspots {spots} "
              f"({time.time() - ta:.0f} s)", flush=True)
        if rr.success:
            break
        if k == attempts:
            break
        for r in spots or {"left": 1}:
            growth[r] = round(growth.get(r, 1.0) * 1.4, 3)
    save(top, "growth", dict(ok=True, factors=growth))
    (d / "placement.json").write_text(json.dumps(g, indent=1))
    gds = d / f"{top}.gds"
    hier = write_hierarchical(top, pdk, rr, g, gds)
    if c["routing"].get("write_flat", False):          # the router's flat view, for comparison
        comp.write_gds(str(d / f"{top}_flat.gds"))
    lvs_ref(top, d / f"{top}_lvs_ref.spice")
    sens = sensitive_report(rr, c["routing"].get("sensitive")) if rr.success else []
    bad = [s for s in sens if not s["ok"]]
    data = dict(ok=bool(rr.success), size_um=[g["width"], g["height"]],
                area_mm2=round(g["width"] * g["height"] / 1e6, 4), wirelength_um=round(rr.wirelength, 1),
                vias=rr.vias, failed=list(rr.failed_nets), unreachable=list(rr.unreachable),
                attempts=log, sensitive=sens, sensitive_violations=[s["net"] for s in bad],
                hierarchy=hier, res_bodies=res_bodies(top, g),
                seconds=round(time.time() - t0))
    save(top, "route", data)
    lines = [f"route {top}: {'routed' if rr.success else 'NOT routed'}, {g['width']:.1f} x {g['height']:.1f} um "
             f"({data['area_mm2']} mm2), wire {rr.wirelength:.0f} um, {rr.vias} vias, "
             f"{len(log)} attempt(s), {data['seconds']} s"]
    if not rr.success:
        lines.append(f"  failed nets {rr.failed_nets[:12]}, unreachable pins {rr.unreachable[:12]}")
    if sens:
        lines.append(f"  sensitive nets: {len(sens) - len(bad)}/{len(sens)} within their parallel-run limit"
                     + "".join(f"\n    {s['net']}: {s['worst_um']} um next to "
                               f"{max(s['parallel_um'], key=s['parallel_um'].get)} (limit {s['limit_um']})"
                               for s in bad[:10]))
    lines.append(f"  wrote {gds.name}, {top}_lvs_ref.spice")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- signoff
def st_signoff(top):
    c = check_top(top)
    need(top, "route")
    d = tdir(top)
    gds = d / f"{top}.gds"
    var = c["signoff"].get("drc_variant", "D")
    out = {}
    out["drc"], waived = flow.drc(gds, top, d / "drc", d / "drc.log", variant=var, timeout=7200)
    if waived:
        out["drc_waived"] = waived
    shutil.rmtree(d / "lvs", ignore_errors=True)
    flow.login(f"python3 {flow.TECH}/lvs/gf180_xschem_klayout_spice_convert.py {top}_lvs_ref.spice "
               f"-o {top}_lvs_ref.cdl > /dev/null 2>&1; python3 {flow.TECH}/lvs/run_lvs.py "
               f"--layout={gds} --netlist={d}/{top}_lvs_ref.cdl --variant={var} --topcell={top} "
               f"--run_dir={d}/lvs > {d}/lvs.log 2>&1", d, timeout=7200)
    log = (d / "lvs.log").read_text()
    out["lvs"] = "match" if "Netlists match" in log else "mismatch" if "don't match" in log else "failed to run"
    save(top, "signoff", dict(ok=out["drc"] == "clean" and out["lvs"] == "match", **out))
    return f"signoff {top}: DRC {out['drc']}, LVS {out['lvs']}"


# ----------------------------------------------------------------------------- status / run
STAGE_ORDER = ("netlist", "abstract", "plan", "place", "route", "signoff")


def st_status(top):
    lines = [f"status {top} (top/{top}/)"]
    for s in STAGE_ORDER:
        d = load(top, s)
        if not d:
            lines.append(f"  {s:9s} -")
            continue
        extra = ""
        if s == "route":
            extra = f"  {d.get('size_um')} um, failed {d.get('failed')}"
        if s == "signoff":
            extra = f"  DRC {d.get('drc')}, LVS {d.get('lvs')}"
        lines.append(f"  {s:9s} {'ok  ' if d.get('ok') else 'FAIL'} {d['time']}{extra}"
                     + "".join(f"\n            {p}" for p in d.get("problems", [])[:5]))
    return "\n".join(lines)


def st_run(top):
    out = []
    for s in STAGE_ORDER:
        try:
            out.append(STAGES[s](top))
        except SystemExit as e:
            out.append(str(e))
            break
        print(out[-1], flush=True)
        if not (load(top, s) or {}).get("ok"):
            out.append(f"stopped after {s}: needs attention (top.py status {top})")
            break
    return out[-1] if out else ""


STAGES = {"netlist": st_netlist, "abstract": st_abstract, "plan": st_plan, "place": st_place,
          "route": st_route, "signoff": st_signoff, "status": st_status, "run": st_run}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in STAGES:
        print(__doc__)
        raise SystemExit(2)
    print(STAGES[sys.argv[1]](sys.argv[2]))
