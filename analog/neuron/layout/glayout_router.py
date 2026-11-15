"""
Small row/channel router for gLayout cells (GF180).

Layer plan (fixed, so nets never meet by accident):
    met2  device buses (drawn by glayout)
    met3  vertical: risers from device buses, cross-channel columns, ring drops
    met4  horizontal: channel tracks
    met5  cap top-plate links

Every shape the router draws is recorded with its net; `check()` reports any two shapes of
different nets on one layer that overlap or are closer than the layer's min spacing.
Run it before DRC/LVS: a short costs one line of output instead of a DRC/LVS loop.
"""
from __future__ import annotations

from collections import defaultdict

from gdsfactory.components import rectangle
from glayout import via_stack

PITCH = 0.8      # track / riser pitch: 0.5 wire + 0.3 space
WIRE = 0.5
SPACE = {"met2": 0.28, "met3": 0.3, "met4": 0.3, "met5": 0.44}


class Router:
    def __init__(self, pdk, top):
        self.pdk, self.top = pdk, top
        self.shapes = defaultdict(list)      # layer -> [(x0, y0, x1, y1, net, tag)]

    # ------------------------------------------------------------------ drawing
    def rect(self, layer, x0, y0, x1, y1, net, tag=""):
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
        r = self.top << rectangle(size=(x1 - x0, y1 - y0), layer=self.pdk.get_glayer(layer))
        r.move((x0, y0))
        self.shapes[layer].append((x0, y0, x1, y1, net, tag))
        return r

    def record(self, layer, x0, y0, x1, y1, net, tag=""):
        """Register metal drawn by someone else (e.g. glayout device buses) for the checker
        and the parasitic predictor, without drawing anything."""
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
        self.shapes[layer].append((x0, y0, x1, y1, net, tag))

    def wire(self, layer, p0, p1, net, w=WIRE, tag=""):
        (x0, y0), (x1, y1) = p0, p1
        return self.rect(layer, min(x0, x1) - w / 2, min(y0, y1) - w / 2,
                         max(x0, x1) + w / 2, max(y0, y1) + w / 2, net, tag)

    def via(self, x, y, lo, hi, net, tag=""):
        v = self.top << via_stack(self.pdk, lo, hi)
        v.move((x - v.center[0], y - v.center[1]))
        h = max(v.xsize, v.ysize) / 2
        lv = int(lo[-1]) if lo.startswith("met") else 1
        for m in range(max(lv, 2), int(hi[-1]) + 1):
            if f"met{m}" in SPACE:
                self.shapes[f"met{m}"].append((x - h, y - h, x + h, y + h, net, tag or "via"))
        return v

    # ------------------------------------------------------------------ checking
    def check(self, limit=12):
        """List shorts / spacing errors between different nets. Empty string = clean."""
        errs = []
        for layer, shp in self.shapes.items():
            sp = SPACE.get(layer, 0.3)
            for i in range(len(shp)):
                a = shp[i]
                for b in shp[i + 1:]:
                    if a[4] == b[4]:
                        continue
                    gx = max(b[0] - a[2], a[0] - b[2])
                    gy = max(b[1] - a[3], a[1] - b[3])
                    if gx < sp - 1e-6 and gy < sp - 1e-6:
                        kind = "SHORT" if gx < 0 and gy < 0 else f"gap {max(gx, gy):.2f}"
                        errs.append(f"{layer} {kind}: {a[4]}[{a[5]}] vs {b[4]}[{b[5]}] "
                                    f"at ({a[0]:.2f},{a[1]:.2f})")
        if not errs:
            return ""
        more = f"\n... {len(errs) - limit} more" if len(errs) > limit else ""
        return "\n".join(errs[:limit]) + more


def pack_tracks(spans: dict, pitch=PITCH, space=SPACE["met4"]):
    """Left-edge track assignment. spans: net -> (xmin, xmax). Returns net -> track index."""
    order = sorted(spans, key=lambda n: spans[n][0])
    track_end, out = [], {}
    for n in order:
        x0, x1 = spans[n]
        for t, end in enumerate(track_end):
            if x0 - WIRE / 2 >= end + space:
                track_end[t] = x1 + WIRE / 2
                out[n] = t
                break
        else:
            track_end.append(x1 + WIRE / 2)
            out[n] = len(track_end) - 1
    return out, len(track_end)
