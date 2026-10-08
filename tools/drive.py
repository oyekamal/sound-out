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
G2P = {o["g"]: o["p"] for o in GPC["order"]}
for o in GPC["order"]:
    PID2G.setdefault(o["p"], o["g"])
URL = None
VOWELS = {"a", "i", "o", "e", "u"}
problems = []
# --track A|B (default both) · --from KEY_PREFIX (seed every earlier sitting as passed, start there) · --until KEY_PREFIX (stop after
# the last sitting matching it). The plan is read from the home screen, so it follows whatever lessons the app ships.
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TRACKS = [ARG("--track")] if ARG("--track") else ["A", "B"]
FROM, UNTIL = ARG("--from"), ARG("--until")
PORT = int(ARG("--port", "5317"))                 # --port N --app DIR: serve DIR (e.g. a clean export of HEAD) on its own port
SERVE = Path(ARG("--app", str(ROOT / "app")))
L1_IDS = [f"L1.{i:02d}" for i in range(1, 15)]
MASTERY = {"letters": 31, "real": 20, "pseudo": 10, "heart": 24, "context": 6, "dictation": 10, "bdpq": 8}   # course/level-1/mastery-check.md


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
    global URL
    URL = f"http://localhost:{PORT}/?fast"
    SHOTS.mkdir(exist_ok=True)
    for t in TRACKS:   # only this run's own screenshots (other drivers write S_* etc. into the same folder)
        for f in SHOTS.glob(f"{t}{'_' + FROM if FROM else ''}_[0-9]*.png"): f.unlink()
    server = None
    if not port_open(PORT):
        server = subprocess.Popen(["npx", "vite", "--port", str(PORT), "--strictPort"], cwd=SERVE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(PORT): break
            time.sleep(0.5)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            for track in TRACKS:
                run(br, track, FROM, UNTIL)
            if "--no-sessions" not in sys.argv:   # Levels 5-7 practice lessons (tools/drive_session.py)
                import drive_session; drive_session.run_all(br, problems, URL)
            br.close()
    finally:
        if server: server.terminate()
    print("\n".join(problems) if problems else "ALL CHECKS GREEN")
    sys.exit(1 if problems else 0)


SEED = """async ([keys]) => {
  const d = await new Promise((res, rej) => { const r = indexedDB.open('sound-out', 1); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
  const get = (st, k) => new Promise(res => { const r = d.transaction(st).objectStore(st).get(k); r.onsuccess = () => res(r.result); });
  const pid = (await get('settings', 'active')).value;
  const p = (await get('progress', pid)) || { id: pid, sittings: {}, lessons: {}, stickers: [], village: [], days: [], sittingCount: 0 };
  for (const k of keys) p.sittings[k] = { done: true, passed: true, correct: 0, judged: 0, at: Date.now() };
  await new Promise(res => { const t = d.transaction('progress', 'readwrite'); t.objectStore('progress').put(p); t.oncomplete = res; });
}"""


def run(br, track, start=None, until=None):
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
        page.screenshot(path=str(SHOTS / f"{track}{'_' + start if start else ''}_{n[0]:02d}_{name}.png"))
    # onboarding
    page.set_default_timeout(5000); page.wait_for_selector(".whocard"); shot("who-is-reading")
    page.click(f".whocard[data-track={track}]")
    page.wait_for_selector(".langs"); shot("help-language")
    page.click(".onboard .skip")
    # the first sitting starts by itself; go home and read the whole path off the screen
    page.wait_for_selector(".sitting"); page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .node")
    plan = page.evaluate("[...document.querySelectorAll('.home .node[data-key]')].map(b => b.dataset.key)")
    miss = [l for l in L1_IDS if not any(k.startswith(l + ":") for k in plan)]
    if miss: problems.append(f"[{track}] Level 1 lessons not on the path: {miss}")
    if not page.locator(".home .node[data-level='2'][disabled], .home .node.locked[data-key^='L2.']").count():
        problems.append(f"[{track}] Level 2 is not shown locked on the path")
    i0 = next((i for i, k in enumerate(plan) if start and k.startswith(start)), 0)
    if i0:
        page.evaluate(SEED, [plan[:i0]]); page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .node"); time.sleep(0.3)
    if until:
        last = max(i for i, k in enumerate(plan) if k.startswith(until)); plan = plan[:last + 1]
    plan = plan[i0:]
    print(f"[{track}] plan: {len(plan)} sittings {plan[0]} .. {plan[-1]}")
    page.evaluate("window.__so.trace.length = 0")
    page.click(f".node[data-key='{plan[0]}']")
    gate_count = {"n": 0}
    done_sittings = []
    deadline = time.time() + 120 + 90 * len(plan)
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
        if step.startswith("oral") and page.locator(".screen .printed, .screen .lettercard, .screen .tilebtn, .screen .g").count():
            problems.append(f"[{track}] letters on an L1.01 oral screen ({step})"); shot("VIOLATION-letters")
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
        l1 = page.locator(".l1-opts .opt[data-ok] .opt-pick:not([disabled])")
        if l1.count():
            l1.first.click(); time.sleep(0.3); return False
        prev = page.locator("button.lettercard.small[data-letter]:not(.seen)")
        if prev.count():
            prev.first.evaluate("b => b.classList.add('seen')"); prev.first.click(); time.sleep(0.3); return False
        picks = page.locator(".options:not(.three):not(.l1-opts) .opt-pick:not([disabled])")
        if picks.count() in (3, 4):   # 4 = 2x2 grid, 3 = early check
            ev = page.evaluate("window.__so.trace.filter(e=>e.type==='gate-show').slice(-1)[0]")
            att = page.evaluate("window.__so.trace.filter(e=>e.type==='attempt').slice(-1)[0].n")
            if att == 1: gate_count["n"] += 1
            gi = gate_count["n"]
            # scripted mistakes: gate 2 = wrong then right (repair); gate 4 = wrong twice (review); check gate (B) = timeout once
            wrong = not start and ((gi == 2 and att == 1) or (track == "A" and gi == 7))   # scripted only on a run from the start (L1.02)
            if not start and track == "B" and gi == 6 and att == 1:
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
            pid = page.get_attribute(".speaker.big", "data-key").split(":")[1]
            cands = [t for t in page.evaluate("[...document.querySelectorAll('.tray .tilebtn[data-letter]:not(.wrong)')].map(b => b.dataset.letter)") if G2P.get(t) == pid]
            # several letters share a sound (c k ck): prefer the letter this sitting just taught
            taught = page.evaluate("window.__so.trace.filter(e => e.type === 'step' && e.letter).map(e => e.letter)")
            g = next((l for l in reversed(taught) if l in cands), cands[0] if cands else PID2G[pid])
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
    if page.locator(".endscreen").count(): page.click(".endscreen .btn.ghost")
    else: shot("STUCK"); page.evaluate("window.__so.app.home()")
    page.wait_for_selector(".home"); time.sleep(0.4); shot("home-after")
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
    parts = [e for e in tr if e["type"] == "mastery-part"]
    for e in parts:
        if e["judged"] != MASTERY[e["id"]]: problems.append(f"[{track}] mastery part {e['id']}: {e['judged']} items run, instrument has {MASTERY[e['id']]}")
    if any(k.startswith("L1.14:") for k in plan) and not parts: problems.append(f"[{track}] the Level 1 mastery check did not run")
    if parts:
        res = next(e for e in reversed(tr) if e["type"] == "check-end" and "parts" in e)
        print(f"[{track}] mastery: {res['result']} " + " ".join(f"{p['id']} {p['correct']}/{p['judged']}" for p in res["parts"]))
    reviews = sum(1 for e in tr if e["type"] == "gate-review"); timeouts = sum(1 for e in tr if e["type"] == "gate-timeout")
    for e in errors: problems.append(f"[{track}] console error: {e}")
    print(f"[{track}] sittings {done_sittings}; gates {len(gates)}; repairs {repairs}; reviews {reviews}; timeouts {timeouts}; "
          f"audio plays {sum(1 for e in tr if e['type'] == 'audio')}; screenshots {n[0]}")
    ctx.close()


if __name__ == "__main__":
    if "--level" in sys.argv:      # Levels 2-4: every sitting + every gate of one level (tools/drive_levels.py)
        sys.path.insert(0, str(Path(__file__).resolve().parent)); import drive_levels; drive_levels.main()
    else:
        main()
