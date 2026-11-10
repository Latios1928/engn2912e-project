"""
Read DPI.gds and report each pin: label, layer, and the access box where the pin
net meets the cell boundary. Also renders a PNG of the layout.

    klayout -b -r extract_pins.py -rd gds=DPI.gds -rd jout=DPI_pins.json -rd png=DPI.png
"""
import json
import pya

GDS = globals().get("gds", "DPI.gds")
JSON = globals().get("jout", "DPI_pins.json")
PNG = globals().get("png", "")

ly = pya.Layout()
ly.read(GDS)
top = ly.top_cell()
dbu = ly.dbu
bbox = top.dbbox()

LAYERS = {(34, 10): ("Metal1", (34, 0)), (36, 10): ("Metal2", (36, 0)),
          (42, 10): ("Metal3", (42, 0)), (81, 10): ("Metal5", (81, 0))}
EDGE = 0.6   # depth of the boundary strip used to find edge access boxes

cell_box = pya.Box(top.bbox())
strip = pya.Region(cell_box) - pya.Region(cell_box.enlarged(-int(EDGE / dbu), -int(EDGE / dbu)))

pins = []
for (lbl_l, lbl_d), (lname, (ml, md)) in LAYERS.items():
    li_lbl = ly.find_layer(lbl_l, lbl_d)
    li_met = ly.find_layer(ml, md)
    if li_lbl is None or li_met is None:
        continue
    metal = pya.Region(top.begin_shapes_rec(li_met)).merged()
    for sh in top.shapes(li_lbl).each():
        if not sh.is_text():
            continue
        t = sh.text
        pt = pya.Point(t.x, t.y)
        net = metal.interacting(pya.Region(pya.Box(pt, pt).enlarged(1, 1)))
        access = (net & strip).merged()
        boxes = [p.bbox().to_dtype(dbu) for p in access.each()]
        side = None
        out = []
        for b in boxes:
            if b.left <= 0.001:
                side = "left"
            elif b.right >= bbox.right - 0.001:
                side = "right"
            elif b.bottom <= 0.001:
                side = "bottom"
            elif b.top >= bbox.top - 0.001:
                side = "top"
            else:
                side = "inside"
            out.append({"side": side, "x1": round(b.left, 3), "y1": round(b.bottom, 3),
                        "x2": round(b.right, 3), "y2": round(b.top, 3),
                        "cx": round(b.center().x, 3), "cy": round(b.center().y, 3)})
        pins.append({"name": t.string, "layer": lname,
                     "label_x": round(t.x * dbu, 3), "label_y": round(t.y * dbu, 3),
                     "access": out})

pins.sort(key=lambda p: p["name"])
data = {"cell": top.name, "units": "um", "origin": "lower-left of PR boundary",
        "bbox": [bbox.left, bbox.bottom, bbox.right, bbox.top], "pins": pins}
with open(JSON, "w") as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))

if PNG:
    lv = pya.LayoutView()
    lv.load_layout(GDS, False)
    lv.load_layer_props("/foss/pdks/gf180mcuD/libs.tech/klayout/tech/gf180mcu.lyp")
    lv.max_hier()
    lv.set_config("background-color", "#ffffff")
    lv.set_config("grid-visible", "false")
    lv.set_config("text-visible", "true")
    lv.set_config("default-text-size", "1.2")
    lv.zoom_box(bbox.enlarged(1.0, 1.0))
    lv.save_image(PNG, 1400, 1300)
    print("wrote", PNG)
