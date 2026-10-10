#!/usr/bin/env python3
"""Tilo CUTE (round 4): round-1 Kapi style, capybara cues, teal ear-bead + satchel. Outputs design/character/tilo-cute/"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kie_img import generate
from gen_character import to_alpha, fit
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design", "character", "tilo-cute")
KAPI = os.path.join(D, "..", "concepts", "kapi", "hero_raw.png")
STYLE = ("Flat vector character illustration, very cute chibi style like the reference image: soft round chubby shapes, NO outlines, solid flat colour fills with one slightly darker flat shade underneath, "
 "BIG round shiny eyes (white with large dark brown pupil and a white highlight), small warm smile, soft pink blush on the cheeks, big head and small round body, plain pure white background, one character centered with generous margin, full body visible, "
 "absolutely no text, no letters, no numbers, no speech bubbles. ")
CAP = ("The character is TILO, a baby capybara: same sandy-brown #C98B55 and cream #F6E3C4 palette as the reference, slightly squarer rounded-rectangle muzzle with a big soft dark nose and two tiny nostrils, tiny round ears set HIGH on top of the head, "
 "a round barrel body, tiny rounded paws, standing upright. Signature items: ONE small teal #1FA6A0 round bead tied on the LEFT ear (viewer's right), and a small cream-and-teal satchel with a strap across the chest (no scarf). ")
VARS = {"a": "Extra chubby, head very wide and round, eyes very large and set wide apart, muzzle a soft rounded square.",
        "b": "Head slightly taller and rounder, eyes big and a little lower on the face, muzzle a soft rounded square with a big nose, small gentle closed smile with a tiny blush, little teeth not shown.",
        "c": "Head wide and squashed-round like a mochi, eyes huge and glossy with two highlights, muzzle small and square with a big nose, tiny pink tongue-less smile, rosy cheeks bigger."}
FH = "HEAD ONLY portrait: draw only the head with both ears and the teal ear-bead, ending at the chin; NO body, NO neck, NO shoulders, NO strap, NO hair tufts, no marks under the chin; whole head fully inside the frame with white margin all around. Expression: "
KEEP = "Keep EXACTLY the same character as the reference: same shape, colours, face, teal ear-bead and satchel. Only the pose or expression changes. "
POSES = {"speaking": "mouth open in a gentle round shape, one paw raised in a friendly explaining gesture",
 "listening": "head tilted a little, one paw cupped at the teal-beaded ear, eyes wide and attentive, mouth in a small smile",
 "pointing": "one arm stretched out pointing to the viewer's right, looking that way, encouraging smile",
 "thinking": "one paw on the chin, eyes looking up and to the side, small mouth, no extra marks around the head",
 "trying": "head tilted warmly, big warm smile, one paw raised in a small fist 'you can do it' cheer",
 "celebrating": "both paws raised high, big open happy smile with eyes joyfully closed arches, three tiny flat sparkle stars around",
 "waiting": "standing relaxed with both paws clasped in front, calm soft smile, eyes open, patient"}
FACES = {"happy": "big happy open smile, eyes round and shiny", "listening": "attentive wide eyes, small closed smile, head tilted slightly",
 "thinking": "eyes looking up to one side, small neutral mouth, one eyebrow slightly raised",
 "encouraging": "warm gentle smile, soft eyes, head tilted", "proud": "eyes happily closed as arches, big smile, chin slightly up",
 "speaking": "mouth open mid-speech, eyes round and bright",
 "mmm": "mouth closed, a clear small wide closed-lips smile line (like humming mmm), cheeks stay normal with the same plain flat pink blush, no puffed or smudged cheeks", "aaa": "mouth wide open tall oval showing pink tongue",
 "ooo": "mouth a small round O shape, lips pushed forward"}
def ref_path(v): return f"{D}/ref_{v}_raw.png"
def mk_ref(v):
    if not os.path.exists(ref_path(v)):
        generate(STYLE + CAP + VARS[v] + " Standing neutral pose facing the viewer, slight smile.", ref_path(v), refs=[KAPI], model="nano-banana-2")
def mk(kind, name, text, ref, aspect="1:1"):
    out = f"{D}/{kind}_{name}_raw.png"
    if not os.path.exists(out):
        generate(STYLE + KEEP + text + ".", out, refs=[ref], model="nano-banana-2")
    return out
if __name__ == "__main__":
    step = sys.argv[1]
    if step == "refs":
        with ThreadPoolExecutor(3) as ex: list(ex.map(mk_ref, VARS))
    else:
        ref = f"{D}/ref_raw.png"; jobs = []
        if step in ("poses", "all"): jobs += [("pose", k, "Pose: " + v) for k, v in POSES.items()]
        if step in ("faces", "all"): jobs += [("face", k, FH + v) for k, v in FACES.items()]
        if step in ("icon", "all"): jobs += [("icon", "head", "Close-up of ONLY the head, big, filling the frame, with the teal ear-bead clearly visible, happy smile, eyes big")]
        if step in ("redo",):
            jobs = [(a.split(":")[0], a.split(":")[1], (("Pose: " + POSES[a.split(":")[1]]) if a.startswith("pose") else FH + FACES[a.split(":")[1]])) for a in sys.argv[2:]]
            for a in sys.argv[2:]:
                p = f"{D}/{a.split(':')[0]}_{a.split(':')[1]}_raw.png"
                if os.path.exists(p): os.remove(p)
        with ThreadPoolExecutor(6) as ex: list(ex.map(lambda j: mk(*j, ref), jobs))
    print("ok")
