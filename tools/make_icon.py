#!/usr/bin/env python3
"""Dedicated Tilo app icon (not a crop): simplified side-profile head, 6 big flat shapes, teal bead as the accent, solid warm background.
Drawn as vectors at 1024 and downsampled -> design/character/tilo/icon_{1024,192,96,48}.png and icon_strip.png (all sizes on light/dark/white)."""
import os
from PIL import Image, ImageDraw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design", "character", "tilo")
S = 2048  # supersample, final 1024
BG = (255, 214, 107); BROWN = (176, 100, 58); DARK = (122, 71, 44); CREAM = (240, 214, 168)
NOSE = (84, 46, 32); TEAL = (23, 166, 160); WHITE = (255, 255, 255); INK = (52, 30, 22)

def draw():
    k = S / 1024; P = lambda *v: [int(x * k) for x in v]
    im = Image.new("RGB", (S, S), BG)
    def layer(fn):
        l = Image.new("RGB", (S, S), BG); fn(ImageDraw.Draw(l)); return l
    head = Image.new("L", (S, S), 0); ImageDraw.Draw(head).rounded_rectangle(P(50, 330, 985, 900), radius=int(190 * k), fill=255)
    def body(d):
        d.rectangle((0, 0, S, S), fill=BROWN)
        d.ellipse(P(-200, 120, 1300, 470), fill=DARK)                      # darker head top
        d.rounded_rectangle(P(0, 560, 480, 940), radius=int(150 * k), fill=CREAM)   # muzzle
        d.rounded_rectangle(P(0, 300, 400, 600), radius=int(130 * k), fill=NOSE)    # nose pad
        d.ellipse(P(90, 400, 170, 470), fill=(40, 20, 14)); d.ellipse(P(250, 400, 330, 470), fill=(40, 20, 14))
        d.arc(P(110, 640, 410, 800), 25, 155, fill=INK, width=int(24 * k))  # warm smile
        d.ellipse(P(560, 480, 770, 690), fill=WHITE); d.ellipse(P(585, 505, 750, 670), fill=INK)  # eye
        d.ellipse(P(640, 530, 705, 595), fill=WHITE); d.ellipse(P(606, 612, 640, 646), fill=WHITE)
        d.arc(P(540, 390, 790, 500), 205, 335, fill=INK, width=int(30 * k))  # lifted brow
    im.paste(layer(body), (0, 0), head)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(P(735, 200, 880, 360), radius=int(70 * k), fill=DARK)   # tiny high ear
    d.ellipse(P(790, 300, 960, 470), fill=TEAL); d.ellipse(P(836, 346, 914, 424), fill=DARK)  # teal bead ring
    return im.resize((1024, 1024), Image.LANCZOS)

if __name__ == "__main__":
    big = draw(); big.save(f"{D}/icon_1024.png")
    sizes = {n: big.resize((n, n), Image.LANCZOS) for n in (192, 96, 48)}
    for n, im in sizes.items(): im.save(f"{D}/icon_{n}.png")
    W = 192 + 96 + 48 + 5 * 24; strip = Image.new("RGB", (W * 3, 192 + 48), "white")
    for j, bgc in enumerate(((255, 255, 255), (245, 240, 230), (30, 30, 36))):
        ImageDraw.Draw(strip).rectangle((j * W, 0, (j + 1) * W, 240), fill=bgc); x = j * W + 24
        for n in (192, 96, 48):
            strip.paste(sizes[n], (x, 24)); x += n + 24
    strip.save(f"{D}/icon_strip.png")
