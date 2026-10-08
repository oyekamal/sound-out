// L1.14 Level 1 mastery check: the course's full instrument (course/level-1/mastery-check.md), each component with its
// own bar; ALL components must meet their bar (the course: "Any row N -> do not advance"). Passing opens Level 2.
// First attempt only. Tap-gate items run through the normal gate (its repair still teaches, but only attempt 1 scores).
import { play, wait, mark } from '../audio.js';
import { h } from '../ui.js';
import { entry, g2p, options } from '../content.js';
import { gate, printedWord } from '../gate.js';
import { spellWord } from './spell.js';
import { choose, shuffle } from './l1steps.js';

export const INSTRUMENT = [
  { id: 'letters', title: 'Letter sounds', pass: 28, items: 'a b c d e f g h i j k l m n o p qu r s t u v w x y z ck ff ll ss zz'.split(' ') },
  { id: 'real', title: 'Real words', pass: 18, items: 'sat pin mad dog sock cut hen fib bell hats jog van wig box yak zip quiz big dip mess'.split(' ') },
  { id: 'pseudo', title: 'Alien words', pass: 9, items: 'taf nid gof kec rup haz vin quob fex dov'.split(' ') },
  { id: 'heart', title: 'Tricky words', pass: 22, items: 'a I the is to of and was said you are he she we me be do what they one have go no so'.split(' ') },
  { id: 'context', title: 'Tricky words in a sentence', pass: 5, items: [['The', 'The dog ran.'], ['They', 'They are at the dock.'], ['What', 'What did you get?'], ['Have', 'Have you got a map?'], ['Go', 'Go to the dock.'], ['said', 'I said so.']] },
  { id: 'dictation', title: 'Spelling', pass: 9, items: 'hat bug fox jazz sock dog pig sat in mud'.split(' ') },   // 5 words + the sentence "The dog and the pig sat in the mud." (its 5 decodable words)
  { id: 'bdpq', title: 'b d p q', pass: 7, items: [['bat', 'read'], ['dip', 'read'], ['pat', 'read'], ['quiz', 'read'], ['bag', 'write'], ['dog', 'write'], ['pin', 'write'], ['quit', 'write']] },
];
const HEART = INSTRUMENT.find(c => c.id === 'heart').items;
const key = w => (w === 'I' ? 'I' : w.toLowerCase());
// the items the app can run (a missing lexicon entry or option grid would be a content bug; drive.py checks there are none)
export const runnable = c => c.items.filter(it => {
  const w = Array.isArray(it) ? it[0] : it;
  if (c.id === 'letters') return !!g2p[w];
  if (c.id === 'real' || c.id === 'pseudo' || (c.id === 'bdpq' && it[1] === 'read')) return !!options[w];
  return !!entry(key(w));
});

function stageFor(ctx, step) { ctx.step = step; mark('step', { key: ctx.sitting.key, step }); return ctx.stage(); }

async function letterSound(ctx, g) {
  const s = stageFor(ctx, 'm-letters');
  const p = g2p[g];
  const others = shuffle([...new Set(Object.values(g2p))].filter(x => x !== p)).slice(0, 2);
  s.append(h('h2', {}, 'What does it say?'), h('div', { class: 'lettercard small' }, g));
  await ctx.instruct('ui:warmIntro');
  return choose(s, shuffle([p, ...others]).map(x => ({ key: `ph:${x}`, ok: x === p, id: x })), { test: true, cls: 'three' });
}

async function heartWord(ctx, w, sentence) {
  const s = stageFor(ctx, sentence ? 'm-context' : 'm-heart');
  const k = key(w);
  if (sentence) {
    const page = h('p', { class: 'sentence' }, ...sentence.split(/(\s+)/).map(t => t.replace(/[^A-Za-z]/g, '') === w ? h('b', { class: 'target' }, t) : t));
    s.append(h('h2', {}, 'Read the dark word'), page);
  } else s.append(h('h2', {}, 'Read it'), printedWord(k, null, ctx.track));
  await ctx.instruct('ui:gateRead'); await wait(1500);
  const others = shuffle(HEART.map(key).filter(x => x !== k && x.length > 1)).slice(0, 2);
  return choose(s, shuffle([k, ...others]).map(x => ({ key: `w:${x}`, ok: x === k, id: x })), { test: true, cls: 'three' });
}

export async function mastery(ctx) {
  const s0 = stageFor(ctx, 'm-intro');
  s0.append(h('h2', {}, 'Level 1 check'), h('p', { class: 'prompt' }, 'Everything from Level 1, no hints. Take your time.'),
    h('ul', { class: 'cue' }, ...INSTRUMENT.map(c => h('li', {}, `${c.title}: ${runnable(c).length}`))));
  await ctx.instruct('ui:l1MasteryIntro'); await ctx.next();
  const parts = [];
  for (const c of INSTRUMENT) {
    let correct = 0, judged = 0;
    for (const it of shuffle(runnable(c))) {
      let r;
      if (c.id === 'letters') r = await letterSound(ctx, it);
      else if (c.id === 'real' || c.id === 'pseudo') { ctx.step = `m-${c.id}`; r = await gate(ctx, it, c.id); await ctx.record(it, c.id, r); }
      else if (c.id === 'heart') r = await heartWord(ctx, it);
      else if (c.id === 'context') r = await heartWord(ctx, it[0], it[1]);
      else if (c.id === 'dictation') { ctx.step = 'm-dictation'; r = await spellWord(ctx, it, ctx.known()); }
      else if (c.id === 'bdpq') { ctx.step = 'm-bdpq'; r = it[1] === 'read' ? await gate(ctx, it[0], 'real') : await spellWord(ctx, it[0], ctx.known()); }
      judged++; if (r.judged && r.correct) correct++;          // a timeout counts as a miss in the check
    }
    // a component's bar scales if an item could not run (never expected; drive.py fails the build if it happens)
    const pass = Math.ceil(c.pass * judged / c.items.length);
    parts.push({ id: c.id, title: c.title, correct, judged, pass, met: correct >= pass });
    mark('mastery-part', parts[parts.length - 1]);
  }
  const met = parts.every(p => p.met);
  const correct = parts.reduce((a, p) => a + p.correct, 0), judged = parts.reduce((a, p) => a + p.judged, 0);
  const result = met ? 'checked' : 'miss';
  mark('check-end', { result, correct, judged, parts });
  const s = stageFor(ctx, 'm-result');
  s.append(h('h2', {}, met ? 'Level 1 passed!' : 'Level 1 check'),
    h('table', { class: 'mastery' }, h('tr', {}, h('th', {}, 'Part'), h('th', {}, 'Score'), h('th', {}, 'Bar'), h('th', {}, '')),
      ...parts.map(p => h('tr', { class: p.met ? 'met' : 'unmet' }, h('td', {}, p.title), h('td', {}, `${p.correct}/${p.judged}`), h('td', {}, `≥${p.pass}`), h('td', {}, p.met ? '✓' : 'practise')))),
    h('p', { class: 'prompt' }, met ? 'Level 2 opens next. It is coming soon.' : 'Practise the parts marked "practise", then try the check again. The rest of Level 1 stays open.'));
  await play(met ? 'ui:l1MasteryPass' : 'ui:l1MasteryMiss');
  await ctx.next();
  return { result, correct, judged, bar: { pass: parts.reduce((a, p) => a + p.pass, 0), of: judged }, mastery: true, parts };
}
