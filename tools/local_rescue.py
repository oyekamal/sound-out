#!/usr/bin/env python3
"""Rescue real words that failed the strict local Whisper gate (decision 31). Run with bakeoff/.venv/bin/python.

  local_rescue.py near                 # step A: re-gate the failed words with a near-match rule calibrated on River (free, uses stored Whisper text)
  local_rescue.py reroll SHARD N       # step B: free re-rolls for what is still failing: text@0.9 / ipa@0.9 / voice af_nova / carrier-phrase trim
  local_rescue.py apply                # fold both into content/local/manifest.json (gate=pass, rescue=<method>)
  local_rescue.py report               # counts per method -> content/local/rescue_report.json

Calibration (River = ElevenLabs River, the 618 real-word clips of Level 1, same Whisper small.en + 'Say.' carrier):
  strict gate 533/618 = 86.2%.  With the near rule 589/618 = 95.3%.  False accept of the near rule on shuffled targets 1.0%.
The near rule accepts a failed word when Whisper (small.en/small, first pass or re-roll) heard a word within 1 character edit
(1 phone edit, same first phone, for words of 3+ phones) AND the phone recogniser (wav2vec2 espeak, tools/phone_rec.py) puts the audio strictly
closer to the TARGET's phones than to the HEARD word's phones. That second test is what keeps one-phone errors (path -> pass) out: the
River baseline shows Whisper alone would let them through. A heard word outside CMUdict needs PER <= 0.34 against the target instead.
"""
import glob, hashlib, json, os, re, sys
from pathlib import Path
import numpy as np, soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import gen_audio_local as L
C = L.C
OUTD = C / "local"
CARRIER_WORDS = {"say", "so", "zay", "they", "zayu", "zayn", "sei", "sa", "the"}
ARPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "EH": "ɛ", "ER": "ɝ", "EY": "eɪ",
        "F": "f", "G": "ɡ", "HH": "h", "IH": "ɪ", "IY": "i", "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ", "OW": "oʊ", "OY": "ɔɪ",
        "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ", "T": "t", "TH": "θ", "UH": "ʊ", "UW": "u", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
_CM = None


def CM():
    global _CM
    if _CM is None:
        from audio_classify import load_cmu
        _CM = load_cmu()
    return _CM


def W(t): return re.findall(r"[a-z]+(?:'[a-z]+)?", t.lower())


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def arpa(w):
    v = CM().get(w); return [x.rstrip("012") for x in v] if v else None


def ipa_of(w): return "".join(ARPA[p] for p in arpa(w))


def strict(tgt, heard):
    tp = arpa(tgt)
    for h in heard:
        hw = W(h)
        if hw and (hw[-1] == tgt or tgt in hw or (tp and arpa(hw[-1]) == tp)): return True
    return False


def near_words(tgt, heard):
    """heard words within one character edit (or one phone edit, same first phone) of the target"""
    tp, out = arpa(tgt), []
    for h in heard:
        for w in W(h)[-2:]:
            if w in CARRIER_WORDS or w == tgt: continue
            if (len(tgt) >= 4 and ed(w, tgt) <= 1) or (len(tgt) == 3 and ed(w, tgt) <= 1 and w[0] == tgt[0] and w[-1] == tgt[-1]): out.append(w); continue
            wp = arpa(w)
            if tp and wp and len(tp) >= 3 and ed(wp, tp) <= 1 and wp[0] == tp[0]: out.append(w)
    return list(dict.fromkeys(out))


def judge(x, tgt, ipa, heard):
    """-> (verdict, method) for audio x (24 kHz) given Whisper's transcripts"""
    import phone_rec
    if strict(tgt, heard): return True, "strict"
    cands = near_words(tgt, heard)
    if not cands: return False, None
    pt, got = phone_rec.per(x, ipa)
    for w in cands:
        if arpa(w):
            ph, _ = phone_rec.per(x, ipa_of(w))
            if pt < ph: return True, f"near:{w}"
        elif pt <= 0.34: return True, f"near-oov:{w}"
    return False, None


def failed_inputs():
    classes = json.loads((C / "audio_classes.json").read_text()); ren = L.renderable(classes)
    res = {}
    for f in glob.glob(str(OUTD / "gate_words_*.json")): res.update(json.loads(Path(f).read_text()))
    byci = {}
    for k, v in sorted(ren.items()):
        if v["kind"] in ("w", "ipa"):
            mode, inp = L.job(k, v); byci.setdefault(L.ckey(mode, inp), (k, v))
    fails = {ci: (byci[ci], r) for ci, r in res.items() if not r["pass"] and not r.get("reroll", {}).get("pass")}
    return fails, byci, ren


def near():
    fails, _, _ = failed_inputs(); out = {}
    for n, (ci, ((k, v), r)) in enumerate(sorted(fails.items())):
        tgt = v["say"].lower()
        heard = list(r["heard"].values()) + list(r.get("reroll", {}).get("heard", {}).values())
        if not near_words(tgt, heard): out[ci] = {"say": tgt, "ok": False}; continue
        best = (False, None)
        for cache in [ci] + ([r["reroll"]["cache"]] if r.get("reroll") else []):
            w = L.RAW / f"{cache}.wav"
            if not w.exists(): continue
            hh = list(r["heard"].values()) if cache == ci else list(r["reroll"]["heard"].values())
            ok, m = judge(sf.read(w)[0], tgt, v["ipa"], hh)
            if ok: best = (True, m, cache); break
        out[ci] = {"say": tgt, "ok": best[0], "method": best[1], "cache": best[2] if best[0] else None}
        if n % 100 == 0: print(n, len(fails), sum(o["ok"] for o in out.values()), flush=True)
    (OUTD / "rescue_near.json").write_text(json.dumps(out, ensure_ascii=False))
    print("near rescued", sum(o["ok"] for o in out.values()), "of", len(out))


# ------------------------------------------------------------------ step B
def segments(a, thr_db=-45.0, gap_ms=60):
    fr = int(.01 * L.SR); n = len(a) // fr
    e = 20 * np.log10(np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1)) + 1e-9)
    on = e > thr_db; segs, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or (j + 1 < n and on[j + 1:j + 1 + gap_ms // 10].any() and not on[j])): j += 1
            segs.append((i * fr, min(len(a), j * fr))); i = j
        else: i += 1
    return segs


def cut_carrier(a, lead):
    """audio of 'The word is X.' -> X: last voiced segment after a pause; else everything after the lead-in length"""
    segs = segments(a)
    if len(segs) >= 2 and segs[-1][1] - segs[-1][0] > int(.08 * L.SR): w = a[segs[-1][0]:]
    else: w = a[int(lead * .92):]
    return L.trim(w)


def load_models():
    import torch
    from kokoro import KModel, KPipeline
    m = KModel(repo_id="hexgrad/Kokoro-82M").eval(); pipe = KPipeline(lang_code="a", model=m, repo_id="hexgrad/Kokoro-82M")
    snap = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices"))[0]
    vt = {v: torch.load(f"{snap}/{v}.pt", weights_only=True) for v in (L.VOICE, "af_nova")}
    return m, pipe, vt


def reroll(shard, n):
    import torch
    torch.set_num_threads(int(os.environ.get("SO_THREADS", "2")))
    import local_gate as G
    G.carrier_load()
    fails, _, _ = failed_inputs()
    nearr = json.loads((OUTD / "rescue_near.json").read_text())
    todo = sorted(ci for ci in fails if not nearr.get(ci, {}).get("ok"))[shard::n]
    op = OUTD / f"rescue_reroll_{shard}.json"
    done = json.loads(op.read_text()) if op.exists() else {}
    m, pipe, vt = load_models()
    lead = L.trim(L.render_one(pipe, m, vt[L.VOICE], "text", "The word is.", L.SPEED))
    lead_len = len(lead)
    def variants(tgt, ipa):
        yield "speed0.9-ipa", lambda: L.render_one(pipe, m, vt[L.VOICE], "ipa", L.to_misaki(ipa), 0.9)
        yield "speed0.9-text", lambda: L.render_one(pipe, m, vt[L.VOICE], "text", tgt + ".", 0.9)
        yield "nova-text", lambda: L.render_one(pipe, m, vt["af_nova"], "text", tgt + ".", L.SPEED)
        yield "nova-ipa", lambda: L.render_one(pipe, m, vt["af_nova"], "ipa", L.to_misaki(ipa), L.SPEED)
        yield "carrier", lambda: cut_carrier(L.render_one(pipe, m, vt[L.VOICE], "text", f"The word is {tgt}.", L.SPEED), lead_len)
    for j, ci in enumerate(todo):
        if ci in done: continue
        (k, v), _ = fails[ci]; tgt = v["say"].lower(); rec = {"say": tgt, "ok": False, "tried": []}
        for name, fn in variants(tgt, v["ipa"]):
            try: a = L.trim(fn())
            except Exception as e: rec["tried"].append([name, f"ERR {e}"]); continue
            if len(a) < int(.12 * L.SR): rec["tried"].append([name, "short"]); continue
            heard = list(G.whisper_hear(np.concatenate([G.CARRIER, np.zeros(int(.25 * L.SR)), a]), ("small.en",)).values())
            ok, how = judge(a, tgt, v["ipa"], heard)
            rec["tried"].append([name, heard[0], how])
            if ok:
                rid = hashlib.sha1(f"rescue|{name}|{ci}".encode()).hexdigest()
                sf.write(L.RAW / f"{rid}.wav", a, L.SR, subtype="PCM_16")
                rec.update({"ok": True, "method": name, "cache": rid, "how": how}); break
        done[ci] = rec
        if j % 10 == 0:
            op.write_text(json.dumps(done, ensure_ascii=False)); print(f"shard {shard}: {j}/{len(todo)} rescued {sum(d['ok'] for d in done.values())}", flush=True)
    op.write_text(json.dumps(done, ensure_ascii=False)); print(f"shard {shard} done rescued {sum(d['ok'] for d in done.values())}/{len(done)}")


def apply():
    fails, byci, ren = failed_inputs()
    nearr = json.loads((OUTD / "rescue_near.json").read_text()); rr = {}
    for f in glob.glob(str(OUTD / "rescue_reroll_*.json")): rr.update(json.loads(Path(f).read_text()))
    man = json.loads(L.MAN.read_text()); counts = {}
    for k, v in ren.items():
        if v["kind"] not in ("w", "ipa") or man.get(k, {}).get("gate") != "fail": continue
        mode, inp = L.job(k, v); ci = L.ckey(mode, inp)
        r = nearr.get(ci) or {}
        if r.get("ok"): meth, cache = "near", r["cache"]
        elif rr.get(ci, {}).get("ok"): meth, cache = rr[ci]["method"], rr[ci]["cache"]
        else: continue
        e = man[k]; e.update({"gate": "pass-reroll", "reroll": True, "cache": cache, "rescue": meth})
        counts[meth] = counts.get(meth, 0) + 1
    L.MAN.write_text(json.dumps(man, indent=0, ensure_ascii=False))
    (OUTD / "rescue_report.json").write_text(json.dumps({"keys_rescued_by_method": counts, "total": sum(counts.values())}, indent=1))
    print("keys rescued", counts, sum(counts.values()))


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "near": near()
    elif c == "reroll": reroll(int(sys.argv[2]), int(sys.argv[3]))
    elif c in ("apply", "report"): apply()
    else: sys.exit(__doc__)
