#!/usr/bin/env python3
"""Full-chip LVS of the submitted GDS, and the checks that it holds the current design.

    python3 librelane/snn_top/chip_lvs.py      # from anywhere in the repo, in the container
    python3 librelane/snn_top/chip_lvs.py --layout path/to/candidate.gds   # check another GDS
                                               # (e.g. a run's final/gds before it is published)

Run it after ANY design change, once the change has gone through the whole chain:
    analog cell -> flow.py -> top.py (SNN_signed, signoff) -> top_pex.sh
    -> librelane/macros/snn_analog/make_macro.py -> librelane/snn_top/run.sh (publishes results/,
       gds/snn_top.gds, verilog/gl/snn_top.v)
It exits 1 if any check fails, and names the step of the chain to rerun.

Why: LibreLane's own LVS black-boxes the analog macro (netgen -blackbox, and Magic extracts
snn_analog as an abstract stub), so a LibreLane "LVS clean" checks only the wires to the
macro's pins. This script extracts the whole chip GDS down to transistors with Magic and
compares it with netgen against the gate-level netlist plus the macro's LVS reference. It reads
those paths from lvs_config.json, so it checks exactly the files the submission names.

Checks (in this order; all run, the summary lists each):
  1. macro signoff    analog/layout_tools/top/SNN_signed/signoff.json: ok, DRC clean, LVS match
  2. macro reference  snn_analog_lvs_ref.spice contains SNN_signed_lvs_ref.spice unchanged
                      (else make_macro.py was not rerun after the last top.py)
  3. macro layout     the SNN_signed geometry in snn_analog.gds equals SNN_signed.gds (XOR, every
                      layer), and snn_analog.gds has the ISOSUB marker (23/5)
  4. chip macro       the snn_analog cell in the chip GDS equals snn_analog.gds (XOR, every layer)
                      (else run.sh was not rerun after make_macro.py)
  5. published files  LAYOUT_FILE == results/snn_top.gds, LVS_VERILOG_FILES == results/snn_top.pnl.v
                      (else the run's outputs were not copied; run.sh skips its copy step when
                      LibreLane exits non-zero, e.g. on the fill errors before fill is added)
  6. extraction       Magic extraction of LAYOUT_FILE; VDDA, VSSA, VDDD and VSSD are four separate
                      ports of snn_top (VSSA joined to VSSD means the ISOSUB marker is missing or wrong)
  7. LVS              netgen: "Circuits match uniquely" at the top; the macro's port errors only
                      on the known isolated Isum / Isum_i p-wells (Magic exports those well nodes as
                      macro ports; at the top they connect to nothing)

Work files: librelane/snn_top/chip_lvs/ (gitignored): extraction, snn_top_ext.spice, lvs.rpt,
lvs.log, summary.txt. Takes about 2 minutes.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import klayout.db as db

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = HERE / "chip_lvs"
PDK_ROOT, PDK = "/foss/pdks", "gf180mcuD"
TOP = "snn_top"
MACRO = "snn_analog"
INNER = "SNN_signed"
SIGNOFF_DIR = ROOT / "analog/layout_tools/top/SNN_signed"
MACRO_DIR = ROOT / "librelane/macros/snn_analog"
RESULTS = HERE / "results"
ISOSUB = (23, 5)
SUPPLIES = ("VDDA", "VSSA", "VDDD", "VSSD")
# Isolated p-well nodes of the DPI / DAC cells that Magic exports as ports of the macro
ALLOWED_PORT_ERROR = re.compile(r"/(Isum|Isum_i)$")

results = []   # (name, ok, detail)


def rel(p):
    p = Path(p)
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def check(name, ok, detail, fix=""):
    results.append((name, ok, detail if ok or not fix else f"{detail} -> {fix}"))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {results[-1][2]}", flush=True)
    return ok


def lvs_config():
    """LAYOUT_FILE, LVS_VERILOG_FILES, LVS_SPICE_FILES and the std-cell SPICE, from lvs_config.json."""
    cfg = json.loads((ROOT / "lvs_config.json").read_text())
    var = {"UPRJ_ROOT": str(ROOT), "PDK": PDK, "PDK_ROOT": PDK_ROOT, "TOP_SOURCE": cfg["TOP_SOURCE"]}
    var["TOP_LAYOUT"] = cfg["TOP_LAYOUT"].replace("$TOP_SOURCE", cfg["TOP_SOURCE"])

    def expand(s):
        return re.sub(r"\$(\w+)", lambda m: var[m.group(1)], s)
    lib = cfg["STD_CELL_LIBRARY"]
    return dict(
        top=cfg["TOP_SOURCE"],
        layout=Path(expand(cfg["LAYOUT_FILE"])),
        verilog=[Path(expand(v)) for v in cfg["LVS_VERILOG_FILES"] if v],
        spice=[Path(expand(s)) for s in cfg["LVS_SPICE_FILES"] if s],
        stdcells=Path(PDK_ROOT) / PDK / "libs.ref" / lib / "spice" / f"{lib}.spice",
    )


def flat_regions(layout, cell, scale=1.0):
    """{(layer, datatype): merged flat Region} of a cell, polygons only, in 1 nm units."""
    out = {}
    trans = db.ICplxTrans(scale)
    for li in layout.layer_indexes():
        info = layout.get_info(li)
        r = db.Region(cell.begin_shapes_rec(li))
        if r.is_empty():
            continue
        out[(info.layer, info.datatype)] = r.transformed(trans).merged()
    return out


def xor_layers(a, b, ignore=()):
    """Layers whose geometry differs between two {layer: Region} maps, with the XOR area."""
    diffs = []
    for key in sorted(set(a) | set(b)):
        if key in ignore:
            continue
        ra, rb = a.get(key, db.Region()), b.get(key, db.Region())
        x = ra ^ rb
        if not x.is_empty():
            diffs.append(f"{key[0]}/{key[1]} ({x.area() * 1e-6:.3f} um2)")
    return diffs


def read_gds(path):
    layout = db.Layout()
    layout.read(str(path))
    return layout


def login_shell(cmd, log):
    """Magic / netgen need the container's login environment (PATH, PDK); a plain shell has no
    magic on PATH, and an inherited FOSS_INIT_DONE makes the profile skip its setup."""
    with open(log, "w") as f:
        return subprocess.run(["env", "-u", "PYTHONPATH", "-u", "FOSS_INIT_DONE", "bash", "-lc", cmd],
                              stdout=f, stderr=subprocess.STDOUT, cwd=WORK).returncode


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--layout", type=Path, help="GDS to check instead of lvs_config.json's LAYOUT_FILE")
    args = ap.parse_args()
    WORK.mkdir(exist_ok=True)
    cfg = lvs_config()
    if args.layout:
        cfg["layout"] = args.layout.resolve()
    print(f"chip_lvs: {rel(cfg['layout'])} against "
          + " + ".join(rel(p) for p in cfg["verilog"] + cfg["spice"]), flush=True)
    for p in [cfg["layout"], *cfg["verilog"], *cfg["spice"], cfg["stdcells"]]:
        if not p.exists():
            check("inputs", False, f"missing {p}", "check lvs_config.json / rerun run.sh")
            return finish()

    # 1. macro signoff
    so = json.loads((SIGNOFF_DIR / "signoff.json").read_text())
    check("macro signoff", so.get("ok") and so.get("drc") == "clean" and so.get("lvs") == "match",
          f"{INNER} signoff {so.get('time')}: drc {so.get('drc')}, lvs {so.get('lvs')}",
          "rerun top.py (signoff stage)")

    # 2. macro reference
    src_ref = (SIGNOFF_DIR / f"{INNER}_lvs_ref.spice").read_text().rstrip()
    mac_ref = (MACRO_DIR / f"{MACRO}_lvs_ref.spice").read_text()
    check("macro reference", src_ref in mac_ref,
          f"{MACRO}_lvs_ref.spice {'contains' if src_ref in mac_ref else 'differs from'} "
          f"{INNER}_lvs_ref.spice", "rerun make_macro.py")

    # 3. macro layout: SNN_signed.gds (5 nm) == the SNN_signed cell of snn_analog.gds (1 nm)
    src = read_gds(SIGNOFF_DIR / f"{INNER}.gds")
    mac = read_gds(MACRO_DIR / f"{MACRO}.gds")
    a = flat_regions(src, src.cell(INNER), src.dbu / 0.001)
    b = flat_regions(mac, mac.cell(INNER), mac.dbu / 0.001)
    diffs = xor_layers(a, b)
    check("macro layout", not diffs,
          f"{INNER} in {MACRO}.gds {'equals' if not diffs else 'differs from'} {INNER}.gds"
          + (": " + ", ".join(diffs[:6]) if diffs else ""), "rerun make_macro.py")
    mac_regions = flat_regions(mac, mac.cell(MACRO), mac.dbu / 0.001)
    iso = mac_regions.get(ISOSUB, db.Region())
    check("ISOSUB marker", not iso.is_empty(),
          f"{iso.count()} polygon(s), {iso.area() * 1e-6:.0f} um2 on 23/5 in {MACRO}.gds",
          "make_macro.py must draw it (rerun it)")

    # 4. chip macro: the snn_analog cell of the chip GDS == snn_analog.gds
    chip = read_gds(cfg["layout"])
    cc = chip.cell(MACRO)
    if cc is None:
        check("chip macro", False, f"no {MACRO} cell in {cfg['layout'].name}", "rerun run.sh")
    else:
        # PR boundary (63/0) is LibreLane bookkeeping, not geometry
        diffs = xor_layers(flat_regions(chip, cc, chip.dbu / 0.001), mac_regions, ignore={(63, 0)})
        check("chip macro", not diffs,
              f"{MACRO} in {cfg['layout'].name} {'equals' if not diffs else 'differs from'} {MACRO}.gds"
              + (": " + ", ".join(diffs[:6]) if diffs else ""), "rerun run.sh")

    # 5. published files == the run's outputs in results/
    # (with --layout the candidate GDS is not published yet, so only the netlist is compared)
    pairs = [] if args.layout else [(cfg["layout"], RESULTS / f"{TOP}.gds")]
    for pub, res in pairs + [(cfg["verilog"][0], RESULTS / f"{TOP}.pnl.v")]:
        same = res.exists() and pub.read_bytes() == res.read_bytes()
        check("published files", same, f"{rel(pub)} {'==' if same else '!='} {rel(res)}",
              "copy the run's final/gds and final/pnl (run.sh does it when LibreLane exits 0)")

    # 6. extraction
    ext = WORK / f"{TOP}_ext.spice"
    ext.unlink(missing_ok=True)
    (WORK / "extract.tcl").write_text(
        "drc off\ncrashbackups disable\nlocking disable\n"
        f"cd {WORK}\ngds read {cfg['layout']}\nload {TOP}\nextract all\n"
        f"ext2spice lvs\next2spice -o {ext}\nquit -noprompt\n")
    rc = login_shell(f"magic -dnull -noconsole -rcfile {PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc "
                     f"{WORK}/extract.tcl", WORK / "extract.log")
    if rc != 0 or not ext.exists():
        check("extraction", False, f"Magic failed (exit {rc}), see {WORK / 'extract.log'}")
        return finish()
    text = ext.read_text()
    m = re.search(rf"^\.subckt {TOP} (.*?)\n(?!\+)", text, re.M | re.S)
    ports = m.group(1).replace("\n+", " ").split() if m else []
    missing = [s for s in SUPPLIES if s not in ports]
    joined = text.replace("\n+", " ")
    devices = len(re.findall(r"\b[np]fet_(?:03v3|05v0)\b", joined))
    cells = len(re.findall(r"^\.subckt ", joined, re.M))
    check("extraction", not missing,
          f"hierarchical netlist, {cells} subcircuits, {devices} transistor lines (each cell type once); "
          "supplies " + ("all four separate" if not missing else
                                                  f"missing as ports: {', '.join(missing)}"),
          "VSSA merged into VSSD: check the ISOSUB marker (make_macro.py)")

    # 7. LVS
    rpt = WORK / "lvs.rpt"
    rpt.unlink(missing_ok=True)
    lines = [f"set c1 [readnet spice {ext}]", f"set c2 [readnet spice {cfg['stdcells']}]"]
    lines += [f"readnet spice {s} $c2" for s in cfg["spice"]]
    lines += [f"readnet verilog {v} $c2" for v in cfg["verilog"]]
    lines += [f'lvs "$c1 {TOP}" "$c2 {TOP}" {PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl {rpt} -json']
    (WORK / "lvs.tcl").write_text("\n".join(lines) + "\n")
    rc = login_shell(f"netgen -batch source {WORK}/lvs.tcl", WORK / "lvs.log")
    if not rpt.exists():
        check("LVS", False, f"netgen failed (exit {rc}), see {WORK / 'lvs.log'}")
        return finish()
    r = rpt.read_text()
    final = re.findall(r"Final result: (.*)", r)
    top_ok = bool(final) and final[-1].strip().startswith("Circuits match uniquely")
    bad_ports = [n for n in re.findall(r"^(\S+)\s+\|\(no pin, node is", r, re.M) if not ALLOWED_PORT_ERROR.search(n)]
    known = len(re.findall(r"^\S+\s+\|\(no pin, node is", r, re.M)) - len(bad_ports)
    # The macro's flattened device counts, layout side, from its subcircuit summary
    blk = re.search(rf"Subcircuit summary:\nCircuit 1: {MACRO}\s+\|Circuit 2: {MACRO}\s*\n[-|]+\n(.*?)\nNumber of devices",
                    r, re.S)
    counts = ", ".join(f"{n} {d}" for d, n in re.findall(r"^(\S+) \((\d+)", blk.group(1), re.M)) if blk else "?"
    check("LVS", top_ok and not bad_ports,
          f"top: {final[-1].strip() if final else 'no final result'}; macro compared at transistor level "
          f"({counts}); macro port errors: {known} known "
          f"(isolated Isum wells)" + (f", {len(bad_ports)} unexpected: {', '.join(bad_ports[:5])}" if bad_ports else ""),
          f"see {rpt}")
    return finish()


def finish():
    ok = all(r[1] for r in results)
    summary = "\n".join(f"{'PASS' if r[1] else 'FAIL'}  {r[0]}: {r[2]}" for r in results)
    (WORK / "summary.txt").write_text(summary + "\n")
    print(f"chip_lvs: {'PASS' if ok else 'FAIL'} ({sum(r[1] for r in results)} / {len(results)} checks), "
          f"details in {rel(WORK)}/", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
