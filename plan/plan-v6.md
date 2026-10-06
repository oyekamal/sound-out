# Sound Out: the app plan, v6 (consolidation)

Date: 2026-10-06. Owner: Kamal. Repo `oyekamal/sound-out`. Play title "Sound Out: Read English", package `com.oyekamal.soundout`.
- **What v6 is**: v5 plus lead decisions (13)–(17) and the round-5 defects, consolidated. `v6-changes.md` maps each one.
- **Evidence**: `plan/research/` 01–06, `english-reading-course` (DESIGN.md, 108 lessons, `placement-test.md`), `plan/bar/`, `plan/critics/`, and the prototype in `app/` and `tools/` (reference only; this plan does not count it as built).
- **Labels**: "unverified" (the source said so), "estimate" (ours), "budget" (a target), "assumed" (an input we chose). **Nothing here is measured yet.**

---

## 0. Summary, decisions, the pause

Sound Out is a free, offline Android app (plus a web app) that teaches anyone to read English from the first sound. The core needs no home language: **one English voice**, icons, pictures and demonstrated gestures carry every instruction. Home-language help is an optional **helper pack**.

- **v1 scope**: gated Levels 0–4. **Level 5 practice moves to v1.1** (decision 13 re-estimate, §8). A **fresh codebase** (decision 13): the Urdu Qaida repo is reference for patterns only; no code is copied.
- **Night one**: a child taps "A child", picks a picture, and taps the first sound **≤90 s from process start**; she meets two sounds that night, then free play. An adult who reads a Latin-script language (**B-Latin**) reads "sat" in **≤12 min**; a new reader (**B-new**) does a print-concepts module and reads "as" in **≤15 min**. All are budgets.
- **Learned means remembered tomorrow** (decision 14): new sounds are capped per calendar day, and nothing counts as learned until a next-day retrieval passes.
- **The tap gate (E6d)**: read a printed word silently, tap which of four spoken words it says; options form a 2×2 grid (§3.4). Early lessons use an **early check** (sound → letter, plus 3-option blend-and-pick).
- **Not in v1**: accounts, ads, analytics, microphone.

### D0: one voice, end to end (decision 16)

No hybrid and no voice change anywhere. The week-1 voice spike decides between:
- **(a) Kokoro-only.** Every clip is rendered by Kokoro-82M `af_heart`. Isolated sounds, partial blends, onset+rime pieces and syllable chunks are **sliced from Kokoro's own word renders** using its predicted phoneme durations, so they are the same voice by construction. Evidence to judge: `tools/slice_phonemes.py` and the prototype's `app/public/listen.html`, which plays sliced sounds beside IPA-direct renders. Cost: compute plus review; no speaker.
- **(b) One human speaker records everything.** v1 (L0–L4): **~8,000–12,500 clips ≈ 53–83 h at 150 clips/h, 66–104 h at 120/h**; adding L5 later: +1,690–2,610 clips (+11–17 h / +14–22 h). Cost: a paid speaker, an engineer, a drift gate, a text freeze per level.

**How it is decided**: Kamal listens to the listen page on the test phone; 8 mixed native/non-native listeners do forced-choice identification of the sliced sounds and 40 chunks on Opus-decoded clips through the phone speaker. (a) wins if Kamal accepts it **and** every sound class and the chunk set reach ≥90%; otherwise (b). The evidence for (a) is unproven: research-02 §5's Gemini judge failed /s/ /ʃ/ /θ/ /æ/ (and research-02 says the judge may be at fault), and no human has rated slices yet.

### D0b: listening

v1 has no speech gate and no microphone. Sherpa-onnx keyword spotting cannot return yes/unsure/no; CTC scoring was "10–15 working days before any kid data" (critics-round-2-engineer.md line 15). This reverses research-03 §7's v1 speech witness; research-04 D6 had already deferred ASR, and v6 drops helper-judged read-aloud as the gate. The Whistle verifier (research-06) is a spike in a **separate repo**, outside the v1 schedule (§5).

### After v6 the plan gauntlet pauses (decision 17)

Five critic rounds have narrowed the plan to questions only data can settle. Next: the **prototype**, **Kamal's own playtest**, and these **week-1 spikes**. Each answers named open questions:

| Spike | When / who | Answers |
|---|---|---|
| S1 Voice | week 1; Kamal + 8 listeners, test phone | D0: are Kokoro slices (sounds, chunks, onset+rime) clear and the same voice? |
| S2 Overnight retention | weeks 1–2; prototype with Kamal's children + 3–5 adults | Does next-day retrieval track same-day scores? Is 2 new sounds/day right (§3.3)? |
| S3 Night-one length | week 1; stopwatch on the prototype from process start | First sound ≤90 s; B-Latin "sat" ≤12 min; B-new "as" ≤15 min (D35) |
| S4 Option pools | week 1; `tools/gen_options.py` on L1.02–L1.13 | Grid-able targets per lesson; early-check feasibility; the generated made-up count (§4.1) |
| S5 Tap-gate validity | weeks 1–3; oracles on real JSON, Monte-Carlo, paper proxy test (blind teacher), hidden-print listening test | Is a tap pick ≥90% in agreement with reading aloud? Do lexicality, medoid and fingerprint pickers sit at chance? The real axis-rule figure (§3.4) |
| S6 Audio clock and memory | week 1; both Android phones | Clip-store decode time, peak memory at real size, gap p95 ≤15 ms |
| S7 No-English full check | week 3; 10 adults + 10 children, ≥3 countries incl. Mexico and one non-Latin-script country | Can someone with no English finish a whole check, incl. the made-up-word idea, from icons and demos? |
| S8 Pack on mobile data | week 3; 3 parents on data only | Time from choosing a language to its first spoken line |
| S9 iPhone web app | pilot; borrowed iPhone | Ringer-switch muting, Opus vs AAC decode, storage after an 8-day gap |

Kamal's playtest answers the one question no spike can: is it worth coming back to tomorrow.

### The bar (features: Duolingo ABC, Khan Kids; play: Teach Your Monster; pedagogy: DESIGN.md; audio: Sara clips)

| Sound Out v1 | Duolingo ABC | Khan Kids | Google Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes | parent email account* | Yes | iOS $8.99 | $4.99/mo |
| Offline | "Offline Learning" | partial | after download | not documented | no evidence |
| Adult path | No | No | No | No (ages 3–6) | multi-level adult-to-child (research-01; 3.2/5 on justuseapp) |
| Placement | No | age/performance path* | No | not found | not found |
| Made-up-word gate | not found | not found | not found | not found ("progress by guessing", one review) | not found |
| Home-language help | No | Spanish read-to-me (bar JSON) | several languages (research-01) | No | a few onboarding languages |

\* Common Sense reviews fetched by critics in rounds 1 and 5, not in research-01 or the bar JSON. "Read Along" is Google's app (research-01), not `bar/Read_Along_Kids_Books.json` (a different app). US iOS: Khan 4.80 (131,337 ratings, 201 MiB); ABC 4.25 (3,810, 212 MiB); TYM 4.47 (29,802, 96 MiB).

---

## 1. Who it is for

**Promise:** "A few minutes a day, and more play whenever you want. Starts at the first sound. Works in English alone, with help in your language if you want it. Offline, free, private, never starts you over, and no one who reads English has to help."

**Time to the end of L4** (estimate; 61 lessons from L1.02):

| Path | Sittings | 1 a day | 2 a day |
|---|---|---|---|
| Track A child, ~6/lesson, ≤2 new sounds/day | ~366 | ~12 months | ~6 months |
| B-new adult, ~3/lesson, ≤2 new sounds/day | ~183 | ~6 months | ~3 months |
| B-Latin adult, ~1.5–2/lesson, ≤3 new sounds/day | ~92–122 | 3–4 months | 1.5–2 months |

No age is collected. A grown-up may give any child the Track B skin.

### 1.1 Five people, night one

| | Ayesha, 5, Rawalpindi; mother reads no English | Lívia, 6, Recife; father reads Portuguese | Emma, 5, Ohio; native, knows letter names | Rukhsana, 35, Rawalpindi; reads Urdu only | Budi, 29, Jakarta rider; reads Indonesian |
|---|---|---|---|---|---|
| Path | Track A + Urdu pack | Track A + Portuguese pack (on mobile data) | Track A, Just English | **B-new** + Urdu pack | **B-Latin** + Indonesian pack |
| Night one | /s/, /a/ (judged trio each, name + capital shown), cap reached → Stories and sound games | same | quick-start 2/5 → /s/, /a/; names match what she knows | print module → /s/, /a/ → reads "as", ≤15 min; PIN after | s, a, t in one sitting, names day 1 → reads "sat", ≤12 min; PIN after |
| Day 2 | warm-up retrieval of s, a first | same | same | retrieval of s, a | retrieval of s, a, t |

Sibling fixture: Hamza, 8, own profile; quick-start 5/5 → ladder → L2.03, skipped tricky words back-filled (§3.6).

---

## 2. The pedagogical engine

| Level | Lessons | Notes (heading-level greps) | v1 |
|---|---|---|---|
| 1 | 14 | Blend 13, Listen & Talk 14, Track B 12; L1.13 letter names review | gated |
| 2 | 14 | L&T 13, Track B 13 | gated |
| 3 | 18 | L&T 17, Track B 17 | gated |
| 4 | 16 | Blend 14, L&T 15, Track B 15; L4.12–14 syllables and word attack | gated |
| 5 | 16 | free-response checks | v1.1 practice |
| 6–7 | 30 | no Track B | v1.1 |

69 tricky words (L1 24, L2 29, L3 16) in `data/heart.json`, shown as "tricky words" (A) or "words to remember" (B). **Tier-2 words: 73** (auditor r5 per-lesson grep: two per lesson in L1, one in L2–L4: ≈28 + 13 + 17 + 15).

| DESIGN rule | How | Check |
|---|---|---|
| 1 No cueing | no picture beside an unread word anywhere; the picture (= meaning) appears only after the word is decoded and picked; no repair plays the target before the retry | DOM test; audio trace between miss and retry |
| 2 Decodable (L1–L4) | taught GPCs, scheduled tricky words, ≤2 flagged story words | `decodable.py` |
| 3 Blend before spell | step order | snapshot on real JSON |
| 4 Mastery gate | lesson bar on judged first attempts; course issue #1 | reachability + oracles |
| 5 Heart words, never flashcard drilling | tricky words are reviewed only as E8 maps (find the irregular part, then read the word in a phrase); the Leitner `tricky` card opens an E8 item, never a flash recall | lint: no `tricky` card renders a bare-word flash screen |
| 6 Two registers | `read.B` or `sameAsA` | parser + child-word lint |
| 7 Comprehension daily | picture-word meaning after decoding; Listen & Talk (§3.8) | coverage + the muted-audio test (§3.8) |
| 8 Two metrics | decoding and comprehension never blended | schema + grep |
| 9 L1 notes | only in helper packs, keyed to `l1_tags` | tag + pack lint |
| 10 Pause-safe, no streaks | "skip" = take the lesson's check first, gated | kill/resume ×20 |
| 11 Multisensory optional | guided tracing, skippable (unscored in v1) | settings test |
| 12 Research claims cite research/0X; nothing invented | every number in this plan, the store copy and the in-app "why" cards carries a source tag (research file, course file or "estimate"); the claims auditor checks them before release; a banned-claims grep runs on store copy | source-tag lint; auditor pass |
| Machine never promotes mastery or an unretrieved sound | "learned" needs next-day retrieval; "mastered" needs a helper | reducer tests |

---

## 3. Product

### 3.1 Onboarding, profiles, locks

1. **"Who is reading?"**: a child icon and an adult icon, spoken in English. No mascot on this screen.
2. **Child** → "Pick your picture" (one tap). Pebble appears only from here. **Adult** → "Can you read this?" with two tiles: **"I read another language in these letters"** (sample "a b c" letters, a book icon) → B-Latin; **"I am new to reading"** → B-new.
3. **"Help in your language?"**: chips with each language's name in its own script; tapping a chip plays a **pre-recorded greeting in that language** (bundled in core, ~15 KB each). **"Just English" is a flag-free globe icon** with a spoken English line. A chosen pack shows an icon, its size as a number (e.g. "2.2 MB") and a spoken line in the pack's own language; a second tap downloads it. **Packs under 5 MB download on any connection**; level packs (17–27 MB) say "Wi-Fi is best" by icon and spoken line, and mobile data needs a grown-up confirm.
4. **First sound.** For an adult, the **PIN is offered after the first word**, not before.

- **Doors** with two or more profiles (two children count): Children (picture tiles) and Me (plain icon, no animals).
- **Locks**: picture lock (2 of 4 in order) for young children, shapes optional; 10 min idle → doors. **Grown-up gate**: a written sum; it keeps out young children, not an 8-year-old (parent r5), so deleting a profile also needs the adult PIN when one exists.

### 3.2 English-only instructions, and the six that cannot be mimed

≤60 English lines in the one voice, ≤6 words, each with a fixed icon; Pebble demonstrates each verb once (Track A). Track B uses the same icons and a short animated hand, never Pebble. Six instructions cannot be mimed and get extra support (global r5):

| Instruction | Icon | Demo before the first judged item | Pack line |
|---|---|---|---|
| "Some are made-up words. Sound them out." | word with a question mark | 3 worked items: a made-up word is sounded out, its picture slot stays empty, the pick is still praised | yes |
| "Read it to yourself." | eye + closed mouth | finger slides under the word, mouth closed, then the tap | yes |
| "Which starts with /s/?" | arrow at a word's start | 2 worked items stretching the first sound ("ssss-un") | yes |
| "Let's finish tomorrow." | moon | the screen dims to night, the path shows tomorrow's spot | yes |
| "Help in your language?" | globe + speech bubbles | each chip greets in its own language | — |
| Tricky words | word with a star on the odd part | one E8 map shown before the first tricky word | yes |

### 3.3 Sittings, spacing, retrieval (decision 14)

- **One new sound per sitting** (course), and **new sounds capped per calendar day: 2 for Track A and B-new, 3 for B-Latin** (B-Latin meets 3 per sitting, so one new-sound sitting a day). After the cap, "One more?" offers **review, Stories and sound games, unlimited**.
- **Mini check**: 5 items, bar **4/5 first attempts**, the course's own early bar (≥4/5 appears 19 times in 10 L1 lessons). Stated once; it applies to every track. **A first miss never ends the night**: one more try on a different item set; a second miss → "tomorrow" (with free play still open).
- **Next-day retrieval**: the first warm-up on a later calendar day asks yesterday's sounds (sound → letter and one blend pick per sound). A sound is **learned** only when it passes (≥2 of 3 first attempts). A failed sound is re-taught first that day, and that day's new-sound cap drops by one.
- **Judged trio** in every new-sound sitting (3 spoken trials, 3 options, random 3.7%): a **sprout** appears in the village; it grows into the sound's piece after next-day retrieval.
- **Leitner in calendar days** (1, 2, 4, 8, 16). A re-check is ≥2 days after the check.
- **Budgets**: Track A sitting ≤8 min, Track B 10–15 min; spike S3 measures them.

### 3.4 Exercises and the tap gate

**v1 exercises (17)**: E1 sound game · E2 Meet card (**lowercase + capital, sound as the tool, name as the label**: "This is s, capital S. Its name is ess. It says /s/." from L1.02) · E3 sound tap · **E3b sound → letter** ("tap the letter that says /s/") · E4 guided trace + write from memory (unscored in v1) · E5 blend · E6d tap gate · E7 spell with tiles · E8 tricky-word map · E9 reader + questions · E10 Listen & Talk · E11 check · E12 Leitner card · E13 morphology (L4) · E22 ear (v/w, short vowels) · E23 b/d/p/q · E25 picture-word (meaning after decoding). v1.1: E14–E21 (fluency, L5, helper WCPM, reciprocal teaching, record-and-replay).

**E5 repairs, by word type** (never the whole target before the retry; the retry is always a fresh item with all options):
- CVC and blends (L1–L2): successive blending from a partial ("sssaaa…"), the learner adds the last sound.
- One-syllable words with a digraph or vowel team (L2–L4, e.g. "coin"): **onset + rime** ("c · oin"), in the exercise's one voice, then tile-building of the word's spelling.
- Multi-syllable (L3–L4): syllable chunks ("gar · den") with the 350 ms gap.
In (a) all pieces are slices of the word's own Kokoro render; in (b) they are the speaker's.

**E6d grid (L1.05 onward).** Options T (answer), F (first position changed), X (vowel in half the items, final in the other half), FX (both). Each option is one change from two others, so the answer is never the unique centre. Lexicality never mixes; no word twice per check; C14 review. Answer and foils share a recording or render batch.

**Early check (L1.02–L1.04), labelled "early check".** The letter sets cannot fill grids. Build-time enumeration (engineer r5, `/usr/share/dict/american-english` as oracle): **L1.02** over {s, a, t}: "sat" has two neighbours (tat, sas); **"at" and "as" have one neighbour each (each other)**. **L1.03** (s a t p i n): **≈11 made-up strings**, 7 grid-able; 22 real, 16 grid-able. **L1.04** (+m d): ≈33 made-up, 23 grid-able. So early checks use:
- **sound → letter items** (3 options from taught letters, upper- or lowercase);
- **blend-and-pick with 3 options**, same lexicality; the third option may be two changes away (e.g. the reversal "ta" for "at"), and no centring is claimed;
- an item that cannot get two same-lexicality options becomes a sound → letter item;
- repeats allowed only on a different day.
`tools/gen_options.py` prints, per lesson, pool size, grid-able targets and distinct strings, and the build fails when a check needs more than the pool.

**Flow**: printed word alone; eye icon + "Read it to yourself"; options; window 12 s (L1–L2), 8 s (L3+), 20 s after a first timeout; timeout = not judged, fresh item; first miss → targeted repair (letter pointed to, its sound; vowel → mouth cue + a non-target contrast) → fresh item; second miss → review, and only then the whole word. **Only first attempts count.** Ear or eye: after a vowel pick, an E22 item; failing it logs "ear", not a reading miss. A vowel contrast enters gate options only after the **vowel panel** passes it at ≥90%: 12 non-native listeners (3 each Spanish, Urdu, Portuguese, Indonesian L1) and 3 native controls.

**Axis rule.** A pass counts only if each axis reaches ≥70% across the lesson's judged picks (≥8 per axis).

**Chance of passing without reading** (L1.05–L1.13: 5 real + 5 made-up + 1 dictation, bar 10/11):

| Learner | Dictation right | Wrong | Unconditional (50/50) |
|---|---|---|---|
| Random tapper (¼) | 0.003% | ~0 | ~0.002% |
| First-position-blind (½ each item) | 1.1% | 0.1% | ~0.6% |
| Vowel- or final-blind, no axis rule | 18.8% | 3.1% | ~10.9% |
| Vowel- or final-blind, axis rule | | | **~1.6% to ~6%** |

The axis-rule range: **~1.6% assumes 8 extra axis picks independent of the gate** (bar 6/8 at ½ = 14.5%; 10.9% × 14.5%); **~6% if the axis picks include the gate's own items**. Independence is an assumption; spike S5 runs a Monte-Carlo on the real JSON. If the measured figure is above 3%, checks move to 12 items (D40). "Checked twice" by chance is then ~0.03–0.4% (independence again assumed). Next-day retrieval adds another filter, not modelled.

**Early check, random tapper**: 10 items at ⅓; L1.02 (bar 9/11, dictation right) needs ≥8/10 = 0.34%; L1.03–L1.04 (10/11) need ≥9/10 = 0.036%. Other strategies are measured by oracles at build.

### 3.5 Track A world, Stories, free play

- **Pebble**, a silent mascot that demonstrates gestures; **Track A only**.
- **Village**: a sprout per sound, a piece after next-day retrieval; sticker per sitting; region-neutral art tested in BR, ID, MX, US.
- **Read-to-me**: all Listen & Talk passages of the current and earlier levels; **sentence-level highlight** following the voice; each chunk's picture after it is heard.
- **Tap-read decodables**: unlocked after that lesson's pick; no highlighting; no picture until the word or page is read. An "attempt" is a pick or a tile step: a tapped decodable word plays its sounds, then asks a 3-option pick, then the picture; a non-decodable word plays whole with no credit.
- **Sound games, unlimited**: hear it, segment, rhyme, letter-name bingo (from L1.02, with capitals), sound chant. No print in sound games; never counts toward gates.

### 3.6 Night one and placement

- **Child**: Who → picture → Help → first sound (clock from process start). Quick-start after the first sound: 5 E6d items across L1–L2, stops after 2 misses; 5/5 → Stage 3 ladder → placement. **Back-fill**: skipped tricky words become E8 items within 2 sittings; skipped GPCs become ear-and-eye items on day 1.
- **B-Latin** (≤12 min, budget): no print module; s, a, t with names and capitals in one sitting; blend; read "sat" (early check picks, ≥2 of 3 first time, a milestone not a gate); PIN offered; day 2 retrieves s, a, t.
- **B-new** (≤15 min, budget): 3-minute print module (left to right, letter vs word, return sweep; for readers of a right-to-left script the direction part is the core); /s/; /a/; read "as"; PIN offered. Fallback if spike S3 shows >15 min for 3 of 5: /s/ and the print module only, "as" on night two.
- **Placement** for grown-ups follows `placement-test.md` as in v5. Stage 4 uses Hasbrouck–Tindal Fall 50th percentile (G2 50, G4 94, G6 132 WCPM), **US native-speaker norms**. A reader who clears Passage C is placed by the course at Level 6; v1 places them at the end of L4 with "more levels arrive in an update".

### 3.7 States

| State | When | Then |
|---|---|---|
| `practised` | the check's bar and the axis rule are met today | next lesson's new-sound sittings unlock |
| `checked` | next-day retrieval of 5 check items (fresh variants) passes | "Checked" |
| `rechecked` | re-check ≥2 days later passes | "Checked twice"; reachable with no helper |
| miss | bar not met | targeted repair next sitting, re-check on a later day |
| `still_learning` | second miss | the next lesson's sittings unlock; missed sounds stay unlearned, join every warm-up, and get a machine re-check every 2 days until two pass |
| `mastered` | a helper hears her read | optional |

### 3.8 Meaning and Listen & Talk (decision 15)

- **Core vocabulary = picturable words.** After a decodable word is picked correctly, its **picture appears as its meaning** (allowed by rule 1, because it comes after decoding). Every L1–L4 noun, verb and adjective with a clear picture gets one (C12).
- **Listen & Talk**: the English passage in chunks, a picture after each chunk, then 3-picture questions. The course's questions are open oral inference; **picture questions are an app departure**, authored separately (C19), and their answer pictures differ from the chunk pictures.
- **Abstract Tier-2 words** (e.g. "generous", "precise"): with a helper pack, **the home-language gloss plays BEFORE the questions** (passage gloss + word gloss); without a pack they are **deferred and counted as not taught**, and the grown-up view lists them as "waiting for a language pack".
- **Comprehension score** counts only for learners with a pack or who chose "Just English". Others' Listen & Talk is labelled listening practice.
- **Picture-match test**: 5 no-English adults answer with audio muted and the passage hidden; above ~45% means the item is a picture match and is rewritten.

### 3.9 Grown-up view, Track B

- **Grown-up view**, per child: what was learned (only next-day-retrieved sounds), the village, and **play-and-compare**: the app plays a sound, the child repeats it, the grown-up taps "same" or "not sure". It is labelled **encouragement, not a test**, and never feeds a gate. For English-reading grown-ups, an "I can help" card opens helper sessions. A "why no pictures beside words?" card explains rule 1.
- **Track B**: no Pebble, no village, no stickers, no animal icons anywhere. "Words you can read now", plus **real-world unlockables** built only from taught shapes, capitals included (lint).
- No streaks; reminders opt-in, ≤weekly.

---

## 4. Voice (D0: one voice)

### 4.1 Clips and sizes (identical content under (a) and (b))

**Per-clip KB, 24 kbps Opus with padding (assumed, conservative)**: word/made-up/option 3.0 (research-02 measured 1.77 trimmed; research-05 2.5 incl. ~0.4 KB container) · sentence, Tier-2 line 12.5 · slow take 5 · sound, name, slice piece 2.5 · demo 8 · UI or pack line 6 · gloss 9. 3 KB/s.

**Rules (assumed)**: words = research-05 learner-facing count to ×1.6 (round-3 tokenizer found ~10% fewer); sentences ±25%; option clips = 30–60% of option slots; made-up foils are in the option row.

**Two sets per check, not three.** Each check has the course's set plus one generated set for the re-check (a later day); later re-checks repeat items across days. Option slots: L1–L2 = 3 early checks × 10 × 2 foils × 2 + 22 × 10 × 3 × 2 + level 240 + placement 288 = **1,968 → 590–1,180 clips**; L3 = 17 × 60 + 120 + 144 = 1,284 → 385–770; L4 = 14 × 60 + 120 + 144 = 1,104 → 330–660.

**Made-up targets: ~720** = course markdown 5 per check (56 checks = 280) + generated 5 per check (275) + level 80 + placement 80, ≈ 715; split L1–L2 ~330, L3 ~210, L4 ~180. C2 commissions the generated ~435 plus review of all ~720. Early-lesson pools are smaller (§3.4), so S4 may lower this.

| | L0–L2 (base) | | L3 | | L4 | |
|---|---|---|---|---|---|---|
| | clips | MB | clips | MB | clips | MB |
| Words | 1,828–2,925 | 5.5–8.8 | 442–707 | 1.3–2.1 | 714–1,142 | 2.1–3.4 |
| Made-up | ~330 | 1.0 | ~210 | 0.6 | ~180 | 0.5 |
| Option clips | 590–1,180 | 1.8–3.5 | 385–770 | 1.2–2.3 | 330–660 | 1.0–2.0 |
| Sentences | 609–1,015 | 7.6–12.7 | 289–481 | 3.6–6.0 | 223–371 | 2.8–4.6 |
| Tier-2 lines (73 words × 3: 41 / 17 / 15) | 123 | 1.5 | 51 | 0.6 | 45 | 0.6 |
| UI lines; letter names | 60; 26 | 0.4 | — | — | — | — |
| Slow takes; partials | 350–460; ~200 | 2.4–2.9 | ~150 | 0.8 | — | — |
| Sounds (47 + 6 final-stop variants); demos | 53; 88 | 0.8 | — | — | — | — |
| Onset+rime; syllable chunks | — | — | — | — | 300–500; 400–750 | 1.8–3.1 |
| **Total** | **~4,260–6,460** | **~21–32** | **~1,530–2,370** | **~8–12** | **~2,190–3,650** | **~9–14** |

**v1 total ~7,980–12,480 clips.** L5 (v1.1): 1,690–2,610 clips, 12–18 MB.

**Helper pack**: 60 UI + 40 grown-up + **132 glosses** (59 passage glosses + 73 Tier-2 glosses) = **232 lines** + 20–40 notes ≈ **2.2 MB** of audio (estimate), plus a font subset for non-Latin scripts (§7.2).

| Sizes (estimates) | Download MB | Installed MB |
|---|---|---|
| Shell: ~8 MB code and Lottie (research-05) + pictures and icons 6–10 MB (assumed ~17–28 KB each) | 14–18 | 14–18 |
| Base audio L0–L2 | 21–32 | 21–32 |
| Runtime overhead | — | +3–10 |
| **App install** | **~35–50** | **~38–60** |
| L3–L4 pack | 17–27 | 17–27 |
| **All of v1** | **~52–77** | **~55–87** |

### 4.2 The two options side by side

| | (a) Kokoro-only | (b) One human speaker |
|---|---|---|
| Production | render all ~8.0–12.5k clips; slices (sounds, partials, onset+rime, chunks) cut from word renders by predicted durations, 5–10 ms crossfades at zero crossings | record all ~8.0–12.5k clips; pieces recorded (or sliced from her takes, cut 1) |
| Effort | ~1–3 CPU hours per full pass at 1.3–2 clips/s (engineer r5 rate); re-render loops for misheard made-up words (research-02: vop → "vob") | **53–83 h at 150/h, 66–104 h at 120/h**, 90-min sessions; peak ~9–17 h/week over weeks 2–7; engineer take-picking ~16–25k takes (estimate) |
| Pipeline | pinned Docker image built in week 0 (research-02: pip hung, espeakng-loader aborted); approved clip ids never re-rendered; build hashes the approved 24 kHz WAV | `voice_studio` built fresh (48 kHz/24-bit raw capture, numbered takes, upload, live Q1); build hashes the approved 48 kHz WAV |
| Audition | none | 3 candidates, two 90-min sessions in one day plus one the next; accepted clips/h reported |
| Stops | sliced bursts judged by S1 | separate initial (*pin*) and final (*cup*) takes; picked for burst/VOT cues on the phone speaker (the voicing bar sits below its roll-off) |
| Consistency | same model, same voice, same seed rules | **drift gate** (§4.4), (b) only |
| Disclosure | AI voice disclosed in the listing | speaker credited |
| Main risk | slices sound clipped or unnatural; made-up words misheard | hours, fatigue, availability; text freezes per level |

### 4.3 One post-process

1. Trim at −45 dBFS (whole burst kept on stop-final words).
2. **Loudness, one measure for every clip**: K-weighted active RMS over the loudest 100 ms window. Each clip within **±1.5 dB of its class target**; class targets (sounds, words, sentences, UI) set by ear on the test phone in week 1. No LUFS path.
3. True-peak limiter −1.5 dBTP; Q1 reports limiting per clip; >2 dB → the clip is re-gained to its class floor and flagged, not failed silently.
4. Padding 40/80 ms; fades 5 ms; stop-final fade-out ≥15 ms; one 350 ms gap in timelines.
5. Opus 24 kbps mono; measured decoded.

### 4.4 QA (one voice)

- **Voice-id check**: every clip in the core and level packs carries the same voice id; the build fails otherwise. Helper-pack lines are a **separate pack voice** and play only on their own card, outside exercises.
- **Q1** (script, 100%): coverage, padding, loudness window, limiting report, slice click check, sub-100 Hz flag.
- **Q2** ASR round-trip (desktop) on words, options and sentences; the lowest 20% go to the reviewer. Gemini only triages.
- **GA reviewer**: 100% of sounds, slices, made-up words and made-up options; 10% of the rest. Reviewer + a second native GA listener (not Kamal) rate 150 clips including 15 planted bad ones: **both** ICC(2,1) ≥0.75 and weighted kappa ≥0.6, planted recall ≥90% each.
- **Non-native intelligibility**: 5 listeners (Spanish, Urdu, Portuguese, Indonesian, Hindi L1), 100 clips, phone speaker, ≥90% in 4-way choice.
- **Reviewer workload, re-summed** (estimate): first pass ~3,600–5,800 clips + Q2 second pass ~1,200–2,000 + re-review of ~10% re-made clips + 150-clip set ≈ **14–22 h**, ≤4 h/week over weeks 2–8 (32 h).
- **Drift gate, (b) only**: a fixed 60-second sheet at session open **and close**; pYIN median F0, 1/3-octave long-term spectrum 100 Hz–8 kHz, syllables per second, SNR, tail-based reverb estimate, each against the audition baseline; a breach blocks the session's clips; a waiver needs a second person's sign-off and flags them. Validated by flagging a deliberately degraded copy of the audition.
- **Pack speakers**: each auditioned by 5 listeners (warmth, pace).

### 4.5 Licences

Kokoro Apache-2.0; misaki (check); speaker releases perpetual and commercial; course CC BY 4.0; Andika OFL (Latin only); Noto fonts (OFL) for non-Latin packs; Piper unused (lead's reading of the Lessac page: research-only); OpenMoji unconfirmed; name unsearched (D37).

---

## 5. Listening

- **v1: none.** No microphone anywhere in the store app.
- **v1.1 candidate: Whistle** (research-06: 16.9 MB, CPU, Apache-2.0; real words recognised, made-up words mixed (blim, strag yes; vop → "VAP"; fraim → "Frame"; chote only with biasing at 0.46); 8.9 s first call, then 0.1–0.25 s; isolated sounds and letter names failed; tested in Python, not the C API). Unverified: child and non-native speech, cheap-phone latency, binary licence.
- **The spike lives in a separate repo** (`sound-out-whistle-spike`, its own app id). The store app never depends on it, so `cap sync` cannot link the plugin and no `RECORD_AUDIO`, plugin class or `.so` can reach the store AAB. CI on the store repo checks the merged manifest and `unzip -l` of the AAB. It runs outside the 10-week schedule; its gold set needs ≥60 items per class before any go decision.
- v2: CTC fallback (~10–15 days, engineer r2).

---

## 6. Tech (fresh codebase, decision 13)

### 6.1 Content pipeline

`tools/parse_course.py` and `tools/gen_options.py` (prototype) grow into the strict pipeline: parse 115 files; yield per level (engineer r4: L1–L4 55/62 lessons parse a Check, L5–L7 0/46); per-lesson option pools; made-up generation with the real-word filter (course issue #2). Fixes go back as `app:` YAML PRs (issue #3).

**Build gates**: decodability · made-up filter · option rule (grid from L1.05; early-check rules L1.02–L1.04; pool ≥ need) · voice-id · audio coverage + Q1 · bars reachable · sitting budget · no-cueing strings · ≤60 UI lines · unlockables from taught shapes · source tags (rule 12) · pack lint.

### 6.2 Audio: clip store and clock

- **Clip store, no duplication** (research-05): per lesson, one file of concatenated complete Ogg Opus streams plus an offset index; each step has a manifest of clip ids. Shipped MB = unique MB.
- Each clip is a Blob slice decoded with `decodeAudioData` into `AudioContext({sampleRate:24000})`; clips are scheduled with `AudioBufferSourceNode.start(when)` on the audio clock (needed because the WebView's local server ignores `Range`, engineer r3).
- **Decode-ahead**: the next step's clips decode during the current step. A **check step holds one option set**: 10 items × 4 options × ~1 s + dictation and repairs ≈ ≤60 s. The re-check set is on another day, never co-resident.

| Memory (decoded Float32, 96 KB/s) | s | MB |
|---|---|---|
| Core: 53 sounds × 2.5 KB + 60 UI × 6 KB | ~164 | 15.8 |
| Current step (≤60 s) + next step (≤60 s) | 120 | 11.5 |
| Review clips (≤30 s) | 30 | 2.9 |
| **Peak (budget)** | | **~30** |

On a WebView that ignores `sampleRate` (older than Chrome 74, engineer r4) the context runs at 48 kHz: ~60 MB. Spike S6 measures decode ms and `dumpsys meminfo` at real size on both phones, plus the loopback gap test (3.5 mm cable into a recorder, p95 ≤15 ms) and tap-to-sound on the speaker route.

### 6.3 Data (designed fresh)

- **IndexedDB stores**: profiles (`track: A|B-Latin|B-new`, lock, picture, helperPack), sessions, attempts (lesson id, item text, first attempt, axis, day), cards (Leitner box, due **date**), progress (per lesson: state, counters, so home renders read one record), mastery, packs, helper.
- Versioned `onupgradeneeded` ladder from v1 onward, tested against fixtures.
- **Backup/restore**: a versioned JSON (`sound-out-1`) with a schema per store and no key caps.
- **Test**: deep-equality round trip of a fixture with 61 lessons, 20,000 attempts, every track, a pack, the word "don't"; render ms on the Android 10 phone.

### 6.4 Packs, web app, devices, tests

- **Packs** (level and helper): resumed per file; an **ed25519-signed manifest verified in JS** with `@noble/ed25519` (~5 KB gzip, estimate; needs BigInt, Chrome 67+; SHA-512 via WebCrypto). It is unit-tested on the oldest WebView in the floor (Chrome 74) and inside the 150 KB JS budget. A failed pack says what to do and retries.
- **Web app** (PWA): pack cache; lazy base audio; `storage.persist()`. **iOS** is the web app, **tested on a borrowed iPhone in the pilot** (S9). If Opus fails in Safari, the server ships an AAC `.m4a` variant to Safari only (research-05). If the iPhone test fails, the iOS claim is dropped.
- **Devices (D24)**: Android 10 (2–3 GB) and Android 13 phones, a 3.5 mm cable and a recorder; a borrowed iPhone in the pilot.
- **Budgets**: cold start <2 s, render <100 ms, tap-to-sound p95 <150 ms, gap ≤15 ms, JS <150 KB gzip, memory <150 MB, audio ~30 MB.
- **Auto tests**: reducer (first attempts, axis rule, day cap, next-day retrieval, `still_learning`); a perfect bot running 10 hours gets ≤2 new sounds and no `checked` that day; oracles on real JSON (first-position-blind, vowel/final-blind, medoid, fingerprint, lexicality, reversed reader, partial-aware guesser, random tapper's village); the axis-rule Monte-Carlo; placement back-fill; DOM and audio traces (lessons and Stories); voice-id; English-only path with no pack; DB ladder, backup, pack signature.
- **Human tests**: S2, S3, S5, S7, S8, S9; sibling test; grown-up view test (3 parents with no English: "what do you do tonight?"); Track B screenshot audit (count child-coded assets: target 0); vowel panel; listening tests in §4.4.

---

## 7. Global

### 7.1 English first

The core is complete in English. **General American is the app's default**, not a claim of neutrality: a learner in Kenya, Nigeria, India, the UK or Australia hears GA with American spelling. The course's L1.05 mouth cue describes a rounded British /ɒ/; C6 adapts it to GA /ɑ/ (a departure, signed off by the phonetician).

### 7.2 Helper packs, priced per language

| Part | ≈ |
|---|---|
| UI lines | 60 |
| Grown-up lines | 40 |
| Glosses (59 passages + 73 Tier-2 words), played before questions | 132 |
| Interference notes (`l1_tags`) | 20–40 |
| Greeting sample (in core) | 1 |
| Audio | ~2.2 MB |
| Font subset, non-Latin scripts only (Noto Sans Devanagari, Noto Naskh Arabic, Noto Nastaliq Urdu, Noto Sans Bengali; OFL) | ~0.1–0.5 MB (estimate) |

**Production per language (estimate)**: speaker 2–3 h (after a 5-listener audition); translation draft + native review 6–8 h; notes drafted from a contrastive reference and approved by a native English teacher 1–2 h; field check with 2 adults who read that language but not English 2 h; **localised Play listing** (title, short and long description, captions, keyword research from native search data) 2–3 h; non-Latin script: font subsetting and layout QA +2–4 h. **≈13–19 person-hours + 2–3 speaker hours per Latin-script pack; ≈15–23 + 2–3 for non-Latin.**

**Launch set, by Play reach** (order is an estimate to confirm against Play Console data, not chosen by the owner's contacts): **Spanish, Portuguese (Brazil), Hindi, Indonesian, Arabic, Urdu**: three Latin-script packs (es, pt-BR, id) and three with a script font (hi, ar, ur) ≈ **84–126 person-hours + 12–18 speaker hours**. Later: French, Bengali, Vietnamese, Swahili. Speakers of Punjabi, Pashto and other unlisted languages use English only or a related pack.

### 7.3 Compliance and listing

- As v5: Families; no SDKs; no age; no microphone; "No data collected"; DPIA note covering GDPR-K, the UK Children's Code, LGPD and Indonesia's PDP Law (our reading, not legal review); closed test ≥12 × 14 days across ≥3 countries; AI-voice disclosure if (a).
- **Listing**: English title "Sound Out: Read English" and short description "Learn to read English with phonics. Kids & adults. Free, offline, no ads."; **a localised listing for every launch-pack language** (e.g. es-419 with a Spanish title and "aprender inglés" search terms), priced in §7.2. Banned claims as v5. NAME-ASO needs no keyword change (global r5: it already has no Urdu keyword); screenshots get localised caption sets.

---

## 8. Build plan (fresh codebase; 10 weeks + week 0; week 9 slack)

**Staffing**: the build agent (Claude Code) full-time, Kamal reviewing ~1 h a day; human contributors per §4 and §7.2.

**Module effort, from scratch (estimate, engineer-weeks)**:

| Module | Weeks |
|---|---|
| Content pipeline, generators, lints | 1.0 |
| Clip store + audio clock | 0.5 |
| IndexedDB, migrations, backup | 0.5 |
| Day scheduler (cap, retrieval, Leitner in days) | 0.5 |
| Profiles, locks, doors, PIN, gate | 0.5 |
| 17 exercise types, gate reducer, repairs | 2.0 |
| Track A world (Lottie village, stickers), two skins | 0.5 |
| Stories + sound games | 0.5 |
| Placement + back-fill | 0.5 |
| Grown-up view incl. play-and-compare | 0.25 |
| Service worker, pack manager, signature check | 0.75 |
| Onboarding, language grid, pack loader | 0.25 |
| Guided tracing (unscored) | 0.25 |
| **Total** | **8.0** |

Weeks 1–8 hold exactly 8.0, so the margin is week 9 alone. **To make it fit, these move to v1.1**: Level 5 practice (E16, E17, E19, L5 pack), E14, E15, E18, E20, E21, stroke-scored tracing, placement Stages 1 and 4 (helper parts), judge's card and "mastered" marking, WCPM. Prototype code in `app/` may be promoted after review, but it is not counted as done.

| Week | Deliverables | Exit |
|---|---|---|
| 0 | D-decisions; phones, cable, recorder; recruit lists (PK, BR, ID, MX, US + one non-Latin-script country); (b) speaker shortlist held in reserve; Docker image; paper prototypes | dated recruit lists |
| 1 | **Spikes S1, S3, S4, S6; S2 starts**; pipeline; **D0 decided at week end** | spike results committed |
| 2 | Generators, lints; DB, scheduler; (a) render + review L0–L2, or (b) recording starts | L1–L2 content builds |
| 3 | Profiles, onboarding, locks; **S5 paper proxy test, S7, S8**; S2 result; Track B audit; exercises start | G0 stopwatch |
| 4 | Exercises, reducer, repairs; Track A world | auto tests green |
| 5 | Check flow, placement, Stories, sound games; vowel panel; **Kamal playtests an L1.02–L1.04 build** | playtest notes |
| 6 | Service worker, pack manager; es, pt-BR, id packs; L3–L4 audio | pack tests pass |
| 7 | hi, ar, ur packs with fonts; grown-up view; localised listings; audio QA | packs pass field checks |
| 8 | Performance, a11y, web app, signed APK | budgets or gap list |
| 9 | **Slack for one gate failure** | — |
| 10 | Release checks; closed test; pilot | — |

**Gate failures and what each costs**:

| Gate | Fails → | Cost | Absorbed by |
|---|---|---|---|
| S1 voice: (a) rejected | (b) | 53–104 recording h over weeks 2–7 (9–17 h/week) | cuts 1–2, then cut 8 (L3–L4 → v1.1) is likely |
| S3 night-one length | fallbacks in §3.6 | ~1 day | week 9 |
| S4 pools too small | more sound → letter items | ~1 day | week 2 |
| S5 proxy <90% (≥80%) / <80% | 12-item checks / gate redesign | 2 days / ~1 week | week 9 |
| S6 memory or gap | smaller steps; floor raised | 2–3 days | week 9 |
| S7 instructions fail | rework demos and icons | 3 days | week 9 |
| S2 retention poor | cap 1 new sound/day | ~0 build; slower pace | — |
| Vowel panel | contrast excluded | 0 | — |
| S9 iPhone | iOS claim dropped | 0 | — |

Week 9 absorbs one failure, not two; a second failure triggers the cut list.

**Cut list, in order**:
1. (b) only: pieces sliced from her takes (saves ~1,050–1,600 clips, ~7–13 h).
2. Option clips at the 30% ratio (up to ~1,300 clips; in (b) ~9–11 h).
3. Slow takes for L1 only.
4. E22 cut to v/w and short vowels.
5. Stories tap-read (read-to-me and sound games stay).
6. Launch packs cut to es, pt-BR, id; hi, ar, ur move to v1.1.
7. Web app → v1.1 (drops the iOS claim).
8. **L3–L4 pack → v1.1** ((b): saves ~3,720–6,020 clips, 25–40 h at 150/h, 31–50 h at 120/h).

**Never cut**: L0–L2 audio, the tap gate and early check, next-day retrieval, both skins, the English-only path, Track B unlockables.

---

## 9. Risks

| Risk | L | I | Mitigation | Known by |
|---|---|---|---|---|
| Kokoro slices unusable and (b) needs 53–104 h | Med | High | S1 in week 1; cuts 1, 2, 8 | Week 1 |
| Tap pick ≠ reading | Med | High | S5 proxy, oracles, axis Monte-Carlo, next-day retrieval | Week 3 |
| Children forget overnight | Med | High | day cap, next-day retrieval, S2 | Week 2 |
| No-English learner lost in the first check | Med | High | six instructions demoed; S7 | Week 3 |
| Schedule: 8.0 weeks of build in 8 | High | High | week 9; v1.1 list; cut list | Weekly |
| Audio memory | Low | Med | clip store, ≤60 s steps, S6 | Week 1 |
| Pack quality ×6 and fonts | Med | Med | per-pack audition, review, field check | Week 7 |
| iOS web app | Med | Low | S9; AAC fallback; claim dropped if it fails | Pilot |
| Year-long dropout | High | High | free play unlimited, sprouts, grown-up view | Pilot |
| Trademark | ? | High | D37 | Before upload |

---

## 10. Decisions for Kamal

| # | Decision | Default | Blocks |
|---|---|---|---|
| **D0** | One voice: (a) Kokoro-only with sliced pieces, or (b) one human for everything (53–83 h at 150/h, 66–104 h at 120/h) | decided by S1 with you listening | end of week 1 |
| D0b | No speech gate; Whistle spike in a separate repo, outside v1 | Confirm | W0 |
| **D8** | Launch packs by Play reach: es, pt-BR, hi, id, ar, ur; later fr, bn, vi, sw | Yes | W0 |
| D9 | Urdu pack voice: human speaker (Sara only with written licence terms) | Human | week 5 |
| **D16** | (b) only: speaker fee for the hours above, 90-min sessions | Shortlist now, hire only if (b) | week 1 |
| **D21** | Pilot: 10 children (PK, BR, ID, MX, US, 2 each) + 8 adults (PK B-new 2, BR, ID, MX B-Latin 2 each), remote, one borrowed iPhone | Yes | W0 |
| **D24** | Two Android phones + cable + recorder; borrow an iPhone for the pilot | Buy / borrow | W0 |
| **D28** | Picture lock for young children; PIN offered after the adult's first word; deleting a profile needs the PIN | Yes | week 3 |
| **D35** | Night one: B-Latin "sat" ≤12 min; B-new "as" ≤15 min; mini-check bar 4/5; first miss = one more try | Yes | W0 |
| **D38** | Six launch packs ≈ 84–126 person-hours + 12–18 speaker hours, incl. listings and fonts | Yes | week 3 |
| **D39** | New sounds ≤2/day (A, B-new), ≤3/day (B-Latin); learned = next-day retrieval | Yes | W0 |
| **D40** | Axis rule (1.6–6%, independence assumed); switch to 12-item checks if S5's Monte-Carlo shows >3% | Yes | week 3 |
| D41 | (b) only: drift gate at session open and close | Yes | if (b) |
| **D42** | Fresh codebase, 8.0 engineer-weeks; L5 practice and the §8 list move to v1.1 | Yes | W0 |
| **D43** | The plan gauntlet pauses after v6; next = prototype, your playtest, spikes S1–S9 | Yes | now |

Unchanged from v5: D15 General American (now "the app's default") · D18 Pebble (Track A only) · D27 course issues · D29 start at L1.02 · D31 first attempts · D32 Kamal holds the signing key · D33 recording engineer, (b) only · D34 second native GA listener · D36 1 Mbit/s for level-pack minutes · D37 trademark search.

---

## 11. Content to commission

| # | Item | Owner | By |
|---|---|---|---|
| C1 | Print-concepts module (B-new; direction for right-to-left readers) | build agent + author | week 1 |
| C2 | ~435 generated made-up words; review of all ~720 | build agent + GA reviewer | weeks 1–5 |
| C6 | 44 mouth cues; GA /ɑ/ for L1.05 | art + phonetician | week 4 |
| C9 | ≤60 English lines, icons, demos incl. the six unmimeable instructions | build agent + reviewer | weeks 0–1 |
| C10 | Six helper packs (232 lines + notes each) + fonts | translators, native reviewers, speakers | weeks 3–7 |
| C12 | Pictures: picturable L1–L4 words (meaning after decoding), L&T chunks, answers; Track A art; Track B adult art; icons | art | weeks 2–5 |
| C14 | Option sets checked for rude, obscure, confusable words | build agent + reviewer | weeks 1–4 |
| C16 | English Tier-2 definitions (73 words) | build agent + reviewer | week 4 |
| C17 | Track B unlockables from taught shapes (capitals included) | author + art | week 4 |
| C18 | Sound-game item sets | build agent | week 4 |
| **C19** | Picture questions for Listen & Talk (an app departure from the course's open oral questions) | author | week 4 |
| C20 | Localised listings for each launch pack | per-language reviewer | week 7 |

Unchanged: C3 placement forms B/C · C4 lexicon + `heartIdx` · C5 `pron.json` · C7 `app:` YAML · C11 L5 MCQ checks (v1.1) · C13 scripts frozen per level ((b) only) · C15 course tickets.

---

## 12. How we will know it works

**Metrics, on the phone only**: E6d first-attempt accuracy per axis; **same-day vs next-day accuracy per sound**; checked / twice / mastered; `still_learning`; ear vs eye; Listen & Talk with and without a pack; sittings and free-play minutes per day; returns after a gap; dropout.

**Pilot (week 10, 6 weeks, remote)**: 10 children and 8 adults (D21) in PK, BR, ID, MX, US; one borrowed iPhone; country coordinators on WhatsApp; Play internal test; consent; recordings deleted after scoring. Proxy validity: a blind GA teacher scores recorded read-alouds of tapped items after L1.04 and L1.06 (children) and L1.04 and L1.08 (adults); she first rates 20 accent-only clips so accent is not scored as error. **Next-morning retrieval** of yesterday's sounds, blind-scored, against same-day mini-check scores.

**v1.1 bar**: every child advances unaided; proxy ≥90%; next-day retrieval ≥80% of same-day; ≥12/18 practising in week 6; no Track B "childish" reports; no no-pack first-check failure in S7 or the pilot; zero cueing.

**Release gates (on the built app, week 10)**: G0 night one (pass/fail: first sound ≤90 s; B-Latin ≤12 min; B-new ≤15 min) · G1 child week one vs Duolingo ABC · G2 play loop vs Teach Your Monster · G3 grown-up view vs Khan Kids · G4 adult dignity vs Learning Upgrade · G5 audio vs Sara (one voice, slices, loudness window) · G6 proxy validity · G7 rule audit (pass/fail, rules 1–12).

---

## Appendix: sources

- `sound-out/`: `plan/` (research, critics r1–r5, bar, decisions.tsv rows 1–17, plan-v1–v5), `store/NAME-ASO.md`, prototype `app/` and `tools/` (`slice_phonemes.py`, `gen_options.py`, `parse_course.py`, `app/public/listen.html`).
- `english-reading-course/`: DESIGN.md, `placement-test.md`, 108 lessons + 7 mastery checks, `tools/decodable.py`, issues #1–3.
- The Urdu Qaida repo is reference only and is not cited for code.
