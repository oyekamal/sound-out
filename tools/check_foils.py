#!/usr/bin/env python3
"""Pronunciation check of every MADE-UP option clip (targets and foils of pseudo items).

  python3 tools/check_foils.py            # whisper both models, writes content/foil_check.json + content/foil_check.md
  python3 tools/check_foils.py --fix      # for flagged clips, re-render with alternative respellings (cap 2,000 new characters) and keep the better

Whisper is decoded prompt-free (temperature 0, no previous-text conditioning, language en). The heard text is turned into Arpabet
with CMUdict (word known) or the course GPC table (word not in CMUdict) and compared with the intended Arpabet of the option.
Two models (small, small.en; CUDA is unusable on this box, CPU only); a clip passes when EITHER hears the intended sounds, so the flags are the ones both models miss.
Chosen respellings go to content/foil_respell.json (ipa -> text given to the TTS), which tools/gen_audio_el.py reads.
"""
import json, re, sys, collections
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_audio_el as G

C = G.C
CAP = 2000
VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
CMU = collections.defaultdict(set)
for line in (C / "cmudict/cmudict.dict").read_text(encoding="utf-8").splitlines():
    if not line or line.startswith(";"): continue
    w, _, rest = line.partition(" ")
    w = re.sub(r"\(\d+\)$", "", w)
    CMU[w].add(tuple(x.rstrip("012") for x in rest.split("#")[0].split()))
GPC = json.loads((C / "gpc.json").read_text())
PID = {"s": "S", "a": "AE", "t": "T", "p": "P", "i": "IH", "n": "N", "m": "M", "d": "D", "g": "G", "o": "AA", "k": "K", "e": "EH",
       "u": "AH", "r": "R", "h": "HH", "b": "B", "f": "F", "l": "L", "j": "JH", "v": "V", "w": "W", "y": "Y", "z": "Z"}
G2P = {}
for o in GPC["order"]:
    if o["p"] in PID: G2P[o["g"]] = PID[o["p"]]
G2P.update({"ck": "K", "c": "K", "ff": "F", "ll": "L", "ss": "S", "zz": "Z", "x": "K S", "qu": "K W", "ng": "NG", "ch": "CH", "sh": "SH", "th": "TH"})


def g2p(w):
    out, i = [], 0
    while i < len(w):
        for n in (2, 1):
            g = w[i:i + n]
            if g in G2P: out += G2P[g].split(); i += n; break
        else: i += 1
    return tuple(out)


def heard_prons(text):
    w = re.sub(r"[^a-z]", "", text.lower())
    if not w: return set(), "empty"
    if w in CMU: return CMU[w], "cmu"
    return {g2p(w)}, "g2p"


def collapse(p):   # ignore geminate spelling artefacts and AO/AA, ER/AH+R merges that CMUdict dialects blur
    return tuple({"AO": "AA"}.get(x, x) for x in p)


def match(intended, text):
    ps, how = heard_prons(text)
    ok = any(collapse(p) == collapse(intended) for p in ps)
    return ok, how, sorted(" ".join(p).lower() for p in ps)[:2]


_models = {}
HEARD = C / "foil_heard_cache.json"
_cache = json.loads(HEARD.read_text()) if HEARD.exists() else {}


def hear(a, name, say=None):
    key = f"{name}|{say}"
    if say and key in _cache: return _cache[key]
    h = _hear(a, name)
    if say:
        _cache[key] = h; HEARD.write_text(json.dumps(_cache, indent=0, ensure_ascii=False))
    return h


def _hear(a, name):
    import whisper
    if name not in _models: _models[name] = whisper.load_model(name, device="cpu")
    x = resample_poly(a, 2, 3).astype(np.float32)             # 24k -> 16k
    x = np.concatenate([np.zeros(8000, np.float32), x, np.zeros(8000, np.float32)])
    r = _models[name].transcribe(x, language="en", temperature=0.0, condition_on_previous_text=False, fp16=False, without_timestamps=True)
    return r["text"].strip()


def cut_for(voice, say):
    t = f"Say: {say}."
    a, al = G.tts(voice, t)
    return G.cut_last(a, t, al, say)


def variants(say, p):
    """Alternative respellings to try for a made-up sound sequence, most conservative first."""
    base, out = say, []
    m = re.match(r"^(.*?)([aeiou]+)([^aeiou]+)$", base)
    if m:
        on, v, co = m.groups()
        if len(co) == 1 and co not in "x": out += [on + v + co + co, on + v + co + co + "e"]
        vow = {"AA": ["ah", "o"], "AE": ["a", "ah"], "AH": ["uh", "u"], "EH": ["eh", "e"], "IH": ["ih", "i"], "UH": ["oo"]}.get(p[[i for i, x in enumerate(p) if x in VOWELS][0]], [])
        for vv in vow:
            if vv != v: out.append(on + vv + co)
    return [x for i, x in enumerate(out) if x != base and x not in out[:i]]


def main():
    fix = "--fix" in sys.argv
    voice = G.get_voice()
    plan = json.loads((C / "audio_plan.json").read_text())
    opts = json.loads((C / "options.json").read_text())
    rows = {}
    for k, o in opts.items():
        if o["kind"] != "pseudo": continue
        for x in [o["target"], *o["foils"]]:
            rows.setdefault(x["ipa"], {"w": x["w"], "p": tuple(y.upper() for y in x["p"]), "items": []})["items"].append(k)
    res = []
    for ipa, r in sorted(rows.items(), key=lambda kv: kv[1]["w"]):
        say = plan[f"ipa:{ipa}"]["say"]
        if plan[f"ipa:{ipa}"]["cut"] == "open": continue            # open syllables are cut from a carrier of a real word; not a made-up foil render
        a = cut_for(voice, say)
        heard = {m: hear(a, m, say) for m in ("small", "small.en")}
        oks = {m: match(r["p"], h) for m, h in heard.items()}
        res.append({"foil": r["w"], "say": say, "ipa": ipa, "intended": " ".join(r["p"]).lower(), "heard": heard,
                    "heard_sounds": {m: v[2] for m, v in oks.items()}, "ok": any(v[0] for v in oks.values()), "action": "ok" if any(v[0] for v in oks.values()) else "flagged", "items": r["items"]})
    bad = [x for x in res if not x["ok"]]
    spent = 0
    respell = json.loads((C / "foil_respell.json").read_text()) if (C / "foil_respell.json").exists() else {}
    if fix:
        def sev(x):   # both models agree on the same wrong sounds = most likely a real mispronunciation: fix those first
            p = tuple(x["intended"].upper().split())
            hs = [tuple(v[0].split()) if v else () for v in x["heard_sounds"].values()]
            return (0 if len(set(hs)) == 1 else 1, -abs(len(hs[0]) - len(p)))
        for x in sorted(bad, key=sev):
            p = tuple(x["intended"].upper().split())
            best = None
            for v in variants(x["say"], p):
                if spent + len(f"Say: {v}.") > CAP: x["action"] += "; cap hit"; break
                if not G.cached(voice, f"Say: {v}."): spent += len(f"Say: {v}.")
                a = cut_for(voice, v)
                if len(a) > 1.3 * len(cut_for(voice, x["say"])): continue      # a variant that runs 30% longer was spoken as two syllables
                h = {m: hear(a, m, v) for m in ("small", "small.en")}
                if any(match(p, t)[0] for t in h.values()):
                    best = (v, h); break
            if best:
                respell[x["ipa"]] = best[0]; x["action"] = f"re-rendered as '{best[0]}' (heard {best[1]['small']!r}/{best[1]['small.en']!r}), kept"
            else:
                x["action"] = "no variant heard right; kept original"
        (C / "foil_respell.json").write_text(json.dumps(respell, indent=1, ensure_ascii=False))
    (C / "foil_check.json").write_text(json.dumps({"characters_spent": spent, "rows": res}, indent=1, ensure_ascii=False))
    md = ["# Made-up option pronunciation check (tools/check_foils.py)", "",
          f"{len(res)} made-up option clips (targets and foils of made-up items), whisper small + small.en, prompt-free decode; a clip passes when either model's heard word has the intended Arpabet "
          f"(CMUdict lookup, else the course GPC table). Flagged: {len(bad)}. New characters spent on re-renders: {spent} (cap {CAP}).", "",
          "| foil | rendered as | intended | heard (small / small.en) | action |", "|---|---|---|---|---|"]
    md += [f"| {x['foil']} | {x['say']} | {x['intended']} | {x['heard']['small']} / {x['heard']['small.en']} | {x['action']} |" for x in res if not x["ok"] or "--all" in sys.argv]
    (C / "foil_check.md").write_text("\n".join(md) + "\n")
    print(f"{len(res)} clips, flagged {len(bad)}, spent {spent}")


if __name__ == "__main__":
    main()
