#!/usr/bin/env python3
"""Tilo in the app at 360x640: Playwright screenshots of every state on Track A, and Track B with no mascot.

  python3 tools/shoot_tilo.py [--port 5393] [--out store/android-test/tilo-in-app]

Serves a static build (vite build) on its own port, plays a real Track A lesson at normal speed and waits for each
state to be real before shooting: speaking (mid-flap, mouths differ between shots), listening, celebrating,
encouraging, idle (idle ladder, ?idlefast). Then Track B: asserts Tilo is hidden. Also asserts that Tilo never
overlaps a button / option / input / link on the screens it visits. Exit 0 = green.
"""
import socket, subprocess, sys, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
PORT = int(ARG("--port", "5393"))
OUT = ROOT / ARG("--out", "store/android-test/tilo-in-app"); OUT.mkdir(parents=True, exist_ok=True)
problems = []
for f in OUT.glob("*.png"): f.unlink()
OVERLAP = """() => { const hit = (a, b) => b.left < a.right && b.right > a.left && b.top < a.bottom && b.bottom > a.top; const bad = [];
  const live = [...document.querySelectorAll('button, a, input, textarea, .opt-pick, [role=button], canvas')].filter(el => !el.closest('.tilo') && el.offsetParent !== null && el.getBoundingClientRect().width && getComputedStyle(el).visibility !== 'hidden');
  const t = document.querySelector('.tilo');
  if (t && !t.hidden) { const r = t.getBoundingClientRect(); for (const el of live) if (hit(r, el.getBoundingClientRect())) bad.push('tilo~' + (el.className || el.tagName)); }
  const ear = document.getElementById('ear');   // the fixed ear button must never sit on another control or the header pill
  if (ear && !ear.hidden) { const r = ear.getBoundingClientRect(); for (const el of live) if (el !== ear && hit(r, el.getBoundingClientRect())) bad.push('ear~' + (el.className || el.tagName)); }
  return bad; }"""


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


def state(page): return page.evaluate("({...window.__so.tilo.state, tier: window.__so.teacher.state.tier})")


def wait_state(page, pred, what, secs=25):
    end = time.time() + secs
    while time.time() < end:
        s = state(page)
        if pred(s): return s
        time.sleep(0.05)
    problems.append(f"never saw: {what} (last {state(page)})"); return None


def onboard(page, track):
    page.wait_for_selector(".whocard"); page.click(f".whocard[data-track={track}]")
    page.wait_for_selector(".sitting", timeout=25000)


def main():
    dist = Path(tempfile.mkdtemp(prefix="so-tilo-"))
    subprocess.run(["npx", "vite", "build", "--base=/", "--outDir", str(dist), "--emptyOutDir", "--logLevel", "error"], cwd=ROOT / "app", check=True)
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(dist)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if port_open(PORT): break
        time.sleep(0.3)
    errors = []
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            def newpage(q=""):
                ctx = br.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=2)
                pg = ctx.new_page(); pg.set_default_timeout(8000)
                pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                pg.on("response", lambda r: errors.append(f"HTTP {r.status} {r.url}") if r.status >= 400 else None)
                pg.on("pageerror", lambda e: errors.append(str(e)))
                pg.goto(f"http://localhost:{PORT}/{q}"); return pg
            def shot(pg, name):
                pg.screenshot(path=str(OUT / f"{name}.png"))
                bad = pg.evaluate(OVERLAP)
                if bad: problems.append(f"Tilo overlaps {bad} on {name}")
            # ---- Track A, real speed
            pg = newpage(); onboard(pg, "A")
            # one CLOSED frame (mmm), one OPEN frame (aaa) and the middle one (mid): the flap must visibly alternate. Each frame is checked
            # (the mouth state must be the same before and after the screenshot, the flap changes every ~100 ms) and cropped into mouth_zoom.png
            from PIL import Image; import io
            frames = {}
            for want, name in (("mmm", "A_speaking_closed_mmm"), ("aaa", "A_speaking_open_aaa"), ("mid", "A_speaking_mid")):
                if not wait_state(pg, lambda s: s["pose"] == "speaking", "speaking pose", 12): break
                pg.evaluate(f"window.__so.tilo.hold('{want}')"); time.sleep(0.15)
                box = pg.evaluate("(() => { const r = document.querySelector('.tilo-stage').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })()")
                png = pg.screenshot(); (OUT / f"{name}.png").write_bytes(png); frames[want] = (png, box)
                if pg.evaluate("[...document.querySelectorAll('.tilo-mouth')].filter(m => !m.hidden).map(m => m.dataset.mouth).join()") != want: problems.append(f"frozen mouth is not {want}")
                pg.evaluate("window.__so.tilo.hold(null)"); time.sleep(0.25)
            if "mmm" in frames and "aaa" in frames and "mid" in frames:
                tiles = []
                for k in ("mmm", "mid", "aaa"):
                    png, (x, y, w, h) = frames[k]; im = Image.open(io.BytesIO(png)); f = 2   # the shot is at device scale 2
                    face = im.crop((int((x + w * .12) * f), int((y + h * .02) * f), int((x + w * .88) * f), int((y + h * .50) * f)))
                    tiles.append(face.resize((face.width * 2, face.height * 2), Image.LANCZOS))   # 2 x 2 = 4x css px
                strip = Image.new("RGB", (sum(t.width for t in tiles) + 12 * (len(tiles) - 1), tiles[0].height), (246, 241, 231)); xx = 0
                for t in tiles: strip.paste(t, (xx, 0)); xx += t.width + 12
                strip.save(OUT / "mouth_zoom.png")
                a, b_ = Image.open(io.BytesIO(frames["mmm"][0])).convert("RGB"), Image.open(io.BytesIO(frames["aaa"][0])).convert("RGB")
                from PIL import ImageChops
                if not ImageChops.difference(a, b_).getbbox(): problems.append("closed and open speaking frames are identical")
            else: problems.append(f"missing speaking frames, got {sorted(frames)}")
            bad = pg.evaluate(OVERLAP)
            if bad: problems.append(f"Tilo overlaps {bad} on speaking")
            wait_state(pg, lambda s: s["pose"] == "listening", "listening after the prompt", 40); time.sleep(0.2); shot(pg, "A_listening")
            pg.evaluate("window.__so.teacher.right({kind:'pick'})")
            if wait_state(pg, lambda s: s["pose"] == "celebrating", "celebrating", 3): time.sleep(0.3); shot(pg, "A_celebrating")
            time.sleep(2.5)
            pg.evaluate("window.__so.teacher.wrong({first:true, model:[]})")
            if wait_state(pg, lambda s: s["pose"] == "encouraging", "encouraging", 3): time.sleep(0.25); shot(pg, "A_encouraging")
            n_missing = pg.evaluate("window.__so.missing.length")
            if n_missing: problems.append(f"missing audio {pg.evaluate('window.__so.missing')}")
            # ---- idle ladder
            pg = newpage("?idlefast"); onboard(pg, "A")
            # at tier 3 the idle ladder shows its own hints on purpose (a yellow nudge ring on a card, a ring on the ear): shoot that as A_idle_hint,
            # then clear the hints and shoot the calm idle state as A_idle (that one must have no ring at all)
            if wait_state(pg, lambda s: s["tier"] >= 3 and s["pose"] == "idle", "idle pose on the idle ladder", 60):
                pg.wait_for_function("[...document.querySelectorAll('.nudge, .ear.attn')].some(e => +(getComputedStyle(e).outlineColor.match(/[\\d.]+/g)[3] ?? 1) > .35)", timeout=6000)   # shoot at the halo's peak (it pulses)
                shot(pg, "A_idle_hint"); pg.evaluate("window.__so.teacher.clearHints()"); time.sleep(0.5); shot(pg, "A_idle")
                if pg.evaluate("document.querySelector('.nudge, .ear.attn')"): problems.append("a hint ring is still on after clearHints")
            # ---- Home (Tilo in the hero) and the end-of-sitting hero
            pg.evaluate("window.__so.app.home()"); pg.wait_for_selector(".home .tilo-slot .tilo"); time.sleep(0.5)
            pg.screenshot(path=str(OUT / "A_home.png"))
            # ---- Track B: no mascot anywhere
            pg = newpage(); onboard(pg, "B"); time.sleep(1.5)
            vis = pg.evaluate("[...document.querySelectorAll('.tilo')].filter(e => !e.hidden && e.offsetParent !== null).length")
            if vis: problems.append("Track B shows Tilo")
            pg.screenshot(path=str(OUT / "B_no_mascot.png"))
            pg.evaluate("window.__so.app.home()"); pg.wait_for_selector(".home"); time.sleep(0.5)
            if pg.evaluate("[...document.querySelectorAll('.tilo')].filter(e => !e.hidden && e.offsetParent !== null).length"): problems.append("Track B home shows Tilo")
            pg.screenshot(path=str(OUT / "B_home_no_mascot.png"))
            br.close()
    finally:
        server.terminate()
    for e in errors: problems.append(f"console error: {e}")
    print("\n".join(problems) if problems else "TILO SHOTS GREEN")
    sys.exit(1 if problems else 0)


main()
