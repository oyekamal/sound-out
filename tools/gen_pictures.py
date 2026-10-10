#!/usr/bin/env python3
"""Sound Out word + scene pictures with Kie nano-banana-2, in the approved Tilo style (flat vector, soft rounded shapes, warm palette, no outlines).
  gen_pictures.py samples          -> design/pictures/samples/*.png (6 style samples, alpha)
  gen_pictures.py run [--levels 1-4]-> raw + alpha for everything in content/pictures_needed.json (resumable)
"""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kie_img import generate
from gen_character import to_alpha, fit
ROOT = os.path.join(HERE, ".."); REF = os.path.join(ROOT, "design/character/tilo-cute/ref.png")
OUT = os.path.join(ROOT, "design/pictures")
STYLE_VERSION = 5
STYLE = ("Flat vector children's-book illustration in EXACTLY the rendering style of the reference image: soft round chubby shapes with rounded corners, NO outlines or contour strokes at all (shapes are separated only by flat colour changes), solid flat colour fills with one slightly darker flat shade "
 "for form, slightly muted warm friendly palette, never neon or oversaturated (sandy browns, cream, warm orange, soft pink, sky blue, leaf green), tiny pink blush on faces, big round shiny eyes with a white highlight on animals and people ONLY (objects, food, buildings and vehicles have NO faces and no eyes). "
 "Draw ONLY the subject described below: ONE clear subject or ONE tiny scene, centred, filling about 70 percent of the square frame with at least 10 percent white margin on every side, plain pure white background, no ground line, no frame, no border, NO shadow and no ground under it. Camera is front-on or a flat side view: NO perspective, NO isometric or 3/4 views. No decorative plants, filler shapes, extra props or background objects: only what the description names. "
 "Do NOT draw the capybara character from the reference and do NOT copy its teal ear-bead or satchel onto anything; use the reference for rendering style only. The WHOLE subject must be fully inside the frame with clear white margin on all four sides, nothing cropped or touching the edge. No jewellery, collars or accessories unless the subject is that item. "
 "ABSOLUTELY NO text, letters, numbers, words, signs, logos, labels or speech bubbles anywhere. No flags, no religious or cultural symbols. People are generic and global (varied skin tones, simple dress). Cute and calm, never scary. People and animals have a friendly, gentle, smiling expression unless the description names another emotion. ")
def prompt(desc, scene=False):
    kind = "A tiny self-contained scene (a small vignette, no big background): " if scene else "Subject: "
    return STYLE + kind + desc.strip().rstrip(".") + "."
def make(key, desc, out_dir, scene=False, tries=3):
    raw = f"{out_dir}/raw/{key}.png"; png = f"{out_dir}/{key}.png"
    os.makedirs(f"{out_dir}/raw", exist_ok=True)
    if not os.path.exists(raw): generate(prompt(desc, scene), raw, refs=[REF], model="nano-banana-2", tries=tries)
    if not os.path.exists(png): fit(to_alpha(raw), 512, 0.04).save(png)
    return png
SAMPLES = {"cat": ("a cute orange tabby cat sitting", False), "bed": ("a single bed seen from the side, flat, with a blue blanket and one plain cream pillow, nothing else", False), "run": ("a child running fast with arms pumping, a small speed puff behind", False),
           "sad": ("a child with drooping shoulders and head tilted down, downturned mouth, arms hanging limp, eyebrows slanted up in the middle, mouth strongly downturned, eyes glossy and lowered, no tears, no puddle", False), "rainbow": ("a bright rainbow arching over green hills", False),
           "scene_truck": ("a boy leaning back with both hands up near his ears, eyes wide and mouth open in an O, startled, beside an old blue pickup truck with a puff of grey smoke rising from its hood, and three short curved cartoon sound-wave lines beside the truck showing a loud noise; plain bare legs, no socks", True)}
if __name__ == "__main__":
    if sys.argv[1] == "samples":
        d = f"{OUT}/samples"
        with ThreadPoolExecutor(6) as ex: list(ex.map(lambda kv: make(kv[0], kv[1][0], d, kv[1][1]), SAMPLES.items()))
        print("ok")

# ---- batch run, OCR check, pack ----
NEEDED = os.path.join(ROOT, "content/pictures_needed.json")
WEBP = os.path.join(ROOT, "app/public/img/words")
OCRPY = "/tmp/claude-1000/sc/ocrenv/bin/python"
def fname(key): return key.replace(":", "-")
def concepts():
    c = json.load(open(NEEDED))["concepts"]
    return {k: v for k, v in c.items() if not v.get("alias_of")}
def batch(keys, workers=16):
    c = concepts(); fails = {}
    def one(k):
        try: make(fname(k), c[k]["draw"], f"{OUT}/all", scene=c[k]["type"] == "scene", tries=3)
        except Exception as e: fails[k] = str(e)[:200]
    with ThreadPoolExecutor(workers) as ex: list(ex.map(one, keys))
    return fails
def ocr_check(files):
    """Run rapidocr in its venv; returns {file: [text,...]} of Latin/digit detections (CJK false positives on eyes are ignored)."""
    import subprocess, re
    code = ("import sys,json,re\nfrom rapidocr_onnxruntime import RapidOCR\no=RapidOCR();out={}\nfor f in sys.argv[1:]:\n"
            " from PIL import Image\n im=Image.open(f).convert('RGBA');bg=Image.new('RGBA',im.size,(255,255,255,255));bg.alpha_composite(im);bg.convert('RGB').save('/tmp/_ocr.png')\n"
            " r,_=o('/tmp/_ocr.png');out[f]=[t for b,t,s in (r or []) if re.search('[A-Za-z]{2,}',t) and float(s)>0.6]\nprint(json.dumps(out))")
    res = {}
    for i in range(0, len(files), 40):
        res.update(json.loads(subprocess.run([OCRPY, "-c", code, *files[i:i + 40]], capture_output=True, text=True).stdout.strip().splitlines()[-1]))
    return res
def pack(key, src, size=256, target=15000):
    from PIL import Image
    im = Image.open(src).convert("RGBA"); im = im.resize((size, size), Image.LANCZOS)
    out = f"{WEBP}/{fname(key)}.webp"; os.makedirs(WEBP, exist_ok=True)
    for q in (82, 74, 66, 58, 50, 42):
        im.save(out, "WEBP", quality=q, alpha_quality=80, method=6)
        if os.path.getsize(out) <= target: break
    return out
if __name__ == "__main__" and sys.argv[1] == "run":
    c = concepts(); keys = [k for k in c if not os.path.exists(f"{OUT}/all/{fname(k)}.png")]
    print("to make", len(keys)); t = time.time(); fails = batch(keys); print("fails", len(fails), time.time() - t)
    json.dump(fails, open(f"{OUT}/fails.json", "w"), indent=1)

def border_touch(raw, thresh=235):
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(raw).convert("RGB")).astype(int); h, w, _ = a.shape; r = 4
    ring = np.concatenate([a[:r].reshape(-1, 3), a[-r:].reshape(-1, 3), a[:, :r].reshape(-1, 3), a[:, -r:].reshape(-1, 3)])
    return float(((ring < thresh).any(axis=1)).mean())
def qa(keys=None):
    """Auto checks: OCR text (Latin/digits), subject touching the frame edge (cropped). Writes design/pictures/qa.json; returns failing keys."""
    c = concepts(); keys = [k for k in (keys or c) if os.path.exists(f"{OUT}/all/{fname(k)}.png")]
    ocr = ocr_check([f"{OUT}/all/{fname(k)}.png" for k in keys]); res = {}
    for k in keys:
        f = f"{OUT}/all/{fname(k)}.png"; txt = ocr.get(f, []); bt = border_touch(f"{OUT}/all/raw/{fname(k)}.png")
        res[k] = {"text": txt, "edge": round(bt, 4), "fail": ("text" if txt else "") + (" crop" if bt > 0.012 else "")}
    json.dump(res, open(f"{OUT}/qa.json", "w"), indent=1)
    return [k for k, v in res.items() if v["fail"]]
def redo(keys, hint):
    c = concepts()
    for k in keys:
        for p in (f"{OUT}/all/{fname(k)}.png", f"{OUT}/all/raw/{fname(k)}.png"):
            if os.path.exists(p): os.remove(p)
    def one(k):
        try: make(fname(k), hint + c[k]["draw"], f"{OUT}/all", scene=c[k]["type"] == "scene")
        except Exception as e: print("fail", k, e)
    with ThreadPoolExecutor(16) as ex: list(ex.map(one, keys))
if __name__ == "__main__" and sys.argv[1] == "qa":
    bad = qa(); print(len(bad), bad)

def pack_all():
    c = json.load(open(NEEDED))["concepts"]; man = {}; meta = {}; sizes = []
    for k, v in c.items():
        src_key = fname(v.get("alias_of") or k)
        src = f"{OUT}/all/{src_key}.png"
        if not os.path.exists(src): continue
        out = pack(src_key, src); man[k] = os.path.basename(out); sizes.append(os.path.getsize(out))
        meta[k] = {"type": v["type"], "count": v["count"], "levels": v["levels"], "ambiguous": v.get("ambiguous", False), "must_show_action": v.get("must_show_action", False)}
    json.dump(dict(sorted(man.items())), open(f"{WEBP}/pictures.json", "w"), indent=1)
    json.dump(meta, open(f"{WEBP}/pictures.meta.json", "w"), indent=1)
    return len(man), sum(sizes) // len(sizes), max(sizes), sum(sizes)
if __name__ == "__main__" and sys.argv[1] == "pack":
    print(pack_all())
