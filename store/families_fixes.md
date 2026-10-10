# Families-policy audit and the exact fixes needed

Audit of `app/src`, `app/index.html`, `app/capacitor.config.json`, `app/android/app/src/main/AndroidManifest.xml` and the merged release manifest, 2026-10-10 (snapshot at commit d4f7d8c plus the working tree). Policy: https://support.google.com/googleplay/android-developer/answer/9893335 . Another agent owns `app/src`; **nothing under `app/src` was changed by this audit.** The one app-side edit made was `app/android/variables.gradle` (targetSdk 36, see PLAY_CONSOLE_CHECKLIST.md §0).

## Result
- **Hard Families violations: 0.** No outbound link, no data collection, no contact or donate control, no ads, no permissions.
- **Findings to fix before submission: 7 (F1-F7).** None is a policy violation today; F1-F3 are release blockers (privacy access, misleading child-facing text), F4-F7 are hardening.
- The user's claims hold: IndexedDB only, no network calls, no analytics. Nothing contradicts them. One future plan does (F3, language-help downloads).

## Method (re-run this on the final code)
```
cd /home/oye/Documents/free_work/sound-out
grep -rn -E "https?://|fetch\(|XMLHttpRequest|WebSocket|sendBeacon|window\.open|location\.(href|assign|replace)|mailto:|tel:|target=|<a |href=|navigator\.(share|clipboard)|iframe|gtag|analytics|firebase|sentry|mixpanel" app/src app/index.html
grep -rn -E "getUserMedia|SpeechRecognition|MediaRecorder|geolocation|Notification|localStorage|sessionStorage|indexedDB|document\.cookie" app/src
grep -n "uses-permission" app/android/app/build/intermediates/merged_manifest/release/processReleaseMainManifest/AndroidManifest.xml
grep -n "dependencies" -A12 app/package.json
```
Results on 2026-10-10:
- Network/links: the only `http://` strings are namespace URIs in `content/` XML; **zero** hits in `app/src` and `app/index.html` for fetch, XHR, WebSocket, sendBeacon, window.open, location changes, mailto, anchors or hrefs. Audio is `new Audio(\`${BASE}audio/<id>.ogg\`)` from the app's own files (`app/src/audio.js:35`, `app/src/placeholder.js:32`).
- Storage: IndexedDB database `sound-out` (`app/src/db.js:2-24`: settings, profiles, progress, cards). `localStorage` is used for exactly one flag, `so-gate-demo-<profileId>` (`app/src/gate.js:39,42`). No cookies, no sessionStorage.
- Sensors: no getUserMedia, SpeechRecognition, MediaRecorder or geolocation anywhere (the `mic` icon in `app/src/ui.js` is only a drawing).
- Analytics/SDKs: none. `app/package.json` dependencies are `@capacitor/android|app|core|status-bar` only; `google-services.json` is absent so the Google Services plugin is not applied (`app/android/app/build.gradle:tail`, `try { file('google-services.json') }`).
- Manifest: no INTERNET, no AD_ID, no RECORD_AUDIO; `android:allowBackup="false"` (`AndroidManifest.xml:6`), `usesCleartextTraffic="false"` (line 5).
- Contact / donate: **do not exist** in the app (grep for donate, support, contact, email: no matches). If either is added, use the gate below.
- Typed text: the only free-text field is the Level 5-7 writing box (`app/src/screens/session/write.js:9`); its content is compared on screen and only its length goes to the in-memory `window.__so.trace` (`write.js:29`). Never stored, never sent.

## Findings

### F1. No in-app access to the privacy policy (release blocker)
Play's User Data policy expects the privacy policy to be reachable in the app as well as in the Console, and this is a children's app. There is no privacy entry anywhere (`grep -ri privacy app/src` returns nothing).
**Fix:** add a small "For grown-ups" screen reached from Home, behind the grown-up gate (§Gate). It shows the policy as plain text (copy the "short version" and the table from `app/public/privacy.html`), prints the URL `oyekamal.github.io/sound-out/privacy.html` as **non-tappable text**, and has no links. Because it has no link, no gate would strictly be needed, but keep the gate so a child does not wander into adult text.
- `app/src/home.js` line 18, inside the `homehdr` header after the "Who is reading?" button: add `btn('For grown-ups', 'lock', { class: 'btn ghost small', say: 'ui:forGrownups', onclick: async () => { if (await askGrownup()) app.privacyInfo(); } })`.
- New `app/src/privacy.js` exporting `privacyScreen(app)` using `h()` from `ui.js`; add `privacyInfo() { stop(); return privacyScreen(app); }` to the `app` object in `app/src/main.js` (after line 24).
- `app/src/native.js` back button handler (lines 10-15): add `if (el.querySelector('.privacy')) return app.home();` before the final `app.home()` at line 14 (optional, it already goes Home).
- Record one clip `ui:forGrownups` ("For grown-ups") through `tools/gen_audio_el.py` so the button speaks when held (a button without a clip is silent, which the voice-first rule forbids).

### F2. Prototype wording on child-facing screens (release blocker)
Text a child or parent sees that says the app is unfinished or fake. It breaks the "no misleading or incomplete app" expectation and the listing's claims.
- `app/src/home.js:52` — `'Prototype: all voices are a computer voice for now; pictures are placeholders.'` → **delete the line** (the voice is a finished AI voice, disclosed in the listing and policy).
- `app/src/onboarding.js:36` — `'Language help packs are not in this prototype.'` → delete (see F3).
- `app/src/screens/listen.js:34` — `'Picture answers are placeholders in this prototype.'` → delete; `listen.js:16` label `'picture placeholder'` and `app/src/screens/l1oral.js:14` `picture ${i + 1}` stay only until the real word pictures land (picture lane); then use the real alt text.
- `app/src/screens/listen.js:37` — "any picture is accepted" (placeholders) must become a real check once the pictures exist, otherwise Listen & Talk praises every answer.
- `app/src/placeholder.js` (`coming.ogg` beep for Levels 2-7 clips with no audio): must not play in a released build. Fix by rendering the audio, not by hiding the code.

### F3. "Help in your language?" chips do nothing (release blocker unless removed)
`app/src/onboarding.js:7` lists Urdu, Spanish and Portuguese chips and `onboarding.js:31-37` saves the choice and moves on, but no help pack exists. A child-facing screen promises something that is not there.
**Fix (choose one):**
1. Remove the whole `helpLang` step: in `choose()` (`onboarding.js:13-18`) replace `helpLang(app, p)` with `app.firstSitting(p)`; delete `LANGS` (line 7) and `helpLang()` (lines 31-40). This keeps the listing true ("no second language needed").
2. Keep it only when packs ship *inside the AAB*. Downloaded packs (plan-v6 section 3, "a second tap downloads it") add a network request and the INTERNET permission, which would make "no data leaves the device", the Data safety "No", the privacy policy and the listing's PRIVACY lines wrong. If that is ever done: bundle packs in the app, or update all four documents and re-declare in the Console first.

### F4. No Content-Security-Policy (hardening)
`app/index.html:3-8`: no CSP meta tag. The Urdu app had one that blocks all outside addresses, which let its policy state that outright. Sound Out's policy deliberately does *not* claim that.
**Fix:** add inside `<head>` of `app/index.html`:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'">
```
Then run the driver (`python3 tools/drive.py`) and the APK on the emulator: the Vite dev server (`npm run dev`) needs `connect-src 'self' ws:` for hot reload, so apply the tag only in the production build (inject it in `vite.config.js` with `transformIndexHtml` when `command === 'build'`). After it ships, one sentence can be added to the privacy policy: "a Content-Security-Policy blocks the app from contacting other addresses".

### F5. Guard against an advertising-ID permission (hardening)
No AD_ID permission today, but a future dependency could add it silently and Play flags it for child-directed apps.
**Fix:** `app/android/app/src/main/AndroidManifest.xml`: add `xmlns:tools="http://schemas.android.com/tools"` to the `<manifest>` tag (line 2) and, before `<application>` (line 4), add:
```xml
<uses-permission android:name="com.google.android.gms.permission.AD_ID" tools:node="remove" />
<uses-permission android:name="android.permission.INTERNET" tools:node="remove" />
```
The second line makes a stray library unable to grant the app network access. Verify with `./gradlew :app:processReleaseMainManifest` and grep the merged manifest.

### F6. A Pages-only demo page ships inside the APK (hardening)
`app/package.json:10` (`build:android`) strips `compare`, `audition`, `compare.html`, `plan.html`, `listen.html`, `voices.html` and the `*-data.json` files from `dist/`, but not `app/public/tilo-demo.html` (an internal art demo) or the new `privacy.html`. They are unreachable from the UI, but they are extra files and `tilo-demo.html` is not part of the product.
**Fix:** append ` dist/tilo-demo.html` to the `rm -rf` list in `build:android`. Keep `privacy.html` in (F1 may reuse it).

### F7. Writing box keyboard hardening (hardening)
`app/src/screens/session/write.js:9`: the textarea has no `autocomplete`, `autocorrect`, `autocapitalize` or `spellcheck` attributes, so the phone keyboard may suggest and learn from what a child types.
**Fix:** add `autocomplete: 'off', autocorrect: 'off', autocapitalize: 'off', spellcheck: 'false'` to the attribute object on that line. (Android keyboards do not all honour the web hints; the text is never stored by the app either way.)

## Gate (for any future contact, donate or outside link)
None is needed today. If the owner adds an "Email Kamal" or a support button, or F1's screen later gains a tappable link, it must open only after this gate (Google's guidance: a challenge a young child cannot do, never a bare "I am an adult" tap).
Do **not** reuse the Urdu app's spelled-out-number gate unchanged: a child who is learning to read English can sound out "forty-seven". Use arithmetic shown in digits instead, with the Urdu app's lockout.
- New file `app/src/grownup.js` exporting `askGrownup(opts) -> Promise<boolean>` (name it `grownup.js`, not `gate.js`: `app/src/gate.js` is the *reading tap gate*).
- Challenge: two-digit by one-digit multiplication, e.g. `What is 17 × 6?` (operand a in 13..19, b in 4..9, never a multiple of 10 result trivially guessable), shown as digits and read aloud by nothing (no audio, so a pre-reader cannot be coached by the voice). Answer typed with a numeric keypad (`inputmode="numeric"`).
- Rules copied from `urdu-reading-course/mobile/src/gate.js`: bottom sheet with `role="dialog"` `aria-modal="true"`; 3 wrong tries then a 30 s calm lockout; the try counter and the lock time persist in `localStorage` (`so-gate-tries`, `so-gate-lock`) so a restart does not reset them; a second request while the sheet is open resolves `false`; Escape and the Close button resolve `false`; a wrong answer shows a new sum; focus trap and focus restore.
- Wire every outside action as `if (await askGrownup()) { ... }`. For a mailto: `window.location.href = 'mailto:...'` only inside that branch. After adding one, update `privacy.html` ("Sharing you start yourself"), the Data safety answers (a mailto sends nothing by itself, still "No") and `PLAY_CONSOLE_CHECKLIST.md` §3.4.
- Tests: extend `tools/drive.py` to assert that no `<a href>` and no `mailto:` exists in the DOM on any screen outside the gate, and that the sheet appears before any outside action.

## Items that were checked and are fine (no change)
- `app/capacitor.config.json`: `androidScheme: "https"` (served locally), no `server.url`, no `allowNavigation`, `allowMixedContent: false`.
- `app/src/native.js`: only the back button and the status bar; no plugin that reaches the network.
- `app/src/teacher.js` press-and-hold and the global click handlers: no navigation, no external effect.
- Profile labels are generated ("Child 1", `onboarding.js:13`); no name, email, age or birthday is asked for.
- `window.__so.trace` (`app/src/audio.js:4,11`) keeps events in memory only for the test drivers; nothing persists or leaves the page. The `?fast` and `?idlefast` URL switches are test hooks that a child cannot reach inside the app.
