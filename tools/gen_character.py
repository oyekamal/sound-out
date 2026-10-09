#!/usr/bin/env python3
"""Sound Out character concepts (round 1). Hero image -> 4 pose images using the hero as reference -> sheet + 48 px icon.
  python3 tools/gen_character.py [concept ...]      outputs design/character/concepts/<name>/
Pattern from urdu-reading-course/design/gen/gen_assets.py (STYLE + reference image, white flood-filled to alpha), backend = Kie nano-banana."""
import os, sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kie_img import generate
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design", "character", "concepts")

STYLE = ("Flat vector character illustration for a global reading-teacher app, soft rounded shapes, NO outlines, "
         "solid flat colour fills with one slightly darker flat shade on the underside, big round white eyes with a dark pupil and a tiny white highlight, "
         "a small warm closed-mouth smile, calm and kind, friendly to a 5-year-old but dignified enough that a 40-year-old would not find it babyish, "
         "plain pure white background, single character centered with generous margin, full body visible, "
         "absolutely no text, no letters, no numbers, no symbols, no speech bubbles, no props that contain writing. ")
KEEP = "Keep EXACTLY the same character as the reference image: same species, shape, colours, proportions, eyes and style. Only the pose changes. "
POSES = {"speaking": "mouth open in a gentle round 'oh' shape as if speaking clearly to the viewer, one hand/limb raised slightly in a friendly explaining gesture",
         "listening": "head tilted a little to one side, one hand/limb cupped behind where an ear would be, eyes wide and attentive, mouth closed, patient",
         "pointing": "pointing firmly to the viewer's right with one arm/limb stretched out, other arm relaxed, looking toward the pointed direction, encouraging smile",
         "cheering": "both arms/limbs raised high, joyful open smile, eyes happy, a few tiny flat sparkle shapes around, celebrating"}
C = {
 "kapi": dict(line="Capybara: the world's calmest animal, a meme-loved calm that adults adore, nobody's national mascot.",
   desc="a chubby capybara standing upright on two feet like a small gentle teacher, warm sandy-brown body, lighter cream belly, small round ears, blunt friendly snout with two tiny nostrils, tiny rounded hands, a small round teal scarf, palette of sandy brown #C98B55, cream #F6E3C4, teal #1FA6A0", crop=(0.1, 0.0, 0.9, 0.5)),
 "tola": dict(line="Tortoise: patient by nature, it waits without sighing; slowness becomes a virtue for the learner.",
   desc="a small round tortoise standing upright on two sturdy legs, a big domed shell in warm saffron-orange #F2A23A with a simple soft hexagon pattern, soft sage-green body #8CC084, a long gentle neck, big kind eyes, tiny rounded hands, palette saffron #F2A23A, sage #8CC084, cream #FFF1D6", crop=(0.15, 0.0, 0.85, 0.5)),
 "noo": dict(line="Cloud: no species, no culture, no age; a soft voice made visible, floats rather than walks, so it never looks like it is talking down.",
   desc="a small fluffy cloud character with no legs, a soft rounded cloud body in sky blue #8FD0F5 with a lighter white top #FFFFFF-ish #E9F6FF, two small cloud-puff hands, rosy cheeks #F7A8B8, a floating little tuft of cloud on its head, palette sky blue #8FD0F5, pale #E9F6FF, rose #F7A8B8", crop=(0.1, 0.1, 0.9, 0.9)),
 "axi": dict(line="Axolotl: a global internet favourite for all ages, permanent smile, gill-frills like three tiny ear-trumpets that make 'listening' read instantly.",
   desc="an axolotl standing upright on two short legs with a tail, rosy-pink body #F4A6B8, lighter pink belly #FBD3DC, three feathery gill frills on each side of the head in deeper coral #E8697F, wide gentle smile, big dark friendly eyes, tiny rounded hands, palette rose-pink #F4A6B8, coral #E8697F, cream #FFF0E6", crop=(0.05, 0.0, 0.95, 0.5)),
 "lumo": dict(line="Lamp: a small glowing lantern, the 'light comes on' moment of reading; an object, not an animal, so it is culturally neutral and ageless.",
   desc="a small round paper-lantern-like lamp character with a short stubby handle loop on top, body a warm glowing amber-yellow #FFC93C fading to soft orange #F7A233 at the bottom, a soft cream glow shape inside the belly, two tiny stubby feet, two small rounded hands, big kind eyes on the front, palette amber #FFC93C, orange #F7A233, deep plum #5B3A6B for the handle and feet", crop=(0.1, 0.0, 0.9, 0.6)),
}

def to_alpha(path, thresh=222):
    im = Image.open(path).convert("RGBA"); w, h = im.size; px = im.load()
    bg = lambda p: p[0] > thresh and p[1] > thresh and p[2] > thresh
    seen = bytearray(w * h); q = deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    mask = Image.new("L", (w, h), 255); mp = mask.load()
    while q:
        x, y = q.popleft(); i = y * w + x
        if seen[i]: continue
        seen[i] = 1
        if not bg(px[x, y]): continue
        mp[x, y] = 0
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    im.putalpha(mask); b = im.getchannel("A").getbbox()
    return im.crop(b) if b else im

def fit(im, size, pad=0.06):
    s = int(size * (1 - 2 * pad)); im = im.copy(); im.thumbnail((s, s), Image.LANCZOS)
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0)); c.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im); return c

def build(name):
    d = os.path.join(ROOT, name); os.makedirs(d, exist_ok=True); c = C[name]
    hero_raw = f"{d}/hero_raw.png"
    if not os.path.exists(hero_raw):
        generate(STYLE + "Character: " + c["desc"] + ". Standing neutral pose, facing the viewer, a slight welcoming smile.", hero_raw, model="nano-banana-pro")
    for p, t in POSES.items():
        out = f"{d}/pose_{p}_raw.png"
        if not os.path.exists(out):
            generate(STYLE + KEEP + "Pose: " + t + ".", out, refs=[hero_raw], model="nano-banana-2")
    hero = to_alpha(hero_raw); fit(hero, 768).save(f"{d}/hero.png")
    cells = [fit(to_alpha(f"{d}/pose_{p}_raw.png"), 384) for p in POSES]
    sheet = Image.new("RGBA", (384 * 4, 384), (255, 255, 255, 255))
    for i, im in enumerate(cells): sheet.alpha_composite(im, (384 * i, 0))
    sheet.convert("RGB").save(f"{d}/sheet.png")
    x0, y0, x1, y1 = c["crop"]; W, H = hero.size
    icon = hero.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    fit(icon, 192, 0.04).save(f"{d}/icon_192.png"); fit(icon, 48, 0.04).save(f"{d}/icon_48.png")
    return name

if __name__ == "__main__":
    names = sys.argv[1:] or list(C)
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(build, names): print("done", r)
