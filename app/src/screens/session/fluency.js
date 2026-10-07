// Fluency / close reading: the passage with tap-any-word, and a 1-minute "pace" (words reached in 60 s).
// Pace is practice, not WCPM: no one checks accuracy here, so it is labelled pace.
import { h } from '../../ui.js';
import { mark, has, play, isFast } from '../../audio.js';
import { voice, wordPara } from './kit.js';
import { passagesFor } from './data.js';

export async function fluency(ctx, S) {
  const id = S.id;
  let paras = S.fluency.paragraphs, title = S.fluency.title;
  if (!paras) { const p = passagesFor(S, ctx.track)[0]; paras = p.paragraphs; title = p.title; }
  // keep it to about a page (<= 260 words)
  const out = []; let n = 0;
  for (const p of paras) { if (n > 0 && n + p.split(/\s+/).length > 260) break; out.push(p); n += p.split(/\s+/).length; }
  const s = ctx.stage();
  const box = h('div', { class: 'ss-passage ss-flu' }); const words = [];
  for (const p of out) { const w = wordPara(p, words.length); words.push(...w.words); box.append(w.el); }
  const status = h('p', { class: 'ss-pace', 'aria-live': 'polite' }, '');
  let phase = 'idle', t0 = 0, timer = null;
  const SECS = isFast ? 3 : 60;
  const start = h('button', { class: 'btn primary small ss-start' }, 'Start 1-minute read');
  const stopB = h('button', { class: 'btn ghost small ss-stop', hidden: true }, 'I finished');
  const finish = () => { clearInterval(timer); phase = 'pick'; start.hidden = true; stopB.hidden = true; box.classList.add('picking'); status.textContent = 'Time! Tap the last word you reached.'; };
  start.addEventListener('click', () => {
    phase = 'run'; t0 = performance.now(); start.hidden = true; stopB.hidden = false; box.classList.remove('picking'); mark('ss-pace-start', {});
    timer = setInterval(() => { const left = Math.max(0, SECS - Math.floor((performance.now() - t0) / 1000)); status.textContent = `Reading… ${left} s`; if (left <= 0) finish(); }, 200);
  });
  stopB.addEventListener('click', finish);
  words.forEach((b, i) => b.addEventListener('click', () => {
    if (phase === 'pick') {
      const secs = Math.min(SECS, (performance.now() - t0) / 1000);
      const full = secs >= SECS - 0.5;
      const pace = full ? i + 1 : Math.round((i + 1) * SECS / Math.max(secs, 1));   // finished early: scale to a minute
      words.forEach((x, k) => x.classList.toggle('reached', k <= i));
      phase = 'idle'; box.classList.remove('picking'); start.hidden = false; start.textContent = 'Try again';
      status.replaceChildren(h('b', {}, full ? `Pace: ${pace} words in 1 minute` : `Pace: about ${pace} words a minute`), ' · practice, not a score (this is not WCPM).');
      mark('ss-pace', { words: i + 1, pace }); ctx.paceDone = true; ctx.enableNext(); return;
    }
    words.forEach(x => x.classList.remove('hl')); b.classList.add('hl');
    const w = b.textContent.replace(/[^A-Za-z']/g, '').toLowerCase();
    mark('ss-word', { w }); if (has(`w:${w}`)) play(`w:${w}`);
  }));
  s.append(h('h2', {}, S.fluency.paragraphs ? 'Read it smoothly' : `Read it smoothly: ${title}`),
    h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-instr' }, S.fluency.phrased ? 'Hear it first, then read it aloud. Pause where the sentence pauses.' : 'Hear it first, then read it aloud. Tap any word you are stuck on.'), voice(`ss:${id}:flu:0`, 'Hear it read well')),
    box, h('div', { class: 'row' }, start, stopB), status);
  await ctx.next();
  clearInterval(timer);
}
