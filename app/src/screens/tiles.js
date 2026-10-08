// Levels 2-4 word display on top of the printed-word spans (one span per grapheme, class "g"):
//   split vowel (a_e)  -> the vowel and its silent e share a colour and an underline arc around the consonant
//   suffix (-s -es -ed -ing -er ...) -> the ending is its own coloured tile after a small "+"
//   syllables (rab·bit, can·dle) -> a dot between chunks; a doubled consonant splits in the middle (rab·bit)
// Long words shrink so a 12-letter word fits a 390px phone without horizontal scroll.
import { h } from '../ui.js';

export function decorate(box, e, { syllables = true } = {}) {
  if (!e || !e.g) return box;
  const spans = [...box.querySelectorAll(':scope > .g')];
  if (spans.length !== e.g.length) return box;
  for (const [a, b] of e.split || []) {
    spans[a].classList.add('split'); spans[b].classList.add('split');
    for (let i = a; i <= b; i++) spans[i].classList.add('arc');
  }
  if (e.suffix != null && spans[e.suffix]) {
    spans.slice(e.suffix).forEach(s => s.classList.add('suffix'));
    spans[e.suffix].before(h('span', { class: 'plus', 'aria-hidden': 'true' }, '+'));
  } else if (syllables && e.syl) {
    for (const s of e.syl) {
      if (s % 1) { const sp = spans[Math.floor(s)]; const t = sp.textContent; sp.replaceChildren(t[0], h('i', { class: 'sylmid', 'aria-hidden': 'true' }, '·'), t.slice(1)); }
      else spans[s]?.before(h('span', { class: 'syldot', 'aria-hidden': 'true' }, '·'));
    }
  }
  if (e.prefix) spans.slice(0, e.prefix).forEach(s => s.classList.add('prefix'));
  const n = e.g.join('').length + (e.syl?.length || 0);
  if (n > 6) { box.classList.add('long'); box.style.setProperty('--fs', `${Math.max(1.5, Math.min(4.2, 26 / n)).toFixed(2)}rem`); }
  return box;
}

// A plain word box (no syllable dots) for the word-attack routine, which reveals the parts step by step.
export function plainWord(e) {
  const box = h('div', { class: 'printed tiles', 'data-word': e.w });
  e.g.forEach((g, i) => box.append(h('span', { class: 'g', 'data-i': i }, g)));
  decorate(box, { ...e, suffix: null, syl: null, prefix: null });
  return box;
}
