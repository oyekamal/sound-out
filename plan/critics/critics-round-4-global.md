# Critics round 4: global (Recife, Jakarta, Ohio)

Read: plan-v4.md in full, store/NAME-ASO.md. Question: "for the whole world, not for Urdu speakers". Verdict: v4 is an Urdu app with an English course inside it.

## Week-one verdicts (A = Sound Out v4 as written, B = what they have)

1. **Recife father, 6-year-old, 2 GB Android: B stays.** Night one opens on "Who is reading?" spoken in Urdu then English (§3.1); neither he nor his daughter understands a word of it, Portuguese is not in wave 1 (§7: Hindi, Arabic, Spanish, Bengali), and the 44-59 MB install plus 29-44 MB packs buys him nothing he can navigate, while Duolingo ABC opens in his language.
2. **Jakarta rider, adult, reads Indonesian: B stays.** He taps "Me" and every instruction, check intro ("Some are made-up words...") and mother/grown-up explanation is Urdu or English audio he cannot parse; Indonesian is absent from every wave, so main Duolingo, which at least talks to him in Indonesian, wins the first week even though Sound Out's decoding path would suit a Bahasa reader better.
3. **Ohio mother, 5-year-old, native English: B stays.** She meets an Urdu-first launch line, Urdu tips on Meet cards, an Urdu-voiced "tonight, ask her" view, a year to reach L4 at one sitting a day (§1), no iOS (v2 in §8), and nothing Khan Kids lacks except no-account privacy, which does not outweigh Khan's 131k-rating polish.

## The single biggest Urdu-lock

**The "no English reader needed" promise is delivered entirely by recorded Urdu audio, and nothing in v4 makes that layer swappable.**
- Every instruction a non-reader needs (§3.1 first launch, §3.3 E6d step 1 "read it to yourself", §3.6 the Show-what-you-know intro, §3.11 the mother's view) is a spoken line in "the UI language", and the only authored UI language is Urdu (C9: 300 UR lines, C10: 600 glosses, 900 lines, 5.4 MB).
- A pre-literate child or an adult who cannot read English has no other way in, so in any country without a recorded pack the first screen is a wall.
- §6.4 stores a `homeLang` field, but no section says what reads it.
- Adding Portuguese means a voice actor, a licence (D9-style), QA and a reviewer per language. The plan prices none of that.

## Every Urdu/Pakistan assumption (section / says / global-first)

1. **§3.1 first launch.** Says: "Who is reading?" spoken Urdu then English. Global: pick language first from device locale, using native-name chips and icon cards; with no pack, fall back to icons plus animation and English, never Urdu.
2. **§3.3 E6d flow.** Says: a spoken UI-language line says "read it to yourself". Global: a wordless ritual (eye, finger, ear icons) taught once by animation; speech optional.
3. **§3.6 check intro.** Says: an Urdu audio line explains made-up words. Global: a 10-second animated demo that works with no language; narration as a pack.
4. **§3.8 and C10 Listen & Talk.** Says: Urdu gloss gives context (step 1) and defines the Tier-2 word (step 4), about 600 lines, faded after two weeks. Global: English-only path is default (picture or simple English definition); home-language gloss is an optional helper pack keyed on `homeLang`.
5. **§3.3 E2 "Urdu tip", §2.3 rule 9.** Says: Urdu interference notes ship in the core. Global: notes are a pack per L1 attached to `l1_tags`; off for English-native; Portuguese, Indonesian and Spanish packs say different things (final vowels, th, short-i).
6. **§1.1, §12.2 personas and pilot.** Says: five Pakistani personas; Kamal's two kids; mothers who cannot read English; Urdu-only recruits. Global: add one persona each for Brazil, Indonesia, USA; pilot at least one site per market; mascot and village art (§3.4, sun, tent, apple tree, "the village") checked by those testers, with an art-skin option.
7. **§3.11 mother's view.** Says: Urdu audio and icons for a mother who cannot read English. Global: "grown-up view", gender-neutral, icons first, text and audio per pack; where the grown-up reads English it shows a text version with the same "ask her these 3 sounds".
8. **§4.1, §6.4, §7 sizes and download.** Says: 1 Mbit/s assumed (D36), "no rupee figures", 73-103 MB total, one universal APK. Global: show MB only, Wi-Fi-only default, a tiny English-only base (about 45 MB) with each language as a separate pack; confirm the Recife/Jakarta prepaid-data case at a lower assumed speed.
9. **§3.3, §6.6, §5 test listeners and accent.** Says: vowel contrasts validated by 5 "Urdu-only" listeners; Urdu-accented vowel merges "practice, never wrong"; Whistle child/accent unverified. Global: validate per L1 (Portuguese and Indonesian have their own merges: /ɪ/-/i/, /æ/-/ɛ/); native English listeners are the control group the plan never runs; GA fixed (D15) with no UK/Indian/Nigerian choice, so call it a default.
10. **§7 languages.** Says: v1 EN + UR; wave 1 Hindi, Arabic, Spanish, Bengali, Punjabi/Pashto get Urdu, "follows Play data". Global: Portuguese (Brazil), Indonesian, French and Swahili are bigger markets than Pashto; define a language-pack format (about 300 text lines, machine draft plus native review, audio only for pre-readers) so a wave is days, not a studio.
11. **NAME-ASO, §7 listing.** Says: keyword "Urdu to English reading", "English is the word Urdu/Hindi/Arabic-speaking adults search with", screenshots "EN + UR", Play title "Read English". Global: listings per market locale (pt-BR, id, en-US), en-US title that reads for natives ("Learn to Read: Sound Out"), no Urdu keywords in the global listing.
12. **§0 and §1 promise.** Says: "no one who reads English has to help"; helper tools behind PIN. Global: that is one audience; for an English-reading parent the helper path should be the default, visible, and not gated like a threat.

## What the native-English Ohio child needs that v4 does not give

- **A zero-home-language path.** The plan never states one. Steps in §3.8 (gloss first), §3.3 E2 (Urdu tip), §3.6 (Urdu intro) and §3.11 have no defined behaviour when `homeLang` is empty; "English UI lines ~200" exist but no flow uses them alone.
- **English Tier-2 meaning.** Vocabulary is explained only in Urdu, so an English child gets the word with no definition.
- **A faster start.** Quick-start is 5 items and stops after 2 misses; a 5-year-old who knows letter names but cannot blend starts at /s/ and does one sound per sitting (about 12 months to L4). Her oral English and comprehension need no repetition of L&T; letter names are also not taught at all (rule: letter-name answers are an error class), while the ABC-song world she lives in uses them.
- **iOS.** v1 is Android plus a PWA with "lessons may be cleared" (§6.4); iOS is v2. A US family is likely on iPad.
- **Evidence.** The pilot (§12.2) has zero native-English children, so E6d is never calibrated against the cleanest decoder, and the proxy check (§12.2) is not run on her.
- **A rest of the world.** Rule 1 (no picture beside an unread word) and a mascot that never speaks are right for the method; but nothing explains them to a parent who has Khan's talking animals as the baseline.

## Bottom line

For the three people, B wins in all three cases, and for the same reason: the first minute is in a language they do not have. Until the instruction layer is a pack and an English-only path exists, "for the whole world" is a roadmap line, not a feature.
