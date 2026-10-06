# Critics round 5, audio (plan-v5 §4, D0a)

**Verdict: B.** The one-voice-per-exercise rule is unreachable as written: the 60 instruction and feedback lines stay Sound Teacher at Level 4, so every Reader exercise plays both voices, and the Reader's chunk repair ("gar... den") has no evidence at all.

**Biggest gap: the Level 4 boundary is not join-free (D1).**

Evidence: bakeoff wavs (measured), research-02 §5-6, research-06. The bakeoff has no chunk clips; Kokoro is not installed here.

## Defects

**D1. §4.4 table, §3.2, §3.5, §3.6, §8 cuts | the L4 join survives**
- Wrong: the table assigns "UI" to Sound Teacher for L0-L3 only; the L4+ rows list no UI, feedback or intro lines. §3.2's ≤60 lines ("Tap what it says.", "Yes!", "Which starts with /s/?" plus a sound clip) are level-independent. Either every L4 exercise holds a Sound Teacher clip and a Reader clip, so the "no exception" trace test fails them all or is silently exempt, or the lines move to the Reader and the human /s/ in the prompt sits in a Reader exercise.
- Also: the Stories tab queues human L3 beside Reader L4 passages; placement Stage 3 alternates voices item by item (the handover test covers one L3 to L4 sequence); cut A3 puts Reader texts inside human L3; cut A1 reuses foils across checks, breaking "T, F, X, FX share a session" (§4.5); L4 Meet cards play a human sound then Reader words.
- Fix: add a row "L4+ instructions, feedback, intros: Sound Teacher, always"; define "exercise" as prompt plus content plus feedback, and say the boundary is "instruction voice, content voice". Delete A3. Restrict A1 reuse to within one recorded session. Say whether a Meet card is an exercise.
- Verify: a script walks real timelines for every exercise type, the Stories queue and placement; the handover stimulus includes an instruction line, a feedback line, a Reader item and a repair.

**D2. §4.2 step 3, §3.4 E5(6) | chunk rendering via IPA is assumed**
- Wrong: research-02 §5 measured Kokoro single phonemes at 0.09-0.19 s active inside 0.5-0.7 s of padding; whole pseudowords already failed (vop→"vob", chote→"Chode", blim naturalness 1). A separately synthesised "gar" gets phrase-final fall and length, and "den" alone is stressed /dɛn/, the real word "den", not the syllabic n of /ˈgɑɹdn̩/. The learner hears a different vowel than in "garden". Chunk QA is a human listening to chunks, with no chunk-to-word criterion.
- Fix: do not synthesise chunks. Render the word once, take Kokoro's predicted phoneme durations for syllable boundaries, slice chunks from that waveform with 5-10 ms crossfades at zero crossings. IPA-rendered chunks only when a slice fails the click check, flagged for the reviewer.
- Verify: ASR round-trip of the concatenated chunks with the 350 ms gap against the word, plus a blind native check on 40 chunks ("part of garden?" ≥90%).

**D3. §4.3 step 2 | loudness rule is computable but wrong**
- Wrong: it contradicts itself (clips gained "to the word class mean" versus "each class within 1 dB of the sentence mean"). A class mean permits a 6 dB outlier clip. Equal K-weighted RMS makes /s/ and /sh/ perceptibly harsher than vowels on a phone speaker. A 100 ms /p/ is about 10 frames, with the burst one of them, so estimates swing per take. Gaining to sentence RMS limits stops routinely (bakeoff ph_p peak -12.9/RMS -30.9; word_sat -8.6/-27.7; sent_adult -7.5/-26.2), and the ">2 dB limiting" Q1 fail has no remedy. Kokoro words (0.37-0.50 s active) straddle the 0.4 s switch, giving one class two definitions.
- Fix: one measure for every clip, K-weighted active RMS over the loudest 100 ms, a per-clip ±1.5 dB window. Sounds get their own target set by ear on the test phone in week 0. Drop the LUFS path for single words.
- Verify: Q1 prints per-clip deviation.

**D4. §4.5 drift check | bands without method, coverage or enforcement**
- Wrong: F0 ±10% is about ±1.7 semitones, measured on 10 words and one sentence. Tilt ±2 dB has no band or frame definition,. Rate ±8% on one sentence is within natural variation. The baseline is session 1 (sounds, UI), not words, and a bad day anchors everything. It runs at session open, so it cannot see the within-session slump the plan fears; no per-clip check exists. Reverb and list intonation go unmeasured. "Engineer accepts with a note" lets the person who wants the clips waive the breach.
- Fix: a fixed 60-second prompt sheet at session open and close; pYIN median F0, 1/3-octave long-term spectrum 100 Hz-8 kHz, syllables per second; SNR ≥ 50 dB A-weighted; an RT60 estimate from word tails. A waiver needs a second person's sign-off and flags the clips.
- Verify: replay the pilot recordings plus a deliberately degraded copy (mic 15 cm closer, +2 dB tilt, 10% faster); the script must flag it.

**D5. §4.5 fatigue, throughput, stop gate | schedule assumptions untested**
- Wrong: the pilot is one 2-hour sitting; the real load is 90-minute sessions, 6-11 a week, "near full-time", where the third session of a day is the failure. 120-150 clips/h is not defined as accepted clips. Engineer take-picking hours appear in no table. Selecting stops "through the phone speaker" selects on burst and VOT cues, because the voicing bar sits below the speaker's roll-off; the plan should say so. The ≥90% gate has 8 listeners, no trial count, and does not say whether it runs on the WAV or the 24 kbps Opus decode.
- Fix: week-0 pilot of two 90-minute sessions in one day plus one the next; report accepted clips/h; run the stop gate on Opus-decoded clips, 3 contrasts x 3 words x 8 listeners (72 trials each), ≥90% each.

**D6. §4.4 handover test | right statistic, wrong population**
- Wrong: the arithmetic holds (SD 1, n 16, bound about 0.34 below the mean), but the SD is assumed; report the observed interval. Sixteen adults rate one 10-item sequence once; users are children and low-literacy adults with hours of Reader exposure, so irritation and mispronounced made-up words (vop→"vob") go undetected. "Same teacher?" is not gated, so 16/16 "no" with comfort within 0.16 passes, yet the app must announce the change. Groups are not powered, and non-native listeners likely rate the Reader worse.
- Fix: pass = pooled bound ≥ -0.5 and each group's mean difference ≥ -0.75; random Reader items including an instruction line (D1), the announcement and one repair; add 3 pilot-site learners and fail if the Reader has ≥1 audible error per 20 items.

**D7. §7.2 and §4.4 workload | third voice, and a sum that omits second passes**
- Wrong: the pack speaker (60 UI lines plus 177 glosses, 2-3 h, non-professional) is a third voice in Listen & Talk after the questions, with unspecified gender and age, no audition, no drift check and no comfort test. The reviewer sum (4,100-6,500 clips at 400/h = 10-16 h) omits the Q2 lowest-20% pass (about 600-1,000 clips), the 150-clip two-rater set, the non-native test, re-review of re-records (10% reject is 700-1,000 clips), week-9 pickups and the Reader re-render loop. A realistic total is 18-26 h against a ≤4 h/week cap over 8 weeks (32 h), with no slack.
- Fix: audition each pack speaker against the Sound Teacher (5 listeners, warmth and pace); pack lines play only on their own card after the exercise, never inside it. Re-sum the workload with those rows.
