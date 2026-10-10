#!/usr/bin/env python3
"""Fresh, curated review screenshots of the CURRENT app, 412x915 CSS px @2x, saved as WebP into store/review/.

  python3 tools/shoot_review.py                       # every section
  python3 tools/shoot_review.py --sections 3,4        # only those sections (others kept from the existing index.json)
  python3 tools/shoot_review.py --explore L1.02:A:A --track A     # print the screen kinds a sitting walks through (no shots)
  options: --port 5461 (own static server) · --out store/review

Reuses the navigation helpers of tools/drive_levels.py (act), tools/drive_session.py (act, Level 5-7 practice) and the
trace / seed ideas of tools/drive.py, tools/shoot_tilo.py and tools/shoot_pictures.py. The existing tools are imported, never edited.
Every shot goes into index.json as {file, track, section, title, note}; a screen that cannot be reached is recorded with
note "COULD NOT REACH: <reason>". Console / page / HTTP errors go to console_errors.txt.
Sections: 1 First run · 2 Home · 3 Level 1 Track A · 4 Level 1 Track B · 5 Levels 2-7 · 6 Rewards and progress.
"""
import io, json, re, socket, subprocess, sys, tempfile, time
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright, Error as PWError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
PORT = int(ARG("--port", "5461"))
OUT = ROOT / ARG("--out", "store/review")
SECTIONS = {1: "1 First run", 2: "2 Home", 3: "3 Level 1, Track A", 4: "4 Level 1, Track B", 5: "5 Levels 2 to 7", 6: "6 Rewards and progress"}
RUN = [int(x) for x in ARG("--sections", "1,2,3,4,5,6").split(",")]
VP = {"width": 412, "height": 915}

# reuse the older drivers (they parse argv at import time: give drive_levels the --level it insists on)
sys.path.insert(0, str(HERE))
_argv = sys.argv; sys.argv = [_argv[0], "--level", "2"]
import drive_levels as DL      # noqa: E402  act(), SEED
import drive_session as DS     # noqa: E402  act() for Levels 5-7
sys.argv = _argv
for _f in sorted((ROOT / "content/levels").glob("L*.json")):   # drive_levels only knows the grapheme sounds of level 2
    DL.G2P.update(json.loads(_f.read_text())["g2p"])

errors = []          # (scenario, text)
entries = []         # shots of this run: dict(section, track, stem, title, note)
SCEN = [""]


def port_open(p):
    with socket.socket() as s: return s.connect_ex(("127.0.0.1", p)) == 0


# ------------------------------------------------------------------ output
class Out:
    """Collects shots into <out>/_work/<n>.webp; finalize() renames them NN_track_area_what.webp in section order."""
    def __init__(self):
        self.dir = OUT; self.dir.mkdir(parents=True, exist_ok=True)
        self.n = 0

    def save(self, png, section, track, area, what, title, note):
        self.n += 1
        stem = f"{track.replace('+', '')}_{area}_{what}".lower()
        stem = re.sub(r"[^a-z0-9_]+", "-", stem).strip("-")
        tmp = self.dir / f"_new_{section}_{self.n:04d}.webp"
        Image.open(io.BytesIO(png)).convert("RGB").save(tmp, "WEBP", quality=80, method=4)
        entries.append(dict(section=section, track=track, stem=stem, title=title, note=note, tmp=tmp.name))

    def missing(self, section, track, area, what, title, reason):
        entries.append(dict(section=section, track=track, stem=re.sub(r"[^a-z0-9_]+", "-", f"{track}_{area}_{what}".lower()).strip("-"),
                            title=title, note=f"COULD NOT REACH: {reason}", tmp=None))
        print(f"   !! COULD NOT REACH {title}: {reason}", flush=True)

    def finalize(self):
        idx_path = self.dir / "index.json"
        old = json.loads(idx_path.read_text()) if idx_path.exists() else []
        ran = {SECTIONS[s] for s in RUN}
        keep = [e for e in old if e["section"] not in ran]
        # drop the old files of re-run sections
        for e in old:
            if e["section"] in ran and e.get("file") and (self.dir / e["file"]).exists(): (self.dir / e["file"]).unlink()
        order = {v: k for k, v in SECTIONS.items()}
        rows = [dict(e, _src=self.dir / e["file"] if e.get("file") else None) for e in keep]
        rows += [dict(e, file=None, _src=self.dir / e["tmp"] if e["tmp"] else None) for e in entries]
        rows.sort(key=lambda e: order[e["section"]])    # stable: keeps shoot order inside a section
        for e in rows:
            st = e["stem"] if "stem" in e else (re.sub(r"^\d+_", "", e["file"]).removesuffix(".webp") if e.get("file") else None)
            e["_drop"] = st in DROP and e["_src"] is not None
            if e["_drop"]: e["_src"].unlink()
        rows = [e for e in rows if not e["_drop"]]
        final, staged = [], []
        for i, e in enumerate(rows, 1):
            name = None
            if e["_src"] is not None:
                stem = e["stem"] if "stem" in e else re.sub(r"^\d+_", "", e["file"]).removesuffix(".webp")
                name = f"{i:02d}_{stem}.webp"
                staged.append((e["_src"], self.dir / f"_stage_{name}", name))
            final.append(dict(file=name, track=e["track"], section=e["section"], title=e["title"], note=e["note"]))
        for src, st, _ in staged: src.rename(st)
        for _, st, name in staged: st.rename(self.dir / name)
        idx_path.write_text(json.dumps(final, indent=1, ensure_ascii=False))
        for f in self.dir.glob("_new_*.webp"): f.unlink()
        return final


# The walkers shoot every distinct screen type they meet (about 150); the review set keeps one of each kind per track and
# trims near-duplicates. These stems (track_area_what) are shot and then dropped from the published set, so the set stays near 90.
DROP = set('''ab_firstrun_privacy-bottom a_home_a-foot-grownups b_home_b-level-card-locked a_home_a-practice-section
a_l1_count-sounds a_l1_preview-letters a_l1_minicheck-result a_l1_check-intro a_l1_check-gate a_l1_check-result a_l1_review-name-or-sound
a_l1_review-bdpq-pick a_l1_mastery-made-up-words a_l1_mastery-sentences a_l1_mastery-bdpq a_l1_warm-up a_l1_mastery-tricky-words a_l1_spell-letter
a_l1_hear a_l1_mastery-dictation b_l1_hear b_l1_meet-letter b_l1_correct b_l1_listen b_l1_check-gate b_l1_check-result b_l1_review-bdpq
b_l1_tricky-word b_l1_read-it b_l1_trace
a_l2_l2-06-blend-it a_l2_l2-06-spell a_l2_l2-06-tap-gate a_l2_check-part a_l3_l3-01-rule a_l3_l3-01-spell a_l3_l3-01-tap-gate a_l3_check-part
a_l4_l4-03-tap-gate a_l4_l4-12-spell a_l4_l4-12-rule a_l4_l4-15-attack-check-word a_l4_check-part
b_l2_l2-06-rule b_l2_l2-06-blend-it b_l2_l2-06-spell b_l2_l2-06-tap-gate b_l2_check-part
a_l5_discussion a_l6_warm-up a_l6_discussion a_l7_warm-up a_l7_discussion a_l5_word-work a_l7_word-work
b_l5_practice-section b_l5_warm-up b_l5_discussion b_l5_word-work a_rewards_a-days-practised'''.split())

O = Out()


# ------------------------------------------------------------------ browser helpers
class S:
    """One browser context (one learner profile) + shot helpers."""
    def __init__(self, br, url, track, fast=True):
        self.ctx = br.new_context(viewport=VP, device_scale_factor=2, reduced_motion="reduce")   # as the drive_* tools: pulsing hint tiles are never "stable" to click
        self.page = self.ctx.new_page(); self.page.set_default_timeout(6000)
        self.url, self.track, self.fast = url, track, fast
        p = self.page
        p.on("console", lambda m: errors.append((SCEN[0], f"console.{m.type}: {m.text}")) if m.type == "error" else None)
        p.on("pageerror", lambda e: errors.append((SCEN[0], f"pageerror: {e}" if "at predicate (eval at evaluate" not in (getattr(e, "stack", "") or "") else "pageerror from the test harness, not the app (Playwright wait_for_function string vs the production CSP, from drive_session.act): " + str(e)[:90])))
        p.on("response", lambda r: errors.append((SCEN[0], f"HTTP {r.status} {r.url}")) if r.status >= 400 else None)

    def q(self): return "?fast" if self.fast else ""

    def goto(self):
        self.page.goto(self.url + self.q())

    def onboard(self):
        p = self.page; self.goto(); p.wait_for_selector(".whocard"); time.sleep(0.5)

    def choose(self):
        self.page.click(f".whocard[data-track={self.track}]"); self.page.wait_for_selector(".sitting", timeout=25000)

    def home(self):
        p = self.page
        p.evaluate("() => { window.__so.app.home(); }"); p.wait_for_selector(".home .node", timeout=10000); time.sleep(0.45)

    def reload_home(self):
        self.goto(); self.page.wait_for_selector(".home .node", timeout=15000); time.sleep(0.5)

    def plan(self):
        return self.page.evaluate("[...document.querySelectorAll('.home .node[data-key]')].map(b => b.dataset.key)")

    def seed(self, passed=(), stickers=0, village=(), days=3, lessons=None, words=()):
        self.page.evaluate("""async ([keys, st, vil, days, lessons, words]) => {
          const d = await new Promise((res, rej) => { const r = indexedDB.open('sound-out', 1); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
          const get = (s, k) => new Promise(res => { const r = d.transaction(s).objectStore(s).get(k); r.onsuccess = () => res(r.result); });
          const pid = (await get('settings', 'active')).value;
          const p = (await get('progress', pid)) || { id: pid, sittings: {}, lessons: {}, stickers: [], village: [], days: [], sittingCount: 0 };
          for (const k of keys) p.sittings[k] = { done: true, passed: true, correct: 4, judged: 5, at: Date.now() };
          const S = ['★', '♥', '☀', '☘', '♪', '✿', '☂', '⚑'];
          p.stickers = Array.from({ length: st }, (_, i) => S[i % S.length]); p.village = vil;
          p.days = Array.from({ length: days }, (_, i) => new Date(Date.now() - i * 864e5).toISOString().slice(0, 10));
          p.sittingCount = keys.length; Object.assign(p.lessons, lessons || {}); if (words.length) p.words = words;
          await new Promise(res => { const t = d.transaction('progress', 'readwrite'); t.objectStore('progress').put(p); t.oncomplete = res; });
        }""", [list(passed), stickers, list(village), days, lessons or {}, list(words)])

    # -- shots
    def png(self, full=False): return self.page.screenshot(full_page=full)

    def shot(self, section, area, what, title, note, track=None, full=False):
        O.save(self.png(full), SECTIONS[section], track or self.track, area, what, title, note)
        print(f"   + {title}", flush=True)

    def pose(self, pose, t=2.0):
        end = time.time() + t
        while time.time() < end:
            try:
                if self.page.evaluate("window.__so.tilo && window.__so.tilo.state.pose") == pose: return True
            except PWError: pass
            time.sleep(0.03)
        return False

    def close(self): self.ctx.close()


# ------------------------------------------------------------------ the sitting walker
INFO = """() => {
  const q = s => document.querySelector(s), n = s => document.querySelectorAll(s).length;
  const sc = q('.screen');
  const visible = e => e && e.offsetParent !== null;
  return { end: !!q('.endscreen'), step: sc?.dataset.step || '', h2: (q('.screen h2')?.textContent || '').trim(),
    beat: !!q('.beat .tilo-bubble.on') || !!q('.beat'), gate: n('.options:not(.l1-opts):not(.three) .opt-pick'), three: n('.options.three .opt'),
    l1: n('.l1-opts .opt-pick'), l1pending: !!q('.l1-opts.pending'), pics: n('.screen .picture'), canvas: n('canvas.trace'),
    slots: n('.slot'), tricky: n('.printed.tricky'), page: n('.page .word'), answers: n('.answer'), talk: n('.talk'), printed: n('.printed'),
    lettercard: n('.lettercard'), startplay: n('.startplay'), startbtn: n('#teacher-start, .startbtn'), tilo: [...document.querySelectorAll('.tilo')].filter(visible).length,
    small: n('button.lettercard.small[data-letter]'), tiles: n('.tray .tilebtn'), word: q('.printed')?.dataset.word || '', pose: window.__so.tilo?.state.pose || null,
    mastery: !!q('.mastery-result, .m-result'), text: (q('.screen')?.innerText || '').slice(0, 400) };
}"""


def kind_of(i):
    if i["end"]: return "end"
    step = i["step"] or "screen"
    if i["gate"] >= 3 or i["three"]: tag = "gate"
    elif i["l1"]: tag = "pick"
    elif i["canvas"]: tag = "trace"
    elif i["slots"]: tag = "spell"
    elif i["tricky"]: tag = "tricky"
    elif i["page"]: tag = "page"
    elif i["answers"]: tag = "answers"
    elif i["talk"]: tag = "talk"
    elif i["beat"]: tag = "beat"
    elif i["printed"]: tag = "printed"
    elif i["lettercard"]: tag = "letter"
    else: tag = "plain"
    return f"{step}:{tag}"


TRACE_JS = "window.__so.traceGuide"


def trace_it(page):
    tg = page.evaluate(TRACE_JS); cv = page.locator("canvas.trace").bounding_box()
    if not (tg and cv): return False
    x0, y0, x1, y1 = tg["box"]; k = cv["width"] / 300
    for _ in range(2):
        if not page.locator("canvas.trace").count() or page.locator(".foot .next:not([hidden])").count(): break
        page.mouse.move(cv["x"] + x0 * k, cv["y"] + y0 * k); page.mouse.down(); y = y0
        while y <= y1:
            page.mouse.move(cv["x"] + x0 * k, cv["y"] + y * k, steps=3); page.mouse.move(cv["x"] + x1 * k, cv["y"] + y * k, steps=6); y += 7
        page.mouse.up(); time.sleep(0.5)
    return True


def act(page, track, key, gates, shot):
    """One action on the current screen (Level 1 extras first, then drive_levels.act). True = acted."""
    if page.locator("#teacher-start, .startbtn").count():
        page.locator(".startbtn").first.click(); return True
    if page.locator("canvas.trace").count() and not page.locator(".foot .next:not([hidden]):not([disabled])").count():
        if trace_it(page): return True
    l1 = page.locator(".l1-opts .opt[data-ok] .opt-pick:not([disabled])")
    if l1.count(): l1.first.click(); time.sleep(0.3); return True
    prev = page.locator("button.lettercard.small[data-letter]:not(.seen)")
    if prev.count():
        prev.first.evaluate("b => b.classList.add('seen')"); prev.first.click(); time.sleep(0.3); return True
    if page.locator(".l1-opts").count(): return False       # waiting for the options to enable
    if key.startswith("L1."): return l1_tail(page, track, key, gates)
    return DL.act(page, track, key, gates, shot)


def l1_tail(page, track, key, gates):
    """Level 1 actions, as in drive.py (drive_levels.act's Level 2-4 selectors loop forever on a Level 1 blend screen)."""
    nt = page.locator(".printed.tiles .g.next")
    if nt.count(): nt.first.click(); return True
    if page.locator(".saidit").count() and page.locator(".saidit").first.is_visible(): page.locator(".saidit").first.click(); return True
    if page.locator("button.lettercard").count() and not page.locator(".foot .next:not([hidden]):not([disabled])").count():
        page.locator("button.lettercard").first.click(); time.sleep(0.2); return True
    picks = page.locator(".options:not(.three):not(.l1-opts) .opt-pick:not([disabled])")
    if picks.count() in (3, 4):
        page.locator(".opt[data-cell=target] .opt-pick").first.click(); time.sleep(0.3); return True
    if page.locator(".options.three .opt").count():
        letter = page.inner_text(".lettercard.small").strip()
        page.locator(f".options.three .opt[data-sound='{letter}'] .opt-pick").click(); time.sleep(0.3); return True
    tb = page.locator(".tray .tilebtn[data-letter]:not(.wrong):not(.right)")
    if tb.count():
        pid = page.get_attribute(".speaker.big", "data-key").split(":")[1]
        cands = [x for x in page.evaluate("[...document.querySelectorAll('.tray .tilebtn[data-letter]:not(.wrong)')].map(b => b.dataset.letter)") if DL.G2P.get(x) == pid]
        taught = page.evaluate("window.__so.trace.filter(e => e.type === 'step' && e.letter).map(e => e.letter)")
        g = next((l for l in reversed(taught) if l in cands), cands[0] if cands else tb.first.get_attribute("data-letter"))
        page.click(f".tilebtn[data-letter='{g}']"); time.sleep(0.3); return True
    if page.locator(".slot").count() and page.locator(".tray .tilebtn[data-g]:not([disabled])").count():
        w = page.get_attribute(".speaker.big", "data-key").split(":", 1)[1]
        empty = page.locator(".slot:not([data-g])").count()
        if empty:
            i = len(DL.LEX[w]["g"]) - empty
            page.locator(f".tray .tilebtn[data-g='{DL.LEX[w]['g'][i]}']:not([disabled])").first.click(); time.sleep(0.15); return True
    if page.locator(".printed.tricky").count():
        w = page.evaluate("[...document.querySelectorAll('.printed.tricky .g')].map(x=>x.textContent).join('')")
        e = DL.LEX.get(w) or DL.LEX.get(w.lower()); acted = False
        for i in (e or {}).get("heartIdx", []):
            b = page.locator(f".printed.tricky .g[data-i='{i}']")
            if "heart" not in (b.get_attribute("class") or ""): b.click(); time.sleep(0.25); acted = True
        if acted: return True
    if page.locator(".page .word").count() and page.locator(".row .btn:not([hidden])").count():
        page.locator(".page .word").first.click(); time.sleep(0.6)
        page.locator(".page .word").first.click(); time.sleep(0.4)
        page.locator(".row .btn").first.click(); return True
    ans = page.locator(".answer:not(.chosen)")
    if ans.count() == 3: ans.first.click(); return True
    nb = page.locator(".foot .next:not([hidden]):not([disabled])")
    if nb.count(): nb.click(); return True
    return False


def click_pick(page, ok):
    """Click the right (ok=True) or a wrong option on a gate or a Level 1 pick card. False if nothing to click."""
    if page.locator(".options.three .opt[data-sound]").count() and page.locator(".lettercard.small").count():
        letter = page.inner_text(".lettercard.small").strip()
        loc = page.locator(f".options.three .opt[data-sound='{letter}'] .opt-pick" if ok else f".options.three .opt:not([data-sound='{letter}']) .opt-pick")
        if loc.count(): loc.first.click(); return True
    for sel_ok, sel_bad in ((".l1-opts .opt[data-ok] .opt-pick:not([disabled])", ".l1-opts .opt:not([data-ok]) .opt-pick:not([disabled])"),
                            (".opt[data-cell=target] .opt-pick:not([disabled])", ".opt:not([data-cell=target]) .opt-pick:not([disabled])")):
        loc = page.locator(sel_ok if ok else sel_bad)
        if loc.count(): loc.first.click(); return True
    return False


def poll(page, js, secs):
    """Poll a JS function until truthy (page.wait_for_function evals a string, which the production CSP forbids)."""
    end = time.time() + secs
    while time.time() < end:
        try:
            if page.evaluate(js): return True
        except PWError: pass
        time.sleep(0.1)
    return False


def settle(page, tag):
    """Wait until the screen is really ready to look at."""
    if tag in ("gate", "pick"):
        poll(page, "() => document.querySelectorAll('.opt-pick:not([disabled])').length >= 2 && !document.querySelector('.l1-opts.pending')", 5)
    elif tag == "beat":
        poll(page, "() => !!document.querySelector('.beat .tilo-bubble.on')", 4)
    poll(page, "() => [...document.querySelectorAll('img')].every(i => i.complete)", 2.5)
    time.sleep(0.35)


def walk(s, key, targets, section=None, area="", explore=False, budget=170, extra=None):
    """Open one sitting and walk it. targets = list of dict(kind=<regex on step:tag>, what, title, note, [pre=lambda info->bool], [cheer|wrong]).
    A target is shot at its first matching screen. Returns the set of target `what`s that were shot. Stops when all are shot,
    on the end screen (after shooting an 'end' target), on a stall or at the budget."""
    page = s.page; got = set(); seenk = []
    page.evaluate(f"() => {{ window.__so.app.sitting('{key}'); }}")
    gates = {"n": -999}; t0 = time.time(); last, last_chg = None, time.time(); track = key.split(":")[1]
    while time.time() - t0 < budget:
        try:
            time.sleep(0.05)
            i = page.evaluate(INFO); k = kind_of(i)
            if not seenk or seenk[-1] != k:
                seenk.append(k)
                if explore: print(f"   {k:28s} h2={i['h2'][:34]!r:38s} tilo={i['tilo']} pose={i['pose']} word={i['word']}", flush=True)
            sig = k + i["h2"] + i["word"] + str(i["gate"]) + i["text"][:60]
            if sig != last: last, last_chg = sig, time.time()
            elif time.time() - last_chg > 60:
                if not explore and section: print(f"   stalled in {key} on {k}", flush=True)
                break
            if explore:
                if i["end"]: break
                if act(page, track, key, gates, lambda *_: None): continue
                continue
            for t in targets:
                if t["what"] in got or not re.fullmatch(t["kind"], k): continue
                if t.get("pre") and not t["pre"](i): continue
                tag = k.split(":")[-1]
                if t.get("wrong") and (i["gate"] >= 3 or i["l1"]) and track == "A":      # wrong answer with the encouraging Tilo
                    settle(page, tag)
                    if click_pick(page, False):
                        ok = s.pose("encouraging", 2.5); s.shot(t.get("sec", section), area, t["what"], t["title"], t["note"] + ("" if ok else " (Tilo's pose was not caught on this frame)"))
                        got.add(t["what"])
                    break
                if t.get("cheer") and (i["gate"] >= 3 or i["l1"]) and track == "A":      # right answer cheer
                    settle(page, tag)
                    if click_pick(page, True):
                        ok = s.pose("celebrating", 2.0); s.shot(t.get("sec", section), area, t["what"], t["title"], t["note"] + ("" if ok else " (Tilo's pose was not caught on this frame)"))
                        got.add(t["what"])
                    break
                if t.get("wrong") or t.get("cheer"):
                    # Track B: the same moment with no mascot (a wrong pick shows the model, a right pick just moves on)
                    if (i["gate"] >= 3 or i["l1"]):
                        settle(page, tag)
                        if click_pick(page, bool(t.get("cheer"))): time.sleep(0.3); s.shot(t.get("sec", section), area, t["what"], t["title"], t["note"]); got.add(t["what"])
                    break
                settle(page, tag)
                s.shot(t.get("sec", section), area, t["what"], t["title"], t["note"]); got.add(t["what"])
            if track == "B" and i["tilo"] and not explore: errors.append((SCEN[0], f"[B] a Tilo is visible on {k} ({key})"))
            if all(t["what"] in got for t in targets) and targets: break
            if i["end"]: break
            if extra and extra(page, i): continue
            if act(page, track, key, gates, lambda *_: None): continue
        except PWError as e:
            if "Timeout" not in str(e) and "Execution context" not in str(e) and "Target" not in str(e): print("   ..", str(e).splitlines()[0][:100])
    return got


def need(section, track, area, targets, got, reason):
    for t in targets:
        if t["what"] not in got: O.missing(SECTIONS[t.get("sec", section)], track, area, t["what"], t["title"], reason)


# ------------------------------------------------------------------ build + serve
def serve():
    dist = Path(tempfile.mkdtemp(prefix="so-review-"))
    for attempt in range(6):   # another agent may be writing files into app/public while vite copies it: retry
        if subprocess.run(["npx", "vite", "build", "--base=/", "--outDir", str(dist), "--emptyOutDir", "--logLevel", "error"], cwd=ROOT / "app").returncode == 0: break
        time.sleep(20)
    else: sys.exit("vite build kept failing")
    srv = None
    if not port_open(PORT):
        srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(dist)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(PORT): break
            time.sleep(0.3)
    else:
        sys.exit(f"port {PORT} is already in use: pass --port")
    return srv



def T(kind, what, title, note, **kw):
    return dict(kind=kind, what=what, title=title, note=note, **kw)


def scroll_to(page, sel, block="start"):
    page.evaluate("([s, b]) => { const e = document.querySelector(s); if (e) e.scrollIntoView({ block: b }); }", [sel, block]); time.sleep(0.4)


def K(plan, lesson, sid=None):
    ks = [k for k in plan if k.startswith(lesson + ":") and (sid is None or k.endswith(":" + sid))]
    return ks[0] if ks else None


def run_walk(s, key, targets, section, area, reason="the walk never showed this screen", budget=170, track=None):
    """Walk one sitting from a freshly loaded Home; report any target that never appeared."""
    SCEN[0] = f"{key}"
    s.reload_home(); print(f" walk {key}", flush=True)
    got = walk(s, key, targets, section=section, area=area, budget=budget)
    need(section, track or s.track, area, [t for t in targets if t["what"] not in got], got, reason)
    return got


def new(br, base, track, fast=True):
    s = S(br, base, track, fast); s.onboard(); s.choose(); s.home(); return s


# ---- 1 First run
def sec1(br, base):
    SCEN[0] = "1 first run"; print("== 1 First run", flush=True)
    a = S(br, base, "A"); a.onboard()
    a.shot(1, "firstrun", "who-is-reading", "Who is reading? (very first screen)", "The first screen ever shown: two big cards, a child or a grown-up, with the choice spoken in English.", track="A+B")
    a.choose()
    try: a.page.wait_for_selector(".beat .tilo-bubble.on", timeout=8000)
    except PWError: pass
    time.sleep(0.6)
    a.shot(1, "firstrun", "child-first-sitting", "After picking a child: the first sitting starts by itself", "Straight into the first sound game with Tilo in the header, no sign-up and no language step.", track="A")
    a.home()
    a.page.click(".homehdr .btn"); a.page.wait_for_selector(".whocard"); time.sleep(0.5)
    a.shot(1, "firstrun", "who-is-reading-again", "Who is reading? once a profile exists", "The same picker on a later visit, now with an 'Or carry on' button for the profile that already exists.", track="A+B")
    a.home()
    # privacy screens, behind the grown-up gate
    a.page.click(".grownups"); a.page.wait_for_selector(".gu-sheet"); time.sleep(0.4)
    a.shot(2, "home", "grownup-gate", "Grown-up gate (grownup.js)", "A multiplication sum in digits that a young child cannot do; it keeps the privacy page and grown-up area away from children.", track="A+B")
    a.page.fill(".gu-in", "1"); a.page.click(".gu-sheet .btn.primary"); time.sleep(0.4)
    a.shot(2, "home", "grownup-gate-wrong", "Grown-up gate after a wrong answer", "A wrong answer shows 'Not quite. Try this one.' and a new sum; three misses lock it for 30 seconds.", track="A+B")
    q = a.page.inner_text(".gu-q"); n1, n2 = map(int, re.findall(r"\d+", q)[:2])
    a.page.fill(".gu-in", str(n1 * n2)); a.page.click(".gu-sheet .btn.primary"); a.page.wait_for_selector(".privacy"); time.sleep(0.5)
    a.shot(1, "firstrun", "privacy-top", "Privacy screen (top)", "The plain-text privacy page: works offline, no account, no ads, no analytics, all data stays on the phone.", track="A+B")
    a.page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); time.sleep(0.4)
    a.shot(1, "firstrun", "privacy-bottom", "Privacy screen (bottom)", "The rest of the privacy page: what the app does not do and the address of the full policy.", track="A+B")
    a.close()
    b = S(br, base, "B"); b.onboard(); b.choose(); time.sleep(0.8)
    b.shot(1, "firstrun", "grownup-first-sitting", "After picking a grown-up: the first sitting", "The same first sitting for a grown-up: plain page, no mascot, no speech bubble.", track="B")
    O.missing(SECTIONS[2], "A+B", "home", "settings", "Settings screen", "the app has no settings screen; the only grown-up areas are the 'Who is reading?' picker and the gated privacy page")
    b.close()


# ---- 2 Home
def sec2(br, base):
    SCEN[0] = "2 home"; print("== 2 Home", flush=True)
    a = new(br, base, "A")
    a.shot(2, "home", "A-fresh", "Track A home, first visit", "Child home: Tilo in the hero, an empty village, and the path with the first sitting open and the rest locked.")
    scroll_to(a.page, ".node.locked", "center")
    a.shot(2, "home", "A-locked-node", "Locked node on the path", "A node with a padlock: it opens only after the sitting before it is passed.")
    plan = a.plan()
    seed = [k for k in plan if k.split(".")[0] == "L1" and k.split(":")[0] <= "L1.05"]
    a.seed(passed=seed, stickers=6, village=["s", "a", "t", "p", "i"], days=4)
    a.reload_home()
    a.shot(2, "home", "A-progress", "Track A home after some lessons", "Child home with village pieces, a row of stickers, days practised in the header and done ticks on the path.")
    scroll_to(a.page, ".node.open", "center")
    a.shot(2, "home", "A-path-open-node", "Level map: done, open and locked nodes", "The path in the middle of Level 1: ticked nodes behind, one open node, locked nodes ahead.")
    scroll_to(a.page, ".level-card[data-level='2']", "start")
    a.shot(2, "home", "A-level-card-locked", "Level card, locked", "Level 2 card, greyed and locked until the Level 1 check is passed.")
    scroll_to(a.page, ".ss-practice", "start")
    a.shot(2, "home", "A-practice-section", "Practice section for Levels 5 to 7", "The 'Practice: Levels 5-7' block with its three level cards (locked until Level 4 is checked) and a Library button.")
    scroll_to(a.page, ".foot-note", "end")
    a.shot(2, "home", "A-foot-grownups", "Home footer with the For grown-ups button", "The bottom of Home: the 'For grown-ups' button that opens the sum gate.")
    a.close()
    b = new(br, base, "B")
    b.shot(2, "home", "B-fresh", "Track B home, first visit", "Grown-up home: a plain 'Lessons' list and a count of words you can read, with no mascot and no village.")
    plan = b.plan()
    seed = [k for k in plan if k.split(":")[0] <= "L1.05"]
    b.seed(passed=seed, days=4, words=["sat", "sip", "pin", "tap", "nip", "pat"], lessons={"L1.02": {"state": "checked"}, "L1.04": {"state": "still_learning"}})
    b.reload_home()
    b.shot(2, "home", "B-progress", "Track B home after some lessons", "Grown-up home with done ticks, 'checked by tapping' and 'still learning' badges and the words to remember.")
    scroll_to(b.page, ".level-card[data-level='2']", "start")
    b.shot(2, "home", "B-level-card-locked", "Level card, locked (Track B)", "The same locked Level 2 card on the grown-up list.")
    b.close()


# ---- 3 Level 1, Track A
def sec3(br, base):
    SCEN[0] = "3 L1 A"; print("== 3 Level 1 Track A", flush=True)
    s = new(br, base, "A"); A = "L1"
    run_walk(s, "L1.01:A:A", [
        T(r"oral-first:.*", "first-sound", "First sound game", "'What sound does it start with?': a real picture and three sound cards, no letters yet."),
        T(r"oral-blend:.*", "blend-pictures", "Blend the sounds, with pictures", "'Which word do the sounds make?': a picture on each answer card."),
        T(r"oral-count:.*", "count-sounds", "Count the sounds", "'How many sounds?' with a picture and number cards."),
        T(r"preview:.*", "preview-letters", "Preview of the first two letters", "The only letters in the oral sitting: a short look at s and a for next time.")], 3, A)
    run_walk(s, "L1.01:A:L", [
        T(r"listen:beat", "listen-intro-tilo", "Listen intro with big Tilo", "The Listen & Talk intro: big Tilo with his speech bubble and one large play button."),
        T(r"listen:plain", "listen-story", "Listen story scenes", "The story screen: the scene pictures appear after each chunk of the story."),
        T(r"listen:talk", "listen-question", "Listen question", "'Say your answer out loud': the scene above a big microphone cue, no tapping needed.")], 3, A)
    run_walk(s, "L1.01:A:X", [
        T(r"oral-check:beat", "minicheck-intro", "Mini check intro", "'Show what you know': the short check at the end of the oral lessons."),
        T(r"oral-check:gate", "minicheck-item", "Mini check item", "One item of the check: hear the sounds, pick the word, one try."),
        T(r"oral-check:plain", "minicheck-result", "Mini check result", "'Checked by tapping': the result screen of the check.")], 3, A)
    run_walk(s, "L1.02:A:A", [
        T(r"hear:.*", "hear", "Hear the new sound", "'Listen to this sound': the new sound is played and Tilo listens along."),
        T(r"meet:.*", "meet-letter", "Meet the letter", "'This letter makes that sound': the letter card, tap to hear it."),
        T(r"trace:.*", "trace", "Trace the letter", "Finger-trace the letter on a canvas with a guide."),
        T(r"spell:.*", "spell-letter", "Which letter makes this sound?", "First spelling step: hear a sound, pick its letter from the tray.")], 3, A)
    # the encouraging pose is too quick at ?fast speed: shoot it at normal speed like tools/shoot_tilo.py (a real wrong pick on the first gate)
    SCEN[0] = "wrong answer, normal speed"
    n = S(br, base, "A", fast=False); n.onboard(); n.choose()
    try:
        n.page.wait_for_selector(".l1-opts:not(.pending):not(.ghost) .opt-pick:not([disabled])", timeout=120000); time.sleep(0.5)
        n.page.locator(".l1-opts .opt:not([data-ok]) .opt-pick:not([disabled])").first.click()
        ok = n.pose("encouraging", 6); time.sleep(0.3)
        n.shot(3, A, "wrong-answer-tilo", "Wrong answer with encouraging Tilo", "A wrong pick on a first-sound card: Tilo takes the thinking pose (hand on chin) and the cards stay for another try." + ("" if ok else " (the encouraging pose was not caught on this frame)"))
    except PWError as e:
        O.missing(SECTIONS[3], "A", A, "wrong-answer-tilo", "Wrong answer with encouraging Tilo", f"normal-speed run failed ({str(e).splitlines()[0][:100]})")
    n.close()
    run_walk(s, "L1.02:A:D", [
        T(r"warm:gate", "warm-up", "Warm-up: what does it say?", "A warm-up card for a letter learned earlier, three answers."),
        T(r"blend:printed", "blend-it", "Blend it", "'Blend it': the printed word split into sounds, tapped one by one."),
        T(r"blend:gate", "tap-gate", "Tap gate: pick the word you heard", "The 2x2 tap gate: four printed words that differ in one or two sounds."),
        T(r"blend:gate", "wrong-answer", "Wrong answer on a tap gate", "A wrong pick on a printed-word gate: the app repeats the right sound and the gate stays for a second try.", wrong=True),
        T(r"blend:gate", "correct-cheer", "Correct answer cheer", "A right pick: Tilo celebrates.", cheer=True),
        T(r"tricky:.*", "tricky-word", "Tricky word", "A 'heart word': tap the part of the word that does not follow the usual sounds."),
        T(r"spell:spell", "spell-word", "Spell it", "Spell a whole word by dropping letters into the slots."),
        T(r"end", "end-of-sitting", "End of a sitting with the mini check score", "'Well done!': dots for each first-try answer, a sticker and Tilo celebrating.")], 3, A, budget=200)
    run_walk(s, "L1.02:A:R", [T(r"read:page", "read-it", "Read it", "A short page to read aloud; tap a word to hear it.")], 3, A)
    run_walk(s, "L1.02:A:X", [
        T(r"check:beat", "check-intro", "Show what you know: intro", "The check after a lesson, as a child sees it."),
        T(r"check:gate", "check-gate", "Check item", "A check item: one try, no repair."),
        T(r"check:plain", "check-result", "Check result", "'Checked by tapping': the result of the lesson check.")], 3, A, budget=200)
    run_walk(s, "L1.13:A:A", [
        T(r"names:.*", "review-names", "Review sitting: name and sound", "A review sitting: a letter has a name and a sound."),
        T(r"names-quiz:pick", "review-name-or-sound", "Review: name or sound?", "Pick whether you heard the letter's name or its sound."),
        T(r"bdpq:.*", "review-bdpq", "Review: b d p q", "The four look-alike letters side by side."),
        T(r"bdpq-pick:pick", "review-bdpq-pick", "Review: which letter makes this sound?", "Pick the right one of the look-alike letters.")], 3, A, budget=240)
    run_walk(s, "L1.14:A:X", [
        T(r"m-intro:.*", "mastery-intro", "Level 1 mastery check: intro", "The Level 1 check intro, with big Tilo."),
        T(r"m-letters:gate", "mastery-letters", "Mastery check: letters", "Part 1: what does each letter say."),
        T(r"m-real:gate", "mastery-real-words", "Mastery check: real words", "Part 2: real words as tap gates."),
        T(r"m-pseudo:gate", "mastery-made-up-words", "Mastery check: made-up words", "Part 3: made-up words, so the reader cannot just remember them."),
        T(r"m-heart:.*", "mastery-tricky-words", "Mastery check: tricky words", "Part 4: tricky words."),
        T(r"m-context:.*", "mastery-sentences", "Mastery check: words in a sentence", "Part 5: words in a short sentence."),
        T(r"m-dictation:.*", "mastery-dictation", "Mastery check: spelling", "Part 6: spell a word you hear."),
        T(r"m-bdpq:.*", "mastery-bdpq", "Mastery check: b d p q", "Part 7: the look-alike letters again."),
        T(r"m-result:.*", "mastery-result", "Mastery check result", "The table of scores per part against the bar, with Level 2 opening on a pass."),
        T(r"end", "mastery-end", "End of the Level 1 check", "The celebration after the Level 1 check.", sec=6)], 3, A, budget=700)
    s.close()


# ---- 4 Level 1, Track B
def sec4(br, base):
    SCEN[0] = "4 L1 B"; print("== 4 Level 1 Track B", flush=True)
    s = new(br, base, "B"); A = "L1"
    run_walk(s, "L1.01:B:A", [
        T(r"oral-first:.*", "first-sound", "First sound game (no mascot)", "The same first-sound game for a grown-up: no Tilo, plain header."),
        T(r"oral-blend:.*", "blend-pictures", "Blend the sounds with pictures (no mascot)", "Blending with pictures on the grown-up track."),
        T(r"oral-blend:.*", "wrong-answer", "Wrong answer, no mascot", "A wrong pick on the grown-up track: the model is spoken, nothing else changes.", wrong=True)], 4, A)
    run_walk(s, "L1.01:B:L", [
        T(r"listen:plain", "listen-story", "Listen story (no mascot)", "The story scenes on the grown-up track."),
        T(r"listen:talk", "listen-question", "Listen question (no mascot)", "Say-it-out-loud question on the grown-up track.")], 4, A)
    run_walk(s, "L1.02:B:ABC", [
        T(r"hear:.*", "hear", "Hear the new sound (no mascot)", "New sounds are heard first, as for the child."),
        T(r"meet:.*", "meet-letter", "Meet the letter (no mascot)", "The letter card on the grown-up track."),
        T(r"trace:.*", "trace", "Trace the letter (no mascot)", "Tracing on the grown-up track."),
        T(r"blend:printed", "blend-it", "Blend it (no mascot)", "Printed word blending for a grown-up."),
        T(r"blend:gate", "tap-gate", "Tap gate (no mascot)", "The same 2x2 tap gate."),
        T(r"blend:gate", "correct", "Correct answer, no mascot", "A right pick on the grown-up track: no cheer animation, the next item simply appears.", cheer=True),
        T(r"spell:.*", "spell", "Spell it (no mascot)", "Spelling on the grown-up track."),
        T(r"end", "end-of-sitting", "End of a sitting (no mascot)", "End screen for a grown-up: score dots and a Home button, no Tilo.")], 4, A, budget=240)
    run_walk(s, "L1.02:B:D", [
        T(r"tricky:.*", "tricky-word", "Tricky word (no mascot)", "Heart-word screen on the grown-up track."),
        T(r"read:page", "read-it", "Read it (no mascot)", "Reading page on the grown-up track."),
        T(r"listen:.*", "listen", "Listen in a combined sitting (no mascot)", "Grown-ups get Read and Listen in one sitting.")], 4, A, budget=200)
    run_walk(s, "L1.02:B:X", [
        T(r"check:(plain|beat)", "check-intro", "Check intro (no mascot)", "'Show what you know' for a grown-up.", pre=lambda i: i["h2"] == "Show what you know"),
        T(r"check:gate", "check-gate", "Check item (no mascot)", "One check item, one try."),
        T(r"check:plain", "check-result", "Check result (no mascot)", "Result screen of the lesson check.", pre=lambda i: "Checked" in i["h2"] or "Still" in i["h2"])], 4, A, budget=200)
    run_walk(s, "L1.13:B:A", [
        T(r"names:.*", "review-names", "Review: name and sound (no mascot)", "Review sitting on the grown-up track."),
        T(r"bdpq:.*", "review-bdpq", "Review: b d p q (no mascot)", "Look-alike letters for a grown-up.")], 4, A, budget=240)
    run_walk(s, "L1.14:B:X", [
        T(r"m-intro:.*", "mastery-intro", "Level 1 check intro (no mascot)", "Level 1 check on the grown-up track."),
        T(r"m-letters:(gate|pick|letter)", "mastery-letters", "Level 1 check: letters (no mascot)", "First part of the Level 1 check.", pre=lambda i: i["l1"] >= 2 or i["gate"] >= 3),
        T(r"m-real:gate", "mastery-real", "Level 1 check: real words (no mascot)", "Real-word part.")], 4, A, budget=500)
    s.close()


LEVELS = {  # level -> (A sittings to walk, level-check key)
    2: dict(walks=[("L2.06", "T", [
                T(r"teach:.*", "teach", "L2 teach", "The new idea of the lesson, with the letters on a card."),
                T(r"rule:.*", "rule", "L2 rule", "The spelling or reading rule in plain words."),
                T(r"blend:printed", "blend-it", "L2 blend it", "Blend a printed word with the new pattern."),
                T(r"blend:gate", "tap-gate", "L2 tap gate", "A tap gate on words with the new pattern."),
                T(r"spell:.*", "spell", "L2 spell it", "Spell a word with the new pattern.")])], check="L2.14"),
    3: dict(walks=[("L3.01", "T", [
                T(r"teach:.*", "teach", "L3 teach", "Long vowels: the new spelling shown on a card."),
                T(r"rule:.*", "rule", "L3 rule", "The long-vowel rule."),
                T(r"blend:gate", "tap-gate", "L3 tap gate", "A tap gate on long-vowel words."),
                T(r"spell:.*", "spell", "L3 spell it", "Spell a long-vowel word.")])], check="L3.18"),
    4: dict(walks=[("L4.03", "T", [
                T(r"teach:.*", "teach", "L4 teach", "Longer words: the new part (prefix, suffix or syllable pattern)."),
                T(r"blend:gate", "tap-gate", "L4 tap gate", "A tap gate on longer words.")]),
            ("L4.12", "D", [
                T(r"rule:.*", "rule", "L4 rule: breaking words apart", "The word-attack rule."),
                T(r"attack:printed", "attack", "L4 attack: break it apart", "The five-step attack on a long word, step by step."),
                T(r"spell:.*", "spell", "L4 spell it", "Spell a longer word.")]),
            ("L4.15", "X", [
                T(r"attackcheck:beat", "attack-check-intro", "L4 attack check intro", "A short check of the five-step attack on unseen words."),
                T(r"attackcheck:printed", "attack-check-word", "L4 attack check word", "Break a never-practised word apart, then say whether you got it.")])], check="L4.16"),
}


def level_check_targets(n, full):
    ts = [T(r"mastery:(beat|plain)", "check-intro", f"Level {n} check: intro", f"The Level {n} check explains that every part must be passed to open Level {n + 1}.", pre=lambda i: "check" in i["h2"].lower() and "Real" not in i["h2"]),
          T(r"mastery:plain", "check-part", f"Level {n} check: part title", "Each part of the check starts with a title card showing the items and the bar.", pre=lambda i: "check" not in i["h2"].lower() and "passed" not in i["h2"] and "Not yet" not in i["h2"]),
          T(r"mastery:gate", "check-item", f"Level {n} check: an item", "A single check item: one try, no repair.")]
    if full:
        ts += [T(r"mastery:plain", "check-result", f"Level {n} check result", f"The result: score per part and 'Level {n} passed', so Level {n + 1} opens.", pre=lambda i: bool(re.search(r"passed|Not yet", i["h2"]))),
               T(r"end", "check-end", f"End of the Level {n} check", f"Celebration after the Level {n} check.", sec=6)]
    return ts


def sec5(br, base):
    SCEN[0] = "5 levels"; print("== 5 Levels 2-7", flush=True)
    for track in ("A", "B"):
        s = new(br, base, track); plan = s.plan()
        for n in ((2, 3, 4) if track == "A" else (2,)):
            L = LEVELS[n]; area = f"L{n}"
            earlier = [k for k in plan if k < f"L{n}."]
            s.seed(passed=earlier, stickers=6, village=["s", "a", "t", "p", "i"], days=4); s.reload_home()
            scroll_to(s.page, f".level-card[data-level='{n}']", "start")
            s.shot(5, area, "level-home", f"Level {n} home (level card and first lessons)", f"The open Level {n} card with the first lesson's nodes underneath, as a learner sees the level.")
            for lesson, sid, targets in L["walks"]:
                key = K(plan, lesson, sid if track == "A" else None) if track == "A" else K(plan, lesson)
                if track == "B":   # grown-up sittings are merged: same lesson, its first sitting
                    targets = [dict(t, title=t["title"] + " (Track B)") for t in targets]
                if not key: O.missing(SECTIONS[5], track, area, "lesson", f"{lesson} sitting", "no such sitting in the plan"); continue
                run_walk(s, key, [dict(t, what=f"{lesson}-{t['what']}") for t in targets], 5, area, budget=150)
            ck = K(plan, L["check"], "X")
            full = n == 2 and track == "A"
            s.seed(passed=[k for k in plan if k < ck], stickers=6, village=["s", "a", "t", "p", "i"], days=4)
            run_walk(s, ck, level_check_targets(n, full), 5, area, budget=720 if full else 70)
            if full:   # the level opened: show Level 3 open on Home
                s.reload_home(); scroll_to(s.page, ".level-card[data-level='3']", "start")
                s.shot(6, "rewards", f"L2-passed-L3-open-{track}", f"Level 3 open after passing the Level 2 check ({track})", "Home after the Level 2 check is passed: the Level 3 card is open and its first nodes are open.")
        s.close()
    # Levels 5-7 practice
    for track, levels in (("A", (5, 6, 7)), ("B", (5,))):
        s = new(br, base, track); DS.SHOTS = Path(tempfile.mkdtemp(prefix="so-review-ds-"))
        s.seed(passed=[k for k in s.plan() if k < "L5."], stickers=6, village=["s", "a", "t"], days=4); s.reload_home()
        for lv in levels:
            area = f"L{lv}"; lid = DS.WALK[lv]; SCEN[0] = f"practice {lid} {track}"; print(f" practice {lid} {track}", flush=True)
            s.reload_home(); scroll_to(s.page, ".ss-practice", "start")
            if lv == levels[0]:
                s.shot(5, area, "practice-section", "Practice section on Home (Levels 5 to 7)", "Home with the Practice block: three level cards and a Library button; levels 5-7 are practice only, nothing is locked by them.")
            s.page.click(".ss-practice .ss-libbtn"); s.page.wait_for_selector(".ss-library"); time.sleep(0.5)
            scroll_to(s.page, f".ss-level[data-level='{lv}']", "start")
            s.shot(5, area, "level-home", f"Level {lv} in the Library", f"The Library list for Level {lv}: every lesson opens, with its title.")
            want = {"warm": ("warm-up", "Practice warm-up"), "word": ("word-work", "Practice word work"), "text": ("knowledge-text", "Practice knowledge text"),
                    "discuss": ("discussion", "Practice discussion"), "check": ("level-check", "Practice check at the end of the lesson")}
            notes = {"warm": "Warm-up chips to tap before the lesson.", "word": "Word work: build words from parts.", "text": "A knowledge text to read, sentence by sentence.",
                     "discuss": "Questions to talk through with a partner.", "check": "A self-check: mark each item as 'I had it' or 'nearly'."}
            s.page.click(f".ss-lesson[data-id='{lid}']"); s.page.wait_for_selector(".ss-screen"); got = set(); t0 = time.time()
            while time.time() - t0 < 200:
                try:
                    if s.page.locator(".ss-end").count():
                        if track == "A" and lv == 5: time.sleep(0.4); s.shot(6, "rewards", "practice-done-L5", "End of a practice lesson (Levels 5 to 7)", "'Practice done': the self-check score and a link back to the Library; practice never locks anything.")
                        break
                    step = (s.page.get_attribute(".ss-screen", "data-step") or "").replace("ss-", "")
                    if step in want and step not in got:
                        got.add(step); time.sleep(0.5)
                        s.shot(5, area, want[step][0], f"L{lv} {want[step][1]}" + (" (Track B)" if track == "B" else ""), notes[step], full=(step == "text"))
                    DS.act(s.page)
                except PWError: time.sleep(0.2)
            need(5, track, area, [dict(what=v[0], title=f"L{lv} {v[1]}") for k, v in want.items() if k not in got], got, "the walk never showed this screen")
        s.close()


# ---- 6 Rewards and progress
def sec6(br, base):
    SCEN[0] = "6 rewards"; print("== 6 Rewards", flush=True)
    a = new(br, base, "A"); plan = a.plan()
    a.seed(passed=[k for k in plan if k <= "L1.05:Z"], stickers=8, village=["s", "a", "t", "p", "i", "n", "m", "d"], days=7, lessons={"L1.02": {"state": "checked"}, "L1.04": {"state": "still_learning"}})
    a.reload_home(); scroll_to(a.page, ".village", "center")
    a.shot(6, "rewards", "A-stickers-village", "Stickers and village", "The child's rewards on Home: a row of earned stickers and the village that grows with each new sound.")
    a.page.evaluate("window.scrollTo(0, 0)"); time.sleep(0.3)
    a.shot(6, "rewards", "A-days-practised", "Progress: days practised", "The header counts days practised and never resets, so a missed day does not look like a loss.")
    scroll_to(a.page, ".badge", "center")
    a.shot(6, "rewards", "A-lesson-badges", "Progress: lesson badges", "Lesson headings carry 'checked by tapping' or 'still learning' once a lesson check is done.")
    run_walk(a, "L1.03:A:A", [T(r"end", "end-new-sound", "End of a sitting that teaches a new sound", "A sticker, a new village piece and Tilo celebrating after a new letter.")], 6, "rewards", budget=120)
    a.close()
    b = new(br, base, "B"); plan = b.plan()
    b.seed(passed=[k for k in plan if k < "L1.06"], days=7, words=["sat", "sip", "pin", "tap", "nip", "pat", "map", "dip"], lessons={"L1.02": {"state": "checked"}, "L1.04": {"state": "still_learning"}})
    b.reload_home(); scroll_to(b.page, ".wordlist", "center")
    b.shot(6, "rewards", "B-words-to-remember", "Track B progress: words to remember", "The grown-up track shows a word list instead of stickers and a village.")
    b.close()


def run_sections(br):
    base = f"http://localhost:{PORT}/"
    fns = {1: sec1, 2: sec2, 3: sec3, 4: sec4, 5: sec5, 6: sec6}
    for n in RUN:
        t0 = time.time()
        try: fns[n](br, base)
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"!! section {n} crashed: {e!r}", flush=True); errors.append((f"section {n}", f"script crash: {e!r}"))
            O.missing(SECTIONS[n], "A+B", "script", "crash", f"Rest of section {n}", f"the review script crashed here ({str(e).splitlines()[0][:120]})")
        print(f"-- section {n} took {time.time() - t0:.0f}s", flush=True)
    final = O.finalize()
    lines = [f"[{sc}] {e}" for sc, e in errors]
    old_errs = [l for l in (OUT / "console_errors.txt").read_text().splitlines() if l.strip() and not l.startswith("No console")] if len(RUN) < 6 and (OUT / "console_errors.txt").exists() else []
    lines = old_errs + lines
    (OUT / "console_errors.txt").write_text("\n".join(dict.fromkeys(lines)) + "\n" if lines else "No console errors, page errors or HTTP errors >= 400 were seen while shooting.\n")
    from collections import Counter
    print(Counter(e["section"] for e in final), len(final), "entries;", sum(1 for e in final if e["note"].startswith("COULD NOT")), "could not reach")


def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            if ARG("--explore"):
                s = S(br, f"http://localhost:{PORT}/", ARG("--track", "A")); s.onboard(); s.choose(); s.home()
                for k in ARG("--explore").split(","):
                    s.reload_home(); print(k, flush=True); walk(s, k, [], explore=True, budget=float(ARG("--budget", 120)))
            else:
                run_sections(br)
            br.close()
    finally:
        if srv: srv.terminate()


if __name__ == "__main__":
    main()
