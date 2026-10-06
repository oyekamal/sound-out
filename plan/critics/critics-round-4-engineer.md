# Critic round 4, engineer: plan-v4.md

**Verdict: B.** The Levels 0-2 recording chain (33-50 h) is serial behind an option generator that cannot produce the course's own L1.03-L1.04 checks, and the audio engine as sized needs about 300 MB of PCM against a 150 MB budget. Any fix lands in weeks 2-5, and the cut list cannot touch either.

## Single biggest engineering gap: the sprite sizes contradict the plan's own table (§6.3 vs §4.1)

§6.3 says the always-decoded core sprite is "about 90 s, about 8.6 MB" and a lesson sprite is "about 150 s, about 14 MB". Opus at 24 kbps is 3 KB/s (§4.1).
- **Core.** Its contents per the §4.1 table are 47 phonemes 0.12 MB, UI lines 1.8 MB, partial blends 0.6 MB and Urdu lines 5.4 MB. That is 7.9 MB, or about 2,640 s. Decoded at 24 kHz Float32 (96 KB/s) it is about 253 MB, 29 times the plan's figure.
- **Lesson sprites.** Sound Teacher audio less core is 22-33.5 MB over about 28 lessons. That is 0.8-1.2 MB each, 260-400 s, 25-38 MB decoded, so 1.8-2.7 times the plan's figure.
- **Total.** Core plus the 2-sprite LRU is about 300-330 MB, against a "<150 MB" budget (§6.5) and a "<40 MB audio" claim (§6.3). `decodeAudioData` peaks above steady state, and decode time for 260-400 s sprites is unbudgeted.
- **Access pattern.** The warm-up shows up to 3 cards from other lessons (§3.7). Each is a 25-38 MB decode with an LRU of 2, so it thrashes. A tapped L1 word inside an L3 sentence plays its "own lexicon voice" (§4.4), which means another lesson's sprite,.
- The week-1 test measures only gap jitter, so it passes with toy sprites.

**Fix.**
- Sprites of 20-30 s (about 2-3 MB decoded), keyed by step.
- Core limited to the 47 phonemes plus about 20 UI lines. Urdu lines load per screen.
- A decode-ahead rule: the next step's sprite is decoded during the current step.
- Review cards served from a per-card short sprite.

**Verify.** Week 1 on the test phone: build sprites at real size from the §4.1 counts, then check `dumpsys meminfo` and decode ms for the worst screen (L3 sentence with L1 taps; review warm-up with 3 lessons).

## Defects

**1. Option generator cannot satisfy the rule at L1.03-L1.05 (§3.3, §6.2 gate 3, §4.1 counts).**
- Evidence. I enumerated every CVC/VC/CV string over the letters taught by L1.03 (s,t,p,n / a,i) against `/usr/share/dict/american-english`: 48 strings, 32 real, **16 made-up**. A check needs 5 made-up items × 4 words = 20 distinct made-up words with no repeat, before any "fresh set" for re-checks. L1.04 has 40.
- The course's own L1.03 items fail the one-position rule. Made-up *tas* has no made-up final-only neighbour, *pas* has no vowel-only, and real *nap* has no real final-only (L1.03 lines 129-130).
- Fix. Before the L0-L1 freeze, decide what relaxes (fewer items, shared options, mixed lexicality) and re-derive the 1.1% figure.
- Verify. Run gate 3 on the course's own L1.03-L1.08 real/pseudo lists now.

**2. Timing claims have no instrument and one is arithmetically over (§1.1, §3.2, §3.4, §8).**
- Evidence. The plan stopwatches 5 children on Sittings B and C "before the text is frozen in week 2". No E5, E6d or repo exists until weeks 2-4.
- A p90 of 5 samples is the maximum.
- Sitting A alone is 7:30 of 8:00 (§3.4). Sitting C adds 4 blends and a spell step; the course allots ~15 min per sitting (L1.05).
- "First sound ≤90 s" (G0) never says which clock. Launch screen (~10 s) + quick-start (~25 s) + 1:10 is about 105 s.
- Fix. Define the clock, paper-prototype B and C in week 1, move quick-start after the first sound.
- Verify. A week-3 stopwatch from process start.

**3. Recording chain (§4.5, §8).**
- Evidence. `voice_studio.py` is 547 lines. Urdu kinds are hard-coded in `build_items` (:58-120), capture is `getUserMedia` with echoCancellation true (:353), and saving goes through ffmpeg and `import_recordings.process_array` (:497-503, 16 kHz). Five of the seven listed changes are a rewrite. None adds upload to the engineer (24 h review) or a live Q1, so "retake in the same session" cannot be enforced and retakes pile into week 9.
- Load. Week 1 has about 535 clips. That leaves 4,400-6,900 for weeks 2-5, or 29-46 h, which is 7-11.5 h per week with a single speaker, before generator review gates.
- "150 clips/h" is unsourced, and a 200-clip word pilot does not measure sentences, stops or retakes. No week freezes L2 text, but week-4 and week-5 sessions record it.
- Fix. Pilot sentences and stops too, freeze L2 in week 3, add upload plus a live Q1.
- Verify. Clips/h per type in week 0.

**4. Reader QA misses the clips that matter (§4.4, §4.2).**
- Evidence. research-02 §6: made-up words misheard in both engines (vop→"vob", chote→"Chode") and real "ship" heard as "chef", 1 of 5. §4.4 gives the reviewer 10% of a pack plus 100% of 398 made-up words. The 1,000-2,000 L3-L4 options (about half made-up) are neither. A mispronounced answer clip makes a correct reader fail the item.
- Gemini triage is the judge that misheard /s/ /ʃ/ /θ/ /æ/ (research-02 §5). The pinned Docker image is untested (research-02: pip hung, espeakng-loader aborted).
- Fix. 100% human review of every made-up option, or ASR round-trip plus the reviewer on the lowest 20%. Build the image in week 0.
- Verify. Plant 20 wrong clips, count catches.

**5. DB and backup list is incomplete (§6.4).**
- Evidence. `db.js:44` `fix()` coerces any track outside `child|adult|heritage` to `child` on every read, so Track B adults silently become children. Backup `SCHEMA` is a whitelist, and LIMITS entries alone do not back up new stores (mastery, packs, helper). Progress `units` is `dict(unitRec, 40, /^\d{1,2}$/)`: lesson ids fail the key regex, and 115 lessons exceed the 40-key cap, which `break`s silently. The planned fixture uses "L1.02 keys", so it passes.
- Every home render runs `stats`, `streak`, `pearls` (`learner.js:41-43`), each a `getAll` plus recursive scrub: ~18k attempt rows after a child year, unbudgeted.
- Fix. Add these sites to the table; fixture with 61 lessons and 20k attempts; keep counters in the progress record.
- Verify. Round trip plus render ms on the test phone.

**6. Device tests and the loopback rig (§6.3, §6.5, §6.6).**
- Evidence. D24 buys one Android 10 phone, but file-transfer resume must pass on "Android 10 and 13". The loopback needs a USB interface or a line-out recorder, and neither is purchased. A USB interface reroutes the audio output, so it does not measure the speaker or headphone route kids use. minSdk 23 WebViews older than Chrome 74 ignore `AudioContext({sampleRate})`, doubling memory.
- Fix. Buy a second phone and a 3.5 mm cable; set a WebView floor.
- Verify. Run on an old-WebView device.

**7. Whistle spike (§5, §8 week 1, research-06).**
- Evidence. The spike is "JNI to the C API". research-06 never opened the C API; it ran Python. The spike takes 2 days plus recruiting Kamal's children and recording 180 takes. It takes the same build agent that week 1 already loads with the parser, ipa2misaki and the loopback test. A plugin merged for the spike pulls `RECORD_AUDIO` into the app manifest through the manifest merger, contradicting "no microphone" and Data Safety.
- Fix. Move it to week 9 slack or a side branch that never merges before v1.
- Verify. A manifest-diff check in CI.

**8. Cut list and slack (§8).**
- Evidence. Items 1-7 are small features. The real schedule risk is audio and generator work, which is "never cut". Item 9 says "L4 pack" but L3-L4 is one pack (§4.1). Week 8 holds 8 deliverables plus human tests. Week 9 holds pickups, lost-gate re-runs, D37, and the L3-handover fallback (+10 h of recording, §9), which also has to be QA'd.
- Fix. Add cuts that save audio hours (option sets to the §4.1 low end) and decide the handover in week 4.
- Verify. An hours-per-week table.

**Checked, not defects.**
- §4.1 clip and MB totals reconcile, and the install sums (44-59, 47-69) follow from them. The inputs are estimates, notably ~27 KB per picture from Urdu's 872 KB / 32 images.
- A crude `Check` regex over L1-L4 parses 55 of 62 lessons. L5-L7 parse 0 of 46.
