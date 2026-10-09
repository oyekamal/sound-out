// Warm-up: flash known letters ("what does it say?") — the learner picks the sound — plus due review cards.
import { play, mark } from '../audio.js';
import { h, speaker, btn } from '../ui.js';
import { teacher } from '../teacher.js';
import { g2p } from '../content.js';

const shuffle = a => [...a].sort(() => Math.random() - 0.5);
const OTHER = ['m', 'd', 'o', 'e', 'b', 'f', 'l'];

export async function warmLetter(ctx, letter, known) {
  const s = ctx.stage();
  const pool = shuffle([letter, ...shuffle([...known, ...OTHER].filter(x => x !== letter)).slice(0, 2)]);
  s.append(h('h2', {}, 'What does it say?'), h('div', { class: 'lettercard small' }, letter));
  const row = h('div', { class: 'options three' });
  let first = null, tries = 0, resolve; const done = new Promise(r => { resolve = r; });
  pool.forEach((l, i) => {
    const card = h('div', { class: 'opt', 'data-sound': l },
      speaker(`ph:${g2p[l]}`, { label: `Sound ${i + 1}` }),
      btn('This one', 'check', { class: 'opt-pick', say: 'ui:thisOne' }));
    card.querySelector('.opt-pick').addEventListener('click', async () => {
      const ok = l === letter; if (first === null) first = ok;
      mark('warm-pick', { letter, pick: l, correct: ok });
      card.classList.add(ok ? 'right' : 'wrong');
      if (ok) { await teacher.right({ kind: 'pick', tries: tries ? 2 : 1 }); resolve(); }
      else await teacher.wrong({ first: tries++ === 0, carrier: 'ui:thisLetterSays', model: [`ph:${g2p[letter]}`] });   // "Not quite. This letter says /s/. Now you try."
    });
    row.append(card);
  });
  s.append(row);
  const cardOf = l => row.querySelector(`.opt[data-sound='${l}'] .opt-pick`);
  const hearAll = async () => { for (const l of pool) { if ((await play(`ph:${g2p[l]}`)) === false) return false; } return true; };
  await ctx.instruct('ui:warmIntro', { stim: hearAll, nudge: 'ui:idlePick', hint: () => teacher.point(cardOf(letter)) });
  await done;
  const r = { judged: true, correct: first && !teacher.consumeHinted() };
  await ctx.record(`letter:${letter}`, 'letter', r);
  return r;
}
