// "Audio coming": a clip the app needs but that is not rendered yet (listed in content/audio_needed.json, Levels 2-4).
// It plays a short silent placeholder file and shows a visible label, so a learner (and a tester) can see that the
// sound exists in the plan and is missing on purpose. 'ph:_' is a silent letter (the e in cake): no sound, no label.
import { COMING } from './levels.js';
const BASE = import.meta.env.BASE_URL;
const fast = new URLSearchParams(location.search).has('fast');
const so = (window.__so = window.__so || { trace: [], missing: [] });
so.coming = so.coming || [];
let toast = null, hideT = null;

export const isComing = key => key === 'ph:_' || COMING.has(key);

function label(key) {
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'coming'; toast.setAttribute('role', 'status');
    document.body.append(toast);
  }
  const kind = key.startsWith('ph:') ? 'sound' : key.startsWith('w:') || key.startsWith('ipa:') ? 'word' : 'voice';
  toast.textContent = `audio coming (${kind})`;
  toast.dataset.key = key;
  toast.classList.add('show');
  clearTimeout(hideT); hideT = setTimeout(() => toast.classList.remove('show'), fast ? 300 : 1600);
}

export function comingPlay(key) {
  if (key === 'ph:_') return Promise.resolve();
  so.coming.push(key);
  label(key);
  return new Promise(res => {
    if (fast) return setTimeout(res, 20);
    const a = new Audio(`${BASE}coming.ogg`);
    let done = false; const end = () => { if (!done) { done = true; res(); } };
    a.onended = end; a.onerror = end;
    a.play().catch(end);
    setTimeout(end, 900);
  });
}
