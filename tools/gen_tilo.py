#!/usr/bin/env python3
"""NOTE: pose_wait_raw.png came out facing right and was mirrored once after generation.
Sound Out character round 3: Tilo the capybara (renamed from Kapi). Warm open eyes, big-body acting, 3 mouth shapes, dedicated icon.
  python3 tools/gen_tilo.py refs              4 new-face reference variants from the round-2 silhouette -> tilo/ref_<v>.png (copy the winner to ref.png)
  python3 tools/gen_tilo.py poses [name..]    -> tilo/pose_<name>_raw.png
  python3 tools/gen_tilo.py faces [name..]    -> tilo/face_<name>_raw.png  (incl. mouth_mmm/aaa/ooo)
  python3 tools/gen_tilo.py build             alpha, pose + face boards, silhouette strip
Backend Kie nano-banana (tools/kie_img.py). Delete a *_raw.png to regenerate it. Icon: tools/make_icon.py."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kie_img import generate
from gen_character import to_alpha as _to_alpha, fit
import numpy as np
from scipy import ndimage
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = f"{R}/design/character/tilo"; OLD = f"{R}/design/character/kapi"

STYLE = ("Flat vector character illustration, NO outlines, solid flat colour fills, one slightly darker flat shade for volume, plain pure white background, "
         "one character centered with generous margin, whole body visible and not cropped. Absolutely no text, letters, numbers, symbols or speech bubbles. ")
EYES = ("EYES: bright, open, kind and alert, NOT half-lidded, NOT sleepy, NOT bored: a rounded dark brown eye with a thin pale rim, fully open upper lid, and a clear bright WHITE highlight "
        "(one larger white dot and one tiny white dot) so the eye sparkles with life. Moderate size, adult-friendly, no giant anime eyes, no blush, no cheek circles. "
        "Two soft eyebrows in deeper brown, gently lifted. The resting look is warm attention, like a teacher who is glad you are here, with a small genuine smile (mouth corners clearly lifted). ")
SAME = ("Keep EXACTLY the same character and silhouette as the reference image: same long boxy capybara head, blunt snout with dark nose pad, tiny high ears, same russet-brown and cream colours, "
        "seated barrel body, ONE small teal bead on the LEFT ear (viewer's right) only, same cream-and-teal woven cord across the chest and the same small tan satchel at the hip. "
        "Exactly two eyes, one eyebrow per eye, NO stray floating marks anywhere off the head (in particular NOTHING floats above the head: each eyebrow is painted ON the face right above its eye and never detached), anatomically correct paws with small blunt toes. ")

REF = {
 "a": "Redraw only the face: the eyes as described, slightly raised brows, a gentle closed smile. Same three-quarter side view facing left, same seated pose.",
 "b": "Redraw only the face: the eyes as described, brows soft and lifted, a warm closed smile and a very slight head tilt toward the viewer. Same seated pose facing left, eyes turned a little to look at the viewer.",
 "c": "Redraw the face and tilt the whole head a little down toward the viewer, as if looking at a child in front of it: the eyes as described, brows lifted, warm smile. Same seated body facing left.",
 "d": "Redraw only the face: the eyes as described, looking straight out at the viewer with the head turned a little more toward the viewer, a warm smile with a hint of the lower lip showing. Same seated body.",
}
POSES = {
 "listen": "LISTEN: the WHOLE BODY pitches forward strongly toward the viewer's LEFT like someone straining to hear: the torso tilted about 35 degrees forward, the head pushed far forward and low past the front of the feet, back arched, ONE forepaw lifted and CUPPED (fingers curled like a shell) right behind its LEFT ear with the teal bead, the other forepaw planted on the ground in front for balance, eyes wide, bright and looking toward the viewer's left where the learner is, mouth closed in a soft attentive smile, brows lifted.",
 "think": "THINK: sits low and compact, hunched slightly, the whole head TILTED sideways about 20 degrees, ONE forepaw raised with a single toe touching its own CHIN and the ELBOW sticking out sideways, the other forearm across the belly, eyes looking UP and to the right, one brow raised higher than the other, mouth closed and slightly pursed to one side, curious not worried.",
 "model": "MODEL A SOUND: rises tall on its haunches with chest lifted and head held high, faces toward the viewer's left, ONE forepaw raised high with a single extended toe POINTING AT ITS OWN MOUTH, the mouth open in a clear round 'aaa' shape (jaw dropped, upper teeth and pink tongue visible) so a learner can copy it, three small curved teal sound-wave arcs flat in front of the snout, eyes bright and focused on the viewer, brows lifted, confident and patient, clearly speaking and not yawning.",
 "try": "TRY AGAIN, ENCOURAGING: the body leans forward LOW toward the viewer's left on its haunches with the chest dipped, BOTH forelegs stretched far forward with OPEN PALMS facing up toward the learner (a welcoming 'you are nearly there, have another go' gesture), head tilted a little, eyes bright and warm looking right at the learner, eyebrows softly lifted high in the middle, a small reassuring smile with the corners clearly lifted. Never sad, never skeptical.",
 "celebrate": "CELEBRATE: HUGE joy. SAME long boxy capybara head profile as the reference facing left (blunt snout with nose pad clearly visible, NOT a short round face). The capybara stands up on its hind legs, body stretched tall, BOTH forelegs thrown straight UP above its head with paws open, torso arched back slightly, BOTH eyes closed in happy upward arcs, mouth wide open in a delighted laugh with pink tongue, ears perked, a few small flat teal and gold sparkle dots around the head. Much taller and wider than the resting pose.",
 "wait": "WAIT: calm, attentive, patient. Settled low in a compact LOAF shape, hind legs tucked under, belly near the ground, both forelegs folded neatly forward and tucked, the body long and low and wide, BUT the head is held UP, neck stretched, eyes wide open, bright and looking toward the viewer's left at the learner, a small gentle smile, brows relaxed and slightly lifted. Alert and kind, absolutely not sleepy. Satchel visible on the hip.",
 "point": "POINT: stands up TALL on its hind legs with the body straight, and ONE foreleg stretched out long and diagonally UP and to the viewer's LEFT at about 45 degrees, pointing with a single extended toe at something high up beside it, the other forepaw on its belly, eyes bright and glancing along the pointing arm, brows lifted, mouth in a warm smile.",
}
FACES = {
 "rest": "WAIT / resting: eyes bright and open, brows relaxed, gentle small smile.",
 "listen": "LISTENING: eyes wide and bright, looking toward the viewer's left (toward the learner), head leaning forward a little, brows lifted, mouth closed in a soft attentive smile.",
 "think": "THINKING: eyes looking UP and to the right, one brow raised higher than the other, mouth closed and slightly pursed to one side.",
 "proud": "DELIGHTED PROUD: eyes closed in two happy upward arcs (smiling eyes), brows lifted, the mouth wide open in a happy smile showing pink tongue, chin up.",
 "retry": "ENCOURAGING try-again: eyes bright and warm, brows softly lifted high in the middle, a small reassuring smile with the corners clearly lifted, head tilted a little. Never sad or skeptical.",
 "speak": "SPEAKING: mouth open in a clear round-oval shape with upper teeth and a pink tongue, eyes bright, brows lifted.",
 "mouth_mmm": "SOUND 'mmm': the mouth is fully CLOSED, lips pressed together in ONE straight horizontal line with the corners NOT lifted (neutral, not a smile), and the upper lip slightly tucked, as when humming 'mmm'. Eyes bright and open, brows relaxed, friendly.",
 "mouth_aaa": "SOUND 'aaa': jaw dropped, mouth wide open in a tall oval, upper teeth and pink tongue visible, eyes bright and open, brows lifted.",
 "mouth_ooo": "SOUND 'ooo': lips pushed forward into a small, tight, round 'O' ring, the snout slightly extended, a dark round hole in the middle, eyes bright and open, brows slightly lifted.",
}

def to_alpha(path, min_frac=0.02):
    """Alpha cut-out; drops detached specks (stray floating eyebrows) smaller than min_frac of the body, except on poses whose marks are intended (sparkles, sound waves)."""
    im = _to_alpha(path)
    if any(k in os.path.basename(path) for k in ("pose_celebrate", "pose_model")): return im
    a = np.array(im.getchannel("A")) > 0; lab, n = ndimage.label(a)
    if n > 1:
        sizes = ndimage.sum(a, lab, range(1, n + 1)); keep = [i + 1 for i, z in enumerate(sizes) if z >= min_frac * sizes.max()]
        m = np.isin(lab, keep); al = np.array(im.getchannel("A")); al[~m] = 0; im.putalpha(Image.fromarray(al))
        b = im.getchannel("A").getbbox(); im = im.crop(b)
    return im

def refs():
    def one(v):
        out = f"{D}/ref_{v}.png"
        if not os.path.exists(out):
            generate(STYLE + SAME + EYES + REF[v], out, refs=[f"{OLD}/ref.png"], model="nano-banana-pro")
        return v
    with ThreadPoolExecutor(4) as ex: list(map(print, ex.map(one, REF)))

def _gen(kind, table, names):
    ref = f"{D}/ref.png"
    def one(n):
        out = f"{D}/{kind}_{n}_raw.png"
        if not os.path.exists(out):
            tail = "Pose and body language: " if kind == "pose" else "Same full-body seated pose and same side view as the reference; only the face changes. Expression: "
            generate(STYLE + SAME + EYES + tail + table[n], out, refs=[ref], model="nano-banana-pro")
        return n
    with ThreadPoolExecutor(6) as ex: list(map(print, ex.map(one, names or list(table))))

def cut_head(p):
    a = to_alpha(p); w, h = a.size
    return a.crop((0, 0, int(w * 0.94), int(h * 0.50)))

def silhouettes(cell=300):
    names = list(POSES); sh = Image.new("RGB", (cell * len(names), cell), "white")
    for i, n in enumerate(names):
        p = f"{D}/pose_{n}_raw.png"
        if not os.path.exists(p): continue
        im = fit(to_alpha(p), cell, 0.06); m = Image.new("RGBA", im.size, (0, 0, 0, 255)); m.putalpha(im.getchannel("A"))
        bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(m); sh.paste(bg.convert("RGB"), (cell * i, 0))
    sh.save(f"{D}/sheet_silhouettes.png")

def boards():
    names = list(POSES); cell, cols = 480, 4; rows = (len(names) + cols - 1) // cols
    sh = Image.new("RGB", (cell * cols, cell * rows), "white")
    for i, n in enumerate(names):
        p = f"{D}/pose_{n}_raw.png"
        if os.path.exists(p):
            im = fit(to_alpha(p), cell, 0.04); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
            sh.paste(bg.convert("RGB"), (cell * (i % cols), cell * (i // cols)))
    sh.save(f"{D}/sheet_poses.png")
    for n in FACES:
        p = f"{D}/face_{n}_raw.png"
        if os.path.exists(p): cut_head(p).save(f"{D}/face_{n}.png")
    cw, ch, cols = 520, 340, 3; fs = Image.new("RGB", (cw * cols, ch * 3), "white")
    for i, n in enumerate(FACES):
        if os.path.exists(f"{D}/face_{n}.png"):
            im = Image.open(f"{D}/face_{n}.png"); im.thumbnail((cw - 20, ch - 20), Image.LANCZOS)
            bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
            fs.paste(bg.convert("RGB"), (cw * (i % cols) + (cw - im.width) // 2, ch * (i // cols) + (ch - im.height) // 2))
    fs.save(f"{D}/sheet_faces.png")
    fit(to_alpha(f"{D}/ref.png"), 768).save(f"{D}/ref_alpha.png")
    silhouettes()

if __name__ == "__main__":
    a = sys.argv[1:]; cmd = a[0] if a else "build"
    if cmd == "refs": refs()
    elif cmd == "poses": _gen("pose", POSES, a[1:])
    elif cmd == "faces": _gen("face", FACES, a[1:])
    else: boards()
