# Round 2 critic: structured-literacy teacher

## Verdicts

1. **5-year-old, Urdu-first, mother cannot read English, 10 min/day: B (Teach Your Monster).** A as written has no adult to catch its errors. Its gate is either a speech verifier that has never been run on an Urdu-accented 5-year-old, or a tap check that does not test blending. B's known weakness, progressing by guessing, does less harm than A telling a child she is wrong when she is right.
2. **35-year-old non-reader, alone on a phone: A.** B is a monster game for ages 3-6 (listing), narrated in British English with no adult track. A has a Track B skin, Urdu spoken instructions, offline use and a hidden adult profile. This is conditional on the fixes below.

## Single biggest gap: no path credits blending without miscrediting it

- **Verifier path (plan 5.5, 3.5).** `clear_yes` recall is allowed to be 60%. The gate needs `clear_yes` on the real-word items at about 10/11 (91%). A learner who decodes every word correctly gets about 6.6/11 credits. Everyone else lands in `reteach` or `parked`.
- **Harm to the child.** Unsure and no look identical (5.1), so a child who blended "sat" correctly is told to "point to each sound... blend" again. That teaches her that her right answer is wrong.
- **Accent.** The gold set (5.6) uses Kamal's children. It has no accent-tolerance requirement. Urdu speakers say a retroflex /t/, merge v/w, and pronounce /æ/ and /ɛ/ close together. The competitors list includes exactly that vowel swap (`sɪt` for `sæt`), so the verifier is designed to reject the accent.
- **Cut path E6c (5.7).** The child hears /s/…/æ/…/t/ already separated and picks from sat/sit/sap/sip. She never produces or assembles the word. The candidates share the first letter, so hearing only the last sound halves the choices. That is guessing with partial knowledge, not 25% chance. Knowing the letters for /æ/ and /t/ is enough, which is E3 repeated. The follow-up "segment" step only taps three boxes that each play their sound, and checks nothing. The plan admits it does not measure reading print aloud, yet `provisional` still unlocks the next lesson. That breaks DESIGN rule 3 (blend) and rule 4 (a gate that tests blending).
- **What a teacher does.** Never mark a possibly-correct blend wrong. Let the verifier catch clear errors (`clear_no`, high precision) and not certify.
- **Verify.** Run a simulated perfect-decoder child through L1.02 to L1.06 at recall 0.6 and 0.3. Count sittings to `secure`. Run an E6c oracle that knows only two letter-sound pairs and cannot blend; it should fail.

## Further defects

### 1. E5 step 2 and the repair (3.3)
- **Wrong.** The child taps a grapheme and the app plays the sound, then she "says it". That is echoing, not retrieving the sound from the letter. Repair 1 plays the sounds "one at a time, with gaps", which is the hardest form of blending (stop-start). Teachers stretch continuously (sssaaat) and glide. A child who cannot blend gets the stimulus that already failed, twice.
- **Teacher would.** Cover the sound, point to the letter, and have her say it first. Then confirm. For a stuck blend, model successive blending (sa, then sat) with no gap and no whole word.
- **Verify.** An audio trace of one failed item must show a letter-first prompt before any grapheme audio, and a repair 1 clip with gap under 150 ms or successive blending.

### 2. `parked` has no exit for a child without a helper (3.5, 3.10)
- **Wrong.** The third miss `parked` the gate: "Never past a failed hard-prerequisite gate". Resolution needs a helper or a "repair mini-lesson". Ayesha's mother cannot judge English sounds and cannot pass the 5-of-5 judge's-card check.
- **Teacher would.** After two parks, reroute to the oral on-ramp, then a tap-only gate. Never lock.
- **Verify.** Run the oracle with the verifier at recall 0.3 and no helper. It must reach L1.06 in a bounded number of sittings.

### 3. Production is unjudged exactly where Urdu speakers fail (5.3, E22, E23, 3.9)
- **Isolated sounds.** Production of /æ ɛ ɪ/, v/w and th is "none" for the gate. E22 trains the ear only, and E21 is self-compare with nobody listening. The repair is generic even though the verifier knows which competitor won (vowel swap, dropped final sound).
- **Teacher would.** Pick the mouth cue and minimal-pair replay from the winning competitor.
- **b/d/p/q.** E23's "four rotated shapes" puts mirror foils in front of a child before the shapes are automatic. There is no stable anchor such as bat-and-ball, and no left-to-right print concept for a child whose mother cannot model it (C1 is adult-only and opt-in).
- **Letter formation.** Track A is tracing only. Spelling uses tiles, so a child never writes a letter from memory. Stroke scoring at 12% tolerance will false-fail a 5-year-old finger.
- **Verify.** Test Urdu-accented children on 20 minimal pairs; the repair must match the winning competitor.

### 4. The 8-minute, one-sound sitting does not hold the lesson (3.2, 1)
- **Cost.** One sound per sitting is a sound pace. But 64 lessons at about 6 sittings is about 380 days to the end of Level 4, and the plan calls the ratio an estimate.
- **Track A order omits steps.** It lists warm-up, a sound, 6-8 blends, then stop. Spell, heart words, Read it and the 11-item check appear in no sitting. Rule 3 needs spell after blend, and §6.2's JSON has it, so §3.2 and §6.2 contradict each other.
- **Time.** Hear, meet, trace, 6-8 produced blends at 15-25 s each, and a mini-check already reach 8-9 min, before heart words, spelling or Listen & Talk.
- **Teacher would.** Cut blends to 4-5 and alternate spell and heart-word sittings.
- **Verify.** Run the budget lint on real L1.02-L1.06 JSON with every DESIGN section 4 step; report days-to-L2.

### 5. Listen & Talk for a beginner (3.8)
- **Wrong.** English passages are played to an Urdu-only 5-year-old in 2-3 sentence chunks. The picture comes only after each chunk, though pictures before listening help comprehension and the no-picture rule is about decoding. The only Urdu support is the Tier-2 gloss. The "Talk" recording is heard by nobody.
- **Rule.** DESIGN rule 7 is met on paper only; the Urdu pilot questions measure comprehension and do not teach it.
- **Teacher would.** Picture first, a two-line Urdu summary, then the English passage.
- **Verify.** Urdu-only children answer literal questions in Urdu, with and without the summary.

### 6. Levels 5-7 on a phone teach little (3.3 E14-E20, 3.7)
- **Wrong.** E14 (echo reading) is self-judged. E18 (reciprocal teaching) and E19 (write to read) are "content self" with a key-term check. E15 needs a helper, so solo learners get "pace". A solo adult therefore gets a reader with MCQs and no corrective feedback on summaries, inference or fluency. L6-L7 MCQ anchors are v1.1, so v1 does not ship what the listing claims ("runs to critical reading").
- **Teacher would.** Drop the claim for v1, or ship L5 only, with a rubric-based model-answer comparison for E19.
- **Verify.** Count, per L5-L7 exit gate, the items that need a human. A gate with zero machine-judged items must not be scored as passed.
