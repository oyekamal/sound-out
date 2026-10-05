# Research 02 — Local English TTS for the free offline reading app

Date: 2026-10-05. Machine: 16 cores, 31 GB RAM, CPU only (T2000 4 GB not used). Scratch + all test wavs: `/tmp/claude-1000/-home-oye-Documents-free-work-personal-agent-v2/1be7ddf4-3868-4e0c-bd38-1aae7cd3186a/scratchpad/tts/wav/` (about 230 files, named `engine_item.wav`; `piperlong_*` are extra fricative tests). Nobody has listened to these by ear yet. Every quality statement below is either a published ranking, a number I measured, or a Gemini judge reading. Where it is none of these, it is marked UNVERIFIED.

## 0. Bottom line

1. **Licence is the first filter, and it changes the answer.** Every Piper English voice I tested (lessac, amy, alba) traces to a research-only or unclear dataset (section 2). Piper's engine is now GPL-3. Kokoro-82M is Apache-2.0 on code and weights, which makes it the cleanest local option.
2. **Recommended voice:** Kokoro-82M `af_heart` (American female) for the main voice. Fallback: `bf_emma` (British). The weights are small (82M), and sherpa-onnx can load Kokoro on Android, so on-device is possible later.
3. **Recommended deployment: A.** Generate every clip once on the laptop and ship Opus files. Size is about 19 MB for 10.5k words and about 36 MB for 3,000 sentences, so about 55 MB in total. On-device TTS (B) is a later option for dynamic text only.
4. **Isolated phonemes are not solved by any local model.** After trimming, the Kokoro and Piper phoneme clips were 70–200 ms of sound. Gemini Flash often heard /s/, /ʃ/ and /θ/ as t/ch/h/k. Plan to human-record the phoneme set (section 6). That is also what the Urdu project found for stop consonants.

## 1. Landscape (as of Oct 2026)

Sources: awesomeagents.ai (2026-05-23), pinggy.io (2026-08-26, Artificial Analysis Speech Arena Elo), localaimaster.com, texttolab.com, project READMEs. Cells marked "UNVERIFIED" come from my background knowledge and were not fetched in this session.

| Model | Licence (weights) | Size | CPU / Android | Quality signal | Raw IPA input? | Child voice? |
|---|---|---|---|---|---|---|
| **Kokoro-82M** | Apache-2.0 (code and weights) | 82M, about 314 MB on disk in HF cache (fp32 weights + voices) | CPU yes. Sherpa-onnx lists Kokoro, and a third-party Android app (VoxSherpa) uses it | Arena Elo about 1060 (pinggy). Several blogs call it the top small model | **Yes.** Pass an IPA string via `KPipeline.infer(model, ps, pack)`. G2P is misaki; espeak is only an out-of-vocabulary fallback | No dedicated child voice. 54 adult voices (US/UK) |
| **Piper** (VITS) | Engine: GPL-3 (`OHF-Voice/piper1-gpl`). The older rhasspy repo was MIT, and some blogs still say MIT. Voices: per-dataset, see section 2 | about 15–60 MB per voice (medium is 63 MB fp32 onnx) | Very fast on CPU. Sherpa-onnx supports Piper VITS, 48 monolingual models listed. Android works | Clear and a bit robotic. Not on the arena board | Yes, via `phonemes_to_ids(list_of_IPA_chars)`, constrained to the voice's `phoneme_id_map` | None |
| **Matcha-TTS** | MIT code. LJSpeech voice (public domain) | small | Sherpa-onnx: American English 1 female | Decent, below Kokoro | Yes (espeak phonemes) | No |
| **KittenTTS** | Code Apache-2.0. **Models are under a separate Stellon Labs Community licence, so read it before commercial use** | 15–80M ONNX variants (25–80 MB). A newer 1.7B v2 also exists | CPU real-time. Sherpa-onnx has KittenTTS and an Android TTS-engine APK | Not ranked | Not documented | 47 built-in voices. Not checked for child-like ones |
| **Supertonic** | Code MIT. **Model OpenRAIL-M**, which has use restrictions | about 99M | ONNX, runs on Raspberry Pi, 31 languages. Android is not documented in the repo. Sherpa-onnx references it | Not ranked | Not documented | Presets M3–M5 and F3–F5 (adult) |
| **Chatterbox** (Resemble) | MIT | Turbo 350M, Nano 110M, Multilingual 500M | Nano claims about 3x real-time on 8 cores. Turbo and Multilingual are GPU-oriented. No sherpa-onnx support found | Elo about 1020. Beat ElevenLabs Flash in Resemble's own tests | Not documented | Zero-shot clone, so a child voice is possible from a reference clip. Output carries a Perth watermark |
| **Qwen3-TTS** (Jan 2026) | Apache-2.0 | 0.6B / 1.7B | GPU-oriented | Unranked | No | Voice design by text prompt, 3 s cloning |
| **Orpheus 3B** | Apache-2.0 (UNVERIFIED) | 3B | GPU | Expressive | No | Clone |
| **Dia / Dia 2** | Apache-2.0 | 1.6B | GPU | Dialogue-focused | No | No |
| **Fish Audio S2 Pro / OpenAudio** | Research / non-commercial | 4.4B | GPU | Highest benchmark scores | No | Clone |
| **F5-TTS** | Code MIT, **weights CC-BY-NC** (UNVERIFIED, localaimaster agrees non-commercial) | about 330M | GPU | Good | No | Clone |
| **XTTS v2** | Coqui CPML, non-commercial | about 470M | Slow on CPU | Good | No | Clone |
| **MeloTTS** | MIT (UNVERIFIED) | small VITS | CPU OK. Sherpa-onnx lists Melo (zh+en) | Okay | No | No |
| **StyleTTS2, Zonos, Sesame CSM, VibeVoice** | StyleTTS2 MIT (the code has a GPL espeak dependency), Zonos Apache (pinggy confirms), CSM Apache, VibeVoice (UNVERIFIED) | 1–2B for the last three | GPU | Zonos Elo about 1000 | No | Clone, except VibeVoice |
| Breeze TTS 2, Voxtral, Higgs V3 | Non-commercial | 3–4B | No | Top of arena (1215, 1082, 1042) | No | No |

**Takeaways**
- Only Kokoro, Piper, Matcha, Kitten and Supertonic are small enough to run on cheap Android. Only Kokoro has both an Apache-2.0 licence and a high arena score.
- Large cloning models (Chatterbox, Qwen3-TTS, Orpheus) can imitate a child or adult reference voice, but they are slow on CPU and take no phoneme input. At build time on a laptop, Chatterbox is still feasible for 13k+ clips. I did not test it.
- Raw phoneme control, which is what pseudowords and phonics need, exists only in Kokoro, Piper and Matcha. This is the strongest argument for a Kokoro-class model.
- "Child voice" does not exist off the shelf in any of the small models. It would need cloning (Chatterbox or Qwen3-TTS) or human recording.

## 2. Licence findings that need a decision from Kamal

- Piper voices en_US-lessac: the model card points to the Blizzard 2013 Lessac dataset. Its licence text (cstr.ed.ac.uk) says "Research Purposes only", excludes "any commercial purpose, including the development, marketing, commercialisation, sale or licencing of voice synthesis" products, and forbids redistribution. I read this via WebFetch summary, not the full legal text.
- en_US-amy and en_GB-alba are fine-tuned from lessac per their model cards. Whether a fine-tune inherits the restriction is a legal grey area. Alba's own dataset is CC-BY-4.0 and amy's data licence just says "See URL".
- The Piper engine is GPL-3. A shipped Android app that bundles it would need to be GPL. Shipping only audio files avoids that, but I have not checked whether the voice licences allow redistributing generated audio.
- Kokoro: Apache-2.0 for weights. Its training data included synthetic and public-domain audio per the model card, but I did not verify that claim line by line. This is an assumption, not a legal review.
- Whatever voice is chosen, keep a short LICENSES.md in the app repo naming model, version and licence.

## 3. Bakeoff method and what I could and could not install

- Piper 1.8.0 installed with `pip install piper-tts` into a venv. It bundles espeak-ng, so no apt was needed. Voices downloaded from rhasspy/piper-voices on Hugging Face: lessac-medium, amy-medium, alba-medium.
- Kokoro 0.9.4 plus misaki 0.9.4: a plain `pip install kokoro "misaki[en]"` hung in dependency resolution, so I used a `--system-site-packages` venv with `--no-deps` and installed the small dependencies by hand. Model `hexgrad/Kokoro-82M`, run on CPU with 8 threads, voices `af_heart` and `bf_emma`.
- **Not working:** the bundled `espeakng-loader` 0.2.4 hard-fails on this machine ("Error processing file .../runner/work/.../phontab") and aborts the Python process. It happens even when I call `espeak_Initialize` directly with a correct data path. I did not debug it further because of the time box. I disabled the espeak fallback instead. Effect: Kokoro's text path cannot pronounce out-of-vocabulary words (all four unknown pseudowords produced no audio), but the IPA path works fine. A system `espeak-ng` binary was not available and I did not try sudo/apt.
- Not installed or tested (time box): Matcha, Kitten, Supertonic, Chatterbox, MeloTTS, any sherpa-onnx runtime, any Android build. Everything about these rests on READMEs only.
- Judge: reused `urdu-reading-course/scripts/listen_judge.py` (`ask`, `audio`) read-only with its Gemini key. The first run used the repo's default Pro model and was far too slow (about 90 of 230 clips in 14 minutes), so I killed it and reran with `gemini-2.5-flash` on a subset: all phonemes, letters, pseudowords, sentences, and 5 of the 10 words, for kokoro af_heart, kokoro bf_emma, piper lessac and piper alba (amy skipped). Each clip was peak-normalised and padded with 150 ms of silence before upload. I did not install faster-whisper (not present; the Urdu notes say Whisper cannot judge clips this short anyway).

## 4. Measured results (CPU, single clip, after warm-up)

| Engine / voice | Sample rate | Avg gen time, single word | Avg raw word length | Raw wav size per word |
|---|---|---|---|---|
| Piper lessac-medium | 22.05 kHz | 0.05 s | 0.52 s | about 23 KB |
| Piper alba-medium | 22.05 kHz | 0.06 s | 0.65 s | about 29 KB |
| Piper amy-medium | 22.05 kHz | 0.06 s | 0.60 s | about 27 KB |
| Kokoro af_heart | 24 kHz | 0.76 s | 1.32 s (includes padding silence) | about 64 KB |
| Kokoro bf_emma | 24 kHz | 0.47 s | 0.77 s | about 37 KB |

- Sentences: Piper 0.11–0.16 s to generate 1.3–2.2 s of audio. Kokoro 1.0–1.5 s to generate 1.9–2.8 s.
- Throughput: Piper about 20 words/s, Kokoro about 1.3–2 words/s on this laptop. 10.5k words take about 9 minutes in Piper or about 2 hours in Kokoro single-threaded. Running 4 processes in parallel brings Kokoro to roughly 30–40 minutes (estimate, not measured). Both are trivially fine for a one-off build.
- Opus check: after `silenceremove` and `libopus 24k mono`, 10 words averaged **1,772 bytes (Kokoro af_heart)** and 1,526 bytes (Piper lessac). Durations after trimming are about 0.5 s.

## 5. What the pure-phoneme output looked like

Phoneme input method: Kokoro takes an IPA string directly (`s`, `m`, `p`, `æ`, `ʃ`, `θ`). Piper takes a list of IPA symbols and maps each through the voice's `phoneme_id_map`. I measured active duration (samples above 3% of peak) and judged by ear-proxy (Gemini Flash).

**Kokoro af_heart**
- Total clip about 0.5–0.7 s, but active sound only about 90–190 ms. The rest is silence the model pads in.
- No vowel was appended by the judge's count (`extra_vowel` false for s, m, p, a, ʃ, θ). But the judge heard /s/ as "ch", /ʃ/ as "d", /θ/ as "k", /æ/ as "h"; /m/ and /p/ were identified correctly. Because a 100 ms burst of noise is hard for any listener, this may be the judge as much as the model. I cannot tell without a human listening.
- Control cases worked as expected: `sə` and `pə` came back flagged as having an "uh" vowel.
- Slowing it down (speed 0.6) lengthened /s/ to 480 ms, but the judge then heard "h".

**Kokoro bf_emma**: active 100–290 ms; judge heard a/s/ʃ/θ/m as f/l/t/t/p. Letter names were less reliable too (a→I, b→G, p→C), so I would not use bf_emma without a human check.

**Piper (all three voices)**
- /p/ 104–116 ms, /s/ 70–450 ms (lessac only 70 ms and very quiet, peak 0.098 before normalisation), /ʃ/ 80–220 ms, /θ/ 100–170 ms. Autocorrelation showed no pitched component in the /s/ and /p/ clips, so I believe no vowel was added in them, but this is a rough signal measure.
- Repeating the symbol (`ssss`, `ʃʃʃʃ`) only reached 190–260 ms. `mmm` gave 685 ms with a slight vocalic release flagged by the judge.
- The judge heard Piper /s/ as "t" and /p/ as "k"/"t" (alba) — effectively all stops and fricatives became "t/k".

**Conclusion for phonemes:** local models generate something, but not a trustworthy, teachable /s/ /m/ /p/. The same is true of the stop consonants, which cannot be said in isolation without a vowel, and for which even human teachers use a short release. I recommend human recording for the 44 phonemes, with the TTS used only for words.

## 6. Words, letters, pseudowords, sentences

Gemini Flash readings (single run, short clips, treat as a noisy screen, not a score):

- **Letter names via IPA:** Kokoro af_heart heard 6/6 correct (A, B, M, P, S, W). Piper lessac heard 3/6 (b and p both heard as B, m as N). Piper alba 4/6.
- **Real words (5 tested):** Kokoro af_heart 4/5 (ship heard as "chef"). Kokoro bf_emma 2/5. Piper lessac 1/5 (sat→"sunset", ship→"chip", through→"crew"). Piper alba 2/5. I suspect the very short Piper clips (0.4–0.6 s) may be partly a judge problem, but they are clearly less intelligible than Kokoro.
- **Pseudowords via IPA:** Kokoro af_heart got strag and fraim (heard "frame", should be /fɹeɪm/ so ok), vop→"vob", chote→"Chode", blim fine but naturalness 1. bf_emma: blim→"glow", the rest roughly right. Piper: vop→"foll"/"fop", chote→"toot"/"chute", blim→"blin"/"wun". Piper's text path (espeak) was no better.
- **Sentences:** all four voices transcribed the child sentence and the adult sentence correctly (digit "6" for "six" is a judge formatting quirk). Naturalness 4/5 for all except af_heart child sentence, which got 2 (unexplained; needs a human listen).
- Kokoro af_heart peaks 0.2–0.4 and Piper 0.02–0.48 on the single phoneme clips, so always peak-normalise in the build pipeline. Piper sentence output was already normalised to 1.0.

**Ranking from this evidence:** Kokoro af_heart > Kokoro bf_emma ≈ Piper alba > Piper lessac/amy. The sample is small and the judge is a Flash model on sub-second audio. A 30-minute human listening session on the saved wavs would settle it.

## 7. Recommendation

**Voice:** Kokoro-82M `af_heart`, American female. Reasons: Apache-2.0 weights, best intelligibility in my sample, IPA input for pseudowords and controlled pronunciations, and a runtime path to Android through sherpa-onnx. **Fallback:** Kokoro `bf_emma` if a British voice is wanted for Track B (needs a human spot-check first), or Piper alba if the licensing question is answered in Kamal's favour and speed matters.

**Gaps in this choice**
- No child voice exists. For Track A the same adult teacher voice is the realistic option. Cloning a child-like voice with Chatterbox is possible but untested and carries watermark and consent concerns.
- A consistent single voice across thousands of items is a Kokoro strength (fixed voice pack, no sampling drift). Piper is the same.

**Deployment: A (pre-generate at build time).**
- Words: 10,500 × about 1.8 KB = about 19 MB (Opus 24 kbps mono, trimmed). At 16 kbps it would be about 13 MB.
- Sentences: say 3,000 × 4 s × 3 KB/s = about 36 MB.
- Letters, phonemes, UI prompts: under 2 MB.
- **Total about 55 MB**, easy to ship or lazy-download by track. Fits offline on cheap phones with no inference cost, no model download, and no risk of GPL or runtime crashes on 2 GB RAM devices.
- Why not B now: Kokoro at about 82M params is heavy for a 2 GB-RAM phone (the ONNX is hundreds of MB at fp32; int8 builds exist in the sherpa-onnx releases but I did not test them), and nothing in this app needs on-the-fly speech except future user-typed text. Keep B as an option for later. The same Kokoro voice would run through sherpa-onnx so the voice stays consistent.
- Build pipeline: one script reading the word list, generating with fixed voice and speed, `silenceremove`, peak-normalise to -3 dBFS, then Opus. Keep a manifest (text, voice, model version, sha) so clips can be regenerated.
- Regenerating a 10.5k word set costs about 2 hours single-process, so there is no reason to compromise on build-time quality.

## 8. Needs a human recording

1. **All 44 isolated phonemes**, especially stops (/p/ /b/ /t/ /d/ /k/ /g/), which cannot be said purely, and the fricatives /s/ /ʃ/ /θ/ /f/ /v/, where TTS clips were 70–200 ms of noise that a judge could not identify. Voiced continuants /m/ /n/ /l/ /r/ may be acceptable from TTS after an ear check; Kokoro /m/ and /p/ were heard correctly once.
2. **Short vowels** (æ, ɛ, ɪ, ɒ, ʌ, ʊ): Kokoro /æ/ was heard as "h" by the judge. Must be checked by ear and probably recorded.
3. **Blending demonstrations** (s-a-t drawn out, "ssaat") — TTS does not do stretched blending reliably.
4. **Pseudowords**: use IPA input and check each by ear. Vop/chote/blim were misheard in both engines, so a human spot-check is needed for the whole pseudoword list, not a sample.
5. **Any word the judge or Kamal flags**: ship/chef type errors suggest a checking pass over the 10.5k words. A cheap approach is forced-alignment or a Whisper pass at build time, plus a human listen to the 5% with lowest confidence.
6. **A child voice**, if Track A should sound like a child, and **UI prompts in other languages** (the Urdu app already has ElevenLabs Sara; that stays).

## 9. Unverified and open

- No human has listened to any of these wavs. The Gemini results are single-run, used a Flash model, and the Urdu project already found short consonant clips are hard for it.
- The espeak-ng failure in `espeakng-loader` was not resolved, so Kokoro's own handling of unknown words was not tested.
- Matcha, Kitten, Supertonic, Chatterbox, MeloTTS, Orpheus, Dia, Fish, F5, XTTS, StyleTTS2, Zonos, CSM, VibeVoice were not run. The licence cells marked UNVERIFIED need a model-card check before use.
- sherpa-onnx on a real Android device (RAM, speed, int8 Kokoro) was not tried. Whether sherpa-onnx's Kokoro API accepts raw IPA input is not documented in what I fetched (their docs page said nothing about phoneme input).
- The Piper-voice licence reading (research-only) comes from a WebFetch summary of the Blizzard 2013 page and the HF model cards. It needs a human or lawyer to confirm.
- TTS Arena numbers come from secondary blogs (pinggy.io's Artificial Analysis Elo list). I did not open the leaderboard itself.

## Sources

- https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/ (Elo, licences)
- https://awesomeagents.ai/tools/best-open-source-voice-tts-2026/
- https://localaimaster.com/blog/best-local-tts-models
- https://texttolab.com/blog/open-source-text-to-speech
- https://huggingface.co/hexgrad/Kokoro-82M
- https://github.com/OHF-Voice/piper1-gpl
- https://huggingface.co/rhasspy/piper-voices (model cards for lessac, amy, alba under `en/`)
- https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html
- https://github.com/k2-fsa/sherpa-onnx and https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/index.html
- https://github.com/KittenML/KittenTTS
- https://github.com/supertone-inc/supertonic
- https://github.com/resemble-ai/chatterbox
- https://github.com/QwenLM/Qwen3-TTS
- https://github.com/shivammehta25/Matcha-TTS
