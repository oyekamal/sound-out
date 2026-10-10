# Teacher audio QA: 106 new River lines (critic pass, 2026-10-10)

Scope: the 106 `kind: "teacher"` lines in `content/teacher_lines.json` (ids in `content/ui_lines.json`, files via `content/audio_index.json` → `app/public/audio/<id>.ogg`). Every id resolved to a file; text in `ui_lines.json` matches `teacher_lines.json` for all 106. Nothing was re-rendered.

Method (all automated; nobody listened):
- **Intelligibility:** openai-whisper `small` on CPU, `language=en`, `temperature=0`, one process, nice 10. Run on clips of 1.0 s or more (83 clips). The 23 clips under 1 s got steps 2 and 3 only. WER is word-level Levenshtein after lowercasing, number-word mapping and punctuation removal. The primary column strips apostrophes, because `its`/`it's` and `Let's`/`lets` are spelling choices, not audio. The raw (apostrophe-kept) figure is shown for the two clips it flagged.
- **Duration:** ms per character (len of the text, spaces included). Silence: ffmpeg `silencedetect` at -50 dB, minimum 80 ms, plus a numpy check of edges at -50 dBFS. Truncation: RMS of the last 30 ms.
- **Loudness:** ffmpeg `ebur128` (integrated LUFS, true peak). Every clip is at least 0.4 s, so the integrated gate applies.
- **Joins:** 6 carrier+clip joins built the way `app/src/teacher.js` `seq()` plays them: carrier clip, then `wait(180 ms)`, then the model clip (`wrong()` with `carrier: thisLetterSays|thisWordSays`). Gap = trailing silence of part 1 + 180 ms + leading silence of part 2; checked again by silencedetect on the joined file.

## Summary

| Check | Checked | Pass | Flagged |
|---|---|---|---|
| Presence (id→file→text) | 106 | 106 | 0 |
| 1. Intelligibility, WER > 0.2, raw (apostrophes kept) | 83 | 81 | 2 (`itsSound`, `tipQ`) |
| 1. Intelligibility, WER > 0.2, primary (apostrophes stripped) | 83 | 83 | 0 |
| 2. ms/char outside 40–150 | 106 | 106 | 0 (range 51.9–131.4) |
| 2. Leading or trailing silence > 600 ms | 106 | 106 | 0 (no run of 80 ms+ found; numpy edges ~40 ms lead, ~80 ms trail) |
| 2. Truncation (speech in last 30 ms) | 106 | 106 | 0 (last 30 ms at -114 to -74 dBFS) |
| 3. Integrated loudness outside -18 ± 2 LU | 106 | 106 | 0 (range -18.3 to -17.9 LUFS) |
| 3. True peak above -1 dBTP | 106 | 106 | 0 (range -5.3 to -1.8 dBTP) |
| 4. Joins: gap > 400 ms | 6 | 6 | 0 (0.30 s each) |
| 4. Joins: loudness jump > 3 LU | 6 | 5 | 1 (see note; measurement artefact, RMS check passes) |

Flagged clips in the raw intelligibility column: 2 (both cleared by the primary normalisation, listed below).
Clips under 1 s (steps 2–3 only): 23.

## Flagged clips

| id | text | Whisper transcript | Reason | Disposition |
|---|---|---|---|---|
| `itsSound` | Its sound. | It's sound. | Intelligibility, raw WER 0.50 | Apostrophe-only mismatch. Primary WER 0.00. Cleared. |
| `tipQ` | q hangs down too. It always needs its u. | Q hangs down too. It always needs it's you. | Intelligibility, raw WER 0.22 | Apostrophe `it's` plus `u` heard as `you` (letter name `u` is a homophone of `you`). Primary WER 0.11, below threshold. Cleared on the metric, but a human should confirm `u` is said as the letter sound. |

Join flag (not a clip defect):

| join | Reason | Disposition |
|---|---|---|
| `thisLetterSays` + `ph:t` | Loudness jump 51.8 LU | The model clip is 0.34 s, under ebur128's 0.4 s gate, so its integrated LUFS reads -70 (gated). Speech RMS: `ph:t` -18.4 dBFS vs `thisLetterSays` -17.7 dBFS (0.7 dB). Cleared. |

## Watch list (not flagged, a human should listen)

| id | text | Whisper transcript | Why |
|---|---|---|---|
| `qNote` | The letter q is called cue. With u, it says | The letter Q is called Q. With U, it says. | WER 0.10, but `cue` came out as the letter `Q`. Same homophone risk as `tipQ`. |
| `teachBlend` | These letters keep both sounds. Say them quickly together. | …Save them quickly together. | WER 0.11. `Say` heard as `Save`; a real word-level confusion. |
| `practisedToday` | You practised today. Well done. | …practiced… (WER 0.20) | Spelling variant only (British vs US). Audio is fine. |
| `masteryMiss` | …let's practise… | …practice… | Spelling variant only. |

Other notes: all six `ph:`/`w:` model clips used in the joins sit at -18 dBFS speech RMS. `ph:s` integrates at -15.8 LUFS, so it is about 2.4 LU hot on the LUFS scale. This is inside the 3 LU join rule. These model clips are shared with other lessons and were not in the 106-line scope.

## Re-render list

None. No clip failed a check after the normalisation above. If the human listen confirms the `u`-as-`you` or `cue`-as-`Q` ambiguity, re-render these ids: `tipQ`, `qNote`. Also re-render `teachBlend` if `Say` is not clearly heard.
