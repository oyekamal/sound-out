# Teacher voice audit: Sound Out vs a Duolingo ABC style guided teacher

Read-only audit, 2026-10-09. Scope: `app/src` (all screens, session.js, gate.js, onboarding.js, home.js, audio.js, level1.js, levels.js, placeholder.js), `content/` (audio_index.json, audio_plan.json, audio_needed.json, audio_needed_l5_7.json, ui_lines.json, levels/L2-4 ui, lessons), `plan/plan-v6.md`, `plan/decisions.tsv`. No decision is re-opened: voice = ElevenLabs River (SAz9YHcvj6GT2YYXdXww), eleven_v4, pre-rendered, one voice for everything (decisions 16, 18).

Goal of the coming build: a voice teacher guides every step, so a learner who cannot read never has to read an instruction. Bar: Duolingo ABC speaks on every screen, prompts before each task, praises or corrects after each answer, models before asking, re-prompts after silence.

**Headline.** Today the app speaks a prompt on most Level 1 screens and gives a one-word verdict ("Yes!", "Try again.") on pick screens, and that is nearly all. There is no idle re-prompt anywhere (only the 12 s tap-gate timer), Home is completely silent, every button is a text label, and Levels 2-7 narration is either a placeholder beep or absent.

Legend for the table below: **Y** yes, **P** partial, **N** no, **-** not applicable. "A" = Track A (child), "B" = Track B (grown-up). Screens are identical for both tracks unless the row says otherwise; both tracks hear the same clips (only `trickyIntroA/B` differ).

## 1. Screen and exercise audit

| Code | Screen / exercise | Track | Spoken now | Learner must read now | Prompt | Right/wrong feedback | Model before ask | Idle re-prompt |
|---|---|---|---|---|---|---|---|---|
| S01 | Onboarding: Who is reading? | A+B | `ui:who` on load; speaker icon replays | Title, card labels ("A child", "A grown-up"; icons help), "Or carry on:" + profile names | Y | N | - | N. `ui:child` / `ui:adult` clips exist but are never played |
| S02 | Onboarding: help in your language | A+B | `ui:helpLang` | Title, "Optional. You can learn with English only.", "Skip", "Language help packs are not in this prototype." (chips are native script) | Y | N | - | N. `ui:skip` exists, unused |
| S03 | Home (A: Pebble + village + path; B: lesson list) | A+B | Nothing. `home.js` has no `play` call | Everything: brand, day count, "Your sounds"/"Lessons", node labels (letters, "Words", "Read", "Listen", "Show what you know"), level cards ("Opens when you pass the Level 1 check."), badges | N | N | - | N |
| S04 | Sitting shell (header, progress, Next, Skip, close) | A+B | Only the header speaker, which replays the last `ctx.instruct` clip | "Next", "Skip", close ×; progress bar is silent | N | - | - | N. Next is enabled at once on Hear, so a learner can skip a prompt |
| S05 | Warm-up: what does it say? (A 3 letters, B 6) | A+B | `ui:warmIntro`, each option's sound, then `ui:good` / `ui:tryAgain` | "What does it say?", "This one" x3, the big letter | Y | P. Generic verdict; after a miss nothing models the right sound | N | N |
| S06 | Tap gate "read it, pick what it says" (used by warm-up words, blend, check, mastery) | A+B | `ui:gateRead`, 2 s silence, `ui:gatePick`, four option clips in turn, `ui:good`; first miss `ui:gateRepair` + sounds one by one; second miss `ui:gateReview`; 12 s timeout `ui:gateTimeout` | The printed word (the task), duplicate prompt text, "This one" x4, tag "alien word" (A) / "made-up word" (B) | Y | Y. The best-covered screen | N. No worked example before the first gate (plan 3.2 promised demos for "read it to yourself" and "made-up words") | P. 12 s timer then `gateTimeout`; no earlier nudge |
| S07 | Hear it (new sound) | A+B | `ui:hearIntro`, sound twice, `ui:hearExample`, example word | Heading, "Your mouth: <cue>" (never spoken), "a word that starts with it" | Y | - | Y (this screen is the model) | N |
| S08 | Meet it (letter card) | A+B | `ui:meetIntro`; tap plays the sound | Heading, "its name - when we read, we use its sound" | Y | P. Sound plays on tap, no praise | P. Says "tap it" but plays no sound first | N. Next stays disabled until a tap, with no nudge |
| S09 | Trace the letter (2 rounds) | A+B | `ui:traceIntro`; `ui:traceGood` after each round | Heading, "Trace 1 of 2", Skip | Y | P. Success only; a stroke under 70% gets silence | N. Faint guide only, no demo stroke | N |
| S10 | Blend it (tap tiles, say it, then gate) | A+B | First item of a new-sound sitting: `ui:blendModel` + sounds one by one. Every item: `ui:blendIntro`, tile tap plays its sound, `ui:blendSay` | Heading ("Blend it" / "A practice sound (not a word yet)"), hint text, "I said it", "self-report" note | Y | P. Correct tile sounds; out-of-order tile ignored silently; "I said it" gets no reply (the gate follows) | P. Model only on the first item of new-sound sittings | N |
| S11 | Spell a letter (hear sound, tap letter) | A+B | `ui:spellLetter` + sound; `ui:good`; miss `ui:tryAgain` + sound again | Heading, letter tiles (task content) | Y | Y (generic) | N | N |
| S12 | Spell a word (build from tiles) | A+B | `ui:spellIntro` + word; `ui:good`; miss `ui:tryAgain` + word again; second miss shows answer + `ui:gateReview` | Heading, tiles, boxes | Y | Y | P. Hears the word; no demo of tile building | N |
| S13 | Tricky word / word to remember | A: `trickyIntroA`; B: `trickyIntroB` | Intro, the word, `ui:trickyTap`; `ui:good` when all heart parts found; a wrong tap plays that letter's sound | Heading, and the message for words with no heart part ("Good news: this one sounds out. No tricky part.") is text only | Y | P. No spoken "not that part" | P | N |
| S14 | Read it (decodable text) | A+B | `ui:readIntro`; tap word = sounds then whole word; "I read it" then `ui:readHear` + passage read aloud | The passage (that is the task), title (not voiced), "I read it", "Hear it read" | Y | N. Self-report; nothing is said back | P. Model plays after the attempt (by design) | N |
| S15 | Listen and talk (story, new word, 2 questions) | A+B | `ui:listenIntro`, title, story chunks (picture after each), `ui:listenWord` + t2 clip, `ui:listenQ` + question clip | Heading, "You don't need to read this", printed question text (also voiced), "Question 1", placeholder note | Y | N. Any picture is accepted, no praise, no correction | Y (story read to learner) | N |
| S16 | "Show what you know" shell (L1.02-12, L2-4) | A+B | `ui:checkIntro`; items run through S06/S12; `ui:checkPass` / `ui:checkMiss` / `ui:finishTomorrow` | Heading, prompt, "N of M on the first try - bar x/y", score dots | Y | P. Verdict at the end only | N | N |
| S17 | End of sitting | A: Pebble cheer + sticker + village; B: plain | `ui:miniPass` / `ui:miniMiss`, then `ui:village` or `ui:sticker`, then `ui:keepGoing` | "Well done!", "Mini check: 3 of 5 on the first try", "You earned a sticker!", buttons "Keep going?" and "Home" | Y | Y (one verdict) | - | N |
| S18 | L1.01 oral: first sound | A+B | `ui:l1OralFirst`, the word, option sounds; `ui:good` / `ui:tryAgain` | Heading, "This one" x3, picture placeholder | Y | Y (generic) | N. No worked example | N |
| S19 | L1.01 oral: blend the sounds | A+B | `ui:l1OralBlend`, the sounds, 3 word options with pictures; verdict | Heading, "This one" x3 | Y | Y | N | N |
| S20 | L1.01 oral: how many sounds | A+B | `ui:l1OralCount`, the word; options are dot counts with no voice; after the pick the dots light with each sound | Heading, "This many" x3 | Y | Y | P (after the answer) | N |
| S21 | L1.01 preview of s and a | A+B | `ui:l1OralPreview`, s, a | Heading, "Tap a letter to hear its sound. You will learn them properly in the next lesson." | Y | P | Y | N |
| S22 | L1.01 oral check (test mode) | A+B | `ui:l1OralCheck`; items silent (no feedback by design); `ui:checkPass/Miss` | Heading, prompt, score | Y | N between items; verdict at end | N | N |
| S23 | L1.13 names vs sounds | A+B | `ui:l1Names`, then name and sound | Heading, "its name" / "its sound", notes such as "q is called "cue". With its u it says /kw/." (text only) | Y | - | Y | N |
| S24 | L1.13 name-or-sound quiz | A+B | `ui:l1NameOrSound` + the clip; verdict | "Name or sound?", buttons "Its name" / "Its sound" (no voice) | Y | Y | N | N |
| S25 | L1.13 b d p q intro | A+B | `ui:l1Bdpq` only | The bed trick paragraph and four tips, about 370 characters, all text only | P | - | N. The trick is shown as text | N |
| S26 | L1.13 b d p q pick | A+B | The sound, no prompt; verdict; after a miss the tip appears as text for 1.2 s | Heading, four letter options (no voice), tip text | N | P | N | N |
| S27 | L1.14 Level 1 check (7 parts, test mode) | A+B | `ui:l1MasteryIntro`; letters reuse `warmIntro`; words/hearts/context reuse `gateRead`; verdict `ui:l1MasteryPass/Miss` ("Level 2 is coming soon" is now stale) | Part list, per-part score table, "Read the dark word", the sentence | P. One line serves four different tasks | N between items | N | N |
| S28 | L2-4 teach: new spelling / ending | A+B | `teachIntro` / `teachSuffix`, sound, `teachExample`, word. UI lines are placeholders: a silent beep and an "audio coming" toast | Heading, grapheme card, label ("one sound") | P (placeholder) | P | Y (sound) | N |
| S29 | L2-4 teach grid (blends, endings) | A+B | `ui:teachBlend` (placeholder) | Heading, prompt text | P (placeholder) | P | N | N |
| S30 | L2-4 rule card | A+B | `ui:ruleIntro` + `rule:<lesson>` (both placeholders) | Rule title and 2-3 sentences of rule text, example words | P (placeholder) | - | Y | N |
| S31 | L2-4 word attack (5 steps: vowels, peel, chunk, blend, flex) | A+B | `attackVowels`, `attackPeel`, `attackChunk` then `attackBlend` back to back, `attackFlex` (all placeholders); vowel taps play the sound; chunk taps play `syl:` clips (placeholders) | Step bar labels, headings, "N vowel sounds: N chunks.", "No start or ending to peel off here.", the long flex prompt | P (placeholder) | N. Wrong tap only shakes the tile | N | N |
| S32 | L2-4 self-checked word (no tap-gate options) | A+B | `ui:gateRead`; "I said it. Let me hear it" plays the word | Prompt text, three buttons ("I said it. Let me hear it", "I read it right", "Not quite"), self-check note | Y | N (self-judged) | N | N |
| S33 | L2-4 level mastery | A+B | `masteryIntro`, `masteryPass/Miss` (placeholders); per-part title screens silent; items via S06/S32 | Component list ("N items - pass M"), results table, "Practise the parts that were hard..." | P | N between items | N | N |
| S34 | L4.15 attack check | A+B | `attackCheckIntro` (placeholder), then S31 + S32 | Heading, prompt, bar | P (placeholder) | N | N | N |
| S35 | L5-7 practice (warm, word, fluency, prime, text, discuss, write, check) | A+B (one text set at L6-7; L5 has A and B texts) | No spoken instruction at all. Content `voice()` buttons all read "audio coming" | All instructions ("Read each word aloud, cold, no help. Then tap it.", "Think, then tap to see a good answer.", "Check yourself", ...), passages, answers, self-marks ("I had it", "Nearly", "Not yet") | N | N (self-marking) | N | N |

Cross-cutting facts behind the table:

- Whole spoken verdict vocabulary today: `good` ("Yes!"), `tryAgain` ("Try again."), `traceGood`, `miniPass`, `checkPass/Miss`. Three short lines carry every right and wrong answer.
- Idle behaviour: none. `gate.js` waits 12 s then says `gateTimeout`; every other screen waits forever in silence.
- Unused rendered clips: `ui:child`, `ui:adult`, `ui:skip`, `ui:saidIt`, `ui:soundTap`, `ui:pickNext`, `ui:selfReport`, `ui:daysPractised`, `ui:wordsToRemember`, `ui:trickyWords`, `ui:next`. They show the intent to voice buttons, but nothing plays them.
- Autoplay-blocked path: `audio.js` swallows the rejection and carries on silently, so on a web first load the "Who is reading?" prompt can be skipped without the learner knowing.
- Test mode (`choose(... test:true)`, L1.01 check, L1.14 check) is silent between items by design. A narrator can still say "Next one." without giving feedback.

## 2. Audio coverage per level

Source: `content/audio_index.json` (rendered), `content/audio_needed.json` (L2-L4), `content/audio_needed_l5_7.json` (L5-L7). "Placeholder" = the app plays a short silent file and shows an "audio coming" toast (`placeholder.js`) for L2-L4, and a visible "audio coming" button for L5-L7 (`kit.js`).

| Level | Real River clips today | Placeholders (clips still needed) | Characters still needed | What a learner hears today |
|---|---|---|---|---|
| L1 (14 lessons) | 1,212 clips, `missing: []`: ipa 564, w 279, read 134, ui 59, lt 53, q 28, name 26, ph 25, ex 24, t2 14, exw 6 | 0 | 0 | Full narration of prompts and content. The gaps are structural (silence on Home, text-only controls, no idle, thin feedback), not missing files |
| L2 (14 lessons) | Reuses L1 clips: letter sounds, `gateRead/gatePick/...`, `checkPass/Miss`, `good/tryAgain` | 1,285 keys + 23 isolated sounds. By kind: ipa 636, w 375, read 73, syl 139, lt 40, rule 7, ui 15 | 26,279 (950 requests). By kind: ipa 6,892, lt 8,113, read 7,638, rule 997, syl 1,074, ui 666, w 3,861 | Gate and check prompts are real; every teach, rule and attack line, every new word and chunk is a beep plus a toast |
| L3 (18 lessons) | Same reuse | 1,869 keys + 24 isolated sounds. ipa 969, w 630, syl 143, q 34, read 34, lt 18, t2 17, rule 9, ui 15 | 32,198 (1,392 requests). ipa 10,251, read 10,578, w 6,335, lt 3,632, q 1,691, t2 1,291, syl 1,041, rule 936, ui 666 | Same pattern |
| L4 (16 lessons) | Same reuse | 3,176 keys + 43 isolated sounds. w 1,199, ipa 1,092, syl 575, read 235, q 21, lt 15, t2 15, rule 9, ui 15 | 47,684 (2,489 requests). w 13,340, ipa 12,127, read 16,030, syl 4,511, lt 2,727, t2 1,549, q 1,330, rule 1,176, ui 666 | Same pattern |
| L2-L4 total | | 6,330 keys (5,487 unique across the three levels: L3 repeats 164 L2 keys, L4 repeats 679) + 43 unique isolated sounds | 106,161 as written in the files. Re-counted de-duplicated across levels: about 98,900 before cached renders, so expect roughly 97,000 to 99,000 | |
| L5 (16 lessons) | 0 | 1,339 clips | 78,698 | No spoken instructions; all content `voice()` buttons say "audio coming" |
| L6 (16 lessons) | 0 | 449 clips | 96,835 | Same |
| L7 (14 lessons) | 0 | 349 clips | 81,874 | Same |
| L5-L7 total | | 2,137 clips | 257,407 | |

Notes:

- The 43 isolated sounds (ph:) are not charged per character the same way: `tools/iso_sounds.py` renders three prompt forms each and picks one; decision 19 kept the L1 spend at 2,343 characters for 206 renders, so plan about 1,500 to 3,000 for 43 more.
- The 15 `ui:` lines in each of L2-L4 are the same 15 lines repeated (666 characters each, counted three times in the 106,161 total). Rendered once they cost 666.
- `ui:attackIntro` is in the placeholder list but no screen plays it. `ui:l1MasteryIntro/Pass/Miss` should be retired in favour of `masteryIntro/Pass/Miss`, because `l1MasteryPass` says "Level 2 is coming soon" while L2 is now on the path.
- L1 content narration that is still text only (not in `missing`, because no screen asks for it): 21 mouth cues (1,884 characters) in `lessons/L1.02-L1.11`, the b/d/p/q trick and tips, the name-versus-sound notes. See script group 8.

## 3. The teacher script

Design rules (all lines: short, warm, plain global English, no idioms, no jokes, no names):

1. **One voice, River, speed 0.9**, same settings as the shipped clips, so new lines splice in without a seam (decision 16).
2. **Shared by default, track-specific only where tone differs.** A-only lines: `homeGoA`, `alienWord`, `wow`, `sticker`, `village`, `trickyIntroA`. B-only: `homeGoB`, `madeUpWord`, `goodWork`, `trickyIntroB`. Everything else is neutral enough for a nine-year-old and for a shopkeeper (no "superstar", no baby talk, no exclamation marks except the three already shipped).
3. **Praise is a pool, not one line.** Draw from the pool per screen family (the "pool:" screens in group 4), never the same line twice in a row. `good` stays the default. `youGotIt` after a second-try success, `firstTry` after a miss streak, `threeInRow` at a streak of 3. Test mode (check, mastery): no praise, only `nextOne`, by design.
4. **Correction is a fixed three-step chain, never a bare "Try again."**: `notQuite` then the model (a templated carrier plus an existing clip) then `yourTurn`. Tap-gate repair stays as it is (`gateRepair` plus sounds one by one, never the whole target word inside a repair, decision 11).
5. **Model before ask**: `watchMe` plus a demonstration on the first item of each exercise type, `letsDoOne` plus one worked item before the six unmimeable instructions in plan-v6 3.2 (read to yourself, made-up words, first sound, finish tomorrow, tricky words), then `yourTurn`.
6. **Idle ladder** (timer resets on any tap, runs only while no clip is playing): tier 1 at 7 s replays the current prompt clip (zero new characters); tier 2 at 15 s plays the type-specific nudge and pulses the target; tier 3 at 25 s plays `idleHelp`; tier 4 at 40 s on pick items plays `gateTimeout` and moves on exactly as the tap gate does today; tier 5 at 70 s plays `idleWait` and pauses (no scoring, no timers).
7. **Every button gets a voice-on-tap or an icon.** Next becomes an arrow icon (`tapArrow` explains it once per sitting), "This one" becomes a tick icon, Skip and Home become icons with `ui:skip` and a spoken label.

**Templated lines** (composed from separate renders; they sound natural because the carrier is short and the join uses the existing 250 ms gap from `audio.seq`; check the three that join an isolated sound by ear, since stops like /b/ are only about 60 ms): `thisLetterIs` + `name:{letter}`, `andSays` + `ph:{sound}`, `thisLetterSays` + `ph:{sound}`, `thisWordSays` + `w:{word}`, `qNote` + `ph:kw`, `mouthLead` + `mouth:{lesson}:{sitting}`. Every other line is a standalone clip.

Status: **E** = already rendered in River (0 new characters), **P** = placeholder wording already written and already counted in the L2-L4 total, **N** = new render.


**1. Entry, navigation, session arc**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:who | E | Who is reading? | A+B | S01 | - | 15 |
| ui:child | E | A child | A+B | S01 (voice on tap) | - | 7 |
| ui:adult | E | A grown-up | A+B | S01 (voice on tap) | - | 10 |
| ui:helpLang | E | Do you want help in your own language? You can skip this. | A+B | S02 | - | 57 |
| ui:skip | E | Skip | A+B | S02, S04 (voice on tap) | - | 4 |
| ui:homeGoA | N | Tap the shining sound to go on. | A | S03 | - | 31 |
| ui:homeGoB | N | Tap the next lesson to go on. | B | S03 | - | 29 |
| ui:welcomeBack | N | Welcome back. Let's keep going. | A+B | S03 (return visit) | - | 31 |
| ui:begin | N | Let's begin. | A+B | S04 (start of every sitting) | - | 12 |
| ui:halfway | N | You are halfway through. | A+B | S04 (progress 50%) | - | 24 |
| ui:lastOne | N | Last one. | A+B | S04 (final item) | - | 9 |
| ui:nextOne | N | Next one. | A+B | S10, S16, S22, S27, S33 | - | 9 |
| ui:nextPart | N | Here is the next part. | A+B | S27, S33, step changes in S04 | - | 22 |
| ui:tapArrow | N | Tap the arrow to go on. | A+B | S04 (every Next button; needs an arrow icon) | - | 23 |
| ui:seeYou | N | See you next time. | A+B | S17 (Home tapped or day cap reached) | - | 18 |
| ui:practisedToday | N | You practised today. Well done. | A+B | S17 (first sitting of the day) | - | 31 |

**2. Task prompts (what to do)**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:hearIntro | E | Listen to this sound. | A+B | S07 | - | 21 |
| ui:hearExample | E | You can hear it at the start of this word. | A+B | S07 | - | 42 |
| ui:meetIntro | E | This letter makes that sound. Tap it to hear it. | A+B | S08 | - | 48 |
| ui:traceIntro | E | Trace the letter with your finger. | A+B | S09 | - | 34 |
| ui:traceAgain | N | Once more. Trace it again. | A+B | S09 (round 2) | - | 26 |
| ui:traceHelp | N | Follow the faint letter. Go slowly. | A+B | S09 (stroke under 70%) | - | 35 |
| ui:blendModel | E | Watch and listen. Sound by sound, then slide them together. | A+B | S10 | - | 59 |
| ui:blendIntro | E | Say each sound, then tap its letter. Left to right. | A+B | S10 | - | 51 |
| ui:blendSay | E | Now slide the sounds together and say it out loud. | A+B | S10 | - | 50 |
| ui:wrongTile | N | Start at the first letter. | A+B | S10 (tile tapped out of order) | - | 26 |
| ui:gateRead | E | Read it to yourself. Say it. | A+B | S06, S27, S32 | - | 28 |
| ui:gatePick | E | Tap the one that matches the word. | A+B | S06 | - | 34 |
| ui:alienWord | N | This is an alien word. Sound it out. | A | S06, S32 (pseudo items) | - | 36 |
| ui:madeUpWord | N | This is a made-up word. Sound it out. | B | S06, S32 (pseudo items) | - | 37 |
| ui:warmIntro | E | Warm up. What does it say? | A+B | S05, S27 (letters) | - | 26 |
| ui:spellLetter | E | Listen. Tap the letter that makes this sound. | A+B | S11, S26 | - | 45 |
| ui:spellIntro | E | Listen. Then build it with the letters. | A+B | S12 | - | 39 |
| ui:trickyIntroA | E | This is a tricky word. The heart part does not sound the way you expect. | A | S13 | - | 72 |
| ui:trickyIntroB | E | This is a word to remember. The marked part does not sound the way you expect. | B | S13 | - | 78 |
| ui:trickyTap | E | Tap the part that is different. | A+B | S13 | - | 31 |
| ui:trickyRegular | N | This word is not tricky. Sound it out. | A+B | S13 (no heart part) | - | 38 |
| ui:readIntro | E | Read it. Tap any word for its sounds. | A+B | S14 | - | 37 |
| ui:readHear | E | Now listen to it read aloud. | A+B | S14 | - | 28 |
| ui:listenIntro | E | Listen to a story. You don't need to read it. | A+B | S15 | - | 45 |
| ui:listenWord | E | Here is a new word. | A+B | S15 | - | 19 |
| ui:listenQ | E | Listen to the question. Tap your answer. | A+B | S15 | - | 40 |
| ui:checkIntro | E | Show what you know. Some are made-up words. Just sound them out. | A+B | S16 | - | 64 |
| ui:l1OralFirst | E | Listen. What sound does it start with? | A+B | S18 | - | 38 |
| ui:l1OralBlend | E | Listen to the sounds. Which word do they make? | A+B | S19, S22 | - | 46 |
| ui:l1OralCount | E | Listen to the word. How many sounds? | A+B | S20 | - | 36 |
| ui:l1OralPreview | E | Here are two letters for next time. | A+B | S21 | - | 35 |
| ui:l1OralCheck | E | Listen to the sounds, and pick the word. | A+B | S22 | - | 40 |
| ui:l1Names | E | Every letter has a name and a sound. | A+B | S23 | - | 36 |
| ui:l1NameOrSound | E | Was that its name, or its sound? | A+B | S24 | - | 32 |
| ui:itsName | N | Its name. | A+B | S24 (voice on button tap) | - | 9 |
| ui:itsSound | N | Its sound. | A+B | S24 (voice on button tap) | - | 10 |
| ui:l1Bdpq | E | These letters look alike. Look closely. | A+B | S25 | - | 39 |
| ui:selfRead | N | Read it out loud. Then tap to hear it. | A+B | S32 | - | 38 |
| ui:selfJudge | N | Did you read it right? | A+B | S32 (after the word plays) | - | 22 |
| ui:masteryIntro | P | This is the check for the whole level. Do your best. | A+B | S27 (replaces l1MasteryIntro), S33 | - | 52 |
| ui:teachIntro | P | Here is a new spelling for a sound. Tap it to hear it. | A+B | S28 | - | 54 |
| ui:teachSuffix | P | This is an ending. Read the base word, then add the ending. | A+B | S28 | - | 59 |
| ui:teachExample | P | Here it is in a word. | A+B | S28 | - | 21 |
| ui:teachBlend | P | These letters keep both sounds. Say them quickly together. | A+B | S29 | - | 58 |
| ui:ruleIntro | P | Here is a rule that helps you read. | A+B | S30 | - | 35 |
| ui:attackIntro | P | A long word. Let's break it apart, step by step. | A+B | S31 (never called today; wire it) | - | 48 |
| ui:attackVowels | P | Tap every vowel sound. | A+B | S31 | - | 22 |
| ui:attackCount | N | Each vowel sound makes one chunk. | A+B | S31 | - | 33 |
| ui:attackPeel | P | Tap the parts at the start or end that you know. | A+B | S31 | - | 48 |
| ui:attackNoPeel | N | Nothing to take off here. Go on. | A+B | S31 | - | 32 |
| ui:attackChunk | P | Here are the chunks. | A+B | S31 | - | 20 |
| ui:attackBlend | P | Tap each chunk to say it, then put them together. | A+B | S31 | - | 49 |
| ui:attackFlex | P | Is it a real word? If not, try the vowel the other way. | A+B | S31 | - | 55 |
| ui:attackCheckIntro | P | Show how you read a word you have never seen. | A+B | S34 | - | 45 |
| ui:ssPrime | N | Before you read, think about this. | A+B | S35 | - | 34 |
| ui:ssWarm | N | Read each word out loud. Then tap it. | A+B | S35 | - | 37 |
| ui:ssFind | N | Tap the word you hear. | A+B | S35 | - | 22 |
| ui:ssBuild | N | Build the word. Tap the parts in order. | A+B | S35 | - | 39 |
| ui:ssRead | N | Read one part at a time. Tap a sentence to hear it. | A+B | S35 | - | 51 |
| ui:ssFlu | N | Read it out loud. Tap start when you are ready. | A+B | S35 | - | 47 |
| ui:ssThink | N | Think first. Then tap to see a good answer. | A+B | S35 | - | 43 |
| ui:ssMark | N | How did you do? Tap one. | A+B | S35 | - | 24 |
| ui:ssWrite | N | Write your answer. Then compare it. | A+B | S35 | - | 35 |
| ui:ssTalk | N | Take each role. Say your answer out loud. | A+B | S35 | - | 41 |

**3. Model before ask**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:watchMe | N | Watch me first. | A+B | S06, S09, S10, S11, S12 (first item of each type) | - | 15 |
| ui:letsDoOne | N | Let's do one together. | A+B | S06, S18-S20, S32 (worked item) | - | 22 |
| ui:yourTurn | N | Now you try. | A+B | after any model, all task screens | - | 12 |
| ui:thisLetterIs | N | This letter is | A+B | S08 (+ name:{l}) | templated | 14 |
| ui:andSays | N | and it says | A+B | S08 (+ ph:{p}) | templated | 11 |
| ui:thisLetterSays | N | This letter says | A+B | S05, S11, S26 repair (+ ph:{p}) | templated | 16 |
| ui:thisWordSays | N | This word says | A+B | S12, S13 repair (+ w:{word}) | templated | 14 |
| ui:nameSoundNote | N | When we read, we use the sound, not the name. | A+B | S08, S23 | - | 45 |
| ui:qNote | N | The letter q is called cue. With u, it says | A+B | S23 (+ ph:kw) | templated | 43 |
| ui:mouthLead | N | Here is how your mouth moves. | A+B | S07 (+ mouth:{lesson}:{sitting}) | templated | 29 |

**4. Praise after a right answer**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:good | E | Yes! | A+B | S05, S06, S11, S12, S13, S18-S20, S24, S26 | - | 4 |
| ui:traceGood | E | Good tracing! | A+B | S09 | - | 13 |
| ui:right | N | That's right. | A+B | pool: S05, S11, S12, S24, S26 | - | 13 |
| ui:goodListening | N | Good listening. | A+B | pool: S15, S18, S19, S20 | - | 15 |
| ui:goodReading | N | Good reading. | A+B | pool: S06, S16, S27 | - | 13 |
| ui:goodSounding | N | Good sounding out. | A+B | pool: S10, S31 | - | 18 |
| ui:niceSpelling | N | Nice spelling. | A+B | pool: S11, S12 | - | 14 |
| ui:youGotIt | N | You got it. | A+B | second-try correct, all pick screens | - | 11 |
| ui:firstTry | N | First try! Well done. | A+B | first-try correct after a miss streak | - | 21 |
| ui:threeInRow | N | Three right in a row. | A+B | streak of 3, all pick screens | - | 21 |
| ui:wow | N | Wow! That was great. | A | pool: S06, S10, S18-S20 | - | 20 |
| ui:goodWork | N | Good work. | B | pool: S06, S10, S12, S16 | - | 10 |

**5. Correction, gentle**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:tryAgain | E | Try again. | A+B | S05, S11, S12, S18-S20, S24, S26 | - | 10 |
| ui:notQuite | N | Not quite. Listen again. | A+B | S05, S11, S12, S18-S20, S24, S26 | - | 24 |
| ui:lookCloser | N | Look closely. | A+B | S25, S26 | - | 13 |
| ui:notThatPart | N | That part sounds normal. Find the different part. | A+B | S13 | - | 49 |
| ui:notVowel | N | Not a vowel sound. Try another. | A+B | S31 | - | 31 |
| ui:gateRepair | E | Let's look again, sound by sound. | A+B | S06 | - | 33 |
| ui:gateReview | E | We will practise this one again later. | A+B | S06, S12 | - | 38 |
| ui:gateTimeout | E | That's okay. Let's try another one. | A+B | S06 (idle tier 4) | - | 35 |

**6. Idle re-prompts (tier 1 replays the current prompt clip: 0 new characters)**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:idleTap | N | Tap the letter. I will wait. | A+B | tier 2: S07, S08, S13, S23, S28-S31 | - | 28 |
| ui:idlePick | N | Take your time. Tap the one you think. | A+B | tier 2: S05, S06, S11, S15, S18-S20, S24, S26 | - | 38 |
| ui:idleSay | N | Say it out loud. Then tap the button. | A+B | tier 2: S10, S14, S31, S32 | - | 37 |
| ui:idleTrace | N | Put your finger on the letter. Trace it. | A+B | tier 2: S09 | - | 40 |
| ui:idleArrow | N | Tap the arrow when you are ready. | A+B | tier 2: S04 (any Next screen) | - | 33 |
| ui:idleHelp | N | Need help? Tap the speaker to hear me again. | A+B | tier 3: every screen | - | 44 |
| ui:idleWait | N | I will wait here. Tap when you are ready. | A+B | tier 5: every screen, then pause | - | 41 |

**7. Checks, results, session end**

| id | status | line | track | screens | templated | chars |
|---|---|---|---|---|---|---|
| ui:checkPass | E | You did it! The next part is open. | A+B | S16, S22 | - | 34 |
| ui:checkMiss | E | We'll practise these again. The next part is still open. | A+B | S16, S22 | - | 56 |
| ui:masteryPass | P | You passed! The next level is open. | A+B | S27 (replaces l1MasteryPass, which says Level 2 is coming soon), S33 | - | 35 |
| ui:masteryMiss | P | Not yet. Let's practise the parts that were hard, then try again. | A+B | S27 (replaces l1MasteryMiss), S33 | - | 65 |
| ui:miniPass | E | Well done! | A+B | S17 | - | 10 |
| ui:miniMiss | E | Let's practise this sitting again next time. | A+B | S17 | - | 44 |
| ui:keepGoing | E | Keep going? | A+B | S17 | - | 11 |
| ui:finishTomorrow | E | Let's finish this tomorrow. | A+B | S16, S17 | - | 27 |
| ui:sticker | E | You earned a sticker! | A | S17 | - | 21 |
| ui:village | E | A new piece for your village! | A | S17 | - | 29 |

**8. Lesson content that is text-only today (needs its own narration)**

| id | line | screens | chars |
|---|---|---|---|
| mouth:{lesson}:{sitting} (21 clips) | one render per mouth cue, e.g. "teeth close together, air hisses out." | S07 | 1884 |
| tipBedTrick | Make two fists with your thumbs up. Hold them side by side. The left fist is b. The right fist is d. Together they make bed. | S25 | 124 |
| tipB | b: the bat comes first, then the ball. The belly of b points right. | S25, S26 | 67 |
| tipD | d: the drum comes first, then the stick. The belly of d points left. | S25, S26 | 68 |
| tipP | p hangs down. Its loop is at the top, on the right. | S25, S26 | 51 |
| tipQ | q hangs down too. It always needs its u. | S25, S26 | 40 |

Counts: 48 E lines (1651 chars), 15 P lines (666 chars), 64 N lines (1709 chars), group 8 content (2234 chars). 

## 4. Total ElevenLabs characters

| Bucket | Lines or clips | Characters |
|---|---|---|
| Script lines already rendered (E) | 48 | 1,651 (no new cost) |
| Script lines already written as L2-L4 placeholders (P) | 15 | 666 (inside the L2-L4 figure below, not added again) |
| **Script, new renders (N), incl. L5-L7 instruction lines and the six templated carriers** | 64 | **1,709** |
| **Lesson content narration, new (group 8: 21 mouth cues + bed trick + 4 tips)** | 26 | **2,234** |
| L2-L4 placeholders, as written in `audio_needed.json` | 6,330 keys | 106,161 (about 97,000 to 99,000 once de-duplicated across levels and cached renders are excluded) |
| L5-L7 placeholders, `audio_needed_l5_7.json` | 2,137 clips | 257,407 |
| **Grand total, sum of the files** | | **367,511** (3,943 new teacher and narration + 106,161 + 257,407) |
| **Grand total, de-duplicated estimate** | | **about 359,000** |
| Plus isolated sounds for L2-L4 (43 unique, separate render path) | 43 | about 1,500 to 3,000 |
| Plus retries and rejected takes (assumed 10 to 15% headroom; the L1 overrun was not measured) | | about 36,000 to 54,000 |

Practical reading: the teacher script itself is tiny, **3,943 characters** (script 1,709 plus content narration 2,234, 90 clips), and covers every Level 1 screen. At the unverified $0.10 to $0.30 per 1,000 characters logged in decisions.tsv (the real PAYG rate for eleven_v4 was never checked) that is about $0.40 to $1.20. The big numbers are lesson content for L2-L7 (99% of the total), not teacher lines. If the build needs only the guided teacher first, render the 3,943 characters now, keep L2-L7 content as placeholders, and the first-session experience is complete. The ElevenLabs account quota was reported exhausted on 2026-10-08, so confirm the dashboard before a render pass; also verify the commercial-use licence for shipped clips (still open in decisions.tsv).

## 5. Top 10 gaps against a Duolingo ABC style guided teacher, ranked

Ranked by how soon a learner who cannot read gets stuck.

1. **Navigation and controls are silent and text-only.** Home speaks nothing; Next, Skip, "This one" (x3 or x4 on every pick screen), "I said it", "Keep going?", "Home", level cards and node labels are all words. After the auto-started first sitting a non-reader cannot tell what to tap. Fix: `homeGoA/B`, `tapArrow`, `welcomeBack`, icons instead of words, voice-on-tap for `ui:skip`, `ui:child`, `ui:adult` (clips already exist). Cost: 114 characters for the four new lines.
2. **No idle detection or re-prompt.** The only silence handling is the tap gate's 12 s timer. Duolingo ABC re-prompts after silence on every task. Fix: the five-tier ladder in section 3; tier 1 reuses the current prompt clip, so it is free. Cost: 7 lines, 261 characters.
3. **Levels 2-7 have no real teacher narration.** Every teach, rule and attack instruction in L2-L4 is a beep plus an "audio coming" toast (15 lines, 666 characters, never rendered); L5-L7 speak no instruction at all. The learner who passes L1 loses the voice. Fix: render the 15 `P` lines and the 10 `ss*` lines now (1,039 characters together); content clips follow later.
4. **Feedback is three words.** `good`, `tryAgain` and the verdict lines carry every answer. Misses in warm-up and the L1 choose screens model nothing, a failed trace and an out-of-order tile get silence, test mode is silent between items, and Listen answers are accepted without praise or correction. Fix: praise pool, the notQuite then model then yourTurn chain, `traceHelp`, `wrongTile`, `nextOne`, and a spoken verdict on Listen answers once real pictures land.
5. **Little modelling before asking.** Only the first blend item of a new-sound sitting is modelled. No worked example before the first tap gate or the first made-up word (plan-v6 3.2 promised demos for six instructions and none is built), Meet asks "tap it" without first playing the sound, and Trace shows only a faint guide with no demonstrated stroke. Fix: `watchMe`, `letsDoOne`, `yourTurn`, `thisLetterIs/andSays`, `alienWord/madeUpWord`, plus Pebble or a hand animation for the demo.
6. **Explanations exist only as text.** 21 mouth cues (1,884 characters), the b/d/p/q bed trick and four tips (about 370 characters, the only teaching on S25), the name-versus-sound notes, the tricky-word "no heart part" message, the attack-step messages, the mastery tables and score lines. A non-reader gets none of it. Fix: script group 8 and the N lines in groups 2 and 3.
7. **No central teacher controller.** Each screen calls `ctx.instruct` or `play` by hand. The header speaker replays only the last `instruct`, not the current prompt; nothing queues, interrupts or ducks when the learner taps mid-clip; `audio.js` carries on silently when autoplay is blocked; prompts and option playback ignore taps for several seconds. Fix: one `teacher.say(id, {track, interruptible})` layer that owns the queue, replay, idle ladder and the A/B line choice.
8. **No session arc.** The app never says hello, "let's begin", "halfway", "last one", "you practised today" or "see you next time", and the progress bar and day counter are mute. Duolingo ABC's narrator frames every lesson. Fix: `begin`, `halfway`, `lastOne`, `practisedToday`, `seeYou`.
9. **Self-report steps get no reply.** "I said it", "I read it" and "I read it right / Not quite" are taps the app cannot check, and the teacher says nothing back, so the learner gets neither confirmation nor guidance. Fix: `selfRead`, `selfJudge`, and a spoken acknowledgement from the praise pool or `gateReview`; the Whistle spike in decisions.tsv (2026-10-06) is the route to real checking later.
10. **One register for both tracks, with no teacher persona.** Both tracks hear identical lines, the child track has no playful voice moments (Pebble animates but never speaks) and the adult track meets a few child-flavoured words ("alien word", "heart part", "You earned a sticker!" is already A only). Fix: the track-specific lines in section 3 (`wow`, `goodWork`, `alienWord`/`madeUpWord`, `homeGoA/B`) and a decision on whether Pebble is the voice's character on Track A.
