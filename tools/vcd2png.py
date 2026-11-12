#!/usr/bin/env python3
"""Draw a time window of a VCD as a clean waveform PNG (for slides).

Each --sig is  PATH[:LABEL[:FORMAT]]
  PATH    hierarchical name, e.g. tb_rf.weights or tb_pulse_gen.en[1] (bit select)
  LABEL   row label (default: the last part of PATH)
  FORMAT  for buses: hex (default), dec or bin

Example (from the repo root):
  python3 tools/vcd2png.py digital/tb_rf.vcd --start 0 --end 110 \\
      --sig tb_rf.clk --sig tb_rf.wren --sig tb_rf.addr::dec \\
      --sig tb_rf.data --sig tb_rf.weights -o slides/rf_wave.png
"""

import argparse
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def read_vcd(path):
    """{full name: (width, [(time, value string), ...])} and the timescale."""
    vars_, changes, scope, timescale = {}, {}, [], "1ns"
    t = 0
    with open(path) as f:
        text = f.read()
    m = re.search(r"\$timescale\s+(\S+)\s+\$end", text)
    if m:
        timescale = m.group(1)
    header, _, body = text.partition("$enddefinitions")
    for tok in re.finditer(r"\$(scope|upscope|var)\b(.*?)\$end", header, re.S):
        kind, args = tok.group(1), tok.group(2).split()
        if kind == "scope":
            scope.append(args[1])
        elif kind == "upscope":
            scope.pop()
        else:
            width, code, name = int(args[1]), args[2], args[3]
            vars_.setdefault(".".join(scope + [name]), (width, code))
            changes.setdefault(code, [])
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("$"):
            continue
        if s[0] == "#":
            t = int(s[1:])
        elif s[0] in "bBrR":
            val, code = s[1:].split()
            if code in changes:
                changes[code].append((t, val))
        elif s[0] in "01xXzZ" and s[1:] in changes:
            changes[s[1:]].append((t, s[0]))
    out = {}
    for name, (width, code) in vars_.items():
        out[name] = (width, changes[code])
    return out, timescale


def get_signal(vcd, path):
    """(width, [(t, value)]) for PATH, with an optional [bit] select."""
    m = re.match(r"^(.*)\[(\d+)\]$", path)
    if path in vcd:
        return vcd[path]
    if not m or m.group(1) not in vcd:
        raise SystemExit(f"vcd2png: no signal {path}")
    width, ch = vcd[m.group(1)]
    bit = int(m.group(2))
    sel = []
    for t, v in ch:
        v = v.lower().rjust(width, v[0] if v[0] in "xz" else "0")
        sel.append((t, v[width - 1 - bit]))
    return 1, sel


def window(ch, start, end):
    """Value segments [(t0, t1, value)] covering start..end."""
    segs, cur = [], None
    for t, v in ch:
        if t <= start:
            cur = v
            continue
        if t >= end:
            break
        if v != cur:
            segs.append([start if not segs else segs[-1][1], t, cur])
            cur = v
    first = start if not segs else segs[-1][1]
    segs.append([first, end, cur])
    if segs and segs[0][0] != start:
        segs[0][0] = start
    return [s for s in segs if s[1] > s[0]]


def fmt(v, kind, width):
    if v is None:
        return "?"
    if any(c in v.lower() for c in "xz"):
        return "x"
    n = int(v, 2)
    if kind == "dec":
        return str(n)
    if kind == "bin":
        return v
    return format(n, f"0{(width + 3) // 4}X")  # all hex digits, so each lines up with its bits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vcd")
    ap.add_argument("--sig", action="append", required=True, help="PATH[:LABEL[:FORMAT]]")
    ap.add_argument("--start", type=float, required=True, help="window start, VCD time units")
    ap.add_argument("--end", type=float, required=True, help="window end, VCD time units")
    ap.add_argument("--vline", type=float, action="append", default=[], help="dashed marker at this time")
    ap.add_argument("--title", default=None)
    ap.add_argument("--width", type=float, default=12.0, help="figure width, inches")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    vcd, timescale = read_vcd(args.vcd)
    rows = []
    for spec in args.sig:
        parts = spec.split(":")
        path = parts[0]
        label = parts[1] if len(parts) > 1 and parts[1] else path.split(".")[-1]
        kind = parts[2] if len(parts) > 2 else "hex"
        width, ch = get_signal(vcd, path)
        rows.append((label, width, kind, window(ch, args.start, args.end)))

    h = 0.55
    fig, ax = plt.subplots(figsize=(args.width, h * len(rows) + 0.9))
    span = args.end - args.start
    edge = span * 0.004  # slope of bus transitions
    for i, (label, width, kind, segs) in enumerate(rows):
        y0 = (len(rows) - 1 - i) * 1.0
        lo, hi = y0 + 0.15, y0 + 0.75
        ax.text(args.start - span * 0.01, y0 + 0.45, label, ha="right", va="center", fontsize=12,
                family="monospace")
        if width == 1:
            xs, ys = [], []
            for t0, t1, v in segs:
                y = hi if v == "1" else lo if v == "0" else (lo + hi) / 2
                xs += [t0, t1]
                ys += [y, y]
            ax.plot(xs, ys, color="#1f5fa8", lw=1.8, drawstyle="default")
            for t0, t1, v in segs:
                if v not in ("0", "1"):
                    ax.fill_between([t0, t1], lo, hi, color="#d9534f", alpha=0.15, lw=0)
        else:
            mid = (lo + hi) / 2
            for t0, t1, v in segs:
                e = min(edge, (t1 - t0) / 2)
                xs = [t0, t0 + e, t1 - e, t1, t1 - e, t0 + e, t0]
                ys = [mid, hi, hi, mid, lo, lo, mid]
                bad = v is None or any(c in v.lower() for c in "xz")
                ax.fill(xs, ys, color="#d9534f" if bad else "#e8f0fa", alpha=0.35 if bad else 1, lw=0)
                ax.plot(xs, ys, color="#1f5fa8", lw=1.4)
                text = fmt(v, kind, width)
                if (t1 - t0) > span * 0.0095 * max(1, len(text)):
                    ax.text((t0 + t1) / 2, mid, text, ha="center", va="center", fontsize=11,
                            family="monospace")
    for x in args.vline:
        ax.axvline(x, color="#888888", ls="--", lw=1)
    ax.set_xlim(args.start, args.end)
    ax.set_ylim(-0.2, len(rows))
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    unit = re.sub(r"^\d+", "", timescale)
    ax.set_xlabel(f"time ({unit})", fontsize=11)
    if args.title:
        ax.set_title(args.title, fontsize=13)
    fig.tight_layout()
    fig.savefig(args.out, dpi=200, bbox_inches="tight")
    print(f"vcd2png: wrote {args.out}")


if __name__ == "__main__":
    main()
