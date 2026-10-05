# Critic round 1: structured-literacy teacher

Read plan-v1.md, DESIGN.md, the TMTR listing and the Common Sense page (fetched; it says nothing about error feedback). A is unbuilt; B is shipped with 29,802 ratings.

## Verdicts

1. **5-year-old, Urdu-first, parent 10 min/day: B (Teach Your Monster).** The child needs a tested loop and a parent who can run it; plan A as written asks the mother to pass a helper qualification, judge pseudowords from a "judge's card" and hear 5 planted errors, none of which exists yet, and its English-only passages and tips give an Urdu-first 5-year-old little she can use.
2. **35-year-old adult, alone, phone: A.** B is a monster game rated 4+ and aimed at ages 3-6 with a UK phases curriculum; no adult would sit through it, while A at least has a Track B, pseudoword gates and Urdu notes, even though it can never verify that she can blend aloud.

## Single biggest gap: blending is shown to the learner, never produced by the learner and corrected

DESIGN.md rule 3 is "hear -> see -> blend (read) -> segment". In the plan, the blend step (E5, section 3.3) is "tap each grapheme (sound plays), slide to blend, hear the word", judge: "none (modelling)". The app does the blending. The only machine-checked "reading" evidence is E6b: hear a word, pick its spelling from foils. That is spelling-by-ear (encoding), and it can be passed by matching first letters and last letters. The actual act, looking at "sat" and producing /s/ /a/ /t/ -> "sat", is checked only by a human helper (E6a, section 3.5 `pass_mastered`). The solo adult never has that act checked. A learner can reach "Checked twice" (section 3.5) without once blending a word aloud.

What a teacher does: the learner does each step (tap under the letter, say the sound with the model half a second ahead, slide and say), then the model fades to whole words alone.

How to verify: record 5 solo adults and 5 children (with a parent) doing L1.02-L1.04; a blind teacher listens and marks whether each printed-word reading was blended without letter names or "tuh". Pass bar: the in-app "credited" items agree with the teacher on at least 90%. Add a DOM test: no whole-word audio before a learner attempt on a blend screen.

## Further defects (6)

**1. The app's universal repair is to say the answer (violates rule 1 in spirit).**
- Where: section 5.1 (`unsure` -> "The model voice plays"), E9 reader "tap a word to hear it" (section 3.3), E9 no-mic fallback "read-aloud audio", section 3.11 "a hint, try again".
- Wrong: when the learner is stuck, the app reads the whole word. That is the cue, and it trains "tap and wait". The no-cueing lint only bans the words "guess" and "look at the picture", not the audio hint.
- Teacher: on an error, go back to the sounds: re-point each grapheme, model the first sound only, ask for the blend again, re-present the item two items later. Tap-a-word plays the sounds one by one; the whole word plays only after an attempt.
- Verify: scripted-error test that fails the build if any whole-word audio plays between a wrong attempt and the next attempt; 3-error session trace read by a teacher.

**2. Step order in the lesson schema breaks rule 3 and the plan's own test.**
- Where: section 6.2 example, L1.02 sitting A: `"steps":["hear","meet","spell","mini"]`, newGpc "s". Section 2.3 says a snapshot test asserts no spell step before blend for a new GPC.
- Wrong: a spell step with no blend, and a 5/5 "mini" check on one letter is a tap-recognition check that proves nothing about decoding. You cannot blend with one letter, so the plan splits L1.02 into sittings, yet sitting A already asks for spelling.
- Teacher: s alone: hear, meet, trace, sound-to-letter only. Spell and blend begin once a second letter is known (s + a). Spelling follows blending in the same or a later sitting.
- Verify: run the claimed snapshot test against the real L1.02-L1.05 JSON; it should fail today.

**3. Letter formation and spelling on a phone (E4, E7, section 3.8).**
- Wrong: trace is optional, off by default for Track B, "formation only"; Track A spells with a tile tray that supplies the letters; the paper option is self-checked "against the model" with no camera. b/d/p/q is the named Urdu-reader problem (DESIGN.md rule 9), and a tile you tap cannot show whether a learner reverses it.
- Teacher: a short compulsory trace (about 1 min) for each new letter in the first sitting in BOTH tracks, then dictation on paper in the first 2 lessons, with a printable letter card. Offer the full alphabet in the tray once five letters are known.
- Verify: compare b/d reversals in paper dictation at L1.13 for learners with and without compulsory trace.

**4. Isolated phoneme production is helper-only, and "self" judging cannot work for the sounds that matter.**
- Where: section 5.2 (helper only), E21 (judge: "self").
- Wrong: an Urdu-first adult cannot hear that her /v/ is /w/ or her /ae/ is /e/ by comparing her clip to the model.
- Teacher: ear training first (vet/wet, sat/set, ship/chip) with the tap judge, then echo-production with the model a beat ahead.
- Verify: a discrimination test (20 minimal pairs) before and after L1.02-L1.08 for 8 Urdu-first adults.

**5. Listen & Talk does not survive the phone, or an ESL learner (rule 7, E10).**
- Where: section 2.2, E10: English-narrated passage "above decoding level", English "friendly definition", "your turn" frames, 2 prompts; the no-mic fallback is "choose 1 of 3 sentences, then the model answer plays".
- Wrong: a beginner with no English gets incomprehensible input; "talk" is a multiple-choice read, which is reading, not speaking; and a model answer that plays after any choice rewards tapping. For adults there is also no one to talk to.
- Teacher: 2-3 sentence passages at the learner's oral level (concrete nouns, actions, a picture, which is allowed here), Urdu gloss on tap for definitions, shadowing ("say it after me") as the solo adult's production, and discussion prompts handed to the helper only when one exists.
- Verify: after each Listen block in the pilot, ask 2 literal questions in Urdu; an Urdu-first beginner should get at least 80%. If not, the passage is too hard.

**6. Pacing rule covers Level 1 only, and the sitting budget does not fit the 10-minute parent.**
- Where: section 3.2 ("One new GPC per sitting in Level 1"; Track A 5-8 min) against section 3.6 (6-10 warm-up cards) and rule 7 ("Listen & Talk is never dropped, only moved").
- Wrong: 6-10 review cards (2-3 min), a Listen block (5 min in the template) and hear/meet leave no time for blending in a 5-8 minute sitting. L2.6 has 20 initial blends with no per-sitting cap.
- Teacher: protect blending first: warm-up 3 cards, one new sound, blend 6-8 words, stop; Listen & Talk moves to a separate sitting on alternate days. Cap new items per sitting (one new GPC or at most 5 new words) in every level.
- Verify: lint that sums budgeted seconds per sitting and fails over 8 min for Track A; one parent times 5 days.
