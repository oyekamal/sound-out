# Read English: the app plan, v2

Date: 2026-10-05. Owner: Kamal. Board task #118 (project english-reading-course).
v2 rebuilds v1 after critic round 1 (teacher, parent+adult, engineer, audio, auditor) and the lead's seven decisions. `v2-changes.md` maps every finding to the change. Evidence: research-01 to research-05, `english-reading-course/DESIGN.md` and the lesson files, `course/level-0/placement-test.md`, `bar/*.json`, and critics-round-1-*.md. Labels kept: "unverified" means the source said so; "estimate" means this plan made the number.

---

## 0. Summary and the bar

**Summary.** Read English is a free Android app (with a PWA twin) that teaches anyone, a 5-year-old or a 60-year-old, to read English, starting from the first sound. It runs the 108-lesson, 8-level course in `english-reading-course` on a copy of the Urdu Qaida app shell (Capacitor 7, Vite, IndexedDB, Leitner, pearl path, feel.js).

- **First launch.** The learner taps who is reading (two picture cards, spoken in Urdu and English). The first lesson starts on the next screen. The first letter sound is heard and tapped within 90 seconds. Placement is opt-in.
- **Tracks.** Children get Track A, everyone else Track B. Both run one engine with the same sequence and the same gates.
- **Blending.** The learner produces it: sound by sound, then the whole word. An on-device verifier checks the word by comparing the audio against the target word and a handful of likely mistakes, using sherpa-onnx inside a native plugin.
- **Progress without a reading adult.** When the verifier says "clearly right" on the real-word set, and a later sitting confirms it, the lesson becomes `secure` and the next one unlocks. No adult who reads English is needed. A helper can upgrade a lesson to `mastered`, but never has to.
- **One voice.** Words and sentences are spoken by Kokoro-82M `af_heart`, pre-rendered at build time. The 44 phonemes and the blending demos come from one human speaker chosen for a voice match to af_heart. The speaker is bandwidth- and loudness-matched to it, and the join is tested on naive parents in week 1.
- **Privacy.** Audio never leaves the phone. No account, no ads, no analytics.

On why the phonemes are human: in our bakeoff, judged only by Gemini Flash with no human listen, neither tested engine produced a clean isolated /s/ or /θ/. This is unverified by a human, and it is why the week-1 spike includes a human listen before the speaker is booked (research-02 §5, §9).

**The bar.** Features: Duolingo ABC and Khan Academy Kids. Interaction: Teach Your Monster. Pedagogy: DESIGN.md. Audio: the ElevenLabs Sara clips (RESUME.md). The brief adds Google Read Along and Learning Upgrade.

| We ship | Duolingo ABC | Khan Academy Kids | Google Read Along | Teach Your Monster | Learning Upgrade |
|---|---|---|---|---|---|
| Free, no ads, no account | Yes | Yes (Khan needs an email-verified parent account, per the parent critic's Common Sense fetch) | Yes | No: iOS $8.99 (bar json) | No: $4.99/mo up to $59.99/yr (research-01) |
| Fully offline | Listing has an "Offline Learning" section; current builds not tested | Partial: downloaded books and games | Yes, after download | Not documented | No evidence found |
| Adult track on the same sequence | No (preschool to grade 2) | No (2–8) | No (5+) | No (listing: ages 3–6) | Yes, but songs and video, 3.2/5 on justuseapp |
| Placement and skip-ahead | No: "No option to skip ahead" (Common Sense) | not found | No | not found | not found |
| Gate on real **and** pseudowords | not found | not found | not found | not found; reviews say children "can progress by guessing" | not found |
| Learner produces blending, app checks it | Speech in some games, mixed reviews | not found | Listens to story reading, not decoding | No speech | not found |
| Runs to critical reading (L5–L7) | No ("very simple short stories") | Stops near grade 2 | Story practice only | Phonics phases 2–5 | Partial |
| First-language support for the English code | No | Read-to-me in English or Spanish | Urdu story language, no code teaching | No | Spanish and a few onboarding languages |
| Install (iOS file size, bar json) | 212 MB | 201 MB | not verified | 96 MB | not verified |

"Not found" means absent from research-01 and the listings, not proven absent. Duolingo ABC's listing says "over 700 hands-on lessons", while Common Sense counted 127 units. We report both and do not reconcile them. Store data (US iOS): Khan 4.80 on 131,337 ratings. Duolingo ABC 4.25 on 3,810, last updated 2023-08-02. Teach Your Monster 4.47 on 29,802. Reading Eggs 4.70 on 7,369. `bar/Read_Along_Kids_Books.json` is a different product (Smart Kidz Club). Google Read Along facts come from research-01 only.

Our install matrix (§4.1) is about 54–94 MB for one ABI with listening, plus about 54 MB of optional level packs. That is not like-for-like with iOS file sizes, and we say so in the listing.

---

## 1. Who it is for, and the promise

**Promise:** "Ten minutes most days. Starts at the first sound. Works offline, costs nothing, knows nothing about you, never makes you start over, and you don't need anyone who reads English to help."

Time honesty: a Level 1–4 lesson is about 6 child sittings or 3 adult sittings. The real figure is computed per lesson by the week-2 budget lint (§3.2), so a 14-lesson level is roughly 84 or 42 sittings. The parent summary states this.

### 1.1 Five archetypes, night one

| | Ayesha, 5, Urdu at home | Leo, 7, native English | Bilal, 14, hides not reading | Rukhsana, 35, stall worker | Nana Karim, 60 |
|---|---|---|---|---|---|
| Phone | Mother's; mother does not read English | Father's | His own, at night | Hers, between customers | His, shared with grandson |
| Launch screen (spoken in Urdu + English) | Mother taps the child card | Father taps the child card | Taps "Me" | Taps "Me" | Taps "Me" |
| Next screen | L1.02 Sitting A, Track A. "sun… s-s-s-un", then letter s, tap it. Under 90 s | Same. Father taps "I can already read some English" for him later | L1.02 A, Track B (no mascot). He taps "I can already read some English" | L1.02 A, Track B. Urdu instructions spoken on every screen | L1.02 A. He taps "I can already read some English" |
| Placement (opt-in, §3.4) | none | Later, with father: Stage 2 Block A 26/26, Block B misses th → **L2.03** | Stage 3 Tier 1 = 13/16, below 14 → **L1.02** per the file's rule; mini-check streaks fast-track him | none | Block A 26/26, Block B misses sh → **L2.01** |
| What is stored | Nickname chosen at "stop here" | — | — | Comfort: large text | Comfort: large text, slow-word mode |

No one hears a spoken question about their reading history on night one.

### 1.2 Their first month (illustrative, computed from the sitting ratio)

- **Ayesha** (1 sitting a day, about 30): L1.02–L1.06. Her blending is checked by the verifier. Lessons become `secure` without her mother judging anything. The grown-up page says "Checked by the app" per lesson. If the verifier spike fails, the cut path applies (§5.7) and the page says "Checked by tapping. We'll check again soon".
- **Leo** (5–6 sittings a week, Track A, 6 per lesson): 20–26 sittings, about L2.03–L2.06. His father may judge in helper sessions to upgrade lessons to `mastered`.
- **Bilal** (5 a week, Track B, 3 per lesson): about 20 sittings. Fast-track streaks let him merge sittings, so about L1.02–L1.08. No notifications. A neutral icon and name.
- **Rukhsana** (4 a week, interrupted): about 16 sittings, L1.02–L1.06. Each interruption resumes on the same screen. The print-concepts module (C1) is offered from the Me tab if she taps the "new to reading" icon. A price list unlocks at the end of Level 1.
- **Nana Karim** (5 a week): L2.01–L2.06 or so. His grandson has a child profile. Nana's adult profile is hidden behind the gate on the launch screen (§3.1).

---

## 2. The pedagogical engine

### 2.1 The course mapped to the app

Block coverage was counted over all 108 lesson files on 2026-10-05 (string match on headings and labels; the week-1 parser report replaces it).

| Level | Lessons | Template | Blocks present (files with block / lessons) | Exit gate (DESIGN.md §3) |
|---|---|---|---|---|
| 1 First Sounds | 14 | lesson | Hear/Meet/Blend/Spell 13, Read 14, Listen & Talk 14, Track B 12, Check 14 | CVC real + pseudo ≥90% |
| 2 Sounds Together | 14 | lesson | Blend 13, Listen & Talk 13, Track B 14, Check 14 | CCVC/CVCC + 2-syllable ≥90% |
| 3 Long Vowels | 18 | lesson | Blend 17, Listen & Talk 18, Track B 17 | VCe / vowel-team ≥90%, ~40 WCPM equivalent |
| 4 The Full Code | 16 | lesson | Blend 14, Listen & Talk 15, Track B 15 | multisyllabic pseudowords ≥90% |
| 5 Word Power & Fluency | 16 | session | Retrieval 16, Word work 15, Prime 16, Write 16, **Track B 16**, Listen & Talk 0 | ~100+ WCPM with prosody |
| 6 Reading to Learn | 16 | session | Retrieval, Word work, Prime 16; **Track B 0**; Listen & Talk 0 | B2 text |
| 7 Advanced & Critical | 14 | session | Retrieval, Word work, Prime 14; Write 13; Track B 0; Listen & Talk 0 | C1 |

So the schema makes blocks optional per template. Listen & Talk is expected in L1–L4 lesson files only. Track B is expected in L1–L5; L6–L7 use one text set for teens and adults (DESIGN.md §4). Review, check and mastery-check lessons (L1.13/14, L2.13/14…) legitimately lack some blocks. The parser reports gaps; it does not invent blocks.

Order and heart words move from `tools/decodable.py` into `data/gpc.json` and `data/heart.json` (69 heart words: L1 24, L2 29, L3 16), and every tool reads them.

### 2.2 Strands

- **Code** (L1–L4): Hear, Meet, Blend (produced), Spell, Heart words, Check.
- **Read it**: a decodable text, Track A or B by skin, with 2 literal questions and 1 think question.
- **Listen & Talk** (L1–L4): the honest phone version (§3.8).
- **Review**: the warm-up is the Leitner review.
- **Fluency** is a strand **from L2** (DESIGN.md §1).
- **Morphology** runs **L4–L7**.
- **From L5**: prime-the-topic, knowledge texts, reciprocal teaching, and writing to read. Lateral reading at L6–L7.

### 2.3 Every rule, and how software enforces it

| Rule | Mechanism | Check |
|---|---|---|
| 1 No cueing | No picture beside an undecoded word. Pictures appear in Listen & Talk only after the passage is heard. Prompts come from a whitelist. **Repair never starts with the whole word**: a first repair replays the sounds one at a time. Reader tap-a-word plays sounds one by one; the whole word plays only after the learner's attempt | DOM test: no image before `decoded=true`. **Audio-trace test**: the build fails if any whole-word clip plays between a failed attempt and the next attempt on blend, reader or check screens. String lint bans "guess", "look at the picture" and "what makes sense" before a decode |
| 2 Decodable = decodable (L1–L4) | Every word in read/blend/check is decodable from the cumulative GPCs, a scheduled heart word, or a flagged story word (≤2 per text) | `decodable.py` on the JSON; build fails on any unflagged word |
| 3 Blend before segment; spell after blend | `lessonsFor()` emits hear → meet → (trace) → blend → spell. Single-letter sittings get no spell-word step: L1.02 Sitting A is `hear, meet, trace, mini`. Blend and spell start at Sitting B ("sa") | Snapshot test over the real L1.02–L1.12 JSON: no spell step before the first blend in any sitting |
| 4 Mastery gate | Each check uses **its own lesson's stated bar**, parsed into JSON; 0.9 is the default when none is stated (§3.5). The level check needs ≥90% on real and on pseudowords separately | A unit test enumerates every reachable score per lesson against its stored bar. The oracle runs a just-below-bar attempt **per lesson** and asserts reteach |
| 5 Heart words mapped, never flashed | E8 heart-word map; no flash type exists in the schema | Lint: all 69 heart words have `heartIdx` |
| 6 Two registers | `read.B` required in L1–L5 lesson/session files, or `sameAsA` | Parser + a child-coded-word lint on B |
| 7 Comprehension from day one | L1–L4: Listen & Talk in every lesson that has it in the course (§2.1). L5–L7: prime + knowledge text + questions | Parser coverage report; missing blocks are listed as course tickets, not faked |
| 8 Two metrics | Mastery components kept separate; "pace" vs WCPM labelled | Schema has no `total`; a UI grep finds no single blended percentage |
| 9 L1 notes | `l1_tags` per lesson; one note per tag × language family | Tag lint |
| 10 Pause-safe, no streaks, skip = take the check | Days practised only goes up. Checkpoint on every screen. Leitner in sittings. "I already know this" opens the check | 20 random kills resume on the same screen; string lint bans "streak", "don't lose", "you missed" |
| 11 Multisensory optional | Trace **on by default** for Track A and Track B Level 1, with a visible "Skip tracing" button and a settings switch | Settings test |
| 12 Honest citations | Listing and in-app claims come only from the evidence tables | Listing review (§7.6) |
| Fixed: machine never promotes **mastery** alone | `mastered` requires helper evidence. The machine gives `secure` (verifier + delayed re-check) or `provisional` (proxy). Both unlock the next lesson; neither is called mastery | Gate-reducer unit tests over all evidence combinations |
| Fixed: audio never leaves the device | No network code in the speech plugin; buffers dropped after scoring | Proxy test: zero requests in 100 attempts |
| Fixed: no ads/account/analytics | Dependency allowlist | CI |

---

## 3. Product

### 3.1 App structure and launch screen

- **Launch screen**: avatar tiles of child profiles, shown first, and "+ add a child". The adult profiles sit behind a small lock tile that opens with the grown-up PIN. Child profiles never show an adult's name.
- **Grown-up gate**: a 4-digit PIN the grown-up sets at the first grown-up action, shown in the UI language's numerals. It replaces the Urdu app's spoken number-words gate, which an 8-year-old can pass by listening (parent critic). PIN reset: hold the lock for 10 s, then answer a written arithmetic item. Weak, but it protects only settings.
- **Destructive actions** (delete profile, restore over existing, reset progress) need the PIN plus a second "Hold to confirm" with a spoken warning. Never one tap.

| Track A tabs | Track B tabs | Grown-up area (PIN) |
|---|---|---|
| Path (pearls) | Lessons (list + level line) | Profiles, helper session, reports, listening, reminders, packs, backup/restore, comfort, about/licences, privacy |
| Stories | Read | |
| Practice | Practice ("words you can read now") | |
| Me (stickers, days practised) | Progress (decoding / comprehension / fluency) | |

Speaking happens through entry points inside these tabs, as research-05 §1 suggests. There is no fifth tab. Voice: every screen auto-plays its instruction once for Track A and for Track B Levels 1–2, then on tap. "Hear it again" is on every screen.

### 3.2 The sitting model

A sitting is one opening of the app: 1–4 block-units, then "you can stop here", with a checkpoint on every screen.

- **Budgets.** Track A 5–8 min, Track B 10–15 min. A lint sums each sitting's budgeted seconds (from item counts × per-item time) and fails a Track A sitting over 8 min.
- **One new GPC per sitting in every level, L1–L4**, or at most 5 new words for pattern lessons such as L2.6's 20 initial blends, which become 4–5 sittings by blend family.
- **Track A order inside a sitting.** Warm-up ≤3 cards (Track B ≤6) → one new sound → blend 6–8 words → stop. Listen & Talk moves to its own sitting on alternate days, so blending is never squeezed out (teacher defect 6).
- **Repeats.** Hear/Meet can re-run twice. A third miss triggers the oral on-ramp repair (§3.4) and a helper flag.
- **Fast track.** Five fast correct mini-check items in a row offer "Skip ahead: take the check". Track B may merge sittings.
- **L5–L7 sessions** split into three sittings: S-A (retrieval, word work, fluency), S-B (prime, first half of the text), S-C (second half, roles, write, check).
- **Sitting counts** per lesson come out of the week-2 lint, not a fixed ratio. The ratios in §1 are estimates.

### 3.3 Exercise catalogue

| ID | Type | Input | Judge | No mic / no helper |
|---|---|---|---|---|
| E1 | Sound game: hear two **spoken words** (no pictures), tap the one that starts/ends with the sound | tap | machine | — |
| E2 | Meet card: letter, human phoneme clip, mouth picture, L1 tip | tap | none | static image |
| E3 | Sound tap: hear a sound, pick the letter from 2–4 | tap | machine | — |
| E4 | Trace with stroke scoring (§3.9) | finger | machine | — |
| **E5** | **Blend it, produced** (below) | tap + speak | verifier; helper optional | E6c |
| E6c | **No-mic blending check** (cut path, §5.7) | tap | machine (proxy) | is the fallback |
| E7 | Spell: tiles (A) / keyboard + tiles (B); sounds → words → sentence | tiles, keys | machine; error class tagged | — |
| E8 | Heart-word map | tap, tiles | machine | — |
| E9 | Decodable reader; tap a word = its sounds one by one; whole word only after an attempt | tap, speak | literal = machine; think = self; read-aloud lines via verifier if on | silent reading + questions |
| E10 | Listen & Talk, honest version (§3.8) | listen, tap, record | none (oral practice) | tap-choice + model |
| E11 | Check: the lesson's items and bar | mixed | verifier (real words), verifier or E6c (pseudo), E7 (dictation) | E6c → provisional |
| E12 | Retrieval card (Leitner) | tap | machine | — |
| E13 | Morphology builder (L4+) | drag | machine | — |
| E14 | Phrase-cued echo reading (fluency from L2) | speak | self (v1), verifier lines (v2) | listen and follow |
| E15 | Timed read: 60 s, helper marks errors, or "pace" | speak, tap | helper / pace | pace |
| E16 | Prime the topic | tap | none | text-only |
| E17 | Long-text reader (§3.7) | scroll, tap | machine (MCQ anchors) | — |
| E18 | Reciprocal teaching with a scripted partner | tap, type | structure machine, content self | — |
| E19 | Write to read | keys | self + key-term check | — |
| E20 | Lateral-reading sandbox (L6–7) | tap | machine (authored) | — |
| E21 | Record and compare (practice, labelled "practice") | speak | self | hidden |
| **E22** | **Ear training**: minimal pairs (vet/wet, sat/set, ship/chip, thin/tin), hear one, tap which. Runs before production of Urdu-contrast sounds | tap | machine | — |
| **E23** | **b/d/p/q**: hear the sound, pick from the four rotated shapes; formation replay on a miss; interleaved in warm-ups from L1.09, timed rounds at L1.13 | tap | machine; error class `bdpq` | — |

**E5, Blend it, step by step:**
1. **Model once.** The successive-blending highlighter sweeps "s → sa → sat". Each grapheme lights as its human sound plays, then the Kokoro word plays. Shown only on the first item of a new pattern.
2. **Learner, sound by sound.** The learner taps each grapheme (its sound plays) and says it. The highlighter grows over the graphemes said so far. Track A holds the mic ring; Track B taps once.
3. **Learner says the whole word.**
4. **Judge.** The verifier returns `clear_yes`, `unsure` or `clear_no` (§5). In a helper session the helper can tap instead.
5. **Repair** on unsure/no. Repair 1: "Point to each sound. Say the sounds. Blend." The sounds replay one at a time with gaps, never the whole word. Repair 2: the first sound is modelled and the learner blends again. Then the item **moves on**, is re-presented two items later and queued for review. The whole word plays only after the learner's re-attempt. The screen never waits for an adult.

### 3.4 Night one and opt-in placement

**Night one (exit check: first letter sound heard and tapped ≤90 s from first launch, stopwatched on a non-reader; §12.3 G0):**
1. **Launch → role screen.** Language comes from the device locale. On ur/PK the prompt is spoken in Urdu then English; a small language button sits in the corner. Two cards:
   - **"Me"**: one adult figure holding a phone, alone.
   - **"A child"**: a child figure with an adult hand on the shoulder, with "+ more children later" spoken.
   The icons were chosen in a sound-off test (five Urdu-only adults must pick correctly, 5/5).
2. **The lesson starts.** L1.02 Sitting A begins: Hear it (spoken "sun… s-s-s-un", no picture), then Meet it (letter s, human /s/, "tap the s"). Then trace, then the mini item. No nickname, PIN, mic or questions before this.
3. **Stop-here screen.** Nickname and avatar (optional). For the child card the grown-up is asked to set a PIN "next time you open settings". Mic setup is deferred to Sitting B, which needs speech.

**The oral on-ramp.** L1.01 is a deliberate change of course order (D29). The course starts with L1.01, an oral on-ramp. The app starts at L1.02 and uses L1.01's oral games as the Hear-it items of the first sittings. The full L1.01 runs as a repair when Hear-it items are missed twice, or when opt-in placement Stage 1 places there.

**Opt-in placement** ("I can already read some English", on the first lesson screen and in Me/Progress). It runs `placement-test.md`'s checkpoints with its real rules. The file's tester script says: *"Some of the 'words' aren't real words — they're made-up. Just tell me the sounds you'd make if you saw them. There's no embarrassment here; this just tells us where to start."*

- **Stage 0 (intake).** Not asked as a spoken questionnaire. Q1 is answered by pressing the button. Q3 comes from the UI language. Q2 ("ever taught to read in another language?") is one optional silent on-screen card. Q4 (languages always hard) lives in the optional screener, where it is a screener flag.
- **Stage 1 (oral PA, ~5 min).** The file's PAST-informed deletion/substitution items, 4 levels × 8. The app speaks each item and the learner answers aloud. **Correct** is judged by the verifier (targets are known real words, e.g. "boy"). **Automatic** is latency ≤2 s, measured by the app. Both outputs are stored. Stop below 6/8 Correct. Without the verifier or a helper, Stage 1 is **not administered**, as the file's self-test section says ("a missing data point is honest"), and the learner goes to Stage 2.
- **Stage 2 (letter sounds).** Block A 26 items (<24/26 → Level 1 at the first missed letter in sequence). Block B 5 (any miss → Level 2 at that digraph). Block C 7 (any miss → Level 3/4). The app version is receptive (E3: hear a sound, tap the letter) and labelled "app version: hearing, not saying". That is a proxy for the file's spoken version.
- **Stage 3 (decoding ladder).** Tiers of 8 real + 8 pseudo, pass ≥14/16. Real words go to the verifier. Pseudowords go to the verifier if that class passed the gold set (§5.6), else to E6c. Placement is the first tier below 14/16. **If Tier 1 is below 90%, place at L1.02.**
- **Stage 4 (oral reading fluency).** **Only if Tier 3+ cleared.** Passages A/B/C (FK ≈1.7/4.7/6.8). Hasbrouck–Tindal 2017 Fall 50th percentile cuts, already in the file: Grade 2 = 50, Grade 4 = 94, Grade 6 = 132 WCPM. The file's DIBELS rules apply: 3 s hesitation, self-correction within 3 s, and discontinue on zero correct in the first line. v1 needs a helper to mark errors; otherwise Stage 4 is skipped and placement uses Stage 3. All tiers pass and Passage C reaches ≥132 → Level 6 entry.
- **Result.** "Start at Level N, lesson K", plus "earlier" and "later (take that check)". No score shown. Three equivalent forms (C3) so a retake does not reuse items.

### 3.5 Pass bars, gates and the state machine

**Pass bars, as the course states them** (counted 2026-10-05; the week-1 parser report is authoritative):
- L1.02 Check **≥9/11 (81.8%, labelled "≈≥90%" in the lesson)**.
- L1.03–L1.13 Checks **≥10/11 (91%)**.
- **≥4/5 appears 19 times, in 10 Level 1 lessons (L1.01, L1.03–L1.09, L1.11, L1.12)**: sitting mini-check blend bars, plus L1.01's check.
- Also present: ≥3/3, ≥2/2, ≥5/6 and ≥7/8 (mini checks).
- L3 checks are written "≥90%?".
- **L5 checks state ≥5/8 or ≥6/9 (62–67%)**.
- L6 states "4/5 or more".

The app stores each lesson's own bar as `{pass, of}` or `{ratio}`. If no bar is stated it uses DESIGN.md's 0.9. Mini-check bars only trigger a repeat; they never lock a lesson. The bars below 90% (L1.02, L5, L6) are **not hidden or silently raised**. A ticket on `english-reading-course` proposes harmonising them with rule 4, or documenting why a lower bar is right there (D27). The app follows whatever the course decides.

**Pseudoword freshness.** L1.02's letters s, a, t allow only a handful of pseudowords, and the lesson already uses 5 (tas, ast, sta, sas, att). **Three fresh sets cannot exist for L1.02.** Its re-check reuses the set in a new order, with a different dictated item. The ≥3-fresh-sets rule starts where `gen_pseudo.py` can supply them (expected from L1.03–L1.04; the week-2 generator report confirms).

| State | Enters when | Leaves to |
|---|---|---|
| `in_lesson(L,k,s)` | lesson unlocked | next sitting, or `gate` |
| `gate(L,k)` | check sitting | `awaiting_recheck`, `provisional`, `reteach` |
| `awaiting_recheck` | bar met with **verifier `clear_yes` on the real-word items**, pseudowords via verifier or E6c, dictation via E7 | the next sitting opens with a 2-min re-check (fresh items where they exist). Pass → `secure`, and the next lesson unlocks **in that same sitting**. Fail → `reteach` |
| `secure` | re-check passed | next lesson. UI label: "Checked by the app" |
| `provisional` | bar met but no verifier evidence (no mic, permission denied, or the cut path) | next lesson unlocks. An extra re-check is scheduled 3 sittings later. UI label: "Checked by tapping. We'll check again soon." The word "provisional" never appears in the UI. Upgrades to `secure` when verifier evidence arrives |
| `mastered` | a helper session confirms production items (blending aloud, pseudowords) | optional upgrade from `secure`/`provisional`. UI label: "Checked by [helper name]" |
| `reteach(L,k,step)` | bar missed | the lesson's named reteach step, then a re-check next sitting |
| `parked` | third miss on one gate | repair mini-lesson from the prior lesson; helper flag; "This one is taking longer. That is common." Never past a failed hard-prerequisite gate |
| `skip` | "I already know this" | `gate` |
| `level_check(L)` | last lesson secure/provisional | pass → re-placement slice for L+1; fail → reteach by error class |
| `repair` | a Leitner GPC drops twice in a week | a repair sitting is inserted |

**Unjudged items.** If an item cannot be judged (verifier unsure three times, or no helper response in a helper session within 20 s), it is marked `pending` and re-queued. It is never auto-passed, and the sitting moves on.

### 3.6 Spaced review

- **Decks**: GPCs, heart words, Tier-2 words, morphemes (L4+). Pseudowords are always regenerated.
- **Boxes**: 5, scheduled in **sittings** (1, 2, 4, 8, 16). The Urdu `session.js` uses days; we keep its box logic and change the unit.
- **Wrong answer**: down one box. Two wrong in a row → box 1.
- **Cap**: Track A ≤3 cards per warm-up, Track B ≤6, confusables interleaved (b/d via E23).
- **Return after a gap**: "Welcome back" runs 3–6 cards, oldest first, with no overdue pile.
- **FSRS**: only after real usage data exists.

### 3.7 Levels 5–7 reading on a phone

- Screens of 150–250 words, a progress bar, sticky resume.
- Line length 30–45 characters, in Andika (SIL OFL per research-05; licence file verified in week 2).
- Tap-for-gloss on taught Tier-2 words only.
- Lesson stop-and-check anchors become MCQs (C11).
- Signal-word highlighter toggle (L6).
- Read-along audio is a toggle, off for any text that feeds a fluency measure.
- These are defaults, not evidence. Tested in week 7 on the test phone with two pilot learners.

### 3.8 Listen & Talk, the honest version (L1–L4)

For an English beginner on a phone:
1. **Listen.** The course passage is played in chunks of 2–3 sentences. A picture appears **after** each chunk is heard, as an anchor for meaning; it is allowed here because nothing is being decoded.
2. **Word.** The Tier-2 word is spoken in English, then a **first-language gloss** is spoken in the UI language (C10), then the course's two examples.
3. **Talk.** A 10-second recording to answer the prompt. The recording is replayed to the helper in a helper session, or to the learner for self-listening, and labelled "**Speaking practice, not reading**". It is never stored past the sitting. Solo adults shadow ("say it after me") instead of discussing.
4. **No-mic fallback.** Tap one of 3 spoken answers, then the model plays.

Discussion prompts appear only in helper sessions. Verification: two literal questions in Urdu after each Listen block in the pilot; Urdu-first beginners should reach ≥80%.

### 3.9 Writing to read and letter formation

- **E4 trace scoring.** For each stroke the app scores: start point within 12% of glyph height of the model start; stroke count; stroke order; direction of each stroke; checkpoints passed in order; end point. Neatness and size are not scored. A failed stroke replays the model formation. Formation results feed error class `formation`, and b/d/p/q misses feed `bdpq`.
- **Dictation.** E7 runs in every lesson after blending. Tiles for Track A, keyboard for Track B, with error classes (missing blend letter, omitted silent e).
- **Paper.** Optional "write it on paper too" prompt, unscored.
- **L5–L7.** E19 frames + 4-point checklist + key-term check, with a model answer after.

### 3.10 Helper sessions (optional)

A grown-up opens "I'm sitting with [child] now" with the PIN. Inside a helper session only:
- "Got it / Not yet" buttons appear on production items.
- The judge's card is available: five error types (letter name for sound, added "uh" vowel, gaps instead of a blend, long "aaa", right only after a stare), each with its human-recorded audio example.

Outside a helper session no helper buttons exist, so a child cannot judge themselves. A helper's taps upgrade lessons to `mastered` only after the helper passes the 5-example classification (5/5). This comes from canvas `v6-changes.md`, not research-04. A helper who doesn't read English can skip it. Nothing is lost: the child still progresses via `secure`.

**Teacher mode** (`teacher.js`, `egra.js` mapped to the English subtasks) comes in v1.1.

### 3.11 Progress views

- **Track A**: pearls, a sticker per sound secured, days practised.
- **Track B**: "words you can read now" (lexicon words whose GPCs are all secure or mastered), the level line, days practised.
- **Grown-up page**, separate panels:
  - **Decoding**: real, pseudo and letter-sounds per level, each with its label: Checked by the app / by tapping / by helper.
  - **Comprehension**.
  - **Fluency**: WCPM if helper-marked, otherwise "pace", against the Hasbrouck–Tindal reference cuts (reference only).
  - **Flags**: parked gates, the oral on-ramp repeated, screener 3+, low letter-sound recall.
- No blended score anywhere.

### 3.12 Motivation, accessibility, reminders

**Motivation.**
- Keep: days practised (never resets), pearls and stickers (Track A), "words you can read now" (Track B), real-world texts unlocked at level ends, effort praise, no red X and no failure sound in Track A.
- Refuse: streaks, hearts/lives, leagues, guilt copy, celebrating each tap.

**Reminders.** Opt-in, local, at most weekly, off for Track A unless the parent turns them on, prompted only after the first completed sitting.

**Reading comfort** (research-04 §6.1):
- Size, line spacing, a letter-spacing slider, tints and high contrast (no efficacy claims). OpenDyslexic as a choice only. Reduce motion.
- Touch targets 60–80 px in Track A, ≥48 px in Track B.
- **Slow-word mode**: plays the pre-rendered 0.8× word variants (§4.2), so pitch is unchanged. Sentences in slow mode play word by word with small gaps.
- The screener is offered after opt-in placement or from the Me tab. It is private, skippable, and never gates anything.

**Voice-first.** Every control has an icon and a spoken label, and there is an auto-played instruction per screen (§3.1). Audit: complete lesson one and a backup restore with the text blinded (§12.3 G0).

### 3.13 Screens

Launch (child tiles + adult lock) · Role · Sitting runner (E1–E23) · Stop here (nickname/avatar) · PIN set/enter · Mic explainer · Placement (opt-in, stages 1–4) · Placement result · Screener · Path/Lessons · Check result (secure / checked by tapping / reteach / parked) · Re-check opener · Stories/Read · Reader · Listen & Talk · Practice · Me/Progress · Grown-up area · Helper session · Pack download (MB shown, ask every time) · Missing-pack screen (spoken: "This level needs a download, N MB. You can still review.") · Reading comfort · Room check · Welcome back.

---

## 4. Voice: the audio system end to end

### 4.1 Clip inventory, size range and install matrix

**Counts are a range until the week-1 parser report settles them.**
- **Lower bound**: research-05 §3 counted words only from blockquotes, tables and bold/italic: 5,763 learner-facing words and 3,546 sentences (±25%).
- **The undercount**: the engineer found plain `**label:** a, b, c` lists and backtick lists in L2–L4 that this method missed.
- **Upper bound**: every distinct word in every lesson file, 9,238.

| Clip type | Source | Count | Size each | MB |
|---|---|---|---|---|
| Words | Kokoro | 5,763 – 9,238 | 2.5 KB budget (1.77 KB measured, n=10) | 14.4 – 23.1 |
| Generated pseudowords | Kokoro (IPA) | ~770 (below) | 2.5 KB | 1.9 |
| Sentences L1–L5 | Kokoro | 2,224 (±25%) | 12.5 KB | 27.8 |
| Sentences L6–L7 | Kokoro | 1,322 (±25%) | 17 KB | 22.5 |
| Level 0 / placement | Kokoro | ~190 + 3 forms | — | ~0.8 |
| Tier-2 lines | Kokoro | 360 – 650 (60 to 108 lessons × 2 × 3) | 12.5 KB | 4.5 – 8.1 |
| UI lines (English) | Kokoro | ~200 | 9 KB | 1.8 |
| Slow 0.8× word variants, L1–L2 | Kokoro | ~1,640 | ~3.1 KB | 5.1 |
| Phonemes | Human | 44 + 3 combination sounds (/ks/ x, /kw/ qu, /juː/ u_e) = 47 × 2 takes | ~2.5 KB | 0.24 |
| Blending demos | Human | 23 lessons (L1.02–L1.12, L2.01–L2.12) × 3 = 69 | ~9 KB | 0.6 |
| Judge's-card examples | Human | 10 | ~6 KB | 0.06 |
| **Total** | | **~12,700 – 16,800 clips** | | **~80 – 93 MB** |

**Pseudoword derivation**:
- L1.03–L4 lesson checks: 61 × 2 extra sets × 5 = 610.
- Level checks: 4 × 2 extra sets × 10 = 80.
- Placement forms B and C: 5 tiers × 8 × 2 = 80.
- Total ≈ 770 generated, plus the markdown's own pseudowords (counted in week 1). L1.02 gets none (§3.5).

**Storage.** Clips ship as one Ogg Opus bundle per lesson with an offset index. Decoding is **per clip** (§6.8), never the whole bundle.

**Install matrix (per ABI; "est." = estimate, "unv." = unverified until measured):**

| Piece | MB | Status |
|---|---|---|
| Shell (JS, Lottie, Andika, images) | ~8 | est. (research-05) |
| Base audio: L0–L2 words + sentences 14.3, pseudo ~1, L0 0.8, UI 1.8, human 0.9, Tier-2 L1–L2 ~2.1, slow variants 5.1 | **~26** (lower bound) | computed from the table above; the undercount lands mostly here |
| Native speech runtime (onnxruntime + sherpa-onnx JNI) | 15–20 | unv. (research-05 "probably") |
| Verifier model | 5–40 | unv., measured in the week-1 spike |
| **Install** | **~54 – 94** | measured by `bundletool get-size total` in week 2 |
| Pack L3–L4 / L5 / L6 / L7 | ~13 / 12 / 18 / 11 (≈54, lower bounds) | computed |
| v2 only: Whisper tiny.en (75 MiB) or base.en (142 MiB) for WCPM | not in v1 | research-03 [V] |
| **Whole app with all packs** | **~108 – 148** | |

**Model placement.** The verifier model ships in the base if it is ≤25 MB. Otherwise it downloads at the first speaking step: "Listening needs a download, N MB. Ask me later / Download now".

**Packs.** "**Ask every time, show MB**", Wi-Fi or mobile data, never silent. Offered one level ahead. A missing pack shows the spoken missing-pack screen, and review still works. Also: hash manifest, resume, `persist()`. Phone-to-phone pack sharing in v1.1. No rupee estimate: PKR data prices are unverified (parent critic).

**Opus** in Ogg is verified on the week-0 test phones; iOS later gets AAC.

### 4.2 Kokoro pipeline

1. **Pinned environment.** A Docker image (or lockfile) pins kokoro, misaki, torch, espeak-ng, the thread count and the CPU flags. The **espeak fallback is disabled**, because `espeakng-loader` aborts the Python process rather than raising an error (research-02 §3). These versions go **into the clip id**: `sha1(voice, model_sha, torch, misaki, espeak, text, ipa)[:10]`. Check: render 100 clips twice, on two machines; the PCM sha256 must match, or the doc records which component drifts.
2. **OOV pre-check, before any rendering.** Each word is looked up in misaki's lexicon. A word not found with no entry in `data/pron.json` stops the build with a report. No exception handling inside the batch.
3. **IPA mapping layer.** `data/gpc.json` stores standard IPA (General American). `tools/ipa2misaki.py` maps it to misaki/Kokoro's own phoneme symbols (diphthongs and affricates are single symbols there; the exact table is verified in week 1). Round-trip check: every pseudoword and override string uses only symbols in Kokoro's vocabulary, or the build fails.
4. **Overrides** for heteronyms (read, live, lead, tear, wind, bow, close, use, does, wound, minute), "a" (/ə/ vs letter /eɪ/), "the" (/ðə/) and the -ed allomorphs. Each is reviewed by the **General American native reviewer** (D23).
5. **Render.** `af_heart`, speed 1.0 for all normal clips. A **single tier-wide 0.8× pass for L1–L2 words** produces the slow variants. That is a consistent tier, not per-clip tuning. Cost: +~1,640 clips, +5.1 MB base, about 25 min of rendering (estimate), the same QA. Rejected alternative: a JS time-stretch library, which costs bundle size and CPU on 2 GB phones and has unknown artefacts.
6. **Post-process (all clips, Kokoro and human, by one function):**
   - Trim by an energy detector at −45 dBFS, then pad exactly **40 ms head / 80 ms tail** with 5 ms fades.
   - Loudness: two-pass to **−18 LUFS integrated** for words and sentences. For clips **<0.4 s**, active-segment **RMS −20 dBFS** (BS.1770 gating is unreliable there).
   - True peak −1.5 dBTP. Opus 24 kbps mono.
   - **All checks run on the decoded Opus**, not the WAV.
7. **Manifest** per clip: text, ipa, method, versions, speed tier, duration, LUFS/RMS, lead/tail ms, QA results, rerolls.
8. **Throughput.** research-02 measured 1.3–2 words/s and 1–1.5 s per short sentence. ~13–17k clips is about 3–5 h single-process (estimate), which is fine for a one-off build.

### 4.3 QA loop

| Stage | What | Applies to | Pass |
|---|---|---|---|
| Q1 auto | coverage, hash, single voice; lead 30–60 ms, tail 60–110 ms; loudness sd <0.5 LU over each pack, human vs Kokoro means within 1 LU; duration; clipping | 100% | all, or build fails |
| Q2 ASR | faster-whisper transcript = text | real words, sentences | mismatch → Q3 |
| Q3 judge | `listen_judge.py` with **new English prompts** (the script is Urdu-only today). Real words: open "which word?". **Pseudowords: forced choice among 4 minimal-pair foils** | all pseudowords, Q2 fails, 10% of words | triage only |
| Q4 human | **The GA native reviewer** hears all pseudowords (~770 + markdown's), all Q3 fails, and the lowest-confidence 5%. Kamal and **one naive parent** rate a frozen 200 per pack on a rubric: correct word (Y/N); **same teacher as the neighbours? pace? sentence intonation natural?** (1–5) | as listed | ≥98% correct; consistency mean ≥4/5; pseudoword error <2% |

Before any further build work in week 1, the first listen covers 100 L1 clips, **including all 50 Track A sentences**. That settles the unexplained 2/5 child-sentence score (research-02 §6).

### 4.4 One voice, no audible join

1. **Speaker audition (week 1).** 2–3 candidates read /s/ /æ/ /t/ + "sat" + 10 words. We measure F0 median and range, speaking rate and spectral centroid against af_heart. Shortlist: F0 median within 2 semitones, similar pace, and a warmth rating by the audio critic.
2. **Bandwidth match.** Record at 48 kHz, resample to 24 kHz, low-pass near 12 kHz and EQ to af_heart's long-term spectrum. Af_heart has 1.2–4.4% of its energy above 8 kHz (audio critic). Target: the centroid of the human /s/ within 15% of the /s/ inside Kokoro "sat".
3. **Same-person gate.** Five naive parents (not Kamal) hear /s/ /æ/ /t/ → "sat" and are asked "same person?". **≥4/5 yes**, or the fallback fires.
4. **Fallback (a spike, unverified).** Clone the human speaker for the words with Chatterbox (MIT, Perth watermark) or Qwen3-TTS (Apache-2.0). Then the human voice speaks everything. Known gap: neither takes phoneme input (research-02 §1), so pseudowords would need a separate route (text spelling + verification, or human recording). This is a risk with a two-week cost, logged as D25.
5. **No voice switching inside a list.** Words are never replaced by human recordings, except the L1–L2 blending-demo words, which are human by design.

### 4.5 Re-roll policy

Kokoro is deterministic for fixed inputs. A failing clip:
1. IPA override, reviewed by the GA native reviewer.
2. Stress marks only, as a one-word utterance.

There are **no per-clip speed changes** and **no carrier crops**, because those import sentence prosody. After three failures:
- if the word is an L1–L2 blending-demo word, it goes to the human queue;
- otherwise it is **replaced in the lesson** by another word with the same pattern, through a course ticket.

If more than 2% of words need replacement, Chatterbox and bf_emma get re-tested (risk §9).

### 4.6 Human recording kit

- **Speaker**: chosen by §4.4 (D16), with a release for perpetual commercial use.
- **Conditions**: quiet small room, mic at 20–30 cm, 48 kHz mono WAV, no AGC/NS. Each session starts with room tone and a reference /æ/ compared with session 1. Tool: `voice_studio.py`.
- **The 44 phonemes (General American)**, 3 takes each, best 2 shipped:
  - **24 consonants**: /p b t d k g/ (short, clipped, no added vowel), /tʃ dʒ/, /f v θ ð s z ʃ ʒ h/, /m n ŋ/, /l r w j/. Continuants are held ~0.8–1.0 s.
  - **20 vowels**: short /æ ɛ ɪ ɑ ʌ ʊ/ + /ə/ (7); long /iː uː ɔː ɝ/ (4); diphthongs /eɪ aɪ ɔɪ aʊ oʊ/ (5); r-controlled /ɑr ɔr ɛr ɪr/ (4).
  - **Plus 3 combination clips** that the course teaches as units, not phonemes: /ks/ (x), /kw/ (qu), /juː/ (u_e, ew).
  - Reconciled against `gpc.json` in week 2; the audio gate fails if any `phoneme` lacks a human clip.
- **Blending demos**: 69 ("s-a-t" stretched → "sat"). 10 pilot demos in week 1, the rest in week 2.
- **Judge's-card examples**: 10.

### 4.7 Licence table

| Asset | Licence | Action |
|---|---|---|
| Kokoro-82M | Apache-2.0 (training data not verified line by line, research-02) | LICENSES.md with versions |
| misaki | check | week 2 |
| Generated audio | ours | AI-voice disclosure in About and the listing |
| Human recordings | signed release | week 1–2 |
| Course content | CC BY 4.0 | attribute |
| Andika | SIL OFL (per research-05) | verify, bundle the licence |
| Piper voices | **The Blizzard 2013 Lessac licence clause 3.2 grants use exclusively for Research Purposes (read by the lead 2026-10-05)**. amy/alba are fine-tunes, a grey area. Engine GPL-3 | not used |
| sherpa-onnx | Apache-2.0 (research-03: background knowledge) | verify week 1 |
| Verifier model | per model card | verify in the spike |
| Chatterbox / Qwen3-TTS (fallback only) | MIT / Apache-2.0 per research-02 | only if D25 fires |
| OpenMoji | CC BY-SA 4.0 | check share-alike before use |

### 4.8 What still fails

| Failure | Handling |
|---|---|
| Phoneme rationale unverified by a human | week-1 human listen before booking (§0) |
| The human/TTS join | §4.4 gate + fallback |
| Pseudoword IPA misreads (vop→"vob") | mapping layer, forced-choice Q3, native reviewer on 100% |
| af_heart child sentence 2/5 | week-1 listen of all 50 |
| No child voice | accepted |
| Slow mode | pre-rendered 0.8× words; sentences word by word |
| Rebuild drift across machines | versions in the clip id; two-machine sha test |
| Dynamic text | not in v1 |

---

## 5. Listening

### 5.1 Verification, not recognition

We always know the target. The verifier asks: is this audio the target word, or one of its likely errors? It decodes over a **small vocabulary**: the target plus 3–8 competitors generated from the lexicon:
- the vowel swap (/sɪt/);
- a dropped final sound (/sæ/);
- the first sound changed (/tæt/);
- schwa epenthesis (/səæt/);
- the letter-name reading;
- for heart words, the regular decoding ("said" as /seɪd/).

Output:
- `clear_yes` (target wins by margin) **credits** the item.
- `unsure` and `clear_no` look the same to the learner: the E5 repair. `clear_no` is logged for the grown-up view and is never shown as a fail.

Whisper is **not** the core. Open ASR snaps pseudowords to real words (research-03 §0), and whisper tiny needs ~273 MB RAM (research-03 [V]).

### 5.2 Engine and spike #1

- **Plugin.** A Kotlin Capacitor plugin: `AudioRecord` 16 kHz mono PCM → silero-VAD → sherpa-onnx → JS events. The WebView never touches raw audio. WASM is a PWA-only experiment, because SharedArrayBuffer is not available from `https://localhost` without cross-origin isolation (research-05 §4).
- **Which sherpa-onnx mode** the spike decides between: (a) keyword spotting with a per-item keyword list (target + competitors); (b) a small streaming transducer with hotword biasing, scored as target vs competitor margin over the n-best. Neither has been run here. Model sizes and pseudoword support (can keywords be given as phone/BPE token sequences for non-words?) are **unverified**.
- **Effort.** 6–10 working days on a real phone (engineer). It starts on day 1 of week 1 and decides at the end of week 2.
- **Budgets.** Plugin + model RSS ≤150 MB on top of the app. `.so` files pass `zipalign -c -P 16 4` (targetSdk 36 makes 16 KB alignment an upload gate). minSdk checked.

### 5.3 What the machine judges

| Item | v1 | v2 | Gate role |
|---|---|---|---|
| Taps, tiles, typed spelling, trace | machine | same | full |
| Real words (blend, check, reader lines) | **verifier** (if the class passes §5.6) | + phoneme-CTC margin | gives `secure` |
| Pseudowords | verifier **only if** its class passes §5.6 separately; else E6c | phoneme-CTC with known IPA | `secure` or `provisional` |
| Heart words | verifier with the regular-decoding competitor, if the class passes | same | as real words |
| Isolated sounds, incl. Urdu contrasts (v/w, short vowels) | **E22 ear training + E21 self-compare, labelled practice** | record-and-compare scored by the verifier's phoneme competitors | none |
| Passage / WCPM | helper-marked or "pace" | Whisper/Moonshine alignment, "approximate" | none |
| Mastery (`mastered`) | helper only | helper only | — |

### 5.4 Pipeline for one spoken item

1. Half-duplex: prompt → beep → mic. Never overlapping playback.
2. Track A holds the ring; Track B taps once, VAD stops.
3. Pre-gates → `unsure`, never no: <150 ms of speech, clipping, SNR <10 dB, more than one speaker, silence.
4. Constrained decode over target + competitors.
5. Margin vs per-class threshold.
6. Store metrics only (target, best competitor, state, margin, ms). The buffer is dropped.
7. Three `unsure` in a row → item `pending`, re-queued, move on (§3.5). Never a frozen screen.

### 5.5 Thresholds (research-03 §8)

| Metric | Bar |
|---|---|
| `clear_yes` precision | ≥97%, lower 95% CI ≥92%, ≥60 items per child per class, both kids and both conditions |
| `clear_yes` recall | ≥60% |
| `clear_no` precision | ≥90%, else demoted to unsure |
| Latency, end of speech → result | p95 <3 s; p50 <500 ms (budget) |
| Mic stability | 20 relaunch cycles, 0 failures |

5- and 7-year-olds are reported separately, never pooled.

### 5.6 Kid gold-set protocol (weeks 1–2, repeated in week 6)

- **Per child**: 100 items over 3–4 sessions of ≤8 min: 20 isolated sounds, 40 real CVC, 20 pseudo, 10 heart, 10 sentences.
- **Labels**: Kamal labels correct / wrong-type / unclear; a second adult labels a random 30.
- **Planted errors**: 30, adult-imitated (a floor, not a ceiling).
- **Conditions**: quiet room, TV/fan room, 30 cm and 1 m, the family phone and the week-0 test phone, battery saver on.
- **Adults**: 3 for Track B (40 real + 20 pseudo each).
- **Recording**: clips are kept only in the gated **research-recording mode** (D22): parent consent on screen, app-private storage, manual export, off in store builds.
- **Decision**: per class, go/no-go against §5.5. Pseudowords and isolated sounds may fail; that is an answer, not a bug.

### 5.7 Cut path if the verifier fails

**E6c, the no-mic blending check:**
1. The learner hears the word's sounds **separately, with gaps**, in the human phoneme voice: /s/ … /æ/ … /t/.
2. The learner sees **four written candidates on a 2×2 grid**. All share the first letter. They differ in the middle **and** the end: *sat / sit / sap / sip*. First-letter and last-letter matching leaves two candidates, so the middle vowel must be decoded.
3. The learner picks one.
4. The learner then **segments** it by tapping one sound box per sound, in order; each box plays its sound.
5. Both the pick and the segmentation must be right. Chance is 25% per item, so ≥9/10 by guessing is negligible.

**What E6c measures, stated plainly in the plan and the parent copy:** blending by ear and mapping sounds to letters. It does not measure reading print aloud.

Gates passed this way are `provisional`, with the extra re-check. The same path serves no-mic phones and permission-denied learners, even when the verifier works.

### 5.8 WCPM

- **v1**: E15. The helper taps errors. The DIBELS rules from `placement-test.md` apply: 3 s hesitation, self-correction within 3 s, discontinue on zero correct in the first line. WCPM = (words reached − errors) per minute; with no helper it is "pace".
- **Reference**: Hasbrouck–Tindal 2017 (G2 50/84/100, G4 94/120/133, G6 132/145/146 Fall/Winter/Spring 50th percentile, as in `placement-test.md`) and DIBELS 8 Grade 1 ORF (35/57/76). Reference only.
- **v2**: ASR alignment, "approximate", expected ±5–10 WCPM (research-03, unverified).

### 5.9 Privacy

On device, in memory, discarded. Metrics only, kept in the user's own backups. No voiceprints are created (COPPA amendment, research-04 §5). Data Safety stays "No data collected", re-checked against the live form before submission.

---

## 6. Tech

### 6.1 Repo and reuse

- **Repo.** New repo `read-english` (`com.oyekamal.readenglish`), with files copied once from `urdu-reading-course/mobile` and a `PROVENANCE.md`.
- **What copies cleanly** (research-05 §1): AS-IS 449 lines (12%), WITH CHANGES 2,702 (70%), brand 391 (10%), REWRITE 313 (8%).
- **What is new work, not edits** (engineer): `path.js`, `learner.js`, `onboarding.js` and `drills.js` are bound to the Urdu unit model (`C.units`, `n < 12`). The level/lesson/sitting/track state machine, 23 exercise types, opt-in placement, the gate reducer and the native plugin are **new work**, scheduled as such.
- **Layout.** `app/`, `android/` (+ `plugins/verify`), `data/` (gpc, heart, pron, blocklist, bars), `tools/`, `tests/`, `store/`, `LICENSES.md`, `PROVENANCE.md`, `PRIVACY.md`. The course is pinned by commit.

### 6.2 Content pipeline

- **Parser.** `tools/build_content.py --strict` runs over **all 108 lessons + 7 mastery checks from day 1**.
- **Week-1 exit: a coverage report**, one row per file: blocks found, word lists found and in which form (pipe table, `**label:** a, b, c`, backticks), the bar found, and unknown headings.
- **Variant structures** are handled explicitly: L1.02 nests `### 7. Read it` inside `## Sitting D`; L7.03 has "Meet the move" and two close-reading blocks.
- **Prose fields** that machines need but the markdown lacks (`errorClasses`, `reteach.step`, MCQ `anchors`, `keyTerms`, bars written as prose) are added as a fenced `app:` YAML block per lesson. A script inserts them, a human reviews, and they go in as PRs to the course repo (C7, C11). The parser never infers them from prose.
- **Round-trip.** Each JSON re-renders to markdown and is diffed against the source, so silent drops show up.

**Schema.** All blocks except `id`, `level`, `type` are optional; per-template requirements are enforced by the coverage lint (§2.1).

```jsonc
// data/gpc.json   { "s": {"ipa":"s","misaki":"s","intro":"L1.02","audio":"ph.s","l1_tags":[…],"locale":{"ur":"…"}} }
// content/lexicon.json
{ "sat": {"g":["s","a","t"],"p":["s","æ","t"],"kind":"decodable","intro":"L1.02","audio":{"n":"w.…","slow":"w.…"},
          "competitors":["sɪt","sæ","tæt","səæt"], "pron":"misaki|override"},
  "said":{"g":["s","ai","d"],"p":["s","ɛ","d"],"kind":"heart","heartIdx":[1],"competitors":["seɪd"]},
  "tas": {"kind":"pseudo","g":["t","a","s"],"p":["t","æ","s"],"review":"native|pending"} }
// content/lessons/L1.02.json
{ "id":"L1.02","level":1,"type":"lesson","contentVersion":"2026.10.1",
  "sittings":[{"id":"A","newGpc":["s"],"steps":["hear","meet","trace","mini"],"mini":{"kind":"repeat-trigger","pass":5,"of":5}},
              {"id":"B","newGpc":["a"],"steps":["warm","hear","meet","trace","blend","spell","mini"]}, …],
  "blend":{"real":["at","as","sat"],"pseudo":["tas","ast","sta","sas","att"]},
  "read":{"A":{…},"B":{"sameAsA":true},"questions":[…]},           // optional per template
  "listen":{"chunks":[…],"tier2":[{"word":"…","gloss":{"ur":"…"}}],"talk":"…"}, // L1–L4 only
  "check":{"real":[…],"pseudoSets":[[…]],"freshSets":false,"dictation":["at"],
           "bar":{"pass":9,"of":11,"source":"lesson"},"reteach":{"step":"C"},"errorClasses":{…}} }
// content/mastery/L1.json   components scored separately, each with its own bar
// content/placement.json    forms A/B/C; stage1 items with automaticity ms; stage2 blocks; stage3 tiers; stage4 passages + HT cuts
// content/ui.json + ui.<lang>.json   text, icon, audio id
```

### 6.3 Build-time gates

`npm run content` fails on any of these:
1. Decodability on L1–L4 (A and B).
2. **Pseudoword filter**: real-word check against CMUdict and the lexicon, blocklist, IPA homophones, and the native-review flag set. The `gan/nob/rob` history shows why human review is required.
3. **OOV pre-check and IPA vocabulary round-trip** (§4.2).
4. **Audio coverage + Q1 on decoded Opus.**
5. Paths: every lesson reachable; every reteach target exists; every check's bar reachable with its own item count.
6. Coverage lint per template.
7. No-cueing strings, plus the whole-word-repair audio trace (in tests).
8. Sitting budget lint (Track A ≤8 min).
9. Sizes: lesson JSON ≤50 KB; base audio within the §4.1 matrix (+10%).
10. Parser snapshots + round-trip diff.

### 6.4 Data model and migrations

**IndexedDB stores.** Kept from the Urdu app: `settings`, `profiles`, `attempts`, `cards`, `sessions`, `progress`, `assessments`. Added: `speech` (metrics only), `mastery` (state, components, evidence with judge type), `packs`, `helper`.

**Migrations** (engineer). The Urdu `db.js` hard-codes `VERSION = 1` and "repairs" by bumping the version; no migration has ever shipped.
- v2 starts at `DB_VERSION = 1` with a real `onupgradeneeded` ladder: one function per version step, each with a test that upgrades a fixture DB from every previous version.
- **Progress is keyed by lesson id and item text**, never by clip id. Clip ids change when text changes.
- **Content versions.** Every pack manifest carries `contentVersion` and `gpcHash` (hash of gpc.json + heart.json). The app stores the base `contentVersion`. A downloaded pack with a different `gpcHash` is **rejected** with "update the app first". A pack built for an older compatible base is accepted.
- `mastery` and `cards` records carry the `contentVersion` they were earned under. If a lesson's items change, its earned state stays and only the item queue is rebuilt.
- **Test**: finish L1.05 on build N, upgrade to N+1 with L1.05 edited and ids shifted, and assert progress is intact.

**Pack reconcile at launch.** Stat the pack files; if IndexedDB and disk disagree, mark the pack absent.

**Profiles.**
- `track`, `skin`, `homeLang`, `l1Family`, `comfort`, `placement{…,form,stage1:{correct,automatic}}`, `daysPractised` (monotonic).
- Adult profiles carry `hiddenOnLaunch:true`.
- Cards, attempts, speech and mastery are keyed by `profileId`.

**Backup.** `backup.js` merges by id + updatedAt. Its regex and `BACKUP_FORMAT` are updated and it is behind the PIN. Sync is not in v1.

### 6.5 Platforms and test devices

- **Week-0 decision (D24)**: **buy or borrow a 2–3 GB RAM Android 10 phone** (Tecno/Infinix/Redmi A class). Kamal's family phone is the second device. No physical device is attached today, and the SDK only has x86_64 emulator images (engineer). Opus on the Android 10 WebView, armeabi-v7a and RSS cannot be checked on an emulator.
- **Android AAB + PWA.** minSdk 24 (verify against sherpa-onnx), targetSdk 36, ABI splits arm64-v8a and armeabi-v7a, 16 KB alignment checked. iOS later.

### 6.6 Audio playback path

- Bytes reach JS via `fetch(Capacitor.convertFileSrc(path))`, not base64 `Filesystem.readFile` over the bridge.
- Each clip is sliced from the lesson bundle and decoded on demand into an LRU of decoded `AudioBuffer`s capped at 8 MB. The next 3 expected clips are pre-decoded.
- Whole bundles are never decoded: an L6 bundle would be about 70 MB decoded (engineer).
- **PWA**: the service worker caches each lesson bundle as one file, and the slicing code is shared.

### 6.7 Performance budgets

Budgets, not measurements, until the week-0 phone is in hand:

| Metric | Budget |
|---|---|
| Cold start | <2 s |
| Tap → lesson render | <100 ms |
| Tap → first sound | <150 ms (p95 over 200 taps) |
| JS | <150 KB gzip |
| Memory | <150 MB without the verifier, <300 MB with it |
| Verifier load / result | <3 s / p95 <3 s |
| Night-one first sound tapped | ≤90 s |

### 6.8 Test harness

1. Parser coverage + snapshots + round-trip.
2. Content gates.
3. **Oracle driver**: completes L1–L2. **Per lesson**, a just-below-bar run must reteach and a third miss must park.
4. DOM no-cueing + **whole-word-repair audio trace**.
5. Gate reducer over all evidence combinations, including "child reaches L2 with no helper and no 'provisional' string in the UI".
6. Kill-and-resume ×20.
7. `ui_audit.py` + **blinded-text audio-only run** (lesson one + backup restore).
8. **Child-cannot-open-adult test**: an 8-year-old tries for 1 minute.
9. Parent-absent test: 6 screens with no adult; unjudged items pending, never passed.
10. `check_audio.py` on decoded Opus.
11. `speech_eval.py` over the gold set.
12. `perf.py` CSV.
13. DB migration ladder.
14. Pack interrupt / resume / bad hash / incompatible gpcHash.
15. Airplane-mode install-to-L1.
16. Network-silence proxy.
17. `zipalign -c -P 16`, `bundletool get-size total`.
18. `store_judge.py`, `leak_check.sh`.

---

## 7. Global

### 7.1 Localisation

Course text stays English. Localised: UI strings + audio (~200 lines in English, budget ~300 per language), Tier-2 glosses (C10), helper card, L1 notes, privacy page, listing.

| Wave | Languages |
|---|---|
| v1 | English + Urdu UI |
| 1 | Hindi, Arabic, Spanish, Bengali |
| 2 | Portuguese (BR), Indonesian, French, Swahili, Persian/Dari |

The wave ranking is from memory (research-04 §4.1) and gets confirmed with Play Console data (D8).

**Stated limitation**: Punjabi and Pashto speakers get the **Urdu UI**, not their own language, in v1. Many Pakistani learners are therefore taught in their second language. A Punjabi UI (Shahmukhi script) is a wave-1 candidate if the pilot shows Urdu instructions are not understood.

**UI voice per language.** Licensed for commercial use. Urdu uses the Sara clips only if their licence covers this app (D9).

### 7.2 L1 notes

`l1_tags`: short_vowels, th_voiced, th_unvoiced, v_w, p_b, b_v, clusters, s_clusters, final_clusters, silent_letters, vce, schwa, direction, opaque_spelling. One note per tag × family (Perso-Arabic, Indic, Spanish/Portuguese, French, Bantu/Indonesian). Each note is one spoken sentence plus an E22 contrast pair. The family generalisations are from memory and get native review. Urdu notes convert first.

### 7.3 RTL

Logical layout. UI mirrors for ur/ar/fa. English content never mirrors: words, highlight, trace and blend sweep all run left to right. Mixed-direction labels are tested in week 7.

### 7.4 Icon- and voice-first

Auto-played instruction per screen (§3.1). Icons tested sound-off with five Urdu-only adults. Destructive actions take the PIN plus hold-to-confirm. Blinded-text audit (§6.8).

### 7.5 Compliance

| Area | What we do |
|---|---|
| Play Families | Mixed audience; no ads/analytics SDK, no ad ID, no location, no age collected |
| COPPA (amended; compliance 22 Apr 2026) | No personal information; no voiceprints; written retention statement |
| GDPR-K / UK Children's Code | Nothing processed off device; plain privacy page per language; short DPIA; no nudges |
| Grown-up gate | PIN before settings, helper sessions, backup/restore, delete, links out, mic setup for child profiles, pack downloads, research-recording mode |
| Mic | Requested at first speaking step; app fully usable without it (E6c) |
| Native libs | 16 KB alignment verified before upload |
| Voice disclosure | Kokoro + named human speaker in About and the listing |
| Rating / testing | IARC Education; closed test ≥12 testers × 14 days |

### 7.6 Store listing

- **Name** (D17): age-neutral, e.g. "Read English: Learn to Read". Neutral icon.
- **Short description**: "Learn to read English from the first sound. Free, offline, any age."
- **Hooks**: free, no ads; works offline; for children **and adults**; checks the learner really reads, using made-up words, with **no English-reading helper needed**; never resets progress. No bar app leads with adults or a mastery check. Duolingo ABC does list offline.
- **Size**: an honest line: "Install about N MB; later levels download when you choose (about 54 MB in total)", with N from `bundletool`.
- **Banned claims**: "proven", "guaranteed", "cures dyslexia", any effect size, any Teach Your Monster "RCT".
- **Screenshots**: per language via `make_store.py`, judged by `store_judge.py`.

---

## 8. Build plan

**Who does what.**
- **Kamal**: decisions, kids' sessions, Play Console.
- **Speaker**.
- **GA reviewer**: native General American English reviewer.
- **Naive parents**: 5, for the same-person test.
- **Build agent**: a Claude Code session in `read-english`.
- **Critics**: fresh, blind, one per lens.
- **Judge**: `listen_judge.py`, triage only.

| Week | Deliverables | Exit check | Who |
|---|---|---|---|
| **0** | D24 test phone in hand; 2–3 speaker candidates and the GA reviewer booked; W0/W1 decisions answered; Docker render env started | dated device list in repo; decisions logged in decisions.tsv | Kamal |
| **1** | **Spike #1 verifier** begins: plugin skeleton, AudioRecord → VAD → sherpa-onnx, both modes, 30 real + 10 pseudo × 3 speakers, first 2 gold-set sessions per kid. **Parser coverage over all 108 + 7.** IPA path: all GPC strings + 100 pseudowords through ipa2misaki → Kokoro → GA reviewer. Voice audition + **same-person test**. First listen: 100 L1 clips incl. 50 Track A sentences. Opus on both phones | coverage report for 115 files committed; IPA round-trip 100% in vocab, reviewer error rate logged; same-person ≥4/5 (else D25 spike scheduled for week 2); listen verdict logged; Opus plays on both; verifier: first RSS, latency and accuracy numbers in `spikes/verify.md` | build agent, Kamal, speaker, GA reviewer, parents |
| **2** | Verifier spike completes: gold set run, **go/no-go per class**, 16 KB + size numbers. Repo + data files; strict parser on all files; `app:` YAML PRs for bars and reteach steps; decodability; `gen_pseudo.py` + filter; OOV pre-check; **word recount settles §4.1**. Speaker records 47 × 3 + 69 demos + 10 examples | go/no-go table per class vs §5.5; `npm run content` exits 0 for L1–L4; `bundletool` install size; recount committed; human clips pass the §4.2 post-process checks | build agent, Kamal, speaker |
| **3** | Render L0–L2 (+ slow variants) with the loudness/padding spec; Q1–Q4 for L1–L2. Shell boots: launch screen, role screen, **night one into L1.02 A**, DB migration ladder, LRU playback | Q1 100%; Q4 ≥98% correct and consistency ≥4/5 by a naive parent; **G0 stopwatch ≤90 s** on a non-reader; offline airplane boot; migration test passes | build agent, Kamal, GA reviewer |
| **4** | E1–E12 with **produced E5**, E6c, E22, E23, trace scoring; gate reducer (secure/provisional/mastered); repair lint + audio trace; oracle per-lesson bars; Listen & Talk honest version; Track A/B skins. **Critic round 2** (teacher, parent) on a recorded L1.02–L1.04 run | oracle L1–L2 complete; below-bar run reteaches **per lesson**; no whole-word audio before a re-attempt; teacher-agreement test set up (5 solo adults + 5 children, blind teacher, ≥90% agreement target) | build agent, critics |
| **5** | L3–L4 content and audio pack; opt-in placement with real rules and 3 forms; PIN gate, hidden adult profiles, helper sessions + card; screener; progress panels; Urdu UI strings and audio | scripted placement places the 5 archetype fixtures exactly per `placement-test.md` rules; 8-year-old cannot open the adult profile; parent-absent test passes | build agent, Kamal |
| **6** | Verifier hardening (room check, permission flow, handover, pending queue); gold-set re-run on device; pack manager (ask every time, MB, missing-pack screen, reconcile); L5–L7 session screens | §5.5 metrics per class and per kid; 100 record cycles + 20 relaunches with 0 failures; pack interrupt/resume/bad-hash/incompatible tests pass | build agent, Kamal |
| **7** | Perf on the test phone; a11y, comfort, RTL; blinded-text audio audit; backup A→B; PWA; signed AAB, 16 KB verified | budgets met or a gap list; audio-only lesson one + restore succeeds; backup round trip identical; `zipalign -P 16` passes | build agent |
| **8** | **Gauntlet G0–G7** (§12.3); privacy, DPIA, Data Safety, Families; listing EN/UR; Play internal testing; closed test started; pilot starts | gate verdicts recorded; install from the internal link on both phones; L1 offline; pre-launch report clean; 12 testers enrolled | critics, Kamal, build agent |

**If the verifier is no-go at the end of week 2.** E6c becomes the child gate path (`provisional` + extra re-check). Week 6's verifier slot becomes helper-session polish and teacher mode. Nothing else slips.

**If the same-person test fails in week 1.** The cloning spike (D25) runs in week 2 alongside, and words for L1–L2 are re-rendered in week 3 in the chosen voice. Packs for L3+ follow in week 5.

**Roadmap.**
- **v1.1**: production after the closed test; teacher mode; phone-to-phone pack sharing; wave-1 languages; Track B real-world texts; course-bar harmonisation applied.
- **v2**: phoneme-CTC verifier (pseudowords, isolated-sound record-and-compare for Urdu contrasts); ASR WCPM; FSRS; iOS.
- **v3**: prosody proxies; tutor review queue; optional sync; on-device TTS for dynamic text.

---

## 9. Risks and honest unknowns

| Risk | Likelihood | Impact | Mitigation | Known by |
|---|---|---|---|---|
| Verifier fails the kids' gold set | Medium–High | High (child progression quality) | E6c cut path, `provisional` + re-check, helper upgrade | End of week 2 |
| Native plugin RAM, 16 KB, size or effort overrun | Medium | Medium | Spike first; model as a download if >25 MB; 6–10 day budget | Week 2 |
| The human/TTS join is audible | Medium | High | Audition, bandwidth/loudness match, same-person gate, cloning fallback | Week 1 |
| Cloning fallback cannot take phoneme input for pseudowords | High if it fires | Medium | Text spelling + verification, or human pseudowords | Week 2 |
| Parser yield is poor across 108 files | Medium | High (no cut path) | Coverage report on day 1; `app:` YAML blocks; round-trip diff | Week 1 |
| Word counts undercounted → bigger audio and longer QA | High | Medium | Range planned; recount in week 2 | Week 2 |
| IPA → Kokoro symbol mismatch | Medium | Medium | Mapping layer + round-trip gate | Week 1 |
| Course bars below 90% (L1.02, L5, L6) | Certain (exists) | Medium | Course ticket; the app follows the course | Week 2 decision |
| Night-one start skips L1.01 for learners who need it | Medium | Medium | Hear-it misses trigger the full L1.01; placement Stage 1 | Pilot |
| Solo adults stall | Medium | High | Verifier `secure` without a helper; "checked by the app" wording | Pilot |
| Rebuild drift across machines | Low–Medium | Medium | Versions in the clip id; two-machine test | Week 1 |
| Pack downloads on poor data | Medium | Medium | Ask every time, MB shown, resume, sharing in v1.1 | Week 6 |
| No test phone | Medium | High | Week-0 decision D24 | Week 0 |
| Families review on mic + mixed audience | Low–Medium | High | Mic optional, explained; Urdu precedent | Week 8 |
| No telemetry, so efficacy is unproven | Certain | Medium | Pilot + opt-in export | Pilot end |

---

## 10. Decisions for Kamal

**W0** = needed before week 1. **W1** = blocks week 1.

| # | Decision | Recommended default | Blocks |
|---|---|---|---|
| D1 / D2 | Stack; role not age | **Decided** (fixed) | — |
| D3 | Ask age ever? | No | — |
| D4 | Teens default to Track B | Yes, with a skin switch | — |
| D5 | Gate without a verifier | E6c → `provisional` (unlocks), extra re-check; UI "Checked by tapping" | W1 |
| D6 | Speech in v1 | **Constrained verifier is core in v1**, spike #1; Whisper not core; on device only | **W1** |
| D7 | Leitner rule | −1 box; two wrong → box 1; sittings | — |
| D8 | UI languages | v1 EN + UR; wave 1 confirmed by Play data | — |
| D9 | L1 notes and UI voice per language; Sara licence | Native reviewer per language; Sara only if licensed | week 5 |
| D10 | Donation link | None | — |
| D11 | Efficacy measurement | Pilot pre/post + opt-in export | week 8 |
| D13 | Reminders | Opt-in, weekly cap, off for Track A | — |
| D14 | Teacher mode | v1.1 | — |
| D15 | Accent | General American (matches af_heart) | **W0** |
| D16 | Phoneme speaker | Chosen by voice-match audition + same-person gate | **W1** |
| D17 | Name and icon | Age-neutral | week 7 |
| D18 | Mascot | Keep the Marko rig, re-skinned, Track A only | week 4 |
| D19 | Code licence | Open licence for code, CC BY 4.0 for content | week 2 |
| D21 | Pilot participants | 2 kids + 1 teen + 3 adults | week 6 |
| D22 | Research-recording mode | Debug/pilot builds only, consented, local | **W1** |
| **D23** | **General American native reviewer** (role: reviews IPA overrides, all pseudowords, Q4 sample; ~4–8 h per pack) | Paid freelance or volunteer, named before week 1 | **W0** |
| **D24** | **Buy or borrow a 2–3 GB Android 10 test phone** | Buy one (budget class) | **W0** |
| **D25** | Fallback if the same-person test fails: clone the speaker (Chatterbox / Qwen3-TTS) | Approve the spike in advance | W1 |
| **D26** | Slow mode | Pre-rendered 0.8× L1–L2 words (+5 MB) | — |
| **D27** | Course pass bars (L1.02 9/11, L5 5/8 and 6/9, L6 4/5) | Open a ticket on english-reading-course; Kamal or the course author decides | week 2 |
| **D28** | Grown-up gate = PIN instead of spoken number words | PIN | week 3 |
| **D29** | Night one starts at L1.02 A (L1.01 as embedded Hear-it + repair) instead of L1.01 | Yes | **W1** |

(D12 is merged into §11.)

---

## 11. Content work to commission

| # | Item | Size | Owner | By |
|---|---|---|---|---|
| C1 | Level 0 print-concepts module | ~3 short lessons | course author | week 5 |
| C2 | Generated pseudowords + native review | ~770 + markdown's own | build agent + GA reviewer | weeks 2–5 |
| C3 | Placement forms B and C (all stages incl. Stage 1 items) | 2 forms | course author | week 5 |
| C4 | g/p alignment for the lexicon; `heartIdx` for all **69** heart words | 5,763–9,238 words auto; 69 by hand | build agent; Kamal checks heart words | week 2 |
| C5 | `pron.json` overrides | ~100–300 (estimate) | build agent + GA reviewer | week 2 |
| C6 | Mouth-cue images | 44 | generated + reviewed | week 4 |
| C7 | `app:` YAML per lesson: bar, reteach step, error classes | 108 + 7 | build agent drafts; author reviews | weeks 2–4 |
| C8 | Track B real-world unlockables | ~2 per level L1–L4 | course author | week 5 |
| C9 | UI script EN (~200) + UR (~300) with icons | 500 lines | build agent + native reviewer | weeks 3–5 |
| C10 | L1 notes per tag × family; **Tier-2 glosses in Urdu** | 14 tags × 5 families; 360–650 glosses | author + native reviewers | Urdu week 5 |
| C11 | L5–L7 MCQ anchors, partner scripts, checklists, model answers, key terms | ~46 sessions | course author | L5 week 6; L6–L7 v1.1 |
| C12 | Pictures for Listen & Talk chunks and nouns (after-hearing only) | ~300 (estimate) | generated / OpenMoji | week 4 |
| C13 | In-app helper guide (5 screens) + judge's-card audio | 5 screens | build agent | week 5 |
| C14 | Heading normalisation PRs (from the coverage report) | per report | build agent | week 2 |
| C15 | Course ticket on pass bars (D27) and on any missing Listen & Talk / Track B in L1–L4 lessons | 1 ticket | build agent | week 2 |
| C16 | Replacement words for Kokoro words failing three re-rolls | as needed | course author | ongoing |

---

## 12. How we will know it works

### 12.1 Metrics without telemetry

All on the phone. Exported to the pilot lead only by the user's choice.
- **Decoding** per level: share of secure / checked-by-tapping / mastered, pseudoword accuracy.
- **Comprehension**.
- **Fluency**: WCPM or pace.
- **Persistence**: days practised, sittings per week, returns after a >7-day gap.
- **Friction**: parked gates, pending items, repairs used, verifier unsure rate.

### 12.2 Pilot (from week 8, 6 weeks)

- **Participants**: Kamal's two kids, 1 teen, 3 adults (shop worker, solo, Urdu UI; grandparent; Urdu-literate adult). At least one adult cannot read Urdu.
- **Pre/post**: placement form A, then form B, plus the level check, judged by a person who is not the learner's helper.
- **Weekly**: a 10-minute check-in plus the Urdu Listen & Talk comprehension questions (§3.8).
- **Teacher agreement**: on 5 solo adults and 5 children doing L1.02–L1.04, a blind teacher marks each printed-word reading. App-credited items must agree with the teacher on ≥90%.
- **v1.1 bar**:
  - every child advances ≥1 placement step **without a helper judging**;
  - ≥4/6 still practising in week 6;
  - zero "childish" reports from Track B;
  - zero cueing incidents;
  - zero frozen screens;
  - nobody told they failed.
- Public copy may say only "piloted with N learners".

### 12.3 Gauntlet gates

**Method.** Fresh critics who did not build the app, plus named humans. Comparison material is anonymised. Rubric scored in both orders. A win = higher total in both orders and no row worse by more than one point. G0 and G7 are pass/fail.

| Gate | We vs | Rubric / test | Judges | When |
|---|---|---|---|---|
| **G0 Night one** | stopwatch | first letter sound heard and tapped ≤90 s; zero spoken history questions; icons-only role pick 5/5; blinded-text lesson one completes | parent critic + 1 Urdu-only non-reader | week 3, re-run week 8 |
| G1 Child first 10 min | Duolingo ABC | sound teaching explicit; **learner produces blending**; feedback kind; **no adult needed**; pacing; return wish | teacher + parent critics; kids observed | week 8 |
| G2 Interaction | Teach Your Monster | pass-by-guessing resistance; produced blending + repair quality; pause/resume; accent; narration clarity | teacher + engineer critics | week 8 |
| G3 Parent view | Khan Kids | where the child is and why; separate metrics; skip/placement; offline; install honesty | parent critic | week 8 |
| G4 Adult dignity | Learning Upgrade | nothing child-coded; real texts; hidden adult profile; privacy; night one | parent+adult critic + 2 pilot adults | week 8 |
| G5 Audio | Sara clips (reference) | clarity, naturalness, **one-teacher consistency, the s-a-t → sat join**, phoneme purity, loudness spread | audio critic + 5 naive parents + GA reviewer | week 3, re-run week 8 |
| G6 Listening | Read Along helper behaviour | false credits on planted errors; frustration; no frozen screen; handover | engineer critic + Kamal | week 6 |
| **G7 Rule audit** | DESIGN.md §2 + fixed decisions | every row of §2.3 pass/fail, incl. the whole-word-repair trace and per-lesson bars | teacher critic | week 8 + every release |

A lost gate turns its top two findings into the next week's first tasks, and the gate re-runs.

---

## Appendix: source index

**This folder** (`/home/oye/Documents/free_work/personal-agent-v2/vault/research/read-english-app/`): RESUME.md, decisions.tsv, research-01…05, plan-v1.md, critics-round-1-{teacher,parent-adult,engineer,audio,auditor}.md, bar/*.json (Read_Along_Kids_Books.json is a different product).

**Course**: `/home/oye/Documents/free_work/english-reading-course/` DESIGN.md; course/level-0/placement-test.md (Stage 0–4 rules, HT 2017 table, DIBELS administration rules, self-test version), screener.md, urdu-speakers.md, guide-tutors-parents.md; course/level-1…7/lessons (108) and mastery-check.md (7); tools/decodable.py; LICENSE (CC BY 4.0).

**Urdu app**: `/home/oye/Documents/free_work/urdu-reading-course/mobile/src/*.js`, mobile/tools/drive_all.py, ui_audit.py, scripts/listen_judge.py, voice_studio.py, store/PLAY_CONSOLE_CHECKLIST.md, research/09, 10, 12.

**Canvas plan**: `/home/oye/Documents/free_work/personal-agent-v2/vault/research/english-canvas-tutor/v6-changes.md` (5-example helper qualification), decisions.tsv.

**External**: the URL lists in research-01 (competitors), research-02 (TTS: Kokoro, Piper, Blizzard 2013 licence, sherpa-onnx, Chatterbox, Qwen3-TTS), research-03 (whisper.cpp, Moonshine, charsiu, Azure, SpeechAce, DIBELS PDF), research-04 (Play Families, COPPA via JD Supra, ICO code, accessibility studies) are carried over unchanged; see plan-v1.md's appendix for the full list. Store listings: apps.apple.com ids 1378467217, 1440502568, 828392046, 726696040.
