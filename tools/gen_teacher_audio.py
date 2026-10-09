#!/usr/bin/env python3
"""Render the teacher-voice lines (content/teacher_lines.json) in the shipped voice, WITHOUT rebuilding every clip.

  python3 tools/gen_teacher_audio.py plan                 # what would be rendered, characters, no API
  python3 tools/gen_teacher_audio.py render [--cap 5000]  # render in tier order until the cap, encode, update the index

Same voice, model, settings and seed as tools/gen_audio_el.py (River, eleven_v4, speed .9). Same cut (trim), same
loudness rule (-18 LUFS on the shipped Opus for clips >= 0.4 s; shorter clips RMS-matched to the word class), same
Opus 24 kb/s. New lines are merged into content/ui_lines.json (so `gen_audio_el.py plan/build` keeps them) and into
content/audio_index.json / app/public/audio. Every NEW render is appended to content/el_chars.json (kind "teacher").
A line that would pass the cap is skipped and listed.
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_audio_el as G

C, OUT = G.C, G.OUT
LEDGER = C / "el_chars.json"
SRC = C / "teacher_lines.json"


def todo(cap):
    lines = json.loads(SRC.read_text()); idx = json.loads((C / "audio_index.json").read_text())
    voice = G.get_voice(); out, skipped, used = [], [], 0
    for k, v in sorted(lines.items(), key=lambda kv: (kv[1]["tier"], list(lines).index(kv[0]))):
        if f"ui:{k}" in idx["clips"]: continue
        n = 0 if G.cached(voice, v["text"]) else len(v["text"])
        if used + n > cap: skipped.append((k, v["text"], n)); continue
        used += n; out.append((k, v["text"], n))
    return out, skipped, used


def word_rms():
    plan = json.loads((C / "audio_plan.json").read_text()); voice = G.get_voice(); vals = []
    for key, c in plan.items():
        if not key.startswith(("w:", "ipa:")) or c["cut"] not in ("last", "open"): continue
        t = G.req_text(c)
        if not G.cached(voice, t): continue   # never spend characters to measure loudness
        a, al = G.tts(voice, t)
        w = G.cut_last(a, t, al, c["say"])
        if c["cut"] == "open": w = G.open_cut(w)
        if len(w) >= G.MIN_LUFS_DUR * G.SR: vals.append(G.rms_db(G.loudness(w)[0]))
    return float(np.median(vals))


def encode_clip(a, cid, wrms):
    b, rule = G.loudness(a, wrms)
    dst = OUT / f"{cid}.ogg"; d = G.encode(b, dst)
    if rule.startswith("lufs"):
        gain = 0.0
        for _ in range(4):
            L = G.lufs(G.decode(dst))
            if L is None or abs(G.LUFS - L) <= 0.3: break
            gain += G.LUFS - L; G.encode(b * 10 ** (gain / 20), dst)
    return d, rule, G.lufs(G.decode(dst))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    cap = int(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 5000
    out, skipped, used = todo(cap)
    print(f"{len(out)} lines, {used} new characters (cap {cap}); skipped {len(skipped)}: {[s[0] for s in skipped]}")
    if cmd == "plan" or not out: return
    voice = G.get_voice()
    G.render_all({t for _, t, _ in out}, voice)
    ledger = json.loads(LEDGER.read_text())
    ui = json.loads((C / "ui_lines.json").read_text()); idx = json.loads((C / "audio_index.json").read_text())
    plan = json.loads((C / "audio_plan.json").read_text())
    wrms = word_rms(); print(f"word RMS {wrms:.1f} dBFS")
    for k, t, n in out:
        if not G.cached(voice, t): print("NOT RENDERED", k); continue
        a, _ = G.tts(voice, t); a = G.trim(a)
        cid = hashlib.sha1(f"{G.rkey(voice, t)}|text||\"\"".encode()).hexdigest()[:12]
        d, rule, L = encode_clip(a, cid, wrms)
        idx["clips"][f"ui:{k}"] = {"id": cid, "dur": d}
        ui[k] = t; plan[f"ui:{k}"] = {"cut": "text", "text": t}
        if n: ledger.append({"text": t, "model": G.MODEL, "kind": "teacher", "chars": n})
        print(f"  ui:{k:16s} {d:5.2f}s {rule:12s} {L if L is None else round(L, 1)}  {t}")
    idx["missing"] = [m for m in idx.get("missing", []) if m not in idx["clips"]]
    (C / "audio_index.json").write_text(json.dumps(idx, indent=1, ensure_ascii=False))
    (C / "ui_lines.json").write_text(json.dumps(ui, indent=1, ensure_ascii=False))
    (C / "audio_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    LEDGER.write_text(json.dumps(ledger, indent=0, ensure_ascii=False))
    print(f"teacher ledger total: {sum(x['chars'] for x in ledger if x['kind'] == 'teacher')} characters")


if __name__ == "__main__":
    main()
