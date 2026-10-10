#!/usr/bin/env python3
"""Android icons (adaptive + legacy + round), splash screens, Play icon and feature graphic from the approved cute Tilo art.

  python3 tools/make_tilo_icons.py

Approach copied from the Urdu Qaida app (make_icons.py / make_store.py), with the art swapped: the icon is Tilo's head on
the app's accent blue. Text on the feature graphic is real PIL text in the bundled Fredoka font, never model-drawn."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{R}/tools")
import numpy as np
from tilo_cutout import cutout
SRC = f"{R}/design/character/tilo-cute"; RES = f"{R}/app/android/app/src/main/res"
BLUE, BLUE2, PAPER, CREAM, INK = "#2F6F8F", "#3E86A9", "#F6F1E7", "#FFF3D6", "#24211D"
FRED = f"{R}/store/fonts/Fredoka-Bold.ttf"; FRED_M = f"{R}/store/fonts/Fredoka-Medium.ttf"


def load(name):
    im = Image.fromarray(cutout(f"{SRC}/{name}_raw.png"), "RGBA"); return im.crop(im.getbbox())


HEAD = load("icon_head"); IDLE = load("pose_waiting"); POINT = load("pose_pointing"); CELEB = load("pose_celebrating")


def fit(im, w=None, h=None):
    s = (w / im.width) if w else (h / im.height); return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def shadow(im, off, blur, alpha):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)); s = Image.new("RGBA", im.size, (20, 40, 60, 0)); s.putalpha(a); return s


def head_on(size, head_frac, bg=True, dy=0.02):
    """Square canvas, head centred (slightly low: the ears add visual weight on top), soft shadow so it lifts off the blue."""
    c = Image.new("RGBA", (size, size), BLUE if bg else (0, 0, 0, 0)); h = fit(HEAD, w=round(size * head_frac))
    x, y = (size - h.width) // 2, (size - h.height) // 2 + round(size * dy); sh = shadow(h, 0, size * .012, .35)
    c.alpha_composite(sh, (x, y + round(size * .015))); c.alpha_composite(h, (x, y)); return c


def mask_round(im, radius_frac=None):
    s = im.width; m = Image.new("L", (s * 4, s * 4), 0); d = ImageDraw.Draw(m)
    if radius_frac is None: d.ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    else: d.rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), radius=int(s * 4 * radius_frac), fill=255)
    m = m.resize((s, s), Image.LANCZOS); out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out


def splash(w, h):
    im = Image.new("RGB", (w, h), PAPER); d = ImageDraw.Draw(im); u = min(w, h)
    t = fit(IDLE, h=round(u * (.50 if w < h else .52)))
    title = ImageFont.truetype(FRED, round(u * .105)); sub = ImageFont.truetype(FRED_M, round(u * .052))
    gap = round(u * .04); block = t.height + gap + round(u * .105) + round(u * .07)
    y0 = (h - block) // 2; rgba = im.convert("RGBA"); rgba.alpha_composite(t, ((w - t.width) // 2, y0)); im = rgba.convert("RGB"); d = ImageDraw.Draw(im)
    ty = y0 + t.height + gap + round(u * .05); d.text((w // 2, ty), "Sound Out", font=title, fill=BLUE, anchor="mm")
    d.text((w // 2, ty + round(u * .085)), "Read English", font=sub, fill="#6F675C", anchor="mm"); return im


def tile(ch, size, colour, rot):
    t = Image.new("RGBA", (size + 30, size + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((15, 21, size + 15, size + 21), radius=size // 4, fill=(0, 0, 0, 60)); t = t.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((15, 15, size + 15, size + 15), radius=size // 4, fill=colour, outline="white", width=max(3, size // 20))
    d.text((15 + size // 2, 15 + size // 2 + 2), ch, font=ImageFont.truetype(FRED, int(size * (.55 if len(ch) == 1 else .42))), fill="white", anchor="mm")
    return t.rotate(rot, expand=True, resample=Image.BICUBIC)


def feature():
    W, H = 1024, 500; bg = Image.new("RGB", (W, H), BLUE); px = np.zeros((H, W, 3), np.float32)
    c1, c2 = np.array([0x2F, 0x6F, 0x8F]), np.array([0x41, 0x8D, 0xB0]); gx = np.linspace(0, 1, W)[None, :, None]; gy = np.linspace(0, 1, H)[:, None, None]
    px = c1 * (1 - (gx * .6 + gy * .4)) + c2 * (gx * .6 + gy * .4); im = Image.fromarray(px.astype(np.uint8), "RGB").convert("RGBA")
    for ch, x, y, s, col, r in [("sh", 452, 36, 78, "#F2A93B", -8), ("ee", 905, 40, 74, "#E8664F", 9), ("a", 900, 390, 76, "#4FA35E", -7), ("b", 760, 408, 62, "#8E5BB5", 8)]:
        t = tile(ch, s, col, r); im.alpha_composite(t, (x, y))
    # Tilo, pointing at the title
    p = fit(POINT, h=458); sh = shadow(p, 0, 8, .3); im.alpha_composite(sh, (24, H - p.height - 2 + 8)); im.alpha_composite(p, (24, H - p.height - 6))
    d = ImageDraw.Draw(im); f1 = ImageFont.truetype(FRED, 112)
    while f1.getlength("Sound Out") > 540: f1 = ImageFont.truetype(FRED, f1.size - 2)   # fit the title to the free column
    f2 = ImageFont.truetype(FRED_M, round(f1.size * .53)); f3 = ImageFont.truetype(FRED_M, 31)
    tx = 455
    d.text((tx + 4, 178 + 5), "Sound Out", font=f1, fill=(15, 45, 65, 120), anchor="lm")
    d.text((tx, 178), "Sound Out", font=f1, fill="white", anchor="lm")
    d.text((tx + 3, 262), "Read English", font=f2, fill=CREAM, anchor="lm")
    d.rounded_rectangle((tx + 3, 322, tx + 3 + 392, 322 + 46), radius=23, fill=(255, 255, 255, 235))
    d.text((tx + 3 + 196, 322 + 24), "Phonics for kids and adults", font=f3, fill=BLUE, anchor="mm")
    return im.convert("RGB")


def main():
    os.makedirs(f"{R}/store", exist_ok=True)
    head_on(1024, .66, dy=.02).convert("RGB").save(f"{R}/store/icon-1024.png")
    play = head_on(512, .66, dy=.02).convert("RGB"); play.save(f"{R}/store/icon-512.png")
    for dpi, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        fg_px = px * 108 // 48                                               # adaptive layers are 108dp: 108/48 x the legacy size
        # safe zone = 66dp circle of 108dp (61%); head width 54% keeps ears/cheeks inside it on every mask shape
        head_on(fg_px, .54, bg=False, dy=.0).save(f"{RES}/mipmap-{dpi}/ic_launcher_foreground.png")
        leg = head_on(px * 4, .72); leg_sq = mask_round(leg, .22).resize((px, px), Image.LANCZOS); leg_sq.save(f"{RES}/mipmap-{dpi}/ic_launcher.png")
        mask_round(head_on(px * 4, .66)).resize((px, px), Image.LANCZOS).save(f"{RES}/mipmap-{dpi}/ic_launcher_round.png")
    open(f"{RES}/values/ic_launcher_background.xml", "w").write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{BLUE}</color>\n</resources>')
    for dpi, (pw, ph) in {"mdpi": (320, 480), "hdpi": (480, 800), "xhdpi": (720, 1280), "xxhdpi": (960, 1600), "xxxhdpi": (1280, 1920)}.items():
        splash(pw, ph).save(f"{RES}/drawable-port-{dpi}/splash.png", optimize=True); splash(ph, pw).save(f"{RES}/drawable-land-{dpi}/splash.png", optimize=True)
    splash(480, 320).save(f"{RES}/drawable/splash.png", optimize=True)
    feature().save(f"{R}/store/feature-graphic.png", optimize=True)
    # 48 px launcher look on light and dark wallpapers (round + squircle + adaptive-on-circle), for eyeballing
    prev = Image.new("RGB", (2 * 360, 150), "white"); 
    for i, wp in enumerate([(235, 232, 225), (22, 24, 30)]):
        panel = Image.new("RGB", (360, 150), wp); x = 20
        for shape in ("square", "round", "adaptive-circle"):
            if shape == "square": ic = Image.open(f"{RES}/mipmap-xxxhdpi/ic_launcher.png").resize((48, 48), Image.LANCZOS)
            elif shape == "round": ic = Image.open(f"{RES}/mipmap-xxxhdpi/ic_launcher_round.png").resize((48, 48), Image.LANCZOS)
            else:
                fg = Image.open(f"{RES}/mipmap-xxxhdpi/ic_launcher_foreground.png"); a = Image.new("RGBA", fg.size, BLUE); a.alpha_composite(fg)
                ic = mask_round(a).resize((48, 48), Image.LANCZOS)
            panel.paste(ic, (x, 50), ic); x += 110
        prev.paste(panel, (i * 360, 0))
    prev.save(os.environ.get("ICON_PREVIEW", "/tmp/icon_preview.png")); print("done")


if __name__ == "__main__":
    main()
