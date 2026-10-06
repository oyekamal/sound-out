# Critic round 5: claims auditor (plan-v5.md)

Scope: plan-v5.md read in full (9,499 words) against research-01..06, DESIGN.md, placement-test.md, all 108 lesson files (counted: 14/14/18/16/16/16/14), L1.02, L1.03 and L1.13 in full, bar/*.json, the Urdu repo files the plan cites, and the Capacitor source in the Urdu repo's node_modules. I recomputed every sum, binomial and unit conversion in 3.3, 3.4, 4.1, 4.4, 4.5, 6.2 and 8 with python.

## Prior-round classes: status

| Class | Status |
|---|---|
| Heart-word count 69 = 24+29+16 | GONE. Recounted from lesson headers (L1 24, L2 29 "last 3 of Level 2's 29", L3 "16 Level 3 heart words"). |
| Phoneme counts 47 / 53 clips | GONE as a count (53 = 47 + 6 final stops). No course source for "47"; it is the team's own figure, labelled as such nowhere. Left as is. |
| Placement quotes | GONE. "90% (14+)" with "≈14/16", H-T 50/94/132, Passage C to Level 6, /ɒ/ or /ɑ/ (line 264), the 10+10+15 A-C minutes (L1.02 sittings A ~10, B ~10, C ~15) all match. |
| Gate-vs-recall | GONE. 11(.6^10)(.4)+.6^11 = 3.0%; research-03 §8 does set "recall >= 60%". |
| "Measured" vs budget | GONE. Line 6 says no budget is measured, and I found none stated as measured. |
| Pseudoword derivation | PARTLY BACK. 710 reproduces (55 x 2 x 5 + 160) but the recording table prices 1,040 made-up clips (below). |
| Size-table bounds | GONE. 23.2-34.8 / 9.55-14.35 / 32.7-49.1 MB, 37-53 / 40-63 / 69-103 / 72-113 all reproduce. Reader L4 2,582-4,383 clips and 10.4-17.2 MB reproduce; L5 1,686-2,613 and 12.1-18.4 MB reproduce. |
| Recording hours at one rate | GONE. 6,670/150 = 44.5, 10,190/150 = 67.9, /120 = 55.6-84.9. Every instance now gives both rates. |
| Kokoro pack MB | GONE (see size row). |
| Chance-pass scope | MOSTLY GONE. 0.003%, 1.1%, 0.1%, 0.6%, 18.8%, 3.1%, 10.9%, 70%, 32%, 1.97%, 14.5%, 3.5%, 26% all reproduce. The 1.9% does not hold without an unstated assumption (below). |
| Night-one minutes | GONE. 18 min is a labelled target; course A-C is 35 tutor minutes. §0 line 15 states "about 18 minutes" without the word "target". |
| D15 accent | GONE as worded ("the app's choice"). One residue below (L1.05 mouth cue). |
| Sprite memory vs §4.1 | NOT GONE. The arithmetic reproduces (15.8 + 17.3 + 2.9 = 36.0 MB) but the premise contradicts §4.1 (below). |
| 3.0 KB/clip unlabelled | GONE. Labelled "assumed, conservative"; research-02 1.77 KB and research-05 2.5 KB both cited correctly. |
| Whistle pseudoword overstatement | GONE. Line 41 now says blim/strag only, vop/fraim failed, chote only with biasing at 0.46; all match research-06. |

## Findings

| Section | Claim | What the source says | Severity |
|---|---|---|---|
| 4.1 Tier-2 lines; 7.2 glosses; C10 | "Tier-2 lines (L&T lessons x 2 x 3)" = 162 / 102 / 90 clips; helper glosses "59 lessons x (passage + 2 Tier-2 words)" = 177; "from the course's own Tier-2 bullets" | Only L1 has two Tier-2 words per lesson (bullet list, "Tier-2 words:", 2 each in L1.02-L1.13). L2, L3, L4 carry one: "Tier-2 word: generous", "precise", "fulfillment", "functional" (grep: one hit per lesson in L2-L4; L2.13 has none). DESIGN §3 line 82 says "1-2 Tier-2 words". Real count is about 28 + 13 + 17 + 15 = 73 words, not 118. Corrected: Tier-2 clips about 123 / 51 / 45; gloss lines about 132, not 177; helper pack about 235-265 lines, not 310 | overstated (basis wrong; cost errs high) |
| 4.1 / 7.2 / C10 helper pack | "~310 voiced lines + ~30 notes" | The §7.2 table gives 60 + 40 + 177 = 277 lines plus 20-40 notes. 310 only appears if notes are counted as lines (277 + 30 = 307), but §4.1 and C10 then say "+ ~30 notes" again | arithmetic |
| 6.2 audio memory | "step sprites of 20-30 s ... holding every clip the step can play"; peak ~36 MB; risk row "Low" | Plan's own §4.1: a word clip is 3.0 KB = 1.0 s at 3 KB/s. A Check step plays 10 items x 4 spoken options = 40 s before the dictation, repairs or any fresh retry item, and §4.1 sizes the option pool at 3 sets per check (120 option clips = ~120 s = 11.5 MB decoded). A Check sprite is 4x the 30 s assumed; three such sprites in the LRU break 36 MB. "~370-550 step sprites" is total audio / 30 and ignores this. 36 MB holds only for non-check steps | arithmetic (internal contradiction) |
| 3.4 chance table, D40 | "~1.9% with the axis rule" = 10.9% x 17.2% | Both factors reproduce (176/1024 = 17.2%). The product assumes the 10 extra axis picks are independent of the gate. They are not: mini checks are themselves gated at 4/5, so conditional on passing them a blind learner's vowel-axis accuracy is already inflated. If the axis picks include the gate's own 5 vowel items, P(gate and axis>=7/10) is ~6.4% unconditional, not 1.9%. The rule says ">= 8 per axis", not 10: at n = 8 the bar is 6/8, 14.5%, product 1.6%; at n = 12, 9/12, 7.3%, 0.8%. The 1.9% is correct only for n = 10 fully independent picks, stated nowhere | unverified-as-fact |
| D40 "~0.04% for checked twice" | placement ambiguous after "~1.9% with" | 1.9%^2 = 0.036% is the with-rule figure; without the rule twice is 1.2%. Reader cannot tell which | arithmetic |
| 4.1 made-up counts; C2 | C2 "710 made-up words"; table rows L0-L2 ~560, L3 ~300, L4 ~180 | 560 + 300 + 180 = 1,040 clips. 710 + the ~250 markdown words = 960. v4's own split (L1-L2 312 + 250; L3-L4 398) gives 480 for L3+L4 and the table has 480, but then the total is 80 higher than 960 (placement/level 80 double counted). C2 commissions 710 while the recording budget prices 1,040 | arithmetic |
| 4.1 option slots | L1-L2 "900-1,800 clips" from 2,832 slots at 30-60% | 2,832 x 0.3 = 850, x 0.6 = 1,699. L3 (556-1,112 vs 550-1,100) and L4 (475-950) are fine. L1-L2 is rounded up about 6% | arithmetic (small) |
| 0 / 10 D0a-alt | "10,400-16,300 clips"; "lead's ~10k, ~65 h = low end" | 6,670-10,190 + L4 without chunks (2,182-3,633) + L5 (1,690-2,610) = 10,540-16,430, about 1% off the stated range. 10,400 clips at 150/h is 69 h, not 65, so "lead's 65 h = low end" is 6% loose | arithmetic (small) |
| 4.5 weekly table | Total L0-L3 6,670-10,190 | Rows sum to 6,670-10,200 (3,940 + 2,990 + 2,840 + 430). Rounding | fine |
| 4.4 reviewer workload | Reader L4 ~960-1,650 clips | Not derivable from the stated rule ("100% of made-up words, made-up options and chunks; 10% of the rest"): made-up 180 + chunks 400-750 + 10% of rest (~150-250) = 730-1,180 before any option share; ~960-1,650 needs about half the options. The share is unstated. Human 3,000-4,630 reproduces | unverified-as-fact |
| 1.1 / bar table | Khan "parent email account", "age/performance path" | Not in research-01 or bar/Khan json (json only has Spanish read-to-me, which is cited). v4 credited "Common Sense via a round-1 critic fetch"; v5 dropped the credit, so it reads as sourced from the bar | fine-but-uncited |
| bar table, Learning Upgrade | "Adult track, same sequence: Yes, 3.2/5" | research-01: LU is the only multi-level adult-through-child app, 3.2/5 on justuseapp. "Same sequence" is not stated; the 3.2/5 is a rating in a feature cell | fine-but-uncited |
| bar table header "Read Along" | Home-language help "several languages" | True of Google Read Along (research-01). The bar/Read_Along_Kids_Books.json in the folder is a different app (Smart Kidz Club, 4.59, 1,857 ratings); the plan never says which | fine-but-uncited |
| 2 DESIGN rule 5 | "Tricky words mapped: E8" listed as rule 5 enforced | DESIGN rule 5: "Heart words, never flashcard drilling". Plan also stores `tricky` as a Leitner card kind and back-fills tricky words as "E8 review cards". No row says why that is not drilling | overstated |
| 2 DESIGN rule 12 | "Honest citations: no effect sizes in store or app | banned-claims grep" | DESIGN rule 12 is "research claims cite research/0X; nothing invented". The grep enforces store copy, not citations in the plan or course | overstated |
| 2 DESIGN rule 7 / 3.8 | Listen & Talk "questions answered by tapping one of 3 pictures" | Course questions are open oral inference ("How did Sam feel ... How do you know?", "Why do you think Mia's words helped"). Picture MCQ versions do not exist; the ~355 pictures (59 x 2 x 3 = 354) imply they will be authored, but no C-item commissions the questions themselves (C16 is Tier-2 only) and it is not marked as a departure from the course | unverified-as-fact |
| 7.1 D15 | "course names no accent" | Placement test line 264 accepts /ɒ/ or /ɑ/ (matches). L1.05 mouth cue is "rounds the lips slightly, unlike /a/'s flat-open shape", a British /ɒ/ description; a GA Sound Teacher's /ɑ/ is unrounded. C6 phonetician sign-off may cover it, but §7.1 says the course is neutral | unverified-as-fact |
| 7.2 wave 1 | Wave 1 includes Vietnamese; order "estimate" | research-04 §4.1 puts Vietnamese under "Later", and says the ranking is [memory]; Persian/Dari dropped. The plan's own caveat covers the order, not the swap | fine-but-uncited |
| 7.2 recipe | "Swan & Smith, Learner English" | Not in any research file. Background citation | fine-but-uncited |
| 6.3 Urdu repo | "`db.js:44` `fix()` coerces any track outside child|adult|heritage to child" | The behaviour is real, but `fix` is defined at db.js:58 and the profiles branch is line 61; line 44 is the `onversionchange` handler. `learner.js:41-43`, `backup.js` units cap 40, `voice_studio.py` :353 (547 lines) all verify | fine-but-uncited (wrong line) |
| 6.2 Capacitor | "`WebViewLocalServer.java:369-386` ignores `Range`" | Verified in the Urdu repo's node_modules (7.6.9): the Range branch sets 206 and Content-Range but returns the whole stream from byte 0. `downloadFile` "deprecated since 7.1.0" verified in @capacitor/filesystem 7.1.8 docs | fine |
| 4.1 shell size | Shell 14-18 MB with ~355 pictures, ~40 icons | research-05 §? says the shell is about 8 MB. The extra 6-10 MB for pictures is asserted; no per-picture size is given | unverified-as-fact (labelled estimate) |
| 0 D0b | "10-15 working days" CTC; KWS cannot return yes/unsure/no | critics-round-2-engineer.md line 15 has the 10-15 days. Verified | fine |
| 0 D0a evidence | Gemini judge heard /m/ /p/ not /s/ /ʃ/ /θ/ /æ/; "the judge may be at fault; no human listened" | research-02 §5 says exactly this and "I cannot tell without a human listening". Verified | fine |
| 4.1 per-clip KB | research-02 1.77 KB; research-05 2.5 KB; word 3.0 KB | 1,772 bytes (10 trimmed words) and 2.5 KB (0.6 s) verified; 3.0 is the assumption | fine |
| 4.2 | pip hang, espeakng-loader abort, vop -> "vob" | research-02 §3 and §5 verified | fine |
| 4.5 licences | "clause 3.2 is the lead's reading, research-02 gives none" | research-02 gives no clause number; verified | fine |
| 5 Whistle | 16.9 MB, CPU, Apache-2.0, 8.9 s then 0.1-0.25 s, sat 0.63, pin 0.73, cake -> Take 0.83, chote 0.46, 97% / 1.5 s go bar, 30 x 3 x 2 | All match research-06. Spike plan there is weeks 1-2; plan puts it in week 9 (a deliberate change) | fine |
| 3.3 / 3.6 / 12 sittings | 366 / 183 / 92-122; L1.04 = 18, L1.06 = 30, L1.08 = 42 (adult 21); "random 26%" | All reproduce (6/lesson and 3/lesson from research-04 §2.2). L1.08 at 42 days = exactly six weeks, as stated | fine |
| 3.7 / 2 bars | L1.02 9/11; L1.03-L1.13 10/11; "≥4/5 19 times in 10 L1 lessons"; L5 5/8, 6/9; L5.16 no bar | 19 hits in 10 files; L1.02 9/11 and the others 10/11 verified by grep; L5.01-10 5/8, L5.11-15 6/9 | fine |
| 2 table counts | Blend 13/13/17/14, L&T 14/13/17/15, Track B 12/13/17/15 | L&T heading counts reproduce (14/13/17/15 = 59). Raw `grep -il` gives L2 Track B 14 and L3 L&T 18 because the mastery-check lessons mention both; the plan's numbers need a heading-level grep, which the table does not say | fine-but-uncited |
| 3.4 L1.02 check | "course has real at, sat, as, at, sat (repeats), 5 made-up, 1 dictation; app uses 3 + 5 + 3" | L1.02 file: real "at, sat, as, at, sat", pseudo "tas, sta, ast, sas, att", dictated "at". Matches; marked as app change. L1.03-L1.13 are 5 + 5 + 1 (L1.03, L1.10, L1.13 read in full) | fine |
| bar numbers | Khan 4.80 / 131,337 / 201 MiB; ABC 4.25 / 3,810 / 212; TYM 4.47 / 29,802 / 96 / $8.99 | 210,646,016 B = 200.9 MiB; 221,852,672 = 211.6; 100,752,384 = 96.1; ratings and price match | fine |
| 4.4 handover test | SE 0.25, bound 0.34 below mean, pass within ~0.16 | 1/sqrt(16) x 1.341 = 0.335; -0.5 + 0.34 = -0.16. Reproduces | fine |
| 8 cut list | A1 <= 1,450 clips 10-12 h; A2 390-575; A3 145-240; A4 140-184; cut 12 12-19 h / 15-24 h | All reproduce from the §4.1 counts (A2 from 205 targets + 3 foils at 30-60%) | fine |
| 7.3 | COPPA 22 April 2026, closed test >= 12 x 14 days | research-04 §5 verified | fine |

## Claims checked and failed

About 130 numeric or sourced claims checked. 12 rows above fail or need a caveat: 6 arithmetic, 3 overstated, 4 unverified-as-fact, 5 fine-but-uncited (some overlap). No fabrication found. Every "(research-0X §Y)" citation resolves to a section that says what the plan says (research-02 §5, research-03 §6/§7/§8, research-04 §5 and D6, research-05 counts, research-06). Every course quote I tested matches, including L1.13 ("the letter is called 'bee'; it says /b/" appears in §3 as "bee, dee, pee, cue"; the plan's E24 line is a paraphrase, and L1.13 is a single 25-30 min sitting with no heart words, as the plan treats it). The L1.13 letter-names claim is fine.

## Verdict

**NO on handing to Kamal as-is.** Nothing is invented and the headline decisions (D0a clips and hours at both rates, D16, sizes) reproduce. But three figures that a decision rests on do not hold as written, and each is a one-paragraph fix: the Tier-2 basis, the sprite memory premise, and the 1.9% axis-rule assumption. Fix those, reconcile the made-up count (710 vs 1,040) and the 277-vs-310 line count, then it can go.

## Three worst offenders

1. **Tier-2 "x 2 x 3" (4.1, 7.2, C10).** The course gives two Tier-2 words only in Level 1; L2-L4 give one. The clip counts (162/102/90), the 177 glosses and the "310 lines" all rest on the wrong count, and 310 does not even equal the table's 277.
2. **Audio memory ~36 MB (6.2).** The plan's own clip sizes make one Check step about 40 s for a single set and about 120 s with the three option sets §4.1 prices, against "20-30 s step sprites holding every clip the step can play". The "Low" risk row inherits that.
3. **~1.9% with the axis rule (3.4, D40).** It is 10.9% x 17.2% and silently assumes ten extra independent vowel-axis picks. The rule says >= 8, the picks are selected by earlier 4/5 gates, and using the gate's own items gives about 6%. The D40 "accept" decision is made on this number.
