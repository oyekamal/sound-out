# v6 changes: finding → change → section → how to verify

Sources: decisions.tsv rows (13)–(17), the coordinator's v6 brief, and critics-round-5-{teacher, parent-adult, global, engineer, audio, auditor}.md. plan-v6.md is 8,606 words by `wc -w`. After v6 the plan gauntlet pauses (decision 17); "verify" now usually means a week-1 spike (S1–S9, plan §0) rather than another critic round.

## Lead decisions

| # | Finding | Change | § | Verify |
|---|---|---|---|---|
| 13a | The app is a fresh codebase; v5 still claimed "copied from urdu-reading-course" and patched Urdu bugs (engineer r5's biggest gap) | Every copy claim and every Urdu file/line reference removed (`db.js`, `learner.js`, `backup.js`, `voice_studio.py`, `WebViewLocalServer` line ref); §6.3 data layer designed fresh; Urdu repo is reference only | §0, §6, Appendix | `grep -n "db.js\|learner.js\|copied" plan-v6.md` returns only the "no code is copied" line |
| 13b | Weeks 2–5 not re-estimated for from-scratch modules | Module table: 13 modules, 8.0 engineer-weeks over weeks 1–8, staffing named (build agent full-time + Kamal ~1 h/day) | §8 | Table sums to 8.0 |
| 13c | What moves to v1.1 as a result | L5 practice (E16, E17, E19, L5 pack), E14, E15, E18, E20, E21, stroke-scored tracing, placement Stages 1 and 4, judge's card and "mastered" marking, WCPM | §0, §3.4, §8 | v1 exercise list = 17 |
| 14a | Binge with no retention (teacher r5's biggest gap) | New sounds capped per calendar day (2 for Track A and B-new; 3 for B-Latin, so the lead's "3 per sitting" for B-Latin still holds); "learned" needs a next-day retrieval; Leitner and re-checks in calendar days; free play, Stories and review unlimited | §3.3, §3.7 | Reducer test: a perfect bot over 10 hours gets ≤2 new sounds and no `checked` that day; S2 |
| 14b | Letter names too late; capitals never taught | Meet card shows lowercase + capital, sound as the tool, name as the label, from L1.02; letter-name bingo from L1.02; unlockables linted to taught shapes | §3.4, §3.5, §3.9 | E2 spec; unlockables lint |
| 14c | One-syllable L4 words had no repair ("coin") | Repairs defined per word type: CVC = successive blending; one syllable with a digraph or vowel team = onset + rime ("c · oin") in the exercise's one voice + tiles; multi-syllable = chunks. Row 14 said "human Sound Teacher onset+rime"; decision 16 supersedes it with one voice | §3.4 | Every L2–L4 word has a repair plan (lint) |
| 15a | No-English learners never learn meaning (global r5's biggest gap) | Picturable core vocabulary: the picture appears as meaning **after** the word is decoded and picked (E25); abstract Tier-2 words get the pack gloss **before** the questions, or are deferred and counted as not taught | §3.8, §2 rule 1 | DOM test: no picture before a correct pick; grown-up view lists deferred words |
| 15b | Latin-literate adults forced to the pre-literate pace | Track B split: **B-Latin** (no print module, 3 sounds per sitting, names day 1, "sat" ≤12 min) and **B-new** (print module, 1 sound per sitting, "as" ≤15 min); chosen with two tiles at onboarding | §1, §3.1, §3.6 | S3 stopwatch |
| 15c | iOS web-only and untested | iOS = the web app, tested on a borrowed iPhone in the pilot (S9); AAC fallback if Opus fails; claim dropped if the test fails | §6.4, D24 | S9 record |
| 15d | Spanish missing; launch set followed the owner's contacts | Spanish added to the vowel panel (12 non-native + 3 native) and the intelligibility panel; launch packs by Play reach: es, pt-BR, hi, id, ar, ur; Mexico added to the pilot and S7 | §3.4, §4.4, §7.2, D8, D21 | Panel composition; pilot countries |
| 15e | Packs ×N unpriced; fonts missing | Per-language price incl. audition, review, notes, field check, localised listing, and a font subset for non-Latin scripts; six packs ≈ 84–126 person-hours + 12–18 speaker hours | §7.2, D38 | Recompute: 3 × (13–19) + 3 × (15–23) person-hours |
| 16a | Two voices still join at L4 (UI lines, placement, Stories, tap-read: audio r5 D1, engineer r5 defect 2) | **One voice end to end.** D0 = (a) Kokoro-only with sounds and chunks sliced from Kokoro's own word renders, or (b) one human for everything; decided by spike S1 with Kamal listening to `app/public/listen.html` plus 8 listeners at ≥90% | §0, §4 | S1 result |
| 16b | (b) ranges | v1 L0–L4 ≈ 7,980–12,480 clips = 53–83 h at 150/h, 66–104 h at 120/h; L5 later +1,690–2,610 clips (+11–17 h / +14–22 h) | §0, §4.2, §10 | §4.1 table totals ÷150 and ÷120 |
| 16c | §4 must be parallel, with one decision | §4.2 is a two-column (a)/(b) table; D0 is the single decision | §4.2, §10 | — |
| 16d | Rules written for two voices | Trace test → voice-id check (one voice id across core and level packs); voice table removed; handover test removed; drift gate kept only in (b); pack voice plays only on its own card outside exercises | §4.4 | Build fails on a second voice id |
| 16e | Early-lesson pools too small for grids (engineer r5 defects 3–4) | Early check (L1.02–L1.04) = sound → letter items + 3-option blend-and-pick, same lexicality, labelled "early check". Counts stated: L1.03 ≈ 11 made-up strings (7 grid-able), 22 real (16); L1.04 ≈ 33 (23); "at" and "as" have one neighbour. The build fails when need > pool. No centring claim; random-tapper figures 0.34% (L1.02) and 0.036% (L1.03–04) | §3.4 | `gen_options.py` per-lesson report (S4) |
| 17 | Diminishing returns from critic rounds | §0 states the pause and lists spikes S1–S9, each with the open questions it answers, plus Kamal's playtest | §0, D43 | — |

## Auditor r5

| Finding | Change | § |
|---|---|---|
| Tier-2 basis ×2 everywhere (should be 73) | 73 words (auditor's per-lesson grep: L1 two per lesson, L2–L4 one: ≈28 + 13 + 17 + 15), method stated; Tier-2 clips 123/51/45; glosses 132 | §2, §4.1, §7.2 |
| 310 vs 277 pack lines | Pack = 60 + 40 + 132 = **232 lines** + 20–40 notes, counted separately everywhere | §4.1, §7.2, C10 |
| Step-sprite premise fails for 3-set checks | Two option sets per check (course set + one generated re-check set), on different days; check step holds one set (≤60 s); clip store with no duplication; memory ~30 MB recomputed | §4.1, §6.2 |
| 1.9% axis-rule figure | Stated as **~1.6% to ~6%**, with the independence assumption named; Monte-Carlo in S5; 12-item checks if >3% (D40); "checked twice" placement fixed (0.03–0.4%, with the rule) | §3.4, D40 |
| Made-up 710 vs 1,040 | Reconciled at ~720 targets (280 course + 275 generated + 160 level/placement), split 330/210/180; C2 commissions ~435 generated + review of all | §4.1, C2 |
| L1–L2 option rounding (900 vs 850) | Recomputed from slots: 1,968 × 30–60% = 590–1,180 | §4.1 |
| D0a-alt range and "65 h" | Replaced by D0 (b) ranges computed from the table | §0 |
| Reader reviewer share unstated | One-voice workload re-summed (first pass, Q2 second pass, re-review, agreement set) ≈ 14–22 h | §4.4 |
| `db.js:44` (actually :58) | All Urdu code references removed (13a) | §6 |
| Khan Kids facts uncredited | Footnote: Common Sense via critic fetches in rounds 1 and 5 | §0 bar |
| Learning Upgrade cell; Read Along ambiguity | "Multi-level adult-to-child (research-01; 3.2/5 justuseapp)"; Read Along named as Google's app, not the bar JSON | §0 bar |
| Rule 5 enforcement overstated | Tricky words reviewed only as E8 maps; the Leitner `tricky` card opens an E8 item; lint forbids a bare-word flash screen | §2 |
| Rule 12 enforcement overstated | Source tag on every number in the plan, store copy and in-app "why" cards; the claims auditor checks them before release; grep only for store banned claims | §2, §6.1 |
| Listen & Talk picture questions not marked as a departure | Marked as a departure; commissioned as C19 | §3.8, §11 |
| L1.05 British /ɒ/ mouth cue vs "course names no accent" | GA as the "app's default"; C6 adapts the L1.05 cue to /ɑ/ as a signed-off departure | §7.1, C6 |
| Shell size asserted | ~8 MB from research-05 + 6–10 MB pictures (assumed ~17–28 KB each) | §4.1 |
| Swan & Smith uncited; Vietnamese wave placement | Kept "a contrastive reference" without the title; Vietnamese stays in the later group, order labelled an estimate | §7.2 |

## Parent-adult r5

| Finding | Change | § |
|---|---|---|
| Biggest stop: one missed mini check ends the adult's night; bar stated two ways | Mini-check bar stated once: 4/5 on 5 items, the course's own early bar; a first miss gets one more try with a different item set, then "tomorrow" with free play open | §3.3 |
| Night one 18 min | B-Latin ≤12 min ("sat"), B-new ≤15 min ("as"), both budgets; fallback for B-new | §3.6, D35 |
| PIN before the first word | PIN offered after the first word | §3.1, D28 |
| Child-coded adult entry | No mascot on "Who is reading?"; no Pebble, village, stickers or animal icons anywhere in Track B; audit target 0 child-coded assets | §3.1, §3.9, §6.4 |
| Language question and the mobile-data wall | Pack prompt = icon + MB number + a spoken line in the pack's own language (pre-recorded greeting in core); no Wi-Fi default for packs under 5 MB; S8 times it on data | §3.1, §0 S8 |
| Grown-up view unusable for a parent with no English | Play-and-compare: app plays a sound, the child repeats, the parent taps "same / not sure"; labelled encouragement, not a test; never feeds a gate | §3.9 |
| 8-year-old defeats the sum gate | Gate admitted to keep out young children only; deleting a profile also needs the PIN where an adult exists | §3.1 |
| Listen & Talk is noise for a no-English child | 15a + comprehension scored only with a pack or "Just English"; muted-audio picture-match test | §3.8 |

## Global r5

| Finding | Change | § |
|---|---|---|
| Unmimeable instructions | Six listed (made-up words, read silently, "starts with", finish tomorrow, help in your language, tricky words), each with an icon, a demo before the first judged item, and an optional pack line; S7 runs a full check, not just the first sound, in ≥3 countries incl. Mexico and a non-Latin-script country | §3.2, §0 S7 |
| "Just English" undefined | A flag-free globe icon with a spoken English line; language chips play a greeting in their own language; a second tap is needed to download | §3.1 |
| Latin-literate adults at the pre-literate pace | 15b | §3.6 |
| Localised listings unpriced | A localised listing per launch-pack language, 2–3 h each, in the per-pack price (C20) | §7.2, §7.3 |
| GA presented as neutral | "The app's default", named for Kenya, Nigeria, India, UK, Australia | §7.1 |
| Hasbrouck–Tindal norms | Labelled US native-speaker norms | §3.6 |
| Pilot n=2 per cell; no Spanish or iPhone | 10 children + 8 adults, MX added, borrowed iPhone; proxy rater first scores 20 accent-only clips | §12, D21 |
| Stale NAME-ASO note | Removed: NAME-ASO has no Urdu keyword (global r5) | §7.3 |

## Engineer r5

| Finding | Change | § |
|---|---|---|
| Step sprites over 30 s; duplication not counted | Clip store of concatenated Ogg streams + offset index, per-step manifests, no duplication; check steps ≤60 s with one option set; ~30 MB peak (~60 MB at 48 kHz) | §6.2 |
| Tap-read breaks the two-voice trace test | Moot under one voice | §4.4 |
| Early pools (L1.02 chains impossible; L1.03 ~11 strings) | 16e | §3.4 |
| Chunk pipeline unevidenced | Chunks are slices of the word render, judged in S1; (b) records or slices them | §4.2 |
| No slack for gate failures | Gate-failure table with cost and what absorbs it; week 9 holds one failure; a second triggers the cut list; Whistle and the handover test leave the schedule | §8 |
| Ed25519 on the Chrome 74 floor; Safari format | JS verification with `@noble/ed25519` (~5 KB gzip, estimate; BigInt needs Chrome 67+), unit-tested on a Chrome 74 WebView; AAC variant for Safari if S9 needs it. The floor is kept, so no device-share figure is needed | §6.4 |
| Whistle flavour isolation is fragile | Spike moved to a separate repo and app id; store CI checks the merged manifest and `unzip -l` of the AAB | §5 |
| 150 clips/h unsourced; take-picking unbudgeted | Both rates shown; (b) audition = two 90-min sessions in one day + one next day, reporting accepted clips/h; take-picking ~16–25k takes (estimate) | §4.2 |

## Audio r5

| Finding | Change | § |
|---|---|---|
| L4 join survives in UI, placement, Stories, Meet cards | One voice (16a) | §0, §4 |
| Chunks synthesised from IPA would be the wrong syllable | Chunks sliced from the word's own render with crossfades at zero crossings (the critic's fix) | §4.2 |
| Loudness rule contradictory; class means hide outliers | One measure (K-weighted active RMS, loudest 100 ms), ±1.5 dB per clip around class targets set by ear on the phone; LUFS path dropped; limiting reported and re-gained, not silently failed | §4.3 |
| Drift check weak | (b) only: sheet at open and close; pYIN F0, 1/3-octave spectrum, syllables/s, SNR, reverb; waiver needs a second sign-off; validated on a degraded copy | §4.4 |
| Stop selection on a phone speaker | (b): picked for burst/VOT cues, stated as such; (a): judged in S1 on Opus-decoded clips | §4.2 |
| Handover test population | Test removed (no handover) | §4.4 |
| Pack voice is a third voice; reviewer sum incomplete | Pack lines on their own card outside exercises; pack speakers auditioned by 5 listeners; reviewer workload re-summed ≈14–22 h | §4.4 |

## Teacher r5

| Finding | Change | § |
|---|---|---|
| Same-sitting signals only (biggest gap) | 14a | §3.3, §3.7 |
| Early checks mix lexicality; repeats are memory | Same lexicality always; an item that cannot get two same-lexicality options becomes a sound → letter item; repeats only on a different day | §3.4 |
| 1.9% joint assumption | Auditor row above | §3.4 |
| Repairs supply the whole word; L4 one-syllable gap | 14c; the retry is always a fresh item | §3.4 |
| Stories karaoke highlight; "attempt" undefined | Sentence-level highlight in read-to-me; an attempt = a pick or tile step; a decodable unlocks only after its lesson's pick | §3.5 |
| Letter names and capitals | 14b | §3.4 |
| Listen & Talk = picture matching | 15a + C19 + muted-audio test | §3.8 |

## Declined or partial, with reasons

| Finding | Status | Reason |
|---|---|---|
| Teacher r5: tile spelling as ≥ half of check items from L1.03 | Deferred | Changes the course's check composition; the dictation item stays. S5 data decides whether spelling items are needed |
| Teacher r5: text hidden in L1–L2 read-to-me | Partial | Lead decision 12 keeps visible text following the voice; v6 moves the highlight to sentence level, as the teacher asked |
| Teacher r5: for no-English learners, replace the L&T passage with picture-words | Partial | Lead decision 15 keeps the passage, adds picture-meaning after decoding, the pack gloss before the questions, and comprehension scored only with a pack or "Just English" |
| Global r5: native iOS App Store listing | Declined for v1 | Decision 15: iOS is the tested web app; native iOS is v2 |
| Global r5: a 3-second greeting as the only language cue for illiterate users | Adopted | Greeting chips in core (~15 KB each) |
| Parent r5: no locks at all, like Khan | Declined | Lead decision 12 keeps picture locks for sibling separation; the PIN now guards profile deletion |
| Audio r5 D6: handover test with per-group bars | Moot | No handover under one voice |
| Engineer r5: raise the WebView floor instead | Declined | The JS verification path works on Chrome 74 (to be unit-tested), so the floor stays |
| Coordinator: price fonts and listings per language | Adopted | §7.2 |
| decisions.tsv row 14, "human Sound Teacher onset+rime" | Superseded | Decision 16 (one voice); onset+rime is in whichever single voice D0 picks |
