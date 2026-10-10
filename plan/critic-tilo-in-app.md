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
