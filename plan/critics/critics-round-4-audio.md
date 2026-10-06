# Round 4 audio critic (speech/audio engineer)

## Verdict: B

Levels 0-2 with one human voice are credible. The Level 3 handover is not: the core L3+ loop (human sounds, then a Kokoro word) is the same join rounds 1 and 2 rejected, now relabelled "confirmation". The within-level consistency claim also has no gate across 13-20 recording sessions.

## Single biggest audio gap

The L3+ repair (§3.3 line 266) and tap-to-read (§3.4 line 333) still splice two timbres on one word.
- §4.4 forbids the same word in both voices within 1 s, then exempts the exact step that does it.
- Repair is human s-a-t, 350 ms, Reader "sat". The learner is trying to hear the sounds fuse into the word, so a timbre change reads as a different word, not a confirmation.
- Tap-read does this on every tapped word.
- "After the 2nd attempt" delays the join by one try. The learners who fail are the ones who need the cleanest blend model.
- The plan's own fallback (Sound Teacher records L3 words) is the only join-free version, and it sits in the risk table, not the design.

Fix, pick one:
- (a) The human records the blend/repair/tap-read set at L3+ (slow take plus whole word).
- (b) The Reader never plays in the blend, repair or tap loop. Repair ends on the learner's attempt plus a human whole word, and the Reader speaks only prose and passages.

Verify: a trace test fails any timeline where a human sound clip is followed within 2 s by a Reader clip of that word. Delete the confirmation-step exception.

## Defects

**1. §4.4 tapped word plays "its own lexicon voice"; review cards use the voice learned in.**
- Wrong: a Reader sentence containing an L1 word plays a human take mid-sentence on tap. One word has two voices inside one level.
- Evidence: L3+ sentences are built from L1-L2 words, so this is the common case. The 1 s trace test cannot see it.
- Fix: a sentence plays whole in one voice, and a tap inside it resolves to that sentence's voice.
- Verify: a tap-resolution table test; fail if any tap target voice differs from the containing clip.

**2. §4.3 loudness rule is not computable and contradicts Q1.**
- Wrong: "cap +6 dB over the clip's own integrated loudness" applies to clips under 0.4 s, which have no integrated loudness (BS.1770 needs a 400 ms block).
- Measured: Kokoro bakeoff clips trimmed at -45 dBFS give `ph_s` 104 ms, `ph_p` 144 ms, `ph_a` 198 ms, `let_s` 314 ms. ffmpeg ebur128 returns I = -70 (undefined) for all of them.
- Measured: trimmed `sat`, `pin` and `ship` are 0.43-0.45 s, right on the 0.4 s class boundary. A 30 ms trim difference changes the rule.
- Wrong: Q1 demands class means within 1 dB of sentences, while §4.3 lets phonemes sit 3-4 dB under. Padding `ph_s` and `ph_p` to a 0.4 s window measures -29.9 LUFS. With the +6 cap that lands about 6 dB under words, not 3-4.
- Fix: one defined statistic for all classes (LUFS-S on a clip padded to a fixed length, or active-frame RMS) with an explicit per-class offset table, and make Q1 check that table.
- Verify: run it on the 68 Kokoro bakeoff clips and the audition files; no undefined values, offsets inside tolerance.

**3. §4.4 handover bar: 8 listeners, mean >=4/5, at most 1 below 3.**
- Wrong: with SD about 1 on a 5-point scale, 8 raters give a CI half-width of about 0.7. The bar cannot separate 3.5 from 4.2.
- Wrong: "naive listeners rating comfortable" is not the target. Learners are Urdu-L1 on a phone speaker, and the question is "same teacher?".
- Wrong: there is no control against the human-only fallback.
- Fix: 12 or more Urdu-L1 listeners on the test phone's speaker. The same 10-item L2 to L3 sequence is played in both conditions. They rate "same teacher" and "comfortable", and the pass rule is non-inferiority to human-only with a pre-committed margin.
- Verify: commit the margin, the analysis script and the stimulus list before rating.

**4. §4.5 stops: voiced murmur on phone speakers, "shortest clean burst", one take for two positions.**
- Wrong: the /b d g/ cue ("short murmur, no vowel") sits below about 300 Hz, where budget phone speakers roll off. /b/ vs /p/ may be indistinguishable on target hardware.
- Wrong: selecting the shortest burst, then the 15 ms fade, -45 dBFS trim and sub-100 Hz flag, strip that cue further.
- Wrong: initial /p/ ("pin") and final /p/ ("cup") need different releases but share one take.
- Fix: record initial-released and final-unreleased variants. Gate on a blind /b/-/p/, /d/-/t/, /g/-/k/ discrimination test through the test phone's own speaker with Urdu-L1 listeners.
- Verify: >=90% identification, committed before week 2.

**5. §4.5 no cross-session consistency gate, and the rate ignores fatigue.**
- Wrong: each session opens with room tone and a reference /æ/, but nothing compares them to a baseline. There is no limit on F0, spectral tilt or speaking rate across 13-20 sessions. Q1 checks only loudness and padding.
- Wrong: week-9 pickups are recorded weeks later and inserted into frozen levels, bypassing any check.
- Wrong: 150 clips/h (24 s a clip including 3 stop takes and retakes) over 2.5 h sessions ignores vocal fatigue. The 200-clip pilot does not measure it.
- Fix: a fixed per-session reference script (the /æ/, 10 words, one sentence). Compare against the session-1 baseline with limits (for example F0 median within 10%, tilt within 2 dB, rate within 8%), and re-record on breach. Cap sessions at 90 min. Use the pilot's second-hour rate in place of 150/h.
- Verify: apply the thresholds to the 3 audition files before choosing the speaker.

**6. §4.4 rater agreement and reviewer workload.**
- Wrong: "ICC(2,1) >= 0.75 or weighted kappa >= 0.6": "or" lets the lenient statistic pass. On 150 pre-screened clips the score range is narrow, so ICC is unstable either way.
- Wrong: both raters are General American speakers judging GA clarity. No Urdu-L1 listener rates intelligibility of the English clips, apart from the 5 on minimal-pair vowels.
- Wrong: the workload is never summed. The reviewer hears 100% of phonemes (47 x 3 takes), demos, made-up words (~560), options (900-1,800), 10% of 2,400-3,900 words and sentences, then 500-790 Reader clips plus 398 made-up words and every override. That is roughly 3,500-4,500 clips plus the 150-clip overlap.
- Fix: require both statistics on a set with planted bad clips. Add 5 Urdu-L1 raters on 100 clips through the phone speaker. Total the reviewer hours and set a weekly cap.
- Verify: planted-defect recall >=90% for each rater.

## Probes with no finding

- Urdu at 24 kHz: the Sara clips are 22.05 kHz MP3 and measure -17.9 to -21.6 LUFS, TP -1.7 to -6.6. Through §4.3 they are fine for glosses and UI only. Upsampling adds nothing but does no harm.
- Frozen clip ids: the guarantee holds, but "build fails if a frozen clip's hash changes" must hash the approved pre-Opus WAV. A libopus or ffmpeg bump changes encoded bytes.
- Spec numbers (-60 dBFS room, -12 dBFS peak, 20-30 cm, 48 kHz/24-bit, no AGC) are fine. The problems are what is not checked (defects 4 and 5).
