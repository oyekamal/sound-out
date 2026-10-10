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
