#!/usr/bin/env python3
"""Evidence sheet for the critic subagent (bakeoff/.venv/bin/python): per sampled local clip, the machine numbers a text-only critic can judge:
transcript vs text, WER, phone-recogniser output vs CMUdict phones, duration, speaking rate, median F0, WavLM x-vector cosine to the River
centroid; plus per-twin local-vs-River deltas. Writes content/local/critic_input.md. Nothing here is a listening test."""
import json, sys, glob, os
from pathlib import Path
import numpy as np, torch
from scipy.signal import resample_poly
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import gen_audio_el as g
import local_gate as G, gen_audio_local as L
import librosa
from transformers import AutoFeatureExtractor, WavLMForXVector
torch.set_num_threads(2)
fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xm = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").eval()
def emb(x16):
    with torch.no_grad(): return torch.nn.functional.normalize(xm(**fe(x16, sampling_rate=16000, return_tensors="pt")).embeddings, dim=-1)[0]
def f0(x16):
    f, _, _ = librosa.pyin(x16, fmin=70, fmax=400, sr=16000, frame_length=1024); f = f[~np.isnan(f)]
    return float(np.median(f)) if len(f) else 0.0
def x16_of(path): return g.decode(path)[:0] if False else resample_poly(g.decode(path), 2, 3).astype(np.float32)
res = json.loads(G.SAMPLE.read_text()); idx = json.loads((L.C / "audio_index.json").read_text())["clips"]
plan = json.loads((L.C / "audio_plan.json").read_text())
rk = [k for k, c in plan.items() if c.get("cut") == "text" and k in idx and idx[k].get("src") is None and 1.5 < idx[k]["dur"] < 9][::12][:14]
rv = [x16_of(g.OUT / f"{idx[k]['id']}.ogg") for k in rk]; cent = torch.nn.functional.normalize(torch.stack([emb(x) for x in rv]).mean(0), dim=0)
rf0 = float(np.median([f0(x) for x in rv]))
out = [f"# Critic evidence: local Kokoro {L.VOICE} (speed {L.SPEED}) vs River\n", f"River reference: median F0 {rf0:.0f} Hz over {len(rk)} shipped sentence clips.\n",
       "## A. 60-clip sample (local only)\n", "| # | key | lvl | kind | sec | chars/s | F0 | cos->River | WER | whisper small.en | text | extra |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for i, r in enumerate(res["samples"], 1):
    x = x16_of(G.PAGE_DIR / Path(r["file"]).name); e = emb(x)
    cps = len(r["text"]) / max(r["sec"], .1)
    extra = f"phoneme-recogniser PER {r.get('phone_per')} heard '{r.get('phone_heard')}'" if r.get("phone_per") is not None else ("OOV overridden: " + ",".join(r.get("oov", [])) if r.get("oov") else "")
    out.append(f"| {i} | {r['key']} | {r['level']} | {r['sub']} | {r['sec']} | {cps:.1f} | {f0(x):.0f} | {float(e @ cent):.2f} | {r['wer']} | {r['heard']['small.en'][:70]} | {r['text'][:70]} | {extra} |")
out += ["", "## B. Twins: same item, local vs shipped River", "| key | text | local sec | River sec | local F0 | River F0 | cos(local,River) | local whisper |", "|---|---|---|---|---|---|---|---|"]
for r in res["twins"]:
    xl = x16_of(G.PAGE_DIR / Path(r["file"]).name); xr = x16_of(ROOT / "bakeoff" / r["river"])
    out.append(f"| {r['key']} | {r['text'][:50]} | {len(xl) / 16000:.2f} | {len(xr) / 16000:.2f} | {f0(xl):.0f} | {f0(xr):.0f} | {float(emb(xl) @ emb(xr)):.2f} | {r['heard']['small.en'][:50]} |")
(L.C / "local" / "critic_input.md").write_text("\n".join(out)); print("written", len(out))
