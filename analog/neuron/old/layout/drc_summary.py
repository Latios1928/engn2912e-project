import pya, glob, sys
d = sys.argv[-1] if len(sys.argv) > 1 else "drc"
import os
d = os.environ.get("RDBDIR", "drc")
for f in sorted(glob.glob(d + "/*.lyrdb")):
    db = pya.ReportDatabase("")
    try: db.load(f)
    except Exception as e: continue
    for cat in db.each_category():
        if cat.num_items() == 0: continue
        print(os.path.basename(f), "|", cat.name(), "|", cat.description[:110], "| n =", cat.num_items())
        for it in db.each_item_per_category(cat.rdb_id()):
            for v in it.each_value():
                print("     ", str(v)[:160])
            break_ = None
