# Sound Out: the app plan, v5

Date: 2026-10-06. Owner: Kamal. Repo: `oyekamal/sound-out`. Play title "Sound Out: Read English", package `com.oyekamal.soundout`.
- **What v5 is**: v4 re-centred on Kamal's call "this app is for the whole world, not for Urdu speakers" (decisions row 9), plus lead decisions (10)–(12) and every round-4 defect, each mapped in `v5-changes.md`.
- **Evidence**: `plan/research/` 01–06, `english-reading-course` (DESIGN.md, 108 lessons, `placement-test.md`), `plan/bar/`, `plan/critics/`.
- **Labels**: "unverified" (the source said so), "estimate" (ours), "budget" (a target), "assumed" (an input we chose). **No budget here is measured.**

---

## 0. Summary, two decisions, the bar

Sound Out is a free, offline Android app (plus PWA) that teaches anyone, anywhere, to read English from the first sound. **The core needs no home language**: an English teacher voice, icons, pictures and gestures the mascot demonstrates carry every instruction. Home-language help is an optional **helper pack**; Urdu is one of them.

- **v1 scope**: gated Levels 0–4; Level 5 practice until its MCQ checks exist (C11); L6–L7 in v1.1. Urdu Qaida shell reused (Capacitor 7, Vite, IndexedDB, Leitner).
- **Night one, nothing extra downloaded**: an Ohio child and a Recife child both tap "A child", pick a picture, skip "Help in your language?", and tap the first letter sound **≤90 s from process start**. An adult does 3 minutes of print concepts, then picks "sat" from print in about 18 minutes, in private.
- **The tap gate (E6d)**: read a printed word silently, tap which of four spoken words it says; the options form a **2×2 grid** (answer, first-sound change, vowel-or-final change, both), so no option is structurally special. No English reader needed; a helper may upgrade to "mastered".
- **Not in v1**: accounts, ads, analytics, mic.

### D0a: voice (boundary at Level 4, lead decision 10)

- **Levels 0–3: one human General American female voice, the Sound Teacher**: 47 sounds (53 clips with stop variants), 26 letter names, every L0–L3 word, made-up word, option, sentence (both tracks), Tier-2 line, slow take, partial blend, and the ≤60 English UI lines.
- **From Level 4: the Reader** (Kokoro-82M `af_heart`, rendered offline). L4's method is syllable and morpheme chunking (DESIGN L4.12–4.14), so repairs play **the Reader's own chunks** ("gar… den", from IPA), then its word. **No isolated sound inside any Reader exercise**; sound review cards use human core clips only. The Reader is introduced once, at L4.
- **Evidence**: research-02 §5's Gemini judge heard Kokoro /m/ /p/ but not /s/ /ʃ/ /θ/ /æ/ (research-02: the judge may be at fault; no human listened). Kokoro's /s/ centres at 513 Hz (critics-round-2-audio.md). Audio critics in all four rounds rejected human sounds then a Kokoro word; v5 removes that join.
- **Cost (assumed rates; week 0 measures)**: **~6,670–10,190 clips ≈ 44–68 studio hours at 150 clips/h, 56–85 h at 120/h** (§4.1, §4.5). L0–L3 text frozen before recording.
- **D0a-alt: the human records all v1 audio, Kokoro dropped**: L0–L5 ≈ **10,400–16,300 clips ≈ 70–109 h at 150/h, 87–136 h at 120/h** (lead's "~10k, ~65 h" = low end). Gains: one voice, no AI disclosure, no Kokoro pipeline. Costs: +26–51 h; L4–L5 text changes need pickups; L6–L7 need her too.

### D0b: listening

- v1 has no speech gate and no microphone permission.
- **Evidence**: sherpa-onnx keyword spotting cannot return yes/unsure/no; CTC scoring was "10–15 working days before any kid data" (critics-round-2-engineer.md line 15). At research-03 §8's 60% recall target a correct reader passes a 10/11 gate ~3% of the time.
- **Reverses** research-03 §7's v1 speech witness. research-04 D6 already deferred ASR; what v5 drops from it is helper-judged read-aloud (E6b) as the gate.
- **Roadmap**: v1.1 record-and-replay + Whistle verifier candidate (research-06); v2 CTC fallback (~10–15 days, engineer r2).

### The bar (features: Duolingo ABC, Khan Kids; play: Teach Your Monster; pedagogy: DESIGN.md; audio: Sara)

| Sound Out v1 | Duolingo ABC | Khan Kids | Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes | parent email account | Yes | iOS $8.99 | $4.99/mo |
| Offline | "Offline Learning" | partial | after download | not documented | no evidence |
| Adult track, same sequence | No | No | No | No (ages 3–6) | Yes, 3.2/5 |
| Placement | No | age/performance path | No | not found | not found |
| Made-up-word gate, balanced options | not found | not found | not found | not found ("progress by guessing", one review) | not found |
| Home-language help | No | Spanish read-to-me | several languages | No | a few onboarding languages |

"Not found" = absent from research-01 and listings. US iOS: Khan 4.80 (131,337 ratings, 201 MiB); ABC 4.25 (3,810, 212 MiB); TYM 4.47 (29,802, 96 MiB).

---

## 1. Who it is for

**Promise:** "Ten minutes, or more if you want. Starts at the first sound. Works in English alone, with help in your language if you want it. Offline, free, private, never starts you over, and no one who reads English has to help."

**Time** (estimate). Sittings run **on demand**, each unlocked by the previous mini check (§3.3).

| L1.02 to end of L4 (61 lessons) | Sittings | 1 a day | 2 a day |
|---|---|---|---|
| Child, Track A, ~6/lesson | ~366 | ~12 months | ~6 months |
| Adult, Track B, ~3/lesson | ~183 | ~6 months | ~3 months |
| Adult fast track, ~1.5–2/lesson | ~92–122 | 3–4 months | 1.5–2 months |

No age is collected; only placement moves a learner ahead. A grown-up may give any profile the Track B skin (an 8-year-old who finds the village babyish).

### 1.1 Five people, night one

| | Ayesha, 5, Rawalpindi; mother reads no English | Lívia, 6, Recife; father reads Portuguese only | Emma, 5, Ohio; native, knows letter names | Rukhsana, 35, Rawalpindi stall worker; reads Urdu | Budi, 29, Jakarta rider; reads Indonesian |
|---|---|---|---|---|---|
| Onboarding | picture → Urdu pack (background) | picture → skip | picture → "Just English" | PIN → Urdu pack | PIN → skip; Indonesian on night two |
| Night one | Sitting A (/s/ ~1:10, trio, sticker), "One more?" → B; ~16 min | same, English only, via gestures | quick-start 2/5 (names, not sounds); A, B, C on demand | print concepts → A+B+C → picks **sat** | same, English only |
| Exit | first sound ≤90 s | ≤90 s, no pack | ≤90 s | first word ≤~18 min | same |

Sibling fixture: Ayesha's brother Hamza, 8, own profile, quick-start 5/5 → tap ladder → L2.03, skipped tricky words back-filled (§3.6).

**Month one (illustrative)**: Ayesha, Rukhsana to L1.08; Lívia to L1.06; Emma to L1.10; Budi to L1.12.

---

## 2. The pedagogical engine

| Level | Lessons | Notes (greps, reproduced by auditor r4) | v1 | Voice |
|---|---|---|---|---|
| 1 | 14 | Blend 13, Listen & Talk 14, Track B 12; L1.13 letter names vs sounds | gated | Sound Teacher |
| 2 | 14 | Listen & Talk 13, Track B 13 | gated | Sound Teacher |
| 3 | 18 | Listen & Talk 17, Track B 17 | gated | Sound Teacher |
| 4 | 16 | Blend 14, L&T 15, Track B 15; L4.12–14 syllables, word attack | gated | Reader |
| 5 | 16 | free-response checks; L5.16 no bar | practice | Reader |
| 6–7 | 30 | no Track B; most L7 no bar | v1.1 | Reader |

Order and the 69 tricky words (L1 24, L2 29, L3 16) in `data/gpc.json`, `data/heart.json`; shown as "tricky words" (A) or "words to remember" (B). Strands as v4, plus letter names (L1.13, free play).

**Every DESIGN.md rule, enforced**

| Rule | How | Check |
|---|---|---|
| 1 No cueing | no picture beside an unread word (Stories too); no repair plays the target before the retry | DOM test; audio trace between miss and retry |
| 2 Decodable (L1–L4) | taught GPCs, scheduled tricky words, ≤2 flagged story words | `decodable.py` |
| 3 Blend before segment/spell | step order; single-sound sittings spell no words | snapshot on real JSON |
| 4 Mastery gate | lesson's bar on judged first attempts (default 0.9); course issue #1 | reachability + oracles |
| 5 Tricky words mapped | E8; 1–2-letter tricky words never in E6d | lint `heartIdx` |
| 6 Two registers | `read.B` or `sameAsA` | parser + child-word lint |
| 7 Comprehension daily | English Listen & Talk, picture answers | coverage |
| 8 Two metrics | no blended score; L5 "pace" | schema + grep |
| 9 L1 notes | `l1_tags`; notes ship only in helper packs | tag + pack lint |
| 10 Pause-safe, no streaks | "skip" = take the lesson's check first, gated | kill/resume ×20 |
| 11 Multisensory optional | tracing default on, skippable | settings test |
| 12 Honest citations | no effect sizes in store or app | banned-claims grep |
| Machine never promotes mastery or a `still_learning` sound | "mastered" needs a helper (departs from research-03 §6 so homes with no English reader progress) | reducer tests |
| No microphone | store flavour has none | CI manifest diff |

---

## 3. Product

### 3.1 Onboarding, profiles, locks

1. **"Who is reading?"** Child icon, adult icon; the Sound Teacher asks while Pebble points.
2. **Child** → "Pick your picture" (6 animals, one tap; names the profile). **Me** → set a 4-digit PIN now ("Later" once).
3. **"Help in your language?"** (optional): language names in their own script with the variety's flag ("Português (Brasil)"), device locale first, a big **"Just English"** button. A pack shows its size (~2.5 MB) and downloads in the background; **the lesson starts in English at once**. Never automatic.
4. **First sound.** Before it, one line lists later downloads: "Levels 3–4 about 20–32 MB, Level 5 about 12–18 MB, once. Wi-Fi is best."

- **Doors** appear with **two or more profiles** (two children count) or any adult: Children (picture tiles) and Me. "Add a child" sits there, gated. One child alone opens straight into lessons.
- **Locks**: young child (Track A default) = **picture lock, 2 of 4 pictures in order** (12 orderings; separates siblings, not security); older child optional 4-of-9 shape pattern; 3 misses → 30 s lockout; 10 min idle → doors.
- **Grown-up gate** (a written sum) protects placement, skip, adding a child, mobile-data downloads, lock resets, delete/restore, role change. Forgotten PIN: gate + 24 h.
- **Tabs** as v4 (A: Path · Stories · Practice · Me; B: Lessons · Read · Practice · Progress); the ear icon replays any line.

### 3.2 The English-only instruction set

All learner instructions are **≤60 distinct English lines**, ≤6 words, imperative, each with a **fixed icon**. Pebble **demonstrates each new verb once** (taps, traces, slides a finger, cups an ear) before the learner does it.

| Group | Lines | Examples |
|---|---|---|
| Ritual verbs | 14 | "Listen." (ear) · "Read it to yourself." (eye) · "Tap what it says." · "Say it." · "Slide and say." |
| Exercise intros | 16 | "Which starts with /s/?" (+ sound clip) · "Build the word." · "How many sounds?" |
| Feedback | 10 | "Yes!" · "Try again." · "Listen again." (no "wrong") |
| Check | 6 | "Show what you know." · "Some are made-up words. Sound them out." · "Let's finish tomorrow." |
| Navigation | 8 | "Who is reading?" · "Pick your picture." · "Help in your language?" · "One more?" |
| Handover | 6 | "Show your grown-up." |

### 3.3 Sittings on demand

- The course rule is **one new sound per sitting**, not per day (L1.02). "One more?" offers the next sitting **only if this sitting's mini check met its bar** (default 4/5 first attempts); otherwise tomorrow, and free play now. A grown-up may set a daily cap (D39).
- **Budgets**: Track A ≤8 min, B 10–15 min; lint = audio × 1.5 (assumed); stopwatches on paper (week 1) and app (week 3); 5 samples give a maximum, not a p90.
- **Track A L1.02** (L1.02–L1.04: one trace + one from memory; three traces from L1.05): A /s/ (hear, meet, trace, write, sound game, judged trio) · B /a/ (warm-up ≤3, hear, meet, trace, blend "sa", spell, mini check) · C /t/ (same, blend 4 words, spell "at") · D blend, tricky *a, I*, spell "sat" · E Read it · F Listen & Talk · G Show what you know.
- **The judged trio** (every new-sound sitting, incl. A): three spoken trials, three spoken options, no print ("Which starts with /s/? sun / map / fan"). 3/3 → village piece; otherwise the sound is re-taught first next sitting. A random tapper passes (⅓)³ = 3.7%.
- **Track B** merges into ~3 sittings; after a ≥90% mini check "Keep going?" (offered, never a test).

### 3.4 Exercises and the tap gate

**v1**: E1–E17, E19, E22 (ear), E23 (b/d/p/q) as in v4, plus **E24 letter names** (L1.13: "Its name is *bee*. It says /b/."). v1.1: E18, E20, E21.

**E5, Blend it.** (1) New pattern: modelled once under a growing highlighter. (2) Say each sound, then tap its letter. (3) Slide and say; tap "I said it" (**self-report: the app does not hear you**). (4) **Judged step**: an E6d pick before the word plays. (5) **Repair L1–L3**: the Sound Teacher's partial ("sssaaa"); she adds the last sound aloud; **retry = a fresh item from the same sounds, all four options**. (6) **Repair L4+**: Reader chunks with 350 ms gaps; she blends; fresh item; the Reader's word after the second attempt (same voice).

**E6d grid rule (lead decision 11).**
- Options: **T** (answer), **F** (first position changed), **X** (second axis changed), **FX** (both). Every item varies the first position; the second axis is the **vowel in half the items, the final in the other half**, balanced in real and made-up. *sat* → sat/pat/sit/pit; *mad* → mad/sad/map/sap; *at* → at/it/an/in.
- Each option is one change from two others and two from the third, so the answer is never the unique centre (teacher r4 defect 1).
- Lexicality never mixed; no word twice per check; no 1–2-letter tricky words; C14 review. L3–L4: X changes the target vowel pattern or the ending.
- **Answer and foil clips are recorded in the same session** (§4.5).

**Early-lesson checks (L1.02–L1.04).** Too few letters to fill grids (engineer r4: 48 strings over L1.03's letters, 16 made-up, vs 20 needed). Relaxed rule: **3 options in a chain** (neighbours one change apart), the answer in the middle in a third of items, so "pick the middle" is at chance; lexicality may mix; **repeats across sittings allowed**. Labelled **"early-lesson check"** in data and the grown-up view. The **L1.02 check composition is an app change**: the course has real at, sat, as, at, sat (repeats), 5 made-up, 1 dictation; the app uses 3 real + 5 made-up + 3 dictated. Bar 9/11 as in the course.

**Flow.**
1. Printed word alone; eye icon + "Read it to yourself."
2. Options appear. Window 12 s (L1–L2), 8 s (L3+); after a first timeout, 20 s for the rest of the check.
3. Timeout = not judged; a fresh item (early-lesson: same item, at the end). 3 timeouts: "Let's finish tomorrow."
4. **First miss → a repair that never plays the target**: first-position pick → point to the printed first letter, play its sound; vowel pick → mouth cue + a **non-target** contrast ("pan… pin"); final pick → point to the last letter, play its sound. Then a **fresh item** (early-lesson: same, reshuffled).
5. Second miss → review; only now the whole word plays.
6. **Only first attempts count**, so retry leaks cannot move the gate.

**Ear or eye.** After a vowel pick, an E22 item with non-target words; failing it logs **ear**, not a reading miss. A vowel contrast enters gate options only after **9 non-native listeners (3 each Urdu, Portuguese, Indonesian L1) and 3 native controls** pass that minimal-pair set at ≥90% (week 5).

**Axis rule.** A pass counts only if first-attempt accuracy on **each** axis across the lesson's judged picks (E5 + mini checks, ≥8 per axis) is ≥70%; otherwise it is held and the re-check weights the weak axis 7:3.

**Chance of passing without reading** (E6d is a decoding proxy, not oral reading; L1.03–L1.13: 5 real + 5 made-up + 1 dictation, bar 10/11; independence assumed):

| Learner | Dictation right | Wrong | Unconditional (50/50) |
|---|---|---|---|
| Random or "pick the centre" (¼) | 0.003% | ~0 | ~0.002% |
| First-position-blind (½ every item) | 11/1024 = 1.1% | 0.1% | ~0.6% |
| Vowel-blind (free on 5 final items) | ≥4/5 at ½: 18.8% | 3.1% | ~10.9% |
| Final-blind | 18.8% | 3.1% | ~10.9% |
| Vowel- or final-blind **with the axis rule** (≥7/10 at ½ = 17.2%) | | | **~1.9%** |
| Genuine 90% / 80% reader | ~70% / ~32% first try | | |

- **Trade-off (D40).** The grid fixes the hub leak but varies two positions per item, not three: ~11% for a vowel- or final-blind learner without the axis rule, ~1.9% with it, ~0.04% for "checked twice". Oracles measure it (§6.4).
- **Early-lesson**: random tapper (⅓) passes L1.02 with 3/3 dictation 1.97%; first-position-blind 14.5% (3/3) / 3.5% (2/3). Other classes depend on chain layout; the week-2 oracle run reports them. L1.02 stays the weak spot: delayed re-check, L1.03 re-tests s, a, t.

### 3.5 The Track A world, Stories, free play

- **Pebble**: silent Lottie mascot that **demonstrates gestures**; only the Sound Teacher speaks.
- **Village**: a piece per sound, earned by the judged trio; region-neutral art, checked by testers in Brazil, Indonesia, the USA (week 3). Sticker per sitting, pearl per check.
- **Stories, read-to-me**: every Listen & Talk passage of the current and earlier levels unlocked (13–17 per level). Text shown, **highlight follows the voice word by word**, each chunk's picture **after** it is heard; no picture-first word solving.
- **Tap-read decodables**: no highlighting; no picture until the page is read; a tapped decodable word plays sounds first, the word after an attempt; a non-decodable word plays whole, no credit; taps use **the sentence's voice**.
- **Free play, unlimited**: *hear it*, *segment*, *rhyme*, *letter-name bingo* (from L1.13), and the sound chant. Spoken words and pictures, no print, recorded clips only; never counts toward gates.

### 3.6 Night one and placement

- **Child**: Who → picture → Help → **first sound** (clock: process start → first correct tap). **Quick-start moves after the first sound**: end of Sitting A, 5 E6d items across L1–L2, stops after 2 misses (~25 s), no feedback; 5/5 → Stage 3 tap ladder → placement.
- **Back-fill**: a placed child gets every skipped tricky word (all 24 of L1, plus L2.01–02's, for an L2.03 placement) as E8 review cards within 2 sittings, and skipped GPCs (v/w, x/y/z/qu, b/d/p/q) as ear-and-eye items in the first sitting.
- **Adult (D35)**: **3-minute print-concepts module before /s/** (C1): finger slides left to right, "a letter / a word" (tap the spaces), return sweep. Then the course's fast track, compressed and said so (the course gives A–C ~35 tutor minutes, 10+10+15): taps and tiles, each sound behind a ≥90% mini check before "Keep going?". Target ~18 min. A missed mini check → "Tomorrow you will read your first word"; day 2 retests s, a, t. **Milestone** (not a gate): sat, at, as as early-lesson picks, ≥2 right first time (random 26%). **Fallback** if >20 min for 3 of 5 adults in week 3: print concepts + A + B; "sat" on night two.
- **L1.01 (D29)**: start at L1.02; L1.01's oral games become Hear-it items and a repair.
- **Grown-up placement** (`placement-test.md`, gated) as in v4: Stage 0 not asked aloud (Q3 = the pack choice); Stage 1 helper-judged or skipped; Stage 2 hearing version; Stage 3 E6d tiers of 8+8 ("90% (14+)", though 14/16 = 87.5%); Stage 4 helper-only (Hasbrouck–Tindal Fall 50th: G2 50, G4 94, G6 132 WCPM). The course places a reader who clears Passage C at **Level 6**; v1 has none, so they land in **Level 5 practice** with "Level 6 arrives in an update".

### 3.7 Checks and states

Before the first check, a **10-second wordless demo** (Pebble sounds out a made-up word, shrugs, smiles) + "Some are made-up words. Sound them out." Bars as the course states them: L1.02 9/11; L1.03–L1.13 10/11; ≥4/5 19 times in 10 L1 lessons; L3 "≥90%"; L5 5/8 or 6/9; L6 4/5; most L7 none.

| State | When | Then |
|---|---|---|
| `checked` | bar + axis rule met | next lesson unlocks; "Checked by tapping"; re-check 3 sittings later |
| `rechecked` | re-check passed | "Checked twice"; **reachable with no helper** |
| miss | bar not met | targeted repair next sitting, re-check with fresh items; never sent back |
| `still_learning` | second miss | the next lesson's new-sound sittings unlock; **the missed sounds are not promoted**: they stay "learning", join every warm-up, count in no "words you can read", and get an automatic machine re-check every 3 sittings until two pass (**machine-checked twice**). The grown-up view gives an action, never "needs a person": "Play these 2 sounds together tonight" with buttons; "Listen to her read" only if a helper exists |
| `mastered` | a helper hears her read | optional |

**Review**: 5 Leitner boxes in sittings (1, 2, 4, 8, 16); miss = down one, two in a row = box 1; warm-up ≤3 (A) / ≤6 (B).

### 3.8 Listen & Talk, English-only by default

1. The English passage in chunks (Sound Teacher L1–L3, Reader L4); a picture **after** each chunk.
2. Questions **spoken in English**, answered by tapping one of 3 pictures.
3. The Tier-2 word: **picture + simple English definition + example**, from the course's own Tier-2 bullets; definitions linted to taught words + a high-frequency list (C16).
4. **Then**, only with a helper pack: a one-line gloss of passage and word, **after** the questions, so it cannot leak answers.
5. "Talk" card in helper sessions.

Pilot: ≥80% on English questions, with and without a pack.

### 3.9 Writing, helpers, grown-up view

- **E4**: traces then from memory; scored on start (20% of letter height A, 12% B), stroke count, order, direction, checkpoints, end; b/d/p/q bowl side and stem-first. Formative.
- **Helper sessions** (PIN or gate): read-aloud marking, placement Stages 1 and 4, WCPM, judge's card; an English-reading grown-up sees a visible "I can help" card.
- **Grown-up view** (gender-neutral, English text + icons, pack language optional), per child: "**Tonight, ask them these 3 sounds**" with sound buttons; the latest check as pictures (checked / twice / try tomorrow / still practising: play these together); the village; a "why no pictures beside words?" card. No blended score.
- **Track B**: "words you can read now" plus **real-world unlockables**: each checked lesson unlocks an everyday text from its words (shop sign, bus board, label, form, text message), adult-styled. No village, Pebble or stickers.
- No streaks; reminders opt-in, ≤weekly; comfort settings and slow mode as v4.

---

## 4. Voice

### 4.1 Clips and sizes

**KB per clip, 24 kbps Opus with padding (assumed, conservative)**: word/made-up/option 3.0 (one Kokoro "sat" 2.8; research-02 1.77 trimmed; research-05 2.5) · sentence, Tier-2 12.5 · slow take 5 · phoneme, name, chunk 2.5 · demo 8 · **UI or pack line 6 (≤2 s)** · gloss 9. 3 KB/s.

**Count rules (assumed)**: words = research-05 learner-facing count to ×1.6 (a round-3 tokenizer found ~10% fewer); sentences ±25%; **option clips = 30–60% of slots** (asserted; settled in week 2), made-up foils included; the made-up row is targets only.

**Option slots** (10 items × 3 foils per check): L1–L2 24 checks × 30 × 3 sets + level 360 + placement 288 + L1.02 24 = 2,832 → 900–1,800 clips. L3 17 × 90 + 180 + 144 = 1,854 → 550–1,100. L4 14 × 90 + 180 + 144 = 1,584 → 475–950. **Made-up words**: 55 checks × 2 sets × 5 + 80 + 80 = 710; L1–L2 ~560 (incl. ~250 from the markdown), L3 ~300, L4 ~180 (estimates).

| Sound Teacher | L0–L2 (base) clips | MB | L3 (pack) clips | MB |
|---|---|---|---|---|
| Words | 1,828–2,925 (L1 1,066 + L2 575 + L0 187, ×1.6) | 5.5–8.8 | 442–707 | 1.3–2.1 |
| Made-up | ~560 | 1.7 | ~300 | 0.9 |
| Option clips | 900–1,800 | 2.7–5.4 | 550–1,100 | 1.7–3.3 |
| Sentences | 609–1,015 | 7.6–12.7 | 289–481 | 3.6–6.0 |
| Tier-2 lines (L&T lessons × 2 × 3) | 162 | 2.0 | 102 | 1.3 |
| UI lines | ≤60 | 0.36 | — | — |
| Letter names | 26 | 0.07 | — | — |
| Slow takes / partials | 350–460 + ~200 | 2.4–2.9 | ~150 | 0.75 |
| Sounds: 47 + 6 final stop variants | 53 | 0.13 | — | — |
| Demos + judge's-card examples | 88 | 0.7 | — | — |
| **Total** | **~4,840–7,350** | **~23–35** | **~1,830–2,840** | **~9.5–14.4** |

**Human L0–L3: ~6,670–10,190 clips, ~33–49 MB.**

**Reader L4** (in the L3–L4 pack): words 714–1,142 + earlier words used in L4 texts 500–900 (estimate) + sentences 223–371 + made-up ~180 + options 475–950 + Tier-2 90 (15 × 6) + chunks 400–750 (estimate) = **2,580–4,380 clips, 10.4–17.2 MB**. **L5 practice**: words 938–1,500 + sentences 548–913 + ~200 Tier-2 lines at 12.5 KB = **1,690–2,610, 12.1–18.4 MB**. L6/L7 (v1.1): ~18/11 MB.

**Helper pack**: ≈310 voiced lines + ≈30 notes, **≈2–3 MB** (§7.2).

| Sizes (estimates; measured week 3, final week 8) | Download MB | Installed MB |
|---|---|---|
| Shell: JS, Lottie, Andika, ~355 pictures, ~40 icons | 14–18 | 14–18 |
| Sound Teacher L0–L2 | 23–35 | 23–35 |
| Runtime overhead | — | +3–10 |
| **App install** | **~37–53** | **~40–63** |
| L3–L4 pack (human L3 + Reader L4) | 20–32 | 20–32 |
| L5 practice pack | 12–18 | 12–18 |
| **All of v1** | **~69–103** | **~72–113** |
| Each helper pack | 2–3 | 2–3 |

Plugins: filesystem, haptics, share, file-transfer (`downloadFile` deprecated since 7.1.0); no `.so` in the store flavour. **Pack prompts**: MB, "Wi-Fi recommended", minutes at an assumed 1 Mbit/s, "longer on slow connections" (D36); Wi-Fi-only default; safe to stop; a failed pack says what to do and retries; tested at 200 kbps, three drops.

### 4.2 Reader pipeline

1. **Docker image built in week 0** (research-02: pip hung, espeakng-loader aborted): pinned kokoro, misaki, torch, espeak-ng, threads, `MKL_CBWR=COMPATIBLE`, seed per clip. The guarantee: **an approved clip id is never re-rendered**; the build fails if the hash of its **approved pre-Opus WAV** changes.
2. misaki looks up all L4–L5 words; espeak-ng only proposes; a reviewer approves `pron.json`.
3. `ipa2misaki.py` with symbol round-trip (week 1); chunks rendered from IPA syllables.
4. Re-render loop for misheard made-up words (research-02: vop → "vob"), weeks 6–7. Speed 1.0 only.

### 4.3 One post-process for every clip

1. **Trim** at −45 dBFS (whole burst kept on stop-final words); measure on the trimmed, unpadded clip.
2. **Loudness, computable for every clip.** Clips **≥0.4 s**: −18 LUFS integrated (BS.1770). Clips **<0.4 s** (BS.1770 is undefined below a 400 ms block): **no LUFS requirement**; instead **active-frame RMS** (K-weighted, 10 ms frames, frames within 20 dB of the loudest kept, RMS over them), gained to the word class's mean active-frame RMS. **Q1 uses active-frame RMS for every class**: each class mean (sounds, names, words, options, sentences, UI) within **1 dB** of the sentence mean. Clips trimmed to 0.38–0.45 s are measured both ways; >1 dB disagreement is flagged. The v4 "+6 dB cap" is gone.
3. True-peak limiter −1.5 dBTP after gain; Q1 fails >2 dB of limiting.
4. Padding 40 ms / 80 ms; fades 5 ms; stop-final fade-out ≥15 ms.
5. Pack clips through the same chain at 24 kHz. Opus 24 kbps mono; measured decoded; **hashed as the approved 48 kHz WAV**.
6. One gap: 350 ms, authored in the timeline.

### 4.4 Voice table, QA, handover test

| Moment | Voice |
|---|---|
| Isolated sounds, letter names, sound review cards (any level) | Sound Teacher (core) |
| L0–L3 words, sentences, made-up, options, Tier-2, UI | Sound Teacher |
| L4+ words, sentences, made-up, options, chunks | Reader |
| L1–L3 repair | Sound Teacher partial → learner → fresh item; her word after the 2nd attempt |
| L4+ repair | Reader chunks → learner → fresh item; Reader word after the 2nd attempt |
| Tap inside a sentence | **the sentence's voice** |
| Word review cards | the voice of the word's level |

**Trace test, no exception**: fails any exercise timeline holding both a Sound Teacher and a Reader clip, and any tap whose voice differs from its sentence.

| QA stage | Scope and pass |
|---|---|
| Q1 script | 100%: coverage, padding, class means within 1 dB, ≤2 dB limiting, stop caps, sub-100 Hz flag, per-session drift |
| Q2 ASR round-trip (desktop) | all words, options, sentences; lowest 20% to the reviewer; Gemini only triages |
| Human clips | engineer picks takes; **GA reviewer** hears 100% of sounds (53 × 3), names, demos, made-up words, options; 10% of words and sentences. Reviewer + **second native GA listener (not Kamal)** rate 150 clips incl. **15 planted bad ones**: **both** ICC(2,1) ≥0.75 **and** weighted kappa ≥0.6, planted recall ≥90% each |
| Non-native intelligibility | 5 listeners (Urdu, Portuguese, Indonesian, Spanish, Hindi L1), 100 clips, test-phone speaker: ≥90% identified (4-way choice) |
| Reader clips | 100% of made-up words, made-up options and chunks; 10% of the rest; all overrides; per frozen pack version; 20 planted errors, ≥18 caught |
| Helper packs | native reviewer 100% (§7.2) |

**Reviewer workload (estimate)**: human ~3,000–4,630 clips + Reader L4 ~960–1,650 + L5 ~170–260 = **≈4,100–6,500 ≈ 10–16 h** at an assumed 400 clips/h, plus the 150-clip set; ≤4 h/week, weeks 1–8.

**Handover test (paired).** One 10-item L3 → L4 sequence, L4 voiced by the **Reader** or by the **Sound Teacher** (40-clip human L4 sample, week 5). **16 listeners (8 native, 8 non-native)** hear both, counterbalanced, **on the test phone's speaker**: "Same teacher?" (diagnostic) and "Comfortable to learn from?" (1–5). **Pass, committed with script and stimuli before rating**: paired comfort difference (Reader − human), one-sided 90% lower bound ≥ −0.5. At an assumed SD of 1 the bound is ~0.34 below the mean, so the Reader must land within ~0.16 of the human. Groups reported apart (not powered). **Fail** → D0a-alt for L4 (~14–29 h) or L4 → v1.1.

### 4.5 Sound Teacher and recording chain

- **Audition (week 0)**: three GA candidates; /p t k b d g/ ×3 in both positions; a **timed 2-hour pilot** (words, made-up, options, sentences, stops) giving **clips/h per type and for the second hour** (fatigue); drift thresholds applied. GA reviewer scores accent; 3 blind mixed listeners score pace and warmth against af_heart. No pitch target (af_heart 215–238 Hz, critics-round-2-audio.md).
- **Stops**: "as if the word stopped there, no 'uh'". **Separate initial (*pin*) and final (*cup*) takes**: Meet cards use initial, final-sound repairs final. **No shortest-burst rule**: pick the take whose voicing (/b d g/) or aspiration (/p t k/) is clearest **through the test phone's speaker**. Gate before week 2: blind /b/–/p/, /d/–/t/, /g/–/k/ identification on that speaker, 8 mixed listeners, ≥90%.
- **Per-session drift check, before a session's clips are accepted**: each session opens with room tone, /æ/, 10 words, 1 sentence, compared with session 1: **F0 median ±10%, spectral tilt ±2 dB, speaking rate ±8%**. A breach blocks the clips until the engineer accepts with a note or schedules re-records. Pickups too. **Sessions ≤90 min** (D41).
- **Spec**: pop filter; room ≤ −60 dBFS; peaks ~−12 dBFS; 20–30 cm; 48 kHz 24-bit mono; no AGC, noise suppression or echo cancellation; retake in-session on clipping, thump, noise, click, schwa on a stop, or a live Q1 fail.
- **`voice_studio.py` is a rewrite, week 0, 3 days** (engineer r4: Urdu kinds at :58–120, echo cancellation at :353, 16 kHz import at :497–503): AudioWorklet 48 kHz/24-bit capture, English JSON scripts, numbered takes + selection view, meter, **upload to the engineer**, **live Q1 and drift per take**. Or her own software to the same spec.
- **Answer and foils together**: option sets are generated and reviewed (C14) **before** a level is recorded, so each item's T, F, X, FX share a session.

| Weeks | Content | Clips | h at 150/h | h at 120/h |
|---|---|---|---|---|
| 1 | sounds (53 × 3), names, UI, demos, partials | ~430 | 2.9 | 3.6 |
| 2–3 | L0–L1 | 2,520–3,940 | 16.8–26.3 | 21.0–32.8 |
| 4–5 | L2 | 1,890–2,990 | 12.6–19.9 | 15.8–24.9 |
| 5–7 | L3 | 1,830–2,840 | 12.2–18.9 | 15.3–23.7 |
| **Total** | **L0–L3** | **6,670–10,190** | **~44–68** | **~56–85** |

Peak (weeks 2–3): **8–16 h a week**, 6–11 ninety-minute sessions, near full-time above ~10 h. **If week 0 measures <120/h or she offers <10 h/week, cuts A1–A4 (§8) apply before week 2.** Pickups: week 9.

**Recording engineer (D33)**: reviews uploads within 24 h, picks takes, runs drift checks.

**Licences**: Kokoro Apache-2.0; misaki (check, week 1); perpetual commercial releases from all speakers; Urdu voice per D9; course CC BY 4.0; Andika OFL (verify); Piper unused (lead read the Lessac page as research-only; "clause 3.2" is the lead's reading, research-02 gives none); OpenMoji and the Whistle binary unconfirmed; name unsearched (D37).

---

## 5. Listening

- **v1: none.** No microphone in the store build; read-aloud only in helper sessions.
- **v1.1**: record and replay (practice, gated) and the **Whistle candidate** (research-06: 16.9 MB, CPU, Apache-2.0, arm64/armv7/WASM). Keywords = target + the gate's three options; target with prob ≥ θ → `clear_yes`, an option → `clear_no`, else `unsure`, never yes ("cake" → "Take" at 0.83 when "take" was not a keyword).
- **Lead's desktop test** (Python, adult Kokoro clips): real words recognised (sat 0.63, pin 0.73; "ship" only with biasing). **Made-up words mixed**: blim, strag recognised (0.59–0.60); vop → "VAP"; fraim → "Frame"; chote only with biasing at 0.46. First call 8.9 s, then 0.1–0.25 s. Isolated sounds and letter names failed.
- **Unverified**: child speech, non-native speech, cheap-phone latency and RAM, beam settings, biasing strength, the C API (the test used Python), the engine binary's licence.
- **Separate build flavour**: Gradle flavour `spike` (applicationId `.spike`) carries the plugin and `RECORD_AUDIO`; CI fails if the merged `store` manifest contains it. Scheduled in **week 9 slack**: 30 CVC words × 3 speakers × 2 takes with planted errors; go bar ≥97% `clear_yes` precision, ≤1.5 s p95 on the Android 10 phone.
- **Gold set**: ≥60 items per class, labelled by a native GA speaker (not Kamal); speakers from ≥3 L1s plus native children; precision ≥97%, lower bound ≥92%; thin class = no-go; non-native vowel merges are practice. WCPM (v1.1) from timestamps, "approximate".

---

## 6. Tech

### 6.1 Repo and content

- Copied from `urdu-reading-course/mobile` (PROVENANCE.md): ~12% as-is, 70% changed. New: sitting machine, gate reducer, grid/chain generator, placement + back-fill, Track A world, Stories + free play, grown-up view, profiles/locks/doors, audio clock, pack loader. minSdk 23, targetSdk 36.
- `build_content.py --strict` over 115 files; week-1 exit: coverage + **yield per level** (engineer r4 regex: L1–L4 55/62 parse a Check; L5–L7 0/46). **The option generator runs on the course's own L1.03–L1.08 lists in week 1**, reporting which items fall to the early-lesson rule. Fixes as `app:` YAML PRs (course issue #3).

```jsonc
// content/lessons/L1.02.json (generated, excerpt)
{ "id":"L1.02","checkKind":"early",
  "sittings":{"A":[{"id":"A","new":["s"],"steps":["hear","meet","trace1","write","sound_game","trio"]}, "…"],
              "B":[{"id":"P","steps":["print_concepts"],"once":true},{"id":"ABC","keepGoing":true}, "…"]},
  "pick":{"sat":{"kind":"chain","opts":["tat","sat","sas"],"answerPos":1}},
  "check":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"],"dictation":["at","sat","as"],
           "bar":{"pass":9,"of":11,"courseIssue":1},"composition":"app-change","firstAttemptOnly":true} }
```

**Build gates**: decodability · made-up filter (issue #2) · **option rule** (grid with first position always varied and axes balanced; chains with answer position balanced; lexicality kept outside early-lesson) · pronunciation round-trip · audio coverage + Q1 · bars reachable · budget ×1.5 · no-cueing strings · ≤60 UI lines · sizes within §4.1 +10% · snapshots · pack lint (every pack key exists in the English source).

### 6.2 Audio engine

As v4 (the Urdu `Audio()` never seeks; `WebViewLocalServer.java:369-386` ignores `Range`): fetch sprite + offsets, `decodeAudioData` into `AudioContext({sampleRate:24000})`, schedule with `AudioBufferSourceNode.start(when, offset, duration)`.

**Sprites (engineer r4 fix)**: **step sprites of 20–30 s**, keyed by lesson + step, holding every clip the step can play including tap targets; **decoded on demand**, the next step's during the current one. **Core sprite, always decoded: the 53 sound clips + ≤60 UI lines only.** Pack lines decode per screen; review cards decode their own step's sprite.

**Memory from §4.1 sizes** (Opus 3 KB/s; decoded Float32 mono 24 kHz = 96 KB/s):

| Item | Opus | s | Decoded |
|---|---|---|---|
| Core: 53 × 2.5 KB + 60 × 6 KB | 0.49 MB | ~164 | **~15.8 MB** |
| One 30 s step sprite | 90 KB | 30 | 2.9 MB |
| LRU of 6 (current, next, 3 review, 1 spare) | | | 17.3 MB |
| One decode in flight | | | +2.9 MB |
| **Audio peak (budget)** | | | **~36 MB** |

On a WebView that ignores `sampleRate` (engineer r4: older than Chrome 74) the context runs at 48 kHz and this doubles to ~72 MB, inside the 150 MB app budget. Human L0–L3 audio is ~11,000–16,400 s, so ~370–550 step sprites (estimate).

**Week-1 test at real size**: §4.1-sized sprites; on both phones `dumpsys meminfo` and decode ms on the worst screens (L3 sentence with taps; 3-lesson warm-up). Loopback by **3.5 mm cable into a recorder**: s-a-t → "sat" ×200 under heavy Lottie, p95 gap error ≤15 ms. Tap-to-sound p95 <150 ms on the **speaker route** (recorder at 10 cm).

### 6.3 Data, backup, packs

Stores as v4 + mastery, packs, helperPacks, helper; tested `onupgradeneeded` ladder; progress keyed by lesson id and item text. **Counters live in the progress record** (today `learner.js:41-43` runs stats, streak, pearls via `getAll` every render; streak is deleted).

| Site | Fix |
|---|---|
| **`db.js:44` `fix()`** | coerces any track outside `child\|adult\|heritage` to `child` on every read (Track B adults become children). Enum `A\|B`; test: a B profile survives 100 reads |
| `profiles` | `track A\|B`, `lock picture\|shapes\|none`, `picture`, `pinEveryTime`, `helperPack` (BCP-47 or null) |
| **progress `units` `dict(unitRec, 40, /^\d{1,2}$/)`** | lesson ids fail the regex and 115 lessons exceed the 40-key cap, which `break`s silently. New `lessons: dict(lessonRec, 200, /^L[0-7]\.\d{2}$/)`; overflow throws |
| backup `SCHEMA` whitelist | new stores added to `SCHEMA`, not only `LIMITS` |
| `unit int(0,12)`, `cards.idx`, `cards.kind` | `lesson /^L[0-7]\.\d{2}$/`; `int(0,20000)`; `gpc\|word\|tricky\|tier2\|morph\|lettername` |
| `UI_KEYS`, ids, format | + helperPack, dailyCap; card ids `profileId:kind:sha1(text)[:8]`; `BACKUP_FORMAT="sound-out-1"` |

**Test (week 3)**: deep-equality round trip of a fixture with **61 lessons of progress and 20,000 attempts**, a Track B adult, a picture lock, a pack, the word "don't"; home render ms on the Android 10 phone.

**`helperPack` is read by** the onboarding grid, pack loader, `l1_tags` note filter, grown-up view language, and the Listen & Talk gloss step. Null = English only; every flow defines that case.

**Packs** (level and helper alike): resumed per file; signed ed25519 manifest (D32) checked against `contentVersion`/`gpcHash`. **PWA**: runtime pack cache; lazy base audio with retries; `storage.persist()` result shown. **iPad/iPhone use the PWA** from the Home Screen; Safari may evict storage of sites not added there (WebKit policy, unverified for current iPadOS), so the grown-up view warns. Native iOS is v2.

### 6.4 Devices, budgets, tests

- **D24: two phones** (Android 10, 2–3 GB; Android 13), a 3.5 mm cable, a recorder. WebView floor Chrome 74 preferred; older tested once.
- **Budgets**: as v4 (cold start <2 s, render <100 ms, tap-to-sound p95 <150 ms, gap ≤15 ms, JS <150 KB, memory <150 MB) plus audio ~36 MB, first sound ≤90 s from process start, adult first word ≤~18 min.
- **Auto (green by week 4)**: parser, gates, snapshots; reducer (timeouts, `minJudged`, first attempts, axis rule, `still_learning`). **Oracles on real L1.03–L1.13 and L3 JSON**: perfect decoder reaches L1.06 unaided; first-position-blind ≤1.1%/check; vowel- and final-blind with and without the axis rule (≤2% with); **medoid** (min summed edit distance) and **take-fingerprint** (session id) pickers at 25% ± 5 per item; lexicality picker at chance; 14 s decoder finishes L1.02; **partial-aware guesser** at chance on retries; **reversed reader** fails; random tapper earns 0–1 village pieces in 5 sittings; 80% learner over 13 lessons; L2.03 placement has all 24 L1 tricky words in review within 2 sittings; onset-blind and medoid never placed above L1.06. DOM + audio traces on lessons **and Stories**; every screen works with `helperPack = null`; DB ladder, backup, pack signatures, manifest diff.
- **Device (both phones)**: loopback, tap-to-sound, memory, decode, size, airplane-mode L1, kill-and-resume, 200 kbps with drops.
- **Human** (recruited week 0, ≥3 countries, remote): **no-language first launch** (10 adults + 10 children with no English, PK/BR/ID, no pack, unaided to the first sound); 5 US native children as control; sibling test; grown-up view test (3 non-English-reading parents: "What do you do tonight?"); **Track B screenshot audit, week 3**; vowel (9 + 3) and stop (8) listening tests; stopwatches (paper week 1, app week 3).

---

## 7. Global

### 7.1 English first

- The core is complete in English: instructions (§3.2), vocabulary (§3.8), letter names (E24), Listen & Talk, grown-up view as text + icons.
- **Accent (D15): General American is the app's choice.** The course names none; its placement test accepts /ɒ/ or /ɑ/, and GA /ɑ/ falls inside. No other accent in v1.
- Grown-up view text renders RTL with an Arabic or Urdu pack; lesson screens never mirror.

### 7.2 Helper packs

| Part | ≈ | Content |
|---|---|---|
| UI voice lines | 60 | the instruction set, translated, spoken |
| Grown-up lines | 40 | text + audio |
| Listen & Talk glosses | 177 | 59 L1–L4 lessons × (passage + 2 Tier-2 words), played **after** the questions |
| Interference notes | 20–40 | keyed to `l1_tags` (e.g. Portuguese speakers adding a vowel after a final consonant); on Meet cards and after a matching error |
| **Total** | **≈310 lines + ≈30 notes** | **≈2–3 MB** (estimate), `packs/help-<bcp47>-v<n>/`, signed |

**Recipe, per language**: (1) export the frozen English script with context and max length; (2) draft translation (machine allowed), rewritten by a **native reviewer** for listeners who may not read; (3) notes from a contrastive reference (e.g. Swan & Smith, *Learner English*), approved by a native English teacher; (4) a native speaker records to the same spec (~2–3 h); (5) §4.3 + Q1; the reviewer hears 100%; (6) **field check**: 2 adults who read that language but not English do night one over WhatsApp video, pass = Sitting A without asking; (7) sign, publish. ~2–3 speaker h + ~6–8 translator/reviewer h per pack (D38).

**Which**: **at launch Urdu, Portuguese (Brazil), Indonesian**, because the pilot sites need them. **Wave 1, by Play reach and ESL demand (order is an estimate, to confirm against Play Console data)**: Spanish, Portuguese (BR) ✓, Hindi, Arabic, Indonesian ✓, French, Urdu ✓, Bengali, Vietnamese, Swahili. Punjabi and Pashto speakers get Urdu or English only (a stated limitation).

### 7.3 Compliance and listing

- As v4 (Families, no SDKs, no age, no microphone; COPPA amended 22 April 2026, research-04 §5; "No data collected"; IARC Education), plus: nothing leaves the phone, so GDPR-K, the UK Children's Code, Brazil's LGPD and Indonesia's PDP Law reduce to a DPIA note (our reading, not legal review); closed test ≥12 × 14 days across ≥3 countries; AI-voice disclosure for the Reader; credits for all speakers.
- **Listing**: title "Sound Out: Read English" and short description "Learn to read English with phonics. Kids & adults. Free, offline, no ads." (no Urdu in either). Global keywords as NAME-ASO minus "Urdu to English reading"; each localized listing (pt-BR, id, ur, then wave 1) may carry "<language> to English" in its language. English screenshots with localized caption sets, one showing "Help in your language?". Hooks: offline; works in English alone; adults welcome; free, no ads, no account; no English-reading helper needed; made-up-word checks; never resets. Banned: "proven", "guaranteed", "cures dyslexia", effect sizes, a TYM "RCT", "critical reading", "100 WCPM". D37 before upload.
- **Note for `store/NAME-ASO.md`** (not edited here): change "the word Urdu/Hindi/Arabic-speaking adults search with" to "the word ESL adults worldwide search with"; drop "Urdu to English reading" from global keywords; "screenshots EN + UR" → "EN + localized captions per listing language".

---

## 8. Build plan (10 weeks + week 0; week 9 slack)

**Who**: as v4, plus pack translators, reviewers and speakers (ur, pt-BR, id) and country coordinators (PK, BR, ID, US).

| Week | Deliverables | Exit |
|---|---|---|
| **0** | D-decisions; phones, cable, recorder; recruit lists (≥3 countries); speaker pilots; hires; **voice_studio rewrite**; **Docker image**; paper prototypes | clips/h per type, per hour |
| **1** | Speaker chosen; sounds, names, UI, demos, partials; stop test; parser + yield; **generator on L1.03–L1.08**; L0–L1 options reviewed, text frozen; `ipa2misaki`; **audio test at real sprite size**; **paper stopwatch** (≥2 countries); C1 | sounds pass Q1 + reviewer; gap ≤15 ms; memory measured |
| 2 | Repo; strict parser; generators; L1 options reviewed; sessions L0–L1 words + options together | `npm run content` exits 0 for L1–L2 |
| 3 | Onboarding, doors, locks; DB ladder + db.js fix; backup; step sprites; **paper proxy-validity test** (blind GA teacher, 5 children + 5 adults, ≥2 countries, ≥90%; <80% sends E6d back to critics); **Track B screenshot audit**; L2 frozen; pack scripts out; L1 sentences | **G0** stopwatch; first size; round trip |
| 4 | Exercises, grid + chain, reducer, repairs, axis rule; Track A world; **Stories + free play**; Listen & Talk; L2 words | auto set green |
| 5 | Check + demo; grown-up view; placement + back-fill; helper sessions; vowel validation; **human L4 sample**; L2 sentences, L3 words; **critic round 5** (no-pack L1.02–L1.04 run) | fixtures placed; sibling, grown-up tests |
| 6 | Pack manager; ur, pt-BR, id packs recorded; Reader L4 render + review; **handover test**; L3 sentences | handover pass or fallback |
| 7 | L5 pack; SW cache; L3 QA; re-render loop; pack QA + field checks | L5 oracle; 3 packs pass |
| 8 | Performance, a11y, PWA (incl. iPad), signed APK, final size, human tests | budgets or gap list |
| **9** | **Slack**: pickups (drift-checked), lost-gate re-runs; **Whistle spike in the `spike` flavour** | — |
| 10 | Gauntlet; privacy, Families; listings; closed test; pilot | verdicts |

**Cut list, in order, weeks 2–8.** Audio is the critical path, so audio-hour cuts come first.

| # | Cut | Saves (estimate) |
|---|---|---|
| A1 | Option clips at the 30% distinct ratio (foils reused across checks) | ≤~1,450 clips, ~10–12 h |
| A2 | One extra made-up set per check, not two (L1–L3) | ~390–575 clips, 2.6–4.8 h |
| A3 | **L3 Track B texts voiced by the Reader in v1** (human in v1.1; whole sentences in one voice, taps resolve to it) | ~145–240 clips, 1–2 h |
| A4 | Slow takes for L1 only | ~140–184 clips, ~1–1.5 h |
| 5 | Placement Stages 1 and 4 | — |
| 6 | Judge's card and "mastered" | — |
| 7 | E14 | — |
| 8 | E22 cut to v/w and short vowels | — |
| 9 | Stories tap-read and chant (read-to-me and sound games stay) | — |
| 10 | pt-BR and id packs to the pilot build only | ~4–6 speaker h |
| 11 | L5 practice pack → v1.1 | Reader time |
| 12 | **L3–L4 pack → v1.1** (one pack; v1 gated becomes L0–L2) | **12–19 h at 150/h, 15–24 h at 120/h** |
| 13 | PWA → v1.1 | — |

**Never cut**: L0–L2 Sound Teacher audio, the tap gate, Track A/B skins, **the English-only path**, Track B real-world unlockables.

**Roadmap**: v1.1 L5 MCQ gates, L6–L7, E18/E20/E21, teacher mode, pack sharing, wave-1 packs, Whistle verifier and WCPM if they pass. v2 CTC fallback, FSRS, native iOS.

---

## 9. Risks

| Risk | L | I | Mitigation | Known by |
|---|---|---|---|---|
| L0–L3 recording 44–68 h (150/h) or 56–85 h (120/h); speaker short of 8–16 h/week | High | High | 2-hour pilot; 90-min sessions; A1–A4 before week 2; cut 12 | Week 0 |
| E6d over-credits a vowel- or final-blind learner | Med | High | axis rule (~1.9%), re-check, oracles, week-3 paper proxy test | Week 3 |
| Vowel options test non-native hearing | Med | Med | ear/eye split; 9 + 3 validation | Week 5 |
| Audio memory on 2 GB phones | Low | Med | 30 s sprites, ~36 MB, measured at real size | Week 1 |
| No-language first launch fails | Med | High | Pebble gesture demos; 3-country field test | Week 3 |
| L4 handover disliked | Med | Med | paired test; D0a-alt for L4 or L4 → v1.1 | Week 6 |
| A year of use loses children | High | High | sittings on demand, free play, Stories, grown-up view | Pilot |
| Whistle fails child/non-native speech | Med | Low (v1) | spike flavour, gold set, CTC v2 | Week 9 + |
| "Sound Out" trademark | ? | High | D37 | Before upload |

---

## 10. Decisions for Kamal

| # | Decision | Default | Blocks |
|---|---|---|---|
| **D0a** | Sound Teacher L0–L3 + all isolated sounds; Reader from L4 with chunk repairs, no join. **6,670–10,190 clips; 44–68 h at 150/h, 56–85 h at 120/h** | Confirm | **W0** |
| **D0a-alt** | Human records all v1 (L0–L5), Kokoro dropped: **10,400–16,300 clips; 70–109 h at 150/h, 87–136 h at 120/h** | Alternative | **W0** |
| **D0b** | No speech gate; E6d; Whistle spike in a separate flavour | Confirm | **W0** |
| **D8** | English-only core; launch packs ur, pt-BR, id; wave-1 order confirmed by Play data | Yes | **W0** |
| D9 | Urdu pack voice: Sara terms in writing, or a human | By week 5 | week 5 |
| **D16** | Sound Teacher fee: **44–68 h (150/h) to 56–85 h (120/h)**, 90-min sessions, + pickups | Hire, remote | **W0** |
| **D21** | Pilot: 8 children + 6 adults, ≥3 countries (PK, BR, ID, US), remote | Yes | W0 |
| D23 | GA reviewer, ~10–16 h, ≤4 h/week | Paid | **W0** |
| **D24** | Two phones (Android 10 2–3 GB; Android 13) + cable + recorder | Buy | **W0** |
| **D28** | PIN at first adult launch; picture lock (2 of 4) for young children, shapes optional; doors at ≥2 profiles; grown-up gate; 24 h reset | Yes | week 3 |
| **D35** | Adult night one = print concepts + compressed A+B+C, ~18 min; fallback print concepts + A+B | Yes | W0 |
| **D38** | Helper-pack fees: ~2–3 speaker h + ~6–8 translator/reviewer h each; 3 at launch | Yes | week 3 |
| **D39** | Sittings on demand gated by mini checks; optional daily cap | Yes | week 4 |
| **D40** | Accept the grid trade-off: ~1.9% single-check chance for a vowel- or final-blind learner with the axis rule (~11% without). Alternative: 12-item checks (longer, more clips) | Accept + axis rule | week 2 |
| **D41** | Sessions ≤90 min with the drift gate | Yes | W0 |

**Unchanged from v4, defaults stand**: D15 General American (the app's choice) · D18 Pebble (now demonstrates gestures) · D27 course issues (+ L5 MCQ, L5.16/L7 bars, L4.15, 14/16) · D29 start at L1.02 · D30 L0–L4 gated, L5 practice · D31 first attempts only · D32 Kamal holds the signing key · D33 recording engineer (W0) · D34 second native GA listener (W0) · D36 1 Mbit/s, Wi-Fi default · D37 trademark search before upload.

---

## 11. Content to commission

| # | Item | Owner | By |
|---|---|---|---|
| C1 | Print-concepts module (adult night one; L0 repair) | build agent + author | **week 1** |
| C2 | 710 made-up words + review | build agent + GA reviewer | weeks 1–5 |
| C9 | **English instruction set ≤60 lines** + icons + Pebble gestures | build agent + reviewer | weeks 0–1 |
| C10 | Helper-pack scripts ur, pt-BR, id (~310 lines + ~30 notes each) | translators + native reviewers | weeks 3–6 |
| C12 | Neutral village, Pebble rig, L&T / Stories / answer art (~355), Track B adult art, ~40 icons | art | weeks 2–4 |
| C13 | Recording scripts frozen (L0–L1 wk 1, L2 wk 3, L3 wk 4) | build agent | weeks 0–4 |
| C14 | Option sets checked for rude, obscure, confusable words | build agent + reviewer | weeks 1–4 |
| C16 | English Tier-2 definitions linted + one picture each | build agent + reviewer | week 4 |
| C17 | Track B real-world unlockables, one per L1–L4 lesson, region-neutral | author + art | week 4 |
| C18 | Free-play item sets (hear it, segment, rhyme, bingo) | build agent | week 4 |

Unchanged from v4: C3 placement forms B/C (wk 5) · C4 lexicon + `heartIdx` (wk 2) · C5 `pron.json` (wks 1–6) · C6 mouth cues, phonetician sign-off (wk 4) · C7 `app:` YAML (wks 2–4) · C11 L5 MCQ, L6–L7 (v1.1) · C15 course tickets (wk 2).

---

## 12. How we will know it works

**Metrics, on the phone only**: E6d first-attempt accuracy per axis; checked / twice / mastered; `still_learning`; ear vs eye; timeouts; Listen & Talk with and without a pack; sittings per day; free-play minutes; returns after a gap; dropout.

**Pilot (week 10, 6 weeks, remote).** 8 children: Pakistan 2 (Kamal's two), Brazil 2, Indonesia 2, USA 2 native; ≥3 with a parent who cannot read English. 6 Track B: Pakistan 2 (a shop worker; an adult who cannot read Urdu), Brazil 2, Indonesia 2. Recruited by country coordinators over WhatsApp; builds via Play internal test; consent forms; recordings deleted after scoring.

**Proxy validity, twice**: **week 3 on paper prototypes** (§8), and in the pilot after L1.04 (~18 sittings) and L1.06 (~30) for children, L1.04 and L1.08 (~21) for adults, by recorded WhatsApp video to a blind GA teacher; ≥90% agreement. (L1.08 for a child at one sitting a day is 42 sittings, exactly the 6 weeks with no slack, so children stop at L1.06.) Also: placement forms A/B; weekly Listen & Talk; grown-up interview; L4 handover question; English-only vs pack users.

**v1.1 bar**: every child advances unaided; proxy ≥90%; ≥10/14 practising in week 6; no Track B "childish" reports; no no-pack first-launch failure; zero freezes, zero cueing.

| Gate | Compared with | Test |
|---|---|---|
| G0 Night one (pass/fail) | stopwatch | first sound ≤90 s from process start for an English child **and** a no-English child with no pack; adult first word ≤~18 min (else D35 fallback); relaunch ≤10 s |
| G1 Child week one | Duolingo ABC | judged blending; sittings on demand; no adult; delight |
| G2 Play loop | Teach Your Monster | village, Stories, free play; oracles; repairs |
| G3 Parent view | Khan Kids | tonight's 3 sounds; no dead ends; sibling-proof; sizes at install |
| G4 Adult dignity | Learning Upgrade | first word; print concepts; unlockables; PIN at start |
| G5 Audio | Sara | clarity, warmth, drift; stops on a phone speaker; class spread ≤1 dB; handover test |
| G6 Proxy validity | blind teacher | ≥90% in week 3 and pilot; oracle table |
| G7 Rule audit (pass/fail) | DESIGN.md §2 | every §2 row, rules 1–12 |

---

## Appendix: sources

- Repo `sound-out/`: `plan/` (research, critics r1–r4, bar, decisions.tsv, plan-v1–v4), `store/NAME-ASO.md`.
- Course `/home/oye/Documents/free_work/english-reading-course/`: DESIGN.md (L1–L4 sequence; L1.13 letter names; L4.12–14 syllables), `placement-test.md`, 108 lessons + 7 mastery checks, `tools/decodable.py`, issues #1–3.
- Urdu app `/home/oye/Documents/free_work/urdu-reading-course/`: `mobile/src/content.js`, `db.js:44`, `backup.js` (`units` cap 40), `learner.js:41-43`, `scripts/voice_studio.py` (:58–120, :353–357, :497–503), `mobile/package.json`.
- Capacitor `WebViewLocalServer.java:369-386`; external URLs as research-01–06.
