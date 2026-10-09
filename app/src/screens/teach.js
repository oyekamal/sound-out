// Levels 2-4 "Meet it" for a new spelling: a grapheme card (sh, tch, igh as ONE tile; a_e as a vowel and a silent e
// around a gap), its sound, and the first course word that uses it. Blends show their letters as separate tiles
// (each keeps its own sound); endings show base + ending; patterns (-ild -ind) show the chunk.
import { play, wait, mark } from '../audio.js';
import { h, speaker } from '../ui.js';
import { entry } from '../content.js';
import { printedWord } from '../gate.js';
import { teacher } from '../teacher.js';

function card(u, onTap) {
  const b = h('button', { class: 'lettercard unitcard', 'aria-label': `${u.g}, tap to hear it` });
  if (u.kind === 'split') { const [v, e] = u.g.split('_'); b.append(v, h('span', { class: 'gap' }, '_'), e); }
  else if (u.kind === 'suffix') b.append(h('span', { class: 'sfx' }, u.g.startsWith('-') ? u.g : '-' + u.g));
  else b.append(u.g);
  b.addEventListener('click', async () => { b.classList.add('pop'); await onTap(); b.classList.remove('pop'); });
  return b;
}

async function example(s, w, g) {
  const e = entry(w); if (!e) return;
  const box = printedWord(w, null, null);
  [...box.querySelectorAll('.g')].forEach((sp, i) => { if (e.g[i] === g || (g && g.includes('_') && e.split?.some(p => p.includes(i)))) sp.classList.add('hl'); });
  s.append(h('div', { class: 'row' }, box, speaker(`w:${w}`, { label: `Hear ${w}` })));
  await play('ui:teachExample'); await play(`w:${w}`);
}

async function one(ctx, u) {
  const s = ctx.stage();
  let tapped = 0;
  const say = () => u.pid ? play(`ph:${u.pid}`) : Promise.resolve();
  s.append(...[h('h2', {}, u.kind === 'suffix' ? 'A new ending' : 'A new spelling'),
    card(u, async () => { tapped++; mark('teach-tap', { unit: u.g }); await say(); ctx.enableNext(); }),
    u.label ? h('p', { class: 'unitlabel' }, u.label) : null,
    u.pid ? h('div', { class: 'row small' }, speaker(`ph:${u.pid}`, { label: 'Hear its sound' }), h('span', { class: 'muted' }, 'one sound')) : null].filter(Boolean));
  await ctx.instruct(u.kind === 'suffix' ? 'ui:teachSuffix' : 'ui:teachIntro', { stim: async () => { await say(); await wait(300); }, nudge: 'ui:idleTap', hint: () => teacher.point(s.querySelector('.unitcard')) });
  if (u.example) await example(s, u.example, u.g.replace(/^-/, ''));
  await ctx.next({ disabledUntil: () => tapped > 0 });
}

async function grid(ctx, us, title, instr) {
  const s = ctx.stage();
  const seen = new Set();
  const g = h('div', { class: 'unitgrid' });
  for (const u of us) {
    g.append(card(u, async () => {
      seen.add(u.g); ctx.enableNext(); mark('teach-tap', { unit: u.g });
      for (const l of u.letters || []) { const e = entry(l); if (e) await play(`ph:${e.p[0]}`); await wait(120); }
      if (u.example) await play(`w:${u.example}`);
    }));
  }
  s.append(h('h2', {}, title), g, h('p', { class: 'prompt' }, instr));
  await ctx.instruct('ui:teachBlend', { nudge: 'ui:idleTap', hint: () => teacher.point(g.querySelector('.unitcard')) });
  await ctx.next({ disabledUntil: () => seen.size > 0 });
}

export async function teach(ctx) {
  const units = ctx.lesson.units || [];
  const blends = units.filter(u => u.kind === 'blend'), patterns = units.filter(u => u.kind === 'pattern' || (u.kind === 'suffix' && !u.pid));
  for (const u of units) if (u.kind === 'grapheme' || u.kind === 'split' || (u.kind === 'suffix' && u.pid)) await one(ctx, u);
  if (blends.length) await grid(ctx, blends, 'Blends: both sounds, quickly', 'Each letter keeps its own sound. Tap one to hear it.');
  if (patterns.length) await grid(ctx, patterns, 'Word endings and chunks', 'Read the chunk as one piece. Tap one to hear a word with it.');
}
