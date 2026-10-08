#!/usr/bin/env python3
"""Level 1 items that live outside the lesson files: the Level 1 mastery instrument (course/level-1/mastery-check.md),
used by app/src/screens/l1mastery.js. Adds the words no lesson lists (fib, mud, 7 alien words) to content/lexicon.json,
segmented with parse_course's Level 1 GPC table, tagged lesson L1.14. Idempotent; run after tools/parse_course.py, then
`--options`: tap-gate grids for them through tools/gen_options.py's Level 1 ladder (unchanged), with the words that
content/lexicon_full.json does not know yet given an Arpabet entry in memory (CMUdict for real words, the Level 1 GPC
sounds for alien words), so lexicon_full.json is not rewritten. Then tools/gen_audio_el.py plan/render/build.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_course as pc

C = Path(__file__).resolve().parent.parent / "content"
REAL = "sat pin mad dog sock cut hen fib bell hats jog van wig box yak zip quiz big dip mess hat bug fox jazz pig in mud bag quit bat pat".split()
PSEUDO = "taf nid gof kec rup haz vin quob fex dov".split()

lex = json.loads((C / "lexicon.json").read_text())
added = []
for kind, ws in (("real", REAL), ("pseudo", PSEUDO)):
    for w in ws:
        if w in lex:
            if "L1.14" not in lex[w]["lessons"]: lex[w]["lessons"] = sorted(set(lex[w]["lessons"]) | {"L1.14"})
            continue
        g, p = pc.segment(w)
        lex[w] = {"w": w, "g": g, "p": p, "ipa": pc.ipa_of(p), "kind": kind, "lessons": ["L1.14"]}
        added.append(w)
(C / "lexicon.json").write_text(json.dumps(lex, indent=1, ensure_ascii=False))
print(f"lexicon: +{len(added)} ({' '.join(added)}); {len(lex)} entries")

ARPA = {"s": "S", "a": "AE", "t": "T", "p": "P", "i": "IH", "n": "N", "m": "M", "d": "D", "g": "G", "o": "AA", "k": "K", "e": "EH",
        "u": "AH", "r": "R", "h": "HH", "b": "B", "f": "F", "l": "L", "j": "JH", "v": "V", "w": "W", "ks": "K S", "y": "Y", "z": "Z", "kw": "K W"}
if "--options" in sys.argv:
    import gen_options as go
    for w in added or [w for w in REAL + PSEUDO if w not in go.FULL]:
        e = lex[w]
        if w in go.FULL: continue
        arpa = " ".join(sorted(go.CMU[w])[0]) if e["kind"] == "real" and w in go.CMU else " ".join(ARPA[x] for x in e["p"])
        go.FULL[w] = {"kind": e["kind"], "arpa": arpa, "source": "cmudict" if e["kind"] == "real" and w in go.CMU else "gpc-composed"}
        print("arpa", w, arpa)
    go.main()
