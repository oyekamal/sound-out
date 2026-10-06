// Warm-up: flash known letters ("what does it say?") — the learner picks the sound — plus due review cards.
import { play, mark } from '../audio.js';
import { h, speaker } from '../ui.js';
import { g2p } from '../content.js';

const shuffle = a => [...a].sort(() => Math.random() - 0.5);
const OTHER = ['m', 'd', 'o', 'e', 'b', 'f', 'l'];

export async function warmLetter(ctx, letter, known) {
  const s = ctx.stage();
  const pool = shuffle([letter, ...shuffle([...known, ...OTHER].filter(x => x !== letter)).slice(0, 2)]);
  s.append(h('h2', {}, 'What does it say?'), h('div', { class: 'lettercard small' }, letter));
  const row = h('div', { class: 'options three' });
  let first = null, resolve; const done = new Promise(r => { resolve = r; });
  pool.forEach((l, i) => {
    const card = h('div', { class: 'opt', 'data-sound': l },
      speaker(`ph:${g2p[l]}`, { label: `Sound ${i + 1}` }),
      h('button', { class: 'opt-pick' }, 'This one'));
    card.querySelector('.opt-pick').addEventListener('click', async () => {
      const ok = l === letter; if (first === null) first = ok;
      mark('warm-pick', { letter, pick: l, correct: ok });
      card.classList.add(ok ? 'right' : 'wrong');
      if (ok) { await play('ui:good'); resolve(); } else await play('ui:tryAgain');
    });
    row.append(card);
  });
  s.append(row);
  await ctx.instruct('ui:warmIntro');
  for (const l of pool) await play(`ph:${g2p[l]}`);
  await done;
  const r = { judged: true, correct: first };
  await ctx.record(`letter:${letter}`, 'letter', r);
  return r;
}
