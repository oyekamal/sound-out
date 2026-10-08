// Level 1 extra steps, registered in session.js: L1_STEPS[step](ctx) -> undefined, or a check result
// ({ result, correct, judged, bar, gate? }) that the session treats like "Show what you know".
// Every judged pick below is an `.l1-opts .opt` card; the right one carries data-ok (the test driver reads it).
import { play, wait, mark, stop } from '../audio.js';
import { h, icon } from '../ui.js';
import { oral, oralCheck } from './l1oral.js';
import { names, bdpq } from './l1review.js';
import { mastery } from './l1mastery.js';

export const L1_STEPS = { oral, oralCheck, names, bdpq, mastery };

export const shuffle = a => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

// One choice: cards = [{ key?: audio clip, body?: node, ok: bool, id }]. `test` = one attempt, no retry.
// Teaching mode: a wrong pick says "try again" and the learner picks again; only the first pick is scored.
export async function choose(stage, cards, { test = false, autoplay = true, cls = 'two' } = {}) {
  const row = h('div', { class: `options l1-opts ${cls}` });
  let first = null, resolve; const done = new Promise(r => { resolve = r; });
  const els = cards.map((c, i) => {
    const el = h('div', { class: 'opt', 'data-ok': c.ok ? '1' : null, 'data-id': c.id || null },
      c.key ? h('button', { class: 'opt-play', 'aria-label': `Option ${i + 1}: play`, onclick: () => play(c.key) }, icon('speaker'), h('span', { class: 'n' }, String(i + 1))) : null,
      c.body || null,
      h('button', { class: 'opt-pick', disabled: true }, c.label || 'This one'));
    el.querySelector('.opt-pick').addEventListener('click', async () => {
      if (first === null) first = !!c.ok;
      stop();
      el.classList.add(c.ok ? 'right' : 'wrong');
      mark('l1-pick', { id: c.id, ok: !!c.ok, test });
      if (c.ok || test) { els.forEach(x => x.querySelector('.opt-pick').disabled = true); if (c.ok && !test) await play('ui:good'); resolve(); }
      else { el.querySelector('.opt-pick').disabled = true; await play('ui:tryAgain'); }
    });
    return el;
  });
  row.append(...els);
  stage.append(row);
  if (autoplay) for (const [i, c] of cards.entries()) if (c.key) { els[i].classList.add('hl'); await play(c.key); els[i].classList.remove('hl'); await wait(200); }
  els.forEach(x => x.querySelector('.opt-pick').disabled = false);
  await done;
  return { judged: true, correct: first };
}
export const sounds = async (keys, gap = 450) => { for (const k of keys) { await play(k); await wait(gap); } };
