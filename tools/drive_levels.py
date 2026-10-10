#!/usr/bin/env python3
"""Drive one of Levels 2-4 end to end with Playwright (mouse only, 390x844) and check the rules.

  python3 tools/drive.py --level 2        (same as: python3 tools/drive_levels.py 2)
  options: --track A|B (default both) · --only L2.05 (one lesson) · --full-b (Track B walks every sitting too)

Every sitting of every lesson of the level is opened from the path and walked to its end screen, as a child (Track A);
as a grown-up (Track B) each lesson's first sitting and its check; earlier sittings are seeded as passed. That covers each lesson's first screen and every
gate (blend gates, "Show what you know", the level mastery check). Screenshots: app/shots/levels/L<N>/. Asserts:
  1. no console errors / page errors
  2. every audio key the app asked for is either rendered (content/audio_index.json + file on disk) or listed as
     "audio coming" for this level (content/audio_needed.json); nothing else may be missing
  3. every tap-gate item (static pass over content/options_L<N>.json AND every gate shown in the browser) is a 2x2 grid
     {target, onset|final, vowel, both} at the positions the item states (stressed vowel), or a 3-option chain, on Arpabet;
     every gate item has options or a logged reason in options_unbuildable_L<N>.json
  4. no picture is on screen while a printed word or a reading page is on screen
  5. inside a repair the target's whole-word clip never plays
  6. the mastery check gates the next level: a missed mastery check keeps L<N+1>.01 locked, a passed one opens it
Exit code 0 = green.
"""
import json, socket, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright, Error as PWError

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"; C = ROOT / "content"
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
LEVEL = int(ARG("--level") or next(a for a in sys.argv[1:] if a.isdigit()))
TRACKS = [ARG("--track")] if ARG("--track") else ["A", "B"]
ONLY = ARG("--only")
SHOTS = APP / "shots" / "levels" / f"L{LEVEL}"
IDX = json.loads((C / "audio_index.json").read_text())["clips"]
LEX = json.loads((C / "lexicon.json").read_text())
OPTS = json.loads((C / "options.json").read_text())
COMING, BUNDLE = set(), None
LVLEX = {}   # same merge as app/src/levels.js: a later level's entry for a word replaces an earlier level's
for f in sorted((C / "levels").glob("L*.json")):
    b = json.loads(f.read_text())
    COMING |= set(b.get("audioKeys", []))
    LVLEX.update(b["lexicon"])
    if b["level"] == LEVEL: BUNDLE = b
for k, e in LVLEX.items():   # same rule as app/src/content.js: Level 1 wins unless the level entry is a heart word
    if k not in LEX or (e["kind"] == "heart" and LEX[k]["kind"] != "heart"): LEX[k] = e
for f in sorted(C.glob("options_L*.json")):
    for k, o in json.loads(f.read_text()).items(): OPTS.setdefault(k, o)
G2P = {o["g"]: o["p"] for o in json.loads((C / "gpc.json").read_text())["order"]}
G2P.update(BUNDLE["g2p"])
PORT = int(ARG("--port") or 5330 + LEVEL)   # own port per level so levels can drive in parallel (5318 belongs to the dev server)
URL = f"http://localhost:{PORT}/?fast"   # a static build (no dev-server reloads while other work edits files)
ARPA_VOWELS = {"aa", "ae", "ah", "ao", "aw", "ay", "eh", "er", "ey", "ih", "iy", "ow", "oy", "uh", "uw"}
problems = []


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


def check_grid(word, opts, early, pos):
    t = next((o for o in opts if o["cell"] == "target"), None)
    if not t: return f"{word}: no target"
    p = t["p"]
    words = [o["w"] for o in opts]
    if len(set(words)) != len(words): return f"{word}: duplicate option words {words}"
    for o in opts:
        if len(o["p"]) != len(p): return f"{word}: option {o['w']} length differs"
        if o["cell"] != "target" and tuple(o["p"]) == tuple(p): return f"{word}: option {o['w']} sounds like the target"
    diff = lambda a, b: [i for i in range(len(p)) if a[i] != b[i]]
    if early:
        if len(opts) != 3: return f"{word}: early check has {len(opts)} options"
        for o in opts:
            if o["cell"] != "target" and not 1 <= len(diff(p, o["p"])) <= 2: return f"{word}: early option {o['w']} differs at {diff(p, o['p'])}"
        if not any(len(diff(a["p"], b["p"])) == 1 for a in opts for b in opts if a is not b): return f"{word}: early options are not a chain"
        return None
    if not pos:
        vs = [i for i, x in enumerate(p) if x in ARPA_VOWELS]
        if len(vs) != 1: return f"{word}: {len(vs)} vowels and no stated positions"
        pos = {"vowel": vs[0], "onset": vs[0] - 1, "final": len(p) - 1}
    if len(opts) != 4: return f"{word}: {len(opts)} options"
    if pos.get("vowel") is not None and p[pos["vowel"]] not in ARPA_VOWELS: return f"{word}: stated vowel position {pos['vowel']} is not a vowel"
    for o in opts:
        if o["cell"] == "target": continue
        axes = o["cell"].split("+")
        if any(a not in pos for a in axes): return f"{word}: unknown cell {o['cell']}"
        if diff(p, o["p"]) != sorted(pos[a] for a in axes): return f"{word}: option {o['w']} ({o['cell']}) differs at {diff(p, o['p'])}, want {sorted(pos[a] for a in axes)}"
    cells = sorted(o["cell"] for o in opts)
    axes = {a for c in cells for a in c.split("+")} - {"target"}
    if len(axes) != 2: return f"{word}: grid axes {sorted(axes)}"
    A, B = sorted(axes)
    if cells not in (sorted(["target", A, B, f"{A}+{B}"]), sorted(["target", A, B, f"{B}+{A}"])): return f"{word}: cells {cells} are not a 2x2"
    return None


def static_checks():
    lo = json.loads((C / f"options_L{LEVEL}.json").read_text())
    unb = json.loads((C / f"options_unbuildable_L{LEVEL}.json").read_text())
    for k, o in lo.items():
        err = check_grid(k, [o["target"], *o["foils"]], o.get("early"), o.get("pos"))
        if err: problems.append(f"[options] {err}")
        for x in (o["target"], *o["foils"]):
            key = f"ipa:{x['ipa']}"
            if key not in IDX and key not in COMING: problems.append(f"[options] {k}: clip {key} neither rendered nor listed in audio_needed.json")
    silent = [k for k in BUNDLE["gateItems"] if k not in OPTS and k not in unb]
    if silent: problems.append(f"[options] gate items with no options and no logged reason: {silent}")
    need = json.loads((C / "audio_needed.json").read_text()).get(f"L{LEVEL}", {})
    print(f"[static] L{LEVEL}: {len(lo)} option sets checked; {len(unb)} unbuildable (logged, self-check in the app); silently missing {len(silent)}; "
          f"audio needed {need.get('keys')} keys / {need.get('chars')} chars")


SEED = """async ([keys, notPassed]) => {
  const d = await new Promise((res, rej) => { const r = indexedDB.open('sound-out', 1); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
  const get = (st, k) => new Promise(res => { const r = d.transaction(st).objectStore(st).get(k); r.onsuccess = () => res(r.result); });
  const pid = (await get('settings', 'active')).value;
  const p = (await get('progress', pid)) || { id: pid, sittings: {}, lessons: {}, stickers: [], village: [], days: [], sittingCount: 0 };
  for (const k of keys) p.sittings[k] = { done: true, passed: true, correct: 0, judged: 0, at: Date.now() };
  for (const k of notPassed) p.sittings[k] = { done: true, passed: false, correct: 0, judged: 1, at: Date.now(), check: 'miss' };
  await new Promise(res => { const t = d.transaction('progress', 'readwrite'); t.objectStore('progress').put(p); t.oncomplete = res; });
}"""


def run(br, track):
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, reduced_motion="reduce")
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    page.set_default_timeout(5000)
    page.wait_for_selector(".whocard"); page.click(f".whocard[data-track={track}]")
    page.wait_for_selector(".sitting")
    page.wait_for_selector(".sitting"); page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .node")
    allkeys = page.evaluate("[...document.querySelectorAll('.home .node[data-key]')].map(b => b.dataset.key)")
    pre = f"L{LEVEL}."
    plan = [k for k in allkeys if k.startswith(pre) and (not ONLY or k.startswith(ONLY + ":"))]
    if track == "B" and "--full-b" not in sys.argv:   # Track A walks every gate; Track B walks each lesson's first sitting + its check
        firsts = {}
        for k in plan: firsts.setdefault(k.split(":")[0], k)
        plan = [k for k in plan if k in firsts.values() or k.endswith(":X")]
    earlier = [k for k in allkeys if k < pre]
    later = [k for k in allkeys if not k.startswith(pre) and k > pre]
    mastery_key = next((k for k in plan if k.startswith(f"L{LEVEL}.{ {2: 14, 3: 18, 4: 16}[LEVEL]:02d}:")), None)
    nxt_first = next((k for k in later if k.startswith(f"L{LEVEL + 1}.01:")), None)
    page.evaluate(SEED, [earlier + [k for k in plan if k != mastery_key], []])
    page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .node"); time.sleep(0.2)
    # rule 6a: mastery not passed -> next level locked
    if mastery_key and nxt_first:
        page.evaluate(SEED, [[], [mastery_key]]); page.evaluate("window.__so.app.home()"); page.wait_for_selector(".home .node"); time.sleep(0.2)
        if not page.locator(f".node.locked[data-key='{nxt_first}']").count(): problems.append(f"[{track}] {nxt_first} open although {mastery_key} was missed")
    print(f"[{track}] plan: {len(plan)} sittings {plan[0]} .. {plan[-1]}")
    page.evaluate("window.__so.trace.length = 0; window.__so.missing.length = 0; (window.__so.coming || []).length = 0")
    n = [0]; seen = set(); first_seen = set()
    def shot(name):
        n[0] += 1; page.screenshot(path=str(SHOTS / f"{track}_{n[0]:03d}_{name}.png"))
    gates = {"n": 0}
    done = []
    for key in plan:
        page.evaluate(f"() => {{ window.__so.app.sitting('{key}'); }}")
        lid = key.split(":")[0]
        deadline = time.time() + 240
        first = True
        while time.time() < deadline:
            try:
                time.sleep(0.04)
                if page.locator(".printed, .page").count() and page.locator(".picture").count():
                    problems.append(f"[{track}] picture on screen with a printed word ({key})")
                if page.locator(".endscreen").count():
                    done.append(key); break
                if page.locator(".screen").count():
                    sig = page.evaluate("(document.querySelector('.screen')?.dataset.step||'') + '|' + (document.querySelector('.screen h2')?.textContent||'') + '|' + (document.querySelector('.printed')?.dataset.word||'')")
                    if first and lid not in first_seen:
                        first_seen.add(lid); time.sleep(0.15); shot(f"{lid}-first-{key.split(':')[-1]}")
                    first = False
                    if sig not in seen and len(seen) < 400 and sig.split("|")[0] in ("teach", "rule", "attack", "check", "mastery", "attackcheck", "read", "listen"):
                        seen.add(sig); shot(f"{lid}-{sig.split('|')[0]}-{sig.split('|')[1][:18].replace(' ', '_')}")
                if act(page, track, key, gates, shot): continue
            except PWError:
                pass
        else:
            tail = page.evaluate("window.__so.trace.slice(-6).map(e => e.type + ':' + (e.key || e.word || e.step || ''))")
            problems.append(f"[{track}] timed out in {key}; last events {tail}; console {errors[-2:]}"); shot("TIMEOUT-" + key.replace(":", "_"))
            page.evaluate("window.__so.app.home()")
        if key == mastery_key:
            page.click(".endscreen .btn.ghost"); page.wait_for_selector(".home"); time.sleep(0.3); shot(f"home-after-L{LEVEL}-mastery")
            r = page.evaluate("window.__so.trace.filter(e=>e.type==='mastery-end').slice(-1)[0]")
            if not r or r["result"] != "checked": problems.append(f"[{track}] mastery not passed with all-correct answers: {r}")
            elif nxt_first and page.locator(f".node.locked[data-key='{nxt_first}']").count():
                problems.append(f"[{track}] {nxt_first} still locked after passing {mastery_key}")
            elif not nxt_first: print(f"[{track}] mastery passed; Level {LEVEL + 1} is not in the app yet (unlock checked when it ships)")
            else: print(f"[{track}] mastery passed -> {nxt_first} open")
    page.evaluate("window.__so.app.home()"); time.sleep(0.3)
    tr = page.evaluate("window.__so.trace"); missing = page.evaluate("window.__so.missing"); coming = page.evaluate("window.__so.coming || []")
    for m in missing: problems.append(f"[{track}] missing audio (not rendered, not listed): {m}")
    for e in tr:
        if e["type"] == "audio":
            c = IDX.get(e["key"])
            if c:
                if not (APP / "public/audio" / f"{c['id']}.ogg").exists(): problems.append(f"[{track}] audio file missing: {e['key']}")
            elif e["key"] not in COMING and e["key"] != "ph:_": problems.append(f"[{track}] audio key neither rendered nor listed: {e['key']}")
    gshow = [e for e in tr if e["type"] == "gate-show"]
    for g in gshow:
        o = OPTS.get(g["word"].lower(), {})
        err = check_grid(g["word"], g["options"], g.get("early"), o.get("pos"))
        if err: problems.append(f"[{track}] grid rule: {err}")
    repairs = 0
    for i, e in enumerate(tr):
        if e["type"] == "repair-start":
            repairs += 1
            g = next(x for x in reversed(tr[:i]) if x["type"] == "gate-show")
            t = next(o for o in g["options"] if o["cell"] == "target")
            j = next((k for k in range(i, len(tr)) if tr[k]["type"] == "attempt" and tr[k]["n"] == 2), len(tr))
            bad = [x["key"] for x in tr[i:j] if x["type"] == "audio" and x["key"] in (f"w:{g['word']}", f"ipa:{t['ipa']}")]
            if bad: problems.append(f"[{track}] whole word played inside repair of {g['word']}: {bad}")
    for e in errors: problems.append(f"[{track}] console error: {e}")
    selfc = sum(1 for e in tr if e["type"] == "selfcheck-show")
    print(f"[{track}] sittings {len(done)}/{len(plan)}; lessons with first screen {len(first_seen)}; gates {len(gshow)} (+{selfc} self-checks); repairs {repairs}; "
          f"audio plays {sum(1 for e in tr if e['type'] == 'audio')}, of them 'audio coming' {len(coming)}; screenshots {n[0]}")
    ctx.close()


def act(page, track, key, gates, shot):
    """One action on whatever is on screen. True = acted."""
    if page.locator("button.lettercard").count() and not page.locator(".foot .next:not([hidden]):not([disabled])").count():
        page.locator("button.lettercard").first.click(); time.sleep(0.2); return True
    w = page.locator(".printed .g.want")
    if w.count(): w.first.click(); return True
    ch = page.locator(".chunk.want")
    if ch.count(): ch.first.click(); return True
    if page.locator(".flexbtn").count(): page.locator(".flexbtn").first.click(); return True
    if page.locator(".selfhear:not([hidden])").count(): page.locator(".selfhear").click(); return True
    if page.locator(".selfrow:not([hidden]) .selfok").count(): page.locator(".selfok").click(); return True
    nt = page.locator(".printed.tiles .g.next")
    if nt.count(): nt.first.click(); return True
    if page.locator(".saidit:not([hidden])").count() and page.locator(".saidit").first.is_visible():
        page.locator(".saidit").first.click(); return True
    picks = page.locator(".options:not(.three) .opt-pick:not([disabled])")
    if picks.count() in (3, 4):
        att = page.evaluate("window.__so.trace.filter(e=>e.type==='attempt').slice(-1)[0].n")
        if att == 1: gates["n"] += 1
        wrong = gates["n"] == 2 and att == 1 and not key.endswith(":X")      # one scripted repair per run, never inside a check
        if wrong: shot("gate-repair")
        page.locator(".opt:not([data-cell=target]) .opt-pick" if wrong else ".opt[data-cell=target] .opt-pick").first.click(); time.sleep(0.3)
        return True
    warm = page.locator(".options.three .opt")
    if warm.count():
        letter = page.inner_text(".lettercard.small").strip()
        page.locator(f".options.three .opt[data-sound='{letter}'] .opt-pick").click(); time.sleep(0.3); return True
    tb = page.locator(".tray .tilebtn[data-letter]:not(.wrong):not(.right)")
    if tb.count():
        pid = page.get_attribute(".speaker.big", "data-key").split(":", 1)[1]
        cands = [t for t in page.evaluate("[...document.querySelectorAll('.tray .tilebtn[data-letter]:not(.wrong)')].map(b => b.dataset.letter)") if G2P.get(t) == pid]
        page.click(f".tilebtn[data-letter='{cands[0] if cands else tb.first.get_attribute('data-letter')}']"); time.sleep(0.3); return True
    if page.locator(".slot").count() and page.locator(".tray .tilebtn[data-g]:not([disabled])").count():
        wd = page.get_attribute(".speaker.big", "data-key").split(":", 1)[1]
        empty = page.locator(".slot:not([data-g])").count()
        if empty:
            i = len(LEX[wd]["g"]) - empty
            page.locator(f".tray .tilebtn[data-g='{LEX[wd]['g'][i]}']:not([disabled])").first.click(); time.sleep(0.15); return True
    if page.locator(".printed.tricky").count():
        wd = page.evaluate("document.querySelector('.printed.tricky')?.parentElement && [...document.querySelectorAll('.printed.tricky .g')].map(x=>x.textContent).join('')")
        e = LEX.get(wd) or LEX.get(wd.lower())
        acted = False
        for i in (e or {}).get("heartIdx", []):
            b = page.locator(f".printed.tricky .g[data-i='{i}']")
            if "heart" not in (b.get_attribute("class") or ""): b.click(); time.sleep(0.25); acted = True
        if acted: return True
    if page.locator(".page .word").count() and page.locator(".row .btn:not([hidden])").count():
        page.locator(".page .word").first.click(); time.sleep(0.4)
        page.locator(".row .btn").first.click(); return True
    ans = page.locator(".answer:not(.chosen)")
    if ans.count() == 3: ans.first.click(); return True
    nb = page.locator(".foot .next:not([hidden]):not([disabled])")
    if nb.count(): nb.click(); return True
    return False


def main():
    static_checks()
    SHOTS.mkdir(parents=True, exist_ok=True)
    for f in SHOTS.glob("*.png"): f.unlink()
    import tempfile
    dist = Path(tempfile.mkdtemp(prefix="so-drive-"))
    subprocess.run(["npx", "vite", "build", "--base=/", "--outDir", str(dist), "--emptyOutDir", "--logLevel", "error"], cwd=APP, check=True)
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(dist)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        if port_open(PORT): break
        time.sleep(0.25)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            for track in TRACKS: run(br, track)
            br.close()
    finally:
        server.terminate()
    print("\n".join(problems) if problems else "ALL CHECKS GREEN")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
