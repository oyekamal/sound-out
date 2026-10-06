# Critics round 5: teacher (structured literacy; 5-year-olds and adult ESL beginners)

Read: plan-v5.md, DESIGN.md, TYM store JSON, Common Sense TYM review (thin: awkward navigation, repetitive games, British narration, ~43 weeks).

## Verdicts (A = Sound Out as written, B = Teach Your Monster today)

1. **5-year-old, parents read no English, 10 min/day: B.** TYM is built and child-tested; A's lesson design is sounder, but its Listen & Talk is noise for this child (defect 4), spacing is unenforced (defect 1), and no child has met it.
2. **5-year-old native English speaker, US: B.** She knows letter names, TYM matches her phonics phases, and A withholds names to L1.13 (defect 6) for ~12 months to L4.
3. **35-year-old adult non-reader, alone: A.** TYM is for ages 3-6 with no adult register; A alone has a private adult skin, print concepts and real-world texts.

## Single biggest pedagogical gap

**Every "learned" signal is a same-sitting recognition tap, so nothing shows a sound or word is retained overnight or produced from print.** `checked`, village pieces, "One more?" and `rechecked` can all be earned from working memory in one binge, on spoken options. v5 hardened the option geometry; it still measures the wrong thing at the wrong time. A child can tap s-a-t correctly at minute 38 and not know /s/ tomorrow.

## Defects

### 1. §3.3 sittings on demand, §3.7 review in sittings
- **Wrong.** "One more?" appears whenever the mini check hits 4/5; the daily cap is optional (D39). Leitner boxes and "re-check 3 sittings later" count sittings, not days, so "checked twice" can be earned before lunch. Night one models this (~16 min, two sounds).
- **Teacher would.** Cap new sounds per calendar day (two child, three adult), not optional. Re-checks and warm-up retrieval must fall on a different day from teaching; after the cap, only free play and earlier review.
- **Verify.** Reducer test: a perfect bot over 10 hours gets at most 2 new sounds and no `rechecked` that day. Pilot: next-morning retrieval of yesterday's sounds, blind-teacher scored, against same-day mini-check scores.

### 2. §3.4 tap gate and early-lesson check
- **Wrong.** (a) Early-lesson checks let lexicality mix and repeat across sittings: a native child picks the one real word in "tat / sat / sas" without reading, and repeats are memory. This is exactly where G0 and the adult milestone are scored. (b) A learner with first letters and word shape alone scores 50% per item. (c) The 1.9% figure multiplies the axis-rule and check passes as independent; both come from the same coin flips. With 8 picks per axis, a 50% guesser clears 6/8 about 14% of the time. (d) A learner who cannot hear the vowel contrast (Urdu /æ/-/ɛ/, Portuguese /ɪ/-/i/) fails the vowel axis for ear reasons and sits in `still_learning`.
- **Teacher would.** Never mix lexicality, even early; accept fewer items. No same-day repeats. Make tile spelling at least half the items from L1.03: spelling from sound proves GPC knowledge without a mic. Compute pass rates by joint simulation.
- **Verify.** Lexicality-picker oracle at chance on early-lesson items (today it is the unique real word). Monte-Carlo of the axis rule on the real JSON. Week-3 paper test with the printed word hidden: 5 English-speaking and 5 non-English children must sit at chance.

### 3. §3.4 E5 blending and repairs (L1-L3 and L4+)
- **Wrong.** "I said it" is honour system, so blending is never produced where the app can see it. The L1-L3 repair plays "sssaaa" then says the last sound: the whole word is supplied before a retry that, early on, is "same, reshuffled". At L4+ the repair is Reader chunks, but chunks exist only for L4.12-L4.14. L4.01-L4.11 words ("coin", "burn") are one syllable with a digraph, nothing to chunk, and no isolated sound may play in a Reader exercise. The plan never says what the repair is for "coin".
- **Teacher would.** Repair by grapheme chunking ("c · oi · n") with human sound clips as their own step (Meet-card style), then tile-building of the failed word from audio, then retry. Define the repair per lesson type, not per level.
- **Verify.** Audio trace on every L4.01-L4.11 repair, each with its chunk plan; the list of L4 words with no valid plan must be empty. Add "oi" (L4.05) to the handover test.

### 4. §3.8 Listen & Talk, English only
- **Wrong.** For a learner with no English, the passage is above level, in a language they do not understand, and answers are one of 3 pictures that follow each chunk, so it is picture matching. The "≥80% with and without a pack" target passes on matching alone, and rule 8's second metric becomes invalid. Decoded words ("sat", "pin") get no meaning reveal after decoding, so she decodes noise.
- **Teacher would.** For no-English learners, replace the passage with 4-6 labelled-picture words drawn from just-decoded words, picture shown after the pick; do not call it comprehension. Passage comprehension only after an English-listening placement. Answer pictures must differ from those shown.
- **Verify.** 5 no-English adults answer with audio muted and passage hidden; above ~45% means the item is a picture match.

### 5. §3.5 Stories tab
- **Wrong.** Word-by-word highlight in read-to-me trains following a voice: look-say with a karaoke bar. Tap-read says "sounds first, the word after an attempt" and "no picture until the page is read", but with no mic both are undefined; a "next" button satisfies them.
- **Teacher would.** Text hidden in L1-L2 read-to-me; sentence-level highlight only. Define "attempt" as a pick or tile step; the picture appears after a correct pick. Unlock a decodable only after that lesson's pick.
- **Verify.** DOM test: no word-level highlight class in L1-L2 Stories. Trace: whole-word audio never plays before at least one sound-by-sound event plus one pick.

### 6. §3.4 letter names at L1.13, and capitals
- **Wrong.** Names arrive ~36 adult sittings (~70 child) in. An adult needs "S" for a sign, name or plate in week one; a US child hears names everywhere and gets a contradicting app; the acrophonic cue (b d p t k) is discarded. Uppercase is never taught (the course mentions "capital" only for "I" and proper names), yet the Track B unlockables (sign, bus board, form) are capitals. Three minutes of print concepts will not carry a non-literate adult through left-to-right and letter/number/shape; Urdu-literate adults will track right to left.
- **Teacher would.** A name button on each Meet card from L1.02 (untested), capitals taught beside lowercase with the sound, unlockables only from taught shapes.
- **Verify.** Lint: every unlockable uses only taught shapes. Adult night one on video: does the learner sweep left to right unprompted?

## Held, no defect
The 2×2 grid fixes the hub leak. The repair never plays the target alone (the problem is what it plays, defect 3). One new sound per sitting is right; the binge is the problem.
