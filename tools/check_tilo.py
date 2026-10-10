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

# ---- (a) numeric: shipped mouths vs the ORIGINAL speaking art (measured independently from pose_speaking_raw, scaled to 2x = 512/768) ----
from scipy import ndimage as ndi
SC = 512 / 768; CROP = (186, 116)
raw = np.array(Image.open(f"{R}/design/character/tilo-cute/pose_speaking_raw.png").convert("RGB")).astype(float)
d = np.abs(raw - (195, 127, 77)).max(2); sub = np.zeros_like(d, bool); sub[372:460, 470:556] = True      # below the nostrils, inside the muzzle
orig = (d > 14) & sub
def bbox(m):
    ys, xs = np.where(m); return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
def open_part(m):
    sw = int(m[m.any(1)][6].sum()); o = ndi.binary_opening(m, iterations=sw // 2 + 2); return o if o.any() else m
ob = bbox(open_part(orig)); orig_open = ((ob[2] - ob[0]) * SC, (ob[3] - ob[1]) * SC, ((ob[0] + ob[2]) / 2 - CROP[0]) * SC, ((ob[1] + ob[3]) / 2 - CROP[1]) * SC)
print(f"\noriginal open mouth @2x: w {orig_open[0]:.1f} h {orig_open[1]:.1f} centre ({orig_open[2]:.1f},{orig_open[3]:.1f})")
pa = []
for n, v in m["talk"]["mouths"].items():
    mo = np.array(Image.open(f"{D}/{v['files']['2x']}").convert("RGBA"))[:, :, 3] > 128; ox, oy = v["offset"]["2x"]
    part = open_part(mo); b = bbox(part); w, h = b[2] - b[0], b[3] - b[1]; cx, cy = ox + (b[0] + b[2]) / 2, oy + (b[1] + b[3]) / 2
    full = bbox(mo)
    if n == "mmm": ref_w = (full[2] - full[0]); print(f"{n}: closed smile w {full[2]-full[0]} (+ philtrum) centre x {ox + (full[0]+full[2])/2:.1f} (orig centre x {orig_open[2]:.1f}, dx {ox + (full[0]+full[2])/2 - orig_open[2]:+.1f})"); continue
    rw, rh = w / orig_open[0], h / orig_open[1]
    print(f"{n}: open w {w} h {h}  ratio w {rw:.2f} h {rh:.2f}  centre ({cx:.1f},{cy:.1f}) dx {cx-orig_open[2]:+.1f} dy {cy-orig_open[3]:+.1f}")
    if n in ("mid", "aaa"): pa.append(abs(1 - rh) <= .15 and abs(cx - orig_open[2]) <= 2 and abs(cy - orig_open[3]) <= 2 or n == "aaa" and abs(cx - orig_open[2]) <= 2)
print("NUMERIC OK (mid within +-15%, aaa height <= +15%)" if all(pa) else "NUMERIC CHECK FAILED")
