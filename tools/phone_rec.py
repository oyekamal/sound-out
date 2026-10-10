"""Phoneme recogniser helpers (facebook/wav2vec2-lv-60-espeak-cv-ft, cached; run with bakeoff/.venv). Smoke-test grade, not a score:
the recogniser is multilingual and noisy, so use it to RANK takes of one sound, never as a pass/fail truth on its own."""
import glob, json, os, re
import numpy as np
from scipy.signal import resample_poly

_M = None


def _load():
    global _M
    if _M is None:
        import torch
        from transformers import Wav2Vec2ForCTC
        P = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--facebook--wav2vec2-lv-60-espeak-cv-ft/snapshots/*"))[0]
        V = json.load(open(P + "/vocab.json")); _M = (Wav2Vec2ForCTC.from_pretrained(P).eval(), V, {v: k for k, v in V.items()}, torch)
    return _M


def norm_p(s):
    s = (s.replace("ː", "").replace("ʰ", "").replace("ɐ", "ʌ").replace("ə", "ʌ").replace("ɚ", "ɜ").replace("ɝ", "ɜ").replace("ᵻ", "ɪ")
         .replace("ɫ", "l").replace("ɾ", "t").replace("ɒ", "ɑ").replace("g", "ɡ").replace("ʧ", "tʃ").replace("ʤ", "dʒ").replace("ɹ", "ɹ"))
    return [c for c in re.findall(r"tʃ|dʒ|aʊ|aɪ|eɪ|oʊ|ɔɪ|.", s) if c.strip() and c not in "ˈˌ ‿"]


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def recognise(x24):
    M, V, iv, torch = _load()
    x16 = resample_poly(x24, 2, 3).astype(np.float32)
    x = (x16 - x16.mean()) / (x16.std() + 1e-7)
    with torch.no_grad(): ids = M(torch.tensor(x)[None]).logits[0].argmax(-1).numpy()
    out, prev = [], -1
    for i in ids:
        if i != prev and i != V.get("<pad>", 0): out.append(iv[int(i)])
        prev = i
    return norm_p("".join(out))


def per(x24, target_ipa):
    got, exp = recognise(x24), norm_p(target_ipa)
    return ed(got, exp) / max(1, len(exp)), "".join(got)
