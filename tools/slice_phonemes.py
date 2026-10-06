#!/usr/bin/env python3
"""Isolated sounds sliced from Kokoro's OWN word renders (coordinator ask, 2026-10-06).

For each Level 1 sound, render a carrier word from IPA, take Kokoro's predicted per-token durations
(pred_dur, 1 unit = 600 samples at 24 kHz), cut the target phoneme's span, trim, pad 40/80 ms,
normalise to -3 dBFS and encode. Stops keep the burst only (cut before the vowel's span).
The IPA-direct render (gen_audio.py `ph:<id>`) stays alongside for comparison on app/public/listen.html.

  <kokoro-venv>/bin/python tools/slice_phonemes.py
Writes app/public/audio/sl_<id>.ogg, app/public/audio/slw_<id>.ogg (carrier word), content/slices.json.
"""
import json, subprocess
from pathlib import Path
import numpy as np, soundfile as sf, torch

torch.set_num_threads(6)
from misaki import espeak as _e
def _boom(*a, **k): raise RuntimeError("espeak fallback disabled")
_e.EspeakFallback = _boom
from kokoro import KPipeline, KModel

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "app/public/audio"
SR, HOP = 24000, 600
# sound id -> (carrier word, carrier IPA in Kokoro alphabet, index range of the target phoneme chars in the IPA string)
STOPS = {"t", "p", "d", "g", "k", "b"}
CARRIER = {
    "s": ("sat", "sˈæt"), "a": ("at", "ˈæt"), "t": ("tap", "tˈæp"), "p": ("pat", "pˈæt"), "i": ("it", "ˈɪt"),
    "n": ("nap", "nˈæp"), "m": ("map", "mˈæp"), "d": ("dip", "dˈɪp"), "g": ("got", "ɡˈɑt"), "o": ("on", "ˈɑn"),
    "k": ("kit", "kˈɪt"), "e": ("egg", "ˈɛɡ"), "u": ("up", "ˈʌp"), "r": ("rat", "ɹˈæt"), "h": ("hat", "hˈæt"),
    "b": ("bat", "bˈæt"), "f": ("fan", "fˈæn"), "l": ("lap", "lˈæp"), "j": ("jam", "ʤˈæm"), "v": ("van", "vˈæn"),
    "w": ("wet", "wˈɛt"), "ks": ("box", "bˈɑks"), "y": ("yes", "jˈɛs"), "z": ("zip", "zˈɪp"), "kw": ("quit", "kwˈɪt"),
}
TARGET = {"ks": ("k", "s"), "kw": ("k", "w")}
IPA_OF = {"s": "s", "a": "æ", "t": "t", "p": "p", "i": "ɪ", "n": "n", "m": "m", "d": "d", "g": "ɡ", "o": "ɑ", "k": "k",
          "e": "ɛ", "u": "ʌ", "r": "ɹ", "h": "h", "b": "b", "f": "f", "l": "l", "j": "ʤ", "v": "v", "w": "w", "y": "j", "z": "z"}
VOICELESS = {"s", "t", "p", "k", "h", "f", "ks"}


def periodicity(x):
    """Peak normalised autocorrelation in 80-400 Hz: ~1 = voiced/vowel-like, ~0 = noise/silence."""
    if len(x) < 600: return 0.0
    x = x - x.mean(); e = float((x * x).sum())
    if e < 1e-8: return 0.0
    ac = np.correlate(x, x, "full")[len(x) - 1:]
    lo, hi = SR // 400, min(SR // 80, len(ac) - 1)
    return float(ac[lo:hi].max() / ac[0])


def encode(a, dst):
    a = np.concatenate([np.zeros(int(.04 * SR)), a, np.zeros(int(.08 * SR))])
    a = a * (10 ** (-3 / 20) / max(1e-6, np.abs(a).max()))
    tmp = dst.with_suffix(".wav"); sf.write(tmp, a, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-c:a", "libopus", "-b:a", "32k", "-ac", "1", str(dst)], check=True)
    tmp.unlink()
    return round(len(a) / SR, 3)


def main():
    model = KModel(repo_id="hexgrad/Kokoro-82M").to("cpu").eval()
    pack = KPipeline(lang_code="a", model=False).load_voice("af_heart")
    rows = []
    for sid, (word, ipa) in CARRIER.items():
        with torch.no_grad():
            out = KPipeline.infer(model, ipa, pack, 1.0)
        audio = out.audio.numpy(); dur = out.pred_dur.numpy().astype(int)
        # token i of the IPA string = dur[i+1] (dur[0] and dur[-1] are the pad tokens)
        starts = np.concatenate([[0], np.cumsum(dur)]) * HOP
        chars = list(ipa)
        want = TARGET[sid] if sid in TARGET else (IPA_OF[sid],)
        idx = [i for i, ch in enumerate(chars) if ch in want]
        # first occurrence run of the wanted chars (skip the stress mark)
        run = []
        for i in idx:
            if not run or i == run[-1] + 1 or (chars[run[-1] + 1] == "ˈ" and i == run[-1] + 2): run.append(i)
        a0, a1 = starts[run[0] + 1], starts[run[-1] + 2]
        nxt = run[-1] + 1
        if nxt < len(chars) and chars[nxt] == "ˈ" and sid not in STOPS:   # stress-mark frames belong to neighbours
            a1 += (starts[nxt + 2] - starts[nxt + 1]) // 2
        if run[0] > 0 and chars[run[0] - 1] == "ˈ":
            a0 = starts[run[0]]
        # 1) Kokoro's predicted durations run ~0.1 s LATE against its own audio: re-anchor on the acoustic onset
        x = audio.astype(np.float64); pk = np.abs(x).max(); W = int(.01 * SR)
        rms = lambda st: float(np.sqrt((x[st:st + W] ** 2).mean()))
        zcr = lambda st: float(np.mean(np.abs(np.diff(np.sign(x[st:st + W])))) / 2)
        onset = next(st for st in range(0, len(x) - W, W // 2) if rms(st) > .05 * pk)
        shift = onset - starts[1]
        a0, a1 = max(0, a0 + shift), max(0, a1 + shift)
        method = "durations re-anchored on onset"
        # 2) voiceless sounds: end where the vowel starts (low zero-crossing rate + energy)
        if sid in VOICELESS and sid != "ks":
            vo = next((st for st in range(a0 + W, len(x) - W, W // 2) if zcr(st) < .15 and rms(st) > .15 * pk), None)
            if vo: a1 = vo - int(.005 * SR); method = "cut at vowel onset (zero-crossing)"
            if sid in STOPS: a1 = min(a1, a0 + int(.09 * SR))
        if sid in ("a", "i", "o", "e", "u"):   # vowel in a VC word: end where the closure starts
            ve = next((st for st in range(a0 + int(.05 * SR), len(x) - W, W // 2) if rms(st) < .12 * pk), None)
            if ve: a1 = ve; method = "vowel ends at closure (energy)"
        seg = x[a0:a1]
        thr = 10 ** (-40 / 20) * max(1e-6, np.abs(seg).max())
        nz = np.where(np.abs(seg) > thr)[0]
        if len(nz): seg = seg[nz[0]: nz[-1] + 1]
        ms = round(1000 * len(seg) / SR)
        tail = seg[-int(.02 * SR):]
        tz = float(np.mean(np.abs(np.diff(np.sign(tail)))) / 2) if len(tail) > 2 else 0
        if sid in VOICELESS and sid not in STOPS and tz < .2: verdict = "vowel leak (tail is voiced)"
        elif sid in STOPS and not (10 <= ms <= 90): verdict = f"burst length off ({ms} ms)"
        elif sid not in STOPS and ms < 80: verdict = f"too short ({ms} ms)"
        elif sid in VOICELESS or sid in ("a", "i", "o", "e", "u"): verdict = "clean (heuristic)"
        else: verdict = "voiced: no automatic boundary check, needs ears"
        per = round(tz, 2)
        d1 = encode(seg, OUT / f"sl_{sid}.ogg")
        d2 = encode(audio.astype(np.float64)[np.abs(audio).argmax() * 0:], OUT / f"slw_{sid}.ogg")
        rows.append({"id": sid, "word": word, "ipa": ipa, "ms": ms, "tailZcr": per, "method": method, "verdict": verdict, "dur": d1, "wordDur": d2})
        print(sid, word, ms, round(per, 2), verdict)
    (ROOT / "content/slices.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    cov = ROOT / "content/coverage.md"
    txt = cov.read_text().split("\n## Isolated sounds")[0].rstrip() + "\n\n"
    clean = [r["id"] for r in rows if r["verdict"].startswith("clean")]
    ears = [r["id"] for r in rows if r["verdict"].startswith("voiced")]
    bad = [r["id"] for r in rows if not r["verdict"].startswith(("clean", "voiced"))]
    txt += ("## Isolated sounds sliced from Kokoro word renders (tools/slice_phonemes.py)\n\n"
            "Kokoro's predicted durations run about 0.1 s late against its own audio, so raw duration slicing cut the wrong span "
            "(the /s/ of 'sat' came out as the vowel). Slices are re-anchored on the acoustic onset; voiceless sounds are then cut "
            "at the vowel onset (zero-crossing rate), vowels end at the closure (energy). Voiced consonants have no automatic "
            "boundary check. **Machine checks are heuristics; Kamal's ears on app/public/listen.html decide.**\n\n"
            f"- Slice cleanly (heuristic): {', '.join(clean)}\n- Voiced, needs ears: {', '.join(ears)}\n- Do not slice cleanly: {', '.join(bad)}\n\n"
            "| Sound | Carrier | Slice ms | Method | Verdict |\n|---|---|---|---|---|\n"
            + "\n".join(f"| {r['id']} | {r['word']} | {r['ms']} | {r['method']} | {r['verdict']} |" for r in rows) + "\n")
    cov.write_text(txt)
    plan = json.loads((ROOT / "content/audio_plan.json").read_text())
    for r in rows: r["ipaDirect"] = plan[f"ph:{r['id']}"]["id"]
    data = {"rows": rows, "sat": plan["w:sat"]["id"], "note": "Kokoro af_heart. Sliced = cut from a Kokoro word render by predicted durations; IPA direct = the phoneme rendered alone."}
    (ROOT / "app/public/listen-data.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
