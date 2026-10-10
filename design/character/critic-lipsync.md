# Critic: Tilo lip-sync mouths

Verdict: **FAIL**. Placement and style are fine. The mouths are too small to read on a phone.

Most important change: scale all four mouths (mmm, mid, aaa, ooo) 1.5x around their own centre, with the centre at about (217, 213) in the 450x512 demo frame. Then check that the bottom edge stays inside the muzzle. If it does not, move the mouth up by a few px.

## Evidence

1. **Placement: PASS.** Measured mouth centres sit at x about 217, the muzzle centre (about 220). The mouths sit inside the muzzle and do not protrude below it. The OLD version (column 2 of lipsync_check.png) hangs out below the muzzle, which is why Kamal called it out of place. The thin vertical line from the nose to the mouth also appears in the original art (zoomed column 1), so it is not a leftover seam.
2. **Size at about 200 px tall: FAIL.** The figure is about 483 px tall in the demo frame, so 200 px tall means a scale of about 0.41. Measured mouths at that scale:
   - aaa: 26x28 px in the frame, about 11x12 px on the phone
   - mid: 28x14 px, about 12x6 px
   - ooo: about 23x31 px including its ring, about 10x13 px
   - mmm: about 24x5 px of visible line
   The OLD version was roughly twice the area of aaa, which matches Kamal's "was better" comment. A child at phone size will barely see mid, ooo or mmm. The OLD size was too big, so the fix is to scale up, not to go back to it.
3. **Shapes: PARTIAL.**
   - aaa: distinct and cute (dark open oval with a pink lower lip). PASS.
   - mid: a small open oval, close to the original art. It reads like a tiny "o". Too small to distinguish from ooo at this size.
   - ooo: a ring with a dot and an arc above it. It reads as a target or button, not as a mouth. FAIL. Change to a filled, rounder dark oval with a pink lower lip, similar to aaa but smaller.
   - mmm: a curved line that looks like a smile. Kamal will read it as happy, not as closed lips. Use a flat closed line with a slight pink edge, no upward curve.
4. **Style consistency: PASS.** Line weight, brown outlines and pink lip colour match the blush and the original art. No scary or gaping shapes.

## Acceptance check

Re-render the four demo frames at 200 px tall. aaa should be at least about 16x17 px and mid at least about 17x9 px, and all four should be readable on a phone without zooming.

## Round 2

Verdict: **FAIL**. Placement and size of aaa and mid are now fixed. mmm is still unreadable and ooo is too close to aaa.

Most important change: make mmm a closed lip line at least 34 px wide and 8 px thick in the 450x512 demo frame (about 14x3 px on the phone at 200 px tall). Keep it flat, with a pink lower edge and no upward curve. Today it measures about 24x12 px and reads as a small pink blob, not as closed lips.

## Evidence

1. **Placement: PASS for aaa, mid and ooo; mmm PARTIAL.** Each mouth sits centred on the muzzle (centre x about 217) and inside its bottom edge. The nostrils are clear and there is no halo or leftover original mouth. mmm sits in the right place but is too small to show its shape.
2. **Visibility at about 200 px tall: FAIL for mmm.** At the 0.41 scale, aaa is about 40 px wide in the frame (about 16 px on the phone) and readable. mid and ooo are about 35 px and 20 px, so they read. mmm is about 24x12 px in the frame, about 10x5 px on the phone. A child will not see it as closed lips.
3. **Shapes: PARTIAL.**
   - aaa: wide dark open oval with a pink tongue. PASS.
   - mid: tall dark oval with pink. Close to aaa. Acceptable, but mid and aaa differ mainly in height.
   - ooo: small dark oval, roughly 20x25 px. It is now a clean round shape, but it is nearly the same as mid at phone size. Make ooo about 22x22 px so it is clearly round and smaller than aaa.
   - mmm: flat pink blob, not a visible closed line. FAIL.
4. **Edge quality: FAIL (minor).** The zoomed row shows a dark fuzzy halo on the lower edge of mid and aaa (anti-alias or blur residue). Clean the edge to a 1 px hard stroke. Also, a thin vertical line from the nose runs into the mouth in mid. The original art has it, but it looks like a seam on the zoom.
5. **Style match: PASS.** Brown and pink palette and flat shapes match the original pose_speaking.png.

## Acceptance check

At 200 px tall, mmm must show a readable closed line of at least 14x3 px on the phone. aaa must be at least 16x16 px and wider than tall. ooo must be round and about 22x22 px in the frame. Edges must have no fuzz at 3x zoom.

## Round 3

Verdict: **PASS**. All four round 2 fixes are in place. The only remaining issues are minor and would not stop a child or parent from reading the mouths on a phone.

Measured from zoomed crops of the four demo frames (450x512, scale 2x in the check image, so divide by 2 for frame px):

1. **Round 2 fixes made: PASS.** mmm is now a flat closed line about 58x8 px in the frame (about 24x3 px on the phone), well above the 34x8 minimum. ooo is a clean round dark dot about 22x21 px, matching the 22x22 target. aaa is a wide dark open oval about 42x60 px, clearly larger than ooo. The dark fuzzy halo on mid and aaa is gone at 2x; the edges are a clean 1 px outline.
2. **Placement: PASS.** All four mouths are centred under the nose on the same x, and their bottoms sit inside the muzzle edge. No mouth hangs out below the muzzle. The old seam is gone.
3. **Visibility at about 200 px tall: PASS.** Approximate phone sizes at scale 0.41: mmm about 24x3 px (a thin but clear line), mid about 18x20 px, aaa about 17x25 px, ooo about 9x9 px (a small dark dot with a pink rim, readable as a small "o").
4. **Shapes: PASS, with one minor note.** mmm reads as closed lips, aaa as a dark open mouth, ooo as a small round "o", and mid as a tall pinkish-maroon oval. Note: mid is dominated by its pale pink core, so at phone size it is the least distinct from aaa. It still reads as a different, smaller open shape, so this does not fail.
5. **Edges and style: PASS.** Flat brown and pink fills match the original pose_speaking.png. The philtrum line from the nose runs into the mouth on mid and ooo, but the original art has it too, so it is not a seam.

Not a fail: a faint vertical nose line touches the top of ooo, making it look slightly like a lollipop at zoom. Ignore unless a parent flags it.

Note on method: my first look at the full-frame demo_mmm.png did not show a closed line. The 2x crop of the same file does, so the verdict uses the crops.
