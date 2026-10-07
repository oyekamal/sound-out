#!/usr/bin/env python3
"""Dictionary-driven ElevenLabs renders (decision 21): CMUdict pronunciations via a PLS pronunciation dictionary.

  python3 tools/dict_audio.py pls        # content/sound-out.pls (Level 1 words + pseudowords + compare extras + sentence
                                         # capitals, CMU Arpabet) and content/sound-out-iso.pls / -iso-ipa.pls (44 phonemes)
  python3 tools/dict_audio.py render     # Level 1 set again on eleven_v4 + dictionary (same River voice, settings, seed,
                                         # carrier "Say: X."), compare extras, 40 sentences, flash_v2 on the compare rows
  python3 tools/dict_audio.py phonemes   # 44 phonemes x 2 forms x {eleven_v4, eleven_flash_v2}
  python3 tools/dict_audio.py measure    # content/dict_audio.json (+ prints the tables)
  python3 tools/dict_audio.py compare    # app/public/compare-data.json + app/public/compare/*.ogg
The existing v4 renders are untouched; the app keeps playing them. Every new render is logged in content/el_chars.json;
the script stops before a render that would take this spike past CHAR_CAP characters.

Which models honour a dictionary's phoneme rules (ElevenLabs docs 2026-10: "only eleven_v4, eleven_flash_v2 and
eleven_v3"; confirmed here with a nonsense grapheme 'zorblak' -> K AE1 T, Whisper on the render): eleven_v4 "Say cat",
eleven_flash_v2 "Say cat", eleven_turbo_v2 "Say Cat" (deprecated alias of flash_v2); eleven_flash_v2_5 "Say, uh",
eleven_turbo_v2_5 "Say.", eleven_multilingual_v2 "Say." -> not honoured (the word is dropped).
"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_audio_el as g
import el_dict as E
import iso_sounds as iso

ROOT, C, PUB, SR, FR = g.ROOT, g.C, g.PUB, g.SR, g.FR
PLS_W, PLS_P, PLS_PI = C / "sound-out.pls", C / "sound-out-iso.pls", C / "sound-out-iso-ipa.pls"
V4, FLASH = "eleven_v4", "eleven_flash_v2"
CHAR_CAP = 11000            # whole spike, probes included (account had 11,018 left on 2026-10-07)
OUTJ = C / "dict_audio.json"
PROBE = {"cmu 'zorblak' -> K AE1 T": {"eleven_v4": "Say cat.", "eleven_flash_v2": "Say cat.", "eleven_turbo_v2": "Say Cat.",
                                       "eleven_flash_v2_5": "Say, uh.", "eleven_turbo_v2_5": "Say.", "eleven_multilingual_v2": "Say."},
         "ipa 'zorblik' -> dˈɔɡ": {"eleven_v4": "Say, dog.", "eleven_flash_v2": "Say dog."},
         "raw": ["0efc9cf109ea", "6fd759c859fb", "2bdcfff93dbd", "ac4722dd82bc", "404de34b4dfd", "60b80384fcb9", "f8b1c441a733", "4be9934efccc"]}

# compare page: 20 words (homographs + tricky + Level 1) and 5 pseudowords; sense hints for the homographs
COMPARE_EXTRA = {"station": None, "through": None, "garden": None, "read": "present: 'I can read'", "live": "verb: 'we live here'",
                 "wind": "verb: 'wind the clock' (L3.16 -ind)", "close": "verb: 'close the door'", "use": "verb: 'use a pen'",
                 "said": None, "was": None, "flobin": None, "pademic": None}
COMPARE_L1 = ["the", "of", "full", "dog", "off", "son", "fall", "a", "is", "to", "sas", "tas", "sa"]


# ------------------------------------------------------------------ Level 1 items
def l1_items():
    """One item per (spelling, intended IPA) the app says as a word: lexicon words + tap-gate foils."""
    lex = json.loads((C / "lexicon.json").read_text()); opts = json.loads((C / "options.json").read_text())
    plan = json.loads((C / "audio_plan.json").read_text())
    full = json.loads((C / "lexicon_full.json").read_text())["words"]
    cmu = {}
    for line in (C / "cmudict/cmudict.dict").read_text().splitlines():
        w, *ph = line.split("#")[0].split()
        if not re.search(r"\(\d+\)$", w): cmu.setdefault(w, " ".join(ph))
    ipa_spell, kind_of = {}, {}
    for e in lex.values(): ipa_spell.setdefault(e["ipa"], e["w"]); kind_of[(e["w"], e["ipa"])] = e["kind"]
    for o in opts.values():
        for f in [o["target"], *o["foils"]]: ipa_spell.setdefault(f["ipa"], f["w"])
    items = {}
    for key, c in plan.items():
        if c["cut"] not in ("last", "open") or not (key.startswith("w:") or key.startswith("ipa:")): continue
        ipa = c["ipa"]; w = lex[key[2:]]["w"] if key.startswith("w:") else ipa_spell[ipa]
        it = items.setdefault((w, ipa), {"w": w, "ipa": ipa, "keys": [], "current_text": g.req_text(c), "current_cut": c["cut"],
                                          "current_say": c["say"]})
        it["keys"].append(key)
    by_sp = {}
    for (w, ipa), it in items.items(): by_sp.setdefault(w, []).append(it)
    for w, its in by_sp.items():
        for it in its:
            lw = w if w == "I" else w.lower()
            k = kind_of.get((w, it["ipa"])) or ("real" if lw in cmu else "pseudo")
            course = E.ipa2arpa(it["ipa"])
            primary = len(its) == 1 or E.strip(course) == E.strip(cmu.get(lw, ""))   # "is" /ɪz/ vs foil /ɪs/
            if k in ("real", "heart") and primary and lw in full and full[lw]["kind"] == "real":
                arpa, src = full[lw]["arpa_stress"], full[lw]["source"]
            else:
                arpa, src = course, "course IPA"
            it.update(kind="pseudo" if k == "pseudo" else "real" if k != "syllable" else "syllable", arpa=arpa, arpa_source=src,
                      grapheme=w if primary else w.upper())
    return list(items.values())


def stressed(a):   # PLS: CMU vowels need a stress digit; first vowel 1 when none given
    out, seen = [], any(p[-1] in "12" for p in a.split())
    for p in a.split():
        if p in E.VOW: out.append(p + ("0" if seen else "1")); seen = True
        else: out.append(p)
    return " ".join(out)


def sentences():
    plan = json.loads((C / "audio_plan.json").read_text())
    ss = sorted({c["text"] for k, c in plan.items() if k.startswith("read:")}, key=lambda t: (len(t), t))
    return [t for t in ss if len(t.split()) >= 3][:40]


def extra_items():
    full = json.loads((C / "lexicon_full.json").read_text())["words"]; out = []
    for w, hint in COMPARE_EXTRA.items():
        e = full[w]; arpa = e["arpa_stress"] if e["kind"] == "real" else stressed(e["arpa"])
        out.append({"w": w, "grapheme": w, "arpa": arpa, "kind": e["kind"], "hint": hint, "arpa_source": e["source"],
                    "current_text": f"Say: {w}.", "current_cut": "last", "current_say": w, "keys": []})
    return out


# ------------------------------------------------------------------ 44 phonemes
P44 = [  # (id, CMU, IPA form for the IPA dictionary, class, example)
    ("p", "P", "pʰ", "stop", "pat"), ("b", "B", "b", "stop", "bat"), ("t", "T", "tʰ", "stop", "tap"), ("d", "D", "d", "stop", "dip"),
    ("k", "K", "kʰ", "stop", "kit"), ("g", "G", "ɡ", "stop", "got"), ("ch", "CH", "tʃ", "stop", "chip"), ("j", "JH", "dʒ", "stop", "jam"),
    ("f", "F", "fː", "hiss", "fan"), ("v", "V", "vː", "hum", "van"), ("th", "TH", "θː", "hiss", "thin"), ("dh", "DH", "ðː", "hum", "this"),
    ("s", "S", "sː", "hiss", "sat"), ("z", "Z", "zː", "hum", "zip"), ("sh", "SH", "ʃː", "hiss", "ship"), ("zh", "ZH", "ʒː", "hum", "vision"),
    ("h", "HH", "hː", "hiss", "hat"), ("m", "M", "mː", "hum", "map"), ("n", "N", "nː", "hum", "nap"), ("ng", "NG", "ŋː", "hum", "sing"),
    ("l", "L", "lː", "hum", "lap"), ("r", "R", "ɹː", "hum", "rat"), ("w", "W", "w", "glide", "wet"), ("y", "Y", "j", "glide", "yes"),
    ("ae", "AE1", "æː", "vowel", "at"), ("eh", "EH1", "ɛː", "vowel", "egg"), ("ih", "IH1", "ɪː", "vowel", "if"), ("aa", "AA1", "ɑː", "vowel", "ox"),
    ("ah", "AH1", "ʌː", "vowel", "up"), ("uh", "UH1", "ʊː", "vowel", "book"), ("iy", "IY1", "iː", "vowel", "see"), ("ar", "AA1 R", "ɑːɹ", "vowel", "car"),
    ("ao", "AO1", "ɔː", "vowel", "saw"), ("uw", "UW1", "uː", "vowel", "moon"), ("er", "ER1", "ɝː", "vowel", "her"), ("ey", "EY1", "eɪ", "vowel", "day"),
    ("ay", "AY1", "aɪ", "vowel", "my"), ("oy", "OY1", "ɔɪ", "vowel", "boy"), ("ow", "OW1", "oʊ", "vowel", "go"), ("aw", "AW1", "aʊ", "vowel", "cow"),
    ("ir", "IH1 R", "ɪɹ", "vowel", "ear"), ("air", "EH1 R", "ɛɹ", "vowel", "air"), ("ur", "UH1 R", "ʊɹ", "vowel", "tour"), ("schwa", "AH0", "ə", "vowel", "about"),
]
L1_PID = {"s": "s", "a": "ae", "t": "t", "p": "p", "i": "ih", "n": "n", "m": "m", "d": "d", "g": "g", "o": "aa", "k": "k", "e": "eh",
          "u": "ah", "r": "r", "h": "h", "b": "b", "f": "f", "l": "l", "j": "j", "v": "v", "w": "w", "y": "y", "z": "z"}   # ks kw: clusters


def phoneme_jobs():
    jobs = []
    for pid, cmu, ipa, cl, ex in P44:
        for model in (V4, FLASH):
            jobs.append((pid, "cmu", model, f"sound_{pid}", PLS_P))
            jobs.append((pid, "ipa", model, f"long_{pid}", PLS_PI))
    return jobs


# ------------------------------------------------------------------ PLS
def cmd_pls():
    its = l1_items() + extra_items()
    ents, seen = [], {}
    for it in its:
        gr, a = it["grapheme"], stressed(it["arpa"])
        if gr in seen and seen[gr] != a: print("CONFLICT", gr, seen[gr], a); continue
        if gr not in seen: seen[gr] = a; ents.append((gr, a))
    # capitalised forms for the sentences (PLS graphemes are case-sensitive)
    low = {gr: a for gr, a in seen.items() if gr.islower()}
    for t in sentences():
        for tok in re.findall(r"[A-Za-z']+", t):
            if tok[0].isupper() and tok not in seen and tok.lower() in low:
                seen[tok] = low[tok.lower()]; ents.append((tok, low[tok.lower()]))
    PLS_W.write_text(E.pls(ents))
    PLS_P.write_text(E.pls([(f"sound_{pid}", cmu) for pid, cmu, *_ in P44]))
    PLS_PI.write_text(E.pls([(f"long_{pid}", ipa) for pid, cmu, ipa, *_ in P44], "ipa"))
    (C / "dict_items.json").write_text(json.dumps(its, indent=0, ensure_ascii=False))
    print(f"{PLS_W.name}: {len(ents)} lexemes ({len(l1_items())} Level 1 items); {PLS_P.name}/{PLS_PI.name}: {len(P44)} phonemes")


# ------------------------------------------------------------------ render
def dict_text(it): return f"Say: {it['grapheme']}."


def jobs_all():
    its = json.loads((C / "dict_items.json").read_text())
    voice = g.get_voice(); J = []
    for it in its:
        J.append(("dict", voice, dict_text(it), V4, None, PLS_W))
        if not it["keys"]: J.append(("plain", voice, it["current_text"], V4, None, None))      # extras: current-style v4
    for t in sentences(): J.append(("dict", voice, t, V4, None, PLS_W))
    for it in its:
        if it["grapheme"] in COMPARE_L1 + list(COMPARE_EXTRA): J.append(("dict", voice, dict_text(it), FLASH, None, PLS_W))
    return J


def todo(J):
    out = []
    for kind, voice, text, model, st, pls in J:
        if kind == "dict" and not E.is_cached(voice, text, model, st, pls): out.append((kind, voice, text, model, st, pls))
        if kind == "plain" and not (g.CACHE / f"{g.rkey(voice, text, model, st)}.wav").exists(): out.append((kind, voice, text, model, st, pls))
    return list(dict.fromkeys(out))


def run(J):
    T = todo(J); chars = sum(len(x[2]) for x in T)
    print(f"{len(T)} uncached renders, {chars} chars; spent so far {E.spent()}; cap {CHAR_CAP}")
    if E.spent() + chars > CHAR_CAP: sys.exit("STOP: would pass the character cap")
    fails = []
    def one(x):
        kind, voice, text, model, st, pls = x
        try:
            if kind == "dict": E.tts(voice, text, model, st, pls)
            else: E.plain(voice, text, model, st)
        except Exception as e: fails.append((text, model, str(e)[:200]))
    with ThreadPoolExecutor(3) as ex: list(ex.map(one, T))
    for f in fails: print("FAIL", f)
    print("spent now", E.spent())


def cmd_render(): run(jobs_all())


def cmd_phonemes():
    voice = g.get_voice()
    run([("dict", voice, t, m, None, p) for pid, form, m, t, p in phoneme_jobs()])


# ------------------------------------------------------------------ measures
def cut(a, text, al, word):
    try: return g.cut_last(a, text, al, word)
    except Exception: return g.trim(a)


def nucleus(x):
    db, per, _, _ = iso.frames(x)
    if not len(db): return None
    pk = db.max(); idx = [i for i in range(len(db)) if per[i] and db[i] > pk - 15]
    return x[idx[0] * FR:(idx[-1] + 1) * FR] if len(idx) >= 4 else None


REF_WORD = {"AE": "at", "EH": "egg", "IH": "if", "AA": "ox", "AH": "up"}
_ref = {}


def ref_formants(v):
    if v not in _ref:
        voice = g.get_voice(); t = f"Say: {REF_WORD[v]}."; a, al = g.tts(voice, t); w = g.cut_last(a, t, al, REF_WORD[v])
        n = nucleus(w); _ref[v] = iso.formants(n) if n is not None else None
    return _ref[v]


def word_measures(x, arpa):
    if len(x) < 4 * FR: return {"ms": round(1000 * len(x) / SR), "lufs": None, "rms_db": None, "empty": True}
    m = {"ms": round(1000 * len(x) / SR), "lufs": None, "rms_db": round(float(g.rms_db(x)), 1) if len(x) else None}
    pad = np.concatenate([x, np.zeros(max(0, int(.45 * SR) - len(x)))])
    L = g.lufs(pad); m["lufs"] = round(L, 1) if L is not None else None
    vs = [p.rstrip("012") for p in arpa.split() if p.rstrip("012") in E.VOW]
    n = nucleus(x)
    if n is not None:
        F = iso.formants(n)
        if F: m["F1F2"] = [round(F[0]), round(F[1])]
    if len(vs) == 1 and vs[0] in REF_WORD and m.get("F1F2"):
        R = ref_formants(vs[0])
        if R: m["bark_to_ref"] = round(float(np.hypot(iso.bark(m["F1F2"][0]) - iso.bark(R[0]), iso.bark(m["F1F2"][1]) - iso.bark(R[1]))), 2)
    return m


_wm = None


def asr(x):
    global _wm
    import whisper
    from scipy.signal import resample_poly
    if _wm is None: _wm = whisper.load_model("small.en")
    if len(x) < 400: return ""
    y = resample_poly(x, 2, 3).astype(np.float32); y = y / (np.abs(y).max() + 1e-9) * .5
    y = np.concatenate([np.zeros(8000, np.float32), y, np.zeros(8000, np.float32)])
    return _wm.transcribe(y, language="en", fp16=False, temperature=0)["text"].strip()


def norm(t): return re.sub(r"[^a-z' ]", "", t.lower().replace("-", " ")).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp); d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[len(h)] / max(1, len(r))


def current_clip(voice, it):
    t = it["current_text"]; a, al = g.tts(voice, t)
    w = cut(a, t, al, it["current_say"])
    return g.open_cut(w) if it["current_cut"] == "open" else w


def dict_clip(voice, it, model=V4):
    t = dict_text(it); a, al = E.tts(voice, t, model, None, PLS_W)
    return cut(a, t, al, it["grapheme"])


def cmd_measure():
    voice = g.get_voice(); its = json.loads((C / "dict_items.json").read_text())
    rows = []
    for it in its:
        if not E.is_cached(voice, dict_text(it), V4, None, PLS_W): continue
        cur, dic = current_clip(voice, it), dict_clip(voice, it)
        mc, md = word_measures(cur, it["arpa"]), word_measures(dic, it["arpa"])
        r = {"w": it["w"], "grapheme": it["grapheme"], "kind": it["kind"], "arpa": it["arpa"], "arpa_source": it["arpa_source"],
             "current": mc, "dict": md, "current_text": it["current_text"]}
        if mc.get("F1F2") and md.get("F1F2"):
            r["bark_between"] = round(float(np.hypot(iso.bark(mc["F1F2"][0]) - iso.bark(md["F1F2"][0]), iso.bark(mc["F1F2"][1]) - iso.bark(md["F1F2"][1]))), 2)
        if it["kind"] == "real":
            r["asr_current"], r["asr_dict"] = asr(cur), asr(dic)
        if E.is_cached(voice, dict_text(it), FLASH, None, PLS_W):
            r["flash"] = word_measures(dict_clip(voice, it, FLASH), it["arpa"])
        rows.append(r)
    sent = []
    for t in sentences():
        if not E.is_cached(voice, t, V4, None, PLS_W): continue
        a0, _ = g.tts(voice, t); a1, _ = E.tts(voice, t, V4, None, PLS_W); a0, a1 = g.trim(a0), g.trim(a1)
        h0, h1 = asr(a0), asr(a1)
        sent.append({"text": t, "current": {"s": round(len(a0) / SR, 2), "lufs": round(g.lufs(a0) or 0, 1), "asr": h0, "wer": round(wer(t, h0), 3)},
                     "dict": {"s": round(len(a1) / SR, 2), "lufs": round(g.lufs(a1) or 0, 1), "asr": h1, "wer": round(wer(t, h1), 3)}})
    ph = phoneme_measures(voice)
    out = {"voice": voice, "probe": PROBE, "items": rows, "sentences": sent, "phonemes": ph, "chars_spent": E.spent(),
           "summary": summarise(rows, sent, ph)}
    OUTJ.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps(out["summary"], indent=1, ensure_ascii=False))


def summarise(rows, sent, ph):
    def med(v): v = [x for x in v if x is not None]; return round(float(np.median(v)), 2) if v else None
    s = {"items": len(rows)}
    for k in ("real", "pseudo"):
        R = [r for r in rows if r["kind"] == k]
        s[k] = {"n": len(R), "ms_current": med([r["current"]["ms"] for r in R]), "ms_dict": med([r["dict"]["ms"] for r in R]),
                "lufs_current": med([r["current"]["lufs"] for r in R]), "lufs_dict": med([r["dict"]["lufs"] for r in R]),
                "bark_to_ref_current": med([r["current"].get("bark_to_ref") for r in R]),
                "bark_to_ref_dict": med([r["dict"].get("bark_to_ref") for r in R]),
                "n_bark": sum(1 for r in R if r["current"].get("bark_to_ref") is not None and r["dict"].get("bark_to_ref") is not None),
                "dict_closer_to_ref": sum(1 for r in R if r["current"].get("bark_to_ref") is not None and r["dict"].get("bark_to_ref") is not None
                                          and r["dict"]["bark_to_ref"] < r["current"]["bark_to_ref"] - 0.3),
                "current_closer_to_ref": sum(1 for r in R if r["current"].get("bark_to_ref") is not None and r["dict"].get("bark_to_ref") is not None
                                             and r["current"]["bark_to_ref"] < r["dict"]["bark_to_ref"] - 0.3),
                "bark_between_median": med([r.get("bark_between") for r in R]),
                "empty_dict": sum(1 for r in R if r["dict"]["ms"] < 120)}
        if k == "real":
            ok = lambda h, w: w.lower() in norm(h)
            s[k]["asr_hit_current"] = sum(ok(r["asr_current"], r["w"]) for r in R)
            s[k]["asr_hit_dict"] = sum(ok(r["asr_dict"], r["w"]) for r in R)
    if sent:
        s["sentences"] = {"n": len(sent), "wer_current": round(float(np.mean([x["current"]["wer"] for x in sent])), 3),
                          "wer_dict": round(float(np.mean([x["dict"]["wer"] for x in sent])), 3),
                          "s_current": round(float(np.sum([x["current"]["s"] for x in sent])), 1), "s_dict": round(float(np.sum([x["dict"]["s"] for x in sent])), 1)}
    if ph: s["phonemes"] = {f"{m}/{f}": sum(1 for p in ph for t in p["takes"] if t["model"] == m and t["form"] == f and t["verdict"] in ("usable", "usable?"))
                            for m in (V4, FLASH) for f in ("cmu", "ipa")}
    return s


# ------------------------------------------------------------------ phoneme measures
def phoneme_eval(cl, pid, x):
    """-> (clip for the A/B page, measures, verdict). Verdict: usable / short / schwa-tail / silent / literal (read the
    grapheme as words) / vowel-in-fricative."""
    if len(x) < 4 * FR: return x, {"ms": round(1000 * len(x) / SR)}, "silent"
    db, per, z, _ = iso.frames(x); pk = db.max()
    aud = [i for i in range(len(db)) if db[i] > pk - 30]; audible = (aud[-1] - aud[0] + 1) * 10
    m = {"ms": round(1000 * len(x) / SR), "audible_ms": audible, "voiced_ms": int(np.sum(per & (db > pk - 20))) * 10}
    if audible > 1100: return x, m, "literal"
    if cl == "stop" or cl == "glide":
        out, mm, fails, _ = iso.eval_stop("w" if cl == "glide" else "t", x); m.update(mm)
        cap = 120 if cl == "glide" else 60
        return out, m, "usable" if mm["natural_vowel_ms"] <= cap and mm["burst_ms"] >= 10 else ("schwa-tail" if mm["natural_vowel_ms"] > cap else "no-burst")
    if cl == "hiss":
        vf = int(np.sum(per & (z < 0.15) & (db > pk - 15))) * 10; m["vowel_ms"] = vf
        out = iso.fade(x[aud[0] * FR:(aud[-1] + 1) * FR][:int(.6 * SR)], 10, 40)
        return out, m, "usable" if audible >= 250 and vf <= 30 else ("vowel-in-fricative" if vf > 30 else "short")
    if cl == "hum":
        out, mm, fails, _ = iso.eval_held("m", x, 0.0081); m.update({k: mm[k] for k in ("hold_ms", "swell_db", "f0_range_st") if k in mm})
        return out, m, "usable" if audible >= 250 else "short"
    out = iso.fade(x[aud[0] * FR:(aud[-1] + 1) * FR][:int(.5 * SR)], 6, 60)
    return out, m, "usable" if audible >= 250 else "short"


def phoneme_measures(voice):
    shipped = json.loads((C / "iso_sounds.json").read_text())["sounds"]
    ref_flat = json.loads((C / "iso_sounds.json").read_text())["word_flatness_ref"]
    res = []
    inv = {v: k for k, v in L1_PID.items()}
    for pid, cmu, ipa, cl, ex in P44:
        row = {"id": pid, "cmu": cmu, "ipa": ipa, "class": cl, "example": ex, "takes": []}
        for _, form, model, text, pls in [j for j in phoneme_jobs() if j[0] == pid]:
            if not E.is_cached(voice, text, model, None, pls): continue
            a, al = E.tts(voice, text, model, None, pls); x = g.trim(a)
            out, m, verdict = phoneme_eval(cl, pid, x)
            heard = asr(x) if len(x) > 4 * FR else ""
            # Whisper is unreliable on a lone sound (it hears /æ/ as "I"), so it is used only to catch a LITERAL reading:
            # the model saying the dictionary's symbols ("slash M slash") or a phrase instead of the sound
            if "slash" in heard.lower() or len(norm(heard)) >= 3:
                if verdict in ("usable", "short", "schwa-tail"): verdict = "literal"
            t = {"form": form, "model": model, "text": text, "verdict": verdict, "heard_as": heard[:40], "measures": m}
            if pid in inv:   # Level 1 sound: the shipped sound's own checks (tools/iso_sounds.py) on this take
                _, mm, fails, score = iso.evaluate(inv[pid], x, voice, ref_flat)
                t["l1_checks"] = {"fails": fails, "score": round(float(score), 2), "ms": mm.get("ms")}
                if iso.klass(inv[pid]) == "vowel" and any("quality" in f for f in fails) and verdict == "usable":
                    verdict = t["verdict"] = "wrong-vowel"   # F1/F2 > 1.5 Bark from the same vowel in River's own word
            elif cl == "vowel" and verdict == "usable":
                t["verdict"] = verdict = "usable?"            # duration only: no reference to check the vowel quality
            row["takes"].append(t)
        if pid in inv:
            s = shipped[inv[pid]]; b = s["takes"][s["pick"]]
            row["shipped"] = {"l1": inv[pid], "verdict": s["verdict"], "text": b["text"], "model": b["model"], "ms": b["measures"].get("ms"),
                              "score": b["score"]}
            better = [t for t in row["takes"] if t.get("l1_checks") and not t["l1_checks"]["fails"] and s["verdict"] != "pass"]
            row["measurably_better"] = [f"{t['model']}/{t['form']}" for t in better]
        res.append(row)
    return res


def cmd_measure_phonemes():
    out = json.loads(OUTJ.read_text()); out["phonemes"] = phoneme_measures(g.get_voice())
    out["summary"] = summarise(out["items"], out["sentences"], out["phonemes"]); out["chars_spent"] = E.spent()
    OUTJ.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for p in out["phonemes"]:
        print(p["id"], p["class"], " | ".join(f"{t['model'][7:]}/{t['form']}: {t['verdict']} {t['measures'].get('audible_ms', t['measures'].get('ms'))}ms '{t['heard_as']}'" for t in p["takes"]), p.get("measurably_better", ""))


# ------------------------------------------------------------------ compare page
def cmd_compare():
    import hashlib, random
    voice = g.get_voice(); its = {it["grapheme"]: it for it in json.loads((C / "dict_items.json").read_text())}
    idx = json.loads((C / "audio_index.json").read_text())["clips"]
    meas = json.loads(OUTJ.read_text()) if OUTJ.exists() else {"items": [], "phonemes": []}
    mrow = {r["grapheme"]: r for r in meas["items"]}
    dst = PUB / "compare"; dst.mkdir(exist_ok=True)
    for f in dst.glob("*.ogg"): f.unlink()
    def enc(x, tag, rms=False):
        cid = hashlib.sha1(f"{tag}".encode()).hexdigest()[:12]
        b = x * 10 ** ((-19.0 - g.rms_db(x)) / 20) if rms else g.loudness(g.fades(x), -19.0)[0]
        g.encode(b, dst / f"{cid}.ogg"); return f"compare/{cid}.ogg"
    ph = {p["id"]: p for p in meas.get("phonemes", [])}
    def phon_cands(arpa):
        out = []
        for p in arpa.split():
            b = p.rstrip("012"); pid = next((x[0] for x in P44 if x[1].rstrip("012") == b), None)
            if not pid or pid not in ph or any(o["id"] == pid for o in out): continue
            for t in ph[pid]["takes"]:
                if t["verdict"] not in ("usable", "usable?"): continue
                pls = PLS_P if t["form"] == "cmu" else PLS_PI
                a, _ = E.tts(voice, t["text"], t["model"], None, pls)
                clip, _, _ = phoneme_eval(ph[pid]["class"], pid, g.trim(a))
                out.append({"id": pid, "label": f"/{E.arpa2ipa(ph[pid]['cmu']).replace('ˈ', '')}/", "model": t["model"], "form": t["form"],
                            "file": enc(clip, f"ph|{pid}|{t['model']}|{t['form']}", rms=True)})
                break
        return out
    rows = []
    order = list(COMPARE_EXTRA) + COMPARE_L1
    rng = random.Random(21)
    for gr in order:
        it = its[gr] if gr in its else its.get(gr.upper())
        if it is None: print("missing", gr); continue
        cur = (f"audio/{idx[it['keys'][0]]['id']}.ogg" if it["keys"] else enc(current_clip(voice, it), f"cur|{gr}"))
        dic = enc(dict_clip(voice, it), f"dict|{gr}")
        A = [{"set": "v4 current", "file": cur}, {"set": "v4 + CMU dictionary", "file": dic}]; rng.shuffle(A)
        m = mrow.get(it["grapheme"], {})
        rows.append({"word": it["w"], "kind": it["kind"], "hint": it.get("hint"), "arpa": E.strip(it["arpa"]),
                     "ipa": E.arpa2ipa(it["arpa"]).replace("ˈ", ""), "current_text": it["current_text"], "dict_text": dict_text(it),
                     "opts": A, "phonemes": phon_cands(it["arpa"]),
                     "measures": {k: m.get(k) for k in ("current", "dict", "bark_between")} if m else None})
    (PUB / "compare-data.json").write_text(json.dumps({"voice": "River", "rows": rows,
        "note": "v4 current = the clip the app plays now (eleven_v4, spelling or respelling in 'Say: X.'); v4 + CMU dictionary = "
                "same voice, model, settings, seed and carrier, with content/sound-out.pls (CMU Arpabet) attached."}, indent=1, ensure_ascii=False))
    print(f"{len(rows)} rows; {len(list(dst.glob('*.ogg')))} clips in app/public/compare/")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    {"pls": cmd_pls, "render": cmd_render, "phonemes": cmd_phonemes, "measure": cmd_measure, "compare": cmd_compare,
     "measure-phonemes": cmd_measure_phonemes}.get(c, lambda: sys.exit(__doc__))()
