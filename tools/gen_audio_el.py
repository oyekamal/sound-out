#!/usr/bin/env python3
"""Level 1 audio from ONE ElevenLabs English voice (decision 18). Pre-rendered at build time, shipped as files.

  python3 tools/gen_audio_el.py audition            # 3 candidate voices -> app/public/voices.html data
  python3 tools/gen_audio_el.py plan                # content/audio_plan.json (what each key renders, no API)
  python3 tools/gen_audio_el.py render              # every uncached request, 3 concurrent, with timestamps
  python3 tools/gen_audio_el.py build               # cut words + isolated sounds (tools/iso_sounds.py picks) + loudness + encode -> app/public/audio,
                                                    # content/audio_index.json, listen-data.json, coverage.md
Key: ELEVENLABS_API_KEY in env or ./.env (gitignored). Stdlib + numpy/scipy/soundfile + ffmpeg.

Cache (committed): content/audio_raw/<sha1(voice|model|settings|text)>.wav + .json (alignment). Same voice, model,
settings and text = same file, so re-runs cost nothing. Clip ids = sha1(request key | cut)[:12].
Words and pseudowords are spoken in a carrier ("Say: vop.") and the last word is cut out on silence, located by
the ElevenLabs word timestamps (character timestamps are interpolated, so phoneme cuts are found acoustically).
"""
import base64, hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
C, OUT, PUB = ROOT / "content", ROOT / "app/public/audio", ROOT / "app/public"
CACHE = ROOT / "content/audio_raw"   # raw ElevenLabs renders + timestamp JSON, committed
SR = 24000
MODEL = os.environ.get("SO_EL_MODEL", "eleven_v4")
VOICE = os.environ.get("SO_EL_VOICE", "")            # filled from content/voice.json after the audition
SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 0.9}
CANDIDATES = {  # premade voices, General American; picked from /v2/voices for warm + clear + not childish
    "hpp4J3VqNfWAUOO0d1Us": "Bella",
    "XrExE9yKIg1WjnnlVkGX": "Matilda",
    "SAz9YHcvj6GT2YYXdXww": "River",
}
CHAR_STOP = 30000
LUFS, TP, MIN_LUFS_DUR = -18.0, -1.5, 0.4


# ---------------------------------------------------------------- API + cache
def api_key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    env = ROOT / ".env"
    if not k and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                k = line.split("=", 1)[1].strip().strip('"')
    if not k: sys.exit("ELEVENLABS_API_KEY missing (env or ./.env)")
    return k


def api(path, body=None):
    req = urllib.request.Request(f"https://api.elevenlabs.io{path}", method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"xi-api-key": api_key(), "Content-Type": "application/json"})
    for i in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 5:   # plan allows 3 concurrent; back off
                time.sleep(3 * (i + 1)); continue
            raise RuntimeError(f"ElevenLabs {e.code}: {e.read()[:300].decode(errors='replace')}") from None


def rkey(voice, text, model=None, settings=None):
    model = model or MODEL
    return hashlib.sha1(f"{voice}|{model}|{json.dumps(settings or SETTINGS, sort_keys=True)}|{text}".encode()).hexdigest()


def tts(voice, text, model=None, settings=None):
    """Cached render with timestamps. Returns (float audio @24k, alignment dict)."""
    model = model or MODEL; settings = settings or SETTINGS
    k = rkey(voice, text, model, settings); wav, js = CACHE / f"{k}.wav", CACHE / f"{k}.json"
    if not wav.exists():
        body = {"text": text, "model_id": model, "voice_settings": settings, "seed": 18, "language_code": "en"}
        d = api(f"/v1/text-to-speech/{voice}/with-timestamps?output_format=pcm_24000", body)
        a = np.frombuffer(base64.b64decode(d["audio_base64"]), dtype="<i2").astype(np.float64) / 32768
        CACHE.mkdir(parents=True, exist_ok=True)
        js.write_text(json.dumps({"voice": voice, "model": model, "settings": settings, "text": text,
                                  "alignment": d.get("alignment"), "normalized_alignment": d.get("normalized_alignment")}))
        sf.write(wav, a, SR, subtype="PCM_16")
    a, _ = sf.read(wav)
    return a, json.loads(js.read_text())["alignment"]


def cached(voice, text): return (CACHE / f"{rkey(voice, text)}.wav").exists()


def render_all(reqs, voice):
    todo = sorted({t for t in reqs if not cached(voice, t)})
    chars = sum(len(t) for t in todo)
    print(f"{len(todo)} uncached requests, {chars} characters ({MODEL}, voice {voice})")
    if chars > CHAR_STOP: sys.exit(f"STOP: {chars} characters > {CHAR_STOP}; not rendering")
    fails = []
    def one(t):
        try: tts(voice, t)
        except Exception as e: fails.append((t, str(e)))
    with ThreadPoolExecutor(3) as ex: list(ex.map(one, todo))
    for t, e in fails: print("FAIL", repr(t), e)
    return chars, fails


# ---------------------------------------------------------------- signal helpers
FR = int(0.01 * SR)


def frames_db(a):
    n = len(a) // FR
    r = np.sqrt((a[:n * FR].reshape(n, FR) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r)


def gaps(a, thr_db=-50.0, min_ms=40):
    """Silent stretches [(start_s, end_s)] where 10 ms frames sit below thr_db (absolute dBFS)."""
    db = frames_db(a); out, s = [], None
    for i, v in enumerate(db < thr_db):
        if v and s is None: s = i
        if not v and s is not None:
            if (i - s) * 10 >= min_ms: out.append((s / 100, i / 100))
            s = None
    if s is not None and (len(db) - s) * 10 >= min_ms: out.append((s / 100, len(db) / 100))
    return out


def trim(a, thr_db=-45.0):
    thr = 10 ** (thr_db / 20); nz = np.where(np.abs(a) > thr)[0]
    return a[nz[0]: nz[-1] + 1] if len(nz) else a[:0]


def word_span(text, al, word):
    """(start, end) seconds of the LAST occurrence of `word` in `text` from character timestamps."""
    i = text.rfind(word)
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    return st[i], en[i + len(word) - 1]


def cut_last(a, text, al, word):
    """The last word of a carrier render: from the end of the silent gap before it to the end of sound."""
    t0, _ = word_span(text, al, word)
    g = [x for x in gaps(a) if x[0] < t0 + 0.12]          # gaps that start before the word's onset (+ slack)
    # the carrier pause is the LONGEST such gap (~0.35 s); a later short one is a stop closure inside the word
    # ("stat", "scat": taking the last gap dropped the /s/)
    start = max(g, key=lambda x: x[1] - x[0])[1] if g else max(0.0, t0 - 0.05)
    # a stop-initial word's closure merges with the pause; the gap end is the burst. Weak onsets (/f/ /h/) sit
    # below -50 dB for a frame or two, so step back 15 ms; the -45 dBFS trim takes off anything silent.
    seg = a[max(0, int((start - 0.015) * SR)):]
    return trim(seg)


def open_cut(w):
    """Open syllable from a CVC carrier ("sat" -> "sa"): keep up to where the vowel energy falls 20 dB below its peak
    (the final stop's closure), minus 10 ms so no closure transition is left."""
    db = frames_db(w); ipk = int(np.argmax(db)); pk = db[ipk]
    end = next((i for i in range(ipk, len(db)) if db[i] < pk - 20), len(db))
    return trim(w[:max(FR, end * FR - int(.01 * SR))])


def zcr(x): return float(np.mean(np.abs(np.diff(np.sign(x)))) / 2) if len(x) > 2 else 0.0


def periodicity(x):
    """Peak normalised autocorrelation in 80-400 Hz: ~1 voiced, ~0 noise."""
    if len(x) < 240: return 0.0
    x = x - x.mean(); e = float((x * x).sum())
    if e < 1e-9: return 0.0
    ac = np.correlate(x, x, "full")[len(x) - 1:]
    return float(ac[SR // 400: SR // 80].max() / ac[0])


def lufs(a):
    """BS.1770 integrated loudness (K-weighting, 400 ms blocks 75% overlap, -70 abs / -10 rel gates)."""
    if len(a) < int(0.4 * SR): return None
    # K-weighting at 24 kHz: high-shelf (+4 dB above ~1.5 kHz) then RLB high-pass ~38 Hz (bilinear designs)
    import scipy.signal as ss
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = np.tan(np.pi * f0 / SR); Vh = 10 ** (G / 20); Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b1 = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a1 = [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    f0, Q = 38.13547087602444, 0.5003270373238773; K = np.tan(np.pi * f0 / SR)
    b2 = [1, -2, 1]; a2 = [1, 2 * (K * K - 1) / (1 + K / Q + K * K), (1 - K / Q + K * K) / (1 + K / Q + K * K)]
    y = ss.lfilter(b2, a2, ss.lfilter(b1, a1, a))
    B, H = int(0.4 * SR), int(0.1 * SR)
    z = np.array([np.mean(y[i:i + B] ** 2) for i in range(0, len(y) - B + 1, H)])
    L = -0.691 + 10 * np.log10(z + 1e-15)
    z = z[L > -70]
    if not len(z): return None
    rel = -0.691 + 10 * np.log10(z.mean()) - 10
    z = z[(-0.691 + 10 * np.log10(z + 1e-15)) > rel]
    return float(-0.691 + 10 * np.log10(z.mean()))


def true_peak_db(a):
    return 20 * np.log10(np.abs(resample_poly(a, 4, 1)).max() + 1e-12)


def rms_db(a):
    t = trim(a, -45) if len(trim(a, -45)) else a
    return 20 * np.log10(np.sqrt(np.mean(t ** 2)) + 1e-12)


def fades(a, ms_in=3, ms_out=8):
    a = a.copy(); i, o = int(ms_in * SR / 1000), int(ms_out * SR / 1000)
    if len(a) > i + o:
        a[:i] *= np.linspace(0, 1, i); a[-o:] *= np.linspace(1, 0, o)
    return a


def loudness(a, word_rms=None):
    """-18 LUFS for clips >= 0.4 s; shorter clips RMS-matched to the word class; true peak <= -1.5 dBTP (gain only)."""
    L = lufs(a) if len(a) >= MIN_LUFS_DUR * SR else None
    if L is not None: g = LUFS - L; rule = "lufs"
    else: g = (word_rms if word_rms is not None else -24.0) - rms_db(a); rule = "rms"
    a = a * 10 ** (g / 20)
    if true_peak_db(a) > TP - 1.5: rule += "+limiter"   # encode() runs a -3 dBFS look-ahead limiter: loudness kept, TP <= -1.5
    return a, rule


def encode(a, dst):
    a = np.concatenate([np.zeros(int(.04 * SR)), a, np.zeros(int(.08 * SR))])
    tmp = dst.with_suffix(".wav"); sf.write(tmp, a, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp),
                    "-af", "aresample=96000,alimiter=limit=0.708:attack=2:release=40:level=disabled,aresample=24000",
                    "-c:a", "libopus", "-b:a", "24k", "-ac", "1",
                    str(dst)], check=True)
    tmp.unlink()
    return round(len(a) / SR, 3)


def decode(src):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(src), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").astype(np.float64)


# ---------------------------------------------------------------- what each key says
PSEUDO_RESPELL = {  # course spelling -> what the TTS is given (ambiguous spellings only); matched by IPA, not text
    "sˈæs": "sass", "tˈæs": "tass", "nˈæs": "nass", "pˈæs": "pass", "tˈɪs": "tiss", "nˈɪs": "niss", "ˈɪs": "iss",
    "hˈæs": "hass", "ʤˈɪz": "jiz", "sˈɪz": "siz", "kˈæk": "kack", "kˈɪd": "kid", "sˈɑk": "sock", "kˈɛk": "keck", "hˈæk": "hack", "ˈætt": "at",
    "lˈɑdd": "lod", "ʌ": "uh", "ˈɪz": "is", "fˈɛs": "fess", "nˈʌz": "nuzz", "sˈɛd": "said", "sˈɛlz": "sells", "tˈɛlz": "tells",
}
if (C / "foil_respell.json").exists(): PSEUDO_RESPELL.update(json.loads((C / "foil_respell.json").read_text()))   # tools/check_foils.py --fix (whisper-checked respellings)
OPEN = {"sˈæ": "sat", "stˈæ": "stat", "skˈæ": "scat"}   # open syllables: cut from a carrier render, before the final stop's closure


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", text) if s.strip()]


def say_for(ipa, spelling):
    if ipa in PSEUDO_RESPELL: return PSEUDO_RESPELL[ipa]
    if re.search(r"[^aeiouz]zz$", spelling): return spelling[:-2] + "s"   # course foils "hagzz" -> "hags" (/z/ after a consonant)
    return spelling


def build_plan():
    lex = json.loads((C / "lexicon.json").read_text())
    opts = json.loads((C / "options.json").read_text())
    gpc = json.loads((C / "gpc.json").read_text())
    ui = json.loads((C / "ui_lines.json").read_text())
    ipa_spell = {}
    for e in lex.values(): ipa_spell.setdefault(e["ipa"], e["w"])
    for o in opts.values():
        for f in [o["target"], *o["foils"]]: ipa_spell.setdefault(f["ipa"], f["w"])
    clips = {}
    def word(key, ipa, spelling):
        if ipa in OPEN: clips[key] = {"cut": "open", "say": OPEN[ipa], "ipa": ipa}
        else: clips[key] = {"cut": "last", "say": say_for(ipa, spelling), "ipa": ipa}
    for k, e in lex.items(): word(f"w:{k}", e["ipa"], e["w"])
    for ipa, w in ipa_spell.items(): word(f"ipa:{ipa}", ipa, w)
    for pid in gpc["phonemes"]: clips[f"ph:{pid}"] = {"cut": "phone", "pid": pid}
    NAME = {"w": "double-u"}
    for letter in gpc["letterNames"]: clips[f"name:{letter}"] = {"cut": "letter", "say": NAME.get(letter, letter.upper())}
    for k, t in ui.items(): clips[f"ui:{k}"] = {"cut": "text", "text": t}
    for f in sorted((C / "lessons").glob("L1.*.json")):
        L = json.loads(f.read_text()); lid = L["id"]
        for s in L.get("sittings", []):
            m = re.search(r'(?:start of|like|Say) ["“](\w+)', (s.get("hear") or {}).get("text", ""))
            if m: clips[f"ex:{lid}:{s['id']}"] = {"cut": "last", "say": m.group(1)}
        r = L.get("read") or {}
        for tr in ("A", "B"):
            t = (r.get(tr) or {}).get("text")
            if t:
                for i, sn in enumerate(sentences(t)): clips[f"read:{lid}:{tr}:{i}"] = {"cut": "text", "text": sn}
        li = L.get("listen")
        if li:
            ss = sentences(li["passage"])
            if li.get("title"): clips[f"lt:{lid}:title"] = {"cut": "text", "text": li["title"] + "."}
            for i in range(0, len(ss), 2): clips[f"lt:{lid}:{i // 2}"] = {"cut": "text", "text": " ".join(ss[i:i + 2])}
            for j, t2 in enumerate(li.get("tier2", [])[:1]):
                clips[f"t2:{lid}:{j}"] = {"cut": "text", "text": f"{t2['word']}. {t2['word'][0].upper() + t2['word'][1:]} means {t2['def'][0].lower() + t2['def'][1:]}"}
            for j, q in enumerate(li.get("questions", [])[:2]): clips[f"q:{lid}:{j}"] = {"cut": "text", "text": q}
    (C / "audio_plan.json").write_text(json.dumps(clips, indent=1, ensure_ascii=False))
    print(f"plan: {len(clips)} keys, {len(requests(clips))} requests, {sum(len(t) for t in requests(clips))} characters")
    return clips


def req_text(c):
    if c["cut"] in ("last", "open"): return f"Say: {c['say']}."
    if c["cut"] == "letter": return f"The letter {c['say']}."
    if c["cut"] == "text": return c["text"]
    return None


def requests(clips):
    return {req_text(c) for c in clips.values() if req_text(c)}


# Isolated sounds (ph:*) are DIRECT renders in the same voice, picked by tools/iso_sounds.py (decision 19: slicing
# dropped after Kamal's listen). Example words for the listen page: lexicon words where they exist, else rendered here.
EXAMPLE = {"s": "sat", "a": "apple", "t": "tap", "p": "pat", "i": "igloo", "n": "nap", "m": "map", "d": "dip", "g": "got",
           "o": "octopus", "c": "cat", "k": "kit", "ck": "sock", "e": "egg", "u": "umbrella", "r": "rat", "h": "hat",
           "b": "bat", "f": "fan", "l": "lap", "ff": "off", "ll": "bell", "ss": "kiss", "zz": "buzz", "j": "jam", "v": "van",
           "w": "wet", "x": "box", "y": "yes", "z": "zip", "qu": "quit"}


# ---------------------------------------------------------------- build
def get_voice():
    vf = C / "voice.json"
    v = VOICE or (json.loads(vf.read_text())["voice_id"] if vf.exists() else "")
    if not v: sys.exit("no voice chosen: run audition, write content/voice.json")
    return v


def build():
    import iso_sounds
    voice = get_voice()
    clips = json.loads((C / "audio_plan.json").read_text())
    gpc = json.loads((C / "gpc.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    raw = {}
    for key, c in clips.items():
        t = req_text(c)
        if not t: continue
        a, al = tts(voice, t)
        if c["cut"] in ("last", "letter"): a = cut_last(a, t, al, c["say"])
        elif c["cut"] == "open":
            w = cut_last(a, t, al, c["say"])
            a = open_cut(w)
        else: a = trim(a)
        raw[key] = a
    # isolated sounds: the picked direct take per phoneme (no API call when every take is cached)
    iso, res, _ = iso_sounds.pick_all(voice, do_render=False)
    iso_key = {}
    for pid, x in iso.items():
        raw[f"ph:{pid}"] = x
        t = res[pid]["takes"][res[pid]["pick"]]
        iso_key[f"ph:{pid}"] = f"{t['model']}|{t['text']}|{t['flat_settings']}|{t['measures'].get('ms')}"
    # example words not in the lexicon (listen page only)
    for gph, w in EXAMPLE.items():
        if f"w:{w}" not in clips:
            t = f"Say: {w}."; a, al = tts(voice, t); raw[f"exw:{w}"] = cut_last(a, t, al, w)
    # loudness: words class RMS (after -18 LUFS on >=0.4 s words) is the target for short clips AND isolated sounds
    word_keys = [k for k in raw if k.startswith(("w:", "ipa:"))]
    longw = [loudness(raw[k])[0] for k in word_keys if len(raw[k]) >= MIN_LUFS_DUR * SR]
    word_rms = float(np.median([rms_db(x) for x in longw])) if longw else -24.0
    def enc(a, cid, force_rms=False):
        if force_rms:
            b, rule = a * 10 ** ((word_rms - rms_db(a)) / 20), "rms"
        else:
            b, rule = loudness(a, word_rms)
        dst = OUT / f"{cid}.ogg"
        d = encode(b, dst)
        if force_rms:   # Opus at 24 kb/s drops some fricative energy: measure the SHIPPED file, correct to the word RMS
            gain = 0.0
            for _ in range(3):
                e = word_rms - rms_db(decode(dst))
                if abs(e) <= 0.3: break
                gain += e; encode(b * 10 ** (gain / 20), dst)
        if rule.startswith("lufs"):   # measure the SHIPPED file (padding + limiter + Opus) and correct once
            gain = 0.0
            for _ in range(4):   # the limiter eats loudness on peaky clips, so converge in a few passes
                L = lufs(decode(dst))
                if L is None or abs(LUFS - L) <= 0.3: break
                gain += LUFS - L; encode(b * 10 ** (gain / 20), dst)
        return d, rule
    old = {p.name for p in OUT.glob("*.ogg")}
    index, rules = {}, {}
    def cid_for(key):
        if key in iso_key: return hashlib.sha1(f"iso|{voice}|{iso_key[key]}".encode()).hexdigest()[:12]
        if key.startswith("exw:"): return hashlib.sha1(f"{rkey(voice, 'Say: ' + key[4:] + '.')}|last".encode()).hexdigest()[:12]
        c = clips[key]
        return hashlib.sha1(f"{rkey(voice, req_text(c) or '')}|{c['cut']}|{c.get('pid', '')}|\"\"".encode()).hexdigest()[:12]
    for key in list(clips) + [k for k in raw if k.startswith("exw:")]:
        if key not in raw or not len(raw[key]): continue
        cid = cid_for(key)
        if cid not in rules: rules[cid] = enc(raw[key], cid, force_rms=key.startswith("ph:"))
        d, rule = rules[cid]
        index[key] = {"id": cid, "dur": d}
    # decision 30: carry over L2-L7 clips from tools/gen_audio_local.py / gen_audio_hard.py (src='local'|'elevenlabs') so a rebuild never deletes them
    prev_p = C / "audio_index.json"
    if prev_p.exists():
        for k, v in json.loads(prev_p.read_text()).get("clips", {}).items():
            if v.get("src") and k not in index: index[k] = v
    keep = {f"{v['id']}.ogg" for v in index.values()}
    for n in old - keep: (OUT / n).unlink()
    # shipped isolated sounds: measure what the app actually plays
    shipped = {}
    for pid in iso:
        x = decode(OUT / f"{index['ph:' + pid]['id']}.ogg")
        shipped[pid] = {"rms_db": round(float(rms_db(x)), 1), "true_peak_db": round(float(true_peak_db(x)), 2), "file_s": index["ph:" + pid]["dur"]}
    names = json.loads((C / "voice.json").read_text())
    (C / "audio_index.json").write_text(json.dumps({"voice": f"ElevenLabs {names['name']} ({voice})", "model": MODEL, "settings": SETTINGS,
        "note": "ElevenLabs, one voice for everything (decision 18); isolated sounds = direct renders (decision 19, tools/iso_sounds.py); tools/gen_audio_el.py",
        "clips": index, "missing": [k for k in clips if k not in index], "skipped": []}, indent=1, ensure_ascii=False))
    # listen page: one row per Level 1 spelling
    rows = []
    for o in gpc["order"]:
        gph, pid = o["g"], o["p"]
        w = EXAMPLE[gph]; wk = f"w:{w}" if f"w:{w}" in index else f"exw:{w}"
        letter = "q" if gph == "qu" else gph if len(gph) == 1 else None
        rows.append({"g": gph, "pid": pid, "sound": index[f"ph:{pid}"]["id"], "name": index[f"name:{letter}"]["id"] if letter else None,
                     "nameLabel": letter.upper() if letter else None, "word": w, "wordId": index[wk]["id"],
                     "ms": res[pid]["takes"][res[pid]["pick"]]["measures"].get("ms")})
    (PUB / "listen-data.json").write_text(json.dumps({"voice": names["name"], "rows": rows,
        "blend": [index[k]["id"] for k in ("ph:s", "ph:a", "ph:t")], "sat": index["w:sat"]["id"]}, indent=1, ensure_ascii=False))
    write_coverage(res, shipped, names["name"])
    size = sum(f.stat().st_size for f in OUT.glob("*.ogg"))
    print(f"encoded {len(index)} keys / {len(rules)} clips, {size / 1e6:.1f} MB; word RMS {word_rms:.1f} dBFS; removed {len(old - keep)} old files")
    for pid, m in shipped.items(): print(f"  ph:{pid:3s} {m}")
    return res, shipped


def write_coverage(res, shipped, vname):
    cov = C / "coverage.md"
    txt = cov.read_text().split("\n## Isolated sounds")[0].rstrip() + "\n\n"
    txt += (f"## Isolated sounds: direct renders in the app voice ({vname}; tools/iso_sounds.py, decision 19)\n\n"
            "No slicing. Each sound is its own ElevenLabs render, three prompt forms per sound, picked by machine checks "
            "(hums m n l r v z: 300-350 ms, F0 range <= 2 st, swell <= 3 dB, not breathier than the voice's words; "
            "s f h: 400-600 ms, no vowel, swell <= 3 dB; vowels: 300-400 ms audible, F1/F2 within 1.5 Bark of the vowel in "
            "River's own word; stops: <= 220 ms, vowel tail <= 60 ms; w y: <= 250 ms, tail <= 120 ms). RMS = the word class; "
            "true peak <= -1.5 dBTP. **Kamal's ears decide.**\n\n"
            "| Sound | Class | Picked take | Model | ms | RMS dBFS | TP dBTP | Verdict |\n|---|---|---|---|---|---|---|---|\n")
    for pid, r in res.items():
        t = r["takes"][r["pick"]]; sh = shipped[pid]
        txt += f"| {pid} | {r['class']} | `{t['text'][-40:]}` | {t['model']} | {t['measures'].get('ms')} | {sh['rms_db']} | {sh['true_peak_db']} | {r['verdict']} |\n"
    cov.write_text(txt)


# ---------------------------------------------------------------- audition
AUDITION = [("sss", "sustained", "Sssss."), ("mmm", "sustained", "Mmmmm."), ("a (apple)", "slice", "Say: apple."),
            ("sat", "word", "Say: sat."), ("pin", "word", "Say: pin."), ("ship", "word", "Say: ship."),
            ("garden", "word", "Say: garden."), ("vop", "pseudo", "Say: vop."), ("The cat sat on the mat.", "text", "The cat sat on the mat.")]


def audition():
    dst = PUB / "audition"; dst.mkdir(parents=True, exist_ok=True)
    reqs = [(v, t) for v in CANDIDATES for _, _, t in AUDITION]
    chars = sum(len(t) for v, t in reqs if not cached(v, t))
    print(f"audition: {chars} uncached characters"); assert chars <= 2000
    with ThreadPoolExecutor(3) as ex: list(ex.map(lambda vt: tts(*vt), reqs))
    data = {"model": MODEL, "voices": [], "items": [x[0] for x in AUDITION]}
    for v, name in CANDIDATES.items():
        col = {"id": v, "name": name, "clips": [], "metrics": {}}
        for label, kind, t in AUDITION:
            a, al = tts(v, t)
            if kind in ("word", "pseudo"): a = cut_last(a, t, al, t[5:-1])
            elif kind == "slice": a = cut_last(a, t, al, t[5:-1])   # slicing dropped (decision 19); historical item
            else: a = trim(a)
            fn = f"{name.lower()}_{re.sub(r'[^a-z]+', '_', label.lower()).strip('_')}.ogg"
            b, _ = loudness(fades(a)); encode(b, dst / fn)
            col["clips"].append({"label": label, "file": f"audition/{fn}", "ms": round(1000 * len(a) / SR)})
        col["metrics"]["sentence_s"] = round(len(trim(tts(v, AUDITION[-1][2])[0])) / SR, 2)
        data["voices"].append(col)
    (PUB / "voices-data.json").write_text(json.dumps(data, indent=1))
    print(json.dumps([(c["name"], [(x["label"], x["ms"]) for x in c["clips"]]) for c in data["voices"]]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "audition": audition()
    elif cmd == "plan": build_plan()
    elif cmd == "render":
        clips = json.loads((C / "audio_plan.json").read_text()); render_all(requests(clips), get_voice())
    elif cmd == "build": build()
    elif cmd == "needed":   # Levels 2-4: `needed L2` merges content/audio_needed.json["L2"].clips into the plan, renders, builds
        lv = sys.argv[2]; need = json.loads((C / "audio_needed.json").read_text())[lv]
        clips = json.loads((C / "audio_plan.json").read_text()); clips.update(need["clips"])
        print(f"{lv}: {need['keys']} keys, {need['chars']} new characters (isolated sounds listed separately: {need['isoSounds']})")
        (C / "audio_plan.json").write_text(json.dumps(clips, indent=1, ensure_ascii=False))
        render_all(requests(clips), get_voice()); build()
    else: sys.exit(__doc__)
