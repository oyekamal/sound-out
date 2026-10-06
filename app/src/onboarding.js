// First launch: ONE screen, "Who is reading?" (child / grown-up), spoken in English.
// Then an optional, skippable "help in your language?" grid. Then straight into the first sitting.
import { h, icon, speaker } from './ui.js';
import { play } from './audio.js';
import * as db from './db.js';

const LANGS = [['ur', 'اردو', 'Urdu'], ['es', 'Español', 'Spanish'], ['pt', 'Português', 'Portuguese']];

export async function onboarding(app) {
  const profiles = await db.all('profiles');
  const s = h('div', { class: 'onboard' });
  const choose = async track => {
    const p = { id: 'p' + Date.now().toString(36), track, createdAt: Date.now(), name: `${track === 'A' ? 'Child' : 'Grown-up'} ${profiles.filter(x => x.track === track).length + 1}` };
    await db.put('profiles', p);
    await db.setting('active', p.id);
    helpLang(app, p);
  };
  s.append(h('h1', {}, 'Who is reading?'), speaker('ui:who', { label: 'Hear it again' }),
    h('div', { class: 'who' },
      h('button', { class: 'whocard child', 'data-track': 'A', onclick: () => choose('A') }, icon('child', 'big-icon'), h('span', {}, 'A child')),
      h('button', { class: 'whocard adult', 'data-track': 'B', onclick: () => choose('B') }, icon('adult', 'big-icon'), h('span', {}, 'A grown-up'))));
  if (profiles.length) s.append(h('div', { class: 'existing' }, h('p', { class: 'muted' }, 'Or carry on:'),
    ...profiles.map(p => h('button', { class: 'btn ghost', onclick: async () => { await db.setting('active', p.id); app.boot(); } }, p.name))));
  app.mount(s);
  await play('ui:who');
}

async function helpLang(app, p) {
  const s = h('div', { class: 'onboard' });
  const done = async lang => { p.helpLang = lang; await db.put('profiles', p); app.firstSitting(p); };
  s.append(icon('globe', 'mid-icon'), h('h2', {}, 'Help in your language?'), h('p', { class: 'muted' }, 'Optional. You can learn with English only.'),
    h('div', { class: 'langs' }, ...LANGS.map(([code, native, en]) => h('button', { class: 'lang', 'data-lang': code, onclick: () => done(code) }, h('b', {}, native), h('small', {}, en)))),
    h('p', { class: 'muted small' }, 'Language help packs are not in this prototype.'),
    h('button', { class: 'btn primary skip', onclick: () => done(null) }, 'Skip'));
  app.mount(s);
  await play('ui:helpLang');
}
