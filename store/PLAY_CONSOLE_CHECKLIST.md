# Play Console checklist · Sound Out: Read English (com.oyekamal.soundout)

Modelled on the Urdu Qaida checklist (urdu-reading-course/store/PLAY_CONSOLE_CHECKLIST.md) and its research/16 Play rules (official Google pages, fetched 2026-09-19). Copy for the listing is in `listing_en.md`; the policy page is `app/public/privacy.html`. Written 2026-10-10, before the final app and the screenshots exist. Policy wording changes often: re-read the live pages named below before pressing Publish.

## 0. Status at a glance
| Item | Status |
|---|---|
| targetSdk | **36 (fixed 2026-10-10).** `app/android/variables.gradle` was compileSdk 35 / targetSdk 35; now 36 / 36. Verified: merged release manifest (`app/android/app/build/intermediates/merged_manifest/release/processReleaseMainManifest/AndroidManifest.xml`) says `minSdkVersion=23`, `targetSdkVersion=36`. Same AGP 8.7.2 + Gradle 8.11.1 setup the Urdu app shipped with at 36. Rebuild the AAB before upload (the current `app-release.aab` in `app/android/app/build/outputs/bundle/release/` was built at 35). |
| 16 KB page size | No native libraries (`unzip -l app-release.aab` shows 0 `.so`), so the rule does not apply. Re-check after the final build. |
| Version | `versionCode 1`, `versionName 0.1.0` (`app/android/app/build.gradle:10-11`). Bump `versionCode` for every upload; use a real `1.0.0` for the production release. |
| Permissions | Merged release manifest requests none (only the Capacitor-internal `DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`). No INTERNET, no AD_ID, no RECORD_AUDIO. |
| Privacy policy | Written: `app/public/privacy.html` (copied to `docs/privacy.html` too). Live only after the next `git push` of `docs/` (GitHub Pages). URL: https://oyekamal.github.io/sound-out/privacy.html . Check it loads before submitting. |
| Signing | Upload keystore `~/.kamil-harness/keys/sound-out-upload.keystore`, env `~/.kamil-harness/keys/sound-out.env` (not in git; back up to the private `oyekamal/app-signing-keys` repo). |

**Where privacy.html lives and why.** The Pages build is `cd app && npx vite build --base=/sound-out/ --outDir ../docs --emptyOutDir`, which deletes everything in `docs/` first. Anything in `app/public/` is copied into the build output, so the master copy is `app/public/privacy.html` and survives every rebuild. `docs/privacy.html` is the same file committed so the URL works as soon as the commit is pushed. The Android build (`npm run build:android`) also copies it into the APK assets, where nothing links to it; harmless, and usable later for an in-app privacy screen.

## 1. Account (Kamal)
- [ ] Personal developer account ($25 once), identity verified. Say in the Console which account this app goes on (the Urdu Qaida one, or Orenda/Taleemabad as an organisation: organisation accounts skip the 12-tester gate in §5).
- [ ] Developer name shown on the listing: "Muhammad Kamal" (matches the privacy policy) or the organisation name. Decide.
- [ ] Contact email on the listing: proposed `oyekamalkhan@gmail.com` (same as Urdu Qaida, and printed in the description and the policy). **Kamal to confirm or give another.** Phone number: leave blank.

## 2. First upload
- [ ] Build: `cd app && npm run aab` (runs `build:android`, `cap sync`, then `gradlew bundleRelease` with the upload key). Output: `app/android/app/build/outputs/bundle/release/app-release.aab`.
- [ ] Copy to `~/.kamil-harness/keys/releases/sound-out-<versionName>-vc<versionCode>.aab` (the naming Urdu Qaida used).
- [ ] Check it: `unzip -l <aab> | grep -c '\.so$'` → 0; `jarsigner -verify -verbose <aab> | tail -3` shows it is signed; `bundletool dump manifest` shows targetSdkVersion 36 and no `<uses-permission>` beyond the Capacitor one.
- [ ] Upload to a **Closed testing** track first (§5). Enrol in Play App Signing when asked (upload key = the keystore above).

## 3. Declarations (answer exactly like this)

### 3.1 Data safety form
"Does your app collect or share any of the required user data types?" → **No.**
Why this is true under Google's definition: learner data is stored on the device and never transmitted off it (no network permission, no network code, no SDKs). Data that stays on the device is not "collected".
Everything else on the form is then skipped by the Console. If it still asks:
| Question | Answer |
|---|---|
| Data collected | None |
| Data shared | None |
| Encrypted in transit | Not applicable (nothing is transmitted) |
| Users can request data deletion | Not applicable; uninstalling or clearing app storage deletes everything |
| Security practices: independent security review | No |
| Families policy / children's data | App targets children but collects no data |
**Change triggers:** any network request (optional language-help pack downloads from plan-v6 §3 count), any analytics or crash SDK, an in-app export, or a contact/mailto link all need the form, `privacy.html` and `listing_en.md` re-checked.

### 3.2 Other App content forms
| Form | Answer |
|---|---|
| Privacy policy | https://oyekamal.github.io/sound-out/privacy.html |
| Ads | **No**, the app contains no ads |
| Advertising ID | **No**, the app does not use advertising ID (no AD_ID permission in the manifest) |
| App access | **All functionality is available without special access** (no login, no location, no paid tier). Note for reviewers in the optional instructions box: "Levels open as lessons and checks are completed; no account needed." |
| News app | No |
| Government app | No |
| COVID-19 contact tracing / status | No |
| Financial features | My app doesn't provide any financial features |
| Health features | No |
| Social features / user-generated content | No (nothing is shared between users) |
| Gambling | No |
| Account deletion | Not applicable (the app has no accounts) |
| Photos and videos / sensitive permissions | None requested |
| Actors, AI-generated content policy | The app does not generate content with AI. Its teacher voice was AI-generated before release and ships as audio files; the listing and the privacy policy both say so. |

### 3.3 Content rating (IARC questionnaire)
Category: **Reference, news, or educational**. Answers:
| Question | Answer |
|---|---|
| Violence / blood / fear-inducing content | No / No / No |
| Sexual content or nudity | No |
| Profanity or crude humour | No |
| Controlled substances (drugs, alcohol, tobacco) | No |
| Gambling or simulated gambling | No |
| Users can interact or exchange content | No |
| Shares the user's location | No |
| Digital purchases | No |
| Unrestricted internet access / web browser | No |
| Ads | No |
Expected result: **Everyone** (ESRB), PEGI 3, USK 0, IARC 3+. Check the lesson texts and stories for anything scary before answering (Listen & Talk stories, `content/lessons/`): the stories should be everyday and gentle.

### 3.4 Target audience and content (Families policy)
- Age groups: select **5 and under, 6-8, 9-12, 13-15, 16-17, 18 and over.** The child track is the main use and is designed from about age 4, so "5 and under" is the honest answer. Selecting it has no extra cost for this app because it has no ads, no data and no SDKs. (Kamal's call: if you would rather not appear for under-5s, drop that band only if the app is not actually designed for them; do not drop it to dodge review.)
- "Does your app appeal to children?" **Yes.**
- This puts the app under the **Families policy requirements** (https://support.google.com/googleplay/android-developer/answer/9893335). What that means here:
  - No ads of any kind: true.
  - No advertising ID, no behavioural data, no unapproved SDKs: true (no SDKs).
  - API level target: 36, done.
  - Any link out of the app, and any contact or donate action, must sit behind a parental gate. At the moment the app has none (store/families_fixes.md: 0 hard violations). If a contact or donate button is added later it needs the grown-up gate specified in `families_fixes.md` §Gate.
  - Store listing and graphics must be appropriate for children and must not mislead: see the claims audit in `listing_en.md`.
  - Privacy policy link required: done (§0).
- Mixed audience: because grown-ups use the app too, Google treats it as targeting children and adults. Since nothing is collected there is no age-screen requirement.
- Store listing "Contains ads": No.

### 3.5 Teacher Approved (optional, after launch)
Not required to publish. Eligibility notes (verify the current criteria at the Families policy page above and in Play Console → Policy → App content → Target audience; Google invites or lets you opt in once the app complies):
- Must comply with the Families policy: yes by design.
- Wants a clearly educational app for children, age-appropriate content, no ads or data collection, and a quality experience (stable, no broken features). Today's blockers: placeholder audio in Levels 2-7, "Prototype" strings, non-working language chips, placeholder pictures (see `families_fixes.md`).
- Strengths to cite when applying: free, offline, no ads, no data, voice-led so non-readers can use it, a structured synthetic-phonics sequence, grown-up track.
- Do not claim "Teacher Approved" anywhere until the badge is granted.

### 3.6 Store settings
App category **Education**. Tags: see `listing_en.md`. Email: see §1. Website: https://oyekamal.github.io/sound-out/ . Free. Countries: all (the listing is global-first, not Pakistan-first). Default language en-US.

## 4. Store listing (copy from this folder)
- [ ] `listing_en.md`: title, short description, full description (the text between the two rules only).
- [ ] App icon: `store/icon-512.png` (512x512, RGB PNG, no alpha; Play accepts it, convert to RGBA only if the upload form complains). Hi-res source `store/icon-1024.png`. Feature graphic: `store/feature-graphic.png` (exactly 1024x500, RGB, no alpha, ok).
- [ ] Screenshots: **NOT DONE on purpose** (after the app is finished). Phone: minimum 2, aim for 8, 9:16, 1080x1920 or larger. Optional 7-inch and 10-inch tablet sets. Urdu Qaida tooling: `urdu-reading-course/scripts/make_store.py`, `store_judge.py`. First screenshot = the benefit (child tapping the answer with Tilo), not a menu.
- [ ] Release notes: the "What's new" text at the end of `listing_en.md`.

## 5. Closed testing gate (new personal accounts)
Rule (support.google.com/googleplay/android-developer/answer/14151465): a personal developer account created after 13 Nov 2023 must run a **closed test with at least 12 testers opted in continuously for 14 days** before it can apply for production access. Organisation accounts are exempt. If the Console dashboard on the app shows "Apply for production access", the gate applies to this app.
- [ ] Testing → Closed testing → Create track. Add **at least 12 testers** (an email list or a Google Group; use 15-20 so a drop-out does not reset the count).
- [ ] Share the opt-in link; every tester opts in and installs. Ask each to open the app at least once and to give a rating or a note.
- [ ] Keep them opted in for **14 uninterrupted days**. A tester who leaves can break the streak.
- [ ] After day 14: Dashboard → **Apply for production access**. Answer the questions (how testing went, who the app is for, what you changed from feedback). Google answers in about 7 days. Budget about 3 weeks from first upload to Production.
- [ ] Promote the tested release to Production, countries all, price Free.
- [ ] Testers can be the Urdu Qaida testers, teachers, and parents from the tinkering-rnd and homeschooling groups.

## 6. Release steps (in order)
1. Pass every release gate below.
2. Bump `versionCode` (and `versionName`) in `app/android/app/build.gradle`; commit.
3. `cd app && npm run aab`; copy the AAB to `~/.kamil-harness/keys/releases/` with the version in its name; run the checks in §2.
4. Play Console → Create app: name `Sound Out: Read English`, default language English (United States), App, Free, accept the Developer Program Policies and US export laws.
5. Fill App content (§3), Store settings (§3.6) and Main store listing (§4).
6. Closed testing → Create release → upload the AAB → accept Play App Signing → release name `1.0.0 (N)` → paste the release notes → countries → Review → Start rollout.
7. Run the 14-day test (§5). Fix bugs found by testers, upload a higher `versionCode` to the same track, and keep testers opted in (a new build does not reset the 14 days).
8. Apply for production access, then Production release.
9. After launch: add per-language store listings (NAME-ASO.md lists the order), consider Teacher Approved (§3.5).

## 7. Release gates (nothing here is in Play Console; all must be true first)
- [ ] **Tilo is in the child track** (listing mentions Tilo; `app/src/ui.js` still draws Pebble).
- [ ] **Levels 2-7 lesson audio is real**, not placeholder beeps (`content/audio_needed*.json`; blocked on an ElevenLabs top-up, Kamal's decision).
- [ ] The "Prototype: ..." and "...placeholders" strings are gone (`families_fixes.md` F2) and no child-facing screen says "not in this prototype".
- [ ] The "Help in your language?" chips are removed or really work (F3).
- [ ] Word pictures are real art, not grey shapes (picture lane).
- [ ] An in-app privacy entry exists behind the grown-up gate (F1).
- [ ] **Voice licence**: confirm the ElevenLabs plan used to render the shipped audio allows commercial distribution in an app (README flags "PAYG commercial licence terms" as open). Keep the invoice and terms on file in case Google asks (Intellectual Property policy). Same check for the Kie/nano-banana images used for Tilo and word pictures.
- [ ] **Trademark search** for "Sound Out" (in apps and class 9/41) and "Tilo" (USPTO/WIPO/EUIPO), per NAME-ASO.md and design/character/names.md. Backups for Tilo: Moku, Tolu.
- [ ] Re-run the Families audit against the final `app/src` (`families_fixes.md` §Method) and re-read the live Families policy page.
- [ ] `listing_en.md` claims audit all "verified" against the final build (108 lessons, level unlocks, hold-to-hear).
- [ ] Final QA on a real phone and on the Play emulator: cold start, offline, back button, rotation (the app is portrait only), TalkBack.
