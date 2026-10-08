#!/usr/bin/env python3
"""Parse english-reading-course lesson markdown into Sound Out lesson JSON (plan-v4 §6.2, optional blocks).

Usage: python3 tools/parse_course.py [COURSE_DIR] [--levels 2,3,4]   (--levels: rewrite only those lesson JSONs)
Writes content/lessons/L<level>.<nn>.json, content/coverage.md, content/gpc.json, content/lexicon.json.
Level 1 is parsed fully; Levels 2-7 best effort (yield reported per level in coverage.md).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_args = [a for a in sys.argv[1:] if not a.startswith("--")]
LEVELS_ONLY = {int(x) for x in sys.argv[sys.argv.index("--levels") + 1].split(",")} if "--levels" in sys.argv else None
if LEVELS_ONLY: _args = [a for a in _args if a != sys.argv[sys.argv.index("--levels") + 1]]
COURSE = Path(_args[0]) if _args else ROOT.parent / "english-reading-course" / "course"
OUT = ROOT / "content"
CONTENT_VERSION = "2026.10.proto"
WORD = re.compile(r"[A-Za-z][A-Za-z']*")

# ---------- GPC sequence for Level 1 (DESIGN.md §3 master sequence) ----------
# phoneme id -> IPA (Kokoro/misaki alphabet). General American.
PHON = {"s": "s", "a": "æ", "t": "t", "p": "p", "i": "ɪ", "n": "n", "m": "m", "d": "d", "g": "ɡ",
        "o": "ɑ", "k": "k", "e": "ɛ", "u": "ʌ", "r": "ɹ", "h": "h", "b": "b", "f": "f", "l": "l",
        "j": "ʤ", "v": "v", "w": "w", "ks": "ks", "y": "j", "z": "z", "kw": "kw"}
# grapheme -> (phoneme id, lesson where taught), in teaching order
GPC_ORDER = [("s", "s", "L1.02"), ("a", "a", "L1.02"), ("t", "t", "L1.02"),
             ("p", "p", "L1.03"), ("i", "i", "L1.03"), ("n", "n", "L1.03"),
             ("m", "m", "L1.04"), ("d", "d", "L1.04"), ("g", "g", "L1.05"), ("o", "o", "L1.05"),
             ("c", "k", "L1.06"), ("k", "k", "L1.06"), ("ck", "k", "L1.06"),
             ("e", "e", "L1.07"), ("u", "u", "L1.07"), ("r", "r", "L1.08"), ("h", "h", "L1.08"),
             ("b", "b", "L1.09"), ("f", "f", "L1.09"), ("l", "l", "L1.09"),
             ("ff", "f", "L1.10"), ("ll", "l", "L1.10"), ("ss", "s", "L1.10"), ("zz", "z", "L1.10"),
             ("j", "j", "L1.11"), ("v", "v", "L1.11"), ("w", "w", "L1.11"),
             ("x", "ks", "L1.12"), ("y", "y", "L1.12"), ("z", "z", "L1.12"), ("qu", "kw", "L1.12")]
G2P = {g: p for g, p, _ in GPC_ORDER}
LETTER_NAME_IPA = {"a": "ˈeɪ", "b": "bˈi", "c": "sˈi", "d": "dˈi", "e": "ˈi", "f": "ˈɛf", "g": "ʤˈi",
                   "h": "ˈeɪʧ", "i": "ˈaɪ", "j": "ʤˈeɪ", "k": "kˈeɪ", "l": "ˈɛl", "m": "ˈɛm", "n": "ˈɛn",
                   "o": "ˈoʊ", "p": "pˈi", "q": "kjˈu", "r": "ˈɑɹ", "s": "ˈɛs", "t": "tˈi", "u": "jˈu",
                   "v": "vˈi", "w": "dˈʌbəlju", "x": "ˈɛks", "y": "wˈaɪ", "z": "zˈi"}
# Heart words L1: hand-mapped from each lesson's "Heart part" notes. heartIdx = grapheme indices
# that are the irregular part (empty = fully decodable per the course). ipa = whole-word pronunciation.
HEART = {
    "a": ([0], "ʌ"), "I": ([0], "ˈaɪ"), "the": ([0, 1, 2], "ðʌ"), "is": ([1], "ˈɪz"),
    "to": ([1], "tˈu"), "of": ([0, 1], "ˈʌv"), "and": ([], "ˈænd"), "was": ([1, 2], "wˈʌz"),
    "said": ([1, 2], "sˈɛd"), "you": ([0, 1, 2], "jˈu"), "are": ([0, 1, 2], "ˈɑɹ"), "he": ([1], "hˈi"),
    "she": ([0, 1, 2], "ʃˈi"), "we": ([1], "wˈi"), "me": ([], "mˈi"), "be": ([], "bˈi"),
    "do": ([1], "dˈu"), "what": ([0, 1, 2, 3], "wˈʌt"), "they": ([0, 1, 2, 3], "ðˈeɪ"),
    "one": ([0, 1, 2], "wˈʌn"), "have": ([3], "hˈæv"), "go": ([1], "ɡˈoʊ"), "no": ([1], "nˈoʊ"),
    "so": ([1], "sˈoʊ")}
VOWELS = {"a", "i", "o", "e", "u"}


def segment(word):
    """Greedy longest-match GPC parse. Returns (graphemes, phoneme ids) or None if a letter has no GPC."""
    w = word.lower()
    g, p, i = [], [], 0
    while i < len(w):
        two = w[i:i + 2]
        if two in G2P and len(two) == 2:
            g.append(two); p.append(G2P[two]); i += 2; continue
        if w[i] in G2P:
            g.append(w[i]); p.append(G2P[w[i]]); i += 1; continue
        return None
    # final -s reads /z/ only in "as/has/his" and plurals after a voiced consonant (L1.10); never in made-up words
    if len(p) > 1 and g[-1] == "s" and (w in {"as", "has", "his"} or (len(g) > 2 and p[-2] in {"g", "b", "d", "n", "m", "l", "v", "r"} and g[-2] != "s")):
        p[-1] = "z"
    return g, p


def ipa_of(pids):
    out, stressed = "", False
    for pid in pids:
        ph = PHON[pid]
        if pid in VOWELS and not stressed:
            out += "ˈ"; stressed = True
        out += ph
    return out


# ---------- markdown helpers ----------
def words_in(s):
    s = re.sub(r"\([^)]*\)", "", s)          # drop parentheticals
    s = s.replace("`", "").replace("*", "")
    return [m.group(0).strip("'") for m in WORD.finditer(s)]


def comma_list(s):
    s = re.sub(r"\([^)]*\)", "", s).replace("`", "").replace("*", "")
    s = s.split(". ")[0] if re.search(r"\.\s+[A-Z]", s) else s
    out = []
    for part in re.split(r"[,;]", s):
        part = part.strip().strip(".").strip('"“”').strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", part):
            out.append(part)
    return out


def label_value(text, label_re):
    """Find **Label...:** value (value may continue over wrapped lines until blank line or next **)."""
    m = re.search(r"\*\*(" + label_re + r")[^*]*?:?\*\*:?\s*(.*?)(?=\n\s*\n|\n\*\*|\n#|\n- \*\*|\Z)", text, re.S | re.I)
    return m.group(2).replace("\n", " ").strip() if m else None


def split_sections(md):
    """Split on ## / ### headings -> list of (level, title, body)."""
    parts = re.split(r"^(#{2,3}) (.*)$", md, flags=re.M)
    out = [(0, "_head", parts[0])]
    for i in range(1, len(parts), 3):
        out.append((len(parts[i]), parts[i + 1].strip(), parts[i + 2]))
    return out


def blockquote(body):
    lines = [l[1:].strip() for l in body.splitlines() if l.startswith(">")]
    return lines


def numbered(body):
    items, cur = [], None
    for l in body.splitlines():
        m = re.match(r"\s*(\d+)[.)]\s+(.*)", l)
        if m:
            if cur: items.append(cur)
            cur = m.group(2).strip()
        elif cur is not None and l.startswith("   ") and l.strip():
            cur += " " + l.strip()
        elif cur is not None and not l.strip():
            items.append(cur); cur = None
    if cur: items.append(cur)
    return [re.sub(r"\*", "", x) for x in items]


def parse_bar(s):
    if not s: return None
    m = re.search(r"≥\s*(\d+)\s*/\s*(\d+)", s) or re.search(r"(\d+)\s*/\s*(\d+)\s*(?:=\s*pass|correct|or better)", s) \
        or re.search(r"\b(\d+)\s+of\s+(\d+)\b", s)
    if m:
        return {"pass": int(m.group(1)), "of": int(m.group(2)), "source": "lesson", "raw": m.group(0)}
    m = re.search(r"≥\s*(\d+)\s*%", s)
    if m:
        return {"ratio": int(m.group(1)) / 100, "source": "lesson", "raw": m.group(0)}
    return None


def parse_tier2(body):
    out = []
    for m in re.finditer(r"^- \*\*([^*]+)\*\*\s*[—–-]\s*(.*?)(?=\n- \*\*|\n\s*\n|\Z)", body, re.S | re.M):
        text = m.group(2).replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        definition = re.split(r'(?<=[.!?])\s+["“]', text)[0].strip()
        out.append({"word": m.group(1).strip(), "def": definition, "full": text})
    return out


def parse_listen(body):
    lines = blockquote(body)
    if not lines: return None
    title = None
    if lines and re.fullmatch(r"\*\*.+\*\*", lines[0]):
        title = lines[0].strip("*"); lines = lines[1:]
    passage = re.sub(r"\s+", " ", " ".join(lines)).strip()
    if len(passage) < 40: return None
    qs = []
    m = re.search(r"\*\*Discussion questions?:?\*\*:?(.*)", body, re.S | re.I)
    if m: qs = numbered(m.group(1))
    t2 = parse_tier2(body)
    return {"title": title, "passage": passage, "tier2": t2, "questions": qs[:3]}


def parse_listen_inline(body):
    """Levels 3-4 Listen & Talk: the passage is a quotation inside the paragraph, not a blockquote."""
    b = re.sub(r"\s+", " ", body)
    m = re.search(r'Read (?:aloud|this)[^"“]*["“](.+?)["”]\*?\s*(?=\*?\*?Tier|Tier|$)', b) or re.search(r'["“](.{60,}?)["”]', b)
    if not m: return None
    passage = m.group(1).replace("**", "").replace("*", "").strip()
    t2 = []
    tm = re.search(r"Tier-2 word:\s*(?:\*\*)?([A-Za-z' -]+?)\*\*\s*[—–-]\s*friendly definition:?\s*[\"“]([^\"”]+)", b)
    if tm: t2 = [{"word": tm.group(1).strip(), "def": tm.group(2).strip(), "full": tm.group(2).strip()}]
    qs = []
    qm = re.search(r"(?:Discussion|Discuss)[^:]*:\*?\s*(.*)", b)
    if qm:
        qs = [q.strip() + "?" for q in re.split(r"\?", re.sub(r"\d\)\s*", "", qm.group(1))) if len(q.strip()) > 8][:2]
    return {"title": None, "passage": passage, "tier2": t2, "questions": qs}


def parse_read(body):
    res = {}
    # Track A / B text: blockquote after a "Track A"/"Track B" marker
    chunks = re.split(r"(?:^|\n)(?:#{3,4} |\*\*)(Track [AB][^\n]*)", body)
    if len(chunks) > 1:
        for i in range(1, len(chunks), 2):
            label, txt = chunks[i], chunks[i + 1]
            q = blockquote(txt)
            if not q: continue
            text = re.sub(r"\s+", " ", " ".join(q)).strip()
            title = None
            m = re.match(r"\*\*(.+?)\*\*\s*(.*)", text)
            if m: title, text = m.group(1), m.group(2)
            if "Track A" in label and "Track B" in label:
                res["A"] = {"text": text, "title": title}; res["B"] = {"sameAsA": True}
            elif "Track A" in label and "A" not in res:
                res["A"] = {"text": text, "title": title}
            elif "Track B" in label and "B" not in res:
                res["B"] = {"text": text, "title": title}
    m = re.search(r"\*\*(?:Questions|Comprehension)[^*]*\*\*:?(.*)", body, re.S)
    if m: res["questions"] = numbered(m.group(1))[:3]
    return res or None


def parse_check(body):
    def grab(pat):
        v = label_value(body, pat)
        if v: return v
        m = re.search(r"(?im)^\s*(?:- )?(?:\d+ )?(?:" + pat + r")[^:\n]*:\s*(.*)$", body)
        return m.group(1) if m else None
    real = grab(r"Real")
    pseudo = grab(r"Pseudo")
    dict_ = grab(r"Dictat")
    if real and re.search(r"Pseudo", real):
        parts = re.split(r"\.\s+Pseudo[^:]*:\s*", real)
        real = parts[0]
        if len(parts) > 1:
            rest = re.split(r"\.\s+Dictat[^:]*:\s*", parts[1]); pseudo = rest[0]
            if len(rest) > 1: dict_ = rest[1]
    c = {}
    if real:
        real = re.split(r"\.\s+Pseudo", real)[0]
        c["real"] = comma_list(real)
    if pseudo: c["pseudo"] = comma_list(pseudo)
    if dict_:
        dict_ = dict_.replace("*", "").replace("`", "").strip()
        d = dict_.strip().strip('"“”').split('"')[0] if dict_.strip().startswith('"') else dict_
        c["dictation"] = [w for w in comma_list(d)] or [re.sub(r'["“”.]', "", d).strip()]
    bar = parse_bar(body)
    if bar: c["bar"] = bar
    else:
        c["bar"] = {"ratio": 0.9, "source": "default", "raw": None}
    c["firstAttemptOnly"] = True
    return c if (c.get("real") or c.get("pseudo")) else ({"bar": c["bar"], "freeResponse": True} if bar else None)


def parse_head(head):
    h = {}
    for key, lab in [("goal", "Goal"), ("newToday", "New today"), ("review", "Review"), ("heartLine", "Heart words"), ("time", "Time")]:
        v = label_value(head, re.escape(lab))
        if v: h[key] = re.sub(r"\s+", " ", v)
    return h


def heart_list(line):
    if not line: return []
    line = re.sub(r"\([^)]*\)", "", line)
    line = re.split(r"(?i)review|none", line)[0]
    return [w for w in words_in(line) if w.lower() in {k.lower() for k in HEART} or len(w) <= 8][:4] if line.strip() else []


def parse_sitting(sid, title, body):
    s = {"id": sid, "title": title.strip()}
    m = re.match(r"([^(]*?)\s*(?:\(|$)", title)
    head = m.group(1).strip() if m else title
    if "together" not in head.lower() and "review" not in head.lower():
        s["new"] = [g.strip() for g in re.split(r"[,\s]+", head) if g.strip() and re.fullmatch(r"[a-z]{1,3}", g.strip())]
    else:
        s["new"] = []
    warm = label_value(body, r"Warm-up")
    if warm:
        s["warm"] = {"text": warm}
        m = re.search(r"[Rr]ead \d+ review words?:\s*(.*)", warm) or re.search(r"words?(?: spanning[^:]*)?:\s*(.*)", warm)
        if m: s["warm"]["words"] = comma_list(m.group(1))
    hear = label_value(body, r"Hear it")
    if hear: s["hear"] = {"text": hear}
    meet = label_value(body, r"Meet it")
    if meet:
        mc = re.search(r"\*\*Mouth cue:\*\*\s*(.*?)(?=\*\*|\n\s*\n|\Z)", body, re.S)
        s["meet"] = {"text": meet, "mouthCue": re.sub(r"\s+", " ", mc.group(1)).strip() if mc else None}
    blend = None
    bl = re.search(r"\*\*Blend it[^*]*\*\*:?\s*(.*?)(?=\n\s*\n\*\*|\n\*\*Spell|\Z)", body, re.S)
    if bl:
        txt = bl.group(1)
        real = label_value(body, r"Real words") ; pseudo = label_value(body, r"Pseudowords")
        tab = re.findall(r"^\|\s*([a-z ,]+?)\s*\|\s*([a-z ,]+?)\s*\|\s*$", body, re.M)
        if tab:
            blend = {"real": comma_list(tab[-1][0]), "pseudo": comma_list(tab[-1][1])}
        elif real or pseudo:
            blend = {"real": comma_list(real or ""), "pseudo": comma_list(pseudo or "")}
        else:
            first = txt.split("\n\n")[0].replace("\n", " ")
            if "not yet possible" in first.lower() or "not applicable" in first.lower():
                blend = {"real": [], "pseudo": [], "note": "not yet possible"}
            else:
                lst = first.split(":", 1)[-1] if ":" in first and "**" not in first.split(":", 1)[-1][:3] else first
                blend = {"real": comma_list(lst), "pseudo": []}
                # "practice syllable" (L1.02 B "sa")
                ps = re.search(r'into "(\w+)', first)
                if ps and not blend["real"]: blend = {"real": [], "pseudo": [], "syllable": ps.group(1)}
    if blend: s["blend"] = blend
    sp = label_value(body, r"Spell it")
    spell = {}
    if sp:
        spell["text"] = sp
        ws = re.findall(r'"(\w+)[,.]?"', sp)
        spell["words"] = ws
    sent = re.search(r'Sentence dictation:\s*\*\*"?([^*"]+)"?\*\*', body)
    if sent: spell["sentence"] = sent.group(1).strip()
    segs = re.search(r'Segment and write:\s*(.*)', body)
    if segs and not spell.get("words"): spell["words"] = re.findall(r'"(\w+)', segs.group(1))
    if spell: s["spell"] = spell
    mini = label_value(body, r"Mini check")
    if mini:
        s["mini"] = {"text": mini, "bar": parse_bar(mini)}
    hw = re.search(r"\*\*Heart word\(s\)[^*]*\*\*(.*?)(?=\n#|\Z)", body, re.S)
    if hw:
        s["heart"] = [{"word": m.group(1), "note": re.sub(r"\s+", " ", m.group(2)).strip()}
                      for m in re.finditer(r"^- \*\*(\w+)\*\*\s*[—–-]\s*(.*?)(?=\n- \*\*|\n\s*\n|\Z)", hw.group(1), re.S | re.M)]
    return s


# ---------- Levels 2-4 (course pass: Levels 2-4 made playable) ----------
CANON_HEART = {  # DESIGN.md §3, CANONICAL schedule (tools/decodable.py enforces it); Level 4 adds none
    "L2.01": ["says", "for"], "L2.02": ["there", "where"], "L2.03": ["were", "from"], "L2.04": ["come", "some"],
    "L2.05": ["done", "want"], "L2.06": ["put", "push"], "L2.07": ["pull", "full"], "L2.08": ["who", "could"],
    "L2.09": ["would", "should"], "L2.10": ["your", "four"], "L2.11": ["many", "any", "her"], "L2.12": ["does", "goes", "two"],
    "L2.13": ["again", "friend", "because"],
    "L3.01": ["once", "only"], "L3.02": ["very", "every"], "L3.03": ["great", "eye"], "L3.04": ["busy", "people"],
    "L3.05": ["water", "laugh"], "L3.06": ["walk", "talk"], "L3.07": ["buy", "answer"], "L3.08": ["whole", "earth"]}
# Check steps whose items sit in prose, not in Real:/Pseudo: lists (read from the lesson text, by hand)
CHECK_FIX = {
    "L3.04": {"real": ["hoping", "saving", "closing", "riding", "making"], "dictation": ["hoping", "saving", "closing", "riding", "making"],
              "bar": {"pass": 9, "of": 10, "source": "lesson", "raw": "9/10 across writing+reading"}, "firstAttemptOnly": True,
              "note": "learner writes the -ing form (dictation) and reads it (tap gate)"},
    "L3.15": {"real": ["moon", "book", "soon", "hook", "cool"], "pseudo": ["sproom", "blook", "twood", "froon", "gloot"], "dictation": ["look"],
              "bar": {"ratio": 0.9, "source": "lesson", "raw": "≥90%"}, "firstAttemptOnly": True,
              "note": "dictated sentence 'I took a good look at the book.' -> the app dictates 'look'; flex narration is self-report"},
    "L4.15": {"real": [], "pseudo": [], "attack": ["comfortable", "dangerous", "ingredients"], "bar": {"pass": 2, "of": 3, "source": "lesson", "raw": "2 of 3"},
              "freeResponse": True, "note": "unknown-word protocol narrated on 3 words: the app runs the word-attack routine, self-report per word"},
}
MASTERY_LESSON = {"L2.14", "L3.18", "L4.16"}


def extract_words(txt):
    """Words from course word lists: backtick/comma/· lists, arrows (hope→hoping) count both sides."""
    t = re.sub(r"\([^()]*\)", "", txt).replace("→", ",").replace("·", ",").replace("*", "").replace("`", ",")
    out = []
    for m in re.finditer(r"(?:^|[:,;])\s*([a-z][a-z']*)\s*(?=[,.;]|$)", t, re.M):
        w = m.group(1)
        if w not in out: out.append(w)
    return out


def blend_lists(body):
    parts = re.split(r"(?im)^\s*(?:\*\*)?pseudo", body, maxsplit=1)
    real = extract_words(parts[0])
    pseudo = extract_words("Pseudo" + parts[1]) if len(parts) > 1 else []
    return {"real": real[:40], "pseudo": [w for w in pseudo if w not in real][:12]}


def spell_block(body):
    b = body.replace("*", "")
    m = re.search(r"(?is)\bwords?\s*(?:\([^)]*\))?:?\s*(.*?)(?=\n?\s*\d[.)]|sentence|\Z)", b)
    words = extract_words(":" + m.group(1)) if m else []
    if not words:
        words = re.findall(r"\d\)\s*([a-z]+)\b(?!\s*[a-z])", b)
    sent = re.search(r'"([A-Z][^"]+)"', b)
    return {"words": words[:6], **({"sentence": sent.group(1)} if sent else {})}


def parse_mastery(level):
    """Level mastery instrument (course/level-N/mastery-check.md) -> components the app scores (tap gate / spell);
    passage reading, prosody and narration stay with the tutor (listed as offline components)."""
    md = (COURSE / f"level-{level}" / "mastery-check.md").read_text()
    sec = lambda pat: (re.search(pat + r".*?(?=\n## |\Z)", md, re.S | re.I) or [""])[0]
    def items(block, skip=1):
        lines = block.split("\n")[skip:]
        txt = "\n".join(l for l in lines if not re.match(r"\s*\*\*|\s*\*\(|\s*\(|\s*Flash|\s*Label|\s*\(any|\s*Have|\s*Read each", l))
        return extract_words(":" + txt.strip().split("\n\n")[0])
    comps = []
    def add(cid, label, kind, ws, p, of):
        comps.append({"id": cid, "label": label, "kind": kind, "items": ws, "bar": {"pass": p, "of": of, "source": "mastery-check.md"}})
    if level == 2:
        add("real", "Real words", "real", items(sec(r"## Component 1")), 26, 28)
        add("pseudo", "Alien words", "pseudo", items(sec(r"## Component 2")), 11, 12)
        add("heart", "Heart words", "heart", items(sec(r"## Component 4")), 27, 29)
        add("dictation", "Spelling", "dictation", ["catches", "helped", "sunset"], 2, 3)
        offline = ["Decoding passage (read aloud with the tutor)", "Comprehension (3 questions, with the tutor)"]
    elif level == 3:
        add("heart", "Heart words", "heart", items(sec(r"## 1\. Heart"), 3), 14, 16)
        real = re.findall(r"([a-z]+) \([^)]*\)\s*(?=·|$)", sec(r"## 2\. Real").split("\n", 1)[1], re.M)
        # the instrument says "31 items listed" but lists 32 and scores "≥90%": the app uses all 32 at the 90% band (29/32)
        add("real", "Real words", "real", real, -(-9 * len(real) // 10), len(real))
        add("pseudo", "Alien words", "pseudo", items(sec(r"## 3\. Pseudo"), 2), 9, 10)
        add("dictation", "Spelling", "dictation", ["plane", "smile", "close", "baby", "page", "train", "coat", "blue"], 7, 8)
        offline = ["Connected-text reading (WCPM + phrasing, with the tutor)", "Comprehension 3/3", "Flex-decode narration"]
    else:
        real = re.findall(r"^\| \d+ \| (\w+) \|", md, re.M)
        add("real", "Real words", "real", real, 14, 16)
        ital = lambda b: extract_words(":" + (re.search(r"\n\*([a-z][a-z,\s]+)\*", b) or [""])[0].replace("\n", " "))
        add("pseudo", "Alien words", "pseudo", ital(sec(r"## Section 2")), 9, 10)
        add("multi_pseudo", "Long alien words", "pseudo", ital(sec(r"## Section 3")), 7, 8)
        add("multi_real", "Long real words", "real", ital(sec(r"## Section 4")), 9, 10)
        add("dictation", "Spelling", "dictation", ["yard", "store", "shirt", "square", "join", "town", "wall", "hoping", "running", "happier"], 8, 10)
        offline = ["Authentic passage + unknown-word protocol (with the tutor)", "Fluency reading (WCPM + prosody)"]
    for c in comps:   # the stated denominators must match the parsed lists (else the instrument changed: fail loudly)
        if len(c["items"]) != c["bar"]["of"]:
            raise SystemExit(f"L{level} mastery {c['id']}: parsed {len(c['items'])} items, instrument says {c['bar']['of']}: {c['items']}")
    return {"mastery": True, "components": comps, "offline": offline,
            "bar": {"ratio": 0.9, "source": "mastery-check.md", "raw": "every component at its threshold"}, "firstAttemptOnly": True}


def parse_lesson(path):
    md = path.read_text()
    lid = re.match(r"(L\d)\.(\d+)", path.name)
    level, num = int(lid.group(1)[1]), int(lid.group(2))
    lesson = {"id": f"L{level}.{num:02d}", "level": level, "contentVersion": CONTENT_VERSION,
              "source": str(path.relative_to(COURSE.parent))}
    t = re.search(r"^# (.*)$", md, re.M)
    lesson["title"] = t.group(1).split("—", 1)[-1].strip() if t else path.stem
    secs = split_sections(md)
    lesson.update(parse_head(secs[0][2]))
    found = []
    sittings = []
    for lvl, title, body in secs[1:]:
        tl = title.lower()
        m = re.match(r"Sitting ([A-Z])\s*[—–-]\s*(.*)", title)
        if m:
            sittings.append(parse_sitting(m.group(1), m.group(2), body)); continue
        if re.search(r"\bread it\b|^track [ab]", tl) or (re.search(r"fluency & knowledge|close reading|knowledge text", tl)):
            r = parse_read(body + "".join(b for l2, t2, b in secs if t2.lower().startswith("track")))
            if r and "read" not in lesson: lesson["read"] = r
        if "listen & talk" in tl or "listen and talk" in tl:
            li = parse_listen(body) or (parse_listen_inline(body) if level >= 3 else None)
            if li: lesson["listen"] = li
        if re.search(r"(^|\d\.\s*|\s)check\b", tl) and "mini" not in tl and "fluency" not in tl and "self" not in tl:
            c = parse_check(body)
            if c: lesson["check"] = c
        if re.match(r"(\d\.\s*)?blend it", tl):
            if level >= 2:
                b = blend_lists(body)      # Levels 2-4: split at the Pseudowords label, words from every list (decision: course pass)
            else:
                b = {"real": comma_list(label_value(body, r"Real") or ""), "pseudo": comma_list(label_value(body, r"Pseudo") or "")}
                if not b["real"]:
                    b["real"] = [w for line in body.splitlines() if ":" in line for w in comma_list(line.split(":", 1)[1])][:20]
            if b["real"] or b["pseudo"]: lesson["blendList"] = b
        if level >= 2 and re.match(r"(\d\.\s*)?spell it", tl):
            sp = spell_block(body)
            if sp: lesson["spell"] = sp
        if re.match(r"(\d\.\s*)?heart word", tl):
            hs = [{"word": m.group(1), "note": re.sub(r"\s+", " ", m.group(2)).strip()}
                  for m in re.finditer(r"^- \*\*(\w+)\*\*\s*[—–-]\s*(.*?)(?=\n- \*\*|\n\s*\n|\Z)", body, re.S | re.M)]
            if hs: lesson["heart"] = hs
        if "tier-2" in tl or "tier 2" in tl:
            t2 = parse_tier2(body)
            if t2: lesson.setdefault("tier2", t2)
    # Track A/B can sit in the head of a sitting section (L1 style: "### 7. Read it" after Sitting D)
    if sittings:
        lesson["sittings"] = sittings
        # Lesson-level blend list and heart words for L1 live inside the final sitting
        last = sittings[-1]
        for s in sittings:
            if s.get("heart") and "heart" not in lesson: lesson["heart"] = s["heart"]
        if "blendList" not in lesson:
            for s_ in reversed(sittings):
                b_ = s_.get("blend") or {}
                if b_.get("real") or b_.get("pseudo"):
                    lesson["blendList"] = {"real": b_.get("real", []), "pseudo": b_.get("pseudo", [])}; break
        if "check" not in lesson:
            for lvl, title, body in secs:
                if title.startswith("Sitting") and re.search(r"\*\*Real \(", body):
                    c = parse_check(body.split("9. Check")[-1]); 
                    if c: lesson["check"] = c
    # Levels 2-4: the CANONICAL heart-word schedule (DESIGN.md §3) decides, notes kept where the lesson has them
    if 2 <= level <= 4:
        notes = {h["word"].lower(): h.get("note") for h in lesson.get("heart", [])}
        lesson["heart"] = [{"word": w, "note": notes.get(w)} for w in CANON_HEART.get(lesson["id"], [])]
        if not lesson["heart"]: del lesson["heart"]
        fix = CHECK_FIX.get(lesson["id"])
        if fix: lesson["check"] = fix
        if lesson["id"] in MASTERY_LESSON:
            lesson["check"] = parse_mastery(level)
    # heart word list from header if notes not found
    hl = lesson.get("heartLine", "")
    if "heart" not in lesson and hl and not re.match(r"(?i)none|cumulative", hl) and not 2 <= level <= 4:
        lesson["heart"] = [{"word": w, "note": None} for w in words_in(re.split(r"\(", hl)[0])
                           if w.lower() not in {"taught", "in", "the", "final", "review", "new"}][:4]
    # where Read-it lives under Sitting D (L1.02 style) parse it from full text
    if "read" not in lesson:
        m = re.search(r"#{2,3} (?:7\. )?Read it.*?(?=\n#{2,3} (?:8\.|Listen)|\Z)", md, re.S)
        if m:
            r = parse_read(m.group(0))
            if r: lesson["read"] = r
    if "listen" not in lesson:
        m = re.search(r"#{2,3} (?:8\. )?Listen & Talk.*?(?=\n#{2,3} (?:9\.|Check)|\Z)", md, re.S)
        if m:
            li = parse_listen(m.group(0))
            if li: lesson["listen"] = li
    if "check" not in lesson:
        m = re.search(r"#{2,3} (?:\d\. )?Check.*?(?=\n---|\n#{2,3} Tutor|\Z)", md, re.S)
        if m:
            c = parse_check(m.group(0))
            if c: lesson["check"] = c
    # blocks found
    for k in ["sittings", "blendList", "heart", "read", "listen", "check"]:
        if lesson.get(k): found.append(k)
    if lesson.get("read", {}).get("B"): found.append("trackB")
    if lesson.get("listen", {}).get("tier2"): found.append("tier2")
    lesson["blocksFound"] = found
    lesson["appSittings"] = app_sittings(lesson)
    return lesson


def app_sittings(lesson):
    """Map course sittings onto app step lists (plan-v4 §3.2). Track B merges teaching sittings."""
    ss = lesson.get("sittings")
    if not ss: return None
    A = []
    for s in ss:
        steps = []
        if s.get("warm") and s["id"] != "A": steps.append("warm")
        if s.get("new"):
            steps += ["hear", "meet", "trace"]
        b = s.get("blend") or {}
        if b.get("real") or b.get("pseudo") or b.get("syllable"):
            steps.append("blend")
        if s.get("heart"): steps.append("tricky")
        if s.get("spell") and (s["spell"].get("words") or s.get("new")): steps.append("spell")
        if not s.get("new"):
            steps = ["warm", "blend"] + (["tricky"] if s.get("heart") else []) + ["spell"]
        A.append({"id": s["id"], "new": s.get("new", []), "steps": steps, "mini": True})
    A.append({"id": "R", "steps": ["read"]}); A.append({"id": "L", "steps": ["listen"]}); A.append({"id": "X", "steps": ["check"]})
    teach = [s for s in A if s.get("new")]
    B = [{"id": "".join(s["id"] for s in teach), "new": [g for s in teach for g in s["new"]],
          "steps": ["hear", "meet", "trace", "blend", "spell"], "keepGoing": True}] if teach else []
    B.append({"id": "D", "steps": ["warm", "tricky", "read", "listen"]}); B.append({"id": "X", "steps": ["check"]})
    return {"A": A, "B": B}


def main():
    files = sorted(COURSE.glob("level-*/lessons/L*.md"))
    if LEVELS_ONLY:   # --levels 2,3,4: rewrite ONLY those lesson files (lexicon.json / gpc.json / coverage.md belong to Level 1 + build_lexicon.py)
        for f in files:
            if int(f.name[1]) in LEVELS_ONLY:
                L = parse_lesson(f)
                (OUT / "lessons" / f"{L['id']}.json").write_text(json.dumps(L, indent=1, ensure_ascii=False))
                print(L["id"], L["blocksFound"], {k: len(v) for k, v in (L.get("blendList") or {}).items()}, [h["word"] for h in L.get("heart", [])])
        return
    lessons = []
    for f in files:
        L = parse_lesson(f)
        (OUT / "lessons" / f"{L['id']}.json").write_text(json.dumps(L, indent=1, ensure_ascii=False))
        lessons.append(L)
    # gpc.json
    gpc = [{"g": g, "p": p, "ipa": PHON[p], "lesson": les, "name": LETTER_NAME_IPA.get(g) if len(g) == 1 else None}
           for g, p, les in GPC_ORDER]
    (OUT / "gpc.json").write_text(json.dumps({"order": gpc, "phonemes": PHON, "letterNames": LETTER_NAME_IPA}, indent=1, ensure_ascii=False))
    # lexicon for Level 1
    lex, unseg = {}, []
    def add(w, kind, lesson):
        if not w: return
        key = w if w == "I" else w.lower()
        if key in lex:
            lex[key]["lessons"] = sorted(set(lex[key]["lessons"] + [lesson])); return
        if key in HEART or (key.capitalize() == "I" and key == "i" and False):
            pass
        if w in HEART or key in HEART:
            hw = w if w in HEART else key
            idx, ipa = HEART[hw]
            seg = segment(hw.lower()) or ([c for c in hw.lower()], [])
            lex[key] = {"w": hw, "g": seg[0], "p": seg[1] if seg[1] else None, "ipa": ipa, "kind": "heart", "heartIdx": idx, "lessons": [lesson]}
            return
        seg = segment(key)
        if seg and kind == "pseudo" and seg[1][-1] == "z" and seg[0][-1] == "s":
            seg[1][-1] = "s"
        if not seg:
            unseg.append((w, lesson)); return
        lex[key] = {"w": key, "g": seg[0], "p": seg[1], "ipa": ipa_of(seg[1]), "kind": "syllable" if key == "sa" else kind, "lessons": [lesson]}
    for L in lessons:
        if L["level"] != 1: continue
        lid = L["id"]
        for h in L.get("heart", []): add(h["word"], "heart", lid)
        for s in L.get("sittings", []):
            b = s.get("blend") or {}
            for w in b.get("real", []): add(w, "real", lid)
            for w in b.get("pseudo", []): add(w, "pseudo", lid)
            for w in (s.get("warm") or {}).get("words", []): add(w, "real", lid)
            for w in (s.get("spell") or {}).get("words", []): add(w, "real", lid)
        bl = L.get("blendList") or {}
        for w in bl.get("real", []): add(w, "real", lid)
        for w in bl.get("pseudo", []): add(w, "pseudo", lid)
        c = L.get("check") or {}
        for w in c.get("real", []): add(w, "real", lid)
        for w in c.get("pseudo", []): add(w, "pseudo", lid)
        for w in c.get("dictation", []):
            for x in words_in(w): add(x if x == "I" else x.lower(), "real", lid)
        r = L.get("read") or {}
        for tr in ("A", "B"):
            for x in words_in((r.get(tr) or {}).get("text", "") or ""):
                add(x if x == "I" else x.lower(), "real", lid)
    (OUT / "lexicon.json").write_text(json.dumps(lex, indent=1, ensure_ascii=False))
    # coverage.md
    rows = ["# Content coverage (generated by tools/parse_course.py)", "",
            f"{len(lessons)} lesson files parsed from `{COURSE}`. Blocks: S=sittings, B=blend list, H=heart words, "
            "R=read (Track A), TB=Track B, LT=Listen & Talk passage, T2=Tier-2 words, C=check items. "
            "**Yield** = lesson whose check items AND bar parsed unaided (plan-v4 §6.2 week-1 exit).", ""]
    for lv in range(1, 8):
        ls = [L for L in lessons if L["level"] == lv]
        y = [L for L in ls if (L.get("check") or {}).get("real") and (L.get("check") or {}).get("bar", {}).get("source") == "lesson"]
        rows.append(f"## Level {lv}: yield {len(y)}/{len(ls)}")
        rows.append("")
        rows.append("| Lesson | Title | S | B | H | R | TB | LT | T2 | C real/pseudo/dict | Bar (as stated) | Words |")
        rows.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for L in ls:
            c = L.get("check") or {}
            f_ = L["blocksFound"]
            yes = lambda k: "✓" if k in f_ else "·"
            nw = len(set((L.get("blendList") or {}).get("real", []) + c.get("real", [])))
            bar = (c.get("bar") or {})
            bars = (f"{bar.get('pass')}/{bar.get('of')}" if bar.get("pass") else (f"≥{int(bar['ratio']*100)}%" if bar.get("ratio") else "—"))
            if bar.get("source") == "default": bars = "none → default 90%"
            if c.get("freeResponse"): bars += " (free response)"
            rows.append(f"| {L['id']} | {L['title'][:40]} | {len(L.get('sittings', [])) or '·'} | {yes('blendList')} | {yes('heart')} | {yes('read')} | {yes('trackB')} | {yes('listen')} | {yes('tier2')} | "
                        f"{len(c.get('real', []))}/{len(c.get('pseudo', []))}/{len(c.get('dictation', []))} | {bars} | {nw} |")
        rows.append("")
    rows.append(f"## Level 1 lexicon\n\n{len(lex)} entries; unsegmentable (letters outside the L1 GPC set, skipped): "
                + (", ".join(f"{w} ({l})" for w, l in unseg) or "none"))
    (OUT / "coverage.md").write_text("\n".join(rows) + "\n")
    print(f"parsed {len(lessons)} lessons; lexicon {len(lex)}; unsegmentable {len(unseg)}")
    # Levels 5-7 use the session template (warm-up, word work, fluency, prime, knowledge text, discussion, write, check):
    # the Level 1-4 blocks above find no learner words there, so tools/parse_sessions.py parses them for the practice screens.
    import parse_sessions; parse_sessions.main(COURSE)


if __name__ == "__main__":
    main()
