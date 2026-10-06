// Plays clips by key. Every play is recorded in window.__so.trace so tests can audit what was heard and when.
import { audioIndex } from './content.js';
const so = (window.__so = window.__so || { trace: [], missing: [] });
const fast = new URLSearchParams(location.search).has('fast');
let current = null;
// ?sliced = play isolated sounds cut from Kokoro word renders (tools/slice_phonemes.py) instead of IPA-direct renders
const sliced = new URLSearchParams(location.search).has('sliced');
let slices = {};
if (sliced) fetch('/listen-data.json').then(r => r.json()).then(d => { slices = Object.fromEntries(d.rows.map(r => [r.id, r])); }).catch(() => {});

export function mark(type, data = {}) { so.trace.push({ t: performance.now(), type, ...data }); }
export const has = key => !!audioIndex.clips[key];
export const dur = key => audioIndex.clips[key]?.dur || 0;

export function stop() { if (current) { current.pause(); current.onended = null; current = null; } }

export function play(key, { rate = 1 } = {}) {
  const c = audioIndex.clips[key];
  mark('audio', { key });
  if (!c) { so.missing.push(key); console.warn('missing clip', key); return Promise.resolve(); }
  stop();
  return new Promise(res => {
    const sl = sliced && key.startsWith('ph:') && slices[key.slice(3)];
    const a = new Audio(sl ? `/audio/sl_${key.slice(3)}.ogg` : `/audio/${c.id}.ogg`);
    current = a;
    a.playbackRate = fast ? 4 : rate;
    let done = false;
    const end = () => { if (!done) { done = true; res(); } };
    a.onended = end;
    a.onerror = () => { so.missing.push(key + ' (load error)'); console.warn('clip failed to load', key); end(); };
    a.play().catch(() => setTimeout(end, 50)); // autoplay blocked: carry on silently
    setTimeout(end, (c.dur * 1000) / a.playbackRate + 1500); // never hang on a clip
  });
}

export async function seq(keys, gap = 250) {
  for (const k of keys) { await play(k); await wait(gap); }
}
export const wait = ms => new Promise(r => setTimeout(r, fast ? Math.min(ms, 60) : ms));
export const isFast = fast;
