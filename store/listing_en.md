# Google Play listing, English (default, en-US)

Sources: store/NAME-ASO.md (keywords), plan/bar/*.json (competitor listings), Urdu Qaida listing (format). Limits: title ≤30, short ≤80, full ≤4000. Counts are in the "Counts" section.

## Title (23/30)
Sound Out: Read English

## Short description (77/80)
Phonics with Tilo the capybara. Learn to read English. Free, offline, no ads.

## Full description
(Paste everything between the two lines. Do not paste this heading or the notes below.)

-----
Learn to read English from the first letter sound. Sound Out is for children from about age 4 or 5, and for teens and grown-ups. It is free and works offline. It has no ads, no account, no login and no internet permission, so nothing you do leaves the phone.

It uses synthetic phonics: you learn the sound each letter or letter group makes, blend the sounds into real words, then read short texts. A teacher's voice speaks every step, so a child who cannot read yet never has to read a menu.

WHO IT IS FOR
• Children from about age 4 or 5. Tilo the capybara is their guide. He shows what to do, sounds words out with them and cheers when they get one right.
• Teens and grown-ups who want to read English. Pick "A grown-up" for the same course on plain screens, with no mascot.
• Anyone learning English as another language. The teacher speaks English, and pictures and icons show what to do.

HOW A SITTING GOES
• Hear a new sound, see its letter, trace it.
• Blend sounds into words. Tap a word to hear it sound by sound.
• Pick the right word from answer cards. In the child track, many cards carry a real picture.
• Build words from letter tiles.
• Meet tricky words that do not follow the rules, and spot the tricky part.
• Read short texts made only from sounds you have learned, and listen to short illustrated stories.
• Sounds and words you miss come back for review on later days.

THE COURSE
108 lessons in 7 levels. It starts with single letter sounds, then moves on to sounds that team up, long vowels and longer words, then to reading and writing practice with fuller texts. Each level ends with a "Show what you know" check, and the next level opens when you pass it.

A TEACHER THAT WAITS
• Press and hold any button to hear what it does.
• Tap the ear button to hear the instruction again.
• If you pause, the teacher says it again and points at what to tap. No lives, no timer that punishes.
• A "days practised" counter that never resets, so a missed day costs you nothing.

WHAT IT DOES NOT DO
• It does not listen to you. Sound Out never uses the microphone, so it cannot grade your pronunciation. You tap your answers, and for reading aloud a grown-up decides how it went.
• It does not teach speaking or other languages. It teaches reading, and works best next to real books.

PRIVACY AND CHILDREN
• No ads, no in-app purchases, no account, no analytics, no tracking.
• Nothing in the app links out of the app, and nothing asks a child for personal information.
• Everything stays on your phone. The app has no internet permission and sends nothing anywhere. Deleting the app erases all progress.
• The teacher's voice is AI-generated and recorded in advance, so nothing is generated online.

Made by one developer, Kamal, in Pakistan. The lessons come from a free, open course whose full text is public: github.com/oyekamal/english-reading-course. Questions or a wrong sound? Write to oyekamalkhan@gmail.com.
-----

## Counts (checked with len() on 2026-10-10, after the Tilo update)
Title 23/30 · short description 77/80 · full description 2934/4000 (the text between the two rules). Remaining open items are the release gates below, not copy.

## Category and settings
Education · Free · No ads · No in-app purchases · Phone screenshots: store/screenshots/phone/ (8, 1080x1920) · Title note: the critic suggested "Sound Out: Learn to Read"; the title stays as set by Kamal (NAME-ASO.md: "English" is the ESL keyword), and "Learn to read English" opens the full description and the short description.
Tags (pick up to 5 that Play offers): Language learning · Reading · Alphabet · Kids · Education.
Content rating target: Everyone. Target audience: includes children (see PLAY_CONSOLE_CHECKLIST.md §3).
Contact email: oyekamalkhan@gmail.com (PROPOSED, Kamal to confirm; same address as the Urdu Qaida listing). Website: https://oyekamal.github.io/sound-out/ . Privacy policy URL: https://oyekamal.github.io/sound-out/privacy.html

## Keywords carried (from store/NAME-ASO.md)
Primary: learn to read (title-adjacent, short + full), learn to read English (full, first lines), phonics (short + full), reading app for kids (children line + full), English reading for beginners (full).
Secondary: ESL / English as another language (full), offline (short + full), alphabet sounds and letter sounds (full), blend / blending (full), decodable (full, "made only from sounds you have learned" carries the idea), adults (short).
Not used on purpose: "research-proven", "best", "#1", "award-winning", "learn English" (the app teaches reading, not speaking; a "learn English" install would be a mismatch and a 1-star risk).

## Claims audit (every sentence that states a fact, and where it is checked)
| Claim | Evidence | Status |
|---|---|---|
| Free, no in-app purchases | no billing library in app/package.json or the merged manifest | verified 2026-10-10 |
| No ads, no account, no analytics | app/src has no ad, auth or analytics code (grep, store/families_fixes.md §Method) | verified |
| No internet permission, sends nothing | merged release manifest lists no INTERNET permission; no fetch/XHR/WebSocket in app/src | verified |
| Never uses the microphone | no getUserMedia/SpeechRecognition in app/src; no RECORD_AUDIO in manifest | verified |
| Progress only on the phone, deleting the app erases it | IndexedDB (app/src/db.js) + two tiny localStorage flags (app/src/gate.js:39-42); allowBackup=false | verified |
| Voice is AI-generated, pre-recorded | ElevenLabs River renders shipped as .ogg (plan/RESUME.md, decision 18) | verified |
| 108 lessons in 7 levels | content/lessons/ has L1 14, L2 14, L3 18, L4 16, L5 16, L6 16, L7 14 = 108 | verified against content, RE-CHECK on the final build |
| Level checks unlock the next level | app/src/home.js level cards ("Opens when you pass the Level N check") | verified for L1-L4; RE-CHECK L5-L7 |
| Press and hold speaks a button; ear button repeats; idle re-prompt | app/src/teacher.js (HOLD_MS, ear, idle ladder) | verified in code |
| days practised never resets | app/src/home.js title "never resets" | verified |
| Tilo the capybara shows what to do, sounds words out, cheers on right answers (child track) | app/src/tilo.js, teacher.js events, session.js beat; shots in store/android-test/tilo-in-app/ and store/screenshots/phone/ | verified 2026-10-10 (Tilo r1-r8, plan/RESUME.md) |
| Many child-track answer cards carry a real picture | app/public/img/words/pictures.json (512 pictures), app/src/optionset.js; 52 ambiguous words get labels or speaker-only cards instead | verified; the text says "many", not "every" on purpose |
| Short illustrated stories | content/lessons/*.json listen blocks, scene pictures (shoot_pictures.py) | verified L1; later levels RE-CHECK |
| No link leaves the app, nothing asks a child for personal information | grep in store/families_fixes.md Method; no `<a>`, href, mailto in app/src | verified 2026-10-10 |
| Stickers for finishing a sitting | app/src/home.js, `STICKERS` in ui.js | listing does not mention them, fine |
| "Grown-up" track: plain screens, no mascot | plan Track B + home.js (no pebble on track B) | verified |
| No second language needed | core voice is English only; "Help in your language" chips are placeholders (onboarding.js:7,31-37) and are not advertised | verified |
| Sounds and words you miss come back | app/src/scheduler.js (Leitner cards) | verified in code |

## Release gates that touch this text
1. Tilo is live in the child track (done, see claims audit).
2. Levels 2-7 lesson audio: 2,252 clips were still missing on 2026-10-10 (plan/RESUME.md). Re-check the count before publishing; do not publish with placeholder beeps; Play can reject a "broken or incomplete" app and the "108 lessons" line would mislead.
3. The child-facing "Prototype: ..." strings (store/families_fixes.md F2) were removed by the app lane; grep once more on the final build.
4. Trademark check for "Sound Out" and "Tilo" (store/NAME-ASO.md says not done).
5. If the optional language-help packs ship as downloads, the "no internet permission" lines and the Data safety answers change (store/PLAY_CONSOLE_CHECKLIST.md §3).

## What's new (first release)
First release. Sound Out teaches reading English from the first letter sound: 108 lessons, a voice teacher, free and offline.
