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
ref = analyse(f"{SRC}/pose_speaking_raw.png")
srcs = {"mid": ("pose_speaking", ref)}
for n in ("mmm", "aaa", "ooo"): srcs[n] = (f"face_{n}", analyse(f"{SRC}/face_{n}_raw.png"))
scale = {n: ref["mw"] / a["mw"] for n, (_, a) in srcs.items()}       # face px -> pose px (muzzle width = shared feature)
# the aaa drawing opens much wider than the artist's speaking mouth; cap it so its open mouth is at most 1.15x the original
scale["aaa"] = min(scale["aaa"], 1.15 * ref["oh"] / srcs["aaa"][1]["oh"])
# aaa/ooo open far lower/higher than the original on the philtrum: shift each so the OPEN MOUTH is centred on the original's
dyn = {n: (ref["ocy"] - (ref["ay"] + (a["ocy"] - a["ay"]) * scale[n])) if n in ("aaa", "ooo") else 0.0 for n, (_, a) in srcs.items()}
def to_pose(n, x, y): a = srcs[n][1]; return ref["ax"] + (x - a["ax"]) * scale[n], ref["ay"] + dyn[n] + (y - a["ay"]) * scale[n]
ub = [1e9, 1e9, -1e9, -1e9]
for n, (_, a) in srcs.items():
    ys, xs = np.where(ndi.binary_dilation(a["mask"], iterations=3))
    for (x, y) in ((xs.min(), ys.min()), (xs.max() + 1, ys.max() + 1)):
        px, py = to_pose(n, x, y); ub = [min(ub[0], px), min(ub[1], py), max(ub[2], px), max(ub[3], py)]
x0 = int(np.floor((ub[0] - PAD) / 3) * 3); y0 = int(np.ceil(max(ub[1] - PAD, ref["nend"] + 1) / 3) * 3)   # never cut into the nostrils
x1 = int(np.ceil((ub[2] + PAD) / 3) * 3); y1 = int(np.ceil((ub[3] + PAD) / 3) * 3)
bw, bh = x1 - x0, y1 - y0
print("muzzle", ref["box"], "box", (x0, y0, x1, y1), "open-mouth px (1024 scale): ref", ref["oh"], ref["ow"], {n: (a["oh"], a["ow"], a["sw"]) for n, (_, a) in srcs.items()})
print("mouth box (1024):", (x0, y0, x1, y1), "scales", {k: round(v, 3) for k, v in scale.items()})
def cut(n):
    """RGBA overlay in pose coords: alpha = distance from the flat muzzle colour; RGB = the artist's pixels."""
    _, a = srcs[n]; al = np.clip((a["d"] - 2) / 22, 0, 1) * ndi.binary_dilation(a["mask"], iterations=5)
    # un-mix against the flat muzzle: alpha*C + (1-alpha)*MUZ == the artist's pixel, so edges composite back exactly (no halo, rim kept)
    C = (np.array(MUZ, np.float32) + (a["rgb"] - np.array(MUZ, np.float32)) / np.maximum(al, 1e-3)[:, :, None]).clip(0, 255)
    pm = np.dstack([C * al[:, :, None], al * 255]).clip(0, 255).astype(np.uint8)
    sc = scale[n]; fx0 = a["ax"] + (x0 - ref["ax"]) / sc; fy0 = a["ay"] + (y0 - ref["ay"] - dyn[n]) / sc
    r = np.array(Image.fromarray(pm, "RGBA").resize((bw, bh), Image.LANCZOS, box=(fx0, fy0, fx0 + bw / sc, fy0 + bh / sc))).astype(np.float32)
    ra = r[:, :, 3:4] / 255; rgb = np.where(ra > 0.003, r[:, :, :3] / np.maximum(ra, 0.003), 0)
    return Image.fromarray(np.dstack([rgb, r[:, :, 3:4]]).clip(0, 255).astype(np.uint8), "RGBA")
mouths = {n: cut(n) for n in srcs}
# every overlay shares the artist's own philtrum (same stroke width) down to where its mouth proper starts, so frames never step or flicker there
for n in ("mmm", "aaa", "ooo"):
    yw = int(min(to_pose(n, 0, srcs[n][1]["wide"])[1], ref["wide"])) - 2 - y0
    c0 = int(ref["ax"] - x0 - 8); r0 = int(ref["ay"] - y0) - 2
    if yw > r0:
        mo = np.array(mouths[n]); mo[r0:yw, c0:c0 + 16] = np.array(mouths["mid"])[r0:yw, c0:c0 + 16]; mouths[n] = Image.fromarray(mo, "RGBA")
# ---- speaking body WITHOUT a mouth: the muzzle is one flat colour, so repaint the whole mouth box with it (no trace) ----
# keep the artist's philtrum down to just above where the highest mouth proper begins (each overlay redraws its own philtrum on top)
yp = int(min(to_pose(n, 0, a["wide"])[1] for n, (_, a) in srcs.items())) - 3
keep = np.zeros((y1 - y0, x1 - x0), bool); keep[:max(0, yp - y0), int(ref["ax"] - x0 - 8):int(ref["ax"] - x0 + 8)] = True
base = speaking_cut.copy(); fill = ref["muz"][y0:y1, x0:x1] & ~keep; base[y0:y1, x0:x1, :3][fill] = MUZ   # muzzle pixels only; corners of the box outside the muzzle are left alone
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
