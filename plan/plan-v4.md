# Sound Out: the app plan, v4

Date: 2026-10-06. Owner: Kamal. Repo: `oyekamal/sound-out` (`/home/oye/Documents/free_work/sound-out`).
- **App**: Sound Out. Play title "Sound Out: Read English". Package `com.oyekamal.soundout` (see `store/NAME-ASO.md`).
- **What v4 is**: plan-v3 plus its addendum (rows 6–10) plus every critic-round-3 defect. `v4-changes.md` maps each one.
- **Evidence**: `plan/research/`, `english-reading-course` (DESIGN.md, 108 lessons, `course/level-0/placement-test.md`), `plan/bar/*.json`, `plan/critics/`.
- **Labels**: "unverified" = the source said so. "estimate" = this plan's number. "budget" = a target, not a measurement. "assumed" = an input chosen by us.

---

## 0. Summary, two decisions to confirm, and the bar

**Summary.** Sound Out is a free, offline Android app (plus a PWA) that teaches anyone to read English from the first sound.

**v1 scope**
- Machine-gated lessons for Levels 0–4.
- Level 5 ships as **practice** until its multiple-choice checks are written (content ticket). Levels 6–7 come in v1.1.
- It reuses the Urdu Qaida shell: Capacitor 7, Vite, IndexedDB, Leitner, pearl path, feel.js.

**Night one**
- A child taps "A child" and is inside a game world with Pebble the mascot. She hears and taps her first letter sound within 90 seconds.
- An adult taps "Me". If his quick checks go well, he reads the word "sat" within about 15 minutes, in private.

**How progress is checked**
- **The tap gate.** The learner reads a printed word to herself, then taps which of four spoken words it says. Each of the three wrong options changes exactly one sound. So no adult who reads English is needed.
- A helper who listens can upgrade a lesson to "mastered". This is optional.

**What v1 does not have**: no accounts, no ads, no analytics, no microphone.

### Decision D0a: voice (reverses "local model for all voices" for Levels 0–2)

**The proposal: two named voices.**
- **Levels 0–2: one human General American female voice, called the Sound Teacher.** She records everything:
  - the 44 phonemes and the blending demos;
  - every word, made-up word and answer option;
  - every sentence, in both tracks;
  - the English UI prompts and the slow takes.
- **From Level 3:**
  - **the Reader** (Kokoro-82M `af_heart`, rendered on Kamal's laptop) speaks the new words and sentences;
  - **the Sound Teacher** keeps the isolated sounds.
- The app introduces the Reader once, at the start of Level 3.
- Inside one exercise, the voices never alternate on the same word (§4.4 voice table).

**The evidence.**
- research-02 §5: a Gemini judge correctly identified Kokoro's /m/ and /p/, but not /s/, /ʃ/, /θ/ or /æ/. No human has listened yet.
- The audio critic (round 2) measured Kokoro's isolated /s/: its energy centres at 513 Hz, which is a rumble, not a hiss.
- No text-to-speech produces a clean isolated stop like /p/.
- Audio critics in rounds 1 and 2 both rejected a human /s/ /æ/ /t/ followed by a Kokoro "sat".

**The alternative.** Kokoro speaks every word, and only the phonemes are recorded. This is the v1/v2 design; it lost both rounds (verdict B both times).

**The cost.**
- About 33–50 studio hours of a paid speaker (§4.5).
- Level 0–2 text must be frozen before recording. Any later text change needs a pickup session.

### Decision D0b: listening (reverses research-03's v1 stack and research-04's D6)

**The proposal.** v1 has no speech gate and asks for no microphone permission.

**The evidence.**
- Engineer, round 2: sherpa-onnx keyword spotting and hotword biasing cannot return the three answers the design needs (yes / unsure / no). Proper scoring of the target against likely mistakes is a 10–15-day CTC project.
- Teacher and auditor, round 2: research-03 §8 set a 60% recall *target* for its test protocol. At that recall, a correct reader passes a 10/11 gate only about 3% of the time.

**The roadmap.**
- **v1.1**: record and replay, self-compare only, labelled practice.
- **v1.1 verifier candidate: Whistle** with keyword biasing (research-06; child and accented speech unverified). A CTC verifier is the v2 fallback (§5).

**The alternative.** Put the verifier on the v1 critical path. The engineer judged that this makes the ship date slip.

### The bar

Features: Duolingo ABC and Khan Academy Kids. Child experience: **Teach Your Monster** (§3.4). Pedagogy: DESIGN.md. Audio reference: the ElevenLabs Sara clips. Also compared: Google Read Along and Learning Upgrade.

| Sound Out v1 | Duolingo ABC | Khan Kids | Google Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes | Free, no ads; parent account with email (Common Sense, via a round-1 critic fetch) | Yes | No: iOS $8.99 | No: $4.99/mo–$59.99/yr |
| Offline | listing: "Offline Learning" | partial | after download | not documented | no evidence |
| Adult track, same sequence | No | No | No | No (listing: ages 3–6) | Yes, songs/video, 3.2/5 |
| Placement | No ("No option to skip ahead") | path "tailored to their age and previous performance" (Common Sense, via parent critic r3) | No | not found | not found |
| Gate on real and made-up words, one-sound-change options | not found | not found | not found | not found; one justuseapp review: "children can progress by guessing" | not found |
| Depth | "stops at simple stories" (research-01) | to about grade 2–3 | story practice | phases 2–5 | partial |
| Urdu support for the English code | No | Spanish read-to-me | Urdu stories, no code teaching | No | a few onboarding languages |

"Not found" means absent from research-01 and the listings, not proven absent. Duolingo ABC's listing says "over 700 lessons"; Common Sense counted 127 units. Both are reported as found.

Store data (US iOS, MiB): Khan 4.80 on 131,337 ratings, 201 MiB. Duolingo ABC 4.25 on 3,810, 212 MiB. Teach Your Monster 4.47 on 29,802, 96 MiB. `bar/Read_Along_Kids_Books.json` is a different product.

Sound Out's own sizes are in §4.1, in MB, given as both download and installed size.

---

## 1. Who it is for, and the promise

**Promise:** "Ten minutes most days. Starts at the first sound. Offline, free, knows nothing about you, never makes you start over, and no one who reads English has to help."

**How long it takes** (estimate; the week-2 lint replaces it):

| | From L1.02 to the end of L4 (61 lessons) | At 1 sitting a day | At 5 a week |
|---|---|---|---|
| Child, Track A, ~6 sittings/lesson | ~366 sittings | ~12 months | ~17 months |
| Adult, Track B, ~3 sittings/lesson | ~183 | ~6 months | ~8.5 months |
| Adult fast track, ~1.5–2 sittings/lesson | ~92–122 | 3–4 months | 4–5.5 months |

**Two age paths, only through placement.** Track A has no age setting; an 8-year-old starts later only by passing quick-start.

**Dropout.** Expected; countered by the Track A world, Stories and the mother's view; the pilot counts it.

### 1.1 Five archetypes, night one

| | Ayesha, 5 (Urdu home; mother doesn't read English) | Her brother Hamza, 8 (knows A–Z) | Bilal, 14 | Rukhsana, 35 (stall worker) | Nana Karim, 60 |
|---|---|---|---|---|---|
| First screen | "A child" | added as a second child | "Me" | "Me" | "Me" |
| Night one | Quick-start: misses 2 items, stops after ~25 s. Then Sitting A: /s/ tapped at ~1:10, trace, write s from memory, the sun rises in the village, sticker. ~8 min | Quick-start 5/5 → tap ladder (Stage 3) → placed at **L2.03**. Starts with th, not s | Fast track A+B+C: reads **sat, at, as**, spells "sat". Sets his PIN at the end | Same as Bilal; Urdu instructions; large text offered | Same; next night runs placement from his PIN settings → **L2.01** |
| Exit check | first sound tapped ≤90 s | placed above L1 in sitting 1 | first word read ≤~15 min (§3.5) | same | same |

### 1.2 First month (illustrative)

- **Ayesha**: L1.02–L1.06, about 30 sittings. Her village has 10 pieces. Each night her mother sees "ask her these 3 sounds" with audio.
- **Hamza**: L2.03–L2.06.
- **Bilal**: L1.02–L1.12 on the fast track.
- **Rukhsana**: L1.02–L1.06.
- **Nana**: L2.01–L2.07.

---

## 2. The pedagogical engine

### 2.1 The course mapped to the app

Counts are from greps over the 108 lesson files, which the round-3 auditor reproduced.

| Level | Lessons | Template | Notes | In v1 |
|---|---|---|---|---|
| 1 | 14 | lesson | Blend in 13, Listen & Talk 14, Track B 12 | **gated** |
| 2 | 14 | lesson | Listen & Talk 13, Track B 13 | **gated** |
| 3 | 18 | lesson | Listen & Talk 17, Track B 17 | **gated** |
| 4 | 16 | lesson | Blend 14, Listen & Talk 15, Track B 15; L4.15 is a real-world protocol with no made-up words | **gated** |
| 5 | 16 | session | Free-response checks (e.g. L5.03), "4/6 = pass" formats, L5.16 has no bar | **practice only** until MCQ checks are written (C11) |
| 6–7 | 30 | session | No Track B; most L7 lessons have no bar (only L7.07 has "4 of 6") | v1.1 |

**Where the order lives.** The lesson order and the 69 heart words (L1 24, L2 29, L3 16) are stored in `data/gpc.json` and `data/heart.json`.

**What heart words are called on screen:**
- Track A: "tricky words".
- Track B: "**words to remember**". This avoids child-coded words for adults (G4).

### 2.2 Strands

- **Code** (L1–L4): Hear, Meet, Blend, Spell, Tricky words, Check.
- **Read it**: Track A or Track B text, then 2 literal questions and 1 "think" question.
- **Listen & Talk** (§3.8).
- **Review**: the warm-up.
- **Fluency practice**: from L2.
- **Morphology**: L4, plus L5 practice.

### 2.3 Every rule, enforced

| Rule | How the app does it | How we check it |
|---|---|---|
| 1. No cueing | No image beside an unread word. A repair never plays the whole target word before the learner's second attempt. Tapping a word plays its sounds first; the whole word only after an attempt | DOM test. Audio-trace test: no clip containing the whole target word (stretched takes included) between a wrong answer and the next attempt |
| 2. Decodable texts (L1–L4) | Only taught letter-sounds, scheduled tricky words, and at most 2 flagged story words | `decodable.py` run on the JSON |
| 3. Blend before segment; spell after blend | Each sitting's step list puts blend before spell. A single-sound sitting has no word spelling | Snapshot test on the real L1.02–L1.12 JSON |
| 4. Mastery gate | Each check uses **its own lesson's bar**, applied to judged items. The default is 0.9. Real and made-up words are scored separately at level checks. Bars under 90% are raised with the course in **english-reading-course issue #1** | Reachable-score test per lesson; a below-bar oracle run per lesson |
| 5. Tricky words: map, don't flash | E8 map. Words of 1–2 letters (a, I, is, to) are checked by E8 + dictation, never by the tap gate | Lint: all 69 words have `heartIdx` |
| 6. Two registers | `read.B` or `sameAsA` in every L1–L5 lesson | Parser plus a lint for child-coded words |
| 7. Comprehension every day | Listen & Talk, with English questions (§3.8) | Coverage report |
| 8. Two metrics | No blended score anywhere. L5 shows "pace", never words-correct-per-minute | Schema check + UI grep |
| 9. L1 notes | `l1_tags`; Urdu notes come unchanged from the course | Tag lint |
| 10. Pause-safe, no streaks | Days practised only goes up. A checkpoint on every screen. Skip and placement sit behind the grown-up gate | Kill/resume ×20 |
| 11. Multisensory optional | Tracing on by default for Track A and Track B Level 1, with a skip button | Settings test |
| Machine never promotes **mastery** | A tap-judged gate unlocks the next lesson as "checked by tapping". "Mastered" needs a helper. **Departs from research-03 §6** (adult confirms every gate). Reason: a home with no English reader would otherwise never progress | Gate-reducer tests |
| Audio stays on the phone | v1 has no microphone at all | Manifest has no `RECORD_AUDIO` |

---

## 3. Product

### 3.1 First launch, profiles, gates

**First launch.**
- On a fresh install the app shows **one screen**: "Who is reading?", with two cards, spoken in Urdu then English.
- If the parent picks "A child" and no adult exists, the next screen is the lesson. No other screens come first.

**When the "doors" launch screen appears.** Only when there are two or more profiles, or an adult profile:
- a large **Children** door that opens the child tiles;
- a **Me** door with a person icon. It shows a lock only once a PIN exists.

**Adult PIN.**
- It exists **only once an adult profile exists**.
- It is set at the end of the adult's first night (one "Later" allowed).
- An adult-only phone opens straight into the lessons. An optional switch asks for the PIN on every open.

**Children-only phone.** The grown-up gate is an **arithmetic gate**: a written sum such as "7 + 8" answered with digits. It protects:
- placement and "I already know this";
- pack downloads on mobile data;
- resetting a child's shape pattern;
- delete and restore.

**Forgotten PIN.** Answer the arithmetic gate, then wait **24 hours**. The reset completes the next time the app opens after 24 h. Lessons stay usable meanwhile, except when "ask PIN every time" is on: in that case the adult's lessons open after the arithmetic gate during the wait.

**Child shape pattern.**
- Each child profile has a pattern of **4 shapes from a grid of 9** (3,024 orderings), set by the grown-up.
- **3 wrong tries lock it for 30 s.**
- **10 minutes idle → back to the doors**, so a sibling can't keep playing in an open profile.

**Wrong role.** "Change who is reading" sits behind the grown-up gate.

**No microphone permission in v1.**

**Tabs.**
- Track A: Path · **Stories** · Practice · Me.
- Track B: Lessons · Read · Practice · Progress.

Every screen plays its instruction once on entry (Track A, and Track B L1–2). "Hear it again" is always available.

### 3.2 The sitting model

**Budgets**
- **Track A ≤8 min.** The lint sums the audio durations and multiplies by **1.5 for child response time**. Before the text is frozen in week 2, 5 children are stopwatched on Sittings B and C; p90 must be ≤8 min.
- **Track B**: 10–15 min.

**Pace**
- One new letter-sound per sitting in L1–L4.
- Pattern lessons get at most 5 new words per sitting. L2.06's 21 initial blends become 5 sittings: s-blends twice, l-blends once, r-blends twice, with tw in the last.
- **Track A L1.02:**
  - A: /s/ (hear, meet, trace, write from memory, sound game).
  - B: /a/ (warm-up ≤3 cards, hear, meet, trace, blend "sa", spell "sa").
  - C: /t/ (warm-up, hear, meet, trace, blend 4 words, spell "at").
  - D: warm-up, blend, tricky words *a, I*, spell "sat".
  - E: Read it.
  - F: Listen & Talk.
  - G: Show what you know.
- **Track B** merges these into about 3 sittings. On the fast track, after a ≥90% mini check, "Keep going?" continues to the next course sitting. It is offered, never a test.

### 3.3 Exercises

**v1 exercises**
- E1: sound game (spoken words, no pictures).
- E2: Meet card (letter, Sound Teacher's sound, mouth picture, Urdu tip).
- E3: sound tap.
- E4: trace → write from memory (§3.9).
- E5: blend it (below).
- E6d: the tap gate (below).
- E7: spell with tiles (Track A) or keyboard + tiles (Track B).
- E8: tricky-word map.
- E9: reader + questions.
- E10: Listen & Talk.
- E11: Show what you know (the check).
- E12: Leitner card.
- E13: morphology (L4, L5 practice).
- E14: listen and follow.
- E15: "pace" (helper-marked WCPM inside helper sessions only).
- E16/E17: L5 practice reader.
- E19: L5 writing practice with a model answer.
- E22: ear training (minimal pairs).
- E23: b/d from L1.09, b/d/p/q from L1.12, formation anchors first.

**v1.1**: E18 reciprocal teaching, E20 lateral reading, E21 record and replay.

**E5, Blend it.**
1. **First item of a new pattern only.** The Sound Teacher models the blend once, under a highlighter that grows letter by letter.
2. **Sound by sound.** The learner says each sound **before** tapping its letter. The tap then plays the sound as confirmation.
3. **Whole word.** She slides a finger under the word and says it, then taps "**I said it**". On screen this is labelled **self-report: the app does not hear you**.
4. **The judged step.** The same word goes straight into an E6d pick *before* the word is played.
5. **Repair (L1–L2): successive blending.** The Sound Teacher's partial clip plays ("sssaaa"); the learner adds the last sound; a second E6d pick follows. Rule 1 holds: the stretched partial never contains the whole word.
6. **Repair (L3+).** The Sound Teacher's sounds play one at a time with the **single 350 ms gap**. The learner blends. The Reader's whole word plays **only as confirmation after the second attempt**.

**E6d, the tap gate. Its rule, stated once:**
- **Each item has three options that are not the answer. Each differs from it in exactly one position:**
  - one in the **first sound only** (for example s→p, or b↔d / p↔q where taught);
  - one in the **vowel only**;
  - one in the **final sound only**.
- Example, *sat*: **pat / sit / sad**. A learner who cannot read the first letter still has two options left, so a gate cannot be passed onset-blind.

**Option rules**
- Real-word items use real-word options; made-up-word items use made-up options. **They never mix.**
- **Two-sound words** (at, as) get three options under the same rule:
  - one first-sound-only (*it*);
  - two final-sound-only (*an*, *am*).
  - This replaces v3's *at/it/ap*: "ap" is not a word, and the set broke the rule.
- **Multi-syllable words (L3–L4)**: one option changes only the first sound, one only the lesson's target vowel pattern, one only the ending.
- **No word appears twice in one check.**
- Tricky words of 1–2 letters are never used in E6d.

**Flow**
1. The printed word appears alone. A spoken line in the UI language says "read it to yourself".
2. The four option buttons appear. The answer window is **12 s for L1–L2 and 8 s from L3**.
3. **A timeout is "not judged".** A check needs at least as many judged items as the bar's denominator, so it re-asks with a fresh item. With more than 2 timeouts the screen says "let's finish this tomorrow", not "passed".
4. **First wrong answer:** a targeted repair based on which option was picked:
   - first-sound option → replay the first sound and its letter;
   - vowel option → the paired E22 ear item first (below), then the vowel with its mouth cue;
   - final-sound option → replay the last sound.
   - Then the same item is asked again with the options reshuffled.
5. **Second wrong answer:** the item goes to review. Only now does the whole word play.
6. **Only first attempts count** toward the gate.

**Ear or eye.**
- When a vowel option is picked, the paired E22 pair plays (sat/sit by ear). If she fails the ear item, the miss is logged as **ear** (hearing practice) and is **not counted** as a reading miss.
- A vowel contrast is used in gate options only after **5 Urdu-only listeners** (not the speaker) pass that minimal-pair set at ≥90% (week 5). Otherwise the option uses a different vowel.

**What E6d proves.** It is a decoding proxy: from print to recognising the spoken word. It is not oral reading.

**Chance of passing without real reading** (worked per real check):

| Learner | L1.03–L1.13 check (5 real + 5 made-up E6d, 1 dictation; bar 10/11) | L1.02 check (3 real + 5 made-up E6d, 3 dictation; bar 9/11) |
|---|---|---|
| Can't read the first letter, reads the rest (p = ½ per item) | dictation right → needs ≥9/10: **1.1%**; dictation wrong → needs 10/10: 0.1% | 3/3 dictation → needs ≥6/8: 14.5%; 2/3 → needs ≥7/8: 3.5% |
| Reads one position only (p = ⅓) | 0.04% | ≤2% |
| Genuine 90% reader | passes first try ~70% | — |
| Genuine 80% reader | ~32% | — |

- **L1.02 is the weak spot**, because only three letters are known. It gets the delayed re-check, and L1.03's check covers s, a and t again. A miss is never a dead end (§3.6).

### 3.4 The Track A world (the Teach Your Monster bar)

- **Pebble**, a new mascot (not Marko), animated as a silent Lottie. It waves, cheers and points; only the Sound Teacher speaks.
- **The village.** Each sound met adds a piece: the sun for s, an apple tree for a, a tent for t. A piece appears only after its sound is learned.
- **Rewards are never withheld:**
  - every finished sitting earns a sticker and a celebration;
  - every new sound adds a village piece;
  - a passed check adds a pearl on the path.
- **What Ayesha does alone in Sitting A:**
  - 0:00 Pebble waves; an Urdu line, then "Let's meet a sound!"
  - 0:20 E1: tap the word that starts with /s/ (×4).
  - 0:60 E2: the s and its sound; tap it.
  - 2:00 Trace ×3, then write from memory.
  - 4:00 Pop the s-bubbles (×6).
  - 6:00 The sun rises over the village.
  - 7:00 Sticker.
  - 7:30 "Show your grown-up": she says /s/.
- **Stories tab** (the read-to-me bar):
  - the Sound Teacher **reads the Listen & Talk passages aloud with pictures**, already recorded;
  - **tap-read decodable readers**: tapping a word plays its sounds; the whole word plays only after the learner's attempt;
  - a **sound chant**: every learned letter lights up as its sound plays, built from the phoneme clips on the audio clock, with no new recording.

### 3.5 Night one and placement

**Child night one**
1. **Quick-start placement**: 5 tap-gate items across Levels 1–2.
   - It stops after 2 misses, about 25 s for a non-reader, and shows no wrong-answer feedback.
   - **5/5 continues straight into the Stage 3 tap ladder** (about 5 min), with no gate needed, and places the child.
   - Otherwise Sitting A starts.
2. **Exit check**: first sound tapped ≤90 s.

**Adult night one** (D35)
- **Choice made:** the **course's own fast track, compressed and said so.**
  - The course allots about 35 minutes to Sittings A–C of L1.02, tutor-led with paper.
  - The app runs them as taps and tiles, targeting about 15 minutes.
  - It moves on to B and C only through "Keep going?" after a ≥90% mini check.
- **Why this option.** The shopkeeper's A verdict in round 3 rests on reading a word on night one, and the course allows merging sittings after a passed mini check.
- **Fallback (an alternative, not a fix).**
  - Trigger: if the week-3 stopwatch shows more than 20 min for 3 of 5 adults.
  - Night one becomes Sittings A+B (/s/, /a/, the blend "sa"). "sat" moves to night two.
  - The promise becomes "your first word on night two".
- **Exit check**: a real word read via E6d within about 15 min of first launch.

**The L1.01 order (D29).** The app starts at L1.02. L1.01's oral games become the Hear-it items. The full L1.01 runs as a repair.

**Grown-up placement** ("I can already read some English", behind the gate) follows `placement-test.md`:

| Stage | What the course says | What the app does |
|---|---|---|
| Stage 0 | spoken intake questions | Not asked aloud. Q1 = the button. Q3 = the UI language. Q2 is one optional silent card. Q4 moves to the screener |
| Stage 1 | Oral sound-play items with **made-up-word answers** ("ig", "ap"), Correct and Automatic (2 s) | **Helper-judged in a helper session** (right and quick / right but slow / not right). **With no helper it is skipped** (the course's self-test allows this) and placement goes to Stage 2. Never machine-judged |
| Stage 2 | letter-sound blocks | Hearing version (E3), labelled as such |
| Stage 3 | tiers of 8 real + 8 made-up words | E6d tiers. The course pass mark is "90% (14+)"; note **14/16 = 87.5%**, flagged in the course ticket. Placement = the first tier below it; Tier 1 below → L1.02 |
| Stage 4 | timed passage | Only if Tier 3+ is cleared, and only in a helper session (Hasbrouck–Tindal Fall 50th: G2 50, G4 94, G6 132 WCPM). Placement above L4 lands in Level 5 practice |

The course's tester script applies only to helper-run stages; the app says "tap what it says".

### 3.6 Checks, bars and states

**The Check.** It is called "**Show what you know**". Before the first one, an Urdu audio line explains: "Some are made-up words, to show you can sound out any word. Just sound them out."

**Bars, as the course states them.**
- L1.02: 9/11 (82%).
- L1.03–L1.13: 10/11.
- ≥4/5 appears 19 times in 10 Level 1 lessons, mostly mini checks.
- L3: "≥90%".
- L5: 5/8 or 6/9; L5.16 has none. L6 "4/5". Most of L7 has none.

The app applies each lesson's own bar to judged first attempts, defaulting to 0.9. Issue #1 asks the course to raise bars under 90%.

**L1.02's check** has 3 real words (at, as, sat), 5 made-up words and 3 dictated words. There are no repeats. s, a and t allow no fresh sets.

| State | When | Then |
|---|---|---|
| `checked` | bar met | **next lesson unlocks**; "Checked by tapping"; delayed re-check 3 sittings later |
| `rechecked` | delayed re-check passed | "Checked twice" |
| miss | bar not met | **targeted repair of the missed items' errors inside the next sitting, then a re-check (fresh items where they exist)**. Never sent back a sitting |
| `still_learning` | second miss on the same re-check | the next lesson unlocks **with its new-sound sittings intact**; the missed items stay in daily review; the parent view shows "**Needs a person**" with a spoken Urdu explanation. Never a lock |
| `mastered` | a helper hears the learner read | optional upgrade |

### 3.7 Review

- 5 Leitner boxes, scheduled in sittings (1, 2, 4, 8, 16). A wrong answer moves a card down one box; two wrong in a row → box 1.
- Warm-up holds ≤3 cards in Track A and ≤6 in Track B.

### 3.8 Listen & Talk (L1–L4)

**Order**
1. A one-line Urdu gloss gives the context. It is authored so it **never contains the answer**, and is reviewed for leakage.
2. The English passage plays (Sound Teacher, or the Reader from L3), with a picture **after** each chunk.
3. **Comprehension questions about the English passage**, spoken in English with picture answers and an Urdu instruction line.
4. The Tier-2 word, then its Urdu gloss.
5. "Talk" is a prompt card, shown only in helper sessions.

**Pilot**
- Target ≥80% on the English questions.
- An A/B test of picture-before versus picture-after.
- A test that the gloss is faded after the first two weeks.

### 3.9 Writing

- **E4.** Three traces, then the guide fades to a start dot: write from memory. Each stroke is scored on:
  - start position, with tolerance 20% of letter height (Track A) or 12% (Track B);
  - number of strokes, their order and direction;
  - checkpoints passed in order;
  - end position.
- **b/d/p/q** are also checked for which side the bowl is on and whether the stem comes first.
- Formative only; misses go to error classes.
- E7 spelling follows blending.

### 3.10 Helper sessions (optional)

Opened by PIN or the arithmetic gate. A helper session gives access to:
- read-aloud "Got it / Not yet" buttons;
- placement Stages 1 and 4;
- WCPM marking;
- the judge's card.

The "mastered" label needs the 5-example classification. Children progress fully without a helper.

### 3.11 Progress and the mother's view

**The mother's view**, in Urdu audio and icons, for each child:
- "**Tonight, ask her these 3 sounds**": three big letters, each with the Sound Teacher's sound button, picked from that day's sitting and the weakest review cards;
- her latest "Show what you know" result as pictures (checked / try again tomorrow / needs a person);
- the village.

**The grown-up page** shows decoding (made-up and real words per level), comprehension, L5 "pace", and flags. There is no blended score.

**Track B**: "words you can read now".

**Everything else**
- No streaks. Reminders are opt-in, at most weekly, and off for Track A unless turned on.
- Comfort settings: size, spacing, tints, OpenDyslexic, reduced motion.
- Slow mode uses the Sound Teacher's slow takes (L1–L2 only).

### 3.12 Screens

All screens named in §3.1–3.11, plus: Level 3 "the Reader joins you", pack download (MB + minutes), missing pack, comfort.

---

## 4. Voice

### 4.1 Clip counts and sizes

**Sizes, KB per clip at 24 kbps Opus with padding (one table for both voices):**
- word, made-up word or option: **3.0 KB** (round-2 audio critic measured a Kokoro "sat" at 2.8 KB; research-02's 1.77 KB was a trimmed average);
- sentence or Tier-2 line: **12.5 KB**;
- slow take: 5 KB; phoneme: 2.5 KB; demo: 8 KB; Urdu line: 6 KB.

**Count ranges**
- Words: research-05's per-level count is the low end; the high end is ×1.6. Note that 9,238 is research-05's ceiling "if every word in tutor prose is voiced".
- Sentences: research-05's count ±25%.

**Option-word derivation**
- One check has 10 tap items × 3 options.
- L1–L2: 24 checks × 30 × 3 sets = 2,160. Plus level checks 2 × 20 × 3 × 3 = 360. Plus placement tiers 1–2: 16 × 3 × 3 forms × 2 = 288. Plus L1.02's 24. Total **2,832 option slots**.
- The floor is 720 (one set of L1–L2 check options, auditor). **Plan for 900–1,800 distinct new clips.** The generator settles the number in week 2.
- L3–L4: 31 checks (L4.15 and L4.16 excluded) × 30 × 3 + 360 + 288 = 3,438 slots; **plan 1,000–2,000**.

**Made-up-word derivation**
- L1.03–L4.16 is 60 lessons, minus 4 mastery checks and L4.15, so 55 checks × 2 extra sets × 5 = 550. Plus level checks 80, plus placement 80 = **710**.
- L1–L2 share: 312, plus the markdown's own (about 250, estimate).
- L3–L4 share: 398.

**Sound Teacher (human), Levels 0–2**

| Type | Count | MB |
|---|---|---|
| Words: L1 1,066 + L2 575 + L0 187 | 1,828 – 2,925 | 5.5 – 8.8 |
| Made-up words | ~560 | 1.7 |
| Answer-option words not already in the word list | 900 – 1,800 | 2.7 – 5.4 |
| Sentences (812 ± 25%) | 609 – 1,015 | 7.6 – 12.7 |
| Tier-2 lines (27 Listen & Talk lessons × 2 × 3) | 162 | 2.0 |
| English UI lines | ~200 | 1.8 |
| Slow takes (L1–L2 blend words) | 350 – 460 | 1.8 – 2.3 |
| Partial blends for the repair ("saaa"; distinct first-sound+vowel pairs in L1–L2) | ~200 (estimate) | 0.6 |
| Phonemes: 44 + /ks/ /kw/ /juː/ | 47 | 0.12 |
| Blending demos (26 lessons with a Blend section × 3) + judge's-card examples | 78 + 10 | 0.7 |
| **Total** | **~4,940 – 7,460 clips** | **~24.5 – 36 MB** |

**Urdu voice**: about **900 lines** (C9's 300 UI lines + C10's 600 glosses), 5.4 MB.

**The Reader (Kokoro), packs**

| Pack | Clips (words + sentences + made-up + options + Tier-2/word work) | MB |
|---|---|---|
| L3–L4 | 1,156–1,850 + 512–853 + 398 + 1,000–2,000 + 204 = **3,270–5,305** | **16.6 – 26.0** |
| L5 (practice) | 938–1,500 + 548–913 + ~200 = **1,686–2,613** | **12.1 – 18.4** |
| v1.1: L6 / L7 | research-05 gives about 18 / 11 MB (low end) | 29 + |

**Install size (estimates; first measured in week 3, final in week 8).**

| | Download (MB) | Installed (MB) |
|---|---|---|
| Shell: JS, Lottie, Andika font, about 315 pictures | **14 – 17** | 14 – 17 |
| Base audio: Sound Teacher + Urdu | 30 – 42 | 30 – 42 |
| Runtime overhead (estimate) | — | +3 – 10 |
| **App install** | **~44 – 59** | **~47 – 69** |
| Packs L3–L4 + L5 | 29 – 44 | 29 – 44 |
| **All of v1** | **~73 – 103** | **~76 – 113** |

**Native code, stated honestly.**
- Capacitor plugins: `@capacitor/filesystem`, `haptics`, `share`, plus **`@capacitor/file-transfer`**, because `Filesystem.downloadFile` has been deprecated since 7.1.0.
- No `.so` libraries of our own. One universal APK.

**Pack download prompt.**
- It shows **MB and minutes at an assumed 1 Mbit/s**, a slow mobile connection, which is about 7.5 MB a minute (D36; unmeasured).
- Example: "L3–L4: about 20 MB, about 3 minutes on slow internet".
- Stopping midway is safe, and the prompt says so.
- **No rupee figures**, because data prices are unverified.

### 4.2 Reader (Kokoro) pipeline

1. **Pinned build image.**
   - A Docker image pins kokoro, misaki, torch, system espeak-ng, the thread count and CPU dispatch (`MKL_CBWR=COMPATIBLE`), with a seed per clip.
   - The seed and threads are **hygiene**. **The guarantee is that an approved clip id is never re-rendered.**
   - Rendered approved files are the source of truth, and the build fails if a frozen clip's hash changes.
2. **Out-of-vocabulary words.**
   - On day 1, misaki looks up all 9,238 words.
   - For unknown words, espeak-ng (system build) only **proposes** a pronunciation. A reviewer approves it into `pron.json`.
3. **`ipa2misaki.py`** converts pronunciations to Kokoro's symbols, with a round-trip check that every symbol is in Kokoro's vocabulary. Owner: the build agent, week 1.
4. **Re-render loop.** If made-up words are misheard (research-02: vop→"vob"): reject → new pronunciation → new id → review. Budgeted in weeks 6–7.
5. **Speed 1.0 only.** No per-clip changes.

### 4.3 One post-process for every clip (human, Kokoro, Urdu)

1. **Trim** at −45 dBFS, keeping the whole burst on stop-final words. **Every threshold below is judged on the trimmed clip before padding.**
2. **Loudness.**
   - Clips ≥0.4 s: −18 LUFS integrated.
   - Shorter clips: −18 LUFS measured on a 0.4 s window centred on the energy peak, but **the boost is capped at +6 dB over the clip's own integrated loudness**.
   - So phonemes may sit 3–4 dB under words, and fricatives stay under the limiter.
3. **True-peak limiter at −1.5 dBTP is the hard cap**, applied after gain. Q1 **fails any clip limited by more than 2 dB**.
4. **Padding** 40 ms head / 80 ms tail. Fades: 5 ms; stop-final fade-out ≥15 ms.
5. **Urdu clips** go through the same chain, **resampled to 24 kHz**.
6. **Format**: Opus 24 kbps mono. Every measurement is taken on the decoded Opus.
7. **One gap value: 350 ms.** It is authored in the exercise timeline: between a sound sequence and its word, between repair sounds, and in the chant.

### 4.4 Voice-resolution table and QA

| Moment | Voice |
|---|---|
| Isolated sounds, any level | Sound Teacher |
| Words, sentences, made-up words, options in L0–L2 | Sound Teacher |
| Words and sentences in L3+ | Reader |
| L3+ repair | Sound Teacher sounds → learner blends → Reader word **only as confirmation after the 2nd attempt** |
| A tapped word, anywhere | **its own lexicon voice** (an L1 word inside an L3 sentence plays the Sound Teacher's take) |
| Review cards | the voice the item was learned in |
| Urdu lines | Urdu voice |

Test: an audio-trace check fails if a Sound Teacher clip and a Reader clip of the **same word** play within 1 s, except in the L3+ confirmation step.

**QA**

| Stage | Who | Scope |
|---|---|---|
| Q1 automatic | script | 100%: coverage, padding windows, loudness class means within 1 dB of sentences, ≤2 dB limiting, stop duration caps per class, sub-100 Hz flag in the first 30 ms |
| Q2 speech recognition | script | real words and sentences |
| Q3 judge | Gemini (triage) | made-up words by forced choice among their options |
| Human clips | **Recording engineer** picks takes (§4.5). The **General American reviewer** hears 100% of phonemes, made-up words, options and demos, plus 10% of words and sentences. A **second native General American listener (not Kamal)** rates a 150-clip overlap on an anchored 1–5 scale (clarity, pace, warmth) | **pre-set floor: ICC(2,1) ≥ 0.75 or weighted kappa ≥ 0.6**; below that, re-anchor and re-rate |
| Reader clips | General American reviewer: **10% per pack** (about 500–790 of the 4,950–7,920 L3–L5 clips) **plus 100% of overrides and made-up words**, once per frozen pack version, skipped when ids are unchanged | per pack |
| Handover | **8 naive listeners** rate the first L3 sitting for "comfortable" | **pass: mean ≥4/5 and at most 1 rating below 3**, committed before rating |

### 4.5 The Sound Teacher and the recording chain

**Audition (weeks 0–1).**
- Three General American female candidates record a test file that includes three /p t k/ takes and **a timed 200-clip pilot** (words, made-up words, stops), which measures the real clips per hour.
- Scoring: the General American reviewer scores accent; 3 blind listeners score pace and warmth against af_heart sentences.
- No pitch or spectral target. Reasons:
  - af_heart's pitch (215–238 Hz) sits at the top of the adult range;
  - Kokoro has no usable isolated-sound reference (/s/ centres at 513 Hz);
  - the voices never alternate inside an exercise, so only pace and warmth carry across the Level 3 handover.

**Direction for stops**
- "Say the sound as if the word stopped right there: the /p/ at the end of *cup*, with no 'uh' after it."
- Voiced stops are a short murmur with no vowel.
- Three takes each; **pick the shortest clean burst**.
- The General American reviewer blind-labels the /p t k b d g/ takes as free of an added "uh".

**Recording spec.**
- Pop filter required. Room tone ≤ −60 dBFS. Input peaks around −12 dBFS. Mic at 20–30 cm.
- 48 kHz mono WAV masters, no AGC, no noise suppression, no echo cancellation.
- **Retake rule**: retake in the same session (or at a pickup) on any clipping, plosive thump, noise above the floor, mouth click, schwa on a stop, or reviewer flag.
- Each session opens with room tone and a reference /æ/.

**`voice_studio.py` changes (it currently does the opposite)**
1. Request audio with `echoCancellation:false, noiseSuppression:false, autoGainControl:false, sampleRate:48000`.
2. Capture PCM through an AudioWorklet and write **48 kHz 24-bit WAV**, replacing MediaRecorder webm/opus.
3. Drop the import's **16 kHz** resample, trim and normalise. Masters stay raw; the shared post-process (§4.3) makes the 24 kHz deliverables.
4. Add an input meter with the −12 dBFS target and a room-tone check at ≤ −60 dBFS.
5. Store numbered takes (3 per phoneme and per stop) and add a take-selection view for the engineer.
6. Load scripts from the English content JSON in place of the Urdu clip kinds.
7. The speaker runs it locally (one Python file) or records in her own software to the same naming and spec.

**Rate and hours.** One rate: **150 clips/hour**, including retakes and the session check. That gives **4,940–7,460 clips ≈ 33–50 studio hours**, about 13–20 sessions of 2.5 h:
- week 1: phonemes, demos, partials, UI;
- weeks 2–5: L0–L2 words, made-up words, options (only after they are reviewed), sentences, slow takes;
- week 9: pickups.

The week-0 pilot replaces the 150/h assumption with a measured number.

**Recording engineer (D33).** A named role, paid. They review uploaded takes within 24 h, pick takes, and request retakes. This is separate from the General American reviewer.

**Urdu voice (D9).**
- The Sara licence is closed in writing before week 3: terms in force at generation, commercial use, redistribution in an APK.
- Otherwise a human Urdu speaker records with the same kit.
- Either way the clips go through §4.3.

### 4.6 Licences

| Item | Licence | Action |
|---|---|---|
| Kokoro-82M | Apache-2.0 | versions in LICENSES.md |
| misaki | check | week 1 |
| Sound Teacher | signed release, perpetual and commercial | — |
| Urdu voice | per D9 | — |
| Course content | CC BY 4.0, attributed | — |
| Andika | SIL OFL per research-05 | verify |
| Piper | not used: the Blizzard 2013 Lessac licence clause 3.2 restricts use to research (read by the lead 2026-10-05) | — |
| OpenMoji | CC BY-SA, unconfirmed | check before use |
| "Sound Out" name | not searched (NAME-ASO) | **D37** |

---

## 5. Listening

- **v1: none.** No microphone. Read-aloud checks happen only in optional helper sessions. Unchanged by research-06.
- **v1.1: record and replay** (labelled practice; microphone behind the grown-up gate), plus the **verifier candidate: Whistle** (research-06).
  - **What it is.** On-device speech-to-text: one 16.9 MB model, CPU only, Apache-2.0; Android arm64/armv7 and WASM engine builds.
  - **How it would judge.** Keyword biasing with the target plus the gate's three options (first sound / vowel / final sound), and a probability for each word.
    - transcript = target and prob ≥ θ → `clear_yes`;
    - transcript = an option → `clear_no`;
    - anything else → `unsure`, never yes.
    - "cake" was heard as "Take" at 0.83 with "take" missing from the keywords, so the keyword list must be the gate's options.
  - **Lead's desktop test** (research-06, adult Kokoro clips): keyword words and pseudowords recognised; biasing fixed "ship" and "chote"; 0.1–0.25 s per clip after warm-up. **Isolated sounds and letter names failed**; they stay tap- or helper-judged.
  - **Unverified** (research-06): child speech, Urdu-accented speech, latency and RAM on a cheap Android phone, beam settings, how strong the keyword biasing is, and the engine binary's licence.
  - **Gate role:** only after the gold set passes; extra credit on top of E6d, never a replacement.
- **Fallback (v2), if Whistle fails the kid test:** a CTC phoneme verifier, roughly 10–15 days of work.
  - A wav2vec2-class model running in onnxruntime.
  - Our own scoring of the target against the one-position options, the letter name, an added schwa, and the regular reading of tricky words.
- **Gold set (for either engine).**
  - ≥60 items **per class**, labelled by a **native General American speaker, not Kamal**, with Kamal as second rater.
  - Pass: precision ≥97% with a lower bound of ≥92%. A class with too few items is "undecidable", which counts as no-go.
  - Urdu-accented vowel merges are practice, never wrong.
  - A native plugin brings the first `.so`, so 16 KB alignment applies.
- **WCPM (v1.1, Level 5 passages):** Whistle word timestamps (test sentences exact in research-06), shown as "approximate"; child speech unverified.
- This **reverses research-03's v1 stack and research-04's D6** (see D0b).

---

## 6. Tech

### 6.1 Repo and reuse

- **Repo:** `oyekamal/sound-out`. Code is copied from `urdu-reading-course/mobile`; PROVENANCE.md records it. Copied code: about 12% as-is, 70% with changes.
- **New work:**
  - the lesson/sitting state machine and the gate reducer;
  - E5, E6d and the option generator;
  - placement and quick-start;
  - the Track A world and the Stories tab;
  - the mother's view and the profile/gate flows;
  - the audio-clock engine.
- path/learner/onboarding/drills are rewrites.
- minSdk 23, targetSdk 36.

### 6.2 Content pipeline

- **Parser:** `build_content.py --strict` over all 115 files (108 lessons + 7 mastery checks).
- **Week-1 exit:** a coverage report plus **yield per level**, meaning the share of lessons whose check items, bar and made-up-word set parse unaided. Engineer's crude regex: L1–L4 high, **L5 0/16**. Free-response L5 items are flagged.
- **Fixes** go in as reviewed `app:` YAML blocks, sent as PRs to the course repo (issue #3).
- **L5 multiple-choice checks** are a content ticket (C11); until they land, L5 is practice.

```jsonc
// content/lessons/L1.02.json (generated by the build; the sample must pass its own gates)
{ "id":"L1.02","contentVersion":"2026.10.1",
  "sittings":{"A":[{"id":"A","new":["s"],"steps":["hear","meet","trace","sound_game"]},
                   {"id":"B","new":["a"],"steps":["warm","hear","meet","trace","blend","spell"]},
                   {"id":"C","new":["t"],"steps":["warm","hear","meet","trace","blend","spell"]},
                   {"id":"D","steps":["warm","blend","tricky","spell"]},
                   {"id":"E","steps":["read"]},{"id":"F","steps":["listen"]},{"id":"G","steps":["check"]}],
              "B":[{"id":"ABC","steps":["hear","meet","blend","pick","spell"],"keepGoing":true},
                   {"id":"D","steps":["warm","tricky","read","listen"]},{"id":"G","steps":["check"]}]},
  "pick":{"sat":{"onset":"pat","vowel":"sit","final":"sad"},
          "at":{"onset":"it","final":["an","am"]}},
  "check":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"],"dictation":["at","sat","as"],
           "bar":{"pass":9,"of":11,"source":"lesson","courseIssue":1},"firstAttemptOnly":true,"minJudged":11} }
```

**Gates.** The build fails on any of:
1. decodability;
2. made-up-word filter (issue #2);
3. **the option rule** (one first-sound-only, one vowel-only, one final-only; same lexicality; no repeats);
4. pronunciation round-trip;
5. audio coverage + Q1;
6. every bar reachable on judged items;
7. sitting budget ×1.5;
8. no-cueing strings;
9. sizes within §4.1 ranges +10%;
10. snapshots.

### 6.3 Audio engine (audio clock)

**Why the Urdu player won't work.** The Urdu `Audio()` player never seeks. Capacitor's local server answers `Range` with the whole file from byte 0 (`WebViewLocalServer.java:369-386`). Timers cannot hold the gaps.

**The engine**
- Fetch a lesson sprite (one Opus per lesson, plus an offsets JSON) via `convertFileSrc`.
- **`decodeAudioData` once** into an `AudioContext({sampleRate:24000})`.
- Schedule each clip with **`AudioBufferSourceNode.start(when, offset, duration)` on the audio clock**.
- Gaps (350 ms), sequences and the chant are scheduled ahead, so animation stutter cannot stretch them.

**Sprites**
- A **core sprite** with the 47 sound clips, the UI lines, the partial blends and the Urdu lines is always decoded: about 90 s, about 8.6 MB as Float32 at 24 kHz.
- **Lesson sprites**: about 150 s each, about 14 MB decoded. At most 2 are kept in an LRU (current + review source), so audio memory stays under about 40 MB.
- Review cards from other lessons load their lesson's sprite on demand.

**Week-1 test.** On the test phone:
- record the device output through a USB audio interface, or with a second recorder on the line out;
- play **s-a-t → "sat"** 200 times under a Lottie-heavy screen;
- pass: **p95 deviation from the 350 ms gap ≤15 ms**, and no audible click at clip edges;
- also measure p95 tap-to-sound (budget <150 ms).

### 6.4 Data, migrations, backup, packs

**Database**
- Stores, kept: settings, profiles, attempts, cards, sessions, progress, assessments. Added: mastery, packs, helper.
- Delete the Urdu `db.js` repair path that bumps the version.
- `onupgradeneeded` gets a ladder of upgrade steps, tested against fixture databases.
- Progress is keyed by lesson id and item text, never by clip id.

**`backup.js` field fixes**

| Field | Change |
|---|---|
| `profiles.track` | `oneOf('A','B')` plus `shapes`, `pinEveryTime`, `homeLang` |
| `unit: int(0,12)` | becomes `lesson: /^L[0-7]\.\d{2}$/` in attempts, cards, profiles and wpm |
| `cards.idx: int(0,500)` | becomes `int(0,20000)` |
| `cards.kind` | becomes `gpc\|word\|tricky\|tier2\|morph` |
| `UI_KEYS` | gets the new settings (comfort, slow mode, reminders, pinEveryTime) |
| `LIMITS` | gains entries for mastery, packs and helper |
| progress keys | lesson ids |
| card ids | `profileId:kind:sha1(text)[:8]` |
| format | `BACKUP_FORMAT="sound-out-1"`; Urdu backups are rejected with a message |

**Test (week 3):** a deep-equality round trip of a **fully populated fixture** (Track B adult, shapes, PIN toggle, L1.02 keys, the word "don't").

**Packs**
- Downloaded with `@capacitor/file-transfer`, resumed per file.
- **Signed ed25519 manifest** (D32), checked against `contentVersion` and `gpcHash`, with a reconcile at launch.

**PWA service worker**
- The **runtime cache** stores pack paths (`packs-v{contentVersion}`).
- Base audio is cached **lazily per lesson with retries**, not in the eager install set, so one failed fetch cannot break the install.
- It calls `navigator.storage.persist()` and **shows the result** in the grown-up area ("this phone may clear lessons when full").

### 6.5 Devices and budgets

- **D24 (week 0):** buy a 2–3 GB Android 10 phone.
- **Budgets:** cold start <2 s; render <100 ms; tap-to-sound p95 <150 ms (audio clock); gap p95 error ≤15 ms; JS <150 KB gzip; memory <150 MB; child night one ≤90 s; adult ≤~15 min.

### 6.6 Tests (auto / device / human)

**Auto** (green by the end of week 4, when its subjects exist):
- parser, content gates, snapshots;
- reducer tests: timeouts, `minJudged`, first-attempt-only;
- **oracles**:
  - a perfect decoder reaches L1.06 within a bounded number of sittings, with no helper;
  - an **onset-blind oracle fails** the L1.03–L1.06 gates (≤1.1% each);
  - a **lexicality oracle** (always picks the real word) is at chance;
  - a **slow decoder** (correct at 10 s) passes L1–L2 checks;
  - an **80%-per-item learner over 13 lessons** reports how many lessons are cleared and how many end `still_learning`;
- no-cueing DOM checks + audio traces (whole-word and same-word voice mixing);
- DB ladder; backup deep-equality; pack signature / incompatible-pack tests.

**Device:** the loopback gap test, tap-to-sound, memory, installed size, airplane-mode L1, file-transfer kill-and-resume on Android 10 and 13.

**Human** (recruited in week 0):
- icons-only first launch (10 Urdu-only adults + 10 children);
- sibling test (an 8-year-old, 10 minutes, open profile and pattern);
- parent-absent test;
- the mother's view test (3 Urdu-only mothers: "Is she doing well? What do you do tomorrow?");
- Track B screenshot audit;
- the Urdu-only minimal-pair validation (5 listeners);
- stopwatching 5 children on Sittings B and C.

---

## 7. Global

**Languages**
- v1: English + Urdu UI.
- Wave 1: Hindi, Arabic, Spanish, Bengali. Wave 2 follows Play data (D8).
- Punjabi and Pashto speakers get the Urdu UI in v1. This is a stated limitation.

**Accent (D15).** General American is **the app's choice**.
- The course names no accent: its placement test accepts /ɒ/ or /ɑ/, and L1.05 describes o as /ɒ/.
- General American /ɑ/ falls inside what the course accepts.
- Urdu-speaker notes come unchanged from the course.

**RTL**: the UI mirrors; English content does not.

**Compliance**
- Play Families, mixed audience.
- No ad, analytics or ad-ID SDKs; no age collected.
- No microphone in v1 (COPPA amended 22 April 2026).
- GDPR-K and the UK Children's Code: nothing leaves the phone; a DPIA note.
- Data Safety: "No data collected".
- IARC rating: Education.
- Closed test: ≥12 testers × 14 days.
- AI-voice disclosure for the Reader, plus credit for the Sound Teacher.

**Listing** (from `store/NAME-ASO.md`)
- Title: "**Sound Out: Read English**".
- Short description: "Learn to read English with phonics. Kids & adults. Free, offline, no ads."
- Hooks:
  - offline;
  - adults welcome;
  - free, no ads, no account;
  - no English-reading helper needed;
  - checks with made-up words;
  - never resets.
- Size line: the measured download and installed size.
- Banned claims: "proven", "guaranteed", "cures dyslexia", any effect size, a Teach Your Monster "RCT", "critical reading" and "100 WCPM" (until v1.1 / v2).
- The trademark check (D37) comes before upload.

---

## 8. Build plan (10 weeks + week 0; week 9 is slack)

**Who:**
- Kamal;
- the Sound Teacher (speaker);
- the recording engineer;
- the General American reviewer;
- a second native listener;
- the build agent (Claude Code);
- fresh critics;
- the Gemini judge (triage only).

| Week | Deliverables | Exit check |
|---|---|---|
| **0** | D0a/D0b confirmed; phone bought; **recruit lists for every human test and the pilot, with dates**; 3 speaker candidates sent the test file with the timed 200-clip pilot; engineer, reviewer, second listener and D16 fee agreed; `voice_studio.py` changes; Docker env | dated recruit list; measured clips/h per candidate |
| **1** | **Parallel, does not gate v1:** 2-day Whistle spike (research-06): android-arm64 Needle in a Capacitor plugin; 30 CVC words × 3 speakers (Kamal's two kids + one adult) × 2 takes, with planted first-sound/vowel/final errors. **Go bar: ≥97% `clear_yes` precision and ≤1.5 s p95 latency on the test phone** (continues into week 2). Speaker chosen; **phoneme session** (47 × 3 takes, stop direction) + demos, partials, UI; parser coverage + **yield per level**; misaki OOV count; `ipa2misaki`; **audio-clock loopback test**; L0–L1 text frozen | coverage + yield committed; phonemes pass Q1 and the reviewer; gap p95 ≤15 ms |
| 2 | Repo; strict parser + `app:` PRs; made-up-word and option generators; **review of L1 made-up words and options before they are recorded**; recount; sessions: L0–L1 words | `npm run content` exits 0 for L1–L2; the §6.2 sample passes the gates |
| 3 | Shell: one-screen first launch, child night one (quick-start + A), adult fast-track night one, gates/PIN/shapes, DB ladder, backup round trip, audio-clock engine + core sprite; L1 audio QA; sessions: L1 sentences, options, slow takes | **G0** stopwatches; first installed-size reading; round trip passes |
| 4 | E1–E12, E5, E6d, E22, E23, E4; gate reducer and repairs; Track A world; **Stories tab**; Listen & Talk; sessions: L2 words, made-up words | auto set green; oracles behave as stated |
| 5 | Show-what-you-know flow + Urdu intro; mother's view; quick-start + grown-up placement; helper sessions; Urdu minimal-pair validation; sessions: L2 sentences, options, slow takes; **critic round 5** (teacher, parent) on a recorded L1.02–L1.04 run | 5 archetype fixtures placed correctly; sibling and mother tests run |
| 6 | Reader L3–L4 pack + review; handover screen + voice table; pack manager (file-transfer, signed manifest, MB + minutes); L2 audio QA | handover listening test passes; pack tests pass |
| 7 | L5 practice sessions + pack; service-worker pack cache + persist(); Urdu clips QA; Reader re-render loop | L5 oracle runs end to end |
| 8 | Performance, a11y, RTL, blinded-text audit; PWA; signed APK; final installed size; remaining human tests | budgets met or a gap list |
| **9** | **Slack**: lost-gate re-runs, pickups, fixes | — |
| 10 | Gauntlet G0–G7; privacy, Data Safety, Families; listing EN/UR; internal test; closed test; pilot starts | verdicts recorded |

**Cut list, in order, any week from 3 to 8.** When a week slips, drop the first item still unfinished:
1. Placement Stages 1 and 4 (helper parts).
2. Judge's card and "mastered".
3. E14.
4. Track B real-world unlockables.
5. Urdu Tier-2 glosses beyond L1–L2.
6. E22 cut down to v/w and the short vowels.
7. Stories tap-read and the chant (read-to-me stays).
8. **L5 practice pack → v1.1.**
9. **L4 pack → v1.1** (v1 gated content becomes L0–L3).
10. PWA → v1.1.

**Never cut:** the **Levels 0–2 Sound Teacher audio**, the **tap gate (E6d)**, and the **Track A / Track B skins**.

**Roadmap**
- v1.1: L5 MCQ gates; L6–L7; E18, E20, E21; teacher mode; pack sharing; wave-1 languages.
- v1.1 also: the Whistle verifier and Whistle WCPM, if the spike and the gold set pass.
- v2: the CTC fallback verifier if Whistle fails; FSRS scheduling; iOS.

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation | Known by |
|---|---|---|---|---|
| Recording takes 33–50 h and the speaker's availability slips | Medium | High | Timed pilot in week 0; L1 first; week 9 slack; cut items 8–9 | Week 2 |
| E6d over-credits | Medium | High | One-position option rule; oracles; first attempt only; re-check; proxy validity test | Pilot |
| Vowel options measure hearing, not reading (Urdu ears) | Medium | Medium | Ear/eye split; 5-listener validation | Week 5 |
| Audio-clock engine memory on 2 GB phones | Low–Medium | Medium | 24 kHz context; LRU of 2 sprites | Week 1 |
| Parser yield on L5 | Certain | Medium | L5 ships as practice; C11 ticket | Week 1 |
| Level 3 handover disliked | Medium | Medium | Pass bar; fallback: Sound Teacher records L3 words (estimate +10 h) | Week 6 |
| Night-one adult runs over 20 min | Medium | Medium | Fallback to A+B with "sat" on night two | Week 3 |
| A year of daily use loses children | High | High | Track A world, Stories, mother's view; measured in the pilot | Pilot |
| Whistle fails on child or Urdu-accented speech (unverified, research-06) | Medium | Low for v1 (no speech gate) | 2-day spike + gold set; CTC fallback in v2 | Weeks 1–2 spike; gold set later |
| Whistle engine binary licence (repo says Apache-2.0; the platform folder's LICENSE is unconfirmed, research-06) | Low | Medium | Confirm before the spike code is merged | Week 1 |
| Trademark conflict on "Sound Out" | Unknown | High | D37 search | Before upload |

---

## 10. Decisions for Kamal

**W0** = needed before week 1.

| # | Decision | Default | Blocks |
|---|---|---|---|
| **D0a** | Voice: Sound Teacher (human) for L0–L2 and all isolated sounds; the Reader (Kokoro) for L3+ words. Reverses "local model for all voices" | Confirm. Alternative: Kokoro words + recorded phonemes (B in rounds 1–2) | **W0** |
| **D0b** | No speech gate in v1; E6d tap gate; verifier in v2. Reverses research-03's v1 stack and research-04 D6 | Confirm. Alternative: verifier on the v1 path (engineer: slips) | **W0** |
| D8 | Languages | EN + UR; waves follow Play data | — |
| D9 | Urdu voice licence (Sara) or a human Urdu speaker | Close in writing by week 3 | week 3 |
| D15 | Accent: General American (the app's choice; the course names none) | Yes | W0 |
| D16 | Sound Teacher + fee for **33–50 studio hours** + pickups | Hire, remote | **W0** |
| D18 | Mascot Pebble (new, silent) | Yes | week 3 |
| D21 | Pilot: 5 children + 5 Track B learners | Yes | week 0 |
| D23 | General American reviewer | Paid | **W0** |
| D24 | Test phone (2–3 GB, Android 10) | Buy | **W0** |
| D27 | Course issues #1 (bars), #2 (made-up-word filter), #3 (machine-readable structure); new: L5 MCQ checks, L5.16/L7 bars, L4.15 format, 14/16 = 87.5% | File the new ones | week 2 |
| D28 | Adult PIN only once an adult exists; arithmetic gate otherwise; 24 h reset; child pattern 4 of 9, lockout, 10-min idle timeout | Yes | week 3 |
| D29 | Start at L1.02 | Yes | W0 |
| D30 | v1 = L0–L4 gated, L5 practice, L6–L7 in v1.1 | Yes | W0 |
| D31 | Only first attempts count | Yes | week 4 |
| D32 | Who holds the pack-signing key | Kamal, offline | week 6 |
| **D33** | Recording engineer (take selection) | Paid freelance | **W0** |
| **D34** | Second native General American listener (not Kamal) | Paid | **W0** |
| **D35** | Adult night one = compressed course fast track (A+B+C, ~15 min target), fallback A+B | Yes | W0 |
| **D36** | Assumed download speed for pack prompts | 1 Mbit/s | week 6 |
| **D37** | Trademark search for "Sound Out" | Before upload | week 9 |


---

## 11. Content work to commission

| # | Item | Owner | By |
|---|---|---|---|
| C1 | Print-concepts mini-module | course author | week 5 |
| C2 | 710 generated made-up words + native review | build agent + General American reviewer | weeks 2–6 |
| C3 | Placement forms B and C | author | week 5 |
| C4 | Grapheme/phoneme lexicon; `heartIdx` for the 69 tricky words | build agent + Kamal | week 2 |
| C5 | `pron.json` from the OOV count | build agent + reviewer | weeks 1–6 |
| C6 | 44 mouth-cue images, **signed off by a phonetician** (the General American reviewer, if qualified; else a paid check) | art + phonetician | week 4 |
| C7 | `app:` YAML (bars, reteach, error classes) | build agent + author | weeks 2–4 |
| C9 | UI script EN ~200 + UR ~300 | build agent + reviewer | weeks 1–4 |
| C10 | Urdu glosses ~600, **checked for answer leakage** | author + Urdu reviewer | week 5 |
| C11 | **L5 MCQ checks** (v1.1 gate) and the L6–L7 materials | author | v1.1 |
| C12 | Village art, Pebble rig, Listen & Talk / Stories pictures (~315 total) | art | weeks 3–4 |
| C13 | Recording scripts, frozen per level | build agent | weeks 0–4 |
| C14 | Option sets reviewed for rude or confusable words | build agent + reviewer | week 2 |
| C15 | Course tickets (D27) | build agent | week 2 |

---

## 12. How we will know it works

### 12.1 Metrics without telemetry

All on the phone; the user exports them if she wants.
- First-attempt E6d accuracy, real and made-up words.
- Share of lessons that are checked, checked twice, or mastered.
- `still_learning` count; ear-versus-eye misses; timeouts.
- English Listen & Talk score; L5 pace.
- Days practised; returns after a gap; **dropout**.

### 12.2 Pilot (from week 10, 6 weeks)

**Recruits**
- 5 children: Kamal's two, plus three others, at least two with a mother who cannot read English.
- 5 Track B learners: a teen, a shop worker, a grandparent, an Urdu-literate adult, and an adult who cannot read Urdu.

**Proxy-validity check.** A blind teacher who speaks General American hears each learner read aloud the same items they answered by tapping. Target: **≥90% agreement**. Timing:

| | When | What |
|---|---|---|
| Children | after L1.04 (about 18 sittings) and after L1.06 (about 30) | both fit inside 42 days at 1 sitting a day (L1.08 would not) |
| Adults | after L1.04 and after L1.08 (about 21 sittings) | — |

**Also measured**
- Pre/post: placement form A, then form B.
- Weekly: English Listen & Talk questions, the mother's view interview, the Level 3 handover question for anyone who reaches it.

**v1.1 bar**
- Every child advances with no helper.
- Proxy agreement ≥90%.
- ≥7/10 still practising in week 6.
- No reports that the app feels made for children from Track B.
- Zero frozen screens; zero cueing.

### 12.3 Gauntlet gates

Fresh critics, anonymised material, scored both ways round. G0 and G7 are pass/fail.

| Gate | Compared with | Test |
|---|---|---|
| G0 Night one | stopwatch | child's first sound ≤90 s, one screen before the lesson; adult's first word ≤~15 min (else the D35 fallback is adopted); relaunch ≤10 s |
| G1 Child first week | Duolingo ABC | explicit sounds; judged blending; no adult needed; delight; mother's view |
| G2 Play loop | **Teach Your Monster** | village, stickers, Stories; resistance to guessing (oracle results); repair quality |
| G3 Parent view | Khan Kids | "tonight's 3 sounds"; honest labels; sibling-proof; size + minutes honesty |
| G4 Adult dignity | Learning Upgrade | first word on night one; "words to remember"; no child avatars; PIN flow |
| G5 Audio | Sara (reference) | Sound Teacher clarity, warmth and consistency; stops free of "uh"; loudness spread; **handover bar (§4.4)** |
| G6 Proxy validity | blind teacher | ≥90% agreement; oracle table |
| G7 Rule audit | DESIGN.md §2 | every §2.3 row passes |

---

## Appendix: sources

- **Repo:** `/home/oye/Documents/free_work/sound-out/`
  - `plan/` (research/research-01…06, critics/, bar/, decisions.tsv, RESUME.md, plan-v1…v3, v2/v3-changes);
  - `store/NAME-ASO.md`.
- **Course:** `/home/oye/Documents/free_work/english-reading-course/` (DESIGN.md, course/level-0/placement-test.md, 108 lessons + 7 mastery checks, tools/decodable.py, issues #1–3).
- **Urdu app:** `/home/oye/Documents/free_work/urdu-reading-course/`
  - `mobile/src/content.js` (Audio() player), `db.js`, `backup.js` (validators cited in §6.4);
  - `scripts/voice_studio.py` (lines 353–357: echo cancellation and noise suppression on, webm; importer at 16 kHz);
  - `mobile/package.json` (filesystem, haptics, share).
- **Capacitor:** `WebViewLocalServer.java:369-386` (Range handling, per engineer r3).
- **External URLs:** as in research-01 to research-04 and plan-v1's appendix.
