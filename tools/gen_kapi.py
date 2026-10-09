#!/usr/bin/env python3
"""Sound Out character round 2: Kapi the capybara, rebuilt. Reference variants -> poses -> expressions -> sheets.
  python3 tools/gen_kapi.py refs            4 reference variants into design/character/kapi/ref_<v>.png (pick one, copy to ref.png)
  python3 tools/gen_kapi.py poses [name..]  poses from ref.png      -> kapi/pose_<name>_raw.png
  python3 tools/gen_kapi.py faces [name..]  head expressions        -> kapi/face_<name>_raw.png
  python3 tools/gen_kapi.py build           alpha, pose sheet, expression sheet, 48 px icon
Backend Kie nano-banana (tools/kie_img.py). Delete a *_raw.png to regenerate it."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kie_img import generate
from gen_character import to_alpha, fit
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design", "character", "kapi")

STYLE = ("Flat vector character illustration, NO outlines, solid flat colour fills, one slightly darker flat shade for volume, plain pure white background, "
         "one character centered with generous margin. Absolutely no text, letters, numbers, symbols, speech bubbles or props with writing. ")
ANATOMY = ("A real CAPYBARA, not a bear, not a hamster, not a teddy: a very long, flat-topped, BOXY rectangular head, a big blunt square snout with a large dark nose pad "
           "and a split upper lip, TINY small ears set high and far back on the head (small, low, slightly oval, NOT big round bear ears), small eyes set HIGH and toward the sides of the head, "
           "a heavy barrel-shaped body, short stubby legs, small blunt toes. Colours: russet-brown #B5764A body, deeper brown #8A5535 across the head top and back, "
           "tan-cream #E8CFA6 on the muzzle sides, chin and belly. ")
FACE = ("The FACE has its own acting: small dark glossy oval eyes (no big white sclera, no sparkles, no anime shine, just one tiny highlight) with a visible flat UPPER EYELID that can droop or lift, "
        "and two clear expressive eyebrows in deeper brown above the eyes. NO blush, no cheek circles, calm and warm and grown-up, never babyish. ")
SIG = ("Two signature details: (1) a small round TEAL #1FA6A0 bead-ring clipped on the LEFT ear (viewer's right) only, the 'listening ear'; "
       "(2) a slim cream-and-teal woven cord worn like a sash across the chest holding a small flat tan satchel at the hip. No scarf. No hat, no fruit, no flowers. ")
REF = {
 "a": "STANCE: stands on four short legs in a three-quarter side view, long body horizontal, head turned to look at the viewer, calm.",
 "b": "STANCE: sits upright on its haunches like a patient dog or meerkat, torso raised about 70 degrees, short forelegs free to gesture, three-quarter view, head level, calm.",
 "c": "STANCE: stands upright on two hind legs, barrel body, short forelegs held in front, front view of the face, calm.",
 "d": "STANCE: sits on its haunches, torso upright, seen from the FRONT, forepaws resting on its belly, long boxy head facing the viewer, calm and attentive.",
}
POSES = {
 "listen": "leans toward the viewer's right, one forepaw raised cupped just behind its LEFT ear with the teal bead, head tilted slightly, eyes soft and focused on the viewer, mouth closed, eyebrows slightly raised.",
 "point": "sits tall facing the viewer's LEFT exactly like the reference (long snout toward the left), one foreleg stretched straight out to the LEFT, below and in front of the snout, pointing with a single extended toe at an empty spot beside it, eyes glancing toward that spot, one eyebrow raised slightly, mouth gently closed.",
 "model": "face turned a little toward the viewer, mouth open in a clear round 'oh' shape with the tongue and lower teeth subtly visible so a learner can copy the mouth shape, one forepaw touching its own chin, eyebrows lifted, patient and clear.",
 "correct": "head tilted a little, eyebrows pulled up and slightly together in the middle (concern, not sadness), eyelids soft, small closed mouth with one corner slightly lifted, one forepaw held open palm-up toward the viewer as an offering 'try again' gesture.",
 "wait": "relaxed rest pose, lying settled like a loaf with forelegs folded forward and tucked, head up, eyes half-lidded and calm, a tiny tilt of the head, mouth softly closed, bead ear still visible.",
 "celebrate": "sits tall with chest lifted, BOTH forelegs raised symmetrically to shoulder height with paws open, like a quiet proud cheer, eyes warm and slightly closed in a pleased smile, eyebrows soft, a small closed-mouth smile, two tiny flat teal sparkle dots near the head, restrained and proud not hyper.",
}
FACES = {
 "listen": "calm listening: eyes open and steady, eyebrows level and slightly lifted, head tilted a few degrees, mouth closed.",
 "think": "thinking: eyes glancing up and to the side, one eyebrow raised higher than the other, mouth closed and slightly pursed to one side.",
 "proud": "warm pride: eyelids softened into gentle arcs, eyebrows relaxed and slightly raised, a small closed-mouth smile lifting both corners, chin up a touch.",
 "retry": "gentle 'not quite, try again': inner ends of the eyebrows pulled up, eyes soft and attentive, small mouth slightly pressed with one corner lifted. Concern, NOT sadness, no tears.",
 "wait": "patient waiting: upper eyelids half-lowered, eyebrows relaxed, mouth closed and neutral, serene.",
 "speak": "speaking: mouth open in a round 'oh' shape with a hint of tongue, eyebrows slightly raised, eyes open and kind.",
}

def refs():
    os.makedirs(D, exist_ok=True)
    def one(v):
        out = f"{D}/ref_{v}.png"
        if not os.path.exists(out):
            generate(STYLE + ANATOMY + FACE + SIG + REF[v] + " Neutral calm expression.", out, model="nano-banana-pro")
        return v
    with ThreadPoolExecutor(4) as ex: list(map(print, ex.map(one, REF)))

def _gen(kind, table, extra, names, size_ref="ref.png"):
    ref = f"{D}/{size_ref}"
    keep = ("Keep EXACTLY the same character as the reference image: same long boxy capybara head, same tiny high ears, same colours, same teal ear bead on the left ear, "
            "the teal bead on the LEFT ear ONLY (never on both ears), same cord and satchel, only ONE eyebrow per visible eye and NO stray floating marks, dots or eyebrows anywhere off the head, "
            "same face style with eyelids and brows, same flat style. Unless the expression below says otherwise the mouth is warm and neutral (corners level or very slightly lifted, never turned down, never grumpy). Only the " + extra + " changes. ")
    def one(n):
        out = f"{D}/{kind}_{n}_raw.png"
        if not os.path.exists(out):
            generate(STYLE + keep + ("Pose: " if kind == "pose" else "Same full-body sitting pose and same side view as the reference, only the face changes (the head will be cropped later). Expression: ") + table[n],
                     out, refs=[ref], model="nano-banana-2")
        return n
    with ThreadPoolExecutor(6) as ex: list(map(print, ex.map(one, names or list(table))))

def sheets():
    def row(kind, table, cell, cols):
        names = list(table); rows = (len(names) + cols - 1) // cols
        sh = Image.new("RGB", (cell * cols, cell * rows), "white")
        for i, n in enumerate(names):
            p = f"{D}/{kind}_{n}_raw.png"
            if os.path.exists(p):
                im = fit(to_alpha(p), cell, 0.04); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
                sh.paste(bg.convert("RGB"), (cell * (i % cols), cell * (i // cols)))
        return sh
    row("pose", POSES, 480, 3).save(f"{D}/sheet_poses.png")
    for n in FACES:
        p = f"{D}/face_{n}_raw.png"
        if os.path.exists(p):
            a = to_alpha(p); w, h = a.size; a.crop((0, 0, int(w * 0.94), int(h * 0.50))).save(f"{D}/face_{n}.png")
    cw, ch = 520, 340; fs = Image.new("RGB", (cw * 3, ch * 2), "white")
    for i, n in enumerate(FACES):
        if os.path.exists(f"{D}/face_{n}.png"):
            im = Image.open(f"{D}/face_{n}.png"); im.thumbnail((cw - 20, ch - 20), Image.LANCZOS)
            bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
            fs.paste(bg.convert("RGB"), (cw * (i % 3) + (cw - im.width) // 2, ch * (i // 3) + (ch - im.height) // 2))
    fs.save(f"{D}/sheet_faces.png")
    ref = to_alpha(f"{D}/ref.png"); fit(ref, 768).save(f"{D}/ref_alpha.png")
    # icon: head crop of the face_listen image (head fills frame)
    f = Image.open(f"{D}/face_listen.png"); f = f.crop((0, 0, f.width, f.height))
    S = 768; tile = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(tile).ellipse((0, 0, S - 1, S - 1), fill=(241, 221, 187, 255))
    g = f.copy(); g.thumbnail((int(S * 0.84), int(S * 0.84)), Image.LANCZOS); lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    lay.alpha_composite(g, ((S - g.width) // 2, S - g.height - int(S * 0.02)))
    m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
    tile.alpha_composite(Image.composite(lay, Image.new("RGBA", (S, S), (0, 0, 0, 0)), m)); tile.save(f"{D}/icon_768.png")
    tile.resize((192, 192), Image.LANCZOS).save(f"{D}/icon_192.png"); tile.resize((48, 48), Image.LANCZOS).save(f"{D}/icon_48.png")

if __name__ == "__main__":
    a = sys.argv[1:]; cmd = a[0] if a else "sheets"
    if cmd == "refs": refs()
    elif cmd == "poses": _gen("pose", POSES, "pose and head angle", a[1:])
    elif cmd == "faces": _gen("face", FACES, "expression", a[1:])
    else: sheets()
