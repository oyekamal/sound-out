#!/usr/bin/env python3
"""Build store/review/review.html from store/review/index.json (one figure per shot)."""
import html, json, pathlib

HERE = pathlib.Path(__file__).parent
shots = json.loads((HERE / "index.json").read_text())

sections = []
for s in shots:
    if s["section"] not in sections:
        sections.append(s["section"])

def fig(s):
    miss = s.get("note", "").startswith("COULD NOT REACH")
    t = s.get("track", "")
    img = "" if miss else f'<button class="zoom" type="button" aria-label="Enlarge {html.escape(s["title"])}"><img src="{html.escape(s["file"])}" alt="{html.escape(s["title"])}" loading="lazy" width="412" height="915"></button>'
    return (f'<figure class="shot{" miss" if miss else ""}" data-track="{html.escape(t if t in ("A","B") else "")}">{img}'
            f'<figcaption><span class="tag t{t if t in ("A","B") else ""}">{"Child · Tilo" if t=="A" else "Grown-up" if t=="B" else "Both tracks"}</span>'
            f'<b>{html.escape(s["title"])}</b><span>{html.escape(s.get("note",""))}</span></figcaption></figure>')

body = "".join(
    f'<section id="s{i}"><h2>{html.escape(sec)} <small>{sum(1 for s in shots if s["section"]==sec)}</small></h2>'
    f'<div class="grid">{"".join(fig(s) for s in shots if s["section"]==sec)}</div></section>'
    for i, sec in enumerate(sections))
nav = "".join(f'<a href="#s{i}">{html.escape(sec)}</a>' for i, sec in enumerate(sections))


missing = sum(1 for s in shots if s.get("note","").startswith("COULD NOT REACH"))
page = (HERE / "template.html").read_text()
page = page.replace("{{NAV}}", nav).replace("{{BODY}}", body).replace("{{COUNT}}", str(len(shots)-missing)).replace("{{MISSING}}", str(missing))
(HERE / "review.html").write_text(page)
print(f"review.html: {len(shots)} shots, {missing} unreachable, {len(sections)} sections")
