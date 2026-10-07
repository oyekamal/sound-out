// Runs one Level 5-7 practice lesson through the session template. No mini check, no gate: practice.
import { h, icon } from '../../ui.js';
import { stop, mark } from '../../audio.js';
import * as db from '../../db.js';
import { loadSession, SESSIONS } from './data.js';
import { warm } from './warm.js';
import { word } from './word.js';
import { fluency } from './fluency.js';
import { prime } from './prime.js';
import { text } from './text.js';
import { discuss } from './discuss.js';
import { write } from './write.js';
import { check } from './check.js';

const SCREEN = { warm, word, fluency, prime, text, discuss, write, check };
export const NAMES = { warm: 'Warm-up', word: 'Word work', fluency: 'Fluency', prime: 'Prime the topic', text: 'Knowledge text', discuss: 'Discussion', write: 'Write to read', check: 'Check' };

export async function activeProfile() {
  const id = await db.setting('active');
  return id ? db.get('profiles', id) : null;
}

export async function runPractice(app, id, { only } = {}) {
  stop();
  const S = await loadSession(id);
  const profile = await activeProfile();
  const track = profile?.track || 'B';
  const root = h('div', { class: `sitting ss-session track-${track}`, 'data-lesson': id });
  const bar = h('div', { class: 'progress' }, h('i'));
  const close = h('button', { class: 'close', 'aria-label': 'Stop and go back', onclick: () => { stop(); window.__so.practice.library(); } }, '×');
  const body = h('main', { class: 'stage' }); const foot = h('footer', { class: 'foot' });
  root.append(h('header', { class: 'hdr' }, close, bar, h('span', { class: 'ss-tag' }, 'Practice')), body, foot);
  app.mount(root);
  const ctx = {
    track, S,
    stage() { body.replaceChildren(); foot.replaceChildren(); window.scrollTo(0, 0); const s = h('div', { class: 'screen ss-screen', 'data-step': `ss-${ctx.step}`, 'data-lesson': id }); body.append(s); return s; },
    enableNext: () => {},
    next({ disabledUntil } = {}) {
      return new Promise(res => {
        const btn = h('button', { class: 'btn primary next' }, 'Next');
        const update = () => { btn.disabled = disabledUntil ? !disabledUntil() : false; };
        ctx.enableNext = update; update();
        btn.addEventListener('click', () => { stop(); res(); });
        foot.append(btn);
      });
    },
  };
  const steps = only ? S.screens.filter(x => only.includes(x)) : S.screens;
  let result = null;
  for (const [k, st] of steps.entries()) {
    ctx.step = st; bar.firstChild.style.width = Math.round(100 * k / steps.length) + '%';
    mark('step', { key: `${id}:practice`, step: `ss-${st}` });
    const r = await SCREEN[st](ctx, S);
    if (st === 'check') result = r;
  }
  if (profile) {
    const prog = await db.progress(profile.id);
    prog.practice = { ...(prog.practice || {}), [id]: { done: true, at: Date.now(), check: result } };
    const today = new Date().toISOString().slice(0, 10);
    prog.days = [...new Set([...(prog.days || []), today])];
    await db.saveProgress(prog);
  }
  mark('practice-end', { key: id, result });
  return endScreen(app, S, result);
}

function endScreen(app, S, result) {
  const i = SESSIONS.findIndex(x => x.id === S.id); const nxt = SESSIONS[i + 1];
  const s = h('div', { class: 'endscreen ss-end', 'data-lesson': S.id });
  s.append(h('h2', {}, 'Practice done'), h('p', { class: 'prompt' }, S.title));
  if (result) s.append(h('p', { class: 'score' }, `You marked ${result.had} of ${result.items} as "I had it"` + (result.nearly ? `, ${result.nearly} nearly` : '') + '.'),
    h('p', { class: 'muted small' }, (result.bar ? `The course bar is ${result.bar}. ` : '') + 'Practice only: nothing is locked by this.'));
  const row = h('div', { class: 'row' });
  if (nxt) row.append(h('button', { class: 'btn primary ss-nextlesson', onclick: () => runPractice(app, nxt.id) }, `Next: ${nxt.id}`));
  row.append(h('button', { class: 'btn ghost ss-tolib', onclick: () => window.__so.practice.library() }, 'Library'));
  s.append(row);
  app.mount(s);
}
