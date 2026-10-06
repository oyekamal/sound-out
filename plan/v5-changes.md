# v5 changes: finding → change → section → how a critic verifies

Sources: decisions.tsv rows (9)–(12) (lead), critics-round-4-{global, teacher, parent-adult, engineer, audio, auditor}.md. "§" = plan-v5 section. Declined or partial items are in the last table with reasons. plan-v5.md is 9,499 words by `wc -w`.

Note: decisions.tsv gained a row on 2026-10-06 11:00 (Kamal: build a prototype slice with Kokoro placeholder audio, human voice later). It runs in parallel and changes nothing in this plan; prototype audio is a placeholder, not the D0a voice.

## Frame change (row 9, Kamal: global, not Urdu-first)

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| F1 | Core instructions carried by ~900 Urdu lines; no English-only path (global critic, biggest lock) | Core = English only: ≤60 English UI lines, each ≤6 words with a fixed icon, every verb demonstrated once by Pebble; Urdu removed from base install | §0, §3.2, §4.1, §7.1 | Count UI lines in C9 (≤60); test "every screen works with `helperPack = null`" (§6.4); no Urdu clip in base audio table |
| F2 | First launch spoken in Urdu then English | "Who is reading?" (English + icons) → picture or PIN → optional "Help in your language?" grid (endonyms + flag, locale first, "Just English") → first sound | §3.1 | Walk the 4 steps; G0 run with a no-English child and no pack ≤90 s |
| F3 | Vocabulary explained only in Urdu | Tier-2 = picture + simple English definition + example from the course's Tier-2 bullets; definitions linted (C16) | §3.8, §11 | Open any L&T lesson with no pack; C16 lint output |
| F4 | Letter names never taught | E24 at L1.13 (course "letter names vs sounds"), 26 Sound Teacher clips, letter-name bingo in free play | §3.4, §3.5, §4.1 | L1.13 step list; 26 clips in §4.1 table |
| F5 | Listen & Talk relies on Urdu gloss first | English passage → picture after each chunk → English questions with picture answers → Tier-2 in English → gloss only with a pack, after the questions | §3.8 | Step order; gloss cannot leak (plays after answers) |
| F6 | `homeLang` stored but nothing reads it | `helperPack` field; readers listed (onboarding, loader, note filter, grown-up view, gloss step); null behaviour defined | §6.3 | Grep the five readers in the build; null-path test |
| F7 | Interference notes ship in core as Urdu | Notes move to helper packs, keyed to `l1_tags`; none for English-only | §2 rule 9, §7.2 | Pack lint; English-only profile shows no notes |
| F8 | No pack format, no recipe, no cost | Format (≈310 voiced lines + ≈30 notes, ≈2–3 MB), 7-step recipe with native review and a field check, ~2–3 speaker h + 6–8 reviewer h per pack (D38) | §7.2, §10 | Recompute: 60 + 40 + 177 (= 59 L&T lessons × 3) + notes; size at 6/9 KB |
| F9 | Languages: wave 1 Hindi, Arabic, Spanish, Bengali only | Launch packs ur, pt-BR, id (pilot sites); wave 1 order Spanish, Portuguese (BR), Hindi, Arabic, Indonesian, French, Urdu, Bengali, Vietnamese, Swahili, stated as an estimate to confirm with Play Console data | §7.2, D8 | Text says "estimate"; no market figures claimed |
| F10 | Personas and pilot all Pakistani | Personas: Ayesha (PK child), Rukhsana (PK adult), Lívia (Recife), Budi (Jakarta), Emma (Ohio native); pilot 8 children + 6 adults across PK, BR, ID, US, remote via WhatsApp + Play internal test | §1.1, §12, D21 | Count countries ≥3; recruit lists dated in week 0 |
| F11 | Test listeners Urdu-only | Vowel validation 9 non-native (ur, pt, id) + 3 native; handover 8 native + 8 non-native; intelligibility 5 non-native (5 L1s); stop test mixed | §3.4, §4.4, §4.5 | Listener composition in each test |
| F12 | "Mother's view" in Urdu, gendered | "Grown-up view", gender-neutral, English text + icons, pack adds language | §3.9 | Screenshot audit |
| F13 | Store copy and keywords Urdu-tinged | Title/short description unchanged (no Urdu); "Urdu to English reading" leaves global keywords; localized listings per pack language; note for NAME-ASO.md (file not edited) | §7.3 | Diff listing text; NAME-ASO note present |
| F14 | Accent unstated as a global choice | "General American is the app's choice", course accepts /ɒ/ or /ɑ/ | §7.1 | placement-test.md line 264 |
| F15 | Village art regional | Region-neutral set, checked by BR/ID/US testers in week 3 | §3.5 | Week-3 test record |
| F16 | English-reading parent's helper path hidden | Visible "I can help" card in the grown-up view (still gated) | §3.9 | Screenshot |
| F17 | Rule 1 (no pictures beside words) unexplained vs Khan baseline | "Why no pictures beside words?" card in the grown-up view | §3.9 | Screenshot |
| F18 | Sizes and prompts PK-specific (rupees, 1 Mbit/s) | MB + Wi-Fi recommended, Wi-Fi-only default, 200 kbps test, compliance adds LGPD and Indonesia PDP (our reading, not legal review) | §4.1, §7.3 | Prompt text; test log |

## Lead decision (10): voice boundary at Level 4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| V1 | L3+ repair joins human sounds and a Kokoro word (audio r1–r4) | Sound Teacher records L0–L3 incl. UI; Reader from L4 only; L4 repair = Reader chunks (IPA) → learner → fresh item → Reader word; no isolated sound in a Reader exercise; sound review cards from core | §0 D0a, §3.4 E5, §4.4 | Trace test with **no exception**: fails any exercise holding both voices |
| V2 | Hours quoted only at 150/h (auditor) | L0–L3 = 6,670–10,190 clips, 44–68 h at 150/h, 56–85 h at 120/h, shown in §0, §4.5, §10 D0a/D16, §9 | §0, §4.1, §4.5, §9, §10 | Recompute: L0–L2 4,836–7,349 + L3 1,833–2,840; ÷150 and ÷120 |
| V3 | Alternative for Kamal | D0a-alt: human records all v1 (L0–L5) = 10,400–16,300 clips, 70–109 h / 87–136 h; lead's ~10k/~65 h is the low end | §0, §10 | L0–L3 + L4 human (2,082–3,483) + L5 (1,686–2,613) |
| V4 | L3 audio and the pack | L3 human audio (1,830–2,840 clips, 9.5–14.4 MB) sits in the L3–L4 pack with Reader L4 | §4.1 | Size table rows |

## Lead decision (11): 2×2 tap-gate grid

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| G1 | Answer is the hub of its option set (teacher r4 defect 1) | Options T / F / X / FX; first position always varied; second axis vowel in half the items, final in half | §3.4 | Medoid oracle at 25% ± 5 per item (§6.4) |
| G2 | Answers and foils recorded weeks apart (timbre cue) | Option sets generated and reviewed before each level is recorded; T, F, X, FX in the same session | §3.4, §4.5 | Session ids in the clip manifest; take-fingerprint oracle at chance |
| G3 | Repairs played the target before the retry (vowel ear item; first-sound replay) | Vowel repair = mouth cue + non-target contrast; first/final repairs point to the letter; retry is a fresh item | §3.4 | Audio trace: no target, stretched take or partial + final between miss and retry |
| G4 | After a partial blend only 2 options remained (teacher r4 2b) | Retry is a fresh item with all four options | §3.4 E5 | Partial-aware guesser at chance on retries |
| G5 | Generator cannot fill L1.02–L1.04 (engineer r4 defect 1: 16 strings at L1.03) | Early-lesson rule: 3 options in a chain, answer mid-chain in ⅓ of items, lexicality may mix, repeats across sittings allowed; labelled "early-lesson check"; generator run on L1.03–L1.08 in week 1 | §3.4, §6.1 | Week-1 generator report; `checkKind:"early"` in JSON |
| G6 | New: the grid varies two positions per item, not three | Chance table recomputed per blind class; vowel/final-blind ~10.9% per check without, ~1.9% with a new **axis rule** (≥70% per axis across the lesson's judged picks); D40 surfaces the trade-off | §3.4, §10 | Recompute: 6/32 and 1/32 binomials; 176/1024 = 17.2%; vowel/final-blind oracles |

## Lead decision (12): sittings on demand, Stories, back-fill, doors, picture lock

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| S1 | Child finishes in 7 min with nothing to do (parent r4 biggest stop) | "One more?" after a passed mini check (course: one new sound per sitting); otherwise free play; optional daily cap (D39) | §3.3 | Reducer test: next sitting unlocks only after the mini-check bar |
| S2 | Stories nearly empty | All read-to-me passages of current and earlier levels unlocked; unlimited sound games (hear it, segment, rhyme, letter-name bingo) | §3.5 | Count unlocked passages per level (13–17) |
| S3 | Placement skips L1/L2 tricky words (teacher r4 4, parent r4 3) | Back-fill skipped tricky words as E8 cards within 2 sittings; skipped GPCs as ear-and-eye items in sitting 1 | §3.6 | Fixture: L2.03 placement has all 24 L1 tricky words in review within 2 sittings |
| S4 | Children-only phone has no doors; siblings share a profile (parent r4 1) | Doors whenever ≥2 profiles exist (two children count); picture pick names each child; "Add a child" on the doors screen | §3.1 | Sibling test, two children, one phone |
| S5 | 4-of-9 pattern too hard for a 5-year-old | Picture lock: 2 of 4 in order (12 orderings), default for Track A; shapes optional | §3.1, D28 | Sibling test with locks set and unset |

## Engineer r4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| E1 | Sprites decode to ~300 MB (biggest gap) | 20–30 s step sprites keyed by step, decoded on demand with decode-ahead; core = 53 sound clips + ≤60 UI lines; memory recomputed from §4.1: core ~15.8 MB, peak ~36 MB (~72 MB if `sampleRate` is ignored) | §6.2 | 0.49 MB ÷ 3 KB/s = 164 s × 96 KB/s; week-1 `dumpsys meminfo` at real sprite size |
| E2 | Timing claims without instrument; G0 clock undefined | Clock = process start → first correct tap; quick-start after the first sound; paper stopwatch week 1, app week 3; "5 samples = maximum, not p90" | §3.3, §3.6, §8 | Week-1 and week-3 logs |
| E3 | Recording chain: voice_studio rewrite, pilot types, L2 freeze, upload, live Q1 | Rewrite scheduled in week 0 (3 days) with upload, live Q1 and drift; 2-hour pilot covers words, made-up, options, sentences, stops, second-hour rate; L2 frozen week 3; hours-per-week table | §4.5, §8 | Week-0 pilot report per type |
| E4 | Reader QA misses made-up options | 100% review of made-up words, made-up options and chunks; ASR round-trip with lowest 20% to reviewer; Docker image built week 0; 20 planted errors, ≥18 caught | §4.2, §4.4 | Planted-error log |
| E5 | `db.js:44` coerces Track B to child; backup 40-key cap + regex; SCHEMA whitelist; render cost | Enum A/B with 100-read test; `lessons` dict cap 200, new regex, overflow throws; new stores in SCHEMA; counters in progress; fixture 61 lessons + 20k attempts | §6.3 | Round trip + render ms on the Android 10 phone |
| E6 | One phone; loopback rig unpurchased; old WebView | Two phones (Android 10, 13), 3.5 mm cable + recorder, speaker-route tap test, WebView floor stated | §6.2, §6.4, D24 | Purchase list; device test on both |
| E7 | Whistle spike pulls RECORD_AUDIO; overloads week 1 | Separate `spike` Gradle flavour; CI manifest diff on `store`; scheduled in week 9 slack | §5, §2 | CI job fails if `RECORD_AUDIO` in merged store manifest |
| E8 | Cut list saves no audio hours; "L4 pack" wrong | Audio cuts A1–A4 first (with clip and hour savings); cut 12 = L3–L4 pack (one pack), 12–24 h | §8 | Savings recomputed from §4.1 |

## Audio r4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| A1 | L3+ join renamed "confirmation" | Removed: voice boundary at L4, no-exception trace test (V1) | §4.4 | Trace test |
| A2 | Tap inside a sentence switched voice | Tap resolves to the sentence's voice | §3.5, §4.4 | Tap-resolution test |
| A3 | Loudness rule uncomputable < 0.4 s; Q1 contradiction | ≥0.4 s: −18 LUFS; <0.4 s: no LUFS, active-frame RMS (K-weighted, 10 ms frames, within 20 dB of max); Q1 class means within 1 dB on active-frame RMS for every class; +6 dB cap removed | §4.3 | Run on the 68 bakeoff clips: no undefined values |
| A4 | Handover bar without power or control | Paired test: Reader-L4 vs human-L4 sample, 16 listeners (8 native, 8 non-native), phone speaker, "same teacher?" + "comfortable?", pre-committed one-sided 90% lower bound ≥ −0.5 | §4.4 | Script, stimuli and threshold committed before rating |
| A5 | Stops: shortest-burst rule, one take for two positions, phone-speaker loss | Takes picked for cue retention on the phone speaker; separate initial/final takes (+6 clips); blind identification ≥90% before week 2 | §4.5 | Identification test record |
| A6 | No cross-session consistency; fatigue | Per-session reference script; F0 median ±10%, tilt ±2 dB, rate ±8% before acceptance; 90-min sessions (D41); pickups checked | §4.5 | Drift log per session |
| A7 | "ICC or kappa"; no non-native raters; workload unsummed | Both statistics on a set with 15 planted bad clips, recall ≥90%; 5 non-native intelligibility raters; workload ≈4,100–6,500 clips ≈10–16 h, ≤4 h/week | §4.4 | Planted-defect results; workload sum |
| A8 | Hash on encoded bytes | Hash on the approved pre-Opus 48 kHz WAV | §4.2, §4.3 | Build script |

## Teacher r4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| T1 | Defect 1 hub leak | G1, G2 | §3.4 | Medoid + fingerprint oracles |
| T2 | Defect 2 repair leaks | G3, G4 | §3.4 | Audio trace; partial-aware guesser |
| T3 | Defect 3: Sitting A has no judged step; tracing load | Judged trio (3 spoken trials, 3 options, 3/3 → village piece, random 3.7%); one trace + one from memory in L1.02–L1.04 | §3.3 | Random-tapper bot: 0–1 pieces in 5 sittings |
| T4 | `still_learning` promotes the sound | Missed sounds stay "learning": every warm-up, not counted, machine re-check every 3 sittings | §3.7 | Reducer test |
| T5 | Defect 4 placement | S3 back-fill | §3.6 | Placement fixture |
| T6 | Defect 5 Stories cueing; gloss first | Pictures after text heard; highlight follows the voice in read-to-me; decodables no highlighting, no picture before reading; non-decodable taps no credit; gloss after questions | §3.5, §3.8 | DOM and audio traces on Stories |
| T7 | Defect 6 adult night one: no print concepts | 3-minute print-concepts module before /s/ (C1 moved to week 1); missed mini check → "tomorrow"; day-2 retest; reversed-reading oracle; target ~18 min | §3.6, §6.4 | Week-3 stopwatch; reversed oracle fails |
| T8 | Proxy validity tested only in week 10 | Paper-prototype proxy test in week 3 (blind GA teacher, 5 + 5, ≥2 countries, ≥90%; <80% returns E6d to critics) | §8, §12 | Week-3 record |

## Parent-adult r4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| P1 | Biggest stop: nothing after 7 minutes | S1, S2 | §3.3, §3.5 | — |
| P2 | Defect 1 profiles and doors | S4, S5 | §3.1 | Sibling test |
| P3 | Defect 2 sizes told late | Install-time line lists later packs with MB; helper pack size on the grid; failed-pack screen; 200 kbps test | §3.1, §4.1 | Onboarding screenshot; test log |
| P4 | Defect 4 "Needs a person" dead end | Replaced by the machine-checked-twice path and an action ("play these 2 sounds together tonight") | §3.7, §3.9 | Grown-up view test: "what do you do tonight?" |
| P5 | Defect 5 PIN at the end of night one | PIN set at first adult launch, "Later" once | §3.1 | Onboarding walk |
| P6 | Defect 5 slow reader loops on the L1.02 check | Window 20 s after the first timeout; timed-out item re-asked at the end (early-lesson) | §3.4 | 14 s decoder oracle finishes L1.02 |
| P7 | Defect 6 Track B reward on the cut list; child-style art | Real-world unlockables moved to never-cut (C17); adult-styled art; Track B shows no village/Pebble/stickers; screenshot audit in week 3 | §3.9, §8, §11 | Cut list; week-3 audit |

## Auditor r4

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| U1 | §6.3 sprite memory contradicts §4.1 | E1 recomputation shown as a table | §6.2 | Arithmetic in the table |
| U2 | Hours at 150/h only, unlabelled in 3 places | V2: both rates everywhere | §0, §4.5, §10 | Grep "120/h" next to every hours figure |
| U3 | Option ratio asserted; made-up foils unplaced | "30–60% of slots (asserted)"; made-up foils counted in the option row | §4.1 | Count rules line |
| U4 | Made-up split basis | L1–L2 ~560, L3 ~300, L4 ~180 all labelled estimates | §4.1 | Labels |
| U5 | 3.0 KB/clip unlabelled | Labelled "assumed, conservative" with the 2.8 / 1.77 / 2.5 KB sources | §4.1 | Line text |
| U6 | UI lines at 9 KB inconsistent | UI and pack lines set at 6 KB (≤2 s), stated | §4.1 | Line text |
| U7 | L5 "~200" priced at 12.5 KB undisclosed | "~200 Tier-2 lines at 12.5 KB" | §4.1 | Line text |
| U8 | L3–L4 Tier-2 = 204 should be 192 | L3 102 (17 × 6), L4 90 (15 × 6) | §4.1 | 17 + 15 L&T lessons |
| U9 | Word range low end may not be a floor | Note: round-3 tokenizer ~10% fewer | §4.1 | Line text |
| U10 | Chance table conditional only | Unconditional column added (dictation 50/50) | §3.4 | Table |
| U11 | L1.02 check composition passed off as the course's | Marked "app change" with the course's actual composition; `"composition":"app-change"` in JSON | §3.4, §6.1 | L1.02-s-a-t.md Check section |
| U12 | Placement above L4 → Level 6 omitted | Course places at Level 6; v1 lands in L5 practice with "Level 6 arrives in an update" | §3.6 | placement-test.md |
| U13 | Rule 10 skip omits the check | "skip = take the lesson's check first" | §2 | DESIGN rule 10 |
| U14 | Rule 12 missing from §2.3 | Row 12 added; G7 says rules 1–12 | §2, §12 | Table |
| U15 | D0a "no TTS produces a clean stop" overstated | Judge caveat stated; claim limited to the models tested | §0 | research-02 §5 |
| U16 | D0b "reverses research-04 D6" overstated | research-04 D6 already deferred ASR; v5 drops helper-judged E6b as the gate | §0 | research-04 D6 |
| U17 | "10–15-day CTC" not located | Cited to critics-round-2-engineer.md line 15 (found) | §0 | grep |
| U18 | Whistle "pseudowords recognised" overstated; warm-up omitted | Made-up words "mixed" with each result; 8.9 s first call; test was Python, not the C API | §5 | research-06 table |
| U19 | Piper clause 3.2 uncited | "the lead's reading; research-02 gives no clause number" | §4.5 | Text |
| U20 | af_heart pitch, 513 Hz uncited | Cited to critics-round-2-audio.md | §0, §4.5 | Text |
| U21 | "L1.08 would not fit in 42 days" wrong | "exactly the 6 weeks with no slack, so children stop at L1.06" | §12 | 42 sittings = 42 days |

## Declined or partial, with reasons

| Finding | Status | Reason |
|---|---|---|
| Teacher r4-4: place one tier lower | Declined | The 2×2 grid removes the hub leak that made guessers place high (onset-blind 5/5 = 3%, ladder ≥14/16 ≈ 0.2%), and back-fill covers skipped content; an extra tier costs real readers weeks. Round 5 can re-raise with oracle data |
| Teacher r4-5: hide read-to-me text in L1–L2 | Declined | Lead decision 12 chose text with the highlight following the voice; mitigated by pictures after the text, no credit, and decodable readers kept separate with no highlighting |
| Teacher r4-1: 5 Urdu-only adults on option audio with print hidden | Replaced | Same-session recording removes the timbre cue at source and the take-fingerprint oracle measures any residue; a human hidden-print test can be added in week 5 if the oracle is off chance |
| Teacher r4-3: re-teach next sitting when trio missed | Adopted as written | — |
| Global: native iOS for the Ohio family | Declined for v1 | iOS stays v2; v1 serves iPad/iPhone through the PWA with a stated storage-eviction caveat |
| Global: en-US title "Learn to Read: Sound Out" | Declined | Brief keeps "Sound Out: Read English"; it carries no Urdu and works for ESL; localized listings carry local phrasing |
| Global: UK/Indian/Nigerian accent choice | Declined | General American stays the app's choice (Kamal's brief); a second accent would double recording |
| Global: MB only, no minutes | Partial | MB first, Wi-Fi default; minutes kept with "longer on slow connections" because the parent critic asked for time |
| Global: auto-pick language from device locale | Partial | Locale language is listed first; never auto-selected or auto-downloaded, per the brief's onboarding order |
| Global: art-skin option for children | Partial | One region-neutral set tested in BR/ID/US; any profile may switch to the Track B skin. A second child skin is not costed |
| Global: wordless E6d ritual, speech optional | Partial | Icons + Pebble gesture demos carry it; the English line still plays (the instruction set is the core) |
| Parent r4-5: first check real words only | Declined | Made-up words are the course's decoding test (DESIGN rule 4); the wordless demo and 20 s window address the "alien words" quit |
| Parent r4-5: daily reminders like Duolingo | Declined | DESIGN rule 10 (no streaks); reminders stay opt-in, ≤weekly |
| Parent r4-3: ask three 8-year-olds if Track A is for babies | Partial | Track B skin switch added; the question is left to the round-5 parent critic and the pilot |
| Engineer r4-8: decide the handover in week 4 | Declined | The Reader L4 render needs the week-0 Docker image and the week-1 `ipa2misaki`; the human L4 sample lands week 5 and the paired test week 6, with cut 12 as the fallback |
| Engineer r4-2: move quick-start after the first sound | Adopted | — |
| Audio r4-3: 12 Urdu-L1 listeners, non-inferiority | Replaced by lead's spec | 16 mixed native/non-native listeners, pre-committed bound (lead decision); non-native share reported separately |
| Audio r4 fix (b): Reader never plays in repair | Superseded | The boundary move to L4 makes Reader repairs Reader-only (chunks), which satisfies the critic's intent |
| v4 "Urdu tip" on Meet cards | Removed from core | Becomes a helper-pack interference note |
