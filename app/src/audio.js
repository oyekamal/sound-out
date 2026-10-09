// Plays clips by key. Every play is recorded in window.__so.trace so tests can audit what was heard and when.
import { audioIndex } from './content.js';
import { isComing, comingPlay } from './placeholder.js';
const so = (window.__so = window.__so || { trace: [], missing: [] });
const fast = new URLSearchParams(location.search).has('fast');
let current = null;
// Isolated sounds (ph:*) are direct ElevenLabs renders in the app voice, picked by tools/iso_sounds.py (no slicing).
// Paths go through BASE_URL so the GitHub Pages build (/sound-out/) finds them.
const BASE = import.meta.env.BASE_URL;

export function mark(type, data = {}) { so.trace.push({ t: performance.now(), type, ...data }); }
export const has = key => !!audioIndex.clips[key] || isComing(key);
export const dur = key => audioIndex.clips[key]?.dur || 0;

// A play() promise resolves true when the clip finished and FALSE when it was interrupted (a tap, a replay, another
// clip). Loops that narrate in order stop as soon as one clip comes back false (see teacher.js for the rules).
let settleCurrent = null, blockedHandler = null, unlocking = null;
export const bus = new EventTarget();
export const playing = () => !!current;
export const setBlockedHandler = fn => { blockedHandler = fn; };

function halt() {
  if (current) { try { current.pause(); } catch { /* already gone */ } current.onended = null; current = null; }
  if (settleCurrent) { const s = settleCurrent; settleCurrent = null; s(false); }
}
export function stop() { halt(); }

export function play(key, { rate = 1 } = {}) {
  const c = audioIndex.clips[key];
  mark('audio', { key });
  if (!c && isComing(key)) return comingPlay(key).then(() => true);   // Levels 2-4: listed in content/audio_needed.json, not rendered yet
  if (!c) { so.missing.push(key); console.warn('missing clip', key); return Promise.resolve(true); }
  halt();
  return new Promise(res => {
    const a = new Audio(`${BASE}audio/${c.id}.ogg`);
    current = a;
    a.playbackRate = fast ? 4 : rate;
    let done = false, t = null;
    const settle = ok => {
      if (done) return; done = true; clearTimeout(t);
      if (settleCurrent === settle) settleCurrent = null;
      if (current === a) current = null;
      bus.dispatchEvent(new CustomEvent('end', { detail: { key, ok } }));
      res(ok);
    };
    settleCurrent = settle;
    a.onended = () => settle(true);
    a.onerror = () => { so.missing.push(key + ' (load error: ' + (a.error && a.error.message || a.error?.code) + ')'); console.warn('clip failed to load', key); settle(true); };
    bus.dispatchEvent(new CustomEvent('start', { detail: { key } }));
    const go = () => a.play().catch(async err => {
      // autoplay blocked (a web first load): ask for ONE big tap, then play this clip for real
      if (err && err.name === 'NotAllowedError' && blockedHandler && !done) {
        clearTimeout(t);                       // the hang timer waits while the start button is on screen
        unlocking = unlocking || blockedHandler().finally(() => { unlocking = null; });
        await unlocking;
        if (!done && current === a) { arm(); return go(); }
      }
      setTimeout(() => settle(true), 50);
    });
    const arm = () => { clearTimeout(t); t = setTimeout(() => settle(true), (c.dur * 1000) / a.playbackRate + 1500); }; // never hang on a clip
    arm();
    go();
  });
}

export async function seq(keys, gap = 250) {
  for (const k of keys) { if ((await play(k)) === false) return false; await wait(gap); }
  return true;
}
export const wait = ms => new Promise(r => setTimeout(r, fast ? Math.min(ms, 60) : ms));
export const isFast = fast;
