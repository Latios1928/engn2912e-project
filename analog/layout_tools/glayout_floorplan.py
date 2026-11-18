"""
Reusable two-row floorplan for GF180 gLayout cells: schematic in, DRC/LVS-ready GDS out.

    from glayout_netlist import from_schematic
    from glayout_floorplan import two_row, write_cell
    cell = from_schematic("analog/neuron/spike_amplifier_sized.sch").legalize()
    cell.connect("net2", "VN")                       # explicit schematic fix, if any
    res = two_row(cell, "spike_amp_fp")
    print(write_cell(res, "analog/neuron/layout"))   # GDS, LVS ref, predictions

  CLI (no code needed for a new cell):
    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python glayout_floorplan.py \\
        analog/neuron/spike_amplifier_sized.sch --name spike_amp_fp --connect net2=VN

Floorplan (bottom -> top):
    bottom channel   NMOS gate nets + their pins           met4 tracks
    NMOS row         NMOS with body on ground: dummy ring, one shared DNWELL (body VSS);
                     each other NMOS body net (e.g. body tied to source): its own DNWELL
                     island with its own dummy ring and p+ body ring on that net, side by side
    mid channel      all source/drain nets, VSS, VDD
    PMOS row         all PMOS rotated 180 deg, dummy ring, n-tap ring (body VDD)
    top channel      PMOS gate nets + their pins
    left             met3 columns for nets in more than one channel; pin labels; edge pins:
                     every pin track ends in a met2 stub at the left cell edge, VSS / VDD in
                     met1 straps from the substrate / n-tap rings (ports in <cell>_pins.json)
    right            up to 2 MIM caps sharing one bottom-plate net: met4 spine to that net's
                     mid track, met5 top-plate links
Layer plan: met2 device buses, met3 vertical, met4 horizontal, met5 cap links.
Every shape is net-tagged in a Router, so the short checker, the DRC predictor and the
parasitic predictor all run before the real tools.

Assumptions (checked, with a clear error otherwise): PMOS body = VDD, m = 1, at most 2 caps,
all with the same bottom-plate net (any net: VSS, VDD or a signal). NMOS bodies may be any net (islands, see above).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from gdsfactory.component import Component
from gdsfactory.components import rectangle
from glayout import gf180 as pdk, straight_route, mimcap

from glayout_helpers import fet
from glayout_rings import dummy_ring, dnw_guard, nwell_guard
from glayout_router import Router, pack_tracks, PITCH, WIRE

GAP = 0.6            # device-to-device gap in a row
CH_MARGIN = 0.9      # ring metal -> first/last channel track (centre)
CAP_GAP = 2.0        # spine centre -> MIM plate: 0.25 + MIMTM.1 (1.2) + margin
CAP_PITCH = 1.6      # met5 link columns: 1.0 wire + 0.44 space + margin
MIM_KEEPOUT = 1.3    # cell outline past a MIM plate (MIMTM.1 1.2 + margin), for top-level routers
GROUND = ("VSS", "GND", "0")
PIN_BLANK_TRACKS = 2 # empty channel tracks between two edge-pin tracks (pin pitch = (1 + this) x 0.8 um).
                     # 1 (1.6 um) still walled VMEM in on glayout.floorplan's router (row_111 test)
ISLAND_GAP = 0.4     # guard bbox to guard bbox. 0 put neighbouring substrate-ring metal
                     # < M1.2a 0.23 / M2.2a 0.28 apart where guards of different heights meet;
                     # DNWELLs end up > 5.7 um apart (DN.2a 2.5, DN.2b 5.42)


@dataclass
class Result:
    name: str
    top: Component
    router: Router
    ref_lines: list
    pins: list
    summary: str
    notes: list
    edge_ports: list = None      # [{net, layer, x, y, orientation, width}] at the cell's left edge


def bus(dev, term):
    a, b = dev.ports[f"multiplier_0_{term}_W"].center, dev.ports[f"multiplier_0_{term}_E"].center
    return min(a[0], b[0]), max(a[0], b[0]), a[1]


DBU = 0.005      # GF180 database unit (um)


def _snap(v: float) -> float:
    """Round a move to the database grid. A device whose height is an odd multiple of 5 nm has
    its centre on 2.5 nm; centring it there puts every shape off-grid, and the GDS writer's
    rounding then makes 0.225 um contacts, 0.265 um vias and slivers (bias_cell, W = 1.435 um)."""
    return round(v / DBU) * DBU


def _row(top, fets):
    refs, x = {}, 0.0
    for f in fets:
        r = top << fet(pdk, f.kind, f.w, f.l, fingers=f.nf, with_dummy=False)
        if f.kind == "p":
            r.rotate(180)                      # gates on top, S/D buses at the bottom
        r.move((_snap(x - r.xmin), _snap(-r.center[1])))   # stay on the 5 nm grid
        x = r.xmax + GAP
        refs[f.name] = r
    return refs


def _risers(refs, fets):
    """(net, x, y_bus, channel, tag) per terminal: S at left end, D at right end, G centre."""
    out = []
    for f in fets:
        r = refs[f.name]
        sx0, _, sy = bus(r, "source")
        _, dx1, dy = bus(r, "drain")
        gx0, gx1, gy = bus(r, "gate")
        g_ch = "bot" if f.kind == "n" else "top"
        out += [(f.s, sx0 + WIRE / 2, sy, "mid", f"{f.name}.S"),
                (f.d, dx1 - WIRE / 2, dy, "mid", f"{f.name}.D"),
                (f.g, (gx0 + gx1) / 2, gy, g_ch, f"{f.name}.G")]
    return out


def _ring_y(port):
    """y of a via pad on a ring side, given that side's outer/inner edge port."""
    return port.center[1] + (-WIRE / 2 if round(port.orientation) == 90 else WIRE / 2)


SIDE = {"W": "W", "E": "E", "N": "N", "S": "S", "LEFT": "W", "RIGHT": "E", "TOP": "N", "BOTTOM": "S"}
NS_PITCH = 2.4       # N/S pin riser columns (same spacing rule as edge pins, see PIN_BLANK_TRACKS)


def _pin_side(pin_sides, net):
    """Edge side of a pin net from {"default": "W", net: side}; VSS / VDD stay on the left."""
    if net in ("VSS", "VDD") or not pin_sides:
        return "W"
    side = pin_sides.get(net, pin_sides.get("default", "W"))
    out = SIDE.get(str(side).upper())
    if out is None:
        raise ValueError(f"pin_sides: {net}: side {side!r} (use W/E/N/S or left/right/top/bottom)")
    return out


def _supply_sides(pin_sides, net):
    """Edges the VSS / VDD met1 strap reaches: pin_sides {VSS: [W, E]} (or "WE"); default W."""
    raw = (pin_sides or {}).get(net, "W")
    items = list(raw) if isinstance(raw, str) and raw.upper() in ("WE", "EW") else (
        [raw] if isinstance(raw, str) else list(raw))
    out = []
    for s in items:
        side = SIDE.get(str(s).upper())
        if side not in ("W", "E"):
            raise ValueError(f"pin_sides: {net}: supply side {s!r} (use W and/or E)")
        if side not in out:
            out.append(side)
    return out


def two_row(cell, name: str, order_n=None, order_p=None, dummy_l: float = 1.0,
            pin_sides: dict | None = None) -> Result:
    """Build the cell. order_n / order_p: device names left->right (default: netlist order).
    pin_sides: {"default": side, <pin net>: side}, side W/E/N/S (left/right/top/bottom); edge
    pins leave the cell on that side (default: every pin on the left, W). VSS / VDD take a list
    of W and/or E (met1 strap to each listed edge; default [W])."""
    # one ground name: the layout's substrate / guard rings are labelled VSS, so a cell that
    # calls its ground GND or 0 (DAC, DAC_signed) is drawn and LVS-referenced as VSS
    alias = [n for n in GROUND if n != "VSS"]
    hit = set()
    for obj, terms in [(f, "dgsb") for f in cell.fets] + [(c, ("top", "bot")) for c in cell.caps]:
        for t in terms:
            if getattr(obj, t) in alias:
                hit.add(getattr(obj, t)); setattr(obj, t, "VSS")
    if hit:
        cell.pins = ["VSS" if p in alias else p for p in cell.pins]
        cell.pins = list(dict.fromkeys(cell.pins))
        cell.log.append(f"ground net {', '.join(sorted(hit))} drawn as VSS")
    nm = [cell.by_name(n) for n in order_n] if order_n else cell.nmos
    pm = [cell.by_name(n) for n in order_p] if order_p else cell.pmos
    if not nm or not pm:
        raise ValueError("two_row needs at least one NMOS and one PMOS")
    for f in nm + pm:
        if (f.kind == "p" and f.b != "VDD") or f.m != 1:
            raise ValueError(f"{f.name}: need {'body VDD and ' if f.kind == 'p' else ''}m=1 "
                             f"(got body {f.b}, m={f.m})")
    caps = list(cell.caps)
    if len(caps) > 2 or len({c.bot for c in caps}) > 1:
        raise NotImplementedError("two_row supports <= 2 caps that share one bottom-plate net "
                                  f"(got {[(c.name, c.bot) for c in caps]})")
    cap_bot = caps[0].bot if caps else None      # net of the met4 spine
    pins = list(cell.pins)
    for rail in ("VSS", "VDD"):          # the layout always has a substrate (VSS) and VDD wells
        if rail not in pins:
            pins.append(rail)
    pnames = {f.name for f in pm}

    top = Component(f"{name}_build")
    R = Router(pdk, top)

    # ------------------------------------------------------------------ NMOS row in DNW(s)
    # Ground-body NMOS share one DNW (first); every other body net gets its own island:
    # dummy ring on that net, p+ body ring on that net, DNW tie to VDD, substrate ring to VSS.
    by_body = {}
    for f in nm:
        by_body.setdefault("VSS" if f.b in GROUND else f.b, []).append(f)
    bodies = (["VSS"] if "VSS" in by_body else []) + [b for b in by_body if b != "VSS"]
    nref, wells, cursor = {}, [], 0.0
    for k, body in enumerate(bodies):
        refs = _row(top, by_body[body])
        main = body == "VSS"
        dn_k = dummy_ring(pdk, top, list(refs.values()), "n", length=dummy_l,
                          name="DN" if main else f"DNI{k}", rail=body)
        g_k = dnw_guard(pdk, top, list(refs.values()) + [dn_k.ref], body=body, dnw="VDD", sub="VSS",
                        name="dnw_guard" if main else f"dnw_guard_{body}")
        rt = top << straight_route(pdk, dn_k.ports["rail_N"], g_k.ports["body_N_top_met_S"])
        if k:                            # islands go right of the previous guard
            dx = _snap(cursor - g_k.ref.xmin)
            for o in list(refs.values()) + [dn_k.ref, g_k.ref, rt]:
                o.movex(dx)
        cursor = g_k.ref.xmax + ISLAND_GAP
        nref.update(refs)
        wells.append(dict(body=body, dn=dn_k, g=g_k))
    g = wells[0]["g"]                    # leftmost guard: VSS pin label
    n_xmin = min(w["g"].ref.xmin for w in wells)
    n_xmax = max(w["g"].ref.xmax for w in wells)
    n_ymin = min(w["g"].ref.ymin for w in wells)
    n_ymax = max(w["g"].ref.ymax for w in wells)

    # ------------------------------------------------------------------ PMOS row (built at y=0)
    ncx = (min(r.xmin for r in nref.values()) + max(r.xmax for r in nref.values())) / 2
    pref = _row(top, pm)
    p0, p1 = min(r.xmin for r in pref.values()), max(r.xmax for r in pref.values())
    for r in pref.values():
        r.movex(_snap(ncx - (p0 + p1) / 2))
    dp = dummy_ring(pdk, top, list(pref.values()), "p", length=dummy_l, name="DP")
    ng = nwell_guard(pdk, top, list(pref.values()) + [dp.ref], body="VDD")
    p_rail = top << straight_route(pdk, dp.ports["rail_N"], ng.ports["body_N_top_met_S"])
    pmos_objs = list(pref.values()) + [dp.ref, ng.ref, p_rail]

    # supply / body columns (met3, over the dummy side columns): (net, x, ring ys, tag)
    cols = []
    for w in wells:
        d, gw = w["dn"].ref, w["g"]
        yb_body, yb_sub = _ring_y(gw.ports["body_N_top_met_N"]), _ring_y(gw.ports["sub_N_top_met_S"])
        y_dnw = _ring_y(gw.ports["dnw_N_top_met_N"])
        if w["body"] == "VSS":           # body ring -> sub ring -> VSS track; DNW tie -> VDD
            cols += [("VSS", d.xmin + 0.8, [yb_body, yb_sub], "vss-col"),
                     ("VDD", d.xmax - 0.8, [y_dnw], "dnw-col")]
        else:                            # island: body ring -> body net; sub ring -> VSS
            cols += [(w["body"], d.xmin + 0.8, [yb_body], "isl-body-col"),
                     ("VSS", d.xmin + 0.8 + PITCH, [yb_sub], "isl-sub-col"),
                     ("VDD", d.xmax - 0.8, [y_dnw], "isl-dnw-col")]
    x_vss = next(x for n, x, _y, _t in cols if n == "VSS")

    ns_pins = [n for n in pins if _pin_side(pin_sides, n) in "NS"]
    _chans0 = {}
    for net, *_r, ch, _t in _risers(nref, nm) + _risers(pref, pm):
        _chans0.setdefault(net, set()).add(ch)

    def pin_ch(net):
        """Channel whose track carries the pin out: N prefers top, S bot, E/W the first."""
        have = _chans0.get(net, set()) | ({"mid"} if net == cap_bot else set())
        pref_order = {"N": ("top", "mid", "bot"), "S": ("bot", "mid", "top")}.get(
            _pin_side(pin_sides, net), ("bot", "mid", "top"))
        return next((c for c in pref_order if c in have), None)

    def plan(sh):
        terms = _risers(nref, nm) + [(n, x + sh, y, c, t) for n, x, y, c, t in _risers(pref, pm)]
        chans_of = {}
        for net, *_r, ch, _t in terms:
            chans_of.setdefault(net, set()).add(ch)
        for net, *_c in cols:
            chans_of.setdefault(net, set()).add("mid")
        chans_of.setdefault("VDD", set()).add("mid")
        if cap_bot:
            chans_of.setdefault(cap_bot, set()).add("mid")
        cross = sorted(n for n, c in chans_of.items() if len(c) > 1)
        left = min(n_xmin, ng.ref.xmin + sh) - 1.0
        col_x = {n: left - i * PITCH for i, n in enumerate(cross)}
        pin_x = left - len(cross) * PITCH - 0.6
        # strip right of the rows (before the cap spine): N/S pin risers, then the E turn column
        rows_x = max(n_xmax, ng.ref.xmax + sh)
        ns_x = {net: rows_x + 0.8 + k * NS_PITCH for k, net in enumerate(ns_pins)}
        x_sp = rows_x + 2.4 + len(ns_pins) * NS_PITCH
        x_er = x_sp - 1.6                                # E pins: met4 -> met2 turn column
        cap_x = {c.top: x_sp - 0.8 - i * CAP_PITCH for i, c in enumerate(caps)}
        x_ntap = ng.ref.xmin + sh + 0.8
        extra = {}                       # mid-channel x points of the supply / body columns
        for net, x, _ys, _t in cols:
            extra.setdefault(net, []).append(x)
        extra.setdefault("VDD", []).append(x_ntap)
        if cap_bot:
            extra.setdefault(cap_bot, [])

        def spans(ch):
            sp = {}
            for net, x, _y, c, _t in terms:
                if c == ch:
                    lo, hi = sp.get(net, (x, x)); sp[net] = (min(lo, x), max(hi, x))
            for net in list(sp) + ([n for n in extra if n not in sp] if ch == "mid" else []):
                xs = extra.get(net, []) if ch == "mid" else []
                lo, hi = sp.get(net, (min(xs), max(xs)) if xs else (0.0, 0.0))
                if xs:
                    lo, hi = min(lo, *xs), max(hi, *xs)
                if net in col_x:
                    lo = min(lo, col_x[net])
                if net in pins and net not in ("VSS", "VDD") and pin_ch(net) == ch:
                    side = _pin_side(pin_sides, net)
                    if side == "W":
                        lo = min(lo, pin_x)      # left edge-pin column
                    elif side == "E":
                        hi = max(hi, x_er)       # right turn column (stops before the cap spine)
                    else:
                        hi = max(hi, ns_x[net])  # own N/S riser column
                elif net in pins and net not in ("VSS", "VDD") and _pin_side(pin_sides, net) == "W":
                    lo = min(lo, pin_x)          # (left pins: every channel reaches the column)
                if ch == "mid" and net == cap_bot:
                    hi = max(hi, x_sp)
                if ch == "mid" and net in cap_x:
                    hi = max(hi, cap_x[net])
                sp[net] = (lo, hi)
            return sp

        tracks = {}
        for ch in ("bot", "mid", "top"):
            sp = spans(ch)
            idx, n = pack_tracks(sp)
            if ch == "mid":     # NMOS-heavy tracks low, PMOS-heavy high
                score = [0] * n
                for net, _x, _y, c, tag in terms:
                    if c == "mid":
                        score[idx[net]] += 1 if tag.split(".")[0] in pnames else -1
                order = sorted(range(n), key=lambda t: score[t])
                remap = {old: new for new, old in enumerate(order)}
                idx = {k: remap[v] for k, v in idx.items()}
            # edge pins at least 2 tracks apart: a top-level router lands a via just outside
            # the cell for every pin; at 1 track pitch a middle pin is walled in by its
            # neighbours' landings (row_111 test: VMEM between Vamp_bias and VT)
            pin_tr = {i for net, i in idx.items() if net in pins and net not in ("VSS", "VDD")}
            if pin_tr:
                new, k, prev = {}, 0, False
                for t in range(n):
                    if t in pin_tr and prev:
                        k += PIN_BLANK_TRACKS        # blank tracks between two pin tracks
                    new[t], k, prev = k, k + 1, t in pin_tr
                idx = {net: new[i] for net, i in idx.items()}
                n = k
            tracks[ch] = (sp, idx, n)

        mid = tracks["mid"][1]
        nr = [(x, net, mid[net]) for net, x, _y, c, t in terms
              if c == "mid" and t.split(".")[0] not in pnames]
        pr = [(x, net, mid[net]) for net, x, _y, c, t in terms
              if c == "mid" and t.split(".")[0] in pnames]
        nr += [(x, net, mid[net]) for net, x, _ys, _t in cols]
        pr += [(x_ntap, "VDD", mid["VDD"])]
        bad = [(a, b) for a in nr for b in pr
               if a[1] != b[1] and abs(a[0] - b[0]) < PITCH and a[2] >= b[2]]
        return len(bad), dict(terms=terms, chans_of=chans_of, cross=cross, col_x=col_x, pin_x=pin_x,
                              ns_x=ns_x, x_er=x_er, pin_ch={n: pin_ch(n) for n in pins},
                              x_sp=x_sp, cap_x=cap_x, x_ntap=x_ntap, tracks=tracks, bad=bad)

    best = None
    for k in sorted(range(-80, 81), key=abs):
        nbad, p = plan(k * 0.05)
        if best is None or nbad < best[0]:
            best = (nbad, k * 0.05, p)
        if nbad == 0:
            break
    nbad, sh, P = best
    if nbad:
        raise RuntimeError(f"{nbad} riser conflicts at best shift {sh:+.2f}: {P['bad'][:4]}; "
                           f"try another device order or a larger GAP")
    for o in pmos_objs:
        o.movex(sh)
    chans_of, cross, col_x = P["chans_of"], P["cross"], P["col_x"]
    x_sp, cap_x, tracks, x_ntap = P["x_sp"], P["cap_x"], P["tracks"], P["x_ntap"]

    y_mid0 = n_ymax + CH_MARGIN
    n_mid = tracks["mid"][2]
    dy = y_mid0 + (n_mid - 1) * PITCH + CH_MARGIN - ng.ref.ymin
    for o in pmos_objs:
        o.movey(dy)
    y0 = {"mid": y_mid0,
          "bot": n_ymin - CH_MARGIN - (tracks["bot"][2] - 1) * PITCH,
          "top": ng.ref.ymax + CH_MARGIN}
    track_y = {(ch, net): y0[ch] + i * PITCH
               for ch, (sp, idx, n) in tracks.items() for net, i in idx.items()}

    # ------------------------------------------------------------------ tracks, risers, buses
    for ch, (sp, idx, n) in tracks.items():
        for net, (lo, hi) in sp.items():
            y = track_y[(ch, net)]
            R.wire("met4", (lo, y), (hi, y), net, tag=f"trk-{ch}")
    for net, x, yb, ch, tag in _risers(nref, nm) + _risers(pref, pm):
        yt = track_y[(ch, net)]
        R.via(x, yb, "met2", "met3", net, tag)
        R.via(x, yt, "met3", "met4", net, tag)
        R.wire("met3", (x, yb), (x, yt), net, tag=tag)
    for f in nm + pm:
        r = nref.get(f.name) or pref[f.name]
        for term, net in (("drain", f.d), ("gate", f.g), ("source", f.s)):
            x0, x1, y = bus(r, term)
            R.record("met2", x0 - WIRE / 2, y - WIRE / 2, x1 + WIRE / 2, y + WIRE / 2, net, "bus")

    # ------------------------------------------------------------------ cross-channel columns
    for net, x in col_x.items():
        ys = [track_y[(ch, net)] for ch in chans_of[net]]
        for y in ys:
            R.via(x, y, "met3", "met4", net, "col")
        R.wire("met3", (x, min(ys)), (x, max(ys)), net, tag="col")

    # ------------------------------------------------------------------ supply columns
    y_vss = track_y[("mid", "VSS")]
    for net, x, ys, tag in cols + [("VDD", x_ntap, [_ring_y(ng.ports["body_S_top_met_S"])], "ntap-col")]:
        yt = track_y[("mid", net)]
        for y in ys:
            R.via(x, y, "met2", "met3", net, tag)
        R.via(x, yt, "met3", "met4", net, tag)
        R.wire("met3", (x, min(ys + [yt])), (x, max(ys + [yt])), net, tag=tag)

    # ------------------------------------------------------------------ caps (0: above, 1: below)
    placed = []
    for i, c in enumerate(caps):
        # no extension tab: glayout lifts the bottom plate to met5 on it, which the met5
        # top-plate links would cross; the met4 spine touches the bottom plate instead.
        m = top << mimcap(pdk, (c.w, c.l), with_extension=False)
        if i == 0:
            m.move((x_sp + CAP_GAP - m.xmin, ng.ref.ymin - m.ymin))
        else:
            m.move((x_sp + CAP_GAP - m.xmin, y_mid0 - 1.2 - m.ymax))
        hx, hy = c.w / 2 - 0.28, c.l / 2 - 0.28
        R.shapes["met5"].append((m.center[0] - hx, m.center[1] - hy,
                                 m.center[0] + hx, m.center[1] + hy, c.top, c.name))
        R.shapes["met4"].append((m.xmin, m.ymin, m.xmax, m.ymax, c.bot, c.name))
        # MIMTM.1 keep-out on the PR boundary layer (0/0, not checked by DRC/LVS): the cell
        # outline then reaches 1.3 um past the plate, so a top-level router that only sees cell
        # outlines keeps other met4 >= 1.2 um away (row_111: router met4 0.87 um from DPI's cap)
        kb = top << rectangle(size=(m.xsize + 2 * MIM_KEEPOUT, m.ysize + 2 * MIM_KEEPOUT), layer=(0, 0))
        kb.move((m.xmin - MIM_KEEPOUT - kb.xmin, m.ymin - MIM_KEEPOUT - kb.ymin))
        placed.append((c, m))
    if placed:
        ys = [m.center[1] for _, m in placed] + [track_y[("mid", cap_bot)]]
        R.wire("met4", (x_sp, min(ys)), (x_sp, max(ys)), cap_bot, tag="spine")
        for c, m in placed:
            R.wire("met4", (x_sp, m.center[1]), (m.xmin + 0.3, m.center[1]), c.bot, tag=c.name)
            x, y, yc = cap_x[c.top], track_y[("mid", c.top)], m.center[1]
            R.via(x, y, "met4", "met5", c.top, "cap")
            R.wire("met5", (x, y), (x, yc), c.top, w=1.0, tag="cap")
            R.wire("met5", (x, yc), (m.center[0], yc), c.top, w=1.0, tag=c.name)

    # ------------------------------------------------------------------ pins
    notes = []
    lab = pdk.get_glayer("met4_label")
    labelled = set()
    for (ch, net), y in track_y.items():
        if net in pins and net not in ("VSS", "VDD") and net not in labelled:
            top.add_label(text=net, position=(tracks[ch][0][net][0] + 0.1, y), layer=lab)
            labelled.add(net)
    for net, port in (("VSS", g.ports["sub_S_top_met_S"]), ("VDD", ng.ports["body_N_top_met_N"])):
        top.add_label(text=net, position=(port.center[0], _ring_y(port)),
                      layer=pdk.get_glayer("met2_label"))
    for p in pins:
        if p not in labelled | {"VSS", "VDD"}:
            notes.append(f"pin {p} has no metal in this cell (unconnected in the netlist?)")

    # ------------------------------------------------------------------ edge pins
    # top-level routers reach a block from outside on met1/met2/met3: every pin net gets a stub
    # that ends exactly on the cell edge of its side (pin_sides):
    #   W  met2 stub from the left pin column          E  met2 stub from the right turn column
    #   N  met3 riser up from the top-most use          S  met3 riser down
    # (E runs on met4 only up to x_er, before the cap spine and the MIM plates, then on met2)
    pin_x, x_er, ns_x = P["pin_x"], P["x_er"], P["ns_x"]
    x_edge = pin_x - 1.3          # the cell's left edge: every stub's metal ends exactly here
    (bx0, by0), (bx1, by1) = top.bbox
    x_redge, y_top, y_bot = float(bx1), float(by1), float(by0)
    edge_ports = []
    for net in pins:
        if net in ("VSS", "VDD"):
            continue
        ch = P["pin_ch"].get(net)
        if ch is None or (ch, net) not in track_y:
            continue
        y = track_y[(ch, net)]
        side = _pin_side(pin_sides, net)
        if side == "W":
            R.via(pin_x, y, "met3", "met4", net, "edge-pin")
            R.via(pin_x, y, "met2", "met3", net, "edge-pin")
            R.wire("met2", (x_edge + WIRE / 2, y), (pin_x, y), net, tag="edge-pin")   # wire() adds w/2 caps
            edge_ports.append(dict(net=net, layer="met2", x=round(x_edge, 4), y=round(y, 4),
                                   orientation=180, width=WIRE))
        elif side == "E":
            R.via(x_er, y, "met3", "met4", net, "edge-pin")
            R.via(x_er, y, "met2", "met3", net, "edge-pin")
            R.wire("met2", (x_er, y), (x_redge - WIRE / 2, y), net, tag="edge-pin")
            edge_ports.append(dict(net=net, layer="met2", x=round(x_redge, 4), y=round(y, 4),
                                   orientation=0, width=WIRE))
        else:
            x = ns_x[net]
            R.via(x, y, "met3", "met4", net, "edge-pin")
            ye = y_top if side == "N" else y_bot
            R.wire("met3", (x, y), (x, ye - WIRE / 2 if side == "N" else ye + WIRE / 2), net, tag="edge-pin")
            edge_ports.append(dict(net=net, layer="met3", x=round(x, 4), y=round(ye, 4),
                                   orientation=90 if side == "N" else 270, width=WIRE))
    # supply straps: met1 from the substrate (VSS) / n-tap (VDD) ring side to each listed edge
    g_e = max((w["g"] for w in wells), key=lambda gw: gw.ref.xmax)   # rightmost guard (VSS sub ring)
    for net, ring_w, ring_e in (("VSS", g.ports["sub_W_top_met_W"], g_e.ports["sub_E_top_met_E"]),
                                ("VDD", ng.ports["body_W_top_met_W"], ng.ports["body_E_top_met_E"])):
        for side in _supply_sides(pin_sides, net):
            port = ring_w if side == "W" else ring_e
            x_r, y_r = float(port.center[0]), float(port.center[1])
            if side == "W":
                R.wire("met1", (x_edge + 0.5, y_r), (x_r + 0.3, y_r), net, w=1.0, tag="edge-pin")
            else:
                R.wire("met1", (x_r - 0.3, y_r), (x_redge - 0.5, y_r), net, w=1.0, tag="edge-pin")
            edge_ports.append(dict(net=net, layer="met1", x=round(x_edge if side == "W" else x_redge, 4),
                                   y=round(y_r, 4), orientation=180 if side == "W" else 0, width=1.0))

    # ------------------------------------------------------------------ LVS reference
    ref = []
    for f in nm + pm:
        model = "nfet_03v3" if f.kind == "n" else "pfet_03v3"
        for k in range(f.nf):           # LVS extracts one device per finger, W per finger
            sfx = f"_f{k}" if f.nf > 1 else ""
            ref.append(f"X{f.name}{sfx} {f.d} {f.g} {f.s} {f.b} {model} L={f.l:g}u W={f.w:g}u nf=1")
    for c in caps:
        # the PDK's spice->CDL converter strips one leading X; what is left must start with C
        # to be read as a capacitor (a cap from a subcell, x1_C2, would become a subckt call)
        cname = c.name if c.name.upper().startswith("C") else f"C{c.name}"
        ref.append(f"X{cname} {c.top} {c.bot} cap_mim_2f0fF c_width={c.w:g}e-6 "
                   f"c_length={c.l:g}e-6 m=1")
    ref += [line for w in wells for line in w["dn"].spice] + dp.spice
    islands = [w["body"] for w in wells if w["body"] != "VSS"]
    summary = (f"{name}: {len(nm)} NMOS + {len(pm)} PMOS + {len(caps)} caps, "
               + (f"{len(islands)} isolated NMOS body island(s) ({', '.join(islands)}), " if islands else "")
               + 
               f"tracks bot/mid/top {tracks['bot'][2]}/{n_mid}/{tracks['top'][2]}, "
               f"{len(cross)} columns, PMOS shift {sh:+.2f}")
    return Result(name, top, R, ref, pins, summary, notes + cell.log, edge_ports)


def write_cell(res: Result, out_dir: str | Path, report_nets=None) -> str:
    """Flatten + write <name>.gds, <name>_lvs_ref.spice, <name>_pred.spice; run predictions."""
    from glayout_predrc import predrc
    import json
    from glayout_parasitics import predict_caps, report, inject_caps, save_shapes
    out = Path(out_dir)
    flat = res.top.flatten()
    flat.name = res.name
    gds = out / f"{res.name}.gds"
    flat.write_gds(str(gds))
    ref = out / f"{res.name}_lvs_ref.spice"
    ref.write_text(f"* LVS reference for {res.name}.gds (glayout_floorplan.two_row)\n"
                   + "".join(f"* note: {n}\n" for n in res.notes)
                   + f".subckt {res.name} {' '.join(res.pins)}\n"
                   + "\n".join(res.ref_lines) + "\n.ends\n")
    caps = predict_caps(res.router.shapes, cell=res.name)
    n = inject_caps(ref, out / f"{res.name}_pred.spice", caps, subckt=res.name)
    save_shapes(res.router.shapes, out / f"{res.name}.shapes.json")
    (out / f"{res.name}_pins.json").write_text(json.dumps(dict(
        cell=res.name, units="um", origin="GDS coordinates",
        bbox=[round(flat.xmin, 4), round(flat.ymin, 4), round(flat.xmax, 4), round(flat.ymax, 4)],
        ports=res.edge_ports or []), indent=1))
    nets = report_nets or [p for p in res.pins if p not in ("VSS", "VDD")][:6]
    short = res.router.check()
    pre = predrc(str(gds))
    (out / f"{res.name}.build.json").write_text(json.dumps(dict(
        cell=res.name, size_um=[round(flat.xsize, 2), round(flat.ysize, 2)],
        router_check=short or "clean", predrc=pre, summary=res.summary, notes=res.notes,
        predicted_fF={k: round(v["total"] * 1e15, 1) for k, v in sorted(caps.items())}), indent=1))
    lines = [res.summary, f"cell {flat.xsize:.2f} x {flat.ysize:.2f} um -> {gds.name}",
             "router check: " + (short or "clean"), pre,
             "predicted parasitic C:", report(caps, nets=nets),
             f"wrote {ref.name}, {res.name}_pred.spice (+{n} predicted caps), "
             f"{res.name}.shapes.json, {res.name}.build.json"]
    lines += [f"note: {x}" for x in res.notes]
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from glayout_netlist import from_schematic
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("schematic", help=".sch or .spice")
    ap.add_argument("--name", required=True)
    ap.add_argument("--connect", action="append", default=[], help="NET=TO (schematic fix)")
    ap.add_argument("--order-n", help="comma-separated NMOS order")
    ap.add_argument("--order-p", help="comma-separated PMOS order")
    ap.add_argument("--dummy-l", type=float, default=1.0)
    ap.add_argument("--out", default=".")
    ap.add_argument("--decisions", help="<cell>.layout.yaml from decide.py (order, dummy_l)")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()
    cell = from_schematic(a.schematic).legalize()
    for c in a.connect:
        cell.connect(*c.split("=", 1))
    for w in cell.warnings():
        print("WARNING", w)
    order_n, order_p, dummy_l = (a.order_n and a.order_n.split(","),
                                 a.order_p and a.order_p.split(","), a.dummy_l)
    if a.decisions:
        import yaml
        from decide import two_row_args
        order_n, order_p, dummy_l = two_row_args(yaml.safe_load(open(a.decisions)))
    res = two_row(cell, a.name, order_n, order_p, dummy_l)
    print(write_cell(res, a.out))
    if a.show:
        res.top.flatten().show()
