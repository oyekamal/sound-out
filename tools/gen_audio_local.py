#!/usr/bin/env python3
"""Local (Kokoro, CPU) renders for the EASY clips of Levels 2-7 (decision 30). Run with bakeoff/.venv/bin/python.

  gen_audio_local.py render [shard n_shards] [--limit N] [--keys file]   # resumable; raw wav cache, no ffmpeg
  gen_audio_local.py build                                                # post-chain -> app/public/audio + merge into content/audio_index.json

Inputs: content/audio_classes.json (tools/audio_classify.py). EASY clips, plus prose clips whose only trouble is a name
or a morpheme string (they get a hand pronunciation from content/local/pron_overrides.json, markdown-link syntax
[word](/ipa/) in Kokoro's text path).
Words (w:/ipa: keys): the course IPA goes straight to Kokoro as phonemes, the way Level 1's prototype did, so a foil and its
target differ by exactly the phoneme the lesson cares about. Text clips: Kokoro's own G2P.
Cache (raw 24 kHz wav, NOT committed: ~1 GB, deterministic from the weights): content/audio_raw_local/<sha1>.wav
  sha1(voice | speed | version | mode | input).  content/local/manifest.json records key -> cache id, input, gate results.
Same post-chain as gen_audio_el.build(): -18 LUFS (>= 0.4 s) or word-class RMS, true peak <= -1.5 dBTP, Opus 24 kbps, 40 ms / 80 ms pad.
"""
import hashlib, json, os, re, sys, glob, time
from pathlib import Path
import numpy as np, soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
C = ROOT / "content"
RAW = C / "audio_raw_local"
MAN = C / "local" / "manifest.json"
OUT = ROOT / "app/public/audio"
SR = 24000
VERSION = "v1"
CFG = json.loads((C / "local" / "voice.json").read_text()) if (C / "local" / "voice.json").exists() else {"voice": "af_river", "speed": 1.0}
VOICE, SPEED = CFG["voice"], CFG["speed"]
DIPH = [("aɪ", "I"), ("eɪ", "A"), ("oʊ", "O"), ("aʊ", "W"), ("ɔɪ", "Y")]


def to_misaki(ipa):
    for a, b in DIPH: ipa = ipa.replace(a, b)
    return ipa.replace("ɝ", "ɜɹ").replace("ɚ", "əɹ").replace("ʤ", "ʤ").replace("ʧ", "ʧ")


def clean_text(t):
    t = t.replace("**", "").replace("*", "").replace(" / ", " ").replace("_", "")
    return re.sub(r"\s+", " ", t).strip()


def overrides():
    p = C / "local" / "pron_overrides.json"
    return json.loads(p.read_text()) if p.exists() else {}


def with_overrides(text, ov):
    def rep(m):
        w = m.group(0); k = w.lower()
        if k in ov: return f"[{w}](/{ov[k]}/)"
        if k.endswith("'s") and k[:-2] in ov: return f"[{w}](/{ov[k[:-2]]}z/)"
        return w
    return re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", rep, text)


def job(key, v):
    """(mode, input) a clip is rendered from."""
    if v["kind"] in ("w", "ipa"): return "ipa", to_misaki(v["ipa"])
    if v["cut"] == "text": return "text", with_overrides(clean_text(v["text"]), overrides())
    raise ValueError(key)


def ckey(mode, inp, speed=None):
    return hashlib.sha1(f"{VOICE}|{speed or SPEED}|{VERSION}|{mode}|{inp}".encode()).hexdigest()


def renderable(classes):
    """EASY clips + name/morpheme prose (rendered with overrides)."""
    return {k: v for k, v in classes.items() if v["kind"] != "iso" and
            (v["class"] == "easy" or (v["sub"] == "name" and v["cut"] == "text"))}


def trim(a, thr_db=-48.0):
    thr = 10 ** (thr_db / 20); nz = np.where(np.abs(a) > thr)[0]
    return a[max(0, nz[0] - int(.015 * SR)): nz[-1] + int(.04 * SR)] if len(nz) else a


def render_one(pipe, model, voice_t, mode, inp, speed):
    import torch
    from kokoro import KPipeline
    if mode == "ipa":
        with torch.no_grad(): return KPipeline.infer(model, inp, voice_t, speed=speed).audio.numpy()
    parts = [r.audio.numpy() for r in pipe(inp, voice=voice_t, speed=speed) if r.audio is not None]
    gap = np.zeros(int(.12 * SR), dtype=np.float32)
    return np.concatenate([x for p in parts for x in (p, gap)][:-1]) if parts else np.zeros(0, np.float32)


def render(shard=0, n=1, limit=None, keys=None):
    import torch
    from kokoro import KModel, KPipeline
    torch.set_num_threads(int(os.environ.get("SO_THREADS", "4")))
    classes = json.loads((C / "audio_classes.json").read_text())
    todo = renderable(classes)
    if keys: todo = {k: v for k, v in todo.items() if k in set(json.loads(Path(keys).read_text()))}
    jobs = {}
    for k, v in todo.items():
        mode, inp = job(k, v); jobs.setdefault(ckey(mode, inp), (mode, inp))
    ids = sorted(jobs)[shard::n]
    ids = [i for i in ids if not (RAW / f"{i}.wav").exists()]
    if limit: ids = ids[:limit]
    print(f"shard {shard}/{n}: {len(ids)} to render of {len(jobs)} unique inputs ({len(todo)} keys), voice {VOICE} speed {SPEED}", flush=True)
    RAW.mkdir(exist_ok=True)
    m = KModel(repo_id="hexgrad/Kokoro-82M").eval(); pipe = KPipeline(lang_code="a", model=m, repo_id="hexgrad/Kokoro-82M")
    snap = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices"))[0]
    vt = torch.load(f"{snap}/{VOICE}.pt", weights_only=True)
    t0 = time.time(); audio_s = 0.0
    for j, i in enumerate(ids):
        mode, inp = jobs[i]
        try: a = render_one(pipe, m, vt, mode, inp, SPEED)
        except Exception as e:
            print("FAIL", mode, repr(inp)[:80], e, flush=True); continue
        a = trim(a); audio_s += len(a) / SR
        sf.write(RAW / f"{i}.tmp.wav", a, SR, subtype="PCM_16"); os.replace(RAW / f"{i}.tmp.wav", RAW / f"{i}.wav")
        if j % 50 == 0: print(f"  {j}/{len(ids)} {time.time() - t0:.0f}s wall, {audio_s:.0f}s audio, rtf {(time.time() - t0) / max(audio_s, 1e-9):.2f}", flush=True)
    print(f"shard {shard} done {time.time() - t0:.0f}s wall for {audio_s:.0f}s audio", flush=True)


def build(shard=0, n=1, encode_only=False):
    import gen_audio_el as g
    classes = json.loads((C / "audio_classes.json").read_text())
    todo = renderable(classes)
    idx_path = C / "audio_index.json"
    index = json.loads(idx_path.read_text())
    clips = index["clips"]
    # word-class RMS from the shipped Level 1 River words, so local words sit at the same level
    rr = []
    for k, v in clips.items():
        if k.startswith("w:") and v.get("src") is None and v["dur"] > 0.55 and len(rr) < 150:
            rr.append(g.rms_db(g.decode(OUT / f"{v['id']}.ogg")))
    word_rms = float(np.median(rr)) if rr else -24.0
    man = json.loads(MAN.read_text()) if MAN.exists() else {}
    done = enc_n = 0
    for j, (k, v) in enumerate(sorted(todo.items())):
        if j % n != shard: continue
        mode, inp = job(k, v); ci = ckey(mode, inp)
        m0 = man.get(k, {})
        if m0.get("reroll") and (RAW / f"{m0['cache']}.wav").exists(): ci = m0["cache"]   # passed on its one re-roll
        w = RAW / f"{ci}.wav"
        if not w.exists(): continue
        if m0.get("gate") == "fail": continue          # failed the gate twice: reclassified HARD, not shipped
        if v["kind"] in ("w", "ipa") and m0.get("gate") not in ("pass", "pass-reroll"): continue   # single words ship only after the full word gate
        cid = hashlib.sha1(f"local|{ci}".encode()).hexdigest()[:12]
        dst = OUT / f"{cid}.ogg"
        if not dst.exists():
            a, _ = sf.read(w)
            b, rule = g.loudness(a, word_rms)
            g.encode(b, dst)
            if rule.startswith("lufs"):
                gain = 0.0
                for _ in range(4):
                    L = g.lufs(g.decode(dst))
                    if L is None or abs(g.LUFS - L) <= 0.3: break
                    gain += g.LUFS - L; g.encode(b * 10 ** (gain / 20), dst)
            enc_n += 1
        if encode_only: continue
        dur = round(len(g.decode(dst)) / SR, 3) if not dst.stat().st_size == 0 else 0
        clips[k] = {"id": cid, "dur": dur, "src": "local"}
        man.setdefault(k, {}).update({"cache": ci, "voice": VOICE})
        if not m0.get("reroll"): man[k].update({"mode": mode, "input": inp, "speed": SPEED})
        done += 1
    if encode_only: print(f"shard {shard}: encoded {enc_n}"); return
    index["note"] = (index.get("note", "").split(" | local:")[0] +
                     f" | local: Kokoro {VOICE} speed {SPEED} for EASY L2-L7 clips (decision 30, tools/gen_audio_local.py); src='local' marks them")
    idx_path.write_text(json.dumps(index, indent=1, ensure_ascii=False))
    MAN.write_text(json.dumps(man, indent=0, ensure_ascii=False))
    print(f"index: {done} local clips ({enc_n} newly encoded); word RMS target {word_rms:.1f} dBFS; total keys {len(clips)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    def opt(n, d=None):
        return a[a.index(n) + 1] if n in a else d
    if a[0] == "render":
        pos = [x for x in a[1:] if not x.startswith("--") and x not in (opt("--limit"), opt("--keys"))]
        render(int(pos[0]) if pos else 0, int(pos[1]) if len(pos) > 1 else 1, int(opt("--limit")) if opt("--limit") else None, opt("--keys"))
    elif a[0] == "build":
        pos = [x for x in a[1:] if not x.startswith("--")]
        build(int(pos[0]) if pos else 0, int(pos[1]) if len(pos) > 1 else 1, "--encode-only" in a)
    else: sys.exit(__doc__)
