// E11 "Show what you know": the lesson's own check items through the tap gate (+ dictation through Spell it).
// Score = first attempts on judged items; the lesson's bar decides. A miss never locks the path.
import { play, mark } from '../audio.js';
import { h } from '../ui.js';
import { options, entry } from '../content.js';
import { gate } from '../gate.js';
import { spellWord } from './spell.js';

export function checkItems(lesson) {
  const c = lesson.check || {};
  const uniq = a => [...new Set((a || []).map(w => w.toLowerCase()))];
  const real = uniq(c.real).filter(w => options[w]), pseudo = uniq(c.pseudo).filter(w => options[w]);
  let dict = uniq(c.dictation).filter(w => entry(w));
  const of = c.bar?.of || real.length + pseudo.length + dict.length;
  // L1.02: only 3 real words exist; the course repeats them, the app dictates them instead (plan §3.6)
  for (const w of real) if (real.length + pseudo.length + dict.length < of && !dict.includes(w)) dict.push(w);
  const items = [];
  for (let i = 0; i < Math.max(real.length, pseudo.length); i++) { if (real[i]) items.push({ w: real[i], kind: 'real' }); if (pseudo[i]) items.push({ w: pseudo[i], kind: 'pseudo' }); }
  dict.forEach(w => items.push({ w, kind: 'dictation' }));
  const spare = (lesson.blendList?.pseudo || []).concat(lesson.blendList?.real || []).map(w => w.toLowerCase()).filter(w => options[w] && !items.some(x => x.w === w));
  const bar = c.bar?.pass ? { pass: c.bar.pass, of: c.bar.of } : { pass: Math.ceil((c.bar?.ratio || 0.9) * items.length), of: items.length };
  return { items, spare, bar };
}

export async function check(ctx) {
  const { items, spare, bar } = checkItems(ctx.lesson);
  const s0 = ctx.stage();
  s0.append(h('h2', {}, 'Show what you know'), h('p', { class: 'prompt' }, 'Some are made-up words. Just sound them out.'));
  await ctx.instruct('ui:checkIntro');
  await ctx.next();
  let correct = 0, judged = 0, timeouts = 0;
  const queue = [...items];
  mark('check-start', { lesson: ctx.lesson.id, items: items.map(i => i.w), bar });
  while (queue.length) {
    const it = queue.shift();
    let r;
    if (it.kind === 'dictation') r = await spellWord(ctx, it.w, ctx.known());
    else { r = await gate(ctx, it.w, it.kind); await ctx.record(it.w, it.kind, r); }
    if (!r.judged) {
      timeouts++;
      if (timeouts > 2) { mark('check-end', { result: 'unfinished' }); return finish(ctx, 'unfinished', correct, judged, bar); }
      const fresh = spare.shift(); if (fresh) queue.push({ w: fresh, kind: entry(fresh).kind });
      continue;
    }
    judged++; if (r.correct) correct++;
  }
  const pass = correct / judged >= bar.pass / bar.of;
  mark('check-end', { result: pass ? 'checked' : 'miss', correct, judged, bar });
  return finish(ctx, pass ? 'checked' : 'miss', correct, judged, bar);
}

async function finish(ctx, result, correct, judged, bar) {
  const s = ctx.stage();
  const dots = h('div', { class: 'dots' }, ...Array.from({ length: judged }, (_, i) => h('i', { class: i < correct ? 'on' : '' })));
  const msg = { checked: 'You did it! The next part is open.', miss: "We'll practise these again. The next part is still open.", unfinished: "Let's finish this tomorrow." }[result];
  s.append(h('h2', {}, result === 'checked' ? 'Checked by tapping' : 'Show what you know'), dots,
    h('p', { class: 'score' }, `${correct} of ${judged} on the first try · bar ${bar.pass}/${bar.of}`), h('p', { class: 'prompt' }, msg));
  await play({ checked: 'ui:checkPass', miss: 'ui:checkMiss', unfinished: 'ui:finishTomorrow' }[result]);
  await ctx.next();
  return { result, correct, judged, bar };
}
