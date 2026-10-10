# Critic: Tilo in app, round 1

Blind visual review of `store/android-test/tilo-in-app/` against the source art in `app/public/img/tilo/` and the Duolingo ABC bar in `design/character/bar/`. Only defects are listed.

## Per-screen verdict (child track, Track A)

| Screen | Mouth placement | Cuteness | Clarity (360x640) | Pose reads | Result |
|---|---|---|---|---|---|
| A_celebrating | n/a (closed smile) | PASS | PASS, no button overlap | PASS, arms up plus sparkles read at a glance | PASS |
| A_encouraging | PASS (smile) | PASS | PASS | FAIL: one raised hand, same silhouette as speaking, reads as a wave or hello | FAIL |
| A_idle | n/a | PASS | FAIL: yellow focus ring on Check 1 and on the ear button | PASS | FAIL (ring) |
| A_listening | n/a | PASS | PASS, hand sits over the teal bead but no button hit | PASS (hand at head) | PASS |
| A_speaking_1_mid | FAIL: mouth is a small dot inside the snout, not under the nose | PASS | FAIL: answer cards are gone and the picture card is shrunk to about 253px wide | FAIL: reads as a wave, not talking | FAIL |
| A_speaking_2_aaa | FAIL: aaa looks the same as mid at 4x; no visible open-jaw change | PASS | FAIL: picture card jumps to about 414px wide, so the layout reflows between frames | FAIL: same as mid | FAIL |
| emulator_lesson_tilo (speaking, 1080x2400 device) | FAIL: open "o" in the snout reads as shock, not speech | PASS | PASS | FAIL: alarmed, not talking | FAIL |

## Per-screen verdict (grown-up track, Track B)

| Screen | Mascot absent? | Clarity | Result |
|---|---|---|---|
| B_home_no_mascot | PASS, no Tilo | FAIL: the 84px ear button covers the "Who... reading" profile pill; the label is cut off | FAIL (clarity only) |
| B_no_mascot | PASS, no Tilo | PASS for overlap; the bottom 40% of the screen is empty | PASS (layout note below) |

## A/B verdict (Duolingo ABC lesson screens vs Sound Out lesson screens)

**Winner: A (Tilo track).** A has a character in the lesson frame, a warmer palette and a more finished header. B is clean but bare. Both lose to Duolingo on lesson polish.

**Biggest gap:** Tilo is a 62px badge in the top-left corner of the lesson, not the lesson's companion. Duolingo's mascot is large, sits inside the content and reacts to the question. The lesson body is also a generic grey mountain placeholder ("picture 1") with no real picture, so the middle of the screen has no content. Fix 1 and fix 8 address the mascot; fix 9 addresses the placeholder.

## Numbered fix list (most important first)

1. **Mouth assets carry a stalk.** Every file in `app/public/img/tilo/mouth_{mid,aaa,mmm,ooo}_{1x,2x}.webp` has a dark vertical stick above the mouth blob (confirmed in the 2x contact sheet). Re-cut these from the source so the mouth is a clean blob. `mouth_mmm` is a T-shape and should be a plain closed-lip line.
2. **Mouth sits in the snout, not under it.** Mouth position comes from `TILO.talk.mouths` in `app/public/img/tilo/tilo.json` (fed to `app/src/tilo.js` lines 26-31). Move the `y` anchor of every mouth down to the chin, about 4-6% of `.tilo-stage` height below the snout bottom, so the mouth sits under the nose.
3. **aaa does not read as open.** `mouth_aaa` is only slightly bigger than mid. Make the aaa blob about 1.6-1.8x the mid height, and open the jaw in the speaking pose asset (`speaking_1x/2x.webp`) too, or the flap reads as noise. Check `tilo.js` `FLAP` order (line 14) against the frames.
4. **Speaking state reflows the question.** During speech the answer cards are removed and the picture card shrinks (A_speaking_1_mid vs A_speaking_2_aaa). Keep the cards mounted and set `visibility: hidden` (not `display: none`) during speech, and give the picture container a fixed `width`/`aspect-ratio` so it does not resize.
5. **Ear button covers the profile pill.** On the home and lesson headers (A_home, B_home_no_mascot) the 84px listen button in the top-right overlaps the "Who... reading" pill. Add `padding-inline-end` to the header row, or move the pill left, in `app/src/style.css` header rules.
6. **Encouraging and speaking look the same.** Both use a single raised hand (`encouraging_1x/2x.webp` vs `speaking_1x/2x.webp`). Redraw encouraging with a distinct gesture (both hands together or a thumbs-up) so it does not read as a wave.
7. **Tilo is too small in the lesson header.** `.hdr-tilo .tilo.inline { width: 62px }` in `app/src/style.css` (line 187). Raise to about 96px, or move Tilo into the body above the question with a speech bubble.
8. **Speaking pose reads as alarm.** The open "o" mouth with a raised arm reads as shock in `emulator_lesson_tilo.png`. Use a smaller open mouth with a smile curve for speaking (`mouth_mid`), keeping `aaa` only for the flap.
9. **Lesson body is a placeholder.** The "picture 1" mountain-and-sun card is generic and makes the lesson look empty. Replace it with real picture art before the next store build (outside Tilo's scope, but it is the largest visual gap vs Duolingo).
10. **Lower third is empty on question screens.** In B_no_mascot and the speaking frames, the bottom 40% has no content. Anchor the speaker button and cards to the bottom, or enlarge the picture card.
11. **Yellow focus rings in the default state.** A_idle shows a yellow ring on Check 1 and on the ear button. Scope focus rings to `:focus-visible` in `app/src/style.css` so they do not show after a tap.
12. **Cuteness at header size.** At 62px the teal bag and bead are hard to see and the face loses its eyes. Use the `1x` poses only at 62px-96px and the `2x` set above 96px, and check that the body keeps the blush.

---

## Round 2

Judged fresh on the re-shot `store/android-test/tilo-in-app/` (A_*, B_*) and `store/android-test/pictures-in-app/` (1 to 4). `emulator_lesson_tilo.png` excluded, as instructed. Commits reviewed: 02706ac, e9c28fe.

### Per-screen verdict (child track)

| Screen | Mouth placement | Cuteness | Clarity (360x640) | Pose reads | Picture cards | Result |
|---|---|---|---|---|---|---|
| A_celebrating | n/a | PASS | FAIL: the head and sparkles touch the top edge (96px Tilo has no top inset) | PASS, arms up | PASS, sun fills card at a good size | FAIL (top clip) |
| A_encouraging | n/a | PASS | PASS | FAIL: now the thinking pose (hand to chin), so it reads as "thinking", not "encouraging" | PASS | FAIL |
| A_idle | n/a | PASS | FAIL: yellow halo on the ear button at rest (see fix 6) | PASS | PASS | FAIL (halo) |
| A_idle_hint | n/a | PASS | FAIL: halo on Check 3, which reads as a selected answer | PASS | PASS | FAIL (halo) |
| A_listening | n/a | PASS | PASS | PASS, hand to ear | PASS | PASS |
| A_speaking_1_mid | FAIL: mouth is an open "o" inside the snout, not under the nose | PASS | PASS: cards hidden, picture card holds its size (fixed, was FAIL) | FAIL: arm raised plus open "o" reads as alarm, not speech | PASS | FAIL |
| A_speaking_2_mmm | FAIL: mmm frame shows the same open "o" as mid, so the flap is not visible | PASS | PASS | FAIL: same as mid | PASS | FAIL |
| A_home | n/a (Tilo in hero) | PASS | PASS: ear button no longer covers the profile pill (fixed) | PASS, wave | n/a | PASS |

### Per-screen verdict (grown-up track)

| Screen | Mascot absent? | Clarity | Result |
|---|---|---|---|
| B_home_no_mascot | PASS, no Tilo | PASS, pill clear of ear button | PASS |
| B_no_mascot | PASS, no Tilo | PASS, bottom 40% empty | PASS (layout note, fix 10) |

### Picture-card screens (pictures-in-app)

| Screen | Result | Why |
|---|---|---|
| 1_first_sound | PASS | Sun picture at a good size, three cards aligned, Tilo clear of content. |
| 2_blend_pictures | FAIL | Card 1 has no picture at all: an empty box with a speaker and check. Reads as a broken or missing asset, and a blank card is itself a hint. |
| 3_listen_story | PASS (minor) | Three panels read as a story. The 2+1 grid leaves the bottom-right empty. |
| 4_listen_question | FAIL | Tilo has the open-mouth alarm pose, and roughly 55% of the screen is empty below the prompt. |

### A/B verdict (Duolingo ABC vs Sound Out round 2)

**Winner: A (Tilo track), by a wider margin than round 1.** Tilo is now 96px in the header, and the real word pictures make the cards read as a lesson. Both still lose to Duolingo ABC on lesson polish.

**Biggest gap now:** the lesson's middle is still under-filled. In the speaking and Listen frames, the picture and button sit in the top half and the rest of the screen is blank. Duolingo fills the frame with content and a character that reacts to it. Sound Out has no speech bubble and Tilo is still a corner companion, not part of the content.

### Response to the builder's rebuttal

- **Fix 1 (stalk) and fix 2 (mouth anchor):** I did not accept "matches the lip-sync-passed demo." A demo passing lip-sync does not mean it reads as a mouth at the size users see it. In `A_speaking_1_mid` and `A_speaking_2_mmm` the mouth sits inside the snout, and the mid and mmm frames look identical. Keep both fixes open. If the demo really has the stalk, the demo is also wrong. Show a 2x crop of the speaking frame with the mouth placed under the nose and a flap that changes between frames.
- **A_idle ring:** the hint can stay as a concept, but a static yellow halo on a control at rest reads as focus or selection. Use a pulse or a one-time bob on the ear button and keep the ring for `:focus-visible` only.

### Remaining fix list (most important first)

1. **Mouth still inside the snout, and the flap does not change.** In both speaking frames the mouth is an open "o" in the snout. Move the anchor in `TILO.talk.mouths` (`app/public/img/tilo/tilo.json`, used by `app/src/tilo.js` lines 26-31) about 4-6% of `.tilo-stage` below the snout bottom. Make mmm a closed-lip line, not the open "o". Check that mid and mmm are visibly different in a 2x crop.
2. **Speaking pose reads as alarm.** Arm raised plus open "o" is "Oh!" (`A_speaking_1_mid`, `4_listen_question`). Use a smile-open mouth for speaking, or a speaking pose with the arm down, and keep the open "o" for the aaa flap only.
3. **Encouraging is now thinking.** `A_encouraging` uses the thinking pose, so the state reads as "hmm". Give encouraging its own asset: both hands together or a thumbs-up, from `encouraging_1x/2x.webp` redrawn, not a reuse.
4. **Empty picture card in 2_blend_pictures.** Card 1 has no image. Either give the card a real picture or hide the picture box and keep the speaker and check, so it does not read as a broken asset.
5. **Lower half empty in speaking and Listen frames.** `4_listen_question` and the speaking frames leave roughly 40-55% of the screen blank. Anchor the Listen prompt and speaker lower, or enlarge the picture card in `app/src/style.css` (`.picture` sizing, `picture-gap` rules from e9c28fe).
6. **Yellow halo at rest.** `A_idle` puts a yellow ring on the ear button and `A_idle_hint` on Check 3. Keep the hint, but use a pulse animation, and keep the solid ring for `:focus-visible` only.
7. **Tilo touches the top edge.** At 96px Tilo's ears and sparkles touch y=0 in `A_celebrating`. Add top padding to the header in `app/src/style.css` or drop the header Tilo to 88px.
8. **No speech bubble.** Tilo is a corner companion with no bubble, so the lesson has no voice. Add a bubble next to the header Tilo for the prompt in `app/src/tilo.js` or the lesson layout.
9. **Lesson body still has no hero content.** The picture card is good, but the lesson has no mascot-sized moment. Duolingo fills the frame with a character and content. Consider a larger Tilo beat on Listen intro screens (3_listen_story already has the space).
10. **Asymmetric story grid.** `3_listen_story` leaves the bottom-right empty. Center the third panel or use a 3-up strip.
11. **Lesson-screen polish still behind Duolingo.** Flat grey buttons and no progress celebration. This is the gap to close after items 1-8.

---

## Round 3

Judged on the round-3 re-shot (commits 90f80b8, 1f9bad3). Tilo screens are the 9 `A_*` child-track shots plus the 4 `pictures-in-app` shots (13 total). `B_*` shots have no Tilo and are judged as controls only. `emulator_lesson_tilo.png` skipped (stale).

### Mouth check (mouth_zoom.png)

Three distinct mouths at 2x: closed smile (mmm), small open D (mid), larger open D with tongue (aaa). No stalk. The flap changes between frames, so round 2 fix 1 is closed. Mouth placement on the snout is accepted per the lead ruling.

### Per-screen verdict (child track, Tilo screens)

| Screen | Mouth | Cuteness | Clarity (360x640) | Pose reads | Result | Reason |
|---|---|---|---|---|---|---|
| A_speaking_closed_mmm | PASS (closed smile reads as mmm) | PASS | FAIL | PASS (ruling: wave stays) | FAIL | Cards hidden with `visibility: hidden`, so the bottom ~35% of the frame is blank while Tilo talks. Round 2 fix 5 not addressed. |
| A_speaking_mid | PASS (small open D, distinct from mmm) | PASS | FAIL | PASS | FAIL | Same blank lower third. |
| A_speaking_open_aaa | PASS (aaa visibly bigger than mid) | PASS | FAIL | PASS | FAIL | Same blank lower third. |
| A_celebrating | PASS (closed smile) | PASS | PASS, top gap fixed, no clip | PASS | PASS | Arms up and sparkles clear of y=0. |
| A_idle | n/a | PASS | PASS, no rings at rest | PASS | PASS | Ring gone from ear button and Check 1. |
| A_idle_hint | n/a | PASS | PASS at rest; PASS at pulse peak | PASS | PASS | Pulse accepted. Peak frame shows a yellow ring on ear button and Check 1 (see fix 5). |
| A_listening | n/a | PASS | PASS | PASS (hand at head) | PASS | Reads as listening. |
| A_encouraging | n/a | PASS | PASS | Thinking pose | PASS | Ruled: thinking pose fits a wrong answer. |
| A_home | n/a | PASS | PASS, ear button clear of pill | PASS (wave) | PASS | |
| pictures 1_first_sound | n/a | PASS | PASS | PASS (listening) | PASS | |
| pictures 2_blend_pictures | n/a | PASS | PASS | PASS | PASS | Card 1 now has a real picture (woven mat). Round 2 fix 4 closed. Mat is a little abstract. |
| pictures 3_listen_story | n/a | PASS | PASS | PASS (wave) | PASS (minor) | 2+1 panel grid still leaves bottom-right empty (round 2 fix 10 open). |
| pictures 4_listen_question | n/a | PASS | PASS | PASS (listening) | PASS | Scene picture fills the slot. Bottom ~17% blank, down from ~55%. Open-mouth alarm pose gone. |

Control shots (no Tilo, not counted): B_home_no_mascot PASS (pill clear of ear button). B_no_mascot PASS (bottom ~45% empty).

**Screens passed: 10 of 13. Round 3 FAILS** (the three speaking frames).

### A/B verdict (Duolingo ABC vs Sound Out child track)

**Winner: Duolingo ABC.** Caveat: most duolingo_abc shots are store marketing crops, not lesson frames. The lesson frames (3, 4, 9) are the fair comparison, and they still win. Duolingo's mascot and content sit inside the lesson frame at scale, the progress bar is a chunky green band, and the tiles and letters are large with bold contrast. Sound Out's strengths are a calmer palette, a clean question hierarchy, and a Tilo that now has a pose per state. Sound Out's lesson frame still looks like a settings page next to Duolingo's.

### Remaining fix list (most important first)

1. **Speaking frames leave the bottom third blank.** `.options.pending { visibility: hidden }` in `app/src/style.css` (line 205) keeps the slot empty. Fix: while speaking, show the answer cards dimmed and non-interactive (opacity around .45, `pointer-events: none`), or put the speech bubble (fix 2) in that slot. Keep the same size. Check `A_speaking_mid` at 360x640.
2. **No voice line.** Header Tilo (`.hdr-tilo .tilo.inline`, `app/src/style.css` line 192, 96px) is a corner companion with no speech bubble. Add a bubble tied to the speaking state, driven from the speak hook in `app/src/tilo.js` and the question header in `app/src/screens/l1oral.js`. Round 2 fix 8, still open.
3. **Lesson chrome is behind Duolingo.** `.progress` is 10px high (`app/src/style.css` line 71). Duolingo ABC uses a chunky green band of about 18-20px. Raise the bar to 16-18px, round the fill, and add a small celebration on a correct answer (bar step plus a Tilo beat). Give the check buttons a bottom ledge so they match the bar's weight.
4. **Story grid is asymmetric.** `pictures-in-app/3_listen_story` leaves the bottom-right empty (round 2 fix 10). Centre the third panel or use a 3-up strip. The story grid rule was not located in this pass; start in `app/src/screens/listen.js`.
5. **Idle-hint pulse peaks look like focus.** At peak, `A_idle_hint` shows the same yellow ring on the ear button and Check 1 that focus uses. Keep the pulse (`app/src/style.css` line 155), but tint it softer than the focus ring so a hint never reads as a selected answer or a focused control.
6. **Tilo is still small next to the content.** At 96px in the header, Tilo is a companion, not the lesson's moment. Add a larger Tilo beat on Listen intro screens (round 2 fix 9).

---

## Round 4

Judged on the round-4 re-shot (builder commit 22e15b2). Tilo screens are the 9 `A_*` child-track shots plus the 4 `pictures-in-app` shots (13 total). `B_*` shots are controls, not counted. `emulator_lesson_tilo.png` skipped (stale). Lead rulings respected: thinking pose on encouraging, waving arm on speaking, mouth on the snout are not re-failed.

### Per-screen verdict (child track and pictures)

| Screen | Cuteness | Clarity (360x640) | Pose / state reads | Result | Reason |
|---|---|---|---|---|---|
| A_speaking_closed_mmm | PASS | PASS: dimmed answer cards fill the lower slot, bubble "First sound?" clear | PASS | PASS | Round 3 blank lower third closed. |
| A_speaking_mid | PASS | PASS | PASS (ruled wave) | PASS | Mouth distinct from mmm. |
| A_speaking_open_aaa | PASS | PASS | PASS | PASS | Larger open mouth, flap visibly changes. |
| A_celebrating | PASS | PASS: arms up and sparkles clear of y=0 | PASS | PASS | |
| A_idle | PASS | PASS: no rings at rest | PASS | PASS | |
| A_idle_hint | PASS | FAIL: at pulse peak the ear button and Check 3 show a saturated yellow ring (`@keyframes halo`, peak rgba(255,214,90,.95), 7px offset) that is the same as the focus ring | PASS | FAIL | Round 3 fix 5 not made. At peak Check 3 reads as the selected answer. |
| A_listening | PASS | PASS | PASS (hand at head) | PASS | |
| A_encouraging | PASS | PASS | Thinking pose (ruled) | PASS | |
| A_home | PASS | PASS: ear button clear of pill | PASS (wave) | PASS | Pale halo on "Sound games" reads as selected, not focus. |
| pictures 1_first_sound | PASS | PASS | PASS (listening) | PASS | |
| pictures 2_blend_pictures | PASS | FAIL: option 2 is an empty dotted box with a speaker glyph (`.picture-gap`, style.css line 213) while options 1 and 3 have pictures | PASS | FAIL | Reads as a missing image, the same defect as round 2 fix 4. Round 3 mat card has been replaced by the dotted gap. |
| pictures 3_listen_story | PASS | FAIL: 2+1 grid leaves the bottom-right cell empty | PASS (wave) | FAIL | Round 2 fix 10 and round 3 fix 4 still open. Asymmetry is a visible layout defect. |
| pictures 4_listen_question | PASS | PASS: bottom ~17% blank | PASS (listening) | PASS | |

**Pass count: 10 of 13. Round 4 FAILS.** Fixed since round 3: the speaking frames (cards dimmed and inert, no reflow), the speech bubble, the 17px progress bar and the correct-answer cheer.

### Per-screen verdict (grown-up control shots, not counted)

B_home_no_mascot PASS. B_no_mascot PASS (bottom ~40% empty, layout note only).

### A/B verdict (Duolingo ABC lesson frames 3, 4, 9 vs Sound Out child track)

**Winner: Duolingo ABC.** Caveat: frames 3, 4 and 9 are store crops in a phone frame, but frame 3 is a fair lesson comparison. Duolingo's mascot is large and sits in the content, its progress bar is a chunky green band, and the letters fill the frame. Sound Out closed part of the gap this round: the bar is now chunky, dimmed cards keep the lower third full while Tilo talks, and the bubble gives Tilo a voice. Tilo is still a 96px corner companion, and the lesson body still reads as a settings stack. Gap is narrower than round 3.

### Remaining fix list (most important first)

1. **Blend card 2 looks like a missing image.** `.picture-gap` (`app/src/style.css` line 213) is used for an ambiguous word in the blend options (`app/src/screens/blend.js`, `app/src/screens/l1oral.js`, grep `picture-gap`). Give that word a real picture, or drop the picture box so all three cards are speaker-only with the same structure. Do not mix a dotted box with pictured cards.
2. **Idle-hint peak reads as focus.** `@keyframes halo` (`app/src/style.css` lines 156-157) peaks at a saturated yellow with a 7px offset. Lower the peak alpha to about .45, reduce the offset to 3-4px, and keep the solid ring for `:focus-visible` only. Check the peak frame on both the ear button and Check 3.
3. **Story grid is asymmetric.** `.pics` (`app/src/style.css` line 117) is a 2-column grid, and `app/src/screens/listen.js` line 12 renders the three panels into it. Centre the third panel (`grid-column: 1 / -1; justify-self: center; max-width: 50%` on the odd last child, behind a `.pics.story` class added in listen.js). Open since round 2.
4. **Tilo has no mascot-scale moment.** The 96px header Tilo (`.hdr-tilo .tilo.inline`, `app/src/style.css` around line 192) is still a corner companion. Add a larger Tilo beat on the Listen intro, where `3_listen_story` has room (`app/src/screens/listen.js` and `app/src/tilo.js`). Round 2 fix 9, still open.
5. **Lower third on the Listen question is blank.** `4_listen_question` leaves about 17% empty. Anchor the speaker and prompt lower, or enlarge `.pics.scene` (`app/src/style.css` line 215). Minor.

---

## Round 5

Judged on the round-5 re-shoot (commit c7e2a4b, code from f490621). Tilo screens are the 9 `A_*` child-track shots plus the 4 `pictures-in-app` shots (13 total). `B_*` shots are controls, not counted. `emulator_lesson_tilo.png` skipped (stale). Lead rulings respected: thinking pose on encouraging, waving arm on speaking, mouth on the snout, and speaker-only blend sets are not re-failed.

### Per-screen verdict (child track and pictures)

| Screen | Cuteness | Clarity (360x640) | Pose / state reads | Result | Reason |
|---|---|---|---|---|---|
| A_speaking_closed_mmm | PASS | PASS: dimmed cards fill the lower slot, bubble clear | PASS (wave ruled) | PASS | Closed smile reads as mmm. |
| A_speaking_mid | PASS | PASS | PASS | PASS | Small open mouth, distinct from mmm (mouth_zoom.png). |
| A_speaking_open_aaa | PASS | PASS | PASS | PASS | Larger open mouth, flap changes between frames. |
| A_celebrating | PASS | PASS: head and sparkles clear of y=0 | PASS, arms up | PASS | |
| A_idle | PASS | PASS: no yellow ring at rest | PASS | PASS | Faint grey pulse ring on the ear button in this frame, not a focus colour (note only). |
| A_idle_hint | PASS | PASS: pulse peak is a pale yellow ring on Check 1, no ring on the ear button | PASS | PASS | Round 4 fix 2 done: peak is softer than the focus ring. Still a ring on one answer at peak, so watch it (note only). |
| A_listening | PASS | PASS | PASS, hand at head | PASS | |
| A_encouraging | PASS | PASS | Thinking pose (ruled) | PASS | |
| A_home | PASS | PASS: ear button clear of profile pill | PASS, wave | PASS | Pale halo on the current lesson reads as "current", not focus. |
| pictures 1_first_sound | PASS | PASS | PASS, listening | PASS | |
| pictures 2_blend_pictures | PASS | PASS: three speaker-only cards, same size, no dotted box | PASS, listening | PASS | Round 4 fix 1 done. Bottom ~28% blank, layout note only. |
| pictures 3_listen_story | PASS | PASS: third panel centred | PASS, wave | PASS | Round 4 fix 3 done. Bottom ~13% blank, note only. |
| pictures 4_listen_question | PASS | PASS: bottom ~16% blank | PASS, listening | PASS | |

**Pass count: 13 of 13. Round 5 PASSES.**

Fixed since round 4: blend card 2 no longer reads as a missing image (speaker-only sets), the idle hint peak is softer, and the story's third panel is centred.

Control shots (not counted): B_home_no_mascot PASS. B_no_mascot PASS (bottom ~35% empty, layout note only).

### A/B verdict (Duolingo ABC lesson frames 3, 4, 9 vs Sound Out child track)

Not blind: the labels were not shuffled in this pass, so treat this as an unblinded read.

- **Mascot:** Tilo wins on pose coverage (wave, listening, thinking, celebrating, three mouth shapes) and on a calm, cute look. Duolingo wins on scale and integration: its character sits inside the frame and reacts to the content.
- **Lesson polish:** Duolingo ABC wins. Its frame is filled with content and a large character, and its progress band is bolder. Sound Out's lesson frame still reads as a tidy settings stack, with Tilo as a 96px corner companion.

**Winner: Duolingo ABC on lesson polish. Tilo wins on the pose set.** The gap is narrower than round 4.

### Remaining fixes (most important first, none block the pass)

1. **Tilo is still a corner companion, not a lesson moment.** `.hdr-tilo .tilo.inline { width: 96px }` (`app/src/style.css` line 192). Open since round 2 fix 9 and round 4 fix 4. Add a larger Tilo beat on the Listen intro (`app/src/screens/listen.js`, `app/src/tilo.js`).
2. **Lower third is blank on the blend question.** `2_blend_pictures` leaves ~28% empty below the options. `.options` (`app/src/style.css` line 92) sits at the top of the slot. Anchor the options lower, or add a larger Tilo or bubble beat in that space.
3. **Lesson body still lacks hero content.** The picture cards are good, but the frame has no mascot-scale moment. Duolingo fills the frame with a character and content. Same root as fix 1; close it before polishing chrome.
4. **Watch the idle-hint peak.** The pale yellow ring on Check 1 (`A_idle_hint`) still sits on an answer. Keep it, and keep the solid ring for `:focus-visible` only (`@keyframes halo`, `app/src/style.css` ~lines 156-157). Note only.
