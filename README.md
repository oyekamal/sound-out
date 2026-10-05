# Sound Out — learn to read English, any age, offline

Play title: **Sound Out: Read English** · package `com.oyekamal.soundout` · see `store/NAME-ASO.md`.

A free, offline-first Android/PWA app that takes anyone (age 4 to 60, Urdu-first learners especially) from the first letter sound to reading real text. Built on the open course [english-reading-course](https://github.com/oyekamal/english-reading-course) (8 levels, synthetic phonics) and on the shell of the shipped [Urdu Qaida](https://github.com/oyekamal/urdu-reading-course) app.

## Status (2026-10-05)
Planning complete through three gauntlet-loop critic rounds. **No app code yet.** Next session: write `plan/plan-v4.md` from the addendum at the end of `plan/plan-v3.md`, run critic round 4, then start the build (week 1 spikes).

## Read in this order
1. `plan/RESUME.md` — where things stand, how to resume
2. `plan/plan-v3.md` — the plan (13 sections) + addendum = v4 brief; rendered page: https://claude.ai/artifact/4ENL1yCCVFgFkMb9gyW8am
3. `plan/decisions.tsv` — every decision with why and evidence
4. `plan/research/` — 01 competitors · 02 local TTS bakeoff · 03 listening/ASR · 04 pedagogy→product · 05 stack and reuse
5. `plan/critics/` — rounds 1–3, five personas each (teacher, parent+adult, engineer, audio, auditor)
6. `plan/bar/` — App Store listings of the apps we benchmark against

## Decisions that need Kamal (plan §0 / §10)
- **Voice:** one human teacher voice for Levels 0–2 (no TTS yields a clean isolated phoneme), Kokoro `af_heart` (Apache-2.0, local) from Level 3. Piper's English voices are research-licence only.
- **Listening:** no speech gate in v1; print-to-spoken-word tap gate; on-device verifier in v1.1.
- Accent (General American), phoneme speaker, test phone, and the rest of the D-list in §10.

## Build
`python3 plan/build_page.py plan/plan-v3.md plan.html` renders the plan page.
