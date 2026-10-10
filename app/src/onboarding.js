// First launch: ONE screen, "Who is reading?" (child / grown-up), spoken in English.
// Then straight into the first sitting (no language-help step: no help packs ship with the app).
import { h, icon } from './ui.js';
import { teacher } from './teacher.js';
import * as db from './db.js';

export async function onboarding(app) {
  const profiles = await db.all('profiles');
  const s = h('div', { class: 'onboard' });
  const choose = async track => {
    const p = { id: 'p' + Date.now().toString(36), track, createdAt: Date.now(), name: `${track === 'A' ? 'Child' : 'Grown-up'} ${profiles.filter(x => x.track === track).length + 1}` };
    await db.put('profiles', p);
    await db.setting('active', p.id);
    teacher.track(track);
    app.firstSitting(p);
  };
  s.append(h('h1', {}, 'Who is reading?'),
    h('div', { class: 'who' },
      h('button', { class: 'whocard child', 'data-track': 'A', 'data-say': 'ui:child', onclick: () => choose('A') }, icon('child', 'big-icon'), h('span', {}, 'A child')),
      h('button', { class: 'whocard adult', 'data-track': 'B', 'data-say': 'ui:adult', onclick: () => choose('B') }, icon('adult', 'big-icon'), h('span', {}, 'A grown-up'))));
  if (profiles.length) s.append(h('div', { class: 'existing' }, h('p', { class: 'muted' }, 'Or carry on:'),
    ...profiles.map(p => h('button', { class: 'btn ghost', onclick: async () => { await db.setting('active', p.id); app.boot(); } }, p.name))));
  app.mount(s);
  // a first launch says hello once, then asks who is reading; the cards speak when pressed and held
  const first = !profiles.length && !window.__so.hello; window.__so.hello = true;
  await teacher.prompt(first ? ['ui:hello', 'ui:who'] : ['ui:who'], { nudge: 'ui:who', hint: () => teacher.point(...s.querySelectorAll('.whocard')), replay: () => teacher.seq(['ui:who', 'ui:child', 'ui:adult'], 150) });
}
