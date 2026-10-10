#!/usr/bin/env python3
"""contact.py out.png key1 key2 ... : labelled contact sheet from design/pictures/all (labels are for humans/critics only)."""
import sys, os
from PIL import Image, ImageDraw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design/pictures/all")
def sheet(keys, out, cols=8, cell=220):
    rows = (len(keys) + cols - 1) // cols; W = Image.new("RGB", (cols * cell, rows * (cell + 18)), "white"); d = ImageDraw.Draw(W)
    for i, k in enumerate(keys):
        p = f"{D}/{k.replace(':', '-')}.png"
        if not os.path.exists(p): continue
        im = Image.open(p).convert("RGBA").resize((cell - 8, cell - 8)); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        x, y = (i % cols) * cell + 4, (i // cols) * (cell + 18) + 2; W.paste(bg.convert("RGB"), (x, y)); d.text((x + 2, y + cell - 6), f"{i+1}. {k}", fill=(0, 0, 0))
    W.save(out)
if __name__ == "__main__": sheet(sys.argv[2:], sys.argv[1])
