# Critic round 2: audio

Measured: 68 bakeoff wavs, 24 fresh Kokoro renders, 10 Sara mp3s, Opus round trips (scripts in `scratchpad/tts/`).

## Verdict: B

There is no demonstrated route to one voice: the human-to-Kokoro join rests on an unmeasurable EQ step and a 5-parent test that cannot reject a bad join, and the fallback cannot make pseudowords.

## Single biggest gap

There is no measurable definition of "same teacher". §4.4 says "EQ to af_heart's long-term spectrum" with no tool, target curve, formant or F0-contour criterion, and no owner, then protects it with a gate a noticeable join passes about half the time. The s-a-t to "sat" blend is the core interaction.

## Defects

**1. §4.4 steps 2-3: the spectral target is meaningless.**
- Evidence: Kokoro is 24 kHz, so "low-pass near 12 kHz" is Nyquist, a no-op. Kokoro's isolated /s/ (`ph_s`) has centroid 513 Hz (40 dB at 0-1 kHz, 16 dB at 6-10 kHz): a rumble, so there is no Kokoro reference for isolated phonemes. The /s/ inside "sat" (first 100 ms) has centroid 9.1 kHz; inside "ship", 5.7 kHz. "Within 15% of the /s/ in sat" is 7.8-10.5 kHz: one word, one fricative.
- Fix: a per-sound table (s z ʃ ʒ f v θ ð; F1/F2 for the short vowels) with centroid and 3-6/6-10 kHz band levels, taken from Kokoro in-word segments via forced alignment (MFA or whisperx). Name the EQ method (matching EQ from 60 s long-term spectra per side, 1/3-octave, ±3 dB cap) and the owner (build agent, `tools/match_eq.py`).
- Verify: script prints human vs Kokoro per cell; gate = all within tolerance, committed.

**2. §4.4 step 1: F0 target sits at the top of the adult range.**
- Evidence: af_heart word medians are 215-238 Hz (sat 233, cake 238, ship 224, pin 215); the sentence is 194 Hz. "Within 2 semitones" is about 199-261 Hz. Sara reads 135-166 Hz. A recruited teacher at 180-210 Hz fails the shortlist or will strain upward. No accent criterion exists although the phonemes are specified General American. Isolated phonemes are flat; Kokoro words span p10-p90 of 25-50 Hz.
- Fix: audition adds rhoticity, /æ/, /ɑ/-/ɒ/, flap-t scored by the GA reviewer; compare F0 contour, not just median.
- Verify: F0 and contour table per candidate before recording.

**3. §4.4 step 3: the "same person?" gate is statistically empty.**
- Evidence: pass is >=4/5. A pure guesser passes 6/32 = 19%. If 30% of listeners hear the join (p_yes 0.7), it passes 53%: a join a third of parents hear is waved through about half the time. The parents are only "naive". The prompt is leading. One stimulus (sat) says nothing about 69 demos or 44 phonemes. Phone speakers hide the >8 kHz band where /s/ differs.
- Fix: blind ABX/2AFC, 20 trials per parent, controls (all-Kokoro, all-human), on phone speaker and cheap earbuds, >=10 parents from the real install population, 4 stimuli (sat, zip, ship, thin). Pass: join detection within 10 points of control false alarms, with the interval reported.
- Verify: results file with per-listener counts and binomial 95% intervals.

**4. §4.2 step 6: loudness rule splits identical words across two scales.**
- Evidence: CVC words trim to 0.36-0.45 s at -45 dBFS (sat 0.40, ship 0.39, cake 0.41, pin 0.42). The 0.4 s cutoff puts neighbours on different branches: -18 LUFS (about -16.2 dBFS active RMS here) vs -20 dBFS RMS, a ~4 dB step inside one list. BS.1770 has one gated block under 0.5 s, so the "sd <0.5 LU" check measures gating noise. Peaks fight the -1.5 dBTP limit: raw af_heart "sat" is -8.6 dBFS at -24.5 LUFS, so +6.5 dB lands near -2.1 dBFS; "fraim" (pk 0.48, -23.8 LUFS) lands near -0.6 dBFS before Opus overshoot. `loudnorm` on sub-second clips goes dynamic and compresses. Sara measures -17.8 to -19.2 LUFS, so the target is fine; the peaks are not addressed.
- Fix: one rule for all clips under 1 s: K-weighted RMS over the active segment at a single value calibrated by ear against 3 s sentences at -18 LUFS, plus a fixed limiter; phonemes get a per-class offset table.
- Verify: Q1 on decoded Opus; every class mean within 1 dB of sentences, 95% of clips within 2 dB.

**5. §4.2 padding/fades: nothing defines the blend gap.**
- Evidence: raw Kokoro clips carry 380-440 ms lead and 410-560 ms tail; Sara 160-750 ms lead, 270-400 ms tail. 40/80 ms is fine for latency, but the gap between /s/ /æ/ /t/ and "sat" is unspecified, and that gap is where the join is heard. A 5 ms fade-out on a voiceless stop trimmed at -45 dBFS can eat the burst (`ph_p` is 0.15 s).
- Fix: a blend timing table (inter-phoneme gap, word gap) and burst-preserving trim for stops (no fade-out).
- Verify: spectrogram sheet of 10 blend demos; Q4 same-teacher rating on the sequence.

**6. §4.5 and §4.2 step 1: "Kokoro is deterministic" is false as built.**
- Evidence: same text, voice and speed rendered twice in one process gives different PCM, residual -17 to -20 dB (sat, ship, strag). With `torch.manual_seed(0)` per render, runs match (ad2eb9f9), but 1 thread vs 8 threads differ (ad2eb9f9 vs 16aa8db5). The plan pins threads but never seeds, so the two-machine sha test cannot pass, and a QA-approved clip is not what a rebuild ships.
- Fix: seed per clip from the clip id; pin threads and CPU flags; content-address clips and never re-render an approved id.
- Verify: 100 clips twice on two machines, bit-identical, or the drifting component is named.

**7. §4.4 step 4 and §4.2 step 5: the fallback leaves pseudowords unsolved; slow mode is a different render.**
- Evidence: Chatterbox and Qwen3-TTS take text, not phonemes (research-02 §1). Pseudowords (vop heard "vob", chote) go through their own grapheme guess with per-clip sampling noise, single-word input is a known failure zone, and a clone cannot speak an isolated /s/. D25 would fix words and break the ~770 decoding checks. Slow mode: Kokoro `speed` rescales predicted durations rather than resampling, so median F0 holds (sat 233 to 238, ship 224 to 240 Hz) but sat goes 1.23 to 1.55 s, F0 p10 207 to 178 Hz, centroid 692 to 912 Hz, >8 kHz share 0.43% to 2.19%.
- Fix: fallback = voice conversion of the Kokoro IPA renders to the human timbre (keeps phoneme control), or human-record all of L1-L2. Treat 0.8x as its own QA class and listen to 50.
- Verify: spike renders 20 pseudowords through the fallback; forced-choice Q3 >=95%.

## Probes answered briefly

- **Reviewer workload**: ~770 pseudowords + markdown's + overrides + Q3 fails + lowest 5% of ~14k (~700) is ~1,700 items, about 4 h at 8 s each, repeated on every rebuild unless clips are frozen (defect 6). Natives hear nonwords through lexical bias; give forced-choice foils, not "sounds right".
- **Q4 rating**: Kamal (the author, unblind) plus one parent is n=2 with no anchors or agreement statistic; 200 clips cannot separate 98% from 96% (95% interval about ±1.9 points). Use anchored scales, 3+ raters, kappa, and the full pseudoword set.
- **Opus**: 24 kbps keeps 8-12 kHz (sat 37 dB band energy preserved, centroid 9.06 to 9.36 kHz), so the codec is not the problem; but unpadded sat is 2.8 KB vs the 1.77 KB budget figure, so re-measure after trimming.
