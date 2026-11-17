"""
Layout decisions before layout: wells / DNW islands, dummy rings, guard rings, placement.

    env -u PYTHONPATH .venv-glayout/bin/python analog/layout_tools/decide.py analog/DAC/DAC_binary.sch
        -> analog/layout_tools/DAC_binary.layout.yaml (or --out; + a short review on stdout)

    from decide import decide, review, two_row_args
    dec = decide(cell)                       # cell from glayout_netlist
    print(review(dec))
    order_n, order_p, dummy_l = two_row_args(dec)   # raises if two_row can't do it yet

How decisions are made, in order of authority:
  rule      forced by the netlist + PDK (e.g. NMOS body != ground needs an isolated DNW;
            every DNW needs a p+ substrate ring, DN.3). Not optional.
  policy    project defaults from layout_policy.yaml (e.g. "every NMOS in a DNW").
  designer  anything you edit in <cell>.layout.yaml: set `decided_by: designer` on that item
            and re-running decide.py keeps it.
Items that need a judgement the netlist can't supply go to `questions`.

Structure recognition (from topology only):
  inverter      NMOS + PMOS, same gate, same drain              -> drain net is "switching"
  diff_pair     2 same-type, same W/L/nf, common non-rail source, different gates
  mirror        >= 2 same-type, same gate + source + L (diode device D=G if present)
  binary_array  a mirror whose unit counts (W*nf*m) are 1:2:4:8...
  switch        gate on a digital pin (gate-only pin, all gated L <= switch_max_l) or on a
                switching net
Net classes: rail, integrating (cap top plate), switching, digital_pin, bias_pin, signal.
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
POLICY = HERE / "layout_policy.yaml"

RING_STACK = 6.4     # um per side: DNW guard stack (body ring .. substrate ring), measured
DN_SPACE = 5.42      # um, DN.2b: DNW to DNW (different potential)


def load_policy(path=POLICY) -> dict:
    return yaml.safe_load(Path(path).read_text())


def footprint(f):
    """(w, h) estimate of a glayout FET in um (fit to measured bboxes, no dummies)."""
    return f.nf * (f.l + 0.9) + 1.0, f.w + 3.13


def _units(f):
    return f.w * f.nf * f.m


# ----------------------------------------------------------------------------- nets
def classify_nets(cell, pol):
    gnd, sup = set(pol["rails"]["ground"]), set(pol["rails"]["supply"])
    use = defaultdict(lambda: defaultdict(list))
    for f in cell.fets:
        for t in "dgsb":
            use[getattr(f, t)][t].append(f)
    caps_top = {c.top for c in cell.caps}
    inv_out = set()
    for n in cell.nmos:
        for p in cell.pmos:
            if n.g == p.g and n.d == p.d:
                inv_out.add(n.d)
    out = {}
    for net, k in use.items():
        if net in gnd or net in sup:
            out[net] = ("rail", "ground" if net in gnd else "supply")
        elif net in inv_out:
            out[net] = ("switching", "inverter output" + (" (with cap)" if net in caps_top else ""))
        elif net in caps_top:
            out[net] = ("integrating", "top plate of a capacitor")
        elif net in cell.pins and set(k) == {"g"}:
            ls = [f.l for f in k["g"]]
            series = any(f.s not in gnd | sup for f in k["g"])
            if max(ls) <= pol["devices"]["switch_max_l"] and series:
                out[net] = ("digital_pin", f"gate-only pin, short L, drives a series switch")
            else:
                out[net] = ("bias_pin", "gate-only pin driving current sources / long-L devices")
        else:
            out[net] = ("signal", "")
    return out


# ----------------------------------------------------------------------------- structures
def find_groups(cell, nets, pol):
    used, groups = set(), []
    gnd = set(pol["rails"]["ground"]); sup = set(pol["rails"]["supply"])

    def add(kind, devs, **kw):
        groups.append(dict(id=f"G{len(groups) + 1}", type=kind, devices=[d.name for d in devs],
                           decided_by="rule", **kw))
        used.update(d.name for d in devs)

    # inverters
    for n in cell.nmos:
        for p in cell.pmos:
            if n.g == p.g and n.d == p.d and n.name not in used and p.name not in used:
                add("inverter", [n, p], placement="free", dummy_ring="none",
                    reason=f"N+P share gate {n.g} and drain {n.d}")
    # diff pairs
    fets = cell.fets
    for i, a in enumerate(fets):
        for b in fets[i + 1:]:
            if (a.name in used or b.name in used or a.kind != b.kind or a.s != b.s
                    or a.s in gnd | sup or a.g == b.g or a.d == b.d
                    or (a.w, a.l, a.nf, a.m) != (b.w, b.l, b.nf, b.m)):
                continue
            tail = [f for f in fets if f.d == a.s and f.name not in used and f not in (a, b)]
            if tail:
                used.add(tail[0].name)          # the tail belongs to the pair
            add("diff_pair", [a, b], tail=tail[0].name if tail else None,
                placement=pol["placement"]["diff_pair"], dummy_ring=pol["dummies"]["matched_groups"],
                dummy_l=a.l, reason=f"same W/L, common source {a.s}, gates {a.g}/{b.g}")
    # mirrors / binary arrays (same gate, source, L)
    key = defaultdict(list)
    for f in fets:
        if f.name not in used and nets.get(f.g, ("",))[0] not in ("digital_pin", "switching"):
            key[(f.kind, f.g, f.s, f.l)].append(f)
    for (kind, g, s, l), devs in key.items():
        if len(devs) < 2:
            continue
        u = sorted(_units(d) for d in devs)
        ratios = [x / u[0] for x in u]
        binary = len(devs) >= 3 and all(abs(math.log2(r) - round(math.log2(r))) < 1e-6
                                        for r in ratios) and len(set(ratios)) > 1
        diode = [d.name for d in devs if d.d == d.g]
        if binary:
            add("binary_array", devs, placement=pol["placement"]["binary_array"],
                dummy_ring=pol["dummies"]["matched_groups"], dummy_l=l,
                ratios=[round(r) for r in ratios],
                reason=f"common gate {g} / source {s}, unit ratios {[round(r) for r in ratios]}")
        else:
            add("mirror", devs, diode=diode or None, placement=pol["placement"]["mirror"],
                dummy_ring=pol["dummies"]["matched_groups"], dummy_l=l,
                reason=f"common gate {g} / source {s}" + (f", diode {diode}" if diode else ""))
    # switches
    for f in fets:
        cls = nets.get(f.g, ("",))[0]
        if f.name not in used and cls in ("digital_pin", "switching"):
            add("switch", [f], placement="free", dummy_ring=pol["dummies"]["switches"],
                reason=f"gate on {cls.replace('_', ' ')} {f.g}")
    return groups


# ----------------------------------------------------------------------------- wells
def decide_wells(cell, pol, groups, questions):
    gnd, sup = set(pol["rails"]["ground"]), set(pol["rails"]["supply"])
    gtype = {d: g["type"] for g in groups for d in g["devices"]}
    by_body = defaultdict(list)
    for f in cell.fets:
        by_body[(f.kind, f.b)].append(f)
    wells = []
    for (kind, body), devs in by_body.items():
        w = sum(footprint(d)[0] for d in devs) + 0.6 * (len(devs) - 1)
        h = max(footprint(d)[1] for d in devs)
        names = [d.name for d in devs]
        if kind == "n":
            if body in gnd:
                dnw = bool(pol["wells"]["nmos_in_dnw"])
                wells.append(dict(id=f"W{len(wells) + 1}", kind="dnw" if dnw else "psub",
                                  body=body, devices=names, required=False, decided_by="policy",
                                  reason=("policy nmos_in_dnw (substrate-noise isolation)" if dnw
                                          else "body on ground: plain substrate is enough"),
                                  cost_um2=round((w + 2 * RING_STACK) * (h + 2 * RING_STACK) - w * h)
                                  if dnw else 0))
            else:
                sw = all(gtype.get(n) == "switch" for n in names)
                src_tied = all(d.s == body for d in devs)
                wid = f"W{len(wells) + 1}"
                cost = round((w + 2 * RING_STACK) * (h + 2 * RING_STACK) - w * h + DN_SPACE * (h + 2 * RING_STACK))
                wells.append(dict(id=wid, kind="dnw", body=body, devices=names, required=True,
                                  decided_by="rule",
                                  reason=f"NMOS body on {body} (not ground): needs its own isolated "
                                         f"p-well in a DNW island",
                                  cost_um2=cost))
                if sw and src_tied and pol["wells"]["propose_body_to_ground_for_switches"]:
                    questions.append(dict(id=f"Q-body-{body}", about=wid,
                                          question=f"{', '.join(names)}: body tied to source {body} "
                                                   f"needs its own DNW island (~{cost} um^2). Tie the "
                                                   f"body to ground instead? (saves the island; body "
                                                   f"effect raises the switch Vt/Ron)",
                                          options=["keep isolated island", "body -> ground"],
                                          default=("body -> ground" if pol.get("decisions", {})
                                                   .get("defaults", {}).get("body_tied_to_source")
                                                   == "ground" else "keep isolated island"),
                                          default_reason="policy decisions.defaults.body_tied_to_source"
                                                         " (keep = circuit unchanged)"))
        else:
            wells.append(dict(id=f"W{len(wells) + 1}", kind="nwell", body=body, devices=names,
                              required=body not in sup, decided_by="rule",
                              reason="PMOS n-well on VDD (shared)" if body in sup
                              else f"PMOS body on {body}: separate n-well island", cost_um2=0))
    return wells


def decide_rings(wells, groups, nets, cell, pol):
    rings = []
    for w in wells:
        if w["kind"] == "dnw":
            rings += [dict(around=w["id"], type="p+ body ring", net=w["body"], required=True,
                           rule="LVPWELL tie"),
                      dict(around=w["id"], type="n+ DNW tie ring", net="VDD", required=True,
                           rule="DNW bias"),
                      dict(around=w["id"], type="p+ substrate ring", net="ground", required=True,
                           rule="DN.3")]
        elif w["kind"] == "nwell":
            rings.append(dict(around=w["id"], type="n+ tap ring", net=w["body"], required=True,
                              rule="DF.13 latch-up (tap within 20 um)"))
        else:
            rings.append(dict(around=w["id"], type="p+ substrate ring", net=w["body"],
                              required=True, rule="DF.14 latch-up (tap within 20 um)"))
    # optional: separate switching from sensitive devices in the same well
    mode = pol["guards"]["separate_switching_from_sensitive"]
    if mode != "never":
        gtype = {d: g["type"] for g in groups for d in g["devices"]}
        for w in wells:
            sw = [d for d in w["devices"] if gtype.get(d) in ("switch", "inverter")]
            sens = [d for d in w["devices"]
                    if gtype.get(d) in ("diff_pair", "mirror", "binary_array")
                    or any(nets.get(getattr(f, t), ("",))[0] == "integrating"
                           for f in cell.fets if f.name == d for t in "dgs")]
            if sw and sens:
                rings.append(dict(around=w["id"], type="extra p+ guard between groups",
                                  required=False, decided_by="policy", enabled=(mode == "always"),
                                  reason=f"switching {sw} share a well with sensitive {sens}"))
    return rings


# ----------------------------------------------------------------------------- floorplan
def decide_floorplan(cell, groups, wells, pol, questions):
    order = {"n": [], "p": []}
    kinds = {f.name: f.kind for f in cell.fets}
    prio = ["diff_pair", "mirror", "binary_array", "inverter", "switch"]
    for t in prio:
        for g in groups:
            if g["type"] != t:
                continue
            seq = ([g["tail"]] if g.get("tail") else []) + g["devices"]
            if t == "mirror" and g.get("diode"):        # diode in the middle
                rest = [d for d in g["devices"] if d not in g["diode"]]
                seq = rest[:len(rest) // 2] + g["diode"] + rest[len(rest) // 2:]
            for d in seq:
                if d not in order[kinds[d]]:
                    order[kinds[d]].append(d)
    for f in cell.fets:
        if f.name not in order[f.kind]:
            order[f.kind].append(f.name)
    matched_l = [g["dummy_l"] for g in groups if g.get("dummy_l") and g.get("dummy_ring") != "none"]
    cap = pol["dummies"]["dummy_l_cap"]
    dl = pol["dummies"]["dummy_l"]
    if dl == "match":
        want = max(matched_l) if matched_l else 1.0
        dummy_l = min(want, cap)
        if want > cap:
            questions.append(dict(id="Q-dummy_l", about="floorplan.dummy_l",
                                  question=f"matched devices have L up to {want:g} um; dummies at "
                                           f"L={want:g} cost area, capped at {cap:g} um now. Keep cap?",
                                  options=[f"cap {cap:g}", f"match {want:g}"],
                                  default=(f"match {want:g}" if pol.get("decisions", {})
                                           .get("defaults", {}).get("dummy_l_over_cap") == "match"
                                           else f"cap {cap:g}"),
                                  default_reason="policy decisions.defaults.dummy_l_over_cap"))
    else:
        dummy_l = float(dl)
    n_islands = sum(1 for w in wells if w["kind"] == "dnw")
    style = "two_row" if cell.nmos and cell.pmos else "single_row"
    return dict(style=style, order_n=order["n"], order_p=order["p"], dummy_l=dummy_l,
                dnw_islands=n_islands, decided_by="rule")


# ----------------------------------------------------------------------------- top level
def decide(cell, policy=None, previous: dict | None = None, mode: str | None = None) -> dict:
    """mode: 'auto' answers open questions with their policy default (answered_by: auto);
    'manual' leaves them open. Default: policy decisions.mode (auto)."""
    import copy
    pol = policy or load_policy()
    mode = mode or pol.get("decisions", {}).get("mode", "auto")
    if previous:   # auto answers from an earlier run are recomputed, never inherited
        previous = copy.deepcopy(previous)
        for q in previous.get("questions", []):      # hand-edited answer => designer's
            if q.get("answered_by") == "auto" and q.get("answer") != q.get("default"):
                q["answered_by"] = "designer"
        previous["questions"] = [q for q in previous.get("questions", [])
                                 if q.get("answered_by") != "auto"]
        for q in previous["questions"]:
            if q.get("answer"):
                q.setdefault("answered_by", "designer")
    dec = _decide(copy.deepcopy(cell), pol, previous)
    if mode == "auto":
        auto = [q for q in dec["questions"] if not q.get("answer") and q.get("default")]
        if auto:
            prev = copy.deepcopy(previous) if previous else {}
            designer = {q["id"]: q for q in prev.get("questions", [])
                        if q.get("answer") and q.get("answered_by") != "auto"}
            prev["questions"] = list(designer.values()) + [
                {**q, "answer": q["default"], "answered_by": "auto"} for q in auto
                if q["id"] not in designer]
            for k in ("groups", "wells", "floorplan"):
                prev.setdefault(k, dec[k] if k != "floorplan" else {})
            dec = _decide(copy.deepcopy(cell), pol, prev)     # re-decide with the answers
    dec["mode"] = mode
    return dec


def apply_answers(cell, dec: dict | None, pol=None) -> dict:
    """Apply the netlist changes that answered questions imply (e.g. body -> ground) to
    `cell`, logging each one. decide and build both call this, so the layout always
    matches the decision file. Returns {question id: answer}."""
    pol = pol or load_policy()
    qs = (dec or {}).get("questions", [])
    answers = {q["id"]: q["answer"] for q in qs if q.get("answer")}
    who = {q["id"]: q.get("answered_by", "designer") for q in qs}
    gnd_net = next((g for g in pol["rails"]["ground"] if any(f.b == g for f in cell.fets)),
                   pol["rails"]["ground"][0])
    for qid, ans in answers.items():
        if qid.startswith("Q-body-") and "ground" in str(ans):
            net = qid[len("Q-body-"):]
            for f in cell.fets:
                if f.b == net:
                    f.b = gnd_net
            cell.log.append(f"{who[qid]} decision {qid}: body {net} -> {gnd_net} "
                            f"(schematic must match before LVS against it)")
    return answers


def _decide(cell, pol, previous):
    questions = []
    answers = apply_answers(cell, previous, pol)
    nets = classify_nets(cell, pol)
    groups = find_groups(cell, nets, pol)
    wells = decide_wells(cell, pol, groups, questions)
    rings = decide_rings(wells, groups, nets, cell, pol)
    fp = decide_floorplan(cell, groups, wells, pol, questions)
    ans = answers.get("Q-dummy_l")
    if ans and str(ans).startswith("match"):
        fp["dummy_l"] = float(str(ans).split()[1]); fp["dummy_l_from"] = "Q-dummy_l"
        # (not decided_by: designer -- that would freeze the whole floorplan on re-runs)
    dec = dict(cell=cell.name, pins=cell.pins,
               nets={n: {"class": c, "why": r} for n, (c, r) in sorted(nets.items())},
               groups=groups, wells=wells, rings=rings, floorplan=fp, questions=questions,
               caps=[dict(name=c.name, top=c.top, bot=c.bot, w=c.w, l=c.l) for c in cell.caps],
               schematic_warnings=cell.warnings(), schematic_changes=list(cell.log))
    return merge(previous, dec) if previous else dec


def merge(old: dict, new: dict) -> dict:
    """Keep every item the designer edited (decided_by: designer) from the old file."""
    for sect in ("groups", "wells"):
        keep = {i["id"]: i for i in old.get(sect, []) if i.get("decided_by") == "designer"}
        new[sect] = [keep.get(i["id"], i) for i in new[sect]] + \
                    [i for k, i in keep.items() if k not in {x["id"] for x in new[sect]}]
    if old.get("floorplan", {}).get("decided_by") == "designer":
        new["floorplan"] = old["floorplan"]
    answered = {q["id"]: q for q in old.get("questions", []) if q.get("answer")}
    # (auto answers are passed in only by decide()'s own auto pass; a fresh run recomputes
    #  them from the policy, so editing the policy changes them)
    new["questions"] = [answered.get(q["id"], q) for q in new["questions"]]
    return new


def blockers(dec) -> list:
    """Decisions the current floorplanner (glayout_floorplan.two_row) cannot build yet."""
    out = []
    fp = dec["floorplan"]
    if fp["style"] != "two_row":
        out.append(f"floorplan style {fp['style']} (two_row needs NMOS and PMOS)")
    for w in dec["wells"]:
        # NMOS DNW islands for non-ground bodies (e.g. body tied to source): two_row builds
        # one island per body net, so they are no longer blockers.
        if w["kind"] == "nwell" and w["body"] != "VDD":
            out.append(f"{w['id']}: separate n-well island for body {w['body']}")
        if w["kind"] == "psub":
            out.append(f"{w['id']}: NMOS without DNW (two_row always draws one)")
    for g in dec["groups"]:
        # common_centroid: built as a 1-D mirror-symmetric unit sequence (expand_common_centroid)
        if g.get("dummy_ring") == "group":
            pass        # two_row puts one ring around each row: satisfied, but shared
    caps = dec.get("caps") or []
    if len(caps) > 2 or len({c.get("bot") for c in caps}) > 1:
        out.append(f"caps: two_row places <= 2 MIM caps sharing one bottom-plate net "
                   f"(got {[(c.get('name'), c.get('bot')) for c in caps]})")
    for r in dec["rings"]:
        if r.get("enabled"):
            out.append(f"extra guard ring around {r['around']}")
    for q in dec["questions"]:
        if not q.get("answer"):
            out.append(f"open question {q['id']}")
    return out


def centroid_pattern(counts: dict) -> list:
    """1-D common-centroid order of device names, one entry per unit.

    The row is mirror-symmetric (half + odd units + reversed half), so every device's units
    are centred on the middle of the row: a linear gradient along x cancels exactly. Inside
    the half, units are interleaved by largest deficit, so each device is spread along the row.
    1:2:4:8 (A..D) gives D C D B D C D A D C D B D C D. With more than one odd count the odd
    units share the middle, so their centroids differ by under one unit pitch.
    """
    half = {d: c // 2 for d, c in counts.items()}
    odd = [d for d, c in sorted(counts.items(), key=lambda x: x[1]) if c % 2]
    n = sum(half.values())
    placed = {d: 0 for d in half}
    seq = []
    for i in range(n):
        d = max(half, key=lambda d: (half[d] * (i + 1) / n - placed[d], half[d]))
        placed[d] += 1
        seq.append(d)
    if len(odd) > 1:                    # keep the middle symmetric as far as possible
        odd = odd[1::2][::-1] + odd[::2]
    return seq + odd + seq[::-1]


def expand_common_centroid(cell, dec, order_n, order_p):
    """Split every common_centroid group into unit devices (one finger each, same W/L and
    terminals) and put them in centroid_pattern order in the row. Changes `cell` in place
    (logged); returns the new device orders."""
    from glayout_netlist import Fet
    order = {"n": list(order_n), "p": list(order_p)}
    for g in dec["groups"]:
        if g.get("placement") != "common_centroid":
            continue
        devs = [cell.by_name(n) for n in g["devices"]]
        keys = {(f.kind, round(f.w, 4), round(f.l, 4), f.g, f.s, f.b) for f in devs}
        if len(keys) != 1:
            raise NotImplementedError(f"{g['id']}: common-centroid needs one unit device (same "
                                      f"type, W per finger, L, gate, source, body); got {sorted(keys)}")
        counts = {f.name: f.nf for f in devs}
        pat = centroid_pattern(counts)
        made = defaultdict(int)
        units = []
        for name in pat:
            f = cell.by_name(name)
            units.append(Fet(f"{name}_u{made[name]}", f.kind, f.w, f.l, f.d, f.g, f.s, f.b, nf=1, m=1))
            made[name] += 1
        idx = min(i for i, f in enumerate(cell.fets) if f.name in counts)
        cell.fets = [f for f in cell.fets if f.name not in counts]
        cell.fets[idx:idx] = units
        row = order[devs[0].kind]
        pos = min(row.index(n) for n in counts)
        row[:] = [n for n in row if n not in counts]
        row[pos:pos] = [u.name for u in units]
        letter = {n: chr(65 + i) for i, n in enumerate(sorted(counts, key=lambda n: counts[n]))}
        cell.log.append(f"{g['id']} common-centroid, {len(units)} units: {' '.join(letter[n] for n in pat)}"
                        f" ({', '.join(f'{letter[n]}={n} x{counts[n]}' for n in letter)})")
    return order["n"], order["p"]


def two_row_args(dec):
    b = blockers(dec)
    if b:
        raise NotImplementedError("two_row cannot build these decisions yet: " + "; ".join(b))
    fp = dec["floorplan"]
    return fp["order_n"], fp["order_p"], fp["dummy_l"]


def review(dec) -> str:
    L = [f"== {dec['cell']}: {sum(len(g['devices']) for g in dec['groups'])} grouped devices, "
         f"{len(dec['wells'])} wells, {len(dec['questions'])} open questions"]
    for g in dec["groups"]:
        L.append(f"  {g['id']} {g['type']:12s} {','.join(g['devices'])}"
                 f"  [{g.get('placement')}, dummies {g.get('dummy_ring')}]  {g['reason']}")
    for w in dec["wells"]:
        L.append(f"  {w['id']} {w['kind']:5s} body={w['body']:8s} {'REQUIRED' if w['required'] else 'policy  '}"
                 f" ~{w['cost_um2']} um2  {','.join(w['devices'])}  ({w['reason']})")
    opt = [r for r in dec["rings"] if not r["required"]]
    L.append(f"  rings: {sum(r['required'] for r in dec['rings'])} required"
             + (f", {len(opt)} optional suggestion(s): " + "; ".join(r["reason"] for r in opt) if opt else ""))
    fp = dec["floorplan"]
    L.append(f"  floorplan {fp['style']}: N {fp['order_n']}  P {fp['order_p']}  dummy_l {fp['dummy_l']:g}")
    for q in dec["questions"]:
        who = q.get("answered_by", "designer") if q.get("answer") else None
        L.append(f"  QUESTION {q['id']}: {q['question']}  options {q['options']}"
                 + (f"  -> {q['answer']} ({who}" + (f": {q.get('default_reason')}" if who == "auto" else "")
                    + ")" if q.get("answer") else f"  [open; default would be {q.get('default')}]"))
    for w in dec["schematic_warnings"]:
        L.append(f"  SCHEMATIC {w}")
    b = blockers(dec)
    L.append("  two_row can build this now" if not b else "  two_row blockers: " + "; ".join(b))
    return "\n".join(L)


if __name__ == "__main__":
    import argparse
    from glayout_netlist import from_schematic
    ap = argparse.ArgumentParser(description="layout decisions -> <cell>.layout.yaml")
    ap.add_argument("schematic")
    ap.add_argument("--connect", action="append", default=[], help="NET=TO (schematic fix)")
    ap.add_argument("--out")
    ap.add_argument("--policy", default=str(POLICY))
    ap.add_argument("--manual", action="store_true", help="leave questions open (stop)")
    ap.add_argument("--auto", action="store_true", help="answer questions with policy defaults")
    a = ap.parse_args()
    cell = from_schematic(a.schematic).legalize()
    for c in a.connect:
        cell.connect(*c.split("=", 1))
    out = Path(a.out) if a.out else HERE / f"{cell.name}.layout.yaml"
    prev = yaml.safe_load(out.read_text()) if out.exists() else None
    dec = decide(cell, load_policy(a.policy), prev,
                 mode="manual" if a.manual else "auto" if a.auto else None)
    out.write_text("# Layout decisions (decide.py). Edit an item and set decided_by: designer to\n"
                   "# keep it across re-runs; answer questions with `answer:`.\n"
                   + yaml.safe_dump(dec, sort_keys=False, width=110))
    print(review(dec))
    print(f"wrote {out}")
