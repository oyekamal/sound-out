// Tilo: the teacher's face on Track A (the child track). Track B gets no mascot.
// One persistent element, driven by teacher.js (mood / emote / pin / screen) and by the audio bus (speaking = lip-flap).
//   body + mouth sit in ONE .tilo-stage wrapper (the wrapper breathes, the mouth is placed in percent of the stage),
//   so they scale and move together and can never drift apart. Sizes and offsets come from tilo.json, never hardcoded.
//   Poses: idle (waiting), listening (waiting for a tap), speaking (+ mouths), celebrating (right), encouraging (wrong).
//   prefers-reduced-motion: no breathing, no pop, no flap (a still, open mouth while the voice talks).
import TILO from '../public/img/tilo/tilo.json';
import { bus } from './audio.js';

const BASE = import.meta.env.BASE_URL;
const SZ = (window.devicePixelRatio || 1) >= 1.5 ? '2x' : '1x';
const BODY_W = 225, BODY_H = 256;                       // the 1x art size of every pose (2x files are exactly double)
const POSES = ['idle', 'listening', 'encouraging', 'celebrating', 'speaking'];
const FLAP = ['mid', 'aaa', 'mid', 'mmm', 'aaa', 'mid'];   // no 'ooo': a round 'o' with a raised arm read as shock in the critic round
const reduced = () => !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

const st = { homeHost: null, track: null, mood: 'idle', emote: null, emoteKey: null, pinned: null, speaking: false, mouth: 'mid', offT: 0, emoteT: 0, flapT: 0, host: null };
let el = null, stage = null, bubble = null; const bodies = {}, mouths = {};

function img(src, cls) { const i = new Image(); i.className = cls; i.alt = ''; i.decoding = 'async'; i.src = BASE + src; return i; }

function build() {
  el = document.createElement('div'); el.className = 'tilo corner'; el.setAttribute('aria-hidden', 'true'); el.hidden = true;
  stage = document.createElement('div'); stage.className = 'tilo-stage';
  // 'encouraging' (a wrong answer) uses the thinking pose: hand on chin, gentle smile. The raised-hand art read as a wave, same as speaking.
  const ART = { encouraging: 'thinking' };
  for (const p of POSES) { const b = img(TILO.poses[ART[p] || p][SZ], 'tilo-body'); b.dataset.pose = p; bodies[p] = b; stage.append(b); }
  for (const [name, m] of Object.entries(TILO.talk.mouths)) {
    const i = img(m.files[SZ], 'tilo-mouth'); i.dataset.mouth = name; i.hidden = true;
    const f = SZ === '2x' ? 2 : 1, [ox, oy] = m.offset[SZ], [sw, sh] = m.size[SZ];   // percent of the stage, from the manifest
    i.style.left = (ox / f / BODY_W * 100) + '%'; i.style.top = (oy / f / BODY_H * 100) + '%';
    i.style.width = (sw / f / BODY_W * 100) + '%'; i.style.height = (sh / f / BODY_H * 100) + '%';
    mouths[name] = i; stage.append(i);
  }
  el.append(stage); document.body.append(el);
  bubble = document.createElement('div'); bubble.className = 'tilo-bubble'; bubble.setAttribute('aria-hidden', 'true');
  bus.addEventListener('start', e => onStart(e.detail?.key));
  bus.addEventListener('end', e => onEnd(e.detail?.key));
}

function pose() {
  if (st.pinned) return st.pinned;
  if (st.speaking && !st.emote) return 'speaking';
  if (st.emote) return st.emote;
  return st.mood;
}

function render() {
  if (!el) return;
  const show = st.track === 'A';
  el.hidden = !show; if (!show) return;
  const p = pose(); const was = el.dataset.pose;
  el.dataset.pose = p;
  for (const k of POSES) bodies[k].classList.toggle('on', k === p);
  const talking = p === 'speaking';
  for (const [n, m] of Object.entries(mouths)) m.hidden = !(talking && n === st.mouth);
  if (was && was !== p && !reduced()) { el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
  if (talking) startFlap(); else stopFlap();
  renderBubble(talking && st.uiKey);
}

// Speech bubble (Track A): shows the short prompt on screen while a spoken instruction plays; hidden otherwise.
const SHORT = { 'what sound does it start with?': 'First sound?', 'which word do the sounds make?': 'Which word?', 'how many sounds?': 'How many sounds?' };
function bubbleText() {
  const src = document.querySelector('.stage .screen h2, .stage .screen .prompt');
  const t = (src?.textContent || '').trim();
  if (SHORT[t.toLowerCase()]) return SHORT[t.toLowerCase()];
  return t.length > 26 ? t.slice(0, 24).replace(/\s+\S*$/, '') + '…' : t;
}
function renderBubble(on) {
  if (!bubble) return;
  const hdr = st.host?.closest?.('header.hdr') || null;
  const text = on && st.track === 'A' && hdr ? bubbleText() : '';
  if (text) { if (bubble.parentNode !== hdr) hdr.append(bubble); bubble.textContent = text; bubble.classList.add('on'); }
  else bubble.classList.remove('on');
}

function startFlap() {
  if (st.flapT || st.hold) return;
  if (reduced()) { st.mouth = 'mid'; for (const [n, m] of Object.entries(mouths)) m.hidden = n !== 'mid'; return; }
  let last = '';
  const step = () => {
    let n; do { n = FLAP[Math.floor(Math.random() * FLAP.length)]; } while (n === last);
    last = n; st.mouth = n;
    for (const [k, m] of Object.entries(mouths)) m.hidden = k !== n;
    st.flapT = setTimeout(step, 85 + Math.random() * 55);
  };
  step();
}
function stopFlap() { clearTimeout(st.flapT); st.flapT = 0; }

function onStart(key) {
  clearTimeout(st.offT);
  if (st.emote && key === st.emoteKey) { clearTimeout(st.emoteT); render(); return; }   // the praise / "not quite" clip itself: show the emotion, no flap
  if (st.emote) { clearTimeout(st.emoteT); st.emote = null; st.emoteKey = null; }          // a different clip follows: the voice talks again
  st.uiKey = typeof key === 'string' && key.startsWith('ui:'); st.speaking = true; render();
}
function onEnd(key) {
  if (st.emote && key === st.emoteKey) { clearTimeout(st.emoteT); st.emoteT = setTimeout(() => { st.emote = null; st.emoteKey = null; render(); }, 1100); return; }
  clearTimeout(st.offT);
  st.offT = setTimeout(() => { st.speaking = false; render(); }, 260);                     // bridges the short gaps between clips of one line
}

export const tilo = {
  // Track A only. null hides it (onboarding, Track B).
  setTrack(t) { if (!el) build(); st.track = t; render(); },
  // a new screen: back in the corner, calm, nothing pinned
  screen() {
    if (!el) build();
    st.uiKey = false; st.mood = 'idle'; st.emote = null; st.emoteKey = null; st.pinned = null; clearTimeout(st.emoteT);
    tilo.dock(st.homeHost && st.homeHost.isConnected ? st.homeHost : null); render();
  },
  // a persistent spot for this screen group (the sitting header); mount() clears it
  setHome(host) { st.homeHost = host; if (host) tilo.dock(host); },
  // put Tilo inside a host element (Home hero, end screen) or back in the fixed corner (null)
  dock(host) {
    if (!el) build();
    st.host = host;
    if (host) { el.classList.remove('corner'); el.classList.add('inline'); host.replaceChildren(el); }
    else { el.classList.remove('inline'); el.classList.add('corner'); if (el.parentNode !== document.body) document.body.append(el); }
  },
  mood(m) { if (!el) build(); st.mood = m; render(); },                                  // idle | listening
  emote(name, key, hold = 3000) { if (!el) build(); st.emote = name; st.emoteKey = key || null; clearTimeout(st.emoteT); st.emoteT = setTimeout(() => { st.emote = null; st.emoteKey = null; render(); }, hold); render(); },
  pin(name) { if (!el) build(); st.pinned = name; render(); },                            // held until the next screen, even while the voice talks
  // test hook (tools/shoot_tilo.py): freeze the flap on one mouth so a screenshot cannot race it; hold(null) resumes
  hold(n) { st.hold = n; if (n) { stopFlap(); st.mouth = n; for (const [k, m] of Object.entries(mouths)) m.hidden = k !== n; } else render(); },
  get state() { return { pose: el?.dataset.pose || null, track: st.track, speaking: st.speaking, mouth: st.mouth }; },
};
