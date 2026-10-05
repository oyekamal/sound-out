# Research 03 — Hearing the learner read (ASR / phoneme scoring) for the Read English app

Date: 2026-10-05. Scope: free offline Android/PWA, Urdu-first ESL, ages 4-60, synthetic phonics (course rules: DESIGN.md s2 - no cueing, mastery gate 90% on real + pseudo words, heart words, two metrics; template s4 - Blend it, Check, Read it).

Evidence labels: [V] = fetched and read this session; [B] = background knowledge, NOT re-verified (treat as lead). DDG was flaky (several queries returned nothing), so some vendor claims are [B].

## 0. Bottom line

1. Open-vocabulary ASR (Whisper, Moonshine, Android SpeechRecognizer) is the wrong tool for a phonics app. It is a language model that "repairs" what it hears, so a child's "sut" for "sat", or an alien word "blop", gets snapped to a real word or dropped. That is exactly the failure the earlier critic found (decisions.tsv, critic-4: "ASR snaps pseudowords to real words").
2. The right tool is **constrained verification**: we always know the target (the word on screen). Ask "did the audio match THIS phoneme string better than the plausible wrong ones?" using a CTC phoneme model or a forced aligner with a competitor set. That also handles pseudowords, because pseudowords have a known phoneme string.
3. Nothing offline is reliable enough on 4-7 year olds to be a *judge*. Build it as a *witness*: it can confidently say "yes, clearly right" and otherwise says "I'm not sure - parent/tutor taps". Never punish on a machine "no".
4. Keep the earlier decisions (whisper.cpp offline primary, Azure online-only optional, pseudowords/heart words human-judged) as a **v1 fallback**, but revise the v2 direction: replace Whisper with a small phoneme-CTC model in onnxruntime for the verify step. Retain Whisper only for passage word-level transcription (WCPM).
5. Godot mic bug godot#110337 is closed with milestone 4.6 [V], so it is no longer a blocker on 4.7, but the repro (first recording OK, after app restart only noise) must stay a day-1 device test. For a PWA/Capacitor build the issue is moot (WebView getUserMedia).

## 1. On-device ASR options (Android + web)

| Option | Size / cost | Offline? | Fit for phonics | Notes |
|---|---|---|---|---|
| whisper.cpp tiny / base | tiny 75 MiB disk, ~273 MB RAM; base 142 MiB, ~388 MB RAM [V github.com/ggml-org/whisper.cpp]; MIT; int quantization; Android + WASM examples | Yes | Words only. Hallucinates on silence/noise, snaps pseudowords | Pi 5 RTF 0.23-0.41 for tiny.en [V arxiv.org/html/2507.14451]; a budget Android phone is slower than a Pi 5 - measure. Use whisper's VAD |
| Moonshine (moonshine-ai/moonshine) | "down to tiny 1 MB models" per repo; MIT for current models; Python/JS-WASM/iOS/Android [V github.com/moonshine-ai/moonshine] | Yes | Streaming, low latency; still word-level open ASR | Good candidate for passage/WCPM word stream; check the 1 MB claim vs actual English model size before relying on it |
| sherpa-onnx (k2-fsa) | Apache-2.0 [B]; runtime for Zipformer, SenseVoice, Paraformer, Whisper, keyword spotting, VAD, TTS; Android, WASM, Kotlin/JS bindings [V github.com/k2-fsa/sherpa-onnx] | Yes | Best single *runtime* for Android + web (one lib, many models). Keyword spotting mode is a cheap "did they say one of these N tokens" check | Parakeet support: not confirmed from the README fetch [unverified] |
| Vosk | Apache-2.0, ~40-50 MB small English models [B] | Yes | Kaldi grammar-constrained decoding is possible (restrict to target + foils) - an old but valid way to do "verify" | Accuracy on kids worse than Whisper in most papers [B]; maintenance slow |
| Android SpeechRecognizer | free | `createOnDeviceSpeechRecognizer`, `isOnDeviceRecognitionAvailable`, `EXTRA_BIASING_STRINGS` exist [V developer.android.com]; needs API 33 and an installed language pack [B]; cheap Android Go phones often lack it [B] | Biasing strings help, but the output is still a language-model guess; silent app-level download dependency | Use only as an optional probe, not core |
| Web Speech API (Chrome) | free | `processLocally` is experimental [V MDN]; default Chrome Android sends audio to Google [B] | Poor: no confidence control, online by default, Chrome-only, kids' audio leaves the device | Reject for core |
| wav2vec2 phoneme CTC: facebook/wav2vec2-lv-60-espeak-cv-ft | Apache-2.0, large (300M params, ~1.2 GB fp32 [B - HF page did not state size]), outputs IPA/espeak phoneme strings [V HF] | Only after distillation/quantisation (INT8 ~300 MB) - too big for v1 | Directly emits phonemes, so pseudowords work | Trained on adult Common Voice, multilingual. Use on a server/laptop for evaluation to set thresholds |
| Charsiu (lingjzhu/charsiu), `charsiu/en_w2v2_fc_10ms` | MIT [V]; text-aware forced alignment or text-free phone recognition; English + Mandarin | Via ONNX | Directly relevant: gives phone-level alignment + per-frame phone probabilities | **charsiu-js**: wav2vec2 frame classifier on onnxruntime-web, English model ~123 MB INT8, fully client-side in browser and Node, MIT [V github.com/mnaoizy/charsiu-js, dated 2026-05-30]. Single-maintainer, young - vendor it and pin |

Latency reality: wav2vec2-base-class models (95M params) on a budget ARM phone are roughly 1-3 s for a 3 s clip on CPU via ONNX Runtime [B, unmeasured]. Acceptable because verification is per word after the child stops, not streaming. Must be measured on Kamal's actual phone (test protocol, section 6).

Capacitor / WebView: onnxruntime-web (WASM, optionally WebGPU) runs inside Android WebView; no native plugin needed except mic permission. whisper.cpp WASM works but is slow single-threaded unless cross-origin-isolated (COOP/COEP) for SharedArrayBuffer [B]. transformers.js can load the HF ONNX models directly [B]. Model download once, cache in Cache Storage/IndexedDB; "offline" then means offline after first install.

## 2. Children's speech: why it fails and what vendors do

Why it fails [B, standard literature]: higher F0 and formants (shorter vocal tract) shift away from adult training data; unstable articulation, over-/under-voicing; disfluency (sounding out "s... a... t" is *the intended behaviour* in phonics and looks like garbage to an LM); short utterances; noise and mic distance. The phonics-specific insult: ASR trained to output fluent text penalises exactly the segmented sounding-out we want.

Numbers:
- Fine-tuned Whisper on MyST child speech: tiny.en 39M params WER 15.9% (11.8% on filtered data), base.en 74M 13.9% (9.9%), small.en 244M 13.0% (8.9%); zero-shot tiny.en 28.0% [V arxiv.org/html/2507.14451]. MyST is 8-12-year-old science tutoring, sentence-length, in-domain. Our users are 4-7 isolated sounds and CVC words, which is harder per token and out of the fine-tune domain. Earlier plan noted zero-shot base ~13-14% on MyST (audit.md) - consistent only for the fine-tuned numbers, so do not quote 13% as zero-shot. Expect much worse for 5-year-olds and for L2 (Urdu-accented) speech.
- Datasets to know: MyST (public, CC-BY-NC [B]), CSLU Kids (licensed), SpeechOcean762 (5,000 utterances, 250 speakers, half children, phone-level scores from 5 experts, open [B]) - the only open set with phoneme-level pronunciation labels. Use SpeechOcean762 for sanity-checking a GOP threshold, not as proof for Urdu-accented 5-year-olds.
- Vendors [mostly B; only SoapBox page fetched, abstract only]:
  - SoapBox Labs Fluency: cloud API, ASR over a reference passage, compared to the text; built for ages 2-12; the founder's stated design principle is that a false positive (telling a kid they're right when wrong) is as bad as a false negative [V christenseninstitute.org snippet]. Accuracy figures were not in what I could read.
  - Amira: cloud ASR + reading-miscue model, scores oral reading fluency against the passage, used in-class with teacher dashboards [B].
  - Google Read Along (ex-Bolo): ASR on-device, works offline after download, ages 5+, English plus Hindi/Urdu etc. [V play.google.com / readalong.google snippets]. Their design: word-level highlighting and a gentle "reading buddy" that helps rather than fails - tolerance is in the UX. Rendered lesson: the tutor *helps on uncertainty*.
  - Ello: the product is a reading coach with a microphone, phoneme-level feedback; also human-in-loop review of hard cases [B].
  - Microsoft Reading Progress/Reading Coach: Azure speech + miscue detection with *teacher review* of every flagged word; the teacher can override [B]. This is the pattern to copy: machine flags, human decides.
  - Kidsense: on-device kid ASR SDK [B].
- Realistic accuracy: for passage reading by 8-12-year-olds, fine-tuned systems get roughly 90%+ word-level agreement with humans; for 4-6-year-olds and single phonemes nobody publishes numbers I can verify. Assume **machine "correct" is trustworthy at maybe 85-95% for real CVC words, and unusable for isolated phonemes** until we measure. Verification, not recognition, is what moves this number.

How good apps avoid punishing correct children: (a) asymmetric thresholds - accept generously, flag stingily; (b) uncertain = "let's do it together" with the model voice and a free retry, never a red X; (c) count only machine-"yes" as a mastery credit, and a machine-"no" as "unknown"; (d) human override one tap away; (e) never block progression on ASR alone.

## 3. Per-phoneme pronunciation assessment

- **Azure Speech Pronunciation Assessment**: cloud only (the SDK needs the service; no offline container for this feature that I found). en-US supports phoneme granularity, IPA alphabet, prosody (en-US only), miscue (omission/insertion; not in continuous mode over 30 s), unscripted mode with a different STT [V learn.microsoft.com .../how-to-pronunciation-assessment, updated 2026-07]. Billed at Speech-to-Text standard pricing; ~$1.32/hour is the quoted figure [V learn.microsoft.com/answers, search snippet]. Concretely: 10,000 five-second clips is ~14 hours of audio, about $14-19 per month [V toneperfect.app pricing post computes ~$14 for 10k clips]. So cost is trivial for two kids; the blockers are connectivity and child-voice privacy, not price. Child audio sent to a US cloud: COPPA/GDPR-K consent needed for any public release. Not documented anywhere I read: child-voice accuracy and pseudoword behaviour - the earlier plan's "Azure test in week 1" stays right.
- **SpeechAce**: `score/word` handles words, letters and non-words with word, syllable and phoneme quality scores; `score/text` for scripted [V api-docs.speechace.com]; cloud only; plans start ~$40/month (Basic) [V toneperfect post]. The only mainstream API that explicitly claims non-word scoring.
- **ELSA**: consumer app, adult L2, B2B API on request [B]; not a fit for 4-year-olds.
- **Offline GOP** (the key finding): yes, it is a standard technique. With a CTC phoneme model: force-align the *expected* phoneme sequence, compute the log posterior of the expected phone vs the best competing phone in its segment (GOP), plus a free-phone decode and compare. Papers on wav2vec2 + GOP/CTC for mispronunciation detection exist [B, search timed out - not cited]; Charsiu already exposes the per-frame phone probabilities needed [V]. Caveat: models trained on native adult speech penalise *accent* as error. For Urdu-first learners this is the central risk: the model will flag "v" realised as [w] (a real, taught contrast in DESIGN s2 rule 9) but also flag harmless accent. Thresholds must be set on our own recordings, per target phoneme.

## 4. Design patterns that make it workable

1. **Forced alignment against the expected item, not open recognition.** Items come from lesson JSON, so the target phoneme string is known. Outputs: expected-phone posterior, best competitor phone, duration, silence gaps. Far easier and more accurate than transcribing.
2. **Competitor set per item** (generated from the lesson): for "sat" accept /sæt/; compare to /sɪt/, /sʌt/, /sæ/, /tæt/, and "sat" with schwa epenthesis (/səæt/ "suh-at" - the 'tacked-on vowel' error from the v6 judge's card). Decision = margin between target and best competitor, not an absolute score.
3. **Three-state output, not two**: `clear_yes` / `unsure` / `clear_no`. Only `clear_yes` auto-credits. `unsure` and `clear_no` both show "let's try together" and offer the adult/tutor tap. Matches Reading Progress-style teacher review [B] and DESIGN rule 10 (no shaming).
4. **Tap-the-sound fallback** for isolated sounds: child says "sss", then the screen plays 2-3 sound options (target + a foil) and the child taps the one that matches the picture/letter. This tests *discrimination* (receptive), which machines judge perfectly (no ASR), and is a legitimate synthetic-phonics activity (DESIGN s4 block 2 "Hear it"). Isolated sound *production* stays human-judged in v1.
5. **Parent/tutor-as-judge mode** (already decided in v6): the phone shows the item; two big buttons "Got it / Not yet"; judge card with planted-error qualification. Keep it as the default for pseudowords, heart words, isolated phonemes, and the flagship until measurement says otherwise.
6. **Mic permission UX for kids**: the grown-up taps "Allow microphone" once on an adult-facing setup screen with a plain-language sentence ("The app listens only while the big mic ring is glowing; nothing leaves the phone"); child-facing screens show a mic ring that is visibly on/off; push-to-talk (hold) for under-7s, auto-VAD for adults; handle permission revoked and `getUserMedia` failures with a "checking is off, you decide" state. Android WebView needs `RECORD_AUDIO` runtime permission plus `onPermissionRequest` grant in Capacitor [B].
7. **Noise in a Pakistani home/classroom**: assume TV, fan, siblings, call-to-prayer, street. Mitigations: gain normalisation + VAD pre-gate (silero-VAD via sherpa-onnx or whisper.cpp VAD [V whisper.cpp has VAD]); a 1-second "room check" that measures ambient level and tells the adult "too noisy - move closer / switch to tutor judging"; record 16 kHz mono, keep the phone within ~30 cm; discard clips with SNR under ~10 dB as `unsure`, never `no`. Close-talk on cheap phone mics also clips on plosives - peak-normalise.
8. **Never judge what you cannot hear cleanly**: duration < 150 ms, clipping, multiple speakers → `unsure`.

## 5. Oral reading fluency (WCPM)

- WCPM = (words read - errors) / minutes (timed 60 s or prorated). The app needs word-level transcript + timing, so this is the one place open-ish ASR is the right tool: transcribe the passage reading (Whisper base.en or Moonshine via sherpa-onnx/whisper.cpp), align the transcript to the known passage with word-level edit distance (Needleman-Wunsch), count correct words, subtract substitutions/omissions, ignore repetitions and self-corrections within 3 s [B - DIBELS scoring rule], stop at 60 s.
- DIBELS 8th ed. benchmarks (Grade 1, ORF words correct, at/above goal = core/negligible risk): beginning 35+, middle 57+, end 76+; ORF accuracy 67+ / 87+ / 91+ %. NWF Correct Letter Sounds 47+ / 78+ / 87+; Words Recoded Correctly 16+ / 26+ / 28+. Intensive-support (at-risk) end of Grade 1 ORF 0-25, accuracy 0-84% [V dibels.amplify.com/docs/DIBELS8thEditionGoals_1.pdf]. Grade 2+ and Hasbrouck-Tindal 2017 norms: not fetched [unverified - fetch before putting numbers in the app].
- Use these as **reference ranges for the parent page**, not pass/fail: our Level 1-3 learners are mostly ESL and older than Grade 1. NWF is the DIBELS analogue of our pseudoword check; machine-scoring NWF is the harder, human-judged item.
- Accuracy expectation: transcript-based WCPM should land within roughly +/-5-10 WCPM of a human count on clean audio [B]; errors skew toward *under*-counting kids (omitted mumbled words). Fine for trend lines, wrong for single-session verdicts. Always show "approximate".
- Prosody: Azure's prosody (en-US only) gives break and monotone flags [V Azure doc]; offline, only crude proxies (pause length, pace variance) are feasible. Defer to v3; DESIGN rule 8 already says to report decoding and comprehension separately, so do not invent a single "fluency score".

## 6. Decision table - who judges what

| Item | Offline machine (v1) | Offline machine (v2 w/ phoneme CTC) | Online (Azure/SpeechAce) | Human (parent/tutor) |
|---|---|---|---|---|
| Receptive: pick the matching sound / word (tap) | Yes, perfect, no ASR | same | n/a | not needed |
| Isolated sound produced (/s/, /a/) | No | Weak: `unsure` heavy; stops (/t/, /p/, /k/) and "tuh" epenthesis hard; try only for fricatives/vowels with long steady state | Plausible but untested on kids | **Judge** (judge's card) |
| Real CVC/CCVC word, blended | Whisper-tiny/base word match: auto-credit only on exact match + conf margin; else unsure | Forced-align + competitor margin: better, verify on kids first | Phoneme-level, untested on kids | Fallback + spot-check |
| Pseudowords ("alien words") | **No** (snaps to real words) | Yes in principle (known phoneme string); must validate, Urdu accent risk | SpeechAce non-word scoring; Azure scripted mode - untested | **Judge (default)** |
| Heart words | No | No (irregularity is the lesson, not the sound) | No | **Judge** |
| Sentence (decodable) read | Word-level via Whisper, compare to text | same | Azure miscue | Unsure → parent |
| Passage / WCPM | Whisper/Moonshine + alignment, trend only | same | Azure continuous (no miscue flag over 30 s) | Parent spot-check weekly |
| Prosody | No | Crude proxy only | Azure en-US | Parent listening |
| Mastery gate decision (>=90%) | Never auto-promote on machine alone | Machine credits count only if validated per kid; gate needs adult confirm | n/a | **Final say** |

## 7. Recommended stack

**v1 (ship in weeks, minimal risk)**
- Platform-neutral core in JS; Capacitor Android + PWA. If staying in Godot, keep the mic path on 4.7 (godot#110337 closed for 4.6 [V]) and still run the day-1 close/relaunch recording test.
- Mic capture 16 kHz mono PCM; VAD (whisper.cpp VAD or sherpa-onnx silero) to cut silence; peak-normalise.
- **Judge mode by default** for: isolated sounds, pseudowords, heart words (v6 decisions retained).
- **Machine as witness for real CVC words only**: whisper.cpp **base.en** quantised (142 MiB on disk [V]) if the phone does it in under ~2 s, else **tiny.en** (75 MiB [V]); constrain with an initial prompt of the target word list; output `clear_yes` only on exact target match AND confidence above threshold set on the kids' own recordings; everything else `unsure`.
- Tap-the-sound discrimination for Hear it.
- Log every attempt (audio clip kept locally with parent consent, machine label, human label) - this is the dataset for v2.

**v2 (after measuring)**
- Add a **phoneme verify module**: Charsiu-style wav2vec2 frame classifier (charsiu-js English ~123 MB INT8 via onnxruntime-web [V]) or sherpa-onnx; forced alignment against lesson-JSON phonemes plus competitor margin; thresholds per phoneme from the kids' logged clips. Optional: fine-tune a small CTC head on collected Urdu-accented kid speech.
- Whisper/Moonshine retained for WCPM passages only.
- **Azure Pronunciation Assessment, opt-in online**, for adult learners and passage coaching with explicit consent; never required.
- Android on-device SpeechRecognizer: skip.

**v3**: prosody proxies; teacher dashboard with review queue (Reading Progress pattern).

## 8. Test protocol with Kamal's two kids (5 and 7), before trusting anything

Pre-registered, per child, no teaching during the test.
1. **Gold set**: Kamal records and labels 100 items per child over 3-4 short sessions (<=8 min each), mixing: 20 isolated sounds, 40 real CVC words, 20 pseudowords, 10 heart words, 10 sentences. Another adult (spouse/sibling) independently labels a random 30 to measure inter-rater agreement (the v6 "false pass" worry). Labels: correct / wrong-type (from the judge's card) / unclear.
2. **Planted errors**: Kamal also deliberately mispronounces 30 items in a child-like voice (letter name for sound, "tuh", long aaa, gaps) - to test false positives. Caveat: adult-imitated errors are easier than real child errors; treat as a floor.
3. **Conditions**: quiet room, the real room with TV/fan, phone at 30 cm, phone at 1 m, on the family phone (not a laptop), battery-saver on.
4. **Metrics** per item class: machine-"yes" precision (of items the machine credits, % that humans agree are correct) - target >=97% on real words; recall of `clear_yes` among human-correct (target >=60%, otherwise it just annoys); `clear_no` precision (target >=90% or demote to `unsure`); rate of `unsure`; latency p50/p95 (target p95 <3 s); crash/mic-permission failures over 20 relaunches (godot#110337 repro: record, close app, relaunch, record again - 10 cycles).
5. **Go/no-go**: a class graduates from human-judged to machine-credited only if precision >=97% (lower 95% CI >=92%) on >=60 items with both kids and both conditions. 5-year-old and 7-year-old are reported separately; no pooling. Pseudowords and isolated sounds are expected to fail in v1; that is the answer, not a bug.
6. **Child-experience check**: no tears, no "it didn't hear me" loops; if the child hits 3 `unsure` in a row, UI must hand over to the parent.
7. Repeat after any model, threshold, or phone change; keep gold set frozen, add a fresh held-out set each round.

## 9. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| ASR/LM "repairs" wrong answers → false pass, learner moves on undertrained | High | Verify-not-recognise; `clear_yes` only; adult confirms gate; planted-error tests |
| False negatives on correct children (pitch, accent, noise) → shame, drop-out | High | Asymmetric thresholds; unsure ≠ wrong; no red X; one-tap adult override |
| Urdu-accented English flagged as error by native-trained GOP | High (v2) | Per-phoneme thresholds from own recordings; accept /v~w/ only when lesson says not to; do not publish phoneme verdicts for unvalidated phones |
| Isolated stop consonants unscoreable (tuh/puh) | Medium | Human-judged; use word context instead |
| Cheap-phone latency / RAM / thermal throttling with base or wav2vec2 | Medium | Measure on the family phone; tiny fallback; INT8; one inference per item |
| Godot mic regression (godot#110337 closed for 4.6 but "first OK then noise" pattern was repeatable in 4.4/4.5; 111187 shows 4.5 breakage too [V]) | Medium | Day-1 relaunch test; JS/Capacitor path avoids it |
| Child audio privacy/compliance (COPPA/GDPR-K, Pakistan norms) | High if online | Offline default; Azure opt-in with adult consent; delete clips by default; disclose retention |
| Single-maintainer dependencies (charsiu-js) | Medium | Vendor + pin model hashes; keep Python charsiu as reference implementation |
| Licence traps (MyST CC-BY-NC, Moonshine non-English legacy community licence [V], wav2vec2 Apache-2.0 [V]) | Low-Medium | Record licences per model in repo; avoid non-commercial data in shipped weights |
| Offline claim: first-run model download needs data | Low | Bundle in APK or pre-seed via sideload; PWA first-load caching |
| Unverified claims in this report | Medium | Items tagged [B] need a source before they enter the app copy |

## 10. Changes vs the earlier plan (v6/decisions.tsv)

- Keep: offline-first; Azure optional/online; machines judge real words only after their own test; pseudowords + heart words parent-judged; godot#110337 as an explicit test (now known closed, milestone 4.6).
- Revise: the earlier "Azure as the pseudoword gate" idea is not supported by anything I could verify - only SpeechAce explicitly documents non-word scoring. Treat as an experiment.
- Add: tap-the-sound discrimination as a machine-perfect activity; three-state verdicts; competitor-set forced alignment as the v2 core; gold-set measurement protocol with CIs.
- Correct: WER numbers. 13-16% are fine-tuned MyST results for 8-12-year-olds; zero-shot tiny.en is 28.0% [V]; don't extrapolate to 4-7-year-olds.

## Sources

- https://huggingface.co/facebook/wav2vec2-lv-60-espeak-cv-ft
- https://arxiv.org/html/2507.14451 (Whisper tiny/base/small on MyST, Pi 5 RTF)
- https://github.com/ggml-org/whisper.cpp
- https://github.com/moonshine-ai/moonshine
- https://github.com/k2-fsa/sherpa-onnx
- https://github.com/lingjzhu/charsiu ; https://github.com/mnaoizy/charsiu-js
- https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment
- https://learn.microsoft.com/en-us/answers/questions/5608069/pricing-and-usage-of-pronunciation-assessment-feat
- https://api.toneperfect.app/blog/pronunciation-assessment-api-pricing-compared/
- https://api-docs.speechace.com/getting-started/how-speechace-scoring-works
- https://developer.android.com/reference/android/speech/SpeechRecognizer
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/processLocally
- https://github.com/godotengine/godot/issues/110337 ; https://github.com/godotengine/godot/issues/111187
- https://dibels.amplify.com/docs/DIBELS8thEditionGoals_1.pdf
- https://www.isca-archive.org/interspeech_2020/kelly20b_interspeech.html (SoapBox Fluency, abstract only)
- https://www.christenseninstitute.org/blog/soapbox-labs-gives-voice-to-the-obstacles-opportunities-of-remote-learning/ ; https://readalong.google/ (snippets only)
