#!/usr/bin/env python3
"""Tilo (cute, approved) raw art -> app/public/img/tilo/*.webp (1x=256px, 2x=512px tall) + tilo.json.

  python3 tools/pack_tilo.py

Poses share one crop box so Tilo never jumps between states. The speaking body is repainted WITHOUT a mouth and the
mouths are drawn as overlays at integer offsets, so a lip-flap changes only the mouth region (checked by check_tilo.py).
Scales are exactly 2/3 (512 tall) and 1/3 (256 tall) of a 768 px crop, and the mouth box is a multiple of 3, so overlay
offsets land on whole pixels at both sizes."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{R}/tools")
from tilo_cutout import cutout
SRC = f"{R}/design/character/tilo-cute"; DST = f"{R}/app/public/img/tilo"; os.makedirs(DST, exist_ok=True)
CROP = (186, 116, 861, 884)                 # x0, y0, x1, y1 in the 1024 raw: w 675, h 768
MOUTH = (480, 360, 546, 459)                # overlay box in the 1024 raw (multiples of 3)
POSES = {"idle": "waiting", "speaking": "speaking", "listening": "listening", "pointing": "pointing", "thinking": "thinking", "encouraging": "trying", "celebrating": "celebrating"}
FACES = {"happy": "happy", "proud": "proud", "listening": "listening", "thinking": "thinking", "encouraging": "encouraging", "mmm": "mmm", "aaa": "aaa", "ooo": "ooo"}
SIZES = {"1x": 256, "2x": 512}
manifest = {"version": 1, "sizes": {k: v for k, v in SIZES.items()}, "poses": {}, "faces": {}, "talk": {}}
total = 0


def save(im, name, q=86):
    global total
    p = f"{DST}/{name}.webp"; im.save(p, quality=q, method=6, alpha_quality=92); total += os.path.getsize(p); return f"img/tilo/{name}.webp"


def scaled(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def premult_resize(im, size):
    """Resize without dark/white fringes: premultiply alpha, resize, un-premultiply."""
    a = np.array(im).astype(np.float32); al = a[:, :, 3:4] / 255
    pm = Image.fromarray(np.dstack([a[:, :, :3] * al, a[:, :, 3:4]]).astype(np.uint8), "RGBA")
    r = np.array(pm.resize(size, Image.LANCZOS)).astype(np.float32); ra = r[:, :, 3:4] / 255
    rgb = np.where(ra > 0.003, r[:, :, :3] / np.maximum(ra, 0.003), 0)
    return Image.fromarray(np.dstack([rgb, r[:, :, 3:4]]).clip(0, 255).astype(np.uint8), "RGBA")


def sized(arr):
    im = Image.fromarray(arr, "RGBA").crop(CROP)
    return {k: premult_resize(im, (round(im.width * h / 768), h)) for k, h in SIZES.items()}


# ---- poses (shared crop) ----
cuts = {s: cutout(f"{SRC}/pose_{f}_raw.png") for s, f in POSES.items()}
for s, arr in cuts.items():
    files = {}
    base = arr
    if s == "speaking":                     # mouthless body for the lip-flap; keep original as the 'mid' overlay
        orig = arr.copy(); base = arr.copy(); x0, y0, x1, y1 = MOUTH
        # flat muzzle colour per row, sampled left and right of the mouth, so the muzzle shading is kept
        for y in range(y0, y1):
            l = base[y, x0 - 6:x0 - 2, :3].mean(0); r = base[y, x1 + 2:x1 + 6, :3].mean(0)
            for x in range(x0, x1): t = (x - x0) / (x1 - x0); base[y, x, :3] = (l * (1 - t) + r * t)
        speaking_base = base
    for k, im in sized(base).items(): files[k] = save(im, f"{s}_{k}")
    manifest["poses"][s] = files
# ---- mouths: drawn at 4x then reduced to 1024-scale, in the same box ----
x0, y0, x1, y1 = MOUTH; bw, bh = x1 - x0, y1 - y0; SS = 4
LINE, DARK, TONGUE, RIM = (112, 56, 32), (122, 50, 44), (243, 133, 126), (143, 66, 48)
def canvas(): return Image.new("RGBA", (bw * SS, bh * SS), (0, 0, 0, 0))
def P(x, y): return ((x - x0) * SS, (y - y0) * SS)
def philtrum(d, y_end):
    d.rounded_rectangle((*P(508.5, 372), *P(516, y_end)), radius=3 * SS, fill=LINE + (255,))
def arc(d, cx, y, w, depth, width):
    pts = [P(cx + (i / 20 - .5) * w, y + depth * (1 - (2 * (i / 20) - 1) ** 2) ) for i in range(21)]
    d.line(pts, fill=LINE + (255,), width=width * SS, joint="curve")
    for p in (pts[0], pts[-1]): d.ellipse((p[0] - width * SS / 2, p[1] - width * SS / 2, p[0] + width * SS / 2, p[1] + width * SS / 2), fill=LINE + (255,))
mouths = {}
m = canvas(); d = ImageDraw.Draw(m); philtrum(d, 398)    # mmm: closed smile
arc(d, 512, 392, 50, 14, 6); mouths["mmm"] = m
m = canvas(); d = ImageDraw.Draw(m); philtrum(d, 394)    # aaa: wide open
d.ellipse((*P(486, 394), *P(538, 454)), fill=RIM + (255,)); d.ellipse((*P(491, 399), *P(533, 449)), fill=DARK + (255,))
d.ellipse((*P(497, 428), *P(527, 447)), fill=TONGUE + (255,)); mouths["aaa"] = m
m = canvas(); d = ImageDraw.Draw(m); philtrum(d, 402)    # ooo: small round
d.ellipse((*P(500, 402), *P(524, 432)), fill=RIM + (255,)); d.ellipse((*P(504, 406), *P(520, 428)), fill=DARK + (255,))
d.ellipse((*P(507, 418), *P(517, 426)), fill=TONGUE + (200,)); mouths["ooo"] = m
mouths = {k: v.resize((bw, bh), Image.LANCZOS) for k, v in mouths.items()}
# mid: the artist's own half-open mouth, lifted from the original speaking pixels (alpha = where it differs from the flat fill)
o = cuts["speaking"][y0:y1, x0:x1].astype(np.float32); f = speaking_base[y0:y1, x0:x1].astype(np.float32)
diff = np.abs(o[:, :, :3] - f[:, :, :3]).max(2) > 14
diff = ndi.binary_closing(ndi.binary_dilation(diff, iterations=2), iterations=2)
al = ndi.gaussian_filter(diff.astype(np.float32), 1.0)
mouths["mid"] = Image.fromarray(np.dstack([o[:, :, :3], al * 255]).clip(0, 255).astype(np.uint8), "RGBA")
# ---- write talk set: body + overlays at both sizes, offsets in output pixels ----

cx0, cy0 = CROP[0], CROP[1]
manifest["talk"] = {"body": manifest["poses"]["speaking"], "mouths": {}, "order": ["mmm", "mid", "aaa", "ooo"]}
for name, mo in mouths.items():
    files, offs = {}, {}
    for k, h in SIZES.items():
        sc = h / 768
        ov = premult_resize(np.array(mo) if False else mo, (round(bw * sc), round(bh * sc)))
        files[k] = save(ov, f"mouth_{name}_{k}", 90); offs[k] = [round((x0 - cx0) * sc), round((y0 - cy0) * sc)]
    manifest["talk"]["mouths"][name] = {"files": files, "offset": offs}
# ---- faces (own union crop, square-ish) ----
fc = {s: cutout(f"{SRC}/face_{f}_raw.png") for s, f in FACES.items()}
bb = [np.where(a[:, :, 3] > 8) for a in fc.values()]
fx0 = min(b[1].min() for b in bb) - 4; fx1 = max(b[1].max() for b in bb) + 4; fy0 = min(b[0].min() for b in bb) - 4; fy1 = max(b[0].max() for b in bb) + 4
for s, a in fc.items():
    im = Image.fromarray(a, "RGBA").crop((fx0, fy0, fx1, fy1)); files = {}
    for k, h in SIZES.items(): files[k] = save(premult_resize(im, (round(im.width * h / im.height), h)), f"face_{s}_{k}")
    manifest["faces"][s] = files
manifest["note"] = "Per-state files are keyed by size; draw talk.body then overlay talk.mouths[name] at offset[size] (css px = file px / (size 1x:1, 2x:2))."
json.dump(manifest, open(f"{DST}/tilo.json", "w"), indent=1)
print("tilo images:", len(os.listdir(DST)) - 1, "files,", total // 1024, "KB")
