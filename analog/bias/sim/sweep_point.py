"""Evaluate bias_gen for one mirror unit size: stack factors -> calibration -> PVT + mismatch.

    python3 analog/bias/sim/sweep_point.py --wn 2 --ln 4 --wp 2 --lp 4 [--mc 50] [--dir DIR]
    python3 analog/bias/sim/sweep_point.py --params params.json     # from the sizing loop

Runs entirely in memory (bias_gen.py, bias_gen.spice and the schematic are not changed) in its own
folder, so several points can run at once. Prints one 'name = value' line per metric (the format
the sizing loop's parse_meas reads) and writes metrics.json. The unit size is the 'unit' device of
both mirror banks and the master (M1-M4, MS2, Imon); the replicas keep the size of the devices they
copy. Metrics are described in bias_tb.evaluate().
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", type=Path, help="JSON with unit_wn, unit_ln, unit_wp, unit_lp (m or um)")
    ap.add_argument("--wn", type=float)
    ap.add_argument("--ln", type=float)
    ap.add_argument("--wp", type=float)
    ap.add_argument("--lp", type=float)
    ap.add_argument("--mc", type=int, default=50)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--dir", type=Path, default=None)
    a = ap.parse_args()
    if a.params:
        p = json.loads(a.params.read_text())
        um = lambda x: x * 1e6 if x < 1e-3 else x      # the loop works in SI (m)
        a.wn, a.ln, a.wp, a.lp = (um(p[k]) for k in ("unit_wn", "unit_ln", "unit_wp", "unit_lp"))
        a.mc = int(p.get("n_mc", a.mc))
    a.wn, a.ln, a.wp, a.lp = (round(x, 3) for x in (a.wn, a.ln, a.wp, a.lp))
    d = (a.dir or Path.cwd()).resolve()
    d.mkdir(parents=True, exist_ok=True)
    os.environ["BIAS_RUNS"] = str(d / "sims")
    sys.path.insert(0, str(HERE.parent))
    sys.path.insert(0, str(HERE))
    import bias_gen as bg
    import stack_corr
    import bias_tb

    t0 = time.time()
    bg.UNIT_N, bg.UNIT_P = (a.wn, a.ln), (a.wp, a.lp)
    bg.STACK_N = stack_corr.measure("n", a.wn, a.ln, d / "sims")
    bg.STACK_P = stack_corr.measure("p", a.wp, a.lp, d / "sims")
    bg.CORR.clear()
    bg.FROZEN.clear()
    for o in bg.OUTPUTS:
        o.n_rep = o.n_max
    cal = bias_tb.calibrate(iters=8, write=False, verbose=False)
    m = bias_tb.evaluate(n_mc=a.mc, jobs=a.jobs)
    m.update({"cal_err": cal, "stack_n24": bg.STACK_N[24], "units": sum(o.p * o.s for o in bg.OUTPUTS),
              "sqt": bg.SQT, "eval_s": round(time.time() - t0, 1)})
    plan = {o.pin: [o.p, o.s, o.n_rep] for o in bg.OUTPUTS}
    (d / "metrics.json").write_text(json.dumps({"unit_n": [a.wn, a.ln], "unit_p": [a.wp, a.lp],
                                                "metrics": m, "plan": plan, "corr": bg.CORR}, indent=1))
    for k, v in m.items():
        print(f"{k} = {v:.6g}")


if __name__ == "__main__":
    main()
