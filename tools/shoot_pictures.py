#!/usr/bin/env python3
"""Real word pictures in the lessons, at 360x640 (Track A): three shots into store/android-test/pictures-in-app/.

  python3 tools/shoot_pictures.py [--port 5394]

  1_first_sound.png   L1.01 "What sound does it start with?" with the real picture and the three answer cards
  2_blend_pictures.png L1.01 "Which word do the sounds make?" with a real picture on each card, or speaker-only cards when ANY option has no safe picture
  3_listen_story.png   L1.01 Listen & Talk: the story scenes, real art after each chunk
  (4_listen_question.png is a bonus: the non-graded "say your answer out loud" step)
Asserts: no console errors, no HTTP >= 400 (no missing image), every shown picture really loaded (naturalWidth > 0),
no picture card changes size between the first-sound screen and its answer cards. Exit 0 = green.
"""
import socket, subprocess, sys, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
PORT = int(ARG("--port", "5394"))
OUT = ROOT / "store/android-test/pictures-in-app"; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*.png"): f.unlink()
problems, errors = [], []
LOADED = "[...document.querySelectorAll('.picture img')].every(i => i.complete && i.naturalWidth > 0)"


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


def main():
    dist = Path(tempfile.mkdtemp(prefix="so-pic-"))
    subprocess.run(["npx", "vite", "build", "--base=/", "--outDir", str(dist), "--emptyOutDir", "--logLevel", "error"], cwd=ROOT / "app", check=True)
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(dist)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if port_open(PORT): break
        time.sleep(0.3)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            ctx = br.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=2)
            pg = ctx.new_page(); pg.set_default_timeout(8000)
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("response", lambda r: errors.append(f"HTTP {r.status} {r.url}") if r.status >= 400 else None)
            pg.goto(f"http://localhost:{PORT}/?fast"); pg.wait_for_selector(".whocard"); pg.click(".whocard[data-track=A]"); pg.wait_for_selector(".sitting", timeout=25000)
            got, widths, deadline = set(), [], time.time() + 330
            while time.time() < deadline and len(got) < 2:
                if pg.locator(".pics.one .picture").count():
                    w = pg.evaluate("document.querySelector('.pics.one .picture').getBoundingClientRect().width"); widths.append(round(w))
                visible_opts = pg.locator(".l1-opts:not(.pending) .opt-pick:not([disabled])")
                if visible_opts.count() >= 3:
                    if "first" not in got and pg.locator(".pics.one .picture").count() and pg.locator(".l1-opts .picture").count() == 0:
                        pg.wait_for_function(LOADED); time.sleep(0.3); pg.screenshot(path=str(OUT / "1_first_sound.png")); got.add("first")
                    elif "blend" not in got and (pg.locator(".l1-opts .picture").count() >= 2 or pg.locator(".l1-opts.speaker-only").count()):
                        n_pic, n_opt = pg.locator(".l1-opts .picture").count(), pg.locator(".l1-opts .opt").count()
                        if n_pic not in (0, n_opt): problems.append(f"blend options mix pictured and picture-less cards ({n_pic} of {n_opt})")
                        if pg.locator(".picture-gap").count(): problems.append("blend screen still shows a .picture-gap")
                        pg.wait_for_function(LOADED); time.sleep(0.3); pg.screenshot(path=str(OUT / "2_blend_pictures.png")); got.add("blend")
                    pg.locator(".l1-opts .opt[data-ok='1'] .opt-pick").first.click(); time.sleep(0.4)
                nb = pg.locator(".foot .next:not([hidden]):not([disabled])")
                if nb.count() and not pg.locator(".l1-opts").count(): nb.click(); time.sleep(0.3)
                time.sleep(0.15)
            for k in ("first", "blend"):
                if k not in got: problems.append(f"never saw the {k} screen with pictures")
            if widths and len(set(widths)) > 1: problems.append(f"picture card changed width: {sorted(set(widths))}")
            # Listen & Talk
            pg.evaluate("() => { window.__so.app.home(); }"); pg.wait_for_selector(".home .node", timeout=8000)
            keys = pg.evaluate("[...document.querySelectorAll('.home .node[data-key]')].map(n => [n.dataset.key, n.textContent.trim()])")
            lk = next((k for k, t in keys if k.startswith("L1.01:") and "Listen" in t), None)
            if not lk: problems.append(f"no Listen node found in {keys[:6]}")
            else:
                pg.evaluate(f"() => {{ window.__so.app.sitting('{lk}'); }}")   # not awaited: a sitting runs until its end screen
                seen_scene = seen_q = False; deadline = time.time() + 120
                try:   # the Listen intro starts by itself: it must carry one big, labelled play button under the scene
                    pg.wait_for_selector(".intro-hero ~ .startplay", timeout=8000); pg.wait_for_function(LOADED); pg.screenshot(path=str(OUT / "0_listen_intro.png"))
                    bb = pg.locator(".startplay").bounding_box()
                    if not pg.locator(".startplay").get_attribute("aria-label"): problems.append("listen intro: play button has no aria-label")
                    if bb["width"] < 64 or bb["height"] < 64: problems.append(f"listen intro: play button too small {bb}")
                except Exception as e: problems.append(f"listen intro: no play button under the scene ({e.__class__.__name__})")
                while time.time() < deadline and not seen_q:
                    if not seen_scene and pg.locator(".pics .picture").count() >= 3:
                        pg.wait_for_function(LOADED); time.sleep(0.3); pg.screenshot(path=str(OUT / "3_listen_story.png")); seen_scene = True
                    if pg.locator(".talk").count():
                        time.sleep(0.4); pg.screenshot(path=str(OUT / "4_listen_question.png")); seen_q = True
                        pose = pg.evaluate("window.__so.tilo.state.pose")
                        if pose != "listening": problems.append(f"listen question: Tilo pose is {pose}, want listening")
                        # the scene now sits ABOVE the say-it-out-loud cue (it used to be below it), and the cue is a big mic glyph
                        if not pg.locator(".pics.scene .picture img").count(): problems.append("listen question: no scene picture")
                        elif not pg.locator(".pics.scene ~ .talk .talk-mic svg").count(): problems.append("listen question: scene is not above the mic cue")
                        else:
                            sy, ty = pg.evaluate("[document.querySelector('.pics.scene').getBoundingClientRect().top, document.querySelector('.talk').getBoundingClientRect().top]")
                            if not sy < ty: problems.append(f"listen question: scene (top {sy:.0f}) is not above the mic cue (top {ty:.0f})")
                            if pg.evaluate("document.querySelector('.sitting').getBoundingClientRect().height > window.innerHeight + 1"): problems.append("listen question overflows 360x640")
                        if pg.locator(".answer").count(): problems.append("graded picture answers still on the Listen question")
                        break
                    nb = pg.locator(".foot .next:not([hidden]):not([disabled])")
                    if nb.count(): nb.click(); time.sleep(0.3)
                    time.sleep(0.15)
                if not seen_scene: problems.append("never saw the story scenes")
                if not seen_q: problems.append("never saw the Listen question step")
            br.close()
    finally:
        server.terminate()
    problems.extend(f"console/http error: {e}" for e in errors)
    print("\n".join(problems) if problems else "PICTURE SHOTS GREEN")
    sys.exit(1 if problems else 0)


main()
