#!/usr/bin/env python3
"""Redraw Tilo's talking mouths (mid, aaa = cheerful open D/smile shapes; mmm = closed smile line) with PIL.
Same canvas (78x74 @2x, 39x37 @1x), same brown outline + pink inside as the original cut-out art, stalk under the nose kept.
  python3 tools/gen_tilo_mouths.py
"""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter
OUT = Path(__file__).resolve().parent.parent / "app/public/img/tilo"
S = 8; W, H = 78, 74
BROWN = (125, 62, 27, 255); INSIDE = (104, 48, 24, 255); PINK = (238, 128, 116, 255)

def bez(p0, p1, p2, n=60):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0], (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/n for i in range(n+1)]]

def sc(pts): return [(x*S, y*S) for x, y in pts]

def canvas(): return Image.new("RGBA", (W*S, H*S), (0, 0, 0, 0))

def stalk(d, y1):
    d.line(sc([(39, 5), (39, y1)]), fill=BROWN, width=5*S); 
    for y in (5, y1): d.ellipse([(39-2.5)*S, (y-2.5)*S, (39+2.5)*S, (y+2.5)*S], fill=BROWN)

def line_curve(d, pts, w):
    d.line(sc(pts), fill=BROWN, width=int(w*S), joint="curve")
    for x, y in (pts[0], pts[-1]): d.ellipse([(x-w/2)*S, (y-w/2)*S, (x+w/2)*S, (y+w/2)*S], fill=BROWN)

def smile():
    im = canvas(); d = ImageDraw.Draw(im)
    stalk(d, 32); line_curve(d, bez((13, 33), (39, 52), (65, 33)), 5)
    return im

def dmouth(depth, tongue, rx=27, y0=26):
    """a rounded D: slightly sagging top edge, full superellipse belly, rounded corners (turned up)"""
    top = [(39 + rx*u, y0 + 3.5*(1-u*u)) for u in [i/40*2-1 for i in range(41)]]
    bot = [(39 + rx*u, y0 + depth*(1-abs(u)**2.6)**(1/2.6)) for u in [1-i/60*2 for i in range(61)]]
    m = Image.new("L", (W*S, H*S), 0); ImageDraw.Draw(m).polygon(sc(top + bot), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.2*S)).point(lambda v: 255 if v > 128 else 0)   # round the corners
    im = canvas(); d = ImageDraw.Draw(im); stalk(d, y0 + 2)
    im.paste(Image.new("RGBA", im.size, BROWN), (0, 0), m)
    inner = m.filter(ImageFilter.MinFilter(4*S + 1))                                         # uniform ~2px outline
    im.paste(Image.new("RGBA", im.size, INSIDE), (0, 0), inner)
    t = Image.new("L", im.size, 0); by = y0 + depth + 1
    ImageDraw.Draw(t).ellipse([(39-tongue[0])*S, (by-tongue[1]*2)*S, (39+tongue[0])*S, by*S], fill=255)
    t = ImageChops.multiply(t, inner); im.paste(Image.new("RGBA", im.size, PINK), (0, 0), t)
    return im

def save(im, n):
    big = im.resize((W, H), Image.LANCZOS); small = im.resize((W//2, H//2), Image.LANCZOS)
    big.save(OUT / f"mouth_{n}_2x.webp", lossless=True, quality=100); small.save(OUT / f"mouth_{n}_1x.webp", lossless=True, quality=100)

save(smile(), "mmm"); save(dmouth(17, (12, 5)), "mid"); save(dmouth(33, (18, 9)), "aaa")
print("mouths written")
