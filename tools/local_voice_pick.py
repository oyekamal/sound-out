#!/usr/bin/env python3
"""Pick the Kokoro stock voice closest to ElevenLabs River (decision 30). Run with bakeoff/.venv/bin/python.

For N shipped River sentence clips (text from content/audio_plan.json), render the same text with every Kokoro voice
and compare: WavLM x-vector cosine to the River clips (microsoft/wavlm-base-plus-sv), median F0, speech rate.
Writes content/local/voice_pick.json. Machine measure only; the critic + Kamal's ears decide.
"""
import json, sys, glob, os, subprocess
from pathlib import Path
import numpy as np, soundfile as sf, torch
ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
SR = 24000
VOICES = "af_river af_heart af_nicole af_sarah af_sky af_nova af_alloy af_aoede af_jessica af_kore af_bella am_adam am_echo am_eric am_liam am_onyx am_puck am_fenrir am_michael bf_emma".split()


def dec(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").astype(np.float32)


def f0(x16):
    import librosa
    f, v, _ = librosa.pyin(x16, fmin=70, fmax=400, sr=16000, frame_length=1024)
    f = f[~np.isnan(f)]
    return float(np.median(f)) if len(f) else 0.0, float(np.percentile(f, 90) - np.percentile(f, 10)) if len(f) else 0.0


def main():
    from kokoro import KModel, KPipeline
    from transformers import AutoFeatureExtractor, WavLMForXVector
    plan = json.loads((C / "audio_plan.json").read_text()); idx = json.loads((C / "audio_index.json").read_text())["clips"]
    items = [(k, c["text"]) for k, c in plan.items() if c.get("cut") == "text" and k in idx and 1.5 < idx[k]["dur"] < 9 and k.startswith(("read", "lt", "q", "ui"))]
    items = items[::max(1, len(items) // 16)][:16]
    fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xm = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").eval()
    def emb(x16):
        i = fe(x16, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad(): e = xm(**i).embeddings
        return torch.nn.functional.normalize(e, dim=-1)[0]
    ref = [dec(ROOT / "app/public/audio" / f"{idx[k]['id']}.ogg") for k, _ in items]
    rE = torch.stack([emb(x) for x in ref]); rmean = torch.nn.functional.normalize(rE.mean(0), dim=0)
    rf = np.array([f0(x) for x in ref]); rdur = sum(len(x) for x in ref) / 16000; rchars = sum(len(t) for _, t in items)
    out = {"river": {"f0_median": float(np.median(rf[:, 0])), "f0_range": float(np.median(rf[:, 1])), "chars_per_s": rchars / rdur}}
    print("river", out["river"], flush=True)
    m = KModel(repo_id="hexgrad/Kokoro-82M").eval(); pipe = KPipeline(lang_code="a", model=m)
    snap = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices"))[0]
    from scipy.signal import resample_poly
    for v in VOICES:
        vt = torch.load(f"{snap}/{v}.pt", weights_only=True); es, fs, ds, ch = [], [], 0.0, 0
        pipe_v = KPipeline(lang_code="b" if v.startswith("b") else "a", model=m)
        for k, t in items:
            a = np.concatenate([r.audio.numpy() for r in pipe_v(t, voice=vt, speed=0.9)])
            x16 = resample_poly(a, 2, 3).astype(np.float32)
            es.append(emb(x16)); fs.append(f0(x16)); ds += len(x16) / 16000; ch += len(t)
        E = torch.stack(es); cos_each = float((E * rmean).sum(1).mean()); cos_mean = float(torch.dot(torch.nn.functional.normalize(E.mean(0), dim=0), rmean))
        fs = np.array(fs)
        out[v] = {"cos_each": cos_each, "cos_mean": cos_mean, "f0_median": float(np.median(fs[:, 0])), "f0_range": float(np.median(fs[:, 1])), "chars_per_s": ch / ds}
        print(v, {k: round(x, 3) for k, x in out[v].items()}, flush=True)
    (C / "local" / "voice_pick.json").write_text(json.dumps(out, indent=1))
    print("ranked:", sorted([k for k in out if k != "river"], key=lambda k: -out[k]["cos_mean"]))


if __name__ == "__main__": main()
