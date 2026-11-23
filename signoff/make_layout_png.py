#!/usr/bin/env python3
"""Render gds/snn_top.gds as signoff/img/snn_top_layout.png (plain) and
signoff/img/snn_top_floorplan.png (with the blocks labelled).

    python3 signoff/make_layout_png.py

KLayout draws the layout with the PDK's layer colours; marker and boundary layers that cover
the whole macro (0/0, 63/0 and the ISOSUB marker 23/5) are hidden so the devices stay visible.
The block outlines come from the GDS itself (the placed analog cells UY_* and the standard
cells), so they follow the layout after a rebuild.
"""
import os
import re
from collections import defaultdict

import klayout.db as db
import klayout.lay as lay
import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.patches as patches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GDS = os.path.join(ROOT, "gds", "snn_top.gds")
LYP = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "gf180mcuD"),
                   "libs.tech", "klayout", "tech", "gf180mcu.lyp")
OUT = os.path.join(ROOT, "signoff", "img")
HIDE = {(0, 0), (63, 0), (23, 5)}
PX_PER_UM = 2.0
MARGIN = 12.0   # um around the die

# label, colour, cell name
BLOCKS = [
    ("DAC, one per synapse (8): weight → current", "#1f5fa8", "UY_DAC"),
    ("DPI filter, excitatory, one per neuron (5)", "#2e8b57", "UY_DPI"),
    ("DPI filter, inhibitory, hidden + output (3)", "#c0392b", "UY_DPI_inh"),
    ("neuron, leaky integrate-and-fire (5)", "#7c4dbd", "UY_neuron"),
    ("bias generator", "#d9822b", "UY_bias"),
]


def block_boxes(layout):
    """{cell name: [DBox in top coordinates]} for the analog cells, the box around the logic
    standard cells, and the die box."""
    top = layout.top_cell()
    boxes = defaultdict(list)
    it = top.begin_instances_rec()
    while not it.at_end():
        c = layout.cell(it.inst_cell().cell_index())
        if c.name.startswith("UY_") or c.name == "snn_analog" or c.name.startswith("gf180mcu_fd_sc"):
            boxes[c.name].append(c.dbbox().transformed(it.dtrans() * it.inst_dtrans()))
        it.next()
    std, n_std = db.DBox(), 0   # logic cells only: fillers and end caps also line the die edges
    for name, bs in boxes.items():
        if name.startswith("gf180mcu_fd_sc") and not re.search(r"__(fill|endcap|antenna)", name):
            for b in bs:
                std += b
            n_std += len(bs)
    return boxes, (std, n_std), top.dbbox()


def render(die, path):
    v = lay.LayoutView()
    v.load_layout(GDS)
    v.load_layer_props(LYP)
    v.max_hier()
    it = v.begin_layers()
    while not it.at_end():
        p = it.current()
        if (p.source_layer, p.source_datatype) in HIDE:
            p.visible = False
            v.set_layer_properties(it, p)
        it.next()
    for k, val in (("background-color", "#ffffff"), ("grid-visible", "false"), ("text-visible", "false")):
        v.set_config(k, val)
    view = die.enlarged(MARGIN, MARGIN)
    v.zoom_box(view)
    v.save_image(path, int(view.width() * PX_PER_UM), int(view.height() * PX_PER_UM))
    return view


def main():
    os.makedirs(OUT, exist_ok=True)
    layout = db.Layout()
    layout.read(GDS)
    boxes, (std, n_std), die = block_boxes(layout)
    plain = os.path.join(OUT, "snn_top_layout.png")
    view = render(die, plain)
    print("wrote", plain)

    img = mpimg.imread(plain)
    fig, ax = plt.subplots(figsize=(11, 11 * view.height() / (view.width() + 330)))
    ax.imshow(img, extent=(view.left, view.right, view.bottom, view.top), alpha=0.55)
    ax.set_xlim(view.left, view.right + 330)
    ax.set_ylim(view.bottom, view.top)
    ax.set_aspect("equal")
    ax.axis("off")

    def outline(b, color, lw=2.0, ls="-"):
        ax.add_patch(patches.Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False,
                                       ec=color, lw=lw, ls=ls))

    legend = []
    outline(die, "#333333", 1.5)
    if "snn_analog" in boxes:
        outline(boxes["snn_analog"][0], "#555555", 1.5, "--")
        legend.append(("analog macro snn_analog (SNN_signed)", "#555555", "--"))
    outline(std, "#b8860b", 2.5)
    legend.append((f"digital: regs + pulse_gen ({n_std} standard cells)", "#b8860b", "-"))
    for label, color, cell in BLOCKS:
        for b in boxes.get(cell, []):
            outline(b, color)
        legend.append((label, color, "-"))

    # legend to the right of the die
    x0, y = view.right + 20, view.top - 40
    ax.text(x0, y, "snn_top  ·  GF180MCU  ·  640 × 910 µm", fontsize=12, weight="bold", va="top")
    y -= 55
    for label, color, ls in legend:
        ax.add_patch(patches.Rectangle((x0, y - 14), 34, 22, fill=False, ec=color, lw=2.2, ls=ls))
        ax.text(x0 + 48, y - 3, label, fontsize=10, va="center")
        y -= 45
    y -= 20
    notes = ["Network: 2 inputs → 2 hidden → 1 output,",
             "8 signed synapses (4-bit magnitude + sign).",
             "",
             "Separate supplies: VDDA / VSSA (analog),",
             "VDDD / VSSD (digital); ISOSUB marker",
             "(23/5, hidden here) over the macro keeps",
             "them apart in extraction / LVS."]
    for line in notes:
        ax.text(x0, y, line, fontsize=9.5, color="#444444", va="top")
        y -= 26
    path = os.path.join(OUT, "snn_top_floorplan.png")
    fig.savefig(path, dpi=140, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    print("wrote", path)


if __name__ == "__main__":
    main()
