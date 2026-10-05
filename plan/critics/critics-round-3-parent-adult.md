# Critics round 3: parent and adult (plan-v3)

Personas: mother in Rawalpindi (3 GB phone, kids 5 and 8, patchy data, no English, has Khan Kids + Duolingo ABC); shopkeeper, 38 (Urdu/Punjabi, slow Urdu reader, no English, embarrassed, 15 min a night, quit Duolingo once).
Read: plan-v3.md, both bar JSONs, both Common Sense reviews.

## Verdicts after one week

- **Mother: B stays.** Her 5-year-old got one letter a day with a silent mascot while Khan Kids gives songs, read-to-me books and an age-fitted path, and her 8-year-old, who knows letters, is made to trace "s" because the plan has no age path.
- **Shopkeeper: A stays, narrowly.** Main Duolingo never taught him to decode and A has him reading "sat" on night one in private, if the first Check does not become his second quit.

## The single biggest stop

**Shopkeeper, night 2 or 3: the first Check.** Track B is sitting ABC (night 1), D (night 2), G = Check (night 2 or 3) (§3.2, §6.2). G is 11 items, bar 9/11, first attempts only (§3.6), with made-up words (tas, ast, sta), a 6-second window that starts after he has played up to four sound buttons (E6d), and dictation. Nothing in the exercise flow tells him in Urdu what "made-up words" are; the reassuring script exists only in the placement tester notes (§3.5).

Using the plan's own binomial arithmetic: at 80% per-item accuracy he passes about 62% of tries; at 70%, about 31%. A miss sends him to "reteach step C", the "t" sitting he thought he had finished. G0 promises "no test", yet night one already has two ≥90% mini checks deciding whether he continues into B and C (§3.2). With no streak or reminder (§3.11), nothing pulls him back on night four.

## Defects (6)

### 1. No grown-up PIN on a child-only phone; no recovery for a forgotten one
- **Section:** §3.1, §3.12.
- **Failing moment:** The mother taps "A child" and never "Me". The adult PIN is "set on first adult launch", so she has none. Placement, "I already know this", pack downloads, pattern reset and progress are all behind it. The shopkeeper sets his at the end of night one (one "Later" allowed). Forgetting it is not covered anywhere. With "ask my PIN every time" on, he is locked out of his own lessons, and restore-backup is also behind the PIN.
- **Better apps:** Khan Kids has a parent account with confirmed email and parent-created child profiles (Common Sense), so there is one recovery route.
- **Verify:** Fresh install through "Children" only; try to reach placement and pack download. Grep §3.1 for "forgot". Run a forgotten-PIN test on day 7.

### 2. One fixed sequence for a 5-year-old and an 8-year-old
- **Section:** §1.1 (no Urdu-home 8-year-old archetype), D2 "role not age", §3.5.
- **Failing moment:** Both start at L1.02, s/a/t over about 7 sittings. The only way past is placement behind the PIN, with Stage 1 skipped when no English-reading helper exists and Stage 2 a receptive "hearing version" the mother cannot supervise.
- **Better apps:** Common Sense: Khan Kids follows "a learning path tailored to their age and previous performance". The plan's bar table says Khan placement is "not found"; that is stale. ABC cannot skip ahead and "may be best in small doses" (Common Sense), and A copies that weakness.
- **Verify:** Give an 8-year-old who knows A-Z three days. Time how long before she meets something new.

### 3. Sibling protection has no stated limits
- **Section:** §3.1, §6.6 (one 9-year-old, 10 minutes, week 5).
- **Failing moment:** The plan states no pattern space (4 from how many shapes), no lockout after wrong tries, no auto-return to the doors when the phone is put down. The 8-year-old watches the 5-year-old tap four shapes. She can also play inside an already-open profile, and her wrong taps become the younger child's first attempts (§3.6), pushing her to reteach and raising a grown-up flag the mother cannot read.
- **Better apps:** Khan Kids' path re-fits to performance, so stray taps self-correct. A's first-attempt-only gates do not.
- **Verify:** Add pattern space, lockout and session timeout to the spec. Test: 8-year-old plays 5 minutes in an open profile; inspect the gate record and flags.

### 4. "Free, offline" holds only for Levels 0-2; the pack prompt speaks in MB
- **Section:** §4.1, §3.1 (pack downloads behind PIN), §3.12, §7 listing.
- **Failing moment:** Install is a 34-46 MB estimate (measured only in week 7). L3-L5 packs add 27-40 MB, about the app's size again, at roughly month 6 at one sitting a day, shown as "N MB" with "no rupee figures". She has patchy data and cannot read English, so MB means nothing. The prompt sits behind the PIN she may not have (defect 1). Nothing tells her that stopping mid-download is safe.
- **Better apps:** Khan Kids (201 MiB) and ABC (212 MiB) show one number in the store and ask for nothing later. A is much smaller, which is its real win on 3 GB.
- **Verify:** Ask the mother "will this cost me money, how much?" Review the listing copy and the Urdu pack string. Measure installed size in week 3.

### 5. First launch for a non-reader
- **Section:** §3.1, §3.12 (Launch, then Role), §6.6 icons-only test (week 8).
- **Failing moment:** The launch screen asks "Children" or "Me", then the Role screen asks "A child" or "Me" again; the order on a fresh install is unstated, as is first-run language. The adult door is a small lock beside a large "Children" door, and a lock reads as "locked" before any PIN exists. Track B calls them "tricky words" (§2.1), while G4 (§12.3) bans that word as child-coded. No headphone prompt for night use.
- **Better apps:** Khan Kids puts the parent first; ABC asks for a child name or nickname (Common Sense).
- **Verify:** Run the icons-only test now on paper mocks with 5 Urdu-only adults. Grep Track B strings for "tricky".

### 6. The mother's view does not tell her what to do
- **Section:** §3.4 "Show your grown-up", §3.8, §3.10, §3.11.
- **Failing moment:** The 5-year-old's 8 minutes alone: Pebble waves, 4 sound-game taps, meet /s/, 3 traces, 6 bubbles, the sun rises. The mother can judge /s/ but not /æ/ on day two. "Mastered" needs a helper who hears English, so her best label for months is "Checked by tapping". "Tell your grown-up" in Listen & Talk assumes she understands the English answer. Passing and failing the gate look the same to her.
- **Better apps:** Khan Kids kids pick activities and collect prizes; ABC highlights words read aloud in stories (listing). The parent can see something happened.
- **Verify:** Show three Urdu-only mothers the "Show your grown-up" screen and the Progress page. Ask "Is she doing well? What do you do tomorrow?"

## Biggest gap

"No one who reads English has to help" breaks exactly where a judgement is needed: the PIN that gates everything, the 5/8-year-old mismatch on one sequence, and the shopkeeper's first Check, which is a graded test of made-up words that the plan told him would not exist.
