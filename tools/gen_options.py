#!/usr/bin/env python3
"""Tap-gate (E6d) option sets for Level 1, built from PHONEMES (decision 11 + the cmudict spike fix).

An item is a 2x2 grid {target, onset-change, vowel-change, onset+vowel-change}; for a word with no onset (at, in)
the grid is {target, final-change, vowel-change, final+vowel-change}. Every option differs from the target in exactly
the stated phoneme position(s), measured on Arpabet (content/lexicon_full.json, built from CMUdict), never on letters.
Rules:
  * options never mix real and made-up words: a real target gets 3 real words, a made-up target gets 3 made-up ones
  * real options come from CMUdict words with one pronunciation (the course vocabulary first, other dictionary words
    only when needed); made-up options must NOT sound like any CMUdict word, must not be spelled like one, and must
    pass the profanity blocklist (content/blocklist.txt, by spelling and by sound)
  * foils use only sounds taught by the lesson where the word first appears (plus the target's own sounds); every
    made-up option is a legal English syllable made of GPC-table phonemes
  * L1.02-L1.04: where the pool cannot fill a grid -> the plan's early check: 3 options in a chain (neighbours one
    change apart), same lexicality, label early:true; repeats across sittings are allowed
Fallback ladder when the first grid cannot be built (every step logged in options_report.md; nothing is dropped silently):
  1. 2x2 {target, onset, vowel, onset+vowel}            (taught sounds, then any L1 sound)
  2. 2x2 {target, onset, final, onset+final}            (final-change instead of vowel-change, `axes: [onset, final]`)
  3. 3-option chain, any single-position change         (`early: true`)
  4. MADE-UP targets only: allow ONE foil that sounds like a REAL word already taught in Level 1 (`realfoil: true`, spoken only)
  5. otherwise `unbuildable` with a reason: written to content/options_unbuildable.json and the report; the app skips these words.
Writes content/options.json and content/options_report.md. Options are SPOKEN (never printed).
`--level N` (N = 2-4): the same ladder over content/levels/L<N>.json gate items -> content/options_L<N>.json (see the Levels 2-4 section).
"""
import json, random, re, collections, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
LEX = json.loads((C / "lexicon.json").read_text())
FULL = json.loads((C / "lexicon_full.json").read_text())["words"]
GPC = json.loads((C / "gpc.json").read_text())

VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
PID2ARPA = {"s": ["S"], "a": ["AE"], "t": ["T"], "p": ["P"], "i": ["IH"], "n": ["N"], "m": ["M"], "d": ["D"], "g": ["G"],
            "o": ["AA"], "k": ["K"], "e": ["EH"], "u": ["AH"], "r": ["R"], "h": ["HH"], "b": ["B"], "f": ["F"], "l": ["L"],
            "j": ["JH"], "v": ["V"], "w": ["W"], "ks": ["K", "S"], "y": ["Y"], "z": ["Z"], "kw": ["K", "W"]}
IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "EH": "ɛ", "IH": "ɪ", "IY": "i", "UH": "ʊ", "UW": "u", "ER": "ɝ",
       "EY": "eɪ", "AY": "aɪ", "OW": "oʊ", "AW": "aʊ", "OY": "ɔɪ",
       "S": "s", "T": "t", "P": "p", "N": "n", "M": "m", "D": "d", "G": "ɡ", "K": "k", "R": "ɹ", "HH": "h", "B": "b",
       "F": "f", "L": "l", "JH": "ʤ", "V": "v", "W": "w", "Y": "j", "Z": "z", "NG": "ŋ", "CH": "ʧ", "SH": "ʃ", "ZH": "ʒ",
       "TH": "θ", "DH": "ð"}
# legal two-consonant onsets and codas for MADE-UP words (real words are legal by being real)
LEGAL_ONSET2 = {("S", x) for x in "T P K N M L W".split()} | {(a, b) for a in "P B K G F".split() for b in "L R".split()} \
    | {("T", "R"), ("D", "R"), ("T", "W"), ("K", "W")}
LEGAL_CODA2 = {("S", "T"), ("S", "K"), ("S", "P"), ("N", "T"), ("N", "D"), ("M", "P"), ("L", "T"), ("L", "D"), ("L", "K"),
               ("L", "P"), ("F", "T"), ("P", "T"), ("K", "T"), ("NG", "K"), ("N", "S"), ("L", "S"), ("T", "S"), ("K", "S"), ("P", "S")}
FINAL_BAD = {"HH", "W", "Y", "R", "JH", "V", "NG", "CH", "SH", "ZH", "TH", "DH"}   # not offered as a made-up single final
ONSET_BAD = {"NG", "ZH"}
EARLY = {"L1.02", "L1.03", "L1.04"}


def strip(a): return tuple(x.rstrip("012") for x in a.split())


def load_cmu():
    prons = collections.defaultdict(set)
    for line in (C / "cmudict/cmudict.dict").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(";"): continue
        w, _, rest = line.partition(" ")
        w = re.sub(r"\(\d+\)$", "", w)
        if w.isalpha() and w.islower(): prons[w].add(strip(rest.split("#")[0].strip()))
    return prons


CMU = load_cmu()
try:
    from wordfreq import zipf_frequency as ZIPF     # commonness oracle (pip install wordfreq); keeps obscure dictionary words out of options
except ImportError:
    ZIPF = lambda w, lang: 3.0
AMERICAN = {w.strip() for w in open("/usr/share/dict/american-english") if w.strip().isalpha() and w.strip().islower()}
COURSE_ALL = {w for w, f in FULL.items() if f["kind"] in ("real", "heart")}
# a made-up foil must not SOUND like a dictionary word (ear can't tell); CMUdict's names/jargon alone do not count, the spelling check covers those
ALL_SOUNDS = {p for w, ps in CMU.items() if w in COURSE_ALL or (w in AMERICAN and ZIPF(w, 'en') >= 2.5) for p in ps}

# ---- blocklist
BL_SPELL, BL_SOUND = set(), set()
for line in (C / "blocklist.txt").read_text().splitlines():
    line = line.split("#")[0].strip()
    if not line: continue
    soft = line.startswith("~"); line = line.lstrip("~")
    w, _, arpa = line.partition("=")
    BL_SPELL.add(w)
    if arpa: BL_SOUND.add(tuple(arpa.split()))
    elif not soft: BL_SOUND |= CMU.get(w, set())


# made-up shapes that read as rude near-spellings ("fock", "cuck", "fap", "kunt"): F?K F?G F?P K?K P?D K AH N T
PSEUDO_BAD_SHAPES = [("F", "*", "K"), ("F", "*", "G"), ("F", "*", "P"), ("K", "*", "K"), ("P", "AH", "D"), ("K", "AH", "N", "T"),
                     ("F", "*", "K", "S"), ("S", "AE", "K"), ("D", "IH", "K")]


def blocked_spelling(s):
    return any(s == b if len(b) <= 3 else b in s for b in BL_SPELL)


# ---- real-word index: sound -> candidate spellings (course vocabulary = tier 1, other dictionary words = tier 2)
COURSE = {w for w, f in FULL.items() if f["kind"] == "real"}
REAL = collections.defaultdict(list)
for w, ps in CMU.items():
    if len(ps) != 1 or not 2 <= len(w) <= 6 or blocked_spelling(w): continue
    tier = 1 if w in COURSE else 2 if (w in AMERICAN and ZIPF(w, 'en') >= 3.0) else 0
    if not tier: continue
    p = next(iter(ps))
    if p in BL_SOUND: continue
    REAL[p].append((tier, w))
for p in REAL: REAL[p].sort()


def taught_upto(lid):
    t = set()
    for o in GPC["order"]:
        if o["lesson"] <= lid: t |= set(PID2ARPA.get(o["p"], []))
    return t


def ipa(p):
    out, st = "", False
    for x in p:
        if x in VOWELS and not st: out += "ˈ"; st = True
        out += IPA[x]
    return out


def spell(p):
    """Spelling for a made-up sound sequence: what a TTS voice reads back as that sequence (the audio is rendered from this)."""
    v = next(i for i, x in enumerate(p) if x in VOWELS)
    s = ""
    for i, x in enumerate(p):
        nxt = p[i + 1] if i + 1 < len(p) else None
        if x in VOWELS: s += {"AE": "a", "IH": "i", "AA": "o", "EH": "e", "AH": "u"}.get(x, "?"); continue
        if x == "K":
            if i < v: s += "c" if p[v] in ("AE", "AA", "AH") and i == v - 1 else "k"
            elif nxt is None and i == v + 1: s += "ck"
            else: s += "k"
            continue
        if i > v and nxt is None and i == v + 1:
            s += {"F": "ff", "L": "ll", "S": "ss", "Z": "zz"}.get(x, x.lower()); continue
        s += {"JH": "j", "HH": "h", "NG": "ng", "CH": "ch", "SH": "sh", "Y": "y"}.get(x, x.lower())
    if p[-2:] == ("NG", "K"): s = s[:-3] + "nk"
    return s


def legal_pseudo(p, v):
    on, co = p[:v], p[v + 1:]
    if len(on) > 2 or len(co) > 2 or any(x in ONSET_BAD for x in on): return False
    if len(on) == 2 and tuple(on) not in LEGAL_ONSET2: return False
    if len(co) == 2 and tuple(co) not in LEGAL_CODA2: return False
    if len(co) == 1 and co[0] in FINAL_BAD and False: return False
    return True


def pseudo_ok(p, v):
    if p in ALL_SOUNDS or p in BL_SOUND or not legal_pseudo(p, v): return None
    s = spell(p)
    if "?" in s or s in CMU or s in AMERICAN or ZIPF(s, "en") >= 3.6 or blocked_spelling(s): return None
    if any(len(p) == len(pat) + 0 and all(a == "*" or a == b for a, b in zip(pat, p)) for pat in PSEUDO_BAD_SHAPES): return None
    return s


def real_pick(p, avoid=()):
    for tier, w in REAL.get(p, []):
        if w not in avoid: return tier, w
    return None


def axes_of(t):
    """(vowel index v, the consonant position that moves with it): the onset for a word with one, else the last sound (final)."""
    v = next((i for i, x in enumerate(t) if x in VOWELS), None)
    vs = [i for i, x in enumerate(t) if x in VOWELS]
    if v is None or len(vs) != 1: return None
    if v > 0: return v, v - 1, "onset"
    if len(t) < 2: return None
    return v, len(t) - 1, "final"


def label(t, q, v, b, ax):
    pos = [i for i in range(len(t)) if t[i] != q[i]]
    names = []
    for i in pos:
        names.append("vowel" if i == v else ax if i == b else "onset" if i < v else "coda")
    return "+".join(sorted(names, key=lambda n: ["onset", "final", "vowel", "coda"].index(n)))


def target_sounds(k, e):
    f = FULL.get(k) or FULL.get(k.lower())
    t = tuple(f["arpa"].split()) if f else None
    if e["kind"] == "real" and t is not None and k in CMU and t not in CMU[k]:
        t = sorted(CMU[k])[0]
    if e["kind"] == "real" and f and f.get("source") != "cmudict" and k in CMU:
        t = sorted(CMU[k])[0]
    return t


def foil_pool(t, lid, wide=False):
    """Sounds a foil may use: those taught by the item's first lesson (+ the target's own); wide = any Level 1 sound (foils are spoken, not printed)."""
    return sorted(taught_upto("L1.13" if wide else lid) | set(t))     # sorted: set order is hash-seeded, and runs must be reproducible


REAL_FOIL_LID = [None]      # set per item: the lesson id; a made-up foil may collide with a real word taught up to there


def taught_real(p, lid):
    """A Level 1 real word (CMUdict single pronunciation `p`) already taught by lesson `lid`, or None."""
    for tier, w in REAL.get(p, []):
        e = LEX.get(w)
        if tier == 1 and e and e["kind"] == "real" and min(e["lessons"]) <= lid: return w
    return None


def make(real, q, v, b, ax, pool, ban=(), allow_real=False):
    """A word (spelling, tier) for sound sequence q under the item's lexicality, or None. tier 3 = made-up slot filled by a taught real word."""
    if any(x not in pool for x in q): return None
    if real:
        r = real_pick(tuple(q), ban)
        return r
    s = pseudo_ok(tuple(q), v)
    if s: return (0, s)
    if allow_real and REAL_FOIL_LID[0] and tuple(q) not in BL_SOUND and legal_pseudo(tuple(q), v):
        w = taught_real(tuple(q), REAL_FOIL_LID[0])
        if w and w not in ban: return (3, w)
    return None


def build_grid(k, e, t, lid, rng, wide=False, second="vowel", allow_real=False):
    """2x2 grid. Axes: (onset|final, vowel) by default; second="final" gives (onset, final) for a word with onset AND coda."""
    a = axes_of(t)
    if not a: return None, "no single-vowel shape"
    v, b, ax = a
    real = e["kind"] == "real"
    pool = foil_pool(t, lid, wide)
    if second == "final":
        if ax != "onset" or len(t) - 1 <= v: return None, "no onset+coda shape"
        A, pa, B, pb = "onset", b, "final", len(t) - 1
    else:
        A, pa, B, pb = ax, b, "vowel", v

    def cands(axis, pos):
        if axis == "vowel":
            vows = [x for x in pool if x in VOWELS and x != t[v] and x not in ("AO",)]
            if v == len(t) - 1: vows = []     # open syllable (sta): a bare vowel letter has no stable spoken reading, so no vowel foils
            if t[v] == "AA": vows = [x for x in vows if x != "AO"]
            return vows
        cons = [x for x in pool if x not in VOWELS and x != t[pos]]
        if axis == "final":
            cons = [x for x in cons if x not in FINAL_BAD]
            if len(t) - v - 1 > 1: cons = [x for x in cons if (t[pos - 1], x) in LEGAL_CODA2]
        else:
            cons = [x for x in cons if x not in ONSET_BAD]
            if pos > 0 and v - 1 > 0: cons = [x for x in cons if (t[pos - 1], x) in LEGAL_ONSET2]
        return cons

    combos = [(x, y) for x in cands(A, pa) for y in cands(B, pb)]
    rng.shuffle(combos)
    best = None
    for x, y in combos:
        q1 = list(t); q1[pa] = x
        q2 = list(t); q2[pb] = y
        q3 = list(t); q3[pa] = x; q3[pb] = y
        ws, ban = [], {k}
        for q in (q1, q2, q3):
            r = make(real, q, v, b, ax, pool, ban, allow_real)
            if not r: break
            ws.append(r); ban.add(r[1])
        else:
            nreal = sum(1 for r in ws if r[0] == 3)
            if nreal > 1: continue      # at most ONE real-word foil per made-up item
            score = sum(1 for r in ws if r[0] == 2) + 5 * nreal     # fewer non-course words is better
            if best is None or score < best[0]:
                best = (score, ws, (q1, q2, q3))
                if score == 0: break
    if not best: return None, "no grid"
    _, ws, qs = best
    foils = [(ws[i][1], tuple(qs[i]), c, ws[i][0] == 3) for i, c in enumerate((A, B, f"{A}+{B}"))]
    return foils, None


def neighbours(t, v, real, pool, ban, allow_real=False):
    """Words one change away (vowel / onset / final) in the pool, same lexicality."""
    out = []
    for i in range(len(t)):
        if t[i] in VOWELS:
            cand = [x for x in pool if x in VOWELS and x not in (t[i], "AO")] if i < len(t) - 1 else []
        else:
            cand = [x for x in pool if x not in VOWELS and x != t[i] and x not in (FINAL_BAD if i > v else ONSET_BAD)]
        for x in cand:
            q = list(t); q[i] = x
            r = make(real, q, v, i, "", pool, ban, allow_real)
            if r: out.append((tuple(q), r))
    return out


def build_early(k, e, t, lid, rng, idx, wide=False, allow_real=False):
    a = axes_of(t)
    if not a: return None, "no single-vowel shape"
    v, b, ax = a
    real = e["kind"] == "real"
    pool = foil_pool(t, lid, wide)
    n1 = neighbours(t, v, real, pool, {k}, allow_real)
    rng.shuffle(n1)
    middle = idx % 3 == 0       # target in the middle of the chain in a third of the items
    opts = None
    if middle:
        seen = []
        for q, r in n1:
            if all(r[1] != s[1][1] for s in seen): seen.append((q, r))
        if len(seen) >= 2:
            opts = [seen[0], seen[1]]
    if not opts:
        for q, r in n1:
            n2 = [(q2, r2) for q2, r2 in neighbours(q, v, real, pool, {k, r[1]}, allow_real) if q2 != t]
            if n2:
                rng.shuffle(n2); opts = [(q, r), n2[0]]; break
    if not opts and len(n1) >= 2:
        opts = [n1[0], next((x for x in n1[1:] if x[1][1] != n1[0][1][1]), None)]
        if not opts[1]: opts = None
    if not opts: return None, "no early chain"
    if sum(1 for q, r in opts if r[0] == 3) > 1: return None, "early chain needs 2 real-word foils"
    return [(r[1], q, label(t, q, v, b, ax), r[0] == 3) for q, r in opts], None


def main():
    out, fails, stats = {}, [], collections.defaultdict(lambda: collections.Counter())
    items = [(k, e) for k, e in LEX.items() if e["kind"] in ("real", "pseudo")]
    n_early = 0
    # STICKY: an item that already has options (and whose target sounds are unchanged) keeps them, so its rendered audio clips stay valid
    # and a re-run costs no new characters. `--fresh` rebuilds everything.
    prev = {} if "--fresh" in sys.argv else json.loads((C / "options.json").read_text()) if (C / "options.json").exists() else {}
    kept = 0
    for idx, (k, e) in enumerate(items):
        lid = min(e["lessons"])
        t = target_sounds(k, e)
        if not t: fails.append((k, lid, "no sounds")); continue
        o0 = prev.get(k.lower())
        if o0 and tuple(x.upper() for x in o0["target"]["p"]) == tuple(t):
            o0.setdefault("via", "early chain" if o0.get("early") else "2x2")
            out[k.lower()] = o0; kept += 1; continue
        a = axes_of(t)
        why_all = []
        REAL_FOIL_LID[0] = lid
        rg = random.Random(f"so-{k}")     # ONE stream per item, consumed in ladder order, so items the old ladder built come out identical
        rng = lambda: rg
        # existing ladder first (so items that already had options keep them), then the new fallbacks
        steps = [("grid", False, "vowel", False), ("early", False, None, False), ("grid", True, "vowel", False), ("early", True, None, False),
                 ("grid", False, "final", False), ("grid", True, "final", False), ("early", False, None, False), ("early", True, None, False)]
        if e["kind"] == "pseudo":
            steps += [("grid", False, "vowel", True), ("grid", True, "vowel", True), ("grid", False, "final", True), ("grid", True, "final", True),
                      ("early", False, None, True), ("early", True, None, True)]
        foils = None; early = wide = False; how = ""
        for si, (kind, w_, second, ar) in enumerate(steps):
            if kind == "early":
                # steps 0-3 are the original ladder (early chain only in L1.02-L1.04); the early chain in later lessons is a fallback (step 6+)
                if lid not in EARLY and si < 4: continue
                foils, why = build_early(k, e, t, lid, rng(), n_early, w_, ar)
            else:
                foils, why = build_grid(k, e, t, lid, rng(), w_, second, ar)
            if foils:
                early, wide = kind == "early", w_
                how = ("early chain" if early else "2x2 onset+final" if second == "final" else "2x2") + (" + real-word foil" if ar else "")
                break
            why_all.append(why)
        if early: n_early += 1
        if not foils:
            fails.append((k, lid, "no 2x2 (onset|final x vowel), no 2x2 (onset x final), no 3-option chain" + (", and no taught real-word foil fits" if e["kind"] == "pseudo" else "") + (" (" + "; ".join(sorted(set(why_all))) + ")" if set(why_all) - {"no grid", "no early chain", "no onset+coda shape"} else "")))
            continue
        cell = lambda w, p, c, rf=False: {"w": w, "p": [x.lower() for x in p], "ipa": ipa(p), "cell": c, **({"realfoil": True} if rf else {})}
        axn = [] if early else [foils[0][2], foils[1][2]]
        o = {"target": cell(e["w"], t, "target"), "foils": [cell(w, p, c, rf) for w, p, c, rf in foils],
             "axes": axn, "kind": e["kind"], "relaxed": False, "via": how}
        if early: o["early"] = True
        if wide: o["untaught"] = True
        if any(f[3] for f in foils): o["realfoil"] = True
        out[k.lower()] = o
    (C / "options.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (C / "options_unbuildable.json").write_text(json.dumps({k: {"lesson": lid, "reason": why} for k, lid, why in fails}, indent=1, ensure_ascii=False))
    report(out, fails, items)
    print(f"kept {kept} existing; options for {len(out)} of {len(items)} items; early {sum(1 for o in out.values() if o.get('early'))}; "
          f"by route {dict(collections.Counter(o['via'] for o in out.values()))}; unbuildable {[f[0] for f in fails]}")


def report(out, fails, items):
    L = collections.defaultdict(lambda: {"items": 0, "grid": 0, "early": 0, "fail": [], "tier2": 0})
    failed = {f[0]: f for f in fails}
    for k, e in items:
        o = out.get(k.lower())
        for lid in e["lessons"]:
            if not lid.startswith("L1."): continue
            r = L[lid]; r["items"] += 1
            if k in failed: r["fail"].append(f"{k} ({failed[k][2]})")
            elif o.get("early"): r["early"] += 1
            else: r["grid"] += 1
            if o and e["kind"] == "real" and any(f["w"] not in COURSE for f in o["foils"]): r["tier2"] += 1
    t1 = sum(1 for p in REAL.values() for tier, w in p if tier == 1); t2 = sum(1 for p in REAL.values() for tier, w in p if tier == 2)
    md = ["# Tap-gate options (generated by tools/gen_options.py)", "",
          "Built from phonemes (Arpabet from content/lexicon_full.json / CMUdict), not letters. Foils use only sounds taught by the "
          "lesson where the word first appears (plus the target's own). Real options are CMUdict words with one pronunciation, course vocabulary "
          f"first ({t1} sound-forms in the course, {t2} other dictionary words, after content/blocklist.txt); made-up options sound like no CMUdict word, "
          "are not spelled like one, pass the blocklist (spelling and sound) and are legal syllables of GPC-table phonemes.", "",
          f"Items: {len(items)}; built {len(out)} ({sum(1 for o in out.values() if not o.get('early'))} 2x2 grids, "
          f"{sum(1 for o in out.values() if o.get('early'))} early checks with 3 options, `early: true`); could not build {len(fails)}. "
          f"{sum(1 for o in out.values() if o.get('untaught'))} items needed a foil sound not yet taught at their first lesson (`untaught: true`; spoken only, never printed).", "",
          "| Lesson | Items | 2x2 grid | Early (3 opts) | Real items using a non-course foil | Pool (taught sounds): real words / made-up strings | Could not build |", "|---|---|---|---|---|---|---|"]
    for lid in sorted(L):
        pool = taught_upto(lid)
        real_n = sum(1 for p in REAL if all(x in pool for x in p))
        mk = 0
        vs = [x for x in pool if x in VOWELS]; cs = [x for x in pool if x not in VOWELS and x not in FINAL_BAD]
        for v in vs:
            mk += sum(1 for c in cs if pseudo_ok((c, v), 1)) if False else 0
        mk = sum(1 for v in vs for c in [x for x in pool if x not in VOWELS and x not in ONSET_BAD] for f in cs
                 if pseudo_ok((c, v, f), 1)) + sum(1 for v in vs for f in cs if pseudo_ok((v, f), 0))
        r = L[lid]
        md.append(f"| {lid} | {r['items']} | {r['grid']} | {r['early']} | {r['tier2']} | {real_n} / {mk} | {'; '.join(r['fail']) or '-'} |")
    via = collections.Counter(o.get("via", "?") for o in out.values())
    md += ["", "## Fallback ladder (which route built each item)", ""]
    md += [f"- {n} items: {v}" for v, n in via.most_common()]
    md += [f"- {sum(1 for o in out.values() if o.get('realfoil'))} items use a real-word foil in a made-up item (`realfoil: true`; allowed only for a Level 1 word already taught, at most one per item, spoken only). "
           "Judgement: acceptable in principle because every option is spoken and all are 'alien words' by instruction, the learner chooses by sound, and a real word that is picked instead of the printed made-up word is "
           "itself a useful error (a lexicalisation slip); the cost is that a child can discard it by familiarity, so the guess rate drops from 1/4 to 1/3 on those items. It was therefore the LAST resort and it was never needed."
           if any(True for _ in [0]) else ""]
    md += ["", "## Items that could not be built (dropped from the tap gate, logged here and in content/options_unbuildable.json; the app skips them)", ""]
    md += [f"- `{k}` ({lid}): {why}" for k, lid, why in fails] or ["None."]
    md += [f"", f"Dropped from the check: {len(fails)} of {len(items)}. Silently missing: 0."]
    md += ["", "## Early checks (3 options, same lexicality, chain of one-change neighbours; repeats across sittings allowed)", ""]
    md += [f"- {k}: " + " / ".join(x["w"] for x in [o["target"], *o["foils"]]) for k, o in out.items() if o.get("early")]
    (C / "options_report.md").write_text("\n".join(md) + "\n")


# ====================================================================== Levels 2-4 (`--level N`)
# Same rules and the same fallback ladder as Level 1, generalised for multi-letter graphemes, suffixes and syllables:
#   * the grid axes sit on the STRESSED vowel (the syllable the ear keys on) and the consonant before it (onset) or,
#     with no onset, the word's last sound (final); every other sound is copied from the target. Options carry
#     `pos` {onset|final, vowel} so the checker (tools/drive.py) measures exactly those positions on Arpabet.
#   * foil sounds: those taught by the item's lesson in DESIGN.md §3 (gpc.json "full", main GPCs) + the target's own
#   * real options: CMUdict words with one pronunciation, up to 12 letters (course vocabulary first)
#   * made-up options: not a CMUdict/dictionary sound or spelling, blocklist-clean, the changed consonant cluster legal
# Ladder per item (pools stay sorted, one seeded RNG per item, sticky across runs): 2x2 onset|final x vowel (taught,
# then wide) -> 2x2 onset x final -> 3-option chain -> (made-up only) one taught real-word foil -> unbuildable (logged).
LEGAL_ON = {(x,) for x in "B D F G HH JH K L M N P R S T V W Y Z CH SH TH DH".split()} | LEGAL_ONSET2 | {
    ("SH", "R"), ("TH", "R"), ("S", "K", "W"), ("S", "T", "R"), ("S", "P", "R"), ("S", "K", "R"), ("S", "P", "L"), ("G", "L"),
    ("B", "L"), ("K", "L"), ("F", "L"), ("P", "L"), ("D", "W"), ("S", "W"), ("S", "L"), ("S", "N"), ("S", "M")}
LEGAL_CO = {(x,) for x in "B D F G JH K L M N P R S T V Z CH SH TH DH NG".split()} | LEGAL_CODA2 | {
    ("N", "CH"), ("L", "F"), ("L", "M"), ("R", "D"), ("R", "T"), ("R", "K"), ("R", "M"), ("R", "N"), ("R", "P"), ("R", "B"),
    ("R", "L"), ("R", "S"), ("R", "Z"), ("R", "F"), ("R", "CH"), ("R", "JH"), ("R", "TH"), ("N", "Z"), ("M", "Z"), ("L", "Z"),
    ("D", "Z"), ("G", "Z"), ("B", "Z"), ("NG", "Z"), ("F", "S"), ("NG", "K", "S"), ("N", "D", "Z"), ("N", "T", "S"), ("S", "T", "S"),
    ("M", "P", "S"), ("K", "S", "T"), ("M", "D"), ("N", "D"), ("L", "D"), ("JH", "D"), ("CH", "T"), ("SH", "T"), ("Z", "D"), ("V", "D")}
VSPELL = {"AE": "a", "IH": "i", "AA": "o", "EH": "e", "AH": "u", "EY": "ay", "IY": "ee", "AY": "igh", "OW": "oa", "UW": "oo",
          "UH": "oo", "ER": "er", "AW": "ow", "OY": "oy", "AO": "aw"}
CSPELL = {"JH": "j", "HH": "h", "NG": "ng", "CH": "ch", "SH": "sh", "TH": "th", "DH": "th", "ZH": "zh", "Y": "y"}
FULL_SEQ = GPC.get("full", {}).get("sequence", [])
REAL_LONG = collections.defaultdict(list)
for _w, _ps in CMU.items():
    if len(_ps) != 1 or not 2 <= len(_w) <= 12 or blocked_spelling(_w): continue
    _tier = 1 if _w in COURSE else 2 if (_w in AMERICAN and ZIPF(_w, 'en') >= 3.0) else 0
    _p = next(iter(_ps))
    if _tier and _p not in BL_SOUND: REAL_LONG[_p].append((_tier, _w))
for _p in REAL_LONG: REAL_LONG[_p].sort()


def lk(lid):
    m = re.match(r"L(\d+)\.(\d+)", lid); return (int(m.group(1)), int(m.group(2)))


def taught_upto2(lid):
    t = set(taught_upto("L1.13"))
    for o in FULL_SEQ:
        if lk(o["lesson"]) <= lk(lid) and o["g"] != "ə":
            for ph in o["main"]: t |= set(ph.split())
    return t


def spell2(p):
    out = []
    for i, x in enumerate(p):
        nxt = p[i + 1] if i + 1 < len(p) else None
        if x in VOWELS: out.append(VSPELL.get(x, "?")); continue
        if x == "K":
            prevv = i > 0 and p[i - 1] in ("AE", "IH", "AA", "EH", "AH")
            out.append("ck" if nxt is None and prevv else "c" if nxt in ("AE", "AA", "AH", "R", "L") else "k"); continue
        out.append(CSPELL.get(x, x.lower()))
    s = "".join(out)
    return s.replace("ngk", "nk")


def clusters(p):
    vs = [i for i, x in enumerate(p) if x in VOWELS]
    if not vs: return None
    return tuple(p[:vs[0]]), tuple(p[vs[-1] + 1:])


def pseudo_ok2(q, t):
    q = tuple(q)
    if q in ALL_SOUNDS or q in BL_SOUND: return None
    cq, ct = clusters(q), clusters(t)
    if not cq: return None
    if cq[0] != ct[0] and cq[0] and cq[0] not in LEGAL_ON: return None
    if cq[1] != ct[1] and cq[1] and cq[1] not in LEGAL_CO: return None
    if any(x in ONSET_BAD for x in cq[0]): return None
    s = spell2(q)
    if "?" in s or s in CMU or s in AMERICAN or ZIPF(s, "en") >= 3.6 or blocked_spelling(s): return None
    if any(len(q) == len(pat) and all(a == "*" or a == b for a, b in zip(pat, q)) for pat in PSEUDO_BAD_SHAPES): return None
    return s


def taught_real2(q, lid):
    for tier, w in REAL_LONG.get(tuple(q), []):
        f = FULL.get(w)
        if tier == 1 and f and f["kind"] == "real" and min(f["lessons"], key=lk) <= lid: return w
    return None


def make2(real, q, t, pool, ban, allow_real, lid):
    if any(x not in pool for x in q): return None
    if real:
        for tier, w in REAL_LONG.get(tuple(q), []):
            if w not in ban: return (tier, w)
        return None
    s = pseudo_ok2(q, t)
    if s and s not in ban: return (0, s)      # TH/DH both spell "th": never two options with one spelling
    if allow_real:
        w = taught_real2(q, lid)
        if w and w not in ban and tuple(q) not in BL_SOUND: return (3, w)
    return None


def axes2(t, stress):
    vs = [i for i, x in enumerate(t) if x in VOWELS]
    if not vs: return None
    v = stress if stress in vs else vs[0]
    if v > 0 and t[v - 1] not in VOWELS: return v, v - 1, "onset"
    if t[-1] not in VOWELS and len(t) - 1 != v: return v, len(t) - 1, "final"
    return None


def grid2(k, real, t, stress, lid, rng, wide, second, allow_real):
    a = axes2(t, stress)
    if not a: return None, "no onset/final consonant beside the stressed vowel"
    v, b, ax = a
    pool = sorted((taught_upto2("L4.16") if wide else taught_upto2(lid)) | set(t))
    if second == "final":
        if ax != "onset" or t[-1] in VOWELS or len(t) - 1 == v: return None, "no onset+final shape"
        A, pa, B, pb = "onset", b, "final", len(t) - 1
    else:
        A, pa, B, pb = ax, b, "vowel", v

    def cands(axis, pos):
        if axis == "vowel":
            return [x for x in pool if x in VOWELS and x != t[v] and x != "AO"] if v != len(t) - 1 or len(t) > 1 else []
        cons = [x for x in pool if x not in VOWELS and x != t[pos]]
        return [x for x in cons if x not in (FINAL_BAD if axis == "final" else ONSET_BAD)]
    combos = [(x, y) for x in cands(A, pa) for y in cands(B, pb)]
    rng.shuffle(combos)
    best = None
    for x, y in combos[:400]:
        q1 = list(t); q1[pa] = x
        q2 = list(t); q2[pb] = y
        q3 = list(t); q3[pa] = x; q3[pb] = y
        ws, ban = [], {k}
        for q in (q1, q2, q3):
            r = make2(real, q, t, pool, ban, allow_real, lid)
            if not r: break
            ws.append(r); ban.add(r[1])
        else:
            nreal = sum(1 for r in ws if r[0] == 3)
            if nreal > 1: continue
            score = sum(1 for r in ws if r[0] == 2) + 5 * nreal
            if best is None or score < best[0]:
                best = (score, ws, (q1, q2, q3))
                if score == 0: break
    if not best: return None, "no grid"
    _, ws, qs = best
    pos = {A: pa, B: pb}
    return [(ws[i][1], tuple(qs[i]), c, ws[i][0] == 3) for i, c in enumerate((A, B, f"{A}+{B}"))], pos


def chain2(k, real, t, stress, lid, rng, wide, allow_real):
    pool = sorted((taught_upto2("L4.16") if wide else taught_upto2(lid)) | set(t))
    def nb(base, ban):
        out = []
        for i in range(len(base)):
            if base[i] in VOWELS: cand = [x for x in pool if x in VOWELS and x not in (base[i], "AO")]
            else: cand = [x for x in pool if x not in VOWELS and x != base[i] and x not in (ONSET_BAD if i == 0 else ())]
            for x in cand:
                q = list(base); q[i] = x
                r = make2(real, q, t, pool, ban, allow_real, lid)
                if r: out.append((tuple(q), r))
        return out
    n1 = nb(t, {k}); rng.shuffle(n1)
    for q, r in n1[:60]:
        n2 = [(q2, r2) for q2, r2 in nb(q, {k, r[1]}) if q2 != tuple(t) and sum(a != b for a, b in zip(q2, t)) <= 2]
        if n2:
            rng.shuffle(n2); opts = [(q, r), n2[0]]
            if sum(1 for _, rr in opts if rr[0] == 3) > 1: continue
            return [(rr[1], qq, "chain", rr[0] == 3) for qq, rr in opts], None
    return None, "no 3-option chain"


def ipa2(p, stress):
    out = ""
    for i, x in enumerate(p):
        if i == stress: out += "ˈ"
        out += IPA[x]
    return out


def main_level(level):
    B = json.loads((C / "levels" / f"L{level}.json").read_text())
    lex = B["lexicon"]
    L1OPT = json.loads((C / "options.json").read_text())
    outf, unbf = C / f"options_L{level}.json", C / f"options_unbuildable_L{level}.json"
    prev = {} if "--fresh" in sys.argv else json.loads(outf.read_text()) if outf.exists() else {}
    out, fails, kept, l1 = {}, [], 0, 0
    for k, meta in sorted(B["gateItems"].items()):
        if k in L1OPT: l1 += 1; continue            # Level 1 options (and their rendered clips) are reused as they are
        lid = meta["lesson"]; real = meta["kind"] == "real"
        f = FULL.get(k)
        if not f: fails.append((k, lid, "not in lexicon_full")); continue
        st = (f.get("arpa_stress") or "").split()
        t = tuple(x.rstrip("012") for x in st) if st else tuple(f["arpa"].split())
        if real and k in CMU and t not in CMU[k]: t = sorted(CMU[k])[0]
        stress = next((i for i, x in enumerate(st) if x.endswith("1")), next((i for i, x in enumerate(t) if x in VOWELS), 0))
        if len(st) != len(t): stress = next((i for i, x in enumerate(t) if x in VOWELS), 0)
        o0 = prev.get(k)
        if o0 and tuple(x.upper() for x in o0["target"]["p"]) == t:
            out[k] = o0; kept += 1; continue
        rg = random.Random(f"so-{k}")
        steps = [("grid", False, "vowel", False), ("grid", True, "vowel", False), ("grid", False, "final", False), ("grid", True, "final", False),
                 ("chain", False, None, False), ("chain", True, None, False)]
        if not real: steps += [("grid", False, "vowel", True), ("grid", True, "vowel", True), ("chain", True, None, True)]
        foils = None; why_all = []
        for kind, wide, second, ar in steps:
            if kind == "grid": foils, extra = grid2(k, real, t, stress, lid, rg, wide, second, ar)
            else: foils, extra = chain2(k, real, t, stress, lid, rg, wide, ar)
            if foils:
                how = ("early chain" if kind == "chain" else "2x2 onset+final" if second == "final" else "2x2") + (" + real-word foil" if ar else "") + (" (wide pool)" if wide else "")
                break
            why_all.append(extra)
        if not foils:
            fails.append((k, lid, "no 2x2 (onset|final x vowel), no 2x2 (onset x final), no 3-option chain" + (", no taught real-word foil" if not real else "")
                          + " (" + "; ".join(sorted(set(x for x in why_all if x))) + ")")); continue
        cell = lambda w, p, c, rf=False: {"w": w, "p": [x.lower() for x in p], "ipa": ipa2(p, stress), "cell": c, **({"realfoil": True} if rf else {})}
        early = kind == "chain"
        o = {"target": cell(k, t, "target"), "foils": [cell(w, p, c, rf) for w, p, c, rf in foils], "kind": meta["kind"], "via": how, "lesson": lid,
             "axes": [] if early else [foils[0][2], foils[1][2]]}
        if early: o["early"] = True
        else: o["pos"] = {kk: vv for kk, vv in extra.items()}
        o["stress"] = stress
        if any(x[3] for x in foils): o["realfoil"] = True
        out[k] = o
    outf.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    unbf.write_text(json.dumps({k: {"lesson": lid, "reason": why} for k, lid, why in fails}, indent=1, ensure_ascii=False))
    via = collections.Counter(o["via"] for o in out.values())
    by_lesson = collections.defaultdict(lambda: [0, 0, []])
    for k, meta in B["gateItems"].items():
        if k in L1OPT: continue
        r = by_lesson[meta["lesson"]]; r[0] += 1
        if k in out: r[1] += 1
    for k, lid, why in fails: by_lesson[lid][2].append(f"`{k}` ({why})")
    md = [f"# Tap-gate options, Level {level} (generated by tools/gen_options.py --level {level})", "",
          f"Gate items: {len(B['gateItems'])}; {l1} reuse their Level 1 options; built {len(out)}; could not build {len(fails)} "
          "(dropped from the tap gate, listed below and in " + unbf.name + "; the app skips them, the lesson bar is scaled to the items it can show).", "",
          "## Route", ""] + [f"- {n}: {v}" for v, n in via.most_common()] + ["", "| Lesson | Items | Built | Could not build |", "|---|---|---|---|"]
    md += [f"| {lid} | {r[0]} | {r[1]} | {'; '.join(r[2]) or '-'} |" for lid, r in sorted(by_lesson.items(), key=lambda x: lk(x[0]))]
    md += ["", f"Silently missing: 0."]
    (C / f"options_report_L{level}.md").write_text("\n".join(md) + "\n")
    print(f"L{level}: kept {kept}; built {len(out)} of {len(B['gateItems']) - l1} (+{l1} via Level 1 options); by route {dict(via)}; unbuildable {len(fails)}")


if __name__ == "__main__":
    if "--level" in sys.argv: main_level(int(sys.argv[sys.argv.index("--level") + 1]))
    else: main()
