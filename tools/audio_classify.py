#!/usr/bin/env python3
"""Classify every clip Levels 2-7 still need as EASY (local TTS) or HARD (ElevenLabs River). Decision 30.

  python3 tools/audio_classify.py     # writes content/audio_classes.json, prints counts per level x class x kind

Spoken text per key: L2-4 from content/audio_needed.json (what the River plan would have sent as "Say: <word>."),
L5-7 from content/sessions/*.json via tools/parse_sessions.clip_texts().
EASY = real words (in CMUdict), sentences/passages/questions/definitions/rules/UI lines.
HARD = isolated sounds (ph:*), made-up words (spelling not in CMUdict), syllable chunks (syl:*, sound-by-sound
       blends), and prose clips holding a token neither CMUdict nor a GPC respelling can voice (unusual names).
chars = characters ElevenLabs would bill for the HARD clips in the form the River plan sends them.
"""
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
sys.path.insert(0, str(ROOT / "tools"))


def load_cmu():
    cmu = {}
    for line in (C / "cmudict/cmudict.dict").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(";"): continue
        w, _, rest = line.partition(" ")
        w = re.sub(r"\(\d+\)$", "", w)
        cmu.setdefault(w, [x for x in rest.split("#")[0].split()])
    return cmu


def tokens(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.replace("*", ""))


def known(tok, cmu):
    t = tok.lower()
    if t in cmu: return True
    if t.endswith("'s") and t[:-2] in cmu: return True
    if t.endswith("s") and t[:-1] in cmu: return True       # plurals / 3rd person
    if t.endswith("ed") and (t[:-2] in cmu or t[:-1] in cmu): return True
    if t.endswith("ing") and (t[:-3] in cmu or t[:-3] + "e" in cmu): return True
    return False


def river_chars(c):
    if c["cut"] in ("last", "open"): return len(f"Say: {c['say']}.")
    if c["cut"] == "text": return len(c["text"])
    return 0


def main():
    cmu = load_cmu()
    out = {}
    need = json.loads((C / "audio_needed.json").read_text())
    for lv in ("L2", "L3", "L4"):
        N = need[lv]
        for k, c in N["clips"].items():
            kind = k.split(":")[0]
            if kind in ("w", "ipa"):
                cls = "easy" if c["say"].lower() in cmu else "hard"
                sub = "word" if cls == "easy" else "pseudo"
            elif kind == "syl": cls, sub = "hard", "chunk"
            else: cls, sub = "easy", {"ui": "instruction", "rule": "instruction", "read": "sentence", "lt": "passage",
                                      "q": "sentence", "t2": "sentence"}[kind]
            if cls == "easy" and c["cut"] == "text":
                bad = [t for t in tokens(c["text"]) if not known(t, cmu)]
                if bad: cls, sub = "hard", "name"
            out[k] = {"level": int(lv[1]), "kind": kind, "class": cls, "sub": sub, "chars": river_chars(c), **c}
        for k, c in N["iso"].items():
            out[f"{lv}:{k}"] = {"level": int(lv[1]), "kind": "iso", "class": "hard", "sub": "isolated", "chars": 0, "key": k, **c}
    from parse_sessions import clip_texts
    for f in sorted((C / "sessions").glob("L[567].*.json")):
        S = json.loads(f.read_text())
        for k, t in clip_texts(S).items():
            toks = tokens(t); bad = [x for x in toks if not known(x, cmu)]
            cls, sub = ("hard", "name") if bad else ("easy", "passage" if len(t) > 150 else "sentence")
            if len(toks) <= 2 and not bad: sub = "word"
            out[k] = {"level": int(S["id"][1]), "kind": "ss", "class": cls, "sub": sub, "chars": len(t), "cut": "text", "text": t,
                      **({"oov": bad} if bad else {})}
    (C / "audio_classes.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    tab = defaultdict(lambda: [0, 0])
    for k, v in out.items():
        a = tab[(v["level"], v["class"], v["sub"])]; a[0] += 1; a[1] += v["chars"]
    print(f"{'level':5} {'class':5} {'sub':12} {'clips':>6} {'chars':>8}")
    for key in sorted(tab): print(f"L{key[0]:<4} {key[1]:5} {key[2]:12} {tab[key][0]:>6} {tab[key][1]:>8}")
    tot = defaultdict(lambda: [0, 0])
    for v in out.values(): t = tot[v["class"]]; t[0] += 1; t[1] += v["chars"]
    print("TOTAL", {k: v for k, v in tot.items()})
    oov = Counter(w.lower() for v in out.values() for w in v.get("oov", []))
    print("OOV tokens", len(oov), oov.most_common(40))


if __name__ == "__main__":
    main()
