"""Test of gLayout's floorplan-router branch (glayout.floorplan) on one SNN row:
DAC_signed_binary -> DPI -> neuron_glayout, from the flow-built cells (flow/<cell>/).

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python \
        analog/layout_tools/top/row_111/build_row.py [--seed 0] [--no-signoff]

Blocks: each cell's GDS without its own labels (a flat top would merge them), with one port
per pin from <cell>_pins.json (left-edge stubs, met2; VSS/VDD met1). Placement and routing:
glayout.floorplan.closed_loop_floorplan + route_floorplan (annealing with the router in the
loop). Then: top labels, LVS reference (the three cells' own references under one top
subckt), real KLayout DRC + LVS. Everything is written next to this script.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[1]
sys.path.insert(0, str(TOOLS))

import klayout.db as kdb                                           # noqa: E402
import gdsfactory as gf                                            # noqa: E402
from glayout import gf180 as pdk                                   # noqa: E402
from glayout.floorplan.block import Block, Variant, extract_pins   # noqa: E402
from glayout.floorplan.circuit import Circuit, Instance           # noqa: E402
from glayout.floorplan.route_flow import closed_loop_floorplan, route_floorplan   # noqa: E402
from glayout.floorplan.router import RouterTech                   # noqa: E402

import flow                                                        # noqa: E402
import glayout.floorplan.route_flow as _rf                          # noqa: E402

# route_floorplan builds a glayout Netlist from each block's component.info["netlist"]; imported
# GDS blocks have none, and this script writes its own LVS reference, so skip that step.
_rf.floorplan_netlist = lambda circuit, result, name: None

NAME = "row_111"
CELLS = {"DAC": "DAC_signed_binary", "DPI": "DPI", "NEU": "neuron_glayout"}
# instance -> {cell pin: top net}
NETS = {
    "DAC": {"Isum_e": "Isum", "Isum_i": "VDD", "en": "pulse", "s": "s", "Vb": "Vb",
            "w[0]": "w[0]", "w[1]": "w[1]", "w[2]": "w[2]", "w[3]": "w[3]", "VDD": "VDD", "VSS": "VSS"},
    "DPI": {"VDD": "VDD", "VSS": "VSS", "Vthr": "Vthr", "Isyn": "VMEM", "Isum": "Isum", "VT": "VT_dpi"},
    "NEU": {"VSS": "VSS", "VDD": "VDD", "VMEM": "VMEM", "VNA": "VNA", "Vlk": "Vlk", "VK": "VK",
            "VIp": "VIp", "VKup": "VKup", "VKdn": "VKdn", "Vamp_bias": "Vamp_bias", "VT": "VT",
            "spike": "spike"},
}
PORTS = ["VDD", "VSS", "w[3]", "w[2]", "w[1]", "w[0]", "pulse", "s", "Vb", "Vthr", "VT_dpi",
         "VNA", "Vlk", "VK", "VIp", "VKup", "VKdn", "Vamp_bias", "VT", "spike"]


def unlabelled_gds(cell: str) -> Path:
    """Copy of the cell's GDS without text (labels), so the flat top has only top labels."""
    src = flow.FLOW / cell / f"{cell}.gds"
    out = HERE / f"{cell}_nolabels.gds"
    ly = kdb.Layout(); ly.read(str(src))
    for c in ly.each_cell():
        for li in ly.layer_indexes():
            for s in list(c.shapes(li).each(kdb.Shapes.STexts)):
                c.shapes(li).erase(s)
    ly.write(str(out))
    return out


def make_block(inst: str, cell: str) -> Block:
    pins = json.loads((flow.FLOW / cell / f"{cell}_pins.json").read_text())
    comp = gf.import_gds(str(unlabelled_gds(cell)), cellname=cell)
    comp = comp.copy() if getattr(comp, "_locked", False) else comp
    if hasattr(comp, "unlock"):
        comp.unlock()
    net_ports = {}
    for p in pins["ports"]:
        name = f"{p['net']}_W"
        comp.add_port(name=name, center=(p["x"], p["y"]), width=p["width"],
                      orientation=p["orientation"], layer=pdk.get_glayer(p["layer"]))
        net_ports[p["net"]] = [name]
    v = Variant({}, float(comp.xsize), float(comp.ysize), extract_pins(comp, net_ports, pdk), comp)
    return Block(cell, inst, [v])


def lvs_ref(path: Path):
    """Top subckt over the three cells' own LVS references (pins matched by name)."""
    parts, lines = [], []
    for inst, cell in CELLS.items():
        txt = (flow.FLOW / cell / f"{cell}_lvs_ref.spice").read_text()
        parts.append(txt)
        hdr = next(l for l in txt.splitlines() if l.lower().startswith(".subckt"))
        cpins = hdr.split()[2:]
        # gf180_xschem_klayout_spice_convert strips one leading X (XDAC -> DAC = a diode)
        lines.append(f"XX{inst} " + " ".join(NETS[inst][p] for p in cpins) + f" {cell}")
    path.write_text("\n".join(parts) + f"\n.subckt {NAME} {' '.join(PORTS)}\n" + "\n".join(lines)
                    + "\n.ends\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-signoff", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    pdk.activate()
    blocks = {i: make_block(i, c) for i, c in CELLS.items()}
    circuit = Circuit(NAME, [Instance(i, blocks[i], NETS[i]) for i in CELLS], ports=PORTS)
    tech = RouterTech.from_pdk(pdk)
    loop = closed_loop_floorplan(pdk, circuit, list(blocks.values()), tech, seed=a.seed)
    comp, rr = route_floorplan(pdk, circuit, loop.floorplan, tech, name=NAME)
    # route_floorplan labels nets on met2 only; VSS / VDD reach the blocks on met1 straps
    have = {lab.text for lab in comp.labels}
    for net in PORTS:
        if net in have:
            continue
        for inst, m in NETS.items():
            cnet = next((c for c, t in m.items() if t == net), None)
            if cnet is None:
                continue
            p = loop.floorplan.placed[inst]
            v = blocks[inst].variants[p.variant]
            px, py = v.pin_xy(cnet, p.mirrored)
            comp.add_label(text=net, position=(p.x + px + (-0.3 if p.mirrored else 0.3), p.y + py),
                           layer=pdk.get_glayer(f"{v.pins[cnet].layer}_label"))
            break
    gds = HERE / f"{NAME}.gds"
    comp.write_gds(str(gds))
    lvs_ref(HERE / f"{NAME}_lvs_ref.spice")
    summary = dict(routed=rr.success, failed=list(rr.failed_nets) + list(rr.unreachable),
                   wirelength_um=round(rr.wirelength, 1), vias=rr.vias,
                   size_um=[round(comp.xsize, 2), round(comp.ysize, 2)],
                   placement={k: dict(x=round(v.x, 2), y=round(v.y, 2), mirrored=v.mirrored)
                              for k, v in loop.floorplan.placed.items()},
                   build_s=round(time.time() - t0))
    print(json.dumps(summary, indent=1))
    if a.no_signoff:
        return
    import re
    import shutil
    d = HERE
    shutil.rmtree(d / "drc", ignore_errors=True); shutil.rmtree(d / "lvs", ignore_errors=True)
    flow.login(f"python3 {flow.TECH}/drc/run_drc.py --path={gds} --variant=D --topcell={NAME} "
               f"--run_dir={d}/drc --mp=4 > {d}/drc.log 2>&1", d)
    log = (d / "drc.log").read_text()
    m = re.search(r"Violated rules are : (.*)", log)
    drc = "clean" if "is clean" in log else (m.group(1) if m else "failed to run")
    flow.login(f"python3 {flow.TECH}/lvs/gf180_xschem_klayout_spice_convert.py {NAME}_lvs_ref.spice "
               f"-o {NAME}_lvs_ref.cdl > /dev/null 2>&1; python3 {flow.TECH}/lvs/run_lvs.py "
               f"--layout={gds} --netlist={d}/{NAME}_lvs_ref.cdl --variant=D --topcell={NAME} "
               f"--run_dir={d}/lvs > {d}/lvs.log 2>&1", d)
    log = (d / "lvs.log").read_text()
    lvs = "match" if "Netlists match" in log else "mismatch" if "don't match" in log else "failed to run"
    summary.update(drc=drc, lvs=lvs, total_s=round(time.time() - t0))
    (d / f"{NAME}.json").write_text(json.dumps(summary, indent=1))
    print(f"DRC {drc}, LVS {lvs} ({summary['total_s']} s)")


if __name__ == "__main__":
    main()
