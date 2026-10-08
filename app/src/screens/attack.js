// L4.12-L4.15 multisyllabic word attack (DESIGN.md §3, L4.14): 1 mark the vowels -> 2 peel prefixes/suffixes ->
// 3 chunk into syllables -> 4 blend the chunks -> 5 flex (try the other vowel sound if it is not a real word).
// Then the tap gate on the same word when it has options, else a read-aloud self-check (logged as self-report).
import { play, wait, mark } from '../audio.js';
import { h } from '../ui.js';
import { entry, options } from '../content.js';
import { gate } from '../gate.js';
import { plainWord, decorate } from './tiles.js';
import { selfCheck } from './levelcheck.js';

const STEPS = ['Vowels', 'Peel', 'Chunk', 'Blend', 'Flex'];
const bar = n => h('div', { class: 'steps' }, ...STEPS.map((x, i) => h('span', { class: i === n ? 'on' : '' }, `${i + 1} ${x}`)));

export async function attackWord(ctx, w, { judge = true } = {}) {
  const e = entry(w);
  if (!e) return { judged: false };
  mark('attack-start', { word: w });
  // 1 vowels
  let s = ctx.stage(); let box = plainWord(e);
  const spans = [...box.querySelectorAll(':scope > .g')];
  const vow = new Set(e.vow || []);
  const msg = h('p', { class: 'prompt' }, 'Tap every vowel sound.');
  s.append(h('h2', {}, 'Break it apart'), bar(0), box, msg);
  await ctx.instruct('ui:attackVowels');
  await new Promise(res => {
    const found = new Set();
    spans.forEach((sp, i) => {
      if (vow.has(i)) sp.classList.add('want');
      sp.addEventListener('click', async () => {
        if (vow.has(i)) { if (found.has(i)) return; found.add(i); sp.classList.remove('want'); sp.classList.add('vowel'); mark('attack-vowel', { word: w, i }); if (found.size === vow.size) res(); await play(`ph:${e.p[i]}`); }
        else { sp.classList.add('nope'); setTimeout(() => sp.classList.remove('nope'), 400); }
      });
    });
    if (!vow.size) res();
  });
  msg.textContent = `${vow.size} vowel sound${vow.size === 1 ? '' : 's'}: ${vow.size} chunk${vow.size === 1 ? '' : 's'}.`;
  await ctx.next();
  // 2 peel
  s = ctx.stage(); box = plainWord(e);
  const sp2 = [...box.querySelectorAll(':scope > .g')];
  const affix = [...(e.prefix ? [...Array(e.prefix).keys()] : []), ...(e.suffix != null ? [...Array(e.g.length - e.suffix).keys()].map(k => k + e.suffix) : [])];
  s.append(h('h2', {}, 'Peel off the parts you know'), bar(1), box);
  if (affix.length) {
    s.append(h('p', { class: 'prompt' }, 'Tap the start or ending you know.'));
    await ctx.instruct('ui:attackPeel');
    await new Promise(res => {
      const groups = [e.prefix ? [...Array(e.prefix).keys()] : null, e.suffix != null ? affix.filter(i => i >= e.suffix) : null].filter(Boolean);
      let left = groups.length;
      for (const gidx of groups) {
        gidx.forEach(i => sp2[i].classList.add('want'));
        const peel = () => { if (sp2[gidx[0]].classList.contains('peeled')) return; gidx.forEach(i => { sp2[i].classList.remove('want'); sp2[i].classList.add('peeled'); }); mark('attack-peel', { word: w, at: gidx[0] }); if (--left === 0) res(); };
        gidx.forEach(i => sp2[i].addEventListener('click', peel));
      }
    });
  } else s.append(h('p', { class: 'prompt' }, 'No start or ending to peel off here.'));
  await ctx.next();
  // 3 chunk + 4 blend
  s = ctx.stage(); box = plainWord(e); decorate(box, { ...e, suffix: null, prefix: null });
  const ch = e.chunks || [{ text: e.w, ipa: null }];
  const row = h('div', { class: 'chunks' });
  const said = h('button', { class: 'btn primary saidit', hidden: true }, 'I said it');
  s.append(h('h2', {}, 'Chunk and blend'), bar(3), box, row, said, h('p', { class: 'selfreport' }, 'self-report: the app does not hear you'));
  await ctx.instruct('ui:attackChunk');
  await ctx.instruct('ui:attackBlend');
  await new Promise(res => {
    let n = 0;
    ch.forEach((c, i) => {
      const b = h('button', { class: 'chunk want', 'data-i': i }, c.text);
      b.addEventListener('click', async () => {
        if (b.classList.contains('done')) return;
        b.classList.remove('want'); b.classList.add('done'); mark('attack-chunk', { word: w, i });
        if (++n === ch.length) { said.hidden = false; }
        if (c.ipa) await play(`syl:${c.ipa}`);
      });
      row.append(b);
    });
    said.addEventListener('click', res, { once: true });
  });
  // 5 flex
  s = ctx.stage(); box = plainWord(e); decorate(box, e);
  let pick; const picked = new Promise(r => { pick = r; });
  s.append(h('h2', {}, 'Is it a real word?'), bar(4), box,
    h('p', { class: 'prompt' }, 'If it is not a word you know, try a vowel the other way: long instead of short, or "uh".'),
    h('div', { class: 'selfrow' },
      h('button', { class: 'btn flexbtn', onclick: () => pick('real') }, 'Yes, a real word'),
      h('button', { class: 'btn ghost flexbtn', onclick: () => pick('flex') }, 'I flexed a vowel')));
  await ctx.instruct('ui:attackFlex');
  mark('attack-flex', { word: w, choice: await picked });
  await wait(200);
  if (!judge) return { judged: false };
  const kind = e.kind === 'pseudo' ? 'pseudo' : 'real';
  const r = options[w.toLowerCase()] ? await gate(ctx, w, kind) : await selfCheck(ctx, w, kind);
  await ctx.record(w, kind, r);
  return r;
}

export async function attack(ctx) {
  for (const w of ctx.lesson.attack || []) await attackWord(ctx, w);
}
