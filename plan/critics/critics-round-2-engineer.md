# Critic round 2, engineer: plan-v2.md

Checked against research-02/03/05, the Urdu `mobile/` code, lessons L1.02, L1.14, L3.05, L5.05, L6.05, L7.03 plus heading counts over all 108.

## Verdict: B

The 8-week build slips or ships with listening cut, because the week-2 verifier go/no-go cannot be decided on the data collected, the sherpa-onnx path it names probably does not give yes/unsure/no, and weeks 3-5 carry roughly 20 new exercise types plus placement, helper mode and two audio packs on one build agent.

## Biggest gap: the verifier is a research project scheduled as a spike

§5.1-5.2 promise "decode over a small vocabulary" and a margin-based `clear_yes/unsure/clear_no`. Neither candidate mode gives that. This is from my knowledge of sherpa-onnx and must be confirmed on day 1. The reports verify none of it (research-05 line 6: sizes "from memory"; research-02 §9: nothing tried on Android).

- **(a) Keyword spotting.** It is a detector with a per-keyword threshold and boost. It has no negative class and, as far as I know, returns no score, so there is no `clear_no`. The English KWS model is a ~3.3M-param zipformer trained on adult GigaSpeech, roughly 5-15 MB. Competitors as extra keywords give "which fired first", not a margin. Pseudowords are spelling strings, not phones.
- **(b) Transducer with hotwords.** This is biasing, not constraining. Boosting the target raises false accepts on `sit` for `sat`, the opposite of the ≥97% precision bar. The Kotlin API returns the best hypothesis, so §5.2(b)'s "n-best margin" needs JNI patching. A streaming zipformer-20M is 40-90 MB, 150-250 MB RSS.
- **What would work.** A CTC model run through onnxruntime directly, scoring target vs competitor token sequences with your own CTC forward pass (~100 lines of C++/Kotlin) and per-class calibration. My estimate is 10-15 working days before any kid data, not 6-10 days in a week that also holds the parser, IPA and voice audition.

Verification: day 1, run one KWS and one CTC model on the test phone over 20 near-miss pairs (`sat/sit/set`); report false-accept rate, RSS, ms.

## Defects

**1. Gold set cannot certify the thresholds, and the labeller is a confound (§5.5-5.6).**
- §5.5 demands ≥60 items per child per class and lower CI ≥92% at 97% precision. §5.6 supplies 40 real, 20 pseudo, 10 heart, 10 sentences, 20 isolated per child. Pseudo, heart and sentence classes cannot reach 60 per child; two children give n=1 per age band.
- Wilson lower bound for 48/48 is ~0.93 and one miss collapses it.
- Kamal, an Urdu-L1 speaker, is the primary labeller. /æ/ vs /ɛ/ and v/w are the contrasts in dispute; the GA reviewer (D23) never labels child speech.
- Fix: state required n per class; GA reviewer labels the near-miss subset; plan on no-go as default. Verify: `speech_eval.py` prints "undecidable" when n is short.

**2. Schedule is not feasible as parallelised (§8 weeks 1-5).**
- Week 1 runs six streams: plugin spike, kids' sessions that need a research-recording mode not yet built, parser over 115 files, IPA path, voice audition with five parents, Opus on two phones. Speaker chosen week 1, recorded week 2; a failed same-person gate (D25) moves it again.
- Week 4 builds E1-E12 + E6c + E22 + E23 + trace scoring + gate reducer + repair audio trace + Listen & Talk + two skins + critic round 2. §3.3 lists 23 types and §6.1 admits `path/learner/onboarding/drills` are rewrites.
- The only pre-agreed cut is the verifier (§8). Nothing is named to drop if week 4 slips.
- Fix: commit an ordered cut list (placement stages 1 and 4, judge's card, L6-L7 packs, Urdu glosses, Track B skin) with dates.

**3. IPA to Kokoro and OOV (§4.2 steps 1-3, C5).**
- Kokoro silently drops phonemes not in its vocab, so the round-trip gate is right. But misaki US uses single-symbol diphthongs (`A I W Y O`), `ʤ ʧ`, `ɜɹ` for /ɝ/; the table is "verified in week 1" with no owner.
- The espeak fallback was disabled, not fixed (research-02 §3). OOV words therefore need manual IPA. misaki stems only -s/-ed/-ing, but L5-L7 word work is prefix/suffix derivatives (`unmistakable`, `corroboration`).
- C5 "100-300 overrides" has no support. My estimate is several hundred to ~1,300 across 4,100 L3-L7 new words.
- §4.1 uses 61 lessons for pseudowords; L1.03-L4 is 60.
- Slow mode (§4.1, D26) covers L1-L2 words only (1,066+575). Nana Karim reaches L3 within a month (§1.2) and loses it; extending costs ~4,100 clips, ~12.8 MB. Slow sentences are normal-speed isolated words, which flatten prosody.
- Fix: run the misaki lookup over all 9,238 words on day 1 (an hour) and publish the OOV count; repair espeak instead of banning it.

**4. Audio engine and pack delivery are new code mislabelled as reuse (§6.6, research-05 §3).**
- Urdu `content.js:4-17` is one `new Audio()` with a queue and a 1.5 s watchdog that rebuilds the element. §6.6 replaces it with WebAudio, bundle slicing, an 8 MB LRU and pre-decode. That is a new engine and it is not in the §6.1 "new work" list.
- 8 MB is ~41 s of 48 kHz float32. Android WebView `decodeAudioData` on Ogg Opus slices, AudioContext resume, and volume or route changes when the mic opens are all unmeasured. The watchdog is dropped.
- `Filesystem.downloadFile` has no Range resume, so resume is per file (L6 bundles ~1.1 MB, fine, but unstated). Manifest and packs share one GitHub Pages origin, so a hash manifest is unsigned.
- Fix: spike WebAudio decode plus mic handoff on the 2 GB phone in week 1. Sign the manifest. Verify: p95 tap-to-sound over 200 taps; `dumpsys meminfo`.

**5. Install table is not honest as stated (§0, §4.1, §7.6).**
- "Install" is measured by `bundletool get-size total`, which is download size, not installed size. 16 KB alignment forces uncompressed `.so`, inflating the libs' share.
- 54 MB is the sum of lower bounds. The 94 MB end pairs lower-bound audio with upper-bound native. The words ceiling adds +8.7 MB, and a model ≤25 MB in base takes base to ~79 MB before audio growth.
- A sideloaded universal APK carries both ABIs (+15-20 MB). The listing's "about 54 MB" for later levels is a lowest-of-lowest sum.
- Fix: publish named ranges; measure download and installed size on the phone by week 2.

**6. Migration ladder and backup are the wrong fix (§6.4, research-05).**
- The Urdu `db.js:42-44` repair path bumps `d.version+1` on missing stores and must be deleted, or it races the ladder.
- `backup.js` is a strict whitelist. Progress keys must match `^\d{1,2}$` (line 34), so `L1.02` keys are dropped. Units are `int(0,12)`. Card kinds are `oneOf('letter','word','sight')`. The `id` regex (line 16) rejects apostrophes and spaces, so `profile:don't` cards are dropped. The four new stores are not in `SCHEMA`.
- Backup is tested in week 7, one week before ship. Fix: schema plus A-to-B round trip in week 3, with an apostrophe item and `L1.02` keys.

**7. L6-L7 are shipped with no way to pass them (§2.1, §3.5, C11).**
- L6.05 Check is 5 items; 3 are inferential or evaluative with prose answer keys. L7.03 "Check" states no bar at all, only model answer plus a self-check. §3.5 defaults those to 0.9, which no machine can compute.
- C11 delivers MCQ anchors for L5 in week 6 and L6-L7 in v1.1, yet the L6-L7 packs (18+11 = 29 of 54 MB) are rendered, QA'd and listed in v1.
- The §2.1 block counts match my grep, but §6.2 makes every block optional, so the coverage report cannot fail; "committed" is the exit, not a yield.
- Fix: defer L6-L7 audio to v1.1 with their gates; set a numeric parser bar (e.g. ≥95% of L1-L4 lessons yield check, bar and pseudoword set without `app:` help).

**8. Test harness is half manual and cannot run (§6.8).**
- No device is attached (round 1, point 8). Items 7, 8, 9, 11, 15 and G0 need people or phones; items 4 and 6 need an oracle driver that exists only as a proposal.
- Fix: tag each item auto/device/human; a green auto set must exist before week 4.

## Unsupported numbers
- "6-10 days" for the plugin and "15-20 MB" native: research-05 says "probably".
- p50 <500 ms after end of speech: VAD hangover alone is ~500 ms.
- "≥4/5 same person" with n=5 cannot separate 60% from 80%.
- pron.json "100-300" and model "5-40 MB": estimates that drive decisions.
