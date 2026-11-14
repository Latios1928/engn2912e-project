"""Bias cell netlist generator + sizing at tt/27 C."""
import subprocess, re, json, sys
LIBH = ".include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice\n.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice {c}\n"
IREF = 100e-9
LM = 8.0                    # mirror base length
W0 = 10.0                   # masters MN0 / MP0 width (L = LM)
# bias: (replica type, W, L, m, target V, mirror side, output L)
# mirror side "P": PMOS output sources current into an NMOS replica; "N": NMOS output sinks from a PMOS replica
B = {
 "Vb":        ("n", 1.0, 8.0, 1, None, "P", 8.0),
 "Vlk":       ("n", 1.0, 1.0, 8, 0.425, "P", 16.0),
 "VKdn":      ("n", 1.0, 1.0, 4, 0.588, "P", 8.0),
 "VIp":       ("n", 1.0, 1.0, 1, 0.573, "P", 8.0),
 "Vamp_bias": ("n", 0.22, 0.28, 1, 0.535, "P", 8.0),
 "VK":        ("n", 0.22, 40.0, 1, 1.22, "P", 8.0),
 "VNA":       ("p", 0.22, 20.0, 1, 1.93, "N", 8.0),
 "VKup":      ("p", 1.0, 8.0, 1, 2.35, "N", 8.0),
 "Vthr":      ("p", 0.22, 0.28, 32, 2.909, "N", 32.0),
 "VT_dpi":    ("p", 0.22, 0.28, 32, 2.90, "N", 32.0),
 "VT_inh":    ("p", 0.88, 1.12, 16, 2.7904, "N", 32.0),
}
TARGET_VB_I = 14.42e-9      # DAC reference (DACs-DPI.sch, snn_ms_tb.sch): unit current 15 nA
EXPAND = False             # write m parallel devices as separate instances (the PDK mismatch model ignores m)
def fet(name, k, d, g, s, w, l, m=1):
    model = "nfet_03v3" if k == "n" else "pfet_03v3"
    if EXPAND and m > 1:
        return "\n".join("X%s_%d %s %s %s %s %s W=%.4gu L=%.4gu nf=1" % (name, j, d, g, s, s, model, w, l) for j in range(m))
    return "X%s %s %s %s %s %s W=%.4gu L=%.4gu nf=1 m=%d" % (name, d, g, s, s, model, w, l, m)
def subckt(W):
    """W: {bias: output width}. Ports: Iref VDD VSS and the bias outputs."""
    L = [".subckt bias_cell Iref VDD VSS " + " ".join(B)]
    L.append(fet("MN0", "n", "Iref", "Iref", "VSS", W0, LM))                    # NMOS master diode
    L.append(fet("MNP", "n", "vgp", "Iref", "VSS", W["MNP"], LM))               # -> PMOS master
    L.append(fet("MP0", "p", "vgp", "vgp", "VDD", W0, LM))                      # PMOS master diode
    for b, (k, w, l, m, v, side, lo) in B.items():
        if side == "P":
            L.append(fet("MO_" + b, "p", b, "vgp", "VDD", W[b], lo))
            L.append(fet("MR_" + b, "n", b, b, "VSS", w, l, m))
        else:
            L.append(fet("MO_" + b, "n", b, "Iref", "VSS", W[b], lo))
            L.append(fet("MR_" + b, "p", b, b, "VDD", w, l, m))
    L.append(".ends bias_cell")
    return "\n".join(L) + "\n"
def targets():
    """Branch currents that put each replica at its target voltage (tt, 27 C)."""
    L = ["* targets", LIBH.format(c="typical"), "VSUP VDD 0 3.3"]
    for i, (b, (k, w, l, m, v, side, lo)) in enumerate(B.items()):
        if v is None: continue
        L.append("VB%d g%d 0 %g" % (i, i, v))
        L.append(fet("R%d" % i, k, "g%d" % i, "g%d" % i, "0" if k == "n" else "VDD", w, l, m))
    L += [".control", "op"] + ["let i%d=abs(i(VB%d))" % (i, i) for i, b in enumerate(B) if B[b][4] is not None] + \
         ["print " + " ".join("i%d" % i for i, b in enumerate(B) if B[b][4] is not None), ".endc", ".end"]
    open("tg.spice", "w").write("\n".join(L) + "\n")
    out = subprocess.run(["ngspice", "-b", "tg.spice"], capture_output=True, text=True).stdout
    vals = {int(i): float(v) for i, v in re.findall(r"^\S*?i(\d+) = ([-+0-9.eE]+)", out, re.M)}
    t = {b: (vals[i] if B[b][4] is not None else TARGET_VB_I) for i, b in enumerate(B)}
    return t
def measure(W, corner="typical", temp=27, extra=""):
    L = ["* cell", LIBH.format(c=corner), ".temp %g" % temp, "VSUP VDD 0 3.3", "Iref VDD Iref %g" % IREF, subckt(W),
         "X1 Iref VDD 0 " + " ".join(B) + " bias_cell", extra, ".control", "op"]
    L += ["let i_%s=abs(@m.x1.xmr_%s.m0[id])" % (b.lower(), b.lower()) for b in B]
    L += ["print " + " ".join("v(%s)" % b.lower() for b in B), "print " + " ".join("i_%s" % b.lower() for b in B),
          "print i(vsup)", ".endc", ".end"]
    open("m.spice", "w").write("\n".join(L) + "\n")
    out = subprocess.run(["ngspice", "-b", "m.spice"], capture_output=True, text=True).stdout
    v = {b: float(x) for b, x in re.findall(r"^v\((\w+)\) = ([-+0-9.eE]+)", out, re.M)}
    i = {b: abs(float(x)) for b, x in re.findall(r"^i_(\w+) = ([-+0-9.eE]+)", out, re.M)}
    isup = re.search(r"^i\(vsup\) = ([-+0-9.eE]+)", out, re.M)
    return v, i, (abs(float(isup.group(1))) if isup else None), out
if __name__ == "__main__":
    T = targets()
    W = {"MNP": W0}
    for b, (k, w, l, m, v, side, lo) in B.items():
        W[b] = W0 * T[b] / IREF * lo / LM
    for it in range(6):
        v, i, isup, out = measure(W)
        if not i:
            print(out[-2000:]); sys.exit(1)
        err = max(abs(i[b.lower()] / T[b] - 1) for b in B)
        for b in B:
            W[b] *= T[b] / i[b.lower()]
        # the PMOS master current: keep MP0 at Iref (MNP mirrors MN0 1:1 apart from CLM)
        print("iter %d: worst current error %.3f %%, supply %.1f nA" % (it, 100 * err, isup * 1e9))
        if err < 1e-4: break
    W = {k: round(x / 0.005) * 0.005 for k, x in W.items()}
    v, i, isup, _ = measure(W)
    print("\n%-10s %-22s %-9s %-10s %-10s %s" % ("bias", "replica", "out W/L", "target", "cell (tt27)", "branch"))
    for b, (k, w, l, m, vt, side, lo) in B.items():
        tv = "%.4f V" % vt if vt is not None else "(14.42 nA)"
        print("%-10s %s %4g/%-5g x%-3d  %5.3f/%-4g %-10s %.4f V   %.3g nA" % (b, k + "fet", w, l, m, W[b], lo, tv, v[b.lower()], i[b.lower()] * 1e9))
    print("supply current %.1f nA (incl. Iref %.0f nA) -> %.2f uW" % (isup * 1e9, IREF * 1e9, isup * 3.3e6))
    json.dump(W, open("W.json", "w"), indent=1)
