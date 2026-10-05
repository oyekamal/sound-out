# Read English: the app plan, v1

Date: 2026-10-05. Owner: Kamal. Board task #118 (project english-reading-course).
Builder: one Opus session. Critics: four fresh agents (teacher, parent+adult, engineer, audio), per decisions.tsv.
Evidence: research-01 to research-05 in this folder, `english-reading-course/DESIGN.md`, and the store listings in `bar/`. Claims keep the reports' verification labels. "Unverified" means the source report said so.

---

## 0. Summary and the bar

**Summary.** Read English is a free Android app (with a PWA twin) that takes anyone, a 5-year-old or a 60-year-old, from "cannot read a letter" to reading critically in English. It runs the 108-lesson, 8-level course in `english-reading-course` (DESIGN.md) on a copy of the Urdu Qaida app shell (Capacitor 7, Vite, IndexedDB, Leitner review, pearl path, feel.js, resumable onboarding). Onboarding asks who is reading, never how old they are. Children get Track A, everyone else Track B. Both tracks run the same engine, the same letter-sound sequence and the same mastery gates. Every word, sentence and instruction is spoken by one voice, Kokoro-82M `af_heart`, rendered once on Kamal's laptop at build time and shipped as Opus files. The 44 isolated phonemes and the stretched blending demos are recorded by one human speaker, because no local model produced a teachable /s/ or /θ/ (research-02 §5). Nothing leaves the phone: no account, no ads, no analytics, no audio upload. The machine judges only what it can judge reliably: taps, tiles and typed spelling. On-device listening exists to confirm a correct answer, never to fail one, and it never promotes a learner on its own. Install size is about 27 MB, with later levels as download packs. The bar apps are 96–212 MB (bar/*.json).

**The bar.** RESUME.md fixes the bar. Features and experience: Duolingo ABC and Khan Academy Kids. Interaction: Teach Your Monster to Read. Pedagogy: DESIGN.md. Audio: the ElevenLabs Sara clips in urdu-reading-course. Kamal's brief adds Google Read Along and Learning Upgrade. The table shows what each lacks that we ship.

| We ship | Duolingo ABC | Khan Academy Kids | Google Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes (free, no ads, no IAP) | Yes (free, nonprofit) | Yes | **No**: iOS $8.99 (bar json); web free | **No**: $4.99/mo up to $59.99/yr (research-01) |
| Fully offline | Store listing claims it ("Enjoy playing and learning offline"). Current builds not tested (research-01 open item) | **Partial**: only downloaded books and games | Yes, after download | Not documented | No evidence found |
| Adult track, same skill sequence | **No**, preschool to grade 2 | **No**, ages 2–8 | **No**, ages 5+ | **No**, listing says ages 3–6 | Yes, but songs and video in English immersion, 3.2/5 on justuseapp |
| Placement and skip-ahead | **No**: "No option to skip ahead", "Kids can't choose where to start" (Common Sense, via research-01) | Adaptive, no explicit placement found | No placement | Not found | Not found |
| 90% mastery gate on real **and** pseudowords | No | No | No | No. Reviews say children "can progress by guessing" | No |
| Runs to fluency and critical reading (L5–L7) | **No**, stops at "very simple short stories" | Stops around grade 2 | Story practice only, no code teaching | Phonics phases 2–5 only | Partial |
| First-language support for the English code (Urdu first, then tags per language family) | No; users ask for other languages | Read-to-me in English or Spanish only | Story languages include Urdu, but no code instruction | No | Spanish and a few other onboarding languages |
| Listening that confirms correct answers and never fails a child | Speech required for some games, mixed reviews | Not found | On-device speech helper; the core feature | None | Not found |
| One consistent voice, accent stated | US | US | Per language | British narration, a US parent complaint | — |
| Install size | 212 MB (iOS, bar json) | 201 MB (iOS) | not verified | 96 MB (iOS) | not verified |

Store data from bar/*.json (US iOS App Store): Khan Kids 4.80 stars on 131,337 ratings. Duolingo ABC 4.25 on 3,810 ratings, last updated 2023-08-02, with "over 700 hands-on lessons" (Common Sense counted 127 units, so the two count different things). Teach Your Monster 4.47 on 29,802 ratings at $8.99. Reading Eggs 4.70 on 7,369 ratings, subscription. **Caution:** `bar/Read_Along_Kids_Books.json` is "Read-Along: Kids Books" by Smart Kidz Club, a different product. Google Read Along is Android-only and has no iOS listing, so every Read Along fact here comes from research-01.

Our position in one line, taken from the hooks nobody uses (research-01 §3.5): **free, offline, for any age, and it checks that you can really read.**

---

## 1. Who it is for, and the promise

**Promise:** "If you practise for 10 minutes most days, this app will teach you to read English from the first sound. It works without internet, costs nothing, knows nothing about you, and never makes you start over."

The time honesty comes from research-04 §2.2. One 14-lesson level is about 84 child sittings or 42 adult sittings. At five sittings a week, an adult needs about 8–9 weeks per level, and a child at one sitting a day needs longer. The parent summary says so.

### 1.1 Five archetypes, first 10 minutes

| | Ayesha, 5, Urdu at home | Leo, 7, native English | Bilal, 14, hides that he can't read | Rukhsana, 35, market stall worker | Nana Karim, 60, grandparent |
|---|---|---|---|---|---|
| Who holds the phone | Her mother | His father, then Leo | Bilal, alone, at night | Rukhsana, between customers | Himself; his grandson sometimes |
| Language screen | Mother taps اردو (the name is spoken) | English | English (he speaks it at school) | Urdu. She may not read Urdu well, so every control is an icon plus speech | Urdu |
| "Who is reading?" | "My child is reading, I will help" | Same | "I am reading" | "I am reading" | "I am reading" |
| Gate and setup | Mother passes the number-words gate. A 30-second helper intro, the judge's card (§3.9), the mic explainer, mic allowed | Same | None. Track B skin: no mascot, no confetti | Track B | Track B. App suggests "Reading comfort" (§3.12): large text, slower voice |
| Placement (§3.4) | Stage 0: mother answers four voice questions. Stage 1: tap-the-picture sound games. Ayesha misses the oral items. Placed at L1.01, the oral on-ramp | Stage 2 letter grid: 25/26 letters, 3/5 digraphs. Placed at L2.1 | Knows most letters. Stage 3 CVC tier: 8/8 real words, 5/8 pseudowords, so he has been memorising word shapes. Placed at L1.13 review with a fast track. The result is shown as "start here", never as a score | Stage 1 passes. Stage 2: 14/26 letters. Placed at the first missed letter, L1.4 | Stage 2: 26/26 letters. Stage 3 fails on digraphs. Placed at L2.1 |
| First sitting | 6 minutes: warm-up, Hear it (tap the picture that starts with /s/), Meet it (the letter s, the human /s/ clip, a mouth picture, the Urdu tip "same as س"). Ends with "You can stop here" and one pearl | 7 minutes: sh. Hear it, Meet it, blend ladder: sh-i-p | 12 minutes, adult wording. Review mini-check, then "I already know this: take the check" | 10 minutes: m, d. Spelling uses the tile tray because typing is slow for her | 12 minutes: sh, with large text and the voice at 0.9 speed |
| What the app has stored | Nickname, Track A, placement L1.01 (provisional: mother judged) | Track A | Track B, placement L1.13 | Track B, Urdu notes on | Track B, comfort settings |

### 1.2 Their first month

- **Ayesha** (one sitting a day, about 30): L1.01–L1.05 (s a t, p i n, m d). Her review deck holds about 10 letter-sounds and 8 heart words. Her mother judges the pseudoword items with the judge's card. Every lesson gate that passed with her mother judging is marked "mastered". On day 30 the grown-up area says: "Ayesha can read 40+ words made from s a t p i n m d. Level 1 has 14 lessons, so expect about 3 months at this pace."
- **Leo** (5–6 sittings a week): finishes Level 2 digraphs and blends and starts the L2 mastery check. Listening (where switched on) credits his clear real-word readings. His father confirms the gate.
- **Bilal**: fast-tracks the L1 review, then works through L2 at Track B pace (10–15 min). He passes or is parked privately, with no notifications and no one watching. His home screen shows "words you can read now: 312", not pearls. The app's icon and name don't look like a kids' app on a phone his friends might see (store listing, §7.6).
- **Rukhsana** (4 sittings a week, often interrupted): about 16 sittings, L1.4–L1.9. Each interruption resumes on the exact screen. The Level 0 print-concepts module (left to right, what a word is) runs first if her Stage 0 answers show no literacy in Urdu either. Her first real-world unlockable at the end of Level 1 is a price list.
- **Nana Karim**: L2.1–L2.7. His grandson is added as a second profile on the same phone. Nana's progress stays separate. His Track B reader texts are about the bus, the pharmacy and the phone.

---

## 2. The pedagogical engine: how anyone gets from zero to reading

### 2.1 The course mapped to the app

| Level | Lessons | Exit gate (DESIGN.md §3) | App content form | Sittings A / B (estimate) |
|---|---|---|---|---|
| 0 Start Here | placement, screener, Urdu guide, helper guide | placed | onboarding, placement flow, screener, helper intro | — |
| 1 First Sounds | 14 | CVC real + pseudo ≥90% | 9-block lessons split into sittings | ~84 / ~42 |
| 2 Sounds Together | 14 | CCVC/CVCC + 2-syllable closed ≥90% | same | ~84 / ~42 |
| 3 Long Vowels | 18 | vowel-team and VCe words ≥90%, ~40 WCPM equivalent | same | ~108 / ~54 |
| 4 The Full Code | 16 | multisyllabic pseudowords ≥90%; reads an ungraded simple text | same, plus off-ramp | ~96 / ~48 |
| 5 Word Power & Fluency | 16 | ~100+ WCPM with prosody on A2–B1 text | session template, 3 sittings each | ~48 |
| 6 Reading to Learn | 16 | B2 text | session template | ~48 |
| 7 Advanced & Critical | 14 | C1 | session template | ~42 |

The sitting counts multiply research-04 §2.2's ratio (6 child or 3 adult sittings per L1–L4 lesson, 3 per L5–L7 session). They are planning estimates, not measurements.

The master sequence and heart-word schedules (DESIGN.md §3) move out of `tools/decodable.py` into `data/gpc.json` and `data/heart.json`. These files are the single owner of order (research-05 §2). The app's path, the decodability gate, the pseudoword generator and the Leitner seeding all read them.

### 2.2 The strands inside every lesson

- **Code** (Hear, Meet, Blend, Spell, Heart words, Check): explicit grapheme-phoneme teaching, blend before segment, mastery gate.
- **Read it**: a decodable text in two registers. Track A carries the child text, Track B the adult text, with the same target patterns (rule 6). Three questions follow: two literal, one think.
- **Listen & Talk**: a passage read to the learner, above their decoding level, with 1–2 Tier-2 words and two discussion prompts. This runs from day one, so comprehension grows before decoding catches up (rule 7).
- **Review**: the warm-up block *is* the Leitner review (research-04 §3.3).
- **From L5**: morphology, fluency (model, assisted, independent), prime-the-topic, knowledge texts, reciprocal teaching, writing to read, and lateral reading at L6–L7.

### 2.3 Every rule, and how software enforces it

| Rule (DESIGN.md §2 + fixed decisions) | Mechanism in the app | Check that proves it |
|---|---|---|
| 1 No cueing | No picture or hint renders beside an undecoded word. Images appear only after a correct decode, or in Listen & Talk. Prompt strings come from a whitelist ("Point to each sound. Say the sounds. Blend."). "Does that make sense?" only appears after a decode | DOM test: no `img`/hint node in the reader or blend screen before `decoded=true` (research-05 §7.5). A string lint fails the build on "guess", "look at the picture" or "what makes sense" in pre-decode prompts |
| 2 Decodable = decodable (L1–L4) | Every word in `read`, `blend` and `check` is either decodable from the cumulative GPCs, a scheduled heart word, or a flagged story word (at most 2 per text) | `tools/decodable.py` on the JSON. Any unflagged violation fails `npm run content` (research-05 §7.1). Per-text audit stored in lesson JSON |
| 3 Blend before segment; letters with sounds | Step order in `lessonsFor()` is fixed: hear → meet → blend → spell. A letter is always shown with its sound clip | Snapshot test of step order per lesson. The oracle driver asserts that no spell step comes before blend for a new GPC |
| 4 Mastery gate, not calendar | Each lesson's Check uses the bar from its lesson file (mini-checks 5/5, 7/8, 9/11; Checks 9/10). The level check needs ≥90% on real **and** pseudowords, scored separately | Oracle driver runs a deliberate 80% pass, which must route to reteach. Path checker: every Check has ≥10 items, so 90% is reachable (research-05 §7.3) |
| 5 Heart words, never flashcard drilling | E8 heart-word map: sounds as dots, tap the heart part, rebuild. Heart words are not in Leitner as whole-word flash; the card is the map | No "flash" exercise type exists for heart words in the schema. Lint: every heart word has `heartIdx` |
| 6 Two registers, one skill | `read.A` and `read.B` are both required in L1–L4 lesson JSON. The skin picks one. The decodability gate runs on both | Parser fails if a lesson lacks B (or `sameAsA:true`). A word-list lint flags child-coded words in B (teddy, mummy, potty, ...) |
| 7 Comprehension from day one | `listen` is required in every lesson. Sittings are built so Listen & Talk is never dropped, only moved | Parser: 100% of lessons have `listen` |
| 8 Two metrics, never blended | Mastery store keeps components separate (letter-sounds, real, pseudo, heart, dictation, b/d/p/q, comprehension). The UI shows no blended score. WCPM without error marking is labelled "pace" | Schema has no `total` field. A UI test greps rendered progress for any single percentage across components |
| 9 Urdu / South-Asian notes | `l1_tags` per lesson. Notes are authored once per tag × language family and shown when the profile's home language matches | Lint: every lesson with v/w, th, short vowels or clusters carries the tag. Coverage report per family |
| 10 No streak-shaming, pause-safe; skip = take the check first | Days practised only goes up. A checkpoint is saved on every screen. Leitner is scheduled in sittings, not days. "I know this" opens the Check | Kill the app mid-step 20 times; it must resume on the same screen. A string lint bans "streak", "don't lose", "you missed" |
| 11 Multisensory optional | Trace and air-write are labelled "optional". Off by default in Track B | Settings test |
| 12 Honest citations | Store and in-app claims come from the evidence tables only | Listing review against §7.6 |
| Fixed: machine never promotes mastery alone | Gate evidence carries a `judge` value (`machine`, `helper`, `self`, `recognition`). `mastered` needs helper evidence on production items. Machine-only evidence gives `provisional` | Unit test of the gate reducer over every evidence combination |
| Fixed: audio never leaves the device | No network code in the speech module. Audio buffers stay in memory and are dropped after scoring. The only stored record is metrics | Static check: speech plugin has no network permission use. Proxy test: zero requests during 100 speaking attempts |
| Fixed: no ads, no account, no analytics | No ad, analytics or payment SDK in `package.json` or Gradle | Dependency allowlist check in CI |

---

## 3. Product

### 3.1 App structure

| Track A (child) tabs | Track B (teen/adult) tabs | Shared |
|---|---|---|
| **Path**: pearl necklace of lessons, the current pearl glows | **Lessons**: a plain list by level with a progress line | Grown-up area behind the gate: profiles, helper settings, backup/restore, listening on/off, reminders, reports, comfort settings |
| **Stories**: decodable readers already unlocked, plus Listen & Talk passages | **Read**: unlocked texts, real-world texts, from L5 the knowledge library | Profile switcher on the launch screen |
| **Practice**: Leitner cards due, games on known sounds | **Practice**: due cards, spelling, "words you can read now" list | "Hear it again" button on every screen |
| **Me**: stickers for each sound mastered, days practised | **Progress**: decoding / comprehension / fluency shown separately, days practised | Settings: language, look (switch skin), reading comfort |

The Urdu shell's `learner.js` already has Learn / Review / Read / Me (research-05 §1). We rename them per skin and do not add a fifth tab.

### 3.2 The sitting model

A sitting is one opening of the app: 1–4 block-units, then a "you can stop here" screen. A checkpoint is saved on every screen (research-04 §2.1).

- Budgets: Track A 5–8 min (3–5 min floor for very young learners), Track B 10–15 min.
- No sitting runs all 9 blocks. The Check is its own short sitting, or the last 2–3 minutes of a short one.
- One new GPC per sitting in Level 1.
- Hear it and Meet it can be re-run twice. A third miss raises a helper flag.
- Track B may merge sittings once a mini-check is passed (fast track).
- Splits come from the lesson file where it defines sittings (L1.02 A–D). Elsewhere they follow research-04 §2.2's table: Track A takes 6 sittings per lesson, Track B takes 3.
- L5–L7 sessions split into S-A (retrieval, word work, fluency), S-B (prime the topic, first half of the text with stop-and-check), and S-C (second half, reciprocal roles, write, check).

### 3.3 Exercise catalogue (consolidated from research-04 §2.4)

| ID | Type | Blocks | Input | Judge | No mic / no helper fallback |
|---|---|---|---|---|---|
| E1 | Sound game: tap the picture that starts or ends with the sound; tap dots to blend or segment | Hear, Warm-up, Placement stage 1 | tap | machine | none needed |
| E2 | Meet card: big letter, human phoneme clip, mouth picture, L1 tip chip | Meet | tap play | none | static mouth image |
| E3 | Sound tap: hear a sound, pick the letter from 2–4, confusables mixed in (b/d/p/q) | Warm-up, Meet, Check | tap | machine | none needed |
| E4 | Trace: start dot, arrows, checkpoints | Meet, Spell | finger | machine (formation only) | optional; off in Track B |
| E5 | Blend ladder: tap each grapheme (sound plays), slide to blend, hear the word. Human stretched demo on first exposure | Blend | tap, slide | none (modelling) | none needed |
| E6a | Say it: learner reads a shown word aloud | Blend, Read, Check | speak | machine witness for real words only (§5); helper for pseudo and heart words | → E6b |
| E6b | Hear and pick: audio plays a real word or pseudoword, learner picks the spelling from near foils (fape / fap / fepe) | Blend, Check, Placement | tap | machine (recognition) | gives a `provisional` gate |
| E7 | Spell: tiles (A) or keyboard with a tile fallback (B); sounds → words → one sentence | Spell, Check | tiles, keys | machine (exact match; error class tagged) | none needed |
| E8 | Heart-word map | Heart words | tap, tiles | machine | none needed |
| E9 | Decodable reader: word highlight, tap a word to hear it, 3 questions | Read | tap | literal = machine; think = self, then model answer | read-aloud audio; no mic needed |
| E10 | Listen & Talk: narrated passage, Tier-2 card, "your turn" sentence frames, 2 prompts | Listen | listen, tap, optional speak | none (formative) | choose 1 of 3 sentences, then the model answer plays |
| E11 | Check (mini and full): 5 real + 5 pseudo + 1 dictated, using the lesson's own bar | Check | mixed | machine for E3/E6b/E7; helper for spoken pseudowords | E6b path, `provisional`; a fresh pseudoword set (≥3 per check) on every retry |
| E12 | Retrieval card (Leitner) | Warm-up, L5+ | tap | machine | none needed |
| E13 | Morphology builder | L5+ word work | drag | machine | none needed |
| E14 | Phrase-cued echo reading | L5+ fluency | speak | self (machine optional, v2) | listen and follow: tap each phrase; counts as practice only |
| E15 | Timed read: 60 s, tap the last word reached | L5+ fluency | speak, tap | helper marks errors (v1); ASR (v2) | "pace", never "WCPM" |
| E16 | Prime the topic: picture or map description, 2–3 facts, a prediction tap | L5+ | tap | none | text-only variant |
| E17 | Long-text reader (§3.7) | L5+ | scroll, tap | machine (MCQ anchors) | none needed |
| E18 | Reciprocal teaching with a scripted partner (research-04 §2.5) | L6–7 | tap, type | machine on structure, self on content | none needed; no LLM |
| E19 | Write to read (§3.8) | all levels; extended from L5 | keys, dictation | self against checklist + machine key-term check (formative) | none needed |
| E20 | Lateral-reading sandbox: authored search results, "who is behind this page?" | L6–7 | tap | machine (authored best/ok/poor) | fully offline |
| E21 | Record and compare (new): learner records, then hears their own clip next to the model voice. The clip is never stored | practice in Blend, Read, Fluency | speak | self | hidden if no mic |

Distractors for E3, E6b and E7 are minimal pairs built at compile time from the lexicon: same length, one grapheme changed, already taught (research-05 §2).

### 3.4 Placement flow

Source: `course/level-0/placement-test.md`, stages 0–4. Rule: "stop each stage-type and place at the first point accuracy drops below 90%." Framed as "sound games and reading, to find where to start. Some words are made up. There is no pass or fail."

1. **Stage 0 intake (2 min)**: four voice questions on Yes / No / Skip cards. Do you know any English? Were you taught to read in another language? Is English your first language? Have languages always felt hard? Answers turn on Urdu notes and the print-concepts module.
2. **Stage 1 oral phonological awareness (~5 min)**: E1 items, no print. Failing early places the learner at L1.01.
3. **Stage 2 letter-sound grid**: Block A, 26 single letters (fewer than 24 → place at the first missed letter in L1 order). Block B, 5 digraphs (any miss → L2). Block C, 7 vowel teams and r-controlled (any miss → L3/4). Each block runs only if the previous one passed.
4. **Stage 3 decoding ladder**: tiers of 8 real + 8 pseudowords, spoken (helper-judged, or machine witness for real words) or E6b. If E6b was used, the placement is `provisional`.
5. **Stage 4 oral reading fluency**: only after CVC and digraphs clear. A 60 s passage, helper-marked. Skipped without a helper (or, in v2, ASR).
6. **Result**: "Start at Level N, lesson K", plus "Start earlier" and "Start later (take that check first)". No score is shown. Stored with a date and the `provisional` flag. Strong readers exit early, after about 5 minutes.

The item bank needs three equivalent forms so re-placement does not reuse items (content ask, §11).

### 3.5 Mastery, re-place, reteach state machine

| State | Enters when | Leaves to |
|---|---|---|
| `placing` | new profile, or "redo placement" | `in_lesson(L,k,s)` |
| `in_lesson(L,k,s)` | lesson unlocked | next sitting, or `gate(L,k)` after the last sitting. Closing the app saves the screen; no timeout |
| `gate(L,k)` | check sitting starts | `pass_mastered`, `pass_provisional`, `reteach` |
| `pass_mastered` | bar met **and** production items (spoken pseudo and heart words) judged by a qualified helper | next lesson; GPCs, heart words and Tier-2 words enter Leitner box 1 |
| `pass_provisional` | bar met with machine-only evidence (E6b, tiles, machine-witness real words) | next lesson; a re-check is scheduled 3 sittings later with fresh pseudowords. Passing it marks the lesson `secure` (app-checked twice). Only helper evidence upgrades it to `mastered` |
| `reteach(L,k,step)` | bar missed | the lesson's named reteach step ("reteach step 3, the silent-e reach-back"), then a re-check next sitting with a fresh pseudoword set |
| `parked(L,k)` | third miss on the same gate | repair mini-lesson from the previous lesson. Quiet helper flag. Next lesson's Hear/Meet only if this gate is not a hard prerequisite. Never past a failed gate. Copy: "This one is taking longer. That is common." |
| `skip(L,k)` | "I already know this" | `gate`: a pass skips the lesson, a fail starts it |
| `level_check(L)` | last lesson passed | pass → `replacement(L+1)`. Fail → reteach routed **by error class** to the weak lesson cluster, never to lesson 1 |
| `replacement(L+1)` | level check passed | runs the next level's placement slice (Stage 3 tier + fluency); fast learners jump ahead |
| `repair` (insert) | a Leitner GPC drops twice in a week | a short repair sitting is inserted before the next lesson |

Every check item carries an `error_class` from the lesson's tutor notes, so reteach targets the error, not the lesson. The level-check result always shows the pseudoword share separately. A high real-word score cannot hide memorised word shapes (placement-test.md calls pseudowords "the single most load-bearing design choice").

For the solo adult with no helper, the app never claims mastery of spoken production. The plain wording is "You can recognise and spell these" and "Checked twice". This follows the fixed decision and rule 8. It also leaves Rukhsana able to advance (D5, recommended default).

### 3.6 Spaced review

- **Decks**: GPCs, heart words, Tier-2 vocabulary, and from L5 morphemes. Real check words are not Leitnered. Pseudowords are regenerated fresh every time.
- **Boxes**: 5, scheduled in **sittings**: box 1 next sitting, then after 2, 4, 8 and 16 sittings. The Urdu `session.js` uses days `[0,1,2,4,8,16]`. We keep the box logic and change the unit (research-04 §3.3, research-05 §1).
- **Wrong answer**: drop one box. Two wrong in a row → box 1 (D7).
- **Cap**: 6–10 cards per warm-up, confusables interleaved (b/d, a/e).
- **Long gap**: no overdue pile. "Welcome back" runs 6 cards, oldest first.
- **FSRS**: only after real usage data exists.

### 3.7 Levels 5–7 reading on a phone

E17 rules, treated as defaults to test, not proven (research-04 §2.6):
- Text cut into 150–250-word screens with a progress bar. Sticky position, resumes at the last screen.
- Line length 30–45 characters. Andika font (SIL OFL, single-storey a and g), subset to Latin, about 30 KB.
- Tap-for-gloss on taught Tier-2 words only, so the app does not become a dictionary crutch.
- "Stop and check" anchors from the lesson files become literal and inferential MCQs, which also serve as pause points.
- Signal-word highlighter toggle (for the L6 text-structure work).
- Audio read-along is a toggle, off by default for text that feeds a fluency measure.
- Tested on a real 5-inch phone with two real learners before lock (week 7).

### 3.8 Writing to read

- **L1–L4**: dictation in every lesson (E7). Sounds, then words, then one sentence. Track A uses tiles, Track B the keyboard. Error classes (omitted silent e, missing blend letter) feed reteach.
- **Paper option**: "Write it on paper, then tap to see it." Self-check against the model. Formative only; no camera, so nothing to upload.
- **L5–L7**: E19 summary or response with sentence frames and a 4-point checklist. The machine checks that key terms are present (formative). The model answer appears after submission. Adults may dictate with the system keyboard's voice input, but the app warns that some keyboards send audio to the cloud. Our own mic path never does.

### 3.9 Helper and tutor mode

- **Helper** = any grown-up beside the learner. Set up once behind the gate. Before their judgements count toward `mastered`, the helper takes a **qualification**: five audio examples with planted errors (letter name for sound, "tuh" vowel added, gaps instead of a blend, long "aaa" for short a, right only after a long stare). They must mark all five correctly. This is the canvas plan's 5-planted-error qualification (research-04 §2.3). The examples are recorded by the same human phoneme speaker.
- **Judge's card**: on every helper-judged item, two big buttons, "Got it" and "Not yet", plus a one-line reminder of the five error types with a play button for each.
- **Who judges what** is labelled on screen in one plain sentence: "The app checks this." / "Ask your helper to listen." / "You decide."
- **Tutor/teacher mode** (D14): the Urdu `teacher.js` (roster, groups, reports, device mode, PIN, CSV share) is adapted in v1.1, not v1. `egra.js` maps to the English subtasks (letter sounds, nonwords, familiar words, passage, comprehension) and becomes the tutor's assessment screen.

### 3.10 Progress views

- **Learner (Track A)**: pearls on the path, one sticker per sound mastered, days practised.
- **Learner (Track B)**: "Words you can read now: N", where N counts lexicon words whose GPCs are all `secure` or `mastered`. Also the level line and days practised.
- **Grown-up area** (per profile): three separate panels: **Decoding** (letter-sounds, real words, pseudowords per level, each with `mastered/secure/provisional`), **Comprehension** (literal and think questions), **Fluency** (WCPM if helper-marked, otherwise "pace", with DIBELS ranges as reference only, never pass/fail; research-03 §5). Helper flags sit here too: parked gates, Stage 1 placement failed twice, screener 3+, low letter-sound recall after many reviews (research-04 §6.3).
- No blended score anywhere.

### 3.11 Motivation rules

Keep: days practised that never resets. Pearls and stickers for Track A. "Words you can read now" for Track B. Real-world texts (price list, bus ticket, SMS, pharmacy label) unlocked at level ends. Effort praise, not "smart". Soft errors: a hint, "try again", no red X and no failure sound in Track A.

Refuse: streaks with loss framing, streak freezes, hearts/lives, leagues, leaderboards, guilt-copy notifications, celebrating each tap. Celebrate the gate pass, not every correct pseudoword.

Reminders: opt-in, local, neutral ("A 10 minute sitting is ready when you are"), at most one a week by default, off for Track A unless the parent turns them on (D13). The notification prompt appears only after the first completed sitting.

### 3.12 Accessibility and reading comfort

A "Reading comfort" screen, not labelled "dyslexia" (research-04 §6.1):
- Text size, line spacing, a letter-spacing slider (default slightly wider; no claim that it treats dyslexia), left-aligned text.
- Background tints and high contrast as preferences, with no efficacy claim.
- OpenDyslexic offered as a choice only, not the default (Wery & Diliberto 2017 found no benefit).
- Voice speed 0.8 / 0.9 / 1.0, applied by playback rate with pitch preserved. This needs no second render. Test that pitch preservation sounds clean on WebView before shipping.
- Reduce motion. Touch targets 60–80 px for Track A, ≥48 px for Track B. Every control has an icon and a spoken label. Live regions and a focus trap (`a11y.js`).
- "Which looks easier?": a two-screen A/B where the learner's choice becomes the setting.
- The Level 0 screener is offered after placement. It is private, skippable and never gates anything. The learner-facing result never uses the word "dyslexia" (research-04 §6.2).

### 3.13 The "any age" onboarding script

The engine is `onboarding.js`: 17 screens, saved after every step, resumable. Every line below is spoken in the UI language and shown as icon plus text.

1. Language grid. Each language name is in its own script and spoken when tapped. *"Choose your language."*
2. *"Who is reading?"* Card 1, person icon: *"I am reading."* Card 2, adult + small figure: *"My child is reading. I will help."*
3. (Card 2) Gate: *"Grown-ups: tap the number seven."* (the number spelled out in words). Then the helper intro (30 s), the judge's card, the mic explainer: *"The app listens only while the ring is glowing. Nothing is recorded or sent anywhere."* → system mic prompt, or "Not now".
4. (Card 1) Track B. *"You can change how the app looks any time in Settings."* Mic explainer without a gate: *"Want the app to listen when you read? It stays on this phone."*
5. Nickname (optional, stays on the phone). Avatar for Track A.
6. Demo: s + a + t builds "sat" (replaces the Urdu demo بابا; research-05 §1). Three taps, with the human /s/ /æ/ /t/ clips and the Kokoro "sat".
7. Placement (§3.4).
8. Result. *"Start here. You can change this."*
9. Screener offer (skippable).
10. The first sitting starts. No account, no email.

### 3.14 Screens list

Launch / profile picker · Language · Who is reading · Grown-up gate · Helper intro + qualification · Mic explainer · Nickname/avatar · Demo · Placement stages 0–4 · Placement result · Screener · Home (Path / Lessons) · Sitting runner (hosts E1–E21) · Stop-here screen · Check result (pass / reteach / parked wording) · Level check result · Stories/Read library · Reader (E9 / E17) · Listen & Talk · Practice · Me / Progress · Grown-up area (profiles, reports, helper, listening, reminders, backup/restore, pack downloads, about/licences, privacy) · Reading comfort · Settings · Pack download manager · Room check (noise test before listening) · Welcome back.

---

## 4. Voice: the audio system end to end

### 4.1 Clip inventory and size

Counts come from research-05 §3 (a script over the course markdown, learner-facing text, ±25% on sentences). Clip sizes: research-05 budgets 2.5 KB per word and 12.5 KB per L1–L5 sentence (4 s at 24 kbps mono Opus ≈ 3 KB/s plus 0.4 KB container). L6–L7 sentences average 15 words, so 5.5 s and 17 KB. research-02 §4 *measured* 1,772 bytes per trimmed Kokoro af_heart word, so 2.5 KB is a safe ceiling.

| Clip type | Source | Count | Size each | MB | Math |
|---|---|---|---|---|---|
| Words, learner-facing, L1–L7 | Kokoro af_heart | 5,763 | 2.5 KB (1.77 measured) | 14.4 (10.2 at measured size) | 5,763 × 2.5 |
| Generated pseudowords (fresh check sets) | Kokoro via IPA | ~1,000 (my estimate, below) | 2.5 KB | 2.5 | 1,000 × 2.5 |
| Sentences L1–L5 | Kokoro | 2,224 | 12.5 KB | 27.8 | (297+515+385+297+730) × 12.5 |
| Sentences L6–L7 | Kokoro | 1,322 | 17 KB | 22.5 | (823+499) × 17 |
| Level 0 words and prompts | Kokoro | ~190 | 2.5–12.5 KB | ~0.5 | research-05 notes 187 quoted words |
| Tier-2 definitions and examples | Kokoro | ~360 | 12.5 KB | 4.5 | 60 lessons × 2 words × 3 lines |
| UI and instruction lines (English) | Kokoro | ~200 | 9 KB | 1.8 | research-05 extras |
| Isolated phonemes | **Human** | 44 × 2 shipped takes = 88 | ~2.3 KB | 0.2 | short clips |
| Stretched blending demos (L1–L2) | **Human** | ~66 (my estimate: 22 lessons × 3) | ~9 KB (3 s) | 0.6 | 66 × 9 |
| Judge's-card error examples | **Human** | ~10 | ~6 KB | 0.06 | 5 error types × 2 |
| **Total** | | **~11,200 clips** | | **~75 MB ceiling, ~71 MB at measured word size** | |

The pseudoword estimate: L1–L4 have 62 lessons. Each needs ≥3 fresh check sets of 5 pseudowords (research-04 E11), about 15 beyond the markdown's blend list, so 930. Add 4 level checks × 3 sets × 10 = 120. Some already exist in the markdown tables, so ~1,000 new is a round planning number.

Earlier figures: research-02 §7 estimated ~55 MB from 10,500 words × 1.8 KB plus 3,000 sentences × 12 KB. That word count was a guess from the brief. research-05 counted the real corpus. **We plan on ~75 MB** and treat research-02's number as superseded.

On-disk waste: 5,763 small files at 4 KB filesystem blocks take ~23 MB, not 14. Clips ship as one concatenated Ogg Opus bundle per lesson plus an offset index, sliced with `Blob` at play time (research-05 §3). That also gives one request per lesson.

**Delivery:**

| Pack | Contents | MB (approx.) | How |
|---|---|---|---|
| Base (in AAB / PWA precache) | Shell (~8 MB: JS, Lottie, Andika, images) + L0 + L1 + L2 audio + UI + phonemes + demos + L1–L2 Tier-2 | ~19 MB audio → **~27 MB AAB** (Urdu AAB is 27.8 MB) | bundled |
| L3–L4 | words, sentences, Tier-2, pseudowords | ~13 | downloaded |
| L5 | | ~12 | downloaded |
| L6 | | ~18 | downloaded |
| L7 | | ~11 | downloaded |
| Listening model (v1 beta / v2) | sherpa-onnx model | 40–123 (per model, §5; unverified until the spike) | downloaded, optional |

A pack downloads when the learner is one level away from it, on Wi-Fi by default, or on mobile data if the grown-up allows it. It can also be side-loaded from another phone's export (§6.6). Mechanism (research-05 §3): the APK writes to `Directory.Data` via `@capacitor/filesystem`, the PWA uses the Cache API. Both use a hash manifest, resume per file, verify the hash, then call `navigator.storage.persist()`. Play Asset Delivery is deferred: it needs a native bridge and the PWA gets nothing from it.

Opus in Ogg plays in Chrome and Android WebView. This must be verified on two real Android 10 phones in week 1. iOS gets AAC `.m4a` packs later (~30% larger).

### 4.2 Kokoro pipeline

`tools/render_audio.py`, run on Kamal's laptop. Kokoro 0.9.4 + misaki 0.9.4 were already installed during research-02.

1. **Inputs**: `content/lexicon.json` (each word with graphemes `g` and phonemes `p`), `content/lessons/*.json` (sentences, questions, Tier-2 lines), `content/ui.json`.
2. **Pronunciation source per item**:
   - Real words: misaki G2P. If misaki returns out-of-vocabulary, the build **fails** unless `data/pron.json` holds an IPA override. Reason: the espeak-ng fallback crashes on this machine (research-02 §3), so OOV words would otherwise come back silent.
   - Pseudowords: **always IPA** from the lexicon's `p` array. That array is derived from the GPC table, so it is deterministic by construction (research-05 §2).
   - Heteronyms and context words get explicit IPA in `data/pron.json`. The list: read, live, lead, tear, wind, bow, close, use, does, wound, minute. Also "a" (/ə/ as an article, /eɪ/ as a letter name) and "the" (/ðə/).
   - -ed allomorphs in L2.10 (/t/ /d/ /ɪd/) are checked against the lesson's own lists.
   - Accent: `af_heart` is American, so the GPC table's `ipa` fields are written in General American (short o = /ɑ/, r-colouring kept). The human phoneme speaker matches this (D15).
3. **Fixed render settings**: model sha, voice `af_heart`, speed 1.0 for words and sentences (0.9 allowed only for L1–L2 sentences if the A/B shows it helps; decided once, applied to the whole tier), 24 kHz.
4. **Post-process**: `silenceremove` (head and tail under 150 ms), peak-normalise to −3 dBFS, then loudness normalise to one target ±1 LU, Opus 24 kbps mono.
5. **Clip id** = `sha1(voice + model_sha + normalised text + ipa_override)[:10]`. Unchanged text never re-renders, and reordering a list never breaks keys (research-05 §2).
6. **Manifest** `audio_manifest.json`: per clip `text`, `ipa`, `method` (`kokoro`/`human`), `voice`, `model_sha`, `speed`, `duration_ms`, `lufs`, `qa` (`auto_pass`, `judge`, `human`), `rerolls`.
7. **Throughput**: research-02 measured Kokoro at 1.3–2 words/s single-process, and 1.0–1.5 s per short sentence. ~11,200 clips ≈ 3–4 hours single-process. Four processes in parallel is an estimate of about an hour. Fine for a one-off build.

### 4.3 QA loop

| Stage | What | Applies to | Pass rule |
|---|---|---|---|
| Q1 automatic | `tools/check_audio.py`: every content string has a clip and every clip is referenced; hash matches; one voice in the manifest; duration 0.2–12 s; silence < 150 ms; loudness within 1 LU; no clipping | 100% | all pass, or the build fails |
| Q2 ASR check | faster-whisper word check: transcript equals text (real words and sentences only; Whisper snaps pseudowords to real words, so they skip this) | real words, sentences | mismatch → Q3 |
| Q3 blind judge | `listen_judge.py` (Gemini, English prompts): "which word is this?" with no text given; A/B against the re-roll | 100% of pseudowords, all Q2 mismatches, 10% random words | judge names the target, or Q4 decides |
| Q4 human spot-check | Kamal (and a native-speaker reviewer for pseudowords if one is found) listens in a review page built from `voice_studio.py` | all pseudowords (~1,360), all Q3 fails, the 5% lowest-confidence words, and a frozen random 200 per pack | ≥98% of the random 200 judged clear and correct, or the pack is blocked. Flagged clips are re-rolled |

Two cautions apply. research-02 §9 notes that no human has listened to any of the bakeoff clips yet, and that Gemini Flash judgements on sub-second audio are noisy. So Q4 decides, and Q3 only triages. The first full listen to a 100-clip L1 set happens in week 1.

### 4.4 Consistency rules

1. One synthetic voice (`af_heart`), one model sha, one speed per content tier, for the life of a major version. Changing any of them re-renders everything and goes through Q1–Q4 again.
2. A word in a list and the same word inside a sentence may differ, as natural speech does. The word clip is the citation form, and the reader's tap-to-hear plays the word clip.
3. Human clips come from one speaker, one microphone and one room, in sessions with the same settings (§4.6), and go through the same loudness target as Kokoro.
4. No fallback voice inside one install. `bf_emma` is a whole-app alternative only if D15 picks British, and it needs a human check first (research-02 §5 found its letter names unreliable).

### 4.5 Re-roll policy

Kokoro has no sampling drift (research-02 §7), so a "re-roll" means changing the input, in this order:

1. IPA override in `data/pron.json`.
2. Speed 0.9 for that one clip (allowed within the tier's rule).
3. Carrier phrase: render "the word sat.", forced-align, crop to the word.
4. After 3 failed re-rolls, the clip joins the human recording queue for the next session with the phoneme speaker. It is marked `method: human` in the manifest.

Expected human share: unknown until week 1. If more than 2% of words need a human voice, the plan changes: re-test `bf_emma` or Chatterbox, which research-02 lists but did not test. This is a risk item (§9).

### 4.6 Human recording kit

- **Speaker** (D16, blocks week 1): one adult whose isolated phonemes are identified correctly by two blind listeners (≥42/44), and whose short vowels match the General American values in the GPC table. A female speaker sits closest to `af_heart`, but correctness matters more than gender. Candidates are auditioned in week 1 with a 10-phoneme screen.
- **Conditions**: quiet small room with soft furnishings, phone or USB mic at 20–30 cm, pop filter or off-axis placement, 48 kHz mono WAV, no AGC or noise suppression. The same session settings every time. Tool: `scripts/voice_studio.py` (browser recorder, research-05 §1).
- **Script and list (44 phonemes, General American)**: 3 takes each, best 2 shipped (one for Meet it, one for warm-up variety).
  - Continuants, held ~0.8–1.0 s: /m/ /n/ /s/ /z/ /f/ /v/ /θ/ /ð/ /ʃ/ /ʒ/ /l/ /r/ /h/ (/h/ as a short breath).
  - Stops, short and clipped, **no added vowel**: /p/ /b/ /t/ /d/ /k/ /g/ /tʃ/ /dʒ/.
  - Other consonants: /w/ /j/ /ŋ/ (ŋ held). The x clip is the sequence /ks/, and qu is /kw/, as course clips.
  - Short vowels, held ~0.6 s: /æ/ /ɛ/ /ɪ/ /ɑ/ (short o) /ʌ/ /ʊ/.
  - Long vowels and diphthongs: /eɪ/ /iː/ /aɪ/ /oʊ/ /uː/ /juː/ /ɔɪ/ /aʊ/ /ɔː/.
  - R-controlled: /ɑr/ /ɔr/ /ɝ/ /ɛr/ (air) /ɪr/ (ear).
  - Schwa: /ə/.
  - The exact list is reconciled against `data/gpc.json` in week 2. Every `phoneme` value there must have a human clip, or the audio coverage gate fails.
- **Blending demos**: for each L1–L2 lesson, 3 words, each "stretched then said" (s-a-t → "sssaaat" → "sat"). ~66 clips.
- **Judge's-card error examples**: letter name for sound ("ess" for /s/), "tuh", gapped blend "s… a… t", long "aaa", hesitate-then-right. ~10 clips.
- **Per session**: record a room-tone sample and the reference vowel /æ/ first. Compare against the first session's reference to keep the voice steady. Post-process: trim, light high-pass at 70 Hz, loudness to the shared target.
- **Consent and licence**: the speaker signs a short release granting perpetual, worldwide, commercial redistribution of the recordings within the app and its packs.

### 4.7 Licence table

| Asset | Licence | Status / action |
|---|---|---|
| Kokoro-82M weights and code | Apache-2.0 | research-02: assumption from the model card, training-data claims not verified line by line. Record in `LICENSES.md` with the version |
| misaki G2P | per repo (check) | verify in week 2 |
| Generated audio | ours (from an Apache model) | state "voice generated with Kokoro-82M" in About and the listing (AI-voice disclosure) |
| Human phoneme recordings | release signed by speaker | week 1 |
| Course content | CC BY 4.0 (english-reading-course LICENSE) | attribute in About |
| Andika font | SIL OFL | verify, bundle the licence |
| Piper engine / voices | GPL-3 engine; lessac-derived voices research-only | **not used** (research-02 §2) |
| sherpa-onnx | Apache-2.0 (research-03 marks it background knowledge) | verify before the week-1 spike |
| whisper.cpp | MIT (verified, research-03) | if used |
| Whisper / Moonshine models | MIT for current English models (research-03) | verify per model file |
| charsiu / charsiu-js (v2) | MIT | vendor and pin |
| OpenMoji (if used for pictures) | CC BY-SA 4.0 | check share-alike implications for the app before use |
| Lottie (Marko rig, if kept) | ours | — |

### 4.8 What still fails, and how we handle it

| Failure | Handling |
|---|---|
| Isolated phonemes from TTS | Human recorded (fixed decision) |
| Stops cannot be said purely, even by humans | Short, clipped release. The Meet card says "short sound". Placement and checks use words, not isolated stops, for production |
| Pseudowords misheard (research-02: vop→"vob", chote→"Chode") | IPA input + Q3 on 100% + Q4 on 100% + re-roll ladder |
| Real-word confusions (ship→"chef") | Q2 Whisper pass + Q3 + Q4 on flagged clips |
| `af_heart` child sentence rated 2/5 naturalness by the judge, unexplained (research-02 §6) | Week-1 human listen of 50 Track A sentences. If the problem is real, try speed 0.9 for L1–L2 sentences, then a carrier-phrase render |
| No child voice | Accepted. Track A uses the same warm adult teacher voice. Cloning a child voice is out of scope (watermark and consent issues, research-02 §7) |
| Dynamic text (teacher-typed words) | Not supported in v1. A later on-device Kokoro via sherpa-onnx int8 is untested (research-02 §9) |
| Opus on old WebViews | Week-1 device test. Fallback: AAC packs |

---

## 5. Listening

### 5.1 Principle: verification, not recognition

Open ASR "repairs" what it hears: "sut" becomes "sat", and the alien word "blop" becomes a real word. The app always knows the target, so it asks a different question: did this audio match **this** phoneme string better than its plausible wrong versions? (research-03 §0, §4). Output has three states. Only one of them credits:

- `clear_yes`: credit the item, chime.
- `unsure`: "Let's do it together." The model voice plays, then a free retry or the helper's tap.
- `clear_no`: shown to the learner **exactly like `unsure`**. Logged as `machine_no` for the helper view, never as a fail.

A machine "no" never costs the learner anything. A machine "yes" never promotes a gate on its own (§3.5).

### 5.2 What the machine judges, by version

| Item | v1 (8-week build) | v2 (after the gold set) | v3 |
|---|---|---|---|
| Receptive taps (E1, E3, E6b) | machine, perfect, no ASR | same | same |
| Tiles and typed spelling (E7, E8) | machine | same | same |
| Isolated sound produced | helper only | weak; try only for fricatives and vowels with a long steady state | — |
| Real CVC/CCVC word read aloud (E6a) | **witness**: sherpa-onnx native plugin running Whisper tiny.en/base.en int8 or a small Zipformer (spike decides), word list constrained to target + minimal-pair foils; `clear_yes` only on exact target match above threshold. Behind a "Listening (beta)" switch, **off by default** in the public build unless the class passes the gold-set test (§5.6) | phoneme-CTC forced alignment with a competitor set (charsiu-class wav2vec2 frame classifier, ~123 MB INT8, research-03 §1) | fine-tuned on consented, locally exported clips |
| Pseudowords | helper, or E6b `provisional` | phoneme-CTC with known IPA, validated per phoneme; Urdu-accent risk | — |
| Heart words | helper | helper (irregularity is the lesson) | — |
| Sentence read | helper | word-level ASR vs text, as a witness only | — |
| Passage, WCPM | helper-marked (E15) or "pace" | Whisper/Moonshine + alignment, trend only, "approximate" | — |
| Prosody | helper listening | crude proxies (pause length, pace variance) | v3 |
| Mastery gate | never machine alone | never machine alone | never machine alone |

**Engine choice.** research-05 §4 recommends a native Kotlin Capacitor plugin wrapping sherpa-onnx (AudioRecord 16 kHz PCM → recogniser → JS events). It rejects WASM in the Android WebView, because SharedArrayBuffer needs cross-origin isolation the `https://localhost` scheme lacks, which leaves single-threaded inference on a 2 GB phone. research-03 §1 says onnxruntime-web runs inside the WebView. Both are true. We use the native plugin on Android and keep WASM for a PWA-only experiment. The v2 phoneme model is exported to ONNX and runs through the same native onnxruntime. charsiu-js stays the reference implementation.

### 5.3 Pipeline for one spoken item

1. Half-duplex: play the prompt → beep → open the mic. Never overlap with playback (research-05 §4).
2. Track A: hold to talk (push the big ring). Track B: tap, then auto-stop by VAD (silero-VAD via sherpa-onnx).
3. Pre-gates. Any of these gives `unsure`, never `no`: duration < 150 ms, clipping, SNR < ~10 dB, more than one speaker detected, no speech.
4. Decode, constrained to the target and its competitor set: minimal pairs from the lexicon, vowel swaps (/sɪt/ /sʌt/), dropped final (/sæ/), first-sound swap (/tæt/), and schwa epenthesis (/səæt/ "suh-at").
5. Decision is the margin between the target and the best competitor (v2), or exact match plus confidence (v1). Thresholds come from §5.6, set per item class.
6. Store metrics only: `{lesson, target, heard, state, conf, ms, ts}`. The audio buffer is dropped.
7. Three `unsure` in a row on one screen → hand over: helper judge, or E6b for this item.

### 5.4 Thresholds (targets, from research-03 §8)

| Metric | Target to switch on machine credit for an item class |
|---|---|
| `clear_yes` precision (humans agree it was right) | ≥97%, lower 95% CI ≥92%, on ≥60 items per child, both kids, both conditions |
| `clear_yes` recall among human-correct items | ≥60% (otherwise it only annoys) |
| `clear_no` precision | ≥90%, otherwise demoted to `unsure` (it is never shown as a fail anyway) |
| Latency, end of speech to result | p95 < 3 s (research-03), p50 < 500 ms target (research-05 budget) |
| Mic stability | 0 failures in 20 relaunch cycles (record, close, relaunch, record) |

The 5-year-old and the 7-year-old are reported separately. Results are not pooled.

### 5.5 Room check, permission, no-mic path

- **Room check**: before the first speaking exercise of a sitting, one second of ambient level. If it is too noisy: *"Too noisy for listening. Move closer, or your helper can judge."*
- **Permission**: requested only when a speaking exercise first appears. For Track A the grown-up passes the gate first. On denial: self-grade or helper mode. The choice is remembered and there is no re-prompt loop. A "Turn on listening" row sits in the grown-up area. Permanent denial shows text instructions for system settings. Permission state is re-checked on every speaking screen (Android 11 "only this time", Android 13 auto-reset).
- **No mic or no permission**: E6a becomes E6b, E14 becomes listen-and-follow, E15 becomes "pace". Placement Stage 3 uses E6b (`provisional`). Nothing is blocked.

### 5.6 Kid test protocol (before trusting any machine credit)

Pre-registered. No teaching during the test (research-03 §8).

1. **Gold set**: per child (5 and 7), 100 items over 3–4 sessions of ≤8 min each: 20 isolated sounds, 40 real CVC words, 20 pseudowords, 10 heart words, 10 sentences. Kamal labels each item correct / wrong-type / unclear. A second adult independently labels a random 30 for inter-rater agreement.
2. **Planted errors**: Kamal mispronounces 30 items in a child-like way (letter name, "tuh", long aaa, gaps). Adult imitations are easier than real child errors, so treat the result as a floor.
3. **Conditions**: quiet room, the real room with TV and fan, phone at 30 cm and at 1 m, the family phone (not a laptop), battery saver on.
4. **Also**: 3 adults (Kamal, one Urdu-first adult, one older adult) with 40 real words and 20 pseudowords each, for Track B.
5. **Metrics**: as §5.4, per item class and per speaker.
6. **Go/no-go**: an item class moves from helper-judged to machine-witness-credited only if it meets §5.4. Pseudowords and isolated sounds are *expected* to fail in v1, and that is a valid answer.
7. **Child experience**: no tears, no "it didn't hear me" loops, handover after 3 `unsure`.
8. Repeat after any change of model, threshold or phone. The gold set stays frozen, and each round adds a fresh held-out set.

Clips for the gold set are stored only in a gated "Research recording" mode. The parent consents on screen, files sit in app-private storage, and they are exported by hand via the share sheet. Never uploaded. Off in store builds.

### 5.7 WCPM method

- **v1**: E15. A 60 s timer. The helper taps each misread word on their view of the passage. Self-corrections within 3 s don't count as errors. Repetitions are ignored (DIBELS-style rule, research-03 marks it background knowledge). WCPM = (words reached − errors) per minute. With no helper, the result is labelled "pace".
- **v2**: Whisper base.en or Moonshine transcribes the passage reading. The transcript is aligned to the known passage with word-level Needleman-Wunsch. Correct words are counted, substitutions and omissions subtracted, and the count stops at 60 s. Shown as "approximate". Expected within ±5–10 WCPM of a human count on clean audio (research-03, unverified), biased toward under-counting children.
- **Reference ranges** on the grown-up page only: DIBELS 8 Grade 1 ORF (beginning 35+, middle 57+, end 76+; verified PDF, research-03 §5). Grade 2+ and Hasbrouck-Tindal norms are not fetched, so they are not shown until someone fetches them.

### 5.8 Privacy

Audio is processed on the phone, in memory, and discarded. Only metrics are stored, in the `speech` store, inside backups the user exports themselves. No network code in the speech plugin. The COPPA amendment counts voiceprints as personal information (research-04 §5), so we do not create, keep or send any. The privacy page says this in each UI language. Play Data Safety stays "No data collected" (to be re-checked against Google's current wording before submission; research-05 §4).

---

## 6. Tech

### 6.1 Repo plan

- New repo `read-english` (`appId com.oyekamal.readenglish`). Files are copied once from `urdu-reading-course/mobile`. `PROVENANCE.md` lists each copied file with the Urdu commit hash. No fork and no shared package until both apps ship (research-05 §1).
- Reuse summary (research-05 §1): AS-IS 449 lines (12%: `safe`, `gate`, `fx`, `motion`, `swreg`, `restore`, `premium`). WITH CHANGES 2,702 (70%: `db`, `backup`, `session`, `path`, `learner`, `onboarding`, `teacher`, `egra`, `feel`, `a11y`, `dashboard`, `practice`, `main`). Brand decision 391 (10%: `marko`, `memory`, `stickers`, `icons`). REWRITE 313 (8%: `drills`, `content`).
- Scripts: `ui_audit.py`, `shots.py`, `store_judge.py`, `leak_check.sh` as-is. `listen_judge.py` and `voice_studio.py` with English prompts. `drive_all.py` rewritten around an oracle. The Urdu TTS scripts are replaced by `render_audio.py`.
- Layout:

```
read-english/
  app/            Vite + Capacitor (copied shell)
  android/        Capacitor Android project; plugins/speech (Kotlin, sherpa-onnx)
  data/           gpc.json, heart.json, pron.json, blocklist.txt  (machine-critical truth)
  content/        built JSON (git-ignored, produced by tools/)
  audio/          built Opus bundles + audio_manifest.json (LFS or release assets)
  tools/          build_content.py, decodable.py, gen_pseudo.py, render_audio.py,
                  check_audio.py, check_paths.py, speech_eval.py, perf.py
  tests/          parser snapshots, oracle driver, DOM no-cueing test, gate reducer tests
  store/          listing text per language, screenshots, PLAY_CONSOLE_CHECKLIST.md
  LICENSES.md  PROVENANCE.md  PRIVACY.md
```

- The course repo stays the content source. A pinned commit of `english-reading-course` is pulled in as a git submodule or a release tarball. `build_content.py --strict` reads it.

### 6.2 Content pipeline and schema

The parser is `tools/build_content.py` (Python stdlib, research-05 §2). It builds a heading tree, maps headings to step types by keyword, and extracts by block type: pipe tables → word lists, `>` after a Track heading → texts, Tier-2 bullets, question lists, Check rows. `--strict` fails on an unknown heading. Findings are fixed by normalising the markdown (L1 mixes `##` and `###` for "Read it"), not by special cases in the parser.

Schema (adopted from research-05 §2, with additions marked ★):

```jsonc
// content/gpc.json — one entry per grapheme–phoneme pair
{ "s": { "id":"s", "kind":"letter", "ipa":"s", "phoneme":"/s/", "intro":"L1.02",
         "mouth":"teeth close, air hisses", "audio":"ph.s", "examples":["sat","sun"],
         "l1_tags":["…"], "locale":{"ur":"Same as Urdu س"} } }

// content/lexicon.json — every word the learner can meet
{ "sat":  { "g":["s","a","t"], "p":["s","æ","t"], "kind":"decodable",  // decodable|heart|story|tier2|pseudo
            "intro":"L1.02", "audio":"w.9f3a1c", "img":null, "level":1,
            "foils":["sit","set","mat"] /*★ minimal pairs*/, "pron":"misaki|override" /*★*/ },
  "said": { "g":["s","ai","d"], "p":["s","ɛ","d"], "kind":"heart", "heartIdx":[1], "intro":"L1.06" },
  "tas":  { "kind":"pseudo", "g":["t","a","s"], "p":["t","æ","s"], "checked":"human" /*★*/ } }

// content/lessons/L1.02.json
{ "id":"L1.02", "level":1, "order":2, "title":"s a t", "type":"lesson",
  "newGpc":["s","a","t"], "review":[], "heart":["a","I"], "l1_tags":["short_vowels"] /*★*/,
  "sittings":[{"id":"A","newGpc":["s"],"steps":["hear","meet","spell","mini"],
               "mini":{"gpc":["s"],"pass":5,"of":5}}],
  "blend":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"]},
  "spell":{"words":["at","sat"],"sentence":null},
  "read":{"A":{"title":null,"sentences":[{"id":"s1","text":"Sat.","words":["sat"],"audio":"s.1a2b3c",
               "align":[[0,420]] /*★ word timings ms*/}]},
          "B":{"sameAsA":true},
          "questions":[{"type":"literal","q":"…","a":["sat"],"audio":"q.…"}],
          "audit":{"gpcs":["s","a","t"],"heart":[],"story":[]} /*★*/ },
  "listen":{"title":"…","sentences":[…],"tier2":[{"word":"nervous","def":"…","examples":["…","…"],
            "yourTurn":"…","audio":{…}}],"discuss":["…","…"]},
  "check":{"real":[…],"pseudoSets":[[…],[…],[…]] /*★ ≥3 fresh sets*/,"dictation":["at"],
           "pass":0.9,"reteach":{"step":"C","text":"Redo Sitting C blending drill…"},
           "errorClasses":{"tuh":"…","letter_name":"…"} /*★*/ },
  "notes":"…tutor notes (teacher mode only)…" }

// L5–7: "type":"session", steps: retrieval[], wordwork{morphemes[]}, prime{facts[],questions[]},
//   text{A:{screens:[[phrases…]]},B:…, anchors:[{after:screen,q,type,options,a}]}★, roles{…}, write{prompt,checklist[],model,keyTerms[]}★

// content/mastery/L1.json
{ "level":1, "components":[{"id":"letter-sounds","items":[…],"gate":0.9},{"id":"real-words",…},
   {"id":"pseudo","sets":[…]},{"id":"heart",…},{"id":"dictation",…},{"id":"bdpq",…}],
  "scoring":"separate", "reteachMap":{"letter-sounds":"L1.13"} }

// content/placement.json ★
{ "forms":["A","B","C"], "stage0":[…], "stage1":[…], "stage2":{"A":[…26],"B":[…5],"C":[…7]},
  "stage3":[{"tier":"CVC","real":[…8],"pseudo":[…8]},…], "stage4":{"passage":"…","words":…} }

// content/ui.json ★ — ~200 English lines; locale packs ui.<lang>.json with text + audio ids
{ "stop_here": {"text":"You can stop here.","icon":"pause","audio":"u.…"} }
```

Per-lesson JSON stays under 50 KB (build check).

### 6.3 Build-time gates (`npm run content` fails on any)

1. **Decodability**: for every L1–L4 lesson, every `decodable` word in `read.A`, `read.B`, `blend` and `check` is covered by the cumulative GPC set at that lesson. Heart words follow `heart.json`. Story words: at most 2 per text, flagged. From L5, every word is in the lexicon with a `kind`.
2. **Pseudoword real-word filter**: `gen_pseudo.py` builds candidates only from GPCs taught so far (CVC, then CCVC…). Each candidate is rejected if it is in CMUdict, in the lexicon, on `blocklist.txt` (slurs, rude words, brand names), or a homophone of a real word by IPA (e.g. "nite"). Then a human-review flag: placement-test.md shows three real-word defects slipped past rounds of review ("gan", "nob", "rob"), so the human review is required, not optional.
3. **Audio coverage**: §4.3 Q1, plus every `phoneme` in `gpc.json` has a `method:human` clip.
4. **Paths**: graph walk from L1.01: every lesson reachable, every reteach target exists, every Check has ≥10 items, and pseudo sets ≥3 per check.
5. **Two registers**: every L1–L4 lesson has `read.B` or `sameAsA`, and B passes the child-coded lint.
6. **No-cueing strings**: lint over the prompt strings.
7. **Size**: lesson JSON ≤ 50 KB, base audio ≤ 20 MB.
8. **Parser snapshots**: golden JSON for L1.02, L3.05, L4.03, L5.01.

### 6.4 Offline data model

IndexedDB, keeping the Urdu stores (`db.js`): `settings`, `profiles`, `attempts`, `cards`, `sessions`, `progress`, `assessments`. Every record has `id`, `profileId`, `updatedAt`. Added:

```jsonc
speech:   { id, profileId, lesson, target, heard, state:"clear_yes|unsure|machine_no", conf, ms, ts }   // no audio
mastery:  { id:"pid:L1.05", profileId, lesson, state:"mastered|secure|provisional|parked",
            components:{ real:{score,judge}, pseudo:{score,judge}, … }, evidence:[…], at }
packs:    { id:"L3-4", version, sha, status:"absent|downloading|ready", bytes }
helper:   { profileId, qualifiedAt, name? }
```

`profiles` gains `track: "A"|"B"`, `skin`, `homeLang`, `l1Family`, `comfort{}`, `placement{level,lesson,provisional,at,form}`, `daysPractised` (monotonic) and `lastSittingAt`.

### 6.5 Profiles on a shared phone

The Urdu profile list is reused unchanged (research-05 §6). Switching to a Track B profile needs no gate. Deleting, exporting, or switching a child into the grown-up area needs the gate. Cards, attempts, speech and mastery are all keyed by `profileId`. A helper's qualification is stored per helper and linked to the child profiles they help.

### 6.6 Backup, share, optional sync

- `backup.js` is kept: whitelisted stores, field checks, a 64 MB cap, and a merge by `id` + `updatedAt`, so two phones combine cleanly. Changes: `BACKUP_FORMAT`, the id regex (drop the Arabic range), and the new stores. Shared through the Android share sheet. Behind the gate.
- **Pack sharing** (new, v1.1): a grown-up can export a downloaded pack as a file and share it to another phone (Bluetooth/Files), which verifies the hash on import. This is how a whole school gets L3–L7 from one download.
- **Optional sync**: not in v1. A later design is one Supabase table with RLS and last-write-wins, metrics only, behind its own privacy page. Turning it on changes the Data Safety answer, so it would ship as a separate flag (research-05 §6).

### 6.7 Platforms and device targets

- Android AAB first, plus a PWA on GitHub Pages from the same codebase. iOS later (Mac, $99/yr, Swift speech plugin, AAC packs, Kids Category review; 1–2 weeks, not in the 8 weeks).
- minSdk 24 if the native speech plugin ships (sherpa-onnx's own minSdk is checked in the spike), otherwise 23. targetSdk 36. ABIs `arm64-v8a` and `armeabi-v7a` via AAB splits, because many budget Pakistani phones still run 32-bit userspace (research-05 §5).
- 16 KB page alignment for the onnxruntime / sherpa-onnx `.so` files. Confirm the chosen build provides them.
- Device target: 2–3 GB RAM, 16–32 GB storage, Android 10–13. Android 8–9 is "works if it works". Test phones: Kamal's family phone plus one 2 GB Android 10 phone (Tecno/Infinix/Redmi A class).

### 6.8 Performance budgets (research-05 §5, measured on the 2 GB phone)

| Metric | Budget | Measured by |
|---|---|---|
| Cold start to interactive | < 2 s | `adb shell am start -W` TotalTime; Lighthouse for PWA |
| Tap to lesson render | < 100 ms | `performance.now()` marks; Playwright with 6× CPU throttle |
| Tap to first sound | < 150 ms | the current lesson's bundle pre-decoded into `AudioContext` |
| JS shipped | < 150 KB gzip | lazy Lottie |
| Lesson JSON | < 50 KB | build check |
| Memory | < 150 MB without ASR, < 300 MB with | `dumpsys meminfo` |
| ASR model load / result | < 3 s / p95 < 3 s, p50 < 500 ms | spike, then `tools/perf.py` |
| IndexedDB open | < 200 ms | existing 8 s timeout stays as a safety net |
| Base install | ≤ 27 MB AAB (+ the measured native delta if the speech plugin is in base) | Play Console |

### 6.9 Test harness

1. Parser snapshots. 2. Content gates (§6.3). 3. **Oracle driver**: test builds expose `window.__oracle()`. A ~40-line Playwright driver completes L1 and L2 end to end, then makes a deliberate 80% run that must hit reteach, and a third miss that must park (research-05 §7). 4. DOM no-cueing test. 5. Gate reducer unit tests over every evidence combination. 6. Kill-and-resume test (20 random kills). 7. `ui_audit.py`: tap targets, overflow, contrast, at 360×640 and 390×800. 8. `check_audio.py`. 9. `speech_eval.py` over the gold set, per group. 10. `perf.py` with a CSV history. 11. Backup round trip, phone A → phone B. 12. Airplane-mode test: fresh install, then full L1 offline. 13. Pack download interrupted by airplane mode, resumed, and a deliberate bad hash rejected. 14. Network-silence test: proxy logs zero requests during lessons and speaking. 15. `store_judge.py` and `leak_check.sh` before every release.

---

## 7. Global

### 7.1 Localisation waves

Course text stays English. Localised: UI strings and their audio (~200 lines in English; budget ~300 per language per research-04 §4.2), helper and judge cards, L1 notes, parent summaries, privacy page, store listing.

| Wave | Languages | Ships |
|---|---|---|
| 0 (v1) | English UI + Urdu UI | week 8 |
| 1 | Hindi, Arabic, Spanish, Bengali | v1.1–v2 |
| 2 | Portuguese (BR), Indonesian, French, Swahili, Persian/Dari | v2+ |

The wave ranking is from memory in research-04 §4.1 and unverified. It must be confirmed with Play Console country data after launch (D8). Pashto and Punjabi learners are served by the Urdu UI first.

UI audio per language: a licensed voice for commercial use (Urdu: the existing ElevenLabs Sara clips if their licence covers this app, otherwise a new render; check D9). These are instruction clips, not English content, so they do not break the one-English-voice rule.

### 7.2 L1 interference notes model

Notes are tagged by feature, not rewritten per language (research-04 §4.3). Each lesson carries `l1_tags`: `short_vowels`, `th_voiced`, `th_unvoiced`, `v_w`, `p_b`, `b_v`, `clusters`, `s_clusters`, `final_clusters`, `silent_letters`, `vce`, `schwa`, `direction`, `opaque_spelling`. One note is authored per (tag × family): Perso-Arabic (Urdu, Arabic, Persian), Indic, Spanish/Portuguese, French, Bantu/Indonesian. A note is a single sentence plus an optional audio contrast pair ("vet / wet"), shown as a chip on Meet it and in the helper view. The family-level generalisations are from memory and need a native-speaker review before they ship. Urdu notes already exist in the course (`urdu-speakers.md`, per-lesson tips) and are converted first.

### 7.3 RTL

UI uses logical start/end layout. Urdu, Arabic and Persian mirror navigation, back/next and the progress direction. **English content never mirrors**: words, word highlight, tracing and the blend slide always run left to right. Mixed-direction labels are tested in week 7 (Urdu UI with English words inside).

### 7.4 Icon- and voice-first UI

Assume the user cannot read their own UI language. Every control has an icon and a spoken label. Every instruction auto-plays once (Track A) or plays on tap (Track B). "Hear it again" is on every screen (Urdu `path.js` pattern). No screen is explained only in text. The language picker speaks each name. Usability testing includes at least one adult who cannot read Urdu (§12).

### 7.5 Compliance checklist

| Area | What we do | Evidence status |
|---|---|---|
| Play Families | Mixed audience declared. No ads, no ad/analytics SDK, no advertising ID, no precise location, no age collected | Families policy read (research-04 §5) |
| Teacher Approved | Apply after launch and the closed test | snippet only |
| COPPA (amended; compliance date 22 April 2026) | No personal information collected. No voiceprints: audio is processed on device and discarded. No third-party disclosure. A written retention policy anyway ("we keep nothing; your phone keeps your progress until you delete it") | JD Supra summary read; FTC statement snippet |
| GDPR-K | No personal data processed, so no consent flow. Plain privacy page per UI language | Art. 8 ages from memory, unverified |
| UK Children's Code | High privacy by default, no nudges, no profiling beyond on-device learning state. Write a short DPIA | ICO code read |
| Parental gate | Before profile delete/export, backup/restore, links out, mic setup for Track A, pack download on mobile data, research-recording mode | Urdu checklist |
| Microphone | RECORD_AUDIO requested only at first use. The app is fully usable without it | Families permission rules |
| Content rating | IARC Education, no UGC, no purchases | Urdu checklist |
| Native libs | 16 KB page alignment if the speech plugin ships | Urdu checklist §2 |
| Voice disclosure | "Voice generated with Kokoro-82M; sounds recorded by [speaker]" in About and the listing | — |
| Closed test | ≥12 testers for 14 days before production on a new personal account | Urdu checklist §5 |
| Donation links | None in v1 (D10) | — |

### 7.6 Store listing plan

- **Name** (D17): something plain and age-neutral, e.g. "Read English: Learn to Read". No "kids", "ABC" or "baby" in the title or icon, because a 14-year-old and a 35-year-old must be willing to have it on their phone.
- **Short description** (≤80 chars): "Learn to read English from the first sound. Free, offline, any age."
- **Hook order**: free and no ads → works offline → for children and adults → checks you can really read (made-up "alien words") → never resets your progress. Nobody in the bar leads with offline, adults, or a mastery check (research-01 §3.5).
- **Claims we may make**: course built on systematic synthetic phonics (DESIGN.md §1 evidence). No account. No data collected. Size.
- **Claims we may not make**: "proven", "guaranteed level", "cures dyslexia", any efficacy number before the pilot. No "RCT" borrowed from Teach Your Monster (research-01 found none).
- **Screenshots**: 2 Track A, 2 Track B, 1 placement, 1 grown-up progress, 1 offline/size. Per UI language, generated with `make_store.py`, judged with `store_judge.py`.
- **Data Safety**: "No data collected, no data shared". Re-checked against the current form before submission.

---

## 8. Build plan: 8 weeks

Who does what: **Kamal** (decisions, human listening, kids' gold set, pilot recruiting, Play Console). **Speaker** (phoneme recordings). **Build agent** (a Claude Code session in the `read-english` repo: code, tools, content pipeline). **Critic agents** (fresh, blind, one per lens: teacher, parent+adult, engineer, audio). **Judge** (`listen_judge.py` / Gemini, triage only).

The three riskiest unknowns run in week 1: phoneme audio, listening, and the content parser (research-05 §8).

| Week | Deliverables | Verifiable exit check | Who |
|---|---|---|---|
| **1 — spikes** | (a) **Phoneme audio**: audition 2–3 speakers on 10 phonemes; the chosen speaker records all 44 × 3 takes plus 10 blending demos; Kokoro IPA versions of /m/ /n/ /l/ /r/ for comparison. (b) **Listening**: Kotlin sherpa-onnx plugin on Kamal's phone and one 2 GB phone; 3 candidate models; 30 target words + 10 pseudowords × 3 speakers; first 2 gold-set sessions per kid. (c) **Parser**: `--strict` over L1.02, L3.05, L4.03, L5.01. (d) **Playback**: Opus on two Android 10 phones; the 100-clip L1 Kokoro sample gets its first human listen (including 50 Track A sentences, for the 2/5 naturalness flag) | (a) both blind human listeners identify ≥42/44 phonemes; the speaker release is signed. (b) cold-load s, RSS MB, latency p95, and word accuracy per speaker recorded in `spikes/listening.md`; go/no-go for a "Listening (beta)" in v1. (c) 4/4 files parse to the schema. (d) plays on both phones; ≥95% of the 100 clips judged clear by Kamal | Kamal, speaker, build agent |
| **2 — repo + content** | Repo from copied files plus PROVENANCE; `data/gpc.json` / `heart.json` / `pron.json`; full parser over 8 levels; heading normalisation PRs to the course repo; decodability gate on the JSON; `gen_pseudo.py` with the filter; misaki OOV report | `npm run content` exits 0 for L1–L4 with 0 decodability violations; 100% of lessons have `check`, `read`, `listen`; `check_paths.py` passes; OOV list has an IPA override for each entry; first 300 generated pseudowords human-reviewed | build agent; Kamal reviews pseudowords |
| **3 — audio L1–L2 + shell boot** | `render_audio.py`, `check_audio.py`; L0–L2 rendered (~3,000 clips); human clips integrated; per-lesson Ogg bundles; the shell boots with English content: db, onboarding (role screens, demo "sat"), path, session with Leitner in sittings | Q1 passes 100%; the Q4 random 200 for L1–L2 ≥98%; the app starts offline in airplane mode and shows the L1 path; Leitner seeds from L1 GPCs; onboarding resumes after a kill at every step | build agent; Kamal listens (Q4) |
| **4 — drills, gate, reader** | E1–E12 (E6a stubbed); Check with lesson-specific bars, evidence-typed gate reducer, reteach/parked/skip; reader with word highlight; Listen & Talk; Track A/B skins; oracle driver | Oracle completes L1 and L2; a deliberate 80% run routes to reteach; 3 misses park; no-cueing DOM test passes; `ui_audit` 0 violations; **critic round 1** (teacher + parent lenses) on a recorded L1.02 run | build agent; critics |
| **5 — L3–L4, placement, helper** | L3–L4 content and audio (pack); placement flow with 3 forms; mastery components per level; helper intro, judge's card, 5-error qualification; screener; grown-up progress panels; Urdu UI strings and audio (wave 0) | Decodability still 0; Q1/Q4 pass for L3–L4; a scripted placement run with planted answers lands at the expected lesson for 5 test profiles (one per archetype); helper qualification rejects a helper who misses 1 of 5 | build agent; Kamal (Urdu strings review) |
| **6 — listening, packs, L5–L7 screens** | If week 1 said go: E6a with the three-state output, room check, permission flow, handover after 3 unsure, behind the "Listening (beta)" switch; gold-set evaluation run. Pack manager: manifest, resumable download, hash verify. L5–L7 session screens (E13–E20), long-text reader | On device: §5.4 metrics reported per class and per kid; 100 record cycles with no crash; 20 relaunch cycles with no mic failure; a pack download survives airplane-mode interruption; a bad hash is rejected. If week 1 said no-go: speech ships as E21 record-and-compare practice only, and nothing else slips | build agent; Kamal runs the kid sessions |
| **7 — polish, perf, PWA** | Perf pass on the 2 GB phone; a11y and comfort settings; RTL check; backup/restore round trip; PWA to GitHub Pages; store assets; signed AAB with ABI splits. **Critic round 2** (all four lenses) + gauntlet gates G1–G4 (§12) | Cold start < 2 s, lesson render < 100 ms on the target phone; backup A → B restores identical progress; AAB ≤ 27 MB + measured native delta; G1–G4 verdicts recorded | build agent; critics; Kamal |
| **8 — ship to testing + pilot** | PRIVACY.md (EN, UR), DPIA note, Data Safety, Families answers, listing (EN, UR); upload to Play internal testing; start the 12-tester / 14-day closed test; pilot starts (§12.2) | Installs from the internal link on 2 devices; L1 completed offline; no crash in the pre-launch report; 12 testers enrolled; pilot pre-tests done | Kamal; build agent |

### Roadmap after week 8

- **v1.1 (weeks 9–14)**: production release after the closed test. Teacher/tutor mode (`teacher.js`, `egra.js`). Pack sharing between phones. Wave 1 UI languages (Hindi, Arabic, Spanish, Bengali), each with a native reviewer. Pilot fixes. Real-world texts for Track B. Grade 2+ fluency reference norms fetched.
- **v2 (months 4–6)**: phoneme-CTC verifier with competitor sets. Machine witness for pseudowords only if per-phoneme validation passes, including Urdu-accented speech. ASR-based approximate WCPM. A fine-tuning experiment on consented, locally exported clips. FSRS if usage data supports it. iOS build. Wave 2 languages.
- **v3**: prosody proxies, a tutor review queue (machine flags, human decides), optional sync behind its own privacy page, on-device Kokoro for dynamic text (only if int8 runs on 2 GB phones).

---

## 9. Risks and honest unknowns

| Risk | Likelihood | Impact | Mitigation | When we know |
|---|---|---|---|---|
| Human phoneme clips are inconsistent, or the speaker's vowels don't match af_heart's American vowels | Medium | High: the phonics foundation | Audition with blind ID; the reference-vowel ritual each session; D15 fixes the accent | Week 1 |
| Kokoro word errors exceed 2% after re-rolls | Low–Medium | Medium | Re-roll ladder; human queue; re-test bf_emma or Chatterbox if it goes over 2% | Week 3 (L1–L2 Q4) |
| The af_heart child-sentence naturalness issue is real | Medium | Medium for Track A | Speed 0.9 or a carrier render; human listen | Week 1 |
| Machine listening fails on 4–7-year-olds and Urdu-accented speech | High | Low by design (witness only), Medium for the solo adult experience | Three-state output; helper and E6b paths; beta switch | Weeks 1 and 6 |
| Native plugin size, 16 KB pages, ABI or crash issues | Medium | Medium | Model as a downloaded pack; ABI splits; 100-cycle test | Week 1 spike |
| Parser yield is poor (inconsistent headings) | Medium | Medium: delays content | Normalise the markdown, not the parser; strict mode | Weeks 1–2 |
| Generated pseudowords that are real or rude words | Medium | High (trust) | CMUdict + lexicon + blocklist + homophone check + human review | Week 2 onward |
| Solo adults stall without a helper; `provisional` feels second-class | Medium | High for Track B retention | "Checked twice" wording; delayed re-check path; pilot interviews | Pilot weeks 2–6 |
| The course itself has had critic rounds but no field trial | High | High | Pilot (§12.2); gate and parked logs reviewed weekly | Pilot |
| Time per level discourages learners (84 kid sittings per level) | Medium | Medium | Honest parent summary; fast-track and skip; replacement at level ends | Pilot |
| Opus not playing on some WebViews | Low | Medium | Week-1 device test; AAC fallback packs | Week 1 |
| Pack download fails on poor connections | Medium | Medium | Resume, hash verify, Wi-Fi default, phone-to-phone sharing (v1.1) | Week 6 |
| Licence surprise (Kokoro training data, misaki, OpenMoji SA) | Low | High | LICENSES.md per asset; avoid SA art if unclear | Weeks 2 and 7 |
| Play Families review rejects the mic use or a mixed-audience declaration | Low–Medium | High (launch slip) | Mic optional, explained behind the gate; Urdu precedent | Week 8 submission |
| Wave ranking of languages is wrong | Medium | Low | Decide waves from Play Console data | 3 months after launch |
| Rule leakage: a hint or picture appears before a decode | Low | High (rule 1) | DOM test in CI | Every build |
| Nobody can tell whether it works, because no telemetry | Certain | Medium | Pilot with pre/post; opt-in aggregate export (D11) | Pilot end |

---

## 10. Decisions for Kamal

**W1** marks decisions that block week 1.

| # | Decision | Recommended default | Blocks |
|---|---|---|---|
| D1 | Stack: Urdu Capacitor engine or the Godot canvas | **Decided**: copy the Urdu shell (fixed) | — |
| D2 | Onboarding asks role, not age | **Decided**: role (fixed) | — |
| D3 | Ever ask age for a parent summary? | No; use performance triggers | — |
| D4 | Teens default to Track B | Yes, with a two-tap skin switch | — |
| D5 | Gate with no mic and no helper | Advance on E6b ≥90% as `provisional`; delayed re-check → "secure"; never "mastered" | W1 (gate reducer design) |
| D6 | Speech in v1 | Native sherpa-onnx witness for real words behind "Listening (beta)", off unless the gold set passes; never off-device | W1 (spike scope) |
| D7 | Leitner wrong-answer rule | Drop one box; two wrongs → box 1; sittings, not days | — |
| D8 | First UI languages | v1: English + Urdu. Wave 1: Hindi, Arabic, Spanish, Bengali, confirmed by Play data | — |
| D9 | Who writes and reviews L1 notes and UI strings per language; which voice speaks the UI audio | Authored per tag × family; native reviewer per language; Urdu UI audio uses Sara only if its licence covers this app | before week 5 |
| D10 | Donation or support link | None in v1 | — |
| D11 | Efficacy measurement without data collection | Pilot pre/post plus an opt-in, parent-initiated aggregate export file; no telemetry SDK | before week 8 |
| D12 | Content gaps to commission | See §11 | week 2 |
| D13 | Reminders | Opt-in, local, neutral, weekly cap, off for Track A | — |
| D14 | Teacher/tutor mode | v1.1 | — |
| **D15** (new) | Accent of the whole app | **General American**, to match `af_heart`; GPC IPA and human phonemes follow it | **W1** |
| **D16** (new) | Who records the 44 phonemes | One adult chosen by the week-1 blind audition (≥42/44 identified); release signed | **W1** |
| **D17** (new) | App name and icon | Age-neutral, e.g. "Read English: Learn to Read"; no "kids" or "ABC" | week 7 |
| **D18** (new) | Mascot: keep Marko (re-skinned) or a neutral one | Keep the Marko rig, re-skinned for a global audience, Track A only (research-05 §1) | week 4 |
| **D19** (new) | App code licence | Match the course repo's split (code under an open licence, content CC BY 4.0) | week 2 |
| **D20** (new) | Solo-adult progress wording | "You can recognise and spell these" / "Checked twice"; "mastered" only with a helper | week 4 |
| **D21** (new) | Pilot participants | Kamal's two kids + 1 teen + 3 adults (one market or shop worker, one grandparent, one Urdu-literate adult) | week 6 |
| **D22** (new) | Research-recording mode for the gold set | Debug and pilot builds only, parent-consented, local, manual export | **W1** |

---

## 11. Content work to commission

The course markdown does not supply these (research-04 D12, research-05 §2):

| # | Item | Size | Owner (suggested) | Needed by |
|---|---|---|---|---|
| C1 | **Level 0 print-concepts module** for learners with no L1 literacy: left to right, return sweep, word boundaries, what a letter is | ~3 short lessons | course author + critic round | week 5 |
| C2 | **≥3 fresh pseudoword sets per check** + mastery-check sets, from `gen_pseudo.py`, human-reviewed | ~1,000 items | build agent generates; Kamal + 1 reviewer | weeks 2–5 |
| C3 | **Placement item bank, forms B and C**, equivalent to form A | 2 × placement-test items | course author | week 5 |
| C4 | **Per-word grapheme–phoneme alignment** (`g`/`p`) for all lexicon words; `heartIdx` for heart words | 5,763 words (auto from CMUdict + aligner); ~50 heart words by hand | build agent; Kamal checks heart words | week 2 |
| C5 | **Pronunciation overrides** (`pron.json`): OOV words, heteronyms, letter names | ~100–300 entries (estimate) | build agent | week 2 |
| C6 | **Mouth-cue images** for 44 phonemes | 44 images | art (generated + reviewed) | week 4 |
| C7 | **Error-class map per Check**, from the tutor notes, and the reteach step per lesson | 108 lessons + 7 checks | build agent extracts; course author confirms | week 4 |
| C8 | **Track B real-world texts** as level-end unlockables (price list, bus ticket, SMS, pharmacy label, form) | ~2 per level for L1–L4 | course author | week 5 |
| C9 | **UI script** in English (~200 lines) and Urdu, with icons | 200 + 300 | build agent drafts; native reviewer | weeks 3–5 |
| C10 | **L1 notes per tag × family**, Urdu first (convert existing), then wave 1 | ~14 tags × 5 families | course author + native reviewers | Urdu week 5; rest v1.1 |
| C11 | **L5–L7 stop-and-check MCQs**, E18 partner scripts, E19 checklists + model answers + key terms, E20 authored search results | per session (~46 sessions) | course author | weeks 6–7 (L5); v1.1 (L6–L7) |
| C12 | **Pictures** for nouns and Tier-2 words, shown only after decode | ~300 (estimate) | generated art or OpenMoji (licence check) | week 4 |
| C13 | **Helper guide in-app** (from `guide-tutors-parents.md`), condensed to 5 screens + judge's-card audio | 5 screens | build agent | week 5 |
| C14 | **Heading normalisation** of the course markdown | dozens of small edits | build agent, PRs to the course repo | week 2 |
| C15 | **Grade 2+ fluency reference norms** (Hasbrouck-Tindal 2017) fetched and cited | 1 table | research agent | v1.1 |

---

## 12. How we will know it works

### 12.1 Success metrics without telemetry

All of these are computed on the phone and seen only by the user, or by Kamal in the pilot via a manual export:
- **Decoding**: lessons passed per level, with the share `mastered` / `secure` / `provisional`. Pseudoword accuracy per level check.
- **Comprehension**: literal and think question accuracy, shown separately.
- **Fluency**: WCPM (helper-marked) or pace, trend per level.
- **Persistence**: days practised, sittings per week, return after a gap of more than 7 days.
- **Friction**: parked gates, handovers after 3 `unsure`, Hear/Meet re-runs.
- **Opt-in aggregate export** (D11): a JSON of these counts, with no names and no audio, shared by the parent or learner through the share sheet if they choose.

### 12.2 The pilot (starts week 8, 6 weeks)

- **Participants** (D21): Kamal's 5- and 7-year-olds (Track A, Kamal as helper), one teen (Track B, solo), three adults: a shop or market worker (Track B, Urdu UI, solo), a grandparent (comfort settings on), and an Urdu-literate adult.
- **Pre and post**: the app's own placement (form A pre, form B post) plus the matching level mastery check, judged by a human who is not the learner's helper, with pseudowords included.
- **Weekly**: a 10-minute check-in (what was confusing, what felt babyish, what was too slow), plus the export file.
- **Pass bar for v1.1 production** (targets, not predictions):
  - every child advances ≥1 placement step;
  - ≥4 of 6 participants still practising in week 6;
  - zero reports of the app feeling childish from Track B adults;
  - zero rule-1 cueing incidents;
  - no learner told they failed;
  - every parked gate resolved by its repair path within 2 weeks.
- **Honesty**: the pilot is tiny and not a trial. Public copy may say "piloted with N learners" and nothing about effect sizes.

### 12.3 Gauntlet gates the build must pass

Method for each gate: fresh critic agents who did not build the app, plus named human judges. Comparison material is anonymised (logos, names and mascots blurred, our voice and theirs both kept). Each judge scores both sides on a written rubric, in both orders (A/B then B/A). We **win** only if we score higher in both orders on the rubric total, and no rubric row is worse by more than one point.

| Gate | We vs bar | Material | Rubric (each 1–5) | Judges | When |
|---|---|---|---|---|---|
| G1 Child first 10 minutes | Track A vs **Duolingo ABC** first 10 min (screen recording) | recorded runs, same tester's hands | clarity without reading; explicit sound teaching; no cueing; feedback kindness; pacing; would a 5-year-old want to return | teacher critic + parent critic + Kamal's kids' reactions (observed, not scored by the kids) | week 7 |
| G2 Interaction | our blend + segment + check sitting vs **Teach Your Monster** blending games | recorded runs | can a child pass by guessing (fewer = better); blend modelling; pause/resume; accent clarity; noise and music over narration | teacher critic + engineer critic | week 7 |
| G3 Breadth and free-ness | our grown-up progress + placement vs **Khan Academy Kids** parent view | screenshots + flows | can a parent see where the child is and why; separate metrics; skip/placement; offline coverage | parent critic | week 7 |
| G4 Adult dignity | Track B first session vs **Learning Upgrade** (store screenshots and video) | anonymised screens | nothing child-coded; real-life texts; speed control; privacy; would a 35-year-old use this on a bus | parent+adult critic + 2 pilot adults | week 7 |
| G5 Audio | 50 Kokoro clips (words, pseudowords, sentences) and the 44 human phonemes vs **ElevenLabs Sara** clips (urdu-reading-course) as the quality reference | blind clips, shuffled | clarity, naturalness, consistency of voice across clips, phoneme purity (no added vowel) | audio critic + Kamal + one native-speaker listener; Gemini only to triage | week 3, re-run week 7 |
| G6 Listening | our three-state witness vs **Google Read Along**'s helper behaviour on the same short decodable text read by both kids | live sessions | false credits on planted errors (fewer = better); child frustration; handover quality | engineer critic + Kamal | week 6 |
| G7 Rule audit | the running app vs **DESIGN.md §2** | oracle-driven run of L1–L4 + manual L5 | all 12 rules + 3 fixed decisions: pass/fail per row, no partial credit | teacher critic | week 7 and every release |

If a gate is lost, the critic's top two findings become the next week's first tasks and the gate re-runs. G7 has no "win": it must pass every row.

---

## Appendix: source index

**This folder** (`/home/oye/Documents/free_work/personal-agent-v2/vault/research/read-english-app/`): `RESUME.md`, `decisions.tsv`, `research-01-competitors.md`, `research-02-local-tts.md`, `research-03-listening.md`, `research-04-pedagogy-to-product.md`, `research-05-stack-and-reuse.md`, `bar/Khan_Academy_Kids.json`, `bar/Learn_to_Read_Duolingo_ABC.json`, `bar/Teach_Your_Monster_to_Read.json`, `bar/Reading_Eggs_Learn_to_Read.json`, `bar/Read_Along_Kids_Books.json` (a different product from Google Read Along).

**Course**: `/home/oye/Documents/free_work/english-reading-course/DESIGN.md`, `course/level-0/placement-test.md`, `screener.md`, `urdu-speakers.md`, `guide-tutors-parents.md`, `course/level-N/lessons/*.md` (108 lessons), `course/level-N/mastery-check.md`, `tools/decodable.py`, `LICENSE` (content CC BY 4.0).

**Urdu app**: `/home/oye/Documents/free_work/urdu-reading-course/mobile/src/*.js`, `mobile/tools/drive_all.py`, `ui_audit.py`, `scripts/listen_judge.py`, `voice_studio.py`, `store/PLAY_CONSOLE_CHECKLIST.md`, `research/09_tech_stack.md`, `10_learning_design.md`, `12_child_ux.md`.

**Other internal**: `/home/oye/Documents/free_work/personal-agent-v2/vault/research/english-canvas-tutor/decisions.tsv`, `v6-changes.md`. Research-02 test WAVs: `/tmp/claude-1000/-home-oye-Documents-free-work-personal-agent-v2/1be7ddf4-3868-4e0c-bd38-1aae7cd3186a/scratchpad/tts/wav/`.

**Competitors (research-01)**: https://support.google.com/readalong/answer/12281788 · https://teachustechnology.com/read-along-by-google-free-ai-reading-practice-app/ · http://readalong.google/impact/ · https://www.sattva.co.in/wp-content/uploads/2020/09/Sattva_Google_Read-Along-IA-Report.pdf · https://play.google.com/store/apps/details?id=com.google.android.apps.seekh · https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read · https://justuseapp.com/en/app/1440502568/duolingo-abc-learn-to-read/reviews · https://9to5mac.com/2020/03/26/duolingo-abc-learn-to-read-ios-free-app/ · https://www.plaudan.com/en/blog/duolingo-abc-review · https://screenwiseapp.com/guides/khan-academy-kids-app · https://khankids.zendesk.com/hc/en-us/articles/360029139531 · https://www.khanacademy.org/kids · https://help.teachyourmonster.org/en/articles/5736688 · https://www.usbornefoundation.org.uk/teachyourmonstertoread/ · https://www.roehampton.ac.uk/globalassets/documents/research/ref2021/ref3-casestudy-23-ur23-playful-pedagogies.pdf/ · https://www.commonsensemedia.org/app-reviews/teach-your-monster-to-read · https://justuseapp.com/en/app/828392046/teach-your-monster-to-read/reviews · https://www.trustpilot.com/review/readingeggs.com · https://www.proliteracy.org/news/4-apps-that-empower-adult-learners/ · https://web.learningupgrade.com/adult-education/esl/ · https://justuseapp.com/en/app/1185694693/learning-upgrade/reviews · https://www.cell-ed.com/how-it-works/ · https://spellingjoy.com/best-apps/app/ello · https://academicaitrends.com/blog/is-amira-learning-worth-it-2026/ · https://www.reddit.com/r/ESL_Teachers/comments/vz71qm/

**TTS (research-02)**: https://huggingface.co/hexgrad/Kokoro-82M · https://github.com/OHF-Voice/piper1-gpl · https://huggingface.co/rhasspy/piper-voices · https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html · https://github.com/k2-fsa/sherpa-onnx · https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/index.html · https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/ · https://awesomeagents.ai/tools/best-open-source-voice-tts-2026/ · https://github.com/KittenML/KittenTTS · https://github.com/supertone-inc/supertonic · https://github.com/resemble-ai/chatterbox · https://github.com/QwenLM/Qwen3-TTS · https://github.com/shivammehta25/Matcha-TTS

**Listening (research-03)**: https://huggingface.co/facebook/wav2vec2-lv-60-espeak-cv-ft · https://arxiv.org/html/2507.14451 · https://github.com/ggml-org/whisper.cpp · https://github.com/moonshine-ai/moonshine · https://github.com/lingjzhu/charsiu · https://github.com/mnaoizy/charsiu-js · https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment · https://api-docs.speechace.com/getting-started/how-speechace-scoring-works · https://developer.android.com/reference/android/speech/SpeechRecognizer · https://github.com/godotengine/godot/issues/110337 · https://dibels.amplify.com/docs/DIBELS8thEditionGoals_1.pdf · https://www.isca-archive.org/interspeech_2020/kelly20b_interspeech.html

**Pedagogy, compliance, accessibility (research-04)**: https://support.google.com/googleplay/android-developer/answer/9893335 · https://www.jdsupra.com/legalnews/the-amended-children-s-online-privacy-5418605/ · https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children · https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/ · https://developers.google.com/edu/guidelines · https://eric.ed.gov/?id=EJ1156546 · https://www.pnas.org/doi/10.1073/pnas.1205566109 · https://pubmed.ncbi.nlm.nih.gov/27580753/ · https://www.nber.org/papers/w22746 · https://www.npr.org/sections/ed/2018/04/26/602797769/ · https://link.springer.com/chapter/10.1007/978-3-031-54585-6_6 · https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2020/01/BjorkBjorkEducatinMythChapterPublishedFormSept2019.pdf · https://en.wikipedia.org/wiki/Google_Read_Along

**Store listings (bar/*.json)**: https://apps.apple.com/us/app/khan-academy-kids/id1378467217 · https://apps.apple.com/us/app/learn-to-read-duolingo-abc/id1440502568 · https://apps.apple.com/us/app/teach-your-monster-to-read/id828392046 · https://apps.apple.com/us/app/reading-eggs-learn-to-read/id726696040
