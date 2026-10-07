// Knowledge text: long text chunked by paragraph, tap a sentence to highlight (and hear it, once audio exists); questions after.
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, sentencePara, reveal, selfMark } from './kit.js';
import { passagesFor } from './data.js';

export async function text(ctx, S) {
  const id = S.id;
  for (const mv of S.text.moves || []) {
    if (!mv.paragraphs.length) continue;
    const s = ctx.stage();
    s.append(h('h2', {}, `The move: ${mv.title}`), h('div', { class: 'ss-card' }, ...mv.paragraphs.map(p => h('p', {}, p))));
    await ctx.next();
  }
  const all = S.text.passages;
  for (const ps of passagesFor(S, ctx.track)) {
    const j = all.indexOf(ps);
    const s = ctx.stage();
    const box = h('div', { class: `ss-passage${ps.script ? ' script' : ''}` });
    let shown = 0;
    const more = h('button', { class: 'btn small ss-more' }, 'Read on');
    const count = h('span', { class: 'muted small' });
    const showNext = () => {
      box.append(h('div', { class: 'ss-chunk', 'data-p': shown }, sentencePara(ps.paragraphs[shown], `ss:${id}:text:${j}:${shown}`), voice(`ss:${id}:text:${j}:${shown}`, 'Hear this paragraph')));
      shown++; count.textContent = `${shown} of ${ps.paragraphs.length}`;
      mark('ss-chunk', { j, shown });
      if (shown >= ps.paragraphs.length) { more.hidden = true; ctx.enableNext(); }
      box.lastChild.scrollIntoView?.({ block: 'nearest' });
    };
    more.addEventListener('click', showNext);
    s.append(h('h2', {}, ps.title || 'Read'), h('p', { class: 'ss-instr' }, 'Read one part at a time. Tap a sentence to mark it.'), box, h('div', { class: 'row' }, more, count));
    showNext();
    await ctx.next({ disabledUntil: () => shown >= ps.paragraphs.length });
    if (ps.questions.length) {
      const q = ctx.stage();
      q.append(h('h2', {}, 'Questions'), h('p', { class: 'ss-instr' }, 'Think, then tap to see a good answer. This is practice.'));
      ps.questions.forEach((x, i) => q.append(h('div', { class: 'ss-card' }, h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, x.q), voice(`ss:${id}:text:${j}:q${i}`, 'Hear the question')),
        reveal(x.a), selfMark(m => mark('ss-self', { block: 'text', j, i, m })))));
      await ctx.next();
    }
  }
}
