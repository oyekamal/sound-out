// Read it: Track A or Track B text. Tap a word: first its sounds, one at a time; tap again for the whole word.
// Tricky words play whole (they can't be sounded out yet). No pictures beside unread words.
import { play, wait, mark, seq } from '../audio.js';
import { h, speaker } from '../ui.js';
import { entry } from '../content.js';

export async function read(ctx) {
  const r = ctx.lesson.read || {};
  const tr = ctx.track === 'B' && r.B && !r.B.sameAsA ? 'B' : 'A';
  const text = r[tr]?.text || '';
  const s = ctx.stage();
  const page = h('div', { class: 'page' });
  const tapped = {};
  for (const tok of text.split(/\s+/)) {
    const bare = tok.replace(/[^A-Za-z']/g, '');
    const e = entry(bare === 'I' ? 'I' : bare.toLowerCase());
    const b = h('button', { class: 'word', 'data-w': bare }, ...(e ? e.g.map((g, i) => h('span', { class: 'g', 'data-i': i }, i === 0 && /^[A-Z]/.test(bare) ? g.toUpperCase() : g)) : [bare]), tok.replace(/[A-Za-z']/g, ''));
    b.addEventListener('click', async () => {
      if (!e) return;
      tapped[bare] = (tapped[bare] || 0) + 1;
      if (e.kind === 'heart' || tapped[bare] > 1) { mark('read-word', { word: bare, whole: true }); return play(`w:${e.w === 'I' ? 'I' : e.w}`); }
      mark('read-word', { word: bare, whole: false });
      const sp = [...b.querySelectorAll('.g')];
      for (let i = 0; i < sp.length; i++) { sp[i].classList.add('hl'); await play(`ph:${e.p[i]}`); await wait(200); sp[i].classList.remove('hl'); }
    });
    page.append(b, ' ');
  }
  const keys = [...Array(20).keys()].map(i => `read:${ctx.lesson.id}:${tr}:${i}`).filter(k => ctx.hasClip(k));
  const readBtn = h('button', { class: 'btn' }, 'I read it');
  const listenBtn = speaker(null, { label: 'Hear it read', onplay: () => seq(keys, 300) });
  listenBtn.hidden = true;
  readBtn.addEventListener('click', async () => { readBtn.hidden = true; listenBtn.hidden = false; await ctx.instruct('ui:readHear'); mark('read-aloud', {}); await seq(keys, 300); ctx.enableNext(); });
  s.append(h('h2', {}, r[tr]?.title || 'Read it'), page, h('div', { class: 'row' }, readBtn, listenBtn));
  await ctx.instruct('ui:readIntro');
  await ctx.next({ disabledUntil: () => readBtn.hidden });
}
