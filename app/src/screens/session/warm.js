// Retrieval warm-up: earlier words (tap each as you read it, then tap-the-word) or recall prompts (think, then check).
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, say, reveal, selfMark, shuffle } from './kit.js';

export async function warm(ctx, S) {
  const w = S.warm; const id = S.id;
  const words = [...(w.words || []), ...(w.heart || [])];
  if (words.length) {
    const s = ctx.stage();
    const seen = new Set();
    const grid = h('div', { class: 'ss-chips' }, ...words.map((x, i) => {
      const b = h('button', { class: 'ss-chip', 'data-w': x }, x);
      b.addEventListener('click', () => { b.classList.add('done'); seen.add(x); mark('ss-warm-read', { w: x }); say(`ss:${id}:warm:w${i}`); ctx.enableNext(); });
      return b;
    }));
    s.append(h('h2', {}, 'Warm-up: words you know'), h('p', { class: 'ss-instr' }, 'Read each word aloud, cold, no help. Then tap it.'), grid,
      h('p', { class: 'muted small' }, (w.heart || []).length ? `Heart words today: ${w.heart.join(', ')}` : 'Words from earlier lessons.'));
    await ctx.next({ disabledUntil: () => seen.size >= Math.min(words.length, 3) });
    // tap-the-word: hear (or, until audio arrives, see) a word and find it
    const pool = shuffle(words, id.length).slice(0, Math.min(3, words.length));
    for (const [k, target] of pool.entries()) {
      const s2 = ctx.stage();
      const i = words.indexOf(target);
      let ok; const found = new Promise(r => { ok = r; });
      const opts = shuffle(words, k + 3).slice(0, 4); if (!opts.includes(target)) opts[k % opts.length] = target;
      s2.append(h('h2', {}, 'Find the word'), voice(`ss:${id}:warm:w${i}`, 'Hear the word'),
        h('p', { class: 'ss-cue' }, 'Until the voice is ready: ', h('b', {}, target)),
        h('div', { class: 'ss-chips' }, ...opts.map(x => {
          const b = h('button', { class: 'ss-chip', 'data-w': x, 'data-target': x === target ? '1' : '' }, x);
          b.addEventListener('click', () => { mark('ss-tapword', { target, pick: x, correct: x === target }); if (x === target) { b.classList.add('right'); ok(); } else b.classList.add('wrong'); });
          return b;
        })));
      say(`ss:${id}:warm:w${i}`);
      await found; await ctx.next();
    }
  }
  if ((w.prompts || []).length) {
    const s = ctx.stage();
    s.append(h('h2', {}, words.length ? 'Remember' : 'Warm-up: remember'), h('p', { class: 'ss-instr' }, 'Answer from memory, out loud or on paper. Then check yourself.'));
    w.prompts.forEach((p, i) => {
      const card = h('div', { class: 'ss-card' }, h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, p), voice(`ss:${id}:warm:p${i}`, 'Hear the question')));
      const rv = reveal(null, { label: 'Done? Check yourself', fallback: 'Practice: if you were not sure, look back at the last lesson before you go on.' });
      card.append(rv, selfMark(m => mark('ss-self', { block: 'warm', i, m })));
      s.append(card);
    });
    await ctx.next();
  }
}
