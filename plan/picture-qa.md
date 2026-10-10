# Picture QA: full critic pass

Scope: all 512 pictures in `app/public/img/words/pictures.json`, judged visually on 18 labelled grids (30 per grid). Ambiguous words flagged in `pictures.meta.json` are listed only, not judged.

## Totals

| Item | Count |
|---|---|
| Pictures total | 512 |
| Ambiguous (skipped, listed below) | 52 |
| Judged | 460 |
| - word pictures judged | 348 |
| - scene pictures judged | 112 |
| FAIL | 38 |
| PASS | 422 |

Scene pictures were judged visually against their intent summary in `content/picture_scenes.json`. Several scenes have an empty intent, so only their visual quality was checked there.

## FAIL

| word | file | what a child would say instead | one-line prompt fix |
|---|---|---|---|
| brush | brush.webp | child brushing teeth (toothbrush), not a paint brush | show a single large paint brush alone on white, no child |
| bug | bug.webp | ladybird / ladybug | draw a generic bug (e.g. beetle with 6 legs, not spotted red) |
| bun | bun.webp | bread roll / bread | draw a round bun with sesame seeds, clearly different from the loaf |
| claw | claw.webp | lobster or crab | draw a single animal-free claw-shaped pincer tool or make clear it is a bird claw |
| cot | cot.webp | crib or bed | draw an empty folding camp cot with visible legs, no baby |
| den | den.webp | fox or hole | show an empty burrow with no animal inside |
| dish | dish.webp | food or curry or bowl | show an empty plate with a fork, no food |
| dry | dry.webp | cracked ground, cookie | show a dry towel or dry sunny cracked soil with a sun overhead |
| empty | empty.webp | plate or cup | show an empty glass in side view, nothing inside |
| fast | fast.webp | cat or cheetah running | show a clearly speeding car or rabbit with motion lines |
| flute | flute.webp | pipe or stick | show a wooden recorder with finger holes, clearly a musical instrument |
| fly | fly.webp | bird | show a clearly flying insect or bird with a visible flying action |
| full | full.webp | cup of water | show a glass filled to the brim with a clear level line |
| giant | giant.webp | boy | show a huge figure towering over a small house |
| hawk | hawk.webp | owl or eagle | draw a hawk with hooked beak and sharp eyes, clearly a raptor |
| hop | hop.webp | jump | show a bunny or child on one foot with clear hop motion, not a jump with arms out |
| knee | knee.webp | boy or ball | close-up of a bent knee with a plaster or scraped skin |
| lawn | lawn.webp | grass or bush | show a mown lawn with a lawnmower |
| long | long.webp | ribbon or tape | show a long rope or road stretching edge to edge |
| moth | moth.webp | butterfly | draw a moth with feathery antennae and dull wings, distinct from butterfly |
| napkin | napkin.webp | towel or cloth | show a napkin folded on a table beside a plate |
| nut | nut.webp | peanut | show a walnut or hazelnut in its shell, not a peanut |
| point | point.webp | star | show a hand with index finger extended pointing at an object |
| ride | ride.webp | bike | show a child on a rocking horse or a bike clearly in motion with a visible route |
| room | room.webp | house or door | show a room with furniture visible inside four walls, a sofa and a lamp |
| sip | sip.webp | drink | show a cup held to lips with a straw, clearly a small sip from a spoon or cup rim |
| small | small.webp | mouse | show a tiny object next to a huge one, e.g. a pea beside a plate |
| snore | snore.webp | sleep | show a sleeping person with ZZZ and open mouth, nose-whistle lines |
| snow | snow.webp | cloud | show a snowy ground with a snowman or piled snow on a lawn |
| straw | straw.webp | candy cane | show a clear plastic drinking straw standing in a glass of juice |
| tail | tail.webp | fire or flame | show a fox tail attached to a fox body |
| tall | tall.webp | child with arms up or happy | show a tall tree or tall giraffe next to a short person |
| thumb | thumb.webp | thumbs up | show a single thumb pointed at a finger or tiny thumb labelled by a finger |
| tie | tie.webp | shoelace or bow | show a necktie knotted on a shirt collar |
| tube | tube.webp | toothpaste | show a tube with a clear cap and squeeze lines, no toothpaste on the table |
| wait | wait.webp | stand or door | show a child looking at a clock or tapping foot, clearly waiting |
| wig | wig.webp | hair or ball | show a wig on a mannequin head |
| wind | wind.webp | flag | show leaves or a kite blowing in the wind with wind lines |

## Ambiguous (skipped, not judged)

animal, at, bat, boss, brave, busy, caravan, card, cart, chin, cot, count, crumb, dish, dock, dot, engine, fat, field, gate, glue, gum, ham, hard, head, hog, hold, hole, hood, it, jet, key, kid, kind, lamb, lid, lip, mule, new, nose, old, on, proud, rat, sat, sky, string, tank, thin, tool, uncle, up

## Round 2 (36 redone pictures)

Scope: the 36 pictures redone after Round 1 failures, judged on 3 labelled grids (12 per grid) in the scratch folder. Verdict is what a 5-year-old would name on seeing the picture; FAIL lists that wrong name.

| word | file | verdict | what a child would say instead / note |
|---|---|---|---|
| brush | brush.webp | PASS | paintbrush with paint |
| bug | bug.webp | PASS | beetle |
| bun | bun.webp | PASS | seeded bun |
| claw | claw.webp | FAIL | bird foot or chicken leg; reads as a foot gripping a branch, not a claw |
| cot | cot.webp | FAIL | bench or folding chair; no mattress or bed cue |
| den | den.webp | FAIL | cave or hill with a hole; no animal home cue |
| dish | dish.webp | PASS | plate with fork and spoon (arrow marks are a minor distraction) |
| dry | dry.webp | FAIL | towel or sun; drying is implied, not shown |
| empty | empty.webp | FAIL | cup or milk; interior is filled with pale colour, emptiness not shown |
| fast | fast.webp | PASS | fast car with speed lines |
| flute | flute.webp | PASS | recorder or flute |
| fly | fly.webp | FAIL | bee; the insect is a bee, not a fly |
| full | full.webp | FAIL | orange juice; glass is not filled to the brim |
| hawk | hawk.webp | FAIL | owl or bird; big front-facing eyes read as an owl |
| hop | hop.webp | PASS | bunny jumping with arc |
| knee | knee.webp | FAIL | leg or bottom with a plaster; joint not clear |
| lawn | lawn.webp | PASS | lawnmower on striped grass |
| moth | moth.webp | FAIL | butterfly or bug; cute winged bug, moth cues too weak (previous misread still applies) |
| napkin | napkin.webp | FAIL | paper, card or tent; no cloth cue |
| nut | nut.webp | PASS | walnut halves |
| point | point.webp | PASS | pointing finger at an apple |
| ride | ride.webp | PASS | child riding a horse |
| room | room.webp | PASS | room with sofa, lamp and window |
| sip | sip.webp | PASS | child sipping from a cup |
| small | small.webp | FAIL | pumpkin; the tiny green ball does not show smallness |
| snore | snore.webp | PASS | sleeping child with ZZZ and open mouth |
| snow | snow.webp | PASS | snowman with snowflakes |
| straw | straw.webp | PASS | drinking straw in a glass; stripes are still candy-cane-like but the glass gives the context |
| tail | tail.webp | FAIL | fox; the tail is not isolated from the animal |
| tall | tall.webp | PASS | giraffe beside a small child |
| thumb | thumb.webp | PASS | hand with thumb circled (weak highlight, borderline) |
| tie | tie.webp | PASS | blue necktie on a shirt |
| tube | tube.webp | PASS | toothpaste tube |
| wait | wait.webp | PASS | child on a bench by a clock |
| wig | wig.webp | PASS | curly wig on a head form |
| wind | wind.webp | FAIL | kite; wind is only thin swirl lines |

### Round 2 totals

| Item | Count |
|---|---|
| Pictures redone and judged | 36 |
| PASS | 22 |
| FAIL | 14 |

FAIL list: claw, cot, den, dry, empty, fly, full, hawk, knee, moth, napkin, small, tail, wind.

## Round 3 (10 regenerated nouns, commit 391b902)

Scope: the 10 nouns regenerated after Round 2 failures, judged on 1 labelled grid (10 per grid) in the scratch folder. Verdict is what a 5-year-old would name on seeing the picture; FAIL lists that wrong name.

| word | file | verdict | what a child would say instead / note |
|---|---|---|---|
| claw | claw.webp | FAIL | crab or lobster; reads as a crab pincer, not a claw |
| cot | cot.webp | FAIL | crib or baby bed; wooden crib with a blue lump, not the empty folding cot the prompt asked for |
| den | den.webp | FAIL | fox; a fox sits inside the burrow, the prompt said empty |
| fly | fly.webp | PASS | housefly with red eyes and clear wings |
| hawk | hawk.webp | FAIL | bird or eagle; flying bird with the raptor cues (hooked beak, talons) too small to read |
| knee | knee.webp | FAIL | leg; a bent limb with a yellow ring, no clear knee joint or plaster |
| moth | moth.webp | FAIL | butterfly or owl; the moth is small on a branch and its feathery antennae are the only clue |
| napkin | napkin.webp | PASS | folded cloth napkin beside a plate on a table (blue stripe can read as a tea towel, borderline) |
| tail | tail.webp | FAIL | pig; the curly tail is small and the animal is the subject |
| wind | wind.webp | PASS | tree bending in swirling wind lines |

### Round 3 totals

| Item | Count |
|---|---|
| Pictures redone and judged | 10 |
| PASS | 3 |
| FAIL | 7 |

FAIL list: claw, cot, den, hawk, knee, moth, tail.
