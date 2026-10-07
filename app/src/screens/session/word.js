// Word work: build words from prefix / root / suffix tiles, then the meaning (simple English) and an example from the lesson.
// Tier-2 / academic words: friendly definition + examples. Level 5 review: affix chips.
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, say, reveal, selfMark, shuffle } from './kit.js';
import { passagesFor } from './data.js';

const COMMON = ['un', 're', 'dis', 'pre', 'mis', 'ing', 'ed', 'ly', 'ness', 'ful', 'less', 'able', 'tion', 'er'];

function exampleFrom(S, word) {
  const text = (S.text?.passages || []).flatMap(p => p.paragraphs).join(' ');
  const s = text.split(/(?<=[.!?])\s+/).find(x => new RegExp(`\\b${word}\\b`, 'i').test(x));
  return s && s.length < 200 ? s : null;
}

function pickItems(items, n = 5) {
  const built = items.filter(x => (x.parts || []).length > 1);
  const by = {}; for (const x of built) (by[x.affix || ''] ||= []).push(x);
  const out = []; const keys = Object.keys(by);
  for (let r = 0; out.length < n && r < 6; r++) for (const k of keys) if (by[k][r] && out.length < n) out.push(by[k][r]);
  return out;
}

export async function word(ctx, S) {
  const W = S.word; const id = S.id;
  const items = pickItems(W.items || []);
  const allParts = [...new Set((W.items || []).flatMap(x => x.parts || []))];
  for (const it of items) {
    const i = W.items.indexOf(it);
    const s = ctx.stage();
    const distract = shuffle([...allParts, ...COMMON].filter(p => !it.parts.includes(p)), i + 1)[0];
    const tiles = shuffle([...it.parts, distract], i + 2);
    const slots = h('div', { class: 'ss-slots' }, ...it.parts.map((_, k) => h('span', { class: 'ss-slot', 'data-k': k })));
    let n = 0; let done; const built = new Promise(r => { done = r; });
    const tray = h('div', { class: 'ss-tray' }, ...tiles.map(p => {
      const b = h('button', { class: 'ss-tile', 'data-part': p }, p);
      b.addEventListener('click', () => {
        if (p === it.parts[n]) { slots.children[n].textContent = p; slots.children[n].dataset.part = p; b.disabled = true; n++; mark('ss-build', { word: it.word, part: p, ok: true }); if (n === it.parts.length) done(); }
        else { b.classList.add('wrong'); setTimeout(() => b.classList.remove('wrong'), 500); mark('ss-build', { word: it.word, part: p, ok: false }); }
      });
      return b;
    }));
    const aff = (W.affixes || []).find(a => a.affix === it.affix);
    const head = it.root ? `Root ${it.affix} = "${it.rootMeaning}"` : it.affix ? `${it.affix}${aff?.meaning ? ` = "${aff.meaning.replace(/^"|"$/g, '')}"` : ''}` : 'Word parts';
    s.append(h('h2', {}, 'Build the word'), h('p', { class: 'ss-label' }, head), h('p', { class: 'ss-instr' }, 'Build the word that means ', h('b', {}, it.meaning), '. Tap the parts in order.'),
      slots, tray, h('p', { class: 'muted small' }, 'One tile does not belong.'));
    say(`ss:${id}:word:${i}:m`);
    await built;
    const ex = exampleFrom(S, it.word);
    s.append(h('div', { class: 'ss-card ss-built', 'data-word': it.word }, h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-big' }, it.word), voice(`ss:${id}:word:${i}`, 'Hear the word')),
      h('p', {}, h('b', {}, 'Means: '), it.meaning),
      ex ? h('p', { class: 'ss-ex' }, h('b', {}, 'In the lesson: '), ex) : h('p', { class: 'muted small' }, `Peel it: ${it.parts.join(' + ')}.`)));
    await ctx.next();
  }
  for (const [i, v] of (W.vocab || []).entries()) {
    const s = ctx.stage();
    s.append(h('h2', {}, 'A useful word'), h('div', { class: 'ss-card ss-vocab' }, h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-big' }, v.word), voice(`ss:${id}:vocab:${i}`, 'Hear the word and its meaning')),
      h('p', {}, h('b', {}, 'Means: '), v.def), ...(v.examples || []).map(e => h('p', { class: 'ss-ex' }, e))));
    if (v.task) s.append(h('div', { class: 'ss-card' }, h('p', { class: 'ss-q' }, h('b', {}, 'Your turn: '), v.task), reveal(null, { label: 'I said mine', fallback: 'Practice: a good answer uses the word in a sentence of your own that fits its meaning.' })));
    await ctx.next();
  }
  for (const [g, grp] of (W.review || []).entries()) {
    const s = ctx.stage();
    s.append(h('h2', {}, `Review: ${grp.label}`), h('p', { class: 'ss-instr' }, 'For each one, say an example word and what it means. Tap it when you have.'),
      h('div', { class: 'ss-chips' }, ...grp.items.map(x => { const b = h('button', { class: 'ss-chip' }, x); b.addEventListener('click', () => { b.classList.toggle('done'); mark('ss-review', { g, x }); }); return b; })),
      selfMark(m => mark('ss-self', { block: 'review', g, m })));
    await ctx.next();
  }
}
