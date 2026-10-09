// Shared bits for the session screens: audio-or-placeholder, reveal, tappable sentences/words.
import { play, has, mark } from '../../audio.js';
import { h, icon } from '../../ui.js';

// A speaker that plays the clip when it exists; until then it shows a visible "audio coming" placeholder.
// (ElevenLabs quota exhausted: L5-7 clips are not rendered; characters are counted in content/audio_needed_l5_7.json.)
export function voice(key, label = 'Hear it') {
  if (has(key)) {
    const b = h('button', { class: 'speaker ss-voice', 'aria-label': label, 'data-key': key }, icon('speaker'));
    b.addEventListener('click', async () => { b.classList.add('playing'); try { await play(key); } finally { b.classList.remove('playing'); } });
    return b;
  }
  const b = h('button', { class: 'ss-coming', 'data-key': key, 'aria-label': `${label}: audio coming` }, icon('speaker'), h('span', {}, 'audio coming'));
  b.addEventListener('click', () => { mark('audio-coming', { key }); b.classList.add('pinged'); setTimeout(() => b.classList.remove('pinged'), 600); });
  return b;
}
// Plays the clip if it exists; never asks for a missing one (that would be logged as missing audio).
export const say = key => (has(key) ? play(key) : Promise.resolve());

export function practiceTag(text = 'Practice') { return h('span', { class: 'ss-tag' }, text); }

// "Think, then tap to see a good answer" self-check. Resolves when the answer is shown.
export function reveal(answer, { label = 'Show a good answer', fallback } = {}) {
  const box = h('div', { class: 'ss-reveal' });
  const btn = h('button', { class: 'btn ghost small ss-show', 'data-say': 'ui:showAnswer' }, label);
  const ans = h('div', { class: 'ss-answer', hidden: true }, answer ? h('p', {}, answer) : h('p', { class: 'muted' }, fallback || 'Look back at the text: a good answer points to a sentence in it.'));
  box.append(btn, ans);
  box.done = new Promise(res => btn.addEventListener('click', () => { btn.hidden = true; ans.hidden = false; mark('ss-reveal', {}); res(); }));
  return box;
}

// Self-mark after a reveal: practice only, recorded but never a gate.
export function selfMark(onPick) {
  const row = h('div', { class: 'row ss-self' });
  for (const [k, t, say] of [['yes', 'I had it', 'ui:markHad'], ['close', 'Nearly', 'ui:markNearly'], ['no', 'Not yet', 'ui:markNot']]) {
    const b = h('button', { class: 'btn small ss-mark', 'data-mark': k, 'data-say': say }, t);
    b.addEventListener('click', () => { row.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); onPick(k); });
    row.append(b);
  }
  return row;
}

// A paragraph as tappable sentences (tap = highlight + its audio when it exists).
export function sentencePara(text, key) {
  const p = h('p', { class: 'ss-para' });
  const parts = text.split(/(?<=[.!?…]["”’)]?)\s+(?=["“‘(]?[A-Z0-9])/);
  parts.forEach((s, i) => {
    const sp = h('span', { class: 'ss-sent', 'data-i': i, tabindex: 0, role: 'button' }, s);
    sp.addEventListener('click', () => {
      p.closest('.screen')?.querySelectorAll('.ss-sent.hl').forEach(x => x.classList.remove('hl'));
      sp.classList.add('hl'); mark('ss-sentence', { key, i }); say(`${key}:s${i}`);
    });
    p.append(sp, ' ');
  });
  return p;
}

// A passage as tappable words (fluency): returns { el, words }.
export function wordPara(text, start = 0) {
  const p = h('p', { class: 'ss-para ss-words' }); const ws = [];
  for (const tok of text.split(/\s+/).filter(Boolean)) {
    const b = h('button', { class: 'ss-w', 'data-n': start + ws.length }, tok);
    ws.push(b); p.append(b, ' ');
  }
  return { el: p, words: ws };
}

export const shuffle = (a, seed = 7) => { const r = [...a]; let s = seed; for (let i = r.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor(s / 233280 * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
