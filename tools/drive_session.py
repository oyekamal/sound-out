#!/usr/bin/env python3
"""Drive the Level 5-7 PRACTICE lessons (session template) with Playwright, mouse only, 390x844.

  python3 tools/drive_session.py [--levels 5,6,7]     # own Vite dev server on :5318
  (also called from tools/drive.py, on its server)
Checks:
  1. every lesson in content/sessions/index.json opens from the Library and shows its first screen (h2 + content)
  2. one full walk per level; across the walks every screen type is reached once:
     warm, word, fluency, prime, text, discuss, write, check
  3. Home shows the "Practice: Levels 5-7" section, locked until the Level 4 check, with a Library entry
  4. no console / page errors; no missing audio asked for (L5-7 clips are placeholders: "audio coming" chips);
     every speaker on a session screen is either a real clip or a visible placeholder
Exit code 0 = green.
"""
import json, socket, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright, Error as PWError

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"; SHOTS = APP / "shots"
SCREENS = ["warm", "word", "fluency", "prime", "text", "discuss", "write", "check"]
WALK = {5: "L5.01", 6: "L6.01", 7: "L7.02"}


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


def run_all(br, problems, url, levels=(5, 6, 7)):
    index = [x for x in json.loads((ROOT / "content/sessions/index.json").read_text()) if x["level"] in levels]
    IDX = json.loads((ROOT / "content/audio_index.json").read_text())["clips"]
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, reduced_motion="reduce")
    page = ctx.new_page(); errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.set_default_timeout(6000)
    page.goto(url)
    page.wait_for_selector(".whocard"); page.click(".whocard[data-track=B]")
    page.wait_for_selector(".langs"); page.click(".onboard .skip")
    # onboarding drops the learner into the first sitting: go home
    page.wait_for_selector(".close, .home");
    if page.locator(".close").count(): page.click(".close")
    page.wait_for_selector(".home .ss-practice", timeout=8000)
    SHOTS.mkdir(exist_ok=True)
    page.screenshot(path=str(SHOTS / "S_00_home-practice.png"), full_page=True)
    if page.locator(".ss-practice .ss-levelcard:not([disabled])").count():
        problems.append("[S] practice levels open before the Level 4 check")
    if not page.locator(".ss-practice .ss-libbtn").count(): problems.append("[S] no Library entry on Home")
    page.click(".ss-practice .ss-libbtn"); page.wait_for_selector(".ss-library")
    page.screenshot(path=str(SHOTS / "S_01_library.png"), full_page=True)

    def check_speakers(lid):
        bad = page.evaluate("""() => [...document.querySelectorAll('.ss-screen [data-key]')].filter(b =>
            !(b.classList.contains('ss-coming') && b.textContent.includes('audio coming')) && !b.classList.contains('ss-voice')).map(b => b.dataset.key)""")
        for k in bad: problems.append(f"[S] {lid}: speaker {k} is neither a clip nor an 'audio coming' placeholder")

    # 1. every lesson's first screen
    first_ok = 0
    for x in index:
        lid = x["id"]
        page.click(f".ss-lesson[data-id='{lid}']")
        try:
            page.wait_for_selector(".ss-screen h2")
            step = page.get_attribute(".ss-screen", "data-step")
            h2 = page.inner_text(".ss-screen h2").strip()
            body = page.inner_text(".ss-screen").strip()
            if step != f"ss-{x['screens'][0]}": problems.append(f"[S] {lid}: first screen {step}, want ss-{x['screens'][0]}")
            elif not h2 or len(body) < 40: problems.append(f"[S] {lid}: first screen looks empty ({h2!r})")
            else: first_ok += 1
            check_speakers(lid)
            if lid.endswith(".01"): page.screenshot(path=str(SHOTS / f"S_{lid}_first.png"))
        except PWError as e:
            problems.append(f"[S] {lid}: did not open ({str(e).splitlines()[0]})")
        page.click(".close"); page.wait_for_selector(".ss-library")
    print(f"[S] first screens ok: {first_ok}/{len(index)}")

    # 2. full walks
    seen = set()
    for lv in levels:
        lid = WALK[lv]
        if not any(x["id"] == lid for x in index): continue
        page.click(f".ss-lesson[data-id='{lid}']"); page.wait_for_selector(".ss-screen")
        shots, n, deadline = set(), 0, time.time() + 240
        while time.time() < deadline:
            try:
                if page.locator(".ss-end").count():
                    page.screenshot(path=str(SHOTS / f"S_{lid}_end.png")); break
                step = page.get_attribute(".ss-screen", "data-step") or ""
                seen.add(step.replace("ss-", ""))
                sig = step + "|" + page.inner_text(".ss-screen h2")
                if sig not in shots:
                    shots.add(sig); n += 1; check_speakers(lid)
                    page.screenshot(path=str(SHOTS / f"S_{lid}_{n:02d}_{step}.png"), full_page=True)
                act(page)
            except PWError:
                time.sleep(0.2)
        else:
            problems.append(f"[S] {lid}: walk timed out on {page.get_attribute('.ss-screen', 'data-step')}")
        print(f"[S] {lid} walk: {n} screens")
        if page.locator(".ss-end .ss-tolib").count(): page.click(".ss-end .ss-tolib"); page.wait_for_selector(".ss-library")
    for s in SCREENS:
        if s not in seen: problems.append(f"[S] screen type never reached in the walks: {s}")
    tr = page.evaluate("window.__so.trace"); missing = page.evaluate("window.__so.missing")
    for m in missing: problems.append(f"[S] missing audio asked for: {m}")
    for e in tr:
        if e["type"] == "audio" and e["key"] not in IDX: problems.append(f"[S] audio key not in index: {e['key']}")
    for e in errors: problems.append(f"[S] console error: {e}")
    print(f"[S] screen types reached: {sorted(seen)}; placeholder taps {sum(1 for e in tr if e['type'] == 'audio-coming')}")
    ctx.close()


def act(page):
    """Do whatever the current session screen asks, then press Next."""
    time.sleep(0.12)
    step = page.get_attribute(".ss-screen", "data-step") or ""
    if step == "ss-warm":
        t = page.locator(".ss-chip[data-target='1']:not(.right)")
        if t.count(): t.first.click(); return
        for c in page.locator(".ss-chip:not(.done)").all()[:3]: c.click()
    if step == "ss-word":
        tiles = page.locator(".ss-tray .ss-tile:not([disabled])")
        if page.locator(".ss-slot:not([data-part])").count():
            for i in range(tiles.count()):
                if not page.locator(".ss-slot:not([data-part])").count(): break
                b = page.locator(".ss-tray .ss-tile:not([disabled])").nth(0 if i == 0 else 0)
                # try each enabled tile until one lands
                for j in range(page.locator(".ss-tray .ss-tile:not([disabled])").count()):
                    before = page.locator(".ss-slot[data-part]").count()
                    page.locator(".ss-tray .ss-tile:not([disabled])").nth(j).click(); time.sleep(0.05)
                    if page.locator(".ss-slot[data-part]").count() > before: break
            return
        for c in page.locator(".ss-chip:not(.done)").all()[:2]: c.click()
    if step == "ss-fluency" and page.locator(".ss-start").is_visible() and page.inner_text(".ss-start") == "Start 1-minute read":
        page.click(".ss-start"); page.wait_for_function("document.querySelector('.ss-pace').textContent.startsWith('Time')", timeout=8000)
        page.screenshot(path=str(SHOTS / "S_fluency-pick.png"))
        page.locator(".ss-w").nth(min(9, page.locator(".ss-w").count() - 1)).click(); time.sleep(0.2)
        if "words" not in page.inner_text(".ss-pace"): raise AssertionError("pace not shown")
        return
    if step == "ss-text" and page.locator(".ss-more:not([hidden])").count():
        page.click(".ss-more"); return
    if page.locator(".ss-sent").count() and not page.locator(".ss-sent.hl").count(): page.locator(".ss-sent").first.click()
    if step == "ss-write":
        ta = page.locator(".ss-text")
        if ta.count() and not ta.input_value():
            if page.locator(".ss-tilesbtn").count(): page.click(".ss-tilesbtn"); page.locator(".ss-wtiles .ss-tile").first.click()
            ta.type(" My summary in one sentence.")
        if page.locator(".ss-compare:not([hidden])").count(): page.click(".ss-compare")
    for b in page.locator(".ss-show:not([hidden])").all(): b.click()
    for r in page.locator(".ss-self").all():
        if not r.locator(".on").count(): r.locator(".ss-mark").first.click()
    nb = page.locator(".foot .next:not([disabled])")
    if nb.count(): nb.click(); time.sleep(0.15)


def main():
    levels = (5, 6, 7)
    if "--levels" in sys.argv: levels = tuple(int(x) for x in sys.argv[sys.argv.index("--levels") + 1].split(","))
    problems = []; server = None
    if not port_open(5318):
        server = subprocess.Popen(["npx", "vite", "--port", "5318", "--strictPort"], cwd=APP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(5318): break
            time.sleep(0.5)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            run_all(br, problems, "http://localhost:5318/?fast", levels)
            br.close()
    finally:
        if server: server.terminate()
    print("\n".join(problems) if problems else "ALL CHECKS GREEN")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
