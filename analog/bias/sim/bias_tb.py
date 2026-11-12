"""Testbench for analog/bias/bias_gen.spice. Run inside the IIC-OSIC container from the project root.

    python3 analog/bias/sim/bias_tb.py --calibrate   # set SQ8 and the mirror corrections at tt, 27 C
    python3 analog/bias/sim/bias_tb.py               # corners x temperature, supply, trim, start-up
    python3 analog/bias/sim/bias_tb.py --mc 100      # mismatch at tt, 27 C

Each output pin drives a probe: one copy of the transistor that pin biases on the chip, with its
drain held at its gate voltage (a unity VCVS, no load). The probe current divided by the study's
calibrated current (bias_replica.md) is the bias error 'g' that the network would see. All g
values follow the master current (trimmed on chip with Imon); what trim cannot fix is the
spread of g / m between outputs, where m = Imon / (2 Iref) is the master current error.
"""

import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bias_gen as bg  # noqa: E402

RUNS = Path(os.environ.get("BIAS_RUNS", HERE / "runs"))   # sweep points each use their own folder
PDK = "/foss/pdks/gf180mcuD/libs.tech/ngspice"
CORNERS = {"tt": ("typical", "res_typical"), "ss": ("ss", "res_ss"), "ff": ("ff", "res_ff"),
           "sf": ("sf", "res_typical"), "fs": ("fs", "res_typical")}
TEMPS = [0, 27, 85]


def deck(sub, corner="tt", temp=27, code=None, vdd=3.3, seed=None, ctl=None, glob=False):
    """seed: local mismatch on. glob (with seed): global process variation instead (PDK 'statistical'
    section, sw_stat_global = 1, mismatch off), i.e. a random process point per sample."""
    mos, res = CORNERS[corner]
    if glob:
        mos = "statistical"
    code = bg.TRIM_NOM if code is None else code
    bits = [(code >> b) & 1 for b in (3, 2, 1, 0)]
    L = ["* bias_gen testbench",
         f".include {PDK}/design.ngspice",
         f".lib {PDK}/sm141064.ngspice {mos}",
         f".lib {PDK}/sm141064.ngspice {res}",
         f".temp {temp}"]
    if seed is not None:
        stat = ".param sw_stat_global=1 sw_stat_mismatch=0" if glob else ".param sw_stat_mismatch=1"
        L += [stat, f".options seed={seed}"]
    L += [sub, f"Vdd VDD 0 {vdd} ac 1", f"Vdb VDDB VDD 0",
          *[f"Vt{b} tr{b} 0 {vdd * x}" for b, x in zip((3, 2, 1, 0), bits)],
          "Vmon Imon 0 1.65",
          "X1 VDDB 0 tr3 tr2 tr1 tr0 Imon " + " ".join(o.pin for o in bg.OUTPUTS) + " VT bias_gen"]
    for o in bg.OUTPUTS:
        rail = "0" if o.rtype == "n" else "VDD"
        model = "nfet_03v3" if o.rtype == "n" else "pfet_03v3"
        L += [f"E{o.pin} pd_{o.pin} 0 {o.pin} 0 1",
              f"XP{o.pin} pd_{o.pin} {o.pin} ps_{o.pin} {rail} {model} L={o.l}u W={o.w}u nf=1",
              f"Vp{o.pin} {'ps_' + o.pin if o.rtype == 'n' else 'VDD'} {'0' if o.rtype == 'n' else 'ps_' + o.pin} 0"]
    meas = " ".join(f"g_{o.pin}=$&@{{abs(i(Vp{o.pin}))/{o.i_t:g}}}".replace("@", "") for o in bg.OUTPUTS)
    lets = "\n".join(f"let g_{o.pin}=abs(i(Vp{o.pin}))/{o.i_t:g}" for o in bg.OUTPUTS)
    echo = "echo RES m=$&m itot=$&itot vt=$&v(VT) " + " ".join(
        f"g_{o.pin}=$&g_{o.pin} v_{o.pin}=$&v({o.pin})" for o in bg.OUTPUTS)
    ctl = ctl or f"op\nlet m=abs(i(Vmon))/{bg.IMON_P * bg.UN * bg.trim_ratio(code):g}\nlet itot=abs(i(Vdb))\n{lets}\n{echo}"
    del meas
    L += [".control", ctl, "quit", ".endc", ".end"]
    return "\n".join(L) + "\n"


def run(name, text):
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / ".spiceinit").write_text("set ngbehavior=hsa\nset num_threads=1\n")
    (RUNS / f"{name}.spice").write_text(text)
    p = subprocess.run(["ngspice", "-b", f"{name}.spice"], cwd=RUNS, capture_output=True, text=True, timeout=900)
    log = p.stdout + p.stderr
    (RUNS / f"{name}.log").write_text(log)
    rows = []
    for m in re.finditer(r"^RES (.*)$", log, re.M):
        rows.append({k: float(v) for k, v in re.findall(r"(\w+)=(\S+)", m.group(1))})
    if not rows:
        raise RuntimeError(f"no results in {RUNS / (name + '.log')}")
    return rows[0] if len(rows) == 1 else rows


def pmap(fn, items, jobs=8):
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(fn, items))


def calibrate(iters=6, write=True, verbose=True):
    """SQT so that m = 1 at tt / 27 C / TRIM_NOM; then, per output, CORR so that g / m = 1.
    CORR depends on the (P, S, n_rep) chosen, so it is iterated until the plan stops changing."""
    sqt = bg.SQT
    for _ in range(4):
        r = run("cal", deck(bg.subckt(sqt)))
        if verbose:
            print(f"  m={r['m']:.4f} at SQT {sqt:.2f}")
        if abs(r["m"] - 1) < 0.002:
            break
        sqt = sqt * r["m"] ** 1.05
    bg.SQT = sqt
    bg.FROZEN.clear()
    for it in range(iters):
        r = run("cal", deck(bg.subckt(sqt)))
        rel = {o.pin: r[f"g_{o.pin}"] / r["m"] for o in bg.OUTPUTS}
        worst = max(abs(v - 1) for v in rel.values())
        if verbose:
            print(f"  iter {it}: worst |g/m - 1| = {worst * 100:.1f} %  "
                  + " ".join(f"{k}={v:.3f}" for k, v in rel.items()))
        if worst < 0.03:
            break
        for k, v in rel.items():
            if abs(v - 1) >= 0.02:
                bg.CORR[k] = bg.CORR.get(k, 1.0) * v
    if verbose:
        print("SQT =", round(sqt, 2))
        print("plan: " + ", ".join(f"{o.pin} {o.p}/{o.s} n{o.n_rep}" for o in bg.OUTPUTS))
    if write:
        write_back(sqt)
    return worst


def write_back(sqt):
    """Store SQT, CORR and the frozen plan in bias_gen.py."""
    f = Path(bg.__file__)
    s = f.read_text()
    s = re.sub(r"^SQT = [0-9.]+", f"SQT = {sqt:.2f}", s, flags=re.M)

    def block(name, items, fmt):
        body = ", ".join(fmt(k, v) for k, v in items)
        lines, line = [], f"{name} = {{"
        for part in body.split(", "):
            if len(line) + len(part) > 100:
                lines.append(line.rstrip())
                line = " " * (len(name) + 4)
            line += part + ", "
        return "\n".join(lines + [line.rstrip(", ") + "}"])

    corr = block("CORR", bg.CORR.items(), lambda k, v: f'"{k}": {v:.4f}')
    frozen = block("FROZEN", [(o.pin, (o.p, o.s, o.n_rep)) for o in bg.OUTPUTS], lambda k, v: f'"{k}": {v}')
    s = re.sub(r"^CORR = \{.*?\}\n", corr + "\n", s, flags=re.M | re.S)
    s = re.sub(r"^FROZEN = \{.*?\}\n", frozen + "\n", s, flags=re.M | re.S)
    f.write_text(s)
    print("updated", f)


def table(rows, keys, title):
    print(f"\n{title}")
    print(f"{'case':14s} {'m':>6s} " + " ".join(f"{k[:9]:>9s}" for k in keys) + "  spread  itot uA")
    for name, r in rows:
        rel = [r[f"g_{k}"] / r["m"] for k in keys]
        print(f"{name:14s} {r['m']:6.3f} " + " ".join(f"{x:9.3f}" for x in rel)
              + f"  {max(rel) / min(rel):6.3f}  {r['itot'] * 1e6:6.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--mc", type=int, default=0)
    ap.add_argument("--mc-only", action="store_true")
    ap.add_argument("--compare-sch", action="store_true", help="xschem netlist of bias_gen.sch vs bias_gen.spice")
    ap.add_argument("--startup", action="store_true", help="supply ramps 10 ns - 10 ms, all corners")
    ap.add_argument("--psrr", action="store_true", help="AC supply rejection per output")
    ap.add_argument("--compliance", action="store_true", help="output voltage window per mirror output, Imon pad")
    ap.add_argument("--mc-global", type=int, default=0, help="Monte Carlo with global process variation + mismatch")
    a = ap.parse_args()
    if a.startup or a.psrr or a.compliance or a.mc_global:
        if a.startup:
            startup()
        if a.psrr:
            for c, t in (("tt", 27), ("ss", 85), ("ff", 0)):
                psrr(c, t)
        if a.compliance:
            compliance()
        if a.mc_global:
            mc_global(a.mc_global)
        return
    if a.compare_sch:
        compare_sch()
        return
    if a.mc_only:
        mismatch(bg.subckt(), [o.pin for o in bg.OUTPUTS], a.mc or 100)
        return
    if a.calibrate:
        calibrate()
        return
    sub = bg.subckt()
    keys = [o.pin for o in bg.OUTPUTS]
    cases = [(c, t) for c in CORNERS for t in TEMPS]
    res = pmap(lambda ct: run(f"pvt_{ct[0]}_{ct[1]}", deck(sub, ct[0], ct[1])), cases)
    r0 = res[cases.index(("tt", 27))]
    print(f"tt 27 C code {bg.TRIM_NOM}:"
          " m = %.4f, VT = %.4f V, bias_gen supply %.2f uA" % (r0["m"], r0["vt"], r0["itot"] * 1e6))
    print("pin voltages (generated vs study nominal):")
    for o in bg.OUTPUTS:
        print(f"  {o.pin:10s} {r0['v_' + o.pin]:.4f}  (nominal {o.v_nom:.4f})  g={r0['g_' + o.pin]:.3f}")
    table([(f"{c} {t}C", r) for (c, t), r in zip(cases, res)], keys,
          "g / m per output (1 = exact ratio); m = master current error before trim")
    # supply
    sup = pmap(lambda v: run(f"vdd_{v}", deck(sub, vdd=v)), [3.0, 3.15, 3.3, 3.45, 3.6])
    table([(f"VDD {v}", r) for v, r in zip([3.0, 3.15, 3.3, 3.45, 3.6], sup)], keys, "supply (tt, 27 C)")
    # trim: I0 for every code at tt, ss (res high) and ff (res low)
    print("\ntrim code -> I0 / (16 Iref)  (tt / ss / ff, 27 C)")
    tr = {c: pmap(lambda k: run(f"trim_{c}_{k}", deck(sub, c, 27, k))["m"] * bg.trim_ratio(k), range(16))
          for c in ("tt", "ss", "ff")}
    for k in range(16):
        print(f"  {k:2d}  " + "  ".join(f"{tr[c][k]:.3f}" for c in tr))
    for c in tr:
        best = min(range(16), key=lambda k: abs(tr[c][k] - 1))
        print(f"  {c}: best code {best}, m = {tr[c][best]:.3f}")
    # start-up with a 100 us supply ramp
    ctl = (f"tran 2u 3m\nmeas tran m1 find i(Vmon) at=2.9m\nlet m=abs(m1)/{bg.IMON_P * bg.UN * bg.trim_ratio(bg.TRIM_NOM):g}\n"
           f"meas tran vthr find v(Vthr) at=2.9m\necho RES m=$&m vthr=$&vthr")
    for c in ("tt", "ss", "ff"):
        for t in (0, 85):
            d = deck(sub, c, t, ctl=ctl).replace("Vdd VDD 0 3.3 ac 1", "Vdd VDD 0 pwl(0 0 100u 3.3)")
            r = run(f"start_{c}_{t}", d)
            print(f"start-up {c} {t}C: m = {r['m']:.3f}, Vthr = {r['vthr']:.3f} V")
    if a.mc:
        mismatch(sub, keys, a.mc)


def probe_curves(corner="tt", temp=27):
    """Mismatch-free I(V) of every probe device (drain = gate), to read the bias error off a
    Monte Carlo pin voltage without the probe's own mismatch."""
    L = ["* probe curves", f".include {PDK}/design.ngspice", f".lib {PDK}/sm141064.ngspice {CORNERS[corner][0]}",
         f".temp {temp}", "Vdd VDD 0 3.3", "Vg g 0 0"]
    for o in bg.OUTPUTS:
        if o.rtype == "n":
            L += [f"X{o.pin} g g s{o.pin} 0 nfet_03v3 L={o.l}u W={o.w}u nf=1", f"V{o.pin} s{o.pin} 0 0"]
        else:
            L += [f"X{o.pin} g g s{o.pin} VDD pfet_03v3 L={o.l}u W={o.w}u nf=1", f"V{o.pin} VDD s{o.pin} 0"]
    L += [".control", "dc Vg 0 3.3 0.0005",
          "wrdata probe_iv.txt " + " ".join(f"abs(i(V{o.pin}))" for o in bg.OUTPUTS), "quit", ".endc", ".end"]
    run_raw("probe_iv", "\n".join(L) + "\n")
    data = [list(map(float, l.split())) for l in (RUNS / "probe_iv.txt").read_text().splitlines() if l.strip()]
    v = [r[0] for r in data]
    return {o.pin: (v, [r[2 * k + 1] for r in data]) for k, o in enumerate(bg.OUTPUTS)}


def interp_log(curve, x):
    import bisect
    import math
    v, i = curve
    k = min(max(bisect.bisect_left(v, x), 1), len(v) - 1)
    f = (x - v[k - 1]) / (v[k] - v[k - 1])
    return math.exp(math.log(i[k - 1]) * (1 - f) + math.log(i[k]) * f)


def mismatch(sub, keys, n, verbose=True, jobs=8):
    """Returns {pin: sigma after trim}, plus 'm' (sigma of the Imon reading)."""
    import statistics as st
    curves = probe_curves()
    nom = run("mc_nom", deck(sub))
    mc = pmap(lambda s: run(f"mc_{s}", deck(sub, seed=s)), range(1, n + 1), jobs)
    ms = [r["m"] / nom["m"] for r in mc]
    out = {"m": st.pstdev(ms)}
    for k in keys:
        i0 = interp_log(curves[k], nom["v_" + k])
        out[k] = st.pstdev([interp_log(curves[k], r["v_" + k]) / i0 / m for r, m in zip(mc, ms)])
    if not verbose:
        return out
    print(f"\nmismatch, {n} samples (tt, 27 C, code {bg.TRIM_NOM}). Bias error from the generated voltage,")
    print("read on a mismatch-free device: g = I(V_pin) / I(V_pin nominal). 'after trim' = g / m, where")
    print("m is the Imon reading (trim brings m to 1). sigma / min / max:")
    ms = [r["m"] / nom["m"] for r in mc]
    print(f"  {'m (Imon)':12s} {st.pstdev(ms):.3f} {min(ms):.3f} {max(ms):.3f}")
    for k in keys:
        c = curves[k]
        i0 = interp_log(c, nom["v_" + k])
        g = [interp_log(c, r["v_" + k]) / i0 for r in mc]
        gt = [x / m for x, m in zip(g, ms)]
        print(f"  {k:12s} raw {st.pstdev(g):.3f} {min(g):.3f} {max(g):.3f}   after trim {st.pstdev(gt):.3f} "
              f"{min(gt):.3f} {max(gt):.3f}   sigma(V) {st.pstdev([r['v_' + k] for r in mc]) * 1e3:.2f} mV")
    return out


def area_um2(sub):
    """Gate area (sum of W*L over every transistor, decaps included) and n-well resistor area, um^2."""
    gate = res = 0.0
    for line in sub.splitlines():
        if line.startswith("X") and "fet_03v3" in line:
            w = float(re.search(r"W=([0-9.]+)u", line).group(1))
            l = float(re.search(r"L=([0-9.]+)u", line).group(1))
            m = re.search(r" m=(\d+)", line)
            gate += w * l * (int(m.group(1)) if m else 1)
        elif line.startswith("X") and " nwell " in line:
            res += float(re.search(r"r_length=([0-9.]+)u", line).group(1)) * bg.RW
    return gate, res


def evaluate(n_mc=50, jobs=8):
    """Metrics of the current bias_gen configuration (call calibrate first). Keys:
    pvt_err: worst |g/m - 1| over 5 corners x 0/27/85 C and all outputs (what trim cannot fix);
    vdd_err: same over 3.0-3.6 V; sigma_max: worst after-trim mismatch sigma of the outputs whose
    replicas copy sized devices; sigma_dpi (Vthr, VT_dpi) and sigma_vamp, which copy minimum-size
    0.22/0.28 devices; m_sigma (Imon);
    i_supply (A); a_gate, a_res, a_total (um^2, gate area x1, resistor x1)."""
    sub = bg.subckt()
    keys = [o.pin for o in bg.OUTPUTS]
    cases = [(c, t) for c in CORNERS for t in TEMPS]
    res = pmap(lambda ct: run(f"pvt_{ct[0]}_{ct[1]}", deck(sub, ct[0], ct[1])), cases, jobs)
    sup = pmap(lambda v: run(f"vdd_{v}", deck(sub, vdd=v)), [3.0, 3.6], jobs)
    err = lambda rows: max(abs(r[f"g_{k}"] / r["m"] - 1) for r in rows for k in keys)
    r0 = res[cases.index(("tt", 27))]
    mm = mismatch(sub, keys, n_mc, verbose=False, jobs=jobs)
    gate, resa = area_um2(sub)
    return {"pvt_err": err(res), "vdd_err": err(sup),
            # sigma_max: the biases whose replicas copy sized devices; the DPI biases and Vamp_bias copy
            # minimum-size 0.22/0.28 devices and are reported on their own
            "sigma_max": max(v for k, v in mm.items() if k not in ("m", "Vamp_bias", "Vthr", "VT_dpi")),
            "sigma_dpi": max(mm["Vthr"], mm["VT_dpi"]), "sigma_vamp": mm["Vamp_bias"], "m_sigma": mm["m"],
            "i_supply": r0["itot"], "a_gate": gate, "a_res": resa, "a_total": gate + resa}


def startup(jobs=8):
    """Supply ramps from 0 V: 10 ns, 1 us, 100 us, 10 ms, at 5 corners x 0 / 27 / 85 C. Pass when
    Imon settles within 1 % of its DC operating point (the reference does not stay in the
    zero-current state). Returns the rows."""
    sub = bg.subckt()
    unit = bg.IMON_P * bg.UN * bg.trim_ratio(bg.TRIM_NOM)
    cases = [(r, c, t) for r in ("10n", "1u", "100u", "10m") for c in CORNERS for t in TEMPS]
    ct = [(c, t) for c in CORNERS for t in TEMPS]
    dc = dict(zip(ct, pmap(lambda x: run(f"su_dc_{x[0]}_{x[1]}", deck(sub, x[0], x[1]))["m"], ct, jobs)))

    def one(rct):
        r, c, t = rct
        tr = {"10n": 1e-8, "1u": 1e-6, "100u": 1e-4, "10m": 1e-2}[r]
        tstop = tr + 3e-3
        # print step 1 us; ngspice refines the step at the PWL corner itself. Save only i(Vmon):
        # a 10 ns ramp with a fixed tiny step and all nodes saved runs out of memory.
        # Imon is averaged over the last 1 ms: the instantaneous current through a voltage source
        # is noisy in a transient with variable steps (+-37 % sample to sample, same average).
        ctl = (f"save i(Vmon)\ntran 1u {tstop:g} 0 10u uic\n"
               f"meas tran m1 avg i(Vmon) from={tstop - 1e-3:g} to={tstop:g}\n"
               f"let m=abs(m1)/{unit:g}\necho RES m=$&m")
        d = deck(sub, c, t, ctl=ctl).replace("Vdd VDD 0 3.3 ac 1", f"Vdd VDD 0 pwl(0 0 {tr:g} 3.3)")
        m = run(f"su_{r}_{c}_{t}", d)["m"]
        return {"ramp": r, "corner": c, "temp": t, "m": m, "mdc": dc[(c, t)],
                "ok": abs(m / dc[(c, t)] - 1) < 0.01}
    rows = pmap(one, cases, jobs)
    print(f"\nstart-up: {sum(r['ok'] for r in rows)}/{len(rows)} settle within 1 % of the DC point "
          "(ramps 10 ns / 1 us / 100 us / 10 ms x 5 corners x 0/27/85 C)")
    for r in rows:
        if not r["ok"]:
            print(f"  FAIL ramp {r['ramp']} {r['corner']} {r['temp']}C: m = {r['m']:.3f} vs DC {r['mdc']:.3f}")
    return rows


def psrr(corner="tt", temp=27):
    """AC: 1 V of supply ripple; what reaches each driven device's gate drive. For a pFET-type bias
    (source on VDD) the drive is VDD - V(pin), for an nFET-type bias V(pin). Reported in dB (0 dB =
    the whole ripple) and as the current change of a weak-inversion device per 10 mV of supply
    ripple (dV / (n UT), n UT ~ 35 mV)."""
    sub = bg.subckt()
    freqs = ["10", "1k", "100k", "1meg", "10meg"]
    lets = []
    for o in bg.OUTPUTS + [type("V", (), {"pin": "VT", "rtype": "n"})()]:
        expr = f"1 - v({o.pin})" if o.rtype == "p" else f"v({o.pin})"
        lets.append(f"let ps_{o.pin} = mag({expr})")
    ctl = ("ac dec 10 1 100meg\n" + "\n".join(lets) + "\n"
           + "\n".join(f"meas ac r_{o}_{f} find ps_{o} at={f}\necho RES r_{o}_{f}=$&r_{o}_{f}"
                       for o in [x.pin for x in bg.OUTPUTS] + ["VT"] for f in freqs))
    rows = run(f"psrr_{corner}_{temp}", deck(sub, corner, temp, ctl=ctl))
    r = {k: v for row in (rows if isinstance(rows, list) else [rows]) for k, v in row.items()}
    import math
    print(f"\nPSRR ({corner}, {temp} C): supply ripple reaching the gate drive, dB; [current change per 10 mV ripple]")
    print(f"  {'pin':10s} " + " ".join(f"{f:>16s}" for f in freqs))
    for p in [x.pin for x in bg.OUTPUTS] + ["VT"]:
        cells = []
        for f in freqs:
            x = r[f"r_{p}_{f}"]
            cells.append(f"{20 * math.log10(max(x, 1e-12)):6.1f} [{x * 0.01 / 0.035 * 100:5.2f}%]")
        print(f"  {p:10s} " + " ".join(f"{c:>16s}" for c in cells))
    return r


def compliance(corners=("tt", "ss", "ff")):
    """Each mirror output with its replica detached and the pin forced by a swept source: the voltage
    window where the output current stays within 1 % of its value at the nominal pin voltage,
    against the pin voltages the generator itself produces over corners. Also the Imon pad."""
    base = bg.subckt()
    keys = [o.pin for o in bg.OUTPUTS]
    vpin = {}
    for c in corners:
        for t in TEMPS:
            r = run(f"cmpl_op_{c}_{t}", deck(base, c, t))
            for k in keys:
                vpin.setdefault(k, []).append(r["v_" + k])
    print("\ncompliance: output current within 1 % of its value at the nominal pin voltage, over V(pin);"
          " pin range = what the generator produces over tt/ss/ff x 0/27/85 C")
    for o in bg.OUTPUTS:
        tag = o.pin.upper()
        sub = "\n".join((l.replace(f" {o.pin} ", f" rep_{o.pin} ") if l.startswith(f"XMR{tag}_") else l)
                         for l in base.splitlines())
        win = []
        for c in corners:
            nom = sum(vpin[o.pin]) / len(vpin[o.pin])
            ctl = (f"dc Vf 0 3.3 0.01\nwrdata cmpl_{o.pin}_{c}.txt abs(i(Vf))\n")
            d = deck(sub, c, 27, ctl=ctl)
            d = d.replace(f"X1 VDDB 0 tr3", f"Vf vf_{o.pin} 0 {nom:.4f}\nX1 VDDB 0 tr3")
            d = re.sub(rf"(X1 VDDB 0 tr3 tr2 tr1 tr0 Imon .*?) {o.pin} ", rf"\1 vf_{o.pin} ", d, count=1)
            run_raw(f"cmpl_{o.pin}_{c}", d)
            rows = [list(map(float, l.split())) for l in (RUNS / f"cmpl_{o.pin}_{c}.txt").read_text().splitlines()
                    if l.strip() and not l.lstrip().startswith(("v", "s"))]
            v = [x[0] for x in rows]
            i = [x[1] for x in rows]
            k0 = min(range(len(v)), key=lambda k: abs(v[k] - nom))
            ok = [k for k in range(len(v)) if abs(i[k] / i[k0] - 1) < 0.01]
            lo = k0
            while lo - 1 in ok:
                lo -= 1
            hi = k0
            while hi + 1 in ok:
                hi += 1
            win.append((v[lo], v[hi]))
        wl, wh = max(w[0] for w in win), min(w[1] for w in win)
        pl, ph = min(vpin[o.pin]), max(vpin[o.pin])
        margin = min(pl - wl, wh - ph)
        print(f"  {o.pin:10s} 1 %-window {wl:.2f}-{wh:.2f} V (worst of {'/'.join(corners)}), pin {pl:.3f}-{ph:.3f} V,"
              f" margin {margin:+.2f} V {'OK' if margin > 0.1 else 'CHECK'}")
    # Imon pad
    ctl = "dc Vmon 0 3.3 0.01\nwrdata cmpl_imon.txt abs(i(Vmon))\n"
    run_raw("cmpl_imon", deck(base, ctl=ctl))
    rows = [list(map(float, l.split())) for l in (RUNS / "cmpl_imon.txt").read_text().splitlines()
            if l.strip() and not l.lstrip().startswith(("v", "s"))]
    i165 = min(rows, key=lambda x: abs(x[0] - 1.65))[1]
    good = [x[0] for x in rows if abs(x[1] / i165 - 1) < 0.01]
    print(f"  Imon pad: within 1 % of its 1.65 V value for {min(good):.2f}-{max(good):.2f} V")


def mc_global(n, jobs=8):
    """Global process variation (random process point per sample, local mismatch off): does every
    output still track its driven device? g / m from the in-deck probes, which share the sample's
    process (m = Imon reading, which the per-chip trim removes)."""
    import statistics as st
    sub = bg.subckt()
    rows = pmap(lambda s: run(f"mcg_{s}", deck(sub, seed=s, glob=True)), range(1, n + 1), jobs)
    ms = [r["m"] for r in rows]
    print(f"\nglobal process Monte Carlo, {n} samples (tt nominal, 27 C, code {bg.TRIM_NOM}): "
          f"Imon reading m: mean {st.mean(ms):.3f} sigma {st.pstdev(ms):.3f} min {min(ms):.3f} max {max(ms):.3f}")
    print("  per output, g / m (after trim): mean / sigma / min / max")
    for o in bg.OUTPUTS:
        x = [r[f"g_{o.pin}"] / r["m"] for r in rows]
        print(f"  {o.pin:10s} {st.mean(x):.3f} {st.pstdev(x):.3f} {min(x):.3f} {max(x):.3f}")
    vt = [r["vt"] for r in rows]
    print(f"  VT         {st.mean(vt):.4f} V, sigma {st.pstdev(vt) * 1e3:.2f} mV")


def sch_subckt():
    """Netlist analog/bias/bias_gen.sch with xschem and return it as a .subckt."""
    out = RUNS / "sch"
    out.mkdir(parents=True, exist_ok=True)
    root = HERE.parents[2]
    subprocess.run(["xschem", "-q", "-x", "-r", "-n", "-s", "-o", str(out), "-N", "bias_gen_sch.spice",
                    str(root / "analog/bias/bias_gen.sch")], cwd=root, capture_output=True, text=True, timeout=300)
    t = (out / "bias_gen_sch.spice").read_text()
    t = re.sub(r"^\*\*\.subckt", ".subckt", t, flags=re.M)
    t = re.sub(r"^\*\+", "+", t, flags=re.M)
    t = re.sub(r"^\*\*\.ends", ".ends", t, flags=re.M)
    assert ".subckt bias_gen" in t and ".ends" in t
    return t


def compare_sch():
    a, b = bg.subckt(), sch_subckt()
    keys = [o.pin for o in bg.OUTPUTS]
    for c, t in [("tt", 27), ("ss", 85), ("ff", 0)]:
        ra = run(f"cmp_spice_{c}", deck(a, c, t))
        rb = run(f"cmp_sch_{c}", deck(b, c, t))
        worst = max(abs(rb["v_" + k] - ra["v_" + k]) for k in keys)
        print(f"{c} {t}C: m spice {ra['m']:.4f} sch {rb['m']:.4f}; VT {ra['vt']:.4f} / {rb['vt']:.4f}; "
              f"worst pin voltage difference {worst * 1e3:.2f} mV; supply {ra['itot'] * 1e6:.2f} / {rb['itot'] * 1e6:.2f} uA")


def run_raw(name, text):
    RUNS.mkdir(exist_ok=True)
    (RUNS / f"{name}.spice").write_text(text)
    p = subprocess.run(["ngspice", "-b", f"{name}.spice"], cwd=RUNS, capture_output=True, text=True, timeout=900)
    (RUNS / f"{name}.log").write_text(p.stdout + p.stderr)


if __name__ == "__main__":
    main()
