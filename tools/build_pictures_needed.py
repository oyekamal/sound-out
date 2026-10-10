#!/usr/bin/env python3
"""Inventory every picture a learner could see -> content/pictures_needed.json (word concepts + Listen&Talk chunk scenes)."""
import sys, json, glob, re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE)
from picture_words import W
lessons = {}
for f in sorted(glob.glob(f"{ROOT}/content/lessons/*.json")):
    d = json.load(open(f))
    if d["level"] <= 4: lessons[d["id"]] = d
def texts(d):
    li = d.get("listen") or {}
    return {"blend": " ".join((d.get("blendList") or {}).get("real", [])),
            "spell": " ".join((d.get("spell") or {}).get("words", []) + [(d.get("spell") or {}).get("sentence", "") or ""]),
            "read": " ".join(v["text"] for v in (d.get("read") or {}).values() if isinstance(v, dict) and v.get("text")),
            "listen": li.get("passage", "") + " " + " ".join(li.get("questions", []))}
T = {i: texts(d) for i, d in lessons.items()}
irregular = {"sat": "sit|sat|sits|sitting", "cooking": r"cook\w*", "cook": r"cook\w*", "crying": "cry|cries|crying", "cry": "cry|cries|crying", "mother": "mother|mom|mum", "bike": "bike|bikes|bicycle|bicycles", "ear": "ears?", "eye": "eyes?", "friend": "friends?", "animal": "animals?"}
L1ORAL = {"sun": ["first", "check"], "top": ["first", "check"], "mat": ["first", "blend", "check"], "pig": ["first", "check"], "dog": ["first", "segment", "check"],
          "sat": ["worked", "blend", "segment", "check"], "at": ["blend", "segment"], "it": ["blend"], "on": ["blend"], "up": ["segment"]}
AMB = set("animal at bat boss brave busy caravan card cart chin cot count crumb dish dock dot engine fat field gate glue gum ham hard head hog hold hole hood it jet key kid kind lamb lid lip mule new nose old on proud rat sat sky string tank thin tool uncle up".split())   # synonym-siblings / abstract words a picture cannot pin down (flagged by the haiku critic passes)
words = {}
for s, (k, desc) in W.items():
    pat = irregular.get(s, re.escape(s) + r"(?:s|es|ed|ing)?")
    if k == "v" and s.endswith("e"): pat = re.escape(s[:-1]) + r"(?:e|es|ed|ing)"
    rx = re.compile(r"\b(?:%s)\b" % pat, re.I); scr = []
    for i, t in T.items():
        for kind, txt in t.items():
            if rx.search(txt): scr.append(f"{kind}:{i}")
    scr += [f"l1oral:{st}" for st in L1ORAL.get(s, [])]
    if not scr: continue          # not used anywhere in L1-L4: no picture needed
    lv = sorted({int(x.split(":")[1][1]) for x in scr if x.split(":")[1].startswith("L")} | ({1} if s in L1ORAL else set()))
    words[s] = {"type": "word", "kind": {"n": "noun", "v": "verb", "a": "adjective", "f": "function word"}[k], "draw": desc, "levels": lv, "count": len(scr), "screens": scr,
                "must_show_action": k in ("v", "a"),
                "ambiguous": k == "f" or s in AMB,
                "alias_of": "sit" if s == "sat" else None,
                "note": "function word: no natural picture; best-effort scene; the app should avoid picture-only choices for at/it/on/up" if k == "f" else ""}
sent = lambda t: [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\"\u201c])", t) if x.strip()]   # same split as build_levels / gen_audio_el
chunks = []
for lid, d in lessons.items():
    li = d.get("listen")
    if li:
        ss = sent(li["passage"])
        chunks += [{"id": f"{lid}:{i // 2}", "text": " ".join(ss[i:i + 2])} for i in range(0, len(ss), 2)]
scenes = {s["id"]: s for s in json.load(open(f"{ROOT}/content/picture_scenes.json"))}   # hand/agent-authored scene descriptions
sc = {}
for c in chunks:
    s = scenes[c["id"]]; lid, i = c["id"].split(":")
    sc[f"scene:{lid}:{i}"] = {"type": "scene", "level": int(lid[1]), "lesson": lid, "chunk": int(i), "text": c["text"], "draw": s["scene"], "levels": [int(lid[1])], "count": 1,
        "screens": [f"listen:{lid}:chunk{i}"], "must_show_action": True, "must_show": bool(s["must_show"]), "why": s["why"], "ambiguous": False}
import picture_overrides as PO
fixes = json.load(open(f"{ROOT}/content/picture_scene_fixes.json"))
for k, d in PO.O.items():
    if k in words: words[k]["draw_v1"] = words[k]["draw"]; words[k]["draw"] = d
for k, d in {**fixes, **PO.S}.items():
    if k in sc: sc[k]["draw_v1"] = sc[k]["draw"]; sc[k]["draw"] = d
out = {"note": "Every picture request in Sound Out L1-L4. Words: shown after decoding (blend/spell/read picks) and L1.01 oral screens. Scenes: Listen & Talk, one per 2-sentence chunk (clip lt:<lesson>:<i>). Track B (L5-L7 sessions) requests NO pictures. Listen & Talk 3-picture ANSWERS are not authored yet (C19, open oral questions): see unmet.",
       "unmet": ["Listen & Talk question answers (3 pictures each, 2 questions/lesson): the course questions are open oral inference, no authored picture options exist; app currently shows placeholders and accepts any pick. Needs authored picture questions (plan C19) before art can be made.",
                 "L5-L7 (Track B sessions): no picture screens request art.", "Picture 'picture N' labels in l1oral.js are indexes, not concepts: wire by word key via pictures.json."],
       "counts": {"words": len(words), "scenes": len(sc), "total": len(words) + len(sc), "word_screen_uses": sum(w["count"] for w in words.values()), "by_level_words": {str(l): sum(1 for w in words.values() if min(w["levels"] or [9]) == l) for l in (1, 2, 3, 4)}},
       "concepts": {**words, **sc}}
json.dump(out, open(f"{ROOT}/content/pictures_needed.json", "w"), indent=1, ensure_ascii=False)
print(out["counts"])
