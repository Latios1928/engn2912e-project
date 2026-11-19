#!/usr/bin/env python3
"""Plot a mixed-signal SNN run (ngspice .raw from mixed/ or librelane/snn_top/gls_ms) as
clean waveform PNGs in the style of tools/vcd2png.py, and print a per-scenario summary.

    python3 tools/snn_waves.py librelane/snn_top/gls_ms/gls_ms.raw -o slides/gls_ms
    python3 tools/snn_waves.py mixed/snn_ms_tb.raw -o slides/rtl_ms --title "RTL + SPICE"

Writes <out>_overview.png (all scenarios: pulses and spikes) and <out>_scen<N>.png (the run
window of scenario N: pulses, each neuron's membrane voltage and spikes).

The .raw has no digital testbench signals, so the scenario windows come from the testbench
timing (mixed/snn_ms_tb.v, 1 us clock): 3 us reset + 4 register writes, then per scenario
10 register writes (30 us), SETTLE us with in = 0 and RUN us with in applied. The script
checks this against the data: in every scenario with in != 0 the first input pulse must start
within one pulse period of the run window's start. Needs numpy and matplotlib (the container
has both).
"""
import argparse
import re

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLUE, FILL, GRID, RED, GREY = "#1f5fa8", "#e8f0fa", "#888888", "#d9534f", "#f2f2f2"
VTH = 1.65                                      # logic threshold (V), as SpiceBind uses
NEURONS = ["input 0", "input 1", "hidden 0", "hidden 1", "output"]   # spike[0..4]

# Scenarios of mixed/snn_ms_tb.v: (short name, in[1:0], expected fired {out,hid1,hid0,in1,in0},
# overview label, signed weights {synapse k: value}; negative = inhibitory (s[k] = 1))
SCENARIOS = {
    1: ("all weights max, no input", 0b00, "00000", "all max", {k: 15 for k in range(8)}),
    2: ("pulse 0 -> input 0 only", 0b01, "00001", "p0→in0", {0: 15, 1: 15}),
    3: ("path in1 -> hid1 -> out", 0b11, "11010", "in1→hid1→out", {1: 15, 5: 15, 7: 15}),
    4: ("as 3, hid1 -> out = 0", 0b11, "01010", "in1→hid1", {1: 15, 5: 15}),
    5: ("as 3 + in0 -| hid1 (inhibitory)", 0b11, "00011", "in0 inh. hid1", {0: 15, 1: 15, 4: -15, 5: 15, 7: 15}),
}
# Synapse k: (source, target neuron index); neurons 0..4 = in0, in1, hid0, hid1, out
SYNAPSES = {0: ("p0", 0), 1: ("p1", 1), 2: ("in0", 2), 3: ("in1", 2),
            4: ("in0", 3), 5: ("in1", 3), 6: ("hid0", 4), 7: ("hid1", 4)}


def inputs_of(weights, neuron):
    """Short note of the non-zero synapses into a neuron, e.g. '← in1 +15, in0 −15'."""
    parts = [f"{src} {'+' if w > 0 else '−'}{abs(w)}"
             for k, (src, dst) in SYNAPSES.items() if dst == neuron and (w := weights.get(k, 0))]
    return "← " + ", ".join(parts) if parts else "no input"


def read_raw(path):
    """ngspice binary or ASCII raw (real transient) -> {name: np.array}."""
    data = open(path, "rb").read()
    hdr_end = data.find(b"Binary:\n")
    ascii_ = hdr_end < 0
    if ascii_:
        hdr_end = data.find(b"Values:\n")
    hdr = data[:hdr_end].decode("latin-1")
    nvar = int(re.search(r"No\. Variables:\s*(\d+)", hdr).group(1))
    npts = int(re.search(r"No\. Points:\s*(\d+)", hdr).group(1))
    names = re.findall(r"^\s*\d+\s+(\S+)\s+\S+", hdr.split("\nVariables:")[1], re.M)[:nvar]
    if ascii_:
        # ASCII: each point is "<index> <v0>" then nvar - 1 more values
        tok = data[hdr_end + 8:].split()
        arr = np.array([float(x) for x in tok], float).reshape(-1, nvar + 1)[:, 1:]
    else:
        arr = np.frombuffer(data[hdr_end + 8:], dtype="<f8", count=npts * nvar).reshape(npts, nvar)
    out = {}
    for i, n in enumerate(names):
        n = n.lower()
        m = re.match(r"v\((.*)\)$", n)
        out[m.group(1) if m else n] = arr[:, i]
    return out


def rising(t, v, th=VTH):
    """Times where v crosses th upwards."""
    above = v > th
    idx = np.nonzero(~above[:-1] & above[1:])[0] + 1
    return t[idx]


def pair_vmem(sig, t):
    """{neuron k: vmem name}. The macro netlists (LVS reference and extraction) name the
    membrane of neuron k (spike[k]) VMEM_k, so pair by index. As a check, a neuron that spikes
    should see its own membrane drop right after its spikes; warn if not. (Pairing by that
    drop alone fails when two neurons fire at the same instants, e.g. the two inputs.)"""
    vm = {int(re.search(r"vmem_(\d)$", k).group(1)): k for k in sig if re.search(r"vmem_\d$", k)}
    pairs = {k: vm[k] for k in range(5) if k in vm}
    for k, name in pairs.items():
        edges = rising(t, sig[f"spike[{k}]"])[:20]
        if len(edges) == 0:
            continue
        v = sig[name]
        d = [v[max(np.searchsorted(t, e - 5e-6), 0)] - v[min(np.searchsorted(t, e + 15e-6), len(v) - 1)]
             for e in edges]
        if np.mean(d) < 0.3:
            print(f"WARNING: {NEURONS[k]} spikes but {name} does not drop after its spikes "
                  f"({np.mean(d):.2f} V); the VMEM_k = spike[k] naming may not hold for this netlist")
    return pairs


def windows(n_scen, first, settle_us, run_us):
    """[(scenario, load_start, run_start, run_end)] in seconds."""
    out, t = [], 15e-6                                   # 3 us reset + 4 writes x 3 us
    for k in range(first, first + n_scen):
        out.append((k, t, t + 30e-6 + settle_us * 1e-6, t + 30e-6 + (settle_us + run_us) * 1e-6))
        t += 30e-6 + (settle_us + run_us) * 1e-6
    return out


class Wave:
    """One axes, rows stacked top to bottom, drawn like tools/vcd2png.py."""

    def __init__(self, nrows, width, title, xlabel):
        self.h = 0.62
        self.fig, self.ax = plt.subplots(figsize=(width, 0.55 * nrows + 1.0))
        self.n, self.row, self.labels = nrows, 0, []
        self.ax.set_title(title, fontsize=12)
        self.ax.set_xlabel(xlabel)
        for s in ("top", "right", "left"):
            self.ax.spines[s].set_visible(False)
        self.ax.set_yticks([])

    def _y0(self):
        return self.n - 1 - self.row

    def digital(self, label, x, v, th=VTH, color=BLUE):
        y0 = self._y0()
        b = (v > th).astype(float)
        # keep only edges (step plot from the samples)
        self.ax.step(x, y0 + b * self.h, where="post", color=color, lw=1.6)
        self.labels.append((y0, label))
        self.row += 1

    def analog(self, label, x, v, vmax=3.3, color=BLUE, note=None):
        y0 = self._y0()
        self.ax.plot(x, y0 + np.clip(v, 0, vmax) / vmax * self.h, color=color, lw=1.2)
        self.ax.plot([x[0], x[-1]], [y0, y0], color="#cccccc", lw=0.6)
        if note:   # small grey note in the gap above the row (e.g. the neuron's input weights)
            self.ax.text(x[0] + (x[-1] - x[0]) * 0.005, y0 + self.h + 0.06, note, ha="left",
                         va="bottom", fontsize=8.5, color="#666666", family="monospace")
        self.labels.append((y0, label))
        self.row += 1

    def bus(self, label, segments):
        """segments: [(x0, x1, text, highlight)]"""
        y0, h = self._y0(), self.h
        for x0, x1, text, hi in segments:
            d = min((x1 - x0) * 0.15, (self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) * 0.004)
            xs = [x0, x0 + d, x1 - d, x1, x1 - d, x0 + d, x0]
            ys = [y0 + h / 2, y0 + h, y0 + h, y0 + h / 2, y0, y0, y0 + h / 2]
            self.ax.fill(xs, ys, color=hi or FILL, lw=0)
            self.ax.plot(xs, ys, color=BLUE, lw=1.2)
            if text:
                self.ax.text((x0 + x1) / 2, y0 + h / 2, text, ha="center", va="center",
                             fontsize=8.5, family="monospace", clip_on=True)
        self.labels.append((y0, label))
        self.row += 1

    def vline(self, x, **kw):
        self.ax.axvline(x, color=kw.get("color", GRID), ls=kw.get("ls", "--"), lw=kw.get("lw", 1))

    def save(self, path, x0, x1):
        self.ax.set_xlim(x0, x1)
        self.ax.set_ylim(-0.3, self.n)
        for y0, lab in self.labels:
            self.ax.text(x0 - (x1 - x0) * 0.01, y0 + self.h / 2, lab, ha="right", va="center",
                         fontsize=10, family="monospace")
        self.fig.tight_layout()
        self.fig.savefig(path, dpi=150)
        plt.close(self.fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("-o", "--out", required=True, help="output prefix, e.g. slides/gls_ms")
    ap.add_argument("--title", default="Gate-level + SPICE")
    ap.add_argument("--first", type=int, default=1, help="first scenario in the run (SCEN_FIRST)")
    ap.add_argument("--settle", type=float, default=4000, help="SETTLE (us)")
    ap.add_argument("--run", type=float, default=3000, help="RUN (us)")
    ap.add_argument("--width", type=float, default=14)
    a = ap.parse_args()

    sig = read_raw(a.raw)
    t = sig["time"]
    n_scen = 0
    for k in range(a.first, 6):
        # the testbench calls $finish right at the end of the last run window
        if windows(k - a.first + 1, a.first, a.settle, a.run)[-1][3] <= t[-1] + 100e-6:
            n_scen = k - a.first + 1
    win = windows(n_scen, a.first, a.settle, a.run)
    pairs = pair_vmem(sig, t)
    pulses = [rising(t, sig[f"pulse[{i}]"]) for i in range(2)]
    spikes = [rising(t, sig[f"spike[{k}]"]) for k in range(5)]

    # ---- summary (and the timing check)
    print(f"{a.raw}: {t[-1] * 1e3:.2f} ms simulated, {len(t)} points, {n_scen} scenario(s)")
    print("membranes: " + ", ".join(f"{NEURONS[k]} = {pairs[k]}" for k in sorted(pairs)))
    ok_all = True
    for k, t_load, t0, t1 in win:
        name, inv, exp, _, _ = SCENARIOS.get(k, (f"scenario {k}", None, None, "", {}))
        np_ = [int(((p >= t0) & (p < t1)).sum()) for p in pulses]
        if inv:
            firsts = [p[(p >= t0) & (p < t1)] for p in pulses]
            starts = [f[0] - t0 for f in firsts if len(f)]
            if not starts or min(starts) > 205e-6:
                print(f"  WARNING scenario {k}: no input pulse within 200 us of the computed run start; "
                      f"check --first/--settle/--run")
        cnt = [((s >= t0) & (s < t1)).sum() for s in spikes]
        first = [(s[(s >= t0) & (s < t1)][0] - t0) * 1e6 if cnt[j] else None for j, s in enumerate(spikes)]
        fired = "".join("1" if cnt[j] else "0" for j in (4, 3, 2, 1, 0))
        verdict = "" if exp is None else ("PASS" if fired == exp else f"FAIL (expected {exp})")
        ok_all &= verdict in ("", "PASS")
        parts = [f"{NEURONS[j]} {cnt[j]} ({first[j]:.0f} us)" for j in range(5) if cnt[j]]
        print(f"  scenario {k} [{name}], in={inv:02b}: pulses {np_[0]}/{np_[1]}, fired {fired} {verdict}; "
              + ("; ".join(parts) if parts else "no spikes"))

    # ---- overview: all scenarios
    ms = 1e3
    tt = t * ms
    rows = 2 + 2 + 5
    w = Wave(rows, a.width, f"{a.title}: scenarios {win[0][0]}-{win[-1][0]} "
             f"(settle {a.settle / 1000:g} ms with in = 00, then run {a.run / 1000:g} ms)", "time (ms)")
    w.ax.set_xlim(0, tt[-1])
    segs, insegs = [], []
    for k, t_load, t0, t1 in win:
        _, inv, exp, path, _ = SCENARIOS.get(k, ("", 0, None, "run", {}))
        segs += [(t_load * ms, t0 * ms, f"{k}: settle", GREY), (t0 * ms, t1 * ms, path, None)]
        insegs += [(t_load * ms, t0 * ms, "00", GREY), (t0 * ms, t1 * ms, f"{inv:02b}", None)]
    w.bus("scenario", segs)
    w.bus("in", insegs)
    for i in range(2):
        w.digital(f"pulse[{i}]", tt, sig[f"pulse[{i}]"])
    for k in (0, 1, 2, 3, 4):
        w.digital(f"{NEURONS[k]} spike", tt, sig[f"spike[{k}]"])
    for _, _, t0, _ in win:
        w.vline(t0 * ms)
    w.save(f"{a.out}_overview.png", 0, tt[-1])

    # ---- one figure per scenario: its run window
    us = 1e6
    for k, t_load, t0, t1 in win:
        name, inv, exp, _, wts = SCENARIOS.get(k, (f"scenario {k}", 0, None, "", {}))
        i0, i1 = np.searchsorted(t, t0 - 100e-6), np.searchsorted(t, t1)
        x = (t[i0:i1] - t0) * us
        cnt = [((s >= t0) & (s < t1)).sum() for s in spikes]
        fired = "".join("1" if cnt[j] else "0" for j in (4, 3, 2, 1, 0))
        verdict = "" if exp is None else ("PASS" if fired == exp else f"FAIL, expected {exp}")
        w = Wave(2 + 10, a.width, f"{a.title}, scenario {k}: {name} (in = {inv:02b}) - fired {fired} {verdict}",
                 "time from run start (us)")
        w.ax.set_xlim(x[0], x[-1])
        for i in range(2):
            w.digital(f"pulse[{i}]", x, sig[f"pulse[{i}]"][i0:i1])
        for j in range(5):
            vm = pairs.get(j)
            if vm:
                w.analog(f"{NEURONS[j]} VMEM", x, sig[vm][i0:i1], note=inputs_of(wts, j) if wts else None)
            w.digital(f"{NEURONS[j]} spike", x, sig[f"spike[{j}]"][i0:i1],
                      color=RED if exp and fired != exp and fired[4 - j] != exp[4 - j] else BLUE)
        for p in pulses[0][(pulses[0] >= t0) & (pulses[0] < t1)] if inv & 1 else \
                pulses[1][(pulses[1] >= t0) & (pulses[1] < t1)]:
            w.vline((p - t0) * us, lw=0.8)
        w.save(f"{a.out}_scen{k}.png", x[0], x[-1])

    print(f"wrote {a.out}_overview.png and {a.out}_scen<N>.png "
          f"({'all scenarios as expected' if ok_all else 'some scenarios differ from the expected set'})")


if __name__ == "__main__":
    main()
