// E7 Spell it: a dictated sound or word; build it from a tile tray. Single-sound sittings spell the letter only.
import { play, mark } from '../audio.js';
import { h, speaker } from '../ui.js';
import { entry, g2p } from '../content.js';

const shuffle = a => [...a].sort(() => Math.random() - 0.5);
const EXTRA = ['m', 'd', 'o', 'e', 'u', 'b', 'f', 'l', 'g', 'r'];

export async function spellLetter(ctx, letter, known) {
  const s = ctx.stage();
  const pid = g2p[letter];
  const pool = shuffle([letter, ...shuffle([...known, ...EXTRA].filter(x => x !== letter)).slice(0, 2)]);
  s.append(h('h2', {}, 'Which letter makes this sound?'), speaker(`ph:${pid}`, { big: true, label: 'Hear the sound' }));
  const tray = h('div', { class: 'tray' });
  let first = null, resolve; const done = new Promise(r => { resolve = r; });
  for (const l of pool) {
    const b = h('button', { class: 'tilebtn', 'data-letter': l }, l);
    b.addEventListener('click', async () => {
      const ok = l === letter;
      if (first === null) first = ok;
      mark('spell-letter', { letter, pick: l, correct: ok });
      b.classList.add(ok ? 'right' : 'wrong');
      if (ok) { await play('ui:good'); resolve(); } else { await play('ui:tryAgain'); await play(`ph:${pid}`); }
    });
    tray.append(b);
  }
  s.append(tray);
  await ctx.instruct('ui:spellLetter');
  await play(`ph:${pid}`);
  await done;
  const r = { judged: true, correct: first };
  await ctx.record(`letter:${letter}`, 'letter', r);
  return r;
}

export async function spellWord(ctx, w, known, { judgedOnly = false } = {}) {
  const e = entry(w);
  const s = ctx.stage();
  const boxes = h('div', { class: 'boxes' });
  const slots = e.g.map((_, i) => h('button', { class: 'slot', 'data-i': i, 'aria-label': `box ${i + 1}` }));
  boxes.append(...slots);
  const extras = shuffle([...known].filter(g => !e.g.includes(g))).slice(0, 2);
  const tiles = shuffle([...e.g, ...extras]).map((g, i) => h('button', { class: 'tilebtn', 'data-g': g, 'data-k': i }, g));
  const tray = h('div', { class: 'tray' }, ...tiles);
  s.append(h('h2', {}, 'Spell it'), speaker(`w:${w}`, { big: true, label: 'Hear the word' }), boxes, tray);
  const fill = t => { const slot = slots.find(x => !x.dataset.g); if (!slot) return; slot.dataset.g = t.dataset.g; slot.dataset.k = t.dataset.k; slot.textContent = t.dataset.g; t.disabled = true; check(); };
  tiles.forEach(t => t.addEventListener('click', () => fill(t)));
  slots.forEach(sl => sl.addEventListener('click', () => { if (!sl.dataset.g) return; tiles[ +sl.dataset.k ] && (tiles.find(t => t.dataset.k === sl.dataset.k).disabled = false); delete sl.dataset.g; delete sl.dataset.k; sl.textContent = ''; sl.classList.remove('wrong'); }));
  let tries = 0, first = null, resolve; const done = new Promise(r => { resolve = r; });
  async function check() {
    if (slots.some(x => !x.dataset.g)) return;
    const ok = slots.every((x, i) => x.dataset.g === e.g[i]);
    tries++; if (first === null) first = ok;
    mark('spell-word', { word: w, correct: ok, tries });
    if (ok) { slots.forEach(x => x.classList.add('right')); await play('ui:good'); return resolve(); }
    slots.forEach((x, i) => { if (x.dataset.g !== e.g[i]) x.classList.add('wrong'); });
    if (tries >= 2) { slots.forEach((x, i) => { x.textContent = e.g[i]; x.dataset.g = e.g[i]; x.classList.remove('wrong'); x.classList.add('shown'); }); await play('ui:gateReview'); return resolve(); }
    await play('ui:tryAgain'); await play(`w:${w}`);
  }
  await ctx.instruct('ui:spellIntro');
  await play(`w:${w}`);
  await done;
  const r = { judged: true, correct: first };
  await ctx.record(`spell:${w}`, 'spell', r);
  return r;
}
