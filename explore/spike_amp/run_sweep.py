import sys, json, itertools
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import amp_char as amp
res = []
for i, (wp, lp, wm, lm) in enumerate(itertools.product([0.5, 1, 2, 4, 8], [0.5, 1, 2, 4], [0.5, 1, 2, 4], [1, 2, 4, 8])):
    try:
        r = amp.characterize((wp, lp, wm, lm), n_mc=40, tag="s%d" % i)
    except Exception as e:
        r = {"size": [wp, lp, wm, lm], "error": str(e)}
    res.append(r)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "spike_amp_sweep.json"), "w"))
print(len(res))
