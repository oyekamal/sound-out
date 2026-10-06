# plan-v3 → plan-v4: change map

Sources: plan-v3 addendum rows 6–10 (lead decisions) and the five `critics/critics-round-3-*.md` reports. The app is named **Sound Out** throughout (`store/NAME-ASO.md`). Each row: finding → change → where in plan-v4 → how a critic verifies.

## Teacher (round 3)

| Finding | Change | Where | Verify |
|---|---|---|---|
| Tap-gate options can't see the first letter; an onset-blind reader passes | The option rule is stated once: one option differs only in the first sound (b/d, p/q where taught), one only in the vowel, one only in the final sound (*sat: pat/sit/sad*). An onset-blind oracle must fail | §3.3 E6d, §6.2 gate 3, §6.6 | Onset-blind oracle ≤1.1% per L1.03–L1.06 gate |
| Repeated items; real vs made-up options give the answer away | No repeats in a check; real items get real options, made-up items get made-up options; lexicality oracle at chance; L1.02 check = 3 real + 5 made-up + 3 dictated | §3.3, §3.6, §6.2 sample, §6.6 | Gate 3 + lexicality oracle |
| Two-sound words had a broken option set | 3 options under the same rule: *at → it / an / am* | §3.3, §6.2 | Gate 3 on the sample JSON |
| Timeouts drop the slow decoder's items | 12 s for L1–L2, 8 s from L3; a timeout is "not judged"; a check needs judged items ≥ the bar's denominator and re-asks; more than 2 timeouts → "finish tomorrow", never passed | §3.3, §6.2 `minJudged` | Slow-decoder oracle passes L1–L2 |
| E5 self-report; the repair speaks the whole word | "I said it" labelled self-report on screen. E5 ends with a judged E6d pick before the word plays. L1–L2 repair = successive blending from a partial clip ("saaa"), never the whole word; L3+ repair per the addendum | §3.3 E5, §2.3 rule 1, §4.1 (partials) | Audio trace: no whole-target clip (stretched clips included) before attempt 2 |
| Bars below DESIGN's 90%; gates have no teeth | Each lesson's own bar applies, with course issue #1 referenced. Chance maths per real check composition. A second miss gives `still_learning` with the next lesson's new-sound sittings intact plus a spoken Urdu "Needs a person" in the parent view | §2.3 rule 4, §3.3 table, §3.6 | 80%-learner oracle over 13 lessons reported |
| 8 minutes is budgeted, not measured | Lint ×1.5 for child response time; 5 children stopwatched on Sittings B and C before freeze, p90 ≤8 min | §3.2, §6.6 | Stopwatch log |
| Vowel options measure the Urdu ear | Ear/eye split: a vowel-option miss plays the paired E22 item; an ear miss is not counted. A vowel contrast is used only after 5 Urdu-only listeners pass it at ≥90%. Stops recorded without schwa; a phonetician signs the mouth images | §3.3, §4.5, C6 | Validation set in week 5 |
| Listen & Talk measured the Urdu gloss | The gloss sets context without the answer (reviewed); questions are about the English passage, in English with picture answers; the gloss fades in the pilot | §3.8, C10 | Leakage review; English question score |
| L5 "pace" vs WCPM claim | L5 shows "pace" only; "100 WCPM" removed and banned from the listing | §0, §2.3 rule 8, §7 | grep |
| Formation never counts b/d | Bowl-side and stem-order scoring for b/d/p/q (formative) | §3.9 | Scoring test |

## Parent + adult (round 3)

| Finding | Change | Where | Verify |
|---|---|---|---|
| The 8-year-old is forced to trace s | Child quick-start: 5 tap-gate items in sitting 1; 5/5 runs the Stage 3 tap ladder and places her; stops after 2 misses (~25 s) for a non-reader. Two age paths inside Track A only through placement, stated | §1, §1.1 (Hamza), §3.5 | Hamza fixture placed above L1 in sitting 1 |
| Nothing to hand over versus Khan read-to-me | **Stories** tab: Sound Teacher read-to-me of the Listen & Talk passages with pictures, tap-read decodables, sound chant built from phoneme clips | §3.4, §3.1 tabs | G2 vs Teach Your Monster |
| The first Check is the shopkeeper's second quit | "Show what you know", with an Urdu explanation of made-up words; a miss → targeted repair + re-check next sitting, never sent back a sitting; the fast-track mini check is "Keep going?", never a test | §3.2, §3.6 | Adult night 2–3 walkthrough |
| The mother's view doesn't say what to do | "Tonight, ask her these 3 sounds", with the Sound Teacher's audio; results as pictures; village | §3.11 | 3 Urdu-only mothers answer "what do you do tomorrow?" |
| No PIN on a child-only phone; no recovery | The PIN exists only once an adult profile exists; arithmetic gate otherwise; reset = arithmetic gate + 24 h delay | §3.1, D28 | Child-only install reaches placement via the arithmetic gate; forgotten-PIN test |
| Sibling limits unstated | Pattern of 4 of 9 shapes (3,024), 3 tries → 30 s lockout, 10-min idle → doors | §3.1 | Sibling test |
| First launch confusing; a lock before any PIN | One screen on a children-only phone; doors only when needed; lock icon only once a PIN exists | §3.1, §3.12 | Icons-only test (10 + 10) |
| MB means nothing | Pack prompt shows MB and minutes at an assumed 1 Mbit/s (D36); "safe to stop"; no rupees | §4.1, D36 | Urdu pack string review |
| "Tricky words" is child-coded | Track B says "words to remember"; the G4 contradiction is removed | §2.1, §12.3 G4 | Track B string grep |

## Engineer (round 3)

| Finding | Change | Where | Verify |
|---|---|---|---|
| Audio() sprite seeking broken (Capacitor Range); timers can't hold gaps | Fetch sprite → `decodeAudioData` once at 24 kHz → `AudioBufferSourceNode.start(when, offset, dur)`; a core sprite (47 sounds, UI, partials, Urdu) always loaded; LRU of 2 lesson sprites; memory maths given | §6.3 | Week-1 loopback test: s-a-t→sat, gap p95 error ≤15 ms over 200 runs |
| Recording chain starts too late; no engineer | Audition + timed 200-clip pilot weeks 0–1; phoneme session week 1; L0–L2 weeks 2–5 at 150 clips/h; recording engineer named (D33); options recorded only after review | §4.5, §8, D33 | Measured clips/h; session log |
| voice_studio.py has echo cancellation and noise suppression on, webm, 16 kHz | Seven listed changes (constraints off, AudioWorklet 48 kHz 24-bit WAV, no import resample/trim, meter and room-tone check, numbered takes and selection, English scripts, local or DAW) | §4.5 | Diff of the tool; >8 kHz energy survives into the decoded Opus |
| Parser yield 72%; L5 has no machine checks | Yield reported per level; L5 free-response flagged; v1 gated content = L0–L4, L5 ships as practice until MCQ checks (C11 ticket) | §2.1, §6.2, D30 | Yield table in week 1 |
| "No native code" false | Plugins listed: filesystem, haptics, share, file-transfer (downloadFile deprecated since 7.1.0); no `.so` of our own | §4.1, §6.4 | package.json |
| Shell ~8 MB too low | 14–17 MB with ~315 pictures | §4.1 | Week-3 measurement |
| backup.js drops fields | Field table (track, unit→lesson, idx, kind, UI_KEYS, LIMITS, ids, format); deep-equality round trip on a fully populated fixture | §6.4 | Week-3 test |
| The service worker doesn't cache packs; persist() ignored | Runtime pack cache; lazy base with retries; persist() result shown | §6.4 | Offline L1 after storage pressure |
| 150 vs 350 ms gap; the at/it/ap option set | One gap: 350 ms, authored in the timeline; the option set fixed | §4.3 item 7, §3.3 | grep "150 ms" in gap contexts = 0 |
| 8 weeks, no slack; cut list stops at week 5 | 10 weeks, week 9 slack; cut list from week 3 to week 8, reaching the L5 and L4 packs and the PWA; never cut = L0–L2 human audio, tap gate, Track A/B skins; human-test recruitment in week 0 | §8 | Dated recruit list |
| Auto tests "green before week 4" while built in week 4 | "Green by the end of week 4, when its subjects exist" | §6.6 | — |

## Audio (round 3)

| Finding | Change | Where | Verify |
|---|---|---|---|
| The L3 repair mixes voices on one word | Two named characters (Sound Teacher, Reader); L3+ repair = Sound Teacher sounds → learner blends → Reader word only as confirmation after attempt 2; voice-resolution table; a tapped word plays its lexicon voice | §0 D0a, §3.3 E5, §4.4 | Same-word mixed-voice audio trace |
| Loudness threshold inside the word distribution; short clips overdrive | Judged on the trimmed clip before padding; the short-clip boost capped at +6 dB over the clip's own loudness; −1.5 dBTP limiter as hard cap; Q1 fails >2 dB limiting | §4.3 | Q1 report |
| No stop direction or recording spec | "Say the sound as if the word stopped", 3 takes, shortest clean burst; pop filter, room ≤ −60 dBFS, peaks ~−12 dBFS, retake rule; reviewer blind-labels stops | §4.5 | Reviewer labels; Q1 stop caps |
| 250 clips/h optimistic | 150/h, one hours figure: 33–50 h; the week-0 pilot measures the real rate | §4.5, D16 | Timed pilot |
| Seeding ≠ determinism | The guarantee is "approved clip ids never re-rendered; build fails if a frozen hash changes"; seed/threads/MKL as hygiene | §4.2 item 1 | Frozen-hash check |
| Rater statistics | ICC(2,1) ≥0.75 or weighted kappa ≥0.6, pre-set; second listener is a native speaker, not Kamal (D34) | §4.4 | Committed thresholds |
| Urdu voice unprocessed; licence open | Same post-process chain, resampled to 24 kHz; D9 closed in writing by week 3, else a human Urdu speaker | §4.3, §4.5 | Q1 on the Urdu set; LICENSES.md |
| Handover has no bar | 8 naive listeners, mean ≥4/5 "comfortable", at most 1 below 3, pre-registered | §4.4, §12.3 G5 | Rating sheet |

## Auditor (round 3)

| Finding | Change | Where |
|---|---|---|
| 250/h unsourced; "20–30" vs "19–28" | One rate (150/h, assumed until the pilot), one figure (33–50 h) in §0, §4.5, D16 | §0, §4.5, §10 |
| Urdu 600 vs ~900 lines | ~900 lines, 5.4 MB | §4.1 |
| Demos 23 lessons | 26 lessons with a Blend section × 3 = 78 clips | §4.1 |
| Option count not derived | Derived: 2,832 L1–L2 slots (floor 720), plan 900–1,800 distinct; L3–L4 3,438 slots, plan 1,000–2,000 | §4.1 |
| Kokoro "about 3,000"; pack MB don't reproduce | One KB/clip table; L3–L4 3,270–5,305 clips / 16.6–26.0 MB; L5 1,686–2,613 / 12.1–18.4 MB; 10% review = ~500–790 | §4.1, §4.4 |
| L6/L7 row mislabelled | Labelled as MB from research-05 | §4.1 |
| Sentences "low end" wrong | Stated as research-05 count ±25% | §4.1 |
| 9,238 called an undercount | Labelled research-05's ceiling if all tutor prose were voiced | §4.1 |
| +30% block waste | Removed with the per-clip fallback (audio clock) | §6.3 |
| Installed size week 3 vs 7 | First reading week 3, final week 8, the same in §4.1 and §8 | §4.1, §8 |
| Chance maths scope (L1.02 repeats, dictation, 2×2) | One option rule; maths per real composition (L1.03–L1.13 and L1.02 rows); L1.02 called the weak spot | §3.3 |
| 1–2-letter tricky words can't be E6d | Checked by E8 + dictation, never E6d | §2.3 rule 5, §3.3 |
| L4.15 has no made-up set | 55 checks → 710 generated; excluded from option slots | §4.1 |
| Night one 15 vs the course's 35 min | **Chosen: compressed course fast track, said so** (A+B+C via "Keep going?" after ≥90% mini checks; ~15 min target). Fallback A+B with "sat" on night two if the stopwatch shows >20 min for 3 of 5 adults (D35). Why: the shopkeeper's round-3 A rests on a word on night one, and the course allows merging sittings | §3.5, D35 |
| Pilot cannot reach L1.08 | Children measured after L1.04 (~18 sittings) and L1.06 (~30); adults after L1.04 and L1.08 (~21) | §12.2 |
| D15 "course table" | General American is the app's choice; the course names no accent (accepts /ɒ/ or /ɑ/) | §7, §10 |
| Stage 3 14/16 = 87.5% | Flagged, added to the course tickets | §3.5, D27 |
| Tester quote misplaced | Applies to helper-run stages only | §3.5 |
| "L7.03 no bar" | Most of L7 has no bar (only L7.07); L5.16 none; ticketed | §2.1, §3.6, D27 |
| Bar table: Khan account / grade / placement; TYM quote | Credited to the round-1 critic fetch; "grade 2–3"; Khan path "tailored to their age and previous performance" (Common Sense via the parent critic); TYM quote attributed to one justuseapp review | §0 |
| D0a research-02 wording; D0b "floor" | "/m/ and /p/ identified, /s/ /ʃ/ /θ/ /æ/ not"; "60% recall target for the test protocol" | §0 |
| Tap-to-sound budget had no mechanism | The audio clock now provides it | §6.3, §6.5 |
| L2.06 "5 sittings by family" | s-blends ×2, l ×1, r ×2, tw in the last = 5 | §3.2 |

## Declined or adjusted, with reasons

- **Teacher's "unlock only with the next lesson's new-sound sittings" + "needs a person":** adopted. Their stricter alternative, to block progression in no-helper mode, is not adopted, because a home with no English reader would stall (parent critics, rounds 1–3).
- **Teacher's E5 pre-answer "tap two letters then pick":** folded in as the E6d pick at the end of E5. The separate letter-order tap was dropped to protect the 8-minute budget.
- **Picture-first in Listen & Talk:** still picture-after, per the earlier lead decision. It remains a pilot A/B.
- **Engineer's "commission L5 MCQs now":** L5 ships as practice. The MCQ authoring is ticketed (C11) for v1.1, because writing it inside the 10 weeks would compete with the recording schedule.
- **Never-cut list:** exactly the three items the lead named. Night one and the Urdu instructions are not on it, because their pieces are covered by the three named items or are cheap.
- **Sound chant:** built from existing phoneme clips on the audio clock, so it adds no new recording.
- **Rupee figures:** still none, because data prices are unverified.
- **Length:** v4 is 8,855 words before the appendix, against v3's 8,856. To fit, the "Retired decisions" line in §10 and one risk row (course bars, now covered by D27) were dropped.
- **Critic round numbering:** the week-5 review is called "critic round 5". Round 4 is the next gauntlet pass on this document.
