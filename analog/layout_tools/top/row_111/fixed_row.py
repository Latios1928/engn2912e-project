"""Fixed-placement test of glayout.floorplan's router on one SNN row (step 1 of the top level).

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python \
        analog/layout_tools/top/row_111/fixed_row.py [--gaps 8,6,4,3,2] [--margin 6]

Row (our zoning, not the annealer's):  [DAC mirrored] gap [DPI] gap [neuron], bottoms aligned,
`margin` um of free routing space around the row. For every channel width (gap) in --gaps:
route, then measure (1) whether the given placement is used as is, (2) routability, (3) where
the sensitive nets Isum / VMEM go (wire vs. shortest possible, wire outside the row's channels,
parallel run next to switching nets), (5) area. The narrowest gap that routes is drawn and
signed off (4: real DRC + LVS). Writes fixed_row.json and row_111_fixed.gds next to this file.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_row as B                                              # noqa: E402  (blocks, circuit nets, LVS ref)

from glayout.floorplan.anneal import FloorplanResult, FloorplanWeights, Placed   # noqa: E402
from glayout.floorplan.circuit import Circuit, Instance           # noqa: E402
from glayout.floorplan.route_flow import route_floorplan          # noqa: E402
from glayout.floorplan.router import RouterTech, detours          # noqa: E402

NAME = "row_111_fixed"
ORDER = [("DAC", True), ("DPI", False), ("NEU", False)]           # left -> right, mirrored?
SENSITIVE = ["Isum", "VMEM"]
AGGRESSORS = ["pulse", "s", "w[0]", "w[1]", "w[2]", "w[3]", "spike"]
NEAR_UM = 2.0                                                      # "running next to" distance


def placement(blocks, gap, margin):
    placed, x = {}, margin
    for inst, mir in ORDER:
        v = blocks[inst].variants[0]
        placed[inst] = Placed(inst, x, margin, v.width, v.height, 0, mir)
        x += v.width + gap
    width = x - gap + margin
    height = max(blocks[i].variants[0].height for i, _ in ORDER) + 2 * margin
    return placed, width, height


def segments(rr):
    """net -> [(layer z, x0, y0, x1, y1)] of the routed wires (grid paths)."""
    g, out = rr.grid, {}
    for net, plist in rr.paths.items():
        for path in plist:
            for a, b in zip(path, path[1:]):
                if g.layer(a) == g.layer(b):
                    (ax, ay), (bx, by) = g.xy(a), g.xy(b)
                    out.setdefault(net, []).append((g.layer(a), ax, ay, bx, by))
    return out


def parallel_run(sa, sb, near):
    """Length over which segments of a and b on the same layer run side by side within `near`."""
    tot = 0.0
    for za, ax0, ay0, ax1, ay1 in sa:
        for zb, bx0, by0, bx1, by1 in sb:
            if za != zb:
                continue
            if ay0 == ay1 and by0 == by1 and abs(ay0 - by0) <= near:          # both horizontal
                tot += max(0.0, min(max(ax0, ax1), max(bx0, bx1)) - max(min(ax0, ax1), min(bx0, bx1)))
            elif ax0 == ax1 and bx0 == bx1 and abs(ax0 - bx0) <= near:        # both vertical
                tot += max(0.0, min(max(ay0, ay1), max(by0, by1)) - max(min(ay0, ay1), min(by0, by1)))
    return tot


def measure(rr, placed, blocks, row_y0, row_y1):
    seg = segments(rr)
    det = detours(rr)
    out = {}
    for net in SENSITIVE + ["VDD", "VSS"]:
        s = seg.get(net, [])
        wire = sum(abs(x1 - x0) + abs(y1 - y0) for _z, x0, y0, x1, y1 in s)
        outside = sum(abs(x1 - x0) + abs(y1 - y0) for _z, x0, y0, x1, y1 in s
                      if max(y0, y1) > row_y1 or min(y0, y1) < row_y0)
        lands = rr.landings.get(net, [])
        hp = (max(l.x for l in lands) - min(l.x for l in lands) + max(l.y for l in lands)
              - min(l.y for l in lands)) if len(lands) > 1 else 0.0
        out[net] = dict(wire_um=round(wire, 1), shortest_um=round(hp, 1),
                        detour_ratio=round(det.get(net, wire / hp if hp else 1.0), 2),
                        outside_row_um=round(outside, 1),
                        next_to_switching_um=round(sum(parallel_run(s, seg.get(a, []), NEAR_UM)
                                                       for a in AGGRESSORS), 1) if net in SENSITIVE else None)
    return out


def signoff(gds: Path, ref_spice: Path):
    import flow
    d = HERE / "fixed_signoff"
    shutil.rmtree(d, ignore_errors=True); d.mkdir()
    flow.login(f"python3 {flow.TECH}/drc/run_drc.py --path={gds} --variant=D --topcell={NAME} "
               f"--run_dir={d}/drc --mp=4 > {d}/drc.log 2>&1", d)
    log = (d / "drc.log").read_text()
    m = re.search(r"Violated rules are : (.*)", log)
    drc = "clean" if "is clean" in log else (m.group(1) if m else "failed to run")
    flow.login(f"python3 {flow.TECH}/lvs/gf180_xschem_klayout_spice_convert.py {ref_spice} "
               f"-o {d}/{NAME}_lvs_ref.cdl > /dev/null 2>&1; python3 {flow.TECH}/lvs/run_lvs.py "
               f"--layout={gds} --netlist={d}/{NAME}_lvs_ref.cdl --variant=D --topcell={NAME} "
               f"--run_dir={d}/lvs > {d}/lvs.log 2>&1", d)
    log = (d / "lvs.log").read_text()
    lvs = "match" if "Netlists match" in log else "mismatch" if "don't match" in log else "failed to run"
    return drc, lvs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gaps", default="8,6,4,3,2")
    ap.add_argument("--margin", type=float, default=6.0)
    ap.add_argument("--no-signoff", action="store_true")
    ap.add_argument("--mirror-dpi", action="store_true", help="DPI pins face the neuron instead of the DAC")
    ap.add_argument("--tag", default="")
    ap.add_argument("--as-drawn", action="store_true", help="no mirroring (blocks with pin_sides facing their neighbours)")
    a = ap.parse_args()
    global ORDER
    if a.mirror_dpi:
        ORDER = [("DAC", True), ("DPI", True), ("NEU", False)]
    if a.as_drawn:
        ORDER = [("DAC", False), ("DPI", False), ("NEU", False)]
    t0 = time.time()
    B.pdk.activate()
    blocks = {i: B.make_block(i, c) for i, c in B.CELLS.items()}
    circuit = Circuit(NAME, [Instance(i, blocks[i], B.NETS[i]) for i in B.CELLS], ports=B.PORTS)
    tech = RouterTech.from_pdk(B.pdk)
    runs, best = [], None
    for gap in [float(g) for g in a.gaps.split(",")]:
        placed, W, H = placement(blocks, gap, a.margin)
        fp = FloorplanResult(circuit, placed, dict(width=W, height=H), FloorplanWeights())
        comp, rr = route_floorplan(B.pdk, circuit, fp, tech, name=NAME)
        # (1) placement used as given: every block where we put it (realise checks bbox == cell)
        refs_ok = all(abs(placed[i].x - (fp.placed[i].x)) < 1e-9 for i in placed)
        row = dict(gap_um=gap, routed=rr.success, failed=list(rr.failed_nets) + list(rr.unreachable),
                   size_um=[round(W, 1), round(H, 1)], area_um2=round(W * H),
                   wirelength_um=round(rr.wirelength, 1), vias=rr.vias, placement_kept=refs_ok,
                   nets=measure(rr, placed, blocks, a.margin, H - a.margin) if rr.success else None)
        runs.append(row)
        print(f"gap {gap:g} um: routed={rr.success} size {W:.1f} x {H:.1f} um wire {rr.wirelength:.0f} um "
              f"vias {rr.vias} {row['failed'] or ''}", flush=True)
        if rr.success:
            best = (gap, comp, rr, fp)
    out = dict(order=ORDER, margin_um=a.margin, runs=runs)
    if best and not a.no_signoff:
        gap, comp, rr, fp = best
        have = {lab.text for lab in comp.labels}
        for net in B.PORTS:                       # VSS / VDD: met1 labels (route_floorplan: met2 only)
            if net in have:
                continue
            for inst, m in B.NETS.items():
                cnet = next((c for c, t in m.items() if t == net), None)
                if cnet is None:
                    continue
                p = fp.placed[inst]; v = blocks[inst].variants[0]
                px, py = v.pin_xy(cnet, p.mirrored)
                comp.add_label(text=net, position=(p.x + px + (-0.3 if p.mirrored else 0.3), p.y + py),
                               layer=B.pdk.get_glayer(f"{v.pins[cnet].layer}_label"))
                break
        gds = HERE / f"{NAME}.gds"
        comp.write_gds(str(gds))
        B.NAME = NAME
        ref = HERE / f"{NAME}_lvs_ref.spice"
        B.lvs_ref(ref)
        drc, lvs = signoff(gds, ref)
        out["signed_off"] = dict(gap_um=gap, drc=drc, lvs=lvs)
        print(f"signoff at gap {gap:g} um: DRC {drc}, LVS {lvs}")
    out["total_s"] = round(time.time() - t0)
    (HERE / f"fixed_row{a.tag}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
