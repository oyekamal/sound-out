# Critics round 3: audio (plan-v3 §4, D0a)

**Verdict: B.** One human voice within L0–L2 is fine, but the Level 3 handover is not a clean announced swap: the plan's own repair and tap-a-word rules play human sounds then a Kokoro whole word in one exercise (the join both earlier audio critics rejected), and no test catches it.

**Single biggest gap:** the "voices never alternate inside one word exercise" rule is contradicted by the plan's own mechanisms (defect 1).

## Defects

**1. §2.3 rule 1, §3.3 line 223, D0a: the human-sounds-then-Kokoro-word join is back at L3.**
- Wrong: D0a promises no alternation inside a word exercise. Line 223 has L3 repair use "human grapheme sounds with gaps ≤150 ms"; rule 1 has tap-a-word play grapheme sounds, then the whole word (Kokoro from L3). That is s-a-t then "sat" in a different voice, every time.
- Also: the gap is ≤150 ms here and 350 ms in §4.3 item 6. The lexicon sets `"voice":"human"` per word, yet L1–L2 words recur in L3+ review and inside Kokoro sentences. A tapped "sat" in a Kokoro sentence has no stated voice.
- Fix: either record L3+ decodable words with the human (the plan's own +~10 h fallback), or write a voice-resolution table for review, tap, repair and sentence-word-tap, with one gap value.
- Verify: an audio-trace test failing any timeline where a human clip precedes a Kokoro clip of the same word within 1 s; run G5 on the real L3 repair, not on isolated clips.

**2. §4.3 item 3: the loudness rule's threshold sits inside the word distribution, and the short-clip branch overdrives.**
- Wrong: bakeoff af_heart words trimmed at −45 dBFS are 0.39–0.45 s (sat 0.40, ship 0.39, cake 0.41, pin 0.42). The plan does not say if "≥0.4 s" is judged before or after the 120 ms padding, so near-identical words fall on opposite sides of a switch between integrated LUFS and the window method, creating a step in the middle of the word population. A 400 ms window is one BS.1770 gating block, so LUFS there is valid; the problem is that a 105–240 ms phoneme leaves the window mostly empty.
- Evidence (my own K-weighting approximation; absolute levels ±4 dB, relative figures hold): reaching −18 in the window needs roughly 7 dB more gain for /s/ than for a word. Own loudness ends ~5–6 dB above words and the peak ~6 dB above word peaks. Words have about 2.7 dB headroom to −1.5 dBTP, so /s/ /ʃ/ /θ/ land 3–4 dB over the limiter. The limiter then flattens the sibilance that separates /s/ from /ʃ/. A 20–40 ms stop burst needs more again.
- Fix: judge the threshold on the unpadded trimmed clip; cap the short-clip boost (for example +6 dB over the clip's own integrated loudness); accept phonemes 3–4 dB under words.
- Verify: Q1 measures post-limiter decoded-Opus loudness and per-clip gain reduction; fail any clip limited by more than 2 dB.

**3. §4.5 recording spec: no direction for the hardest clips.**
- Wrong: it gives format (48 kHz mono, 20–30 cm, no AGC) and nothing on room noise floor, pop filter, input level or headroom, retake rule, or distance consistency. At 20–30 cm without a pop filter a /p/ thump passes a −45 dBFS trimmer and a loudness check. Nothing tells the speaker to say stops without a vowel; research-02 says stops "cannot be said in isolation", and the bakeoff's own `ph_p_schwa` is 1.30 s against 0.57 s for `ph_p`. Left alone, a human says "tuh".
- Fix: write the direction (minimal aspiration, no vowel; voiced stops as a short murmur; three exemplars in the test file); mandate a pop filter, ≤ −60 dBFS room tone, peaks near −12 dBFS, and a retake rule.
- Verify: Q1 rejects stops over a per-class duration cap and flags sub-100 Hz energy in the first 30 ms; the GA reviewer blind-labels three takes each of /p t k/ as schwa-free.

**4. §4.5 studio time: 250 clips per hour does not survive the QA design.**
- Wrong: 250/h is 14 s per clip including three takes of each phoneme, retakes, and a room-tone plus reference /æ/ check at every session start. Pseudowords are the clips speakers normalise toward real words. §4.4 says "Take chosen at capture by the recording engineer", but a remote self-recorded speaker has no engineer.
- Evidence: this is my estimate from practice, not a measurement; the plan's figure is also an estimate, with no pilot behind it.
- Fix: budget 120–150 clips per hour (about 35–55 h) or cut the foil count; name who chooses takes.
- Verify: time 200 mixed clips (words, pseudowords, stops) from the candidate speakers before D16 is signed.

**5. §4.2 item 1, §4.4 determinism: seeding does not make cross-machine bit-identity.**
- Wrong: seed, thread count and "CPU flags" are pinned, but torch CPU kernels dispatch on the CPU (AVX2/AVX-512, oneDNN, MKL) and summation order changes with threads; a different CPU generation can still differ. The test also passes if the drifting component is merely "named".
- The real protection is "an approved clip id is never re-rendered". Say that, and demote bit-identity to a nice-to-have.
- Fix: pin dispatch (`MKL_CBWR=COMPATIBLE`, `ONEDNN_MAX_CPU_ISA`, deterministic algorithms), or treat rendered files as the source and test ASR-equivalence instead.
- Verify: sha256 over 100 clips on two different CPU generations; the build fails if a frozen clip's hash changes.

**6. §4.4 rating design: the sample and the raters cannot support "one-teacher consistency".**
- Wrong: Cohen's kappa on a 5-point anchored scale over 100 clips needs a weighted kappa or ICC; with most scores at 4–5 plain kappa can be low despite good agreement. The second listener may be Kamal, who wrote the plan; the GA reviewer is both primary reviewer and speaker-selector. The Level 3 handover has "acceptance by 5 parents and 3 adults" with no pass bar.
- Fix: weighted kappa or ICC with a pre-set floor, an independent second rater, and a stated handover bar (for example ≥6 of 8 acceptable and nobody says the teacher left). Pre-register it in G5.
- Verify: thresholds committed before any rating is collected.

**7. §4.5, D9: the Urdu voice is a third voice with an unresolved licence.**
- Wrong: the measured Sara passage clip is 22.05 kHz, from a different pipeline and room than the English human set, so §4.3 levels do not apply unless re-run. The licence is only "check". I did not verify ElevenLabs terms, so treat the commercial-redistribution-in-an-APK question as open. §3.8 puts Urdu gloss then English chunk in one exercise, so a learner hears three voices there, with the Urdu one the only unprocessed one.
- Fix: close D9 in writing before week 3 (terms in force at generation date, commercial, redistribution); pass the clips through §4.3; otherwise record a human Urdu speaker with the same kit.
- Verify: Q1 loudness and padding on the Urdu set; licence text in LICENSES.md.

## Checked and fine
- 40/80 ms padding and the 15 ms stop fade fit the measured bursts. The 350 ms gap is sensible if used everywhere.
