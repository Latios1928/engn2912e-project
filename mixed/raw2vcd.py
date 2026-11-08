#!/usr/bin/env python3
"""Convert an ngspice binary .raw file to .vcd for gtkwave / Surfer.

Based on CAD7/raw2vcd.py of engn1600-team1, simplified:
  https://github.com/mgyee/engn1600-team1
  - name[i] traces become one digital bus `name`, thresholded at VDD/2;
  - traces matching --real (default: membrane voltages, currents) stay analog;
  - every other trace becomes a 1-bit wire, thresholded at VDD/2.
A value is only written when it changes (analog: by more than --resolution).

Usage: raw2vcd.py [--vth 1.65] [--real REGEX] in.raw [out.vcd]
"""

import argparse
import re
from pathlib import Path

import numpy as np
from vcd import VCDWriter

BIT_RE = re.compile(r"^(.*)\[(\d+)\]$")


def read_raw(path):
    """(names, data[points, vars]) from a binary, real-valued .raw file."""
    names, nvars, npts = [], 0, 0
    with open(path, "rb") as f:
        while True:
            line = f.readline()
            if not line:
                raise SystemExit("raw2vcd: no Binary: section (ASCII or complex raw files are not supported)")
            line = line.decode("ascii", "ignore").strip()
            if line.startswith("No. Variables:"):
                nvars = int(line.split(":")[1])
            elif line.startswith("No. Points:"):
                npts = int(line.split(":")[1])
            elif line == "Variables:":
                names = [f.readline().decode("ascii", "ignore").split()[1] for _ in range(nvars)]
            elif line == "Binary:":
                off = f.tell()
                break
    data = np.memmap(path, dtype=np.float64, mode="r", offset=off, shape=(npts, nvars))
    return names, data


def clean(name):
    m = re.match(r"^[vV]\((.*)\)$", name)
    return m.group(1) if m else name


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw", type=Path)
    ap.add_argument("vcd", type=Path, nargs="?")
    ap.add_argument("--vth", type=float, default=1.65)
    ap.add_argument("--real", default=r"(?i)vmem|^i\(|#branch", help="regex of traces kept analog")
    ap.add_argument("--resolution", type=float, default=1e-3, help="analog value step written to the VCD")
    args = ap.parse_args()
    out = args.vcd or args.raw.with_suffix(".vcd")
    real_re = re.compile(args.real)

    names, data = read_raw(args.raw)
    t = data[:, names.index("time")]

    buses, wires, reals = {}, {}, {}
    for col, raw_name in enumerate(names):
        if raw_name == "time":
            continue
        n = clean(raw_name)
        m = BIT_RE.match(n)
        if real_re.search(raw_name):
            reals[n] = col
        elif m:
            buses.setdefault(m.group(1), {})[int(m.group(2))] = col
        else:
            wires[n] = col

    # Per trace, the sample indices where its value changes, found with numpy;
    # then all changes are written in time order. Analog values are rounded to
    # --resolution so that tiny steps do not each become an event.
    tn = np.rint(t * 1e9).astype(np.int64)
    events = []  # (sample index, var number, value)
    specs = []  # (name, kind, size)
    for base, bits in sorted(buses.items()):
        size = max(bits) + 1
        # One row of characters per sample, MSB first; works for any width.
        chars = np.full((len(t), size), ord("x"), dtype=np.uint8)
        for i, col in bits.items():
            chars[:, size - 1 - i] = np.where(data[:, col] >= args.vth, ord("1"), ord("0"))
        code = chars.view(f"S{size}").ravel()
        specs.append((base, "wire", size))
        events.append((code, lambda c: c.decode()))
    for n, col in sorted(wires.items()):
        specs.append((n, "wire", 1))
        events.append(((data[:, col] >= args.vth).astype(np.int64), lambda c: str(int(c))))
    for n, col in sorted(reals.items()):
        specs.append((n, "real", 64))
        q = np.rint(data[:, col] / args.resolution).astype(np.int64)
        events.append((q, lambda c: float(c) * args.resolution))

    changes = []
    for k, (code, _) in enumerate(events):
        idx = np.flatnonzero(code[1:] != code[:-1]) + 1
        changes.append(np.stack([np.concatenate(([0], idx)), np.full(len(idx) + 1, k)], axis=1))
    order = np.concatenate(changes)
    order = order[np.lexsort((order[:, 1], order[:, 0]))]

    with open(out, "w") as f:
        w = VCDWriter(f, timescale="1 ns", date="raw2vcd")
        vars_ = [w.register_var("ngspice", n, kind, size=size) for n, kind, size in specs]
        for i, k in order:
            code, fmt = events[k]
            w.change(vars_[k], int(tn[i]), fmt(code[i]))
        w.close(int(tn[-1]))
    print(f"raw2vcd: wrote {out} ({len(buses)} buses, {len(wires)} wires, {len(reals)} analog)")


if __name__ == "__main__":
    main()
