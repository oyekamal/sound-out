# Critic round 5, engineer (plan-v5)

**Verdict: B.** The week-3 to week-8 app scope is now fully from scratch, while the voice chain needs 44-85 recorded hours plus about ten serial human-subject gates, and the only slack (week 9) is already booked three times, so something gets cut or slips.

**Single biggest engineering gap: the plan still prices a copy-and-patch app.** The owner's rule is now "no code copied", but §6.1 says "Copied from urdu-reading-course/mobile (~12% as-is, 70% changed)". §6.3 is a patch list against Urdu files (`db.js:44`, the `units` cap of 40, `learner.js:41-43`, `backup.js SCHEMA`). Research-05 marks `gate.js`, `swreg.js`, `backup.js` ("Keep it exactly"), `content.js` and the Marko rig as AS-IS or reusable. Its week plan assumed "Repo from copied files". With reuse gone, these are all new in weeks 2-5, beside content generation:
- IndexedDB schema, migration ladder and backup/restore.
- Leitner scheduler and the profile/lock/doors system.
- Service worker.
- Tracing canvas with stroke-order, direction and start-zone scoring for 26 letters (E4).
- The Lottie runtime.
- About 22 exercise types, two skins, Stories, free play, placement and the grown-up view.
- A pack manager with signature checks.

Nothing in §8 re-estimates this. The §6.3 bug list is moot; a fresh schema needs its own design and round-trip test.

- **Fix:** delete §6.1's "Copied" line and rewrite §6.3 as a fresh design. Add an app-side effort table per module, with a named engineer-week count. Cut A-list items to match.
- **Verify:** the module table sums to at most 5 engineer-weeks in weeks 2-8 on a named staffing level, and `db.js`, `learner.js` and `voice_studio.py` appear nowhere in the build plan.

## Defects

**1. Sprite sizing: the 30 s cap does not hold, and the disk and download maths ignore duplication. (§6.2, §4.1)**
- Wrong or unproven: the 36 MB peak assumes each step sprite is 30 s. A check step must hold, per item, T/F/X/FX options, partials, a non-target contrast pair and the fresh-item retry pool. 10 items x 4 options x about 0.7 s is already 28 s before repairs, retries or the L3 sentence-with-taps case. The step is one sprite, so it breaks the cap. §4.1 sizes are unique clips. "Every clip the step can play" copies the same clips (sat, the sounds, UI lines) into hundreds of sprites. That inflates the 23-35 MB base figure by an unmeasured 2-4x, and the 370-550 sprite count is an estimate.
- Evidence: §6.2 text; the 12.5 KB/sentence and 3 KB/option clip lines. Research-05 line 188 already notes 4 KB block rounding on small files.
- Fix: define the sprite as a dedup'd lesson blob plus offset index, or a content-addressed clip store with per-step manifests. Report unique MB and shipped MB separately.
- Verify: the week-1 build script prints max sprite seconds across all steps, the shipped-to-unique ratio, and `dumpsys meminfo` on both phones with real sprites.

**2. Tap-read contradicts the voice trace test. (§3.5, §4.4)**
- Wrong: "a tapped decodable word plays sounds first, the word after" uses core human sound clips. Taps must also use "the sentence's voice". At L4, tapping a decodable word in a Reader sentence therefore plays human sounds inside a Reader timeline. That fails the plan's own trace test ("fails any exercise timeline holding both a Sound Teacher and a Reader clip"). It also breaks the claim "No isolated sound inside any Reader exercise".
- Fix: L4 Stories and tap-read play whole Reader words or Reader chunks only. Sound-first stays L1-L3.
- Verify: trace-test fixture of an L4 tap-read page passes.

**3. L1.03/L1.04 made-up options do not support the check design. (§3.4, §6.1)**
- Wrong: I enumerated strings over the taught letters with `/usr/share/dict/american-english` as the real/made-up oracle. At L1.03 (s a t p i n) about 11 made-up CVC/VC strings exist, and only 7 can be the target of a made-up 2x2 grid. At L1.04 (+m d) it is about 33 and 23. Real words at L1.03 are 22, 16 with a grid, and that is before dropping rude or obscure words such as tit, nit, pap.
- Evidence: the course check is "Pseudo (5): tas nas pas tis nis". All five are targets and also foils of each other. Four targets share the single 4-cycle {tas, nas, tis, nis}.
- With "no word twice per check", late items fall to elimination. "2 sets x 5 made-up" plus fresh-item retries exceed the pool.
- Fix: cap made-up sets at the grid-able pool; use the chain rule where it is too small.
- Verify: `gen_options.py` emits pool size, grid-able targets and distinct strings per lesson for L1.02-L1.13, and the build fails when `needed_sets x 5` exceeds the grid-able pool.

**4. L1.02 chains are mostly impossible, so the "middle in a third" rule fails. (§3.4)**
- Wrong: over {s, a, t} the one-change neighbours of "sat" are tat and sas. "at" has one valid neighbour ("as"; "ta"/"sa" differ by two edits). "as" has one ("at"), so there is no 3-chain, and the course checks "at, sat, as, at, sat" are exactly these. For "sta", "ast" and "att", most neighbours are unpronounceable (sst, aat).
- Consequence: the answer cannot be centred for at/as, which are 4 of the 11 real items. So answer position is determined by the target, and the plan's "chance" figure (1.97% random) assumes balancing it cannot achieve.
- Fix: for L1.02, drop the chain claim and use plain 3-way pick with unequal edit distance, and state the real chance numbers. Or take L1.02's check from tiles only.
- Verify: the generator prints the achievable answer-position distribution for the L1.02 items, and the oracle runs on it.

**5. Reader pipeline: chunk rendering is unproven and mis-sourced. (§4.2)**
- Wrong: "chunks rendered from IPA syllables" ("gar… den") is presented as a pipeline. Research-02 tested isolated phonemes and whole words only, found made-up words misheard (vop, chote) and called for human review of the whole list. No evidence shows Kokoro gives clean, correctly stressed fragments from syllable IPA, and no word-level concatenation test exists. Kokoro runs about 1.3-2 words/s, and 2,580-4,380 clips with re-render loops is a multi-day compute job.
- Evidence: research-02 lines 67, 95, 123, 132.
- Fix: week-0 spike on 30 L4 words, chunked and whole, played through the test-phone speaker, before D0a is confirmed. The week-1 `ipa2misaki` round trip alone does not cover this.
- Verify: 8 listeners identify the syllable boundary and word at ≥90%.

**6. The schedule has no slack for its own gate failures. (§8, §4.4, §9)**
- Wrong: the stop gate (8 listeners, before week 2), the vowel test (12, week 5), the handover test (16 listeners, week 6), non-native intelligibility, the ICC pair, the paper proxy test (10 people in 2+ countries, week 3), and the no-language launch test with 20 participants all depend on recruiting. Any failure forces re-records or D0a-alt. The handover-fail fallback is 14-29 h of recording, landing in weeks 7-9.
- Week 9 "slack" already carries pickups, "lost-gate re-runs" and the Whistle spike (the research estimated about 2 days of JNI/plugin work). L1 sentences are a week-3 deliverable but L0-L1 is recorded in weeks 2-3 and frozen in week 1.
- Fix: a dependency chart with each gate's no-go consequence in hours. Move the Whistle spike out of the 10 weeks, and drop the handover test for an up-front decision on L4.
- Verify: weeks 2-8 can absorb the worst single gate failure without touching week 9.

**7. Signed packs and PWA assumptions are not checked against the Chrome 74 floor. (§6.3, §6.4)**
- Wrong: the signed ed25519 manifest has no verification path. WebCrypto Ed25519 is missing from old WebViews, so a JS library is needed, against a JS budget of <150 KB. Research-05 line 196 says to ship an AAC `.m4a` variant for Safari, and the plan drops it while still promising iPad PWA. Ogg Opus decode on Safari/iOS is not shown.
- Fix: choose a verification library and count its bytes. Decide iOS format or cut the PWA (cut 13) now.
- Verify: unit test of signature verify on the Chrome 74 test WebView; an iPad decode test.

**8. Whistle flavour isolation is fragile in Capacitor. (§5)**
- Wrong: `cap sync` regenerates plugin Gradle lines, so a plugin is `implementation`-linked into all variants and merges `RECORD_AUDIO`. Flavour-only linkage needs `spikeImplementation` and a post-sync patch. The manifest check does not catch the plugin's native code or `.so` in the store AAB. The 97%/92% go bar needs about 60 items per class; the spike gives 180 clips in total.
- Fix: keep the spike in a separate repo and app id, not a Gradle flavour. Or cut it from v1.
- Verify: the merged store manifest and `unzip -l` of the AAB show no plugin class or `.so`.

## Unmeasured
- 150 clips/h is assumed; no research file gives a recording rate. Speaker fatigue and engineer take-picking (about 14-20k takes) are unbudgeted.
- Tap-to-sound p95 <150 ms on a 2 GB Android 10 phone has no fallback. Decode time and `decodeAudioData` transient memory are outside the 36 MB.
