// Runs one sitting: a list of steps from the lesson JSON (appSittings), then the mini check and rewards.
import { play, stop, mark, has } from './audio.js';
import { h, icon, pebble, village, STICKERS } from './ui.js';
import * as db from './db.js';
import { review, due } from './scheduler.js';
import { lessonById, sittingsFor, blendItems, spellWords, entry, LESSONS, options } from './content.js';
import { hear } from './screens/hear.js';
import { meet } from './screens/meet.js';
import { trace } from './screens/trace.js';
import { blend } from './screens/blend.js';
import { spellLetter, spellWord } from './screens/spell.js';
import { tricky } from './screens/tricky.js';
import { read } from './screens/read.js';
import { listen } from './screens/listen.js';
import { check } from './screens/check.js';
import { warmLetter } from './screens/warm.js';
import { gate } from './gate.js';
import { L1_STEPS } from './screens/l1steps.js';
import { LEVEL_STEPS } from './screens/levelsteps.js';

export const MINI_BAR = 0.8;   // course mini checks are 4/5 and 7/8

// Every grapheme taught before this sitting starts (track-aware), and after it ends.
export function knownBefore(track, key) {
  const out = [];
  for (const l of LESSONS) for (const s of sittingsFor(l, track)) { if (s.key === key) return out; out.push(...(s.new || [])); }
  return out;
}

export async function runSitting(app, profile, key) {
  const [lid, track, sid] = key.split(':');
  const lesson = lessonById(lid);
  const sitting = sittingsFor(lesson, track).find(s => s.key === key);
  const prog = await db.progress(profile.id);
  const results = [];
  const known = knownBefore(track, key);
  const root = h('div', { class: `sitting track-${track}` });
  const bar = h('div', { class: 'progress' }, h('i'));
  let lastInstr = null;
  const again = h('button', { class: 'speaker hdr', 'aria-label': 'Hear it again', onclick: () => lastInstr && play(lastInstr) }, icon('speaker'));
  const close = h('button', { class: 'close', 'aria-label': 'Stop and go home', onclick: () => { stop(); app.home(); } }, '×');
  const body = h('main', { class: 'stage' });
  const foot = h('footer', { class: 'foot' });
  root.append(h('header', { class: 'hdr' }, close, bar, again), body, foot);
  app.mount(root);
  let stepN = 0; const totalSteps = sitting.steps.length;
  const ctx = {
    track, lesson, sitting, profile,
    stage() { body.replaceChildren(); foot.replaceChildren(); const s = h('div', { class: 'screen', 'data-step': ctx.step || '' }); body.append(s); return s; },
    async instruct(k) { lastInstr = k; await play(k); },
    enableNext: () => {},
    next({ disabledUntil, waitFor, skippable } = {}) {
      return new Promise(res => {
        const btn = h('button', { class: 'btn primary next' }, 'Next');
        const update = () => { btn.disabled = disabledUntil ? !disabledUntil() : false; };
        ctx.enableNext = update; update();
        btn.addEventListener('click', () => { stop(); res(); });
        if (waitFor) {
          btn.hidden = true;
          const skip = h('button', { class: 'btn ghost skip' }, 'Skip');
          skip.addEventListener('click', () => { stop(); mark('skip', { step: ctx.step }); res(); });
          foot.append(skip);
          waitFor.then(() => { skip.remove(); btn.hidden = false; });
        }
        foot.append(btn);
      });
    },
    async record(item, kind, r) {
      if (!r.judged) return;
      results.push({ item, kind, correct: !!r.correct });
      await review(profile.id, item, kind, !!r.correct, prog.sittingCount || 0);
    },
    lessonSitting: letter => lesson.sittings.find(s => (s.new || []).includes(letter)),
    known: () => [...known, ...(sitting.new || [])],
    rememberWord: w => { prog.words = [...new Set([...(prog.words || []), w])]; },
    hasClip: has,
  };
  const step = n => { ctx.step = n; stepN++; bar.firstChild.style.width = Math.round(100 * stepN / (totalSteps + 1)) + '%'; mark('step', { key, step: n }); };
  let checkResult = null;
  for (const st of sitting.steps) {
    step(st);
    if (st === 'warm') {
      const cards = (await due(profile.id, prog.sittingCount || 0, track === 'A' ? 3 : 6));
      const letters = [...new Set([...cards.filter(c => c.kind === 'letter').map(c => c.item.split(':')[1]), ...known.slice(-2)])].filter(l => known.includes(l)).slice(0, track === 'A' ? 3 : 6);
      for (const l of letters) await warmLetter(ctx, l, known);
      const word = cards.find(c => (c.kind === 'real' || c.kind === 'pseudo') && entry(c.item) && options[c.item.toLowerCase()]);   // words without tap-gate options (Levels 2-4 unbuildable) are not warm-up gates
      if (word) { const r = await gate(ctx, word.item, word.kind); await ctx.record(word.item, word.kind, r); }
    } else if (st === 'hear' || st === 'meet' || st === 'trace') {
      // the new-sound steps run letter by letter: hear s, meet s, trace s, then the next letter
      if (ctx.didIntro) continue;
      ctx.didIntro = true;
      const intro = sitting.steps.filter(x => x === 'hear' || x === 'meet' || x === 'trace');
      for (const l of sitting.new) for (const x of intro) {
        ctx.step = x; mark('step', { key, step: x, letter: l });
        if (x === 'hear') await hear(ctx, l);
        if (x === 'meet') await meet(ctx, l);
        if (x === 'trace') await trace(ctx, l);
      }
    } else if (st === 'blend') {
      await blend(ctx, blendItems(lesson, sitting));
    } else if (st === 'spell') {
      let words = spellWords(lesson, sitting);
      if (track === 'B' && sitting.new?.length) words = (lesson.check?.dictation || []).slice(0, 1).concat((lesson.blendList?.real || []).slice(-1));
      if (!words.length) for (const l of sitting.new) await spellLetter(ctx, l, ctx.known());
      for (const w of words) await spellWord(ctx, w, ctx.known());
    } else if (st === 'tricky') {
      for (const hw of lesson.heart || []) if (entry(hw.word)) await tricky(ctx, hw.word);
    } else if ((lesson.level || 1) > 1 && LEVEL_STEPS[st]) {   // Levels 2-4 screens (teach, rule, attack, check, mastery)
      const r = await LEVEL_STEPS[st](ctx); if (r?.result) checkResult = r;
    } else if (st === 'read') await read(ctx);
    else if (st === 'listen') await listen(ctx);
    else if (st === 'check') checkResult = await check(ctx);
    else if (L1_STEPS[st]) checkResult = (await L1_STEPS[st](ctx)) || checkResult;
  }
  // mini check = first attempts on everything judged in this sitting
  const judged = results.length, correct = results.filter(r => r.correct).length;
  const passed = checkResult ? (checkResult.mastery ? checkResult.result === 'checked' : checkResult.result !== 'unfinished') : (judged === 0 || correct / judged >= MINI_BAR);
  const today = new Date().toISOString().slice(0, 10);
  prog.days = [...new Set([...(prog.days || []), today])];
  prog.sittingCount = (prog.sittingCount || 0) + 1;
  const prev = prog.sittings[key];
  prog.sittings[key] = { done: true, passed: passed || !!prev?.passed, correct, judged, at: Date.now(), check: checkResult?.result };
  if (checkResult) prog.lessons[lid] = { state: checkResult.result === 'checked' ? 'checked' : checkResult.result === 'miss' ? 'still_learning' : 'unfinished', correct: checkResult.correct, judged: checkResult.judged };
  let sticker = null, piece = null;
  if (track === 'A') {
    sticker = STICKERS[prog.stickers.length % STICKERS.length]; prog.stickers.push(sticker); // never withheld
    for (const l of sitting.new || []) if (!prog.village.includes(l)) { prog.village.push(l); piece = l; }
  }
  await db.saveProgress(prog);
  mark('sitting-end', { key, judged, correct, passed });
  return endScreen(app, profile, key, { judged, correct, passed, sticker, piece, prog, checkResult });
}

async function endScreen(app, profile, key, { judged, correct, passed, sticker, piece, prog, checkResult }) {
  const [, track] = key.split(':');
  const next = app.nextOpen(prog, track, key);
  const s = h('div', { class: `endscreen track-${track}` });
  if (track === 'A') s.append(pebble('cheer'));
  s.append(h('h2', {}, passed ? 'Well done!' : 'Good practice'));
  if (judged && !checkResult) s.append(h('div', { class: 'dots' }, ...Array.from({ length: judged }, (_, i) => h('i', { class: i < correct ? 'on' : '' }))),
    h('p', { class: 'score' }, `Mini check: ${correct} of ${judged} on the first try`));
  if (!passed) s.append(h('p', { class: 'prompt' }, "Let's practise this sitting again next time."));
  if (sticker) s.append(h('div', { class: 'sticker' }, sticker), h('p', { class: 'muted' }, 'You earned a sticker!'));
  if (track === 'A') s.append(village(prog.village, { justAdded: piece }));
  const row = h('div', { class: 'row' });
  // Track B fast track: "Keep going?" only after a >= 90% mini check (course fast-track note); the path still opens at 80%
  const offer = next && (track === 'A' || checkResult || !judged || correct / judged >= 0.9);
  if (offer) row.append(h('button', { class: 'btn primary keepgoing', onclick: () => app.sitting(next) }, 'Keep going?'));
  row.append(h('button', { class: 'btn ghost', onclick: () => app.home() }, 'Home'));
  s.append(row);
  app.mount(s);
  await play(passed ? 'ui:miniPass' : 'ui:miniMiss');
  if (piece) await play('ui:village'); else if (sticker) await play('ui:sticker');
  if (offer) await play('ui:keepGoing');
}
