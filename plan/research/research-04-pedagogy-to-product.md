# Read English app — research 04: from 8-level course to an any-age app

Date: 2026-10-05. Scope: turn the course in `/home/oye/Documents/free_work/english-reading-course/` (DESIGN.md contract, Levels 0-7) into one app that a 5-year-old, a teenager and a 45-year-old all use. The course content is not redesigned here; this file maps it to screens, gates, review, languages and compliance.

Evidence labels: **[read]** I opened the source this session. **[snippet]** only a search-result abstract/snippet was seen. **[memory]** background knowledge I could not re-verify (the search tool failed on several queries, and some pages returned 403). Anything tagged [memory] or [snippet] should be confirmed before it goes in a public doc or a store declaration.

---

## 0. The shape of the answer

1. **One engine, two skins.** Content is typed JSON blocks parsed from the lesson markdown (the canvas-tutor plan already built a parser for L1.02 A-D). Track A (child) and Track B (teen/adult) differ only in skin, voice, carrier text and reward style. Same GPCs, same gates, same review deck. This is DESIGN.md rule 6 and `research/04` §5 rules 1-2 made literal.
2. **Route by role, never by age.** The first question is "who will read?", not "how old are you?". Placement then sets the level by skill (TaRL logic).
3. **The sitting is the app's unit, not the lesson.** The repo already splits L1.02 into four sittings (A ~10, B ~10, C ~15, D ~25-30 min) and the canvas critics forced "no sitting runs all 9 blocks". The app formalises this.
4. **A gate is only as honest as its judge.** Machines judge what machines can judge (taps, tiles, typed spelling, real-word speech once tested). Pseudowords and heart-word pronunciation need a parent/helper or a clearly labelled recognition substitute. Self-judging never opens a gate on its own.
5. **Recommended stack: extend the Urdu app engine**, not rebuild in Godot. `/home/oye/Documents/free_work/urdu-reading-course/mobile/src/` already has profiles with `track: child|adult|heritage` (`db.js`, `main.js:80`), `lessonsFor()` path of typed lessons (`path.js:39`), Leitner review (`memory.js`), unit quiz gate, parental gate, offline Capacitor build, and a finished Play checklist. The Godot canvas coach is parked material (`vault/research/english-canvas-tutor/decisions.tsv`, row "pivot"). See open decision D1.

---

## 1. One app, any age

### 1.1 What the big apps do (for contrast)

| App | Age handling | Lesson for us | Source |
|---|---|---|---|
| Duolingo | Splits the audience into separate products: main app with a 13+ account rule and restricted child accounts under 13, plus **Duolingo ABC** (ages 3-8) as a different app. | Separate apps double the content and compliance work; we get the same effect with a skin switch on one engine and no accounts. | [snippet] https://darlingmellow.co.uk/duolingo-kids-review-home-education/ ; https://duolingoguides.com/duolingo-kids/ (secondary blogs, not Duolingo's own pages) |
| Google Read Along (ex-Bolo) | Children's app only; speech recognition matches the child's reading to the text; Diya character; Android + web. | Confirms speech matching for read-aloud is mainstream; it is child-only, so adults have no equivalent. That is our gap. | [read] https://en.wikipedia.org/wiki/Google_Read_Along |
| Khan Academy Kids | Free, no ads, short 3-5 min lessons; no timers or competition. | Borrow short units and no-pressure tone. Claims about it come from the Urdu research file, which marks them unverified. | `/home/oye/Documents/free_work/urdu-reading-course/research/12_child_ux.md` (secondary) |
| Finch | Self-care pet app with a gentle, non-punishing loop. | Not retrieved this session. Treat as an inspiration only. | [memory] |

I could not retrieve first-party pages for Khan Kids, Finch or Teach Your Monster this session (search tool errors). Before copying any mechanic, fetch their own pages.

### 1.2 Onboarding flow (no birthday)

Principle: ask for the **role** and the **language**, never a date of birth. FTC's amended COPPA rule says any age collection must be neutral, must not default to a set age and must not encourage falsifying it [read] https://www.jdsupra.com/legalnews/the-amended-children-s-online-privacy-5418605/ . Google's Families policy likewise says an age screen must be neutral [read] https://support.google.com/googleplay/android-developer/answer/9893335 . The simplest compliant design is to not need an age at all, because nothing is collected and the app is the same for everyone underneath.

Screens (all voice-narrated, icon-first; text is secondary):

1. **Language.** Grid of native-script language names with a speaker icon on each (auto-plays the name). Sets UI + instruction audio language. Not tied to track.
2. **"Who is reading?"** Two large picture cards, narrated:
   - "I am reading" (person icon, no age words)
   - "My child is reading — I will help" (adult + small figure icon)
   This mirrors what the Urdu app already does (`main.js:80`: `a.who === 'me'` -> adult/heritage, else child).
3. **If "my child":** one-time **grown-up gate** (number spelled out in the UI language, as in the Urdu app) to set up the helper role, mic permission explanation and the "judge's card" (see §2.3). Then Track A skin.
4. **If "I am reading":** Track B skin. A teen lands here too. No mascot, no confetti, no pearls. A small, always-available "switch look" in Settings lets anyone move to the playful skin (a 9-year-old who picked "I am reading" gets playful art in two taps; a grown-up never sees it unless they ask).
5. **Name** (optional nickname, stays on device) and **avatar** (Track A only).
6. **Placement** (§3.1), framed as "sound games and reading, to find where to start. Some words are made up. There is no pass or fail." Taken from `course/level-0/placement-test.md` Stage 0 intake script.
7. **Reading-history questions** (screener), offered after placement, private, skippable (§6).
8. **First sitting starts immediately.** No account, no sign-up, no email, no notifications prompt until after the first completed sitting.

Edge cases:
- A young child who taps "I am reading" alone gets Track B text and a lower-key skin but the identical engine. No harm, nothing collected. The Families declaration still treats the app as child-directed-capable (§5), so ads/SDK rules apply regardless.
- Several learners per phone: profile list as in the Urdu app; per-profile streak-free progress; profile switch needs no gate for adult profiles, a gate to delete/export any profile.
- A shared phone where a parent and child both learn is the normal case; the Urdu app's profile model already handles it.

### 1.3 "Grown-up mode" spec (Track B skin)

Same engine, same lesson JSON. Differences:

| Element | Track A | Track B |
|---|---|---|
| Voice | warm character voice, short praise | plain adult voice, no pet names, no "great job!" every tap |
| Art | friendly characters, picture prompts | none or photographs/line icons of adult-life objects (bus ticket, phone, pharmacy label) |
| Carrier text | `Track A` readers in the lesson files | `Track B` readers (work, money, family, health, bus, market) |
| Reward | pearl/collection + short celebration | quiet "words you can read now" list; one-line summary at end of sitting |
| Trace/air-write | on by default (optional per DESIGN rule 11) | off by default, available |
| Typing | tile tray | system keyboard for spelling, with tile tray as fallback |
| Sitting length | 5-8 min | 10-15 min |
| Wording | "Let's play" | "Practice" ; never "baby", "easy", "kids" |
| Fast track | parent opt-in | visible "I already know this: take the check" on every lesson |

Why this matters: `research/04` §1 (lines 173-186) records that stigma is a primary barrier to adults even enrolling, and many hide low literacy rather than seek help; persistence is "the single hardest design problem"; the design implication is zero penalty for pausing and never showing an adult kid-labeled material [read]. External support: NPR 2018 https://www.npr.org/sections/ed/2018/04/26/602797769/casting-aside-shame-and-stigma-adults-tackle-struggles-with-literacy and a 2024 qualitative study of 12 people with low literacy reporting shame and stigmatisation https://link.springer.com/chapter/10.1007/978-3-031-54585-6_6 [snippet]. I found no direct experiment on how UI tone changes dropout; the link from "kid-coded UI" to dropout is an inference from stigma findings, not a measured effect. Say that in any public claim.

Cell-Ed and ProLiteracy outcome data: my searches returned nothing usable (tool errors). Do not cite either until fetched. The TaRL evidence for place-by-skill is solid: randomised evaluations of Pratham's Teaching at the Right Level, summarised at https://www.nber.org/papers/w22746 [snippet].

### 1.4 What age does change

Only things that are physically different: touch-target size (60-80 px for 3-5, 44-48 px for 9-12 per `urdu-reading-course/research/12_child_ux.md`, secondary sources), instruction audio on by default for Track A, timers hidden for Track A, and whether a helper is assumed. Everything else is a skin flag, not a branch.

---

## 2. Lesson template to screens

### 2.1 The sitting

Definition: a **sitting** is the unit of one open-the-app session; it contains 1-4 "block-units", ends on a deliberate "you can stop here" screen, and saves a checkpoint so closing the app mid-sitting resumes at the same screen.

Rules (carried from the repo and from what the canvas critics forced):
- No sitting runs all 9 blocks (canvas v2 critic; teacher). The Check is always its own short sitting or the last 2-3 min of a sitting that is otherwise under budget.
- A mini-check (the repo's L1.02 "Mini check" lines) is a tenth block type. Its pass rule comes from the lesson file (5/5, 7/8, 9/11), not a generic 90% (canvas v4 critic).
- One new GPC per sitting in Level 1 (L1.02 rule; `research/01` §5).
- Hear it / Meet it can be re-run at most twice; a third miss raises a helper flag (canvas v6).
- Adults may merge sittings if the mini-check is passed (L1.02 "Fast track").

Budgets: **Track A 5-8 min, Track B 10-15 min.** Khan Kids-style 3-5 min units are the floor for young children (secondary source in `12_child_ux.md`).

### 2.2 Breaking a lesson into sittings

Levels 1-4 lesson = 9 blocks, repo time 20-35 min.

| Sitting | Track A (5-8 min) | Track B (10-15 min) |
|---|---|---|
| 1 | Warm-up (2) + Hear (2) + Meet (3) | Warm-up + Hear + Meet + Blend (~12) |
| 2 | Blend (5) + mini-check (2) | Spell + Heart words + Read it (~13) |
| 3 | Spell (4) + Heart words (2) | Listen & Talk + Check (~8; may fold into next day's warm-up) |
| 4 | Read it (5-8) | — |
| 5 | Listen & Talk (5) | — |
| 6 | Check (2-3) | — |

Consequence: a 14-lesson level is about 84 kid sittings or 42 adult sittings. At 5 sittings a week that is roughly 8-9 weeks for an adult per level and longer for a child at one sitting a day. This is honest; state it in the parent summary so nobody thinks Level 1 is a week. Lessons with a one-sound-per-sitting structure (L1.02) already show this pattern: four sittings for three letters.

Levels 5-7 session template (30-45 min): retrieval warm-up, word work, fluency/close reading, **prime the topic** (3-5 min), knowledge text + discussion, write-to-read, check. Split into three sittings of ~12-15 min:
- S-A: retrieval + word work + fluency passage.
- S-B: prime + first half of text with stop-and-check anchors.
- S-C: second half + reciprocal teaching + write + check.

A 14-16 lesson level is then ~45 sittings.

### 2.3 Judge model

Three judges, always labelled on-screen with one plain sentence ("the app checks this", "ask your helper to listen", "you decide"):
- **Machine:** deterministic (tap/tile/typed spelling) or speech matching on real words after the speech engine has passed its own test (canvas v5: machines judge real words only after tests).
- **Helper:** parent/tutor with the **judge's card** (one line + one audio example per fail type: letter name for sound, vowel tacked on "tuh", gaps instead of blend, long aaa for short a, right answer after staring). Adapted from canvas v6.
- **Self:** allowed for practice and Listen & Talk, **never alone for a mastery gate**.

If no mic and no helper: gate items degrade to **recognition proxies** (see E6 below) and the result is stored as `provisional`, which schedules an extra spaced re-check and shows no "mastered" mark. Open decision D5.

### 2.4 Screen / exercise catalogue

| ID | Exercise type | Blocks it serves | Input | Judge | Time | Offline / no-mic / no-helper fallback |
|---|---|---|---|---|---|---|
| E1 | Sound game: listen, tap the picture that starts/ends with the sound; blend or segment by tapping dots | Hear it, Warm-up | tap | machine | 1-2 min | fully offline (pre-recorded audio). Speaking variant skips to tap-only. |
| E2 | Meet card: big letter, audio of sound, animated mouth cue, L1 tip chip | Meet it | tap play | none | 1 min | static mouth image if no animation. |
| E3 | Sound tap: hear a sound, pick the letter among 2-4; confusables interleaved (b/d/p/q) | Warm-up, Meet, Check | tap | machine | 1 min | offline. |
| E4 | Trace: stroke path with start dot and direction arrows, matcher checks start, checkpoints, end | Meet, Spell | finger | machine (formation only) | 1-2 min | optional per DESIGN rule 11; off by default in Track B; skip on small/slow devices. |
| E5 | Blend ladder: letters shown, tap each sound (audio plays), slide finger across to blend, then hear the word | Blend it | tap + slide | none (modelling) | 2 min | offline. |
| E6a | Say-it: show word, learner says it, app listens (on-device ASR) | Blend, Read, Check | speak | machine for real words only; helper for pseudowords and heart words | 2-3 min | **No mic:** replace with E6b. **No helper:** pseudowords go to E6b only. |
| E6b | Hear-and-pick (recognition proxy): audio plays a real word or pseudoword; pick its spelling among near foils (fape vs fap vs fepe) | Blend, Check | tap | machine | 1-2 min | works with no mic, no helper. Measures decoding by recognition, not production; label gate as `provisional`. |
| E7 | Spell: tiles from audio (kids) or typed (adults); sentence dictation last | Spell it, Check | tiles/keyboard | machine (exact match + hint on near-miss) | 2-4 min | offline. Error classes tagged for reteach (omitted silent e, etc.). |
| E8 | Heart-word map: word with sounds as dots; tap each sound; tap the heart part; rebuild from memory | Heart word | tap + tiles | machine | 2 min | offline. Never a flashcard drill (DESIGN rule 5). |
| E9 | Decodable reader: pages with word highlight; tap any word to hear it; then 3 questions (2 literal, 1 think) | Read it | tap | literal = machine; "think" = self with model answer shown after | 4-8 min | read-aloud audio on; no-mic fine. Track A/B text swapped by skin. Decodability audit stored per text. |
| E10 | Listen & Talk: narrated passage above decoding level, Tier-2 word card (friendly definition, two examples, "your turn" with sentence frames), two discussion prompts | Listen & Talk | listen, tap, optional speak | none (formative) | 4-5 min | no-helper: prompts answered by choosing among 3 sentences, then a model answer plays. Not a gate. |
| E11 | Check (mini and full): 5 real + 5 pseudo + dictated word, per the lesson file's own bar | Check, mini-check | tap/speak/type mix | machine for E3/E6b/E7; helper for pseudoword speech if on | 2-3 min | fresh pseudoword set on retry (need >=3 sets per check). |
| E12 | Retrieval card (Leitner): GPC, heart word, vocab or morpheme due now | Warm-up, L5+ retrieval | tap | machine | 2-3 min | offline. |
| E13 | Morphology builder: drag prefix/suffix/root tiles, sort by meaning, "does the new word make sense?" check after decoding | L5+ word work | drag | machine | 3-4 min | offline. |
| E14 | Phrase-cued echo reading: model plays, slash-chunked text highlights, learner reads back | L5+ fluency | speak | self/machine-ASR optional | 3-5 min | no mic: listen-and-follow mode (tap each phrase as you say it) counts as practice, not as measurement. |
| E15 | Timed read for WCPM: 60-second timer, learner taps the last word reached | L5+ fluency | speak + tap | machine (ASR) or helper marks errors | 2 min | Without ASR or helper the app can compute only **words reached in 60 s**; label it "pace", not WCPM, because errors are unseen. This is DESIGN rule 8 (two metrics). |
| E16 | Prime the topic: one picture or map description, 2-3 key facts, orienting question with a tap prediction | L5+ prime | tap | none | 3-5 min | text-only variant. |
| E17 | Long-text reader: text cut into 150-250 word screens, progress bar, resume position, font size, tap-for-gloss on Tier-2 words only, signal-word highlighter toggle, "stop and check" anchors (literal and inferential MCQ) | L5+ knowledge text | scroll/tap | machine (MCQ) | 10-15 min across a sitting | offline; audio read-along optional; resume from last screen after interruption. |
| E18 | Reciprocal teaching alone (scripted partner): see §2.5 | L6-7 | tap, type | machine on structure, self vs model answer on content | 5-8 min | offline; no LLM in the core loop (canvas decision). |
| E19 | Write-to-read: summary or response with sentence frames and a 4-point checklist; key-term presence check; model answer revealed after | all levels, L5+ extended | keyboard or dictation | self against checklist + machine key-term check (formative only) | 3-6 min | no helper: self-check with model answer. |
| E20 | Lateral reading sandbox (L6-7): authored mini search results; "who is behind this page?"; pick which source to open next | L6-7 | tap | machine (authored best/ok/poor options) | 4-6 min | offline; fully authored, no live web. |

### 2.5 Reciprocal teaching, alone (E18)

The course routine is Predictor, Questioner, Clarifier, Summarizer (L6.01). On a phone with no human, the scripted partner is an authored character-neutral voice ("Partner") that plays one role while the learner plays another, then swaps. Per section of text:
- **Predict:** learner picks or types a prediction; Partner shows its authored prediction; learner marks "closer / different". No right answer, so no failure.
- **Question:** learner picks the best of three candidate questions (one good, one yes/no, one too vague) and says why from a short list; for the stretch version learner writes their own and compares with a model plus a 3-item question checklist.
- **Clarify:** learner taps any word or phrase they did not follow; app offers authored clarification options for the glossed items and a re-read strategy for the rest.
- **Summarize:** reorder four sentences, then compose a one-sentence summary from selectable chunks (machine-checkable), then free-type for stretch (self against model).
Nothing here needs a live model. An LLM tutor is a later, separate decision; the canvas plan's ruling was "no LLM in the core loop".

### 2.6 Reading long text on a phone

Design choices, none of them measured here (I found no strong direct evidence; treat as defaults to test): screen-sized chunks over infinite scroll; sticky position; large text with line length of 30-45 characters; tap-for-gloss restricted to taught Tier-2 words so the app does not become a dictionary crutch; the "stop and check" anchors from the lesson files used as natural pause points; audio read-along as a toggle, off by default for gate-relevant fluency text. Check on real 5-inch phones with real learners before locking.

---

## 3. Placement, mastery, review

### 3.1 Placement flow on screen

Source: `course/level-0/placement-test.md` (stages 0-4; "stop each stage-type and place at the first point accuracy drops below 90%").

1. **Stage 0 intake (2 min):** four voice questions with big Yes/No/Skip cards (any English? ever taught to read in another language? first language English? learning languages always hard?). Answers are stored locally and tune what the app shows, e.g. a literate-in-Urdu adult gets the Urdu notes.
2. **Stage 1 oral phonological awareness (~5 min):** E1 tap items, no print. Fail early -> Level 1 start, lesson 1.01 (oral on-ramp).
3. **Stage 2 letter-sound grid:** Block A single letters 26 items (<24/26 -> place at first missed letter in the 1.2-1.12 order); Block B digraphs 5 (any miss -> Level 2); Block C vowel teams / r-controlled 7 (any miss -> Level 3/4). Each block runs only if the previous passed.
4. **Stage 3 decoding ladder:** tiers of 8 real + 8 pseudowords. Spoken items need ASR or helper; **without either, use E6b** and mark the placement `provisional`. Placement is shown as "start here (you can change this)".
5. **Stage 4 oral reading fluency** only after Stage 3 clears CVC+digraph: 1-minute timed passage, DIBELS-style hesitation rules. Needs mic or helper; otherwise skip and place by Stage 3.
6. **Result screen:** "Start at Level N, lesson K" with one button, plus "Start earlier" and "Start later (take that check first)". Never shows a score. Placement result is written to the profile with date and `provisional` flag.

Early exit for strong readers after Stage 3 or 4 is built into the test (5 min total).

### 3.2 State machine in words

States per profile: `placing` -> `in_lesson(L, k, sitting s)` -> `gate(L, k)` -> one of `next_lesson`, `reteach(L, k, step)`, `parked(L, k)` -> `level_check(L)` -> `replacement(L+1)` -> next level.

- **in_lesson:** the learner moves through sittings. Closing the app stores the screen. No timeout, no lost progress.
- **gate:** the check uses the lesson file's own bar (L1.02 mini checks 5/5, 5/5, 7/8, 9/11; later lessons 9/10). Every item carries an `error_class` tag from the lesson's Tutor notes (e.g. "silent e omitted").
- **pass:** write passed GPCs, heart words and Tier-2 word to the review deck (Leitner box 1), unlock next lesson.
- **fail:** go to `reteach` at the exact step the lesson's Check line names ("reteach step 3, the silent-e reach-back"), then re-check next sitting with a **fresh pseudoword set**. Hear/Meet reruns capped at two (canvas v6).
- **third miss on the same gate:** `parked`. Show: "This one is taking longer. That is common." Route to a review/repair mini-lesson from the previous lesson, raise a quiet helper flag in the grown-up area, and offer to continue with the next lesson's Hear/Meet only if the gate is not a hard prerequisite (never advance past a failed gate to the next one). The learner is never dead-ended and never told they failed.
- **skip ("I know this"):** takes the mastery check first (DESIGN rule 10). Pass = skip, fail = start at the lesson.
- **level_check:** the L1.14-style mastery-check lesson. Pass requires >=90% on real + pseudowords (e.g. L1 CVC; L2 CCVC/CVCC and 2-syllable closed words; L4 multisyllabic pseudowords). Fail routes back to the weak lesson cluster by error class, not to lesson 1.
- **replacement:** at each level end run the next level's placement slice (Stage 3 tier + fluency) so fast learners jump (`research/04` §5 rule 8). Also trigger an automatic **repair** insertion if a Leitner GPC box drops (e.g. two failures on an old grapheme in a week), so earlier gaps are fixed without restarting.
- **Mastery gate wording:** "real + pseudo >= 90%" is per DESIGN rule 4; pseudoword share must be visible in the result so a high real-word score from memorised words cannot hide a decoding gap (`placement-test.md`: pseudowords are "the single most load-bearing design choice").

Content ask: pseudoword generator or pool must exclude real words. The placement file records three real-word defects in one tier across three rounds ("gan", "nob", "rob"). Build the app's generator on a dictionary filter plus human review, not on a regex.

### 3.3 Spaced review (Leitner, as the Urdu app does)

Urdu research (`10_learning_design.md` §1) recommends Leitner for a simple offline start, FSRS later, and budgets about 5-8 seconds per review so a 10-minute session fits tens of reviews. Duolingo's own scheduler is half-life regression, not Leitner.

Proposal:
- **Decks:** GPCs (each grapheme-sound), heart words, Tier-2 vocabulary, from L5 morphemes (prefix/suffix/root). Real words used in checks are not Leitnered; pseudowords are regenerated fresh.
- **Boxes:** 5 boxes, scheduled in **sittings**, not calendar days, because adults are irregular and a calendar backlog punishes pausing (violates DESIGN rule 10). Defaults: box 1 next sitting, box 2 after 2, box 3 after 4, box 4 after 8, box 5 after 16.
- **Wrong answer:** drop one box; two wrongs in a row drop to box 1. (The Urdu app drops to box 1; this is gentler for adults. Open decision.)
- **Cap:** 6-10 cards per warm-up (2-3 min), interleaving confusables (b/d, a/e) because interleaving beats blocking for discrimination (Bjork & Bjork, cited in the Urdu research file, https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2020/01/BjorkBjorkEducatinMythChapterPublishedFormSept2019.pdf).
- **Return after a long gap:** no overdue pile. A "welcome back" warm-up of 6 cards, oldest-due first, then normal flow.
- Warm-up block 1 *is* the review. There is no separate "review chore" screen, except an optional Practice tab.
- Evolve to FSRS only after real usage data exists; embedding is optional (`rs-fsrs`).

---

## 4. Global: localisation and first-language support

### 4.1 Which languages first

I could not retrieve a verified ranking of English-learner populations or Play Store reach this session (search errors). The following is a reasoned shortlist, **[memory], to be confirmed** with Play Console country data and an Android-share source before committing. Criteria: size of English-as-second-language demand, Android share (Play reach), and low-literacy adult need.

| Wave | Languages | Why | Script / direction |
|---|---|---|---|
| 1 | Urdu (existing notes) , Hindi, Arabic, Spanish, Bengali | Large ESL populations; Android dominant in South Asia; Arabic/Spanish give two big non-South-Asian families | Urdu RTL, Arabic RTL, Hindi/Bengali Indic, Spanish Latin |
| 2 | Portuguese (BR), Indonesian, French (Africa + Europe), Swahili, Persian/Dari (and Pashto if the Pakistan audience needs it) | Brazil, Indonesia and francophone/anglophone Africa are Android-heavy; Persian/Dari RTL | Persian RTL |
| Later | Mandarin, Vietnamese, Turkish, Tagalog | Huge learner counts but Play distribution to mainland China is blocked; others add less new interference-pattern coverage | — |

Wave 1 should be chosen with Kamal's actual reachable audience (Pakistan first). Pashto and Punjabi are spoken L1s for Pakistani learners but are largely oral or use Urdu/Perso-Arabic script for literacy, so Urdu UI + Urdu notes covers most before a dedicated Pashto UI.

### 4.2 What is localised vs not

- **Course text stays English.** Only scaffolding is localised: UI strings (~300, estimated), narrated instructions, L1 tip chips, store listing, helper/judge cards, parent summaries, privacy policy.
- **Instructions are audio first.** Never text-only (§4.4). Cost: ~300 clips per language; start with synthetic or recorded voices that are licensed for commercial use (Urdu checklist flags voice licensing).
- **Tier-2 glosses in L1** (translation of the word, not of the definition) are a Wave-2 add-on for L5+ because many are cognates in Spanish/French/Portuguese and Latin-root words help there (and Urdu already has loanword notes in lesson files).

### 4.3 First-language interference notes, generalised

The course has an Urdu note system: `course/level-0/urdu-speakers.md` and per-lesson "Urdu-speaker tip" lines and "Urdu note" on vocabulary. Generalise by **feature tags, not per-language rewrite**: each lesson carries `l1_tags` such as `short_vowels`, `th_voiced`, `v_w`, `final_clusters`, `silent_letters`, `vce`, `schwa`. A single note per (tag x language family) is authored once and shown on any lesson with that tag. Starting families (documented contrastive-analysis generalisations, **[memory], need native-speaker review**):

| Family | Likely trouble | Tags |
|---|---|---|
| Perso-Arabic script (Urdu, Arabic, Persian) | vowels not written in everyday script so English written vowels feel unfamiliar; short vowel contrasts (i/e, a/u); /p/-/b/ in Arabic; consonant clusters broken with a vowel ("iskool"); right-to-left habits | `short_vowels`, `clusters`, `direction`, `p_b` |
| Indic (Hindi, Bengali, Punjabi) | v/w; "th" as aspirated dental; retroflex t/d; clusters; expecting one sound per letter (English is not) | `v_w`, `th`, `clusters`, `opaque_spelling` |
| Spanish/Portuguese | vowel letters as pure sounds (i says "ee"), b/v merging, s+consonant onset gets an "e", silent h, sh/ch/j | `short_vowels`, `b_v`, `s_clusters`, `silent_letters` |
| French | silent letters, h, stress, th, English vowel teams differ | `silent_letters`, `th` |
| Bantu / Indonesian | final consonant clusters, vowel length, th | `final_clusters`, `th` |
| East Asian | l/r, final consonants, no case/spacing habits | later wave |

Notes for learners with **no L1 literacy** are a separate module in Level 0: print concepts (left to right, return sweep, word boundaries, what a letter is). That is a content gap for the course; flag it as a Level 0 addition.

### 4.4 RTL and low-literacy UI

- Build the UI with logical start/end layout so Arabic/Urdu/Persian mirror correctly. Mirror navigation (back/next arrows, progress direction), not the English reading content or letter tracing. English words sit LTR inside RTL screens; test mixed-direction labels.
- Progress bars and word-by-word highlights in the English text always run left to right.
- **Low literacy in L1 as the default assumption:** every control has an icon and a spoken label; every instruction auto-plays once in the UI language (Track A) or on tap (Track B); a persistent "hear it again" button on every screen (Urdu app has `Repeat instruction`, `path.js:127`); no screen explained only in text; test with learners who cannot read their own UI language, not just with those who choose Hindi from a list.

---

## 5. Compliance checklist (global kids app)

What the Urdu app already did (`/home/oye/Documents/free_work/urdu-reading-course/store/PLAY_CONSOLE_CHECKLIST.md`): Data safety "no data collected, no data shared", on-device storage with a user-initiated export through the Android share sheet, privacy policy URL, no ads, no login, IARC Education -> Everyone, target audience 5-8 / 9-12 / 13-15 / 16-17 / 18+, spelled-out-number gate in front of links out, no payment SDK, voice-provider licence check, closed testing with >=12 testers for 14 days for a new personal account, Teacher Approved applied for after launch.

Checklist for Read English (reuse and extend):

| Area | Requirement | Plan | Source |
|---|---|---|---|
| Google Play Families | Declare target age groups accurately; select multiple groups only if the app is appropriate for all of them; child-directed apps cannot send AAID, IMEI, MAC or precise location; ads (if any) only via Families-certified SDKs; neutral age screen for mixed audiences when restricting content | **No ads, no ad SDK, no analytics SDK, no advertising ID permission.** Declare mixed audience as the Urdu app did. Do not collect age. | [read] https://support.google.com/googleplay/android-developer/answer/9893335 |
| Teacher Approved | Basic requirements include that apps and any ads must not collect PII (beyond limited exceptions), designed for K-12 | Apply after launch and after 14-day closed test, like the Urdu app | [snippet] https://developers.google.com/edu/guidelines ; https://play.google.com/console/about/programs/teacherapproved/ |
| COPPA (amended rule) | Compliance date 22 April 2026. Personal information now includes biometric identifiers such as voiceprints; separate parental consent for disclosures to third parties; written retention policy; security program; any age collection must be neutral | Do not collect voiceprints: run speech recognition **on device only**, discard audio after scoring unless the learner/parent explicitly saves a local recording. No third-party disclosure. No data collected -> consent mechanisms not triggered, but write the policy anyway | [read] https://www.jdsupra.com/legalnews/the-amended-children-s-online-privacy-5418605/ ; FTC Feb 2026 age-verification policy statement https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children [snippet] |
| GDPR-K | Special rules for children's consent (member states set the digital-consent age between 13 and 16) | Process no personal data -> no consent flow needed. Still publish a plain-language privacy page in each UI language | [memory] confirm Art. 8 values |
| UK Children's Code (15 standards) | Best interests, DPIA, high privacy by default, data minimisation, no sharing, geolocation off, no nudging toward weakening privacy, limited profiling | Defaults already satisfy: nothing collected. Write a short DPIA anyway; no nudge copy ("don't lose your streak") | [read] https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/ |
| No account by default | Profiles are local nicknames only | Same as Urdu app | Urdu checklist |
| Data stays on device | IndexedDB / local DB; export and reset behind the grown-up gate | Same as Urdu app | Urdu checklist |
| Parental gate | In front of: settings that change profiles, export/backup, delete, any link out, mic permission set-up for kids | Number-as-words gate in each UI language (needs translating number words per language; verify it is hard for a pre-reader but passable for a literate adult) | Urdu checklist; `12_child_ux.md` |
| Microphone | RECORD_AUDIO only at the moment the learner or helper chooses a speaking exercise; app fully usable without | Explain on a pre-permission screen; never block progress when denied | Families policy on permissions [read] |
| Content rating | IARC Education, no UGC, no purchases | Same as Urdu app | Urdu checklist |
| Links out and support/donation | Any out-link needs the gate; a donation or bank-transfer text for a global app is a separate decision | Open decision D10 | Urdu checklist |
| Voice licensing | Commercial distribution rights for shipped audio; disclose AI voices | Verify per provider, per language | Urdu checklist §6 |
| Targeting SDK / 16 KB pages | Urdu build: targetSdk 36, no native libs so the 16 KB rule did not apply | If whisper.cpp or any native ASR is embedded, the 16 KB page-size rule applies; build for it | Urdu checklist §2 |
| Store listing | Localised listings, screenshots per language, no unverifiable claims ("dyslexia cure", "guaranteed level") | Keep claims to what the evidence tables support | — |

Note on accounts later: any future sync/teacher dashboard changes the data practices and reopens COPPA, GDPR-K and Families review. Keep it off the first release.

---

## 6. Accessibility and reading difficulty

### 6.1 Reading-comfort settings (evidence is mixed; say so)

Offer as plain-named toggles in a "Reading comfort" screen, not under a "dyslexia" label. Default to clear sans-serif with single-storey a and g for beginners (a literacy-designed face such as Andika is a candidate [memory]; check licence).

| Setting | Evidence | Verdict |
|---|---|---|
| Specialised dyslexia font (OpenDyslexic) | Wery & Diliberto 2017 found no improvement in reading rate or accuracy versus Arial or Times, in children with dyslexia | **Do not default it.** If included, as a user choice only. [read] https://eric.ed.gov/?id=EJ1156546 |
| Extra letter spacing | Zorzi et al. 2012 (PNAS) reported better reading by dyslexic children with extra-large spacing; a published commentary disputes its statistical and practical significance | Offer as slider; default a little wider than normal; do not claim it treats dyslexia. [snippet] https://www.pnas.org/doi/10.1073/pnas.1205566109 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC3497831/ |
| Coloured overlays / tinted backgrounds | A systematic review exists examining quality of evidence; consensus is weak and results mixed | Offer a few background tints and a high-contrast mode as a personal preference; make no efficacy claim. [snippet] https://pubmed.ncbi.nlm.nih.gov/27580753/ |
| Large text, line spacing, left-aligned text, reduce motion, slower speech rate | Standard accessibility practice | On by request; easy to find. |
| Personal A/B check | — | "Which looks easier?" two-screen comparison; the learner's choice is the setting. |

### 6.2 The screener

Level 0 has a non-diagnostic screener (`course/level-0/screener.md`): adult part A (10 yes/no), child part B (10 observations by a parent or tutor), 0-2 / 3-5 / 6+ yes bands, and "never labels, never gates access". In the app:
- Offered after the first placement, never before, private, skippable, results kept on device.
- Outcome copy is the repo's two outcomes only: "no flags" or "some flags: the course still works for you, here is what you can do alongside it". No word "dyslexia" in the learner-facing result; it appears in the grown-up notes as "a specialist can assess this".
- Never changes the lesson the learner starts on (placement alone does that).

### 6.3 When to tell a parent (or adult) to seek help

Signals the app can see without any age field:
- Same gate missed three times after reteach (repeat ceiling).
- Placement stops in Stage 1 (oral phonological awareness) after a second attempt on another day.
- Screener flags 3+ (Part B for children).
- Persistently low accuracy on letter-sound recall despite many Leitner reviews.

Message shape: plain, short, no blame: "Some sounds are taking longer. That is common. A teacher or reading specialist can check how your child hears and sees letters, and also hearing and eyesight. The lessons still help; keep going at this pace." Repeat the screener caveat: it is a flag, not a diagnosis. For adult learners: the same, framed as access to accommodations (screener file text). Avoid any numeric age thresholds in the app because it does not know age.

---

## 7. Motivation: what to borrow, what to refuse

### 7.1 What already works (Urdu app)

- **"Days practised. It never resets."** The kind-progress rule from `/home/oye/Documents/free_work/urdu-reading-course/brag-output/brag-plan.md` and the video line. A count of days that only ever goes up.
- **Pearl necklace path** (`path.js:66`): done lessons become pearls on a thread, current one glows, later ones are empty outlines; unlock moment on completing a unit.
- Child-track-only sounds and mascot (`path.js:126`, `drills.js:10`), adult track gets less animation.
- Soft errors: hints not red Xs, "try again", no failure sounds in the child track (`12_child_ux.md`, secondary).

### 7.2 Borrow

| From | Mechanic | Why it fits |
|---|---|---|
| Urdu app | never-resetting practice count; pearls | no loss framing; DESIGN rule 10 "no streak-shaming, pause-safe" |
| Teach Your Monster | progression through a world of small challenges and collectable rewards | [memory, verify first-party] suits Track A |
| Khan Kids | short lessons, no timers or competition | [secondary] |
| Course design | "words you can read now" counter for Track B; real-world texts (bus ticket, SMS, pharmacy label) as unlockables at level ends | competence shown as real-life capability, not game points. Content ask for course authors. |

### 7.3 Avoid

- **Streaks with loss framing, streak freezes, hearts/lives, leagues, leaderboards, guilt-copy notifications.** Teardowns describe the loss-aversion mechanic and its monetisation directly (https://zicozhou10.github.io/behavioral-design-hub/teardowns/duolingo/ [snippet]). Honest caveat: I found commentary, not a peer-reviewed trial of streak anxiety; the rationale for avoiding it here is DESIGN rule 10 and the adult-persistence evidence in `research/04`, not a proven harm effect.
- Praise for being "smart"; praise effort (`12_child_ux.md`, Futurice guideline cited there).
- Reminders: opt-in only, local notifications, neutral copy ("A 10 minute sitting is ready when you are"), a single weekly maximum by default, off for Track A unless the parent chooses.
- Celebrating pseudoword mastery with the same fanfare as real words; reward the gate pass, not each tap.

---

## 8. Open decisions for Kamal (with recommended defaults)

| # | Decision | Default recommendation |
|---|---|---|
| D1 | Stack: extend the Urdu Capacitor/JS app engine vs the Godot canvas coach | Extend the Urdu engine; keep Godot canvas as parked material. Revisit only if an AI-tutor product is wanted. |
| D2 | Onboarding question: role ("I am reading / my child is reading") rather than age | Role, no birthday, no age field anywhere. |
| D3 | Do we ever ask the child's age for a parent-only summary? | No. Use performance triggers. |
| D4 | Track B for teens by default | Yes, with a two-tap switch to the playful skin. |
| D5 | Gate behaviour with no mic and no helper | Allow advance on recognition proxy (E6b) >= 90%, mark `provisional`, schedule extra re-check, show no "mastered" mark. Alternative: block. |
| D6 | Speech engine: on-device whisper.cpp or similar vs none in v1 | Ship v1 with E6b + helper judging; add on-device ASR for real words in a later release after the 5-planted-error qualification used in the canvas plan; never send audio off-device. |
| D7 | Leitner wrong-answer rule | Drop one box, two wrongs -> box 1. Sitting-count scheduling, not calendar days. |
| D8 | First 10 UI languages | Wave 1: Urdu, Hindi, Arabic, Spanish, Bengali; Wave 2: Portuguese, Indonesian, French, Swahili, Persian/Dari. Confirm against Play Console data. |
| D9 | Who writes and reviews L1 notes and the ~300 UI strings/audio per language | Authored once per (tag x family); native reviewer per language, paid or volunteer. |
| D10 | Support/donation links in a Families app | Leave out in v1; if kept, behind the gate and not for Track A. |
| D11 | Efficacy measurement without collecting data | Opt-in, parent-initiated, aggregate export file only; no telemetry SDK. Without it we cannot prove outcomes. |
| D12 | Content gaps to commission | (a) Level 0 print-concepts module for L1-illiterate learners; (b) >=3 fresh pseudoword sets per check; (c) a pseudoword real-word filter; (d) Track B real-world texts; (e) reading-comfort defaults tested on 5 real users. |
| D13 | Reminder policy | Opt-in, local, neutral, off by default for Track A, weekly cap. |
| D14 | Availability of a teacher/tutor mode | Reuse Urdu `teacher.js` (profile management, export) in a later release; gated. |

---

## Source index

Internal: `/home/oye/Documents/free_work/english-reading-course/DESIGN.md`; `course/level-0/placement-test.md`, `screener.md`; `course/level-1/lessons/L1.02-s-a-t.md`; `course/level-3/lessons/L3.01-a_e.md`; `course/level-6/lessons/L6.01-how-your-body-is-built.md`; `research/04-adult-adolescent-esl.md`; `research/07-program-scopes-assessment.md`; `/home/oye/Documents/free_work/personal-agent-v2/vault/research/english-canvas-tutor/decisions.tsv` and `v6-changes.md`; `/home/oye/Documents/free_work/urdu-reading-course/research/10_learning_design.md`, `11_letter_lesson_flow.md`, `12_child_ux.md`, `store/PLAY_CONSOLE_CHECKLIST.md`, `mobile/src/path.js`, `main.js`, `db.js`.

External read in full or in useful part: Google Play Families policy; JD Supra COPPA summary; UK ICO Children's Code; Wikipedia Read Along. Search snippets only: TaRL/NBER, PNAS Zorzi, pubmed overlays review, ERIC Wery & Diliberto, NPR stigma, Springer shame chapter, Teacher Approved pages, FTC policy statement, Duolingo teardown and kids reviews. Not retrieved: Cell-Ed, ProLiteracy, Khan Kids, Finch, Teach Your Monster, Android share and ESL population ranking.
