#!/usr/bin/env python3
"""Build design/character/round1.html: blind A/B of each concept vs a Duolingo ABC cast crop (bar_crops/, gitignored with bar/).
Anonymous images go to blind/, answer key to round1_key.js/.json (loaded by the reveal view only)."""
import json, os, random
from PIL import Image
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design", "character"))
os.makedirs("blind", exist_ok=True)
NAMES = ["kapi", "tola", "noo", "axi", "lumo"]
LINE = {"kapi": "Capybara: the calmest animal there is, loved by adults.", "tola": "Tortoise: patient by nature, waiting is its virtue.",
        "noo": "Cloud: no species, culture or age; floats, never talks down.", "axi": "Axolotl: permanent smile, gill frills read as listening ears.",
        "lumo": "Lantern: the light-comes-on moment of reading; an object, so culture-neutral."}
TILE = {"kapi": "#7FD3CC", "tola": "#F7D58A", "noo": "#FFB0A0", "axi": "#B9A3F0", "lumo": "#8EC8F7"}
BAR = ["d1", "d6", "d4", "d8", "d3"]
rnd = random.Random(20261009); key = {}; order = list(range(5)); rnd.shuffle(order)
for slot, i in enumerate(order):
    n = NAMES[i]; hero = Image.open(f"concepts/{n}/hero.png").convert("RGBA")
    tile = Image.new("RGBA", (512, 512), TILE[n]); h = hero.copy(); h.thumbnail((440, 440), Image.LANCZOS)
    tile.alpha_composite(h, ((512 - h.width) // 2, (512 - h.height) // 2)); ours = tile.convert("RGB")
    theirs = Image.open(f"bar_crops/{BAR[i]}.png").convert("RGB").resize((512, 512))
    ours_left = rnd.random() < 0.5
    l, r = (ours, theirs) if ours_left else (theirs, ours)
    l.save(f"blind/p{slot+1}_A.jpg", quality=90); r.save(f"blind/p{slot+1}_B.jpg", quality=90)
    key[f"p{slot+1}"] = {"ours": "A" if ours_left else "B", "concept": n, "line": LINE[n], "bar_crop": BAR[i]}
json.dump(key, open("round1_key.json", "w"), indent=1)
open("round1_key.js", "w").write("window.KEY=" + json.dumps(key) + ";")
rows = "".join(f'<section><h2>Pair {s}</h2><div class="pair"><figure><img src="blind/p{s}_A.jpg"><figcaption>A</figcaption></figure>'
               f'<figure><img src="blind/p{s}_B.jpg"><figcaption>B</figcaption></figure></div>'
               f'<div class="vote">Which one would you want teaching you to read? <button onclick="v({s},\'A\')">A</button> <button onclick="v({s},\'B\')">B</button> <span id="v{s}"></span></div>'
               f'<div class="rev" id="r{s}"></div></section>' for s in range(1, 6))
icons = "".join(f'<figure><img src="concepts/{n}/icon_48.png" width="48" height="48"><figcaption>{n}</figcaption></figure>' for n in NAMES)
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Round 1 blind compare</title><style>
:root{{--bg:#faf6ef;--fg:#2b2a33;--card:#fff;--ac:#2a7f78}}@media(prefers-color-scheme:dark){{:root{{--bg:#17161c;--fg:#eee;--card:#23222b;--ac:#6fd3c9}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.4 system-ui,sans-serif;padding:16px;max-width:900px;margin:auto}}
h1{{font-size:22px}}h2{{font-size:16px;margin:0 0 8px}}section{{background:var(--card);border-radius:14px;padding:14px;margin:14px 0}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}figure{{margin:0;text-align:center}}img{{max-width:100%;border-radius:10px;display:block;margin:auto}}
figcaption{{font-weight:700;margin-top:4px}}button{{font:inherit;padding:6px 16px;border-radius:8px;border:2px solid var(--ac);background:none;color:var(--fg);cursor:pointer}}
.vote{{margin-top:10px}}.rev{{margin-top:8px;font-size:15px}}#reveal{{background:var(--ac);color:#fff;border:0;padding:10px 22px;font-weight:700}}
.icons{{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px}}.icons figure{{font-size:12px}}</style></head><body>
<h1>Round 1: which is ours?</h1><p>Five concepts each sit next to one character from a world-class reading app. Labels are removed and the A/B side is random. Pick a side for each pair, then press reveal.</p>
{rows}
<p><button id="reveal" onclick="reveal()">Reveal answers</button></p><div id="rv"></div>
<section><h2>48 px icons (ours, for the small-size test)</h2><div class="icons">{icons}</div></section>
<script>
const votes={{}};function v(s,x){{votes[s]=x;document.getElementById('v'+s).textContent='you picked '+x}}
function reveal(){{const sc=document.createElement('script');sc.src='round1_key.js';sc.onload=()=>{{let won=0,n=0;
for(const k in KEY){{const s=k.slice(1),e=KEY[k];document.getElementById('r'+s).innerHTML='<b>Ours is '+e.ours+':</b> '+e.concept+' - '+e.line;
if(votes[s]){{n++;if(votes[s]===e.ours)won++}}}}
document.getElementById('rv').textContent=n?('You picked ours '+won+' of '+n+' times.'):'Pick sides first to get a tally.'}};document.body.appendChild(sc)}}
</script></body></html>"""
open("round1.html", "w").write(html); print("ok")
