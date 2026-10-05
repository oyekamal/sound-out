# Critic round 3: structured-literacy teacher (plan-v3 vs Teach Your Monster)

Read: plan-v3.md, DESIGN.md, the TYMR listing JSON, the Common Sense review (silent on guessing, offline and adult help).

## Verdicts

1. Ayesha, 5, Urdu-first, mother cannot read English, 10 min/day: **A**, narrowly. Urdu instructions, learner-led blending and tracing beat an English-instructed game, but only if a real 8-minute sitting is actually 8 minutes (defect 4); otherwise B's proven play loop wins.
2. Rukhsana, 35, non-reader alone on a phone: **A**. TYMR is a monster game for ages 3 to 6 with no adult track; A at least offers a private first word.

In both cases A's gate would credit non-decoders (see the gap).

## Single biggest gap: E6d cannot see the onset

E6d foils "share the onset and differ in the middle and/or end" (sat/sit/sap/sip). So the first letter is never tested, and a wrong first letter is invisible and even rewarded.
- A child who reads b as d, p as q, or misses the newest letter has no wrong-onset option to choose. She hears four /b/ words and picks among them. She passes.
- L1.03 to L1.13 each introduce 2 to 3 new letters, mostly as onsets. L2.06's 21 initial blends are all onsets. The newest GPC is the one thing the gate cannot check.
- b/d/p/q reversals live here; E23 trains them but the gate cannot catch them.
- The only productive onset check is the single dictated word in the 11-item check.

Teacher's fix: single-change foils. Each item gets one foil that differs only in the onset (including b/d and p/q reversals), one in the vowel, one in the final sound (sat: pat, sit, sap). Reading any one position then eliminates only one foil. Expected pass for a one-position reader falls to about 33%.

Verify: add an "onset-blind oracle" (decodes vowel and final perfectly, reads the onset as a random wrong letter). Today it should score 100% on every L1 check. After the fix it should fail.

## Defects

**1. §3.3 E6d, §3.6, §6.2: gameable by memory, lexicality and timeouts.**
- L1.02 has 3 real words, 5 pseudowords, `freshSets:false`, and the same words were just blended. A learner can match word shape, since "at" and "sat" differ in length. The two-letter words get only 3 options.
- Foils that are not in the lexicon (800 to 1,500 recorded "foil words not already in the lexicon") let a native English child pick the only real word without reading.
- Timeouts (6 s) are dropped as "unjudged", re-presented once, then discarded. A slow correct decoder (every adult beginner, every 5-year-old) loses exactly the items she needs time on. The remaining quick items are the memorised ones. No count of dropped items is shown.
- Do: all foils must be real-lexicon or all pseudo, matched per item; fresh items even in L1.02 (more dictation, not reuse); timeout at 12 s for L1 to L2 and 8 s after; more than 2 unjudged per check means "not enough evidence", not "passed".
- Verify: lexicality oracle (picks the real word) must be at chance. Slow-decoder oracle (all correct at 9 s) must not pass or fail on 3 items.

**2. §3.3 E5: blending is self-reported, and repair hands over the word.**
- "I said it" is a tap. Nothing hears the child say anything. Then "the word plays; same as you?" is an answer key followed by a yes/no she is rewarded for tapping.
- Repair on "No" plays the human continuous blend "sssaaat". That is the whole word, spoken. Rule 1 says repairs never start with the whole word. For a CVC the blend is the word.
- Do: say "learner-led blending" only for E6d. In E5, replace the post-hoc "same as you?" with a pre-answer choice: she must tap two letters in order at finger speed, then pick the word from the options before any audio plays. Repair with 2 sounds joined (successive blending: "sa" then add "t"), never the full stretched word.
- Verify: audio trace, no clip containing the complete target word between a wrong answer and the next attempt, including the continuous clip. The current trace test allows it.

**3. §3.6 gates: no teeth, and thresholds under DESIGN.md rule 4.**
- Bars are 9/11 (82%) and 4/5 (80%), against DESIGN's 90%. A child who really gets 80% of items right passes 10/11 about 32% of the time. A 50% half-decoder passes 9/11 3.3% of the time per gate.
- Failure never blocks: "still_learning" unlocks the next lesson on the third miss, and a failed delayed re-check does not relock. With no helper and no mic, a non-decoder is promoted to L1.03 on cumulative decodability she does not have.
- Do: no-helper mode may unlock, but it must keep the next lesson's new-sound sittings and add a distinct "needs a person" state in the Urdu parent view (not a silent flag).
- Verify: simulate an 80%-per-item learner over 13 lessons; report lessons cleared.

**4. §3.2, §3.4: the 8-minute sitting is budgeted, not measured.**
- Sitting A already fills 7:00 with one sound and no blending. B and C add warm-up, a trace x3 plus memory, blend, spell, the village animation and the sticker.
- Urdu plus English instruction lines play on every screen, leaving a 5-year-old no slack.
- Do: sum audio durations x1.5 for child latency in the lint, and stopwatch 5 children on B and C before freezing text.
- Verify: video each sitting, count minutes, report p90.

**5. Urdu contrasts, no mic.**
- E6d vowel foils (sat/sit/sap) ask an Urdu-first ear to separate /æ/ /ɪ/ /ɛ/. A child who decodes correctly fails because she cannot hear the foils. This is an ear score recorded as decoding, and it feeds "still_learning".
- "She says /s/; her mother taps to compare." The mother cannot judge /θ/ vs /s/, /v/ vs /w/, or the stop released without a schwa ("buh").
- Do: classify E6d failures as ear vs eye with a paired E22 item before a reteach; record stops clipped with no schwa (check 20 clips); have a phonetician sign the generated mouth images (C6);
- Verify: Urdu-only listeners (not the speaker) pass a minimal-pair set at 90% before the gate may use it.

**6. §3.8 Listen & Talk and Level 5.**
- The Urdu gloss plays first, then the English. Comprehension questions are in Urdu, target 80%. That measures the gloss. It builds no English listening comprehension and the Talk step ("tell your grown-up") is empty with a non-English mother. Fade the gloss (after the English chunk, then on tap only) and ask the questions in English with pictures.
- Level 5 fluency: "pace" is tap-through time; WCPM needs a helper; prosody has no measure. The bar table promises "to ~100 WCPM, morphology", yet the L5 gate scores only MCQ and morphology. A learner who skims by tapping passes. Rename it, never display it as fluency, and drop the 100 WCPM claim until a helper session or v2 evidence supports it.

## Lesser points
- Formation is formative only, so a b written as d never costs anything; check bowl-side and stem order for b/d/p/q.
- About 366 sittings to the end of L4 is a year of daily use with no streaks, no reminders for Track A and no helper. Plan for dropout.
