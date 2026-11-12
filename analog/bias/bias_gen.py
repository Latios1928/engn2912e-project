"""On-chip bias generator for snn_analog: one description, written as a SPICE subcircuit.

    python3 analog/bias/bias_gen.py            # writes analog/bias/bias_gen.spice, prints the ratio plan

Architecture (see analog/bias/README.md):
  1. Master reference: subthreshold beta multiplier, I0 = n*UT*ln(K)/R with an n-well R.
     The n-well's +2900 ppm/K nearly cancels UT's +3300 ppm/K, so I0 is flat over temperature.
  2. 4-bit trim: R = R15 + (15 - code)*dR. Bit i = 1 shorts a segment of 2^i dR (more current).
  3. Mirror tree from the master's gates: nFET outputs (from Vgn) sink current, pFET outputs
     (from Vgp) source it. Every output is P unit devices in parallel, S in series.
  4. Each output feeds a diode-connected replica of the transistor its pin drives (same type,
     W, L and rail, the scheme of the xor-inhibition branch's bias_replica.py), so the generated voltage
     tracks process and temperature. Weak-inversion replicas use n_rep copies in parallel
     (mismatch / sqrt(n_rep)); strong-inversion ones (VK, VNA, VKup) use s_rep in series to
     cut their current.
  5. VT (comparator threshold, ~VDD/2): four identical diode-connected pFETs in series,
     each in its own n-well, so VT = VDD/2 by symmetry at a few nA.

Pins: VDD VSS trim[3] trim[2] trim[1] trim[0] Imon, then the 10 bias outputs in OUTPUTS order, then VT
(the 11 bias pins of main's snn_analog.sym, same order).
"""

from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
IREF = 14.42e-9          # DAC unit reference (analog/neuron/DACs-DPI.sch)
VDD = 3.3

# ---------------------------------------------------------------- master reference
K = 8                     # M2 : M1 size ratio
P1 = 8                    # M1 = 8 unit nFETs
PM = 4                    # M3 = M4 = 4 unit pFETs
UNIT_N = (1.0, 6.0)       # unit nFET W, L (um): from the unit sweep (results/unit_sweep.md)
UNIT_P = (1.0, 6.0)       # unit pFET W, L (um)
RW = 2.0                  # n-well resistor width (um)
I0 = 16 * IREF            # master current at mid trim code 8 (230.7 nA)
UN = I0 / P1              # current per unit nFET (2 Iref)
UP = I0 / PM              # current per unit pFET (4 Iref)
SQT = 247.53               # n-well squares that give I0 exactly (set by sim/bias_tb.py --calibrate)
TRIM_R15 = 0.743          # R(code 15) / SQT: lets the ss corner (I0 -18 %) reach +10 % margin
TRIM_R0 = 1.42            # R(code 0) / SQT: lets the ff corner (I0 +28 %) reach -10 % margin
TRIM_NOM = 9              # code closest to SQT (tt)


def trim_squares(sqt=SQT):
    """(R15 squares, dR squares): R(code) = R15 + (15 - code) * dR."""
    r15 = sqt * TRIM_R15
    return r15, (sqt * TRIM_R0 - r15) / 15


def trim_ratio(code):
    """Nominal I0(code) / I0 (= SQT / R(code))."""
    return 1 / (TRIM_R15 + (15 - code) * (TRIM_R0 - TRIM_R15) / 15)


@dataclass
class Out:
    pin: str
    rtype: str            # replica type: "n" (nFET to VSS, fed by a pFET source) or "p"
    w: float              # replica (driven device) W, L in um
    l: float
    i_t: float            # current of one replica at the nominal voltage (A), from bias_replica.md
    v_nom: float          # nominal pin voltage (V), from bias_replica.md / xor_tb
    n_rep: int = 1        # replicas in parallel
    s_rep: int = 1        # replicas in series (strong inversion only)
    rep_scale: float = 1  # replica drawn at rep_scale x W and x L (same W/L) for matching
    p: int = 0            # mirror output: P units in parallel ...
    s: int = 0            # ... of S units in series (filled in by plan())
    note: str = ""
    n_min: int = 0        # fewest replicas plan() may use (default n_rep / 2)

    def __post_init__(self):
        self.n_max = self.n_rep   # plan() may use n_min .. n_max replicas
        self.n_min = self.n_min or max(1, self.n_max // 2)

    @property
    def i_branch(self):
        return self.i_t * self.n_rep / self.s_rep

    @property
    def unit(self):       # unit current of the mirror bank that feeds it
        return UP if self.rtype == "n" else UN


# Driven devices and nominal voltages of main's 2-2-1 network: analog/snn/snn_analog.sch with
# DPI.sch, neuron_sized.sch, spike_amplifier.sch; voltages from mixed/snn_ms_tb.sch. i_t = current of
# one driven device at its nominal voltage (tt, 27 C, drain = gate), from sim/targets.py.
# DPI.sch uses minimum 0.22/0.28 devices: one replica that small has sigma(V) ~ 25 mV, so Vthr and
# VT_dpi use 32 copies (the synapse devices themselves keep that spread: see README).
OUTPUTS = [
    Out("Vb", "n", 1.0, 8.0, IREF, 0.0, n_rep=4, note="DAC unit reference, Mref of DACs-DPI.sch"),
    # Vthr: gate of the DPI's nFET M1, compared by the M1/M2 pair with net1, the gate of the output
    # pFET M4 (which is referenced to VDD), so its replica is a copy of M4 from VDD.
    Out("Vthr", "p", 0.22, 0.28, 73.67e-12, 2.909, n_rep=32, n_min=32, note="DPI gain (replica of M4)"),
    Out("VT_dpi", "p", 0.22, 0.28, 93.70e-12, 2.900, n_rep=32, n_min=32, note="DPI tau (replica of M3)"),
    Out("VNA", "p", 1.0, 1.0, 5049e-9, 1.9300, s_rep=16, note="neuron Na current source"),
    Out("Vlk", "n", 1.0, 1.0, 0.5415e-9, 0.4250, n_rep=16, note="membrane leak"),
    Out("VK", "n", 1.0, 1.0, 17520e-9, 1.2200, s_rep=16, note="neuron K current"),
    Out("VIp", "n", 1.0, 1.0, 24.02e-9, 0.5730, n_rep=8, note="neuron Ip"),
    Out("VKup", "p", 1.0, 1.0, 551.3e-9, 2.3500, s_rep=2, note="neuron K pull-up"),
    Out("VKdn", "n", 1.0, 1.0, 34.18e-9, 0.5880, n_rep=8, note="neuron K pull-down"),
    # The tail is 0.22/0.28: one replica that small has sigma(V) = 25 mV, and a larger replica at the
    # same W/L does not track it over corners (short-channel effects), so 4 real copies in parallel.
    Out("Vamp_bias", "n", 0.22, 0.28, 96.54e-9, 0.5350, n_rep=4, n_min=4, note="spike amplifier tail"),
]
VT_DIV = (1.0, 10.0)      # VT divider pFET W, L (um), 4 in series
DECAP = (10.0, 10.0)      # default MOS decap per output (W, L um), referenced to the replica's rail
DECAP_PIN = {}            # per-pin override: pin -> (W, L) or None for no decap (sim/decap_sweep.py)


def decap(pin):
    return DECAP_PIN.get(pin, DECAP)
IMON_P = 8                # Imon: 8 unit nFETs (a copy of M1) sink I0 = 16 Iref (230.7 nA) for trimming
PINS = ["VDD", "VSS", "trim[3]", "trim[2]", "trim[1]", "trim[0]", "Imon"] + [o.pin for o in OUTPUTS] + ["VT"]

# Stack factors (sim/stack_corr.py, tt, for UNIT_N / UNIT_P): current of S units in series x S / one unit
# in the master diode, output at 2.5 V (nFET) / 0.7 V (pFET). Unit nFETs in series behave like one longer
# device, and longer nFETs have a lower threshold in this PDK (halo implant): +7 % to +29 %.
STACK_N = {1: 1.0434, 2: 1.1226, 3: 1.1602, 4: 1.1823, 5: 1.1969, 6: 1.2072, 7: 1.2149, 8: 1.2209,
           9: 1.2256, 10: 1.2295, 12: 1.2354, 14: 1.2398, 16: 1.2431, 18: 1.2457, 20: 1.2479,
           22: 1.2497, 24: 1.2513}
STACK_P = {1: 1.0055, 2: 0.9645, 3: 0.9521, 4: 0.9467, 5: 0.9439, 6: 0.9424, 7: 0.9415, 8: 0.9409,
           9: 0.9406, 10: 0.9405, 12: 0.9404, 14: 0.9406, 16: 0.9408, 18: 0.9411, 20: 0.9414,
           22: 0.9417, 24: 0.9421}


def stack_factor(typ, s):
    t = STACK_N if typ == "n" else STACK_P
    if s in t:
        return t[s]
    lo = max(k for k in t if k < s)
    hi = min(k for k in t if k > s)
    return t[lo] + (t[hi] - t[lo]) * (s - lo) / (hi - lo)


# Residual per-pin correction (pin voltage, replica stacks), measured by sim/bias_tb.py --calibrate
# as g / m with the stack factors already applied.
CORR = {"Vb": 0.9641, "VT_dpi": 0.9596, "VNA": 1.0824, "VK": 1.1036, "VIp": 0.9523, "VKup": 1.0524,
        "VKdn": 0.9531, "Vamp_bias": 0.9676}

# Frozen plan (from plan() with the corrections above): pin -> (P, S, n_rep). Edit only together
# with a rerun of sim/bias_tb.py --calibrate; set FROZEN = {} to let plan() choose again.
FROZEN = {"Vb": (5, 6, 3), "Vthr": (1, 15, 32), "VT_dpi": (2, 23, 32), "VNA": (18, 2, 1), "Vlk": (1,
          7, 14), "VK": (17, 1, 1), "VIp": (3, 1, 7), "VKup": (16, 2, 1), "VKdn": (5, 1, 8),
          "Vamp_bias": (7, 1, 4)}


def plan(max_p=24, max_s=24, tol=0.025):
    """Pick (P, S), and n_rep within [n_rep/2, n_rep] for weak-inversion replicas, so that
    unit * P / S matches the branch current within tol with the fewest devices."""
    for o in OUTPUTS:
        if o.pin in FROZEN:
            o.p, o.s, o.n_rep = FROZEN[o.pin]
            continue
        reps = range(o.n_min, o.n_max + 1) if o.s_rep == 1 else [o.n_max]
        best = None
        for n in reps:
            want = o.i_t * n / o.s_rep / o.unit / CORR.get(o.pin, 1.0)
            bank = "p" if o.rtype == "n" else "n"      # n-type replicas are fed by the pFET bank
            for s in range(1, max_s + 1):
                f = stack_factor(bank, s)
                for p in range(1, max_p + 1):
                    err = abs(p / s * f / want - 1)
                    # within tol: fewest mirror units, a dropped replica counting as 2 units (area vs matching)
                    cost = (max(err, tol), p * s + 2 * (o.n_max - n))
                    if best is None or cost < best[0]:
                        best = (cost, p, s, n)
        o.p, o.s, o.n_rep = best[1], best[2], best[3]
    return OUTPUTS


def _dev(name, d, g, s, b, typ, w, l, m=1):
    """m unit instances in parallel. Written out one by one (not m=), because the PDK mismatch
    model ignores m: an m=8 device would get the mismatch of a single unit."""
    model = "nfet_03v3" if typ == "n" else "pfet_03v3"
    if m == 1:
        return f"X{name} {d} {g} {s} {b} {model} L={l}u W={w}u nf=1"
    return "\n".join(f"X{name}_m{k} {d} {g} {s} {b} {model} L={l}u W={w}u nf=1" for k in range(m))


def _stack(name, top, g, bot, b, typ, w, l, p, s):
    """S devices in series (top = drain side), each P in parallel."""
    nodes = [top] + [f"{name}_{k}" for k in range(1, s)] + [bot]
    return [_dev(f"{name}_{k}", nodes[k], g, nodes[k + 1], b, typ, w, l, p) for k in range(s)]


def subckt(sqt=SQT):
    plan()
    wn, ln = UNIT_N
    wp, lp = UNIT_P
    r15, dr = trim_squares(sqt)
    L = [f"* bias_gen: generated by analog/bias/bias_gen.py (I0 = {I0 * 1e9:.1f} nA with SQT = {sqt:.2f} squares)",
         ".subckt bias_gen " + " ".join(PINS),
         "* --- master reference: beta multiplier",
         _dev("M1", "Vgn", "Vgn", "VSS", "VSS", "n", wn, ln, P1),
         _dev("M2", "Vgp", "Vgn", "Vr", "VSS", "n", wn, ln, K * P1),
         _dev("M3", "Vgp", "Vgp", "VDD", "VDD", "p", wp, lp, PM),
         _dev("M4", "Vgn", "Vgp", "VDD", "VDD", "p", wp, lp, PM),
         "* --- start-up: MS1 (4 x 0.22/50 series, always on) pulls X up while Vgn = 0, MS3 pulls Vgp down;",
         "*     once running, MS2 (mirror of M1, 2x) holds X at VSS",
         *_stack("MS1", "X", "VSS", "VDD", "VDD", "p", 0.22, 50, 1, 4),
         _dev("MS2", "X", "Vgn", "VSS", "VSS", "n", wn, ln, 2 * P1),
         _dev("MS3", "Vgp", "X", "VSS", "VSS", "n", 0.5, 4, 1),
         f"* --- n-well resistor with 4-bit trim: R15 = {r15:.1f} sq, dR = {dr:.2f} sq (x {RW} um)",
         f"XR15 Vr t3 VSS nwell r_length={r15 * RW:.3f}u r_width={RW}u"]
    nodes = ["t3", "t2", "t1", "t0", "VSS"]
    for i, bit in enumerate([3, 2, 1, 0]):
        a, b = nodes[i], nodes[i + 1]
        L.append(f"XRT{bit} {a} {b} VSS nwell r_length={(2 ** bit) * dr * RW:.3f}u r_width={RW}u")
        L.append(_dev(f"MT{bit}", a, f"trim[{bit}]", b, "VSS", "n", 4.0, 0.28, 2 ** max(bit - 1, 0)))
    L.append(f"* --- trim monitor: {IMON_P} units sink {IMON_P}/{P1} x I0 from the Imon pad (hold it at 1.65 V)")
    L.append(_dev("MMON", "Imon", "Vgn", "VSS", "VSS", "n", wn, ln, IMON_P))
    for o in OUTPUTS:
        L.append(f"* --- {o.pin}: {o.note}; {o.i_branch * 1e9:.3g} nA = {o.p}/{o.s} x {o.unit * 1e9:.2f} nA,"
                 f" replica {o.rtype}FET {o.w}/{o.l} x{o.n_rep} parallel x{o.s_rep} series")
        tag = o.pin.upper()
        if o.rtype == "p":
            # sink from the nFET bank, into a pFET diode replica from VDD
            L += _stack(f"MO{tag}", o.pin, "Vgn", "VSS", "VSS", "n", wn, ln, o.p, o.s)
            L += _rep(tag, o, "VDD")
            if decap(o.pin):
                L.append(_dev(f"MC{tag}", "VDD", o.pin, "VDD", "VDD", "p", *decap(o.pin)))
        else:
            L += _stack(f"MO{tag}", o.pin, "Vgp", "VDD", "VDD", "p", wp, lp, o.p, o.s)
            L += _rep(tag, o, "VSS")
            if decap(o.pin):
                L.append(_dev(f"MC{tag}", "VSS", o.pin, "VSS", "VSS", "n", *decap(o.pin)))
    L.append("* --- VT = VDD/2: four identical pFET diodes, each source tied to its own n-well")
    vt_nodes = ["VDD", "vt3", "VT", "vt1", "VSS"]
    for k in range(4):
        s_, d_ = vt_nodes[k], vt_nodes[k + 1]
        L.append(_dev(f"MVT{k}", d_, d_, s_, s_, "p", *VT_DIV))
    if decap("VT"):
        L.append(_dev("MCVT", "VSS", "VT", "VSS", "VSS", "n", *decap("VT")))
    L.append(".ends bias_gen")
    return "\n".join(L) + "\n"


def _rep(tag, o, rail):
    """Diode replica: n_rep in parallel, s_rep in series, gates on the pin, from rail."""
    k = o.rep_scale
    return _stack(f"MR{tag}", o.pin, o.pin, rail, rail, o.rtype, round(o.w * k, 3), round(o.l * k, 3),
                  o.n_rep, o.s_rep)


def report():
    plan()
    tot = 0
    print(f"I0 = {I0 * 1e9:.1f} nA, nFET unit {UN * 1e9:.2f} nA, pFET unit {UP * 1e9:.2f} nA")
    for o in OUTPUTS:
        got = o.unit * o.p / o.s * stack_factor("p" if o.rtype == "n" else "n", o.s) * CORR.get(o.pin, 1.0)
        tot += got
        print(f"{o.pin:10s} {o.rtype} rep {o.w}/{o.l} x{o.n_rep}p x{o.s_rep}s  branch {o.i_branch * 1e9:8.2f} nA "
              f"-> {o.p:2d}/{o.s:2d} units = {got * 1e9:8.2f} nA ({(got / o.i_branch - 1) * 100:+.1f} %)")
    print(f"outputs total {tot * 1e6:.2f} uA")


if __name__ == "__main__":
    report()
    (HERE / "bias_gen.spice").write_text(subckt())
    print("wrote", HERE / "bias_gen.spice")
