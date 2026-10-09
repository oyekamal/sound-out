// Small DOM helpers, the speaker button, Pebble (Track A mascot placeholder) and the village strip.
import { play } from './audio.js';

export function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat()) if (kid != null && kid !== false) el.append(kid instanceof Node ? kid : document.createTextNode(kid));
  return el;
}

export const ICON = {
  speaker: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
  child: '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="22" r="11" fill="currentColor"/><path d="M14 58c2-14 9-21 18-21s16 7 18 21z" fill="currentColor"/></svg>',
  adult: '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="17" r="10" fill="currentColor"/><path d="M12 60c1-19 9-29 20-29s19 10 20 29z" fill="currentColor"/></svg>',
  lock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="2" fill="currentColor"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="2" fill="none"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="currentColor"/></svg>',
  globe: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>',
};
Object.assign(ICON, {
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  home: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 11.5 12 4l8.5 7.5" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 10.5V20h12v-9.5" fill="currentColor"/><rect x="10" y="14" width="4" height="6" fill="#fffdf8"/></svg>',
  skip: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5.5 14 12l-9 6.5z" fill="currentColor"/><path d="M18 5v14" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>',
  play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5 20 12 7 19.5z" fill="currentColor"/></svg>',
  mic: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3" fill="currentColor"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>',
  book: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 5.5c3-1 6-.8 8.5 1 2.5-1.800 5.500-2 8.500-1V19c-3-1-6-.8-8.500 1-2.500-1.800-5.500-2-8.500-1z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M12 6.500V20" stroke="currentColor" stroke-width="2.200"/></svg>',
  question: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.500 9a3.500 3.500 0 1 1 5 3.100c-1 .6-1.500 1.200-1.500 2.400" stroke="currentColor" stroke-width="2.600" fill="none" stroke-linecap="round"/><circle cx="12" cy="19" r="1.600" fill="currentColor"/></svg>',
  ear: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 9.500a4.500 4.500 0 0 1 9 0c0 2.600-2 3.400-3 4.700-.7.900-.7 1.600-.7 2.300a2.800 2.800 0 0 1-5.300 1.200" stroke="currentColor" stroke-width="2.200" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.800 9.800a1.800 1.800 0 0 1 3.600 0c0 1-.7 1.400-1.300 2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M3.300 8.500a8 8 0 0 1 2-3.200M2 12.500a11 11 0 0 1 .5-2.300" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
});
export const icon = (name, cls = 'icon') => h('span', { class: cls, html: ICON[name] });

// A button that carries an icon as well as its word. `say` = the clip a press-and-hold speaks (teacher.js).
export function btn(label, name, attrs = {}) {
  const say = attrs.say; delete attrs.say;
  return h('button', { ...attrs, 'data-say': say || null }, name ? icon(name, 'icon bi') : null, h('span', { class: 'bl' }, label));
}

// A speaker button: plays one clip (or a sequence via onplay) and pulses while playing.
export function speaker(key, { label = 'Hear it again', big = false, onplay } = {}) {
  const b = h('button', { class: 'speaker' + (big ? ' big' : ''), 'aria-label': label, 'data-key': key || '' }, icon('speaker'));
  b.addEventListener('click', async () => {
    b.classList.add('playing');
    try { await (onplay ? onplay() : play(key)); } finally { b.classList.remove('playing'); }
  });
  return b;
}

export function pebble(mood = 'wave') {
  // Placeholder mascot: a round pebble with eyes. The real app animates Pebble as a silent Lottie.
  const arm = mood === 'cheer' ? '<path d="M18 52 L6 34" /><path d="M82 52 L94 34" />' : '<path d="M82 52 L94 40" />';
  return h('div', { class: `pebble ${mood}`, 'aria-hidden': 'true', html:
    `<svg viewBox="0 0 100 90"><g stroke="#5b4a3a" stroke-width="5" stroke-linecap="round" fill="none">${arm}</g>
     <ellipse cx="50" cy="55" rx="34" ry="28" fill="#b9a993"/><ellipse cx="42" cy="44" rx="14" ry="7" fill="#cbbda9"/>
     <circle cx="39" cy="52" r="5" fill="#2b2b2b"/><circle cx="61" cy="52" r="5" fill="#2b2b2b"/>
     <circle cx="41" cy="50" r="1.6" fill="#fff"/><circle cx="63" cy="50" r="1.6" fill="#fff"/>
     <path d="M42 64 Q50 71 58 64" stroke="#2b2b2b" stroke-width="3" fill="none" stroke-linecap="round"/></svg>` });
}

// One village piece per learned sound. Simple shapes; real art comes later.
const PIECES = {
  s: ['sun', '<circle cx="20" cy="20" r="10" fill="#f4b73b"/><g stroke="#f4b73b" stroke-width="3">' + [0, 45, 90, 135, 180, 225, 270, 315].map(a => `<line x1="${20 + 13 * Math.cos(a * Math.PI / 180)}" y1="${20 + 13 * Math.sin(a * Math.PI / 180)}" x2="${20 + 18 * Math.cos(a * Math.PI / 180)}" y2="${20 + 18 * Math.sin(a * Math.PI / 180)}"/>`).join('') + '</g>'],
  a: ['apple tree', '<rect x="17" y="22" width="6" height="16" fill="#8a5a3b"/><circle cx="20" cy="17" r="13" fill="#5f9e5a"/><circle cx="14" cy="16" r="2.5" fill="#d9483b"/><circle cx="25" cy="12" r="2.5" fill="#d9483b"/><circle cx="23" cy="22" r="2.5" fill="#d9483b"/>'],
  t: ['tent', '<path d="M4 36 L20 6 L36 36 Z" fill="#e0794a"/><path d="M20 36 L20 18 L27 36 Z" fill="#7b3a22"/>'],
  p: ['pond', '<ellipse cx="20" cy="28" rx="17" ry="8" fill="#5aa6c9"/><ellipse cx="14" cy="26" rx="5" ry="2" fill="#9fd3ea"/>'],
  i: ['ink pot', '<rect x="11" y="14" width="18" height="22" rx="4" fill="#3b4f8a"/><rect x="15" y="9" width="10" height="6" fill="#3b4f8a"/>'],
  n: ['nest', '<ellipse cx="20" cy="28" rx="15" ry="8" fill="#a07444"/><circle cx="15" cy="23" r="4" fill="#e9e4d4"/><circle cx="24" cy="23" r="4" fill="#e9e4d4"/>'],
  m: ['mountain', '<path d="M2 36 L16 10 L24 22 L30 14 L39 36 Z" fill="#8c8f9e"/><path d="M16 10 L12 18 L20 18 Z" fill="#fff"/>'],
  d: ['dog house', '<path d="M6 18 L20 6 L34 18 Z" fill="#c0563f"/><rect x="9" y="18" width="22" height="18" fill="#e3b86c"/><path d="M16 36 v-9 a4 4 0 0 1 8 0 v9z" fill="#5b4a3a"/>'],
};
export function village(letters, { justAdded } = {}) {
  const strip = h('div', { class: 'village', 'aria-label': 'Your village' });
  strip.append(h('div', { class: 'ground' }));
  for (const l of letters) {
    const p = PIECES[l]; if (!p) continue;
    strip.append(h('div', { class: 'piece' + (l === justAdded ? ' new' : ''), title: `${p[0]} (${l})`, html: `<svg viewBox="0 0 40 40">${p[1]}</svg>` }));
  }
  if (!letters.length) strip.append(h('div', { class: 'piece empty', html: '<svg viewBox="0 0 40 40"><circle cx="20" cy="30" r="3" fill="#b9a993"/></svg>' }));
  return strip;
}

export const STICKERS = ['★', '♥', '☀', '☘', '♪', '✿', '☂', '⚑'];

// Picture placeholder: shown ONLY in Listen & Talk, after the chunk it illustrates.
export function picture(n, label) {
  const hues = [28, 200, 120, 280, 340, 60];
  return h('div', { class: 'picture', 'data-chunk': n, html:
    `<svg viewBox="0 0 120 80"><rect width="120" height="80" rx="10" fill="hsl(${hues[n % 6]} 45% 85%)"/><circle cx="34" cy="30" r="12" fill="hsl(${hues[n % 6]} 45% 60%)"/><path d="M10 72 L46 40 L70 60 L86 46 L112 72Z" fill="hsl(${hues[n % 6]} 35% 55%)"/></svg><span>${label}</span>` });
}

// Big letter rendering with graphemes as separate spans (for highlight and tap).
export function wordTiles(graphemes, cls = 'tile') {
  return graphemes.map((g, i) => h('span', { class: cls, 'data-i': i }, g));
}
