// Home: Track A = Pebble, the village, stickers and the sitting path. Track B = a plain lesson list and words to remember.
import { h, icon, pebble, village } from './ui.js';
import { play } from './audio.js';
import { LESSONS } from './content.js';
import { states, LABEL } from './path.js';
import * as db from './db.js';

export async function home(app, profile) {
  const prog = await db.progress(profile.id);
  const track = profile.track;
  const st = states(prog, track);
  const s = h('div', { class: `home track-${track}` });
  const days = (prog.days || []).length;
  s.append(h('header', { class: 'homehdr' },
    h('div', { class: 'brand' }, 'Sound Out'),
    h('div', { class: 'days', title: 'Days practised (never resets)' }, h('b', {}, String(days)), ' ', days === 1 ? 'day practised' : 'days practised'),
    h('button', { class: 'btn ghost small', onclick: () => app.onboarding() }, 'Who is reading?')));
  if (track === 'A') {
    s.append(h('div', { class: 'hero' }, pebble('wave'), h('div', {}, h('h1', {}, 'Your sounds'), h('p', { class: 'muted' }, 'Each new sound adds to your village.'))),
      village(prog.village), h('div', { class: 'stickers', 'aria-label': 'Stickers' }, ...(prog.stickers || []).map(x => h('span', {}, x))));
  } else {
    s.append(h('h1', {}, 'Lessons'), h('p', { class: 'muted' }, `Words you can read now: ${countWords(prog)}`));
  }
  for (const l of LESSONS) {
    const ls = st.filter(x => x.lessonId === l.id);
    const lstate = prog.lessons[l.id]?.state;
    const sec = h('section', { class: 'lesson' }, h('h3', {}, track === 'A' ? `Sounds: ${l.title}` : `Lesson ${l.id.slice(1)} · ${l.title}`,
      lstate === 'checked' ? h('span', { class: 'badge' }, 'checked by tapping') : lstate === 'still_learning' ? h('span', { class: 'badge soft' }, 'still learning') : null));
    const path = h('div', { class: track === 'A' ? 'path' : 'list' });
    for (const x of ls) {
      const label = x.label || (x.new?.length ? x.new.join(' ') : LABEL[track][x.id] || x.id);
      const b = h('button', { class: `node ${x.state}${x.new?.length ? '' : ' wide'}`, 'data-key': x.key, disabled: x.state === 'locked' },
        x.state === 'locked' ? icon('lock') : x.state === 'done' ? icon('check') : null, h('span', {}, label));
      b.addEventListener('click', () => app.sitting(x.key));
      path.append(b);
    }
    sec.append(path); s.append(sec);
  }
  if (track === 'B' && (prog.words || []).length) s.append(h('section', { class: 'lesson' }, h('h3', {}, 'Words to remember'), h('p', { class: 'wordlist' }, prog.words.join(' · '))));
  s.append(h('p', { class: 'muted small foot-note' }, 'Prototype: all voices are a computer voice for now; pictures are placeholders.'));
  app.mount(s);
}

function countWords(prog) {
  // real words from passed lessons' blend lists (Track B "words you can read now")
  const done = new Set(Object.keys(prog.sittings).filter(k => prog.sittings[k].passed).map(k => k.split(':')[0]));
  return new Set(LESSONS.filter(l => done.has(l.id)).flatMap(l => l.blendList?.real || [])).size;
}
