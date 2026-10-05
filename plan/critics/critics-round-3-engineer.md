# Critic round 3, engineer: plan-v3.md

**Verdict: B.** The audio and content chain (speaker, freeze, record, QA, pickup) starts after week 1, the audio engine's central assumption fails in the installed Capacitor code, and week 8 holds all gauntlet, store, test and pilot work with no slack. The cut list (§8) never touches audio or content, so a slip lands there.

## Single biggest engineering gap: the audio engine (§6.3, §4.3.6)

v3 swaps per-clip files for one Opus sprite per lesson: `play(id)` sets `currentTime`, a timer stops it, and gaps are "authored in the timeline". It calls this "kept from Urdu", but the Urdu engine (`content.js:5-19`) never seeks. It drains its queue on `ended` (line 6), tests `currentTime === 0` in the watchdog (line 19), and `rebuild()`s (line 8). All three break.

1. **Range.** Capacitor 7.6.9 `WebViewLocalServer.java:369-386` answers any `Range` with 206 and a `Content-Range: bytes X-…` header, but returns the whole stream from byte 0; there is no `skip()` in that path. Seeking works only if Chromium has buffered the whole file, which is not guaranteed on a 2 GB phone or after `rebuild()`. The week-1 "p95 <20 ms" test cannot see this, and the plan names no way to measure acoustic accuracy (JS cannot).
2. **Bleed.** A `setTimeout` stop 50-100 ms late (Lottie jank) leaks the next entry's onset past the 80 ms tail pad (§4.3.2). A stale timer from clip A can pause clip B; the plan has no cancel rule.
3. **Queue/watchdog.** Timer-stopped clips never fire `ended`, so `drain` never runs. The `currentTime === 0` test is meaningless at a non-zero offset, so a healthy element is rebuilt.
4. **Gaps.** `play()` after a seek adds variable latency. A 350 ms (or ≤150 ms, see defect 7) gap cannot be held by timers on one element. This is the s-a-t then "sat" moment.
5. **Cross-lesson clips.** Warm-ups, Leitner review (§3.7) and the 44 phonemes need clips from other lessons' sprites. The plan has no answer.

The per-clip fallback fails the same gap test and adds block waste (research-05:188: +60%).

**Fix:** fetch the sprite, `decodeAudioData` once (~8 MB Float32 per ~40 s), and schedule `AudioBufferSourceNode.start(when, offset, dur)` on the audio clock. That removes Range, timers, watchdog and gap jitter. research-05:188 proposed Blob slicing; v3 dropped it unexplained.
**Verify:** loopback recording on the test phone, 200 sequences under a Lottie-heavy screen, p95 of the actual inter-phoneme gap against the authored value.

## Defects

**1. Recording kit and schedule (§4.5, §8, §4.4).**
- The named tool `voice_studio.py` calls `getUserMedia({echoCancellation:true, noiseSuppression:true})` and records MediaRecorder webm (`:353-357`); its importer outputs 16 kHz (docstring line 4). The plan wants 48 kHz WAV, no suppression. Suppression is worst on isolated /s/ /f/ /θ/.
- 250 clips/h appears only at `v3-changes.md:11`; it has no source.
- §4.4 has "the recording engineer"; §8 has no such person, and the speaker works remotely, alone.
- Week-2 sessions record L1 words and foils while the foil and pseudoword generators land the same week; pseudowords need native review (C2, weeks 2-5) first.
- One GA reviewer covers speaker scoring, ~1,600-2,300 phoneme/pseudoword/foil/demo clips, Kokoro samples, `pron.json` and 720 pseudowords.

Fix: rewrite the recorder; run a 200-clip pilot with the real speaker in week 0; record phonemes and L1.02-L1.06 first, foils after review; name the engineer and a second reviewer. Verify: measured clips/h; energy above 8 kHz survives in the decoded final Opus.

**2. Parser yield ≥95% (§6.2).** 95% of 78 L1-L5 lessons allows 3 failures. A crude regex (Check section has real, pseudo and a bar) passes **56/78 = 72%**. It fails all 16 L5 lessons (word-work lists, "(4/6 = pass)", "≥5/8", L5.03:175-179) plus L1.01, L2.14, L3.04, L3.18, L4.15, L4.16. At least three grammars exist: L1.04 "Real words (15, cumulative):", L2.03 "5 real words:", L3 "Real: … Pseudo: …". Bars are "≥90%?" with no denominator (L3.05:55). L5 comprehension is free-response (L5.03:114-120), and no MCQ authoring is commissioned (C11 is L6-L7). Under §3.6 a gate with no machine-judged items is "not scored as passed", so L5 gates cannot pass. Fix: yield per level; commission L5 MCQs now or move L5 to v1.1 explicitly. Verify: machine-judgeable item count per L5 gate.

**3. "No native plugin" is false (§0, §6.1).** The Urdu app ships `@capacitor/filesystem`, `haptics`, `share` (`feel.js:46`, `main.js:147`, `practice.js:39`, `teacher.js:77`). Packs need Filesystem, and `downloadFile` is deprecated since 7.1.0 for `@capacitor/file-transfer` (`definitions.d.ts:597-603`). "No .so" holds; "no native code" does not. Fix: list the plugins, add file-transfer. Verify: kill-and-resume mid-download on Android 10 and 13.

**4. Numbers (§4.1, §4.4).** I recomputed the clip counts (4,642-6,954) and MB columns; the arithmetic holds. The inputs do not:
- Shell "~8 MB (estimate)" comes from the Urdu shell, whose 32 images total 872 KB. C6/C12 add ~315 pictures, about +8.5 MB at Urdu's per-image size, so ~14-17 MB.
- "About 3,000 Kokoro clips" (§4.4) conflicts with the table: L3-L4 is 2,978-4,712 and L5 is 1,688-2,610, so ~4.7k-7.3k and review hours are low by up to 2.4×.
- Urdu voice "~600 clips" versus C9 (~300 lines) plus C10 (~600 lines) = ~900, and the Sara licence is unresolved.
- research-02 shows IPA pseudowords misheard (vop→"vob", chote→"Chode"); the reject, re-IPA, new-id, re-review loop is unscheduled.

Fix: measure the shell with C12 stubs; recompute review hours. Verify: gate 9 on the corrected baseline.

**5. Migration and backup (§6.4).** The listed changes are incomplete. In `backup.js`: `profiles.track` is `oneOf('child','adult','heritage')`, so Track A/B is silently dropped and an adult returns as a child; `unit: int(0,12)` in attempts/cards/profiles/wpm; `cards.idx: int(0,500)` against L1's 1,066 words; `UI_KEYS` is a fixed whitelist that drops new settings; `LIMITS[s]` is undefined for new stores. Optional fields drop without error, so the planned "L1.02 key plus apostrophe" test passes while data is lost. Fix: a field-by-field table and a deep-equality round trip on a fully populated fixture. Verify: restore preserves track, shapes, PIN toggle.

**6. PWA caching undesigned (§8 week 7).** Urdu `sw.js:71` serves only build-manifest paths, so downloaded packs bypass it. Its eager set is hard-coded to Urdu audio folders; one failed eager fetch fails the install, so a 26-38 MB English base is fragile. `persist()` is called blind (`main.js:51`, result ignored); non-persisted Cache storage is evictable on 16-32 GB phones. `rangeOf` does handle 206, but copies the full body per seek. Fix: runtime pack cache, visible `persisted` state, lazy base. Verify: offline L1 after simulated storage pressure on Chrome Android.

**7. Self-contradictions an agent will implement literally.**
- Gaps: ≤150 ms (§3.3 E5 repair) versus 350 ms (§4.3.6, "same for E6d repairs").
- E6d "all options share the onset", yet `at/it/ap` and `pick:{"at":["it","ap"]}` (§6.2) include "it". Gate 3 would reject the plan's own sample.
- Vowel-initial pseudowords (ast, att) have no onset to share; L3-L5 polysyllables have no foil rule.
- §6.6 says auto tests are "green before week 4", but E6d, the reducer and the oracles are built in week 4.

Fix: one rule table; generate the §6.2 sample from the generator. Verify: `npm run content` passes it.

**8. Schedule and cut list (§8).** The cut list stops at week 5 and its "never cut" list is the whole core. Week 1 has seven deliverables, week 4 has E1-E12, stroke scoring, reducer, village and a critic round, and week 6 has L5 plus signed-manifest packs. "A lost gate re-runs next week" has no week 9. Human tests (non-reader for G0, 10+10 icons-only, sibling, parent-absent, 3-adult audit) have no recruitment slot. Fix: a weeks 6-8 cut list that names audio and L5, and a recruitment line in week 0. Verify: dated recruit list by week 2.
