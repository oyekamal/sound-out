// The grown-up gate (Families policy): a sum a young child cannot do, shown in digits and never spoken.
// askGrownup() -> Promise<boolean>. 3 wrong tries -> a 30 s calm lockout; tries and lock time persist in localStorage.
import { h } from './ui.js';
import { stop } from './audio.js';

const TRIES = 'so-gate-tries', LOCK = 'so-gate-lock', LOCK_MS = 30000;
const ls = {
  get: k => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* no storage: lockout lasts this session only */ } },
};
let open = false;
const sum = () => { const a = 13 + Math.floor(Math.random() * 7), b = 4 + Math.floor(Math.random() * 6); return { a, b, ans: a * b }; };

export function askGrownup() {
  if (open) return Promise.resolve(false);
  open = true; stop();
  return new Promise(res => {
    const prev = document.activeElement;
    let q = sum();
    const input = h('input', { class: 'gu-in', type: 'text', inputmode: 'numeric', pattern: '[0-9]*', autocomplete: 'off', autocorrect: 'off', autocapitalize: 'off', spellcheck: 'false', 'aria-label': 'Answer' });
    const msg = h('p', { class: 'gu-msg', 'aria-live': 'polite' });
    const qEl = h('p', { class: 'gu-q' }, `What is ${q.a} × ${q.b}?`);
    const ok = h('button', { class: 'btn primary', type: 'button' }, 'Open');
    const close = h('button', { class: 'btn ghost', type: 'button' }, 'Close');
    const sheet = h('div', { class: 'gu-sheet', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'For grown-ups' },
      h('h2', {}, 'For grown-ups'), h('p', { class: 'muted' }, 'Answer this sum to go on.'), qEl, input, msg, h('div', { class: 'row' }, close, ok));
    const wrap = h('div', { class: 'gu-wrap' }, sheet);
    const done = v => { clearInterval(tm); wrap.remove(); document.removeEventListener('keydown', key, true); open = false; try { prev?.focus?.(); } catch { /* gone */ } res(v); };
    const locked = () => Math.max(0, Number(ls.get(LOCK) || 0) - Date.now());
    const tick = () => { const l = locked(); ok.disabled = input.disabled = l > 0; if (l > 0) msg.textContent = `Please wait ${Math.ceil(l / 1000)} seconds.`; else if (msg.dataset.lock) { msg.textContent = ''; delete msg.dataset.lock; } if (l > 0) msg.dataset.lock = '1'; };
    const tm = setInterval(tick, 500); tick();
    const submit = () => {
      if (locked() > 0) return;
      if (Number(input.value.trim()) === q.ans) { ls.set(TRIES, '0'); return done(true); }
      const n = Number(ls.get(TRIES) || 0) + 1; input.value = '';
      if (n >= 3) { ls.set(TRIES, '0'); ls.set(LOCK, String(Date.now() + LOCK_MS)); tick(); }
      else { ls.set(TRIES, String(n)); msg.textContent = 'Not quite. Try this one.'; }
      q = sum(); qEl.textContent = `What is ${q.a} × ${q.b}?`;
    };
    const key = e => {
      if (e.key === 'Escape') return done(false);
      if (e.key === 'Enter' && document.activeElement === input) return submit();
      if (e.key === 'Tab') { const f = [input, close, ok].filter(x => !x.disabled); const i = f.indexOf(document.activeElement); const n = f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length]; if (n) { e.preventDefault(); n.focus(); } }
    };
    document.addEventListener('keydown', key, true);
    ok.addEventListener('click', submit); close.addEventListener('click', () => done(false));
    document.body.append(wrap); input.focus();
  });
}
