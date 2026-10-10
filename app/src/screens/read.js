// Read it: Track A or Track B text. Tap a word: first its sounds, one at a time; tap again for the whole word.
// Tricky words play whole (they can't be sounded out yet). No pictures beside unread words.
import { play, wait, mark, seq } from '../audio.js';
import { h, speaker, btn } from '../ui.js';
import { teacher } from '../teacher.js';
import { entry } from '../content.js';
import { splitToken, wordUnits } from '../readtext.js';

export async function read(ctx) {
  const r = ctx.lesson.read || {};
  const tr = ctx.track === 'B' && r.B && !r.B.sameAsA ? 'B' : 'A';
  const text = r[tr]?.text || '';
  const s = ctx.stage();
  const page = h('div', { class: 'page' });
  const tapped = {};
  for (const tok of text.split(/\s+/)) {
    const { lead, core, trail, bare } = splitToken(tok);
    const e = entry(bare === 'I' ? 'I' : bare.toLowerCase());
    const units = wordUnits(bare, e);
    const b = h('button', { class: 'word', 'data-w': bare }, lead, ...(e ? units.map((g, i) => h('span', { class: 'g', 'data-i': i }, g)) : [core]), trail);
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
  const readBtn = btn('I read it', 'book', { class: 'btn', say: 'ui:iReadIt' });
  const listenBtn = speaker(null, { label: 'Hear it read', onplay: () => seq(keys, 300) });
  listenBtn.hidden = true;
  readBtn.addEventListener('click', async () => { readBtn.hidden = true; listenBtn.hidden = false; await teacher.ack('read'); await ctx.instruct('ui:readHear', { stim: () => seq(keys, 300) }); mark('read-aloud', {}); ctx.enableNext(); });
  s.append(h('h2', {}, r[tr]?.title || 'Read it'), page, h('div', { class: 'row' }, readBtn, listenBtn));
  await ctx.instruct('ui:readIntro', { nudge: 'ui:idleSay', hint: () => teacher.point(readBtn.hidden ? null : readBtn) });
  await ctx.next({ disabledUntil: () => readBtn.hidden });
}
