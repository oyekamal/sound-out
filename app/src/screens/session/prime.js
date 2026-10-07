// Prime the topic: 2-3 facts and one orienting question (text now, audio later).
import { h } from '../../ui.js';
import { voice } from './kit.js';

export async function prime(ctx, S) {
  const P = S.prime; const id = S.id;
  const s = ctx.stage();
  s.append(h('h2', {}, 'Before you read'));
  if ((P.facts || []).length) s.append(h('ol', { class: 'ss-facts' }, ...P.facts.map((f, i) => h('li', {}, h('span', {}, f[0].toUpperCase() + f.slice(1)), voice(`ss:${id}:prime:${i}`, 'Hear this fact')))));
  if (P.question) s.append(h('div', { class: 'ss-card ss-orient' }, h('p', { class: 'ss-label' }, 'Think about this'), h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, P.question), voice(`ss:${id}:prime:q`, 'Hear the question')),
    h('p', { class: 'muted small' }, 'No right answer. Say what you think, then read.')));
  await ctx.next();
}
