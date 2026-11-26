"""Spike-amplifier characterization (5T OTA used as the neuron's comparator)."""
import re, subprocess, math, os
from concurrent.futures import ThreadPoolExecutor
import tempfile
RUN = tempfile.mkdtemp(prefix="spike_amp_")
open(os.path.join(RUN, ".spiceinit"), "w").write("set num_threads=1\n")
LIB = ".include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice\n.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice {c}\n"
VT, VAMP, VIP = 1.66, 0.535, 0.573
def amp(wp, lp, wm, lm, wt=0.22, lt=0.28):
    return f""".subckt spike_amp VDD VSS VP VN VB out
XA1 n2 VP tail VSS nfet_03v3 W={wp}u L={lp}u nf=1
XA2 out VN tail VSS nfet_03v3 W={wp}u L={lp}u nf=1
XA3 tail VB VSS VSS nfet_03v3 W={wt}u L={lt}u nf=1
XA4 n2 n2 VDD VDD pfet_03v3 W={wm}u L={lm}u nf=1
XA5 out n2 VDD VDD pfet_03v3 W={wm}u L={lm}u nf=1
.ends
"""
LOAD = """* load: the neuron's inverter 1 (M1/M3, current limit M8 at VIp) and a little wiring
XM1 inv out n4 0 nfet_03v3 W=0.22u L=0.28u nf=1
XM3 inv out VDD VDD pfet_03v3 W=0.22u L=0.28u nf=1
XM8 n4 VIp 0 0 nfet_03v3 W=1u L=1u nf=1
Cw out 0 2f
Cinv inv 0 3f
"""
def bench(sz, corner="typical", temp=27, mc_seed=None):
    s = ["* amp", LIB.format(c=corner), ".temp %g" % temp]
    if mc_seed is not None: s += [".param sw_stat_mismatch=1", ".options seed=%d" % mc_seed]
    s += [amp(*sz), "VDD VDD 0 3.3", "VB VB 0 %g" % VAMP, "VN VN 0 %g" % VT, "VIp VIp 0 %g" % VIP, LOAD,
          "X1 VDD 0 VP VN VB out spike_amp"]
    return "\n".join(s) + "\n"
def run(name, txt):
    p = os.path.join(RUN, name); open(p, "w").write(txt)
    return subprocess.run(["ngspice", "-b", name], cwd=RUN, capture_output=True, text=True, timeout=600).stdout
def num(out, key):
    m = re.search(r"^\s*%s\s*=\s*([-+0-9.eE]+)" % key, out, re.M)
    return float(m.group(1)) if m else None
def trip(sz, corner="typical", temp=27, seed=None, tag=""):
    """VP where the output crosses VDD/2, and the peak DC gain."""
    txt = bench(sz, corner, temp, seed) + "VP VP 0 1.66\n.control\ndc VP 1.36 1.96 0.0005\nmeas dc vtrip when v(out)=1.65 rise=1\n" \
          "let g = deriv(v(out))\nmeas dc gmax max g\n.endc\n.end\n"
    out = run("dc_%s.spice" % tag, txt)
    return num(out, "vtrip"), num(out, "gmax")
def ac_noise(sz, vtrip, tag=""):
    txt = bench(sz) + ("VP VP 0 dc %.6f ac 1\n.control\nop\nlet itail = abs(@m.x1.xa3.m0[id])\nprint itail\n"
          "ac dec 50 1 1e9\nlet g = db(v(out))\nlet ph = 180/pi*cph(v(out))\nmeas ac a0 find g at=1\n"
          "meas ac fu when g=0 fall=1\nmeas ac phu find ph when g=0 fall=1\nmeas ac f3 when g=a0-3 fall=1\n"
          "noise v(out) VP dec 20 1 1e5 1\nsetplot noise1\nwrdata nz_%s.txt inoise_spectrum\nsetplot noise2\nprint inoise_total\n"
          ".endc\n.end\n") % (vtrip, tag)
    out = run("ac_%s.spice" % tag, txt)
    r = {k: num(out, k) for k in ("itail", "a0", "fu", "phu", "f3", "inoise_total")}
    try:
        import numpy as np
        nz = np.loadtxt(os.path.join(RUN, "nz_%s.txt" % tag))
        r["in10"] = float(np.interp(1.0, np.log10(nz[:, 0]), nz[:, 1]))
        r["in1k"] = float(np.interp(3.0, np.log10(nz[:, 0]), nz[:, 1]))
    except Exception:
        r["in10"] = r["in1k"] = None
    return r
def delay(sz, vtrip, tag=""):
    """VP ramps at 9.5 mV/us (9.5 nA into 1 pF) through the trip point: delay to the output crossing VDD/2,
    measured from the instant VP passes the DC trip point."""
    v0 = vtrip - 0.05
    tr = 0.1 / 9.5e3
    txt = bench(sz) + "VP VP 0 pwl(0 %.6f %.6g %.6f)\n.control\ntran 2n %.6g 0 2n\nmeas tran tout when v(out)=1.65 rise=1\n.endc\n.end\n" % (v0, tr, v0 + 0.1, tr)
    out = run("tr_%s.spice" % tag, txt)
    t = num(out, "tout")
    return None if t is None else t - 0.05 / 9.5e3
def area(sz):
    wp, lp, wm, lm = sz[:4]
    return 2 * wp * lp + 2 * wm * lm + 0.22 * 0.28
def characterize(sz, n_mc=60, tag="x"):
    vt, g = trip(sz, tag=tag)
    with ThreadPoolExecutor(8) as ex:
        mc = list(ex.map(lambda s: trip(sz, seed=s, tag="%s_mc%d" % (tag, s))[0], range(1, n_mc + 1)))
    mc = [m for m in mc if m is not None]
    mu = sum(mc) / len(mc); sig = (sum((m - mu) ** 2 for m in mc) / len(mc)) ** 0.5
    a = ac_noise(sz, vt, tag); d = delay(sz, vt, tag)
    return {"size": sz, "vos_sys_mV": (vt - VT) * 1e3, "vos_sigma_mV": sig * 1e3, "gain_dc": g, **a, "delay_us": d * 1e6 if d else None,
            "area_um2": area(sz)}
if __name__ == "__main__":
    import json, sys
    r = characterize((0.22, 0.28, 0.22, 0.28), tag="base")
    print(json.dumps(r, indent=1))
