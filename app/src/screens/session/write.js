// Write to read: type (or build from word tiles) a short answer, then compare with the model answer and self-check.
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, selfMark, shuffle } from './kit.js';

export async function write(ctx, S) {
  const W = S.write; const id = S.id;
  const s = ctx.stage();
  const ta = h('textarea', { class: 'ss-text', rows: 5, placeholder: 'Write your answer here…', 'aria-label': 'Your answer' });
  s.append(h('h2', {}, 'Write to read'), h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, W.task), voice(`ss:${id}:write`, 'Hear the task')), ta);
  const first = (W.model || '').split(/(?<=[.!?])\s+/)[0] || '';
  const toks = first.split(/\s+/).filter(Boolean);
  if (toks.length >= 4 && toks.length <= 16) {
    const tiles = h('div', { class: 'ss-tray ss-wtiles', hidden: true }, ...shuffle(toks, toks.length).map(t => {
      const b = h('button', { class: 'ss-tile small' }, t);
      b.addEventListener('click', () => { ta.value = (ta.value ? ta.value + ' ' : '') + t; b.disabled = true; mark('ss-wtile', { t }); });
      return b;
    }));
    const tb = h('button', { class: 'btn ghost small ss-tilesbtn' }, 'Build it from word tiles instead');
    tb.addEventListener('click', () => { tiles.hidden = false; tb.hidden = true; });
    s.append(tb, tiles);
  }
  const cmp = h('button', { class: 'btn small ss-compare' }, 'Compare with a model answer');
  const res = h('div', { class: 'ss-card ss-model', hidden: true },
    h('p', { class: 'ss-label' }, W.model ? 'Model answer' : 'Check your answer'),
    W.model ? h('p', {}, W.model) : h('ul', {}, h('li', {}, 'Does it answer the task in your own words?'), h('li', {}, 'Does it use the word or idea the task asks for?'), h('li', {}, 'Could someone who did not read the text understand it?')),
    h('p', { class: 'muted small' }, 'Does yours say the same main thing? Practice only: you decide.'),
    selfMark(m => mark('ss-self', { block: 'write', m })));
  cmp.addEventListener('click', () => { res.hidden = false; cmp.hidden = true; mark('ss-compare', { len: ta.value.length }); ctx.enableNext(); });
  s.append(h('div', { class: 'row' }, cmp), res);
  await ctx.next({ disabledUntil: () => cmp.hidden });
}
