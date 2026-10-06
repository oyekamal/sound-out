# Critic round 4: claims auditor (plan-v4.md)

Scope: plan-v4.md read in full (1,021 lines), against research-01..06, DESIGN.md, placement-test.md, all 108 lesson files (counted by grep, per level 14/14/18/16/16/16/14), bar/*.json, the Urdu repo files it cites, and the round-3 auditor and round-4 audio critic. I recomputed every sum, binomial and unit conversion in 3.3, 4.1, 6.3 and 12.2.

## Prior-round classes: status

| Class | Status |
|---|---|
| Heart-word count 69 = 24+29+16 | GONE. Recounted from DESIGN.md schedule. |
| Phoneme count 47 = 44 + 3 combos | GONE (no source in the course for "44"; research-02 uses it too). |
| Placement misquotes | GONE. Stage 0/1/2/3/4, "90% (14+)", self-test skip, H-T 50/94/132, /ɒ/ or /ɑ/ all match. |
| Pseudoword derivation | GONE. 60 lessons, minus 4 mastery lessons and L4.15 = 55; 550+80+80 = 710. L1.03-L2.13 = 24 checks, L3.01-L4.14 = 31, total 55. |
| Gate-vs-recall | GONE. 11(.6^10)(.4)+.6^11 = 3.0%. |
| Size-table bound mixing | MOSTLY GONE. 44-59 / 47-69 / 73-103 / 76-113 all reproduce (below). Kokoro L3-L4 16.6-26.0 MB reproduces exactly. L5 only with an undisclosed assumption. |
| "Measured" vs budget | MOSTLY GONE, except 33-50 h (see table). |
| Night one vs 35 min | GONE. The course's 10+10+15 = 35 min for A-C is stated; 15 min is a labelled target with a fallback. |
| D15 accent | GONE. Now "the app's choice"; course accepts /ɒ/ or /ɑ/ (verified, placement-test line 264). |
| Chance-pass scope | MOSTLY GONE. 1.1%, 0.1%, 14.5%, 3.5%, 0.04%, ~2%, 70%, 32% all reproduce. Residual below. |

## Findings

| Section | Claim | What the source or arithmetic says | Severity |
|---|---|---|---|
| 6.3 core sprite | Core sprite holds the 47 sounds, UI lines, partial blends and Urdu lines: "about 90 s, about 8.6 MB decoded" | The plan's own 4.1 sizes at 24 kbps (3 KB/s) give: Urdu 900 lines 5.4 MB = 1,800 s; English UI 1.8 MB = 600 s; partials 0.6 MB = 200 s; phonemes 0.12 MB = 40 s. About 2,600 s, not 90 s. Decoded Float32 at 24 kHz that is ~250 MB, not 8.6 MB. Only the 47 phonemes alone are ~25-40 s | arithmetic |
| 6.3 lesson sprite, memory cap | "~150 s each, ~14 MB decoded; LRU of 2; audio memory under ~40 MB" | Sound Teacher audio is 24.5-36 MB = 8,200-12,000 s across 29 lesson units (L0 + L1 14 + L2 14), so ~280-410 s per lesson, 27-39 MB decoded each. Two sprites = 54-79 MB, plus core, against a stated 40 MB cap and a 150 MB total budget. 150 s has no derivation. Risk row "audio-clock memory: Low-Medium" rests on this | arithmetic |
| 4.5, 0, 9, D16 | "One rate: 150 clips/hour" gives 33-50 h | 4,940/150 = 32.9, 7,460/150 = 49.7: division is right. But 150 is the top of the round-3 audio critic's 120-150 range; at 120/h it is 41-62 h. Round-4 audio critic adds fatigue. 4.5 says "assumption", but 0 ("The cost: about 33-50 studio hours"), risk table and D16 state it unlabelled. Urdu voice (900 lines) is outside the figure if no Sara licence | unverified-as-fact |
| 4.1 foil derivation | 2,832 slots "so plan 900-1,800 distinct" | Slots reproduce: 2,160+360+288+24 = 2,832 (24 checks x 30 x 3 sets). The step to 900-1,800 (32-64% unique) is asserted. L3-L4 3,438 to 1,000-2,000 (29-58%) uses a different ratio. Made-up-word items need made-up foils (never mix), and those are not "words already in the list"; whether they are inside 900-1,800 or the 560 is not stated | unverified-as-fact |
| 4.1 made-up counts | L1-L2 "312 + the markdown's own (about 250, estimate)" = 562 | 710 reproduces. The 312/398 split (240+72 / 310+88) has no stated basis for the 72/88 level-check/placement split. The ~250 is labelled estimate but 24 checks x 5 = 120 only | fine-but-uncited |
| 4.1 per-clip KB | "3.0 KB per word at 24 kbps with padding" | Sourced to one clip (audio critic: a "sat" at 2.8 KB, unpadded). research-02 measured 1,772 bytes on 10 trimmed Kokoro words; research-05 uses 2.5 KB. The table is a conservative assumption, not a measurement, and it is the base of every MB figure | unverified-as-fact |
| 4.1 units | English UI 200 lines = 1.8 MB | 9 KB per line, a size that appears in neither the stated per-clip table nor Urdu's 6 KB. Inherited from research-05. Mild | arithmetic |
| 4.1 L5 pack | 1,686-2,613 clips = 12.1-18.4 MB | Reproduces only if the "~200" extra clips are priced at 12.5 KB (Tier-2 lines). At 3.0 KB it is 10.3-16.5 MB (same issue round 3 found). The L3-L4 row prices Tier-2 at 12.5 KB too, so it is consistent, but the L5 "~200" is not described as Tier-2 | arithmetic |
| 4.1 L3-L4 Tier-2 | "204" | L3-L4 have 17+15 = 32 Listen & Talk lessons x 6 = 192; 204 = 34 lessons (includes the two mastery lessons, which have no Listen & Talk) | arithmetic |
| 4.1 word range | "research-05's per-level count is the low end; the high end is x1.6" | research-05: counts are learner-facing "new this level", and 9,238 is its own ceiling "if every word in tutor prose is voiced". Round 3's independent tokenizer got 963 / 498 for L1/L2, below research-05's 1,066 / 575, so research-05 may be the loose count, not the floor. The x1.6 is the all-text ratio, not a measured high end | unverified-as-fact |
| 4.1 install and totals | 14-17 + 30-42 = 44-59; +3-10 = 47-69; +29-44 = 73-103 / 76-113 | All reproduce (30-42 = 24.5-36 + 5.4). Low+low and high+high sums assume correlated bounds; stated as estimates. MB for Sound Out vs MiB for competitors is noted | fine |
| 3.3 chance table | L1.03-L1.13: 1.1%, 0.1%, 0.04%, 70%, 32% | Binomials correct: 11/1024 = 1.07%; 1/1024; (21/59049)=0.036%; .9^11+11(.9^10)(.1) = 69.7%; 32.2%. L1.02: 37/256 = 14.5%; 9/256 = 3.5%; 129/6561 = 1.97%. Cells are conditional on dictation outcome; the unconditional chance is never given. Course L1.03-L1.13 composition (5+5+1) verified in 9 of 11 files by grep | fine |
| 3.6 L1.02 check | "L1.02's check has 3 real words, 5 made-up, 3 dictated... no repeats" placed under "Bars, as the course states them" | Course L1.02 check: real = at, sat, as, at, sat (5 items, repeats); pseudo 5; dictated 1 ("at"). 9/11 matches, but the composition is the app's change, not the course's, and it is not marked as a deviation. The 14.5% figure applies to the app's version | overstated |
| 3.5 placement | "Placement above L4 lands in Level 5 practice" | Course: Tier 5 below 90% = Level 5; all five tiers pass and Passage C clears 132 WCPM = Level 6. Level 6 is not in v1 and is not mentioned | unverified-as-fact |
| 2.3 rule 10 | "Skip and placement sit behind the grown-up gate" | DESIGN rule 10: "'skip if you know it' = take the mastery check first". The row does not say the check is required before a skip | fine-but-uncited |
| 2.3 rules | 11 rows + 2 | DESIGN has 12 rules; rule 12 (honest citations) has no row, yet G7 says "every 2.3 row passes" against DESIGN 2 | fine-but-uncited |
| 0 D0a | "No text-to-speech produces a clean isolated stop like /p/" | research-02 §0/§5: Kokoro and Piper only, and "may be the judge as much as the model... cannot tell without a human". It also says Kokoro /m/ /p/ were heard correctly (once). Plan's evidence bullet omits the judge caveat | overstated |
| 0 D0b | "reverses research-03's v1 stack and research-04's D6" | research-03 §7 v1 (Whisper witness for CVC words) is reversed: true. research-04 D6 already says "Ship v1 with E6b + helper judging; add on-device ASR in a later release". D6 is not reversed on ASR. What v4 drops is helper-judged E6b as the gate | overstated |
| 0 D0b engineer | "10-15-day CTC project" | round-2 engineer file: KWS has no negative class/score (matches). The 10-15 days is not found in that file by grep; it may be in a different critic file | unverified-as-fact |
| 5 Whistle | "keyword words and pseudowords recognised" | research-06: blim/strag recognised (0.59-0.60); vop heard "VAP", fraim heard "Frame" with or without keywords; chote fixed only by biasing at 0.46. Words: sat 0.63, pin 0.73, ship fixed by biasing. So pseudowords were mixed (2 of 5 right as spelled). Also omitted: 8.9 s first-call warm-up | overstated |
| 5 Whistle | 16.9 MB, CPU only, Apache-2.0, arm64/armv7/WASM, cake to "Take" 0.83, ship, chote, 0.1-0.25 s, isolated sounds and letter names failed, sentences exact, spike 30 CVC x 3 speakers x 2 takes, go bar 97% / 1.5 s | All match research-06 | fine |
| 4.6 Piper | "Blizzard 2013 Lessac licence clause 3.2... read by the lead 2026-10-05" | research-02 says the licence text excludes commercial use but gives no clause number. "3.2" appears only in plan/decision files; labelled as the lead's reading | fine-but-uncited |
| 4.5 pitch | af_heart 215-238 Hz, /s/ centroid 513 Hz | Match critics-round-2-audio.md (not research-02). Cited to no file | fine-but-uncited |
| 1 time table | 61 lessons; 366/183/92-122 sittings; 12/17, 6/8.5, 3-4/4-5.5 months | All reproduce. 12.2: L1.02-L1.04 = 18, L1.02-L1.06 = 30, L1.02-L1.08 = 42 sittings. "L1.08 would not [fit in 42 days]" is wrong at exactly 42 (fits with zero slack); adult 7 x 3 = 21 reproduces | arithmetic |
| 2.1 counts | Blend L1 13 / L2 13 / L3 17 / L4 14; Listen & Talk 14/13/17/15; Track B 12/13/17/15; L5 Track B 16 | All reproduce by grep. L5 "4/6" (L5.01-10) and 5/8 vs 6/9 both present; L6 4/5 in 16 of 16; L7 only L7.07 "4 of 6". 19 hits of ">=4/5" in 10 L1 lessons | fine |
| 2.1 heart words | L1 24, L2 29, L3 16 | Reproduce | fine |
| 3.2 L2.06 | 21 initial blends; s x2, l x1, r x2, tw last | 21 reproduces (8+5+7+1). Family sizes 8/5/7 vs "5 new words per sitting": s-blends 8 over 2 sittings = 4, r-blends 7 over 2 = 3.5, l 5 in 1 = 5. OK | fine |
| 6.4 backup.js, voice_studio | echoCancellation/noiseSuppression true, webm; int(0,12), idx 0-500, track enum, 16 kHz import | Verified in the Urdu repo (voice_studio.py 353-357; backup.js lines 27-33). Capacitor ^7.x, filesystem/haptics/share only | fine |
| Bar table, store data | Khan 4.80 / 131,337 / 201 MiB; ABC 4.25 / 3,810 / 212; TYM 4.47 / 29,802 / 96 / $8.99; "over 700 lessons"; 127 units; Khan Spanish read-to-me; TYM ages 3-6, phases 2-5; LU $4.99-$59.99, 3.2/5 | All verified in bar/*.json and research-01. Khan account/placement are "via critic fetch", labelled | fine |
| Citations | research-02 §5 (judge), research-02 1.77 KB, research-03 §6 and §8 (60% target), research-04 §5 COPPA 22 Apr 2026, research-05 counts/9,238/18-11 MB, Andika OFL | Section numbers and content check out, except the D6 and judge-caveat issues above | fine |

## Claims checked and failed

About 110 numeric or sourced claims checked. 14 rows above fail or need a caveat: 6 arithmetic, 5 overstated, 4 unverified-as-fact (some overlap in class). No fabrication found. Prior-round fabricated item (D15) is fixed.

## Verdict

**NO** on handing to Kamal as-is, but narrowly. The classes that sank rounds 1-3 are fixed. What remains:

- One engineering budget (6.3 audio memory) that contradicts the plan's own size table by an order of magnitude on the core sprite and 2x on lesson sprites. It is a promise to a 2 GB phone.
- The fee Kamal signs (D16) is quoted at the best end of its own source range and labelled "assumed" in only one of four places.
- Two evidence citations in D0b and 5 say more than the sources do.

About an hour of edits: recompute sprite seconds from clip counts and re-derive the LRU or the cap; present hours as "33-50 at 150/h, 41-62 at 120/h" in D0a and D16; fix D6 and Whistle wording; mark the L1.02 check as an app change.

## Three worst offenders

1. **6.3 audio-clock memory.** 90 s core sprite and 150 s lesson sprites cannot hold the content 4.1 sizes (about 2,600 s core; 280-410 s per lesson). The "under 40 MB" claim and a Low-Medium risk rating depend on it.
2. **4.5 / D0a / D16 studio hours.** 33-50 h is 4,940-7,460 divided by the optimistic end of the cited 120-150/h range; the unlabelled restatements and the missing Urdu hours make D16 look firmer than it is.
3. **4.1 foil and per-clip assumptions.** 2,832 slots to 900-1,800 clips is asserted, made-up foils are uncounted, and every MB figure sits on a 3.0 KB/clip assumption one measured clip high versus research-02's 1.77 KB. The sizes are likely conservative but are presented as a derived table.

Runners-up: "pseudowords recognised" for Whistle; "reverses research-04 D6"; L1.02 check composition passed off as the course's.
