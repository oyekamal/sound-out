# Read English: the app plan, v3

Date: 2026-10-05. Owner: Kamal. Board task #118.
v3 rebuilds v2 after critic round 2 (teacher, parent+adult, engineer, audio, auditor) and the lead's two reversals and seven fix sets. `v3-changes.md` maps every finding to its change. Evidence: research-01…05, `english-reading-course` (DESIGN.md, 108 lesson files, `course/level-0/placement-test.md`), `bar/*.json`, critics-round-1/2-*.md. Labels: "unverified" = the source said so; "estimate" = this plan made the number; "budget" = a target, not a measurement.

---

## 0. Summary, two decisions to confirm, and the bar

**Summary.** Read English is a free, offline Android app (plus a PWA) that takes anyone from the first sound to fluent reading. Version 1 ships Levels 0–5 of the 108-lesson course. Levels 6–7 (critical reading) arrive in v1.1. The app is a copy of the Urdu Qaida shell (Capacitor 7, Vite, IndexedDB, Leitner, pearl path, feel.js, single `Audio()` player) with no native code.

- **Night one is a lesson, not a test.** A child hears and taps her first letter sound within 90 seconds of first launch, inside a small game world. An adult reads his first real word ("sat") within 15 minutes, in private.
- **Blending.** The learner says each sound, then the word. The gate is checked by tapping. The learner reads a printed word, then picks which of four spoken words it says. All four options share the first sound and differ in the middle **and** the end. So no adult who reads English is needed.
- **Helpers.** A helper who listens can upgrade a lesson to "mastered". This is optional.
- **No accounts, ads or analytics, and no microphone in v1.**

### Decision D0a: voice (reverses Kamal's "local model for all voices" for Levels 0–2)

**Proposal.**
- **Levels 0–2 use one human teacher voice for everything**: 44 phonemes, blending demos, every word, pseudoword, sentence, Track A and B text, English UI prompts, and slow takes.
- **Levels 3–5 (and 6–7 in v1.1) use Kokoro-82M `af_heart`**, pre-rendered on the build machine.
- The handover happens once, at the start of Level 3, announced in the app: *"A new reader joins you. Your sound teacher is still here."*
- From Level 3 the human teacher's voice still speaks isolated sounds (Meet it, sound buttons), because no TTS gives a clean isolated sound. Words and sentences use the Kokoro reader. The two voices have two named roles and never alternate inside one word exercise.

**Evidence.**
- research-02 §5: neither Kokoro nor Piper produced isolated phonemes a judge could identify, and stops cannot be said in isolation. This is Gemini-judged and unverified by a human.
- Audio critic, round 2, measured Kokoro's isolated /s/: spectral centroid 513 Hz. That is low rumble, not a hiss, so no Kokoro reference exists for isolated sounds.
- Round 1 (audio B) and round 2 (audio B) both rejected the human-phoneme → Kokoro-word join, the core s-a-t → "sat" moment. Round 2 called the planned "same person?" gate statistically empty.

**Alternative: "Kokoro-only words with recorded phonemes"** (the v1/v2 design). It keeps Kamal's local-model rule but plays a human /s/ /æ/ /t/ then a Kokoro "sat" in every L1–L2 blend. Both audio critics voted B against it.

**Cost of D0a.**
- About 20–30 studio hours of a paid speaker (§4.5).
- L0–L2 text must be frozen before recording. Later edits need pickup sessions.

### Decision D0b: listening (reverses research-03's v1 stack and research-04's D6)

**Proposal.** v1 ships **no speech gate and does not request the microphone.**

**Why.**
- The engineer (round 2): sherpa-onnx keyword spotting and hotword biasing cannot return the three answers the design needs (yes, unsure, no). Real target-vs-competitor scoring is a 10–15-day CTC project.
- The teacher and the auditor (round 2): at research-03's 60% recall floor, a child who reads every word correctly passes a 10/11 gate only about 3% of the time.
- research-03 had recommended Whisper as a witness for real words in v1, and research-04 D6 had recommended on-device speech recognition later. Both are superseded for v1.

**Roadmap.**
- **v1.1**: record and replay, self-compare only, labelled practice.
- **v2**: a phoneme verifier. A CTC model runs via onnxruntime, with our own scoring of target vs competitor sequences: 10–15 days. It needs a kid gold set of ≥60 items per class, labelled by a native General American speaker (not Kamal), with Kamal as second rater. Urdu-accented vowel merges are flagged as practice, never as wrong.
- Only after v2 passes does any machine listening touch a gate.

**Alternative.** Keep the v2 verifier on the critical path. The engineer judged that an 8-week ship then likely fails or slips.

### The bar

Features: Duolingo ABC, Khan Academy Kids. Interaction and child experience: **Teach Your Monster** (§3.4 is built against it). Pedagogy: DESIGN.md. Audio reference: the ElevenLabs Sara clips. The brief adds Google Read Along and Learning Upgrade.

| We ship (v1 unless marked) | Duolingo ABC | Khan Kids | Google Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes | Yes (parent account per Common Sense) | Yes | No: iOS $8.99 | No: $4.99/mo–$59.99/yr |
| Offline | listing has "Offline Learning" | partial | yes, after download | not documented | no evidence |
| Adult track, same sequence | No (pre-K–2) | No (2–8) | No (5+) | No (listing: 3–6) | Yes, songs/video, 3.2/5 |
| Placement + skip | No ("No option to skip ahead") | not found | No | not found | not found |
| Gate on real and pseudowords | not found | not found | not found | not found; "children can progress by guessing" | not found |
| Gate cannot be passed by first-letter matching | — | — | — | — | — |
| Goes beyond early phonics | No; research-01: progression "stops at simple stories" | ~grade 2 | story practice | phases 2–5 | partial |
| Our depth | L0–L5 in v1 (to ~100 WCPM, morphology); L6–L7 critical reading on the v1.1 roadmap | | | | |
| First-language (Urdu) support for the English code | No | Spanish read-to-me | Urdu stories, no code teaching | No | a few onboarding languages |

"Not found" means absent from research-01 and the listings, not proven absent. Duolingo ABC lists "over 700 hands-on lessons"; Common Sense counted 127 units. Both are reported. Store data (US iOS, sizes in MiB): Khan 4.80 on 131,337 ratings, 201 MiB. Duolingo ABC 4.25 on 3,810, 212 MiB, last updated 2023-08-02. Teach Your Monster 4.47 on 29,802, 96 MiB. `bar/Read_Along_Kids_Books.json` is a different product. Our sizes are in §4.1, in MB, as download and installed size.

---

## 1. Who it is for, and the promise

**Promise:** "Ten minutes most days. Starts at the first sound. Offline, free, knows nothing about you, never makes you start over, and no one who reads English has to help."

**Honest time** (estimates from the sitting model in §3.2; the week-2 budget lint replaces them):

| | Lessons L1.02 → end of L4 | Sittings | At 1/day | At 5/week |
|---|---|---|---|---|
| Child, Track A, ~6 sittings/lesson | 61 | ~366 | ~12 months | ~17 months |
| Adult, Track B, ~3 sittings/lesson | 61 | ~183 | ~6 months | ~9 months |
| Adult fast track (course "Fast track": merge sittings after a ≥90% mini check), ~1.5–2/lesson | 61 | ~92–122 | 3–4 months | 4–6 months |

### 1.1 Five archetypes, night one

| | Ayesha, 5, Urdu home; mother doesn't read English | Leo, 7, native English | Bilal, 14, hides it | Rukhsana, 35, stall worker | Nana Karim, 60 |
|---|---|---|---|---|---|
| Role tap | "A child" (mother taps) | "A child" | "Me" | "Me" | "Me" |
| Night one | Track A world (§3.4): Pebble the mascot, /s/ heard and tapped by ~0:60, trace, write s from memory, sun rises in the village, sticker. 8 min. She shows her mother the s and says /s/ | Same night one. Later his father opens grown-up settings → placement → Stage 2 Block B misses th → **L2.03** | 15-min sitting, L1.02 A+B+C: says s, a, t, blends and reads **sat, at, as**, spells "sat". Sets his PIN at the end | Same as Bilal. Urdu instructions; large text offered | Same night one. Next night: placement from his PIN-protected settings → Block B misses sh → **L2.01** |
| Exit check | first sound tapped ≤90 s | — | first word read ≤15 min | same | same |

### 1.2 Their first month (illustrative, from the sitting ratios)

- **Ayesha** (~30 sittings): L1.02–L1.06. Gates are "checked by tapping". The village has 10 buildings, one per sound met.
- **Leo** (20–26 sittings): L2.03–L2.06.
- **Bilal** (fast track, ~20 sittings): about L1.02–L1.12.
- **Rukhsana** (~16 sittings, interrupted): L1.02–L1.06. She resumes on the same screen each time.
- **Nana** (~20): L2.01–L2.07.

---

## 2. The pedagogical engine

### 2.1 The course mapped to the app (v1 = L0–L5)

Block counts are from a grep over all 108 files, corrected by the round-2 auditor. The week-1 parser report is authoritative.

| Level | Lessons | Template | Notes | v1? |
|---|---|---|---|---|
| 1 | 14 | lesson | Blend 13, Listen & Talk 14, Track B 12 | yes |
| 2 | 14 | lesson | Listen & Talk 13, Track B 13 (L2.14 mentions it only in prose) | yes |
| 3 | 18 | lesson | Listen & Talk 17 (L3.18 only in tutor notes), Track B 17 | yes |
| 4 | 16 | lesson | Blend 14, Listen & Talk 15, Track B 15 | yes |
| 5 | 16 | session | Retrieval, Prime, Write 16; Word work 15; Track B 16; Listen & Talk 0 | yes |
| 6 | 16 | session | Track B 0; checks have prose answer keys (e.g. L6.05) | **v1.1** |
| 7 | 14 | session | Track B 0; **L7.03 states no pass bar** | **v1.1** |

Order and the 69 heart words (L1 24, L2 29, L3 16) live in `data/gpc.json` and `data/heart.json`. Track B calls them **"tricky words"**.

### 2.2 Strands

- **Code** (L1–L4): Hear, Meet, Blend, Spell, Tricky words, Check.
- **Read it**: Track A or B text, with 2 literal questions and 1 think question.
- **Listen & Talk** (L1–L4, §3.8).
- **Review**: the warm-up is the review.
- **Fluency** from L2.
- **Morphology** L4–L5 in v1.
- **L5 sessions**: prime the topic, knowledge text, write to read.

### 2.3 Every rule, enforced

| Rule | Mechanism | Check |
|---|---|---|
| 1 No cueing | No image beside an undecoded word. Repairs never start with the whole word. Reader tap-a-word plays the grapheme sounds first; the whole word plays only after an attempt | DOM test. Audio-trace test: no whole-word clip between a wrong answer and the next attempt |
| 2 Decodable (L1–L4) | Cumulative GPCs + scheduled tricky words + ≤2 flagged story words | `decodable.py` on the JSON |
| 3 Blend before segment; spell after blend | Every sitting's step list puts blend before spell. Single-sound sittings have no word spelling | Snapshot test over real L1.02–L1.12 JSON |
| 4 Mastery gate | Each check uses its lesson's stated bar on **judged items** (§3.6); default 0.9; real and pseudo scored separately at level checks | Reachable-score unit test per lesson; per-lesson below-bar oracle run |
| 5 Tricky words mapped, not flashed | E8 map; tricky-word E6d uses the regular-decoding foil | Lint: 69 `heartIdx` |
| 6 Two registers | `read.B` or `sameAsA` in L1–L5 | Parser + child-coded-word lint |
| 7 Comprehension daily | Listen & Talk in L1–L4 lessons that have it; L5 prime + text + questions | Coverage report |
| 8 Two metrics | No blended score; "pace" vs WCPM labelled | Schema + UI grep |
| 9 L1 notes | `l1_tags`; Urdu notes unchanged from the course | Tag lint |
| 10 Pause-safe, no streaks; skip = take the check | Days practised only goes up; checkpoint on every screen; Leitner in sittings; **"I already know this" sits behind the grown-up gate** | Kill/resume ×20; string lint |
| 11 Multisensory optional | Trace on by default for Track A and Track B Level 1, with a visible skip | Settings test |
| 12 Honest citations | Listing and in-app claims come from the evidence tables only | Listing review |
| Machine never promotes **mastery** | A tap-judged gate unlocks the next lesson as "checked by tapping"; "mastered" needs a helper. **This departs from research-03 §6**, which asked for an adult to confirm every gate. Reason: in a home with no English reader the child would never progress (parent critics, rounds 1–2). Mitigations: decoding-sensitive foils, a delayed re-check, optional helper upgrade, and a v1 validity test (§12.2) | Gate-reducer tests |
| Audio never leaves the device | v1 has no microphone at all | Manifest has no `RECORD_AUDIO` |
| No ads/account/analytics | Dependency allowlist | CI |

---

## 3. Product

### 3.1 Profiles, gates, launch

- **Phone with one adult profile.** The app opens straight into his lesson. No PIN is asked on launch (relaunch to lesson ≤10 s). The PIN only guards settings. An optional "ask my PIN every time I open" switch is for privacy from customers.
- **Phone with children.** The launch screen shows two doors: a large **"Children"** door (opens the child tiles) and a small lock **"Me"** (adult PIN). An adult never sees child avatars unless he opens the Children door. A child never sees an adult's name.
- **Adult PIN, set on first adult launch.** "Me" → night-one lesson → stop-here screen: *"Make a 4-number code so only you open your lessons."* Enter it twice, digits in the UI language's numerals. "Later" postpones it once; it is asked again at the next stop-here. Without a PIN, gated actions are unavailable.
- **Child profiles get a 4-shape pattern** (e.g. star, fish, moon, ball), set by the grown-up when the child profile is named at its first stop-here screen. Siblings cannot enter each other's profiles. A forgotten pattern is reset from the grown-up area.
- **Behind the grown-up PIN only:** "I already know this", placement and re-placement, delete or reset a profile, restore a backup, pack downloads on mobile data, helper sessions, changing the role or track ("Not right? Change who is reading" is the undo for a wrong role tap), links out.
- **Destructive actions** need the PIN plus a spoken hold-to-confirm.
- **No microphone permission is requested in v1.** This removes the day-2 English system dialog the parent critic flagged.

Tabs:
- Track A: Path · Stories · Practice · Me.
- Track B: Lessons · Read · Practice · Progress.

Every screen auto-plays its instruction once (Track A, and Track B L1–L2), then on tap. "Hear it again" is on every screen.

### 3.2 The sitting model

- Budgets: Track A ≤8 min (lint-enforced), Track B 10–15 min.
- One new GPC per sitting in L1–L4. Pattern lessons get at most 5 new words per sitting: L2.06's **21** initial blends become 5 sittings by family.
- **Track A L1.02, matching the JSON in §6.2:**
  - A, s: hear, meet, trace → write from memory, sound game.
  - B, a: warm-up (≤3 cards), hear, meet, trace, blend "sa", spell "sa" with tiles.
  - C, t: warm-up, hear, meet, trace, blend 4 items, spell "at".
  - D: warm-up, blend 4 items, tricky words *a, I*, spell "sat".
  - E: Read it (Track A text, 3 questions).
  - F: Listen & Talk (alternate day).
  - G: Check (11 items, E6d + dictation).
- **Typical two-letter lesson, Track A (~6 sittings):**
  1. Sound 1 (hear, meet, trace, blend 4–5, spell 2).
  2. Sound 2 (same).
  3. Blend 4–5 + tricky words + spell a sentence.
  4. Read it.
  5. Listen & Talk.
  6. Check.
- **Track B** merges these into ~3 sittings. Fast track: after a ≥90% mini check, the next course sitting continues in the same session. That is how night one covers A+B+C.
- **Mini checks** never lock; they repeat a step.

### 3.3 Exercise catalogue

| ID | Exercise | v1 / v1.1 | Judge |
|---|---|---|---|
| E1 | Sound game: two spoken words, tap the one that starts/ends with the sound (no pictures) | v1 | machine |
| E2 | Meet card: letter, human sound, mouth picture, Urdu tip | v1 | — |
| E3 | Sound tap: hear a sound, pick its letter | v1 | machine |
| E4 | Trace → write from memory (§3.9) | v1 | machine, formative |
| E5 | Blend it, learner-led (below) | v1 | self + E6d |
| **E6d** | **Read it, pick what it says** (below): the gate item for real words, pseudowords and tricky words | v1 | machine |
| E7 | Spell: tiles (A), keyboard + tiles (B); error classes | v1 | machine |
| E8 | Tricky-word map | v1 | machine |
| E9 | Reader + questions | v1 | literal machine, think self |
| E10 | Listen & Talk (§3.8) | v1 | — |
| E11 | Check = E6d items + dictation (E7) at the lesson's bar | v1 | machine |
| E12 | Leitner card | v1 | machine |
| E13 | Morphology builder (L4–L5) | v1 | machine |
| E14 | Listen-and-follow fluency: phrase highlight with the model voice, tap along | v1 | practice |
| E15 | Timed read: "pace" solo, WCPM in a helper session | v1 | helper / pace |
| E16, E17 | Prime the topic; long-text reader (L5) | v1 | MCQ machine |
| E19 | Write to read (L5): frames, then the model answer side by side with a 4-point rubric the learner ticks | v1 | self (practice), key-term check |
| E22 | Ear training: minimal pairs (vet/wet, sat/set, ship/chip) | v1 | machine |
| E23 | b/d (from L1.09, once both are taught) and b/d/p/q (from L1.12): formation anchor first ("b: bat, then ball"; "d: c, then the line"), then pick-the-letter | v1 | machine |
| E18, E20 | Reciprocal teaching; lateral reading | **v1.1** (L6–L7) | — |
| E21 | Record and replay, self-compare (needs mic) | **v1.1** | self |

**E5, Blend it (learner-led, no microphone):**
1. On the first item of a new pattern only, the teacher voice models continuous blending under the highlighter ("sssaaat… sat").
2. The learner **says each sound first**, then taps the letter. The tap plays the sound as confirmation, never before.
3. The learner slides a finger under the word, saying it smoothly, then taps "I said it". The word plays. "Same as you?" Yes moves on.
4. **Repair** on "No", or when E6d misses this word later: the human **continuous** blend clip ("sssaaat"), the L1–L2 slow take. Then the learner tries again.
   - From L3 there are no stretched takes. Repair uses the human grapheme sounds with gaps ≤150 ms, plus syllable chunks for L4 multisyllabic words.
   - Accepted v1 weakness: the continuous-blend repair exists only for L1–L2.

**E6d, Read it, pick what it says:**
1. The written word appears alone. The teacher voice (instruction in the UI language) says: *"Read it to yourself."*
2. After 1.5 s, four plain buttons appear, each playing one spoken word: the target and three foils. All share the onset and differ in the middle and/or end on a 2×2 grid: *sat / sit / sap / sip*. For two-sound words there are three options: *at / it / ap*.
3. The learner taps the one the print says. The response window is 6 s from the last button played. A timeout counts as **unjudged**: the item is re-presented once later, and if unjudged again it goes to review and does not count.
4. **First wrong tap:** the grapheme sounds of the printed word replay **one at a time** under the highlighter. The repair is targeted by the foil chosen: a vowel foil replays the vowel with its mouth cue, an end foil replays the final sound. Then the same four options are reshuffled. In a check, a continuous blend would give the answer away, so E6d uses separate sounds; E5 practice uses continuous blending.
5. **Second wrong:** the item goes to review. The whole word plays only now, after two attempts.
6. **Gate counting:** only the first attempt counts (§3.6).

**What E6d measures, stated honestly.** It is a decoding proxy: print → phonology recognition. It is not oral reading. Because all options share the onset, **first-letter matching cannot pass it**. A learner who decodes only one of {vowel, final letter} is at 50% per item: P(≥10/11) = 0.6%, P(≥9/11) = 3.3%. Pure guessing (25%) is negligible. The delayed re-check (§3.6) cuts these further. The v1 validity test is in §12.2.

### 3.4 Track A experience layer (built against Teach Your Monster)

- **Mascot: Pebble** (working name, D18). A new character, not Marko. A small round creature, built on the existing Lottie pipeline.
  - **Pebble never speaks.** It waves, listens, cheers and points with sound effects. The teacher voice does all speech, so one voice is kept.
- **The village.** Every sound met adds one thing to Pebble's village: s brings the sun, a an apple tree, t a tent. It appears only after the sound is learned, never beside an unread word.
- **Rewards never withheld for errors:**
  - every finished sitting earns a sticker and a celebration;
  - every new sound met adds a village piece.
  - Gate passes add a pearl on the path, a progress marker, not a prize. A wrong answer never costs anything.
- **What Ayesha does alone in 8 minutes (Sitting A):**
  1. 0:00 Pebble waves; the Urdu line, then the English line: "Let's meet a sound!"
  2. 0:20 E1: hears two words, taps the one starting with /s/ (×4).
  3. 0:60 E2: big **s**, the human /s/, mouth picture; "Say it!"; she taps the s.
  4. 2:00 Trace s ×3, then write it from memory on a blank canvas with a start dot.
  5. 4:00 Pop the s-bubbles (E3 variant, s among unknown shapes, ×6).
  6. 6:00 The sun rises over the village.
  7. 7:00 Sticker + celebration.
- **What she shows her mother.** The last screen, "Show your grown-up", has the big s, her sticker and a play button. She says /s/; her mother taps the button to hear the teacher's /s/ and compare. This works without the mother reading English.
- **Bar.** Teach Your Monster's play loop. G1/G2 (§12.3) score delight and guess-resistance against it.

### 3.5 Night one and opt-in placement

- **Child:** role → Sitting A (§3.4). **Exit check:** first letter sound heard and tapped ≤90 s from first launch.
- **Adult:** role → one 15-minute sitting covering course Sittings A+B+C of L1.02:
  - s, a, t, each heard, met and said;
  - E5 blends "at", "as", "sat";
  - E6d reads them;
  - E7 spells "sat" with tiles;
  - stop-here screen, PIN setup.
  - **Exit check:** a real word read by the learner ≤15 min from first launch, in private, with no test.
- **L1.01 order (D29).** The app starts at L1.02. L1.01's oral games are the Hear-it items of the first sittings. The full L1.01 runs as a repair after two Hear-it misses, or when placement Stage 1 places there.

**Placement** (behind the grown-up PIN; "I can already read some English"). It follows `placement-test.md`. The file's tester script: *"Some of the 'words' aren't real words — they're made-up. Just tell me the sounds you'd make if you saw them. There's no embarrassment here; this just tells us where to start."*
- **Stage 0:** not asked aloud. Q1 = pressing the button; Q3 = UI language; Q2 is one optional silent card; Q4 moves to the screener.
- **Stage 1** (oral deletion/substitution, 4 levels × 8; answers include non-words such as "ig", "ap", "han"):
  - **in a helper session**, the app speaks each item and the helper taps *right and quick* / *right but slow* / *not right*. That gives the file's Correct and Automatic (2 s) outputs. Stop below 6/8 Correct.
  - **with no helper, Stage 1 is skipped**, as the file's self-test section allows, and the learner goes to Stage 2.
  - Never machine-judged in v1.
- **Stage 2:** Blocks A (26, <24 → first missed letter), B (5, any miss → Level 2), C (7 → Level 3/4). The app version is receptive (E3: hear the sound, tap the letter), labelled "hearing version".
- **Stage 3:** tiers of 8 real + 8 pseudo via E6d, pass ≥14/16. Placement = first tier below 14/16. Tier 1 below 90% → **L1.02**.
- **Stage 4:** only if Tier 3+ cleared, and only in a helper session (passages A/B/C, Hasbrouck–Tindal Fall 50th: G2 50, G4 94, G6 132 WCPM, DIBELS 3 s rules). Otherwise skipped. Passage C ≥132 would mean Level 6, which in v1 places at L5's end with "Level 6 arrives in an update".
- **Result:** "Start at Level N, lesson K", earlier/later options, no score. Three forms (C3).

### 3.6 Pass bars, gate counting, states

**Bars as stated in the course:**
- L1.02 Check ≥9/11 (81.8%). L1.03–L1.13 ≥10/11.
- ≥4/5 appears 19 times in 10 Level 1 lessons (L1.01, L1.03–L1.09, L1.11, L1.12), mostly mini checks.
- L3 "≥90%". L5 ≥5/8 or ≥6/9. L6 "4/5 or more". **L7.03 none.**

The app stores each bar and applies it to **judged items only** (timeouts excluded). If a check has fewer judged items than the bar's denominator, the missing ones are re-presented. **Only first attempts count.** A repaired second-attempt success is praised but not credited. The lower bars and the missing L7.03 bar go to a course ticket (D27); the app follows the course's answer. L5 gates score only machine-judged components; self-judged parts (E19) are practice. A gate with no machine-judged items is not scored as passed.

**L1.02 freshness.** s/a/t cannot yield three fresh pseudoword sets. Its re-check reuses the set in a new order with a new dictated item.

| State | When | Then |
|---|---|---|
| `in_lesson` | unlocked | sittings |
| `checked` | bar met on first attempts (E6d + E7) | **next lesson unlocks**; label "Checked by tapping"; delayed re-check scheduled 3 sittings later (fresh items where they exist) |
| `rechecked` | delayed re-check passed | label "Checked twice" |
| re-check failed | — | a repair sitting is inserted, the items go to daily review, grown-up flag; no relock |
| `mastered` | helper session confirms the learner reads the items aloud | optional upgrade; "Checked by [helper]" |
| `reteach` | bar missed | the lesson's named reteach step, then re-check next sitting |
| `still_learning` | second park on one gate (third miss → park → repair → miss again) | **next lesson unlocks** anyway, the gate's items stay in daily review and are re-checked every 3 sittings, grown-up flag. Never locked |
| `level_check` | last lesson checked | pass → re-placement slice; fail → reteach by error class |

### 3.7 Review

5 Leitner boxes in sittings (1, 2, 4, 8, 16); a wrong answer drops one box, two wrong in a row → box 1. Track A warm-up ≤3 cards, Track B ≤6. Welcome-back of 3–6 cards, no backlog. Items sent to review by E6d enter box 1.

### 3.8 Listen & Talk (L1–L4)

- **Track A, for Urdu-only children:**
  1. A one-line Urdu gloss of the chunk is spoken first (Urdu voice, §4.5).
  2. Then the English chunk (2–3 sentences, teacher voice).
  3. A picture appears after each chunk.
  4. Tier-2 word: English, then its Urdu gloss.
  5. "Talk": an optional recorded answer for the helper, labelled optional. In v1, with no microphone, it is "tell your grown-up", a prompt card shown in helper sessions.
- **Track B:** chunks with an Urdu gloss on tap; shadowing ("say it after me").
- **Pilot check:** two literal Urdu questions after each block, target ≥80%. The pilot also A/B tests picture-before versus picture-after, as the teacher suggested.

### 3.9 Letter formation and writing

- **E4:** three traces with the guide. After 3 correct traces the guide fades to a start dot only (**write from memory**), scored the same way.
- **Scored per stroke:** start point (tolerance 20% of glyph height for Track A, 12% for Track B), stroke count, order, direction, checkpoints in order, end. Formative only, never a gate.
- **Feeds:** misses feed `formation`; b/d/p/q confusions feed `bdpq` (E23).
- **Spelling:** E7 in every lesson after blend.
- **L5 writing:** E19.

### 3.10 Helper sessions (optional)

PIN → "I'm sitting with [child]". Only here:
- "Got it / Not yet" buttons on read-aloud items;
- Stage 1 and Stage 4 of placement;
- WCPM marking;
- the judge's card, with five error types and the teacher's audio examples.

`mastered` upgrades need the 5-example classification (canvas `v6-changes.md`). Children progress fully without helpers.

### 3.11 Progress, motivation, comfort

- **Grown-up page:** Decoding (real/pseudo per level, labelled *checked by tapping / checked twice / mastered*), Comprehension, Fluency (pace or WCPM vs Hasbrouck–Tindal, reference only), flags (still learning, failed re-check, repeated on-ramp, screener).
- **No blended score.**
- **Track B:** "words you can read now".
- **No streaks or hearts.** Reminders opt-in, weekly cap, off for Track A unless the parent turns them on.
- **Comfort:** size, spacing, tints, contrast, OpenDyslexic as an option, reduce motion. **Slow mode** uses the human slow takes for L1–L2 blend words. No slow mode from L3 in v1.
- **Screener:** optional, private.

### 3.12 Screens

Launch (Children door / Me lock) · Role · Sitting runner · Stop here (nickname, shapes, PIN) · Shape pattern · PIN · Track A village · Show your grown-up · Placement (helper/PIN) · Result · Screener · Path/Lessons · Check result · Re-check opener · Level 3 handover ("a new reader joins you") · Stories/Read · Reader · Listen & Talk · Practice · Me/Progress · Grown-up area · Helper session · Pack download (MB shown, ask every time) · Missing pack ("This level needs a download, N MB. You can still review.") · Comfort · Welcome back.

---

## 4. Voice

### 4.1 Clip inventory and size (download and installed)

**Basis.** Ranges use research-05 §3 per-level counts as the low end. The high end applies the undercount ratio 9,238 / 5,763 = 1.6 to words, ±25% to sentences. The week-2 recount settles them.

**Human voice, Levels 0–2:**

| Type | Count (range) | KB each | MB |
|---|---|---|---|
| Words L1+L2 (1,066 + 575) + L0 (187) | 1,828 – 2,925 | 2.5–3.0 | 4.6 – 8.8 |
| Pseudowords: generated (L1–L2 share, below) + markdown's own (estimate ~250) | ~560 | 3.0 | 1.7 |
| E6d foil words not already in the lexicon | 800 – 1,500 (estimate; generator report week 2) | 3.0 | 2.4 – 4.5 |
| Sentences L1+L2 (297 + 515 = 812 ± 25%) | 610 – 1,015 | 12.5 | 7.6 – 12.7 |
| Tier-2 lines (~28 lessons × 2 × 3) | ~168 | 12.5 | 2.1 |
| English UI prompts | ~200 | 9 | 1.8 |
| Slow continuous-blend takes (L1–L2 blend words) | 350 – 460 (estimate) | 5 | 1.8 – 2.3 |
| Phonemes 44 + 3 combination clips (/ks/, /kw/, /juː/) | 47 shipped (×3 takes recorded) | 2.5 | 0.12 |
| Blending demos (23 lessons × 3) / judge's-card examples | 69 / 10 | 9 / 6 | 0.7 |
| **Human total** | **~4,640 – 6,950 clips** | | **~23 – 35 MB** |

**Urdu voice** (instructions, glosses, Listen & Talk lines): ~600 clips, ~3.6 MB. See §4.5 on why this second voice exists.

**Pseudoword derivation (whole of L1–L4).**
- L1.03–L4.16 is 60 lessons; 4 are mastery-check lessons. That leaves **56 lesson checks × 2 extra sets × 5 = 560**.
- Level checks: 4 × 2 × 10 = 80. Placement forms B/C: 5 tiers × 8 × 2 = 80.
- **Total 720 generated.**
- L1–L2 share: 24 checks × 10 + 2 × 20 + tiers 1–2 × 16 = 312, plus the markdown's own (~250, estimate). The week-1 parser counts the markdown.

**Kokoro packs (v1: L3–L5):**

| Pack | Words (range) | Sentences (range) | Pseudo + foils + Tier-2 | MB |
|---|---|---|---|---|
| L3–L4 | 1,156 – 1,850 | 510 – 850 | ~408 generated, 700–1,400 foils, ~204 Tier-2 | 15 – 22 |
| L5 | 938 – 1,500 | 550 – 910 | ~200 word-work lines | 12 – 18 |
| v1.1: L6 / L7 | research-05: 18 / 11 (low end) | | | 29 – 45 |

**Install, v1.** Pure Capacitor WebView, **no native libraries**, one universal APK. The two-ABI and 16 KB-alignment issues disappear.

| | Download | Installed (on the phone) |
|---|---|---|
| Shell (JS, Lottie, Andika, art) | ~8 (estimate) | ~8 |
| Base audio: human L0–L2 + Urdu voice | 26 – 38 | 26 – 38 (Opus is stored as-is) |
| Runtime overhead (ART, IndexedDB, WebView cache) | — | +3 – 10 (estimate) |
| **App install** | **~34 – 46 MB** | **~37 – 56 MB** |
| Packs L3–L4 + L5 (asked each time, MB shown) | 27 – 40 | 27 – 40 |
| **All of v1** | **~61 – 86 MB** | **~64 – 96 MB** |

`bundletool get-size total` gives download size. Installed size is read from Android Settings → Apps on the test phone in week 3. Competitor figures are iOS MiB; ours are MB, and the units differ by 4.9%. **No rupee figures**: data prices are unverified.

### 4.2 Kokoro pipeline (L3–L5; L6–L7 in v1.1)

1. **Pinned Docker image**: kokoro, misaki, torch, system espeak-ng, the thread count and the CPU flags. **Seed fixed per clip** (derived from the clip id). The audio critic found same-input renders differ without a seed, and 1 vs 8 threads differ even with one. All versions, the seed and the threads go **into the clip id**. An approved clip id is never re-rendered.
2. **Day-1 OOV count.** misaki lookup over all 9,238 words; the count is published.
   - In the Docker image with system espeak-ng, the fallback is allowed only to **propose** IPA for OOV words. Proposals are reviewed and written to `pron.json`, never rendered directly. The bundled `espeakng-loader` that aborted (research-02 §3) is not used.
   - The engineer estimates several hundred to ~1,300 OOV derivatives across L3–L7.
3. **`ipa2misaki.py` mapping table**, owned by the build agent, delivered in week 1. Includes misaki's single-symbol diphthongs (`A I W Y O`), `ʤ ʧ`, `ɜɹ`. Round-trip vocabulary gate: Kokoro silently drops unknown symbols.
4. **Heteronyms and "a"/"the"** in `pron.json`.
5. **Speed 1.0 only.** No slow mode from L3 in v1. No per-clip speed changes, no carrier crops.

### 4.3 One post-process for every clip (human and Kokoro)

1. Trim with a −45 dBFS energy detector, keeping the full burst on stop-final words.
2. Pad **40 ms head / 80 ms tail**. Fades are 5 ms, except **stop-final clips, whose fade-out is never shorter than 15 ms**, so the release burst survives.
3. **Loudness, one rule:** −18 LUFS integrated for every clip ≥0.4 s. For shorter clips, gain is set so that a **0.4 s window centred on the clip's energy peak** measures −18 LUFS. One scale, so neighbours in a word list do not step 4 dB apart.
4. **True-peak limiter at −1.5 dBTP, applied after gain.**
5. Opus 24 kbps mono. All measurements are taken on the decoded Opus.
6. **The gap between a phoneme sequence and its blended word is 350 ms of silence authored in the exercise timeline**, not baked into clips. The same goes for the gaps between phonemes in E6d repairs.

### 4.4 QA

| Stage | What | Who | Scope |
|---|---|---|---|
| Q1 | coverage, hash, padding windows (30–60 / 60–110 ms), loudness: every class mean within 1 dB of sentences and 95% of clips within 2 dB; clipping | script | 100% |
| Q2 | faster-whisper transcript = text | script | real words, sentences |
| Q3 | `listen_judge.py` with new English prompts; pseudowords by forced choice among 4 foils | Gemini, triage only | pseudowords, Q2 fails |
| **Human clips** | Take chosen at capture by the recording engineer. Then **two listeners**: the GA reviewer (100% of phonemes, pseudowords, foils, demos; 10% of words and sentences) and a second listener (a teacher or Kamal) on a 100-clip overlap, with an anchored 1–5 scale (anchor clips for 1/3/5) for clarity, pace and warmth. Cohen's kappa reported. Approved ids are **frozen**; changes need a pickup session | GA reviewer + second listener | as stated |
| **Kokoro clips** | GA reviewer samples **10% per pack + 100% of IPA overrides and pseudowords**, **once per frozen pack version**. The review is **skipped on rebuilds whose clip ids did not change** | GA reviewer | as stated |
| Determinism | 100 clips rendered twice on two machines must be bit-identical, or the drifting component is named | script | per build env |

Reviewer load for the L3–L5 packs: about 3,000 Kokoro clips → ~300 sampled + ~400 pseudowords + overrides. At ~8 s each, that is roughly 2–3 hours per pack version (estimate).

### 4.5 The human teacher voice and the recording kit

**Choosing the speaker (D16).** A comfortable, natural **General American female** voice. Three candidates send a 20-item test file. The GA reviewer scores accent features (rhoticity, /æ/, /ɑ/, flap t). Three blind listeners rate pace and warmth against af_heart sentences, because the learner meets af_heart at Level 3.
- **No F0 or spectral target.** af_heart's word F0 sits at 215–238 Hz, at the top of the adult range, so matching it would rule out most natural voices.
- Spectral matching has no valid reference: Kokoro's isolated /s/ is a 513 Hz rumble, and in-word fricatives vary per word (9.1 kHz in "sat", 5.7 kHz in "ship").
- Under D0a the voices never alternate inside an exercise. The only join is the announced Level 3 handover, where pace and warmth are what a learner notices.

**Session conditions.** The speaker works remotely, in her own treated space, against a spec and an approved test file. 48 kHz mono WAV, no AGC or noise suppression, mic at 20–30 cm. Each session starts with room tone and a reference /æ/ compared with session 1. Script delivery via `voice_studio.py` or our script sheets.

**What she records.**
- The **44 phonemes**: 24 consonants /p b t d k g tʃ dʒ f v θ ð s z ʃ ʒ h m n ŋ l r w j/ and 20 vowels: /æ ɛ ɪ ɑ ʌ ʊ ə/, /iː uː ɔː ɝ/, /eɪ aɪ ɔɪ aʊ oʊ/, /ɑr ɔr ɛr ɪr/.
- 3 combination clips. Every clip ×3 takes.
- Then all L0–L2 items in §4.1, the slow continuous-blend takes, 69 demos and 10 judge examples.

**Studio time.** About 4,640–6,950 clips at ~250 clips per hour including retakes is **~19–28 studio hours**. That is about 8–12 sessions of 2.5 h across weeks 2–5: phonemes, demos, UI and L1 first, then L2. A fee is budgeted under D16.

**Urdu voice.** Urdu instructions and glosses are a different language. They come from a separate Urdu voice: the existing Sara clips if their licence covers this app (D9), otherwise one recorded Urdu speaker. This does not break the one-English-voice rule. The UI keeps Urdu and English on separate lines, never mixed inside one clip.

### 4.6 Licences

| Asset | Licence / action |
|---|---|
| Kokoro-82M | Apache-2.0 (training data not verified line by line); versions in LICENSES.md |
| misaki | check in week 1 |
| Human recordings | signed release: perpetual, worldwide, commercial |
| Urdu voice | Sara licence check or new release (D9) |
| Course content | CC BY 4.0, attributed |
| Andika | SIL OFL per research-05; verify |
| Piper | Blizzard 2013 Lessac licence clause 3.2 grants use exclusively for Research Purposes (read by the lead 2026-10-05). Not used |
| OpenMoji | CC BY-SA 4.0 (no source in folder); check before use |

### 4.7 What still fails

| Failure | Handling |
|---|---|
| L0–L2 content edits after recording | Text frozen per level before its sessions; pickup sessions budgeted (~2 h/month) |
| Speaker unavailable mid-build | Book in week 0; L1 recorded first so a delay hits L2 only |
| Level 3 voice change disliked | Announced handover; pilot question; G5 rating. Fallback: record L3 with the human too (cost +~10 h, estimate) |
| Kokoro OOV and IPA drops | Day-1 count, mapping gate, reviewed overrides |
| Continuous-blend repair missing from L3 | Accepted in v1; v1.1 candidate |
| No child voice | Accepted |

---

## 5. Listening

**v1: none.** No microphone, no speech judging (D0b). Read-aloud production is checked only by a helper, optionally, for `mastered`.

**v1.1: record and replay.** The learner records a word or a line and hears it next to the teacher's clip. Practice only, labelled "practice". The audio stays in memory and is discarded. The microphone is requested at the first use of this feature, behind the grown-up PIN for child profiles.

**v2: phoneme verifier.**
- **Model.** A CTC phoneme model (a wav2vec2-class frame classifier, e.g. the charsiu family) exported to ONNX and run through onnxruntime in a small native plugin.
- **Scoring.** Our own CTC forward pass scores the target phoneme sequence against competitor sequences: vowel swap, dropped final sound, onset swap, schwa insertion, letter name, and the regular decoding for tricky words. The margin gives yes / unsure / no.
- **Effort.** 10–15 working days before any kid data (engineer estimate).
- **Kid gold set.** ≥60 items **per class**: real CVC, pseudo, tricky, sentences, isolated sounds. Labelled by a **native General American speaker, not Kamal**, with Kamal as second rater. Children recorded in the gated research mode with parent consent. Thresholds: `clear_yes` precision ≥97% with lower 95% bound ≥92%, recall reported. When n is short, the class is reported "undecidable" and is a no-go by default.
- **Urdu-accented vowel merges** (/æ/–/ɛ/, v/w) are flagged as practice with the matching E22 pair, **never counted as wrong**.
- **Gate role.** Only after a class passes may the verifier add credit to a gate, and only on top of E6d, never replacing it. Unsure and no never cost the learner anything.
- **Privacy.** On device, metrics only, no voiceprints (COPPA, research-04 §5).

This reverses research-03's v1 stack (a Whisper witness for real words) and research-04 D6. The reasons are in §0 D0b.

---

## 6. Tech

### 6.1 Repo and reuse

- **Repo.** `read-english` (`com.oyekamal.readenglish`), files copied from `urdu-reading-course/mobile`, plus `PROVENANCE.md`.
- **Copied code** (research-05): 12% as-is, 70% with changes.
- **New work, named:**
  - the level/lesson/sitting state machine;
  - the v1 exercise set (§3.3);
  - placement;
  - the gate reducer;
  - the Track A village layer;
  - the profile shapes and PIN flow.
- `path.js`, `learner.js`, `onboarding.js` and `drills.js` are rewrites, not edits (engineer).
- **No native plugin in v1.** minSdk 23 as in the Urdu app, targetSdk 36.

### 6.2 Content pipeline

- **Parser.** `build_content.py --strict` over all 108 + 7 files from day 1.
- **Week-1 exit:** a coverage report per file, plus a **yield number**: the share of L1–L5 lessons whose check items, bar and pseudoword set parse without help. **Target ≥95%.**
- **Gaps** (error classes, reteach steps, bars written in prose) go into reviewed `app:` YAML blocks, sent as PRs to the course repo. Never inferred.
- **Round-trip diff** against the source markdown.

```jsonc
// content/lessons/L1.02.json  (Track A sittings match §3.2; Track B merges them)
{ "id":"L1.02","level":1,"type":"lesson","contentVersion":"2026.10.1",
  "sittings":{
    "A":[{"id":"A","new":["s"],"steps":["hear","meet","trace","sound_game"]},
         {"id":"B","new":["a"],"steps":["warm","hear","meet","trace","blend","spell"]},
         {"id":"C","new":["t"],"steps":["warm","hear","meet","trace","blend","spell"]},
         {"id":"D","steps":["warm","blend","tricky","spell"]},
         {"id":"E","steps":["read"]},{"id":"F","steps":["listen"]},{"id":"G","steps":["check"]}],
    "B":[{"id":"ABC","steps":["hear","meet","blend","pick","spell"],"fastTrack":true},
         {"id":"D","steps":["warm","tricky","read","listen"]},{"id":"G","steps":["check"]}] },
  "blend":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"]},
  "pick":{"sat":["sit","sap","sip"],"at":["it","ap"]},                 // E6d foils, same onset
  "tricky":["a","I"],
  "check":{"items":[…],"bar":{"pass":9,"of":11,"source":"lesson"},"firstAttemptOnly":true,
           "freshSets":false,"reteach":{"step":"C"},"errorClasses":{…}} }
// lexicon: { "sat":{"g":[…],"p":[…],"kind":"decodable","voice":"human","audio":{"n":"…","slow":"…"}} }
// placement.json: forms A/B/C; stage1 (helper-only); stage2 blocks; stage3 tiers (E6d foils); stage4 passages + HT cuts
```

Gates (`npm run content` fails):
1. Decodability on L1–L4.
2. Pseudoword filter: CMUdict, lexicon, blocklist, IPA homophones, native-review flag.
3. **Foil validity**: every E6d foil shares the onset and differs in the middle and/or end on the 2×2 pattern.
4. OOV/IPA round-trip.
5. Audio coverage + Q1.
6. Every bar reachable on judged items.
7. Sitting budget ≤8 min (Track A).
8. No-cueing strings.
9. Sizes within the §4.1 ranges +10%.
10. Snapshots + round-trip.

### 6.3 Audio engine (kept from the Urdu app)

- The Urdu `content.js` pattern stays: **one shared `Audio()` element**, a one-deep queue for instructions, content clips interrupting, and a **1.5 s watchdog that rebuilds a wedged element**.
- The only change: the source is a **per-lesson sprite file** (one Ogg Opus per lesson) plus an offsets JSON. `play(id)` sets `currentTime` to the clip start and stops at its end with a timer. **No WebAudio rewrite.**
- **Week-1 device check:** seek accuracy p95 <20 ms on the test phone's WebView; p95 tap-to-sound over 200 taps.
- **Fallback if seeking is imprecise:** per-clip files, the Urdu pattern exactly (it shipped 1,463 files). Per-lesson zips are extracted on download, accepting roughly +30% disk for block waste.
- Bytes come from `Capacitor.convertFileSrc` URLs, never base64 over the bridge.

### 6.4 Data, migrations, backup

- **Stores**, kept from the Urdu app: settings, profiles, attempts, cards, sessions, progress, assessments. Added: `mastery`, `packs`, `helper`.
- **Migrations.** Delete the Urdu `db.js` repair path that bumps `version+1` (it would race migrations). Start `DB_VERSION=1` with a real `onupgradeneeded` ladder, one tested step per version, using fixture DBs.
- **Progress keys** are lesson ids and item text, never clip ids.
- **Packs** carry `contentVersion` + `gpcHash`. Incompatible packs are rejected ("update the app first").
- **Signed pack manifest.** ed25519; Kamal holds the key (D32); the public key ships in the app. Resume is per file (`Filesystem.downloadFile` has no Range resume; per-lesson files are ~0.3–1.1 MB).
- **Launch reconcile** of packs on disk vs IndexedDB.
- **`backup.js` id-format change.**
  - Progress keys move from `^\d{1,2}$` (Urdu units 0–12) to `^L[1-7]\.\d{2}$`.
  - The unit field becomes a lesson field.
  - Card kinds change from `letter|word|sight` to `gpc|word|tricky|tier2|morph`.
  - Card ids become `profileId:kind:sha1(text)[:8]`, so apostrophes and spaces never reach the id regex.
  - The new stores are added to `SCHEMA`. `BACKUP_FORMAT = "read-english-1"`.
  - **Migration:** no English backups exist yet, so there is nothing to migrate in v1. An Urdu-app backup is rejected with a clear message. Future format bumps carry an upgrade function per version, mirroring the DB ladder.
  - **Round-trip test in week 3** with an L1.02 key and an apostrophe word ("don't").

### 6.5 Devices and budgets

- **D24 (week 0):** buy a 2–3 GB Android 10 phone. Kamal's phone is the second device. No device is attached today.
- **Budgets (targets, not measurements):** cold start <2 s; lesson render <100 ms; tap-to-sound p95 <150 ms; JS <150 KB gzip; memory <150 MB; child night one ≤90 s to first tap; adult ≤15 min to first word.

### 6.6 Test harness (tagged auto / device / human)

**Auto** (green before week 4):
- parser coverage, snapshots, round-trip; content gates;
- oracle: completes L1–L2; below-bar run per lesson reteaches; **perfect-decoder oracle reaches L1.06 in bounded sittings with no helper**;
- **final-letter-only oracle fails the L1.03–L1.06 gates** (expected pass ≤0.6% per gate);
- no-cueing DOM + audio trace;
- gate reducer incl. timeouts and first-attempt-only;
- kill/resume; DB ladder; backup round trip;
- pack bad-hash, bad-signature, incompatible.

**Device** (test phone): sprite seek accuracy, tap-to-sound, cold start, meminfo, installed size, airplane-mode L1, Opus playback.

**Human:** G0 stopwatches; icons-only role test (10 Urdu-only adults + 10 children, sound off; wrong picks undone without reinstalling); sibling test (a 9-year-old gets 10 minutes on a 5-year-old's profile and must not change placement, skip a gate or open it without the shapes); parent-absent test; Track B screenshot audit ("is this for children?", 3 adults, week 4); blinded-text audio-only lesson one.

---

## 7. Global

- **Languages.** v1: English + Urdu UI. Wave 1: Hindi, Arabic, Spanish, Bengali. Wave 2: Portuguese, Indonesian, French, Swahili, Persian. The wave ranking is from memory; Play data confirms it (D8). **Stated limitation:** Punjabi and Pashto speakers get the Urdu UI in v1; a Punjabi (Shahmukhi) UI is a wave-1 candidate if the pilot shows need.
- **L1 notes.** `l1_tags` × family. Urdu notes come from the course, unchanged. The sound table and the human speaker are **General American** (D15).
- **RTL.** UI mirrors; English content never does.
- **Voice-first.** Instruction auto-play; icons tested sound-off; destructive actions PIN + hold.
- **Compliance.**
  - Play Families mixed audience: no ads/analytics SDK, no ad ID, no age.
  - COPPA (amended, 22 Apr 2026): no personal information; **no microphone in v1**.
  - GDPR-K / UK Children's Code: nothing off device; DPIA note.
  - Data Safety "No data collected", re-checked against the live form.
  - IARC Education. Closed test ≥12 testers × 14 days. AI-voice disclosure for Kokoro, plus the named human speaker.
- **Listing.**
  - Name: age-neutral (D17).
  - "Learn to read English from the first sound. Free, offline, any age."
  - Hooks: free; offline; children **and** adults; no English-reading helper needed; checks with made-up words; never resets.
  - Size line: download and installed size from §4.1, measured.
  - Banned: "proven", "guaranteed", "cures dyslexia", effect sizes, a Teach Your Monster "RCT", and "critical reading" (until v1.1 ships L6–L7).

---

## 8. Build plan (8 weeks + week 0; v1 = Levels 0–5)

**Who does what.**
- Kamal: decisions, pilot, Play Console.
- Speaker: remote recordings.
- GA reviewer.
- Build agent: a Claude Code session.
- Critics: fresh, one per lens.
- Judge: `listen_judge.py`, triage only.

| Week | Deliverables | Exit check |
|---|---|---|
| **0** | D0a/D0b confirmed; D24 phone bought; 3 speaker candidates sent the test file; GA reviewer and D16 fee agreed; Docker env started | decisions in decisions.tsv; dated device list |
| **1** | Parser coverage over 115 files + yield; misaki OOV count over 9,238 words; `ipa2misaki` table; Kokoro determinism test; sprite seek + tap-to-sound on the test phone; speaker chosen; L0–L1 text frozen | coverage report + yield committed; OOV count published; two-machine sha result; seek p95 measured; speaker booked |
| **2** | Repo from copied files; strict parser + `app:` PRs; decodability; `gen_pseudo` + foil generator; **recount settles §4.1**; recording sessions 1–3 (phonemes, demos, UI, L1 words) | `npm run content` exits 0 for L1–L2; recount committed; GA reviewer passes the phoneme set |
| **3** | Shell boots: launch doors, role, **night one (child A + adult A+B+C)**, PIN + shapes, DB ladder, backup round trip, sprite player; L1 human audio through QA; sessions 4–6 (L1 sentences, L2 words) | **G0**: ≤90 s and ≤15 min stopwatched on a non-reader; Q1 100%; backup test passes |
| **4** | E1–E12, E5, E6d, E22, E23, E4 write-from-memory, gate reducer, repair audio trace, Track A village layer, Listen & Talk; **critic round 3** (teacher, parent) on a recorded L1.02–L1.04 run; sessions 7–9 (L2 sentences, slow takes) | auto test set green; perfect-decoder and final-letter oracles behave as stated; Track B screenshot audit |
| **5** | L2 audio QA; L3–L4 Kokoro pack + review; placement (helper Stage 1/4, E6d Stage 3); helper sessions; progress panels; Urdu voice clips | scripted placement places the 5 archetype fixtures per file rules; sibling test passes |
| **6** | L5 sessions (E13, E16, E17, E19) + L5 pack; pack manager (ask each time, MB, signed manifest, reconcile, missing-pack screen) | L5 oracle complete; pack interrupt/bad signature tests pass |
| **7** | Perf on the test phone; a11y, comfort, RTL; blinded-text audit; PWA; signed APK; installed-size measurement | budgets met or gap list; sizes recorded in §4.1 |
| **8** | Gauntlet G0–G7; privacy, Data Safety, Families; listing EN/UR; internal testing; closed test; pilot starts | gate verdicts recorded; L1 offline on both phones |

**Cut list for weeks 3–5, in order** (drop the first item still unfinished when a week slips):
1. Placement Stage 1 and Stage 4 (helper-only parts).
2. Judge's card and `mastered` upgrades (helper sessions keep only WCPM marking).
3. E14 listen-and-follow.
4. Track B real-world unlockables.
5. Urdu Tier-2 glosses beyond L1–L2.
6. E22 limited to v/w and the short vowels.
7. The L5 pack moves to v1.1.

**Never cut:** night one, E5, E6d, E7, the gate, the Track A layer, Urdu instructions.

**Roadmap.**
- **v1.1:** L6–L7 with C11 checks and E18/E20; record and replay (E21); teacher mode; pack sharing; wave-1 languages; continuous-blend repair for L3.
- **v2:** CTC verifier (§5); ASR WCPM; FSRS; iOS.
- **v3:** prosody; tutor review queue; optional sync.

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation | Known by |
|---|---|---|---|---|
| E6d over-credits learners who don't really blend | Medium | High | Shared-onset 2×2 foils, first-attempt-only, delayed re-check, validity test (§12.2) | Pilot week 3 |
| Speaker booking, fee or remote quality | Medium | High | Week-0 booking; test file first; L1 recorded first | Week 1 |
| L0–L2 edits after recording | High | Medium | Freeze per level; pickup sessions | Ongoing |
| Learners dislike the Level 3 voice change | Medium | Medium | Announced handover; pilot; fallback human L3 | Pilot |
| Sprite seeking imprecise in WebView | Medium | Medium | Week-1 test; per-clip fallback | Week 1 |
| Kokoro OOV load (L3–L5) | Medium | Medium | Day-1 count; reviewed overrides | Week 1 |
| Parser yield <95% | Medium | High | `app:` YAML PRs | Week 1 |
| Course bars below 90% / L7.03 none | Certain | Medium | Course ticket D27 | Week 2 |
| 366 sittings to end of L4 discourages families | Medium | High | Track A layer; honest time; fast track for adults | Pilot |
| No listening in v1 (adults want feedback on speaking) | Medium | Medium | v1.1 record-replay; v2 verifier | Pilot |
| No test phone | Medium | High | D24 week 0 | Week 0 |
| Families review | Low | High | No mic, no data | Week 8 |

---

## 10. Decisions for Kamal

**W0** = before week 1.

| # | Decision | Default | Blocks |
|---|---|---|---|
| **D0a** | **Voice: human teacher for L0–L2, Kokoro af_heart from L3 (reverses "local model for all voices")** | Confirm. Alternative: Kokoro-only with recorded phonemes (round 1 + 2 audio critics: B) | **W0** |
| **D0b** | **Listening: no speech gate in v1; E6d tap gate; verifier in v2 (reverses research-03 v1 stack, research-04 D6)** | Confirm. Alternative: verifier on the v1 critical path (engineer: likely slip) | **W0** |
| D1/D2 | Stack; role not age | Decided | — |
| D4 | Teens → Track B | Yes | — |
| D7 | Leitner | −1 box, two wrong → box 1, sittings | — |
| D8 | Languages | EN + UR; wave 1 by Play data | — |
| D9 | Urdu voice (Sara licence or new speaker); per-language reviewers | Check Sara licence | week 3 |
| D10 | Donation link | None | — |
| D11 | Efficacy | Pilot + opt-in export | week 8 |
| D13 | Reminders | Opt-in, weekly, off for Track A | — |
| D14 | Teacher mode | v1.1 | — |
| D15 | Accent | General American (course table + speaker) | W0 |
| D16 | Speaker + fee for ~19–28 studio hours + pickups | Hire, remote GA female voice | **W0** |
| D17 | Name/icon | Age-neutral | week 7 |
| D18 | Mascot | New silent mascot "Pebble" (working name), Lottie | week 3 |
| D19 | Code licence | Open code licence, CC BY 4.0 content | week 2 |
| D21 | Pilot | 5 children + 5 Track B learners (§12.2) | week 6 |
| D23 | GA native reviewer (phonemes, pseudowords, 10% Kokoro samples, v2 gold-set labeller) | Paid freelance | **W0** |
| D24 | Test phone | Buy a 2–3 GB Android 10 | **W0** |
| D27 | Course ticket: bars <90% (L1.02, L5, L6), L7.03 no bar, missing blocks | Open ticket | week 2 |
| D28 | Adult PIN + child shape patterns | Yes | week 3 |
| D29 | Start at L1.02 (L1.01 embedded + repair) | Yes | W0 |
| D30 | v1 scope = L0–L5; L6–L7 in v1.1 | Yes | W0 |
| D31 | Only first attempts count toward gates | Yes | week 4 |
| D32 | Pack-manifest signing key custody | Kamal holds the key offline | week 6 |

Retired: D5, D6 (superseded by D0b), D22 (moves to v2), D25 (clone fallback removed), D26 (slow mode is human takes). D3, D12 and D20 are not used.

---

## 11. Content work to commission

| # | Item | Size | Owner | By |
|---|---|---|---|---|
| C1 | Print-concepts mini-module (left to right, word boundaries), opt-in from Me | ~3 short lessons | course author | week 5 |
| C2 | 720 generated pseudowords + native review | 720 + markdown's | build agent + GA reviewer | weeks 2–5 |
| C3 | Placement forms B, C | 2 | course author | week 5 |
| C4 | g/p alignment; `heartIdx` for 69 tricky words | lexicon | build agent + Kamal | week 2 |
| C5 | `pron.json` from the day-1 OOV count | count-driven | build agent + GA reviewer | weeks 1–5 |
| C6 | Mouth-cue images | 44 | generated + reviewed | week 4 |
| C7 | `app:` YAML (bars, reteach, error classes) | per yield report | build agent + author | weeks 2–4 |
| C8 | Track B real-world unlockables | ~2 per level L1–L4 | author | week 5 (cuttable) |
| C9 | UI script EN (~200) + UR (~300) | 500 | build agent + reviewer | weeks 2–4 |
| C10 | Urdu chunk glosses + Tier-2 glosses (L1–L4) | ~600 lines | author + Urdu reviewer | week 5 |
| C11 | L6–L7 MCQ anchors, partner scripts, model answers, keys | ~30 sessions | author | v1.1 |
| C12 | Village art (one item per GPC), Pebble rig, Listen & Talk pictures | ~70 items + rig + ~200 | art | weeks 3–4 |
| C13 | Recording scripts per session (frozen text) | per level | build agent | weeks 1–4 |
| C14 | E6d foil sets, reviewed for rude or confusable words | per generator | build agent + reviewer | week 2 |
| C15 | Course ticket (D27) incl. L7.03 bar | 1 | build agent | week 2 |

---

## 12. How we will know it works

### 12.1 Metrics without telemetry

All on the device; exported only by the user's choice.
- **Decoding:** checked / checked twice / mastered shares; first-attempt E6d accuracy; pseudoword accuracy.
- **Comprehension.**
- **Fluency:** pace or WCPM.
- **Persistence:** days practised, sittings per week, returns after a gap.
- **Friction:** still-learning gates, failed re-checks, timeouts.

### 12.2 Pilot (from week 8, 6 weeks)

- **Recruitment:** 5 children (Track A, including Kamal's two; at least two with a parent who doesn't read English) and 5 Track B learners (1 teen, 4 adults: a shop worker, a grandparent, an Urdu-literate adult, and one adult who cannot read Urdu).
- **Proxy validity (the key test).** For each learner, after L1.04 and again after L1.08, a blind GA-speaking teacher hears them read aloud the same items they answered by E6d. Target: ≥90% agreement between E6d first-attempt credit and the teacher's judgement. If agreement is lower, the gate design is revisited before any production release.
- **Pre/post:** placement form A, then form B, with a level check judged by someone other than the helper.
- **Weekly:** check-ins, the Urdu Listen & Talk questions, the voice-change question at L3 (for anyone who reaches it).
- **v1.1 production bar:**
  - every child advances ≥1 placement step with no helper;
  - proxy agreement ≥90%;
  - ≥7/10 still practising in week 6;
  - zero "childish" reports from Track B;
  - zero frozen screens;
  - zero cueing incidents.
- Public copy may say only "piloted with N learners".

### 12.3 Gauntlet gates

**Method.** Fresh critics who did not build the app, plus named humans. Material anonymised, scored in both orders. A win = higher total in both orders, no rubric row worse by more than one point. G0 and G7 are pass/fail.

| Gate | vs | Test / rubric | When |
|---|---|---|---|
| **G0 Night one** | stopwatch | child: first sound tapped ≤90 s; adult: real word read ≤15 min; no questions; no mic dialog; relaunch to lesson ≤10 s | weeks 3 and 8 |
| G1 Child first week | Duolingo ABC | explicit sounds; learner-led blending; no adult needed; delight; kindness of errors | week 8 |
| G2 Interaction | **Teach Your Monster** | play-loop delight (village, stickers); resistance to guessing (oracle results shown); repair quality | week 8 |
| G3 Parent view | Khan Kids | where the child is; labels honest; sibling-proof; size honesty | week 8 |
| G4 Adult dignity | Learning Upgrade | first word on night one; nothing child-coded ("tricky words", no avatars); privacy; PIN flow | week 8 |
| G5 Audio | Sara (reference) | human L0–L2 clarity, warmth, one-teacher consistency, loudness spread; Level 3 handover acceptance by 5 parents and 3 adults | weeks 3 and 8 |
| G6 Proxy validity | blind teacher | E6d vs read-aloud agreement ≥90% (§12.2), plus the oracle results | pilot week 3 |
| G7 Rule audit | DESIGN.md §2 | every §2.3 row pass/fail | week 8 + every release |

A lost gate turns its top two findings into the next week's first tasks, and the gate re-runs.

---

## Appendix: sources

**This folder** (`/home/oye/Documents/free_work/personal-agent-v2/vault/research/read-english-app/`): RESUME.md, decisions.tsv, research-01…05, plan-v1/v2.md, v2-changes.md, critics-round-1-*.md, critics-round-2-*.md, bar/*.json.

**Course**: `/home/oye/Documents/free_work/english-reading-course/`: DESIGN.md; course/level-0/placement-test.md (Stages 0–4, self-test version, HT 2017 table, DIBELS rules); course/level-1…7/lessons (108) + mastery-check.md (7); tools/decodable.py; LICENSE.

**Urdu app**: `/home/oye/Documents/free_work/urdu-reading-course/mobile/src/` (content.js single-Audio player + watchdog, db.js, backup.js, path.js, learner.js), mobile/tools/, scripts/listen_judge.py, voice_studio.py, store/PLAY_CONSOLE_CHECKLIST.md.

**Canvas plan**: `/home/oye/Documents/free_work/personal-agent-v2/vault/research/english-canvas-tutor/v6-changes.md`.

**External URLs**: as listed in research-01 to research-04 and plan-v1's appendix (unchanged).

---

## Addendum — Round 3 verdicts and the v4 changes still to make (2026-10-05)

Gauntlet status after three rounds: **not yet won.** Teacher: A for both learners (first time). Parent: shopkeeper A, mother B. Engineer: B. Audio: B (narrow). Auditor: round 3 pending. Full reports: `critics-round-3-*.md`; decision log: `decisions.tsv`.

Lead decisions adopted for v4 (not yet written into the sections above):

| # | Change | Why (critic) |
|---|---|---|
| 6 | From Level 3 the two voices are two named characters: **Sound Teacher** (human) and **Reader** (Kokoro). Repair at L3+ = human sounds only → learner blends → Kokoro word only as confirmation after the second attempt. A tapped word always plays its own lexicon voice. Loudness judged before padding; the −1.5 dBTP limiter is the hard cap; plan recording at 150 clips/hour; recording spec adds stop-without-schwa direction, pop filter, noise floor, input level, retake rule; rater agreement = weighted kappa/ICC, second listener not Kamal. | Audio r3: L3 repair mixed voices in one exercise. |
| 7 | Track A gets a child quick-start placement (5 tap-gate items in sitting 1; pass → skip ahead), a **Stories** tab (human read-to-me of the Listen & Talk passages with pictures, tap-read decodable readers, a sound chant), the Check reframed as "show what you know" explained in Urdu, a miss → targeted repair + re-check next sitting (never sent back a sitting), and a mother's view that says which 3 sounds to ask tonight, with audio. PIN exists only once an adult profile exists; reset via the arithmetic gate. "Tricky words" → "words to remember" in Track B. | Parent r3: one sound a day with nothing to hand over; 8-year-old forced to trace s; first Check = second quit. |
| 8 | Audio engine = fetch sprite → `decodeAudioData` once → `AudioBufferSourceNode.start(when, offset, dur)` on the audio clock (the Urdu `Audio()` player never seeks and Capacitor's local server ignores Range requests). Schedule becomes 10 weeks with week 9 as slack; speaker audition and the phoneme session move to week 1. v1 machine-gated content = Levels 0–4; Level 5 ships as practice until MCQ checks are authored (course ticket). Fix backup.js field drops, service-worker pack caching, the ≤150 ms vs 350 ms gap contradiction, the `at/it/ap` foil. | Engineer r3. |
| 9 | Tap-gate foils: one foil differs only in the onset, one only in the vowel, one only in the final sound (an onset-blind oracle must fail the gate); E5 "I said it" stays self-report in v1 and is labelled so; gate bars follow the lesson's own bar (course issue #1 to raise them to 90%). | Teacher r3. |

Course issues filed: oyekamal/english-reading-course #1 (bars < 90%), #2 (pseudoword real-word filter), #3 (machine-readable lesson structure).
| 10 | Auditor r3 (NO, ~1 hour of fixes): recording rate 150/h and one hours figure; Urdu voice ~900 lines; blending demos 26; foil-word count derived (≥720 for L1–L2 checks alone); Kokoro L3–L5 clips 4.7k–7.3k and pack MB recomputed from the stated KB/clip; chance maths restated per real check composition (L1.02 9/11 ≈ 6%); foil rule worded once; night one for an adult = L1.02 A+B+C is ~35 min in the course, so night one is Sittings A+B (/s/, /a/, blend "sa") and "sat" lands on night two — or the course fast-track is explicitly compressed and said so; pilot length vs L1.08 reach recomputed; D15: the course names no accent (accepts /ɒ/ or /ɑ/) — General American is the app's choice, not the course's. | Auditor r3. |

Next session: write plan-v4 from this table, then critic round 4 (same five personas). Resume from `RESUME.md`.
