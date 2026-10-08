#!/usr/bin/env python3
"""Full-course lexicon from CMUdict with grapheme<->phoneme alignment (decision 21).

  python3 tools/build_lexicon.py

Reads content/lessons/*.json (all 108 lessons, Levels 1-7), content/lexicon.json + content/options.json (Level 1
pseudowords and tap-gate foils) and content/cmudict/cmudict.dict (cmusphinx/cmudict, BSD-2, LICENSE alongside).
Writes:
  content/lexicon_full.json  word -> Arpabet (stress stripped; stressed form kept for the PLS), grapheme<->phoneme
                             alignment, status, levels/lessons, homograph senses
  content/gpc.json           adds "full": the DESIGN.md L1-L4 grapheme table in Arpabet (the existing Level 1
                             "order"/"phonemes"/"letterNames" keys are left exactly as they were: the app uses them)
  content/coverage.md        "## Full-course lexicon (CMUdict)" section, per level

Alignment: greedy longest-grapheme parse first (each grapheme takes the first of its GPC candidates that matches the
CMU phonemes at that point; the parse must consume the phonemes exactly). If greedy fails, a cost search over the same
table (main GPC = 0, listed alternate = 1, irregular vowel/silent letter = 2; fewer, longer graphemes preferred).
Status: gpc (all main), alt (alternates, no irregular step), irregular (needs an irregular step), unaligned (none).
Pseudowords: Arpabet composed from the GPC table deterministically (greedy parse, main candidate, plus the VCe,
open-syllable (Level >= 3), soft c/g (Level >= 3), final -y, consonant-le rules).
Homographs (read, live, wind ...): the sense the lesson context implies, by rule; every one is flagged "review".
"""
import collections, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
VOW = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}

# ------------------------------------------------------------------ GPC table, DESIGN.md §3 master sequence L1-L4
# grapheme: (main candidates [Arpabet strings], alternates, where taught). "" = silent.
T = {
    # Level 1 (1.2-1.12)
    "s": (["S", "Z"], ["ZH", "SH"], "L1.02"), "a": (["AE"], ["EH", "AA", "AO", "IH"], "L1.02"), "t": (["T"], ["CH", "SH"], "L1.02"),
    "p": (["P"], [], "L1.03"), "i": (["IH"], ["IY", "Y"], "L1.03"), "n": (["N"], ["NG"], "L1.03"), "m": (["M"], [], "L1.04"),
    "d": (["D"], ["JH", "T"], "L1.04"), "g": (["G"], ["ZH"], "L1.05"), "o": (["AA", "AO"], ["UW", "UH", "W AH", "IH"], "L1.05"),
    "c": (["K"], ["SH", "CH"], "L1.06"), "k": (["K"], [], "L1.06"), "ck": (["K"], [], "L1.06"), "e": (["EH"], ["EY", "IH"], "L1.07"),
    "u": (["AH"], ["UH", "IH", "EH", "W"], "L1.07"), "r": (["R"], [], "L1.08"), "h": (["HH"], [], "L1.08"), "b": (["B"], [], "L1.09"),
    "f": (["F"], ["V"], "L1.09"), "l": (["L"], [], "L1.09"), "ff": (["F"], [], "L1.10"), "ll": (["L"], [], "L1.10"),
    "ss": (["S"], ["SH", "Z"], "L1.10"), "zz": (["Z"], [], "L1.10"), "j": (["JH"], ["Y", "HH"], "L1.11"), "v": (["V"], [], "L1.11"),
    "w": (["W"], [], "L1.11"), "x": (["K S"], ["G Z", "Z", "K SH"], "L1.12"), "y": (["Y"], [], "L1.12"), "z": (["Z"], ["S"], "L1.12"),
    "qu": (["K W"], ["K"], "L1.12"),
    # Level 2
    "sh": (["SH"], [], "L2.01"), "ch": (["CH"], [], "L2.02"), "tch": (["CH"], [], "L2.02"), "th": (["TH", "DH"], ["T"], "L2.03"),
    "wh": (["W"], ["HH W", "HH"], "L2.04"), "ng": (["NG"], ["NG G", "N JH"], "L2.05"), "nk": (["NG K"], [], "L2.05"),
    "es": (["IH Z", "AH Z", "Z"], ["S"], "L2.09"), "ed": (["T", "D", "IH D", "AH D"], [], "L2.10"),
    "ing": (["IH NG"], [], "L2.11"), "er": (["ER"], ["EH R", "IH R"], "L2.11"),
    "bb": (["B"], [], "L2.12"), "dd": (["D"], [], "L2.12"), "gg": (["G"], [], "L2.12"), "mm": (["M"], [], "L2.12"),
    "nn": (["N"], [], "L2.12"), "pp": (["P"], [], "L2.12"), "rr": (["R"], [], "L2.12"), "tt": (["T"], [], "L2.12"),
    "cc": (["K", "K S"], [], "L2.12"),
    # Level 3
    "a_e": (["EY"], [], "L3.01"), "i_e": (["AY"], [], "L3.02"), "o_e": (["OW"], [], "L3.03"), "u_e": (["UW", "Y UW"], [], "L3.03"),
    "e_e": (["IY"], [], "L3.03"), "a.": (["EY"], [], "L3.05"), "e.": (["IY"], [], "L3.05"), "i.": (["AY"], [], "L3.05"),
    "o.": (["OW"], [], "L3.05"), "u.": (["UW", "Y UW"], [], "L3.05"), "y.": (["IY", "AY", "IH"], [], "L3.06"),
    "c.": (["S"], [], "L3.07"), "g.": (["JH"], [], "L3.07"), "ce": (["S"], [], "L3.07"), "ge": (["JH"], [], "L3.07"),
    "dge": (["JH"], [], "L3.07"), "ar": (["AA R"], ["ER", "EH R", "AO R"], "L3.08"), "or": (["AO R"], ["ER"], "L3.09"),
    "ore": (["AO R"], [], "L3.09"), "ai": (["EY"], ["EH"], "L3.10"), "ay": (["EY"], [], "L3.10"), "ee": (["IY"], ["IH"], "L3.11"),
    "ea": (["IY"], ["EY"], "L3.11"), "oa": (["OW"], [], "L3.12"), "ow": (["OW"], [], "L3.12"), "oe": (["OW"], ["UW"], "L3.12"),
    "igh": (["AY"], [], "L3.13"), "ie": (["AY", "IY"], ["EH"], "L3.13"), "ue": (["UW", "Y UW"], [], "L3.14"),
    "ew": (["UW", "Y UW"], [], "L3.14"), "ui": (["UW"], ["IH"], "L3.14"), "oo": (["UW", "UH"], ["AH"], "L3.15"),
    # Level 4
    "ir": (["ER"], [], "L4.03"), "ur": (["ER"], [], "L4.03"), "air": (["EH R"], [], "L4.04"), "are": (["EH R"], ["AA R"], "L4.04"),
    "ear": (["IH R", "EH R"], ["ER"], "L4.04"), "eer": (["IH R"], [], "L4.04"), "oi": (["OY"], [], "L4.05"), "oy": (["OY"], [], "L4.05"),
    "ou": (["AW"], ["UW", "AH", "OW", "AO", "UH"], "L4.06"), "ow.": (["AW"], [], "L4.06"), "aw": (["AO"], [], "L4.07"),
    "au": (["AO"], ["AA"], "L4.07"), "al": (["AO L"], ["AA", "AE L"], "L4.07"), "all": (["AO L"], [], "L4.07"),
    "ea.": (["EH"], [], "L4.08"), "kn": (["N"], [], "L4.08"), "wr": (["R"], [], "L4.08"), "gn": (["N"], [], "L4.08"),
    "mb": (["M"], [], "L4.08"), "ph": (["F"], [], "L4.09"), "ch.": (["K", "SH"], [], "L4.09"), "gh": (["F", "G", ""], [], "L4.09"),
    "le": (["AH L"], [], "L4.10"), "tion": (["SH AH N"], [], "L4.11"), "sion": (["SH AH N", "ZH AH N"], [], "L4.11"),
    "ture": (["CH ER"], [], "L4.11"), "ous": (["AH S"], [], "L4.11"), "cial": (["SH AH L"], [], "L4.11"),
    "tial": (["SH AH L"], [], "L4.11"), "ə": (["AH", "IH"], [], "L4.12"),
}
SCHWA_LETTERS = "aeiouy"           # L4.12: any vowel letter may reduce to schwa (AH) or IH in an unstressed syllable
LONG = {"a": "a_e", "e": "e_e", "i": "i_e", "o": "o_e", "u": "u_e"}
SILENT = set("hkwbtglspcndr")       # irregular silent letters (cost 2)


def table():
    """grapheme -> [(phoneme tuple, cost, tag)], where tag is the GPC entry it came from."""
    out = collections.defaultdict(list)
    def add(gr, ph, cost, tag):
        t = tuple(ph.split()) if ph else ()
        if not any(x[0] == t and x[1] <= cost for x in out[gr]): out[gr].append((t, cost, tag))
    for key, (main, alt, _) in T.items():
        gr = key.rstrip(".")
        if "_" in key:   # split digraph: the vowel letter carries it; the final e is silent (see align)
            for ph in main: add(key[0], ph, 0, key)
            continue
        if key == "ə":
            for v in SCHWA_LETTERS:
                for ph in main: add(v, ph, 0, "ə")
            continue
        for ph in main: add(gr, ph, 0, key)
        for ph in alt: add(gr, ph, 1, key + "~")
    add("e", "", 0, "e(silent)")
    for v in "aeiouy":
        for p in VOW: add(v, p, 2, "irregular")
    for c in SILENT: add(c, "", 2, "silent")
    add("w", "W AH", 1, "o~")
    for gr, ph in [("oo", "AO"), ("ou", "AA"), ("au", "AE"), ("ay", "IY"), ("ay", "EH"), ("ay", "AY"), ("ai", "AH"), ("oa", "AO"),
                   ("aa", "AA"), ("uy", "AY"), ("oe", "AH"), ("re", "ER"), ("r", "ER"), ("q", "K"), ("u", "Y AH"), ("u", "Y UH"),
                   ("u", "AH W"), ("u", "UW W"), ("u", "Y UW"), ("u", "UW"), ("u", "Y ER"), ("u", "Y AH W"), ("l", "AH L"), ("nt", "AH N T"), ("io", "AH"),
                   ("ion", "AH N"), ("ion", "Y AH N"), ("ious", "AH S"), ("ious", "IY AH S"), ("ious", "Y AH S"), ("tious", "SH AH S"),
                   ("cious", "SH AH S"), ("ey", "EY"), ("ey", "IY"), ("ei", "EY"), ("ei", "IY"), ("ough", "AO"), ("ough", "OW"),
                   ("ough", "UW"), ("ough", "AW"), ("augh", "AO"), ("our", "AO R"), ("our", "AW ER"), ("ire", "AY ER"),
                   ("ia", "IY AH"), ("eo", "IY AH"), ("ue", "UW AH")]:
        add(gr, ph, 1, gr + "~")
    for c in "aeiour": add(c, "", 2, "silent")
    return out


TAB = table()
MAXG = max(len(k) for k in TAB)


def greedy(w, P):
    """Greedy longest-grapheme parse, each grapheme takes the first main candidate that fits."""
    out, i, j = [], 0, 0
    while i < len(w):
        for L in range(min(MAXG, len(w) - i), 0, -1):
            gr = w[i:i + L]
            if gr in TAB: break
        else:
            return None
        hit = next(((t, tag) for t, c, tag in sorted(TAB[gr], key=lambda x: -len(x[0])) if c == 0 and tuple(P[j:j + len(t)]) == t
                    and (t or gr == "e" and i == len(w) - 1)), None)
        if hit is None: return None
        out.append((gr, " ".join(hit[0]), hit[1])); i += L; j += len(hit[0])
    return out if j == len(P) else None


def search(w, P):
    """Min-cost alignment (Dijkstra over (i, j)); 0.01 per grapheme so fewer, longer graphemes win ties."""
    import heapq
    best = {(0, 0): 0.0}; prev = {}; pq = [(0.0, 0, 0)]
    while pq:
        c, i, j = heapq.heappop(pq)
        if (i, j) == (len(w), len(P)): break
        if c > best.get((i, j), 1e9): continue
        for L in range(1, min(MAXG, len(w) - i) + 1):
            gr = w[i:i + L]
            for t, cost, tag in TAB.get(gr, ()):
                if tuple(P[j:j + len(t)]) != t: continue
                if not t and gr == "e" and cost == 0 and not (i == len(w) - 1 or w[i + 1:] in ("s", "d", "ly", "ful", "ment", "ness")):
                    cost = 2   # a silent e is regular only word-finally (or before an ending)
                nc = c + cost + 0.01; k = (i + L, j + len(t))
                if nc < best.get(k, 1e9):
                    best[k] = nc; prev[k] = (i, j, gr, " ".join(t), tag); heapq.heappush(pq, (nc, *k))
    k = (len(w), len(P))
    if k not in prev: return None, None
    out = []
    while k != (0, 0):
        i, j, gr, ph, tag = prev[k]; out.append((gr, ph, tag)); k = (i, j)
    return out[::-1], best[(len(w), len(P))]


def mark_split(al):
    """VCe: long vowel + one consonant grapheme + silent final e -> the vowel's tag becomes a_e/i_e/..."""
    al = [list(x) for x in al]
    for n in range(len(al) - 2):
        g0, p0, _ = al[n]
        if g0 in LONG and al[n + 2][0] == "e" and al[n + 2][1] == "" and not any(ch in "aeiou" for ch in al[n + 1][0]):
            if p0 in T[LONG[g0]][0]: al[n][2] = LONG[g0]; al[n + 2][2] = LONG[g0] + "(e)"
    return [tuple(x) for x in al]


def status_of(al, cost):
    if al is None: return "unaligned"
    tags = [t for _, _, t in al]
    if any(t in ("irregular", "silent") for t in tags): return "irregular"
    if any(t.endswith("~") for t in tags): return "alt"
    return "gpc"


# ------------------------------------------------------------------ CMUdict
def load_cmu():
    d = collections.defaultdict(list)
    for line in (C / "cmudict/cmudict.dict").read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line: continue
        w, *ph = line.split()
        d[re.sub(r"\(\d+\)$", "", w)].append(" ".join(ph))
    return d


def strip(a): return " ".join(p.rstrip("012") for p in a.split())


# ------------------------------------------------------------------ homographs: sense by lesson context (rules)
DET = r"(?:a|an|the|this|that|my|your|his|her|our|their|its|no|every|each)"
MODAL = r"(?:to|will|can|could|would|should|must|might|may|shall|let's|please|don't|didn't|do|does|did|i'll|we'll|you'll)"
HOMO = {   # word: {sense: Arpabet(stressed)}, rule(context, lesson) -> sense
    "read": ({"present": "R IY1 D", "past": "R EH1 D"},
             lambda c, L: "past" if re.search(r"\b(had|has|have|was|were|been|having)\s+(\w+\s+)?read\b|\bread\s+(it|that|the\s+\w+)\s+(yesterday|last|before)", c) else "present"),
    "live": ({"verb": "L IH1 V", "adj": "L AY1 V"},
             lambda c, L: "adj" if re.search(r"\b(a|the)\s+live\b|\blive\s+(music|show|wire|animals?|broadcast|stream|bait|concert)", c) else "verb"),
    "lives": ({"verb": "L IH1 V Z", "noun": "L AY1 V Z"},
              lambda c, L: "noun" if re.search(rf"\b({DET}|save|saved|whole|many|two|three|nine|daily|busy|their|our)\s+lives\b", c) else "verb"),
    "wind": ({"noun": "W IH1 N D", "verb": "W AY1 N D"},
             lambda c, L: "verb" if (re.search(rf"\b{MODAL}\s+wind\b|\bwind\s+(up|it|the\s+(clock|string|rope))", c) or "ind" in L.get("title", "")) else "noun"),
    "lead": ({"verb": "L IY1 D", "metal": "L EH1 D"},
             lambda c, L: "metal" if re.search(r"\blead\s+(pipe|paint|pencil|poisoning)|\bof\s+lead\b", c) else "verb"),
    "tear": ({"cry": "T IH1 R", "rip": "T EH1 R"},
             lambda c, L: "rip" if re.search(rf"\b{MODAL}\s+tear\b|\btear\s+(up|off|apart|down|it|the|a)\b", c) else "cry"),
    "tears": ({"cry": "T IH1 R Z", "rip": "T EH1 R Z"},
              lambda c, L: "rip" if re.search(r"\b(he|she|it)\s+tears\b", c) else "cry"),
    "bow": ({"bend": "B AW1", "ribbon": "B OW1"},
            lambda c, L: "ribbon" if (re.search(r"\b(a|the)\s+bow\b|\bbow\s+(and|tie)|\bribbon", c) or "ō" in L.get("newToday", "") ) else "bend"),
    "close": ({"verb": "K L OW1 Z", "near": "K L OW1 S"},
              lambda c, L: "near" if re.search(r"\bclose\s+(to|by|friend|call|look|together)\b|\b(so|very|too|a)\s+close\b", c) else "verb"),
    "use": ({"verb": "Y UW1 Z", "noun": "Y UW1 S"},
            lambda c, L: "noun" if re.search(rf"\b({DET}|of|any|some|in)\s+use\b|\buse\s+(of|for)\b", c) else "verb"),
    "wound": ({"injury": "W UW1 N D", "wound-up": "W AW1 N D"},
              lambda c, L: "wound-up" if re.search(r"\bwound\s+(up|around|the|it)\b", c) else "injury"),
    "minute": ({"time": "M IH1 N AH0 T", "tiny": "M AY0 N UW1 T"},
               lambda c, L: "tiny" if re.search(r"\b(a|so|very)\s+minute\s+(amount|detail|change)", c) else "time"),
    "row": ({"line": "R OW1", "fight": "R AW1"}, lambda c, L: "line"),
    "does": ({"verb": "D AH1 Z", "deer": "D OW1 Z"}, lambda c, L: "verb"),
    "excuse": ({"noun": "IH0 K S K Y UW1 S", "verb": "IH0 K S K Y UW1 Z"},
               lambda c, L: "noun" if re.search(rf"\b({DET}|good|poor)\s+excuse\b", c) else "verb"),
    "present": ({"noun": "P R EH1 Z AH0 N T", "verb": "P R IY0 Z EH1 N T"},
                lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+present\b", c) else "noun"),
    "record": ({"noun": "R EH1 K ER0 D", "verb": "R IH0 K AO1 R D"},
               lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+record\b", c) else "noun"),
    "object": ({"noun": "AA1 B JH EH0 K T", "verb": "AH0 B JH EH1 K T"},
               lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+object\b", c) else "noun"),
    "content": ({"noun": "K AA1 N T EH0 N T", "adj": "K AH0 N T EH1 N T"},
                lambda c, L: "adj" if re.search(r"\b(feel|felt|feels|was|is|be|are|were|seem|seemed)\s+content\b", c) else "noun"),
    "project": ({"noun": "P R AA1 JH EH2 K T", "verb": "P R AA0 JH EH1 K T"},
                lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+project\b", c) else "noun"),
    "produce": ({"verb": "P R AH0 D UW1 S", "noun": "P R OW1 D UW0 S"},
                lambda c, L: "noun" if re.search(rf"\b({DET}|fresh|local)\s+produce\b", c) else "verb"),
    "refuse": ({"verb": "R IH0 F Y UW1 Z", "noun": "R EH1 F Y UW2 Z"}, lambda c, L: "verb"),
    "permit": ({"noun": "P ER1 M IH2 T", "verb": "P ER0 M IH1 T"},
               lambda c, L: "noun" if re.search(rf"\b{DET}\s+permit\b", c) else "verb"),
    "subject": ({"noun": "S AH1 B JH IH0 K T", "verb": "S AH0 B JH EH1 K T"}, lambda c, L: "noun"),
    "desert": ({"sand": "D EH1 Z ER0 T", "leave": "D IH0 Z ER1 T"},
               lambda c, L: "leave" if re.search(rf"\b{MODAL}\s+desert\b", c) else "sand"),
    "conduct": ({"noun": "K AA1 N D AH0 K T", "verb": "K AH0 N D AH1 K T"},
                lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+conduct\b", c) else "noun"),
    "contract": ({"noun": "K AA1 N T R AE2 K T", "verb": "K AH0 N T R AE1 K T"},
                 lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+contract\b", c) else "noun"),
    "house": ({"noun": "HH AW1 S", "verb": "HH AW1 Z"}, lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+house\b", c) else "noun"),
    "separate": ({"adj": "S EH1 P ER0 IH0 T", "verb": "S EH1 P ER0 EY2 T"},
                 lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+separate\b", c) else "adj"),
    "estimate": ({"noun": "EH1 S T AH0 M AH0 T", "verb": "EH1 S T AH0 M EY2 T"},
                 lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+estimate\b", c) else "noun"),
    "moderate": ({"adj": "M AA1 D ER0 AH0 T", "verb": "M AA1 D ER0 EY2 T"}, lambda c, L: "adj"),
    "polish": ({"shine": "P AA1 L IH0 SH", "nationality": "P OW1 L IH0 SH"}, lambda c, L: "shine"),
    "dove": ({"bird": "D AH1 V", "dived": "D OW1 V"}, lambda c, L: "dived" if re.search(r"\b(he|she|they|we|i|it)\s+dove\b", c) else "bird"),
    "bass": ({"music": "B EY1 S", "fish": "B AE1 S"}, lambda c, L: "music"),
    "sow": ({"plant": "S OW1", "pig": "S AW1"}, lambda c, L: "plant"),
    "invalid": ({"adj": "IH2 N V AE1 L IH0 D", "noun": "IH1 N V AH0 L IH0 D"}, lambda c, L: "adj"),
    "alternate": ({"adj": "AO1 L T ER0 N AH0 T", "verb": "AO1 L T ER0 N EY2 T"}, lambda c, L: "adj"),
    "graduate": ({"noun": "G R AE1 JH AH0 W AH0 T", "verb": "G R AE1 JH AH0 W EY2 T"},
                 lambda c, L: "verb" if re.search(rf"\b{MODAL}\s+graduate\b", c) else "noun"),
}


# ------------------------------------------------------------------ pseudoword composer
def lkey(lid):
    m = re.match(r"L(\d+)\.(\d+)", lid or "L9.99"); return (int(m.group(1)), int(m.group(2)))


def compose(w, level, lesson=None):
    """Deterministic Arpabet (stressed: first vowel 1) for a made-up word from the GPC table, using only the
    graphemes taught by `lesson` (default: the end of `level`)."""
    w = w.lower(); grs, i = [], 0
    upto = lkey(lesson) if lesson else (level, 99)
    taught = {k: v for k, v in T.items() if "_" not in k and "." not in k and lkey(v[2]) <= upto and k != "ə"}
    while i < len(w):
        for L in range(min(4, len(w) - i), 0, -1):
            gr = w[i:i + L]
            if gr in taught or L == 1:
                if L > 1 and gr in ("le",) and i + 2 != len(w): continue
                if gr in ("es", "ed", "ing", "er", "ous", "tion", "sion", "ture") and i + L != len(w) and gr not in ("er",): continue
                break
        grs.append(gr); i += L
    vowel_g = lambda gr: gr[0] in "aeiou" and gr in "aeiou" or gr in ("y",) and False
    out = []
    for n, gr in enumerate(grs):
        nxt = grs[n + 1] if n + 1 < len(grs) else None; nxt2 = grs[n + 2] if n + 2 < len(grs) else None
        if gr == "e" and n == len(grs) - 1 and n > 0 and upto >= (3, 1): continue      # silent final e
        if gr in "aeiou" and len(gr) == 1:
            rest = "".join(grs[n + 1:])
            longv = lambda: out.append(T[LONG[gr]][0][0].split()[0] if gr != "u" else "UW")
            if upto >= (3, 1) and nxt in ("ce", "ge") and n + 1 == len(grs) - 1: longv(); continue           # plage
            if upto >= (3, 16) and ((gr == "o" and rest in ("ld", "st", "lt")) or (gr == "i" and rest in ("ld", "nd"))):
                longv(); continue                                                                          # -old -ost -ild -ind
            if upto >= (3, 4) and nxt and len(nxt) == 1 and nxt not in "aeiouxwy" and "".join(grs[n + 2:]) in ("ing", "ed", "er", "y", "est"):
                longv(); continue                                                                          # drop-e: snaping
            if nxt and nxt2 == "e" and n + 2 == len(grs) - 1 and not any(ch in "aeiou" for ch in nxt) and upto >= (3, 1):
                out.append(T[LONG[gr]][0][0].split()[0] if gr != "u" else "UW"); continue   # VCe
            if upto >= (3, 5) and nxt and nxt2 and len(nxt) == 1 and nxt not in "aeiouxwy" and nxt2[0] in "aeiouy" and n + 2 < len(grs) - 1:
                out.append(T[gr + "."][0][0].split()[0] if gr != "u" else "UW"); continue   # V/CV open syllable
            out.append(T[gr][0][0].split()[0]); continue
        if gr == "gh" and n == 0: out.append("G"); continue                                              # ghost, ghab
        if gr in ("c", "g") and upto >= (3, 7) and nxt and nxt[0] in "eiy":
            out.append("S" if gr == "c" else "JH"); continue
        if gr == "y" and n == len(grs) - 1 and n > 0 and upto >= (3, 6):
            out.append("IY" if sum(ch in "aeiou" for ch in w) >= 1 and len(w) > 3 else "AY"); continue
        if gr == "s" and n == len(grs) - 1: out.append("S"); continue
        main = taught[gr][0][0] if gr in taught else T[gr][0][0] if gr in T else ""
        out.extend(main.split())
    if grs and grs[-1] == "ed" and len(out) >= 2 and out[-1] in ("T",):   # L2.10: -ed is /t/ /d/ /ed/ by the sound before it
        prev = out[-2]
        out[-1:] = ["IH", "D"] if prev in ("T", "D") else ["T"] if prev in ("P", "K", "F", "S", "SH", "CH", "TH") else ["D"]
    out = [p for n, p in enumerate(out) if n == 0 or p != out[n - 1] or p in VOW]   # no geminates (brammed = B R AE M D)
    st, res = False, []
    for p in out:
        if p in VOW: res.append(p + ("0" if st else "1")); st = True
        else: res.append(p)
    return " ".join(res), grs


# ------------------------------------------------------------------ word harvest
LEARNER = [("read.A.text", "text"), ("read.B.text", "text"), ("read.questions", "text"), ("listen.title", "text"),
           ("listen.passage", "text"), ("listen.tier2.word", "text"), ("listen.tier2.def", "text"), ("listen.tier2.full", "text"),
           ("listen.questions", "text"), ("blendList.real", "real"), ("blendList.pseudo", "pseudo"), ("check.real", "real"),
           ("check.pseudo", "pseudo"), ("check.dictation", "text"), ("heart.word", "real"), ("sittings.heart.word", "real"),
           ("sittings.warm.words", "real"), ("sittings.blend.real", "real"), ("sittings.blend.pseudo", "pseudo"),
           ("sittings.spell.words", "real"), ("sittings.spell.sentence", "text"), ("check.freeResponse", "text"),
           ("spell.words", "real"), ("spell.sentence", "text"), ("check.attack", "real")]   # Levels 2-4 lesson-level spell + L4.15 attack words


def get(o, path):
    if not path:
        if isinstance(o, list): yield from o
        else: yield o
        return
    k, *rest = path.split(".", 1); rest = rest[0] if rest else ""
    if isinstance(o, list):
        for x in o: yield from get(x, path)
    elif isinstance(o, dict) and o.get(k) is not None:
        yield from get(o[k], rest)


def sentences_with(text, w):
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if re.search(rf"\b{re.escape(w)}\b", s, re.I)]


def harvest():
    global ALLW
    ALLW = collections.defaultdict(set)
    def walk(o):
        if isinstance(o, str): yield o
        elif isinstance(o, dict):
            for v in o.values(): yield from walk(v)
        elif isinstance(o, list):
            for v in o: yield from walk(v)
    words = collections.defaultdict(lambda: {"levels": set(), "lessons": set(), "fields": set(), "ctx": []})
    pseudo = collections.defaultdict(lambda: {"levels": set(), "lessons": set(), "fields": set()})
    for f in sorted((C / "lessons").glob("*.json")):
        L = json.loads(f.read_text()); lid, lv = L["id"], L["level"]
        for k, v in L.items():
            if k in ("id", "source", "contentVersion", "blocksFound"): continue
            for st in walk(v): ALLW[lv].update(t.lower() for t in WORD.findall(st))
        comps = [(f"check.components.{c['id']}", "pseudo" if c["kind"] == "pseudo" else "real", c["items"]) for c in (L.get("check") or {}).get("components", [])]
        for path, kind, strs in [(p_, k_, list(get(L, p_))) for p_, k_ in LEARNER] + comps:   # + level mastery-check components
            for s in strs:
                if not isinstance(s, str): continue
                for tok in WORD.findall(s):
                    key = tok if tok == "I" else tok.lower()
                    d = (pseudo if kind == "pseudo" else words)[key]
                    d["levels"].add(lv); d["lessons"].add(lid); d["fields"].add(path)
                    if kind != "pseudo":
                        if kind == "real": d.setdefault("target_lessons", set()).add(lid)
                        if len(d["ctx"]) < 12:
                            for sn in (sentences_with(s, tok) if kind == "text" else [s]):
                                d["ctx"].append((lid, sn.lower()))
    # Level 1 tap-gate items and the app lexicon (made-up words that exist only there)
    lex = json.loads((C / "lexicon.json").read_text()); opts = json.loads((C / "options.json").read_text())
    l1 = {}
    for e in lex.values(): l1.setdefault((e["w"], e["ipa"]), {"kind": e["kind"], "lessons": e.get("lessons", [])})
    for k, o in opts.items():
        for x in [o["target"], *o["foils"]]: l1.setdefault((x["w"], x["ipa"]), {"kind": None, "lessons": []})
    return words, pseudo, l1


def main():
    cmu = load_cmu()
    words, pseudo, l1 = harvest()
    lessons = {json.loads(f.read_text())["id"]: json.loads(f.read_text()) for f in (C / "lessons").glob("*.json")}
    out, l1_cmp = {}, []
    for w in list(words):
        if w in pseudo and not any(f.endswith(("text", "passage", "questions", "sentence", "def", "full", "title")) for f in words[w]["fields"]):
            pseudo[w]["levels"] |= words[w]["levels"]; pseudo[w]["lessons"] |= words[w]["lessons"]; del words[w]
    for w in sorted(words, key=str.lower):
        d = words[w]; key = w.lower()
        prons = cmu.get(key, [])
        e = {"kind": "real", "levels": sorted(d["levels"]), "lessons": sorted(d["lessons"]), "source": "cmudict"}
        flags = []
        if not prons and key.endswith("'s") and cmu.get(key[:-2]):
            b = cmu[key[:-2]][0]; last = strip(b).split()[-1]
            suf = " IH0 Z" if last in ("S", "Z", "SH", "ZH", "CH", "JH") else " S" if last in ("P", "T", "K", "F", "TH") else " Z"
            prons = [b + suf]; e["source"] = "cmudict+'s"
        if not prons:
            lvl = min(d["levels"]); a, _ = compose(key.replace("'", ""), lvl, min(d["lessons"], key=lkey))
            prons = [a]; e["source"] = "gpc-composed (not in CMUdict)"; flags.append("oov")
        pick = prons[0]
        if key in HOMO:
            senses, rule = HOMO[key]
            e["homograph"] = []
            for lid, ctx in d["ctx"][:12]:
                s = rule(ctx, lessons.get(lid, {}))
                e["homograph"].append({"lesson": lid, "context": ctx[:120], "sense": s, "arpa": strip(senses[s])})
            from collections import Counter
            tl = sorted(d.get("target_lessons", ()), key=lkey)
            if tl:   # taught as a list word in a lesson: that lesson's spelling pattern decides (wind in L3.16 -ind = /waɪnd/)
                s0 = rule(f"{key} " + lessons.get(tl[0], {}).get("title", ""), lessons.get(tl[0], {}))
                e["homograph"].insert(0, {"lesson": tl[0], "context": "(word list) " + lessons.get(tl[0], {}).get("title", ""), "sense": s0,
                                          "arpa": strip(senses[s0]), "decides": True})
                top = s0
            else:
                top = Counter(x["sense"] for x in e["homograph"]).most_common(1)[0][0] if e["homograph"] else next(iter(senses))
            pick = senses[top]; flags.append("homograph-review")
        e["arpa_stress"] = pick; e["arpa"] = strip(pick)
        if len(prons) > 1: e["variants"] = [strip(p) for p in prons[1:4]]
        P = e["arpa"].split(); wl = re.sub(r"[^a-z]", "", key)
        al = greedy(wl, P); how = "greedy"
        if al is None: al, cost = search(wl, P); how = "search"
        if al is not None: al = mark_split(al)
        e["status"] = status_of(al, None); e["parse"] = how if al else None
        if len(key.split("'")[0]) == 1 and key not in ("a", "i"): e["status"] = "letter-name"
        if key in ("mr", "mrs", "dr", "st", "ms", "th"): e["status"] = "abbreviation"
        e["align"] = [[gr, ph] for gr, ph, _ in al] if al else None
        e["gpc"] = [t for _, _, t in al] if al else None
        if e["status"] in ("unaligned", "irregular"): flags.append(e["status"])
        e["flags"] = flags
        out[w] = e
    for w in sorted(pseudo):
        if w in out: continue   # also used as a real word somewhere
        d = pseudo[w]; lvl = min(d["levels"]); a, grs = compose(w, lvl, min(d["lessons"], key=lkey))
        out[w] = {"kind": "pseudo", "levels": sorted(d["levels"]), "lessons": sorted(d["lessons"]), "source": "gpc-composed",
                  "arpa_stress": a, "arpa": strip(a), "graphemes": grs, "status": "composed",
                  "flags": ["multisyllable-review"] if sum(p in VOW for p in strip(a).split()) > 1 else [],
                  **({"in_cmudict": strip(cmu[w][0])} if w in cmu else {})}
    # Level 1 app items (lexicon + tap-gate foils): course IPA vs CMUdict vs composer
    import sys; sys.path.insert(0, str(ROOT / "tools")); import el_dict
    for (w, ipa), m in sorted(l1.items()):
        course = el_dict.strip(el_dict.ipa2arpa(ipa)); key = w if w == "I" else w.lower()
        kind = m["kind"] or ("real" if key in cmu or key in out and out[key]["kind"] == "real" else "pseudo")
        cm = [strip(p) for p in cmu.get(key.lower(), [])]
        comp = strip(compose(key, 1, min(m["lessons"], key=lkey) if m["lessons"] else "L1.14")[0])
        row = {"w": w, "ipa": ipa, "course_arpa": course, "kind": kind, "cmudict": cm[:3], "composed": comp,
               "agrees_cmu": (course in cm) if cm else None, "agrees_composed": course == comp}
        l1_cmp.append(row)
        if key not in out:
            out[key] = {"kind": "pseudo" if kind == "pseudo" else "real", "levels": [1], "lessons": m["lessons"], "source": "level1-app (course IPA)",
                        "arpa_stress": el_dict.ipa2arpa(ipa), "arpa": course, "status": "composed" if kind == "pseudo" else "course-ipa",
                        "flags": [], "app_only": True}
    (C / "lexicon_full.json").write_text(json.dumps({"source": "CMUdict cmusphinx/cmudict (content/cmudict, BSD-2) + GPC table (content/gpc.json full)",
                                                    "words": out, "level1_check": l1_cmp}, indent=0, ensure_ascii=False))
    # gpc.json: add the full L1-L4 table, keep the app's keys untouched
    gpc = json.loads((C / "gpc.json").read_text())
    gpc["full"] = {"note": "DESIGN.md §3 master sequence L1-L4 in CMU Arpabet (tools/build_lexicon.py). key suffix '.' = "
                           "context variant (open syllable, soft c/g, ow /aw/, ea /e/, ch /k/); 'a_e' etc = split digraph; "
                           "main = taught GPC, alt = alternates the aligner accepts at cost 1.",
                   "sequence": [{"g": k, "main": v[0], "alt": v[1], "lesson": v[2]} for k, v in T.items()],
                   "arpabet_ipa": el_dict.ARPA2IPA,
                   "level1_ids": {pid: el_dict.strip(el_dict.ipa2arpa(ipa)) for pid, ipa in gpc["phonemes"].items()}}
    (C / "gpc.json").write_text(json.dumps(gpc, indent=1, ensure_ascii=False))
    write_coverage(out, l1_cmp)


def write_coverage(out, l1_cmp):
    cmu = load_cmu()
    rows = []
    for lv in range(1, 8):
        R = [e for e in out.values() if lv in e["levels"] and e["kind"] == "real" and not e.get("app_only")]
        P = [e for e in out.values() if lv in e["levels"] and e["kind"] == "pseudo" and not e.get("app_only")]
        inc = sum(e["source"].startswith("cmudict") for e in R)
        st = collections.Counter(e["status"] for e in R)
        hom = sum("homograph-review" in e["flags"] for e in R)
        multi = sum("multisyllable-review" in e["flags"] for e in P)
        rows.append(f"| {lv} | {len(R)} | {inc} ({100 * inc / max(1, len(R)):.1f}%) | {st['gpc']} | {st['alt']} | {st['irregular']} | "
                    f"{st['unaligned']} | {st['letter-name'] + st['abbreviation']} | {len(R) - inc} | {hom} | {len(P)} | {multi} | "
                    f"{len(ALLW[lv])} / {sum(w in cmu for w in ALLW[lv])} |")
    allR = [e for e in out.values() if e["kind"] == "real" and not e.get("app_only")]
    allP = [e for e in out.values() if e["kind"] == "pseudo" and not e.get("app_only")]
    oov = sorted(w for w, e in out.items() if "oov" in e["flags"])
    hom = {w: e for w, e in out.items() if "homograph-review" in e["flags"]}
    una = sorted(w for w, e in out.items() if e["status"] == "unaligned")
    real1 = [r for r in l1_cmp if r["kind"] != "pseudo" and r["cmudict"]]
    dis = [r for r in real1 if not r["agrees_cmu"]]
    ps1 = [r for r in l1_cmp if r["kind"] == "pseudo"]
    psd = [r for r in ps1 if not r["agrees_composed"]]
    txt = ("## Full-course lexicon (CMUdict, decision 21)\n\n"
           "`tools/build_lexicon.py` -> `content/lexicon_full.json`. Words = every word token in the learner-facing fields of all "
           "108 lessons (read texts + questions, listen passages/titles/Tier-2/questions, blend lists, checks, dictation, heart "
           "words, sitting word lists); tutor notes (goal, newToday, time, mouth cues) are not harvested. A word is counted in "
           "every level it appears in. Arpabet from CMUdict (first pronunciation, stress stripped; stressed form kept for the PLS). "
           "Alignment against the DESIGN.md L1-L4 GPC table (`content/gpc.json` `full`): **gpc** = every grapheme is a taught "
           "main correspondence, **alt** = uses a listed alternate, **irregular** = needs an irregular vowel or silent letter "
           "(heart-word parts; Level 5-7 vocabulary), **unaligned** = no parse. Pseudowords are composed from the table, never "
           "looked up. Levels 5-7 have little parsed learner text in this prototype (parse_course.py best effort: mostly "
           "read questions), so their counts are small; the last column counts every field, tutor notes included.\n\n"
           "| Level | real words | in CMUdict | gpc | alt | irregular | unaligned | letter/abbrev. | not in CMUdict | homographs | pseudowords | multi-syll. pseudo (review) | all fields incl. tutor notes: words / in CMUdict |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
           f"All levels: {len(allR)} distinct real words, {sum(e['source'].startswith('cmudict') for e in allR)} in CMUdict; "
           f"{len(allP)} distinct pseudowords.\n\n"
           f"**Not in CMUdict ({len(oov)}; composed from the GPC table, flagged `oov`):** {', '.join(oov[:80])}{' ...' if len(oov) > 80 else ''}\n\n"
           f"**Unaligned ({len(una)}):** {', '.join(una[:80])}{' ...' if len(una) > 80 else ''}\n\n"
           f"**Homographs ({len(hom)}, sense chosen by lesson-context rules, all flagged `homograph-review`):** "
           + "; ".join(f"{w} -> {e['arpa']} ({e['homograph'][0]['lesson'] if e.get('homograph') else ''}: "
                       f"{collections.Counter(x['sense'] for x in e.get('homograph', [])).most_common()})" for w, e in sorted(hom.items())) + "\n\n"
           f"**Level 1 app items vs CMUdict:** {len(real1)} real Level 1 items (lexicon + tap-gate) are in CMUdict; "
           f"{len(real1) - len(dis)} match the course IPA exactly, {len(dis)} differ: "
           + ", ".join(f"{r['w']} (course {r['course_arpa']} / CMU {r['cmudict'][0]})" for r in dis[:40]) + ". "
           f"**Level 1 pseudowords:** {len(ps1)}; the GPC composer reproduces the course IPA for {len(ps1) - len(psd)}"
           + (": differs for " + ", ".join(f"{r['w']} ({r['course_arpa']} vs {r['composed']})" for r in psd[:30]) if psd else "") + ".\n\n")
    cov = C / "coverage.md"
    cur = cov.read_text() if cov.exists() else ""
    cur = re.sub(r"## Full-course lexicon \(CMUdict.*?(?=\n## |\Z)", "", cur, flags=re.S)
    if "\n## Isolated sounds" in cur:
        a, b = cur.split("\n## Isolated sounds", 1); cur = a.rstrip() + "\n\n" + txt + "## Isolated sounds" + b
    else:
        cur = cur.rstrip() + "\n\n" + txt
    cov.write_text(cur)
    print(txt[:6000])


if __name__ == "__main__":
    main()
