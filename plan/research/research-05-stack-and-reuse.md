# Read English app: stack plan and reuse audit

Date: 2026-10-05. Read-only audit. Nothing in `urdu-reading-course` or `english-reading-course` was changed.
Sources read: Urdu repo `README.md`, `research/09_tech_stack.md`, `mobile/package.json`, `mobile/src/*.js` (all 26 files by header and exports, db/session/content/path/onboarding in more depth), `mobile/vite-sw-plugin.js`, `mobile/tools/*`, `scripts/*`, `store/PLAY_CONSOLE_CHECKLIST.md`; English repo `DESIGN.md`, `tools/decodable.py`, lessons `L1.02`, `L3.05`, `L4.03`, `L5.01`, level READMEs.

Caveat on method: I did not read every line of `teacher.js`, `egra.js`, `feel.js`, `a11y.js`, `marko.js`. Their verdicts come from headers, export lists and grep, and are marked "skim" where that matters. Figures about Piper/Kokoro/sherpa model sizes are the ones in the brief or from memory. They are not verified here.

---

## 1. Reuse map

### Decision: new repo, copy files once, no fork, no shared package

- A GitHub fork carries the Urdu history, 190 MB of `assets/audio`, 35 MB of Urdu card images and 18 Urdu research files. All of it would have to be deleted and would stay in history.
- A shared package is premature. The "generic" modules are not generic yet. `session.js` hard-codes `C.units`, a 0 to 12 unit loop (`while (p.units[n]?.passed && n < 12)`) and Urdu audio keys (`units/u01_03`). `backup.js` allows Arabic code points in ids. `content.js` mixes Urdu helpers (`dotInfo`, `glyphForm`, `SAME_SOUND`) with generic helpers (`el`, `toast`, `shuffle`, `play`). Extracting a package means designing the abstraction before the second consumer exists, and the Urdu app is already shipped at v0.11.0 and would have to be regression-tested against it.
- Plan: `git init read-english`, copy the files below, and keep a `PROVENANCE.md` listing each copied file with the Urdu commit hash. Backport a bug fix by hand if one turns up. After English ships, a diff of the two repos shows what is truly shared. Extract only then.

### Per-module verdict (`mobile/src/`, 3,855 lines in total)

| Module | Lines | Verdict | What changes |
|---|---|---|---|
| `safe.js` | 40 | AS-IS | Input sanitising (`cleanName`, `esc`, `tapLock`). |
| `gate.js` | 89 | AS-IS | Spelled-out-number grown-up gate. Reused to guard the mic permission, backup/export and links out. |
| `fx.js` | 34 | AS-IS | Lottie confetti wrapper. |
| `motion.js` | 120 | AS-IS | Frame budget policy (one shared loop, pause offscreen). |
| `swreg.js` | 67 | AS-IS | Service worker registration and "update ready" toast. Skips on native. |
| `restore.js` | 29 | AS-IS | File picker into `validateBackup`. |
| `premium.js` | 70 | AS-IS (optional) | Tilt/parallax scene. Drop it if cold-start time is tight. |
| `db.js` | 129 | WITH CHANGES | Change `DB_NAME`. Keep the store list (settings, profiles, attempts, cards, sessions, progress, assessments). Add `speech` (metrics only) and `mastery`. Keep the `withTimeout` and `createMissing` repair logic. |
| `backup.js` | 72 | WITH CHANGES | Change `BACKUP_FORMAT`. Remove `؀-ۿ` from the id regex. `unitRec` becomes `lessonRec` (`passed`, `steps`, `lessons`). `wpmRec.unit` becomes `lesson`. Add the new stores. Lines are very long, so the real size is about 3x. |
| `session.js` | 71 | WITH CHANGES | Leitner boxes `[0,1,2,4,8,16]` days and `gradeCard`/`missCard` are right as they are. `ensureCards` should seed cards from GPCs and words introduced up to lesson N, not from `u.letters`/`u.words`. `currentUnit` loops to 12 and becomes `currentLesson` over about 100 ordered lessons. `audioKeyFor` becomes a content-addressed id. `DRILL_ITEM` gets the new drill names. |
| `path.js` | 221 | WITH CHANGES | `renderPath`, `lessonState`, `countUp`, `dailyGoal`, `unlockInfo` and `stringThread` are generic. `lessonsFor(u)` is Urdu-specific (join, marks, nonjoin, aspirates, nastaliq) and is rewritten to emit the 9-step English lesson (hear, meet, blend, spell, heart, read, listen, check). `markLesson` locks stay. |
| `learner.js` | 244 | WITH CHANGES | Tabs (Learn/Review/Read/Me) stay. Remove `styleName`/naskh/nastaliq and the `marks` flag. Add Speak tab entry points. `lang="en"` and no `ur` class. |
| `onboarding.js` | 231 | WITH CHANGES | The engine (17-screen flow, saved after every step, resumable) is reusable. The demo reads بابا built from ا+ب. English version reads "sat" built from s+a+t. The `speak`/`reads` questions become "what language do you speak at home" and "can you read any English". Copy changes. |
| `teacher.js` | 494 | WITH CHANGES (skim) | Roster, groups, reports, device mode, PIN and CSV share are generic. Strings and the unit picker change. Add speech-metrics column. |
| `egra.js` | 330 | WITH CHANGES (skim) | The 5 subtasks map directly: letter sounds, nonwords, familiar words, passage, comprehension. `PRP` bands (Pakistan grade-2: 60/90 cwpm) become English benchmarks (Hasbrouck-Tindal style, cite when added). `scriptClass`/nastaliq goes. This is the screen a speech scorer would later automate. |
| `feel.js` | 282 | WITH CHANGES (skim) | Tones via WebAudio, `@capacitor/haptics`, ripple/bounce/wobble. The copy lines (`lineFor`) are text that needs rewording. |
| `a11y.js` | 293 | WITH CHANGES (skim) | Live regions, dialog focus trap, nav inert handling and `fitLesson` are generic. `markUrdu` (tags Urdu runs with lang/dir) is deleted. |
| `dashboard.js` | 41 | WITH CHANGES | The letter-mastery grid becomes a GPC/heart-word grid. The rest stays. |
| `practice.js` | 139 | WITH CHANGES | Share/print cards. It uses `@capacitor/filesystem` and `@capacitor/share`. Keep it if printables ship. |
| `main.js` | 155 | WITH CHANGES | Mode choice, profile picker, teacher PIN, routing. Rename only. |
| `marko.js` / `memory.js` / `stickers.js` / `icons.js` | 187 / 41 / 100 / 63 | BRAND DECISION | Marko is a Pakistani-village Lottie mascot. A global audience may want a neutral mascot, but the rig (`design/marko-rig/`) is the expensive asset and is reusable. `memory.js` ("one kind specific thing") and `stickers.js` (sticker per mastered letter, so per GPC) are good no-guilt mechanics. Recommend keeping Marko and re-skinning. |
| `drills.js` | 246 | REWRITE | `inkPad`/`judgeTrace` (about 90 lines), `joinIt`, `tellApart` with `SAME_SOUND`, `formsOf` and `dotInfo` are all glyph-form logic and not needed. Reusable patterns: tile choice grid, `cue()` sounds, `playBtn`, the quiz/dictation skeleton. New drills: blend (sound buttons), Elkonin segment boxes, tile spell, pseudoword read, heart-word, b/d/p/q discrimination. |
| `content.js` | 67 | REWRITE (about 20 lines kept) | Keep `loadContent`, `play`, `el`, `toast`, `shuffle`, `W`. Delete `STROKE`, `DOT_*`, `glyphForm`, `SAME_SOUND`. Keep `bandFor` and `PRP` shape with English numbers. |

Totals: AS-IS 449 lines (12%), WITH CHANGES 2,702 (70%), brand-dependent 391 (10%), REWRITE 313 (8%). Every Urdu-specific idea (RTL, Nastaliq/Naskh switch, letter joining, positional forms, vowel marks, non-joiners, aspirates, dot confusions, numerals) is in `drills.js`, `content.js`, `path.js:lessonsFor` and a few lines in `learner.js`/`a11y.js`. The rest is generic.

### Non-JS assets

| Asset | Lines | Verdict |
|---|---|---|
| `vite.config.js` (CSP + sw plugin) | 14 | AS-IS. Needs `worker-src`, `wasm-unsafe-eval` only if WASM is chosen (not recommended, section 4). |
| `vite-sw-plugin.js` (hashes files, eager vs lazy, `sw.js` versioning) | 71 | WITH CHANGES. `EAGER_AUDIO` regex becomes "L1-2 packs eager, rest lazy or downloaded". |
| `capacitor.config.json`, `android/` | n/a | Copy, change `appId` (`com.oyekamal.readenglish`), `appName`. Capacitor 7.6, minSdk 23, targetSdk 36. |
| `scripts/subset_fonts.py` | 40 | WITH CHANGES. Subset Andika (SIL OFL, single-storey a/g, literacy-designed) to Latin, about 30 KB woff2. |
| `scripts/make_icons.py` 55, `make_store.py` 157, `pack_images.py` 21 | 233 | AS-IS or light edit. |
| `scripts/listen_judge.py` | 85 | WITH CHANGES. Blind "which word/phoneme is this" and A/B via Gemini. Perfect for TTS QA. Prompts change from Urdu letters to English. |
| `scripts/store_judge.py` | 31 | AS-IS. |
| `scripts/voice_studio.py` | 547 | OPTIONAL. Browser recorder for human clips (getUserMedia + MediaRecorder). Useful for the 44 phoneme clips. |
| `scripts/el_audio.py` + `eleven.py` + `gen_audio.py` | 193 + 69 + 91 | REWRITE. Replace with a local-TTS batch (section 3). Keep the per-clip provenance idea (`method`, `voice`, `frame` in `audio_overrides.json`). |
| `check_decodable.py` | 32 | NOT NEEDED. Replaced by the English `tools/decodable.py` (163 lines). |
| `render_cards.py` 135, `vowelise_units.py` 253, `lexicon.py` 350, `build_course.py` 269, `build_pdfs.py` 934, `apply_*`, `make_review_needed.py` | n/a | NOT NEEDED (Urdu raqm rendering, vowelisation, Urdu lexicon). PDFs are optional later. |
| `mobile/tools/ui_audit.py` | 200 | AS-IS. Tap targets, overflow, docked actions, contrast. |
| `mobile/tools/drive_all.py` | 137 | REWRITE. Its answer logic regex-parses prompts like "Which is X at the initial position" and uses Urdu letter tables. English needs an oracle hook (section 7). |
| `shots.py`, `store_shots.py`, `store_shots_play.py`, `onb_shots.py`, `feel_seq.py`, `motion_seq.py`, `gate_test.py` | 15-124 | AS-IS or light edit (selectors). |
| `store/PLAY_CONSOLE_CHECKLIST.md` | 46 | AS-IS as a template. Data-safety answers change if speech or sync ship (section 4, 6). |

---

## 2. Content pipeline: markdown to JSON

### What the markdown looks like (grounded in the files read)

- `L1.02-s-a-t.md`: a lesson split into four "Sitting A/B/C/D" blocks, each with sub-steps (Hear it, Meet it, Blend it, Spell it, Mini check). Only Sitting D carries heart words, `### 7. Read it`, `### 8. Listen & Talk`, `### 9. Check`, `### Tutor notes`, `### Decodability audit`. Blend words sit in a pipe table (`| Real words (3) | Pseudowords / "alien words" (5) |` then `at, as, sat | tas, ast, sta, sas, att`). The Track A/B text is a blockquote: `> Sat. A tat. At.`.
- `L3.05`, `L4.03`: flat `## N. Step name (N min)` headings with `### Track A (child)` / `### Track B (adult)` (L3) or `### Track A — "Her First Bird"` (L4). Texts are `>` blockquote lines. L3 texts use `/` as a sentence/phrase separator inside one line.
- `L5.01` (session template): `## 1. Retrieval warm-up`, `## 2. Word work` with `### un-` sub-heads and pipe tables (`| Word | Meaning check | Spelling note |`), `## 3. Prime the topic`, `## 4. Fluency & Knowledge Text` with Track A/B texts where `/` marks phrase cues, then reciprocal roles and "Write to read". L6/L7 are the same shape with `## 2.1`-style numbering in places.
- Heading frequency check: L1 has 14 `Tutor notes` and 14 `Decodability audit` headings, 10 `### N. Read it`, 4 `## N. Read it`. So L1 itself is inconsistent (`###` vs `##`).

### Parser design (`tools/build_content.py`, Python stdlib)

1. Walk `course/level-N/lessons/*.md` plus `mastery-check.md`. Tokenise into heading tree with `^(#{2,3})\s+(?:\d+(?:\.\d+)?\.?\s+)?(.*?)(?:\s*\((\d+)[–-]?\d*\s*min\))?$`.
2. Map a heading to a step type by keyword, case-insensitive: `warm-up|retrieval` review, `hear it`, `meet it`, `blend it`, `spell it`, `heart word` heart, `read it|fluency` read, `listen & talk` listen, `prime` prime, `word work` wordwork, `check` check, `tutor notes` notes, `decodability audit` audit, `sitting [a-z]` sitting.
3. Extract by block type, not by prose: pipe tables become word lists; `>` blocks following a `Track A|B` heading become texts; `**word** — definition. "ex" "ex" Your turn: ...` bullets become Tier-2 entries; numbered lists after "Questions" become questions; `Real` and `Pseudo` rows in Check become item lists; `**Heart words:**` and `Heart words L1` lines are cross-checked against the canonical schedule.
4. `--strict` fails on an unrecognised `##`/`###` and prints the file and line. Expect a first run with a few dozen findings. Fix them by normalising the markdown headings (small, safe edits) rather than adding parser special cases.
5. Truth split: the GPC order (`SEQ`) and heart-word schedule (`HEART`) currently live inside `tools/decodable.py`. Move them to `data/gpc.json` and `data/heart.json` and have both `decodable.py` and the builder import them. Markdown stays the source for prose, lists and texts. Everything machine-critical has one owner.
6. Output: `content/index.json`, `content/gpc.json`, `content/lexicon.json`, `content/lessons/L1.02.json`, `content/mastery/L1.json`, `content/ui.json`. Per-lesson sharding keeps each fetch under about 50 KB.

### Proposed schema

```jsonc
// content/gpc.json: one entry per grapheme
{ "s": { "id":"s", "kind":"letter", "ipa":"s", "phoneme":"/s/", "intro":"L1.02",
         "mouth":"teeth close, air hisses", "audio":"ph.s", "examples":["sat","sun"],
         "locale":{"ur":"Same as Urdu س"} } }

// content/lexicon.json: every word the learner can meet
{ "sat": { "g":["s","a","t"], "p":["s","æ","t"], "kind":"decodable",   // decodable|heart|story|tier2|pseudo
           "intro":"L1.02", "audio":"w.9f3a1c", "img":null, "level":1 },
  "said":{ "g":["s","ai","d"], "p":["s","ɛ","d"], "kind":"heart", "heartIdx":[1], "intro":"L1.06" },
  "tas": { "kind":"pseudo", "g":["t","a","s"], "p":["t","æ","s"] } }

// content/lessons/L1.02.json
{ "id":"L1.02", "level":1, "order":2, "title":"s a t",
  "newGpc":["s","a","t"], "review":[], "heart":["a","I"],
  "sittings":[{"id":"A","newGpc":["s"],"steps":["hear","meet","spell","mini"],"mini":{"gpc":["s"],"pass":5,"of":5}}, ...],
  "blend":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"]},
  "spell":{"words":["at","sat"],"sentence":null},
  "read":{ "A":{"title":null,"sentences":[{"id":"s1","text":"Sat.","words":["sat"],"audio":"s.1a2b3c"}]},
           "B":{"sameAsA":true},
           "questions":[{"type":"literal","q":"Which word means someone sat down?","a":["sat"],"audio":"q.…"}] },
  "listen":{ "title":"Sam's First Day","sentences":[{"text":"…","audio":"s.…"}],
             "tier2":[{"word":"nervous","def":"…","examples":["…","…"],"yourTurn":"…","audio":{"def":"…"}}],
             "discuss":["…","…"] },
  "check":{ "real":["at","sat","as","at","sat"],"pseudo":["tas","sta","ast","sas","att"],
            "dictation":["at"],"pass":0.9,"reteach":"Redo Sitting C blending drill…" },
  "notes":"…tutor notes markdown (ship in teacher mode only)…" }

// L5-7 session: same file shape with "type":"session" and steps:
//  retrieval[], wordwork:{morphemes:[{affix,meaning,words:[{w,meaning,spell}]}]},
//  prime:{questions,facts[]}, text:{A:{phrases:[["Every morning","the sun comes up"…]]},B:…},
//  roles:{…}, write:{prompt}

// content/mastery/L1.json
{ "level":1, "components":[{"id":"letter-sounds","items":["s","a",…],"gate":0.9},
   {"id":"real-words"…},{"id":"pseudo"…},{"id":"heart"…},{"id":"dictation"…},{"id":"bdpq"…}],
  "scoring":"separate", "reteachMap":{"letter-sounds":"L1.13"} }
```

`pass` and the six separate components encode DESIGN.md rules 4 and 8. Never average them in the app either.

### What the markdown is missing for an app

| Missing | Why it blocks | How to get it |
|---|---|---|
| Per-word phoneme segmentation (`g` and `p` arrays) | The blend screen highlights grapheme by grapheme and plays a sound per tile. | Real words: CMUdict phonemes aligned to graphemes with a small GPC aligner. Extend the greedy longest-grapheme parse already in `tools/decodable.py`. Pseudowords: derive directly from the GPC table (deterministic by construction). Heart words: hand-mark `heartIdx` (the 11 of about 50 L1-L3 heart words that matter most). |
| Audio ids per word, sentence, question, UI line | Nothing plays without them. | Content-addressed: `id = sha1(voice + normalised text)[:10]`. The Urdu index keys (`units/u01_03`) break when a list is reordered. Hashes never do, and unchanged text never re-synthesises. |
| Sentence-to-word alignment | Karaoke highlighting while a sentence is read aloud. | Tokenise at build. Timing: forced alignment (Whisper word timestamps or MFA) once per clip, stored as ms offsets. |
| Isolated phoneme clips (44 or so) | The phonics foundation. TTS says "ess" for /s/. | Phoneme-input synthesis (Piper accepts phoneme ids, Kokoro takes phonemes) trimmed and QA'd, or record a human (`voice_studio.py`). Human is cheap at 44 x 2 variants. |
| Pictures | Tier-2 and noun words. | Rule 1 of DESIGN.md forbids cueing, so an image must be hidden until the word is decoded, never beside the unread word. Enforce that in a DOM test. Sources: OpenMoji (CC BY-SA 4.0) or generated art. Licences to check before shipping. |
| Distractors for choice drills | Multiple choice needs wrong answers. | Derive minimal pairs from the lexicon at build time (same length, one grapheme changed, taught so far). |
| Question answer keys beyond literal | Open "think" questions. | Mark `type:"think"` as self/tutor graded. Never auto-score. |
| UI strings with audio | Pre-readers cannot read English instructions. | `content/ui.json` of about 150 short spoken lines with icons. Locale packs (ur, hi, ar, es) as optional text+audio, later. |
| Level 6-7 chunking | Long texts need pagination and glossary. | Split into paragraphs, page by sentence group, link Tier-2 words to a pop-up. |
| Urdu/South-Asian notes as data | Rule 9 content currently sits in prose. | Put them under `locale.ur` and show only when the learner profile says Urdu. |

Decodability enforcement: `tools/decodable.py` only covers L1-L4 and is a greedy parse that "ignores which sound a grapheme makes" (its own docstring). That is acceptable as a build gate. From L5 on, the gate becomes "every word is in the lexicon with `kind` set". Tier-2 and story words must be explicitly flagged and counted (max 2 story words per text, DESIGN.md).

---

## 3. Audio

### Counts (script: `/tmp/claude-1000/.../scratchpad/count.py` and `count2.py`, run from the English repo root)

Method: lowercase, `[a-z]+('[a-z]+)?` tokens; "learner-facing" = words in `>` blockquotes, pipe tables and **bold/italic** spans; "all text" = every word in any lesson markdown including tutor prose. Sentences = `.`, `!`, `?` and `/` separators inside blockquotes, so L5 is overcounted (phrase cues counted as sentences) and the whole column is about plus or minus 25%.

| Level | Distinct (all text, per level) | Learner-facing, new this level | Sentences (blockquote) | Quote tokens |
|---|---|---|---|---|
| 1 | 2,261 | 1,066 | 297 | 2,344 |
| 2 | 2,078 | 575 | 515 | 3,044 |
| 3 | 2,212 | 442 | 385 | 2,232 |
| 4 | 2,910 | 714 | 297 | 3,395 |
| 5 | 3,394 | 938 | 730 | 2,047 |
| 6 | 3,925 | 1,229 | 823 | 12,255 |
| 7 | 3,448 | 799 | 499 | 6,448 |
| Cumulative | 9,238 (all text) | 5,763 | 3,546 | 31,765 |

Level 0 adds 187 quoted words. My 9,238 all-text figure differs from the brief's about 10,500 (probably hyphen/number tokenisation). I budget the learner-facing 5,763 and treat 9,238 as the ceiling if every word in tutor prose is voiced.

### Clip and MB math (24 kbps Opus, mono = 3 KB/s, plus about 0.4 KB container overhead)

- Word: 0.6 s, about 2.5 KB. Sentence: 4 s, about 12.5 KB (L6-L7 sentences average 15 words, so I use 5.5 s, 17 KB).
- Extra clips: Tier-2 definitions and examples (about 60 lessons x 2 words x 3 lines = 360 clips, 4.5 MB), UI/instruction lines (about 200, 1.8 MB), phonemes (about 90, 0.2 MB).

| Pack | Words | Sentences | MB |
|---|---|---|---|
| L1 | 1,066 | 297 | 6.4 |
| L2 | 575 | 515 | 7.9 |
| L3 | 442 | 385 | 5.9 |
| L4 | 714 | 297 | 5.5 |
| L5 | 938 | 730 | 11.5 |
| L6 | 1,229 | 823 | 17.1 |
| L7 | 799 | 499 | 10.5 |
| Extras (Tier-2, UI, phonemes) | | | about 6.5 |
| **Total** | **5,763** | **3,546** | **about 71 MB, about 9,960 clips** |

If every one of the 9,238 distinct words were voiced: about 23 MB for words instead of 14.4, so about 80 MB total.

Disk rounding matters: 5,763 files at 4 KB filesystem blocks occupy about 23 MB, not 14.4. Pack clips per lesson as a concatenated file of complete Ogg Opus streams plus an offset index, fetch once, slice with `Blob`. Fewer SW cache entries, no block waste, one request per lesson.

### Delivery recommendation

- Base AAB: shell (about 8 MB, the Urdu dist JS is 240 KB + 169 KB lottie) + L1-L2 audio + extras = about 18 MB audio, so roughly 26 MB AAB. For comparison the Urdu AAB is 27.8 MB and its 1,463 mp3s are 15 MB.
- Download packs: `L3-4` (about 12.5 MB), `L5` (12), `L6` (18), `L7` (11). Ship them as plain zips or per-lesson blob files hosted on GitHub Pages / a CDN, with a hash manifest.
- One mechanism for both targets: the PWA fetches packs into Cache API; the APK fetches into `Directory.Data` via `@capacitor/filesystem` (already a dependency). Resume per file, verify hash, `navigator.storage.persist()` after completion (from the Urdu 09 notes).
- Play Asset Delivery is the alternative for Android only. It needs a Gradle asset-pack module and a native `AssetPackManager` bridge (not in Capacitor core), and the PWA gets nothing from it. The whole 71 MB would fit under the 200 MB base-size limit, so the only reason for PAD is install size on 16-32 GB phones and cost of data. Defer. Total at all-in-AAB is roughly 80 MB; I would still go with downloaded packs because the first install is what a Pakistani parent on mobile data feels.
- Opus in Ogg plays in Chrome/Android WebView. Safari/iOS Opus support is the later risk: ship AAC `.m4a` as the iOS pack variant (about 30% larger). Verify on two real Android 10 devices before committing (Urdu `09` flagged this same item untested).

### TTS: pre-rendered vs on-device (sherpa-onnx)

| | Pre-rendered Opus (build-time local TTS) | On-device Piper via sherpa-onnx | On-device Kokoro |
|---|---|---|---|
| Size on device | 71 MB total, but only 18 MB at install | about 60 MB model + espeak-ng-data (from brief; verify) | about 300 MB (from brief; verify) |
| Voice consistency | Perfect: one model, one seed, pinned in manifest | Same voice but varies by phone speed/threads | Same |
| Latency | zero | likely 0.5-3 s per sentence on a 2 GB phone (unmeasured) | worse |
| Works in PWA | yes | WASM build is heavy; not recommended | no |
| Arbitrary text | no | yes | yes |
| Quality control | every clip auditioned and judged (`listen_judge.py`) | none per output | none per output |

Answer: ship pre-rendered clips on both Android and PWA. Do not put a TTS engine on device in v1. Render at build time on Kamal's machine with the best local model (Kokoro-class for quality, Piper if licence/size simpler). Pin `model_sha` and `voice` in `audio_manifest.json`, so a text fix re-renders only the changed hash. On-device Piper becomes an optional Android-only "voice engine" download later, solely for dynamic text (teacher-typed words, pasted text). The Urdu research reached the same conclusion for the same reason (09 section 3.3).

One thing TTS cannot do well is isolated sounds, and those are the most pedagogically important clips. Budget a spike for them (section 8).

---

## 4. Speech input in Capacitor

The Urdu app has no learner speech input. `RECORD_AUDIO` is absent and `getUserMedia` appears only in the dev tool `voice_studio.py`. So `listen_judge.py` (a Gemini QA judge of TTS output) is not a precedent for listening to a learner. This is new engineering.

### Options for recognition

1. **Android `SpeechRecognizer` plugin** (`@capacitor-community/speech-recognition`): small, but depends on the Google speech service, is often online-only or needs a separate offline pack, gives no per-word timing, and is untested for children's voice or unseen pseudowords ("tas", "sta"). Reject as the primary route.
2. **WASM sherpa-onnx or whisper.cpp in the WebView**: avoids native code but needs SharedArrayBuffer for threads (cross-origin-isolated headers, not available from the Capacitor `https://localhost` scheme without extra work), so single-threaded WASM on a 2 GB phone. Adds `wasm-unsafe-eval` to the CSP. Reject for Android. Reasonable as a later PWA-only experiment.
3. **Native plugin wrapping sherpa-onnx (recommended)**: a small Capacitor Kotlin plugin: `AudioRecord` at 16 kHz mono PCM, push to a sherpa-onnx recogniser, emit `partialResult` / `finalResult` events to JS. Candidates: a small streaming Zipformer English model (about 20M parameters, likely 20-40 MB; check) or Whisper tiny.en int8 (about 40 MB; check). Only the app, not the Play Store listing, bears the cost: onnxruntime `.so` per ABI is probably 15-20 MB, which the AAB ABI split keeps to one ABI per device.

### The honest design: constrained scoring, not free dictation

Open ASR on a child or an Urdu-accented adult reading "tas" will fail often. The app knows the target word. Score with the target in mind: biased hotwords or keyword spotting in sherpa-onnx, or compare the recogniser's n-best against the target and its minimal-pair distractors. Output is "heard it / try again", never a grade that blocks progress. Always offer "I said it" self-grade. Treat speech as practice and as an assist to the Check step, not a gate, until measured.

### Capacitor / Android pitfalls to plan for

- `RECORD_AUDIO` must be in the manifest and requested at runtime. The WebView `getUserMedia` path needs the permission granted to the WebView through Capacitor's `BridgeWebChromeClient`; test on an actual Android 10 and Android 13 phone, not only the emulator. If using the native plugin, request through the Capacitor `Permissions` API.
- Android 11+ "Only this time" and Android 13 auto-reset of unused permissions: re-check permission state on each speaking screen rather than caching "granted".
- Audio focus: playing the model voice and recording at once causes echo and false recognition. Make it half-duplex: play, then beep, then record, never overlap. Detect headphones and relax.
- `MediaRecorder` in the WebView returns webm/opus, not PCM, so decode costs time. Prefer `AudioWorklet` or native `AudioRecord` for 16 kHz PCM.
- Cheap phones: noise-suppression and AGC differ per vendor. Keep a per-device calibration (a "say the word *sat*" check) and store only the metric.
- Privacy: audio is processed on device and not stored. Store only per-attempt metrics (`target`, `heard`, `ok`, `ms`). State this in the privacy page. Play Data Safety can then remain "No data collected" (the Urdu checklist answer), which must be re-checked against Google's current wording.
- The 16 KB page-size rule: the Urdu checklist notes it did not apply because there are no native libraries. Adding sherpa-onnx/onnxruntime changes that. Ship `.so` files aligned for 16 KB pages, and confirm the sherpa-onnx build you pick provides them.

### Permission flow for kids

1. First time the learner reaches a "Say it" step: show a grown-up-gated explainer (`askGrownup`, reused unchanged): "This lets the app hear your child read. Nothing is recorded or sent anywhere."
2. Only after the grown-up passes, call the system permission prompt.
3. If denied: show the same activity in self-grade mode ("I said it"), remember the choice per device, and surface a "Turn on listening" row in the parent screen. Do not re-prompt in a loop.
4. If "denied permanently": the row explains how to enable it in system settings (Capacitor core cannot open the settings page, so text instructions or a tiny plugin).
5. Families / kids policy review before release. The Urdu checklist says re-read the Families page before publishing (it changes often).

---

## 5. Platforms and budgets

- **Android APK/AAB first and PWA alongside**, same as Urdu: Capacitor 7.6 shell (Urdu repo) plus GitHub Pages PWA. Single codebase. Teacher laptops get the PWA.
- **minSdk**: Urdu is 23. With onnxruntime and a native plugin, 24 is the safe choice. I have not verified sherpa-onnx's own minSdk, so check it in the spike. targetSdk 36 as Urdu.
- **ABIs**: `arm64-v8a` and `armeabi-v7a`. Many budget Pakistani phones (Tecno, Infinix, Itel, Redmi A series) still run 32-bit userspace. Use AAB ABI splits so each phone downloads one.
- **Device target**: 2-3 GB RAM, 16-32 GB storage, Android 10-13 (Android 13 about 18%, Android 11 about 15% of Pakistan per the Urdu `09` notes, StatCounter). Android 8-9 stays "works if it works".
- **iOS later** (Capacitor already helps): `npx cap add ios`, needs a Mac and Apple Developer account ($99/yr). Costs: native Swift version of the speech plugin (sherpa-onnx has iOS builds), AAC audio packs, Kids Category review, and Safari PWA storage eviction (installed PWAs behave better). Estimate 1-2 weeks of work plus review time. Not in the 8 weeks.

### Performance budgets (measure on a real 2 GB phone)

| Metric | Budget | How measured |
|---|---|---|
| Cold start to first interactive | under 2 s | `adb shell am start -W -n <pkg>/.MainActivity` `TotalTime`; PWA: Lighthouse |
| Tap to lesson screen render | under 100 ms | `performance.now()` marks around `runLesson`; Playwright with CDP CPU throttle 6x as a proxy |
| First sound after tap | under 150 ms | pre-decode current lesson's clips into an `AudioContext` |
| JS shipped | under 150 KB gzip | Urdu is 240 KB + 169 KB lottie raw; make lottie lazy |
| Lesson JSON | under 50 KB each | build check |
| Memory without ASR | under 150 MB; with ASR under 300 MB | `adb shell dumpsys meminfo` |
| ASR load / end-of-speech to result | under 3 s / under 500 ms | spike |
| IndexedDB open | under 200 ms | existing 8 s timeout stays as a safety net |

---

## 6. Offline-first data

Keep the Urdu stores (`db.js`): `settings`, `profiles`, `attempts`, `cards` (Leitner), `sessions`, `progress`, `assessments`. Every record has `id`, `profileId`, `updatedAt`. Add:

```jsonc
// speech (metrics only, no audio)
{ "id":"…", "profileId":"…", "lesson":"L1.05", "target":"got", "heard":"got", "ok":true, "conf":0.82, "ms":1400, "ts":… }
// mastery (separate components per level, never blended)
{ "id":"profileId:L1", "profileId":"…", "level":1,
  "components":{ "letter-sounds":{"score":0.97,"pass":true}, "pseudo":{…}, "comprehension":{…} }, "at":… }
```

- **Profiles on a shared phone**: already built. Each learner row has name, track (child/adult/heritage), avatar, colour; the teacher PIN and `askGrownup` gate protect mode switches. Reuse as is. Cards, attempts and speech are all keyed by `profileId`.
- **Export/backup**: `backup.js` validates a JSON file with whitelisted stores, field checkers and size limits (`MAX_BACKUP_BYTES` 64 MB), shared via the Android share sheet. It merges by id and `updatedAt`, so two phones can be combined. Keep it exactly, change only `BACKUP_FORMAT` and the schema list.
- **Optional sync (later, off by default)**: Supabase, since Kamal uses it elsewhere. One table `sync_records(id text pk, owner uuid, store text, payload jsonb, updated_at timestamptz)` with RLS on `owner`, last-write-wins by `updated_at`, anonymous auth plus email magic link for a teacher or parent. Sync metrics only, never audio. Turning it on changes the Data Safety answer from "No data collected", so ship it behind a separate flag and a separate privacy page, and do not include it in the first store build.

---

## 7. Test and verification harness

### What exists in the Urdu repo

| Tool | Lines | What it does | English status |
|---|---|---|---|
| `mobile/tools/drive_all.py` | 137 | Playwright at 390x800; plays every lesson by answering from the audio key it just played (`HTMLMediaElement.play` is patched to record `window.__last`) and prompt regexes | Rewrite (below) |
| `mobile/tools/ui_audit.py` | 200 | Visits each screen type; checks tap targets, overflow, docked actions, hidden content, contrast | Reuse |
| `mobile/tools/shots.py` etc. | 15-124 | Screenshots, motion/feel sequences, onboarding, store shots, gate test | Reuse with selector edits |
| `scripts/store_judge.py` | 31 | Gemini judge of store screenshots | Reuse |
| `scripts/listen_judge.py` | 85 | Blind identify and A/B of audio clips with Gemini | Reuse for TTS QA, English prompts |
| `scripts/verify_audio.py` | 25 | Whisper smoke test | Reuse; or `faster-whisper` for word-level check of every clip |
| `scripts/leak_check.sh` | 23 | Secret/leak scan before publishing | Reuse |
| `scripts/content_metrics.py` | 151 | Content statistics | Adapt |
| `store/PLAY_CONSOLE_CHECKLIST.md` | 46 | Console steps | Template |

### What English needs added

1. **Decodability gate at build** (`tools/decodable.py` extended to the JSON): for each lesson, the cumulative GPC set at that lesson (from `data/gpc.json`) must cover every `decodable` word in `read`, `blend`, `check`. Heart words must be on the schedule. Story words at most 2 per text and flagged. Exit code non-zero fails `npm run build`. Also fail if a pseudoword is a real word (check against CMUdict and the lexicon) or is on a blocklist.
2. **Audio coverage check** (`tools/check_audio.py`): every text string, word, sentence, question and UI line in `content/` has a clip; every clip is referenced; clip hash equals `sha1(voice + text)`; manifest voice is a single value; duration inside 0.2-12 s; head/tail silence under 150 ms; loudness within 1 LU of target (`ffmpeg -af loudnorm=print_format=json`); and a Whisper pass confirms the spoken word equals the text (flag mismatches for `listen_judge.py` A/B repair).
3. **Every path reachable** (`tools/check_paths.py`): a graph walk from lesson 1, pass or fail, over `lessonsFor`, mastery gates and "reteach" targets. No orphan lesson, no dead end, no gate that cannot be passed with the content provided (e.g. Check lists at least 10 items so 90% is achievable).
4. **Oracle mode for `drive_all`**: a test build exposes `window.__oracle()` returning the correct answer for the current prompt. The Urdu driver parses prompt text with regexes that are tied to Urdu letter tables and are brittle. With the oracle the driver is about 40 lines, language-independent, and can also deliberately answer wrong to test the 90% gate and the reteach branch.
5. **No-cueing test**: a DOM check that no image or hint is present before a word is decoded (DESIGN.md rule 1).
6. **Parser snapshot tests**: golden JSON for `L1.02`, `L3.05`, `L4.03`, `L5.01`, so a markdown edit that breaks structure fails fast.
7. **Speech eval** (`tools/speech_eval.py`): a folder of labelled recordings (adult, child, Urdu-accented), run through the same model, reports word accuracy and false-accept rate per group.
8. **Perf test** (`tools/perf.py`): Playwright with CPU throttle plus real-device `am start -W`, recorded to a CSV so regressions show.
9. **Store judge** and `ui_audit` on every build.

---

## 8. Build order: 8 weeks, riskiest first

Riskiest unknowns, in order: (1) speech recognition accuracy on children and accented adults on 2 GB devices; (2) quality of isolated phoneme audio from TTS; (3) markdown parse yield; (4) native-library impact on size, ABIs, 16 KB rule and Play policy for a kids app with a microphone; (5) asset-pack download UX on poor connections; (6) Opus on old WebViews; (7) the course itself has had critic rounds but no field trial with real learners, so the pedagogy is unproven in the app; (8) a global audience whose UI instructions must be spoken, since pre-readers cannot read English prompts.

| Week | Work | Verifiable exit check |
|---|---|---|
| 1 (spikes) | (a) sherpa-onnx native plugin on one real 2 GB Android phone with 3 candidate models; test 30 target words + 10 pseudowords from 3 speakers. (b) TTS: render 20 words and 10 phonemes from two models, blind-judge with `listen_judge.py`. (c) Parser spike on L1.02, L3.05, L4.03, L5.01. (d) Opus playback on two real phones. | (a) numbers recorded: cold-load seconds, RSS MB, word accuracy per speaker; go/no-go on "speech gates anything". (b) phoneme identification at least 8/10 for the chosen method. (c) 4 of 4 files parse to the schema with `--strict`. (d) plays on both. |
| 2 | Repo from copied files; full parser over all 8 levels; `gpc.json`/`heart.json` extracted; decodability gate on JSON; ABI/size plan from week-1 numbers. | `npm run content` exits 0 for L1-L4 with 0 decodability violations; parse report shows 100% of lessons have `check` and `read`; `check_paths.py` passes on content only. |
| 3 | Audio pipeline for L1-L2 (words, sentences, UI, phonemes), content-addressed ids, per-lesson Ogg bundles; shell boots with English content: db, onboarding, path, session. | About 2,400 clips; `check_audio.py` passes; the app starts offline in a browser with airplane mode and shows the L1 path; Leitner cards seed from L1 GPCs. |
| 4 | Drills: blend, Elkonin segment, tile spell, pseudoword, heart word, discrimination, Check with 90% gate and reteach routing; Read with word highlight; Listen & Talk. | Oracle `drive_all` completes L1 and L2 end to end; a deliberate 80% run is blocked and routed to the reteach lesson; `ui_audit` has 0 violations. |
| 5 | Levels 3-4 content and audio; Tier-2 and questions; mastery checks as separate components; teacher/EGRA adaptation. | Decodability gate still 0; `check_audio.py` passes for L3-L4; EGRA subtask run saves an assessment with English band. |
| 6 | Speech feature behind a flag if week 1 said go; permission flow; self-grade fallback; asset packs: manifest, resumable download, hash verify; Levels 5-7 session screens. | On device: word accuracy at or above the week-1 agreed threshold on a 100-utterance set; 100 record cycles with no crash; pack download survives airplane-mode interruption and resumes; a deliberate bad hash is rejected. |
| 7 | Perf and low-end pass; a11y; backup/restore round trip; PWA to GitHub Pages; store assets with `make_store.py`; signed AAB with ABI splits. | Cold start under 2 s and lesson render under 100 ms on the target phone; backup exported from phone A restores on phone B with the same progress; AAB size at or under the budget (about 26 MB without ASR libs, plus the measured native delta). |
| 8 | Privacy page, Data Safety and Families answers, listing; upload to Play **internal testing**; start the closed-test clock if going for production. | Install from the Play internal link on two devices, finish L1 offline, no crash in Play pre-launch report. |

Notes: internal testing needs no tester minimum. Production access for a new personal account needs a closed test of at least 12 testers for 14 days (Urdu checklist section 5), which runs after week 8. If speech fails the week-1 spike, week 6 becomes the teacher mode and Leitner polish, and speech ships as self-graded practice only. Nothing else slips.
