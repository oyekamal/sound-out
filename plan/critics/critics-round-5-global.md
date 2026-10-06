# Critics round 5: global (Jakarta, Ohio, Mexico City)

Read: plan-v5.md (all 586 lines), store/NAME-ASO.md, critics-round-4-global.md. Verdict: the Urdu lock is gone from the text. What remains is an English-first Android app whose first week still assumes English comprehension and a Play account, piloted through Kamal's own contacts.

## Week-one verdicts (A = Sound Out v5, B = what they have)

1. **Jakarta rider, reads Indonesian: B (Duolingo) stays.** He reads Latin script, yet v5 gives him a print-concepts module (§3.6), one sound per sitting (~183 sittings to L4, §1), no Indonesian on night one (Budi's row says "skip"), and English-only Listen & Talk he cannot answer; Duolingo speaks Indonesian and tells him what words mean.
2. **Ohio mother, 5-year-old: B (Khan Kids + ABC) stays.** Her family is likely on an iPad, v5 has no App Store listing and a Home Screen web app untested on any Apple device (D24, §6.3), and a child who knows letter names gets a silent mascot and a year to L4.
3. **Mexico City grandmother, iPhone: B (Duolingo) stays.** She cannot find the app (Play-only, §7.3), cannot read its English listing, and would need Safari's "Add to Home Screen" for a web app whose storage Safari may evict.

## The single biggest remaining failure

**A learner with no English never learns what anything means, and the plan counts that as success.** §3.8 steps 1 to 3 (passage, spoken questions, "simple English definition") are English-only; the pack gloss comes after the questions and covers 177 lines for L1 to L4. Rule 7 is enforced by a coverage test, so it passes while the learner answers by chance (1 in 3). The pilot bar ("≥80% on English questions, with and without a pack") is unreachable for Budi or the grandmother without a pack. "Works in English alone" is verified only to "first sound in 90 s".

## Round-4 assumptions

Gone: 1 first-launch Urdu, 2 E6d spoken line, 5 Urdu tips in core, 8 sizes (37 to 53 MB base), 11 ASO (NAME-ASO already has no Urdu keyword; the §7.3 "note" is stale). Partly: 3 check intro (D1), 6 personas (D4), 7 grown-up view (English text for a no-English parent), 12 helper path (still behind a written-sum gate). Stuck: 4 gloss (biggest gap), 9 validation and accent (D7), 10 languages (D8).

## Probes

**Unmimeable by Pebble demos:** "Some are made-up words. Sound them out." (a shrug cannot say "no such word, pick the sound anyway"); "Read it to yourself" (silently, no helper); "Which starts with /s/?" (first sound, before sounds are taught); "Let's finish tomorrow"; "Help in your language?"; the idea of tricky words.

**"Just English"** is a text button with no specified icon, on a screen whose question is spoken in English. A non-reader cannot tell which tap means "no help", and the background download hides a wrong tap.

## Defects

**D1. §3.2/§3.7 instructions.** Says: ≤60 lines, each mimed. Global-first: name the six lines above as unmimeable and teach each by three worked items before the first judged one. Verify: week-3 no-English test (10 adults + 10 children) runs a full check, not just the first sound, in PK, BR, ID, **MX and a non-Latin-script country**, scored on whether they say the words were real.

**D2. §3.1 step 3.** Says: names in native script, big "Just English". Global-first: chips with a 3-second spoken greeting bundled in core (~15 KB each), "no help" as a crossed speech-bubble icon, nothing downloads without a second tap. Verify: 10 non-readers choose language-or-none on paper with no instruction.

**D3. §7.2 packs x10.** Says: ~310 lines + ~30 notes, 2 to 3 speaker h + 6 to 8 reviewer h, 2 to 3 MB. Global-first: ten languages is 20 to 30 speaker hours, 60 to 80 reviewer hours, ten field checks with adults who read the language but not English, ten English-teacher approvals of notes, ten voices recorded to a 48 kHz no-AGC spec on their own hardware; D38 prices three. Andika (§4.5) lacks Arabic, Devanagari, Bengali and Nastaliq glyphs, so 2 to 3 MB omits fonts. Verify: cost one non-Latin pack (Hindi) end to end, with its font, before wave 1 is promised.

**D4. §12 pilot.** Says: 8 children + 6 adults, 4 countries, remote, Play internal test. Global-first: n=2 per cell cannot show "every child advances unaided"; US children can only be Android; no Mexico, Spanish or iPad cell; proxy validity needs a GA teacher judging accented children over WhatsApp video. Verify: add a Spanish cell and an iPad cell (after D5); the blind teacher first rates 20 accent-only clips.

**D5. §6.3 iOS web-only.** Says: Home Screen PWA, eviction warning, native iOS v2; PWA is cut #13. Global-first: drop iOS from the v1 claim, or test an iPhone for Web Audio muted by the ringer switch, Opus decode on older Safari, cache quota, an 8-day gap (all unverified). Verify: add an iPhone to D24.

**D6. §7.3/NAME-ASO locales.** Says: localized listings for ur, pt-BR, id, then wave 1. Global-first: es-419 users see "Learn to read English with phonics" and no Spanish search term; listing translation and keyword work appear in no §8 week or D38. Verify: write es-419 and id listings from native search data, check the Play render on a Spanish-set device.

**D7. §3.4 vowel validation, §7.1 accent.** Says: 9+3 listeners (Urdu, Portuguese, Indonesian L1); General American only. Global-first: Spanish L1, the largest ESL group, merges /æ ʌ ɑ/, so vowel-axis misses read as reading misses; add Spanish. GA with American spelling is a default for Kenya, Nigeria, India, UK, Australia, and should say so. Verify: vowel-axis pass rate per L1; comfort scores from 5 local-accent listeners per region.

**D8. §7.2 "Which", §3.6, residual Pakistan.** Says: launch ur + pt-BR + id "because the pilot sites need them"; "Punjabi and Pashto speakers get Urdu"; D9 covers only the Urdu voice; one adult path for every adult. Global-first: the launch set follows Kamal's contacts, not Play reach (Spanish, Hindi wait); a Pakistan-only limitation sits in a global plan; a Latin-literate adult gets the pre-literate print module and one-sound sittings. Verify: add an "I read another language in Latin letters" tile that skips print concepts; test with Budi-type and grandmother-type users; label Hasbrouck-Tindal US WCPM norms as native-speaker norms.

## Bottom line

B wins for all three: Budi has no meaning path, Emma's mother has no iOS app, the grandmother cannot find or install anything. No test yet proves a person with no English gets through a full week.
