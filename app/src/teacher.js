// The teacher: ONE module that owns every instruction clip. A learner who cannot read yet is guided by this voice.
//   prompt()   say what to do (then the stimulus), remember it so the ear button can say it again, arm the idle ladder
//   idle       no input for ~8 s: say the prompt again; ~16 s: nudge + point (a gentle highlight, or a model);
//              ~28 s: "tap the speaker to hear me again"; ~60 s: "I will wait here" and pause. Never a penalty.
//   right() / wrong()   a varied praise pool (never the same line twice running) and a correction that models the answer
//   ear        a big replay button on every screen
//   hold       press and hold any [data-say] control to hear what it is (Home nodes, Next, Skip, "This one" ...)
//   start      autoplay blocked on a web first load -> one big tap-to-start, then the prompt plays
// Timers: ?fast (the test drivers) switches the idle ladder off; ?idlefast shortens it (1.5/3/5/9 s) for a test run.
import { play, stop, wait, mark, has, playing, bus, isFast, setBlockedHandler } from './audio.js';
import { tilo } from './tilo.js';
import { screenChanged, placeEar } from './a11y.js';

const q = new URLSearchParams(location.search);
const IDLE_ON = !isFast || q.has('idle') || q.has('idlefast');
const T = q.has('idlefast') ? [1.5, 3, 5, 9] : [8, 16, 28, 60];   // seconds of no input: re-prompt, nudge+point, "tap the speaker", wait+pause
const HOLD_MS = 450;

const EAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 9.500a4.500 4.500 0 0 1 9 0c0 2.600-2 3.400-3 4.700-.7.900-.7 1.600-.7 2.300a2.800 2.800 0 0 1-5.300 1.200" stroke="currentColor" stroke-width="2.200" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.800 9.800a1.800 1.800 0 0 1 3.600 0c0 1-.7 1.400-1.300 2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M3.300 8.500a8 8 0 0 1 2-3.200M2 12.500a11 11 0 0 1 .5-2.300" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>';
const PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.500 20 12 7 19.500z" fill="currentColor"/></svg>';

const POOLS = {   // praise per kind; A-only and B-only lines are marked. "good" is the short default.
  pick: { all: ['good', 'right'], A: ['wow'], B: ['goodWork'] },
  listen: { all: ['goodListening', 'good', 'right'], A: [], B: [] },
  read: { all: ['goodReading', 'good'], A: ['wow'], B: ['goodWork'] },
  sound: { all: ['goodSounding', 'good', 'right'], A: ['wow'], B: ['goodWork'] },
  spell: { all: ['niceSpelling', 'good', 'right'], A: [], B: ['goodWork'] },
  trace: { all: ['traceGood'], A: [], B: [] },
};

const S = {
  track: 'A', prompt: null, stim: null, nudge: 'ui:idlePick', hint: null, tier: 0, base: Date.now(), paused: false, ready: false, busy: false,
  extra: null, idleAudio: false, streak: 0, lastMiss: false, lastPraise: null, hinted: false, replayFn: null, hold: null, suppressClick: 0, hintEls: [],
};
let ear = null;

const sayKey = k => (k.startsWith('ui:') || k.includes(':') ? k : `ui:${k}`);

export const teacher = {
  track: t => { S.track = t || S.track; tilo.setTrack(t === undefined ? S.track : t); },
  get playing() { return playing(); },

  // ---- lifecycle -------------------------------------------------------------------------------------------------
  start() {
    ear = document.createElement('button');
    ear.id = 'ear'; ear.className = 'ear'; ear.type = 'button'; ear.hidden = true;
    ear.setAttribute('aria-label', 'Hear it again'); ear.dataset.say = 'ui:hearAgain';
    ear.innerHTML = `<span class="ear-ic">${EAR}</span>`;
    ear.addEventListener('click', () => teacher.replay());
    document.body.append(ear);
    window.__so = window.__so || { trace: [], missing: [] }; window.__so.teacher = teacher; window.__so.tilo = tilo;   // test hooks (tools/drive_teacher.py, tools/shoot_tilo.py)
    bus.addEventListener('start', () => ear.classList.add('playing'));
    bus.addEventListener('end', e => { ear.classList.remove('playing'); if (!S.idleAudio) S.base = Date.now(); });
    // any tap: it is input (idle clock restarts), and it cuts the teacher off when it lands on a control
    document.addEventListener('pointerdown', e => {
      S.base = Date.now(); S.tier = 0; S.paused = false; teacher.clearHints(); if (S.ready) tilo.mood('listening');
      const t = e.target.closest('button, [role=button], canvas, .opt-pick');
      if (t && !t.closest('#ear') && !t.closest('#teacher-start') && playing()) { mark('interrupt', { by: t.className }); stop(); }
      const say = (t || e.target)?.closest?.('[data-say]');
      if (say && say.dataset.say) {
        clearTimeout(S.hold);
        S.hold = setTimeout(() => { S.suppressClick = Date.now(); mark('hold-say', { key: say.dataset.say }); stop(); teacher.seq(say.dataset.say.split(','), 120); }, HOLD_MS);
      }
    }, true);
    const cancel = () => clearTimeout(S.hold);
    document.addEventListener('pointerup', cancel, true); document.addEventListener('pointercancel', cancel, true);
    document.addEventListener('pointermove', e => { if (e.pressure === 0) cancel(); }, true);
    document.addEventListener('click', e => { if (Date.now() - S.suppressClick < 700) { e.stopPropagation(); e.preventDefault(); S.suppressClick = 0; } }, true);
    document.addEventListener('contextmenu', e => { if (e.target.closest('[data-say]')) e.preventDefault(); }, true);
    document.addEventListener('keydown', () => { S.base = Date.now(); S.tier = 0; S.paused = false; }, true);
    setBlockedHandler(showStart);
    setInterval(tick, 400);
  },

  // a new screen: forget the previous prompt, hint and idle clock
  newScreen({ keepRecord } = {}) {
    S.prompt = null; S.stim = null; S.extra = null; S.hint = null; S.nudge = null; S.tier = 0; S.paused = false; S.ready = false; S.replayFn = null; S.hinted = false;
    S.base = Date.now(); teacher.clearHints(); tilo.screen();
    if (ear) { ear.hidden = false; placeEar(ear); }
    screenChanged();
  },

  // ---- saying things ---------------------------------------------------------------------------------------------
  say(key) { const k = sayKey(key); return has(k) && !window.__so?.audioOff ? play(k) : Promise.resolve(true); },
  async seq(keys, gap = 180) { for (const k of keys.filter(Boolean)) { if ((await teacher.say(k)) === false) return false; await wait(gap); } return true; },

  // Say what to do, then the stimulus (the sound/word/question). The ear button runs exactly this again.
  async prompt(key, { stim, nudge, hint, replay } = {}) {
    S.prompt = key; S.stim = stim || null; S.extra = null; S.hint = hint || null; S.nudge = nudge || S.nudge || 'ui:idlePick'; S.tier = 0; S.paused = false; S.ready = false;
    if (ear) ear.hidden = false;
    S.replayFn = replay || null;
    mark('prompt', { key });
    const ok = await runPrompt();
    S.base = Date.now(); S.ready = true;
    if (ok !== false) tilo.mood('listening');   // the question is asked: Tilo waits for a tap
    return ok;
  },
  setIdle({ nudge, hint } = {}) { if (nudge) S.nudge = nudge; if (hint !== undefined) S.hint = hint; },
  setReplay(fn) { S.replayFn = fn; },
  setExtra(fn) { S.extra = fn; },
  hinted: () => { const h = S.hinted; return h; },
  clearHints() { S.hintEls.forEach(el => el.classList.remove('nudge')); S.hintEls = []; ear?.classList.remove('attn'); },
  point(...els) { teacher.clearHints(); els.flat().filter(Boolean).forEach(el => { el.classList.add('nudge'); S.hintEls.push(el); }); },

  // The ear button, the idle re-prompt, and "Hear it again" all come here.
  async replay() {
    stop(); S.base = Date.now(); S.tier = 0; S.paused = false; teacher.clearHints();
    mark('replay', { key: S.prompt });
    if (S.replayFn) return S.replayFn();
    return runPrompt();
  },

  // ---- feedback --------------------------------------------------------------------------------------------------
  // right({kind, tries}) : the praise pool. tries>1 means a second go.
  async right({ kind = 'pick', tries = 1 } = {}) {
    const pool = POOLS[kind] || POOLS.pick, tr = S.track === 'B' ? 'B' : 'A';
    let key;
    if (tries > 1) { key = 'youGotIt'; S.streak = 0; }
    else if (S.lastMiss && kind !== 'trace') { key = 'firstTry'; S.streak = 0; }
    else {
      S.streak++;
      if (S.streak >= 3 && kind !== 'trace') { key = 'threeInRow'; S.streak = 0; }
      else {
        const opts = [...pool.all, ...pool[tr]].filter(k => k !== S.lastPraise && has(`ui:${k}`));
        key = opts[Math.floor(Math.random() * opts.length)] || 'good';
      }
    }
    S.lastMiss = false; S.lastPraise = key;
    mark('praise', { key, kind });
    tilo.emote('celebrating', sayKey(key));
    return teacher.say(key);
  },
  // wrong({first, carrier, model}) : "not quite", then the right sound/word modelled (with a carrier: "This letter says ..."), then "now you try".
  async wrong({ first = true, carrier = null, model = [], ask = true } = {}) {
    S.lastMiss = true; S.streak = 0;
    mark('correct', { first, model });
    tilo.emote('encouraging', sayKey(first ? 'notQuite' : 'tryAgain'));
    if (first) return teacher.seq(['notQuite', carrier, ...model, ask && model.length ? 'yourTurn' : null]);
    return teacher.seq(['tryAgain', carrier, ...model]);
  },
  // between test items: no praise, no correction, just "next one"
  nextItem: () => teacher.say('nextOne'),
  // a self-report step (I said it / I read it): acknowledge, never grade
  ack: (kind = 'sound') => teacher.say({ sound: 'goodSounding', read: 'goodReading' }[kind] || 'good'),
  miss() { S.lastMiss = true; S.streak = 0; },
  consumeHinted() { const h = S.hinted; S.hinted = false; return h; },

  // ---- test helpers ----------------------------------------------------------------------------------------------
  get state() { return { tier: S.tier, prompt: S.prompt, paused: S.paused, ready: S.ready }; },
};

async function runPrompt() {
  const keys = Array.isArray(S.prompt) ? S.prompt : [S.prompt];
  for (const k of keys.filter(Boolean)) { if ((await teacher.say(k)) === false) return false; await wait(130); }
  if (S.stim) { const r = await S.stim(); if (r === false) return false; }
  if (S.extra && S.ready) { const r = await S.extra(); if (r === false) return false; }
  return true;
}

// ---- idle ladder ---------------------------------------------------------------------------------------------------
async function tick() {
  if (!IDLE_ON || !S.ready || S.paused || S.busy || playing() || !S.prompt) return;
  if (document.hidden || document.getElementById('teacher-start')) return;
  const el = (Date.now() - S.base) / 1000;
  let tier = -1;
  if (S.tier < 1 && el >= T[0]) tier = 1; else if (S.tier < 2 && el >= T[1]) tier = 2; else if (S.tier < 3 && el >= T[2]) tier = 3; else if (S.tier < 4 && el >= T[3]) tier = 4;
  if (tier < 0) return;
  S.tier = tier; S.busy = true; S.idleAudio = true;
  if (tier >= 2) tilo.mood('idle');   // still waiting: the idle pose
  mark('idle', { tier, key: S.prompt });
  try {
    if (tier === 1) { await (S.replayFn ? S.replayFn() : runPrompt()); tilo.mood('listening'); }
    else if (tier === 2) {
      if (typeof S.hint === 'function') { S.hinted = true; await S.hint(); }
      else { pointDefault(); }
      if (S.nudge) await teacher.say(S.nudge);
    }
    else if (tier === 3) { ear?.classList.add('attn'); await teacher.say('idleHelp'); }
    else if (tier === 4) { await teacher.say('idleWait'); S.paused = true; }
  } finally { S.busy = false; S.idleAudio = false; }
}
const DEFAULT_POINT = ['[data-hint]', '.opt-pick:not(:disabled)', '.printed.tiles .g.next', '.lettercard:not(.small)', '.foot .next:not([hidden]):not(:disabled)', '.saidit', '.foot .btn.primary', 'canvas.trace'];
function pointDefault() {
  for (const sel of DEFAULT_POINT) { const el = document.querySelector(`#app ${sel}`); if (el && el.offsetParent !== null) { teacher.point(el); return; } }
  ear?.classList.add('attn');
}

// ---- autoplay blocked: one big tap-to-start --------------------------------------------------------------------------
function showStart() {
  return new Promise(res => {
    if (document.getElementById('teacher-start')) return res();
    const o = document.createElement('div');
    o.id = 'teacher-start'; o.setAttribute('role', 'dialog');
    o.innerHTML = `<button type="button" class="startbtn" aria-label="Tap to start"><span class="ear-ic">${EAR}</span><span class="pl">${PLAY}</span></button><p>Tap to start</p>`;
    o.querySelector('button').addEventListener('click', () => { o.remove(); mark('tap-to-start'); res(); });
    document.body.append(o);
  });
}
