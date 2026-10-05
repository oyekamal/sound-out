# plan-v2 → plan-v3: change map

R1/R2 = the lead's reversals; L3–L9 = the lead's numbered fix sets. Each row: finding → change → where in plan-v3 → how a critic verifies.

## Lead reversals

| # | Finding / decision | Change | Where | Verify |
|---|---|---|---|---|
| R1 | Human→Kokoro join rejected twice (audio r1, r2); Kokoro isolated /s/ centroid 513 Hz; no TTS gives a clean stop | One human GA female teacher voice for all of L0–L2 (phonemes, demos, words, pseudowords, sentences, A and B texts, English UI, slow takes). Kokoro af_heart from L3, handover announced once ("a new reader joins you"). The human keeps isolated sounds from L3 as the named "sound teacher". Presented as **D0a** with evidence, cost and the alternative (Kokoro words + recorded phonemes, B in rounds 1 and 2) | §0 D0a, §4.5, §10 D0a | Read §0; G5 handover rating |
| R1a | Spectral and F0 match targets are unmeasurable | Dropped. The speaker is picked for natural GA accent, pace and warmth against af_heart; the reasons are stated (no Kokoro reference for isolated sounds; in-word fricatives vary 5.7–9.1 kHz; voices never alternate inside an exercise) | §4.5 | Audition sheet: accent scores and blind pace/warmth ratings |
| R1b | Recording kit not costed | L0–L2 counts recomputed as ranges from research-05 per-level numbers: ~4,640–6,950 clips, ~19–28 studio hours at 250 clips/h, 8–12 sessions in weeks 2–5. Human-clip QA: 2 listeners, anchored scale, kappa, frozen ids | §4.1, §4.4, §4.5 | Recount (week 2) vs the range; session log |
| R1c | Kokoro non-deterministic without a seed (audio r2) | Seed per clip from the clip id, threads pinned, versions + seed + threads in the clip id, approved ids never re-rendered, two-machine bit-identity test | §4.2 step 1, §4.4 | 100 clips rendered twice on two machines |
| R1d | Loudness split at 0.4 s puts neighbours 4 dB apart; peaks hit the limit | One rule: −18 LUFS integrated for ≥0.4 s; shorter clips gain-set so a 0.4 s window centred on the energy peak reads −18 LUFS; −1.5 dBTP limiter after gain; checks on decoded Opus | §4.3 | Q1 class means within 1 dB; 95% within 2 dB |
| R1e | Fades eat stop bursts; blend gap undefined | 40/80 ms padding; stop-final fade-out ≥15 ms; a fixed 350 ms phoneme→word gap authored in the exercise timeline, not in clips | §4.3 steps 2, 6 | Spectrogram sheet; exercise timeline JSON |
| R1f | Reviewer load repeats on every rebuild | GA reviewer: 10% of Kokoro clips per pack + 100% of overrides and pseudowords, once per frozen pack version, skipped when ids are unchanged | §4.4 | Review log keyed by pack version |
| R1g | Clone fallback can't do pseudowords; 5-parent gate statistically empty | Both removed. D25 retired | §10 | Search plan: no clone, no 5-parent gate |
| R1h | Slow mode at 0.8× is a different render | Human slow continuous-blend takes for L1–L2 blend words; no slow mode from L3 in v1 | §3.11, §4.1, §4.2 step 5 | Clip inventory row |
| R2 | Verifier can't give yes/unsure/no (engineer); 60% recall vs 10/11 gate ≈3% pass (teacher, auditor) | v1 has no speech gate and no mic. New gate exercise **E6d** (read the word, pick from 4 spoken options sharing the onset, 2×2 foils, 6 s window, targeted repair with one-at-a-time sounds, two wrongs → review, no whole word before attempt 2). Honest proxy statement and guess maths. Roadmap: v1.1 record-replay; v2 CTC verifier (10–15 days, ≥60 items per class, native GA labeller, Kamal second rater, Urdu merges as practice). Reversal of research-03 v1 and research-04 D6 stated. Presented as **D0b** | §0 D0b, §3.3 E6d, §5, §10 | Final-letter-only oracle fails gates (≤0.6% at 10/11); proxy validity test §12.2 |
| R2a | Gate maths | Gate counts judged items only (timeouts excluded and re-presented); the lesson's bar applies; first attempts only (D31) | §3.6 | Reachable-score unit test; gate reducer tests |

## L3–L9 fix sets

| # | Finding | Change | Where | Verify |
|---|---|---|---|---|
| L3 | Shopkeeper: 15 min, no word (parent r2 defect 2) | Adult night one = L1.02 A+B+C via the course fast track: reads sat/at/as (E5 + E6d), spells "sat"; exit ≤15 min | §3.5, §1.1 | G0 stopwatch |
| L3 | Child night one lacks the game loop (Teach Your Monster bar) | Track A experience layer: new silent mascot Pebble (not Marko), village grows one piece per sound met, sticker + celebration every sitting (never withheld), minute-by-minute 8-minute script, "Show your grown-up" screen | §3.4 | G1/G2 vs Teach Your Monster |
| L4 | Siblings can enter each other's profiles; skip/placement ungated (parent r2 defect 3) | Child 4-shape pattern; "I already know this", placement, re-place, delete behind the grown-up PIN | §3.1 | Sibling test (9-year-old, 10 min) |
| L4 | Adult relaunch hits child avatars + an unset PIN (defect 1) | Adult-only phone opens straight to the lesson; mixed phone has two doors (Children / Me lock); adult PIN flow written; "tricky words" in Track B | §3.1, §2.1 | Relaunch ≤10 s; screenshot audit |
| L4 | Day-2 mic dialog | No microphone permission in v1, stated | §3.1, §7 | Manifest has no RECORD_AUDIO |
| L4 | Wrong role tap can't be undone (defect 5) | "Change who is reading" behind PIN; icons-only test with 10 adults + 10 children | §3.1, §6.6 | Human test |
| L5 | Install table mixes download/installed and lower/upper bounds (engineer r2 5, parent r2 4) | Download AND installed columns, ranges with upper bounds; no native libs in v1 (no ABI split, no 16 KB issue); pack prompts show MB each time; no rupees | §4.1 | bundletool + Android Settings in week 7 |
| L6 | 8-week scope too big (engineer r2 2, 7; teacher r2 6) | v1 = L0–L5; L6–L7 + C11 + E18/E20 in v1.1; "critical reading" is roadmap only and banned from the listing until then | §0, §2.1, §3.3, §7, §8, §12 | Listing text; pack list |
| L6 | No cut list | Ordered cut list for weeks 3–5 + never-cut list | §8 | Read |
| L6 | WebAudio engine is new code (engineer r2 4) | Keep the Urdu single `Audio()` + watchdog; per-lesson sprite + offsets JSON; week-1 seek accuracy test; per-clip fallback | §6.3 | Seek p95 <20 ms on device |
| L6 | backup.js drops L1.02 keys and apostrophe ids (engineer r2 6) | Id-format change spelled out (lesson keys, card kinds, hashed card ids, new stores, `read-english-1`); Urdu backups rejected; per-version upgrade functions; delete the db.js repair bump; round trip in week 3 | §6.4 | Round trip with "don't" + L1.02 |
| L6 | L7.03 no bar | Added to the course ticket D27 / C15 | §2.1, §3.6, §10, §11 | Ticket text |
| L6 | Unsigned manifest | ed25519-signed manifest, D32 | §6.4 | Bad-signature test |
| L7 | E5 is echoing (teacher r2 defect 1) | Learner says each sound **before** tapping; the tap plays the sound only as confirmation; repair = continuous blend ("sssaaat") from the human slow takes; L3+ uses ≤150 ms gaps + syllable chunks (stated as a v1 weakness) | §3.3 E5 | Audio trace: no grapheme audio before the learner's tap |
| L7 | Track A order omits spell/tricky/read/check; contradicts JSON (teacher defect 4) | L1.02 Track A sittings A–G and a typical lesson listed; the §6.2 JSON matches; budget lint ≤8 min | §3.2, §6.2 | Lint on real JSON |
| L7 | b/d/p/q before shapes known (defect 3) | E23 starts b/d from L1.09, b/d/p/q from L1.12; formation anchors first | §3.3 E23 | Lesson-gated exercise schedule |
| L7 | Child never writes from memory; 12% tolerance false-fails (defect 3) | Trace fades after 3 correct traces to write-from-memory; Track A tolerance 20%; formative only | §3.9 | Settings + scoring tests |
| L7 | Listen & Talk for Urdu-only children (defect 5) | Urdu one-line gloss spoken first, English chunk, picture after; recorded answer optional for the helper (a prompt card in v1, no mic); pilot A/B on picture before vs after | §3.8 | Pilot Urdu questions ≥80% |
| L7 | Days to end of L4 unstated (defect 4) | Table: ~366 sittings Track A (~12 months daily), ~183 Track B, fast track ~92–122 | §1 | Arithmetic from the §3.2 ratio |
| L7 | `parked` has no exit without a helper (teacher defect 2) | `still_learning` after the second park: next lesson unlocks, items stay in review, re-checked every 3 sittings, flag; never locked | §3.6 | Perfect- and weak-decoder oracle runs reach L1.06 bounded |
| L7 | Repair not matched to the error (defect 3) | E6d repair targets the foil chosen (vowel vs final) | §3.3 E6d step 4 | Audio trace per foil type |
| L7 | L5 gates with self-judged items (defect 6) | L5 scores machine-judged components only; a gate with zero machine items is not passed; E19 model-answer rubric as practice | §3.6, §3.3 E19 | Gate reducer test |

## Auditor round 2 (13 rows)

| # | Claim | Fix | Where |
|---|---|---|---|
| 1 | Gate vs 60% recall | Speech gate removed (R2); E6d maths given | §0, §3.3, §3.6 |
| 2 | Stage 1 targets "boy" | Stage 1 has non-word answers; helper-judged in a helper session, skipped otherwise (then Stage 2) | §3.5 |
| 3 | research-03 §6 departure unstated | Stated twice: the gate row in §2.3 and D0b in §0/§5 | §2.3, §5 |
| 4 | E6c 25% vs 50% | E6c removed; E6d 50% partial-knowledge case computed (0.6% / 3.3%) | §3.3 |
| 5 | Agreement test needs 10 learners, pilot had 6 | Pilot recruits 5 children + 5 Track B learners explicitly | §12.2, D21 |
| 6 | "very simple short stories" quote | Replaced with research-01's "stops at simple stories" | §0 |
| 7 | L2.06 = 20 blends | 21 | §3.2 |
| 8 | Pseudoword derivation over 61 lessons | 60 lessons, 4 mastery checks → 56 × 10 = 560; total 720 | §4.1 |
| 9 | Clip total high end overstated | Totals recomputed row by row | §4.1 |
| 10 | L0 0.8 MB unexplained | L0 187 words folded into the words row | §4.1 |
| 11 | Pack 13 vs 12.5 | Packs recomputed as ranges from component rows | §4.1 |
| 12 | Whole-app understates | Upper bounds carried through download and installed columns | §4.1 |
| 13 | Citation drift (60 per child; p50 from research-05; 16 KB claim) | 60 items per class in v2 gold set stated as the plan's own bar; p50 removed; 16 KB claim removed (no native libs) | §5, §6.5 |
| also | L3 Listen & Talk 18→17; L2 Track B 14→13; MiB vs MB; D20 gap | Corrected; MiB/MB noted; D20 listed as unused | §2.1, §0, §10 |

## Other round-2 findings

| Source | Finding | Change | Where |
|---|---|---|---|
| Engineer 1 | Gold set n too small; Kamal confounds labels | v2: ≥60 per class, GA native labeller, Kamal second rater, "undecidable" = no-go | §5 |
| Engineer 3 | OOV overrides unsupported; espeak banned not fixed | Day-1 misaki count over 9,238 words; system espeak-ng in Docker proposes IPA, which is reviewed, never rendered directly | §4.2 |
| Engineer 3 | IPA table ownerless | `ipa2misaki.py` owned by the build agent, week 1 | §4.2 |
| Engineer 7 | Coverage report can't fail | Yield target ≥95% for L1–L5 | §6.2 |
| Engineer 8 | Test harness can't run | Tests tagged auto/device/human; auto set green before week 4 | §6.6 |
| Engineer | Unsupported numbers (p50 <500 ms, 4/5 gate, model MB) | Removed with the verifier and the 5-parent gate | — |
| Audio 2 | F0 target at top of range; no accent criterion | F0 target dropped; GA reviewer scores accent features in audition | §4.5 |
| Audio | Q4 n=2, no anchors | Anchored scale, kappa on a 100-clip overlap | §4.4 |
| Parent r2 main | Day-2 mic + unsure loop dead end | No mic, no speech gate in v1 | §0, §3.1 |
| Parent r2 6 | Adult must say "tas" aloud in af_heart's voice | L0–L2 in the human voice; E6d is tap-based; "tricky words" | §4, §3.3 |

## Declined or changed from the brief, with reasons

- **The human voice for Urdu UI prompts.** R1 says the teacher voice speaks UI prompts. v3 has her speak the **English** UI prompts only. Urdu instructions and glosses need an Urdu speaker: the Sara clips if their licence allows, else a recorded Urdu voice (D9). A General American speaker cannot voice Urdu. This is a second language channel, not a second English voice.
- **Isolated sounds from Level 3.** R1 hands over to Kokoro at L3. v3 keeps the human for isolated sounds at L3+ (named as the "sound teacher"), because Kokoro has no usable isolated phonemes. This is presented in D0a, not hidden.
- **E6d repair vs teacher fix 7.** The lead gave E5 a continuous-blend repair and E6d a one-sound-at-a-time repair. v3 keeps both and explains why: in a check, a continuous blend would reveal the answer.
- **Picture after the chunk in Listen & Talk.** Kept per the lead. The teacher's picture-first suggestion is added as a pilot A/B, not adopted.
- **"Recorded answer for the helper."** No microphone in v1, so the "Talk" step is a prompt card in helper sessions until v1.1 record-replay. This is stated.
- **The grown-up gate for a non-reading mother.** The PIN uses digits, which most non-literate adults read. The child shape pattern is icon-only.
- **Rupee figures.** Not added, because data prices are unverified.
