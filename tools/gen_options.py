#!/usr/bin/env python3
"""Tap-gate (E6d) option sets for Level 1 — decision (11): a 2x2 grid
{target, onset-change, vowel-change, onset+vowel-change}; for words with no onset (at, in)
the grid is {target, vowel-change, final-change, vowel+final-change}.

Options are SPOKEN (the learner hears them), so foils may use sounds not yet taught.
Real-word targets get real-word foils where the dictionary allows; made-up targets get made-up
foils. Where no real word fills a cell, the cell is filled anyway and flagged `relaxed`.
Writes content/options.json.
"""
import json, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEX = json.loads((ROOT / "content/lexicon.json").read_text())
GPC = json.loads((ROOT / "content/gpc.json").read_text())
PHON = GPC["phonemes"]
VOWELS = ["a", "i", "o", "e", "u"]
CONS = ["s", "t", "p", "n", "m", "d", "g", "k", "r", "h", "b", "f", "l", "j", "v", "w", "z"]
FINAL_OK = [c for c in CONS if c not in ("h", "w", "r", "j")]  # English CVC finals
DICT = {w.strip() for w in open("/usr/share/dict/american-english") if w.strip().isalpha() and w.strip().islower()}
BLOCK = {"ass", "tits", "tit", "sexy", "sex", "piss", "puss", "pus", "cum", "fat", "nob", "dam", "fag", "nig", "fuk", "god", "jap", "kik", "dik"}
SPELL = {"s": ["s"], "t": ["t"], "p": ["p"], "n": ["n"], "m": ["m"], "d": ["d"], "g": ["g"], "k": ["c", "k"],
         "r": ["r"], "h": ["h"], "b": ["b"], "f": ["f"], "l": ["l"], "j": ["j"], "v": ["v"], "w": ["w"], "z": ["z"],
         "a": ["a"], "i": ["i"], "o": ["o"], "e": ["e"], "u": ["u"], "ks": ["x"], "kw": ["qu"], "y": ["y"]}
BLOCK_IPA = {"ˈæs", "tˈɪts", "tˈɪt", "pˈɪs", "kˈʌm", "sˈɛks", "fˈʌk", "dˈɪk", "kˈɑk", "ʃˈɪt"}
FINAL_SPELL = {"k": ["ck", "k"], "f": ["ff", "f"], "l": ["ll", "l"], "s": ["ss", "s"], "z": ["zz", "z"]}


def spellings(p):
    opts = []
    for i, ph in enumerate(p):
        opts.append(FINAL_SPELL.get(ph, SPELL[ph]) if i == len(p) - 1 and i > 0 else SPELL[ph])
    return ["".join(x) for x in itertools.product(*opts)]


def real(p):
    return next((s for s in spellings(p) if s in DICT and s not in BLOCK), None)


def ipa(p):
    out, st = "", False
    for x in p:
        if x in VOWELS and not st: out += "ˈ"; st = True
        out += PHON[x]
    return out


def build(entry):
    p = entry["p"]
    if not p or entry["kind"] not in ("real", "pseudo"): return None
    vi = [i for i, x in enumerate(p) if x in VOWELS]
    if len(vi) != 1: return None
    v = vi[0]
    # onset axis = the consonant just before the vowel; final axis = the consonant just after it
    if v == 0:
        if len(p) < 2: return None
        a, b, pool_b, axes = v, 1, FINAL_OK, ("vowel", "final")
    else:
        a, b, pool_b, axes = v, v - 1, CONS, ("vowel", "onset")
        if v - 1 > 0:  # cluster onset (sta): keep it a legal s-cluster
            pool_b = [c for c in ["t", "p", "k", "n", "m", "l", "w"]]
    want_real = entry["kind"] == "real"
    target = entry["w"]
    def ok(q):
        r = real(q)
        if want_real: return r
        return None if r else spellings(q)[0]
    best, relaxed = None, False
    # pass 1: all three cells match lexicality; pass 2: allow mismatch (flag relaxed)
    for strict in (True, False):
        for nb in pool_b:
            if nb == p[b] or (b + 1 < len(p) and nb == p[b + 1]) or (b > 0 and nb == p[b - 1]): continue
            for nv in VOWELS:
                if nv == p[a]: continue
                q1 = list(p); q1[b] = nb
                q2 = list(p); q2[a] = nv
                q3 = list(p); q3[b] = nb; q3[a] = nv
                labels = [ok(q) for q in (q1, q2, q3)]
                if strict and not all(labels): continue
                labels = [l or spellings(q)[0] for l, q in zip(labels, (q1, q2, q3))]
                if len({target, *labels}) < 4: continue
                if any(ipa(q) in BLOCK_IPA for q in (q1, q2, q3)): continue
                best = (q1, q2, q3, labels); break
            if best: break
        if best: relaxed = not strict; break
    if not best: return None
    q1, q2, q3, labels = best
    cell = lambda q, lab, kind: {"w": lab, "p": q, "ipa": ipa(q), "cell": kind}
    ax_b, ax_a = axes[1], axes[0]
    return {"target": {"w": target, "p": p, "ipa": entry["ipa"], "cell": "target"},
            "foils": [cell(q1, labels[0], ax_b), cell(q2, labels[1], ax_a), cell(q3, labels[2], f"{ax_b}+{ax_a}")],
            "axes": [ax_b, ax_a], "kind": entry["kind"], "relaxed": relaxed}


def main():
    out, skipped = {}, []
    for k, e in LEX.items():
        o = build(e)
        if o: out[k] = o
        elif e["kind"] in ("real", "pseudo"): skipped.append(k)
    (ROOT / "content/options.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"options for {len(out)} words; relaxed {sum(o['relaxed'] for o in out.values())}; skipped {skipped}")


if __name__ == "__main__":
    main()
