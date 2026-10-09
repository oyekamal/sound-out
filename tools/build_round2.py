#!/usr/bin/env python3
"""Round 2 blind test: Kapi composited INTO real Sound Out lesson screenshots vs Duolingo ABC lesson screens (marketing header and phone frame cropped away).
  python3 tools/build_round2.py   -> design/character/round2/p<N>_<A|B>.png, round2_key.json, round2_key.js (the HTML only loads the key on reveal)."""
import json, os, random
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
C = f"{R}/design/character"; O = f"{C}/round2"; os.makedirs(O, exist_ok=True)
W, H = 420, 608          # both sides rendered at the same size
# (Sound Out shot, Kapi pose, width as fraction of screen, x centre, y bottom in the 780x1125 crop) vs (Duolingo shot, crop box)
PAIRS = [
 ("A_03_oral-first-What_sound_does_it_start.png", "point", 0.44, 0.74, 1115, 5, (56, 292, 322, 696)),
 ("A_04_oral-blend-Which_word_do_the_sounds.png", "listen", 0.58, 0.60, 1110, 3, (56, 292, 336, 696)),
 ("A_01_who-is-reading.png", "wait", 0.52, 0.62, 1115, 7, (56, 272, 336, 696)),
]
def alpha(p):
    import sys; sys.path.insert(0, f"{R}/tools"); from gen_character import to_alpha; return to_alpha(p)
def ours(shot, pose, wfrac, cx, yb):
    bg = Image.open(f"{R}/app/shots/{shot}").convert("RGBA").crop((0, 0, 780, 1125))
    k = alpha(f"{C}/kapi/pose_{pose}_raw.png"); w = int(780 * wfrac); k = k.resize((w, int(k.height * w / k.width)), Image.LANCZOS)
    bg.alpha_composite(k, (int(780 * cx - w / 2), yb - k.height))
    return bg.convert("RGB").resize((W, H), Image.LANCZOS)
def theirs(n, box):
    return Image.open(f"{C}/bar/duolingo_abc_{n}.jpg").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
rng = random.Random(20261009); key = {}
for i, (shot, pose, wf, cx, yb, dn, box) in enumerate(PAIRS, 1):
    a, b = ours(shot, pose, wf, cx, yb), theirs(dn, box); ours_side = rng.choice("AB")
    (a if ours_side == "A" else b).save(f"{O}/p{i}_{ours_side}.png")
    (b if ours_side == "A" else a).save(f"{O}/p{i}_{'B' if ours_side == 'A' else 'A'}.png")
    key[f"p{i}"] = {"ours": ours_side, "screen": shot, "kapi_pose": pose, "duolingo_shot": f"duolingo_abc_{dn}.jpg"}
json.dump(key, open(f"{C}/round2_key.json", "w"), indent=1)
open(f"{C}/round2_key.js", "w").write("const KEY=" + json.dumps(key) + ";")
print(key)
