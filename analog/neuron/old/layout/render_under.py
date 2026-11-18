import pya
GDS = globals().get("gds", "DPI.gds"); PNG = globals().get("png", "DPI_under_cap.png")
lv = pya.LayoutView()
lv.load_layout(GDS, False)
lv.load_layer_props("/foss/pdks/gf180mcuD/libs.tech/klayout/tech/gf180mcu.lyp")
lv.max_hier()
hide = {(46, 0), (81, 0), (41, 0), (40, 0), (75, 0), (117, 5), (117, 10), (38, 0), (42, 0), (0, 0)}
it = lv.begin_layers()
while not it.at_end():
    lp = it.current()
    if (lp.source_layer, lp.source_datatype) in hide:
        lp.visible = False
        lv.set_layer_properties(it, lp)
    it.next()
lv.set_config("background-color", "#ffffff")
lv.set_config("grid-visible", "false")
lv.set_config("default-text-size", "0.8")
ly = lv.cellview(0).layout()
lv.zoom_box(ly.top_cell().dbbox().enlarged(0.5, 0.5))
lv.save_image(PNG, 1400, 1300)
print("wrote", PNG)
