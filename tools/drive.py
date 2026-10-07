#!/usr/bin/env python3
"""Drive the prototype end to end with Playwright (mouse only, 390x844) and check the rules.

  python3 tools/drive.py            # starts the Vite dev server itself
Walks onboarding -> L1.02 as a child (Sittings A-D, Read, Listen, Show what you know) and as a grown-up
(ABC, D, Check). Screenshots every screen into app/shots/. Asserts:
  1. no console errors / page errors
  2. every audio key the app asked for exists in content/audio_index.json and on disk
  3. every tap-gate item offers a 2x2 grid {target, onset|final, vowel, both}, or the 3-option early check, checked on Arpabet phonemes
  4. no picture is on screen while a printed word or a reading page is on screen
  5. inside a repair (wrong pick -> next attempt) the target's whole-word clip never plays
Exit code 0 = green.
"""
import json, socket, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright, Error as PWError

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"; SHOTS = APP / "shots"
LEX = json.loads((ROOT / "content/lexicon.json").read_text())
GPC = json.loads((ROOT / "content/gpc.json").read_text())
IDX = json.loads((ROOT / "content/audio_index.json").read_text())["clips"]
PID2G = {}
for o in GPC["order"]:
    PID2G.setdefault(o["p"], o["g"])
URL = "http://localhost:5317/?fast"
VOWELS = {"a", "i", "o", "e", "u"}
problems = []


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


ARPA_VOWELS = {"aa", "ae", "ah", "ao", "aw", "ay", "eh", "er", "ey", "ih", "iy", "ow", "oy", "uh", "uw"}


def check_grid(ev):
    """Phoneme check (options carry lower-case Arpabet in `p`; letters never decide).
    2x2 item: 4 options {target, onset|final, vowel, both}, each differing from the target at EXACTLY the stated positions.
    early check (L1.02-L1.04): 3 options, one target, every option within 1 sound of another option (a chain), 2 sounds at most from the target."""
    opts = ev["options"]
    t = next((o for o in opts if o["cell"] == "target"), None)
    if not t: return f"{ev['word']}: no target"
    p = t["p"]; vs = [i for i, x in enumerate(p) if x in ARPA_VOWELS]
    if len(vs) != 1: return f"{ev['word']}: target has {len(vs)} vowels"
    v = vs[0]
    pos = {"vowel": v, "onset": v - 1, "final": len(p) - 1}
    diff = lambda a, b: [i for i in range(len(p)) if a[i] != b[i]]
    words = [o["w"] for o in opts]
    if len(set(words)) != len(words): return f"{ev['word']}: duplicate option words {words}"
    for o in opts:
        if len(o["p"]) != len(p): return f"{ev['word']}: option {o['w']} length differs"
        if o["cell"] != "target" and tuple(o["p"]) == tuple(p): return f"{ev['word']}: option {o['w']} sounds like the target"
    if ev.get("early"):
        if len(opts) != 3: return f"{ev['word']}: early check has {len(opts)} options"
        for o in opts:
            if o["cell"] == "target": continue
            d = diff(p, o["p"])
            if not 1 <= len(d) <= 2: return f"{ev['word']}: early option {o['w']} differs at {d}"
        if not any(len(diff(a["p"], b["p"])) == 1 for a in opts for b in opts if a is not b): return f"{ev['word']}: early options are not a chain"
        return None
    cells = sorted(o["cell"] for o in opts)
    if len(opts) != 4: return f"{ev['word']}: {len(opts)} options"
    for o in opts:
        if o["cell"] == "target": continue
        axes = o["cell"].split("+")
        if any(a not in pos for a in axes): return f"{ev['word']}: unknown cell {o['cell']}"
        want = sorted(pos[a] for a in axes)
        d = diff(p, o["p"])
        if d != want: return f"{ev['word']}: option {o['w']} ({o['cell']}) differs at {d}, want {want}"
    axes = {a for c in cells for a in c.split("+")} - {"target"}
    if len(axes) != 2: return f"{ev['word']}: grid axes {sorted(axes)}, want exactly two (onset|final x vowel, or onset x final)"
    A, B = sorted(axes)
    if sorted(cells) != sorted(["target", A, B, f"{A}+{B}"]) and sorted(cells) != sorted(["target", B, A, f"{B}+{A}"]): return f"{ev['word']}: cells {cells} are not a 2x2"
    return None


def check_all_options():
    """Static pass over EVERY item in content/options.json (the browser run only reaches L1.02): grid rule + every option has a clip + the unbuildable list is complete."""
    opts = json.loads((ROOT / "content/options.json").read_text())
    unb = json.loads((ROOT / "content/options_unbuildable.json").read_text())
    for k, o in opts.items():
        ev = {"word": k, "early": o.get("early"), "options": [dict(x) for x in (o["target"], *o["foils"])]}
        err = check_grid(ev)
        if err: problems.append(f"[all options] {err}")
        for x in ev["options"]:
            if f"ipa:{x['ipa']}" not in IDX: problems.append(f"[all options] no audio clip for {k}: {x['w']} ({x['ipa']})")
        if o["kind"] == "pseudo" and any(f["cell"] != "target" and f.get("realfoil") for f in o["foils"]) and sum(1 for f in o["foils"] if f.get("realfoil")) > 1:
            problems.append(f"[all options] {k}: more than one real-word foil")
    items = [k for k, e in LEX.items() if e["kind"] in ("real", "pseudo")]
    silent = [k for k in items if k.lower() not in opts and k not in unb]
    if silent: problems.append(f"[all options] items with no options and no logged reason: {silent}")
    print(f"[all options] {len(opts)} items checked; {len(unb)} unbuildable (logged); silently missing {len(silent)}")


def main():
    check_all_options()
    SHOTS.mkdir(exist_ok=True)
    for f in SHOTS.glob("*.png"): f.unlink()
    server = None
    if not port_open(5317):
        server = subprocess.Popen(["npx", "vite", "--port", "5317", "--strictPort"], cwd=APP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(5317): break
            time.sleep(0.5)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            for track, plan in (("A", ["L1.02:A:A", "L1.02:A:B", "L1.02:A:C", "L1.02:A:D", "L1.02:A:R", "L1.02:A:L", "L1.02:A:X"]),
                                ("B", ["L1.02:B:ABC", "L1.02:B:D", "L1.02:B:X"])):
                run(br, track, plan)
            if "--no-sessions" not in sys.argv:   # Levels 5-7 practice lessons (tools/drive_session.py)
                import drive_session; drive_session.run_all(br, problems, URL)
            br.close()
    finally:
        if server: server.terminate()
    print("\n".join(problems) if problems else "ALL CHECKS GREEN")
    sys.exit(1 if problems else 0)


def run(br, track, plan):
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=False, reduced_motion="reduce")
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    assert page.title() == "Sound Out", f"wrong app on the port: {page.title()}"
    n = [0]; seen = set()
    def shot(name):
        n[0] += 1
        page.screenshot(path=str(SHOTS / f"{track}_{n[0]:02d}_{name}.png"))
    # onboarding
    page.set_default_timeout(5000); page.wait_for_selector(".whocard"); shot("who-is-reading")
    page.click(f".whocard[data-track={track}]")
    page.wait_for_selector(".langs"); shot("help-language")
    page.click(".onboard .skip")
    gate_count = {"n": 0}
    done_sittings = []
    deadline = time.time() + 600
    def step_once():
        time.sleep(0.15)
        # rule 4: no picture beside a printed word / reading page
        if page.locator(".printed, .page").count() and page.locator(".picture").count():
            problems.append(f"[{track}] picture on screen with a printed word"); shot("VIOLATION-picture")
        if page.locator(".endscreen").count():
            key = page.evaluate("window.__so.trace.filter(e=>e.type==='sitting-end').slice(-1)[0].key")
            if key not in done_sittings:
                done_sittings.append(key); shot("end-" + key.split(":")[-1])
            nxt = plan[plan.index(key) + 1] if key in plan and plan.index(key) + 1 < len(plan) else None
            if not nxt: return True
            if page.locator(".keepgoing").count() and page.evaluate("1") and nxt:
                page.click(".keepgoing")
            else:
                page.click(".endscreen .btn.ghost"); page.wait_for_selector(".home")
                shot("home")
                if page.locator(f".node[data-key='{nxt}'][disabled]").count():
                    problems.append(f"[{track}] {nxt} locked after {key} (mini check missed)"); return True
                page.click(f".node[data-key='{nxt}']")
            return False
        step = page.evaluate("document.querySelector('.screen')?.dataset.step || ''")
        sig = step + "|" + page.evaluate("document.querySelector('.screen h2')?.textContent || ''") + "|" + page.evaluate("document.querySelector('.printed')?.dataset.word || ''")
        if sig not in seen and page.locator(".screen").count():
            seen.add(sig); time.sleep(0.2); shot((step or "screen") + "-" + sig.split("|")[1].replace(" ", "_").replace("?", "")[:24])
        # -- act on whatever is on screen --
        if page.locator(".lettercard:not(.small)").count() and page.locator("button.lettercard").count():
            page.click("button.lettercard"); time.sleep(0.3)
        if page.locator("canvas.trace").count():
            tg = page.evaluate("window.__so.traceGuide")
            cv = page.locator("canvas.trace").bounding_box()
            if tg and cv:
                x0, y0, x1, y1 = tg["box"]; k = cv["width"] / 300
                for _ in range(2):
                    if not page.locator("canvas.trace").count() or page.locator(".foot .next:not([hidden])").count(): break
                    page.mouse.move(cv["x"] + x0 * k, cv["y"] + y0 * k); page.mouse.down()
                    y = y0
                    while y <= y1:
                        page.mouse.move(cv["x"] + x0 * k, cv["y"] + y * k, steps=3)
                        page.mouse.move(cv["x"] + x1 * k, cv["y"] + y * k, steps=6)
                        y += 7
                    page.mouse.up(); time.sleep(0.6)
        nxt_tile = page.locator(".printed.tiles .g.next")
        if nxt_tile.count(): nxt_tile.first.click(); return False
        if page.locator(".saidit").count() and page.locator(".saidit").is_visible():
            page.click(".saidit"); return False
        picks = page.locator(".options:not(.three) .opt-pick:not([disabled])")
        if picks.count() in (3, 4):   # 4 = 2x2 grid, 3 = early check
            ev = page.evaluate("window.__so.trace.filter(e=>e.type==='gate-show').slice(-1)[0]")
            att = page.evaluate("window.__so.trace.filter(e=>e.type==='attempt').slice(-1)[0].n")
            if att == 1: gate_count["n"] += 1
            gi = gate_count["n"]
            # scripted mistakes: gate 2 = wrong then right (repair); gate 4 = wrong twice (review); check gate (B) = timeout once
            wrong = (gi == 2 and att == 1) or (track == "A" and gi == 7)
            if track == "B" and gi == 6 and att == 1:
                shot("gate-waiting-timeout"); time.sleep(4.5); return False
            sel = ".opt:not([data-cell=target]) .opt-pick" if wrong else ".opt[data-cell=target] .opt-pick"
            if att == 1 and gi in (1, 2): shot(f"gate-{gi}-options")
            page.locator(sel).first.click(); time.sleep(0.4)
            if wrong and att == 1: shot(f"gate-{gi}-repair")
            return False
        warm = page.locator(".options.three .opt")
        if warm.count():
            letter = page.inner_text(".lettercard.small").strip()
            page.locator(f".options.three .opt[data-sound='{letter}'] .opt-pick").click(); time.sleep(0.4); return False
        tb = page.locator(".tray .tilebtn[data-letter]:not(.wrong):not(.right)")
        if tb.count():
            key = page.get_attribute(".speaker.big", "data-key")
            g = PID2G[key.split(":")[1]]
            page.click(f".tilebtn[data-letter='{g}']"); time.sleep(0.4); return False
        if page.locator(".slot").count() and page.locator(".tray .tilebtn[data-g]:not([disabled])").count():
            w = page.get_attribute(".speaker.big", "data-key").split(":", 1)[1]
            empty = page.locator(".slot:not([data-g])").count()
            if empty:
                i = len(LEX[w]["g"]) - empty
                page.locator(f".tray .tilebtn[data-g='{LEX[w]['g'][i]}']:not([disabled])").first.click(); time.sleep(0.2)
                return False
        if page.locator(".printed.tricky").count():
            w = page.evaluate("[...document.querySelectorAll('.printed.tricky .g')].map(x=>x.textContent).join('')")
            e = LEX.get(w) or LEX.get(w.lower())
            for i in e.get("heartIdx", []):
                b = page.locator(f".printed.tricky .g[data-i='{i}']")
                if "heart" not in (b.get_attribute("class") or ""): b.click(); time.sleep(0.3)
        if page.locator(".page .word").count() and page.locator(".row .btn:not([hidden])").count():
            page.locator(".page .word").first.click(); time.sleep(0.8)
            page.locator(".page .word").first.click(); time.sleep(0.5)
            page.locator(".row .btn").first.click(); return False
        ans = page.locator(".answer:not(.chosen)")
        if ans.count() == 3: ans.first.click(); return False
        nb = page.locator(".foot .next:not([hidden]):not([disabled])")
        if nb.count(): nb.click(); return False

        return False
    while time.time() < deadline:
        try:
            if step_once(): break
        except PWError:
            pass
    else:
        problems.append(f"[{track}] timed out; done {done_sittings}")
    page.click(".endscreen .btn.ghost"); page.wait_for_selector(".home"); time.sleep(0.4); shot("home-after")
    # ---- rule checks over the trace ----
    tr = page.evaluate("window.__so.trace"); missing = page.evaluate("window.__so.missing")
    for m in missing: problems.append(f"[{track}] missing audio: {m}")
    for e in tr:
        if e["type"] == "audio":
            c = IDX.get(e["key"])
            if not c: problems.append(f"[{track}] audio key not in index: {e['key']}")
            elif not (APP / "public/audio" / f"{c['id']}.ogg").exists(): problems.append(f"[{track}] audio file missing: {e['key']}")
    gates = [e for e in tr if e["type"] == "gate-show"]
    for g in gates:
        err = check_grid(g)
        if err: problems.append(f"[{track}] 2x2 rule: {err}")
    repairs = 0
    for i, e in enumerate(tr):
        if e["type"] == "repair-start":
            repairs += 1
            g = next(x for x in reversed(tr[:i]) if x["type"] == "gate-show")
            t = next(o for o in g["options"] if o["cell"] == "target")
            j = next((k for k in range(i, len(tr)) if tr[k]["type"] == "attempt" and tr[k]["n"] == 2), len(tr))
            bad = [x["key"] for x in tr[i:j] if x["type"] == "audio" and x["key"] in (f"w:{g['word']}", f"ipa:{t['ipa']}")]
            if bad: problems.append(f"[{track}] whole word played inside repair of {g['word']}: {bad}")
    reviews = sum(1 for e in tr if e["type"] == "gate-review"); timeouts = sum(1 for e in tr if e["type"] == "gate-timeout")
    for e in errors: problems.append(f"[{track}] console error: {e}")
    print(f"[{track}] sittings {done_sittings}; gates {len(gates)}; repairs {repairs}; reviews {reviews}; timeouts {timeouts}; "
          f"audio plays {sum(1 for e in tr if e['type'] == 'audio')}; screenshots {n[0]}")
    ctx.close()


if __name__ == "__main__":
    main()
