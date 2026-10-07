#!/usr/bin/env python3
"""ElevenLabs pronunciation dictionaries (decision 21): PLS writing, upload, and dictionary-aware cached TTS.

Shared by tools/dict_audio.py. Same voice, settings, seed and cache dir as tools/gen_audio_el.py; the cache key adds
the sha1 of the PLS text, so a changed dictionary = a new render, an unchanged one = no API call.
Uploaded dictionaries are remembered in content/el_dicts.json (sha1 of PLS -> id + version_id).
"""
import base64, hashlib, json, sys, urllib.request, uuid
from pathlib import Path
from xml.sax.saxutils import escape
import numpy as np, soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_audio_el as g

ROOT, C, CACHE, SR = g.ROOT, g.C, g.CACHE, g.SR
REG = C / "el_dicts.json"

# CMU Arpabet <-> IPA (General American). Stress digits are kept separately.
ARPA2IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "B": "b", "CH": "tʃ", "D": "d", "DH": "ð",
            "EH": "ɛ", "ER": "ɝ", "EY": "eɪ", "F": "f", "G": "ɡ", "HH": "h", "IH": "ɪ", "IY": "i", "JH": "dʒ", "K": "k",
            "L": "l", "M": "m", "N": "n", "NG": "ŋ", "OW": "oʊ", "OY": "ɔɪ", "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ",
            "T": "t", "TH": "θ", "UH": "ʊ", "UW": "u", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
VOW = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
_IPA_MULTI = sorted({"ʤ": "JH", "dʒ": "JH", "ʧ": "CH", "tʃ": "CH", "eɪ": "EY", "aɪ": "AY", "oʊ": "OW", "aʊ": "AW",
                     "ɔɪ": "OY", "ɝ": "ER", "ɚ": "ER", "ə": "AH", "ɡ": "G", "g": "G", "r": "R",
                     **{v: k for k, v in ARPA2IPA.items()}}.items(), key=lambda kv: -len(kv[0]))


def ipa2arpa(ipa):
    """Course IPA ('sˈæt', 'ðʌ') -> Arpabet with stress ('S AE1 T'). The vowel after ˈ gets 1, other vowels 0
    (one-syllable words with no mark get 1 unless the vowel is ʌ/ə in a function word -> 0)."""
    out, i, stress = [], 0, False
    s = ipa.replace("ː", "")
    while i < len(s):
        if s[i] in "ˈˌ": stress = True; i += 1; continue
        for k, v in _IPA_MULTI:
            if s.startswith(k, i):
                if v in VOW: out.append(v + ("1" if stress else "0")); stress = False
                else: out.append(v)
                i += len(k); break
        else:
            raise ValueError(f"IPA symbol {s[i]!r} in {ipa!r}")
    return " ".join(out)


def strip(arpa): return " ".join(p.rstrip("012") for p in arpa.split())


def arpa2ipa(arpa, long=False):
    out = []
    for p in arpa.split():
        st, b = p[-1] if p[-1] in "012" else "", p.rstrip("012")
        if st == "1": out.append("ˈ")
        out.append("ə" if (b == "AH" and st == "0") else ARPA2IPA[b])
    return "".join(out) + ("ː" if long else "")


def pls(entries, alphabet="cmu-arpabet"):
    """entries: [(grapheme, phoneme string)]. PLS 1.0 as the ElevenLabs docs show it (case-sensitive graphemes)."""
    rows = "\n".join(f"  <lexeme>\n    <grapheme>{escape(gr)}</grapheme>\n    <phoneme>{escape(ph)}</phoneme>\n  </lexeme>"
                     for gr, ph in entries)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<lexicon version="1.0"\n'
            '    xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"\n'
            '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
            '    xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon\n'
            '        http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"\n'
            f'    alphabet="{alphabet}" xml:lang="en-US">\n{rows}\n</lexicon>\n')


def sha(s): return hashlib.sha1(s.encode()).hexdigest()


def upload(path, name):
    """Upload a PLS file once (keyed by its sha1); returns {'id', 'version_id'}."""
    path = Path(path).resolve(); text = path.read_text(); h = sha(text)
    reg = json.loads(REG.read_text()) if REG.exists() else {}
    if h in reg: return reg[h]
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{name}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\nSound Out (decision 21), sha1 {h[:12]}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{Path(path).name}\"\r\n"
            f"Content-Type: application/pls+xml\r\n\r\n").encode() + text.encode() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/pronunciation-dictionaries/add-from-file", data=body,
                                 method="POST", headers={"xi-api-key": g.api_key(), "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"upload {e.code}: {e.read()[:400].decode(errors='replace')}") from None
    reg[h] = {"id": d["id"], "version_id": d["version_id"], "name": name, "file": str(Path(path).relative_to(ROOT))}
    REG.write_text(json.dumps(reg, indent=1))
    return reg[h]


LEDGER = C / "el_chars.json"   # every NEW (uncached) render this spike made: text, model, chars
_lock = __import__("threading").Lock()


def entries(dict_path):
    import re
    t = Path(dict_path).read_text()
    return dict(re.findall(r"<grapheme>(.*?)</grapheme>\s*<phoneme>(.*?)</phoneme>", t, re.S))


def matched(text, ents):
    """The dictionary entries a text can hit (whole-token, case-sensitive), as 'grapheme=phoneme' strings."""
    import re
    toks = set(re.findall(r"[A-Za-z_']+", text))
    return sorted(f"{g_}={p}" for g_, p in ents.items() if g_ in toks)


def dkey(voice, text, model, settings, hit):
    """Cache key = the plain request key + the dictionary entries that apply to this text (so adding unrelated
    entries to the PLS never invalidates a render)."""
    return hashlib.sha1(f"{g.rkey(voice, text, model, settings)}|dict:{'|'.join(hit)}".encode()).hexdigest()


def is_cached(voice, text, model, settings, dict_path):
    hit = matched(text, entries(dict_path))
    return (CACHE / f"{dkey(voice, text, model, settings or g.SETTINGS, hit)}.wav").exists()


def tts(voice, text, model, settings, dict_path):
    """Cached dictionary-driven render with timestamps -> (float audio @24k, alignment)."""
    settings = settings or g.SETTINGS
    dict_path = Path(dict_path).resolve(); hit = matched(text, entries(dict_path))
    k = dkey(voice, text, model, settings, hit); wav, js = CACHE / f"{k}.wav", CACHE / f"{k}.json"
    if not wav.exists():
        d = upload(dict_path, dict_path.stem)
        body = {"text": text, "model_id": model, "voice_settings": settings, "seed": 18, "language_code": "en",
                "pronunciation_dictionary_locators": [{"pronunciation_dictionary_id": d["id"], "version_id": d["version_id"]}]}
        r = g.api(f"/v1/text-to-speech/{voice}/with-timestamps?output_format=pcm_24000", body)
        a = np.frombuffer(base64.b64decode(r["audio_base64"]), dtype="<i2").astype(np.float64) / 32768
        js.write_text(json.dumps({"voice": voice, "model": model, "settings": settings, "text": text,
                                  "dictionary": {"file": str(dict_path.relative_to(ROOT)), "entries": hit, **d},
                                  "alignment": r.get("alignment"), "normalized_alignment": r.get("normalized_alignment")}))
        sf.write(wav, a, SR, subtype="PCM_16")
        log(text, model, "dict")
    a, _ = sf.read(wav)
    return a, json.loads(js.read_text())["alignment"]


def plain(voice, text, model=None, settings=None):
    """gen_audio_el.tts (no dictionary) + ledger entry when it was not cached."""
    new = not g.cached(voice, text) if (model or g.MODEL) == g.MODEL and settings is None else \
        not (CACHE / f"{g.rkey(voice, text, model, settings)}.wav").exists()
    out = g.tts(voice, text, model, settings)
    if new: log(text, model or g.MODEL, "plain")
    return out


def log(text, model, kind):
    with _lock:
        L = json.loads(LEDGER.read_text()) if LEDGER.exists() else []
        L.append({"text": text, "model": model, "kind": kind, "chars": len(text)})
        LEDGER.write_text(json.dumps(L, indent=0))


def spent():
    return sum(x["chars"] for x in json.loads(LEDGER.read_text())) if LEDGER.exists() else 0
