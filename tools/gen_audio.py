#!/usr/bin/env python3
"""PROTOTYPE audio for Level 1 — Kokoro af_heart for EVERYTHING.

This is a placeholder voice. The real app records a human Sound Teacher for Levels 0-3
(decision 10); isolated phonemes here are Kokoro approximations and are marked placeholder.

  python3 tools/gen_audio.py plan            # write content/audio_plan.json (no TTS)
  <kokoro-venv>/bin/python tools/gen_audio.py render I N   # render shard I of N to wav cache
  python3 tools/gen_audio.py encode          # trim/pad/normalise/encode -> app/public/audio, audio_index.json

Ids = sha1(voice + "|" + source)[:12]. Words/pseudowords/foils/heart words are rendered from IPA
(one path, same session) so answer and foil clips match; UI lines and passages from text via misaki.
Words misaki cannot phonemize are skipped and logged (espeak fallback is disabled: it aborts).
"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
CACHE = ROOT / "tools" / ".audio_cache"   # gitignored wavs
OUT = ROOT / "app" / "public" / "audio"
VOICE = "af_heart"
# misaki/Kokoro alphabet for diphthongs
MISAKI = [("aɪ", "I"), ("eɪ", "A"), ("oʊ", "O"), ("aʊ", "W"), ("ɔɪ", "Y")]
CONTINUANT = {"s", "m", "n", "f", "l", "v", "z", "r", "h", "a", "i", "o", "e", "u", "w", "y", "j"}


def to_misaki(ipa):
    for a, b in MISAKI: ipa = ipa.replace(a, b)
    return ipa


def cid(src):
    return hashlib.sha1(f"{VOICE}|{src}".encode()).hexdigest()[:12]


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", text) if s.strip()]


def build_plan():
    lex = json.loads((C / "lexicon.json").read_text())
    opts = json.loads((C / "options.json").read_text())
    gpc = json.loads((C / "gpc.json").read_text())
    ui = json.loads((C / "ui_lines.json").read_text())
    clips = {}   # key -> {mode: ipa|text, src, placeholder?}
    def ph(key, ipa, **kw): clips[key] = {"mode": "ipa", "src": to_misaki(ipa), **kw}
    def tx(key, text, **kw): clips[key] = {"mode": "text", "src": text, **kw}
    for k, e in lex.items():
        ph(f"w:{k}", e["ipa"])
    for k, o in opts.items():   # tap-gate options keyed by IPA so a foil never borrows a homograph's clip
        for f in [o["target"], *o["foils"]]:
            ph(f"ipa:{f['ipa']}", f["ipa"])
    for pid, ipa in gpc["phonemes"].items():
        # isolated phoneme: Kokoro cannot produce a clean one; continuants lengthened, stops bare. PLACEHOLDER
        ph(f"ph:{pid}", ipa + ("ːː" if pid in CONTINUANT else ""), placeholder="kokoro isolated phoneme approximation")
    for letter, ipa in gpc["letterNames"].items():
        ph(f"name:{letter}", ipa)
    for k, t in ui.items(): tx(f"ui:{k}", t)
    for f in sorted((C / "lessons").glob("L1.*.json")):
        L = json.loads(f.read_text()); lid = L["id"]
        for s in L.get("sittings", []):
            hear = (s.get("hear") or {}).get("text", "")
            m = re.search(r'(?:start of|like|Say) ["“](\w+)', hear)
            if m: tx(f"ex:{lid}:{s['id']}", m.group(1) + ".")
        r = L.get("read") or {}
        for tr in ("A", "B"):
            t = (r.get(tr) or {}).get("text")
            if t:
                for i, sn in enumerate(sentences(t)): tx(f"read:{lid}:{tr}:{i}", sn)
        li = L.get("listen")
        if li:
            ss = sentences(li["passage"])
            chunks = [" ".join(ss[i:i + 2]) for i in range(0, len(ss), 2)]
            if li.get("title"): tx(f"lt:{lid}:title", li["title"] + ".")
            for i, ch in enumerate(chunks): tx(f"lt:{lid}:{i}", ch)
            for j, t2 in enumerate(li.get("tier2", [])[:1]):
                tx(f"t2:{lid}:{j}", f"{t2['word']}. {t2['word'][0].upper() + t2['word'][1:]} means {t2['def'][0].lower() + t2['def'][1:]}")
            for j, q in enumerate(li.get("questions", [])[:2]): tx(f"q:{lid}:{j}", q)
    for v in clips.values(): v["id"] = cid(v["mode"] + ":" + v["src"])
    (C / "audio_plan.json").write_text(json.dumps(clips, indent=1, ensure_ascii=False))
    print(f"plan: {len(clips)} clips, {len({v['id'] for v in clips.values()})} unique")


def render(shard, n):
    import numpy as np, soundfile as sf, torch
    torch.set_num_threads(4)
    from misaki import espeak as _e
    def _boom(*a, **k): raise RuntimeError("espeak fallback disabled")
    _e.EspeakFallback = _boom
    from kokoro import KPipeline, KModel
    model = KModel(repo_id="hexgrad/Kokoro-82M").to("cpu").eval()
    pipe = KPipeline(lang_code="a", model=False)
    pack = pipe.load_voice(VOICE)
    plan = json.loads((C / "audio_plan.json").read_text())
    CACHE.mkdir(exist_ok=True)
    uniq = sorted({v["id"]: v for v in plan.values()}.items())
    mine = [u for i, u in enumerate(uniq) if i % n == shard]
    log = []
    t0 = time.time()
    for cid_, v in mine:
        p = CACHE / f"{cid_}.wav"
        if p.exists(): continue
        try:
            with torch.no_grad():
                if v["mode"] == "ipa":
                    a = KPipeline.infer(model, v["src"], pack, 1.0).audio.numpy()
                else:
                    parts = [r.audio.numpy() for r in pipe(v["src"], voice=VOICE, speed=1.0, model=model) if r.audio is not None]
                    if not parts: raise RuntimeError("no audio (OOV)")
                    a = np.concatenate(parts)
            sf.write(p, a, 24000)
        except Exception as ex:
            log.append({"id": cid_, "src": v["src"], "error": str(ex)})
    (CACHE / f"skipped_{shard}.json").write_text(json.dumps(log, indent=1, ensure_ascii=False))
    print(f"shard {shard}: {len(mine)} clips in {time.time() - t0:.0f}s, skipped {len(log)}")


def encode():
    import numpy as np, soundfile as sf
    plan = json.loads((C / "audio_plan.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    def one(cid_):
        src = CACHE / f"{cid_}.wav"
        if not src.exists(): return cid_, None
        a, sr = sf.read(src)
        thr = 10 ** (-45 / 20) * max(1e-6, np.abs(a).max())
        idx = np.where(np.abs(a) > thr)[0]
        if len(idx): a = a[max(0, idx[0] - int(0.005 * sr)): idx[-1] + int(0.01 * sr)]
        a = np.concatenate([np.zeros(int(0.04 * sr)), a, np.zeros(int(0.08 * sr))])
        a = a * (10 ** (-3 / 20) / max(1e-6, np.abs(a).max()))
        tmp = CACHE / f"{cid_}.norm.wav"; sf.write(tmp, a, sr)
        dst = OUT / f"{cid_}.ogg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-c:a", "libopus", "-b:a", "32k", "-ac", "1", str(dst)], check=True)
        tmp.unlink()
        return cid_, round(len(a) / sr, 3)
    ids = sorted({v["id"] for v in plan.values()})
    with ThreadPoolExecutor(12) as ex: durs = dict(ex.map(one, ids))
    index, missing = {}, []
    for k, v in plan.items():
        if durs.get(v["id"]):
            index[k] = {"id": v["id"], "dur": durs[v["id"]], **({"placeholder": v["placeholder"]} if v.get("placeholder") else {})}
        else: missing.append({"key": k, "src": v["src"]})
    skipped = [s for f in CACHE.glob("skipped_*.json") for s in json.loads(f.read_text())]
    (C / "audio_index.json").write_text(json.dumps({"voice": VOICE, "note": "PROTOTYPE: Kokoro af_heart for everything; human Sound Teacher records L0-L3 later", "clips": index, "missing": missing, "skipped": skipped}, indent=1, ensure_ascii=False))
    size = sum(f.stat().st_size for f in OUT.glob("*.ogg"))
    print(f"encoded {sum(1 for d in durs.values() if d)} clips, {size/1e6:.1f} MB; missing keys {len(missing)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "plan": build_plan()
    elif cmd == "render": render(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "encode": encode()
