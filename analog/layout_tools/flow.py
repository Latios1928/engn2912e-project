"""
Layout flow as file-based stages: every input and output is a file under flow/<cell>/, every
stage prints a short status and writes <stage>.json. Nothing depends on a conversation, so an
API call (or a new session, or a script) can run, inspect or resume any cell from scratch.

    F="env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/layout_tools/flow.py"
    $F status  neuron_glayout          # what exists, what passed, what blocks the next stage
    $F table   neuron_glayout          # schematic -> table.json  (devices, pins, warnings)
    $F decide  neuron_glayout          # -> layout.yaml (edit / answer questions there)
    $F build   neuron_glayout          # -> GDS, LVS ref, predictions (build.json)
    $F signoff neuron_glayout          # real DRC + LVS + Magic PEX + predictor feedback
    $F sim     neuron_glayout          # testbench: predicted-parasitic sim vs PEX sim
    $F run     neuron_glayout          # table..signoff; decisions auto by default
    $F run     neuron_glayout --manual # stop at every open decide question instead
    $F answer  neuron_glayout Q-dummy_l "cap 2"    # answer a decide.py question

Stages and their files (flow/<cell>/):
    table    table.json                       from the schematic (glayout_netlist)
    decide   layout.yaml                      decide.py; designer edits survive re-runs
    build    <cell>.gds _lvs_ref.spice _pred.spice .shapes.json build.json
    signoff  drc/ lvs/ <cell>_pex.spice signoff.json, updates parasitic_calib.json
    sim      sim/ sim.json
A stage refuses to run if the previous one has not passed, and says why.
Cells are registered in flow_cells.yaml (schematic, schematic fixes, symbol, testbench).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
FLOW = HERE / "flow"
REG = HERE / "flow_cells.yaml"
PEX_DIR = HERE.parent / "neuron" / "layout" / "PEX"    # shared Magic extraction scripts
ENV = {"PDK_ROOT": os.environ.get("PDK_ROOT", "/foss/pdks"), "PDK": os.environ.get("PDK", "gf180mcuD")}
TECH = f"{ENV['PDK_ROOT']}/{ENV['PDK']}/libs.tech/klayout/tech"


# ----------------------------------------------------------------------------- helpers
def registry() -> dict:
    import yaml
    return yaml.safe_load(REG.read_text())


def conf(cell: str) -> dict:
    reg = registry()
    if cell not in reg:
        raise SystemExit(f"error: {cell} not in {REG.name} (cells: {', '.join(reg)})")
    c = dict(reg[cell])
    for k in ("schematic", "symbol", "testbench"):
        if c.get(k):
            c[k] = str((HERE / c[k]).resolve())
    return c


def cdir(cell: str) -> Path:
    d = FLOW / cell
    d.mkdir(parents=True, exist_ok=True)
    return d


def save(cell: str, stage: str, data: dict) -> dict:
    data = {"stage": stage, "cell": cell, "time": time.strftime("%Y-%m-%d %H:%M:%S"), **data}
    (cdir(cell) / f"{stage}.json").write_text(json.dumps(data, indent=1, default=str))
    return data


def load(cell: str, stage: str) -> dict | None:
    f = FLOW / cell / f"{stage}.json"
    return json.loads(f.read_text()) if f.exists() else None


def login(cmd: str, cwd: Path, timeout: int = 1800) -> subprocess.CompletedProcess:
    """Run in a login shell (the PDK tools expect the container's login environment)."""
    return subprocess.run(["bash", "-lc", cmd], cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, env={**os.environ, **ENV})


def _cell(cell: str):
    from glayout_netlist import from_schematic
    c = conf(cell)
    nl = from_schematic(c["schematic"]).legalize()
    for net, to in (c.get("connect") or {}).items():
        nl.connect(net, to)
    nl.name = cell
    return nl


def need(cell: str, stage: str, ok_key: str = "ok"):
    d = load(cell, stage)
    if not d or not d.get(ok_key):
        raise SystemExit(f"blocked: stage '{stage}' has not passed for {cell} "
                         f"(run: flow.py {stage} {cell}; status: flow.py status {cell})")
    return d


# ----------------------------------------------------------------------------- stages
def st_table(cell):
    nl = _cell(cell)
    data = dict(ok=True, pins=nl.pins,
                fets=[f.__dict__ for f in nl.fets], caps=[c.__dict__ for c in nl.caps],
                warnings=nl.warnings(), changes=nl.log)
    save(cell, "table", data)
    return (f"table {cell}: {len(nl.nmos)} NMOS, {len(nl.pmos)} PMOS, {len(nl.caps)} caps, "
            f"{len(nl.pins)} pins; {len(data['warnings'])} warnings, {len(nl.log)} changes"
            + "".join(f"\n  WARNING {w}" for w in data["warnings"]))


def decision_mode(cell, override: str | None = None) -> str:
    """CLI flag > flow_cells.yaml `decisions:` > layout_policy.yaml decisions.mode > auto."""
    if override:
        return override
    c = conf(cell)
    if c.get("decisions"):
        return c["decisions"]
    from decide import load_policy
    return load_policy().get("decisions", {}).get("mode", "auto")


def st_decide(cell, mode: str | None = None):
    import yaml
    from decide import decide, review, blockers
    need(cell, "table")
    out = cdir(cell) / "layout.yaml"
    prev = yaml.safe_load(out.read_text()) if out.exists() else None
    mode = decision_mode(cell, mode)
    dec = decide(_cell(cell), previous=prev, mode=mode)
    out.write_text("# Layout decisions (decide.py). Edit an item and set decided_by: designer to\n"
                   "# keep it across re-runs; answer questions with `answer:`.\n"
                   + yaml.safe_dump(dec, sort_keys=False, width=110))
    b = blockers(dec)
    save(cell, "decide", dict(ok=not b, blockers=b, mode=mode,
                              open_questions=[q["id"] for q in dec["questions"] if not q.get("answer")],
                              auto_answers={q["id"]: q["answer"] for q in dec["questions"]
                                            if q.get("answered_by") == "auto"}))
    return review(dec)


def st_build(cell):
    import yaml
    from decide import two_row_args, apply_answers
    from glayout_floorplan import two_row, write_cell
    need(cell, "decide")
    dec = yaml.safe_load((cdir(cell) / "layout.yaml").read_text())
    order_n, order_p, dummy_l = two_row_args(dec)
    nl = _cell(cell)
    apply_answers(nl, dec)              # same netlist changes the decisions assumed
    res = two_row(nl, cell, order_n, order_p, dummy_l)
    text = write_cell(res, cdir(cell))
    b = json.loads((cdir(cell) / f"{cell}.build.json").read_text())
    ok = b["router_check"] == "clean" and " 0 rule(s) predicted to fail" in b["predrc"]
    save(cell, "build", dict(ok=ok, size_um=b["size_um"], router_check=b["router_check"],
                             predrc=b["predrc"].splitlines()[0], notes=b["notes"]))
    return text


def st_signoff(cell, pex: bool = True):
    from glayout_parasitics import calibrate, calibration_report, load_shapes
    need(cell, "build")
    d = cdir(cell)
    gds = d / f"{cell}.gds"
    out = {}
    # DRC
    shutil.rmtree(d / "drc", ignore_errors=True)
    login(f"python3 {TECH}/drc/run_drc.py --path={gds} --variant=D --topcell={cell} "
          f"--run_dir={d}/drc --mp=4 > {d}/drc.log 2>&1", d)
    log = (d / "drc.log").read_text()
    m = re.search(r"Violated rules are : (.*)", log)
    out["drc"] = "clean" if "is clean" in log else (m.group(1) if m else "failed to run")
    # LVS
    shutil.rmtree(d / "lvs", ignore_errors=True)
    login(f"python3 {TECH}/lvs/gf180_xschem_klayout_spice_convert.py {cell}_lvs_ref.spice "
          f"-o {cell}_lvs_ref.cdl > /dev/null 2>&1; "
          f"python3 {TECH}/lvs/run_lvs.py --layout={gds} --netlist={d}/{cell}_lvs_ref.cdl "
          f"--variant=D --topcell={cell} --run_dir={d}/lvs > {d}/lvs.log 2>&1", d)
    log = (d / "lvs.log").read_text()
    out["lvs"] = ("match" if "Netlists match" in log else
                  "mismatch" if "don't match" in log else "failed to run")
    # PEX + extraction -> predictor feedback
    if pex:
        r = login(f"bash {PEX_DIR}/RC_extract.sh {gds} {cell} > {d}/pex.log 2>&1", d)
        pspice = d / f"{cell}_pex.spice"
        if pspice.exists():
            txt = pspice.read_text()
            out["pex"] = dict(devices=len(re.findall(r"^X", txt, re.M)),
                              C=len(re.findall(r"^C", txt, re.M)), R=len(re.findall(r"^R", txt, re.M)))
            cal = calibrate(load_shapes(d / f"{cell}.shapes.json"), pspice, cell, gds=gds)
            out["calibration"] = {k: v for k, v in cal.items() if k != "rows"}
            out["calibration_text"] = calibration_report(cal)
        else:
            out["pex"] = "failed (see pex.log)"
    ok = out["drc"] == "clean" and out["lvs"] == "match" and (not pex or isinstance(out.get("pex"), dict))
    save(cell, "signoff", dict(ok=ok, **out))
    lines = [f"signoff {cell}: DRC {out['drc']}, LVS {out['lvs']}"]
    if pex:
        lines.append(f"  PEX {out['pex']}")
        if "calibration_text" in out:
            lines.append("  " + out["calibration_text"].replace("\n", "\n  "))
    return "\n".join(lines)


def st_sim(cell):
    """Predicted-parasitic pre-layout sim vs real PEX sim, typical corner."""
    from glayout_corners import for_sim, testbench_deck, pex_wrapper, run, period
    from glayout_netlist import netlist_schematic
    c = conf(cell)
    if not c.get("testbench") or not c.get("symbol"):
        raise SystemExit(f"blocked: {cell} needs 'testbench' and 'symbol' in {REG.name}")
    need(cell, "signoff")
    d = cdir(cell); s = d / "sim"; s.mkdir(exist_ok=True)
    tb = s / "tb.spice"
    tb.write_text(netlist_schematic(c["testbench"]))
    for_sim(d / f"{cell}_pred.spice", s / "pred.spice")
    pex_wrapper(d / f"{cell}_pex.spice", c["symbol"], s / "pex_wrap.spice", f"{cell}_pex")
    decks = [testbench_deck(tb, cell, s / "pred.spice", s / "pred_tb.spice"),
             testbench_deck(tb, f"{cell}_pex", s / "pex_wrap.spice", s / "pex_tb.spice")]
    res = run(decks, jobs=2)
    m = c.get("metric", {})
    vals = {}
    for deck, ok, sec in res:
        vals[deck.stem] = dict(ok=ok, seconds=round(sec),
                               value=period(deck.with_suffix(".raw"), m.get("node", "v(spike)"),
                                            m.get("threshold", 1.65)) if ok else None)
    p, x = vals["pred_tb"]["value"], vals["pex_tb"]["value"]
    err = (p - x) / x if p and x else None
    save(cell, "sim", dict(ok=err is not None, metric=m, predicted=p, pex=x, error=err, runs=vals))
    return (f"sim {cell}: predicted {p * 1e6:.1f} us ({vals['pred_tb']['seconds']} s) vs PEX "
            f"{x * 1e6:.1f} us ({vals['pex_tb']['seconds']} s): {err * 100:+.1f} %"
            if err is not None else f"sim {cell}: failed {vals}")


def st_status(cell, as_json=False):
    st = {s: load(cell, s) for s in ("table", "decide", "build", "signoff", "sim")}
    if as_json:
        return json.dumps(st, indent=1, default=str)
    L = [f"status {cell} (flow/{cell}/)"]
    for s, d in st.items():
        if not d:
            L.append(f"  {s:8s} -- not run"); continue
        mark = "ok " if d.get("ok") else "NO "
        extra = {"table": lambda d: f"{len(d['fets'])} FETs, {len(d['warnings'])} warnings",
                 "decide": lambda d: (f"[{d.get('mode', '?')}] " + ("; ".join(d["blockers"]) or "buildable")
                                      + (f"; auto-answered {d['auto_answers']}" if d.get("auto_answers") else "")),
                 "build": lambda d: f"{d['size_um'][0]}x{d['size_um'][1]} um, router {d['router_check']}, {d['predrc']}",
                 "signoff": lambda d: f"DRC {d['drc']}, LVS {d['lvs']}"
                 + (f", calib factor {d['calibration'].get('mean_factor')}" if d.get("calibration") else ""),
                 "sim": lambda d: f"pred vs PEX {d['error'] * 100:+.1f} %" if d.get("error") is not None else "failed"}[s]
        L.append(f"  {s:8s} {mark} {d['time']}  {extra(d)}")
    nxt = next((s for s in ("table", "decide", "build", "signoff") if not (st[s] or {}).get("ok")), None)
    L.append(f"  next: {'flow.py ' + nxt + ' ' + cell if nxt else 'done (optional: sim)'}")
    return "\n".join(L)


def st_answer(cell, qid: str, answer: str):
    """Answer a decide.py question in layout.yaml (same as editing `answer:` by hand)."""
    import yaml
    p = cdir(cell) / "layout.yaml"
    dec = yaml.safe_load(p.read_text())
    q = next((q for q in dec["questions"] if q["id"] == qid), None)
    if not q:
        raise SystemExit(f"error: no question {qid} (open: {[q['id'] for q in dec['questions']]})")
    if q.get("options") and answer not in q["options"]:
        raise SystemExit(f"error: answer must be one of {q['options']}")
    q["answer"] = answer
    q["answered_by"] = "designer"
    p.write_text(p.read_text().split("\n", 2)[0] + "\n" + p.read_text().split("\n", 2)[1] + "\n"
                 + yaml.safe_dump(dec, sort_keys=False, width=110))
    return f"answered {qid}: {answer}\n" + st_decide(cell)


def st_run(cell, mode: str | None = None):
    out = []
    for s, fn in (("table", st_table), ("decide", lambda c: st_decide(c, mode)),
                  ("build", st_build), ("signoff", st_signoff)):
        try:
            out.append(fn(cell))
        except SystemExit as e:
            out.append(str(e)); break
        except NotImplementedError as e:
            out.append(f"stopped at {s}: {e}"); break
        if not (load(cell, s) or {}).get("ok"):
            out.append(f"stopped after {s}: needs attention (flow.py status {cell})"); break
    return "\n".join(out)


STAGES = {"table": st_table, "decide": st_decide, "build": st_build, "signoff": st_signoff,
          "sim": st_sim, "status": st_status, "run": st_run, "answer": st_answer}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in STAGES:
        print(__doc__); raise SystemExit(2)
    stage, cell = sys.argv[1], sys.argv[2]
    kw = {}
    if stage == "status" and "--json" in sys.argv:
        kw["as_json"] = True
    if stage == "signoff" and "--no-pex" in sys.argv:
        kw["pex"] = False
    if stage in ("decide", "run"):
        kw["mode"] = "manual" if "--manual" in sys.argv else "auto" if "--auto" in sys.argv else None
    if stage == "answer":
        kw = dict(qid=sys.argv[3], answer=sys.argv[4])
    print(STAGES[stage](cell, **kw))
