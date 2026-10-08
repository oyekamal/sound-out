#!/usr/bin/env python3
"""Parse the Level 5-7 SESSION-TEMPLATE lessons (english-reading-course) into Sound Out practice JSON.

Usage: python3 tools/parse_sessions.py [COURSE_DIR] [--levels 5,6,7]
Also called from tools/parse_course.py.

Session template (DESIGN.md §4): Retrieval warm-up · Word work (morphology / vocabulary) · Fluency or
close reading · Prime the topic · Knowledge text + discussion (reciprocal roles, Support/Challenge) ·
Write to read · Check. Level 5 puts Track A / Track B passages inside "Fluency & Knowledge Text";
Level 6 has a short phrase-cued fluency passage then one long knowledge text with Stop-and-check items;
Level 7 has "Meet the move" + one or more close-reading sources and a model-answer Check.

Writes content/sessions/L<l>.<nn>.json, content/sessions/index.json, content/audio_needed_l5_7.json and
the "Levels 5-7 session blocks" section of content/coverage.md (between markers, rest untouched).
L5+ ship as PRACTICE (plan-v6): nothing here is a gate; free-response checks are self-checked.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content"
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*[A-Za-z]|[A-Za-z]")
SCREENS = ["warm", "word", "fluency", "prime", "text", "discuss", "write", "check"]
ROLES = ["Predictor", "Questioner", "Clarifier", "Summarizer"]
# Role cards as worded in course L6.05 ("GUIDED -> INDEPENDENT"), used where a lesson says "run all four roles alone".
DEFAULT_ROLES = [
    {"role": "Predictor", "prompt": "Before you read a paragraph, glance at its first sentence. Say what you think it will tell you, in one sentence.", "model": None},
    {"role": "Questioner", "prompt": "After you read a paragraph, ask one real question about it, not a question you already know the answer to. A good question usually starts with why, how, or what would happen if.", "model": None},
    {"role": "Clarifier", "prompt": "Find one word or one sentence in the paragraph that felt confusing or unclear. Say what confused you, then work out what it means using the words around it.", "model": None},
    {"role": "Summarizer", "prompt": "Say the paragraph's main point in one sentence, in your own words.", "model": None}]


# ---------- text helpers ----------
def clean(s):
    """Markdown -> plain learner text."""
    s = re.sub(r"`([^`]*)`", r"\1", s or "")
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\1", s)
    s = s.replace("**", "").replace("\\", "")
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def unslash(s):
    """Phrase-cued text 'a / b / c' -> 'a b c'."""
    return re.sub(r"\s*/\s*", " ", s).replace("  ", " ").strip()


def words(s):
    return [w.strip("'’-").lower() for w in WORD.findall(s or "")]


def sections(md, level=2):
    """Split on headings of exactly `level` hashes -> [(title, body)]."""
    parts = re.split(r"^" + "#" * level + r" (.*)$", md, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def subsections(body):
    parts = re.split(r"^### (.*)$", body, flags=re.M)
    return [("_lead", parts[0])] + [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def quote_paragraphs(body):
    """Blockquote lines -> paragraphs (a blank '>' line or a gap ends a paragraph)."""
    paras, cur = [], []
    for l in body.splitlines() + [""]:
        if l.startswith(">"):
            t = l[1:].strip()
            if t: cur.append(t)
            elif cur: paras.append(" ".join(cur)); cur = []
        elif cur:
            paras.append(" ".join(cur)); cur = []
    return paras


def numbered(body):
    items, cur = [], None
    for l in body.splitlines():
        m = re.match(r"\s{0,3}(\d+)[.)]\s+(.*)", l)
        if m:
            if cur is not None: items.append(cur)
            cur = m.group(2).strip()
        elif cur is not None and l.strip() and (l.startswith("  ") or not re.match(r"\s*([-*>#|]|\*\*)", l)):
            cur += " " + l.strip()
        elif cur is not None and not l.strip():
            items.append(cur); cur = None
    if cur is not None: items.append(cur)
    return items


def bullets(body):
    items, cur = [], None
    for l in body.splitlines():
        m = re.match(r"\s{0,2}[-*]\s+(.*)", l)
        if m:
            if cur is not None: items.append(cur)
            cur = m.group(1).strip()
        elif cur is not None and l.startswith("  ") and l.strip():
            cur += " " + l.strip()
        elif cur is not None:
            items.append(cur); cur = None
    if cur is not None: items.append(cur)
    return items


def plain_paragraphs(body):
    """Paragraphs that are ordinary prose (not quote, list, table, heading)."""
    out = []
    for p in re.split(r"\n\s*\n", body):
        p = p.strip()
        if not p or re.match(r"([>|#]|[-*]\s|\d+[.)]\s|```)", p): continue
        out.append(clean(p))
    return out


def sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.!?…])[\"”’]?\s+(?=[\"“‘(]?[A-Z0-9])", p) if s.strip()]


def first_quoted(s):
    m = re.search(r"[\"“]([^\"”]{8,})[\"”]", s)
    return m.group(1).strip() if m else None


# ---------- blocks ----------
def parse_warm(body):
    words_ = []
    for m in re.finditer(r"(?<![\w*])\*([^*]{2,200}?)\*(?![\w*])", body):
        chunk = m.group(1)
        if re.search(r"[.!?]$", chunk.strip()) or len(chunk.split()) > 14: continue
        for w in re.split(r",\s*|\s+and\s+|\s*/\s*", chunk):
            w = w.strip(" .;:")
            if w and re.fullmatch(r"[A-Za-z][A-Za-z'’ -]{0,30}", w) and len(w.split()) <= 3: words_.append(w)
    heart = []
    m = re.search(r"Heart words?[^:]*:\s*\*\*([^*]+)\*\*", body)
    if m: heart = [w.strip(" .") for w in m.group(1).split(",") if w.strip()]
    prompts = [clean(x) for x in numbered(body)]
    prompts = [p for p in prompts if len(p) > 12]
    if not prompts:
        lead = clean(re.split(r"\n\s*\n", body.strip())[0]) if body.strip() else ""
        qs = [x for x in sentences(lead) if x.endswith("?")]
        if lead and not words_: prompts = qs or [lead]
    seen, ws = set(), []
    for w in words_:
        k = w.lower()
        if k not in seen and len(k) > 2 and k not in {x.lower() for x in heart}: seen.add(k); ws.append(w)
    if prompts: ws = []
    return {"words": ws[:12], "heart": heart, "prompts": prompts[:4]}


def split_parts(word, note, affix_hint, bold_parts):
    w = word.lower()
    if bold_parts and "".join(bold_parts).lower() == w and len(bold_parts) > 1: return bold_parts
    if note:
        m = re.match(r"\s*([a-z]+(?:\s*\+\s*[a-z]+)+)", note.lower())
        if m:
            ps = [p.strip() for p in m.group(1).split("+")]
            if "".join(ps) == w: return ps
    for a in affix_hint:
        a2 = a.strip("-").lower()
        if a.endswith("-") and w.startswith(a2) and len(w) > len(a2) + 1: return [w[:len(a2)], w[len(a2):]]
        if a.startswith("-") and w.endswith(a2) and len(w) > len(a2) + 1: return [w[:-len(a2)], w[-len(a2):]]
    return [w]


def parse_tables(body, affix_hint):
    """Markdown tables of words (L5): | Word | Meaning check | Spelling note | or | Root | Meaning | Examples |."""
    items = []
    rows = [l for l in body.splitlines() if l.startswith("|")]
    if len(rows) < 3: return items
    head = [c.strip().lower() for c in rows[0].strip("|").split("|")]
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip("|").split("|")]
        if len(cells) < 2: continue
        if head[0].startswith("word") or head[0] in ("prefix", "suffix"):
            word = clean(cells[0])
            if not re.fullmatch(r"[A-Za-z'-]+", word): continue
            note = cells[2] if len(cells) > 2 else ""
            items.append({"word": word, "meaning": clean(cells[1]), "parts": split_parts(word, note, affix_hint, None), "affix": affix_hint[0] if affix_hint else None})
        elif head[0].startswith("root"):
            root, meaning = clean(cells[0]), clean(cells[1])
            for m in re.finditer(r"([a-z]*\*\*[a-z]+\*\*[a-z]*)\s*\(([^)]*)\)", cells[2] if len(cells) > 2 else ""):
                raw = m.group(1)
                parts = [p for p in re.split(r"\*\*", raw) if p]
                word = "".join(parts)
                items.append({"word": word, "meaning": clean(m.group(2)), "parts": parts, "affix": root, "root": True, "rootMeaning": meaning})
    return items


def parse_vocab(body):
    """Tier-2 words in three course styles."""
    out = []
    # L5: **gradually** — friendly definition: "..." Examples: "..." / "..."
    for m in re.finditer(r"^\*\*([A-Za-z' -]+)\*\*\s*[—–-]\s*friendly definition:\s*(.*?)(?=^\*\*[A-Za-z' -]+\*\*\s*[—–-]|\Z)", body, re.S | re.M | re.I):
        txt = m.group(2)
        d = first_quoted(txt) or clean(txt.split("Examples")[0])
        ex = re.findall(r"[\"“]([^\"”]{8,})[\"”]", txt.split("Examples", 1)[1]) if "Examples" in txt else []
        gen = re.search(r"Generative use:\s*(.*)", txt, re.S)
        out.append({"word": m.group(1).strip(), "def": clean(d), "examples": [clean(e) for e in ex[:2]], "task": clean(gen.group(1)) if gen else None})
    if out: return out
    # L6.05 on: **vast** — *adjective* — definition.  - Example: "..."  - **Your turn:** ...
    for m in re.finditer(r"^\*\*([A-Za-z' -]+)\*\*\s*[—–-]\s*\*[a-z ]+\*\s*[—–-]\s*(.*?)(?=^\*\*[A-Za-z' -]+\*\*\s*[—–-]\s*\*|\Z)", body, re.S | re.M):
        txt = m.group(2)
        ex = re.findall(r"Example:\s*[\"“]([^\"”]+)[\"”]", txt)
        task = re.search(r"Your turn:\*?\*?\s*(.*?)(?=\n\s*\n|\Z)", txt, re.S)
        out.append({"word": m.group(1).strip(), "def": clean(txt.split("\n-")[0]).rstrip(" ."), "examples": [clean(e) for e in ex[:2]], "task": clean(task.group(1)) if task else None})
    if out: return out
    # L6: **Word 1: organ** - Friendly definition: ... - Example 1: "..."
    for m in re.finditer(r"\*\*Word \d+:\s*([^*]+)\*\*(.*?)(?=\*\*Word \d+:|\Z)", body, re.S):
        txt = m.group(2)
        d = re.search(r"Friendly definition:\s*(.*)", txt)
        ex = re.findall(r"Example \d:\s*[\"“]([^\"”]+)[\"”]", txt)
        gen = re.search(r"Generative task:\s*(.*)", txt)
        out.append({"word": clean(m.group(1)), "def": clean(d.group(1)) if d else "", "examples": [clean(e) for e in ex[:2]], "task": clean(gen.group(1)) if gen else None})
    if out: return out
    # L7: - **Deposition** — definition. *"example"* Your turn: ...   (or numbered "1. **Straw man** — ...")
    for it in bullets(body) + numbered(body):
        m = re.match(r"\*\*([^*]{2,40})\*\*\s*[—–-]\s*(.*)", it, re.S)
        if not m: continue
        rest = m.group(2)
        ex = re.findall(r"\*[\"“]([^\"”]{6,})[\"”]", rest) or re.findall(r"[\"“]([^\"”]{10,})[\"”]", rest)
        d = re.split(r"\s\*[\"“]|\s[\"“]|Your turn:", rest)[0]
        task = re.search(r"Your turn:\s*(.*)", rest)
        out.append({"word": clean(m.group(1)), "def": clean(d).rstrip(" ."), "examples": [clean(e) for e in ex[:2]], "task": clean(task.group(1)) if task else None})
    return out


def parse_wordwork(body):
    items, vocab, affixes = [], [], []
    for title, sb in subsections(body):
        tl = title.lower()
        if "tier-2" in tl or "tier 2" in tl:
            vocab += parse_vocab(sb); continue
        hint = re.findall(r"(-?[a-z]+-|-[a-z]+)", title.split("(")[0]) if title != "_lead" else []
        if title != "_lead" and hint: affixes.append({"affix": title.split("(")[0].strip(), "meaning": clean(title.split("(", 1)[1].rstrip(")")) if "(" in title else ""})
        items += parse_tables(sb, hint)
        if title == "_lead" or not hint:
            vocab += parse_vocab(sb)
    review = []
    for m in re.finditer(r"\*\*All ([^*]+)\*\*[^`]*?`([^`]+)`", body):
        review.append({"label": clean(m.group(1)), "items": [x.strip() for x in re.split(r",|·", m.group(2)) if x.strip()]})
    seen, uniq = set(), []
    for it in items:
        if it["word"].lower() in seen: continue
        seen.add(it["word"].lower()); uniq.append(it)
    return {"items": uniq, "vocab": vocab, "affixes": affixes, "review": review}


def parse_prime(body):
    facts = []
    m = re.search(r"(?:Give\s+2[–-]3\s+quick\s+facts|(?:Key|One|Two|Three)\s+facts?[^:]*):\s*(.*?)(?=Orienting\s+question|\*\*Orienting|\n\s*\n\S|\Z)", body, re.S | re.I)
    if m:
        txt = m.group(1)
        nums = numbered(txt)
        if nums: facts = [clean(x) for x in nums]
        elif re.search(r"\*\*\(\d\)\*\*|\(\d\)", txt):
            facts = [clean(x) for x in re.split(r"\*\*\(\d\)\*\*|\(\d\)", txt) if clean(x)]
        else:
            facts = [clean(x) for x in re.split(r";\s*", clean(txt)) if clean(x)]
    if not facts:
        nums = numbered(body)
        facts = [clean(x) for x in nums][:3]
    q = re.search(r"Orienting\s+question:?\*?\*?:?\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
    intro = [p for p in plain_paragraphs(body) if not re.match(r"(Key facts|Orienting|Give 2|Three facts)", p)]
    return {"facts": [f.rstrip(" ;") for f in facts if len(f) > 8][:4], "question": clean(q.group(1)).strip('"“” ') if q else None,
            "intro": intro[0] if intro else None}


def stop_checks(paras):
    """Pull 'Stop and check (Literal): Q Answer: A' out of quoted paragraphs."""
    text, qs = [], []
    for p in paras:
        m = re.match(r"\*\*Stop and check[^*]*\*\*:?\s*(.*?)\s*\*?Answer:\s*(.*?)\*?$", p)
        if m: qs.append({"q": clean(m.group(1)), "a": clean(m.group(2))}); continue
        if p.startswith("**Stop and check"): qs.append({"q": clean(re.sub(r"^\*\*[^*]*\*\*:?", "", p)), "a": None}); continue
        text.append(p)
    return text, qs


def passage(title, body, track=None):
    paras = quote_paragraphs(body)
    code = re.search(r"```\n(.*?)```", body, re.S)
    script = False
    if not paras and code:   # Readers Theatre script: one line per speaker turn
        script = True
        turns, cur = [], None
        for l in code.group(1).splitlines():
            if re.match(r"[A-Z][A-Z .]+:", l):
                if cur: turns.append(cur)
                cur = l.strip()
            elif cur and l.strip(): cur += " " + l.strip()
            elif cur: turns.append(cur); cur = None
        if cur: turns.append(cur)
        paras = [t for t in turns if not t.startswith("CAST")]
    if not paras:   # plain-prose passage (L5.07 on): paragraphs up to the word count / comprehension check
        prose = re.split(r"\n\(≈|\n\*\*Comprehension check", body)[0]
        paras = [p for p in plain_paragraphs(prose) if not re.match(r"(\(≈|Comprehension check|Model first|Read it twice)", p)]
    roles = [p for p in paras if re.match(r"\*\*(PREDICTOR|Predictor|QUESTIONER|Questioner)", p)]
    paras = [p for p in paras if p not in roles]
    text, qs = stop_checks(paras)
    phrased = any(" / " in p for p in text)
    text = [clean(unslash(p)) if phrased else clean(p) for p in text]
    text = [t for t in text if t and not re.match(r"\(≈?\d+ words", t)]
    cc = re.search(r"\*\*Comprehension check[^*]*\*\*:?\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
    if cc:
        for q in re.split(r"\(\d\)\s*", cc.group(1))[1:]:
            qs.append({"q": clean(q), "a": None})
    qs += [{"q": clean(x), "a": None} for x in numbered(body) if "?" in x and not any(clean(x) == q["q"] for q in qs)]
    t = clean(re.sub(r"^(Track [AB](?: script)?\s*[—–-]\s*|The [Tt]ext:\s*)", "", title))
    t = re.sub(r"\s*\(for an? [^)]*\)?$", "", t)
    t = re.sub(r"^\d+\.\s*", "", t); t = t[:1].upper() + t[1:]
    return {"track": track, "title": t, "paragraphs": text, "phrased": phrased, "script": script,
            "questions": [q for q in qs if q["q"]][:8], "_roles": parse_roles("\n\n".join(roles)) if roles else []}


def parse_roles(body):
    roles = []
    # L5 / L7: **Predictor** — ..., **Predict:** ...
    body = re.sub(r"^>\s?", "", body, flags=re.M)
    for m in re.finditer(r"\*\*(Predict(?:or)?|Question(?:er)?|Clarif(?:y|ier)|Summari[sz](?:e|er))(?: card)?:?\*\*:?\s*[—–-]?\s*(.*?)(?=\*\*(?:Predict|Question|Clarif|Summari)|\n\s*\n|\Z)", body, re.S | re.I):
        name = {"predic": "Predictor", "questi": "Questioner", "clarif": "Clarifier", "summar": "Summarizer"}[m.group(1).lower()[:6]]
        txt = clean(m.group(2)).strip(" ,(\"“”")
        ex = re.search(r"\be\.g\.\s*(.*?)\)?$", txt)
        pr = re.sub(r"\s*\(?\be\.g\..*$", "", txt)
        pr = re.sub(r"[\"”]?\s*After reading.*$", "", pr).strip(" ,—–-()\"“”")
        if pr.count("(") < pr.count(")"): pr = pr.replace(")", "")
        if pr.count('"') % 2: pr = pr.replace('"', "")
        pr = pr.rstrip(" .") + ("" if pr.endswith("?") else ".") if pr else pr
        roles.append({"role": name, "prompt": pr[0].upper() + pr[1:] if pr else pr, "model": ex.group(1).strip('"“”) ') if ex else None})
    # L6: **Tutor as Predictor:** "..."  (modeled dialogue -> good answers)
    for m in re.finditer(r"\*\*(?:Tutor|Learner) as (\w+):\*\*\s*[\"“](.*?)[\"”]\s*$", body, re.S | re.M):
        r = next((x for x in roles if x["role"] == m.group(1)), None)
        if r: r["model"] = r["model"] or clean(m.group(2))
        else: roles.append({"role": m.group(1), "prompt": None, "model": clean(m.group(2))})
    return roles


def parse_write(body):
    task = re.search(r"\*\*Task:?\*\*:?\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
    model = re.search(r"\*\*Model answer[^*]*\*\*:?\s*(.*?)(?=\n\s*\n\*\*|\n\s*\n#|\Z)", body, re.S)
    t = clean(task.group(1)) if task else (plain_paragraphs(body) or [""])[0]
    return {"task": t, "model": clean(model.group(1)).strip('"“” ') if model else None}


def parse_check(body):
    items = []
    nums = numbered(body.split("**Answer key")[0])
    for x in nums:
        m = re.match(r"\*\*\((\w+)\)\*\*\s*(.*)", x, re.S)
        items.append({"q": clean(m.group(2) if m else x), "kind": m.group(1).lower() if m else None, "a": None})
    key = re.search(r"\*\*Answer key:?\*\*:?(.*?)(?=\n\*\*[A-Z]|\n#|\Z)", body, re.S)
    if key:
        for i, a in enumerate(numbered(key.group(1))):
            if i < len(items): items[i]["a"] = clean(a)
    if not items:
        for b in bullets(body.split("**≥")[0]):
            if re.match(r"\*\*", b) and not re.match(r"\*\*(Read|Define|Give|Spell|Write|Name)", b): continue
            items.append({"q": clean(b), "kind": "task", "a": None})
    model = re.search(r"Model answer[^:]*:\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
    selfc = re.search(r"Self-check:?\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
    if model and not any(i["a"] for i in items):
        items.append({"q": "Compare your answers with the model answer.", "kind": "model", "a": clean(model.group(1))})
    if selfc:
        items.append({"q": clean(selfc.group(1)), "kind": "self", "a": None})
    bar = re.search(r"\*\*(≥\s*\d+/\d+)[^*]*\*\*|Pass rule:\*\*\s*([^.→,]*)", body)
    sup = re.search(r"\*\*Support:\*\*\s*(.*?)(?=\n\*\*|\n\s*\n|\Z)", body, re.S)
    ch = re.search(r"\*\*Challenge:\*\*\s*(.*?)(?=\n\*\*|\n\s*\n|\Z)", body, re.S)
    if not items:
        items = [{"q": p, "kind": "self", "a": None} for p in plain_paragraphs(body)[:2]]
    for i in items: i["q"] = i["q"][:1].upper() + i["q"][1:]
    return {"items": [i for i in items if i["q"]][:10], "bar": clean((bar.group(1) or bar.group(2))) if bar else None,
            "support": clean(sup.group(1)) if sup else None, "challenge": clean(ch.group(1)) if ch else None}


# ---------- lesson ----------
def parse_session(path):
    md = path.read_text()
    m = re.match(r"L(\d)\.(\d+)", path.name)
    level, num = int(m.group(1)), int(m.group(2))
    t = re.search(r"^# (.*)$", md, re.M)
    S = {"id": f"L{level}.{num:02d}", "level": level, "title": t.group(1).split("—", 1)[-1].strip() if t else path.stem,
         "source": f"course/level-{level}/lessons/{path.name}", "practice": True}
    goal = re.search(r"\*\*Goal:\*\*\s*(.*?)(?=\n\*\*|\n\s*\n)", md, re.S)
    S["goal"] = clean(goal.group(1)) if goal else None
    passages, discuss, moves = [], [], []
    for title, body in sections(md, 2):
        tl = title.lower()
        if "tutor note" in tl or "kids-track" in tl or "wrap-up" in tl or "a note on" in tl: continue
        if "retrieval" in tl:
            S["warm"] = parse_warm(body)
        elif "word work" in tl or "morphology review" in tl:
            S["word"] = parse_wordwork(body)
        elif "prime" in tl:
            S["prime"] = parse_prime(body)
        elif tl.startswith("3. fluency or close") or tl.startswith("3. fluency or"):
            ps = quote_paragraphs(body)
            if ps:
                txt = " ".join(ps)
                S["fluency"] = {"title": "Read it smoothly", "paragraphs": [clean(unslash(p)) for p in ps], "phrased": " / " in txt}
        elif "meet the move" in tl:
            moves.append({"title": clean(re.sub(r"\(\d+ min\)", "", title.split(":", 1)[-1])).strip(), "paragraphs": plain_paragraphs(body)[:3]})
        elif "discussion" in tl and "knowledge" not in tl:
            discuss += parse_roles(body)
        elif re.search(r"writ(e|ing)", tl) and ("read" in tl or "capstone" in tl):
            S.setdefault("write", parse_write(body))
        elif re.match(r"(\d\.\s*)?(check|level \d mastery check)", tl) or tl.startswith("check") or ("check" in tl and "mastery" in tl):
            S["check"] = parse_check(body)
        elif "synthesis questions" in tl:
            discuss += [{"role": "Synthesis", "prompt": clean(x), "model": None} for x in numbered(body)[:4]]
        elif "expected findings" in tl:
            passages.append({"track": None, "title": "Expected findings (read after you search)", "paragraphs": plain_paragraphs(body)[:6],
                             "phrased": False, "script": False, "questions": [], "_roles": []})
        elif re.search(r"fluency|knowledge text|close reading|read all four|sustained deep|practice — matching|the real exercise", tl):
            subs = subsections(body)
            for st, sb in subs:
                stl = st.lower()
                if "discussion" in stl or "reciprocal" in stl:
                    discuss += parse_roles(sb); continue
                tr = "A" if stl.startswith("track a") else "B" if stl.startswith("track b") else None
                is_text = ("text" in stl and not re.search(r"structure|strategy|strategies", stl)) or "script" in stl
                if (st == "_lead" and (level == 7 or len(subs) == 1)) or tr or is_text:
                    p = passage(st if st != "_lead" else clean(re.sub(r"\(\d+[–-]?\d* min\)", "", title.split("—", 1)[-1].split(":", 1)[-1])), sb, tr)
                    if st == "_lead" and level == 7:
                        bg = [x for x in plain_paragraphs(sb) if x.startswith("Background:")]
                        if bg: p["paragraphs"] = [bg[0]] + p["paragraphs"]
                    discuss += p["_roles"]
                    if p["paragraphs"]: passages.append(p)
    for p in passages: p.pop("_roles", None)
    if passages: S["text"] = {"passages": passages, "moves": moves}
    if not discuss and passages:
        # "Learner runs all four roles alone, as in the last lessons": use the course's own role cards (L6.05)
        discuss = [dict(r, default=True) for r in DEFAULT_ROLES]
    if "fluency" not in S and passages:
        # Level 5 and 7: the fluency read is the opening of the knowledge passage (per track)
        S["fluency"] = {"title": "Read it smoothly", "fromText": True, "phrased": any(p["phrased"] for p in passages)}
    if discuss: S["discuss"] = {"roles": discuss}
    S["screens"] = [k for k in SCREENS if S.get(k)]
    return S


# ---------- audio plan (render nothing now; count characters) ----------
def clip_texts(S):
    """Every line the app would voice, keyed like the app asks for it: ss:<lesson>:<block>:<n>."""
    out, lid = {}, S["id"]
    w = S.get("warm") or {}
    for i, x in enumerate(w.get("words", []) + w.get("heart", [])): out[f"ss:{lid}:warm:w{i}"] = x
    for i, x in enumerate(w.get("prompts", [])): out[f"ss:{lid}:warm:p{i}"] = x
    wd = S.get("word") or {}
    for i, it in enumerate(wd.get("items", [])):
        out[f"ss:{lid}:word:{i}"] = it["word"]; out[f"ss:{lid}:word:{i}:m"] = f"{it['word']}: {it['meaning']}"
    for i, v in enumerate(wd.get("vocab", [])):
        out[f"ss:{lid}:vocab:{i}"] = " ".join([f"{v['word']}. {v['def']}."] + v.get("examples", []))
    pr = S.get("prime") or {}
    for i, f in enumerate(pr.get("facts", [])): out[f"ss:{lid}:prime:{i}"] = f
    if pr.get("question"): out[f"ss:{lid}:prime:q"] = pr["question"]
    fl = S.get("fluency") or {}
    for i, p in enumerate(fl.get("paragraphs", [])): out[f"ss:{lid}:flu:{i}"] = p
    for j, ps in enumerate((S.get("text") or {}).get("passages", [])):
        for i, p in enumerate(ps["paragraphs"]): out[f"ss:{lid}:text:{j}:{i}"] = p
        for i, q in enumerate(ps["questions"]): out[f"ss:{lid}:text:{j}:q{i}"] = q["q"]
    for i, r in enumerate((S.get("discuss") or {}).get("roles", [])):
        if r.get("prompt"): out[f"ss:{lid}:disc:{i}"] = r["prompt"]
    if (S.get("write") or {}).get("task"): out[f"ss:{lid}:write"] = S["write"]["task"]
    for i, it in enumerate((S.get("check") or {}).get("items", [])): out[f"ss:{lid}:check:{i}"] = it["q"]
    return out


def learner_words(S):
    return set(words(" ".join(clip_texts(S).values())))


def main(course=None, levels=(5, 6, 7)):
    course = Path(course) if course else ROOT.parent / "english-reading-course" / "course"
    (OUT / "sessions").mkdir(exist_ok=True)
    idx_path = OUT / "sessions" / "index.json"
    index = json.loads(idx_path.read_text()) if idx_path.exists() else []
    index = [x for x in index if x["level"] not in levels]
    need_path = OUT / "audio_needed_l5_7.json"
    need = json.loads(need_path.read_text()) if need_path.exists() else {"note": "", "levels": {}, "lessons": {}}
    need["note"] = ("Characters Sound Out would send to ElevenLabs for Levels 5-7 practice (River voice). NOTHING is rendered yet "
                    "(quota exhausted): every clip shows an 'audio coming' placeholder. Keys are ss:<lesson>:<block>:<n>; texts are "
                    "rebuilt from content/sessions/*.json by tools/parse_sessions.py clip_texts().")
    rows = []
    for lv in levels:
        files = sorted(course.glob(f"level-{lv}/lessons/L{lv}.*.md"))
        tot_c = tot_k = 0
        for f in files:
            S = parse_session(f)
            (OUT / "sessions" / f"{S['id']}.json").write_text(json.dumps(S, indent=1, ensure_ascii=False))
            ct = clip_texts(S); ch = sum(len(t) for t in ct.values())
            need["lessons"][S["id"]] = {"clips": len(ct), "chars": ch}
            tot_c += ch; tot_k += len(ct)
            lw = learner_words(S)
            index.append({"id": S["id"], "level": lv, "title": S["title"], "screens": S["screens"], "words": len(lw)})
            rows.append((S, len(lw), ch))
        need["levels"][str(lv)] = {"lessons": len(files), "clips": tot_k, "chars": tot_c}
    index.sort(key=lambda x: (x["level"], x["id"]))
    idx_path.write_text(json.dumps(index, indent=1, ensure_ascii=False))
    need["levels"] = dict(sorted(need["levels"].items())); need["lessons"] = dict(sorted(need["lessons"].items()))
    need["total"] = {"clips": sum(v["clips"] for v in need["levels"].values()), "chars": sum(v["chars"] for v in need["levels"].values())}
    need_path.write_text(json.dumps(need, indent=1, ensure_ascii=False))
    write_coverage(index, need)
    for lv in levels:
        ls = [r for r in rows if r[0]["level"] == lv]
        full = sum(1 for S, _, _ in ls if len(S["screens"]) == len(SCREENS))
        print(f"L{lv}: {len(ls)} lessons, {full} with all 8 screens, learner words {sum(n for _, n, _ in ls)}, chars {need['levels'][str(lv)]['chars']}")
    return index


def write_coverage(index, need):
    cov = OUT / "coverage.md"
    A, B = "<!-- sessions:start -->", "<!-- sessions:end -->"
    rows = [A, "## Levels 5-7 session blocks (tools/parse_sessions.py, practice only)", "",
            "Session template parsed per lesson: W=warm-up, WW=word work, F=fluency/close reading, P=prime, T=knowledge text, "
            "D=discussion (reciprocal roles), Wr=write to read, C=check. **Words** = distinct learner-facing words parsed "
            "(the old L5-L7 table above counts only Level 1-4 style blend/check words, hence its 0). Chars = characters to voice "
            "(none rendered yet, see content/audio_needed_l5_7.json).", ""]
    for lv in sorted({x["level"] for x in index}):
        ls = [x for x in index if x["level"] == lv]
        full = sum(1 for x in ls if len(x["screens"]) == len(SCREENS))
        rows += [f"### Level {lv}: {full}/{len(ls)} lessons with all 8 screens · {need['levels'][str(lv)]['chars']:,} chars to voice", "",
                 "| Lesson | Title | W | WW | F | P | T | D | Wr | C | Words | Chars |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for x in ls:
            y = lambda k: "✓" if k in x["screens"] else "·"
            rows.append(f"| {x['id']} | {x['title'][:40]} | " + " | ".join(y(k) for k in SCREENS) + f" | {x['words']} | {need['lessons'][x['id']]['chars']:,} |")
        rows.append("")
    rows.append(B)
    txt = cov.read_text() if cov.exists() else ""
    block = "\n".join(rows)
    if A in txt: txt = re.sub(re.escape(A) + r".*?" + re.escape(B), lambda _: block, txt, flags=re.S)
    else: txt = txt.rstrip("\n") + "\n\n" + block + "\n"
    cov.write_text(txt)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    lv = (5, 6, 7)
    if "--levels" in sys.argv: lv = tuple(int(x) for x in sys.argv[sys.argv.index("--levels") + 1].split(","))
    args = [a for a in args if not re.fullmatch(r"[\d,]+", a)]
    main(args[0] if args else None, lv)
