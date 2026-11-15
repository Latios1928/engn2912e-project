"""
gLayout generator for the sized neuron (analog/neuron/neuron_sized.sch, spike amplifier
flattened as A1..A5).

    env -u PYTHONPATH PDK_ROOT=/foss/pdks .venv-glayout/bin/python analog/neuron/layout/gen_neuron_glayout.py

Writes neuron_glayout.gds and neuron_glayout_lvs_ref.spice next to this file.
(The hand-drawn neuron_sized.gds from gen_neuron.py is left untouched.)

Layout-only changes vs the schematic (glayout cannot draw W < 0.5 um; W/L is kept):
    M1..M5  0.22/0.28 -> 0.5/0.64        M6  0.22/5 -> 0.5/11.36
Assumed fix: spike amplifier M2 gate = VN (= neuron VT). In spike_amplifier_sized.sch the
VN wire currently stops 10 units short of its label, leaving M2's gate floating.

Floorplan (bottom -> top):
    bottom channel   NMOS gate nets + bias pins   (met4 tracks)
    NMOS row         all NMOS, dummy ring, one shared DNWELL (body VSS)
    mid channel      all source/drain nets, VSS, VDD
    PMOS row         all PMOS rotated 180 deg (gates up), dummy ring, n-tap ring
    top channel      PMOS gate nets + bias pins
    left columns     met3 links for nets that live in more than one channel
    right            C2 (VMEM) and C1 (spike) MIM caps, met4 VSS spine, met5 top-plate links
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from gdsfactory.component import Component
from glayout import gf180 as pdk, straight_route, mimcap

from glayout_helpers import fet, describe
from glayout_rings import dummy_ring, dnw_guard, nwell_guard
from glayout_router import Router, pack_tracks, PITCH, WIRE

GAP = 0.6            # device-to-device gap in a row
DUMMY_L = 1.0        # dummy-ring gate length (both rows)
CH_MARGIN = 0.9      # ring metal -> first/last channel track (centre)
CAP_GAP = 2.0        # spine centre -> MIM plate: 0.25 + MIMTM.1 (1.2) + margin

#            name  kind  W     L      drain      gate        source
NMOS = [("A3", "n", 0.5, 0.64, "tail", "Vamp_bias", "VSS"),
        ("A1", "n", 4.0, 2.0, "amp_n2", "VMEM", "tail"),
        ("A2", "n", 4.0, 2.0, "net1", "VT", "tail"),
        ("M1", "n", 0.5, 0.64, "net2", "net1", "net4"),
        ("M8", "n", 1.0, 1.0, "net4", "VIp", "VSS"),
        ("M2", "n", 0.5, 0.64, "spike", "net2", "net5"),
        ("M7", "n", 1.0, 1.0, "net5", "VKdn", "VSS"),
        ("M6", "n", 0.5, 11.36, "VMEM", "spike", "net6"),
        ("M10", "n", 1.0, 1.0, "net6", "VK", "VSS"),
        ("M11", "n", 1.0, 1.0, "VMEM", "Vlk", "VSS")]
PMOS = [("A4", "p", 0.5, 8.0, "amp_n2", "amp_n2", "VDD"),
        ("A5", "p", 0.5, 8.0, "net1", "amp_n2", "VDD"),
        ("M3", "p", 0.5, 0.64, "net2", "net1", "VDD"),
        ("M4", "p", 0.5, 0.64, "spike", "net2", "net3"),
        ("M12", "p", 1.0, 1.0, "net3", "VKup", "VDD"),
        ("M5", "p", 0.5, 0.64, "VMEM", "net2", "net7"),
        ("M9", "p", 1.0, 1.0, "net7", "VNA", "VDD")]
CAPS = [("C1", "spike", 10.0), ("C2", "VMEM", 22.18)]
PINS = ["VSS", "VDD", "VMEM", "VNA", "Vlk", "VK", "VIp", "VKup", "VKdn", "Vamp_bias", "VT", "spike"]


def bus(dev, term):
    a, b = dev.ports[f"multiplier_0_{term}_W"].center, dev.ports[f"multiplier_0_{term}_E"].center
    return min(a[0], b[0]), max(a[0], b[0]), a[1]


def row(top, spec, x0):
    refs = {}
    x = x0
    for name, kind, w, l, *_ in spec:
        r = top << fet(pdk, kind, w, l, with_dummy=False)
        if kind == "p":
            r.rotate(180)                      # gates on top, S/D buses at the bottom
        r.move((x - r.xmin, -r.center[1]))
        x = r.xmax + GAP
        refs[name] = r
    return refs


def risers(refs, spec):
    """(net, x, y_bus, channel) for every terminal. S at left end, D at right end, G centre."""
    out = []
    for name, kind, w, l, d, g, s in spec:
        r = refs[name]
        sx0, sx1, sy = bus(r, "source")
        dx0, dx1, dy = bus(r, "drain")
        gx0, gx1, gy = bus(r, "gate")
        sd_ch, g_ch = ("mid", "bot") if kind == "n" else ("mid", "top")
        out += [(s, sx0 + WIRE / 2, sy, sd_ch, f"{name}.S"),
                (d, dx1 - WIRE / 2, dy, sd_ch, f"{name}.D"),
                (g, (gx0 + gx1) / 2, gy, g_ch, f"{name}.G")]
    return out


def ring_y(port):
    """y of a via pad sitting on a ring side, given that side's outer/inner edge port."""
    return port.center[1] + (-WIRE / 2 if round(port.orientation) == 90 else WIRE / 2)


def neuron():
    top = Component("neuron_glayout_build")
    R = Router(pdk, top)

    # ------------------------------------------------------------------ NMOS row in DNW
    nref = row(top, NMOS, 0.0)
    dn = dummy_ring(pdk, top, list(nref.values()), "n", length=DUMMY_L, name="DN")
    g = dnw_guard(pdk, top, list(nref.values()) + [dn.ref], body="VSS", dnw="VDD", sub="VSS")
    top << straight_route(pdk, dn.ports["rail_N"], g.ports["body_N_top_met_S"])

    # ------------------------------------------------------------------ PMOS row (built at y=0)
    ncx = (nref["A3"].xmin + nref["M11"].xmax) / 2
    pref = row(top, PMOS, 0.0)
    pw = pref["M9"].xmax - pref["A4"].xmin
    for r in pref.values():
        r.movex(ncx - pw / 2)
    dp = dummy_ring(pdk, top, list(pref.values()), "p", length=DUMMY_L, name="DP")
    ng = nwell_guard(pdk, top, list(pref.values()) + [dp.ref], body="VDD")
    p_rail = top << straight_route(pdk, dp.ports["rail_N"], ng.ports["body_N_top_met_S"])
    pmos_objs = list(pref.values()) + [dp.ref, ng.ref, p_rail]

    x_vss = dn.ref.xmin + 0.8          # body ring -> sub ring -> VSS track
    x_dnw = dn.ref.xmax - 0.8          # DNW tie -> VDD track -> PMOS n-tap ring

    def plan(sh):
        """Track plan for a PMOS-row x shift `sh`. Returns (conflicts, plan dict)."""
        terms = risers(nref, NMOS) + [(n, x + sh, y, c, t) for n, x, y, c, t in risers(pref, PMOS)]
        chans_of = {}
        for net, *_r, ch, _t in terms:
            chans_of.setdefault(net, set()).add(ch)
        chans_of["VSS"].add("mid"); chans_of["VDD"].add("mid")
        cross = sorted(n for n, c in chans_of.items() if len(c) > 1)
        left = min(g.ref.xmin, ng.ref.xmin + sh) - 1.0
        col_x = {n: left - i * PITCH for i, n in enumerate(cross)}
        pin_x = left - len(cross) * PITCH - 0.6
        x_sp = max(g.ref.xmax, ng.ref.xmax + sh) + 2.4
        cap_x = {"spike": x_sp - 2.4, "VMEM": x_sp - 0.8}
        x_ntap = ng.ref.xmin + sh + 0.8                 # n-tap ring -> VDD track

        def spans(ch):
            sp = {}
            for net, x, _y, c, _t in terms:
                if c == ch:
                    lo, hi = sp.get(net, (x, x)); sp[net] = (min(lo, x), max(hi, x))
            for net in list(sp) + (["VSS", "VDD"] if ch == "mid" else []):
                lo, hi = sp.get(net, (x_vss, x_vss) if net == "VSS" else (x_dnw, x_dnw))
                if net in col_x:
                    lo = min(lo, col_x[net])
                if net in PINS and ch != "mid":
                    lo = min(lo, pin_x)
                if ch == "mid" and net == "VSS":
                    lo, hi = min(lo, x_vss), max(hi, x_sp)
                if ch == "mid" and net == "VDD":
                    lo, hi = min(lo, x_dnw, x_ntap), max(hi, x_dnw, x_ntap)
                if ch == "mid" and net in cap_x:
                    hi = max(hi, cap_x[net])
                sp[net] = (lo, hi)
            return sp

        tracks = {}
        for ch in ("bot", "mid", "top"):
            sp = spans(ch)
            idx, n = pack_tracks(sp)
            if ch == "mid":
                # NMOS-heavy tracks low, PMOS-heavy tracks high: risers from the two rows
                # then end before they can meet
                pmos_names = {p[0] for p in PMOS}
                score = [0] * n
                for net, _x, _y, c, tag in terms:
                    if c == "mid":
                        score[idx[net]] += 1 if tag.split(".")[0] in pmos_names else -1
                order = sorted(range(n), key=lambda t: score[t])
                remap = {old: new for new, old in enumerate(order)}
                idx = {k: remap[v] for k, v in idx.items()}
            tracks[ch] = (sp, idx, n)

        # conflicts: NMOS riser (up to track tn) vs PMOS riser (down to track tp), |dx|<PITCH
        mid = tracks["mid"][1]
        pnames = {p[0] for p in PMOS}
        nr = [(x, net, mid[net]) for net, x, _y, c, t in terms
              if c == "mid" and t.split(".")[0] not in pnames]
        pr = [(x, net, mid[net]) for net, x, _y, c, t in terms
              if c == "mid" and t.split(".")[0] in pnames]
        nr.append((x_dnw, "VDD", mid["VDD"]))             # DNW tie up to the VDD track
        pr.append((x_ntap, "VDD", mid["VDD"]))            # n-tap ring down to the VDD track
        nr.append((x_vss, "VSS", mid["VSS"]))
        bad = [(a, b) for a in nr for b in pr
               if a[1] != b[1] and abs(a[0] - b[0]) < PITCH and a[2] >= b[2]]
        return len(bad), dict(terms=terms, chans_of=chans_of, cross=cross, col_x=col_x,
                              x_sp=x_sp, cap_x=cap_x, x_ntap=x_ntap, tracks=tracks, bad=bad)

    best = None
    for k in sorted(range(-80, 81), key=abs):
        nbad, p = plan(k * 0.05)
        if best is None or nbad < best[0]:
            best = (nbad, k * 0.05, p)
        if nbad == 0:
            break
    nbad, sh, P = best
    if nbad:
        raise RuntimeError(f"{nbad} riser conflicts remain at best shift {sh:+.2f}: {P['bad'][:4]}")
    for o in pmos_objs:
        o.movex(sh)
    terms, chans_of, cross, col_x = P["terms"], P["chans_of"], P["cross"], P["col_x"]
    x_sp, cap_x, tracks, x_ntap = P["x_sp"], P["cap_x"], P["tracks"], P["x_ntap"]

    y_mid0 = g.ref.ymax + CH_MARGIN
    n_mid = tracks["mid"][2]
    p_bottom = y_mid0 + (n_mid - 1) * PITCH + CH_MARGIN
    dy = p_bottom - ng.ref.ymin
    for o in pmos_objs:
        o.movey(dy)
    y0 = {"mid": y_mid0,
          "bot": g.ref.ymin - CH_MARGIN - (tracks["bot"][2] - 1) * PITCH,
          "top": ng.ref.ymax + CH_MARGIN}
    track_y = {(ch, net): y0[ch] + i * PITCH
               for ch, (sp, idx, n) in tracks.items() for net, i in idx.items()}

    # ------------------------------------------------------------------ draw tracks
    for ch, (sp, idx, n) in tracks.items():
        for net, (lo, hi) in sp.items():
            y = track_y[(ch, net)]
            R.wire("met4", (lo, y), (hi, y), net, tag=f"trk-{ch}")

    # ------------------------------------------------------------------ risers (re-read PMOS after move)
    terms = risers(nref, NMOS) + risers(pref, PMOS)
    for net, x, yb, ch, tag in terms:
        yt = track_y[(ch, net)]
        R.via(x, yb, "met2", "met3", net, tag)
        R.via(x, yt, "met3", "met4", net, tag)
        R.wire("met3", (x, yb), (x, yt), net, tag=tag)

    # device met2 buses: recorded (not drawn) so the parasitic predictor sees them
    for name, kind, w, l, d, gt, s_ in NMOS + PMOS:
        r = nref.get(name) or pref[name]
        for term, net in (("drain", d), ("gate", gt), ("source", s_)):
            x0, x1, y = bus(r, term)
            R.record("met2", x0 - WIRE / 2, y - WIRE / 2, x1 + WIRE / 2, y + WIRE / 2, net, "bus")

    # ------------------------------------------------------------------ cross-channel columns
    for net, x in col_x.items():
        ys = [track_y[(ch, net)] for ch in chans_of[net]]
        for y in ys:
            R.via(x, y, "met3", "met4", net, "col")
        R.wire("met3", (x, min(ys)), (x, max(ys)), net, tag="col")

    # ------------------------------------------------------------------ supply columns
    yb_body = ring_y(g.ports["body_N_top_met_N"])
    yb_sub = ring_y(g.ports["sub_N_top_met_S"])
    y_vss = track_y[("mid", "VSS")]
    for y in (yb_body, yb_sub):
        R.via(x_vss, y, "met2", "met3", "VSS", "vss-col")
    R.via(x_vss, y_vss, "met3", "met4", "VSS", "vss-col")
    R.wire("met3", (x_vss, yb_body), (x_vss, y_vss), "VSS", tag="vss-col")

    yb_dnw = ring_y(g.ports["dnw_N_top_met_N"])
    yb_ntap = ring_y(ng.ports["body_S_top_met_S"])
    y_vdd = track_y[("mid", "VDD")]
    for x, yr, tag in ((x_dnw, yb_dnw, "dnw-col"), (x_ntap, yb_ntap, "ntap-col")):
        R.via(x, yr, "met2", "met3", "VDD", tag)
        R.via(x, y_vdd, "met3", "met4", "VDD", tag)
        R.wire("met3", (x, yr), (x, y_vdd), "VDD", tag=tag)

    # ------------------------------------------------------------------ caps
    y_c1 = ng.ref.ymin                     # C1 above the mid channel, C2 below it
    caps = {}
    for name, net, size in CAPS:
        # no extension tab: glayout lifts the bottom plate to met5 on the tab, which the
        # met5 top-plate links would cross. The spine touches the met4 bottom plate instead.
        c = top << mimcap(pdk, (size, size), with_extension=False)
        if name == "C1":
            c.move((x_sp + CAP_GAP - c.xmin, y_c1 - c.ymin))
        else:
            c.move((x_sp + CAP_GAP - c.xmin, y_mid0 - 1.2 - c.ymax))
        caps[name] = c
        # record plates for the checker: met5 top contact = net, met4 bottom plate = VSS
        cx_, cy_, h5 = c.center[0], c.center[1], size / 2 - 0.28
        R.shapes["met5"].append((cx_ - h5, cy_ - h5, cx_ + h5, cy_ + h5, net, name))
        R.shapes["met4"].append((c.xmin, c.ymin, c.xmax, c.ymax, "VSS", name))
    # VSS spine (met4) from C2's bottom-plate tab to C1's, through the VSS track end
    ys = [caps["C1"].center[1], caps["C2"].center[1], y_vss]
    R.wire("met4", (x_sp, min(ys)), (x_sp, max(ys)), "VSS", tag="spine")
    for name in ("C1", "C2"):
        c = caps[name]
        R.wire("met4", (x_sp, c.center[1]), (c.xmin + 0.3, c.center[1]), "VSS", tag=name)
    # met5 links: track end -> up/down -> into the cap's top plate
    for name, net, _ in CAPS:
        c, x, y = caps[name], cap_x[net], track_y[("mid", net)]
        R.via(x, y, "met4", "met5", net, "cap")
        yc = c.center[1]
        R.wire("met5", (x, y), (x, yc), net, w=1.0, tag="cap")
        R.wire("met5", (x, yc), (c.center[0], yc), net, w=1.0, tag=name)

    # ------------------------------------------------------------------ pins
    lab = pdk.get_glayer("met4_label")
    for (ch, net), y in track_y.items():
        if net in PINS and net not in ("VSS", "VDD"):
            lo = tracks[ch][0][net][0]
            top.add_label(text=net, position=(lo + 0.1, y), layer=lab)
    # supply labels on the ring metal itself (a label on the polygon edge may not attach)
    for net, port in (("VSS", g.ports["sub_S_top_met_S"]), ("VDD", ng.ports["body_N_top_met_N"])):
        top.add_label(text=net, position=(port.center[0], ring_y(port)),
                      layer=pdk.get_glayer("met2_label"))

    # ------------------------------------------------------------------ LVS reference
    lines = []
    for name, kind, w, l, d, gt, s in NMOS + PMOS:
        b, model = ("VSS", "nfet_03v3") if kind == "n" else ("VDD", "pfet_03v3")
        lines.append(f"X{name} {d} {gt} {s} {b} {model} L={l:g}u W={w:g}u nf=1")
    for name, net, size in CAPS:
        lines.append(f"X{name} {net} VSS cap_mim_2f0fF c_width={size:g}e-6 c_length={size:g}e-6 m=1")
    lines += dn.spice + dp.spice
    summary = (f"tracks bot/mid/top = {tracks['bot'][2]}/{n_mid}/{tracks['top'][2]}, "
               f"cross-channel columns = {len(cross)}")
    return top, R, lines, summary


if __name__ == "__main__":
    top, R, lines, summary = neuron()
    print(summary)
    errs = R.check()
    print("router check:", errs or "clean")
    flat = top.flatten()
    flat.name = "neuron_glayout"
    w, h = flat.xsize, flat.ysize
    print(f"cell {w:.2f} x {h:.2f} um")
    flat.write_gds(str(HERE / "neuron_glayout.gds"))
    # predictions (seconds): DRC subset on the GDS, parasitic C per net from the router shapes
    from glayout_predrc import predrc
    from glayout_parasitics import predict_caps, report, inject_caps
    print(predrc(str(HERE / "neuron_glayout.gds")))
    caps = predict_caps(R.shapes)
    print("predicted parasitic C (calibrated):")
    print(report(caps, nets=["VMEM", "spike", "net1", "net2", "amp_n2"]))
    with open(HERE / "neuron_glayout_lvs_ref.spice", "w") as f:
        f.write("* LVS reference for neuron_glayout.gds (generated by gen_neuron_glayout.py)\n"
                "* neuron_sized.sch, spike amp flattened as A1..A5, W<0.5 devices scaled\n"
                "* (W/L kept), amp M2 gate = VT, MIM caps as cap_mim_2f0fF, + dummy rings\n")
        f.write(".subckt neuron_glayout " + " ".join(PINS) + "\n")
        f.write("\n".join(lines) + "\n.ends\n")
    # same reference + predicted lumped C: drop-in for a fast "predicted post-layout" sim
    n = inject_caps(HERE / "neuron_glayout_lvs_ref.spice", HERE / "neuron_glayout_pred.spice",
                    caps, subckt="neuron_glayout")
    print(f"wrote neuron_glayout_pred.spice ({n} predicted caps; cap_mim_2f0fF is the LVS name,"
          f" use cap_mim_2f0_m4m5_noshield for simulation)")
    if "--show" in sys.argv:
        flat.show()
