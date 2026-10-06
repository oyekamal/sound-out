# Read English App — RESUME (read first in a new session)

Owner: Kamal. Started 2026-10-05. Board task #118 (project english-reading-course).
Goal: a free, offline-first app anyone on earth (age 4–60, Urdu-first ESL focus) downloads to learn to read English, one consistent LOCAL TTS voice, built on github.com/oyekamal/english-reading-course (8 levels) and reusing the Urdu Qaida app shell (~/Documents/free_work/urdu-reading-course/mobile).
Deliverable of this session: a gauntlet-looped DETAILED PLAN (not code yet).

## Bar
Features/experience: Duolingo ABC + Khan Academy Kids (store listings, reviews). Interaction: Teach Your Monster to Read (RCT). Pedagogy checklist: english-reading-course/DESIGN.md. Audio: ElevenLabs Sara clips (urdu-reading-course) as the quality bar for the local voice.

## Files here
decisions.tsv · research-01-competitors.md · research-02-local-tts.md · research-03-listening.md · research-04-pedagogy-to-product.md · research-05-stack-and-reuse.md · plan-vN.md · critics-round-N.md

## State
- research wave dispatched (5 sonnet agents) — see decisions.tsv
- 5 research reports done; licences verified by lead (Lessac research-only, Kokoro Apache)
- plan-v1.md written (Opus builder, ~12.9k words)
- critic round 1 dispatched: teacher / parent+adult / engineer / audio / claims-auditor → critics-round-1-*.md
- NEXT: apply fixes → plan-v2 → critic round 2 → loop until A wins; then publish Artifact + copy plan into english-reading-course repo
- plan-v2.md + v2-changes.md written; critic round 2 dispatched (5 fresh critics) → critics-round-2-*.md
- course issues filed: english-reading-course #1-3
- Artifact (same URL for all versions): https://claude.ai/artifact/4ENL1yCCVFgFkMb9gyW8am — rebuild: python3 build_page.py plan-vN.md plan.html then republish plan.html
- round 2 lost (all 5); v3 brief sent (two reversals: human voice L0–2, verifier off v1 path). NEXT: critic round 3 on plan-v3 → publish
- 2026-10-05 PAUSED at Kamal's request (usage 90%). Round 3: teacher A/A, parent shopkeeper A / mother B, engineer B, audio B (narrow), auditor NO (~1h fixes). plan-v3.md ADDENDUM rows 6–10 = the complete v4 brief. NEXT: resume builder (or fresh Opus) → plan-v4.md from the addendum + critics-round-3-*.md → round 4 (same 5 personas) → republish plan.html.

- 2026-10-06 session 2: plan-v4 (+Whistle patch, research-06) → round 4 LOST (teacher child B/adult A; parent mother B/shopkeeper A; global critic 3×B; engineer B; audio B; auditor NO narrow). KAMAL: app is GLOBAL, not Urdu-first. Lead decisions (9)–(12) in decisions.tsv. plan-v5 (fresh Opus builder) in progress = global-first rewrite + voice boundary at L4 + 2×2 tap-gate grid + sittings on demand. NEXT: round 5 critics on plan-v5 (teacher, parent, global, engineer, audio, auditor) → republish plan.html → when won, start week 1.
- 2026-10-06 later: plan-v5 → round 5 LOST (teacher child B/adult A; parent mother B/Recife A/shopkeeper B; global 3×B; engineer B; audio B 5th time; auditor NO, no fabrications). Lead decisions (13)–(17). plan-v6.md = CONSOLIDATION and the plan gauntlet is PAUSED (decision 17): open questions are empirical → prototype + Kamal playtest + spikes S1–S9 (listed in plan-v6 §0). Voice decision D0 = ONE voice: (a) Kokoro-only with sounds sliced from its own word renders vs (b) one human records all — Kamal listens to app/public/listen.html first. Prototype is being built from scratch in app/ (Level 1, Kokoro placeholder audio, 2×2 tap gate). NEXT: run prototype → Kamal plays → decide D0 → week-1 spikes.
- PROTOTYPE LIVE: https://oyekamal.github.io/sound-out/ (rebuild: cd app && npx vite build --base=/sound-out/ --outDir ../docs --emptyOutDir; commit docs/). Dev: cd app && npm i && npm run dev → :5317 (?fast, ?sliced). Verify: python3 tools/drive.py. Sound decision page: /listen.html. Screenshots: app/shots/. NEXT: Kamal plays (child + grown-up), listens to listen.html → D0 voice decision → fix what he reports → spikes S1–S9.
- 2026-10-06 ~14:20 SPEND LIMIT hit (resets 14:50 PKT). State: Kamal rejected Kokoro audio → decision (18) ElevenLabs, one English voice. Audio builder got through the voice audition only: blind ranking River > Bella (breathy) > Matilda (sing-song), one trial. NEXT (resume the audio brief): confirm voice with a second shuffled trial, write tools/gen_audio_el.py (with-timestamps, 3 concurrent, content-addressed cache, key from .env), re-render all Level 1 clips, slice isolated sounds from word renders, loudness −18 LUFS, rebuild listen.html + voices.html, drive.py green, rebuild docs/ and push; then plan addendum for D0 = ElevenLabs.
- 2026-10-06 ~15:50 AUDIO DONE: ElevenLabs River (eleven_v4) for all Level 1 audio, 860 clips, 21,252 chars; raw renders in content/audio_raw/; re-render: python3 tools/gen_audio_el.py plan|render|build. Sliced clean: s a t p i o k e u h f ks; sustained: m n r l v z; needs ears: d g b j w y kw. Fixed live-site audio 404 (BASE_URL). drive.py GREEN. Pages: /sound-out/listen.html, /sound-out/voices.html. Second blind voice trial could not run (Gemini keys invalid). NEXT: Kamal listens on voices.html + listen.html, plays the app; verify ElevenLabs PAYG licence; then week-1 spikes.
