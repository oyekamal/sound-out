#!/usr/bin/env python3
"""Levels 2-4 app bundles: content/levels/L<N>.json (lessons + sittings + app lexicon + rule cards + mastery) and the
per-level audio list content/audio_needed.json. Level 1 files (lexicon.json, options.json, lessons/L1.*) are not touched.

  python3 tools/build_levels.py 2            # bundle (run gen_options.py --level 2 next, then this again for the audio list)
  python3 tools/gen_options.py --level 2     # content/options_L2.json + options_unbuildable_L2.json + options_report_L2.md
  python3 tools/build_levels.py 2            # bundle again: audio list now includes every tap-gate option clip

Pipeline: parse_course.py --levels 2,3,4 -> build_lexicon.py (CMUdict alignment) -> this file.
Every word the app shows gets an entry {w, g (graphemes), p (phoneme ids, '_' = silent), ipa, kind, heartIdx?, split?,
suffix?, syl?, vow?}. Phoneme ids reuse the Level 1 ids (s a t ... kw) where the sound is the Level 1 sound; new sounds
get their Arpabet as the id (sh, ey, aa-r ...). Audio is NOT rendered here: content/audio_needed.json lists every clip
key per level in tools/gen_audio_el.py's plan format with exact character totals (`gen_audio_el.py needed L2` renders).
"""
import json, math, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_lexicon as BL   # noqa: E402  (alignment table + search)

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
FULL = json.loads((C / "lexicon_full.json").read_text())["words"]
L1LEX = json.loads((C / "lexicon.json").read_text())
VOW = BL.VOW
WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
L1_PID = {("S",): "s", ("AE",): "a", ("T",): "t", ("P",): "p", ("IH",): "i", ("N",): "n", ("M",): "m", ("D",): "d", ("G",): "g",
          ("AA",): "o", ("K",): "k", ("EH",): "e", ("AH",): "u", ("R",): "r", ("HH",): "h", ("B",): "b", ("F",): "f", ("L",): "l",
          ("JH",): "j", ("V",): "v", ("W",): "w", ("K", "S"): "ks", ("Y",): "y", ("Z",): "z", ("K", "W"): "kw"}
IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "EH": "ɛ", "IH": "ɪ", "IY": "i", "UH": "ʊ", "UW": "u", "ER": "ɝ",
       "EY": "eɪ", "AY": "aɪ", "OW": "oʊ", "AW": "aʊ", "OY": "ɔɪ", "S": "s", "T": "t", "P": "p", "N": "n", "M": "m", "D": "d",
       "G": "ɡ", "K": "k", "R": "ɹ", "HH": "h", "B": "b", "F": "f", "L": "l", "JH": "ʤ", "V": "v", "W": "w", "Y": "j", "Z": "z",
       "NG": "ŋ", "CH": "ʧ", "SH": "ʃ", "ZH": "ʒ", "TH": "θ", "DH": "ð"}
LONGV = {"EY", "IY", "AY", "OW", "UW"}
NLESSONS = {2: 14, 3: 18, 4: 16}
SUFFIX_LESSONS = {"L2.09", "L2.10", "L2.11", "L2.13", "L2.14", "L3.04", "L4.13", "L4.16"}
ATTACK_LESSONS = {"L4.12": 2, "L4.14": 3}
PREFIXES = ["dis", "mis", "non", "un", "re", "pre", "con", "de", "ex", "in"]
SUFFIXES = ["ing", "est", "ed", "er", "es", "ly", "ful", "ness", "ment", "s", "ier", "ied", "ies", "iest"]

# Teaching units by lesson (DESIGN.md §3). Graphemes come from the GPC table; blends/patterns are written out here.
BLENDS = {"L2.06": "st sp sn sm sl sw sk sc bl cl fl gl pl br cr dr fr gr pr tr tw".split(),
          "L2.07": "-st -nd -nt -mp -sk -lt -ft -lk".split(), "L2.08": "str spr scr spl squ shr thr".split()}
PATTERNS = {"L3.16": ["ild", "ind", "old", "ost"], "L2.09": ["-s"]}
SUFFIX_UNITS = {"es", "ed", "ing", "er"}
UNIT_LABEL = {"c.": "soft c", "g.": "soft g", "y.": "y as a vowel", "ch.": "ch as /k/ or /sh/", "ow.": "ow as in cow",
              "ea.": "ea as in bread", "a.": "open a", "e.": "open e", "i.": "open i", "o.": "open o", "u.": "open u"}
UNIT_EXAMPLE = {"a.": "paper", "e.": "even", "i.": "tiger", "o.": "robot", "u.": "music", "c.": "city", "g.": "cage",
                "y.": "happy", "ch.": "school", "ow.": "cow", "ea.": "bread", "-s": "cats"}

RULES = {  # short rule cards (the course's own rule, in two or three plain sentences) + example words
    "L2.06": ("Blends", "Two consonants side by side keep BOTH sounds. Say them quickly, one after the other. "
              "FLOSS: after a short vowel at the end of a short word, f, l, s and z are doubled: stuff, smell, glass, buzz.", ["stop", "smell", "spuff"]),
    "L2.07": ("Final blends", "At the end of a word two consonants keep both sounds: nest, hand, jump. "
              "FLOSS still holds: a short vowel then f, l, s or z at the end doubles it.", ["nest", "jump", "milk"]),
    "L2.08": ("Three-letter blends", "s plus a blend: three sounds said quickly, s-t-r in strap. shr and thr start with one digraph sound.", ["strap", "split", "thrill"]),
    "L2.09": ("Adding -s and -es", "Add -s to most words: cat, cats. Add -es after s, x, z, sh, ch and tch: it adds a syllable you can hear, wish, wishes.", ["cats", "wishes", "boxes"]),
    "L2.10": ("Adding -ed", "-ed says /t/ after p k f s sh ch (jumped), /d/ after voiced sounds (grinned), and /ed/ after t or d (wanted).", ["jumped", "grinned", "wanted"]),
    "L2.11": ("Adding -ing and -er", "Read the base word, then add the ending. The base word does not change: jump, jumping, jumper.", ["jumping", "helper", "fixing"]),
    "L2.12": ("Two-syllable words", "Find the two vowels. Split between the two consonants in the middle: rab·bit, nap·kin. Read each part, then the whole word.", ["rabbit", "napkin", "sunset"]),
    "L3.01": ("Silent e", "The e at the end is silent. It jumps over one consonant and makes the vowel say its name: cap, cape.", ["cake", "name", "plane"]),
    "L3.02": ("Silent e", "i_e: the e is silent and the i says its name: kit, kite.", ["time", "bike", "smile"]),
    "L3.03": ("Silent e", "o_e, u_e and e_e work the same way: hop, hope; cub, cube.", ["home", "cute", "these"]),
    "L3.04": ("Drop the e", "Before an ending that starts with a vowel (-ing, -ed, -er), drop the silent e: hope, hoping.", ["hoping", "riding", "making"]),
    "L3.05": ("Open syllables", "A syllable that ends with a vowel is open: the vowel says its name. Try the first vowel open: ro·bot, mu·sic.", ["go", "robot", "music"]),
    "L3.06": ("Y as a vowel", "At the end of a short word y says /ī/: my. At the end of a longer word it says /ē/: happy.", ["my", "happy", "fly"]),
    "L3.07": ("Soft c and soft g", "Before e, i or y, c says /s/ and g usually says /j/: city, cage. After a short vowel, /j/ is spelled -dge: bridge.", ["city", "cage", "bridge"]),
    "L3.15": ("oo has two sounds", "Try the long sound first, moon. If it is not a real word, flex to the short sound, book.", ["moon", "book", "look"]),
    "L3.16": ("Long vowel families", "In -ild, -ind, -old and -ost the vowel says its name even with no silent e: wild, kind, cold, most.", ["wild", "find", "cold"]),
    "L4.02": ("war and wor", "After w, ar often sounds like or (warm) and or often sounds like er (work).", ["warm", "work", "world"]),
    "L4.08": ("Silent letters", "Some letter pairs keep only one sound: kn and gn say /n/, wr says /r/, mb says /m/.", ["knock", "write", "lamb"]),
    "L4.09": ("ph, ch and gh", "ph says /f/. ch can say /k/ (school) or /sh/ (chef). gh says /g/ at the start (ghost).", ["phone", "school", "ghost"]),
    "L4.10": ("Consonant-le", "A word ending in a consonant + le: that last chunk is one syllable, can·dle, ta·ble.", ["candle", "table", "little"]),
    "L4.11": ("-tion, -sion, -ture", "-tion and -sion say /shun/, -ture says /cher/, -ous says /us/. Read the ending as one chunk.", ["nation", "picture", "famous"]),
    "L4.12": ("Breaking words apart", "Mark the vowels. VC/CV: split between consonants (rab·bit). V/CV: try open first (ti·ger). If that is not a word, flex: cab·in. Unstressed vowels often say 'uh'.", ["rabbit", "tiger", "cabin"]),
    "L4.13": ("Suffix spelling", "1-1-1: one syllable, one vowel, one final consonant: double it (run, running). Consonant + y: change y to i (happy, happier). Silent e: drop it (hope, hoping).", ["running", "happier", "hoping"]),
    "L4.14": ("The word-attack routine", "1 Mark the vowels. 2 Peel off prefixes and suffixes. 3 Chunk the middle into syllables. 4 Blend the chunks. 5 Flex if it is not a real word.", ["unfriendly", "reporting", "nonstop"]),
    "L4.15": ("Unknown words", "Do not guess from the picture or the first letter. Use the routine: vowels, peel, chunk, blend, flex. Then check: does it make sense here?", ["comfortable", "dangerous"]),
}
UI_NEW = {"teachIntro": "Here is a new spelling for a sound. Tap it to hear it.", "teachBlend": "These letters keep both sounds. Say them quickly together.",
          "teachSuffix": "This is an ending. Read the base word, then add the ending.", "teachExample": "Here it is in a word.",
          "ruleIntro": "Here is a rule that helps you read.", "attackIntro": "A long word. Let's break it apart, step by step.",
          "attackVowels": "Tap every vowel sound.", "attackPeel": "Tap the parts at the start or end that you know.",
          "attackChunk": "Here are the chunks.", "attackBlend": "Tap each chunk to say it, then put them together.",
          "attackFlex": "Is it a real word? If not, try the vowel the other way.", "masteryIntro": "This is the check for the whole level. Do your best.",
          "masteryPass": "You passed! The next level is open.", "masteryMiss": "Not yet. Let's practise the parts that were hard, then try again.",
          "attackCheckIntro": "Show how you read a word you have never seen."}


def lkey(lid): return BL.lkey(lid)


def lesson_json(lid): return json.loads((C / "lessons" / f"{lid}.json").read_text())


def pid_for(gr, arpa):
    if not arpa: return "_"
    t = tuple(arpa.split())
    if t in L1_PID: return L1_PID[t]
    if t == ("AO",) and gr == "o": return "o"
    return "-".join(x.lower() for x in t)


def ipa_of(arpa_stress):
    out = ""
    for x in arpa_stress.split():
        b = x.rstrip("012")
        if x.endswith("1"): out += "ˈ"
        out += IPA[b]
    return out


def pid_ipa(pid):
    if pid == "_": return ""
    if pid in {v: k for k, v in L1_PID.items()}:
        return "".join(IPA[x] for x in {v: k for k, v in L1_PID.items()}[pid])
    return "".join(IPA[x.upper()] for x in pid.split("-"))


def tag_lesson(t):
    b = (t or "").split("(")[0].rstrip("~")
    return BL.T[b][2] if b in BL.T else None


def align_of(w, f, lid=None):
    """[(grapheme, arpa, tag)] for a lexicon_full entry (aligned real word, or a composed made-up word). With `lid`, a word
    whose parse uses a grapheme taught AFTER lid (king -> k + ing before L2.11) is re-parsed with only the graphemes taught by then."""
    if f.get("align"):
        al = [(g, a, t) for (g, a), t in zip(f["align"], f.get("gpc") or [""] * len(f["align"]))]
    else:
        P = f["arpa"].split()
        al = BL.greedy(w, P)
        if al is None: al, _ = BL.search(w, P)
        al = BL.mark_split(al) if al else None
    if al and lid and any(tag_lesson(t) and lkey(tag_lesson(t)) > lkey(lid) for _, _, t in al):
        full = BL.TAB
        try:
            BL.TAB = {g: [x for x in v if not tag_lesson(x[2]) or lkey(tag_lesson(x[2])) <= lkey(lid)] for g, v in full.items()}
            P = [x for _, a, _ in al for x in a.split()]
            al2, _ = BL.search(w, P)
        finally:
            BL.TAB = full
        if al2: al = BL.mark_split(al2)
    return al


def chunk_text(g, a, s, t):
    """Text + phonemes of grapheme span [s, t) where s/t may be x.5 (a doubled consonant split in the middle: rab|bit)."""
    i0, i1 = math.floor(s), math.ceil(t)
    txt, ph = "", []
    for i in range(i0, i1):
        gr = g[i]
        if i == i0 and s != i0: txt += gr[1:]; continue          # second half of a doubled consonant: letters only, sound already used
        if i == i1 - 1 and t != i1: txt += gr[:1]; ph += a[i].split(); continue
        txt += gr; ph += a[i].split()
    return txt, ph


def syllables(g, a, f_stress):
    """Grapheme-index syllable starts (VC/CV, V/CV for a long first vowel, VC/V otherwise; doubled consonant splits in the middle -> 'i.5')."""
    vow = [i for i, x in enumerate(a) if any(p in VOW for p in x.split())]
    if len(vow) < 2: return [], vow
    starts = []
    for i, j in zip(vow, vow[1:]):
        cons = list(range(i + 1, j))
        if not cons: starts.append(j); continue
        if g[j] == "le" or g[j] in ("tion", "sion", "ture", "cial", "tial"):
            starts.append(j if len(cons) == 0 else cons[-1] if g[j] == "le" else j); continue
        if len(cons) == 1:
            c = cons[0]
            if len(g[c]) == 2 and g[c][0] == g[c][1] and g[c] not in ("ee", "oo"): starts.append(c + 0.5); continue
            if g[c] in ("ck", "x"): starts.append(c + 1); continue
            starts.append(c if a[i].split()[-1] in LONGV else c + 1); continue
        starts.append(cons[1] if len(cons) >= 2 else cons[0])
    return starts, vow


def make_entry(w, lid, heart=False, suffix_lesson=False):
    f = FULL.get(w) or FULL.get(w.lower())
    if not f: return None, "not in lexicon_full"
    al = align_of(w.lower(), f, lid)
    if not al: return None, f"no alignment ({f.get('status')})"
    g = [x[0] for x in al]; a = [x[1] for x in al]; tags = [x[2] for x in al]
    if "".join(g) != w.lower(): return None, "alignment does not spell the word"
    stress = f.get("arpa_stress") or f["arpa"]
    if f["kind"] == "pseudo" and not re.search(r"[012]", stress):
        st = False; out = []
        for x in stress.split():
            out.append(x + ("0" if st else "1") if x in VOW else x); st = st or x in VOW
        stress = " ".join(out)
    e = {"w": w, "g": g, "p": [pid_for(gr, ar) for gr, ar in zip(g, a)], "ipa": ipa_of(stress),
         "kind": "heart" if heart else ("pseudo" if f["kind"] == "pseudo" else "real"), "lessons": [lid]}
    split = []
    for i, t in enumerate(tags):
        if t and t.endswith("_e(e)"):
            j = max((k for k in range(i) if tags[k] == t[:3]), default=None)
            if j is not None: split.append([j, i])
    if split: e["split"] = split
    syl, vow = syllables(g, a, stress)
    if syl: e["syl"] = syl
    e["vow"] = vow
    if suffix_lesson or len(vow) > 1:
        for sfx in SUFFIXES:
            if w.lower().endswith(sfx) and len(w) > len(sfx) + 2:
                n, acc = 0, ""
                for k in range(len(g) - 1, -1, -1):
                    acc = g[k] + acc
                    if acc == sfx: n = k; break
                    if len(acc) >= len(sfx): break
                if n:
                    e["suffix"] = n; break
    pre = next((p for p in PREFIXES if w.lower().startswith(p) and len(w) > len(p) + 3), None)
    if pre:
        acc = ""
        for k, gr in enumerate(g):
            acc += gr
            if acc == pre: e["prefix"] = k + 1; break
            if len(acc) >= len(pre): break
    if heart:
        idx = [i for i, t in enumerate(tags) if not t or t.endswith("~") or t in ("irregular", "silent")
               or (t.rstrip(".").split("(")[0] in BL.T and lkey(BL.T[t.rstrip(".").split("(")[0]][2] if t.rstrip(".").split("(")[0] in BL.T else ("L9.99")) > lkey(lid))]
        e["heartIdx"] = idx or list(range(len(g)))
    e["arpa"] = a
    return e, None


def chunks(e):
    """Syllable chunks (start, end) + their IPA, for the attack routine's blend step (audio key syl:<ipa>)."""
    cuts = [0] + list(e.get("syl", [])) + [len(e["g"])]
    out = []
    for s, t in zip(cuts, cuts[1:]):
        txt, ph = chunk_text(e["g"], e["arpa"], s, t)
        out.append({"from": s, "to": t, "text": txt, "ipa": "".join(IPA[x] for x in ph)})
    return out


def units_for(lid, blend_real):
    out = []
    for g, (main, alt, les) in BL.T.items():
        if les != lid or g == "ə" or "_" in g and g.endswith("(e)"): continue
        disp = g.rstrip(".")
        kind = "split" if "_" in g else "suffix" if g in SUFFIX_UNITS else "grapheme"
        pid = pid_for(disp, main[0])
        ex = UNIT_EXAMPLE.get(g)
        if not ex:
            for w in blend_real:
                f = FULL.get(w)
                if f and f.get("gpc") and g in f["gpc"]: ex = w; break
            ex = ex or next((w for w in blend_real if disp.replace("_", "")[:1] in w and (kind != "split" or w.endswith("e"))), None)
        out.append({"g": disp, "kind": kind, "pid": pid, "ipa": pid_ipa(pid), "label": UNIT_LABEL.get(g), "example": ex, **({"variant": True} if g.endswith(".") else {})})
    for b in BLENDS.get(lid, []):
        out.append({"g": b, "kind": "blend", "letters": list(b.strip("-")), "example": next((w for w in blend_real if (w.endswith(b[1:]) if b.startswith("-") else w.startswith(b))), None)})
    for pt in PATTERNS.get(lid, []):
        out.append({"g": pt, "kind": "suffix" if pt.startswith("-") else "pattern", "example": UNIT_EXAMPLE.get(pt) or next((w for w in blend_real if pt.strip("-") in w), None)})
    return out


def sentence_word(s, prefer):
    ws = [x.lower() for x in WORD.findall(s)]
    for w in ws:
        if w in prefer: return w
    return max(ws, key=len) if ws else None


def build(level):
    lex, problems, lessons = {}, [], []
    gate_items = {}     # word -> {"kind", "lesson"}: every word the tap gate may show at this level

    def add(w, lid, heart=False, gate=None):
        key = w if w == "I" else w.lower()
        if key in L1LEX and not (heart and L1LEX[key]["kind"] != "heart"):
            if gate: gate_items.setdefault(key, {"kind": "pseudo" if gate == "pseudo" else "real", "lesson": lid})
            return key      # the Level 1 entry (with its rendered audio) stays
        if key in lex:
            if lid not in lex[key]["lessons"]: lex[key]["lessons"].append(lid)
            if heart and lex[key]["kind"] != "heart":
                e, _ = make_entry(key, lid, heart=True); lex[key] = e or lex[key]
        else:
            e, why = make_entry(key, lid, heart=heart, suffix_lesson=lid in SUFFIX_LESSONS)
            if not e:
                problems.append(f"{lid}: {key} -> {why}"); return None
            lex[key] = e
        if gate: gate_items.setdefault(key, {"kind": "pseudo" if gate == "pseudo" else "real", "lesson": lid})
        return key

    for n in range(1, NLESSONS[level] + 1):
        lid = f"L{level}.{n:02d}"; L = lesson_json(lid)
        heart = [h["word"] for h in L.get("heart", [])]
        for hw in heart: add(hw, lid, heart=True)
        bl = L.get("blendList") or {"real": [], "pseudo": []}
        real = [w for w in bl.get("real", []) if add(w, lid, gate="real")]
        pseudo = [w for w in bl.get("pseudo", []) if add(w, lid, gate="pseudo")]
        chk = dict(L.get("check") or {})
        if chk.get("components"):
            for c in chk["components"]:
                c["items"] = [w for w in c["items"] if add(w, lid, heart=c["kind"] == "heart", gate=None if c["kind"] == "dictation" else ("pseudo" if c["kind"] == "pseudo" else "real"))]
        else:
            chk["real"] = [w for w in chk.get("real", []) if add(w, lid, gate="real")]
            chk["pseudo"] = [w for w in chk.get("pseudo", []) if add(w, lid, gate="pseudo")]
            dic = []
            for d in chk.get("dictation", []):
                w = d if " " not in d else sentence_word(d, set(real) | set(chk["real"]))
                if w and add(w, lid): dic.append(w.lower())
            chk["dictation"] = dic
            for w in chk.get("attack", []): add(w, lid, gate="real")
        sp = L.get("spell") or {}
        spell = [w.lower() for w in sp.get("words", []) if len(w) > 2 and FULL.get(w.lower(), {}).get("kind") == "real" and add(w, lid)]
        if not spell: spell = (chk.get("dictation") or [])[:1] + real[-1:]
        for tr in ("A", "B"):
            t = ((L.get("read") or {}).get(tr) or {}).get("text") or ""
            for tok in WORD.findall(t):
                k = tok if tok == "I" else tok.lower()
                if k not in L1LEX and k not in lex and FULL.get(k, {}).get("align") and "'" not in k: add(k, lid)
        units = units_for(lid, real)
        new = [u["g"] for u in units if u["kind"] in ("grapheme", "split", "suffix") and u.get("pid") and not u.get("variant")]   # soft c, open a ...: taught on a card, not a new tile
        rule = RULES.get(lid)
        if rule:
            for w in rule[2]: add(w, lid)
        attack = [w for w in real if len(lex.get(w, {}).get("vow", [])) >= 2][:ATTACK_LESSONS.get(lid, 0)]
        if lid == "L4.14": attack = (attack + [w for w in pseudo if len(lex.get(w, {}).get("vow", [])) >= 2][:1])
        is_mastery = bool(chk.get("mastery"))
        half = max(3, len(real) // 2)
        S = {"T": {"id": "T", "new": new, "blend": {"real": real[:half], "pseudo": pseudo[:2]}, "spell": {"words": spell[:1]}},
             "D": {"id": "D", "new": [], "blend": {"real": real[half:] or real, "pseudo": pseudo[2:] or pseudo}, "spell": {"words": spell[1:3] or spell[:1]}}}
        S["TD"] = {**S["T"], "id": "TD", "spell": {"words": spell[:2]}}
        has_read, has_listen = bool((L.get("read") or {}).get("A")), bool(L.get("listen"))
        label = ", ".join(u["g"] for u in units[:6]) or None
        A, B = [], []
        if is_mastery:
            A = [{"id": "X", "steps": ["mastery"], "label": f"Level {level} check"}]; B = list(A)
        else:
            if units:
                A.append({"id": "T", "new": new, "steps": ["teach"] + (["rule"] if rule else []) + ["blend", "spell"], "mini": True, "label": label})
                d_steps = ["warm"] + (["attack"] if attack else []) + ["blend"] + (["tricky"] if heart else []) + ["spell"]
                B.append({"id": "TD", "new": new, "steps": ["teach"] + (["rule"] if rule else []) + (["attack"] if attack else []) + ["blend", "spell"] + (["tricky"] if heart else []), "keepGoing": True, "label": label})
            else:
                d_steps = ["warm"] + (["rule"] if rule else []) + (["attack"] if attack else []) + (["blend"] if real or pseudo else []) + (["tricky"] if heart else []) + (["spell"] if spell else [])
                B.append({"id": "TD", "new": [], "steps": [s for s in d_steps if s != "warm"] or ["rule"], "keepGoing": True, "label": rule[0] if rule else "Words"})
            A.append({"id": "D", "new": [], "steps": d_steps, "mini": True})
            if has_read: A.append({"id": "R", "steps": ["read"]})
            if has_listen: A.append({"id": "L", "steps": ["listen"]})
            B.append({"id": "D", "steps": ["warm"] + (["read"] if has_read else []) + (["listen"] if has_listen else [])})
            if chk.get("attack"): A.append({"id": "X", "steps": ["attackcheck"]}); B.append({"id": "X", "steps": ["attackcheck"]})
            elif chk.get("real") or chk.get("pseudo"): A.append({"id": "X", "steps": ["check"]}); B.append({"id": "X", "steps": ["check"]})
            else: problems.append(f"{lid}: no check items")
        out = {k: L[k] for k in ("id", "level", "title", "goal", "newToday", "review", "heartLine", "source", "read", "listen") if L.get(k)}
        out.update({"contentVersion": "2026.10.levels", "heart": [{"word": w, "note": next((h.get("note") for h in L.get("heart", []) if h["word"] == w), None)} for w in heart if w.lower() in lex or w in L1LEX],
                    "blendList": {"real": real, "pseudo": pseudo}, "check": chk, "sittings": [S["T"], S["D"], S["TD"]],
                    "units": units, "rule": {"title": rule[0], "text": rule[1], "examples": rule[2]} if rule else None,
                    "attack": attack, "appSittings": {"A": A, "B": B}})
        if is_mastery: out["mastery"] = True
        lessons.append(out)
    for e in lex.values():
        if e.get("syl") or e.get("prefix") or e.get("suffix"): e["chunks"] = chunks(e)
        e.pop("arpa", None)
    gpcmap = {}
    for L in lessons:
        for u in L["units"]:
            if u.get("pid") and not u.get("variant"): gpcmap[u["g"]] = u["pid"]
    return {"level": level, "lessons": lessons, "lexicon": lex, "g2p": gpcmap, "gateItems": gate_items, "ui": UI_NEW, "problems": problems}


# ------------------------------------------------------------------ audio list (rendered later, one command)
def audio_needed(level, bundle):
    import gen_audio_el as GA
    idx = json.loads((C / "audio_index.json").read_text())["clips"]
    opts_f = C / f"options_L{level}.json"
    opts = json.loads(opts_f.read_text()) if opts_f.exists() else {}
    clips, iso = {}, {}
    def word(key, ipa, spelling):
        if key in idx: return
        clips[key] = {"cut": "last", "say": spelling, "ipa": ipa}
    for k, e in bundle["lexicon"].items():
        word(f"w:{k}", e["ipa"], e["w"])
        for c in e.get("chunks", []):
            if c["ipa"] and f"syl:{c['ipa']}" not in idx: clips[f"syl:{c['ipa']}"] = {"cut": "open", "say": c["text"], "ipa": c["ipa"]}
        for pid in e["p"]:
            if pid != "_" and f"ph:{pid}" not in idx: iso[f"ph:{pid}"] = {"cut": "phone", "pid": pid, "ipa": pid_ipa(pid)}
    for o in opts.values():
        for x in [o["target"], *o["foils"]]:
            if f"ipa:{x['ipa']}" not in idx: word(f"ipa:{x['ipa']}", x["ipa"], x["w"])
    for k, t in bundle["ui"].items():
        if f"ui:{k}" not in idx: clips[f"ui:{k}"] = {"cut": "text", "text": t}
    for L in bundle["lessons"]:
        lid = L["id"]
        for u in L["units"]:
            if u.get("pid") and f"ph:{u['pid']}" not in idx: iso[f"ph:{u['pid']}"] = {"cut": "phone", "pid": u["pid"], "ipa": u["ipa"], "grapheme": u["g"]}
        if L.get("rule"): clips[f"rule:{lid}"] = {"cut": "text", "text": f"{L['rule']['title']}. {L['rule']['text']}"}
        r = L.get("read") or {}
        for tr in ("A", "B"):
            t = (r.get(tr) or {}).get("text")
            if t:
                for i, sn in enumerate(GA.sentences(t)): clips[f"read:{lid}:{tr}:{i}"] = {"cut": "text", "text": sn}
        li = L.get("listen")
        if li:
            ss = GA.sentences(li["passage"])
            if li.get("title"): clips[f"lt:{lid}:title"] = {"cut": "text", "text": li["title"] + "."}
            for i in range(0, len(ss), 2): clips[f"lt:{lid}:{i // 2}"] = {"cut": "text", "text": " ".join(ss[i:i + 2])}
            for j, t2 in enumerate(li.get("tier2", [])[:1]):
                clips[f"t2:{lid}:{j}"] = {"cut": "text", "text": f"{t2['word']}. {t2['word'][0].upper() + t2['word'][1:]} means {t2['def'][0].lower() + t2['def'][1:]}"}
            for j, q in enumerate(li.get("questions", [])[:2]): clips[f"q:{lid}:{j}"] = {"cut": "text", "text": q}
    reqs = {GA.req_text(c) for c in clips.values() if GA.req_text(c)}
    voice = json.loads((C / "voice.json").read_text())["voice_id"] if (C / "voice.json").exists() else ""
    new_reqs = {t for t in reqs if not (voice and GA.cached(voice, t))}
    by = {}
    for k, c in clips.items():
        pre = k.split(":")[0]; t = GA.req_text(c)
        by.setdefault(pre, [0, 0]); by[pre][0] += 1; by[pre][1] += len(t) if t in new_reqs else 0
    return {"level": level, "clips": clips, "iso": iso,
            "chars": sum(len(t) for t in new_reqs), "requests": len(new_reqs), "keys": len(clips),
            "byKind": {k: {"keys": v[0], "chars": v[1]} for k, v in sorted(by.items())},
            "isoSounds": len(iso),
            "render": f"python3 tools/gen_audio_el.py needed L{level}   (merges these clips into audio_plan.json, renders, builds; isolated sounds need tools/iso_sounds.py picks first)"}


def main():
    level = int(sys.argv[1])
    b = build(level)
    an = audio_needed(level, b)
    b["audioKeys"] = sorted(set(an["clips"]) | set(an["iso"]))
    (C / "levels").mkdir(exist_ok=True)
    (C / "levels" / f"L{level}.json").write_text(json.dumps(b, ensure_ascii=False, separators=(",", ":")))
    f = C / "audio_needed.json"
    allneed = json.loads(f.read_text()) if f.exists() else {}
    allneed["note"] = ("Clips the app needs and does not have yet, per level (ElevenLabs quota reserved for Level 1). The app plays a short "
                       "silent placeholder and shows 'audio coming' for each. chars = exact characters of the NEW requests "
                       "(already-cached renders excluded). Isolated sounds (iso) are listed, not rendered.")
    allneed[f"L{level}"] = an
    allneed["totalChars"] = sum(v["chars"] for k, v in allneed.items() if k.startswith("L") and isinstance(v, dict))
    f.write_text(json.dumps(allneed, indent=1, ensure_ascii=False))
    n_sit = sum(len(L["appSittings"]["A"]) for L in b["lessons"])
    print(f"L{level}: {len(b['lessons'])} lessons, {n_sit} Track A sittings, lexicon {len(b['lexicon'])}, gate items {len(b['gateItems'])}, "
          f"audio keys {an['keys']} ({an['chars']} chars, {an['requests']} requests), iso sounds {an['isoSounds']}; problems {len(b['problems'])}")
    for p in b["problems"]: print("  -", p)


if __name__ == "__main__":
    main()
