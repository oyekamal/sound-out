#!/usr/bin/env python3
"""plan-vN.md -> plan.html for the Artifact tool. Usage: build_page.py plan-v3.md [out.html]"""
import re, sys, html, markdown, pathlib

src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "plan.html")
md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"], extension_configs={"toc": {"toc_depth": "2", "permalink": False}})
body = md.convert(src.read_text())
body = re.sub(r"<table>", '<div class="tw"><table>', body).replace("</table>", "</table></div>")
toc = md.toc
page = f"""<title>Read English App Plan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* layout: narrow reading column + a quiet contents rail on wide screens; one column on phones */
:root{{--bg:#f7f8f6;--fg:#1c2430;--mute:#5a6675;--line:#d9dfd9;--accent:#1f4e79;--accent-2:#b8860b;--card:#eef2ee;--code:#e8ece7;
--display:"Fraunces",Georgia,serif;--body:"Source Sans 3","Segoe UI",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#141a20;--fg:#e6e9e4;--mute:#9aa6b2;--line:#2b3540;--accent:#7fb2e5;--accent-2:#e0b24a;--card:#1c242c;--code:#1a2129;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141a20;--fg:#e6e9e4;--mute:#9aa6b2;--line:#2b3540;--accent:#7fb2e5;--accent-2:#e0b24a;--card:#1c242c;--code:#1a2129;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 var(--body);margin:0;padding-block:24px;padding-inline:16px}}
.wrap{{max-width:1120px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr);gap:32px}}
@media(min-width:960px){{.wrap{{grid-template-columns:240px minmax(0,1fr)}}}}
nav{{font-size:14px;align-self:start}}
@media(min-width:960px){{nav{{position:sticky;top:env(safe-area-inset-top,0px);max-height:calc(100vh - 32px);overflow:auto}}}}
nav .toc ul{{list-style:none;padding:0;margin:0}}nav .toc li{{margin:0 0 6px}}nav a{{color:var(--mute);text-decoration:none}}nav a:hover{{color:var(--accent)}}
nav .eyebrow{{font:600 12px/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:0 0 12px}}
main{{min-width:0;max-width:72ch}}
h1,h2,h3,h4{{font-family:var(--display);text-wrap:balance;line-height:1.15;margin:1.6em 0 .5em}}h1{{font-size:2.3rem;margin-top:0}}h2{{font-size:1.6rem;padding-top:.4em;border-top:1px solid var(--line)}}h3{{font-size:1.2rem}}h4{{font-size:1rem;font-family:var(--body);font-weight:600}}
p,li{{max-width:68ch}}a{{color:var(--accent)}}
.tw{{overflow-x:auto;margin:1em 0}}table{{border-collapse:collapse;font-size:14.5px;min-width:100%}}th,td{{border-bottom:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}}th{{font-weight:600;background:var(--card)}}td{{font-variant-numeric:tabular-nums}}
code{{font:14px var(--mono);background:var(--code);padding:1px 5px;border-radius:3px}}pre{{background:var(--code);padding:14px;overflow-x:auto;border-radius:4px}}pre code{{background:none;padding:0}}
blockquote{{margin:1em 0;padding:8px 16px;border-left:3px solid var(--accent-2);color:var(--mute)}}
hr{{border:0;border-top:1px solid var(--line);margin:2em 0}}
.meta{{color:var(--mute);font-size:14px;margin-bottom:24px}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
@media(prefers-reduced-motion:no-preference){{html{{scroll-behavior:smooth}}}}
</style>
<div class="wrap">
<nav><p class="eyebrow">Contents</p>{toc}</nav>
<main>
<p class="meta">Source: <code>{html.escape(src.name)}</code> · gauntlet-looped plan · owner Kamal</p>
{body}
</main>
</div>
"""
out.write_text(page); print(out, len(page)//1024, "KB")
