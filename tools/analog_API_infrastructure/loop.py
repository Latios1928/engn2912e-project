#!/usr/bin/env python3
"""Sizing loop: propose -> validate -> simulate -> measure -> log -> repeat.

Run inside the iic-osic-tools container, from this folder:

    python3 loop.py --proposer random --budget 20            # baseline, no API
    python3 loop.py --proposer llm --model <slug> --budget 20 # needs advisor.suggest()

Each run gets its own folder runs/<timestamp>_<proposer>/ holding the configs,
the base and template netlists, one pNNNN/ folder per simulated point, and
history.jsonl (one line per candidate, rejected ones included).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import random
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from metrics import area, meets_spec, parse_meas, score
from netlist import generate_base_netlist, make_template, write_params
from params import Param, Spec, load_sim, load_space, load_spec
from runner import SimTimeout, run_ngspice

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


# ---------------------------------------------------------------- proposers
def propose_random(space: list[Param], n: int, rng: random.Random) -> list[dict]:
    return [{p.name: p.fix(rng.uniform(p.lo, p.hi)) for p in space} for _ in range(n)]


def propose_llm(space: list[Param], history: list[dict], spec: Spec, n: int, model: str | None) -> list[dict]:
    try:
        import advisor
    except Exception as e:  # SyntaxError, ImportError, ...
        raise SystemExit(f"--proposer llm needs advisor.py to import ({e!r}).")
    if not hasattr(advisor, "suggest"):
        raise SystemExit("advisor.py has no suggest() yet.")
    nan = float("nan")
    hist = [{"params": h["params"],
             "metrics": {m: nan if h["metrics"].get(m) is None else h["metrics"][m] for m in spec}}
            for h in history if h["status"] == "simulated"]
    return advisor.suggest(space, hist, spec, n=n, model=model)


# ---------------------------------------------------------------- validation
def validate(cand, space, seen, sim, spec, template, check_area=True) -> tuple[dict | None, dict, str]:
    """Return (values, areas, reason); reason is empty when the candidate is accepted.
    check_area=False lets the init point through even if it is over the area budget,
    so every run has the starting design as a reference."""
    if not isinstance(cand, dict):
        return None, {}, "not a dict"
    missing = [p.name for p in space if p.name not in cand]
    if missing:
        return None, {}, f"missing {missing}"
    try:
        values = {p.name: p.fix(cand[p.name]) for p in space}
    except (TypeError, ValueError):
        return None, {}, "non-numeric value"
    if tuple(values[p.name] for p in space) in seen:
        return values, {}, "duplicate"
    ns = {**sim["fixed"], **values}
    for c in sim["constraints"]:
        if not eval(c, {"__builtins__": {}}, dict(ns)):
            return values, {}, f"constraint failed: {c}"
    areas = area(template, ns, sim["layout_factor"])
    for m, v in areas.items():
        if check_area and m in spec and not (spec[m][0] <= v <= spec[m][1]):
            return values, areas, f"{m}={v:.4g} outside spec (rejected before simulation)"
    return values, areas, ""


# ---------------------------------------------------------------- simulation
def simulate(pid: int, values: dict, areas: dict, run_dir: Path, template: str, sim: dict) -> dict:
    pdir = run_dir / f"p{pid:04d}"
    pdir.mkdir()
    write_params({**sim["fixed"], **values}, pdir / "params.spice")
    (pdir / "tb.spice").write_text(template)
    t0 = time.time()
    try:
        log = run_ngspice(Path("tb.spice"), pdir, sim["timeout_s"])
        status = "simulated"
    except SimTimeout:
        log, status = "", "timeout"
    metrics = {**parse_meas(log, sim["measures"]), **areas}
    if status == "simulated" and "error" in log.lower() and all(
            metrics.get(m) is None for m in sim["measures"]):
        status = "sim_error"   # nothing measured and ngspice complained: see pNNNN/sim.log
    return {"id": pid, "params": values, "metrics": metrics, "status": status,
            "sim_s": round(time.time() - t0, 2)}


# ---------------------------------------------------------------- main loop
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--configs", default=HERE / "configs", type=Path)
    ap.add_argument("--proposer", choices=["random", "llm"], default="random")
    ap.add_argument("--model", default=None, help="OpenRouter model slug (llm only)")
    ap.add_argument("--budget", type=int, default=20, help="max simulations")
    ap.add_argument("--batch", type=int, default=4, help="candidates per round")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-init", action="store_true", help="skip simulating the params.yaml init point")
    ap.add_argument("--keep-going", action="store_true", help="don't stop at the first point meeting spec")
    ap.add_argument("--max-empty-rounds", type=int, default=5)
    a = ap.parse_args(argv)

    space = load_space(a.configs / "params.yaml")
    spec = load_spec(a.configs / "spec.yaml")
    sim = load_sim(a.configs / "sim.yaml")
    sim["measures"] = sorted(set(sim["measures"]) | {m.lower() for m in spec if m not in ("a_active", "a_cap")})
    rng = random.Random(a.seed)
    if a.proposer == "llm":   # fail fast instead of burning empty rounds
        a.model = a.model or os.environ.get("ADVISOR_MODEL")
        if not a.model:
            raise SystemExit("--proposer llm: pass --model <slug> or set ADVISOR_MODEL")
        if not os.environ.get("OPENROUTER_API_KEY"):
            raise SystemExit("--proposer llm: OPENROUTER_API_KEY is not set")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = HERE / "runs" / f"{stamp}_{a.proposer}"
    run_dir.mkdir(parents=True)
    shutil.copytree(a.configs, run_dir / "configs")
    if a.proposer == "llm":   # prompts, replies, token usage for this run
        import advisor
        advisor.LOG_PATH = run_dir / "advisor_log.jsonl"

    if sim.get("base_netlist"):
        base = REPO / sim["base_netlist"]
    else:
        base = generate_base_netlist(REPO / sim["testbench"], run_dir / "base", REPO)
    template = make_template(base.read_text(), space, list(sim["fixed"]), sim["analysis"])
    (run_dir / "template.spice").write_text(template)

    meta = {"started": stamp, "proposer": a.proposer, "model": a.model, "budget": a.budget,
            "batch": a.batch, "seed": a.seed, "base_netlist": str(base),
            "space": [p.__dict__ for p in space], "spec": spec}
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2, default=str))

    hist_path = run_dir / "history.jsonl"
    history: list[dict] = []
    seen: set[tuple] = set()
    sims = pid = empty = rounds = 0
    first_pass = None
    pending_init = not a.no_init and all(p.init is not None for p in space)
    t_start = time.time()

    def log(rec: dict) -> None:
        rec.setdefault("t", round(time.time() - t_start, 2))
        history.append(rec)
        with open(hist_path, "a") as f:
            f.write(json.dumps(rec, default=lambda x: None) + "\n")

    print(f"run folder: {run_dir}")
    while sims < a.budget:
        n = min(a.batch, a.budget - sims)
        rounds += 1
        if pending_init:
            cands, source, pending_init = [{p.name: p.init for p in space}], "init", False
        elif a.proposer == "random":
            cands, source = propose_random(space, n, rng), "random"
        else:
            try:
                cands, source = propose_llm(space, history, spec, n, a.model), "llm"
            except SystemExit:
                raise
            except Exception as e:
                print(f"  round {rounds}: proposer failed: {e!r}")
                cands, source = [], "llm"

        todo = []
        for c in cands[:n]:
            values, areas, reason = validate(c, space, seen, sim, spec, template,
                                             check_area=(source != "init"))
            if reason:
                log({"id": None, "round": rounds, "source": source, "params": values or c,
                     "metrics": areas, "status": "rejected", "reason": reason})
                continue
            pid += 1
            seen.add(tuple(values[p.name] for p in space))
            todo.append((pid, values, areas))

        if not todo:
            empty += 1
            print(f"  round {rounds}: no valid candidates ({empty}/{a.max_empty_rounds})")
            if empty >= a.max_empty_rounds:
                print("stopping: proposer keeps producing no valid candidates")
                break
            continue
        empty = 0

        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            results = list(ex.map(lambda t: simulate(*t, run_dir, template, sim), todo))
        for r in results:
            r.update(round=rounds, source=source, score=score(r["metrics"], spec),
                     meets_spec=meets_spec(r["metrics"], spec))
            log(r)
            sims += 1
            ms = " ".join(f"{m}={_fmt(r['metrics'].get(m))}" for m in spec)
            print(f"  p{r['id']:04d} [{source}] {r['status']:9s} score={r['score']:.3g} "
                  f"{'PASS' if r['meets_spec'] else '    '} {ms}")
            if r["meets_spec"] and first_pass is None:
                first_pass = sims
        if first_pass and not a.keep_going:
            break

    done = [h for h in history if h["status"] == "simulated"]
    best = min(done, key=lambda h: h["score"], default=None)
    summary = {"sims": sims, "rounds": rounds, "first_pass_at_sim": first_pass,
               "rejected": sum(h["status"] == "rejected" for h in history),
               "failed": sum(h["status"] in ("timeout", "sim_error") for h in history),
               "best": best, "wall_s": round(time.time() - t_start, 1)}
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=lambda x: None))
    print(f"\n{sims} sims, first pass at sim {first_pass}, "
          f"best score {best['score']:.3g} (p{best['id']:04d})" if best else f"\n{sims} sims, none succeeded")
    if best:
        for p in space:
            print(f"  {p.name} = {best['params'][p.name]:.6g} {p.unit}")
    return 0


def _fmt(x) -> str:
    return "None" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.4g}"


if __name__ == "__main__":
    sys.exit(main())
