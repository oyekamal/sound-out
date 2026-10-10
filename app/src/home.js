// Home: Track A = Tilo, the village, stickers and the sitting path. Track B = a plain lesson list and words to remember.
import { h, icon, btn, village } from './ui.js';
import { teacher } from './teacher.js';
import { askGrownup } from './grownup.js';
import { tilo } from './tilo.js';
import { LESSONS } from './content.js';
import { states, LABEL } from './path.js';
import * as db from './db.js';
import { level2Teaser } from './screens/l1home.js';

export async function home(app, profile) {
  const prog = await db.progress(profile.id);
  const track = profile.track;
  const st = states(prog, track);
  const s = h('div', { class: `home track-${track}` });
  const days = (prog.days || []).length;
  s.append(h('header', { class: 'homehdr' },
    h('div', { class: 'brand' }, 'Sound Out'),
    h('div', { class: 'days', title: 'Days practised (never resets)' }, h('b', {}, String(days)), ' ', days === 1 ? 'day practised' : 'days practised'),
    btn('Who is reading?', 'child', { class: 'btn ghost small', say: 'ui:who', onclick: () => app.onboarding() })));
  if (track === 'A') {
    s.append(h('div', { class: 'hero' }, h('div', { class: 'tilo-slot' }), h('div', {}, h('h1', {}, 'Your sounds'), h('p', { class: 'muted' }, 'Each new sound adds to your village.'))),
      village(prog.village), h('div', { class: 'stickers', 'aria-label': 'Stickers' }, ...(prog.stickers || []).map(x => h('span', {}, x))));
  } else {
    s.append(h('h1', {}, 'Lessons'), h('p', { class: 'muted' }, `Words you can read now: ${countWords(prog)}`));
  }
  const LEVEL_NAME = { 2: 'Sounds Together', 3: 'Long Vowels', 4: 'Longer Words' };
  let lastLevel = 1;
  for (const l of LESSONS) {
    if ((l.level || 1) !== lastLevel) {   // a level card before the first lesson of Level 2, 3, 4 (locked until the level before is checked)
      lastLevel = l.level || 1;
      const open = st.some(x => x.lessonId === l.id && x.state !== 'locked');
      s.append(h('section', { class: `level-card${open ? '' : ' locked'}`, 'data-level': String(lastLevel) },
        h('h2', { 'data-say': `ui:lvl${lastLevel}${open ? '' : ',ui:lockedNote'}` }, `Level ${lastLevel}${LEVEL_NAME[lastLevel] ? ` · ${LEVEL_NAME[lastLevel]}` : ''}`),
        h('p', { class: 'muted small' }, open ? 'Open. Pick up where you stopped.' : `Opens when you pass the Level ${lastLevel - 1} check.`)));
    }
    const ls = st.filter(x => x.lessonId === l.id);
    const lstate = prog.lessons[l.id]?.state;
    const sec = h('section', { class: 'lesson' }, h('h3', {}, track === 'A' ? `Sounds: ${l.title}` : `Lesson ${l.id.slice(1)} · ${l.title}`,
      lstate === 'checked' ? h('span', { class: 'badge' }, 'checked by tapping') : lstate === 'still_learning' ? h('span', { class: 'badge soft' }, 'still learning') : null));
    const path = h('div', { class: track === 'A' ? 'path' : 'list' });
    for (const x of ls) {
      const label = x.label || (x.new?.length ? x.new.join(' ') : LABEL[track][x.id] || x.id);
      const say = x.new?.length ? `name:${x.new[0]}` : ({ D: 'ui:lblWords', R: 'ui:lblRead', L: 'ui:lblListen', X: track === 'A' ? 'ui:lblCheck' : 'ui:lblCheckB' })[x.id] || null;
      const b = h('button', { class: `node ${x.state}${x.new?.length ? '' : ' wide'}`, 'data-key': x.key, 'data-say': x.state === 'locked' ? 'ui:lockedNote' : say, disabled: x.state === 'locked' },
        x.state === 'locked' ? icon('lock') : x.state === 'done' ? icon('check') : null, h('span', {}, label));
      b.addEventListener('click', () => app.sitting(x.key));
      path.append(b);
    }
    sec.append(path); s.append(sec);
  }
  s.append(level2Teaser(prog, track));
  if (track === 'B' && (prog.words || []).length) s.append(h('section', { class: 'lesson' }, h('h3', {}, 'Words to remember'), h('p', { class: 'wordlist' }, prog.words.join(' · '))));
  s.append(h('div', { class: 'row foot-note' }, btn('For grown-ups', 'lock', { class: 'btn ghost small grownups', say: 'ui:forGrownups', onclick: async () => { if (await askGrownup()) app.privacyInfo(); } })));
  app.mount(s);
  if (track === 'A') tilo.dock(s.querySelector('.tilo-slot'));
  // Home speaks: "Welcome back" on a return visit, then which node to tap; a stall points at that node
  const so = window.__so; const back = days > 0 && !so.homeVisited; so.homeVisited = true;
  const go = track === 'A' ? 'ui:homeGoA' : 'ui:homeGoB';
  const openNode = () => s.querySelector('.node.open');
  teacher.track(track);
  teacher.prompt(back ? ['ui:welcomeBack', go] : [go], { nudge: go, hint: () => { const n = openNode(); n?.scrollIntoView?.({ block: 'center' }); teacher.point(n); }, replay: () => teacher.seq([go]) });
}

function countWords(prog) {
  // real words from passed lessons' blend lists (Track B "words you can read now")
  const done = new Set(Object.keys(prog.sittings).filter(k => prog.sittings[k].passed).map(k => k.split(':')[0]));
  return new Set(LESSONS.filter(l => done.has(l.id)).flatMap(l => l.blendList?.real || [])).size;
}
