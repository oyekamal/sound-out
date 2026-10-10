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
