# Local English TTS bakeoff vs ElevenLabs River (2026-10-08)

Goal: does any local model, driven by CMUdict phonemes, match the shipped ElevenLabs River renders? Listen blind at `bakeoff/listen.html`
(`cd bakeoff && python3 -m http.server`, open http://localhost:8000/listen.html). 32 items, 196 clips, all 24 kHz mono, -18 LUFS (pyloudnorm, peak-capped at 0.97).

**I have not listened to any clip.** Everything below is process facts plus one automatic, weak check (section 4). Kamal's ears decide.

## 1. Test set (`testset.json`)
- 12 real words: sat mug chunk full cat dog win quit fox hill what said. The brief's ship/think/queen/wind/read/pull are not in `lexicon.json` or the shipped River index, so there is no River bar for them; I took words that do have a River clip.
- 8 made-up words from `options.json` (kind=pseudo): tas mip gid cak nuzz zox quab wux.
- 12 isolated sounds: s a t p i o m n d g b r (bar = shipped `ph:*` River clips).
- Phonemes: real words from `content/cmudict/cmudict.dict`; made-up words by a letter rule to ARPAbet (no CMUdict entry). ARPAbet -> misaki/IPA in `build_testset.py`.
- Bar: `app/public/audio/<id>.ogg` from `content/audio_index.json`, decoded and re-normalised like the rest.

## 2. Candidates
Order followed, stopped at 4 rendered models (about 40 min wall time, well under 90).

| Model | Rendered | Licence (verified from file) | Install size | CPU time per word clip (median) | Phoneme control | Isolated sounds |
|---|---|---|---|---|---|---|
| Kokoro-82M `af_heart` | yes, all 32 | Apache-2.0: `kokoro-0.9.4.dist-info/LICENSE` and `misaki-0.9.4.dist-info/LICENSE` (code); weights card says Apache-2.0 (not re-fetched this run, taken from research-02, verified there). Commercial OK | venv 1.7 GB (torch CPU 0.9 GB of it) + weights 315 MB | 0.77 s | Yes: raw misaki phoneme string via `KPipeline.infer` | (a) direct phoneme: worked, but clips are 0.15-0.37 s; (b) carrier + alignment: worked |
| Piper `en_US-lessac-medium` (reference only) | yes, all 32 | Engine GPL-3.0-or-later (`piper_tts-1.8.0.dist-info/METADATA`). Voice: Lessac dataset is research-only per `plan/research/research-02-local-tts.md` s2 (not re-verified this run). **Not usable commercially** | venv 1.7 GB (shared with Kokoro) + voice 61 MB | 0.04 s | Yes: IPA ids via `phonemes_to_ids` | (a) direct: worked but very short (s = 58 ms); (b) carrier: worked |
| Chatterbox Turbo (Resemble AI) | yes, all 32 (iso = carrier only) | MIT: `chatterbox_tts-0.1.7.dist-info/licenses/LICENSE`. Commercial OK (outputs carry Perth watermark) | venv 1.8 GB + weights 2.8 GB | 5.9 s (all cores, about 530% CPU) | **No.** Text only: I fed the spelling, so made-up words are spelled, not phoneme-controlled | (a) not possible; (b) carrier: worked |
| StyleTTS2 LJSpeech (pip `styletts2`) | yes, all 32 | MIT: `styletts2/LICENSE` (code). LJSpeech-trained weights: licence not checked in a file this run; the project README asks to disclose synthetic speech | venv 1.9 GB + weights (not measured) | 0.65 s | Yes: I bypassed its phonemizer and fed my IPA ids | (a) direct: worked; (b) carrier: worked |
| Orpheus | **skipped** | not checked | needs llama.cpp + 3B GGUF; no phoneme input, text only; not worth CPU time for one-word clips | - | - | - |
| Fish/OpenAudio S1-mini, Zonos, Qwen3-TTS | not attempted (4 rendered) | not checked | - | - | - | - |

Install wall time (timings in `install_*.log`; Kokoro and Chatterbox weights were already in the HF cache, so download time is understated): venv + torch + kokoro 2 min, piper 7 s, chatterbox venv 4.5 min, styletts2 venv 5.4 min.

Safety note: the StyleTTS2 checkpoint is a pickle that `torch.load` refuses under the default `weights_only=True`. I loaded it with `weights_only=False` from the author's official repo (yl4579). A trust decision; do not ship that path without a safetensors conversion.

## 3. How isolated sounds were made
- (a) direct: the single phoneme string as model input (`s_<x>__direct.wav`). Kokoro, Piper and StyleTTS2 only.
- (b) carrier (`s_<x>__carrier.wav`): render a CVC word (sat, tap, pat, sit, dot, map, nap, dad, gap, bat, rat), force-align with the cached phoneme recogniser `facebook/wav2vec2-lv-60-espeak-cv-ft` (own numpy CTC Viterbi, `align.py`), cut the target phone. Not whisperx/MFA (not installed) and not torchaudio MMS_FA (`forced_align` is gone in torchaudio 2.9+). CTC spikes arrive late, so onsets ran into the vowel; I added a heuristic (s: cut where voicing starts; stops capped at 120 ms; nasals and r capped at 250 ms). These lengths are my guess at natural, not measured on real speech. Method (b) clips are likely to have clipped edges: judge by ear.

## 4. Automatic check (indicative only)
`per.py`: greedy decode each word clip with the espeak phoneme recogniser and compare with the CMUdict target (vowel variants collapsed). The recogniser is multilingual and noisy (it even emits tone digits), so treat this as a smoke test, not a score. 20 word clips per model, 66 target phones.

| Model | Phone error rate |
|---|---|
| ElevenLabs River | 0.35 |
| Piper | 0.44 |
| Kokoro | 0.47 |
| Chatterbox Turbo | 0.55 |
| StyleTTS2 | 0.71 (e.g. "chunk" decoded as "ty", "sat" as "sad") |

The bar itself scores 0.35, so about a third of this metric is recogniser noise.

## 5. Honest ranking (provisional, no ears, per-clip timing from this laptop CPU)
1. **ElevenLabs River**: the bar; best on the automatic check. Only closed, paid; PAYG licence still unverified (RESUME).
2. **Kokoro**: the only candidate that is both commercial-licensed and phoneme-controlled; sub-second CPU render; Apache-2.0. The previous lesson (Kamal rejected Kokoro audio 2026-10-06) still stands unless the blind page changes his mind.
3. **Piper**: marginally lower error than Kokoro on the automatic check (0.44 vs 0.47, within noise) and about 20x faster, but the voice licence blocks commercial use; useful only as a reference.
4. **Chatterbox Turbo**: MIT and natural-sounding by reputation (unheard), but no phoneme input, 6 s per word, 2.8 GB. Made-up words risk being read as English spelling.
5. **StyleTTS2**: phoneme-controlled and MIT code, but worst on the automatic check with visible mispronunciations and clipped words; LJSpeech voice is adult.

## 6. Reproduce
`python3 -m venv .venv` etc. are in `install_*.log`; scripts: `build_testset.py`, `prep_bar.py`, `r_kokoro.py`, `r_piper.py`, `r_chatterbox.py` (`.venv-cb`), `r_styletts2.py` (`.venv-st`), `align.py <model>`, `per.py`, `build_listen.py`. venvs, raw renders and models are gitignored.
