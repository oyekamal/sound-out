#!/usr/bin/env python3
"""Isolated sounds (ph:*) as DIRECT ElevenLabs renders in the app voice, teacher-style (decision 19: no slicing).

  python3 tools/iso_sounds.py          # render uncached takes (<= CHAR_CAP characters), pick, print the table,
                                       # write content/iso_sounds.json (every take, its measures, the pick)
tools/gen_audio_el.py build calls pick_all() and ships the picks as ph:<pid>.

Classes (Kamal's spec, decisions 19 + 20):
  hum   m n l r v z   held 300-350 ms, stability 1 / style 0 / speaker boost off, flat prompt forms ("mm.", "m-m-m",
                      "The sound mm." cut on the timestamps). Auto-reject: F0 range > 2 semitones, envelope swell
                      > 3 dB across the hold, low-band spectral flatness (breathiness) above the voice's word median.
                      Pick = flattest + most monotone.
  hiss  s f h         held 400-600 ms, no vowel frames, same swell check (F0/flatness do not apply to noise).
  vowel a e i o u     300-400 ms of the SHORT vowel; pick = nearest F1/F2 (Bark) to the vowel in River's own word.
  stop  t p k b d g j ks kw   burst + minimal release: total <= 220 ms, vowel tail <= 60 ms (trimmed with a fade).
  glide w y           <= 250 ms, tail <= 120 ms (a glide IS vowel-like; there is no vowelless /w/).
Three takes per sound, varied by prompt form (seed fixed). Takes that fail every check fall back to an IPA
<phoneme> render on eleven_turbo_v2 (the model family that honours IPA; multilingual_v2 ignores phoneme rules).
"""
import json, re, sys
from pathlib import Path
import numpy as np
import librosa
from scipy.signal import resample_poly, butter, sosfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_audio_el as g

SR, FR = g.SR, g.FR
ROOT = g.ROOT
CHAR_CAP = 2600          # this script's own budget (plus ~400 spent probing = ~3,000 total)
FLAT = {"stability": 1.0, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": False, "speed": 0.9}
V4, TURBO, ML2 = "eleven_v4", "eleven_turbo_v2", "eleven_multilingual_v2"


def ph(ipa, txt): return f'<phoneme alphabet="ipa" ph="{ipa}">{txt}</phoneme>'


HUM = {"m": "m", "n": "n", "l": "l", "r": "r", "v": "v", "z": "z"}
HUM_IPA = {"m": "mː", "n": "nː", "l": "lː", "r": "ɹː", "v": "vː", "z": "zː"}
HISS = {"s": "s", "f": "f", "h": "h"}
VOWEL = {"a": ("æ", "aaa", "apple"), "e": ("ɛ", "ehh", "egg"), "i": ("ɪ", "ihh", "igloo"),
         "o": ("ɑ", "ahh", "octopus"), "u": ("ʌ", "uhh", "umbrella")}
VOWEL_TAKES = {"a": ["æ.", "æ...", "æ—"], "e": ["ɛ.", "ɛː.", "/ɛ/"], "i": ["ɪ.", "ɪ—", "ɪ..."],   # v4 reads IPA vowels
               "o": ["ɑ.", "ɑː.", "/ɑ/"], "u": ["/ʌ/", "uh.", "Uh!"]}                                  # (probe 2026-10-06)
VOWEL_REF = {"a": "at", "e": "egg", "i": "if", "o": "ox", "u": "up"}   # River's word renders (cached) for F1/F2
STOP = {"t": "t", "p": "p", "k": "k", "b": "b", "d": "d", "g": "g", "j": "j", "ks": "ks", "kw": "kw"}
GLIDE = {"w": "w", "y": "y"}
STOP_IPA = {"t": "tʰ", "p": "pʰ", "k": "kʰ", "b": "b", "d": "d", "g": "ɡ", "j": "dʒ", "ks": "ks", "kw": "kw", "w": "w", "y": "j"}


def takes(pid):
    """[(label, model, text, settings, cut_word)] -- 3 prompt forms, + IPA fallback (only rendered if all 3 fail)."""
    if pid in HUM:
        c = HUM[pid]
        # multilingual_v2 with no final period reads a hum level (no statement fall); v4 rise-falls ("moan")
        return [("carrier 'The sound cc.'", V4, f"The sound {c}{c}.", FLAT, f"{c}{c}"),
                ("flat 'ccc'", ML2, c * 3, FLAT, None), ("flat 'Ccccc'", ML2, c.upper() + c * 4, FLAT, None)], \
               ("IPA fallback", TURBO, ph(HUM_IPA[pid], c + c), FLAT, None)
    if pid in HISS:
        c = HISS[pid]
        return [("'Ccccc.'", V4, f"{c.upper()}{c * 4}.", None, None), ("flat 'Ccccc.'", V4, f"{c.upper()}{c * 4}.", FLAT, None),
                ("flat 'cccccc'", V4, c * 6, FLAT, None)], ("IPA fallback", TURBO, ph(pid + "ː", c * 2), FLAT, None)
    if pid in VOWEL:
        ipa, resp, word = VOWEL[pid]
        return [(f"'{t}'", V4, t, None, None) for t in VOWEL_TAKES[pid]], None
    c = STOP.get(pid) or GLIDE[pid]
    if pid in ("t", "p", "k", "ks"):
        alt = ("whispered", V4, f"[whispers] {c}.", None, None)
    else:
        alt = ("'c'", V4, c, None, None)
    return [(f"'{c}.'", V4, f"{c}.", None, None), (f"'{c}uh.'", V4, f"{c}uh.", None, None), alt], \
           ("IPA fallback", TURBO, ph(STOP_IPA[pid], c), None, None)


def klass(pid):
    return "hum" if pid in HUM else "hiss" if pid in HISS else "vowel" if pid in VOWEL else "glide" if pid in GLIDE else "stop"


# ---------------------------------------------------------------- measures
def frames(a):
    """Per 10 ms frame: dB, periodic (bool), zcr, low-band ratio."""
    db = g.frames_db(a); n = len(db)
    per, z, lo = np.zeros(n, bool), np.zeros(n), np.zeros(n)
    sos = butter(4, [300, 3000], btype="band", fs=SR, output="sos"); band = sosfilt(sos, a)
    for i in range(n):
        x = a[max(0, i * FR - 120):(i + 1) * FR + 120]
        per[i] = g.periodicity(x) > 0.6
        z[i] = g.zcr(a[i * FR:(i + 1) * FR])
        e = np.sum(a[i * FR:(i + 1) * FR] ** 2) + 1e-12
        lo[i] = np.sum(band[i * FR:(i + 1) * FR] ** 2) / e
    return db, per, z, lo


def f0_range_st(x):
    if len(x) < int(.08 * SR): return None
    f0, vf, _ = librosa.pyin(x.astype(np.float32), fmin=70, fmax=450, sr=SR, frame_length=1024, hop_length=120)
    f = f0[vf & ~np.isnan(f0)]
    if len(f) < 5: return None
    st = 12 * np.log2(f / np.median(f))
    return float(np.percentile(st, 95) - np.percentile(st, 5))


def swell_db(x):
    """Largest difference between the mean levels of the three thirds of the hold (crescendo/decrescendo)."""
    n = len(x) // 3
    if n < FR: return 0.0
    lv = [g.rms_db(x[i * n:(i + 1) * n]) for i in range(3)]
    return float(max(lv) - min(lv))


_LP1K = butter(6, 1000, fs=SR, output="sos")
_LP = butter(6, [60, 2000], btype="band", fs=SR, output="sos")


def flatness(x):
    """Median spectral flatness of the 60-2000 Hz band (voicing region): breathy/noisy voice -> higher."""
    y = sosfilt(_LP, x).astype(np.float32)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=240))[:86]   # bins up to ~2 kHz
    f = librosa.feature.spectral_flatness(S=S)[0]
    return float(np.median(f))


def word_flatness_ref(voice):
    """Median low-band flatness over the voiced, loud frames of 20 River word renders."""
    vals = []
    for w in ["sat", "map", "nap", "man", "lap", "rat", "van", "zip", "mom", "men", "run", "leg", "dog", "big", "bell",
              "hill", "fun", "mud", "jam", "wet"]:
        t = f"Say: {w}."
        if not (g.CACHE / f"{g.rkey(voice, t)}.wav").exists(): continue
        a, al = g.tts(voice, t); a = g.cut_last(a, t, al, w)
        db, per, _, _ = frames(a); pk = db.max()
        seg = np.concatenate([a[i * FR:(i + 1) * FR] for i in range(len(db)) if per[i] and db[i] > pk - 15] or [a[:0]])
        if len(seg) > 2048: vals.append(flatness(seg))
    return float(np.median(vals))


def formants(x):
    """Median (F1, F2) Hz by LPC on 10 kHz, 30 ms frames."""
    y = resample_poly(x, 5, 12); sr = 10000
    y = np.append(y[0], y[1:] - 0.63 * y[:-1])
    F1, F2 = [], []
    for i in range(0, len(y) - 250 + 1, 50):
        fr = y[i:i + 250] * np.hamming(250)
        if np.sqrt(np.mean(fr ** 2)) < 1e-4: continue
        A = librosa.lpc(fr.astype(np.float64), order=12)
        r = [z for z in np.roots(A) if np.imag(z) > 0]
        fs = sorted((np.angle(z) * sr / (2 * np.pi), -sr / np.pi * np.log(abs(z))) for z in r)
        fs = [f for f, bw in fs if f > 200 and bw < 400]
        if len(fs) >= 2: F1.append(fs[0]); F2.append(fs[1])
    if not F1: return None
    return float(np.median(F1)), float(np.median(F2))


def bark(f): return 13 * np.arctan(0.00076 * f) + 3.5 * np.arctan((f / 7500) ** 2)


def fade(x, i_ms=8, o_ms=30):
    x = x.copy(); i, o = int(i_ms * SR / 1000), int(o_ms * SR / 1000)
    if len(x) > i + o: x[:i] *= np.linspace(0, 1, i); x[-o:] *= np.linspace(1, 0, o)
    return x


def source(voice, tk):
    label, model, text, settings, cutw = tk
    a, al = g.tts(voice, text, model, settings)
    if cutw:
        return g.cut_last(a, text, al, cutw)
    return g.trim(a)


# ---------------------------------------------------------------- per-class evaluation
def eval_held(pid, a, ref_flat):
    """Find the steadiest window of the target length inside the hold (a held sound's own onset/decay are trimmed,
    nothing is cut out of a word), then apply the moan checks to that window."""
    k = klass(pid)
    lo_ms, target = (300, 310) if k == "hum" else (400, 420)
    db, per, z, lob = frames(a); pk = db.max()
    loud = db > pk - 12
    best, s = (0, 0), None
    for i, v in enumerate(list(loud) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s > best[1] - best[0]: best = (s, i)
            s = None
    s0, s1 = best
    hold_ms = (s1 - s0) * 10
    m = {"hold_ms": hold_ms}
    med = np.median(db[s0:s1]) if s1 > s0 else pk
    vf = int(np.sum(per & (z < 0.15) & (db > pk - 15))) if k == "hiss" else int(np.sum(per[s0:s1] & (db[s0:s1] > med + 6)))
    m["vowel_frames"] = vf
    W = target // 10
    f0 = None
    if k == "hum":
        y = sosfilt(_LP1K, a).astype(np.float32)   # low-pass so the frication of v/z does not hide the voicing
        f, vflag, _ = librosa.pyin(y, fmin=70, fmax=450, sr=SR, frame_length=1024, hop_length=FR)
        f0 = np.where(vflag, f, np.nan)
    cands = []
    for st in range(s0, max(s0, s1 - W) + 1, 2):
        win = a[st * FR:(st + W) * FR]
        sw = swell_db(win)
        gl = 0.0
        if f0 is not None:
            ff = f0[st:st + W]; ff = ff[~np.isnan(ff)]
            gl = float(np.percentile(12 * np.log2(ff / np.median(ff)), 95) - np.percentile(12 * np.log2(ff / np.median(ff)), 5)) if len(ff) >= 5 else 99.0
        cands.append((sw + gl, st, sw, gl))
    _, st, sw, gl = min(cands)
    out = a[st * FR:(st + W) * FR]
    m["window_start_ms"] = (st - s0) * 10
    m["swell_db"] = round(sw, 2)
    if k == "hum":
        m["f0_range_st"] = round(gl, 2); m["flatness"] = round(flatness(out), 4); m["flat_ref"] = round(ref_flat, 4)
    fails = []
    if hold_ms < lo_ms: fails.append(f"hold {hold_ms} ms < {lo_ms}")
    if vf > 2: fails.append(f"vowel {vf * 10} ms")
    if sw > 3: fails.append(f"swell {round(sw, 1)} dB")
    if k == "hum":
        if gl > 2: fails.append(f"F0 glide {round(gl, 1)} st")
        if m["flatness"] > ref_flat: fails.append("breathy")
    score = gl + sw + vf
    out = fade(out, 10, 40)
    m["ms"] = round(1000 * len(out) / SR)
    return out, m, fails, score


_REF = {}


def eval_vowel(pid, a, voice):
    """Vowel quality from the voiced core (F1/F2 vs the same vowel in River's own word); duration = audible span
    (above peak - 30 dB: the voiced core plus the voice's own soft decay), cut at 380 ms with a fade."""
    if pid not in _REF:
        t = f"Say: {VOWEL_REF[pid]}."; r, al = g.tts(voice, t); w = g.cut_last(r, t, al, VOWEL_REF[pid])
        db, per, _, _ = frames(w); pk = db.max()
        idx = [i for i in range(min(len(db), 25)) if per[i] and db[i] > pk - 20]
        _REF[pid] = formants(w[idx[0] * FR:(idx[-1] + 1) * FR]) if idx else None
    db, per, z, _ = frames(a); pk = db.max()
    vi = [i for i in range(len(db)) if per[i] and db[i] > pk - 20]
    if not vi: return a, {"ms": 0}, ["no voiced frames"], 99
    core = a[vi[0] * FR:(vi[-1] + 1) * FR]
    au = [i for i in range(len(db)) if db[i] > pk - 30]
    on, off = au[0], au[-1] + 1
    span = (off - on) * 10
    out = a[on * FR: off * FR][:int(.38 * SR)]
    F = formants(core); R = _REF[pid]
    d = 9.0 if not (F and R) else float(np.hypot(bark(F[0]) - bark(R[0]), bark(F[1]) - bark(R[1])))
    m = {"voiced_core_ms": (vi[-1] - vi[0] + 1) * 10, "audible_ms": span, "F1F2": [round(F[0]), round(F[1])] if F else None,
         "ref_F1F2": [round(R[0]), round(R[1])] if R else None, "bark_dist": round(d, 2)}
    fails = []
    if span < 300: fails.append(f"audible {span} ms < 300")
    if d > 1.5: fails.append(f"vowel quality off ({d:.2f} Bark)")
    out = fade(out, 6, 60); m["ms"] = round(1000 * len(out) / SR)
    return out, m, fails, d


def eval_stop(pid, a):
    k = klass(pid)
    tail_cap, tot_cap = (0.12, 0.25) if k == "glide" else (0.06, 0.22)
    db, per, z, lob = frames(a); pk = db.max()
    on = next(i for i in range(len(db)) if db[i] > pk - 30)
    # vowel = voiced (periodicity > .45 catches the breathy end of "tuh" too), low ZCR, within 18 dB of the peak
    # (a voiced stop's closure voice bar is quieter than that, so it does not count as vowel)
    p45 = np.array([g.periodicity(a[max(0, i * FR - 120):(i + 1) * FR + 120]) > 0.45 for i in range(len(db))])
    isv = p45 & (z < 0.15) & (db > pk - 18)
    start = on + (0 if k == "glide" else 1)
    vo = next((i for i in range(start, len(db)) if isv[i]), None)
    nat_tail = int(np.sum(isv[vo:])) * 10 if vo is not None else 0
    burst = (vo - on) * 10 if vo is not None else (len(db) - on) * 10
    end = len(a) if vo is None else int((vo * 10 / 1000 + tail_cap) * SR)
    end = min(end, int((on * 10 / 1000 + tot_cap) * SR), len(a))
    out = fade(a[on * FR:end], 2, 15)
    m = {"burst_ms": burst, "natural_vowel_ms": nat_tail, "tail_ms": min(nat_tail, round(tail_cap * 1000)),
         "ms": round(1000 * len(out) / SR)}
    fails = []
    if m["ms"] < 60: fails.append(f"too short {m['ms']} ms")
    # a letter NAME / drawn-out syllable shows up as a long natural vowel (> 250 ms "tee", "jay")
    if nat_tail > 250: fails.append(f"long vowel {nat_tail} ms (letter name?)")
    score = nat_tail - 0.5 * min(burst, 120)
    return out, m, fails, score


def evaluate(pid, a, voice, ref_flat):
    k = klass(pid)
    if len(a) < 5 * FR: return a, {"ms": round(1000 * len(a) / SR)}, ["empty / silent render"], 999
    if k in ("hum", "hiss"): return eval_held(pid, a, ref_flat)
    if k == "vowel": return eval_vowel(pid, a, voice)
    return eval_stop(pid, a)


# ---------------------------------------------------------------- render + pick
SOUNDS = ["s", "a", "t", "p", "i", "n", "m", "d", "g", "o", "k", "e", "u", "r", "h", "b", "f", "l", "j", "v", "w", "ks", "y", "z", "kw"]


def uncached(voice, tk): return not (g.CACHE / f"{g.rkey(voice, tk[2], tk[1], tk[3])}.wav").exists()


def render(voice, tks):
    todo = [tk for tk in tks if uncached(voice, tk)]
    chars = sum(len(tk[2]) for tk in todo)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(3) as ex: list(ex.map(lambda tk: g.tts(voice, tk[2], tk[1], tk[3]), todo))
    return chars


def pick_all(voice=None, do_render=True, asr=False):
    voice = voice or g.get_voice()
    out_json = ROOT / "content/iso_sounds.json"
    spent = 0
    if do_render:
        spent += render(voice, [t for p in SOUNDS for t in takes(p)[0]])
        if spent > CHAR_CAP: sys.exit(f"STOP: {spent} chars")
    ref_flat = word_flatness_ref(voice)
    res, audio = {}, {}
    for pid in SOUNDS:
        main, fb = takes(pid)
        rows = []
        for tk in main:
            if uncached(voice, tk): continue
            a, m, fails, score = evaluate(pid, source(voice, tk), voice, ref_flat)
            rows.append({"label": tk[0], "model": tk[1], "text": tk[2], "flat_settings": tk[3] is FLAT, "measures": m,
                         "fails": fails, "score": round(float(score), 2), "_a": a})
        ok = [r for r in rows if not r["fails"]]
        if not ok and fb is not None:
            if do_render and uncached(voice, fb): spent += render(voice, [fb])
            if not uncached(voice, fb):
                a, m, fails, score = evaluate(pid, source(voice, fb), voice, ref_flat)
                rows.append({"label": fb[0], "model": fb[1], "text": fb[2], "flat_settings": fb[3] is FLAT, "measures": m,
                             "fails": fails, "score": round(float(score), 2), "_a": a})
                ok = [r for r in rows if not r["fails"]]
        pool = ok or rows
        best = min(pool, key=lambda r: r["score"])
        audio[pid] = best["_a"]
        for r in rows: r.pop("_a")
        res[pid] = {"class": klass(pid), "verdict": "pass" if ok else "FAIL (least-bad take shipped)",
                    "pick": rows.index(best), "takes": rows}
    if asr:
        import whisper
        wm = whisper.load_model("small.en")
        for pid, x in audio.items():
            y = resample_poly(x, 2, 3).astype(np.float32); y = y / (np.abs(y).max() + 1e-9) * .5
            y = np.concatenate([np.zeros(8000, np.float32), y, np.zeros(8000, np.float32)])
            t = wm.transcribe(y, language="en", fp16=False, temperature=0)["text"].strip()
            res[pid]["heard_as"] = t[:24]
    out_json.write_text(json.dumps({"voice": voice, "flat_settings": FLAT, "word_flatness_ref": round(ref_flat, 4),
                                    "chars_this_run": spent, "sounds": res}, indent=1, ensure_ascii=False))
    return audio, res, spent


if __name__ == "__main__":
    audio, res, spent = pick_all(asr="--asr" in sys.argv)
    print(f"characters rendered this run: {spent}")
    for pid, r in res.items():
        b = r["takes"][r["pick"]]
        print(f"{pid:3s} {r['class']:5s} {r['verdict'][:4]:4s} {b['measures'].get('ms')}ms  {b['model']:15s} {b['text'][-36:]!r:40s} "
              f"{r.get('heard_as', '')!r}  " + " | ".join(f"{t['label']}: {','.join(t['fails']) or 'ok'}" for t in r["takes"]))
