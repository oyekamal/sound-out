#!/usr/bin/env python3
"""Quality gate for the local (Kokoro) renders (decision 30). Run with bakeoff/.venv/bin/python.

  local_gate.py sample            # pick the 60-clip sample + 20 L1 twins, render them (cache), whisper + phone check + voice stats
                                  #   -> content/local/gate_sample.json, bakeoff/l2_sample.html (+ bakeoff/l2_sample/*.ogg)
  local_gate.py reroll            # clips that failed: re-render once (speed x1.08, words also via text), re-check; still failing -> gate=fail
  local_gate.py words SHARD N    # gate EVERY local word clip (Whisper small.en + small after a 'Say.' carrier); fails re-roll once via Kokoro text
                                  #   mode at speed x1.08; still failing -> reclassified HARD (content/local/gate_words_<shard>.json)
  local_gate.py critic-input      # content/local/critic_input.md : the evidence the separate critic reads

Machine checks only; nothing here listens. Whisper small.en AND small, prompt-free, temperature 0: a sentence passes when either has
WER <= 0.12 (words in pron_overrides excluded); a word passes when either hears it, or hears a homophone (same CMUdict phones).
"""
import hashlib, json, random, re, sys, glob, os
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import gen_audio_local as L
import gen_audio_el as g
C = L.C
SAMPLE = C / "local" / "gate_sample.json"
PAGE_DIR = ROOT / "bakeoff" / "l2_sample"
WER_MAX = 0.12


def words_of(t): return re.findall(r"[a-z]+(?:'[a-z]+)?", re.sub(r"\*", "", t.lower()))


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def cmu():
    from audio_classify import load_cmu
    return load_cmu()


def phones(w, CM): return tuple(x.rstrip("012") for x in CM.get(w, [])) or None


_W = {}


def whisper_hear(x24, models=("small.en", "small")):
    import whisper
    for n in models:
        if n not in _W: _W[n] = whisper.load_model(n)
    y = resample_poly(x24, 2, 3).astype(np.float32)
    y = np.concatenate([np.zeros(8000, np.float32), y, np.zeros(8000, np.float32)])
    return {n: _W[n].transcribe(y, language="en", fp16=False, temperature=0, condition_on_previous_text=False)["text"].strip() for n in models}


def pick_sample(classes):
    rnd = random.Random(30)
    ren = L.renderable(classes)
    pools = {"word": [], "sentence": [], "passage": [], "instruction": [], "name": [], "ss-sentence": []}
    for k, v in ren.items():
        if v["sub"] == "name": pools["name"].append(k)
        elif v["kind"] == "ss":
            if v["sub"] != "word": pools["ss-sentence"].append(k)
        elif v["sub"] in pools: pools[v["sub"]].append(k)
    want = {"word": 18, "sentence": 14, "passage": 10, "instruction": 6, "name": 6, "ss-sentence": 6}
    out = []
    for p, n in want.items():
        pool = sorted(pools[p]); rnd.shuffle(pool)
        # spread over levels
        by = {}
        for k in pool: by.setdefault(ren[k]["level"], []).append(k)
        got = []
        while len(got) < n and any(by.values()):
            for lv in sorted(by):
                if by[lv] and len(got) < n: got.append(by[lv].pop())
        out += got
    return out


def render_keys(vs):
    """vs: {key: v} -> {key: (cache id, audio float)}; renders uncached inputs in-process."""
    import torch
    from kokoro import KModel, KPipeline
    torch.set_num_threads(int(os.environ.get("SO_THREADS", "8")))
    m = KModel(repo_id="hexgrad/Kokoro-82M").eval(); pipe = KPipeline(lang_code="a", model=m, repo_id="hexgrad/Kokoro-82M")
    snap = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices"))[0]
    vt = torch.load(f"{snap}/{L.VOICE}.pt", weights_only=True)
    L.RAW.mkdir(exist_ok=True); res = {}
    for k, v in vs.items():
        mode, inp = L.job(k, v); ci = L.ckey(mode, inp); w = L.RAW / f"{ci}.wav"
        if not w.exists():
            a = L.trim(L.render_one(pipe, m, vt, mode, inp, L.SPEED)); sf.write(w, a, L.SR, subtype="PCM_16")
        res[k] = (ci, sf.read(w)[0])
    return res, (m, pipe, vt)


def stats_for(x24):
    import librosa
    x16 = resample_poly(x24, 2, 3).astype(np.float32)
    f, vf, _ = librosa.pyin(x16, fmin=70, fmax=400, sr=16000, frame_length=1024)
    f = f[~np.isnan(f)]
    return {"sec": round(len(x24) / L.SR, 2), "f0": round(float(np.median(f)), 0) if len(f) else None}


CARRIER = None


def check(k, v, x, CM, ov, fast=False):
    """Machine checks for one clip; returns dict with pass flag. Single words are heard after a local 'Say.' carrier
    (Whisper is unreliable on a bare one-word clip; the River plan used the same carrier idea)."""
    r = {"key": k, "level": v["level"], "sub": v["sub"], "kind": v["kind"], "sec": round(len(x) / L.SR, 2)}
    xin = np.concatenate([CARRIER, np.zeros(int(.25 * L.SR)), x]) if v["kind"] in ("w", "ipa") and CARRIER is not None else x
    if fast and v["kind"] in ("w", "ipa"):   # bulk word gate: small.en first, `small` only when small.en misses
        tgt = v["say"].lower(); tp = phones(tgt, CM); heard = {}
        def hit(h):
            hw = words_of(h); return bool(hw) and (hw[-1] == tgt or tgt in hw or bool(tp and phones(hw[-1], CM) == tp))
        for n in ("small.en",):   # one model only: the full word gate is the CPU hog; the 60-clip sample used both
            heard.update(whisper_hear(xin, (n,)))
            if hit(heard[n]): break
        ok = any(hit(h) for h in heard.values())
        return {"key": k, "level": v["level"], "sub": v["sub"], "kind": v["kind"], "sec": round(len(x) / L.SR, 2), "heard": heard, "text": tgt,
                "wer": 0.0 if ok else 1.0, "pass": ok}
    heard = whisper_hear(xin); r["heard"] = heard
    if v["kind"] in ("w", "ipa"):
        tgt = v["say"].lower(); tp = phones(tgt, CM)
        ok = False
        for h in heard.values():
            hw = words_of(h)
            if hw and (hw[-1] == tgt or (tp and phones(hw[-1], CM) == tp) or tgt in hw): ok = True
        r["text"] = tgt; r["wer"] = 0.0 if ok else 1.0; r["pass"] = ok
        try:
            import phone_rec
            r["phone_per"], r["phone_heard"] = (lambda p: (round(p[0], 2), p[1]))(phone_rec.per(x, v["ipa"]))
        except Exception as e: r["phone_per"] = None
    else:
        t = v["text"]; tw = [w for w in words_of(L.clean_text(t)) if w not in ov and w.split("'")[0] not in ov]
        best = 9.0
        for h in heard.values():
            hw = [w for w in words_of(h) if w not in ov and w.split("'")[0] not in ov]
            best = min(best, ed(hw, tw) / max(1, len(tw)))
        r["text"] = L.clean_text(t)[:300]; r["wer"] = round(best, 3); r["pass"] = best <= WER_MAX
        if v.get("oov"): r["oov"] = v["oov"]
    return r


def carrier_load():
    global CARRIER
    f = C / "local" / "carrier_say.wav"
    if f.exists(): CARRIER = sf.read(f)[0]


def words(shard, n):
    import torch
    from kokoro import KModel, KPipeline
    torch.set_num_threads(int(os.environ.get("SO_THREADS", "4")))
    classes = json.loads((C / "audio_classes.json").read_text()); CM = cmu(); ren = L.renderable(classes)
    carrier_load()
    uniq = {}
    for k, v in sorted(ren.items()):
        if v["kind"] in ("w", "ipa"):
            mode, inp = L.job(k, v); uniq.setdefault(L.ckey(mode, inp), (k, v))
    ids = sorted(uniq)[shard::n]
    out_p = C / "local" / f"gate_words_{shard}.json"
    done = json.loads(out_p.read_text()) if out_p.exists() else {}
    m = KModel(repo_id="hexgrad/Kokoro-82M").eval(); pipe = KPipeline(lang_code="a", model=m, repo_id="hexgrad/Kokoro-82M")
    snap = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices"))[0]
    vt = torch.load(f"{snap}/{L.VOICE}.pt", weights_only=True)
    for j, ci in enumerate(ids):
        if ci in done: continue
        k, v = uniq[ci]; w = L.RAW / f"{ci}.wav"
        if not w.exists(): continue
        r = check(k, v, sf.read(w)[0], CM, {}, fast=True); rec = {"say": v["say"], "pass": r["pass"], "heard": r["heard"], "phone_per": r.get("phone_per")}
        if not r["pass"]:
            sp = round(L.SPEED * 1.08, 3); rci = L.ckey("text", v["say"] + ".", sp); rw = L.RAW / f"{rci}.wav"
            if not rw.exists(): sf.write(rw, L.trim(L.render_one(pipe, m, vt, "text", v["say"] + ".", sp)), L.SR, subtype="PCM_16")
            r2 = check(k, v, sf.read(rw)[0], CM, {}, fast=True)
            rec["reroll"] = {"cache": rci, "speed": sp, "mode": "text", "input": v["say"] + ".", "pass": r2["pass"], "heard": r2["heard"]}
        done[ci] = rec
        if j % 20 == 0:
            out_p.write_text(json.dumps(done, ensure_ascii=False)); print(f"shard {shard}: {j}/{len(ids)} pass1 {sum(d['pass'] for d in done.values())}/{len(done)}", flush=True)
    out_p.write_text(json.dumps(done, ensure_ascii=False))
    print(f"shard {shard} done: first-pass {sum(d['pass'] for d in done.values())}/{len(done)}; after re-roll {sum(d['pass'] or d.get('reroll', {}).get('pass', False) for d in done.values())}/{len(done)}")


def apply_words():
    """Fold content/local/gate_words_*.json into the manifest (gate = pass | pass-reroll | fail) per word key."""
    classes = json.loads((C / "audio_classes.json").read_text()); ren = L.renderable(classes)
    man = json.loads(L.MAN.read_text()) if L.MAN.exists() else {}
    res = {}
    for f in (C / "local").glob("gate_words_*.json"): res.update(json.loads(f.read_text()))
    n = {"pass": 0, "pass-reroll": 0, "fail": 0, "ungated": 0}
    for k, v in ren.items():
        if v["kind"] not in ("w", "ipa"): continue
        mode, inp = L.job(k, v); r = res.get(L.ckey(mode, inp))
        if r is None: n["ungated"] += 1; continue
        e = man.setdefault(k, {})
        if r["pass"]: e["gate"] = "pass"; e.pop("reroll", None)
        elif r.get("reroll", {}).get("pass"): e.update({"gate": "pass-reroll", "reroll": True, "cache": r["reroll"]["cache"], "mode": "text", "input": r["reroll"]["input"], "speed": r["reroll"]["speed"]})
        else: e["gate"] = "fail"
        n[e["gate"]] += 1
    L.MAN.write_text(json.dumps(man, indent=0, ensure_ascii=False)); print("word gate by key:", n)


def sample():
    classes = json.loads((C / "audio_classes.json").read_text()); CM = cmu(); ov = L.overrides()
    keys = pick_sample(classes); ren = L.renderable(classes)
    vs = {k: ren[k] for k in keys}
    # L1 twins: River exists for these, local renders of the same items
    plan = json.loads((C / "audio_plan.json").read_text()); idx = json.loads((C / "audio_index.json").read_text())["clips"]
    rnd = random.Random(31)
    tw_w = [k for k, c in plan.items() if k.startswith("w:") and c["cut"] == "last" and (k in idx) and idx[k].get("src") is None and c["say"] in CM]
    tw_s = [k for k, c in plan.items() if c["cut"] == "text" and k in idx and idx[k].get("src") is None and 2.0 < idx[k]["dur"] < 9 and k[:2] in ("re", "lt", "q:")]
    rnd.shuffle(tw_w); rnd.shuffle(tw_s)
    twins = {}
    for k in tw_w[:12]: twins[k] = {"kind": "w", "ipa": plan[k]["ipa"], "say": plan[k]["say"], "cut": "last", "level": 1, "sub": "word"}
    for k in tw_s[:8]: twins[k] = {"kind": "r", "cut": "text", "text": plan[k]["text"], "level": 1, "sub": "sentence"}
    allv = {**vs, **{"twin:" + k: v for k, v in twins.items()}}
    global CARRIER
    audio, (m, pipe, vt) = render_keys(allv)
    CARRIER = L.trim(L.render_one(pipe, m, vt, "text", "Say.", L.SPEED)); sf.write(C / "local" / "carrier_say.wav", CARRIER, L.SR)
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    res = {"samples": [], "twins": []}
    word_rms = float(np.median([g.rms_db(g.decode(ROOT / "app/public/audio" / f"{idx[k]['id']}.ogg")) for k in tw_w[:60]]))
    def ship(name, x):
        b, _ = g.loudness(x, word_rms); dst = PAGE_DIR / f"{name}.ogg"; g.encode(b, dst); return f"l2_sample/{name}.ogg"
    for k in keys:
        ci, x = audio[k]; r = check(k, vs[k], x, CM, ov); r["file"] = ship("s_" + ci[:10], x); r["cache"] = ci
        res["samples"].append(r); print(("PASS" if r["pass"] else "FAIL"), k, r["wer"], r["heard"], flush=True)
    for k, v in twins.items():
        ci, x = audio["twin:" + k]; r = check(k, v, x, CM, ov); r["file"] = ship("t_" + ci[:10], x); r["river"] = f"../app/public/audio/{idx[k]['id']}.ogg"
        res["twins"].append(r)
    SAMPLE.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    sp = [r for r in res["samples"]]
    print(f"sample pass {sum(r['pass'] for r in sp)}/{len(sp)}; twins pass {sum(r['pass'] for r in res['twins'])}/{len(res['twins'])}")
    page(res)


def page(res):
    rnd = random.Random(32); items = []
    for r in res["twins"]:
        first_local = rnd.random() < .5
        a, b = (r["file"], r["river"]) if first_local else (r["river"], r["file"])
        items.append((r["text"], a, b, "A" if first_local else "B"))
    rows = "\n".join(
        f'<div class=row><b>{i + 1}.</b> <i>{t[:140]}</i><br>A <audio controls preload=none src="{a}"></audio> B <audio controls preload=none src="{b}"></audio>'
        f' <button onclick="this.nextElementSibling.hidden=false">Reveal</button><span hidden> local = <b>{loc}</b></span></div>'
        for i, (t, a, b, loc) in enumerate(items))
    srows = "\n".join(
        f'<div class=row><span class={"ok" if r["pass"] else "bad"}>{"PASS" if r["pass"] else "FAIL"}</span> {r["key"]} (L{r["level"]}, {r["sub"]}, {r["sec"]}s, WER {r["wer"]}) '
        f'<audio controls preload=none src="{r["file"]}"></audio><br><small>text: {r["text"][:160]}<br>whisper: {r["heard"].get("small.en", "")[:160]}</small></div>'
        for r in res["samples"])
    ok = sum(r["pass"] for r in res["samples"])
    html = f"""<!doctype html><meta charset=utf-8><title>L2 local voice sample</title>
<style>body{{font:15px system-ui;max-width:860px;margin:2rem auto;padding:0 1rem}}.row{{margin:.7rem 0;padding:.5rem;border-bottom:1px solid #ddd}}.ok{{color:#070}}.bad{{color:#b00}}small{{color:#555}}</style>
<h1>Local (Kokoro {L.VOICE}) vs ElevenLabs River</h1>
<p>Serve the repo root: <code>python3 -m http.server</code> then open <code>/bakeoff/l2_sample.html</code>. Nobody has listened to these yet. Machine checks only.</p>
<h2>1. Blind A/B on the same items (Level 1 items River already voices)</h2>{rows}
<h2>2. The 60-clip gate sample (Levels 2-7, local only; River has none of these yet). Whisper pass {ok}/{len(res["samples"])}</h2>{srows}"""
    (ROOT / "bakeoff" / "l2_sample.html").write_text(html)


def reroll():
    classes = json.loads((C / "audio_classes.json").read_text()); CM = cmu(); ov = L.overrides(); ren = L.renderable(classes)
    res = json.loads(SAMPLE.read_text()); man = json.loads(L.MAN.read_text()) if L.MAN.exists() else {}
    fails = [r for r in res["samples"] if not r["pass"]]
    if not fails: print("nothing to re-roll"); return
    import torch
    global CARRIER
    audio, (m, pipe, vt) = render_keys({r["key"]: ren[r["key"]] for r in fails[:1]})
    CARRIER = L.trim(L.render_one(pipe, m, vt, "text", "Say.", L.SPEED))
    for r in fails:
        v = ren[r["key"]]; sp = round(L.SPEED * 1.08, 3)
        if v["kind"] in ("w", "ipa"): mode, inp = "text", v["say"] + "."
        else: mode, inp = L.job(r["key"], v)
        ci = L.ckey(mode, inp, sp); w = L.RAW / f"{ci}.wav"
        if not w.exists(): sf.write(w, L.trim(L.render_one(pipe, m, vt, mode, inp, sp)), L.SR, subtype="PCM_16")
        x = sf.read(w)[0]; r2 = check(r["key"], v, x, CM, ov)
        r["reroll"] = {"speed": sp, "mode": mode, "wer": r2["wer"], "pass": r2["pass"], "heard": r2["heard"]}
        man.setdefault(r["key"], {})["gate"] = "pass-reroll" if r2["pass"] else "fail"
        if r2["pass"]: man[r["key"]].update({"cache": ci, "mode": mode, "input": inp, "speed": sp, "reroll": True})
        print(r["key"], "reroll", "PASS" if r2["pass"] else "FAIL", r2["wer"])
    L.MAN.write_text(json.dumps(man, indent=0, ensure_ascii=False)); SAMPLE.write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    (lambda c: words(int(sys.argv[2]), int(sys.argv[3])) if c == "words" else apply_words() if c == "apply" else {"sample": sample, "reroll": reroll}.get(c, lambda: sys.exit(__doc__))())(sys.argv[1] if len(sys.argv) > 1 else "")
