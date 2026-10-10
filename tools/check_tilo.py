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
# Mouths are deliberately 1.5x the original (Kamal + critic: too small on a phone); aaa is capped by the muzzle height.
from scipy import ndimage as ndi
SC = 512 / 768; CROP = (186, 116); DISP = 200 / 512          # 2x px -> 200 px-tall display
raw = np.array(Image.open(f"{R}/design/character/tilo-cute/pose_speaking_raw.png").convert("RGB")).astype(float)
d = np.abs(raw - (195, 127, 77)).max(2); sub = np.zeros_like(d, bool); sub[372:460, 470:556] = True
orig = (d > 14) & sub
def bbox(m):
    ys, xs = np.where(m); return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
def open_part(m):
    sw = int(m[m.any(1)][6].sum()); o = ndi.binary_opening(m, iterations=sw // 2 + 2); return o if o.any() else m
ob = bbox(open_part(orig)); OW, OH = (ob[2] - ob[0]) * SC, (ob[3] - ob[1]) * SC
OX, OY = ((ob[0] + ob[2]) / 2 - CROP[0]) * SC, ((ob[1] + ob[3]) / 2 - CROP[1]) * SC
print(f"\noriginal open mouth @2x: w {OW:.1f} h {OH:.1f} centre ({OX:.1f},{OY:.1f})   @200px-tall: w {OW*DISP:.1f} h {OH*DISP:.1f}")
mz = np.array(Image.open(f"{R}/design/character/tilo-cute/pose_speaking_raw.png").convert("RGB")).astype(float); mzm = np.abs(mz - (195, 127, 77)).max(2) < 14
lab, k = ndi.label(ndi.binary_opening(mzm, iterations=2)); big = max(range(1, k + 1), key=lambda i: (lab == i).sum()); MY = np.where(ndi.binary_fill_holes(lab == big))[0]
muz_bottom = (MY.max() + 1 - CROP[1]) * SC; nose_end = None
ok_all = True
for n, v in m["talk"]["mouths"].items():
    mo = np.array(Image.open(f"{D}/{v['files']['2x']}").convert("RGBA"))[:, :, 3] > 128; ox, oy = v["offset"]["2x"]
    full = bbox(mo); fw, fh = full[2] - full[0], full[3] - full[1]; top, bot = oy + full[1], oy + full[3]
    part = open_part(mo); b = bbox(part); w, h = b[2] - b[0], b[3] - b[1]; cx, cy = ox + (b[0] + b[2]) / 2, oy + (b[1] + b[3]) / 2
    inside = bot <= muz_bottom - 2; ok_all &= inside and top >= (362 - CROP[1]) * SC + 1
    print(f"{n}: @2x open/line w {w} h {h} (x{w/OW:.2f} / x{h/OH:.2f} of original)  centre ({cx:.1f},{cy:.1f}) dx {cx-OX:+.1f} dy {cy-OY:+.1f}  | whole overlay w {fw} h {fh}, top {top:.0f} bottom {bot:.0f} (muzzle bottom {muz_bottom:.0f})")
    print(f"     @200px-tall: open/line {w*DISP:.1f} x {h*DISP:.1f}, whole {fw*DISP:.1f} x {fh*DISP:.1f}")
    if n == "mid": ok_all &= abs(w / OW - 1.5) <= .15 * 1.5 and abs(h / OH - 1.5) <= .15 * 1.5 and abs(cx - OX) <= 2 and abs(cy - OY) <= 3
print("NUMERIC OK (mid 1.5x +-15%, centre within 2/3 px, all bottoms inside muzzle, nothing above the nostrils)" if ok_all else "NUMERIC CHECK FAILED")
