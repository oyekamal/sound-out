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
