#!/usr/bin/env python3
"""Alignment + edge check for the shipped Tilo webp files (reads tilo.json, composites body+mouth at both sizes)."""
import json, os, itertools
import numpy as np
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{R}/app/public"
m = json.load(open(f"{D}/img/tilo/tilo.json")); ok = True
for k in m["sizes"]:
    body = Image.open(f"{D}/{m['talk']['body'][k]}").convert("RGBA"); frames = {}
    boxes = []
    for n, v in m["talk"]["mouths"].items():
        mo = Image.open(f"{D}/{v['files'][k]}").convert("RGBA"); ox, oy = v["offset"][k]
        fr = body.copy(); fr.alpha_composite(mo, (ox, oy)); frames[n] = np.array(fr).astype(int); boxes.append((ox, oy, ox + mo.width, oy + mo.height))
    bx = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    worst = 0
    for a, b in itertools.combinations(frames, 2):
        d = np.abs(frames[a] - frames[b]).max(2) > 0
        ys, xs = np.where(d); inside = d[bx[1]:bx[3], bx[0]:bx[2]].sum(); outside = d.sum() - inside; worst = max(worst, outside)
        print(f"{k} {a}-{b}: changed px {d.sum()}, outside mouth box {outside}")
    ok &= worst == 0; print(k, "canvas", body.size, "mouth box", bx)
print("ALIGNED" if ok else "MISALIGNED")
