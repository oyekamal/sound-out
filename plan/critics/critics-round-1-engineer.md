# Critic round 1: engineer

Verdict: **B**. The plan ships a Play internal-test AAB in week 8 only if the listening plugin is cut or the audio pipeline is thinned, because the content and audio pipelines are sized from 4 hand-picked lessons and a regex word count, while week 1 and week 7 each carry 6+ jobs that depend on people and a device that are not confirmed.

## Single biggest gap

**The "parser" is not a parser job.** Markdown to typed JSON for 108 lessons is sold as `build_content.py --strict` plus "dozens of heading edits" (C14), with a week-1 exit of 4/4 hand-picked files (L1.02, L3.05, L4.03, L5.01). Everything downstream (decodability gate, audio render list, mastery, oracle) reads its output, and unlike listening it has no cut path. The ★ fields in §6.2 (`errorClasses`, `anchors`, `keyTerms`, `reteach.step`) do not exist in the markdown.

## Defects

**1. Schema does not match the course files** (§6.2, §6.3 gate 5, §8 wk2 exit "100% of lessons have check, read, listen").
Counted in `english-reading-course/course/level-*/lessons`:
- "Listen & Talk" appears in 0/16 L5, 0/16 L6, 0/14 L7 lessons (L2 13/14, L4 15/16). The plan's exit check and rule 7 require 100%.
- "Track B" appears in 0/16 L6 and 0/14 L7 lessons. `decodability audit` appears in 0 L5, 0 L6, 1 L7. The `text{A,B}` schema and gate 5 assume otherwise.
- Word lists in L2–L4 are plain `**label:** a, b, c` lines or backticked lists (L3.05 Blend/Check; L2.03 Check). Pipe tables exist only in L1.02 and L5. The parser rule "pipe tables become word lists" covers neither.
- L1.02 nests `### 7. Read it` inside `## Sitting D`; L7.03 has "Meet the move", two "Close reading" blocks and a fill-in table. Neither fits the templates.
Fix: pick one machine-readable form (fenced YAML block per step, added to the 108 files by a script plus review) and fail the build on any lesson without it; do not infer from prose. Verify: `--strict` over all 108 lessons plus 7 mastery checks, then re-render each JSON back to a lesson and diff. Run this in week 1, not 4 files.

**2. The 90% gate contradicts the lessons and the oracle test** (§2.3 row 4, §6.2 `pass:0.9`, §6.9 item 3).
Pass bars found in L1–L4 prose: `≥4/5` x19, `≥10/11` x11, `≥3/3` x3, `≥2/2` x2, `≥9/11`, `≥7/8`, `≥5/6`. `≥4/5` is 80%, so the planned "deliberate 80% run must hit reteach" would pass 19 lessons. `≥9/11` is 81.8%, and the plan itself writes "Checks 9/10" in one row and 5+5+1=11 items in another. L1.02's Check has 3 real words (repeated) and its pseudo list already uses 5 of the few strings possible from s, a, t, so "≥3 fresh sets of 5" (E11, gate 4) cannot exist for L1.02–L1.03. Fix: one signed-off bar table; relax the fresh-set rule for L1.02–L1.03. Verify: unit test enumerating every reachable score per lesson against the stored bar; oracle 80% run asserted per lesson, not globally.

**3. Audio counts and the IPA path are unproven** (§4.1–4.3).
- research-05 §3 counts words from blockquotes, tables and bold/italic only. Check/Blend/Spell words in L2–L4 sit in plain or backtick text (L3.05, L2.03), so "5,763 words" and "+1,000 pseudowords" are undercounts of unknown size (a rough re-scan finds hundreds of extra distinct tokens per level). Only sentences carry a ±25% caveat.
- research-02's 4 IPA pseudowords: vop→"vob", chote→"Chode", blim naturalness 1. Expect >2% human re-records. Q4 asks Kamal to hear all ~1,360 pseudowords plus Q3 fails, the lowest 5% and 200 per pack, with Q3 acknowledged as noisy.
- Lexicon `p` uses standard IPA (æ, eɪ, dʒ); misaki/Kokoro use their own symbols (single-letter diphthongs, fused affricates; verify). No mapping layer is planned.
Fix: week-1 render of all 44 GPC strings and 100 pseudowords through the real IPA path; recount words with a tokenizer over every learner-facing line. Verify: every token resolves to a clip id; compare with 5,763.

**4. The Kokoro build environment aborts, it does not fail** (§4.2 step 2).
research-02 §3: `espeakng-loader` "aborts the Python process" and the venv was hand-built with `--no-deps` after pip resolution hung. "The build fails unless pron.json holds an override" cannot be implemented by catching an exception; an OOV hit with the fallback on kills a 3-hour batch, with it off yields silence. Fix: pinned Docker build with system espeak-ng; misaki fallback off, `❓` a hard error. Verify: render 20 known-OOV words; process exits non-zero with a report, zero silent files.

**5. Clip playback and storage are unmeasured on the target** (§4.1, §6.8).
- Plan: one concatenated Ogg Opus file per lesson, sliced with `Blob`, the whole bundle pre-decoded for 150 ms tap-to-sound. At 3 KB/s a 0.66 MB lesson is ~220 s, ~42 MB decoded (48 kHz float32); an L6 session (18 MB / 16 lessons) is ~70 MB. The whole app budget is 150 MB on a 2 GB phone.
- How bytes reach JS is unstated: `@capacitor/filesystem` `readFile` returns base64 over the bridge; `fetch(convertFileSrc(...))` avoids it.
- IDB `packs` row and files on disk can disagree, with no launch reconcile. The PWA (SW + Cache API) is a second delivery pipeline; `vite-sw-plugin.js` caches whole files by name, not offset bundles.
Fix: decode per clip with an LRU, stat files at launch, use `fetch`. Verify: `dumpsys meminfo` in an L6 session on a 2 GB phone; p95 tap-to-sound over 200 taps.

**6. Native speech plugin: effort, RAM, 16 KB, size** (§5.2, §6.7, §8 wk1/wk6, §0 "about 27 MB").
- Nobody has run sherpa-onnx; research-05 says its model sizes are "from memory" and sherpa's minSdk is unchecked.
- research-03 [V]: whisper tiny ~273 MB RAM, base ~388 MB. Plan budget with ASR: under 300 MB total including WebView.
- "Constrained to target + foils" and "exact match above confidence" are not shown to be available for sherpa Whisper (hotwords are a transducer feature).
- targetSdk 36 makes 16 KB alignment of native `.so` files a Play upload gate, not a "confirm".
- Two ABIs of onnxruntime plus JNI add tens of MB (my estimate), so "about 27 MB" stops being true.
- Realistic effort on a real phone: 6–10 working days, inside a week shared with three other spikes.
Fix: take it off the critical path (ship E6b and E21); run it as a branch gated on RSS and alignment checks. Verify: `bundletool get-size total` per ABI; `zipalign -c -P 16 4`; `dumpsys meminfo` after 20 decodes.

**7. No schema or content migration story** (§6.4, §4.2).
`db.js` hard-codes `VERSION = 1` and "repairs" missing stores by bumping `d.version + 1`; no migration has ever shipped. The plan adds four stores and new profile fields. Clip ids are `sha1(voice+model+text+ipa)`, so any text edit changes ids, and `gpc.json`/lexicon are global while L3+ packs are built and downloaded separately, so bundled L0–L2 and a later pack can disagree on the GPC set. Fix: `contentVersion` in every pack manifest and on `mastery`/`cards`; real `onupgradeneeded` steps; reject incompatible packs. Verify: finish L1.05 on build N, upgrade to a build with that lesson edited and ids shifted, assert progress intact.

**8. Schedule inputs are not in hand; some numbers are unsupported** (§6.8, §8, §12.3).
- `adb devices` here lists nothing; the SDK has only x86_64 emulator images (API 34, 36). Opus on Android 10 WebView, armeabi-v7a and 2 GB RSS cannot be checked on those. The 2 GB phone and the speaker are assumptions.
- Week 1 holds audition, 44x3 recordings, plugin on two phones, three models, kid sessions, parser spike, Opus check. Week 7 holds perf, a11y, RTL, backup, PWA, store assets, signed AAB, critic round 2 and G1–G4.
- §6.8 is headed "measured on the 2 GB phone"; research-05 §5 is a budget table, and no Urdu cold-start number exists in any report.
- Plan ~11,200 clips / ~75 MB vs research-05 ~9,960 / ~71 MB; the 1,000 pseudowords are the plan's own "round number".
- Reuse line counts (449 / 2,702 / 391 / 313) match `wc -l`. But `path.js` (39.6 KB), `learner.js` (52.3 KB), `onboarding.js`, `drills.js` are tied to the Urdu unit model (`C.units`, `n < 12`); a level/lesson/sitting/track state machine, 21 exercise types and 5-stage placement are new work, not edits.
Fix: name the phone and speaker before week 1; split week 1 into 1a (parser on all 108, IPA test) and 1b (speaker, listening); move G1–G4 to week 8. Verify: dated device list in the repo.
