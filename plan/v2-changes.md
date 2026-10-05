# plan-v1 → plan-v2: change map

Every critic-round-1 finding and lead decision, what changed, where it lives in plan-v2.md, and how a critic checks it. "L#" = lead decision number in the coordinator's brief. Rows marked **not changed** say why.

## Teacher (critics-round-1-teacher.md)

| # | Finding | What changed | Where in v2 | How a critic verifies |
|---|---|---|---|---|
| T0 | Blending is shown, never produced by the learner and corrected (E5 judge "none") | E5 rewritten: model once → learner sound by sound with successive-blending highlighter → says whole word → verifier/helper judges → repair with sounds one at a time; verifier is a v1 core feature (L1) | §3.3 E5, §5.1–5.3, §2.3 row 3 | Read E5 steps; G1/G2 rubric row "learner produces blending"; pilot teacher-agreement test ≥90% (§12.2) |
| T0b | Solo adult can reach "Checked twice" without blending aloud | `secure` now requires verifier `clear_yes` on real words + delayed re-check; E6c-only gates are `provisional` and labelled "Checked by tapping" | §3.5 state table | Gate-reducer tests (§6.8 item 5) |
| T1 | Universal repair is to say the whole word | Repair 1 = sounds one at a time; repair 2 = first sound modelled; whole word only after a re-attempt; reader tap-a-word plays sounds first; build fails on whole-word audio between a failed attempt and the next | §2.3 row 1, §3.3 E5/E9, §6.3 gate 7, §6.8 item 4 | Run the audio-trace test; read a 3-error session trace |
| T2 | L1.02 sitting A has spell with no blend; snapshot test would fail on real JSON | Sitting A steps = `hear, meet, trace, mini`; blend+spell from sitting B; snapshot test runs over real L1.02–L1.12 JSON; mini-checks are repeat triggers only | §2.3 row 3, §6.2 schema example, §3.5 | Inspect L1.02.json snapshot; run the test |
| T3 | Trace optional, off for Track B; paper self-check; no b/d/p/q handling | Trace on by default for all Track A and Track B Level 1 (skippable, rule 11 kept); stroke scoring defined (start, count, order, direction, checkpoints, end); paper unscored; new E23 b/d/p/q exercise | §3.9, §3.3 E4/E23, §2.3 row 11 | Read scoring list; settings test; E23 in warm-ups from L1.09 |
| T4 | Isolated phoneme production self-judged; Urdu adult can't hear own v/w | New E22 ear-training minimal pairs before production; v1 self-compare labelled practice; v2 record-and-compare via verifier phoneme competitors (L1) | §3.3 E21/E22, §5.3 row "Isolated sounds" | Check labels say "practice"; pilot discrimination check |
| T5 | Listen & Talk incomprehensible for ESL beginners; "talk" is MCQ reading | Honest version: 2–3 sentence chunks, picture after hearing, Tier-2 gloss spoken in UI language, 10-s recorded answer labelled "speaking practice, not reading", shadowing for solo adults, prompts only in helper sessions (L7) | §3.8, C10 | Pilot: 2 literal Urdu questions ≥80% |
| T6 | Pacing rule only L1; warm-up + Listen crowd out blending | One new GPC (or ≤5 new words) per sitting L1–L4; Track A warm-up ≤3 cards; Listen & Talk on alternate-day sittings; sitting budget lint fails >8 min | §3.2, §3.6, §6.3 gate 8 | Run the budget lint; one parent times 5 days |

## Parent + adult (critics-round-1-parent-adult.md)

| # | Finding | What changed | Where | Verify |
|---|---|---|---|---|
| P0 | Night one is an English test before any learning | First launch → role tap → L1.02 Sitting A; no spoken history questions; placement opt-in; nickname/PIN/mic deferred; exit check ≤90 s to first letter sound tapped (L3) | §3.4, §1.1, §12.3 G0 | Stopwatch a non-reader on the test phone |
| P0b | Stage 1 picture vocabulary measures English words, not sounds | E1 uses spoken words, no pictures; Stage 1 placement uses the file's oral items | §3.3 E1, §3.4 | Inspect E1 items |
| P1 | Child can't pass a gate in a home with no English reader | Helper optional; verifier `secure` unlocks; cut path E6c `provisional` also unlocks; UI never shows "provisional" (L1) | §3.5, §3.10, §0 | §6.8 item 5: child reaches L2 with no helper and no "provisional" string |
| P2 | Role cards ambiguous; singular child; 8-year-old passes spoken number gate | Cards redrawn ("Me" adult alone; "A child" + "more children later"), sound-off icon test 5/5; PIN gate replaces spoken number words (D28) | §3.4, §3.1, §10 D28 | Five Urdu-only adults sound-off; 8-year-old gate attempt |
| P3 | Shared phone shows adult profile; no gate on adult/delete | Child tiles first; adult profiles behind lock tile + PIN; destructive actions PIN + hold-to-confirm with spoken warning (L5) | §3.1, §6.4 profiles | §6.8 item 8 (8-year-old, 1 minute) |
| P4 | Child says wrong sound, parent cooking: screen waits | Self-repair then move on, item `pending` re-queued, never auto-passed; helper buttons exist only inside PIN-opened helper sessions; 20-s timeout | §3.3 E5 step 5, §3.5 "Unjudged items", §5.4 step 7, §3.10 | §6.8 item 9 parent-absent test |
| P5 | Voice-only navigation is a rule not a design; Punjabi gets Urdu | Auto-played instruction per screen (Track A, Track B L1–2); blinded-text audit; Punjabi/Pashto via Urdu UI stated as a limitation with a wave-1 option | §3.1, §7.1, §7.4, §6.8 item 7 | Blinded-text run of lesson one + restore |
| P6 | 27 MB is a quarter of the app; Wi-Fi default; no missing-pack screen | Full install matrix (~54–94 MB per ABI with listening, packs ~54 MB, whole ~108–148 MB); pack downloads "ask every time, show MB"; spoken missing-pack screen, review still works; listing size line | §0, §4.1 matrix, §3.13, §7.6 | Read matrix; airplane test at the L2→L3 boundary |
| P6b | Rupee estimate requested | **Not changed**: PKR data prices unverified; MB shown instead | §4.1 | — |
| P-verdict | Mother picks Khan/ABC because they need no adult | Addressed by P1 + verifier; G1 rubric adds "no adult needed" | §12.3 G1 | G1 run |

## Engineer (critics-round-1-engineer.md)

| # | Finding | What changed | Where | Verify |
|---|---|---|---|---|
| E0 | Parser sized from 4 files; ★ fields not in markdown | Parser on all 108 + 7 from day 1; week-1 exit = coverage report over 115 files; ★ fields come from reviewed `app:` YAML blocks (PRs to course repo), never inferred; round-trip diff (L4) | §6.2, §8 weeks 1–2, C7, C14 | Coverage report committed in week 1 |
| E1 | Schema demands Listen & Talk/Track B where course has none; word lists not in tables | Optional blocks; per-template expectations table from a count over all files (L5 has Track B 16/16; L6–L7 none; Listen & Talk 0 in L5–L7); parser handles `**label:**` and backtick lists | §2.1, §2.3 rows 6–7, §6.2 | Compare §2.1 to the coverage report |
| E2 | 90% gate contradicts lessons; 80% oracle would pass ≥4/5 | Each lesson's own bar parsed; 0.9 default; bars listed plainly (L1.02 9/11 = 81.8%; L1.03–L1.13 10/11; ≥4/5 ×19 mostly mini-checks; L5 5/8, 6/9; L6 4/5); course ticket D27; oracle per lesson below its own bar | §3.5, §2.3 row 4, §6.8 item 3, D27, C15 | Unit test enumerating reachable scores per lesson |
| E2b | L1.02–L1.03 can't have 3 fresh pseudo sets | Stated: L1.02 cannot; freshness from where the generator can (L1.03–L1.04, confirmed week 2); `freshSets:false` flag | §3.5, §6.2 schema | Generator report week 2 |
| E3 | Word counts undercount; IPA mapping layer missing | Counts restated as range 5,763–9,238 words, recount in week 2; `ipa2misaki.py` + vocabulary round-trip gate; week-1 IPA path test | §4.1, §4.2 step 3, §6.3 gate 3 | Week-2 recount; round-trip report |
| E4 | espeak fallback aborts, can't be caught | Fallback disabled in pinned env; OOV pre-check against misaki lexicon before rendering (L4) | §4.2 steps 1–2 | Render 20 known-OOV words: build stops with report, 0 silent files |
| E5 | Whole-bundle pre-decode blows memory; base64 bridge; pack/IDB drift; PWA path | Per-clip decode with 8 MB LRU + 3-clip lookahead; `fetch(convertFileSrc)`; launch reconcile; SW caches whole bundle files, shared slicing | §6.6, §6.4 reconcile | `dumpsys meminfo` in an L6 session; p95 tap-to-sound over 200 taps |
| E6 | Native plugin effort/RAM/16 KB/size unproven | Verifier is spike #1 (lead overrides "take it off the critical path"), with 6–10-day budget over weeks 1–2, RSS budget, `zipalign -P 16`, `bundletool` sizes; Whisper not core; model downloaded if >25 MB; E6c cut path documented | §5.2, §4.1 matrix, §8 weeks 1–2, §9 | `spikes/verify.md` numbers; go/no-go table end week 2 |
| E6b | Engineer's fix "ship E6b + E21, run plugin as a branch" | **Not adopted** as stated: lead decision L1 makes the verifier a v1 feature because child progression without a reading adult depends on it; the engineer's concern is met by the explicit cut path (E6c) and the week-2 go/no-go | §5.7, §8 | — |
| E7 | No schema/content migration story | Real `onupgradeneeded` ladder with fixture tests; progress keyed by lesson id + item text; `contentVersion` + `gpcHash` on packs and earned records; incompatible packs rejected (L4) | §6.4 | L1.05-edit upgrade test |
| E8 | No device; "measured" wording; week 1/7 overloaded; reuse is new work | Week 0 added with D24 test phone; §6.7 headed "budgets, not measurements"; G1–G7 moved to week 8; new-work modules named | §6.5, §6.7, §8, §6.1, D24 | Dated device list in repo |

## Audio (critics-round-1-audio.md)

| # | Finding | What changed | Where | Verify |
|---|---|---|---|---|
| A0 | Human phoneme voice → Kokoro word voice join unspecified/untested | Speaker chosen by match to af_heart (F0, pace, warmth); 48k→24k, low-pass/EQ to af_heart spectrum; centroid within 15%; 5 naive parents "same person?" ≥4/5 else cloning fallback spike (L2) | §4.4, §8 week 1, D16, D25 | `spikes/voice-match.md`; G5 |
| A1 | Loudness spec wrong (no target; 3.1 LU spread) | −18 LUFS integrated words/sentences; clips <0.4 s RMS −20 dBFS; TP −1.5 dBTP; one function for human and Kokoro; measured after Opus decode; sd <0.5 LU, human vs Kokoro within 1 LU | §4.2 step 6, §4.3 Q1 | Histogram over 200 decoded clips |
| A2 | Silence trim ambiguous | −45 dBFS detector, exact 40 ms head / 80 ms tail, 5 ms fades, Q1 windows 30–60 / 60–110 ms | §4.2 step 6, §4.3 Q1 | Q1 report |
| A3 | Pseudoword review by a non-native listener; open-ended Q3 | Mandatory GA native reviewer (D23) on all pseudowords; Q3 forced choice among 4 foils; IPA vocab round-trip | §4.3, §4.2 step 3, D23 | Reviewer sign-off per pack; error <2% on frozen 200 |
| A4 | Re-roll mixes voices; carrier crops import prosody; determinism not pinned | No per-clip speed, no carrier crops; human queue only for L1–L2 demo words; else IPA override → replace word via course ticket; torch/misaki/espeak versions in clip id; two-machine sha test (L2) | §4.5, §4.2 step 1, C16 | Render 100 clips twice on two machines |
| A5 | Slow mode via playbackRate pitch-shifts | Pre-rendered 0.8× L1–L2 word variants (+1,640 clips, +5.1 MB, ~25 min render); sentences word-by-word in slow mode; time-stretch library rejected with reason (L2) | §4.2 step 5, §3.12, D26 | F0 median of 0.8× vs 1.0× within 3% |
| A6 | QA blind to prosody; child sentence 2/5 unheard | Q4 rubric adds same-teacher/pace/intonation 1–5, naive parent rater; first week-1 listen includes all 50 Track A sentences | §4.3 | Parent scores 20 clips "one teacher?" ≥4/5 |
| A7 | listen_judge.py is Urdu-only | Stated; English prompts are a build task | §4.3 Q3 | Script diff |
| A8 | Kokoro ≥ Sara at word level (not a defect) | Kept as context; G5 now tests the join and consistency, not Kokoro vs Sara | §12.3 G5 | — |

## Auditor (critics-round-1-auditor.md, 27 rows)

| # | Claim | Fix | Where |
|---|---|---|---|
| 1 | "No local model produced a teachable /s/ or /θ/" | Replaced with the lead's exact qualified wording | §0 |
| 2 | Bars 9/11, 9/10 mislabelled | Real bars listed; L1.03–L1.13 = 10/11; 9/11 = L1.02 Check (81.8%) | §3.5 |
| 3 | Fabricated "no pass or fail" quote | Actual tester script quoted | §3.4 |
| 4 | Stage 4 after CVC + digraphs | "Only if Tier 3+ cleared"; passages A/B/C, discontinue rule, DIBELS rules | §3.4 |
| 5 | Bilal placed at L1.13 | Tier 1 13/16 < 14 → L1.02 per file | §1.1 |
| 6 | Stage 1 as tap games | File's deletion/substitution items, Correct + Automatic (2 s), not administered without verifier/helper | §3.4 |
| 7 | HT norms "not fetched" | Uses the table already in placement-test.md (G2 50, G4 94, G6 132 Fall) | §3.4, §5.8 |
| 8 | ~50 heart words | 69 (24 + 29 + 16) | §2.1, C4 |
| 9 | Leo finishes Level 2 in a month | 20–26 sittings ≈ L2.03–L2.06 | §1.2 |
| 10 | Pseudowords ~1,000 vs ~1,360 | One derived number: ~770 generated (+ markdown's own, counted week 1) | §4.1, §4.3, C2 |
| 11 | 45 phonemes listed as 44 | Exactly 24 consonants + 20 vowels = 44, plus 3 named combination clips | §4.6 |
| 12 | 22 demo lessons | 23 lessons × 3 = 69; week-1 pilot 10 | §4.1, §4.6 |
| 13 | Piper research-only overstated | Lead's wording: Blizzard 2013 Lessac licence clause 3.2, read by the lead 2026-10-05; amy/alba grey area | §4.7 |
| 14 | "27 MB" unqualified | Install matrix with estimate/unverified labels | §0, §4.1 |
| 15 | Listening model 40–123 MB | Whisper tiny 75 / base 142 MiB (v2 only); verifier model 5–40 MB unverified | §4.1 |
| 16 | "measured on the 2 GB phone" | "Budgets, not measurements" | §6.7 |
| 17 | "Nobody leads with offline" vs ABC listing | Changed to "no bar app leads with adults or a mastery check; Duolingo ABC lists offline" | §0, §7.6 |
| 18 | 127 vs 700 interpretation | Both reported, no interpretation | §0 |
| 19 | Absence claims | "Not found in research-01 / listings, not proven absent" | §0 |
| 20 | Qualification mis-cited | Cited to canvas v6-changes.md; helper optional | §3.10 |
| 21 | "no fifth tab" vs research-05 | Speak entry points inside tabs, as research-05 says | §3.1 |
| 22 | Fluency/morphology from L5 | Fluency from L2, morphology L4–L7 | §2.2 |
| 23 | Tier-2 360 | Range 360–650 | §4.1 |
| 24 | Illustrative word counts as facts | Removed; month section labelled illustrative and derived from the sitting ratio | §1.2 |
| 25 | Render time and clip counts underived | Derived from research-02 rates, labelled estimate | §4.2 step 8 |
| 26 | Andika licence stated plainly | "SIL OFL per research-05; verify" | §3.7, §4.7 |
| 27 | Base audio gate fails at own numbers | Base recomputed (~26 MB incl. slow variants); gate tied to the matrix +10% | §4.1, §6.3 gate 9 |

## Lead decisions not covered above

| L# | Decision | Where |
|---|---|---|
| L1 | Ladder provisional → secure → mastered; secure unlocks; verifier spike #1 and v1; E6c cut path designed with honest proxy label; E5 produced; spell after blend; Urdu-contrast production self-compare in v1, verifier in v2 | §3.3, §3.5, §5.2–5.7, §8 |
| L2 | Voice match, loudness/padding spec, same-person gate, cloning fallback, slow mode choice, re-roll rules, GA reviewer role, QA consistency rating, §0 wording | §0, §4.2–4.5, D23, D25, D26 |
| L3 | Night one is a lesson; opt-in placement with real rules; 90-s exit check | §3.4, §12.3 G0 |
| L4 | Parser on 108; optional blocks; L5–L7 session template; bars as stated + course ticket; L1.02 freshness; OOV pre-check; migrations; audio range; budgets wording; test phone week 0 | §2.1, §3.5, §4.1, §4.2, §6.2–6.7, D24, D27 |
| L5 | Parent fixes | see P rows |
| L6 | Auditor fixes | see table above |
| L7 | Teacher fixes | see T rows |

## Deliberate deviations and things not changed

- **L5–L7 Track B:** the brief said Levels 5–7 have no Track B. The count over the lesson files shows **L5 has Track B in 16/16**, while L6–L7 have none. v2 follows the files: Track B is expected in L1–L5 (§2.1).
- **"19 lessons state ≥4/5":** the course has 19 *occurrences* of ≥4/5, in 10 lessons (L1.01, L1.03–L1.09, L1.11, L1.12): sitting mini-check blend bars plus L1.01's check. v2 says this precisely (§3.5).
- **L1.01 order:** to meet the 90-second rule, night one starts at L1.02 Sitting A. L1.01's oral games are embedded as Hear-it items, and the full L1.01 runs as a repair. This is flagged as decision D29, not hidden.
- **Trace "on by default":** the teacher asked for compulsory tracing. v2 sets it on by default with a skip, because DESIGN.md rule 11 makes multisensory work optional.
- **Rupee cost estimate:** not added, because PKR data prices are unverified.
- **Appendix:** external URLs are carried by reference to plan-v1's appendix instead of repeated, to hold length. All internal paths are listed in full.
