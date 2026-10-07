// Levels 5-7 as PRACTICE (plan-v6: L5+ ship as practice in v1). Registered by one import in main.js.
// Adds: a "Practice: Levels 5-7" section on Home (unlocked once the Level 4 mastery check is passed) and a Library
// that always opens every Level 5-7 lesson. Kept in its own folder so Level 1-4 files stay untouched.
import './session.css';
import { h, icon } from '../../ui.js';
import * as db from '../../db.js';
import { SESSIONS, LEVELS } from './data.js';
import { runPractice, activeProfile, NAMES } from './run.js';

const so = (window.__so = window.__so || { trace: [], missing: [] });
const app = () => so.app;
const LEVEL_NAME = { 5: 'Word parts and knowledge texts', 6: 'Text structures and reciprocal reading', 7: 'Reading like an expert' };

// Level 4 mastery check passed? (L4.16 recorded as "checked" by the Level 4 check; any L4.16 sitting passed also counts.)
export function level4Passed(prog) {
  if (prog?.lessons?.['L4.16']?.state === 'checked') return true;
  return Object.entries(prog?.sittings || {}).some(([k, v]) => k.startsWith('L4.16:') && v.passed);
}

async function library(level) {
  const profile = await activeProfile();
  const prog = profile ? await db.progress(profile.id) : {};
  const s = h('div', { class: `home ss-library track-${profile?.track || 'B'}` });
  s.append(h('header', { class: 'homehdr' }, h('div', { class: 'brand' }, 'Library'), h('button', { class: 'btn ghost small ss-home', onclick: () => app().home() }, 'Home')),
    h('p', { class: 'muted' }, 'Levels 5–7 are practice: open any lesson. Audio for these levels is coming; the speaker buttons say so.'));
  for (const lv of LEVELS) {
    if (level && lv !== level) continue;
    const sec = h('section', { class: 'lesson ss-level', 'data-level': lv }, h('h3', {}, `Level ${lv} · ${LEVEL_NAME[lv] || ''}`));
    const list = h('div', { class: 'list' });
    for (const x of SESSIONS.filter(y => y.level === lv)) {
      const done = prog.practice?.[x.id]?.done;
      const b = h('button', { class: `node ss-lesson${done ? ' done' : ''}`, 'data-id': x.id, title: x.screens.map(k => NAMES[k]).join(' · ') },
        done ? icon('check') : null, h('span', {}, `${x.id.slice(1)} · ${x.title}`));
      b.addEventListener('click', () => runPractice(app(), x.id));
      list.append(b);
    }
    sec.append(list); s.append(sec);
  }
  app().mount(s);
}

async function addToHome(el) {
  if (el.querySelector('.ss-practice') || !SESSIONS.length) return;
  const profile = await activeProfile();
  const prog = profile ? await db.progress(profile.id) : {};
  if (!el.isConnected || el.querySelector('.ss-practice')) return;
  const open = level4Passed(prog);
  const sec = h('section', { class: 'lesson ss-practice' }, h('h3', {}, `Practice: Levels ${LEVELS[0]}–${LEVELS[LEVELS.length - 1]}`, h('span', { class: 'badge soft' }, 'practice')));
  const path = h('div', { class: 'list' });
  for (const lv of LEVELS) {
    const n = SESSIONS.filter(x => x.level === lv).length;
    const done = SESSIONS.filter(x => x.level === lv && prog.practice?.[x.id]?.done).length;
    const b = h('button', { class: `node ss-levelcard ${open ? 'open' : 'locked'}`, 'data-level': lv, disabled: !open },
      open ? null : icon('lock'), h('span', {}, `Level ${lv} · ${n} lessons` + (done ? ` · ${done} done` : '')));
    b.addEventListener('click', () => library(lv));
    path.append(b);
  }
  sec.append(path);
  if (!open) sec.append(h('p', { class: 'muted small' }, 'These open after the Level 4 check. You can look at them now in the Library.'));
  sec.append(h('div', { class: 'row' }, h('button', { class: 'btn ghost small ss-libbtn', onclick: () => library() }, 'Library')));
  const foot = el.querySelector('.foot-note');
  foot ? el.insertBefore(sec, foot) : el.append(sec);
}

// Watch for the Home screen (rendered by home.js) and add the practice section; no edits to home.js needed.
new MutationObserver(() => { const el = document.querySelector('#app > .home:not(.ss-library)'); if (el) addToHome(el); })
  .observe(document.getElementById('app') || document.body, { childList: true });

so.practice = { library, open: id => runPractice(app(), id), sessions: SESSIONS };
