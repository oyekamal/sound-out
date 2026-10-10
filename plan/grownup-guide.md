# Grown-up guide: where it lives and how a parent reaches it

Content: `content/guide.json` (about 1,775 words, ste_lint: 0 errors). A builder wires it in later. This doc covers placement, UX and the bar.

## 1. Where it lives

Today the "For grown-ups" button on Home (`home.js`) opens the sum gate (`grownup.js`) and then the Privacy screen (`privacy.js`), which holds one setting (no time limit on the Level 1 check) and the privacy text. The guide goes in the same area.

- After the sum, the screen becomes "For grown-ups" with three rows: **Grown-up guide** (first, large), **Settings**, **Privacy**. Today's Privacy screen becomes the third row. No new gate: one sum covers all three.
- The guide is a single screen of collapsible sections, in the order of `guide.json`.
- One-time card: after the first profile is made, and only when the grown-up opens "For grown-ups" for the first time, show "Helping a child? Read the 1-minute guide" above the three rows. It opens the guide with only "Start here" expanded. A close button hides it for good (a `guideSeen` setting, same store as `noTimeLimit`). Never show it on the child's screen, and never speak it.
- Track B profiles see the card text "New to reading? Read the 1-minute guide for helpers." The content is the same.

## 2. Screen layout

- Collapsible sections (`details`/`summary`), one open at a time, "Start here" open by default. Section titles are the headings in `guide.json`.
- Readable at 360 px wide: one column, 16 px side gutters, no horizontal scroll, the sound table turns into stacked cards (sound in a large chip, then "say it like", then the tip).
- Body text 18 px or larger, line height 1.5, 44 px minimum tap targets, high contrast, works with the app's reduced-motion and text-size settings.
- "Start here" shows its seven tips as a plain list with no scrolling needed on a 360 x 640 screen. Target: readable in 60 seconds (about 100 words).
- Levels: one accordion item per level, with three labelled lines (Learns, Try off-screen, Ready to move on). Show the learner's current level first.
- Back button returns to the "For grown-ups" list. No links out. The page works offline.
- No audio, no Tilo, no pictures in v1 of the guide. Do not speak it; the learner must not be pulled into the grown-up area.

## 3. What the guide says, and where each idea comes from

| Guide idea | Source in our own files |
|---|---|
| Sounds, not letter names; names as labels | plan-v6 section 3.4 (E2 "sound as the tool, name as the label"); course L1.13 |
| Short, clean sounds | course L1.02 ("practise saying /s/ crisply"); mouth cues in L1.02, L1.04, L1.07, L1.09, L1.11 |
| Blend by sliding | course L1.02 tutor notes (slide a finger under the letters); guide-tutors-parents.md |
| Short daily sittings, one new sound | plan-v6 section 3.3 (one new sound per sitting, budgets) |
| Next-day review | plan-v6 section 3.3 (next-day retrieval) |
| Let the learner tap; no guessing; no picture before the word | DESIGN.md rule 1; plan-v6 section 2 rule 1 |
| Say "check it again", not "wrong"; praise process | guide-tutors-parents.md (error routine, praise the process) |
| Tricky words | DESIGN.md rule 5 |
| Grown-up learner dignity | guide-tutors-parents.md ("Keeping an adult learner's dignity"); DESIGN.md rule 6 |
| Group size, small group | guide-tutors-parents.md (cites research/03 section 5) |
| What the grown-up screen shows | `home.js` (days practised, village, stickers; Track B words and badges) |

## 4. The bar: what the four named products offer a parent

Findings come from fetches and searches on 2026-10-10. None of the four has a single teaching guide inside the app. Most "guides" are setup pages.

| Product | What a parent gets | Length and tone |
|---|---|---|
| Khan Academy Kids | Help Center pages on accounts, parental controls, devices; a parent dashboard on the main Khan Academy site; Common Sense Media is where the teaching advice appears (sit together, point out sounds in names and signs) | Short FAQ answers, neutral support tone. No in-app teaching guide found. |
| Reading Eggs | "Getting Started Guide for Parents": account, dashboard, starting lessons, tracking, changing levels. The support page itself is about 100 words and has no teaching tips. | Upbeat, brief, mostly setup. |
| Teach Your Monster to Read | Teacher pages: parent letter, password cards, take-home slips, shared progress stats. | Roughly 700 words, warm and promotional, aimed at teachers, little on how to help a child read. |
| Duolingo ABC | Setup (name, microphone), a linear path. No official parent FAQ found; advice comes from Common Sense Media (ask what letters they learned, read aloud, set screen rules). | Brief and neutral from third parties. |

**What we do better.** A parent with one minute gets seven tips (the "Start here" list), example phrases for each moment, and a no-printout activity for every level. None of the four gives example phrases or per-level checks. We also say what to do when a child guesses, which the sources do not cover.

**What they do that we do not.** Teach Your Monster prints a parent letter and password cards, and Khan Kids and Reading Eggs have an online parent dashboard that shares progress across devices. Our app is offline and has no account, by design, so the home screen is the whole progress view. See "Open items" below.

## 5. Open items for the builder and for Kamal

- The grown-up view in plan-v6 section 3.9 (per-child list of learned sounds, "play and compare", "I can help" card, "why no pictures beside words?" card) is not built yet. The guide's teacher section describes only the home screen. Update it when the view ships.
- A printable one-page parent letter (like Teach Your Monster's) is not in v1. It could be made from "Start here" and shared as a PDF.
- Level 5 to 7 entries are written but only Levels 1 to 4 are in the app today (`LEVEL_NAME` in `home.js`). Show only the levels the installed version has.
- Child sitting lengths (8 minutes or less) and grown-up lengths (10 to 15 minutes) are plan budgets, not measured times. Check against spike S3 before release.
- The advice not to add "uh" to a sound is standard phonics practice, but our own course files do not state it as a rule. The only support is "say /s/ crisply" in L1.02. Review it, or have the audio team confirm.
- Translate through the helper-pack route (plan-v6 section 7.2), not by hand. The guide is English-only in v1.

## Sources

- Khan Academy support, Parent Quick Start Guide: https://support.khanacademy.org/hc/articles/360040168512-Parent-Quick-Start-Guide
- Khan Academy Kids contact and support page: https://www.khanacademy.org/kids/contact-us
- Common Sense Media, Khan Academy Kids review: https://www.commonsensemedia.org/app-reviews/khan-academy-kids
- Reading Eggs support, parent guide article: https://support.readingeggs.com/support/solutions/articles/266672-is-there-a-guide-to-help-parents-get-started-with-reading-eggs-
- Teach Your Monster to Read, sharing games with parents: https://www.teachyourmonster.org/teachers/sharing-our-games-with-parents-and-guardians/
- Teach Your Monster Help Center, sharing player information: https://help.teachyourmonster.org/en/articles/5698285-sharing-player-information-with-parents
- Common Sense Media, Duolingo ABC review: https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read
- Our own: plan/plan-v6.md sections 2, 3.3, 3.4, 3.9; english-reading-course/DESIGN.md; course/level-0/guide-tutors-parents.md; course/level-1 lessons.
