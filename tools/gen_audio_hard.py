#!/usr/bin/env python3
"""HARD clips of Levels 2-7 in ElevenLabs River under a hard character cap (decision 30). Run with bakeoff/.venv/bin/python.

  gen_audio_hard.py plan      # choose what fits CAP (priority below), write content/local/hard_plan.json + content/audio_still_needed.json
  gen_audio_hard.py render    # call ElevenLabs for the planned requests only (cap re-checked against the ledger content/el_chars.json)
  gen_audio_hard.py build     # cut, loudness, Opus, merge into content/audio_index.json (src='elevenlabs')

Priority: iso L2, pseudowords L2, syllable chunks L2, iso L3, iso L4, pseudowords L3, chunks L3, pseudowords L4, chunks L4.
Whatever does not fit is listed with its character count in content/audio_still_needed.json for a top-up.
Isolated sounds (new phonemes of L2-L4): three prompt forms each, the take whose phone-recogniser output is closest to the target
IPA is shipped (tools/phone_rec.py; smoke test only, Kamal's ears decide). Same voice, model, settings and cache as Level 1.
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import gen_audio_el as g
C, OUT, SR = g.C, g.OUT, g.SR
CAP = 6000
LEDGER = C / "el_chars.json"
PLAN = C / "local" / "hard_plan.json"

ISO_FORMS = {  # pid -> three prompt texts (each is one billed request)
    "sh": ["Shhhh.", "Shhhhhh.", "Sh."], "th": ["Thhhh.", "Thhhhhh.", "Th."], "dh": ["Dhhhh.", "Thhhh, the.", "Thuh."],
    "zh": ["Zhhhh.", "Zhhhhhh.", "Zh."], "ch": ["Ch.", "Chuh.", "[whispers] ch."], "ng": ["Ngngng.", "Ng.", "Nggg."],
    "ng-k": ["Ngk.", "Nk.", "Ank."], "ng-g": ["Ngg.", "Ng-g.", "Anguh."],
    "ao": ["Aw.", "Awww.", "Aww—"], "aw": ["Ow.", "Ow!", "Owww."], "ow": ["Oh.", "Ohhh.", "Oh—"], "ay": ["Eye.", "Eyyy.", "Aye."],
    "ey": ["Ay.", "Ayyy.", "Aaay."], "iy": ["Ee.", "Eee.", "Eeee."], "uw": ["Oo.", "Ooo.", "Oooo."], "uh": ["ʊ.", "ʊ...", "/ʊ/"],
    "oy": ["Oy.", "Oyyy.", "Oi."], "er": ["Er.", "Err.", "Urr."], "aa-r": ["Ar.", "Arr.", "Are."], "ao-r": ["Or.", "Orr.", "Oar."],
    "eh-r": ["Air.", "Err.", "Ehr."], "ih-r": ["Ear.", "Eer.", "Ihr."], "ay-er": ["Ire.", "Eye-er.", "Iyer."], "aw-er": ["Our.", "Ower.", "Owr."],
    "ao-l": ["All.", "Awl.", "Ahl."], "y-uw": ["You.", "Yoo.", "Yew."], "y-uh": ["Yuh.", "Yoo-uh.", "Yuu."], "y-ah": ["Yuh.", "Yah.", "Yu."],
    "w-ah": ["Wuh.", "Wah.", "Wuhh."], "sh-ah-n": ["Shun.", "Shuhn.", "Shan."], "zh-ah-n": ["Zhun.", "Zhuhn.", "Zhn."],
    "ch-er": ["Cher.", "Chur.", "Chuhr."], "ah-s": ["Us.", "Uss.", "Uhs."], "ah-z": ["Uz.", "Uzz.", "Uhz."], "ah-l": ["Ul.", "Uhl.", "Ull."],
    "ah-n": ["Un.", "Uhn.", "Unn."], "ah-n-t": ["Unt.", "Uhnt.", "Un-t."], "ah-d": ["Ud.", "Uhd.", "Udd."], "ih-z": ["Iz.", "Izz.", "Ihz."],
    "ih-d": ["Id.", "Idd.", "Ihd."], "ih-ng": ["Ing.", "Ihng.", "Ing—"], "iy-ah-s": ["Eeus.", "Ee-us.", "Eeuss."], "sh-ah-l": ["Shul.", "Shuhl.", "Shal."],
}


def spent():
    return sum(r["chars"] for r in json.loads(LEDGER.read_text()) if str(r.get("kind", "")).startswith("d30"))


def plan():
    classes = json.loads((C / "audio_classes.json").read_text())
    idx = json.loads((C / "audio_index.json").read_text())["clips"]
    voice = g.get_voice()
    iso = {}   # pid -> (level first needed, ipa)
    for k, v in classes.items():
        if v["kind"] == "iso" and f"ph:{v['pid']}" not in idx: iso.setdefault(v["pid"], (v["level"], v["ipa"]))
    missing = [p for p in iso if p not in ISO_FORMS]
    assert not missing, missing
    budget = CAP - spent(); chosen_req, rows, still = {}, [], []
    def want(label, items):
        nonlocal budget
        for key, texts, meta in items:
            new = [t for t in texts if t not in chosen_req and not g.cached(voice, t)]
            cost = sum(len(t) for t in new)
            if cost <= budget:
                budget -= cost
                for t in new: chosen_req[t] = key
                rows.append({"key": key, "group": label, "requests": texts, "chars": cost, **meta})
            else: still.append({"key": key, "group": label, "requests": texts, "chars": cost, **meta})
    def isos(L): return [(f"ph:{p}", ISO_FORMS[p], {"kind": "iso", "pid": p, "ipa": ipa}) for p, (lv, ipa) in iso.items() if lv == L]
    def words(L, sub):
        out = []
        for k, v in classes.items():
            if v["level"] == L and v["sub"] == sub and v["cut"] in ("last", "open"):
                out.append((k, [g.req_text(v)], {"kind": v["kind"], "cut": v["cut"], "say": v["say"], "ipa": v["ipa"]}))
        return out
    for lab, it in [("iso L2", isos(2)), ("pseudo L2", words(2, "pseudo")), ("chunk L2", words(2, "chunk")), ("iso L3", isos(3)), ("iso L4", isos(4)),
                    ("pseudo L3", words(3, "pseudo")), ("chunk L3", words(3, "chunk")), ("pseudo L4", words(4, "pseudo")), ("chunk L4", words(4, "chunk"))]:
        want(lab, it)
    newchars = sum(len(t) for t in chosen_req)
    PLAN.write_text(json.dumps({"voice": voice, "cap": CAP, "already_spent": spent(), "new_chars": newchars, "rows": rows}, indent=1, ensure_ascii=False))
    # leftovers: every HARD clip not planned, with its character count (name-class prose is rendered locally with pronunciation overrides)
    planned = {r["key"] for r in rows}
    still_ids = {s["key"] for s in still}
    for k, v in classes.items():
        if v["class"] == "hard" and v["kind"] != "iso" and v["sub"] != "name" and k not in planned and k not in still_ids:
            still.append({"key": k, "group": f"{v['sub']} L{v['level']}", "requests": [g.req_text(v)], "chars": 0, "say": v.get("say")})
    seen, per_req = set(), []
    for s in still:
        tot = sum(len(t) for t in s["requests"] if t and t not in seen and not g.cached(voice, t)); seen.update(s["requests"]); s["chars"] = tot
    by = {}
    for s in still: by.setdefault(s["group"], [0, 0]); by[s["group"]][0] += 1; by[s["group"]][1] += s["chars"]
    (C / "audio_still_needed.json").write_text(json.dumps({
        "note": "HARD clips (isolated sounds, made-up words, syllable chunks) that did not fit the 6,000-character ElevenLabs cap of decision 30. "
                "chars = new characters to send (River, eleven_v4, fixed settings; requests shared between keys counted once, in listed order). Top up, then run tools/gen_audio_hard.py plan/render/build.",
        "cap": CAP, "by_group": {k: {"clips": a, "chars": b} for k, (a, b) in by.items()}, "total_chars": sum(b for a, b in by.values()),
        "clips": still}, indent=1, ensure_ascii=False))
    print(f"planned {len(rows)} clips, {newchars} new chars (ledger already {spent()}, cap {CAP}); still needed {len(still)} clips, {sum(s['chars'] for s in still)} chars")
    for lab in dict.fromkeys(r["group"] for r in rows): print(f"  {lab}: {sum(1 for r in rows if r['group'] == lab)} clips, {sum(r['chars'] for r in rows if r['group'] == lab)} chars")
    for k, (a, b) in by.items(): print(f"  STILL {k}: {a} clips {b} chars")


def render():
    p = json.loads(PLAN.read_text()); voice = g.get_voice()
    reqs = {t for r in p["rows"] for t in r["requests"] if not g.cached(voice, t)}
    chars = sum(len(t) for t in reqs)
    if spent() + chars > CAP: sys.exit(f"STOP: ledger {spent()} + {chars} > {CAP}")
    print(f"{len(reqs)} requests, {chars} chars (ledger {spent()} -> {spent() + chars})")
    led = json.loads(LEDGER.read_text())
    from concurrent.futures import ThreadPoolExecutor
    fails = []
    def one(t):
        try: g.tts(voice, t); return t
        except Exception as e: fails.append((t, str(e)))
    with ThreadPoolExecutor(3) as ex: done = [t for t in ex.map(one, sorted(reqs)) if t]
    for t in done: led.append({"text": t, "model": g.MODEL, "kind": "d30-hard", "chars": len(t)})
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False))
    for t, e in fails: print("FAIL", repr(t), e)
    print(f"rendered {len(done)}; ledger now {spent()}")


def fade(x, i_ms=8, o_ms=30):
    x = x.copy(); i, o = int(i_ms * SR / 1000), int(o_ms * SR / 1000)
    if len(x) > i + o: x[:i] *= np.linspace(0, 1, i); x[-o:] *= np.linspace(1, 0, o)
    return x


def build():
    import phone_rec
    p = json.loads(PLAN.read_text()); voice = g.get_voice()
    idxp = C / "audio_index.json"; index = json.loads(idxp.read_text()); clips = index["clips"]
    rr = [g.rms_db(g.decode(OUT / f"{v['id']}.ogg")) for k, v in clips.items() if k.startswith("w:") and v.get("src") is None and v["dur"] > .55][:150]
    word_rms = float(np.median(rr))
    report = {}
    def put(key, a, tag, force_rms):
        cid = hashlib.sha1(f"d30|{voice}|{tag}".encode()).hexdigest()[:12]; dst = OUT / f"{cid}.ogg"
        if force_rms:
            b = a * 10 ** ((word_rms - g.rms_db(a)) / 20); g.encode(b, dst); gain = 0.0
            for _ in range(3):
                e = word_rms - g.rms_db(g.decode(dst))
                if abs(e) <= .3: break
                gain += e; g.encode(b * 10 ** (gain / 20), dst)
        else:
            b, rule = g.loudness(a, word_rms); g.encode(b, dst)
            if rule.startswith("lufs"):
                gain = 0.0
                for _ in range(4):
                    L = g.lufs(g.decode(dst))
                    if L is None or abs(g.LUFS - L) <= .3: break
                    gain += g.LUFS - L; g.encode(b * 10 ** (gain / 20), dst)
        clips[key] = {"id": cid, "dur": round(len(g.decode(dst)) / SR, 3), "src": "elevenlabs"}
    n = {"iso": 0, "word": 0, "skipped": 0}
    for r in p["rows"]:
        texts = r["requests"]
        if not all(g.cached(voice, t) for t in texts): n["skipped"] += 1; continue
        if r["kind"] == "iso":
            best = None
            for t in texts:
                a, al = g.tts(voice, t); a = g.trim(a)[:int(.7 * SR)]
                if len(a) < int(.06 * SR): continue
                s, heard = phone_rec.per(a, r["ipa"]); ms = 1000 * len(a) / SR
                score = s + abs(ms - 350) / 2000
                if best is None or score < best[0]: best = (score, t, a, s, heard, ms)
            if best is None: n["skipped"] += 1; continue
            _, t, a, s, heard, ms = best
            put(r["key"], fade(a, 8, 40), f"{r['key']}|{t}", True); n["iso"] += 1
            report[r["key"]] = {"ipa": r["ipa"], "take": t, "per": round(s, 2), "heard": heard, "ms": round(ms)}
        else:
            t = texts[0]; a, al = g.tts(voice, t)
            w = g.cut_last(a, t, al, r["say"])
            a = g.open_cut(w) if r["cut"] == "open" else w
            put(r["key"], a, f"{r['key']}|{t}|{r['cut']}", False); n["word"] += 1
    index["note"] = index.get("note", "") if "d30 hard" in index.get("note", "") else index.get("note", "") + " | d30 hard: ElevenLabs River for isolated sounds, made-up words, chunks of L2-L4 (src='elevenlabs', tools/gen_audio_hard.py)"
    idxp.write_text(json.dumps(index, indent=1, ensure_ascii=False))
    (C / "local" / "hard_iso_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(n, "word RMS", round(word_rms, 1))


if __name__ == "__main__":
    {"plan": plan, "render": render, "build": build}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
