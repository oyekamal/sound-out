# Critic round 3 — claims auditor (plan-v3.md)

Scope: all of plan-v3.md (read in full) against research-01..05, DESIGN.md, placement-test.md, 108 lesson files (counted: 14/14/18/16/16/16/14 = 108, matches), bar/*.json, decisions.tsv, critic round-2 files. Recomputed every sum I could.

## Prior-round classes: status

| Class | Status |
|---|---|
| Heart-word count (69 = 24+29+16) | GONE. Recounted from DESIGN.md schedule: 24, 29, 16. |
| Phoneme count (44 = 24+20, +3 combos) | GONE. Lists enumerate to 24 and 20. |
| Pseudoword derivation lesson count | MOSTLY GONE. 60 lessons L1.03-L4.16, 4 mastery lessons, 56 checks, 560+80+80=720, 720-312=408 all reproduce. One residual (L4.15, below). |
| Gate-vs-recall | GONE. 11*.6^10*.4+.6^11 = 3.0%. |
| Placement misquotes | MOSTLY GONE. Tester script, Block A 26/<24, B 5, C 7, Stage 3 tiers, HT 50/94/132, DIBELS 3 s all match. Residuals below. |
| "measured" vs budget | MOSTLY GONE. Section 6.5 labels budgets; one budget has no mechanism (below). |
| Size-table bound mixing | NOT GONE. Kokoro pack ranges do not reproduce (below). |

## Findings

| Section | Claim | What the source / arithmetic says | Severity |
|---|---|---|---|
| 4.4 reviewer load | "about 3,000 Kokoro clips" for the L3-L5 packs; ~300 sampled | Plan's own 4.1 table: L3-L4 = 1,156-1,850 words + 510-850 sentences + 408 pseudo + 700-1,400 foils + 204 Tier-2 = 2,978-4,712; L5 = 1,688-2,610. L3-L5 total 4,666-7,322. 3,000 is the L3-L4 low end only. 10% sample = 470-730, not 300 | arithmetic |
| 4.5 / 4.1 recording kit | "~250 clips per hour including retakes" gives 19-28 h | Division is right (4,640/250=18.6; 6,950/250=27.8). The rate has no source in any research file. 250/h = 14.4 s per clip, while the same paragraph says every phoneme is recorded x3, there is a room-tone + reference /ae/ check each session, and sentences run ~4 s. "Every clip x3 takes" is ambiguous: if literal, takes are ~3x the clip count. Round-3 audio critic independently says 120-150/h (35-55 h) | unverified-as-fact |
| 0 vs 4.5 vs D16 | "About 20-30 studio hours" (0) vs "~19-28" (4.5, D16) | Two different ranges for one number | arithmetic |
| 4.1 Urdu voice | "~600 clips, ~3.6 MB" | Section 11 lists C9 (~300 Urdu UI lines) + C10 (~600 Urdu glosses, L1-L4) = ~900 lines to voice. 600 x 6 KB = 3.6 MB ties only to 600 | arithmetic |
| 4.1 demos | "Blending demos (23 lessons x 3)" | No derivation. My grep: L1 has 13 lessons with a Blend section; L2 has 13 with a Blend heading = 26, not 23 | unverified-as-fact |
| 4.1 foils | "800-1,500 E6d foil words not already in lexicon" | No derivation. Lower bound: 24 L1-L2 checks x 10 read-items x 3 foils = 720 before mini checks, E12 cards, placement Stage 3 (tiers 1-2 x 16 x 3 foils x 3 forms = 288). Pseudoword items need spoken pseudoword foils, which are not in the 560 | unverified-as-fact |
| 4.1 Kokoro pack MB | L3-L4 15-22 MB; L5 12-18 MB | Using the plan's own per-clip sizes (3.0 / 12.5 KB): L3-L4 = 15.8-24.2 MB (high end 2 MB short); L5 = 10.3-16.5 MB (both ends ~1.5 MB high). Plan silently uses human-voice KB for Kokoro; research-02 measured Kokoro words at 1,772 bytes. Gate 9 ("within the 4.1 ranges +10%") would be checking against ranges that do not reproduce | arithmetic |
| 4.1 L6/L7 row | Column "Words (range)" holds "18 / 11 (low end)" | Those are MB (research-05 delivery table: L6 ~18, L7 ~11), not word counts. Header mislabeled; "29-45" high end has no derivation | arithmetic |
| 4.1 basis sentence | "Ranges use research-05 per-level counts as the low end" | True for words (442+714=1,156; 938). Not true for sentences: L3+L4 = 385+297 = 682, plan's 510-850 is 682 +/-25%, i.e. the count is the midpoint | arithmetic |
| 4.1 undercount ratio | "9,238 / 5,763 = 1.6 undercount" | Ratio is right (1.603). But research-05 calls 9,238 a ceiling "if every word in tutor prose is voiced", not an undercount of learner-facing words. Label is the plan's own gloss | overstated |
| 4.1 shell size | Shell "~8 MB (estimate)" | Same research-05 §3 says the Urdu AAB is 27.8 MB with 15 MB of mp3, i.e. ~12.8 MB non-audio. 8 MB is research-05's guess for the new app, contradicted by its own Urdu data point. Labeled estimate, so mild | unverified-as-fact |
| 6.3 fallback | "per-lesson zips ... roughly +30% disk for block waste" | research-05 §3: 5,763 files at 4 KB blocks = ~23 MB vs 14.4 MB, i.e. +60% for words | overstated |
| 4.1 install table | Sums | 8+26-38 = 34-46; +3-10 = 37-56; +27-40 = 61-86 / 64-96. All reproduce. MiB vs MB 4.9% correct | fine |
| 4.1 / 8 | "Installed size read ... in week 3" | Section 8 puts installed-size measurement in week 7; week 3 has none | arithmetic |
| 1 days table | 61 lessons; 366/183/92-122 sittings; 12/17, 6/9, 3-4/4-6 months | 13+14+18+16 = 61 ok. 366/5 per week = 16.8 mo ok. 183 at 5/wk = 8.4 months, plan says ~9 (rounded up); 92-122 at 5/wk = 4.2-5.6 mo, plan says 4-6. Rounded up, not wrong | fine-but-uncited |
| 1 / 3.2 sitting model | 6 and 3 sittings per lesson, "from the sitting model" | Course L1.02 has 4 sittings (A 10 min, B 10, C 15, D 25-30). 6/3 are the plan's own, labeled estimate. DESIGN §4 says a lesson is 20-35 min | fine-but-uncited |
| 1.1 / 3.5 night one | Adult: A+B+C in 15 min, "says s, a, t, blends and reads sat, at, as, spells sat" | Course allots 10+10+15 = ~35 min to Sittings A-C (L1.02 header). Plan never says it compresses 35 to 15; only a Week-3 stopwatch (G0) will tell. Stated as the promise in 1, 1.1, 3.5, 12.3 | unverified-as-fact |
| 12.2 pilot | Proxy-validity read-aloud "after L1.04 and again after L1.08" within a 6-week pilot | L1.02-L1.08 = 7 lessons x ~6 sittings = 42 sittings = exactly 42 days at 1/day, zero slack. Track A children cannot reach L1.08 unless >1 sitting/day | arithmetic |
| 3.3 E6d / 6.6 | P(>=10/11)=0.6%, P(>=9/11)=3.3% at 50% | Binomials are correct (12/2048, 67/2048). Assumes 11 independent E6d items. Real checks are 5 real + 5 pseudo + 1 dictation (L1.02, L1.10, L1.13). At L1.02 the 5 real items are only 3 words (at, sat, as, at, sat): with repeated words answered consistently, P(>=9/11) rises to ~6.1%, not 3.3%. For >=10/11 gates the dictation makes it stricter (conservative) | arithmetic |
| 0 vs 3.3 vs gate 3 | "differ in the middle **and** the end" (0) / "and/or" (3.3) / "2x2 pattern" (gate 3) | The 50% figure holds only for a full 2x2 grid. If any set differs in one position only, a final-letter-only reader gets that item at 100%. 3-option sets (at/it/ap) and pseudoword/multisyllable items (L3.05 checks "zoric, hitane, flobin, pademic") cannot be 2x2 with a shared onset; no feasibility shown | unverified-as-fact |
| 3.3 E6d tricky words | "tricky-word E6d uses the regular-decoding foil" | L1.02's tricky words are "a" and "I" (one letter). A 4-option shared-onset grid cannot exist for them | unverified-as-fact |
| 4.1 pseudo derivation | 56 lesson checks x 5 pseudo | L4.15 "Reading the real world" check is a protocol narration (pass: 2 of 3 words), no real/pseudo set. So 55 at most | arithmetic |
| 3.5 Stage 3 | "pass >=14/16" | Faithful to the course, but course says "90% (14+)"; 14/16 = 87.5%. Inherited error, not flagged anywhere in the plan, and the plan's own default is 0.9 | arithmetic |
| 3.5 tester script | Quotes the script ("tell me the sounds you'd make") | Quote is exact. But the app Stage 3 is tap-the-spoken-word, so the learner is never asked to say sounds; the quote is placed under the app's placement as if it applies | overstated |
| 3.6 / 10 D27 | "L7.03 states no pass bar" | Only L7.07 states one ("4 of 6"). L7.02, .04, .08 etc. also give model answers and "self-check" prose with no bar. L7.03 is not the exception | overstated |
| 3.6 bars | "L3 '>=90%'" | Grep: all L3 lessons >=90% except two ">=95%" hits (L3.15 and L4.15) which are decodability targets, not bars. Fine. "L5 >=5/8 or >=6/9": L5.01-10 5/8, L5.11-15 6/9, L5.16 none. Plan lists no L5.16 gap | fine-but-uncited |
| 3.6 / 2.1 | L1.02 >=9/11, L1.03-L1.13 >=10/11, ">=4/5 19 times in 10 lessons" | Verified exactly (19; 10 lessons listed) | fine |
| 2.1 block counts | L1 Blend 13, L&T 14, TrackB 12; L2 13/13; L3 17/17; L4 14/15/15; L5 16/15/16 | All reproduce by grep | fine |
| 3.2 | "L2.06's 21 initial blends" | 21 confirmed (8 s-blends + 5 l + 7 r + tw). "5 sittings by family" is not derivable: families are 3-4 | unverified-as-fact |
| 0 D0a | "research-02 §5: neither Kokoro nor Piper produced isolated phonemes a judge could identify" | research-02 §5: Kokoro af_heart /m/ and /p/ "were identified correctly"; failures were /s/ /ʃ/ /θ/ /æ/. It does say "I cannot tell without a human listening", and plan does carry "unverified". "Neither ... identify" is too broad | overstated |
| 0 D0b | "research-03's 60% recall floor" | research-03 §8 item 4 gives "recall >= 60% (target), otherwise it just annoys". A target for the test protocol, not a floor of the product | overstated |
| 7 / 10 D15 | "General American (course table + speaker)"; "sound table ... General American" | No "General American" or accent specification anywhere in the course (grep over course/, DESIGN.md). Placement-test explicitly accepts /ɒ/ or /ɑ/, and L1.05 describes o as /ɒ/. There is no "course table" | fabricated (attribution) |
| bar table | Khan "Free, no ads, no account: Yes (parent account per Common Sense)" | Cell contradicts its own row label. Common Sense/Khan account is not in research-01 or the json; it comes from a round-1 critic's fetch (plan-v2 says so; v3 dropped the credit). Khan "~grade 2": research-01 says "around grade 2-3" | overstated |
| bar table | TYM "children can progress by guessing" | Quote is real but is a single justuseapp review via research-01, presented in the "Gate on real and pseudowords" cell as a product fact | overstated |
| 6.5 budgets | "tap-to-sound p95 <150 ms" | Budget is copied from research-05, whose mechanism was "pre-decode the lesson's clips into an AudioContext". Plan 6.3 rejects any WebAudio rewrite and uses seek-in-sprite on one Audio(). Budget kept, mechanism dropped; plan's week-1 device test is the only evidence | unverified-as-fact |
| 2.2 / 12.3 G4 | Track B calls heart words "tricky words" (2.1) vs G4 "nothing child-coded ('tricky words' ...)" | Direct contradiction in the same plan; DESIGN.md says "heart words" | arithmetic (internal) |
| Citations | research-02 §3 (espeakng-loader abort), research-03 §6 (adult confirm every gate), research-04 §5 (COPPA voiceprints, 22 Apr 2026), research-04 D6, research-05 §3 counts, 12%/70% reuse, Andika OFL, 1,463 files, 1.5 s watchdog | All check out against the source text | fine |
| Store data | Khan 4.80/131,337/201 MiB; ABC 4.25/3,810/212 MiB/2023-08-02; TYM 4.47/29,802/96 MiB/$8.99; 700 lessons; 127 units; $4.99-$59.99; 3.2/5 | All verified in bar/*.json and research-01 (bytes/1,048,576 gives 200.9/211.6/96.1) | fine |
| 4.4 audio evidence | 513 Hz /s/, 9.1 / 5.7 kHz, F0 215-238 Hz, seed/thread drift | Match critics-round-2-audio.md | fine |
| 5 / C5 | Engineer "several hundred to ~1,300 OOV" | Matches round-2 engineer (across 4,100 L3-L7 new words) | fine |
| L1-L2 word counts | 1,066 / 575 / 187 | My independent tokenizer (blockquote, table, bold/italic spans) gives 963 / 498 new / similar ballpark, so research-05 is the looser (higher) count. Order of magnitude holds | fine-but-uncited |

## Claims checked and failed

Checked about 95 numeric or sourced claims; 33 table rows above are failures or caveats. By class: 12 arithmetic/internal inconsistency, 9 overstated, 9 unverified-as-fact, 1 fabricated attribution, 2 fine-but-uncited with notes.

## Verdict

NO on handing to Kamal as-is.

The prior-round classes (heart words, phonemes, pseudoword lesson count, gate-vs-recall, placement quotes) are genuinely fixed. What remains is concentrated in the new recording-kit and size material, which was added in v3 without a derivation trail, plus a few attributions. Nothing here changes the architecture, but D16 (the fee Kamal signs off on) is built on a studio-hours figure with no source, and two decisions cite things the sources do not say. About an hour of fixes: re-derive the Kokoro clip count and pack MB from one stated KB/clip table, replace 250/h with a range labeled "assumed", delete the GA "course table" attribution, and add the L4.15/L1.02 caveats to the E6d maths.

## Three worst offenders

1. Recording-kit hours and clip counts (4.1/4.5/D16): the 250 clips/h rate is unsourced and conflicts with the plan's own x3 takes and session overhead; "20-30" vs "19-28" disagree; Urdu voice 600 clips vs ~900 lines commissioned; demos (23) and foils (800-1,500) have no derivation. This is the figure Kamal will pay against.
2. Kokoro pack arithmetic (4.4, 4.1): "about 3,000 clips" for L3-L5 is 4,666-7,322 on the plan's own table, and pack MB ranges do not reproduce from the stated KB/clip (size-table bound mixing is still present, and gate 9 would enforce the non-reproducible ranges).
3. E6d chance maths scope (3.3): the 0.6%/3.3% figures are correct binomials but are applied to checks that contain a dictation item, repeated words at L1.02 (6.1%, not 3.3%), and words (one-letter tricky words, multisyllable pseudowords, 3-option sets) for which no 2x2 shared-onset grid can exist. "Middle and the end" vs "and/or" vs "2x2" is stated three ways. The central guess-resistance claim is only proven for the CVC examples.

Runners-up: night one "15 min" vs course's ~35 min for the same sittings; pilot cannot reach L1.08 in six weeks at one sitting a day; D15 "General American (course table)" has no course table behind it.
