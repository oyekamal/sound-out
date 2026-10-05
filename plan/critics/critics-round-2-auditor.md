# Critics round 2: claims auditor on plan-v2.md

Scope: all 898 lines of plan-v2.md against research-01..05, DESIGN.md, placement-test.md, the 108 lesson files (counted by me with grep and heading scans), bar/*.json, critics-round-1-*.md, decisions.tsv. Nothing was run on a device; this is a document audit.

## Did the round-1 error classes go away?

- Heart words: gone. DESIGN.md schedules give L1 24, L2 29, L3 16 = 69 unique-by-slot. Plan says 69 (24/29/16). Correct.
- Phoneme count: gone. 24 consonants + 20 vowels = 44, +3 combination clips = 47, x2 takes = 94. Counted from the plan's own lists, adds up.
- Placement-test quotes: mostly gone. The tester script quote is verbatim; "a missing data point is honest" is verbatim; Block A 26 / B 5 / C 7, 24/26, 14/16, 6/8, HT 50/94/132, FK 1.7/4.7/6.8, DIBELS 3 s rules all match. One new misreading found (Stage 1 targets, below).
- Pass-bar counts: gone. 19 occurrences of >=4/5 in 10 L1 lessons (L1.01, L1.03-09, L1.11, L1.12) is exact; L1.02 9/11, L1.03-L1.13 10/11, L5 5/8 and 6/9, L6 "4/5 or more", L3 "90%?" all verified. Level lesson counts 14/14/18/16/16/16/14 = 108 verified; 7 mastery-check.md files verified; 0 Listen & Talk in all 46 L5-L7 verified.
- "Measured" budgets: mostly honest now. 1.77 KB is labelled n=10 (research-02: 1,772 B over 10 words). Everything else is labelled estimate/unverified/budget. The remaining slips are listed in the table.
- New classes appeared: one misread source (Stage 1), two unreconciled-arithmetic problems that bear on the central promise (gate vs recall; guessing odds), a research-03 recommendation reversed without saying so, and a handful of small counts.

## Findings table

| Section | Claim | What the source says | Severity |
|---|---|---|---|
| 3.5 + 5.5 (gate vs recall) | `secure` needs bar met on verifier `clear_yes`; acceptable verifier recall floor is >=60% (research-03 §8) | Not reconciled. At 60% recall a fully correct child gets 10-of-11 clear_yes with p=0.03, 9-of-11 (L1.02 bar) p=0.12, all 5 real-word items p=0.08. At 80% recall: 0.32 / 0.62 / 0.33. Add the second-sitting re-check and the "no adult needed" promise is mostly unreachable at the stated floor. Items pass through repair and re-presentation, but the plan never says repaired items count toward the bar. | arithmetic (central) |
| 3.4 Stage 1 | "Correct is judged by the verifier (targets are known real words, e.g. 'boy')" | "boy" is never a target. It is part of the prompt ("Say cowboy, now say it without boy"; answer "cow"). Answers include non-words: "ig" (big minus /b/), "ap" (map minus /m/), "han" (hand minus /d/). The verifier-with-real-word-targets design does not fit those items. | fabricated (misread) |
| 0 / 2.3 / 5.3 / research-03 | "Fixed: machine never promotes mastery alone"; verifier-credited heart words; machine `secure` unlocks next lesson | research-03 §6: mastery gate "Never auto-promote on machine alone", "gate needs adult confirm"; heart words "No" for machines, "Judge" is human; §0.3 "build it as a witness, not a judge". The plan departs (lead-call 1 in decisions.tsv) and the sentence is true only because `secure` is a different label. The departure from research-03 is not stated in the plan. | overstated |
| 5.7 E6c | "Chance is 25% per item, so >=9/10 by guessing is negligible" | Same section says matching first and last letter leaves two candidates, so the working chance for a learner who hears only the final sound is 50%. P(>=9/10 at 50%) = 1.1%, not 0.003%. Still low per check, but the stated 25% contradicts the plan's own step 2. | arithmetic |
| 12.2 vs 10 D21 vs 8 wk4 | Teacher agreement on "5 solo adults and 5 children"; pilot is "2 kids + 1 teen + 3 adults" | 10 learners needed, 6 recruited. The agreement test cannot be run inside the pilot as written. | arithmetic |
| 0 table | Duolingo ABC "Runs to critical reading: No ('very simple short stories')" | No such phrase in research-01 or the parent critic. research-01 says "stops at simple stories" / "ends at short stories". Scare quotes around a phrase nobody wrote. | fabricated (quote) |
| 3.2 | "L2.6's 20 initial blends" | DESIGN.md and L2.06 heading list 21 (st sp sn sm sl sw sk sc / bl cl fl gl pl / br cr dr fr gr pr tr / tw = 8+5+7+1). | arithmetic |
| 4.1 pseudoword derivation | "L1.03-L4 lesson checks: 61 x 2 x 5 = 610" | L1.03-L4.16 is 60 files (108 - 2 - 46). And four of those are mastery-check lessons (L1.14, L2.14, L3.18, L4.16) with no 5-pseudo check. 610 is not derived from anything countable. Total ~770 inherits this. | arithmetic |
| 4.1 table total | "~12,700-16,800 clips", "~80-93 MB" | Summing the plan's own rows: 12,642-16,407 clips; 79.7-92.0 MB. Low end fine. High end overstated by ~390 clips / 1 MB. | arithmetic |
| 4.1 L0 row | "Level 0 ~190 + 3 forms, ~0.8 MB" | research-05: 187 quoted words. 190 x 2.5 KB = 0.48 MB. Remaining 0.3 MB is unexplained (3 forms?). | unverified-as-fact |
| 4.1 pack row | "L3-L4 / L5 / L6 / L7 ~13 / 12 / 18 / 11 (~54), computed" | research-05: 12.5 / 12 / 18 / 11 (53.5); its own table gives L3+L4 = 11.4 plus extras. 13 matches neither. Sum 54 only by rounding up. | arithmetic (minor) |
| 4.1 install and "whole app" | 54-94 MB install; 108-148 with packs | Arithmetic correct (8+26+15+5 = 54; 8+26+20+40 = 94). But base audio 26 and packs 54 are both lower-bound word counts; at the plan's own 9,238 ceiling total audio is ~92 MB, so "whole app" understates by up to ~12 MB. Plan says "lower bounds" for the packs only. | overstated (minor) |
| 0 / 4.1 | Compares our "54-94 MB" to competitors' 212/201/96 | Competitor figures are bytes/1024^2 (221,852,672 B = 211.6 MiB), ours are KB x 1000. Plan says "not like-for-like" but for a different reason. | fine-but-uncited |
| 2.1 table | Level 3 "Listen & Talk 18" | 17 files have the heading; L3.18 mentions it only in a Tutor-notes sentence. Same table counts L3 Blend by heading (17). Level 2 "Track B 14" likewise counts L2.14's prose mention (13 real blocks). | overstated (off by 1) |
| 5.5 | "`clear_yes` precision ... >=60 items per child per class"; "p50 <500 ms" cited to research-03 §8 | research-03 §8 says ">=60 items with both kids and both conditions" (not per child). p50 <500 ms comes from research-05 §6.7, not research-03. "0 failures" on 20 relaunches is added. | overstated (citation drift) |
| 5.2 | targetSdk 36 "makes 16 KB alignment an upload gate" | research-05 only says the 16 KB rule changes once native libs are added. The Play-policy claim is background knowledge, unlabelled. | unverified-as-fact |
| 0 intro paragraph | "neither tested engine produced a clean isolated /s/ or /theta/" | research-02 §5: Gemini Flash mis-heard them; "may be the judge as much as the model", nobody has listened. Plan does add "unverified by a human", so this is labelled, but the first clause reads as a finding. | overstated (labelled) |
| 4.6 | 44 phonemes incl. /ar or er ir/ r-controlled as four "phonemes" and both /a/ (ɑ) and /ɔː/ | Counts add up. Whether the course teaches /ɔː/ vs /ɑ/ as distinct in General American (cot/caught merger) is not checked against gpc data; plan defers to week-2 reconciliation. | fine-but-uncited |
| 3.3 E-table / 3.4 | Pseudoword freshness: "Three fresh sets cannot exist for L1.02" | Plausible (course uses 5 pseudo from s, a, t) but not enumerated. | fine-but-uncited |
| 10 | Decision numbering | D20 absent, no note (D12 has one). | fine-but-uncited |
| 4.7 | "Lessac clause 3.2, read by the lead" | consistent with decisions.tsv line 6 (lead read it) and research-02 §2. | fine |
| 7.5 | Closed test 12 testers x 14 days, IARC Education, COPPA 22 Apr 2026 | research-05 / research-04 (Urdu checklist, JD Supra). Cited and correct. | fine |
| 4.7 | OpenMoji CC BY-SA 4.0, Chatterbox "Perth watermark" | OpenMoji: no source in the folder (flagged "check"). Perth: research-02 §1 says it. | fine-but-uncited / fine |

## Checked and passed (selection)

Store figures (Khan 4.80/131,337, ABC 4.25/3,810/2023-08-02, TYM 4.47/29,802/$8.99, Reading Eggs 4.70/7,369, sizes 212/201/96 MiB); "over 700 hands-on lessons"; Common Sense "No option to skip ahead", 127 units; Learning Upgrade $4.99-$59.99, 3.2/5; "children can progress by guessing" (justuseapp, via research-01); sentences 2,224 and 1,322 (sums of research-05 rows); 5,763 / 9,238 / 3,546; 2.5 KB x counts = 14.4 / 23.1 MB; 1,640 slow clips = L1+L2 words 1,066+575; 69 blending demos (23 lessons x 3); 360-648 Tier-2 clips; base audio 26.0; packs 54; 449/2702/391/313 reuse split; Capacitor 7.6, minSdk 24, 150/300 MB RSS; DIBELS 35/57/76; HT table; wave 1/2 languages; 84/42 sittings per level; archetype first-month sitting arithmetic (30/5=L1.02-L1.06, 20/3 etc.); 14 l1_tags x 5 families; C11 ~46 sessions; block-coverage rows for L1, L4-L7 (including Word work 15 in L5 because L5.16 lacks it, Write 13 in L7 because L7.11 lacks it); pseudoword set of L1.02 (tas, ast, sta, sas, att); Af_heart 1.2-4.4% above 8 kHz; vop to "vob"; af_heart child sentence 2/5.

## Counts

Claims checked: about 120 (numbers, citations, quotes, arithmetic, labels). Failed or materially off: 13 table rows with severity above "fine" (3 fabricated/misread, 7 arithmetic, 5 overstated or citation drift, 1 unverified-as-fact, some rows combine). Labels: every "unverified"/"estimate" I tested held; no unlabelled measurement found beyond the 5.2 Play-policy line.

## Verdict: hand to Kamal as-is?

NO. Not because of hidden fabrication (the round-1 classes are largely fixed and the labelling is now honest) but because the headline promise, "a child progresses without any English-reading adult", rests on a gate whose numbers do not work together, and because one input description (Stage 1 targets) is wrong. Both are quick to fix before it goes out: state the gate rule (how many repaired items count, or what recall is required for a 10/11 bar), fix Stage 1, and say plainly that `secure` departs from research-03 §6.

## Three worst offenders

1. Gate vs recall (3.5, 5.5): verifier recall floor of 60% makes the `secure` path reachable for a correct reader only about 3% of the time at 10/11 (12% at 9/11), so "no adult needed" is not supported by the plan's own thresholds.
2. Stage 1 verifier targets (3.4): says "known real words, e.g. boy"; "boy" is a prompt word, and the file's answers include non-words (ig, ap, han).
3. Unflagged reversal of research-03 §6 (0, 2.3, 5.3): "machine never promotes mastery alone" is true only by renaming the state `secure`; the research says never auto-promote the gate on machine alone and keeps heart words human-judged. Close runners-up: E6c "25% chance" contradicted by its own step 2, and the teacher-agreement test needing 10 learners from a 6-person pilot.
