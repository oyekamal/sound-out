// Level 1 extra steps, registered in session.js: L1_STEPS[step](ctx) -> undefined, or a check result
// ({ result, correct, judged, bar, gate? }) that the session treats like "Show what you know".
// Every judged pick below is an `.l1-opts .opt` card; the right one carries data-ok (the test driver reads it).
import { play, wait, mark, stop } from '../audio.js';
import { h, icon, btn, ICON } from '../ui.js';
import { teacher } from '../teacher.js';
import { oral, oralCheck } from './l1oral.js';
import { names, bdpq } from './l1review.js';
import { mastery } from './l1mastery.js';

export const L1_STEPS = { oral, oralCheck, names, bdpq, mastery };

export const shuffle = a => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

// One choice: cards = [{ key?: audio clip, body?: node, ok: bool, id }]. `test` = one attempt, no retry.
// Teaching mode: a wrong pick says "try again" and the learner picks again; only the first pick is scored.
// `model`: the clip(s) that model the right answer after a miss ("Not quite ... <model> ... Now you try"); default = the right card's own clip.
const GENERIC = /^(This one|This many)$/;
// a pill's accessible name. A real visible label ("Its name", "Its sound") stays in the name; the generic ones get "option N".
// Pre-reader picture/sound cards have no printed word, so they are only ever "option N" (the name never gives the answer away).
const pillName = (c, i, cards) => (c.label && !GENERIC.test(c.label) ? `Choose ${c.label}` : `${c.label || 'This one'}, option ${i + 1}`);
export const choose = (stage, cards, opts) => choice(stage, cards, opts).start();
// choice() mounts the cards at once, invisible (visibility:hidden keeps their space, so nothing jumps while the prompt
// is spoken); start() shows them, plays the options and waits for the pick.
export function choice(stage, cards, { test = false, autoplay = true, cls = 'two', model = null, carrier = null } = {}) {
  const row = h('div', { class: `options l1-opts ${cls}` });
  let first = null, tries = 0, resolve; const done = new Promise(r => { resolve = r; });
  const els = cards.map((c, i) => {
    const el = h('div', { class: 'opt', 'data-ok': c.ok ? '1' : null, 'data-id': c.id || null },
      // the picture IS the tap-to-hear target (small speaker glyph in its corner); no picture = the big speaker button is the card
      c.key && c.body ? h('button', { class: 'opt-play pic-play', 'aria-label': `Option ${i + 1}: play`, onclick: () => play(c.key) }, c.body, h('span', { class: 'pic-glyph', html: ICON.speaker }))
        : c.key ? h('button', { class: 'opt-play', 'aria-label': `Option ${i + 1}: play`, onclick: () => play(c.key) }, icon('speaker')) : (c.body || null),
      // unique name per pill: a visible label stays in the name ("Choose Its name"), a generic one gets its position; the picture/speaker (the answer) is never named
      btn(c.label || 'This one', c.icon ?? (c.say ? null : 'check'), { class: 'opt-pick', disabled: true, say: c.say || 'ui:thisOne', 'aria-label': pillName(c, i, cards) }));
    el.setAttribute('role', 'group'); el.setAttribute('aria-label', `Option ${i + 1}`);
    el.querySelector('.opt-pick').addEventListener('click', async () => {
      if (first === null) first = !!c.ok;
      stop();
      el.classList.add(c.ok ? 'right' : 'wrong');
      mark('l1-pick', { id: c.id, ok: !!c.ok, test });
      if (c.ok || test) {
        els.forEach(x => x.querySelector('.opt-pick').disabled = true);
        if (!c.ok && test) teacher.miss();
        if (c.ok && !test) await teacher.right({ kind: 'pick', tries: tries ? 2 : 1 });
        resolve();
      } else {
        el.querySelector('.opt-pick').disabled = true;
        const right = cards.find(x => x.ok);
        await teacher.wrong({ first: tries++ === 0, carrier, model: model || (right?.key ? [right.key] : []) });
      }
    });
    return el;
  });
  row.append(...els); row.classList.add('pending'); row.inert = true; row.setAttribute('aria-disabled', 'true');
  stage.append(row);
  const hearAll = async () => { for (const [i, c] of cards.entries()) if (c.key) { els[i].classList.add('hl'); const ok = await play(c.key); els[i].classList.remove('hl'); if (ok === false) return false; await wait(200); } return true; };
  const pointRight = () => teacher.point(els.find(x => x.dataset.ok)?.querySelector('.opt-pick'));
  // a stall in a TEACHING item points at the right card after the re-prompt; in a test it only nudges (no pointing)
  const start = async () => {
    row.classList.remove('pending'); row.inert = false; row.removeAttribute('aria-disabled');
    teacher.setIdle({ nudge: 'ui:idlePick', hint: test ? null : pointRight });
    if (autoplay) await hearAll();
    els.forEach(x => x.querySelector('.opt-pick').disabled = false);
    if (autoplay) teacher.setExtra(hearAll);   // the ear button: prompt, stimulus, then each option again
    await done;
    return { judged: true, correct: first && !teacher.consumeHinted() };
  };
  return { start };
}
export const sounds = async (keys, gap = 450) => { for (const k of keys) { if ((await play(k)) === false) return false; await wait(gap); } return true; };
