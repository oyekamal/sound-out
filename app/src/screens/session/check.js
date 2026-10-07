// Check: the lesson's items. Free response -> self-checked practice, never a gate (plan-v6: L5+ ship as practice).
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, reveal, selfMark } from './kit.js';

export async function check(ctx, S) {
  const C = S.check; const id = S.id; const marks = {};
  const s = ctx.stage();
  s.append(h('h2', {}, 'Check yourself'), h('p', { class: 'ss-instr' }, 'Answer each one, then look at a good answer and mark yourself honestly. This is practice: nothing is locked.'));
  C.items.forEach((it, i) => {
    s.append(h('div', { class: 'ss-card ss-item', 'data-i': i }, h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, `${i + 1}. ${it.q}`), voice(`ss:${id}:check:${i}`, 'Hear the question')),
      reveal(it.a, { fallback: it.kind === 'self' ? 'Answer it honestly for yourself.' : 'Practice: check it against the text or the word list above, or ask someone to listen.' }),
      selfMark(m => { marks[i] = m; mark('ss-self', { block: 'check', i, m }); })));
  });
  if (C.support || C.challenge) s.append(h('details', { class: 'ss-card' }, h('summary', {}, 'Need more, or want a challenge?'),
    C.support ? h('p', {}, h('b', {}, 'Support: '), C.support) : null, C.challenge ? h('p', {}, h('b', {}, 'Challenge: '), C.challenge) : null));
  await ctx.next();
  const vals = Object.values(marks);
  return { items: C.items.length, had: vals.filter(v => v === 'yes').length, nearly: vals.filter(v => v === 'close').length, bar: C.bar };
}
