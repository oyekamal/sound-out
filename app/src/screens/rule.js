// Levels 2-4 rule card: the lesson's own rule in two or three plain sentences (FLOSS, -es, -ed, silent e, drop-e,
// open syllables, soft c/g, consonant-le, -tion, syllable division, suffix spelling, the word-attack routine).
import { play, mark } from '../audio.js';
import { h, speaker } from '../ui.js';
import { entry } from '../content.js';
import { decorate } from './tiles.js';
import { teacher } from '../teacher.js';

export async function rule(ctx) {
  const r = ctx.lesson.rule; if (!r) return;
  const s = ctx.stage();
  const ex = h('div', { class: 'examples' });
  for (const w of r.examples || []) {
    const e = entry(w); if (!e) continue;
    const b = h('button', { class: 'ex printed', 'data-w': w }, ...e.g.map((g, i) => h('span', { class: 'g', 'data-i': i }, g)));
    decorate(b, e);
    b.addEventListener('click', () => { mark('rule-word', { word: w }); play(`w:${w}`); });
    ex.append(b);
  }
  s.append(h('h2', {}, r.title), h('div', { class: 'rulecard' }, h('p', {}, r.text)), speaker(`rule:${ctx.lesson.id}`, { label: 'Hear the rule' }), ex);
  await ctx.instruct('ui:ruleIntro', { stim: () => play(`rule:${ctx.lesson.id}`), nudge: 'ui:idleTap' });
  await ctx.next();
}
