#!/usr/bin/env python3
"""Tilo (cute, approved) raw art -> app/public/img/tilo/*.webp (1x=256px, 2x=512px tall) + tilo.json.

  python3 tools/pack_tilo.py

Poses share one crop box so Tilo never jumps between states. The speaking body is repainted WITHOUT a mouth and the
mouths are drawn as overlays at integer offsets, so a lip-flap changes only the mouth region (checked by check_tilo.py).
Scales are exactly 2/3 (512 tall) and 1/3 (256 tall) of a 768 px crop, and the mouth box is a multiple of 3, so overlay
offsets land on whole pixels at both sizes.

The mouths are NOT hand-drawn: every one is cut from the real art (pose_speaking_raw for 'mid', face_{mmm,aaa,ooo}_raw for
the rest). The face crops are at a different scale, so each is registered to the speaking pose by the muzzle width (a flat
rounded rectangle, same colour in every image) and by the philtrum top; line weight, colour and shading are the artist's."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{R}/tools")
from tilo_cutout import cutout
SRC = f"{R}/design/character/tilo-cute"; DST = f"{R}/app/public/img/tilo"; os.makedirs(DST, exist_ok=True)
CROP = (186, 116, 861, 884)                 # x0, y0, x1, y1 in the 1024 raw: w 675, h 768
MUZ = (195, 127, 77)                        # flat muzzle colour in every raw
PAD = 12                                    # clear space around the union of all mouths (1024 px)
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
    if s == "speaking": speaking_cut = arr
    if s == "speaking": continue            # written below, once the mouth box is known
    for k, im in sized(base).items(): files[k] = save(im, f"{s}_{k}")
    manifest["poses"][s] = files
# ---- mouths: cut from the real art, registered by muzzle width + philtrum top ----
def analyse(path):
    rgb = np.array(Image.open(path).convert("RGB")).astype(np.float32)
    d = np.abs(rgb - MUZ).max(2)
    lab, k = ndi.label(ndi.binary_opening(d < 14, iterations=2))
    big = max(range(1, k + 1), key=lambda i: (lab == i).sum())
    muz = ndi.binary_fill_holes(lab == big); ys, xs = np.where(muz)
    rows = ((d > 14) & muz).sum(1); y = ys.min()
    while rows[y] == 0: y += 1              # nostril band
    while rows[y] > 0: y += 1               # ...ends at the first clear row
    nend = int(y)
    while rows[y] == 0: y += 1              # philtrum top = first mouth row
    mask = (d > 14) & ndi.binary_erosion(muz, iterations=8) & (np.arange(rgb.shape[0])[:, None] >= y - 1)
    my, mx = np.where(mask & (np.arange(rgb.shape[0])[:, None] < y + 12))
    sw = int(mask[int(y) + 6].sum()); op = ndi.binary_opening(mask, iterations=sw // 2 + 2)   # open mouth = what survives removing the philtrum/strokes
    oy, ox = np.where(op); oh = int(oy.max() - oy.min() + 1) if len(oy) else 0; ow = int(ox.max() - ox.min() + 1) if len(ox) else 0
    wide = next(yy for yy in range(int(y), mask.shape[0]) if mask[yy].sum() > 1.8 * sw)   # first row wider than the philtrum = where the mouth proper begins
    ocy = (oy.min() + oy.max() + 1) / 2 if len(oy) else 0
    return dict(nend=nend, wide=wide, ocy=ocy, oh=oh, ow=ow, sw=sw, rgb=rgb, d=d, muz=muz, mask=mask, mw=xs.max() - xs.min() + 1, ax=mx.mean(), ay=float(y), box=(xs.min(), ys.min(), xs.max(), ys.max()))
ref = analyse(f"{SRC}/pose_speaking_raw.png"); aaa = analyse(f"{SRC}/face_aaa_raw.png")
K = 1.5                                      # critic + Kamal: mouths read too small on a phone, so everything is 1.5x the artist's speaking mouth
AX = ref["ax"]; TOP = ref["ay"]              # philtrum x centre / top, from the original art
PH_W = ref["sw"] * K                         # nose-line stroke scales with the mouth (12 px at 1024)
def med(a, m): return tuple(np.median(a[m], axis=0))
PH = med(ref["rgb"], (ref["mask"] & (np.abs(np.arange(1024)[None, :] - AX) < 2) & (np.arange(1024)[:, None] > TOP + 8) & (np.arange(1024)[:, None] < TOP + 22)))
aop = ndi.binary_opening(aaa["mask"], iterations=aaa["sw"] // 2 + 2); arg = aaa["rgb"]
PINK = med(arg, aop & (arg[:, :, 0] > 215) & (arg[:, :, 1] > 100)); DARK = med(arg, aop & (arg[:, :, 0] < 150))
MUZ_BOTTOM = ref["box"][3]
# open-mouth centre: the original's, nudged up so the 1.5x bottom edge stays inside the muzzle (it is only ~13 px from the bottom edge)
CY_MID = ref["ocy"] - 3; MID_H = ref["oh"] * K
AAA_CY = ref["ocy"] - 5.5; AAA_BOTTOM = CY_MID + MID_H / 2; AAA_H = 2 * (AAA_BOTTOM - AAA_CY)
ROI = (399, 351, 624, 489)                   # canvas in pose coords (multiples of 3), big enough for every mouth
rw, rh = ROI[2] - ROI[0], ROI[3] - ROI[1]
def art_mouth(a, t, cy, sx=1.0):
    """The artist's mouth proper (philtrum rows dropped), scaled by t about its open centre, landed on (AX, cy). Un-mixed against flat muzzle, so edges are exact."""
    rows = np.arange(a["rgb"].shape[0])[:, None]
    al = np.clip((a["d"] - 12) / 8, 0, 1) * ndi.binary_dilation(a["mask"], iterations=5) * (rows >= a["wide"] - 3)   # no soft drop-shadow: it showed as a dark halo
    core = ndi.binary_erosion(al > 0.98, iterations=2); idx = ndi.distance_transform_edt(~core, return_distances=False, return_indices=True)
    C = a["rgb"][idx[0], idx[1]]            # edge pixels take the colour of the nearest solid mouth pixel: no muzzle- or shadow-coloured fringe
    pm = np.dstack([C * al[:, :, None], al * 255]).clip(0, 255).astype(np.uint8)
    sx0 = a["ax"] + (ROI[0] - AX) / (t * sx); sy0 = a["ocy"] + (ROI[1] - cy) / t
    r = np.array(Image.fromarray(pm, "RGBA").resize((rw, rh), Image.LANCZOS, box=(sx0, sy0, sx0 + rw / (t * sx), sy0 + rh / t))).astype(np.float32)
    ra = r[:, :, 3:4] / 255; rgb = np.where(ra > 0.003, r[:, :, :3] / np.maximum(ra, 0.003), 0)
    ra = np.clip((ra - 0.5) * 2.4 + 0.5, 0, 1)              # steepen the resampled edge to a crisp ~1 px anti-aliased stroke
    return Image.fromarray(np.dstack([rgb, ra * 255]).clip(0, 255).astype(np.uint8), "RGBA"), a["ay"]
SS = 4
def blank(): return Image.new("RGBA", (rw * SS, rh * SS), (0, 0, 0, 0))
def P(x, y): return ((x - ROI[0]) * SS, (y - ROI[1]) * SS)
def ell(d, cx, cy, w, h, col): d.ellipse((*P(cx - w / 2, cy - h / 2), *P(cx + w / 2, cy + h / 2)), fill=tuple(int(c) for c in col) + (255,))
def bar(d, y_end):                           # philtrum: same colour as the art, stroke scaled with the mouth, round top
    d.rounded_rectangle((*P(AX - PH_W / 2, TOP), *P(AX + PH_W / 2, y_end)), radius=PH_W / 2 * SS, fill=tuple(int(c) for c in PH) + (255,))
def done(im): return im.resize((rw, rh), Image.LANCZOS)
def over(under, top): u = under.copy(); u.alpha_composite(top); return u
mouths = {}
# mid: the artist's own half-open mouth, 1.5x
m, _ = art_mouth(ref, K, CY_MID); b = blank(); bar(ImageDraw.Draw(b), CY_MID - MID_H / 2 + 10); mouths["mid"] = over(done(b), m)
# aaa: the artist's wide-open drawing, scaled so it is as tall as the muzzle allows
t_aaa = AAA_H / aaa["oh"]; m, _ = art_mouth(aaa, t_aaa, AAA_CY, 1.12)   # 12% wider so it reads at phone size (>=16 px wide at 200 px tall)
b = blank(); bar(ImageDraw.Draw(b), AAA_CY - AAA_H / 2 + 10); mouths["aaa"] = over(done(b), m)
# ooo: filled, rounder dark oval with a pink lower lip (colours sampled from the artist's aaa mouth)
OW, OH_, OCY = 33, 33, CY_MID - 1          # round, ~22 px at 2x: clearly smaller and rounder than mid
b = blank(); d = ImageDraw.Draw(b); bar(d, OCY - OH_ / 2 + 10); ell(d, AX, OCY, OW, OH_, DARK)
lip = blank(); ld = ImageDraw.Draw(lip); ell(ld, AX, OCY + OH_ / 2 - 8, OW * 0.66, 11, PINK)
clip = blank(); ell(ImageDraw.Draw(clip), AX, OCY, OW, OH_, (255, 255, 255)); lip.putalpha(Image.fromarray(np.minimum(np.array(lip)[:, :, 3], np.array(clip)[:, :, 3])))
b.alpha_composite(lip); mouths["ooo"] = done(b)
# mmm: flat closed-lips line, a slight curve at most, stroke = the scaled nose-line weight
LW, LY, LD, LS = 74, CY_MID - 2, 2, 14      # LS: lip stroke (a touch heavier than the nose line so it reads at phone size)
LIP = tuple(int(c * 0.82) for c in PH)       # dark lip colour, no pink
b = blank(); d = ImageDraw.Draw(b); bar(d, LY)
pts = [P(AX + (i / 24 - .5) * LW, LY + LD * (1 - (2 * i / 24 - 1) ** 2)) for i in range(25)]   # ends lifted by LD: gentle smile at most
d.line(pts, fill=LIP + (255,), width=int(LS * SS), joint="curve")
for q in (pts[0], pts[-1]): d.ellipse((q[0] - LS * SS / 2, q[1] - LS * SS / 2, q[0] + LS * SS / 2, q[1] + LS * SS / 2), fill=LIP + (255,))
mouths["mmm"] = done(b)
# ---- mouth box = union of every overlay + PAD, on the 3 px grid; never above the nostrils ----
al_u = np.max([np.array(v)[:, :, 3] for v in mouths.values()], axis=0) > 8; ys, xs = np.where(al_u)
x0 = int(np.floor((ROI[0] + xs.min() - PAD) / 3) * 3); x1 = int(np.ceil((ROI[0] + xs.max() + 1 + PAD) / 3) * 3)
y0 = int(np.ceil(max(ROI[1] + ys.min() - PAD, ref["nend"] + 1) / 3) * 3); y1 = int(np.ceil((ROI[1] + ys.max() + 1 + PAD) / 3) * 3)
bw, bh = x1 - x0, y1 - y0
mouths = {n: v.crop((x0 - ROI[0], y0 - ROI[1], x1 - ROI[0], y1 - ROI[1])) for n, v in mouths.items()}
print("muzzle", ref["box"], "mouth box", (x0, y0, x1, y1))
for n, v in mouths.items(): print(n, "visible bbox (1024):", (lambda yy, xx: (x0 + xx.min(), y0 + yy.min(), x0 + xx.max() + 1, y0 + yy.max() + 1))(*np.where(np.array(v)[:, :, 3] > 128)))
# ---- speaking body WITHOUT a mouth: the muzzle is one flat colour, so repaint the whole mouth box with it (no trace) ----
base = speaking_cut.copy(); fill = ref["muz"][y0:y1, x0:x1]; base[y0:y1, x0:x1, :3][fill] = MUZ   # muzzle pixels only
files = {}
for k, im in sized(base).items(): files[k] = save(im, f"speaking_{k}")
manifest["poses"]["speaking"] = files
# ---- write talk set: body + overlays at both sizes, offsets in output pixels ----
cx0, cy0 = CROP[0], CROP[1]
manifest["talk"] = {"body": manifest["poses"]["speaking"], "mouths": {}, "order": ["mmm", "mid", "aaa", "ooo"]}
for name, mo in mouths.items():
    files, offs, sz = {}, {}, {}
    for k, h in SIZES.items():
        sc = h / 768
        ov = premult_resize(mo, (round(bw * sc), round(bh * sc)))
        files[k] = save(ov, f"mouth_{name}_{k}", 90); offs[k] = [round((x0 - cx0) * sc), round((y0 - cy0) * sc)]; sz[k] = list(ov.size)
    manifest["talk"]["mouths"][name] = {"files": files, "offset": offs, "size": sz}
# ---- faces (own union crop, square-ish) ----
fc = {s: cutout(f"{SRC}/face_{f}_raw.png") for s, f in FACES.items()}
bb = [np.where(a[:, :, 3] > 8) for a in fc.values()]
fx0 = min(b[1].min() for b in bb) - 4; fx1 = max(b[1].max() for b in bb) + 4; fy0 = min(b[0].min() for b in bb) - 4; fy1 = max(b[0].max() for b in bb) + 4
for s, a in fc.items():
    im = Image.fromarray(a, "RGBA").crop((fx0, fy0, fx1, fy1)); files = {}
    for k, h in SIZES.items(): files[k] = save(premult_resize(im, (round(im.width * h / im.height), h)), f"face_{s}_{k}")
    manifest["faces"][s] = files
manifest["note"] = "Per-state files are keyed by size; draw talk.body then overlay talk.mouths[name] at offset[size] with width/height size[size] (css px = file px / (1x:1, 2x:2)); never hardcode the mouth size."
json.dump(manifest, open(f"{DST}/tilo.json", "w"), indent=1)
print("tilo images:", len(os.listdir(DST)) - 1, "files,", total // 1024, "KB")
