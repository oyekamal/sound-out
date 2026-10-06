# Critics round 4: teacher (structured literacy; 5-year-olds and Urdu/Arabic adult ESL beginners)

Read: plan-v4.md (all), DESIGN.md, the Teach Your Monster (TYM) listing, Common Sense review of TYM.

## Verdicts

1. **5-year-old, Urdu-first, mother reads no English, 10 min/day: B (TYM).** A as written puts mastery logic on a tap gate that can be passed without reading (defect 1) and an 8-minute sitting nobody has timed, while TYM already holds a child's attention.
2. **35-year-old adult non-reader alone: A (Sound Out).** TYM is a monster game for ages 3-6 with no adult track; A is the only one with a private adult path, Urdu instructions and "words to remember", provided night one is cut down (defect 6).

## Single biggest pedagogical gap

**Decoding is never observed; it is inferred from a recognition tap whose option structure is itself a cue.** The learner never produces a word from print in a way the app can check. E5 sound-by-sound and "I said it" are honour system, so the tap gate is the only evidence behind `checked`, unlocks and placement. Proxy validity (blind teacher) is tested only in week 10+, after everything rests on it.

## Defects

### 1. §3.3 E6d: the answer is the centre of the option set
- **Wrong.** Answer plus three one-position foils means the answer is the only option at edit distance 1 from all others; foils sit at distance 2 from each other (sat / pat, sit, sad). Options are spoken, so a learner who reads nothing can pick "the one like all the others". None of the §6.6 oracles covers this, and the 1.1% / 0.1% figures assume p=1/2 per item. Same for at / it, an, am and all made-up sets. Second leak: answers come from the lesson word list, foils are "not already in the word list" and are recorded weeks later (§4.1, §4.5), so familiarity and session timbre can mark the answer; Q1 loudness matching does not remove that.
- **Teacher would.** Vary set topology so the answer is sometimes a leaf (sat; sit, sip, pat), keep one-position coverage across the whole check rather than inside each item, and record answers and foils interleaved in the same sessions.
- **Verify.** Add a medoid oracle (minimum summed edit distance) and a take-fingerprint oracle (session id) to §6.6; both must be at chance (25% +/- 5) on the real L1.03-L1.13 and L3 JSON. Run 5 Urdu-only adults on option audio with the printed word hidden: chance.

### 2. §3.3 E5 and E6d repair
- **Wrong.** (a) The vowel repair plays the paired E22 pair ("sat/sit by ear"), which plays the target between the wrong answer and retry; this breaks rule 1 and the §2.3 audio-trace test. (b) L1-L2 successive blending plays "saaa" then re-asks the same reshuffled options; only sat and sad remain, so the retry is a 50% guess on one sound. (c) Replaying "the first sound and its letter" gives away the answer's first position.
- **Teacher would.** For a vowel miss play the mouth cue and a non-target contrast, never the target. Make the retry a different item built from the same sounds.
- **Verify.** Audio-trace: no clip of the target, or its partial plus final sound, between miss and retry. A partial-aware guesser must not clear retries above 50%.

### 3. §3.2 / §3.4 sitting model and village: credit without evidence
- **Wrong.** Sitting A has no judged step (spoken game, tap, trace, bubbles). "A piece appears only after its sound is learned" is undefined, so the sun rises for a random tapper. L1.02 runs seven sittings with no check until G. A no-helper child who ends `still_learning` is promoted with the sound unlearned and the next Read-it uses it, so guessing is invisible; the mother cannot judge "ask her these 3 sounds". Sitting B packs warm-up, hear, meet, 3 traces plus write, blend, spell, village, sticker, show-grown-up; tracing alone is 2+ minutes at age 5. The x1.5 multiplier is a guess; stopwatch is week 2-3.
- **Teacher would.** One judged mini item (three trials, onset contrast) before the village piece, and re-teach the same sound next sitting when missed. One trace plus one from memory on days 1-3.
- **Verify.** Random-tapper bot: village pieces after 5 sittings must be 0-1. Stopwatch 5 real 5-year-olds on A, B, C; p90 <= 8 min including celebrations.

### 4. §3.5 quick-start and placement (Hamza, 8)
- **Wrong.** 5 items at p=1/2 plus the defect-1 leak places a guesser; 5/5 feeds the Stage 3 ladder, the same leaky gate (14/16 = 87.5%). Landing at L2.03 skips the 24 L1 heart words, L2.01-02 tricky words, v/w, x/y/z/qu and b/d/p/q, and the plan never back-fills them. L2.03 texts then use "said, you, was, are" as taught. A child who knows letter names may answer sound items by name.
- **Teacher would.** Place one tier lower, back-fill every skipped heart word and GPC into review with E8 in the first sitting, and open with a v/w and b/d ear-and-eye item.
- **Verify.** Fixture: a child placed at L2.03 has all 24 L1 heart words in review within 2 sittings. Onset-blind and medoid learners are never placed above L1.06.

### 5. §3.4 Stories tab and §3.8 Listen & Talk
- **Wrong.** The Stories tab, where children will spend time, has no cueing rules. It never says whether a picture sits beside an unread word or whether text highlights while read (a memorised, highlighted story is look-say). §3.4 says a tapped word plays its sounds first; §4.4 says its own lexicon voice, and "water" has no taught sounds. The Urdu gloss comes first, "never contains the answer" by human review only, so the 80% English-question target may measure gloss inference.
- **Teacher would.** Decodable readers: no picture before the page is read, no highlighting. Read-to-me kept separate with text hidden in L1-L2. Non-decodable tapped words give whole-word audio with no credit. English passage first, gloss after.
- **Verify.** Run DOM and audio-trace tests on Stories. Gloss-leak test: 5 Urdu listeners get gloss + questions without the English audio; score at chance.

### 6. §3.5 adult night one in 15 minutes
- **Wrong.** The course gives about 35 tutor minutes to A-C (3 sounds, blend, spell, tricky words); the plan taps it into 15 with no print-concepts module (C1 is week 5). An Urdu-script reader may scan right to left ("tas" for "sat") and nothing checks direction. The first-word exit check is one tap among four with the defect-1 leak, so "read sat" can be a non-reading pass. /a/ has no Urdu counterpart, and three sounds in one sitting will not reach night two without retrieval.
- **Teacher would.** Keep the fast track only behind a >=90% mini check per sound, add a left-to-right finger slide card, and promise "tomorrow you will read it" if the checks miss. Day-2 warm-up retests all three sounds.
- **Verify.** Stopwatch 5 adults, including one who cannot read Urdu. Day-2 retention of s, a, t >= 80% first attempts. A reversed-reading oracle fails the gate.

## No defect found
- Level 5 as practice only is sound for v1; say on screen that an adult placed above L4 is in ungated practice.
