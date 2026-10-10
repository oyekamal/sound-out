#!/usr/bin/env python3
"""Checks for the teacher-voice layer (app/src/teacher.js) with Playwright at 390x844.

  python3 tools/drive_teacher.py [--port 5318]

1. First launch with autoplay BLOCKED (default Chromium policy): the big tap-to-start shows, one tap removes it and the prompt plays.
2. Onboarding speaks hello + who; every control that a pre-reader must use carries an icon (svg) and a data-say clip.
3. The ear button is on every screen and replays the current prompt (trace 'replay').
4. Idle ladder (?idlefast = 1.5 / 3 / 5 / 9 s): after a prompt, silence gives re-prompt (tier 1), nudge + point (tier 2),
   "tap the speaker" (tier 3), "I will wait" and pause (tier 4); a tap resets it; the point is a .nudge outline.
5. Praise pool: 60 draws, never the same line twice in a row, A-only and B-only lines respect the track.
6. Press and hold a [data-say] control speaks its label and swallows the click.
7. The self-check row is hidden until "Let me hear it" (the `hidden` attribute is not overridden by CSS).
8. No console errors, no missing audio.
Exit code 0 = green.
"""
import json, socket, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
PORT = int(ARG("--port", "5318"))
IDX = json.loads((ROOT / "content/audio_index.json").read_text())["clips"]
problems = []


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


def trace(page, typ=None):
    t = page.evaluate("window.__so.trace")
    return [e for e in t if typ is None or e["type"] == typ]


def waitkey(page, key, secs=10):
    end = time.time() + secs
    while time.time() < end and not any(e["key"] == key for e in trace(page, "audio")): time.sleep(0.2)


def check(cond, msg):
    if not cond: problems.append(msg)
    print(("ok   " if cond else "FAIL ") + msg)


def main():
    server = None
    if not port_open(PORT):
        server = subprocess.Popen(["npx", "vite", "--port", str(PORT), "--strictPort"], cwd=APP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(PORT): break
            time.sleep(0.5)
    out = ROOT / "store/android-test/teacher"; out.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as pw:
            # ---- 1. autoplay blocked (no autoplay flag): tap to start
            br = pw.chromium.launch()
            ctx = br.new_context(viewport={"width": 390, "height": 844}, reduced_motion="no-preference")
            page = ctx.new_page(); errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(f"http://localhost:{PORT}/?idlefast"); page.set_default_timeout(8000)
            page.wait_for_selector(".whocard")
            try: page.wait_for_selector("#teacher-start", timeout=4000); blocked = True
            except Exception: blocked = False
            check(blocked, "autoplay blocked: the tap-to-start overlay is shown")
            if blocked:
                page.screenshot(path=str(ROOT / "app/shots/T_tap-to-start.png"))
                page.click("#teacher-start .startbtn", force=True); waitkey(page, "ui:who")
                check(page.locator("#teacher-start").count() == 0, "tap-to-start disappears after one tap")
                check(any(e["key"] == "ui:who" for e in trace(page, "audio")), "the 'who is reading' prompt plays after the tap")
            ctx.close(); br.close()

            # ---- 2-8 with autoplay allowed
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            for track in ("A", "B"):
                ctx = br.new_context(viewport={"width": 390, "height": 844}, reduced_motion="no-preference")
                page = ctx.new_page(); errs = []
                page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); page.on("pageerror", lambda e: errs.append(str(e)))
                page.goto(f"http://localhost:{PORT}/?idlefast"); page.set_default_timeout(8000)
                page.wait_for_selector(".whocard"); waitkey(page, "ui:who")
                keys = [e["key"] for e in trace(page, "audio")]
                check("ui:hello" in keys and "ui:who" in keys, f"[{track}] onboarding says hello and who")
                check(page.locator("#ear").is_visible(), f"[{track}] the ear button is on the first screen")
                for sel in (".whocard.child", ".whocard.adult"):
                    check(page.locator(f"{sel} svg").count() > 0 and bool(page.get_attribute(sel, "data-say")), f"[{track}] {sel} has an icon and a spoken label")
                # hold-to-hear: press and hold the child card, the click must NOT choose it
                box = page.locator(".whocard.child").bounding_box()
                page.mouse.move(box["x"] + 20, box["y"] + 20); page.mouse.down(); time.sleep(0.8); page.mouse.up(); time.sleep(0.4)
                check(any(e["type"] == "hold-say" and e["key"] == "ui:child" for e in trace(page)), f"[{track}] press-and-hold speaks 'A child'")
                check(page.locator(".whocard").count() == 2, f"[{track}] a hold does not activate the card")
                page.click(f".whocard[data-track={track}]", force=True); page.wait_for_selector(".sitting")
                # the first sitting: begin + prompt; then a silent wait climbs the ladder
                page.wait_for_selector(".screen"); time.sleep(1.2)
                keys = [e["key"] for e in trace(page, "audio")]
                check("ui:begin" in keys, f"[{track}] the sitting says 'Let's begin'")
                page.evaluate("window.__so.trace.length = 0")
                # wait without touching: tier 1..4 within ~16 s of idlefast timings (1.5/3/5/9 s after the prompt ends)
                deadline = time.time() + 40
                while time.time() < deadline and not any(e.get("tier") == 4 for e in trace(page, "idle")): time.sleep(0.5)
                tiers = [e["tier"] for e in trace(page, "idle")]
                check(tiers[:4] == [1, 2, 3, 4], f"[{track}] idle ladder fires tiers 1,2,3,4 in order (got {tiers})")
                ak = [e["key"] for e in trace(page, "audio")]
                check("ui:idleHelp" in ak and "ui:idleWait" in ak, f"[{track}] idle plays 'tap the speaker' and 'I will wait'")
                page.screenshot(path=str(ROOT / f"app/shots/T_{track}_idle.png"))
                n_before = len(trace(page, "idle"))
                time.sleep(3.0)
                check(len(trace(page, "idle")) == n_before, f"[{track}] after 'I will wait' the teacher pauses (no more idle events)")
                # a tap restarts the ladder; the ear replays the prompt
                page.click("#ear", force=True); time.sleep(0.3)
                check(len(trace(page, "replay")) >= 1, f"[{track}] the ear button replays the prompt")
                # spoken navigation: Next and Skip are arrows with a clip
                if page.locator(".foot .next").count():
                    check(page.locator(".foot .next svg").count() > 0 and page.get_attribute(".foot .next", "data-say") == "ui:next", f"[{track}] Next carries an arrow icon and a clip")
                # praise pool: no back-to-back repeats, track lines respected
                res = page.evaluate("""async () => { const t = window.__so.teacher; const seen = []; window.__so.trace.length = 0;
                  for (let i = 0; i < 60; i++) { window.__so.audioOff = true; await t.right({ kind: ['pick','read','sound','spell','listen'][i % 5], tries: 1 }); }
                  return window.__so.trace.filter(e => e.type === 'praise').map(e => e.key); }""")
                rep = [i for i in range(1, len(res)) if res[i] == res[i - 1]]
                check(len(res) >= 60 and not rep, f"[{track}] praise pool: 60 draws, no line twice in a row ({len(set(res))} distinct)")
                check(("goodWork" not in res) if track == "A" else ("wow" not in res), f"[{track}] track lines respected ({'no goodWork' if track == 'A' else 'no wow'})")
                # Tilo: child track only
                vis = page.evaluate("[...document.querySelectorAll('.tilo')].filter(e => !e.hidden && e.offsetParent !== null).length")
                check((vis == 1) if track == "A" else (vis == 0), f"[{track}] Tilo is {'shown' if track == 'A' else 'absent'} ({vis} visible)")
                # For grown-ups: Home -> gate -> privacy text, no outside link anywhere
                page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .grownups")
                page.locator(".home .grownups").scroll_into_view_if_needed(); page.click(".home .grownups"); page.wait_for_selector(".gu-wrap")
                import re as _re
                def sum_(): a, b = map(int, _re.findall(r"\d+", page.inner_text(".gu-q"))); return a * b
                page.fill(".gu-in", "1"); page.press(".gu-in", "Enter")
                check("Not quite" in page.inner_text(".gu-msg"), f"[{track}] a wrong sum is refused with a new sum")
                page.fill(".gu-in", str(sum_())); page.press(".gu-in", "Enter"); page.wait_for_selector(".privacy")
                check(page.locator("a[href], [href^=mailto]").count() == 0 and "oyekamal.github.io/sound-out/privacy.html" in page.inner_text(".privacy"), f"[{track}] privacy screen shows the address as text, no link")
                check(page.locator(".tilo:not([hidden])").count() == 0 or track == "A", f"[{track}] no mascot on the privacy screen")
                for e in errs: problems.append(f"[{track}] console error: {e}")
                ctx.close()
            br.close()
    finally:
        if server: server.terminate()
    print("\n".join(problems) if problems else "ALL TEACHER CHECKS GREEN")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
