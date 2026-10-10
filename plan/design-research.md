# Sound Out: design research (colour, motion, onboarding)

Researched 2026-10-10. Scope: Track A (children, Tilo the capybara) and Track B (grown-ups, no mascot). Nothing here edits `app/src`; it is input for the next design pass.

How to read the evidence labels:
- **OFFICIAL**: from a brand guide or the company's own page.
- **SAMPLED/APPROXIMATE**: from a third-party site or a search snippet, not a brand guide. Do not treat as exact.
- **Not stated**: no source we could read gives it. We did not guess.

---

## 0. What we have today (from `store/review/*.webp` and `app/src/style.css`)

Tokens now: `--paper #f6f1e7`, `--card #fffdf8`, `--ink #24211d`, `--accent #2f6f8f`, `--good #3f8a4f`, `--bad #c4553c`, `--hl #ffe08a`. Track B only swaps `--accent #33475b` and `--paper #f4f5f7`.

Honest read of the 95 screenshots:
- **Both tracks are beige.** Track A and Track B differ only by a slightly cooler page. Nothing says "joyful" on A. The only warm colour is Tilo himself (sampled from the render: body `#e1a263`, ear `#ca804c`, bag teal `#1e7b70`, cheek `#fbaaa3`).
- **The main action looks disabled.** The "This one" pick buttons (screens 02, 29) are pale blue with white text, about 2:1 contrast, so they read as greyed out on a screen where they are the only thing a child can press. The Duolingo ABC pattern is the opposite: one saturated button.
- **Motion is thin.** There are about 8 keyframes in `style.css` (pulse, hop, grow, tilo-breathe, tilo-pop, opt-cheer, opt-spark, halo) and a global `prefers-reduced-motion` kill switch. No press depth on buttons, no screen transitions, no progress-fill animation, no unlock or level-complete moment beyond stickers.
- **Onboarding is one text screen** ("Who is reading?", spoken in English) then straight into the first sitting. That is fast, which is good. It has no mascot meeting, no avatar and no celebration before the first lesson.
- **The Level map nodes (screen 12) are all pill-shaped, same size.** Done is pale green, locked is pale beige. The state is only readable through a tiny check or lock badge.
- **Track B home (screen 15) is a plain list.** It is dignified but has no colour state at all.

---

## 1. Prior research taken (from `~/Documents/free_work/urdu-reading-course/research/`)

Urdu-script items (Nastaliq line-height, RTL, Noorani Qaida font notes, Ajrak/truck-art motifs) are ignored. What applies:

| Rule | From | Use here |
|---|---|---|
| Touch targets 60-80 px for ages 3-5, 50-60 px for 6-8, 64 px spacing | `12_child_ux.md` (Gapsy Studio, NN/g) | Child buttons min 64 px tall, 16 px gap. Today's `.btn` is 52 px and `.btn.small` 48 px. |
| Children expect feedback on every tap; mistakes must never feel like failure; no red X, no buzzer; use colour AND icon AND sound | `12_child_ux.md` | Every tap gets a reaction within 100 ms. Wrong = soft shake + Tilo "hmm", never a red flash. |
| One task per screen, 3-5 choices max, repeat button always visible | `12_child_ux.md` | Already true. Keep the speaker button reachable. |
| 3-5 minute lesson blocks (Khan Academy Kids case, second-hand) | `12_child_ux.md` | A "sitting" stays 3-5 min. |
| No streak pressure, no leaderboards, no guilt copy, no fake urgency | `12_child_ux.md`, `18_emotional_design_talk.md` | Keep "days practised" as a quiet count only. No streak loss, ever. |
| Micro-animations are emotional feedback loops: bounce, sparkle, glow on repeated actions; celebrate small wins; expressive mascot; animate progress and milestones | `18_emotional_design_talk.md` (talk summary supplied by Kamal, not re-checked against the video) | Basis of the motion spec in section 4. |
| Duolingo path: grey locked, saturated current, gold done; one colour band per unit inside one brand palette | `13_ui_reference.md` | Level bands in 3B. State by colour + shape + icon. |
| Press = hard shadow collapses (3D button) | `13_ui_reference.md` | Section 4, press spec. |
| Age-tune saturation: calmer for the youngest, full primary energy for preschoolers; one brand, two modes | `13_ui_reference.md` (Lingokids design write-up) | A = high saturation, B = same bones at low saturation. |
| Interactive elements never at the screen edge | `13_ui_reference.md` (Lingokids) | Keep 16 px side gutter. Tilo's corner placement is fine. |
| Cut chrome, then simplify again after testing with real children | `13_ui_reference.md` (HOMER case study, via search summary) | Do not add decoration to Track B. |
| Avoid the "AI cream + terracotta + brass" palette | `13_ui_reference.md` | Our `#f6f1e7` paper is close to the banned cream. Section 3A moves to a clearer warm white plus real colour. |
| Parent gate as a spoken-number or digit challenge | `12_child_ux.md` | Keep `gate.js`. See section 5. |
| Emoji are not icons (render differently across Android) | `13_ui_reference.md` | Keep SVG icons. |

---

## (a) Popular apps: palette, onboarding, motion

Popularity numbers are store snapshots from 2026-10-10 and trackers disagree. Ranked by the biggest install bucket and rating count: Lingokids (Play 50M+, 222K ratings), Duolingo ABC (10M+), Khan Academy Kids (10M+, best rating, 4.8 on iOS from 131K), Prodigy (5M+), ABCmouse (5M+), Reading Eggs (5M+), Teach Your Monster to Read (1M+, paid), Endless Alphabet (1M+, paid). HOMER has no Play figure we could find.

| App | Popularity (store, 2026-10-10) | Palette | Onboarding | Motion |
|---|---|---|---|---|
| **Duolingo ABC** | Play 3.9 from 23.6K ratings, 10M+ ([Play](https://play.google.com/store/apps/details?id=com.duolingo.literacy&hl=en&gl=US)). iOS 4.2 from 3.8K ([App Store](https://apps.apple.com/us/app/learn-to-read-duolingo-abc/id1440502568)). | No ABC-specific palette. Duolingo brand core, **OFFICIAL** per [design.duolingo.com/identity/color](https://design.duolingo.com/identity/color) as quoted in a search summary (the page redirects to the blog hub when fetched, so we could not re-read it): Feather Green `#58CC02`, Mask Green `#89E219`, Eel `#4B4B4B`, Snow `#FFFFFF`. Same source, secondary: Macaw `#1CB0F6`, Cardinal `#FF4B4B`, Bee `#FFC800`, Fox `#FF9600`, Beetle `#CE82FF`, Humpback `#2B70C9`; neutrals Wolf `#777777`, Hare `#AFAFAF`, Swan `#E5E5E5`, Polar `#F7F7F7`. The four core values are corroborated by [BrandPalettes](https://brandpalettes.com/duolingo-colors/) (SAMPLED). Beak colours `#B66E28 #F49000 #FFC200 #FFDE00` are SAMPLED, same page. | **About 11 steps listed, "over a dozen" in its own notes** ([ScreensDesign](https://screensdesign.com/showcase/learn-to-read-duolingo-abc)). Preview shows welcome, "how did you hear about us", child name, character pick ([ScreensDesign onboarding](https://screensdesign.com/explore/apps/duolingo-abc/onboarding/)). The **parent** types the child's name; then privacy/terms, microphone, optional email ([Common Sense](https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read)). First child task: spell the child's own name. Parent gate protects settings and level-locking with numbers typed as words (ScreensDesign showcase, 05:27). A sample lesson before sign-up: **not stated** for ABC. (The main Duolingo app does one, [Appcues](https://goodux.appcues.com/blog/duolingo-user-onboarding).) | "Animated cinematic" intro; stories advance on tap; visual city map as the core loop; a "sparkling coin animation" on lesson complete; "satisfying sounds and animations" ([ScreensDesign](https://screensdesign.com/showcase/learn-to-read-duolingo-abc)). Duolingo's own art post says moving things win attention and animated skill icons held attention longer than static ones; characters are exaggerated "almost to the point of caricature"; timings **not stated** ([Duolingo blog](https://blog.duolingo.com/shape-language-duolingos-art-style/)). Main-app characters have "20+ mouths" and idle head nods, blinks and eyebrows, driven by Rive state machines ([Duolingo blog](https://blog.duolingo.com/world-character-visemes/), via search). 4 px hard bottom shadow on buttons and 12 px radius come from a third-party description of the main app, not Duolingo ([opendesigner.io](https://opendesigner.io/design-systems/duolingo), SAMPLED). |
| **Khan Academy Kids** | Play 4.57 from 57K, 10M+ ([Play](https://play.google.com/store/apps/details?id=org.khankids.android&hl=en&gl=US)). iOS 4.8 from 131K, "always 100% free, no ads, no subscriptions", ages 2-8 ([App Store](https://apps.apple.com/us/app/khan-academy-kids/id1378467217)). | No Kids palette found. Colours are **not stated** in any readable source. (A Khan Academy, not Kids, listing gives `#9CB443`; unverified: [brandcolor.dev](https://brandcolor.dev/brands/khan-academy).) | Parent gives an email and confirms it; then creates child profiles with name, avatar and age; the animal guides greet them ([Common Sense](https://www.commonsensemedia.org/app-reviews/khan-academy-kids) and a video walkthrough via search). Screen count, parent gate, sample lesson: **not stated**. | Not stated. Only fact found: it has a lead animator for Kodi Bear ([video](https://m.youtube.com/watch?v=Nflprw-Ni-I)). |
| **Lingokids** | Play 4.33 from 222K, **50M+** ([Play](https://play.google.com/store/apps/details?id=es.monkimun.lingokids&hl=en&gl=US)). iOS 4.3 from 665K ([App Store](https://apps.apple.com/us/app/lingokids-games-shows/id1002043426)). | Official [brandbook PDF](https://lingokids.com/wp-content/uploads/2020/10/LINGOKIDS_brandbook.pdf) exists but has no readable text. Confirmed OFFICIAL: fallback fonts Arial and Nunito. Character swatches are SAMPLED, not UI colours: Eliot `#ff3c64 #3cdcb4 #787878 #fff0f0` ([colorswall](https://colorswall.com/palette/268564)). Lingokids' own design principle (via `13_ui_reference.md`): calmer for babies, full primary colours for preschoolers. | Email sign-in plus one child profile with name, birth month and year, English level; subscription with a 7-day trial, so **no sample lesson before sign-up** ([Common Sense](https://www.commonsensemedia.org/app-reviews/lingokids-play-and-learn)). Parent gate: tap twice and enter your birth year ([Lingokids help via search](https://help.lingokids.com/hc/en-us/articles/115005129325)). | Not stated. |
| **Reading Eggs** | Play 4.1 from 12K, 5M+ ([Play](https://play.google.com/store/apps/details?id=com.blake.readingeggs.android&hl=en&gl=US)). iOS 4.7 from 7.4K ([App Store](https://apps.apple.com/us/app/reading-eggs-learn-to-read/id726696040)). | Not found. | 4-step parent sign-up making the parent account and first child; 30-day trial; child name and **birth year** pick the programme; a placement test on first lesson that stops after 3 wrong answers and can be skipped; avatar edited later, not in sign-up ([getting-started guide](https://readingeggs.com.au/articles/getting-started-guide-parents/), [avatar help](https://support.readingeggs.com/support/solutions/articles/245297-how-can-my-child-change-the-appearance-of-their-avatar-)). | Not stated. |
| **Teach Your Monster to Read** | Play 4.6 from 4K reviews, 1M+, paid ([Play](https://play.google.com/store/apps/details?id=com.teachyourmonstertoread.tmapp&hl=en-US)). iOS 4.5 from 30K, $8.99 ([App Store](https://apps.apple.com/us/app/teach-your-monster-to-read/id828392046)). | No official hexes found ([press centre](https://www.teachyourmonster.org/press-centre/)). | **The child builds their own monster first** (body, head, face, ears), then picks one of three starting points: beginner, knows letter sounds, ready for sentences ([Horn Book](https://hbook.com/story/teach-your-monster-to-read-app-review), [Common Sense](https://www.commonsensemedia.org/app-reviews/teach-your-monster-to-read)). Since Feb 2024 new users sign up before playing ([App Store note](https://apps.apple.com/us/app/teach-your-monster-to-read/id828392046)). Narrated by a voice actor ([overview](https://www.teachyourmonster.org/teach-your-monster-to-read-overview/)). Parent gate: not stated. | Not stated. Story beat: after the build the monster boards a spaceship. |
| **Endless Alphabet** | Play 4.3 from 17.8K reviews, 1M+ ([Play](https://play.google.com/store/apps/details?id=com.originatorkids.EndlessAlphabet&hl=en-US)). iOS 4.6 from 1.4K, $8.99 ([App Store](https://apps.apple.com/us/app/endless-alphabet/id591626572)). | Not found. | No child questions. Opens with a short intro animation of creatures running across the screen; alphabet across the top; narrator speaks every word ([Children and Media Australia](https://childrenandmedia.org.au/app-reviews/apps/endless-alphabet), [Horn Book](https://hbook.com/story/endless-alphabet-app-review)). | Per word: narrator says it, monsters scatter the letters, the child drags them into place, a short animation shows the meaning; letters "talk" ([review](https://childrenandmedia.org.au/app-reviews/apps/endless-alphabet)). No timings. |
| **ABCmouse** | Play 4.4 from 34K, 5M+ ([Play](https://play.google.com/store/apps/details?id=com.aofl.abcmouse&hl=en-US)). iOS 4.1 from 146K ([App Store](https://apps.apple.com/us/app/id6460300848)). | Red `#EE3124`, Blue `#0072CE`, Green `#8DC63F`, **SAMPLED** ([colorcodeguide](https://colorcodeguide.com/official/abcmouse); no brand guide cited). | 13 screens, **hard paywall** (free week then pay), no sample lesson ([Botsi flow recording](https://www.botsi.com/resources/flows/apps/abcmouse)). Parent gate: "complete the equation, 1 + 1", and a birth-year gate for adding a child ([support](https://support.abcmouse.com/hc/en-us/articles/34386800033687-Adding-a-Child-Profile-in-ABCmouse)). Child later picks a teacher and an avatar (search summary only). | Not stated. |
| **HOMER** | iOS 4.4 from 25K ([App Store](https://apps.apple.com/us/app/homer-learn-grow/id601437586)). Play figure not found. | None found. Warning: brand.homer.co is a different company. | Parent answers reading and maths level questions and the child picks topics, under a minute ([Fatherly](https://www.fatherly.com/parenting/homer-learn-and-grow-app-review)). A 2015 wireframe set shows a voiced welcome, "find a grown-up to help you set up", a mirror, optional photo, Skip offered throughout ([PDF](https://kennethroraback.s3.amazonaws.com/media/addenda/Homer-setup-content-management-purchase-popup-wireframes.pdf), older than the current app). The designer says an early version had too much per screen for ages 2-8 and was simplified ([case study](https://www.hollydoodlestudio.com/homer-learn-grow)). | "Native + Lottie animations", custom load screens, achievement celebrations; no timings ([designer page](http://www.hollydoodlestudio.com/homer-learn-grow)). Two-year-olds "expect rich interactions and are unwilling to wait". |
| **Prodigy Math** | Play 4.0 from 68K, 5M+ ([Play](https://play.google.com/store/apps/details?id=com.prodigygame.prodigy&hl=en-US)). iOS 4.8 from 249K ([App Store](https://apps.apple.com/us/app/prodigy-math-game/id950795722)). | Orange `#FF5C0B`, cream `#F7E9DB`, plum `#6F1F3A`, **SAMPLED** from a search snippet ([colorcodehub](https://colorcodehub.com/brand/prodigygame.com)). | The child enters a name, grade and customises a wizard; can start without an account, a parent email is needed to finish ([Common Sense](https://www.commonsensemedia.org/app-reviews/prodigy-kids-math-game), [forum guide](https://prodigy-game.discourse.group/t/how-to-create-your-prodigy-account/29)). | Not stated. |

**What the table tells us (and what it does not):**
1. No source gave millisecond timings, press depths or confetti specs for any kids' app. The numbers in section (c) are therefore **our own spec**, built on named references (Josh Comeau's measured 3D button, Material 3 easing used in our `lottie-motion` skill, WCAG), not copied from those apps.
2. Only Duolingo publishes a palette. The saturated green + orange + sky blue set is its lever; the other apps' colours could not be confirmed. We take Duolingo's structure (one saturated action colour, bands per unit, gold = done) but not its colours, because our mascot is tan and teal.
3. Onboarding patterns that repeat across sources: the **parent does the typing** (name, email, birth year) and the child only taps; avatar or character choice is a child step in 4 of 8 apps (Duolingo ABC, Khan Kids, TYMTR build-a-monster, Prodigy); a **birth-year or arithmetic parent gate** is the norm (Lingokids, ABCmouse, Duolingo ABC); only Reading Eggs and TYMTR ask for a starting level or run a skippable placement. Most of these gate behind an account or trial. **Sound Out has no account, so it can put a child in a lesson in under a minute. Most of the sourced apps put an account, email or trial first (Prodigy can start without one, Duolingo ABC's flow is unclear), so this is the gap to use.**

---

## (b) Recommended palette

Design logic: Tilo is tan and teal on a warm page. The new Track A takes **teal as the main action colour** (Tilo's bag, `#1e7b70`, deepened so white text passes), **sun yellow as the "tap me" colour**, and a family of light unit bands. Today's blue accent is dropped on Track A because it has no link to the mascot. Track B keeps a calm slate-blue family at low saturation so it reads as the same product.

All ratios computed with the WCAG 2.x relative-luminance formula (script in the scratchpad; reproducible with any contrast checker). Targets: body text 4.5:1, large text and UI parts 3:1.

### Track A: child (warm, joyful, high contrast)

```css
.track-A {
  /* surfaces */
  --paper:      #FFF6E5;  /* page: warm cream, lighter and yellower than old #f6f1e7 */
  --card:       #FFFFFF;
  --card-soft:  #FFF1C2;  /* hint / highlight fill */
  --line:       #8C7860;  /* interactive borders (3.94:1 on paper); decorative lines may use #E8DFD0 */
  /* ink */
  --ink:        #2A1F17;  /* warm near-black */
  --muted:      #6A5645;
  /* brand */
  --primary:    #12776B;  /* main action: Tilo-teal, deepened */
  --primary-edge:#0B5148; /* 3D button edge */
  --primary-ink:#FFFFFF;
  --tap:        #FFC53D;  /* "tap me": sun */
  --tap-edge:   #B87300;
  --tap-ink:    #2A1F17;
  --accent:     #E1A263;  /* Tilo tan (sampled from the Tilo render) */
  --accent-deep:#9A5A1E;  /* tan as text */
  /* feedback: colour is never the only signal; always paired with icon + sound */
  --good:       #1B7F41;  --good-edge:#115C2D;  --good-tint:#E0F5E5;  --good-text:#176B38;
  --oops:       #C8452D;  --oops-tint:#FFE8E0;  --oops-text:#A63A22;  /* "oops", not "wrong" */
  --star:       #F2A900;  /* only ever on a dark or white chip, never as text on paper (1.87:1) */
  /* locked */
  --locked-fill:#EADFCB;  --locked-ink:#6A5645;
  /* level bands (fill with --ink text) */
  --band-1:#BFE6F2; --band-2:#CFEBB5; --band-3:#FFE08A; --band-4:#FFD3C7;
  --band-5:#E3D5F7; --band-6:#BFEBDD; --band-7:#F2D3A8;
  --radius: 22px; --press: 5px;
}
```

| Pair (text on background) | Ratio | Result |
|---|---|---|
| `--ink` #2A1F17 on `--paper` #FFF6E5 | 14.97 | pass AAA |
| `--ink` on `--card` #FFFFFF | 16.07 | pass AAA |
| `--muted` #6A5645 on `--paper` | 6.46 | pass AA |
| `--muted` on `--card` | 6.93 | pass AA |
| `--primary-ink` #FFF on `--primary` #12776B (main button) | 5.42 | pass AA |
| `--primary` as text/icon on `--paper` | 5.05 | pass AA |
| `--tap-ink` #2A1F17 on `--tap` #FFC53D (tap-me button) | 10.18 | pass AAA |
| `--tap-edge` #B87300 on `--paper` (button outline vs page) | 3.56 | pass non-text 3:1 |
| `--tap` #FFC53D on `--paper` (fill alone) | 1.47 | **fails alone**: so the tap button always carries the `--tap-edge` edge and ink label |
| #FFF on `--good` #1B7F41 | 5.05 | pass AA |
| `--good-text` #176B38 on `--good-tint` #E0F5E5 | 5.74 | pass AA |
| `--good-edge` #115C2D on `--paper` | 7.55 | pass |
| #FFF on `--oops` #C8452D | 4.83 | pass AA |
| `--oops-text` #A63A22 on `--oops-tint` #FFE8E0 | 5.50 | pass AA |
| `--accent-deep` #9A5A1E on `--paper` | 5.08 | pass AA |
| `--ink` on `--accent` #E1A263 | 7.31 | pass |
| `--ink` on `--card-soft` #FFF1C2 | 14.24 | pass |
| `--locked-ink` #6A5645 on `--locked-fill` #EADFCB | 5.25 | pass AA |
| `--ink` on bands 1-7 | 11.2 to 12.5 (sky 12.10, leaf 12.40, sun 12.46, blush 11.78, lilac 11.58, mint 12.35, tan 11.22) | pass AAA |
| `--line` #8C7860 on `--paper` | 3.94 | pass 3:1 |

Picks, as asked:
- **Accent (brand):** Tilo tan `#E1A263` for decoration, badges and the village; `#9A5A1E` when it must be text.
- **Main action:** teal `#12776B` with white label.
- **"Tap me":** sun `#FFC53D` with ink label and `#B87300` edge. Use it for exactly one thing per screen, the thing the child should press next, and let it pulse (section c). Rationale: yellow is the one colour no state uses, so it never means "right" or "wrong".
- **Success:** green `#1B7F41` + a check icon + a rising chime.
- **Error:** warm coral `#C8452D` shown only as a thin border and tint, always paired with Tilo's thinking pose and a soft "hmm" sound. The label word is "try again", never "wrong".

Do not copy Duolingo's white-on-Feather-Green label: it measures 2.09:1 (white on `#58CC02`), and white on Macaw `#1CB0F6` is 2.44:1. Duolingo gets away with it by relying on big bold type; our readers are learning to read, so we do not.

### Track B: grown-up (calm, adult, dignified)

```css
.track-B {
  --paper:#F4F5F7; --card:#FFFFFF; --line:#76848F;   /* line 3.84:1 on card, 3.27:1 on paper with #7C8998 */
  --ink:#1E2A36; --muted:#566272;
  --primary:#2F5573; --primary-edge:#22405A; --primary-ink:#FFFFFF;
  --tap:#2F5573;           /* no "tap me" yellow: next step is the primary button */
  --accent:#2F5573;
  --good:#2D7A4D; --good-tint:#E4F2E8; --good-text:#1F6039;
  --oops:#B0432C; --oops-tint:#FBE9E4; --oops-text:#9C3B26;
  --hl:#FFE08A;            /* reading highlight, same as today */
  --radius: 14px; --press: 2px;
}
```

| Pair | Ratio | Result |
|---|---|---|
| `--ink` #1E2A36 on `--paper` #F4F5F7 | 13.37 | pass AAA |
| `--ink` on `--card` | 14.59 | pass AAA |
| `--muted` #566272 on `--paper` | 5.69 | pass AA |
| `--muted` on `--card` | 6.20 | pass AA |
| #FFF on `--primary` #2F5573 | 7.87 | pass AAA |
| `--primary` on `--paper` | 7.22 | pass |
| #FFF on `--good` #2D7A4D | 5.25 | pass AA |
| `--good-text` #1F6039 on `--good-tint` | 6.51 | pass AA |
| #FFF on `--oops` #B0432C | 5.70 | pass AA |
| `--oops-text` #9C3B26 on `--oops-tint` | 5.83 | pass AA |
| `--ink` on `--hl` #FFE08A | 11.31 | pass |
| `--line` #76848F on `--card` | 3.84 | pass 3:1 |

Today's tokens for comparison: white on old `--accent` #2f6f8f is 5.54 (fine), but `--good` #3f8a4f on card is 4.17 and `--bad` #c4553c on card is 4.38, both just under AA for small text. The new values fix that.

Track B differences from A: no yellow, smaller radius (14 px vs 22 px), press depth 2 px not 5 px, status by colour **and** word ("Done", "Locked") not just icon, and the home screen gets the same unit bands at 40% opacity as a thin left stripe on each lesson card so levels are findable without becoming childish.

Track-wide: keep one shared dark-ink-on-light rule. Dark mode is out of scope for this pass.

---

## (c) Motion spec

References behind the numbers (all checked this session unless noted):
- 3D button measured values: rest `translateY(-4px)` front / shadow `+2px`; hover rise to `-6px` over 250 ms with `cubic-bezier(.3,.7,.4,1.5)`; **press to `-2px` in 34 ms**; release back over 600 ms `cubic-bezier(.3,.7,.4,1)` ([Josh Comeau](https://www.joshwcomeau.com/animation/3d-button/)). Animating `transform` on separate layers instead of `box-shadow` or `border` is advised there for cost.
- Mascot timing table already in the repo: breathing 1 cycle per 3 s at 1-2 px; blink 100 ms close, 50 ms hold, 100 ms open every 3-5 s; overshoot 5-10% then settle at about 65% of the previous bounce; secondary action lags 50-100 ms; easing `cubic-bezier(.4,0,.2,1)` standard, `(0,0,.2,1)` entering, `(.4,0,1,1)` exiting (`.claude/skills/lottie-motion/SKILL.md`, which cites Material).
- Default control transitions 140-220 ms; avoid endless decorative loops unless they show status; stagger small groups only ([emilkowalski-motion skill text](https://raw.githubusercontent.com/nexu-io/open-design/main/skills/emilkowalski-motion/SKILL.md)).
- Reduced motion: WCAG 2.3.3 (AAA) requires interaction-triggered motion can be turned off, and names `prefers-reduced-motion` as a technique ([WCAG 2.2 Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)). Touch target minimum is 24 CSS px at AA ([2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)); Android says 48 dp ([Android accessibility](https://developer.android.com/design/ui/mobile/guides/foundations/accessibility)); our child rule is 64 px (prior research).
- Duolingo-side facts to respect: motion pulls the eye, so one moving thing at a time ([Duolingo blog](https://blog.duolingo.com/shape-language-duolingos-art-style/)).

Tokens:

```css
:root {
  --e-std:  cubic-bezier(.4, 0, .2, 1);
  --e-in:   cubic-bezier(0, 0, .2, 1);      /* things arriving */
  --e-out:  cubic-bezier(.4, 0, 1, 1);      /* things leaving */
  --e-pop:  cubic-bezier(.3, .7, .4, 1.5);  /* overshoot, from Comeau's hover curve */
  --t-press: 80ms; --t-fast: 160ms; --t-base: 220ms; --t-slow: 400ms;
}
```

Note: Comeau's active press is 34 ms, which is below the 100 ms feedback threshold for "instant", but on a phone a 34 ms CSS transition is only one or two frames, so we use 80 ms to make the movement visible to a small child.

| # | Interaction | Track A animation | Duration / easing | Track B | Reduced-motion fallback |
|---|---|---|---|---|---|
| 1 | **Button press** (all `.btn`, option picks, speaker) | Layered button: edge span stays; face `translateY(-5px)` at rest, `0` pressed; edge shadow shrinks to 0 with it. Light haptic tick if available. | Down 80 ms `--e-std`; release 250 ms `--e-pop`. Only `transform`. | Same, 2 px depth, release 160 ms `--e-std`, no overshoot. | Keep the depth change (it is feedback, not decoration) but set release to 0 ms, no overshoot. |
| 2 | **"Tap me" hint** (the one next action) | Sun button breathes: scale 1 to 1.05 and back, plus a 2-ring halo outline pulse. Starts after 4 s of no input; stops on first touch. Tilo points at it if narrating. | 1.2 s loop, `--e-std`, max 3 loops then rest 6 s, repeat. | A 2 px outline blink twice, no scale. | Static 3 px `--tap` outline, no loop. |
| 3 | **Tilo idle** | Breathing on the stage wrapper: scale 1 to 1.012/1.022. Blink swap every 3-5 s (random): 100/50/100 ms. Every 9-12 s one ear flick or weight shift: rotate 4 degrees and back. Never two at once. | Breath 3 s sinusoidal; blink 250 ms total; ear flick 400 ms `--e-std`. | none (no mascot) | Still pose; blink only (a 250 ms eye swap is not movement). No breath, no flick. |
| 4 | **Tilo arrives / leaves a screen** | Pops up from the screen corner: `translateY(24px)` to `0` with 8% overshoot, then waves once (the existing `wave`, 2 half-swings). Leaves by sinking 24 px and fading. | In 450 ms `--e-pop`; out 200 ms `--e-out`. | none | Fade only, 120 ms. |
| 5 | **Tilo speaks** | Mouth swap flap sequence (existing `FLAP`) at about 140 ms per frame while audio plays; small head bob of 2 px on each stressed syllable; bubble fades in 160 ms. | Flap 140 ms/frame; bubble 160 ms `--e-in`. | none | Still open mouth while the voice talks (already coded in `tilo.js`). |
| 6 | **Correct answer** | (1) Chosen card scales 1 to 1.06 and lifts 4 px, border turns `--good`, check icon pops in (scale 0 to 1.2 to 1). (2) 5-7 sparkle dots burst from the card, drift up 28 px and fade. (3) Tilo switches to the celebrating pose, one hop of 10 px, arms up. (4) Rising two-note chime, then Tilo says the sound again ("sss"). Whole thing 900 ms, then auto-advance. | Card 350 ms `--e-pop`; sparkles 600 ms `--e-in`, staggered 40 ms; hop 360 ms; advance after 900 ms. | Green border and check pop only (scale 0.9 to 1, 160 ms); text "Yes". No sparkles. | Border and check appear at once (opacity 160 ms); sparkles removed; Tilo swaps pose with no hop. Chime stays. |
| 7 | **Wrong answer ("oops")** | Card does one gentle side shake: 4 px, 2 swings. Tint turns `--oops-tint`, thin `--oops` border (not red fill). Tilo takes the thinking pose and tilts head 5 degrees. Soft low "hmm" sound, never a buzzer. After the second miss on the same item the right card gets the hint glow. Never subtract anything from the child. | Shake 300 ms `--e-std` (reuses the existing `nope` keyframe); tilt 400 ms; hint glow starts 600 ms after the second miss. | Same shake at 2 px, text "Not this one. Listen again." | No shake: border colour change and Tilo pose swap only; "hmm" sound stays. |
| 8 | **Screen transition (forward)** | New screen slides in 24 px from the right while fading in; old one fades out 40% of the way. Shared header (home button, progress bar) does not move. | 220 ms `--e-in`; old out 160 ms `--e-out`. | Same without the slide: 160 ms cross-fade only. | 120 ms cross-fade, no translation. |
| 9 | **Screen transition (back / home)** | Mirror: new screen slides in from the left, 24 px. | 180 ms `--e-in`. | 160 ms cross-fade. | 120 ms cross-fade. |
| 10 | **Progress bar fill** | Fill grows by `transform: scaleX` to the new value; at the leading edge a 10 px highlight dot rides along; on each new segment the bar bumps (scale Y 1 to 1.12 to 1). Tilo's face never covers the bar. | Grow 400 ms `--e-std`; bump 200 ms `--e-pop`. | Fill only, no bump or dot. | Jump to the new value in one 120 ms step. |
| 11 | **Unlock (node, level, sticker)** | Lock icon wobbles (3 degrees, 2 swings, 300 ms), then pops off: scale 1 to 1.25 then 0 with 20 degree turn and fade (250 ms). Node fill changes from `--locked-fill` to its band colour, node scales 0.8 to 1.1 to 1 and a halo ring grows 1 to 1.6 and fades. Tilo cheers (pose + hop). New sticker lands in the village with the existing `grow` keyframe. | Wobble 300 ms; pop 250 ms; node 600 ms `--e-pop`; ring 700 ms `--e-in`. Total under 1.2 s. | Lock fades out (160 ms), node colour fades in (240 ms), "Unlocked" text line. | No wobble, ring or scale: lock and fill swap with a 160 ms fade. Chime stays. |
| 12 | **Sitting complete** | Short celebration under 2.5 s: 3 stars fill one by one (scale 0 to 1.3 to 1 each, 250 ms apart, a rising note per star). Tilo celebrating with two hops. 20-24 paper confetti pieces in the Tilo palette fall for 1.8 s. Words-learned counter counts up. A big primary button "Go on" rises in last. Tap anywhere skips to the end state. | Stars 250 ms each `--e-pop`; hops 360 ms; confetti 1.8 s linear-ish with random drift; counter 600 ms. | Check mark, score text, count-up over 400 ms, no confetti. | Static starburst badge with the same stars drawn already filled; no confetti; no count-up animation; chime and Tilo voice remain. |
| 13 | **Level complete** (mastery check passed) | Everything in #12 plus the next level's node unlocks in the same moment (#11), and Tilo holds the celebrating pose for 1.5 s. Maximum 4 s, always skippable by tap. | As above, 4 s cap. | Same as #12, plus a plain "Level N done. Level N+1 is open." line. | As #12. |
| 14 | **Card / list entrance on home** | Lesson cards fade and rise 12 px, staggered 50 ms, first 5 only; later cards appear instantly. | 220 ms `--e-in`. | Fade only. | No stagger, instant. |

Global rules:
- Animate `transform` and `opacity` only. Never `top`, `left`, `width`, `height`, and avoid animating `box-shadow` (Comeau).
- At most **one** attention-grabbing loop on screen at a time (the tap-me hint). Tilo's idle is subtle enough to not count.
- Every animation has a sound twin and a non-colour twin (icon or word) so nothing depends on seeing motion or colour.
- Keep the global `@media (prefers-reduced-motion: reduce)` guard, but fix its blunt form (`* { animation: none !important; transition: none !important }`): it also removes the colour-change feedback. Replace with the per-row fallbacks above: keep opacity and colour changes at 120 ms, remove movement and loops.
- Add an **in-app "calm motion" switch** behind the parent gate. Many Android phones in this market do not have the OS setting turned on, and a sensitive child or parent should not depend on it. (Our own recommendation; no source needed.)
- Frame budget: all of the above is CSS or one small canvas for confetti; no Lottie is needed for Tilo because Tilo is a set of pose images with a CSS-driven stage (`tilo.js`). Lottie becomes worth it only if we draw a full-body walking or dancing Tilo; if so use the `lottie-motion` skill's rules (rest at least 40% of the loop).

---

## (d) Onboarding spec

Principles from the research:
1. The parent does the typing; the child only taps ([Common Sense on Duolingo ABC](https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read), Lingokids, Reading Eggs, above).
2. A pre-reader cannot read "Who is reading?". Today the question is spoken but the cards are plain text. Make every screen **voice-first with a picture answer**.
3. The sourced apps put an account, trial or email before the first lesson (Lingokids, ABCmouse, Reading Eggs, TYMTR since 2024). Sound Out has no account, so the first sound lesson starts inside 60 s. That is the differentiator.
4. Fewer questions. Duolingo ABC lists about 11 steps; HOMER's own case study says it simplified after seeing too many elements per screen. We target **4 screens before the first sound, 0 typed words**.
5. Never ask the child something they can fail. The first interaction is a guaranteed success.

### Track A: pre-reader, nothing typed, everything spoken (target: first correct answer by 0:40, mini-lesson done by 1:00)

| Screen | Time | What the child sees | What the child hears | Child action | Notes |
|---|---|---|---|---|---|
| **A0 Splash** | 0:00-0:02 | `--paper` background. Tilo peeks up from the bottom edge, then waves once. App name small and quiet. | Soft three-note jingle, then "Hi!" in Tilo's voice. | none (auto-advances at 2 s, or tap) | Tilo arrives per motion row 4. |
| **A1 Who is here?** | 0:02-0:10 | Two large picture cards, 64 px+ targets: a child's face and an adult's face. A small sun "tap me" ring pulses on the child card after 4 s. Tilo stays in the corner and points at the cards. | "I'm Tilo! Who is playing? Tap the little one, or tap the big one." (spoken, replayable by tapping Tilo or the ear button.) | Tap one card. | Keeps today's `onboarding.js` logic (profile = track A or B) but with face art, not just a grey figure, and with Tilo pointing. The grown-up card goes to Track B (section below), no gate needed because it only changes mode, not settings. |
| **A2 Pick a friend (optional, 8 s, skippable)** | 0:10-0:18 | Six round animal faces in a 3x2 grid (offline SVG: capybara cub, frog, owl, bunny, fox, duckling), each a different `--band-*` background. A big "skip" arrow that is a picture (a hand waving "later"), not text. | "Which one is you? Tap your friend." On each tap the animal says a sound ("ribbit") and Tilo smiles. | Tap one animal, or the skip arrow. | Costs: 6 SVGs in the existing style, stored in the same IndexedDB `profiles` row as `avatar`. Duolingo ABC, Khan Kids, TYMTR and Prodigy all give the child a character choice, so it is the expected beat. **No name is typed by the child.** The parent can set a name later in the gated settings (Duolingo ABC has the parent type the name too). Home shows the avatar in the header. |
| **A3 First-sound mini-lesson** | 0:18-1:00 | The existing first-sound game, but made un-failable and short: 3 rounds, 2 choices each. Round 1 picture = sun, choices /s/ and /m/ (speaker cards, big). Progress bar at top with 3 dots. | Tilo: "Listen. Sss. Sun starts with sss! Which one says sss?" Each speaker card plays its sound on tap, then the "This one" button picks it. | Tap a speaker, tap "This one". | Round 1 has a built-in **free nudge**: if no tap in 5 s the right card glows (hint) and Tilo repeats. A wrong pick in round 1 shows the oops animation (row 7) and the right card glows at once; it still counts as a finish so the child never leaves round 1 unrewarded. Round 2-3: 3 choices as today. Voice instructions only, no text needed. Whole path is about 42 s for a 4-5 year old at 3 rounds. |
| **A4 First celebration** | 1:00-1:10 | Motion row 12: 3 stars, confetti, Tilo hops. First sticker, "a seed", lands in the village. | "You did it! You found sss, mmm and ttt! Here is your first sticker." | Tap "Go on" (the sun button). | The first sticker doubles as the village's starting piece. |
| **A5 Home** | 1:10 | Level 1 with its node pulsing sun. Tilo in corner. | "Tap the glowing one to play again, any time." | Tap the node. | The home screen shows no unlock yet. |

Parent gate (where it lives):
- **Not in the first run.** Nothing the child can reach in A0-A5 spends money, links out or changes settings, and the app is offline with no ads or accounts (per `store/review/04` privacy screen). Gating the start would add friction for no safety gain (our judgement, not sourced); gating comes only at the **settings, privacy, language and "grown-up" corner**.
- Keep `gate.js`. Sourced norms: arithmetic "complete the equation" (ABCmouse), numbers typed as words (Duolingo ABC), birth year typed after two taps (Lingokids). A birth-year gate is weak for kids who know their parent's age; the multiplication gate we already have in digits is stronger than ABCmouse's "1 + 1". Recommended: keep the multiplication, add a **hold the corner icon for 2 seconds** to open it, so a toddler's random tap never reaches the sum. Use words for the digits aloud in the voice line only when the screen reader is on.
- Gate copy for the grown-up is plain text; Tilo is not shown on it.

### Track B: grown-up (no mascot, no spoken question needed, but voice available)

| Screen | What they see | What they hear / do | Notes |
|---|---|---|---|
| **B1 Who is reading?** | Same two cards as A1, same art, adult card highlighted on the second visit. | Optional spoken prompt via the ear button only (no auto-voice, less noise for an adult in a public place). | Same screen. The adult card sets Track B. |
| **B2 One-line promise (skippable)** | One screen, 3 plain lines: "Works with no internet. No account. Nothing leaves this phone." Primary button "Start". Link "Read the privacy page". | None. | Mirrors the existing privacy facts (`store/review/04`). One screen, not a carousel; no illustration. |
| **B3 Where to start (optional)** | Two buttons: "Start from the first sound" (default, primary) and "I know some letters, check me" (secondary, opens a 6-item placement of 1 minute that can be skipped at any time). | Plain voice for each item. | Reading Eggs and TYMTR both offer a starting-level pick; Reading Eggs' placement stops after 3 wrong answers and can be skipped ([guide](https://readingeggs.com.au/articles/getting-started-guide-parents/)). Make it optional so the default path still hits the first sound in under 60 s. If the placement is not built yet, ship B3 as the single "Start from the first sound" button. |
| **B4 First-sound mini-lesson** | Same 3 rounds as A3, no Tilo; a quiet progress line instead of a mascot. A wrong pick says "Not this one. Listen again." in text under the card. | Same sound prompts. | Track B colours and motion (rows 6-9, 12-14 with the B column). |
| **B5 Done** | "3 sounds learned" with a plain check mark and `--good` colour. A single line: "Next: Lesson 1.02, s a t". | none | Count-up 400 ms. No confetti. |

No name, avatar or email is asked of an adult either. If the adult wants a name, it is in settings behind no gate (an adult).

Timing check for the 60-second claim: A0 2 s + A1 8 s + A2 8 s (skippable) + A3 42 s = 60 s with the avatar step, 52 s without it. The first correct answer lands around 0:30. These are design targets; time them with a real child before calling the 60 s met.

---

## (e) Skills found

Searches run with `.claude/hooks/skillsmp_search.py` for: "kids app UI motion animation", "onboarding flow mobile", "duolingo style ui", "micro-interactions css", "lottie mascot animation", plus "mobile onboarding screen design UX", "animation principles easing spring web ui", "children app accessibility reduced motion", "mascot character animation rive". The first query returned no relevant result. Licence is read from the GitHub licence API for the repo; where a skill file itself states none, that is noted. Nothing was installed.

### Top 3 external skills

**1. `emilkowalski-motion`** (nexu-io/open-design, ★98.5K). Repo licence **Apache-2.0** (GitHub API); the SKILL.md itself states no licence and cites the upstream [emilkowal.ski/skill](https://emilkowal.ski/skill). Source: `skills/emilkowalski-motion/SKILL.md`.
- **What it says:** add motion only to an existing interface; pick the fewest motion moments (entry reveal, hover/active feedback, state changes); animate `transform` and `opacity`, never layout properties; one motion language, no mixed easings; reduced-motion fallbacks for automatic motion; "140-220 ms for most controls"; stagger only small groups; avoid endless decorative loops and noisy particles.
- **Useful?** Yes, as a review checklist that matches our global rules in section (c) almost exactly. It is thin: no easing curves, no kids' feedback patterns, no mascot guidance, and it demands a "design system" and two craft skills (`animation-discipline`, `accessibility-baseline`) that are not in our repo, so it will not run as designed. Use it as a read-only reference, not an installed dependency.

**2. `ui-ux-pro-max`** (nextlevelbuilder/ui-ux-pro-max-skill, ★131K). Licence **MIT** (GitHub API); not restated in SKILL.md.
- **What it says:** a searchable local database (79 styles, 192 product palettes, 74 font pairings, 119 UX guidelines, 17 GSAP presets, 22 stacks). Run `--design-system` for new work, `--domain` for one concern, `--stack` for implementation. Rules: 44x44 px touch targets with 8 px+ spacing (marked critical), contrast 4.5:1, semantic colour tokens, base 16 px type at 1.5 line-height, no "One duration for every transition", no missing reduced-motion. No millisecond values.
- **Useful?** Partly. Its checks agree with ours, but its adult-web defaults (44 px targets, 16 px text) are below our child numbers (64 px), it never mentions kids' apps, and its Python search tooling would need setup. Good for a generic palette/type sanity check on Track B; not a source of child-specific rules.

**3. `lottie-bodymovin`** (calesthio/OpenMontage, ★63.9K). Repo licence **AGPL-3.0** (GitHub API); SKILL.md states none. AGPL on a skill's text is a flag: copying its code snippets into a closed-source app would need a legal read first.
- **What it says:** Disney's 12 principles applied to Lottie exported from After Effects, with `lottie-react` snippets: anticipation 0-10 frame wind-up, 10-40 action, 40-50 settle with a 200 ms gap; follow-through offsets of 2-4 frames; exaggeration to 120-150% scale with overshoot amp 15, freq 3, decay 5; speed 0.5 / 1 / 2; 24 / 30 / 60 fps.
- **Useful?** Only if we later draw a fully animated Tilo in After Effects. It assumes AE expressions survive export (unverified) and React. It overlaps and is weaker than our own local `lottie-motion` skill for our python-lottie workflow. Skip.

Also seen: `affaan-m/motion-patterns` (ECC; React `motion/react` button/stagger/page transitions; no durations stated, defers to a `motion-foundations` skill; repo licence not checked) is React-only and Sound Out's app is vanilla JS, so not usable as written. `Manavarya09/designlang-tokens` (MIT) is a Duolingo.com token extract with only 3 colour tokens (primary `#d7ffb8`, white, black), one 2 px radius and no motion, so it is useless here.

### Local skills (already installed)

| Skill | Verdict for Sound Out |
|---|---|
| `lottie-motion` (`.claude/skills/lottie-motion/`) | **Use** the timing table (breathing, blink, anticipation, overshoot, easing) as the source for Tilo; it already holds the numbers in section (c). Only needed if Tilo moves beyond poses plus CSS. |
| `frontend-design` (plugin, `claude-plugins-official/frontend-design`) | **Use** at the start of the implementation pass to avoid templated results. It is generic, with no kids' rules, so pair it with this file. |
| `hairline` | **Skip.** Isometric line-art figures that follow the cursor; adult dashboard style, no touch-first child value. Possible calm empty-state art for Track B only; not needed. |
| `thinking-orbs` | **Skip** for Track A (Tilo is the "thinking" signal). Possible neutral "listening" indicator for Track B when voice input is added; not needed now. |

### Recommendation

Do **not** install any external skill. The three external ones either duplicate what we have (emilkowalski-motion, lottie-bodymovin), target adult web (ui-ux-pro-max), or carry a licence flag (AGPL). The right toolkit for the implementation pass is:
1. This file as the spec.
2. `frontend-design` for the visual build.
3. `lottie-motion` only if Tilo is redrawn as a rig.
4. `emilkowalski-motion` text as a one-page review checklist after the build (read, not install).
5. For visual check afterwards, regenerate `store/review/*.webp` and run a separate critic before showing Kamal each round, as in `feedback_critic_before_showing`.

---

## Open items and honesty notes

- No millisecond value in section (c) comes from a kids' app. They are our spec, anchored to Comeau's measured button, Material-style easing in `lottie-motion`, and WCAG. Timings should be tested with real children on the lowest-end Android phone before they are fixed.
- Duolingo's secondary and neutral hexes were read from a search summary of the official colour page; the page itself redirected when fetched. The four core hexes are confirmed by a second site. All other apps' hexes are third-party or absent.
- Install buckets and ratings differ between Apple, Google and trackers (Duolingo ABC is 4.2 on iOS from 3.8K and 3.9 on Play from 23.6K). Use them for rank order only.
- The timing target of 60 seconds (section d) is arithmetic from the screen plan, not a measured run.
- `18_emotional_design_talk.md` is a summary supplied by Kamal and was not re-checked against the video.
- Not researched: Toca Boca (Prodigy was used instead because its onboarding asks the child for a name, grade and avatar).
- Track A avatar art (six animals) does not exist yet; the avatar step is optional and costs six SVGs.
