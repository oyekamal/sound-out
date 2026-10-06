# research-06 — Whistle (Cactus Compute) spike, 2026-10-06

**What it is:** https://huggingface.co/Cactus-Compute/whistle — on-device speech-to-text, one 16.9 MB `.cact` file, CPU only, no GPU, Apache-2.0, released 2026-10-02. Engine = Needle (https://huggingface.co/Cactus-Compute/needle3), platform folders include `android-arm64`, `android-armv7`, `ios-arm64`, `wasm`, `wasm-component`, linux/mac/windows. Features: transcription (EN + 6 EU languages, ≤30 s per pass, silence → empty string), **word timestamps with per-word probability**, **keyword biasing**, encoder embeddings (80 ms frames). Python: `pip install cactus-needle`; `needle.transcribe(path, language="en", keywords=[...], word_timestamps=True)`.

**Test (lead, this machine, CPU, 16 cores):** 20 Kokoro `af_heart` bakeoff clips resampled to 16 kHz. Keywords = target words + foils (`sat sit sap pin pan pit ship shop think thing vop blim strag fraim chote`). Clips kept in `whistle-spike-clips/`.

| clip | plain | with keywords | word prob | note |
|---|---|---|---|---|
| sat | Sat | Sat | 0.63 | 8.9 s first call (engine warm-up), then 0.1–0.25 s per clip |
| pin | PIN | Pin | 0.73 | |
| ship | **Shabbat** | **Ship** | 0.58 | biasing fixed it |
| think / light / garden / station | correct | correct | 0.84–0.98 | |
| cake | **Take** | Take (not in keywords) | 0.83 | onset error passes with high confidence |
| vop (IPA) | VAP | VAP | 0.72 | pseudoword; vowel heard as /æ/ (may be Kokoro's rendering) |
| blim / strag | Blim / Strag | same | 0.59–0.60 | pseudowords recognised when in keywords |
| fraim | Frame | Frame | 0.78 | homophone; spelling is irrelevant for a reading gate |
| chote | Chode | **Chote** | 0.46 | biasing fixed it, low prob |
| /s/ /m/ /p/ isolated | garbage | garbage | 0.44–0.55 | **cannot judge isolated sounds** |
| letter names s, b | Yes / BA | Yes / BA | | cannot judge letter names |
| "The cat sat on the mat." | exact | exact | 0.92–1.0 per word | word timings usable for WCPM |
| "The bus to the market leaves at six." | exact ("6") | exact | 0.49–1.0 | |

**What this changes in the plan**
- The v1.1 verifier candidate becomes Whistle + keyword biasing (target + the gate's three foils as keywords) + per-word probability → `clear_yes` (transcript = target, prob ≥ θ) / `unsure` / `clear_no` (transcript = a foil). This is the "verification not recognition" design with an off-the-shelf engine; no CTC scoring to write. Word timestamps give WCPM for Level 5 passages for free.
- Still true: isolated sounds and letter names stay human/tap-judged; `cake→take` shows a high-confidence onset error passes if the foil list misses it, so the foil list must come from the gate (onset/vowel/final) and anything outside target+foils is `unsure`, never `yes`.
- Unverified: child speech (all clips are adult TTS), Urdu-accented speech, cheap-Android latency and RAM (needle binary + 16.9 MB model; wasm folder exists for the PWA), beam settings, keyword-biasing strength, licence of the engine binary (repo says Apache-2.0; confirm the platform folder's LICENSE).
- Spike plan (weeks 1–2, 2 days, does not gate v1): build android-arm64 `needle` into a Capacitor plugin (JNI to the C API); record 30 CVC words × 3 speakers (Kamal's two kids + one adult) × 2 takes; measure `clear_yes` precision on correct reads and on planted onset/vowel/final errors; p95 latency on the test phone. Go bar: ≥97% precision, ≤1.5 s p95.
