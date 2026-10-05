# Research 01 — Competitor landscape for a free, offline-first "read English from zero, any age" app

Date: 2026-10-05. Method: live search (ddg.py) plus page fetches. Several store pages (Google Play, APKPure, chrome-stats) returned 403 or truncated content, so install counts for those apps are **not verified** and marked as such. Aggregator review sites (justuseapp, spellingjoy, etc.) are secondary sources; Reading.com's "programs to avoid" blog is a competitor and biased. Where a claim could not be confirmed, it says "not found".

Pedagogy reference: Kamal's course DESIGN.md (synthetic phonics backbone, decodables, 90% mastery gates, Track A child / Track B adult, no cueing).

---

## 1. Product-by-product table

| Product | Ages | Pedagogy | Offline | Price | Platform | Speech rec | Adults? |
|---|---|---|---|---|---|---|---|
| **Read Along (Google, ex-Bolo)** | 5+ (primary grades; "some basic alphabet knowledge") | Read-aloud practice with word-level feedback; not a phonics course. Assumes letters known | **Yes, fully offline once downloaded**; voice processed on-device for most languages | Free, no ads, no IAP, no account | Android + Android TV only, no iOS | Yes, core feature (Diya) | No (designed for children) |
| **Duolingo ABC** | 3-8 (Common Sense: 3+) | Systematic phonics, one letter at a time, 127 units, tracing | Launch coverage said offline learning included (9to5mac 2020); Common Sense review did not specify | Free, no ads, no IAP | iOS/Android | Yes, required for some games | No |
| **Khan Academy Kids** | 2-8 | Adaptive; phonics plus letter recognition plus read-to-me books | **Partial**: "Kodi's Suitcase" section of the library is offline; rest needs internet | Free, nonprofit | iOS/Android/Amazon | Not found | No |
| **Teach Your Monster to Read** | 4+ (UK Reception/Y1) | Systematic synthetic phonics, 3 stages, ~43 weeks at 20 min/wk | Not documented on official pages | Web free; app one-time ~$7.50 per aggregator | Web, iOS, Android | No | No |
| **Reading Eggs** | 2-13 (Eggs 3-7) | Phonics plus sight words plus comprehension; critics say picture-cue reliance | No evidence found | $9.99/mo or $69.99/yr (aggregator) | Web/iOS/Android | Not found | No |
| **Homer** | 2-8 | Phonics plus sight words plus interest-personalised content, 1,000+ lessons | **Partial**: download lessons, app must run in background | $9.99/mo or $59.99/yr | iOS/Android | Not found | No |
| **ABCmouse** | 2-8 | Single structured path, mixed methods | Not found | $14.99/mo or $45/yr; free tier 10 activities/day | Web/iOS/Android | Not found | No |
| **Starfall** | Pre-K-5 | Phonics-first, free tier plus paid | Not found | In-app $5.99/mo; home membership cheaper | Web/iOS/Android | Not found | No |
| **Bob Books Reading Magic #1/#2** | Preschool-K | Decodable phonics, blend-first | Native apps, so effectively offline (not stated on page) | Paid app; $1.99 Android listing, ~$3.99 iOS | iOS/Android | No | No |
| **Lexia Core5** | Pre-K-5 | Structured literacy, adaptive | Not found | School licence only, not sold to individuals | Web/app via school | Not found | No |
| **Amira Learning** | PreK-3 | Oral-reading tutor; fluency plus screening | Not found | ~$7.50-$35/student/yr via districts | School platform | Yes, core | No |
| **Ello** | 4-9 (Pre-K-3) | Decodable books, phonics coaching | Not found | $14.99/mo or $139/yr | **iPhone/iPad only** | Yes, core | No |
| **Hooked on Phonics app** | Pre-K-2 | Systematic phonics, 20-min lessons | Not found | ~$6.99-$12.99/mo, $59.99/yr | iOS/Android/web | Not found | Marketed "Pre-K through Adult" by one reviewer; not core |
| **Reading.com** | 3-8 | Phonics, 120 lessons | Not found | $14.99/mo or $89.99/yr | iOS/Android/web | Not found | No |
| **Lalilo (Renaissance)** | K-2 | Phonics plus comprehension | Not found | School licence | Web | Not found | No |
| **Phonics Hero** | K-3 | Systematic synthetic phonics, 850+ games | Not found | ~$72/yr home | Web/app | Not found | No |
| **Nessy Reading & Spelling** | 6-11 | Structured literacy, dyslexia focus | Not found | ~$10.51-$12/mo | Web/app | Not found | No |
| **Epic!** | 2-12 | Library of 40k+ books, no instruction | "Read Offline" for most titles (not all) | $84.99/yr (spellingjoy) | Web/iOS/Android | No | No |
| **Endless Alphabet** | Toddler-early | Letter sounds plus vocabulary | Offline once downloaded (Screenwise) | Free sample plus one-time unlock | iOS/Android | No | No |

### Adult / ESL
| Product | Pedagogy | Offline | Price | Notes |
|---|---|---|---|---|
| **Learning Upgrade** | 28 courses, 1,000+ lessons: songs, videos, games; covers alphabet, phonics, decoding, sight words, then ESL. Claims greatest pre/post reading gains in 12,000-adult field test; Adult Literacy XPRIZE winner | No evidence found | Free to start; app $4.99/mo up to $59.99/yr (justuseapp) | Closest "one app, all ages". Core instruction is English immersion; onboarding in Spanish and a few others. Rating 3.2/5 on justuseapp |
| **Cell-Ed** | 3-minute micro-lessons plus live bilingual coaches; 6 CASAS-aligned ESL levels | **Yes, via phone call, WhatsApp or SMS, no app, no wifi** | B2B only (employers, libraries, agencies), no public price | English, Spanish, Ukrainian, Russian, Dari "and more"; no Urdu found |
| **Beeline Reader** | Colour-gradient overlay for fluent readers; not a teaching tool | n/a | Freemium | Does not teach decoding |
| **ReadTheory** | Adaptive comprehension quizzes, K-12/ESL/adult worksheets | No | Free + premium | Assumes you can already decode |
| **Duolingo main app** | English course exists for several languages, but no Urdu-to-English course was surfaced in my searches; secondary sources say Duolingo has no Urdu *course* at all | Limited | Free + Super | Not a decoding course either way |
| **"Learn English in Urdu" Play Store apps** (e.g. com.urdupurelearnenglish, 1M+ downloads per AppBrain/APKPure) | Phrases, dictionary, translator, grammar; Urdu explanations | Yes, "study offline, completely free" | Free (ads) | Teaches speaking phrases, not systematic decoding |
| **Kiwa / other adult literacy apps** | Not found in search | — | — | Nothing equivalent surfaced |
| **Read Along** | See above | Yes | Free | Has Urdu (and Hindi, Bangla, etc.) but is child-framed |

---

## 2. Evidence notes per product (cited)

**Read Along.** Supported languages include Urdu, Hindi, Bangla, English, Arabic, Gujarati, Marathi, Portuguese, Spanish, Tamil, Telugu (https://support.google.com/readalong/answer/12281788?hl=en). Review of the app: works fully offline once downloaded, voice processed on-device, Diya "listens as a child reads aloud, offers help when they struggle, rewards progress with stars", no ads, no IAP, no account, Android only (https://teachustechnology.com/read-along-by-google-free-ai-reading-practice-app/). Impact: 64% of India pilot participants improved reading proficiency; 95% of parents would continue (http://readalong.google/impact/); Sattva ran a non-equivalent-group study over 6,000 learners (https://www.sattva.co.in/wp-content/uploads/2020/09/Sattva_Google_Read-Along-IA-Report.pdf). Play Store text: "Read Along (formerly Bolo) is a free and fun speech based reading tutor app designed for children aged 5 and above" (https://play.google.com/store/apps/details?id=com.google.android.apps.seekh&hl=en-GB&gl=in). Download count: not verified (page fetches blocked). It teaches by listening to a learner read stories; it does not teach the letter-sound code explicitly, and it is not a 0-to-fluent progression.

**Duolingo ABC.** Common Sense: ages 3+, systematic phonics, 127 units, tracing, speech recognition required for certain games; cons: "No option to skip ahead", "Kids can't choose where to start", navigation causing lesson repetition (https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read). justuseapp (4.2/5): level-progression loops ("constant loop on one level"), cannot skip, requests for other languages, no progress tracking for parents (https://justuseapp.com/en/app/1440502568/duolingo-abc-learn-to-read/reviews). Launch coverage: ad-free, no IAP, "includes offline learning" (https://9to5mac.com/2020/03/26/duolingo-abc-learn-to-read-ios-free-app/). Progression reaches "very simple short stories", then stops (https://www.plaudan.com/en/blog/duolingo-abc-review).

**Khan Academy Kids.** Offline only for Kodi's Suitcase (https://screenwiseapp.com/guides/khan-academy-kids-app; official note https://khankids.zendesk.com/hc/en-us/articles/360029139531-Learn-on-the-go-with-offline-content-in-Khan-Academy-Kids). Characters may feel "babyish" at 6-8. Official hook: "A free, 5-star rated (Common Sense Media) learning app for kids ages 2-8" (https://www.khanacademy.org/kids).

**Teach Your Monster to Read.** Systematic synthetic phonics designed with Roehampton academics (https://help.teachyourmonster.org/en/articles/5736688-how-is-teach-your-monster-to-read-educational). Usborne Foundation: 16 million children supported, 1.5 million play monthly (https://www.usbornefoundation.org.uk/teachyourmonstertoread/). Roehampton REF impact case study claims games reached ~20 million children (https://www.roehampton.ac.uk/globalassets/documents/research/ref2021/ref3-casestudy-23-ur23-playful-pedagogies.pdf/). **The requested "Roehampton RCT": I could not find a published RCT or any effect size on the official pages, the help article, or the Usborne page.** All three explicitly lack trial data. Do not cite an RCT for TYMR until someone locates the paper; say "co-designed with Roehampton, no independent trial found". Common Sense: 43 weeks at 20 min/week, repetitive mini-games, British narration, awkward navigation (https://www.commonsensemedia.org/app-reviews/teach-your-monster-to-read). justuseapp: British accent complaints, loud music over narration, cannot pause/save mid-level, "children can progress by guessing" (https://justuseapp.com/en/app/828392046/teach-your-monster-to-read/reviews).

**Reading Eggs.** Trustpilot 2.1/5 on 26 reviews: continued charges after cancellation, "Reading eggspress characters are more for 6-year-olds", "got absolutely hooked on the gaming side. Reading did not progress" (https://www.trustpilot.com/review/readingeggs.com). justuseapp: sound cutting out, repeated password prompts, lag, British content, errors can't be corrected mid-activity (https://justuseapp.com/en/app/726696040/reading-eggs-learn-to-read/reviews). Competitor claim (biased): "encourages children to use picture clues" (https://blog.reading.com/childrens-literacy-roundup-reading-programs-to-avoid/). Reading Eggs' own "negative reviews" page is marketing, not evidence.

**Homer.** $9.99/mo or $59.99/yr; offline download needs app running in background; complaints: instability, slow support, unclear auto-renewal (https://www.topconsumerreviews.com/best-learn-to-read-products/reviews/homer.php). Reddit: parent hesitating at "almost $60 a year" (https://www.reddit.com/r/homeschool/comments/15ylsyg/is_the_homer_app_any_good/).

**ABCmouse.** Trustpilot/PissedConsumer: 1,633 reviews averaging 1.9, issues "Cancellation, Refund, Subscription" (https://abcmouse.pissedconsumer.com/review.html). Renewal trap: app-store renewal can land at $59.99 vs $45 web; free tier = 10 activities/day (https://learningappforkids.com/blog/abcmouse-cost).

**Ello.** $14.99/mo or $139/yr; 700+ decodable books; child speech recognition; iOS only; collects audio data; glitches (https://spellingjoy.com/best-apps/app/ello). Common Sense called it responsible AI per same source.

**Amira.** Teachers report speech recognition fails with "accents, lisps, articulation disorders, and ELL speech"; effect size 0.40 is vendor-reported; Boston University evaluation pending (https://academicaitrends.com/blog/is-amira-learning-worth-it-2026/).

**Lexia Core5.** Used in 1 in 4 US schools; not available for individual purchase (https://spellingjoy.com/best-apps/app/lexia-core5).

**Hooked on Phonics.** $6.99-$12.99/mo, $59.99/yr app plan (https://spellingjoy.com/best-apps/duolingo-abc-vs-hooked-on-phonics); Trustpilot lists 1,375 reviews (https://www.trustpilot.com/review/hookedonphonics.com). Reading.com: from $14.99/mo, $89.99/yr (https://brighterly.com/blog/how-much-is-reading-com/). Nessy ~ $10.51/mo (https://www.modulo.app/all-resources/nessy-reading-review). Phonics Hero ~$72/yr (https://spellingjoy.com/best-apps/app/phonics-hero). Starfall in-app $5.99/mo (https://help.starfall.com/help/help-me-choose-a-membership). Bob Books Android listing $1.99 (https://m.apkpure.com/bob-books-reading-magic-1/com.learningtouch.bobbooksrm1). Epic "Read Offline" not available for all titles (https://support.getepic.com/hc/en-us/articles/205484365-Can-I-read-books-offline). Endless Alphabet offline once downloaded (https://screenwiseapp.com/media/endless-alphabet-app).

**Learning Upgrade (adults).** "28 courses with 1,000+ lessons that include songs, videos, and games" (https://www.proliteracy.org/news/4-apps-that-empower-adult-learners/). ESL page: phonics, decoding, sight words across six English courses; pilots give three months free then paid licence; no offline mention (https://web.learningupgrade.com/adult-education/esl/). justuseapp 3.2/5: login lockouts ("already signed in somewhere else"), freezing, sound failures, "songs aren't teaching anything", support "go around in circles"; prices $4.99/mo to $59.99/12 months (https://justuseapp.com/en/app/1185694693/learning-upgrade/reviews).

**Cell-Ed.** "No app required. No wifi needed. No barriers." Works over phone call or WhatsApp; 6 CASAS-aligned levels; sold to organisations, no public price, demo-request flow (https://www.cell-ed.com/how-it-works/). Claims 84% faster skill gains, 75% completion (vendor-reported).

---

## 3. Answers to the five questions

### 3.1 Which actually run offline?
Confirmed offline: **Read Along** (full), **Khan Academy Kids** (Kodi's Suitcase only), **Homer** (downloads, with background-process caveat), **Endless Alphabet**, **Bob Books** (native apps), **Epic** (most titles), **Cell-Ed** (via voice call), and Duolingo ABC per launch coverage. Not found for: Reading Eggs, ABCmouse, Starfall, Reading.com, Hooked on Phonics, Lexia, Amira, Ello, Lalilo, Phonics Hero, Nessy, Learning Upgrade, TYMR. Of these, only Read Along is **free + fully offline + speech-based**, and it is Android-only and child-framed.

### 3.2 Recurring complaints (parents and adults)
1. **Billing and cancellation traps**: ABCmouse (1.9 avg, 1,633 reviews), Reading Eggs (2.1 Trustpilot), Homer auto-renewal confusion, ABCmouse app-store renewal at higher price. Sources above.
2. **No way to skip or place out**: Duolingo ABC (Common Sense and justuseapp). Also Amira teachers lack override of algorithmic scores.
3. **Age ceiling and "babyish" framing**: Reading Eggs (12-year-old complaint), Khan Kids (6-8s), Duolingo ABC ages 3-8. Nothing in the table is built to feel adult.
4. **Bugs and repetition loops**: Duolingo ABC stuck-level loop, Reading Eggs sound dropouts and lag, Learning Upgrade freezing and logins.
5. **Accent and locale mismatch**: TYMR and Reading Eggs British narration disliked by US parents; Amira fails on accents and ELL speech. For Urdu speakers the inverse matters: no product models South Asian L1 interference.
6. **Gamification beats learning**: "got absolutely hooked on the gaming side. Reading did not progress" (Reading Eggs); TYMR guessing-through levels.
7. **Locked to schools**: Lexia, Lalilo, Amira are not available to a family or an adult.

### 3.3 Speech recognition: who has it, how is it rated
- **Read Along**: core feature; on-device; no complaint corpus retrieved (store review pages blocked). A rural India study reports a "significant impact" on reading skills (https://www.researchgate.net/publication/367530432_EFFECTIVENESS_OF_GOOGLE_READ_ALONG_APP_IN_IMPROVING_READING_SKILLS_OF_RURAL_AREA_PRIMARY_SCHOOL_STUDENTS). Unverified: Play Store rating.
- **Duolingo ABC**: used in some games, mic permission required; reviewers split ("chimed because he got it right" vs struggles with accuracy).
- **Amira**: documented failures on accents, lisps, ELL.
- **Ello**: core feature, 4.8 stars on 2,500+ iOS reviews per spellingjoy, but "glitches" and data collection (audio).
- **Everyone else**: no speech recognition found.
Pattern: speech recognition is trusted when it scaffolds (Diya helps) and resented when it gates progress or fails on non-standard speech.

### 3.4 Does one app for "any age" exist?
**Not really.** Closest are:
- **Learning Upgrade**: K-12 plus adult plus refugee programs under one app, but it is subscription/licence-based, online (no offline claim found), 3.2/5, and its pedagogy is songs/videos in English immersion.
- **Cell-Ed**: adult-only, B2B, phone-delivered.
- **Read Along**: free and offline, but child framing and no systematic code instruction.
Child apps stop at roughly grade 2-3 or age 8-9; adult products assume prior decoding. Nobody advertises a single zero-to-fluent path with age-appropriate content registers.

### 3.5 Store-listing hook lines (verbatim where available)
- Read Along: "a free and fun speech based reading tutor app" / "an in-app reading buddy that listens to your young learner read aloud, offers assistance when they struggle".
- Khan Kids: "A free, 5-star rated (Common Sense Media) learning app for kids ages 2-8".
- Duolingo ABC: ad-free, no IAP, designed by "literacy and early-education experts".
- Cell-Ed: "3-minute lessons on any device... Skills for work, life, and health."
- Learning Upgrade: "individualized, self paced, and comprehensive English, math, test prep, and career readiness courses".
- TYMR: "free, award-winning reading, mathematics and phonics games"; "BAFTA-nominated".
- Reading Eggs (user quote used as hook): "starting kindergarten on a second grade reading level".
- Reading.com: "ground-breaking phonics program... 64 million children since 1998" (company-wide).
Dominant hooks: speed ("level X by kindergarten"), fun, expert-designed, and free/no ads. **No one leads with offline, with adults, or with a mastery guarantee.**

---

## 4. Gaps nobody fills (one page)

1. **A decoding-first path that runs to fluency and critical reading in one product.** Duolingo ABC stops at simple stories; Khan Kids and Starfall stop around grade 2-3; ReadTheory and Beeline assume you can decode. Learning Upgrade is the only multi-level one and is paywalled and songs-based. Kamal's L1-L7 spine is unmatched.
2. **Adult-respectful content on the same skill sequence.** Every child product is cartoon-coded (Reading Eggs complaint at 12 years old; Khan "babyish"). Track B (work, money, bus, market, phone, health) with the *same target patterns* as Track A does not exist anywhere in this set.
3. **Free + fully offline + speech feedback, on a phone a Pakistani family actually owns.** Only Read Along does this, and it is Android-only, assumes known letters, and has no placement or mastery gate. Everything else with speech feedback (Ello iOS only, Amira school-only) is paid or institutional.
4. **Mastery gates with real placement and skip-ahead.** The top complaint on the free leader, Duolingo ABC, is "can't skip"; Amira teachers cannot override. A 90% gate with pseudowords and a placement test fixes both.
5. **Urdu-first instruction of the English code.** Urdu is supported in Read Along's *story languages*, but I found no product teaching the English letter-sound code *using Urdu-speaker error patterns* (v/w, th, short vowels, cluster epenthesis). The Urdu-medium Play Store apps (1M-5M downloads) teach phrases and translation, not decoding.
6. **Speech recognition tuned to L2 and child speech with human-in-the-loop fallback.** Amira's known failure on accents and ELL, Ello's audio-data worries; an on-device recogniser that scores *sounds* (not word guesses) and degrades gracefully to self-check would beat both. (Feasibility is a build question, not shown by this research.)
7. **Honesty about evidence.** TYMR has reach numbers but no found trial; Amira's 0.40 is vendor-reported. A published, independent pre/post (even small) would be a differentiator.
8. **No billing surface.** Billing/cancellation is the biggest recurring complaint across the paid set; free, no account is a trust position only Read Along and Duolingo ABC currently hold.
9. **Phone-call/WhatsApp delivery for the lowest-connectivity adults.** Cell-Ed proves demand but sells only B2B; an offline PWA plus optional audio-only lessons covers the same ground for free.

### Top 5 bars worth beating

| # | Bar | Why it is the bar | What to beat | URL for critics |
|---|---|---|---|---|
| 1 | **Read Along (Google)** | Free, offline, on-device speech, Urdu stories, India pilot (64% improved) | Add explicit code teaching, placement, mastery gates, adult track, PWA (no Android lock-in) | https://readalong.google/impact/ and https://teachustechnology.com/read-along-by-google-free-ai-reading-practice-app/ |
| 2 | **Duolingo ABC** | Free, ad-free, 127 phonics units, tracing, best-in-class polish | Skip-ahead/placement; loops; ends at short stories; no adults | https://www.commonsensemedia.org/app-reviews/duolingo-abc-learn-to-read |
| 3 | **Teach Your Monster to Read** | Closest SSP pedagogy to DESIGN.md; 16M reached | Pause/save, accent neutrality, shorter path, true offline, trial evidence | https://www.commonsensemedia.org/app-reviews/teach-your-monster-to-read |
| 4 | **Learning Upgrade** | Only multi-level adult-through-child literacy app, XPRIZE | Free, offline, Urdu support, reliable login, real decoding instruction | https://web.learningupgrade.com/adult-education/esl/ |
| 5 | **Ello (and Amira as the speech benchmark)** | Best-reviewed speech-listening reading tutor (4.8 on 2,500+ reviews) | Free, Android, offline, accent-tolerant, no audio harvesting | https://spellingjoy.com/best-apps/app/ello and https://academicaitrends.com/blog/is-amira-learning-worth-it-2026/ |

Honourable mention: Cell-Ed as the access-model bar for adults (https://www.cell-ed.com/how-it-works/).

### Open items for the next research pass
- Verify Read Along install count and Play Store rating/complaints (page fetches were blocked; try an APK mirror or Play scraper).
- Locate any published TYMR trial; if none, drop the claim.
- Confirm Duolingo ABC offline behaviour on current builds (only 2020 launch coverage found).
- Check whether Duolingo offers any English course reachable from Urdu (searches returned only "no Urdu course").
- Pull Reddit threads on adult illiterate English learners (r/ESL_Teachers thread found: https://www.reddit.com/r/ESL_Teachers/comments/vz71qm/does_anyone_have_experience_teaching_adults_how/ — notes child phonics programs rely on pre-reading concepts and suggests Language Experience Approach, which matches DESIGN.md).
