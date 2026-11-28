"""
Fast DRC prediction for GF180 gLayout cells (KLayout geometry engine, ~1 s).

    from glayout_predrc import predrc
    print(predrc("neuron.gds"))          # or predrc(component)

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python glayout_predrc.py cell.gds

Runs a small subset of the GF180 deck: the rules that actually failed while building cells
with gLayout, plus the cheap metal width/space rules. Each check mirrors the real deck's
formulation (rule decks in $PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/rule_decks), so a
predicted error is a real error. It is a pre-filter, not a signoff: a clean result means
"run the real DRC now", not "DRC clean".

Add a rule when a real DRC run finds something this misses: one function in RULES.
"""
from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

import klayout.db as kdb

# GF180 GDS layers (layers_def.drc)
L = {"comp": (22, 0), "dnwell": (12, 0), "nwell": (21, 0), "lvpwell": (204, 0),
     "poly2": (30, 0), "nplus": (32, 0), "pplus": (31, 0), "fusetop": (75, 0),
     "cap_mk": (117, 5), "res_mk": (110, 5), "metal1": (34, 0), "metal2": (36, 0), "metal3": (42, 0),
     "metal4": (46, 0), "metal5": (81, 0), "via4": (41, 0)}
LABEL_DT = 10                      # metalN label = (metalN layer, 10)
METAL_WS = {"metal1": (0.23, 0.23), "metal2": (0.28, 0.28), "metal3": (0.28, 0.28),
            "metal4": (0.28, 0.28), "metal5": (0.28, 0.28)}   # M*.1 width, M*.2a space


class Geo:
    """Merged flat regions of one top cell, in database units."""

    def __init__(self, layout: kdb.Layout):
        self.ly = layout
        self.top = layout.top_cell()
        self.dbu = layout.dbu
        self._r = {}

    def __getitem__(self, name):
        if name not in self._r:
            ln, dt = L[name]
            li = self.ly.find_layer(ln, dt)
            r = kdb.Region() if li is None else kdb.Region(self.top.begin_shapes_rec(li))
            self._r[name] = r.merged()
        return self._r[name]

    def um(self, x):
        return int(round(x / self.dbu))


def _ep(ep_or_region, dbu):
    """(count, first location string) of an EdgePairs/Region result."""
    n = ep_or_region.count() if hasattr(ep_or_region, "count") else ep_or_region.size()
    if n == 0:
        return 0, ""
    first = next(iter(ep_or_region.each()))
    b = first.bbox()
    return n, f"({b.left * dbu:.2f},{b.bottom * dbu:.2f})"


# ----------------------------------------------------------------------------- rules
def r_metal(g):
    out = []
    for m, (w, s) in METAL_WS.items():
        r = g[m]
        n = m[-1]
        out.append((f"M{n}.1 width<{w}", *_ep(r.width_check(g.um(w)), g.dbu)))
        out.append((f"M{n}.2a space<{s}", *_ep(r.space_check(g.um(s)), g.dbu)))
    return out


def r_implant(g):
    return [(f"{k.upper()[0]}P.2 space<0.4", *_ep(g[k].space_check(g.um(0.4)), g.dbu))
            for k in ("nplus", "pplus")]


def r_mim(g):
    # mim_b.drc: mimtm_virtual = fusetop.sized(1.06).and(metal4.interacting(fusetop))
    #            MIMTM.1 = metal4.separation(mimtm_virtual, transparent, 1.2)
    ft = g["fusetop"]
    if ft.is_empty():
        return []
    virt = ft.sized(g.um(1.06)) & g["metal4"].interacting(ft)
    ep = g["metal4"].separation_check(virt, g.um(1.2), False, kdb.Metrics.Euclidian,
                                      None, None, None, False)
    return [("MIMTM.1 met4-to-MIM bottom plate<1.2", *_ep(ep, g.dbu))]


def r_wells(g):
    dnw, nw, lpw = g["dnwell"], g["nwell"], g["lvpwell"]
    pcomp = g["comp"] & g["pplus"]
    sub_pcomp = (pcomp - nw) - dnw
    out = []
    if not dnw.is_empty():
        out.append(("NW.3 nwell-to-DNWELL<3.1",
                    *_ep((nw - dnw).separation_check(dnw, g.um(3.1)), g.dbu)))
        out.append(("DF.18 DNWELL-to-sub PCOMP<2.5",
                    *_ep(dnw.separation_check(sub_pcomp, g.um(2.5)), g.dbu)))
        out.append(("LPW.3 DNWELL enclose LVPWELL<2.5",
                    *_ep(dnw.enclosing_check(lpw & dnw, g.um(2.5)), g.dbu)))
        holes = sub_pcomp.holes()
        out.append(("DN.3 DNWELL not inside a p+ substrate ring",
                    *_ep(dnw.not_inside(holes), g.dbu)))
        out.append(("LPW.11 LVPWELL outside DNWELL", *_ep(lpw - dnw, g.dbu)))
    out.append(("LPW.12 LVPWELL overlaps NWELL", *_ep(lpw & nw, g.dbu)))
    return out


def r_nwell_res(g):
    # nwell.drc: NW.1b width of n-well under RES_MK >= 2; Magic's rnw rules: NW.2b spacing to
    # other n-well >= 1.4 (the deck's conn_space uses 1.4 for unconnected n-wells), DN.12
    mk = g["res_mk"]
    if mk.is_empty():
        return []
    nw = g["nwell"]
    res = nw.interacting(mk)
    other = nw - res
    return [("NW.1b n-well resistor width<2", *_ep((nw & mk).width_check(g.um(2.0)), g.dbu)),
            ("NW.2b n-well resistor to other n-well<1.4", *_ep(res.separation_check(other, g.um(1.4)), g.dbu)),
            ("NW.2b n-well resistor bars<1.4", *_ep(res.space_check(g.um(1.4)), g.dbu)),
            ("DN.12 n-well resistor in DNWELL", *_ep(res & g["dnwell"], g.dbu))]


def r_labels(g):
    """LVS: every pin label must sit on metal of its own layer (else the net is unnamed)."""
    bad, first = 0, ""
    for m in ("metal1", "metal2", "metal3", "metal4", "metal5"):
        li = g.ly.find_layer(L[m][0], LABEL_DT)
        if li is None:
            continue
        metal = g[m]
        it = g.top.begin_shapes_rec(li)
        while not it.at_end():
            sh = it.shape()
            if sh.is_text():
                p = it.trans() * sh.text.trans.disp
                pt = kdb.Box(p.x - 1, p.y - 1, p.x + 1, p.y + 1)
                if (kdb.Region(pt) & metal).is_empty():
                    bad += 1
                    first = first or f"'{sh.text.string}' ({p.x * g.dbu:.2f},{p.y * g.dbu:.2f})"
            it.next()
    return [("LBL label not on its metal", bad, first)]


RULES = [r_metal, r_implant, r_mim, r_wells, r_nwell_res, r_labels]


# ----------------------------------------------------------------------------- entry
def predrc(src, show_clean: bool = False) -> str:
    """Predict DRC errors. src: GDS path or gdsfactory Component. Returns a short report."""
    t0 = time.time()
    if not isinstance(src, (str, Path)):
        tmp = Path(tempfile.mkdtemp()) / "predrc.gds"
        src.write_gds(str(tmp))
        src = tmp
    ly = kdb.Layout()
    ly.read(str(src))
    g = Geo(ly)
    rows = [row for rule in RULES for row in rule(g)]
    bad = [r for r in rows if r[1]]
    lines = [f"predrc {ly.top_cell().name}: {len(bad)} rule(s) predicted to fail "
             f"({len(rows)} checked, {time.time() - t0:.1f} s)"]
    for name, n, where in (rows if show_clean else bad):
        lines.append(f"  {'FAIL' if n else 'ok  '} {name}: {n} {where}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(predrc(sys.argv[1], show_clean="-v" in sys.argv))
